"""
Do NOT manually edit this file.
Instead, run ./bin/ask_rules_update.py.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.ask import Q
from sympy.assumptions.rule_engine import (ALWAYS_FALSE, ALWAYS_TRUE, FALSE_IF,
    FIRST_ARG_IS, FIRST_ARG_IS_NOT, SECOND_ARG_IS, SECOND_ARG_IS_NOT, SELF_IS,
    SELF_IS_NOT, TRUE_IF)
from sympy.core.basic import Basic
from sympy.core.expr import Expr
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
from sympy.matrices.expressions.determinant import Determinant
from sympy.matrices.expressions.inverse import Inverse
from sympy.matrices.expressions.matexpr import MatrixElement
from sympy.matrices.expressions.matpow import MatPow
from sympy.matrices.expressions.slice import MatrixSlice
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
