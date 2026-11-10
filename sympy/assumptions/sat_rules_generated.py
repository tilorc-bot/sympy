"""
Do NOT manually edit this file.
Instead, run ./bin/ask_update.py.
"""

from sympy.assumptions.ask import Q
from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.core.power import Pow
from sympy.functions.elementary.complexes import Abs
from sympy.matrices.expressions.matmul import MatMul

# A literal ``(predicate, slot, value)`` says that the predicate has the truth
# value ``value`` for an expression: the argument number ``slot`` of the
# expression which a rule is about, or that expression itself for the slot
# ``EXPR``. A sum or a product is read as its first argument and the rest.
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
        # Q.extended_nonnegative(f(x))
        ((Q.extended_nonnegative, EXPR, True),),
        # Implies(Q.finite(x), Q.nonnegative(f(x)))
        ((Q.finite, 0, False), (Q.nonnegative, EXPR, True)),
        # Equivalent(Q.zero(x), Q.zero(f(x)))
        ((Q.zero, 0, False), (Q.zero, EXPR, True)),
        ((Q.zero, 0, True), (Q.zero, EXPR, False)),
        # Implies(Q.integer(x), Q.integer(f(x)))
        ((Q.integer, 0, False), (Q.integer, EXPR, True)),
    ),
    (Add, 2): (
        # Implies(Q.positive(x) & Q.positive(y), Q.positive(f(x, y)))
        ((Q.positive, 0, False), (Q.positive, 1, False), (Q.positive, EXPR, True)),
        # Implies(Q.negative(x) & Q.negative(y), Q.negative(f(x, y)))
        ((Q.negative, 0, False), (Q.negative, 1, False), (Q.negative, EXPR, True)),
        # Implies(Q.real(x) & Q.real(y), Q.real(f(x, y)))
        ((Q.real, 0, False), (Q.real, 1, False), (Q.real, EXPR, True)),
        # Implies(Q.rational(x) & Q.rational(y), Q.rational(f(x, y)))
        ((Q.rational, 0, False), (Q.rational, 1, False), (Q.rational, EXPR, True)),
        # Implies(Q.integer(x) & Q.integer(y), Q.integer(f(x, y)))
        ((Q.integer, 0, False), (Q.integer, 1, False), (Q.integer, EXPR, True)),
        # Implies(Q.integer(x) & ~Q.integer(y), ~Q.integer(f(x, y)))
        ((Q.integer, 0, False), (Q.integer, 1, True), (Q.integer, EXPR, False)),
        # Implies(Q.integer(y) & ~Q.integer(x), ~Q.integer(f(x, y)))
        ((Q.integer, 0, True), (Q.integer, 1, False), (Q.integer, EXPR, False)),
        # Implies(Q.irrational(y) & Q.rational(x), Q.irrational(f(x, y)))
        ((Q.rational, 0, False), (Q.irrational, 1, False), (Q.irrational, EXPR, True)),
        # Implies(Q.irrational(x) & Q.rational(y), Q.irrational(f(x, y)))
        ((Q.irrational, 0, False), (Q.rational, 1, False), (Q.irrational, EXPR, True)),
    ),
    (MatMul, 2): (
        # Implies(Q.square(x) & Q.square(y), Equivalent(Q.invertible(f(x, y)), Q.invertible(x) & Q.invertible(y)))
        ((Q.invertible, 0, False), (Q.square, 0, False), (Q.invertible, 1, False), (Q.square, 1, False), (Q.invertible, EXPR, True)),
        ((Q.invertible, 0, True), (Q.square, 0, False), (Q.square, 1, False), (Q.invertible, EXPR, False)),
        ((Q.square, 0, False), (Q.invertible, 1, True), (Q.square, 1, False), (Q.invertible, EXPR, False)),
    ),
    (Mul, 2): (
        # Implies(Q.complex(f(x, y)), Q.finite(x) & Q.finite(y))
        ((Q.finite, 0, True), (Q.complex, EXPR, False)),
        ((Q.finite, 1, True), (Q.complex, EXPR, False)),
        # Implies(Q.commutative(x) & Q.commutative(y), Q.commutative(f(x, y)))
        ((Q.commutative, 0, False), (Q.commutative, 1, False), (Q.commutative, EXPR, True)),
        # Implies(Q.integer(x) & Q.integer(y), Equivalent(Q.even(f(x, y)), Q.even(x) | Q.even(y)))
        ((Q.even, 0, False), (Q.integer, 0, False), (Q.integer, 1, False), (Q.even, EXPR, True)),
        ((Q.even, 0, True), (Q.integer, 0, False), (Q.even, 1, True), (Q.integer, 1, False), (Q.even, EXPR, False)),
        ((Q.integer, 0, False), (Q.even, 1, False), (Q.integer, 1, False), (Q.even, EXPR, True)),
        # Implies(Q.prime(x) & Q.prime(y), Q.composite(f(x, y)))
        ((Q.prime, 0, False), (Q.prime, 1, False), (Q.composite, EXPR, True)),
        # Implies(Q.composite(y) & Q.prime(x), Q.composite(f(x, y)))
        ((Q.prime, 0, False), (Q.composite, 1, False), (Q.composite, EXPR, True)),
        # Implies(Q.positive(x) & Q.positive(y), Q.positive(f(x, y)))
        ((Q.positive, 0, False), (Q.positive, 1, False), (Q.positive, EXPR, True)),
        # Implies(Q.zero(f(x, y)), Q.zero(x) | Q.zero(y))
        ((Q.zero, 0, True), (Q.zero, 1, True), (Q.zero, EXPR, False)),
        # Implies(Q.finite(y) & Q.zero(x), Q.zero(f(x, y)))
        ((Q.zero, 0, False), (Q.finite, 1, False), (Q.zero, EXPR, True)),
        # Implies(Q.finite(x) & Q.zero(y), Q.zero(f(x, y)))
        ((Q.finite, 0, False), (Q.zero, 1, False), (Q.zero, EXPR, True)),
        # Implies(Q.real(x) & Q.real(y), Q.real(f(x, y)))
        ((Q.real, 0, False), (Q.real, 1, False), (Q.real, EXPR, True)),
        # Implies(Q.rational(x) & Q.rational(y), Q.rational(f(x, y)))
        ((Q.rational, 0, False), (Q.rational, 1, False), (Q.rational, EXPR, True)),
        # Implies(Q.integer(x) & Q.integer(y), Q.integer(f(x, y)))
        ((Q.integer, 0, False), (Q.integer, 1, False), (Q.integer, EXPR, True)),
        # Implies(Q.rational(x) & ~Q.rational(y) & ~Q.zero(x), ~Q.rational(f(x, y)))
        ((Q.rational, 0, False), (Q.zero, 0, True), (Q.rational, 1, True), (Q.rational, EXPR, False)),
        # Implies(Q.rational(y) & ~Q.rational(x) & ~Q.zero(y), ~Q.rational(f(x, y)))
        ((Q.rational, 0, True), (Q.rational, 1, False), (Q.zero, 1, True), (Q.rational, EXPR, False)),
        # Implies(Q.irrational(y) & Q.rational(x) & ~Q.zero(x), Q.irrational(f(x, y)))
        ((Q.rational, 0, False), (Q.zero, 0, True), (Q.irrational, 1, False), (Q.irrational, EXPR, True)),
        # Implies(Q.irrational(x) & Q.rational(y) & ~Q.zero(y), Q.irrational(f(x, y)))
        ((Q.irrational, 0, False), (Q.rational, 1, False), (Q.zero, 1, True), (Q.irrational, EXPR, True)),
        # Implies(Q.imaginary(y) & Q.real(x) & ~Q.zero(x), Q.imaginary(f(x, y)))
        ((Q.real, 0, False), (Q.zero, 0, True), (Q.imaginary, 1, False), (Q.imaginary, EXPR, True)),
        # Implies(Q.imaginary(x) & Q.real(y) & ~Q.zero(y), Q.imaginary(f(x, y)))
        ((Q.imaginary, 0, False), (Q.real, 1, False), (Q.zero, 1, True), (Q.imaginary, EXPR, True)),
    ),
    (Pow, 2): (
        # Implies(Q.even(exponent) & Q.nonnegative(exponent) & Q.real(base), Q.nonnegative(f(base, exponent)))
        ((Q.real, 0, False), (Q.even, 1, False), (Q.nonnegative, 1, False), (Q.nonnegative, EXPR, True)),
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
    ),
}
