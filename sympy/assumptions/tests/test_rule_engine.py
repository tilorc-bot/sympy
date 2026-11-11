from __future__ import annotations

from contextlib import contextmanager
from importlib import import_module
from itertools import permutations
from typing import TYPE_CHECKING

from sympy.abc import w, x, y, z
from sympy.assumptions.ask import _ask_single_fact as _ask_single_fact_of_ask
from sympy.assumptions.ask import Q, _extract_all_facts
from sympy.assumptions.ask_generated import get_known_facts_dict
from sympy.assumptions.cnf import CNF
from sympy.assumptions.rule_checks import check_no_cycles
from sympy.assumptions.rule_engine import (ALL_ARGS_ARE, ALL_ARGS_ARE_NOT,
    ALWAYS_FALSE, ALWAYS_TRUE, ANY_ARG_IS, ANY_ARG_IS_NOT, EVEN_NUMBER_OF_ARGS_ARE,
    EVEN_NUMBER_OF_ARGS_ARE_NOT, FALSE_IF, FIRST_ARG_IS, FIRST_ARG_IS_NOT,
    IF_AND_ONLY_IF, ODD_NUMBER_OF_ARGS_ARE, ODD_NUMBER_OF_ARGS_ARE_NOT, ONE_ARG_IS,
    ONE_ARG_IS_NOT, OTHER_ARGS_ARE, OTHER_ARGS_ARE_NOT, SECOND_ARG_IS, SELF_IS,
    SELF_IS_NOT, TRUE_IF, _UnaryFactsEngine, ask_by_rules)
from sympy.core.add import Add
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.core.facts import FactKB
from sympy.core.function import Function
from sympy.core.mul import Mul
from sympy.core.numbers import Integer
from sympy.core.power import Pow
from sympy.core.symbol import Symbol
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.exponential import exp
from sympy.logic.boolalg import And
from sympy.testing.pytest import raises

if TYPE_CHECKING:
    from sympy.assumptions.rule_engine import Rules

RULES: Rules = {
    (Abs, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (Abs, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.even)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.odd)]),
    ],
    (Abs, Q.negative): [
        ALWAYS_FALSE,
    ],
    (Abs, Q.zero): [
        (IF_AND_ONLY_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (Abs, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (exp, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (Pow, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.even)]),
    ],
    (Add, Q.integer): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.integer)]),
    ],
    (Add, Q.positive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonnegative), (ANY_ARG_IS, Q.positive)]),
    ],
    (Add, Q.irrational): [
        (TRUE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
    ],
    (Add, Q.odd): [
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
    ],
    (Add, Q.even): [
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
    ],
    (Mul, Q.positive): [
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
    ],
    (Mul, Q.negative): [
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
    ],
    (Mul, Q.zero): [
        (TRUE_IF, [(ANY_ARG_IS, Q.zero), (ALL_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.zero)]),
    ],
    (Mul, Q.even): [
        (TRUE_IF, [(ANY_ARG_IS, Q.even), (ALL_ARGS_ARE, Q.integer)]),
    ],
    (Expr, Q.real): [
        (TRUE_IF, [(SELF_IS, Q.positive)]),
    ],
    (Expr, Q.zero): [
        (FALSE_IF, [(SELF_IS, Q.positive)]),
    ],
    (Expr, Q.nonnegative): [
        (TRUE_IF, [(SELF_IS, Q.positive)]),
    ],
}


def ask(predicate, expr, assumptions=True):
    return ask_by_rules(predicate, expr, assumptions, RULES)


def test_assumed():
    assert _UnaryFactsEngine(True).assumed == {}
    assert _UnaryFactsEngine(Q.even(x)).assumed == {x: [(Q.even, True)]}
    assumed = _UnaryFactsEngine(~Q.even(x) & Q.real(y) & Q.zero(x)).assumed
    assert set(assumed) == {x, y}
    assert set(assumed[x]) == {(Q.zero, True), (Q.even, False)}
    assert assumed[y] == [(Q.real, True)]
    assert _UnaryFactsEngine(Q.even(x) | Q.odd(x)).assumed == {}
    assert _UnaryFactsEngine(Q.gt(x, y) & Q.real(x)).assumed == {x: [(Q.real, True)]}


def test_ask_single_fact():
    def ask_single_fact(key, assumptions):
        return _UnaryFactsEngine(assumptions).ask_single_fact(key, x)

    assert ask_single_fact(Q.zero, ~Q.zero(x)) is False
    assert ask_single_fact(Q.zero, ~Q.even(x)) is False
    assert ask_single_fact(Q.even, Q.zero(x)) is True
    assert ask_single_fact(Q.even, Q.odd(x)) is False
    assert ask_single_fact(Q.even, Q.integer(x)) is None
    assert ask_single_fact(Q.even, Q.real(x) & Q.zero(x)) is True
    assert ask_single_fact(Q.even, Q.zero(y)) is None
    assert ask_single_fact(Q.even, True) is None


def test_ask_single_fact_agrees_with_the_one_of_ask():
    predicates = sorted(get_known_facts_dict(), key=str)
    for key in predicates:
        for predicate in predicates:
            for value in (True, False):
                assumption = predicate(x) if value else ~predicate(x)
                expected = _ask_single_fact_of_ask(
                    key, _extract_all_facts(CNF.from_prop(assumption), (x,)))
                assert _UnaryFactsEngine(assumption).ask_single_fact(key, x) is expected


def test_rule_about_an_argument():
    assert ask(Q.integer, Abs(x), Q.integer(x)) is True
    assert ask(Q.integer, Abs(x)) is None
    assert ask(Q.even, Abs(x), Q.even(x)) is True
    assert ask(Q.even, Abs(x), Q.integer(x)) is None
    assert ask(Q.even, Abs(x)) is None
    assert ask(Q.odd, Abs(x), Q.even(x)) is None


def test_rule_without_conditions():
    assert ask(Q.negative, Abs(x)) is False
    rules = {(exp, Q.complex): [ALWAYS_TRUE]}
    assert ask_by_rules(Q.complex, exp(x), True, rules) is True


def test_condition_which_must_not_hold():
    assert ask(Q.positive, Abs(x), Q.complex(x) & ~Q.zero(x)) is True
    assert ask(Q.positive, Abs(x), Q.negative(x)) is True
    assert ask(Q.positive, Abs(x), Q.complex(x)) is None
    assert ask(Q.positive, Abs(x), Q.zero(x)) is None
    assert ask(Q.positive, Abs(x), ~Q.zero(x)) is None
    rules = {
        (Expr, Q.positive): [
            (TRUE_IF, [(SELF_IS, Q.nonnegative), (SELF_IS_NOT, Q.zero)]),
        ],
    }
    assert ask_by_rules(Q.positive, x, Q.nonnegative(x) & ~Q.zero(x), rules) is True
    assert ask_by_rules(Q.positive, x, Q.nonnegative(x), rules) is None


def test_if_and_only_if_with_a_condition_which_must_not_hold():
    class g(Function):
        pass

    # not true of anything: only the shape is tested
    rules = {(g, Q.even): [(IF_AND_ONLY_IF, [(FIRST_ARG_IS_NOT, Q.odd)])]}
    assert ask_by_rules(Q.even, g(x), ~Q.odd(x), rules) is True
    assert ask_by_rules(Q.even, g(x), Q.odd(x), rules) is False
    assert ask_by_rules(Q.even, g(x), True, rules) is None


def test_several_rules_for_one_predicate():
    assert ask(Q.even, Abs(x), Q.even(x)) is True
    assert ask(Q.even, Abs(x), Q.odd(x)) is False
    assert ask(Q.positive, x**y, Q.positive(x) & Q.real(y)) is True
    assert ask(Q.positive, x**y, Q.negative(x) & Q.even(y)) is True
    assert ask(Q.positive, x**y, Q.negative(x) & Q.real(y)) is None


def test_if_and_only_if():
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
    assert ask(Q.nonnegative, exp(x), Q.real(x)) is True


SYMBOLS = (x, y, z, w)


def is_not(predicate):
    return lambda symbol: ~predicate(symbol)


def ask_each(predicate, cls, facts, rules=RULES):
    """The answers for every way of giving *facts* to the arguments, one each."""
    symbols = SYMBOLS[:len(facts)]
    expr = cls(*symbols)
    answers = set()
    for order in permutations(facts):
        assumptions = And(*(fact(symbol) for fact, symbol in zip(order, symbols)))
        answers.add(ask_by_rules(predicate, expr, assumptions, rules))
    return answers


def test_all_args_are():
    assert ask_each(Q.integer, Add, [Q.integer]*2) == {True}
    assert ask_each(Q.integer, Add, [Q.integer]*3) == {True}
    assert ask_each(Q.integer, Add, [Q.integer]*4) == {True}
    assert ask_each(Q.integer, Add, [Q.integer]*2 + [Q.real]) == {None}
    assert ask_each(Q.integer, Add, [Q.integer]*3 + [is_not(Q.integer)]) == {None}
    assert ask_each(Q.even, Mul, [Q.even, Q.integer]) == {True}
    assert ask_each(Q.even, Mul, [Q.even, Q.integer, Q.odd, Q.odd]) == {True}
    assert ask_each(Q.even, Mul, [Q.even, Q.integer, Q.real]) == {None}


def test_any_arg_is():
    N, P = Q.nonnegative, Q.positive
    assert ask_each(Q.positive, Add, [P, N]) == {True}
    assert ask_each(Q.positive, Add, [P, N, Q.zero]) == {True}
    assert ask_each(Q.positive, Add, [P, P, N, Q.zero]) == {True}
    assert ask_each(Q.positive, Add, [N, N, N]) == {None}
    assert ask_each(Q.positive, Add, [P, N, Q.real]) == {None}
    assert ask_each(Q.nonnegative, Add, [P, N, N]) == {True}
    assert ask_each(Q.zero, Mul, [Q.zero, Q.finite]) == {True}
    assert ask_each(Q.zero, Mul, [Q.zero, Q.positive, Q.finite]) == {True}
    assert ask_each(Q.zero, Mul, [Q.zero, Q.finite, Q.finite, Q.real]) == {True}
    assert ask_each(Q.zero, Mul, [Q.zero, Q.finite, Q.complex]) == {True}
    assert ask_each(Q.zero, Mul, [Q.zero, Q.extended_real]) == {None}


def test_one_arg_is():
    R, IR = Q.rational, Q.irrational
    assert ask_each(Q.irrational, Add, [IR, R]) == {True}
    assert ask_each(Q.irrational, Add, [IR, R, R]) == {True}
    assert ask_each(Q.irrational, Add, [IR, R, Q.integer, R]) == {True}
    assert ask_each(Q.irrational, Add, [IR, IR, R]) == {None}
    assert ask_each(Q.irrational, Add, [R, R]) == {None}


def test_even_and_odd_number_of_args():
    even, odd = Q.even, Q.odd
    assert ask_each(Q.odd, Add, [odd, even]) == {True}
    assert ask_each(Q.odd, Add, [odd, odd, odd]) == {True}
    assert ask_each(Q.odd, Add, [odd, odd, odd, even]) == {True}
    assert ask_each(Q.odd, Add, [odd, odd, even, even]) == {None}
    assert ask_each(Q.even, Add, [even, even]) == {True}
    assert ask_each(Q.even, Add, [odd, odd, even]) == {True}
    assert ask_each(Q.even, Add, [odd, odd, odd, odd]) == {True}
    assert ask_each(Q.even, Add, [odd, even, even]) == {None}
    assert ask_each(Q.even, Add, [odd, odd, Q.integer]) == {None}
    N, P = Q.negative, Q.positive
    assert ask_each(Q.positive, Mul, [N, N]) == {True}
    assert ask_each(Q.positive, Mul, [N, N, P]) == {True}
    assert ask_each(Q.positive, Mul, [P, P, P, P]) == {True}
    assert ask_each(Q.positive, Mul, [N, N, N, P]) == {None}
    assert ask_each(Q.positive, Mul, [N, N, Q.nonnegative]) == {None}
    assert ask_each(Q.negative, Mul, [N, P]) == {True}
    assert ask_each(Q.negative, Mul, [N, N, N]) == {True}
    assert ask_each(Q.negative, Mul, [N, P, P, P]) == {True}
    assert ask_each(Q.negative, Mul, [N, N, P, P]) == {None}
    assert ask_each(Q.real, Mul, [N, N, P]) == {True}
    assert ask_each(Q.zero, Mul, [N, N, P]) == {False}


def test_counting_with_an_undecided_argument():
    assert ask_each(Q.odd, Add, [Q.odd, Q.integer]) == {None}
    assert ask_each(Q.odd, Add, [Q.odd, Q.even, Q.real]) == {None}
    assert ask_each(Q.irrational, Add, [Q.irrational, Q.rational, Q.real]) == {None}
    assert ask_each(Q.negative, Mul, [Q.negative, Q.positive, Q.real]) == {None}

    class g(Function):
        pass

    # not true of anything: only the shape is tested
    rules = {(g, Q.even): [(IF_AND_ONLY_IF, [(ONE_ARG_IS, Q.zero)])]}
    assert ask_each(Q.even, g, [Q.zero, Q.real], rules) == {None}
    assert ask_each(Q.even, g, [Q.zero, Q.zero, Q.real], rules) == {None}


def test_conditions_which_must_not_hold_for_the_arguments():
    assert ask_each(Q.zero, Mul, [Q.positive, Q.negative]) == {False}
    assert ask_each(Q.zero, Mul, [Q.positive, Q.negative, is_not(Q.zero)]) == {False}
    assert ask_each(Q.zero, Mul, [Q.positive, Q.real]) == {None}

    class g(Function):
        pass

    # not true of anything: only the shape is tested
    rules = {
        (g, Q.zero): [(IF_AND_ONLY_IF, [(ALL_ARGS_ARE_NOT, Q.zero)])],
        (g, Q.even): [(IF_AND_ONLY_IF, [(ANY_ARG_IS_NOT, Q.odd)])],
        (g, Q.odd): [(IF_AND_ONLY_IF, [(ONE_ARG_IS_NOT, Q.zero)])],
        (g, Q.prime): [(IF_AND_ONLY_IF, [(EVEN_NUMBER_OF_ARGS_ARE_NOT, Q.zero)])],
        (g, Q.composite): [(IF_AND_ONLY_IF, [(ODD_NUMBER_OF_ARGS_ARE_NOT, Q.zero)])],
        (g, Q.positive): [
            (IF_AND_ONLY_IF, [(ONE_ARG_IS, Q.zero), (OTHER_ARGS_ARE_NOT, Q.negative)]),
        ],
    }
    Z, NZ = Q.zero, is_not(Q.zero)
    assert ask_each(Q.zero, g, [NZ, NZ, NZ], rules) == {True}
    assert ask_each(Q.zero, g, [NZ, Z, NZ], rules) == {False}
    assert ask_each(Q.zero, g, [NZ, Q.real], rules) == {None}
    assert ask_each(Q.even, g, [Q.odd, is_not(Q.odd)], rules) == {True}
    assert ask_each(Q.even, g, [Q.odd, Q.odd, Q.odd], rules) == {False}
    assert ask_each(Q.even, g, [Q.odd, Q.real], rules) == {None}
    assert ask_each(Q.odd, g, [Z, NZ, Z], rules) == {True}
    assert ask_each(Q.odd, g, [Z, NZ, NZ], rules) == {False}
    assert ask_each(Q.odd, g, [Z, Z, Z, Z], rules) == {False}
    assert ask_each(Q.prime, g, [Z, NZ, NZ, Z], rules) == {True}
    assert ask_each(Q.prime, g, [Z, Z, Z], rules) == {True}
    assert ask_each(Q.prime, g, [Z, NZ, Z], rules) == {False}
    assert ask_each(Q.composite, g, [Z, NZ, Z], rules) == {True}
    assert ask_each(Q.composite, g, [NZ, NZ, NZ, Z], rules) == {True}
    assert ask_each(Q.composite, g, [NZ, NZ], rules) == {False}
    P = Q.positive
    assert ask_each(Q.positive, g, [Z, P], rules) == {True}
    assert ask_each(Q.positive, g, [Z, P, P, P], rules) == {True}
    assert ask_each(Q.positive, g, [Z, P, Q.negative], rules) == {False}
    assert ask_each(Q.positive, g, [Z, P, P, Q.nonzero], rules) == {None}


def test_if_and_only_if_with_a_condition_about_the_arguments():
    class g(Function):
        pass

    # not true of anything: only the shape is tested
    rules = {
        (g, Q.even): [(IF_AND_ONLY_IF, [(ALL_ARGS_ARE, Q.even)])],
        (g, Q.odd): [(IF_AND_ONLY_IF, [(ANY_ARG_IS, Q.odd)])],
        (g, Q.zero): [(IF_AND_ONLY_IF, [(ONE_ARG_IS, Q.zero)])],
        (g, Q.positive): [
            (IF_AND_ONLY_IF, [
                (EVEN_NUMBER_OF_ARGS_ARE, Q.zero),
                (OTHER_ARGS_ARE, Q.odd),
            ]),
        ],
    }
    even, odd = Q.even, Q.odd
    assert ask_each(Q.even, g, [even, even, even], rules) == {True}
    assert ask_each(Q.even, g, [even, odd, even], rules) == {False}
    assert ask_each(Q.even, g, [even, Q.integer, odd], rules) == {False}
    assert ask_each(Q.even, g, [even, Q.integer], rules) == {None}
    assert ask_each(Q.odd, g, [even, odd, Q.real], rules) == {True}
    assert ask_each(Q.odd, g, [even, even, even, even], rules) == {False}
    assert ask_each(Q.odd, g, [even, even, Q.integer], rules) == {None}
    assert ask_each(Q.zero, g, [Q.zero, Q.positive], rules) == {True}
    assert ask_each(Q.zero, g, [Q.zero, Q.zero], rules) == {False}
    assert ask_each(Q.zero, g, [Q.positive, Q.positive], rules) == {False}
    assert ask_each(Q.zero, g, [Q.zero, Q.real], rules) == {None}
    assert ask_each(Q.positive, g, [Q.zero, Q.zero, odd], rules) == {True}
    def nonzero_even(symbol):
        return Q.even(symbol) & ~Q.zero(symbol)

    assert ask_each(Q.positive, g, [Q.zero, Q.zero, nonzero_even], rules) == {False}
    assert ask_each(Q.positive, g, [Q.zero, Q.zero, even], rules) == {None}
    assert ask_each(Q.positive, g, [Q.zero, Q.zero, Q.integer], rules) == {None}
    assert ask_each(Q.positive, g, [Q.zero, odd], rules) == {False}


def test_several_other_args_conditions():
    rules = {
        (Add, Q.odd): [
            (TRUE_IF, [
                (ONE_ARG_IS, Q.odd),
                (OTHER_ARGS_ARE, Q.integer),
                (OTHER_ARGS_ARE_NOT, Q.odd),
            ]),
        ],
    }
    def E(symbol):
        return Q.integer(symbol) & ~Q.odd(symbol)

    assert ask_each(Q.odd, Add, [Q.odd, E], rules) == {True}
    assert ask_each(Q.odd, Add, [Q.odd, E, E], rules) == {True}
    assert ask_each(Q.odd, Add, [Q.odd, E, E, E], rules) == {True}
    assert ask_each(Q.odd, Add, [Q.odd, E, is_not(Q.odd)], rules) == {None}

    class g(Function):
        pass

    # not true of anything: only the shape is tested
    rules = {
        (g, Q.even): [
            (IF_AND_ONLY_IF, [
                (ONE_ARG_IS, Q.zero),
                (OTHER_ARGS_ARE, Q.positive),
                (ONE_ARG_IS, Q.odd),
                (OTHER_ARGS_ARE, Q.zero),
            ]),
        ],
    }
    expr = g(x, y)
    assert ask_by_rules(Q.even, expr, Q.zero(x) & Q.positive(y) & Q.odd(y),
        rules) is True
    assert ask_by_rules(Q.even, expr, Q.zero(x) & Q.prime(y), rules) is None
    assert ask_by_rules(Q.even, expr, Q.zero(x) & Q.negative(y), rules) is False


def test_other_args_need_a_counting_condition_before_them():
    rules = {(Add, Q.even): [(TRUE_IF, [(OTHER_ARGS_ARE, Q.even)])]}
    raises(ValueError, lambda: ask_by_rules(Q.even, x + y, True, rules))
    rules = {
        (Add, Q.even): [(TRUE_IF, [(ALL_ARGS_ARE, Q.even), (OTHER_ARGS_ARE, Q.even)])],
    }
    assumptions = Q.even(x) & Q.even(y)
    raises(ValueError, lambda: ask_by_rules(Q.even, x + y, assumptions, rules))


def test_conditions_about_the_arguments_of_an_expression_without_any():
    class g(Function):
        pass

    # not true of anything: only the shape is tested
    selectors = [ALL_ARGS_ARE, ALL_ARGS_ARE_NOT, ANY_ARG_IS, ANY_ARG_IS_NOT,
        ONE_ARG_IS, ONE_ARG_IS_NOT, EVEN_NUMBER_OF_ARGS_ARE,
        EVEN_NUMBER_OF_ARGS_ARE_NOT, ODD_NUMBER_OF_ARGS_ARE,
        ODD_NUMBER_OF_ARGS_ARE_NOT]
    for selector in selectors:
        for kind in (TRUE_IF, FALSE_IF, IF_AND_ONLY_IF):
            rules = {(g, Q.even): [(kind, [(selector, Q.even)])]}
            assert ask_by_rules(Q.even, g(), True, rules) is None
    rules = {
        (g, Q.even): [
            (IF_AND_ONLY_IF, [(ONE_ARG_IS, Q.even), (OTHER_ARGS_ARE, Q.even)]),
        ],
    }
    assert ask_by_rules(Q.even, g(), True, rules) is None


def test_check_no_cycles():
    check_no_cycles(RULES)
    loop = {
        (Expr, Q.nonnegative): [(TRUE_IF, [(SELF_IS, Q.positive)])],
        (Expr, Q.positive): [(TRUE_IF, [(SELF_IS, Q.nonnegative), (SELF_IS, Q.nonzero)])],
    }
    error = raises(ValueError, lambda: check_no_cycles(loop))
    assert 'Q.nonnegative, Q.positive' in str(error.value)
    raises(ValueError, lambda: check_no_cycles(
        {(Abs, Q.even): [(TRUE_IF, [(SELF_IS, Q.even)])]}))
    raises(ValueError, lambda: check_no_cycles({
        (Abs, Q.nonnegative): [(TRUE_IF, [(SELF_IS, Q.positive)])],
        (Expr, Q.positive): [(TRUE_IF, [(SELF_IS, Q.nonnegative)])],
    }))
    check_no_cycles({(Abs, Q.even): [(TRUE_IF, [(FIRST_ARG_IS, Q.even)])]})


def _subclasses(cls, seen):
    for subclass in cls.__subclasses__():
        if subclass not in seen:
            seen.add(subclass)
            _subclasses(subclass, seen)
    return seen


@contextmanager
def old_assumptions_forbidden():
    """
    Inside it, every ``is_<fact>`` attribute of the old assumptions, the
    function which runs the ``_eval_is_`` handlers, and
    ``FactKB.deduce_all_facts`` raise.
    """
    def forbidden(*args):
        raise AssertionError('the old assumptions were used')

    # sympy.core.assumptions is also the name of a function
    core_assumptions = import_module('sympy.core.assumptions')
    names = ['is_' + fact for fact in core_assumptions._assume_defined]
    attributes = [(cls, name, vars(cls)[name])
                  for cls in _subclasses(Basic, {Basic})
                  for name in names if name in vars(cls)]
    functions = core_assumptions._ask, FactKB.deduce_all_facts
    for cls, name, _ in attributes:
        setattr(cls, name, property(forbidden))
    core_assumptions._ask = FactKB.deduce_all_facts = forbidden
    try:
        yield
    finally:
        for cls, name, value in attributes:
            setattr(cls, name, value)
        core_assumptions._ask, FactKB.deduce_all_facts = functions


def test_old_assumptions_forbidden():
    p = Symbol('p', positive=True)
    q = Symbol('q', real=True)
    three = Integer(3)
    with old_assumptions_forbidden():
        raises(AssertionError, lambda: p.is_positive)
        raises(AssertionError, lambda: (q + 1).is_real)
        raises(AssertionError, lambda: three.is_odd)
        raises(AssertionError, lambda: x.is_commutative)
    assert p.is_positive is True
    assert (q + 1).is_real is True
    assert three.is_odd is True
    assert x.is_commutative is True


def test_old_assumptions_are_not_used():
    p = Symbol('p', positive=True)
    queries = [
        (Q.positive, exp(x)**y, Q.real(x) & Q.real(y), True),
        (Q.even, Abs(Abs(x)), Q.even(x), True),
        (Q.zero, Abs(x), ~Q.zero(x), False),
        (Q.positive, x, True, None),
        (Q.positive, p, True, None),
        (Q.zero, Abs(p), True, None),
        (Q.positive, x + y + z, Q.positive(x) & Q.positive(y) & Q.positive(z), True),
        (Q.odd, x + y + p, Q.odd(x) & Q.odd(y) & Q.odd(p), True),
        (Q.zero, x*p, Q.positive(x), None),
    ]
    with old_assumptions_forbidden():
        for predicate, expr, assumptions, expected in queries:
            assert ask(predicate, expr, assumptions) is expected
