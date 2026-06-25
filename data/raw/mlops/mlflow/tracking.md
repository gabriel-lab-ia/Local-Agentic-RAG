---
source_id: mlops_mlflow_tracking
title: "Experiment Tracking with MLflow"
domain: mlops
topic: experiment_tracking
url: "https://mlflow.org/docs/latest/ml/tracking/"
license: Apache-2.0
language: en
source_type: official_documentation_summary
---

# Experiment tracking

Experiment tracking records the evidence required to understand,
reproduce, compare, and audit model-development runs.

A run should connect:

- source code revision;
- dataset version;
- model configuration;
- hyperparameters;
- metrics;
- artifacts;
- environment;
- execution status.

## Experiments and runs

An experiment groups related runs. A run represents one execution of a
training, evaluation, tuning, or validation workflow.

```python
import mlflow

mlflow.set_experiment("fraud-classification")

with mlflow.start_run():
    mlflow.log_param("max_depth", 8)
    mlflow.log_param("class_weight", "balanced")

    mlflow.log_metric("validation_roc_auc", 0.91)
    mlflow.log_metric("validation_recall", 0.87)

    mlflow.log_artifact("reports/confusion_matrix.png")
```

## Parameters, metrics, tags, and artifacts

Parameters describe run configuration and are generally stable during a
run.

Metrics represent numerical observations and may vary over steps or time.

Tags hold searchable metadata such as:

- Git commit;
- dataset identifier;
- model family;
- owner;
- environment;
- evaluation policy.

Artifacts include:

- serialized models;
- plots;
- reports;
- schemas;
- feature definitions;
- evaluation results;
- configuration files.

## Reproducibility

Tracking alone does not guarantee reproducibility.

A reproducible run also requires:

- immutable or versioned data;
- dependency lock state;
- deterministic configuration where practical;
- source revision;
- hardware and runtime metadata;
- saved preprocessing state.

## Nested runs

Nested runs can represent hyperparameter trials under a parent experiment.

```python
with mlflow.start_run(run_name="search"):
    for learning_rate in learning_rates:
        with mlflow.start_run(nested=True):
            mlflow.log_param(
                "learning_rate",
                learning_rate,
            )
```

## Production guidance

Use stable metric names.
Log units explicitly.
Avoid logging secrets or raw private data.
Record failed and cancelled runs.
Keep large artifacts in appropriate object storage.
Make run identifiers visible in deployment metadata.
