"""Check that new C, C++ and Rust code printed by SymPy's tests compiles.

Code printer tests compare printed strings, e.g.
``assert rust_code(expr) == "..."``, so nothing checks that the asserted code
is valid in the target language. This module does, in two steps:

1. Loaded as a pytest plugin, it records every snippet that the printers in
   ``TARGETS`` print during the tests, with the test that printed it and the
   types the test declares for its symbols::

       pytest -p sympy.testing.check_printed_code --printed-code=head.json sympy/printing

2. Run as a script on two such captures (of the merge base and the head of a
   pull request), it compiles each snippet that is in the head capture but
   not in the base capture::

       python -m sympy.testing.check_printed_code base.json head.json

A snippet is new if the base capture has no snippet from the same printer
with the same code and declarations. Only new snippets are checked, so
existing output is never examined unless a pull request changes it.

The types come only from what a test declares:

- A symbol with ``integer=True`` is an ``int`` (``i32`` in Rust), a symbol
  with ``real=True`` (and not integer) is a ``double`` (``f64``), and a
  symbol used as a boolean (an argument of ``And``, ``Or``, ``Not``, ... or
  a ``Piecewise`` condition) is a ``bool``. For any other symbol the test
  must declare ``real=True`` or ``integer=True``. If a new or edited test
  (one whose source differs from the merge base's) does not, that is a
  failure. If an unchanged test prints new code, it is a warning.
- Snippets that need declarations the check cannot make (arrays, matrices,
  codegen AST nodes, ``user_functions``, ``dereference`` and other
  non-default settings) are not checked, which is reported for new and
  edited tests.
- A test whose printed code is deliberately not valid code, for example a
  test of the "Not supported" comment, is marked with
  ``@uncompilable_code(reason)`` from ``sympy.testing.pytest`` and is not
  captured.
"""
from __future__ import annotations

import hashlib
import inspect
import json
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

from sympy.codegen.ast import CodegenAST
from sympy.core.basic import Basic
from sympy.core.symbol import Dummy, Symbol
from sympy.core.traversal import preorder_traversal
from sympy.functions.elementary.piecewise import ExprCondPair
from sympy.logic.boolalg import (And, Boolean, Equivalent, ITE, Implies, Nand,
                                 Nor, Not, Or, Xnor, Xor)
from sympy.matrices.expressions.matexpr import MatrixElement, MatrixSymbol
from sympy.printing.codeprinter import CodePrinter
from sympy.tensor.indexed import Idx, Indexed


# The targets: one per printer class, each with the compiler command (run
# with the source file appended), the code put before the snippet's function,
# and the names of the int, real and bool types. Only the printer classes
# themselves are checked, not subclasses.

C_HEADER = """\
#define _XOPEN_SOURCE 700
#include <math.h>
#include <stdlib.h>
"""  # M_PI, M_E, ... are POSIX, not ISO C
C99_HEADER = C_HEADER + "#include <stdbool.h>\n"
CXX_HEADER = "#include <algorithm>\n#include <cmath>\n#include <cstdlib>\n"
RUST_HEADER = """\
#![allow(unused)]
use std::f64::consts::*;
use std::f64::{INFINITY, NAN, NEG_INFINITY};
"""

GCC = ['-fsyntax-only', '-pedantic-errors']
# C89 allows calls to undeclared functions
C_FLAGS = [*GCC, '-Werror=implicit-function-declaration']
C_TYPES = {'int': 'int', 'real': 'double', 'bool': 'bool'}

TARGETS = {
    'C89CodePrinter': (['gcc', '-std=c89', *C_FLAGS], C_HEADER,
                       {'int': 'int', 'real': 'double', 'bool': 'int'}),
    'C99CodePrinter': (['gcc', '-std=c99', *C_FLAGS], C99_HEADER, C_TYPES),
    'C11CodePrinter': (['gcc', '-std=c11', *C_FLAGS], C99_HEADER, C_TYPES),
    'CXX98CodePrinter': (['g++', '-std=c++98', *GCC], CXX_HEADER, C_TYPES),
    'CXX11CodePrinter': (['g++', '-std=c++11', *GCC], CXX_HEADER, C_TYPES),
    'CXX17CodePrinter': (['g++', '-std=c++17', *GCC], CXX_HEADER, C_TYPES),
    'RustCodePrinter': (['rustc', '--edition=2021', '--crate-type=lib',
                         '--emit=metadata'], RUST_HEADER,
                        {'int': 'i32', 'real': 'f64', 'bool': 'bool'}),
}
PRINTER_MODULES = ('sympy.printing.c', 'sympy.printing.cxx', 'sympy.printing.rust')

# Settings that change the code, but not what it needs declared
HARMLESS_SETTINGS = {'order', 'full_prec', 'human', 'precision', 'contract',
                     'strict', 'error_on_reserved', 'reserved_word_suffix', 'inline'}
# Their arguments are booleans (unlike those of isnan and other BooleanFunctions)
LOGIC = (And, Or, Not, Xor, Xnor, Nand, Nor, Implies, Equivalent, ITE)
# C printer settings that __init__ removes from the settings and stores here
C_TYPE_TABLES = ('type_aliases', 'type_mappings', 'type_headers', 'type_macros',
                 'type_func_suffixes', 'type_literal_suffixes',
                 'type_math_macro_suffixes')


# ---------------------------------------------------------------- capture --

_capture: dict | None = None    # {'tests': ..., 'snippets': ...} while capturing
_current_test: str | None = None


def pytest_addoption(parser):
    parser.addoption('--printed-code', metavar='FILE',
                     help='record C, C++ and Rust printer output to FILE')


def pytest_configure(config):
    global _capture
    if config.getoption('printed_code') is None:
        return
    if hasattr(config, 'workerinput'):
        raise RuntimeError('--printed-code does not support pytest-xdist')
    _capture = {'tests': {}, 'snippets': []}
    original = CodePrinter.doprint

    # Every C, C++ and Rust printer inherits doprint from CodePrinter and
    # no printer calls it recursively, so wrapping it here sees each
    # snippet a test prints exactly once. A passing test asserts the string
    # that doprint returned, so checking that string checks the test.
    def doprint(self, expr, assign_to=None):
        code = original(self, expr, assign_to)
        if (_current_test is not None and type(self).__name__ in TARGETS
                and type(self).__module__ in PRINTER_MODULES
                and isinstance(code, str)):
            _capture['snippets'].append(dict(
                describe(self, expr, assign_to, code), test=_current_test))
        return code

    CodePrinter.doprint = doprint  # type: ignore[method-assign]


def pytest_runtest_setup(item):
    global _current_test
    if _capture is None or not hasattr(item, 'function'):
        return
    source = inspect.getsource(item.function)
    _capture['tests'][item.nodeid] = hashlib.sha1(source.encode()).hexdigest()
    if not hasattr(item.function, '_uncompilable_code'):
        _current_test = item.nodeid


def pytest_runtest_teardown(item):
    global _current_test
    _current_test = None


def pytest_unconfigure(config):
    if _capture is not None:
        with open(config.getoption('printed_code'), 'w') as f:
            json.dump(_capture, f, indent=0)


def describe(printer, expr, assign_to, code):
    """Describe a printed snippet by what the test declared about it.

    Returns a dict with the printer class name, the code, the parameters
    and assigned variable as ``[printed name, kind]`` pairs (kind is
    'int', 'real', 'bool' or None when undeclared) and, if the snippet
    cannot be checked, the reason.
    """
    record = {'printer': type(printer).__name__, 'code': code,
              'params': [], 'target': None, 'reason': unsupported(printer, expr, assign_to)}
    if record['reason']:
        return record
    booleans = set()
    for node in preorder_traversal(expr):
        if isinstance(node, LOGIC):
            booleans.update(node.args)
        elif isinstance(node, ExprCondPair):
            booleans.add(node.cond)

    def declare(symbol, is_boolean):
        if is_boolean:
            kind = 'bool'
        elif symbol.is_integer:
            kind = 'int'
        elif symbol.is_real:
            kind = 'real'
        else:
            kind = None
        return [printer._print(symbol), kind]

    record['params'] = [declare(s, s in booleans)
                        for s in sorted(expr.free_symbols, key=str)]
    if assign_to is not None:
        target = Symbol(assign_to) if isinstance(assign_to, str) else assign_to
        is_boolean = isinstance(expr, Boolean) and not isinstance(expr, Symbol)
        name, kind = declare(target, is_boolean)
        record['target'] = [name, dict(record['params']).get(name, kind)]
    bad = [name for name, _ in declared(record) if not name.isidentifier()]
    if bad:
        record['reason'] = 'symbols printed as %s' % ', '.join(bad)
    return record


def declared(snippet):
    """The [name, kind] pairs of the parameters and the assigned variable."""
    return snippet['params'] + ([snippet['target']] if snippet['target'] else [])


def unsupported(printer, expr, assign_to):
    """Why the snippet cannot be checked, or None."""
    settings = [k for k, v in printer._settings.items()
                if k not in HARMLESS_SETTINGS and v != printer._default_settings.get(k)]
    settings += [k for k in C_TYPE_TABLES
                 if getattr(printer, k, None) != getattr(type(printer), k, None)]
    if settings:
        return 'printer setting %s' % ', '.join(sorted(settings))
    if not isinstance(expr, Basic) or isinstance(expr, CodegenAST) or expr.is_Matrix:
        return 'printing a %s' % type(expr).__name__
    if expr.atoms(Indexed, Idx, MatrixSymbol, MatrixElement):
        return 'arrays'
    if expr.atoms(Dummy):
        return 'Dummy symbols, whose names change between runs'
    if not all(isinstance(s, Symbol) for s in expr.free_symbols):
        return 'free symbols that are not Symbols'
    if assign_to is not None and not isinstance(assign_to, (str, Symbol)):
        return 'assigning to a %s' % type(assign_to).__name__
    return None


# ------------------------------------------------------------------ check --

def key(snippet):
    return json.dumps([snippet['printer'], snippet['code'], snippet['params'],
                       snippet['target'], snippet['reason']])


def source(snippet):
    """The snippet wrapped into a function, so that it compiles if valid."""
    _, header, types = TARGETS[snippet['printer']]
    rust = snippet['printer'] == 'RustCodePrinter'
    params = [(name, types[kind]) for name, kind in snippet['params']]
    lines = snippet['code'].splitlines()
    target = snippet['target']
    if target is None:
        if rust:
            # A block, since an expression can follow declarations of
            # number constants such as GoldenRatio
            body = ['let _ = {', *indent(lines, '    '), '};']
        else:
            n = 0
            while n < len(lines) and (lines[n].endswith(';')
                                      or lines[n].startswith(('//', '/*'))):
                n += 1
            body = lines[:n] + ['(void)(', *indent(lines[n:], '    '), ');']
    elif target[0] in [name for name, _ in params]:
        body = lines
    elif rust:
        body = ['let mut %s: %s;' % (target[0], types[target[1]]), *lines]
    else:
        body = ['%s %s;' % (types[target[1]], target[0]), *lines]
    if rust:
        signature = 'pub fn f(%s)' % ', '.join(
            '%s%s: %s' % ('mut ' if target and name == target[0] else '', name, type_)
            for name, type_ in params)
    else:
        signature = 'void f(%s)' % (', '.join(
            '%s %s' % (type_, name) for name, type_ in params) or 'void')
    return '%s\n%s\n{\n%s\n}\n' % (header, signature, '\n'.join(indent(body, '    ')))


def compile_snippet(snippet):
    """Compile the snippet; return the compiler's error output, or None."""
    command = TARGETS[snippet['printer']][0]
    suffix = {'gcc': '.c', 'g++': '.cpp', 'rustc': '.rs'}[command[0]]
    with tempfile.TemporaryDirectory() as tmp:
        path = '%s/snippet%s' % (tmp, suffix)
        with open(path, 'w') as f:
            f.write(source(snippet))
        result = subprocess.run(command + [path], cwd=tmp, capture_output=True,
                                text=True)
    return result.stderr.replace(path, 'snippet' + suffix) if result.returncode else None


def check(base, head, compile=compile_snippet):
    """Check the snippets in the capture head that are not in base.

    Returns the number of new snippets and a (status, message) pair for
    each. The status is 'ok', 'fail', 'warning', 'not checked', or 'ignored'
    for a snippet that cannot be checked and was printed only by unchanged
    tests (such as one with names that differ between runs).
    """
    old = {key(s) for s in base['snippets']}
    new = {}
    for s in head['snippets']:
        if key(s) not in old:
            tests = new.setdefault(key(s), (s, []))[1]
            if s['test'] not in tests:
                tests.append(s['test'])
    to_compile, results = [], []
    for s, tests in new.values():
        touched = any(head['tests'][t] != base['tests'].get(t) for t in tests)
        about = '%s printed by %s (%s)\n%s\n' % (
            s['printer'], ', '.join(tests),
            'new or edited test' if touched else 'unchanged test, new output',
            '\n'.join(indent(s['code'].splitlines(), '  > ')))
        missing = [name for name, kind in declared(s) if kind is None]
        if s['reason']:
            results.append(('not checked' if touched else 'ignored',
                            about + 'cannot check: %s' % s['reason']))
        elif missing:
            results.append(('fail' if touched else 'warning', about + (
                'cannot check: the test does not declare the type of %s. Create '
                'the symbols with real=True or integer=True, e.g. '
                "Symbol('%s', real=True)" % (', '.join(missing), missing[0]))))
        else:
            to_compile.append((s, about))
    with ThreadPoolExecutor(4) as pool:
        errors = list(pool.map(compile, [s for s, _ in to_compile]))
    for (s, about), error in zip(to_compile, errors):
        if error is None:
            results.append(('ok', about))
        else:
            command = ' '.join(TARGETS[s['printer']][0])
            numbered = ['%4d | %s' % (n, line)
                        for n, line in enumerate(source(s).splitlines(), 1)]
            results.append(('fail', '%s%s failed:\n%s\nwrapped source:\n%s' % (
                about, command, '\n'.join(indent(error.splitlines(), '  ')),
                '\n'.join(numbered))))
    return results, len(new)


def indent(lines, prefix):
    return [prefix + line for line in lines]


def main(base_file, head_file):
    with open(base_file) as f:
        base = json.load(f)
    with open(head_file) as f:
        head = json.load(f)
    for command, _, _ in TARGETS.values():
        if shutil.which(command[0]) is None:
            sys.exit('%s is needed to check printed code' % command[0])
    results, count = check(base, head)
    for status in ('fail', 'warning', 'not checked'):
        for s, message in results:
            if s == status:
                print('%s: %s\n' % (status.upper(), message))
    counts = [sum(s == status for s, _ in results)
              for status in ('fail', 'ok', 'warning', 'not checked', 'ignored')]
    print('%d failed. Of %d printed snippets, %d are new: %d compiled, %d warnings, '
          '%d not checked, %d not checked in unchanged tests.' % (
              counts[0], len(head['snippets']), count, *counts[1:]))
    if counts[0]:
        print('\nA test whose printed code is deliberately not valid code can be '
              'marked with @uncompilable_code(reason) from sympy.testing.pytest.')
    return 1 if counts[0] else 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
