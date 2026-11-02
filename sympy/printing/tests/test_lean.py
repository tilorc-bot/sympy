from __future__ import annotations

from sympy.concrete import Product, Sum
from sympy.core import (E, Eq, Float, Function, I, Lambda, Le, Lt, Ge, Gt, Ne,
                        Rational, S, Subs, Symbol, Derivative, oo, pi, symbols,
                        zoo, nan)
from sympy.functions import (Abs, Heaviside, Max, Min, Piecewise, acos, acot,
                             acosh, arg, asin, asinh, atan, atan2, atanh,
                             ceiling, conjugate, cos, cosh, cot, exp, floor,
                             gamma, im, log, re, sec, sign, sin, sinh, sqrt,
                             tan, tanh, erf)
from sympy.integrals import Integral
from sympy.logic import And, Equivalent, ITE, Implies, Not, Or, Xor
from sympy.logic.boolalg import false, true
from sympy.matrices import (Determinant, Identity, Inverse, Matrix,
                            MatrixSymbol, Trace, Transpose, ZeroMatrix)
from sympy.printing.codeprinter import PrintMethodNotImplementedError
from sympy.printing.lean import lean_code
from sympy.printing.tests.check_printed_code import check_printed_code
from sympy.testing.pytest import raises

x, y, z, w = symbols('x y z w')
n, m, i, j = symbols('n m i j', integer=True)
p, q = symbols('p q')
f, g = symbols('f g', cls=Function)
A, B = MatrixSymbol('A', 2, 2), MatrixSymbol('B', 2, 2)


def complex_code(expr):
    return lean_code(expr, number_type='complex')


@check_printed_code
def test_Integer():
    assert lean_code(x + 67) == "x + 67"
    assert lean_code(x - 1) == "x - 1"
    assert lean_code(-x) == "-x"


@check_printed_code
def test_numbers_are_given_a_type():
    # Without a type Lean would make 3 / 7 a natural number, which is 0
    assert lean_code(S(67)) == "(67 : ℝ)"
    assert lean_code(Rational(3, 7)) == "(3 / 7 : ℝ)"
    assert lean_code(Rational(-3, 7)) == "(-3 / 7 : ℝ)"
    assert complex_code(Rational(3, 7)) == "(3 / 7 : ℂ)"
    assert lean_code(Float(0.5)) == "(0.500000000000000 : ℝ)"
    assert lean_code(Eq(S(1), S(2), evaluate=False)) == "(1 : ℝ) = 2"
    assert lean_code(Piecewise((1, x < 0), (2, True))) == \
        "(if x < 0 then 1 else 2 : ℝ)"


@check_printed_code
def test_Rational():
    assert lean_code(x + Rational(3, 7)) == "x + 3 / 7"
    assert lean_code(Rational(3, 7)*x) == "3 * x / 7"
    assert lean_code(-Rational(3, 7)*x + y) == "-3 * x / 7 + y"
    assert lean_code(x/2) == "x / 2"


@check_printed_code
def test_Float():
    assert lean_code(Float(0.5)*x) == "0.5 * x"
    assert lean_code(Float('1.0e-20')*x) == "1.0e-20 * x"
    raises(PrintMethodNotImplementedError, lambda: lean_code(Float('inf')*x))


@check_printed_code
def test_Mul():
    assert lean_code(x*y*z) == "x * y * z"
    assert lean_code(x/(y*z)) == "x / (y * z)"
    assert lean_code(x*(y + z)) == "x * (y + z)"
    assert lean_code(2*x*(y + 1)/(z + 1)) == "2 * x * (y + 1) / (z + 1)"
    assert lean_code(-x*y) == "-x * y"
    assert lean_code(x - 2*(y + z)) == "x - 2 * y - 2 * z"


@check_printed_code
def test_Pow():
    assert lean_code(x**2) == "x ^ 2"
    # -x ^ 2 is -(x ^ 2) in Lean
    assert lean_code(-x**2) == "-x ^ 2"
    assert lean_code(1/x) == "1 / x"
    assert lean_code(x**-2) == "1 / x ^ 2"
    assert lean_code(x**y) == "x ^ y"
    assert lean_code(x**(y + 1)) == "x ^ (y + 1)"
    assert lean_code((x**y)**z) == "(x ^ y) ^ z"
    assert lean_code((x + 1)**2) == "(x + 1) ^ 2"
    assert lean_code(sin(x)**2) == "Real.sin x ^ 2"
    # A numeral exponent or base would be a natural number
    assert lean_code(x**Rational(1, 3)) == "x ^ (1 / 3 : ℝ)"
    assert lean_code(x**Rational(-2, 3)) == "x ^ (-2 / 3 : ℝ)"
    assert lean_code(2**x) == "(2 : ℝ) ^ x"
    assert lean_code(Rational(1, 2)**x) == "(1 / 2 : ℝ) ^ x"
    assert lean_code((-2)**x) == "(-2 : ℝ) ^ x"


@check_printed_code
def test_Pow_integer_exponent():
    # An exponent that is an integer is printed as an integer, so the power
    # is x ^ n for an integer n, also for a negative x
    assert lean_code(x**n) == "x ^ n"
    assert lean_code(x**(n + 1)) == "x ^ (n + 1)"
    assert lean_code(x**(2*n)) == "x ^ (2 * n)"
    r = Symbol('r', real=True)
    assert lean_code(x**floor(r)) == "x ^ ⌊r⌋"


@check_printed_code
def test_sqrt():
    assert lean_code(sqrt(x)) == "Real.sqrt x"
    assert lean_code(sqrt(x + 1)) == "Real.sqrt (x + 1)"
    assert lean_code(y/sqrt(x)) == "y / Real.sqrt x"
    assert lean_code(sqrt(2)) == "Real.sqrt 2"
    assert complex_code(sqrt(z)) == "z ^ (1 / 2 : ℂ)"


@check_printed_code
def test_integer_variables():
    # Declared as ℤ, so they are cast
    assert lean_code(n) == "(n : ℝ)"
    assert lean_code(x + n) == "(n : ℝ) + x"
    assert lean_code(sin(n)) == "Real.sin (n : ℝ)"
    assert complex_code(z + n) == "(n : ℂ) + z"
    # A variable that is real is cast to ℂ
    r = Symbol('r', real=True)
    assert complex_code(r*z) == "(r : ℂ) * z"


@check_printed_code
def test_names():
    assert lean_code(Symbol('alpha_1')) == "alpha_1"
    assert lean_code(Symbol('fun') + 1) == "«fun» + 1"
    assert lean_code(Symbol('x y') + 1) == "«x y» + 1"
    assert lean_code(Symbol('in')*x) == "«in» * x"


@check_printed_code
def test_constants():
    assert lean_code(pi*x) == "Real.pi * x"
    assert lean_code(E*x) == "Real.exp 1 * x"
    assert lean_code(S.GoldenRatio*x) == "Real.goldenRatio * x"
    assert lean_code(S.EulerGamma*x) == "Real.eulerMascheroniConstant * x"
    assert lean_code(pi) == "Real.pi"
    assert complex_code(pi*z) == "(Real.pi : ℂ) * z"
    assert complex_code(E*z) == "Complex.exp 1 * z"
    assert complex_code(I*z) == "Complex.I * z"
    raises(PrintMethodNotImplementedError, lambda: lean_code(S.Catalan*x))
    raises(PrintMethodNotImplementedError, lambda: lean_code(I*x))
    for value in (oo, -oo, zoo, nan):
        raises(PrintMethodNotImplementedError, lambda: lean_code(value))


@check_printed_code
def test_functions():
    assert lean_code(sin(x) + cos(x) + tan(x) + cot(x)) == \
        "Real.sin x + Real.cos x + Real.tan x + Real.cot x"
    assert lean_code(asin(x) + acos(x) + atan(x)) == \
        "Real.arccos x + Real.arcsin x + Real.arctan x"
    assert lean_code(sinh(x) + cosh(x) + tanh(x)) == \
        "Real.sinh x + Real.cosh x + Real.tanh x"
    assert lean_code(asinh(x) + acosh(x) + atanh(x)) == \
        "Real.arcosh x + Real.arsinh x + Real.artanh x"
    assert lean_code(exp(x) + log(x)) == "Real.exp x + Real.log x"
    assert lean_code(gamma(x) + sign(x)) == "Real.Gamma x + Real.sign x"
    assert lean_code(sin(cos(x))) == "Real.sin (Real.cos x)"
    assert lean_code(sin(-x)) == "-Real.sin x"
    assert lean_code(exp(-x)) == "Real.exp (-x)"
    assert lean_code(exp(x + 1)) == "Real.exp (x + 1)"
    assert lean_code(exp(2*x)) == "Real.exp (2 * x)"


@check_printed_code
def test_functions_rewritten():
    assert lean_code(sec(x)) == "(1 / Real.cos x)"
    assert lean_code(y/sec(x)) == "y / (1 / Real.cos x)"
    assert lean_code(Heaviside(x)) == \
        "(if x < 0 then 0 else if x = 0 then 1 / 2 else 1 : ℝ)"
    assert lean_code(x*Heaviside(x)) == \
        "x * (if x < 0 then 0 else if x = 0 then 1 / 2 else 1 : ℝ)"
    # acot(x) = atan(1/x) would be wrong at 0, where 1/0 = 0 in Lean
    raises(PrintMethodNotImplementedError, lambda: lean_code(acot(x)))
    raises(PrintMethodNotImplementedError, lambda: lean_code(erf(x)))


@check_printed_code
def test_Abs_floor_ceiling_sign():
    assert lean_code(Abs(x)) == "|x|"
    assert lean_code(Abs(x + y)) == "|x + y|"
    assert lean_code(log(Abs(x))) == "Real.log |x|"
    assert lean_code(floor(x)) == "(⌊x⌋ : ℝ)"
    assert lean_code(ceiling(x + y)) == "(⌈x + y⌉ : ℝ)"
    assert complex_code(Abs(z)) == "(‖z‖ : ℂ)"
    raises(PrintMethodNotImplementedError, lambda: complex_code(floor(z)))


@check_printed_code
def test_Max_Min():
    assert lean_code(Max(x, y)) == "max x y"
    assert lean_code(Max(x, y, z)) == "max x (max y z)"
    assert lean_code(Min(x + 1, y)) == "min y (x + 1)"
    raises(PrintMethodNotImplementedError, lambda: complex_code(Max(z, w)))


@check_printed_code
def test_atan2():
    # The argument of x + i y
    assert lean_code(atan2(y, x)) == "Complex.arg ⟨x, y⟩"


@check_printed_code
def test_complex_functions():
    assert complex_code(exp(I*z) + log(z)) == \
        "Complex.exp (Complex.I * z) + Complex.log z"
    assert complex_code(sin(z) + cosh(z) + atan(z) + gamma(z)) == \
        "Complex.sin z + Complex.cosh z + Complex.arctan z + Complex.Gamma z"
    assert complex_code(re(z)) == "(Complex.re z : ℂ)"
    assert complex_code(im(z)) == "(Complex.im z : ℂ)"
    assert complex_code(arg(z)) == "(Complex.arg z : ℂ)"
    assert complex_code(conjugate(z)) == "(starRingEnd ℂ) z"
    assert complex_code(z**w) == "z ^ w"
    raises(PrintMethodNotImplementedError, lambda: complex_code(asin(z)))
    raises(PrintMethodNotImplementedError, lambda: lean_code(re(x)))


@check_printed_code
def test_undefined_functions():
    assert lean_code(f(x)) == "f x"
    assert lean_code(f(x, y + 1)) == "f x (y + 1)"
    assert lean_code(f(g(x))) == "f (g x)"
    assert lean_code(f(x)**2) == "f x ^ 2"


def test_user_functions():
    assert lean_code(f(x), user_functions={'f': 'Real.cos'}) == "Real.cos x"
    assert lean_code(erf(x), user_functions={'erf': 'myErf'}) == "myErf x"
    assert lean_code(f(x), user_functions={
        'f': [(lambda v: v.is_positive, 'fpos'), (lambda v: True, 'fany')]}
        ) == "fany x"


@check_printed_code
def test_Relational():
    assert lean_code(Eq(x, y)) == "x = y"
    assert lean_code(Ne(x, y)) == "x ≠ y"
    assert lean_code(Le(x, y)) == "x ≤ y"
    assert lean_code(Lt(x, y)) == "x < y"
    assert lean_code(Gt(x, y)) == "x > y"
    assert lean_code(Ge(x, y)) == "x ≥ y"
    assert lean_code(Eq(x + 1, 2*y)) == "x + 1 = 2 * y"


@check_printed_code
def test_logic():
    assert lean_code(true) == "True"
    assert lean_code(false) == "False"
    assert lean_code(And(p, q)) == "p ∧ q"
    assert lean_code(Or(p, q)) == "p ∨ q"
    assert lean_code(Not(p)) == "¬p"
    assert lean_code(Not(x < 1)) == "x ≥ 1"
    assert lean_code(Not(Eq(x, 1), evaluate=False)) == "¬x = 1"
    assert lean_code(Not(And(p, q))) == "¬(p ∧ q)"
    assert lean_code(And(x < 1, Or(y > 2, Ne(z, 3)))) == \
        "(y > 2 ∨ z ≠ 3) ∧ x < 1"
    assert lean_code(Or(And(p, q), Not(p))) == "p ∧ q ∨ ¬p"
    assert lean_code(Implies(p, q)) == "p → q"
    assert lean_code(Implies(x > 1, Or(y > 1, z > 1))) == \
        "x > 1 → y > 1 ∨ z > 1"
    assert lean_code(Or(Implies(p, q), q)) == "q ∨ (p → q)"
    assert lean_code(Equivalent(p, q)) == "p ↔ q"
    assert lean_code(Equivalent(x > 1, y > 1, z > 1)) == \
        "(x > 1 ↔ y > 1) ∧ (y > 1 ↔ z > 1)"
    assert lean_code(Xor(p, q)) == "(p ∨ q) ∧ (¬p ∨ ¬q)"
    assert lean_code(ITE(p, x > 1, y > 1)) == "if p then x > 1 else y > 1"


@check_printed_code
def test_Piecewise():
    assert lean_code(Piecewise((x, x < 0), (0, True))) == \
        "if x < 0 then x else 0"
    assert lean_code(Piecewise((x, x < 0), (x**2, x < 1), (1, True))) == \
        "if x < 0 then x else if x < 1 then x ^ 2 else 1"
    assert lean_code(1 + Piecewise((x, x < 0), (0, True))) == \
        "(if x < 0 then x else 0) + 1"
    assert lean_code(Eq(Piecewise((x, x < 0), (0, True)), y)) == \
        "(if x < 0 then x else 0) = y"
    # Undefined where no condition holds
    raises(PrintMethodNotImplementedError,
           lambda: lean_code(Piecewise((x, x < 0))))


@check_printed_code
def test_Lambda():
    assert lean_code(Lambda(x, x**2)) == "fun x : ℝ ↦ x ^ 2"
    assert lean_code(Lambda((x, y), x*y)) == "fun (x : ℝ) (y : ℝ) ↦ x * y"
    assert lean_code(Lambda((x, n), x**n)) == "fun (x : ℝ) (n : ℤ) ↦ x ^ n"


@check_printed_code
def test_Derivative():
    assert lean_code(Derivative(f(x), x)) == "deriv (fun x : ℝ ↦ f x) x"
    assert lean_code(Derivative(x**3, (x, 2))) == \
        "iteratedDeriv 2 (fun x : ℝ ↦ x ^ 3) x"
    # The second variable is differentiated after the first
    assert lean_code(Derivative(sin(x*y), x, y)) == \
        "deriv (fun y : ℝ ↦ deriv (fun x : ℝ ↦ Real.sin (x * y)) x) y"
    assert lean_code(Derivative(f(x), x) + 1) == \
        "deriv (fun x : ℝ ↦ f x) x + 1"
    assert complex_code(Derivative(f(z), z)) == "deriv (fun z : ℂ ↦ f z) z"
    raises(PrintMethodNotImplementedError,
           lambda: lean_code(Derivative(f(x), (x, n))))
    raises(PrintMethodNotImplementedError,
           lambda: lean_code(Derivative(f(x)**2, f(x))))


@check_printed_code
def test_Subs():
    assert lean_code(Subs(x**2, x, y + 1)) == "(fun x : ℝ ↦ x ^ 2) (y + 1)"
    assert lean_code(Subs(Derivative(f(x), x), x, 0)) == \
        "(fun x : ℝ ↦ deriv (fun x : ℝ ↦ f x) x) 0"
    assert lean_code(Subs(x*y, (x, y), (1, 2))) == \
        "(fun (x : ℝ) (y : ℝ) ↦ x * y) 1 2"


@check_printed_code
def test_Integral():
    assert lean_code(Integral(x**2, (x, 0, 1))) == \
        "∫ x in (0 : ℝ)..1, x ^ 2"
    assert lean_code(Integral(sin(x*y), (x, 0, y))) == \
        "∫ x in (0 : ℝ)..y, Real.sin (x * y)"
    assert lean_code(Integral(x*y, (x, 0, 1), (y, -1, z + 1))) == \
        "∫ y in (-1 : ℝ)..(z + 1), ∫ x in (0 : ℝ)..1, x * y"
    assert lean_code(Eq(Integral(x**2, (x, 0, 1)), Rational(1, 3))) == \
        "(∫ x in (0 : ℝ)..1, x ^ 2) = 1 / 3"
    assert lean_code(Integral(1, (x, 0, 1))) == "(∫ x in (0 : ℝ)..1, 1 : ℝ)"
    raises(PrintMethodNotImplementedError, lambda: lean_code(Integral(x, x)))
    raises(PrintMethodNotImplementedError,
           lambda: lean_code(Integral(exp(-x), (x, 0, oo))))


@check_printed_code
def test_Sum_Product():
    assert lean_code(Sum(i**2, (i, 1, n))) == \
        "∑ i ∈ Finset.Icc (1 : ℤ) n, (i : ℝ) ^ 2"
    assert lean_code(Sum(x**i, (i, 0, n))) == \
        "∑ i ∈ Finset.Icc (0 : ℤ) n, x ^ i"
    assert lean_code(Product(i, (i, 1, n))) == \
        "∏ i ∈ Finset.Icc (1 : ℤ) n, (i : ℝ)"
    # A variable that isn't an integer becomes one
    assert lean_code(Sum(1/x, (x, 1, 3))) == \
        "∑ x ∈ Finset.Icc (1 : ℤ) 3, 1 / (x : ℝ)"
    assert lean_code(Sum(i*j, (i, 1, j), (j, -2, n + 1))) == \
        "∑ j ∈ Finset.Icc (-2 : ℤ) (n + 1), ∑ i ∈ Finset.Icc (1 : ℤ) j, " \
        "(i : ℝ) * (j : ℝ)"
    assert lean_code(Sum(1, (i, 1, n))) == \
        "(∑ i ∈ Finset.Icc (1 : ℤ) n, 1 : ℝ)"
    raises(PrintMethodNotImplementedError,
           lambda: lean_code(Sum(i, (i, 1, x))))
    raises(PrintMethodNotImplementedError,
           lambda: lean_code(Sum(1/i**2, (i, 1, oo))))


@check_printed_code
def test_matrices():
    assert lean_code(Matrix([[x, 1], [2, 3]])) == "!![x, 1; 2, 3]"
    assert lean_code(Matrix([[1, 2], [3, 4]])) == \
        "(!![1, 2; 3, 4] : Matrix (Fin 2) (Fin 2) ℝ)"
    assert lean_code(Matrix([[x, y]])) == "!![x, y]"
    assert lean_code(Matrix([x, y])) == "!![x; y]"
    assert lean_code(A*B + A) == "A * B + A"
    assert lean_code(A - B) == "-B + A"
    assert lean_code(2*A) == "(2 : ℝ) • A"
    assert lean_code(x*A*B) == "x • A * B"
    assert lean_code(A**2) == "A ^ 2"
    assert lean_code(Inverse(A)) == "A⁻¹"
    assert lean_code(Inverse(A*B)) == "(A * B)⁻¹"
    assert lean_code(Transpose(A)) == "A.transpose"
    assert lean_code(Determinant(A*B)) == "(A * B).det"
    assert lean_code(Trace(A)) == "A.trace"
    assert lean_code(A[0, 1]) == "A 0 1"
    assert lean_code(Identity(2) + A) == "(1 : Matrix (Fin 2) (Fin 2) ℝ) + A"
    assert lean_code(ZeroMatrix(2, 2)) == "(0 : Matrix (Fin 2) (Fin 2) ℝ)"


@check_printed_code
def test_containers():
    assert lean_code((x, y + 1)) == "(x, y + 1)"
    assert lean_code([x, y]) == "[x, y]"


def test_not_strict():
    assert lean_code(erf(x) + 1, strict=False) == \
        "-- Not supported in Lean:\n-- erf\nerf(x) + 1"


def test_number_type():
    raises(ValueError, lambda: lean_code(x, number_type='rational'))
