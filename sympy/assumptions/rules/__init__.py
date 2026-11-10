"""
Rules about the classes of expressions which the assumptions system knows.

Where things are:

- The rules are written in the modules of this package, one per family of
  predicates. :mod:`~sympy.assumptions.rules.language` describes how.
- :mod:`~sympy.assumptions.rules.compiler` turns them into the modules
  ``sympy/assumptions/*_rules_generated.py``, which are what is used at
  run time. Run ``bin/ask_update.py`` after changing a rule.
- :mod:`~sympy.assumptions.rules.check` tests every rule on concrete
  values.

This package is imported only by ``bin/ask_update.py`` and by the tests.
"""
