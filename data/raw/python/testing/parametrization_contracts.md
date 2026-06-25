---
source_id: pytest_parametrization_contracts
title: "Parametrized and Contract Testing with Pytest"
domain: python
topic: testing_contracts
url: "https://docs.pytest.org/en/stable/how-to/parametrize.html"
license: MIT
language: en
source_type: official_documentation_summary
---

# Parametrization and contract testing

Parametrization executes the same test logic with multiple inputs,
expected outputs, configurations, or implementations.

## Table-driven tests

```python
import pytest

@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("python", "PYTHON"),
        ("mlops", "MLOPS"),
        ("llmops", "LLMOPS"),
    ],
)
def test_normalization(
    value: str,
    expected: str,
) -> None:
    assert value.upper() == expected
```

## Case identifiers

```python
@pytest.mark.parametrize(
    "batch_size",
    [
        pytest.param(1, id="minimum"),
        pytest.param(16, id="default"),
        pytest.param(128, id="large"),
    ],
)
def test_valid_batch_sizes(batch_size: int) -> None:
    assert batch_size > 0
```

Descriptive IDs improve failure reports.

## Exception contracts

```python
@pytest.mark.parametrize("invalid_size", [0, -1, -32])
def test_rejects_invalid_batch_size(
    invalid_size: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="positive",
    ):
        validate_batch_size(invalid_size)
```

## Testing multiple implementations

A protocol can have a reusable contract test.

```python
@pytest.mark.parametrize(
    "embedder_factory",
    [FakeEmbedder, DeterministicEmbedder],
)
def test_embedder_contract(embedder_factory) -> None:
    embedder = embedder_factory()
    vectors = embedder.embed(["a", "b"])

    assert len(vectors) == 2
    assert all(vector for vector in vectors)
```

Contract tests verify common behavior without asserting implementation
details.

## Boundary cases

Include:

- empty values;
- minimum and maximum allowed values;
- malformed data;
- duplicate identifiers;
- Unicode;
- cancellation and timeout;
- partial upstream failure;
- deterministic repeatability.

## Avoid combinatorial explosion

Parametrization should represent meaningful equivalence classes and risks.
Do not generate enormous Cartesian products without a testing strategy.

Property-based testing is useful when invariants matter across broad input
spaces. Example-based tests remain important for known regressions and
domain scenarios.

## Engineering guidance

Give cases meaningful IDs.
Separate test data from complex test logic.
Test stable contracts.
Avoid asserting private implementation structure.
Keep failures independently diagnosable.
Turn every fixed production defect into a regression case.
