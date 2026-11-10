"""
Rules for ``Q.finite``, ``Q.infinite`` and the predicates for the
infinities.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.core.add import Add
from sympy.core.expr import Expr
from sympy.core.mul import Mul
from sympy.core.power import Pow
from sympy.core.symbol import Symbol
from sympy.functions.elementary.complexes import sign
from sympy.functions.elementary.exponential import exp, log
from sympy.functions.elementary.trigonometric import cos, sin

from .language import base, closed, exponent, f, for_all, x, y

RULES = (
    # --- Symbol ---

    # A symbol which is not finite is infinite
    #     it stands for a number, and not for nan
    for_all((Symbol,),
        (Q.commutative(x) & ~Q.finite(x)) >> Q.infinite(x)),

    # --- any expression ---

    # A finite number is not infinite
    for_all((Expr,),
        Q.finite(x) >> ~Q.infinite(x),
        Q.finite(x) >> ~Q.positive_infinite(x),
        Q.finite(x) >> ~Q.negative_infinite(x)),

    # An extended positive number which is not finite is oo, an extended
    # negative one is -oo
    for_all((Expr,),
        (Q.extended_positive(x) & ~Q.finite(x)) >> Q.positive_infinite(x),
        (Q.extended_negative(x) & ~Q.finite(x)) >> Q.negative_infinite(x)),

    # --- Add ---

    # A sum of finite terms is finite
    for_all((Add,),
        closed(f(x, y), Q.finite)),

    # An infinite term plus a finite one is infinite
    #     the sum of the others is not finite either when it is nan
    for_all((Add,),
        (~Q.finite(x) & Q.finite(y)) >> Q.infinite(f(x, y)),
        (Q.finite(x) & Q.infinite(y)) >> Q.infinite(f(x, y))),

    # oo plus an extended real number other than -oo is oo
    #     oo - oo is nan and oo + I is not oo
    for_all((Add,),
        (Q.positive_infinite(x) & Q.extended_real(y) & ~Q.negative_infinite(y))
        >> Q.positive_infinite(f(x, y)),
        (Q.extended_real(x) & ~Q.negative_infinite(x) & Q.positive_infinite(y))
        >> Q.positive_infinite(f(x, y))),

    # -oo plus an extended real number other than oo is -oo
    #     oo - oo is nan and -oo + I is not -oo
    for_all((Add,),
        (Q.negative_infinite(x) & Q.extended_real(y) & ~Q.positive_infinite(y))
        >> Q.negative_infinite(f(x, y)),
        (Q.extended_real(x) & ~Q.positive_infinite(x) & Q.negative_infinite(y))
        >> Q.negative_infinite(f(x, y))),

    # A sum of extended real numbers other than oo is not oo
    for_all((Add,),
        (Q.extended_real(x) & ~Q.positive_infinite(x)
         & Q.extended_real(y) & ~Q.positive_infinite(y))
        >> ~Q.positive_infinite(f(x, y))),

    # A sum of extended real numbers other than -oo is not -oo
    for_all((Add,),
        (Q.extended_real(x) & ~Q.negative_infinite(x)
         & Q.extended_real(y) & ~Q.negative_infinite(y))
        >> ~Q.negative_infinite(f(x, y))),

    # --- Mul ---

    # A product of finite factors is finite
    for_all((Mul,),
        closed(f(x, y), Q.finite)),

    # A product which is a complex number has finite factors
    #     an infinite factor gives an infinite product, or nan with a zero
    #     factor
    for_all((Mul,),
        Q.complex(f(x, y)) >> (Q.finite(x) & Q.finite(y))),

    # An infinite factor times a nonzero one is infinite
    #     0*oo is nan
    #     the product of the others is neither finite nor zero when it is
    #     nan
    for_all((Mul,),
        (~Q.finite(x) & Q.infinite(y)) >> Q.infinite(f(x, y)),
        (~Q.finite(x) & Q.finite(y) & ~Q.zero(y)) >> Q.infinite(f(x, y)),
        (~Q.finite(x) & Q.extended_nonzero(y)) >> Q.infinite(f(x, y)),
        (~Q.zero(x) & Q.infinite(y)) >> Q.infinite(f(x, y))),

    # --- Pow ---

    # A power of finite numbers is finite if the base is not zero
    #     0**-1 is zoo and 0**I is nan
    for_all((Pow,),
        (Q.finite(base) & ~Q.zero(base) & Q.finite(exponent))
        >> Q.finite(f(base, exponent))),

    # A finite number to a power which is not negative is finite
    #     0**0 is 1
    for_all((Pow,),
        (Q.finite(base) & Q.nonnegative(exponent))
        >> Q.finite(f(base, exponent))),

    # Zero to a negative power is infinite
    #     0**-1 is zoo
    for_all((Pow,),
        (Q.zero(base) & Q.extended_negative(exponent))
        >> Q.infinite(f(base, exponent))),

    # An infinite number to a positive power is infinite
    #     oo**-1 is 0 and zoo**oo is nan
    for_all((Pow,),
        (~Q.finite(base) & Q.positive(exponent))
        >> Q.infinite(f(base, exponent))),

    # --- exp ---

    # The exponential of a finite number is finite
    for_all((exp,),
        Q.finite(x) >> Q.finite(f(x))),

    # exp(oo) is oo and exp(-oo) is 0
    #     exp(oo*I) and exp(zoo) are nan
    for_all((exp,),
        Q.positive_infinite(x) >> Q.positive_infinite(f(x)),
        Q.negative_infinite(x) >> Q.zero(f(x))),

    # --- log ---

    # The logarithm of a finite nonzero number is finite
    for_all((log,),
        (Q.finite(x) & ~Q.zero(x)) >> Q.finite(f(x))),

    # The logarithm of zero or of an infinite number is infinite
    #     log(0) is zoo
    for_all((log,),
        Q.zero(x) >> Q.infinite(f(x)),
        ~Q.finite(x) >> Q.infinite(f(x))),

    # log(oo) is oo
    for_all((log,),
        Q.positive_infinite(x) >> Q.positive_infinite(f(x))),

    # --- sin, cos ---

    # The sine and the cosine of a finite number are finite
    #     sin(oo*I) is oo*I and sin(zoo) is nan
    for_all((sin, cos),
        Q.finite(x) >> Q.finite(f(x))),

    # --- sign ---

    # A sign is finite
    for_all((sign,),
        Q.finite(f(x))),
)
