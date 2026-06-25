---
source_id: python_dependency_injection
title: "Dependency Injection and Composition Roots in Python"
domain: python
topic: software_architecture
url: "https://docs.python.org/3.11/tutorial/classes.html"
license: PSF-2.0
language: en
source_type: engineering_synthesis
---

# Dependency injection

Dependency injection means that an object receives required collaborators
instead of constructing hidden global dependencies internally.

Python does not require a dependency injection framework. Constructor
injection and explicit composition are often sufficient.

## Constructor injection

```python
from typing import Protocol

class ExperimentTracker(Protocol):
    def log_metric(self, name: str, value: float) -> None:
        ...

class Trainer:
    def __init__(self, tracker: ExperimentTracker) -> None:
        self._tracker = tracker

    def record_loss(self, loss: float) -> None:
        self._tracker.log_metric("loss", loss)
```

The trainer depends on a capability, not directly on MLflow.

## Composition root

Construct concrete dependencies at one explicit application boundary.

```python
def build_application() -> Trainer:
    tracker = MlflowExperimentTracker(
        tracking_uri="http://localhost:5000"
    )
    return Trainer(tracker=tracker)
```

CLI commands, HTTP startup code, or worker bootstrapping are common
composition roots.

## Configuration

Parse and validate configuration once, then inject typed configuration.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class OllamaSettings:
    base_url: str
    model: str
    timeout_seconds: float
```

Do not scatter direct environment-variable reads across domain and
application modules.

## Lifetimes

Dependencies have lifetimes:

- process-wide: immutable configuration, connection pools;
- request-scoped: request context, correlation identifiers;
- operation-scoped: database transaction, temporary workspace;
- transient: small stateless adapters.

Wrong lifetime choices create leaked connections, unsafe shared state, and
expensive repeated initialization.

## Testing

Explicit dependencies allow simple fakes:

```python
class InMemoryTracker:
    def __init__(self) -> None:
        self.metrics: list[tuple[str, float]] = []

    def log_metric(self, name: str, value: float) -> None:
        self.metrics.append((name, value))
```

Tests can assert observable behavior without patching global module state.

## Framework containers

A framework container can help with large dependency graphs and request
scopes. It can also hide control flow. Use a container when lifecycle
management provides clear value, and keep construction observable.

## Anti-patterns

Service locator calls from arbitrary modules.
Global mutable singletons.
Creating database or model clients during import.
Domain classes importing concrete infrastructure.
Dependency graphs controlled by string names without validation.
Mocking internals instead of injecting stable interfaces.

## Engineering rule

Prefer explicit constructor dependencies.
Keep the composition root near application startup.
Inject capabilities through small protocols.
Make lifecycle and ownership visible.
Use frameworks only when they reduce, rather than conceal, complexity.
