from __future__ import annotations

from contextlib import contextmanager
from importlib import import_module
from itertools import permutations
from typing import TYPE_CHECKING

from sympy.abc import w, x, y, z
from sympy.assumptions.ask import _ask_single_fact as _ask_single_fact_of_ask
from sympy.assumptions.ask import Q, _extract_all_facts
from sympy.assumptions.ask import ask as sympy_ask
from sympy.assumptions.ask_generated import (get_known_facts_dict,
    get_number_facts_combinations)
from sympy.assumptions.cnf import CNF
from sympy.assumptions.number_facts import number_facts
from sympy.assumptions.rule_checks import check_no_cycles
from sympy.assumptions.rule_engine import (ALL_ARGS_ARE, ALL_ARGS_ARE_NOT,
    ALWAYS_FALSE, ALWAYS_TRUE, ANY_ARG_IS, ANY_ARG_IS_NOT, EVEN_NUMBER_OF_ARGS_ARE,
    EVEN_NUMBER_OF_ARGS_ARE_NOT, FALSE_IF, FIRST_ARG_IS, FIRST_ARG_IS_NOT,
    IF_AND_ONLY_IF, ODD_NUMBER_OF_ARGS_ARE, ODD_NUMBER_OF_ARGS_ARE_NOT, ONE_ARG_IS,
    ONE_ARG_IS_NOT, OTHER_ARGS_ARE, OTHER_ARGS_ARE_NOT, SECOND_ARG_IS, SELF_IS,
    SELF_IS_NOT, TRUE_IF, _UnaryFactsEngine, ask_by_rules)
from sympy.assumptions.rule_preprocessing import preprocess
from sympy.core.add import Add
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.core.facts import FactKB
from sympy.core.function import Function
from sympy.core.mul import Mul
from sympy.core.numbers import E, Float, I, Integer, Rational, nan, oo, pi, zoo
from sympy.core.power import Pow
from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.exponential import LambertW, exp, log
from sympy.functions.elementary.hyperbolic import (acosh, acoth, acsch, asech,
    asinh, atanh, cosh, coth, csch, sech, sinh, tanh)
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.functions.elementary.trigonometric import (acos, acot, acsc, asec, asin,
    atan, cos, csc, sec, sin, tan)
from sympy.functions.special.error_functions import erf
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


def test_preprocess():
    assert preprocess(x, True) == {}
    assert preprocess(x, Q.even(x)) == {x: [(Q.even, True)]}
    known = preprocess(x, ~Q.even(x) & Q.real(y) & Q.zero(x))
    assert set(known) == {x, y}
    assert set(known[x]) == {(Q.zero, True), (Q.even, False)}
    assert known[y] == [(Q.real, True)]
    assert preprocess(x, Q.even(x) | Q.odd(x)) == {}
    assert preprocess(x, Q.gt(x, y) & Q.real(x)) == {x: [(Q.real, True)]}


def test_preprocess_numbers():
    three = Integer(3)
    facts = [(Q.positive, True), (Q.odd, True), (Q.antihermitian, False),
             (Q.prime, True)]
    assert preprocess(three, True) == {three: facts}
    assert preprocess(x + 3*y, True) == {three: facts}
    assert preprocess(three, Q.finite(three)) == {three: facts + [(Q.finite, True)]}
    assert preprocess(pi, True) == preprocess(exp(pi*x) + pi, True) == {
        pi: [(Q.positive, True), (Q.irrational, True), (Q.transcendental, True),
             (Q.antihermitian, False)]}


def test_numbers_without_symbols():
    def ask_number(predicate, number, assumptions=True):
        with old_assumptions_forbidden():
            return ask(predicate, number, assumptions)

    def known(expr):
        with old_assumptions_forbidden():
            return preprocess(expr, True)

    positive = [(Q.positive, True), (Q.antihermitian, False)]
    assert ask_number(Q.positive, sqrt(2) - 1) is True
    assert ask_number(Q.negative, 1 - sqrt(2)) is True
    assert ask_number(Q.negative, (1 - sqrt(5))**3) is True
    assert ask_number(Q.real, I**I) is True
    # imaginary
    assert ask_number(Q.imaginary, I*(sqrt(2) - 1)) is True
    assert ask_number(Q.hermitian, I*(sqrt(2) - 1)) is False
    # neither real nor imaginary
    assert ask_number(Q.real, I*(1 + I)) is False
    assert ask_number(Q.imaginary, I*(1 + I)) is False
    assert ask_number(Q.antihermitian, I*(1 + I)) is False
    assert ask_number(Q.imaginary, log(2) + I*pi/2) is False
    assert ask_number(Q.extended_positive, log(2) + I*pi/2) is False
    assert ask_number(Q.real, tan(1 + I)) is False
    # not real, the real part is not decided
    assert ask_number(Q.real, sqrt(sqrt(2) - 2)) is False
    assert ask_number(Q.imaginary, sqrt(sqrt(2) - 2)) is None
    # not imaginary, the imaginary part is not decided
    assert ask_number(Q.imaginary, 2 + I*(cos(1)**2 + sin(1)**2 - 1)) is False
    assert ask_number(Q.zero, 2 + I*(cos(1)**2 + sin(1)**2 - 1)) is False
    assert ask_number(Q.real, 2 + I*(cos(1)**2 + sin(1)**2 - 1)) is None
    # zero, which intervals do not decide
    assert cos(1)**2 + sin(1)**2 - 1 not in known(cos(1)**2 + sin(1)**2 - 1)
    # functions which are not evaluated, and numbers which are too large
    assert erf(Rational(1, 7)) not in known(erf(Rational(1, 7)))
    assert exp(10**10) not in known(exp(10**10))
    assert Pow(2, 10**9, evaluate=False) not in known(Pow(2, 10**9, evaluate=False))
    # in an expression with symbols
    assert ask_number(Q.positive, x + I**I, Q.positive(x)) is True
    assert known(x*(sqrt(2) - 1))[sqrt(2) - 1] == positive
    # only the largest number gets an entry
    assert sqrt(2) not in known(sqrt(2) - 1)
    assert known(sqrt(2) - 1)[sqrt(2) - 1] == positive
    assert known(erf(Rational(1, 7)) + sqrt(2))[sqrt(2)] == positive


def test_exact_numbers_without_symbols():
    def ask_number(predicate, number):
        with old_assumptions_forbidden():
            return ask(predicate, number)

    def known(expr):
        with old_assumptions_forbidden():
            return preprocess(expr, True)

    half = Rational(1, 2)
    # rational numbers
    assert ask_number(Q.integer, Pow(half, 3, evaluate=False)) is False
    assert ask_number(Q.rational, Pow(3, -2, evaluate=False)) is True
    assert ask_number(Q.even, Pow(half, -2, evaluate=False)) is True
    assert ask_number(Q.prime, Pow(4, half, evaluate=False)) is True
    assert ask_number(Q.positive, Pow(Rational(1, 8), Rational(-2, 3), evaluate=False)) is True
    assert ask_number(Q.integer, Pow(Rational(1, 8), Rational(-2, 3), evaluate=False)) is True
    assert ask_number(Q.zero, Add(-1, 1, evaluate=False)) is True
    assert ask_number(Q.zero, Pow(0, half, evaluate=False)) is True
    assert ask_number(Q.odd, Pow(0, 0, evaluate=False)) is True
    assert ask_number(Q.even, Pow(2, 512, evaluate=False)) is True
    assert ask_number(Q.even, Pow(2, 600, evaluate=False)) is None
    assert ask_number(Q.positive, Pow(2, 600, evaluate=False)) is True
    # roots which are not rational, and the root of a negative number
    assert ask_number(Q.integer, Pow(8, half, evaluate=False)) is None
    assert ask_number(Q.real, Pow(-8, Rational(1, 3), evaluate=False)) is False
    # values at 0 and at multiples of pi/2
    assert ask_number(Q.zero, sin(Add(-1, 1, evaluate=False))) is True
    assert ask_number(Q.zero, acosh(1, evaluate=False)) is True
    assert ask_number(Q.zero, cos(5*pi/2, evaluate=False)) is True
    assert ask_number(Q.zero, cosh(5*I*pi/2, evaluate=False)) is True
    assert ask_number(Q.zero, sinh(2*I*pi, evaluate=False)) is True
    assert ask_number(Q.odd, exp(-I*pi, evaluate=False)) is True
    assert tan(pi/2, evaluate=False) not in known(tan(pi/2, evaluate=False))
    assert ask_number(Q.algebraic, exp(I*pi/3)) is True
    assert ask_number(Q.algebraic, cos(2*pi/7)) is True
    assert ask_number(Q.algebraic, sinh(pi/7)) is None


def test_powers_with_infinities():
    def ask_number(predicate, number):
        with old_assumptions_forbidden():
            return ask(predicate, number)

    def known(expr):
        with old_assumptions_forbidden():
            return preprocess(expr, True)

    half = Rational(1, 2)
    assert ask_number(Q.infinite, Pow(2, oo, evaluate=False)) is True
    assert ask_number(Q.zero, Pow(half, oo, evaluate=False)) is True
    assert ask_number(Q.zero, Pow(2, -oo, evaluate=False)) is True
    assert ask_number(Q.infinite, Pow(half, -oo, evaluate=False)) is True
    assert ask_number(Q.infinite, Pow(oo, oo, evaluate=False)) is True
    assert ask_number(Q.zero, Pow(oo, -oo, evaluate=False)) is True
    assert ask_number(Q.infinite, Pow(oo, 1 + I, evaluate=False)) is True
    assert ask_number(Q.zero, Pow(oo, -half, evaluate=False)) is True
    assert ask_number(Q.zero, Pow(0, oo, evaluate=False)) is True
    assert ask_number(Q.infinite, Pow(0, -oo, evaluate=False)) is True
    assert ask_number(Q.infinite, Pow(0, -sqrt(2), evaluate=False)) is True
    # a base which is not real, by its absolute value
    assert ask_number(Q.infinite, (2*I)**oo) is True
    assert ask_number(Q.zero, (2*I)**-oo) is True
    assert ask_number(Q.infinite, (-2*I)**oo) is True
    assert ask_number(Q.zero, (I/2)**oo) is True
    assert ask_number(Q.infinite, (-I/2)**-oo) is True
    assert ask_number(Q.infinite, (1 + I)**oo) is True
    assert ask_number(Q.zero, (1 + I)**-oo) is True
    assert I**oo not in known(I**oo)
    # nan in SymPy
    one_to_oo = Pow(1, oo, evaluate=False)
    assert one_to_oo not in known(one_to_oo)
    oo_to_imaginary = Pow(oo, I/2, evaluate=False)
    assert oo_to_imaginary not in known(oo_to_imaginary)
    zero_to_complex = Pow(0, 1 + I, evaluate=False)
    assert zero_to_complex not in known(zero_to_complex)
    negative_to_minus_oo = Pow(-half, -oo, evaluate=False)
    assert negative_to_minus_oo not in known(negative_to_minus_oo)
    minus_oo_to_oo = Pow(-oo, oo, evaluate=False)
    assert minus_oo_to_oo not in known(minus_oo_to_oo)
    # zoo in SymPy, which is not consistent for negative bases
    minus_two_to_oo = Pow(-2, oo, evaluate=False)
    assert minus_two_to_oo not in known(minus_two_to_oo)
    # 0 in SymPy
    zoo_to_oo = Pow(zoo, oo, evaluate=False)
    assert zoo_to_oo not in known(zoo_to_oo)


def test_functions_of_numbers_without_symbols():
    def ask_number(predicate, number):
        with old_assumptions_forbidden():
            return ask(predicate, number)

    def known(expr):
        with old_assumptions_forbidden():
            return preprocess(expr, True)

    half = Rational(1, 2)
    # sec, csc and the hyperbolic functions
    assert ask_number(Q.positive, sec(1)) is True
    assert ask_number(Q.negative, sec(2)) is True
    assert ask_number(Q.negative, csc(-1)) is True
    assert ask_number(Q.negative, sinh(-2)) is True
    assert ask_number(Q.positive, cosh(2)) is True
    assert ask_number(Q.negative, cosh(2*I, evaluate=False)) is True
    assert ask_number(Q.real, cosh(1 + 2*I)) is False
    assert ask_number(Q.real, tanh(1 + I*pi/3)) is False
    assert ask_number(Q.positive, coth(half)) is True
    assert ask_number(Q.positive, sech(3)) is True
    assert ask_number(Q.negative, csch(-3)) is True
    # poles
    assert sec(pi/2, evaluate=False) not in known(sec(pi/2, evaluate=False))
    assert csc(0, evaluate=False) not in known(csc(0, evaluate=False))
    # inverse functions, inside and outside the real interval where they are real
    assert ask_number(Q.positive, asin(Rational(1, 7))) is True
    assert ask_number(Q.positive, asin(1, evaluate=False)) is True
    assert ask_number(Q.real, asin(3)) is False
    assert ask_number(Q.real, -asin(-3)) is False
    assert ask_number(Q.positive, acos(Rational(-1, 7))) is True
    assert ask_number(Q.imaginary, acos(Rational(3, 2))) is True
    assert ask_number(Q.real, acos(-2)) is False
    assert ask_number(Q.positive, atan(10**10)) is True
    assert ask_number(Q.negative, acot(-3)) is True
    assert acot(0, evaluate=False) not in known(acot(0, evaluate=False))
    assert ask_number(Q.positive, asec(3)) is True
    assert ask_number(Q.imaginary, asec(half)) is True
    assert ask_number(Q.negative, acsc(-3)) is True
    assert ask_number(Q.real, acsc(half)) is False
    assert ask_number(Q.negative, asinh(-2)) is True
    assert ask_number(Q.positive, acosh(2)) is True
    assert ask_number(Q.imaginary, acosh(Rational(1, 5))) is True
    assert ask_number(Q.real, acosh(-2)) is False
    assert ask_number(Q.positive, atanh(Rational(1, 5))) is True
    assert ask_number(Q.real, atanh(2)) is False
    assert atanh(1, evaluate=False) not in known(atanh(1, evaluate=False))
    assert ask_number(Q.positive, acoth(2)) is True
    assert ask_number(Q.real, acoth(half)) is False
    assert ask_number(Q.positive, asech(Rational(2, 3))) is True
    assert ask_number(Q.real, asech(Rational(-1, 3))) is False
    assert ask_number(Q.negative, acsch(-2)) is True
    # an interval across the end of the domain, and a complex argument
    above_one = Float('1.000000000000000000001', 30)
    assert asin(above_one, evaluate=False) not in known(asin(above_one, evaluate=False))
    assert ask_number(Q.positive, acosh(above_one, evaluate=False)) is None
    assert asin(1 + I) not in known(asin(1 + I))
    # LambertW, by its branch and by the side of -1/e and 0 of its argument
    assert ask_number(Q.real, LambertW(-1)) is False
    assert ask_number(Q.positive, LambertW(-1)) is False
    assert ask_number(Q.positive, LambertW(2)) is True
    assert ask_number(Q.negative, LambertW(Rational(-1, 10))) is True
    assert ask_number(Q.negative, LambertW(Rational(-1, 10), -1)) is True
    assert ask_number(Q.real, LambertW(Rational(-1, 10), 1)) is False
    assert ask_number(Q.real, LambertW(-10, -1)) is False
    assert ask_number(Q.real, LambertW(-2, 2)) is False
    assert ask_number(Q.real, LambertW(half, -1)) is False
    at_minus_one_over_e = LambertW(-exp(-1), -1, evaluate=False)
    assert at_minus_one_over_e not in known(at_minus_one_over_e)
    assert LambertW(I) not in known(LambertW(I))


def test_preprocess_declared_symbols():
    p = Symbol('p', positive=True)
    n = Symbol('n', integer=True, nonzero=True)
    c = Symbol('c', commutative=False)
    # only what was declared, not what follows from it
    assert preprocess(p, True) == {p: [(Q.positive, True)]}
    assert preprocess(Abs(p) + x, True) == {p: [(Q.positive, True)]}
    assert set(preprocess(n, True)[n]) == {(Q.integer, True), (Q.nonzero, True)}
    assert preprocess(c, True) == {c: [(Q.commutative, False)]}
    assert preprocess(p, Q.even(p)) == {p: [(Q.positive, True), (Q.even, True)]}
    assert preprocess(x, Q.even(p)) == {p: [(Q.even, True)]}


def test_ask_single_fact():
    def ask_single_fact(key, assumptions):
        return _UnaryFactsEngine(preprocess(x, assumptions)).ask_single_fact(key, x)

    assert ask_single_fact(Q.zero, ~Q.zero(x)) is False
    assert ask_single_fact(Q.zero, ~Q.even(x)) is False
    assert ask_single_fact(Q.even, Q.zero(x)) is True
    assert ask_single_fact(Q.even, Q.odd(x)) is False
    assert ask_single_fact(Q.even, Q.integer(x)) is None
    assert ask_single_fact(Q.even, Q.real(x) & Q.zero(x)) is True
    assert ask_single_fact(Q.even, Q.zero(y)) is None
    assert ask_single_fact(Q.even, True) is None


def test_ask_single_fact_agrees_with_the_one_of_ask():
    predicates = sorted(get_number_facts_combinations(), key=str)
    for key in predicates:
        for predicate in predicates:
            for value in (True, False):
                assumption = predicate(x) if value else ~predicate(x)
                expected = _ask_single_fact_of_ask(
                    key, _extract_all_facts(CNF.from_prop(assumption), (x,)))
                engine = _UnaryFactsEngine(preprocess(x, assumption))
                assert engine.ask_single_fact(key, x) is expected


def test_ask_single_fact_from_several_facts():
    r = Symbol('r', real=True, nonnegative=False)
    power = y**x
    with old_assumptions_forbidden():
        assert ask_by_rules(Q.negative, r, True, {}) is True
        assert ask_by_rules(Q.zero, x, Q.nonnegative(x) & Q.nonpositive(x), {}) is True
        assert ask_by_rules(Q.irrational, x, Q.real(x) & ~Q.rational(x), {}) is True
        assert ask_by_rules(Q.infinite, x, Q.extended_real(x) & ~Q.finite(x), {}) is True
        assert ask_by_rules(Q.irrational, x, Q.real(x) & Q.transcendental(x), {}) is True
        assert ask_by_rules(Q.composite, x,
                            Q.positive(x) & Q.even(x) & ~Q.prime(x), {}) is True
        assert ask_by_rules(Q.infinite, x, ~Q.finite(x), {}) is None
        assert ask_by_rules(Q.negative, x, ~Q.nonnegative(x), {}) is None
        assert ask_number_rules(Q.odd, power,
            Q.nonnegative(x) & Q.nonpositive(x) & Q.eq(y, -1)) is True


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


NUMBER_RULES: Rules = {
    (Pow, Q.odd): [
        (TRUE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
    ],
    (log, Q.zero): [
        (IF_AND_ONLY_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (Expr, S.One): [
        (FALSE_IF, [(SELF_IS, Q.prime)]),
    ],
}


def ask_number_rules(predicate, expr, assumptions=True):
    return ask_by_rules(predicate, expr, assumptions, NUMBER_RULES)


def test_condition_about_a_number():
    assert ask_number_rules(Q.odd, (-1)**x, Q.integer(x)) is True
    assert ask_number_rules(Q.odd, (-1)**x) is None
    assert ask_number_rules(Q.odd, (-3)**x, Q.integer(x)) is None
    assert ask_number_rules(Q.odd, y**x, Q.integer(x)) is None
    assert ask_number_rules(Q.zero, log(1, evaluate=False)) is True
    assert ask_number_rules(Q.zero, log(x)) is None
    # by the rule for S.One
    assert ask_number_rules(Q.zero, log(x), Q.prime(x)) is False
    assert ask_number_rules(Q.zero, log(x), Q.composite(x)) is None


def test_a_number_is_itself():
    # ask_single_fact looks at a number only if something is known of it
    assert ask_by_rules(S.One, S.One, True, {}) is True
    assert ask_by_rules(S.NegativeOne, S.NegativeOne, True, {}) is True
    assert ask_by_rules(S.Half, S.Half, True, {}) is True
    assert ask_by_rules(I, I, True, {}) is True
    assert ask_by_rules(S.One, S.NegativeOne, True, {}) is None
    assert ask_by_rules(S.One, x, True, {}) is None


def test_assumed_equal_to_a_number():
    assert preprocess(x, Q.eq(x, 2)) == {x: [(Integer(2), True), *number_facts(Integer(2))]}
    assert preprocess(x, Q.ne(x, 2)) == {x: [(Integer(2), False)]}
    assert preprocess(x, ~Q.eq(x, I)) == {x: [(I, False)]}
    assert preprocess(x, Q.eq(x, y) & Q.eq(x, pi) & Q.gt(x, 1)) == {}
    assert ask_number_rules(Q.zero, log(x), Q.eq(x, 1)) is True
    assert ask_number_rules(Q.zero, log(x), ~Q.ne(x, 1)) is True
    assert ask_number_rules(Q.zero, log(x), Q.ne(x, 1)) is False
    assert ask_number_rules(Q.zero, log(x), ~Q.eq(x, 1)) is False
    assert ask_number_rules(Q.zero, log(x), Q.ne(x, 2)) is None
    assert ask_number_rules(Q.zero, log(x), Q.eq(x, 2)) is False
    assert ask_number_rules(Q.odd, y**x, Q.integer(x) & Q.eq(y, -1)) is True
    assert ask_number_rules(Q.positive, x, Q.eq(x, 2)) is True
    assert ask_number_rules(Q.prime, x, Q.eq(x, 1)) is False


def test_assumption_about_a_number_is_not_kept():
    facts = list(number_facts(pi))
    assert preprocess(pi, Q.negative(pi))[pi] == facts + [(Q.negative, True)]
    assert number_facts(pi) == facts


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

    # its first call imports modules, and a new class uses the old assumptions
    get_known_facts_dict()
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
    queries = [
        (Q.positive, exp(x)**y, Q.real(x) & Q.real(y), True),
        (Q.even, Abs(Abs(x)), Q.even(x), True),
        (Q.zero, Abs(x), ~Q.zero(x), False),
        (Q.positive, x, True, None),
        (Q.positive, x + y + z, Q.positive(x) & Q.positive(y) & Q.positive(z), True),
        (Q.odd, x + y + z, Q.odd(x) & Q.odd(y) & Q.odd(z), True),
        (Q.zero, x*y, Q.positive(x), None),
    ]
    with old_assumptions_forbidden():
        for predicate, expr, assumptions, expected in queries:
            assert ask(predicate, expr, assumptions) is expected



NUMBERS = [
    (Q.positive, Integer(3), True),
    (Q.even, Integer(3), False),
    (Q.real, Integer(3), True),
    (Q.prime, Integer(7), True),
    (Q.composite, Integer(9), True),
    (Q.prime, Integer(9), False),
    (Q.prime, Integer(1), False),
    (Q.composite, Integer(1), False),
    (Q.zero, Integer(0), True),
    (Q.even, Integer(0), True),
    (Q.positive, Integer(0), False),
    (Q.antihermitian, Integer(0), True),
    (Q.negative, Integer(-2), True),
    (Q.prime, Integer(-2), False),
    (Q.rational, Rational(1, 2), True),
    (Q.integer, Rational(1, 2), False),
    (Q.even, Rational(1, 2), False),
    (Q.negative, Rational(-1, 2), True),
    (Q.positive, Float(2.5), True),
    (Q.integer, Float(2.5), False),
    (Q.integer, Float(2.0), None),
    (Q.rational, Float(2.5), None),
    (Q.zero, Float(0.0), True),
    (Q.irrational, pi, True),
    (Q.algebraic, pi, False),
    (Q.transcendental, E, True),
    (Q.algebraic, S.GoldenRatio, True),
    (Q.irrational, S.GoldenRatio, True),
    (Q.positive, S.EulerGamma, True),
    (Q.rational, S.EulerGamma, None),
    (Q.imaginary, I, True),
    (Q.real, I, False),
    (Q.algebraic, I, True),
    (Q.positive_infinite, oo, True),
    (Q.extended_real, oo, True),
    (Q.real, oo, False),
    (Q.finite, oo, False),
    (Q.negative_infinite, -oo, True),
    (Q.infinite, zoo, True),
    (Q.extended_real, zoo, False),
    (Q.real, nan, None),
    (Q.positive, x, None),
    (Q.hermitian, Integer(3), True),
    (Q.antihermitian, Integer(3), False),
    (Q.antihermitian, Integer(-2), False),
    (Q.hermitian, Integer(0), True),
    (Q.antihermitian, Rational(1, 2), False),
    (Q.antihermitian, Float(2.5), False),
    (Q.antihermitian, pi, False),
    (Q.antihermitian, S.EulerGamma, False),
    (Q.hermitian, I, False),
    (Q.antihermitian, I, True),
    (Q.hermitian, oo, False),
    (Q.antihermitian, oo, False),
    (Q.hermitian, -oo, False),
    (Q.antihermitian, -oo, False),
    (Q.hermitian, zoo, False),
    (Q.antihermitian, zoo, False),
]


def test_number_facts():
    assert number_facts(x) is None
    assert number_facts(x + 1) is None
    with old_assumptions_forbidden():
        for predicate, number, expected in NUMBERS:
            assert ask_by_rules(predicate, number, True, {}) is expected


def test_number_facts_agree_with_ask():
    numbers = {number for _, number, _ in NUMBERS} - {x}
    for predicate in sorted(get_known_facts_dict(), key=str):
        for number in numbers:
            answer = ask_by_rules(predicate, number, True, {})
            expected = sympy_ask(predicate(number))
            assert answer is None or expected is None or answer is expected


def test_numbers_in_expressions():
    queries = [
        (Q.positive, x + 1, Q.positive(x), True),
        (Q.odd, x + 1, Q.even(x), True),
        (Q.even, 2*x, Q.integer(x), True),
        (Q.irrational, x + pi, Q.rational(x), True),
        (Q.positive, x**2, Q.positive(x), True),
        (Q.zero, 3*x, ~Q.zero(x), False),
        (Q.positive, x + 1, True, None),
    ]
    with old_assumptions_forbidden():
        for predicate, expr, assumptions, expected in queries:
            assert ask(predicate, expr, assumptions) is expected


def test_declared_symbols():
    p = Symbol('p', positive=True)
    n = Symbol('n', integer=True)
    c = Symbol('c', commutative=False)
    queries = [
        (Q.positive, p, True, True),
        (Q.real, p, True, True),
        (Q.zero, p, True, False),
        (Q.zero, Abs(p), True, False),
        (Q.positive, p + 1, True, True),
        (Q.positive, p*x, Q.positive(x), True),
        (Q.even, 2*n, True, True),
        (Q.integer, n + 3, True, True),
        (Q.even, n, True, None),
        (Q.commutative, c, True, False),
    ]
    with old_assumptions_forbidden():
        for predicate, expr, assumptions, expected in queries:
            assert ask(predicate, expr, assumptions) is expected
