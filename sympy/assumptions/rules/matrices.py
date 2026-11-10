"""
Rules for the predicates about matrices.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.logic.boolalg import Equivalent
from sympy.matrices.expressions.matmul import MatMul

from .language import f, for_all, x, y

RULES = (
    # A product of square matrices is invertible exactly when each factor is
    #     its determinant is the product of the determinants of the factors
    for_all((MatMul,),
        (Q.square(x) & Q.square(y))
        >> Equivalent(Q.invertible(f(x, y)), Q.invertible(x) & Q.invertible(y))),
)
