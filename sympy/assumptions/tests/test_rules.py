from __future__ import annotations

from pathlib import Path

import sympy.assumptions
from sympy.abc import a, b, c, d
from sympy.assumptions import compiled_rules
from sympy.assumptions.ask import Q, _ask_recursive
from sympy.assumptions.compiled_rules import (ask_rules, evaluate,
    rule_arguments, sat_rules)
from sympy.assumptions.facts import get_known_facts
from sympy.assumptions.rules.check import counterexamples, untested
from sympy.assumptions.rules.compiler import (GENERATED, clauses, nargs,
    statements, ways)
from sympy.assumptions.rules.language import closed, f, for_all, node, x, y
from sympy.core.add import Add
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.core.function import Function
from sympy.core.mul import Mul
from sympy.core.numbers import ImaginaryUnit, nan, oo
from sympy.core.symbol import Symbol
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.trigonometric import cos, sin
from sympy.logic.boolalg import Equivalent
from sympy.logic.inference import satisfiable
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


def test_rows_about_every_expression_follow_from_facts():
    facts = get_known_facts(x)
    for classes, rows in statements():
        if Expr in classes or Basic in classes:
            for row in rows:
                if nargs(row) is None:
                    assert satisfiable(facts & ~row) is False, row


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

    row = (Q.real(x) & ~Q.rational(x)) >> Q.irrational(x)
    assert for_all((Expr,), row).rows == (row,)
    assert node(row) == x
    assert nargs(row) is None
    assert nargs(Q.real(f(x))) == 1
    assert clauses(row) == [
        ((Q.irrational, -1, True), (Q.rational, -1, True), (Q.real, -1, False))]
    assert counterexamples(Expr, row) == []
    assert untested(Expr, row) == []
    assert (0,) in counterexamples(Expr, Q.real(x) >> Q.irrational(x))
    raises(ValueError, lambda: for_all((Expr,), Q.real(x) >> Q.complex(y)))


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
    assert sat_rules(sin, 2) == ()
    # a class has the rules of the classes it derives from
    assert set(sat_rules(Mul, 2)) < set(sat_rules(MatMul, 2))


def test_ways():
    # every literal about the expression, if the others are about arguments
    assert ways(Equivalent(Q.zero(f(x)), Q.zero(x))) == {
        Q.zero: {(True, ((Q.zero, 0, True),)), (False, ((Q.zero, 0, False),))}}
    assert ways((Q.zero(f(x, y)) & Q.finite(x)) >> Q.zero(y)) == {
        Q.zero: {(False, ((Q.finite, 0, True), (Q.zero, 1, False)))}}
    # otherwise only the predicates of the conclusion
    assert ways((Q.integer(x) & ~Q.even(x)) >> Q.odd(x)) == {
        Q.odd: {(True, ((Q.even, -1, False), (Q.integer, -1, True)))}}
    assert ways(Q.finite(f(x)) >> (Q.real(x) >> Q.real(f(x)))) == {
        Q.real: {(True, ((Q.real, 0, True), (Q.finite, -1, True)))}}
    assert ways(Q.imaginary(x) >> (Q.imaginary(f(x)) | Q.zero(f(x)))) == {
        Q.imaginary: {(True, ((Q.imaginary, 0, True), (Q.zero, -1, False)))},
        Q.zero: {(True, ((Q.imaginary, 0, True), (Q.imaginary, -1, False)))}}


def test_ask_rules():
    assert (True, ((Q.even, 0, True),)) in ask_rules(Abs, 1, Q.even)
    # an odd number is not even, and zero is even
    assert (False, ((Q.odd, 0, True),)) in ask_rules(Abs, 1, Q.even)
    assert (True, ((Q.zero, 0, True),)) in ask_rules(Abs, 1, Q.even)
    # a number which is not an integer is not even
    assert (False, ((Q.integer, 0, False), (Q.integer, 1, True))) in ask_rules(Add, 2, Q.even)
    # without rows for a class, the ways are not about arguments
    assert all(slot == -1 for _, conditions in ask_rules(Abs, 2, Q.even)
               for _, slot, _ in conditions)
    assert all(slot == -1 for _, conditions in ask_rules(Function('g'), 1, Q.even)
               for _, slot, _ in conditions)
    assert set(ask_rules(Mul, 2, Q.zero)) <= set(ask_rules(MatMul, 2, Q.zero))


def _with_rules(predicates, function):
    saved = compiled_rules.RULE_PREDICATES
    compiled_rules.RULE_PREDICATES = frozenset(predicates)
    try:
        return function()
    finally:
        compiled_rules.RULE_PREDICATES = saved


def test_evaluate():
    assert evaluate(Q.real, (a,), Q.positive(a)) is True
    assert evaluate(Q.real, (a,), ~Q.complex(a)) is False
    assert evaluate(Q.real, (a,), Q.positive(b)) is None
    assert evaluate(Q.real, (a,), Q.positive(a) | Q.negative(a)) is None
    assert evaluate(Q.real, (a,), ~(Q.complex(a) | Q.zero(b))) is False

    class node(Function):
        pass

    rules = compiled_rules.ASK_RULES
    rules[node, 2] = {
        Q.integer: ((True, ((Q.integer, 0, True), (Q.integer, 1, True))),
                    (False, ((Q.integer, 0, True), (Q.integer, 1, False)))),
        Q.irrational: ((True, ((Q.rational, 0, True), (Q.irrational, 1, True))),),
    }
    try:
        ask = lambda *args: _with_rules(
            [Q.integer, Q.rational], lambda: _ask_recursive(*args))
        assert _with_rules([], lambda: _ask_recursive(
            Q.integer(node(a, b)), Q.integer(a) & Q.integer(b))) is None
        assert ask(Q.integer(node(a, b)), Q.integer(a) & Q.integer(b)) is True
        assert ask(Q.integer(node(a, b)), Q.integer(a) & ~Q.integer(b)) is False
        assert ask(Q.integer(node(a, b)), Q.integer(a)) is None
        assert ask(Q.integer(node(a, node(b, c))),
            Q.integer(a) & Q.integer(b) & Q.integer(c)) is True
        assert ask(Q.integer(node(a, node(b, c))),
            Q.integer(a) & Q.integer(b) & Q.irrational(c)) is False
        # a rule for a predicate also answers for the predicates which it
        # decides: an irrational number is not rational
        assert ask(Q.rational(node(a, b)), Q.rational(a) & Q.irrational(b)) is False
        # only the predicates of RULE_PREDICATES are answered with rules
        assert ask(Q.irrational(node(a, b)), Q.rational(a) & Q.irrational(b)) is None
        # sums and products are read as their first argument and the rest
        rules[Add, 2], saved = rules[node, 2], rules[Add, 2]
        compiled_rules._ask_rules.clear()
        try:
            assert ask(Q.integer(a + b + c + d),
                Q.integer(a) & Q.integer(b) & Q.integer(c) & Q.integer(d)) is True
        finally:
            rules[Add, 2] = saved
            compiled_rules._ask_rules.clear()
    finally:
        del rules[node, 2]


def test_evaluate_one_expression():
    rules = compiled_rules.ASK_RULES
    saved = rules.get((Expr, None))
    rules[Expr, None] = {
        Q.irrational: ((True, ((Q.real, -1, True), (Q.rational, -1, False))),),
    }
    compiled_rules._ask_rules.clear()
    try:
        ask = lambda *args: _with_rules(
            [Q.irrational, Q.real, Q.rational], lambda: _ask_recursive(*args))
        assert ask(Q.irrational(a), Q.real(a) & ~Q.rational(a)) is True
        assert ask(Q.irrational(a + b), Q.real(a + b) & ~Q.rational(a + b)) is True
        assert ask(Q.irrational(a), Q.real(a)) is None
        assert ask(Q.irrational(sin(a)), Q.real(sin(a)) & ~Q.rational(sin(a))) is True
    finally:
        if saved is None:
            del rules[Expr, None]
        else:
            rules[Expr, None] = saved
        compiled_rules._ask_rules.clear()


def test_evaluate_old_assumptions_and_handlers():
    p = Symbol('p', positive=True)
    ask = lambda *args: _with_rules([Q.positive, Q.real, Q.prime], lambda: _ask_recursive(*args))
    assert ask(Q.positive(p)) is True
    assert ask(Q.real(p)) is True
    assert ask(Q.positive(a)) is None
    # a class without rules is asked for its old assumptions
    assert ask(Q.real(sin(p))) is True
    # numbers are given to the handlers
    assert ask(Q.positive(sin(1) - 2)) is False
    assert ask(Q.prime(7)) is True

    has_handler = compiled_rules._has_handler
    assert has_handler(Q.positive, Symbol) is False
    assert has_handler(Q.is_true, Symbol) is False
    assert has_handler(Q.positive, ImaginaryUnit) is True

    class my_function(Function):
        pass

    assert has_handler(Q.prime, my_function) is False
    assert ask(Q.prime(my_function(a))) is None

    @Q.prime.register(my_function)
    def _(expr, assumptions):
        return True

    assert has_handler(Q.prime, my_function) is True
    assert ask(Q.prime(my_function(a))) is True


def test_evaluate_numbers_in_propositions():
    # each part of a proposition is asked about, and its number evaluated
    number = cos(1)**2 + sin(1)**2
    ask = lambda *args: _with_rules(
        [Q.integer, Q.even, Q.zero, Q.positive], lambda: _ask_recursive(*args))
    assert ask(Q.integer(number)) is True
    assert ask(Q.integer(number) | Q.zero(a)) is True
    assert ask(Q.zero(a) | Q.integer(number)) is True
    assert ask(Q.positive(a) & Q.integer(number), Q.positive(a)) is True
    assert ask(~Q.even(number + 2)) is True


def test_evaluate_question_asked_again():
    class node(Function):
        pass

    rules = compiled_rules.ASK_RULES
    rules[node, 1] = {
        Q.real: ((True, ((Q.positive, -1, True),)),
                 (True, ((Q.real, 0, True),))),
        Q.positive: ((True, ((Q.real, -1, True), (Q.positive, 0, True))),),
    }
    try:
        ask = lambda *args: _with_rules(
            [Q.real, Q.positive], lambda: _ask_recursive(*args))
        assert ask(Q.real(node(a))) is None
        assert ask(Q.positive(node(a))) is None
        assert ask(Q.positive(node(a)), Q.positive(a)) is True
        assert ask(Q.real(node(a)), Q.real(a)) is True
        assert ask(Q.positive(node(a)), Q.real(a)) is None
    finally:
        del rules[node, 1]
