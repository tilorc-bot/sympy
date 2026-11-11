"""
Handlers for predicates related to set membership: integer, rational, etc.
"""
from __future__ import annotations

from sympy.assumptions import Q
from sympy.assumptions.ask import _ask_recursive
from sympy.core import Add, Expr, Mul, Pow, S
from sympy.core.numbers import E, I, pi
from sympy.core.logic import fuzzy_and, fuzzy_bool, fuzzy_not, fuzzy_or
from sympy.functions import acos, exp, log
from sympy.core.relational import Eq
from sympy.functions.elementary.complexes import conjugate
from sympy.matrices import Determinant, MatrixBase, Trace
from sympy.matrices.expressions.matexpr import MatrixElement

from sympy.multipledispatch import MDNotImplementedError

from .common import test_closed_group, ask_all, ask_any
from ..predicates.sets import (IntegerPredicate, RationalPredicate,
    IrrationalPredicate, RealPredicate, HermitianPredicate, ComplexPredicate,
    ImaginaryPredicate, AntihermitianPredicate, AlgebraicPredicate,
    TranscendentalPredicate)


# IntegerPredicate

def _IntegerPredicate_number(expr, assumptions):
    # helper function
        try:
            i = int(expr.round())
            if not (expr - i).equals(0):
                raise TypeError
            return True
        except TypeError:
            return False


@IntegerPredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_integer
    if ret is None:
        raise MDNotImplementedError
    return ret


@IntegerPredicate.register(Pow)
def _(expr, assumptions):
    if expr.is_number:
        return _IntegerPredicate_number(expr, assumptions)
    if ask_all(~Q.zero(expr.base), Q.finite(expr.base), Q.zero(expr.exp), assumptions=assumptions):
        return True
    if ask_all(Q.integer(expr.base), Q.integer(expr.exp), assumptions=assumptions):
        neg_exp = _ask_recursive(Q.negative(expr.exp), assumptions)
        if neg_exp is False:
            return True
        base_pm_1 = ask_any(Q.zero(expr.base - 1), Q.zero(expr.base + 1), assumptions=assumptions)
        if base_pm_1:
            return True
        if neg_exp and base_pm_1 is False:
            return False

@IntegerPredicate.register(Mul)
def _(expr, assumptions):
    """
    * Integer*Integer      -> Integer
    * Integer*Irrational   -> !Integer
    * Odd/Even             -> !Integer
    * Integer*Rational     -> ?
    """
    if expr.is_number:
        return _IntegerPredicate_number(expr, assumptions)
    _output = True
    for arg in expr.args:
        if not _ask_recursive(Q.integer(arg), assumptions):
            if arg.is_Rational:
                if arg.q == 2:
                    return _ask_recursive(Q.even(2*expr), assumptions)
                if ~(arg.q & 1):
                    return None
            elif _ask_recursive(Q.irrational(arg), assumptions):
                if _output:
                    _output = False
                else:
                    return
            else:
                return

    return _output


@IntegerPredicate.register_many(Determinant, MatrixElement, Trace)
def _(expr, assumptions):
    return _ask_recursive(Q.integer_elements(expr.args[0]), assumptions)


# RationalPredicate


@RationalPredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_rational
    if ret is None:
        raise MDNotImplementedError
    return ret


@RationalPredicate.register(Pow)
def _(expr, assumptions):
    """
    * Rational ** Integer      -> Rational
    * Irrational ** Rational   -> Irrational
    * Rational ** Irrational   -> ?
    """
    if expr.base == E:
        x = expr.exp
        if _ask_recursive(Q.rational(x), assumptions):
            return _ask_recursive(Q.zero(x), assumptions)
        return

    is_exp_integer = _ask_recursive(Q.integer(expr.exp), assumptions)
    if is_exp_integer:
        is_base_rational = _ask_recursive(Q.rational(expr.base), assumptions)
        if is_base_rational:
            is_base_zero = _ask_recursive(Q.zero(expr.base), assumptions)
            if is_base_zero is False:
                return True
            if is_base_zero and _ask_recursive(Q.positive(expr.exp), assumptions):
                return True
        if _ask_recursive(Q.algebraic(expr.base), assumptions) is False:
            return _ask_recursive(Q.zero(expr.exp), assumptions)
        if _ask_recursive(Q.irrational(expr.base), assumptions) and _ask_recursive(Q.eq(expr.exp, -1), assumptions):
            return False
        return
    elif _ask_recursive(Q.rational(expr.exp), assumptions):
        if _ask_recursive(Q.prime(expr.base), assumptions) and is_exp_integer is False:
            return False
        if _ask_recursive(Q.zero(expr.base), assumptions) and _ask_recursive(Q.positive(expr.exp), assumptions):
            return True
        if _ask_recursive(Q.eq(expr.base, 1), assumptions):
            return True


@RationalPredicate.register_many(acos, log)
def _(expr, assumptions):
    x = expr.args[0]
    if _ask_recursive(Q.rational(x), assumptions):
        return _ask_recursive(~Q.nonzero(x - 1), assumptions)


# IrrationalPredicate

@IrrationalPredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_irrational
    if ret is None:
        raise MDNotImplementedError
    return ret


# RealPredicate

def _RealPredicate_number(expr, assumptions):
    # let as_real_imag() work first since the expression may
    # be simpler to evaluate
    i = expr.as_real_imag()[1].evalf(2)
    if i._prec != 1:
        return not i
    # allow None to be returned if we couldn't show for sure
    # that i was 0


@RealPredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_real
    if ret is None:
        raise MDNotImplementedError
    return ret


@RealPredicate.register(Pow)
def _(expr, assumptions):
    """
    * Real**Integer              -> Real
    * Positive**Real             -> Real
    * Negative**Real             -> ?
    * Real**(Integer/Even)       -> Real if base is nonnegative
    * Real**(Integer/Odd)        -> Real
    * Imaginary**(Integer/Even)  -> Real
    * Imaginary**(Integer/Odd)   -> not Real
    * Imaginary**Real            -> ? since Real could be 0 (giving real)
                                    or 1 (giving imaginary)
    * b**Imaginary               -> Real if log(b) is imaginary and b != 0
                                    and exponent != integer multiple of
                                    I*pi/log(b)
    * Real**Real                 -> ? e.g. sqrt(-1) is imaginary and
                                    sqrt(2) is not
    """
    if expr.is_number:
        return _RealPredicate_number(expr, assumptions)

    if expr.base == E:
        return _ask_recursive(
            Q.integer(expr.exp/I/pi) | Q.real(expr.exp), assumptions
        )

    if expr.base.func == exp or (expr.base.is_Pow and expr.base.base == E):
        if _ask_recursive(Q.imaginary(expr.base.exp), assumptions):
            if _ask_recursive(Q.imaginary(expr.exp), assumptions):
                return True
        # If the i = (exp's arg)/(I*pi) is an integer or half-integer
        # multiple of I*pi then 2*i will be an integer. In addition,
        # exp(i*I*pi) = (-1)**i so the overall realness of the expr
        # can be determined by replacing exp(i*I*pi) with (-1)**i.
        i = expr.base.exp/I/pi
        if _ask_recursive(Q.integer(2*i), assumptions):
            return _ask_recursive(Q.real((S.NegativeOne**i)**expr.exp), assumptions)
        return

    if _ask_recursive(Q.imaginary(expr.base), assumptions):
        if _ask_recursive(Q.integer(expr.exp), assumptions):
            odd = _ask_recursive(Q.odd(expr.exp), assumptions)
            if odd is not None:
                return not odd
            return

    if _ask_recursive(Q.imaginary(expr.exp), assumptions):
        imlog = _ask_recursive(Q.imaginary(log(expr.base)), assumptions)
        if imlog is not None:
            # I**i -> real, log(I) is imag;
            # (2*I)**i -> complex, log(2*I) is not imag
            return imlog

    if _ask_recursive(Q.real(expr.base), assumptions):
        if _ask_recursive(Q.real(expr.exp), assumptions):
            if (expr.exp.is_Rational and
                    _ask_recursive(Q.even(expr.exp.q), assumptions)):
                return _ask_recursive(Q.nonnegative(expr.base), assumptions)
            base_is_zero = _ask_recursive(Q.zero(expr.base), assumptions)
            if base_is_zero or _ask_recursive(Q.integer(expr.exp), assumptions):
                # Division by zero : If the base is 0 and the exponent
                # is negative, ``expr`` evaluates to complex infinity.
                expr_is_complex_infinity = fuzzy_and([base_is_zero,
                                _ask_recursive(Q.negative(expr.exp), assumptions)])
                return fuzzy_not(expr_is_complex_infinity)
            elif _ask_recursive(Q.positive(expr.base), assumptions):
                return True


@RealPredicate.register(exp)
def _(expr, assumptions):
    return _ask_recursive(
        Q.integer(expr.exp/I/pi) | Q.real(expr.exp), assumptions
    )


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


@ComplexPredicate.register(Expr) # type:ignore
def _(expr, assumptions):
    ret = expr.is_complex
    if ret is None:
        raise MDNotImplementedError
    return ret


@ComplexPredicate.register_many(Determinant, MatrixElement, Trace) # type:ignore
def _(expr, assumptions):
    return _ask_recursive(Q.complex_elements(expr.args[0]), assumptions)


# ImaginaryPredicate

def _Imaginary_number(expr, assumptions):
    # let as_real_imag() work first since the expression may
    # be simpler to evaluate
    r = expr.as_real_imag()[0].evalf(2)
    if r._prec != 1:
        return not r
    # allow None to be returned if we couldn't show for sure
    # that r was 0


@ImaginaryPredicate.register(Expr) # type:ignore
def _(expr, assumptions):
    ret = expr.is_imaginary
    if ret is None:
        raise MDNotImplementedError
    return ret


@ImaginaryPredicate.register(Mul) # type:ignore
def _(expr, assumptions):
    """
    * Real*Imaginary      -> Imaginary
    * Imaginary*Imaginary -> Real
    """
    if expr.is_number:
        return _Imaginary_number(expr, assumptions)
    result = False
    reals = 0
    for arg in expr.args:
        if _ask_recursive(Q.imaginary(arg), assumptions):
            result = result ^ True
        elif not _ask_recursive(Q.real(arg), assumptions):
            break
    else:
        if reals == len(expr.args):
            return False
        return result

@ImaginaryPredicate.register(Pow) # type:ignore
def _(expr, assumptions):
    """
    * Imaginary**Odd        -> Imaginary
    * Imaginary**Even       -> Real
    * b**Imaginary          -> !Imaginary if exponent is an integer
                               multiple of I*pi/log(b)
    * Imaginary**Real       -> ?
    * Positive**Real        -> Real
    * Negative**Integer     -> Real
    * Negative**(Integer/2) -> Imaginary
    * Negative**Real        -> not Imaginary if exponent is not Rational
    """
    if expr.is_number:
        return _Imaginary_number(expr, assumptions)

    if expr.base == E:
        a = expr.exp/I/pi
        return _ask_recursive(Q.integer(2*a) & ~Q.integer(a), assumptions)

    if expr.base.func == exp or (expr.base.is_Pow and expr.base.base == E):
        if _ask_recursive(Q.imaginary(expr.base.exp), assumptions):
            if _ask_recursive(Q.imaginary(expr.exp), assumptions):
                return False
            i = expr.base.exp/I/pi
            if _ask_recursive(Q.integer(2*i), assumptions):
                return _ask_recursive(Q.imaginary((S.NegativeOne**i)**expr.exp), assumptions)

    if _ask_recursive(Q.imaginary(expr.base), assumptions):
        if _ask_recursive(Q.integer(expr.exp), assumptions):
            odd = _ask_recursive(Q.odd(expr.exp), assumptions)
            if odd is not None:
                return odd
            return

    if _ask_recursive(Q.imaginary(expr.exp), assumptions):
        imlog = _ask_recursive(Q.imaginary(log(expr.base)), assumptions)
        if imlog is not None:
            # I**i -> real; (2*I)**i -> complex ==> not imaginary
            return False

    if _ask_recursive(Q.real(expr.base) & Q.real(expr.exp), assumptions):
        if _ask_recursive(Q.positive(expr.base), assumptions):
            return False
        else:
            rat = _ask_recursive(Q.rational(expr.exp), assumptions)
            if not rat:
                return rat
            if _ask_recursive(Q.integer(expr.exp), assumptions):
                return False
            else:
                half = _ask_recursive(Q.integer(2*expr.exp), assumptions)
                if half:
                    return _ask_recursive(Q.negative(expr.base), assumptions)
                return half


@ImaginaryPredicate.register(exp) # type:ignore
def _(expr, assumptions):
    a = expr.exp/I/pi
    return _ask_recursive(Q.integer(2*a) & ~Q.integer(a), assumptions)


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
    if expr.base == E:
        if _ask_recursive(Q.algebraic(expr.exp), assumptions):
            return _ask_recursive(~Q.nonzero(expr.exp), assumptions)
        return
    if expr.base == pi:
        if _ask_recursive(Q.integer(expr.exp), assumptions) and _ask_recursive(Q.positive(expr.exp), assumptions):
            return False
        return
    exp_rational = _ask_recursive(Q.rational(expr.exp), assumptions)
    base_algebraic = _ask_recursive(Q.algebraic(expr.base), assumptions)
    exp_algebraic = _ask_recursive(Q.algebraic(expr.exp), assumptions)
    if base_algebraic and exp_algebraic:
        if exp_rational:
            return True
        # Check based on the Gelfond-Schneider theorem:
        # If the base is algebraic and not equal to 0 or 1, and the exponent
        # is irrational,then the result is transcendental.
        if _ask_recursive(Q.ne(expr.base, 0) & Q.ne(expr.base, 1), assumptions) and exp_rational is False:
            return False

    exp_integer = _ask_recursive(Q.integer(expr.exp), assumptions)
    if base_algebraic is False and exp_integer:
        if expr.exp > 0:
            return False


@AlgebraicPredicate.register_many(acos, log) # type:ignore
def _(expr, assumptions):
    x = expr.args[0]
    if _ask_recursive(Q.algebraic(x), assumptions):
        return _ask_recursive(~Q.nonzero(x - 1), assumptions)


# TranscendentalPredicate

@TranscendentalPredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_transcendental
    if ret is not None:
        return ret

    is_complex = _ask_recursive(Q.complex(expr), assumptions)
    if is_complex:
        is_algebraic = _ask_recursive(Q.algebraic(expr), assumptions)
        return fuzzy_not(is_algebraic)
    return is_complex
