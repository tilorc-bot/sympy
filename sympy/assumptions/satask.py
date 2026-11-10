"""
Module to evaluate the proposition with assumptions using SAT algorithm.
"""
from __future__ import annotations

from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.core.kind import NumberKind, UndefinedKind
from sympy.core.numbers import ImaginaryUnit, Number, NumberSymbol
from sympy.assumptions.ask import Q
from sympy.assumptions.ask_generated import get_all_known_matrix_facts, get_all_known_number_facts
from sympy.assumptions.assume import AppliedPredicate
from sympy.assumptions.compiled_rules import (RELATIONS, WRITTEN, canonical,
    rule_arguments, split_sat_rules)
from sympy.core import oo
from sympy.assumptions.cnf import CNF, EncodedCNF, Literal
from sympy.matrices.kind import MatrixKind
from sympy.assumptions.reasoning_engine import ReasoningEngine

_number_properties = {
    Q.positive: 'is_positive',
    Q.zero: 'is_zero',
    Q.negative: 'is_negative',
    Q.rational: 'is_rational',
    Q.irrational: 'is_irrational',
    Q.even: 'is_even',
    Q.odd: 'is_odd',
    Q.imaginary: 'is_imaginary',
    Q.prime: 'is_prime',
    Q.composite: 'is_composite',
}


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

    engine = ReasoningEngine(sat)
    query_literal = engine.create_query(props, _props)

    if early_return:
        res = engine.fixed(query_literal)
        if res is not None:
            return res

    return engine.ask_query(query_literal)


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


def get_relevant_clsfacts(exprs, relevant_facts=None, relations=None):
    """
    Extract relevant facts from the items in *exprs*. Facts come from the
    rules in ``assumptions.rules`` package, in their compiled form, and from
    the numbers among *exprs* themselves.

    A condition of a rule between two arguments, such as ``Q.eq(i, j)``, is
    decided from the form of the arguments if it can be. Otherwise the rule
    is kept only if one of the relations which can make the condition false,
    such as ``Q.eq(i, j)``, ``Q.eq(j, i)`` and ``Q.gt(i, j)`` for
    ``Q.eq(i, j)``, is in *relations*. The condition is then kept as a
    predicate of the two, which is linked to those relations.

    This function is recursively called by ``get_all_relevant_facts()``.

    Parameters
    ==========

    exprs : set
        Expressions whose relevant facts are searched.

    relevant_facts : sympy.assumptions.cnf.CNF, optional.
        Pre-discovered relevant facts. They are updated in place.

    relations : dict, optional.
        The relations of two expressions which the query is about, as
        ``{(relation, a, b): clauses}``, with each relation one of
        ``Q.eq``, ``Q.gt`` and ``Q.ge``, and the clauses which link it to
        the predicates of the query that state it.

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

    >>> from sympy import Abs, Q
    >>> from sympy.assumptions.cnf import Literal
    >>> from sympy.assumptions.satask import get_relevant_clsfacts
    >>> from sympy.abc import x, y
    >>> exprs = {Abs(x*y)}
    >>> exprs, facts = get_relevant_clsfacts(exprs)
    >>> exprs
    {x*y}
    >>> frozenset({Literal(Q.even(x*y), True), Literal(Q.even(Abs(x*y)), False)}) in facts.clauses
    True

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
    if relations is None:
        relations = {}

    newexprs = set()
    for expr in exprs:
        args = rule_arguments(expr)
        rules, related = split_sat_rules(type(expr), len(args))
        if rules or related:
            targets = (*args, expr)
            relevant_facts.clauses.update(
                frozenset(Literal(predicate(targets[slot]), not value)
                          for predicate, slot, value in clause)
                for clause in rules)
            if related:
                relevant_facts.clauses.update(
                    _related_clauses(related, targets, relations))
            newexprs.update(args)
        if isinstance(expr, (Number, NumberSymbol, ImaginaryUnit)):
            for predicate, name in _number_properties.items():
                value = getattr(expr, name)
                if value is not None:
                    relevant_facts.clauses.add(
                        frozenset((Literal(predicate(expr), not value),)))

    return newexprs - exprs, relevant_facts


def _related_clauses(clauses, targets, relations):
    found = set()
    for clause in clauses:
        literals = []
        links = []
        for predicate, slot, value in clause:
            if type(slot) is not tuple:
                literals.append(Literal(predicate(targets[slot]), not value))
                continue
            a, b = (targets[s] if type(s) is int else s for s in slot)
            decide, deciders = RELATIONS[predicate]
            known = decide(a, b)
            if known is value:
                break
            if known is None:
                atom = predicate(a, b)
                kept = False
                for assumed, swapped, assumed_value, answer in deciders:
                    key = (assumed, b, a) if swapped else (assumed, a, b)
                    if answer is value or key not in relations:
                        continue
                    kept = True
                    links.extend(relations[key])
                    other = assumed(*key[1:])
                    if other != atom:
                        links.append(frozenset((Literal(other, assumed_value),
                                                Literal(atom, not answer))))
                if not kept:
                    break
                literals.append(Literal(atom, not value))
        else:
            found.add(frozenset(literals))
            found.update(links)
    return found


def _relations(atoms):
    """
    The relations of two expressions which *atoms* state, as the argument
    *relations* of :func:`get_relevant_clsfacts`.
    """
    relations: dict = {}
    for atom in atoms:
        if not isinstance(atom, AppliedPredicate):
            continue
        arguments = atom.arguments
        if len(arguments) == 2 and atom.function in WRITTEN:
            key, same = canonical(atom.function, *arguments)
            linked = relations.setdefault(key, set())
            other = key[0](*key[1:])
            if other != atom:
                linked.add(frozenset((Literal(atom, True), Literal(other, not same))))
                linked.add(frozenset((Literal(atom, False), Literal(other, same))))
    return relations


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
    relations = _relations(proposition.all_predicates() | assumptions.all_predicates())
    while True:
        if i == 0:
            exprs = extract_predargs(proposition, assumptions)
        all_exprs |= exprs
        exprs, relevant_facts = get_relevant_clsfacts(exprs, relevant_facts, relations)
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
