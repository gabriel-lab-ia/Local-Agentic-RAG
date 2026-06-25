---
source_id: ml_security_evasion
title: "Evasion Attacks and Adversarial Examples"
domain: ml_security
topic: evasion_attacks
url: "https://csrc.nist.gov/pubs/ai/100/2/e2025/final"
license: reference-only
language: en
source_type: official_documentation_summary
---

# Evasion Attacks and Adversarial Examples

## Definition

Evasion attacks manipulate inference-time inputs to cause incorrect or attacker-preferred model behavior without necessarily changing the model.

This document is defensive engineering guidance. It is intended for secure
design, hardening, governance, detection, evaluation, incident response, and
risk reduction. It does not authorize testing against systems without explicit
permission.

## Security objectives

A mature implementation should preserve confidentiality, integrity,
availability, authenticity, accountability, and recoverability while keeping
operational behavior observable and testable.

The control design should answer:

- what asset or decision is protected;
- which identity or component is trusted;
- where trust changes;
- which failure or abuse case is prevented;
- which signal detects control failure;
- how the system contains and recovers from failure.

## Common risks

- Robustness is inferred from normal validation accuracy.
- Preprocessing behavior creates exploitable discontinuities.
- Detection thresholds are tuned on known attacks only.
- Operational constraints differ from laboratory evaluations.

## Engineering controls

- Define allowable perturbations and realistic attacker control.
- Evaluate transformations, preprocessing, and end-to-end pipelines.
- Use layered validation, anomaly signals, and safe fallback behavior.
- Avoid claiming universal robustness from a single defense.

## Architecture guidance

Keep policy enforcement outside probabilistic components whenever a
deterministic decision is required. Treat network input, files, model output,
retrieved text, serialized artifacts, tool results, and external metadata as
untrusted until validated.

Use narrow interfaces and explicit trust boundaries. Separate ingestion,
review, publication, execution, administration, and incident-response
permissions. Prefer immutable versions, reproducible builds, bounded resource
usage, safe defaults, and fail-closed behavior for sensitive operations.

Security controls should remain effective during timeout, retry, cancellation,
partial failure, degraded dependencies, rollback, and recovery. A control that
works only on the happy path is incomplete.

## Verification

- Report attack success under explicit threat models.
- Test adaptive attacks and pipeline-level effects.
- Measure false positives and operational cost.
- Monitor distribution shifts and unusual input patterns.

## Operational telemetry

Record bounded and redacted evidence for:

- authenticated user and workload identity;
- action, resource, and authorization result;
- source, artifact, model, dataset, or policy version;
- validation failures and denied operations;
- latency, timeout, retry, queue, rate, and resource state;
- control changes, deployment events, and administrative access.

Do not place secrets, raw credentials, unrestricted prompts, sensitive
documents, or private model inputs in logs. Protect audit data as a
security-sensitive asset.

## Incident readiness

Define ownership, severity, escalation, containment, evidence preservation,
credential rotation, rollback, recovery validation, and lessons-learned
procedures. Preserve enough provenance to identify which data, model, source,
policy, identity, and deployment version contributed to an incident.

## Engineering checklist

- Threat model and trust boundaries are documented.
- Least privilege is enforced for users, services, pipelines, and tools.
- Inputs and outputs are validated at system boundaries.
- Versions and provenance are immutable and reviewable.
- Abuse cases and negative authorization paths are tested.
- Telemetry supports detection and investigation without leaking secrets.
- Rollback, revocation, quarantine, and recovery are tested.
- Residual risks and limitations are stated explicitly.
