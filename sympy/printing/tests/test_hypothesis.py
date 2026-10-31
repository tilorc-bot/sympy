from __future__ import annotations

import math

from hypothesis import given, settings, strategies as st

from sympy.core.add import Add
from sympy.core.mod import Mod
from sympy.core.mul import Mul
from sympy.core.numbers import Float, I, Integer, Rational, nan, oo, zoo
from sympy.core.power import Pow
from sympy.core.singleton import S
from sympy.core.symbol import symbols
from sympy.functions.elementary.complexes import Abs, sign
from sympy.functions.elementary.exponential import exp, log
from sympy.functions.elementary.integers import floor
from sympy.functions.elementary.miscellaneous import Max, Min, sqrt
from sympy.functions.elementary.trigonometric import sin
from sympy.printing.c import ccode
from sympy.printing.codeprinter import rust_code
from sympy.printing.cxx import cxxcode
from sympy.testing.check_printed_code import compile_function, compiling_enabled
from sympy.testing.pytest import XFAIL, skip


def _random_expressions():
    """A strategy for expressions in real x, y and integer i, j, such as
    Max(i, y) or sin(x)**2 + floor(j/2)."""
    x, y = symbols('x y', real=True)
    i, j = symbols('i j', integer=True)
    leaves = st.sampled_from([x, y, i, j, S(2), S(-3), Rational(1, 2), Float(-2.5)])
    binary = st.sampled_from([Add, Mul, Pow, Mod, Min, Max])
    unary = st.sampled_from([sin, exp, log, sqrt, Abs, floor, sign])

    def apply(function, *args):
        try:
            return function(*args)
        except (ValueError, TypeError, ZeroDivisionError):
            return nan  # e.g. Min of a complex number

    return st.recursive(
        leaves,
        lambda e: st.builds(apply, binary, e, e) | st.builds(apply, unary, e),
        max_leaves=5,
    ).filter(lambda e: e.free_symbols and not e.has(nan, zoo, oo, -oo, I))


# Integers, and reals that are 0 or not tiny, so that products don't underflow
INTEGERS = st.integers(-10, 10)
REALS = st.one_of(st.just(0.0), st.floats(-10, -1e-3), st.floats(1e-3, 10))


def _check_values(printer_name, code, expr, data):
    """Compile code, which the printer printed for expr, and check that it
    computes SymPy's value of expr for 10 values of its symbols from data."""
    symbols = sorted(expr.free_symbols, key=str)
    types = ['int' if symbol.is_integer else 'real' for symbol in symbols]
    function = compile_function(printer_name, code, tuple(zip(map(str, symbols), types)))
    for _ in range(10):
        values = [data.draw(INTEGERS if type_name == 'int' else REALS) for type_name in types]
        expected = _sympy_value(expr, symbols, values)
        nearby = [_sympy_value(expr, symbols, [value*(1 + nudge) for value in values])
                  for nudge in (1e-12, -1e-12)]
        # Not where SymPy's value isn't a real number, where the code could
        # crash (e.g. dividing an integer by 0), or next to a jump (e.g. of
        # floor or Mod), where rounding can give the value on either side
        if expected is None or not all(value is not None and _close(value, expected)
                                       for value in nearby):
            continue
        value = function(*values)
        assert _close(value, expected), (
            '%s printed %s, which gives %r for %s, but SymPy gives %r'
            % (printer_name, code, value, dict(zip(symbols, values)), expected))


def _sympy_value(expr, symbols, values):
    """SymPy's value of expr for the values of its symbols, or None if it
    isn't a real number."""
    try:
        value = expr.xreplace({
            symbol: Integer(value) if isinstance(value, int) else Float(value, 30)
            for symbol, value in zip(symbols, values)}).evalf(30)
    except (ArithmeticError, ValueError):  # e.g. Mod(x, 0)
        return None
    if not value.is_Number or value is S.NaN or value is S.ComplexInfinity:
        return None
    return float(value)


def _close(value, expected):
    return math.isclose(value, expected, rel_tol=1e-6, abs_tol=1e-6)


# The printers must not raise, and what they print must compute SymPy's
# values. Compiling needs SYMPY_CHECK_PRINTED_CODE, and without it the tests
# are skipped.

@XFAIL  # ccode(Mod(x, y)) prints fmod(x, y), which has the sign of x, not y
@settings(derandomize=True, database=None, report_multiple_bugs=False)
@given(_random_expressions(), st.data())
def test_ccode(expr, data):
    if not compiling_enabled():
        skip('SYMPY_CHECK_PRINTED_CODE is not set')
    _check_values('C99CodePrinter', ccode(expr), expr, data)


@XFAIL  # cxxcode(Min(i, x)) calls std::min with an int and a double
@settings(derandomize=True, database=None, report_multiple_bugs=False)
@given(_random_expressions(), st.data())
def test_cxxcode(expr, data):
    if not compiling_enabled():
        skip('SYMPY_CHECK_PRINTED_CODE is not set')
    _check_values('CXX11CodePrinter', cxxcode(expr), expr, data)


@XFAIL  # rust_code(i**2) calls powi on an i32
@settings(derandomize=True, database=None, report_multiple_bugs=False)
@given(_random_expressions(), st.data())
def test_rust_code(expr, data):
    if not compiling_enabled():
        skip('SYMPY_CHECK_PRINTED_CODE is not set')
    _check_values('RustCodePrinter', rust_code(expr), expr, data)
