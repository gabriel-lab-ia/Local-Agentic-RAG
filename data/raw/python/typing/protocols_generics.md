---
source_id: python_protocols_generics
title: "Protocols and Generics for Extensible Python Systems"
domain: python
topic: typing_architecture
url: "https://docs.python.org/3.11/library/typing.html"
license: PSF-2.0
language: en
source_type: official_documentation_summary
---

# Protocols and generics

Protocols describe behavior structurally: an object satisfies a protocol
when it provides the required members. Explicit inheritance is not required
for static compatibility.

Generics preserve relationships between input and output types.

## Structural interfaces

```python
from typing import Protocol

class Embedder(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]:
        ...
```

Any class with a compatible `embed` method can satisfy this interface.

```python
class OllamaEmbedder:
    def embed(self, texts: list[str]) -> list[list[float]]:
        ...
```

This reduces coupling between application logic and infrastructure
implementations.

## Dependency inversion

Domain services should depend on the smallest capability they require.

```python
class VectorIndex(Protocol):
    def search(
        self,
        query_embedding: list[float],
        limit: int,
    ) -> list[str]:
        ...


class Retriever:
    def __init__(self, index: VectorIndex) -> None:
        self._index = index
```

The retriever does not need to know whether the implementation uses
ChromaDB, PostgreSQL with pgvector, an in-memory fake, or a remote service.

## Generic repositories

Python 3.11-compatible syntax:

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Repository(Generic[T]):
    def get(self, identifier: str) -> T | None:
        ...
```

Generics are valuable when the same operation preserves a meaningful type
relationship. Do not introduce type variables when every implementation
immediately returns unrelated dynamic data.

## Covariance and contravariance

Variance describes how relationships between types propagate through
generic containers or callables.

Read-only producers may support covariance.
Consumers may support contravariance.
Mutable containers are commonly invariant because they both produce and
consume values.

Variance should be introduced only when required by a real interface.
Incorrect variance declarations can make APIs unsound or difficult to use.

## Runtime-checkable protocols

`@runtime_checkable` enables limited `isinstance` checks based on member
presence. It does not validate full method signatures or semantic behavior.

Runtime protocol checks must not replace boundary validation or tests.

## Testing with protocols

Protocol-based architecture supports lightweight fakes:

```python
class FakeEmbedder:
    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0, 1.0] for _ in texts]
```

This is usually simpler than mocking deep implementation details.

## Engineering guidance

Define protocols near the consumer.
Keep protocols small and capability-oriented.
Prefer composition over inheritance hierarchies.
Use generics to preserve genuine type relationships.
Avoid abstract interfaces with dozens of unrelated methods.
Test semantic contracts, not merely attribute presence.
