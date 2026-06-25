# Tests and Evaluation

## Unit Tests

Command:

```bash
uv run pytest
```

Result from this workspace:

```text
9 passed in 0.74s
```

Coverage focus:

- recent query routes to web search
- private/internal document query routes to ChromaDB/local RAG
- mixed local plus current query routes to hybrid retrieval
- math query routes to Python/tool execution
- ambiguous unknown query asks for clarification
- unknown longer query uses web when policy allows it
- compatibility shim for the earlier `src.agent_router.route_query` API

## Evaluation Cases

Command:

```bash
uv run python -m src.rag.agent.evaluate
```

Result:

```text
local-only RAG: route=local sources=1 latency_ms=0
web-only: route=web sources=1 latency_ms=0
hybrid RAG + web: route=hybrid sources=2 latency_ms=0
python/tool: route=python sources=1 latency_ms=0
```

The structured artifact is written to `docs/evaluation_results.json`.

This benchmark uses deterministic local fixtures and `MockWebSearchTool`; it is
intended to validate routing, logging shape, source metadata, and citation
coverage without network access, Ollama, or ChromaDB availability. A live
quality benchmark can be added later by configuring a real web provider and
running against the populated local ChromaDB collection.
