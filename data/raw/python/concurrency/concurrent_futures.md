---
source_id: python_concurrent_futures
title: "Concurrent Futures for Managed Task Execution"
domain: python
topic: executor_concurrency
url: "https://docs.python.org/3.11/library/concurrent.futures.html"
license: PSF-2.0
language: en
source_type: official_documentation_summary
---

# concurrent.futures

`concurrent.futures` provides a high-level interface for submitting
callables to thread or process executors.

## Thread pool

```python
from concurrent.futures import ThreadPoolExecutor

def read_document(path: str) -> str:
    with open(path, encoding="utf-8") as stream:
        return stream.read()

paths = ["a.md", "b.md", "c.md"]

with ThreadPoolExecutor(max_workers=4) as executor:
    documents = list(executor.map(read_document, paths))
```

Thread pools are commonly suitable for blocking I/O.

## Process pool

```python
from concurrent.futures import ProcessPoolExecutor

def expensive_score(values: list[float]) -> float:
    return sum(value * value for value in values)

with ProcessPoolExecutor(max_workers=4) as executor:
    scores = list(executor.map(expensive_score, batches))
```

Submitted functions and arguments must satisfy process serialization and
importability requirements.

## Futures

`submit` returns a Future representing eventual completion.

```python
with ThreadPoolExecutor(max_workers=4) as executor:
    future = executor.submit(read_document, "document.md")

    try:
        content = future.result(timeout=10)
    except TimeoutError:
        future.cancel()
        raise
```

Cancellation only succeeds when execution has not already started.

## Completion order

```python
from concurrent.futures import as_completed

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(read_document, path)
        for path in paths
    ]

    for future in as_completed(futures):
        process(future.result())
```

## Deadlocks

Pool tasks can deadlock when they wait on other tasks submitted to the same
exhausted pool. Avoid nested blocking dependencies inside workers.

## Capacity

More workers do not guarantee more throughput. Excessive workers can cause
context switching, upstream overload, memory pressure, rate-limit failures,
and database connection exhaustion.

## Error handling

Exceptions raised by tasks are surfaced when retrieving the future result.
Capture per-task failures when partial success is acceptable.

## Engineering guidance

Bound the worker count.
Define task timeouts.
Avoid hidden global mutable state.
Do not submit unbounded work.
Preserve input identifiers for tracing.
Use process pools cautiously with large models and GPU runtimes.
