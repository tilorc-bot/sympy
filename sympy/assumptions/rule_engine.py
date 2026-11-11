"""Depth-first search over rules about expressions and their arguments."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.ask_generated import get_known_facts_dict
from sympy.assumptions.assume import AppliedPredicate
from sympy.logic.boolalg import And, Not
from sympy.utilities.iterables import strongly_connected_components

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sympy.assumptions.assume import Predicate
    from sympy.core.basic import Basic
    from sympy.logic.boolalg import Boolean

    RuleKind = int
    # (FIRST_ARG_IS, Q.even): Q.even is true of the first argument
    Condition = tuple[tuple[int, bool], Predicate]
    # all of the conditions must hold
    Rule = tuple[RuleKind, list[Condition]]
    Rules = dict[tuple[type[Basic], Predicate], list[Rule]]

FALSE_IF: RuleKind = 0
TRUE_IF: RuleKind = 1
# also false if a condition does not hold
IF_AND_ONLY_IF: RuleKind = 2

ALWAYS_FALSE: Rule = (FALSE_IF, [])
ALWAYS_TRUE: Rule = (TRUE_IF, [])

# As an argument: the expression itself
SELF = -1

# (argument, whether the predicate is true of it)
FIRST_ARG_IS = (0, True)
FIRST_ARG_IS_NOT = (0, False)
SECOND_ARG_IS = (1, True)
SECOND_ARG_IS_NOT = (1, False)
SELF_IS = (SELF, True)
SELF_IS_NOT = (SELF, False)

# As an argument: all of the arguments, any of them, how many of them, and the
# ones which did not have it in the nearest ONE_ARG, EVEN_NUMBER_OF_ARGS or
# ODD_NUMBER_OF_ARGS condition before it
ALL_ARGS = -2
ANY_ARG = -3
ONE_ARG = -4
EVEN_NUMBER_OF_ARGS = -5
ODD_NUMBER_OF_ARGS = -6
OTHER_ARGS = -7

ALL_ARGS_ARE = (ALL_ARGS, True)
ALL_ARGS_ARE_NOT = (ALL_ARGS, False)
ANY_ARG_IS = (ANY_ARG, True)
ANY_ARG_IS_NOT = (ANY_ARG, False)
ONE_ARG_IS = (ONE_ARG, True)
ONE_ARG_IS_NOT = (ONE_ARG, False)
EVEN_NUMBER_OF_ARGS_ARE = (EVEN_NUMBER_OF_ARGS, True)
EVEN_NUMBER_OF_ARGS_ARE_NOT = (EVEN_NUMBER_OF_ARGS, False)
ODD_NUMBER_OF_ARGS_ARE = (ODD_NUMBER_OF_ARGS, True)
ODD_NUMBER_OF_ARGS_ARE_NOT = (ODD_NUMBER_OF_ARGS, False)
OTHER_ARGS_ARE = (OTHER_ARGS, True)
OTHER_ARGS_ARE_NOT = (OTHER_ARGS, False)


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

    The rules must pass :func:`check_no_cycles`.

    Examples
    ========

    >>> from sympy import Abs, Q
    >>> from sympy.abc import x
    >>> from sympy.assumptions.rule_engine import (ALWAYS_FALSE, FALSE_IF,
    ...     FIRST_ARG_IS, TRUE_IF, ask_by_rules)
    >>> rules = {
    ...     (Abs, Q.even): [
    ...         (TRUE_IF, [(FIRST_ARG_IS, Q.even)]),
    ...         (FALSE_IF, [(FIRST_ARG_IS, Q.odd)]),
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
    return _RuleEngine(assumptions, rules).visit(predicate, expr)


def check_no_cycles(rules: Rules) -> None:
    """Raise ``ValueError`` if conditions about SELF form a cycle of predicates."""
    edges = {
        (predicate, condition_predicate)
        for (_, predicate), rules_for_predicate in rules.items()
        for _, conditions in rules_for_predicate
        for (argument, _), condition_predicate in conditions
        if argument == SELF
    }
    vertices = {vertex for edge in edges for vertex in edge}
    graph = (sorted(vertices, key=str), sorted(edges, key=str))
    for component in strongly_connected_components(graph):
        if len(component) > 1 or (component[0], component[0]) in edges:
            names = ', '.join(sorted(map(str, component)))
            raise ValueError(f'the rules have a cycle: {names}')


class _RuleEngine:

    def __init__(self, assumptions: Boolean | bool, rules: Rules):
        self.unary_facts_engine = _UnaryFactsEngine(assumptions)
        self.rules = rules
        self.answers: dict[tuple[Predicate, Basic], bool | None] = {}

    def visit(self, predicate: Predicate, expr: Basic) -> bool | None:
        node = (predicate, expr)
        if node in self.answers:
            return self.answers[node]
        answer = self.unary_facts_engine.ask_single_fact(predicate, expr)
        if answer is None:
            answer = self._from_rules(predicate, expr)
        self.answers[node] = answer
        return answer

    def _from_rules(self, predicate: Predicate, expr: Basic) -> bool | None:
        for cls in type(expr).__mro__:
            for kind, conditions in self.rules.get((cls, predicate), ()):
                answer = self._apply(kind, conditions, expr)
                if answer is not None:
                    return answer
        return None

    def _apply(
            self,
            kind: RuleKind,
            conditions: list[Condition],
            expr: Basic,
    ) -> bool | None:
        others: list[Basic] | None = None
        for (argument, expected), predicate in conditions:
            if argument >= SELF:
                target = expr if argument == SELF else expr.args[argument]
                value = self.visit(predicate, target)
                if value is expected:
                    continue
            else:
                value, others = self._about_args(
                    argument, expected, predicate, expr, others)
                if value:
                    continue
            if value is not None and kind == IF_AND_ONLY_IF:
                return False
            return None
        return kind != FALSE_IF

    def _about_args(
            self,
            argument: int,
            expected: bool,
            predicate: Predicate,
            expr: Basic,
            others: list[Basic] | None,
    ) -> tuple[bool | None, list[Basic] | None]:
        """Whether a condition about the arguments holds, and what OTHER_ARGS means."""
        if argument == OTHER_ARGS:
            if others is None:
                raise ValueError('OTHER_ARGS needs a ONE_ARG, EVEN_NUMBER_OF_ARGS'
                                 ' or ODD_NUMBER_OF_ARGS condition before it')
            args: Sequence[Basic] = others
        else:
            args = expr.args
        if not expr.args:
            return None, others
        if argument == ALL_ARGS or argument == OTHER_ARGS:
            holds: bool | None = True
            for arg in args:
                value = self.visit(predicate, arg)
                if value is not expected:
                    if value is not None:
                        return False, others
                    holds = None
            return holds, others
        if argument == ANY_ARG:
            holds = False
            for arg in args:
                value = self.visit(predicate, arg)
                if value is expected:
                    return True, others
                if value is None:
                    holds = None
            return holds, others
        rest = []
        for arg in args:
            value = self.visit(predicate, arg)
            if value is None:
                return None, others
            if value is not expected:
                rest.append(arg)
        count = len(args) - len(rest)
        if argument == ONE_ARG:
            return count == 1, rest
        if argument == EVEN_NUMBER_OF_ARGS:
            return count % 2 == 0, rest
        return count % 2 == 1, rest
