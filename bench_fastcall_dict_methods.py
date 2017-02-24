#!/usr/bin/env python3
"""
Benchmark on dict methods for FASTCALL.

http://bugs.python.org/issue29311

Created at 2017-02-24 by Victor STINNER.
"""

import perf

runner = perf.Runner()

runner.timeit('{1: 2}.get(1)',
              'mydict.get(1)',
              setup='mydict = {1: 2}',
              duplicate=100)

runner.timeit('{1: 2}.get(7, None)',
              'mydict.get(7, None)',
              setup='mydict = {1: 2}',
              duplicate=100)
