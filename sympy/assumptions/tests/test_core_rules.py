from __future__ import annotations

from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.core.numbers import E, I, nan, oo, pi
from sympy.core.power import Pow
from sympy.core.symbol import Dummy, Symbol
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.functions.elementary.trigonometric import cot
from sympy.matrices.expressions.matexpr import MatrixSymbol


def test_rules_answer():
    x = Symbol('x')
    assert Pow(x, 0, evaluate=False).is_zero is False
    assert sqrt(Symbol('x', real=False)).is_extended_negative is False
    assert cot(Symbol('a', algebraic=True)).is_algebraic is False
    assert Pow(E, I*pi/3, evaluate=False).is_imaginary is False


def test_number_facts():
    assert ((3 - I)**2/2 + I).is_zero is False
    assert (sqrt(2) - 1).is_positive is True
    assert (1 - sqrt(2)).is_negative is True
    assert Add(sqrt(2), -sqrt(2), 1, evaluate=False).is_real is True


def test_no_answer_where_nan_is_possible():
    zero = Dummy(zero=True)
    infinite = Dummy(finite=False)
    product = Mul(zero, infinite, evaluate=False)
    assert product.is_extended_positive is None
    assert product.is_extended_nonzero is None
    assert product.is_commutative is True
    assert Add(oo, -oo, evaluate=False).is_positive is None
    assert sqrt(nan, evaluate=False).is_extended_negative is None


def test_not_finite_is_not_infinite_for_the_rules():
    A = MatrixSymbol('A', 2, 3)
    row = -A[0, :]
    assert row.is_commutative is False
    assert row.is_finite is None
    assert row.is_infinite is None


def test_handler_of_a_subclass_before_the_rules_of_its_base():
    class AlwaysZero(Abs):
        def _eval_is_zero(self):
            return True

    x = Symbol('x', nonzero=True)
    assert Abs(x).is_zero is False
    assert AlwaysZero(x).is_zero is True
