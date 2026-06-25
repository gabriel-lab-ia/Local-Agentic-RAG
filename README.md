## private-qwen-training

Local-first experiments for Qwen/Ollama fine-tuning and retrieval-augmented
question answering with ChromaDB.

### Routed research agent

The project now includes a routed research agent that decides which tool path to
use before answering:

- `local`: ChromaDB/RAG for internal technical or academic knowledge.
- `web`: a pluggable web-search interface for recent, external, uncertain, or
  time-sensitive questions.
- `hybrid`: local ChromaDB plus web search when a question mixes private/local
  context with current external facts.
- `python`: local Python execution for calculations or code validation.
- `clarify`: asks for clarification when the query is too ambiguous for a
  privacy-aware source choice.

The implementation keeps Ollama/Qwen as the answer generator and ChromaDB as
the local vector store. Web search is abstracted through a `WebSearchTool`
protocol; tests use `MockWebSearchTool`, and Tavily, Serper, or Firecrawl can be
added later without changing the router.

Run the routed agent:

```bash
uv run python -m src.rag.agent.router "Explique torchrl nos documentos internos"
```

Run tests:

```bash
uv run pytest
```

Run the deterministic evaluation harness:

```bash
uv run python -m src.rag.agent.evaluate
```

### Privacy posture

The default policy is local-first. Local technical terms route to ChromaDB, and
ambiguous short queries ask for clarification instead of automatically sending
content to a web provider. The included web tool is a mock, so no external web
requests are made unless a real provider adapter is explicitly configured.

Tool decisions are logged as JSONL to `logs/research_agent.jsonl` by default:
route, tool decisions, retrieved source metadata, latency, and simple answer
quality metrics such as citation coverage.

### Existing RAG flows

The existing local RAG entrypoints remain available:

```bash
uv run python -m src.rag.chat
uv run python -m src.rag.chat_technical
```

The routed agent is additive and reuses the technical ChromaDB retriever rather
than replacing existing behavior.
