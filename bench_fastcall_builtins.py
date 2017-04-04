#!/usr/bin/env python3
"""
Benchmark on Python builtin functions to measure the speedup of
_PyObject_FastCall().

http://bugs.python.org/issue26814

Created at 2016-04-22 by Victor Stinner.
"""

import perf

bench = perf.Runner()

bench.timeit("filter(lambda x: x, list(range(1000)))",
             "list(filter(f, s))",
             "f = lambda x: x; s = list(range(1000))")

bench.timeit("map(lambda x: x, list(range(1000)))",
             "list(map(f, s))",
             "f = lambda x: x; s = list(range(1000))")

bench.timeit("sorted(list(range(1000)), key=lambda x: x)",
             "sorted(s, key=f)",
             "f = lambda x: x; s = list(range(1000))")

# Benchmark property_descr_get():
# PyObject_GetAttr() -> property_descr_get() -> itemgetter_call()
# -> PyObject_GetItem() -> tuplesubscript()
bench.timeit("namedtuple.attr",
             "a.a",
             "from collections import namedtuple as n; a = n('n', 'a b c')(1, 2, 3)",
             duplicate=100)

bench.timeit('object.__setattr__(obj, "x", 1)',
             'set(obj, "x", 1)',
             'class SimpleNamespace(object): pass\nset=object.__setattr__; obj=SimpleNamespace()',
             duplicate=100)

bench.timeit('object.__getattribute__(obj, "x")',
             'get(obj, "x")',
             'class SimpleNamespace(object): pass\nget=object.__getattribute__; obj=SimpleNamespace(); obj.x=1',
             duplicate=100)

bench.timeit('getattr(1, "real")',
             'getattr(1, "real")',
             duplicate=100)
