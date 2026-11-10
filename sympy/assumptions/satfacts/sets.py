"""
Facts for set membership predicates: integer, rational, real, etc.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.assumptions.sathandlers import class_fact_registry
from sympy.core import Add, Mul, Pow, S
from sympy.core.numbers import E, I, Rational, pi
from sympy.core.relational import Eq
from sympy.core.logic import fuzzy_and, fuzzy_bool
from sympy.functions import (Abs, acos, acot, asin, atan, cos, cot, exp, im,
    log, re, sin, tan)
from sympy.functions.elementary.complexes import conjugate
from sympy.logic.boolalg import And, Equivalent, Implies
from sympy.matrices import MatrixBase
from sympy.matrices.expressions import Determinant, Trace
from sympy.matrices.expressions.matexpr import MatrixElement

from .common import register_scalar, all_, closed_group, each_with_rest, parity


def _at_most_one_noncommutative(args):
    yield And(*[Q.commutative(a) for a in args])
    for i in range(len(args)):
        yield And(*[Q.commutative(a) for j, a in enumerate(args) if j != i])


### Add ###

@register_scalar(Add)
def _(expr):
    args = expr.args
    return [
        *closed_group(expr, Q.real),
        *closed_group(expr, Q.rational),
        *closed_group(expr, Q.complex),
        *closed_group(expr, Q.algebraic),
        *closed_group(expr, Q.hermitian),
        *closed_group(expr, Q.antihermitian),
        *each_with_rest(args, lambda a: Q.real(a) & Q.nonzero(a), Q.imaginary,
                        ~Q.imaginary(expr)),
    ]


### Mul ###

@register_scalar(Mul)
def _(expr):
    args = expr.args
    nonzero = all_(lambda a: ~Q.zero(a), args)
    facts = [
        Implies(all_(Q.rational, args), Q.rational(expr)),
        *each_with_rest(args, lambda a: ~Q.rational(a), lambda a: Q.rational(a) & ~Q.zero(a),
                        ~Q.rational(expr)),
        Implies(all_(Q.complex, args), Q.complex(expr)),
        Implies(all_(Q.algebraic, args), Q.algebraic(expr)),
        *each_with_rest(args, lambda a: ~Q.algebraic(a), lambda a: Q.algebraic(a) & ~Q.zero(a),
                        ~Q.algebraic(expr)),
        *each_with_rest(args, Q.irrational, lambda a: Q.integer(a) & ~Q.zero(a),
                        ~Q.integer(expr)),
        *parity(args, Q.real, Q.imaginary, Q.real(expr),
                Equivalent(Q.real(expr), Q.zero(expr))),
        *parity(args, Q.real, Q.imaginary, None, Q.imaginary(expr), extra=nonzero),
    ]
    for cond in _at_most_one_noncommutative(args):
        facts.extend(parity(args, Q.hermitian, Q.antihermitian,
                            Q.hermitian(expr), Q.antihermitian(expr), extra=cond))
    for a in args:
        if isinstance(a, Rational) and a.q == 2:
            facts.append(Equivalent(Q.integer(expr), Q.even(2*expr)))
            break
    return facts


### Pow ###

def _exp_facts(expr, x):
    facts = [
        Implies(Q.real(x), Q.real(expr)),
        Implies(Q.hermitian(x), Q.hermitian(expr)),
        Implies(Q.finite(x), Q.complex(expr)),
        Implies(Q.rational(x), Equivalent(Q.rational(expr), Q.zero(x))),
        Implies(Q.algebraic(x), Equivalent(Q.algebraic(expr), Q.zero(x))),
    ]
    if x.has(I):
        a = x/I/pi
        facts.extend([
            Implies(Q.integer(a), Q.real(expr)),
            Implies(Q.integer(2*a) & ~Q.integer(a), Q.imaginary(expr)),
        ])
    return facts


@class_fact_registry.multiregister(exp)
def _(expr):
    return _exp_facts(expr, expr.exp)


@register_scalar(Pow)
def _(expr):
    base, e = expr.base, expr.exp
    if base == E:
        return _exp_facts(expr, e)
    facts = [
        # integer
        Implies(~Q.zero(base) & Q.finite(base) & Q.zero(e), Q.integer(expr)),
        Implies(Q.integer(base) & Q.integer(e) & ~Q.negative(e), Q.integer(expr)),
        # rational
        Implies(Q.integer(e) & Q.rational(base) & ~Q.zero(base), Q.rational(expr)),
        Implies(Q.integer(e) & Q.rational(base) & Q.zero(base) & Q.positive(e), Q.rational(expr)),
        Implies(Q.integer(e) & Q.transcendental(base), Equivalent(Q.rational(expr), Q.zero(e))),
        Implies(Q.rational(e) & ~Q.integer(e) & Q.prime(base), ~Q.rational(expr)),
        # real
        Implies(Q.imaginary(base) & Q.integer(e), Equivalent(Q.real(expr), Q.even(e))),
        Implies(Q.real(base) & Q.integer(e) & ~Q.zero(base), Q.real(expr)),
        Implies(Q.real(base) & Q.integer(e) & ~Q.negative(e), Q.real(expr)),
        Implies(Q.zero(base) & Q.real(e), Equivalent(Q.real(expr), ~Q.negative(e))),
        Implies(Q.positive(base) & Q.real(e), Q.real(expr)),
        # imaginary
        Implies(Q.imaginary(base) & Q.integer(e), Equivalent(Q.imaginary(expr), Q.odd(e))),
        Implies(Q.real(base) & Q.real(e) & Q.irrational(e), ~Q.imaginary(expr)),
        Implies(Q.real(base) & Q.integer(e), ~Q.imaginary(expr)),
        # complex
        Implies(Q.complex(base) & Q.complex(e) & ~Q.zero(base), Q.complex(expr)),
        # hermitian
        Implies(Q.hermitian(base) & ~Q.zero(base) & Q.integer(e), Q.hermitian(expr)),
        Implies(Q.hermitian(base) & Q.integer(e) & ~Q.negative(e), Q.hermitian(expr)),
        Implies(Q.hermitian(base) & ~Q.zero(base) & Q.integer(e), ~Q.antihermitian(expr)),
        Implies(Q.antihermitian(base) & ~Q.zero(base) & Q.even(e), ~Q.antihermitian(expr)),
        Implies(Q.antihermitian(base) & ~Q.zero(base) & Q.odd(e), Q.antihermitian(expr)),
        Implies(Q.antihermitian(base) & Q.odd(e) & Q.positive(e), Q.antihermitian(expr)),
        # algebraic
        Implies(Q.algebraic(base) & Q.rational(e) & ~Q.zero(base), Q.algebraic(expr)),
        Implies(Q.integer(e) & Q.positive(e) & ~Q.algebraic(base), ~Q.algebraic(expr)),
    ]
    if not e.is_number:
        facts.extend([
            Implies(Q.real(base) & Q.real(e) & Q.integer(2*e) & ~Q.integer(e),
                    Equivalent(Q.imaginary(expr), Q.negative(base))),
            Implies(Q.real(base) & Q.real(e) & Q.rational(e) & ~Q.integer(2*e),
                    ~Q.imaginary(expr)),
        ])
    elif e.is_Rational and not e.is_Integer:
        facts.append(Implies(Q.real(base),
            Equivalent(Q.imaginary(expr), Q.negative(base)) if e.q == 2 else ~Q.imaginary(expr)))
        if e.q % 2 == 0:
            facts.append(Implies(Q.real(base), Equivalent(Q.real(expr), Q.nonnegative(base))))
    if e == -1:
        facts.append(Implies(Q.irrational(base), ~Q.rational(expr)))
    if not base.is_number:
        facts.extend([
            Implies(Q.integer(base) & Q.integer(e) & Q.negative(e) & ~Q.zero(base - 1)
                    & ~Q.zero(base + 1), ~Q.integer(expr)),
            Implies(Q.rational(e) & Q.eq(base, 1), Q.rational(expr)),
        ])
    if isinstance(base, exp) or (base.is_Pow and base.base == E):
        facts.append(Implies(Q.imaginary(base.exp) & Q.imaginary(e), Q.real(expr)))
    if base == pi:
        facts.append(Implies(Q.integer(e) & Q.positive(e), ~Q.algebraic(expr)))
    if not base.is_number:
        facts.append(Implies(Q.algebraic(base) & Q.algebraic(e) & ~Q.rational(e)
                             & ~Q.zero(base) & ~Q.zero(base - 1), ~Q.algebraic(expr)))
    elif base.is_algebraic and base not in (S.Zero, S.One):
        facts.append(Implies(Q.algebraic(e) & ~Q.rational(e), ~Q.algebraic(expr)))
    if not e.is_number:
        facts.append(Implies(Q.imaginary(e) & Q.imaginary(log(base)), Q.real(expr)))
    return facts


### Functions ###

@class_fact_registry.multiregister(Abs, re, im)
def _(expr):
    return [Q.real(expr), Q.complex(expr)]


@class_fact_registry.multiregister(Abs)
def _(expr):
    return [Implies(Q.integer(expr.args[0]), Q.integer(expr))]


@class_fact_registry.multiregister(cos, sin)
def _(expr):
    x = expr.args[0]
    return [Q.complex(expr),
            Implies(Q.real(x), Q.real(expr)),
            Implies(Q.hermitian(x), Q.hermitian(expr))]


@class_fact_registry.multiregister(asin, atan, cos, sin, tan)
def _(expr):
    x = expr.args[0]
    return [Implies(Q.rational(x), Equivalent(Q.rational(expr), Q.zero(x))),
            Implies(Q.algebraic(x), Equivalent(Q.algebraic(expr), Q.zero(x)))]


@class_fact_registry.multiregister(acot, cot)
def _(expr):
    x = expr.args[0]
    return [Implies(Q.rational(x), ~Q.rational(expr)),
            Implies(Q.algebraic(x), ~Q.algebraic(expr))]


@class_fact_registry.multiregister(acos, log)
def _(expr):
    x = expr.args[0]
    is_one = Q.zero(x - 1)
    if x.is_number:
        is_one = (x - 1).is_zero
        if is_one is None:
            return []
    return [Implies(Q.rational(x), Equivalent(Q.rational(expr), is_one)),
            Implies(Q.algebraic(x), Equivalent(Q.algebraic(expr), is_one))]


@class_fact_registry.multiregister(log)
def _(expr):
    x = expr.args[0]
    return [Equivalent(Q.real(expr), Q.positive(x)),
            Implies(Q.complex(x) & ~Q.zero(x), Q.complex(expr))]


@class_fact_registry.multiregister(Determinant, MatrixElement, Trace)
def _(expr):
    m = expr.args[0]
    return [Implies(Q.integer_elements(m), Q.integer(expr)),
            Implies(Q.real_elements(m), Q.real(expr)),
            Implies(Q.complex_elements(m), Q.complex(expr))]


### Explicit matrices ###

def _check_entries(mat, rel):
    rows, cols = mat.shape
    conds = [fuzzy_bool(Eq(mat[i, j], rel(mat[j, i])))
             for i in range(rows) for j in range(i, cols)]
    if False in conds:
        return False
    return fuzzy_and(conds)


@class_fact_registry.multiregister(MatrixBase)
def _(mat):
    if not mat.is_square:
        return []
    facts = []
    for pred, rel in [(Q.hermitian, conjugate), (Q.antihermitian, lambda x: -conjugate(x))]:
        value = _check_entries(mat, rel)
        if value is not None:
            facts.append(pred(mat) if value else ~pred(mat))
    return facts
