"""
The classes used here are for the internal use of assumptions system
only and should not be used anywhere else as these do not possess the
signatures common to SymPy objects. For general use of logic constructs
please refer to sympy.logic classes And, Or, Not, etc.
"""
from __future__ import annotations
from itertools import combinations, zip_longest
from sympy.assumptions.assume import AppliedPredicate, Predicate
from sympy.core.relational import Eq, Ne, Gt, Lt, Ge, Le
from sympy.core.singleton import S
from sympy.logic.boolalg import Or, And, Not, Xnor
from sympy.logic.boolalg import (Equivalent, ITE, Implies, Nand, Nor, Xor)


class Literal:
    """
    The smallest element of a CNF object.

    Parameters
    ==========

    lit : Boolean expression

    is_Not : bool

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.assumptions.cnf import Literal
    >>> from sympy.abc import x
    >>> Literal(Q.even(x))
    Literal(Q.even(x), False)
    >>> Literal(~Q.even(x))
    Literal(Q.even(x), True)
    """

    def __new__(cls, lit, is_Not=False):
        if isinstance(lit, Not):
            lit = lit.args[0]
            is_Not = True
        elif isinstance(lit, (AND, OR, Literal)):
            return ~lit if is_Not else lit
        obj = super().__new__(cls)
        obj.lit = lit
        obj.is_Not = is_Not
        return obj

    @property
    def arg(self):
        return self.lit

    def __invert__(self):
        is_Not = not self.is_Not
        return Literal(self.lit, is_Not)

    def __str__(self):
        return '{}({}, {})'.format(type(self).__name__, self.lit, self.is_Not)

    __repr__ = __str__

    def __eq__(self, other):
        return self.arg == other.arg and self.is_Not == other.is_Not

    def __hash__(self):
        h = hash((type(self).__name__, self.arg, self.is_Not))
        return h


class OR:
    """
    A low-level implementation for Or
    """
    def __init__(self, *args):
        self._args = args

    @property
    def args(self):
        return sorted(self._args, key=str)

    def __invert__(self):
        return AND(*[~arg for arg in self._args])

    def __hash__(self):
        return hash((type(self).__name__,) + tuple(self.args))

    def __eq__(self, other):
        return self.args == other.args

    def __str__(self):
        s = '(' + ' | '.join([str(arg) for arg in self.args]) + ')'
        return s

    __repr__ = __str__


class AND:
    """
    A low-level implementation for And
    """
    def __init__(self, *args):
        self._args = args

    def __invert__(self):
        return OR(*[~arg for arg in self._args])

    @property
    def args(self):
        return sorted(self._args, key=str)

    def __hash__(self):
        return hash((type(self).__name__,) + tuple(self.args))

    def __eq__(self, other):
        return self.args == other.args

    def __str__(self):
        s = '('+' & '.join([str(arg) for arg in self.args])+')'
        return s

    __repr__ = __str__


def to_NNF(expr, composite_map=None):
    """
    Generates the Negation Normal Form of any boolean expression in terms
    of AND, OR, and Literal objects.

    Examples
    ========

    >>> from sympy import Q, Eq
    >>> from sympy.assumptions.cnf import to_NNF
    >>> from sympy.abc import x, y
    >>> expr = Q.even(x) & ~Q.positive(x)
    >>> to_NNF(expr)
    (Literal(Q.even(x), False) & Literal(Q.positive(x), True))

    Supported boolean objects are converted to corresponding predicates.

    >>> to_NNF(Eq(x, y))
    Literal(Q.eq(x, y), False)

    If ``composite_map`` argument is given, ``to_NNF`` decomposes the
    specified predicate into a combination of primitive predicates.

    >>> cmap = {Q.nonpositive: Q.negative | Q.zero}
    >>> to_NNF(Q.nonpositive, cmap)
    (Literal(Q.negative, False) | Literal(Q.zero, False))
    >>> to_NNF(Q.nonpositive(x), cmap)
    (Literal(Q.negative(x), False) | Literal(Q.zero(x), False))
    """
    from sympy.assumptions.ask import Q

    if composite_map is None:
        composite_map = {}


    binrelpreds = {Eq: Q.eq, Ne: Q.ne, Gt: Q.gt, Lt: Q.lt, Ge: Q.ge, Le: Q.le}
    if type(expr) in binrelpreds:
        pred = binrelpreds[type(expr)]
        expr = pred(*expr.args)

    if isinstance(expr, Not):
        arg = expr.args[0]
        tmp = to_NNF(arg, composite_map)  # Strategy: negate the NNF of expr
        return ~tmp

    if isinstance(expr, Or):
        return OR(*[to_NNF(x, composite_map) for x in Or.make_args(expr)])

    if isinstance(expr, And):
        return AND(*[to_NNF(x, composite_map) for x in And.make_args(expr)])

    if isinstance(expr, Nand):
        tmp = AND(*[to_NNF(x, composite_map) for x in expr.args])
        return ~tmp

    if isinstance(expr, Nor):
        tmp = OR(*[to_NNF(x, composite_map) for x in expr.args])
        return ~tmp

    if isinstance(expr, Xor):
        cnfs = []
        for i in range(0, len(expr.args) + 1, 2):
            for neg in combinations(expr.args, i):
                clause = [~to_NNF(s, composite_map) if s in neg else to_NNF(s, composite_map)
                          for s in expr.args]
                cnfs.append(OR(*clause))
        return AND(*cnfs)

    if isinstance(expr, Xnor):
        cnfs = []
        for i in range(0, len(expr.args) + 1, 2):
            for neg in combinations(expr.args, i):
                clause = [~to_NNF(s, composite_map) if s in neg else to_NNF(s, composite_map)
                          for s in expr.args]
                cnfs.append(OR(*clause))
        return ~AND(*cnfs)

    if isinstance(expr, Implies):
        L, R = to_NNF(expr.args[0], composite_map), to_NNF(expr.args[1], composite_map)
        return OR(~L, R)

    if isinstance(expr, Equivalent):
        cnfs = []
        for a, b in zip_longest(expr.args, expr.args[1:], fillvalue=expr.args[0]):
            a = to_NNF(a, composite_map)
            b = to_NNF(b, composite_map)
            cnfs.append(OR(~a, b))
        return AND(*cnfs)

    if isinstance(expr, ITE):
        L = to_NNF(expr.args[0], composite_map)
        M = to_NNF(expr.args[1], composite_map)
        R = to_NNF(expr.args[2], composite_map)
        return AND(OR(~L, M), OR(L, R))

    if isinstance(expr, AppliedPredicate):
        pred, args = expr.function, expr.arguments
        newpred = composite_map.get(pred, None)
        if newpred is not None:
            return to_NNF(newpred.rcall(*args), composite_map)

    if isinstance(expr, Predicate):
        newpred = composite_map.get(expr, None)
        if newpred is not None:
            return to_NNF(newpred, composite_map)

    return Literal(expr)


def distribute_AND_over_OR(expr):
    """
    Distributes AND over OR in the NNF expression.
    Returns the result (Conjunctive Normal Form of expression)
    as a set of clauses, each of which is a frozenset of
    :class:`Literal` objects.
    """
    if not isinstance(expr, (AND, OR)):
        return {frozenset((expr,))}

    if isinstance(expr, OR):
        clause_sets = [distribute_AND_over_OR(arg) for arg in expr._args]
        result = clause_sets[0]
        for other in clause_sets[1:]:
            result = {clause1 | clause2
                      for clause1 in result for clause2 in other}
        return result

    if isinstance(expr, AND):
        return {clause
                for clause_set in map(distribute_AND_over_OR, expr._args)
                for clause in clause_set}


def clauses_from_prop(prop):
    """
    Converts a Boolean expression to a set of clauses in conjunctive
    normal form. Each clause is a frozenset of :class:`Literal` objects.

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.assumptions.cnf import clauses_from_prop
    >>> from sympy.abc import x
    >>> sorted(map(str, clauses_from_prop(Q.real(x) & ~Q.zero(x))))
    ['frozenset({Literal(Q.real(x), False)})', \
'frozenset({Literal(Q.zero(x), True)})']
    """
    return distribute_AND_over_OR(to_NNF(prop))


def cnf_to_expr(clauses):
    """
    Converts a set of clauses of :class:`Literal` objects to SymPy's
    boolean expression, retaining the form of the expression.
    """
    def remove_literal(arg):
        return Not(arg.lit) if arg.is_Not else arg.lit

    return And(*(Or(*(remove_literal(arg) for arg in clause)) for clause in clauses))


class CNF:
    """
    Class to represent CNF of a Boolean expression.
    Consists of set of clauses, which themselves are stored as
    frozenset of Literal objects.

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.assumptions.cnf import CNF
    >>> from sympy.abc import x
    >>> cnf = CNF.from_prop(Q.real(x) & ~Q.zero(x))
    >>> cnf.clauses
    {frozenset({Literal(Q.real(x), False)}), frozenset({Literal(Q.zero(x), True)})}
    """
    def __init__(self, clauses=None):
        if not clauses:
            clauses = set()
        self.clauses = clauses

    def add(self, prop):
        clauses = clauses_from_prop(prop)
        self.add_clauses(clauses)

    def __str__(self):
        s = ' & '.join(
            ['(' + ' | '.join([str(lit) for lit in clause]) +')'
            for clause in self.clauses]
        )
        return s

    def copy(self):
        return CNF(set(self.clauses))

    def add_clauses(self, clauses):
        self.clauses |= clauses

    @classmethod
    def from_prop(cls, prop):
        res = cls()
        res.add(prop)
        return res

    def all_predicates(self):
        return {arg.lit for clause in self.clauses for arg in clause}

    def _and(self, cnf):
        clauses = self.clauses.union(cnf.clauses)
        return CNF(clauses)

    @classmethod
    def to_CNF(cls, expr):
        return CNF(clauses_from_prop(expr))


class EncodedCNF:
    """
    Class for encoding the CNF expression.
    """
    def __init__(self, data=None, encoding=None):
        if not data and not encoding:
            data = []
            encoding = {}
        self.data = data
        self.encoding = encoding
        self._symbols = list(encoding.keys())

    @classmethod
    def from_clauses(cls, clauses):
        """
        Constructs an ``EncodedCNF`` from a set of clauses of
        :class:`Literal` objects.

        Each distinct literal atom is assigned a fresh positive integer,
        negated for negated literals. Literals which are ``S.false`` are
        encoded as ``0``, which marks the whole ``EncodedCNF`` as trivially
        unsatisfiable.
        """
        enc = cls()
        enc._symbols = list({arg.lit for clause in clauses for arg in clause})
        n = len(enc._symbols)
        enc.encoding = dict(zip(enc._symbols, range(1, n + 1)))
        enc.data = [enc.encode(clause) for clause in clauses]
        return enc

    def from_cnf(self, cnf):
        enc = EncodedCNF.from_clauses(cnf.clauses)
        self.data = enc.data
        self.encoding = enc.encoding
        self._symbols = enc._symbols

    @property
    def symbols(self):
        return self._symbols

    @property
    def variables(self):
        return range(1, len(self._symbols) + 1)

    def copy(self):
        new_data = [set(clause) for clause in self.data]
        return EncodedCNF(new_data, dict(self.encoding))

    def add_prop(self, prop):
        self.add_clauses(clauses_from_prop(prop))

    def add_from_cnf(self, cnf):
        self.add_clauses(cnf.clauses)

    def add_clauses(self, clauses):
        self.data += [self.encode(clause) for clause in clauses]

    def encode_arg(self, arg):
        literal = arg.lit
        value = self.encoding.get(literal, None)
        if value is None:
            n = len(self._symbols)
            self._symbols.append(literal)
            value = self.encoding[literal] = n + 1
        if arg.is_Not:
            return -value
        else:
            return value

    def encode(self, clause):
        return {self.encode_arg(arg) if not arg.lit == S.false else 0 for arg in clause}
