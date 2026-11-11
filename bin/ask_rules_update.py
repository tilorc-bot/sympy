#!/usr/bin/env python

""" Update the ``ask_rules_generated.py`` file.

This must be run each time ``RULES`` in ``sympy.assumptions.ask_rules`` is
changed.

This must be run each time ``known_facts()`` in ``assumptions.facts`` module
is changed.

Should be run from sympy root directory.

$ python bin/ask_rules_update.py
"""

# hook in-tree SymPy into Python path, if possible
from __future__ import annotations

import os
import sys
from pathlib import Path

isympy_path = os.path.abspath(__file__)
isympy_dir = os.path.dirname(isympy_path)
sympy_top = os.path.split(isympy_dir)[0]
sympy_dir = os.path.join(sympy_top, 'sympy')

if os.path.isdir(sympy_dir):
    sys.path.insert(0, sympy_top)

from textwrap import wrap

from sympy.assumptions import rule_engine
from sympy.assumptions.ask_rules import RULES
from sympy.assumptions.rule_closing import close_rules, remove_implied_rules
from sympy.assumptions.rule_engine import FALSE_IF, TRUE_IF

KIND_NAMES = {FALSE_IF: 'FALSE_IF', TRUE_IF: 'TRUE_IF'}
SELECTOR_NAMES = {getattr(rule_engine, name): name for name in [
    'FIRST_ARG_IS', 'FIRST_ARG_IS_NOT', 'SECOND_ARG_IS', 'SECOND_ARG_IS_NOT',
    'SELF_IS', 'SELF_IS_NOT', 'ALL_ARGS_ARE', 'ALL_ARGS_ARE_NOT', 'ANY_ARG_IS',
    'ANY_ARG_IS_NOT', 'ONE_ARG_IS', 'ONE_ARG_IS_NOT', 'EVEN_NUMBER_OF_ARGS_ARE',
    'EVEN_NUMBER_OF_ARGS_ARE_NOT', 'ODD_NUMBER_OF_ARGS_ARE',
    'ODD_NUMBER_OF_ARGS_ARE_NOT', 'OTHER_ARGS_ARE', 'OTHER_ARGS_ARE_NOT',
]}
INDENT = ' ' * 8


def rule_lines(rule, used):
    kind, conditions = rule
    if not conditions:
        name = 'ALWAYS_TRUE' if kind == TRUE_IF else 'ALWAYS_FALSE'
        used.add(name)
        return [f'{INDENT}{name},']
    kind_name = KIND_NAMES[kind]
    used.add(kind_name)
    texts = []
    for selector, predicate in conditions:
        name = SELECTOR_NAMES.get(selector)
        if name is None:
            name = repr(selector)
        else:
            used.add(name)
        texts.append(f'({name}, {predicate})')
    line = f'{INDENT}({kind_name}, [{", ".join(texts)}]),'
    if len(line) <= 88:
        return [line]
    return ([f'{INDENT}({kind_name}, ['] + [f'{INDENT}    {text},' for text in texts]
            + [f'{INDENT}]),'])


def generate_code():
    rules = remove_implied_rules(close_rules(RULES))
    used = set()
    lines = ['RULES: Rules = {']
    for cls in dict.fromkeys(cls for cls, _ in RULES):
        predicates = sorted((p for c, p in rules if c is cls), key=str)
        for predicate in predicates:
            lines.append(f'    ({cls.__name__}, {predicate}): [')
            for rule in rules[(cls, predicate)]:
                lines.extend(rule_lines(rule, used))
            lines.append('    ],')
    lines.append('}')

    engine_import = ('from sympy.assumptions.rule_engine import ('
                     + ', '.join(sorted(used)) + ')')
    imports = [('sympy.assumptions.ask', 'from sympy.assumptions.ask import Q'),
               ('sympy.assumptions.rule_engine',
                '\n'.join(wrap(engine_import, width=88, subsequent_indent='    ',
                               break_on_hyphens=False)))]
    imports += [(cls.__module__, f'from {cls.__module__} import {cls.__name__}')
                for cls in dict.fromkeys(cls for cls, _ in rules)]
    header = [
        '"""',
        'Do NOT manually edit this file.',
        'Instead, run ./bin/ask_rules_update.py.',
        '"""',
        'from __future__ import annotations',
        '',
        'from typing import TYPE_CHECKING',
        '',
    ]
    header += [line for _, line in sorted(imports)]
    header += [
        '',
        'if TYPE_CHECKING:',
        '    from sympy.assumptions.rule_engine import Rules',
        '',
        '',
    ]
    return '\n'.join(header + lines) + '\n'


code = generate_code()
Path(sympy_dir, 'assumptions', 'ask_rules_generated.py').write_text(
    code, encoding='utf-8')
