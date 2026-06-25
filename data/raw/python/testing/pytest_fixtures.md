---
source_id: pytest_fixtures_engineering
title: "Pytest Fixtures for Reliable Python Systems"
domain: python
topic: testing
url: "https://docs.pytest.org/en/stable/explanation/fixtures.html"
license: MIT
language: en
source_type: official_documentation_summary
---

# Pytest fixtures

Fixtures provide explicit setup, dependencies, reusable test data,
resources, and teardown.

## Basic fixture

```python
import pytest

@pytest.fixture
def sample_documents() -> list[str]:
    return [
        "PyTorch autograd computes gradients.",
        "MLflow tracks experiments.",
    ]

def test_documents_are_not_empty(
    sample_documents: list[str],
) -> None:
    assert all(sample_documents)
```

Test functions request fixtures by parameter name.

## Yield fixtures

Code after `yield` performs teardown.

```python
from collections.abc import Iterator
from pathlib import Path
import pytest

@pytest.fixture
def temporary_corpus(
    tmp_path: Path,
) -> Iterator[Path]:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    yield corpus
```

Prefer built-in temporary-path fixtures over manually managing global
test directories.

## Fixture scopes

Common scopes include function, class, module, package, and session.

Wider scopes reduce repeated setup but increase shared-state risk.

Use the narrowest scope that meets performance requirements.

## Fixture dependencies

```python
@pytest.fixture
def fake_embedder():
    return FakeEmbedder()

@pytest.fixture
def retriever(fake_embedder):
    return Retriever(embedder=fake_embedder)
```

A fixture graph should remain understandable. Deep fixture chains can hide
important test setup.

## Factories

A fixture can return a factory when tests need multiple customized objects.

```python
@pytest.fixture
def make_chunk():
    def factory(text: str, domain: str = "python"):
        return {"text": text, "domain": domain}

    return factory
```

## Autouse fixtures

Autouse fixtures run without explicit test parameters. They are useful for
universal isolation, but can conceal behavior. Use them sparingly.

## Testing external systems

Unit tests should use small fakes at explicit interfaces.
Integration tests may start real databases or services.
Mark slow and environment-dependent tests clearly.

## Engineering guidance

Keep fixtures deterministic.
Avoid network access in unit tests.
Prevent session fixtures from leaking mutable state.
Make teardown resilient.
Prefer meaningful test data over oversized production copies.
Test behavior through public interfaces.
