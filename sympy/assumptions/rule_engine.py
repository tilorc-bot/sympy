"""
The rules which are compiled from ``sympy/assumptions/rules``, and how a
query is answered with them.

A rule is written about a generic expression ``f(x)`` or ``f(x, y)``. In
its compiled form it refers to the expressions it is about by *slots*:
slot ``i`` is the ``i``-th of the :func:`rule_arguments` of an expression,
and slot ``-1`` is the expression itself. A condition between two arguments,
``(Q.eq, (a, b), value)``, ``(Q.gt, (a, b), value)`` or ``(Q.ge, (a, b),
value)``, has a pair of slots in place of one, and one of them can be a
number. It is decided as :class:`Comparisons` says.

There are two compiled forms. :func:`sat_rules` gives the rules as clauses
for :func:`~sympy.assumptions.satask.satask`. :func:`ask_rules` gives them
as ways to find the truth value of a predicate for an expression from what
is known about its arguments, which is what :func:`evaluate` does.
"""
from __future__ import annotations

import threading
from operator import ge, gt

from sympy.assumptions.ask import Q
from sympy.assumptions.ask_generated import get_known_facts_dict
from sympy.assumptions.ask_rules_generated import ASK_RULES
from sympy.assumptions.assume import AppliedPredicate
from sympy.assumptions.cnf import CNF
from sympy.assumptions.sat_rules_generated import SAT_RULES
from sympy.core.add import Add
from sympy.core.basic import Basic
from sympy.core.containers import Tuple
from sympy.core.expr import Expr
from sympy.core.mul import Mul
from sympy.core.numbers import I, Rational
from sympy.core.operations import AssocOp
from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.logic.boolalg import And, Not
from sympy.matrices.expressions.blockmatrix import BlockDiagMatrix

FIRST_AND_REST = (Add, Mul, BlockDiagMatrix)

# The predicates which :func:`evaluate` uses the compiled rules for. The
# others have hand-written handlers for the classes of the rules.
RULE_PREDICATES: frozenset = frozenset()

_sat_rules: dict = {}
_ask_rules: dict = {}
_known_classes: dict = {}
_deciding: dict = {}
_handled: dict = {}
_symbols_unknown: dict = {}
_local = threading.local()


def equal(a, b):
    """
    Whether *a* and *b* are equal, as far as it is seen from their form, or
    ``None``.

    Explanation
    ===========

    They are equal if they are the same expression, other than ``nan``, and
    not equal if they are different explicit numbers (rational numbers,
    ``I`` and ``-I``) or tuples of rational numbers, such as the ranges of a
    matrix slice, or numbers of which :func:`greater` finds one greater than
    the other. No expression is built.

    Examples
    ========

    >>> from sympy import I, S, Tuple, pi
    >>> from sympy.abc import i, j
    >>> from sympy.assumptions.rule_engine import equal
    >>> equal(i, i), equal(S(1), S(2)), equal(Tuple(0, 2, 1), Tuple(0, 3, 1))
    (True, False, False)
    >>> equal(I, S(1)), equal(I, -I), equal(pi, S(1))
    (False, False, False)
    >>> print(equal(i, j), equal(i, S(1)))
    None None

    """
    a_number = isinstance(a, Rational)
    if a_number or isinstance(b, Rational):
        if a_number and isinstance(b, Rational):
            return a.p == b.p and a.q == b.q
        if (b if a_number else a) in _UNITS:
            return False
    elif a == b:
        return None if a is S.NaN else True
    elif _explicit(a) and _explicit(b):
        return False
    if (getattr(a, 'is_number', False) and getattr(b, 'is_number', False)
            and (_compared(a, b, gt) or _compared(b, a, gt))):
        return False
    return None


def _explicit(a):
    return a in _UNITS or (
        isinstance(a, Tuple) and all(isinstance(e, Rational) for e in a.args))


_UNITS = frozenset({I, -I})


def greater(a, b):
    """
    Whether *a* and *b* are extended real numbers and ``a > b``, as far as
    it is seen from their form, or ``None``.

    Explanation
    ===========

    Two rational numbers are compared. Two other numbers are compared if
    both are extended real, and are not ordered if one of them is not
    extended real. No expression is built.

    Examples
    ========

    >>> from sympy import I, S, oo, pi
    >>> from sympy.abc import x
    >>> from sympy.assumptions.rule_engine import greater
    >>> greater(S(2), S(1)), greater(pi, S(1)), greater(oo, S(1)), greater(I, S(1))
    (True, True, True, False)
    >>> print(greater(x, S(1)))
    None

    """
    if isinstance(a, Rational) and isinstance(b, Rational):
        return a.p*b.q > b.p*a.q
    return _compared(a, b, gt)


def not_less(a, b):
    """
    Whether *a* and *b* are extended real numbers and ``a >= b``, as far as
    it is seen from their form, or ``None``. See :func:`greater`.

    Examples
    ========

    >>> from sympy import S
    >>> from sympy.assumptions.rule_engine import not_less
    >>> not_less(S(1), S(1)), not_less(S(1), S(2))
    (True, False)

    """
    if isinstance(a, Rational) and isinstance(b, Rational):
        return a.p*b.q >= b.p*a.q
    return _compared(a, b, ge)


def _compared(a, b, compare):
    if not (getattr(a, 'is_number', False) and getattr(b, 'is_number', False)):
        return None
    a_real = a.is_extended_real
    b_real = b.is_extended_real
    if a_real and b_real:
        result = compare(a, b)
        return True if result is S.true else False if result is S.false else None
    if a_real is False or b_real is False:
        return False
    return None


# The predicates of two arguments which a rule can have as a condition, as
# ``written: (relation, swapped, same)``: ``written(a, b)`` has the truth
# value of ``relation(a, b)``, or of ``relation(b, a)`` if ``swapped``, if
# ``same``, and the opposite truth value otherwise. The compiled rules have
# only the three relations.
WRITTEN = {
    Q.eq: (Q.eq, False, True), Q.ne: (Q.eq, False, False),
    Q.gt: (Q.gt, False, True), Q.lt: (Q.gt, True, True),
    Q.ge: (Q.ge, False, True), Q.le: (Q.ge, True, True),
}

# How each relation is decided from the form of two expressions
RELATIONS = {Q.eq: equal, Q.gt: greater, Q.ge: not_less}


def canonical(written, a, b):
    """
    The relation which ``written(a, b)`` states, as a triple ``(relation,
    a, b)`` of :data:`RELATIONS`, and whether it has the same truth value.

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.abc import x, y
    >>> from sympy.assumptions.rule_engine import canonical
    >>> canonical(Q.lt, x, y)
    ((Q.gt, y, x), True)
    >>> canonical(Q.ne, x, y)
    ((Q.eq, x, y), False)

    """
    relation, swapped, same = WRITTEN[written]
    return ((relation, b, a) if swapped else (relation, a, b)), same


class Comparisons:
    """
    How a relation of :data:`RELATIONS` between two expressions is decided
    under assumptions, which are given as their unit literals ``(applied
    predicate, value)``.

    Explanation
    ===========

    The relation is decided from the form of the two expressions, or by an
    assumption which states it. ``a > b`` also decides ``a >= b`` and
    ``a = b``. No expression is built.

    Examples
    ========

    >>> from sympy import Q, S
    >>> from sympy.abc import x
    >>> from sympy.assumptions.rule_engine import Comparisons
    >>> compared = Comparisons([(Q.lt(1, x), True)])
    >>> compared.decide(Q.gt, x, S(1)), compared.decide(Q.eq, x, S(1))
    (True, False)
    >>> print(compared.decide(Q.gt, x, S(0)))
    None
    >>> Comparisons().decide(Q.gt, S(2), S(1))
    True

    """
    __slots__ = ('stated', 'related')

    def __init__(self, units=()):
        self.stated = stated = {}
        for atom, value in units:
            if len(atom.arguments) == 2 and atom.function in WRITTEN:
                key, same = canonical(atom.function, *atom.arguments)
                stated[key] = value is same
        # The expressions which the stated relations are about
        self.related = {e for key in stated for e in key[1:]} if stated else ()

    def concerns(self, expr):
        """
        Whether an assumption can decide a relation between *expr* and a
        number.
        """
        return expr in self.related

    def decide(self, relation, a, b, form=True):
        """
        The truth value of ``relation(a, b)``, or ``None``. With *form*
        false, the form of the two expressions is not looked at.
        """
        result = RELATIONS[relation](a, b) if form else None
        stated = self.stated
        if result is None and stated:
            result = stated.get((relation, a, b))
            if result is None and relation is not Q.gt:
                if stated.get((Q.gt, a, b)):
                    result = relation is Q.ge
                elif relation is Q.eq:
                    result = False if stated.get((Q.gt, b, a)) else stated.get((Q.eq, b, a))
        return result


def rule_arguments(expr):
    """
    The expressions which the slots of a rule about *expr* stand for.

    Explanation
    ===========

    These are the arguments of *expr*, except that a sum or a product of
    more than two arguments is read as its first argument and the sum or
    the product of the others. Rules about ``f(x, y)`` then apply to sums
    and products of any number of arguments.

    Examples
    ========

    >>> from sympy import sin
    >>> from sympy.abc import x, y, z
    >>> from sympy.assumptions.rule_engine import rule_arguments
    >>> rule_arguments(sin(x))
    (x,)
    >>> rule_arguments(x*y*z)
    (x, y*z)

    A block diagonal matrix is read in the same way.

    """
    args = expr.args
    if len(args) > 2 and isinstance(expr, FIRST_AND_REST):
        if isinstance(expr, AssocOp):
            return (args[0], expr._from_args(args[1:]))
        return (args[0], expr.func(*args[1:]))
    return args


def sat_rules(cls, nargs):
    """
    The compiled clauses which hold for the instances of *cls* that have
    *nargs* rule arguments.

    Explanation
    ===========

    A clause is a tuple of literals ``(predicate, slot, value)``, at least
    one of which is true: the predicate has the truth value ``value`` for
    the expression of the slot.

    Examples
    ========

    >>> from sympy import Abs, Q
    >>> from sympy.assumptions.rule_engine import sat_rules
    >>> ((Q.even, 0, False), (Q.even, -1, True)) in sat_rules(Abs, 1)  # doctest: +SKIP
    True

    """
    return _clauses(cls, nargs)[0]


def split_sat_rules(cls, nargs):
    """
    The clauses of :func:`sat_rules`, as two tuples: those without
    conditions between two arguments, and those with such conditions.
    """
    return _clauses(cls, nargs)[1:]


def _clauses(cls, nargs):
    """
    The clauses of :func:`sat_rules`, those of them without conditions
    between two arguments, and the others.
    """
    key = (cls, nargs)
    entry = _sat_rules.get(key)
    if entry is None:
        rules = tuple(
            clause for base in cls.__mro__ for number in (nargs, None)
            for clause in SAT_RULES.get((base, number), ()))
        plain = []
        related = []
        for clause in rules:
            if any(type(slot) is tuple for _, slot, _ in clause):
                related.append(clause)
            else:
                plain.append(clause)
        entry = _sat_rules[key] = (rules, tuple(plain), tuple(related))
    return entry


def ask_rules(cls, nargs, predicate):
    """
    The ways to find the truth value of *predicate* for an instance of
    *cls* that has *nargs* rule arguments.

    Explanation
    ===========

    A way is a pair ``(answer, conditions)``. Each condition ``(predicate,
    slot, value)`` holds when asking the predicate about the expression of
    the slot gives ``value``, and the answer is given when all of them
    hold.

    The ways include those to find the truth value of another predicate
    which decides *predicate*: a product is real when it is found to be
    positive. After them come the ways which hold for any number of
    arguments. They find the truth value from other predicates of the same
    expression.

    Examples
    ========

    >>> from sympy import Abs, Q
    >>> from sympy.assumptions.rule_engine import ask_rules
    >>> ways = ask_rules(Abs, 1, Q.even)
    >>> (True, ((Q.even, 0, True),)) in ways  # doctest: +SKIP
    True
    >>> (False, ((Q.odd, 0, True),)) in ways  # doctest: +SKIP
    True

    """
    return _ways(cls, nargs, predicate)[0]


def _ways(cls, nargs, predicate):
    """
    The ways of :func:`ask_rules`; those of them without conditions between
    two arguments; the others as triples ``(answer, tests, conditions)``,
    with the conditions between two arguments apart, as pairs ``(index,
    value)`` into the truth values of the conditions between two arguments
    in any way for *cls* and *nargs*; a cache, for each tuple of those truth
    values, of the others which they let apply; those conditions, grouped by
    the slot which is compared with a number, or ``None`` for two slots, as
    tuples ``(slot, conditions, numbers, indices, rest)`` with each
    condition as ``(index, relation, slots)``, the conditions ``Q.eq`` of
    the slot with an explicit
    number as ``numbers``, ``{number: index}``, and their indices, and the
    other conditions as ``rest``; and their number.
    """
    key = (cls, nargs, predicate)
    entry = _ask_rules.get(key)
    if entry is None:
        found = []
        relations = {}
        for base in cls.__mro__:
            ways = ASK_RULES.get((base, nargs))
            if ways:
                for decider, value, answer in _deciders(predicate):
                    found.extend((answer, conditions)
                                 for way_value, conditions in ways.get(decider, ())
                                 if way_value is value)
                relations.update(dict.fromkeys(
                    (relation, slot) for others in ways.values()
                    for _, conditions in others
                    for relation, slot, _ in conditions if type(slot) is tuple))
        _known_classes.setdefault((cls, nargs), any(
            (base, nargs) in ASK_RULES for base in cls.__mro__))
        for base in cls.__mro__:
            found.extend(ASK_RULES.get((base, None), {}).get(predicate, ()))
        rules = tuple(dict.fromkeys(found))
        index = {relation: i for i, relation in enumerate(relations)}
        groups: dict = {}
        numbers: dict = {}
        for (relation, (a, b)), i in index.items():
            slot = None if type(a) is type(b) is int else a if type(a) is int else b
            groups.setdefault(slot, []).append((i, relation, (a, b)))
            other = b if type(a) is int else a
            if slot is not None and relation is Q.eq and _explicit_number(other):
                numbers.setdefault(slot, {})[other] = i
        plain = []
        related = []
        for answer, conditions in rules:
            tests = tuple((index[c[0], c[1]], c[2]) for c in conditions
                          if type(c[1]) is tuple)
            if tests:
                related.append((answer, tests, tuple(
                    c for c in conditions if type(c[1]) is not tuple)))
            else:
                plain.append((answer, conditions))
        entry = _ask_rules[key] = (
            rules, tuple(plain), tuple(related), {},
            tuple(_group(slot, found, numbers.get(slot)) for slot, found in groups.items()),
            len(index))
    return entry


def _explicit_number(a):
    return isinstance(a, Rational) or a in _UNITS


def _group(slot, conditions, numbers):
    """
    The conditions between two arguments which compare *slot* with
    something, as a group of :func:`_ways`.
    """
    if not numbers:
        return (slot, tuple(conditions), None, (), ())
    rest = tuple(c for c in conditions if c[0] not in numbers.values())
    return (slot, tuple(conditions), numbers, tuple(numbers.values()), rest)


def _decided_ways(related, truths):
    """
    The ways of *related* whose conditions between two arguments have the
    truth values *truths*, without those conditions.
    """
    return tuple((answer, conditions) for answer, tests, conditions in related
                 if all(truths[i] is value for i, value in tests))


def _deciders(predicate):
    """
    The literals which decide *predicate*, as triples ``(other, value,
    answer)``: *predicate* is ``answer`` when ``other`` is ``value``.
    """
    deciders = _deciding.get(predicate)
    if deciders is None:
        facts = get_known_facts_dict()
        implied, rejected = facts.get(predicate, ((), ()))
        deciders = [(predicate, True, True), (predicate, False, False)]
        for other in sorted(facts, key=lambda p: p.name):
            if other == predicate:
                continue
            other_implied, other_rejected = facts[other]
            if predicate in other_implied:
                deciders.append((other, True, True))
            if predicate in other_rejected or other in rejected:
                deciders.append((other, True, False))
            if other in implied:
                deciders.append((other, False, False))
        _deciding[predicate] = deciders
    return deciders


def evaluate(predicate, args, assumptions=True):
    """
    The truth value of ``predicate(*args)`` under *assumptions*, as far as
    it is found without logical inference.

    Explanation
    ===========

    The truth value is looked for in the assumptions about the expression
    itself, and then with the handler which is registered to the predicate
    for the class of the expression.

    For the predicates of :data:`RULE_PREDICATES`, the truth value is looked
    for in the old assumptions of the expression, if it is an atom or of a
    class without rules, with a handler which is registered for its class
    itself, and in the compiled rules for its class. The conditions of a
    rule are questions about the arguments of the expression, which are
    answered in the same way.

    A handler which is registered for every expression is used only to
    evaluate numbers: the expression which this function is called for, if
    it is a number, and atoms. A number inside that expression is read from
    its old assumptions.

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.abc import x, y
    >>> from sympy.assumptions.rule_engine import evaluate
    >>> evaluate(Q.even, (x*y,), Q.even(x) & Q.integer(y))
    True
    >>> print(evaluate(Q.even, (x*y,), Q.integer(x) & Q.integer(y)))
    None

    """
    query = getattr(_local, 'query', None)
    asked = args[0] if len(args) == 1 else None
    if query is not None and (
            query.assumptions is assumptions or query.assumptions == assumptions):
        outer, query.asked = query.asked, asked
        try:
            return query.ask(predicate, args)
        finally:
            query.asked = outer
    _local.query = _Query(assumptions, asked)
    try:
        return _local.query.ask(predicate, args)
    finally:
        _local.query = query


class _Query:
    """
    What is found while one query is answered.
    """
    __slots__ = ('assumptions', 'asked', 'assumed', 'compared', 'answers',
                 'asking', 'lowest', 'slots', 'truths', 'plain', 'unknown')

    def __init__(self, assumptions, asked=None):
        self.assumptions = assumptions
        self.asked = asked
        self.assumed, literals = _unit_assumptions(assumptions)
        self.compared = Comparisons(literals)
        self.answers = {}
        self.slots = {}
        # The truth values of the conditions between two arguments of an
        # expression, in the order in which :func:`_ways` lists them for its
        # class.
        self.truths = {}
        # Whether an expression is a symbol without assumptions of any kind,
        # and whether nothing is found about a predicate for such a symbol.
        self.plain = {}
        self.unknown = {}
        # The questions which are being answered, with their depth. A question
        # which comes up again while it is being answered has no answer. What
        # is then found for the questions inside it may be incomplete, and is
        # kept only if it is an answer.
        self.asking = {}
        self.lowest = 0

    def ask(self, predicate, args):
        if len(args) != 1:
            return predicate.eval(args, self.assumptions)
        return self.ask_about(predicate, args[0])

    def ask_about(self, predicate, expr):
        key = (predicate, expr, expr is self.asked)
        answers = self.answers
        if key in answers:
            return answers[key]
        asking = self.asking
        depth = asking.get(key)
        if depth is not None:
            if depth < self.lowest:
                self.lowest = depth
            return None
        depth = len(asking)
        asking[key] = depth
        outer, self.lowest = self.lowest, depth
        try:
            result = self._find(predicate, expr)
        finally:
            del asking[key]
            complete = self.lowest >= depth
            if outer < self.lowest:
                self.lowest = outer
        if result is not None or complete:
            answers[key] = result
        return result

    def _find(self, predicate, expr):
        result = self._assumed(predicate, expr)
        if result is not None:
            return result
        if predicate not in RULE_PREDICATES:
            return _handled_answer(predicate, expr, self.assumptions)
        cls = type(expr)
        number = getattr(expr, 'is_number', False)
        slots = self.slots.get(expr)
        if slots is None:
            slots = self.slots[expr] = rule_arguments(expr)
        key = (cls, len(slots), predicate)
        entry = _ask_rules.get(key)
        if entry is None:
            entry = _ways(*key)
        _, rules, related, decided, groups, count = entry
        # An atom, a number inside the expression which is asked about, and
        # an expression of a class without rules are read from their old
        # assumptions. A handler is used if it is registered for the class
        # itself. The handlers for every expression evaluate numbers, which
        # can take long: they are used for the expression which is asked
        # about and for atoms.
        asked = expr is self.asked
        if not slots or (not asked if number else not _known_classes[key[:2]]):
            result = getattr(expr, 'is_' + predicate.name, None)
            if result is True or result is False:
                return result
        if _has_handler(predicate, cls) or (number and (asked or not slots)):
            result = _handled_answer(predicate, expr, self.assumptions)
            if result is not None:
                return result
        if not (rules or related):
            return None
        targets = (*slots, expr)
        ask_about = self.ask_about
        plain = self.plain
        unknown = self.unknown
        ways = rules
        pending = related
        while True:
            for answer, conditions in ways:
                for condition, slot, value in conditions:
                    target = targets[slot]
                    is_plain = plain.get(target)
                    if is_plain is None:
                        is_plain = plain[target] = (
                            type(target) is Symbol
                            and target not in self.assumed
                            and target.assumptions0 == _NO_ASSUMPTIONS)
                    if is_plain:
                        skip = unknown.get(condition)
                        if skip is None:
                            skip = unknown[condition] = _unknown_for_symbols(condition)
                        if skip:
                            break
                    if ask_about(condition, target) is not value:
                        break
                else:
                    return answer
            # The ways with conditions between two arguments come last, and
            # those conditions are found only when they are needed.
            if not pending:
                return None
            pending = None
            truths = self.truths.get(expr)
            if truths is None:
                truths = self.truths[expr] = self._truths(groups, count, targets)
            ways = decided.get(truths)
            if ways is None:
                ways = decided[truths] = _decided_ways(related, truths)

    def _truths(self, groups, count, targets):
        """
        The truth values of the *count* conditions between two arguments of
        *groups*, for the expressions *targets* of the slots, as
        :class:`Comparisons` decides them.

        A comparison of an argument with a number is decided from the form
        only if the argument is a number, and from the assumptions only if
        they can decide it. An argument which is an explicit number equals
        only the number which it is.
        """
        compared = self.compared
        decide = compared.decide
        found = [None] * count
        for slot, conditions, numbers, indices, rest in groups:
            number = True
            if slot is not None:
                target = targets[slot]
                number = getattr(target, 'is_number', False)
                if not number:
                    if not compared.concerns(target):
                        continue
                elif numbers is not None and _explicit_number(target):
                    for index in indices:
                        found[index] = False
                    index = numbers.get(target)
                    if index is not None:
                        found[index] = True
                    conditions = rest
            for index, relation, (a, b) in conditions:
                if type(a) is int:
                    a = targets[a]
                if type(b) is int:
                    b = targets[b]
                found[index] = decide(relation, a, b, number)
        return tuple(found)

    def _assumed(self, predicate, expr):
        literals = self.assumed.get(expr)
        if literals is None:
            return None
        facts = get_known_facts_dict()
        implied = facts.get(predicate, _NO_FACTS)[0]
        for assumed, value in literals:
            if value:
                assumed_implied, assumed_rejected = facts.get(assumed, _NO_FACTS)
                if predicate in assumed_implied:
                    return True
                if predicate in assumed_rejected:
                    return False
            elif assumed in implied:
                return False
        return None


_NO_FACTS: tuple = ((), ())
_NO_ASSUMPTIONS = {'commutative': True}
_EVERY_EXPRESSION = (object, Basic, Expr)


def _unknown_for_symbols(predicate):
    """
    Whether nothing is found about *predicate* for a symbol which has no
    assumptions of any kind.
    """
    handler = predicate.handler
    stamp = (RULE_PREDICATES, None if handler is None else len(handler.funcs))
    found = _symbols_unknown.get(predicate)
    if found is None or found[0] != stamp:
        symbol = Symbol('x')
        query = _Query(True)
        query.plain[symbol] = False
        found = _symbols_unknown[predicate] = (
            stamp, query.ask_about(predicate, symbol) is None)
    return found[1]


def _handled_answer(predicate, expr, assumptions):
    result = predicate.eval((expr,), assumptions)
    return None if result is None else bool(result)


def _has_handler(predicate, cls):
    """
    Whether a handler is registered to *predicate* for *cls* or for a class
    which it derives from, other than those of every expression.
    """
    handler = predicate.handler
    if handler is None:
        return True
    functions = handler.funcs
    key = (predicate, cls)
    found = _handled.get(key)
    if found is None or found[0] != len(functions):
        function = handler.dispatch(cls)
        found = _handled[key] = (len(functions), function is not None and not any(
            functions.get((generic,)) is function for generic in _EVERY_EXPRESSION))
    return found[1]


def _unit_assumptions(assumptions):
    """
    The assumptions which are a predicate of one expression or the negation
    of one, ``{expression: [(predicate, value), ...]}``, and every assumption
    which is a predicate or the negation of one, as :func:`unit_literals`.
    """
    literals = unit_literals(assumptions)
    units: dict = {}
    for atom, value in literals:
        arguments = atom.arguments
        if len(arguments) == 1:
            units.setdefault(arguments[0], []).append((atom.function, value))
    return units, literals


def unit_literals(assumptions):
    """
    The assumptions which are a predicate or the negation of one, as pairs
    ``(applied predicate, value)``. The assumptions are a formula or a
    :class:`~sympy.assumptions.cnf.CNF`.
    """
    if assumptions is True or assumptions is S.true:
        return ()
    if isinstance(assumptions, CNF):
        return _unit_clauses(assumptions)
    literals = assumptions.args if isinstance(assumptions, And) else (assumptions,)
    found = []
    for literal in literals:
        value = not isinstance(literal, Not)
        atom = literal if value else literal.args[0]
        if not isinstance(atom, AppliedPredicate):
            return _unit_clauses(CNF.from_prop(assumptions))
        found.append((atom, value))
    return found


def _unit_clauses(cnf):
    found = []
    for clause in cnf.clauses:
        if len(clause) == 1:
            literal, = clause
            if isinstance(literal.lit, AppliedPredicate):
                found.append((literal.lit, not literal.is_Not))
    return found
