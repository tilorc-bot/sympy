"""
The rules about the classes of expressions which the assumptions system
knows, one module per family of predicates.

:mod:`~sympy.assumptions.rule_language` describes how they are written, and
:mod:`~sympy.assumptions.rule_compiler` turns them into the modules
``sympy/assumptions/*_rules_generated.py``, which are what is used at run
time. Run ``bin/ask_update.py`` after changing a rule. The tests check every
rule on concrete values (:mod:`~sympy.assumptions.tests.rule_values`).

This package is imported only by ``bin/ask_update.py`` and by the tests.
"""
from __future__ import annotations

MODULES: tuple[str, ...] = ('calculus', 'common', 'matrices', 'ntheory', 'order', 'sets')
