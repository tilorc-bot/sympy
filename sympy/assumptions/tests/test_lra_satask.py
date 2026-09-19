from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.assumptions.cnf import CNF
from sympy.assumptions.lra_satask import check_satisfiability, lra_satask
from sympy.core.singleton import S
from sympy.core.symbol import symbols
from sympy.testing.pytest import raises


x, y = symbols('x y', real=True)


def test_lra_satask_disjunctive_equalities():
    for equality in (Q.eq(x, 0), ~Q.ne(x, 0)):
        for disequality in (Q.ne(x, 0), ~Q.eq(x, 0)):
            assert lra_satask(equality | Q.gt(y, 0),
                              Q.le(x, 0) & Q.ge(x, 0)) is True
            assert lra_satask(disequality | Q.gt(y, 0),
                              Q.eq(x, 0) & Q.le(y, 0)) is False
            assert lra_satask(Q.ne(x, 0),
                              disequality | Q.gt(x, 0)) is True
            assert lra_satask(Q.gt(y, 0),
                              (disequality | Q.gt(y, 0)) & equality) is True


def test_lra_satask_boolean_constants():
    for infinite in (Q.positive_infinite(x), Q.negative_infinite(x)):
        assert lra_satask(infinite | Q.gt(x, 0), Q.lt(x, 0)) is False
        assert lra_satask(~infinite & Q.gt(x, 0), Q.gt(x, 1)) is True
        assert lra_satask(Q.gt(x, 0), infinite | Q.gt(x, 1)) is True
        assert lra_satask(Q.gt(x, 0), ~infinite) is None

    for proposition in (S.true, S.false, Q.gt(x, 0)):
        with raises(ValueError, match='Inconsistent assumptions'):
            lra_satask(proposition,
                       Q.positive_infinite(x) | Q.negative_infinite(x))

    assert lra_satask(S.true) is True
    assert lra_satask(S.false) is False


def test_lra_satask_cnf_inputs_unchanged():
    positive = symbols('positive', positive=True)
    prop = CNF.from_prop(Q.gt(positive, 0))
    negated = CNF.from_prop(~Q.gt(positive, 0))
    assumptions = CNF.from_prop(Q.ne(positive, 0))
    originals = [cnf.copy() for cnf in (prop, negated, assumptions)]

    assert check_satisfiability(prop, negated, assumptions) is True
    for cnf, original in zip((prop, negated, assumptions), originals):
        assert cnf.clauses == original.clauses
