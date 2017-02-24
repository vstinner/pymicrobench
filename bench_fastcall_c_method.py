"""
Benchmark on calling C methods for FASTCALL.

http://bugs.python.org/issue29263

Created at 2017-01-14 by INADA Naoki.
"""

import perf

runner = perf.Runner()
runner.timeit('b"".decode()',
              "empty_bytes.decode()",
              setup="empty_bytes = b''",
              duplicate=100)
runner.timeit('b"".decode("ascii")',
              "empty_bytes.decode('ascii')",
              setup="empty_bytes = b''",
              duplicate=100)
runner.timeit("[0].count(0)",
              "my_list.count(0)",
              setup="my_list = [0]",
              duplicate=100)
