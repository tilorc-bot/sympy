from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.assumptions.core_rules import _CoreRuleEngine, _rules_for_steps
from sympy.assumptions.rule_engine import FALSE_IF, FIRST_ARG_IS, TRUE_IF
from sympy.core.add import Add
from sympy.core.function import Function
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


def test_a_handler_is_called_once_for_an_object():
    calls = []

    class Counted(Function):
        def _eval_is_extended_real(self):
            calls.append(self)

    f = Counted(Symbol('x'))
    assert f.is_positive is None
    assert f.is_negative is None
    assert f.is_zero is None
    assert f.is_extended_real is None
    assert calls == [f]


def test_what_was_tried_is_not_what_is_known():
    class Sometimes(Function):
        def _eval_is_integer(self):
            return self.args[0].is_integer

    assert Sometimes(Symbol('x')).is_rational is None
    f = Sometimes(Symbol('n', integer=True))
    assert f.is_zero is None
    assert f.is_rational is True


def test_rules_for_steps():
    engine = _CoreRuleEngine({}, {})
    infinite = [(FIRST_ARG_IS, Q.infinite)]
    not_real = [(FIRST_ARG_IS, Q.imaginary)]
    rules = _rules_for_steps({
        (Abs, Q.positive_infinite): [(TRUE_IF, infinite)],
        (Abs, Q.nonzero): [(FALSE_IF, not_real)],
        (Abs, Q.integer): [(TRUE_IF, [(FIRST_ARG_IS, Q.integer)])],
    }, engine.predicates)
    # a predicate which is not a fact of the old assumptions: repeated for
    # the facts from which they deduce the others
    assert rules[Abs, Q.infinite] == [(TRUE_IF, infinite)]
    assert rules[Abs, Q.extended_positive] == [(TRUE_IF, infinite)]
    assert (Abs, Q.finite) not in rules and (Abs, Q.extended_real) not in rules
    # an implication which the old assumptions do not have
    assert rules[Abs, Q.irrational] == [(FALSE_IF, not_real)]
    # the old assumptions deduce everything which follows from an integer
    assert (Abs, Q.rational) not in rules and (Abs, Q.real) not in rules


def test_what_was_tried_for_an_object_of_another_class():
    class Positive(Function):
        def _eval_is_positive(self):
            return True

    class Unknown(Function):
        pass

    x = Symbol('x')
    unknown = Unknown(x)
    assert unknown.is_zero is None
    positive = Positive(x)
    positive._assumptions = unknown._assumptions
    assert positive.is_positive is True
