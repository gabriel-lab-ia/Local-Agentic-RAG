---
source_id: ml_model_selection
title: "Model Selection and Hyperparameter Engineering"
domain: machine_learning
topic: model_selection
url: "https://scikit-learn.org/stable/model_selection.html"
license: BSD-3-Clause
language: en
source_type: official_documentation_summary
---

# Model selection

Model selection compares candidate algorithms, representations, and
hyperparameters using data that is separate from final evaluation.

## Parameters and hyperparameters

Parameters are learned from data.

Examples:

- linear coefficients;
- tree split values;
- neural network weights.

Hyperparameters configure the learning process.

Examples:

- regularization strength;
- tree depth;
- number of estimators;
- learning rate;
- batch size;
- architecture width.

## Data roles

A robust workflow distinguishes:

- training data for parameter estimation;
- validation data or cross-validation for model selection;
- test data for final unbiased evaluation.

Repeatedly evaluating on the test set turns it into validation data.

## Search spaces

A search space should reflect meaningful engineering hypotheses.

```python
parameter_grid = {
    "classifier__max_depth": [4, 8, 16, None],
    "classifier__min_samples_leaf": [1, 5, 20],
    "classifier__class_weight": [None, "balanced"],
}
```

Avoid enormous search spaces without sufficient compute or statistical
justification.

## Grid and randomized search

Grid search evaluates combinations from a fixed Cartesian product.

Randomized search samples from distributions or candidate lists and can
explore larger spaces under a fixed budget.

```python
from sklearn.model_selection import RandomizedSearchCV

search = RandomizedSearchCV(
    estimator=pipeline,
    param_distributions=parameter_distributions,
    n_iter=40,
    scoring="average_precision",
    cv=5,
    n_jobs=-1,
    random_state=42,
)

search.fit(X_train, y_train)
```

## Multiple metrics

A single score may hide operational trade-offs.

Track several metrics while choosing one explicit refit objective.

```python
scoring = {
    "precision": "precision",
    "recall": "recall",
    "pr_auc": "average_precision",
    "roc_auc": "roc_auc",
}
```

## Complexity and stability

Prefer a simpler model when performance is effectively equivalent and the
simpler model improves:

- latency;
- interpretability;
- reliability;
- calibration;
- deployment size;
- retraining cost;
- debugging.

## Selection bias

Trying many configurations increases the chance of selecting a model that
benefited from validation noise.

Mitigations include:

- nested cross-validation;
- a separate final test set;
- restricted search spaces;
- repeated validation;
- confidence intervals;
- confirmation on future data.

## Engineering guidance

Search preprocessing and model hyperparameters together.
Keep the test set untouched.
Record every experiment.
Compare runtime and memory as well as predictive metrics.
Prefer reproducible, bounded searches.
Re-evaluate selected models under realistic serving conditions.
