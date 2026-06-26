from pathlib import Path
from textwrap import dedent


DOCUMENTS = {
    "data/raw/machine_learning/sklearn/supervised_learning.md": dedent(
        """
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
        """
    ).strip()
    + "\n",
    "data/raw/machine_learning/sklearn/model_selection.md": dedent(
        """
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
        """
    ).strip()
    + "\n",
    "data/raw/machine_learning/sklearn/cross_validation.md": dedent(
        """
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
        """
    ).strip()
    + "\n",
    "data/raw/machine_learning/sklearn/pipelines.md": dedent(
        """
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
        """
    ).strip()
    + "\n",
    "data/raw/deep_learning/pytorch/autograd.md": dedent(
        """
        ---
        source_id: deep_learning_autograd
        title: "Automatic Differentiation with PyTorch"
        domain: deep_learning
        topic: autograd
        url: "https://docs.pytorch.org/docs/stable/notes/autograd.html"
        license: BSD-3-Clause
        language: en
        source_type: official_documentation_summary
        ---

        # Automatic differentiation

        Automatic differentiation computes derivatives by applying the chain rule
        to operations recorded during program execution.

        PyTorch autograd records a dynamic computation graph for tensor operations
        that participate in gradient tracking.

        ## Gradient tracking

        ```python
        import torch

        weight = torch.tensor(
            2.0,
            requires_grad=True,
        )

        prediction = weight * 3.0
        loss = (prediction - 10.0) ** 2
        loss.backward()

        print(weight.grad)
        ```

        `backward()` propagates derivatives from the output toward leaf tensors.

        ## Computational graph

        Nodes represent operations and tensors.
        Edges represent data dependencies.

        For scalar loss `L` and parameters `theta`, training requires:

        ```text
        dL / dtheta
        ```

        Reverse-mode automatic differentiation is efficient when there are many
        parameters and a scalar or low-dimensional output.

        ## Gradient accumulation

        Gradients accumulate into `.grad` by default.

        A typical optimization step is:

        ```python
        optimizer.zero_grad(set_to_none=True)
        prediction = model(inputs)
        loss = loss_function(prediction, targets)
        loss.backward()
        optimizer.step()
        ```

        Failing to clear gradients unintentionally combines gradients across steps.

        ## Disabling gradients

        Inference normally does not require gradient recording.

        ```python
        model.eval()

        with torch.inference_mode():
            predictions = model(inputs)
        ```

        Disabling gradient tracking reduces graph construction and memory use.

        `model.eval()` changes behavior of modules such as dropout and batch
        normalization, but it does not independently disable autograd.

        ## Detaching

        `tensor.detach()` returns a tensor separated from the current gradient
        history.

        Detaching at the wrong location breaks gradient flow.

        Converting tensors to NumPy or scalars inside a differentiable computation
        can also destroy the intended graph.

        ## In-place operations

        In-place modifications can invalidate values needed during backward.

        Prefer out-of-place operations unless memory requirements and autograd
        behavior are understood.

        ## Higher-order derivatives

        Autograd can construct graphs for gradient computations when higher-order
        derivatives are needed.

        This is relevant to:

        - physics-informed neural networks;
        - meta-learning;
        - gradient penalties;
        - Jacobians;
        - Hessian-vector products.

        Higher-order derivatives increase memory and computational cost.

        ## Debugging gradients

        Inspect:

        - missing gradients;
        - NaN or infinite values;
        - unexpectedly detached tensors;
        - exploding or vanishing norms;
        - incorrect reductions;
        - incorrect device or dtype transitions.

        ## Engineering guidance

        Treat gradient flow as part of the model contract.
        Clear gradients intentionally.
        Separate training and inference modes.
        Avoid unnecessary graph retention.
        Validate gradients on small deterministic examples.
        """
    ).strip()
    + "\n",
    "data/raw/deep_learning/pytorch/neural_networks.md": dedent(
        """
        ---
        source_id: deep_learning_neural_networks
        title: "Neural Network Engineering with PyTorch"
        domain: deep_learning
        topic: neural_networks
        url: "https://docs.pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html"
        license: BSD-3-Clause
        language: en
        source_type: official_documentation_summary
        ---

        # Neural networks

        A neural network composes parameterized transformations and nonlinear
        functions.

        A feedforward layer can be written as:

        ```text
        z_l = a_(l-1) W_l + b_l
        a_l = phi(z_l)
        ```

        where:

        - `W_l` contains weights;
        - `b_l` contains biases;
        - `phi` is an activation function;
        - `l` identifies the layer.

        ## Module definition

        ```python
        import torch
        from torch import nn

        class Classifier(nn.Module):
            def __init__(
                self,
                input_features: int,
                hidden_features: int,
            ) -> None:
                super().__init__()

                self.network = nn.Sequential(
                    nn.Linear(
                        input_features,
                        hidden_features,
                    ),
                    nn.ReLU(),
                    nn.Linear(
                        hidden_features,
                        1,
                    ),
                )

            def forward(
                self,
                inputs: torch.Tensor,
            ) -> torch.Tensor:
                return self.network(inputs)
        ```

        Submodules assigned as attributes are registered automatically.

        ## Tensor shapes

        Shape errors are among the most common deep-learning failures.

        Document dimensions explicitly.

        Example:

        ```text
        input:  [batch, features]
        hidden: [batch, hidden_features]
        logits: [batch, classes]
        ```

        The final layer shape must match the learning objective.

        ## Logits and probabilities

        Classification models often return logits.

        Loss functions may combine numerically stable activation and likelihood
        calculations internally.

        For binary classification:

        ```python
        loss_function = nn.BCEWithLogitsLoss()
        ```

        Apply sigmoid for interpreted probabilities after obtaining logits.

        For multiclass classification:

        ```python
        loss_function = nn.CrossEntropyLoss()
        ```

        Do not apply softmax before this loss unless the API explicitly requires it.

        ## Training and evaluation modes

        ```python
        model.train()
        ```

        activates training behavior.

        ```python
        model.eval()
        ```

        activates evaluation behavior for modules such as dropout and batch
        normalization.

        ## Initialization

        Initialization affects signal propagation and optimization.

        PyTorch modules provide defaults, but specialized architectures may require
        explicit initialization.

        Initialization should be tested with:

        - activation distributions;
        - gradient norms;
        - training stability;
        - reproducibility.

        ## Capacity and regularization

        Capacity depends on architecture, parameter count, activation functions,
        receptive field, and connectivity.

        Regularization mechanisms include:

        - weight decay;
        - dropout;
        - data augmentation;
        - early stopping;
        - architectural constraints;
        - normalization;
        - more representative data.

        ## Engineering guidance

        Assert expected tensor shapes.
        Keep forward computation deterministic during evaluation.
        Separate logits from post-processing.
        Save architecture, configuration, and state together.
        Test small batches before full training.
        Track parameter counts and memory requirements.
        """
    ).strip()
    + "\n",
    "data/raw/deep_learning/pytorch/optimization.md": dedent(
        """
        ---
        source_id: deep_learning_optimization
        title: "Optimization and Training Stability"
        domain: deep_learning
        topic: optimization
        url: "https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html"
        license: BSD-3-Clause
        language: en
        source_type: official_documentation_summary
        ---

        # Optimization and training stability

        Optimization adjusts model parameters to reduce an objective computed from
        training data.

        A basic update has the form:

        ```text
        theta_(t+1) = theta_t - learning_rate * gradient
        ```

        Practical optimizers modify this rule using momentum, adaptive scaling,
        parameter groups, or other state.

        ## Training step

        ```python
        optimizer.zero_grad(set_to_none=True)

        logits = model(inputs)
        loss = loss_function(logits, targets)

        loss.backward()
        optimizer.step()
        ```

        The order is part of the training contract.

        ## Learning rate

        The learning rate strongly influences training.

        Too high may cause:

        - divergence;
        - unstable oscillation;
        - NaN values;
        - destructive updates.

        Too low may cause:

        - slow convergence;
        - wasted compute;
        - apparent training plateaus.

        ## Optimizers

        Common choices include:

        - stochastic gradient descent;
        - SGD with momentum;
        - Adam;
        - AdamW;
        - RMSprop.

        Optimizer choice does not remove the need for learning-rate tuning,
        validation, and stability monitoring.

        ## Weight decay

        Weight decay discourages large parameters.

        Its exact interaction with the optimizer matters. Decoupled weight decay,
        as used by AdamW, is not identical to adding an L2 penalty to every adaptive
        update.

        Biases and normalization parameters are sometimes excluded from weight
        decay through parameter groups.

        ## Gradient clipping

        Gradient clipping can bound extreme updates.

        ```python
        torch.nn.utils.clip_grad_norm_(
            model.parameters(),
            max_norm=1.0,
        )
        ```

        Clipping can stabilize training but may hide an underlying modeling,
        numerical, or data problem.

        ## Learning-rate schedules

        Schedules change the learning rate during training.

        Examples:

        - step decay;
        - cosine decay;
        - warmup;
        - plateau-based reduction;
        - one-cycle schedules.

        Scheduler steps must occur at the intended frequency.

        ## Mixed precision

        Mixed precision can improve accelerator throughput and reduce memory use.

        Numerical behavior must be monitored, especially for operations sensitive
        to reduced precision.

        ## Reproducibility

        Record:

        - random seeds;
        - dataset version;
        - batch order;
        - optimizer;
        - learning rate;
        - scheduler;
        - precision mode;
        - hardware;
        - library versions;
        - checkpoint state.

        Exact reproducibility may be limited by hardware and nondeterministic
        operations.

        ## Monitoring

        Track:

        - training and validation loss;
        - task metrics;
        - learning rate;
        - gradient norms;
        - parameter norms;
        - throughput;
        - memory use;
        - NaN and infinite values.

        ## Checkpoints

        A resumable checkpoint should include:

        - model state;
        - optimizer state;
        - scheduler state;
        - current epoch or step;
        - scaler state when applicable;
        - experiment configuration;
        - random state when required.

        ## Engineering guidance

        Begin with a simple optimizer and baseline.
        Tune the learning rate before adding complexity.
        Validate on representative data.
        Save resumable checkpoints.
        Diagnose instability rather than masking it.
        """
    ).strip()
    + "\n",
}


def main() -> None:
    for raw_path, content in DOCUMENTS.items():
        path = Path(raw_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Preenchido: {path}")

    print(f"\nDocumentos preenchidos: {len(DOCUMENTS)}")


if __name__ == "__main__":
    main()
