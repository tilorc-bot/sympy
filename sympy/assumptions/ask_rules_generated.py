"""
Do NOT manually edit this file.
Instead, run ./bin/ask_rules_update.py.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.ask import Q
from sympy.assumptions.rule_engine import (ALL_ARGS_ARE, ALL_ARGS_ARE_NOT, ALWAYS_FALSE,
    ALWAYS_TRUE, ANY_ARG_IS, ANY_ARG_IS_NOT, EVEN_NUMBER_OF_ARGS_ARE, FALSE_IF,
    FIRST_ARG_IS, FIRST_ARG_IS_NOT, ODD_NUMBER_OF_ARGS_ARE, ONE_ARG_IS, ONE_ARG_IS_NOT,
    OTHER_ARGS_ARE, OTHER_ARGS_ARE_NOT, SECOND_ARG_IS, SECOND_ARG_IS_NOT, SELF_IS,
    SELF_IS_NOT, TRUE_IF)
from sympy.core.add import Add
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.core.mul import Mul
from sympy.core.power import Pow
from sympy.core.symbol import Symbol
from sympy.functions.combinatorial.factorials import factorial
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.complexes import im
from sympy.functions.elementary.complexes import re
from sympy.functions.elementary.complexes import sign
from sympy.functions.elementary.exponential import exp
from sympy.functions.elementary.trigonometric import acos
from sympy.functions.elementary.trigonometric import acot
from sympy.functions.elementary.trigonometric import asin
from sympy.functions.elementary.trigonometric import atan
from sympy.functions.elementary.trigonometric import cos
from sympy.functions.elementary.trigonometric import cot
from sympy.functions.elementary.trigonometric import sin
from sympy.functions.elementary.trigonometric import tan
from sympy.matrices.expressions.blockmatrix import BlockDiagMatrix
from sympy.matrices.expressions.determinant import Determinant
from sympy.matrices.expressions.diagonal import DiagMatrix
from sympy.matrices.expressions.diagonal import DiagonalMatrix
from sympy.matrices.expressions.factorizations import EigenValues
from sympy.matrices.expressions.factorizations import EigenVectors
from sympy.matrices.expressions.factorizations import Factorization
from sympy.matrices.expressions.factorizations import LofLU
from sympy.matrices.expressions.factorizations import QofQR
from sympy.matrices.expressions.factorizations import RofQR
from sympy.matrices.expressions.factorizations import SofSVD
from sympy.matrices.expressions.factorizations import UofLU
from sympy.matrices.expressions.factorizations import UofSVD
from sympy.matrices.expressions.factorizations import VofSVD
from sympy.matrices.expressions.fourier import DFT
from sympy.matrices.expressions.hadamard import HadamardProduct
from sympy.matrices.expressions.inverse import Inverse
from sympy.matrices.expressions.matadd import MatAdd
from sympy.matrices.expressions.matexpr import MatrixElement
from sympy.matrices.expressions.matmul import MatMul
from sympy.matrices.expressions.matpow import MatPow
from sympy.matrices.expressions.slice import MatrixSlice
from sympy.matrices.expressions.special import Identity
from sympy.matrices.expressions.special import ZeroMatrix
from sympy.matrices.expressions.trace import Trace
from sympy.matrices.expressions.transpose import Transpose

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
        (FALSE_IF, [(FIRST_ARG_IS, Q.even)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.irrational)]),
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
    (Add, Q.algebraic): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (TRUE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (TRUE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
    ],
    (Add, Q.composite): [
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonpositive)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.integer)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.integer)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (TRUE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (TRUE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
    ],
    (Add, Q.negative): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonpositive), (ANY_ARG_IS, Q.negative)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.extended_nonnegative)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
    ],
    (Add, Q.nonzero): [
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (TRUE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonpositive), (ANY_ARG_IS, Q.negative)]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonnegative), (ANY_ARG_IS, Q.positive)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.integer)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.extended_real)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.integer)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (TRUE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
    ],
    (Add, Q.transcendental): [
        (TRUE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.commutative), (OTHER_ARGS_ARE, Q.complex)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(EVEN_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.imaginary), (OTHER_ARGS_ARE, Q.hermitian)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.infinite), (OTHER_ARGS_ARE, Q.finite)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.integer)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.irrational), (OTHER_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.odd), (OTHER_ARGS_ARE, Q.even)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(ONE_ARG_IS, Q.transcendental), (OTHER_ARGS_ARE, Q.algebraic)]),
    ],
    (Basic, Q.composite): [
        (TRUE_IF, [(SELF_IS, Q.even), (SELF_IS, Q.positive), (SELF_IS_NOT, Q.prime)]),
        (FALSE_IF, [(SELF_IS_NOT, Q.integer)]),
        (FALSE_IF, [(SELF_IS_NOT, Q.positive)]),
        (FALSE_IF, [(SELF_IS, Q.prime)]),
    ],
    (Basic, Q.odd): [
        (TRUE_IF, [(SELF_IS_NOT, Q.even), (SELF_IS, Q.integer)]),
        (FALSE_IF, [(SELF_IS_NOT, Q.integer)]),
    ],
    (BlockDiagMatrix, Q.complex_elements): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.complex_elements)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.complex_elements)]),
    ],
    (BlockDiagMatrix, Q.fullrank): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.invertible)]),
    ],
    (BlockDiagMatrix, Q.integer_elements): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.integer_elements)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.integer_elements)]),
    ],
    (BlockDiagMatrix, Q.invertible): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.invertible)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.invertible)]),
    ],
    (BlockDiagMatrix, Q.orthogonal): [
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.invertible)]),
    ],
    (BlockDiagMatrix, Q.positive_definite): [
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.invertible)]),
    ],
    (BlockDiagMatrix, Q.real_elements): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.real_elements)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.real_elements)]),
    ],
    (BlockDiagMatrix, Q.singular): [
        (FALSE_IF, [(ALL_ARGS_ARE, Q.invertible)]),
    ],
    (BlockDiagMatrix, Q.square): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.invertible)]),
    ],
    (BlockDiagMatrix, Q.unitary): [
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.invertible)]),
    ],
    (DFT, Q.complex_elements): [
        ALWAYS_TRUE,
    ],
    (DFT, Q.fullrank): [
        ALWAYS_TRUE,
    ],
    (DFT, Q.invertible): [
        ALWAYS_TRUE,
    ],
    (DFT, Q.normal): [
        ALWAYS_TRUE,
    ],
    (DFT, Q.singular): [
        ALWAYS_FALSE,
    ],
    (DFT, Q.square): [
        ALWAYS_TRUE,
    ],
    (DFT, Q.unitary): [
        ALWAYS_TRUE,
    ],
    (Determinant, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (Determinant, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.complex_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
    ],
    (Determinant, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (Determinant, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (Determinant, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (Determinant, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (Determinant, Q.integer_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (Determinant, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (Determinant, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (Determinant, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Determinant, Q.real_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (Determinant, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (Determinant, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (DiagMatrix, Q.diagonal): [
        ALWAYS_TRUE,
    ],
    (DiagMatrix, Q.lower_triangular): [
        ALWAYS_TRUE,
    ],
    (DiagMatrix, Q.normal): [
        ALWAYS_TRUE,
    ],
    (DiagMatrix, Q.square): [
        ALWAYS_TRUE,
    ],
    (DiagMatrix, Q.symmetric): [
        ALWAYS_TRUE,
    ],
    (DiagMatrix, Q.triangular): [
        ALWAYS_TRUE,
    ],
    (DiagMatrix, Q.upper_triangular): [
        ALWAYS_TRUE,
    ],
    (DiagonalMatrix, Q.diagonal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.square)]),
    ],
    (DiagonalMatrix, Q.lower_triangular): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (DiagonalMatrix, Q.normal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (DiagonalMatrix, Q.square): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (DiagonalMatrix, Q.symmetric): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (DiagonalMatrix, Q.triangular): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (DiagonalMatrix, Q.upper_triangular): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (EigenValues, Q.complex_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.symmetric)]),
    ],
    (EigenValues, Q.diagonal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (EigenValues, Q.lower_triangular): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (EigenValues, Q.normal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (EigenValues, Q.real_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.symmetric)]),
    ],
    (EigenValues, Q.square): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (EigenValues, Q.symmetric): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (EigenValues, Q.triangular): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (EigenValues, Q.upper_triangular): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (EigenVectors, Q.complex_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.symmetric)]),
    ],
    (EigenVectors, Q.fullrank): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.symmetric)]),
    ],
    (EigenVectors, Q.invertible): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.symmetric)]),
    ],
    (EigenVectors, Q.normal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.symmetric)]),
    ],
    (EigenVectors, Q.orthogonal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.symmetric)]),
    ],
    (EigenVectors, Q.positive_definite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.symmetric)]),
    ],
    (EigenVectors, Q.real_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.symmetric)]),
    ],
    (EigenVectors, Q.singular): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.symmetric)]),
    ],
    (EigenVectors, Q.square): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.symmetric)]),
    ],
    (EigenVectors, Q.unitary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.symmetric)]),
    ],
    (Expr, Q.antihermitian): [
        (TRUE_IF, [(SELF_IS, Q.imaginary)]),
    ],
    (Expr, Q.diagonal): [
        (TRUE_IF, [(SELF_IS, Q.lower_triangular), (SELF_IS, Q.upper_triangular)]),
    ],
    (Expr, Q.extended_real): [
        (TRUE_IF, [(SELF_IS, Q.extended_negative)]),
        (TRUE_IF, [(SELF_IS, Q.extended_positive)]),
        (TRUE_IF, [(SELF_IS, Q.zero)]),
    ],
    (Expr, Q.hermitian): [
        (TRUE_IF, [(SELF_IS, Q.real)]),
    ],
    (Expr, Q.infinite): [
        (FALSE_IF, [(SELF_IS, Q.finite)]),
    ],
    (Expr, Q.invertible): [
        (TRUE_IF, [(SELF_IS, Q.fullrank), (SELF_IS, Q.square)]),
    ],
    (Expr, Q.irrational): [
        (TRUE_IF, [(SELF_IS_NOT, Q.rational), (SELF_IS, Q.real)]),
    ],
    (Expr, Q.negative_infinite): [
        (TRUE_IF, [(SELF_IS, Q.extended_negative), (SELF_IS_NOT, Q.finite)]),
        (FALSE_IF, [(SELF_IS, Q.finite)]),
    ],
    (Expr, Q.nonzero): [
        (FALSE_IF, [(SELF_IS_NOT, Q.real)]),
    ],
    (Expr, Q.positive_infinite): [
        (TRUE_IF, [(SELF_IS, Q.extended_positive), (SELF_IS_NOT, Q.finite)]),
        (FALSE_IF, [(SELF_IS, Q.finite)]),
    ],
    (Expr, Q.transcendental): [
        (TRUE_IF, [(SELF_IS_NOT, Q.algebraic), (SELF_IS, Q.complex)]),
    ],
    (Expr, Q.zero): [
        (TRUE_IF, [(SELF_IS_NOT, Q.nonzero), (SELF_IS, Q.real)]),
        (FALSE_IF, [(SELF_IS_NOT, Q.real)]),
    ],
    (Factorization, Q.complex_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
    ],
    (HadamardProduct, Q.complex_elements): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.complex_elements)]),
    ],
    (HadamardProduct, Q.integer_elements): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.integer_elements)]),
    ],
    (HadamardProduct, Q.real_elements): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.real_elements)]),
    ],
    (Identity, Q.complex_elements): [
        ALWAYS_TRUE,
    ],
    (Identity, Q.diagonal): [
        ALWAYS_TRUE,
    ],
    (Identity, Q.fullrank): [
        ALWAYS_TRUE,
    ],
    (Identity, Q.integer_elements): [
        ALWAYS_TRUE,
    ],
    (Identity, Q.invertible): [
        ALWAYS_TRUE,
    ],
    (Identity, Q.lower_triangular): [
        ALWAYS_TRUE,
    ],
    (Identity, Q.normal): [
        ALWAYS_TRUE,
    ],
    (Identity, Q.orthogonal): [
        ALWAYS_TRUE,
    ],
    (Identity, Q.positive_definite): [
        ALWAYS_TRUE,
    ],
    (Identity, Q.real_elements): [
        ALWAYS_TRUE,
    ],
    (Identity, Q.singular): [
        ALWAYS_FALSE,
    ],
    (Identity, Q.square): [
        ALWAYS_TRUE,
    ],
    (Identity, Q.symmetric): [
        ALWAYS_TRUE,
    ],
    (Identity, Q.triangular): [
        ALWAYS_TRUE,
    ],
    (Identity, Q.unitary): [
        ALWAYS_TRUE,
    ],
    (Identity, Q.upper_triangular): [
        ALWAYS_TRUE,
    ],
    (Inverse, Q.complex_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
    ],
    (Inverse, Q.diagonal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.diagonal)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.diagonal)]),
    ],
    (Inverse, Q.fullrank): [
        ALWAYS_TRUE,
    ],
    (Inverse, Q.invertible): [
        ALWAYS_TRUE,
    ],
    (Inverse, Q.lower_triangular): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.lower_triangular)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.lower_triangular)]),
    ],
    (Inverse, Q.normal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.diagonal)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.unitary)]),
    ],
    (Inverse, Q.orthogonal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.orthogonal)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.orthogonal)]),
    ],
    (Inverse, Q.positive_definite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive_definite)]),
    ],
    (Inverse, Q.real_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (Inverse, Q.singular): [
        ALWAYS_FALSE,
    ],
    (Inverse, Q.square): [
        ALWAYS_TRUE,
    ],
    (Inverse, Q.symmetric): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.symmetric)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.symmetric)]),
    ],
    (Inverse, Q.triangular): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.lower_triangular)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.upper_triangular)]),
    ],
    (Inverse, Q.unitary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.unitary)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.unitary)]),
    ],
    (Inverse, Q.upper_triangular): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.upper_triangular)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.upper_triangular)]),
    ],
    (LofLU, Q.complex_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (LofLU, Q.lower_triangular): [
        ALWAYS_TRUE,
    ],
    (LofLU, Q.real_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (LofLU, Q.triangular): [
        ALWAYS_TRUE,
    ],
    (MatAdd, Q.complex_elements): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.complex_elements)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex_elements)]),
    ],
    (MatAdd, Q.diagonal): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.diagonal)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.diagonal)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.lower_triangular)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.square)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.symmetric)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.upper_triangular)]),
    ],
    (MatAdd, Q.fullrank): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.positive_definite)]),
    ],
    (MatAdd, Q.integer_elements): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.integer_elements)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.integer_elements)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex_elements)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real_elements)]),
    ],
    (MatAdd, Q.invertible): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.positive_definite)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.square)]),
    ],
    (MatAdd, Q.lower_triangular): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.lower_triangular)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.lower_triangular)]),
    ],
    (MatAdd, Q.normal): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.diagonal)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.square)]),
    ],
    (MatAdd, Q.orthogonal): [
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.square)]),
    ],
    (MatAdd, Q.positive_definite): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.positive_definite)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.square)]),
    ],
    (MatAdd, Q.real_elements): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.real_elements)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real_elements)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex_elements)]),
    ],
    (MatAdd, Q.singular): [
        (FALSE_IF, [(ALL_ARGS_ARE, Q.positive_definite)]),
    ],
    (MatAdd, Q.square): [
        (TRUE_IF, [(ANY_ARG_IS, Q.square)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.square)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.positive_definite)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.symmetric)]),
    ],
    (MatAdd, Q.symmetric): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.symmetric)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.symmetric)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.square)]),
    ],
    (MatAdd, Q.triangular): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.lower_triangular)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.upper_triangular)]),
    ],
    (MatAdd, Q.unitary): [
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.square)]),
    ],
    (MatAdd, Q.upper_triangular): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.upper_triangular)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.upper_triangular)]),
    ],
    (MatMul, Q.complex_elements): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.complex_elements)]),
    ],
    (MatMul, Q.diagonal): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.diagonal)]),
    ],
    (MatMul, Q.fullrank): [
        (TRUE_IF, [(ONE_ARG_IS_NOT, Q.square), (ALL_ARGS_ARE, Q.fullrank)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.invertible)]),
    ],
    (MatMul, Q.integer_elements): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.integer_elements)]),
    ],
    (MatMul, Q.invertible): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.invertible)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.square), (ANY_ARG_IS_NOT, Q.invertible)]),
    ],
    (MatMul, Q.lower_triangular): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.lower_triangular)]),
    ],
    (MatMul, Q.normal): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.diagonal)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.unitary)]),
    ],
    (MatMul, Q.orthogonal): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.orthogonal)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.square), (ANY_ARG_IS_NOT, Q.invertible)]),
    ],
    (MatMul, Q.positive_definite): [
        (FALSE_IF, [(ALL_ARGS_ARE, Q.square), (ANY_ARG_IS_NOT, Q.invertible)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.orthogonal)]),
    ],
    (MatMul, Q.real_elements): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.real_elements)]),
    ],
    (MatMul, Q.singular): [
        (FALSE_IF, [(ALL_ARGS_ARE, Q.invertible)]),
    ],
    (MatMul, Q.square): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.square)]),
    ],
    (MatMul, Q.symmetric): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.diagonal)]),
    ],
    (MatMul, Q.triangular): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.lower_triangular)]),
        (TRUE_IF, [(ALL_ARGS_ARE, Q.upper_triangular)]),
    ],
    (MatMul, Q.unitary): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.unitary)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.square), (ANY_ARG_IS_NOT, Q.invertible)]),
    ],
    (MatMul, Q.upper_triangular): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.upper_triangular)]),
    ],
    (MatPow, Q.complex_elements): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.complex_elements),
            (FIRST_ARG_IS, Q.invertible),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.complex_elements),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
    ],
    (MatPow, Q.diagonal): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.diagonal),
            (FIRST_ARG_IS, Q.invertible),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.diagonal),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
    ],
    (MatPow, Q.fullrank): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.fullrank), (SECOND_ARG_IS, Q.integer)]),
    ],
    (MatPow, Q.integer_elements): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer_elements),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
    ],
    (MatPow, Q.invertible): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.invertible), (SECOND_ARG_IS, Q.integer)]),
        (FALSE_IF, [
            (FIRST_ARG_IS_NOT, Q.invertible),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (MatPow, Q.lower_triangular): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.invertible),
            (FIRST_ARG_IS, Q.lower_triangular),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.lower_triangular),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
    ],
    (MatPow, Q.normal): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.diagonal),
            (FIRST_ARG_IS, Q.invertible),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.diagonal),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.unitary), (SECOND_ARG_IS, Q.integer)]),
    ],
    (MatPow, Q.orthogonal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.orthogonal), (SECOND_ARG_IS, Q.integer)]),
        (FALSE_IF, [
            (FIRST_ARG_IS_NOT, Q.invertible),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (MatPow, Q.positive_definite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite), (SECOND_ARG_IS, Q.integer)]),
        (FALSE_IF, [
            (FIRST_ARG_IS_NOT, Q.invertible),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (MatPow, Q.real_elements): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.invertible),
            (FIRST_ARG_IS, Q.real_elements),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.real_elements),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
    ],
    (MatPow, Q.singular): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.invertible), (SECOND_ARG_IS, Q.integer)]),
    ],
    (MatPow, Q.square): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.invertible), (SECOND_ARG_IS, Q.integer)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.symmetric),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
    ],
    (MatPow, Q.symmetric): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.invertible),
            (FIRST_ARG_IS, Q.symmetric),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.symmetric),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
    ],
    (MatPow, Q.triangular): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.invertible),
            (FIRST_ARG_IS, Q.lower_triangular),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.lower_triangular),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.invertible),
            (FIRST_ARG_IS, Q.upper_triangular),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.upper_triangular),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
    ],
    (MatPow, Q.unitary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.unitary), (SECOND_ARG_IS, Q.integer)]),
        (FALSE_IF, [
            (FIRST_ARG_IS_NOT, Q.invertible),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (MatPow, Q.upper_triangular): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.invertible),
            (FIRST_ARG_IS, Q.upper_triangular),
            (SECOND_ARG_IS, Q.integer),
        ]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.upper_triangular),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
    ],
    (MatrixElement, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (MatrixElement, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
    ],
    (MatrixElement, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
    ],
    (MatrixElement, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (MatrixElement, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
    ],
    (MatrixElement, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (MatrixElement, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (MatrixElement, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
    ],
    (MatrixElement, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (MatrixElement, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (MatrixElement, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
    ],
    (MatrixElement, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
    ],
    (MatrixElement, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (MatrixElement, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (MatrixElement, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (MatrixSlice, Q.complex_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
    ],
    (MatrixSlice, Q.integer_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (MatrixSlice, Q.real_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (Mul, Q.algebraic): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.algebraic)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.imaginary), (OTHER_ARGS_ARE, Q.nonzero)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.extended_negative),
            (OTHER_ARGS_ARE, Q.extended_positive),
        ]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
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
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.negative), (OTHER_ARGS_ARE, Q.positive)]),
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
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
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
    ],
    (Mul, Q.extended_real): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.extended_real), (ONE_ARG_IS_NOT, Q.nonzero)]),
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
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
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
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
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
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
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
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.algebraic), (OTHER_ARGS_ARE_NOT, Q.zero)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.rational)]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.real), (OTHER_ARGS_ARE_NOT, Q.zero)]),
    ],
    (Mul, Q.negative): [
        (TRUE_IF, [(ODD_NUMBER_OF_ARGS_ARE, Q.negative), (OTHER_ARGS_ARE, Q.positive)]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
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
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
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
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.integer), (ANY_ARG_IS, Q.even)]),
        (FALSE_IF, [(ANY_ARG_IS, Q.zero)]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
    ],
    (Mul, Q.positive): [
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.negative),
            (OTHER_ARGS_ARE, Q.positive),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS_NOT, Q.commutative),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
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
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
        (FALSE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.prime),
            (OTHER_ARGS_ARE, Q.integer),
            (OTHER_ARGS_ARE, Q.positive),
            (ANY_ARG_IS, Q.prime),
        ]),
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [(ALL_ARGS_ARE, Q.infinite)]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
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
        (FALSE_IF, [(ANY_ARG_IS_NOT, Q.finite)]),
        (FALSE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.imaginary),
            (OTHER_ARGS_ARE, Q.nonzero),
        ]),
        (FALSE_IF, [
            (ONE_ARG_IS, Q.infinite),
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
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
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.transcendental),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
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
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.extended_nonnegative),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive), (SECOND_ARG_IS, Q.real)]),
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
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite), (SECOND_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.finite),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.finite),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.zero),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.real),
        ]),
    ],
    (Pow, Q.composite): [
        (FALSE_IF, [
            (FIRST_ARG_IS_NOT, Q.algebraic),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.prime),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
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
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Pow, Q.extended_negative): [
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.extended_nonnegative),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.odd),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.real),
            (SECOND_ARG_IS, Q.even),
            (SECOND_ARG_IS, Q.nonnegative),
        ]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
    ],
    (Pow, Q.extended_nonnegative): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.extended_nonnegative),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
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
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
    ],
    (Pow, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.nonpositive),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.odd),
        ]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Pow, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Pow, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.nonpositive),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.odd),
        ]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
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
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.extended_nonnegative),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.even)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.zero),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.real),
        ]),
    ],
    (Pow, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite), (SECOND_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.finite),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.finite),
        ]),
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
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
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
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.zero),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.real),
        ]),
    ],
    (Pow, Q.imaginary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.integer)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.irrational)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.even)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.zero),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.real),
        ]),
    ],
    (Pow, Q.infinite): [
        (TRUE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
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
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
    ],
    (Pow, Q.integer): [
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (FALSE_IF, [
            (FIRST_ARG_IS_NOT, Q.algebraic),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
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
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Pow, Q.irrational): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.prime),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Pow, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.even)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.extended_nonnegative),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
    ],
    (Pow, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (SECOND_ARG_IS, Q.finite)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.extended_nonnegative),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Pow, Q.nonpositive): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.nonpositive),
            (SECOND_ARG_IS, Q.nonnegative),
            (SECOND_ARG_IS, Q.odd),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Pow, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.negative), (SECOND_ARG_IS, Q.odd)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.negative),
            (SECOND_ARG_IS_NOT, Q.integer),
            (SECOND_ARG_IS, Q.rational),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Pow, Q.odd): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.odd),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.negative),
        ]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Pow, Q.positive): [
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonzero), (SECOND_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive), (SECOND_ARG_IS, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
    ],
    (Pow, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (SECOND_ARG_IS, Q.finite)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
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
            (FIRST_ARG_IS_NOT, Q.algebraic),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
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
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.imaginary), (SECOND_ARG_IS, Q.odd)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.finite), (SECOND_ARG_IS, Q.positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(SECOND_ARG_IS, Q.zero)]),
    ],
    (Pow, Q.transcendental): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.transcendental),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS_NOT, Q.zero),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.positive)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(SECOND_ARG_IS, Q.zero)]),
    ],
    (QofQR, Q.complex_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (QofQR, Q.fullrank): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (QofQR, Q.invertible): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (QofQR, Q.normal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (QofQR, Q.orthogonal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.square)]),
    ],
    (QofQR, Q.positive_definite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.square)]),
    ],
    (QofQR, Q.real_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (QofQR, Q.singular): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (QofQR, Q.square): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (QofQR, Q.unitary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (RofQR, Q.complex_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (RofQR, Q.real_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (RofQR, Q.triangular): [
        ALWAYS_TRUE,
    ],
    (RofQR, Q.upper_triangular): [
        ALWAYS_TRUE,
    ],
    (SofSVD, Q.complex_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (SofSVD, Q.diagonal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (SofSVD, Q.lower_triangular): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (SofSVD, Q.normal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (SofSVD, Q.real_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (SofSVD, Q.square): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (SofSVD, Q.symmetric): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (SofSVD, Q.triangular): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (SofSVD, Q.upper_triangular): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (Symbol, Q.infinite): [
        (TRUE_IF, [(SELF_IS, Q.commutative), (SELF_IS_NOT, Q.finite)]),
    ],
    (Trace, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (Trace, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.complex_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
    ],
    (Trace, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (Trace, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (Trace, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (Trace, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.integer): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (Trace, Q.integer_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (Trace, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (Trace, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.rational): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (Trace, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Trace, Q.real_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (Trace, Q.transcendental): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
    ],
    (Trace, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
    ],
    (Transpose, Q.complex_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.complex_elements)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.complex_elements)]),
    ],
    (Transpose, Q.diagonal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.diagonal)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.diagonal)]),
    ],
    (Transpose, Q.fullrank): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.fullrank)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.fullrank)]),
    ],
    (Transpose, Q.integer_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer_elements)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.integer_elements)]),
    ],
    (Transpose, Q.invertible): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.invertible)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.invertible)]),
    ],
    (Transpose, Q.lower_triangular): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.upper_triangular)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.upper_triangular)]),
    ],
    (Transpose, Q.normal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.diagonal)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.unitary)]),
    ],
    (Transpose, Q.orthogonal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.orthogonal)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.orthogonal)]),
    ],
    (Transpose, Q.positive_definite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.positive_definite)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive_definite)]),
    ],
    (Transpose, Q.real_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.real_elements)]),
    ],
    (Transpose, Q.singular): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.invertible)]),
    ],
    (Transpose, Q.square): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.invertible)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.symmetric)]),
    ],
    (Transpose, Q.symmetric): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.symmetric)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.symmetric)]),
    ],
    (Transpose, Q.triangular): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.upper_triangular)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.lower_triangular)]),
    ],
    (Transpose, Q.unitary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.unitary)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.unitary)]),
    ],
    (Transpose, Q.upper_triangular): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.lower_triangular)]),
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.lower_triangular)]),
    ],
    (UofLU, Q.complex_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (UofLU, Q.real_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (UofLU, Q.triangular): [
        ALWAYS_TRUE,
    ],
    (UofLU, Q.upper_triangular): [
        ALWAYS_TRUE,
    ],
    (UofSVD, Q.complex_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (UofSVD, Q.fullrank): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (UofSVD, Q.invertible): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (UofSVD, Q.normal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (UofSVD, Q.orthogonal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.square)]),
    ],
    (UofSVD, Q.positive_definite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.square)]),
    ],
    (UofSVD, Q.real_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (UofSVD, Q.singular): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (UofSVD, Q.square): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (UofSVD, Q.unitary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (VofSVD, Q.complex_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (VofSVD, Q.fullrank): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (VofSVD, Q.invertible): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (VofSVD, Q.normal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (VofSVD, Q.orthogonal): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.square)]),
    ],
    (VofSVD, Q.positive_definite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements), (FIRST_ARG_IS, Q.square)]),
    ],
    (VofSVD, Q.real_elements): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real_elements)]),
    ],
    (VofSVD, Q.singular): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (VofSVD, Q.square): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (VofSVD, Q.unitary): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.square)]),
    ],
    (ZeroMatrix, Q.complex_elements): [
        ALWAYS_TRUE,
    ],
    (ZeroMatrix, Q.diagonal): [
        (TRUE_IF, [(SELF_IS, Q.square)]),
        (FALSE_IF, [(SELF_IS_NOT, Q.square)]),
    ],
    (ZeroMatrix, Q.fullrank): [
        ALWAYS_FALSE,
    ],
    (ZeroMatrix, Q.integer_elements): [
        ALWAYS_TRUE,
    ],
    (ZeroMatrix, Q.invertible): [
        ALWAYS_FALSE,
    ],
    (ZeroMatrix, Q.lower_triangular): [
        (TRUE_IF, [(SELF_IS, Q.square)]),
    ],
    (ZeroMatrix, Q.normal): [
        (TRUE_IF, [(SELF_IS, Q.square)]),
        (FALSE_IF, [(SELF_IS_NOT, Q.square)]),
    ],
    (ZeroMatrix, Q.orthogonal): [
        ALWAYS_FALSE,
    ],
    (ZeroMatrix, Q.positive_definite): [
        ALWAYS_FALSE,
    ],
    (ZeroMatrix, Q.real_elements): [
        ALWAYS_TRUE,
    ],
    (ZeroMatrix, Q.symmetric): [
        (TRUE_IF, [(SELF_IS, Q.square)]),
        (FALSE_IF, [(SELF_IS_NOT, Q.square)]),
    ],
    (ZeroMatrix, Q.triangular): [
        (TRUE_IF, [(SELF_IS, Q.square)]),
    ],
    (ZeroMatrix, Q.unitary): [
        ALWAYS_FALSE,
    ],
    (ZeroMatrix, Q.upper_triangular): [
        (TRUE_IF, [(SELF_IS, Q.square)]),
    ],
    (acos, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (acos, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (acos, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (acos, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (acos, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.positive)]),
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
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (acos, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (acos, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (acos, Q.negative): [
        ALWAYS_FALSE,
    ],
    (acos, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.positive)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (acos, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (acos, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (acos, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (acos, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (acos, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (acos, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.positive)]),
    ],
    (acot, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (acot, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.imaginary)]),
    ],
    (acot, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
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
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
    ],
    (acot, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.imaginary)]),
    ],
    (acot, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (acot, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
    ],
    (acot, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_nonnegative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.nonnegative)]),
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
    (atan, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.imaginary),
            (FIRST_ARG_IS_NOT, Q.zero),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.imaginary),
            (FIRST_ARG_IS_NOT, Q.zero),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.extended_nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.imaginary),
            (FIRST_ARG_IS_NOT, Q.zero),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.imaginary),
            (FIRST_ARG_IS_NOT, Q.zero),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.imaginary),
            (FIRST_ARG_IS_NOT, Q.zero),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.nonnegative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (FALSE_IF, [
            (FIRST_ARG_IS, Q.algebraic),
            (FIRST_ARG_IS_NOT, Q.imaginary),
            (FIRST_ARG_IS_NOT, Q.zero),
        ]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (atan, Q.real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
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
    (cot, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (cot, Q.composite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (cot, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (cot, Q.integer): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (cot, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (cot, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (cot, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
    ],
    (cot, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
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
        ALWAYS_FALSE,
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
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.positive_infinite)]),
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
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.negative_infinite)]),
    ],
    (factorial, Q.commutative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.complex): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.extended_nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.extended_nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.extended_positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.extended_real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.hermitian): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.imaginary): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.nonpositive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.nonzero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
    ],
    (factorial, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
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
    (re, Q.algebraic): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.even)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.odd)]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.even)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.odd)]),
    ],
    (re, Q.zero): [
        (FALSE_IF, [(FIRST_ARG_IS_NOT, Q.even), (FIRST_ARG_IS, Q.real)]),
    ],
    (sign, Q.commutative): [
        ALWAYS_TRUE,
    ],
    (sign, Q.complex): [
        ALWAYS_TRUE,
    ],
    (sign, Q.finite): [
        ALWAYS_TRUE,
    ],
    (sign, Q.infinite): [
        ALWAYS_FALSE,
    ],
    (sign, Q.negative_infinite): [
        ALWAYS_FALSE,
    ],
    (sign, Q.positive_infinite): [
        ALWAYS_FALSE,
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.even): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.extended_negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.extended_nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.extended_nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.extended_nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.extended_positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.extended_real): [
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.irrational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.negative): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.negative_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.nonnegative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.nonpositive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.nonzero): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.odd): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.positive): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.positive_infinite): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.prime): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.rational): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
    (tan, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
}
