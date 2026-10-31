from __future__ import annotations

import math

from hypothesis import given, settings, strategies as st

from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.core.numbers import Float, I, Integer, Rational, nan, oo, zoo
from sympy.core.power import Pow
from sympy.core.singleton import S
from sympy.core.symbol import symbols
from sympy.core.traversal import preorder_traversal
from sympy.functions.elementary.complexes import Abs, sign
from sympy.functions.elementary.exponential import exp, log
from sympy.functions.elementary.integers import floor
from sympy.functions.elementary.miscellaneous import Max, Min, sqrt
from sympy.functions.elementary.trigonometric import sin
from sympy.printing.c import C99CodePrinter
from sympy.testing.check_printed_code import compiled_function, compiling_enabled
from sympy.testing.pytest import skip, slow


def _random_expressions():
    """A strategy for expressions in real x, y and integer i, j, such as
    Max(i, y) or sin(x)**2 + floor(j/2). An exponent is a symbol or a number,
    since i**(i**i) is a huge integer for i = 10. There is no Mod, which ccode
    prints as fmod, which has the wrong sign (see test_ccode_Mod_values)."""
    x, y = symbols('x y', real=True)
    i, j = symbols('i j', integer=True)
    leaves = st.sampled_from([x, y, i, j, S(2), S(-3), Rational(1, 2), Float(-2.5)])
    binary = st.sampled_from([Add, Mul, Min, Max])
    unary = st.sampled_from([sin, exp, log, sqrt, Abs, floor, sign])

    def apply(function, *args):
        try:
            return function(*args)
        except (ValueError, TypeError, ZeroDivisionError):
            return nan  # e.g. Min of a complex number

    return st.recursive(
        leaves,
        lambda e: (st.builds(apply, binary, e, e) | st.builds(apply, st.just(Pow), e, leaves)
                   | st.builds(apply, unary, e)),
        max_leaves=5,
    ).filter(lambda e: e.free_symbols and not e.has(nan, zoo, oo, -oo, I))


# Integers, and reals that are 0 or not tiny, so that products don't underflow
INTEGERS = st.integers(-10, 10)
REALS = st.one_of(st.just(0.0), st.floats(-10, -1e-3), st.floats(1e-3, 10))


@st.composite
def _expressions_and_points(draw):
    """A strategy for an expression from _random_expressions() and 10 points,
    each a value of each of its symbols, sorted by name."""
    expr = draw(_random_expressions())
    values = [INTEGERS if symbol.is_integer else REALS
              for symbol in sorted(expr.free_symbols, key=str)]
    return expr, draw(st.lists(st.tuples(*values), min_size=10, max_size=10))


def _check_values(printer, expr, points):
    """Check that the compiled code that printer prints for expr gives
    SymPy's value of expr at each point, a value of each of its symbols,
    sorted by name."""
    symbols = sorted(expr.free_symbols, key=str)
    function = compiled_function(printer, symbols, expr)
    for point in points:
        expected = _expected_value(expr, symbols, point)
        if expected is None:
            continue
        value = function(*point)
        assert _close(value, expected), (
            '%s printed %s, which gives %r for %s, but SymPy gives %r'
            % (type(printer).__name__, printer.doprint(expr), value,
               dict(zip(symbols, point)), expected))


def _expected_value(expr, symbols, point):
    """SymPy's value of expr at point, or None if the code may give any value
    there: where the value of a part of expr isn't a real number (C has no
    complex numbers, so log(i)**2 is NaN at i = -1), where the code could crash
    (e.g. dividing an integer by 0), or next to a jump in a real symbol (e.g.
    of floor), where rounding can give the value on either side."""
    if any(_sympy_value(part, symbols, point) is None
           for part in preorder_traversal(expr) if part.free_symbols):
        return None
    expected = _sympy_value(expr, symbols, point)
    nearby = [_sympy_value(expr, symbols, [*point[:k], value + nudge*max(1, abs(value)),
                                           *point[k + 1:]])
              for k, value in enumerate(point) if isinstance(value, float)
              for nudge in (1e-12, -1e-12)]
    if not all(value is not None and _close(value, expected) for value in nearby):
        return None
    return expected


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


# The printer must not raise, and what it prints must compute SymPy's values.
# The test is skipped if gcc isn't found or doesn't work (see
# compiling_enabled()), and slow, since it compiles many expressions.

@slow
@settings(derandomize=True, database=None, report_multiple_bugs=False)
@given(_expressions_and_points())
def test_ccode(expr_and_points):
    if not compiling_enabled(C99CodePrinter):
        skip("gcc isn't found or doesn't work")
    _check_values(C99CodePrinter(), *expr_and_points)
