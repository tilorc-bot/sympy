"""
Do NOT manually edit this file.
Instead, run ./bin/ask_rules_update.py.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.ask import Q
from sympy.assumptions.rule_engine import (ALL_ARGS_ARE, ALL_ARGS_ARE_NOT, ALWAYS_FALSE,
    ALWAYS_TRUE, ANY_ARG_IS, EVEN_NUMBER_OF_ARGS_ARE, FALSE_IF, FIRST_ARG_IS,
    FIRST_ARG_IS_NOT, ODD_NUMBER_OF_ARGS_ARE, ONE_ARG_IS, ONE_ARG_IS_NOT,
    OTHER_ARGS_ARE, OTHER_ARGS_ARE_NOT, SECOND_ARG_IS, SECOND_ARG_IS_NOT, SELF_IS,
    SELF_IS_NOT, TRUE_IF)
from sympy.core.add import Add
from sympy.core.expr import Expr
from sympy.core.function import DefinedFunction
from sympy.core.mod import Mod
from sympy.core.mul import Mul
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
from sympy.functions.elementary.hyperbolic import asinh
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

if TYPE_CHECKING:
    from sympy.assumptions.rule_engine import Rules


RULES: Rules = {
    (Abs, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
    ],
    (Abs, Q.commutative): [
        ALWAYS_TRUE,
    ],
    (Abs, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
    ],
    (Abs, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (Abs, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.even)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.even), (FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
    ],
    (Abs, Q.extended_negative): [
        ALWAYS_FALSE,
    ],
    (Abs, Q.extended_nonnegative): [
        ALWAYS_TRUE,
    ],
    (Abs, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (Abs, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (Abs, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (Abs, Q.extended_real): [
        ALWAYS_TRUE,
    ],
    (Abs, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
    ],
    (Abs, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (Abs, Q.imaginary): [
        ALWAYS_FALSE,
    ],
    (Abs, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite)]),
    ],
    (Abs, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
    ],
    (Abs, Q.irrational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.irrational)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.rational)]),
    ],
    (Abs, Q.negative): [
        ALWAYS_FALSE,
    ],
    (Abs, Q.negative_infinite): [
        ALWAYS_FALSE,
    ],
    (Abs, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
    ],
    (Abs, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (Abs, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (Abs, Q.odd): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.odd), (FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
    ],
    (Abs, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (Abs, Q.positive_infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (Abs, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (Abs, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.rational)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
    ],
    (Abs, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
    ],
    (Abs, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
    ],
    (Abs, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (Add, S.One): [
        (TRUE_IF, [(ONE_ARG_IS, S.One), (OTHER_ARGS_ARE, Q.zero)]),
    ],
    (Add, Q.algebraic): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
    ],
    (Add, Q.antihermitian): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.antihermitian)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.antihermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.nonzero), (OTHER_ARGS_ARE, Q.imaginary)]),
    ],
    (Add, Q.commutative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.commutative)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (TRUE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (TRUE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (TRUE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
    ],
    (Add, Q.complex): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (TRUE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (TRUE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
    ],
    (Add, Q.composite): [
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonpositive)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.negative_infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.integer)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
    ],
    (Add, Q.even): [
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.integer)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (FALSE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.zero)]),
    ],
    (Add, Q.extended_negative): [
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_nonpositive),
            (ANY_ARG_IS, Q.extended_negative),
        ]),
        (FALSE_IF, [(ONE_ARG_IS, Q.positive_infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonnegative)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
    ],
    (Add, Q.extended_nonnegative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_nonnegative)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_nonpositive),
            (ANY_ARG_IS, Q.extended_negative),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
    ],
    (Add, Q.extended_nonpositive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_nonpositive)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_nonnegative),
            (ANY_ARG_IS, Q.extended_positive),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
    ],
    (Add, Q.extended_nonzero): [
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_nonpositive),
            (ANY_ARG_IS, Q.extended_negative),
        ]),
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_nonnegative),
            (ANY_ARG_IS, Q.extended_positive),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (TRUE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.zero)]),
    ],
    (Add, Q.extended_positive): [
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_nonnegative),
            (ANY_ARG_IS, Q.extended_positive),
        ]),
        (FALSE_IF, [(ONE_ARG_IS, Q.negative_infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonpositive)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (TRUE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
    ],
    (Add, Q.finite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (TRUE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (TRUE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
    ],
    (Add, Q.hermitian): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (TRUE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
    ],
    (Add, Q.imaginary): [
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.antihermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.nonzero), (OTHER_ARGS_ARE, Q.imaginary)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_real), (ONE_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
    ],
    (Add, Q.infinite): [
        (TRUE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (FALSE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (TRUE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
    ],
    (Add, Q.integer): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.integer)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.integer)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
    ],
    (Add, Q.irrational): [
        (TRUE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (FALSE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
    ],
    (Add, Q.negative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonpositive), (ANY_ARG_IS, Q.negative)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.positive_infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonnegative)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.positive_infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
    ],
    (Add, Q.nonnegative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonnegative)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_nonpositive),
            (ANY_ARG_IS, Q.extended_negative),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
    ],
    (Add, Q.nonpositive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonpositive)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_nonnegative),
            (ANY_ARG_IS, Q.extended_positive),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
    ],
    (Add, Q.nonzero): [
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (TRUE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonpositive), (ANY_ARG_IS, Q.negative)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonnegative), (ANY_ARG_IS, Q.positive)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.zero)]),
    ],
    (Add, Q.odd): [
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.integer)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.zero)]),
    ],
    (Add, Q.positive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonnegative), (ANY_ARG_IS, Q.positive)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonpositive)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.negative_infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.negative_infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
    ],
    (Add, Q.prime): [
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonpositive)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.negative_infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.integer)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
    ],
    (Add, Q.rational): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
    ],
    (Add, Q.real): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (TRUE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
    ],
    (Add, Q.transcendental): [
        (TRUE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (FALSE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
    ],
    (Add, Q.zero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.zero)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_nonpositive),
            (ANY_ARG_IS, Q.extended_negative),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_nonnegative),
            (ANY_ARG_IS, Q.extended_positive),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.integer)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ANY_ARG_IS, Q.negative_infinite),
        ]),
        (FALSE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.extended_real),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ANY_ARG_IS, Q.positive_infinite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
    ],
    (DefinedFunction, Q.commutative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.commutative)]),
    ],
    (Expr, S.NegativeOne): [
        (FALSE_IF, [(SELF_IS_NOT, Q.negative)]),
        (FALSE_IF, [(SELF_IS_NOT, Q.odd)]),
    ],
    (Expr, S.One): [
        (FALSE_IF, [(SELF_IS_NOT, Q.positive)]),
        (FALSE_IF, [(SELF_IS_NOT, Q.odd)]),
        (FALSE_IF, [(SELF_IS, Q.prime)]),
        (FALSE_IF, [(SELF_IS, Q.composite)]),
    ],
    (Expr, S.Half): [
        (FALSE_IF, [(SELF_IS, Q.integer)]),
    ],
    (Expr, S.ImaginaryUnit): [
        (FALSE_IF, [(SELF_IS_NOT, Q.imaginary)]),
    ],
    (FallingFactorial, Q.algebraic): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (FallingFactorial, Q.commutative): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (FallingFactorial, Q.complex): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (FallingFactorial, Q.extended_real): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (FallingFactorial, Q.finite): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (FallingFactorial, Q.hermitian): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (FallingFactorial, Q.imaginary): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (FallingFactorial, Q.infinite): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (FallingFactorial, Q.integer): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (FallingFactorial, Q.irrational): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (FallingFactorial, Q.negative_infinite): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (FallingFactorial, Q.positive_infinite): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (FallingFactorial, Q.rational): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (FallingFactorial, Q.real): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (FallingFactorial, Q.transcendental): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (KroneckerDelta, Q.algebraic): [
        ALWAYS_TRUE,
    ],
    (KroneckerDelta, Q.commutative): [
        ALWAYS_TRUE,
    ],
    (KroneckerDelta, Q.complex): [
        ALWAYS_TRUE,
    ],
    (KroneckerDelta, Q.extended_real): [
        ALWAYS_TRUE,
    ],
    (KroneckerDelta, Q.finite): [
        ALWAYS_TRUE,
    ],
    (KroneckerDelta, Q.hermitian): [
        ALWAYS_TRUE,
    ],
    (KroneckerDelta, Q.imaginary): [
        ALWAYS_FALSE,
    ],
    (KroneckerDelta, Q.infinite): [
        ALWAYS_FALSE,
    ],
    (KroneckerDelta, Q.integer): [
        ALWAYS_TRUE,
    ],
    (KroneckerDelta, Q.irrational): [
        ALWAYS_FALSE,
    ],
    (KroneckerDelta, Q.negative_infinite): [
        ALWAYS_FALSE,
    ],
    (KroneckerDelta, Q.positive_infinite): [
        ALWAYS_FALSE,
    ],
    (KroneckerDelta, Q.rational): [
        ALWAYS_TRUE,
    ],
    (KroneckerDelta, Q.real): [
        ALWAYS_TRUE,
    ],
    (KroneckerDelta, Q.transcendental): [
        ALWAYS_FALSE,
    ],
    (LambertW, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (LambertW, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (LambertW, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (LambertW, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (LambertW, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (LambertW, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (LambertW, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (LambertW, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (LambertW, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (LambertW, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (LambertW, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (LambertW, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (LambertW, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
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
        (FALSE_IF, [
            (ANY_ARG_IS, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.commutative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.complex): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.complex), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.complex), (ALL_ARGS_ARE, Q.extended_real)]),
        (TRUE_IF, [
            (ANY_ARG_IS, Q.nonnegative),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.composite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.composite)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.composite), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.even): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.even), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.extended_negative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_negative)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.extended_negative),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.extended_nonnegative),
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
        (TRUE_IF, [(ALL_ARGS_ARE, Q.composite)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.prime)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.zero)]),
    ],
    (Max, Q.extended_nonpositive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_nonpositive)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.extended_nonpositive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.extended_positive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.extended_nonzero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_negative)]),
        (TRUE_IF, [(ANY_ARG_IS, Q.extended_positive), (ALL_ARGS_ARE, Q.extended_real)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonzero)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.zero)]),
    ],
    (Max, Q.extended_positive): [
        (TRUE_IF, [(ANY_ARG_IS, Q.extended_positive), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.extended_positive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.composite)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.prime)]),
    ],
    (Max, Q.extended_real): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.finite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.finite), (ALL_ARGS_ARE, Q.extended_real)]),
        (TRUE_IF, [
            (ANY_ARG_IS, Q.nonnegative),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.hermitian): [
        (TRUE_IF, [
            (ANY_ARG_IS, Q.nonnegative),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.real)]),
    ],
    (Max, Q.imaginary): [
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.infinite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.infinite), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.infinite), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.nonnegative),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (TRUE_IF, [(ANY_ARG_IS, Q.positive_infinite), (ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Max, Q.integer): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.integer)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.integer), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.irrational): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.irrational)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.irrational), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.negative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.negative)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.negative), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.extended_nonnegative),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.negative_infinite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.negative_infinite)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.extended_nonnegative),
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
        (TRUE_IF, [(ALL_ARGS_ARE, Q.composite)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.prime)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.zero)]),
    ],
    (Max, Q.nonpositive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonpositive)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.nonpositive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.extended_positive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.nonzero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonzero)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.nonzero), (ALL_ARGS_ARE, Q.extended_real)]),
        (TRUE_IF, [
            (ANY_ARG_IS, Q.positive),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.odd): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.odd)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.odd), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.positive): [
        (TRUE_IF, [
            (ANY_ARG_IS, Q.positive),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.positive), (ALL_ARGS_ARE, Q.extended_real)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.composite)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.prime)]),
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
        (FALSE_IF, [
            (ANY_ARG_IS, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.rational): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.rational), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.real): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.real), (ALL_ARGS_ARE, Q.extended_real)]),
        (TRUE_IF, [
            (ANY_ARG_IS, Q.nonnegative),
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.transcendental): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.transcendental), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.transcendental),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Max, Q.zero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.zero)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.zero), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.extended_positive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.algebraic): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.algebraic), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.algebraic), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.commutative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.complex): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.complex), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.complex), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (TRUE_IF, [
            (ANY_ARG_IS, Q.nonpositive),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.composite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.composite)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.composite), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.extended_nonpositive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.even): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.even), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
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
        (FALSE_IF, [
            (ANY_ARG_IS, Q.extended_negative),
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
        (TRUE_IF, [(ALL_ARGS_ARE, Q.zero)]),
    ],
    (Min, Q.extended_nonzero): [
        (TRUE_IF, [(ANY_ARG_IS, Q.extended_negative), (ALL_ARGS_ARE, Q.extended_real)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_positive)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonzero)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.zero)]),
    ],
    (Min, Q.extended_positive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_positive)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.extended_positive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.extended_nonpositive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.extended_real): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.finite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.finite), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (TRUE_IF, [
            (ANY_ARG_IS, Q.nonpositive),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.hermitian): [
        (TRUE_IF, [
            (ANY_ARG_IS, Q.nonpositive),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.real)]),
    ],
    (Min, Q.imaginary): [
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_real)]),
    ],
    (Min, Q.infinite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.infinite), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.infinite), (ALL_ARGS_ARE, Q.extended_real)]),
        (TRUE_IF, [(ANY_ARG_IS, Q.negative_infinite), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.nonpositive),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.integer): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.integer)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.integer), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.irrational): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.irrational)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.irrational), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.negative): [
        (TRUE_IF, [
            (ANY_ARG_IS, Q.negative),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.negative), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
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
        (FALSE_IF, [
            (ANY_ARG_IS, Q.extended_negative),
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
        (FALSE_IF, [
            (ANY_ARG_IS, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.zero)]),
    ],
    (Min, Q.nonzero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonzero)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.nonzero), (ALL_ARGS_ARE, Q.extended_real)]),
        (TRUE_IF, [
            (ANY_ARG_IS, Q.negative),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.odd): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.odd)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.odd), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.positive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.positive)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.positive), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.extended_nonpositive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.positive_infinite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.positive_infinite)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.positive_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.extended_nonpositive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.prime): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.prime)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.prime), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.extended_nonpositive),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.rational): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.rational), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.real): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.real)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.real), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (TRUE_IF, [
            (ANY_ARG_IS, Q.nonpositive),
            (ALL_ARGS_ARE_NOT, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.transcendental): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.transcendental), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE_NOT, Q.transcendental),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.negative_infinite),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Min, Q.zero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.zero)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.zero), (ALL_ARGS_ARE, Q.extended_real)]),
        (FALSE_IF, [
            (ANY_ARG_IS, Q.extended_negative),
            (ALL_ARGS_ARE, Q.extended_real),
        ]),
    ],
    (Mod, Q.algebraic): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
    ],
    (Mod, Q.commutative): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.complex): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Mod, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Mod, Q.extended_nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.extended_real): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.finite): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.hermitian): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.imaginary): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.infinite): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.integer): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
    ],
    (Mod, Q.irrational): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
    ],
    (Mod, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Mod, Q.negative_infinite): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Mod, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.positive_infinite): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.rational): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
    ],
    (Mod, Q.real): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Mod, Q.transcendental): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
    ],
    (Mul, Q.algebraic): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, S.Half),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.even),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
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
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.nonzero)]),
    ],
    (Mul, Q.commutative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.commutative)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.nonzero)]),
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
        (TRUE_IF, [
            (ONE_ARG_IS, S.Half),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.even),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.negative), (OTHER_ARGS_ARE, Q.positive)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.real)]),
        (TRUE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
    ],
    (Mul, Q.complex): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.nonzero)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, S.Half),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.even),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.negative), (OTHER_ARGS_ARE, Q.positive)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.real)]),
        (TRUE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS, S.Half), (OTHER_ARGS_ARE, Q.odd)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.positive)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.negative),
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
    ],
    (Mul, Q.even): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.integer), (ANY_ARG_IS, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS, S.Half), (OTHER_ARGS_ARE, Q.odd)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.odd)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
    ],
    (Mul, Q.extended_negative): [
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.integer),
            (ALL_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.composite),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.negative), (OTHER_ARGS_ARE, Q.positive)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
    ],
    (Mul, Q.extended_nonnegative): [
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
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
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
    ],
    (Mul, Q.extended_nonpositive): [
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.integer),
            (ALL_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.composite),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.negative), (OTHER_ARGS_ARE, Q.positive)]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
    ],
    (Mul, Q.extended_nonzero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero)]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.negative), (OTHER_ARGS_ARE, Q.positive)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
    ],
    (Mul, Q.extended_positive): [
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
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
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
    ],
    (Mul, Q.extended_real): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_real), (ONE_ARG_IS_NOT, Q.nonzero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, S.Half),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.even),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.negative), (OTHER_ARGS_ARE, Q.positive)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.rational)]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.real)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
    ],
    (Mul, Q.finite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.nonzero)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, S.Half),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.even),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.negative), (OTHER_ARGS_ARE, Q.positive)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.real)]),
        (TRUE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
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
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, S.Half),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.even),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.negative), (OTHER_ARGS_ARE, Q.positive)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.real)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
    ],
    (Mul, Q.imaginary): [
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.nonzero)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_real), (ONE_ARG_IS_NOT, Q.nonzero)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, S.Half),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.even),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.real)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
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
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, S.Half),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.even),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.real)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
    ],
    (Mul, Q.irrational): [
        (TRUE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, S.Half),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.even),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
    ],
    (Mul, Q.negative): [
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.negative), (OTHER_ARGS_ARE, Q.positive)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.negative),
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.integer),
            (ALL_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.composite),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
    ],
    (Mul, Q.negative_infinite): [
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, S.Half),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.even),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.real)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
    ],
    (Mul, Q.nonnegative): [
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
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
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
    ],
    (Mul, Q.nonpositive): [
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ALL_ARGS_ARE, Q.integer),
            (ALL_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.composite),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.negative), (OTHER_ARGS_ARE, Q.positive)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
    ],
    (Mul, Q.nonzero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonzero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.negative), (OTHER_ARGS_ARE, Q.positive)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
    ],
    (Mul, Q.odd): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.odd)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.integer), (ANY_ARG_IS, Q.even)]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS, S.Half), (OTHER_ARGS_ARE, Q.odd)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
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
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
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
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
    ],
    (Mul, Q.positive_infinite): [
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, S.Half),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.even),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.real)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
    ],
    (Mul, Q.prime): [
        (FALSE_IF, [(ALL_ARGS_ARE, Q.integer), (ANY_ARG_IS, Q.composite)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS, S.Half), (OTHER_ARGS_ARE, Q.odd)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.positive)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.negative),
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
    ],
    (Mul, Q.rational): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, S.Half),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.even),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
    ],
    (Mul, Q.real): [
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.real)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, S.Half),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.even),
        ]),
        (TRUE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.negative), (OTHER_ARGS_ARE, Q.positive)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonzero)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.rational)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
    ],
    (Mul, Q.transcendental): [
        (TRUE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.algebraic)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonzero), (ANY_ARG_IS, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.finite),
            (OTHER_ARGS_ARE, Q.infinite),
            (ALL_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, S.Half),
            (OTHER_ARGS_ARE, Q.integer),
            (ANY_ARG_IS, Q.even),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
    ],
    (Mul, Q.zero): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.finite), (ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [(ALL_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.real),
            (OTHER_ARGS_ARE, Q.nonzero),
            (ALL_ARGS_ARE, Q.finite),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.finite), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.finite),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS, S.Half), (OTHER_ARGS_ARE, Q.odd)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.irrational),
            (OTHER_ARGS_ARE, Q.rational),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.transcendental),
            (OTHER_ARGS_ARE, Q.algebraic),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
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
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.transcendental),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.zero),
            (FIRST_ARG_IS_NOT, S.One),
            (SECOND_ARG_IS, Q.algebraic),
            (SECOND_ARG_IS_NOT, Q.rational),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
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
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
    ],
    (Pow, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.commutative), (SECOND_ARG_IS, Q.commutative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
    ],
    (Pow, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex), (SECOND_ARG_IS, Q.positive)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.complex),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.complex),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.complex),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (SECOND_ARG_IS_NOT, Q.negative),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative), (SECOND_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.composite): [
        (FALSE_IF, [
            (FIRST_ARG_IS_NOT, Q.algebraic),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS_NOT, S.One),
            (FIRST_ARG_IS_NOT, S.NegativeOne),
            (SECOND_ARG_IS, Q.negative),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.prime),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.nonpositive),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.odd),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.prime),
            (SECOND_ARG_IS_NOT, Q.composite),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
            (SECOND_ARG_IS_NOT, Q.prime),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.transcendental),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.zero),
            (FIRST_ARG_IS_NOT, S.One),
            (SECOND_ARG_IS, Q.algebraic),
            (SECOND_ARG_IS_NOT, Q.rational),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.even): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.even),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS_NOT, Q.algebraic),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS_NOT, S.One),
            (FIRST_ARG_IS_NOT, S.NegativeOne),
            (SECOND_ARG_IS, Q.negative),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.prime),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.transcendental),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.zero),
            (FIRST_ARG_IS_NOT, S.One),
            (SECOND_ARG_IS, Q.algebraic),
            (SECOND_ARG_IS_NOT, Q.rational),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.extended_nonnegative),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.real),
            (SECOND_ARG_IS, Q.even),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative), (SECOND_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.extended_nonnegative): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.extended_nonnegative),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.real),
            (SECOND_ARG_IS, Q.even),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative), (SECOND_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.nonpositive),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.odd),
        ]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.nonpositive),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.odd),
        ]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
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
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.extended_nonnegative),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative), (SECOND_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite), (SECOND_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.finite),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.finite),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (SECOND_ARG_IS_NOT, Q.negative),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.complex),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
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
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative), (SECOND_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.imaginary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.integer)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.irrational)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.extended_nonnegative),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.extended_real),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.extended_real),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative), (SECOND_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.even)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (SECOND_ARG_IS_NOT, Q.negative),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.complex),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (SECOND_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.finite),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.finite),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
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
        (FALSE_IF, [
            (FIRST_ARG_IS_NOT, Q.algebraic),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.prime),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.transcendental),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.zero),
            (FIRST_ARG_IS_NOT, S.One),
            (SECOND_ARG_IS, Q.algebraic),
            (SECOND_ARG_IS_NOT, Q.rational),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.irrational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.prime),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.rational),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.rational),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.even)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.extended_nonnegative),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative), (SECOND_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (SECOND_ARG_IS, Q.finite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.extended_nonnegative),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.nonnegative): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.real),
            (SECOND_ARG_IS, Q.even),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative), (SECOND_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.nonpositive): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.nonpositive),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.odd),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.odd): [
        (TRUE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (FALSE_IF, [
            (FIRST_ARG_IS_NOT, Q.algebraic),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.even),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS_NOT, S.One),
            (FIRST_ARG_IS_NOT, S.NegativeOne),
            (SECOND_ARG_IS, Q.negative),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.prime),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.transcendental),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.zero),
            (FIRST_ARG_IS_NOT, S.One),
            (SECOND_ARG_IS, Q.algebraic),
            (SECOND_ARG_IS_NOT, Q.rational),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.positive): [
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.nonpositive),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.odd),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (SECOND_ARG_IS, Q.finite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
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
        (FALSE_IF, [
            (FIRST_ARG_IS_NOT, Q.algebraic),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS_NOT, S.One),
            (FIRST_ARG_IS_NOT, S.NegativeOne),
            (SECOND_ARG_IS, Q.negative),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.prime),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.nonpositive),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.odd),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.transcendental),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.zero),
            (FIRST_ARG_IS_NOT, S.One),
            (SECOND_ARG_IS, Q.algebraic),
            (SECOND_ARG_IS_NOT, Q.rational),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
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
        (FALSE_IF, [
            (FIRST_ARG_IS_NOT, Q.algebraic),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.prime),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.transcendental),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.zero),
            (FIRST_ARG_IS_NOT, S.One),
            (SECOND_ARG_IS, Q.algebraic),
            (SECOND_ARG_IS_NOT, Q.rational),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
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
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative), (SECOND_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
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
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (SECOND_ARG_IS_NOT, Q.negative),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.zero): [
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
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.extended_real), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, S.Half)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational), (SECOND_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.integer), (FIRST_ARG_IS, S.NegativeOne)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One), (SECOND_ARG_IS, Q.complex)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.imaginary), (FIRST_ARG_IS, S.ImaginaryUnit)]),
    ],
    (RisingFactorial, Q.algebraic): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (RisingFactorial, Q.commutative): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (RisingFactorial, Q.complex): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (RisingFactorial, Q.extended_real): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (RisingFactorial, Q.finite): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (RisingFactorial, Q.hermitian): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (RisingFactorial, Q.imaginary): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (RisingFactorial, Q.infinite): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (RisingFactorial, Q.integer): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (RisingFactorial, Q.irrational): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (RisingFactorial, Q.negative_infinite): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (RisingFactorial, Q.positive_infinite): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (RisingFactorial, Q.rational): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (RisingFactorial, Q.real): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (RisingFactorial, Q.transcendental): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
    ],
    (Symbol, Q.commutative): [
        ALWAYS_TRUE,
    ],
    (acos, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acos, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acos, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acos, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acos, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acos, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acos, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acos, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acos, Q.negative): [
        ALWAYS_FALSE,
    ],
    (acos, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acos, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acos, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acos, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acos, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acos, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acos, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
    ],
    (acot, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (acot, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.imaginary)]),
    ],
    (acot, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.imaginary)]),
    ],
    (acot, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
    ],
    (acot, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (acot, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (acot, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (acot, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (acot, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (acot, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (acot, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (acot, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.imaginary)]),
    ],
    (acot, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (acot, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (acot, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.imaginary)]),
    ],
    (acot, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (acot, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (acot, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (acot, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.imaginary)]),
    ],
    (acot, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (acot, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (acot, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (acot, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (acot, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
    ],
    (acot, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.imaginary)]),
    ],
    (acot, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
    ],
    (acot, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (acot, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (acot, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.imaginary)]),
    ],
    (acot, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (adjoint, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.commutative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.complex): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.finite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.real): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (adjoint, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (airyai, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (airyai, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (airyai, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (airyai, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (airyai, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (airyai, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (airyai, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (airyai, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (airyai, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (airyai, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (andre, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (andre, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (asec, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (asec, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (asec, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (asec, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (asec, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (asec, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (asec, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (asec, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (asec, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (asec, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asec, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (asin, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (asin, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.extended_nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
    ],
    (asin, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
    ],
    (asin, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (asin, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asin, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (asinh, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (asinh, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (asinh, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.extended_negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.extended_nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (asinh, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (asinh, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (asinh, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (asinh, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (asinh, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (asinh, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (asinh, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (asinh, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (asinh, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (atan, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.imaginary),
            (FIRST_ARG_IS_NOT, Q.zero),
        ]),
    ],
    (atan, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.imaginary),
            (FIRST_ARG_IS_NOT, Q.zero),
        ]),
    ],
    (atan, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
    ],
    (atan, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
    ],
    (atan, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
    ],
    (atan, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (atan, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonzero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (atan, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (atan, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.imaginary),
            (FIRST_ARG_IS_NOT, Q.zero),
        ]),
    ],
    (atan, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (atan, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (atan, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.imaginary),
            (FIRST_ARG_IS_NOT, Q.zero),
        ]),
    ],
    (atan, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (atan, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.imaginary),
            (FIRST_ARG_IS_NOT, Q.zero),
        ]),
    ],
    (atan, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
    ],
    (atan, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (atan, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonzero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (atan, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.imaginary),
            (FIRST_ARG_IS_NOT, Q.zero),
        ]),
    ],
    (atan, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
    ],
    (atan, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (atan, Q.transcendental): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.imaginary),
            (FIRST_ARG_IS_NOT, Q.zero),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (besseli, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besseli, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besseli, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besseli, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besseli, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besseli, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besseli, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besseli, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besseli, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besseli, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besselj, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besselj, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besselj, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besselj, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besselj, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besselj, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besselj, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besselj, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besselj, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besselj, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.real)]),
    ],
    (besselk, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (besselk, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (besselk, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (besselk, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (besselk, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (besselk, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (besselk, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (besselk, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (besselk, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (besselk, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (bessely, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (bessely, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (bessely, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (bessely, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (bessely, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (bessely, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (bessely, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (bessely, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (bessely, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (bessely, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.positive)]),
    ],
    (binomial, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (binomial, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (binomial, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (binomial, Q.composite): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (binomial, Q.extended_negative): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.negative),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.even)]),
    ],
    (binomial, Q.extended_nonnegative): [
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
    ],
    (binomial, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (binomial, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (binomial, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (binomial, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (binomial, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (binomial, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (binomial, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (binomial, Q.negative): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.negative),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.even)]),
    ],
    (binomial, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
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
    (binomial, Q.positive): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (binomial, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (binomial, Q.prime): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (binomial, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (binomial, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (binomial, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (binomial, Q.zero): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (catalan, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (catalan, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (ceiling, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (ceiling, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (ceiling, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (ceiling, Q.extended_nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (ceiling, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (ceiling, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (ceiling, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (ceiling, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (ceiling, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (ceiling, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (ceiling, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (ceiling, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (ceiling, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (ceiling, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (conjugate, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.commutative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.complex): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.finite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.real): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (conjugate, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (cos, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (cos, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (cos, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (cos, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (cos, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (cos, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (cos, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (cos, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (cos, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (cos, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (cos, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (cos, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (cos, Q.negative_infinite): [
        ALWAYS_FALSE,
    ],
    (cos, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (cos, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (cos, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (cos, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (cos, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (cos, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (cos, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (cosh, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (cosh, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (cosh, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (cosh, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (cosh, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (cosh, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (cosh, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (cosh, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (cosh, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (cosh, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (cosh, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (cosh, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (cosh, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (cosh, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (cosh, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (cosh, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (cosh, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (cosh, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (cosh, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (cosh, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (cosh, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (cot, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (cot, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (cot, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (cot, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (cot, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (cot, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (coth, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
    ],
    (coth, Q.extended_negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.extended_nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
    ],
    (coth, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
    ],
    (coth, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (coth, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (csc, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (csc, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (csc, Q.complex): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (csc, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (csc, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (csc, Q.finite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (csc, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (csc, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (csc, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (csc, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (csc, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (csc, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (csc, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (csc, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (csc, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (csc, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (csc, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (csc, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (csc, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (csc, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (csc, Q.real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (csc, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (csc, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (csch, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (csch, Q.extended_negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.extended_nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (csch, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (csch, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (csch, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (erf, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.antihermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erf, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erf, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erf, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erf, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erf, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erf, Q.imaginary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erf, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erf, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erf, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erf, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erf, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erf, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (erf2, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (erf2, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (erf2, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.extended_nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (erf2, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (erf2, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (erf2, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (erf2, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (erf2, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (erf2, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (erf2, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (erf2, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erf2, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.zero)]),
    ],
    (erfc, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erfc, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erfc, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfc, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfc, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (erfc, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (erfc, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (erfc, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (erfc, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (erfc, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erfc, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erfc, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erfc, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erfc, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erfc, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfc, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfc, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfc, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erfc, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfc, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfc, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfc, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfc, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfc, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (erfc, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfc, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfc, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfc, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfcinv, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.complex): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.finite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.positive_infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfcinv, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.antihermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (erfi, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.imaginary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (erfi, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (exp, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (exp, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (exp, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (exp, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (exp, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (exp, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (exp, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (exp, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.positive_infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
    ],
    (exp, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
    ],
    (exp_polar, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (exp_polar, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (exp_polar, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (exp_polar, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (exp_polar, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp_polar, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (exp_polar, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (factorial, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (factorial, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (factorial, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (factorial, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (factorial, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (factorial, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (factorial, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (factorial, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (factorial, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (factorial, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.even), (FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (factorial2, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.odd): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.odd), (FIRST_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.even), (FIRST_ARG_IS, Q.positive)]),
    ],
    (factorial2, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial2, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (floor, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (floor, Q.extended_negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (floor, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (floor, Q.extended_nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (floor, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (floor, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (floor, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (floor, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (floor, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (floor, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (floor, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (floor, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (floor, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (floor, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (frac, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (frac, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (frac, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (frac, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (frac, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (frac, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (frac, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (frac, Q.extended_nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (frac, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (frac, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (frac, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (frac, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (frac, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (frac, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (frac, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (frac, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (frac, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (frac, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (frac, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (frac, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (frac, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (frac, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (frac, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (frac, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (frac, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (frac, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (frac, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (frac, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (frac, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (frac, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (fresnelc, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnelc, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnelc, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnelc, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnelc, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnelc, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnelc, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnelc, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnelc, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnelc, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnels, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnels, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnels, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnels, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnels, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnels, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnels, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnels, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnels, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (fresnels, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (gamma, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (gamma, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (gamma, Q.complex): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (gamma, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (gamma, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (gamma, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (gamma, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (gamma, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (gamma, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (gamma, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (gamma, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (gamma, Q.finite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (gamma, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (gamma, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (gamma, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (gamma, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (gamma, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (gamma, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (gamma, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (gamma, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (gamma, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (gamma, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (gamma, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (gamma, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (gamma, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
    ],
    (gamma, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (gamma, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (gamma, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (FIRST_ARG_IS_NOT, Q.integer)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (gamma, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (gamma, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonpositive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (genocchi, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.extended_nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (genocchi, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (im, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (im, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (im, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (im, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (im, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (im, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (im, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (im, Q.imaginary): [
        ALWAYS_FALSE,
    ],
    (im, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (im, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (im, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (im, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (im, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (im, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (im, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (im, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (im, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (jacobi_symbol, Q.algebraic): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (jacobi_symbol, Q.commutative): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (jacobi_symbol, Q.complex): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (jacobi_symbol, Q.extended_real): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (jacobi_symbol, Q.finite): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (jacobi_symbol, Q.hermitian): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (jacobi_symbol, Q.imaginary): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (jacobi_symbol, Q.infinite): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (jacobi_symbol, Q.integer): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (jacobi_symbol, Q.irrational): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (jacobi_symbol, Q.negative_infinite): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (jacobi_symbol, Q.positive_infinite): [
        (FALSE_IF, [
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
    (jacobi_symbol, Q.rational): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (jacobi_symbol, Q.real): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (jacobi_symbol, Q.transcendental): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (kronecker_symbol, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (kronecker_symbol, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (SECOND_ARG_IS, Q.integer)]),
    ],
    (legendre_symbol, Q.algebraic): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (legendre_symbol, Q.commutative): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (legendre_symbol, Q.complex): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (legendre_symbol, Q.extended_real): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (legendre_symbol, Q.finite): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (legendre_symbol, Q.hermitian): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (legendre_symbol, Q.imaginary): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (legendre_symbol, Q.infinite): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (legendre_symbol, Q.integer): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (legendre_symbol, Q.irrational): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (legendre_symbol, Q.negative_infinite): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (legendre_symbol, Q.positive_infinite): [
        (FALSE_IF, [
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
    (legendre_symbol, Q.rational): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (legendre_symbol, Q.real): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (legendre_symbol, Q.transcendental): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.prime),
            (SECOND_ARG_IS, Q.odd),
        ]),
    ],
    (log, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.commutative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.finite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.negative_infinite): [
        ALWAYS_FALSE,
    ],
    (log, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.positive_infinite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.transcendental): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.zero),
            (FIRST_ARG_IS_NOT, S.One),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, S.One)]),
    ],
    (log, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, S.One)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, S.One)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (loggamma, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (loggamma, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (loggamma, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (loggamma, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (loggamma, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (loggamma, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (loggamma, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (loggamma, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (loggamma, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (loggamma, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (loggamma, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (loggamma, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (loggamma, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (loggamma, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (loggamma, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (loggamma, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (loggamma, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (loggamma, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (loggamma, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive)]),
    ],
    (loggamma, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (loggamma, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (loggamma, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (loggamma, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonpositive)]),
    ],
    (mobius, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (mobius, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (owens_t, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (owens_t, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (owens_t, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (owens_t, Q.extended_negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (owens_t, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (owens_t, Q.extended_nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (owens_t, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (owens_t, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (owens_t, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (owens_t, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (owens_t, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (owens_t, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (owens_t, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (owens_t, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (owens_t, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (owens_t, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (owens_t, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (owens_t, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (owens_t, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (owens_t, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (owens_t, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
    ],
    (owens_t, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real), (SECOND_ARG_IS, Q.extended_real)]),
    ],
    (owens_t, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.positive)]),
    ],
    (partition, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (partition, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (partition, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (partition, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (partition, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (partition, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (partition, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer)]),
    ],
    (partition, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (polygamma, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.positive)]),
    ],
    (polygamma, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.positive)]),
    ],
    (polygamma, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.positive)]),
    ],
    (polygamma, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.positive)]),
    ],
    (polygamma, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.positive)]),
    ],
    (polygamma, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.positive)]),
    ],
    (polygamma, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.positive)]),
    ],
    (polygamma, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.positive)]),
    ],
    (polygamma, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.positive)]),
    ],
    (polygamma, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primenu, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primeomega, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (primepi, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (primepi, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (re, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (re, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (re, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (re, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.even)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.even), (FIRST_ARG_IS, Q.real)]),
    ],
    (re, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.odd)]),
    ],
    (re, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (re, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (re, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (re, Q.imaginary): [
        ALWAYS_FALSE,
    ],
    (re, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (re, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.odd)]),
    ],
    (re, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.even)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.odd)]),
    ],
    (re, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (re, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.odd)]),
    ],
    (re, Q.odd): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.even)]),
    ],
    (re, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (re, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.odd)]),
    ],
    (re, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (re, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (re, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.even), (FIRST_ARG_IS, Q.real)]),
    ],
    (reduced_totient, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (reduced_totient, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (sec, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sec, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sec, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sec, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sec, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sec, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sec, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sec, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sec, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sec, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sec, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sec, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sec, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sec, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sec, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (sech, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sech, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sech, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sech, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sech, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sech, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sech, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sech, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sech, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sech, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sech, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sech, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sech, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sech, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sech, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sech, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sech, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sech, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sech, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sech, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sech, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sign, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sign, Q.antihermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (sign, Q.commutative): [
        ALWAYS_TRUE,
    ],
    (sign, Q.complex): [
        ALWAYS_TRUE,
    ],
    (sign, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
    ],
    (sign, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sign, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
    ],
    (sign, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
    ],
    (sign, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (sign, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonzero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sign, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (sign, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sign, Q.finite): [
        ALWAYS_TRUE,
    ],
    (sign, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sign, Q.imaginary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sign, Q.infinite): [
        ALWAYS_FALSE,
    ],
    (sign, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (sign, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sign, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
    ],
    (sign, Q.negative_infinite): [
        ALWAYS_FALSE,
    ],
    (sign, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
    ],
    (sign, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (sign, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonzero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sign, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sign, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
    ],
    (sign, Q.positive_infinite): [
        ALWAYS_FALSE,
    ],
    (sign, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonpositive)]),
    ],
    (sign, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sign, Q.real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sign, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sign, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sin, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (sin, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex)]),
    ],
    (sin, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.extended_nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sin, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (sin, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sin, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sin, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (sin, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.negative_infinite): [
        ALWAYS_FALSE,
    ],
    (sin, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.positive_infinite): [
        ALWAYS_FALSE,
    ],
    (sin, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sin, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sin, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (sinc, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (sinc, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (sinc, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinc, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinc, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinc, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinc, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinc, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (sinc, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (sinc, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (sinc, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (sinc, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (sinc, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinc, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (sinc, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinc, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinc, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinc, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinc, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (sinc, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary)]),
    ],
    (sinc, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (sinh, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sinh, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sinh, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (sinh, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sinh, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (sinh, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (sinh, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (sinh, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (sinh, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (sinh, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (sinh, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative)]),
    ],
    (subfactorial, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.odd), (FIRST_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.even), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.even), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.even), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.odd): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.even), (FIRST_ARG_IS, Q.nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.odd), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (subfactorial, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.even), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (tan, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (tanh, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (tanh, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (tanh, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.even): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.extended_negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.extended_nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (tanh, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (tanh, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (tanh, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (tanh, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (tanh, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (tanh, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (tanh, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_real)]),
    ],
    (tanh, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tanh, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
    ],
    (totient, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (totient, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.positive)]),
    ],
    (transpose, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.commutative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.complex): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.finite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.real): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
    (transpose, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.commutative)]),
    ],
}
