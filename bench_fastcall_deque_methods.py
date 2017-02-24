#!/usr/bin/env python3
"""
Benchmark on the deque type for FASTCALL.

http://bugs.python.org/issue29452

Created at 2017-02-05 by Victor STINNER.
"""

import perf

runner = perf.Runner()

runner.timeit('collections.deque.rotate()',
              'd.rotate()',
              setup='import collections; d=collections.deque()',
              duplicate=100)
runner.timeit('collections.deque.rotate(1)',
              'd.rotate(1)',
              setup='import collections; d=collections.deque()',
              duplicate=100)
runner.timeit('collections.deque.insert()',
              'd = collections.deque(); d.insert(0, None); d.insert(1, None); d.insert(2, None); d.insert(3, None); d.insert(4, None)',
              setup='import collections',
              duplicate=10)
runner.timeit('collections.deque([None]).index(None)',
              'd.index(None)',
              setup='import collections; d = collections.deque([None])',
              duplicate=100)
