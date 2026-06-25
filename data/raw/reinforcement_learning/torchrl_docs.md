---
source_id: torchrl_docs
title: "TorchRL"
domain: reinforcement_learning
topic: torchrl
url: https://docs.pytorch.org/rl/stable/
license: BSD-3-Clause
language: en
source_type: official_documentation
---
# TorchRL

TorchRL is an open-source Reinforcement Learning (RL) library for PyTorch.

You can install TorchRL directly from PyPI (see more about installation

instructions in the dedicated section below):

```

$ pip install torchrl

```

TorchRL provides pytorch and python-first, low and high level abstractions for RL that are intended to be efficient, modular, documented and properly tested.

The code is aimed at supporting research in RL. Most of it is written in python in a highly modular way, such that researchers can easily swap components, transform them or write new ones with little effort.

This repo attempts to align with the existing pytorch ecosystem libraries in that it has a “dataset pillar” (environments) , transforms , models ,

data utilities (e.g. collectors and containers), etc.

TorchRL aims at having as few dependencies as possible (python standard library, numpy and pytorch).

Common environment libraries (e.g. OpenAI gym) are only optional.

On the low-level end, torchrl comes with a set of highly reusable functionals

for cost functions , returns and data processing.

TorchRL aims at a high modularity and good runtime performance.

To read more about TorchRL philosophy and capabilities beyond this API reference,

check the TorchRL paper .

# Installation

TorchRL releases are synced with PyTorch, so make sure you always enjoy the latest

features of the library with the most recent version of PyTorch (although core features

are guaranteed to be backward compatible with pytorch>=2.0).

Nightly releases can be installed via

```

$ pip install tensordict-nightly

$ pip install torchrl-nightly

```

or via a git clone if you’re willing to contribute to the library:

`git clone`

```

$ cd path/to/root

$ git clone https://github.com/pytorch/tensordict

$ git clone https://github.com/pytorch/rl

$ cd tensordict

$ python setup.py develop

$ cd ../rl

$ python setup.py develop

```

If you use uv and you installed a specific PyTorch build beforehand (e.g. a nightly wheel),

use --no-deps for the editable installs to prevent dependency re-resolution (and potential PyTorch downgrades):

`uv`

`--no-deps`

```

$

cd

path/to/root

$

git

clone

https://github.com/pytorch/tensordict

$

git

clone

https://github.com/pytorch/rl

$

cd

tensordict

$

uv

pip

install

--no-deps

-e

.

$

cd

../rl

$

uv

pip

install

--no-deps

-e

.

```

# Getting started

A series of quick tutorials to get ramped up with the basic features of the

library. If you’re in a hurry, you can start by the last item of the series and navigate to the previous ones whenever you want to learn more!

- Get started with Environments, TED and transforms

- Get started with TorchRL’s modules

- Getting started with model optimization

- Get started with data collection and storage

- Get started with logging

- Get started with your own first training loop

# Tutorials

## Basics

- Reinforcement Learning (PPO) with TorchRL Tutorial

- Pendulum: Writing your environment and transforms with TorchRL

- Introduction to TorchRL

## Intermediate

- Multi-Agent Reinforcement Learning (PPO) with TorchRL Tutorial

- TorchRL envs

- Using pretrained models

- Recurrent DQN: Training recurrent policies

- MuJoCo scripted manipulation with human-readable robot actions

- Collectors Deep Dive: Trajectory Assembly

- Using the Evaluator

- Using Replay Buffers

- Memory-Efficient RL Training

- Exporting TorchRL modules

## Advanced

- Competitive Multi-Agent Reinforcement Learning (DDPG) with TorchRL Tutorial

- Task-specific policy in multi-task environments

- TorchRL objectives: Coding a DDPG loss

- TorchRL trainer: A DQN example

# References

- API Reference torchrl.collectors package MultiCollector API Key Features Collection hooks Quick Example Removed legacy names Documentation Sections torchrl.data package Key Features Quick Example CUDA prioritized replay buffers Documentation Sections Data layout: contiguous trajectories Trajectory boundary keys The replay buffer ndim arg and why it doesn’t multi-process well The buffer-to-collector handoff: complete-trajectory writes SliceSampler: variable-length contiguous slices Auto-discoverability for recurrent policies Legacy: split_trajectories Narrow canonicalization for recurrent inputs See also torchrl.envs package Key Features Quick Example Documentation Sections LLM Interface Key Components Quick Example Documentation Sections Environments Objectives torchrl.modules package Key Features Quick Example Documentation Sections torchrl.objectives package Key Features Quick Example Documentation Sections Service Registry Overview Basic Usage Python Executor Service Advanced Usage API Reference Best Practices Examples See Also torchrl.trainers package Key Features Quick Example Documentation Sections torchrl._utils package implement_for set_auto_unwrap_transformed_env auto_unwrap_transformed_env Memory profiling TorchRL Configuration System Quick Start with a Simple Example Configuration Categories and Groups More Complex Example: Parallel Environment with Transforms Getting Available Options Complete Training Example Running Experiments Configuration Store Implementation Details Available Configuration Classes Creating Custom Configurations Best Practices Supported Algorithms Profiling collectors and envs Enabling profiling Driving a torch.profiler trace from the driver What gets instrumented Capturing a trace Multi-process and Ray Performance impact Glossary See also

- torchrl.collectors package MultiCollector API Key Features Collection hooks Quick Example Removed legacy names Documentation Sections

- MultiCollector API

- Key Features

- Collection hooks

- Quick Example

- Removed legacy names

- Documentation Sections

- torchrl.data package Key Features Quick Example CUDA prioritized replay buffers Documentation Sections

- CUDA prioritized replay buffers

- Data layout: contiguous trajectories Trajectory boundary keys The replay buffer ndim arg and why it doesn’t multi-process well The buffer-to-collector handoff: complete-trajectory writes SliceSampler: variable-length contiguous slices Auto-discoverability for recurrent policies Legacy: split_trajectories Narrow canonicalization for recurrent inputs See also

- Trajectory boundary keys

- The replay buffer ndim arg and why it doesn’t multi-process well

`ndim`

- The buffer-to-collector handoff: complete-trajectory writes

- SliceSampler: variable-length contiguous slices

- Auto-discoverability for recurrent policies

- Legacy: split_trajectories

`split_trajectories`

- Narrow canonicalization for recurrent inputs

- See also

- torchrl.envs package Key Features Quick Example Documentation Sections

- LLM Interface Key Components Quick Example Documentation Sections Environments Objectives

- Key Components

- Environments

- Objectives

- torchrl.modules package Key Features Quick Example Documentation Sections

- torchrl.objectives package Key Features Quick Example Documentation Sections

- Service Registry Overview Basic Usage Python Executor Service Advanced Usage API Reference Best Practices Examples See Also

- Overview

- Basic Usage

- Python Executor Service

- Advanced Usage

- API Reference

- Best Practices

- Examples

- torchrl.trainers package Key Features Quick Example Documentation Sections

- torchrl._utils package implement_for set_auto_unwrap_transformed_env auto_unwrap_transformed_env Memory profiling

- implement_for

- set_auto_unwrap_transformed_env

- auto_unwrap_transformed_env

- Memory profiling

- TorchRL Configuration System Quick Start with a Simple Example Configuration Categories and Groups More Complex Example: Parallel Environment with Transforms Getting Available Options Complete Training Example Running Experiments Configuration Store Implementation Details Available Configuration Classes Creating Custom Configurations Best Practices Supported Algorithms

- Quick Start with a Simple Example

- Configuration Categories and Groups

- More Complex Example: Parallel Environment with Transforms

- Getting Available Options

- Complete Training Example

- Running Experiments

- Configuration Store Implementation Details

- Available Configuration Classes

- Creating Custom Configurations

- Supported Algorithms

- Profiling collectors and envs Enabling profiling Driving a torch.profiler trace from the driver What gets instrumented Capturing a trace Multi-process and Ray Performance impact

- Enabling profiling

- Driving a torch.profiler trace from the driver

- What gets instrumented

- Capturing a trace

- Multi-process and Ray

- Performance impact

- Glossary See also

# Knowledge Base

- Knowledge Base Contributing Things to consider when debugging RL Installing dm_control Flaky Test Resolution Guide Working with gym Working with habitat-lab IsaacLab Guide Working with MuJoCo-based environments Common PyTorch errors and solutions Useful resources Versioning Issues Customising Video Renders

- Contributing

- Things to consider when debugging RL

- Installing dm_control

- Flaky Test Resolution Guide

- Working with gym

- Working with habitat-lab

`habitat-lab`

- IsaacLab Guide

- Working with MuJoCo-based environments

- Common PyTorch errors and solutions

- Useful resources

- Versioning Issues

- Customising Video Renders

# Indices and tables

- Index

- Module Index

- Search Page

- ExecuTorch

- Helion

- torchao

- kineto

- torchtitan

- torchvision

- torchaudio

- tensordict

- PyTorch on XLA Devices
