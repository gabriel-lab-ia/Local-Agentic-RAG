# Evaluation

The current test suite validates deterministic behavior that does not require Ollama, ChromaDB, GPU access, or network calls.

## Existing Tests

Run:

```bash
uv run pytest
```

Coverage includes:

- strict JSON tool-call parsing;
- rejection of invalid tools and malformed arguments;
- final-answer schema validation;
- Qwen/Ollama adapter behavior with mocked HTTP responses;
- workspace path traversal rejection;
- read-only filesystem tool behavior;
- ignored local vector-store search paths;
- ToolRegistry execution and controlled errors;
- local, web, hybrid, Python, and clarification route decisions.

## Deterministic Routing Evaluation

Run:

```bash
uv run python -m src.rag.agent.evaluate
```

The evaluation uses fixture retrievers and mock web search. It is meant to validate routing shape, source metadata, and citation coverage, not live answer quality.

## Proposed Benchmark Metrics

| Metric | Definition |
| --- | --- |
| Tool selection accuracy | Percentage of prompts routed to the expected tool path. |
| JSON validity rate | Percentage of model tool responses accepted by `parse_tool_call()`. |
| Domain routing accuracy | Percentage of technical questions assigned to the expected corpus domain. |
| Citation correctness | Percentage of claims supported by cited retrieved chunks. |
| Retrieval coverage | Percentage of benchmark questions with at least one relevant chunk in top-k. |
| Path traversal rejection | Percentage of malicious path attempts rejected. |
| Tool execution failure rate | Percentage of validated tool calls that fail during execution. |
| Latency | End-to-end and per-tool milliseconds. |
| VRAM usage | Local model memory footprint during RAG and routing runs. |
| Task completion rate | Percentage of agent tasks completed within tool and step limits. |

## Reporting Rules

- Do not publish unmeasured metrics as results.
- Separate deterministic tests from live local-model evaluations.
- Record model names, corpus version, collection name, and retrieval settings.
- Treat generated logs as local artifacts unless reviewed for sensitive content.
