"""
Do NOT manually edit this file.
Instead, run ./bin/ask_update.py.
"""

from sympy.assumptions.ask import Q
from sympy.core.add import Add
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

# A literal ``(predicate, slot, value)`` says that the predicate has the truth
# value ``value`` for an expression: the argument number ``slot`` of the
# expression which a rule is about, or that expression itself for the slot
# ``EXPR``. A sum, a product and a block diagonal matrix are read as their
# first argument and the rest. A literal ``(Q.eq, (a, b), value)`` is about
# two arguments: ``a`` and ``b`` are slots, or one of them is a number.
EXPR = -1

# For each class and number of arguments, the clauses which hold for every
# instance. At least one literal of a clause is true. Above each group of
# clauses is the rule which they come from. The clauses under ``None`` are for
# any number of arguments.
SAT_RULES = {
    (Abs, 1): (
        # Implies(Q.even(x), Q.even(f(x)))
        ((Q.even, 0, False), (Q.even, EXPR, True)),
        # Implies(Q.odd(x), Q.odd(f(x)))
        ((Q.odd, 0, False), (Q.odd, EXPR, True)),
        # Implies(Q.real(x) & ~Q.even(x), ~Q.even(f(x)))
        ((Q.even, 0, True), (Q.real, 0, False), (Q.even, EXPR, False)),
        # Q.extended_nonnegative(f(x))
        ((Q.extended_nonnegative, EXPR, True),),
        # Implies(Q.finite(x), Q.nonnegative(f(x)))
        ((Q.finite, 0, False), (Q.nonnegative, EXPR, True)),
        # Equivalent(Q.zero(x), Q.zero(f(x)))
        ((Q.zero, 0, False), (Q.zero, EXPR, True)),
        ((Q.zero, 0, True), (Q.zero, EXPR, False)),
        # Implies(Q.finite(x) & ~Q.zero(x), Q.positive(f(x)))
        ((Q.finite, 0, False), (Q.zero, 0, True), (Q.positive, EXPR, True)),
        # Implies(Q.integer(x), Q.integer(f(x)))
        ((Q.integer, 0, False), (Q.integer, EXPR, True)),
        # Implies(Q.rational(x), Q.rational(f(x)))
        ((Q.rational, 0, False), (Q.rational, EXPR, True)),
        # Implies(Q.algebraic(x), Q.algebraic(f(x)))
        ((Q.algebraic, 0, False), (Q.algebraic, EXPR, True)),
        # Implies(Q.complex(x), Q.real(f(x)))
        ((Q.complex, 0, False), (Q.real, EXPR, True)),
    ),
    (Add, 2): (
        # Implies(Q.finite(x) & Q.finite(y), Q.finite(f(x, y)))
        ((Q.finite, 0, False), (Q.finite, 1, False), (Q.finite, EXPR, True)),
        # Implies(Q.finite(y) & ~Q.finite(x), Q.infinite(f(x, y)))
        ((Q.finite, 0, True), (Q.finite, 1, False), (Q.infinite, EXPR, True)),
        # Implies(Q.finite(x) & Q.infinite(y), Q.infinite(f(x, y)))
        ((Q.finite, 0, False), (Q.infinite, 1, False), (Q.infinite, EXPR, True)),
        # Implies(Q.extended_real(y) & Q.positive_infinite(x) & ~Q.negative_infinite(y), Q.positive_infinite(f(x, y)))
        ((Q.positive_infinite, 0, False), (Q.extended_real, 1, False), (Q.negative_infinite, 1, True), (Q.positive_infinite, EXPR, True)),
        # Implies(Q.extended_real(x) & Q.positive_infinite(y) & ~Q.negative_infinite(x), Q.positive_infinite(f(x, y)))
        ((Q.extended_real, 0, False), (Q.negative_infinite, 0, True), (Q.positive_infinite, 1, False), (Q.positive_infinite, EXPR, True)),
        # Implies(Q.extended_real(y) & Q.negative_infinite(x) & ~Q.positive_infinite(y), Q.negative_infinite(f(x, y)))
        ((Q.negative_infinite, 0, False), (Q.extended_real, 1, False), (Q.positive_infinite, 1, True), (Q.negative_infinite, EXPR, True)),
        # Implies(Q.extended_real(x) & Q.negative_infinite(y) & ~Q.positive_infinite(x), Q.negative_infinite(f(x, y)))
        ((Q.extended_real, 0, False), (Q.positive_infinite, 0, True), (Q.negative_infinite, 1, False), (Q.negative_infinite, EXPR, True)),
        # Implies(Q.extended_real(x) & Q.extended_real(y) & ~Q.positive_infinite(x) & ~Q.positive_infinite(y), ~Q.positive_infinite(f(x, y)))
        ((Q.extended_real, 0, False), (Q.positive_infinite, 0, True), (Q.extended_real, 1, False), (Q.positive_infinite, 1, True), (Q.positive_infinite, EXPR, False)),
        # Implies(Q.extended_real(x) & Q.extended_real(y) & ~Q.negative_infinite(x) & ~Q.negative_infinite(y), ~Q.negative_infinite(f(x, y)))
        ((Q.extended_real, 0, False), (Q.negative_infinite, 0, True), (Q.extended_real, 1, False), (Q.negative_infinite, 1, True), (Q.negative_infinite, EXPR, False)),
        # Implies(Q.even(x) & Q.even(y), Q.even(f(x, y)))
        ((Q.even, 0, False), (Q.even, 1, False), (Q.even, EXPR, True)),
        # Implies(Q.odd(x) & Q.odd(y), Q.even(f(x, y)))
        ((Q.odd, 0, False), (Q.odd, 1, False), (Q.even, EXPR, True)),
        # Implies(Q.even(x) & Q.odd(y), Q.odd(f(x, y)))
        ((Q.even, 0, False), (Q.odd, 1, False), (Q.odd, EXPR, True)),
        # Implies(Q.even(y) & Q.odd(x), Q.odd(f(x, y)))
        ((Q.odd, 0, False), (Q.even, 1, False), (Q.odd, EXPR, True)),
        # Implies(Q.positive(x) & Q.positive(y), Q.positive(f(x, y)))
        ((Q.positive, 0, False), (Q.positive, 1, False), (Q.positive, EXPR, True)),
        # Implies(Q.negative(x) & Q.negative(y), Q.negative(f(x, y)))
        ((Q.negative, 0, False), (Q.negative, 1, False), (Q.negative, EXPR, True)),
        # Implies(Q.nonnegative(y) & Q.positive(x), Q.positive(f(x, y)))
        ((Q.positive, 0, False), (Q.nonnegative, 1, False), (Q.positive, EXPR, True)),
        # Implies(Q.nonnegative(x) & Q.positive(y), Q.positive(f(x, y)))
        ((Q.nonnegative, 0, False), (Q.positive, 1, False), (Q.positive, EXPR, True)),
        # Implies(Q.negative(x) & Q.nonpositive(y), Q.negative(f(x, y)))
        ((Q.negative, 0, False), (Q.nonpositive, 1, False), (Q.negative, EXPR, True)),
        # Implies(Q.negative(y) & Q.nonpositive(x), Q.negative(f(x, y)))
        ((Q.nonpositive, 0, False), (Q.negative, 1, False), (Q.negative, EXPR, True)),
        # Implies(Q.imaginary(y) & Q.real(x), ~Q.extended_real(f(x, y)))
        ((Q.real, 0, False), (Q.imaginary, 1, False), (Q.extended_real, EXPR, False)),
        # Implies(Q.imaginary(x) & Q.real(y), ~Q.extended_real(f(x, y)))
        ((Q.imaginary, 0, False), (Q.real, 1, False), (Q.extended_real, EXPR, False)),
        # Implies(Q.nonnegative(x) & Q.nonnegative(y), Q.nonnegative(f(x, y)))
        ((Q.nonnegative, 0, False), (Q.nonnegative, 1, False), (Q.nonnegative, EXPR, True)),
        # Implies(Q.nonpositive(x) & Q.nonpositive(y), Q.nonpositive(f(x, y)))
        ((Q.nonpositive, 0, False), (Q.nonpositive, 1, False), (Q.nonpositive, EXPR, True)),
        # Implies(Q.extended_positive(x) & Q.extended_positive(y), Q.extended_positive(f(x, y)))
        ((Q.extended_positive, 0, False), (Q.extended_positive, 1, False), (Q.extended_positive, EXPR, True)),
        # Implies(Q.extended_negative(x) & Q.extended_negative(y), Q.extended_negative(f(x, y)))
        ((Q.extended_negative, 0, False), (Q.extended_negative, 1, False), (Q.extended_negative, EXPR, True)),
        # Implies(Q.extended_nonnegative(x) & Q.extended_nonnegative(y), Q.extended_nonnegative(f(x, y)))
        ((Q.extended_nonnegative, 0, False), (Q.extended_nonnegative, 1, False), (Q.extended_nonnegative, EXPR, True)),
        # Implies(Q.extended_nonpositive(x) & Q.extended_nonpositive(y), Q.extended_nonpositive(f(x, y)))
        ((Q.extended_nonpositive, 0, False), (Q.extended_nonpositive, 1, False), (Q.extended_nonpositive, EXPR, True)),
        # Implies(Q.real(x) & Q.real(y), Q.real(f(x, y)))
        ((Q.real, 0, False), (Q.real, 1, False), (Q.real, EXPR, True)),
        # Implies(Q.rational(x) & Q.rational(y), Q.rational(f(x, y)))
        ((Q.rational, 0, False), (Q.rational, 1, False), (Q.rational, EXPR, True)),
        # Implies(Q.integer(x) & Q.integer(y), Q.integer(f(x, y)))
        ((Q.integer, 0, False), (Q.integer, 1, False), (Q.integer, EXPR, True)),
        # Implies(Q.algebraic(x) & Q.algebraic(y), Q.algebraic(f(x, y)))
        ((Q.algebraic, 0, False), (Q.algebraic, 1, False), (Q.algebraic, EXPR, True)),
        # Implies(Q.complex(x) & Q.complex(y), Q.complex(f(x, y)))
        ((Q.complex, 0, False), (Q.complex, 1, False), (Q.complex, EXPR, True)),
        # Implies(Q.hermitian(x) & Q.hermitian(y), Q.hermitian(f(x, y)))
        ((Q.hermitian, 0, False), (Q.hermitian, 1, False), (Q.hermitian, EXPR, True)),
        # Implies(Q.antihermitian(x) & Q.antihermitian(y), Q.antihermitian(f(x, y)))
        ((Q.antihermitian, 0, False), (Q.antihermitian, 1, False), (Q.antihermitian, EXPR, True)),
        # Implies(Q.integer(x) & ~Q.integer(y), ~Q.integer(f(x, y)))
        ((Q.integer, 0, False), (Q.integer, 1, True), (Q.integer, EXPR, False)),
        # Implies(Q.integer(y) & ~Q.integer(x), ~Q.integer(f(x, y)))
        ((Q.integer, 0, True), (Q.integer, 1, False), (Q.integer, EXPR, False)),
        # Implies(Q.rational(x) & ~Q.rational(y), ~Q.rational(f(x, y)))
        ((Q.rational, 0, False), (Q.rational, 1, True), (Q.rational, EXPR, False)),
        # Implies(Q.rational(y) & ~Q.rational(x), ~Q.rational(f(x, y)))
        ((Q.rational, 0, True), (Q.rational, 1, False), (Q.rational, EXPR, False)),
        # Implies(Q.irrational(y) & Q.rational(x), Q.irrational(f(x, y)))
        ((Q.rational, 0, False), (Q.irrational, 1, False), (Q.irrational, EXPR, True)),
        # Implies(Q.irrational(x) & Q.rational(y), Q.irrational(f(x, y)))
        ((Q.irrational, 0, False), (Q.rational, 1, False), (Q.irrational, EXPR, True)),
        # Implies(Q.real(x) & ~Q.real(y), ~Q.real(f(x, y)))
        ((Q.real, 0, False), (Q.real, 1, True), (Q.real, EXPR, False)),
        # Implies(Q.real(y) & ~Q.real(x), ~Q.real(f(x, y)))
        ((Q.real, 0, True), (Q.real, 1, False), (Q.real, EXPR, False)),
        # Implies(Q.real(x) & ~Q.extended_real(y), ~Q.extended_real(f(x, y)))
        ((Q.real, 0, False), (Q.extended_real, 1, True), (Q.extended_real, EXPR, False)),
        # Implies(Q.real(y) & ~Q.extended_real(x), ~Q.extended_real(f(x, y)))
        ((Q.extended_real, 0, True), (Q.real, 1, False), (Q.extended_real, EXPR, False)),
        # Implies(Q.extended_real(y) & Q.real(x), Q.extended_real(f(x, y)))
        ((Q.real, 0, False), (Q.extended_real, 1, False), (Q.extended_real, EXPR, True)),
        # Implies(Q.extended_real(x) & Q.real(y), Q.extended_real(f(x, y)))
        ((Q.extended_real, 0, False), (Q.real, 1, False), (Q.extended_real, EXPR, True)),
        # Implies(Q.extended_positive(x) & Q.extended_positive(y), Q.extended_real(f(x, y)))
        ((Q.extended_positive, 0, False), (Q.extended_positive, 1, False), (Q.extended_real, EXPR, True)),
        # Implies(Q.extended_negative(x) & Q.extended_negative(y), Q.extended_real(f(x, y)))
        ((Q.extended_negative, 0, False), (Q.extended_negative, 1, False), (Q.extended_real, EXPR, True)),
        # Implies(Q.complex(x) & ~Q.complex(y), ~Q.complex(f(x, y)))
        ((Q.complex, 0, False), (Q.complex, 1, True), (Q.complex, EXPR, False)),
        # Implies(Q.complex(y) & ~Q.complex(x), ~Q.complex(f(x, y)))
        ((Q.complex, 0, True), (Q.complex, 1, False), (Q.complex, EXPR, False)),
        # Implies(Q.algebraic(x) & ~Q.algebraic(y), ~Q.algebraic(f(x, y)))
        ((Q.algebraic, 0, False), (Q.algebraic, 1, True), (Q.algebraic, EXPR, False)),
        # Implies(Q.algebraic(y) & ~Q.algebraic(x), ~Q.algebraic(f(x, y)))
        ((Q.algebraic, 0, True), (Q.algebraic, 1, False), (Q.algebraic, EXPR, False)),
        # Implies(Q.algebraic(x) & Q.transcendental(y), Q.transcendental(f(x, y)))
        ((Q.algebraic, 0, False), (Q.transcendental, 1, False), (Q.transcendental, EXPR, True)),
        # Implies(Q.algebraic(y) & Q.transcendental(x), Q.transcendental(f(x, y)))
        ((Q.transcendental, 0, False), (Q.algebraic, 1, False), (Q.transcendental, EXPR, True)),
        # Implies(Q.hermitian(x) & ~Q.hermitian(y), ~Q.hermitian(f(x, y)))
        ((Q.hermitian, 0, False), (Q.hermitian, 1, True), (Q.hermitian, EXPR, False)),
        # Implies(Q.hermitian(y) & ~Q.hermitian(x), ~Q.hermitian(f(x, y)))
        ((Q.hermitian, 0, True), (Q.hermitian, 1, False), (Q.hermitian, EXPR, False)),
        # Implies(Q.antihermitian(x) & ~Q.antihermitian(y), ~Q.antihermitian(f(x, y)))
        ((Q.antihermitian, 0, False), (Q.antihermitian, 1, True), (Q.antihermitian, EXPR, False)),
        # Implies(Q.antihermitian(y) & ~Q.antihermitian(x), ~Q.antihermitian(f(x, y)))
        ((Q.antihermitian, 0, True), (Q.antihermitian, 1, False), (Q.antihermitian, EXPR, False)),
        # Implies(Q.imaginary(x) & Q.imaginary(y) & ~Q.zero(f(x, y)), Q.imaginary(f(x, y)))
        ((Q.imaginary, 0, False), (Q.imaginary, 1, False), (Q.imaginary, EXPR, True), (Q.zero, EXPR, True)),
        # Implies(Q.imaginary(y) & Q.real(x) & ~Q.zero(x), ~Q.imaginary(f(x, y)))
        ((Q.real, 0, False), (Q.zero, 0, True), (Q.imaginary, 1, False), (Q.imaginary, EXPR, False)),
        # Implies(Q.imaginary(x) & Q.real(y) & ~Q.zero(y), ~Q.imaginary(f(x, y)))
        ((Q.imaginary, 0, False), (Q.real, 1, False), (Q.zero, 1, True), (Q.imaginary, EXPR, False)),
    ),
    (BlockDiagMatrix, 1): (
        # Equivalent(Q.invertible(x), Q.invertible(f(x)))
        ((Q.invertible, 0, False), (Q.invertible, EXPR, True)),
        ((Q.invertible, 0, True), (Q.invertible, EXPR, False)),
        # Equivalent(Q.integer_elements(x), Q.integer_elements(f(x)))
        ((Q.integer_elements, 0, False), (Q.integer_elements, EXPR, True)),
        ((Q.integer_elements, 0, True), (Q.integer_elements, EXPR, False)),
        # Equivalent(Q.real_elements(x), Q.real_elements(f(x)))
        ((Q.real_elements, 0, False), (Q.real_elements, EXPR, True)),
        ((Q.real_elements, 0, True), (Q.real_elements, EXPR, False)),
        # Equivalent(Q.complex_elements(x), Q.complex_elements(f(x)))
        ((Q.complex_elements, 0, False), (Q.complex_elements, EXPR, True)),
        ((Q.complex_elements, 0, True), (Q.complex_elements, EXPR, False)),
    ),
    (BlockDiagMatrix, 2): (
        # Equivalent(Q.invertible(f(x, y)), Q.invertible(x) & Q.invertible(y))
        ((Q.invertible, 0, False), (Q.invertible, 1, False), (Q.invertible, EXPR, True)),
        ((Q.invertible, 0, True), (Q.invertible, EXPR, False)),
        ((Q.invertible, 1, True), (Q.invertible, EXPR, False)),
        # Equivalent(Q.integer_elements(f(x, y)), Q.integer_elements(x) & Q.integer_elements(y))
        ((Q.integer_elements, 0, False), (Q.integer_elements, 1, False), (Q.integer_elements, EXPR, True)),
        ((Q.integer_elements, 0, True), (Q.integer_elements, EXPR, False)),
        ((Q.integer_elements, 1, True), (Q.integer_elements, EXPR, False)),
        # Equivalent(Q.real_elements(f(x, y)), Q.real_elements(x) & Q.real_elements(y))
        ((Q.real_elements, 0, False), (Q.real_elements, 1, False), (Q.real_elements, EXPR, True)),
        ((Q.real_elements, 0, True), (Q.real_elements, EXPR, False)),
        ((Q.real_elements, 1, True), (Q.real_elements, EXPR, False)),
        # Equivalent(Q.complex_elements(f(x, y)), Q.complex_elements(x) & Q.complex_elements(y))
        ((Q.complex_elements, 0, False), (Q.complex_elements, 1, False), (Q.complex_elements, EXPR, True)),
        ((Q.complex_elements, 0, True), (Q.complex_elements, EXPR, False)),
        ((Q.complex_elements, 1, True), (Q.complex_elements, EXPR, False)),
    ),
    (Determinant, 1): (
        # Implies(Q.integer_elements(x), Q.integer_elements(f(x)))
        ((Q.integer_elements, 0, False), (Q.integer_elements, EXPR, True)),
        # Implies(Q.real_elements(x), Q.real_elements(f(x)))
        ((Q.real_elements, 0, False), (Q.real_elements, EXPR, True)),
        # Implies(Q.complex_elements(x), Q.complex_elements(f(x)))
        ((Q.complex_elements, 0, False), (Q.complex_elements, EXPR, True)),
        # Implies(Q.positive_definite(x), Q.positive(f(x)))
        ((Q.positive_definite, 0, False), (Q.positive, EXPR, True)),
        # Implies(Q.integer_elements(x), Q.integer(f(x)))
        ((Q.integer_elements, 0, False), (Q.integer, EXPR, True)),
        # Implies(Q.real_elements(x), Q.real(f(x)))
        ((Q.real_elements, 0, False), (Q.real, EXPR, True)),
        # Implies(Q.complex_elements(x), Q.complex(f(x)))
        ((Q.complex_elements, 0, False), (Q.complex, EXPR, True)),
    ),
    (HadamardProduct, 2): (
        # Implies(Q.integer_elements(x) & Q.integer_elements(y), Q.integer_elements(f(x, y)))
        ((Q.integer_elements, 0, False), (Q.integer_elements, 1, False), (Q.integer_elements, EXPR, True)),
        # Implies(Q.real_elements(x) & Q.real_elements(y), Q.real_elements(f(x, y)))
        ((Q.real_elements, 0, False), (Q.real_elements, 1, False), (Q.real_elements, EXPR, True)),
        # Implies(Q.complex_elements(x) & Q.complex_elements(y), Q.complex_elements(f(x, y)))
        ((Q.complex_elements, 0, False), (Q.complex_elements, 1, False), (Q.complex_elements, EXPR, True)),
    ),
    (Inverse, 2): (
        # Q.invertible(f(base, exponent))
        ((Q.invertible, EXPR, True),),
        # Equivalent(Q.symmetric(base), Q.symmetric(f(base, exponent)))
        ((Q.symmetric, 0, False), (Q.symmetric, EXPR, True)),
        ((Q.symmetric, 0, True), (Q.symmetric, EXPR, False)),
        # Equivalent(Q.orthogonal(base), Q.orthogonal(f(base, exponent)))
        ((Q.orthogonal, 0, False), (Q.orthogonal, EXPR, True)),
        ((Q.orthogonal, 0, True), (Q.orthogonal, EXPR, False)),
        # Equivalent(Q.unitary(base), Q.unitary(f(base, exponent)))
        ((Q.unitary, 0, False), (Q.unitary, EXPR, True)),
        ((Q.unitary, 0, True), (Q.unitary, EXPR, False)),
        # Equivalent(Q.positive_definite(base), Q.positive_definite(f(base, exponent)))
        ((Q.positive_definite, 0, False), (Q.positive_definite, EXPR, True)),
        ((Q.positive_definite, 0, True), (Q.positive_definite, EXPR, False)),
        # Equivalent(Q.upper_triangular(base), Q.upper_triangular(f(base, exponent)))
        ((Q.upper_triangular, 0, False), (Q.upper_triangular, EXPR, True)),
        ((Q.upper_triangular, 0, True), (Q.upper_triangular, EXPR, False)),
        # Equivalent(Q.lower_triangular(base), Q.lower_triangular(f(base, exponent)))
        ((Q.lower_triangular, 0, False), (Q.lower_triangular, EXPR, True)),
        ((Q.lower_triangular, 0, True), (Q.lower_triangular, EXPR, False)),
        # Equivalent(Q.diagonal(base), Q.diagonal(f(base, exponent)))
        ((Q.diagonal, 0, False), (Q.diagonal, EXPR, True)),
        ((Q.diagonal, 0, True), (Q.diagonal, EXPR, False)),
        # Implies(Q.real_elements(base), Q.real_elements(f(base, exponent)))
        ((Q.real_elements, 0, False), (Q.real_elements, EXPR, True)),
        # Implies(Q.complex_elements(base), Q.complex_elements(f(base, exponent)))
        ((Q.complex_elements, 0, False), (Q.complex_elements, EXPR, True)),
    ),
    (MatAdd, 2): (
        # Implies(Q.symmetric(x) & Q.symmetric(y), Q.symmetric(f(x, y)))
        ((Q.symmetric, 0, False), (Q.symmetric, 1, False), (Q.symmetric, EXPR, True)),
        # Implies(Q.positive_definite(x) & Q.positive_definite(y), Q.positive_definite(f(x, y)))
        ((Q.positive_definite, 0, False), (Q.positive_definite, 1, False), (Q.positive_definite, EXPR, True)),
        # Implies(Q.upper_triangular(x) & Q.upper_triangular(y), Q.upper_triangular(f(x, y)))
        ((Q.upper_triangular, 0, False), (Q.upper_triangular, 1, False), (Q.upper_triangular, EXPR, True)),
        # Implies(Q.lower_triangular(x) & Q.lower_triangular(y), Q.lower_triangular(f(x, y)))
        ((Q.lower_triangular, 0, False), (Q.lower_triangular, 1, False), (Q.lower_triangular, EXPR, True)),
        # Implies(Q.diagonal(x) & Q.diagonal(y), Q.diagonal(f(x, y)))
        ((Q.diagonal, 0, False), (Q.diagonal, 1, False), (Q.diagonal, EXPR, True)),
        # Implies(Q.symmetric(x) & ~Q.symmetric(y), ~Q.symmetric(f(x, y)))
        ((Q.symmetric, 0, False), (Q.symmetric, 1, True), (Q.symmetric, EXPR, False)),
        # Implies(Q.symmetric(y) & ~Q.symmetric(x), ~Q.symmetric(f(x, y)))
        ((Q.symmetric, 0, True), (Q.symmetric, 1, False), (Q.symmetric, EXPR, False)),
        # Implies(Q.upper_triangular(x) & ~Q.upper_triangular(y), ~Q.upper_triangular(f(x, y)))
        ((Q.upper_triangular, 0, False), (Q.upper_triangular, 1, True), (Q.upper_triangular, EXPR, False)),
        # Implies(Q.upper_triangular(y) & ~Q.upper_triangular(x), ~Q.upper_triangular(f(x, y)))
        ((Q.upper_triangular, 0, True), (Q.upper_triangular, 1, False), (Q.upper_triangular, EXPR, False)),
        # Implies(Q.lower_triangular(x) & ~Q.lower_triangular(y), ~Q.lower_triangular(f(x, y)))
        ((Q.lower_triangular, 0, False), (Q.lower_triangular, 1, True), (Q.lower_triangular, EXPR, False)),
        # Implies(Q.lower_triangular(y) & ~Q.lower_triangular(x), ~Q.lower_triangular(f(x, y)))
        ((Q.lower_triangular, 0, True), (Q.lower_triangular, 1, False), (Q.lower_triangular, EXPR, False)),
        # Implies(Q.diagonal(x) & ~Q.diagonal(y), ~Q.diagonal(f(x, y)))
        ((Q.diagonal, 0, False), (Q.diagonal, 1, True), (Q.diagonal, EXPR, False)),
        # Implies(Q.diagonal(y) & ~Q.diagonal(x), ~Q.diagonal(f(x, y)))
        ((Q.diagonal, 0, True), (Q.diagonal, 1, False), (Q.diagonal, EXPR, False)),
        # Implies(Q.integer_elements(x) & Q.integer_elements(y), Q.integer_elements(f(x, y)))
        ((Q.integer_elements, 0, False), (Q.integer_elements, 1, False), (Q.integer_elements, EXPR, True)),
        # Implies(Q.real_elements(x) & Q.real_elements(y), Q.real_elements(f(x, y)))
        ((Q.real_elements, 0, False), (Q.real_elements, 1, False), (Q.real_elements, EXPR, True)),
        # Implies(Q.complex_elements(x) & Q.complex_elements(y), Q.complex_elements(f(x, y)))
        ((Q.complex_elements, 0, False), (Q.complex_elements, 1, False), (Q.complex_elements, EXPR, True)),
    ),
    (MatMul, 2): (
        # Implies(Q.square(x) & Q.square(y), Equivalent(Q.invertible(f(x, y)), Q.invertible(x) & Q.invertible(y)))
        ((Q.invertible, 0, False), (Q.square, 0, False), (Q.invertible, 1, False), (Q.square, 1, False), (Q.invertible, EXPR, True)),
        ((Q.invertible, 0, True), (Q.square, 0, False), (Q.square, 1, False), (Q.invertible, EXPR, False)),
        ((Q.square, 0, False), (Q.invertible, 1, True), (Q.square, 1, False), (Q.invertible, EXPR, False)),
        # Implies(Q.complex(x) & Q.invertible(y) & ~Q.zero(x), Q.invertible(f(x, y)))
        ((Q.complex, 0, False), (Q.zero, 0, True), (Q.invertible, 1, False), (Q.invertible, EXPR, True)),
        # Implies(Q.fullrank(x) & Q.fullrank(y) & Q.square(x), Q.fullrank(f(x, y)))
        ((Q.fullrank, 0, False), (Q.square, 0, False), (Q.fullrank, 1, False), (Q.fullrank, EXPR, True)),
        # Implies(Q.fullrank(x) & Q.fullrank(y) & Q.square(y), Q.fullrank(f(x, y)))
        ((Q.fullrank, 0, False), (Q.fullrank, 1, False), (Q.square, 1, False), (Q.fullrank, EXPR, True)),
        # Implies(Q.orthogonal(x) & Q.orthogonal(y), Q.orthogonal(f(x, y)))
        ((Q.orthogonal, 0, False), (Q.orthogonal, 1, False), (Q.orthogonal, EXPR, True)),
        # Implies(Q.unitary(x) & Q.unitary(y), Q.unitary(f(x, y)))
        ((Q.unitary, 0, False), (Q.unitary, 1, False), (Q.unitary, EXPR, True)),
        # Implies(Q.upper_triangular(x) & Q.upper_triangular(y), Q.upper_triangular(f(x, y)))
        ((Q.upper_triangular, 0, False), (Q.upper_triangular, 1, False), (Q.upper_triangular, EXPR, True)),
        # Implies(Q.lower_triangular(x) & Q.lower_triangular(y), Q.lower_triangular(f(x, y)))
        ((Q.lower_triangular, 0, False), (Q.lower_triangular, 1, False), (Q.lower_triangular, EXPR, True)),
        # Implies(Q.diagonal(x) & Q.diagonal(y), Q.diagonal(f(x, y)))
        ((Q.diagonal, 0, False), (Q.diagonal, 1, False), (Q.diagonal, EXPR, True)),
        # Implies(Q.complex(x) & Q.symmetric(y), Q.symmetric(f(x, y)))
        ((Q.complex, 0, False), (Q.symmetric, 1, False), (Q.symmetric, EXPR, True)),
        # Implies(Q.complex(x) & Q.upper_triangular(y), Q.upper_triangular(f(x, y)))
        ((Q.complex, 0, False), (Q.upper_triangular, 1, False), (Q.upper_triangular, EXPR, True)),
        # Implies(Q.complex(x) & Q.lower_triangular(y), Q.lower_triangular(f(x, y)))
        ((Q.complex, 0, False), (Q.lower_triangular, 1, False), (Q.lower_triangular, EXPR, True)),
        # Implies(Q.complex(x) & Q.diagonal(y), Q.diagonal(f(x, y)))
        ((Q.complex, 0, False), (Q.diagonal, 1, False), (Q.diagonal, EXPR, True)),
        # Implies(Q.positive_definite(y) & Q.positive(x), Q.positive_definite(f(x, y)))
        ((Q.positive, 0, False), (Q.positive_definite, 1, False), (Q.positive_definite, EXPR, True)),
        # Implies(Q.integer_elements(x) & Q.integer_elements(y), Q.integer_elements(f(x, y)))
        ((Q.integer_elements, 0, False), (Q.integer_elements, 1, False), (Q.integer_elements, EXPR, True)),
        # Implies(Q.real_elements(x) & Q.real_elements(y), Q.real_elements(f(x, y)))
        ((Q.real_elements, 0, False), (Q.real_elements, 1, False), (Q.real_elements, EXPR, True)),
        # Implies(Q.complex_elements(x) & Q.complex_elements(y), Q.complex_elements(f(x, y)))
        ((Q.complex_elements, 0, False), (Q.complex_elements, 1, False), (Q.complex_elements, EXPR, True)),
        # Implies(Q.integer_elements(y) & Q.integer(x), Q.integer_elements(f(x, y)))
        ((Q.integer, 0, False), (Q.integer_elements, 1, False), (Q.integer_elements, EXPR, True)),
        # Implies(Q.real_elements(y) & Q.real(x), Q.real_elements(f(x, y)))
        ((Q.real, 0, False), (Q.real_elements, 1, False), (Q.real_elements, EXPR, True)),
        # Implies(Q.complex_elements(y) & Q.complex(x), Q.complex_elements(f(x, y)))
        ((Q.complex, 0, False), (Q.complex_elements, 1, False), (Q.complex_elements, EXPR, True)),
    ),
    (MatPow, 2): (
        # Implies(Q.integer(exponent) & Q.invertible(base), Q.invertible(f(base, exponent)))
        ((Q.invertible, 0, False), (Q.integer, 1, False), (Q.invertible, EXPR, True)),
        # Implies(Q.fullrank(base) & Q.integer(exponent), Q.fullrank(f(base, exponent)))
        ((Q.fullrank, 0, False), (Q.integer, 1, False), (Q.fullrank, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.positive(exponent) & ~Q.invertible(base), ~Q.invertible(f(base, exponent)))
        ((Q.invertible, 0, True), (Q.integer, 1, False), (Q.positive, 1, False), (Q.invertible, EXPR, False)),
        # Implies(Q.integer(exponent) & Q.orthogonal(base), Q.orthogonal(f(base, exponent)))
        ((Q.orthogonal, 0, False), (Q.integer, 1, False), (Q.orthogonal, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.unitary(base), Q.unitary(f(base, exponent)))
        ((Q.unitary, 0, False), (Q.integer, 1, False), (Q.unitary, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.positive_definite(base), Q.positive_definite(f(base, exponent)))
        ((Q.positive_definite, 0, False), (Q.integer, 1, False), (Q.positive_definite, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.symmetric(base) & (Q.invertible(base) | ~Q.negative(exponent)), Q.symmetric(f(base, exponent)))
        ((Q.invertible, 0, False), (Q.symmetric, 0, False), (Q.integer, 1, False), (Q.symmetric, EXPR, True)),
        ((Q.symmetric, 0, False), (Q.integer, 1, False), (Q.negative, 1, True), (Q.symmetric, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.upper_triangular(base) & (Q.invertible(base) | ~Q.negative(exponent)), Q.upper_triangular(f(base, exponent)))
        ((Q.invertible, 0, False), (Q.upper_triangular, 0, False), (Q.integer, 1, False), (Q.upper_triangular, EXPR, True)),
        ((Q.upper_triangular, 0, False), (Q.integer, 1, False), (Q.negative, 1, True), (Q.upper_triangular, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.lower_triangular(base) & (Q.invertible(base) | ~Q.negative(exponent)), Q.lower_triangular(f(base, exponent)))
        ((Q.invertible, 0, False), (Q.lower_triangular, 0, False), (Q.integer, 1, False), (Q.lower_triangular, EXPR, True)),
        ((Q.lower_triangular, 0, False), (Q.integer, 1, False), (Q.negative, 1, True), (Q.lower_triangular, EXPR, True)),
        # Implies(Q.diagonal(base) & Q.integer(exponent) & (Q.invertible(base) | ~Q.negative(exponent)), Q.diagonal(f(base, exponent)))
        ((Q.diagonal, 0, False), (Q.invertible, 0, False), (Q.integer, 1, False), (Q.diagonal, EXPR, True)),
        ((Q.diagonal, 0, False), (Q.integer, 1, False), (Q.negative, 1, True), (Q.diagonal, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.real_elements(base) & (Q.invertible(base) | ~Q.negative(exponent)), Q.real_elements(f(base, exponent)))
        ((Q.invertible, 0, False), (Q.real_elements, 0, False), (Q.integer, 1, False), (Q.real_elements, EXPR, True)),
        ((Q.real_elements, 0, False), (Q.integer, 1, False), (Q.negative, 1, True), (Q.real_elements, EXPR, True)),
        # Implies(Q.complex_elements(base) & Q.integer(exponent) & (Q.invertible(base) | ~Q.negative(exponent)), Q.complex_elements(f(base, exponent)))
        ((Q.complex_elements, 0, False), (Q.invertible, 0, False), (Q.integer, 1, False), (Q.complex_elements, EXPR, True)),
        ((Q.complex_elements, 0, False), (Q.integer, 1, False), (Q.negative, 1, True), (Q.complex_elements, EXPR, True)),
        # Implies(Q.integer_elements(base) & Q.integer(exponent) & ~Q.negative(exponent), Q.integer_elements(f(base, exponent)))
        ((Q.integer_elements, 0, False), (Q.integer, 1, False), (Q.negative, 1, True), (Q.integer_elements, EXPR, True)),
    ),
    (MatrixElement, 3): (
        # Implies(Q.positive_definite(x) & Q.eq(i, j), Q.positive(f(x, i, j)))
        ((Q.positive_definite, 0, False), (Q.eq, (1, 2), False), (Q.positive, EXPR, True)),
        # Implies(Q.integer_elements(x), Q.integer(f(x, i, j)))
        ((Q.integer_elements, 0, False), (Q.integer, EXPR, True)),
        # Implies(Q.real_elements(x), Q.real(f(x, i, j)))
        ((Q.real_elements, 0, False), (Q.real, EXPR, True)),
        # Implies(Q.complex_elements(x), Q.complex(f(x, i, j)))
        ((Q.complex_elements, 0, False), (Q.complex, EXPR, True)),
    ),
    (MatrixSlice, 3): (
        # Implies(Q.symmetric(x) & Q.eq(rows, columns), Q.symmetric(f(x, rows, columns)))
        ((Q.symmetric, 0, False), (Q.eq, (1, 2), False), (Q.symmetric, EXPR, True)),
        # Implies(Q.diagonal(x) & Q.eq(rows, columns), Q.diagonal(f(x, rows, columns)))
        ((Q.diagonal, 0, False), (Q.eq, (1, 2), False), (Q.diagonal, EXPR, True)),
        # Implies(Q.positive_definite(x) & Q.eq(rows, columns), Q.positive_definite(f(x, rows, columns)))
        ((Q.positive_definite, 0, False), (Q.eq, (1, 2), False), (Q.positive_definite, EXPR, True)),
        # Implies(Q.integer_elements(x), Q.integer_elements(f(x, rows, columns)))
        ((Q.integer_elements, 0, False), (Q.integer_elements, EXPR, True)),
        # Implies(Q.real_elements(x), Q.real_elements(f(x, rows, columns)))
        ((Q.real_elements, 0, False), (Q.real_elements, EXPR, True)),
        # Implies(Q.complex_elements(x), Q.complex_elements(f(x, rows, columns)))
        ((Q.complex_elements, 0, False), (Q.complex_elements, EXPR, True)),
    ),
    (Mul, 2): (
        # Implies(Q.finite(x) & Q.finite(y), Q.finite(f(x, y)))
        ((Q.finite, 0, False), (Q.finite, 1, False), (Q.finite, EXPR, True)),
        # Implies(Q.complex(f(x, y)), Q.finite(x) & Q.finite(y))
        ((Q.finite, 0, True), (Q.complex, EXPR, False)),
        ((Q.finite, 1, True), (Q.complex, EXPR, False)),
        # Implies(Q.infinite(y) & ~Q.finite(x), Q.infinite(f(x, y)))
        ((Q.finite, 0, True), (Q.infinite, 1, False), (Q.infinite, EXPR, True)),
        # Implies(Q.finite(y) & ~Q.finite(x) & ~Q.zero(y), Q.infinite(f(x, y)))
        ((Q.finite, 0, True), (Q.finite, 1, False), (Q.zero, 1, True), (Q.infinite, EXPR, True)),
        # Implies(Q.extended_nonzero(y) & ~Q.finite(x), Q.infinite(f(x, y)))
        ((Q.finite, 0, True), (Q.extended_nonzero, 1, False), (Q.infinite, EXPR, True)),
        # Implies(Q.infinite(y) & ~Q.zero(x), Q.infinite(f(x, y)))
        ((Q.zero, 0, True), (Q.infinite, 1, False), (Q.infinite, EXPR, True)),
        # Implies(Q.commutative(x) & Q.commutative(y), Q.commutative(f(x, y)))
        ((Q.commutative, 0, False), (Q.commutative, 1, False), (Q.commutative, EXPR, True)),
        # Implies(Q.even(x) & Q.integer(y), Q.even(f(x, y)))
        ((Q.even, 0, False), (Q.integer, 1, False), (Q.even, EXPR, True)),
        # Implies(Q.even(y) & Q.integer(x), Q.even(f(x, y)))
        ((Q.integer, 0, False), (Q.even, 1, False), (Q.even, EXPR, True)),
        # Implies(Q.odd(x) & Q.odd(y), Q.odd(f(x, y)))
        ((Q.odd, 0, False), (Q.odd, 1, False), (Q.odd, EXPR, True)),
        # Implies(Q.integer(x) & Q.integer(y), Equivalent(Q.even(f(x, y)), Q.even(x) | Q.even(y)))
        ((Q.even, 0, False), (Q.integer, 0, False), (Q.integer, 1, False), (Q.even, EXPR, True)),
        ((Q.even, 0, True), (Q.integer, 0, False), (Q.even, 1, True), (Q.integer, 1, False), (Q.even, EXPR, False)),
        ((Q.integer, 0, False), (Q.even, 1, False), (Q.integer, 1, False), (Q.even, EXPR, True)),
        # Implies(Q.composite(x) & Q.integer(y), ~Q.prime(f(x, y)))
        ((Q.composite, 0, False), (Q.integer, 1, False), (Q.prime, EXPR, False)),
        # Implies(Q.composite(y) & Q.integer(x), ~Q.prime(f(x, y)))
        ((Q.integer, 0, False), (Q.composite, 1, False), (Q.prime, EXPR, False)),
        # Implies(Q.prime(x) & Q.prime(y), Q.composite(f(x, y)))
        ((Q.prime, 0, False), (Q.prime, 1, False), (Q.composite, EXPR, True)),
        # Implies(Q.composite(y) & Q.prime(x), Q.composite(f(x, y)))
        ((Q.prime, 0, False), (Q.composite, 1, False), (Q.composite, EXPR, True)),
        # Implies(Q.composite(x) & Q.prime(y), Q.composite(f(x, y)))
        ((Q.composite, 0, False), (Q.prime, 1, False), (Q.composite, EXPR, True)),
        # Implies(Q.composite(x) & Q.composite(y), Q.composite(f(x, y)))
        ((Q.composite, 0, False), (Q.composite, 1, False), (Q.composite, EXPR, True)),
        # Implies(Q.positive(x) & Q.positive(y), Q.positive(f(x, y)))
        ((Q.positive, 0, False), (Q.positive, 1, False), (Q.positive, EXPR, True)),
        # Implies(Q.negative(x) & Q.negative(y), Q.positive(f(x, y)))
        ((Q.negative, 0, False), (Q.negative, 1, False), (Q.positive, EXPR, True)),
        # Implies(Q.negative(y) & Q.positive(x), Q.negative(f(x, y)))
        ((Q.positive, 0, False), (Q.negative, 1, False), (Q.negative, EXPR, True)),
        # Implies(Q.negative(x) & Q.positive(y), Q.negative(f(x, y)))
        ((Q.negative, 0, False), (Q.positive, 1, False), (Q.negative, EXPR, True)),
        # Implies(Q.nonzero(x) & Q.nonzero(y), Q.nonzero(f(x, y)))
        ((Q.nonzero, 0, False), (Q.nonzero, 1, False), (Q.nonzero, EXPR, True)),
        # Implies(Q.nonnegative(x) & Q.nonnegative(y), Q.nonnegative(f(x, y)))
        ((Q.nonnegative, 0, False), (Q.nonnegative, 1, False), (Q.nonnegative, EXPR, True)),
        # Implies(Q.nonpositive(x) & Q.nonpositive(y), Q.nonnegative(f(x, y)))
        ((Q.nonpositive, 0, False), (Q.nonpositive, 1, False), (Q.nonnegative, EXPR, True)),
        # Implies(Q.nonnegative(x) & Q.nonpositive(y), Q.nonpositive(f(x, y)))
        ((Q.nonnegative, 0, False), (Q.nonpositive, 1, False), (Q.nonpositive, EXPR, True)),
        # Implies(Q.nonnegative(y) & Q.nonpositive(x), Q.nonpositive(f(x, y)))
        ((Q.nonpositive, 0, False), (Q.nonnegative, 1, False), (Q.nonpositive, EXPR, True)),
        # Implies(Q.extended_positive(x) & Q.extended_positive(y), Q.extended_positive(f(x, y)))
        ((Q.extended_positive, 0, False), (Q.extended_positive, 1, False), (Q.extended_positive, EXPR, True)),
        # Implies(Q.extended_negative(x) & Q.extended_negative(y), Q.extended_positive(f(x, y)))
        ((Q.extended_negative, 0, False), (Q.extended_negative, 1, False), (Q.extended_positive, EXPR, True)),
        # Implies(Q.extended_negative(y) & Q.extended_positive(x), Q.extended_negative(f(x, y)))
        ((Q.extended_positive, 0, False), (Q.extended_negative, 1, False), (Q.extended_negative, EXPR, True)),
        # Implies(Q.extended_negative(x) & Q.extended_positive(y), Q.extended_negative(f(x, y)))
        ((Q.extended_negative, 0, False), (Q.extended_positive, 1, False), (Q.extended_negative, EXPR, True)),
        # Implies(Q.zero(f(x, y)), Q.zero(x) | Q.zero(y))
        ((Q.zero, 0, True), (Q.zero, 1, True), (Q.zero, EXPR, False)),
        # Implies(Q.finite(y) & Q.zero(x), Q.zero(f(x, y)))
        ((Q.zero, 0, False), (Q.finite, 1, False), (Q.zero, EXPR, True)),
        # Implies(Q.finite(x) & Q.zero(y), Q.zero(f(x, y)))
        ((Q.finite, 0, False), (Q.zero, 1, False), (Q.zero, EXPR, True)),
        # Implies(Q.zero(x), ~Q.extended_nonzero(f(x, y)))
        ((Q.zero, 0, False), (Q.extended_nonzero, EXPR, False)),
        # Implies(Q.zero(y), ~Q.extended_nonzero(f(x, y)))
        ((Q.zero, 1, False), (Q.extended_nonzero, EXPR, False)),
        # Implies(Q.real(x) & Q.real(y), Q.real(f(x, y)))
        ((Q.real, 0, False), (Q.real, 1, False), (Q.real, EXPR, True)),
        # Implies(Q.rational(x) & Q.rational(y), Q.rational(f(x, y)))
        ((Q.rational, 0, False), (Q.rational, 1, False), (Q.rational, EXPR, True)),
        # Implies(Q.integer(x) & Q.integer(y), Q.integer(f(x, y)))
        ((Q.integer, 0, False), (Q.integer, 1, False), (Q.integer, EXPR, True)),
        # Implies(Q.algebraic(x) & Q.algebraic(y), Q.algebraic(f(x, y)))
        ((Q.algebraic, 0, False), (Q.algebraic, 1, False), (Q.algebraic, EXPR, True)),
        # Implies(Q.complex(x) & Q.complex(y), Q.complex(f(x, y)))
        ((Q.complex, 0, False), (Q.complex, 1, False), (Q.complex, EXPR, True)),
        # Implies(Q.rational(x) & ~Q.rational(y) & ~Q.zero(x), ~Q.rational(f(x, y)))
        ((Q.rational, 0, False), (Q.zero, 0, True), (Q.rational, 1, True), (Q.rational, EXPR, False)),
        # Implies(Q.rational(y) & ~Q.rational(x) & ~Q.zero(y), ~Q.rational(f(x, y)))
        ((Q.rational, 0, True), (Q.rational, 1, False), (Q.zero, 1, True), (Q.rational, EXPR, False)),
        # Implies(Q.irrational(y) & Q.rational(x) & ~Q.zero(x), Q.irrational(f(x, y)))
        ((Q.rational, 0, False), (Q.zero, 0, True), (Q.irrational, 1, False), (Q.irrational, EXPR, True)),
        # Implies(Q.irrational(x) & Q.rational(y) & ~Q.zero(y), Q.irrational(f(x, y)))
        ((Q.irrational, 0, False), (Q.rational, 1, False), (Q.zero, 1, True), (Q.irrational, EXPR, True)),
        # Implies(Q.algebraic(x) & ~Q.algebraic(y) & ~Q.zero(x), ~Q.algebraic(f(x, y)))
        ((Q.algebraic, 0, False), (Q.zero, 0, True), (Q.algebraic, 1, True), (Q.algebraic, EXPR, False)),
        # Implies(Q.algebraic(y) & ~Q.algebraic(x) & ~Q.zero(y), ~Q.algebraic(f(x, y)))
        ((Q.algebraic, 0, True), (Q.algebraic, 1, False), (Q.zero, 1, True), (Q.algebraic, EXPR, False)),
        # Implies(Q.algebraic(x) & Q.transcendental(y) & ~Q.zero(x), Q.transcendental(f(x, y)))
        ((Q.algebraic, 0, False), (Q.zero, 0, True), (Q.transcendental, 1, False), (Q.transcendental, EXPR, True)),
        # Implies(Q.algebraic(y) & Q.transcendental(x) & ~Q.zero(y), Q.transcendental(f(x, y)))
        ((Q.transcendental, 0, False), (Q.algebraic, 1, False), (Q.zero, 1, True), (Q.transcendental, EXPR, True)),
        # Implies(Q.complex(x) & ~Q.complex(y), ~Q.complex(f(x, y)))
        ((Q.complex, 0, False), (Q.complex, 1, True), (Q.complex, EXPR, False)),
        # Implies(Q.complex(y) & ~Q.complex(x), ~Q.complex(f(x, y)))
        ((Q.complex, 0, True), (Q.complex, 1, False), (Q.complex, EXPR, False)),
        # Implies(Q.imaginary(x) & Q.imaginary(y), Q.real(f(x, y)))
        ((Q.imaginary, 0, False), (Q.imaginary, 1, False), (Q.real, EXPR, True)),
        # Implies(Q.imaginary(y) & Q.real(x) & ~Q.zero(x), Q.imaginary(f(x, y)))
        ((Q.real, 0, False), (Q.zero, 0, True), (Q.imaginary, 1, False), (Q.imaginary, EXPR, True)),
        # Implies(Q.imaginary(x) & Q.real(y) & ~Q.zero(y), Q.imaginary(f(x, y)))
        ((Q.imaginary, 0, False), (Q.real, 1, False), (Q.zero, 1, True), (Q.imaginary, EXPR, True)),
        # Implies(Q.imaginary(y) & Q.real(x), Equivalent(Q.real(f(x, y)), Q.zero(f(x, y))))
        ((Q.real, 0, False), (Q.imaginary, 1, False), (Q.real, EXPR, False), (Q.zero, EXPR, True)),
        ((Q.real, 0, False), (Q.imaginary, 1, False), (Q.real, EXPR, True), (Q.zero, EXPR, False)),
        # Implies(Q.imaginary(x) & Q.real(y), Equivalent(Q.real(f(x, y)), Q.zero(f(x, y))))
        ((Q.imaginary, 0, False), (Q.real, 1, False), (Q.real, EXPR, False), (Q.zero, EXPR, True)),
        ((Q.imaginary, 0, False), (Q.real, 1, False), (Q.real, EXPR, True), (Q.zero, EXPR, False)),
        # Implies(Q.even(y) & Q.eq(x, 1/2), Q.integer(f(x, y)))
        ((Q.eq, (0, Rational(1, 2)), False), (Q.even, 1, False), (Q.integer, EXPR, True)),
        # Implies(Q.odd(y) & Q.eq(x, 1/2), ~Q.integer(f(x, y)))
        ((Q.eq, (0, Rational(1, 2)), False), (Q.odd, 1, False), (Q.integer, EXPR, False)),
        # Implies(Q.extended_real(x) & Q.extended_real(y) & ~Q.zero(x) & ~Q.zero(y), Q.extended_real(f(x, y)))
        ((Q.extended_real, 0, False), (Q.zero, 0, True), (Q.extended_real, 1, False), (Q.zero, 1, True), (Q.extended_real, EXPR, True)),
        # Implies(Q.commutative(x) & Q.hermitian(x) & Q.hermitian(y), Q.hermitian(f(x, y)))
        ((Q.commutative, 0, False), (Q.hermitian, 0, False), (Q.hermitian, 1, False), (Q.hermitian, EXPR, True)),
        # Implies(Q.commutative(y) & Q.hermitian(x) & Q.hermitian(y), Q.hermitian(f(x, y)))
        ((Q.hermitian, 0, False), (Q.commutative, 1, False), (Q.hermitian, 1, False), (Q.hermitian, EXPR, True)),
        # Implies(Q.antihermitian(x) & Q.antihermitian(y) & Q.commutative(x), Q.hermitian(f(x, y)))
        ((Q.antihermitian, 0, False), (Q.commutative, 0, False), (Q.antihermitian, 1, False), (Q.hermitian, EXPR, True)),
        # Implies(Q.antihermitian(x) & Q.antihermitian(y) & Q.commutative(y), Q.hermitian(f(x, y)))
        ((Q.antihermitian, 0, False), (Q.antihermitian, 1, False), (Q.commutative, 1, False), (Q.hermitian, EXPR, True)),
        # Implies(Q.antihermitian(y) & Q.commutative(x) & Q.hermitian(x), Q.antihermitian(f(x, y)))
        ((Q.commutative, 0, False), (Q.hermitian, 0, False), (Q.antihermitian, 1, False), (Q.antihermitian, EXPR, True)),
        # Implies(Q.antihermitian(y) & Q.commutative(y) & Q.hermitian(x), Q.antihermitian(f(x, y)))
        ((Q.hermitian, 0, False), (Q.antihermitian, 1, False), (Q.commutative, 1, False), (Q.antihermitian, EXPR, True)),
        # Implies(Q.antihermitian(x) & Q.commutative(x) & Q.hermitian(y), Q.antihermitian(f(x, y)))
        ((Q.antihermitian, 0, False), (Q.commutative, 0, False), (Q.hermitian, 1, False), (Q.antihermitian, EXPR, True)),
        # Implies(Q.antihermitian(x) & Q.commutative(y) & Q.hermitian(y), Q.antihermitian(f(x, y)))
        ((Q.antihermitian, 0, False), (Q.commutative, 1, False), (Q.hermitian, 1, False), (Q.antihermitian, EXPR, True)),
    ),
    (Pow, 2): (
        # Implies(Q.finite(base) & Q.finite(exponent) & ~Q.zero(base), Q.finite(f(base, exponent)))
        ((Q.finite, 0, False), (Q.zero, 0, True), (Q.finite, 1, False), (Q.finite, EXPR, True)),
        # Implies(Q.finite(base) & Q.nonnegative(exponent), Q.finite(f(base, exponent)))
        ((Q.finite, 0, False), (Q.nonnegative, 1, False), (Q.finite, EXPR, True)),
        # Implies(Q.extended_negative(exponent) & Q.zero(base), Q.infinite(f(base, exponent)))
        ((Q.zero, 0, False), (Q.extended_negative, 1, False), (Q.infinite, EXPR, True)),
        # Implies(Q.positive(exponent) & ~Q.finite(base), Q.infinite(f(base, exponent)))
        ((Q.finite, 0, True), (Q.positive, 1, False), (Q.infinite, EXPR, True)),
        # Implies(Q.even(base) & Q.integer(exponent) & Q.positive(exponent), Q.even(f(base, exponent)))
        ((Q.even, 0, False), (Q.integer, 1, False), (Q.positive, 1, False), (Q.even, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.odd(base) & ~Q.negative(exponent), Q.odd(f(base, exponent)))
        ((Q.odd, 0, False), (Q.integer, 1, False), (Q.negative, 1, True), (Q.odd, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.eq(base, -1), Q.odd(f(base, exponent)))
        ((Q.eq, (0, Integer(-1)), False), (Q.integer, 1, False), (Q.odd, EXPR, True)),
        # Implies(Q.finite(exponent) & Q.eq(base, 1), Q.odd(f(base, exponent)))
        ((Q.eq, (0, Integer(1)), False), (Q.finite, 1, False), (Q.odd, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.positive(exponent) & Q.prime(base) & ~Q.composite(exponent) & ~Q.prime(exponent), Q.prime(f(base, exponent)))
        ((Q.prime, 0, False), (Q.composite, 1, True), (Q.integer, 1, False), (Q.positive, 1, False), (Q.prime, 1, True), (Q.prime, EXPR, True)),
        # Implies(Q.integer(base) & Q.integer(exponent) & ~Q.prime(base), ~Q.prime(f(base, exponent)))
        ((Q.integer, 0, False), (Q.prime, 0, True), (Q.integer, 1, False), (Q.prime, EXPR, False)),
        # Implies(Q.integer(base) & Q.integer(exponent) & ~Q.positive(exponent), ~Q.prime(f(base, exponent)))
        ((Q.integer, 0, False), (Q.integer, 1, False), (Q.positive, 1, True), (Q.prime, EXPR, False)),
        # Implies(Q.integer(base) & Q.prime(exponent), ~Q.prime(f(base, exponent)))
        ((Q.integer, 0, False), (Q.prime, 1, False), (Q.prime, EXPR, False)),
        # Implies(Q.composite(exponent) & Q.integer(base), ~Q.prime(f(base, exponent)))
        ((Q.integer, 0, False), (Q.composite, 1, False), (Q.prime, EXPR, False)),
        # Implies(Q.integer(base) & Q.integer(exponent) & Q.ne(exponent, 1), ~Q.prime(f(base, exponent)))
        ((Q.integer, 0, False), (Q.integer, 1, False), (Q.eq, (1, Integer(1)), True), (Q.prime, EXPR, False)),
        # Implies(Q.zero(exponent), Q.positive(f(base, exponent)))
        ((Q.zero, 1, False), (Q.positive, EXPR, True)),
        # Implies(Q.finite(exponent) & Q.eq(base, 1), Q.positive(f(base, exponent)))
        ((Q.eq, (0, Integer(1)), False), (Q.finite, 1, False), (Q.positive, EXPR, True)),
        # Implies(Q.positive(base) & Q.real(exponent), Q.positive(f(base, exponent)))
        ((Q.positive, 0, False), (Q.real, 1, False), (Q.positive, EXPR, True)),
        # Implies(Q.even(exponent) & Q.nonzero(base), Q.positive(f(base, exponent)))
        ((Q.nonzero, 0, False), (Q.even, 1, False), (Q.positive, EXPR, True)),
        # Implies(Q.negative(base) & Q.odd(exponent), Q.negative(f(base, exponent)))
        ((Q.negative, 0, False), (Q.odd, 1, False), (Q.negative, EXPR, True)),
        # Implies(Q.even(exponent) & Q.real(base), ~Q.negative(f(base, exponent)))
        ((Q.real, 0, False), (Q.even, 1, False), (Q.negative, EXPR, False)),
        # Implies(Q.even(exponent) & Q.nonnegative(exponent) & Q.real(base), Q.nonnegative(f(base, exponent)))
        ((Q.real, 0, False), (Q.even, 1, False), (Q.nonnegative, 1, False), (Q.nonnegative, EXPR, True)),
        # Implies(Q.nonnegative(base) & Q.odd(exponent), ~Q.negative(f(base, exponent)))
        ((Q.nonnegative, 0, False), (Q.odd, 1, False), (Q.negative, EXPR, False)),
        # Implies(Q.nonnegative(base) & Q.nonnegative(exponent) & Q.odd(exponent), Q.nonnegative(f(base, exponent)))
        ((Q.nonnegative, 0, False), (Q.nonnegative, 1, False), (Q.odd, 1, False), (Q.nonnegative, EXPR, True)),
        # Implies(Q.nonnegative(exponent) & Q.nonpositive(base) & Q.odd(exponent), Q.nonpositive(f(base, exponent)))
        ((Q.nonpositive, 0, False), (Q.nonnegative, 1, False), (Q.odd, 1, False), (Q.nonpositive, EXPR, True)),
        # Implies(Q.positive(exponent) & Q.zero(base), Q.zero(f(base, exponent)))
        ((Q.zero, 0, False), (Q.positive, 1, False), (Q.zero, EXPR, True)),
        # Implies(Q.positive(exponent) & Q.zero(f(base, exponent)), Q.zero(base))
        ((Q.zero, 0, True), (Q.positive, 1, False), (Q.zero, EXPR, False)),
        # Implies(Q.finite(base) & Q.finite(exponent) & Q.zero(f(base, exponent)), Q.zero(base))
        ((Q.finite, 0, False), (Q.zero, 0, True), (Q.finite, 1, False), (Q.zero, EXPR, False)),
        # Implies(Q.finite(base) & Q.real(exponent) & Q.zero(f(base, exponent)), Q.positive(exponent))
        ((Q.finite, 0, False), (Q.positive, 1, True), (Q.real, 1, False), (Q.zero, EXPR, False)),
        # Implies(Q.zero(exponent), Q.integer(f(base, exponent)))
        ((Q.zero, 1, False), (Q.integer, EXPR, True)),
        # Implies(Q.integer(base) & Q.integer(exponent) & ~Q.negative(exponent), Q.integer(f(base, exponent)))
        ((Q.integer, 0, False), (Q.integer, 1, False), (Q.negative, 1, True), (Q.integer, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.rational(base) & ~Q.zero(base), Q.rational(f(base, exponent)))
        ((Q.rational, 0, False), (Q.zero, 0, True), (Q.integer, 1, False), (Q.rational, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.rational(base) & ~Q.negative(exponent), Q.rational(f(base, exponent)))
        ((Q.rational, 0, False), (Q.integer, 1, False), (Q.negative, 1, True), (Q.rational, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.real(base) & ~Q.zero(base), Q.real(f(base, exponent)))
        ((Q.real, 0, False), (Q.zero, 0, True), (Q.integer, 1, False), (Q.real, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.real(base) & ~Q.negative(exponent), Q.real(f(base, exponent)))
        ((Q.real, 0, False), (Q.integer, 1, False), (Q.negative, 1, True), (Q.real, EXPR, True)),
        # Implies(Q.hermitian(base) & Q.integer(exponent) & ~Q.zero(base), Q.hermitian(f(base, exponent)))
        ((Q.hermitian, 0, False), (Q.zero, 0, True), (Q.integer, 1, False), (Q.hermitian, EXPR, True)),
        # Implies(Q.hermitian(base) & Q.integer(exponent) & ~Q.negative(exponent), Q.hermitian(f(base, exponent)))
        ((Q.hermitian, 0, False), (Q.integer, 1, False), (Q.negative, 1, True), (Q.hermitian, EXPR, True)),
        # Implies(Q.integer(base) & Q.integer(exponent) & Q.negative(exponent) & Q.ne(base, -1) & Q.ne(base, 1), ~Q.integer(f(base, exponent)))
        ((Q.integer, 0, False), (Q.eq, (0, Integer(-1)), True), (Q.eq, (0, Integer(1)), True), (Q.integer, 1, False), (Q.negative, 1, False), (Q.integer, EXPR, False)),
        # Implies(Q.irrational(base) & Q.eq(exponent, -1), Q.irrational(f(base, exponent)))
        ((Q.irrational, 0, False), (Q.eq, (1, Integer(-1)), False), (Q.irrational, EXPR, True)),
        # Implies(Q.algebraic(base) & Q.rational(exponent) & ~Q.zero(base), Q.algebraic(f(base, exponent)))
        ((Q.algebraic, 0, False), (Q.zero, 0, True), (Q.rational, 1, False), (Q.algebraic, EXPR, True)),
        # Implies(Q.algebraic(base) & Q.rational(exponent) & ~Q.negative(exponent), Q.algebraic(f(base, exponent)))
        ((Q.algebraic, 0, False), (Q.negative, 1, True), (Q.rational, 1, False), (Q.algebraic, EXPR, True)),
        # Implies(Q.complex(base) & Q.complex(exponent) & ~Q.zero(base), Q.complex(f(base, exponent)))
        ((Q.complex, 0, False), (Q.zero, 0, True), (Q.complex, 1, False), (Q.complex, EXPR, True)),
        # Implies(Q.complex(base) & Q.integer(exponent) & ~Q.negative(exponent), Q.complex(f(base, exponent)))
        ((Q.complex, 0, False), (Q.integer, 1, False), (Q.negative, 1, True), (Q.complex, EXPR, True)),
        # Implies(Q.complex(base) & Q.positive(exponent), Q.complex(f(base, exponent)))
        ((Q.complex, 0, False), (Q.positive, 1, False), (Q.complex, EXPR, True)),
        # Implies(Q.positive(base) & Q.real(exponent), Q.real(f(base, exponent)))
        ((Q.positive, 0, False), (Q.real, 1, False), (Q.real, EXPR, True)),
        # Implies(Q.nonnegative(exponent) & Q.real(exponent) & Q.zero(base), Q.real(f(base, exponent)))
        ((Q.zero, 0, False), (Q.nonnegative, 1, False), (Q.real, 1, False), (Q.real, EXPR, True)),
        # Implies(Q.negative(exponent) & Q.zero(base), ~Q.complex(f(base, exponent)) & ~Q.extended_real(f(base, exponent)))
        ((Q.zero, 0, False), (Q.negative, 1, False), (Q.complex, EXPR, False)),
        ((Q.zero, 0, False), (Q.negative, 1, False), (Q.extended_real, EXPR, False)),
        # Implies(Q.extended_real(base) & Q.integer(exponent) & ~Q.zero(base), Q.extended_real(f(base, exponent)))
        ((Q.extended_real, 0, False), (Q.zero, 0, True), (Q.integer, 1, False), (Q.extended_real, EXPR, True)),
        # Implies(Q.extended_real(base) & Q.integer(exponent) & ~Q.negative(exponent), Q.extended_real(f(base, exponent)))
        ((Q.extended_real, 0, False), (Q.integer, 1, False), (Q.negative, 1, True), (Q.extended_real, EXPR, True)),
        # Implies(Q.even(exponent) & Q.imaginary(base), Q.real(f(base, exponent)))
        ((Q.imaginary, 0, False), (Q.even, 1, False), (Q.real, EXPR, True)),
        # Implies(Q.imaginary(base) & Q.odd(exponent), Q.imaginary(f(base, exponent)))
        ((Q.imaginary, 0, False), (Q.odd, 1, False), (Q.imaginary, EXPR, True)),
        # Implies(Q.antihermitian(base) & Q.even(exponent) & ~Q.zero(base), Q.hermitian(f(base, exponent)))
        ((Q.antihermitian, 0, False), (Q.zero, 0, True), (Q.even, 1, False), (Q.hermitian, EXPR, True)),
        # Implies(Q.antihermitian(base) & Q.even(exponent) & ~Q.negative(exponent), Q.hermitian(f(base, exponent)))
        ((Q.antihermitian, 0, False), (Q.even, 1, False), (Q.negative, 1, True), (Q.hermitian, EXPR, True)),
        # Implies(Q.antihermitian(base) & Q.odd(exponent) & ~Q.zero(base), Q.antihermitian(f(base, exponent)))
        ((Q.antihermitian, 0, False), (Q.zero, 0, True), (Q.odd, 1, False), (Q.antihermitian, EXPR, True)),
        # Implies(Q.antihermitian(base) & Q.odd(exponent) & ~Q.negative(exponent), Q.antihermitian(f(base, exponent)))
        ((Q.antihermitian, 0, False), (Q.negative, 1, True), (Q.odd, 1, False), (Q.antihermitian, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.real(base), ~Q.imaginary(f(base, exponent)))
        ((Q.real, 0, False), (Q.integer, 1, False), (Q.imaginary, EXPR, False)),
        # Implies(Q.irrational(exponent) & Q.real(base), ~Q.imaginary(f(base, exponent)))
        ((Q.real, 0, False), (Q.irrational, 1, False), (Q.imaginary, EXPR, False)),
        # Implies(Q.negative(base) & Q.rational(exponent) & ~Q.integer(exponent), ~Q.real(f(base, exponent)))
        ((Q.negative, 0, False), (Q.integer, 1, True), (Q.rational, 1, False), (Q.real, EXPR, False)),
        # Implies(Q.prime(base) & Q.rational(exponent) & ~Q.integer(exponent), Q.irrational(f(base, exponent)))
        ((Q.prime, 0, False), (Q.integer, 1, True), (Q.rational, 1, False), (Q.irrational, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.transcendental(base) & ~Q.zero(exponent), Q.transcendental(f(base, exponent)))
        ((Q.transcendental, 0, False), (Q.integer, 1, False), (Q.zero, 1, True), (Q.transcendental, EXPR, True)),
        # Implies(Q.integer(exponent) & Q.positive(exponent) & ~Q.algebraic(base), ~Q.algebraic(f(base, exponent)))
        ((Q.algebraic, 0, True), (Q.integer, 1, False), (Q.positive, 1, False), (Q.algebraic, EXPR, False)),
    ),
    (Symbol, None): (
        # Implies(Q.commutative(x) & ~Q.finite(x), Q.infinite(x))
        ((Q.commutative, EXPR, False), (Q.finite, EXPR, True), (Q.infinite, EXPR, True)),
    ),
    (Trace, 1): (
        # Implies(Q.integer_elements(x), Q.integer_elements(f(x)))
        ((Q.integer_elements, 0, False), (Q.integer_elements, EXPR, True)),
        # Implies(Q.real_elements(x), Q.real_elements(f(x)))
        ((Q.real_elements, 0, False), (Q.real_elements, EXPR, True)),
        # Implies(Q.complex_elements(x), Q.complex_elements(f(x)))
        ((Q.complex_elements, 0, False), (Q.complex_elements, EXPR, True)),
        # Implies(Q.positive_definite(x), Q.positive(f(x)))
        ((Q.positive_definite, 0, False), (Q.positive, EXPR, True)),
        # Implies(Q.integer_elements(x), Q.integer(f(x)))
        ((Q.integer_elements, 0, False), (Q.integer, EXPR, True)),
        # Implies(Q.real_elements(x), Q.real(f(x)))
        ((Q.real_elements, 0, False), (Q.real, EXPR, True)),
        # Implies(Q.complex_elements(x), Q.complex(f(x)))
        ((Q.complex_elements, 0, False), (Q.complex, EXPR, True)),
    ),
    (Transpose, 1): (
        # Equivalent(Q.symmetric(x), Q.symmetric(f(x)))
        ((Q.symmetric, 0, False), (Q.symmetric, EXPR, True)),
        ((Q.symmetric, 0, True), (Q.symmetric, EXPR, False)),
        # Equivalent(Q.invertible(x), Q.invertible(f(x)))
        ((Q.invertible, 0, False), (Q.invertible, EXPR, True)),
        ((Q.invertible, 0, True), (Q.invertible, EXPR, False)),
        # Equivalent(Q.orthogonal(x), Q.orthogonal(f(x)))
        ((Q.orthogonal, 0, False), (Q.orthogonal, EXPR, True)),
        ((Q.orthogonal, 0, True), (Q.orthogonal, EXPR, False)),
        # Equivalent(Q.unitary(x), Q.unitary(f(x)))
        ((Q.unitary, 0, False), (Q.unitary, EXPR, True)),
        ((Q.unitary, 0, True), (Q.unitary, EXPR, False)),
        # Equivalent(Q.fullrank(x), Q.fullrank(f(x)))
        ((Q.fullrank, 0, False), (Q.fullrank, EXPR, True)),
        ((Q.fullrank, 0, True), (Q.fullrank, EXPR, False)),
        # Equivalent(Q.positive_definite(x), Q.positive_definite(f(x)))
        ((Q.positive_definite, 0, False), (Q.positive_definite, EXPR, True)),
        ((Q.positive_definite, 0, True), (Q.positive_definite, EXPR, False)),
        # Equivalent(Q.diagonal(x), Q.diagonal(f(x)))
        ((Q.diagonal, 0, False), (Q.diagonal, EXPR, True)),
        ((Q.diagonal, 0, True), (Q.diagonal, EXPR, False)),
        # Equivalent(Q.integer_elements(x), Q.integer_elements(f(x)))
        ((Q.integer_elements, 0, False), (Q.integer_elements, EXPR, True)),
        ((Q.integer_elements, 0, True), (Q.integer_elements, EXPR, False)),
        # Equivalent(Q.real_elements(x), Q.real_elements(f(x)))
        ((Q.real_elements, 0, False), (Q.real_elements, EXPR, True)),
        ((Q.real_elements, 0, True), (Q.real_elements, EXPR, False)),
        # Equivalent(Q.complex_elements(x), Q.complex_elements(f(x)))
        ((Q.complex_elements, 0, False), (Q.complex_elements, EXPR, True)),
        ((Q.complex_elements, 0, True), (Q.complex_elements, EXPR, False)),
        # Equivalent(Q.lower_triangular(x), Q.upper_triangular(f(x)))
        ((Q.lower_triangular, 0, False), (Q.upper_triangular, EXPR, True)),
        ((Q.lower_triangular, 0, True), (Q.upper_triangular, EXPR, False)),
        # Equivalent(Q.upper_triangular(x), Q.lower_triangular(f(x)))
        ((Q.upper_triangular, 0, False), (Q.lower_triangular, EXPR, True)),
        ((Q.upper_triangular, 0, True), (Q.lower_triangular, EXPR, False)),
    ),
    (acos, 1): (
        # ~Q.negative(f(x))
        ((Q.negative, EXPR, False),),
        # Implies(Q.zero(x), Q.positive(f(x)))
        ((Q.zero, 0, False), (Q.positive, EXPR, True)),
        # Implies(Q.algebraic(x) & Q.ne(x, 1), ~Q.algebraic(f(x)))
        ((Q.algebraic, 0, False), (Q.eq, (0, Integer(1)), True), (Q.algebraic, EXPR, False)),
    ),
    (acot, 1): (
        # Implies(Q.finite(x) & ~Q.real(x), ~Q.extended_real(f(x)))
        ((Q.finite, 0, False), (Q.real, 0, True), (Q.extended_real, EXPR, False)),
        # Implies(Q.nonnegative(x), Q.positive(f(x)))
        ((Q.nonnegative, 0, False), (Q.positive, EXPR, True)),
        # Implies(Q.negative(x), Q.negative(f(x)))
        ((Q.negative, 0, False), (Q.negative, EXPR, True)),
        # Implies(Q.extended_nonnegative(x), Q.extended_nonnegative(f(x)))
        ((Q.extended_nonnegative, 0, False), (Q.extended_nonnegative, EXPR, True)),
        # Implies(Q.extended_negative(x), Q.nonpositive(f(x)))
        ((Q.extended_negative, 0, False), (Q.nonpositive, EXPR, True)),
        # Implies(Q.algebraic(x), ~Q.algebraic(f(x)))
        ((Q.algebraic, 0, False), (Q.algebraic, EXPR, False)),
        # Implies(Q.algebraic(x) & ~Q.imaginary(x), Q.transcendental(f(x)))
        ((Q.algebraic, 0, False), (Q.imaginary, 0, True), (Q.transcendental, EXPR, True)),
    ),
    (asin, 1): (
        # Implies(Q.zero(x), Q.zero(f(x)))
        ((Q.zero, 0, False), (Q.zero, EXPR, True)),
        # Implies(Q.extended_nonnegative(x), ~Q.negative(f(x)))
        ((Q.extended_nonnegative, 0, False), (Q.negative, EXPR, False)),
        # Implies(Q.extended_nonpositive(x), ~Q.positive(f(x)))
        ((Q.extended_nonpositive, 0, False), (Q.positive, EXPR, False)),
        # Implies(Q.algebraic(x) & ~Q.zero(x), Q.transcendental(f(x)))
        ((Q.algebraic, 0, False), (Q.zero, 0, True), (Q.transcendental, EXPR, True)),
    ),
    (atan, 1): (
        # Implies(Q.finite(x) & ~Q.real(x), ~Q.extended_real(f(x)))
        ((Q.finite, 0, False), (Q.real, 0, True), (Q.extended_real, EXPR, False)),
        # Implies(Q.extended_positive(x), Q.positive(f(x)))
        ((Q.extended_positive, 0, False), (Q.positive, EXPR, True)),
        # Implies(Q.extended_negative(x), Q.negative(f(x)))
        ((Q.extended_negative, 0, False), (Q.negative, EXPR, True)),
        # Implies(Q.zero(x), Q.zero(f(x)))
        ((Q.zero, 0, False), (Q.zero, EXPR, True)),
        # Implies(Q.algebraic(x) & ~Q.zero(x), ~Q.algebraic(f(x)))
        ((Q.algebraic, 0, False), (Q.zero, 0, True), (Q.algebraic, EXPR, False)),
        # Implies(Q.algebraic(x) & ~Q.imaginary(x) & ~Q.zero(x), Q.transcendental(f(x)))
        ((Q.algebraic, 0, False), (Q.imaginary, 0, True), (Q.zero, 0, True), (Q.transcendental, EXPR, True)),
    ),
    (cos, 1): (
        # Implies(Q.finite(x), Q.finite(f(x)))
        ((Q.finite, 0, False), (Q.finite, EXPR, True)),
        # Implies(Q.real(x), Q.real(f(x)))
        ((Q.real, 0, False), (Q.real, EXPR, True)),
        # Implies(Q.complex(x), Q.complex(f(x)))
        ((Q.complex, 0, False), (Q.complex, EXPR, True)),
        # Implies(Q.zero(x), Q.integer(f(x)))
        ((Q.zero, 0, False), (Q.integer, EXPR, True)),
        # Implies(Q.algebraic(x) & ~Q.zero(x), Q.transcendental(f(x)))
        ((Q.algebraic, 0, False), (Q.zero, 0, True), (Q.transcendental, EXPR, True)),
    ),
    (cot, 1): (
        # Implies(Q.algebraic(x), ~Q.algebraic(f(x)))
        ((Q.algebraic, 0, False), (Q.algebraic, EXPR, False)),
    ),
    (exp, 1): (
        # Implies(Q.finite(x), Q.finite(f(x)))
        ((Q.finite, 0, False), (Q.finite, EXPR, True)),
        # Implies(Q.positive_infinite(x), Q.positive_infinite(f(x)))
        ((Q.positive_infinite, 0, False), (Q.positive_infinite, EXPR, True)),
        # Implies(Q.negative_infinite(x), Q.zero(f(x)))
        ((Q.negative_infinite, 0, False), (Q.zero, EXPR, True)),
        # Implies(Q.real(x), Q.positive(f(x)))
        ((Q.real, 0, False), (Q.positive, EXPR, True)),
        # Implies(Q.extended_real(x), Q.extended_nonnegative(f(x)))
        ((Q.extended_real, 0, False), (Q.extended_nonnegative, EXPR, True)),
        # Implies(Q.finite(x), ~Q.zero(f(x)))
        ((Q.finite, 0, False), (Q.zero, EXPR, False)),
        # Implies(Q.real(x), Q.real(f(x)))
        ((Q.real, 0, False), (Q.real, EXPR, True)),
        # Implies(Q.complex(x), Q.complex(f(x)))
        ((Q.complex, 0, False), (Q.complex, EXPR, True)),
        # Implies(Q.zero(x), Q.integer(f(x)))
        ((Q.zero, 0, False), (Q.integer, EXPR, True)),
        # Implies(Q.algebraic(x) & ~Q.zero(x), Q.transcendental(f(x)))
        ((Q.algebraic, 0, False), (Q.zero, 0, True), (Q.transcendental, EXPR, True)),
    ),
    (factorial, 1): (
        # Implies(Q.integer(x) & Q.nonnegative(x), Q.positive(f(x)))
        ((Q.integer, 0, False), (Q.nonnegative, 0, False), (Q.positive, EXPR, True)),
    ),
    (im, 1): (
        # Implies(Q.real(x), Q.even(f(x)))
        ((Q.real, 0, False), (Q.even, EXPR, True)),
        # Implies(Q.complex(x), Q.real(f(x)))
        ((Q.complex, 0, False), (Q.real, EXPR, True)),
    ),
    (log, 1): (
        # Implies(Q.finite(x) & ~Q.zero(x), Q.finite(f(x)))
        ((Q.finite, 0, False), (Q.zero, 0, True), (Q.finite, EXPR, True)),
        # Implies(Q.zero(x), Q.infinite(f(x)))
        ((Q.zero, 0, False), (Q.infinite, EXPR, True)),
        # Implies(~Q.finite(x), Q.infinite(f(x)))
        ((Q.finite, 0, True), (Q.infinite, EXPR, True)),
        # Implies(Q.positive_infinite(x), Q.positive_infinite(f(x)))
        ((Q.positive_infinite, 0, False), (Q.positive_infinite, EXPR, True)),
        # Implies(~Q.positive(x), ~Q.real(f(x)))
        ((Q.positive, 0, True), (Q.real, EXPR, False)),
        # Equivalent(Q.positive(x), Q.real(f(x)))
        ((Q.positive, 0, False), (Q.real, EXPR, True)),
        # Implies(Q.complex(x) & ~Q.zero(x), Q.complex(f(x)))
        ((Q.complex, 0, False), (Q.zero, 0, True), (Q.complex, EXPR, True)),
        # Implies(Q.algebraic(x) & Q.ne(x, 1), ~Q.algebraic(f(x)))
        ((Q.algebraic, 0, False), (Q.eq, (0, Integer(1)), True), (Q.algebraic, EXPR, False)),
    ),
    (re, 1): (
        # Implies(Q.even(x), Q.even(f(x)))
        ((Q.even, 0, False), (Q.even, EXPR, True)),
        # Implies(Q.odd(x), Q.odd(f(x)))
        ((Q.odd, 0, False), (Q.odd, EXPR, True)),
        # Implies(Q.real(x) & ~Q.even(x), ~Q.even(f(x)))
        ((Q.even, 0, True), (Q.real, 0, False), (Q.even, EXPR, False)),
        # Implies(Q.complex(x), Q.real(f(x)))
        ((Q.complex, 0, False), (Q.real, EXPR, True)),
        # Implies(Q.extended_real(x), Q.extended_real(f(x)))
        ((Q.extended_real, 0, False), (Q.extended_real, EXPR, True)),
    ),
    (sign, 1): (
        # Q.finite(f(x))
        ((Q.finite, EXPR, True),),
    ),
    (sin, 1): (
        # Implies(Q.finite(x), Q.finite(f(x)))
        ((Q.finite, 0, False), (Q.finite, EXPR, True)),
        # Implies(Q.real(x), Q.real(f(x)))
        ((Q.real, 0, False), (Q.real, EXPR, True)),
        # Implies(Q.complex(x), Q.complex(f(x)))
        ((Q.complex, 0, False), (Q.complex, EXPR, True)),
        # Implies(Q.zero(x), Q.zero(f(x)))
        ((Q.zero, 0, False), (Q.zero, EXPR, True)),
        # Implies(Q.algebraic(x) & ~Q.zero(x), Q.transcendental(f(x)))
        ((Q.algebraic, 0, False), (Q.zero, 0, True), (Q.transcendental, EXPR, True)),
    ),
    (tan, 1): (
        # Implies(Q.zero(x), Q.zero(f(x)))
        ((Q.zero, 0, False), (Q.zero, EXPR, True)),
        # Implies(Q.algebraic(x) & ~Q.zero(x), Q.transcendental(f(x)))
        ((Q.algebraic, 0, False), (Q.zero, 0, True), (Q.transcendental, EXPR, True)),
    ),
}
