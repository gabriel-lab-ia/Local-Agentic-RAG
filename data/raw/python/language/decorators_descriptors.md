---
source_id: python_decorators_descriptors
title: "Decorators and Descriptors in Python"
domain: python
topic: metaprogramming
url: "https://docs.python.org/3.11/howto/descriptor.html"
license: PSF-2.0
language: en
source_type: official_documentation_summary
---

# Decorators and descriptors

Decorators transform or wrap functions, methods, or classes. Descriptors
customize attribute access. These mechanisms power many frameworks, but
they must preserve transparency and predictable behavior.

## Function decorators

A decorator receives a callable and returns a callable.

```python
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def measure_latency(function: Callable[P, R]) -> Callable[P, R]:
    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = perf_counter()
        try:
            return function(*args, **kwargs)
        finally:
            elapsed_ms = (perf_counter() - start) * 1000
            print({"function": function.__name__, "latency_ms": elapsed_ms})

    return wrapper
```

`functools.wraps` preserves metadata such as the wrapped function name,
documentation, annotations, and the `__wrapped__` reference.

## Decorator design principles

A production decorator should:

- preserve the original callable contract;
- avoid silently changing return types;
- clearly define exception behavior;
- avoid storing unsafe shared mutable state;
- support synchronous and asynchronous functions intentionally;
- expose metrics without logging secrets or raw user data.

Decorators are suitable for cross-cutting concerns such as tracing,
authorization, retries, caching, validation, and timing. They should not
hide core business workflows.

## Descriptor protocol

An object is a descriptor when its class defines one or more of:

```python
__get__
__set__
__delete__
```

A descriptor can control how an attribute is read, assigned, or deleted.

```python
class PositiveFloat:
    def __set_name__(self, owner: type, name: str) -> None:
        self.storage_name = f"_{name}"

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value: float) -> None:
        value = float(value)
        if value <= 0:
            raise ValueError("value must be positive")
        setattr(instance, self.storage_name, value)


class TrainingConfig:
    learning_rate = PositiveFloat()

    def __init__(self, learning_rate: float) -> None:
        self.learning_rate = learning_rate
```

## Data and non-data descriptors

A descriptor defining `__set__` or `__delete__` is generally a data
descriptor. Data descriptors take precedence over instance attributes.

A descriptor defining only `__get__` is a non-data descriptor. Instance
attributes can typically override it.

This distinction matters when building ORMs, validators, dependency
containers, lazy fields, and framework internals.

## Properties and methods

`property` is implemented through the descriptor protocol. Functions stored
on classes also participate in descriptor binding, producing bound methods
when accessed through an instance.

Use `property` when an attribute-like interface is clearer than an explicit
method and the operation is inexpensive and unsurprising. Do not hide slow
I/O, network calls, or database queries behind a property.

## Risks

Excessive metaprogramming increases debugging cost.
Descriptor lookup rules are subtle.
Decorators can break introspection and type checking.
Hidden I/O and mutation create surprising APIs.
Framework magic should remain smaller than the domain logic it supports.
