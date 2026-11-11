"""What is known of expressions before the search over the rules starts."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.ask import Q
from sympy.assumptions.assume import AppliedPredicate
from sympy.assumptions.number_facts import number_facts
from sympy.core.numbers import Integer
from sympy.core.symbol import Symbol
from sympy.logic.boolalg import And, Not
from sympy.matrices.expressions.blockmatrix import BlockMatrix
from sympy.matrices.expressions.diagonal import DiagonalOf
from sympy.matrices.expressions.kronecker import KroneckerProduct
from sympy.matrices.expressions.matexpr import MatrixExpr, MatrixSymbol
from sympy.matrices.expressions.slice import MatrixSlice
from sympy.matrices.expressions.special import GenericIdentity, GenericZeroMatrix

if TYPE_CHECKING:
    from sympy.assumptions.assume import Predicate
    from sympy.core.basic import Basic
    from sympy.logic.boolalg import Boolean

    # expr -> [(predicate, whether it is true)]
    Known = dict[Basic, list[tuple[Predicate, bool]]]


def preprocess(expr: Basic, assumptions: Boolean | bool) -> Known:
    """What the steps below find for a question about *expr* under *assumptions*."""
    known: Known = {}
    _subexpressions(expr, known)
    _assumed(assumptions, known)
    return known


def _subexpressions(expr: Basic, known: Known) -> None:
    """The facts of numbers, what symbols were declared with and the shapes of matrices."""
    todo = [expr]
    while todo:
        expr = todo.pop()
        if isinstance(expr, MatrixExpr):
            if not isinstance(expr, MatrixSymbol):
                todo.extend(expr.args)
            facts = _shape(expr)
        elif not expr.is_Atom:
            todo.extend(expr.args)
            continue
        elif expr in known:
            continue
        elif isinstance(expr, Symbol):
            facts = _declared(expr)
        else:
            facts = number_facts(expr)
        if facts:
            known[expr] = facts


def _declared(symbol: Symbol) -> list[tuple[Predicate, bool]]:
    """
    ``[(Q.positive, True)]`` for ``Symbol('x', positive=True)``: what the
    symbol was declared with, and nothing which follows from it.
    """
    return [(predicate, value)
            for name, value in symbol._assumptions_orig.items()
            if value is not None
            and (predicate := getattr(Q, name, None)) is not None]


# The first four compute their shapes with Add, Mul or Min, which builds
# expressions and reads the old assumptions. The last two have no shape.
_SHAPE_NOT_READ = (BlockMatrix, DiagonalOf, KroneckerProduct, MatrixSlice,
                   GenericIdentity, GenericZeroMatrix)


def _shape(matrix: MatrixExpr) -> list[tuple[Predicate, bool]] | None:
    """Whether *matrix* is square, and that it is diagonal if it is 1x1 or 0x0."""
    if isinstance(matrix, _SHAPE_NOT_READ):
        return None
    rows, cols = matrix.shape
    if isinstance(rows, (int, Integer)) and isinstance(cols, (int, Integer)):
        if rows != cols:
            return [(Q.square, False)]
        return [(Q.diagonal, True)] if rows <= 1 else [(Q.square, True)]
    return [(Q.square, True)] if rows == cols else None


def _assumed(assumptions: Boolean | bool, known: Known) -> None:
    """Only a predicate, its negation and a conjunction of these are read."""
    literals = assumptions.args if isinstance(assumptions, And) else (assumptions,)
    for literal in literals:
        applied = literal.args[0] if isinstance(literal, Not) else literal
        is_true = not isinstance(literal, Not)
        if isinstance(applied, AppliedPredicate) and len(applied.arguments) == 1:
            known.setdefault(applied.arg, []).append((applied.function, is_true))
