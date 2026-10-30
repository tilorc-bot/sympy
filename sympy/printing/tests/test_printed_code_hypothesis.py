"""Check that the C, C++, Fortran and Rust printers print code that
compiles, and computes the same values as SymPy, for expressions generated
with Hypothesis. Skipped unless SYMPY_CHECK_PRINTED_CODE is set (see
sympy/testing/check_printed_code.py).
"""
from __future__ import annotations

from hypothesis import given, settings, strategies as st

from sympy.core.add import Add
from sympy.core.mod import Mod
from sympy.core.mul import Mul
from sympy.core.numbers import Float, I, Rational, nan, oo, zoo
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
from sympy.printing.fortran import fcode
from sympy.testing.check_printed_code import check_printed_code, compiling
from sympy.testing.pytest import XFAIL, skip

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


expressions = st.recursive(
    leaves,
    lambda e: st.builds(apply, binary, e, e) | st.builds(apply, unary, e),
    max_leaves=5,
).filter(lambda e: e.free_symbols and not e.has(nan, zoo, oo, -oo, I))


def check_compiles(printer):
    if not compiling():
        skip('SYMPY_CHECK_PRINTED_CODE is not set')

    @settings(deadline=None, derandomize=True, database=None)
    @given(expressions)
    @check_printed_code
    def compiles(expr):
        printer(expr)
    compiles()


@XFAIL  # ccode(Mod(x, y)) prints fmod(x, y), which has the sign of x, not y
def test_ccode_compiles():
    check_compiles(ccode)


@XFAIL  # cxxcode(Min(i, x)) calls std::min with an int and a double; fmod
def test_cxxcode_compiles():
    check_compiles(cxxcode)


@XFAIL  # fcode(Mod(x, i)) prints modulo(x, i), but modulo needs arguments of one type
def test_fcode_compiles():
    # Not the default Fortran 77, for which fcode cannot print Mod or sign
    check_compiles(lambda expr: fcode(expr, standard=95))


@XFAIL  # rust_code(sin(i)) calls sin on an i32, rust_code(i**x) raises TypeError
def test_rust_code_compiles():
    check_compiles(rust_code)
