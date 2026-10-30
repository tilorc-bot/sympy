"""Check that the C, C++ and Rust printers print code that compiles for
expressions generated with Hypothesis.

The tests are skipped unless SYMPY_CHECK_PRINTED_CODE is set, as in the
"printed code" CI job (see sympy/testing/check_printed_code.py). The C++ and
Rust tests are marked XFAIL because those printers still print code that
does not compile for some expressions; the comments give the simplest
examples Hypothesis finds.
"""
from __future__ import annotations

import os

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
from sympy.testing.check_printed_code import ENVIRONMENT_VARIABLE, check_printed_code
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
    if not os.environ.get(ENVIRONMENT_VARIABLE):
        skip('%s is not set' % ENVIRONMENT_VARIABLE)

    @settings(deadline=None, derandomize=True, database=None)
    @given(expressions)
    @check_printed_code
    def compiles(expr):
        printer(expr)
    compiles()


def test_ccode_compiles():
    check_compiles(ccode)


@XFAIL  # cxxcode(Min(i, x)) calls std::min with an int and a double
def test_cxxcode_compiles():
    check_compiles(cxxcode)


@XFAIL  # rust_code(sin(i)) calls sin on an i32, rust_code(i**x) raises TypeError
def test_rust_code_compiles():
    check_compiles(rust_code)
