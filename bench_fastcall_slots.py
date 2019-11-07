#!/usr/bin/env python3
"""
Benchmark Python "slots".

http://bugs.python.org/issue28915
http://bugs.python.org/issue29507

Created at 2016-12-09 by Victor Stinner.
"""

import pyperf


class Obj:
    def __int__(self):
        return 5

    def __getitem__(self, key):
        return 6


obj = Obj()
if int(obj) != 5:
    raise Exception("bug")
if obj[0] != 6:
    raise Exception("bug")

runner = pyperf.Runner()

runner.timeit('Python __int__: int(obj)',
              'int(obj)',
              duplicate=100,
              # Copy int type builtin into globals for faster lookup
              globals={'int': int, 'obj': obj})

runner.timeit('Python __getitem__: obj[0]',
              'obj[0]',
              duplicate=100,
              globals={'obj': obj})
