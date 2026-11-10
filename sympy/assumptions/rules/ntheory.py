"""
Rules for the number theoretic predicates: ``Q.even``, ``Q.odd``,
``Q.prime`` and ``Q.composite``.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.core.add import Add
from sympy.core.basic import Basic
from sympy.core.mul import Mul
from sympy.core.power import Pow
from sympy.functions.elementary.complexes import Abs, im, re
from sympy.logic.boolalg import Equivalent

from .language import base, closed, exponent, f, for_all, x, y

RULES = (
    # --- any expression ---

    # An integer is odd exactly when it is not even
    for_all((Basic,),
        (Q.integer(x) & ~Q.even(x)) >> Q.odd(x),
        ~Q.integer(x) >> ~Q.odd(x)),

    # A composite number is a positive integer which is not prime
    #     1 is neither, but it is not even
    for_all((Basic,),
        ~Q.positive(x) >> ~Q.composite(x),
        ~Q.integer(x) >> ~Q.composite(x),
        Q.prime(x) >> ~Q.composite(x),
        (Q.even(x) & Q.positive(x) & ~Q.prime(x)) >> Q.composite(x)),

    # --- Abs, re ---

    # The absolute value and the real part of an integer have its parity
    for_all((Abs, re),
        closed(f(x), Q.even, Q.odd)),

    # The absolute value and the real part of a real number are even only if
    # it is even
    #     abs(2*I) is 2 and re(2*I) is 0
    for_all((Abs, re),
        (Q.real(x) & ~Q.even(x)) >> ~Q.even(f(x))),

    # --- im ---

    # The imaginary part of a real number is 0, which is even
    for_all((im,),
        Q.real(x) >> Q.even(f(x))),

    # --- Add ---

    # Parity of a sum
    #     x is the first term and y the sum of the others
    for_all((Add,),
        (Q.even(x) & Q.even(y)) >> Q.even(f(x, y)),
        (Q.odd(x) & Q.odd(y)) >> Q.even(f(x, y)),
        (Q.even(x) & Q.odd(y)) >> Q.odd(f(x, y)),
        (Q.odd(x) & Q.even(y)) >> Q.odd(f(x, y))),

    # --- Mul ---

    # An even number times an integer is even
    for_all((Mul,),
        (Q.even(x) & Q.integer(y)) >> Q.even(f(x, y)),
        (Q.integer(x) & Q.even(y)) >> Q.even(f(x, y))),

    # A product of odd numbers is odd
    for_all((Mul,),
        closed(f(x, y), Q.odd)),

    # A product of integers is even exactly when one of them is even
    for_all((Mul,),
        (Q.integer(x) & Q.integer(y))
        >> Equivalent(Q.even(f(x, y)), Q.even(x) | Q.even(y))),

    # A composite number times an integer is not prime
    #     a prime has no divisor greater than 1 but itself
    for_all((Mul,),
        (Q.composite(x) & Q.integer(y)) >> ~Q.prime(f(x, y)),
        (Q.integer(x) & Q.composite(y)) >> ~Q.prime(f(x, y))),

    # A product of primes and composite numbers is composite
    #     every factor is at least 2
    for_all((Mul,),
        (Q.prime(x) & Q.prime(y)) >> Q.composite(f(x, y)),
        (Q.prime(x) & Q.composite(y)) >> Q.composite(f(x, y)),
        (Q.composite(x) & Q.prime(y)) >> Q.composite(f(x, y)),
        (Q.composite(x) & Q.composite(y)) >> Q.composite(f(x, y))),

    # --- Pow ---

    # A positive power of an even number is even
    for_all((Pow,),
        (Q.even(base) & Q.integer(exponent) & Q.positive(exponent))
        >> Q.even(f(base, exponent))),

    # A nonnegative power of an odd number is odd
    #     n**0 is 1
    for_all((Pow,),
        (Q.odd(base) & Q.integer(exponent) & ~Q.negative(exponent))
        >> Q.odd(f(base, exponent))),

    # A power of -1 is odd
    #     it is 1 or -1
    for_all((Pow,),
        (Q.eq(base, -1) & Q.integer(exponent)) >> Q.odd(f(base, exponent))),

    # One to a finite power is odd
    #     it is 1, and 1**oo is nan
    for_all((Pow,),
        (Q.eq(base, 1) & Q.finite(exponent)) >> Q.odd(f(base, exponent))),

    # A prime to the power 1 is prime
    #     1 is the positive integer which is neither prime nor composite
    for_all((Pow,),
        (Q.prime(base) & Q.integer(exponent) & Q.positive(exponent)
         & ~Q.prime(exponent) & ~Q.composite(exponent))
        >> Q.prime(f(base, exponent))),

    # A power of an integer which is not prime is not prime
    #     a power of -p is -p or a power of p
    for_all((Pow,),
        (Q.integer(base) & ~Q.prime(base) & Q.integer(exponent))
        >> ~Q.prime(f(base, exponent))),

    # A power of an integer is prime only for the exponent 1
    #     n**0 is 1, and n**-k is an integer only for n = 1 and n = -1
    for_all((Pow,),
        (Q.integer(base) & Q.integer(exponent) & ~Q.positive(exponent))
        >> ~Q.prime(f(base, exponent)),
        (Q.integer(base) & Q.prime(exponent)) >> ~Q.prime(f(base, exponent)),
        (Q.integer(base) & Q.composite(exponent))
        >> ~Q.prime(f(base, exponent)),
        (Q.integer(base) & Q.integer(exponent) & Q.ne(exponent, 1))
        >> ~Q.prime(f(base, exponent))),
)
