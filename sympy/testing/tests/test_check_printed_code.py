from __future__ import annotations

import shutil

from sympy.core.relational import Gt
from sympy.core.symbol import Symbol, symbols
from sympy.functions.elementary.trigonometric import sin
from sympy.logic.boolalg import And
from sympy.printing.c import C99CodePrinter
from sympy.printing.rust import RustCodePrinter
from sympy.matrices.expressions.matexpr import MatrixSymbol
from sympy.testing.check_printed_code import (check, compile_snippet, describe,
                                              source)
from sympy.testing.pytest import raises, skip, uncompilable_code

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


def _snippet(test, code, kind):
    return {'printer': 'RustCodePrinter', 'code': code, 'params': [['x', kind]],
            'target': None, 'reason': None, 'test': test}


def test_check():
    base = {'tests': {'test_old': 'a', 'test_edited': 'a'},
            'snippets': [_snippet('test_old', 'x', 'real')]}
    head = {'tests': {'test_old': 'a', 'test_edited': 'b', 'test_new': 'c'},
            'snippets': [_snippet('test_old', 'x', 'real'),
                         _snippet('test_old', 'x + 1', None),
                         _snippet('test_edited', 'x + 2', None),
                         _snippet('test_new', 'x + 3', 'real'),
                         _snippet('test_new', 'x + 4.0', 'real')]}
    compiled = []

    def compile(s):
        compiled.append(s['code'])
        return 'error' if s['code'] == 'x + 3' else None

    results, count = check(base, head, compile)
    assert count == 4
    assert sorted(compiled) == ['x + 3', 'x + 4.0']
    assert [status for status, _ in results] == ['warning', 'fail', 'fail', 'ok']
    assert 'does not declare the type of x' in results[0][1]
    assert 'error' in results[2][1] and 'let _ = {' in results[2][1]


def test_compile_snippet():
    if shutil.which('rustc') is None or shutil.which('gcc') is None:
        skip('rustc and gcc are needed')
    rust = _snippet('test', 'x + 42', 'real')
    assert 'cannot add' in compile_snippet(rust)
    assert compile_snippet(dict(rust, code='x + 42.0')) is None
    c = dict(rust, printer='C99CodePrinter', code='x % x')
    assert 'invalid operands' in compile_snippet(c)
    assert compile_snippet(dict(c, code='fmod(x, x)')) is None


def test_uncompilable_code():
    @uncompilable_code('prints a comment')
    def test():
        pass
    assert test._uncompilable_code == 'prints a comment'
    raises(TypeError, lambda: uncompilable_code(test))
