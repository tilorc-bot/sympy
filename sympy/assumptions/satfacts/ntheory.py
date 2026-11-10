"""
Facts for number theory predicates: prime, composite, even, odd.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.assumptions.sathandlers import class_fact_registry
from sympy.core import Add, Mul, Pow, S
from sympy.core.numbers import Number
from sympy.functions import Abs, im, re
from sympy.logic.boolalg import Equivalent, Implies

from .common import register_scalar, all_, parity


@register_scalar(Mul)
def _(expr):
    args = expr.args
    facts = []
    if any(a.is_number and a.is_composite for a in args):
        facts.append(Implies(all_(Q.integer, args), ~Q.prime(expr)))
    for a, b in zip(args, args[1:]):
        if a.free_symbols & b.free_symbols:
            facts.append(Implies(Q.integer(a) & Q.integer(b) & Q.odd(a + b),
                                 Q.even(expr)))
    return facts


@register_scalar(Add)
def _(expr):
    return parity(expr.args, Q.even, Q.odd, Q.even(expr), Q.odd(expr))


@register_scalar(Pow)
def _(expr):
    base, exp = expr.base, expr.exp
    ints = Q.integer(base) & Q.integer(exp)
    facts = [
        Implies(ints & ~Q.prime(base), ~Q.prime(expr)),
        Implies(ints & Q.ne(exp, 1), ~Q.prime(expr)),
        Implies(ints & Q.positive(exp), Equivalent(Q.even(expr), Q.even(base))),
        Implies(Q.integer(exp) & ~Q.negative(exp) & Q.odd(base), Q.odd(expr)),
    ]
    if exp == 1:
        facts.append(Equivalent(Q.prime(expr), Q.prime(base)))
    elif isinstance(exp, Number):
        facts.append(Implies(ints, ~Q.prime(expr)))
    if base is S.NegativeOne:
        facts.append(Implies(Q.integer(exp), Q.odd(expr)))
    return facts


@class_fact_registry.multiregister(Abs, re)
def _(expr):
    arg = expr.args[0]
    return [Implies(Q.real(arg), Equivalent(Q.even(expr), Q.even(arg)))]


@class_fact_registry.multiregister(im)
def _(expr):
    return [Implies(Q.real(expr.args[0]), Q.even(expr))]
