"""
Handlers related to order relations: positive, negative, etc.
"""
from __future__ import annotations

from sympy.assumptions import Q
from sympy.assumptions.ask import _ask_recursive
from sympy.core import Basic, Expr, S
from sympy.core.logic import fuzzy_not, fuzzy_and, fuzzy_or
from sympy.core.numbers import ImaginaryUnit, NaN

from sympy.multipledispatch import MDNotImplementedError

from ..predicates.order import (NegativePredicate, NonNegativePredicate,
    NonZeroPredicate, ZeroPredicate, NonPositivePredicate, PositivePredicate,
    ExtendedNegativePredicate, ExtendedNonNegativePredicate,
    ExtendedNonPositivePredicate, ExtendedNonZeroPredicate,
    ExtendedPositivePredicate,)


# NegativePredicate

def _NegativePredicate_number(expr, assumptions):
    r, i = expr.as_real_imag()

    if r == S.NaN or i == S.NaN:
        return None

    # If the imaginary part can symbolically be shown to be zero then
    # we just evaluate the real part; otherwise we evaluate the imaginary
    # part to see if it actually evaluates to zero and if it does then
    # we make the comparison between the real part and zero.
    if not i:
        r = r.evalf(2)
        if r._prec != 1:
            return r < 0
    else:
        i = i.evalf(2)
        if i._prec != 1:
            if i != 0:
                return False
            r = r.evalf(2)
            if r._prec != 1:
                return r < 0

@NegativePredicate.register(Basic)
def _(expr, assumptions):
    if expr.is_number:
        return _NegativePredicate_number(expr, assumptions)

@NegativePredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_negative
    if ret is None:
        raise MDNotImplementedError
    return ret

@NegativePredicate.register(ImaginaryUnit)
def _(expr, assumptions):
    return False


# NonNegativePredicate

@NonNegativePredicate.register(Basic)
def _(expr, assumptions):
    if expr.is_number:
        notnegative = fuzzy_not(_NegativePredicate_number(expr, assumptions))
        if notnegative:
            return _ask_recursive(Q.real(expr), assumptions)
        else:
            return notnegative

@NonNegativePredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_nonnegative
    if ret is None:
        raise MDNotImplementedError
    return ret


# NonZeroPredicate

@NonZeroPredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_nonzero
    if ret is None:
        raise MDNotImplementedError
    return ret

@NonZeroPredicate.register(Basic)
def _(expr, assumptions):
    if _ask_recursive(Q.real(expr), assumptions) is False:
        return False
    if expr.is_number:
        # if there are no symbols just evalf
        i = expr.evalf(2)
        def nonz(i):
            if i._prec != 1:
                return i != 0
        return fuzzy_or(nonz(i) for i in i.as_real_imag())

@NonZeroPredicate.register(NaN)
def _(expr, assumptions):
    return None


# ZeroPredicate

@ZeroPredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_zero
    if ret is None:
        raise MDNotImplementedError
    return ret

@ZeroPredicate.register(Basic)
def _(expr, assumptions):
    return fuzzy_and([fuzzy_not(_ask_recursive(Q.nonzero(expr), assumptions)),
        _ask_recursive(Q.real(expr), assumptions)])


# NonPositivePredicate

@NonPositivePredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_nonpositive
    if ret is None:
        raise MDNotImplementedError
    return ret

@NonPositivePredicate.register(Basic)
def _(expr, assumptions):
    if expr.is_number:
        notpositive = fuzzy_not(_PositivePredicate_number(expr, assumptions))
        if notpositive:
            return _ask_recursive(Q.real(expr), assumptions)
        else:
            return notpositive


# PositivePredicate

def _PositivePredicate_number(expr, assumptions):
    r, i = expr.as_real_imag()
    # If the imaginary part can symbolically be shown to be zero then
    # we just evaluate the real part; otherwise we evaluate the imaginary
    # part to see if it actually evaluates to zero and if it does then
    # we make the comparison between the real part and zero.
    if not i:
        r = r.evalf(2)
        if r._prec != 1:
            return r > 0
    else:
        i = i.evalf(2)
        if i._prec != 1:
            if i != 0:
                return False
            r = r.evalf(2)
            if r._prec != 1:
                return r > 0

@PositivePredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_positive
    if ret is None:
        raise MDNotImplementedError
    return ret

@PositivePredicate.register(Basic)
def _(expr, assumptions):
    if expr.is_number:
        return _PositivePredicate_number(expr, assumptions)

@PositivePredicate.register(ImaginaryUnit)
def _(expr, assumptions):
    return False

@PositivePredicate.register(NaN)
def _(expr, assumptions):
    return None


# ExtendedNegativePredicate

@ExtendedNegativePredicate.register(object)
def _(expr, assumptions):
    return _ask_recursive(Q.negative(expr) | Q.negative_infinite(expr), assumptions)


# ExtendedPositivePredicate

@ExtendedPositivePredicate.register(object)
def _(expr, assumptions):
    return _ask_recursive(Q.positive(expr) | Q.positive_infinite(expr), assumptions)


# ExtendedNonZeroPredicate

@ExtendedNonZeroPredicate.register(object)
def _(expr, assumptions):
    return _ask_recursive(
        Q.negative_infinite(expr) | Q.negative(expr) | Q.positive(expr) | Q.positive_infinite(expr),
        assumptions)


# ExtendedNonPositivePredicate

@ExtendedNonPositivePredicate.register(object)
def _(expr, assumptions):
    return _ask_recursive(
        Q.negative_infinite(expr) | Q.negative(expr) | Q.zero(expr),
        assumptions)


# ExtendedNonNegativePredicate

@ExtendedNonNegativePredicate.register(object)
def _(expr, assumptions):
    return _ask_recursive(
        Q.zero(expr) | Q.positive(expr) | Q.positive_infinite(expr),
        assumptions)
