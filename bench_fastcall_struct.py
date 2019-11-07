#!/usr/bin/env python3
"""
Benchmark on the struct module for FASTCALL.

http://bugs.python.org/issue29300

Created at 2017-02-02 by Victor STINNER.
"""

import pyperf

runner = pyperf.Runner()

runner.timeit('int.to_bytes(1, 4, "little")',
              'to_bytes(1, 4, "little")',
              setup='to_bytes = int.to_bytes',
              duplicate=100)

runner.timeit('struct.pack("i", 1)',
              'pack("i", 1)',
              setup='import struct; pack = struct.pack',
              duplicate=100)
