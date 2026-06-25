---
source_id: python_iterators_generators
title: "Iterators, Generators, and Streaming Python"
domain: python
topic: iteration_and_streaming
url: "https://docs.python.org/3.11/reference/expressions.html"
license: PSF-2.0
language: en
source_type: official_documentation_summary
---

# Iterators and generators

Iteration separates producing values from consuming them. This permits
lazy computation, streaming pipelines, bounded memory use, and composition.

## Iterable and iterator

An iterable can produce an iterator. An iterator returns one item at a time
through `__next__` and raises `StopIteration` when exhausted.

```python
numbers = [1, 2, 3]
iterator = iter(numbers)

assert next(iterator) == 1
assert next(iterator) == 2
```

Iterators are stateful and normally single-use.

## Generator functions

A function containing `yield` creates a generator iterator.

```python
from collections.abc import Iterator

def batches(
    values: list[str],
    size: int,
) -> Iterator[list[str]]:
    if size < 1:
        raise ValueError("size must be positive")

    for start in range(0, len(values), size):
        yield values[start : start + size]
```

This pattern is useful for embedding batches, database pagination,
model inference batches, and file processing.

## Streaming files

```python
from collections.abc import Iterator
from pathlib import Path

def nonempty_lines(path: Path) -> Iterator[str]:
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            value = line.strip()

            if value:
                yield value
```

The file remains open while iteration is active. Consumers should not
retain a partially consumed generator indefinitely.

## Generator expressions

```python
squared = (value * value for value in range(1_000_000))
```

Generator expressions avoid materializing the entire result, but they do
not make an expensive algorithm intrinsically faster.

## yield from

`yield from` delegates iteration to another iterable.

```python
def all_chunks(documents: list[list[str]]):
    for document_chunks in documents:
        yield from document_chunks
```

## send, throw, and close

Generator objects also support advanced control methods. These features
enable coroutine-like behavior but can produce difficult control flow.
Prefer ordinary iteration, async generators, queues, or explicit state
machines unless bidirectional generator communication is clearly justified.

## Async generators

An asynchronous generator uses `async def` with `yield`.

```python
from collections.abc import AsyncIterator

async def stream_events() -> AsyncIterator[dict[str, str]]:
    while event := await receive_event():
        yield event
```

Async generators are useful when each item requires asynchronous I/O.

## Failure and cleanup

Exceptions raised by the producer propagate to the consumer.
Cleanup should be protected with `try/finally` or context managers.

## Engineering guidance

Use iterators for single-pass streams.
Use sequences when repeated access and indexing are required.
Avoid converting large streams to lists without a memory budget.
Make ownership and resource lifetime explicit.
Document whether an iterable can be consumed more than once.
