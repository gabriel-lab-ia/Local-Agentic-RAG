# Security Policy

## Supported Versions

This repository is an early local-first research project. Security fixes target the current `main` branch and active feature branches.

## Reporting a Vulnerability

Do not open a public issue containing secrets, exploit details against a real system, private paths, logs, or sensitive data. Open a minimal report with a sanitized reproduction or contact the maintainer privately before disclosure.

## Scope

In scope:

- path traversal in workspace tools;
- unsafe tool-call parsing;
- accidental write or destructive behavior in Agentic Core tools;
- secrets or local artifacts committed to the repository;
- RAG prompt-injection or poisoning weaknesses with clear reproductions;
- CI behavior that downloads models, uses secrets, or requires GPU/Ollama.

Out of scope:

- compromise of the local developer machine;
- attacks requiring existing arbitrary code execution on the host;
- correctness disputes without a reproducible security impact;
- production multi-user hosting, which this project does not implement.

## Local-first Assumptions

The default system runs locally. ChromaDB, logs, model files, `.env`, and generated reports can contain sensitive local context and must not be committed.

## Known Limitations

- The routed Python helper is not a production sandbox.
- The Agentic Core is read-only and does not yet implement an autonomous loop.
- Prompt-level guardrails reduce but do not eliminate prompt-injection risk.
- Retrieval distance is not a trust score.

## Secret Handling

Never submit real secrets, tokens, credentials, private URLs, private local paths, raw logs, vector databases, checkpoints, model weights, or unreviewed generated reports.

Use `.env.example` for safe defaults only.

See [docs/threat-model.md](docs/threat-model.md) for the detailed model.
