---
source_id: python_profiling
title: "Profiling and Performance Engineering in Python"
domain: python
topic: performance
url: "https://docs.python.org/3.11/library/profile.html"
license: PSF-2.0
language: en
source_type: official_documentation_summary
---

# Profiling and performance engineering

Performance work starts with a measurable objective and representative
workloads. Optimize observed bottlenecks, not intuition.

## Define the objective

Measure the relevant service-level property:

- latency percentiles;
- throughput;
- startup time;
- memory peak;
- GPU utilization;
- cost per request;
- queue wait time;
- batch efficiency.

Average latency alone can hide tail failures.

## Deterministic profiling

`cProfile` records call counts and time spent in functions.

```bash
python -m cProfile -o profile.out application.py
```

Analyze cumulative time when a function delegates expensive work and
internal time when the function itself is expensive.

## Microbenchmarks

Use `timeit` for small isolated operations, not for proving end-to-end
service performance.

Warm caches, compilation, network variance, thread scheduling, and dataset
shape can invalidate naive comparisons.

## Numerical workloads

Prefer vectorized NumPy or PyTorch operations over Python loops when the
operation maps naturally to array computation.

Reduce:

- unnecessary device transfers;
- repeated serialization;
- tiny kernel launches;
- unbounded batching;
- duplicate tokenization or embedding;
- redundant copies.

## Production profiling

A production-safe profiler should have bounded overhead and controlled
access. Correlate profiles with request type, model version, payload size,
hardware, and deployment revision.

## Optimization order

Improve algorithmic complexity first.
Remove unnecessary work.
Batch compatible work.
Cache only stable and reusable results.
Move proven hotspots to vectorized or native execution.
Scale resources after software inefficiencies are understood.

## Engineering guidance

Keep a reproducible benchmark.
Report variance, hardware, versions, and configuration.
Compare correctness before comparing speed.
Reject optimizations that destroy maintainability for negligible gain.
Re-profile after every meaningful change.
