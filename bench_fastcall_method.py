#!/usr/bin/env python3
"""
Micro-benchmark to measure the performance of CPython call_method() using
FASTCALL (avoid temporary tuple).

http://bugs.python.org/issue29507

Created at 2017-02-09 by Victor Stinner.
"""

import perf

class C:
    def __getitem__(self, index):
        return index

bench = perf.Runner()
bench.timeit('Python __getitem__()', 'c[0]', duplicate=100, globals={'c': C()})
