# RAG Pipeline

The RAG pipeline answers technical questions from a local ChromaDB collection built from governed Markdown documents.

## Corpus

Raw documents live under `data/raw/` and are organized by domain. The current ingestion report records 84 documents and 757 generated chunks across Python, PyTorch, Machine Learning, Deep Learning, MLOps, LLMOps, Reinforcement Learning, Cybersecurity, Linux Security, ML Security, and AI Security.

## Chunking

`src/rag/ingest_technical.py`:

- parses simple Markdown front matter;
- discovers supported domain folders;
- splits content by Markdown headings;
- chunks long sections with overlap;
- attaches metadata such as `source_id`, `title`, `domain`, `topic`, `url`, and `source_path`.

Default chunk parameters:

- chunk size: `1400`;
- overlap: `220`;
- embedding batch size: `16`.

## Embeddings and ChromaDB

Documents and queries are embedded with EmbeddingGemma through Ollama. Chunks are stored in a persistent ChromaDB collection:

```text
CHROMA_DIR=data/chroma
COLLECTION_NAME=ai_engineering_knowledge
```

`data/chroma/` is local runtime state and is ignored by Git.

## Routing

`infer_domain()` maps query terms to one domain when exactly one domain matches. If zero or multiple domains match, retrieval falls back to global search.

Domain routing is a transparent heuristic. It is fast and easy to audit, but it can misclassify ambiguous queries.

## Top-k, Overfetch, and Diversity

The retriever asks ChromaDB for more candidates than the final `top_k`:

- candidate multiplier: `3`;
- minimum candidates: `15`;
- maximum chunks per source: `2`.

Candidates are sorted by vector distance, deduplicated, and limited per source to reduce source collapse.

## Domain Fallback

If domain-filtered retrieval returns fewer chunks than requested, the retriever performs a global query and diversifies across the combined candidate set.

## Citations

Each retrieved chunk is formatted as `[Fonte N]` with title, section, domain, topic, source ID, URL, vector distance, and document text. Answers are instructed to cite only retrieved sources.

## Context Is Untrusted

Retrieved content can be stale, incomplete, malicious, or irrelevant. The system prompt tells Qwen not to obey commands inside retrieved documents and not to treat context as instructions.

## Limitations

- Vector distance is not probability, confidence, or factual correctness.
- Top-k retrieval can miss relevant material.
- Source diversity can exclude useful adjacent chunks from the same source.
- Keyword domain routing can fail on new terminology.
- Corpus coverage determines answer coverage.
- Local model output still requires review for high-stakes use.
