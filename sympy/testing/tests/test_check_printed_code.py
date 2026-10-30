from __future__ import annotations

import math
import os
import shutil
from contextlib import contextmanager

from sympy.core.mod import Mod
from sympy.core.numbers import oo
from sympy.core.relational import Gt
from sympy.core.symbol import Symbol, symbols
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.functions.elementary.trigonometric import sin
from sympy.logic.boolalg import And
from sympy.printing.c import C99CodePrinter, ccode
from sympy.printing.codeprinter import CodePrinter
from sympy.printing.octave import octave_code
from sympy.printing.codeprinter import rust_code
from sympy.printing.rust import RustCodePrinter
from sympy.matrices.expressions.matexpr import MatrixSymbol
from sympy.testing.check_printed_code import (PrintedCodeError, check,
                                              check_printed_code, compiling,
                                              describe, fixed_values, program,
                                              run_snippets, sympy_value)
from sympy.testing.pytest import raises, skip

x = Symbol('x', real=True)
n = Symbol('n', integer=True)
b, z = symbols('b z')


def _describe(printer, expr, assign_to=None):
    return describe(printer, expr, assign_to, printer.doprint(expr, assign_to))


def test_describe():
    s = _describe(C99CodePrinter(), sin(x) + n)
    assert s['code'] == 'n + sin(x)'
    assert s['params'] == [['n', 'int'], ['x', 'real']]
    assert s['symbols'] == [n, x]
    assert s['target'] is None and s['reason'] is None
    s = _describe(RustCodePrinter(), And(b, Gt(x, 0)), 'y')
    assert s['params'] == [['b', 'bool'], ['x', 'real']]
    assert s['target'] == ['y', 'bool']
    assert _describe(C99CodePrinter(), z + x, 'z')['params'] == [
        ['x', 'real'], ['z', None]]
    assert _describe(C99CodePrinter(), x, 'z')['target'] == ['z', None]
    assert _describe(C99CodePrinter({'user_functions': {'sin': 'mysin'}}),
                     sin(x))['reason'] == 'printer setting user_functions'
    assert _describe(C99CodePrinter(), MatrixSymbol('A', 2, 2)[0, 1])['reason'] == 'arrays'


def test_program():
    c = program(_describe(C99CodePrinter(), x + n, Symbol('y', real=True)))
    assert c.endswith(
        'int main(void)\n{\n    char sympy_line[4096];\n'
        '    while (fgets(sympy_line, sizeof sympy_line, stdin)) {\n'
        '        char *sympy_p = sympy_line;\n'
        '        int n = (int)strtol(sympy_p, &sympy_p, 10);\n'
        '        double x = strtod(sympy_p, &sympy_p);\n'
        '        double y;\n        y = n + x;\n'
        '        printf("%.17g\\n", (double)y);\n        fflush(stdout);\n'
        '    }\n    return 0;\n}\n')
    rust = program(_describe(RustCodePrinter(), And(b, Gt(x, 0))))
    assert ('        let mut b: bool = sympy_values.next().unwrap().parse().unwrap();\n'
            '        let mut x: f64 = sympy_values.next().unwrap().parse().unwrap();\n'
            '        let sympy_value = {\n            b && x > 0.0\n        };\n'
            '        println!("{:?}", sympy_value);\n') in rust


def test_sympy_value():
    def value(expr, *values):
        return sympy_value(_describe(C99CodePrinter(), expr), values)
    assert value(x + n, 2, 0.5) == 2.5
    assert value(And(b, Gt(x, 0)), True, 0.5) == 1.0
    assert value(sqrt(x), -1.0) is None
    assert value(1/x, 0.0) is None
    assert value(Mod(x, n), 0, 1.5) is None
    assert value(x*oo, 1.0) == math.inf


def test_fixed_values():
    p = Symbol('p', positive=True)
    values = fixed_values(_describe(C99CodePrinter(), p + n + x))
    assert len(values) == 50 and len(set(values)) == 50
    assert all(isinstance(i, int) and v > 0 for i, v, _ in values)
    assert fixed_values(_describe(C99CodePrinter(), b & (x > 0))) == [
        (False, 0.0), (False, 1.0), (False, -1.0), (False, 0.5), (False, -2.5),
        (False, 3.75), (True, 0.0), (True, 1.0), (True, -1.0), (True, 0.5),
        (True, -2.5), (True, 3.75)]


def _snippet(code, kind, reason=None):
    return {'printer': 'RustCodePrinter', 'code': code, 'params': [['x', kind]],
            'target': None, 'expr': x, 'symbols': [x], 'reason': reason}


def test_check():
    ran = []

    def run(snippets):
        ran.extend(s['code'] for s in snippets)
        return ['error' if s['code'] == 'x + 3' else None for s in snippets]

    check([_snippet('x + 4.0', 'real'), _snippet('x + 4.0', 'real')], run)
    assert ran == ['x + 4.0']
    # Without a compiler only the declarations are checked
    check([_snippet('x + 3', 'real')])
    e = raises(PrintedCodeError, lambda: check([_snippet('x + 3', 'real')], run))
    assert 'error\nwrapped source' in str(e.value)
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


def test_compiling():
    with _environment('0'):
        assert not compiling()
    with _environment('1'):
        assert compiling()


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


def test_run_snippets():
    if shutil.which('rustc') is None or shutil.which('gcc') is None:
        skip('rustc and gcc are needed')
    r, s = symbols('r s', real=True)
    snippets = [_describe(RustCodePrinter(), x + n),
                dict(_describe(RustCodePrinter(), x + 42.0), code='x + 42'),
                dict(_describe(RustCodePrinter(), x + 1), code='x + 1.5'),
                _describe(C99CodePrinter(), Mod(r, s)),
                _describe(C99CodePrinter(), sqrt(x) + oo)]
    ok, compile_error, wrong, fmod, infinite = run_snippets(snippets)
    assert ok is None and infinite is None
    assert 'which does not compile' in compile_error and 'cannot add' in compile_error
    assert wrong.startswith('which prints 1.5 for x = 0.0, but SymPy computes 1.0')
    # fmod has the sign of r, but Mod(r, s) has the sign of s
    assert fmod.startswith('which prints') and 'for Mod(r, s)' in fmod
