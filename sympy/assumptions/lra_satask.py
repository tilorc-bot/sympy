from __future__ import annotations
from sympy.assumptions.cnf import CNF, EncodedCNF, Literal
from sympy.assumptions.ask import Q
from sympy.assumptions.reasoning_engine import ReasoningEngine
from sympy.logic.algorithms.lra_theory import UnhandledInput, ALLOWED_PRED
from sympy.matrices.kind import MatrixKind
from sympy.core.kind import NumberKind
from sympy.assumptions.assume import AppliedPredicate
from sympy.core.mul import Mul
from sympy.core.singleton import S


def lra_satask(proposition, assumptions=True):
    """
    Function to evaluate the proposition with assumptions using SAT algorithm
    in conjunction with an Linear Real Arithmetic theory solver.

    Used to handle inequalities. Should eventually be depreciated and combined
    into satask, but infinity handling and other things need to be implemented
    before that can happen.
    """
    props = CNF.from_prop(proposition)
    _props = CNF.from_prop(~proposition)

    assumptions = CNF.from_prop(assumptions)

    return check_satisfiability(props, _props, assumptions)

# Some predicates such as Q.prime can't be handled by lra_satask.
# For example, (x > 0) & (x < 1) & Q.prime(x) is unsat but lra_satask would think it was sat.
# WHITE_LIST is a list of predicates that can always be handled.
WHITE_LIST = ALLOWED_PRED.keys() | {Q.positive, Q.negative, Q.zero, Q.nonzero, Q.nonpositive, Q.nonnegative,
                                    Q.extended_positive, Q.extended_negative, Q.extended_nonpositive,
                                    Q.extended_negative, Q.extended_nonzero, Q.negative_infinite,
                                    Q.positive_infinite}


def check_satisfiability(prop, _prop, factbase):
    """Answer a query after validating and rewriting its three CNF inputs."""
    predicates = prop.all_predicates() | _prop.all_predicates() | factbase.all_predicates()
    applied = {pred for pred in predicates if isinstance(pred, AppliedPredicate)}
    all_exprs = {arg for pred in applied for arg in pred.arguments}

    for pred in applied:
        if pred.function not in WHITE_LIST and pred.function != Q.ne:
            raise UnhandledInput(f"LRASolver: {pred} is an unhandled predicate")
    for expr in all_exprs:
        if expr.kind == MatrixKind(NumberKind):
            raise UnhandledInput(f"LRASolver: {expr} is of MatrixKind")
        if expr == S.NaN:
            raise UnhandledInput("LRASolver: nan")

    factbase = factbase.copy()
    for assm in extract_pred_from_old_assum(all_exprs):
        factbase.add(assm)
        predicates.add(assm)

    replacements = {pred: _pred_to_binrel(pred) for pred in predicates}
    encoded = EncodedCNF()
    encoded.from_cnf(_preprocess(factbase, replacements))
    engine = ReasoningEngine(encoded, use_lra_theory=True)
    query = engine.create_query(_preprocess(prop, replacements),
                                _preprocess(_prop, replacements))
    return engine.ask_query(query)


def _preprocess(cnf, replacements):
    """Rewrite each literal as a disjunction of LRA literals within its clause.

    False literals are removed from disjunctions. An entirely false clause
    retains a false literal so EncodedCNF encodes it as the contradiction {0}.
    """
    clauses = set()
    for clause in cnf.clauses:
        rewritten = frozenset(new_lit for lit in clause
                              for new_lit in _rewrite_literal(lit, replacements[lit.lit])
                              if new_lit.lit != S.false)
        clauses.add(rewritten or frozenset((Literal(S.false),)))
    return CNF(clauses)


def _rewrite_literal(literal, pred):
    """Expand disequalities and negated equalities into strict inequalities.

    Negation of a converted Boolean constant must be evaluated here because
    EncodedCNF represents false literals by 0, regardless of their polarity.
    """
    negated = literal.is_Not
    if pred in (True, False):
        return (Literal(S.true if bool(pred) != negated else S.false),)
    if isinstance(pred, AppliedPredicate) and pred.function in (Q.eq, Q.ne):
        if (pred.function == Q.ne) != negated:
            return (Literal(Q.gt(*pred.arguments)), Literal(Q.lt(*pred.arguments)))
        return (Literal(Q.eq(*pred.arguments)),)
    return (Literal(pred, negated),)


def _pred_to_binrel(pred):
    if not isinstance(pred, AppliedPredicate):
        return pred

    if pred.function in pred_to_pos_neg_zero:
        f = pred_to_pos_neg_zero[pred.function]
        if f is False:
            return False
        pred = f(pred.arguments[0])

    if pred.function == Q.positive:
        pred = Q.gt(pred.arguments[0], 0)
    elif pred.function == Q.negative:
        pred = Q.lt(pred.arguments[0], 0)
    elif pred.function == Q.zero:
        pred = Q.eq(pred.arguments[0], 0)
    elif pred.function == Q.nonpositive:
        pred = Q.le(pred.arguments[0], 0)
    elif pred.function == Q.nonnegative:
        pred = Q.ge(pred.arguments[0], 0)
    elif pred.function == Q.nonzero:
        pred = Q.ne(pred.arguments[0], 0)

    return pred

pred_to_pos_neg_zero = {
    Q.extended_positive: Q.positive,
    Q.extended_negative: Q.negative,
    Q.extended_nonpositive: Q.nonpositive,
    Q.extended_negative: Q.negative,
    Q.extended_nonzero: Q.nonzero,
    Q.negative_infinite: False,
    Q.positive_infinite: False
}

def extract_pred_from_old_assum(all_exprs):
    """
    Returns a list of relevant new assumption predicate
    based on any old assumptions.

    Raises an UnhandledInput exception if any of the assumptions are
    unhandled.

    Ignored predicate:
    - commutative
    - complex
    - algebraic
    - transcendental
    - extended_real
    - real
    - all matrix predicate
    - rational
    - irrational

    Example
    =======
    >>> from sympy.assumptions.lra_satask import extract_pred_from_old_assum
    >>> from sympy import symbols
    >>> x, y = symbols("x y", positive=True)
    >>> extract_pred_from_old_assum([x, y, 2])
    [Q.positive(x), Q.positive(y)]
    """
    ret = []
    for expr in all_exprs:
        if not hasattr(expr, "free_symbols"):
            continue
        if len(expr.free_symbols) == 0:
            continue

        if expr.is_real is not True:
            raise UnhandledInput(f"LRASolver: {expr} must be real")
        # test for I times imaginary variable; such expressions are considered real
        if isinstance(expr, Mul) and any(arg.is_real is not True for arg in expr.args):
            raise UnhandledInput(f"LRASolver: {expr} must be real")

        if expr.is_integer == True and expr.is_zero != True:
            raise UnhandledInput(f"LRASolver: {expr} is an integer")
        if expr.is_integer == False:
            raise UnhandledInput(f"LRASolver: {expr} can't be an integer")
        if expr.is_rational == False:
            raise UnhandledInput(f"LRASolver: {expr} is irational")

        if expr.is_zero:
            ret.append(Q.zero(expr))
        elif expr.is_positive:
            ret.append(Q.positive(expr))
        elif expr.is_negative:
            ret.append(Q.negative(expr))
        elif expr.is_nonzero:
            ret.append(Q.nonzero(expr))
        elif expr.is_nonpositive:
            ret.append(Q.nonpositive(expr))
        elif expr.is_nonnegative:
            ret.append(Q.nonnegative(expr))

    return ret
