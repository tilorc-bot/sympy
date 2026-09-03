"""
Module to evaluate the proposition with assumptions using SAT algorithm.
"""
from __future__ import annotations

from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.core.kind import NumberKind, UndefinedKind
from sympy.assumptions.ask_generated import get_all_known_matrix_facts, get_all_known_number_facts
from sympy.assumptions.assume import AppliedPredicate
from sympy.assumptions.sathandlers import (_ARITHMETIC_READING,
    arithmetic_facts, class_fact_registry)
from sympy.logic.algorithms.lra_theory import LRA_PRED, LRASolver
from sympy.core import oo
from sympy.logic.algorithms.dpll2 import SATSolver, IpasirStatus
from sympy.assumptions.cnf import CNF, EncodedCNF
from sympy.matrices.kind import MatrixKind

# the atoms the theory reads, as `arithmetic_facts` emits them
_LRA_PREDICATES = frozenset(LRA_PRED.values())

# and the predicates it reads them from that relate two expressions, rather
# than stating the sign of one
_RELATION_PREDICATES = frozenset(pred for pred, (_, rhs)
                                 in _ARITHMETIC_READING.items() if rhs is None)


def satask(proposition, assumptions=True, use_known_facts=True, iterations=oo,
           early_return=False):
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

    return check_satisfiability(props, _props, sat, early_return)


def check_satisfiability(prop, _prop, factbase, early_return=False):
    if {0} in factbase.data:
        raise ValueError("Inconsistent assumptions")

    true_false_guarded, selector = _encode_with_selector(prop, _prop, factbase)
    lra, conflicts = _lra_theory(true_false_guarded)

    # Run `propogate()` on the assumptions
    solver = _solver_for(true_false_guarded, selector, conflicts, lra)
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
    # A solver of its own, rather than `assume(-witnessed)` on the one that
    # just answered: an assumption is a decision the search is not allowed to
    # take back, so `_find_model` puts it on a level of its own that it makes
    # by hand rather than through `_create_level`. Nothing else in sympy calls
    # `assume()`, and one search saved is not worth being the only caller that
    # has to know that.
    witnessed = solver.val(selector)
    other_side = _solver_for(true_false_guarded, selector,
                             conflicts + [{-witnessed}], lra)
    other = other_side.solve() == IpasirStatus.SATISFIABLE

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


def _solver_for(true_false_guarded, selector, extra_clauses=(), lra=None):
    """A solver over *true_false_guarded*, whose last variable is *selector*.

    *extra_clauses* are added to the ones the encoding already carries. *lra*
    is handed over as it was built, since the solver about to read it starts
    from the root level.
    """
    if lra is not None:
        lra.reset()
    return SATSolver(true_false_guarded.data + list(extra_clauses),
                     range(1, selector + 1), set(),
                     true_false_guarded.symbols + [selector], lra_theory=lra)


def _lra_theory(encoded_cnf):
    """Build a theory solver for *encoded_cnf*, if its atoms could relate
    anything, along with the clauses it knows before any search.

    Explanation
    ===========

    Sign predicates about one expression are already related to each other by
    the known facts, and the bridge gives each of them the atom the theory
    would, so a problem built out of those alone costs time and learns
    nothing new: `Q.positive(x)` contradicting `Q.negative(x)` is something
    the SAT solver settles on its own. Two of them about different
    expressions built from a common symbol are another matter, and so is a
    relation -- `Q.le(x, 0)` appears in no known fact at all, so one of those
    is reason enough on its own.

    Whether a predicate is one or the other is asked of the predicate the
    bridge read, not of the atom it produced: `Q.le(x, 0)` and
    `Q.nonpositive(x)` become the same atom and are not the same question.

    """
    sides = []
    relation = False
    for pred in encoded_cnf.encoding:
        if not isinstance(pred, AppliedPredicate):
            continue
        if pred.function in _LRA_PREDICATES:
            sides.append(pred.arguments[0])
        elif pred.function in _RELATION_PREDICATES:
            relation = True

    if not sides:
        return None, []
    if not relation and not _relates_expressions(sides):
        return None, []
    return _build_lra_theory(encoded_cnf)


def _build_lra_theory(encoded_cnf):
    # satask reads the theory's verdict and never its model, so the atoms it
    # cannot hold as independent variables are relaxed rather than dropped;
    # see `LRASolver.from_encoded_cnf`.
    lra, conflicts = LRASolver.from_encoded_cnf(encoded_cnf, realizable_models=False)
    return lra, [set(clause) for clause in conflicts + lra.bound_conflicts()]


def _relates_expressions(exprs):
    """Whether two of *exprs* are different expressions built from a common
    symbol.
    """
    seen = []
    for expr in exprs:
        if any(expr != other and expr.free_symbols & other.free_symbols
               for other in seen):
            return True
        seen.append(expr)

    return False


def _encode_with_selector(prop, _prop, factbase):
    """Return *factbase* with the clauses of prop and _prop added to it, and
    the selector variable that activates prop when true and _prop when false.
    """
    true_false_guarded = factbase.copy()
    sides = [[true_false_guarded.encode(clause) for clause in side.clauses]
             for side in (prop, _prop)]

    # One past the last predicate, so the selector is a variable of its own.
    selector = len(true_false_guarded.encoding) + 1

    for clauses, guard in zip(sides, (-selector, selector)):
        # Dropping the 0 that encodes False leaves a side nothing can satisfy
        # as the unit {guard}.
        true_false_guarded.data += [(clause - {0}) | {guard}
                                    for clause in clauses]

    return true_false_guarded, selector


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
    return predicate_args(extract_predicates(proposition, assumptions))


def predicate_args(predicates):
    """Return every expression in the arguments of *predicates*."""
    exprs = set()
    for key in predicates:
        if isinstance(key, AppliedPredicate):
            exprs |= set(key.arguments)
        else:
            exprs.add(key)
    return exprs


def extract_predicates(proposition, assumptions=None):
    """
    Extract every predicate of *proposition* and *assumptions* that is
    relevant to *proposition*.

    Parameters
    ==========

    proposition : sympy.assumptions.cnf.CNF

    assumptions : sympy.assumptions.cnf.CNF, optional.

    Examples
    ========

    >>> from sympy import Q, Abs
    >>> from sympy.assumptions.cnf import CNF
    >>> from sympy.assumptions.satask import extract_predicates
    >>> from sympy.abc import x, y
    >>> props = CNF.from_prop(Q.zero(Abs(x*y)))
    >>> assump = CNF.from_prop(Q.zero(x))
    >>> extract_predicates(props, assump) == {Q.zero(Abs(x*y)), Q.zero(x)}
    True

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

    return keys

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


def get_relevant_predfacts(predicates, relevant_facts=None):
    """
    Extract the facts registered for the applied predicates in *predicates*.

    Parameters
    ==========

    predicates : set of AppliedPredicate

    relevant_facts : sympy.assumptions.cnf.CNF, optional
        Return this with the extracted facts added to it.

    Returns
    =======

    (predicates, relevant_facts)

    predicates : set of AppliedPredicate
        The predicates the extracted facts mention that were not given.

    relevant_facts : sympy.assumptions.cnf.CNF

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.assumptions.satask import get_relevant_predfacts
    >>> from sympy.abc import x
    >>> new, facts = get_relevant_predfacts({Q.positive(x)})
    >>> sorted(new, key=str)
    [Q.real(x), lra_gt(x, 0)]

    """
    if not relevant_facts:
        relevant_facts = CNF()

    newpredicates = set()
    for pred in predicates:
        for fact in arithmetic_facts(pred):
            newfact = CNF.to_CNF(fact)
            relevant_facts = relevant_facts._and(newfact)
            newpredicates |= newfact.all_predicates()

    return newpredicates - predicates, relevant_facts


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
            # Both passes read the same relevant predicates, so they are
            # found once rather than once each.
            predicates = extract_predicates(proposition, assumptions)
            exprs = predicate_args(predicates)
        all_exprs |= exprs
        exprs, relevant_facts = get_relevant_clsfacts(exprs, relevant_facts)
        predicates, relevant_facts = get_relevant_predfacts(predicates, relevant_facts)
        # A predicate fact may name an expression nothing has classified yet
        # -- `Q.real(x + y)` for `Q.positive(x + y)` -- so its arguments go
        # back round with the rest. Without this a handler could only ever
        # mention what it was handed, which is a rule nothing states.
        exprs |= predicate_args(predicates) - all_exprs
        i += 1
        if i >= iterations:
            break
        if not exprs and not predicates:
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
