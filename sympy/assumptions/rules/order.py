"""
Rules for the sign of an expression: ``Q.positive``, ``Q.negative``,
``Q.zero`` and the predicates which are made of them.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.core.power import Pow
from sympy.functions.elementary.complexes import Abs
from sympy.logic.boolalg import Equivalent

from .language import base, closed, exponent, f, for_all, x, y

RULES = (
    # --- Abs ---

    # An absolute value is not negative
    #     it is oo, which is not a real number, for an infinite argument
    for_all((Abs,),
        Q.extended_nonnegative(f(x)),
        Q.finite(x) >> Q.nonnegative(f(x))),

    # An absolute value is zero only at zero
    for_all((Abs,),
        Equivalent(Q.zero(f(x)), Q.zero(x))),

    # --- Add ---

    # A sum of positive terms is positive, one of negative terms negative
    for_all((Add,),
        closed(f(x, y), Q.positive, Q.negative)),

    # --- Mul ---

    # A product of positive factors is positive
    for_all((Mul,),
        closed(f(x, y), Q.positive)),

    # A product is zero only if a factor is zero
    for_all((Mul,),
        Q.zero(f(x, y)) >> (Q.zero(x) | Q.zero(y))),

    # Zero times a finite number is zero
    #     0*oo is nan
    for_all((Mul,),
        (Q.zero(x) & Q.finite(y)) >> Q.zero(f(x, y)),
        (Q.finite(x) & Q.zero(y)) >> Q.zero(f(x, y))),

    # --- Pow ---

    # An even power of a real number is not negative
    for_all((Pow,),
        (Q.real(base) & Q.even(exponent) & Q.nonnegative(exponent))
        >> Q.nonnegative(f(base, exponent))),

    # An odd power keeps the sign of its base
    for_all((Pow,),
        (Q.nonnegative(base) & Q.odd(exponent) & Q.nonnegative(exponent))
        >> Q.nonnegative(f(base, exponent)),
        (Q.nonpositive(base) & Q.odd(exponent) & Q.nonnegative(exponent))
        >> Q.nonpositive(f(base, exponent))),

    # Zero to a positive power is zero
    for_all((Pow,),
        (Q.zero(base) & Q.positive(exponent)) >> Q.zero(f(base, exponent))),

    # A positive power is zero only if the base is zero
    #     a positive power of an infinite base is infinite
    for_all((Pow,),
        (Q.zero(f(base, exponent)) & Q.positive(exponent)) >> Q.zero(base)),

    # A power of finite numbers is zero only if the base is zero
    #     for another base it is exp(exponent*log(base)); oo**-1 is zero
    for_all((Pow,),
        (Q.zero(f(base, exponent)) & Q.finite(base) & Q.finite(exponent))
        >> Q.zero(base)),

    # A real power of a finite base is zero only if the exponent is positive
    #     0**0 is 1 and 0**-1 is zoo; 2**-oo is zero
    for_all((Pow,),
        (Q.zero(f(base, exponent)) & Q.finite(base) & Q.real(exponent))
        >> Q.positive(exponent)),
)
