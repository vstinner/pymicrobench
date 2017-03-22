#!/usr/bin/env python3
"""
Micro-benchmark for the Python operation str.format().

Issues:

* http://bugs.python.org/issue14744 str.format()
* http://bugs.python.org/issue14687 str % args
"""

import perf
import sys


def run_benchmark(bench):
    def timeit(stmt, setup):
        name = "%s; %s" % (setup, stmt)
        runner.timeit(name, stmt, setup)

    use_unicode = sys.version_info >= (3,)
    if use_unicode:
        bmp = '"\\u20ac"'
    short_ascii = '"abc"'
    short_int = '123'
    short_float = '12.345'
    short_complex1 = '2j'
    short_complex2 = '1+2j'
    if use_unicode:
        short_bmp = bmp + ' * 3'
        SHORT_ARGS = (short_ascii, short_bmp, short_int)
    else:
        SHORT_ARGS = (short_ascii, short_int)
    SHORT_ARGS += (short_float, short_complex1, short_complex2)

    long_ascii = '"A" * 4096'
    long_int = "2**4096 - 1"
    if use_unicode:
        long_bmp = bmp + ' * 4096'
        LONG_ARGS = (long_ascii, long_bmp, long_int)
    else:
        LONG_ARGS = (long_ascii, long_int)

    # Basic, short output
    for arg in SHORT_ARGS:
        timeit(
            setup='fmt="{x}"; x=%s' % arg,
            stmt='fmt.format(x=x)')
        timeit(
            setup='fmt="%%(x)s"; args={"x": %s}' % arg,
            stmt='fmt % args')

    # Basic, long output
    for arg in LONG_ARGS:
        timeit(
            setup='fmt="{x}"; x=%s' % arg,
            stmt='fmt.format(x=x)')
        timeit(
            setup='fmt="%%(x)s"; args={"x": %s}' % arg,
            stmt='fmt % args')

    # Prefix and suffix, short output
    for arg in SHORT_ARGS:
        timeit(
            setup='fmt="x={x}."; x=%s' % arg,
            stmt='fmt.format(x=x)')
        timeit(
            setup='fmt="x=%%(x)s."; args={"x": %s}' % arg,
            stmt='fmt % args')

    # Prefix and suffix, long output
    for arg in LONG_ARGS:
        timeit(
            setup='fmt="x={x}."; x=%s' % arg,
            stmt='fmt.format(x=x)')
        timeit(
            setup='fmt="x=%%(x)s."; args={"x": %s}' % arg,
            stmt='fmt % args')


runner = perf.Runner()
run_benchmark(runner)
