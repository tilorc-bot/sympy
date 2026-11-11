"""Checks of a table of rules, for tests and for what writes such a table."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.rule_engine import SELF
from sympy.utilities.iterables import strongly_connected_components

if TYPE_CHECKING:
    from sympy.assumptions.rule_engine import Rules


def check_no_cycles(rules: Rules) -> None:
    """Raise ``ValueError`` if conditions about SELF form a cycle of predicates."""
    edges = {
        (predicate, condition_predicate)
        for (_, predicate), rules_for_predicate in rules.items()
        for _, conditions in rules_for_predicate
        for (argument, _), condition_predicate in conditions
        if argument == SELF
    }
    vertices = {vertex for edge in edges for vertex in edge}
    graph = (sorted(vertices, key=str), sorted(edges, key=str))
    for component in strongly_connected_components(graph):
        if len(component) > 1 or (component[0], component[0]) in edges:
            names = ', '.join(sorted(map(str, component)))
            raise ValueError(f'the rules have a cycle: {names}')
