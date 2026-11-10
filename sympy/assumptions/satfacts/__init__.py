"""
Facts for the SAT-based assumptions system that replace the recursive
handlers in ``sympy.assumptions.handlers``.

The facts are registered to the same ``class_fact_registry`` as the facts in
``sympy.assumptions.sathandlers`` so that ``satask`` uses both together.
"""
from __future__ import annotations
from . import common, numbers, ntheory, order, sets, calculus, matrices

__all__ = ['common', 'numbers', 'ntheory', 'order', 'sets', 'calculus', 'matrices']
