---
source_id: python_type_system
title: "Python Type System for Large Codebases"
domain: python
topic: typing
url: "https://docs.python.org/3.11/library/typing.html"
license: PSF-2.0
language: en
source_type: official_documentation_summary
---

# Python type system

Type annotations document contracts and support static analysis. Python
does not enforce ordinary annotations at runtime. Validation, parsing, and
runtime enforcement require explicit code or dedicated libraries.

## Function contracts

```python
from collections.abc import Sequence

def mean(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("values cannot be empty")
    return sum(values) / len(values)
```

Annotations should communicate stable interfaces, not expose every internal
implementation detail.

## Avoid uncontrolled Any

`Any` disables useful checking across the boundary where it appears.
It is appropriate at genuinely dynamic boundaries, but values should be
validated and narrowed quickly.

```python
from typing import Any

def parse_batch_size(payload: dict[str, Any]) -> int:
    raw = payload.get("batch_size")
    if not isinstance(raw, int):
        raise TypeError("batch_size must be an integer")
    if raw < 1:
        raise ValueError("batch_size must be positive")
    return raw
```

## Union and optional values

In Python 3.11:

```python
def find_checkpoint(name: str) -> str | None:
    ...
```

A nullable return type forces callers to address the missing-value case.
Do not use `None` when the domain needs to distinguish several failure
states; use an explicit result object or typed exception hierarchy.

## Typed dictionaries

`TypedDict` describes dictionary-shaped records for static analysis.

```python
from typing import TypedDict

class PredictionPayload(TypedDict):
    request_id: str
    features: list[float]
```

For complex behavior or strong runtime invariants, prefer classes or
validated schemas over raw dictionaries.

## Literal values

```python
from typing import Literal

Device = Literal["cpu", "cuda", "auto"]
```

`Literal` is useful when a finite set of values is part of the public
contract. Enums may be preferable when behavior or runtime identity matters.

## Callable contracts

```python
from collections.abc import Callable

Metric = Callable[[list[float], list[float]], float]
```

For callables with richer methods or overloaded behavior, define a Protocol
rather than forcing an opaque `Callable` signature.

## Narrowing

Use explicit checks to narrow unknown values.

```python
def normalize(value: object) -> float:
    if isinstance(value, int | float):
        return float(value)
    raise TypeError("numeric value required")
```

## Architectural policy

Type public APIs thoroughly.
Keep internal inference practical rather than ceremonial.
Run a static checker in CI.
Avoid casts that merely silence legitimate errors.
Validate data at external boundaries.
Treat types as executable design feedback, not as documentation decoration.
