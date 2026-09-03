"""Implements "A Fast Linear-Arithmetic Solver for DPLL(T)"

The LRASolver class defined in this file can be used
in conjunction with a SAT solver to check the
satisfiability of formulas involving inequalities.

Here's an example of how that would work:

    Suppose you want to check the satisfiability of
    the following formula:

    >>> from sympy.core.relational import Eq
    >>> from sympy.abc import x, y
    >>> f = ((x > 0) | (x < 0)) & (Eq(x, 0) | Eq(y, 1)) & (~Eq(y, 1) | Eq(1, 2))

    First a preprocessing step should be done on f. Unequality like
    `~Eq(y, 1)` should be split. Predicates such as `Q.prime` that the
    solver has no reading for do not need to be removed: they simply go
    unconstrained by the theory.

    I should mention that the paper says to split both equalities and
    unequality, but this implementation only requires that unequality
    be split.

    >>> f = ((x > 0) | (x < 0)) & (Eq(x, 0) | Eq(y, 1)) & ((y < 1) | (y > 1) | Eq(1, 2))

    Then an LRASolver instance needs to be initialized with this formula.
    The solver reads only its own predicates, so the encoding is translated
    with `assume_real` first. That is the step where the caller claims that
    the arguments of every relation in f are real numbers.

    >>> from sympy.assumptions.cnf import CNF, EncodedCNF
    >>> from sympy.assumptions.ask import Q
    >>> from sympy.logic.algorithms.lra_theory import LRASolver, assume_real
    >>> cnf = CNF.from_prop(f)
    >>> enc = EncodedCNF()
    >>> enc.add_from_cnf(cnf)
    >>> lra, conflicts = LRASolver.from_encoded_cnf(assume_real(enc))

    Any immediate one-lital conflicts clauses will be detected here.
    In this example, `~Eq(1, 2)` is one such conflict clause. We'll
    want to add it to `f` so that the SAT solver is forced to
    assign Eq(1, 2) to False.

    >>> f = f & ~Eq(1, 2)

    Now that the one-literal conflict clauses have been added
    and an lra object has been initialized, we can pass `f`
    to a SAT solver. The SAT solver will give us a satisfying
    assignment such as:

    (1 = 2): False
    (y = 1): True
    (y < 1): True
    (y > 1): True
    (x = 0): True
    (x < 0): True
    (x > 0): True

    Next you would pass this assignment to the LRASolver
    which will be able to determine that this particular
    assignment is satisfiable or not.

    Note that since EncodedCNF is inherently non-deterministic,
    the int each predicate is encoded as is not consistent. As a
    result, the code below likely does not reflect the assignment
    given above.

    >>> lra.assert_lit(-1) #doctest: +SKIP
    >>> lra.assert_lit(2) #doctest: +SKIP
    >>> lra.assert_lit(3) #doctest: +SKIP
    >>> lra.assert_lit(4) #doctest: +SKIP
    >>> lra.assert_lit(5) #doctest: +SKIP
    >>> lra.assert_lit(6) #doctest: +SKIP
    >>> lra.assert_lit(7) #doctest: +SKIP
    >>> is_sat, conflict_or_assignment = lra.check()

    As the particular assignment suggested is not satisfiable,
    the LRASolver will return unsat and a conflict clause when
    given that assignment. The conflict clause will always be
    minimal, but there can be multiple minimal conflict clauses.
    One possible conflict clause could be `~(x < 0) | ~(x > 0)`.

    We would then add whatever conflict clause is given to
    `f` to prevent the SAT solver from coming up with an
    assignment with the same conflicting literals. In this case,
    the conflict clause `~(x < 0) | ~(x > 0)` would prevent
    any assignment where both (x < 0) and (x > 0) were both
    true.

    The SAT solver would then find another assignment
    and we would check that assignment with the LRASolver
    and so on. Eventually either a satisfying assignment
    that the SAT solver and LRASolver agreed on would be found
    or enough conflict clauses would be added so that the
    boolean formula was unsatisfiable.


This implementation is based on [1]_, which includes a
detailed explanation of the algorithm and pseudocode
for the most important functions.

[1]_ also explains how backtracking and theory propagation
could be implemented to speed up the current implementation,
but these are not currently implemented.

TODO:
 - Handle non-rational real numbers
 - Handle positive and negative infinity
 - Implement backtracking and theory propagation

References
==========

.. [1] Dutertre, B., de Moura, L.:
       A Fast Linear-Arithmetic Solver for DPLL(T)
       https://link.springer.com/chapter/10.1007/11817963_11
"""
from __future__ import annotations
from sympy.solvers.solveset import linear_eq_to_matrix
from sympy.matrices.dense import eye
from sympy.assumptions import Predicate
from sympy.assumptions.assume import AppliedPredicate
from sympy.assumptions.ask import Q
from sympy.assumptions.cnf import EncodedCNF
from sympy.core import Dummy
from sympy.core.mul import Mul
from sympy.core.add import Add
from sympy.core.relational import Eq, Ge, Gt, Le, Lt, Relational
from sympy.core.symbol import Str
from sympy.core.sympify import sympify
from sympy.core.singleton import S
from sympy.core.numbers import Rational, oo
from sympy.matrices.dense import Matrix
from sympy.utilities.iterables import sift
import math


class UnhandledInput(Exception):
    """
    Raised while creating an LRASolver if non-linearity
    or non-rational numbers are present.
    """

# the relations that can be read as real arithmetic, and the relational
# each one is normalized with. LRASolver reads the predicates of LRA_PRED
# below rather than these; see _LRARelation.
ALLOWED_PRED = {Q.eq: Eq, Q.gt: Gt, Q.lt: Lt, Q.le: Le, Q.ge: Ge}


class _LRARelation(Predicate):
    """
    A relation that LRASolver reads as a constraint on real numbers.

    Explanation
    ===========

    These predicates are deliberately not attached to ``Q``. ``Q.gt(x, y)``
    says nothing about ``x`` and ``y`` being real numbers -- ``oo > 0`` is
    ``True`` -- so a solver that reads it has to decide for itself whether
    the arithmetic applies. ``_lra_gt(x, y)`` means "``x - y`` is a positive
    real number" and nothing else, so only a caller that has already decided
    the arguments are real numbers builds one, and ``from_encoded_cnf`` can
    read one without checking anything about its arguments.

    Use ``assume_real`` to translate an encoding of ordinary relations into
    these, or ``LRA_PRED`` to build one directly.

    """
    def __new__(cls, name):
        if not isinstance(name, Str):
            name = Str(name)
        return super().__new__(cls, name)

    @property
    def name(self):
        return self.args[0]

    def _hashable_content(self):
        return (self.name,)

    def _sympystr(self, printer, *args):
        # not "Q.lra_gt": there is no such attribute of Q to print
        return str(self.name)


_lra_eq = _LRARelation("lra_eq")
_lra_gt = _LRARelation("lra_gt")
_lra_lt = _LRARelation("lra_lt")
_lra_ge = _LRARelation("lra_ge")
_lra_le = _LRARelation("lra_le")

# the theory's own predicate for each relation of ALLOWED_PRED
LRA_PRED = {Q.eq: _lra_eq, Q.gt: _lra_gt, Q.lt: _lra_lt,
            Q.le: _lra_le, Q.ge: _lra_ge}

# the relational each one is normalized with, as in ALLOWED_PRED
_PRED_RELATIONAL = {_lra_eq: Eq, _lra_gt: Gt, _lra_lt: Lt,
                    _lra_le: Le, _lra_ge: Ge}

# and the other way around, for a relation written as ``x > y``
_RELATIONAL_PRED = {rel: pred for pred, rel in _PRED_RELATIONAL.items()}

# if true ~Q.gt(x, y) implies Q.le(x, y)
HANDLE_NEGATION = True


def _as_lra_relation(prop):
    """
    Return *prop* as one of the theory's own relations, or ``None`` if it
    is not a relation.
    """
    if isinstance(prop, AppliedPredicate):
        pred, args = LRA_PRED.get(prop.function), prop.arguments
    elif isinstance(prop, Relational):
        pred, args = _RELATIONAL_PRED.get(type(prop)), prop.args
    else:
        return None
    if pred is None or len(args) != 2:
        return None
    return pred(*args)


def assume_real(encoded_cnf):
    """
    Return *encoded_cnf* with every relation in it read as an arithmetic
    constraint on real numbers.

    Explanation
    ===========

    ``LRASolver.from_encoded_cnf`` only reads the predicates of
    ``LRA_PRED``, so an encoding whose relations are the ordinary ``Q.gt``,
    ``x > y`` and the like has to be translated before it is handed over.
    Translating asserts that the arguments of every relation in the encoding
    are real numbers, which is a claim about the formula that only its
    caller can make -- hence a separate step rather than something the
    solver does on its own.

    Atom ids are left alone, so the boundaries of a solver built from the
    result line up with the literals of *encoded_cnf*.

    Examples
    ========

    >>> from sympy.abc import x
    >>> from sympy.assumptions.cnf import CNF, EncodedCNF
    >>> from sympy.logic.algorithms.lra_theory import assume_real
    >>> enc = EncodedCNF()
    >>> enc.from_cnf(CNF.from_prop(x > 0))
    >>> enc.encoding
    {Q.gt(x, 0): 1}
    >>> assume_real(enc).encoding
    {lra_gt(x, 0): 1}

    """
    encoding = {}
    for prop, atom_id in encoded_cnf.encoding.items():
        relation = _as_lra_relation(prop)
        # Two relations can only translate to the same one if they were
        # already equivalent, and the solver still needs to tell the two
        # atoms apart, so the second one is left as it is and skipped.
        if relation is not None and relation not in encoding:
            prop = relation
        encoding[prop] = atom_id
    return EncodedCNF(encoded_cnf.data, encoding)


def _normalize_prop(prop):
    """
    Return ``(vars, const, var_coeff, terms)`` for the constraint *prop*
    places on ``lhs - rhs``, ``S.true`` or ``S.false`` if it is constant, or
    ``None`` if the theory cannot read it.
    """
    if len(prop.arguments) != 2:
        return None
    lhs, rhs = prop.arguments

    if lhs == S.NaN or rhs == S.NaN:
        return None
    if lhs.is_imaginary or rhs.is_imaginary:
        return None
    if lhs == oo or rhs == oo:
        return None

    expr = lhs - rhs
    pred = _PRED_RELATIONAL[prop.function](expr, S.Zero)
    if pred == True:
        return S.true
    if pred == False:
        return S.false
    if not expr.free_symbols:
        return None

    if prop.function in [_lra_ge, _lra_gt]:
        expr = -expr

    # Example: 2x + 3y, 2 <- _sep_const_terms(2x + 3y + 2)
    vars, const = _sep_const_terms(expr)
    # Examples:
    # x, 2 <- _sep_const_coeff(2x)
    # 2x + 3y, 1 <- _sep_const_coeff(2x + 3y + 2)
    vars, var_coeff = _sep_const_coeff(vars)
    const = const / var_coeff
    # Example: [2x, 3y] <- Add.make_args(2x + 3y)
    terms = Add.make_args(vars)

    # Every number the tableau holds has to be rational -- the bound of each
    # boundary, and each entry of the matrix -- so an atom whose numbers are
    # not is one more the theory cannot read. It is skipped here alongside
    # the others rather than refused once the matrix exists: refusing cost
    # the caller every other atom of the formula as well, and since satask
    # builds a solver out of whatever a user asked about, the refusal came
    # back out of `ask()` and `refine()` as an exception.
    if not isinstance(const, Rational):
        return None
    # One term at a time, because `_sep_const_coeff` of an `Add` returns 1:
    # the `I` of `x + I*y` is in no coefficient but its own term's.
    if any(not isinstance(_sep_const_coeff(term)[1], Rational) for term in terms):
        return None
    # `var_coeff` was divided out and is not in the matrix, but its sign is
    # which way the boundary points, so it has to have one. `I*x` reaches
    # here as `x` with a coefficient of `I`.
    if var_coeff.is_extended_real is not True:
        return None

    return vars, const, var_coeff, terms


def _atom_complexity(atom):
    terms = atom[-1]
    return max(len(term.free_symbols) for term in terms), len(terms)


def _select_atoms(atoms):
    """
    Return the atoms of *atoms* that can share one linear problem.

    Explanation
    ===========

    The terms the solver takes as its variables have to be variable
    disjoint: ``x*y`` and ``x`` cannot both be variables of the same linear
    problem, and neither can the two terms of ``x + x**2``. Atoms are
    considered simplest first -- fewest symbols in a term, then fewest terms
    -- and one that would claim a symbol some other atom's term already owns
    is dropped. Ties are broken by the order the atoms are given in, so the
    selection is a function of the encoding.

    Dropping an atom leaves the solver with one constraint fewer, which can
    only cost it conflicts it would otherwise have found. Refusing the whole
    formula, which is what an earlier version did, costs the caller every
    other atom in it as well.
    """
    order = sorted(range(len(atoms)), key=lambda i: (_atom_complexity(atoms[i]), i))
    owner = {}  # symbol -> the term that owns it
    kept = []
    for i in order:
        terms = {_sep_const_coeff(term)[0] for term in atoms[i][-1]}
        claimed = {sym: term for term in terms for sym in term.free_symbols}
        if len(claimed) != sum(len(term.free_symbols) for term in terms):
            continue  # two terms of the atom itself share a symbol
        if any(owner.get(sym, term) != term for sym, term in claimed.items()):
            continue
        owner.update(claimed)
        kept.append(i)
    return [atoms[i] for i in sorted(kept)]


class LRASolver():
    """
    Linear Arithmetic Solver for DPLL(T) implemented with an algorithm based on
    the Dual Simplex method. Uses Bland's pivoting rule to avoid cycling.

    References
    ==========

    .. [1] Dutertre, B., de Moura, L.:
           A Fast Linear-Arithmetic Solver for DPLL(T)
           https://link.springer.com/chapter/10.1007/11817963_11
    """

    def __init__(self, A, slack_variables, nonslack_variables,
                 atom_id_to_boundaries, s_subs, testing_mode):
        """
        Use the "from_encoded_cnf" method to create a new LRASolver.
        """
        self.run_checks = testing_mode
        self.s_subs = s_subs  # used only for test_lra_theory.test_random_problems

        # `_normalize_prop` skips whatever it cannot give rational numbers
        # for, so by here these hold of every atom that was kept.
        assert all(isinstance(a, Rational) for a in A)
        assert all(isinstance(b.bound, Rational)
                   for bs in atom_id_to_boundaries.values() for b in bs)
        m, n = len(slack_variables), len(slack_variables)+len(nonslack_variables)
        if m != 0:
            assert A.shape == (m, n)
        if self.run_checks:
            assert A[:, n-m:] == -eye(m)

        self.atom_id_to_boundaries = atom_id_to_boundaries
        self.A = A
        self._A0 = A.copy() if self.run_checks else None
        # initially slack/basic and nonslack/nonbasic mean the same thing.
        # however, basic/nonbasic can be modified in process meanwhile slack/nonslack stays constant.
        self.basic = slack_variables
        self.nonbasic = set(nonslack_variables)

        self.all_var = nonslack_variables + slack_variables

        self.bound_history = [BoundLevel()]

    @staticmethod
    def from_encoded_cnf(encoded_cnf, testing_mode=False, realizable_models=True):
        """
        Creates an LRASolver from an EncodedCNF object
        and a list of conflict clauses for propositions
        that can be simplified to True or False.

        Explanation
        ===========

        Only the predicates of ``LRA_PRED`` are read as arithmetic; see
        ``assume_real`` for translating an encoding into those. Every other
        atom of *encoded_cnf* is skipped, and so is one this solver cannot
        take -- an infinite or imaginary side, or a term that would make the
        problem nonlinear. A skipped atom simply gets no boundary, which
        leaves the SAT solver free to assign it either way, so the theory
        admits every model it would otherwise have admitted and possibly
        more. Its caller therefore learns less than it might have, never
        something false.

        Parameters
        ==========

        encoded_cnf : EncodedCNF

        testing_mode : bool
            Setting testing_mode to True enables some slow assert statements
            and sorting to reduce nonterministic behavior.

        realizable_models : bool
            Whether a model this solver reports has to be one real numbers
            could produce. The terms it takes as its variables are variable
            disjoint when this is ``True``, which is what ``_select_atoms``
            makes them by dropping atoms; ``x*y`` and ``x`` cannot then be
            columns of the same problem. When it is ``False`` every atom is
            kept and ``x*y`` becomes a column of its own, unconnected to
            ``x`` and ``y``.

            That second problem is a relaxation of the first: every
            assignment to the symbols gives each column a value and
            satisfies every row, so its solutions include all of the real
            ones and some that are not real at all -- ``x = 0`` with
            ``x*y > 0``, say. A caller that reads a model has to say
            ``True`` here; one that only trusts ``check()`` reporting
            *unsatisfiable* -- infeasible under the relaxation is infeasible
            in the reals too -- can say ``False`` and keep the atoms that
            would otherwise have been dropped.

        Returns
        =======

        (lra, conflicts)

        lra : LRASolver

        conflicts : list
            Contains a one-literal conflict clause for each proposition
            that can be simplified to True or False.

        Example
        =======

        >>> from sympy.core.relational import Eq
        >>> from sympy.assumptions.cnf import CNF, EncodedCNF
        >>> from sympy.assumptions.ask import Q
        >>> from sympy.logic.algorithms.lra_theory import LRASolver, assume_real
        >>> from sympy.abc import x, y, z
        >>> phi = (x >= 0) & ((x + y <= 2) | (x + 2 * y - z >= 6))
        >>> phi = phi & (Eq(x + y, 2) | (x + 2 * y - z > 4))
        >>> phi = phi & Q.gt(2, 1)
        >>> cnf = CNF.from_prop(phi)
        >>> enc = EncodedCNF()
        >>> enc.from_cnf(cnf)
        >>> enc = assume_real(enc)
        >>> lra, conflicts = LRASolver.from_encoded_cnf(enc, testing_mode=True)
        >>> lra #doctest: +SKIP
        <sympy.logic.algorithms.lra_theory.LRASolver object at 0x7fdcb0e15b70>
        >>> conflicts #doctest: +SKIP
        [[4]]
        """
        # This function has three main jobs:
        # - pick out the atoms of the formula the theory can read
        # - preprocesses the formula into a matrix and single variable constraints
        # - create one-literal conflict clauses from predicates that are always True
        #   or always False such as Q.gt(3, 2)
        #
        # See the preprocessing section of "A Fast Linear-Arithmetic Solver for DPLL(T)"
        # for an explanation of how the formula is converted into a matrix
        # and a set of single variable constraints.

        atom_id_to_boundaries = {}
        A = []

        basic = []
        s_count = 0
        s_subs = {}
        nonbasic = []
        atom_vars = set()

        if testing_mode:
            # sort to reduce nondeterminism
            encoded_cnf_items = sorted(encoded_cnf.encoding.items(),
                                       key=lambda x: str(x))
        else:
            encoded_cnf_items = encoded_cnf.encoding.items()

        var_to_lra_var = {}
        conflicts = []
        atoms = []

        for prop, atom_id in encoded_cnf_items:
            if not isinstance(prop, AppliedPredicate):
                if prop == True:
                    conflicts.append([atom_id])
                elif prop == False:
                    conflicts.append([-atom_id])
                continue

            if prop.function not in _PRED_RELATIONAL:
                # An atom the theory has no reading for -- an ordinary
                # predicate, or a relation nobody claimed is about real
                # numbers -- is left to the SAT solver. It gets no boundary,
                # so `assert_lit` ignores it and it is free to be assigned
                # either way.
                continue

            normalized = _normalize_prop(prop)
            if normalized is None:
                continue
            if normalized is S.true:
                conflicts.append([atom_id])
                continue
            if normalized is S.false:
                conflicts.append([-atom_id])
                continue

            atoms.append((atom_id, prop.function) + normalized)

        if realizable_models:
            atoms = _select_atoms(atoms)

        for atom_id, function, vars, const, var_coeff, terms in atoms:
            for term in terms:
                term, _ = _sep_const_coeff(term)
                assert len(term.free_symbols) > 0
                if term not in var_to_lra_var:
                    var_to_lra_var[term] = LRAVariable(term)
                    nonbasic.append(term)

            if len(terms) > 1:
                if vars not in s_subs:
                    s_count += 1
                    d = Dummy(f"s{s_count}")
                    var_to_lra_var[d] = LRAVariable(d)
                    basic.append(d)
                    s_subs[vars] = d
                    A.append(vars - d)
                var = s_subs[vars]
            else:
                var = terms[0]

            atom_vars.add(var)

            assert var_coeff != 0

            equality = function == _lra_eq
            strict = function in [_lra_gt, _lra_lt]
            if equality:
                b1 = Boundary(var_to_lra_var[var], -const, True, False)  # x <= c
                b2 = Boundary(var_to_lra_var[var], -const, False, False) # x >= c
                atom_id_to_boundaries[atom_id] = [b1, b2]
            else:
                upper = var_coeff > 0
                b = Boundary(var_to_lra_var[var], -const, upper, strict)
                atom_id_to_boundaries[atom_id] = [b]

        fs = [v.free_symbols for v in nonbasic + basic]
        assert all(len(syms) > 0 for syms in fs)
        if realizable_models:
            # `_select_atoms` has already dropped whatever was not linear
            fs_count = sum(len(syms) for syms in fs)
            assert len(fs) == 0 or len(set.union(*fs)) == fs_count

        A, _ = linear_eq_to_matrix(A, nonbasic + basic)
        # matrix A is guaranteed to able to be simplified
        # by removing the non-basic (e.g original or nonslack) non-atom variables from it
        # these removed variables will be replaced by linear equation of existing variables.
        nonatom_vars = {i for i in nonbasic if i not in atom_vars}
        A, basic, nonbasic = _reduce_matrix(A, basic, nonbasic, nonatom_vars, testing_mode)
        nonbasic = [var_to_lra_var[nb] for nb in nonbasic]
        basic = [var_to_lra_var[b] for b in basic]
        for idx, var in enumerate(nonbasic + basic):
            var.col_idx = idx

        solver = LRASolver(A, basic, nonbasic, atom_id_to_boundaries,
                           s_subs, testing_mode)
        return solver, conflicts

    def reset(self):
        """
        Resets the state of the LRASolver to before
        anything was asserted.
        """
        for var in self.all_var:
            var.initialize()
        self.bound_history = [BoundLevel()]

    def assert_lit(self, literal):
        """
        Assert a literal representing a constraint
        and update the internal state accordingly.

        Note that due to peculiarities of this implementation
        asserting ~(x > 0) will assert (x <= 0) but asserting
        ~Eq(x, 0) will not do anything.

        Parameters
        ==========

        literal : int
            A mapping of IDs to constraints
            can be found in `self.atom_id_to_boundaries`.

        Returns
        =======

        None or (False, explanation)

        explanation : set of ints
            A conflict clause that "explains" why
            the literals asserted so far are unsatisfiable.
        """
        if abs(literal) not in self.atom_id_to_boundaries:
            return None

        if not HANDLE_NEGATION and literal < 0:
            return None

        boundaries = self.atom_id_to_boundaries[abs(literal)]
        is_literal_negated = literal < 0

        if len(boundaries) > 1 and is_literal_negated:
            # Negated equality is not handled and should only appear in
            # conflict clauses.
            return None

        res = None
        for boundary in boundaries:
            res = self._assert_bound(boundary, literal)
            if res and res[0] is False:
                break

        return res

    def _assert_bound(self, boundary, literal):
        """
        Adjusts the upper or lower bound on variable xi if the new bound is
        more limiting. The assignment of variable xi is adjusted to be
        within the new bound if needed.

        Also calls `self._update` to update the assignment for basic variables
        to keep all equalities satisfied.

        This method is the combination of AssertUpper and AssertLower in [1]
        """
        xi = boundary.var
        ci, upper = boundary.to_rational(is_negated=literal < 0)

        s = 1 if upper else -1
        target_bound = xi.upper if upper else xi.lower
        opposing_bound = xi.lower if upper else xi.upper
        conflicting_lit = xi.lower_literal if upper else xi.upper_literal

        # If asserting lower bound, convert to equivalent upper bound situation
        # to simplify logic.
        c_norm = ci * s
        target_norm = target_bound * s
        opposing_norm = opposing_bound * s

        # Return `None` if new constraint is weaker than existing constraint.
        if c_norm >= target_norm:
            return None

        # Return conflict if new constraint directly conflicts with opposing constraint.
        if c_norm < opposing_norm:
            assert (opposing_bound.d * s >= 0) is True
            assert (ci.d * s <= 0) is True

            return False, [-conflicting_lit, -literal]

        self.bound_history[-1].record(xi, upper)

        xi.set_bound(boundary, literal)

        if xi in self.nonbasic and xi.assign * s > c_norm:
            self._update(xi, ci)

        if self.run_checks and all(not math.isinf(v.assign.q)
                                   for v in self.all_var):
            X = Matrix([v.assign.q for v in self.all_var])
            assert all(abs(val) < 10 ** (-10) for val in self._A0 * X)

        return None

    def _update(self, xi, v):
        """
        Updates all basic variables that have equations that contain
        nonbasic variable xi so that they stay satisfied given xi is equal to v.
        """
        i = xi.col_idx
        assert i is not None
        dv = v - xi.assign
        for j, b in enumerate(self.basic):
            a_ji = self.A[j, i]
            b.assign = b.assign + dv*a_ji
        xi.assign = v

    def check(self):
        """
        Searches for an assignment that satisfies all constraints
        or determines that no such assignment exists and gives
        a minimal conflict clause that "explains" why the
        constraints are unsatisfiable.

        Returns
        =======

        (True, assignment) or (False, explanation)

        assignment : dict of LRAVariables to values
            Assigned values are tuples that represent a rational number
            plus some infinatesimal delta.

        explanation : set of ints
        """
        while True:
            if self.run_checks:
                # nonbasic variables must always be within bounds
                assert all(((nb.assign >= nb.lower) == True) and ((nb.assign <= nb.upper) == True) for nb in self.nonbasic)

                # assignments for x must always satisfy Ax = 0
                # probably have to turn this off when dealing with strict ineq
                if all(not math.isinf(v.assign.q) for v in self.all_var):
                    X = Matrix([v.assign.q for v in self.all_var])
                    assert all(abs(val) < 10**(-10) for val in self._A0*X)

                # check upper and lower match this format:
                # x <= rat + delta iff x < rat
                # x >= rat - delta iff x > rat
                # this wouldn't make sense:
                # x <= rat - delta
                # x >= rat + delta
                assert all(x.upper.d <= 0 for x in self.all_var)
                assert all(x.lower.d >= 0 for x in self.all_var)

            cand = [(r, b) for r, b in enumerate(self.basic)
                    if b.assign < b.lower or b.assign > b.upper]
            if not cand:
                return True, {v: v.assign for v in self.all_var}
            i, xi = min(cand, key=lambda t: t[1].col_idx)  # Bland's rule

            if xi.assign < xi.lower:
                cand = [nb for nb in self.nonbasic
                        if (self.A[i, nb.col_idx] > 0 and nb.assign < nb.upper)
                        or (self.A[i, nb.col_idx] < 0 and nb.assign > nb.lower)]
                if len(cand) == 0:
                    N_plus = [nb for nb in self.nonbasic if self.A[i, nb.col_idx] > 0]
                    N_minus = [nb for nb in self.nonbasic if self.A[i, nb.col_idx] < 0]

                    conflict = []
                    conflict += [nb.upper_literal for nb in N_plus]
                    conflict += [nb.lower_literal for nb in N_minus]
                    conflict.append(xi.lower_literal)
                    conflict = [-conflicting_lit for conflicting_lit in conflict]
                    return False, conflict
                xj = min(cand, key=str)
                self._pivot_and_update(i, xi, xj, xi.lower)

            if xi.assign > xi.upper:
                cand = [nb for nb in self.nonbasic
                        if (self.A[i, nb.col_idx] < 0 and nb.assign < nb.upper)
                        or (self.A[i, nb.col_idx] > 0 and nb.assign > nb.lower)]

                if len(cand) == 0:
                    N_plus = [nb for nb in self.nonbasic if self.A[i, nb.col_idx] > 0]
                    N_minus = [nb for nb in self.nonbasic if self.A[i, nb.col_idx] < 0]

                    conflict_bounds = []
                    conflict_bounds += [nb.upper_literal for nb in N_minus]
                    conflict_bounds += [nb.lower_literal for nb in N_plus]
                    conflict_bounds.append(xi.upper_literal)

                    conflict = [-conflicting_lit for conflicting_lit in conflict_bounds]
                    return False, conflict
                xj = min(cand, key=lambda v: v.col_idx)
                self._pivot_and_update(i, xi, xj, xi.upper)

    def _pivot_and_update(self, i, xi, xj, v):
        """
        Pivots basic variable xi with nonbasic variable xj,
        and sets value of xi to v and adjusts the values of all basic variables
        to keep equations satisfied.

        i is precomputed in check(), it is solely a parameter just for the small optimization, otherwise the method is exactly like [1] paper.
        """
        j = xj.col_idx
        assert j is not None
        assert self.A[i, j] != 0
        theta = (v - xi.assign)*(1/self.A[i, j])
        xi.assign = v
        xj.assign = xj.assign + theta
        for k in range(len(self.basic)):
            if k != i:
                self.basic[k].assign = self.basic[k].assign + theta*self.A[k, j]
        self._pivot(i, j)
        self.basic[i] = xj
        self.nonbasic.discard(xj)
        self.nonbasic.add(xi)

    def _pivot(self, i, j):
        """
        Performs a pivot operation about entry i, j of A by performing
        a series of row operations on A.

        Conceptually, A represents a system of equations and pivoting
        can be thought of as rearranging equation i to be in terms of
        variable j and then substituting in the rest of the equations
        to get rid of other occurrences of variable j.

        Example
        =======

        >>> from sympy.matrices.dense import Matrix
        >>> from sympy.logic.algorithms.lra_theory import LRASolver
        >>> from sympy import var
        >>> lra = LRASolver.__new__(LRASolver)
        >>> lra.A = Matrix(3, 3, var('a:i'))
        >>> lra.A
        Matrix([
        [a, b, c],
        [d, e, f],
        [g, h, i]])

        This matrix is equivalent to:
        0 = a*x + b*y + c*z
        0 = d*x + e*y + f*z
        0 = g*x + h*y + i*z

        >>> lra._pivot(1, 0)
        >>> lra.A
        Matrix([
        [ 0, -a*e/d + b, -a*f/d + c],
        [-1,       -e/d,       -f/d],
        [ 0,  h - e*g/d,  i - f*g/d]])

        We rearrange equation 1 in terms of variable 0 (x)
        and substitute to remove x from the other equations.

        0 = 0 + (-a*e/d + b)*y + (-a*f/d + c)*z
        0 = -x + (-e/d)*y + (-f/d)*z
        0 = 0 + (h - e*g/d)*y + (i - f*g/d)*z
        """
        Aij = self.A[i, j]
        if Aij == 0:
            raise ZeroDivisionError("Tried to pivot about zero-valued entry.")
        self.A[i, :] = -self.A[i, :]/Aij
        for row in range(self.A.shape[0]):
            if row != i:
                self.A[row, :] = self.A[row, :] + self.A[row, j] * self.A[i, :]

    def backtrack(self):
        """
        Revert the most recent bound update to resolve a conflict.

        Pops the last state from the ``bound_history`` stack and restores the
        variable's previous upper or lower bound. It also reverts all variable
        assignments to their previous valid state using a dictionary,
        thus clearing the current conflict and restoring satisfiability.

        Raises
        ======

        ValueError
            If called when the ``bound_history`` stack is empty, indicating
            the solver's internal state is out of sync.
        """
        if not self.bound_history[-1].updates:
            raise ValueError("Cannot backtrack, bound_history stack is empty")

        self.bound_history[-1].undo()

    def push_level(self):
        """
        Save the state of the LRA solver so that pop_level() can restore it.
        Called when the SAT solver starts a new decision level.
        """
        self.bound_history.append(BoundLevel())

    def pop_level(self):
        """
        Restore the LRA solver to its state at the most recent push_level().
        Called when the SAT solver backtracks a decision level.
        """
        while self.bound_history[-1].updates:
            self.backtrack()
        self.bound_history.pop()

def _sep_const_coeff(expr):
    """
    Example
    =======

    >>> from sympy.logic.algorithms.lra_theory import _sep_const_coeff
    >>> from sympy.abc import x, y
    >>> _sep_const_coeff(2*x)
    (x, 2)
    >>> _sep_const_coeff(2*x + 3*y)
    (2*x + 3*y, 1)
    """
    if isinstance(expr, Add):
        return expr, sympify(1)
    const, var = sift(Mul.make_args(expr),
                      lambda c: len(sympify(c).free_symbols) == 0,
                      binary=True)
    return Mul(*var), Mul(*const)


def _sep_const_terms(expr):
    """
    Example
    =======

    >>> from sympy.logic.algorithms.lra_theory import _sep_const_terms
    >>> from sympy.abc import x, y
    >>> _sep_const_terms(2*x + 3*y + 2)
    (2*x + 3*y, 2)
    """
    const, var = sift(Add.make_args(expr),
                      lambda t: len(t.free_symbols) == 0,
                      binary=True)
    return Add(*var), Add(*const)


def _reduce_matrix(A, basic, nonbasic, nonatom_vars, testing_mode):
    """
    Remove every non-atom variable from the tableu A. This is discussed in
    Preprocessing part of the paper [1]_ as the "Gaussian Eliminaton".

    The idea is that, all non-atom variables are dependent of atom variables,
    which consistent-wise means that solving for atom variables should directly
    give solutions for non-atom variables.

    Therefore, any information about dependent, or to be more precise, non atom variables
    in the matrix A is not necessary and can be safely discarded without any correctness worries.
    E.g in,
        x >= 0 & x+y >= 1 -> Phi' := (x >= 0 & s1 >= 1), Phi_A := x + y = s1
    Since y is dependent, solving Phi' alone is enough, and _reduce_matrix should reduce Phi_A
    into collapsed matrix since it stores no useful information.

    Returns
    =======

    (A, basic, nonbasic)

    A : Matrix
        The reduced tableau with every variable in nonatom_vars removed.
        Has one row per basic and one column per (basic + nonbasic).
        In case of empty basic, the matrix collapses.

    basic : list
        The new list of basic variables. The elements (pivots) are basic if and only if
        the pivots survived elimination. These pivots are new basic becuase they are
        definitions at this point.

    nonbasic : list
        The new list of nonbasic variables. Old basic variables can become nonbasic,
        however nonbasic elements cannot become basic.

    Example
    =======

    Consider the formula:

        x >= 0 & z <= 1 & (x + y <= 5 | z + y >= 2)

    Here y is the only non-atom variable, so only y is removed, s1 = x+y, s2 = z+y.
    >>> from sympy.abc import x, y, z
    >>> from sympy import symbols
    >>> from sympy.solvers.solveset import linear_eq_to_matrix
    >>> from sympy.logic.algorithms.lra_theory import _reduce_matrix
    >>> s1, s2 = symbols('s1 s2')
    >>> nonbasic, basic = [x, y, z], [s1, s2]
    >>> A, _ = linear_eq_to_matrix([x + y - s1, z + y - s2], nonbasic + basic)
    >>> A
    Matrix([
    [1, 1, 0, -1,  0],
    [0, 1, 1,  0, -1]])
    >>> A, basic, nonbasic = _reduce_matrix(A, basic, nonbasic, {y},
    ...                                     testing_mode=True)
    >>> basic, nonbasic
    ([s1], [x, z, s2])

    Notice that s2 became nonbasic.

    >>> A
    Matrix([[1, -1, 1, -1]])

    It is possible for the matrix A to collapse entirely, which happens when
    all the remaining terms are linearly independent. Or in other terms, The matrix A
    is no longer "stores" information about variables as there are no information to store.
    E.g,

         (x >= 0) & ((x + y <= 2) | (x + 2 * y - z >= 6)) & (Eq(x + y, 2) | (x + 2 * y - z > 4))

    only x is the atom variable so only y and z is removed, s1 = x+y and s2 = x+2*y-z.
    >>> nonbasic, basic = [x, y, z], [s1, s2]
    >>> A, _ = linear_eq_to_matrix([x + y - s1, x + 2 * y - z - s2], nonbasic + basic)
    >>> A
    Matrix([
    [1, 1,  0, -1,  0],
    [1, 2, -1,  0, -1]])
    >>> A, basic, nonbasic = _reduce_matrix(A, basic, nonbasic, {y, z},
    ...                                     testing_mode=True)
    >>> basic, nonbasic
    ([], [x, s1, s2])

    Basic is empty, which in result should mean A has collapsed.
    >>> A.shape
    (0, 3)
    """
    if not nonatom_vars:
        return A, basic, nonbasic
    if testing_mode:
        nonatom_vars = sorted(nonatom_vars, key=str)
        # precondition for all tableu matrices A
        m = len(basic)
        n = len(nonbasic+basic)
        assert A[:, n-m:] == -eye(m)

    kept_nonbasic = [v for v in nonbasic if v not in nonatom_vars]
    # The order is important because:
    # 1) rref starts pivoting from left to right, so nonatom_vars should come first
    # 2) basic var should come after them and possibly reduce them too
    # Basic vars are also in the form of block matrix -I_m and the rank of that identity
    # matrix makes so that we never touch kept_nonbasic block matrix
    sorted_col_order = list(nonatom_vars) + basic + kept_nonbasic
    var_to_col_orig = {v: i for i, v in enumerate(nonbasic + basic)}
    # reorder the columns of A by the list sorted_col_order
    A = A[:, [var_to_col_orig[v] for v in sorted_col_order]]

    B, pivots = A.rref()

    keep_rows = [r for r, pc in enumerate(pivots) if pc >= len(nonatom_vars)]
    new_basic = [sorted_col_order[pivots[r]] for r in keep_rows]
    basic_set = set(new_basic)
    new_nonbasic = [v for v in kept_nonbasic + basic if v not in basic_set]

    var_to_col_sorted = {v: i for i, v in enumerate(sorted_col_order)}
    # every basic should have -1 coefficent by convention, and rref gives 1 coeff.
    # to all the basic variables. So we have to negative B.
    A = -B[keep_rows, [var_to_col_sorted[v] for v in new_nonbasic + new_basic]]
    if testing_mode:
        # all the nonaotm_vars should be removed
        assert set(nonatom_vars).isdisjoint(new_basic + new_nonbasic)
        # new basic variables should be a subset of old basic variables
        assert set(new_basic) <= set(basic)
        # new nonbasic variables should be a subset of union of old basic and non-atom nonbasics
        assert set(new_nonbasic) <= set(kept_nonbasic) | set(basic)
        # precondition for all tableu matrices A
        m = len(new_basic)
        n = len(new_nonbasic+new_basic)
        assert A[:, n-m:] == -eye(m)
    return A, new_basic, new_nonbasic


class BoundLevel:
    """
    The bound updates made while one decision level of the SAT solver was
    current, together with enough information to undo them.
    """

    def __init__(self):
        self.updates = []

    def record(self, var, upper):
        """
        Save the bound on the given side of ``var`` before it is replaced.
        The literal goes with it, since `check` builds conflict clauses from it.
        """
        if upper:
            self.updates.append((var, var.upper, var.upper_literal, upper))
        else:
            self.updates.append((var, var.lower, var.lower_literal, upper))

    def undo(self):
        """Restore the most recent bound update."""
        var, bound, literal, upper = self.updates.pop()

        if upper:
            var.upper, var.upper_literal = bound, literal
        else:
            var.lower, var.lower_literal = bound, literal


class Boundary:
    """
    Represents an upper or lower bound between a symbol
    and some constant.

    Example
    =======

    >>> from sympy.logic.algorithms.lra_theory import Boundary, LRAVariable
    >>> from sympy.abc import x
    >>> var = LRAVariable(x)
    >>> # x <= 5
    >>> b1 = Boundary(var, 5, upper=True, strict=False)
    >>> b1.get_inequality()
    x <= 5
    >>> # x > 10 (represented as a lower bound with strict=True)
    >>> b2 = Boundary(var, 10, upper=False, strict=True)
    >>> b2.get_inequality()
    x > 10
    """
    def __init__(self, var, const, upper, strict=None):
        self.var = var
        if isinstance(const, tuple):
            s = const[1] != 0
            if strict is not None:
                assert s == strict
            self.bound = const[0]
            self.strict = s
        else:
            self.bound = const
            self.strict = strict
        self.upper = upper
        assert self.strict is not None

    def to_rational(self, is_negated):
        """
        Return the LRARational bound and effective direction (upper=True)
        considering whether the boundary is negated.
        """
        upper = self.upper != is_negated
        delta = 0
        if self.strict != is_negated:
            delta = -1 if upper else 1
        return LRARational(self.bound, delta), upper

    def get_inequality(self):
        if self.upper and self.strict:
            return self.var.var < self.bound
        elif not self.upper and self.strict:
            return self.var.var > self.bound
        elif self.upper:
            return self.var.var <= self.bound
        else:
            return self.var.var >= self.bound

    def __repr__(self):
        return repr("Boundary(" + repr(self.get_inequality()) + ")")

    def __eq__(self, other):
        if not isinstance(other, Boundary):
            return NotImplemented
        return ((self.var, self.bound, self.strict, self.upper)
            == (other.var, other.bound, other.strict, other.upper))

    def __hash__(self):
        return hash((self.var, self.bound, self.strict, self.upper))


class LRARational():
    """
    Represents a rational plus or minus some amount
    of arbitrary small deltas.
    """
    def __init__(self, rational, delta):
        self.value = (rational, delta)

    @property
    def q(self):
        return self.value[0]

    @property
    def d(self):
        return self.value[1]

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        if not isinstance(other, LRARational):
            return NotImplemented
        return self.value == other.value

    def __add__(self, other):
        return LRARational(self.q + other.q, self.d + other.d)

    def __sub__(self, other):
        return LRARational(self.q - other.q, self.d - other.d)

    def __mul__(self, other):
        assert not isinstance(other, LRARational)
        return LRARational(self.q * other, self.d * other)

    def __getitem__(self, index):
        return self.value[index]

    def __repr__(self):
        return repr(self.value)


class LRAVariable():
    """
    Object to keep track of upper and lower bounds
    on `self.var`.
    """
    def __init__(self, var):
        self.initialize()
        self.var = var
        self.col_idx = None

    def initialize(self):
        self.upper = LRARational(float("inf"), 0)
        self.upper_literal = None
        self.lower = LRARational(-float("inf"), 0)
        self.lower_literal = None
        self.assign = LRARational(0,0)

    def __repr__(self):
        return repr(self.var)

    def set_bound(self, boundary, literal):
        """
        Set the upper or lower bound and record its source.

        Example
        =======

        >>> from sympy.logic.algorithms.lra_theory import LRAVariable, Boundary
        >>> from sympy.abc import x
        >>> v = LRAVariable(x)
        >>> b = Boundary(v, 10, upper=False, strict=False)
        >>> # Asserting a lower bound x >= 10 using literal 5
        >>> v.set_bound(b, 5)
        >>> v.lower
        (10, 0)
        >>> v.lower_literal
        5
        """
        is_negated = literal < 0
        ci, upper = boundary.to_rational(is_negated)
        if upper:
            self.upper = ci
            self.upper_literal = literal
        else:
            self.lower = ci
            self.lower_literal = literal

    def __eq__(self, other):
        if not isinstance(other, LRAVariable):
            return False
        return other.var == self.var

    def __hash__(self):
        return hash(self.var)
