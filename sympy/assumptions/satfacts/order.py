"""
Facts for order predicates: positive, negative, zero, etc.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.assumptions.sathandlers import class_fact_registry
from sympy.core import Add, Mul, Pow
from sympy.core.numbers import E, I, pi
from sympy.functions import Abs, acos, acot, asin, atan, exp, factorial, log
from sympy.logic.boolalg import Equivalent, Implies
from sympy.matrices.expressions import Determinant, Trace
from sympy.matrices.expressions.matexpr import MatrixElement

from .common import register_scalar, all_, any_, parity


@register_scalar(Add)
def _(expr):
    args = expr.args
    return [
        Implies(all_(Q.nonnegative, args) & any_(Q.positive, args), Q.positive(expr)),
        Implies(all_(Q.nonpositive, args) & any_(Q.negative, args), Q.negative(expr)),
    ]


@register_scalar(Mul)
def _(expr):
    args = expr.args
    return [
        *parity(args, Q.positive, Q.negative, Q.positive(expr), Q.negative(expr)),
        Implies(all_(Q.nonzero, args), Q.nonzero(expr)),
    ]


def _exp_facts(expr, x):
    facts = [Implies(Q.real(x), Q.positive(expr))]
    if x.has(I):
        facts.append(Implies(Q.imaginary(x),
                             Equivalent(Q.positive(expr), Q.even(x/(I*pi)))))
    return facts


@class_fact_registry.multiregister(exp)
def _(expr):
    return _exp_facts(expr, expr.exp)


@register_scalar(Pow)
def _(expr):
    base, e = expr.base, expr.exp
    if base == E:
        return _exp_facts(expr, e)
    return [
        Implies(Q.positive(base) & Q.real(e), Q.positive(expr)),
        Implies(Q.real(base) & Q.even(e), ~Q.negative(expr)),
        Implies(Q.real(base) & Q.odd(e), Equivalent(Q.negative(expr), Q.negative(base))),
        Implies(Q.real(base) & Q.even(e) & ~Q.zero(base), Q.positive(expr)),
        Implies(Q.real(base) & Q.even(e) & Q.zero(base) & Q.positive(e), ~Q.positive(expr)),
        Implies(Q.negative(base) & Q.odd(e), ~Q.positive(expr)),
        Implies(Q.nonzero(base) & Q.finite(e) & Q.real(expr), Q.nonzero(expr)),
    ]


@class_fact_registry.multiregister(Abs)
def _(expr):
    return [Equivalent(Q.positive(expr), Q.nonzero(expr))]


@class_fact_registry.multiregister(log)
def _(expr):
    x = expr.args[0]
    if x.is_number:
        return []
    return [Implies(Q.real(x) & Q.positive(x - 1), Q.positive(expr)),
            Implies(Q.real(x) & Q.negative(x - 1), ~Q.positive(expr))]


@class_fact_registry.multiregister(factorial)
def _(expr):
    x = expr.args[0]
    return [Implies(Q.integer(x) & Q.positive(x), Q.positive(expr))]


@class_fact_registry.multiregister(Trace, Determinant)
def _(expr):
    return [Implies(Q.positive_definite(expr.arg), Q.positive(expr))]


@class_fact_registry.multiregister(MatrixElement)
def _(expr):
    if expr.i == expr.j:
        return [Implies(Q.positive_definite(expr.parent), Q.positive(expr))]
    return []


@class_fact_registry.multiregister(atan)
def _(expr):
    x = expr.args[0]
    return [Implies(Q.real(x), Equivalent(Q.positive(expr), Q.positive(x)))]


@class_fact_registry.multiregister(asin)
def _(expr):
    x = expr.args[0]
    return [Implies(Q.positive(x) & Q.nonpositive(x - 1), Q.positive(expr)),
            Implies(Q.negative(x) & Q.nonnegative(x + 1), ~Q.positive(expr))]


@class_fact_registry.multiregister(acos)
def _(expr):
    x = expr.args[0]
    return [Implies(Q.negative(x - 1) & Q.nonnegative(x + 1), Q.positive(expr))]


@class_fact_registry.multiregister(acot)
def _(expr):
    x = expr.args[0]
    return [Implies(Q.positive(x), Q.positive(expr)),
            Implies(Q.imaginary(x), ~Q.positive(expr))]

