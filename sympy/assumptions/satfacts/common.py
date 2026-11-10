"""
Helpers, facts bridging the old assumptions system, and facts for
``Q.commutative``.
"""
from __future__ import annotations

from itertools import product

from sympy.assumptions.ask import Q
from sympy.assumptions.sathandlers import ClassFactRegistry, class_fact_registry
from sympy.core import Add, Basic, Expr, Mul, Pow, S, Symbol
from sympy.core.numbers import NaN, Number
from sympy.logic.boolalg import And, Equivalent, Implies, Or
from sympy.matrices.expressions.matexpr import MatrixExpr


default_fact_registry = ClassFactRegistry()
"""
Registry of facts which hold unless the assumptions state otherwise. Each
handler must return literals. ``satask`` drops a literal whose negation is a
unit clause of the assumptions.
"""

MAX_ENUMERATED_ARGS = 6


def all_(pred, args):
    return And(*[pred(a) for a in args])


def any_(pred, args):
    return Or(*[pred(a) for a in args])


def each_with_rest(args, pred, rest_pred, conclusion):
    """
    ``pred(a) & rest_pred(b) for every other b`` implies *conclusion*, for
    every *a* in *args*.
    """
    return [Implies(And(pred(a), *[rest_pred(b) for j, b in enumerate(args) if j != i]),
                    conclusion) for i, a in enumerate(args)]


def closed_group(expr, pred, args=None):
    """
    Facts of ``test_closed_group``: all args satisfying *pred* implies *expr*
    does, and exactly one arg not satisfying it implies *expr* does not.
    """
    args = expr.args if args is None else args
    return [Implies(all_(pred, args), pred(expr)),
            *each_with_rest(args, lambda a: ~pred(a), pred, ~pred(expr))]


def parity(args, even, odd, on_even, on_odd, extra=True):
    """
    Facts for an operation whose result depends on the parity of the number
    of args satisfying *odd*, when every arg satisfies *even* or *odd*.
    """
    if len(args) > MAX_ENUMERATED_ARGS:
        return []
    facts = []
    for bits in product((False, True), repeat=len(args)):
        cond = And(extra, *[odd(a) if b else even(a) for a, b in zip(args, bits)])
        res = on_odd if sum(bits) % 2 else on_even
        if res is not None:
            facts.append(Implies(cond, res))
    return facts


def is_scalar(expr):
    return isinstance(expr, Expr) and not isinstance(expr, MatrixExpr)


numeric_predicates = {Q.positive, Q.negative, Q.zero, Q.real, Q.imaginary,
                      Q.integer, Q.even, Q.odd, Q.prime}


def is_numeric(expr):
    """
    Whether the facts about ``numeric_predicates`` for *expr* are found by
    numerical evaluation in ``sympy.assumptions.satfacts.numbers``.
    """
    return (is_scalar(expr) and expr.is_number and not isinstance(expr, Number)
            and not expr.has(S.Infinity, S.NegativeInfinity, S.ComplexInfinity, S.NaN))


def register_scalar(*classes):
    """
    Register a handler returning a list of facts for the scalar instances of
    *classes*.
    """
    def _(func):
        def wrapper(expr):
            return func(expr) if is_scalar(expr) else []
        class_fact_registry.multiregister(*classes)(wrapper)
        return func
    return _


### Old assumptions ###

_old_assumptions = {
    Q.positive: 'is_positive',
    Q.negative: 'is_negative',
    Q.zero: 'is_zero',
    Q.extended_positive: 'is_extended_positive',
    Q.extended_negative: 'is_extended_negative',
    Q.real: 'is_real',
    Q.extended_real: 'is_extended_real',
    Q.rational: 'is_rational',
    Q.irrational: 'is_irrational',
    Q.integer: 'is_integer',
    Q.even: 'is_even',
    Q.odd: 'is_odd',
    Q.prime: 'is_prime',
    Q.composite: 'is_composite',
    Q.finite: 'is_finite',
    Q.infinite: 'is_infinite',
    Q.imaginary: 'is_imaginary',
    Q.complex: 'is_complex',
    Q.algebraic: 'is_algebraic',
    Q.transcendental: 'is_transcendental',
    Q.hermitian: 'is_hermitian',
    Q.antihermitian: 'is_antihermitian',
}

_old_assumptions_compound = {Q.positive, Q.negative, Q.zero, Q.real, Q.rational,
    Q.irrational, Q.integer, Q.even, Q.odd, Q.prime, Q.composite, Q.imaginary,
    Q.complex, Q.transcendental}
"""
Predicates for which the old assumptions of non-atomic expressions are used.
Facts for ``Add``, ``Mul`` and ``Pow`` come only from their structure.
"""


@class_fact_registry.multiregister(Expr)
def _(expr):
    if not is_scalar(expr) or isinstance(expr, (NaN, Add, Mul, Pow)):
        return []
    facts = []
    numeric = is_numeric(expr)
    for pred, attr in _old_assumptions.items():
        if numeric and pred in numeric_predicates:
            continue
        if not expr.is_Atom and pred not in _old_assumptions_compound:
            continue
        value = getattr(expr, attr)
        if value is not None:
            facts.append(pred(expr) if value else ~pred(expr))
    return facts


@class_fact_registry.multiregister(Expr)
def _(expr):
    if not is_scalar(expr) or isinstance(expr, NaN):
        return []
    return [Implies(Q.commutative(expr), Q.finite(expr) | Q.infinite(expr)),
            Implies(Q.commutative(expr), Equivalent(Q.hermitian(expr), Q.real(expr))),
            Implies(Q.commutative(expr),
                    Equivalent(Q.antihermitian(expr), Q.zero(expr) | Q.imaginary(expr)))]


### Q.commutative ###

@class_fact_registry.multiregister(Basic)
def _(expr):
    if isinstance(expr, Symbol):
        if expr.is_commutative is False:
            return [~Q.commutative(expr)]
        return []
    if not is_scalar(expr):
        return []
    args = [a for a in expr.args if isinstance(a, Expr)]
    return [Equivalent(Q.commutative(expr), all_(Q.commutative, args))]


@default_fact_registry.multiregister(Symbol)
def _(expr):
    if expr.is_commutative:
        return [Q.commutative(expr)]
    return []
