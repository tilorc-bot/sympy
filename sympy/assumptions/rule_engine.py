"""
Rules about expressions and their arguments, and a depth-first search which
answers questions with them.

A rule is a sequence of conditions. It is stored under a class, a predicate
and a truth value, and says that the predicate has that truth value for an
expression of the class when all the conditions hold. A :class:`Condition`
is a question about one argument of the expression, or about the expression
itself.

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
    from collections.abc import Mapping, Sequence

    from sympy.assumptions.assume import Predicate
    from sympy.core.basic import Basic
    from sympy.logic.boolalg import Boolean

# In a condition: the expression itself, instead of one of its arguments
SELF = -1


class Condition(NamedTuple):
    """
    A question which a rule asks about the expression it is used for, and
    the answer which the rule needs.

    ``Condition(Q.even, 0)`` holds for ``expr`` if ``Q.even(expr.args[0])``
    is found to be true, and ``Condition(Q.zero, 0, False)`` if
    ``Q.zero(expr.args[0])`` is found to be false. With :data:`SELF` as the
    ``argument``, the question is about ``expr`` itself. A question without
    an answer does not make a condition hold.
    """
    predicate: Predicate
    argument: int
    value: bool = True


def ask_by_rules(
        predicate: Predicate,
        expr: Basic,
        assumptions: Boolean | bool,
        rules: Mapping[tuple[type[Basic], Predicate, bool], Sequence[Sequence[Condition]]],
) -> bool | None:
    """
    The truth value of ``predicate(expr)`` under *assumptions*, or ``None``
    if the rules do not give it.

    Explanation
    ===========

    *rules* maps ``(class, predicate, truth value)`` to the rules which give
    the predicate that truth value for the expressions of the class. A rule
    is a sequence of conditions, and it applies when all of them hold. A
    rule without conditions always applies. The rules of the classes which
    the class of *expr* derives from are tried too, and the first rule which
    applies gives the answer.

    A question is answered from the assumptions about its expression if they
    decide it, and from the rules otherwise. The questions in the conditions
    of a rule are answered in the same way, by a depth-first search.

    Examples
    ========

    The absolute value of an even number is even, and an absolute value is
    not negative:

    >>> from sympy import Abs, Q
    >>> from sympy.abc import x
    >>> from sympy.assumptions.rule_engine import Condition, ask_by_rules
    >>> rules = {(Abs, Q.even, True): [(Condition(Q.even, 0),)],
    ...          (Abs, Q.negative, False): [()]}
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
        for cls in type(expr).__mro__:
            for answer in (True, False):
                for conditions in self.rules.get((cls, predicate, answer), ()):
                    if all(self._holds(condition, expr) for condition in conditions):
                        return answer
        return None

    def _holds(self, condition, expr):
        predicate, argument, value = condition
        target = expr if argument == SELF else expr.args[argument]
        return self.visit(predicate, target) is value
