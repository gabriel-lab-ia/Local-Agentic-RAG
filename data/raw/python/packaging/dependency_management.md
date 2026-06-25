---
source_id: python_dependency_management_uv
title: "Reproducible Dependency Management with uv"
domain: python
topic: dependency_management
url: "https://docs.astral.sh/uv/concepts/projects/dependencies/"
license: Apache-2.0-MIT
language: en
source_type: official_documentation_summary
---

# Reproducible dependency management with uv

Dependency management converts declared requirements into a resolved,
reproducible environment.

## Declaration and lock state

Direct requirements belong in `pyproject.toml`.
The lockfile records the complete resolved graph for repeatable sync.

```bash
uv add fastapi
uv add --dev pytest ruff
uv remove fastapi
uv sync
uv run pytest
```

Use `uv run` to execute commands in the project environment without relying
on whichever virtual environment happens to be active in the shell.

## Dependency groups

Development-only tools such as test runners, linters, and type checkers
belong in dependency groups rather than runtime package metadata.

## Version constraints

Constraints express compatibility policy.

Too broad can admit incompatible releases.
Too narrow can block security and compatibility upgrades.
Exact pins belong primarily in application lock state.

## Reproducibility

CI and deployment should use the committed lockfile.
Changes to declared dependencies and lock state should be reviewed together.

## Private indexes and credentials

Do not commit index credentials.
Restrict trusted indexes.
Understand dependency-confusion risk.
Prefer explicit source configuration and least-privilege tokens.

## Upgrade policy

Upgrade on a regular cadence.
Review changelogs for critical dependencies.
Run tests, static checks, and representative inference or training checks.
Monitor security advisories and transitive changes.

## Engineering guidance

Use one project environment per repository.
Avoid activating a virtual environment from another project.
Commit `pyproject.toml` and `uv.lock`.
Keep caches and virtual environments out of Git.
Make dependency updates small and observable.
