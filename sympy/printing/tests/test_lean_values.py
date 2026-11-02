"""Compare the values of the Lean terms that lean_code prints with SymPy's.

This needs SYMPY_LEAN_PROJECT, a Lake project that depends on Mathlib (see
check_printed_code.py), and is skipped without it.
"""
from __future__ import annotations

import random

from sympy.concrete import Product, Sum
from sympy.core import (E, Expr, Float, Integer, Rational, Subs, Symbol, pi,
                        symbols)
from sympy.core.function import Derivative
from sympy.functions import (Abs, Heaviside, Max, Min, Piecewise, acos, acosh,
                             asin, asinh, atan, atan2, atanh, ceiling, cos,
                             cosh, cot, exp, floor, gamma, log, sec, sign, sin,
                             sinh, sqrt, tan, tanh)
from sympy.integrals import Integral
from sympy.printing.codeprinter import PrintMethodNotImplementedError
from sympy.printing.lean import LeanPrinter
from sympy.printing.tests.check_printed_code import (compiling_enabled,
                                                     lean_values)
from sympy.testing.pytest import skip

x, y = symbols('x y', real=True)
n = Symbol('n', integer=True)
i = Symbol('i', integer=True)
ARGS = [x, y, n]

# One or more expressions for each thing LeanPrinter prints for real numbers
EXPRESSIONS = [
    x + 2*y - 3, x*y/(x + 1), -x**2, (x + y)**3, 1/x, x**-2, x/(y*(x + 2)),
    Rational(3, 7)*x - Rational(1, 2), 2**x, Rational(1, 2)**y, (-2)**n,
    x**Rational(1, 3), x**Rational(-2, 3), x**y, x**(y + 1), x**n,
    x**(n + 1), x**(2*n), x**floor(y), sqrt(x), sqrt(x**2 + 1), y/sqrt(x),
    n + x, sin(n*x), Float('0.25')*x,
    pi*x, E*x,
    sin(x) + cos(y) + tan(x) + cot(y), asin(x/4) + acos(y/4) + atan(x),
    asin(x) + acos(y), sinh(x) + cosh(y) + tanh(x), asinh(x) + acosh(y),
    atanh(x/4), atanh(x), exp(x) + log(y), log(x), gamma(x), sign(x) + sign(y),
    sin(cos(x)), exp(-x), sec(x)*y, y/sec(x), Heaviside(x), x*Heaviside(y),
    Abs(x) + Abs(x + y), log(Abs(x)), floor(x) + ceiling(x + y),
    Max(x, y), Max(x, y, 1), Min(x + 1, y), atan2(y, x),
    Piecewise((x, x < 0), (0, True)),
    Piecewise((x, x < 0), (x**2, y < 1), (1, True)) + 1,
    Piecewise((1, (x < 0) & (y > 0)), (2, (x > 1) | (y < -1)), (3, True)),
    Derivative(sin(x*y), x), Derivative(sin(x*y), x, y),
    Derivative(x**3*exp(x), (x, 2)), Subs(x**2 + y, x, y + 1),
    Integral(x**2 + y, (x, 0, 1)), Integral(sin(x*y), (x, 0, y)),
    Integral(x*y, (x, 0, 1), (y, -1, 2)),
    Sum(i**2, (i, 1, n)), Sum(x**i, (i, 0, n)), Product(i + x, (i, 1, 3)),
    Sum(i*y, (i, -2, n + 1)),
]

# Expressions whose value is approximated numerically in Lean
APPROXIMATED = (Derivative, Integral)


def random_expressions(rng, count):
    """Random expressions of x, y and n with the functions LeanPrinter
    supports for real numbers."""
    leaves = [x, y, n, Integer(2), Integer(-3), Rational(1, 2),
              Rational(-5, 3), pi, E]
    functions = [sin, cos, tan, cot, sec, exp, log, sqrt, Abs, atan, asin,
                 acos, sinh, cosh, tanh, asinh, acosh, atanh, floor, ceiling,
                 sign, gamma]
    exponents = [2, 3, -1, -2, Rational(1, 2), Rational(1, 3),
                 Rational(-2, 3), n, y]

    def build(depth):
        if depth == 0 or rng.random() < 0.25:
            return rng.choice(leaves)
        k = rng.random()
        if k < 0.35:
            return rng.choice(functions)(build(depth - 1))
        if k < 0.55:
            return build(depth - 1) + build(depth - 1)
        if k < 0.7:
            return build(depth - 1)*build(depth - 1)
        if k < 0.78:
            return build(depth - 1)/build(depth - 1)
        if k < 0.9:
            return build(depth - 1)**rng.choice(exponents)
        if k < 0.95:
            return rng.choice([Max, Min])(build(depth - 1), build(depth - 1))
        return Piecewise((build(depth - 1), x < build(depth - 1)),
                         (build(depth - 1), True))

    expressions = []
    while len(expressions) < count:
        try:
            expr = build(3)
        except (ValueError, TypeError):  # e.g. Max of a complex number
            continue
        if expr.free_symbols and expr.is_finite is not False:
            try:
                LeanPrinter().doprint(expr)
            except PrintMethodNotImplementedError:
                continue
            expressions.append(expr)
    return expressions


def random_points(rng, count):
    return [[round(rng.uniform(-3, 3), 3), round(rng.uniform(-3, 3), 3),
             rng.randint(-3, 3)] for _ in range(count)]


def parts(expr):
    """expr and its parts, except those of sums, integrals and other
    expressions with bound variables."""
    yield expr
    if not isinstance(expr, (Sum, Product, Integral, Derivative, Subs)):
        for arg in expr.args:
            if isinstance(arg, Expr):
                yield from parts(arg)


def sympy_value(expr, point):
    """The value of expr at point, as a float, or None if Lean's can differ:
    where a part of expr isn't real (Lean's real functions take real values,
    e.g. Real.sqrt x = 0 for x < 0), where a sum's upper limit is below its
    lower limit minus 1 (Lean's is empty, SymPy follows Karr's convention), or
    where it can't be compared with a float (too large, or near a jump)."""
    subs = {a: (Integer(int(v)) if a.is_integer else Float(v, 30))
            for a, v in zip(ARGS, point)}

    def value(e):
        try:
            v = e.subs(subs).doit().evalf(30)
        except (ValueError, TypeError):  # e.g. Max of a complex number
            return None
        if not (v.is_Number and v.is_extended_real and v.is_finite):
            return None
        return float(v)
    for part in parts(expr):
        if not part.free_symbols - set(ARGS) and value(part) is None:
            return None
        if isinstance(part, (Sum, Product)):
            for _, lower, upper in part.limits:
                if (upper - lower + 1).subs(subs).is_negative:
                    return None
    v = value(expr)
    if v is None or abs(v) > 1e12:
        return None
    # A value that changes when x and y change in their 9th digit can't be
    # compared, e.g. near a jump of floor or Piecewise
    subs = {a: (Float(p*(1 + 1e-9) + 1e-12, 30) if not a.is_integer else s)
            for (a, s), p in zip(subs.items(), point)}
    nudged = value(expr)
    if nudged is None or abs(nudged - v) > 1e-6*(1 + abs(v)):
        return None
    return v


def compare(expressions, points_per_expression, rng):
    printer = LeanPrinter()
    functions = [(ARGS, e, random_points(rng, points_per_expression))
                 for e in expressions]
    values = lean_values(printer, functions)
    problems, compared = [], 0
    for (_, expr, points), lean in zip(functions, values):
        tolerance = 1e-6 if expr.has(*APPROXIMATED) else 1e-9
        for point, lean_value in zip(points, lean):
            expected = sympy_value(expr, point)
            if expected is None:
                continue
            if isinstance(lean_value, str):
                problems.append('%s at %s: %s' % (printer.doprint(expr), point,
                                                  lean_value))
                continue
            compared += 1
            if not (abs(lean_value - expected) <= tolerance*(1 + abs(expected))):
                problems.append('%s at x, y, n = %s: Lean %r, SymPy %r' % (
                    printer.doprint(expr), point, lean_value, expected))
    return problems, compared


def test_lean_values():
    if not compiling_enabled(LeanPrinter):
        skip("SYMPY_LEAN_PROJECT isn't a Lake project with Mathlib")
    rng = random.Random(1)
    expressions = EXPRESSIONS + random_expressions(rng, 300)
    problems, compared = compare(expressions, 4, rng)
    assert not problems, '\n'.join(problems)
    # Most points can be compared
    assert compared > 600, compared
