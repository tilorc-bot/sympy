from __future__ import annotations

from sympy.abc import w, x, y, z
from sympy.assumptions.ask import Q
from sympy.assumptions.ask_rules import RULES
from sympy.assumptions.ask_rules_generated import RULES as GENERATED_RULES
from sympy.assumptions.assume import Predicate
from sympy.assumptions.rule_checks import check_no_cycles
from sympy.assumptions.tests.test_rule_engine import old_assumptions_forbidden
from sympy.assumptions.rule_engine import (ALL_ARGS, ANY_ARG, EVEN_NUMBER_OF_ARGS,
    FALSE_IF, IF_AND_ONLY_IF, ODD_NUMBER_OF_ARGS, ONE_ARG, OTHER_ARGS, SELF, TRUE_IF,
    ask_by_rules)
from sympy.core.add import Add
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.core.function import Function
from sympy.core.mul import Mul
from sympy.core.numbers import I, pi
from sympy.core.power import Pow
from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.functions.combinatorial.factorials import factorial
from sympy.functions.elementary.complexes import Abs, im, re, sign
from sympy.functions.elementary.exponential import exp, log
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.functions.elementary.trigonometric import (acos, acot, asin, atan,
    cos, cot, sin, tan)

VARYING = (Add, Mul)
ABOUT_ALL_ARGS = (ALL_ARGS, ANY_ARG, ONE_ARG, EVEN_NUMBER_OF_ARGS, ODD_NUMBER_OF_ARGS,
                  OTHER_ARGS)
NUMBERS = (S.One, S.NegativeOne, S.Half, S.ImaginaryUnit)


def ask(predicate, expr, assumptions=True):
    return ask_by_rules(predicate, expr, assumptions, RULES)


def ask_generated(predicate, expr, assumptions=True):
    return ask_by_rules(predicate, expr, assumptions, GENERATED_RULES)


def number_of_arguments(cls):
    if cls in (Basic, Expr, Symbol):
        return 0
    if issubclass(cls, Function):
        return max(cls.nargs)
    return {
        Pow: 2,
    }[cls]


def test_no_cycles():
    check_no_cycles(RULES)


def test_rules_are_well_formed():
    for (cls, predicate), rules in RULES.items():
        assert isinstance(cls, type) and issubclass(cls, Basic)
        assert isinstance(predicate, Predicate) or predicate in NUMBERS
        assert rules
        for kind, conditions in rules:
            assert kind in (FALSE_IF, TRUE_IF, IF_AND_ONLY_IF)
            for selector, condition_predicate in conditions:
                argument, expected = selector
                assert type(argument) is int and type(expected) is bool
                if cls in VARYING:
                    assert argument in ABOUT_ALL_ARGS
                else:
                    assert argument == SELF or 0 <= argument < number_of_arguments(cls)
                assert (isinstance(condition_predicate, Predicate)
                        or condition_predicate in NUMBERS)


def test_numbers():
    assert ask(Q.positive, Abs(x), Q.positive(x)) is True
    assert ask(Q.zero, Abs(x), ~Q.zero(x)) is False
    assert ask(Q.even, Abs(Abs(x)), Q.even(x)) is True
    assert ask_generated(Q.hermitian, sin(x), Q.real(x)) is True
    assert ask(Q.positive, x**y, Q.positive(x) & Q.real(y)) is True
    assert ask(Q.negative, x**y, Q.negative(x) & Q.odd(y)) is True
    assert ask(Q.real, x**y, Q.negative(x) & Q.rational(y) & ~Q.integer(y)) is False
    assert ask(Q.integer, x**y, Q.zero(y)) is True
    assert ask(Q.positive, exp(x), Q.real(x)) is True
    assert ask(Q.zero, exp(x), Q.real(x)) is False
    assert ask(Q.integer, cos(x), Q.zero(x)) is True
    assert ask(Q.zero, sin(x), Q.zero(x)) is True
    assert ask(Q.transcendental, tan(x), Q.algebraic(x) & ~Q.zero(x)) is True
    assert ask(Q.negative, atan(x), Q.negative(x)) is True
    assert ask(Q.negative, acos(x)) is False
    assert ask(Q.positive, acot(x), Q.positive(x)) is True
    assert ask(Q.positive, asin(x), Q.negative(x)) is False
    assert ask(Q.algebraic, cot(x), Q.algebraic(x)) is False
    assert ask(Q.imaginary, re(x)) is False
    assert ask(Q.real, im(x), Q.complex(x)) is True
    assert ask(Q.positive, factorial(x), Q.integer(x) & Q.nonnegative(x)) is True
    assert ask(Q.finite, sign(x)) is True


def test_conditions_about_a_number():
    assert ask_generated(Q.odd, (-1)**x, Q.integer(x)) is True
    assert ask_generated(Q.odd, (-1)**x) is None
    assert ask_generated(Q.even, (-1)**x + 1, Q.integer(x)) is True
    assert ask_generated(Q.odd, y**x, Q.integer(x) & Q.eq(y, -1)) is True
    assert ask_generated(Q.integer, x/2, Q.odd(x)) is False
    assert ask_generated(Q.odd, (-1)**x/2, Q.integer(x)) is False
    assert ask_generated(Q.irrational, 1/x, Q.irrational(x)) is True
    assert ask_generated(Q.rational, y/x, Q.irrational(x) & Q.nonzero(y) & Q.rational(y)
                         ) is False
    assert ask_generated(Q.positive, I**x, Q.imaginary(x)) is True
    assert ask_generated(Q.imaginary, I**x, Q.imaginary(x)) is False
    assert ask_generated(Q.prime, x**y, Q.prime(x) & Q.integer(y) & Q.ne(y, 1)) is False
    assert ask_generated(Q.prime, x**y, Q.prime(x) & Q.integer(y)) is None
    assert ask_generated(Q.algebraic, acos(x), Q.algebraic(x) & Q.ne(x, 1)) is False
    assert ask_generated(Q.algebraic, acos(x), Q.algebraic(x) & Q.negative(x)) is False
    assert ask_generated(Q.algebraic, acos(x), Q.prime(x)) is False
    assert ask_generated(Q.algebraic, acos(x), Q.algebraic(x)) is None


def test_power_of_what_is_not_finite():
    c = Symbol('c', commutative=False)
    assert ask_generated(Q.infinite, x**2, Q.infinite(x)) is True
    assert ask_generated(Q.finite, x**2, ~Q.finite(x)) is False
    # not finite is not infinite: c, nan
    assert ask_generated(Q.infinite, x**2, ~Q.finite(x)) is None
    assert ask_generated(Q.commutative, x**2, ~Q.commutative(x)) is None
    assert ask_generated(Q.commutative, c**2) is None


def test_log():
    assert ask_generated(Q.finite, log(x), Q.infinite(x)) is False
    assert ask_generated(Q.finite, log(x), Q.zero(x)) is False
    assert ask_generated(Q.complex, log(x), Q.nonzero(x)) is True
    assert ask_generated(Q.real, log(x), Q.positive(x)) is True
    assert ask_generated(Q.real, log(x), Q.imaginary(x)) is False
    assert ask_generated(Q.imaginary, log(x), Q.positive(x)) is False
    assert ask_generated(Q.positive, log(x), Q.imaginary(x)) is False
    assert ask_generated(Q.positive, log(x), Q.negative(x)) is False
    assert ask_generated(Q.zero, log(x), Q.eq(x, 1)) is True
    assert ask_generated(Q.zero, log(x), Q.ne(x, 1)) is False
    assert ask_generated(Q.rational, log(x), Q.rational(x) & Q.ne(x, 1)) is False
    assert ask_generated(Q.transcendental, log(x),
                         Q.algebraic(x) & ~Q.zero(x) & Q.ne(x, 1)) is True
    assert ask_generated(Q.transcendental, log(x), Q.algebraic(x) & ~Q.zero(x)) is None


def test_sums_and_products():
    P, N, R = Q.positive, Q.negative, Q.rational
    assert ask_generated(P, x + y, P(x) & Q.nonnegative(y)) is True
    assert ask_generated(P, x + y, Q.nonnegative(x) & P(y)) is True
    assert ask_generated(P, x + y, P(x) & N(y)) is None
    assert ask_generated(N, x + y + z, N(x) & Q.nonpositive(y) & N(z)) is True
    assert ask_generated(Q.even, x + y + z, Q.odd(x) & Q.odd(y) & Q.even(z)) is True
    assert ask_generated(Q.even, x + y + z, Q.even(x) & Q.odd(y) & Q.odd(z)) is True
    assert ask_generated(Q.odd, x + y + z, Q.odd(x) & Q.odd(y) & Q.odd(z)) is True
    assert ask_generated(Q.odd, x + y, Q.odd(x) & Q.odd(y)) is False
    assert ask_generated(Q.irrational, x + y + z, R(x) & Q.irrational(y) & R(z)) is True
    assert ask_generated(Q.irrational, x + y, Q.irrational(x) & Q.irrational(y)) is None
    assert ask_generated(Q.integer, x + y + z,
                         Q.integer(x) & ~Q.integer(y) & Q.integer(z)) is False
    assert ask_generated(Q.integer, x + y, ~Q.integer(x) & ~Q.integer(y)) is None
    assert ask_generated(Q.finite, x + y + z, Q.real(x) & Q.real(z) & ~Q.finite(y)
                         ) is False
    # z may be -y for a y which is not commutative
    assert ask_generated(Q.finite, x + y + z, Q.real(x) & ~Q.finite(y)) is None
    assert ask_generated(Q.finite, x*y, Q.nonzero(x) & ~Q.finite(y)) is False
    # 0*oo is nan
    assert ask_generated(Q.finite, x*y, Q.finite(x) & ~Q.finite(y)) is None
    assert ask_generated(Q.positive_infinite, x + y,
                         Q.positive_infinite(x) & Q.real(y)) is True
    assert ask_generated(Q.extended_real, x + y,
                         Q.positive_infinite(x) & Q.negative_infinite(y)) is None
    assert ask_generated(Q.imaginary, x + y, Q.imaginary(x) & Q.imaginary(y)) is None
    assert ask_generated(Q.imaginary, x + y, Q.imaginary(x) & Q.nonzero(y)) is False
    assert ask_generated(P, x*y*z*w, N(x) & N(y) & P(z) & P(w)) is True
    assert ask_generated(P, x*y*z*w, P(x) & N(y) & P(z) & N(w)) is True
    assert ask_generated(N, x*y*z, N(x) & N(y) & N(z)) is True
    assert ask_generated(P, x*y*z, P(x) & N(y) & P(z)) is False
    assert ask_generated(Q.zero, x*y, Q.zero(x) & Q.finite(y)) is True
    assert ask_generated(Q.zero, x*y, Q.zero(x)) is None
    assert ask_generated(Q.zero, x*y*z, ~Q.zero(x) & Q.nonzero(y) & P(z)) is False
    assert ask_generated(Q.irrational, x*y, Q.irrational(x) & R(y) & ~Q.zero(y)) is True
    assert ask_generated(Q.irrational, x*y, Q.irrational(x) & R(y)) is None
    assert ask_generated(Q.even, x*y*z, Q.integer(x) & Q.even(y) & Q.integer(z)) is True
    assert ask_generated(Q.real, x*y, Q.imaginary(x) & Q.imaginary(y)) is True
    assert ask_generated(Q.real, x*y, Q.imaginary(x) & P(y)) is False
    assert ask_generated(Q.composite, x*y, Q.prime(x) & Q.prime(y)) is True
    assert ask_generated(Q.prime, x*y*z,
                         Q.integer(x) & Q.composite(y) & Q.integer(z)) is False


def test_wrong_answers_of_ask():
    # ask gives an answer for each of these, and it is wrong
    real_and_two_imaginary = Q.real(x) & Q.imaginary(y) & Q.imaginary(z)

    # a factor or a term may be zero
    assert ask_generated(Q.imaginary, x*y, Q.imaginary(x) & Q.real(y)) is None
    assert ask_generated(Q.imaginary, I*x, Q.real(x)) is None
    assert ask_generated(Q.imaginary, x + I, Q.real(x)) is None
    assert ask_generated(Q.imaginary, x + y, Q.imaginary(x) & Q.real(y)) is None
    assert ask_generated(Q.imaginary, x + y + z, real_and_two_imaginary) is None
    assert ask_generated(Q.antihermitian, x, Q.real(x)) is None
    assert ask_generated(Q.antihermitian, I*x, Q.antihermitian(x)) is None
    assert ask_generated(Q.antihermitian, x + I, Q.real(x)) is None
    assert ask_generated(Q.antihermitian, x + y, Q.antihermitian(x) & Q.real(y)) is None
    assert ask_generated(Q.antihermitian, x + y, Q.imaginary(x) & Q.real(y)) is None
    assert ask_generated(Q.antihermitian, x + y + z, real_and_two_imaginary) is None
    assert ask_generated(Q.hermitian, I*x, Q.hermitian(x)) is None
    assert ask_generated(Q.hermitian, I*x, Q.real(x)) is None
    assert ask_generated(Q.hermitian, x*y, Q.real(x) & Q.zero(y)) is True
    assert ask_generated(Q.extended_real, x*y, Q.imaginary(x) & Q.zero(y)) is True
    assert ask_generated(Q.rational, x*y, Q.irrational(x) & Q.zero(y)) is True
    assert ask_generated(Q.irrational, x*y, Q.zero(x) & Q.irrational(y)) is False
    assert ask_generated(Q.transcendental, x*y,
                         Q.zero(x) & Q.transcendental(y)) is False
    assert ask_generated(Q.integer, sqrt(2)*x, Q.integer(x)) is None
    assert ask_generated(Q.nonzero, 5**(2*I*pi*x), Q.integer(x)) is None
    assert ask_generated(Q.imaginary, x**y,
                         Q.negative(x) & Q.rational(y) & Q.integer(2*y)) is None
    assert ask_generated(Q.zero, x*y, Q.zero(x)) is None

    # the terms may cancel
    assert ask_generated(Q.imaginary, x + I, Q.imaginary(x)) is None
    assert ask_generated(Q.imaginary, x + y, Q.imaginary(x) & Q.imaginary(y)) is None

    # the argument may be infinite
    assert ask_generated(Q.real, Abs(x)) is None
    assert ask_generated(Q.complex, Abs(x)) is None
    assert ask_generated(Q.real, re(x)) is None
    assert ask_generated(Q.complex, re(x)) is None
    assert ask_generated(Q.real, im(x)) is None
    assert ask_generated(Q.complex, im(x)) is None
    assert ask_generated(Q.complex, exp(x)) is None
    assert ask_generated(Q.complex, sin(x)) is None
    assert ask_generated(Q.complex, cos(x)) is None
    assert ask_generated(Q.finite, sin(x)) is None
    assert ask_generated(Q.finite, sin(x), ~Q.finite(x)) is None
    assert ask_generated(Q.finite, cos(x)) is None
    assert ask_generated(Q.finite, cos(x), ~Q.finite(x)) is None
    assert ask_generated(Q.finite, 2*sin(x)) is None
    assert ask_generated(Q.finite, sin(x)**2) is None
    assert ask_generated(Q.finite, cos(x)**2) is None
    assert ask_generated(Q.finite, log(x), ~Q.zero(x)) is None
    assert ask_generated(Q.finite, log(x), ~Q.extended_real(x)) is None
    assert ask_generated(Q.complex, log(x)) is None
    assert ask_generated(Q.finite, 2**x, ~Q.finite(x)) is None

    # a power of zero may be infinite
    assert ask_generated(Q.algebraic, x**y, Q.algebraic(x) & Q.rational(y)) is None
    assert ask_generated(Q.complex, x**y, Q.complex(x) & Q.complex(y)) is None

    # acos(1) is zero, acot(-1) is negative, (2*I)**(I*pi/(2*log(2))) is imaginary
    assert ask_generated(Q.positive, acos(x),
                         Q.nonnegative(x + 1) & Q.nonpositive(x - 1)) is None
    assert ask_generated(Q.positive, acot(x), Q.real(x)) is None
    assert ask_generated(Q.imaginary, (2*I)**x, Q.imaginary(x)) is None

    # log(oo) is oo; log(-1) and log(3/5 + 4*I/5) are imaginary
    assert ask_generated(Q.positive_infinite, log(x), Q.positive_infinite(x)) is True
    assert ask_generated(Q.imaginary, log(x), ~Q.imaginary(x)) is None


def test_old_assumptions_are_not_used():
    p = Symbol('p', positive=True)
    # making an expression uses the old assumptions
    power, number, product = exp(x)**y, sqrt(2) - 1, p*x
    with old_assumptions_forbidden():
        assert ask(Q.positive, power, Q.real(x) & Q.real(y)) is True
        assert ask(Q.positive, x) is None
        assert ask(Q.positive, p) is True
        assert ask(Q.zero, product, Q.positive(x)) is False
        assert ask(Q.positive, number) is True
