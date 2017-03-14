#!/usr/bin/env python3
"""
Benchmark on functools.partial().

http://bugs.python.org/issue29735

Created at 2017-03-14 by Victor Stinner.
"""
import perf

runner = perf.Runner()
DUP = 1024

# Use small buffer, total: 2 positional arguments.
runner.timeit('partial Python, 1+1 arg',
              'g(2)',
              setup='from functools import partial; f = lambda x, y: None; g = partial(f, 1)',
              duplicate=DUP)

runner.timeit('partial Python, 2+0 arg',
              'g()',
              setup='from functools import partial; f = lambda x, y: None; g = partial(f, 1, 2)',
              duplicate=DUP)

# Don't use small buffer, total: 6 positional arguments.
runner.timeit('partial Python, 5+1 arg',
              'g(6)',
              setup='from functools import partial; f = lambda a1, a2, a3, a4, a5, a6: None; g = partial(f, 1, 2, 3, 4, 5)',
              duplicate=DUP)

# Another benchmark  with 10 position arguments:
runner.timeit('partial Python, 5+5 arg',
              'g(6, 7, 8, 9, 10)',
              setup='from functools import partial; f = lambda a1, a2, a3, a4, a5, a6, a7, a8, a9, a10: None; g = partial(f, 1, 2, 3, 4, 5)',
              duplicate=DUP)

# C function not supporting FASTCALL
runner.timeit('partial C VARARGS, 1+1 arg',
              'g(2)',
              setup='from functools import partial; f = lambda x, y: None; g = partial(min, 1)',
              duplicate=DUP)

runner.timeit('partial C VARARGS, 2+0 arg',
              'g()',
              setup='from functools import partial; f = lambda x, y: None; g = partial(min, 1, 2)',
              duplicate=DUP)

# C function supporting FASTCALL
runner.timeit('partial C FASTCALL, 1+0 arg',
              'g()',
              setup='from functools import partial; f = lambda x, y: None; g = partial(abs, 1)',
              duplicate=DUP)
