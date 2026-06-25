---
source_id: ml_security_threat_modeling
title: "Threat Modeling for Machine Learning Systems"
domain: ml_security
topic: ml_threat_modeling
url: "https://atlas.mitre.org/"
license: reference-only
language: en
source_type: official_documentation_summary
---

# Threat Modeling for Machine Learning Systems

## Definition

ML threat modeling covers data collection, labeling, feature pipelines, training infrastructure, model artifacts, serving paths, feedback loops, and downstream decisions.

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

- Data writers and labelers are assumed trustworthy.
- Pretrained models and datasets are accepted without provenance.
- Query access and observable outputs are not considered.
- Feedback loops allow attacker influence over future training.

## Engineering controls

- Identify who can read or modify data, labels, features, models, embeddings, logits, and gradients.
- Map suppliers, pretrained artifacts, registries, and evaluation sets.
- Define query, rate, output, and feedback access.
- Link attack paths to business and safety impact.

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

- Review permissions across the entire ML pipeline.
- Test integrity checks on data and artifacts.
- Audit external components and provenance.
- Exercise poisoning and extraction response scenarios.

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
