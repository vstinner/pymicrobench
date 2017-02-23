#!/usr/bin/env python3
"""
Benchmark on Python builtin functions to measure the speedup of
_PyObject_FastCall().

http://bugs.python.org/issue26814

Created at 2016-04-22 by Victor Stinner.
"""

import perf

bench = perf.Runner()

bench.timeit("filter",
             "list(filter(f, s))",
             "f = lambda x: x; s = list(range(1000))")

bench.timeit("map",
             "list(map(f, s))",
             "f = lambda x: x; s = list(range(1000))")

bench.timeit("sorted(list, key=lambda x: x)",
             "sorted(s, key=f)",
             "f = lambda x: x; s = list(range(1000))")

bench.timeit("sorted(list)",
             "sorted(s)",
             "s = list(range(1000))")

bench.timeit('b=MyBytes(); bytes(b)',
             'bytes(b)',
             'class MyBytes:\n def __bytes__(self): return b"abc"\nb = MyBytes()')

bench.timeit("namedtuple.attr",
             "a.a",
             "from collections import namedtuple as n; a = n('n', 'a b c')(1, 2, 3)",
             duplicate=20)

bench.timeit('object.__setattr__(obj, "x", 1)',
             'set(obj, "x", 1)',
             'class SimpleNamespace(object): pass\nset=object.__setattr__; obj=SimpleNamespace()')

bench.timeit('object.__getattribute__(obj, "x")',
             'get(obj, "x")',
             'class SimpleNamespace(object): pass\nget=object.__getattribute__; obj=SimpleNamespace(); obj.x=1')

bench.timeit('getattr(1, "real")',
             'getattr(1, "real")')

bench.timeit('bounded_pymethod(1, 2)',
             'm(1, 2)',
             'class A:\n def meth(self, arg1, arg2): pass\nm=A().meth')

bench.timeit('unbound_pymethod(obj, 1, 2)',
             'm(a, 1, 2)',
             'class A:\n def meth(self, arg1, arg2): pass\na=A(); m=A.meth')

bench.timeit('func()',
             'func()',
             'def func(): pass')

bench.timeit('func(1, 2, 3)',
             'func(1, 2, 3)',
             'def func(a, b, c): pass')
