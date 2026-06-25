---
source_id: python_operational_error_handling
title: "Operational Error Handling in Python Services"
domain: python
topic: reliability
url: "https://docs.python.org/3.11/tutorial/errors.html"
license: PSF-2.0
language: en
source_type: official_documentation_summary
---

# Operational error handling

Reliable systems classify failures, preserve causal information, expose
stable public errors, and define recovery behavior.

## Failure classes

Common categories include:

- invalid input;
- expected domain rejection;
- dependency timeout;
- dependency unavailable;
- rate limiting;
- transient conflict;
- corrupted or incompatible data;
- invariant violation;
- operator or configuration error.

Retry policy, status code, alerting, and user communication depend on the
category.

## Translate at boundaries

```python
class EmbeddingUnavailable(RuntimeError):
    pass

def embed(texts: list[str]) -> list[list[float]]:
    try:
        return client.embed(texts)
    except TimeoutError as exc:
        raise EmbeddingUnavailable(
            "embedding service timed out"
        ) from exc
```

Application code should not depend on every exception class emitted by a
concrete HTTP or database library.

## Retry safety

Retry only when the operation is transient and safe to repeat.

Consider:

- idempotency;
- deadline budget;
- exponential backoff;
- jitter;
- maximum attempts;
- overload amplification;
- partial side effects.

A retry loop without a total deadline can extend an outage.

## Public error responses

External responses should be stable and should not expose stack traces,
internal paths, credentials, SQL, or dependency details.

Internal telemetry should retain exception type, cause, stack trace,
operation, request identifier, and bounded context.

## Fail fast versus degrade

Fail startup for invalid mandatory configuration, incompatible schemas, or
missing critical credentials.

Degrade when an optional capability is unavailable and the fallback remains
correct and visible.

Never silently degrade model quality without telemetry and an explicit
product decision.

## Engineering guidance

Preserve causes with exception chaining.
Define recovery at the correct boundary.
Do not catch exceptions that cannot be handled.
Keep user-facing errors stable.
Separate retryable and permanent failures.
Test timeout, cancellation, partial failure, and cleanup behavior.
