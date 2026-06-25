---
source_id: mlops_mlflow_model_registry
title: "Model Registry and Lifecycle Governance"
domain: mlops
topic: model_registry
url: "https://mlflow.org/docs/latest/ml/model-registry/"
license: Apache-2.0
language: en
source_type: official_documentation_summary
---

# Model registry

A model registry manages model versions and the metadata required to move
models through validation, deployment, rollback, and retirement.

## Registered models and versions

A registered model represents a logical model product.

Each new artifact can create a model version with metadata linking it to:

- experiment run;
- source code;
- dataset;
- evaluation;
- model signature;
- owner;
- deployment history.

## Aliases

Aliases provide stable names for selected versions.

Examples:

```text
champion
challenger
candidate
production
shadow
```

Deployment systems can resolve an alias rather than embedding a numeric
model version into application code.

## Promotion policy

Registration must not imply production approval.

Promotion should require evidence such as:

- minimum predictive metrics;
- subgroup evaluation;
- schema compatibility;
- latency and memory limits;
- security validation;
- reproducibility;
- human approval where required.

## Model signatures

A model signature describes expected inputs and outputs.

Signatures help detect:

- missing fields;
- incorrect types;
- shape mismatch;
- incompatible serving payloads;
- train-serving skew.

## Lineage

A production model version should be traceable to:

```text
deployment
→ registry version
→ experiment run
→ code revision
→ dataset version
→ configuration
→ evaluation report
```

## Rollback and retirement

A registry should support rollback to a previously validated version.

Retired versions should remain auditable even when they are no longer
eligible for deployment.

## Governance guidance

Use immutable model versions.
Use aliases for deployment intent.
Require explicit promotion gates.
Record approval decisions.
Preserve lineage.
Never overwrite historical model evidence.
