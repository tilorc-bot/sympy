"""Depth-first search over rules about expressions and their arguments."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.ask_generated import get_known_facts_dict
from sympy.assumptions.assume import AppliedPredicate
from sympy.logic.boolalg import And, Not

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sympy.assumptions.assume import Predicate
    from sympy.core.basic import Basic
    from sympy.logic.boolalg import Boolean

    Rules = dict[tuple[type[Basic], Predicate, bool],
                 list[tuple[tuple[int, Predicate, bool], ...]]]

# As the argument of a condition: the expression itself
SELF = -1


def index_rules(rows: Iterable[tuple]) -> Rules:
    """
    Index rows ``(class, conclusion, *conditions)`` for :func:`ask_by_rules`.

    Examples
    ========

    >>> from sympy import Abs, Q
    >>> from sympy.abc import x
    >>> from sympy.assumptions.rule_engine import ask_by_rules, index_rules
    >>> rules = index_rules([
    ...     (Abs, Q.even, (0, Q.even)),
    ...     (Abs, ~Q.negative),
    ... ])
    >>> ask_by_rules(Q.even, Abs(x), Q.even(x), rules)
    True
    >>> ask_by_rules(Q.negative, Abs(x), True, rules)
    False

    """
    rules: Rules = {}
    for cls, conclusion, *conditions in rows:
        rules.setdefault((cls, *_literal(conclusion)), []).append(tuple(
            (argument, *_literal(condition)) for argument, condition in conditions))
    return rules


def _literal(literal):
    if isinstance(literal, Not):
        return literal.args[0], False
    return literal, True


def _local_facts(assumptions):
    """
    ``{expr: [(predicate, value), ...]}`` for the assumptions which are a
    predicate of one expression or the negation of one.
    """
    local_facts: dict = {}
    literals = assumptions.args if isinstance(assumptions, And) else (assumptions,)
    for literal in literals:
        predicate, value = _literal(literal)
        if isinstance(predicate, AppliedPredicate) and len(predicate.arguments) == 1:
            local_facts.setdefault(predicate.arg, []).append((predicate.function, value))
    return local_facts


def _ask_single_fact(key, local_facts):
    """
    Whether one of *local_facts*, ``[(predicate, value), ...]`` about one
    expression, implies or refutes the predicate *key* by itself.
    """
    if not local_facts:
        return None
    known_facts = get_known_facts_dict()
    for predicate, value in local_facts:
        if value:
            implied, rejected = known_facts.get(predicate, _NOTHING)
            if key in implied:
                return True
            if key in rejected:
                return False
        elif predicate in known_facts.get(key, _NOTHING)[0]:
            return False
    return None


_NOTHING: tuple = ((), ())


def ask_by_rules(
        predicate: Predicate,
        expr: Basic,
        assumptions: Boolean | bool,
        rules: Rules,
) -> bool | None:
    """Answer ``predicate(expr)`` by a depth-first search over *rules*."""
    return _Search(assumptions, rules).visit(predicate, expr)


class _Search:

    def __init__(self, assumptions, rules):
        self.local_facts = _local_facts(assumptions)
        self.rules = rules
        # finished nodes
        self.answers = {}
        # nodes from the first one to the one which is being visited
        self.path = set()
        self.cycles = 0

    def visit(self, predicate, expr):
        node = (predicate, expr)
        if node in self.answers:
            return self.answers[node]
        if node in self.path:
            self.cycles += 1
            return None
        self.path.add(node)
        cycles = self.cycles
        answer = _ask_single_fact(predicate, self.local_facts.get(expr))
        if answer is None:
            answer = self._from_rules(predicate, expr)
        self.path.remove(node)
        # A node without an answer is finished only if no cycle was closed
        # below it: the node which the cycle led back to may get an answer
        # later, and this one with it.
        if answer is not None or self.cycles == cycles:
            self.answers[node] = answer
        return answer

    def _from_rules(self, predicate, expr):
        for cls in type(expr).__mro__:
            for answer in (True, False):
                for conditions in self.rules.get((cls, predicate, answer), ()):
                    if all(self._holds(condition, expr) for condition in conditions):
                        return answer
        return None

    def _holds(self, condition, expr):
        argument, predicate, value = condition
        target = expr if argument == SELF else expr.args[argument]
        return self.visit(predicate, target) is value
