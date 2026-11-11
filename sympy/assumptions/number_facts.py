"""What a number is, from its class and its value, without the old assumptions."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.ask import Q
from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.core.numbers import (Catalan, ComplexInfinity, EulerGamma, Exp1, Float,
    GoldenRatio, Half, ImaginaryUnit, Infinity, Integer, NegativeInfinity, NegativeOne,
    One, Pi, Rational, TribonacciConstant, Zero, int_valued)
from sympy.core.power import Pow
from sympy.external.mpmath import (fone, from_int, fzero, mpci_abs, mpci_add,
    mpci_cos, mpci_div, mpci_exp, mpci_log, mpci_mul, mpci_pow, mpci_sin, mpf_e,
    mpf_pi, mpf_sign, mpi_div, mpi_neg, round_ceiling, round_floor)
from sympy.functions.elementary.complexes import Abs, conjugate, im, re
from sympy.functions.elementary.exponential import exp, log
from sympy.functions.elementary.trigonometric import cos, cot, sin, tan
from sympy.ntheory.primetest import isprime

if TYPE_CHECKING:
    from collections.abc import Callable

    from sympy.assumptions.assume import Predicate
    from sympy.core.basic import Basic

    Facts = list[tuple[Predicate, bool]]
    # ((lower, upper) of the real part, (lower, upper) of the imaginary part)
    Interval = tuple[tuple[tuple, tuple], tuple[tuple, tuple]]

_ZERO: Facts = [(Q.zero, True), (Q.antihermitian, True)]
_NOT_ANTIHERMITIAN = (Q.antihermitian, False)
_NEITHER_HERMITIAN = [(Q.hermitian, False), (Q.antihermitian, False)]
_CONSTANTS: dict[type, Facts] = {
    Pi: [(Q.positive, True), (Q.irrational, True), (Q.transcendental, True),
         _NOT_ANTIHERMITIAN],
    Exp1: [(Q.positive, True), (Q.irrational, True), (Q.transcendental, True),
           _NOT_ANTIHERMITIAN],
    GoldenRatio: [(Q.positive, True), (Q.irrational, True), (Q.algebraic, True),
                  _NOT_ANTIHERMITIAN],
    TribonacciConstant: [(Q.positive, True), (Q.irrational, True),
                         (Q.algebraic, True), _NOT_ANTIHERMITIAN],
    EulerGamma: [(Q.positive, True), _NOT_ANTIHERMITIAN],
    Catalan: [(Q.positive, True), _NOT_ANTIHERMITIAN],
    ImaginaryUnit: [(Q.imaginary, True), (Q.algebraic, True), (Q.hermitian, False)],
    Infinity: [(Q.positive_infinite, True)] + _NEITHER_HERMITIAN,
    NegativeInfinity: [(Q.negative_infinite, True)] + _NEITHER_HERMITIAN,
    ComplexInfinity: [(Q.infinite, True), (Q.extended_real, False)]
                     + _NEITHER_HERMITIAN,
}


def number_facts(expr: Basic) -> Facts | None:
    """
    A few predicates of the number *expr*, true or false, which decide the
    others through the known facts between predicates. ``None`` if *expr* is
    not a number which this knows.
    """
    facts = _CONSTANTS.get(type(expr))
    if facts is not None:
        return facts
    if isinstance(expr, Integer):
        return _integer_facts(expr.p)
    if isinstance(expr, Rational):
        return [(Q.positive if expr.p > 0 else Q.negative, True),
                (Q.rational, True), (Q.integer, False), _NOT_ANTIHERMITIAN]
    if isinstance(expr, Float):
        sign = mpf_sign(expr._mpf_)
        if sign == 0:
            return _ZERO
        facts = [(Q.positive if sign > 0 else Q.negative, True), _NOT_ANTIHERMITIAN]
        if not int_valued(expr):
            facts.append((Q.integer, False))
        return facts
    if expr.is_Atom:
        return None
    z = _interval(expr)
    return None if z is None else _interval_facts(z)


def _integer_facts(n: int) -> Facts:
    if n == 0:
        return _ZERO
    facts = [(Q.positive if n > 0 else Q.negative, True),
             (Q.even if n % 2 == 0 else Q.odd, True), _NOT_ANTIHERMITIAN]
    if n > 1:
        facts.append((Q.prime if isprime(n) else Q.composite, True))
    else:
        facts += [(Q.prime, False), (Q.composite, False)]
    return facts


_PREC = 53
# no interval has an endpoint of 2**_MAX_MAG or more in absolute value, which
# keeps exp, sin and cos of them fast
_MAX_MAG = 1024
_ZERO_PART = (fzero, fzero)
_ATOM_INTERVALS: dict[type, Interval] = {
    Pi: ((mpf_pi(_PREC, round_floor), mpf_pi(_PREC, round_ceiling)), _ZERO_PART),
    Exp1: ((mpf_e(_PREC, round_floor), mpf_e(_PREC, round_ceiling)), _ZERO_PART),
    ImaginaryUnit: (_ZERO_PART, (fone, fone)),
}


def _sin(z: Interval) -> Interval:
    return mpci_sin(z, _PREC)


def _cos(z: Interval) -> Interval:
    return mpci_cos(z, _PREC)


def _log(z: Interval) -> Interval | None:
    """``log`` of *z* if it lies in ``re > 0``, ``im > 0``, ``im < 0`` or on the negative real axis."""
    (re_a, re_b), (im_a, im_b) = z
    # for a negative real part and an imaginary part from -a to 0, mpmath's
    # interval of the argument is reversed
    if (mpf_sign(re_a) > 0 or mpf_sign(im_a) > 0 or mpf_sign(im_b) < 0
            or im_a == im_b == fzero and mpf_sign(re_b) < 0):
        return mpci_log(z, _PREC)
    return None


_FUNCTIONS: dict[type, Callable[[Interval], Interval | None]] = {
    exp: lambda z: mpci_exp(z, _PREC),
    log: _log,
    sin: _sin,
    cos: _cos,
    tan: lambda z: mpci_div(_sin(z), _cos(z), _PREC),
    cot: lambda z: mpci_div(_cos(z), _sin(z), _PREC),
    Abs: lambda z: (mpci_abs(z, _PREC), _ZERO_PART),
    re: lambda z: (z[0], _ZERO_PART),
    im: lambda z: (z[1], _ZERO_PART),
    conjugate: lambda z: (z[0], mpi_neg(z[1])),
}
# the classes of the numbers which number_facts evaluates if it evaluates their arguments
EVALUATED = frozenset({Integer, Zero, One, NegativeOne, Rational, Half, Float, Pi,
                       Exp1, ImaginaryUnit, Add, Mul, Pow, *_FUNCTIONS})


def _interval(expr: Basic) -> Interval | None:
    """An interval of complex numbers which contains *expr*, or ``None``."""
    cls = type(expr)
    z: Interval | None = None
    if isinstance(expr, Integer):
        z = (_integer_part(expr.p), _ZERO_PART)
    elif isinstance(expr, Rational):
        z = (mpi_div(_integer_part(expr.p), _integer_part(expr.q), _PREC), _ZERO_PART)
    elif isinstance(expr, Float):
        z = ((expr._mpf_, expr._mpf_), _ZERO_PART)
    elif cls in _ATOM_INTERVALS:
        z = _ATOM_INTERVALS[cls]
    elif cls is Add or cls is Mul:
        operation = mpci_add if cls is Add else mpci_mul
        for arg in expr.args:
            w = _interval(arg)
            if w is None:
                return None
            z = w if z is None else operation(z, w, _PREC)
    elif cls is Pow:
        base, exponent = expr.args
        z = _interval(base)
        if z is None:
            return None
        if isinstance(exponent, Integer) and abs(exponent.p) <= _MAX_MAG:
            n = from_int(exponent.p)
            z = mpci_pow(z, ((n, n), _ZERO_PART), _PREC)
        else:
            w, log_z = _interval(exponent), _log(z)
            if w is None or log_z is None:
                return None
            z = mpci_mul(w, log_z, _PREC)
            if not _bounded(z):
                return None
            z = mpci_exp(z, _PREC)
    elif cls in _FUNCTIONS:
        z = _interval(expr.args[0])
        if z is None:
            return None
        z = _FUNCTIONS[cls](z)
    return z if z is not None and _bounded(z) else None


def _integer_part(n: int) -> tuple[tuple, tuple]:
    return (from_int(n, _PREC, round_floor), from_int(n, _PREC, round_ceiling))


def _bounded(z: Interval) -> bool:
    """Whether the endpoints of *z* are finite and below ``2**_MAX_MAG`` in absolute value."""
    for part in z:
        for _, man, exponent, bc in part:
            if man == 0:
                if exponent != 0:
                    return False
            elif exponent + bc > _MAX_MAG:
                return False
    return True


_POSITIVE: Facts = [(Q.positive, True), _NOT_ANTIHERMITIAN]
_NEGATIVE: Facts = [(Q.negative, True), _NOT_ANTIHERMITIAN]
_IMAGINARY: Facts = [(Q.imaginary, True), (Q.hermitian, False)]
_NOT_REAL: Facts = [(Q.extended_real, False), (Q.hermitian, False)]
_NOT_IMAGINARY: Facts = [(Q.imaginary, False), (Q.zero, False), _NOT_ANTIHERMITIAN]
_NEITHER_REAL_NOR_IMAGINARY: Facts = [(Q.extended_real, False), (Q.imaginary, False)
                                      ] + _NEITHER_HERMITIAN


def _interval_facts(z: Interval) -> Facts | None:
    """What the interval *z* proves about every number in it."""
    (re_a, re_b), (im_a, im_b) = z
    re_nonzero = mpf_sign(re_a) > 0 or mpf_sign(re_b) < 0
    if im_a == im_b == fzero:
        if mpf_sign(re_a) > 0:
            return _POSITIVE
        if mpf_sign(re_b) < 0:
            return _NEGATIVE
        return None
    if mpf_sign(im_a) > 0 or mpf_sign(im_b) < 0:
        if re_a == re_b == fzero:
            return _IMAGINARY
        if re_nonzero:
            return _NEITHER_REAL_NOR_IMAGINARY
        return _NOT_REAL
    if re_nonzero:
        return _NOT_IMAGINARY
    return None
