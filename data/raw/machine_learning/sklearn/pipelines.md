---
source_id: ml_pipelines
title: "Leakage-Safe Machine Learning Pipelines"
domain: machine_learning
topic: pipelines
url: "https://scikit-learn.org/stable/modules/compose.html"
license: BSD-3-Clause
language: en
source_type: official_documentation_summary
---

# Machine learning pipelines

A pipeline combines preprocessing and prediction into one estimator-like
object.

Pipelines help ensure that transformations are fitted only on the training
portion of each split.

## Basic pipeline

```python
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median"),
        ),
        (
            "scaler",
            StandardScaler(),
        ),
        (
            "classifier",
            LogisticRegression(max_iter=1_000),
        ),
    ]
)

pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
```

## Column-specific preprocessing

Different feature types require different transformations.

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numeric_columns,
        ),
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
            ),
            categorical_columns,
        ),
    ]
)
```

## Joint hyperparameter search

Pipeline parameters use step names.

```python
parameter_grid = {
    "preprocessor__numeric__imputer__strategy": [
        "mean",
        "median",
    ],
    "classifier__C": [0.01, 0.1, 1.0, 10.0],
}
```

This allows preprocessing choices to be evaluated inside cross-validation.

## Custom transformers

A transformer should implement the estimator contract consistently.

```python
from sklearn.base import BaseEstimator, TransformerMixin

class ClipValues(
    TransformerMixin,
    BaseEstimator,
):
    def __init__(
        self,
        minimum: float,
        maximum: float,
    ) -> None:
        self.minimum = minimum
        self.maximum = maximum

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.clip(
            self.minimum,
            self.maximum,
        )
```

Constructor arguments should be stored without hidden mutation so that
cloning and hyperparameter search behave correctly.

## Train-serving consistency

Deployment should preserve:

- feature order;
- preprocessing parameters;
- category mappings;
- missing-value policy;
- model version;
- schema expectations.

Persisting only the final classifier while recreating preprocessing
manually creates train-serving skew.

## Security and compatibility

Serialized Python model artifacts may execute code when loaded.

Load artifacts only from trusted sources.
Record library and Python versions.
Validate schemas before prediction.

## Engineering guidance

Put all learned preprocessing inside the pipeline.
Avoid preprocessing the full dataset before splitting.
Test pipeline serialization and reload.
Version data schemas and model artifacts.
Monitor rejected, missing, and unseen feature values.
