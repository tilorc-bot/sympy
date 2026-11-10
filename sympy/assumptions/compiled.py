"""
Prototype: handlers compiled from the facts in ``class_fact_registry``.

The fact functions are used exactly as they are written. What changes is when
they run. A fact function is called once on a *generic* instance of an
expression shape, e.g. ``Mul(_a, _b)`` with placeholder arguments, and each
fact it returns is compiled into rules

    conditions on the arguments  =>  literal about the expression

which are reused for every expression of that shape (``_compile``,
``template_for``). Answering a query is then a goal directed walk over those
rules with one pair of bitsets per expression (``Engine.ask``), which is what
a hand written handler does.

Shapes are tried at two levels: every scalar argument replaced by a
placeholder, then with the arguments which are numbers kept, so that facts
about ``x**2`` or ``x/2`` in particular are found. ``COMPILED_LEVELS=2`` adds
a third level which compiles the facts of each expression itself.

This is sound because a fact about ``Mul(a, b)`` for symbols ``a`` and ``b``
has to hold whatever values they take, so it holds for whatever expressions
are put in their place. Matrix shapes are compared structurally in SymPy, so
they are never replaced.

Two kinds of fact are not rules but measurements of one particular
expression: its old assumptions and its numerical value. They are read
lazily, one predicate at a time, with the tables and helpers the fact
functions in ``satfacts.common`` and ``satfacts.numbers`` use.

``fastask(proposition, assumptions)`` returns True, False or None; None means
that the facts do not settle the query by propagation and the SAT solver
should be asked.
"""
from sympy.assumptions.ask import Q
from sympy.assumptions.assume import AppliedPredicate
from sympy.assumptions.ask_generated import get_all_known_facts, get_known_facts_dict
from sympy.assumptions.cnf import CNF
from sympy.assumptions.relation.binrel import AppliedBinaryRelation
from sympy.assumptions.sathandlers import class_fact_registry
from sympy.assumptions.satfacts.common import (_old_assumptions,
    _old_assumptions_compound, numeric_predicates, is_numeric)
from sympy.assumptions.satfacts.numbers import _sign, _evaluated, _rounded
from sympy.core import Add, Mul, Pow, Expr, Float, S, Symbol, Dummy
from sympy.core.cache import cacheit
from sympy.core.function import Function
from sympy.core.numbers import NaN
from sympy.logic.boolalg import (And, Boolean, Or, Not, Implies, Equivalent,
    BooleanTrue, BooleanFalse, to_nnf)
from sympy.matrices.expressions import (MatrixExpr, MatrixSymbol, Trace,
    Determinant)
from sympy.matrices.expressions.matexpr import MatrixElement
from sympy.ntheory import isprime


class Inconsistent(Exception):
    pass


### Predicates as bits ###

_BITS = {}


def bit(pred):
    b = _BITS.get(pred)
    if b is None:
        b = _BITS[pred] = 1 << len(_BITS)
    return b


def _bits(mask):
    while mask:
        low = mask & -mask
        yield low
        mask ^= low


### Facts between the predicates of one expression ###

def _implications():
    """
    Everything which follows from one literal: masks of the predicates which
    are true and false when a predicate is true, and of those which are false
    when it is false.
    """
    true, false = {}, {}
    for p, (implied, rejected) in get_known_facts_dict().items():
        T = F = 0
        for q in implied:
            T |= bit(q)
            false[bit(q)] = false.get(bit(q), 0) | bit(p)
        for q in rejected:
            F |= bit(q)
        true[bit(p)] = (T, F)
    return true, false


_IMPLIED = _implications()


class Table:
    """
    Clauses over the predicates of a single expression: the known facts and
    the facts of a shape which only mention the expression itself.
    """
    _interned = {}

    @classmethod
    def get(cls, extra=frozenset()):
        table = cls._interned.get(extra)
        if table is None:
            table = cls._interned[extra] = cls(extra)
        return table

    def __init__(self, extra):
        clauses = set(extra)
        for clause in get_all_known_facts():
            pos = neg = 0
            for lit in clause:
                if lit.is_Not:
                    neg |= bit(lit.arg)
                else:
                    pos |= bit(lit.arg)
            clauses.add((pos, neg))
        self.clauses = tuple(clauses)
        self.watch = {}
        for c in self.clauses:
            for b in _bits(c[0] | c[1]):
                self.watch.setdefault(b, []).append(c)
        self.memo = {}
        self._chains = {}
        self.T, self.F = self.close(0, 0, full=True)

    def close(self, T, F, full=False):
        """Unit propagation. Returns ``None`` if the facts are inconsistent."""
        key = (T, F)
        try:
            return self.memo[key]
        except KeyError:
            pass
        res = self._close(T, F, full)
        if len(self.memo) > 200000:
            self.memo.clear()
        self.memo[key] = res
        return res

    def _close(self, T, F, full):
        pending = list(self.clauses) if full else None
        todo = T | F
        watch = self.watch
        true, false = _IMPLIED
        while True:
            for b in _bits(todo & T):
                if b in true:
                    T |= true[b][0]
                    F |= true[b][1]
            for b in _bits(todo & F):
                F |= false.get(b, 0)
            if T & F:
                return None
            if pending is None:
                pending = []
                for b in _bits(T | F if todo else 0):
                    pending.extend(watch.get(b, ()))
            todo = 0
            for pos, neg in pending:
                if T & pos or F & neg:
                    continue
                up = pos & ~F
                un = neg & ~T
                if not un:
                    if not up:
                        return None
                    if not up & (up - 1):
                        T |= up
                        todo |= up
                elif not up and not un & (un - 1):
                    F |= un
                    todo |= un
            if not todo:
                return T, F
            pending = None

    def decided(self, b, outcomes):
        """Whether each of *outcomes* decides the predicate *b*."""
        for T, F in outcomes:
            r = self.close(self.T | T, self.F | F)
            if r is not None and not (r[0] | r[1]) & b:
                return False
        return True

    def touched(self, b):
        """Predicates decided by knowing the value of predicate *b* alone."""
        res = 0
        for T, F in ((b, 0), (0, b)):
            r = self.close(self.T | T, self.F | F)
            if r is not None:
                res |= r[0] | r[1]
        return res

    def chains(self, b):
        """
        Clauses with three or more literals which can decide *b*: pairs of
        (literals which must all be false, value of *b*).
        """
        res = self._chains.get(b)
        if res is None:
            res = []
            for pos, neg in self.watch.get(b, ()):
                body = [(q, False) for q in _bits(pos & ~b)]
                body += [(q, True) for q in _bits(neg & ~b)]
                if len(body) >= 2:
                    res.append((tuple(body), bool(pos & b)))
            res = self._chains[b] = tuple(res)
        return res


### Shapes ###

SELF, ARG, DERIVED, CONCRETE = range(4)


class Template:
    """Rules compiled from the facts of one shape of expression."""

    def __init__(self, table, rules, specs, placeholders, old=0, atom=False,
                 scalar=False):
        self.table = table
        self.T, self.F = table.T, table.F
        self.rules = rules
        self.specs = specs
        self.placeholders = placeholders
        self.old = old
        self.atom = atom
        self.scalar = scalar


ALL_LITS, ANY_LITS, ALL, ANY, REL = range(5)
NEVER, ALWAYS = object(), object()


def _falsifier(nnf, term):
    """
    The condition under which the formula *nnf*, in negation normal form, is
    false:

    (ALL_LITS, term, T, F): the predicates *T* of the term are true and the
        predicates *F* are false
    (ANY_LITS, term, alternatives): one of the (T, F) alternatives holds
    (ALL, conditions), (ANY, conditions)
    (REL, predicate, terms, value): a polyadic predicate has this value
    """
    if nnf is S.true:
        return NEVER
    if nnf is S.false:
        return ALWAYS
    if isinstance(nnf, Or):
        parts = [_falsifier(c, term) for c in nnf.args]
        if any(p is NEVER for p in parts):
            return NEVER
        return _all([p for p in parts if p is not ALWAYS])
    if isinstance(nnf, And):
        parts = [_falsifier(c, term) for c in nnf.args]
        if any(p is ALWAYS for p in parts):
            return ALWAYS
        return _any([p for p in parts if p is not NEVER])
    negated = isinstance(nnf, Not)
    a = nnf.args[0] if negated else nnf
    if not isinstance(a, AppliedPredicate):
        return NEVER
    args = a.arguments
    if len(args) == 1 and not isinstance(a, AppliedBinaryRelation):
        b = bit(a.function)
        return (ALL_LITS, term(args[0]), b if negated else 0, 0 if negated else b)
    return (REL, a.function, tuple(term(x) for x in args), negated)


def _all(parts):
    if not parts:
        return ALWAYS
    lits = {}
    rest = []
    for p in parts:
        for q in (p[1] if p[0] == ALL else (p,)):
            if q[0] == ALL_LITS:
                T, F = lits.get(q[1], (0, 0))
                lits[q[1]] = (T | q[2], F | q[3])
            else:
                rest.append(q)
    parts = [(ALL_LITS, t, T, F) for t, (T, F) in lits.items()] + rest
    return parts[0] if len(parts) == 1 else (ALL, tuple(parts))


def _any(parts):
    if not parts:
        return NEVER
    lits = {}
    rest = []
    for p in parts:
        for q in (p[1] if p[0] == ANY else (p,)):
            if q[0] == ALL_LITS and not (q[2] | q[3]) & ((q[2] | q[3]) - 1):
                lits.setdefault(q[1], []).append((q[2], q[3]))
            elif q[0] == ANY_LITS:
                lits.setdefault(q[1], []).extend(q[2])
            else:
                rest.append(q)
    parts = rest
    for t, alts in lits.items():
        if len(alts) == 1:
            parts.append((ALL_LITS, t, alts[0][0], alts[0][1]))
        else:
            parts.append((ANY_LITS, t, tuple(sorted(set(alts)))))
    return parts[0] if len(parts) == 1 else (ANY, tuple(parts))


def _compile(generic, gargs, old, scalar, facts=None):
    """
    Compile the facts of *generic*, whose arguments *gargs* are placeholders
    (or ``None`` where the argument was kept), into a ``Template``.

    A fact which mentions a literal ``c`` about *generic* is read as two
    rules: if the fact with ``c`` replaced by false is false then ``c`` is
    true, and if the fact with ``c`` replaced by true is false then ``c`` is
    false.
    """
    if facts is None:
        facts = class_fact_registry(generic)

    index = {generic: 0}
    specs = [(SELF, None)]
    positions = {g: i for i, g in enumerate(gargs) if g is not None}

    def term(e):
        t = index.get(e)
        if t is None:
            t = index[e] = len(specs)
            if e in positions:
                specs.append((ARG, positions[e]))
            elif positions and e.has(*positions):
                specs.append((DERIVED, e))
            else:
                specs.append((CONCRETE, e))
        return t

    def late(c):
        if c[0] in (ALL_LITS, ANY_LITS):
            return (specs[c[1]][0] in (DERIVED, CONCRETE), c[0], c[1])
        return (True, c[0], 0)

    extra = set()
    raw = []
    for fact in facts:
        if not isinstance(fact, Boolean):
            continue
        atoms = fact.atoms(AppliedPredicate)
        selfs = [a for a in atoms if len(a.arguments) == 1 and a.arguments[0] == generic
                 and not isinstance(a, AppliedBinaryRelation)]
        if not selfs:
            continue
        if len(selfs) == len(atoms):
            for clause in CNF.to_CNF(fact).clauses:
                pos = neg = 0
                for lit in clause:
                    if lit.is_Not:
                        neg |= bit(lit.arg.function)
                    else:
                        pos |= bit(lit.arg.function)
                extra.add((pos, neg))
            continue
        for c in selfs:
            b = bit(c.function)
            for value in (S.false, S.true):
                cond = _falsifier(to_nnf(fact.xreplace({c: value}), simplify=False), term)
                if cond is NEVER:
                    continue
                if cond is ALWAYS:
                    extra.add((0, b) if value is S.true else (b, 0))
                    continue
                conds = cond[1] if cond[0] == ALL else (cond,)
                raw.append((tuple(sorted(conds, key=late)), b, value is S.true))

    table = Table.get(frozenset(extra))
    rules = {}
    for conds, b, is_not in raw:
        closed = table.close(table.T | (0 if is_not else b), table.F | (b if is_not else 0))
        if closed is None:
            continue
        cT, cF = closed
        rule = (conds, cT, cF)
        for q in _bits((cT | cF) & ~(table.T | table.F)):
            rules.setdefault(q, []).append(((q != b, len(conds)), id(rule), rule))
    rules = {q: tuple(r for _, _, r in sorted(rs, key=lambda x: x[:2]))
             for q, rs in rules.items()}
    return Template(table, rules, tuple(specs), tuple(gargs), old=old, scalar=scalar)


_counter = [0]


def _matrix_placeholder(shape):
    _counter[0] += 1
    return MatrixSymbol('_M%d\x00' % _counter[0], *shape)


ATOM, SCALAR, MATRIX, OPAQUE = range(4)
_KIND = {}
_TEMPLATES = {}
STATS = {'compiled': 0, 'instance': 0, 'sign': 0, 'round': 0}


def _classify(cls):
    if issubclass(cls, MatrixExpr) or issubclass(cls, (Trace, Determinant, MatrixElement)):
        return MATRIX
    if issubclass(cls, Expr):
        if cls.is_Atom:
            return ATOM
        if issubclass(cls, (Add, Mul, Pow, Function)):
            return SCALAR
    return OPAQUE


def _old_kind(cls):
    """0: no old assumptions, 1: those of compound expressions."""
    if issubclass(cls, Expr) and not issubclass(cls, (MatrixExpr, NaN, Add, Mul, Pow)):
        return 1
    return 0


def template_for(e, level):
    """
    The template of *e*. *level* 0 replaces every scalar argument with a
    placeholder, *level* 1 keeps the arguments which are numbers and
    *level* 2 uses the facts of *e* itself.
    """
    cls = type(e)
    kind = _KIND.get(cls)
    if kind is None:
        kind = _KIND[cls] = _classify(cls)
    if kind == ATOM:
        return _NAN if cls is NaN else _ATOM
    if kind == OPAQUE or level == 2:
        return _instance_template(e)
    keep = level == 1 or kind == MATRIX
    key = [cls]
    for a in e.args:
        if isinstance(a, MatrixExpr):
            key.append(a.shape)
        elif isinstance(a, Expr):
            if keep and a.is_number:
                key.append(('k', a))
            else:
                c = a.is_commutative
                if c is None:
                    return _instance_template(e)
                key.append(c)
        elif not a.free_symbols:
            key.append(('k', a))
        else:
            return _instance_template(e)
    key = tuple(key)
    try:
        t = _TEMPLATES[key]
    except KeyError:
        t = _TEMPLATES[key] = _generic_template(e, key, kind)
    if t is None:
        return _instance_template(e)
    return t


def _generic_template(e, key, kind):
    gargs = []
    cargs = []
    for a, k in zip(e.args, key[1:]):
        if k is True or k is False:
            g = Dummy(commutative=k)
        elif k[0] == 'k':
            gargs.append(None)
            cargs.append(a)
            continue
        else:
            g = _matrix_placeholder(k)
        gargs.append(g)
        cargs.append(g)
    if not any(g is not None for g in gargs):
        return None
    try:
        generic = e.func(*cargs)
    except Exception:
        return None
    if type(generic) is not type(e) or set(generic.args) != set(cargs) \
            or len(generic.args) != len(cargs):
        return None
    if kind == MATRIX and getattr(generic, 'shape', None) != getattr(e, 'shape', None):
        return None
    STATS['compiled'] += 1
    return _compile(generic, gargs, _old_kind(type(e)),
                    isinstance(e, Expr) and not isinstance(e, MatrixExpr))


@cacheit
def _instance_template(e):
    STATS['instance'] += 1
    scalar = isinstance(e, Expr) and not isinstance(e, MatrixExpr)
    return _compile(e, (), _old_kind(type(e)), scalar, registered_facts(e))


@cacheit
def registered_facts(e):
    return tuple(class_fact_registry(e))


_ATOM = Template(_compile(Dummy(), (), 0, True).table, {}, (), (), old=2,
                 atom=True, scalar=True)
_NAN = Template(Table.get(), {}, (), (), atom=True)


### Measurements ###

_BASE = Table.get()
B = {p: bit(p) for p in list(_old_assumptions) + list(numeric_predicates)}
B_COMM = bit(Q.commutative)
_OLD_ALL = tuple((bit(p), attr) for p, attr in _old_assumptions.items())
_OLD_NONNUM = tuple((bit(p), attr) for p, attr in _old_assumptions.items()
                    if p not in numeric_predicates)
_OLD_COMPOUND = tuple((bit(p), attr) for p, attr in _old_assumptions.items()
                      if p in _old_assumptions_compound)
_NUMERIC_BITS = 0
for _p in numeric_predicates:
    _NUMERIC_BITS |= bit(_p)

# The numerical value decides these predicates whatever it turns out to be,
# so it is looked at first, and the others only when the rules do not answer.
_SIGN_OUTCOMES = [(B[Q.positive], 0), (B[Q.negative], 0), (B[Q.zero], 0), (0, B[Q.real])]
_INT_OUTCOMES = [(0, B[Q.integer])] + [
    (B[Q.integer] | B[parity] | prime[0], prime[1])
    for parity in (Q.even, Q.odd) for prime in ((B[Q.prime], 0), (0, B[Q.prime]))]
_SIGN_EXACT = _INT_EXACT = _SIGN_TRIGGER = _INT_TRIGGER = 0
for _b in list(_BITS.values()):
    if _BASE.decided(_b, _SIGN_OUTCOMES):
        _SIGN_EXACT |= _b
    if _BASE.decided(_b, _INT_OUTCOMES):
        _INT_EXACT |= _b
for _p in (Q.positive, Q.negative, Q.zero, Q.real, Q.imaginary):
    _SIGN_TRIGGER |= _BASE.touched(bit(_p))
for _p in (Q.integer, Q.even, Q.odd, Q.prime):
    _INT_TRIGGER |= _BASE.touched(bit(_p))
_OLD_TRIGGER = {}


def _old_relevant(b):
    res = _OLD_TRIGGER.get(b)
    if res is None:
        res = _OLD_TRIGGER[b] = tuple((q, attr) for q, attr in _OLD_COMPOUND
                                      if q == b or _BASE.touched(q) & b)
    return res


### Evaluation ###

class Node:
    __slots__ = ('e', 'T', 'F', 'tried', 'tmpl', 'terms', 'numeric', 'ran', 'sub')


class Engine:
    def __init__(self, assumptions, level=0):
        self.level = level
        self.assumptions = assumptions
        self.nodes = {}
        self.seeds = {}
        self.lits = {}
        self.roots = set()
        self.constants = False
        for clause in CNF.from_prop(assumptions).clauses:
            if len(clause) != 1:
                continue
            (lit,) = clause
            a = lit.arg
            if isinstance(a, AppliedPredicate) and len(a.arguments) == 1 \
                    and not isinstance(a, AppliedBinaryRelation):
                seed = self.seeds.setdefault(a.arguments[0], [0, 0])
                seed[lit.is_Not] |= bit(a.function)
            else:
                self.lits[a] = not lit.is_Not

    def node(self, e):
        n = Node()
        n.e = e
        n.tried = 0
        n.terms = None
        n.sub = None
        n.ran = 0
        tmpl = n.tmpl = template_for(e, self.level)
        T, F = tmpl.T, tmpl.F
        seed = self.seeds.get(e)
        if seed is not None:
            T |= seed[0]
            F |= seed[1]
        n.numeric = None
        if tmpl.atom:
            n.numeric = False
            if tmpl.old:
                n.numeric = is_numeric(e)
                for b, attr in (_OLD_NONNUM if n.numeric else _OLD_ALL):
                    v = getattr(e, attr)
                    if v is True:
                        T |= b
                    elif v is False:
                        F |= b
            if not (T | F) & B_COMM:
                c = e.is_commutative if isinstance(e, Symbol) else True
                if c is True:
                    T |= B_COMM
                elif c is False:
                    F |= B_COMM
            elif not isinstance(e, Symbol):
                T |= B_COMM
            elif e.is_commutative is False:
                F |= B_COMM
        elif not tmpl.scalar:
            n.numeric = False
        if T != tmpl.T or F != tmpl.F:
            closed = tmpl.table.close(T, F)
            if closed is None:
                raise Inconsistent
            T, F = closed
        n.T = T
        n.F = F
        self.nodes[e] = n
        if not self.constants and not tmpl.atom and self.level == 0:
            self.constants = any(getattr(a, 'is_number', False) for a in e.args)
        return n

    def add(self, n, T, F):
        T |= n.T
        F |= n.F
        if T != n.T or F != n.F:
            closed = n.tmpl.table.close(T, F)
            if closed is None:
                raise Inconsistent
            n.T, n.F = closed

    def term(self, n, t):
        terms = n.terms
        if terms is None:
            terms = n.terms = [None]*len(n.tmpl.specs)
        e = terms[t]
        if e is None:
            kind, x = n.tmpl.specs[t]
            if kind == ARG:
                e = n.e.args[x]
            elif kind == CONCRETE:
                e = x
            elif kind == SELF:
                e = n.e
            else:
                if n.sub is None:
                    n.sub = {g: a for g, a in zip(n.tmpl.placeholders, n.e.args)
                             if g is not None}
                e = x.xreplace(n.sub)
            terms[t] = e
        return e

    def all_of(self, te, m, T, F):
        """Whether the predicates in *T* are true and those in *F* false."""
        if m.F & T or m.T & F:
            return False
        for q in _bits(T & ~m.T):
            if self.ask(te, q) is not True:
                return False
        for q in _bits(F & ~m.F):
            if self.ask(te, q) is not False:
                return False
        return True

    def any_of(self, te, m, alts):
        """Whether one of the alternatives holds, or cannot all fail."""
        for T, F in alts:
            if m.T & T == T and m.F & F == F:
                return True
        for T, F in alts:
            if self.all_of(te, m, T, F):
                return True
        nT = nF = 0
        for T, F in alts:
            if m.F & T or m.T & F:
                continue
            if not F and not T & (T - 1):
                nF |= T
            elif not T and not F & (F - 1):
                nT |= F
            else:
                return False
        return m.tmpl.table.close(m.T | nT, m.F | nF) is None

    def holds(self, n, c):
        kind = c[0]
        if kind == ALL_LITS or kind == ANY_LITS:
            te = self.term(n, c[1])
            m = self.nodes.get(te)
            if m is None:
                m = self.node(te)
            if kind == ALL_LITS:
                return self.all_of(te, m, c[2], c[3])
            return self.any_of(te, m, c[2])
        if kind == ALL:
            for x in c[1]:
                if not self.holds(n, x):
                    return False
            return True
        if kind == ANY:
            for x in c[1]:
                if self.holds(n, x):
                    return True
            return False
        return self.relation(c[1], [self.term(n, t) for t in c[2]]) is c[3]

    def ask(self, e, b):
        n = self.nodes.get(e)
        if n is None:
            n = self.node(e)
        if n.T & b:
            return True
        if n.F & b:
            return False
        if n.tried & b:
            return None
        n.tried |= b
        tmpl = n.tmpl

        if n.numeric is not False:
            if n.numeric is None:
                n.numeric = is_numeric(e)
            if n.numeric and b & _SIGN_EXACT:
                self.measure(n, True, False)
                if n.T & b:
                    return True
                if n.F & b:
                    return False

        rules = tmpl.rules.get(b)
        if rules:
            nodes = self.nodes
            for conds, cT, cF in rules:
                for c in conds:
                    if c[0] == ALL_LITS:
                        t = c[1]
                        if t:
                            te = n.terms[t] if n.terms is not None else None
                            if te is None:
                                te = self.term(n, t)
                            m = nodes.get(te)
                            if m is None:
                                m = self.node(te)
                        else:
                            te = e
                            m = n
                        T = c[2]
                        F = c[3]
                        if m.T & T != T or m.F & F != F:
                            if not self.all_of(te, m, T, F):
                                break
                    elif not self.holds(n, c):
                        break
                else:
                    self.add(n, cT, cF)
                    if n.T & b:
                        return True
                    if n.F & b:
                        return False

        if tmpl.old == 1:
            numeric = n.numeric
            T = F = 0
            for q, attr in _old_relevant(b):
                if numeric and q & _NUMERIC_BITS:
                    continue
                v = getattr(e, attr)
                if v is True:
                    T |= q
                elif v is False:
                    F |= q
            if T or F:
                self.add(n, T, F)
                if n.T & b:
                    return True
                if n.F & b:
                    return False

        table = tmpl.table
        if e in self.roots:
            for body, value in table.chains(b):
                for q, want in body:
                    if self.ask(e, q) is not want:
                        break
                else:
                    self.add(n, b if value else 0, 0 if value else b)
                    return value
            if n.T & b:
                return True
            if n.F & b:
                return False

        if n.numeric and b & (_SIGN_TRIGGER | _INT_TRIGGER):
            self.measure(n, b & _SIGN_TRIGGER, b & _INT_EXACT or e in self.roots and b & _INT_TRIGGER)
            if n.T & b:
                return True
            if n.F & b:
                return False

        # The literal is implied if its negation is refuted by propagation.
        if table.close(n.T | b, n.F) is None:
            self.add(n, 0, b)
            return False
        if table.close(n.T, n.F | b) is None:
            self.add(n, b, 0)
            return True
        return None

    def measure(self, n, sign, integer):
        e = n.e
        T = F = 0
        imaginary_or_zero = False
        if sign and not n.ran & 1:
            n.ran |= 1
            STATS['sign'] += 1
            sign = _sign(e)
            if sign == 'nonreal':
                F |= B[Q.real]
            elif sign is not None:
                T |= B[getattr(Q, sign)]
            real, imag = (_evaluated(p) for p in e.as_real_imag())
            if imag is not None:
                if imag:
                    F |= B[Q.real]
                else:
                    T |= B[Q.real]
            if real is not None:
                if real:
                    F |= B[Q.imaginary]
                else:
                    imaginary_or_zero = True
        if integer and not n.ran & 2:
            n.ran |= 2
            STATS['round'] += 1
            i = _rounded(e)
            if i is False:
                F |= B[Q.integer]
            elif i is not None and not e.atoms(Float):
                T |= B[Q.integer] | B[Q.even if i % 2 == 0 else Q.odd]
                if isprime(i):
                    T |= B[Q.prime]
                else:
                    F |= B[Q.prime]
        self.add(n, T, F)
        if imaginary_or_zero and n.F & B[Q.zero]:
            self.add(n, B[Q.imaginary], 0)

    def relation(self, pred, args):
        prop = pred(*args)
        v = self.lits.get(prop)
        if v is None and all(a.is_number for a in args):
            v = pred.eval(tuple(args))
        return v

    def eval(self, prop):
        if isinstance(prop, AppliedPredicate):
            args = prop.arguments
            if isinstance(prop, AppliedBinaryRelation):
                v = self.lits.get(prop)
                if v is None:
                    v = prop._eval_ask(self.assumptions)
                return v
            if len(args) != 1:
                return self.lits.get(prop)
            if prop.function == Q.is_true:
                if args[0].is_Symbol:
                    return self.lits.get(prop)
                return self.eval(args[0])
            self.roots.add(args[0])
            return self.ask(args[0], bit(prop.function))
        if isinstance(prop, BooleanTrue):
            return True
        if isinstance(prop, BooleanFalse):
            return False
        if isinstance(prop, Not):
            if prop.args[0].is_Symbol:
                return None
            v = self.eval(prop.args[0])
            return None if v is None else not v
        if isinstance(prop, Or):
            result = False
            for arg in prop.args:
                v = self.eval(arg)
                if v is True:
                    return True
                if v is None:
                    result = None
            return result
        if isinstance(prop, And):
            result = True
            for arg in prop.args:
                v = self.eval(arg)
                if v is False:
                    return False
                if v is None:
                    result = None
            return result
        if isinstance(prop, Implies):
            p, q = prop.args
            return self.eval(Or(Not(p), q))
        if isinstance(prop, Equivalent) and len(prop.args) == 2:
            p, q = (self.eval(a) for a in prop.args)
            if p is None or q is None:
                return None
            return p == q
        return None


LEVELS = {0: 0, 1: 0, 2: 0, None: 0}
MAX_LEVEL = int(__import__('os').environ.get('COMPILED_LEVELS', '1'))


def fastask(proposition, assumptions=True):
    """
    Answer *proposition* from the compiled facts. ``None`` means that the
    facts do not settle it by propagation alone.
    """
    try:
        engine = Engine(assumptions)
        res = engine.eval(proposition)
        if res is not None:
            LEVELS[0] += 1
            return res
        if engine.constants:
            res = Engine(assumptions, level=1).eval(proposition)
            if res is not None:
                LEVELS[1] += 1
                return res
        if MAX_LEVEL >= 2:
            res = Engine(assumptions, level=2).eval(proposition)
            if res is not None:
                LEVELS[2] += 1
                return res
    except Inconsistent:
        pass
    LEVELS[None] += 1
    return None


genask = fastask
