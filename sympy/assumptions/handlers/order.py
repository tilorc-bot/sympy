"""
Handlers related to order relations: positive, negative, etc.
"""
from __future__ import annotations

from sympy.assumptions import Q
from sympy.assumptions.ask import _ask_recursive
from sympy.core import Expr, Pow
from sympy.core.numbers import E, I, pi
from sympy.functions import acos, asin, exp, log
from sympy.matrices import Determinant, Trace
from sympy.matrices.expressions.matexpr import MatrixElement

from sympy.multipledispatch import MDNotImplementedError

from ..predicates.order import (NegativePredicate, NonNegativePredicate,
    NonZeroPredicate, ZeroPredicate, NonPositivePredicate, PositivePredicate)


# NegativePredicate

@NegativePredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_negative
    if ret is None:
        raise MDNotImplementedError
    return ret


# NonNegativePredicate


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


# ZeroPredicate

@ZeroPredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_zero
    if ret is None:
        raise MDNotImplementedError
    return ret


# NonPositivePredicate

@NonPositivePredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_nonpositive
    if ret is None:
        raise MDNotImplementedError
    return ret


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


@PositivePredicate.register(Pow)
def _(expr, assumptions):
    if expr.base == E:
        if _ask_recursive(Q.real(expr.exp), assumptions):
            return True
        if _ask_recursive(Q.imaginary(expr.exp), assumptions):
            return _ask_recursive(Q.even(expr.exp/(I*pi)), assumptions)
        return

    if expr.is_number:
        return _PositivePredicate_number(expr, assumptions)
    if _ask_recursive(Q.even(expr.exp), assumptions) and _ask_recursive(Q.real(expr.base), assumptions):
        zero_base = _ask_recursive(Q.zero(expr.base), assumptions)
        if zero_base and _ask_recursive(Q.positive(expr.exp), assumptions):
            return False
        elif zero_base is False:
            return True
    if _ask_recursive(Q.positive(expr.base), assumptions):
        if _ask_recursive(Q.real(expr.exp), assumptions):
            return True
    if _ask_recursive(Q.negative(expr.base), assumptions):
        if _ask_recursive(Q.odd(expr.exp), assumptions):
            return False

@PositivePredicate.register(exp)
def _(expr, assumptions):
    if _ask_recursive(Q.real(expr.exp), assumptions):
        return True
    if _ask_recursive(Q.imaginary(expr.exp), assumptions):
        return _ask_recursive(Q.even(expr.exp/(I*pi)), assumptions)

@PositivePredicate.register(log)
def _(expr, assumptions):
    r = _ask_recursive(Q.real(expr.args[0]), assumptions)
    if r is not True:
        return r
    if _ask_recursive(Q.positive(expr.args[0] - 1), assumptions):
        return True
    if _ask_recursive(Q.negative(expr.args[0] - 1), assumptions):
        return False


@PositivePredicate.register(Trace)
def _(expr, assumptions):
    if _ask_recursive(Q.positive_definite(expr.arg), assumptions):
        return True

@PositivePredicate.register(Determinant)
def _(expr, assumptions):
    if _ask_recursive(Q.positive_definite(expr.arg), assumptions):
        return True

@PositivePredicate.register(MatrixElement)
def _(expr, assumptions):
    if (expr.i == expr.j
            and _ask_recursive(Q.positive_definite(expr.parent), assumptions)):
        return True


@PositivePredicate.register(asin)
def _(expr, assumptions):
    x = expr.args[0]
    if _ask_recursive(Q.positive(x) & Q.nonpositive(x - 1), assumptions):
        return True
    if _ask_recursive(Q.negative(x) & Q.nonnegative(x + 1), assumptions):
        return False

@PositivePredicate.register(acos)
def _(expr, assumptions):
    x = expr.args[0]
    if _ask_recursive(Q.nonpositive(x - 1) & Q.nonnegative(x + 1), assumptions):
        return True
