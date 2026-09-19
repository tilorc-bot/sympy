"""
rename this to test_assumptions.py when the old assumptions system is deleted
"""
from __future__ import annotations
from sympy.abc import x, y
from sympy.assumptions.assume import global_assumptions
from sympy.assumptions.ask import Q, _ask_single_fact
from sympy.printing import pretty
from sympy.assumptions.cnf import clauses_from_prop


def test_equal():
    """Test for equality"""
    assert Q.positive(x) == Q.positive(x)
    assert Q.positive(x) != ~Q.positive(x)
    assert ~Q.positive(x) == ~Q.positive(x)


def test_pretty():
    assert pretty(Q.positive(x)) == "Q.positive(x)"
    assert pretty(
        {Q.positive, Q.integer}) == "{Q.integer, Q.positive}"


def test_global():
    """Test for global assumptions"""
    global_assumptions.add(x > 0)
    assert (x > 0) in global_assumptions
    global_assumptions.remove(x > 0)
    assert not (x > 0) in global_assumptions
    # same with multiple of assumptions
    global_assumptions.add(x > 0, y > 0)
    assert (x > 0) in global_assumptions
    assert (y > 0) in global_assumptions
    global_assumptions.clear()
    assert not (x > 0) in global_assumptions
    assert not (y > 0) in global_assumptions


def test_ask_single_fact():
    assert _ask_single_fact(Q.real, set()) is None
    assert _ask_single_fact(Q.even, clauses_from_prop(Q.zero)) is True
    assert _ask_single_fact(Q.even, clauses_from_prop(Q.odd)) is False
    assert _ask_single_fact(Q.even, clauses_from_prop(Q.real)) is None
    assert _ask_single_fact(Q.integer, clauses_from_prop(Q.even | Q.odd)) is None
    assert _ask_single_fact(Q.integer, clauses_from_prop(Q.prime)) is True
    assert _ask_single_fact(Q.prime,   clauses_from_prop(Q.composite)) is False
    assert _ask_single_fact(Q.zero, clauses_from_prop(~Q.even)) is False

    assert _ask_single_fact(Q.zero, clauses_from_prop(~Q.even & Q.real)) is False
