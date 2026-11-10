from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

import sympy.assumptions
from sympy.abc import a, b, c, d
from sympy.assumptions import rule_compiler, rule_engine
from sympy.assumptions.ask import Q, _ask_recursive
from sympy.assumptions.assume import AppliedPredicate
from sympy.assumptions.cnf import Literal
from sympy.assumptions.rule_engine import (ask_rules, equal, evaluate,
    greater, not_less, rule_arguments, sat_rules, split_sat_rules)
from sympy.assumptions.facts import get_known_facts
from sympy.assumptions.tests.rule_values import SAMPLES, counterexamples, untested
from sympy.assumptions.rule_compiler import (GENERATED, _render, clauses,
    nargs, statements, ways)
from sympy.assumptions.rule_language import (ORDERS, WRITTEN, base, closed,
    columns, exponent, f, for_all, i, j, node, rows, x, y)
from sympy.assumptions.satask import _relations, get_relevant_clsfacts, satask
from sympy.core.add import Add
from sympy.core.basic import Basic
from sympy.core.containers import Tuple
from sympy.core.expr import Expr
from sympy.core.function import Function
from sympy.core.mul import Mul
from sympy.core.numbers import I, ImaginaryUnit, Integer, Rational, nan, oo, pi, zoo
from sympy.core.symbol import Symbol
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.exponential import log
from sympy.functions.elementary.trigonometric import acos, cos, sin
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
    class node(Function):
        pass

    class subnode(node):
        pass

    with installed(for_all((node,), Q.even(x) >> Q.even(f(x))),
                   for_all((subnode,), Q.odd(x) >> Q.odd(f(x)))):
        assert ((Q.even, 0, False), (Q.even, -1, True)) in sat_rules(node, 1)
        assert sat_rules(node, 2) == ()
        assert sat_rules(Function('g'), 1) == ()
        # a class has the rules of the classes it derives from
        assert set(sat_rules(node, 1)) < set(sat_rules(subnode, 1))


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
    class node(Function):
        pass

    class subnode(node):
        pass

    with installed(for_all((node,), Q.even(x) >> Q.even(f(x)), Q.odd(x) >> Q.odd(f(x)),
                           (Q.integer(x) & ~Q.integer(y)) >> ~Q.even(f(x, y))),
                   for_all((subnode,), Q.zero(x) >> Q.zero(f(x)))):
        assert (True, ((Q.even, 0, True),)) in ask_rules(node, 1, Q.even)
        # a way to find that the expression is odd shows that it is not even
        assert (False, ((Q.odd, 0, True),)) in ask_rules(node, 1, Q.even)
        assert (False, ((Q.integer, 0, True), (Q.integer, 1, False))) in ask_rules(node, 2, Q.even)
        # without rows for a class, the ways are not about arguments
        assert all(slot == -1 for _, conditions in ask_rules(node, 3, Q.even)
                   for _, slot, _ in conditions)
        assert all(slot == -1 for _, conditions in ask_rules(Function('g'), 1, Q.even)
                   for _, slot, _ in conditions)
        assert set(ask_rules(node, 1, Q.even)) <= set(ask_rules(subnode, 1, Q.even))
        assert (True, ((Q.zero, 0, True),)) in ask_rules(subnode, 1, Q.zero)
        assert (True, ((Q.zero, 0, True),)) not in ask_rules(node, 1, Q.zero)


@contextmanager
def installed(*written):
    sat = {key: tuple(clause for _, row_clauses in found for clause in row_clauses)
           for key, found in rule_compiler.sat_rules(written).items()}
    ask = rule_compiler.ask_rules(written)
    saved = dict(rule_engine.SAT_RULES), dict(rule_engine.ASK_RULES)
    rule_engine.SAT_RULES.update(sat)
    rule_engine.ASK_RULES.update(ask)
    _clear_caches()
    try:
        yield
    finally:
        for table, old in zip((rule_engine.SAT_RULES, rule_engine.ASK_RULES), saved):
            table.clear()
            table.update(old)
        _clear_caches()


def _clear_caches():
    for cache in (rule_engine._sat_rules, rule_engine._ask_rules,
                  rule_engine._known_classes, rule_engine._symbols_unknown):
        cache.clear()


@contextmanager
def answered_by_rules(*predicates):
    saved = rule_engine.RULE_PREDICATES
    rule_engine.RULE_PREDICATES = frozenset(predicates)
    try:
        yield
    finally:
        rule_engine.RULE_PREDICATES = saved


def _with_rules(predicates, function):
    with answered_by_rules(*predicates):
        return function()


class power(Function):
    pass


class logarithm(Function):
    pass


class arccosine(Function):
    pass


POWER = for_all((power,),
    (Q.gt(base, 1) & Q.extended_negative(exponent)) >> Q.finite(f(base, exponent)),
    (Q.eq(base, 1) & Q.rational(exponent)) >> Q.rational(f(base, exponent)),
    (Q.eq(base, 1) & Q.integer(exponent)) >> Q.odd(f(base, exponent)),
    (Q.eq(base, -1) & Q.integer(exponent)) >> Q.odd(f(base, exponent)),
    (Q.odd(base) & Q.integer(exponent) & Q.nonnegative(exponent)) >> Q.odd(f(base, exponent)),
    (Q.gt(base, 1) & Q.integer(exponent) & Q.negative(exponent)) >> ~Q.odd(f(base, exponent)),
    (Q.eq(exponent, 1) & Q.odd(base)) >> Q.odd(f(base, exponent)),
    (Q.integer(base) & Q.integer(exponent) & Q.ne(exponent, 1)) >> ~Q.prime(f(base, exponent)))
LOGARITHM = for_all((logarithm,),
    (Q.real(x) & Q.gt(x, 1)) >> Q.positive(f(x)),
    Q.lt(x, 1) >> ~Q.positive(f(x)),
    (Q.rational(x) & Q.ne(x, 1)) >> ~Q.rational(f(x)))
ARCCOSINE = for_all((arccosine,),
    (Q.ge(x, -1) & Q.lt(x, 1)) >> Q.positive(f(x)))
ENTRY = for_all((MatrixElement,),
    (Q.positive_definite(x) & Q.eq(i, j)) >> Q.positive(f(x, i, j)),
    Q.integer_elements(x) >> Q.integer(f(x, i, j)))
SLICE = for_all((MatrixSlice,),
    (Q.eq(rows, columns) & Q.symmetric(x)) >> Q.symmetric(f(x, rows, columns)))
BLOCKS = for_all((BlockDiagMatrix,),
    Equivalent(Q.invertible(f(x)), Q.invertible(x)),
    Equivalent(Q.invertible(f(x, y)), Q.invertible(x) & Q.invertible(y)),
    Equivalent(Q.integer_elements(f(x)), Q.integer_elements(x)),
    Equivalent(Q.integer_elements(f(x, y)),
        Q.integer_elements(x) & Q.integer_elements(y)))


def test_evaluate():
    assert evaluate(Q.real, (a,), Q.positive(a)) is True
    assert evaluate(Q.real, (a,), ~Q.complex(a)) is False
    assert evaluate(Q.real, (a,), Q.positive(b)) is None
    assert evaluate(Q.real, (a,), Q.positive(a) | Q.negative(a)) is None
    assert evaluate(Q.real, (a,), ~(Q.complex(a) | Q.zero(b))) is False

    class node(Function):
        pass

    rules = rule_engine.ASK_RULES
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
        saved = rules.get((Add, 2))
        rules[Add, 2] = rules[node, 2]
        rule_engine._ask_rules.clear()
        try:
            assert ask(Q.integer(a + b + c + d),
                Q.integer(a) & Q.integer(b) & Q.integer(c) & Q.integer(d)) is True
        finally:
            if saved is None:
                del rules[Add, 2]
            else:
                rules[Add, 2] = saved
            rule_engine._ask_rules.clear()
    finally:
        del rules[node, 2]


def test_evaluate_one_expression():
    rules = rule_engine.ASK_RULES
    saved = rules.get((Expr, None))
    rules[Expr, None] = {
        Q.irrational: ((True, ((Q.real, -1, True), (Q.rational, -1, False))),),
    }
    rule_engine._ask_rules.clear()
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
        rule_engine._ask_rules.clear()


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

    has_handler = rule_engine._has_handler
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

    rules = rule_engine.ASK_RULES
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
    assert node(Q.ne(i, j) >> Q.positive(f(x, i, j))) == f(x, i, j)
    assert node(Q.ne(base, 1) >> Q.positive(f(base, exponent))) == f(base, exponent)
    assert node(Q.eq(base, I) >> Q.positive(f(base, exponent))) == f(base, exponent)
    assert node(Q.ne(-I, base) >> Q.positive(f(base, exponent))) == f(base, exponent)
    for relation in (Q.gt, Q.lt, Q.ge, Q.le):
        assert node(relation(i, j) >> Q.positive(f(x, i, j))) == f(x, i, j)
        assert node(relation(base, Rational(1, 2)) >> Q.positive(f(base, exponent))) == f(base, exponent)
        assert node(relation(-1, base) >> Q.positive(f(base, exponent))) == f(base, exponent)
        raises(ValueError, lambda: node(relation(base, I) >> Q.positive(f(base, exponent))))
        raises(ValueError, lambda: node(relation(-I, base) >> Q.positive(f(base, exponent))))
        raises(ValueError, lambda: node(relation(base, pi) >> Q.positive(f(base, exponent))))
        raises(ValueError, lambda: node(relation(base, base) >> Q.positive(f(base, exponent))))
        raises(ValueError, lambda: node(relation(1, 2) >> Q.positive(f(base, exponent))))
    raises(ValueError, lambda: node(AppliedPredicate(Q.integer, i, j) >> Q.positive(f(x, i, j))))
    raises(ValueError, lambda: node(Q.eq(I, -I) >> Q.positive(f(x, i, j))))
    raises(ValueError, lambda: node(Q.eq(i, 2*I) >> Q.positive(f(x, i, j))))
    raises(ValueError, lambda: node(Q.eq(i, i) >> Q.positive(f(x, i, j))))
    raises(ValueError, lambda: node(Q.ne(i, i) >> Q.positive(f(x, i, j))))
    raises(ValueError, lambda: node(Q.ne(1, 2) >> Q.positive(f(x, i, j))))
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
    # Q.ne is the negation of Q.eq
    assert clauses((Q.ne(base, -1) & Q.even(exponent)) >> Q.positive(f(base, exponent))) == [
        ((Q.eq, (0, Integer(-1)), True), (Q.even, 1, False), (Q.positive, -1, True))]
    assert clauses(Q.ne(i, j) >> Q.positive(f(x, i, j))) == clauses(
        ~Q.eq(i, j) >> Q.positive(f(x, i, j)))
    assert ways(Q.ne(rows, columns) >> ~Q.symmetric(f(x, rows, columns))) == {
        Q.symmetric: {(False, ((Q.eq, (1, 2), False),))}}
    other, = clauses(Q.eq(Rational(1, 2), base) >> Q.positive(f(base, exponent)))
    assert _render(other) == '((Q.eq, (Rational(1, 2), 0), False), (Q.positive, EXPR, True))'


def test_relations_compiled_rules():
    plain_row = Q.integer_elements(x) >> Q.integer(f(x, i, j))
    with installed(ENTRY):
        assert ((Q.positive_definite, 0, False), (Q.eq, (1, 2), False), (Q.positive, -1, True)
                ) in sat_rules(MatrixElement, 3)
        plain, related = split_sat_rules(MatrixElement, 3)
        assert plain == tuple(clauses(plain_row))
        assert related and all(any(type(slot) is tuple for _, slot, _ in clause)
                               for clause in related)
        assert set(plain) | set(related) == set(sat_rules(MatrixElement, 3))
        assert (True, ((Q.positive_definite, 0, True), (Q.eq, (1, 2), True))
                ) in ask_rules(MatrixElement, 3, Q.positive)


def test_relations_by_size_compiled():
    F = f(base, exponent)
    assert clauses(Q.gt(base, 1) >> Q.finite(F)) == [
        ((Q.gt, (0, Integer(1)), False), (Q.finite, -1, True))]
    assert clauses(Q.lt(base, 1) >> Q.finite(F)) == [
        ((Q.gt, (Integer(1), 0), False), (Q.finite, -1, True))]
    assert clauses(Q.lt(1, base) >> Q.finite(F)) == clauses(Q.gt(base, 1) >> Q.finite(F))
    assert clauses(Q.ge(base, -1) >> Q.finite(F)) == [
        ((Q.ge, (0, Integer(-1)), False), (Q.finite, -1, True))]
    assert clauses(Q.le(base, -1) >> Q.finite(F)) == [
        ((Q.ge, (Integer(-1), 0), False), (Q.finite, -1, True))]
    assert clauses(Q.gt(base, exponent) >> Q.finite(F)) == [
        ((Q.gt, (0, 1), False), (Q.finite, -1, True))]
    swapped, = clauses((Q.lt(base, 1) & Q.real(exponent)) >> Q.finite(F))
    assert _render(swapped) == (
        '((Q.real, 1, False), (Q.gt, (Integer(1), 0), False), (Q.finite, EXPR, True))')
    unit, = clauses(Q.eq(base, I) >> Q.positive(F))
    assert _render(unit) == '((Q.eq, (0, I), False), (Q.positive, EXPR, True))'
    unit, = clauses(Q.ne(base, -I) >> Q.positive(F))
    assert _render(unit) == '((Q.eq, (0, -I), True), (Q.positive, EXPR, True))'
    # literals with I and with rational numbers can be sorted
    assert clauses((Q.eq(base, I) & Q.eq(base, 1)) >> Q.positive(F)) == [
        ((Q.eq, (0, Integer(1)), False), (Q.eq, (0, I), False), (Q.positive, -1, True))]
    assert ways(Q.lt(base, 1) >> Q.finite(F)) == {
        Q.finite: {(True, ((Q.gt, (Integer(1), 0), True),))}}
    # a comparison by size is only a condition
    raises(ValueError, lambda: clauses(Q.finite(F) >> Q.gt(base, 1)))
    raises(ValueError, lambda: clauses(~Q.lt(base, 1) >> Q.finite(F)))
    raises(ValueError, lambda: clauses(Equivalent(Q.ge(base, 1), Q.finite(F))))
    assert clauses(Q.finite(F) >> Q.eq(base, 1))
    assert clauses(Q.finite(F) >> Q.ne(base, I))


def test_written_relations_agree():
    assert WRITTEN == rule_engine.WRITTEN
    assert set(rule_engine.RELATIONS) == {
        relation for relation, _, _ in WRITTEN.values()}
    assert ORDERS < set(rule_engine.RELATIONS)


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
    assert equal(pi, Integer(3)) is False
    assert equal(Integer(1), pi) is False
    assert equal(pi, oo) is False
    assert equal(pi, I) is None
    assert equal(pi, 2*I) is None
    assert equal(I, I) is True
    assert equal(-I, -I) is True
    assert equal(I, -I) is False
    assert equal(I, Integer(1)) is False
    assert equal(Integer(0), -I) is False
    assert equal(a, I) is None
    assert equal(-I, a) is None
    assert equal(2*I, I) is None


def test_greater():
    one, two, half = Integer(1), Integer(2), Rational(1, 2)
    assert greater(two, one) is True
    assert greater(one, one) is False
    assert greater(half, Rational(-1, 2)) is True
    assert greater(Rational(-3, 2), Integer(-1)) is False
    assert not_less(one, one) is True
    assert not_less(half, one) is False
    assert not_less(Rational(2, 4), half) is True
    assert greater(pi, one) is True
    assert greater(one, pi) is False
    assert greater(oo, one) is True
    assert not_less(oo, oo) is True
    assert greater(-oo, Integer(-1)) is False
    assert greater(I, one) is False
    assert not_less(one, I) is False
    assert greater(zoo, one) is False
    assert greater(a, one) is None
    assert not_less(one, a) is None
    assert greater(a, b) is None
    assert greater(nan, one) is None
    assert greater(Tuple(0, 2, 1), one) is None
    assert type(greater(two, one)) is bool and type(greater(pi, one)) is bool


def test_relations_evaluated():
    X = MatrixSymbol('X', 4, 4)
    ask = lambda *args: _with_rules([Q.positive], lambda: _ask_recursive(*args))
    with installed(ENTRY):
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
    with installed(for_all((power,),
            (Q.eq(base, -1) & Q.integer(exponent)) >> Q.integer(f(base, exponent)),
            Q.ne(exponent, -1) >> ~Q.zero(f(base, exponent)))):
        ask = lambda *args: _with_rules(
            [Q.integer, Q.zero], lambda: _ask_recursive(*args))
        assert ask(Q.integer(power(-1, b)), Q.integer(b)) is True
        assert ask(Q.integer(power(1, b)), Q.integer(b)) is None
        assert ask(Q.integer(power(a, b)), Q.integer(b)) is None
        assert ask(Q.integer(power(a, b)), Q.eq(a, -1) & Q.integer(b)) is True
        assert ask(Q.integer(power(a, b)), Q.eq(-1, a) & Q.integer(b)) is True
        assert ask(Q.integer(power(a, b)), ~Q.ne(a, -1) & Q.integer(b)) is True
        assert ask(Q.integer(power(a, b)), Q.ne(a, -1) & Q.integer(b)) is None
        assert ask(Q.zero(power(a, 2)), True) is False
        assert ask(Q.zero(power(a, -1)), True) is None
        assert ask(Q.zero(power(a, b)), True) is None
        assert ask(Q.zero(power(a, b)), Q.ne(b, -1)) is False
        assert ask(Q.zero(power(a, b)), ~Q.eq(-1, b)) is False
        assert ask(Q.zero(power(a, b)), Q.eq(b, -1)) is None


def test_relations_by_size_evaluated():
    rules = rule_engine.ASK_RULES

    def integer(condition, *args, assumptions=True):
        class node(Function):
            pass

        rules[node, 2] = {Q.integer: ((True, (condition,)),)}
        try:
            return _with_rules([Q.integer], lambda: _ask_recursive(
                Q.integer(node(*args)), assumptions))
        finally:
            del rules[node, 2]

    gt, ge, ne = (Q.gt, (0, 1), True), (Q.ge, (0, 1), True), (Q.eq, (0, 1), False)
    assert integer(gt, a, b, assumptions=Q.gt(a, b)) is True
    assert integer(gt, a, b, assumptions=Q.lt(b, a)) is True
    assert integer(gt, a, b, assumptions=~Q.le(a, b)) is None
    assert integer(gt, a, b, assumptions=Q.ge(a, b)) is None
    assert integer(gt, a, b, assumptions=Q.gt(b, a)) is None
    assert integer(gt, 2, 1) is True
    assert integer(gt, pi, 3) is True
    assert integer(gt, I, 1) is None
    assert integer(ge, a, b, assumptions=Q.ge(a, b)) is True
    assert integer(ge, a, b, assumptions=Q.le(b, a)) is True
    assert integer(ge, a, b, assumptions=Q.gt(a, b)) is True
    assert integer(ge, a, b, assumptions=Q.eq(a, b)) is None
    assert integer(ge, a, b, assumptions=~Q.lt(a, b)) is None
    assert integer(ge, 1, 1) is True
    assert integer(ne, a, b, assumptions=Q.gt(a, b)) is True
    assert integer(ne, a, b, assumptions=Q.lt(a, b)) is True
    assert integer(ne, a, b, assumptions=Q.ne(b, a)) is True
    assert integer(ne, a, b, assumptions=~Q.ge(a, b)) is None
    assert integer(ne, a, b, assumptions=Q.ge(a, b)) is None
    number = (Q.gt, (0, Integer(1)), True)
    assert integer(number, a, b, assumptions=Q.gt(a, 1)) is True
    assert integer(number, a, b, assumptions=Q.lt(1, a)) is True
    assert integer(number, a, b, assumptions=Q.ge(a, 1)) is None
    assert integer(number, a, b, assumptions=Q.gt(a, 2)) is None
    assert integer(number, a, b, assumptions=Q.gt(b, 1)) is None
    assert integer(number, oo, b) is True
    assert integer(number, Rational(1, 2), b) is None


def test_relations_assumed():
    _, relations = rule_engine._unit_assumptions(
        Q.eq(a, b) & Q.ne(a, 1) & Q.lt(a, 2) & ~Q.le(b, 3) & Q.ge(c, d) & ~Q.gt(c, 0))
    assert relations == {
        (Q.eq, a, b): True, (Q.eq, a, 1): False, (Q.gt, 2, a): True,
        (Q.ge, 3, b): False, (Q.ge, c, d): True, (Q.gt, c, 0): False}
    assert rule_engine.canonical(Q.le, a, 1) == ((Q.ge, 1, a), True)
    query = rule_engine._Query(Q.gt(a, 1) & Q.integer(b))
    assert query.related == {a, Integer(1)}
    assert not rule_engine._Query(Q.integer(b)).related


def test_relations_decided_once():
    n = Symbol('n')
    with installed(POWER), answered_by_rules(Q.odd, Q.integer, Q.prime, Q.nonnegative):
        query = rule_engine._Query(Q.integer(n), power(-1, n))
        assert query.ask_about(Q.odd, power(-1, n)) is True
        _, plain, related, decided, groups, count = rule_engine._ways(power, 2, Q.odd)
        assert count == sum(len(group[1]) for group in groups)
        assert {group[0] for group in groups} == {0, 1}
        slots = {index: (decide, pair) for group in groups
                 for index, pair, decide, _ in group[1]}
        truths = {slots[index]: truth
                  for index, truth in enumerate(query.truths[power(-1, n)])}
        assert truths[equal, (0, Integer(-1))] is True
        assert truths[equal, (0, Integer(1))] is False
        assert truths[greater, (0, Integer(1))] is False
        assert truths[equal, (1, Integer(1))] is None
        assert (True, ((Q.integer, 1, True),)) in rule_engine._decided_ways(
            related, query.truths[power(-1, n)])
        assert (True, ((Q.integer, 1, True),)) not in plain
        # the conditions between two arguments are found only when the other
        # ways give no answer
        query = rule_engine._Query(Q.odd(a) & Q.integer(b) & Q.nonnegative(b))
        assert query.ask_about(Q.odd, power(a, b)) is True
        assert power(a, b) not in query.truths

        query = rule_engine._Query(Q.integer(a) & Q.integer(b))
        assert query.ask_about(Q.odd, power(a, b)) is None
        assert set(query.truths[power(a, b)]) == {None}
        assert decided[query.truths[power(a, b)]] == ()

        query = rule_engine._Query(Q.integer(a) & Q.integer(b) & Q.ne(b, 1))
        assert query.ask_about(Q.prime, power(a, b)) is False
        _, _, _, _, groups, _ = rule_engine._ways(power, 2, Q.prime)
        slots = {index: (decide, pair) for group in groups
                 for index, pair, decide, _ in group[1]}
        truths = {slots[index]: truth
                  for index, truth in enumerate(query.truths[power(a, b)])}
        assert truths[equal, (1, Integer(1))] is False


def test_relations_kept_in_satask():
    eq = Q.eq(a, Integer(1))
    gt = Q.gt(a, Integer(1))
    facts = lambda *atoms: {literal.lit for clause in get_relevant_clsfacts(
        {power(a, b), logarithm(a)}, relations=_relations(atoms))[1].clauses
        for literal in clause}
    assert _relations([Q.eq(a, 1), Q.integer(a)]) == {(Q.eq, a, 1): set()}
    assert _relations([Q.lt(1, a)]) == {(Q.gt, a, 1): {
        frozenset((Literal(Q.lt(1, a), True), Literal(gt, False))),
        frozenset((Literal(Q.lt(1, a), False), Literal(gt, True)))}}
    with installed(POWER, LOGARITHM, ARCCOSINE):
        assert eq not in facts()
        assert eq not in facts(Q.eq(a, c))
        assert eq in facts(Q.eq(a, 1))
        assert eq in facts(Q.ne(1, a))
        assert Q.eq(1, a) in facts(Q.eq(1, a))
        assert eq in facts(Q.gt(a, 1))
        assert gt in facts(Q.gt(a, 1)) and gt in facts(Q.lt(1, a))
        assert Q.lt(1, a) in facts(Q.lt(1, a))
        assert gt not in facts(Q.ge(a, 1))
        assert gt not in facts(Q.gt(1, a))
        # without predicates of two expressions, no relation is kept
        assert not any(len(literal.lit.arguments) == 2 for clause in
                       get_relevant_clsfacts({power(a, b), logarithm(a), arccosine(a)})[1].clauses
                       for literal in clause)
        assert satask(Q.finite(power(a, b)), Q.lt(1, a) & Q.extended_negative(b)) is True
        assert satask(Q.finite(power(a, b)), Q.gt(a, 1) & Q.extended_negative(b)) is True
        assert satask(Q.finite(power(a, b)), ~Q.le(a, 1) & Q.extended_negative(b)) is None
        assert satask(Q.finite(power(a, b)), Q.ge(a, 1) & Q.extended_negative(b)) is None
        assert satask(Q.positive(arccosine(a)), Q.le(-1, a) & Q.gt(1, a)) is True
        assert satask(Q.lt(a, 1), Q.positive(logarithm(a))) is False
        assert satask(Q.prime(power(a, b)), Q.integer(a) & Q.integer(b) & Q.gt(b, 1)) is False
        assert satask(Q.rational(power(a, b)), Q.rational(b) & Q.eq(a, 1)) is True
        assert satask(Q.rational(power(a, b)), Q.rational(b) & Q.eq(1, a)) is True
        assert satask(Q.rational(power(a, b)), Q.rational(b) & ~Q.ne(a, 1)) is True
        assert satask(Q.rational(power(a, b)), Q.rational(b)) is None
        assert satask(Q.eq(a, 1), Q.integer(b) & Q.even(power(a, b))) is False
        assert satask(Q.prime(power(a, b)), Q.integer(a) & Q.integer(b) & Q.ne(b, 1)) is False


def test_relations_stated_by_sums():
    stated = rule_engine.stated_comparisons
    one, minus_one = Integer(1), Integer(-1)
    assert stated(Q.zero(a - 1)) == ((True, (Q.eq, a, one), True), (False, (Q.eq, a, one), False))
    assert stated(Q.nonzero(a - 1)) == ((True, (Q.eq, a, one), False),)
    assert stated(Q.positive(a - 1)) == ((True, (Q.gt, a, one), True),)
    assert stated(Q.negative(a + 1)) == ((True, (Q.gt, minus_one, a), True),)
    assert stated(Q.nonnegative(a + Rational(1, 2))) == (
        (True, (Q.ge, a, Rational(-1, 2)), True),)
    assert stated(Q.nonpositive(a - 1)) == ((True, (Q.ge, one, a), True),)
    for atom in (Q.real(a - 1), Q.positive(a + b), Q.positive(a + b + 1),
                 Q.positive(a - pi), Q.positive(a), Q.positive(2*a)):
        assert stated(atom) == ()

    def relations(assumptions):
        return rule_engine._unit_assumptions(assumptions)[1]

    assert relations(Q.zero(a - 1)) == {(Q.eq, a, one): True}
    assert relations(~Q.zero(a - 1)) == {(Q.eq, a, one): False}
    assert relations(Q.nonzero(a - 1)) == {(Q.eq, a, one): False}
    assert relations(Q.positive(a - 1)) == {(Q.gt, a, one): True}
    assert relations(Q.negative(a - 1)) == {(Q.gt, one, a): True}
    assert relations(Q.nonnegative(a - 1)) == {(Q.ge, a, one): True}
    assert relations(Q.nonpositive(a - 1)) == {(Q.ge, one, a): True}
    assert relations(~Q.positive(a - 1)) == {}
    assert relations(~Q.nonzero(a - 1)) == {}
    assert relations(Q.positive(a + b + 1)) == {}
    assert relations(Q.positive(a + b)) == {}

    gt = Q.gt(a, one)
    assert _relations([Q.positive(a - 1)]) == {(Q.gt, a, one): {
        frozenset((Literal(Q.positive(a - 1), True), Literal(gt, False)))}}
    assert _relations([Q.zero(a - 1)]) == {(Q.eq, a, one): {
        frozenset((Literal(Q.zero(a - 1), True), Literal(Q.eq(a, one), False))),
        frozenset((Literal(Q.zero(a - 1), False), Literal(Q.eq(a, one), True)))}}
    assert _relations([Q.real(a - 1), Q.positive(a + b + 1)]) == {}


def test_relations_stated_by_sums_compiled():
    gt = Q.gt(a, Integer(1))
    facts = lambda exprs, *atoms: {literal.lit for clause in get_relevant_clsfacts(
        exprs, relations=_relations(atoms))[1].clauses for literal in clause}
    with installed(POWER, LOGARITHM, ARCCOSINE):
        # the comparison is added to the facts only when a rule uses it
        assert gt in facts({power(a, b)}, Q.positive(a - 1))
        assert gt not in facts({sin(a)}, Q.positive(a - 1))
        assert Q.eq(a, 1) not in facts({sin(a)}, Q.nonzero(a - 1))
        assert not any(len(lit.arguments) == 2 for lit in facts({sin(a)}, Q.nonzero(a - 1)))

        ask = lambda *args: _with_rules(
            [Q.positive, Q.rational, Q.finite], lambda: _ask_recursive(*args))
        for engine in (satask, ask):
            assert engine(Q.positive(logarithm(a)), Q.real(a) & Q.positive(a - 1)) is True
            assert engine(Q.positive(logarithm(a)), Q.real(a) & ~Q.nonpositive(a - 1)) is None
            assert engine(Q.positive(logarithm(a)), Q.real(a) & Q.negative(a - 1)) is False
            assert engine(Q.positive(arccosine(a)),
                          Q.negative(a - 1) & Q.nonnegative(a + 1)) is True
            assert engine(Q.positive(arccosine(a)),
                          Q.nonpositive(a - 1) & Q.nonnegative(a + 1)) is None
            assert engine(Q.rational(logarithm(a)), Q.rational(a) & Q.nonzero(a - 1)) is False
            assert engine(Q.rational(logarithm(a)), Q.rational(a) & ~Q.zero(a - 1)) is False
            assert engine(Q.rational(logarithm(a)), Q.rational(a) & ~Q.zero(a - 2)) is None
            assert engine(Q.finite(power(b, a)),
                          Q.positive(b - 1) & Q.extended_negative(a)) is True


def test_relations_in_satask():
    X = MatrixSymbol('X', 4, 4)
    with installed(ENTRY, SLICE):
        assert satask(Q.positive(X[a, b]), Q.positive_definite(X) & Q.eq(a, b)) is True
        assert satask(Q.positive(X[a, b]), Q.positive_definite(X) & Q.eq(b, a)) is True
        assert satask(Q.positive(X[a, b]), Q.positive_definite(X) & ~Q.ne(b, a)) is True
        assert satask(Q.positive(X[a, b]), Q.positive_definite(X)) is None
        assert satask(Q.positive(X[a, a]), Q.positive_definite(X)) is True
        assert satask(Q.positive(X[0, 1]), Q.positive_definite(X)) is None
        assert satask(Q.eq(a, b), Q.positive_definite(X) & ~Q.positive(X[a, b])) is False
        assert satask(Q.symmetric(X[a:a + 2, a:a + 2]), Q.symmetric(X)) is True
        assert satask(Q.symmetric(X[0:2, 1:3]), Q.symmetric(X)) is None
    with installed(for_all((power,),
            (Q.eq(base, -1) & Q.integer(exponent)) >> Q.integer(f(base, exponent)))):
        assert satask(Q.integer(power(-1, b)), Q.integer(b)) is True
        assert satask(Q.integer(power(1, b)), Q.integer(b)) is None
        assert satask(Q.integer(power(a, b)), Q.integer(b)) is None
        assert satask(Q.integer(power(a, b)), Q.eq(a, -1) & Q.integer(b)) is True
        assert satask(Q.integer(power(a, b)), Q.eq(-1, a) & Q.integer(b)) is True
        assert satask(Q.integer(power(a, b)), ~Q.ne(a, -1) & Q.integer(b)) is True


def test_block_diagonal_matrix():
    A, B, C = (MatrixSymbol(name, 3, 3) for name in 'ABC')
    with installed(BLOCKS):
        for predicate in (Q.invertible, Q.integer_elements):
            for blocks in ((A,), (A, B), (A, B, C)):
                matrix = predicate(BlockDiagMatrix(*blocks))
                every = And(*[predicate(block) for block in blocks])
                assert satask(matrix, every) is True
                assert satask(matrix, ~predicate(blocks[-1])) is False
                assert satask(matrix, ~predicate(blocks[0])) is False
                assert satask(matrix, True) is None
                if len(blocks) > 1:
                    assert satask(matrix, predicate(blocks[0])) is None


def test_compiled_rules_of_classes():
    assert ((Q.even, 0, False), (Q.even, -1, True)) in sat_rules(Abs, 1)
    assert sat_rules(Abs, 2) == ()
    assert set(sat_rules(Mul, 2)) < set(sat_rules(MatMul, 2))
    assert (True, ((Q.even, 0, True),)) in ask_rules(Abs, 1, Q.even)
    # an odd number is not even, and zero is even
    assert (False, ((Q.odd, 0, True),)) in ask_rules(Abs, 1, Q.even)
    assert (True, ((Q.zero, 0, True),)) in ask_rules(Abs, 1, Q.even)
    # a number which is not an integer is not even
    assert (False, ((Q.integer, 0, False), (Q.integer, 1, True))) in ask_rules(Add, 2, Q.even)
    assert set(ask_rules(Mul, 2, Q.zero)) <= set(ask_rules(MatMul, 2, Q.zero))
    assert (True, ((Q.positive_definite, 0, True), (Q.eq, (1, 2), True))
            ) in ask_rules(MatrixElement, 3, Q.positive)


def test_rules_with_relations_in_use():
    X = MatrixSymbol('X', 4, 4)
    for engine in (satask, _ask_recursive):
        assert engine(Q.positive(X[a, a]), Q.positive_definite(X)) is True
        assert engine(Q.positive(X[a, b]), Q.positive_definite(X) & Q.eq(a, b)) is True
        assert engine(Q.positive(X[a, b]), Q.positive_definite(X)) is None
        assert engine(Q.finite(a**b), Q.lt(1, a) & Q.extended_negative(b)) is True
        assert engine(Q.finite(a**b), Q.ge(a, 1) & Q.extended_negative(b)) is None
        assert engine(Q.positive(acos(a)), Q.le(-1, a) & Q.gt(1, a)) is True
        assert engine(Q.rational(a**b), Q.rational(b) & Q.eq(a, 1)) is True
        assert engine(Q.prime(a**b), Q.integer(a) & Q.integer(b) & Q.ne(b, 1)) is False
        assert engine(Q.positive(log(a)), Q.real(a) & Q.positive(a - 1)) is True
        assert engine(Q.positive(log(a)), Q.real(a) & Q.negative(a - 1)) is False
        assert engine(Q.positive(acos(a)), Q.negative(a - 1) & Q.nonnegative(a + 1)) is True
        assert engine(Q.positive(acos(a)), Q.nonpositive(a - 1) & Q.nonnegative(a + 1)) is None
        assert engine(Q.rational(log(a)), Q.rational(a) & Q.nonzero(a - 1)) is False
        assert engine(Q.finite(b**a), Q.positive(b - 1) & Q.extended_negative(a)) is True
    assert satask(Q.lt(a, 1), Q.positive(log(a))) is False
    assert _ask_recursive(Q.odd((-1)**Symbol('n')), Q.integer(Symbol('n'))) is True


def test_block_diagonal_matrix_in_use():
    A, B, C = (MatrixSymbol(name, 3, 3) for name in 'ABC')
    for predicate in (Q.invertible, Q.integer_elements):
        for blocks in ((A,), (A, B), (A, B, C)):
            matrix = predicate(BlockDiagMatrix(*blocks))
            every = And(*[predicate(block) for block in blocks])
            for engine in (satask, _ask_recursive):
                assert engine(matrix, every) is True
                assert engine(matrix, ~predicate(blocks[-1])) is False
                assert engine(matrix, True) is None


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

