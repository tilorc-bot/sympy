"""The rules about expressions as the first step of ``expr.is_<fact>``."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sympy.assumptions.ask import Q
from sympy.assumptions.ask_rules_generated import RULES
from sympy.assumptions.number_facts import EVALUATED, number_facts
from sympy.assumptions.rule_engine import _RuleEngine, _UnaryFactsEngine
from sympy.core.add import Add
from sympy.core.assumptions import _assume_defined, _set_ask_rules
from sympy.core.logic import fuzzy_and
from sympy.core.mul import Mul
from sympy.core.power import Pow
from sympy.core.singleton import S

if TYPE_CHECKING:
    from collections.abc import Iterator

    from sympy.assumptions.assume import Predicate
    from sympy.assumptions.number_facts import Facts
    from sympy.assumptions.rule_engine import Rule, Rules
    from sympy.core.basic import Basic

_SIGN_OF_INFINITY = {
    Q.positive_infinite: 'is_extended_positive',
    Q.negative_infinite: 'is_extended_negative',
}
_OPPOSITE = {Q.finite: Q.infinite, Q.infinite: Q.finite}


class _CoreRuleEngine(_RuleEngine):
    """
    The search of the rule engine where a question about an argument is
    ``arg.is_<fact>``: what is known of an expression is what the old
    assumptions hold of it, and a question which the rules leave open goes on
    to the ``_eval_is_<fact>`` handlers.
    """

    def __init__(self, rules: Rules):
        self.rules = rules
        self.unary_facts_engine = _UnaryFactsEngine({})
        where_true = self.unary_facts_engine.where_true
        self.predicates: dict[str, Predicate] = {}
        for fact in _assume_defined:
            predicate = getattr(Q, fact, None)
            if predicate is not None and predicate in where_true:
                self.predicates[fact] = predicate
        self.attributes: dict[Predicate | Basic, str] = {
            predicate: 'is_' + fact for fact, predicate in self.predicates.items()}
        self.attributes[Q.hermitian] = 'is_hermitian'
        self.attributes[Q.antihermitian] = 'is_antihermitian'
        self.handlers: dict[Predicate | Basic, str] = {
            predicate: '_eval_is_' + fact for fact, predicate in self.predicates.items()}
        self.class_rules: dict[tuple[type, Predicate | Basic], tuple[Rule, ...]] = {}

    def ask(self, fact: str, obj: Any) -> bool | None:
        """``obj.is_<fact>`` from the facts of a number and from the rules."""
        predicate = self.predicates.get(fact)
        if predicate is None:
            return None
        known = obj._assumptions
        if not known.number_facts_tried:
            known.number_facts_tried = True
            if obj.args and _is_evaluated_number(obj):
                facts = number_facts(obj)
                if facts:
                    known.deduce_all_facts(list(self._decided(facts)))
                    value = known.get(fact)
                    if value is not None:
                        return value
        value = self._from_rules(predicate, obj)
        if value is False and predicate in _OPPOSITE:
            # for the rules an expression can be neither finite nor infinite
            value = False if self._from_rules(_OPPOSITE[predicate], obj) else None
        if value is not None and predicate is not Q.commutative and _may_be_nan(obj):
            return None
        return value

    def _decided(self, facts: Facts) -> Iterator[tuple[str, bool]]:
        """Every fact of the old assumptions which *facts* decide."""
        where_true = self.unary_facts_engine.where_true
        known: list[tuple[Predicate | Basic, bool]] = list(facts)
        possible = self.unary_facts_engine._possible(known)
        for fact, predicate in self.predicates.items():
            common = possible & where_true[predicate]
            if common == possible:
                yield fact, True
            elif not common:
                yield fact, False

    def visit(self, predicate: Predicate | Basic, expr: Basic) -> bool | None:
        attribute = self.attributes.get(predicate)
        if attribute is not None:
            return getattr(expr, attribute, None)
        attribute = _SIGN_OF_INFINITY.get(predicate)
        if attribute is not None:
            return fuzzy_and((getattr(expr, 'is_infinite', None),
                              getattr(expr, attribute, None)))
        if expr is predicate:
            return True
        if getattr(expr, 'is_Rational', False):
            return False
        return self._from_rules(predicate, expr)

    def _from_rules(self, predicate: Predicate | Basic, expr: Basic) -> bool | None:
        cls = type(expr)
        rules = self.class_rules.get((cls, predicate))
        if rules is None:
            rules = self.class_rules[cls, predicate] = self._rules_of(cls, predicate)
        for kind, conditions in rules:
            answer = self._apply(kind, conditions, expr)
            if answer is not None:
                return answer
        return None

    def _rules_of(self, cls: type, predicate: Predicate | Basic) -> tuple[Rule, ...]:
        """
        The rules for *predicate* of *cls* and of its base classes, unless a
        class between has a handler for it and no rules.
        """
        handler = self.handlers.get(predicate)
        found: list[Rule] = []
        for base in cls.__mro__:
            rules = self.rules.get((base, predicate))
            if rules:
                found += rules
            elif not found and handler in base.__dict__:
                break
        return tuple(found)


def _may_be_nan(expr: Basic) -> bool:
    """
    Whether an expression has the argument ``nan``, or is a sum, a product
    or a power which may be ``nan`` for what is known of its arguments
    (``0*oo``, ``oo - oo``, ``1**oo``, ``0**I``, ``oo**I``). Nothing is said
    of such an expression: the rules answer ``False`` where
    ``nan.is_<fact>`` is ``None``.
    """
    args = expr.args
    if any(arg is S.NaN for arg in args):
        return True
    if isinstance(expr, Mul):
        zero = [arg for arg in args if getattr(arg, 'is_zero', None) is not False]
        if not zero:
            return False
        infinite = [arg for arg in args if getattr(arg, 'is_finite', None) is not True]
        if not infinite:
            return False
        return len(zero) > 1 or len(infinite) > 1 or zero[0] is not infinite[0]
    if isinstance(expr, Add):
        infinite = [arg for arg in args if getattr(arg, 'is_finite', None) is not True]
        if len(infinite) < 2:
            return False
        return not (all(arg.is_extended_nonnegative for arg in infinite)
                    or all(arg.is_extended_nonpositive for arg in infinite))
    if isinstance(expr, Pow):
        base, exponent = args
        if exponent.is_finite is not True:
            return True
        if exponent.is_extended_real:
            return False
        return base.is_zero is not False or base.is_finite is not True
    return False


def _is_evaluated_number(expr: Basic) -> bool:
    return type(expr) in EVALUATED and all(map(_is_evaluated_number, expr.args))


_set_ask_rules(_CoreRuleEngine(RULES).ask)
