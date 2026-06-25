---
source_id: python_secure_services
title: "Secure Engineering for Python AI Services"
domain: python
topic: security
url: "https://docs.python.org/3.11/library/security_warnings.html"
license: PSF-2.0
language: en
source_type: security_engineering_synthesis
---

# Secure Python services

Security must be enforced at trust boundaries, dependency boundaries,
deployment boundaries, and model-tool boundaries.

## Input validation

Validate type, size, encoding, shape, range, and allowed values before
expensive processing.

Set limits for:

- request bodies;
- uploaded files;
- batch size;
- sequence length;
- archive expansion;
- recursion and nesting;
- execution duration;
- generated output.

## Secrets

Load secrets from an approved secret-management mechanism.
Never commit secrets or print them in logs.
Rotate credentials and apply least privilege.

## Dangerous features

Do not use `eval` or `exec` on untrusted input.
Do not unpickle untrusted data.
Treat YAML loaders, template engines, subprocesses, and dynamic imports as
security boundaries.

## Subprocess execution

Prefer argument lists over shell strings.

```python
import subprocess

subprocess.run(
    ["python", "-m", "module_name"],
    check=True,
    timeout=30,
)
```

Avoid `shell=True` with untrusted data.

## File safety

Normalize and constrain paths.
Prevent path traversal.
Store uploads outside executable source directories.
Use generated file names and explicit allowlists.

## AI-specific boundaries

Retrieved text and model output are untrusted data.
Tool calls require schemas, authorization, allowlists, budgets, and audit
events.
Prompt instructions must not override system authorization.
Generated code must not execute automatically in a privileged environment.

## Supply chain

Lock dependencies.
Review updates.
Use trusted indexes.
Scan dependencies and containers.
Minimize runtime images and permissions.

## Engineering guidance

Apply defense in depth.
Fail closed for authorization.
Separate authentication from authorization.
Protect logs and traces as sensitive operational data.
Test abuse cases, not only expected flows.
