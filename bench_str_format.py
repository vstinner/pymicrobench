#!/usr/bin/env python3
"""
Microbenchmarks the Python str.format() operation.

Issues:

* http://bugs.python.org/issue14744 str.format()
* http://bugs.python.org/issue14687 str % args

Benchmarks written for the "faster format" optimizations:

- if the result is just a string, copy the string by reference, don't copy
  it by value => restore an optimization of the PyAccu API.
  Examples:

   * "{}".format(str)
   * "%s".format(str)

- avoid a temporary buffer to format integers (base 2, 8, 10, 16)
  Examples:

   * "decimal=%s".format(int)
   * "hex=%x".format(int)
   * "%o".format(int)
   * "{}".format(int)
   * "{:x}".format(int)

- don't overallocate the last argument of a format string.
  Examples:

   * "x=%s".format("A" * 4096)
"""

import perf
import sys


def run_benchmark(bench):
    def timeit(stmt, setup):
        name = "%s; %s" % (setup, stmt)
        bench.timeit(name, stmt, setup)

    use_unicode = (sys.version_info >= (3,))
    if use_unicode:
        bmp_lit = '\\u20ac'
        bmp = '"\\u20ac"'
    short_ascii = '"abc"'
    short_int = '123'
    short_int_neg = '-123'
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

    huge_ascii = '"A" * (10 * 1024 * 1024)'
    huge_int = "2 ** 123456 - 1"
    if use_unicode:
        huge_bmp = bmp + ' * (10 * 1024 * 1024)'
        HUGE_ARGS = (huge_ascii, huge_bmp, huge_int)
    else:
        HUGE_ARGS = (huge_ascii, huge_int)

    INT_ARGS = (short_int, short_int_neg, long_int, huge_int)

    # Basic format, short ASCII output
    for arg in SHORT_ARGS:
        timeit(setup='fmt="{}"; arg=%s' % arg, stmt='fmt.format(arg)')
    timeit(setup='fmt="{:d}"; arg=%s' % short_int, stmt='fmt.format(arg)')
    timeit(setup='fmt="{:x}"; arg=%s' % short_int, stmt='fmt.format(arg)')
    for arg in SHORT_ARGS:
        timeit(setup='fmt="%%s"; arg=%s' % arg, stmt='fmt % arg')
    timeit(setup='fmt="%%d"; arg=%s' % short_int, stmt='fmt % arg')
    timeit(setup='fmt="%%x"; arg=%s' % short_int, stmt='fmt % arg')

    # Basic format, long output
    for arg in LONG_ARGS:
        timeit(setup='fmt="{}"; arg=%s' % arg, stmt='fmt.format(arg)')
    for arg in LONG_ARGS:
        timeit(setup='fmt="%%s"; arg=%s' % arg, stmt='fmt % arg')
    timeit(setup='fmt="{:d}"; arg=%s' % long_int, stmt='fmt.format(arg)')
    timeit(setup='fmt="{:x}"; arg=%s' % long_int, stmt='fmt.format(arg)')
    timeit(setup='fmt="%%d"; arg=%s' % long_int, stmt='fmt % arg')
    timeit(setup='fmt="%%x"; arg=%s' % long_int, stmt='fmt % arg')

    # One argument with ASCII prefix, short output
    for arg in SHORT_ARGS:
        timeit(setup='fmt="x={}"; arg=' + arg, stmt='fmt.format(arg)')
    for arg in SHORT_ARGS:
        timeit(setup='fmt="x=%s"; arg=' + arg, stmt='fmt % arg')

    # One argument with ASCII suffix, short output
    for arg in SHORT_ARGS:
        timeit(setup='fmt="{}:"; arg=' + arg, stmt='fmt.format(arg)')
    for arg in SHORT_ARGS:
        timeit(setup='fmt="%s:"; arg=' + arg, stmt='fmt % arg')

    if use_unicode:
        # One argument with BMP prefix and suffix, short output
        for arg in SHORT_ARGS:
            timeit(setup='fmt="\\u20ac[{}]"; arg=' + arg, stmt='fmt.format(arg)')
        for arg in SHORT_ARGS:
            timeit(setup='fmt="\\u20ac[%s]"; arg=' + arg, stmt='fmt % arg')

    # Huge output with prefix and suffix
    for arg in HUGE_ARGS:
        timeit(setup='fmt="{}"; arg=' + arg, stmt='fmt.format(arg)')
        timeit(setup='fmt="%s"; arg=' + arg, stmt='fmt % arg')
        timeit(setup='fmt="x=[{}]"; arg=' + arg, stmt='fmt.format(arg)')
        timeit(setup='fmt="x=[%s]"; arg=' + arg, stmt='fmt % arg')

    # Many short arguments
    for arg in SHORT_ARGS:
        timeit(setup='fmt="{0}"*1024', stmt='fmt.format(%s)' % arg)
    timeit(setup='fmt="{0}{1}"*1024', stmt='fmt.format(%s, %s)' % (short_ascii, short_int))
    if use_unicode:
        timeit(setup='fmt="{0}{1}{2}"*1024', stmt='fmt.format(%s, %s, %s)' % (short_ascii, short_bmp, short_int))
    timeit(setup='fmt="{0}-"*1024', stmt='fmt.format(%s)' % short_ascii)
    timeit(setup='fmt="{0}-"*1024', stmt='fmt.format(%s)' % short_int)
    timeit(setup='fmt="{0}-{1}="*1024', stmt='fmt.format(%s, %s)' % (short_ascii, short_int))
    if use_unicode:
        timeit(setup='fmt="{0}-{1}={2}#"*1024', stmt='fmt.format(%s, %s, %s)' % (short_ascii, short_bmp, short_int))

    # Many long arguments
    timeit(
        setup='fmt="{0}"*1024; arg=' + long_ascii,
        stmt='fmt.format(arg)')
    if use_unicode:
        timeit(
            setup='fmt="{0}"*1024; arg=' + long_bmp,
            stmt='fmt.format(arg)')
    timeit(
        setup='fmt="{0}"*1024; arg=' + long_int,
        stmt='fmt.format(arg)')
    timeit(
        setup='fmt="{0}{1}"*1024; args=(%s, %s)' % (long_ascii, long_int),
        stmt='fmt.format(*args)')
    if use_unicode:
        timeit(
            setup='fmt="{0}{1}{2}"*1024; args=(%s, %s, %s)' % (long_ascii, long_bmp, long_int),
            stmt='fmt.format(*args)')
    timeit(
        setup='fmt="{0}-"*1024; arg=' + long_ascii,
        stmt='fmt.format(arg)')
    timeit(
        setup='fmt="{0}-"*1024; arg=' + long_int,
        stmt='fmt.format(arg)')
    timeit(
        setup='fmt="{0}-{1}="*1024; args=(%s, %s)' % (long_ascii, long_int),
        stmt='fmt.format(*args)')
    if use_unicode:
        timeit(
            setup='fmt="{0}-{1}={2}#"*1024; args=(%s, %s, %s)' % (long_ascii, long_bmp, long_int),
            stmt='fmt.format(*args)')

    # Keywords
    timeit(
        setup='s="The {k1} is {k2} the {k3}."; args={"k1": "x", "k2": "y", "k3": "z"}',
        stmt='s.format(**args)')
    timeit(
        setup='s="The %(k1)s is %(k2)s the %(k3)s."; args={"k1":"x","k2":"y","k3":"z",}',
        stmt='s % args')

    if use_unicode:
        FILL = ('', bmp_lit)
    else:
        FILL = ('',)
    args = SHORT_ARGS
    for width in (10, 4096):
        # Align to 'width' characters
        for fill in FILL:
            for align in ('<', '>', '^'):
                for arg in args:
                    timeit('fmt.format(arg)', 'fmt="{:%s%s%s}"; arg=%s' % (fill, align, width, arg))
        # timeit('fmt.format(arg)', 'fmt="%%-%ss"; arg=%s' % (width, arg))
        # timeit('fmt.format(arg)', 'fmt="%%%ss"; arg=%s' % (width, arg))

    # Format number in the locale
    for arg in INT_ARGS:
        timeit('fmt.format(arg)', 'fmt="{:,}"; arg=%s;' % arg)

    # str(int)
    for arg in INT_ARGS:
        timeit(setup='number=' + arg, stmt='str(number)')


runner = perf.Runner()
run_benchmark(runner)
