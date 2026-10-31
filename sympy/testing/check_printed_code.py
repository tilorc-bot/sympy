"""Check that the C, C++ and Rust code printed by a test compiles.

Code printer tests only compare strings. A test opts in to checking the
code with a decorator::

    from sympy.testing.check_printed_code import check_printed_code

    @check_printed_code
    def test_sign():
        x, y = symbols('x y', real=True)
        assert rust_code(sign(x + y)) == "..."

The code is compiled with gcc, g++ or rustc if it is found.
SYMPY_CHECK_PRINTED_CODE=0 turns compiling off, and
SYMPY_CHECK_PRINTED_CODE=1 makes a compiler that isn't found an error::

    SYMPY_CHECK_PRINTED_CODE=1 pytest sympy/printing/tests/test_rust.py

In every run, a decorated test fails if a symbol in its printed code has no
type: integer=True gives an int, real=True a double, and a symbol used in
And, Or, Not or a Piecewise condition a bool. It also fails if it prints no
C, C++ or Rust code, or code that can't be checked yet (arrays, matrices,
most non-default printer settings).
"""
from __future__ import annotations

import functools
import os
import shutil
import subprocess
import tempfile
import textwrap
from typing import TYPE_CHECKING, NamedTuple

from sympy.codegen.ast import CodegenAST
from sympy.core.basic import Basic
from sympy.core.symbol import Symbol
from sympy.core.traversal import preorder_traversal
from sympy.functions.elementary.piecewise import ExprCondPair
from sympy.logic.boolalg import (And, Boolean, Equivalent, ITE, Implies, Nand,
                                 Nor, Not, Or, Xnor, Xor)
from sympy.matrices.expressions.matexpr import MatrixElement, MatrixSymbol
from sympy.printing.c import C11CodePrinter, C89CodePrinter, C99CodePrinter
from sympy.printing.codeprinter import CodePrinter
from sympy.printing.cxx import CXX11CodePrinter, CXX17CodePrinter, CXX98CodePrinter
from sympy.printing.rust import RustCodePrinter
from sympy.tensor.indexed import Idx, Indexed

if TYPE_CHECKING:
    from collections.abc import Callable

# The printed name of a variable and its type, 'int', 'real' or 'bool',
# e.g. ('x', 'real')
Declaration = tuple[str, str]


class Target(NamedTuple):
    command: list[str]
    suffix: str
    header: str
    type_names: dict[str, str]
    # wrap_in_c_function() or wrap_in_rust_function()
    wrap: Callable[[str, list[tuple[str, str]], tuple[str, str] | None], str]


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

# Settings that change how the code is written, but not what it needs declared
HARMLESS_SETTINGS = {'order', 'full_prec', 'human', 'precision', 'contract',
                     'strict', 'error_on_reserved', 'reserved_word_suffix', 'inline'}
# type_aliases and the other type settings of the C printers, which they
# keep as attributes instead of in _settings
C_TYPE_SETTINGS = [name for name in vars(C89CodePrinter) if name.startswith('type_')]
# Their arguments are booleans (unlike those of isnan and other BooleanFunctions)
LOGIC_FUNCTIONS = (And, Or, Not, Xor, Xnor, Nand, Nor, Implies, Equivalent, ITE)

def compiling_enabled(printer_class: type[CodePrinter]) -> bool:
    """Return whether the code that printer_class prints is compiled: if its
    compiler is found, unless SYMPY_CHECK_PRINTED_CODE is 0. Raise
    RuntimeError if it isn't found and SYMPY_CHECK_PRINTED_CODE is set to
    something else."""
    setting = os.environ.get('SYMPY_CHECK_PRINTED_CODE', '')
    if setting == '0':
        return False
    compiler = TARGETS[printer_class].command[0]
    if shutil.which(compiler) is not None:
        return True
    if setting:
        raise RuntimeError('%s is needed to check printed code, since '
                           'SYMPY_CHECK_PRINTED_CODE is set' % compiler)
    return False


class PrintedCodeError(AssertionError):
    """Code printed by a test decorated with ``check_printed_code`` is wrong."""


def check_printed_code(test_func):
    """Make the test fail if C, C++ or Rust code that it prints is wrong.

    Explanation
    ===========

    The test checks that a printer prints the code it expects. This checks
    that the code is actually correct, which for now means that it compiles.

    While the test runs, CodePrinter.doprint is replaced by a wrapper that
    checks what these printers print (see check_code()). The problems are
    raised when the test returns.

    Examples
    ========

    This test fails, since x has no type, so its code can't be compiled:

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

    With Symbol('x', real=True), it passes. If gcc is found, it then also
    compiles sin(x), and fails if gcc can't compile it.
    """
    @functools.wraps(test_func)
    def wrapper(*args, **kwargs):
        printed, problems = set(), []
        original_doprint = CodePrinter.doprint

        # The printers inherit doprint and none calls it recursively, so this
        # sees everything the test prints once
        def doprint(self, expr, assign_to=None):
            code = original_doprint(self, expr, assign_to)
            # Only the classes in TARGETS, not subclasses defined by tests
            if (type(self) in TARGETS and isinstance(code, str)
                    and (type(self), code, expr, assign_to) not in printed):
                printed.add((type(self), code, expr, assign_to))
                try:
                    check_code(self, expr, assign_to, code)
                except PrintedCodeError as problem:
                    problems.append('%s printed\n\n%s\n\n%s' % (
                        type(self).__name__, textwrap.indent(code, '    '), problem))
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


def check_code(printer: CodePrinter, expr: Basic, assign_to: str | Basic | None,
               code: str) -> None:
    """Raise PrintedCodeError if code, which printer printed for expr (assigned
    to assign_to, if it isn't None), is wrong.

    If the compiler is found, this compiles the code (see compiling_enabled()
    and check_compiles()). Before that, and otherwise only, it checks that the
    code can be compiled: that nothing in it is unsupported, such as an array, and
    that each of its symbols has a type (see declarations()).

    Examples
    ========

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

    changed_settings = [
        name for name, value in printer._settings.items()
        if name not in HARMLESS_SETTINGS and value != printer._default_settings.get(name)]
    if isinstance(printer, C89CodePrinter):
        changed_settings += [name for name in C_TYPE_SETTINGS
                             if getattr(printer, name) != getattr(type(printer), name)]
    if changed_settings:
        raise unsupported("it's printed with the setting %s, which can need other "
                          "declarations" % changed_settings[0])
    if isinstance(expr, CodegenAST) or not isinstance(expr, Basic):
        raise unsupported("it's a %s, not an expression" % type(expr).__name__)
    if (expr.is_Matrix or expr.atoms(Indexed, Idx, MatrixSymbol, MatrixElement)
            or not isinstance(assign_to, (str, Symbol, type(None)))):
        raise unsupported("it uses arrays or matrices, whose sizes can't be declared")

    parameters, assigned = declarations(printer, expr, assign_to)
    for name, _ in [*parameters.values(), *([assigned] if assigned else [])]:
        if not name.isidentifier():
            raise unsupported("%s isn't a name" % name)
    if compiling_enabled(type(printer)):
        check_compiles(type(printer), wrap_in_function(
            type(printer), code, list(parameters.values()), assigned))


def declarations(printer: CodePrinter, expr: Basic, assign_to: str | Basic | None
                 ) -> tuple[dict[Basic, Declaration], Declaration | None]:
    """Return the declarations of the symbols in expr, by symbol and sorted by
    name, and of the variable assign_to, or None if it is None. Raise
    PrintedCodeError if the type of one is unknown (see declare()).

    Examples
    ========

    b is a bool since it's an argument of And, and c since it's assigned a
    boolean:

    >>> from sympy import And, Symbol
    >>> from sympy.printing.c import C99CodePrinter
    >>> from sympy.testing.check_printed_code import declarations
    >>> b, x = Symbol('b'), Symbol('x', real=True)
    >>> declarations(C99CodePrinter(), And(b, x > 0), 'c')
    ({b: ('b', 'bool'), x: ('x', 'real')}, ('c', 'bool'))
    """
    booleans: set[Basic] = set()
    for node in preorder_traversal(expr):
        if isinstance(node, LOGIC_FUNCTIONS):
            booleans.update(node.args)
        elif isinstance(node, ExprCondPair):
            booleans.add(node.cond)
    parameters = {symbol: declare(printer, symbol, symbol in booleans)
                  for symbol in sorted(expr.free_symbols, key=str)}
    if assign_to is None:
        return parameters, None
    symbol = Symbol(assign_to) if isinstance(assign_to, str) else assign_to
    name = printer._print(symbol)
    types = dict(parameters.values())
    if name in types:
        return parameters, (name, types[name])
    is_boolean = isinstance(expr, Boolean) and not isinstance(expr, Symbol)
    return parameters, declare(printer, symbol, is_boolean)


def declare(printer: CodePrinter, symbol: Basic, is_boolean: bool) -> Declaration:
    """Return the name that printer prints for symbol and its type, 'bool',
    'int' or 'real', or raise PrintedCodeError if its type is unknown.

    Examples
    ========

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


def wrap_in_function(printer_class: type[CodePrinter], code: str, parameters: list[Declaration],
                     assigned: Declaration | None) -> str:
    """Return the source of a function that declares the parameters and the
    assigned variable and runs the code, so that it compiles if the code is
    valid.

    Examples
    ========

    >>> from sympy.printing.c import C99CodePrinter
    >>> from sympy.testing.check_printed_code import wrap_in_function
    >>> print(wrap_in_function(C99CodePrinter, 'y = fmod(x, 2);',
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
    target = TARGETS[printer_class]
    parameters = [(name, target.type_names[type_name]) for name, type_name in parameters]
    if assigned is not None:
        assigned = (assigned[0], target.type_names[assigned[1]])
    return '%s\n%s' % (target.header, target.wrap(code, parameters, assigned))


def wrap_in_c_function(code: str, parameters: list[tuple[str, str]],
                       assigned: tuple[str, str] | None) -> str:
    """Return a C or C++ function that declares the parameters and the
    assigned variable, given with C type names, and runs the code.

    Examples
    ========

    An expression can follow declarations of number constants:

    >>> from sympy.testing.check_printed_code import wrap_in_c_function
    >>> print(wrap_in_c_function(
    ...     'const double GoldenRatio = 1.6180339887498948;\\nGoldenRatio*x',
    ...     [('x', 'double')], None))
    void f(double x)
    {
        const double GoldenRatio = 1.6180339887498948;
        (void)(
            GoldenRatio*x
        );
    }
    <BLANKLINE>
    """
    lines = code.splitlines()
    if assigned is None:
        declarations_end = 0
        while declarations_end < len(lines) and (
                lines[declarations_end].endswith(';')
                or lines[declarations_end].startswith(('//', '/*'))):
            declarations_end += 1
        body = lines[:declarations_end] + [
            '(void)(', *['    ' + line for line in lines[declarations_end:]], ');']
    elif assigned[0] in dict(parameters):
        body = lines
    else:
        body = ['%s %s;' % (assigned[1], assigned[0]), *lines]
    signature = 'void f(%s)' % (', '.join(
        '%s %s' % (type_name, name) for name, type_name in parameters) or 'void')
    return '%s\n{\n%s\n}\n' % (signature, textwrap.indent('\n'.join(body), '    '))


def wrap_in_rust_function(code: str, parameters: list[tuple[str, str]],
                          assigned: tuple[str, str] | None) -> str:
    """Return a Rust function that declares the parameters and the assigned
    variable, given with Rust type names, and runs the code.

    Examples
    ========

    A parameter that the code assigns to is declared mut:

    >>> from sympy.testing.check_printed_code import wrap_in_rust_function
    >>> print(wrap_in_rust_function('x = x + 1.0;', [('x', 'f64')], ('x', 'f64')))
    pub fn f(mut x: f64)
    {
        x = x + 1.0;
    }
    <BLANKLINE>
    """
    lines = code.splitlines()
    if assigned is None:
        # A block, since an expression can follow declarations of
        # number constants such as GoldenRatio
        body = ['let _ = {', *['    ' + line for line in lines], '};']
    elif assigned[0] in dict(parameters):
        body = lines
    else:
        body = ['let mut %s: %s;' % assigned, *lines]
    signature = 'pub fn f(%s)' % ', '.join(
        '%s%s: %s' % ('mut ' if assigned and name == assigned[0] else '', name, type_name)
        for name, type_name in parameters)
    return '%s\n{\n%s\n}\n' % (signature, textwrap.indent('\n'.join(body), '    '))


TARGETS = {
    C89CodePrinter: Target(['gcc', '-std=c89', *C_FLAGS], '.c', C_HEADER,
                           {'int': 'int', 'real': 'double', 'bool': 'int'},
                           wrap_in_c_function),
    C99CodePrinter: Target(['gcc', '-std=c99', *C_FLAGS], '.c', C99_HEADER, C_TYPE_NAMES,
                           wrap_in_c_function),
    C11CodePrinter: Target(['gcc', '-std=c11', *C_FLAGS], '.c', C99_HEADER, C_TYPE_NAMES,
                           wrap_in_c_function),
    CXX98CodePrinter: Target(['g++', '-std=c++98', *GCC], '.cpp', CXX_HEADER, C_TYPE_NAMES,
                             wrap_in_c_function),
    CXX11CodePrinter: Target(['g++', '-std=c++11', *GCC], '.cpp', CXX_HEADER, C_TYPE_NAMES,
                             wrap_in_c_function),
    CXX17CodePrinter: Target(['g++', '-std=c++17', *GCC], '.cpp', CXX_HEADER, C_TYPE_NAMES,
                             wrap_in_c_function),
    RustCodePrinter: Target(['rustc', '--edition=2021', '--crate-type=lib',
                             '--emit=metadata', '--error-format=short'], '.rs',
                            RUST_HEADER, {'int': 'i32', 'real': 'f64', 'bool': 'bool'},
                            wrap_in_rust_function),
}


def check_compiles(printer_class: type[CodePrinter], source: str) -> None:
    """Compile source, such as wrap_in_function() returns, with the compiler
    for printer_class, and raise PrintedCodeError with what the compiler says
    if it doesn't compile."""
    target = TARGETS[printer_class]
    command, suffix = target.command, target.suffix
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, 'code' + suffix)
        with open(path, 'w') as file:
            file.write(source)
        result = subprocess.run(command + [path], cwd=directory, capture_output=True,
                                text=True)
    if result.returncode:
        # Not the notes and the code around the error, which the source shows
        errors = ''.join(line.replace(path, 'code' + suffix) + '\n'
                         for line in result.stderr.splitlines() if 'error' in line)
        numbered_source = ''.join('%4d | %s\n' % (number, line)
                                  for number, line in enumerate(source.splitlines(), 1))
        raise PrintedCodeError("This doesn't compile. %s says\n\n%s\nabout\n\n%s" % (
            ' '.join(command), textwrap.indent(errors, '    '),
            textwrap.indent(numbered_source, '    ')))
