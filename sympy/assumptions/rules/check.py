"""
Tests the rules of this package on concrete values.

A row holds for every value of its arguments, so it must hold when numbers
or explicit matrices are put in for them. For those, the truth value of a
predicate does not come from any rule: it is read from the value itself.

The values include infinities, and ``nan`` comes up as the value of an
expression (``0*oo``). It is not zero, not real, and so on: no predicate but
``Q.commutative`` holds for ``nan``. So a row may not conclude that an
expression which can be ``nan`` has a property, and whether such an
expression is finite or infinite is not known: a row may not conclude that
it is not finite or not infinite either.

The arguments themselves are numbers and never ``nan``, with one exception.
A row about a sum or a product is written for ``f(x, y)``, where ``y`` is the
sum or the product of all the arguments but the first, and that can be
``nan`` when every argument is a number. So ``y`` is ``nan`` too in the
tests of those rows.
"""
from __future__ import annotations

from itertools import product

from sympy.assumptions.ask import Q
from sympy.assumptions.rules.compiler import clauses, nargs
from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.core.numbers import E, I, Integer, Rational, oo, pi, zoo
from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.matrices.exceptions import ShapeError
from sympy.matrices.immutable import ImmutableMatrix
from sympy.matrices.matrixbase import MatrixBase

NUMBERS = (
    S.Zero, S.One, S.NegativeOne, Integer(2), Integer(-2), Integer(3),
    Integer(4), Rational(1, 2), Rational(-1, 2), Rational(3, 2), sqrt(2),
    -sqrt(2), pi, E, I, -I, 2*I, 1 + I, oo, -oo, zoo, oo*I,
)

MATRICES = (
    ImmutableMatrix([[1, 0], [0, 1]]),
    ImmutableMatrix([[0, 0], [0, 0]]),
    ImmutableMatrix([[1, 2], [3, 4]]),
    ImmutableMatrix([[1, 2], [2, 4]]),
    ImmutableMatrix([[2]]),
    ImmutableMatrix([[1, 2, 3], [4, 5, 6]]),
    ImmutableMatrix([[1, 2], [3, 4], [5, 6]]),
)

NUMBER_TRUTH = {
    Q.positive_infinite: lambda value: value is S.Infinity,
    Q.negative_infinite: lambda value: value is S.NegativeInfinity,
}

MATRIX_TRUTH = {
    Q.square: lambda value: value.rows == value.cols,
    Q.invertible: lambda value: value.rows == value.cols and value.det() != 0,
    Q.positive_definite: lambda value: value.is_positive_definite,
    Q.integer_elements: lambda value: all(e.is_integer for e in value),
    Q.real_elements: lambda value: all(e.is_real for e in value),
    Q.complex_elements: lambda value: all(e.is_complex for e in value),
}

_truth: dict = {}
_values: dict = {}


def truth(predicate, value):
    """
    The truth value of *predicate* for *value*, or ``None`` if it is not
    known.

    Examples
    ========

    >>> from sympy import Q, oo, nan
    >>> from sympy.assumptions.rules.check import truth
    >>> truth(Q.positive, oo), truth(Q.extended_positive, oo)
    (False, True)
    >>> truth(Q.zero, nan)
    False

    """
    key = (predicate, value)
    if key not in _truth:
        _truth[key] = _read(predicate, value)
    return _truth[key]


def _read(predicate, value):
    if value is S.NaN:
        return predicate == Q.commutative
    if isinstance(value, MatrixBase):
        test = MATRIX_TRUTH.get(predicate)
    else:
        test = NUMBER_TRUTH.get(predicate)
        if test is None:
            result = getattr(value, 'is_' + predicate.name, None)
            return result if isinstance(result, bool) else None
    if test is None:
        return None
    return bool(test(value))


def value_of(cls, values):
    """
    The value of ``cls(*values)``, or ``None`` if there is no such
    expression.
    """
    key = (cls, values)
    if key not in _values:
        try:
            value = cls(*values)
            if any(isinstance(v, MatrixBase) for v in values):
                value = value.doit()
        except (TypeError, ValueError, NotImplementedError, ShapeError):
            value = None
        _values[key] = value
    return _values[key]


def _samples(cls, row):
    number = nargs(row)
    if number is None:
        pool = NUMBERS if issubclass(cls, Symbol) else NUMBERS + MATRICES
        yield from ((value,) for value in pool
                    if isinstance(value, cls) or issubclass(cls, Symbol))
        return
    for pool in (NUMBERS, MATRICES):
        for values in product(pool, repeat=number):
            value = value_of(cls, values)
            if value is not None:
                yield (*values, value)
    if number == 2 and issubclass(cls, (Add, Mul)):
        for first in NUMBERS:
            yield (first, S.NaN, value_of(cls, (first, S.NaN)))


def counterexamples(cls, row):
    """
    The values of the arguments for which *row* is false when ``f`` is
    *cls*, each followed by the value of the expression.

    Examples
    ========

    >>> from sympy import Abs, Q
    >>> from sympy.assumptions.rules.check import counterexamples
    >>> from sympy.assumptions.rules.language import f, x
    >>> counterexamples(Abs, Q.integer(x) >> Q.integer(f(x)))
    []
    >>> counterexamples(Abs, Q.nonnegative(f(x)))
    [(oo, oo), (-oo, oo), (zoo, oo), (oo*I, oo)]

    """
    row_clauses = clauses(row)
    return [sample for sample in _samples(cls, row)
            if any(all(_is_false(literal, sample) for literal in clause)
                   for clause in row_clauses)]


def _is_false(literal, sample):
    predicate, slot, value = literal
    if slot == -1 and sample[slot] is S.NaN and predicate in (Q.finite, Q.infinite):
        return True
    return truth(predicate, sample[slot]) is (not value)


def untested(cls, row):
    """
    The clauses of *row* which no value puts to the test when ``f`` is
    *cls*.

    Explanation
    ===========

    A value tests a clause when it makes one of its literals true and the
    others false, so that the clause holds only because of that literal.

    Examples
    ========

    >>> from sympy import Abs, Q
    >>> from sympy.assumptions.rules.check import untested
    >>> from sympy.assumptions.rules.language import f, x
    >>> untested(Abs, Q.integer(x) >> Q.integer(f(x)))
    []
    >>> untested(Abs, Q.symmetric(x) >> Q.integer(f(x)))
    [((Q.symmetric, 0, False), (Q.integer, -1, True))]

    """
    remaining = clauses(row)
    for sample in _samples(cls, row):
        if S.NaN in sample[:-1]:
            continue
        remaining = [clause for clause in remaining
                     if not _tests(sample, clause)]
        if not remaining:
            break
    return remaining


def _tests(sample, clause):
    truths = [truth(predicate, sample[slot]) for predicate, slot, _ in clause]
    if None in truths:
        return False
    return sum(found is value for found, (_, _, value) in zip(truths, clause)) == 1
