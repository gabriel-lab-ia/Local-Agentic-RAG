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
