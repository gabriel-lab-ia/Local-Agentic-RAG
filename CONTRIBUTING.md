# Contributing

Thanks for helping improve Local Agentic RAG.

## Development Setup

```bash
uv sync --dev
cp .env.example .env
```

Local models are required only for live RAG or Ollama experiments:

```bash
ollama pull qwen3:4b
ollama pull embeddinggemma
```

## Quality Checks

Run before opening a pull request:

```bash
make check
```

This formats, lints, tests, validates tracked files, and checks whitespace.

## Security Rules

Do not commit:

- `.env` or secrets;
- ChromaDB files;
- logs;
- model weights;
- checkpoints;
- generated local reports;
- private absolute paths;
- hardware-identifying logs.

## Documentation Rules

Be honest about implementation status. Do not describe planned components as complete. If a feature needs Ollama, ChromaDB, GPU access, or network access, say so explicitly.

## Pull Request Style

Keep changes focused. Prefer small PRs for docs, security, CI, RAG behavior, and agent tooling. Include tests when behavior changes.
