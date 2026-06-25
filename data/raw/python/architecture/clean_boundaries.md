---
source_id: python_clean_boundaries
title: "Clean Architectural Boundaries in Python AI Systems"
domain: python
topic: software_architecture
url: "https://docs.python.org/3.11/tutorial/modules.html"
license: PSF-2.0
language: en
source_type: engineering_synthesis
---

# Clean architectural boundaries

A maintainable AI system separates domain decisions from infrastructure
details. The goal is not to maximize the number of layers. The goal is to
keep change localized and dependencies intentional.

## Typical boundaries

```text
interfaces
├── CLI
├── HTTP API
└── scheduled jobs

application
├── use cases
├── orchestration
└── transaction boundaries

domain
├── entities
├── value objects
├── policies
└── domain errors

infrastructure
├── ChromaDB
├── Ollama
├── PostgreSQL
├── MLflow
└── filesystem
```

Dependencies should generally point toward stable business policies.
Infrastructure adapts external technologies to application-facing
interfaces.

## Example use case

```python
from dataclasses import dataclass
from typing import Protocol

class Retriever(Protocol):
    def retrieve(self, query: str, limit: int) -> list[str]:
        ...

class Generator(Protocol):
    def generate(self, prompt: str) -> str:
        ...

@dataclass(frozen=True)
class Answer:
    text: str
    sources: tuple[str, ...]

class AnswerQuestion:
    def __init__(
        self,
        retriever: Retriever,
        generator: Generator,
    ) -> None:
        self._retriever = retriever
        self._generator = generator

    def execute(self, query: str) -> Answer:
        chunks = self._retriever.retrieve(query, limit=5)
        prompt = self._build_prompt(query, chunks)
        text = self._generator.generate(prompt)
        return Answer(text=text, sources=tuple(chunks))

    @staticmethod
    def _build_prompt(query: str, chunks: list[str]) -> str:
        context = "\n\n".join(chunks)
        return f"Context:\n{context}\n\nQuestion: {query}"
```

This use case contains orchestration but no ChromaDB or HTTP details.

## Boundary validation

Validate untrusted data when it enters the system:

- HTTP payloads;
- environment variables;
- model responses;
- database records;
- retrieved metadata;
- file contents;
- external tool output.

Internal functions can then operate on stronger types and invariants.

## Error translation

Infrastructure errors should be translated into errors meaningful to the
application.

```text
requests.Timeout
→ EmbeddingServiceUnavailable

database connection error
→ PersistenceUnavailable
```

Preserve the original exception as the cause for diagnostics.

## Avoid architecture theater

Warning signs include:

- one class per trivial operation;
- interfaces with only one implementation and no testing benefit;
- domain modules importing web frameworks;
- business rules embedded in route handlers;
- global clients created during import;
- circular imports caused by unclear ownership;
- generic utility modules containing unrelated behavior.

## Decision rule

Introduce a boundary when it isolates volatility, protects a business rule,
improves testability, or supports multiple execution contexts. Do not add a
layer only because a diagram looks more enterprise.
