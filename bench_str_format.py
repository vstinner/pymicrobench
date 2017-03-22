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


use_unicode = (sys.version_info >= (3,))
if use_unicode:
    BMP_LIT = '\\u20ac'
    BMP = '"\\u20ac"'
SHORT_ASCII = '"abc"'
SHORT_INT = '123'
SHORT_INT_NEG = '-123'
SHORT_FLOAT = '12.345'
SHORT_COMPLEX1 = '2j'
SHORT_COMPLEX2 = '1+2j'
if use_unicode:
    SHORT_BMP = BMP + ' * 3'
    SHORT_ARGS = (SHORT_ASCII, SHORT_BMP, SHORT_INT)
else:
    SHORT_ARGS = (SHORT_ASCII, SHORT_INT)
SHORT_ARGS += (SHORT_FLOAT, SHORT_COMPLEX1, SHORT_COMPLEX2)

LONG_ASCII = '"A" * 4096'
LONG_INT = "2**4096 - 1"
if use_unicode:
    LONG_BMP = BMP + ' * 4096'
    LONG_ARGS = (LONG_ASCII, LONG_BMP, LONG_INT)
else:
    LONG_ARGS = (LONG_ASCII, LONG_INT)

HUGE_ASCII = '"A" * (10 * 1024 * 1024)'
HUGE_INT = "2 ** 123456 - 1"
if use_unicode:
    HUGE_BMP = BMP + ' * (10 * 1024 * 1024)'
    HUGE_ARGS = (HUGE_ASCII, HUGE_BMP, HUGE_INT)
else:
    HUGE_ARGS = (HUGE_ASCII, HUGE_INT)

INT_ARGS = (SHORT_INT, SHORT_INT_NEG, LONG_INT, HUGE_INT)


def basic_format_short_ascii_output():
    for arg in SHORT_ARGS:
        timeit(setup='fmt="{}"; arg=%s' % arg, stmt='fmt.format(arg)')
    timeit(setup='fmt="{:d}"; arg=%s' % SHORT_INT, stmt='fmt.format(arg)')
    timeit(setup='fmt="{:x}"; arg=%s' % SHORT_INT, stmt='fmt.format(arg)')
    for arg in SHORT_ARGS:
        timeit(setup='fmt="%%s"; arg=%s' % arg, stmt='fmt % arg')
    timeit(setup='fmt="%%d"; arg=%s' % SHORT_INT, stmt='fmt % arg')
    timeit(setup='fmt="%%x"; arg=%s' % SHORT_INT, stmt='fmt % arg')


def basic_format_long_output():
    for arg in LONG_ARGS:
        timeit(setup='fmt="{}"; arg=%s' % arg, stmt='fmt.format(arg)')
    for arg in LONG_ARGS:
        timeit(setup='fmt="%%s"; arg=%s' % arg, stmt='fmt % arg')
    timeit(setup='fmt="{:d}"; arg=%s' % LONG_INT, stmt='fmt.format(arg)')
    timeit(setup='fmt="{:x}"; arg=%s' % LONG_INT, stmt='fmt.format(arg)')
    timeit(setup='fmt="%%d"; arg=%s' % LONG_INT, stmt='fmt % arg')
    timeit(setup='fmt="%%x"; arg=%s' % LONG_INT, stmt='fmt % arg')


def format_ascii_prefix_short_output():
    # One argument with ASCII prefix, short output
    for arg in SHORT_ARGS:
        timeit(setup='fmt="x={}"; arg=' + arg, stmt='fmt.format(arg)')
    for arg in SHORT_ARGS:
        timeit(setup='fmt="x=%s"; arg=' + arg, stmt='fmt % arg')


def format_ascii_suffix_short_output():
    # One argument with ASCII suffix, short output
    for arg in SHORT_ARGS:
        timeit(setup='fmt="{}:"; arg=' + arg, stmt='fmt.format(arg)')
    for arg in SHORT_ARGS:
        timeit(setup='fmt="%s:"; arg=' + arg, stmt='fmt % arg')


def format_bmp_prefix_suffix_short_output():
    if use_unicode:
        # One argument with BMP prefix and suffix, short output
        for arg in SHORT_ARGS:
            timeit(setup='fmt="\\u20ac[{}]"; arg=' + arg, stmt='fmt.format(arg)')
        for arg in SHORT_ARGS:
            timeit(setup='fmt="\\u20ac[%s]"; arg=' + arg, stmt='fmt % arg')


def format_huge_output_with_prefix_suffix():
    # Huge output with prefix and suffix
    for arg in HUGE_ARGS:
        timeit(setup='fmt="{}"; arg=' + arg, stmt='fmt.format(arg)')
        timeit(setup='fmt="%s"; arg=' + arg, stmt='fmt % arg')
        timeit(setup='fmt="x=[{}]"; arg=' + arg, stmt='fmt.format(arg)')
        timeit(setup='fmt="x=[%s]"; arg=' + arg, stmt='fmt % arg')


def format_many_short_args():
    # Many short arguments
    for arg in SHORT_ARGS:
        timeit(setup='fmt="{0}"*1024', stmt='fmt.format(%s)' % arg)
    timeit(setup='fmt="{0}{1}"*1024', stmt='fmt.format(%s, %s)' % (SHORT_ASCII, SHORT_INT))
    if use_unicode:
        timeit(setup='fmt="{0}{1}{2}"*1024', stmt='fmt.format(%s, %s, %s)' % (SHORT_ASCII, SHORT_BMP, SHORT_INT))
    timeit(setup='fmt="{0}-"*1024', stmt='fmt.format(%s)' % SHORT_ASCII)
    timeit(setup='fmt="{0}-"*1024', stmt='fmt.format(%s)' % SHORT_INT)
    timeit(setup='fmt="{0}-{1}="*1024', stmt='fmt.format(%s, %s)' % (SHORT_ASCII, SHORT_INT))
    if use_unicode:
        timeit(setup='fmt="{0}-{1}={2}#"*1024', stmt='fmt.format(%s, %s, %s)' % (SHORT_ASCII, SHORT_BMP, SHORT_INT))


def format_many_long_args():
    # Many long arguments
    timeit(
        setup='fmt="{0}"*1024; arg=' + LONG_ASCII,
        stmt='fmt.format(arg)')
    if use_unicode:
        timeit(
            setup='fmt="{0}"*1024; arg=' + LONG_BMP,
            stmt='fmt.format(arg)')
    timeit(
        setup='fmt="{0}"*1024; arg=' + LONG_INT,
        stmt='fmt.format(arg)')
    timeit(
        setup='fmt="{0}{1}"*1024; args=(%s, %s)' % (LONG_ASCII, LONG_INT),
        stmt='fmt.format(*args)')
    if use_unicode:
        timeit(
            setup='fmt="{0}{1}{2}"*1024; args=(%s, %s, %s)' % (LONG_ASCII, LONG_BMP, LONG_INT),
            stmt='fmt.format(*args)')
    timeit(
        setup='fmt="{0}-"*1024; arg=' + LONG_ASCII,
        stmt='fmt.format(arg)')
    timeit(
        setup='fmt="{0}-"*1024; arg=' + LONG_INT,
        stmt='fmt.format(arg)')
    timeit(
        setup='fmt="{0}-{1}="*1024; args=(%s, %s)' % (LONG_ASCII, LONG_INT),
        stmt='fmt.format(*args)')
    if use_unicode:
        timeit(
            setup='fmt="{0}-{1}={2}#"*1024; args=(%s, %s, %s)' % (LONG_ASCII, LONG_BMP, LONG_INT),
            stmt='fmt.format(*args)')


def format_keywords():
    # Keywords
    timeit(
        setup='s="The {k1} is {k2} the {k3}."; args={"k1": "x", "k2": "y", "k3": "z"}',
        stmt='s.format(**args)')
    timeit(
        setup='s="The %(k1)s is %(k2)s the %(k3)s."; args={"k1":"x","k2":"y","k3":"z",}',
        stmt='s % args')


def format_align_to_width_chars():
    if use_unicode:
        FILL = ('', BMP_LIT)
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


def format_number_in_the_locale():
    # Format number in the locale
    for arg in INT_ARGS:
        timeit('fmt.format(arg)', 'fmt="{:,}"; arg=%s;' % arg)


def str_int():
    # str(int)
    for arg in INT_ARGS:
        timeit(setup='number=' + arg, stmt='str(number)')


BENCHMARKS = [
    'basic_format_short_ascii_output',
    'basic_format_long_output',
    'format_ascii_prefix_short_output',
    'format_ascii_suffix_short_output',
    'format_bmp_prefix_suffix_short_output',
    'format_huge_output_with_prefix_suffix',
    'format_many_short_args',
    'format_many_long_args',
    'format_keywords',
    'format_align_to_width_chars',
    'format_number_in_the_locale',
    'str_int',
]


def add_cmdline_args(cmd, args):
    if args.benchmark:
        cmd.append(args.benchmark)


def main():
    global timeit

    runner = perf.Runner(add_cmdline_args=add_cmdline_args)
    cmd = runner.argparser
    choices = sorted(BENCHMARKS)
    cmd.add_argument('benchmark', nargs='?', choices=choices)

    def timeit(stmt, setup):
        name = "%s; %s" % (setup, stmt)
        runner.timeit(name, stmt, setup)

    args = runner.parse_args()
    name = args.benchmark
    if not name:
        for name in BENCHMARKS:
            bench = globals()[name]
            bench()
    else:
        bench = globals()[name]
        bench()


if __name__ == "__main__":
    main()
