# Threat Model

## Assets

- Local source code and repository history.
- User intent and private prompts.
- `.env` values and local secrets.
- ChromaDB collection contents.
- Local model files, checkpoints, and weights.
- Logs and generated reports.
- Git state and branch integrity.
- Trust in generated answers and citations.

## Actors

- Benign local developer.
- Malicious or compromised corpus document.
- Malicious user prompt.
- Unreliable or hallucinated model output.
- Future external search provider or remote content source.
- Accidental committer of local artifacts.

## Trust Boundaries

- User prompt to prompt builder.
- Retrieved document text to model context.
- Model output to JSON parser.
- Parsed tool call to ToolRegistry.
- Tool arguments to workspace path policy.
- Local runtime artifacts to Git tracking.

## Attack Surfaces

- Prompt injection and indirect prompt injection.
- Poisoned corpus chunks.
- Tool-call JSON fields.
- Path arguments to filesystem tools.
- Subprocess invocation.
- Logs containing sensitive content.
- Generated reports with local paths.
- Large binary artifacts accidentally tracked.

## Threats and Mitigations

| Threat | Mitigation |
| --- | --- |
| Direct prompt injection | System prompt requires grounding, citations, and insufficiency notices. |
| Indirect prompt injection | Retrieved context is treated as untrusted evidence, not instructions. |
| RAG poisoning | Governed corpus, citations, source IDs, diversity limits, and audit docs. |
| Path traversal | Resolved path must remain under workspace. |
| Unsafe tool call | Strict JSON parser and registry allow only implemented tools. |
| Excessive agency | No write tools, no autonomous loop, no hidden execution. |
| Secrets exposure | `.gitignore`, `.env.example`, validation script, and pre-commit checklist. |
| Large artifact exposure | Ignore model/vector/checkpoint paths and check tracked file sizes. |
| Subprocess abuse | Fixed Git command with list args and timeout. |

## Residual Risks

- Model responses may still be incomplete or incorrectly cite sources.
- Domain routing can miss relevant contexts or choose a narrow filter.
- Vector similarity can surface irrelevant or stale chunks.
- The Python helper in the routed research agent is not a hardened sandbox.
- Local logs can contain user questions and source metadata if enabled.
- Generated reports may need manual review before publication.

## Out of Scope

- Protecting against a fully compromised local machine.
- Guaranteeing correctness of all corpus content.
- Running untrusted code in production.
- Autonomous code modification.
- Multi-user access control.
- Remote hosted inference or SaaS deployment.
