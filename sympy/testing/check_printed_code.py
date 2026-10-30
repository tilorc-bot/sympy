"""Check that the C, C++ and Rust code printed by a test compiles and
computes the same values as SymPy.

Code printer tests compare printed strings, e.g.
``assert rust_code(expr) == "..."``, so nothing checks that the asserted code
is valid in the target language. A test opts in to that check with the
``check_printed_code`` decorator::

    from sympy.testing.check_printed_code import check_printed_code

    @check_printed_code
    def test_sign():
        x, y = symbols('x y', real=True)
        assert rust_code(sign(x + y)) == "..."

While a decorated test runs, every snippet printed by the printers in
``TARGETS`` is recorded. When the test returns:

1. Each snippet must be fully declared by the test, and the test fails if one
   is not. This needs no compiler, so it is done in every test run. The types
   come only from what the test declares, nothing is guessed:

   - A symbol with ``integer=True`` is an ``int`` (``i32`` in Rust), and a
     symbol with ``real=True`` (and not integer) is a ``double`` (``f64``).
   - A symbol used as a boolean (an argument of ``And``, ``Or``, ``Not``, ...
     or a ``Piecewise`` condition) is a ``bool``.
   - Any other symbol must be declared with ``real=True`` or ``integer=True``.
   - Snippets that need declarations that cannot be made this way (arrays,
     matrices, codegen AST nodes, ``user_functions``, ``dereference`` and other
     non-default settings) cannot be checked, so a test that prints them
     must not use the decorator.

2. If the environment variable ``SYMPY_CHECK_PRINTED_CODE`` is set, each
   snippet is wrapped in a program that reads the values of its symbols from
   the command line and prints the snippet's value (or the value assigned).
   The test fails if the program does not compile, or if for some values it
   prints a different value than SymPy computes for the expression. The
   values are generated with Hypothesis, which reports the simplest values
   it finds that give a different value:

   - Reals are 0 or floats with an absolute value in [0.001, 10], integers
     are in [-10, 10], and values that contradict a symbol's assumptions
     (``positive=True``, ``even=True``, ...) are not used.
   - SymPy's value is computed with 30 digits (``evalf(30)``). Values for
     which it is not real (``1/x`` at 0, ``sqrt(x)`` at -1, ...) are not
     used. Infinite values must be printed exactly. Where SymPy's value is
     nan (undefined, e.g. ``atan2(0, 0)``), any printed value is right.
   - The printed value must be within a relative error of 1e-6 (or an
     absolute error of 1e-6 if SymPy's value is smaller than 1), which allows
     for rounding where a function is ill-conditioned (``acosh`` near 1).
     A boolean must be equal.

   CI does this for the tests that use the decorator::

       SYMPY_CHECK_PRINTED_CODE=1 pytest sympy/printing/tests/test_rust.py

A decorated test must print at least one C, C++ or Rust snippet.

In a Hypothesis test, put the decorator below ``@given``, so that each
example is checked and Hypothesis shrinks a failing one, and use
``@settings(deadline=None)``, since compiling takes longer than the
default deadline. See ``sympy/printing/tests/test_printed_code_hypothesis.py``.
"""
from __future__ import annotations

import functools
import math
import os
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor

from sympy.codegen.ast import CodegenAST
from sympy.core.basic import Basic
from sympy.core.numbers import Float, Integer
from sympy.core.singleton import S
from sympy.core.symbol import Dummy, Symbol
from sympy.core.traversal import preorder_traversal
from sympy.functions.elementary.piecewise import ExprCondPair
from sympy.logic.boolalg import (And, Boolean, BooleanAtom, Equivalent, ITE,
                                 Implies, Nand, Nor, Not, Or, Xnor, Xor, false,
                                 true)
from sympy.matrices.expressions.matexpr import MatrixElement, MatrixSymbol
from sympy.printing.codeprinter import CodePrinter
from sympy.tensor.indexed import Idx, Indexed


# The targets: one per printer class, each with the compiler command (run
# with the source file and output file appended), the code put before the
# program, and the names of the int, real and bool types. Only the printer classes
# themselves are checked, not subclasses.

C_HEADER = """\
#define _XOPEN_SOURCE 700
#include <math.h>
#include <stdlib.h>
"""  # M_PI, M_E, ... are POSIX, not ISO C
C99_HEADER = C_HEADER + "#include <stdbool.h>\n"
CXX_HEADER = "#include <algorithm>\n#include <cmath>\n#include <cstdlib>\n"
RUST_HEADER = """\
#![allow(unused)]
use std::f64::consts::*;
use std::f64::{INFINITY, NAN, NEG_INFINITY};
"""

GCC = ['-pedantic-errors']
# C89 allows calls to undeclared functions
C_FLAGS = [*GCC, '-Werror=implicit-function-declaration']
C_TYPES = {'int': 'int', 'real': 'double', 'bool': 'bool'}

TARGETS = {
    'C89CodePrinter': (['gcc', '-std=c89', *C_FLAGS], C_HEADER,
                       {'int': 'int', 'real': 'double', 'bool': 'int'}),
    'C99CodePrinter': (['gcc', '-std=c99', *C_FLAGS], C99_HEADER, C_TYPES),
    'C11CodePrinter': (['gcc', '-std=c11', *C_FLAGS], C99_HEADER, C_TYPES),
    'CXX98CodePrinter': (['g++', '-std=c++98', *GCC], CXX_HEADER, C_TYPES),
    'CXX11CodePrinter': (['g++', '-std=c++11', *GCC], CXX_HEADER, C_TYPES),
    'CXX17CodePrinter': (['g++', '-std=c++17', *GCC], CXX_HEADER, C_TYPES),
    'RustCodePrinter': (['rustc', '--edition=2021', '--error-format=short',
                         '-C', 'debuginfo=0'], RUST_HEADER,
                        {'int': 'i32', 'real': 'f64', 'bool': 'bool'}),
}
PRINTER_MODULES = ('sympy.printing.c', 'sympy.printing.cxx', 'sympy.printing.rust')

# Settings that change the code, but not what it needs declared
HARMLESS_SETTINGS = {'order', 'full_prec', 'human', 'precision', 'contract',
                     'strict', 'error_on_reserved', 'reserved_word_suffix', 'inline'}
# Their arguments are booleans (unlike those of isnan and other BooleanFunctions)
LOGIC = (And, Or, Not, Xor, Xnor, Nand, Nor, Implies, Equivalent, ITE)
# C printer settings that __init__ removes from the settings and stores here
C_TYPE_TABLES = ('type_aliases', 'type_mappings', 'type_headers', 'type_macros',
                 'type_func_suffixes', 'type_literal_suffixes',
                 'type_math_macro_suffixes')

ENVIRONMENT_VARIABLE = 'SYMPY_CHECK_PRINTED_CODE'
# The values of the symbols, and how close the printed value must be
BOUND = 10
SMALLEST = 1e-3
EXAMPLES = 50
TOLERANCE = 1e-6


class PrintedCodeError(AssertionError):
    """The code printed by a test decorated with ``check_printed_code`` is
    not declared or does not compile."""


def check_printed_code(test_func):
    """Decorator for a test whose printed C, C++ and Rust code must compile.

    See the docstring of :mod:`sympy.testing.check_printed_code`.
    """
    @functools.wraps(test_func)
    def wrapper(*args, **kwargs):
        snippets = []
        original = CodePrinter.doprint

        # Every C, C++ and Rust printer inherits doprint from CodePrinter and
        # no printer calls it recursively, so wrapping it here sees each
        # snippet the test prints exactly once. A passing test asserts the
        # string that doprint returned, so checking that string checks the
        # test.
        def doprint(self, expr, assign_to=None):
            code = original(self, expr, assign_to)
            if (type(self).__name__ in TARGETS
                    and type(self).__module__ in PRINTER_MODULES
                    and isinstance(code, str)):
                snippets.append(describe(self, expr, assign_to, code))
            return code

        CodePrinter.doprint = doprint  # type: ignore[method-assign]
        try:
            result = test_func(*args, **kwargs)
        finally:
            CodePrinter.doprint = original  # type: ignore[method-assign]
        run = run_snippets if os.environ.get(ENVIRONMENT_VARIABLE) else None
        check(snippets, run)
        return result
    return wrapper


def describe(printer, expr, assign_to, code):
    """Describe a printed snippet by what the test declared about it.

    Returns a dict with the printer class name, the code, the parameters
    and assigned variable as ``[printed name, kind]`` pairs (kind is
    'int', 'real', 'bool' or None when undeclared), the expression and the
    symbols of the parameters and, if the snippet cannot be checked, the
    reason.
    """
    record = {'printer': type(printer).__name__, 'code': code,
              'params': [], 'target': None, 'expr': expr, 'symbols': [],
              'reason': unsupported(printer, expr, assign_to)}
    if record['reason']:
        return record
    booleans = set()
    for node in preorder_traversal(expr):
        if isinstance(node, LOGIC):
            booleans.update(node.args)
        elif isinstance(node, ExprCondPair):
            booleans.add(node.cond)

    def declare(symbol, is_boolean):
        if is_boolean:
            kind = 'bool'
        elif symbol.is_integer:
            kind = 'int'
        elif symbol.is_real:
            kind = 'real'
        else:
            kind = None
        return [printer._print(symbol), kind]

    record['symbols'] = sorted(expr.free_symbols, key=str)
    record['params'] = [declare(s, s in booleans) for s in record['symbols']]
    if assign_to is not None:
        target = Symbol(assign_to) if isinstance(assign_to, str) else assign_to
        is_boolean = isinstance(expr, Boolean) and not isinstance(expr, Symbol)
        name, kind = declare(target, is_boolean)
        record['target'] = [name, dict(record['params']).get(name, kind)]
    bad = [name for name, _ in declared(record) if not name.isidentifier()]
    if bad:
        record['reason'] = 'symbols printed as %s' % ', '.join(bad)
    return record


def declared(snippet):
    """The [name, kind] pairs of the parameters and the assigned variable."""
    return snippet['params'] + ([snippet['target']] if snippet['target'] else [])


def unsupported(printer, expr, assign_to):
    """Why the snippet cannot be checked, or None."""
    settings = [k for k, v in printer._settings.items()
                if k not in HARMLESS_SETTINGS and v != printer._default_settings.get(k)]
    settings += [k for k in C_TYPE_TABLES
                 if getattr(printer, k, None) != getattr(type(printer), k, None)]
    if settings:
        return 'printer setting %s' % ', '.join(sorted(settings))
    if not isinstance(expr, Basic) or isinstance(expr, CodegenAST) or expr.is_Matrix:
        return 'printing a %s' % type(expr).__name__
    if expr.atoms(Indexed, Idx, MatrixSymbol, MatrixElement):
        return 'arrays'
    if expr.atoms(Dummy):
        return 'Dummy symbols'
    if not all(isinstance(s, Symbol) for s in expr.free_symbols):
        return 'free symbols that are not Symbols'
    if assign_to is not None and not isinstance(assign_to, (str, Symbol)):
        return 'assigning to a %s' % type(assign_to).__name__
    return None


def check(snippets, run=None):
    """Raise PrintedCodeError if a snippet is not fully declared or, when
    ``run`` is given, if it returns an error for a snippet.

    ``run`` takes a list of snippets and returns a list with a description
    of the problem with each, or None.
    """
    if not snippets:
        raise PrintedCodeError('@check_printed_code: the test printed no C, '
                               'C++ or Rust code')
    unique = {}
    for s in snippets:
        unique.setdefault(key(s), s)
    errors, to_run = [], []
    for s in unique.values():
        missing = [name for name, kind in declared(s) if kind is None]
        if s['reason']:
            errors.append(about(s) + 'which cannot be checked (%s), so the test '
                          'cannot use @check_printed_code' % s['reason'])
        elif missing:
            errors.append(about(s) + 'but the test does not declare the type of %s. '
                          'Create the symbols with real=True or integer=True, '
                          "e.g. Symbol('%s', real=True)" % (', '.join(missing), missing[0]))
        else:
            to_run.append(s)
    if run is not None and to_run:
        for s, error in zip(to_run, run(to_run)):
            if error is not None:
                numbered = ['%4d | %s' % (n, line)
                            for n, line in enumerate(program(s).splitlines(), 1)]
                errors.append('%s%s\nwrapped source:\n%s' % (
                    about(s), error, '\n'.join(numbered)))
    if errors:
        raise PrintedCodeError('@check_printed_code:\n\n' + '\n\n'.join(errors))


def about(snippet):
    return '%s printed\n%s\n' % (
        snippet['printer'], '\n'.join(indent(snippet['code'].splitlines(), '  > ')))


def key(snippet):
    return (snippet['printer'], snippet['code'], repr(snippet['params']),
            repr(snippet['target']), snippet['reason'])


def program(snippet):
    """A program that reads lines with values of the snippet's symbols from
    standard input and prints the snippet's value (or the value assigned)
    for each."""
    _, header, types = TARGETS[snippet['printer']]
    rust = snippet['printer'] == 'RustCodePrinter'
    lines = snippet['code'].splitlines()
    target = snippet['target']
    params = snippet['params']
    if rust:
        body = ['let mut sympy_values = sympy_line.split_whitespace();']
        body += ['let mut %s: %s = sympy_values.next().unwrap().parse().unwrap();'
                 % (name, types[kind]) for name, kind in params]
        if target is None:
            # A block, since an expression can follow declarations of
            # number constants such as GoldenRatio
            body += ['let sympy_value = {', *indent(lines, '    '), '};']
        else:
            if target[0] not in dict(params):
                body.append('let mut %s: %s;' % (target[0], types[target[1]]))
            body += [*lines, 'let sympy_value = %s;' % target[0]]
        body += ['println!("{:?}", sympy_value);', 'sympy_line.clear();']
        return ('%s\nfn main()\n{\n    let mut sympy_line = String::new();\n'
                '    while std::io::stdin().read_line(&mut sympy_line).unwrap() > 0 {\n'
                '%s\n    }\n}\n' % (header, '\n'.join(indent(body, '        '))))
    read = {'int': '(int)strtol(sympy_p, &sympy_p, 10)',
            'real': 'strtod(sympy_p, &sympy_p)',
            'bool': '(int)strtol(sympy_p, &sympy_p, 10)'}
    body = ['char *sympy_p = sympy_line;']
    body += ['%s %s = %s;' % (types[kind], name, read[kind]) for name, kind in params]
    if target is None:
        n = 0
        while n < len(lines) and (lines[n].endswith(';')
                                  or lines[n].startswith(('//', '/*'))):
            n += 1
        body += lines[:n] + ['printf("%.17g\\n", (double)(',
                             *indent(lines[n:], '    '), '));']
    else:
        if target[0] not in dict(params):
            body.append('%s %s;' % (types[target[1]], target[0]))
        body += [*lines, 'printf("%%.17g\\n", (double)%s);' % target[0]]
    body.append('fflush(stdout);')
    return ('%s#include <stdio.h>\n\nint main(void)\n{\n    char sympy_line[4096];\n'
            '    while (fgets(sympy_line, sizeof sympy_line, stdin)) {\n%s\n    }\n'
            '    return 0;\n}\n' % (header, '\n'.join(indent(body, '        '))))


def run_snippets(snippets):
    """Compile the snippets' programs and compare the values they print with
    SymPy's; return a description of the first problem with each, or None."""
    for printer in {s['printer'] for s in snippets}:
        compiler = TARGETS[printer][0][0]
        if shutil.which(compiler) is None:
            raise PrintedCodeError('%s is needed to check printed code (%s is set)'
                                   % (compiler, ENVIRONMENT_VARIABLE))
    with tempfile.TemporaryDirectory() as tmp:
        paths = [os.path.join(tmp, str(i)) for i in range(len(snippets))]
        with ThreadPoolExecutor(4) as pool:
            errors = list(pool.map(build, snippets, paths))
        return [error if error is not None else check_values(s, path)
                for s, path, error in zip(snippets, paths, errors)]


def build(snippet, executable):
    """Compile the snippet's program; return the compiler's errors, or None."""
    command = TARGETS[snippet['printer']][0]
    suffix = {'gcc': '.c', 'g++': '.cpp', 'rustc': '.rs'}[command[0]]
    path = executable + suffix
    with open(path, 'w') as f:
        f.write(program(snippet))
    libraries = [] if command[0] == 'rustc' else ['-lm']
    result = subprocess.run(command + [path, '-o', executable] + libraries,
                            cwd=os.path.dirname(path), capture_output=True, text=True)
    if result.returncode:
        return 'which does not compile. %s:\n%s' % (' '.join(command), '\n'.join(
            indent(result.stderr.replace(path, 'snippet' + suffix).splitlines(), '  ')))
    return None


class Program:
    """A running snippet program, which is restarted if it exits."""

    def __init__(self, executable):
        self.executable = executable
        self.process = None

    def value(self, arguments):
        """The line the program prints for the arguments, or raise
        PrintedCodeError if it exits."""
        if self.process is None:
            self.process = subprocess.Popen(
                [self.executable], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True)
        try:
            self.process.stdin.write(' '.join(arguments) + '\n')
            self.process.stdin.flush()
            output = self.process.stdout.readline()
        except BrokenPipeError:
            output = ''
        if not output:
            process, self.process = self.process, None
            process.stdin.close()
            status = process.wait()
            raise PrintedCodeError('which exits with status %d' % status
                                   + (':\n' + process.stderr.read().strip()))
        return output.strip()

    def close(self):
        if self.process is not None:
            self.process.stdin.close()
            self.process.wait()
            self.process.stdout.close()
            self.process.stderr.close()


def check_values(snippet, executable):
    """Compare the values printed by the compiled program with SymPy's for
    values of the symbols generated with Hypothesis; return a description
    of a difference, or None."""
    from hypothesis import HealthCheck, assume, given, settings, strategies as st
    from hypothesis.errors import Unsatisfiable

    rust = snippet['printer'] == 'RustCodePrinter'
    names = [name for name, _ in snippet['params']]
    running = Program(executable)

    def compare(values):
        expected = sympy_value(snippet, values)
        if names:
            assume(expected is not None)
        arguments = [str(v).lower() if rust else str(int(v)) if isinstance(v, bool)
                     else repr(v) for v in values]
        given_values = ', '.join('%s = %r' % (n, v) for n, v in zip(names, values))
        given_values = ' for ' + given_values if given_values else ''
        try:
            output = running.value(arguments)
        except PrintedCodeError as e:
            raise PrintedCodeError(str(e).replace(':', given_values + ':', 1))
        value = {'true': 1.0, 'false': 0.0}.get(output)
        if value is None:
            value = float(output)
        # nan means that the value is undefined (e.g. atan2(0, 0)), so any
        # printed value is right
        if not (value == expected or math.isnan(expected)
                or abs(value - expected) <= TOLERANCE * max(1.0, abs(expected))):
            raise PrintedCodeError('which prints %s%s, but SymPy computes %r for %s' % (
                output, given_values, expected, snippet['expr']))

    try:
        if not names:
            if sympy_value(snippet, []) is None:
                return 'whose value SymPy does not compute as a real number'
            compare([])
        else:
            strategies = [symbol_values(symbol, kind, st) for symbol, (_, kind)
                          in zip(snippet['symbols'], snippet['params'])]
            settings(max_examples=EXAMPLES, deadline=None, database=None,
                     derandomize=True, report_multiple_bugs=False,
                     suppress_health_check=list(HealthCheck),
                     )(given(st.tuples(*strategies))(compare))()
    except PrintedCodeError as e:
        return str(e)
    except Unsatisfiable:
        return ('for which no values of the symbols were found for which SymPy '
                'computes a real number')
    finally:
        running.close()
    return None


def symbol_values(symbol, kind, st):
    """A strategy for values of the symbol that agree with its assumptions."""
    if kind == 'bool':
        return st.booleans()
    if kind == 'int':
        values = st.integers(-BOUND, BOUND)
    else:
        # Not tiny, so that products like x*x do not underflow
        values = st.one_of(st.just(0.0), st.floats(-BOUND, -SMALLEST),
                           st.floats(SMALLEST, BOUND))
    assumptions = [k for k, v in symbol.assumptions0.items() if v]
    return values.filter(lambda v: all(
        getattr(sympy_number(kind, v), 'is_' + k) for k in assumptions))


def sympy_number(kind, value):
    if kind == 'bool':
        return true if value else false
    # Float(value, 30) is exactly the value of the float
    return Integer(value) if kind == 'int' else Float(value, 30)


def sympy_value(snippet, values):
    """SymPy's value of the snippet's expression as a float (1.0 or 0.0 for
    a boolean, and possibly infinite or nan), or None if it is not real."""
    try:
        value = snippet['expr'].xreplace({
            symbol: sympy_number(kind, v)
            for symbol, (_, kind), v in zip(snippet['symbols'], snippet['params'], values)})
        if isinstance(value, BooleanAtom):
            return float(value == true)
        if isinstance(value, Boolean):
            return None
        value = value.doit().evalf(30)
    except (ArithmeticError, ValueError):  # e.g. Mod(x, 0)
        return None
    if not value.is_Number or value is S.ComplexInfinity:
        return None
    return float(value)


def indent(lines, prefix):
    return [prefix + line for line in lines]
