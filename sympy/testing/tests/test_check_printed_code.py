from __future__ import annotations

import os
from contextlib import contextmanager

from sympy.codegen.ast import float80, real
from sympy.core.relational import Gt
from sympy.core.symbol import Symbol, symbols
from sympy.functions.elementary.trigonometric import sin
from sympy.logic.boolalg import And, ITE
from sympy.matrices.expressions.matexpr import MatrixSymbol
from sympy.printing.c import C89CodePrinter, C99CodePrinter, ccode
from sympy.printing.codeprinter import CodePrinter, rust_code
from sympy.printing.octave import octave_code
from sympy.printing.rust import RustCodePrinter
from sympy.testing.check_printed_code import (PrintedCodeError, check_code, check_compiles,
                                              check_printed_code, compiling_enabled,
                                              declarations, declare, wrap_in_function)
from sympy.testing.pytest import raises, skip

x = Symbol('x', real=True)
n = Symbol('n', integer=True)
b, z = symbols('b z')


def test_declare():
    assert declare(C99CodePrinter(), x, False) == ('x', 'real')
    assert declare(C99CodePrinter(), n, False) == ('n', 'int')
    assert declare(C99CodePrinter(), b, True) == ('b', 'bool')
    e = raises(PrintedCodeError, lambda: declare(C99CodePrinter(), z, False))
    assert str(e.value).startswith('The type of z is unknown')


def test_declarations():
    assert declarations(C99CodePrinter(), sin(x) + n, None) == (
        {n: ('n', 'int'), x: ('x', 'real')}, None)
    assert declarations(C99CodePrinter(), x + n, 'x') == (
        {n: ('n', 'int'), x: ('x', 'real')}, ('x', 'real'))
    assert declarations(C99CodePrinter(), And(b, Gt(x, 0)), Symbol('c')) == (
        {b: ('b', 'bool'), x: ('x', 'real')}, ('c', 'bool'))
    raises(PrintedCodeError, lambda: declarations(C99CodePrinter(), x, 'z'))
    m = Symbol('m', integer=True)
    assert declarations(RustCodePrinter(), ITE(Gt(n, 1), m, n), Symbol('r', integer=True)) == (
        {m: ('m', 'int'), n: ('n', 'int')}, ('r', 'int'))
    assert declarations(RustCodePrinter(), ITE(b, b, Gt(x, 0)), 'c') == (
        {b: ('b', 'bool'), x: ('x', 'real')}, ('c', 'bool'))


def _problem(printer, expr, assign_to=None):
    """The message of the PrintedCodeError that check_code() raises, or None."""
    try:
        check_code(printer, expr, assign_to, printer.doprint(expr, assign_to))
    except PrintedCodeError as problem:
        return str(problem)
    return None


def test_check_code():
    with _environment('SYMPY_CHECK_PRINTED_CODE', '0'):
        assert _problem(C99CodePrinter(), sin(x) + n) is None
        assert _problem(RustCodePrinter(), And(b, Gt(x, 0)), Symbol('y')) is None
        assert _problem(C99CodePrinter(), x, 'x') is None
        assert _problem(C99CodePrinter(), 5) is None
        assert _problem(C99CodePrinter(), z + x).startswith('The type of z is unknown')
        assert _problem(C99CodePrinter(), x, 'z').startswith('The type of z is unknown')
        assert 'since it uses arrays' in _problem(C99CodePrinter(), MatrixSymbol('A', 2, 2)[0, 1])
        assert 'since it uses arrays' in _problem(C99CodePrinter(), x, MatrixSymbol('A', 1, 1)[0, 0])
        assert "since it's a list" in _problem(C99CodePrinter(), [x, x])
        assert 'setting user_functions' in _problem(
            C99CodePrinter({'user_functions': {'sin': 'mysin'}}), sin(x)).replace('\n', ' ')
        assert 'setting type_aliases' in _problem(
            C99CodePrinter({'type_aliases': {real: float80}}), x).replace('\n', ' ')
        assert 'setting human' in _problem(C99CodePrinter({'human': False}), z)


def test_wrap_in_function():
    assert wrap_in_function(C89CodePrinter, 'y = M_PI*x;', [('x', 'real')], ('y', 'real')) == (
        '#define _XOPEN_SOURCE 700\n#include <math.h>\n#include <stdlib.h>\n'
        '\nvoid f(double x)\n{\n    double y;\n    y = M_PI*x;\n}\n')
    assert wrap_in_function(RustCodePrinter, 'b && x > 0.0', [('b', 'bool'), ('x', 'real')], None
                  ).endswith('\npub fn f(b: bool, x: f64)\n{\n    let _ = {\n'
                             '        b && x > 0.0\n    };\n}\n')


def test_check_printed_code():
    doprint = CodePrinter.doprint

    class SubclassPrinter(C99CodePrinter):
        pass

    @check_printed_code
    def test_declared():
        assert rust_code(sin(x) + n) == 'n as f64 + x.sin()'
        assert octave_code(z) == 'z'  # not checked
        assert SubclassPrinter().doprint(z) == 'z'  # not checked
    test_declared()
    assert test_declared.__name__ == 'test_declared'

    @check_printed_code
    def test_undeclared():
        assert ccode(z + 1) == 'z + 1'
    e = raises(PrintedCodeError, test_undeclared)
    assert str(e.value).startswith('C99CodePrinter printed\n\n    z + 1\n\nThe type of z')

    @check_printed_code
    def test_fails():
        assert ccode(z + 1) == 'wrong'
    raises(AssertionError, test_fails)

    @check_printed_code
    def test_prints_nothing():
        pass
    raises(PrintedCodeError, test_prints_nothing)

    @check_printed_code
    def test_unchecked():
        assert ccode(sin(x)) == 'sin(x)'
        assert ccode(sin(x), user_functions={'sin': 'sin'}) == 'sin(x)'
        assert ccode(z, human=False) == (set(), set(), 'z')
        ccode([x, x])
    e = raises(PrintedCodeError, test_unchecked)
    assert [problem in str(e.value).replace('\n', ' ') for problem in (
        'setting user_functions', 'setting human', "since it's a list")] == [True]*3
    assert CodePrinter.doprint is doprint


def test_compiling_enabled():
    with _environment('SYMPY_CHECK_PRINTED_CODE', '0'):
        assert not compiling_enabled(C99CodePrinter)
    with _environment('PATH', ''):
        with _environment('SYMPY_CHECK_PRINTED_CODE', ''):
            assert not compiling_enabled(C99CodePrinter)
        with _environment('SYMPY_CHECK_PRINTED_CODE', '1'):
            e = raises(RuntimeError, lambda: compiling_enabled(C99CodePrinter))
            assert str(e.value).startswith('gcc is needed')


@contextmanager
def _environment(name, value):
    old = os.environ.get(name)
    os.environ[name] = value
    try:
        yield
    finally:
        if old is None:
            del os.environ[name]
        else:
            os.environ[name] = old


def test_check_compiles():
    if not (compiling_enabled(C99CodePrinter) and compiling_enabled(RustCodePrinter)):
        skip("gcc or rustc isn't found or SYMPY_CHECK_PRINTED_CODE is 0")
    def wrap_and_compile(printer_class, code):
        check_compiles(printer_class, wrap_in_function(printer_class, code, [('x', 'real')], None))
    e = raises(PrintedCodeError, lambda: wrap_and_compile(RustCodePrinter, 'x + 42'))
    assert str(e.value).startswith("This doesn't compile.") and 'cannot add' in str(e.value)
    wrap_and_compile(RustCodePrinter, 'x + 42.0')
    e = raises(PrintedCodeError, lambda: wrap_and_compile(C99CodePrinter, 'x % x'))
    assert 'invalid operands' in str(e.value)
    wrap_and_compile(C99CodePrinter, 'fmod(x, x)')
