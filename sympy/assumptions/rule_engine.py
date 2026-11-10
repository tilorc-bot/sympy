"""
Rules about expressions and their arguments, and a depth-first search which
answers questions with them.

A :class:`Rule` gives the truth value of a predicate for an expression when
its conditions hold. A :class:`Condition` is a question about one argument of
the expression, or about the expression itself.

:func:`ask_by_rules` searches a graph. A node is a question: a predicate and
an expression. Its edges go to the questions in the conditions of its rules.
The search is depth-first: it tries the rules of a node one after the other,
and visits the nodes of the conditions of a rule before it goes on.
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
    decide it, and from the rules otherwise. The questions in the conditions
    of a rule are answered in the same way, by a depth-first search.

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
    return _Search(assumptions, rules).visit(predicate, expr)


class _Search:
    """
    One depth-first search.

    ``answers`` has the nodes which are finished, with their answers, so
    that a node is visited once. ``path`` has the nodes from the question
    which was asked to the one which is being visited. An edge to a node on
    the path closes a cycle and is not followed.
    """

    def __init__(self, assumptions, rules):
        self.assumptions = CNF.from_prop(assumptions)
        self.rules = rules
        self.answers = {}
        self.path = set()
        self.cycles = 0

    def visit(self, predicate, expr):
        """
        The answer of the node ``(predicate, expr)``.
        """
        node = (predicate, expr)
        if node in self.answers:
            return self.answers[node]
        if node in self.path:
            self.cycles += 1
            return None
        self.path.add(node)
        cycles = self.cycles
        answer = self._from_assumptions(predicate, expr)
        if answer is None:
            answer = self._from_rules(predicate, expr)
        self.path.remove(node)
        # A node without an answer is finished only if no cycle was closed
        # below it: the node which a cycle led back to may get an answer
        # later, and this one with it.
        if answer is not None or self.cycles == cycles:
            self.answers[node] = answer
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
                    if self.visit(condition, target) is not value:
                        break
                else:
                    return rule.answer
        return None
