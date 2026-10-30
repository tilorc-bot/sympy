"""Check that the C, C++ and Rust code printed by a test compiles and
computes the same values as SymPy.

Code printer tests only compare strings. A test opts in to checking the
code with a decorator::

    from sympy.testing.check_printed_code import check_printed_code

    @check_printed_code
    def test_sign():
        x, y = symbols('x y', real=True)
        assert rust_code(sign(x + y)) == "..."

The code is only compiled if SYMPY_CHECK_PRINTED_CODE is set, as in CI::

    SYMPY_CHECK_PRINTED_CODE=1 pytest sympy/printing/tests/test_rust.py

In every run, a decorated test fails if a symbol in its printed code has no
type: integer=True gives an int, real=True a double, and a symbol used in
And, Or, Not or a Piecewise condition a bool. It also fails if it prints no
C, C++ or Rust code, or code that can't be checked yet (arrays, matrices,
most non-default printer settings).

With SYMPY_CHECK_PRINTED_CODE set, the code is also run: it is wrapped in a
program that reads values of its symbols from standard input and prints its
value. The test fails if that value differs from SymPy's evalf(30) value by
more than TOLERANCE. Hypothesis generates the values (see symbol_values())
and reports the simplest ones that give a different value. Values for which
SymPy's value isn't real are skipped, and where it is nan (e.g. atan2(0, 0))
any printed value is accepted.

In a Hypothesis test, put the decorator below @given and use
@settings(deadline=None). expressions() generates expressions to print. The
symbols then take the FIXED_VALUES, since Hypothesis tests can't be nested.
"""
from __future__ import annotations

import functools
import itertools
import math
import os
import shutil
import subprocess
import tempfile
import textwrap
from typing import NamedTuple

from sympy.codegen.ast import CodegenAST
from sympy.core.add import Add
from sympy.core.basic import Basic
from sympy.core.mod import Mod
from sympy.core.mul import Mul
from sympy.core.numbers import Float, I, Integer, Rational, nan, oo, zoo
from sympy.core.power import Pow
from sympy.core.singleton import S
from sympy.core.symbol import Symbol, symbols
from sympy.core.traversal import preorder_traversal
from sympy.functions.elementary.complexes import Abs, sign
from sympy.functions.elementary.exponential import exp, log
from sympy.functions.elementary.integers import floor
from sympy.functions.elementary.miscellaneous import Max, Min, sqrt
from sympy.functions.elementary.piecewise import ExprCondPair
from sympy.functions.elementary.trigonometric import sin
from sympy.logic.boolalg import (And, Boolean, BooleanAtom, Equivalent, ITE,
                                 Implies, Nand, Nor, Not, Or, Xnor, Xor, false,
                                 true)
from sympy.matrices.expressions.matexpr import MatrixElement, MatrixSymbol
from sympy.printing.c import C89CodePrinter
from sympy.printing.codeprinter import CodePrinter
from sympy.tensor.indexed import Idx, Indexed


class Target(NamedTuple):
    command: list[str]
    header: str
    types: dict[str, str]


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
    'C89CodePrinter': Target(['gcc', '-std=c89', *C_FLAGS], C_HEADER,
                             {'int': 'int', 'real': 'double', 'bool': 'int'}),
    'C99CodePrinter': Target(['gcc', '-std=c99', *C_FLAGS], C99_HEADER, C_TYPES),
    'C11CodePrinter': Target(['gcc', '-std=c11', *C_FLAGS], C99_HEADER, C_TYPES),
    'CXX98CodePrinter': Target(['g++', '-std=c++98', *GCC], CXX_HEADER, C_TYPES),
    'CXX11CodePrinter': Target(['g++', '-std=c++11', *GCC], CXX_HEADER, C_TYPES),
    'CXX17CodePrinter': Target(['g++', '-std=c++17', *GCC], CXX_HEADER, C_TYPES),
    'RustCodePrinter': Target(['rustc', '--edition=2021', '--error-format=short',
                               '-C', 'debuginfo=0'],
                              RUST_HEADER, {'int': 'i32', 'real': 'f64', 'bool': 'bool'}),
}
PRINTER_MODULES = ('sympy.printing.c', 'sympy.printing.cxx', 'sympy.printing.rust')

# Settings that change how the code is written, but not what it needs declared
HARMLESS_SETTINGS = {'order', 'full_prec', 'human', 'precision', 'contract',
                     'strict', 'error_on_reserved', 'reserved_word_suffix', 'inline'}
# type_aliases and the other type settings of the C printers, which they
# keep as attributes instead of in _settings
C_TYPE_SETTINGS = [name for name in vars(C89CodePrinter) if name.startswith('type_')]
# Their arguments are booleans (unlike those of isnan and other BooleanFunctions)
LOGIC = (And, Or, Not, Xor, Xnor, Nand, Nor, Implies, Equivalent, ITE)

BOUND = 10
SMALLEST = 1e-3
EXAMPLES = 50
TOLERANCE = 1e-6  # allows for ill-conditioned functions, e.g. acosh near 1
FIXED_VALUES = {'bool': [False, True], 'int': [0, 1, -1, 2, -3, 7],
                'real': [0.0, 1.0, -1.0, 0.5, -2.5, 3.75]}


def compiling():
    """Whether SYMPY_CHECK_PRINTED_CODE is set (and not to 0)."""
    return os.environ.get('SYMPY_CHECK_PRINTED_CODE', '') not in ('', '0')


class PrintedCodeError(AssertionError):
    """Code printed by a test decorated with ``check_printed_code`` is wrong."""


def check_printed_code(test_func):
    """While the test runs, CodePrinter.doprint is replaced by a wrapper that
    checks the code the C, C++ and Rust printers print (see check()). When
    the test returns, it fails if any of that code is wrong.
    """
    @functools.wraps(test_func)
    def wrapper(*args, **kwargs):
        printed, problems = set(), []
        original = CodePrinter.doprint

        # The printers inherit doprint and none calls it recursively, so this
        # sees everything the test prints once
        def doprint(self, expr, assign_to=None):
            code = original(self, expr, assign_to)
            name = type(self).__name__
            # Only the classes in TARGETS, not subclasses defined by tests
            if (name in TARGETS and type(self).__module__ in PRINTER_MODULES
                    and isinstance(code, str)
                    and (name, code, expr, assign_to) not in printed):
                printed.add((name, code, expr, assign_to))
                problem = check(self, expr, assign_to, code)
                if problem:
                    problems.append('%s printed\n\n%s\n\n%s' % (
                        name, textwrap.indent(code, '    '), problem))
            return code

        CodePrinter.doprint = doprint  # type: ignore[method-assign]
        try:
            result = test_func(*args, **kwargs)
        finally:
            CodePrinter.doprint = original  # type: ignore[method-assign]
        if not printed:
            raise PrintedCodeError('The test printed no C, C++ or Rust code, so it '
                                   "shouldn't use @check_printed_code.")
        if problems:
            raise PrintedCodeError('\n\n'.join(problems))
        return result
    return wrapper


def check(printer, expr, assign_to, code):
    """What is wrong with the code that printer printed for expr (assigned to
    assign_to), or None.

    >>> from sympy import Symbol, sin
    >>> from sympy.printing.c import C99CodePrinter
    >>> from sympy.testing.check_printed_code import check
    >>> print(check(C99CodePrinter(), sin(Symbol('x')), None, 'sin(x)'))
    The type of x is unknown, so this can't be compiled. Create x with
    real=True or integer=True, e.g. Symbol('x', real=True).

    With x = Symbol('x', real=True), there is nothing wrong, unless
    SYMPY_CHECK_PRINTED_CODE is set and the code doesn't compile or compute
    the right values (see run_code()).
    """
    reason = unsupported(printer, expr, assign_to)
    if reason:
        return textwrap.fill("This can't be checked, since %s, so the test can't "
                             "use @check_printed_code." % reason, 72)
    booleans = set()
    for node in preorder_traversal(expr):
        if isinstance(node, LOGIC):
            booleans.update(node.args)
        elif isinstance(node, ExprCondPair):
            booleans.add(node.cond)
    symbols = sorted(expr.free_symbols, key=str)
    params = [(printer._print(s), symbol_type(s, s in booleans)) for s in symbols]
    target = None
    if assign_to is not None:
        symbol = Symbol(assign_to) if isinstance(assign_to, str) else assign_to
        name = printer._print(symbol)
        is_boolean = isinstance(expr, Boolean) and not isinstance(expr, Symbol)
        target = (name, dict(params).get(name, symbol_type(symbol, is_boolean)))
    names = params + ([target] if target else [])

    not_names = [name for name, _ in names if not name.isidentifier()]
    if not_names:
        return textwrap.fill("This can't be checked, since %s isn't a name, so the "
                             "test can't use @check_printed_code."
                             % ' or '.join(not_names), 72)
    unknown = [name for name, type_ in names if type_ is None]
    if len(unknown) == 1:
        return textwrap.fill(
            "The type of %s is unknown, so this can't be compiled. Create %s with "
            "real=True or integer=True, e.g. Symbol(%r, real=True)."
            % (unknown[0], unknown[0], unknown[0]), 72)
    if unknown:
        return textwrap.fill(
            "The types of %s are unknown, so this can't be compiled. Create them "
            "with real=True or integer=True, e.g. Symbol(%r, real=True)."
            % (' and '.join(unknown), unknown[0]), 72)
    if compiling():
        return run_code(type(printer).__name__, code, params, target, expr, symbols)
    return None


def symbol_type(symbol, is_boolean):
    """'bool', 'int' or 'real', or None if the symbol's type is unknown."""
    if is_boolean:
        return 'bool'
    if symbol.is_integer:
        return 'int'
    if symbol.is_real:
        return 'real'
    return None


def unsupported(printer, expr, assign_to):
    """Why the code that printer printed for expr can't be checked, or None.

    >>> from sympy import MatrixSymbol
    >>> from sympy.printing.c import C99CodePrinter
    >>> from sympy.testing.check_printed_code import unsupported
    >>> unsupported(C99CodePrinter(), MatrixSymbol('A', 2, 2)[0, 1], None)
    "it uses arrays or matrices, whose sizes can't be declared"
    """
    for name, value in printer._settings.items():
        if name not in HARMLESS_SETTINGS and value != printer._default_settings.get(name):
            return "it's printed with the setting %s, which can need other declarations" % name
    for name in C_TYPE_SETTINGS:
        if getattr(printer, name, None) != getattr(type(printer), name, None):
            return "it's printed with the setting %s, which can need other declarations" % name
    if isinstance(expr, CodegenAST) or not isinstance(expr, Basic):
        return "it's a %s, not an expression" % type(expr).__name__
    if (expr.is_Matrix or expr.atoms(Indexed, Idx, MatrixSymbol, MatrixElement)
            or not isinstance(assign_to, (str, Symbol, type(None)))):
        return "it uses arrays or matrices, whose sizes can't be declared"
    return None


def program(printer_name, code, params, target):
    """A program that reads lines with values of params from standard input
    and prints the code's value (or the value assigned to target) for each.

    >>> from sympy.testing.check_printed_code import program
    >>> print(program('C99CodePrinter', 'fmod(x, 2)', [('x', 'real')], None))
    #define _XOPEN_SOURCE 700
    #include <math.h>
    #include <stdlib.h>
    #include <stdbool.h>
    #include <stdio.h>
    <BLANKLINE>
    int main(void)
    {
        char sympy_line[4096];
        while (fgets(sympy_line, sizeof sympy_line, stdin)) {
            char *sympy_p = sympy_line;
            double x = strtod(sympy_p, &sympy_p);
            printf("%.17g\\n", (double)(
                fmod(x, 2)
            ));
            fflush(stdout);
        }
        return 0;
    }
    <BLANKLINE>
    """
    _, header, types = TARGETS[printer_name]
    lines = code.splitlines()
    if printer_name == 'RustCodePrinter':
        body = ['let mut sympy_values = sympy_line.split_whitespace();']
        body += ['let mut %s: %s = sympy_values.next().unwrap().parse().unwrap();'
                 % (name, types[type_]) for name, type_ in params]
        if target is None:
            # A block, since an expression can follow declarations of
            # number constants such as GoldenRatio
            body += ['let sympy_value = {', *['    ' + line for line in lines], '};']
        else:
            if target[0] not in dict(params):
                body.append('let mut %s: %s;' % (target[0], types[target[1]]))
            body += [*lines, 'let sympy_value = %s;' % target[0]]
        body += ['println!("{:?}", sympy_value);', 'sympy_line.clear();']
        return ('%s\nfn main()\n{\n    let mut sympy_line = String::new();\n'
                '    while std::io::stdin().read_line(&mut sympy_line).unwrap() > 0 {\n'
                '%s\n    }\n}\n' % (header, textwrap.indent('\n'.join(body), '        ')))
    read = {'int': '(int)strtol(sympy_p, &sympy_p, 10)',
            'real': 'strtod(sympy_p, &sympy_p)',
            'bool': '(int)strtol(sympy_p, &sympy_p, 10)'}
    body = ['char *sympy_p = sympy_line;']
    body += ['%s %s = %s;' % (types[type_], name, read[type_]) for name, type_ in params]
    if target is None:
        n = 0
        while n < len(lines) and (lines[n].endswith(';')
                                  or lines[n].startswith(('//', '/*'))):
            n += 1
        body += lines[:n] + ['printf("%.17g\\n", (double)(',
                             *['    ' + line for line in lines[n:]], '));']
    else:
        if target[0] not in dict(params):
            body.append('%s %s;' % (types[target[1]], target[0]))
        body += [*lines, 'printf("%%.17g\\n", (double)%s);' % target[0]]
    body.append('fflush(stdout);')
    return ('%s#include <stdio.h>\n\nint main(void)\n{\n    char sympy_line[4096];\n'
            '    while (fgets(sympy_line, sizeof sympy_line, stdin)) {\n%s\n    }\n'
            '    return 0;\n}\n' % (header, textwrap.indent('\n'.join(body), '        ')))


def run_code(printer_name, code, params, target, expr, symbols):
    """What is wrong with the code when it is compiled into program() and run,
    or None. It must print SymPy's value of expr for the values of symbols
    (whose names and types are params) from check_values()."""
    command = TARGETS[printer_name].command
    if shutil.which(command[0]) is None:
        raise PrintedCodeError('%s is needed to check printed code, since '
                               'SYMPY_CHECK_PRINTED_CODE is set' % command[0])
    wrapped = program(printer_name, code, params, target)
    suffix = {'gcc': '.c', 'g++': '.cpp', 'rustc': '.rs'}[command[0]]
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'code' + suffix)
        executable = os.path.join(tmp, 'code')
        with open(path, 'w') as f:
            f.write(wrapped)
        libraries = [] if command[0] == 'rustc' else ['-lm']
        result = subprocess.run(command + [path, '-o', executable] + libraries,
                                cwd=tmp, capture_output=True, text=True)
        if result.returncode:
            # Not the notes and the code around the error, which the source shows
            errors = ''.join(line.replace(path, 'code' + suffix) + '\n'
                             for line in result.stderr.splitlines() if 'error' in line)
            numbered = ''.join('%4d | %s\n' % (n, line)
                               for n, line in enumerate(wrapped.splitlines(), 1))
            return "This doesn't compile. %s says\n\n%s\nabout\n\n%s" % (
                ' '.join(command), textwrap.indent(errors, '    '),
                textwrap.indent(numbered, '    '))
        return check_values(printer_name, expr, symbols, params, executable)


class Program:
    """A running program from program(), which is restarted if it exits."""

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
            raise PrintedCodeError('exits with status %d\n\n%s' % (
                status, textwrap.indent(process.stderr.read(), '    ')))
        return output.strip()

    def close(self):
        if self.process is not None:
            self.process.stdin.close()
            self.process.wait()
            self.process.stdout.close()
            self.process.stderr.close()


def check_values(printer_name, expr, symbols, params, executable):
    """What is wrong with the values that the compiled program prints, or None.

    The values of symbols are generated with Hypothesis or, inside a
    Hypothesis test, are FIXED_VALUES (see fixed_values()).
    """
    from hypothesis import (HealthCheck, assume, currently_in_test_context, given,
                            settings, strategies as st)
    from hypothesis.errors import Unsatisfiable

    names = [name for name, _ in params]
    types = [type_ for _, type_ in params]
    running = Program(executable)

    def compare(values):
        """Return False if SymPy's value isn't real, else raise
        PrintedCodeError if the printed value is different."""
        expected = sympy_value(expr, symbols, types, values)
        if expected is None:
            return False
        arguments = [str(v).lower() if printer_name == 'RustCodePrinter'
                     else str(int(v)) if isinstance(v, bool) else repr(v) for v in values]
        given_values = ' for ' + ', '.join('%s = %r' % (n, v) for n, v in zip(names, values))
        try:
            output = running.value(arguments)
        except PrintedCodeError as e:
            raise PrintedCodeError('This %s%s.' % (e, given_values if names else ''))
        value = {'true': 1.0, 'false': 0.0}.get(output)
        if value is None:
            value = float(output)
        # nan means undefined, e.g. atan2(0, 0)
        if not (value == expected or math.isnan(expected)
                or abs(value - expected) <= TOLERANCE * max(1.0, abs(expected))):
            raise PrintedCodeError("This gives %s%s, but SymPy's value of %s is %r." % (
                output, given_values if names else '', expr, expected))
        return True

    no_values = ("SymPy's value of %s isn't a real number for any of the values "
                 "tried, so this can't be checked." % expr)
    try:
        if not names:
            if not compare([]):
                return "SymPy's value of %s isn't a real number, so this can't be checked." % expr
        elif currently_in_test_context():
            # Hypothesis tests can't be nested
            if not sum(compare(values) for values in fixed_values(symbols, types)):
                return no_values
        else:
            @settings(max_examples=EXAMPLES, deadline=None, database=None,
                      derandomize=True, report_multiple_bugs=False,
                      suppress_health_check=list(HealthCheck))
            @given(st.tuples(*[symbol_values(s, t, st) for s, t in zip(symbols, types)]))
            def generated(values):
                assume(compare(values))
            generated()
    except PrintedCodeError as e:
        return str(e)
    except Unsatisfiable:
        return no_values
    finally:
        running.close()
    return None


def fixed_values(symbols, types):
    """Up to EXAMPLES combinations of FIXED_VALUES for the symbols that agree
    with their assumptions.

    >>> from sympy import Symbol
    >>> from sympy.testing.check_printed_code import fixed_values
    >>> fixed_values([Symbol('n', integer=True, positive=True)], ['int'])
    [(1,), (2,), (7,)]
    """
    choices = [[v for v in FIXED_VALUES[t] if agrees(s, t, v)]
               for s, t in zip(symbols, types)]
    combinations = list(itertools.product(*choices))
    return combinations[::max(1, len(combinations) // EXAMPLES)][:EXAMPLES]


def agrees(symbol, type_, value):
    """Whether the value agrees with the symbol's assumptions."""
    return type_ == 'bool' or all(getattr(sympy_number(type_, value), 'is_' + k)
                                  for k, v in symbol.assumptions0.items() if v)


def symbol_values(symbol, type_, st):
    """A strategy for values of the symbol that agree with its assumptions:
    0 or floats with an absolute value in [SMALLEST, BOUND] for reals, and
    integers in [-BOUND, BOUND]."""
    if type_ == 'bool':
        return st.booleans()
    if type_ == 'int':
        values = st.integers(-BOUND, BOUND)
    else:
        # Not tiny, so that products like x*x do not underflow
        values = st.one_of(st.just(0.0), st.floats(-BOUND, -SMALLEST),
                           st.floats(SMALLEST, BOUND))
    return values.filter(lambda v: agrees(symbol, type_, v))


def sympy_number(type_, value):
    if type_ == 'bool':
        return true if value else false
    # Float(value, 30) is exactly the value of the float
    return Integer(value) if type_ == 'int' else Float(value, 30)


def sympy_value(expr, symbols, types, values):
    """SymPy's value of expr for the values of symbols as a float (1.0 or 0.0
    for a boolean, and possibly infinite or nan), or None if it isn't real.

    >>> from sympy import Symbol, sqrt
    >>> from sympy.testing.check_printed_code import sympy_value
    >>> x = Symbol('x', real=True)
    >>> sympy_value(sqrt(x), [x], ['real'], [4.0]), sympy_value(sqrt(x), [x], ['real'], [-1.0])
    (2.0, None)
    """
    try:
        value = expr.xreplace({s: sympy_number(t, v) for s, t, v in zip(symbols, types, values)})
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


def expressions():
    """A Hypothesis strategy for expressions in real x, y and integer i, j,
    such as Max(i, y) or sin(x)**2 + floor(j/2)."""
    from hypothesis import strategies as st

    x, y = symbols('x y', real=True)
    i, j = symbols('i j', integer=True)
    leaves = st.sampled_from([x, y, i, j, S(2), S(-3), Rational(1, 2), Float(-2.5)])
    binary = st.sampled_from([Add, Mul, Pow, Mod, Min, Max])
    unary = st.sampled_from([sin, exp, log, sqrt, Abs, floor, sign])

    def apply(f, *args):
        try:
            return f(*args)
        except (ValueError, TypeError, ZeroDivisionError):
            return nan  # e.g. Min of a complex number

    return st.recursive(
        leaves,
        lambda e: st.builds(apply, binary, e, e) | st.builds(apply, unary, e),
        max_leaves=5,
    ).filter(lambda e: e.free_symbols and not e.has(nan, zoo, oo, -oo, I))
