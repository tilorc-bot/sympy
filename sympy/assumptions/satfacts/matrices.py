"""
Facts for matrix predicates: square, symmetric, invertible, etc.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.assumptions.sathandlers import class_fact_registry
from sympy.logic.boolalg import Equivalent, Implies
from sympy.matrices import MatrixBase
from sympy.matrices.expressions import (BlockMatrix, BlockDiagMatrix, Determinant,
    DiagMatrix, DiagonalMatrix, HadamardProduct, Identity, Inverse, MatAdd, MatMul,
    MatPow, MatrixExpr, MatrixSlice, MatrixSymbol, OneMatrix, Trace, Transpose,
    ZeroMatrix)
from sympy.matrices.expressions.blockmatrix import reblock_2x2
from sympy.matrices.expressions.factorizations import Factorization
from sympy.matrices.expressions.fourier import DFT
from sympy.utilities.iterables import sift

from .common import all_, closed_group, each_with_rest


_shape_preds = [Q.symmetric, Q.invertible, Q.orthogonal, Q.unitary, Q.fullrank,
    Q.positive_definite, Q.upper_triangular, Q.lower_triangular, Q.diagonal]
_elements_preds = [Q.integer_elements, Q.real_elements, Q.complex_elements]


def _is_empty_or_1x1(expr):
    return expr.shape in ((0, 0), (1, 1))


def _is_1x1(expr):
    return expr.shape[0] == 1 and expr.shape[1] == 1


@class_fact_registry.multiregister(MatrixExpr)
def _(expr):
    facts = [Q.square(expr) if expr.shape[0] == expr.shape[1] else ~Q.square(expr)]
    if _is_empty_or_1x1(expr) and isinstance(expr, (MatMul, MatrixSymbol, MatrixSlice)):
        facts.append(Q.diagonal(expr))
    return facts


### MatMul ###

@class_fact_registry.multiregister(MatMul)
def _(expr):
    factor, mmul = expr.as_coeff_mmul()
    margs = mmul.args
    _, matrices = expr.as_coeff_matrices()
    facts = [
        Implies(all_(Q.symmetric, margs), Q.symmetric(expr)),
        Implies(all_(Q.invertible, margs), Q.invertible(expr)),
        *[Implies(all_(Q.square, margs) & ~Q.invertible(a), ~Q.invertible(expr))
          for a in margs],
        Implies(all_(Q.fullrank, expr.args), Q.fullrank(expr)),
        Implies(all_(Q.upper_triangular, matrices), Q.upper_triangular(expr)),
        Implies(all_(Q.lower_triangular, matrices), Q.lower_triangular(expr)),
        Implies(all_(Q.diagonal, matrices), Q.diagonal(expr)),
    ]
    if factor == 1:
        facts.append(Implies(all_(Q.orthogonal, margs), Q.orthogonal(expr)))
    if abs(factor) == 1:
        facts.append(Implies(all_(Q.unitary, margs), Q.unitary(expr)))
    if factor.is_positive:
        facts.append(Implies(all_(Q.positive_definite, margs), Q.positive_definite(expr)))
    if len(margs) >= 2 and margs[0] == margs[-1].T:
        if len(margs) == 2:
            facts.append(Q.symmetric(expr))
        else:
            middle = MatMul(*margs[1:-1])
            facts.append(Implies(Q.symmetric(middle), Q.symmetric(expr)))
            facts.append(Implies(Q.fullrank(margs[0]),
                Equivalent(Q.positive_definite(expr), Q.positive_definite(middle))))
    d = sift(expr.args, lambda x: isinstance(x, MatrixExpr))
    scalars, mats = d[False], d[True]
    for mpred, spred in zip(_elements_preds, [Q.integer, Q.real, Q.complex]):
        facts.append(Implies(all_(spred, scalars) & all_(mpred, mats), mpred(expr)))
        facts.extend(each_with_rest(mats, lambda a: ~mpred(a), mpred, ~mpred(expr)))
    return facts


### MatPow ###

@class_fact_registry.multiregister(MatPow)
def _(expr):
    base, e = expr.args
    int_e = Q.integer(e)
    allowed = [int_e & ~Q.negative(e), int_e & Q.invertible(base)]
    facts = []
    for pred in [Q.symmetric, Q.upper_triangular, Q.lower_triangular, Q.diagonal,
                 Q.real_elements, Q.complex_elements]:
        for cond in allowed:
            facts.append(Implies(cond & pred(base), pred(expr)))
    if e.is_negative is False:
        facts.append(Implies(int_e & Q.invertible(base), Q.invertible(expr)))
        facts.append(Implies(int_e & Q.integer_elements(base), Q.integer_elements(expr)))
    facts.extend([
        Implies(int_e & Q.orthogonal(base), Q.orthogonal(expr)),
        Implies(int_e & Q.unitary(base), Q.unitary(expr)),
        Implies(int_e & ~Q.negative(e) & Q.fullrank(base), Q.fullrank(expr)),
        Implies(Q.positive_definite(base), Q.positive_definite(expr)),
    ])
    return facts


### MatAdd ###

@class_fact_registry.multiregister(MatAdd)
def _(expr):
    args = expr.args
    facts = [*closed_group(expr, Q.symmetric)]
    for pred in [Q.positive_definite, Q.upper_triangular, Q.lower_triangular, Q.diagonal]:
        facts.append(Implies(all_(pred, args), pred(expr)))
    for pred in _elements_preds:
        facts.extend(closed_group(expr, pred))
    return facts


### Matrices with fixed properties ###

@class_fact_registry.multiregister(Identity)
def _(expr):
    return [p(expr) for p in _shape_preds] + [Q.integer_elements(expr)]


@class_fact_registry.multiregister(ZeroMatrix)
def _(expr):
    return [Equivalent(Q.symmetric(expr), Q.square(expr)),
            ~Q.invertible(expr), ~Q.orthogonal(expr), ~Q.unitary(expr),
            ~Q.fullrank(expr), ~Q.positive_definite(expr),
            Q.upper_triangular(expr), Q.lower_triangular(expr), Q.diagonal(expr),
            Q.integer_elements(expr)]


@class_fact_registry.multiregister(OneMatrix)
def _(expr):
    facts = [Equivalent(Q.symmetric(expr), Q.square(expr)), Q.integer_elements(expr)]
    for p in [Q.invertible, Q.fullrank, Q.positive_definite, Q.upper_triangular,
              Q.lower_triangular, Q.diagonal]:
        facts.append(p(expr) if _is_1x1(expr) else ~p(expr))
    return facts


@class_fact_registry.multiregister(DiagonalMatrix, DiagMatrix)
def _(expr):
    return [Q.diagonal(expr)]


@class_fact_registry.multiregister(DFT)
def _(expr):
    return [Q.unitary(expr), Q.complex_elements(expr)]


@class_fact_registry.multiregister(Factorization)
def _(expr):
    facts = [p(expr) for p in [Q.orthogonal, Q.unitary, Q.upper_triangular,
             Q.lower_triangular, Q.diagonal] if p in expr.predicates]
    facts.extend(closed_group(expr, Q.real_elements))
    facts.extend(closed_group(expr, Q.complex_elements))
    return facts


### Unary operations ###

@class_fact_registry.multiregister(Inverse)
def _(expr):
    arg = expr.arg
    return [Q.invertible(expr),
            *[Equivalent(p(expr), p(arg)) for p in [Q.symmetric, Q.orthogonal,
              Q.unitary, Q.fullrank, Q.positive_definite, Q.upper_triangular,
              Q.lower_triangular, Q.diagonal, Q.complex_elements]]]


@class_fact_registry.multiregister(Transpose)
def _(expr):
    arg = expr.arg
    return [Equivalent(Q.upper_triangular(expr), Q.lower_triangular(arg)),
            Equivalent(Q.lower_triangular(expr), Q.upper_triangular(arg)),
            *[Equivalent(p(expr), p(arg)) for p in [Q.symmetric, Q.invertible,
              Q.orthogonal, Q.unitary, Q.fullrank, Q.positive_definite, Q.diagonal,
              *_elements_preds]]]


@class_fact_registry.multiregister(MatrixSlice)
def _(expr):
    parent = expr.parent
    facts = [Implies(Q.orthogonal(parent), Q.fullrank(expr)),
             *[Implies(p(parent), p(expr)) for p in _elements_preds]]
    if expr.on_diag:
        facts.extend(Implies(p(parent), p(expr)) for p in [Q.symmetric, Q.invertible,
            Q.orthogonal, Q.unitary, Q.positive_definite, Q.upper_triangular,
            Q.lower_triangular, Q.diagonal])
    return facts


### Explicit and block matrices ###

@class_fact_registry.multiregister(MatrixBase)
def _(expr):
    if not expr.is_square:
        return [~Q.invertible(expr)]
    return [Q.invertible(expr) if expr.rank() == expr.rows else ~Q.invertible(expr)]


@class_fact_registry.multiregister(BlockMatrix)
def _(expr):
    if isinstance(expr, BlockDiagMatrix):
        return []
    blocks = list(expr.blocks)
    if not all(isinstance(b, (MatrixExpr, MatrixBase)) for b in blocks):
        return []
    facts = [Implies(all_(p, blocks), p(expr)) for p in _elements_preds]
    if not expr.is_square:
        return facts
    if expr.blockshape == (1, 1):
        facts.append(Equivalent(Q.invertible(expr), Q.invertible(expr.blocks[0, 0])))
        return facts
    reblocked = reblock_2x2(expr)
    if reblocked.blockshape == (2, 2):
        [[A, B], [C, D]] = reblocked.blocks.tolist()
        for P, schur in [(A, lambda: D - C*Inverse(A)*B), (B, lambda: C - D*Inverse(B)*A),
                         (C, lambda: B - A*Inverse(C)*D), (D, lambda: A - B*Inverse(D)*C)]:
            if isinstance(P, MatrixBase) and P.rank() != P.rows:
                continue
            if (all(isinstance(b, MatrixExpr) for b in (A, B, C, D))
                    and P.is_square and not isinstance(P, ZeroMatrix)):
                facts.append(Implies(Q.invertible(P),
                                     Equivalent(Q.invertible(expr), Q.invertible(schur()))))
    return facts


@class_fact_registry.multiregister(BlockDiagMatrix)
def _(expr):
    if expr.rowblocksizes != expr.colblocksizes:
        return []
    return [Equivalent(Q.invertible(expr), all_(Q.invertible, expr.diag))]


@class_fact_registry.multiregister(Determinant, HadamardProduct, Trace)
def _(expr):
    facts = []
    for pred in _elements_preds:
        facts.extend(closed_group(expr, pred))
    return facts

