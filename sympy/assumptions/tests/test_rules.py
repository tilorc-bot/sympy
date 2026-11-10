from __future__ import annotations

from pathlib import Path

import sympy.assumptions
from sympy.abc import a, b, c, d
from sympy.assumptions import compiled_rules
from sympy.assumptions.ask import Q, _ask_recursive
from sympy.assumptions.compiled_rules import (ask_rules, equal, evaluate,
    rule_arguments, sat_rules, split_sat_rules)
from sympy.assumptions.facts import get_known_facts
from sympy.assumptions.rules.check import SAMPLES, counterexamples, untested
from sympy.assumptions.rules.compiler import (GENERATED, _render, clauses,
    nargs, statements, ways)
from sympy.assumptions.rules.language import (base, closed, columns,
    exponent, f, for_all, i, j, node, rows, x, y)
from sympy.assumptions.satask import satask
from sympy.core.add import Add
from sympy.core.basic import Basic
from sympy.core.containers import Tuple
from sympy.core.expr import Expr
from sympy.core.function import Function
from sympy.core.mul import Mul
from sympy.core.numbers import ImaginaryUnit, Integer, Rational, nan, oo, pi
from sympy.core.symbol import Symbol
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.trigonometric import cos, sin
from sympy.logic.boolalg import And, Equivalent
from sympy.logic.inference import satisfiable
from sympy.matrices.expressions.blockmatrix import BlockDiagMatrix
from sympy.matrices.expressions.matexpr import MatrixElement, MatrixSymbol
from sympy.matrices.expressions.matmul import MatMul
from sympy.matrices.expressions.slice import MatrixSlice
from sympy.matrices.immutable import ImmutableMatrix
from sympy.testing.pytest import raises


def test_generated_modules_are_current():
    # Run bin/ask_update.py if this fails.
    directory = Path(sympy.assumptions.__file__).parent
    for name, source in GENERATED.items():
        assert (directory / name).read_text() == source(), name


def test_rules_hold_for_values():
    for classes, statement_rows in statements():
        for cls in classes:
            for row in statement_rows:
                assert not counterexamples(cls, row), (cls, row)


def test_rules_are_tested_by_values():
    for classes, statement_rows in statements():
        for cls in classes:
            for row in statement_rows:
                assert not untested(cls, row), (cls, row)


def test_rows_about_every_expression_follow_from_facts():
    facts = get_known_facts(x)
    for classes, statement_rows in statements():
        if Expr in classes or Basic in classes:
            for row in statement_rows:
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
    assert rule_arguments(BlockDiagMatrix(X)) == (X,)
    assert rule_arguments(BlockDiagMatrix(X, Y)) == (X, Y)
    assert rule_arguments(BlockDiagMatrix(X, Y, Z)) == (X, BlockDiagMatrix(Y, Z))


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


def test_relations_in_rows():
    row = (Q.positive_definite(x) & Q.eq(i, j)) >> Q.positive(f(x, i, j))
    assert for_all((MatrixElement,), row).rows == (row,)
    assert node(row) == f(x, i, j)
    assert nargs(row) == 3
    assert node(Q.eq(base, -1) >> Q.positive(f(base, exponent))) == f(base, exponent)
    assert node(Q.eq(Rational(1, 2), base) >> Q.positive(f(base, exponent))) == f(base, exponent)
    raises(ValueError, lambda: node(Q.ne(i, j) >> Q.positive(f(x, i, j))))
    raises(ValueError, lambda: node(Q.gt(i, j) >> Q.positive(f(x, i, j))))
    raises(ValueError, lambda: node(Q.eq(i, i) >> Q.positive(f(x, i, j))))
    raises(ValueError, lambda: node(Q.eq(1, 2) >> Q.positive(f(x, i, j))))
    raises(ValueError, lambda: node(Q.eq(i, a) >> Q.positive(f(x, i, j))))
    raises(ValueError, lambda: node(Q.eq(i, pi) >> Q.positive(f(x, i, j))))
    raises(ValueError, lambda: node(Q.eq(i, f(x, i, j)) >> Q.positive(f(x, i, j))))
    raises(ValueError, lambda: node(Q.eq(x, 1) >> Q.positive(x)))


def test_relations_compiled():
    row = (Q.positive_definite(x) & Q.eq(i, j)) >> Q.positive(f(x, i, j))
    assert clauses(row) == [
        ((Q.positive_definite, 0, False), (Q.eq, (1, 2), False), (Q.positive, -1, True))]
    assert ways(row) == {
        Q.positive: {(True, ((Q.positive_definite, 0, True), (Q.eq, (1, 2), True)))}}
    assert clauses(Q.eq(rows, columns) >> Q.symmetric(f(x, rows, columns))) == [
        ((Q.eq, (1, 2), False), (Q.symmetric, -1, True))]
    number, = clauses((Q.eq(base, -1) & Q.even(exponent)) >> Q.positive(f(base, exponent)))
    assert number == ((Q.eq, (0, -1), False), (Q.even, 1, False), (Q.positive, -1, True))
    assert type(number[0][1][0]) is int and type(number[0][1][1]) is not int
    assert _render(number) == (
        '((Q.eq, (0, Integer(-1)), False), (Q.even, 1, False), (Q.positive, EXPR, True))')
    other, = clauses(Q.eq(Rational(1, 2), base) >> Q.positive(f(base, exponent)))
    assert _render(other) == '((Q.eq, (Rational(1, 2), 0), False), (Q.positive, EXPR, True))'
    assert ((Q.positive_definite, 0, False), (Q.eq, (1, 2), False), (Q.positive, -1, True)
            ) in sat_rules(MatrixElement, 3)
    plain, related = split_sat_rules(MatrixElement, 3)
    assert related and all(any(type(slot) is tuple for _, slot, _ in clause) for clause in related)
    assert not any(type(slot) is tuple for clause in plain for _, slot, _ in clause)
    assert set(plain) | set(related) == set(sat_rules(MatrixElement, 3))
    assert (True, ((Q.positive_definite, 0, True), (Q.eq, (1, 2), True))
            ) in ask_rules(MatrixElement, 3, Q.positive)


def test_equal():
    assert equal(a, a) is True
    assert equal(a + 1, a + 1) is True
    assert equal(Tuple(a, 2, 1), Tuple(a, 2, 1)) is True
    assert equal(Integer(1), Integer(2)) is False
    assert equal(Rational(1, 2), Integer(1)) is False
    assert equal(Tuple(0, 2, 1), Tuple(0, 3, 1)) is False
    assert equal(Tuple(0, 2, 1), Tuple(0, 2)) is False
    assert equal(a, b) is None
    assert equal(a, Integer(1)) is None
    assert equal(Tuple(a, 2, 1), Tuple(0, 2, 1)) is None
    assert equal(nan, nan) is None
    assert equal(pi, Integer(3)) is None


def test_relations_evaluated():
    X = MatrixSymbol('X', 4, 4)
    ask = lambda *args: _with_rules([Q.positive], lambda: _ask_recursive(*args))
    assert ask(Q.positive(X[a, a]), Q.positive_definite(X)) is True
    assert ask(Q.positive(X[1, 1]), Q.positive_definite(X)) is True
    assert ask(Q.positive(X[0, 1]), Q.positive_definite(X)) is None
    assert ask(Q.positive(X[a, b]), Q.positive_definite(X)) is None
    assert ask(Q.positive(X[a, b]), Q.positive_definite(X) & Q.eq(a, b)) is True
    assert ask(Q.positive(X[a, b]), Q.positive_definite(X) & Q.eq(b, a)) is True
    assert ask(Q.positive(X[a, b]), Q.positive_definite(X) & ~Q.ne(a, b)) is True
    assert ask(Q.positive(X[a, b]), Q.positive_definite(X) & ~Q.eq(a, b)) is None
    assert ask(Q.positive(X[a, b]), Q.positive_definite(X) & Q.eq(a, c)) is None
    assert ask(Q.positive(X[a, b]),
        Q.positive_definite(X) & (Q.eq(a, b) | Q.eq(a, c)) & Q.eq(a, b)) is True

    class node(Function):
        pass

    rules = compiled_rules.ASK_RULES
    rules[node, 2] = {
        Q.integer: ((True, ((Q.eq, (0, Integer(-1)), True), (Q.integer, 1, True))),),
        Q.zero: ((False, ((Q.eq, (Integer(-1), 1), False),)),),
    }
    try:
        ask = lambda *args: _with_rules(
            [Q.integer, Q.zero], lambda: _ask_recursive(*args))
        assert ask(Q.integer(node(-1, b)), Q.integer(b)) is True
        assert ask(Q.integer(node(1, b)), Q.integer(b)) is None
        assert ask(Q.integer(node(a, b)), Q.integer(b)) is None
        assert ask(Q.integer(node(a, b)), Q.eq(a, -1) & Q.integer(b)) is True
        assert ask(Q.integer(node(a, b)), Q.eq(-1, a) & Q.integer(b)) is True
        assert ask(Q.integer(node(a, b)), ~Q.ne(a, -1) & Q.integer(b)) is True
        assert ask(Q.integer(node(a, b)), Q.ne(a, -1) & Q.integer(b)) is None
        assert ask(Q.zero(node(a, 2)), True) is False
        assert ask(Q.zero(node(a, -1)), True) is None
        assert ask(Q.zero(node(a, b)), True) is None
        assert ask(Q.zero(node(a, b)), Q.ne(b, -1)) is False
        assert ask(Q.zero(node(a, b)), ~Q.eq(-1, b)) is False
        assert ask(Q.zero(node(a, b)), Q.eq(b, -1)) is None
    finally:
        del rules[node, 2]


def test_relations_in_satask():
    X = MatrixSymbol('X', 4, 4)
    assert satask(Q.positive(X[a, b]), Q.positive_definite(X) & Q.eq(a, b)) is True
    assert satask(Q.positive(X[a, b]), Q.positive_definite(X) & Q.eq(b, a)) is True
    assert satask(Q.positive(X[a, b]), Q.positive_definite(X) & ~Q.ne(b, a)) is True
    assert satask(Q.positive(X[a, b]), Q.positive_definite(X)) is None
    assert satask(Q.positive(X[a, a]), Q.positive_definite(X)) is True
    assert satask(Q.positive(X[0, 1]), Q.positive_definite(X)) is None
    assert satask(Q.eq(a, b), Q.positive_definite(X) & ~Q.positive(X[a, b])) is False
    assert satask(Q.symmetric(X[a:a + 2, a:a + 2]), Q.symmetric(X)) is True
    assert satask(Q.symmetric(X[0:2, 1:3]), Q.symmetric(X)) is None

    class node(Function):
        pass

    rules = compiled_rules.SAT_RULES
    rules[node, 2] = (
        ((Q.eq, (0, Integer(-1)), False), (Q.integer, 1, False), (Q.integer, -1, True)),
    )
    try:
        assert satask(Q.integer(node(-1, b)), Q.integer(b)) is True
        assert satask(Q.integer(node(1, b)), Q.integer(b)) is None
        assert satask(Q.integer(node(a, b)), Q.integer(b)) is None
        assert satask(Q.integer(node(a, b)), Q.eq(a, -1) & Q.integer(b)) is True
        assert satask(Q.integer(node(a, b)), Q.eq(-1, a) & Q.integer(b)) is True
        assert satask(Q.integer(node(a, b)), ~Q.ne(a, -1) & Q.integer(b)) is True
    finally:
        del rules[node, 2]


def test_block_diagonal_matrix():
    A, B, C = (MatrixSymbol(name, 3, 3) for name in 'ABC')
    for predicate in (Q.invertible, Q.integer_elements):
        engines = (satask, lambda *args, predicate=predicate: _with_rules(
            [predicate], lambda: _ask_recursive(*args)))
        for blocks in ((A,), (A, B), (A, B, C)):
            matrix = predicate(BlockDiagMatrix(*blocks))
            every = And(*[predicate(block) for block in blocks])
            for engine in engines:
                assert engine(matrix, every) is True
                assert engine(matrix, ~predicate(blocks[-1])) is False
                assert engine(matrix, ~predicate(blocks[0])) is False
                assert engine(matrix, True) is None
                if len(blocks) > 1:
                    assert engine(matrix, predicate(blocks[0])) is None


def test_values_of_entries_and_slices():
    for matrix, slice_rows, slice_columns, value in list(SAMPLES[MatrixSlice]())[::40]:
        assert Basic.__new__(
            MatrixSlice, matrix, slice_rows, slice_columns).as_explicit() == value
    assert untested(MatrixElement, Q.integer_elements(x) >> Q.integer(f(x, i, j))) == []
    assert (ImmutableMatrix([[1, 0], [0, 1]]), 0, 1, 0) in counterexamples(
        MatrixElement, Q.positive_definite(x) >> Q.positive(f(x, i, j)))
    F = f(x, rows, columns)
    assert counterexamples(MatrixSlice, (Q.eq(rows, columns) & Q.symmetric(x)) >> Q.symmetric(F)) == []
    assert (ImmutableMatrix([[0, 1], [1, 0]]), Tuple(0, 1, 1), Tuple(0, 1, 1), ImmutableMatrix([[0]])
            ) in counterexamples(MatrixSlice, (Q.eq(rows, columns) & Q.invertible(x)) >> Q.invertible(F))
    assert (ImmutableMatrix([[1, 2], [0, 3]]), Tuple(1, -1, -1), Tuple(1, -1, -1),
            ImmutableMatrix([[3, 0], [2, 1]])) in counterexamples(
        MatrixSlice, (Q.eq(rows, columns) & Q.upper_triangular(x)) >> Q.upper_triangular(F))
    assert counterexamples(MatrixSlice, Q.symmetric(x) >> Q.symmetric(F))
