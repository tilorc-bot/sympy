"""What a number is, from its class and its value, without the old assumptions."""
from __future__ import annotations

from fractions import Fraction
from math import prod
from typing import TYPE_CHECKING

from sympy.assumptions.ask import Q
from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.core.numbers import (Catalan, ComplexInfinity, EulerGamma, Exp1, Float,
    GoldenRatio, Half, ImaginaryUnit, Infinity, Integer, NegativeInfinity, NegativeOne,
    One, Pi, Rational, TribonacciConstant, Zero, int_valued)
from sympy.core.power import Pow
from sympy.external.gmpy import iroot
from sympy.external.mpmath import (fnone, fone, from_int, fzero, mpci_abs,
    mpci_add, mpci_cos, mpci_div, mpci_exp, mpci_log, mpci_mul, mpci_pow, mpci_sin,
    mpf_acos, mpf_acosh, mpf_asin, mpf_asinh, mpf_atan, mpf_atanh, mpf_e, mpf_ge,
    mpf_gt, mpf_le, mpf_lt, mpf_perturb, mpf_pi, mpf_pos, mpf_shift, mpf_sign,
    mpi_div, mpi_neg, round_ceiling, round_floor)
from sympy.functions.elementary.complexes import Abs, conjugate, im, re
from sympy.functions.elementary.exponential import exp, log
from sympy.functions.elementary.hyperbolic import (acosh, acoth, acsch, asech,
    asinh, atanh, cosh, coth, csch, sech, sinh, tanh)
from sympy.functions.elementary.trigonometric import (acos, acot, acsc, asec, asin,
    atan, cos, cot, csc, sec, sin, tan)
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
    if isinstance(expr, Rational):
        return _rational_facts(expr.p, expr.q)
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
    value = _exact(expr)
    if value is not None:
        return _rational_facts(value.numerator, value.denominator)
    if type(expr) is Pow:
        facts = _power_limit_facts(*expr.args)
        if facts is not None:
            return facts
    z = _interval(expr)
    facts = None if z is None else _interval_facts(z)
    if _is_algebraic(expr):
        return (facts or []) + [(Q.algebraic, True)]
    return facts


def _rational_facts(p: int, q: int) -> Facts:
    if q == 1:
        return _integer_facts(p)
    return [(Q.positive if p > 0 else Q.negative, True), (Q.rational, True),
            (Q.integer, False), _NOT_ANTIHERMITIAN]


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
# keeps exp, sin and cos of them fast, and no exact power has a numerator or a
# denominator of more than _MAX_MAG bits
_MAX_MAG = 1024
_ZERO_PART = (fzero, fzero)
_ONE = ((fone, fone), _ZERO_PART)
_ATOM_INTERVALS: dict[type, Interval] = {
    Pi: ((mpf_pi(_PREC, round_floor), mpf_pi(_PREC, round_ceiling)), _ZERO_PART),
    Exp1: ((mpf_e(_PREC, round_floor), mpf_e(_PREC, round_ceiling)), _ZERO_PART),
    ImaginaryUnit: (_ZERO_PART, (fone, fone)),
}
_EXACT_VALUES: dict[tuple[type, Fraction | int | None], int] = {
    (sin, 0): 0, (tan, 0): 0, (sinh, 0): 0, (tanh, 0): 0, (asin, 0): 0, (atan, 0): 0,
    (asinh, 0): 0, (atanh, 0): 0, (cos, 0): 1, (cosh, 0): 1, (exp, 0): 1, (log, 1): 0,
    (acos, 1): 0, (acosh, 1): 0}
# (function, whether its argument is r*I*pi rather than r*pi): its values at
# r = 0, 1/2, 1, 3/2, which repeat with period 2, None where they are not rational
_AT_HALF_TURNS: dict[tuple[type, bool], tuple[int | None, ...]] = {
    (sin, False): (0, 1, 0, -1), (cos, False): (1, 0, -1, 0),
    (tan, False): (0, None, 0, None), (exp, True): (1, None, -1, None),
    (cosh, True): (1, 0, -1, 0), (sinh, True): (0, None, 0, None)}


def _exact(expr: Basic) -> Fraction | int | None:
    """The value of *expr* if exact arithmetic on rational numbers finds it."""
    cls = type(expr)
    if isinstance(expr, Rational):
        return expr.p if expr.q == 1 else Fraction(expr.p, expr.q)
    if cls is Add or cls is Mul:
        values = []
        # the rational coefficient comes first, and is not converted if another argument fails
        for arg in reversed(expr.args):
            value = _exact(arg)
            if value is None:
                return None
            values.append(value)
        return sum(values) if cls is Add else prod(values)
    if cls is Pow:
        base, exponent = expr.args
        if not isinstance(exponent, Rational):
            return None
        value = _exact(base)
        return None if value is None else _exact_power(value, exponent.p, exponent.q)
    if cls in _FUNCTIONS:
        multiple = _pi_multiple(expr.args[0])
        if multiple is None:
            return _EXACT_VALUES.get((cls, _exact(expr.args[0])))
        r, imaginary = multiple
        turns = _AT_HALF_TURNS.get((cls, imaginary))
        if turns is not None and (2*r).denominator == 1:
            return turns[int(2*r) % 4]
    return None


def _exact_power(base: Fraction | int, p: int, q: int) -> Fraction | int | None:
    """``base**(p/q)`` if it is rational and not too large."""
    if q != 1:
        if base < 0 or q > _MAX_MAG:
            return None
        numerator, numerator_exact = iroot(base.numerator, q)
        denominator, denominator_exact = iroot(base.denominator, q)
        if not (numerator_exact and denominator_exact):
            return None
        base = Fraction(int(numerator), int(denominator))
    bits = max(base.numerator.bit_length(), base.denominator.bit_length())
    if base == 0 and p < 0 or abs(p) * bits > _MAX_MAG:
        return None
    return Fraction(base)**p if p < 0 else base**p


def _pi_multiple(expr: Basic) -> tuple[Fraction | int, bool] | None:
    """``(r, False)`` if *expr* is ``r*pi``, ``(r, True)`` if it is ``r*I*pi``, for a rational ``r``."""
    if type(expr) is Pi:
        return 1, False
    if type(expr) is not Mul:
        return None
    r: Fraction | int = 1
    pi_count = i_count = 0
    for arg in expr.args:
        if type(arg) is Pi:
            pi_count += 1
        elif type(arg) is ImaginaryUnit:
            i_count += 1
        elif isinstance(arg, Rational):
            r *= Fraction(arg.p, arg.q)
        else:
            return None
    return (r, i_count == 1) if pi_count == 1 and i_count <= 1 else None


# the functions which are algebraic at r*pi, or at r*I*pi, for a rational r
_ALGEBRAIC_AT_PI_MULTIPLES: dict[type, bool] = {
    sin: False, cos: False, exp: True, cosh: True, sinh: True}


def _is_algebraic(expr: Basic) -> bool:
    """Whether *expr* is a function of ``_ALGEBRAIC_AT_PI_MULTIPLES`` at such an argument."""
    imaginary = _ALGEBRAIC_AT_PI_MULTIPLES.get(type(expr))
    if imaginary is None:
        return False
    multiple = _pi_multiple(expr.args[0])
    return multiple is not None and multiple[1] is imaginary


_INFINITE: Facts = [(Q.infinite, True)]
# the sign of the real part of an exponent, and of log(abs(base)) of a base
_DIRECTION: dict[type, int] = {Infinity: 1, NegativeInfinity: -1}
_SIZE: dict[type, int] = {Infinity: 1, Zero: -1}


def _power_limit_facts(base: Basic, exponent: Basic) -> Facts | None:
    """
    Whether ``base**exponent`` is zero or infinite, when *base* is ``0`` or
    ``oo``, or *exponent* is ``oo`` or ``-oo`` and *base* is positive.
    """
    direction = _DIRECTION.get(type(exponent))
    size = _SIZE.get(type(base))
    if direction is None:
        if size is None:
            return None
        direction = _sign_of_real_part(exponent, size < 0)
    elif size is None:
        size = _compared_with_one(base)
    if not (size and direction):
        return None
    return _ZERO if size * direction < 0 else _INFINITE


def _sign_of_real_part(expr: Basic, real: bool) -> int:
    """The sign of the real part of *expr*, 0 if not known; with *real*, only for a real *expr*."""
    z = _interval(expr)
    if z is None or real and z[1] != _ZERO_PART:
        return 0
    return 1 if mpf_sign(z[0][0]) > 0 else -1 if mpf_sign(z[0][1]) < 0 else 0


def _compared_with_one(expr: Basic) -> int:
    """1 if *expr* is real and above 1, -1 if it is between 0 and 1, else 0."""
    z = _interval(expr)
    if z is None or z[1] != _ZERO_PART or mpf_sign(z[0][0]) <= 0:
        return 0
    return 1 if mpf_gt(z[0][0], fone) else -1 if mpf_lt(z[0][1], fone) else 0


def _sin(z: Interval) -> Interval:
    return mpci_sin(z, _PREC)


def _cos(z: Interval) -> Interval:
    return mpci_cos(z, _PREC)


def _div(z: Interval, w: Interval) -> Interval:
    return mpci_div(z, w, _PREC)


def _reciprocal(z: Interval) -> Interval:
    return mpci_div(_ONE, z, _PREC)


def _times_i(z: Interval) -> Interval:
    """``I*z``"""
    return mpi_neg(z[1]), z[0]


def _times_minus_i(z: Interval) -> Interval:
    """``-I*z``"""
    return z[1], mpi_neg(z[0])


def _cosh(z: Interval) -> Interval:
    return _cos(_times_i(z))


def _sinh(z: Interval) -> Interval:
    return _times_minus_i(_sin(_times_i(z)))


def _log(z: Interval) -> Interval | None:
    """``log`` of *z* if it lies in ``re > 0``, ``im > 0``, ``im < 0`` or on the negative real axis."""
    (re_a, re_b), (im_a, im_b) = z
    # for a negative real part and an imaginary part from -a to 0, mpmath's
    # interval of the argument is reversed
    if (mpf_sign(re_a) > 0 or mpf_sign(im_a) > 0 or mpf_sign(im_b) < 0
            or im_a == im_b == fzero and mpf_sign(re_b) < 0):
        return mpci_log(z, _PREC)
    return None


# the inverse functions below are evaluated for real arguments only; their
# endpoints are computed with _WP bits and rounded outward to _PREC bits with a
# margin, which covers the error of the mpmath functions
_WP = _PREC + 20
_PI = _ATOM_INTERVALS[Pi][0]
_HALF_PI = (mpf_shift(_PI[0], -1), mpf_shift(_PI[1], -1))


def _real(z: Interval) -> tuple[tuple, tuple] | None:
    """*z* rounded outward to ``_PREC`` bits if it is real."""
    if z[1] != _ZERO_PART:
        return None
    a, b = z[0]
    return mpf_pos(a, _PREC, round_floor), mpf_pos(b, _PREC, round_ceiling)


def _monotone(f: Callable, a: tuple, b: tuple) -> tuple[tuple, tuple]:
    """``f(a)`` rounded down and ``f(b)`` rounded up, for a function *f* of mpmath."""
    return (mpf_perturb(f(a, _WP, round_floor), 1, _PREC, round_floor),
            mpf_perturb(f(b, _WP, round_ceiling), 0, _PREC, round_ceiling))


def _side(x: tuple[tuple, tuple]) -> int | None:
    """1 if *x* lies above 1, -1 if below -1, 0 if within [-1, 1], else ``None``."""
    a, b = x
    if mpf_gt(a, fone):
        return 1
    if mpf_lt(b, fnone):
        return -1
    if mpf_ge(a, fnone) and mpf_le(b, fone):
        return 0
    return None


def _increasing(f: Callable) -> Callable[[Interval], Interval | None]:
    """The function of intervals for an increasing function *f* of mpmath which is real on the real line."""
    def g(z: Interval) -> Interval | None:
        x = _real(z)
        return None if x is None else (_monotone(f, *x), _ZERO_PART)
    return g


def _of_reciprocal(f: Callable[[Interval], Interval | None]) -> Callable[[Interval], Interval | None]:
    """The function ``f(1/x)`` of a real ``x`` which is not zero."""
    def g(z: Interval) -> Interval | None:
        x = _real(z)
        if x is None or mpf_sign(x[0]) <= 0 <= mpf_sign(x[1]):
            return None
        return f((mpi_div(_ONE[0], x, _WP), _ZERO_PART))
    return g


def _asin(z: Interval) -> Interval | None:
    x = _real(z)
    side = None if x is None else _side(x)
    if x is None or side is None:
        return None
    if side == 0:
        return _monotone(mpf_asin, *x), _ZERO_PART
    if side == 1:
        return _HALF_PI, mpi_neg(_monotone(mpf_acosh, *x))
    return mpi_neg(_HALF_PI), _monotone(mpf_acosh, *mpi_neg(x))


def _acos(z: Interval) -> Interval | None:
    x = _real(z)
    side = None if x is None else _side(x)
    if x is None or side is None:
        return None
    if side == 0:
        return _monotone(mpf_acos, x[1], x[0]), _ZERO_PART
    if side == 1:
        return _ZERO_PART, _monotone(mpf_acosh, *x)
    return _PI, mpi_neg(_monotone(mpf_acosh, *mpi_neg(x)))


def _acosh(z: Interval) -> Interval | None:
    x = _real(z)
    side = None if x is None else _side(x)
    if x is None or side is None:
        return None
    if side == 0:
        return _ZERO_PART, _monotone(mpf_acos, x[1], x[0])
    if side == 1:
        return _monotone(mpf_acosh, *x), _ZERO_PART
    return _monotone(mpf_acosh, *mpi_neg(x)), _PI


def _atanh(z: Interval) -> Interval | None:
    x = _real(z)
    side = None if x is None else _side(x)
    if x is None or side is None:
        return None
    if side == 0:
        if mpf_le(x[0], fnone) or mpf_ge(x[1], fone):
            return None
        return _monotone(mpf_atanh, *x), _ZERO_PART
    real_part = _monotone(mpf_atanh, *mpi_div(_ONE[0], x, _WP))
    return real_part, mpi_neg(_HALF_PI) if side == 1 else _HALF_PI


_FUNCTIONS: dict[type, Callable[[Interval], Interval | None]] = {
    exp: lambda z: mpci_exp(z, _PREC),
    log: _log,
    sin: _sin,
    cos: _cos,
    tan: lambda z: _div(_sin(z), _cos(z)),
    cot: lambda z: _div(_cos(z), _sin(z)),
    sec: lambda z: _reciprocal(_cos(z)),
    csc: lambda z: _reciprocal(_sin(z)),
    sinh: _sinh,
    cosh: _cosh,
    tanh: lambda z: _div(_sinh(z), _cosh(z)),
    coth: lambda z: _div(_cosh(z), _sinh(z)),
    sech: lambda z: _reciprocal(_cosh(z)),
    csch: lambda z: _reciprocal(_sinh(z)),
    asin: _asin,
    acos: _acos,
    atan: _increasing(mpf_atan),
    acot: _of_reciprocal(_increasing(mpf_atan)),
    asec: _of_reciprocal(_acos),
    acsc: _of_reciprocal(_asin),
    asinh: _increasing(mpf_asinh),
    acosh: _acosh,
    atanh: _atanh,
    acoth: _of_reciprocal(_atanh),
    asech: _of_reciprocal(_acosh),
    acsch: _of_reciprocal(_increasing(mpf_asinh)),
    Abs: lambda z: (mpci_abs(z, _PREC), _ZERO_PART),
    re: lambda z: (z[0], _ZERO_PART),
    im: lambda z: (z[1], _ZERO_PART),
    conjugate: lambda z: (z[0], mpi_neg(z[1])),
}
# the classes of the numbers which number_facts evaluates if it evaluates their arguments
EVALUATED = frozenset({Integer, Zero, One, NegativeOne, Rational, Half, Float, Pi,
                       Exp1, ImaginaryUnit, Infinity, NegativeInfinity, Add, Mul, Pow,
                       *_FUNCTIONS})


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
