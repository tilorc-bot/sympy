"""
Handlers for predicates related to set membership: integer, rational, etc.
"""
from __future__ import annotations

from sympy.assumptions import Q
from sympy.assumptions.ask import _ask_recursive
from sympy.core import Add, Basic, Expr, Mul, Pow, Symbol
from sympy.core.numbers import (AlgebraicNumber, ComplexInfinity, Exp1, Float,
    GoldenRatio, ImaginaryUnit, Infinity, Integer, NaN, NegativeInfinity,
    Number, NumberSymbol, Pi, Rational, TribonacciConstant)
from sympy.core.logic import fuzzy_bool, fuzzy_not
from sympy.core.relational import Eq
from sympy.functions.elementary.complexes import conjugate
from sympy.matrices import MatrixBase
from sympy.matrices.expressions.matexpr import MatrixElement

from sympy.multipledispatch import MDNotImplementedError

from ..predicates.sets import (IntegerPredicate, RationalPredicate,
    IrrationalPredicate, RealPredicate, ExtendedRealPredicate,
    HermitianPredicate, ComplexPredicate, ImaginaryPredicate,
    AntihermitianPredicate, AlgebraicPredicate, TranscendentalPredicate)


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

@IntegerPredicate.register_many(int, Integer) # type:ignore
def _(expr, assumptions):
    return True

@IntegerPredicate.register_many(Exp1, GoldenRatio, ImaginaryUnit, Infinity,
        NegativeInfinity, Pi, Rational, TribonacciConstant)
def _(expr, assumptions):
    return False

@IntegerPredicate.register(Expr)
def _(expr, assumptions):
    if expr.is_number and isinstance(expr, (Add, Mul, Pow)):
        return _IntegerPredicate_number(expr, assumptions)
    ret = expr.is_integer
    if ret is None:
        raise MDNotImplementedError
    return ret

@IntegerPredicate.register(MatrixElement)
def _(expr, assumptions):
    if _ask_recursive(Q.integer_elements(expr.args[0]), assumptions):
        return True


# RationalPredicate

@RationalPredicate.register(Rational)
def _(expr, assumptions):
    return True

@RationalPredicate.register(Float)
def _(expr, assumptions):
    return None

@RationalPredicate.register_many(Exp1, GoldenRatio, ImaginaryUnit, Infinity,
    NegativeInfinity, Pi, TribonacciConstant)
def _(expr, assumptions):
    return False

@RationalPredicate.register(Expr)
def _(expr, assumptions):
    if (expr.is_number and isinstance(expr, (Add, Mul))
            and expr.as_real_imag()[1]):
        return False
    ret = expr.is_rational
    if ret is None:
        raise MDNotImplementedError
    return ret




# IrrationalPredicate

@IrrationalPredicate.register(Expr)
def _(expr, assumptions):
    ret = expr.is_irrational
    if ret is None:
        raise MDNotImplementedError
    return ret

@IrrationalPredicate.register(Basic)
def _(expr, assumptions):
    _real = _ask_recursive(Q.real(expr), assumptions)
    if _real:
        _rational = _ask_recursive(Q.rational(expr), assumptions)
        if _rational is None:
            return None
        return not _rational
    else:
        return _real


# RealPredicate

def _RealPredicate_number(expr, assumptions):
    # let as_real_imag() work first since the expression may
    # be simpler to evaluate
    i = expr.as_real_imag()[1].evalf(2)
    if i._prec != 1:
        return not i
    # allow None to be returned if we couldn't show for sure
    # that i was 0

@RealPredicate.register_many(Exp1, Float, GoldenRatio, Pi, Rational,
    TribonacciConstant)
def _(expr, assumptions):
    return True

@RealPredicate.register_many(ImaginaryUnit, Infinity, NegativeInfinity)
def _(expr, assumptions):
    return False

@RealPredicate.register(Expr)
def _(expr, assumptions):
    if expr.is_number and isinstance(expr, (Add, Mul, Pow)):
        return _RealPredicate_number(expr, assumptions)
    ret = expr.is_real
    if ret is None:
        raise MDNotImplementedError
    return ret

@RealPredicate.register(MatrixElement)
def _(expr, assumptions):
    if _ask_recursive(Q.real_elements(expr.args[0]), assumptions):
        return True


# ExtendedRealPredicate

@ExtendedRealPredicate.register(object)
def _(expr, assumptions):
    return _ask_recursive(Q.negative_infinite(expr)
               | Q.negative(expr)
               | Q.zero(expr)
               | Q.positive(expr)
               | Q.positive_infinite(expr),
            assumptions)

@ExtendedRealPredicate.register_many(Infinity, NegativeInfinity)
def _(expr, assumptions):
    return True



# HermitianPredicate

@HermitianPredicate.register(object) # type:ignore
def _(expr, assumptions):
    if isinstance(expr, MatrixBase):
        return None
    return _ask_recursive(Q.real(expr), assumptions)

@HermitianPredicate.register(Symbol) # type:ignore
def _(expr, assumptions):
    return _ask_recursive(Q.real(expr), assumptions)

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

@ComplexPredicate.register_many(ImaginaryUnit, Number, NumberSymbol) # type:ignore
def _(expr, assumptions):
    return True

@ComplexPredicate.register_many(Infinity, NegativeInfinity) # type:ignore
def _(expr, assumptions):
    return False

@ComplexPredicate.register(Expr) # type:ignore
def _(expr, assumptions):
    ret = expr.is_complex
    if ret is None:
        raise MDNotImplementedError
    return ret

@ComplexPredicate.register(NaN) # type:ignore
def _(expr, assumptions):
    return None

@ComplexPredicate.register(MatrixElement) # type:ignore
def _(expr, assumptions):
    if _ask_recursive(Q.complex_elements(expr.args[0]), assumptions):
        return True


# ImaginaryPredicate

def _Imaginary_number(expr, assumptions):
    # let as_real_imag() work first since the expression may
    # be simpler to evaluate
    r = expr.as_real_imag()[0].evalf(2)
    if r._prec != 1:
        return not r
    # allow None to be returned if we couldn't show for sure
    # that r was 0

@ImaginaryPredicate.register(ImaginaryUnit) # type:ignore
def _(expr, assumptions):
    return True

@ImaginaryPredicate.register(Expr) # type:ignore
def _(expr, assumptions):
    if expr.is_number and isinstance(expr, (Add, Mul, Pow)):
        return _Imaginary_number(expr, assumptions)
    ret = expr.is_imaginary
    if ret is None:
        raise MDNotImplementedError
    return ret

@ImaginaryPredicate.register_many(Number, NumberSymbol) # type:ignore
def _(expr, assumptions):
    return not (expr.as_real_imag()[1] == 0)

@ImaginaryPredicate.register(NaN) # type:ignore
def _(expr, assumptions):
    return None


# AntihermitianPredicate

def _Antihermitian_scalar(expr, assumptions):
    zero = _ask_recursive(Q.zero(expr), assumptions)
    if zero:
        return True
    imaginary = _ask_recursive(Q.imaginary(expr), assumptions)
    if imaginary:
        return True
    if zero is False and imaginary is False:
        return False

@AntihermitianPredicate.register(object) # type:ignore
def _(expr, assumptions):
    if isinstance(expr, MatrixBase):
        return None
    return _Antihermitian_scalar(expr, assumptions)

@AntihermitianPredicate.register(Symbol) # type:ignore
def _(expr, assumptions):
    return _Antihermitian_scalar(expr, assumptions)

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

@AlgebraicPredicate.register_many(AlgebraicNumber, GoldenRatio, # type:ignore
    ImaginaryUnit, TribonacciConstant)
def _(expr, assumptions):
    return True

@AlgebraicPredicate.register(Expr) # type:ignore
def _(expr, assumptions):
    ret = expr.is_algebraic
    if ret is None:
        raise MDNotImplementedError
    return ret

@AlgebraicPredicate.register(Float)
def _(expr, assumptions):
    return None

@AlgebraicPredicate.register_many(ComplexInfinity, Exp1, Infinity, # type:ignore
    NegativeInfinity, Pi)
def _(expr, assumptions):
    return False

@AlgebraicPredicate.register(Rational) # type:ignore
def _(expr, assumptions):
    return expr.q != 0



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
