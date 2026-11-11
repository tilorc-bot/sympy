"""Depth-first search over rules about expressions and their arguments."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.ask_generated import get_known_facts_dict
from sympy.assumptions.assume import AppliedPredicate
from sympy.logic.boolalg import And, Not

if TYPE_CHECKING:
    from sympy.assumptions.assume import Predicate
    from sympy.core.basic import Basic
    from sympy.logic.boolalg import Boolean

    RuleKind = int
    # (argument, the predicate which must be true of it)
    Condition = tuple[int, Predicate]
    # all of the conditions must hold
    Rule = tuple[RuleKind, list[Condition]]
    Rules = dict[tuple[type[Basic], Predicate], list[Rule]]

FALSE_IF: RuleKind = 0
TRUE_IF: RuleKind = 1
# also false if a condition is false
IF_AND_ONLY_IF: RuleKind = 2

ALWAYS_FALSE: Rule = (FALSE_IF, [])
ALWAYS_TRUE: Rule = (TRUE_IF, [])

FIRST_ARG = 0
SECOND_ARG = 1
# the expression itself
SELF = -1


class _UnaryFactsEngine:
    """Answers from the assumed predicates and the known unary facts."""

    def __init__(self, assumptions: Boolean | bool):
        # expr -> [(predicate, whether it is true)]. Only a predicate, its
        # negation and a conjunction of these are read.
        self.assumed: dict[Basic, list[tuple[Predicate, bool]]] = {}
        literals = assumptions.args if isinstance(assumptions, And) else (assumptions,)
        for literal in literals:
            applied = literal.args[0] if isinstance(literal, Not) else literal
            is_true = not isinstance(literal, Not)
            if isinstance(applied, AppliedPredicate) and len(applied.arguments) == 1:
                self.assumed.setdefault(applied.arg, []).append((applied.function, is_true))

    def ask_single_fact(self, key: Predicate, expr: Basic) -> bool | None:
        """Whether one predicate assumed of *expr* decides *key* by itself."""
        assumed = self.assumed.get(expr)
        if not assumed:
            return None
        # predicate -> (the predicates which it implies, the ones which it excludes)
        known_facts: dict[Predicate, tuple[set[Predicate], set[Predicate]]]
        known_facts = get_known_facts_dict()
        implied_by_key, _ = known_facts.get(key, _NOTHING)
        for predicate, is_true in assumed:
            if is_true:
                implied, excluded = known_facts.get(predicate, _NOTHING)
                if key in implied:
                    return True
                if key in excluded:
                    return False
            elif predicate in implied_by_key:
                # key would imply predicate, which is false
                return False
        return None


_NOTHING: tuple[set, set] = (set(), set())


def ask_by_rules(
        predicate: Predicate,
        expr: Basic,
        assumptions: Boolean | bool,
        rules: Rules,
) -> bool | None:
    """
    Answer ``predicate(expr)`` by a depth-first search over *rules*.

    Examples
    ========

    >>> from sympy import Abs, Q
    >>> from sympy.abc import x
    >>> from sympy.assumptions.rule_engine import (ALWAYS_FALSE, FALSE_IF,
    ...     FIRST_ARG, TRUE_IF, ask_by_rules)
    >>> rules = {
    ...     (Abs, Q.even): [
    ...         (TRUE_IF, [(FIRST_ARG, Q.even)]),
    ...         (FALSE_IF, [(FIRST_ARG, Q.odd)]),
    ...     ],
    ...     (Abs, Q.negative): [
    ...         ALWAYS_FALSE,
    ...     ],
    ... }
    >>> ask_by_rules(Q.even, Abs(x), Q.even(x), rules)
    True
    >>> ask_by_rules(Q.even, Abs(x), Q.odd(x), rules)
    False
    >>> ask_by_rules(Q.negative, Abs(x), True, rules)
    False

    """
    return _Search(assumptions, rules).visit(predicate, expr)


class _Search:

    def __init__(self, assumptions, rules):
        self.unary_facts_engine = _UnaryFactsEngine(assumptions)
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
        answer = self.unary_facts_engine.ask_single_fact(predicate, expr)
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
            for kind, conditions in self.rules.get((cls, predicate), ()):
                answer = self._apply(kind, conditions, expr)
                if answer is not None:
                    return answer
        return None

    def _apply(self, kind, conditions, expr):
        for argument, predicate in conditions:
            target = expr if argument == SELF else expr.args[argument]
            value = self.visit(predicate, target)
            if value is not True:
                if value is False and kind == IF_AND_ONLY_IF:
                    return False
                return None
        return kind != FALSE_IF
