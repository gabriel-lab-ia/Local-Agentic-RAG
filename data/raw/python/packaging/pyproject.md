---
source_id: python_pyproject
title: "Modern pyproject.toml Design"
domain: python
topic: packaging
url: "https://packaging.python.org/en/latest/guides/writing-pyproject-toml/"
license: MIT
language: en
source_type: official_documentation_summary
---

# Modern pyproject.toml design

`pyproject.toml` centralizes project metadata, build configuration, and tool
configuration.

## Main tables

`[build-system]` declares the build backend and build requirements.

`[project]` contains standardized project metadata such as name, version,
Python requirement, dependencies, entry points, and classifiers.

`[tool.*]` contains tool-specific configuration.

```toml
[project]
name = "private-qwen-training"
version = "0.1.0"
requires-python = ">=3.11,<3.12"
dependencies = [
  "chromadb",
  "requests",
]

[dependency-groups]
dev = [
  "pytest",
  "ruff",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## Source layout

A `src/` layout reduces accidental imports from the repository root and
better resembles an installed package.

## Entry points

Command-line entry points provide stable executable interfaces instead of
requiring users to know module paths.

## Tool configuration

Keep configuration near the project when the tool supports it. Avoid
contradictory settings spread across multiple files.

## Version policy

Declare supported Python versions explicitly. Test them in CI. Do not claim
support that is not exercised.

## Engineering guidance

Keep runtime and development dependencies distinct.
Avoid unnecessary upper bounds without evidence.
Pin applications through a lockfile, not by overconstraining library
metadata.
Keep metadata reproducible and reviewable.
Validate builds in CI.
