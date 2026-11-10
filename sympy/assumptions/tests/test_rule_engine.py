from __future__ import annotations

from sympy.abc import x, y
from sympy.assumptions.ask import Q
from sympy.assumptions.rule_engine import SELF, Condition, Rule, ask_by_rules
from sympy.core.expr import Expr
from sympy.core.function import Function
from sympy.core.power import Pow
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.exponential import exp

RULES = {
    # The absolute value of an even number is even
    (Abs, Q.even): (Rule(True, (Condition(Q.even, 0),)),),
    # An absolute value is not negative
    (Abs, Q.negative): (Rule(False),),
    # An absolute value is zero exactly when its argument is
    (Abs, Q.zero): (Rule(True, (Condition(Q.zero, 0),)),
                    Rule(False, (Condition(Q.zero, 0, False),))),
    # exp is positive on the reals
    (exp, Q.positive): (Rule(True, (Condition(Q.real, 0),)),),
    # A positive number to a real power is positive
    (Pow, Q.positive): (Rule(True, (Condition(Q.positive, 0),
                                    Condition(Q.real, 1))),),
    # A positive number is real, and is not zero
    (Expr, Q.real): (Rule(True, (Condition(Q.positive, SELF),)),),
    (Expr, Q.zero): (Rule(False, (Condition(Q.positive, SELF),)),),
    # A positive number is not negative, and a number which is not negative
    # and not zero is positive
    (Expr, Q.nonnegative): (Rule(True, (Condition(Q.positive, SELF),)),),
    (Expr, Q.positive): (Rule(True, (Condition(Q.nonnegative, SELF),
                                     Condition(Q.zero, SELF, False))),),
}


def ask(predicate, expr, assumptions=True):
    return ask_by_rules(predicate, expr, assumptions, RULES)


def test_rule_about_an_argument():
    assert ask(Q.even, Abs(x), Q.even(x)) is True
    assert ask(Q.even, Abs(x), Q.odd(x)) is None
    assert ask(Q.even, Abs(x)) is None
    assert ask(Q.odd, Abs(x), Q.even(x)) is None


def test_rule_without_conditions():
    assert ask(Q.negative, Abs(x)) is False


def test_condition_with_the_value_false():
    assert ask(Q.zero, Abs(x), Q.zero(x)) is True
    assert ask(Q.zero, Abs(x), ~Q.zero(x)) is False
    assert ask(Q.zero, Abs(x), Q.positive(x)) is False
    assert ask(Q.zero, Abs(x)) is None


def test_assumptions_about_the_expression():
    assert ask(Q.even, Abs(x), Q.even(Abs(x))) is True
    assert ask(Q.integer, Abs(x), Q.even(Abs(x))) is True
    assert ask(Q.even, Abs(x), Q.odd(Abs(x))) is False
    assert ask(Q.even, Abs(x), ~Q.integer(Abs(x))) is False
    # assumptions which are not a single predicate are not used
    assert ask(Q.even, Abs(x), Q.even(x) | Q.even(Abs(x))) is None


def test_conditions_are_answered_by_rules():
    assert ask(Q.even, Abs(Abs(x)), Q.even(x)) is True
    assert ask(Q.positive, exp(x)**y, Q.real(x) & Q.real(y)) is True
    assert ask(Q.positive, exp(x)**y, Q.real(x)) is None
    assert ask(Q.positive, exp(exp(x)), Q.real(x)) is True
    assert ask(Q.zero, Abs(exp(x)**y), Q.real(x) & Q.real(y)) is False


def test_rules_of_a_base_class():
    assert ask(Q.real, exp(x), Q.real(x)) is True
    assert ask(Q.real, exp(x)) is None
    assert ask(Q.zero, exp(x), Q.real(x)) is False


def test_rules_which_lead_back_to_the_question():
    # positive asks nonnegative, which asks positive
    assert ask(Q.positive, x) is None
    assert ask(Q.nonnegative, x) is None
    assert ask(Q.positive, x, Q.nonnegative(x) & ~Q.zero(x)) is True
    assert ask(Q.nonnegative, exp(x), Q.real(x)) is True


def test_no_answer_under_a_question_cut_short_is_not_kept():
    class g(Function):
        pass

    # These rules are not true of anything: they only have the shape which
    # is tested. For real, the first rule asks positive, which asks real
    # again and finds nothing; the second rule then answers real. positive
    # has an answer after that.
    rules = {
        (g, Q.real): (Rule(True, (Condition(Q.positive, SELF),)),
                      Rule(True, (Condition(Q.integer, 0),))),
        (g, Q.positive): (Rule(True, (Condition(Q.real, SELF),)),),
        (g, Q.nonzero): (Rule(True, (Condition(Q.real, SELF),
                                     Condition(Q.positive, SELF))),),
    }
    assert ask_by_rules(Q.nonzero, g(x), Q.integer(x), rules) is True
    assert ask_by_rules(Q.nonzero, g(x), True, rules) is None
