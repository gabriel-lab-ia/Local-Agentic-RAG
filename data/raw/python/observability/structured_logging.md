---
source_id: python_structured_logging
title: "Structured Logging for Production Python Systems"
domain: python
topic: observability
url: "https://docs.python.org/3.11/library/logging.html"
license: PSF-2.0
language: en
source_type: official_documentation_summary
---

# Structured logging

Logging records discrete events emitted by software. Production logs should
be machine-readable, correlated across components, bounded in volume, and
safe for operational use.

## Logging architecture

Python logging separates responsibilities:

- loggers create records;
- handlers deliver records;
- formatters serialize records;
- filters enrich or reject records.

Libraries should obtain a module logger and should not configure global
handlers during import.

```python
import logging

logger = logging.getLogger(__name__)

def load_model(model_name: str) -> None:
    logger.info(
        "model_load_started",
        extra={"model_name": model_name},
    )
```

## Structured event fields

Useful fields include:

- event name;
- timestamp;
- severity;
- service and component;
- environment;
- request, trace, and span identifiers;
- model and model version;
- latency and status;
- bounded error classification.

The message should identify the event. Dynamic values should be separate
fields rather than embedded into prose.

## Correlation

A request identifier or trace identifier should cross API, worker, database,
retrieval, model, and tool boundaries.

`contextvars` can carry request-scoped values in async applications without
relying on unsafe process-wide mutable state.

## Severity

DEBUG is diagnostic detail.
INFO is normal lifecycle and business events.
WARNING is degraded or unexpected but recoverable behavior.
ERROR is a failed operation requiring attention.
CRITICAL is a severe service-level failure.

Severity is not a substitute for metrics or alert policy.

## Sensitive data

Never log passwords, tokens, cookies, private keys, raw authorization
headers, complete prompts containing private data, or unrestricted model
outputs.

Use allowlists, redaction, hashing, truncation, and explicit data
classification.

## Operational guidance

Avoid duplicate handlers.
Avoid logging the same exception at every layer.
Use lazy formatting for expensive values.
Bound payload size and cardinality.
Configure output at the application composition root.
Prefer stable event names for queries and dashboards.
