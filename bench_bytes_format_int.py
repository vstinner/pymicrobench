#!/usr/bin/env python3
"""
Microbenchmark on bytes % args for Python 3:
https://bugs.python.org/issue25349
"""

import perf


COUNT = (1, 5, 10, 25, 100, 200, 500)


def main():
    runner = perf.Runner()

    group = None

    def timeit(setup, stmt):
        name = '%s; %s; %s' % (group, setup, stmt)
        runner.timeit(name, setup=setup, stmt=stmt)

    group = '%i'
    for n in COUNT:
        timeit(setup='n = %s; fmt = b"%%d" * n; arg = tuple([12345]*n)' % n,
               stmt='fmt % arg')

    group = 'x=%i'
    for n in COUNT:
        timeit(setup='n = %s; fmt = b"x=%%d " * n; arg = tuple([12345]*n)' % n,
               stmt='fmt % arg')

    group = '%x'
    for n in COUNT:
        timeit(setup='n = %s; fmt = b"%%d" * n; arg = tuple([12345]*n)' % n,
               stmt='fmt % arg')

    group = 'x=%x'
    for n in COUNT:
        timeit(setup='n = %s; fmt = b"x=%%d " * n; arg = tuple([0xabcdef]*n)' % n,
               stmt='fmt % arg')

    group = 'large int: %i'
    for n in range(0, 201, 50):
        timeit(setup='fmt = b"%%i"; arg = 10 ** %s - 1' % n,
               stmt='fmt % arg')

    group = 'large int: x=%i'
    for n in range(0, 200, 50):
        timeit(setup='fmt = b"x=%%i"; arg = 10 ** %s - 1' % n,
               stmt='fmt % arg')


if __name__ == "__main__":
    main()
