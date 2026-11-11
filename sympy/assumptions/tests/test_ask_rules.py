from __future__ import annotations

from importlib import import_module

from sympy.abc import w, x, y, z
from sympy.assumptions.ask import Q
from sympy.assumptions.ask_rules import RULES
from sympy.assumptions.ask_rules_generated import RULES as GENERATED_RULES
from sympy.assumptions.assume import Predicate
from sympy.assumptions.rule_checks import check_no_cycles
from sympy.assumptions.rule_engine import (ALL_ARGS, ANY_ARG, EVEN_NUMBER_OF_ARGS,
    FALSE_IF, IF_AND_ONLY_IF, ODD_NUMBER_OF_ARGS, ONE_ARG, OTHER_ARGS, SELF, TRUE_IF,
    ask_by_rules)
from sympy.core.add import Add
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.core.facts import FactKB
from sympy.core.function import Function
from sympy.core.mul import Mul
from sympy.core.numbers import I, pi
from sympy.core.power import Pow
from sympy.core.symbol import Symbol
from sympy.functions.combinatorial.factorials import factorial
from sympy.functions.elementary.complexes import Abs, im, re, sign
from sympy.functions.elementary.exponential import exp, log
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.functions.elementary.trigonometric import (acos, acot, asin, atan,
    cos, cot, sin, tan)
from sympy.matrices.expressions.blockmatrix import BlockDiagMatrix
from sympy.matrices.expressions.determinant import Determinant
from sympy.matrices.expressions.diagonal import DiagMatrix, DiagonalMatrix
from sympy.matrices.expressions.factorizations import (EigenValues, EigenVectors,
    Factorization, LofCholesky, LofLU, QofQR, RofQR, SofSVD, UofLU, UofSVD, VofSVD)
from sympy.matrices.expressions.fourier import DFT, IDFT
from sympy.matrices.expressions.hadamard import HadamardProduct
from sympy.matrices.expressions.inverse import Inverse
from sympy.matrices.expressions.matadd import MatAdd
from sympy.matrices.expressions.matexpr import MatrixElement, MatrixSymbol
from sympy.matrices.expressions.matmul import MatMul
from sympy.matrices.expressions.matpow import MatPow
from sympy.matrices.expressions.slice import MatrixSlice
from sympy.matrices.expressions.special import Identity, ZeroMatrix
from sympy.matrices.expressions.trace import Trace
from sympy.matrices.expressions.transpose import Transpose

A = MatrixSymbol('A', 3, 3)
B = MatrixSymbol('B', 3, 3)
C = MatrixSymbol('C', 2, 3)
VARYING = (Add, BlockDiagMatrix, HadamardProduct, MatAdd, MatMul, Mul)
ABOUT_ALL_ARGS = (ALL_ARGS, ANY_ARG, ONE_ARG, EVEN_NUMBER_OF_ARGS, ODD_NUMBER_OF_ARGS,
                  OTHER_ARGS)


def ask(predicate, expr, assumptions=True):
    return ask_by_rules(predicate, expr, assumptions, RULES)


def ask_generated(predicate, expr, assumptions=True):
    return ask_by_rules(predicate, expr, assumptions, GENERATED_RULES)


def number_of_arguments(cls):
    if cls in (Basic, Expr, Symbol):
        return 0
    if issubclass(cls, Function):
        return max(cls.nargs)
    if cls is DiagonalMatrix or issubclass(cls, Factorization):
        return 1
    return {
        Pow: 2,
        MatPow: 2,
        Inverse: 2,
        Determinant: 1,
        Trace: 1,
        Transpose: 1,
        MatrixElement: 3,
        MatrixSlice: 3,
    }[cls]


def test_no_cycles():
    check_no_cycles(RULES)


def test_rules_are_well_formed():
    for (cls, predicate), rules in RULES.items():
        assert isinstance(cls, type) and issubclass(cls, Basic)
        assert isinstance(predicate, Predicate)
        assert rules
        for kind, conditions in rules:
            assert kind in (FALSE_IF, TRUE_IF, IF_AND_ONLY_IF)
            for selector, condition_predicate in conditions:
                argument, expected = selector
                assert type(argument) is int and type(expected) is bool
                if cls in VARYING:
                    assert argument in ABOUT_ALL_ARGS
                else:
                    assert argument == SELF or 0 <= argument < number_of_arguments(cls)
                assert isinstance(condition_predicate, Predicate)


def test_numbers():
    assert ask(Q.positive, Abs(x), Q.positive(x)) is True
    assert ask(Q.zero, Abs(x), ~Q.zero(x)) is False
    assert ask(Q.even, Abs(Abs(x)), Q.even(x)) is True
    assert ask(Q.odd, x, Q.integer(x) & ~Q.even(x)) is True
    assert ask(Q.hermitian, sin(x), Q.real(x)) is True
    assert ask(Q.positive, x**y, Q.positive(x) & Q.real(y)) is True
    assert ask(Q.negative, x**y, Q.negative(x) & Q.odd(y)) is True
    assert ask(Q.real, x**y, Q.negative(x) & Q.rational(y) & ~Q.integer(y)) is False
    assert ask(Q.integer, x**y, Q.zero(y)) is True
    assert ask(Q.positive, exp(x), Q.real(x)) is True
    assert ask(Q.zero, exp(x), Q.real(x)) is False
    assert ask(Q.integer, cos(x), Q.zero(x)) is True
    assert ask(Q.zero, sin(x), Q.zero(x)) is True
    assert ask(Q.transcendental, tan(x), Q.algebraic(x) & ~Q.zero(x)) is True
    assert ask(Q.negative, atan(x), Q.negative(x)) is True
    assert ask(Q.negative, acos(x)) is False
    assert ask(Q.positive, acot(x), Q.positive(x)) is True
    assert ask(Q.positive, asin(x), Q.negative(x)) is False
    assert ask(Q.algebraic, cot(x), Q.algebraic(x)) is False
    assert ask(Q.imaginary, re(x)) is False
    assert ask(Q.real, im(x), Q.complex(x)) is True
    assert ask(Q.positive, factorial(x), Q.integer(x) & Q.nonnegative(x)) is True
    assert ask(Q.finite, sign(x)) is True


def test_matrices():
    assert ask(Q.positive, Determinant(A), Q.positive_definite(A)) is True
    assert ask(Q.real, Trace(A), Q.real_elements(A)) is True
    assert ask(Q.lower_triangular, A.T, Q.upper_triangular(A)) is True
    assert ask(Q.invertible, A.T, ~Q.invertible(A)) is False
    assert ask(Q.symmetric, A.I, Q.symmetric(A)) is True
    assert ask(Q.invertible, MatPow(A, x), Q.invertible(A) & Q.integer(x)) is True
    assert ask(Q.real, A[0, 1], Q.real_elements(A)) is True
    assert ask(Q.integer_elements, A[:2, :2], Q.integer_elements(A)) is True


def test_sums_and_products():
    P, N, R = Q.positive, Q.negative, Q.rational
    assert ask_generated(P, x + y, P(x) & Q.nonnegative(y)) is True
    assert ask_generated(P, x + y, Q.nonnegative(x) & P(y)) is True
    assert ask_generated(P, x + y, P(x) & N(y)) is None
    assert ask_generated(N, x + y + z, N(x) & Q.nonpositive(y) & N(z)) is True
    assert ask_generated(Q.even, x + y + z, Q.odd(x) & Q.odd(y) & Q.even(z)) is True
    assert ask_generated(Q.even, x + y + z, Q.even(x) & Q.odd(y) & Q.odd(z)) is True
    assert ask_generated(Q.odd, x + y + z, Q.odd(x) & Q.odd(y) & Q.odd(z)) is True
    assert ask_generated(Q.odd, x + y, Q.odd(x) & Q.odd(y)) is False
    assert ask_generated(Q.irrational, x + y + z, R(x) & Q.irrational(y) & R(z)) is True
    assert ask_generated(Q.irrational, x + y, Q.irrational(x) & Q.irrational(y)) is None
    assert ask_generated(Q.integer, x + y + z,
                         Q.integer(x) & ~Q.integer(y) & Q.integer(z)) is False
    assert ask_generated(Q.integer, x + y, ~Q.integer(x) & ~Q.integer(y)) is None
    assert ask_generated(Q.finite, x + y + z, Q.real(x) & ~Q.finite(y)) is False
    assert ask_generated(Q.positive_infinite, x + y,
                         Q.positive_infinite(x) & Q.real(y)) is True
    assert ask_generated(Q.extended_real, x + y,
                         Q.positive_infinite(x) & Q.negative_infinite(y)) is None
    assert ask_generated(Q.imaginary, x + y, Q.imaginary(x) & Q.imaginary(y)) is None
    assert ask_generated(Q.imaginary, x + y, Q.imaginary(x) & Q.nonzero(y)) is False
    assert ask_generated(P, x*y*z*w, N(x) & N(y) & P(z) & P(w)) is True
    assert ask_generated(P, x*y*z*w, P(x) & N(y) & P(z) & N(w)) is True
    assert ask_generated(N, x*y*z, N(x) & N(y) & N(z)) is True
    assert ask_generated(P, x*y*z, P(x) & N(y) & P(z)) is False
    assert ask_generated(Q.zero, x*y, Q.zero(x) & Q.finite(y)) is True
    assert ask_generated(Q.zero, x*y, Q.zero(x)) is None
    assert ask_generated(Q.zero, x*y*z, ~Q.zero(x) & Q.nonzero(y) & P(z)) is False
    assert ask_generated(Q.irrational, x*y, Q.irrational(x) & R(y) & ~Q.zero(y)) is True
    assert ask_generated(Q.irrational, x*y, Q.irrational(x) & R(y)) is None
    assert ask_generated(Q.even, x*y*z, Q.integer(x) & Q.even(y) & Q.integer(z)) is True
    assert ask_generated(Q.real, x*y, Q.imaginary(x) & Q.imaginary(y)) is True
    assert ask_generated(Q.real, x*y, Q.imaginary(x) & P(y)) is False
    assert ask_generated(Q.composite, x*y, Q.prime(x) & Q.prime(y)) is True
    assert ask_generated(Q.prime, x*y*z,
                         Q.integer(x) & Q.composite(y) & Q.integer(z)) is False
    assert ask_generated(Q.symmetric, A + B, Q.symmetric(A) & Q.symmetric(B)) is True
    assert ask_generated(Q.symmetric, A + B, Q.symmetric(A) & ~Q.symmetric(B)) is False
    assert ask_generated(Q.symmetric, A*B, Q.symmetric(A) & Q.symmetric(B)) is None
    assert ask_generated(Q.invertible, A*B, Q.invertible(A) & Q.invertible(B)) is True
    assert ask_generated(Q.invertible, A*B,
                         Q.square(A) & Q.square(B) & ~Q.invertible(B)) is False
    assert ask_generated(Q.invertible, A*B, ~Q.invertible(B)) is None


def test_matrix_classes():
    square = Q.square
    real_symmetric = Q.real_elements(A) & Q.symmetric(A)
    assert ask_generated(Q.orthogonal, Identity(3)) is True
    assert ask_generated(Q.positive_definite, Identity(3)) is True
    assert ask_generated(Q.singular, Identity(3)) is False
    assert ask_generated(Q.real_elements, Identity(3)) is True
    assert ask_generated(Q.invertible, ZeroMatrix(2, 2)) is False
    assert ask_generated(Q.unitary, ZeroMatrix(2, 2)) is False
    assert ask_generated(Q.integer_elements, ZeroMatrix(2, 3)) is True
    assert ask_generated(Q.diagonal, ZeroMatrix(2, 2), square(ZeroMatrix(2, 2))) is True
    assert ask_generated(Q.normal, ZeroMatrix(2, 2), square(ZeroMatrix(2, 2))) is True
    assert ask_generated(Q.diagonal, ZeroMatrix(2, 3), ~square(ZeroMatrix(2, 3))) is False
    assert ask_generated(Q.symmetric, ZeroMatrix(2, 3), ~square(ZeroMatrix(2, 3))) is False
    assert ask_generated(Q.upper_triangular, ZeroMatrix(2, 3),
                         ~square(ZeroMatrix(2, 3))) is None
    assert ask_generated(Q.symmetric, DiagMatrix(C[0, :].T)) is True
    assert ask_generated(Q.upper_triangular, DiagonalMatrix(A), square(A)) is True
    assert ask_generated(Q.diagonal, DiagonalMatrix(C), ~square(C)) is False
    assert ask_generated(Q.diagonal, DiagonalMatrix(C)) is None
    assert ask_generated(Q.invertible, DFT(3)) is True
    assert ask_generated(Q.unitary, IDFT(3)) is True
    assert ask_generated(Q.complex_elements, DFT(3)) is True
    assert ask_generated(Q.lower_triangular, LofLU(A)) is True
    assert ask_generated(Q.lower_triangular, LofCholesky(A)) is True
    assert ask_generated(Q.triangular, UofLU(C)) is True
    assert ask_generated(Q.upper_triangular, RofQR(C)) is True
    assert ask_generated(Q.real_elements, LofLU(A), Q.real_elements(A)) is True
    assert ask_generated(Q.complex_elements, RofQR(A), Q.complex_elements(A)) is True
    assert ask_generated(Q.unitary, QofQR(A), square(A)) is True
    assert ask_generated(Q.singular, QofQR(A), square(A)) is False
    assert ask_generated(Q.orthogonal, QofQR(A), square(A)) is None
    assert ask_generated(Q.orthogonal, QofQR(A), square(A) & Q.real_elements(A)) is True
    assert ask_generated(Q.unitary, QofQR(C), ~square(C)) is None
    assert ask_generated(Q.invertible, UofSVD(A), square(A)) is True
    assert ask_generated(Q.orthogonal, VofSVD(A), square(A) & Q.real_elements(A)) is True
    assert ask_generated(Q.unitary, VofSVD(C), ~square(C)) is None
    assert ask_generated(Q.diagonal, SofSVD(A), square(A)) is True
    assert ask_generated(Q.diagonal, SofSVD(C), ~square(C)) is None
    assert ask_generated(Q.symmetric, EigenValues(A), square(A)) is True
    assert ask_generated(Q.real_elements, EigenValues(A), Q.real_elements(A)) is None
    assert ask_generated(Q.real_elements, EigenValues(A), real_symmetric) is True
    assert ask_generated(Q.orthogonal, EigenVectors(A), Q.real_elements(A)) is None
    assert ask_generated(Q.orthogonal, EigenVectors(A), real_symmetric) is True


def test_wrong_answers_of_ask():
    # ask gives an answer for each of these, and it is wrong
    N = MatrixSymbol('N', Symbol('n', integer=True), Symbol('m', integer=True))
    real_and_two_imaginary = Q.real(x) & Q.imaginary(y) & Q.imaginary(z)

    # a factor or a term may be zero
    assert ask_generated(Q.imaginary, x*y, Q.imaginary(x) & Q.real(y)) is None
    assert ask_generated(Q.imaginary, I*x, Q.real(x)) is None
    assert ask_generated(Q.imaginary, x + I, Q.real(x)) is None
    assert ask_generated(Q.imaginary, x + y, Q.imaginary(x) & Q.real(y)) is None
    assert ask_generated(Q.imaginary, x + y + z, real_and_two_imaginary) is None
    assert ask_generated(Q.antihermitian, x, Q.real(x)) is None
    assert ask_generated(Q.antihermitian, I*x, Q.antihermitian(x)) is None
    assert ask_generated(Q.antihermitian, x + I, Q.real(x)) is None
    assert ask_generated(Q.antihermitian, x + y, Q.antihermitian(x) & Q.real(y)) is None
    assert ask_generated(Q.antihermitian, x + y, Q.imaginary(x) & Q.real(y)) is None
    assert ask_generated(Q.antihermitian, x + y + z, real_and_two_imaginary) is None
    assert ask_generated(Q.hermitian, I*x, Q.hermitian(x)) is None
    assert ask_generated(Q.hermitian, I*x, Q.real(x)) is None
    assert ask_generated(Q.hermitian, x*y, Q.real(x) & Q.zero(y)) is True
    assert ask_generated(Q.extended_real, x*y, Q.imaginary(x) & Q.zero(y)) is True
    assert ask_generated(Q.rational, x*y, Q.irrational(x) & Q.zero(y)) is True
    assert ask_generated(Q.irrational, x*y, Q.zero(x) & Q.irrational(y)) is False
    assert ask_generated(Q.transcendental, x*y,
                         Q.zero(x) & Q.transcendental(y)) is False
    assert ask_generated(Q.integer, sqrt(2)*x, Q.integer(x)) is None
    assert ask_generated(Q.nonzero, 5**(2*I*pi*x), Q.integer(x)) is None
    assert ask_generated(Q.imaginary, x**y,
                         Q.negative(x) & Q.rational(y) & Q.integer(2*y)) is None
    assert ask_generated(Q.zero, x*y, Q.zero(x)) is None

    # the terms may cancel
    assert ask_generated(Q.imaginary, x + I, Q.imaginary(x)) is None
    assert ask_generated(Q.imaginary, x + y, Q.imaginary(x) & Q.imaginary(y)) is None

    # the argument may be infinite
    assert ask_generated(Q.real, Abs(x)) is None
    assert ask_generated(Q.complex, Abs(x)) is None
    assert ask_generated(Q.real, re(x)) is None
    assert ask_generated(Q.complex, re(x)) is None
    assert ask_generated(Q.real, im(x)) is None
    assert ask_generated(Q.complex, im(x)) is None
    assert ask_generated(Q.complex, exp(x)) is None
    assert ask_generated(Q.complex, sin(x)) is None
    assert ask_generated(Q.complex, cos(x)) is None
    assert ask_generated(Q.finite, sin(x)) is None
    assert ask_generated(Q.finite, sin(x), ~Q.finite(x)) is None
    assert ask_generated(Q.finite, cos(x)) is None
    assert ask_generated(Q.finite, cos(x), ~Q.finite(x)) is None
    assert ask_generated(Q.finite, 2*sin(x)) is None
    assert ask_generated(Q.finite, sin(x)**2) is None
    assert ask_generated(Q.finite, cos(x)**2) is None
    assert ask_generated(Q.finite, log(x), ~Q.zero(x)) is None
    assert ask_generated(Q.finite, 2**x, ~Q.finite(x)) is None

    # a power of zero may be infinite
    assert ask_generated(Q.algebraic, x**y, Q.algebraic(x) & Q.rational(y)) is None
    assert ask_generated(Q.complex, x**y, Q.complex(x) & Q.complex(y)) is None

    # acos(1) is zero, acot(-1) is negative, (2*I)**(I*pi/(2*log(2))) is imaginary
    assert ask_generated(Q.positive, acos(x),
                         Q.nonnegative(x + 1) & Q.nonpositive(x - 1)) is None
    assert ask_generated(Q.positive, acot(x), Q.real(x)) is None
    assert ask_generated(Q.imaginary, (2*I)**x, Q.imaginary(x)) is None

    # the dimensions n and m may be equal
    assert ask_generated(Q.invertible, N) is None

    # a product of symmetric matrices need not be symmetric, and a sum may be
    assert ask_generated(Q.symmetric, A*B, Q.symmetric(A) & Q.symmetric(B)) is None
    assert ask_generated(Q.symmetric, A + B) is None

    # a part of an invertible matrix need not be invertible
    assert ask_generated(Q.invertible, A[1:, 1:], Q.invertible(A)) is None
    assert ask_generated(Q.orthogonal, A[1:, 1:], Q.orthogonal(A)) is None


def test_old_assumptions_are_not_used():
    def forbidden(*args):
        raise AssertionError('the old assumptions were used')

    p = Symbol('p', positive=True)
    queries = [
        (Q.positive, exp(x)**y, Q.real(x) & Q.real(y), True),
        (Q.even, Abs(Abs(x)), Q.even(x), True),
        (Q.zero, Abs(x), ~Q.zero(x), False),
        (Q.symmetric, A.I, Q.symmetric(A), True),
        (Q.positive, x, True, None),
        (Q.positive, p, True, None),
        (Q.zero, Abs(p), True, None),
        (Q.positive, exp(p), True, None),
    ]
    # sympy.core.assumptions is also the name of a function
    core_assumptions = import_module('sympy.core.assumptions')
    originals = core_assumptions._ask, FactKB.deduce_all_facts
    core_assumptions._ask = FactKB.deduce_all_facts = forbidden
    try:
        for predicate, expr, assumptions, expected in queries:
            assert ask(predicate, expr, assumptions) is expected
    finally:
        core_assumptions._ask, FactKB.deduce_all_facts = originals
