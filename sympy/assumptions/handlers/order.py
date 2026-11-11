"""
Handlers related to order relations: positive, negative, etc.
"""
from __future__ import annotations

from sympy.assumptions import Q
from sympy.assumptions.ask import _ask_recursive
from sympy.matrices import Determinant, Trace
from sympy.matrices.expressions.matexpr import MatrixElement

from ..predicates.order import PositivePredicate


# PositivePredicate

@PositivePredicate.register(Trace)
def _(expr, assumptions):
    if _ask_recursive(Q.positive_definite(expr.arg), assumptions):
        return True

@PositivePredicate.register(Determinant)
def _(expr, assumptions):
    if _ask_recursive(Q.positive_definite(expr.arg), assumptions):
        return True

@PositivePredicate.register(MatrixElement)
def _(expr, assumptions):
    if (expr.i == expr.j
            and _ask_recursive(Q.positive_definite(expr.parent), assumptions)):
        return True
