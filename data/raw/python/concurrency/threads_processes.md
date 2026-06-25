---
source_id: python_threads_processes
title: "Threads and Processes in Python Systems"
domain: python
topic: parallelism
url: "https://docs.python.org/3.11/library/concurrency.html"
license: PSF-2.0
language: en
source_type: official_documentation_summary
---

# Threads and processes

Threads share process memory. Processes have separate memory spaces.
The correct choice depends on workload, communication cost, isolation,
runtime behavior, and deployment constraints.

## Threads

Threads are useful for overlapping blocking I/O and integrating libraries
that are not asynchronous.

Shared memory makes communication convenient but introduces synchronization
requirements.

```python
from threading import Lock

class Counter:
    def __init__(self) -> None:
        self._value = 0
        self._lock = Lock()

    def increment(self) -> None:
        with self._lock:
            self._value += 1
```

Correctness must not depend on operations appearing atomic in one CPython
implementation.

## Global interpreter lock

In standard CPython 3.11, the GIL generally prevents multiple threads from
executing Python bytecode simultaneously in one process.

Threads can still improve I/O-bound throughput. Native libraries may release
the GIL during expensive operations.

## Processes

Multiple processes can execute independently and provide stronger failure
isolation and CPU parallelism.

Costs include:

- process startup;
- serialization;
- inter-process communication;
- duplicated memory;
- model and accelerator initialization;
- more complex shutdown.

## AI workload considerations

Loading a large model separately in every process can exceed RAM or VRAM.
Forking after initializing CUDA or threaded native runtimes can be unsafe.
Process start methods and library documentation must be considered.

## Queues and messages

Prefer message passing over widespread shared mutable state.

A message should have a clear schema, bounded size, identifier,
retry policy, and idempotency behavior.

## Worker shutdown

Production workers need:

- stop signals;
- rejection of new work;
- completion or cancellation of active work;
- resource cleanup;
- bounded shutdown time;
- telemetry for abandoned work.

## Selection rule

Use threads for blocking I/O and compatible native operations.
Use processes for isolated CPU-bound Python tasks.
Use asyncio for cooperative high-concurrency I/O.
Use vectorization, native extensions, PyTorch, or CUDA for numerical work.
Benchmark with representative payloads before deciding.
