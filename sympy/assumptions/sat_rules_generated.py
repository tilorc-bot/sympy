"""
Do NOT manually edit this file.
Instead, run ./bin/ask_update.py.
"""

from sympy.assumptions.ask import Q

# A literal ``(predicate, slot, value)`` says that the predicate has the truth
# value ``value`` for an expression: the argument number ``slot`` of the
# expression which a rule is about, or that expression itself for the slot
# ``EXPR``. A sum, a product and a block diagonal matrix are read as their
# first argument and the rest. A literal ``(Q.eq, (a, b), value)``, ``(Q.gt,
# (a, b), value)`` or ``(Q.ge, (a, b), value)`` is about two arguments: ``a``
# and ``b`` are slots, or one of them is a number. ``Q.gt`` and ``Q.ge`` say
# that both are extended real and ``a > b`` or ``a >= b``.
EXPR = -1

# For each class and number of arguments, the clauses which hold for every
# instance. At least one literal of a clause is true. Above each group of
# clauses is the rule which they come from. The clauses under ``None`` are for
# any number of arguments.
SAT_RULES = {
}
