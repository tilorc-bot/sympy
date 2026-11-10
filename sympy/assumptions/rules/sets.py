"""
Rules for the sets of numbers an expression is in: ``Q.integer``,
``Q.rational``, ``Q.irrational``, ``Q.real``, ``Q.imaginary`` and others.
"""
from __future__ import annotations

from sympy.assumptions.ask import Q
from sympy.core.add import Add
from sympy.core.expr import Expr
from sympy.core.mul import Mul
from sympy.core.numbers import Rational
from sympy.core.power import Pow
from sympy.core.singleton import S
from sympy.functions.elementary.complexes import Abs, im, re, sign
from sympy.functions.elementary.exponential import exp, log
from sympy.functions.elementary.trigonometric import (acos, acot, asin, atan,
    cos, cot, sin, tan)
from sympy.logic.boolalg import Equivalent
from sympy.matrices.expressions.determinant import Determinant
from sympy.matrices.expressions.matexpr import MatrixElement
from sympy.matrices.expressions.trace import Trace

from sympy.assumptions.rule_language import base, closed, exponent, f, for_all, i, j, x, y

RULES = (
    # --- any expression ---

    # A real number which is not rational is irrational
    for_all((Expr,),
        (Q.real(x) & ~Q.rational(x)) >> Q.irrational(x)),

    # A complex number which is not algebraic is transcendental
    for_all((Expr,),
        (Q.complex(x) & ~Q.algebraic(x)) >> Q.transcendental(x)),

    # A real number is hermitian
    for_all((Expr,),
        Q.real(x) >> Q.hermitian(x)),

    # An imaginary number is antihermitian
    for_all((Expr,),
        Q.imaginary(x) >> Q.antihermitian(x)),

    # A number which is zero or has a sign, possibly infinite, is extended
    # real
    for_all((Expr,),
        Q.extended_positive(x) >> Q.extended_real(x),
        Q.extended_negative(x) >> Q.extended_real(x),
        Q.zero(x) >> Q.extended_real(x)),

    # --- Abs ---

    # The absolute value of an integer, a rational or an algebraic number is
    # one too
    #     abs(a)**2 is a times its conjugate
    for_all((Abs,),
        closed(f(x), Q.integer, Q.rational, Q.algebraic)),

    # The absolute value of an irrational number is irrational
    for_all((Abs,),
        Q.irrational(x) >> Q.irrational(f(x))),

    # --- Abs, re, im ---

    # The absolute value, the real part and the imaginary part of a complex
    # number are real
    #     they are oo for oo, and re(zoo) is nan
    for_all((Abs, re, im),
        Q.complex(x) >> Q.real(f(x))),

    # The real part of an extended real number is itself
    for_all((re,),
        closed(f(x), Q.extended_real)),

    # A real part and an imaginary part are not imaginary
    #     they are extended real, or nan
    for_all((re, im),
        ~Q.imaginary(f(x))),

    # --- Add ---

    # The reals, the rationals, the integers and the algebraic numbers are
    # closed under addition, and so are the complex, the hermitian and the
    # antihermitian numbers
    for_all((Add,),
        closed(f(x, y), Q.real, Q.rational, Q.integer, Q.algebraic,
               Q.complex, Q.hermitian, Q.antihermitian)),

    # An integer plus a number which is not an integer is not an integer
    #     the difference of two integers is an integer
    for_all((Add,),
        (Q.integer(x) & ~Q.integer(y)) >> ~Q.integer(f(x, y)),
        (~Q.integer(x) & Q.integer(y)) >> ~Q.integer(f(x, y))),

    # A rational number plus a number which is not rational is not rational
    #     the difference of two rational numbers is rational
    for_all((Add,),
        (Q.rational(x) & ~Q.rational(y)) >> ~Q.rational(f(x, y)),
        (~Q.rational(x) & Q.rational(y)) >> ~Q.rational(f(x, y))),

    # A rational number plus an irrational number is irrational
    #     the difference of two rational numbers is rational
    for_all((Add,),
        (Q.rational(x) & Q.irrational(y)) >> Q.irrational(f(x, y)),
        (Q.irrational(x) & Q.rational(y)) >> Q.irrational(f(x, y))),

    # A real number plus a number which is not real is not real
    #     the difference of two real numbers is real
    for_all((Add,),
        (Q.real(x) & ~Q.real(y)) >> ~Q.real(f(x, y)),
        (~Q.real(x) & Q.real(y)) >> ~Q.real(f(x, y))),

    # An extended real number plus a number which is not extended real is
    # not extended real
    #     oo + I is not extended real, and oo + zoo is nan
    for_all((Add,),
        (Q.extended_real(x) & ~Q.extended_real(y)) >> ~Q.extended_real(f(x, y)),
        (~Q.extended_real(x) & Q.extended_real(y)) >> ~Q.extended_real(f(x, y))),

    # A real number plus an extended real number is extended real
    #     oo - oo is nan
    for_all((Add,),
        (Q.real(x) & Q.extended_real(y)) >> Q.extended_real(f(x, y)),
        (Q.extended_real(x) & Q.real(y)) >> Q.extended_real(f(x, y))),

    # A sum of extended real numbers of the same sign is extended real
    for_all((Add,),
        (Q.extended_positive(x) & Q.extended_positive(y))
        >> Q.extended_real(f(x, y)),
        (Q.extended_negative(x) & Q.extended_negative(y))
        >> Q.extended_real(f(x, y))),

    # A complex number plus a number which is not complex is not complex
    #     the difference of two complex numbers is complex
    for_all((Add,),
        (Q.complex(x) & ~Q.complex(y)) >> ~Q.complex(f(x, y)),
        (~Q.complex(x) & Q.complex(y)) >> ~Q.complex(f(x, y))),

    # An algebraic number plus a number which is not algebraic is not
    # algebraic
    #     the difference of two algebraic numbers is algebraic
    for_all((Add,),
        (Q.algebraic(x) & ~Q.algebraic(y)) >> ~Q.algebraic(f(x, y)),
        (~Q.algebraic(x) & Q.algebraic(y)) >> ~Q.algebraic(f(x, y))),

    # An algebraic number plus a transcendental number is transcendental
    for_all((Add,),
        (Q.algebraic(x) & Q.transcendental(y)) >> Q.transcendental(f(x, y)),
        (Q.transcendental(x) & Q.algebraic(y)) >> Q.transcendental(f(x, y))),

    # A hermitian plus a number which is not hermitian is not hermitian
    #     the difference of two hermitian numbers is hermitian
    for_all((Add,),
        (Q.hermitian(x) & ~Q.hermitian(y)) >> ~Q.hermitian(f(x, y)),
        (~Q.hermitian(x) & Q.hermitian(y)) >> ~Q.hermitian(f(x, y))),

    # An antihermitian plus a number which is not antihermitian is not
    # antihermitian
    #     the difference of two antihermitian numbers is antihermitian
    for_all((Add,),
        (Q.antihermitian(x) & ~Q.antihermitian(y)) >> ~Q.antihermitian(f(x, y)),
        (~Q.antihermitian(x) & Q.antihermitian(y)) >> ~Q.antihermitian(f(x, y))),

    # A sum of imaginary numbers is imaginary unless it is zero
    #     I - I is zero
    for_all((Add,),
        (Q.imaginary(x) & Q.imaginary(y) & ~Q.zero(f(x, y)))
        >> Q.imaginary(f(x, y))),

    # A nonzero real number plus an imaginary number is not imaginary
    #     its real part is not zero
    for_all((Add,),
        (Q.real(x) & ~Q.zero(x) & Q.imaginary(y)) >> ~Q.imaginary(f(x, y)),
        (Q.imaginary(x) & Q.real(y) & ~Q.zero(y)) >> ~Q.imaginary(f(x, y))),

    # --- Mul ---

    # The reals, the rationals, the integers and the algebraic and the
    # complex numbers are closed under multiplication
    for_all((Mul,),
        closed(f(x, y), Q.real, Q.rational, Q.integer, Q.algebraic, Q.complex)),

    # A nonzero rational number times a number which is not rational is not
    # rational
    #     the quotient of two rational numbers is rational
    for_all((Mul,),
        (Q.rational(x) & ~Q.zero(x) & ~Q.rational(y)) >> ~Q.rational(f(x, y)),
        (~Q.rational(x) & Q.rational(y) & ~Q.zero(y)) >> ~Q.rational(f(x, y))),

    # A nonzero rational number times an irrational number is irrational
    for_all((Mul,),
        (Q.rational(x) & ~Q.zero(x) & Q.irrational(y)) >> Q.irrational(f(x, y)),
        (Q.irrational(x) & Q.rational(y) & ~Q.zero(y)) >> Q.irrational(f(x, y))),

    # A nonzero algebraic number times a number which is not algebraic is
    # not algebraic
    #     the quotient of two algebraic numbers is algebraic
    for_all((Mul,),
        (Q.algebraic(x) & ~Q.zero(x) & ~Q.algebraic(y)) >> ~Q.algebraic(f(x, y)),
        (~Q.algebraic(x) & Q.algebraic(y) & ~Q.zero(y)) >> ~Q.algebraic(f(x, y))),

    # A nonzero algebraic number times a transcendental number is
    # transcendental
    for_all((Mul,),
        (Q.algebraic(x) & ~Q.zero(x) & Q.transcendental(y))
        >> Q.transcendental(f(x, y)),
        (Q.transcendental(x) & Q.algebraic(y) & ~Q.zero(y))
        >> Q.transcendental(f(x, y))),

    # A complex number times a number which is not complex is not complex
    #     the quotient of two complex numbers is complex, and 0*oo is nan
    for_all((Mul,),
        (Q.complex(x) & ~Q.complex(y)) >> ~Q.complex(f(x, y)),
        (~Q.complex(x) & Q.complex(y)) >> ~Q.complex(f(x, y))),

    # A product of two imaginary numbers is real
    for_all((Mul,),
        (Q.imaginary(x) & Q.imaginary(y)) >> Q.real(f(x, y))),

    # A nonzero real number times an imaginary number is imaginary
    for_all((Mul,),
        (Q.real(x) & ~Q.zero(x) & Q.imaginary(y)) >> Q.imaginary(f(x, y)),
        (Q.imaginary(x) & Q.real(y) & ~Q.zero(y)) >> Q.imaginary(f(x, y))),

    # A real number times an imaginary number is real only if it is zero
    for_all((Mul,),
        (Q.real(x) & Q.imaginary(y)) >> Equivalent(Q.real(f(x, y)), Q.zero(f(x, y))),
        (Q.imaginary(x) & Q.real(y)) >> Equivalent(Q.real(f(x, y)), Q.zero(f(x, y)))),

    # Half a number is an integer exactly when the number is even
    #     an even number is twice an integer, and a number factor of a
    #     product is its first argument; a row cannot say "half of an odd
    #     integer", so 3*x/2 is not covered
    for_all((Mul,),
        (Q.eq(x, S.Half) & Q.even(y)) >> Q.integer(f(x, y)),
        (Q.eq(x, S.Half) & ~Q.even(y)) >> ~Q.integer(f(x, y)),
        (Q.eq(x, -S.Half) & Q.even(y)) >> Q.integer(f(x, y)),
        (Q.eq(x, -S.Half) & ~Q.even(y)) >> ~Q.integer(f(x, y))),

    # A product of nonzero extended real numbers is extended real
    #     0*oo is nan
    for_all((Mul,),
        (Q.extended_real(x) & ~Q.zero(x) & Q.extended_real(y) & ~Q.zero(y))
        >> Q.extended_real(f(x, y))),

    # A nonzero real number times an extended real number is extended real
    #     0*oo is nan
    for_all((Mul,),
        (Q.nonzero(x) & Q.extended_real(y)) >> Q.extended_real(f(x, y)),
        (Q.extended_real(x) & Q.nonzero(y)) >> Q.extended_real(f(x, y))),

    # A product of hermitian or antihermitian factors which commute is
    # hermitian or antihermitian
    #     a factor which is a number commutes with the others
    for_all((Mul,),
        (Q.hermitian(x) & Q.hermitian(y) & Q.commutative(x)) >> Q.hermitian(f(x, y)),
        (Q.hermitian(x) & Q.hermitian(y) & Q.commutative(y)) >> Q.hermitian(f(x, y)),
        (Q.antihermitian(x) & Q.antihermitian(y) & Q.commutative(x))
        >> Q.hermitian(f(x, y)),
        (Q.antihermitian(x) & Q.antihermitian(y) & Q.commutative(y))
        >> Q.hermitian(f(x, y)),
        (Q.hermitian(x) & Q.antihermitian(y) & Q.commutative(x))
        >> Q.antihermitian(f(x, y)),
        (Q.hermitian(x) & Q.antihermitian(y) & Q.commutative(y))
        >> Q.antihermitian(f(x, y)),
        (Q.antihermitian(x) & Q.hermitian(y) & Q.commutative(x))
        >> Q.antihermitian(f(x, y)),
        (Q.antihermitian(x) & Q.hermitian(y) & Q.commutative(y))
        >> Q.antihermitian(f(x, y))),

    # --- Pow ---

    # Anything to the power zero is one
    for_all((Pow,),
        Q.zero(exponent) >> Q.integer(f(base, exponent))),

    # A nonnegative integer power of an integer is an integer
    for_all((Pow,),
        (Q.integer(base) & Q.integer(exponent) & ~Q.negative(exponent))
        >> Q.integer(f(base, exponent))),

    # An integer power of a rational, a real, an algebraic, a complex or a
    # hermitian number is one too
    #     0**-1 is zoo
    for_all((Pow,),
        (Q.rational(base) & ~Q.zero(base) & Q.integer(exponent))
        >> Q.rational(f(base, exponent)),
        (Q.rational(base) & Q.integer(exponent) & ~Q.negative(exponent))
        >> Q.rational(f(base, exponent)),
        (Q.real(base) & ~Q.zero(base) & Q.integer(exponent))
        >> Q.real(f(base, exponent)),
        (Q.real(base) & Q.integer(exponent) & ~Q.negative(exponent))
        >> Q.real(f(base, exponent)),
        (Q.hermitian(base) & ~Q.zero(base) & Q.integer(exponent))
        >> Q.hermitian(f(base, exponent)),
        (Q.hermitian(base) & Q.integer(exponent) & ~Q.negative(exponent))
        >> Q.hermitian(f(base, exponent))),

    # A negative integer power of an integer other than 1 and -1 is not an
    # integer
    #     it is a fraction with a numerator of 1 or -1, and 0**-1 is zoo
    for_all((Pow,),
        (Q.integer(base) & Q.ne(base, 1) & Q.ne(base, -1) & Q.integer(exponent)
         & Q.negative(exponent))
        >> ~Q.integer(f(base, exponent))),

    # The inverse of an irrational number is irrational
    #     the inverse of a rational number is rational
    for_all((Pow,),
        (Q.irrational(base) & Q.eq(exponent, -1)) >> Q.irrational(f(base, exponent))),

    # A rational power of an algebraic number is algebraic
    #     0**-1 is zoo
    for_all((Pow,),
        (Q.algebraic(base) & ~Q.zero(base) & Q.rational(exponent))
        >> Q.algebraic(f(base, exponent)),
        (Q.algebraic(base) & Q.rational(exponent) & ~Q.negative(exponent))
        >> Q.algebraic(f(base, exponent))),

    # An algebraic number other than 0 and 1 to an algebraic power which is
    # not rational is transcendental
    #     the Gelfond-Schneider theorem
    for_all((Pow,),
        (Q.algebraic(base) & ~Q.zero(base) & Q.ne(base, 1)
         & Q.algebraic(exponent) & ~Q.rational(exponent))
        >> Q.transcendental(f(base, exponent))),

    # A complex power of a nonzero complex number is complex
    #     0**-1 is zoo and 0**I is nan
    for_all((Pow,),
        (Q.complex(base) & ~Q.zero(base) & Q.complex(exponent))
        >> Q.complex(f(base, exponent)),
        (Q.complex(base) & Q.integer(exponent) & ~Q.negative(exponent))
        >> Q.complex(f(base, exponent)),
        (Q.complex(base) & Q.positive(exponent)) >> Q.complex(f(base, exponent))),

    # A real power of a positive number is real
    for_all((Pow,),
        (Q.positive(base) & Q.real(exponent)) >> Q.real(f(base, exponent))),

    # A nonnegative real power of zero is real
    #     0**-1 is zoo
    for_all((Pow,),
        (Q.zero(base) & Q.real(exponent) & Q.nonnegative(exponent))
        >> Q.real(f(base, exponent))),

    # Zero to a negative power is zoo
    for_all((Pow,),
        (Q.zero(base) & Q.negative(exponent))
        >> (~Q.complex(f(base, exponent)) & ~Q.extended_real(f(base, exponent)))),

    # An integer power of an extended real number is extended real
    #     0**-1 is zoo
    for_all((Pow,),
        (Q.extended_real(base) & ~Q.zero(base) & Q.integer(exponent))
        >> Q.extended_real(f(base, exponent)),
        (Q.extended_real(base) & Q.integer(exponent) & ~Q.negative(exponent))
        >> Q.extended_real(f(base, exponent))),

    # An even power of an imaginary number is real, an odd power imaginary
    #     I**2 is -1
    for_all((Pow,),
        (Q.imaginary(base) & Q.even(exponent)) >> Q.real(f(base, exponent)),
        (Q.imaginary(base) & Q.odd(exponent)) >> Q.imaginary(f(base, exponent))),

    # An even power of an antihermitian number is hermitian, an odd power
    # antihermitian
    #     0**-1 is zoo
    for_all((Pow,),
        (Q.antihermitian(base) & ~Q.zero(base) & Q.even(exponent))
        >> Q.hermitian(f(base, exponent)),
        (Q.antihermitian(base) & Q.even(exponent) & ~Q.negative(exponent))
        >> Q.hermitian(f(base, exponent)),
        (Q.antihermitian(base) & ~Q.zero(base) & Q.odd(exponent))
        >> Q.antihermitian(f(base, exponent)),
        (Q.antihermitian(base) & Q.odd(exponent) & ~Q.negative(exponent))
        >> Q.antihermitian(f(base, exponent))),

    # A real number to an integer or an irrational power is not imaginary
    #     (-1)**r is imaginary only for r an odd integer over 2
    for_all((Pow,),
        (Q.real(base) & Q.integer(exponent)) >> ~Q.imaginary(f(base, exponent)),
        (Q.real(base) & Q.irrational(exponent)) >> ~Q.imaginary(f(base, exponent))),

    # A negative number to a power which is a rational number but not an
    # integer is not real
    #     (-1)**(1/2) is I
    for_all((Pow,),
        (Q.negative(base) & Q.rational(exponent) & ~Q.integer(exponent))
        >> ~Q.real(f(base, exponent))),

    # A negative number to the power 1/2, -1/2, 3/2 or -3/2 is imaginary
    #     sqrt(-a) is I*sqrt(a); a row cannot say "half of an odd integer",
    #     so other such exponents are not covered
    for_all((Pow,),
        (Q.negative(base) & Q.eq(exponent, S.Half))
        >> Q.imaginary(f(base, exponent)),
        (Q.negative(base) & Q.eq(exponent, -S.Half))
        >> Q.imaginary(f(base, exponent)),
        (Q.negative(base) & Q.eq(exponent, Rational(3, 2)))
        >> Q.imaginary(f(base, exponent)),
        (Q.negative(base) & Q.eq(exponent, Rational(-3, 2)))
        >> Q.imaginary(f(base, exponent))),

    # A prime to a power which is a rational number but not an integer is
    # irrational
    #     the root of a prime is irrational
    for_all((Pow,),
        (Q.prime(base) & Q.rational(exponent) & ~Q.integer(exponent))
        >> Q.irrational(f(base, exponent))),

    # A nonzero integer power of a transcendental number is transcendental
    #     its inverse and its powers are transcendental
    for_all((Pow,),
        (Q.transcendental(base) & Q.integer(exponent) & ~Q.zero(exponent))
        >> Q.transcendental(f(base, exponent))),

    # A positive integer power of a number which is not algebraic is not
    # algebraic
    #     oo**-1 is zero
    for_all((Pow,),
        (~Q.algebraic(base) & Q.integer(exponent) & Q.positive(exponent))
        >> ~Q.algebraic(f(base, exponent))),

    # --- exp ---

    # Real on the reals, complex on the complex numbers
    for_all((exp,),
        closed(f(x), Q.real, Q.complex)),

    # One at zero
    for_all((exp,),
        Q.zero(x) >> Q.integer(f(x))),

    # Lindemann
    #     exp(a) is transcendental for an algebraic a which is not zero
    for_all((exp,),
        (Q.algebraic(x) & ~Q.zero(x)) >> Q.transcendental(f(x))),

    # --- log ---

    # Real exactly on the positive numbers
    #     log(-1) is I*pi, log(0) is zoo and log(oo) is oo
    for_all((log,),
        Equivalent(Q.real(f(x)), Q.positive(x))),

    # Complex on the nonzero complex numbers
    #     log(0) is zoo
    for_all((log,),
        (Q.complex(x) & ~Q.zero(x)) >> Q.complex(f(x))),

    # The logarithm of a finite number which is not positive is not extended
    # real
    #     log(0) is zoo and log(-1) is I*pi; log(-oo) is oo
    for_all((log,),
        (Q.finite(x) & ~Q.positive(x)) >> ~Q.extended_real(f(x))),

    # log of an algebraic number other than 0 and 1 is transcendental
    #     Lindemann: exp(b) is transcendental for an algebraic b other
    #     than 0, and log is 0 only at 1
    for_all((log,),
        (Q.algebraic(x) & ~Q.zero(x) & Q.ne(x, 1)) >> Q.transcendental(f(x)),
        (Q.algebraic(x) & ~Q.zero(x) & ~Q.positive(x))
        >> Q.transcendental(f(x))),

    # log of an algebraic number other than 1 is not algebraic
    #     log(0) is zoo
    for_all((log,),
        (Q.algebraic(x) & Q.ne(x, 1)) >> ~Q.algebraic(f(x))),

    # log of an algebraic number which is not positive is not algebraic
    #     such a number is not 1
    for_all((log,),
        (Q.algebraic(x) & ~Q.positive(x)) >> ~Q.algebraic(f(x))),

    # --- acos ---

    # acos of an algebraic number other than 1 is transcendental
    #     it is not zero, and the cosine of an algebraic number other than
    #     zero is transcendental (Lindemann-Weierstrass)
    for_all((acos,),
        (Q.algebraic(x) & Q.ne(x, 1)) >> Q.transcendental(f(x)),
        (Q.algebraic(x) & ~Q.positive(x)) >> Q.transcendental(f(x))),

    # --- sin, cos, tan, cot ---

    # Real on the reals, complex on the complex numbers
    for_all((sin, cos),
        closed(f(x), Q.real, Q.complex)),

    # Zero at zero
    for_all((sin, tan),
        Q.zero(x) >> Q.zero(f(x))),

    # One at zero
    for_all((cos,),
        Q.zero(x) >> Q.integer(f(x))),

    # Lindemann
    #     the value at an algebraic a which is not zero is a rational
    #     function of exp(I*a), which is transcendental
    for_all((sin, cos, tan),
        (Q.algebraic(x) & ~Q.zero(x)) >> Q.transcendental(f(x))),

    # Not algebraic at an algebraic number
    #     cot(0) is zoo
    for_all((cot,),
        Q.algebraic(x) >> ~Q.algebraic(f(x))),

    # --- asin, atan, acot ---

    # Zero at zero
    for_all((asin, atan),
        Q.zero(x) >> Q.zero(f(x))),

    # Lindemann
    #     an algebraic value at an algebraic number other than zero would
    #     make the sine or the tangent of an algebraic number algebraic
    for_all((asin,),
        (Q.algebraic(x) & ~Q.zero(x)) >> Q.transcendental(f(x))),

    # Not algebraic at an algebraic number other than zero
    #     an algebraic value would make the tangent of an algebraic number
    #     algebraic, and atan(I) is oo*I
    for_all((atan,),
        (Q.algebraic(x) & ~Q.zero(x)) >> ~Q.algebraic(f(x))),

    # Not algebraic at an algebraic number
    #     acot(0) is pi/2
    for_all((acot,),
        Q.algebraic(x) >> ~Q.algebraic(f(x))),

    # Transcendental at an algebraic number other than zero, away from the
    # poles
    #     atan(I) is oo*I
    for_all((atan,),
        (Q.algebraic(x) & ~Q.zero(x) & ~Q.imaginary(x)) >> Q.transcendental(f(x))),

    # Transcendental at an algebraic number, away from the poles
    #     acot(I) is -oo*I
    for_all((acot,),
        (Q.algebraic(x) & ~Q.imaginary(x)) >> Q.transcendental(f(x))),

    # --- sign ---

    # A sign is a complex number
    #     it is 0 or x/Abs(x)
    for_all((sign,),
        Q.complex(f(x))),

    # --- Determinant, Trace ---

    # A matrix of integers, of reals or of complex numbers has a determinant
    # and a trace of the same kind
    #     they are sums of products of the elements
    for_all((Determinant, Trace),
        Q.integer_elements(x) >> Q.integer(f(x)),
        Q.real_elements(x) >> Q.real(f(x)),
        Q.complex_elements(x) >> Q.complex(f(x))),

    # --- MatrixElement ---

    # An entry of a matrix of integers, of reals or of complex numbers is an
    # integer, a real or a complex number
    for_all((MatrixElement,),
        Q.integer_elements(x) >> Q.integer(f(x, i, j)),
        Q.real_elements(x) >> Q.real(f(x, i, j)),
        Q.complex_elements(x) >> Q.complex(f(x, i, j))),
)
