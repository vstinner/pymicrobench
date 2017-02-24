#!/usr/bin/env python3
"""
Benchmark on str methods for FASTCALL.

http://bugs.python.org/issue29286

Created at 2017-01-16 by Victor STINNER.
"""

import perf

runner = perf.Runner()

runner.timeit('"a".replace("x", "y")',
              '"a".replace("x", "y")',
              duplicate=100)
