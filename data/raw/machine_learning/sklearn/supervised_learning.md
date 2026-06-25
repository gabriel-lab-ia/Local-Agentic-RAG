---
source_id: ml_supervised_learning
title: "Supervised Learning Engineering Foundations"
domain: machine_learning
topic: supervised_learning
url: "https://scikit-learn.org/stable/supervised_learning.html"
license: BSD-3-Clause
language: en
source_type: official_documentation_summary
---

# Supervised learning

Supervised learning estimates a relationship between input features and
known target values.

The two principal problem families are:

- classification, where the target represents a category;
- regression, where the target represents a numerical quantity.

## Training examples

A supervised dataset contains pairs:

```text
(x_i, y_i)
```

where `x_i` is an input feature vector and `y_i` is its observed target.

A model learns parameters that minimize an objective over training examples
while aiming to generalize to unseen data.

## Classification

Classification models estimate labels, scores, decision functions, or
probabilities.

Example:

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(
    class_weight="balanced",
    max_iter=1_000,
    random_state=42,
)

model.fit(X_train, y_train)
probabilities = model.predict_proba(X_validation)[:, 1]
```

The default decision threshold is not automatically the correct operational
threshold.

Threshold selection depends on:

- false-positive cost;
- false-negative cost;
- intervention capacity;
- class prevalence;
- calibration;
- regulatory or safety requirements.

## Regression

Regression predicts continuous targets.

```python
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train)
predictions = model.predict(X_validation)
```

Metrics must reflect the application.

Common regression metrics include:

- mean absolute error;
- mean squared error;
- root mean squared error;
- coefficient of determination;
- quantile or asymmetric losses.

## Generalization

Low training error does not imply good generalization.

Generalization depends on:

- representative data;
- correct splitting;
- model capacity;
- regularization;
- feature quality;
- label quality;
- distribution stability;
- hyperparameter selection.

## Baselines

Every experiment should include a simple baseline.

Examples:

- majority classifier;
- mean or median predictor;
- logistic regression;
- linear regression;
- simple decision tree;
- established business rule.

A complex model must justify its added operational cost.

## Class imbalance

Accuracy can be misleading when one class dominates.

Evaluate:

- precision;
- recall;
- F1 score;
- ROC AUC;
- precision-recall AUC;
- confusion matrix;
- cost-weighted outcomes;
- performance by relevant subgroup.

## Data quality

Model quality is bounded by data quality.

Investigate:

- duplicate examples;
- missing values;
- inconsistent units;
- label noise;
- temporal leakage;
- proxy variables;
- sampling bias;
- train-serving skew.

## Engineering guidance

Define the decision before selecting the model.
Preserve an untouched final test set.
Compare against a baseline.
Report uncertainty and subgroup behavior.
Choose metrics and thresholds from operational costs.
Record data, code, configuration, and model versions.
