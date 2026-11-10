"""
Rules for the number theoretic predicates: ``Q.even``, ``Q.odd``,
``Q.prime`` and ``Q.composite``.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.core.mul import Mul
from sympy.functions.elementary.complexes import Abs
from sympy.logic.boolalg import Equivalent

from .language import closed, f, for_all, x, y

RULES = (
    # --- Abs ---

    # The absolute value of an integer has the parity of the integer
    for_all((Abs,),
        closed(f(x), Q.even, Q.odd)),

    # --- Mul ---

    # A product of integers is even exactly when one of them is even
    for_all((Mul,),
        (Q.integer(x) & Q.integer(y))
        >> Equivalent(Q.even(f(x, y)), Q.even(x) | Q.even(y))),

    # A prime times a prime or a composite number is composite
    #     both factors are at least 2
    for_all((Mul,),
        (Q.prime(x) & Q.prime(y)) >> Q.composite(f(x, y)),
        (Q.prime(x) & Q.composite(y)) >> Q.composite(f(x, y))),
)
