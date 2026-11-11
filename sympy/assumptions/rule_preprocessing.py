"""What is known of expressions before the search over the rules starts."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.ask import Q
from sympy.assumptions.assume import AppliedPredicate
from sympy.assumptions.number_facts import EVALUATED, number_facts
from sympy.core.symbol import Symbol
from sympy.logic.boolalg import And, Not

if TYPE_CHECKING:
    from sympy.assumptions.assume import Predicate
    from sympy.core.basic import Basic
    from sympy.logic.boolalg import Boolean

    # expr -> [(predicate, whether it is true)]
    Known = dict[Basic, list[tuple[Predicate, bool]]]


def preprocess(expr: Basic, assumptions: Boolean | bool) -> Known:
    """What the steps below find for a question about *expr* under *assumptions*."""
    known: Known = {}
    if _subexpressions(expr, known):
        _compound_number(expr, known)
    _assumed(assumptions, known)
    return known


def _subexpressions(expr: Basic, known: Known) -> bool:
    """The facts of numbers and what symbols were declared with; whether *expr* is a number."""
    if expr.is_Atom:
        if expr not in known:
            facts = _declared(expr) if isinstance(expr, Symbol) else number_facts(expr)
            if facts:
                known[expr] = facts
        return type(expr) in EVALUATED
    numbers = [arg for arg in expr.args if _subexpressions(arg, known)]
    if len(numbers) == len(expr.args) and type(expr) in EVALUATED:
        return True
    for number in numbers:
        _compound_number(number, known)
    return False


def _compound_number(number: Basic, known: Known) -> None:
    """The facts of *number* as a whole; an atom has them already."""
    if not number.is_Atom and number not in known:
        facts = number_facts(number)
        if facts:
            known[number] = facts


def _declared(symbol: Symbol) -> list[tuple[Predicate, bool]]:
    """
    ``[(Q.positive, True)]`` for ``Symbol('x', positive=True)``: what the
    symbol was declared with, and nothing which follows from it.
    """
    return [(predicate, value)
            for name, value in symbol._assumptions_orig.items()
            if value is not None
            and (predicate := getattr(Q, name, None)) is not None]


def _assumed(assumptions: Boolean | bool, known: Known) -> None:
    """Only a predicate, its negation and a conjunction of these are read."""
    literals = assumptions.args if isinstance(assumptions, And) else (assumptions,)
    for literal in literals:
        applied = literal.args[0] if isinstance(literal, Not) else literal
        is_true = not isinstance(literal, Not)
        if isinstance(applied, AppliedPredicate) and len(applied.arguments) == 1:
            known.setdefault(applied.arg, []).append((applied.function, is_true))
