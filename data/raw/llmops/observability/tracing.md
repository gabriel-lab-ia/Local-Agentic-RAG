---
source_id: llmops_tracing
title: "Tracing and Observability for LLM Applications"
domain: llmops
topic: tracing
url: "https://opentelemetry.io/docs/concepts/signals/traces/"
license: Apache-2.0
language: en
source_type: engineering_synthesis
---

# LLM tracing and observability

LLM applications contain several probabilistic and external components.
Tracing connects the complete request path into one diagnosable execution.

## Trace structure

A trace may contain spans for:

```text
HTTP request
├── input validation
├── query embedding
├── vector search
├── reranking
├── prompt construction
├── model generation
├── tool execution
└── response formatting
```

## Span attributes

Useful attributes include:

- trace and request identifiers;
- component name;
- model and version;
- embedding model;
- retrieval limit;
- result count;
- token counts;
- latency;
- retry count;
- status;
- cache outcome;
- tool name;
- corpus or index version.

Avoid high-cardinality attributes that cannot be queried efficiently.

## Prompt and response privacy

Full prompts, retrieved documents, tool arguments, and generated responses
may contain private or regulated data.

Apply:

- redaction;
- sampling;
- truncation;
- access control;
- encryption;
- retention policy;
- explicit consent and classification.

## Metrics

Important metrics include:

- end-to-end latency;
- time to first token;
- generation duration;
- input and output token count;
- retrieval latency;
- tool latency;
- failure rate;
- timeout rate;
- citation rate;
- cache hit rate;
- cost or compute estimate.

## Quality telemetry

Operational telemetry can include:

- user feedback;
- retrieval confidence;
- grounding checks;
- citation validity;
- refusal rate;
- fallback rate;
- no-answer rate.

Quality indicators should not be confused with verified truth.

## Correlation

Deployment version, prompt version, model version, corpus version, and
evaluation version must be correlated with every production trace.

## Engineering guidance

Instrument component boundaries.
Propagate trace context across workers and tools.
Never log secrets.
Sample intentionally.
bound trace payload size.
connect traces to offline evaluation.
use telemetry to diagnose, not merely collect.
