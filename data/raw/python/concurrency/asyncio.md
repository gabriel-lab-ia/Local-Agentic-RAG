---
source_id: python_asyncio_production
title: "Asyncio for Production Services"
domain: python
topic: asynchronous_concurrency
url: "https://docs.python.org/3.11/library/asyncio.html"
license: PSF-2.0
language: en
source_type: official_documentation_summary
---

# Asyncio for production services

`asyncio` provides cooperative concurrency using an event loop,
coroutines, tasks, futures, queues, synchronization primitives, and
asynchronous network APIs.

It is primarily useful when many operations spend time waiting for I/O.

## Coroutines and tasks

Calling an async function creates a coroutine object. It does not execute
the body immediately.

```python
import asyncio

async def fetch_document(document_id: str) -> str:
    await asyncio.sleep(0.01)
    return document_id

async def main() -> None:
    task = asyncio.create_task(fetch_document("doc-1"))
    document = await task
    print(document)

asyncio.run(main())
```

Tasks schedule coroutines for event-loop execution.

## Structured concurrency

Python 3.11 provides `TaskGroup`.

```python
import asyncio

async def collect_all(ids: list[str]) -> list[str]:
    tasks: list[asyncio.Task[str]] = []

    async with asyncio.TaskGroup() as group:
        for document_id in ids:
            tasks.append(
                group.create_task(fetch_document(document_id))
            )

    return [task.result() for task in tasks]
```

The task group waits for its tasks and coordinates failure propagation.

## Timeouts

External operations need bounded duration.

```python
import asyncio

async def bounded_fetch() -> str:
    async with asyncio.timeout(5):
        return await fetch_document("doc-1")
```

A timeout policy should reflect upstream budgets and retry strategy.

## Cancellation

Cancellation is part of the contract of async code.

```python
async def worker() -> None:
    try:
        await consume_queue()
    except asyncio.CancelledError:
        await flush_pending_metrics()
        raise
```

Cleanup may be performed, but cancellation should normally be propagated.

## Blocking the event loop

CPU-heavy work and synchronous blocking I/O prevent other tasks from
progressing.

```python
result = await asyncio.to_thread(blocking_function, argument)
```

Moving work to a thread prevents event-loop blocking, but does not make
CPU-bound Python execution inherently parallel.

## Backpressure

Unlimited concurrency can overload databases, embedding services,
model servers, and memory.

```python
semaphore = asyncio.Semaphore(8)

async def limited_fetch(document_id: str) -> str:
    async with semaphore:
        return await fetch_document(document_id)
```

Bounded queues and semaphores are common backpressure mechanisms.

## Common failure modes

Creating a coroutine without awaiting it.
Calling blocking libraries in async routes.
Launching unlimited tasks.
Swallowing cancellation.
Sharing clients across incompatible event loops.
Creating event loops inside library functions.
Forgetting graceful shutdown.

## Decision guidance

Use asyncio for high-concurrency I/O-bound services.
Use synchronous code when concurrency adds no operational value.
Use processes, native code, CUDA, or vectorized libraries for CPU-heavy work.
Measure throughput, latency, queue depth, timeout rate, and cancellation.
