---
source_id: ai_security_model_dos
title: "Model Denial of Service and Resource Exhaustion"
domain: ai_security
topic: model_denial_of_service
url: "https://genai.owasp.org/"
license: reference-only
language: en
source_type: official_documentation_summary
---

# Model Denial of Service and Resource Exhaustion

## Definition

AI denial of service targets token budgets, context windows, retrieval, tools, concurrency, accelerators, memory, storage, or downstream costs.

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

- Requests have no token, time, recursion, or tool-call limits.
- Large documents trigger unbounded ingestion or retrieval work.
- Retries amplify overload.
- A single tenant consumes shared model capacity.

## Engineering controls

- Enforce input, output, context, retrieval, tool, time, and cost budgets.
- Apply rate, concurrency, queue, and tenant limits.
- Use deadlines, cancellation, backpressure, and bounded retries.
- Degrade safely and protect critical capacity.

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

- Load-test worst-case request shapes.
- Exercise cancellation and dependency failure.
- Monitor queue depth, accelerator utilization, token use, latency, and cost.
- Verify tenant isolation and overload behavior.

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
