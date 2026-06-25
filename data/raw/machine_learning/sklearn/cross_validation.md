---
source_id: ml_cross_validation
title: "Cross-Validation Without Leakage"
domain: machine_learning
topic: cross_validation
url: "https://scikit-learn.org/stable/modules/cross_validation.html"
license: BSD-3-Clause
language: en
source_type: official_documentation_summary
---

# Cross-validation

Cross-validation estimates how a model-selection procedure may perform on
unseen data by repeatedly training and evaluating on different splits.

## K-fold cross-validation

K-fold cross-validation divides the available training data into `k` folds.

For each iteration:

1. one fold is used for validation;
2. the remaining folds are used for training;
3. the metric is recorded;
4. results are aggregated across folds.

```python
from sklearn.model_selection import cross_validate

result = cross_validate(
    estimator=pipeline,
    X=X_train,
    y=y_train,
    cv=5,
    scoring={
        "f1": "f1",
        "roc_auc": "roc_auc",
    },
    return_train_score=True,
    n_jobs=-1,
)
```

## Stratified splitting

For classification, stratification attempts to preserve class proportions
across folds.

```python
from sklearn.model_selection import StratifiedKFold

splitter = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42,
)
```

Stratification does not solve all sampling or subgroup problems.

## Grouped data

Related examples must not appear in both training and validation folds.

Groups may represent:

- users;
- patients;
- machines;
- physical assets;
- documents from the same source;
- repeated measurements;
- geographic locations.

Use group-aware splitters when examples share information.

## Temporal data

Random splitting is often invalid when future observations would leak into
training.

Time-aware evaluation should train on the past and evaluate on later
periods.

Consider:

- concept drift;
- seasonality;
- delayed labels;
- changing prevalence;
- deployment retraining cadence.

## Preprocessing leakage

Preprocessing must be fitted inside each training fold.

Incorrect:

```python
scaler.fit(X_all)
X_scaled = scaler.transform(X_all)
cross_validate(model, X_scaled, y)
```

Correct:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pipeline = Pipeline(
    steps=[
        ("scaler", StandardScaler()),
        ("model", model),
    ]
)
```

## Nested cross-validation

Nested cross-validation separates hyperparameter selection from performance
estimation.

The inner loop selects hyperparameters.
The outer loop estimates the complete selection process.

## Reporting

Report:

- mean;
- standard deviation;
- fold-level scores;
- splitter type;
- random seed;
- group or time policy;
- preprocessing pipeline;
- sample counts.

## Engineering guidance

Match the splitter to the data-generating process.
Keep preprocessing inside the pipeline.
Preserve an untouched final test set.
Inspect variance, not only the mean.
Treat cross-validation as an estimate, not a guarantee.
