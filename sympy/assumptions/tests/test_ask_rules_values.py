from __future__ import annotations

from itertools import combinations_with_replacement, product

from sympy.assumptions.ask import Q, ask
from sympy.assumptions.ask_rules_generated import RULES
from sympy.assumptions.assume import Predicate
from sympy.assumptions.rule_engine import ask_by_rules
from sympy.core.add import Add
from sympy.core.mod import Mod
from sympy.core.mul import Mul
from sympy.core.numbers import E, I, Rational, nan, oo, pi, zoo
from sympy.core.power import Pow
from sympy.core.singleton import S
from sympy.core.symbol import symbols
from sympy.functions.combinatorial.factorials import (FallingFactorial,
    RisingFactorial, binomial, factorial, factorial2, subfactorial)
from sympy.functions.combinatorial.numbers import (andre, catalan, genocchi, mobius,
    partition, primenu, primeomega, primepi, reduced_totient, totient)
from sympy.functions.elementary.complexes import Abs, re, sign
from sympy.functions.elementary.exponential import LambertW, exp, exp_polar, log
from sympy.functions.elementary.hyperbolic import (asinh, cosh, coth, csch, sech, sinh,
    tanh)
from sympy.functions.elementary.integers import ceiling, floor, frac
from sympy.functions.elementary.miscellaneous import Max, Min, sqrt
from sympy.functions.elementary.trigonometric import (acos, acot, acsc, asec, asin,
    atan, atan2, cos, cot, csc, sec, sin, sinc, tan)
from sympy.functions.special.bessel import (airyai, besseli, besselj, besselk,
    bessely)
from sympy.functions.special.error_functions import (erf, erf2, erfc, fresnelc,
    fresnels, owens_t)
from sympy.functions.special.gamma_functions import gamma, loggamma, polygamma
from sympy.functions.elementary.trigonometric import (acot, asec, atan, cot, csc, sec,
    sinc, tan)
from sympy.functions.special.bessel import (airyai, airyaiprime, airybi,
    airybiprime, besseli, besselj, besselk, bessely, marcumq)
from sympy.functions.special.beta_functions import beta
from sympy.functions.special.elliptic_integrals import elliptic_f, elliptic_k
from sympy.functions.special.error_functions import (Shi, Si, erf, erf2, erf2inv, erfc,
    erfi, fresnelc, fresnels, li, owens_t)
from sympy.functions.special.gamma_functions import (gamma, loggamma, lowergamma,
    polygamma)
from sympy.functions.special.zeta_functions import polylog
from sympy.functions.special.tensor_functions import KroneckerDelta
from sympy.logic.boolalg import And

REAL = (S.Zero, S.One, S.NegativeOne, S(2), Rational(1, 2), sqrt(2), pi, oo, -oo, zoo,
        nan)
IMAGINARY = (S.Zero, I, -I, 2*I, sqrt(2)*I, zoo, nan)
FINITE = (S.Zero, S.One, S.NegativeOne, S(2), Rational(-1, 2), sqrt(2), pi, I, -I,
          2*I, zoo, nan)
EXTENDED_REAL = (S.Zero, S.One, S.NegativeOne, S(2), Rational(1, 2), Rational(-1, 2),
                 sqrt(2), pi, oo, -oo)
COMPLEX = EXTENDED_REAL + (zoo, nan, I, -I, 2*I)
INTEGERS = (S.Zero, S.One, S(2), S(3), S(4), S(5), S.NegativeOne, S(-3), S(-5))
POSITIVE_INTEGERS = (S.One, S(2), S(3), S(4), S(6), S(12))
POWERS = (S.Zero, S.One, S.NegativeOne, S(2), S(-2), Rational(1, 2), Rational(-1, 2),
          sqrt(2), pi, oo, nan, I, -I, 2*I)
PAIRS = (S.Zero, S.One, S.NegativeOne, S(2), S(-3), Rational(1, 2), pi, oo, I)
SIGNED = (S.Zero, S.One, S.NegativeOne, oo, -oo)
# (predicate, whether it is true)
SIGNS = ((Q.zero, True), (Q.zero, False), (Q.positive, True), (Q.negative, True),
         (Q.nonnegative, True), (Q.nonpositive, True), (Q.extended_nonnegative, True),
         (Q.extended_nonpositive, True))
SYMBOLS = symbols('x:3')
_truth: dict = {}


def truth(predicate, value):
    key = (predicate, value)
    if key not in _truth:
        if isinstance(predicate, Predicate):
            _truth[key] = ask(predicate(value))
        else:
            _truth[key] = value == predicate
    return _truth[key]


def literal(predicate, symbol, is_true):
    if isinstance(predicate, Predicate):
        return predicate(symbol) if is_true else ~predicate(symbol)
    return Q.eq(symbol, predicate) if is_true else Q.ne(symbol, predicate)


def check(cls, pool, sizes):
    predicates = sorted({p for c, p in RULES if c is cls}, key=str)
    for size in sizes:
        args = cls(*SYMBOLS[:size])
        for values in combinations_with_replacement(pool, size):
            known = []
            for symbol, value in zip(SYMBOLS, values):
                for predicate in predicates:
                    t = truth(predicate, value)
                    if t is not None:
                        known.append(literal(predicate, symbol, t))
            assumptions = And(*known)
            result = cls(*values)
            for predicate in predicates:
                answer = ask_by_rules(predicate, args, assumptions, RULES)
                if answer is not None:
                    assert truth(predicate, result) in (answer, None), (
                        predicate, cls, values, answer)


def check_told_one_fact(cls, pool, sizes, facts):
    """As ``check``, with only one of *facts* told of each argument, in every way."""
    predicates = sorted({p for c, p in RULES if c is cls}, key=str)
    for size in sizes:
        args = cls(*SYMBOLS[:size])
        for values in combinations_with_replacement(pool, size):
            result = cls(*values)
            known = [[literal(p, symbol, t) for p, t in facts if truth(p, value) is t]
                     for symbol, value in zip(SYMBOLS, values)]
            for told in product(*known):
                assumptions = And(*told)
                for predicate in predicates:
                    answer = ask_by_rules(predicate, args, assumptions, RULES)
                    if answer is not None:
                        assert truth(predicate, result) in (answer, None), (
                            predicate, cls, values, told, answer)


def test_sums_of_real_numbers():
    check(Add, REAL, (2, 3))


def test_sums_of_imaginary_numbers():
    check(Add, IMAGINARY, (2, 3))


def test_products_of_real_numbers():
    check(Mul, REAL, (2, 3))


def test_products_of_finite_numbers():
    check(Mul, FINITE, (2, 3))


def test_products_told_one_fact_of_each_factor():
    check_told_one_fact(Mul, SIGNED, (2, 3), SIGNS)


def test_powers():
    check(Pow, POWERS, (2,))
    check(Pow, POWERS[::-1], (2,))
    check(Pow, (zoo, S.Zero, S(2), Rational(-1, 2), I), (2,))


def test_powers_of_e_have_the_answers_of_exp():
    predicates = sorted({p for c, p in RULES if c is exp}, key=str)
    x = SYMBOLS[0]
    power = Pow(E, x, evaluate=False)
    for value in COMPLEX:
        known = And(*(literal(p, x, t) for p in predicates
                      if (t := truth(p, value)) is not None))
        for predicate in predicates:
            answer = ask_by_rules(predicate, exp(x), known, RULES)
            if answer is not None:
                assert ask_by_rules(predicate, power, known, RULES) is answer


def test_minimum_and_maximum():
    check(Max, EXTENDED_REAL, (2, 3))
    check(Min, EXTENDED_REAL, (2, 3))


def test_functions_of_one_argument():
    for cls in (Abs, re, sign, exp_polar, sinh, cosh, tanh, coth, sech, csch, asinh,
                floor, ceiling, frac, sin, cos, cot, tan, sec, csc, sinc, LambertW, factorial,
                gamma, loggamma, erf, fresnels, fresnelc, airyai):
        check(cls, COMPLEX, (1,))
    # ask raises AttributeError for erfc(-I)
    check(erfc, EXTENDED_REAL + (zoo, nan, I, 2*I), (1,))
    for cls in (atan, acot):
        check(cls, EXTENDED_REAL + (zoo, nan), (1,))
    # ask raises for asec(-1/2)
    for cls in (asec, acsc):
        check(cls, EXTENDED_REAL[:4] + EXTENDED_REAL[6:] + (zoo, nan), (1,))
    # ask raises for asin(oo), asin(sqrt(2)) and acos(I)
    for cls in (asin, acos):
        check(cls, EXTENDED_REAL[:6] + (zoo, nan), (1,))
    check(log, EXTENDED_REAL[:5] + EXTENDED_REAL[6:] + (zoo, nan, I, -I), (1,))


def test_functions_of_integers():
    for cls in (factorial2, subfactorial, catalan, andre, partition, primepi, genocchi):
        check(cls, INTEGERS, (1,))
    for cls in (mobius, totient, reduced_totient, primenu, primeomega):
        check(cls, POSITIVE_INTEGERS, (1,))


def test_functions_of_two_arguments():
    for cls in (binomial, RisingFactorial, FallingFactorial, besselj, besseli, besselk,
                bessely, owens_t, polygamma):
        check(cls, PAIRS, (2,))
        check(cls, PAIRS[::-1], (2,))
    check(Mod, PAIRS[1:], (2,))
    check(Mod, PAIRS[:0:-1], (2,))
    check(erf2, (S.Zero, S.One, S.NegativeOne, oo, -oo), (2,))
    check(KroneckerDelta, (S.Zero, S.One, S(2), Rational(1, 2), I), (2,))
    check(atan2, PAIRS + (-oo,), (2,))
    check(atan2, (-oo,) + PAIRS[::-1], (2,))


def test_special_functions():
    for cls in (erfi, li, Si, Shi, elliptic_k, airybi, airyaiprime, airybiprime):
        check(cls, COMPLEX, (1,))
    for cls in (beta, erf2inv, polylog, elliptic_f, lowergamma):
        check(cls, PAIRS, (2,))
        check(cls, PAIRS[::-1], (2,))
    check(marcumq, (S.Zero, S.One, S(2), oo), (3,))
