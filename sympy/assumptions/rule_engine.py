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
    One requirement of a :class:`Rule`: a question, and the answer which it
    must have.

    Explanation
    ===========

    The question is ``predicate``, asked about one part of the expression
    which the rule is used for: the argument ``expr.args[argument]``, or the
    expression itself if ``argument`` is :data:`SELF`.

    The condition holds if the answer to that question is ``value``. It does
    not hold if the answer is the opposite, and it does not hold if there is
    no answer: ``Condition(Q.zero, 0, False)`` needs the argument to be known
    not to be zero.

    Parameters
    ==========

    predicate : Predicate
        The predicate of the question, such as ``Q.even``.

    argument : int
        The index in ``expr.args`` of the argument which the question is
        about, or :data:`SELF` for the expression itself.

    value : bool, optional
        The answer which the question must have. The default is ``True``.

    Examples
    ========

    For ``Abs(x)``: "the argument is even", and "the argument is not zero".

    >>> from sympy import Q
    >>> from sympy.assumptions.rule_engine import SELF, Condition
    >>> Condition(Q.even, 0)
    Condition(predicate=Q.even, argument=0, value=True)
    >>> Condition(Q.zero, 0, False)
    Condition(predicate=Q.zero, argument=0, value=False)

    For ``x**y``: "the exponent is real". For any expression: "the
    expression itself is positive".

    >>> Condition(Q.real, 1)
    Condition(predicate=Q.real, argument=1, value=True)
    >>> Condition(Q.positive, SELF)
    Condition(predicate=Q.positive, argument=-1, value=True)

    """
    predicate: Predicate
    argument: int
    value: bool = True


class Rule(NamedTuple):
    """
    One way to answer a question about an expression: if every condition
    holds, the answer is ``answer``.

    Explanation
    ===========

    A rule does not say which predicate and which class it is for. It is
    stored under them, in the table which :func:`ask_by_rules` takes:
    ``{(class, predicate): (rule, ...)}``.

    The rules of an entry are tried in order, and the first one whose
    conditions all hold gives the answer. A rule whose conditions do not all
    hold says nothing: the answer is not the opposite of ``answer`` then. A
    statement which gives both answers, such as "zero exactly when the
    argument is zero", is written as two rules.

    Parameters
    ==========

    answer : bool
        The truth value of the predicate for the expression.

    conditions : tuple of Condition, optional
        What has to hold. The default is no conditions, for a rule which
        always applies.

    Examples
    ========

    "The absolute value of an even number is even", and "an absolute value
    is not negative":

    >>> from sympy import Abs, Q
    >>> from sympy.abc import x
    >>> from sympy.assumptions.rule_engine import Condition, Rule, ask_by_rules
    >>> rules = {
    ...     (Abs, Q.even): (Rule(True, (Condition(Q.even, 0),)),),
    ...     (Abs, Q.negative): (Rule(False),),
    ... }

    "An absolute value is zero exactly when its argument is", as two rules:

    >>> rules[Abs, Q.zero] = (
    ...     Rule(True, (Condition(Q.zero, 0),)),
    ...     Rule(False, (Condition(Q.zero, 0, False),)))
    >>> ask_by_rules(Q.zero, Abs(x), Q.zero(x), rules)
    True
    >>> ask_by_rules(Q.zero, Abs(x), Q.positive(x), rules)
    False
    >>> print(ask_by_rules(Q.zero, Abs(x), Q.real(x), rules))
    None

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
