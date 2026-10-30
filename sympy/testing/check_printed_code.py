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
more than TOLERANCE. Hypothesis generates the values (see values_strategy())
and reports the simplest ones that give a different value. Values for which
SymPy's value isn't real are skipped, and where it is nan (e.g. atan2(0, 0))
any printed value is accepted.

In a Hypothesis test, put the decorator below @given and use
@settings(deadline=None). The symbols then take the FIXED_VALUES, since
Hypothesis tests can't be nested.
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
from typing import NamedTuple, cast

from sympy.codegen.ast import CodegenAST
from sympy.core.basic import Basic
from sympy.core.numbers import Float, Integer
from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.core.traversal import preorder_traversal
from sympy.functions.elementary.piecewise import ExprCondPair
from sympy.logic.boolalg import (And, Boolean, BooleanAtom, Equivalent, ITE,
                                 Implies, Nand, Nor, Not, Or, Xnor, Xor, false,
                                 true)
from sympy.matrices.expressions.matexpr import MatrixElement, MatrixSymbol
from sympy.printing.c import C89CodePrinter
from sympy.printing.codeprinter import CodePrinter
from sympy.tensor.indexed import Idx, Indexed

# The printed name of a variable and its type, 'int', 'real' or 'bool',
# e.g. ('x', 'real')
Declaration = tuple[str, str]


class Target(NamedTuple):
    command: list[str]
    header: str
    type_names: dict[str, str]


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
C_TYPE_NAMES = {'int': 'int', 'real': 'double', 'bool': 'bool'}

TARGETS = {
    'C89CodePrinter': Target(['gcc', '-std=c89', *C_FLAGS], C_HEADER,
                             {'int': 'int', 'real': 'double', 'bool': 'int'}),
    'C99CodePrinter': Target(['gcc', '-std=c99', *C_FLAGS], C99_HEADER, C_TYPE_NAMES),
    'C11CodePrinter': Target(['gcc', '-std=c11', *C_FLAGS], C99_HEADER, C_TYPE_NAMES),
    'CXX98CodePrinter': Target(['g++', '-std=c++98', *GCC], CXX_HEADER, C_TYPE_NAMES),
    'CXX11CodePrinter': Target(['g++', '-std=c++11', *GCC], CXX_HEADER, C_TYPE_NAMES),
    'CXX17CodePrinter': Target(['g++', '-std=c++17', *GCC], CXX_HEADER, C_TYPE_NAMES),
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
LOGIC_FUNCTIONS = (And, Or, Not, Xor, Xnor, Nand, Nor, Implies, Equivalent, ITE)

BOUND = 10
SMALLEST = 1e-3
EXAMPLES = 50
TOLERANCE = 1e-6  # allows for ill-conditioned functions, e.g. acosh near 1
FIXED_VALUES: dict[str, list] = {'bool': [False, True], 'int': [0, 1, -1, 2, -3, 7],
                                 'real': [0.0, 1.0, -1.0, 0.5, -2.5, 3.75]}


def compiling_enabled() -> bool:
    """Whether SYMPY_CHECK_PRINTED_CODE is set (and not to 0)."""
    return os.environ.get('SYMPY_CHECK_PRINTED_CODE', '') not in ('', '0')


class PrintedCodeError(AssertionError):
    """Code printed by a test decorated with ``check_printed_code`` is wrong."""


def check_printed_code(test_func):
    """Make the test fail if C, C++ or Rust code that it prints is wrong (see
    find_problem() for what is checked).

    While the test runs, CodePrinter.doprint is replaced by a wrapper that
    checks what these printers print. The problems are raised when the test
    returns.
    """
    @functools.wraps(test_func)
    def wrapper(*args, **kwargs):
        printed, problems = set(), []
        original_doprint = CodePrinter.doprint

        # The printers inherit doprint and none calls it recursively, so this
        # sees everything the test prints once
        def doprint(self, expr, assign_to=None):
            code = original_doprint(self, expr, assign_to)
            printer_name = type(self).__name__
            # Only the classes in TARGETS, not subclasses defined by tests
            if (printer_name in TARGETS and type(self).__module__ in PRINTER_MODULES
                    and isinstance(code, str)
                    and (printer_name, code, expr, assign_to) not in printed):
                printed.add((printer_name, code, expr, assign_to))
                problem = find_problem(self, expr, assign_to, code)
                if problem:
                    problems.append('%s printed\n\n%s\n\n%s' % (
                        printer_name, textwrap.indent(code, '    '), problem))
            return code

        CodePrinter.doprint = doprint  # type: ignore[method-assign]
        try:
            result = test_func(*args, **kwargs)
        finally:
            CodePrinter.doprint = original_doprint  # type: ignore[method-assign]
        if not printed:
            raise PrintedCodeError('The test printed no C, C++ or Rust code, so it '
                                   "shouldn't use @check_printed_code.")
        if problems:
            raise PrintedCodeError('\n\n'.join(problems))
        return result
    return wrapper


def find_problem(printer: CodePrinter, expr: Basic, assign_to: str | Basic | None,
                 code: str) -> str | None:
    """Return a description of what is wrong with code, which printer printed
    for expr (assigned to assign_to, if it isn't None), or None.

    Without SYMPY_CHECK_PRINTED_CODE, this only checks that the code could be
    compiled: that each of its symbols has a type, and that nothing in it is
    unsupported (see unsupported_reason()). With it, this also compiles and
    runs the code, and compares its values with SymPy's (see
    find_run_problem()).

    >>> from sympy import Symbol, sin
    >>> from sympy.printing.c import C99CodePrinter
    >>> from sympy.testing.check_printed_code import find_problem
    >>> print(find_problem(C99CodePrinter(), sin(Symbol('x')), None, 'sin(x)'))
    The type of x is unknown, so this can't be compiled. Create x with
    real=True or integer=True, e.g. Symbol('x', real=True).
    """
    reason = unsupported_reason(printer, expr, assign_to)
    if reason:
        return textwrap.fill("This can't be checked, since %s, so the test can't "
                             "use @check_printed_code." % reason, 72)
    booleans: set[Basic] = set()
    for node in preorder_traversal(expr):
        if isinstance(node, LOGIC_FUNCTIONS):
            booleans.update(node.args)
        elif isinstance(node, ExprCondPair):
            booleans.add(node.cond)
    symbols = sorted(expr.free_symbols, key=str)
    parameters = [(printer._print(symbol), symbol_type(symbol, symbol in booleans))
                  for symbol in symbols]
    assigned = None
    if assign_to is not None:
        symbol = Symbol(assign_to) if isinstance(assign_to, str) else assign_to
        name = printer._print(symbol)
        is_boolean = isinstance(expr, Boolean) and not isinstance(expr, Symbol)
        assigned = (name, dict(parameters).get(name, symbol_type(symbol, is_boolean)))
    declarations = parameters + ([assigned] if assigned else [])

    invalid_names = [name for name, _ in declarations if not name.isidentifier()]
    if invalid_names:
        return textwrap.fill("This can't be checked, since %s isn't a name, so the "
                             "test can't use @check_printed_code."
                             % ' or '.join(invalid_names), 72)
    untyped = [name for name, type_name in declarations if type_name is None]
    if len(untyped) == 1:
        return textwrap.fill(
            "The type of %s is unknown, so this can't be compiled. Create %s with "
            "real=True or integer=True, e.g. Symbol(%r, real=True)."
            % (untyped[0], untyped[0], untyped[0]), 72)
    if untyped:
        return textwrap.fill(
            "The types of %s are unknown, so this can't be compiled. Create them "
            "with real=True or integer=True, e.g. Symbol(%r, real=True)."
            % (' and '.join(untyped), untyped[0]), 72)
    if compiling_enabled():
        # Every type is known now
        return find_run_problem(type(printer).__name__, code,
                                cast('list[Declaration]', parameters),
                                cast('Declaration | None', assigned), expr, symbols)
    return None


def symbol_type(symbol: Basic, is_boolean: bool) -> str | None:
    """Return 'bool', 'int' or 'real', or None if the symbol's type is unknown."""
    if is_boolean:
        return 'bool'
    if symbol.is_integer:
        return 'int'
    if symbol.is_real:
        return 'real'
    return None


def unsupported_reason(printer: CodePrinter, expr: Basic,
                       assign_to: str | Basic | None) -> str | None:
    """Return why the code that printer printed for expr (assigned to
    assign_to) can't be checked, or None if it can.

    >>> from sympy import MatrixSymbol
    >>> from sympy.printing.c import C99CodePrinter
    >>> from sympy.testing.check_printed_code import unsupported_reason
    >>> unsupported_reason(C99CodePrinter(), MatrixSymbol('A', 2, 2)[0, 1], None)
    "it uses arrays or matrices, whose sizes can't be declared"
    """
    for name, value in printer._settings.items():
        if name not in HARMLESS_SETTINGS and value != printer._default_settings.get(name):
            return "it's printed with the setting %s, which can need other declarations" % name
    if isinstance(printer, C89CodePrinter):
        for name in C_TYPE_SETTINGS:
            if getattr(printer, name) != getattr(type(printer), name):
                return ("it's printed with the setting %s, which can need other "
                        "declarations" % name)
    if isinstance(expr, CodegenAST) or not isinstance(expr, Basic):
        return "it's a %s, not an expression" % type(expr).__name__
    if (expr.is_Matrix or expr.atoms(Indexed, Idx, MatrixSymbol, MatrixElement)
            or not isinstance(assign_to, (str, Symbol, type(None)))):
        return "it uses arrays or matrices, whose sizes can't be declared"
    return None


def wrap_in_program(printer_name: str, code: str, parameters: list[Declaration],
                    assigned: Declaration | None) -> str:
    """Return the source of a program that reads lines with values of the
    parameters from standard input, and prints the code's value (or the value
    of the assigned variable) for each.

    >>> from sympy.testing.check_printed_code import wrap_in_program
    >>> print(wrap_in_program('C99CodePrinter', 'fmod(x, 2)', [('x', 'real')], None))
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
    _, header, type_names = TARGETS[printer_name]
    lines = code.splitlines()
    if printer_name == 'RustCodePrinter':
        body = ['let mut sympy_values = sympy_line.split_whitespace();']
        body += ['let mut %s: %s = sympy_values.next().unwrap().parse().unwrap();'
                 % (name, type_names[type_name]) for name, type_name in parameters]
        if assigned is None:
            # A block, since an expression can follow declarations of
            # number constants such as GoldenRatio
            body += ['let sympy_value = {', *['    ' + line for line in lines], '};']
        else:
            if assigned[0] not in dict(parameters):
                body.append('let mut %s: %s;' % (assigned[0], type_names[assigned[1]]))
            body += [*lines, 'let sympy_value = %s;' % assigned[0]]
        body += ['println!("{:?}", sympy_value);', 'sympy_line.clear();']
        return ('%s\nfn main()\n{\n    let mut sympy_line = String::new();\n'
                '    while std::io::stdin().read_line(&mut sympy_line).unwrap() > 0 {\n'
                '%s\n    }\n}\n' % (header, textwrap.indent('\n'.join(body), '        ')))
    read = {'int': '(int)strtol(sympy_p, &sympy_p, 10)',
            'real': 'strtod(sympy_p, &sympy_p)',
            'bool': '(int)strtol(sympy_p, &sympy_p, 10)'}
    body = ['char *sympy_p = sympy_line;']
    body += ['%s %s = %s;' % (type_names[type_name], name, read[type_name]) for name, type_name in parameters]
    if assigned is None:
        declarations_end = 0
        while declarations_end < len(lines) and (lines[declarations_end].endswith(';')
                                  or lines[declarations_end].startswith(('//', '/*'))):
            declarations_end += 1
        body += lines[:declarations_end] + ['printf("%.17g\\n", (double)(',
                             *['    ' + line for line in lines[declarations_end:]], '));']
    else:
        if assigned[0] not in dict(parameters):
            body.append('%s %s;' % (type_names[assigned[1]], assigned[0]))
        body += [*lines, 'printf("%%.17g\\n", (double)%s);' % assigned[0]]
    body.append('fflush(stdout);')
    return ('%s#include <stdio.h>\n\nint main(void)\n{\n    char sympy_line[4096];\n'
            '    while (fgets(sympy_line, sizeof sympy_line, stdin)) {\n%s\n    }\n'
            '    return 0;\n}\n' % (header, textwrap.indent('\n'.join(body), '        ')))


def find_run_problem(printer_name: str, code: str, parameters: list[Declaration],
                     assigned: Declaration | None, expr: Basic,
                     symbols: list[Basic]) -> str | None:
    """Compile the code as wrap_in_program() wraps it and run it, and return
    what is wrong with it, or None. For the values of symbols (whose names and
    types are parameters) that find_value_problem() tries, it must print
    SymPy's value of expr."""
    command = TARGETS[printer_name].command
    if shutil.which(command[0]) is None:
        raise PrintedCodeError('%s is needed to check printed code, since '
                               'SYMPY_CHECK_PRINTED_CODE is set' % command[0])
    source = wrap_in_program(printer_name, code, parameters, assigned)
    suffix = {'gcc': '.c', 'g++': '.cpp', 'rustc': '.rs'}[command[0]]
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, 'code' + suffix)
        executable = os.path.join(directory, 'code')
        with open(path, 'w') as file:
            file.write(source)
        libraries = [] if command[0] == 'rustc' else ['-lm']
        result = subprocess.run(command + [path, '-o', executable] + libraries,
                                cwd=directory, capture_output=True, text=True)
        if result.returncode:
            # Not the notes and the code around the error, which the source shows
            errors = ''.join(line.replace(path, 'code' + suffix) + '\n'
                             for line in result.stderr.splitlines() if 'error' in line)
            numbered_source = ''.join('%4d | %s\n' % (number, line)
                                      for number, line in enumerate(source.splitlines(), 1))
            return "This doesn't compile. %s says\n\n%s\nabout\n\n%s" % (
                ' '.join(command), textwrap.indent(errors, '    '),
                textwrap.indent(numbered_source, '    '))
        return find_value_problem(printer_name, expr, symbols, parameters, executable)


class RunningProgram:
    """A running program from wrap_in_program(), which is restarted if it exits."""

    def __init__(self, executable):
        self.executable = executable
        self.process = None

    def value(self, arguments):
        """Return the line the program prints for the arguments, or raise
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


def find_value_problem(printer_name: str, expr: Basic, symbols: list[Basic],
                       parameters: list[Declaration], executable: str) -> str | None:
    """Run the compiled program for values of symbols, and return what is wrong
    with the values it prints, or None.

    The values are generated with Hypothesis or, inside a Hypothesis test,
    are FIXED_VALUES (see fixed_values()).
    """
    from hypothesis import (HealthCheck, assume, currently_in_test_context, given,
                            settings, strategies as st)
    from hypothesis.errors import Unsatisfiable

    names = [name for name, _ in parameters]
    symbol_types = [type_name for _, type_name in parameters]
    running = RunningProgram(executable)

    def compare(values):
        """Return False if SymPy's value isn't real, else raise
        PrintedCodeError if the printed value is different."""
        expected = sympy_value(expr, symbols, symbol_types, values)
        if expected is None:
            return False
        arguments = [str(value).lower() if printer_name == 'RustCodePrinter'
                     else str(int(value)) if isinstance(value, bool) else repr(value)
                     for value in values]
        given_values = ' for ' + ', '.join('%s = %r' % (name, value)
                                           for name, value in zip(names, values))
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
            if not sum(compare(values) for values in fixed_values(symbols, symbol_types)):
                return no_values
        else:
            @settings(max_examples=EXAMPLES, deadline=None, database=None,
                      derandomize=True, report_multiple_bugs=False,
                      suppress_health_check=list(HealthCheck))
            @given(st.tuples(*[values_strategy(symbol, type_name, st)
                                for symbol, type_name in zip(symbols, symbol_types)]))
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


def fixed_values(symbols: list[Basic], symbol_types: list[str]) -> list[tuple]:
    """Return up to EXAMPLES combinations of FIXED_VALUES for the symbols that
    agree with their assumptions.

    >>> from sympy import Symbol
    >>> from sympy.testing.check_printed_code import fixed_values
    >>> fixed_values([Symbol('n', integer=True, positive=True)], ['int'])
    [(1,), (2,), (7,)]
    """
    choices = [[value for value in FIXED_VALUES[type_name]
                if agrees_with_assumptions(symbol, type_name, value)]
               for symbol, type_name in zip(symbols, symbol_types)]
    combinations = list(itertools.product(*choices))
    return combinations[::max(1, len(combinations) // EXAMPLES)][:EXAMPLES]


def agrees_with_assumptions(symbol: Basic, type_name: str, value) -> bool:
    """Return whether the value agrees with the symbol's assumptions."""
    return type_name == 'bool' or all(getattr(as_sympy_number(type_name, value), 'is_' + assumption)
                                  for assumption, holds in symbol.assumptions0.items() if holds)


def values_strategy(symbol: Basic, type_name: str, st):
    """Return a strategy for values of the symbol that agree with its assumptions:
    0 or floats with an absolute value in [SMALLEST, BOUND] for reals, and
    integers in [-BOUND, BOUND]."""
    if type_name == 'bool':
        return st.booleans()
    if type_name == 'int':
        values = st.integers(-BOUND, BOUND)
    else:
        # Not tiny, so that products like x*x do not underflow
        values = st.one_of(st.just(0.0), st.floats(-BOUND, -SMALLEST),
                           st.floats(SMALLEST, BOUND))
    return values.filter(lambda value: agrees_with_assumptions(symbol, type_name, value))


def as_sympy_number(type_name: str, value) -> Basic:
    if type_name == 'bool':
        return true if value else false
    # Float(value, 30) is exactly the value of the float
    return Integer(value) if type_name == 'int' else Float(value, 30)


def sympy_value(expr: Basic, symbols: list[Basic], symbol_types: list[str],
                values) -> float | None:
    """Return SymPy's value of expr for the values of symbols as a float (1.0
    or 0.0 for a boolean, and possibly infinite or nan), or None if it isn't
    real.

    >>> from sympy import Symbol, sqrt
    >>> from sympy.testing.check_printed_code import sympy_value
    >>> x = Symbol('x', real=True)
    >>> sympy_value(sqrt(x), [x], ['real'], [4.0]), sympy_value(sqrt(x), [x], ['real'], [-1.0])
    (2.0, None)
    """
    try:
        value = expr.xreplace({symbol: as_sympy_number(type_name, value)
                              for symbol, type_name, value in zip(symbols, symbol_types, values)})
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
