"""Check that the C, C++ and Rust code printed by a test compiles.

Code printer tests compare printed strings, e.g.
``assert rust_code(expr) == "..."``, so nothing checks that the asserted code
is valid in the target language. A test opts in to that check with the
``check_printed_code`` decorator::

    from sympy.testing.check_printed_code import check_printed_code

    @check_printed_code
    def test_sign():
        x, y = symbols('x y', real=True)
        assert rust_code(sign(x + y)) == "..."

While a decorated test runs, every snippet printed by the printers in
``TARGETS`` is recorded. When the test returns:

1. Each snippet must be fully declared by the test, and the test fails if one
   is not. This needs no compiler, so it is done in every test run. The types
   come only from what the test declares, nothing is guessed:

   - A symbol with ``integer=True`` is an ``int`` (``i32`` in Rust), and a
     symbol with ``real=True`` (and not integer) is a ``double`` (``f64``).
   - A symbol used as a boolean (an argument of ``And``, ``Or``, ``Not``, ...
     or a ``Piecewise`` condition) is a ``bool``.
   - Any other symbol must be declared with ``real=True`` or ``integer=True``.
   - Snippets that need declarations that cannot be made this way (arrays,
     matrices, codegen AST nodes, ``user_functions``, ``dereference`` and other
     non-default settings) cannot be checked, so a test that prints them
     must not use the decorator.

2. If the environment variable ``SYMPY_CHECK_PRINTED_CODE`` is set, each
   snippet is wrapped in a function and compiled (``gcc -fsyntax-only``,
   ``g++ -fsyntax-only``, ``rustc --emit=metadata``), and the test fails if
   one does not compile. CI does this for the tests that use the decorator::

       SYMPY_CHECK_PRINTED_CODE=1 pytest sympy/printing/tests/test_rust.py

A decorated test must print at least one C, C++ or Rust snippet.

In a Hypothesis test, put the decorator below ``@given``, so that each
example is checked and Hypothesis shrinks a failing one, and use
``@settings(deadline=None)``, since compiling takes longer than the
default deadline. See ``sympy/printing/tests/test_printed_code_hypothesis.py``.
"""
from __future__ import annotations

import functools
import os
import shutil
import subprocess
import tempfile

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
                         '--emit=metadata', '--error-format=short'], RUST_HEADER,
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

ENVIRONMENT_VARIABLE = 'SYMPY_CHECK_PRINTED_CODE'


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

        # Every C, C++ and Rust printer inherits doprint from CodePrinter and
        # no printer calls it recursively, so wrapping it here sees each
        # snippet the test prints exactly once. A passing test asserts the
        # string that doprint returned, so checking that string checks the
        # test.
        def doprint(self, expr, assign_to=None):
            code = original(self, expr, assign_to)
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
        compile = compile_snippet if os.environ.get(ENVIRONMENT_VARIABLE) else None
        check(snippets, compile)
        return result
    return wrapper


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
        return 'Dummy symbols'
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
                    about, ' '.join(TARGETS[s['printer']][0]),
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
    command = TARGETS[snippet['printer']][0]
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
