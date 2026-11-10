"""
Facts for numeric expressions which are found by numerical evaluation.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.assumptions.sathandlers import class_fact_registry
from sympy.core import Expr, Float, S
from sympy.core.numbers import Number, int_valued
from sympy.ntheory import isprime

from .common import is_numeric


def _evaluated(x):
    x = x.evalf(2)
    if isinstance(x, Number) and x._prec != 1:
        return x


def _sign(expr):
    """Return the sign of a real number, ``None`` if it is not known."""
    r, i = expr.as_real_imag()
    if r is S.NaN or i is S.NaN:
        return None
    if i:
        i = _evaluated(i)
        if i is None:
            return None
        if i != 0:
            return 'nonreal'
    r = _evaluated(r)
    if r is None:
        return None
    return 'positive' if r > 0 else 'negative' if r < 0 else 'zero'


def _rounded(expr):
    """
    Return the integer *expr* is equal to, ``False`` if it is not an integer
    and ``None`` if that is not known.
    """
    try:
        i = int(expr.round())
    except TypeError:
        return False
    is_equal = (expr - i).equals(0)
    if is_equal is None:
        return None
    return i if is_equal else False


@class_fact_registry.multiregister(Expr)
def _(expr):
    if not is_numeric(expr):
        return []
    facts = []
    sign = _sign(expr)
    if sign == 'nonreal':
        facts.append(~Q.real(expr))
    elif sign is not None:
        facts.append(getattr(Q, sign)(expr))
    real, imag = (_evaluated(p) for p in expr.as_real_imag())
    if imag is not None:
        facts.append(Q.real(expr) if not imag else ~Q.real(expr))
    if real is not None:
        facts.append(~Q.imaginary(expr) if real else Q.imaginary(expr) | Q.zero(expr))
    i = _rounded(expr)
    if i is False:
        facts.append(~Q.integer(expr))
    elif i is not None and not expr.atoms(Float):
        facts.extend([Q.integer(expr), Q.even(expr) if i % 2 == 0 else Q.odd(expr),
                      Q.prime(expr) if isprime(i) else ~Q.prime(expr)])
    return facts


@class_fact_registry.multiregister(Float)
def _(expr):
    if int_valued(expr):
        return []
    return [~Q.integer(expr)]
