"""Offline steps which turn the table of rules into the one which is read at run time."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.ask_generated import get_known_facts_dict
from sympy.assumptions.rule_checks import check_no_cycles
from sympy.assumptions.rule_engine import (ALL_ARGS, ALL_ARGS_BUT_AT_MOST_ONE,
    ANY_ARG, EVEN_NUMBER_OF_ARGS, FALSE_IF, FIRST_ARG_IS, IF_AND_ONLY_IF, ODD_NUMBER_OF_ARGS,
    ONE_ARG, OTHER_ARGS, OTHER_ARGS_BUT_AT_MOST_ONE, SELF, SOME_EVEN_NUMBER_OF_ARGS, SOME_ODD_NUMBER_OF_ARGS,
    TRUE_IF)
from sympy.core.power import Pow
from sympy.core.singleton import S
from sympy.functions.elementary.exponential import exp

if TYPE_CHECKING:
    from sympy.assumptions.rule_engine import Condition, Rule, Rules

_HOW_MANY_ARGS = (ONE_ARG, EVEN_NUMBER_OF_ARGS, ODD_NUMBER_OF_ARGS, OTHER_ARGS,
                  SOME_EVEN_NUMBER_OF_ARGS, SOME_ODD_NUMBER_OF_ARGS,
                  OTHER_ARGS_BUT_AT_MOST_ONE)
# about the arguments which the counting condition before them left
_OTHER_ARGS = (OTHER_ARGS, OTHER_ARGS_BUT_AT_MOST_ONE)
# a condition about these cannot be negated by another condition
_NOT_FLIPPABLE = _HOW_MANY_ARGS + (ALL_ARGS_BUT_AT_MOST_ONE,)
_FLIPPED_ARGUMENT = {ALL_ARGS: ANY_ARG, ANY_ARG: ALL_ARGS}


def close_rules(rules: Rules) -> Rules:
    """Repeat each rule about arguments for every predicate its conclusion decides."""
    facts = get_known_facts_dict()
    plain = {key: [new_rule for rule in rules_for_key
                   for new_rule in _without_if_and_only_if(rule)]
             for key, rules_for_key in rules.items()}
    closed = {key: list(rules_for_key) for key, rules_for_key in plain.items()}
    for (cls, predicate), rules_for_key in sorted(plain.items(),
                                                  key=lambda item: str(item[0][1])):
        if predicate not in facts:
            # a number: its rules are about the expression itself
            continue
        implied, excluded = facts[predicate]
        implying = [q for q, (implied_by_q, _) in facts.items()
                    if predicate in implied_by_q]
        for kind, conditions in rules_for_key:
            if any(argument == SELF for (argument, _), _ in conditions):
                continue
            if kind == TRUE_IF:
                added = [(q, TRUE_IF) for q in sorted(implied, key=str)]
                added += [(q, FALSE_IF) for q in sorted(excluded, key=str)]
            else:
                added = [(q, FALSE_IF) for q in sorted(implying, key=str)]
            for q, new_kind in added:
                closed.setdefault((cls, q), []).append((new_kind, list(conditions)))
    result: Rules = {}
    for key, rules_for_key in closed.items():
        kept: list[Rule] = []
        for rule in rules_for_key:
            if rule not in kept:
                kept.append(rule)
        result[key] = kept
    check_no_cycles(result)
    return result


def remove_implied_rules(rules: Rules) -> Rules:
    """
    Remove each rule which applies only where another rule of the same kind applies.

    Meant for a table from :func:`close_rules`, in which whenever the rules find
    ``q`` of an expression they also find each ``p`` which ``q`` implies or excludes.
    """
    facts = get_known_facts_dict()
    result: Rules = {}
    for key, rules_for_key in rules.items():
        if any(kind == IF_AND_ONLY_IF for kind, _ in rules_for_key):
            raise ValueError('IF_AND_ONLY_IF rules cannot be compared')
        groups = [(kind, _groups(conditions)) for kind, conditions in rules_for_key]
        result[key] = [
            rule for j, rule in enumerate(rules_for_key)
            if not any(
                i != j and _applies_whenever(groups[i], groups[j], facts)
                and (i < j or not _applies_whenever(groups[j], groups[i], facts))
                for i in range(len(groups)))
        ]
    return result


def exp_rules_for_powers(rules: Rules) -> Rules:
    """Repeat each rule of ``exp`` for ``Pow`` with the base ``E``."""
    result = {key: list(rules_for_key) for key, rules_for_key in rules.items()}
    for (cls, predicate), rules_for_key in rules.items():
        if cls is exp:
            result.setdefault((Pow, predicate), []).extend(
                (kind, [(FIRST_ARG_IS, S.Exp1)] + [
                    ((1 if argument == 0 else argument, expected), condition)
                    for (argument, expected), condition in conditions])
                for kind, conditions in rules_for_key)
    return result


def _without_if_and_only_if(rule: Rule) -> list[Rule]:
    kind, conditions = rule
    if kind != IF_AND_ONLY_IF:
        return [rule]
    if any(argument in _NOT_FLIPPABLE for (argument, _), _ in conditions):
        raise ValueError('IF_AND_ONLY_IF with a condition about how many'
                         ' arguments have a predicate is not supported')
    flipped = [((_FLIPPED_ARGUMENT.get(argument, argument), not expected), predicate)
               for (argument, expected), predicate in conditions]
    return [(TRUE_IF, conditions)] + [(FALSE_IF, [condition]) for condition in flipped]


def _groups(conditions: list[Condition]) -> list[tuple[Condition, ...]]:
    """Each condition alone, except OTHER_ARGS with the condition it refers to."""
    groups: list[tuple[Condition, ...]] = []
    how_many = None
    for condition in conditions:
        argument = condition[0][0]
        if argument in _OTHER_ARGS and how_many is not None:
            groups[how_many] += (condition,)
            continue
        if argument in _HOW_MANY_ARGS:
            how_many = len(groups)
        groups.append((condition,))
    return groups


def _applies_whenever(a, b, facts):
    """Whether rule *a* applies whenever rule *b* does."""
    (a_kind, a_groups), (b_kind, b_groups) = a, b
    return a_kind == b_kind and all(
        any(_implies(b_group, a_group, facts) for b_group in b_groups)
        for a_group in a_groups)


def _implies(b, a, facts):
    if b == a:
        return True
    ((argument, w), q), ((other, v), p) = b[0], a[0]
    if (w and v and other == ALL_ARGS and argument in _HOW_MANY_ARGS
            and argument not in _OTHER_ARGS):
        # all arguments have p if the counted ones and the others have it
        def has_p(r):
            return r in facts and (r == p or p in facts[r][0])

        return has_p(q) and any(arg == OTHER_ARGS and expected and has_p(r)
                                for (arg, expected), r in b[1:])
    if argument != other or argument in _HOW_MANY_ARGS:
        return False
    if q not in facts or p not in facts:
        # a number
        return False
    if w and v:
        return p in facts[q][0]
    if w:
        return p in facts[q][1]
    if v:
        return False
    return q in facts[p][0]
