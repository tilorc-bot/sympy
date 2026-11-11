"""
Handlers for predicates related to set membership: integer, rational, etc.
"""
from __future__ import annotations

from sympy.assumptions import Q
from sympy.assumptions.ask import _ask_recursive
from sympy.core import Add, Mul, Pow
from sympy.core.numbers import E
from sympy.core.logic import fuzzy_bool, fuzzy_or
from sympy.functions import exp
from sympy.core.relational import Eq
from sympy.functions.elementary.complexes import conjugate
from sympy.matrices import Determinant, MatrixBase, Trace
from sympy.matrices.expressions.matexpr import MatrixElement

from sympy.multipledispatch import MDNotImplementedError

from .common import test_closed_group, ask_all
from ..predicates.sets import (IntegerPredicate, RationalPredicate,
    RealPredicate, HermitianPredicate, ComplexPredicate,
    ImaginaryPredicate, AntihermitianPredicate, AlgebraicPredicate)


# IntegerPredicate


@IntegerPredicate.register_many(Determinant, MatrixElement, Trace)
def _(expr, assumptions):
    return _ask_recursive(Q.integer_elements(expr.args[0]), assumptions)


# RationalPredicate


@RationalPredicate.register(Pow)
def _(expr, assumptions):
    if expr.base == E and _ask_recursive(Q.rational(expr.exp), assumptions):
        return _ask_recursive(Q.zero(expr.exp), assumptions)


# RealPredicate


@RealPredicate.register(Pow)
def _(expr, assumptions):
    base = expr.base
    if base.func == exp or (base.is_Pow and base.base == E):
        if ask_all(Q.imaginary(base.exp), Q.imaginary(expr.exp), assumptions=assumptions):
            return True


@RealPredicate.register_many(Determinant, MatrixElement, Trace)
def _(expr, assumptions):
    return _ask_recursive(Q.real_elements(expr.args[0]), assumptions)


# HermitianPredicate

@HermitianPredicate.register(object) # type:ignore
def _(expr, assumptions):
    if isinstance(expr, MatrixBase):
        return None
    return _ask_recursive(Q.real(expr), assumptions)

@HermitianPredicate.register(Add) # type:ignore
def _(expr, assumptions):
    """
    * Hermitian + Hermitian  -> Hermitian
    * Hermitian + !Hermitian -> !Hermitian
    """
    if expr.is_number:
        raise MDNotImplementedError
    return test_closed_group(expr, assumptions, Q.hermitian)

@HermitianPredicate.register(Mul) # type:ignore
def _(expr, assumptions):
    """
    As long as there is at most only one noncommutative term:

    * Hermitian*Hermitian         -> Hermitian
    * Hermitian*Antihermitian     -> !Hermitian
    * Antihermitian*Antihermitian -> Hermitian
    """
    if expr.is_number:
        raise MDNotImplementedError
    nccount = 0
    result = True
    for arg in expr.args:
        if _ask_recursive(Q.antihermitian(arg), assumptions):
            result = result ^ True
        elif not _ask_recursive(Q.hermitian(arg), assumptions):
            break
        if _ask_recursive(~Q.commutative(arg), assumptions):
            nccount += 1
            if nccount > 1:
                break
    else:
        return result


@HermitianPredicate.register(MatrixBase) # type:ignore
def _(mat, assumptions):
    rows, cols = mat.shape
    ret_val = True
    for i in range(rows):
        for j in range(i, cols):
            cond = fuzzy_bool(Eq(mat[i, j], conjugate(mat[j, i])))
            if cond is None:
                ret_val = None
            if cond == False:
                return False
    if ret_val is None:
        raise MDNotImplementedError
    return ret_val


# ComplexPredicate


@ComplexPredicate.register_many(Determinant, MatrixElement, Trace) # type:ignore
def _(expr, assumptions):
    return _ask_recursive(Q.complex_elements(expr.args[0]), assumptions)


# ImaginaryPredicate


@ImaginaryPredicate.register(Pow) # type:ignore
def _(expr, assumptions):
    """
    * Real**Real -> not Imaginary if exponent is not Rational
    """
    base = expr.base
    if base.func == exp or (base.is_Pow and base.base == E):
        if ask_all(Q.imaginary(base.exp), Q.imaginary(expr.exp), assumptions=assumptions):
            return False

    if _ask_recursive(Q.real(base) & Q.real(expr.exp), assumptions):
        if _ask_recursive(Q.rational(expr.exp), assumptions) is False:
            return False


# AntihermitianPredicate

@AntihermitianPredicate.register(object) # type:ignore
def _(expr, assumptions):
    if isinstance(expr, MatrixBase):
        return None
    return fuzzy_or([_ask_recursive(Q.zero(expr), assumptions),
                     _ask_recursive(Q.imaginary(expr), assumptions)])


@AntihermitianPredicate.register(Mul) # type:ignore
def _(expr, assumptions):
    """
    As long as there is at most only one noncommutative term:

    * Hermitian*Hermitian         -> !Antihermitian
    * Hermitian*Antihermitian     -> Antihermitian
    * Antihermitian*Antihermitian -> !Antihermitian
    """
    if expr.is_number:
        raise MDNotImplementedError
    nccount = 0
    result = False
    for arg in expr.args:
        if _ask_recursive(Q.antihermitian(arg), assumptions):
            result = result ^ True
        elif not _ask_recursive(Q.hermitian(arg), assumptions):
            break
        if _ask_recursive(~Q.commutative(arg), assumptions):
            nccount += 1
            if nccount > 1:
                break
    else:
        return result


@AntihermitianPredicate.register(MatrixBase) # type:ignore
def _(mat, assumptions):
    rows, cols = mat.shape
    ret_val = True
    for i in range(rows):
        for j in range(i, cols):
            cond = fuzzy_bool(Eq(mat[i, j], -conjugate(mat[j, i])))
            if cond is None:
                ret_val = None
            if cond == False:
                return False
    if ret_val is None:
        raise MDNotImplementedError
    return ret_val


# AlgebraicPredicate


@AlgebraicPredicate.register(Pow) # type:ignore
def _(expr, assumptions):
    if expr.base == E and _ask_recursive(Q.algebraic(expr.exp), assumptions):
        return _ask_recursive(Q.zero(expr.exp), assumptions)
