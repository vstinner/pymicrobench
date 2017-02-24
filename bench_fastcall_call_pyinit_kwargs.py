#!/usr/bin/env python3
"""
Hardcore microbenchmark on keyword arguments of _PyFunction_FastCallDict().

Pass keyword arguments to the tp_init slot of a Python constructor. Result for
1, 5 and 10 keyword arguments.

http://bugs.python.org/issue28839

Created at 2016-12-01 by Victor Stinner.
"""

import perf


class Bench1:
    def __init__(self, a):
        pass


class Bench5:
    def __init__(self, a, b, c, d, e):
        pass


class Bench10:
    def __init__(self, a, b, c, d, e, f, g, h, i, j):
        pass


def bench1(loops):
    Bench = Bench1   # use a local variable to avoid LOAD_GLOBAL
    it = range(loops)
    t0 = perf.perf_counter()

    for _ in it:
        Bench(a=1)
        Bench(a=1)

        Bench(a=1)
        Bench(a=1)

        Bench(a=1)
        Bench(a=1)

        Bench(a=1)
        Bench(a=1)

        Bench(a=1)
        Bench(a=1)

    dt = perf.perf_counter() - t0
    return dt


def bench5(loops):
    Bench = Bench5   # use a local variable to avoid LOAD_GLOBAL
    it = range(loops)
    t0 = perf.perf_counter()

    for _ in it:
        Bench(a=1, b=2, c=3, d=4, e=5)
        Bench(a=1, b=2, c=3, d=4, e=5)

        Bench(a=1, b=2, c=3, d=4, e=5)
        Bench(a=1, b=2, c=3, d=4, e=5)

        Bench(a=1, b=2, c=3, d=4, e=5)
        Bench(a=1, b=2, c=3, d=4, e=5)

        Bench(a=1, b=2, c=3, d=4, e=5)
        Bench(a=1, b=2, c=3, d=4, e=5)

        Bench(a=1, b=2, c=3, d=4, e=5)
        Bench(a=1, b=2, c=3, d=4, e=5)

    dt = perf.perf_counter() - t0
    return dt


def bench10(loops):
    Bench = Bench10   # use a local variable to avoid LOAD_GLOBAL
    it = range(loops)
    t0 = perf.perf_counter()

    for _ in it:
        Bench(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10)
        Bench(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10)

        Bench(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10)
        Bench(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10)

        Bench(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10)
        Bench(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10)

        Bench(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10)
        Bench(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10)

        Bench(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10)
        Bench(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10)

    dt = perf.perf_counter() - t0
    return dt


runner = perf.Runner()
runner.bench_sample_func('call_pyinit_kw1', bench1, inner_loops=10)
runner.bench_sample_func('call_pyinit_kw5', bench5, inner_loops=10)
runner.bench_sample_func('call_pyinit_kw10', bench10, inner_loops=10)
