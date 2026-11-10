"""
Rules for ``Q.commutative``.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.core.mul import Mul

from .language import closed, f, for_all, x, y

RULES = (
    # A product of commutative factors is commutative
    for_all((Mul,),
        closed(f(x, y), Q.commutative)),
)
