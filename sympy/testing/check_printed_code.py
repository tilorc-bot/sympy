"""Check that the C, C++ and Rust code printed by a test compiles.

Code printer tests only compare strings. A test opts in to checking the
code with a decorator::

    from sympy.testing.check_printed_code import check_printed_code

    @check_printed_code
    def test_sign():
        x, y = symbols('x y', real=True)
        assert rust_code(sign(x + y)) == "..."

The code is only compiled if SYMPY_CHECK_PRINTED_CODE is set, as in CI::

    SYMPY_CHECK_PRINTED_CODE=1 pytest sympy/printing/tests/test_rust.py

In every run, a decorated test fails if a symbol in its printed code has no
type: integer=True gives an int, real=True a double, and a symbol used in
And, Or, Not or a Piecewise condition a bool. It also fails if it prints no
C, C++ or Rust code, or code that can't be checked yet (arrays, matrices,
most non-default printer settings).

In a Hypothesis test, put the decorator below @given and use
@settings(deadline=None).
"""
from __future__ import annotations

import functools
import os
import shutil
import subprocess
import tempfile
from typing import NamedTuple

from sympy.codegen.ast import CodegenAST
from sympy.core.basic import Basic
from sympy.core.symbol import Symbol
from sympy.core.traversal import preorder_traversal
from sympy.functions.elementary.piecewise import ExprCondPair
from sympy.logic.boolalg import (And, Boolean, Equivalent, ITE, Implies, Nand,
                                 Nor, Not, Or, Xnor, Xor)
from sympy.matrices.expressions.matexpr import MatrixElement, MatrixSymbol
from sympy.printing.codeprinter import CodePrinter
from sympy.tensor.indexed import Idx, Indexed


class Target(NamedTuple):
    command: list[str]
    header: str
    types: dict[str, str]


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
    'C89CodePrinter': Target(['gcc', '-std=c89', *C_FLAGS], C_HEADER,
                             {'int': 'int', 'real': 'double', 'bool': 'int'}),
    'C99CodePrinter': Target(['gcc', '-std=c99', *C_FLAGS], C99_HEADER, C_TYPES),
    'C11CodePrinter': Target(['gcc', '-std=c11', *C_FLAGS], C99_HEADER, C_TYPES),
    'CXX98CodePrinter': Target(['g++', '-std=c++98', *GCC], CXX_HEADER, C_TYPES),
    'CXX11CodePrinter': Target(['g++', '-std=c++11', *GCC], CXX_HEADER, C_TYPES),
    'CXX17CodePrinter': Target(['g++', '-std=c++17', *GCC], CXX_HEADER, C_TYPES),
    'RustCodePrinter': Target(['rustc', '--edition=2021', '--crate-type=lib',
                               '--emit=metadata', '--error-format=short'],
                              RUST_HEADER, {'int': 'i32', 'real': 'f64', 'bool': 'bool'}),
}
PRINTER_MODULES = ('sympy.printing.c', 'sympy.printing.cxx', 'sympy.printing.rust')

# Settings that change the code, but not what it needs declared
HARMLESS_SETTINGS = {'order', 'full_prec', 'human', 'precision', 'contract',
                     'strict', 'error_on_reserved', 'reserved_word_suffix', 'inline'}
# Their arguments are booleans (unlike those of isnan and other BooleanFunctions)
LOGIC = (And, Or, Not, Xor, Xnor, Nand, Nor, Implies, Equivalent, ITE)
# Settings that the C printers store as attributes, not in _settings
C_TYPE_TABLES = ('type_aliases', 'type_mappings', 'type_headers', 'type_macros',
                 'type_func_suffixes', 'type_literal_suffixes',
                 'type_math_macro_suffixes')

ENVIRONMENT_VARIABLE = 'SYMPY_CHECK_PRINTED_CODE'


def compiling():
    return os.environ.get(ENVIRONMENT_VARIABLE, '') not in ('', '0')


class PrintedCodeError(AssertionError):
    """The code printed by a test decorated with ``check_printed_code`` is
    not declared or does not compile."""


def check_printed_code(test_func):
    """Decorator for a test whose printed C, C++ and Rust code must compile.

    See the docstring of :mod:`sympy.testing.check_printed_code`.
    """
    @functools.wraps(test_func)
    def wrapper(*args, **kwargs):
        snippets = []
        original = CodePrinter.doprint

        # Every C, C++ and Rust printer inherits doprint and none calls it
        # recursively, so this sees each snippet once
        def doprint(self, expr, assign_to=None):
            code = original(self, expr, assign_to)
            # The classes in TARGETS, not subclasses defined by tests
            if (type(self).__name__ in TARGETS
                    and type(self).__module__ in PRINTER_MODULES
                    and isinstance(code, str)):
                snippets.append(describe(self, expr, assign_to, code))
            return code

        CodePrinter.doprint = doprint  # type: ignore[method-assign]
        try:
            result = test_func(*args, **kwargs)
        finally:
            CodePrinter.doprint = original  # type: ignore[method-assign]
        compile = compile_snippet if compiling() else None
        check(snippets, compile)
        return result
    return wrapper


def describe(printer, expr, assign_to, code):
    """The snippet as a dict of the printer's class name, the code, the
    parameters and assigned variable as [name, kind] pairs, and the reason
    it can't be checked, or None.

    The kind is 'int', 'real', 'bool', or None if the test doesn't declare it.
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
    if not all(isinstance(s, Symbol) for s in expr.free_symbols):
        return 'free symbols that are not Symbols'
    if assign_to is not None and not isinstance(assign_to, (str, Symbol)):
        return 'assigning to a %s' % type(assign_to).__name__
    return None


def check(snippets, compile=None):
    """Raise PrintedCodeError if a snippet is not fully declared or, when
    ``compile`` is given, if it returns an error for a snippet."""
    if not snippets:
        raise PrintedCodeError('@check_printed_code: the test printed no C, '
                               'C++ or Rust code')
    unique = {}
    for s in snippets:
        unique.setdefault(key(s), s)
    errors = []
    for s in unique.values():
        about = '%s printed\n%s\n' % (
            s['printer'], '\n'.join(indent(s['code'].splitlines(), '  > ')))
        missing = [name for name, kind in declared(s) if kind is None]
        if s['reason']:
            errors.append(about + 'which cannot be checked (%s), so the test '
                          'cannot use @check_printed_code' % s['reason'])
        elif missing:
            errors.append(about + 'but the test does not declare the type of %s. '
                          'Create the symbols with real=True or integer=True, '
                          "e.g. Symbol('%s', real=True)" % (', '.join(missing), missing[0]))
        elif compile is not None:
            error = compile(s)
            if error is not None:
                numbered = ['%4d | %s' % (n, line)
                            for n, line in enumerate(source(s).splitlines(), 1)]
                errors.append('%swhich does not compile. %s:\n%s\nwrapped source:\n%s' % (
                    about, ' '.join(TARGETS[s['printer']].command),
                    '\n'.join(indent(error.splitlines(), '  ')), '\n'.join(numbered)))
    if errors:
        raise PrintedCodeError('@check_printed_code:\n\n' + '\n\n'.join(errors))


def key(snippet):
    return (snippet['printer'], snippet['code'], repr(snippet['params']),
            repr(snippet['target']), snippet['reason'])


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
    command = TARGETS[snippet['printer']].command
    if shutil.which(command[0]) is None:
        raise PrintedCodeError('%s is needed to check printed code (%s is set)'
                               % (command[0], ENVIRONMENT_VARIABLE))
    suffix = {'gcc': '.c', 'g++': '.cpp', 'rustc': '.rs'}[command[0]]
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'snippet' + suffix)
        with open(path, 'w') as f:
            f.write(source(snippet))
        result = subprocess.run(command + [path], cwd=tmp, capture_output=True,
                                text=True)
    return result.stderr.replace(path, 'snippet' + suffix) if result.returncode else None


def indent(lines, prefix):
    return [prefix + line for line in lines]
