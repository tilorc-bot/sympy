from __future__ import annotations

from itertools import combinations_with_replacement

from sympy.assumptions.ask import ask
from sympy.assumptions.ask_rules_generated import RULES
from sympy.assumptions.rule_engine import ask_by_rules
from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.core.numbers import I, Rational, nan, oo, pi, zoo
from sympy.core.singleton import S
from sympy.core.symbol import symbols
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.logic.boolalg import And

REAL = (S.Zero, S.One, S.NegativeOne, S(2), Rational(1, 2), sqrt(2), pi, oo, -oo, zoo,
        nan)
IMAGINARY = (S.Zero, I, -I, 2*I, sqrt(2)*I, zoo, nan)
FINITE = (S.Zero, S.One, S.NegativeOne, S(2), Rational(-1, 2), sqrt(2), pi, I, -I,
          2*I, zoo, nan)
SYMBOLS = symbols('x:3')
_truth: dict = {}


def truth(predicate, value):
    key = (predicate, value)
    if key not in _truth:
        _truth[key] = ask(predicate(value))
    return _truth[key]


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
                        known.append(predicate(symbol) if t else ~predicate(symbol))
            assumptions = And(*known)
            result = cls(*values)
            for predicate in predicates:
                answer = ask_by_rules(predicate, args, assumptions, RULES)
                if answer is not None:
                    assert truth(predicate, result) in (answer, None), (
                        predicate, cls, values, answer)


def test_sums_of_real_numbers():
    check(Add, REAL, (2, 3))


def test_sums_of_imaginary_numbers():
    check(Add, IMAGINARY, (2, 3))


def test_products_of_real_numbers():
    check(Mul, REAL, (2, 3))


def test_products_of_finite_numbers():
    check(Mul, FINITE, (2, 3))
