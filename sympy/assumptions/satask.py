"""
Module to evaluate the proposition with assumptions using SAT algorithm.
"""
from __future__ import annotations

from typing import Any

from sympy.core.add import Add
from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.core.kind import NumberKind, UndefinedKind
from sympy.assumptions.ask import Q
from sympy.assumptions.ask_generated import get_all_known_matrix_facts, get_all_known_number_facts
from sympy.assumptions.assume import AppliedPredicate
from sympy.assumptions.sathandlers import class_fact_registry
from sympy.core import oo
from sympy.logic.algorithms.dpll2 import SATSolver, IpasirStatus
from sympy.logic.algorithms.lra_theory import ALLOWED_PRED, LRASolver, UnhandledInput
from sympy.assumptions.cnf import CNF, EncodedCNF, Literal
from sympy.matrices.kind import MatrixKind


def satask(proposition, assumptions=True, use_known_facts=True, iterations=oo,
           early_return=False, use_lra_theory=True):
    """
    Function to evaluate the proposition with assumptions using SAT algorithm.

    This function extracts every fact relevant to the expressions composing
    proposition and assumptions. For example, if a predicate containing
    ``Abs(x)`` is proposed, then ``Q.zero(Abs(x)) | Q.positive(Abs(x))``
    will be found and passed to SAT solver because ``Q.nonnegative`` is
    registered as a fact for ``Abs``.

    Proposition is evaluated to ``True`` or ``False`` if the truth value can be
    determined. If not, ``None`` is returned.

    Parameters
    ==========

    proposition : Any boolean expression.
        Proposition which will be evaluated to boolean value.

    assumptions : Any boolean expression, optional.
        Local assumptions to evaluate the *proposition*.

    use_known_facts : bool, optional.
        If ``True``, facts from ``sympy.assumptions.ask_generated``
        module are passed to SAT solver as well.

    iterations : int, optional.
        Number of times that relevant facts are recursively extracted.
        Default is infinite times until no new fact is found.

    early_return : bool, optional.
        If ``True``, answer from the propagated facts alone, trusting
        *assumptions* to be consistent. Default is ``False``.

    use_lra_theory : bool, optional.
        If ``True``, the predicates that say something about linear real
        arithmetic are given to a theory solver alongside the SAT solver,
        which lets facts about different expressions be combined. Default
        is ``True``.

    Returns
    =======

    ``True``, ``False``, or ``None``

    Examples
    ========

    >>> from sympy import Abs, Q
    >>> from sympy.assumptions.satask import satask
    >>> from sympy.abc import x
    >>> satask(Q.zero(Abs(x)), Q.zero(x))
    True

    """
    props = CNF.from_prop(proposition)
    _props = CNF.from_prop(~proposition)

    assumptions = CNF.from_prop(assumptions)

    sat = get_all_relevant_facts(props, assumptions,
        use_known_facts=use_known_facts, iterations=iterations)
    sat.add_from_cnf(assumptions)

    return check_satisfiability(props, _props, sat, early_return, use_lra_theory)


def check_satisfiability(prop, _prop, factbase, early_return=False,
                         use_lra_theory=True):
    if {0} in factbase.data:
        raise ValueError("Inconsistent assumptions")

    true_false_guarded, selector = _encode_with_selector(prop, _prop, factbase)

    lra = None
    if use_lra_theory:
        lra = _add_arithmetic(true_false_guarded, _asked_about(prop))

    # Run `propogate()` on the assumptions
    solver = SATSolver(true_false_guarded.data, true_false_guarded.variables,
                       set(), true_false_guarded.symbols, lra_theory=lra)
    if solver.propagate() == IpasirStatus.UNSATISFIABLE:
        raise ValueError("Inconsistent assumptions")

    # Check whether proposition is entailed by any of the assigned literals.
    if early_return:
        entailed = solver._is_entailed(prop.clauses, true_false_guarded.encoding)
        if entailed is not None:
            return entailed

        entailed = solver._is_entailed(_prop.clauses, true_false_guarded.encoding)
        if entailed is not None:
            return not entailed

    # Continue on the propogated solver, just call solve() on it.
    if solver.solve() == IpasirStatus.UNSATISFIABLE:
        raise ValueError("Inconsistent assumptions")

    # The model settles the side it activated, so ask about the other one.
    witnessed = solver.val(selector)
    solver.assume(-witnessed)
    other = solver.solve() == IpasirStatus.SATISFIABLE

    can_be_true = witnessed > 0 or other
    can_be_false = witnessed < 0 or other

    if can_be_true and can_be_false:
        return None

    if can_be_true and not can_be_false:
        return True

    if not can_be_true and can_be_false:
        return False

    if not can_be_true and not can_be_false:
        # TODO: Run additional checks to see which combination of the
        # assumptions, global_assumptions, and relevant_facts are
        # inconsistent.
        raise ValueError("Inconsistent assumptions")


def _encode_with_selector(prop, _prop, factbase):
    """Return *factbase* with the clauses of prop and _prop added to it, and
    the selector variable that activates prop when true and _prop when false.
    """
    true_false_guarded = factbase.copy()
    sides = [[true_false_guarded.encode(clause) for clause in side.clauses]
             for side in (prop, _prop)]

    # One past the last predicate, so the selector is a variable of its own.
    selector = true_false_guarded.add_variable(Symbol("selector"))

    for clauses, guard in zip(sides, (-selector, selector)):
        # Dropping the 0 that encodes False leaves a side nothing can satisfy
        # as the unit {guard}.
        true_false_guarded.data += [(clause - {0}) | {guard}
                                    for clause in clauses]

    return true_false_guarded, selector


# The relation each sign predicate is a statement about. Q.positive(x) says
# the same thing about a real x as x > 0 does, and the extended predicates say
# it too once x is known to be a real number rather than an infinity.
_SIGN_RELATION = {
    Q.positive: Q.gt, Q.negative: Q.lt, Q.zero: Q.eq,
    Q.nonpositive: Q.le, Q.nonnegative: Q.ge, Q.nonzero: Q.ne,
    Q.extended_positive: Q.gt, Q.extended_negative: Q.lt,
    Q.extended_nonpositive: Q.le, Q.extended_nonnegative: Q.ge,
    Q.extended_nonzero: Q.ne,
}

# Q.ne is the one relation the theory solver has no boundary for, so it is
# encoded as the two strict inequalities it is the union of.
_RELATIONS = ALLOWED_PRED.keys() | {Q.ne}


def _asked_about(prop: CNF) -> set[Any]:
    """The expressions *prop* is a statement about."""
    return {arg for pred in prop.all_predicates()
            if isinstance(pred, AppliedPredicate) for arg in pred.arguments}


def _add_arithmetic(enc: EncodedCNF,
                    asked_about: set[Any] | frozenset[Any] = frozenset()
                    ) -> LRASolver | None:
    """Give the predicates of *enc* that are linear constraints an arithmetic
    reading, and return the ``LRASolver`` that reads them, or ``None``.

    Each such predicate is tied to a fresh variable that only the theory
    solver knows the meaning of, under a guard on the realness of the
    arguments::

        Q.real(lhs) & Q.real(rhs) >> Implies(Q.gt(lhs, rhs), lhs - rhs > 0)

    and the converse, so that the tie is an equivalence. The arithmetic is
    therefore available exactly when the facts force the arguments to be real
    numbers -- which the fact base can do for a compound expression, since
    ``Q.real(x) & Q.real(y) >> Q.real(x - y)`` is one of the class facts --
    and the predicate stays an opaque boolean when they do not. That keeps
    ``Q.gt(I, 1)`` and its like out of the theory instead of handing it a
    variable that is not a real number.
    """
    candidates: list[tuple[Any, int, Any, Any, set[int], list[Any]]] = []
    settled: list[set[int]] = []
    relational: bool = False
    for pred in list(enc.encoding):
        relation = _as_relation(pred)
        if relation is None:
            continue
        function, lhs, rhs = relation

        guards = _realness_guards(enc, (lhs, rhs))
        if guards is None:
            continue

        try:
            expr = lhs - rhs
        except TypeError:
            # Kinds are not implemented everywhere, so the two sides can still
            # turn out to be things that cannot be subtracted from each other.
            continue

        if not expr.free_symbols:
            # There is nothing for a theory solver to decide here.
            holds = _settle(function, expr)
            if holds is not None:
                var = enc.encoding[pred]
                settled.append(guards | {var if holds else -var})
            continue

        terms = _terms(expr)
        if terms is None:
            continue

        # The question first, then the simple terms: a term the theory cannot
        # take should not be the one that claims a symbol the others need.
        rank = (expr not in asked_about,
                max(len(term.free_symbols) for term in terms), len(terms))
        candidates.append((rank, enc.encoding[pred], function, expr, guards, terms))
        relational = relational or pred.function in _RELATIONS

    lra = None
    if relational or _relates_expressions(candidates):
        lra = _bridge(enc, candidates)
    enc.data += settled
    return lra


def _bridge(enc: EncodedCNF,
            candidates: list[tuple[Any, int, Any, Any, set[int], list[Any]]]
            ) -> LRASolver | None:
    """Tie each of *candidates* to a variable the theory solver reads as a
    constraint, and return the solver, or ``None`` if it cannot be built.
    """
    atoms: dict[Any, int] = {}
    owner: dict[Any, Any] = {}
    clauses: list[set[int]] = []

    def atom(function: Any, expr: Any, terms: list[Any]) -> int | None:
        """The variable the theory solver reads as ``function(expr, 0)``."""
        key = function(expr, S.Zero)
        if key not in atoms:
            if not _claim(owner, terms):
                return None
            atoms[key] = enc.add_variable(key)
        return atoms[key]

    for _, var, function, expr, guards, terms in sorted(candidates):
        if function is Q.ne:
            # x != y is x > y or x < y, both of which the theory can take.
            greater = atom(Q.gt, expr, terms)
            less = atom(Q.lt, expr, terms)
            if greater is None or less is None:
                continue
            clauses.append(guards | {-var, greater, less})
            clauses.append(guards | {var, -greater})
            clauses.append(guards | {var, -less})
        else:
            constraint = atom(function, expr, terms)
            if constraint is None:
                continue
            clauses.append(guards | {-var, constraint})
            clauses.append(guards | {var, -constraint})

    if not atoms:
        return None

    try:
        lra, conflicts = LRASolver.from_encoded_cnf(EncodedCNF([], dict(atoms)))
    except (UnhandledInput, ValueError, AssertionError, NotImplementedError,
            TypeError, AttributeError):
        # The theory is an extra, so being unable to build it is not an error.
        return None

    enc.data += clauses + [set(conflict) for conflict in conflicts]
    return lra


def _settle(function: Any, expr: Any) -> bool | None:
    """Whether ``function(expr, 0)`` holds for a constant *expr*, or ``None``
    when that cannot be decided.
    """
    if function is Q.ne:
        holds = ALLOWED_PRED[Q.gt](expr, S.Zero) | ALLOWED_PRED[Q.lt](expr, S.Zero)
    else:
        holds = ALLOWED_PRED[function](expr, S.Zero)

    if holds is S.true:
        return True
    if holds is S.false:
        return False
    return None



def _as_relation(pred: Any) -> tuple[Any, Any, Any] | None:
    """Return *pred* as ``(relation, lhs, rhs)``, or ``None`` when it does not
    say anything about linear real arithmetic.
    """
    if not isinstance(pred, AppliedPredicate):
        return None

    function = pred.function
    if function in _RELATIONS:
        lhs, rhs = pred.arguments
    elif function in _SIGN_RELATION:
        lhs, rhs = pred.arguments[0], S.Zero
        function = _SIGN_RELATION[function]
    else:
        return None

    return function, lhs, rhs


def _realness_guards(enc: EncodedCNF, sides: tuple[Any, Any]) -> set[int] | None:
    """Return the literals that make the guard false, one for each side whose
    realness is not already settled, or ``None`` if no guard can open.

    A side that is known real needs no literal, and one that is known not to
    be -- an infinity, or an imaginary number -- leaves a guard that could
    never open, so the caller has nothing to encode.
    """
    guards: set[int] = set()
    for side in sides:
        # UndefinedKind is checked for as well since the kind system isn't
        # fully implemented; Abs(x) and sin(x) have no kind of their own.
        if side.kind not in (NumberKind, UndefinedKind) or side is S.NaN:
            return None

        real = side.is_real
        if real is True:
            continue
        if real is False:
            return None

        guards.add(-enc.encode_arg(Literal(Q.real(side), False)))

    return guards


def _terms(expr: Any) -> list[Any] | None:
    """The terms the theory solver will read *expr* as a sum of, or ``None``
    when there are none for it to read.
    """
    terms: list[Any] = []
    for term in Add.make_args(expr):
        _, rest = term.as_coeff_Mul()
        if rest.free_symbols:
            terms.append(rest)

    return terms or None


def _claim(owner: dict[Any, Any], terms: list[Any]) -> bool:
    """Give each symbol of *terms* to the term it appears in, refusing when
    another term already has it.

    The theory solver reads a symbol shared by two of its terms as
    nonlinearity and gives up on the whole formula, so the terms it is given
    have to be kept variable disjoint.
    """
    if any(owner.get(symbol, term) != term
           for term in terms for symbol in term.free_symbols):
        return False

    for term in terms:
        for symbol in term.free_symbols:
            owner[symbol] = term

    return True


def _relates_expressions(
    candidates: list[tuple[Any, int, Any, Any, set[int], list[Any]]]
) -> bool:
    """Whether two of *candidates* constrain different expressions built from
    a common symbol.

    Sign predicates about one expression are already related to each other by
    the known facts, so where that is all there is a theory solver would cost
    time and answer nothing new. A binary relation is not in the known facts
    at all, so its presence is reason enough on its own.
    """
    seen: list[Any] = []
    for candidate in candidates:
        expr = candidate[3]
        if any(expr != other and expr.free_symbols & other.free_symbols
               for other in seen):
            return True
        seen.append(expr)

    return False


def extract_predargs(proposition, assumptions=None):
    """
    Extract every expression in the argument of predicates from *proposition*,
    *assumptions* and *context*.

    Parameters
    ==========

    proposition : sympy.assumptions.cnf.CNF

    assumptions : sympy.assumptions.cnf.CNF, optional.

    Examples
    ========

    >>> from sympy import Q, Abs
    >>> from sympy.assumptions.cnf import CNF
    >>> from sympy.assumptions.satask import extract_predargs
    >>> from sympy.abc import x, y
    >>> props = CNF.from_prop(Q.zero(Abs(x*y)))
    >>> assump = CNF.from_prop(Q.zero(x) & Q.zero(y))
    >>> extract_predargs(props, assump)
    {x, y, Abs(x*y)}

    """
    req_keys = find_symbols(proposition)
    keys = proposition.all_predicates()
    # XXX: We need this since True/False are not Basic
    lkeys = set()
    if assumptions:
        lkeys |= assumptions.all_predicates()

    lkeys = lkeys - {S.true, S.false}
    tmp_keys = None
    while tmp_keys != set():
        tmp = set()
        for l in lkeys:
            syms = find_symbols(l)
            if (syms & req_keys) != set():
                tmp |= syms
        tmp_keys = tmp - req_keys
        req_keys |= tmp_keys
    keys |= {l for l in lkeys if find_symbols(l) & req_keys != set()}

    exprs = set()
    for key in keys:
        if isinstance(key, AppliedPredicate):
            exprs |= set(key.arguments)
        else:
            exprs.add(key)
    return exprs

def find_symbols(pred):
    """
    Find every :obj:`~.Symbol` in *pred*.

    Parameters
    ==========

    pred : sympy.assumptions.cnf.CNF, or any Expr.

    """
    if isinstance(pred, CNF):
        symbols = set()
        for a in pred.all_predicates():
            symbols |= find_symbols(a)
        return symbols
    return pred.atoms(Symbol)


def get_relevant_clsfacts(exprs, relevant_facts=None):
    """
    Extract relevant facts from the items in *exprs*. Facts are defined in
    ``assumptions.sathandlers`` module.

    This function is recursively called by ``get_all_relevant_facts()``.

    Parameters
    ==========

    exprs : set
        Expressions whose relevant facts are searched.

    relevant_facts : sympy.assumptions.cnf.CNF, optional.
        Pre-discovered relevant facts.

    Returns
    =======

    exprs : set
        Candidates for next relevant fact searching.

    relevant_facts : sympy.assumptions.cnf.CNF
        Updated relevant facts.

    Examples
    ========

    Here, we will see how facts relevant to ``Abs(x*y)`` are recursively
    extracted. On the first run, set containing the expression is passed
    without pre-discovered relevant facts. The result is a set containing
    candidates for next run, and ``CNF()`` instance containing facts
    which are relevant to ``Abs`` and its argument.

    >>> from sympy import Abs
    >>> from sympy.assumptions.satask import get_relevant_clsfacts
    >>> from sympy.abc import x, y
    >>> exprs = {Abs(x*y)}
    >>> exprs, facts = get_relevant_clsfacts(exprs)
    >>> exprs
    {x*y}
    >>> facts.clauses #doctest: +SKIP
    {frozenset({Literal(Q.odd(Abs(x*y)), False), Literal(Q.odd(x*y), True)}),
    frozenset({Literal(Q.zero(Abs(x*y)), False), Literal(Q.zero(x*y), True)}),
    frozenset({Literal(Q.even(Abs(x*y)), False), Literal(Q.even(x*y), True)}),
    frozenset({Literal(Q.zero(Abs(x*y)), True), Literal(Q.zero(x*y), False)}),
    frozenset({Literal(Q.even(Abs(x*y)), False),
                Literal(Q.odd(Abs(x*y)), False),
                Literal(Q.odd(x*y), True)}),
    frozenset({Literal(Q.even(Abs(x*y)), False),
                Literal(Q.even(x*y), True),
                Literal(Q.odd(Abs(x*y)), False)}),
    frozenset({Literal(Q.positive(Abs(x*y)), False),
                Literal(Q.zero(Abs(x*y)), False)})}

    We pass the first run's results to the second run, and get the expressions
    for next run and updated facts.

    >>> exprs, facts = get_relevant_clsfacts(exprs, relevant_facts=facts)
    >>> exprs
    {x, y}

    On final run, no more candidate is returned thus we know that all
    relevant facts are successfully retrieved.

    >>> exprs, facts = get_relevant_clsfacts(exprs, relevant_facts=facts)
    >>> exprs
    set()

    """
    if not relevant_facts:
        relevant_facts = CNF()

    newexprs = set()
    for expr in exprs:
        for fact in class_fact_registry(expr):
            newfact = CNF.to_CNF(fact)
            relevant_facts = relevant_facts._and(newfact)
            for key in newfact.all_predicates():
                if isinstance(key, AppliedPredicate):
                    newexprs |= set(key.arguments)

    return newexprs - exprs, relevant_facts


def get_all_relevant_facts(proposition, assumptions,
        use_known_facts=True, iterations=oo):
    """
    Extract all relevant facts from *proposition* and *assumptions*.

    This function extracts the facts by recursively calling
    ``get_relevant_clsfacts()``. Extracted facts are converted to
    ``EncodedCNF`` and returned.

    Parameters
    ==========

    proposition : sympy.assumptions.cnf.CNF
        CNF generated from proposition expression.

    assumptions : sympy.assumptions.cnf.CNF
        CNF generated from assumption expression.

    use_known_facts : bool, optional.
        If ``True``, facts from ``sympy.assumptions.ask_generated``
        module are encoded as well.

    iterations : int, optional.
        Number of times that relevant facts are recursively extracted.
        Default is infinite times until no new fact is found.

    Returns
    =======

    sympy.assumptions.cnf.EncodedCNF

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.assumptions.cnf import CNF
    >>> from sympy.assumptions.satask import get_all_relevant_facts
    >>> from sympy.abc import x, y
    >>> props = CNF.from_prop(Q.nonzero(x*y))
    >>> assump = CNF.from_prop(Q.nonzero(x))
    >>> get_all_relevant_facts(props, assump) #doctest: +SKIP
    <sympy.assumptions.cnf.EncodedCNF at 0x7f09faa6ccd0>

    """
    # The relevant facts might introduce new keys, e.g., Q.zero(x*y) will
    # introduce the keys Q.zero(x) and Q.zero(y), so we need to run it until
    # we stop getting new things. Hopefully this strategy won't lead to an
    # infinite loop in the future.
    i = 0
    relevant_facts = CNF()
    all_exprs = set()
    while True:
        if i == 0:
            exprs = extract_predargs(proposition, assumptions)
        all_exprs |= exprs
        exprs, relevant_facts = get_relevant_clsfacts(exprs, relevant_facts)
        i += 1
        if i >= iterations:
            break
        if not exprs:
            break

    if use_known_facts:
        known_facts_CNF = CNF()

        if any(expr.kind == MatrixKind(NumberKind) for expr in all_exprs):
            known_facts_CNF.add_clauses(get_all_known_matrix_facts())
        # check for undefinedKind since kind system isn't fully implemented
        if any(((expr.kind == NumberKind) or (expr.kind == UndefinedKind)) for expr in all_exprs):
            known_facts_CNF.add_clauses(get_all_known_number_facts())

        kf_encoded = EncodedCNF()
        kf_encoded.from_cnf(known_facts_CNF)

        def translate_literal(lit, delta):
            if lit > 0:
                return lit + delta
            else:
                return lit - delta

        def translate_data(data, delta):
            return [{translate_literal(i, delta) for i in clause} for clause in data]
        data = []
        symbols = []
        n_lit = len(kf_encoded.symbols)
        for i, expr in enumerate(all_exprs):
            symbols += [pred(expr) for pred in kf_encoded.symbols]
            data += translate_data(kf_encoded.data, i * n_lit)

        encoding = dict(list(zip(symbols, range(1, len(symbols)+1))))
        ctx = EncodedCNF(data, encoding)
    else:
        ctx = EncodedCNF()

    ctx.add_from_cnf(relevant_facts)

    return ctx
