# Roadmap

## Phase 0: Local RAG

Implemented. Local Qwen/Ollama generation, EmbeddingGemma embeddings, persistent ChromaDB, governed corpus, citations, domain routing, overfetch, diversity, and fallback.

## Phase 1: Strict Tool Routing

Implemented. Qwen produces JSON-only tool decisions, parsed by a strict schema with controlled validation errors.

## Phase 2: Read-only Tool Execution

Implemented. Workspace-confined `list_directory`, `read_file`, `search_code`, and fixed `git_status`.

## Phase 3: Observation-action Loop

Planned. Add multi-step read-only reasoning with explicit budgets, observations, and stop conditions.

## Phase 4: Safe Patches

Planned. Add patch proposal only, with diff preview, path policy, user approval, and rollback strategy.

## Phase 5: Test and Lint Execution

Planned. Add fixed allowlisted commands such as Ruff and pytest with timeouts, captured output, and no arbitrary shell.

## Phase 6: Git-aware Coding Agent

Planned. Use Git state for checkpoints and review while avoiding automatic push, history rewrites, and destructive commands.

## Phase 7: Episodic Memory

Planned. Introduce auditable memory with poisoning controls, scope separation, deletion, and source provenance.

## Phase 8: Evaluation Harness

Partially implemented. Expand deterministic tests into benchmark suites for routing, retrieval, JSON validity, citation correctness, and task completion.

## Phase 9: Sandboxed Autonomous Workflows

Planned. Add isolated execution, resource limits, approval gates, and policy-based autonomy for narrow workflows.
