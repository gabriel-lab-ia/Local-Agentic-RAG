---
source_id: python_exceptions_context_managers
title: "Exceptions and Context Managers in Production Python"
domain: python
topic: error_handling_and_resources
url: "https://docs.python.org/3.11/reference/compound_stmts.html"
license: PSF-2.0
language: en
source_type: official_documentation_summary
---

# Exceptions and context managers

Exceptions communicate that an operation could not satisfy its contract.
Context managers define deterministic setup and cleanup around a block.

## Exception boundaries

Catch exceptions where the program can recover, translate the error,
add useful context, or guarantee cleanup.

Avoid broad handlers that silently discard failures:

```python
try:
    result = execute_training()
except Exception:
    pass
```

Prefer precise handling:

```python
class ModelLoadError(RuntimeError):
    pass


def load_model(path: str) -> bytes:
    try:
        with open(path, "rb") as stream:
            return stream.read()
    except FileNotFoundError as exc:
        raise ModelLoadError(f"model not found: {path}") from exc
```

The `raise ... from exc` syntax preserves causal information.

## Exception hierarchy

Application exceptions should describe domain or operational meaning.

```python
class ApplicationError(Exception):
    pass


class InvalidPredictionInput(ApplicationError):
    pass


class EmbeddingServiceUnavailable(ApplicationError):
    pass
```

Do not create a unique exception for every line of code. Create exceptions
when callers need distinct recovery, reporting, or translation behavior.

## Else and finally

The `else` block runs only when no exception is raised in `try`.
The `finally` block runs whether the operation succeeds or fails.

```python
try:
    connection.begin()
    persist_metrics(connection)
except DatabaseError:
    connection.rollback()
    raise
else:
    connection.commit()
finally:
    connection.close()
```

## Context manager protocol

A synchronous context manager implements `__enter__` and `__exit__`.

```python
class ModelSession:
    def __enter__(self) -> "ModelSession":
        self.open()
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> bool:
        self.close()
        return False
```

Returning `False` allows an active exception to propagate.

## contextlib

Generator-based context managers can be created with `contextlib`.

```python
from collections.abc import Iterator
from contextlib import contextmanager

@contextmanager
def experiment_run(name: str) -> Iterator[dict[str, str]]:
    run = {"name": name, "status": "running"}

    try:
        yield run
    except Exception:
        run["status"] = "failed"
        raise
    else:
        run["status"] = "completed"
```

Exactly one `yield` separates setup from teardown.

## Async context managers

Resources used by asynchronous services may implement
`__aenter__` and `__aexit__`.

```python
async with client.session() as session:
    response = await session.fetch()
```

## Production guidance

Never suppress unexpected exceptions without telemetry.
Translate low-level errors at architectural boundaries.
Preserve exception causes.
Do not use exceptions for ordinary expected branching.
Use context managers for files, locks, sessions, transactions,
temporary directories, spans, and managed model resources.
