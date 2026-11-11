from __future__ import annotations

from importlib import import_module

from sympy.abc import x, y
from sympy.assumptions.ask import Q
from sympy.assumptions.ask_rules import RULES
from sympy.assumptions.assume import Predicate
from sympy.assumptions.rule_checks import check_no_cycles
from sympy.assumptions.rule_engine import (FALSE_IF, IF_AND_ONLY_IF, SELF,
    TRUE_IF, ask_by_rules)
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.core.facts import FactKB
from sympy.core.function import Function
from sympy.core.power import Pow
from sympy.core.symbol import Symbol
from sympy.functions.combinatorial.factorials import factorial
from sympy.functions.elementary.complexes import Abs, im, re, sign
from sympy.functions.elementary.exponential import exp
from sympy.functions.elementary.trigonometric import (acos, acot, asin, atan,
    cos, cot, sin, tan)
from sympy.matrices.expressions.determinant import Determinant
from sympy.matrices.expressions.inverse import Inverse
from sympy.matrices.expressions.matexpr import MatrixElement, MatrixSymbol
from sympy.matrices.expressions.matpow import MatPow
from sympy.matrices.expressions.slice import MatrixSlice
from sympy.matrices.expressions.trace import Trace
from sympy.matrices.expressions.transpose import Transpose

A = MatrixSymbol('A', 3, 3)


def ask(predicate, expr, assumptions=True):
    return ask_by_rules(predicate, expr, assumptions, RULES)


def number_of_arguments(cls):
    if cls in (Basic, Expr, Symbol):
        return 0
    if issubclass(cls, Function):
        return max(cls.nargs)
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
