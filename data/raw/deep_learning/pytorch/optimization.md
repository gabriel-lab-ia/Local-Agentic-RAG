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
