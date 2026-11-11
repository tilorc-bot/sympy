"""What a number is, from its class and its value, without the old assumptions."""
from __future__ import annotations

from typing import TYPE_CHECKING

from mpmath.libmp import mpf_sign

from sympy.assumptions.ask import Q
from sympy.core.numbers import (Catalan, ComplexInfinity, EulerGamma, Exp1, Float,
    GoldenRatio, ImaginaryUnit, Infinity, Integer, NegativeInfinity, Pi, Rational,
    TribonacciConstant, int_valued)
from sympy.ntheory.primetest import isprime

if TYPE_CHECKING:
    from sympy.assumptions.assume import Predicate
    from sympy.core.basic import Basic

    Facts = list[tuple[Predicate, bool]]

_ZERO: Facts = [(Q.zero, True), (Q.antihermitian, True)]
_CONSTANTS: dict[type, Facts] = {
    Pi: [(Q.positive, True), (Q.irrational, True), (Q.transcendental, True)],
    Exp1: [(Q.positive, True), (Q.irrational, True), (Q.transcendental, True)],
    GoldenRatio: [(Q.positive, True), (Q.irrational, True), (Q.algebraic, True)],
    TribonacciConstant: [(Q.positive, True), (Q.irrational, True), (Q.algebraic, True)],
    EulerGamma: [(Q.positive, True)],
    Catalan: [(Q.positive, True)],
    ImaginaryUnit: [(Q.imaginary, True), (Q.algebraic, True)],
    Infinity: [(Q.positive_infinite, True)],
    NegativeInfinity: [(Q.negative_infinite, True)],
    ComplexInfinity: [(Q.infinite, True), (Q.extended_real, False)],
}


def number_facts(expr: Basic) -> Facts | None:
    """
    A few predicates of the number *expr*, true or false, which decide the
    others through the known facts between predicates. ``None`` if *expr* is
    not a number which this knows.
    """
    facts = _CONSTANTS.get(type(expr))
    if facts is not None:
        return facts
    if isinstance(expr, Integer):
        return _integer_facts(expr.p)
    if isinstance(expr, Rational):
        return [(Q.positive if expr.p > 0 else Q.negative, True),
                (Q.rational, True), (Q.integer, False)]
    if isinstance(expr, Float):
        sign = mpf_sign(expr._mpf_)
        if sign == 0:
            return _ZERO
        facts = [(Q.positive if sign > 0 else Q.negative, True)]
        if not int_valued(expr):
            facts.append((Q.integer, False))
        return facts
    return None


def _integer_facts(n: int) -> Facts:
    if n == 0:
        return _ZERO
    facts = [(Q.positive if n > 0 else Q.negative, True),
             (Q.even if n % 2 == 0 else Q.odd, True)]
    if n > 1:
        facts.append((Q.prime if isprime(n) else Q.composite, True))
    else:
        facts += [(Q.prime, False), (Q.composite, False)]
    return facts
