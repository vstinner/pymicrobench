************
pymicrobench
************

.. image:: https://travis-ci.com/vstinner/pymicrobench.svg?branch=master
   :alt: Build status of pymicrobench on Travis CI
   :target: https://travis-ci.com/github/vstinner/pymicrobench

My collection of Python microbenchmarks written for CPython.

Benchmarks were written to make sure that a change makes CPython faster.

The code is distributed under the MIT license: see the COPYING file.

Benchmarks were written in 2016, and so mostly for CPython 3.6.

The `Python perf module <http://perf.readthedocs.io/>`_ is needed by
benchmarks. Install perf using::

    python3 -m pip install -U perf

Read perf documentation to see how to run stable benchmarks (ex: tune your
system for benchmarking).
