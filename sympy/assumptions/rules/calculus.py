"""
Rules for ``Q.finite``, ``Q.infinite`` and the predicates for the
infinities.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.core.mul import Mul

from .language import f, for_all, x, y

RULES = (
    # A product which is a complex number has finite factors
    #     an infinite factor gives an infinite product, or nan with a zero
    #     factor
    for_all((Mul,),
        Q.complex(f(x, y)) >> (Q.finite(x) & Q.finite(y))),
)
