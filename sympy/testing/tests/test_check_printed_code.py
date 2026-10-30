from __future__ import annotations

import os
import shutil
from contextlib import contextmanager

from sympy.codegen.ast import float80, real
from sympy.core.relational import Gt
from sympy.core.symbol import Symbol, symbols
from sympy.functions.elementary.trigonometric import sin
from sympy.logic.boolalg import And
from sympy.matrices.expressions.matexpr import MatrixSymbol
from sympy.printing.c import C99CodePrinter, ccode
from sympy.printing.codeprinter import CodePrinter, rust_code
from sympy.printing.octave import octave_code
from sympy.printing.rust import RustCodePrinter
from sympy.testing.check_printed_code import (PrintedCodeError, check_printed_code,
                                              compiling_enabled, find_compile_problem,
                                              find_problem, symbol_type,
                                              unsupported_reason, wrap_in_function)
from sympy.testing.pytest import raises, skip

x = Symbol('x', real=True)
n = Symbol('n', integer=True)
b, z = symbols('b z')


def test_symbol_type():
    assert symbol_type(x, False) == 'real'
    assert symbol_type(n, False) == 'int'
    assert symbol_type(b, True) == 'bool'
    assert symbol_type(z, False) is None


def _find_problem(printer, expr, assign_to=None):
    return find_problem(printer, expr, assign_to, printer.doprint(expr, assign_to))


def test_find_problem():
    with _environment('0'):
        assert _find_problem(C99CodePrinter(), sin(x) + n) is None
        assert _find_problem(RustCodePrinter(), And(b, Gt(x, 0)), Symbol('y')) is None
        assert _find_problem(C99CodePrinter(), z + x).startswith('The type of z is unknown')
        assert _find_problem(C99CodePrinter(), x, 'z').startswith('The type of z is unknown')
        assert _find_problem(C99CodePrinter(), z + b).startswith('The types of b and z are unknown')
        assert 'since it uses arrays' in _find_problem(C99CodePrinter(), MatrixSymbol('A', 2, 2)[0, 1])


def test_unsupported_reason():
    assert unsupported_reason(C99CodePrinter(), x, None) is None
    assert 'setting user_functions' in unsupported_reason(
        C99CodePrinter({'user_functions': {'sin': 'mysin'}}), sin(x), None)
    assert 'setting type_aliases' in unsupported_reason(
        C99CodePrinter({'type_aliases': {real: float80}}), x, None)
    assert 'arrays' in unsupported_reason(C99CodePrinter(), x, MatrixSymbol('A', 1, 1)[0, 0])


def test_wrap_in_function():
    assert wrap_in_function('C89CodePrinter', 'y = M_PI*x;', [('x', 'real')], ('y', 'real')) == (
        '#define _XOPEN_SOURCE 700\n#include <math.h>\n#include <stdlib.h>\n'
        '\nvoid f(double x)\n{\n    double y;\n    y = M_PI*x;\n}\n')
    assert wrap_in_function('RustCodePrinter', 'b && x > 0.0', [('b', 'bool'), ('x', 'real')], None
                  ).endswith('\npub fn f(b: bool, x: f64)\n{\n    let _ = {\n'
                             '        b && x > 0.0\n    };\n}\n')


def test_check_printed_code():
    doprint = CodePrinter.doprint

    @check_printed_code
    def test_declared():
        assert rust_code(sin(x) + n) == 'n as f64 + x.sin()'
        assert octave_code(z) == 'z'  # not checked
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
    assert CodePrinter.doprint is doprint


def test_compiling_enabled():
    with _environment('0'):
        assert not compiling_enabled()
    with _environment('1'):
        assert compiling_enabled()


@contextmanager
def _environment(value):
    old = os.environ.get('SYMPY_CHECK_PRINTED_CODE')
    os.environ['SYMPY_CHECK_PRINTED_CODE'] = value
    try:
        yield
    finally:
        if old is None:
            del os.environ['SYMPY_CHECK_PRINTED_CODE']
        else:
            os.environ['SYMPY_CHECK_PRINTED_CODE'] = old


def test_find_compile_problem():
    if shutil.which('rustc') is None or shutil.which('gcc') is None:
        skip('rustc and gcc are needed')
    error = find_compile_problem('RustCodePrinter', 'x + 42', [('x', 'real')], None)
    assert error.startswith("This doesn't compile.") and 'cannot add' in error
    assert find_compile_problem('RustCodePrinter', 'x + 42.0', [('x', 'real')], None) is None
    assert 'invalid operands' in find_compile_problem('C99CodePrinter', 'x % x', [('x', 'real')], None)
    assert find_compile_problem('C99CodePrinter', 'fmod(x, x)', [('x', 'real')], None) is None
