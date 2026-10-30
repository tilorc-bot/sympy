from __future__ import annotations

import math
import os
import shutil
from contextlib import contextmanager

from sympy.codegen.ast import float80, real
from sympy.core.mod import Mod
from sympy.core.numbers import oo
from sympy.core.relational import Gt
from sympy.core.symbol import Symbol, symbols
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.functions.elementary.trigonometric import sin
from sympy.logic.boolalg import And
from sympy.matrices.expressions.matexpr import MatrixSymbol
from sympy.printing.c import C99CodePrinter, ccode
from sympy.printing.codeprinter import CodePrinter, rust_code
from sympy.printing.octave import octave_code
from sympy.printing.rust import RustCodePrinter
from sympy.testing.check_printed_code import (PrintedCodeError, check_printed_code,
                                              compiling_enabled, find_problem,
                                              find_run_problem, fixed_values,
                                              symbol_type, sympy_value,
                                              unsupported_reason, wrap_in_program)
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


def test_wrap_in_program():
    c = wrap_in_program('C99CodePrinter', 'y = n + x;', [('n', 'int'), ('x', 'real')], ('y', 'real'))
    assert c.endswith(
        'int main(void)\n{\n    char sympy_line[4096];\n'
        '    while (fgets(sympy_line, sizeof sympy_line, stdin)) {\n'
        '        char *sympy_p = sympy_line;\n'
        '        int n = (int)strtol(sympy_p, &sympy_p, 10);\n'
        '        double x = strtod(sympy_p, &sympy_p);\n'
        '        double y;\n        y = n + x;\n'
        '        printf("%.17g\\n", (double)y);\n        fflush(stdout);\n'
        '    }\n    return 0;\n}\n')
    rust = wrap_in_program('RustCodePrinter', 'b && x > 0.0', [('b', 'bool'), ('x', 'real')], None)
    assert ('        let mut b: bool = sympy_values.next().unwrap().parse().unwrap();\n'
            '        let mut x: f64 = sympy_values.next().unwrap().parse().unwrap();\n'
            '        let sympy_value = {\n            b && x > 0.0\n        };\n'
            '        println!("{:?}", sympy_value);\n') in rust


def test_sympy_value():
    assert sympy_value(x + n, [n, x], ['int', 'real'], [2, 0.5]) == 2.5
    assert sympy_value(And(b, Gt(x, 0)), [b, x], ['bool', 'real'], [True, 0.5]) == 1.0
    assert sympy_value(sqrt(x), [x], ['real'], [-1.0]) is None
    assert sympy_value(1/x, [x], ['real'], [0.0]) is None
    assert sympy_value(Mod(x, n), [n, x], ['int', 'real'], [0, 1.5]) is None
    assert sympy_value(x*oo, [x], ['real'], [1.0]) == math.inf


def test_fixed_values():
    p = Symbol('p', positive=True)
    values = fixed_values([n, p, x], ['int', 'real', 'real'])
    assert len(values) == 50 and len(set(values)) == 50
    assert all(isinstance(i, int) and v > 0 for i, v, _ in values)
    assert fixed_values([b, x], ['bool', 'real']) == [
        (False, 0.0), (False, 1.0), (False, -1.0), (False, 0.5), (False, -2.5),
        (False, 3.75), (True, 0.0), (True, 1.0), (True, -1.0), (True, 0.5),
        (True, -2.5), (True, 3.75)]


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


def test_find_run_problem():
    if shutil.which('rustc') is None or shutil.which('gcc') is None:
        skip('rustc and gcc are needed')
    r, s = symbols('r s', real=True)
    assert find_run_problem('RustCodePrinter', 'n as f64 + x', [('n', 'int'), ('x', 'real')], None,
                    x + n, [n, x]) is None
    error = find_run_problem('RustCodePrinter', 'x + 42', [('x', 'real')], None, x + 42, [x])
    assert error.startswith("This doesn't compile.") and 'cannot add' in error
    assert find_run_problem('RustCodePrinter', 'x + 1.5', [('x', 'real')], None, x + 1, [x]) == (
        "This gives 1.5 for x = 0.0, but SymPy's value of x + 1 is 1.0.")
    # fmod has the sign of r, but Mod(r, s) has the sign of s
    fmod = find_run_problem('C99CodePrinter', 'fmod(r, s)', [('r', 'real'), ('s', 'real')], None,
                    Mod(r, s), [r, s])
    assert fmod.startswith('This gives') and "SymPy's value of Mod(r, s)" in fmod
    assert find_run_problem('C99CodePrinter', 'INFINITY', [], None, oo, []) is None
