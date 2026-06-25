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
