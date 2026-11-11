"""
This module contains query handlers responsible for calculus queries:
infinitesimal, finite, etc.
"""
from __future__ import annotations

from sympy.assumptions import Q
from sympy.assumptions.ask import _ask_recursive
from sympy.core import Expr, Add, Mul, Pow
from sympy.core.numbers import E

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

@FinitePredicate.register(Pow)
def _(expr, assumptions):
    """
    * Unbounded ** NonZero -> Unbounded

    * Bounded ** Bounded -> Bounded

    * Abs()<=1 ** Positive -> Bounded

    * Abs()>=1 ** Negative -> Bounded

    * Otherwise unknown
    """
    if expr.base == E:
        return _ask_recursive(Q.finite(expr.exp), assumptions)

    base_bounded = _ask_recursive(Q.finite(expr.base), assumptions)
    exp_bounded = _ask_recursive(Q.finite(expr.exp), assumptions)
    if base_bounded is None and exp_bounded is None:  # Common Case
        return None
    if base_bounded is False and _ask_recursive(Q.extended_nonzero(expr.exp), assumptions):
        return False
    if base_bounded and exp_bounded:
        is_base_zero = _ask_recursive(Q.zero(expr.base), assumptions)
        is_exp_negative = _ask_recursive(Q.negative(expr.exp), assumptions)
        if is_base_zero is True and is_exp_negative is True:
            return False
        if is_base_zero is not False and is_exp_negative is not False:
            return None
        return True
    if (abs(expr.base) <= 1) == True and _ask_recursive(Q.extended_positive(expr.exp), assumptions):
        return True
    if (abs(expr.base) >= 1) == True and _ask_recursive(Q.extended_negative(expr.exp), assumptions):
        return True
    if (abs(expr.base) >= 1) == True and exp_bounded is False:
        return False
    return None


# InfinitePredicate


@InfinitePredicate.register(Expr)
def _(expr, assumptions):
    is_finite = _ask_recursive(Q.finite(expr), assumptions)
    if is_finite is None:
        return None
    return not is_finite
