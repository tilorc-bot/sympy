"""
Rules for the sign of an expression: ``Q.positive``, ``Q.negative``,
``Q.zero`` and the predicates which are made of them.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.core.add import Add
from sympy.core.expr import Expr
from sympy.core.mul import Mul
from sympy.core.power import Pow
from sympy.functions.combinatorial.factorials import factorial
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.exponential import exp, log
from sympy.functions.elementary.trigonometric import acos, acot, asin, atan
from sympy.logic.boolalg import Equivalent
from sympy.matrices.expressions.determinant import Determinant
from sympy.matrices.expressions.matexpr import MatrixElement
from sympy.matrices.expressions.trace import Trace

from .language import base, closed, exponent, f, for_all, i, j, x, y

RULES = (
    # --- any expression ---

    # A real number which is not nonzero is zero
    for_all((Expr,),
        (Q.real(x) & ~Q.nonzero(x)) >> Q.zero(x)),

    # A number which is not real is neither zero nor nonzero
    for_all((Expr,),
        ~Q.real(x) >> ~Q.zero(x),
        ~Q.real(x) >> ~Q.nonzero(x)),

    # --- Abs ---

    # An absolute value is not negative
    #     it is oo, which is not a real number, for an infinite argument
    for_all((Abs,),
        Q.extended_nonnegative(f(x)),
        Q.finite(x) >> Q.nonnegative(f(x))),

    # An absolute value is zero only at zero
    for_all((Abs,),
        Equivalent(Q.zero(f(x)), Q.zero(x))),

    # The absolute value of a finite nonzero number is positive
    for_all((Abs,),
        (Q.finite(x) & ~Q.zero(x)) >> Q.positive(f(x))),

    # --- Add ---

    # A sum of positive terms is positive, one of negative terms negative
    for_all((Add,),
        closed(f(x, y), Q.positive, Q.negative)),

    # A positive number plus a number which is not negative is positive
    for_all((Add,),
        (Q.positive(x) & Q.nonnegative(y)) >> Q.positive(f(x, y)),
        (Q.nonnegative(x) & Q.positive(y)) >> Q.positive(f(x, y)),
        (Q.negative(x) & Q.nonpositive(y)) >> Q.negative(f(x, y)),
        (Q.nonpositive(x) & Q.negative(y)) >> Q.negative(f(x, y))),

    # A real number plus an imaginary number is not real
    for_all((Add,),
        (Q.real(x) & Q.imaginary(y)) >> ~Q.extended_real(f(x, y)),
        (Q.imaginary(x) & Q.real(y)) >> ~Q.extended_real(f(x, y))),

    # A sum of terms which are not negative is not negative
    for_all((Add,),
        closed(f(x, y), Q.nonnegative, Q.nonpositive)),

    # A sum of terms of the same extended sign has that sign
    #     oo - oo is nan
    for_all((Add,),
        closed(f(x, y), Q.extended_positive, Q.extended_negative,
               Q.extended_nonnegative, Q.extended_nonpositive)),

    # --- Mul ---

    # Sign of a product
    #     x is the first factor and y the product of the others
    for_all((Mul,),
        (Q.positive(x) & Q.positive(y)) >> Q.positive(f(x, y)),
        (Q.negative(x) & Q.negative(y)) >> Q.positive(f(x, y)),
        (Q.positive(x) & Q.negative(y)) >> Q.negative(f(x, y)),
        (Q.negative(x) & Q.positive(y)) >> Q.negative(f(x, y))),

    # A product of nonzero numbers is nonzero
    for_all((Mul,),
        closed(f(x, y), Q.nonzero)),

    # Sign of a product of numbers which may be zero
    for_all((Mul,),
        (Q.nonnegative(x) & Q.nonnegative(y)) >> Q.nonnegative(f(x, y)),
        (Q.nonpositive(x) & Q.nonpositive(y)) >> Q.nonnegative(f(x, y)),
        (Q.nonnegative(x) & Q.nonpositive(y)) >> Q.nonpositive(f(x, y)),
        (Q.nonpositive(x) & Q.nonnegative(y)) >> Q.nonpositive(f(x, y))),

    # Extended sign of a product
    #     0*oo is nan, so the factors are not zero
    for_all((Mul,),
        (Q.extended_positive(x) & Q.extended_positive(y))
        >> Q.extended_positive(f(x, y)),
        (Q.extended_negative(x) & Q.extended_negative(y))
        >> Q.extended_positive(f(x, y)),
        (Q.extended_positive(x) & Q.extended_negative(y))
        >> Q.extended_negative(f(x, y)),
        (Q.extended_negative(x) & Q.extended_positive(y))
        >> Q.extended_negative(f(x, y))),

    # A product is zero only if a factor is zero
    for_all((Mul,),
        Q.zero(f(x, y)) >> (Q.zero(x) | Q.zero(y))),

    # Zero times a finite number is zero
    #     0*oo is nan
    for_all((Mul,),
        (Q.zero(x) & Q.finite(y)) >> Q.zero(f(x, y)),
        (Q.finite(x) & Q.zero(y)) >> Q.zero(f(x, y))),

    # A product with a zero factor is not nonzero
    #     it is zero, or nan if another factor is infinite
    for_all((Mul,),
        Q.zero(x) >> ~Q.extended_nonzero(f(x, y)),
        Q.zero(y) >> ~Q.extended_nonzero(f(x, y))),

    # --- Pow ---

    # Any number to the power zero is one
    for_all((Pow,),
        Q.zero(exponent) >> Q.positive(f(base, exponent))),

    # One to a finite power is positive
    #     it is 1, and 1**oo is nan
    for_all((Pow,),
        (Q.eq(base, 1) & Q.finite(exponent)) >> Q.positive(f(base, exponent))),

    # A positive number to a real power is positive
    for_all((Pow,),
        (Q.positive(base) & Q.real(exponent)) >> Q.positive(f(base, exponent))),

    # A nonzero real number to an even power is positive
    for_all((Pow,),
        (Q.nonzero(base) & Q.even(exponent)) >> Q.positive(f(base, exponent))),

    # A negative number to an odd power is negative
    for_all((Pow,),
        (Q.negative(base) & Q.odd(exponent)) >> Q.negative(f(base, exponent))),

    # A real number to an even power is not negative
    #     0**-2 is zoo
    for_all((Pow,),
        (Q.real(base) & Q.even(exponent)) >> ~Q.negative(f(base, exponent)),
        (Q.real(base) & Q.even(exponent) & Q.nonnegative(exponent))
        >> Q.nonnegative(f(base, exponent))),

    # An odd power keeps the sign of its base
    #     0**-1 is zoo
    for_all((Pow,),
        (Q.nonnegative(base) & Q.odd(exponent)) >> ~Q.negative(f(base, exponent)),
        (Q.nonnegative(base) & Q.odd(exponent) & Q.nonnegative(exponent))
        >> Q.nonnegative(f(base, exponent)),
        (Q.nonpositive(base) & Q.odd(exponent) & Q.nonnegative(exponent))
        >> Q.nonpositive(f(base, exponent))),

    # Zero to a positive power is zero
    for_all((Pow,),
        (Q.zero(base) & Q.positive(exponent)) >> Q.zero(f(base, exponent))),

    # A positive power is zero only if the base is zero
    #     a positive power of an infinite base is infinite
    for_all((Pow,),
        (Q.zero(f(base, exponent)) & Q.positive(exponent)) >> Q.zero(base)),

    # A power of finite numbers is zero only if the base is zero
    #     for another base it is exp(exponent*log(base)); oo**-1 is zero
    for_all((Pow,),
        (Q.zero(f(base, exponent)) & Q.finite(base) & Q.finite(exponent))
        >> Q.zero(base)),

    # A real power of a finite base is zero only if the exponent is positive
    #     0**0 is 1 and 0**-1 is zoo; 2**-oo is zero
    for_all((Pow,),
        (Q.zero(f(base, exponent)) & Q.finite(base) & Q.real(exponent))
        >> Q.positive(exponent)),

    # --- exp ---

    # The exponential of a real number is positive
    for_all((exp,),
        Q.real(x) >> Q.positive(f(x))),

    # The exponential of an extended real number is not negative
    #     exp(-oo) is zero and exp(oo) is oo
    for_all((exp,),
        Q.extended_real(x) >> Q.extended_nonnegative(f(x))),

    # The exponential of a finite number is not zero
    for_all((exp,),
        Q.finite(x) >> ~Q.zero(f(x))),

    # --- log ---

    # The logarithm of a number which is not positive is not real
    #     log(0) is zoo, log(-1) is I*pi and log(-oo) is oo
    for_all((log,),
        ~Q.positive(x) >> ~Q.real(f(x))),

    # --- factorial ---

    # The factorial of a natural number is positive
    #     factorial(-1) is zoo
    for_all((factorial,),
        (Q.integer(x) & Q.nonnegative(x)) >> Q.positive(f(x))),

    # --- atan, acot ---

    # Not real at a finite number which is not real
    #     acot(x) is atan(1/x); atan(I) is oo*I
    for_all((atan, acot),
        (Q.finite(x) & ~Q.real(x)) >> ~Q.extended_real(f(x))),

    # The arctangent has the sign of its argument
    #     atan(oo) is pi/2
    for_all((atan,),
        Q.extended_positive(x) >> Q.positive(f(x)),
        Q.extended_negative(x) >> Q.negative(f(x)),
        Q.zero(x) >> Q.zero(f(x))),

    # The arccotangent has the sign of its argument, and is pi/2 at zero
    #     acot(oo) is zero
    for_all((acot,),
        Q.nonnegative(x) >> Q.positive(f(x)),
        Q.negative(x) >> Q.negative(f(x)),
        Q.extended_nonnegative(x) >> Q.extended_nonnegative(f(x)),
        Q.extended_negative(x) >> Q.nonpositive(f(x))),

    # --- asin ---

    # The arcsine has the sign of its argument where it is real
    #     asin(2) is not real
    for_all((asin,),
        Q.zero(x) >> Q.zero(f(x)),
        Q.extended_nonnegative(x) >> ~Q.negative(f(x)),
        Q.extended_nonpositive(x) >> ~Q.positive(f(x))),

    # --- acos ---

    # The arccosine is not negative
    #     acos(1) is zero and acos(2) is not real
    for_all((acos,),
        ~Q.negative(f(x)),
        Q.zero(x) >> Q.positive(f(x))),

    # --- Determinant, Trace ---

    # The determinant and the trace of a positive definite matrix are
    # positive
    #     the eigenvalues are positive
    for_all((Determinant, Trace),
        Q.positive_definite(x) >> Q.positive(f(x))),

    # --- MatrixElement ---

    # The diagonal entries of a positive definite matrix are positive
    #     the entry X[i, i] is e.T*X*e for the unit vector e of the index i
    for_all((MatrixElement,),
        (Q.positive_definite(x) & Q.eq(i, j)) >> Q.positive(f(x, i, j))),
)
