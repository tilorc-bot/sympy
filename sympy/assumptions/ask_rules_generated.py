"""
Do NOT manually edit this file.
Instead, run ./bin/ask_update.py.
"""

from sympy.assumptions.ask import Q
from sympy.core.add import Add
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.core.mul import Mul
from sympy.core.numbers import Integer
from sympy.core.numbers import Rational
from sympy.core.power import Pow
from sympy.core.symbol import Symbol
from sympy.functions.combinatorial.factorials import factorial
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.complexes import im
from sympy.functions.elementary.complexes import re
from sympy.functions.elementary.complexes import sign
from sympy.functions.elementary.exponential import exp
from sympy.functions.elementary.exponential import log
from sympy.functions.elementary.trigonometric import acos
from sympy.functions.elementary.trigonometric import acot
from sympy.functions.elementary.trigonometric import asin
from sympy.functions.elementary.trigonometric import atan
from sympy.functions.elementary.trigonometric import cos
from sympy.functions.elementary.trigonometric import cot
from sympy.functions.elementary.trigonometric import sin
from sympy.functions.elementary.trigonometric import tan
from sympy.matrices.expressions.blockmatrix import BlockDiagMatrix
from sympy.matrices.expressions.determinant import Determinant
from sympy.matrices.expressions.hadamard import HadamardProduct
from sympy.matrices.expressions.inverse import Inverse
from sympy.matrices.expressions.matadd import MatAdd
from sympy.matrices.expressions.matexpr import MatrixElement
from sympy.matrices.expressions.matmul import MatMul
from sympy.matrices.expressions.matpow import MatPow
from sympy.matrices.expressions.slice import MatrixSlice
from sympy.matrices.expressions.trace import Trace
from sympy.matrices.expressions.transpose import Transpose

# A condition ``(predicate, slot, value)`` holds when asking the predicate
# about an expression gives ``value``. The expression is the argument number
# ``slot`` of the expression which a rule is about, or that expression itself
# for the slot ``EXPR``. A sum, a product and a block diagonal matrix are read
# as their first argument and the rest. A condition ``(Q.eq, (a, b), value)``
# holds when it is found that the arguments of the slots ``a`` and ``b`` are
# equal, or not equal for the value ``False``. One of ``a`` and ``b`` can be
# a number instead of a slot.
EXPR = -1

# For each class and number of arguments, the ways to find the truth value of
# each predicate for an instance: a truth value, and the conditions which
# together give it. The ways under ``None`` are for any number of arguments.
ASK_RULES = {
    (Abs, 1): {
        Q.algebraic: (
            (True, ((Q.algebraic, 0, True),)),
        ),
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
        Q.positive: (
            (True, ((Q.finite, 0, True), (Q.zero, 0, False))),
        ),
        Q.rational: (
            (True, ((Q.rational, 0, True),)),
        ),
        Q.real: (
            (True, ((Q.complex, 0, True),)),
        ),
        Q.zero: (
            (True, ((Q.zero, 0, True),)),
            (False, ((Q.zero, 0, False),)),
        ),
    },
    (Add, 2): {
        Q.algebraic: (
            (True, ((Q.algebraic, 0, True), (Q.algebraic, 1, True))),
            (False, ((Q.algebraic, 0, False), (Q.algebraic, 1, True))),
            (False, ((Q.algebraic, 0, True), (Q.algebraic, 1, False))),
        ),
        Q.antihermitian: (
            (True, ((Q.antihermitian, 0, True), (Q.antihermitian, 1, True))),
            (False, ((Q.antihermitian, 0, False), (Q.antihermitian, 1, True))),
            (False, ((Q.antihermitian, 0, True), (Q.antihermitian, 1, False))),
        ),
        Q.complex: (
            (True, ((Q.complex, 0, True), (Q.complex, 1, True))),
            (False, ((Q.complex, 0, False), (Q.complex, 1, True))),
            (False, ((Q.complex, 0, True), (Q.complex, 1, False))),
        ),
        Q.even: (
            (True, ((Q.even, 0, True), (Q.even, 1, True))),
            (True, ((Q.odd, 0, True), (Q.odd, 1, True))),
        ),
        Q.extended_negative: (
            (True, ((Q.extended_negative, 0, True), (Q.extended_negative, 1, True))),
        ),
        Q.extended_nonnegative: (
            (True, ((Q.extended_nonnegative, 0, True), (Q.extended_nonnegative, 1, True))),
        ),
        Q.extended_nonpositive: (
            (True, ((Q.extended_nonpositive, 0, True), (Q.extended_nonpositive, 1, True))),
        ),
        Q.extended_positive: (
            (True, ((Q.extended_positive, 0, True), (Q.extended_positive, 1, True))),
        ),
        Q.extended_real: (
            (True, ((Q.extended_negative, 0, True), (Q.extended_negative, 1, True))),
            (True, ((Q.extended_positive, 0, True), (Q.extended_positive, 1, True))),
            (True, ((Q.extended_real, 0, True), (Q.real, 1, True))),
            (True, ((Q.real, 0, True), (Q.extended_real, 1, True))),
            (False, ((Q.extended_real, 0, False), (Q.real, 1, True))),
            (False, ((Q.imaginary, 0, True), (Q.real, 1, True))),
            (False, ((Q.real, 0, True), (Q.extended_real, 1, False))),
            (False, ((Q.real, 0, True), (Q.imaginary, 1, True))),
        ),
        Q.finite: (
            (True, ((Q.finite, 0, True), (Q.finite, 1, True))),
        ),
        Q.hermitian: (
            (True, ((Q.hermitian, 0, True), (Q.hermitian, 1, True))),
            (False, ((Q.hermitian, 0, False), (Q.hermitian, 1, True))),
            (False, ((Q.hermitian, 0, True), (Q.hermitian, 1, False))),
        ),
        Q.imaginary: (
            (True, ((Q.imaginary, 0, True), (Q.imaginary, 1, True), (Q.zero, EXPR, False))),
            (False, ((Q.imaginary, 0, True), (Q.real, 1, True), (Q.zero, 1, False))),
            (False, ((Q.real, 0, True), (Q.zero, 0, False), (Q.imaginary, 1, True))),
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
            (True, ((Q.negative, 0, True), (Q.nonpositive, 1, True))),
            (True, ((Q.nonpositive, 0, True), (Q.negative, 1, True))),
        ),
        Q.negative_infinite: (
            (True, ((Q.extended_real, 0, True), (Q.positive_infinite, 0, False), (Q.negative_infinite, 1, True))),
            (True, ((Q.negative_infinite, 0, True), (Q.extended_real, 1, True), (Q.positive_infinite, 1, False))),
            (False, ((Q.extended_real, 0, True), (Q.negative_infinite, 0, False), (Q.extended_real, 1, True), (Q.negative_infinite, 1, False))),
        ),
        Q.nonnegative: (
            (True, ((Q.nonnegative, 0, True), (Q.nonnegative, 1, True))),
        ),
        Q.nonpositive: (
            (True, ((Q.nonpositive, 0, True), (Q.nonpositive, 1, True))),
        ),
        Q.odd: (
            (True, ((Q.even, 0, True), (Q.odd, 1, True))),
            (True, ((Q.odd, 0, True), (Q.even, 1, True))),
        ),
        Q.positive: (
            (True, ((Q.nonnegative, 0, True), (Q.positive, 1, True))),
            (True, ((Q.positive, 0, True), (Q.nonnegative, 1, True))),
            (True, ((Q.positive, 0, True), (Q.positive, 1, True))),
        ),
        Q.positive_infinite: (
            (True, ((Q.extended_real, 0, True), (Q.negative_infinite, 0, False), (Q.positive_infinite, 1, True))),
            (True, ((Q.positive_infinite, 0, True), (Q.extended_real, 1, True), (Q.negative_infinite, 1, False))),
            (False, ((Q.extended_real, 0, True), (Q.positive_infinite, 0, False), (Q.extended_real, 1, True), (Q.positive_infinite, 1, False))),
        ),
        Q.rational: (
            (True, ((Q.rational, 0, True), (Q.rational, 1, True))),
            (False, ((Q.rational, 0, False), (Q.rational, 1, True))),
            (False, ((Q.rational, 0, True), (Q.rational, 1, False))),
        ),
        Q.real: (
            (True, ((Q.real, 0, True), (Q.real, 1, True))),
            (False, ((Q.real, 0, False), (Q.real, 1, True))),
            (False, ((Q.real, 0, True), (Q.real, 1, False))),
        ),
        Q.transcendental: (
            (True, ((Q.algebraic, 0, True), (Q.transcendental, 1, True))),
            (True, ((Q.transcendental, 0, True), (Q.algebraic, 1, True))),
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
    (BlockDiagMatrix, 1): {
        Q.complex_elements: (
            (True, ((Q.complex_elements, 0, True),)),
            (False, ((Q.complex_elements, 0, False),)),
        ),
        Q.integer_elements: (
            (True, ((Q.integer_elements, 0, True),)),
            (False, ((Q.integer_elements, 0, False),)),
        ),
        Q.invertible: (
            (True, ((Q.invertible, 0, True),)),
            (False, ((Q.invertible, 0, False),)),
        ),
        Q.real_elements: (
            (True, ((Q.real_elements, 0, True),)),
            (False, ((Q.real_elements, 0, False),)),
        ),
    },
    (BlockDiagMatrix, 2): {
        Q.complex_elements: (
            (True, ((Q.complex_elements, 0, True), (Q.complex_elements, 1, True))),
            (False, ((Q.complex_elements, 0, False),)),
            (False, ((Q.complex_elements, 1, False),)),
        ),
        Q.integer_elements: (
            (True, ((Q.integer_elements, 0, True), (Q.integer_elements, 1, True))),
            (False, ((Q.integer_elements, 0, False),)),
            (False, ((Q.integer_elements, 1, False),)),
        ),
        Q.invertible: (
            (True, ((Q.invertible, 0, True), (Q.invertible, 1, True))),
            (False, ((Q.invertible, 0, False),)),
            (False, ((Q.invertible, 1, False),)),
        ),
        Q.real_elements: (
            (True, ((Q.real_elements, 0, True), (Q.real_elements, 1, True))),
            (False, ((Q.real_elements, 0, False),)),
            (False, ((Q.real_elements, 1, False),)),
        ),
    },
    (Determinant, 1): {
        Q.complex: (
            (True, ((Q.complex_elements, 0, True),)),
        ),
        Q.complex_elements: (
            (True, ((Q.complex_elements, 0, True),)),
        ),
        Q.integer: (
            (True, ((Q.integer_elements, 0, True),)),
        ),
        Q.integer_elements: (
            (True, ((Q.integer_elements, 0, True),)),
        ),
        Q.positive: (
            (True, ((Q.positive_definite, 0, True),)),
        ),
        Q.real: (
            (True, ((Q.real_elements, 0, True),)),
        ),
        Q.real_elements: (
            (True, ((Q.real_elements, 0, True),)),
        ),
    },
    (Expr, None): {
        Q.antihermitian: (
            (True, ((Q.imaginary, EXPR, True),)),
        ),
        Q.diagonal: (
            (True, ((Q.lower_triangular, EXPR, True), (Q.upper_triangular, EXPR, True))),
        ),
        Q.extended_real: (
            (True, ((Q.extended_negative, EXPR, True),)),
            (True, ((Q.extended_positive, EXPR, True),)),
            (True, ((Q.zero, EXPR, True),)),
        ),
        Q.hermitian: (
            (True, ((Q.real, EXPR, True),)),
        ),
        Q.infinite: (
            (False, ((Q.finite, EXPR, True),)),
        ),
        Q.invertible: (
            (True, ((Q.fullrank, EXPR, True), (Q.square, EXPR, True))),
        ),
        Q.irrational: (
            (True, ((Q.rational, EXPR, False), (Q.real, EXPR, True))),
        ),
        Q.negative_infinite: (
            (True, ((Q.extended_negative, EXPR, True), (Q.finite, EXPR, False))),
            (False, ((Q.finite, EXPR, True),)),
        ),
        Q.nonzero: (
            (False, ((Q.real, EXPR, False),)),
        ),
        Q.positive_infinite: (
            (True, ((Q.extended_positive, EXPR, True), (Q.finite, EXPR, False))),
            (False, ((Q.finite, EXPR, True),)),
        ),
        Q.transcendental: (
            (True, ((Q.algebraic, EXPR, False), (Q.complex, EXPR, True))),
        ),
        Q.zero: (
            (True, ((Q.nonzero, EXPR, False), (Q.real, EXPR, True))),
            (False, ((Q.real, EXPR, False),)),
        ),
    },
    (HadamardProduct, 2): {
        Q.complex_elements: (
            (True, ((Q.complex_elements, 0, True), (Q.complex_elements, 1, True))),
        ),
        Q.integer_elements: (
            (True, ((Q.integer_elements, 0, True), (Q.integer_elements, 1, True))),
        ),
        Q.real_elements: (
            (True, ((Q.real_elements, 0, True), (Q.real_elements, 1, True))),
        ),
    },
    (Inverse, 2): {
        Q.complex_elements: (
            (True, ((Q.complex_elements, 0, True),)),
        ),
        Q.diagonal: (
            (True, ((Q.diagonal, 0, True),)),
            (False, ((Q.diagonal, 0, False),)),
        ),
        Q.invertible: (
            (True, ()),
        ),
        Q.lower_triangular: (
            (True, ((Q.lower_triangular, 0, True),)),
            (False, ((Q.lower_triangular, 0, False),)),
        ),
        Q.orthogonal: (
            (True, ((Q.orthogonal, 0, True),)),
            (False, ((Q.orthogonal, 0, False),)),
        ),
        Q.positive_definite: (
            (True, ((Q.positive_definite, 0, True),)),
            (False, ((Q.positive_definite, 0, False),)),
        ),
        Q.real_elements: (
            (True, ((Q.real_elements, 0, True),)),
        ),
        Q.symmetric: (
            (True, ((Q.symmetric, 0, True),)),
            (False, ((Q.symmetric, 0, False),)),
        ),
        Q.unitary: (
            (True, ((Q.unitary, 0, True),)),
            (False, ((Q.unitary, 0, False),)),
        ),
        Q.upper_triangular: (
            (True, ((Q.upper_triangular, 0, True),)),
            (False, ((Q.upper_triangular, 0, False),)),
        ),
    },
    (MatAdd, 2): {
        Q.complex_elements: (
            (True, ((Q.complex_elements, 0, True), (Q.complex_elements, 1, True))),
        ),
        Q.diagonal: (
            (True, ((Q.diagonal, 0, True), (Q.diagonal, 1, True))),
            (False, ((Q.diagonal, 0, False), (Q.diagonal, 1, True))),
            (False, ((Q.diagonal, 0, True), (Q.diagonal, 1, False))),
        ),
        Q.integer_elements: (
            (True, ((Q.integer_elements, 0, True), (Q.integer_elements, 1, True))),
        ),
        Q.lower_triangular: (
            (True, ((Q.lower_triangular, 0, True), (Q.lower_triangular, 1, True))),
            (False, ((Q.lower_triangular, 0, False), (Q.lower_triangular, 1, True))),
            (False, ((Q.lower_triangular, 0, True), (Q.lower_triangular, 1, False))),
        ),
        Q.positive_definite: (
            (True, ((Q.positive_definite, 0, True), (Q.positive_definite, 1, True))),
        ),
        Q.real_elements: (
            (True, ((Q.real_elements, 0, True), (Q.real_elements, 1, True))),
        ),
        Q.symmetric: (
            (True, ((Q.symmetric, 0, True), (Q.symmetric, 1, True))),
            (False, ((Q.symmetric, 0, False), (Q.symmetric, 1, True))),
            (False, ((Q.symmetric, 0, True), (Q.symmetric, 1, False))),
        ),
        Q.upper_triangular: (
            (True, ((Q.upper_triangular, 0, True), (Q.upper_triangular, 1, True))),
            (False, ((Q.upper_triangular, 0, False), (Q.upper_triangular, 1, True))),
            (False, ((Q.upper_triangular, 0, True), (Q.upper_triangular, 1, False))),
        ),
    },
    (MatMul, 2): {
        Q.complex_elements: (
            (True, ((Q.complex, 0, True), (Q.complex_elements, 1, True))),
            (True, ((Q.complex_elements, 0, True), (Q.complex_elements, 1, True))),
        ),
        Q.diagonal: (
            (True, ((Q.complex, 0, True), (Q.diagonal, 1, True))),
            (True, ((Q.diagonal, 0, True), (Q.diagonal, 1, True))),
        ),
        Q.fullrank: (
            (True, ((Q.fullrank, 0, True), (Q.square, 0, True), (Q.fullrank, 1, True))),
            (True, ((Q.fullrank, 0, True), (Q.fullrank, 1, True), (Q.square, 1, True))),
        ),
        Q.integer_elements: (
            (True, ((Q.integer, 0, True), (Q.integer_elements, 1, True))),
            (True, ((Q.integer_elements, 0, True), (Q.integer_elements, 1, True))),
        ),
        Q.invertible: (
            (True, ((Q.complex, 0, True), (Q.zero, 0, False), (Q.invertible, 1, True))),
            (True, ((Q.invertible, 0, True), (Q.square, 0, True), (Q.invertible, 1, True), (Q.square, 1, True))),
            (False, ((Q.invertible, 0, False), (Q.square, 0, True), (Q.square, 1, True))),
            (False, ((Q.square, 0, True), (Q.invertible, 1, False), (Q.square, 1, True))),
        ),
        Q.lower_triangular: (
            (True, ((Q.complex, 0, True), (Q.lower_triangular, 1, True))),
            (True, ((Q.lower_triangular, 0, True), (Q.lower_triangular, 1, True))),
        ),
        Q.orthogonal: (
            (True, ((Q.orthogonal, 0, True), (Q.orthogonal, 1, True))),
        ),
        Q.positive_definite: (
            (True, ((Q.positive, 0, True), (Q.positive_definite, 1, True))),
        ),
        Q.real_elements: (
            (True, ((Q.real, 0, True), (Q.real_elements, 1, True))),
            (True, ((Q.real_elements, 0, True), (Q.real_elements, 1, True))),
        ),
        Q.symmetric: (
            (True, ((Q.complex, 0, True), (Q.symmetric, 1, True))),
        ),
        Q.unitary: (
            (True, ((Q.unitary, 0, True), (Q.unitary, 1, True))),
        ),
        Q.upper_triangular: (
            (True, ((Q.complex, 0, True), (Q.upper_triangular, 1, True))),
            (True, ((Q.upper_triangular, 0, True), (Q.upper_triangular, 1, True))),
        ),
    },
    (MatPow, 2): {
        Q.complex_elements: (
            (True, ((Q.complex_elements, 0, True), (Q.invertible, 0, True), (Q.integer, 1, True))),
            (True, ((Q.complex_elements, 0, True), (Q.integer, 1, True), (Q.negative, 1, False))),
        ),
        Q.diagonal: (
            (True, ((Q.diagonal, 0, True), (Q.invertible, 0, True), (Q.integer, 1, True))),
            (True, ((Q.diagonal, 0, True), (Q.integer, 1, True), (Q.negative, 1, False))),
        ),
        Q.fullrank: (
            (True, ((Q.fullrank, 0, True), (Q.integer, 1, True))),
        ),
        Q.integer_elements: (
            (True, ((Q.integer_elements, 0, True), (Q.integer, 1, True), (Q.negative, 1, False))),
        ),
        Q.invertible: (
            (True, ((Q.invertible, 0, True), (Q.integer, 1, True))),
            (False, ((Q.invertible, 0, False), (Q.integer, 1, True), (Q.positive, 1, True))),
        ),
        Q.lower_triangular: (
            (True, ((Q.invertible, 0, True), (Q.lower_triangular, 0, True), (Q.integer, 1, True))),
            (True, ((Q.lower_triangular, 0, True), (Q.integer, 1, True), (Q.negative, 1, False))),
        ),
        Q.orthogonal: (
            (True, ((Q.orthogonal, 0, True), (Q.integer, 1, True))),
        ),
        Q.positive_definite: (
            (True, ((Q.positive_definite, 0, True), (Q.integer, 1, True))),
        ),
        Q.real_elements: (
            (True, ((Q.invertible, 0, True), (Q.real_elements, 0, True), (Q.integer, 1, True))),
            (True, ((Q.real_elements, 0, True), (Q.integer, 1, True), (Q.negative, 1, False))),
        ),
        Q.symmetric: (
            (True, ((Q.invertible, 0, True), (Q.symmetric, 0, True), (Q.integer, 1, True))),
            (True, ((Q.symmetric, 0, True), (Q.integer, 1, True), (Q.negative, 1, False))),
        ),
        Q.unitary: (
            (True, ((Q.unitary, 0, True), (Q.integer, 1, True))),
        ),
        Q.upper_triangular: (
            (True, ((Q.invertible, 0, True), (Q.upper_triangular, 0, True), (Q.integer, 1, True))),
            (True, ((Q.upper_triangular, 0, True), (Q.integer, 1, True), (Q.negative, 1, False))),
        ),
    },
    (MatrixElement, 3): {
        Q.complex: (
            (True, ((Q.complex_elements, 0, True),)),
        ),
        Q.integer: (
            (True, ((Q.integer_elements, 0, True),)),
        ),
        Q.positive: (
            (True, ((Q.positive_definite, 0, True), (Q.eq, (1, 2), True))),
        ),
        Q.real: (
            (True, ((Q.real_elements, 0, True),)),
        ),
    },
    (MatrixSlice, 3): {
        Q.complex_elements: (
            (True, ((Q.complex_elements, 0, True),)),
        ),
        Q.diagonal: (
            (True, ((Q.diagonal, 0, True), (Q.eq, (1, 2), True))),
        ),
        Q.integer_elements: (
            (True, ((Q.integer_elements, 0, True),)),
        ),
        Q.positive_definite: (
            (True, ((Q.positive_definite, 0, True), (Q.eq, (1, 2), True))),
        ),
        Q.real_elements: (
            (True, ((Q.real_elements, 0, True),)),
        ),
        Q.symmetric: (
            (True, ((Q.symmetric, 0, True), (Q.eq, (1, 2), True))),
        ),
    },
    (Mul, 2): {
        Q.algebraic: (
            (True, ((Q.algebraic, 0, True), (Q.algebraic, 1, True))),
            (False, ((Q.algebraic, 0, False), (Q.algebraic, 1, True), (Q.zero, 1, False))),
            (False, ((Q.algebraic, 0, True), (Q.zero, 0, False), (Q.algebraic, 1, False))),
        ),
        Q.antihermitian: (
            (True, ((Q.antihermitian, 0, True), (Q.commutative, 0, True), (Q.hermitian, 1, True))),
            (True, ((Q.antihermitian, 0, True), (Q.commutative, 1, True), (Q.hermitian, 1, True))),
            (True, ((Q.commutative, 0, True), (Q.hermitian, 0, True), (Q.antihermitian, 1, True))),
            (True, ((Q.hermitian, 0, True), (Q.antihermitian, 1, True), (Q.commutative, 1, True))),
        ),
        Q.commutative: (
            (True, ((Q.commutative, 0, True), (Q.commutative, 1, True))),
        ),
        Q.complex: (
            (True, ((Q.complex, 0, True), (Q.complex, 1, True))),
            (False, ((Q.finite, 0, False),)),
            (False, ((Q.finite, 1, False),)),
            (False, ((Q.complex, 0, False), (Q.complex, 1, True))),
            (False, ((Q.complex, 0, True), (Q.complex, 1, False))),
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
        Q.extended_negative: (
            (True, ((Q.extended_negative, 0, True), (Q.extended_positive, 1, True))),
            (True, ((Q.extended_positive, 0, True), (Q.extended_negative, 1, True))),
        ),
        Q.extended_nonzero: (
            (False, ((Q.zero, 0, True),)),
            (False, ((Q.zero, 1, True),)),
        ),
        Q.extended_positive: (
            (True, ((Q.extended_negative, 0, True), (Q.extended_negative, 1, True))),
            (True, ((Q.extended_positive, 0, True), (Q.extended_positive, 1, True))),
        ),
        Q.extended_real: (
            (True, ((Q.extended_real, 0, True), (Q.zero, 0, False), (Q.extended_real, 1, True), (Q.zero, 1, False))),
        ),
        Q.finite: (
            (True, ((Q.finite, 0, True), (Q.finite, 1, True))),
        ),
        Q.hermitian: (
            (True, ((Q.antihermitian, 0, True), (Q.commutative, 0, True), (Q.antihermitian, 1, True))),
            (True, ((Q.antihermitian, 0, True), (Q.antihermitian, 1, True), (Q.commutative, 1, True))),
            (True, ((Q.commutative, 0, True), (Q.hermitian, 0, True), (Q.hermitian, 1, True))),
            (True, ((Q.hermitian, 0, True), (Q.commutative, 1, True), (Q.hermitian, 1, True))),
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
            (True, ((Q.eq, (0, Rational(1, 2)), True), (Q.even, 1, True))),
            (False, ((Q.eq, (0, Rational(1, 2)), True), (Q.odd, 1, True))),
        ),
        Q.irrational: (
            (True, ((Q.irrational, 0, True), (Q.rational, 1, True), (Q.zero, 1, False))),
            (True, ((Q.rational, 0, True), (Q.zero, 0, False), (Q.irrational, 1, True))),
        ),
        Q.negative: (
            (True, ((Q.negative, 0, True), (Q.positive, 1, True))),
            (True, ((Q.positive, 0, True), (Q.negative, 1, True))),
        ),
        Q.nonnegative: (
            (True, ((Q.nonnegative, 0, True), (Q.nonnegative, 1, True))),
            (True, ((Q.nonpositive, 0, True), (Q.nonpositive, 1, True))),
        ),
        Q.nonpositive: (
            (True, ((Q.nonnegative, 0, True), (Q.nonpositive, 1, True))),
            (True, ((Q.nonpositive, 0, True), (Q.nonnegative, 1, True))),
        ),
        Q.nonzero: (
            (True, ((Q.nonzero, 0, True), (Q.nonzero, 1, True))),
        ),
        Q.odd: (
            (True, ((Q.odd, 0, True), (Q.odd, 1, True))),
        ),
        Q.positive: (
            (True, ((Q.negative, 0, True), (Q.negative, 1, True))),
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
            (True, ((Q.imaginary, 0, True), (Q.imaginary, 1, True))),
            (True, ((Q.real, 0, True), (Q.real, 1, True))),
            (True, ((Q.imaginary, 0, True), (Q.real, 1, True), (Q.zero, EXPR, True))),
            (True, ((Q.real, 0, True), (Q.imaginary, 1, True), (Q.zero, EXPR, True))),
            (False, ((Q.imaginary, 0, True), (Q.real, 1, True), (Q.zero, EXPR, False))),
            (False, ((Q.real, 0, True), (Q.imaginary, 1, True), (Q.zero, EXPR, False))),
        ),
        Q.transcendental: (
            (True, ((Q.algebraic, 0, True), (Q.zero, 0, False), (Q.transcendental, 1, True))),
            (True, ((Q.transcendental, 0, True), (Q.algebraic, 1, True), (Q.zero, 1, False))),
        ),
        Q.zero: (
            (True, ((Q.finite, 0, True), (Q.zero, 1, True))),
            (True, ((Q.zero, 0, True), (Q.finite, 1, True))),
            (True, ((Q.imaginary, 0, True), (Q.real, 1, True), (Q.real, EXPR, True))),
            (True, ((Q.real, 0, True), (Q.imaginary, 1, True), (Q.real, EXPR, True))),
            (False, ((Q.zero, 0, False), (Q.zero, 1, False))),
            (False, ((Q.imaginary, 0, True), (Q.real, 1, True), (Q.real, EXPR, False))),
            (False, ((Q.real, 0, True), (Q.imaginary, 1, True), (Q.real, EXPR, False))),
        ),
    },
    (Pow, 2): {
        Q.algebraic: (
            (True, ((Q.algebraic, 0, True), (Q.zero, 0, False), (Q.rational, 1, True))),
            (True, ((Q.algebraic, 0, True), (Q.negative, 1, False), (Q.rational, 1, True))),
            (False, ((Q.algebraic, 0, False), (Q.integer, 1, True), (Q.positive, 1, True))),
        ),
        Q.antihermitian: (
            (True, ((Q.antihermitian, 0, True), (Q.zero, 0, False), (Q.odd, 1, True))),
            (True, ((Q.antihermitian, 0, True), (Q.negative, 1, False), (Q.odd, 1, True))),
        ),
        Q.complex: (
            (True, ((Q.complex, 0, True), (Q.positive, 1, True))),
            (True, ((Q.complex, 0, True), (Q.zero, 0, False), (Q.complex, 1, True))),
            (True, ((Q.complex, 0, True), (Q.integer, 1, True), (Q.negative, 1, False))),
            (False, ((Q.zero, 0, True), (Q.negative, 1, True))),
        ),
        Q.even: (
            (True, ((Q.even, 0, True), (Q.integer, 1, True), (Q.positive, 1, True))),
        ),
        Q.extended_real: (
            (True, ((Q.extended_real, 0, True), (Q.zero, 0, False), (Q.integer, 1, True))),
            (True, ((Q.extended_real, 0, True), (Q.integer, 1, True), (Q.negative, 1, False))),
            (False, ((Q.zero, 0, True), (Q.negative, 1, True))),
        ),
        Q.finite: (
            (True, ((Q.finite, 0, True), (Q.nonnegative, 1, True))),
            (True, ((Q.finite, 0, True), (Q.zero, 0, False), (Q.finite, 1, True))),
        ),
        Q.hermitian: (
            (True, ((Q.antihermitian, 0, True), (Q.zero, 0, False), (Q.even, 1, True))),
            (True, ((Q.antihermitian, 0, True), (Q.even, 1, True), (Q.negative, 1, False))),
            (True, ((Q.hermitian, 0, True), (Q.zero, 0, False), (Q.integer, 1, True))),
            (True, ((Q.hermitian, 0, True), (Q.integer, 1, True), (Q.negative, 1, False))),
        ),
        Q.imaginary: (
            (True, ((Q.imaginary, 0, True), (Q.odd, 1, True))),
            (False, ((Q.real, 0, True), (Q.integer, 1, True))),
            (False, ((Q.real, 0, True), (Q.irrational, 1, True))),
        ),
        Q.infinite: (
            (True, ((Q.finite, 0, False), (Q.positive, 1, True))),
            (True, ((Q.zero, 0, True), (Q.extended_negative, 1, True))),
        ),
        Q.integer: (
            (True, ((Q.zero, 1, True),)),
            (True, ((Q.integer, 0, True), (Q.integer, 1, True), (Q.negative, 1, False))),
            (False, ((Q.integer, 0, True), (Q.eq, (0, Integer(-1)), False), (Q.eq, (0, Integer(1)), False), (Q.integer, 1, True), (Q.negative, 1, True))),
        ),
        Q.irrational: (
            (True, ((Q.irrational, 0, True), (Q.eq, (1, Integer(-1)), True))),
            (True, ((Q.prime, 0, True), (Q.integer, 1, False), (Q.rational, 1, True))),
        ),
        Q.negative: (
            (True, ((Q.negative, 0, True), (Q.odd, 1, True))),
            (False, ((Q.nonnegative, 0, True), (Q.odd, 1, True))),
            (False, ((Q.real, 0, True), (Q.even, 1, True))),
        ),
        Q.nonnegative: (
            (True, ((Q.nonnegative, 0, True), (Q.nonnegative, 1, True), (Q.odd, 1, True))),
            (True, ((Q.real, 0, True), (Q.even, 1, True), (Q.nonnegative, 1, True))),
        ),
        Q.nonpositive: (
            (True, ((Q.nonpositive, 0, True), (Q.nonnegative, 1, True), (Q.odd, 1, True))),
        ),
        Q.odd: (
            (True, ((Q.eq, (0, Integer(-1)), True), (Q.integer, 1, True))),
            (True, ((Q.eq, (0, Integer(1)), True), (Q.finite, 1, True))),
            (True, ((Q.odd, 0, True), (Q.integer, 1, True), (Q.negative, 1, False))),
        ),
        Q.positive: (
            (True, ((Q.zero, 1, True),)),
            (True, ((Q.nonzero, 0, True), (Q.even, 1, True))),
            (True, ((Q.positive, 0, True), (Q.real, 1, True))),
            (True, ((Q.eq, (0, Integer(1)), True), (Q.finite, 1, True))),
        ),
        Q.prime: (
            (True, ((Q.prime, 0, True), (Q.composite, 1, False), (Q.integer, 1, True), (Q.positive, 1, True), (Q.prime, 1, False))),
            (False, ((Q.integer, 0, True), (Q.composite, 1, True))),
            (False, ((Q.integer, 0, True), (Q.prime, 1, True))),
            (False, ((Q.integer, 0, True), (Q.prime, 0, False), (Q.integer, 1, True))),
            (False, ((Q.integer, 0, True), (Q.integer, 1, True), (Q.positive, 1, False))),
            (False, ((Q.integer, 0, True), (Q.integer, 1, True), (Q.eq, (1, Integer(1)), False))),
        ),
        Q.rational: (
            (True, ((Q.rational, 0, True), (Q.zero, 0, False), (Q.integer, 1, True))),
            (True, ((Q.rational, 0, True), (Q.integer, 1, True), (Q.negative, 1, False))),
        ),
        Q.real: (
            (True, ((Q.imaginary, 0, True), (Q.even, 1, True))),
            (True, ((Q.positive, 0, True), (Q.real, 1, True))),
            (True, ((Q.real, 0, True), (Q.zero, 0, False), (Q.integer, 1, True))),
            (True, ((Q.real, 0, True), (Q.integer, 1, True), (Q.negative, 1, False))),
            (True, ((Q.zero, 0, True), (Q.nonnegative, 1, True), (Q.real, 1, True))),
            (False, ((Q.negative, 0, True), (Q.integer, 1, False), (Q.rational, 1, True))),
        ),
        Q.transcendental: (
            (True, ((Q.transcendental, 0, True), (Q.integer, 1, True), (Q.zero, 1, False))),
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
    (Trace, 1): {
        Q.complex: (
            (True, ((Q.complex_elements, 0, True),)),
        ),
        Q.complex_elements: (
            (True, ((Q.complex_elements, 0, True),)),
        ),
        Q.integer: (
            (True, ((Q.integer_elements, 0, True),)),
        ),
        Q.integer_elements: (
            (True, ((Q.integer_elements, 0, True),)),
        ),
        Q.positive: (
            (True, ((Q.positive_definite, 0, True),)),
        ),
        Q.real: (
            (True, ((Q.real_elements, 0, True),)),
        ),
        Q.real_elements: (
            (True, ((Q.real_elements, 0, True),)),
        ),
    },
    (Transpose, 1): {
        Q.complex_elements: (
            (True, ((Q.complex_elements, 0, True),)),
            (False, ((Q.complex_elements, 0, False),)),
        ),
        Q.diagonal: (
            (True, ((Q.diagonal, 0, True),)),
            (False, ((Q.diagonal, 0, False),)),
        ),
        Q.fullrank: (
            (True, ((Q.fullrank, 0, True),)),
            (False, ((Q.fullrank, 0, False),)),
        ),
        Q.integer_elements: (
            (True, ((Q.integer_elements, 0, True),)),
            (False, ((Q.integer_elements, 0, False),)),
        ),
        Q.invertible: (
            (True, ((Q.invertible, 0, True),)),
            (False, ((Q.invertible, 0, False),)),
        ),
        Q.lower_triangular: (
            (True, ((Q.upper_triangular, 0, True),)),
            (False, ((Q.upper_triangular, 0, False),)),
        ),
        Q.orthogonal: (
            (True, ((Q.orthogonal, 0, True),)),
            (False, ((Q.orthogonal, 0, False),)),
        ),
        Q.positive_definite: (
            (True, ((Q.positive_definite, 0, True),)),
            (False, ((Q.positive_definite, 0, False),)),
        ),
        Q.real_elements: (
            (True, ((Q.real_elements, 0, True),)),
            (False, ((Q.real_elements, 0, False),)),
        ),
        Q.symmetric: (
            (True, ((Q.symmetric, 0, True),)),
            (False, ((Q.symmetric, 0, False),)),
        ),
        Q.unitary: (
            (True, ((Q.unitary, 0, True),)),
            (False, ((Q.unitary, 0, False),)),
        ),
        Q.upper_triangular: (
            (True, ((Q.lower_triangular, 0, True),)),
            (False, ((Q.lower_triangular, 0, False),)),
        ),
    },
    (acos, 1): {
        Q.algebraic: (
            (False, ((Q.algebraic, 0, True), (Q.eq, (0, Integer(1)), False))),
        ),
        Q.negative: (
            (False, ()),
        ),
        Q.positive: (
            (True, ((Q.zero, 0, True),)),
        ),
    },
    (acot, 1): {
        Q.algebraic: (
            (False, ((Q.algebraic, 0, True),)),
        ),
        Q.extended_nonnegative: (
            (True, ((Q.extended_nonnegative, 0, True),)),
        ),
        Q.extended_real: (
            (False, ((Q.finite, 0, True), (Q.real, 0, False))),
        ),
        Q.negative: (
            (True, ((Q.negative, 0, True),)),
        ),
        Q.nonpositive: (
            (True, ((Q.extended_negative, 0, True),)),
        ),
        Q.positive: (
            (True, ((Q.nonnegative, 0, True),)),
        ),
        Q.transcendental: (
            (True, ((Q.algebraic, 0, True), (Q.imaginary, 0, False))),
        ),
    },
    (asin, 1): {
        Q.negative: (
            (False, ((Q.extended_nonnegative, 0, True),)),
        ),
        Q.positive: (
            (False, ((Q.extended_nonpositive, 0, True),)),
        ),
        Q.transcendental: (
            (True, ((Q.algebraic, 0, True), (Q.zero, 0, False))),
        ),
        Q.zero: (
            (True, ((Q.zero, 0, True),)),
        ),
    },
    (atan, 1): {
        Q.algebraic: (
            (False, ((Q.algebraic, 0, True), (Q.zero, 0, False))),
        ),
        Q.extended_real: (
            (False, ((Q.finite, 0, True), (Q.real, 0, False))),
        ),
        Q.negative: (
            (True, ((Q.extended_negative, 0, True),)),
        ),
        Q.positive: (
            (True, ((Q.extended_positive, 0, True),)),
        ),
        Q.transcendental: (
            (True, ((Q.algebraic, 0, True), (Q.imaginary, 0, False), (Q.zero, 0, False))),
        ),
        Q.zero: (
            (True, ((Q.zero, 0, True),)),
        ),
    },
    (cos, 1): {
        Q.complex: (
            (True, ((Q.complex, 0, True),)),
        ),
        Q.finite: (
            (True, ((Q.finite, 0, True),)),
        ),
        Q.integer: (
            (True, ((Q.zero, 0, True),)),
        ),
        Q.real: (
            (True, ((Q.real, 0, True),)),
        ),
        Q.transcendental: (
            (True, ((Q.algebraic, 0, True), (Q.zero, 0, False))),
        ),
    },
    (cot, 1): {
        Q.algebraic: (
            (False, ((Q.algebraic, 0, True),)),
        ),
    },
    (exp, 1): {
        Q.complex: (
            (True, ((Q.complex, 0, True),)),
        ),
        Q.extended_nonnegative: (
            (True, ((Q.extended_real, 0, True),)),
        ),
        Q.finite: (
            (True, ((Q.finite, 0, True),)),
        ),
        Q.integer: (
            (True, ((Q.zero, 0, True),)),
        ),
        Q.positive: (
            (True, ((Q.real, 0, True),)),
        ),
        Q.positive_infinite: (
            (True, ((Q.positive_infinite, 0, True),)),
        ),
        Q.real: (
            (True, ((Q.real, 0, True),)),
        ),
        Q.transcendental: (
            (True, ((Q.algebraic, 0, True), (Q.zero, 0, False))),
        ),
        Q.zero: (
            (True, ((Q.negative_infinite, 0, True),)),
            (False, ((Q.finite, 0, True),)),
        ),
    },
    (factorial, 1): {
        Q.positive: (
            (True, ((Q.integer, 0, True), (Q.nonnegative, 0, True))),
        ),
    },
    (im, 1): {
        Q.even: (
            (True, ((Q.real, 0, True),)),
        ),
        Q.real: (
            (True, ((Q.complex, 0, True),)),
        ),
    },
    (log, 1): {
        Q.algebraic: (
            (False, ((Q.algebraic, 0, True), (Q.eq, (0, Integer(1)), False))),
        ),
        Q.complex: (
            (True, ((Q.complex, 0, True), (Q.zero, 0, False))),
        ),
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
        Q.real: (
            (True, ((Q.positive, 0, True),)),
            (False, ((Q.positive, 0, False),)),
        ),
    },
    (re, 1): {
        Q.even: (
            (True, ((Q.even, 0, True),)),
            (False, ((Q.even, 0, False), (Q.real, 0, True))),
        ),
        Q.extended_real: (
            (True, ((Q.extended_real, 0, True),)),
        ),
        Q.odd: (
            (True, ((Q.odd, 0, True),)),
        ),
        Q.real: (
            (True, ((Q.complex, 0, True),)),
        ),
    },
    (sign, 1): {
        Q.finite: (
            (True, ()),
        ),
    },
    (sin, 1): {
        Q.complex: (
            (True, ((Q.complex, 0, True),)),
        ),
        Q.finite: (
            (True, ((Q.finite, 0, True),)),
        ),
        Q.real: (
            (True, ((Q.real, 0, True),)),
        ),
        Q.transcendental: (
            (True, ((Q.algebraic, 0, True), (Q.zero, 0, False))),
        ),
        Q.zero: (
            (True, ((Q.zero, 0, True),)),
        ),
    },
    (tan, 1): {
        Q.transcendental: (
            (True, ((Q.algebraic, 0, True), (Q.zero, 0, False))),
        ),
        Q.zero: (
            (True, ((Q.zero, 0, True),)),
        ),
    },
}
