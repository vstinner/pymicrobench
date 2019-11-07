#!/usr/bin/env python3
"""
Measure the overhead of a logging call doing nothing.
"""

import io
import logging

import six
from six.moves import xrange
import pyperf

FORMAT = 'important: %s'
MESSAGE = 'some important information to be logged'


def bench_logging_silent(loops, logger, stream):
    # micro-optimization: use fast local variables
    m = MESSAGE
    range_it = xrange(loops)
    t0 = pyperf.perf_counter()

    for _ in range_it:
        # repeat 10 times
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)

    dt = pyperf.perf_counter() - t0

    if stream.getvalue():
        raise ValueError("stream is expected to be empty")

    return dt


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata['description'] = ("Measure the overhead of "
                                      "a logging call doing nothing")

    if six.PY3:
        stream = io.StringIO()
    else:
        stream = io.BytesIO()

    handler = logging.StreamHandler(stream=stream)
    logger = logging.getLogger("benchlogger")
    logger.propagate = False
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)

    runner.bench_time_func('logging_silent', bench_logging_silent,
                           logger, stream, inner_loops=10)
