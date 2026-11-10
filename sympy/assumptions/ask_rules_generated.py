"""
Do NOT manually edit this file.
Instead, run ./bin/ask_update.py.
"""

from sympy.assumptions.ask import Q
from sympy.core.add import Add
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.core.mul import Mul
from sympy.core.power import Pow
from sympy.core.symbol import Symbol
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.complexes import im
from sympy.functions.elementary.complexes import re
from sympy.functions.elementary.complexes import sign
from sympy.functions.elementary.exponential import exp
from sympy.functions.elementary.exponential import log
from sympy.functions.elementary.trigonometric import cos
from sympy.functions.elementary.trigonometric import sin
from sympy.matrices.expressions.matmul import MatMul

# A condition ``(predicate, slot, value)`` holds when asking the predicate
# about an expression gives ``value``. The expression is the argument number
# ``slot`` of the expression which a rule is about, or that expression itself
# for the slot ``EXPR``. A sum or a product is read as its first argument and
# the rest.
EXPR = -1

# For each class and number of arguments, the ways to find the truth value of
# each predicate for an instance: a truth value, and the conditions which
# together give it. The ways under ``None`` are for any number of arguments.
ASK_RULES = {
    (Abs, 1): {
        Q.even: (
            (True, ((Q.even, 0, True),)),
            (False, ((Q.even, 0, False), (Q.real, 0, True))),
        ),
        Q.extended_nonnegative: (
            (True, ()),
        ),
        Q.integer: (
            (True, ((Q.integer, 0, True),)),
        ),
        Q.nonnegative: (
            (True, ((Q.finite, 0, True),)),
        ),
        Q.odd: (
            (True, ((Q.odd, 0, True),)),
        ),
        Q.zero: (
            (True, ((Q.zero, 0, True),)),
            (False, ((Q.zero, 0, False),)),
        ),
    },
    (Add, 2): {
        Q.even: (
            (True, ((Q.even, 0, True), (Q.even, 1, True))),
            (True, ((Q.odd, 0, True), (Q.odd, 1, True))),
        ),
        Q.finite: (
            (True, ((Q.finite, 0, True), (Q.finite, 1, True))),
        ),
        Q.infinite: (
            (True, ((Q.finite, 0, False), (Q.finite, 1, True))),
            (True, ((Q.finite, 0, True), (Q.infinite, 1, True))),
        ),
        Q.integer: (
            (True, ((Q.integer, 0, True), (Q.integer, 1, True))),
            (False, ((Q.integer, 0, False), (Q.integer, 1, True))),
            (False, ((Q.integer, 0, True), (Q.integer, 1, False))),
        ),
        Q.irrational: (
            (True, ((Q.irrational, 0, True), (Q.rational, 1, True))),
            (True, ((Q.rational, 0, True), (Q.irrational, 1, True))),
        ),
        Q.negative: (
            (True, ((Q.negative, 0, True), (Q.negative, 1, True))),
        ),
        Q.negative_infinite: (
            (True, ((Q.extended_real, 0, True), (Q.positive_infinite, 0, False), (Q.negative_infinite, 1, True))),
            (True, ((Q.negative_infinite, 0, True), (Q.extended_real, 1, True), (Q.positive_infinite, 1, False))),
            (False, ((Q.extended_real, 0, True), (Q.negative_infinite, 0, False), (Q.extended_real, 1, True), (Q.negative_infinite, 1, False))),
        ),
        Q.odd: (
            (True, ((Q.even, 0, True), (Q.odd, 1, True))),
            (True, ((Q.odd, 0, True), (Q.even, 1, True))),
        ),
        Q.positive: (
            (True, ((Q.positive, 0, True), (Q.positive, 1, True))),
        ),
        Q.positive_infinite: (
            (True, ((Q.extended_real, 0, True), (Q.negative_infinite, 0, False), (Q.positive_infinite, 1, True))),
            (True, ((Q.positive_infinite, 0, True), (Q.extended_real, 1, True), (Q.negative_infinite, 1, False))),
            (False, ((Q.extended_real, 0, True), (Q.positive_infinite, 0, False), (Q.extended_real, 1, True), (Q.positive_infinite, 1, False))),
        ),
        Q.rational: (
            (True, ((Q.rational, 0, True), (Q.rational, 1, True))),
        ),
        Q.real: (
            (True, ((Q.real, 0, True), (Q.real, 1, True))),
        ),
    },
    (Basic, None): {
        Q.composite: (
            (True, ((Q.even, EXPR, True), (Q.positive, EXPR, True), (Q.prime, EXPR, False))),
            (False, ((Q.integer, EXPR, False),)),
            (False, ((Q.positive, EXPR, False),)),
            (False, ((Q.prime, EXPR, True),)),
        ),
        Q.odd: (
            (True, ((Q.even, EXPR, False), (Q.integer, EXPR, True))),
            (False, ((Q.integer, EXPR, False),)),
        ),
    },
    (Expr, None): {
        Q.infinite: (
            (False, ((Q.finite, EXPR, True),)),
        ),
        Q.negative_infinite: (
            (True, ((Q.extended_negative, EXPR, True), (Q.finite, EXPR, False))),
            (False, ((Q.finite, EXPR, True),)),
        ),
        Q.positive_infinite: (
            (True, ((Q.extended_positive, EXPR, True), (Q.finite, EXPR, False))),
            (False, ((Q.finite, EXPR, True),)),
        ),
    },
    (MatMul, 2): {
        Q.invertible: (
            (True, ((Q.invertible, 0, True), (Q.square, 0, True), (Q.invertible, 1, True), (Q.square, 1, True))),
            (False, ((Q.invertible, 0, False), (Q.square, 0, True), (Q.square, 1, True))),
            (False, ((Q.square, 0, True), (Q.invertible, 1, False), (Q.square, 1, True))),
        ),
    },
    (Mul, 2): {
        Q.commutative: (
            (True, ((Q.commutative, 0, True), (Q.commutative, 1, True))),
        ),
        Q.complex: (
            (False, ((Q.finite, 0, False),)),
            (False, ((Q.finite, 1, False),)),
        ),
        Q.composite: (
            (True, ((Q.composite, 0, True), (Q.composite, 1, True))),
            (True, ((Q.composite, 0, True), (Q.prime, 1, True))),
            (True, ((Q.prime, 0, True), (Q.composite, 1, True))),
            (True, ((Q.prime, 0, True), (Q.prime, 1, True))),
        ),
        Q.even: (
            (True, ((Q.even, 0, True), (Q.integer, 1, True))),
            (True, ((Q.integer, 0, True), (Q.even, 1, True))),
            (True, ((Q.even, 0, True), (Q.integer, 0, True), (Q.integer, 1, True))),
            (True, ((Q.integer, 0, True), (Q.even, 1, True), (Q.integer, 1, True))),
            (False, ((Q.even, 0, False), (Q.integer, 0, True), (Q.even, 1, False), (Q.integer, 1, True))),
        ),
        Q.finite: (
            (True, ((Q.finite, 0, True), (Q.finite, 1, True))),
        ),
        Q.imaginary: (
            (True, ((Q.imaginary, 0, True), (Q.real, 1, True), (Q.zero, 1, False))),
            (True, ((Q.real, 0, True), (Q.zero, 0, False), (Q.imaginary, 1, True))),
        ),
        Q.infinite: (
            (True, ((Q.finite, 0, False), (Q.extended_nonzero, 1, True))),
            (True, ((Q.finite, 0, False), (Q.infinite, 1, True))),
            (True, ((Q.zero, 0, False), (Q.infinite, 1, True))),
            (True, ((Q.finite, 0, False), (Q.finite, 1, True), (Q.zero, 1, False))),
        ),
        Q.integer: (
            (True, ((Q.integer, 0, True), (Q.integer, 1, True))),
        ),
        Q.irrational: (
            (True, ((Q.irrational, 0, True), (Q.rational, 1, True), (Q.zero, 1, False))),
            (True, ((Q.rational, 0, True), (Q.zero, 0, False), (Q.irrational, 1, True))),
        ),
        Q.odd: (
            (True, ((Q.odd, 0, True), (Q.odd, 1, True))),
        ),
        Q.positive: (
            (True, ((Q.positive, 0, True), (Q.positive, 1, True))),
        ),
        Q.prime: (
            (False, ((Q.composite, 0, True), (Q.integer, 1, True))),
            (False, ((Q.integer, 0, True), (Q.composite, 1, True))),
        ),
        Q.rational: (
            (True, ((Q.rational, 0, True), (Q.rational, 1, True))),
            (False, ((Q.rational, 0, False), (Q.rational, 1, True), (Q.zero, 1, False))),
            (False, ((Q.rational, 0, True), (Q.zero, 0, False), (Q.rational, 1, False))),
        ),
        Q.real: (
            (True, ((Q.real, 0, True), (Q.real, 1, True))),
        ),
        Q.zero: (
            (True, ((Q.finite, 0, True), (Q.zero, 1, True))),
            (True, ((Q.zero, 0, True), (Q.finite, 1, True))),
            (False, ((Q.zero, 0, False), (Q.zero, 1, False))),
        ),
    },
    (Pow, 2): {
        Q.even: (
            (True, ((Q.even, 0, True), (Q.integer, 1, True), (Q.positive, 1, True))),
        ),
        Q.finite: (
            (True, ((Q.finite, 0, True), (Q.nonnegative, 1, True))),
            (True, ((Q.finite, 0, True), (Q.zero, 0, False), (Q.finite, 1, True))),
        ),
        Q.infinite: (
            (True, ((Q.finite, 0, False), (Q.positive, 1, True))),
            (True, ((Q.zero, 0, True), (Q.extended_negative, 1, True))),
        ),
        Q.nonnegative: (
            (True, ((Q.nonnegative, 0, True), (Q.nonnegative, 1, True), (Q.odd, 1, True))),
            (True, ((Q.real, 0, True), (Q.even, 1, True), (Q.nonnegative, 1, True))),
        ),
        Q.nonpositive: (
            (True, ((Q.nonpositive, 0, True), (Q.nonnegative, 1, True), (Q.odd, 1, True))),
        ),
        Q.odd: (
            (True, ((Q.odd, 0, True), (Q.integer, 1, True), (Q.negative, 1, False))),
        ),
        Q.prime: (
            (True, ((Q.prime, 0, True), (Q.composite, 1, False), (Q.integer, 1, True), (Q.positive, 1, True), (Q.prime, 1, False))),
            (False, ((Q.integer, 0, True), (Q.composite, 1, True))),
            (False, ((Q.integer, 0, True), (Q.prime, 1, True))),
            (False, ((Q.integer, 0, True), (Q.prime, 0, False), (Q.integer, 1, True))),
            (False, ((Q.integer, 0, True), (Q.integer, 1, True), (Q.positive, 1, False))),
        ),
        Q.zero: (
            (True, ((Q.zero, 0, True), (Q.positive, 1, True))),
            (False, ((Q.zero, 0, False), (Q.positive, 1, True))),
            (False, ((Q.finite, 0, True), (Q.zero, 0, False), (Q.finite, 1, True))),
            (False, ((Q.finite, 0, True), (Q.positive, 1, False), (Q.real, 1, True))),
        ),
    },
    (Symbol, None): {
        Q.infinite: (
            (True, ((Q.commutative, EXPR, True), (Q.finite, EXPR, False))),
        ),
    },
    (cos, 1): {
        Q.finite: (
            (True, ((Q.finite, 0, True),)),
        ),
    },
    (exp, 1): {
        Q.finite: (
            (True, ((Q.finite, 0, True),)),
        ),
        Q.positive_infinite: (
            (True, ((Q.positive_infinite, 0, True),)),
        ),
        Q.zero: (
            (True, ((Q.negative_infinite, 0, True),)),
        ),
    },
    (im, 1): {
        Q.even: (
            (True, ((Q.real, 0, True),)),
        ),
    },
    (log, 1): {
        Q.finite: (
            (True, ((Q.finite, 0, True), (Q.zero, 0, False))),
        ),
        Q.infinite: (
            (True, ((Q.finite, 0, False),)),
            (True, ((Q.zero, 0, True),)),
        ),
        Q.positive_infinite: (
            (True, ((Q.positive_infinite, 0, True),)),
        ),
    },
    (re, 1): {
        Q.even: (
            (True, ((Q.even, 0, True),)),
            (False, ((Q.even, 0, False), (Q.real, 0, True))),
        ),
        Q.odd: (
            (True, ((Q.odd, 0, True),)),
        ),
    },
    (sign, 1): {
        Q.finite: (
            (True, ()),
        ),
    },
    (sin, 1): {
        Q.finite: (
            (True, ((Q.finite, 0, True),)),
        ),
    },
}
