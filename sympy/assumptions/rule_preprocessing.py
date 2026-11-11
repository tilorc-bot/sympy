"""What is known of expressions before the search over the rules starts."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.ask import Q
from sympy.assumptions.assume import AppliedPredicate
from sympy.assumptions.number_facts import EVALUATED, number_facts
from sympy.core.numbers import I
from sympy.core.symbol import Symbol
from sympy.logic.boolalg import And, Not

if TYPE_CHECKING:
    from sympy.assumptions.assume import Predicate
    from sympy.core.basic import Basic
    from sympy.logic.boolalg import Boolean

    # expr -> [(predicate, whether it is true)]; a number in the place of the
    # predicate is for whether expr is that number
    Known = dict[Basic, list[tuple[Predicate | Basic, bool]]]


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


_EQUALITY = {Q.eq: True, Q.ne: False}


def _assumed(assumptions: Boolean | bool, known: Known) -> None:
    """
    Only a predicate, its negation and a conjunction of these are read, and
    ``Q.eq(x, 1)`` and ``Q.ne(x, 1)`` with a rational number or ``I``.
    """
    literals = assumptions.args if isinstance(assumptions, And) else (assumptions,)
    for literal in literals:
        applied = literal.args[0] if isinstance(literal, Not) else literal
        is_true = not isinstance(literal, Not)
        if not isinstance(applied, AppliedPredicate):
            continue
        if len(applied.arguments) == 1:
            expr, facts = applied.arg, [(applied.function, is_true)]
        elif applied.function in _EQUALITY:
            expr, number = applied.arguments
            if not (number.is_Rational or number is I):
                continue
            is_equal = is_true is _EQUALITY[applied.function]
            facts = [(number, is_equal)]
            if is_equal:
                facts += number_facts(number)
        else:
            continue
        before = known.get(expr)
        # not changed in place: the list of a number is shared between calls
        known[expr] = facts if before is None else before + facts

