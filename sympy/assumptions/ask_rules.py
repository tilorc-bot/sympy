"""The rules which answer a predicate about an expression from its arguments."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.ask import Q
from sympy.assumptions.rule_engine import (ALL_ARGS_ARE, ALL_ARGS_ARE_NOT,
    ALWAYS_FALSE, ALWAYS_TRUE, ANY_ARG_IS, ANY_ARG_IS_NOT, EVEN_NUMBER_OF_ARGS_ARE,
    FALSE_IF, FIRST_ARG_IS, FIRST_ARG_IS_NOT, IF_AND_ONLY_IF, ODD_NUMBER_OF_ARGS_ARE,
    ONE_ARG_IS, ONE_ARG_IS_NOT, OTHER_ARGS_ARE, OTHER_ARGS_ARE_NOT, SECOND_ARG_IS,
    SECOND_ARG_IS_NOT, SELF_IS, SELF_IS_NOT, TRUE_IF)
from sympy.core.add import Add
from sympy.core.expr import Expr
from sympy.core.mul import Mul
from sympy.core.numbers import I
from sympy.core.power import Pow
from sympy.core.singleton import S
from sympy.functions.combinatorial.factorials import factorial
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.complexes import im
from sympy.functions.elementary.complexes import re
from sympy.functions.elementary.complexes import sign
from sympy.functions.elementary.exponential import exp
from sympy.functions.elementary.exponential import log
from sympy.functions.elementary.trigonometric import acos
from sympy.functions.elementary.trigonometric import acot
from sympy.functions.elementary.trigonometric import asin
from sympy.functions.elementary.trigonometric import atan
from sympy.functions.elementary.trigonometric import cos
from sympy.functions.elementary.trigonometric import cot
from sympy.functions.elementary.trigonometric import sin
from sympy.functions.elementary.trigonometric import tan

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
    ],
    (Add, Q.nonpositive): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.nonpositive)]),
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
        (FALSE_IF, [(ONE_ARG_IS_NOT, Q.complex)]),
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
            (OTHER_ARGS_ARE, Q.complex),
            (OTHER_ARGS_ARE_NOT, Q.zero),
        ]),
    ],
    (Mul, Q.integer): [
        (TRUE_IF, [(ALL_ARGS_ARE, Q.integer)]),
        (FALSE_IF, [(ONE_ARG_IS, S.Half), (OTHER_ARGS_ARE, Q.odd)]),
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
    ],
    (Mul, Q.nonnegative): [
        (TRUE_IF, [
            (EVEN_NUMBER_OF_ARGS_ARE, Q.nonpositive),
            (OTHER_ARGS_ARE, Q.nonnegative),
        ]),
    ],
    (Mul, Q.nonpositive): [
        (TRUE_IF, [
            (ODD_NUMBER_OF_ARGS_ARE, Q.nonpositive),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.zero), (SECOND_ARG_IS, Q.negative)]),
    ],
    (Pow, Q.even): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.even),
            (SECOND_ARG_IS, Q.integer),
            (SECOND_ARG_IS, Q.positive),
        ]),
    ],
    (Pow, Q.extended_nonnegative): [
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.extended_nonnegative),
            (SECOND_ARG_IS, Q.positive),
        ]),
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive), (SECOND_ARG_IS, Q.real)]),
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
    ],
    (Pow, Q.finite): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.finite), (SECOND_ARG_IS, Q.nonnegative)]),
        (TRUE_IF, [
            (FIRST_ARG_IS, Q.finite),
            (FIRST_ARG_IS_NOT, Q.zero),
            (SECOND_ARG_IS, Q.finite),
        ]),
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
        (FALSE_IF, [(FIRST_ARG_IS, Q.real), (SECOND_ARG_IS, Q.even)]),
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
    (acot, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.imaginary)]),
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
    (atan, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (atan, Q.extended_real): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite), (FIRST_ARG_IS_NOT, Q.real)]),
    ],
    (atan, Q.negative): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_negative)]),
    ],
    (atan, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.extended_positive)]),
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
    (cot, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic)]),
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
    (exp, Q.negative_infinite): [
        ALWAYS_FALSE,
    ],
    (exp, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp, Q.positive_infinite): [
        (IF_AND_ONLY_IF, [(FIRST_ARG_IS, Q.positive_infinite)]),
    ],
    (exp, Q.real): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.real)]),
    ],
    (exp, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (exp, Q.zero): [
        (IF_AND_ONLY_IF, [(FIRST_ARG_IS, Q.negative_infinite)]),
        (FALSE_IF, [(FIRST_ARG_IS, Q.finite)]),
    ],
    (factorial, Q.positive): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.integer), (FIRST_ARG_IS, Q.nonnegative)]),
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
    (log, Q.algebraic): [
        (FALSE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, S.One)]),
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
    (sign, Q.complex): [
        ALWAYS_TRUE,
    ],
    (sign, Q.finite): [
        ALWAYS_TRUE,
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
    (tan, Q.transcendental): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.algebraic), (FIRST_ARG_IS_NOT, Q.zero)]),
    ],
    (tan, Q.zero): [
        (TRUE_IF, [(FIRST_ARG_IS, Q.zero)]),
    ],
}
