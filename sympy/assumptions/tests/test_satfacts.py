from __future__ import annotations
from sympy.assumptions.ask import Q
from sympy.assumptions.satask import satask
from sympy.core.numbers import (I, Rational, oo, pi)
from sympy.core.symbol import symbols
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.exponential import (exp, log)
from sympy.functions.elementary.trigonometric import (acos, cos, sin)
from sympy.matrices.dense import Matrix
from sympy.matrices.expressions import (BlockDiagMatrix, BlockMatrix, Identity,
    MatrixSymbol, OneMatrix, ZeroMatrix)
from sympy.testing.pytest import raises

x, y, z = symbols('x y z')


def test_commutative():
    a = symbols('a', commutative=False)
    assert satask(Q.commutative(x)) is True
    assert satask(Q.commutative(x), ~Q.commutative(x)) is False
    assert satask(Q.commutative(x + 1), ~Q.commutative(x)) is False
    assert satask(Q.commutative(a)) is False
    assert satask(Q.commutative(2*x)) is True


def test_old_assumptions():
    p = symbols('p', positive=True)
    assert satask(Q.positive(p + 1)) is True
    assert satask(Q.prime(7)) is True
    assert satask(Q.finite(oo)) is False
    assert satask(Q.algebraic(pi)) is False


def test_numbers():
    assert satask(Q.positive(pi - 3)) is True
    assert satask(Q.negative(-I + I*(cos(2)**2 + sin(2)**2))) is False
    assert satask(Q.real((1 + I)**I)) is False
    assert satask(Q.prime(cos(1)**2 + sin(1)**2 + 12345678901234567890)) is True


def test_ntheory():
    assert satask(Q.even(x + y), Q.odd(x) & Q.odd(y)) is True
    assert satask(Q.odd(x + y + z), Q.odd(x) & Q.even(y) & Q.even(z)) is True
    assert satask(Q.even(x*y*(y + z)), Q.integer(x) & Q.integer(y) & Q.odd(z)) is True
    assert satask(Q.even(x**2), Q.even(x)) is True
    assert satask(Q.odd(x**y), Q.odd(x) & Q.integer(y) & Q.nonnegative(y)) is True
    assert satask(Q.prime(x**2), Q.integer(x)) is False
    assert satask(Q.even(Abs(x)), Q.even(x)) is True
    assert satask(Q.even(Abs(x)), ~Q.even(x)) is None


def test_order():
    assert satask(Q.positive(x + y), Q.positive(x) & Q.nonnegative(y)) is True
    assert satask(Q.negative(x*y), Q.positive(x) & Q.negative(y)) is True
    assert satask(Q.positive(x*y*z), Q.negative(x) & Q.negative(y) & Q.positive(z)) is True
    assert satask(Q.positive(exp(x)), Q.real(x)) is True
    assert satask(Q.positive(x**2), Q.real(x) & ~Q.zero(x)) is True
    assert satask(Q.negative(x**3), Q.negative(x)) is True
    assert satask(Q.positive(acos(x)), Q.nonnegative(x + 1) & Q.negative(x - 1)) is True
    assert satask(Q.positive(acos(x)), Q.nonnegative(x + 1) & Q.nonpositive(x - 1)) is None


def test_sets():
    assert satask(Q.real(x*y), Q.imaginary(x) & Q.imaginary(y)) is True
    assert satask(Q.imaginary(x*y), Q.imaginary(x) & Q.real(y) & ~Q.zero(y)) is True
    assert satask(Q.imaginary(x*y), Q.imaginary(x) & Q.real(y)) is None
    assert satask(Q.imaginary(x + y), Q.imaginary(x) & Q.real(y) & ~Q.zero(y)) is False
    assert satask(Q.integer(x*Rational(1, 2)), Q.even(x)) is True
    assert satask(Q.real(x**y), Q.positive(x) & Q.real(y)) is True
    assert satask(Q.imaginary(x**Rational(1, 2)), Q.negative(x)) is True
    assert satask(Q.real(log(x)), Q.positive(x)) is True
    assert satask(Q.real(log(x)), Q.negative(x)) is False
    assert satask(Q.rational(exp(x)), Q.rational(x) & ~Q.zero(x)) is False
    assert satask(Q.hermitian(x*y), Q.antihermitian(x) & Q.antihermitian(y)) is True
    assert satask(Q.hermitian(Matrix([[1, I], [-I, 2]]))) is True


def test_calculus():
    assert satask(Q.finite(x + y), Q.finite(x) & Q.finite(y)) is True
    assert satask(Q.finite(x + y), Q.finite(x) & ~Q.finite(y)) is False
    assert satask(Q.finite(x + y), Q.positive_infinite(x) & Q.positive_infinite(y)) is False
    assert satask(Q.positive_infinite(x + y), Q.real(x) & Q.positive_infinite(y)) is True
    assert satask(Q.finite(x*y), Q.finite(x) & ~Q.finite(y)) is None
    assert satask(Q.finite(x*y), ~Q.zero(x) & ~Q.finite(y)) is False
    assert satask(Q.finite(exp(x)), Q.finite(x)) is True
    assert satask(Q.finite(log(x)), Q.zero(x)) is False
    assert satask(Q.finite(log(x)), ~Q.zero(x)) is None
    assert satask(Q.finite(sin(x))) is True


def test_matrices():
    X = MatrixSymbol('X', 2, 2)
    Y = MatrixSymbol('Y', 2, 3)
    Z = MatrixSymbol('Z', 2, 2)
    assert satask(Q.square(X)) is True
    assert satask(Q.square(Y)) is False
    assert satask(Q.symmetric(Y*Y.T)) is True
    assert satask(Q.invertible(X*Z), Q.invertible(X) & Q.invertible(Z)) is True
    assert satask(Q.invertible(X*Z), ~Q.invertible(X)) is False
    assert satask(Q.invertible(X.T), Q.invertible(X)) is True
    assert satask(Q.upper_triangular(X.T), Q.lower_triangular(X)) is True
    assert satask(Q.diagonal(X**3), Q.diagonal(X)) is True
    assert satask(Q.symmetric(X**2), ~Q.symmetric(X)) is None
    assert satask(Q.symmetric(X[:2, 1:2]), Q.symmetric(X)) is False
    assert satask(Q.invertible(Identity(3))) is True
    assert satask(Q.invertible(ZeroMatrix(3, 3))) is False
    assert satask(Q.invertible(OneMatrix(3, 3))) is False
    assert satask(Q.invertible(BlockDiagMatrix(Identity(3), Identity(5)))) is True
    assert satask(Q.invertible(BlockMatrix([[Identity(3)]]))) is True
    assert satask(Q.positive(X[1, 1]), Q.positive_definite(X)) is True


def test_inconsistent():
    raises(ValueError, lambda: satask(Q.real(x),
                                      Q.positive(x*y) & Q.positive(x) & Q.negative(y)))
