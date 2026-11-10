"""
Facts for calculus predicates: finite, infinite, etc.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.assumptions.sathandlers import class_fact_registry
from sympy.core import Add, Mul, Pow
from sympy.core.numbers import E
from sympy.functions import cos, exp, log, sign, sin
from sympy.logic.boolalg import Implies, Or

from .common import register_scalar, MAX_ENUMERATED_ARGS, all_, any_, each_with_rest


@register_scalar(Add)
def _(expr):
    args = expr.args
    facts = [
        Implies(all_(Q.finite, args), Q.finite(expr)),
        *each_with_rest(args, lambda a: ~Q.finite(a), Q.finite, ~Q.finite(expr)),
    ]
    if len(args) <= MAX_ENUMERATED_ARGS:
        for inf in (Q.positive_infinite, Q.negative_infinite):
            facts.append(Implies(all_(lambda a: Or(Q.finite(a), inf(a)), args)
                                 & any_(inf, args), ~Q.finite(expr)))
            facts.append(Implies(all_(lambda a: Or(Q.real(a), inf(a)), args)
                                 & any_(inf, args), inf(expr)))
    return facts


@register_scalar(Mul)
def _(expr):
    args = expr.args
    return [
        Implies(all_(Q.finite, args), Q.finite(expr)),
        Implies(any_(lambda a: ~Q.finite(a), args) & all_(lambda a: ~Q.zero(a), args),
                ~Q.finite(expr)),
    ]


def _exp_facts(expr, x):
    return [Implies(Q.finite(x), Q.finite(expr)),
            Implies(Q.positive_infinite(x), ~Q.finite(expr))]


@class_fact_registry.multiregister(exp)
def _(expr):
    return _exp_facts(expr, expr.exp)


@register_scalar(Pow)
def _(expr):
    base, e = expr.base, expr.exp
    if base == E:
        return _exp_facts(expr, e)
    facts = [
        Implies(~Q.finite(base) & Q.extended_positive(e), ~Q.finite(expr)),
        Implies(Q.finite(base) & Q.finite(e) & Q.zero(base) & Q.negative(e), ~Q.finite(expr)),
        Implies(Q.finite(base) & Q.finite(e) & ~Q.zero(base), Q.finite(expr)),
        Implies(Q.finite(base) & Q.finite(e) & Q.nonnegative(e), Q.finite(expr)),
    ]
    if base.is_number:
        if (abs(base) <= 1) == True:
            facts.append(Implies(Q.extended_positive(e), Q.finite(expr)))
        if (abs(base) >= 1) == True:
            facts.append(Implies(Q.extended_negative(e), Q.finite(expr)))
        if (abs(base) > 1) == True:
            facts.append(Implies(Q.positive_infinite(e), ~Q.finite(expr)))
    return facts


@class_fact_registry.multiregister(log)
def _(expr):
    x = expr.args[0]
    return [Implies(Q.infinite(x), ~Q.finite(expr)),
            Implies(Q.zero(x), ~Q.finite(expr)),
            Implies(Q.finite(x) & ~Q.zero(x), Q.finite(expr))]


@class_fact_registry.multiregister(cos, sin, sign)
def _(expr):
    return [Q.finite(expr)]
