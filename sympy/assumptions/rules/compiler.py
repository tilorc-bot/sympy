"""
Compiles the rule files of this package into the modules which are used at
run time.

``bin/ask_update.py`` writes the modules of :data:`GENERATED` into
``sympy/assumptions``: the rules as clauses for the SAT solver, and the rules
as ways to answer a query about an expression from its arguments. Nothing in
this package is imported at run time.
"""
from __future__ import annotations

from importlib import import_module

from sympy.assumptions.assume import AppliedPredicate
from sympy.assumptions.cnf import CNF
from sympy.assumptions.facts import get_known_facts
from sympy.assumptions.rules.language import node
from sympy.core.numbers import Integer, Rational
from sympy.logic.boolalg import Implies
from sympy.logic.inference import satisfiable
from sympy.printing.repr import srepr

RULE_MODULES = ('calculus', 'common', 'matrices', 'ntheory', 'order', 'sets')

EXPR = -1

HEADER = '''\
"""
Do NOT manually edit this file.
Instead, run ./bin/ask_update.py.
"""

'''

SAT_RULES_DOC = '''\
# A literal ``(predicate, slot, value)`` says that the predicate has the truth
# value ``value`` for an expression: the argument number ``slot`` of the
# expression which a rule is about, or that expression itself for the slot
# ``EXPR``. A sum, a product and a block diagonal matrix are read as their
# first argument and the rest. A literal ``(Q.eq, (a, b), value)`` is about
# two arguments: ``a`` and ``b`` are slots, or one of them is a number.
EXPR = -1

# For each class and number of arguments, the clauses which hold for every
# instance. At least one literal of a clause is true. Above each group of
# clauses is the rule which they come from. The clauses under ``None`` are for
# any number of arguments.
'''

ASK_RULES_DOC = '''\
# A condition ``(predicate, slot, value)`` holds when asking the predicate
# about an expression gives ``value``. The expression is the argument number
# ``slot`` of the expression which a rule is about, or that expression itself
# for the slot ``EXPR``. A sum, a product and a block diagonal matrix are read
# as their first argument and the rest. A condition ``(Q.eq, (a, b), value)``
# holds when it is found that the arguments of the slots ``a`` and ``b`` are
# equal, or not equal for the value ``False``. One of ``a`` and ``b`` can be
# a number instead of a slot.
EXPR = -1

# For each class and number of arguments, the ways to find the truth value of
# each predicate for an instance: a truth value, and the conditions which
# together give it. The ways under ``None`` are for any number of arguments.
'''


def statements():
    """
    Every statement of the rule files.
    """
    return [statement for name in RULE_MODULES
            for statement in import_module(f'{__package__}.{name}').RULES]


def _literal_key(literal):
    predicate, slot, value = literal
    return (slot == EXPR, slot if isinstance(slot, tuple) else (slot,),
            predicate.name, value)


def clauses(row):
    """
    The clauses of *row*, with each literal as ``(predicate, slot, value)``.

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.assumptions.rules.compiler import clauses
    >>> from sympy.assumptions.rules.language import f, x
    >>> clauses(Q.even(x) >> Q.even(f(x)))
    [((Q.even, 0, False), (Q.even, -1, True))]

    A condition between two arguments has a pair in place of the slot:

    >>> from sympy.assumptions.rules.language import i, j
    >>> clauses((Q.positive_definite(x) & Q.eq(i, j)) >> Q.positive(f(x, i, j)))
    [((Q.positive_definite, 0, False), (Q.eq, (1, 2), False), (Q.positive, -1, True))]

    """
    expr = node(row)
    slots = {arg: i for i, arg in enumerate(expr.args)}
    slots[expr] = EXPR
    result = set()
    for clause in CNF.to_CNF(row).clauses:
        literals = {(lit.lit.function, _slot(lit.lit.arguments, slots), not lit.is_Not)
                    for lit in clause}
        if not any((p, slot, not value) in literals for p, slot, value in literals):
            result.add(tuple(sorted(literals, key=_literal_key)))
    return sorted(result, key=lambda clause: [_literal_key(lit) for lit in clause])


def _slot(arguments, slots):
    if len(arguments) == 1:
        return slots[arguments[0]]
    return tuple(slots.get(arg, arg) for arg in arguments)


def nargs(row):
    """
    The number of arguments of the expression which *row* is about, or
    ``None`` if the row is about one expression alone.
    """
    expr = node(row)
    return len(expr.args) if expr.args or expr.is_Function else None


def _rules():
    table: dict = {}
    seen: dict = {}
    for classes, rows in statements():
        for row in rows:
            for cls in classes:
                key = (cls, nargs(row))
                new = [c for c in clauses(row) if c not in seen.setdefault(key, set())]
                seen[key].update(new)
                if new:
                    table.setdefault(key, []).append((row, new))
    return table


def sat_rules():
    """
    The clauses of every rule: ``{(class, number of arguments): [(row,
    clauses), ...]}``, without the clauses which an earlier row of the same
    key gave, and without the rows about one expression alone which follow
    from the facts between the predicates.
    """
    table = {}
    for key, rows in _rules().items():
        if key[1] is None:
            rows = [(row, row_clauses) for row, row_clauses in rows
                    if satisfiable(get_known_facts(node(row)) & ~row) is not False]
        if rows:
            table[key] = rows
    return table


def _imports(classes, literals):
    numbers = {type(arg) for _, slot, _ in literals if isinstance(slot, tuple)
               for arg in slot if isinstance(arg, Rational)}
    names = sorted({(cls.__module__, cls.__name__) for cls in classes}
                   | {('sympy.core.numbers', 'Integer' if issubclass(number, Integer)
                       else 'Rational') for number in numbers})
    if len({name for _, name in names}) != len(names):
        raise ValueError("two classes of the rules have the same name")
    return ['from sympy.assumptions.ask import Q'] + [
        f'from {module} import {name}' for module, name in names]


def _render_slot(slot):
    if slot == EXPR:
        return 'EXPR'
    if isinstance(slot, tuple):
        return '({})'.format(', '.join(
            srepr(arg) if isinstance(arg, Rational) else str(arg) for arg in slot))
    return str(slot)


def _render(literals):
    items = ['({}, {}, {})'.format(predicate, _render_slot(slot), value)
             for predicate, slot, value in literals]
    return '({}{})'.format(', '.join(items), ',' if len(items) == 1 else '')


def sat_module():
    """
    The source of ``sympy/assumptions/sat_rules_generated.py``.
    """
    table = sat_rules()
    lines = _imports([cls for cls, _ in table],
        [literal for rows in table.values() for _, row_clauses in rows
         for clause in row_clauses for literal in clause])
    lines += ['', *SAT_RULES_DOC.splitlines(), 'SAT_RULES = {']
    for cls, number in sorted(table, key=lambda key: (key[0].__name__, key[1] or -1)):
        lines.append(f'    ({cls.__name__}, {number}): (')
        for row, row_clauses in table[cls, number]:
            lines.append(f'        # {row}')
            lines += [f'        {_render(clause)},' for clause in row_clauses]
        lines.append('    ),')
    lines.append('}')
    return HEADER + '\n'.join(lines) + '\n'


def ways(row, row_clauses=None):
    """
    The ways which *row* gives to find the truth value of a predicate for
    the expression it is about: ``{predicate: {(value, conditions), ...}}``.

    Explanation
    ===========

    A clause gives a way for a literal about the expression: the literal is
    true when all the other literals are false. If the other literals are
    all about arguments, the way is always given. If some of them are about
    the expression too, it is given only for the predicates in the
    conclusion of the row as it is written.

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.assumptions.rules.compiler import ways
    >>> from sympy.assumptions.rules.language import f, x
    >>> ways(Q.zero(x) >> Q.zero(f(x)))
    {Q.zero: {(True, ((Q.zero, 0, True),))}}

    The next row is a way to find ``Q.odd``, and not one to find ``Q.even``
    or ``Q.integer``:

    >>> ways((Q.integer(x) & ~Q.even(x)) >> Q.odd(x))
    {Q.odd: {(True, ((Q.even, -1, False), (Q.integer, -1, True)))}}

    """
    if row_clauses is None:
        row_clauses = clauses(row)
    expr = node(row)
    conclusion = row.args[1] if isinstance(row, Implies) else row
    concluded = {literal.function for literal in conclusion.atoms(AppliedPredicate)
                 if literal.arg == expr}
    found: dict = {}
    for clause in row_clauses:
        about_expr = [literal for literal in clause if literal[1] == EXPR]
        for literal in about_expr:
            predicate, _, value = literal
            if len(about_expr) > 1 and predicate not in concluded:
                continue
            conditions = tuple((p, slot, not v) for p, slot, v in clause
                               if (p, slot, v) != literal)
            found.setdefault(predicate, set()).add((value, conditions))
    return found


def ask_rules():
    """
    The ways to find the truth value of a predicate for an expression from
    what is known about its arguments: ``{(class, number of arguments):
    {predicate: [(value, conditions), ...]}}``.
    """
    table: dict = {}
    for key, rows in _rules().items():
        found = table.setdefault(key, {})
        for row, row_clauses in rows:
            for predicate, new in ways(row, row_clauses).items():
                found.setdefault(predicate, set()).update(new)
    return {key: {predicate: sorted(found[predicate], key=_way_key)
                  for predicate in sorted(found, key=lambda p: p.name)}
            for key, found in table.items() if found}


def _way_key(way):
    value, conditions = way
    return (not value, len(conditions), [_literal_key(c) for c in conditions])


def ask_module():
    """
    The source of ``sympy/assumptions/ask_rules_generated.py``.
    """
    table = ask_rules()
    lines = _imports([cls for cls, _ in table],
        [literal for found in table.values() for ways in found.values()
         for _, conditions in ways for literal in conditions])
    lines += ['', *ASK_RULES_DOC.splitlines(), 'ASK_RULES = {']
    for cls, number in sorted(table, key=lambda key: (key[0].__name__, key[1] or -1)):
        lines.append(f'    ({cls.__name__}, {number}): {{')
        for predicate, ways in table[cls, number].items():
            lines.append(f'        {predicate}: (')
            lines += [f'            ({value}, {_render(conditions)}),'
                      for value, conditions in ways]
            lines.append('        ),')
        lines.append('    },')
    lines.append('}')
    return HEADER + '\n'.join(lines) + '\n'


GENERATED = {
    'ask_rules_generated.py': ask_module,
    'sat_rules_generated.py': sat_module,
}
