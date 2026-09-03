from __future__ import annotations
from collections import defaultdict

from sympy.assumptions.ask import Q
from sympy.assumptions.assume import AppliedPredicate
from sympy.core import (Add, Mul, Pow, Number, NumberSymbol, Symbol)
from sympy.core.kind import NumberKind, UndefinedKind
from sympy.core.numbers import ImaginaryUnit
from sympy.core.singleton import S
from sympy.functions.elementary.complexes import Abs
from sympy.logic.algorithms.lra_theory import LRA_PRED, lra_ne
from sympy.logic.boolalg import (Equivalent, And, Or, Implies)
from sympy.matrices.expressions import MatMul

# APIs here may be subject to change


### Helper functions ###

def allargs(symbol, fact, expr):
    """
    Apply all arguments of the expression to the fact structure.

    Parameters
    ==========

    symbol : Symbol
        A placeholder symbol.

    fact : Boolean
        Resulting ``Boolean`` expression.

    expr : Expr

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.assumptions.sathandlers import allargs
    >>> from sympy.abc import x, y
    >>> allargs(x, Q.negative(x) | Q.positive(x), x*y)
    (Q.negative(x) | Q.positive(x)) & (Q.negative(y) | Q.positive(y))

    """
    return And(*[fact.subs(symbol, arg) for arg in expr.args])


def anyarg(symbol, fact, expr):
    """
    Apply any argument of the expression to the fact structure.

    Parameters
    ==========

    symbol : Symbol
        A placeholder symbol.

    fact : Boolean
        Resulting ``Boolean`` expression.

    expr : Expr

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.assumptions.sathandlers import anyarg
    >>> from sympy.abc import x, y
    >>> anyarg(x, Q.negative(x) & Q.positive(x), x*y)
    (Q.negative(x) & Q.positive(x)) | (Q.negative(y) & Q.positive(y))

    """
    return Or(*[fact.subs(symbol, arg) for arg in expr.args])


def exactlyonearg(symbol, fact, expr):
    """
    Apply exactly one argument of the expression to the fact structure.

    Parameters
    ==========

    symbol : Symbol
        A placeholder symbol.

    fact : Boolean
        Resulting ``Boolean`` expression.

    expr : Expr

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.assumptions.sathandlers import exactlyonearg
    >>> from sympy.abc import x, y
    >>> exactlyonearg(x, Q.positive(x), x*y)
    (Q.positive(x) & ~Q.positive(y)) | (Q.positive(y) & ~Q.positive(x))

    """
    pred_args = [fact.subs(symbol, arg) for arg in expr.args]
    res = Or(*[And(pred_args[i], *[~lit for lit in pred_args[:i] +
        pred_args[i+1:]]) for i in range(len(pred_args))])
    return res


### Fact registry ###

class ClassFactRegistry:
    """
    Register handlers against classes.

    Explanation
    ===========

    ``register`` method registers the handler function for a class. Here,
    handler function should return a single fact. ``multiregister`` method
    registers the handler function for multiple classes. Here, handler function
    should return a container of multiple facts.

    ``registry(expr)`` returns a set of facts for *expr*.

    Examples
    ========

    Here, we register the facts for ``Abs``.

    >>> from sympy import Abs, Equivalent, Q
    >>> from sympy.assumptions.sathandlers import ClassFactRegistry
    >>> reg = ClassFactRegistry()
    >>> @reg.register(Abs)
    ... def f1(expr):
    ...     return Q.nonnegative(expr)
    >>> @reg.register(Abs)
    ... def f2(expr):
    ...     arg = expr.args[0]
    ...     return Equivalent(~Q.zero(arg), ~Q.zero(expr))

    Calling the registry with expression returns the defined facts for the
    expression.

    >>> from sympy.abc import x
    >>> reg(Abs(x))
    {Q.nonnegative(Abs(x)), Equivalent(~Q.zero(x), ~Q.zero(Abs(x)))}

    Multiple facts can be registered at once by ``multiregister`` method.

    >>> reg2 = ClassFactRegistry()
    >>> @reg2.multiregister(Abs)
    ... def _(expr):
    ...     arg = expr.args[0]
    ...     return [Q.even(arg) >> Q.even(expr), Q.odd(arg) >> Q.odd(expr)]
    >>> reg2(Abs(x))
    {Implies(Q.even(x), Q.even(Abs(x))), Implies(Q.odd(x), Q.odd(Abs(x)))}

    """
    def __init__(self):
        self.singlefacts = defaultdict(frozenset)
        self.multifacts = defaultdict(frozenset)

    def register(self, cls):
        def _(func):
            self.singlefacts[cls] |= {func}
            return func
        return _

    def multiregister(self, *classes):
        def _(func):
            for cls in classes:
                self.multifacts[cls] |= {func}
            return func
        return _

    def __getitem__(self, key):
        ret1 = self.singlefacts[key]
        for k in self.singlefacts:
            if issubclass(key, k):
                ret1 |= self.singlefacts[k]

        ret2 = self.multifacts[key]
        for k in self.multifacts:
            if issubclass(key, k):
                ret2 |= self.multifacts[k]

        return ret1, ret2

    def __call__(self, expr):
        ret = set()

        handlers1, handlers2 = self[type(expr)]

        ret.update(h(expr) for h in handlers1)
        for h in handlers2:
            ret.update(h(expr))
        return ret

class_fact_registry = ClassFactRegistry()


### Arithmetic facts ###

# Every predicate that has a reading as real arithmetic, as the relation it
# becomes and the right-hand side to read it against. A sign predicate is a
# relation against zero, which is all there is to say about one.
_ARITHMETIC_READING = {
    Q.eq: (Q.eq, None), Q.lt: (Q.lt, None), Q.gt: (Q.gt, None),
    Q.le: (Q.le, None), Q.ge: (Q.ge, None), Q.ne: (Q.ne, None),

    Q.positive: (Q.gt, S.Zero), Q.negative: (Q.lt, S.Zero),
    Q.zero: (Q.eq, S.Zero), Q.nonzero: (Q.ne, S.Zero),
    Q.nonpositive: (Q.le, S.Zero), Q.nonnegative: (Q.ge, S.Zero),

    # The extended predicates admit +-oo, which the guard below rules out, so
    # under it they say exactly what their plain counterparts say. They are
    # here because a query reaches them anyway: `ask(Q.eq(x, y), ...)` becomes
    # `Q.zero(x - y)`, whose negation the known facts state as
    # `Q.extended_nonzero(x - y)`, and that is the atom the theory refutes.
    Q.extended_positive: (Q.gt, S.Zero),
    Q.extended_negative: (Q.lt, S.Zero),
    Q.extended_nonpositive: (Q.le, S.Zero),
    Q.extended_nonnegative: (Q.ge, S.Zero),
    Q.extended_nonzero: (Q.ne, S.Zero),
}


def arithmetic_facts(pred):
    """Return the bridge from *pred* to the theory's own atoms, or ``()``.

    Explanation
    ===========

    ``Q.gt(x, 1)`` and ``lra_gt(x, 1)`` are not the same claim: the first
    holds of ``oo`` and the second says ``x - 1`` is a positive real number.
    The fact tying them together is therefore stated under a guard saying
    that the sides are real, which is what leaves ``Q.gt(x, 1)`` with
    ``Q.imaginary(x)``, and ``Q.gt(I, 1)``, opaque to the theory.

    Examples
    ========

    >>> from sympy import Q
    >>> from sympy.abc import x
    >>> from sympy.assumptions.sathandlers import arithmetic_facts
    >>> arithmetic_facts(Q.positive(x))
    (Implies(Q.real(x), Equivalent(Q.positive(x), lra_gt(x, 0))),)
    >>> arithmetic_facts(Q.prime(x))
    ()

    """
    if not isinstance(pred, AppliedPredicate):
        return ()
    reading = _ARITHMETIC_READING.get(pred.function)
    if reading is None:
        return ()

    relation, rhs = reading
    if rhs is None:
        lhs, rhs = pred.arguments
    else:
        lhs = pred.arguments[0]

    guard = _arithmetic_realness_guard(lhs, rhs)
    if guard is None:
        return ()
    # A disequality is not a bound, so the theory reads it as a disjunction;
    # `lra_ne` is where that rule is written down.
    arithmetic = lra_ne(lhs, rhs) if relation is Q.ne else LRA_PRED[relation](lhs, rhs)
    # One fact, and only this one.  `assert_lit` has no single bound to assert
    # for a negated equality and so ignores one; saying the negation separately
    # as `Equivalent(~pred, lra_ne(lhs, rhs))` would tell the theory about it,
    # but it gives every equality two more atoms for the search to assign, and
    # `ask(Q.eq(x, z), Q.eq(x, y) & Q.eq(y, z))` goes from 0.1s to minutes.
    return (Implies(guard, Equivalent(pred, arithmetic)),)


def _arithmetic_realness_guard(*sides):
    """The realness condition under which *sides* can be read by LRA.

    ``None`` means that the predicate has no arithmetic interpretation. A
    side known real does not need a guard; a side known non-real must never be
    handed to the real-arithmetic theory.
    """
    guards = []
    for side in sides:
        # UndefinedKind is included until every scalar expression has a more
        # precise kind (for example, Abs(x) and sin(x)).
        if side.kind not in (NumberKind, UndefinedKind) or side is S.NaN:
            return None
        if side.is_real is False:
            return None
        if side.is_real is not True:
            guards.append(Q.real(side))
    return And(*guards)


### Class fact registration ###

x = Symbol('x')

## Abs ##

@class_fact_registry.multiregister(Abs)
def _(expr):
    arg = expr.args[0]
    return [Q.nonnegative(expr),
            Equivalent(~Q.zero(arg), ~Q.zero(expr)),
            Q.even(arg) >> Q.even(expr),
            Q.odd(arg) >> Q.odd(expr),
            Q.integer(arg) >> Q.integer(expr),
            ]


### Add ##

@class_fact_registry.multiregister(Add)
def _(expr):
    return [allargs(x, Q.positive(x), expr) >> Q.positive(expr),
            allargs(x, Q.negative(x), expr) >> Q.negative(expr),
            allargs(x, Q.real(x), expr) >> Q.real(expr),
            allargs(x, Q.rational(x), expr) >> Q.rational(expr),
            allargs(x, Q.integer(x), expr) >> Q.integer(expr),
            exactlyonearg(x, ~Q.integer(x), expr) >> ~Q.integer(expr),
            ]

@class_fact_registry.register(Add)
def _(expr):
    allargs_real = allargs(x, Q.real(x), expr)
    onearg_irrational = exactlyonearg(x, Q.irrational(x), expr)
    return Implies(allargs_real, Implies(onearg_irrational, Q.irrational(expr)))


### Mul ###

@class_fact_registry.multiregister(Mul)
def _(expr):
    return [Equivalent(Q.zero(expr), anyarg(x, Q.zero(x), expr)),
            allargs(x, Q.positive(x), expr) >> Q.positive(expr),
            allargs(x, Q.real(x), expr) >> Q.real(expr),
            allargs(x, Q.rational(x), expr) >> Q.rational(expr),
            allargs(x, Q.integer(x), expr) >> Q.integer(expr),
            (allargs(x, ~Q.zero(x), expr) &
             exactlyonearg(x, ~Q.rational(x), expr)) >> ~Q.integer(expr),
            allargs(x, Q.commutative(x), expr) >> Q.commutative(expr),
            ]

@class_fact_registry.register(Mul)
def _(expr):
    # Implicitly assumes Mul has more than one arg
    # Would be allargs(x, Q.prime(x) | Q.composite(x)) except 1 is composite
    # More advanced prime assumptions will require inequalities, as 1 provides
    # a corner case.
    allargs_prime = allargs(x, Q.prime(x), expr)
    return Implies(allargs_prime, ~Q.prime(expr))

@class_fact_registry.register(Mul)
def _(expr):
    # General Case: Odd number of imaginary args implies mul is imaginary(To be implemented)
    allargs_imag_or_real = allargs(x, Q.imaginary(x) | Q.real(x), expr)
    allargs_not_zero = allargs(x, ~Q.zero(x), expr)
    onearg_imaginary = exactlyonearg(x, Q.imaginary(x), expr)
    return Implies(allargs_imag_or_real & allargs_not_zero, Implies(onearg_imaginary, Q.imaginary(expr)))

@class_fact_registry.register(Mul)
def _(expr):
    allargs_real = allargs(x, Q.real(x), expr)
    onearg_irrational = exactlyonearg(x, Q.irrational(x), expr)
    return Implies(allargs_real & allargs(x, ~Q.zero(x), expr),
                    Implies(onearg_irrational, Q.irrational(expr)))

@class_fact_registry.register(Mul)
def _(expr):
    # Including the integer qualification means we don't need to add any facts
    # for odd, since the assumptions already know that every integer is
    # exactly one of even or odd.
    allargs_integer = allargs(x, Q.integer(x), expr)
    anyarg_even = anyarg(x, Q.even(x), expr)
    return Implies(allargs_integer, Equivalent(anyarg_even, Q.even(expr)))


### MatMul ###

@class_fact_registry.register(MatMul)
def _(expr):
    allargs_square = allargs(x, Q.square(x), expr)
    allargs_invertible = allargs(x, Q.invertible(x), expr)
    return Implies(allargs_square, Equivalent(Q.invertible(expr), allargs_invertible))


### Pow ###

@class_fact_registry.multiregister(Pow)
def _(expr):
    base, exp = expr.base, expr.exp
    return [
        (Q.real(base) & Q.even(exp) & Q.nonnegative(exp)) >> Q.nonnegative(expr),
        (Q.nonnegative(base) & Q.odd(exp) & Q.nonnegative(exp)) >> Q.nonnegative(expr),
        (Q.nonpositive(base) & Q.odd(exp) & Q.nonnegative(exp)) >> Q.nonpositive(expr),
        Equivalent(Q.zero(expr), Q.zero(base) & Q.positive(exp))
    ]


### Numbers ###

_old_assump_getters = {
    Q.positive: lambda o: o.is_positive,
    Q.zero: lambda o: o.is_zero,
    Q.negative: lambda o: o.is_negative,
    Q.rational: lambda o: o.is_rational,
    Q.irrational: lambda o: o.is_irrational,
    Q.even: lambda o: o.is_even,
    Q.odd: lambda o: o.is_odd,
    Q.imaginary: lambda o: o.is_imaginary,
    Q.prime: lambda o: o.is_prime,
    Q.composite: lambda o: o.is_composite,
}

@class_fact_registry.multiregister(Number, NumberSymbol, ImaginaryUnit)
def _(expr):
    ret = []
    for p, getter in _old_assump_getters.items():
        pred = p(expr)
        prop = getter(expr)
        if prop is not None:
            ret.append(Equivalent(pred, prop))
    return ret
