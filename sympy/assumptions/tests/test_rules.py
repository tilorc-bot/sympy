from __future__ import annotations

from pathlib import Path

import sympy.assumptions
from sympy.abc import a, b, c, d
from sympy.assumptions.ask import Q
from sympy.assumptions.compiled_rules import rule_arguments, sat_rules
from sympy.assumptions.rules.check import counterexamples, untested
from sympy.assumptions.rules.compiler import GENERATED, clauses, statements
from sympy.assumptions.rules.language import closed, f, for_all, x, y
from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.core.numbers import nan, oo
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.trigonometric import sin
from sympy.logic.boolalg import Equivalent
from sympy.matrices.expressions.matexpr import MatrixSymbol
from sympy.matrices.expressions.matmul import MatMul
from sympy.testing.pytest import raises


def test_generated_modules_are_current():
    # Run bin/ask_update.py if this fails.
    directory = Path(sympy.assumptions.__file__).parent
    for name, source in GENERATED.items():
        assert (directory / name).read_text() == source(), name


def test_rules_hold_for_values():
    for classes, rows in statements():
        for cls in classes:
            for row in rows:
                assert not counterexamples(cls, row), (cls, row)


def test_rules_are_tested_by_values():
    for classes, rows in statements():
        for cls in classes:
            for row in rows:
                assert not untested(cls, row), (cls, row)


def test_for_all():
    statement = for_all((Abs, sin), Q.zero(x) >> Q.zero(f(x)), closed(f(x), Q.real, Q.integer))
    assert statement.classes == (Abs, sin)
    assert statement.rows == (
        Q.zero(x) >> Q.zero(f(x)),
        Q.real(x) >> Q.real(f(x)),
        Q.integer(x) >> Q.integer(f(x)))
    assert closed(f(x, y), Q.real) == ((Q.real(x) & Q.real(y)) >> Q.real(f(x, y)),)

    raises(ValueError, lambda: for_all((Mul,), Q.real(x) & Q.real(y) >> Q.real(f(x, y))))
    raises(ValueError, lambda: for_all((Mul,), Q.real(x) >> Q.real(y)))
    raises(ValueError, lambda: for_all((Mul,), Q.real(f(x)) >> Q.real(f(x, y))))
    raises(ValueError, lambda: for_all((Mul,), Q.real(a) >> Q.real(f(x, y))))
    raises(ValueError, lambda: for_all((Mul,), Q.real(f(x, x))))
    raises(ValueError, lambda: for_all((Mul,), Q.real(f(x + 1))))
    raises(TypeError, lambda: for_all((Mul,), f(x)))


def test_clauses():
    assert clauses(Q.real(f(x))) == [((Q.real, -1, True),)]
    assert clauses((Q.real(x) & ~Q.zero(y)) >> Q.real(f(x, y))) == [
        ((Q.real, 0, False), (Q.zero, 1, True), (Q.real, -1, True))]
    assert clauses(Equivalent(Q.zero(f(x)), Q.zero(x))) == [
        ((Q.zero, 0, False), (Q.zero, -1, True)),
        ((Q.zero, 0, True), (Q.zero, -1, False))]
    assert clauses(Q.real(x) >> (Q.real(f(x)) | Q.real(x))) == []


def test_counterexamples():
    assert counterexamples(Abs, Q.real(x) >> Q.nonnegative(f(x))) == []
    assert (oo, oo) in counterexamples(Abs, Q.nonnegative(f(x)))
    assert (0, 1, 0) in counterexamples(
        Mul, Q.zero(f(x, y)) >> (Q.zero(x) & Q.zero(y)))
    # 0*oo is nan, which is not zero and not known to be finite or infinite
    assert (0, oo, nan) in counterexamples(Mul, Q.zero(x) >> Q.zero(f(x, y)))
    assert (0, oo, nan) in counterexamples(Mul, Q.infinite(y) >> ~Q.finite(f(x, y)))
    assert (0, oo, nan) in counterexamples(Mul, Q.infinite(y) >> Q.infinite(f(x, y)))
    assert counterexamples(Mul, Q.infinite(y) >> ~Q.real(f(x, y))) == []
    assert untested(Mul, (Q.symmetric(x) & Q.real(y)) >> Q.real(f(x, y))) == [
        ((Q.symmetric, 0, False), (Q.real, 1, False), (Q.real, -1, True))]


def test_rule_arguments():
    X, Y, Z = (MatrixSymbol(name, 2, 2) for name in 'XYZ')
    assert rule_arguments(a) == ()
    assert rule_arguments(sin(a)) == (a,)
    assert rule_arguments(a**b) == (a, b)
    assert rule_arguments(a*b) == (a, b)
    assert rule_arguments(a + b + c + d) == (a, b + c + d)
    assert rule_arguments(2*a*b) == (2, a*b)
    assert rule_arguments(MatMul(X, Y, Z)) == (X, MatMul(Y, Z))
    assert rule_arguments(Add(a, b, c, evaluate=False)) == (a, b + c)


def test_sat_rules():
    assert ((Q.even, 0, False), (Q.even, -1, True)) in sat_rules(Abs, 1)
    assert sat_rules(Abs, 2) == ()
    assert sat_rules(sin, 1) == ()
    # a class has the rules of the classes it derives from
    assert set(sat_rules(Mul, 2)) < set(sat_rules(MatMul, 2))
