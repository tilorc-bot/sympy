from __future__ import annotations

import shutil

from sympy.core.relational import Gt
from sympy.core.symbol import Symbol, symbols
from sympy.functions.elementary.trigonometric import sin
from sympy.logic.boolalg import And
from sympy.printing.c import C99CodePrinter, ccode
from sympy.printing.codeprinter import CodePrinter
from sympy.printing.octave import octave_code
from sympy.printing.codeprinter import rust_code
from sympy.printing.rust import RustCodePrinter
from sympy.matrices.expressions.matexpr import MatrixSymbol
from sympy.testing.check_printed_code import (PrintedCodeError, check,
                                              check_printed_code, compile_snippet,
                                              describe, source)
from sympy.testing.pytest import raises, skip

x = Symbol('x', real=True)
n = Symbol('n', integer=True)
b, z = symbols('b z')


def _describe(printer, expr, assign_to=None):
    return describe(printer, expr, assign_to, printer.doprint(expr, assign_to))


def test_describe():
    assert _describe(C99CodePrinter(), sin(x) + n) == {
        'printer': 'C99CodePrinter', 'code': 'n + sin(x)',
        'params': [['n', 'int'], ['x', 'real']], 'target': None, 'reason': None}
    s = _describe(RustCodePrinter(), And(b, Gt(x, 0)), 'y')
    assert s['params'] == [['b', 'bool'], ['x', 'real']]
    assert s['target'] == ['y', 'bool']
    assert _describe(C99CodePrinter(), z + x, 'z')['params'] == [
        ['x', 'real'], ['z', None]]
    assert _describe(C99CodePrinter(), x, 'z')['target'] == ['z', None]
    assert _describe(C99CodePrinter({'user_functions': {'sin': 'mysin'}}),
                     sin(x))['reason'] == 'printer setting user_functions'
    assert _describe(C99CodePrinter(), MatrixSymbol('A', 2, 2)[0, 1])['reason'] == 'arrays'


def test_source():
    assert source({'printer': 'C89CodePrinter', 'code': 'y = M_PI*x;',
                   'params': [['x', 'real']], 'target': ['y', 'real']}) == (
        '#define _XOPEN_SOURCE 700\n#include <math.h>\n#include <stdlib.h>\n'
        '\nvoid f(double x)\n{\n    double y;\n    y = M_PI*x;\n}\n')
    assert source({'printer': 'RustCodePrinter', 'code': 'b && x > 0.0',
                   'params': [['b', 'bool'], ['x', 'real']], 'target': None}
                  ).endswith('\npub fn f(b: bool, x: f64)\n{\n    let _ = {\n'
                             '        b && x > 0.0\n    };\n}\n')


def _snippet(code, kind, reason=None):
    return {'printer': 'RustCodePrinter', 'code': code, 'params': [['x', kind]],
            'target': None, 'reason': reason}


def test_check():
    compiled = []

    def compile(s):
        compiled.append(s['code'])
        return 'error' if s['code'] == 'x + 3' else None

    check([_snippet('x + 4.0', 'real'), _snippet('x + 4.0', 'real')], compile)
    assert compiled == ['x + 4.0']
    # Without a compiler only the declarations are checked
    check([_snippet('x + 3', 'real')])
    e = raises(PrintedCodeError, lambda: check([_snippet('x + 3', 'real')], compile))
    assert 'does not compile' in str(e.value) and 'let _ = {' in str(e.value)
    e = raises(PrintedCodeError, lambda: check([_snippet('x + 1', None)]))
    assert 'does not declare the type of x' in str(e.value)
    e = raises(PrintedCodeError, lambda: check([_snippet('A[0]', 'real', 'arrays')]))
    assert 'cannot be checked (arrays)' in str(e.value)
    e = raises(PrintedCodeError, lambda: check([]))
    assert 'printed no C, C++ or Rust code' in str(e.value)


def test_check_printed_code():
    doprint = CodePrinter.doprint

    @check_printed_code
    def test_declared():
        assert rust_code(sin(x) + n) == 'n as f64 + x.sin()'
        assert octave_code(z) == 'z'  # not recorded
    test_declared()
    assert test_declared.__name__ == 'test_declared'

    @check_printed_code
    def test_undeclared():
        assert ccode(z + 1) == 'z + 1'
    raises(PrintedCodeError, test_undeclared)

    @check_printed_code
    def test_fails():
        assert ccode(z + 1) == 'wrong'
    raises(AssertionError, test_fails)
    assert CodePrinter.doprint is doprint


def test_compile_snippet():
    if shutil.which('rustc') is None or shutil.which('gcc') is None:
        skip('rustc and gcc are needed')
    rust = _snippet('x + 42', 'real')
    assert 'cannot add' in compile_snippet(rust)
    assert compile_snippet(dict(rust, code='x + 42.0')) is None
    c = dict(rust, printer='C99CodePrinter', code='x % x')
    assert 'invalid operands' in compile_snippet(c)
    assert compile_snippet(dict(c, code='fmod(x, x)')) is None
