---
source_id: mlops_model_serving
title: "Reliable Model Serving Architecture"
domain: mlops
topic: model_serving
url: "https://mlflow.org/docs/latest/ml/deployment/"
license: Apache-2.0
language: en
source_type: engineering_synthesis
---

# Model serving

Model serving exposes trained models through a controlled inference
interface.

A serving system must preserve correctness, latency, availability,
observability, and model lineage.

## Request lifecycle

A typical inference request passes through:

```text
authentication
→ authorization
→ schema validation
→ preprocessing
→ model inference
→ post-processing
→ response
→ telemetry
```

Every stage can fail and requires bounded behavior.

## Initialization

Models should generally load during application startup rather than once
per request.

Startup should validate:

- model artifact;
- model signature;
- dependency compatibility;
- device availability;
- memory capacity;
- required configuration.

## Health endpoints

Liveness indicates whether the process is running.

Readiness indicates whether the service can safely accept inference
requests.

A process may be alive but not ready while a model is loading.

## Batching

Batching can improve accelerator utilization but adds queue delay.

A batching policy should define:

- maximum batch size;
- maximum waiting time;
- memory limits;
- fairness;
- timeout behavior.

## Deployment strategies

Common strategies include:

- rolling deployment;
- blue-green deployment;
- canary deployment;
- shadow deployment;
- champion-challenger evaluation.

## Monitoring

Track:

- request rate;
- latency percentiles;
- error rate;
- timeout rate;
- queue depth;
- batch size;
- resource use;
- model version;
- input drift;
- prediction distribution;
- outcome metrics when labels arrive.

## Safety

Validate inputs before expensive inference.
Bound payload and sequence size.
Avoid executing model-generated code.
Isolate untrusted artifacts.
Protect endpoints with authorization and rate limits.

## Engineering guidance

Separate serving APIs from training code.
Load immutable model versions.
expose model version in telemetry.
support graceful shutdown.
define rollback before deployment.
test cold start and degraded dependencies.
