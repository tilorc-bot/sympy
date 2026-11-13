from __future__ import annotations

from sympy.abc import x, y
from sympy.assumptions.ask import Q
from sympy.assumptions.ask_rules import RULES
from sympy.assumptions.ask_rules_generated import RULES as GENERATED_RULES
from sympy.assumptions.rule_checks import check_no_cycles
from sympy.assumptions.rule_closing import (close_rules, exp_rules_for_powers,
    remove_implied_rules)
from sympy.assumptions.rule_engine import (ALL_ARGS_ARE, ALL_ARGS_ARE_NOT,
    ALL_ARGS_BUT_AT_MOST_ONE_ARE, ALL_ARGS_BUT_AT_MOST_ONE_ARE_NOT, ANY_ARG_IS, ANY_ARG_IS_NOT, FALSE_IF, FIRST_ARG_IS, FIRST_ARG_IS_NOT,
    IF_AND_ONLY_IF, ONE_ARG_IS, ONE_ARG_IS_NOT, OTHER_ARGS_ARE,
    OTHER_ARGS_BUT_AT_MOST_ONE_ARE, SECOND_ARG_IS, SELF_IS,
    TRUE_IF, ask_by_rules)
from sympy.core.add import Add
from sympy.core.expr import Expr
from sympy.core.power import Pow
from sympy.core.singleton import S
from sympy.functions.combinatorial.factorials import factorial
from sympy.functions.elementary.complexes import Abs, im, re, sign
from sympy.functions.elementary.exponential import exp
from sympy.functions.elementary.trigonometric import (acos, acot, asin, atan,
    cos, cot, sin, tan)
from sympy.testing.pytest import raises


def test_generated_rules_are_up_to_date():
    assert GENERATED_RULES == exp_rules_for_powers(
        remove_implied_rules(close_rules(RULES)))


def test_no_cycles():
    check_no_cycles(GENERATED_RULES)


def test_no_equal_rules():
    for rules in GENERATED_RULES.values():
        assert len(rules) == len({repr(rule) for rule in rules})


def test_close_rules_true_direction():
    closed = close_rules({(Abs, Q.positive): [(TRUE_IF, [(FIRST_ARG_IS, Q.prime)])]})
    assert closed[(Abs, Q.real)] == [(TRUE_IF, [(FIRST_ARG_IS, Q.prime)])]
    assert closed[(Abs, Q.nonzero)] == [(TRUE_IF, [(FIRST_ARG_IS, Q.prime)])]
    assert (Abs, Q.integer) not in closed


def test_close_rules_excluded_direction():
    closed = close_rules({(Abs, Q.positive): [(TRUE_IF, [(FIRST_ARG_IS, Q.prime)])]})
    assert closed[(Abs, Q.negative)] == [(FALSE_IF, [(FIRST_ARG_IS, Q.prime)])]
    assert closed[(Abs, Q.zero)] == [(FALSE_IF, [(FIRST_ARG_IS, Q.prime)])]


def test_close_rules_false_direction():
    closed = close_rules({(Abs, Q.real): [(FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)])]})
    assert closed[(Abs, Q.positive)] == [(FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)])]
    assert closed[(Abs, Q.zero)] == [(FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)])]
    assert (Abs, Q.complex) not in closed


def test_close_rules_if_and_only_if():
    closed = close_rules({(Abs, Q.zero): [(IF_AND_ONLY_IF, [(FIRST_ARG_IS, Q.zero)])]})
    assert closed[(Abs, Q.zero)] == [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.zero)]),
    ]
    closed = close_rules({(Add, Q.zero): [
        (IF_AND_ONLY_IF, [(ALL_ARGS_ARE, Q.real), (ANY_ARG_IS, Q.zero)]),
    ]})
    assert closed[(Add, Q.zero)] == [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.real), (ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.zero)]),
    ]
    raises(ValueError, lambda: close_rules({(Add, Q.zero): [
        (IF_AND_ONLY_IF, [(ONE_ARG_IS, Q.zero)]),
    ]}))
    raises(ValueError, lambda: close_rules({(Add, Q.zero): [
        (IF_AND_ONLY_IF, [(ALL_ARGS_BUT_AT_MOST_ONE_ARE, Q.zero)]),
    ]}))


def test_close_rules_all_args_but_at_most_one():
    rule = (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_real),
                      (ALL_ARGS_BUT_AT_MOST_ONE_ARE, Q.real)])
    closed = close_rules({(Add, Q.extended_real): [rule]})
    assert closed[(Add, Q.extended_real)] == [rule]
    assert closed[(Add, Q.imaginary)] == [(FALSE_IF, rule[1])]


def test_close_rules_order_and_duplicates():
    closed = close_rules({
        (Abs, Q.real): [(TRUE_IF, [(FIRST_ARG_IS, Q.real)])],
        (Abs, Q.positive): [
            (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
            (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        ],
        (Abs, Q.negative): [(TRUE_IF, [(FIRST_ARG_IS, Q.negative)])],
    })
    assert closed[(Abs, Q.real)] == [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ]


def test_close_rules_does_not_repeat_rules_about_self():
    rules = {(Expr, Q.positive): [(TRUE_IF, [(SELF_IS, Q.prime)])]}
    assert close_rules(rules) == rules
    raises(ValueError, lambda: close_rules({
        (Expr, Q.real): [(TRUE_IF, [(SELF_IS, Q.positive)])],
        (Expr, Q.positive): [(TRUE_IF, [(SELF_IS, Q.real)])],
    }))


def test_remove_implied_rules():
    def remove(*rules):
        return remove_implied_rules({(Pow, Q.real): list(rules)})[(Pow, Q.real)]

    real = (TRUE_IF, [(FIRST_ARG_IS, Q.real)])
    positive_and_integer = (TRUE_IF, [(FIRST_ARG_IS, Q.positive),
                                      (SECOND_ARG_IS, Q.integer)])
    positive = (TRUE_IF, [(FIRST_ARG_IS, Q.positive)])
    assert remove(positive, positive_and_integer) == [positive]
    assert remove(positive_and_integer, real) == [real]
    assert remove((FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
                  (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)])) == [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)])]
    assert remove((TRUE_IF, [(FIRST_ARG_IS_NOT, Q.real)]),
                  (TRUE_IF, [(FIRST_ARG_IS_NOT, Q.positive)])) == [
        (TRUE_IF, [(FIRST_ARG_IS_NOT, Q.positive)])]
    assert remove(positive, (FALSE_IF, [(FIRST_ARG_IS, Q.real)])) == [
        positive, (FALSE_IF, [(FIRST_ARG_IS, Q.real)])]
    swapped = (TRUE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)])
    assert remove(swapped, positive_and_integer) == [swapped]
    assert remove((TRUE_IF, [(ALL_ARGS_ARE, Q.positive)]),
                  (TRUE_IF, [(ALL_ARGS_ARE, Q.real)])) == [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.real)])]
    raises(ValueError, lambda: remove((IF_AND_ONLY_IF, [(FIRST_ARG_IS, Q.zero)])))


def test_remove_implied_rules_conditions_about_how_many_arguments():
    def remove(*rules):
        return remove_implied_rules({(Add, Q.real): list(rules)})[(Add, Q.real)]

    one_positive = (TRUE_IF, [(ONE_ARG_IS, Q.positive)])
    one_prime = (TRUE_IF, [(ONE_ARG_IS, Q.prime)])
    one_positive_others_real = (TRUE_IF, [(ONE_ARG_IS, Q.positive),
                                          (OTHER_ARGS_ARE, Q.real)])
    assert remove(one_prime, one_positive) == [one_prime, one_positive]
    assert remove(one_positive_others_real, one_positive) == [
        one_positive_others_real, one_positive]
    with_first = (TRUE_IF, [(ONE_ARG_IS, Q.positive), (FIRST_ARG_IS, Q.real),
                            (OTHER_ARGS_ARE, Q.real)])
    assert remove(with_first, one_positive_others_real) == [
        one_positive_others_real]
    all_real = (TRUE_IF, [(ALL_ARGS_ARE, Q.real)])
    assert remove(one_positive_others_real, all_real) == [all_real]
    # nothing is said of the other arguments
    assert remove(one_positive, all_real) == [one_positive, all_real]
    one_not_positive_others_real = (TRUE_IF, [(ONE_ARG_IS_NOT, Q.positive),
                                              (OTHER_ARGS_ARE, Q.real)])
    assert remove(one_not_positive_others_real, all_real) == [
        one_not_positive_others_real, all_real]


def test_remove_implied_rules_all_args_but_at_most_one():
    def remove(*rules):
        return remove_implied_rules({(Add, Q.real): list(rules)})[(Add, Q.real)]

    real = (TRUE_IF, [(ALL_ARGS_BUT_AT_MOST_ONE_ARE, Q.real)])
    positive = (TRUE_IF, [(ALL_ARGS_BUT_AT_MOST_ONE_ARE, Q.positive)])
    assert remove(positive, real) == [real]
    not_real = (TRUE_IF, [(ALL_ARGS_BUT_AT_MOST_ONE_ARE_NOT, Q.real)])
    not_positive = (TRUE_IF, [(ALL_ARGS_BUT_AT_MOST_ONE_ARE_NOT, Q.positive)])
    assert remove(not_real, not_positive) == [not_positive]
    raises(ValueError, lambda: remove((IF_AND_ONLY_IF, [
        (ONE_ARG_IS, Q.zero), (OTHER_ARGS_BUT_AT_MOST_ONE_ARE, Q.zero)])))
    one_positive = (TRUE_IF, [(ONE_ARG_IS, Q.positive)])
    others_zero = (TRUE_IF, [(ONE_ARG_IS, Q.positive),
                             (OTHER_ARGS_BUT_AT_MOST_ONE_ARE, Q.zero)])
    others_integer = (TRUE_IF, [(ONE_ARG_IS, Q.positive),
                                (OTHER_ARGS_BUT_AT_MOST_ONE_ARE, Q.integer)])
    assert remove(others_zero, one_positive) == [others_zero, one_positive]
    assert remove(others_zero, real) == [others_zero, real]
    # a group with a counting condition is only compared for equality
    assert remove(others_zero, others_integer) == [others_zero, others_integer]
    imaginary = (TRUE_IF, [(ALL_ARGS_BUT_AT_MOST_ONE_ARE, Q.imaginary)])
    assert remove(imaginary, not_positive) == [not_positive]
    assert remove(not_positive, imaginary) == [not_positive]
    # the arguments which have the predicate may be any of them
    all_real = (TRUE_IF, [(ALL_ARGS_ARE, Q.real)])
    one_not_real = (TRUE_IF, [(ONE_ARG_IS_NOT, Q.real)])
    assert remove(real, all_real) == [real, all_real]
    assert remove(real, one_not_real) == [real, one_not_real]
    some_not_real = (TRUE_IF, [(ANY_ARG_IS_NOT, Q.real)])
    assert remove(not_real, some_not_real) == [not_real, some_not_real]


def test_exp_rules_for_powers():
    rules = {
        (exp, Q.positive): [(TRUE_IF, [(FIRST_ARG_IS, Q.real)])],
        (exp, Q.zero): [(FALSE_IF, [(SELF_IS, Q.positive)])],
        (Pow, Q.positive): [(TRUE_IF, [(FIRST_ARG_IS, Q.positive)])],
    }
    assert exp_rules_for_powers(rules) == {
        (exp, Q.positive): [(TRUE_IF, [(FIRST_ARG_IS, Q.real)])],
        (exp, Q.zero): [(FALSE_IF, [(SELF_IS, Q.positive)])],
        (Pow, Q.positive): [
            (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
            (TRUE_IF, [(FIRST_ARG_IS, S.Exp1), (SECOND_ARG_IS, Q.real)]),
        ],
        (Pow, Q.zero): [(FALSE_IF, [(FIRST_ARG_IS, S.Exp1), (SELF_IS, Q.positive)])],
    }


def test_answers_which_only_the_generated_rules_give():
    assert ask_by_rules(Q.nonzero, exp(x), Q.real(x), RULES) is None
    assert ask_by_rules(Q.nonzero, exp(x), Q.real(x), GENERATED_RULES) is True
    assert ask_by_rules(Q.negative, exp(x), Q.real(x), RULES) is None
    assert ask_by_rules(Q.negative, exp(x), Q.real(x), GENERATED_RULES) is False
    assert ask_by_rules(Q.finite, acot(x), Q.nonnegative(x), RULES) is None
    assert ask_by_rules(Q.finite, acot(x), Q.nonnegative(x), GENERATED_RULES) is True


def test_same_answers_as_the_source_rules():
    queries = [
        (Q.positive, Abs(x), Q.positive(x)),
        (Q.zero, Abs(x), ~Q.zero(x)),
        (Q.even, Abs(Abs(x)), Q.even(x)),
        (Q.positive, x**y, Q.positive(x) & Q.real(y)),
        (Q.negative, x**y, Q.negative(x) & Q.odd(y)),
        (Q.real, x**y, Q.negative(x) & Q.rational(y) & ~Q.integer(y)),
        (Q.integer, x**y, Q.zero(y)),
        (Q.positive, exp(x), Q.real(x)),
        (Q.zero, exp(x), Q.real(x)),
        (Q.integer, cos(x), Q.zero(x)),
        (Q.zero, sin(x), Q.zero(x)),
        (Q.transcendental, tan(x), Q.algebraic(x) & ~Q.zero(x)),
        (Q.negative, atan(x), Q.negative(x)),
        (Q.negative, acos(x), True),
        (Q.positive, acot(x), Q.positive(x)),
        (Q.positive, asin(x), Q.negative(x)),
        (Q.algebraic, cot(x), Q.algebraic(x)),
        (Q.real, re(x), Q.finite(x)),
        (Q.real, im(x), Q.complex(x)),
        (Q.positive, factorial(x), Q.integer(x) & Q.nonnegative(x)),
        (Q.finite, sign(x), True),
        (Q.zero, x**y, ~Q.zero(x) & Q.positive(y)),
        (Q.prime, x**y, Q.integer(x) & Q.composite(y)),
    ]
    for predicate, expr, assumptions in queries:
        source = ask_by_rules(predicate, expr, assumptions, RULES)
        assert source is not None
        assert ask_by_rules(predicate, expr, assumptions, GENERATED_RULES) is source
