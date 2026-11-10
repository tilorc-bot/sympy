from __future__ import annotations

from sympy.abc import x, y
from sympy.assumptions.ask import _ask_single_fact as _ask_single_fact_of_ask
from sympy.assumptions.ask import Q, _extract_all_facts
from sympy.assumptions.ask_generated import get_known_facts_dict
from sympy.assumptions.cnf import CNF
from sympy.assumptions.rule_engine import (SELF, _ask_single_fact, _local_facts,
    ask_by_rules, index_rules)
from sympy.core.expr import Expr
from sympy.core.function import Function
from sympy.core.power import Pow
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.exponential import exp

RULES = index_rules([
    (Abs, Q.even, (0, Q.even)),
    (Abs, ~Q.negative),
    (Abs, Q.zero, (0, Q.zero)),
    (Abs, ~Q.zero, (0, ~Q.zero)),
    (exp, Q.positive, (0, Q.real)),
    (Pow, Q.positive, (0, Q.positive), (1, Q.real)),
    (Expr, Q.real, (SELF, Q.positive)),
    (Expr, ~Q.zero, (SELF, Q.positive)),
    (Expr, Q.nonnegative, (SELF, Q.positive)),
    (Expr, Q.positive, (SELF, Q.nonnegative), (SELF, ~Q.zero)),
])


def ask(predicate, expr, assumptions=True):
    return ask_by_rules(predicate, expr, assumptions, RULES)


def test_index_rules():
    assert index_rules([(Abs, Q.even, (0, Q.even)), (Abs, ~Q.negative),
                        (Abs, ~Q.zero, (0, ~Q.zero), (SELF, Q.real)),
                        (Abs, Q.even, (0, Q.zero))]) == {
        (Abs, Q.even, True): [((0, Q.even, True),), ((0, Q.zero, True),)],
        (Abs, Q.negative, False): [()],
        (Abs, Q.zero, False): [((0, Q.zero, False), (SELF, Q.real, True))],
    }


def test_local_facts():
    assert _local_facts(True) == {}
    assert _local_facts(Q.even(x)) == {x: [(Q.even, True)]}
    local_facts = _local_facts(~Q.even(x) & Q.real(y) & Q.zero(x))
    assert set(local_facts) == {x, y}
    assert set(local_facts[x]) == {(Q.zero, True), (Q.even, False)}
    assert local_facts[y] == [(Q.real, True)]
    assert _local_facts(Q.even(x) | Q.odd(x)) == {}
    assert _local_facts(Q.gt(x, y) & Q.real(x)) == {x: [(Q.real, True)]}


def test_ask_single_fact():
    assert _ask_single_fact(Q.zero, [(Q.zero, False)]) is False
    assert _ask_single_fact(Q.zero, [(Q.even, False)]) is False
    assert _ask_single_fact(Q.even, [(Q.zero, True)]) is True
    assert _ask_single_fact(Q.even, [(Q.odd, True)]) is False
    assert _ask_single_fact(Q.even, [(Q.integer, True)]) is None
    assert _ask_single_fact(Q.even, [(Q.real, True), (Q.zero, True)]) is True
    assert _ask_single_fact(Q.even, None) is None


def test_ask_single_fact_agrees_with_the_one_of_ask():
    predicates = sorted(get_known_facts_dict(), key=str)
    for key in predicates:
        for predicate in predicates:
            for value in (True, False):
                assumption = predicate(x) if value else ~predicate(x)
                expected = _ask_single_fact_of_ask(
                    key, _extract_all_facts(CNF.from_prop(assumption), (x,)))
                assert _ask_single_fact(key, [(predicate, value)]) is expected


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
    assert ask(Q.even, Abs(x), Q.even(Abs(x)) & Q.real(y)) is True
    # only a predicate, its negation, and a conjunction of these are used
    assert ask(Q.even, Abs(x), Q.even(x) | Q.even(Abs(x))) is None
    assert ask(Q.even, Abs(x), ~(Q.odd(Abs(x)) | ~Q.even(Abs(x)))) is None


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


def test_cycle():
    # positive has an edge to nonnegative, which has one back to positive
    assert ask(Q.positive, x) is None
    assert ask(Q.nonnegative, x) is None
    assert ask(Q.positive, x, Q.nonnegative(x) & ~Q.zero(x)) is True
    assert ask(Q.nonnegative, exp(x), Q.real(x)) is True


def test_no_answer_below_a_cycle_is_not_kept():
    class g(Function):
        pass

    # These rules are not true of anything: they only have the shape which
    # is tested. The first rule of real leads to positive, which leads back
    # to real: a cycle, so positive has no answer there. The second rule
    # then answers real, and positive has an answer after that.
    rules = index_rules([
        (g, Q.real, (SELF, Q.positive)),
        (g, Q.real, (0, Q.integer)),
        (g, Q.positive, (SELF, Q.real)),
        (g, Q.nonzero, (SELF, Q.real), (SELF, Q.positive)),
    ])
    assert ask_by_rules(Q.nonzero, g(x), Q.integer(x), rules) is True
    assert ask_by_rules(Q.nonzero, g(x), True, rules) is None
