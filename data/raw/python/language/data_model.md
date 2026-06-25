---
source_id: python_data_model
title: "Python Data Model for Production Systems"
domain: python
topic: language_runtime
url: "https://docs.python.org/3.11/reference/datamodel.html"
license: PSF-2.0
language: en
source_type: official_documentation_summary
---

# Python data model

Python programs operate through objects. Every object has an identity, a
type, and a value. Identity distinguishes one object from another, type
determines supported operations, and value represents current state.

## Identity, equality, and mutability

`is` compares identity. `==` asks objects whether their values should be
considered equivalent. These operations answer different questions.

Immutable objects cannot have their visible value changed after creation.
Common examples include integers, strings, bytes, and tuples containing
immutable values. Mutable objects include lists, dictionaries, sets, and
most application-defined instances.

```python
first = {"model": "qwen"}
second = {"model": "qwen"}

assert first == second
assert first is not second
```

Do not use `is` for ordinary value comparison. A production bug can appear
to work for small integers or interned strings and fail with other values.

## Names and references

Assignment binds a name to an object. It does not copy the object.

```python
configuration = {"batch_size": 16}
alias = configuration
alias["batch_size"] = 32

assert configuration["batch_size"] == 32
```

Shared mutable references must be intentional. At service boundaries,
prefer immutable value objects, validated schemas, or defensive copies
when ownership is unclear.

## Attribute access

Attribute lookup is controlled by the object model. Important hooks include:

- `__getattribute__` for all attribute access;
- `__getattr__` as a fallback for missing attributes;
- `__setattr__` for assignment;
- `__delattr__` for deletion;
- descriptors defined with `__get__`, `__set__`, or `__delete__`.

Overriding these hooks can enable proxies, lazy loading, validation, and
instrumentation. It can also make code difficult to reason about. Use them
only when a simpler explicit API is insufficient.

## Equality and hashing contracts

Objects used as dictionary keys or set members require stable hashing.

A core contract is:

```text
if a == b, then hash(a) == hash(b)
```

Mutable state that participates in equality should not participate in a
hash while the object is stored in a hash-based collection.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ModelVersion:
    model_name: str
    version: str
```

Frozen value objects are often appropriate for identifiers, configuration
keys, cache keys, and immutable domain values.

## Resource and lifecycle considerations

CPython uses reference counting plus cyclic garbage collection, but
production code must not depend on object destruction timing for releasing
files, locks, sockets, transactions, or GPU resources.

Use deterministic lifecycle management:

```python
with open("metrics.jsonl", "a", encoding="utf-8") as stream:
    stream.write('{"event":"training_started"}\n')
```

## Engineering guidance

Prefer explicit domain methods over magical attribute behavior.
Treat mutation and ownership as architectural decisions.
Keep equality and hashing semantics stable.
Avoid relying on implementation-specific object destruction behavior.
Use dataclasses for value-oriented records, not as an automatic replacement
for domain modeling.
