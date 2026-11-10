"""
This module contains query handlers responsible for Matrices queries:
Square, Symmetric, Invertible etc.
"""
from __future__ import annotations

from sympy.core.logic import fuzzy_and
from sympy.logic.boolalg import conjuncts
from sympy.assumptions import Q
from sympy.assumptions.ask import _ask_recursive
from sympy.assumptions.handlers import test_closed_group
from sympy.matrices import MatrixBase
from sympy.matrices.expressions import (BlockDiagMatrix, BlockMatrix,
    DiagMatrix, DiagonalMatrix, Identity, MatrixExpr, MatrixSymbol, OneMatrix,
    ZeroMatrix)
from sympy.matrices.expressions.blockmatrix import reblock_2x2
from sympy.matrices.expressions.factorizations import (Factorization, LofLU,
    QofQR, RofQR, SofSVD, UofLU, UofSVD, VofSVD)
from sympy.matrices.expressions.fourier import DFT

from ..predicates.matrices import (SquarePredicate, SymmetricPredicate,
    InvertiblePredicate, OrthogonalPredicate, UnitaryPredicate,
    FullRankPredicate, PositiveDefinitePredicate, UpperTriangularPredicate,
    LowerTriangularPredicate, DiagonalPredicate, IntegerElementsPredicate,
    RealElementsPredicate, ComplexElementsPredicate)


def _Factorization(predicate, expr, assumptions):
    if predicate in expr.predicates:
        return True


def _is_empty_or_1x1(expr):
    return expr.shape in ((0, 0), (1, 1))


def _blocks_elements(predicate, expr, assumptions):
    if isinstance(expr, BlockDiagMatrix):
        return None
    return fuzzy_and(_ask_recursive(predicate(block), assumptions) for block in expr.blocks)


# SquarePredicate

@SquarePredicate.register(MatrixExpr)
def _(expr, assumptions):
    return expr.shape[0] == expr.shape[1]


# SymmetricPredicate

@SymmetricPredicate.register(MatrixExpr)
def _(expr, assumptions):
    if expr.is_square is False:
        return False
    if _is_empty_or_1x1(expr):
        return True

@SymmetricPredicate.register(MatrixSymbol)
def _(expr, assumptions):
    if not expr.is_square:
        return False
    # TODO: implement sathandlers system for the matrices.
    # Now it duplicates the general fact: Implies(Q.diagonal, Q.symmetric).
    if _ask_recursive(Q.diagonal(expr), assumptions):
        return True
    if Q.symmetric(expr) in conjuncts(assumptions):
        return True

@SymmetricPredicate.register_many(OneMatrix, ZeroMatrix)
def _(expr, assumptions):
    return _ask_recursive(Q.square(expr), assumptions)

@SymmetricPredicate.register(Identity)
def _(expr, assumptions):
    return True


# InvertiblePredicate

@InvertiblePredicate.register(MatrixSymbol)
def _(expr, assumptions):
    if not expr.is_square:
        return False
    if Q.invertible(expr) in conjuncts(assumptions):
        return True

@InvertiblePredicate.register(Identity)
def _(expr, assumptions):
    return True

@InvertiblePredicate.register(ZeroMatrix)
def _(expr, assumptions):
    return False

@InvertiblePredicate.register(OneMatrix)
def _(expr, assumptions):
    return expr.shape[0] == 1 and expr.shape[1] == 1

@InvertiblePredicate.register(MatrixBase)
def _(expr, assumptions):
    if not expr.is_square:
        return False
    return expr.rank() == expr.rows

@InvertiblePredicate.register(MatrixExpr)
def _(expr, assumptions):
    if not expr.is_square:
        return False
    return None

@InvertiblePredicate.register(BlockMatrix)
def _(expr, assumptions):
    if expr.is_square is False:
        return False
    if isinstance(expr, BlockDiagMatrix):
        return None
    if expr.blockshape == (1, 1):
        return _ask_recursive(Q.invertible(expr.blocks[0, 0]), assumptions)
    expr = reblock_2x2(expr)
    if expr.blockshape == (2, 2):
        [[A, B], [C, D]] = expr.blocks.tolist()
        if _ask_recursive(Q.invertible(A), assumptions) is True:
            invertible = _ask_recursive(Q.invertible(D - C * A.I * B), assumptions)
            if invertible is not None:
                return invertible
        if _ask_recursive(Q.invertible(B), assumptions) is True:
            invertible = _ask_recursive(Q.invertible(C - D * B.I * A), assumptions)
            if invertible is not None:
                return invertible
        if _ask_recursive(Q.invertible(C), assumptions) is True:
            invertible = _ask_recursive(Q.invertible(B - A * C.I * D), assumptions)
            if invertible is not None:
                return invertible
        if _ask_recursive(Q.invertible(D), assumptions) is True:
            invertible = _ask_recursive(Q.invertible(A - B * D.I * C), assumptions)
            if invertible is not None:
                return invertible
    return None


# OrthogonalPredicate

@OrthogonalPredicate.register(MatrixSymbol)
def _(expr, assumptions):
    if (not expr.is_square or
                    _ask_recursive(Q.invertible(expr), assumptions) is False):
        return False
    if Q.orthogonal(expr) in conjuncts(assumptions):
        return True

@OrthogonalPredicate.register(Identity)
def _(expr, assumptions):
    return True

@OrthogonalPredicate.register(ZeroMatrix)
def _(expr, assumptions):
    return False

@OrthogonalPredicate.register(Factorization)
def _(expr, assumptions):
    return _Factorization(Q.orthogonal, expr, assumptions)


# UnitaryPredicate

@UnitaryPredicate.register(MatrixSymbol)
def _(expr, assumptions):
    if (not expr.is_square or
                    _ask_recursive(Q.invertible(expr), assumptions) is False):
        return False
    if Q.unitary(expr) in conjuncts(assumptions):
        return True

@UnitaryPredicate.register_many(DFT, Identity)
def _(expr, assumptions):
    return True

@UnitaryPredicate.register(ZeroMatrix)
def _(expr, assumptions):
    return False

@UnitaryPredicate.register(Factorization)
def _(expr, assumptions):
    return _Factorization(Q.unitary, expr, assumptions)


# FullRankPredicate

@FullRankPredicate.register(Identity)
def _(expr, assumptions):
    return True

@FullRankPredicate.register(ZeroMatrix)
def _(expr, assumptions):
    return False

@FullRankPredicate.register(OneMatrix)
def _(expr, assumptions):
    return expr.shape[0] == 1 and expr.shape[1] == 1


# PositiveDefinitePredicate

@PositiveDefinitePredicate.register(MatrixSymbol)
def _(expr, assumptions):
    if not expr.is_square:
        return False
    if Q.positive_definite(expr) in conjuncts(assumptions):
        return True

@PositiveDefinitePredicate.register(Identity)
def _(expr, assumptions):
    return True

@PositiveDefinitePredicate.register(ZeroMatrix)
def _(expr, assumptions):
    return False

@PositiveDefinitePredicate.register(OneMatrix)
def _(expr, assumptions):
    return expr.shape[0] == 1 and expr.shape[1] == 1


# UpperTriangularPredicate

@UpperTriangularPredicate.register(MatrixSymbol)
def _(expr, assumptions):
    if Q.upper_triangular(expr) in conjuncts(assumptions):
        return True

@UpperTriangularPredicate.register_many(Identity, ZeroMatrix)
def _(expr, assumptions):
    return True

@UpperTriangularPredicate.register(OneMatrix)
def _(expr, assumptions):
    return expr.shape[0] == 1 and expr.shape[1] == 1

@UpperTriangularPredicate.register(Factorization)
def _(expr, assumptions):
    return _Factorization(Q.upper_triangular, expr, assumptions)

# LowerTriangularPredicate

@LowerTriangularPredicate.register(MatrixSymbol)
def _(expr, assumptions):
    if Q.lower_triangular(expr) in conjuncts(assumptions):
        return True

@LowerTriangularPredicate.register_many(Identity, ZeroMatrix)
def _(expr, assumptions):
    return True

@LowerTriangularPredicate.register(OneMatrix)
def _(expr, assumptions):
    return expr.shape[0] == 1 and expr.shape[1] == 1

@LowerTriangularPredicate.register(Factorization)
def _(expr, assumptions):
    return _Factorization(Q.lower_triangular, expr, assumptions)


# DiagonalPredicate

@DiagonalPredicate.register(MatrixExpr)
def _(expr, assumptions):
    if _is_empty_or_1x1(expr):
        return True

@DiagonalPredicate.register(MatrixSymbol)
def _(expr, assumptions):
    if _is_empty_or_1x1(expr):
        return True
    if Q.diagonal(expr) in conjuncts(assumptions):
        return True

@DiagonalPredicate.register(OneMatrix)
def _(expr, assumptions):
    return expr.shape[0] == 1 and expr.shape[1] == 1

@DiagonalPredicate.register_many(DiagMatrix, Identity, ZeroMatrix)
def _(expr, assumptions):
    return True

@DiagonalPredicate.register(DiagonalMatrix)
def _(expr, assumptions):
    if expr.is_square:
        return True

@DiagonalPredicate.register(Factorization)
def _(expr, assumptions):
    return _Factorization(Q.diagonal, expr, assumptions)


# IntegerElementsPredicate

@IntegerElementsPredicate.register_many(Identity, OneMatrix, ZeroMatrix)
def _(expr, assumptions):
    return True

@IntegerElementsPredicate.register(BlockMatrix)
def _(expr, assumptions):
    return _blocks_elements(Q.integer_elements, expr, assumptions)


# RealElementsPredicate

@RealElementsPredicate.register_many(LofLU, UofLU, QofQR, RofQR, UofSVD,
    SofSVD, VofSVD)
def _(expr, assumptions):
    return test_closed_group(expr, assumptions, Q.real_elements)

@RealElementsPredicate.register(BlockMatrix)
def _(expr, assumptions):
    return _blocks_elements(Q.real_elements, expr, assumptions)


# ComplexElementsPredicate

@ComplexElementsPredicate.register(Factorization)
def _(expr, assumptions):
    return test_closed_group(expr, assumptions, Q.complex_elements)

@ComplexElementsPredicate.register(DFT)
def _(expr, assumptions):
    return True

@ComplexElementsPredicate.register(BlockMatrix)
def _(expr, assumptions):
    return _blocks_elements(Q.complex_elements, expr, assumptions)
