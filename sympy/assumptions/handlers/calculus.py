"""
This module contains query handlers responsible for calculus queries:
infinitesimal, finite, etc.
"""
from __future__ import annotations

from sympy.assumptions import Q
from sympy.assumptions.ask import _ask_recursive
from sympy.core import Expr, Add, Mul

from ..predicates.calculus import FinitePredicate, InfinitePredicate


# FinitePredicate


@FinitePredicate.register(Add)
def _(expr, assumptions):
    """
    Return True if expr is bounded, False if not and None if unknown.

    Truth Table:

    +-------+-----+-----------+-----------+
    |       |     |           |           |
    |       |  B  |     U     |     ?     |
    |       |     |           |           |
    +-------+-----+---+---+---+---+---+---+
    |       |     |   |   |   |   |   |   |
    |       |     |'+'|'-'|'x'|'+'|'-'|'x'|
    |       |     |   |   |   |   |   |   |
    +-------+-----+---+---+---+---+---+---+
    |       |     |           |           |
    |   B   |  B  |     U     |     ?     |
    |       |     |           |           |
    +---+---+-----+---+---+---+---+---+---+
    |   |   |     |   |   |   |   |   |   |
    |   |'+'|     | U | ? | ? | U | ? | ? |
    |   |   |     |   |   |   |   |   |   |
    |   +---+-----+---+---+---+---+---+---+
    |   |   |     |   |   |   |   |   |   |
    | U |'-'|     | ? | U | ? | ? | U | ? |
    |   |   |     |   |   |   |   |   |   |
    |   +---+-----+---+---+---+---+---+---+
    |   |   |     |           |           |
    |   |'x'|     |     ?     |     ?     |
    |   |   |     |           |           |
    +---+---+-----+---+---+---+---+---+---+
    |       |     |           |           |
    |   ?   |     |           |     ?     |
    |       |     |           |           |
    +-------+-----+-----------+---+---+---+

        * 'B' = Bounded

        * 'U' = Unbounded

        * '?' = unknown boundedness

        * '+' = positive sign

        * '-' = negative sign

        * 'x' = sign unknown

        * All Bounded -> True

        * 1 Unbounded and the rest Bounded -> False

        * >1 Unbounded, all with same known sign -> False

        * Any Unknown and unknown sign -> None

        * Else -> None

    When the signs are not the same you can have an undefined
    result as in oo - oo, hence 'bounded' is also undefined.
    """
    sign = -1  # sign of unknown or infinite
    result = True
    for arg in expr.args:
        _bounded = _ask_recursive(Q.finite(arg), assumptions)
        if _bounded:
            continue
        s = _ask_recursive(Q.extended_positive(arg), assumptions)
        # if there has been more than one sign or if the sign of this arg
        # is None and Bounded is None or there was already
        # an unknown sign, return None
        if sign != -1 and s != sign or \
                s is None and None in (_bounded, sign):
            return None
        else:
            sign = s
        # once False, do not change
        if result is not False:
            result = _bounded
    return result

@FinitePredicate.register(Mul)
def _(expr, assumptions):
    """
    Return True if expr is bounded, False if not and None if unknown.

    Truth Table:

    +---+---+---+--------+
    |   |   |   |        |
    |   | B | U |   ?    |
    |   |   |   |        |
    +---+---+---+---+----+
    |   |   |   |   |    |
    |   |   |   | s | /s |
    |   |   |   |   |    |
    +---+---+---+---+----+
    |   |   |   |        |
    | B | B | U |   ?    |
    |   |   |   |        |
    +---+---+---+---+----+
    |   |   |   |   |    |
    | U |   | U | U | ?  |
    |   |   |   |   |    |
    +---+---+---+---+----+
    |   |   |   |        |
    | ? |   |   |   ?    |
    |   |   |   |        |
    +---+---+---+---+----+

        * B = Bounded

        * U = Unbounded

        * ? = unknown boundedness

        * s = signed (hence nonzero)

        * /s = not signed
    """
    result = True
    possible_zero = False
    for arg in expr.args:
        _bounded = _ask_recursive(Q.finite(arg), assumptions)
        if _bounded:
            if _ask_recursive(Q.zero(arg), assumptions) is not False:
                if result is False:
                    return None
                possible_zero = True
        elif _bounded is None:
            if result is None:
                return None
            if _ask_recursive(Q.extended_nonzero(arg), assumptions) is None:
                return None
            if result is not False:
                result = None
        else:
            if possible_zero:
                return None
            result = False
    return result


# InfinitePredicate


@InfinitePredicate.register(Expr)
def _(expr, assumptions):
    is_finite = _ask_recursive(Q.finite(expr), assumptions)
    if is_finite is None:
        return None
    return not is_finite
