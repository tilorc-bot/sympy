"""
Rules for the predicates about matrices: ``Q.invertible``, ``Q.symmetric``,
``Q.orthogonal``, ``Q.diagonal``, ``Q.real_elements`` and others.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.core.expr import Expr
from sympy.logic.boolalg import Equivalent
from sympy.matrices.expressions.blockmatrix import BlockDiagMatrix
from sympy.matrices.expressions.determinant import Determinant
from sympy.matrices.expressions.hadamard import HadamardProduct
from sympy.matrices.expressions.inverse import Inverse
from sympy.matrices.expressions.matadd import MatAdd
from sympy.matrices.expressions.matmul import MatMul
from sympy.matrices.expressions.matpow import MatPow
from sympy.matrices.expressions.slice import MatrixSlice
from sympy.matrices.expressions.trace import Trace
from sympy.matrices.expressions.transpose import Transpose

from .language import (base, closed, columns, exponent, f, for_all, rows, x,
    y)

RULES = (
    # --- any expression ---

    # A square matrix of full rank is invertible
    for_all((Expr,),
        (Q.fullrank(x) & Q.square(x)) >> Q.invertible(x)),

    # A matrix which is upper and lower triangular is diagonal
    for_all((Expr,),
        (Q.upper_triangular(x) & Q.lower_triangular(x)) >> Q.diagonal(x)),

    # --- MatMul ---

    # A product of square matrices is invertible exactly when each factor is
    #     its determinant is the product of the determinants of the factors
    for_all((MatMul,),
        (Q.square(x) & Q.square(y))
        >> Equivalent(Q.invertible(f(x, y)), Q.invertible(x) & Q.invertible(y))),

    # A nonzero number times an invertible matrix is invertible
    for_all((MatMul,),
        (Q.complex(x) & ~Q.zero(x) & Q.invertible(y)) >> Q.invertible(f(x, y))),

    # A square matrix of full rank times a matrix of full rank has full rank
    #     an invertible factor keeps the rank of the other; without a square
    #     factor the rank can drop
    for_all((MatMul,),
        (Q.square(x) & Q.fullrank(x) & Q.fullrank(y)) >> Q.fullrank(f(x, y)),
        (Q.fullrank(x) & Q.square(y) & Q.fullrank(y)) >> Q.fullrank(f(x, y))),

    # Orthogonal and unitary matrices are closed under multiplication
    for_all((MatMul,),
        closed(f(x, y), Q.orthogonal, Q.unitary)),

    # Triangular and diagonal matrices are closed under multiplication
    for_all((MatMul,),
        closed(f(x, y), Q.upper_triangular, Q.lower_triangular, Q.diagonal)),

    # A number times a matrix keeps the shape of its entries
    #     the number must be finite: oo*0 is nan
    for_all((MatMul,),
        (Q.complex(x) & Q.symmetric(y)) >> Q.symmetric(f(x, y)),
        (Q.complex(x) & Q.upper_triangular(y)) >> Q.upper_triangular(f(x, y)),
        (Q.complex(x) & Q.lower_triangular(y)) >> Q.lower_triangular(f(x, y)),
        (Q.complex(x) & Q.diagonal(y)) >> Q.diagonal(f(x, y))),

    # A positive number times a positive definite matrix is positive definite
    #     a product of two positive definite matrices need not be symmetric
    for_all((MatMul,),
        (Q.positive(x) & Q.positive_definite(y)) >> Q.positive_definite(f(x, y))),

    # Integer, real and complex entries are closed under multiplication
    for_all((MatMul,),
        closed(f(x, y), Q.integer_elements, Q.real_elements, Q.complex_elements)),

    # A number times a matrix with entries of the same kind
    for_all((MatMul,),
        (Q.integer(x) & Q.integer_elements(y)) >> Q.integer_elements(f(x, y)),
        (Q.real(x) & Q.real_elements(y)) >> Q.real_elements(f(x, y)),
        (Q.complex(x) & Q.complex_elements(y)) >> Q.complex_elements(f(x, y))),

    # --- MatAdd ---

    # Symmetric, positive definite, triangular and diagonal matrices are
    # closed under addition
    for_all((MatAdd,),
        closed(f(x, y), Q.symmetric, Q.positive_definite, Q.upper_triangular,
            Q.lower_triangular, Q.diagonal)),

    # A symmetric matrix plus one which is not symmetric is not symmetric
    #     the difference of two symmetric matrices is symmetric
    for_all((MatAdd,),
        (Q.symmetric(x) & ~Q.symmetric(y)) >> ~Q.symmetric(f(x, y)),
        (~Q.symmetric(x) & Q.symmetric(y)) >> ~Q.symmetric(f(x, y))),

    # A triangular matrix plus one which is not is not triangular
    #     the difference of two upper triangular matrices is upper triangular
    for_all((MatAdd,),
        (Q.upper_triangular(x) & ~Q.upper_triangular(y)) >> ~Q.upper_triangular(f(x, y)),
        (~Q.upper_triangular(x) & Q.upper_triangular(y)) >> ~Q.upper_triangular(f(x, y)),
        (Q.lower_triangular(x) & ~Q.lower_triangular(y)) >> ~Q.lower_triangular(f(x, y)),
        (~Q.lower_triangular(x) & Q.lower_triangular(y)) >> ~Q.lower_triangular(f(x, y))),

    # A diagonal matrix plus one which is not diagonal is not diagonal
    #     the difference of two diagonal matrices is diagonal
    for_all((MatAdd,),
        (Q.diagonal(x) & ~Q.diagonal(y)) >> ~Q.diagonal(f(x, y)),
        (~Q.diagonal(x) & Q.diagonal(y)) >> ~Q.diagonal(f(x, y))),

    # Integer, real and complex entries are closed under addition
    for_all((MatAdd,),
        closed(f(x, y), Q.integer_elements, Q.real_elements, Q.complex_elements)),

    # --- MatPow ---

    # An integer power of an invertible matrix is invertible
    for_all((MatPow,),
        (Q.integer(exponent) & Q.invertible(base)) >> Q.invertible(f(base, exponent)),
        (Q.integer(exponent) & Q.fullrank(base)) >> Q.fullrank(f(base, exponent))),

    # A positive power of a singular matrix is singular
    #     the power 0 is the identity
    for_all((MatPow,),
        (Q.integer(exponent) & Q.positive(exponent) & ~Q.invertible(base))
        >> ~Q.invertible(f(base, exponent))),

    # Orthogonal, unitary and positive definite matrices are closed under
    # integer powers
    for_all((MatPow,),
        (Q.integer(exponent) & Q.orthogonal(base)) >> Q.orthogonal(f(base, exponent)),
        (Q.integer(exponent) & Q.unitary(base)) >> Q.unitary(f(base, exponent)),
        (Q.integer(exponent) & Q.positive_definite(base))
        >> Q.positive_definite(f(base, exponent))),

    # Symmetric, triangular and diagonal matrices and their kinds of entries
    # are kept by integer powers
    #     a negative power is a power of the inverse, which exists only for an
    #     invertible matrix
    for_all((MatPow,),
        (Q.integer(exponent) & Q.symmetric(base)
            & (~Q.negative(exponent) | Q.invertible(base)))
        >> Q.symmetric(f(base, exponent)),
        (Q.integer(exponent) & Q.upper_triangular(base)
            & (~Q.negative(exponent) | Q.invertible(base)))
        >> Q.upper_triangular(f(base, exponent)),
        (Q.integer(exponent) & Q.lower_triangular(base)
            & (~Q.negative(exponent) | Q.invertible(base)))
        >> Q.lower_triangular(f(base, exponent)),
        (Q.integer(exponent) & Q.diagonal(base)
            & (~Q.negative(exponent) | Q.invertible(base)))
        >> Q.diagonal(f(base, exponent)),
        (Q.integer(exponent) & Q.real_elements(base)
            & (~Q.negative(exponent) | Q.invertible(base)))
        >> Q.real_elements(f(base, exponent)),
        (Q.integer(exponent) & Q.complex_elements(base)
            & (~Q.negative(exponent) | Q.invertible(base)))
        >> Q.complex_elements(f(base, exponent))),

    # A power of a matrix of integers with an exponent which is not negative
    # has integer entries
    #     the inverse of a matrix of integers need not have integer entries
    for_all((MatPow,),
        (Q.integer(exponent) & ~Q.negative(exponent) & Q.integer_elements(base))
        >> Q.integer_elements(f(base, exponent))),

    # --- Inverse ---

    # An inverse is invertible
    for_all((Inverse,),
        Q.invertible(f(base, exponent))),

    # The inverse keeps these properties, and the inverse of the inverse gives
    # them back
    for_all((Inverse,),
        Equivalent(Q.symmetric(f(base, exponent)), Q.symmetric(base)),
        Equivalent(Q.orthogonal(f(base, exponent)), Q.orthogonal(base)),
        Equivalent(Q.unitary(f(base, exponent)), Q.unitary(base)),
        Equivalent(Q.positive_definite(f(base, exponent)), Q.positive_definite(base)),
        Equivalent(Q.upper_triangular(f(base, exponent)), Q.upper_triangular(base)),
        Equivalent(Q.lower_triangular(f(base, exponent)), Q.lower_triangular(base)),
        Equivalent(Q.diagonal(f(base, exponent)), Q.diagonal(base))),

    # The inverse of a matrix with real or complex entries has entries of the
    # same kind
    for_all((Inverse,),
        Q.real_elements(base) >> Q.real_elements(f(base, exponent)),
        Q.complex_elements(base) >> Q.complex_elements(f(base, exponent))),

    # --- Transpose ---

    # The transpose keeps these properties, and the transpose of the transpose
    # gives them back
    for_all((Transpose,),
        Equivalent(Q.symmetric(f(x)), Q.symmetric(x)),
        Equivalent(Q.invertible(f(x)), Q.invertible(x)),
        Equivalent(Q.orthogonal(f(x)), Q.orthogonal(x)),
        Equivalent(Q.unitary(f(x)), Q.unitary(x)),
        Equivalent(Q.fullrank(f(x)), Q.fullrank(x)),
        Equivalent(Q.positive_definite(f(x)), Q.positive_definite(x)),
        Equivalent(Q.diagonal(f(x)), Q.diagonal(x)),
        Equivalent(Q.integer_elements(f(x)), Q.integer_elements(x)),
        Equivalent(Q.real_elements(f(x)), Q.real_elements(x)),
        Equivalent(Q.complex_elements(f(x)), Q.complex_elements(x))),

    # The transpose of an upper triangular matrix is lower triangular
    for_all((Transpose,),
        Equivalent(Q.upper_triangular(f(x)), Q.lower_triangular(x)),
        Equivalent(Q.lower_triangular(f(x)), Q.upper_triangular(x))),

    # --- HadamardProduct ---

    # Integer, real and complex entries are closed under entrywise products
    for_all((HadamardProduct,),
        closed(f(x, y), Q.integer_elements, Q.real_elements, Q.complex_elements)),

    # --- Trace, Determinant ---

    # The trace and the determinant are sums of products of the entries
    for_all((Trace, Determinant),
        closed(f(x), Q.integer_elements, Q.real_elements, Q.complex_elements)),

    # --- MatrixSlice ---

    # A slice with the same range of rows and columns of a symmetric,
    # diagonal or positive definite matrix is one too
    #     its entry (a, b) is the entry (r[a], r[b]) of the matrix, for the
    #     distinct indices r[a] of the range; invertible, orthogonal, unitary
    #     and full rank matrices are not (X[0:1, 0:1] of [[0, 1], [1, 0]]),
    #     nor triangular ones, as a range downwards reverses the order
    for_all((MatrixSlice,),
        (Q.eq(rows, columns) & Q.symmetric(x)) >> Q.symmetric(f(x, rows, columns)),
        (Q.eq(rows, columns) & Q.diagonal(x)) >> Q.diagonal(f(x, rows, columns)),
        (Q.eq(rows, columns) & Q.positive_definite(x))
        >> Q.positive_definite(f(x, rows, columns))),

    # The entries of a slice are entries of the matrix
    for_all((MatrixSlice,),
        Q.integer_elements(x) >> Q.integer_elements(f(x, rows, columns)),
        Q.real_elements(x) >> Q.real_elements(f(x, rows, columns)),
        Q.complex_elements(x) >> Q.complex_elements(f(x, rows, columns))),

    # --- BlockDiagMatrix ---

    # A block diagonal matrix is invertible exactly when each block is
    #     x is the first block and y the block diagonal matrix of the others;
    #     the rank is the sum of the ranks of the blocks, so blocks which are
    #     not square make a matrix which is not invertible
    for_all((BlockDiagMatrix,),
        Equivalent(Q.invertible(f(x)), Q.invertible(x)),
        Equivalent(Q.invertible(f(x, y)), Q.invertible(x) & Q.invertible(y))),

    # A block diagonal matrix has integer, real or complex entries exactly
    # when each block has
    #     its other entries are zeros
    for_all((BlockDiagMatrix,),
        Equivalent(Q.integer_elements(f(x)), Q.integer_elements(x)),
        Equivalent(Q.real_elements(f(x)), Q.real_elements(x)),
        Equivalent(Q.complex_elements(f(x)), Q.complex_elements(x)),
        Equivalent(Q.integer_elements(f(x, y)),
            Q.integer_elements(x) & Q.integer_elements(y)),
        Equivalent(Q.real_elements(f(x, y)),
            Q.real_elements(x) & Q.real_elements(y)),
        Equivalent(Q.complex_elements(f(x, y)),
            Q.complex_elements(x) & Q.complex_elements(y))),

)
