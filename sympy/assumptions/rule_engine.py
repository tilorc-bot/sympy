"""
Backward chaining over rules about expressions and their arguments.

A :class:`Rule` gives the truth value of a predicate for an expression when
its conditions hold. A :class:`Condition` is a question about one argument of
the expression, or about the expression itself. :func:`ask_by_rules` answers
a question by trying the rules for the class of the expression, and answers
the questions of their conditions in the same way.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from sympy.assumptions.ask import _ask_single_fact, _extract_all_facts
from sympy.assumptions.cnf import CNF

if TYPE_CHECKING:
    from sympy.assumptions.assume import Predicate

# In a condition: the expression itself, instead of one of its arguments
SELF = -1


class Condition(NamedTuple):
    """
    ``predicate`` has the truth value ``value`` for the argument of the
    expression at the index ``argument``, or for the expression itself if
    ``argument`` is :data:`SELF`.
    """
    predicate: Predicate
    argument: int
    value: bool = True


class Rule(NamedTuple):
    """
    The predicate which the rule is for has the truth value ``answer`` when
    every one of the ``conditions`` holds.
    """
    answer: bool
    conditions: tuple[Condition, ...] = ()


def ask_by_rules(predicate, expr, assumptions, rules):
    """
    The truth value of ``predicate(expr)`` under *assumptions*, or ``None``
    if the rules do not give it.

    Explanation
    ===========

    *rules* maps ``(class, predicate)`` to the rules for that predicate and
    the expressions of that class. The rules of the classes which the class
    of *expr* derives from are tried too. The first rule whose conditions all
    hold gives the answer.

    A question is answered from the assumptions about its expression if they
    decide it, and from the rules otherwise.

    Examples
    ========

    >>> from sympy import Abs, Q
    >>> from sympy.abc import x
    >>> from sympy.assumptions.rule_engine import Condition, Rule, ask_by_rules
    >>> rules = {(Abs, Q.even): (Rule(True, (Condition(Q.even, 0),)),),
    ...          (Abs, Q.negative): (Rule(False),)}
    >>> ask_by_rules(Q.even, Abs(Abs(x)), Q.even(x), rules)
    True
    >>> ask_by_rules(Q.negative, Abs(x), True, rules)
    False
    >>> print(ask_by_rules(Q.even, Abs(x), True, rules))
    None

    """
    return _Chain(assumptions, rules).ask(predicate, expr)


class _Chain:
    """
    One run of backward chaining.

    It keeps the answers which were found, so that a question is answered
    once, and the questions which are being answered, so that a rule which
    leads back to its own question is not followed again.
    """

    def __init__(self, assumptions, rules):
        self.assumptions = CNF.from_prop(assumptions)
        self.rules = rules
        self.answers = {}
        self.being_answered = set()
        self.cut_short = 0

    def ask(self, predicate, expr):
        question = (predicate, expr)
        if question in self.answers:
            return self.answers[question]
        if question in self.being_answered:
            self.cut_short += 1
            return None
        self.being_answered.add(question)
        cut_short = self.cut_short
        answer = self._from_assumptions(predicate, expr)
        if answer is None:
            answer = self._from_rules(predicate, expr)
        self.being_answered.remove(question)
        # No answer may be for lack of a question which was cut short, and
        # which has an answer later.
        if answer is not None or self.cut_short == cut_short:
            self.answers[question] = answer
        return answer

    def _from_assumptions(self, predicate, expr):
        facts = _extract_all_facts(self.assumptions, (expr,))
        return _ask_single_fact(predicate, facts)

    def _from_rules(self, predicate, expr):
        args = expr.args
        for cls in type(expr).__mro__:
            for rule in self.rules.get((cls, predicate), ()):
                for condition, argument, value in rule.conditions:
                    target = expr if argument == SELF else args[argument]
                    if self.ask(condition, target) is not value:
                        break
                else:
                    return rule.answer
        return None
