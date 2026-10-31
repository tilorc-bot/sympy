"""Check that the C, C++, Fortran and Rust code printed by a test compiles
and computes the same values as SymPy.

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
C, C++, Fortran or Rust code, or code that can't be checked yet (arrays,
matrices, most non-default printer settings).

With SYMPY_CHECK_PRINTED_CODE set, the code is also run: it is wrapped in a
program that reads values of its symbols from standard input and prints its
value. The test fails if that value differs from SymPy's evalf(30) value by
more than TOLERANCE. Hypothesis generates the values (see values_strategy())
and reports the simplest ones that give a different value. Values for which
SymPy's value isn't real are skipped, and where it is nan (e.g. atan2(0, 0))
any printed value is accepted.

Fortran code is compiled with gfortran for the standard and source format
it is printed for. Fortran 77 and 90 code is checked as Fortran 95, and
Fortran 66 code can't be checked.

In a Hypothesis test, put the decorator below @given and use
@settings(deadline=None). The symbols then take the FIXED_VALUES, since
Hypothesis tests can't be nested.
"""
from __future__ import annotations

import functools
import itertools
import math
import os
import re
import shutil
import subprocess
import tempfile
import textwrap
from typing import NamedTuple

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
# fcode's output depends on these settings, so each combination is a target,
# e.g. "FCodePrinter(standard=95, source_format='free')" (see target_name())
TARGET_SETTINGS = {'FCodePrinter': ('standard', 'source_format')}
FORTRAN_STANDARDS = {77: 'f95', 90: 'f95', 95: 'f95', 2003: 'f2003', 2008: 'f2008'}
# double precision is the type of the 1.0d0 literals that fcode prints
FORTRAN_TYPE_NAMES = {'int': 'integer', 'real': 'double precision', 'bool': 'logical'}
for standard, gfortran_standard in FORTRAN_STANDARDS.items():
    for source_format in ('fixed', 'free'):
        name = 'FCodePrinter(standard=%r, source_format=%r)' % (standard, source_format)
        TARGETS[name] = Target(
            # Otherwise gfortran ignores what comes after column 72 in fixed form
            ['gfortran', '-std=' + gfortran_standard, '-f%s-form' % source_format, *GCC,
             '-Werror=line-truncation'], '', FORTRAN_TYPE_NAMES)
PRINTER_CLASS_NAMES = {name.partition('(')[0] for name in TARGETS}
PRINTER_MODULES = ('sympy.printing.c', 'sympy.printing.cxx', 'sympy.printing.fortran',
                   'sympy.printing.rust')

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
    """Return whether SYMPY_CHECK_PRINTED_CODE is set (and not to 0)."""
    return os.environ.get('SYMPY_CHECK_PRINTED_CODE', '') not in ('', '0')


class PrintedCodeError(AssertionError):
    """Code printed by a test decorated with ``check_printed_code`` is wrong."""


def check_printed_code(test_func):
    """Make the test fail if C, C++, Fortran or Rust code that it prints is
    wrong.

    The test checks that a printer prints the code it expects. This checks
    that the code is actually correct: that it compiles and computes the same
    values as SymPy.
    For example, this test fails, since x has no type, so its code can't be
    compiled:

    >>> from sympy import Symbol, sin
    >>> from sympy.printing.c import ccode
    >>> from sympy.testing.check_printed_code import check_printed_code
    >>> @check_printed_code
    ... def test_sin():
    ...     assert ccode(sin(Symbol('x'))) == 'sin(x)'
    >>> test_sin()
    Traceback (most recent call last):
    ...
    sympy.testing.check_printed_code.PrintedCodeError: C99CodePrinter printed
    <BLANKLINE>
        sin(x)
    <BLANKLINE>
    The type of x is unknown, so this can't be compiled. Create x with
    real=True or integer=True, e.g. Symbol('x', real=True).

    With Symbol('x', real=True), it passes. If SYMPY_CHECK_PRINTED_CODE is
    set, it then also compiles and runs sin(x), and fails if gcc can't compile
    it or it doesn't compute SymPy's values of sin(x).

    While the test runs, CodePrinter.doprint is replaced by a wrapper that
    checks what these printers print (see check_code()). The problems are
    raised when the test returns.
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
            if (printer_name in PRINTER_CLASS_NAMES
                    and type(self).__module__ in PRINTER_MODULES
                    and isinstance(code, str)
                    and (printer_name, code, expr, assign_to) not in printed):
                printed.add((printer_name, code, expr, assign_to))
                try:
                    check_code(self, expr, assign_to, code)
                except PrintedCodeError as problem:
                    problems.append('%s printed\n\n%s\n\n%s' % (
                        target_name(self), textwrap.indent(code, '    '), problem))
            return code

        CodePrinter.doprint = doprint  # type: ignore[method-assign]
        try:
            result = test_func(*args, **kwargs)
        finally:
            CodePrinter.doprint = original_doprint  # type: ignore[method-assign]
        if not printed:
            raise PrintedCodeError('The test printed no C, C++, Fortran or Rust code, '
                                   "so it shouldn't use @check_printed_code.")
        if problems:
            raise PrintedCodeError('\n\n'.join(problems))
        return result
    return wrapper


def check_code(printer: CodePrinter, expr: Basic, assign_to: str | Basic | None,
               code: str) -> None:
    """Raise PrintedCodeError if code, which printer printed for expr (assigned
    to assign_to, if it isn't None), is wrong.

    If SYMPY_CHECK_PRINTED_CODE is set, this compiles and runs the code, and
    compares its values with SymPy's (see check_runs()). Before that, and otherwise only, it checks that the code
    can be compiled: that nothing in it is unsupported, such as an array, and
    that each of its symbols has a type (see declare()).

    >>> from sympy import MatrixSymbol
    >>> from sympy.printing.c import C99CodePrinter
    >>> from sympy.testing.check_printed_code import check_code
    >>> check_code(C99CodePrinter(), MatrixSymbol('A', 2, 2)[0, 1], None, 'A[1]')
    Traceback (most recent call last):
    ...
    sympy.testing.check_printed_code.PrintedCodeError: This can't be checked, since it uses arrays or matrices, whose sizes
    can't be declared, so the test can't use @check_printed_code.
    """
    def unsupported(reason):
        return PrintedCodeError(textwrap.fill(
            "This can't be checked, since %s, so the test can't use "
            "@check_printed_code." % reason, 72))

    if target_name(printer) not in TARGETS:
        raise unsupported('there is no compiler for %s' % target_name(printer))
    allowed = HARMLESS_SETTINGS.union(TARGET_SETTINGS.get(type(printer).__name__, ()))
    for name, value in printer._settings.items():
        if name not in allowed and value != printer._default_settings.get(name):
            raise unsupported("it's printed with the setting %s, which can need other "
                              "declarations" % name)
    if isinstance(printer, C89CodePrinter):
        for name in C_TYPE_SETTINGS:
            if getattr(printer, name) != getattr(type(printer), name):
                raise unsupported("it's printed with the setting %s, which can need "
                                  "other declarations" % name)
    if isinstance(expr, CodegenAST) or not isinstance(expr, Basic):
        raise unsupported("it's a %s, not an expression" % type(expr).__name__)
    if (expr.is_Matrix or expr.atoms(Indexed, Idx, MatrixSymbol, MatrixElement)
            or not isinstance(assign_to, (str, Symbol, type(None)))):
        raise unsupported("it uses arrays or matrices, whose sizes can't be declared")

    booleans: set[Basic] = set()
    for node in preorder_traversal(expr):
        if isinstance(node, LOGIC_FUNCTIONS):
            booleans.update(node.args)
        elif isinstance(node, ExprCondPair):
            booleans.add(node.cond)
    symbols = sorted(expr.free_symbols, key=str)
    parameters = [declare(printer, symbol, symbol in booleans) for symbol in symbols]
    assigned = None
    if assign_to is not None:
        symbol = Symbol(assign_to) if isinstance(assign_to, str) else assign_to
        name = printer._print(symbol)
        if name in dict(parameters):
            assigned = (name, dict(parameters)[name])
        else:
            is_boolean = isinstance(expr, Boolean) and not isinstance(expr, Symbol)
            assigned = declare(printer, symbol, is_boolean)
    for name, _ in parameters + ([assigned] if assigned else []):
        if not name.isidentifier():
            raise unsupported("%s isn't a name" % name)
    if compiling_enabled():
        check_runs(target_name(printer), code, parameters, assigned, expr, symbols)


def target_name(printer: CodePrinter) -> str:
    """Return the printer's class name, with the values of its TARGET_SETTINGS
    if it has any, e.g. "FCodePrinter(standard=95, source_format='free')"."""
    name = type(printer).__name__
    if name in TARGET_SETTINGS:
        name += '(%s)' % ', '.join('%s=%r' % (setting, printer._settings[setting])
                                   for setting in TARGET_SETTINGS[name])
    return name


def declare(printer: CodePrinter, symbol: Basic, is_boolean: bool) -> Declaration:
    """Return the name that printer prints for symbol and its type, 'bool',
    'int' or 'real', or raise PrintedCodeError if its type is unknown.

    >>> from sympy import Symbol
    >>> from sympy.printing.c import C99CodePrinter
    >>> from sympy.testing.check_printed_code import declare
    >>> declare(C99CodePrinter(), Symbol('x', real=True), False)
    ('x', 'real')
    """
    name = printer._print(symbol)
    if is_boolean:
        return (name, 'bool')
    if symbol.is_integer:
        return (name, 'int')
    if symbol.is_real:
        return (name, 'real')
    raise PrintedCodeError(textwrap.fill(
        "The type of %s is unknown, so this can't be compiled. Create %s with "
        "real=True or integer=True, e.g. Symbol(%r, real=True)." % (name, name, name), 72))


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
    if printer_name.startswith('FCodePrinter('):
        return wrap_in_fortran_program(printer_name, code, parameters, assigned)
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
    body += ['%s %s = %s;' % (type_names[type_name], name, read[type_name])
             for name, type_name in parameters]
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


# fcode prints each number constant as a parameter, e.g. parameter (pi = ...)
PARAMETER = re.compile(r'\s*parameter \((\w+) = ')


def wrap_in_fortran_program(printer_name: str, code: str, parameters: list[Declaration],
                            assigned: Declaration | None) -> str:
    """Return wrap_in_program() for code printed by FCodePrinter."""
    command, _, type_names = TARGETS[printer_name]
    fixed_form = '-ffixed-form' in command
    # Fixed form: statements start in column 7, continuations have @ in column 6
    lead = '      ' if fixed_form else ''
    lines = code.splitlines()

    def continued(*parts):
        if fixed_form:
            return [lead + parts[0], *('     @' + part for part in parts[1:])]
        return [part + ' &' for part in parts[:-1]] + [parts[-1]]

    # The parameters and comments the code starts with must come before the loop
    specifications_end = 0
    while specifications_end < len(lines) and (
            PARAMETER.match(lines[specifications_end])
            or lines[specifications_end].lstrip()[:1] == '!'
            or fixed_form and lines[specifications_end][:1] == 'C'):
        specifications_end += 1
    declarations = dict(parameters + ([assigned] if assigned else []))
    specifications = ['%s %s' % (type_names[type_name], name)
                      for name, type_name in declarations.items()]
    # Without a declaration, a parameter has the default real type
    specifications += ['double precision ' + match.group(1)
                       for match in map(PARAMETER.match, lines[:specifications_end]) if match]
    # Fixed form lines end at column 72
    read = textwrap.wrap('read (*, *, iostat=sympy_status) ' + ', '.join(dict(parameters)),
                         60, subsequent_indent='      ')
    if assigned is not None:
        body = lines[specifications_end:] + [lead + 'print *, ' + assigned[0]]
    else:
        # The printed expression continues the print statement
        body = (continued('print *,', lines[specifications_end][len(lead):])
                + lines[specifications_end + 1:])
    return '\n'.join([
        *[lead + line for line in ['program sympy_check', 'implicit none',
                                   'integer sympy_status', *specifications]],
        *lines[:specifications_end], lead + 'do', *continued(*read),
        lead + 'if (sympy_status /= 0) exit', *body, lead + 'end do', lead + 'end program', ''])


def check_runs(printer_name: str, code: str, parameters: list[Declaration],
               assigned: Declaration | None, expr: Basic, symbols: list[Basic]) -> None:
    """Compile the code as wrap_in_program() wraps it and run it, and raise
    PrintedCodeError if it doesn't compile or doesn't print SymPy's value of
    expr for the values of symbols (whose names and types are parameters) that
    check_values() tries."""
    command = TARGETS[printer_name].command
    if shutil.which(command[0]) is None:
        raise RuntimeError('%s is needed to check printed code, since '
                           'SYMPY_CHECK_PRINTED_CODE is set' % command[0])
    source = wrap_in_program(printer_name, code, parameters, assigned)
    suffix = {'gcc': '.c', 'g++': '.cpp', 'gfortran': '.f90', 'rustc': '.rs'}[command[0]]
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, 'code' + suffix)
        executable = os.path.join(directory, 'code')
        with open(path, 'w') as file:
            file.write(source)
        libraries = [] if command[0] == 'rustc' else ['-lm']
        result = subprocess.run(command + [path, '-o', executable] + libraries,
                                cwd=directory, capture_output=True, text=True)
        if result.returncode:
            # Not the notes and the code around the error, which the source shows,
            # but gfortran's locations, which are on their own line
            errors = ''.join(line.replace(path, 'code' + suffix) + '\n'
                             for line in result.stderr.splitlines()
                             if 'error' in line.lower() or re.search(r':\d+:\d+:$', line))
            numbered_source = ''.join('%4d | %s\n' % (number, line)
                                      for number, line in enumerate(source.splitlines(), 1))
            raise PrintedCodeError("This doesn't compile. %s says\n\n%s\nabout\n\n%s" % (
                ' '.join(command), textwrap.indent(errors, '    '),
                textwrap.indent(numbered_source, '    ')))
        check_values(printer_name, expr, symbols, parameters, executable)


class RunningProgram:
    """A running program from wrap_in_program(), which is restarted if it exits."""

    def __init__(self, executable):
        self.executable = executable
        self.process = None

    def value(self, arguments):
        """Return the line the program prints for the arguments, or raise
        PrintedCodeError if it exits."""
        if self.process is None:
            # A gfortran program could otherwise buffer its output to the pipe
            self.process = subprocess.Popen(
                [self.executable], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True,
                env=dict(os.environ, GFORTRAN_UNBUFFERED_PRECONNECTED='y'))
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


def check_values(printer_name: str, expr: Basic, symbols: list[Basic],
                 parameters: list[Declaration], executable: str) -> None:
    """Run the compiled program for values of symbols, and raise
    PrintedCodeError if a value it prints isn't SymPy's value of expr.

    The values are generated with Hypothesis or, inside a Hypothesis test,
    are FIXED_VALUES (see fixed_values()).
    """
    from hypothesis import (HealthCheck, assume, currently_in_test_context, given,
                            settings, strategies as st)
    from hypothesis.errors import Unsatisfiable

    names = [name for name, _ in parameters]
    symbol_types = [type_name for _, type_name in parameters]
    # Rust and Fortran read booleans as true and false, C as 1 and 0
    booleans_as_words = TARGETS[printer_name].command[0] in ('rustc', 'gfortran')
    running = RunningProgram(executable)

    def compare(values):
        """Return False if SymPy's value isn't real, else raise
        PrintedCodeError if the printed value is different."""
        expected = sympy_value(expr, symbols, symbol_types, values)
        if expected is None:
            return False
        arguments = [str(value).lower() if booleans_as_words
                     else str(int(value)) if isinstance(value, bool) else repr(value)
                     for value in values]
        given_values = ' for ' + ', '.join('%s = %r' % (name, value)
                                           for name, value in zip(names, values))
        try:
            output = running.value(arguments)
        except PrintedCodeError as e:
            raise PrintedCodeError('This %s%s.' % (e, given_values if names else ''))
        # Fortran prints a logical as T or F
        value = {'true': 1.0, 'false': 0.0, 'T': 1.0, 'F': 0.0}.get(output)
        if value is None:
            try:
                value = float(output)
            except ValueError:  # e.g. a complex number
                raise PrintedCodeError("This gives %s%s, which isn't a real number." % (
                    output, given_values if names else ''))
        # nan means undefined, e.g. atan2(0, 0)
        if not (value == expected or math.isnan(expected)
                or abs(value - expected) <= TOLERANCE * max(1.0, abs(expected))):
            raise PrintedCodeError("This gives %s%s, but SymPy's value of %s is %r." % (
                output, given_values if names else '', expr, expected))
        return True

    no_values = PrintedCodeError("SymPy's value of %s isn't a real number for any "
                                 "of the values tried, so this can't be checked." % expr)
    try:
        if not names:
            if not compare([]):
                raise PrintedCodeError("SymPy's value of %s isn't a real number, so this "
                                       "can't be checked." % expr)
        elif currently_in_test_context():
            # Hypothesis tests can't be nested
            compared = [compare(values) for values in fixed_values(symbols, symbol_types)]
            if not any(compared):
                raise no_values
        else:
            @settings(max_examples=EXAMPLES, deadline=None, database=None,
                      derandomize=True, report_multiple_bugs=False,
                      suppress_health_check=list(HealthCheck))
            @given(st.tuples(*[values_strategy(symbol, type_name, st)
                                for symbol, type_name in zip(symbols, symbol_types)]))
            def generated(values):
                assume(compare(values))
            generated()
    except Unsatisfiable:
        raise no_values
    finally:
        running.close()


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
