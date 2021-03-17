************
pymicrobench
************

.. image:: https://github.com/vstinner/pymicrobench/actions/workflows/build.yml/badge.svg
   :alt: Build status of pymicrobench on GitHub Actions
   :target: https://github.com/vstinner/pymicrobench/actions

My collection of Python microbenchmarks written for CPython.

Benchmarks were written to make sure that a change makes CPython faster.

The code is distributed under the MIT license: see the COPYING file.

Benchmarks were written in 2016, and so mostly for CPython 3.6.

The `Python pyperf module <http://pyperf.readthedocs.io/>`_ is needed by
benchmarks. Install perf using::

    python3 -m pip install -U pyperf

Read pyperf documentation to see how to run stable benchmarks (ex: tune your
system for benchmarking).
