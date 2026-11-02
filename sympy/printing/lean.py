"""
Lean 4 printer

The ``LeanPrinter`` converts SymPy expressions into terms of the Lean 4
theorem prover that use the definitions of its mathematics library, Mathlib:
``sin(x)`` is printed as ``Real.sin x`` and ``Integral(x**2, (x, 0, 1))`` as
``∫ x in (0 : ℝ)..1, x ^ 2``.

The terms are meant to be used in Lean statements, e.g. ``theorem t (x : ℝ) :
<printed term> := ...``. Lean's functions are total: ``x / 0 = 0``,
``Real.log 0 = 0`` and ``Real.sqrt (-1) = 0``, whereas SymPy gives ``zoo``,
``-oo`` and ``I``. The printed term has the same value as the SymPy expression
wherever the SymPy expression is defined and has a value of the printed type
(real numbers by default), but a statement about it may hold in Lean for a
reason that has nothing to do with SymPy, e.g. ``1/x * x = 1`` is false in
Lean at ``x = 0``.
"""

from __future__ import annotations
from typing import Any

from sympy.core import Mul, Pow, S, Symbol
from sympy.core.mul import _keep_coeff
from sympy.core.numbers import Number, NumberSymbol, ImaginaryUnit
from sympy.core.relational import Relational
from sympy.core.sorting import default_sort_key
from sympy.printing.codeprinter import CodePrinter
from sympy.printing.str import StrPrinter


# Functions that are printed as an application of a Mathlib function, for
# real and for complex numbers. A function missing from a dictionary is not
# supported for that number type.
known_functions_real = {
    "exp": "Real.exp",
    "log": "Real.log",
    "sin": "Real.sin",
    "cos": "Real.cos",
    "tan": "Real.tan",
    "cot": "Real.cot",
    "asin": "Real.arcsin",
    "acos": "Real.arccos",
    "atan": "Real.arctan",
    "sinh": "Real.sinh",
    "cosh": "Real.cosh",
    "tanh": "Real.tanh",
    "asinh": "Real.arsinh",
    "acosh": "Real.arcosh",
    "atanh": "Real.artanh",
    "sign": "Real.sign",
    "gamma": "Real.Gamma",
}

known_functions_complex = {
    "exp": "Complex.exp",
    "log": "Complex.log",
    "sin": "Complex.sin",
    "cos": "Complex.cos",
    "tan": "Complex.tan",
    "cot": "Complex.cot",
    "atan": "Complex.arctan",
    "sinh": "Complex.sinh",
    "cosh": "Complex.cosh",
    "tanh": "Complex.tanh",
    "gamma": "Complex.Gamma",
}

# Words that can't be the name of a variable in Lean
reserved_words = {
    'at', 'by', 'calc', 'def', 'do', 'else', 'end', 'example', 'fun', 'have',
    'if', 'import', 'in', 'instance', 'let', 'match', 'namespace', 'open',
    'section', 'show', 'suffices', 'then', 'theorem', 'variable', 'where',
    'with', 'from', 'Type', 'Prop', 'Sort', 'λ', 'Π', 'Σ', 'deriving',
    'mutual', 'structure', 'class', 'abbrev', 'lemma', 'universe',
}

# Precedence levels of Lean's notation: a term is put in parentheses where
# Lean would otherwise read it differently
PREC_BINDER = 0  # fun, if-then-else, ∑, ∏, ∫: they extend as far as possible
PREC_IFF = 20
PREC_IMPLIES = 25
PREC_OR = 30
PREC_AND = 35
PREC_NOT = 40
PREC_REL = 50
PREC_ADD = 65
PREC_MUL = 70
PREC_NEG_NUMBER = 74
PREC_POW = 75
PREC_APP = 1023  # a function application, e.g. Real.sin x
PREC_ATOM = 1024  # a name, a nonnegative numeral or a term in brackets


class LeanPrinter(CodePrinter):
    """A printer to convert SymPy expressions to terms of Lean 4 with
    Mathlib.

    See :func:`lean_code` for the settings.
    """
    printmethod = "_lean"
    language = "Lean"

    _default_settings: dict[str, Any] = dict(CodePrinter._default_settings, **{
        'number_type': 'real',
        'user_functions': {},
    })

    _operators = {
        'and': '∧',
        'or': '∨',
        'not': '¬',
    }

    # acot(x) = atan(1/x) is wrong at x = 0 in Lean, where 1/0 = 0
    _rewriteable_functions = {k: v for k, v in
                              CodePrinter._rewriteable_functions.items()
                              if k not in ('acot', 'Max', 'Min')}

    def __init__(self, settings={}):
        CodePrinter.__init__(self, settings)
        number_type = self._settings['number_type']
        if number_type == 'real':
            self._type, functions = 'ℝ', known_functions_real
        elif number_type == 'complex':
            self._type, functions = 'ℂ', known_functions_complex
        else:
            raise ValueError("number_type must be 'real' or 'complex', not %r"
                             % (number_type,))
        self.known_functions = dict(functions)
        self.known_functions.update(self._settings['user_functions'])
        self.reserved_words = set(reserved_words)
        # Whether a number being printed has the type ℤ instead of ℝ or ℂ
        self._integer_context = False
        # Variables of sums and products, which have the type ℤ
        self._integer_variables: set[Symbol] = set()

    def _get_comment(self, text):
        return "-- {}".format(text)

    def _format_code(self, lines):
        return lines

    def _declare_number_const(self, name, value):
        return "-- {} = {}".format(name, value)

    # Types and precedence

    def _print(self, expr, **kwargs):
        text = super()._print(expr, **kwargs)
        # The type of a term made only of numerals isn't known, and Lean
        # would make it a natural number, so the whole printed term gets one
        if self._print_level == 0 and self._needs_type(expr):
            text = self._ascribe(text, expr)
        return text

    def _needs_type(self, expr):
        from sympy.concrete.expr_with_limits import ExprWithLimits
        from sympy.core.expr import Expr
        from sympy.functions.elementary.piecewise import Piecewise
        from sympy.matrices import MatrixBase
        if isinstance(expr, (Piecewise, ExprWithLimits)):
            return False  # they give themselves a type
        if isinstance(expr, MatrixBase):
            return not any(self._is_typed(e) for e in expr)
        return isinstance(expr, Expr) and not self._is_typed(expr)

    def _ascribe(self, text, expr=None):
        from sympy.matrices import MatrixBase
        if isinstance(expr, MatrixBase):
            return "(%s : Matrix (Fin %s) (Fin %s) %s)" % (
                text, expr.rows, expr.cols, self._type)
        number_type = 'ℤ' if self._integer_context else self._type
        return "(%s : %s)" % (text, number_type)

    def _is_typed(self, expr):
        """Return whether Lean can tell the type of the printed expr from the
        names in it (variables, constants, functions), so a numeral in it
        gets that type and not ℕ."""
        from sympy.concrete.expr_with_limits import ExprWithLimits
        from sympy.core.function import Function, Derivative, Subs
        from sympy.functions.elementary.piecewise import Piecewise
        from sympy.matrices.expressions.matexpr import MatrixExpr
        if isinstance(expr, Piecewise):
            return any(self._is_typed(e) for e, c in expr.args)
        if isinstance(expr, (Symbol, NumberSymbol, ImaginaryUnit, Function,
                             Derivative, Subs, Pow, MatrixExpr)):
            return True
        if isinstance(expr, Number):
            return False
        if isinstance(expr, ExprWithLimits):
            return self._is_typed(expr.function)
        return any(self._is_typed(a) for a in expr.args)

    def _precedence(self, expr):
        from sympy.concrete.expr_with_limits import ExprWithLimits
        from sympy.core.add import Add
        from sympy.core.function import Function, Derivative, Subs, Lambda
        from sympy.functions.elementary.complexes import Abs
        from sympy.functions.elementary.integers import floor, ceiling
        from sympy.functions.elementary.piecewise import Piecewise
        from sympy.logic.boolalg import (And, Or, Not, Implies, Equivalent,
                                         ITE)
        from sympy.matrices.expressions import MatAdd, MatMul, MatPow
        from sympy.matrices.expressions.matexpr import MatrixElement
        if isinstance(expr, (Piecewise, Lambda, ExprWithLimits, ITE)):
            return PREC_BINDER
        if isinstance(expr, Equivalent):
            return PREC_IFF
        if isinstance(expr, Implies):
            return PREC_IMPLIES
        if isinstance(expr, Or):
            return PREC_OR
        if isinstance(expr, And):
            return PREC_AND
        if isinstance(expr, Not):
            return PREC_NOT
        if isinstance(expr, Relational):
            return PREC_REL
        if isinstance(expr, (Add, MatAdd)):
            return PREC_ADD
        if isinstance(expr, (Mul, MatMul)):
            return PREC_MUL
        if expr.is_Rational and not expr.is_Integer:
            return PREC_MUL
        if expr.is_Number:
            return PREC_NEG_NUMBER if expr.is_negative else PREC_ATOM
        if isinstance(expr, (Pow, MatPow)):
            return PREC_POW
        if isinstance(expr, (Abs, floor, ceiling)):
            return PREC_ATOM
        if isinstance(expr, (Function, Derivative, Subs, MatrixElement)):
            return PREC_APP
        if expr is S.Exp1:
            return PREC_APP
        return PREC_ATOM

    def parenthesize(self, item, level, strict=False):
        prec = self._precedence(item)
        if prec < level or (not strict and prec <= level):
            return "(%s)" % self._print(item)
        return self._print(item)

    def _argument(self, expr):
        """Print expr as the argument of a function application."""
        return self.parenthesize(expr, PREC_APP)

    def _apply(self, function, *args):
        return ' '.join([function] + [self._argument(a) for a in args])

    def _in_number_context(self, expr, integer=False):
        """Print expr as a number of type ℝ or ℂ, or ℤ if integer."""
        saved = self._integer_context
        self._integer_context = integer
        try:
            return self._print(expr)
        finally:
            self._integer_context = saved

    def _binder_type(self, symbol):
        return 'ℤ' if symbol.is_integer else self._type

    def _binder_like(self, expr, text):
        """Give a term that extends as far as possible (if-then-else, a sum)
        a type if its value is only numerals."""
        if not self._is_typed(expr):
            return "(%s : %s)" % (text, self._type)
        return text

    # Numbers and variables

    def _print_Integer(self, expr):
        return str(expr.p)

    def _print_Rational(self, expr):
        if self._integer_context:
            return self._print_not_supported(expr)
        return '%d / %d' % (expr.p, expr.q)

    def _print_Float(self, expr):
        if not expr.is_finite:
            return self._print_not_supported(expr)
        return StrPrinter._print_Float(self, expr)

    def _print_Symbol(self, expr):
        name = self._lean_name(expr.name)
        is_integer = expr.is_integer or expr in self._integer_variables
        if self._integer_context:
            if not is_integer:
                return self._print_not_supported(expr)
            return name
        if is_integer or (self._type == 'ℂ' and expr.is_extended_real):
            # Declared as ℤ (or ℝ), so it needs a cast to the number type
            return "(%s : %s)" % (name, self._type)
        return name

    _print_Dummy = _print_Symbol

    def _lean_name(self, name):
        if name.isidentifier() and name not in self.reserved_words and \
                not set(name) & {'λ', 'Π', 'Σ'}:
            return name
        return '«%s»' % name

    def _print_ImaginaryUnit(self, expr):
        if self._type != 'ℂ':
            return self._print_not_supported(expr)
        return 'Complex.I'

    def _real_constant(self, name):
        return name if self._type == 'ℝ' else '(%s : ℂ)' % name

    def _print_Pi(self, expr):
        return self._real_constant('Real.pi')

    def _print_GoldenRatio(self, expr):
        return self._real_constant('Real.goldenRatio')

    def _print_EulerGamma(self, expr):
        return self._real_constant('Real.eulerMascheroniConstant')

    def _print_Exp1(self, expr):
        return self._apply(self.known_functions['exp'], S.One)

    _print_NumberSymbol = CodePrinter._print_not_supported
    _print_Catalan = _print_NumberSymbol
    _print_TribonacciConstant = _print_NumberSymbol

    # Arithmetic

    def _print_Add(self, expr, order=None):
        terms = self._as_ordered_terms(expr, order=order)
        text = self.parenthesize(terms[0], PREC_ADD)
        for term in terms[1:]:
            if term.could_extract_minus_sign():
                text += ' - ' + self.parenthesize(-term, PREC_ADD)
            else:
                text += ' + ' + self.parenthesize(term, PREC_ADD)
        return text

    def _print_Mul(self, expr):
        coeff, rest = expr.as_coeff_Mul()
        if coeff < 0:
            expr = _keep_coeff(-coeff, rest)
            sign = '-'
        else:
            sign = ''
        if self.order not in ('old', 'none'):
            factors = expr.as_ordered_factors()
        else:
            factors = Mul.make_args(expr)
        numerator, denominator = [], []
        for factor in factors:
            if factor.is_Rational and not factor.is_Integer:
                if factor.p != 1:
                    numerator.append(S(factor.p))
                denominator.append(S(factor.q))
            elif factor.is_commutative and factor.is_Pow and \
                    factor.exp.is_Rational and factor.exp.is_negative:
                denominator.append(
                    factor.base if factor.exp == -1 else
                    Pow(factor.base, -factor.exp, evaluate=False))
            else:
                numerator.append(factor)
        text = ' * '.join(self.parenthesize(f, PREC_MUL)
                          for f in numerator) or '1'
        if len(denominator) == 1:
            text += ' / ' + self.parenthesize(denominator[0], PREC_MUL)
        elif denominator:
            text += ' / (%s)' % ' * '.join(self.parenthesize(f, PREC_MUL)
                                           for f in denominator)
        return sign + text

    def _print_Pow(self, expr):
        base, exp = expr.base, expr.exp
        if base.is_Number and not self._integer_context:
            # 2 ^ x would make 2 a natural number
            base_text = '(%s : %s)' % (self._print(base), self._type)
        else:
            base_text = self.parenthesize(base, PREC_POW)
        if exp is S.Half and self._type == 'ℝ':
            return self._apply('Real.sqrt', base)
        if exp.is_Integer:
            if exp.is_negative:
                if exp == -1:
                    return '1 / %s' % self.parenthesize(base, PREC_MUL)
                return '1 / %s ^ %d' % (base_text, -exp)
            return '%s ^ %d' % (base_text, exp)
        if self._integer_context:
            return self._print_not_supported(expr)
        if exp.is_Rational:
            # A numeral exponent is a natural number unless given a type
            return '%s ^ (%d / %d : %s)' % (base_text, exp.p, exp.q,
                                            self._type)
        if exp.is_integer:
            # x ^ n with n : ℤ, which is what SymPy means for any x
            exp_text = self._in_number_context(exp, integer=True)
            if self._precedence(exp) <= PREC_POW:
                exp_text = '(%s)' % exp_text
            return '%s ^ %s' % (base_text, exp_text)
        return '%s ^ %s' % (base_text, self.parenthesize(exp, PREC_POW))

    # Functions

    def _print_Function(self, expr):
        name = expr.func.__name__
        if self._integer_context:
            return self._print_not_supported(expr)
        if name in self.known_functions:
            mapping = self.known_functions[name]
            if isinstance(mapping, str):
                return self._apply(mapping, *expr.args)
            for condition, function in mapping:
                if condition(*expr.args):
                    return self._apply(function, *expr.args)
        elif name in self._rewriteable_functions:
            target, required = self._rewriteable_functions[name]
            if self._can_print(target) and all(self._can_print(f)
                                                for f in required):
                return _bracket(self._print(expr.rewrite(target)))
        return self._print_not_supported(expr)

    def _print_AppliedUndef(self, expr):
        name = expr.func.__name__
        if name in self.known_functions or self._integer_context:
            return self._print_Function(expr)
        return self._apply(self._lean_name(name), *expr.args)

    def _can_print(self, name):
        return name in self.known_functions or name in (
            'Piecewise', 'floor', 'sqrt') or hasattr(self, '_print_' + name)

    def _print_Abs(self, expr):
        arg = self._in_number_context(expr.args[0], self._integer_context)
        if self._type == 'ℂ':
            return '(‖%s‖ : ℂ)' % arg
        return '|%s|' % arg

    def _print_floor(self, expr):
        return self._integer_part(expr, '⌊%s⌋')

    def _print_ceiling(self, expr):
        return self._integer_part(expr, '⌈%s⌉')

    def _integer_part(self, expr, notation):
        if self._type != 'ℝ':
            return self._print_not_supported(expr)
        text = notation % self._in_number_context(expr.args[0])
        if self._integer_context:
            return text
        return '(%s : ℝ)' % text

    def _print_MinMaxBase(self, expr):
        if self._type != 'ℝ' or self._integer_context:
            return self._print_not_supported(expr)
        function = 'max' if expr.func.__name__ == 'Max' else 'min'
        # max a (max b c)
        args = expr.args
        text = self._argument(args[-1])
        for arg in reversed(args[:-1]):
            text = '%s %s %s' % (function, self._argument(arg), text)
            if arg != args[0]:
                text = '(%s)' % text
        return text

    def _print_atan2(self, expr):
        if self._type != 'ℝ':
            return self._print_not_supported(expr)
        y, x = expr.args
        # atan2(y, x) is the argument of x + i y
        return 'Complex.arg ⟨%s, %s⟩' % (self._print(x), self._print(y))

    def _complex_part(self, expr, function):
        if self._type != 'ℂ':
            return self._print_not_supported(expr)
        return '(%s : ℂ)' % self._apply(function, expr.args[0])

    def _print_re(self, expr):
        return self._complex_part(expr, 'Complex.re')

    def _print_im(self, expr):
        return self._complex_part(expr, 'Complex.im')

    def _print_arg(self, expr):
        return self._complex_part(expr, 'Complex.arg')

    def _print_conjugate(self, expr):
        if self._type != 'ℂ':
            return self._print_not_supported(expr)
        return self._apply('(starRingEnd ℂ)', expr.args[0])

    # Calculus

    def _function_of(self, variables, body):
        """Print the function that maps the variables to body."""
        if len(variables) == 1:
            v = variables[0]
            binders = '%s : %s' % (self._print_binder(v), self._binder_type(v))
        else:
            binders = ' '.join('(%s : %s)' % (self._print_binder(v),
                                              self._binder_type(v))
                               for v in variables)
        return 'fun %s ↦ %s' % (binders, body)

    def _print_binder(self, symbol):
        return self._lean_name(symbol.name)

    def _print_Lambda(self, expr):
        if not all(isinstance(v, Symbol) for v in expr.variables):
            return self._print_not_supported(expr)
        return self._function_of(expr.variables, self._print(expr.expr))

    def _print_Derivative(self, expr):
        text = self._print(expr.expr)
        for variable, count in expr.variable_count:
            if not isinstance(variable, Symbol) or variable.is_integer or \
                    not count.is_Integer:
                return self._print_not_supported(expr)
            function = self._function_of([variable], text)
            if count == 1:
                text = 'deriv (%s) %s' % (function, self._print(variable))
            else:
                text = 'iteratedDeriv %d (%s) %s' % (
                    count, function, self._print(variable))
        return text

    def _print_Subs(self, expr):
        if not all(isinstance(v, Symbol) for v in expr.variables):
            return self._print_not_supported(expr)
        function = self._function_of(expr.variables, self._print(expr.expr))
        return ' '.join(['(%s)' % function] +
                        [self._argument(p) for p in expr.point])

    def _print_Integral(self, expr):
        if self._type != 'ℝ' or not all(len(limit) == 3 and all(
                b.is_infinite is not True for b in limit[1:])
                for limit in expr.limits):
            return self._print_not_supported(expr)
        text = self._print(expr.function)
        for variable, lower, upper in expr.limits:
            lower_text = self._print(lower)
            if not self._is_typed(lower):
                lower_text = self._ascribe(lower_text)
            text = '∫ %s in %s..%s, %s' % (
                self._print_binder(variable),
                self._bound(lower, lower_text), self._bound(upper), text)
        return self._binder_like(expr, text)

    def _bound(self, expr, text=None):
        text = self._print(expr) if text is None else text
        if self._precedence(expr) < PREC_ATOM and not text.startswith('('):
            return '(%s)' % text
        return text

    def _print_Sum(self, expr):
        return self._big_operator(expr, '∑')

    def _print_Product(self, expr):
        return self._big_operator(expr, '∏')

    def _big_operator(self, expr, symbol):
        if not all(b.is_integer and b.is_finite for limit in expr.limits
                   for b in limit[1:]):
            return self._print_not_supported(expr)
        variables = {limit[0] for limit in expr.limits}
        saved = self._integer_variables
        self._integer_variables = saved | variables
        try:
            text = self._in_number_context(expr.function)
            for variable, lower, upper in expr.limits:
                lower_text = self._in_number_context(lower, integer=True)
                if lower.is_Number:
                    lower_text = '(%s : ℤ)' % lower_text
                upper_text = self._in_number_context(upper, integer=True)
                text = '%s %s ∈ Finset.Icc %s %s, %s' % (
                    symbol, self._print_binder(variable),
                    self._bound(lower, lower_text),
                    self._bound(upper, upper_text), text)
        finally:
            self._integer_variables = saved
        return self._binder_like(expr, text)

    # Logic

    def _print_Relational(self, expr):
        operators = {'==': '=', '!=': '≠', '<': '<', '<=': '≤', '>': '>',
                     '>=': '≥'}
        if expr.rel_op not in operators:
            return self._print_not_supported(expr)
        lhs = self.parenthesize(expr.lhs, PREC_REL)
        rhs = self.parenthesize(expr.rhs, PREC_REL)
        if not self._is_typed(expr.lhs) and not self._is_typed(expr.rhs):
            lhs = self._ascribe(lhs)
        return '%s %s %s' % (lhs, operators[expr.rel_op], rhs)

    def _print_BooleanTrue(self, expr):
        return 'True'

    def _print_BooleanFalse(self, expr):
        return 'False'

    def _print_And(self, expr):
        return ' ∧ '.join(self.parenthesize(a, PREC_AND)
                          for a in sorted(expr.args, key=default_sort_key))

    def _print_Or(self, expr):
        return ' ∨ '.join(self.parenthesize(a, PREC_OR)
                          for a in sorted(expr.args, key=default_sort_key))

    def _print_Not(self, expr):
        return '¬' + self.parenthesize(expr.args[0], PREC_NOT, strict=True)

    def _print_Implies(self, expr):
        return '%s → %s' % (self.parenthesize(expr.args[0], PREC_IMPLIES),
                            self.parenthesize(expr.args[1], PREC_IMPLIES))

    def _print_Equivalent(self, expr):
        args = expr.args
        if len(args) == 2:
            return '%s ↔ %s' % (self.parenthesize(args[0], PREC_IFF),
                                self.parenthesize(args[1], PREC_IFF))
        # all arguments are equivalent
        return ' ∧ '.join('(%s ↔ %s)' % (self.parenthesize(a, PREC_IFF),
                                         self.parenthesize(b, PREC_IFF))
                          for a, b in zip(args, args[1:]))

    def _print_ITE(self, expr):
        c, a, b = expr.args
        return 'if %s then %s else %s' % (self._print(c), self._print(a),
                                          self._print(b))

    def _print_Piecewise(self, expr):
        if expr.args[-1].cond != True:
            # The expression is undefined where no condition holds
            return self._print_not_supported(expr)
        text = self._print(expr.args[-1].expr)
        for e, c in reversed(expr.args[:-1]):
            text = 'if %s then %s else %s' % (
                self._print(c), self.parenthesize(e, PREC_BINDER), text)
        return self._binder_like(expr, text)

    # Matrices

    def _print_MatrixBase(self, expr):
        if 0 in expr.shape:
            return self._print_not_supported(expr)
        return '!![%s]' % '; '.join(
            ', '.join(self.parenthesize(e, PREC_BINDER) for e in expr.row(i))
            for i in range(expr.rows))

    def _print_MatrixSymbol(self, expr):
        return self._lean_name(expr.name)

    def _matrix_type(self, expr):
        if not all(d.is_Integer for d in expr.shape):
            return None
        return 'Matrix (Fin %s) (Fin %s) %s' % (expr.rows, expr.cols,
                                                self._type)

    def _print_Identity(self, expr):
        matrix_type = self._matrix_type(expr)
        if matrix_type is None:
            return self._print_not_supported(expr)
        return '(1 : %s)' % matrix_type

    def _print_ZeroMatrix(self, expr):
        matrix_type = self._matrix_type(expr)
        if matrix_type is None:
            return self._print_not_supported(expr)
        return '(0 : %s)' % matrix_type

    def _print_MatAdd(self, expr):
        terms = [self.parenthesize(t, PREC_ADD) for t in expr.args]
        text = terms[0]
        for term in terms[1:]:
            if term.startswith('-'):
                text += ' - ' + term[1:]
            else:
                text += ' + ' + term
        return text

    def _print_MatMul(self, expr):
        coeff, matrices = expr.as_coeff_matrices()
        sign = ''
        if coeff.could_extract_minus_sign():
            coeff, sign = -coeff, '-'
        text = ' * '.join(self.parenthesize(m, PREC_MUL) for m in matrices)
        if coeff != 1:
            # A numeral scalar would be a natural number
            scalar = self._print(coeff)
            if not self._is_typed(coeff):
                scalar = self._ascribe(scalar)
            elif self._precedence(coeff) < PREC_ATOM:
                scalar = '(%s)' % scalar
            text = '%s • %s' % (scalar, text)
        return sign + text

    def _print_MatPow(self, expr):
        base, exp = expr.args
        if not exp.is_Integer:
            return self._print_not_supported(expr)
        base_text = self.parenthesize(base, PREC_POW)
        if exp.is_negative:
            return '%s⁻¹ ^ %d' % (self._postfix_operand(base), -exp)
        return '%s ^ %d' % (base_text, exp)

    def _postfix_operand(self, expr):
        return self.parenthesize(expr, PREC_ATOM, strict=True)

    def _print_Inverse(self, expr):
        return '%s⁻¹' % self._postfix_operand(expr.arg)

    def _print_Transpose(self, expr):
        return '%s.transpose' % self._postfix_operand(expr.arg)

    def _print_Determinant(self, expr):
        return '%s.det' % self._postfix_operand(expr.arg)

    def _print_Trace(self, expr):
        return '%s.trace' % self._postfix_operand(expr.arg)

    def _print_MatrixElement(self, expr):
        if not all(i.is_Integer or isinstance(i, Symbol)
                   for i in (expr.i, expr.j)):
            return self._print_not_supported(expr)
        return '%s %s %s' % (self._postfix_operand(expr.parent),
                             self._print(expr.i), self._print(expr.j))

    # Containers

    def _print_tuple(self, expr):
        if len(expr) == 1:
            return self._print(expr[0])
        return '(%s)' % ', '.join(self._print(e) for e in expr)

    _print_Tuple = _print_tuple

    def _print_list(self, expr):
        return '[%s]' % ', '.join(self._print(e) for e in expr)


def _bracket(text):
    """Put text in parentheses unless it is in parentheses already."""
    if text.startswith('('):
        depth = 0
        for k, c in enumerate(text):
            depth += {'(': 1, ')': -1}.get(c, 0)
            if depth == 0:
                if k == len(text) - 1:
                    return text
                break
    return '(%s)' % text


def lean_code(expr, **settings):
    r"""Convert a SymPy expression to a term of Lean 4 with Mathlib.

    Parameters
    ==========

    expr : Expr, Boolean or Matrix
        The expression to convert.
    number_type : str, optional
        ``'real'`` (the default) for terms of type ``ℝ`` or ``'complex'`` for
        terms of type ``ℂ``.
    user_functions : dict, optional
        A dictionary whose keys are the names of SymPy functions and whose
        values are the names of the Lean functions to print instead, or lists
        of ``(argument_test, lean_name)`` tuples.
    strict : bool, optional
        If True (the default), raise an error for an expression that can't be
        printed. If False, print it as SymPy would and list it in a comment.

    Examples
    ========

    >>> from sympy import lean_code, symbols, sin, sqrt, Integral, Eq, S
    >>> x, y = symbols('x y')
    >>> lean_code(sin(x)**2 + sqrt(y)/2)
    'Real.sqrt y / 2 + Real.sin x ^ 2'
    >>> lean_code(Eq(Integral(x**2, (x, 0, 1)), 1/S(3)))
    '(∫ x in (0 : ℝ)..1, x ^ 2) = 1 / 3'

    Variables are printed as they are, so a statement that uses the term has
    to declare them, with the type ``ℝ`` (or ``ℂ``). Variables that are
    integers (``integer=True``) are cast, so they can be declared as ``ℤ``:

    >>> n = symbols('n', integer=True)
    >>> lean_code(x**n + n)
    '(n : ℝ) + x ^ n'

    An undefined function is applied like any Lean function, so ``f`` can be
    declared as ``f : ℝ → ℝ``:

    >>> from sympy import Function
    >>> f = Function('f')
    >>> lean_code(f(x).diff(x))
    'deriv (fun x : ℝ ↦ f x) x'

    A term made only of numbers gets a type, since Lean would make it a
    natural number:

    >>> from sympy import Rational
    >>> lean_code(Rational(1, 2))
    '(1 / 2 : ℝ)'

    With ``number_type='complex'``, the functions are Mathlib's complex
    functions:

    >>> from sympy import I, exp, log
    >>> z = symbols('z')
    >>> lean_code(exp(I*z) + log(z), number_type='complex')
    'Complex.exp (Complex.I * z) + Complex.log z'

    Lean's functions are defined everywhere, while SymPy's need not be, so a
    printed term has the value of the SymPy expression only where that is
    defined and of the printed type:

    - Division by zero is 0, and so are ``Real.log 0`` and ``Real.sqrt x``
      for a negative ``x``; ``Real.log x`` is ``Real.log |x|``.
    - ``Real.arcsin``, ``Real.arccos`` and the other inverse functions return
      some value outside their domain.
    - ``x ^ (1 / 3 : ℝ)`` for a negative ``x`` is a real number, whereas
      SymPy's is the complex principal root.
    - ``deriv`` is 0 where the function isn't differentiable, and an
      integral is 0 if the function isn't integrable.
    - A sum or product whose upper limit is less than its lower limit is
      empty (0 or 1), whereas SymPy follows Karr's convention.

    """
    return LeanPrinter(settings).doprint(expr)

