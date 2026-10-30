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
@settings(deadline=None). expressions() generates expressions to print.
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
from sympy.core.add import Add
from sympy.core.basic import Basic
from sympy.core.mod import Mod
from sympy.core.mul import Mul
from sympy.core.numbers import Float, I, Rational, nan, oo, zoo
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
from sympy.logic.boolalg import (And, Boolean, Equivalent, ITE, Implies, Nand,
                                 Nor, Not, Or, Xnor, Xor)
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

GCC = ['-fsyntax-only', '-pedantic-errors']
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
LOGIC = (And, Or, Not, Xor, Xnor, Nand, Nor, Implies, Equivalent, ITE)


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
    SYMPY_CHECK_PRINTED_CODE is set and the code doesn't compile as
    source() wraps it.
    """
    reason = unsupported(printer, expr, assign_to)
    if reason:
        return ("This can't be checked, since %s, so the test can't use "
                "@check_printed_code." % reason)
    booleans = set()
    for node in preorder_traversal(expr):
        if isinstance(node, LOGIC):
            booleans.update(node.args)
        elif isinstance(node, ExprCondPair):
            booleans.add(node.cond)
    params = [(printer._print(s), symbol_type(s, s in booleans))
              for s in sorted(expr.free_symbols, key=str)]
    target = None
    if assign_to is not None:
        symbol = Symbol(assign_to) if isinstance(assign_to, str) else assign_to
        name = printer._print(symbol)
        is_boolean = isinstance(expr, Boolean) and not isinstance(expr, Symbol)
        target = (name, dict(params).get(name, symbol_type(symbol, is_boolean)))
    names = params + ([target] if target else [])

    not_names = [name for name, _ in names if not name.isidentifier()]
    if not_names:
        return ("This can't be checked, since %s isn't a name, so the test can't "
                "use @check_printed_code." % ' or '.join(not_names))
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
        return compile_code(type(printer).__name__, code, params, target)
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


def source(printer_name, code, params, target):
    """The code wrapped into a function, with params and target declared.

    >>> from sympy.testing.check_printed_code import source
    >>> print(source('C99CodePrinter', 'y = fmod(x, 2);', [('x', 'real')], ('y', 'real')))
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
    _, header, types = TARGETS[printer_name]
    rust = printer_name == 'RustCodePrinter'
    params = [(name, types[type_]) for name, type_ in params]
    lines = code.splitlines()
    if target is None:
        if rust:
            # A block, since an expression can follow declarations of
            # number constants such as GoldenRatio
            body = ['let _ = {', *['    ' + line for line in lines], '};']
        else:
            n = 0
            while n < len(lines) and (lines[n].endswith(';')
                                      or lines[n].startswith(('//', '/*'))):
                n += 1
            body = lines[:n] + ['(void)(', *['    ' + line for line in lines[n:]], ');']
    elif target[0] in dict(params):
        body = lines
    elif rust:
        body = ['let mut %s: %s;' % (target[0], types[target[1]]), *lines]
    else:
        body = ['%s %s;' % (types[target[1]], target[0]), *lines]
    if rust:
        signature = 'pub fn f(%s)' % ', '.join(
            '%s%s: %s' % ('mut ' if target and name == target[0] else '', name, type_)
            for name, type_ in params)
    else:
        signature = 'void f(%s)' % (', '.join(
            '%s %s' % (type_, name) for name, type_ in params) or 'void')
    return '%s\n%s\n{\n%s\n}\n' % (header, signature, textwrap.indent('\n'.join(body), '    '))


def compile_code(printer_name, code, params, target):
    """What the compiler says about the code wrapped by source(), or None if
    it compiles."""
    command = TARGETS[printer_name].command
    if shutil.which(command[0]) is None:
        raise PrintedCodeError('%s is needed to check printed code, since '
                               'SYMPY_CHECK_PRINTED_CODE is set' % command[0])
    wrapped = source(printer_name, code, params, target)
    suffix = {'gcc': '.c', 'g++': '.cpp', 'rustc': '.rs'}[command[0]]
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'code' + suffix)
        with open(path, 'w') as f:
            f.write(wrapped)
        result = subprocess.run(command + [path], cwd=tmp, capture_output=True,
                                text=True)
    if not result.returncode:
        return None
    # Not the notes and the code around the error, which the source shows
    errors = ''.join(line.replace(path, 'code' + suffix) + '\n'
                     for line in result.stderr.splitlines() if 'error' in line)
    numbered = ''.join('%4d | %s\n' % (n, line)
                       for n, line in enumerate(wrapped.splitlines(), 1))
    return "This doesn't compile. %s says\n\n%s\nabout\n\n%s" % (
        ' '.join(command), textwrap.indent(errors, '    '), textwrap.indent(numbered, '    '))


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
