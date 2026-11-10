"""
Rules for the sets of numbers an expression is in: ``Q.integer``,
``Q.rational``, ``Q.irrational``, ``Q.real``, ``Q.imaginary`` and others.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.functions.elementary.complexes import Abs

from .language import closed, f, for_all, x, y

RULES = (
    # --- Abs ---

    # The absolute value of an integer is an integer
    for_all((Abs,),
        closed(f(x), Q.integer)),

    # --- Add ---

    # The reals, the rationals and the integers are closed under addition
    for_all((Add,),
        closed(f(x, y), Q.real, Q.rational, Q.integer)),

    # An integer plus a number which is not an integer is not an integer
    #     the difference of two integers is an integer
    for_all((Add,),
        (Q.integer(x) & ~Q.integer(y)) >> ~Q.integer(f(x, y)),
        (~Q.integer(x) & Q.integer(y)) >> ~Q.integer(f(x, y))),

    # A rational number plus an irrational number is irrational
    #     the difference of two rational numbers is rational
    for_all((Add,),
        (Q.rational(x) & Q.irrational(y)) >> Q.irrational(f(x, y)),
        (Q.irrational(x) & Q.rational(y)) >> Q.irrational(f(x, y))),

    # --- Mul ---

    # The reals, the rationals and the integers are closed under
    # multiplication
    for_all((Mul,),
        closed(f(x, y), Q.real, Q.rational, Q.integer)),

    # A nonzero rational number times a number which is not rational is not
    # rational
    #     the quotient of two rational numbers is rational
    for_all((Mul,),
        (Q.rational(x) & ~Q.zero(x) & ~Q.rational(y)) >> ~Q.rational(f(x, y)),
        (~Q.rational(x) & Q.rational(y) & ~Q.zero(y)) >> ~Q.rational(f(x, y))),

    # A nonzero rational number times an irrational number is irrational
    for_all((Mul,),
        (Q.rational(x) & ~Q.zero(x) & Q.irrational(y)) >> Q.irrational(f(x, y)),
        (Q.irrational(x) & Q.rational(y) & ~Q.zero(y)) >> Q.irrational(f(x, y))),

    # A nonzero real number times an imaginary number is imaginary
    for_all((Mul,),
        (Q.real(x) & ~Q.zero(x) & Q.imaginary(y)) >> Q.imaginary(f(x, y)),
        (Q.imaginary(x) & Q.real(y) & ~Q.zero(y)) >> Q.imaginary(f(x, y))),
)
