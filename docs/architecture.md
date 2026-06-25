# Architecture

## Components

- `src/rag/chat.py`: existing university-books RAG chat.
- `src/rag/chat_technical.py`: existing technical ChromaDB RAG chat over AI
  engineering, PyTorch, and reinforcement-learning sources.
- `src/rag/agent/router.py`: policy-driven research agent that routes a query
  to local RAG, web search, hybrid retrieval, Python execution, or clarification.
- `src/rag/agent/policy.py`: source-selection heuristics and privacy defaults.
- `src/rag/agent/tools.py`: tool protocols and implementations for ChromaDB,
  mock web search, and local Python execution.
- `src/rag/agent/sources.py`: normalized source metadata and cited context
  formatting.
- `src/rag/agent/evaluate.py`: deterministic evaluation cases comparing
  local-only, web-only, hybrid, and Python/tool paths.

## Routing Policy

The router classifies queries with transparent heuristics:

- Technical, academic, project, ChromaDB, RAG, PyTorch, TorchRL, Gymnasium,
  algorithms, ethics, or Pressman-style terms prefer local ChromaDB.
- Recent/current/time-sensitive terms prefer web search.
- Queries with both local and recent/external signals use hybrid retrieval.
- Math, calculation, Python, execution, or code-validation signals use the
  Python tool path.
- Short unknown queries ask for clarification by default.
- Longer unknown queries may use web search if `allow_web_for_unknown` remains
  enabled.

This keeps private/internal queries local unless the query itself asks for
recent or external information.

## Tool Interfaces

The agent depends on protocols rather than concrete providers:

- `LocalRetriever.search(query, top_k) -> list[Source]`
- `WebSearchTool.search(query, max_results) -> list[Source]`
- `PythonTool.run(query) -> Source`

`MockWebSearchTool` is provided for tests and offline evaluation. A future
Tavily, Serper, or Firecrawl adapter only needs to implement the same
`WebSearchTool` protocol and return normalized `Source` objects with title,
content, URL, score, and provider metadata.

## Answer Generation

`ResearchAgent` defaults to `qwen_answer_generator`, which calls Ollama with the
existing Qwen model and the technical RAG system prompt. Tests and evaluations
inject a deterministic answer generator so they do not require Ollama.

All retrieved material is formatted with numbered citations (`[Fonte 1]`,
`[Fonte 2]`) and source metadata before answer generation.

## Logging

Each answered query can append a JSONL record to `logs/research_agent.jsonl`.
Records include:

- user question
- route and route reasons
- tool decisions
- source metadata and source kinds
- per-tool and total latency
- answer quality metrics: source count, answer length, citation coverage, and
  whether an answer was produced

Logging can be disabled by setting `ResearchPolicy(log_path=None)` or passing
`--no-log` to the router CLI.
