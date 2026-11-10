"""
Handlers for keys related to number theory: prime, even, odd, etc.
"""
from __future__ import annotations

from sympy.assumptions import Q
from sympy.assumptions.ask import _ask_recursive
from sympy.core import Basic, Expr, Float
from sympy.core.numbers import (ImaginaryUnit, Infinity, Integer, NaN,
    NegativeInfinity, NumberSymbol, Rational, int_valued)
from sympy.ntheory import isprime

from sympy.multipledispatch import MDNotImplementedError

from ..predicates.ntheory import (PrimePredicate, CompositePredicate,
    EvenPredicate, OddPredicate)


# PrimePredicate

def _PrimePredicate_number(expr, assumptions):
    # helper method
    exact = not expr.atoms(Float)
    try:
        i = int(expr.round())
        if (expr - i).equals(0) is False:
            raise TypeError
    except TypeError:
        return False
    if exact:
        return isprime(i)
    # when not exact, we won't give a True or False
    # since the number represents an approximate value

@PrimePredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_prime
    if ret is None:
        raise MDNotImplementedError
    return ret

@PrimePredicate.register(Basic)
def _(expr, assumptions):
    if expr.is_number:
        return _PrimePredicate_number(expr, assumptions)

@PrimePredicate.register(Integer)
def _(expr, assumptions):
    return isprime(expr)

@PrimePredicate.register_many(Rational, Infinity, NegativeInfinity, ImaginaryUnit)
def _(expr, assumptions):
    return False

@PrimePredicate.register(Float)
def _(expr, assumptions):
    return _PrimePredicate_number(expr, assumptions)

@PrimePredicate.register(NumberSymbol)
def _(expr, assumptions):
    return _PrimePredicate_number(expr, assumptions)

@PrimePredicate.register(NaN)
def _(expr, assumptions):
    return None


# CompositePredicate

@CompositePredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_composite
    if ret is None:
        raise MDNotImplementedError
    return ret

@CompositePredicate.register(Basic)
def _(expr, assumptions):
    _positive = _ask_recursive(Q.positive(expr), assumptions)
    if _positive:
        _integer = _ask_recursive(Q.integer(expr), assumptions)
        if _integer:
            _prime = _ask_recursive(Q.prime(expr), assumptions)
            if _prime is None:
                return
            # Positive integer which is not prime is not
            # necessarily composite
            _is_one = _ask_recursive(Q.eq(expr, 1), assumptions)
            if _is_one:
                return False
            if _is_one is None:
                return None
            return not _prime
        else:
            return _integer
    else:
        return _positive


# EvenPredicate

def _EvenPredicate_number(expr, assumptions):
    # helper method
    if isinstance(expr, (float, Float)):
        if int_valued(expr):
            return None
        return False
    try:
        i = int(expr.round())
    except TypeError:
        return False
    if not (expr - i).equals(0):
        return False
    return i % 2 == 0

@EvenPredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_even
    if ret is None:
        raise MDNotImplementedError
    return ret

@EvenPredicate.register(Basic)
def _(expr, assumptions):
    if expr.is_number:
        return _EvenPredicate_number(expr, assumptions)

@EvenPredicate.register(Integer)
def _(expr, assumptions):
    return not bool(expr.p & 1)

@EvenPredicate.register_many(Rational, Infinity, NegativeInfinity, ImaginaryUnit)
def _(expr, assumptions):
    return False

@EvenPredicate.register(NumberSymbol)
def _(expr, assumptions):
    return _EvenPredicate_number(expr, assumptions)

@EvenPredicate.register(NaN)
def _(expr, assumptions):
    return None


# OddPredicate

@OddPredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_odd
    if ret is None:
        raise MDNotImplementedError
    return ret

@OddPredicate.register(Basic)
def _(expr, assumptions):
    _integer = _ask_recursive(Q.integer(expr), assumptions)
    if _integer:
        _even = _ask_recursive(Q.even(expr), assumptions)
        if _even is None:
            return None
        return not _even
    return _integer
