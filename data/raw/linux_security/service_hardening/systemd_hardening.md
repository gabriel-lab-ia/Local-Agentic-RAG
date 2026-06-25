---
source_id: linux_security_systemd
title: "Systemd Service Hardening"
domain: linux_security
topic: systemd_hardening
url: "https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html"
license: reference-only
language: en
source_type: official_documentation_summary
---

# Systemd Service Hardening

## Definition

Systemd can constrain service privileges, namespaces, filesystems, devices, address families, capabilities, and system calls.

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

- Services inherit broad host access by default.
- Writable paths and network families are unrestricted.
- Hardening options are copied without workload testing.
- Operational fixes disable multiple protections.

## Engineering controls

- Use NoNewPrivileges, PrivateTmp, ProtectSystem, ProtectHome, and capability bounding.
- Restrict writable paths, devices, namespaces, address families, and syscalls.
- Keep service credentials and runtime directories scoped.
- Apply controls incrementally with representative tests.

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

- Run systemd-analyze security as a review aid.
- Inspect the effective unit configuration.
- Exercise startup, reload, shutdown, and failure paths.
- Alert on drift from approved unit files.

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
