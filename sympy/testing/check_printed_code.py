"""Check that the C, C++ and Rust code printed by a test compiles.

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

In a Hypothesis test, put the decorator below @given and use
@settings(deadline=None).
"""
from __future__ import annotations

import functools
import os
import shutil
import subprocess
import tempfile
import textwrap
from typing import NamedTuple

from sympy.codegen.ast import CodegenAST
from sympy.core.basic import Basic
from sympy.core.symbol import Symbol
from sympy.core.traversal import preorder_traversal
from sympy.functions.elementary.piecewise import ExprCondPair
from sympy.logic.boolalg import (And, Boolean, Equivalent, ITE, Implies, Nand,
                                 Nor, Not, Or, Xnor, Xor)
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

GCC = ['-fsyntax-only', '-pedantic-errors']
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
    'RustCodePrinter': Target(['rustc', '--edition=2021', '--crate-type=lib',
                               '--emit=metadata', '--error-format=short'],
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
    unsupported (see unsupported_reason()). With it, this also compiles the
    code (see find_compile_problem()).

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
    booleans = set()
    for node in preorder_traversal(expr):
        if isinstance(node, LOGIC_FUNCTIONS):
            booleans.update(node.args)
        elif isinstance(node, ExprCondPair):
            booleans.add(node.cond)
    parameters = [(printer._print(symbol), symbol_type(symbol, symbol in booleans))
                  for symbol in sorted(expr.free_symbols, key=str)]
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
        return find_compile_problem(type(printer).__name__, code, parameters, assigned)
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


def wrap_in_function(printer_name: str, code: str, parameters: list[Declaration],
                     assigned: Declaration | None) -> str:
    """Return the source of a function that declares the parameters and the
    assigned variable and runs the code, so that it compiles if the code is
    valid.

    >>> from sympy.testing.check_printed_code import wrap_in_function
    >>> print(wrap_in_function('C99CodePrinter', 'y = fmod(x, 2);',
    ...                        [('x', 'real')], ('y', 'real')))
    #define _XOPEN_SOURCE 700
    #include <math.h>
    #include <stdlib.h>
    #include <stdbool.h>
    <BLANKLINE>
    void f(double x)
    {
        double y;
        y = fmod(x, 2);
    }
    <BLANKLINE>
    """
    _, header, type_names = TARGETS[printer_name]
    rust = printer_name == 'RustCodePrinter'
    parameters = [(name, type_names[type_name]) for name, type_name in parameters]
    lines = code.splitlines()
    if assigned is None:
        if rust:
            # A block, since an expression can follow declarations of
            # number constants such as GoldenRatio
            body = ['let _ = {', *['    ' + line for line in lines], '};']
        else:
            declarations_end = 0
            while declarations_end < len(lines) and (
                    lines[declarations_end].endswith(';')
                    or lines[declarations_end].startswith(('//', '/*'))):
                declarations_end += 1
            body = lines[:declarations_end] + [
                '(void)(', *['    ' + line for line in lines[declarations_end:]], ');']
    elif assigned[0] in dict(parameters):
        body = lines
    elif rust:
        body = ['let mut %s: %s;' % (assigned[0], type_names[assigned[1]]), *lines]
    else:
        body = ['%s %s;' % (type_names[assigned[1]], assigned[0]), *lines]
    if rust:
        signature = 'pub fn f(%s)' % ', '.join(
            '%s%s: %s' % ('mut ' if assigned and name == assigned[0] else '', name, type_name)
            for name, type_name in parameters)
    else:
        signature = 'void f(%s)' % (', '.join(
            '%s %s' % (type_name, name) for name, type_name in parameters) or 'void')
    return '%s\n%s\n{\n%s\n}\n' % (header, signature, textwrap.indent('\n'.join(body), '    '))


def find_compile_problem(printer_name: str, code: str, parameters: list[Declaration],
                         assigned: Declaration | None) -> str | None:
    """Compile the code as wrap_in_function() wraps it, and return what the
    compiler says is wrong with it, or None if it compiles."""
    command = TARGETS[printer_name].command
    if shutil.which(command[0]) is None:
        raise PrintedCodeError('%s is needed to check printed code, since '
                               'SYMPY_CHECK_PRINTED_CODE is set' % command[0])
    source = wrap_in_function(printer_name, code, parameters, assigned)
    suffix = {'gcc': '.c', 'g++': '.cpp', 'rustc': '.rs'}[command[0]]
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, 'code' + suffix)
        with open(path, 'w') as file:
            file.write(source)
        result = subprocess.run(command + [path], cwd=directory, capture_output=True,
                                text=True)
    if not result.returncode:
        return None
    # Not the notes and the code around the error, which the source shows
    errors = ''.join(line.replace(path, 'code' + suffix) + '\n'
                     for line in result.stderr.splitlines() if 'error' in line)
    numbered_source = ''.join('%4d | %s\n' % (number, line)
                              for number, line in enumerate(source.splitlines(), 1))
    return "This doesn't compile. %s says\n\n%s\nabout\n\n%s" % (
        ' '.join(command), textwrap.indent(errors, '    '),
        textwrap.indent(numbered_source, '    '))
