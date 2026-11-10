"""
This module contains query handlers responsible for calculus queries:
infinitesimal, finite, etc.
"""
from __future__ import annotations

from sympy.assumptions import Q
from sympy.assumptions.ask import _ask_recursive
from sympy.core import Expr
from sympy.core.numbers import (NegativeInfinity, GoldenRatio,
    Infinity, Exp1, ComplexInfinity, ImaginaryUnit, NaN, Number, Pi,
    TribonacciConstant)

from ..predicates.calculus import (FinitePredicate, InfinitePredicate,
    PositiveInfinitePredicate, NegativeInfinitePredicate)


# FinitePredicate


@FinitePredicate.register_many(Number, Pi, Exp1, GoldenRatio,
    TribonacciConstant, ImaginaryUnit)
def _(expr, assumptions):
    return True

@FinitePredicate.register_many(ComplexInfinity, Infinity, NegativeInfinity)
def _(expr, assumptions):
    return False

@FinitePredicate.register(NaN)
def _(expr, assumptions):
    return None


# InfinitePredicate


@InfinitePredicate.register(Expr)
def _(expr, assumptions):
    is_finite = _ask_recursive(Q.finite(expr), assumptions)
    if is_finite is None:
        return None
    return not is_finite


# PositiveInfinitePredicate


@PositiveInfinitePredicate.register(Infinity)
def _(expr, assumptions):
    return True


@PositiveInfinitePredicate.register_many(NegativeInfinity, ComplexInfinity)
def _(expr, assumptions):
    return False


@PositiveInfinitePredicate.register(Expr)
def _(expr, assumptions):
    if _ask_recursive(Q.complex(expr), assumptions) is True:
        return False
    if _ask_recursive(Q.finite(expr), assumptions) is True:
        return False


# NegativeInfinitePredicate


@NegativeInfinitePredicate.register(NegativeInfinity)
def _(expr, assumptions):
    return True


@NegativeInfinitePredicate.register_many(Infinity, ComplexInfinity)
def _(expr, assumptions):
    return False


@NegativeInfinitePredicate.register(Expr)
def _(expr, assumptions):
    if _ask_recursive(Q.complex(expr), assumptions) is True:
        return False
    if _ask_recursive(Q.finite(expr), assumptions) is True:
        return False
