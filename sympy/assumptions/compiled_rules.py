"""
Access to the rules which are compiled from ``sympy/assumptions/rules``.

A rule is written about a generic expression ``f(x)`` or ``f(x, y)``. In
its compiled form it refers to the expressions it is about by *slots*:
slot ``i`` is the ``i``-th of the :func:`rule_arguments` of an expression,
and slot ``-1`` is the expression itself.
"""
from __future__ import annotations

from sympy.assumptions.sat_rules_generated import SAT_RULES
from sympy.core.add import Add
from sympy.core.mul import Mul

FIRST_AND_REST = (Add, Mul)

_sat_rules: dict = {}


def rule_arguments(expr):
    """
    The expressions which the slots of a rule about *expr* stand for.

    Explanation
    ===========

    These are the arguments of *expr*, except that a sum or a product of
    more than two arguments is read as its first argument and the sum or
    the product of the others. Rules about ``f(x, y)`` then apply to sums
    and products of any number of arguments.

    Examples
    ========

    >>> from sympy import sin
    >>> from sympy.abc import x, y, z
    >>> from sympy.assumptions.compiled_rules import rule_arguments
    >>> rule_arguments(sin(x))
    (x,)
    >>> rule_arguments(x*y*z)
    (x, y*z)

    """
    args = expr.args
    if len(args) > 2 and isinstance(expr, FIRST_AND_REST):
        return (args[0], expr._from_args(args[1:]))
    return args


def sat_rules(cls, nargs):
    """
    The compiled clauses which hold for the instances of *cls* that have
    *nargs* rule arguments.

    Explanation
    ===========

    A clause is a tuple of literals ``(predicate, slot, value)``, at least
    one of which is true: the predicate has the truth value ``value`` for
    the expression of the slot.

    Examples
    ========

    >>> from sympy import Abs, Q
    >>> from sympy.assumptions.compiled_rules import sat_rules
    >>> ((Q.even, 0, False), (Q.even, -1, True)) in sat_rules(Abs, 1)
    True

    """
    key = (cls, nargs)
    rules = _sat_rules.get(key)
    if rules is None:
        rules = _sat_rules[key] = tuple(
            clause for base in cls.__mro__
            for clause in SAT_RULES.get((base, nargs), ()))
    return rules
