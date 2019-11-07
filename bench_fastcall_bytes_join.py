#!/usr/bin/env python3
"""
Benchmark on the struct module for FASTCALL.

http://bugs.python.org/issue28004

Created at 2016-09-07 by Victor STINNER.
"""

import pyperf

runner = pyperf.Runner()


runner.timeit('b"".join((b"hello", b"world"))',
              'sep.join(seq)',
              setup="sep=b''; seq=(b'hello', b'world')",
              duplicate=100)
runner.timeit('b"".join((b"hello", b"world") * 100)',
              'sep.join(seq)',
              setup="sep=b''; seq=(b'hello', b'world', b'. ') * 100",
              duplicate=10)
