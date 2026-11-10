"""
Compiles the rule files of this package into the modules which are used at
run time.

``bin/ask_update.py`` writes the modules of :data:`GENERATED` into
``sympy/assumptions``. Nothing in this package is imported at run time.
"""
from __future__ import annotations

from importlib import import_module

from sympy.assumptions.cnf import CNF
from sympy.assumptions.rules.language import node

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
# ``EXPR``. A sum or a product is read as its first argument and the rest.
EXPR = -1

# For each class and number of arguments, the clauses which hold for every
# instance. At least one literal of a clause is true. Above each group of
# clauses is the rule which they come from.
'''


def statements():
    """
    Every statement of the rule files.
    """
    return [statement for name in RULE_MODULES
            for statement in import_module(f'{__package__}.{name}').RULES]


def _literal_key(literal):
    predicate, slot, value = literal
    return (slot == EXPR, slot, predicate.name, value)


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

    """
    expr = node(row)
    slots = {arg: i for i, arg in enumerate(expr.args)}
    slots[expr] = EXPR
    result = set()
    for clause in CNF.to_CNF(row).clauses:
        literals = {(lit.lit.function, slots[lit.lit.arg], not lit.is_Not)
                    for lit in clause}
        if not any((p, slot, not value) in literals for p, slot, value in literals):
            result.add(tuple(sorted(literals, key=_literal_key)))
    return sorted(result, key=lambda clause: [_literal_key(lit) for lit in clause])


def sat_rules():
    """
    The clauses of every rule: ``{(class, number of arguments): [(row,
    clauses), ...]}``, without the clauses which an earlier row of the same
    key gave.
    """
    table: dict = {}
    seen: dict = {}
    for classes, rows in statements():
        for row in rows:
            nargs = len(node(row).args)
            for cls in classes:
                key = (cls, nargs)
                new = [c for c in clauses(row) if c not in seen.setdefault(key, set())]
                seen[key].update(new)
                if new:
                    table.setdefault(key, []).append((row, new))
    return table


def _imports(classes):
    names = sorted({(cls.__module__, cls.__name__) for cls in classes})
    if len({name for _, name in names}) != len(names):
        raise ValueError("two classes of the rules have the same name")
    return ['from sympy.assumptions.ask import Q'] + [
        f'from {module} import {name}' for module, name in names]


def _render(literals):
    items = ['({}, {}, {})'.format(predicate, 'EXPR' if slot == EXPR else slot, value)
             for predicate, slot, value in literals]
    return '({}{})'.format(', '.join(items), ',' if len(items) == 1 else '')


def sat_module():
    """
    The source of ``sympy/assumptions/sat_rules_generated.py``.
    """
    table = sat_rules()
    lines = _imports(cls for cls, _ in table)
    lines += ['', *SAT_RULES_DOC.splitlines(), 'SAT_RULES = {']
    for cls, nargs in sorted(table, key=lambda key: (key[0].__name__, key[1])):
        lines.append(f'    ({cls.__name__}, {nargs}): (')
        for row, row_clauses in table[cls, nargs]:
            lines.append(f'        # {row}')
            lines += [f'        {_render(clause)},' for clause in row_clauses]
        lines.append('    ),')
    lines.append('}')
    return HEADER + '\n'.join(lines) + '\n'


GENERATED = {
    'sat_rules_generated.py': sat_module,
}
