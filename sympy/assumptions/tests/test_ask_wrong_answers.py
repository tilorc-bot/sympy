"""Wrong answers of ask which the rules do not give."""
from __future__ import annotations

from sympy.abc import n, x, y, z
from sympy.assumptions.ask import Q, ask
from sympy.assumptions.ask_rules_generated import RULES
from sympy.assumptions.rule_engine import ask_by_rules
from sympy.core.numbers import I, oo, pi
from sympy.core.symbol import Symbol
from sympy.functions.elementary.complexes import Abs, im, re
from sympy.functions.elementary.exponential import exp, log
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.functions.elementary.trigonometric import acos, acot, cos, sin
from sympy.matrices.expressions.matexpr import MatrixSymbol
from sympy.matrices.immutable import ImmutableMatrix

A = MatrixSymbol('A', Symbol('n', integer=True), Symbol('m', integer=True))
X = MatrixSymbol('X', 2, 2)
Z = MatrixSymbol('Z', 2, 2)
W = MatrixSymbol('W', 4, 4)

# (query, assumptions, the answer of ask, values at which that answer is wrong)
WRONG_ANSWERS = [
    # a factor or a term may be zero
    (Q.imaginary(x*y), Q.imaginary(x) & Q.real(y), True, {x: I, y: 0}),
    (Q.imaginary(I*x), Q.real(x), True, {x: 0}),
    (Q.imaginary(x + I), Q.real(x), False, {x: 0}),
    (Q.imaginary(x + y), Q.imaginary(x) & Q.real(y), False, {x: I, y: 0}),
    (Q.imaginary(x + y + z), Q.real(x) & Q.imaginary(y) & Q.imaginary(z), False,
        {x: 0, y: I, z: I}),
    (Q.antihermitian(x), Q.real(x), False, {x: 0}),
    (Q.antihermitian(I*x), Q.antihermitian(x), False, {x: 0}),
    (Q.antihermitian(x + I), Q.real(x), False, {x: 0}),
    (Q.antihermitian(x + y), Q.antihermitian(x) & Q.real(y), False, {x: 0, y: 0}),
    (Q.antihermitian(x + y), Q.imaginary(x) & Q.real(y), False, {x: I, y: 0}),
    (Q.antihermitian(x + y + z), Q.real(x) & Q.imaginary(y) & Q.imaginary(z), False,
        {x: 0, y: I, z: I}),
    (Q.hermitian(I*x), Q.hermitian(x), False, {x: 0}),
    (Q.hermitian(I*x), Q.real(x), False, {x: 0}),
    (Q.hermitian(x*y), Q.real(x) & Q.zero(y), False, {x: 1, y: 0}),
    (Q.extended_real(x*y), Q.imaginary(x) & Q.zero(y), False, {x: I, y: 0}),
    (Q.rational(x*y), Q.irrational(x) & Q.zero(y), False, {x: sqrt(2), y: 0}),
    (Q.irrational(x*y), Q.zero(x) & Q.irrational(y), True, {x: 0, y: sqrt(2)}),
    (Q.transcendental(x*y), Q.zero(x) & Q.transcendental(y), True, {x: 0, y: pi}),
    (Q.integer(sqrt(2)*x), Q.integer(x), False, {x: 0}),
    (Q.nonzero(5**(2*I*pi*n)), Q.integer(n), False, {n: 0}),
    (Q.imaginary(x**y), Q.negative(x) & Q.rational(y) & Q.integer(2*y), True,
        {x: -1, y: 0}),
    # the terms may cancel
    (Q.imaginary(x + I), Q.imaginary(x), True, {x: -I}),
    (Q.imaginary(x + y), Q.imaginary(x) & Q.imaginary(y), True, {x: I, y: -I}),
    # the argument may be infinite
    (Q.real(Abs(x)), True, True, {x: oo}),
    (Q.complex(Abs(x)), True, True, {x: oo}),
    (Q.real(re(x)), True, True, {x: oo}),
    (Q.complex(re(x)), True, True, {x: oo}),
    (Q.real(im(x)), True, True, {x: oo*I}),
    (Q.complex(im(x)), True, True, {x: oo*I}),
    (Q.complex(exp(x)), True, True, {x: oo}),
    (Q.complex(sin(x)), True, True, {x: oo*I}),
    (Q.complex(cos(x)), True, True, {x: oo*I}),
    (Q.finite(sin(x)), True, True, {x: oo*I}),
    (Q.finite(sin(x)), ~Q.finite(x), True, {x: oo*I}),
    (Q.finite(cos(x)), True, True, {x: oo*I}),
    (Q.finite(cos(x)), ~Q.finite(x), True, {x: oo*I}),
    (Q.finite(2*sin(x)), True, True, {x: oo*I}),
    (Q.finite(sin(x)**2), True, True, {x: oo*I}),
    (Q.finite(cos(x)**2), True, True, {x: oo*I}),
    (Q.finite(log(x)), ~Q.zero(x), True, {x: oo}),
    (Q.finite(2**x), ~Q.finite(x), False, {x: -oo}),
    # a power of zero may be infinite
    (Q.algebraic(x**y), Q.algebraic(x) & Q.rational(y), True, {x: 0, y: -1}),
    (Q.complex(x**y), Q.complex(x) & Q.complex(y), True, {x: 0, y: -1}),
    # the value at one point of the range
    (Q.positive(acos(x)), Q.nonnegative(x + 1) & Q.nonpositive(x - 1), True, {x: 1}),
    (Q.positive(acot(x)), Q.real(x), True, {x: -1}),
    (Q.imaginary((2*I)**x), Q.imaginary(x), False, {x: I*pi/(2*log(2))}),
    # the two dimensions may be equal
    (Q.invertible(A), True, False, {A: ImmutableMatrix([[1]])}),
]

# (query, assumptions, the answer of ask), where ask cannot judge the values
WRONG_ANSWERS_NOT_CHECKED = [
    # 0*oo is nan
    (Q.zero(x*y), Q.zero(x), True),
    # [[1, 0], [0, 2]]*[[0, 1], [1, 0]] is [[0, 1], [2, 0]]
    (Q.symmetric(X*Z), Q.symmetric(X) & Q.symmetric(Z), True),
    # the sum is symmetric when X and Z are
    (Q.symmetric(X + Z), True, False),
    # W[1:3, 1:3] is zero for W = [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    (Q.invertible(W[1:3, 1:3]), Q.invertible(W), True),
    (Q.orthogonal(W[1:3, 1:3]), Q.orthogonal(W), True),
]


def test_rules_do_not_give_the_wrong_answers():
    for query, assumptions, wrong, *_ in WRONG_ANSWERS + WRONG_ANSWERS_NOT_CHECKED:
        answer = ask_by_rules(query.function, query.arg, assumptions, RULES)
        assert answer is not wrong, (query, assumptions)


def test_ask_gives_the_wrong_answers():
    for query, assumptions, wrong, *_ in WRONG_ANSWERS + WRONG_ANSWERS_NOT_CHECKED:
        assert ask(query, assumptions) is wrong, (query, assumptions)


def test_the_answers_are_wrong():
    for query, assumptions, wrong, values in WRONG_ANSWERS:
        if assumptions is not True:
            assert ask(assumptions.subs(values)) is True, (query, assumptions)
        assert ask(query.subs(values)) is (not wrong), (query, assumptions)
