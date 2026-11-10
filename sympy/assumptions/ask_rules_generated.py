"""
Do NOT manually edit this file.
Instead, run ./bin/ask_update.py.
"""

from sympy.assumptions.ask import Q

# A condition ``(predicate, slot, value)`` holds when asking the predicate
# about an expression gives ``value``. The expression is the argument number
# ``slot`` of the expression which a rule is about, or that expression itself
# for the slot ``EXPR``. A sum, a product and a block diagonal matrix are read
# as their first argument and the rest. A condition ``(Q.eq, (a, b), value)``
# holds when it is found that the arguments of the slots ``a`` and ``b`` are
# equal, or not equal for the value ``False``. A condition ``(Q.gt, (a, b),
# True)`` holds when it is found that both are extended real and ``a > b``,
# and ``(Q.ge, (a, b), True)`` when ``a >= b``. One of ``a`` and ``b`` can be
# a number instead of a slot.
EXPR = -1

# For each class and number of arguments, the ways to find the truth value of
# each predicate for an instance: a truth value, and the conditions which
# together give it. The ways under ``None`` are for any number of arguments.
ASK_RULES = {
}
