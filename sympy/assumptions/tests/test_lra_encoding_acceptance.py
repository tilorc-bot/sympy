"""Acceptance cases for the LRA bridge. Shared between implementations."""
import subprocess
import sys

from sympy import I, Q, S, ask, oo, refine, sqrt, Abs
from sympy.abc import x, y, z
from sympy.assumptions.satask import satask
from sympy.core.symbol import Symbol
from sympy.matrices.expressions import MatrixSymbol

R = Q.real
f = Symbol('f')


# --- the eight answers the change exists to deliver -----------------------

def test_ask_answers_arithmetic():
    assert ask(Q.gt(x, z), Q.gt(x, y) & Q.gt(y, z) & R(x) & R(y) & R(z)) is True
    assert ask(Q.gt(x, y), Q.gt(x, 1) & Q.lt(y, 1) & R(x) & R(y)) is True
    assert ask(Q.eq(x, y), Q.ge(x, y) & Q.le(x, y) & R(x) & R(y)) is True
    assert ask(Q.gt(x + y, 0), Q.gt(x, 0) & Q.gt(y, 0) & R(x) & R(y)) is True
    assert ask(Q.gt(2*x, 2), Q.gt(x, 1) & R(x)) is True
    assert ask(Q.positive(x), Q.gt(x, 0) & R(x)) is True
    assert ask(Q.gt(x, 0), Q.gt(x*y, 0) & Q.gt(x, 1) & R(x) & R(y)) is True
    assert ask(Q.gt(x, 0), Q.gt(f, 0) & Q.gt(x, 1) & R(x)) is True


# --- the realness guard must still hold -----------------------------------

def test_guard_holds():
    assert satask(Q.gt(I, 1)) is None
    assert satask(Q.gt(x, 0)) is None                     # no realness source
    assert satask(Q.positive(x), Q.gt(x, 0)) is None      # ditto
    assert satask(Q.positive(oo)) is False
    assert satask(Q.gt(S(3), S(2))) is True


# --- regressions PR #8 introduced -----------------------------------------

def test_no_unhandled_input_escapes():
    assert ask(Q.positive(x), Q.gt(x, sqrt(2))) is None
    assert refine(Abs(x), Q.gt(x, sqrt(2))) == Abs(x)
    assert satask(Q.positive(x), Q.gt(x, sqrt(2)) & R(x)) in (None, True)


def test_irrational_bound_does_not_cost_the_other_atom():
    # x > sqrt(2) is skipped; y > 1 is not.
    assert satask(Q.gt(y, 0), Q.gt(x, sqrt(2)) & Q.gt(y, 1) & R(x) & R(y)) is True


def test_ne_on_non_arithmetic_operands():
    A = MatrixSymbol('A', 2, 2)
    B = MatrixSymbol('B', 2, 2)
    assert satask(Q.ne(A, B)) is None


def test_ask_calls_satask_once():
    import sympy.assumptions.satask as satmod
    calls = [0]
    original = satmod.satask

    def counted(*a, **k):
        calls[0] += 1
        return original(*a, **k)

    satmod.satask = counted
    try:
        ask(Q.odd(3*x))
    finally:
        satmod.satask = original
    assert calls[0] <= 1


# --- the query that hangs on PR #8 ----------------------------------------

def test_large_factbase_terminates():
    # 841 clauses, 287 atoms, 5 of them arithmetic. Must return, not spin.
    assert satask(~Q.eq(1, x + y),
                  R(x) & R(y) & Q.ne(1, x + y) & ~Q.eq(1, 2*x)
                  & ~Q.positive(x - y)) in (None, True, False)


# --- determinism across processes -----------------------------------------

_DET = (
    "from sympy import Q\n"
    "from sympy.abc import x, y, z\n"
    "from sympy.assumptions.satask import satask\n"
    "print(repr(satask(Q.gt(x*y, -1), Q.gt(x*y, 0) & Q.gt(y*z, 0)"
    " & Q.real(x) & Q.real(y) & Q.real(z))))\n"
)


def test_selection_does_not_depend_on_hash_seed():
    seen = set()
    for seed in ('0', '1', '2', '3', '5', '7', '11', '13'):
        out = subprocess.run([sys.executable, '-c', _DET], capture_output=True,
                             text=True, env={'PYTHONHASHSEED': seed, 'PATH': ''})
        seen.add(out.stdout.strip())
    assert len(seen) == 1, seen
