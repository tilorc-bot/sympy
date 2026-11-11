"""Depth-first search over rules about expressions and their arguments."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.ask_generated import get_number_facts_combinations
from sympy.assumptions.rule_preprocessing import preprocess

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sympy.assumptions.assume import Predicate
    from sympy.assumptions.rule_preprocessing import Known
    from sympy.core.basic import Basic
    from sympy.logic.boolalg import Boolean

    RuleKind = int
    # (FIRST_ARG_IS, Q.even): Q.even is true of the first argument
    # (FIRST_ARG_IS, S.NegativeOne): the first argument is the number -1; only
    # S.One, S.NegativeOne, S.Half and S.ImaginaryUnit, which are compared with "is"
    Condition = tuple[tuple[int, bool], Predicate | Basic]
    # all of the conditions must hold
    Rule = tuple[RuleKind, list[Condition]]
    Rules = dict[tuple[type[Basic], Predicate | Basic], list[Rule]]

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
    """Answers from what is known before the search and the known unary facts."""

    def __init__(self, known: Known):
        self.known = known
        self.where_true = get_number_facts_combinations()
        self.possible: dict[Basic, int] = {}

    def ask_single_fact(self, key: Predicate | Basic, expr: Basic) -> bool | None:
        """Whether what is known of *expr* decides *key*."""
        possible = self.possible.get(expr)
        if possible is None:
            known = self.known.get(expr)
            possible = self.possible[expr] = self._possible(known) if known else 0
        if not possible:
            return None
        where_true = self.where_true.get(key)
        if where_true is None:
            return self._about_itself(key, expr)
        common = possible & where_true
        if common == possible:
            return True
        if not common:
            return False
        return None

    def _possible(self, known: list[tuple[Predicate | Basic, bool]]) -> int:
        """The combinations of true and false which the number facts and *known* allow."""
        # every combination
        possible = -1
        for entry, is_true in known:
            where_true = self.where_true.get(entry)
            if where_true is not None:
                possible &= where_true if is_true else ~where_true
        return possible

    def _about_itself(self, key: Predicate | Basic, expr: Basic) -> bool | None:
        """What is known of *expr* about the number or predicate *key* itself."""
        if key is expr:
            return True
        for entry, is_true in self.known[expr]:
            if entry is key:
                return is_true
        return None


def ask_by_rules(
        predicate: Predicate,
        expr: Basic,
        assumptions: Boolean | bool,
        rules: Rules,
) -> bool | None:
    """
    Answer ``predicate(expr)`` by a depth-first search over *rules*.

    The rules must pass :func:`~sympy.assumptions.rule_checks.check_no_cycles`.

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
    return _RuleEngine(preprocess(expr, assumptions), rules).visit(predicate, expr)


class _RuleEngine:

    def __init__(self, known: Known, rules: Rules):
        self.unary_facts_engine = _UnaryFactsEngine(known)
        self.rules = rules
        self.answers: dict[tuple[Predicate | Basic, Basic], bool | None] = {}

    def visit(self, predicate: Predicate | Basic, expr: Basic) -> bool | None:
        node = (predicate, expr)
        if node in self.answers:
            return self.answers[node]
        answer = self.unary_facts_engine.ask_single_fact(predicate, expr)
        if answer is None:
            answer = self._from_rules(predicate, expr)
        self.answers[node] = answer
        return answer

    def _from_rules(self, predicate: Predicate | Basic, expr: Basic) -> bool | None:
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
