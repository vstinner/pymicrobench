#!/usr/bin/env python3
"""Microbenchmark on ignored warning.

https://bugs.python.org/issue27535
"""

import pyperf
from six.moves import xrange
import warnings


def emit_warning(loops):
    warn_func = warnings.warn
    category = Warning
    range_it = xrange(loops)

    start_time = pyperf.perf_counter()
    for _ in range_it:
        warn_func('test', category)
    dt = pyperf.perf_counter() - start_time
    return dt


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata['description'] = ("Measure the performance of emitting "
                                      "a warning which is ignored")

    # Ignore warnings
    warnings.simplefilter("ignore")

    runner.bench_time_func('emit_warning', emit_warning)
