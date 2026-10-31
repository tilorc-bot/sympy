from __future__ import annotations

import math
import os
import shutil
from contextlib import contextmanager

from sympy.codegen.ast import float80, real
from sympy.core.mod import Mod
from sympy.core.numbers import oo, pi
from sympy.core.relational import Gt
from sympy.core.symbol import Symbol, symbols
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.functions.elementary.trigonometric import sin
from sympy.logic.boolalg import And, Equivalent
from sympy.matrices.expressions.matexpr import MatrixSymbol
from sympy.printing.c import C99CodePrinter, ccode
from sympy.printing.codeprinter import CodePrinter, rust_code
from sympy.printing.fortran import FCodePrinter
from sympy.printing.octave import octave_code
from sympy.printing.rust import RustCodePrinter
from sympy.testing.check_printed_code import (PrintedCodeError, check_code, check_printed_code,
                                              check_runs, compiling_enabled, declare,
                                              fixed_values, sympy_value, target_name,
                                              wrap_in_program)
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


def _problem(printer, expr, assign_to=None):
    """The message of the PrintedCodeError that check_code() raises, or None."""
    try:
        check_code(printer, expr, assign_to, printer.doprint(expr, assign_to))
    except PrintedCodeError as problem:
        return str(problem)
    return None


def test_check_code():
    with _environment('0'):
        assert _problem(C99CodePrinter(), sin(x) + n) is None
        assert _problem(RustCodePrinter(), And(b, Gt(x, 0)), Symbol('y')) is None
        assert _problem(C99CodePrinter(), x, 'x') is None
        assert _problem(C99CodePrinter(), z + x).startswith('The type of z is unknown')
        assert _problem(C99CodePrinter(), x, 'z').startswith('The type of z is unknown')
        assert 'since it uses arrays' in _problem(C99CodePrinter(), MatrixSymbol('A', 2, 2)[0, 1])
        assert 'since it uses arrays' in _problem(C99CodePrinter(), x, MatrixSymbol('A', 1, 1)[0, 0])
        assert 'setting user_functions' in _problem(
            C99CodePrinter({'user_functions': {'sin': 'mysin'}}), sin(x)).replace('\n', ' ')
        assert 'setting type_aliases' in _problem(
            C99CodePrinter({'type_aliases': {real: float80}}), x).replace('\n', ' ')


def test_target_name():
    assert target_name(C99CodePrinter()) == 'C99CodePrinter'
    assert target_name(FCodePrinter({'standard': 95, 'source_format': 'free'})) == (
        "FCodePrinter(standard=95, source_format='free')")


def test_check_fortran_code():
    with _environment('0'):
        assert _problem(FCodePrinter({'standard': 95, 'source_format': 'free'}), x) is None
        assert 'there is no compiler for FCodePrinter(standard=66' in _problem(
            FCodePrinter({'standard': 66}), x).replace('\n', ' ')


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


def test_wrap_in_fortran_program():
    a = symbols('a:12', real=True)
    names = sorted(map(str, a))
    code = FCodePrinter().doprint(pi*sum(a))
    assert wrap_in_program("FCodePrinter(standard=77, source_format='fixed')", code,
                           [(name, 'real') for name in names], None) == (
        '      program sympy_check\n'
        '      implicit none\n'
        '      integer sympy_status\n'
        + ''.join('      double precision %s\n' % name for name in names) +
        '      double precision pi\n'
        '      parameter (pi = 3.1415926535897932d0)\n'
        '      do\n'
        '      read (*, *, iostat=sympy_status) a0, a1, a10, a11, a2, a3,\n'
        '     @      a4, a5, a6, a7, a8, a9\n'
        '      if (sympy_status /= 0) exit\n'
        '      print *,\n'
        '     @pi*(a0 + a1 + a10 + a11 + a2 + a3 + a4 + a5 + a6 + a7 + a8 + a9)\n'
        '      end do\n'
        '      end program\n')
    code = FCodePrinter({'source_format': 'free'}).doprint(And(b, Gt(x, 0)), 'y')
    assert wrap_in_program("FCodePrinter(standard=77, source_format='free')", code,
                           [('b', 'bool'), ('x', 'real')], ('y', 'bool')) == (
        'program sympy_check\nimplicit none\ninteger sympy_status\n'
        'logical b\ndouble precision x\nlogical y\n'
        'do\nread (*, *, iostat=sympy_status) b, x\nif (sympy_status /= 0) exit\n'
        'y = b .and. x > 0\nprint *, y\nend do\nend program\n')


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


def test_check_runs():
    if shutil.which('rustc') is None or shutil.which('gcc') is None:
        skip('rustc and gcc are needed')
    r, s = symbols('r s', real=True)

    def problem(printer_name, code, parameters, expr, symbols):
        e = raises(PrintedCodeError, lambda: check_runs(printer_name, code, parameters, None,
                                                        expr, symbols))
        return str(e.value)

    check_runs('RustCodePrinter', 'n as f64 + x', [('n', 'int'), ('x', 'real')], None,
               x + n, [n, x])
    error = problem('RustCodePrinter', 'x + 42', [('x', 'real')], x + 42, [x])
    assert error.startswith("This doesn't compile.") and 'cannot add' in error
    assert problem('RustCodePrinter', 'x + 1.5', [('x', 'real')], x + 1, [x]) == (
        "This gives 1.5 for x = 0.0, but SymPy's value of x + 1 is 1.0.")
    # fmod has the sign of r, but Mod(r, s) has the sign of s
    fmod = problem('C99CodePrinter', 'fmod(r, s)', [('r', 'real'), ('s', 'real')],
                   Mod(r, s), [r, s])
    assert fmod.startswith('This gives') and "SymPy's value of Mod(r, s)" in fmod
    check_runs('C99CodePrinter', 'INFINITY', [], None, oo, [])


def test_check_fortran_runs():
    if shutil.which('gfortran') is None:
        skip('gfortran is needed')
    a, c, e = symbols('a c e')
    check_runs("FCodePrinter(standard=77, source_format='fixed')",
               FCodePrinter().doprint(pi*x + n), [('n', 'int'), ('x', 'real')], None,
               pi*x + n, [n, x])
    # a .eqv. b .eqv. c is (a .eqv. b) .eqv. c
    expr = Equivalent(a, b, c)
    code = FCodePrinter({'standard': 2003, 'source_format': 'free'}).doprint(expr, e)
    error = raises(PrintedCodeError, lambda: check_runs(
        "FCodePrinter(standard=2003, source_format='free')", code,
        [('a', 'bool'), ('b', 'bool'), ('c', 'bool')], ('e', 'bool'), expr, [a, b, c]))
    assert str(error.value).startswith('This gives F for a = False, b = False, c = False')
    code = FCodePrinter({'standard': 95}).doprint(Mod(x, n))
    error = raises(PrintedCodeError, lambda: check_runs(
        "FCodePrinter(standard=95, source_format='fixed')", code,
        [('n', 'int'), ('x', 'real')], None, Mod(x, n), [n, x]))
    assert (str(error.value).startswith("This doesn't compile.")
            and 'must have the same type' in str(error.value))
