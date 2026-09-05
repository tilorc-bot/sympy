"""
Module to evaluate the proposition with assumptions using SAT algorithm.
"""
from __future__ import annotations

from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.core.kind import NumberKind, UndefinedKind
from sympy.assumptions.ask_generated import get_all_known_matrix_facts, get_all_known_number_facts
from sympy.assumptions.assume import AppliedPredicate
from sympy.assumptions.sathandlers import class_fact_registry
from sympy.core import oo
from sympy.logic.algorithms.dpll2 import SATSolver, IpasirStatus
from sympy.assumptions.cnf import CNF, EncodedCNF
from sympy.matrices.kind import MatrixKind


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


class ReasoningEngine:
    """A SAT solver asked about a proposition and the facts deciding it.

    The engine encodes the proposition, its negation and *factbase* into one
    solver, guarding the two sides of the question with a selector variable
    so that both can be asked of that solver. Building it propagates
    everything the facts imply on their own, which is what :meth:`lookup`
    reads and what :meth:`entailed` answers from; :meth:`decide` then runs
    the search.

    Parameters
    ==========

    factbase : sympy.assumptions.cnf.EncodedCNF
        The assumptions, together with every fact relevant to them.

    prop : sympy.assumptions.cnf.CNF
        The proposition to decide.

    _prop : sympy.assumptions.cnf.CNF
        The negation of *prop*. Negating a CNF is not free, so the caller
        passes the one it has already built.

    Raises
    ======

    ValueError
        If *factbase* is contradictory, as far as propagation can tell.

    TODO: the proposition is fixed at construction because ``SATSolver``
    cannot be given new variables once it exists, and the proposition brings
    new ones: the selector always, and any predicate of its own that the
    facts do not already carry. Once the solver can take them, ``_ask``
    becomes a public ``ask`` that ``__init__`` no longer calls, and one
    engine answers several propositions against facts it has propagated once.

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.abc import x
    >>> from sympy.assumptions.cnf import CNF
    >>> from sympy.assumptions.satask import (ReasoningEngine,
    ...     get_all_relevant_facts)
    >>> prop, _prop = CNF.from_prop(Q.nonzero(x)), CNF.from_prop(~Q.nonzero(x))
    >>> assumptions = CNF.from_prop(Q.positive(x))
    >>> factbase = get_all_relevant_facts(prop, assumptions)
    >>> factbase.add_from_cnf(assumptions)
    >>> engine = ReasoningEngine(factbase, prop, _prop)
    >>> engine.lookup(Q.real(x))
    True
    >>> engine.decide()
    True

    """
    def __init__(self, factbase, prop, _prop):
        if {0} in factbase.data:
            raise ValueError("Inconsistent assumptions")

        # The facts are what an engine that could be asked again would keep.
        self._factbase = factbase
        self._ask(prop, _prop)

    def _ask(self, prop, _prop):
        """Put a question to the facts, propagating what they imply.

        This is the ``ask`` of the TODO above, called from ``__init__`` for
        as long as a question can only be put to a solver of its own.
        """
        self._prop = prop
        self._negation = _prop

        guarded, self._selector = _encode_with_selector(prop, _prop,
                                                        self._factbase)
        self._encoding = guarded.encoding
        self._solver = SATSolver(guarded.data, range(1, self._selector + 1),
                                 set(), guarded.symbols + [self._selector])

        # Run `propogate()` on the assumptions. The guarded clauses say no
        # more than `selector <-> prop`, which ties the selector to the
        # predicates without constraining them, so what propagation fixes
        # among the predicates is what the facts imply and nothing else.
        # Fixing the selector itself is not ruled out, and is what happens
        # whenever the facts already decide the proposition.
        if self._solver.propagate() == IpasirStatus.UNSATISFIABLE:
            raise ValueError("Inconsistent assumptions")

    def lookup(self, pred):
        """Return what propagating the facts fixed *pred* to.

        The answer is ``True`` if the facts imply *pred*, ``False`` if they
        imply its negation, and ``None`` if they leave it open, which is also
        the answer for a *pred* the engine never encoded. Nothing is searched
        for, so this is an O(1) operation.

        What it reports is what the facts imply on their own. The
        proposition is in the same solver, but it cannot fix a predicate that
        the facts leave open, for the reason given in ``__init__``.

        It answers only until :meth:`decide` has run: past that the solver
        holds the assignments of a model rather than those of the root level,
        and asking raises a ``ValueError``.

        Parameters
        ==========

        pred : sympy.assumptions.assume.AppliedPredicate
            A predicate applied to an expression, such as ``Q.real(x)``.

        Examples
        ========

        >>> from sympy import Q
        >>> from sympy.abc import x
        >>> from sympy.assumptions.cnf import CNF
        >>> from sympy.assumptions.satask import (ReasoningEngine,
        ...     get_all_relevant_facts)
        >>> prop, _prop = CNF.from_prop(Q.zero(x)), CNF.from_prop(~Q.zero(x))
        >>> assumptions = CNF.from_prop(Q.positive(x))
        >>> factbase = get_all_relevant_facts(prop, assumptions)
        >>> factbase.add_from_cnf(assumptions)
        >>> engine = ReasoningEngine(factbase, prop, _prop)

        Being positive fixes being real and rules out being negative, while
        saying nothing either way about being an integer.

        >>> engine.lookup(Q.real(x))
        True
        >>> engine.lookup(Q.negative(x))
        False
        >>> engine.lookup(Q.integer(x)) is None
        True

        """
        lit = self._encoding.get(pred)
        if lit is None:
            return None

        return {1: True, -1: False, 0: None}[self._solver.fixed(lit)]

    def entailed(self):
        """Return what the literals fixed so far make of the proposition.

        The answer is ``True`` or ``False`` if they already decide it, and
        ``None`` if deciding it needs the search that :meth:`decide` runs.

        This trusts the facts to be consistent. Propagation does not show up
        every contradiction, and contradictory facts entail the proposition
        whichever way it is asked.

        """
        entailed = self._solver._is_entailed(self._prop.clauses, self._encoding)
        if entailed is not None:
            return entailed

        entailed = self._solver._is_entailed(self._negation.clauses,
                                             self._encoding)
        if entailed is not None:
            return not entailed

        return None

    def decide(self):
        """Search for a model of each side of the question and answer from
        the sides that have one.

        The answer is ``True`` or ``False`` if only the proposition or only
        its negation has a model, and ``None`` if both do. The search
        continues from the work that building the engine already did.

        """
        # Continue on the propogated solver, just call solve() on it.
        if self._solver.solve() == IpasirStatus.UNSATISFIABLE:
            raise ValueError("Inconsistent assumptions")

        # The model settles the side it activated, so ask about the other one.
        witnessed = self._solver.val(self._selector)
        self._solver.assume(-witnessed)
        other = self._solver.solve() == IpasirStatus.SATISFIABLE

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


def check_satisfiability(prop, _prop, factbase, early_return=False):
    engine = ReasoningEngine(factbase, prop, _prop)

    # Check whether proposition is entailed by any of the assigned literals.
    if early_return:
        entailed = engine.entailed()
        if entailed is not None:
            return entailed

    return engine.decide()


def _add_guarded(encoded, cnf, active):
    """Add the clauses of *cnf* to *encoded*, each of them guarded by the
    literal *active*, so that *cnf* holds when *active* is true and says
    nothing at all when it is false.
    """
    # Dropping the 0 that encodes False leaves a clause nothing can satisfy as
    # the unit {-active}, which is what stops *active* from being true.
    encoded.data += [(encoded.encode(clause) - {0}) | {-active}
                     for clause in cnf.clauses]


def _encode_with_selector(prop, _prop, factbase):
    """Return *factbase* with the clauses of prop and _prop added to it, and
    the selector variable that activates prop when true and _prop when false.
    """
    true_false_guarded = factbase.copy()

    # Number the predicates of both sides before choosing the selector. Doing
    # it after would give the selector a number that encoding the second side
    # still hands out to a predicate.
    for clause in (*prop.clauses, *_prop.clauses):
        true_false_guarded.encode(clause)

    # One past the last predicate, so the selector is a variable of its own.
    selector = len(true_false_guarded.encoding) + 1

    _add_guarded(true_false_guarded, prop, selector)
    _add_guarded(true_false_guarded, _prop, -selector)

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
