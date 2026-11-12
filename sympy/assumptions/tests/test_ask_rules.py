from __future__ import annotations

from sympy.abc import w, x, y, z
from sympy.assumptions.ask import Q
from sympy.assumptions.ask_rules import RULES
from sympy.assumptions.ask_rules_generated import RULES as GENERATED_RULES
from sympy.assumptions.assume import Predicate
from sympy.assumptions.rule_checks import check_no_cycles
from sympy.assumptions.tests.test_rule_engine import old_assumptions_forbidden
from sympy.assumptions.rule_engine import (ALL_ARGS, ALL_ARGS_BUT_AT_MOST_ONE, ANY_ARG,
    EVEN_NUMBER_OF_ARGS, FALSE_IF, IF_AND_ONLY_IF, ODD_NUMBER_OF_ARGS, ONE_ARG, OTHER_ARGS,
    OTHER_ARGS_BUT_AT_MOST_ONE, SELF, SOME_EVEN_NUMBER_OF_ARGS, SOME_ODD_NUMBER_OF_ARGS,
    TRUE_IF, ask_by_rules)
from sympy.assumptions.rule_engine import (ALL_ARGS, ANY_ARG, EVEN_NUMBER_OF_ARGS,
    FALSE_IF, IF_AND_ONLY_IF, ODD_NUMBER_OF_ARGS, ONE_ARG, OTHER_ARGS, SELF,
    SOME_EVEN_NUMBER_OF_ARGS, SOME_ODD_NUMBER_OF_ARGS, TRUE_IF, ask_by_rules)
from sympy.calculus.accumulationbounds import AccumulationBounds
from sympy.core.add import Add
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.core.function import DefinedFunction, Derivative, Function, Subs
from sympy.core.mod import Mod
from sympy.core.mul import Mul
from sympy.core.numbers import E, I, pi
from sympy.core.power import Pow
from sympy.core.singleton import S
from sympy.core.symbol import Symbol, symbols
from sympy.functions.combinatorial.factorials import (FallingFactorial, binomial,
    factorial, factorial2, subfactorial)
from sympy.functions.combinatorial.numbers import (catalan, genocchi, legendre_symbol,
    totient)
from sympy.functions.elementary.complexes import (Abs, adjoint, arg, conjugate, im, re,
    sign, transpose)
from sympy.functions.elementary.exponential import LambertW, exp, exp_polar, log
from sympy.functions.elementary.hyperbolic import (acosh, acoth, acsch, asech, asinh, atanh,
    cosh, coth, csch, sech, sinh, tanh)
from sympy.functions.elementary.integers import ceiling, floor, frac
from sympy.functions.elementary.miscellaneous import Max, Min, sqrt
from sympy.functions.elementary.trigonometric import (acos, acot, acsc, asec, asin,
    atan, atan2, cos, cot, csc, sec, sin, sinc, tan)
from sympy.functions.special.error_functions import erf, erf2, erfc, erfcinv, erfi
from sympy.functions.special.gamma_functions import gamma, loggamma, polygamma
from sympy.integrals.integrals import Integral

VARYING = (Add, DefinedFunction, Max, Min, Mul)
SOME_ARGS = (SOME_EVEN_NUMBER_OF_ARGS, SOME_ODD_NUMBER_OF_ARGS)
ABOUT_ALL_ARGS = (ALL_ARGS, ANY_ARG, ONE_ARG, EVEN_NUMBER_OF_ARGS, ODD_NUMBER_OF_ARGS,
                  OTHER_ARGS, ALL_ARGS_BUT_AT_MOST_ONE, OTHER_ARGS_BUT_AT_MOST_ONE) + SOME_ARGS
NUMBERS = (S.One, S.NegativeOne, S.Half, S.ImaginaryUnit)


def ask(predicate, expr, assumptions=True):
    return ask_by_rules(predicate, expr, assumptions, RULES)


def ask_generated(predicate, expr, assumptions=True):
    return ask_by_rules(predicate, expr, assumptions, GENERATED_RULES)


def number_of_arguments(cls):
    if cls in (Basic, Expr, Symbol):
        return 0
    if issubclass(cls, Function) and cls.nargs.is_finite_set:
        return max(cls.nargs)
    return {
        AccumulationBounds: 2,
        Derivative: 1,
        Integral: 1,
        Subs: 1,
        Pow: 2,
        exp_polar: 1,
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
                    assert expected or argument not in SOME_ARGS
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
    assert ask(Q.real, re(x), Q.finite(x)) is True
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
    assert ask_generated(Q.zero, log(x + y), Q.eq(x, 1) & Q.zero(y)) is True
    assert ask_generated(Q.zero, log(x + y), Q.eq(x, 1)) is None
    assert ask_generated(Q.extended_positive, x + y,
                         Q.negative_infinite(x) & Q.finite(y)) is False
    assert ask_generated(Q.extended_negative, x + y,
                         Q.positive_infinite(x) & Q.finite(y)) is False
    # oo + I is not extended real
    assert ask_generated(Q.extended_positive, x + y,
                         Q.positive_infinite(x) & Q.finite(y)) is None
    assert ask_generated(Q.infinite, x*y, Q.infinite(x) & Q.finite(y) & ~Q.zero(y)
                         ) is True
    assert ask_generated(Q.infinite, x*y*z, Q.finite(x) & ~Q.zero(x) & Q.infinite(y)
                         & Q.infinite(z)) is True


def test_sums_and_products_with_one_argument_of_another_kind():
    XR, NZ = Q.extended_real, Q.nonzero
    assert ask_generated(XR, x + y + z, XR(x) & Q.real(y) & Q.real(z)) is True
    assert ask_generated(XR, x + y, Q.positive_infinite(x) & Q.real(y)) is True
    # oo - oo is nan
    assert ask_generated(XR, x + y + z, XR(x) & XR(y) & Q.real(z)) is None
    assert ask_generated(XR, x + y, ~XR(x) & Q.finite(x) & XR(y)) is False
    assert ask_generated(XR, x + y + z, ~XR(x) & Q.real(y) & Q.real(z)) is False
    # zoo + oo is nan
    assert ask_generated(XR, x + y, ~XR(x) & XR(y)) is None
    assert ask_generated(Q.nonzero, x + y, Q.imaginary(x) & Q.imaginary(y)) is False
    assert ask_generated(Q.irrational, x + y, Q.imaginary(x) & Q.imaginary(y)) is False
    assert ask_generated(Q.irrational, x + y + z, Q.integer(x) & Q.imaginary(y)
                         & Q.rational(z)) is False
    assert ask_generated(Q.irrational, x + y, Q.rational(x) & Q.imaginary(y)) is False
    # x = sqrt(2) - I, y = I
    assert ask_generated(Q.irrational, x + y, ~Q.real(x) & Q.imaginary(y)) is None
    # Mod(I, 2) is I
    assert ask_generated(Q.nonnegative, Mod(x, y), Q.complex(x) & Q.positive(y)) is None
    assert ask_generated(Q.zero, x + y, Q.imaginary(x) & Q.imaginary(y)) is None
    assert ask_generated(XR, x*y*z, XR(x) & NZ(y) & NZ(z)) is True
    # 0*oo is nan
    assert ask_generated(XR, x*y*z, XR(x) & XR(y) & NZ(z)) is None
    assert ask_generated(XR, x*y, Q.imaginary(x) & Q.extended_nonzero(y)) is False
    assert ask_generated(XR, x*y, Q.imaginary(x) & XR(y)) is None
    assert ask_generated(Q.infinite, x*y, Q.infinite(x) & ~Q.zero(y)) is True
    assert ask_generated(Q.infinite, x*y, Q.infinite(x)) is None
    assert ask_generated(Q.extended_nonzero, x*y, Q.zero(x) & Q.finite(y)) is False
    assert ask_generated(Q.extended_nonzero, x*y, Q.zero(x) & Q.infinite(y)) is None
    P, N = Q.positive, Q.negative
    assert ask_generated(N, x*y, N(x) & ~P(y)) is False
    assert ask_generated(N, x*y*z, N(x) & N(y) & ~N(z)) is False
    assert ask_generated(P, x*y*z, N(x) & ~N(y) & P(z)) is False
    assert ask_generated(P, x*y*z, N(x) & ~P(y) & N(z)) is False
    # 0*oo is nan
    assert ask_generated(P, x*y*z, N(x) & ~P(y) & ~P(z) & XR(z)) is None
    # x = y = I
    assert ask_generated(N, x*y, ~P(x) & ~P(y)) is None
    XNZ, IM = Q.extended_nonzero, Q.imaginary
    assert ask_generated(XNZ, x*y*z, IM(x) & Q.real(y) & Q.real(z)) is False
    assert ask_generated(Q.extended_positive, x*y, IM(x) & Q.extended_nonnegative(y)) is False
    assert ask_generated(Q.extended_negative, w*x*y*z, IM(x) & IM(y) & IM(z) & XR(w)
                         ) is False
    # 0*oo is nan
    assert ask_generated(XNZ, x*y*z, IM(x) & XR(y) & XR(z)) is None
    assert ask_generated(XNZ, x*y*z, IM(x) & Q.complex(y) & ~IM(y) & Q.real(z)) is False
    # y = z = 1 + I
    assert ask_generated(XNZ, x*y*z, IM(x) & Q.complex(y) & ~IM(y) & Q.complex(z)
                         & ~IM(z)) is None
    assert ask_generated(P, x*y, ~Q.real(x) & Q.extended_positive(y)) is False
    assert ask_generated(Q.real, x*y*z, ~Q.real(x) & XNZ(y) & XNZ(z)) is False
    # x = y = I
    assert ask_generated(Q.real, x*y, ~Q.real(x) & ~Q.real(y) & ~Q.zero(y)) is None
    assert ask_generated(P, x*y*z, N(x) & ~N(y) & ~N(z)) is None


def test_signs_of_products_and_powers():
    assert ask_generated(Q.negative, 2*x, Q.nonnegative(x)) is False
    assert ask_generated(Q.nonpositive, -x*y, Q.nonnegative(x) & Q.positive(y)) is True
    assert ask_generated(Q.nonnegative, x*y*z,
                         Q.negative(x) & Q.nonnegative(y) & Q.negative(z)) is True
    assert ask_generated(Q.positive, x*y, Q.negative(x) & Q.nonnegative(y)) is False
    assert ask_generated(Q.positive, 2*x, ~Q.positive(x)) is False
    assert ask_generated(Q.positive, -x, ~Q.negative(x)) is False
    assert ask_generated(Q.negative, -x, ~Q.positive(x)) is False
    assert ask_generated(Q.integer, x/2, Q.even(x)) is True
    assert ask_generated(Q.integer, x**3/2, Q.even(x)) is True
    assert ask_generated(Q.extended_real, x*y,
                         Q.nonzero(x) & Q.complex(y) & ~Q.real(y)) is False
    assert ask_generated(Q.extended_real, x*y, ~Q.zero(x) & Q.complex(y)
                         & ~Q.real(y)) is None
    assert ask_generated(Q.real, x**y, Q.nonnegative(x) & Q.nonnegative(y)) is True
    assert ask_generated(Q.zero, x**y, Q.zero(x) & Q.positive_infinite(y)) is True
    assert ask_generated(Q.zero, x**y, Q.zero(x) & Q.extended_nonpositive(y)) is False
    assert ask_generated(Q.zero, x**y, ~Q.zero(x) & Q.nonnegative(y)) is False
    assert ask_generated(Q.zero, 1/x, Q.infinite(x)) is True
    assert ask_generated(Q.positive, x**y, Q.zero(x) & ~Q.zero(y)) is False
    assert ask_generated(Q.negative, sqrt(x)) is False
    assert ask_generated(Q.extended_real, sqrt(x + I), Q.real(x)) is False
    assert ask_generated(Q.imaginary, sqrt(x), Q.negative(x)) is True
    assert ask_generated(Q.integer, 2**x, Q.negative(x)) is False
    assert ask_generated(Q.integer, x**y, Q.integer(x) & Q.negative(y)) is None
    assert ask_generated(Q.algebraic, x**y, Q.algebraic(x) & Q.irrational(x)
                         & Q.algebraic(y) & Q.irrational(y)) is False
    assert ask_generated(Q.extended_negative, x**y,
                         Q.extended_real(x) & Q.even(y)) is False
    assert ask_generated(Q.negative, x**2, Q.extended_real(x)) is False
    assert ask_generated(Q.extended_nonnegative, x**y,
                         Q.extended_real(x) & ~Q.zero(x) & Q.even(y)) is True
    assert ask_generated(Q.extended_positive, x**y,
                         Q.extended_real(x) & ~Q.zero(x) & Q.even(y)) is None
    assert ask_generated(Q.extended_negative, x**y, Q.real(x) & Q.integer(y)) is None
    assert ask_generated(Q.complex, x**y, Q.complex(x) & Q.nonnegative(y)) is True
    assert ask_generated(Q.complex, x**y, Q.complex(x) & Q.complex(y)) is None
    assert ask_generated(Q.finite, x**y, Q.infinite(x) & Q.negative(y)) is True
    assert ask_generated(Q.finite, x**y, Q.infinite(x) & Q.real(y)) is None
    assert ask_generated(Q.even, I**x, Q.integer(x)) is False
    assert ask_generated(Q.odd, I**x, Q.integer(x)) is None
    assert ask_generated(Q.even, x**y, Q.imaginary(x) & Q.even(y)) is None


def test_products_of_factors_which_may_be_zero():
    assert ask_generated(Q.nonpositive, x*y, Q.nonnegative(x) & Q.nonpositive(y)) is True
    assert ask_generated(Q.positive, x*y, Q.nonnegative(x) & Q.nonpositive(y)) is False
    assert ask_generated(Q.nonnegative, x*y, Q.nonpositive(x) & Q.nonpositive(y)) is True
    assert ask_generated(Q.negative, x*y, Q.nonpositive(x) & Q.nonpositive(y)) is False
    assert ask_generated(Q.nonnegative, x*y*z, Q.negative(x) & Q.nonnegative(y)
                         & Q.nonpositive(z)) is True
    assert ask_generated(Q.nonpositive, -x*y*z, Q.negative(x) & Q.nonnegative(y)
                         & Q.nonpositive(z)) is True
    assert ask_generated(Q.nonpositive, 17*x*y*z, Q.positive(x) & Q.nonnegative(y)
                         & Q.nonpositive(z)) is True
    assert ask_generated(Q.real, x*y, Q.nonnegative(x) & Q.nonpositive(y)) is True
    assert ask_generated(Q.nonnegative, x*y, Q.nonnegative(x) & Q.nonpositive(y)) is None
    assert ask_generated(Q.zero, x*y, Q.nonnegative(x) & Q.nonpositive(y)) is None
    assert ask_generated(Q.nonpositive, x*y, Q.nonnegative(x) & Q.real(y)) is None
    assert ask_generated(Q.nonpositive, x*y*z, Q.nonnegative(x) & Q.nonpositive(y)
                         & Q.nonpositive(z)) is None
    # 0*oo is nan
    assert ask_generated(Q.extended_nonpositive, x*y, Q.extended_nonnegative(x)
                         & Q.extended_nonpositive(y)) is None
    # y may be I
    assert ask_generated(Q.real, I*y, ~Q.zero(y)) is None
    assert ask_generated(Q.real, I*y, Q.nonzero(y)) is False


def test_sums_with_one_and_minus_one():
    positive_integer = Q.integer(x) & Q.positive(x)
    assert ask_generated(Q.nonnegative, x - 1, positive_integer) is True
    assert ask_generated(Q.negative, x - 1, positive_integer) is False
    assert ask_generated(Q.nonnegative, x + y - 1, positive_integer & Q.prime(y)) is True
    assert ask_generated(Q.nonpositive, 1 - x, positive_integer) is True
    assert ask_generated(Q.nonnegative, atan(x - 1), positive_integer) is True
    assert ask_generated(Q.positive, factorial2(x - 1), Q.even(x) & Q.positive(x)) is True
    assert ask_generated(Q.nonnegative, x - 1, Q.positive(x)) is None
    assert ask_generated(Q.nonnegative, x - 1, Q.integer(x) & Q.nonnegative(x)) is None
    assert ask_generated(Q.nonnegative, x - 2, positive_integer) is None
    assert ask_generated(Q.positive, x - 1, positive_integer) is None
    assert ask_generated(Q.integer, (x + 1)**-2, positive_integer) is False
    assert ask_generated(Q.integer, (x + 1)**-2, Q.integer(x) & Q.nonnegative(x)) is None
    assert ask_generated(Q.prime, x**(y + 1), positive_integer & Q.integer(y)
                         & Q.positive(y)) is False
    assert ask_generated(Q.prime, x**(y + 1), positive_integer & Q.integer(y)
                         & Q.nonnegative(y)) is None


def test_composite_products_and_powers():
    positive_integers = (Q.integer(x) & Q.positive(x) & Q.integer(y) & Q.positive(y))
    assert ask_generated(Q.composite, (x + 1)*(y + 1), positive_integers) is True
    assert ask_generated(Q.prime, (x + 1)*(y + 1), positive_integers) is False
    assert ask_generated(Q.composite, (x + 1)**(y + 1), positive_integers) is True
    assert ask_generated(Q.composite, (-x - 1)**(2*y), positive_integers) is True
    assert ask_generated(Q.composite, x*y, Q.prime(x) & Q.integer(y) & Q.positive(y)
                         & Q.ne(y, 1)) is True
    assert ask_generated(Q.composite, x**y, Q.prime(x) & Q.even(y) & Q.positive(y)
                         ) is True
    # x or y may be 1
    assert ask_generated(Q.composite, x*(y + 1), positive_integers) is None
    assert ask_generated(Q.composite, (x + 1)**y, positive_integers) is None
    # -1 to an even power is 1
    assert ask_generated(Q.composite, (-x)**(2*y), positive_integers) is None
    # an odd power of a negative number is negative
    assert ask_generated(Q.composite, (-x - 1)**(y + 1), positive_integers) is None


def test_min_and_max():
    assert ask_generated(Q.rational, Min(x, y), Q.integer(x) & Q.rational(y)) is True
    assert ask_generated(Q.even, Max(x, y), Q.irrational(x) & Q.odd(y)) is False
    assert ask_generated(Q.positive, Max(x, y, z), Q.positive(x) & Q.real(y)) is None
    assert ask_generated(Q.positive, Max(x, y, z),
                         Q.positive(x) & Q.real(y) & Q.real(z)) is True
    # Max(1, oo) is oo
    assert ask_generated(Q.positive, Max(x, y),
                         Q.positive(x) & Q.extended_real(y)) is None
    assert ask_generated(Q.extended_positive, Max(x, y),
                         Q.positive(x) & Q.extended_real(y)) is True
    # Max and Min have a value only if every argument is extended real
    assert ask_generated(Q.extended_positive, Max(x, y), Q.positive(x)) is True
    assert ask_generated(Q.finite, Max(x, y), Q.finite(x) & Q.finite(y)) is True
    assert ask_generated(Q.imaginary, Min(x, y), ~Q.imaginary(x) & ~Q.imaginary(y)
                         ) is False
    # Max(-1, oo) is oo
    assert ask_generated(Q.positive, Max(x, y), Q.negative(x) & Q.infinite(y)) is False
    assert ask_generated(Q.negative, Max(x, y), Q.negative(x) & Q.infinite(y)) is None
    assert ask_generated(Q.negative, Min(x, y), Q.negative(x) & Q.real(y)) is True
    assert ask_generated(Q.negative, Min(x, y),
                         Q.positive(x) & Q.nonnegative(y)) is False


def test_elementary_functions():
    assert ask_generated(Q.odd, Abs(x), Q.real(x) & ~Q.odd(x)) is False
    assert ask_generated(Q.real, atan(x), Q.extended_real(x)) is True
    assert ask_generated(Q.nonzero, atan(x), Q.extended_nonzero(x)) is True
    assert ask_generated(Q.finite, x*atan(x), Q.extended_real(x) & Q.infinite(x)
                         ) is False
    assert ask_generated(Q.real, acot(x), Q.real(x)) is True
    assert ask_generated(Q.imaginary, sign(x), Q.imaginary(x)) is True
    assert ask_generated(Q.integer, sign(x), Q.extended_real(x)) is True
    assert ask_generated(Q.zero, sign(x), Q.nonzero(x)) is False
    assert ask_generated(Q.nonnegative, log(x), Q.integer(x) & Q.positive(x)) is True
    assert ask_generated(Q.algebraic, re(x), Q.algebraic(x)) is True
    assert ask_generated(Q.extended_real, re(x), Q.extended_real(x)) is True
    assert ask_generated(Q.real, re(x), Q.finite(x)) is True
    assert ask_generated(Q.extended_real, re(x), ~Q.commutative(x)) is True
    assert ask_generated(Q.commutative, re(x), ~Q.commutative(x)) is True
    assert ask_generated(Q.zero, re(x), ~Q.commutative(x)) is False
    assert ask_generated(Q.zero, im(x), ~Q.commutative(x)) is False
    assert ask_generated(Q.imaginary, sign(x), ~Q.commutative(x)) is False
    assert ask_generated(Q.algebraic, re(x), Q.extended_real(x) & ~Q.algebraic(x)) is False
    assert ask_generated(Q.integer, re(x), Q.infinite(x) & Q.extended_real(x)) is False
    assert ask_generated(Q.extended_negative, re(x), Q.negative_infinite(x)) is True
    assert ask_generated(Q.extended_positive, re(x), Q.extended_nonpositive(x)) is False
    assert ask_generated(Q.algebraic, Abs(x), Q.imaginary(x) & ~Q.algebraic(x)) is False
    assert ask_generated(Q.algebraic, im(x), Q.imaginary(x) & ~Q.algebraic(x)) is False
    assert ask_generated(Q.imaginary, re(x), Q.infinite(x) & Q.extended_real(x)) is False
    assert ask_generated(Q.zero, re(x), Q.imaginary(x)) is True
    assert ask_generated(Q.zero, re(x), Q.complex(x) & ~Q.imaginary(x) & ~Q.zero(x)
                         ) is False
    assert ask_generated(Q.zero, re(x), Q.infinite(x) & Q.extended_real(x)) is False
    assert ask_generated(Q.algebraic, im(x), Q.algebraic(x)) is True
    assert ask_generated(Q.zero, im(x), Q.extended_real(x)) is True
    assert ask_generated(Q.zero, im(x), Q.complex(x) & ~Q.extended_real(x)) is False
    assert ask_generated(Q.finite, im(x), Q.finite(x)) is True
    assert ask_generated(Q.imaginary, im(x), Q.extended_real(x)) is False
    assert ask_generated(Q.imaginary, sign(x), Q.complex(x) & ~Q.imaginary(x)) is False
    assert ask_generated(Q.integer, sign(x), ~Q.extended_real(x)) is False
    assert ask_generated(Q.integer, Abs(x), Q.extended_real(x) & ~Q.integer(x)) is False
    assert ask_generated(Q.rational, Abs(x), Q.extended_real(x) & ~Q.rational(x)) is False
    assert ask_generated(Q.even, Abs(x), Q.infinite(x)) is False
    assert ask_generated(Q.extended_positive, Abs(x), ~Q.zero(x)) is True
    assert ask_generated(Q.real, arg(x), Q.complex(x) & ~Q.zero(x)) is True
    assert ask_generated(Q.finite, arg(x), Q.extended_real(x) & ~Q.zero(x)) is True
    assert ask_generated(Q.algebraic, conjugate(x), Q.algebraic(x)) is True
    assert ask_generated(Q.algebraic, conjugate(x), Q.transcendental(x)) is False
    assert ask_generated(Q.finite, conjugate(x), Q.complex(x)) is True
    assert ask_generated(Q.zero, conjugate(x), Q.zero(x)) is True
    assert ask_generated(Q.complex, conjugate(x), ~Q.complex(x)) is False
    assert ask_generated(Q.real, cot(x), Q.finite(x) & ~Q.real(x)) is False
    assert ask_generated(Q.finite, cot(x), Q.imaginary(x)) is True
    # cot(0) and sec(pi/2) are zoo
    assert ask_generated(Q.extended_real, cot(x), Q.real(x)) is None
    # sec(oo*I) is zero
    assert ask_generated(Q.zero, sec(x)) is None
    assert ask_generated(Q.zero, sec(x), Q.finite(x)) is False
    assert ask_generated(Q.algebraic, sec(x), Q.algebraic(x) & ~Q.zero(x)) is False
    assert ask_generated(Q.positive, cosh(x), Q.real(x)) is True
    assert ask_generated(Q.negative, sinh(x), Q.negative(x)) is True
    assert ask_generated(Q.real, tanh(x), Q.extended_real(x)) is True
    # sech(oo) is zero
    assert ask_generated(Q.positive, sech(x), Q.extended_real(x)) is None
    assert ask_generated(Q.zero, LambertW(x), Q.negative(x)) is False
    assert ask_generated(Q.negative, floor(x), Q.negative(x)) is True
    assert ask_generated(Q.positive, ceiling(x), Q.positive(x)) is True
    assert ask_generated(Q.zero, frac(x), Q.integer(x)) is True
    assert ask_generated(Q.nonnegative, Mod(x, y), Q.integer(x) & Q.positive(y)) is True
    assert ask_generated(Q.infinite, csc(x), Q.zero(x)) is True
    assert ask_generated(Q.positive, sinc(x), Q.zero(x)) is True
    assert ask_generated(Q.integer, exp_polar(x), Q.zero(x)) is True
    # LambertW(1, 1) is not real
    assert ask_generated(Q.real, LambertW(x), Q.positive(x)) is None
    assert ask_generated(Q.complex, exp(x), Q.extended_negative(x)) is True
    assert ask_generated(Q.finite, exp(x), Q.negative_infinite(x)) is True
    assert ask_generated(Q.extended_positive, exp(x),
                         Q.extended_real(x) & ~Q.negative_infinite(x)) is True
    assert ask_generated(Q.zero, exp(x), Q.positive_infinite(x)) is False
    # exp(-oo) is zero
    assert ask_generated(Q.extended_positive, exp(x), Q.extended_real(x)) is None
    assert ask_generated(Q.finite, exp_polar(x), Q.finite(x)) is True
    assert ask_generated(Q.extended_real, exp_polar(x), Q.extended_real(x)) is True
    assert ask_generated(Q.zero, exp_polar(x), Q.finite(x)) is False
    assert ask_generated(Q.extended_real, log(x), ~Q.extended_real(x)) is False
    # log(-oo) is oo
    assert ask_generated(Q.extended_real, log(x), Q.extended_negative(x)) is None
    assert ask_generated(Q.finite, floor(x), Q.finite(x)) is True
    assert ask_generated(Q.infinite, ceiling(x), Q.infinite(x)) is True
    # floor(I/2) is 0
    assert ask_generated(Q.real, floor(x), ~Q.real(x)) is None
    assert ask_generated(Q.finite, frac(x), Q.finite(x)) is True
    assert ask_generated(Q.negative, frac(x), Q.extended_real(x)) is False
    assert ask_generated(Q.zero, frac(x), Q.real(x) & ~Q.integer(x)) is False
    # frac(I) is 0
    assert ask_generated(Q.integer, frac(x), Q.imaginary(x)) is None
    assert ask_generated(Q.integer, frac(x), Q.transcendental(x)) is False
    assert ask_generated(Q.odd, frac(x), Q.finite(x)) is False
    # floor(I*b) is I*floor(b)
    assert ask_generated(Q.extended_nonzero, floor(x), Q.imaginary(x)) is False
    assert ask_generated(Q.extended_negative, floor(x), Q.extended_negative(x)) is True
    assert ask_generated(Q.extended_positive, ceiling(x), Q.extended_positive(x)) is True
    assert ask_generated(Q.irrational, floor(x)) is False
    # log(-oo) is oo, log(0) is zoo
    assert ask_generated(Q.positive_infinite, log(x), Q.negative_infinite(x)) is True
    assert ask_generated(Q.extended_nonpositive, log(x), Q.extended_nonpositive(x)
                         ) is False


def test_hyperbolic_functions():
    infinite_real = Q.extended_real(x) & Q.infinite(x)
    # sinh(oo) = cosh(oo) = oo
    assert ask_generated(Q.infinite, sinh(x), infinite_real) is True
    assert ask_generated(Q.positive, sinh(x), Q.extended_positive(x)) is None
    assert ask_generated(Q.positive, sinh(x), Q.extended_real(x) & ~Q.positive(x)) is False
    assert ask_generated(Q.extended_negative, sinh(x), Q.extended_nonnegative(x)) is False
    assert ask_generated(Q.zero, sinh(x), Q.extended_nonzero(x)) is False
    assert ask_generated(Q.infinite, cosh(x), infinite_real) is True
    # tanh(oo) = coth(oo) = 1, coth(0) = zoo
    assert ask_generated(Q.positive, tanh(x), Q.extended_nonpositive(x)) is False
    assert ask_generated(Q.negative, tanh(x), Q.extended_positive(x)) is False
    assert ask_generated(Q.integer, tanh(x), infinite_real) is True
    assert ask_generated(Q.prime, tanh(x), Q.extended_real(x)) is False
    assert ask_generated(Q.zero, tanh(x), Q.extended_nonzero(x)) is False
    assert ask_generated(Q.positive, coth(x), Q.extended_positive(x)) is True
    assert ask_generated(Q.positive, coth(x), Q.extended_nonpositive(x)) is False
    assert ask_generated(Q.real, coth(x), Q.extended_nonzero(x)) is True
    assert ask_generated(Q.real, coth(x), Q.real(x)) is None
    assert ask_generated(Q.infinite, coth(x), Q.zero(x)) is True
    assert ask_generated(Q.zero, coth(x), Q.extended_real(x)) is False
    assert ask_generated(Q.composite, coth(x), infinite_real) is False
    # csch(oo) = sech(oo) = 0, csch(0) = zoo
    assert ask_generated(Q.zero, csch(x), infinite_real) is True
    assert ask_generated(Q.zero, csch(x), Q.finite(x)) is False
    assert ask_generated(Q.infinite, csch(x), Q.zero(x)) is True
    assert ask_generated(Q.real, csch(x), Q.extended_nonzero(x)) is True
    assert ask_generated(Q.positive, csch(x), Q.extended_real(x) & ~Q.positive(x)) is False
    assert ask_generated(Q.imaginary, csch(x), Q.extended_real(x)) is False
    assert ask_generated(Q.zero, sech(x), infinite_real) is True
    assert ask_generated(Q.zero, sech(x), Q.finite(x)) is False
    assert ask_generated(Q.imaginary, sech(x), Q.imaginary(x)) is False
    # asinh(zoo) = acosh(zoo) = zoo, asech(0) = oo, acsch(0) = zoo
    assert ask_generated(Q.zero, asinh(x), ~Q.zero(x)) is False
    assert ask_generated(Q.extended_real, asinh(x), ~Q.extended_real(x)) is False
    assert ask_generated(Q.infinite, asinh(x), Q.infinite(x)) is True
    assert ask_generated(Q.finite, acosh(x), Q.finite(x)) is True
    assert ask_generated(Q.infinite, asech(x), Q.zero(x)) is True
    assert ask_generated(Q.extended_positive, asech(x), Q.zero(x)) is True
    assert ask_generated(Q.extended_negative, asech(x)) is False
    assert ask_generated(Q.finite, asech(x), ~Q.zero(x)) is True
    assert ask_generated(Q.extended_real, acsch(x), Q.extended_nonzero(x)) is True
    assert ask_generated(Q.extended_real, acsch(x), Q.zero(x)) is False
    assert ask_generated(Q.extended_real, acsch(x), Q.extended_real(x)) is None
    assert ask_generated(Q.extended_nonzero, acsch(x), ~Q.extended_real(x)) is False
    assert ask_generated(Q.zero, acsch(x), Q.infinite(x)) is True
    assert ask_generated(Q.infinite, acsch(x), Q.zero(x)) is True
    # atanh(oo) = -I*pi/2
    assert ask_generated(Q.imaginary, atanh(x), Q.imaginary(x)) is True
    assert ask_generated(Q.imaginary, atanh(x), Q.finite(x) & ~Q.imaginary(x)) is False
    assert ask_generated(Q.imaginary, atanh(x), Q.extended_real(x)) is None
    # atanh(1) = oo, acoth(-1) = -oo
    one, minus_one = atanh(S.One, evaluate=False), acoth(S.NegativeOne, evaluate=False)
    assert ask_generated(Q.extended_positive, one) is True
    assert ask_generated(Q.infinite, one) is True
    assert ask_generated(Q.extended_negative, minus_one) is True
    assert ask_generated(Q.zero, minus_one) is False
def test_trigonometric_functions():
    # sin(oo) and cos(oo) are AccumBounds(-1, 1)
    assert ask_generated(Q.complex, sin(x), Q.extended_real(x)) is True
    assert ask_generated(Q.finite, cos(x), Q.extended_real(x)) is True
    assert ask_generated(Q.extended_real, sin(x), Q.extended_real(x)) is True
    assert ask_generated(Q.transcendental, cot(x), Q.algebraic(x) & ~Q.zero(x)) is True
    assert ask_generated(Q.transcendental, cot(x), Q.algebraic(x)) is None
    # sinc(oo) and sinc(-oo) are zero, sinc(oo*I) is oo
    assert ask_generated(Q.real, sinc(x), Q.extended_real(x)) is True
    assert ask_generated(Q.zero, sinc(x), Q.extended_real(x) & Q.infinite(x)) is True
    assert ask_generated(Q.zero, sinc(x), Q.infinite(x)) is None
    # tan(pi/2), cot(0), sec(pi/2) and csc(0) are zoo
    for f in (tan, cot, sec, csc):
        assert ask_generated(Q.real, f(x), Q.real(x)) is None
        # tan(oo), cot(oo), sec(oo) and csc(oo) are AccumBounds(-oo, oo)
        assert ask_generated(Q.extended_real, f(x), Q.extended_real(x)
                             & Q.infinite(x)) is True
    assert ask_generated(Q.real, tan(x), Q.algebraic(x) & Q.real(x)) is True
    assert ask_generated(Q.real, sec(x), Q.rational(x)) is True
    assert ask_generated(Q.real, cot(x), Q.rational(x)) is None
    assert ask_generated(Q.real, cot(x), Q.rational(x) & ~Q.zero(x)) is True
    assert ask_generated(Q.real, csc(x), Q.algebraic(x) & Q.real(x)
                         & ~Q.zero(x)) is True
    assert ask_generated(Q.imaginary, sec(x), Q.extended_real(x)) is False
    assert ask_generated(Q.imaginary, csc(x), Q.extended_real(x)) is False
    assert ask_generated(Q.zero, sec(x), Q.extended_real(x)) is False
    assert ask_generated(Q.zero, csc(x), Q.extended_real(x)) is False


def test_inverse_trigonometric_functions():
    assert ask_generated(Q.complex, asin(x), Q.complex(x)) is True
    assert ask_generated(Q.complex, acos(x), Q.complex(x)) is True
    # asin(oo) is -oo*I, acos(zoo) is zoo
    assert ask_generated(Q.real, asin(x), Q.infinite(x)) is False
    assert ask_generated(Q.extended_real, asin(x), ~Q.extended_real(x)) is False
    assert ask_generated(Q.extended_real, acos(x), Q.infinite(x)) is False
    assert ask_generated(Q.extended_real, acos(x), Q.real(x)) is None
    assert ask_generated(Q.zero, asin(x), ~Q.zero(x)) is False
    assert ask_generated(Q.zero, acos(x), Q.negative(x)) is False
    assert ask_generated(Q.zero, acos(x), Q.positive(x)) is None
    # atan(oo*I) is pi/2
    assert ask_generated(Q.positive, atan(x), ~Q.extended_positive(x)) is None
    assert ask_generated(Q.positive, atan(x), ~Q.extended_positive(x)
                         & Q.finite(x)) is False
    assert ask_generated(Q.negative, atan(x), ~Q.extended_negative(x)
                         & Q.finite(x)) is False
    # the real parts of asin, atan, acot and acsc are at most pi/2, acos(cos(2)) is 2
    for f in (asin, atan, acot, acsc):
        assert ask_generated(Q.prime, f(x)) is False
        assert ask_generated(Q.composite, f(x)) is False
    assert ask_generated(Q.prime, acos(x)) is None
    # asin(0) and atan(0) are zero, acos(1) is zero, acos(-1) is pi
    for f in (asin, acos, atan):
        assert ask_generated(Q.odd, f(x), Q.integer(x)) is False
        assert ask_generated(Q.prime, f(x), Q.algebraic(x)) is False
        assert ask_generated(Q.composite, f(x), Q.rational(x)) is False
        assert ask_generated(Q.even, f(x), Q.integer(x)) is None
    # acot(oo), acot(-oo), acot(zoo) and acot(oo*I) are zero
    assert ask_generated(Q.zero, acot(x), Q.infinite(x)) is True
    assert ask_generated(Q.zero, acot(x), Q.finite(x)) is False
    assert ask_generated(Q.positive, acot(x), ~Q.nonnegative(x)) is False
    assert ask_generated(Q.negative, acot(x), ~Q.negative(x)) is False
    assert ask_generated(Q.real, acot(x), Q.infinite(x)) is True
    # acot(oo + I) is zero, acot(1 + I) is not real
    assert ask_generated(Q.extended_nonzero, acot(x), ~Q.real(x)) is False
    # atan(oo + I) is pi/2, atan(1 + I) is not real
    assert ask_generated(Q.rational, atan(x), ~Q.real(x)) is False
    # asec(oo), asec(-oo), asec(zoo) and asec(oo*I) are pi/2
    assert ask_generated(Q.positive, asec(x), Q.infinite(x)) is True
    assert ask_generated(Q.nonnegative, asec(x), Q.integer(x) & ~Q.zero(x)) is True
    assert ask_generated(Q.positive, asec(x), Q.integer(x) & Q.negative(x)) is True
    assert ask_generated(Q.positive, asec(x), Q.integer(x) & Q.positive(x)) is None
    assert ask_generated(Q.zero, asec(x), Q.negative(x)) is False
    assert ask_generated(Q.negative, asec(x)) is False
    assert ask_generated(Q.extended_negative, asec(x)) is False
    assert ask_generated(Q.nonpositive, asec(x), ~Q.real(x)) is False
    assert ask_generated(Q.nonpositive, asec(x), Q.real(x)) is None
    assert ask_generated(Q.rational, asec(x), ~Q.real(x)) is False
    assert ask_generated(Q.rational, asec(x), Q.real(x)) is None
    assert ask_generated(Q.zero, acsc(x), Q.infinite(x)) is True
    assert ask_generated(Q.zero, acsc(x), Q.finite(x)) is False
    assert ask_generated(Q.positive, acsc(x), Q.integer(x) & Q.positive(x)) is True
    assert ask_generated(Q.negative, acsc(x), Q.integer(x) & Q.negative(x)) is True
    assert ask_generated(Q.real, acsc(x), Q.positive(x)) is None
    assert ask_generated(Q.real, acsc(x), Q.finite(x) & ~Q.real(x)) is False


def test_atan2():
    assert ask_generated(Q.real, atan2(x, y), Q.real(x) & Q.real(y)
                         & ~Q.zero(x)) is True
    assert ask_generated(Q.real, atan2(x, y), Q.real(x) & Q.extended_real(y)
                         & ~Q.zero(y)) is True
    # atan2(0, 0), atan2(oo, 0) and atan2(oo, -1) are nan
    assert ask_generated(Q.real, atan2(x, y), Q.real(x) & Q.real(y)) is None
    assert ask_generated(Q.real, atan2(x, y), Q.extended_real(x) & Q.extended_real(y)
                         & ~Q.zero(x) & ~Q.zero(y)) is None
    assert ask_generated(Q.real, atan2(x, y), Q.extended_real(x) & ~Q.zero(x)
                         & Q.real(y)) is None
    # atan2(oo, 1) is pi/2, atan2(y, oo) is 0, atan2(oo, -oo) is pi
    assert ask_generated(Q.real, atan2(x, y), Q.extended_real(x)
                         & Q.extended_positive(y)) is True
    assert ask_generated(Q.real, atan2(x, y), Q.extended_real(x) & Q.extended_real(y)
                         & Q.infinite(y)) is True
    # atan2(I, 0) is pi/2, atan2(0, I) and atan2(I, -oo) are zero,
    # atan2(I*sin(1), I*cos(1)) is 1
    assert ask_generated(Q.irrational, atan2(x, y), Q.imaginary(x) & Q.zero(y)) is True
    assert ask_generated(Q.zero, atan2(x, y), Q.zero(x) & Q.imaginary(y)) is True
    assert ask_generated(Q.zero, atan2(x, y), Q.imaginary(x) & Q.extended_real(y)
                         & Q.infinite(y)) is True
    assert ask_generated(Q.zero, atan2(x, y), Q.imaginary(x) & Q.imaginary(y)) is False
    assert ask_generated(Q.composite, atan2(x, y), Q.imaginary(x)
                         & Q.imaginary(y)) is False
    assert ask_generated(Q.integer, atan2(x, y), Q.imaginary(x) & Q.imaginary(y)) is None
    # atan2(1, 1 + I) is not real, atan2(1, -I) is nan
    assert ask_generated(Q.extended_real, atan2(x, y), Q.real(x) & ~Q.zero(x)
                         & Q.finite(y) & ~Q.real(y) & ~Q.imaginary(y)) is False
    assert ask_generated(Q.extended_real, atan2(x, y), Q.finite(x) & ~Q.real(x)
                         & ~Q.imaginary(x) & Q.real(y) & ~Q.zero(y)) is False
    assert ask_generated(Q.extended_real, atan2(x, y), Q.real(x) & ~Q.zero(x)
                         & Q.imaginary(y)) is None
    assert ask_generated(Q.positive, atan2(x, y), Q.positive(x) & Q.real(y)) is True
    assert ask_generated(Q.negative, atan2(x, y), Q.negative(x) & Q.real(y)) is True
    # atan2(1, oo) is zero
    assert ask_generated(Q.positive, atan2(x, y), Q.positive(x)
                         & Q.extended_real(y)) is None


def test_combinatorial_and_special_functions():
    assert ask_generated(Q.integer, factorial(x), Q.integer(x) & Q.nonnegative(x)) is True
    assert ask_generated(Q.real, factorial(x), Q.real(x) & ~Q.integer(x)) is True
    # factorial(oo) is oo
    assert ask_generated(Q.real, factorial(x), Q.noninteger(x)) is None
    assert ask_generated(Q.even, factorial2(x), Q.even(x) & Q.positive(x)) is True
    assert ask_generated(Q.odd, factorial2(x), Q.zero(x)) is True
    assert ask_generated(Q.even, factorial2(x), Q.odd(x)) is False
    assert ask_generated(Q.odd, subfactorial(x), Q.even(x) & Q.nonnegative(x)) is True
    assert ask_generated(Q.nonnegative, binomial(x, y), Q.integer(x) & Q.nonnegative(x)
                         & Q.integer(y)) is True
    assert ask_generated(Q.positive, catalan(x), Q.nonnegative(x)) is True
    assert ask_generated(Q.positive, totient(x), Q.integer(x) & Q.positive(x)) is True
    assert ask_generated(Q.prime, legendre_symbol(x, y),
                         Q.integer(x) & Q.prime(y) & Q.odd(y)) is False
    # legendre_symbol(1, 4) has no value
    assert ask_generated(Q.prime, legendre_symbol(x, y)) is None
    assert ask_generated(Q.real, gamma(x), Q.real(x) & ~Q.integer(x)) is True
    assert ask_generated(Q.real, gamma(x), Q.integer(x) & Q.nonpositive(x)) is False
    assert ask_generated(Q.real, loggamma(x), Q.negative(x)) is False
    assert ask_generated(Q.positive, erf(x), Q.extended_positive(x)) is True
    assert ask_generated(Q.nonnegative, binomial(x, y), Q.integer(x) & Q.even(y)) is True
    assert ask_generated(Q.nonnegative, binomial(x, y), Q.integer(x) & Q.integer(y)
                         & Q.negative(y)) is True
    assert ask_generated(Q.nonnegative, binomial(x, y), Q.integer(x) & Q.negative(x)
                         & Q.odd(y) & Q.positive(y)) is False
    # binomial(1/2, 1/2) is 1
    assert ask_generated(Q.integer, binomial(x, y), ~Q.integer(y)) is None
    # FallingFactorial(pi, 0) is 1
    assert ask_generated(Q.integer, FallingFactorial(x, y), Q.irrational(x)
                         & Q.integer(y) & Q.nonnegative(y)) is None
    assert ask_generated(Q.zero, genocchi(x), Q.zero(x)) is True
    assert ask_generated(Q.odd, genocchi(x), Q.zero(x)) is False
    assert ask_generated(Q.real, polygamma(x, y), Q.positive(x) & Q.positive(y)) is True
    assert ask_generated(Q.positive, polygamma(x, y), Q.odd(x) & Q.positive(x)
                         & Q.positive(y)) is True
    assert ask_generated(Q.positive, polygamma(x, y), Q.odd(x) & Q.positive(x)
                         & Q.negative(y) & ~Q.integer(y)) is True
    assert ask_generated(Q.negative, polygamma(x, y), Q.even(x) & Q.positive(x)
                         & Q.positive(y)) is True
    assert ask_generated(Q.positive, polygamma(3, x), Q.eq(x, S.Half)) is True
    # polygamma(1, -2) is zoo
    assert ask_generated(Q.positive, polygamma(x, y), Q.odd(x) & Q.positive(x)
                         & Q.real(y)) is None
    # polygamma(2, -3/10) is positive and polygamma(2, -7/10) is negative
    assert ask_generated(Q.negative, polygamma(x, y), Q.even(x) & Q.positive(x)
                         & Q.negative(y) & ~Q.integer(y)) is None
    assert ask_generated(Q.positive, polygamma(x, y), Q.positive(x) & Q.positive(y)
                         ) is None
    assert ask_generated(Q.zero, Integral(x, (y, 0, 1)), Q.zero(x)) is True
    assert ask_generated(Q.zero, Integral(x, (y, 0, 1))) is None
    assert ask_generated(Q.zero, erf(x), Q.zero(x)) is True
    assert ask_generated(Q.real, erf(x), Q.imaginary(x)) is False
    # erf has zeros which are not real
    assert ask_generated(Q.zero, erf(x), ~Q.zero(x)) is None
    assert ask_generated(Q.real, erfi(x), Q.zero(x)) is True
    assert ask_generated(Q.real, erfi(x), Q.imaginary(x)) is False
    assert ask_generated(Q.zero, erfc(x), Q.zero(x)) is False
    assert ask_generated(Q.real, erfc(x), Q.imaginary(x)) is False
    # erfc(oo) is zero
    assert ask_generated(Q.positive, erfc(x), Q.extended_real(x)) is None
    assert ask_generated(Q.infinite, erfcinv(x), Q.zero(x)) is True
    assert ask_generated(Q.zero, erf2(x, y), Q.zero(x) & Q.zero(y)) is True


def test_accumulation_bounds():
    r, t = symbols('r t', extended_real=True)
    assert ask_generated(Q.real, AccumulationBounds(r, t), Q.real(r) & Q.real(t)) is True
    assert ask_generated(Q.finite, AccumulationBounds(r, t), Q.real(r) & Q.real(t)) is True
    assert ask_generated(Q.real, AccumulationBounds(r, t), Q.real(r)) is None


def test_powers_of_e():
    def power(exponent):
        return Pow(E, exponent, evaluate=False)

    assert ask_generated(Q.positive, power(x), Q.real(x)) is True
    assert ask_generated(Q.zero, power(x), Q.negative_infinite(x)) is True
    assert ask_generated(Q.zero, power(x), Q.finite(x)) is False
    assert ask_generated(Q.transcendental, power(x), Q.algebraic(x) & ~Q.zero(x)) is True
    assert ask_generated(Q.integer, power(x), Q.zero(x)) is True
    assert ask_generated(Q.positive_infinite, power(x), Q.positive_infinite(x)) is True
    assert ask_generated(Q.transcendental, power(x), Q.algebraic(x)) is None
    assert ask_generated(Q.positive, power(x), Q.extended_real(x)) is None
    assert ask(Q.zero, power(x), Q.negative_infinite(x)) is None
    assert ask_generated(Q.transcendental, Pow(y, x, evaluate=False),
                         Q.algebraic(x) & ~Q.zero(x) & Q.transcendental(y)) is None


def test_commutative():
    c = Symbol('c', commutative=False)
    f = Function('f')
    assert ask_generated(Q.commutative, x) is True
    assert ask_generated(Q.commutative, x, ~Q.commutative(x)) is False
    assert ask_generated(Q.commutative, c) is False
    assert ask_generated(Q.commutative, S.NaN) is True
    assert ask_generated(Q.commutative, x + y) is True
    assert ask_generated(Q.commutative, x*y) is True
    assert ask_generated(Q.commutative, x**y) is True
    assert ask_generated(Q.commutative, log(x)) is True
    assert ask_generated(Q.commutative, log(c)) is False
    assert ask_generated(Q.complex, log(c)) is False
    assert ask_generated(Q.commutative, conjugate(c)) is False
    assert ask_generated(Q.commutative, transpose(c)) is False
    assert ask_generated(Q.commutative, adjoint(c)) is False
    # x may be zero or nan
    assert ask_generated(Q.commutative, x*c) is None
    assert ask_generated(Q.commutative, x + c) is None
    # exp(2*pi*I*c) is 1 if c is a projection
    assert ask_generated(Q.commutative, exp(c)) is None
    # Function('f', commutative=False)(x) is not commutative
    assert ask_generated(Q.commutative, f(x)) is None
    assert ask_generated(Q.commutative, Derivative(f(x), x)) is None
    assert ask_generated(Q.commutative, Derivative(x*y, x)) is True
    assert ask_generated(Q.commutative, Derivative(c, x)) is False
    assert ask_generated(Q.commutative, Subs(x*y, x, 1)) is True
    assert ask_generated(Q.commutative, Subs(c, x, 1)) is False


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
    # re(zoo), im(zoo) and re(oo*(1 + I)) are nan, re(oo*I) is zero
    assert ask_generated(Q.extended_real, re(x)) is None
    assert ask_generated(Q.extended_real, im(x)) is None
    assert ask_generated(Q.imaginary, re(x)) is None
    assert ask_generated(Q.imaginary, im(x)) is None
    assert ask_generated(Q.zero, re(x), ~Q.imaginary(x) & ~Q.zero(x)) is None
    assert ask_generated(Q.zero, im(x), ~Q.extended_real(x)) is None
    # sign(oo*I) is I
    assert ask_generated(Q.imaginary, sign(x), ~Q.imaginary(x)) is None
    # arg(0) and arg(zoo) are nan
    assert ask_generated(Q.real, arg(x)) is None
    assert ask_generated(Q.real, arg(x), Q.real(x)) is None
    assert ask_generated(Q.real, arg(x), ~Q.zero(x)) is None
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
