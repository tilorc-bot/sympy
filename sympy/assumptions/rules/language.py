"""
The words which the rule files of this package are written in.

A rule file holds one tuple, ``RULES``, of :func:`for_all` statements::

    RULES = (
        # Real on the reals
        for_all((sin, cos),
            closed(f(x), Q.real)),

        # Sign of a product
        #     x is the first factor and y the product of the others
        for_all((Mul,),
            (Q.positive(x) & Q.negative(y)) >> Q.negative(f(x, y)),
            (Q.negative(x) & Q.positive(y)) >> Q.negative(f(x, y))),
    )

A statement names the classes it is about and gives *rows*. A row is a
formula about the generic expression ``f(x)`` or ``f(x, y)`` and its
arguments, with ``f`` standing for each of the classes. It is written with
predicates of ``Q`` and the operators ``&``, ``|``, ``~``, ``>>`` and
``Equivalent``, and it holds for every value of ``x`` and ``y``.

A sum or a product has any number of arguments. A row about one is written
for ``f(x, y)``, where ``x`` is its first argument and ``y`` is the sum or
the product of the others. A row about a power is written for
``f(base, exponent)``.

A row can also be about one expression alone. It is then written with ``x``
and without ``f``, and holds for every instance ``x`` of the classes::

    # A real number which is not rational is irrational
    for_all((Expr,),
        (Q.real(x) & ~Q.rational(x)) >> Q.irrational(x)),

A row for every expression (``Expr`` or ``Basic``) says nothing new: it must
follow from the facts between the predicates in
:mod:`sympy.assumptions.facts`. It tells how the truth value of one
predicate is found from other predicates of the same expression.

Above each statement is a comment with the name of the property and, under
it and indented, the reason for which it is true.

Python binds ``>>`` tighter than ``&``, so the conditions of a row are
written in parentheses: ``a & b >> c`` is ``a & (b >> c)``.
"""
from __future__ import annotations

from typing import NamedTuple

from sympy.assumptions.assume import AppliedPredicate
from sympy.core.function import AppliedUndef, Function
from sympy.core.symbol import Symbol
from sympy.logic.boolalg import And, Boolean, Implies

x = Symbol('x')
y = Symbol('y')
base = Symbol('base')
exponent = Symbol('exponent')
f = Function('f')


class ForAll(NamedTuple):
    """A :func:`for_all` statement."""
    classes: tuple
    rows: tuple


def for_all(classes, *rows):
    """
    The *rows* hold for the instances of each of the *classes*.

    Examples
    ========

    >>> from sympy import Abs, Q
    >>> from sympy.assumptions.rules.language import f, for_all, x
    >>> statement = for_all((Abs,), Q.even(x) >> Q.even(f(x)))
    >>> statement.rows
    (Implies(Q.even(x), Q.even(f(x))),)

    """
    flat = []
    for row in rows:
        flat.extend(row if isinstance(row, tuple) else (row,))
    for row in flat:
        node(row)
    return ForAll(tuple(classes), tuple(flat))


def closed(expr, *predicates):
    """
    Rows which say that *expr* has each of the *predicates* when all of its
    arguments have it.

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.assumptions.rules.language import closed, f, x, y
    >>> closed(f(x, y), Q.integer)
    (Implies(Q.integer(x) & Q.integer(y), Q.integer(f(x, y))),)

    """
    return tuple(Implies(And(*[p(arg) for arg in expr.args]), p(expr))
                 for p in predicates)


def node(row):
    """
    The generic expression which *row* is about.

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.assumptions.rules.language import f, node, x
    >>> node(Q.zero(x) >> Q.zero(f(x)))
    f(x)
    >>> node(Q.zero(x) >> Q.real(x))
    x

    """
    if not isinstance(row, Boolean):
        raise TypeError(f"the row {row} is not a formula")
    if isinstance(row, And):
        raise ValueError(
            f"the row {row} is a conjunction: put the conditions in "
            "parentheses, because >> binds tighter than &")
    nodes = [e for e in row.atoms(AppliedUndef) if e.func == f]
    if not nodes:
        nodes = list(row.free_symbols)
    if len(nodes) != 1:
        raise ValueError(f"the row {row} must be about one expression")
    expr, = nodes
    args = expr.args
    if not all(isinstance(arg, Symbol) for arg in args) or len(set(args)) != len(args):
        raise ValueError(f"the arguments of {expr} must be distinct symbols")
    for literal in row.atoms(AppliedPredicate):
        if len(literal.arguments) != 1 or literal.arg not in (expr, *args):
            raise ValueError(
                f"{literal} in the row {row} is not about {expr} or one of "
                "its arguments")
    return expr
