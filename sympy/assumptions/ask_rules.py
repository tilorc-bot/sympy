"""The rules which answer a predicate about an expression from its arguments."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.ask import Q
from sympy.assumptions.rule_engine import (ALL_ARGS_ARE, ALL_ARGS_ARE_NOT,
    ALWAYS_FALSE, ALWAYS_TRUE, ANY_ARG_IS, EVEN_NUMBER_OF_ARGS_ARE,
    FALSE_IF, FIRST_ARG_IS, FIRST_ARG_IS_NOT, IF_AND_ONLY_IF, ODD_NUMBER_OF_ARGS_ARE,
    ONE_ARG_IS, ONE_ARG_IS_NOT, OTHER_ARGS_ARE, OTHER_ARGS_ARE_NOT, SECOND_ARG_IS,
    SECOND_ARG_IS_NOT, SELF_IS, SELF_IS_NOT, SOME_EVEN_NUMBER_OF_ARGS_ARE,
    SOME_ODD_NUMBER_OF_ARGS_ARE, TRUE_IF)
from sympy.core.add import Add
from sympy.core.expr import Expr
from sympy.core.function import DefinedFunction
from sympy.core.mod import Mod
from sympy.core.mul import Mul
from sympy.core.numbers import I
from sympy.core.numbers import NaN
from sympy.core.power import Pow
from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.functions.combinatorial.factorials import FallingFactorial
from sympy.functions.combinatorial.factorials import RisingFactorial
from sympy.functions.combinatorial.factorials import binomial
from sympy.functions.combinatorial.factorials import factorial
from sympy.functions.combinatorial.factorials import factorial2
from sympy.functions.combinatorial.factorials import subfactorial
from sympy.functions.combinatorial.numbers import andre
from sympy.functions.combinatorial.numbers import catalan
from sympy.functions.combinatorial.numbers import genocchi
from sympy.functions.combinatorial.numbers import jacobi_symbol
from sympy.functions.combinatorial.numbers import kronecker_symbol
from sympy.functions.combinatorial.numbers import legendre_symbol
from sympy.functions.combinatorial.numbers import mobius
from sympy.functions.combinatorial.numbers import partition
from sympy.functions.combinatorial.numbers import primenu
from sympy.functions.combinatorial.numbers import primeomega
from sympy.functions.combinatorial.numbers import primepi
from sympy.functions.combinatorial.numbers import reduced_totient
from sympy.functions.combinatorial.numbers import totient
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.complexes import adjoint
from sympy.functions.elementary.complexes import conjugate
from sympy.functions.elementary.complexes import im
from sympy.functions.elementary.complexes import re
from sympy.functions.elementary.complexes import sign
from sympy.functions.elementary.complexes import transpose
from sympy.functions.elementary.exponential import LambertW
from sympy.functions.elementary.exponential import exp
from sympy.functions.elementary.exponential import exp_polar
from sympy.functions.elementary.exponential import log
from sympy.functions.elementary.hyperbolic import acosh
from sympy.functions.elementary.hyperbolic import acsch
from sympy.functions.elementary.hyperbolic import asech
from sympy.functions.elementary.hyperbolic import asinh
from sympy.functions.elementary.hyperbolic import atanh
from sympy.functions.elementary.hyperbolic import cosh
from sympy.functions.elementary.hyperbolic import coth
from sympy.functions.elementary.hyperbolic import csch
from sympy.functions.elementary.hyperbolic import sech
from sympy.functions.elementary.hyperbolic import sinh
from sympy.functions.elementary.hyperbolic import tanh
from sympy.functions.elementary.integers import ceiling
from sympy.functions.elementary.integers import floor
from sympy.functions.elementary.integers import frac
from sympy.functions.elementary.miscellaneous import Max
from sympy.functions.elementary.miscellaneous import Min
from sympy.functions.elementary.trigonometric import acos
from sympy.functions.elementary.trigonometric import acot
from sympy.functions.elementary.trigonometric import asec
from sympy.functions.elementary.trigonometric import asin
from sympy.functions.elementary.trigonometric import atan
from sympy.functions.elementary.trigonometric import cos
from sympy.functions.elementary.trigonometric import cot
from sympy.functions.elementary.trigonometric import csc
from sympy.functions.elementary.trigonometric import sec
from sympy.functions.elementary.trigonometric import sin
from sympy.functions.elementary.trigonometric import sinc
from sympy.functions.elementary.trigonometric import tan
from sympy.functions.special.bessel import airyai
from sympy.functions.special.bessel import besseli
from sympy.functions.special.bessel import besselj
from sympy.functions.special.bessel import besselk
from sympy.functions.special.bessel import bessely
from sympy.functions.special.error_functions import erf
from sympy.functions.special.error_functions import erf2
from sympy.functions.special.error_functions import erfc
from sympy.functions.special.error_functions import erfcinv
from sympy.functions.special.error_functions import erfi
from sympy.functions.special.error_functions import fresnelc
from sympy.functions.special.error_functions import fresnels
from sympy.functions.special.error_functions import owens_t
from sympy.functions.special.gamma_functions import gamma
from sympy.functions.special.gamma_functions import loggamma
from sympy.functions.special.gamma_functions import polygamma
from sympy.functions.special.tensor_functions import KroneckerDelta
from sympy.integrals.integrals import Integral

if TYPE_CHECKING:
    from sympy.assumptions.rule_engine import Rules

THIRD_ARG_IS = (2, True)
THIRD_ARG_IS_NOT = (2, False)


RULES: Rules = {
    (Abs, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (Abs, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.even)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.even), (FIRST_ARG_IS, Q.real)]),
    ],
    (Abs, Q.extended_nonnegative): [
        ALWAYS_TRUE,
    ],
    (Abs, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (Abs, Q.irrational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.irrational)]),
    ],
    (Abs, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (Abs, Q.odd): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.odd), (FIRST_ARG_IS, Q.real)]),
    ],
    (Abs, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (Abs, Q.positive_infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite)]),
    ],
    (Abs, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.rational)]),
    ],
    (Abs, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (Abs, Q.zero): [
        (IF_AND_ONLY_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (Add, Q.algebraic): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic)]),
    ],
    (Add, Q.antihermitian): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.antihermitian)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.antihermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.nonzero), (OTHER_ARGS_ARE, Q.imaginary)]),
    ],
    (Add, Q.commutative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.commutative)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
    ],
    (Add, Q.complex): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
    ],
    (Add, Q.even): [
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
    ],
    (Add, Q.extended_negative): [
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_nonpositive),
            (ANY_ARG_IS, Q.extended_negative),
        ]),
        (FALSE_IF, [(ONE_ARG_IS, Q.positive_infinite), (OTHER_ARGS_ARE, Q.finite)]),
    ],
    (Add, Q.extended_nonnegative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_nonnegative)]),
    ],
    (Add, Q.extended_nonpositive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_nonpositive)]),
    ],
    (Add, Q.extended_positive): [
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_nonnegative),
            (ANY_ARG_IS, Q.extended_positive),
        ]),
        (FALSE_IF, [(ONE_ARG_IS, Q.negative_infinite), (OTHER_ARGS_ARE, Q.finite)]),
    ],
    (Add, Q.extended_real): [
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
        ]),
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_real), (ONE_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
    ],
    (Add, Q.finite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
    ],
    (Add, Q.hermitian): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
    ],
    (Add, Q.infinite): [
        (TRUE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
    ],
    (Add, Q.integer): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.integer)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.integer)]),
    ],
    (Add, Q.irrational): [
        (TRUE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
    ],
    (Add, Q.negative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonpositive), (ANY_ARG_IS, Q.negative)]),
    ],
    (Add, Q.negative_infinite): [
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
        ]),
    ],
    (Add, Q.nonnegative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonnegative)]),
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.integer),
            (ONE_ARG_IS, S.NegativeOne),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
    ],
    (Add, Q.nonpositive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonpositive)]),
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.integer),
            (ONE_ARG_IS, S.One),
            (OTHER_ARGS_ARE, Q.negative),
        ]),
    ],
    (Add, Q.odd): [
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
    ],
    (Add, Q.positive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonnegative), (ANY_ARG_IS, Q.positive)]),
    ],
    (Add, Q.positive_infinite): [
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
        ]),
    ],
    (Add, Q.rational): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational)]),
    ],
    (Add, Q.real): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
    ],
    (Add, Q.transcendental): [
        (TRUE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
    ],
    (Add, Q.zero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.zero)]),
    ],
    (Add, S.NegativeOne): [
        (FALSE_IF, [(ALL_ARGS_ARE, Q.negative), (ANY_ARG_IS, S.NegativeOne)]),
    ],
    (Add, S.One): [
        (TRUE_IF, [(ONE_ARG_IS, S.One), (OTHER_ARGS_ARE, Q.zero)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.positive), (ANY_ARG_IS, S.One)]),
    ],
    (DefinedFunction, Q.commutative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.commutative)]),
    ],
    (Expr, S.NegativeOne): [
        (FALSE_IF, [(SELF_IS_NOT, Q.negative)]),
        (FALSE_IF, [(SELF_IS_NOT, Q.odd)]),
    ],
    (Expr, S.Half): [
        (FALSE_IF, [(SELF_IS, Q.integer)]),
    ],
    (Expr, S.One): [
        (FALSE_IF, [(SELF_IS_NOT, Q.positive)]),
        (FALSE_IF, [(SELF_IS_NOT, Q.odd)]),
        (FALSE_IF, [(SELF_IS, Q.prime)]),
        (FALSE_IF, [(SELF_IS, Q.composite)]),
    ],
    (Expr, I): [
        (FALSE_IF, [(SELF_IS_NOT, Q.imaginary)]),
    ],
    (FallingFactorial, Q.integer): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (Integral, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (KroneckerDelta, Q.integer): [
        ALWAYS_TRUE,
    ],
    (LambertW, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (LambertW, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (Max, Q.algebraic): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.algebraic), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.algebraic), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.complex): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.complex), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.complex), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.composite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.composite)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.composite), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.even): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.even), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.extended_negative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_negative)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.extended_negative),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.extended_nonnegative): [
        (TRUE_IF, [
            (ANY_ARG_IS, Q.extended_nonnegative),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.extended_nonnegative),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.extended_nonpositive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_nonpositive)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.extended_nonpositive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.extended_positive): [
        (TRUE_IF, [(ANY_ARG_IS, Q.extended_positive), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.extended_positive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.extended_real): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.finite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.finite), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.infinite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.infinite), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.infinite), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.integer): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.integer)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.integer), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.irrational): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.irrational)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.irrational), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.negative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.negative)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.negative), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.negative_infinite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.negative_infinite)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.nonnegative): [
        (TRUE_IF, [
            (ANY_ARG_IS, Q.nonnegative),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.nonnegative),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.nonpositive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonpositive)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.nonpositive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.nonzero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonzero)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.nonzero), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.odd): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.odd)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.odd), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.positive): [
        (TRUE_IF, [
            (ANY_ARG_IS, Q.positive),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.positive), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.positive_infinite): [
        (TRUE_IF, [(ANY_ARG_IS, Q.positive_infinite), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.prime): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.prime)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.prime), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.rational): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.rational), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.real): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.real), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.transcendental): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.transcendental), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.transcendental),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.zero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.zero)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.zero), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.algebraic): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.algebraic), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.algebraic), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.complex): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.complex), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.complex), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.composite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.composite)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.composite), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.even): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.even), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.extended_negative): [
        (TRUE_IF, [(ANY_ARG_IS, Q.extended_negative), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.extended_negative),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.extended_nonnegative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_nonnegative)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.extended_nonnegative),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.extended_nonpositive): [
        (TRUE_IF, [
            (ANY_ARG_IS, Q.extended_nonpositive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.extended_nonpositive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.extended_positive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_positive)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.extended_positive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.extended_real): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.finite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.finite), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.infinite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.infinite), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.infinite), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.integer): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.integer)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.integer), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.irrational): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.irrational)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.irrational), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.negative): [
        (TRUE_IF, [
            (ANY_ARG_IS, Q.negative),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.negative), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.negative_infinite): [
        (TRUE_IF, [(ANY_ARG_IS, Q.negative_infinite), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.nonnegative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonnegative)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.nonnegative),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.nonpositive): [
        (TRUE_IF, [
            (ANY_ARG_IS, Q.nonpositive),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.nonpositive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.nonzero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonzero)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.nonzero), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.odd): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.odd)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.odd), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.positive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.positive)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.positive), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.positive_infinite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.positive_infinite)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.prime): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.prime)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.prime), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.rational): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.rational), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.real): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.real), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.transcendental): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.transcendental), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.transcendental),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.zero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.zero)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.zero), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Mod, Q.integer): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
    ],
    (Mod, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Mod, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mul, Q.algebraic): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic), (OTHER_ARGS_ARE_NOT, Q.zero)]),
    ],
    (Mul, Q.antihermitian): [
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.antihermitian),
            (OTHER_ARGS_ARE, Q.hermitian),
            (ALL_ARGS_ARE, Q.commutative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.antihermitian),
            (OTHER_ARGS_ARE, Q.hermitian),
            (ONE_ARG_IS_NOT, Q.commutative),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
    ],
    (Mul, Q.commutative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.commutative)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
    ],
    (Mul, Q.complex): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
    ],
    (Mul, Q.composite): [
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.integer),
            (ALL_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.composite),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.integer),
            (ALL_ARGS_ARE, Q.positive),
            (ALL_ARGS_ARE_NOT, S.One),
        ]),
    ],
    (Mul, Q.even): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.integer), (ANY_ARG_IS, Q.even)]),
    ],
    (Mul, Q.extended_negative): [
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
    ],
    (Mul, Q.extended_nonzero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero)]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
    ],
    (Mul, Q.extended_positive): [
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
    ],
    (Mul, Q.extended_real): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_real), (ONE_ARG_IS_NOT, Q.nonzero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
    ],
    (Mul, Q.finite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
    ],
    (Mul, Q.hermitian): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.hermitian), (ALL_ARGS_ARE, Q.commutative)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.hermitian), (ONE_ARG_IS_NOT, Q.commutative)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.antihermitian),
            (OTHER_ARGS_ARE, Q.hermitian),
            (ALL_ARGS_ARE, Q.commutative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.antihermitian),
            (OTHER_ARGS_ARE, Q.hermitian),
            (ONE_ARG_IS_NOT, Q.commutative),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
    ],
    (Mul, Q.imaginary): [
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.nonzero)]),
    ],
    (Mul, Q.infinite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (TRUE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
    ],
    (Mul, Q.integer): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.integer)]),
        (FALSE_IF, [(ONE_ARG_IS, S.Half), (OTHER_ARGS_ARE, Q.odd)]),
        (TRUE_IF, [
            (ONE_ARG_IS, S.Half),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.even),
        ]),
    ],
    (Mul, Q.irrational): [
        (TRUE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
    ],
    (Mul, Q.negative): [
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.negative), (OTHER_ARGS_ARE, Q.positive)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.negative),
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
        ]),
    ],
    (Mul, Q.nonnegative): [
        (TRUE_IF, [
            (SOME_EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
    ],
    (Mul, Q.nonpositive): [
        (TRUE_IF, [
            (SOME_ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
    ],
    (Mul, Q.nonzero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonzero)]),
    ],
    (Mul, Q.odd): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.odd)]),
    ],
    (Mul, Q.positive): [
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.positive)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.negative),
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
        ]),
    ],
    (Mul, Q.prime): [
        (FALSE_IF, [(ALL_ARGS_ARE, Q.integer), (ANY_ARG_IS, Q.composite)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.prime),
        ]),
    ],
    (Mul, Q.rational): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational), (OTHER_ARGS_ARE_NOT, Q.zero)]),
    ],
    (Mul, Q.real): [
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
    ],
    (Mul, Q.transcendental): [
        (TRUE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
    ],
    (Mul, Q.zero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.zero)]),
    ],
    (NaN, Q.commutative): [
        ALWAYS_TRUE,
    ],
    (Pow, Q.algebraic): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (SECOND_ARG_IS_NOT, Q.negative),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS_NOT, Q.algebraic),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (Pow, Q.antihermitian): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.antihermitian),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.odd),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.antihermitian),
            (SECOND_ARG_IS_NOT, Q.negative),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (Pow, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.commutative), (SECOND_ARG_IS, Q.commutative)]),
    ],
    (Pow, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex), (SECOND_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.complex),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.complex),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.composite): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS, Q.positive),
            (FIRST_ARG_IS_NOT, S.One),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
            (SECOND_ARG_IS_NOT, S.One),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS, Q.negative),
            (FIRST_ARG_IS_NOT, S.NegativeOne),
            (SECOND_ARG_IS, Q.even),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (Pow, Q.even): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.even),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, I), (SECOND_ARG_IS, Q.integer)]),
    ],
    (Pow, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.even)]),
    ],
    (Pow, Q.extended_nonnegative): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.extended_nonnegative),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.extended_real),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.even),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive), (SECOND_ARG_IS, Q.real)]),
    ],
    (Pow, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS_NOT, Q.zero)]),
    ],
    (Pow, Q.extended_real): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.extended_real),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.extended_real),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
    ],
    (Pow, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite), (SECOND_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.finite),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.finite),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Pow, Q.hermitian): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.antihermitian),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.even),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.antihermitian),
            (SECOND_ARG_IS, Q.even),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.hermitian),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.hermitian),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
    ],
    (Pow, Q.imaginary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.integer)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.irrational)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
    ],
    (Pow, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
    ],
    (Pow, Q.integer): [
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS_NOT, S.One),
            (FIRST_ARG_IS_NOT, S.NegativeOne),
            (SECOND_ARG_IS, Q.negative),
        ]),
    ],
    (Pow, Q.irrational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.prime),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
    ],
    (Pow, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative), (SECOND_ARG_IS, Q.odd)]),
    ],
    (Pow, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (SECOND_ARG_IS, Q.finite)]),
    ],
    (Pow, Q.nonnegative): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.odd),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.real),
            (SECOND_ARG_IS, Q.even),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative), (SECOND_ARG_IS, Q.nonnegative)]),
    ],
    (Pow, Q.nonpositive): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.nonpositive),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (Pow, Q.odd): [
        (TRUE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
    ],
    (Pow, Q.positive): [
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, I)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
    ],
    (Pow, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (SECOND_ARG_IS, Q.finite)]),
    ],
    (Pow, Q.prime): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.prime),
            (SECOND_ARG_IS_NOT, Q.composite),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
            (SECOND_ARG_IS_NOT, Q.prime),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.composite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.prime)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS_NOT, Q.prime),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.positive),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, S.One),
        ]),
    ],
    (Pow, Q.rational): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.rational),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.rational),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
    ],
    (Pow, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.real),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.real),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.zero),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.real),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
    ],
    (Pow, Q.transcendental): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.transcendental),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.zero),
            (FIRST_ARG_IS_NOT, S.One),
            (SECOND_ARG_IS, Q.algebraic),
            (SECOND_ARG_IS_NOT, Q.rational),
        ]),
    ],
    (Pow, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.zero), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.finite),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.finite),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.finite),
            (SECOND_ARG_IS_NOT, Q.positive),
            (SECOND_ARG_IS, Q.real),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_nonpositive)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.zero), (SECOND_ARG_IS, Q.nonnegative)]),
    ],
    (RisingFactorial, Q.integer): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (Symbol, Q.commutative): [
        ALWAYS_TRUE,
    ],
    (acos, Q.negative): [
        ALWAYS_FALSE,
    ],
    (acos, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acosh, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (acosh, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite)]),
    ],
    (acot, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (acot, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
    ],
    (acot, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (acot, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (acot, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
    ],
    (acot, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (acot, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (acot, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.imaginary)]),
    ],
    (acsch, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real)]),
    ],
    (acsch, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonzero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.extended_real)]),
    ],
    (acsch, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (acsch, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (acsch, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acsch, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (adjoint, Q.commutative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (airyai, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (andre, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (asec, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (asech, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (asech, Q.positive_infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
    ],
    (asin, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
    ],
    (asin, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (asin, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real)]),
    ],
    (asinh, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (asinh, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite)]),
    ],
    (asinh, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (asinh, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (asinh, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (asinh, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (atan, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (atan, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (atan, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
    ],
    (atan, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
    ],
    (atan, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
    ],
    (atan, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonzero)]),
    ],
    (atan, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
    ],
    (atan, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (atan, Q.transcendental): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.imaginary),
            (FIRST_ARG_IS_NOT, Q.zero),
        ]),
    ],
    (atan, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (atanh, Q.imaginary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.imaginary)]),
    ],
    (atanh, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (besseli, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besselj, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besselk, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (bessely, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (binomial, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (binomial, Q.nonnegative): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.negative),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.even)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (catalan, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (ceiling, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (ceiling, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (conjugate, Q.commutative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (cos, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (cos, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (cos, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (cos, Q.negative_infinite): [
        ALWAYS_FALSE,
    ],
    (cos, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (cos, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (cosh, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (cosh, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (cosh, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (FIRST_ARG_IS, Q.infinite)]),
    ],
    (cosh, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (cosh, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (cot, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (cot, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (coth, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real), (FIRST_ARG_IS, Q.infinite)]),
    ],
    (coth, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (coth, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (FIRST_ARG_IS, Q.infinite)]),
    ],
    (coth, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
    ],
    (coth, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
    ],
    (coth, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real), (FIRST_ARG_IS, Q.infinite)]),
    ],
    (coth, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonzero)]),
    ],
    (coth, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (csc, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (csc, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (csc, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (csch, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (csch, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (csch, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real), (FIRST_ARG_IS_NOT, Q.negative)]),
    ],
    (csch, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (csch, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonzero)]),
    ],
    (csch, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (FIRST_ARG_IS, Q.infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (erf, Q.imaginary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erf, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
    ],
    (erf, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (erf, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erf, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (erf2, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erfc, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (erfc, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfcinv, Q.positive_infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.imaginary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfi, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (exp, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (exp, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (exp, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (exp, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (exp, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp, Q.positive_infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
    ],
    (exp, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (exp, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (exp_polar, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (exp_polar, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (factorial, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (factorial2, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.even), (FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.odd)]),
    ],
    (factorial2, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.odd): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.odd), (FIRST_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (factorial2, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (floor, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (floor, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (frac, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (frac, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (fresnelc, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnels, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (gamma, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (gamma, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (gamma, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (genocchi, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (im, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (im, Q.imaginary): [
        ALWAYS_FALSE,
    ],
    (im, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (jacobi_symbol, Q.integer): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (jacobi_symbol, Q.prime): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (kronecker_symbol, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (legendre_symbol, Q.integer): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (legendre_symbol, Q.prime): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (log, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (log, Q.commutative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (log, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (log, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (log, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite)]),
    ],
    (log, Q.negative_infinite): [
        ALWAYS_FALSE,
    ],
    (log, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (log, Q.positive_infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (log, Q.real): [
        (IF_AND_ONLY_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (log, Q.transcendental): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.zero),
            (FIRST_ARG_IS_NOT, S.One),
        ]),
    ],
    (log, Q.zero): [
        (IF_AND_ONLY_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (loggamma, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (mobius, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (owens_t, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (owens_t, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (owens_t, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (partition, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (polygamma, Q.negative): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.even),
            (FIRST_ARG_IS, Q.positive),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (polygamma, Q.positive): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.odd),
            (FIRST_ARG_IS, Q.positive),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.odd),
            (FIRST_ARG_IS, Q.positive),
            (SECOND_ARG_IS, Q.real),
            (SECOND_ARG_IS_NOT, Q.integer),
        ]),
    ],
    (polygamma, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primepi, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (re, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (re, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.even)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.even), (FIRST_ARG_IS, Q.real)]),
    ],
    (re, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (re, Q.imaginary): [
        ALWAYS_FALSE,
    ],
    (re, Q.odd): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.odd)]),
    ],
    (re, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (reduced_totient, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (sec, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sec, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (sech, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (sech, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sech, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sech, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (FIRST_ARG_IS, Q.infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (sign, Q.complex): [
        ALWAYS_TRUE,
    ],
    (sign, Q.finite): [
        ALWAYS_TRUE,
    ],
    (sign, Q.imaginary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (sign, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sign, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
    ],
    (sign, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
    ],
    (sign, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
    ],
    (sign, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonzero)]),
    ],
    (sign, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (sign, Q.zero): [
        (IF_AND_ONLY_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (sin, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (sin, Q.negative_infinite): [
        ALWAYS_FALSE,
    ],
    (sin, Q.positive_infinite): [
        ALWAYS_FALSE,
    ],
    (sin, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sin, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sin, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinc, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinc, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (sinh, Q.extended_negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
    ],
    (sinh, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
    ],
    (sinh, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sinh, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (sinh, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (FIRST_ARG_IS, Q.infinite)]),
    ],
    (sinh, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real), (FIRST_ARG_IS_NOT, Q.negative)]),
    ],
    (sinh, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (sinh, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sinh, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonzero)]),
    ],
    (subfactorial, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.odd), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.odd): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.even), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (tan, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (tan, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (tan, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (tanh, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (FIRST_ARG_IS, Q.infinite)]),
    ],
    (tanh, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
    ],
    (tanh, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
    ],
    (tanh, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (tanh, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (tanh, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonzero)]),
    ],
    (totient, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (transpose, Q.commutative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
}
