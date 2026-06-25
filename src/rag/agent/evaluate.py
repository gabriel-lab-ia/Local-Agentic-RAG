from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.rag.agent.router import ResearchAgent, ResearchPolicy
from src.rag.agent.sources import Source
from src.rag.agent.tools import MockWebSearchTool


def deterministic_answer(question: str, sources: list[Source]) -> str:
    if not sources:
        return "Sem fontes recuperadas."
    citations = " ".join(f"[Fonte {index}]" for index in range(1, len(sources) + 1))
    return f"Resposta sintética para avaliação: {question} {citations}"


def run_evaluation(output_path: Path) -> list[dict[str, object]]:
    web = MockWebSearchTool(
        fixtures={
            "qwen": [
                Source(
                    title="Qwen release mock",
                    content="Dados simulados sobre uma versão recente do Qwen.",
                    kind="web",
                    url="https://example.test/qwen-release",
                    metadata={"provider": "mock"},
                )
            ],
            "pytorch": [
                Source(
                    title="PyTorch current mock",
                    content="Dados simulados sobre documentação recente do PyTorch.",
                    kind="web",
                    url="https://example.test/pytorch",
                    metadata={"provider": "mock"},
                )
            ],
        }
    )

    local_sources = [
        Source(
            title="Local PyTorch docs",
            content="Trecho local sobre torch.nn.Module e treinamento.",
            kind="local",
            metadata={"collection": "ai_engineering_knowledge"},
            score=0.2,
        )
    ]

    class StaticLocalRetriever:
        def search(self, query: str, top_k: int = 5) -> list[Source]:
            return local_sources[:top_k]

    cases = [
        {
            "name": "local-only RAG",
            "question": "Explique torch.nn.Module nos documentos internos de PyTorch",
        },
        {
            "name": "web-only",
            "question": "Qual é a versão mais recente do Qwen em 2026?",
        },
        {
            "name": "hybrid RAG + web",
            "question": "Compare os documentos internos de PyTorch com a versão atual da API",
        },
        {
            "name": "python/tool",
            "question": "Calcule 128 * 32 / 4",
        },
    ]

    agent = ResearchAgent(
        local_retriever=StaticLocalRetriever(),
        web_search=web,
        answer_generator=deterministic_answer,
        policy=ResearchPolicy(log_path=None),
    )

    rows: list[dict[str, object]] = []
    for case in cases:
        result = agent.answer(str(case["question"]))
        rows.append(
            {
                "case": case["name"],
                "route": result.route.kind,
                "source_count": len(result.sources),
                "latency_ms": result.latency_ms,
                "quality": result.quality,
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(rows, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Run routed agent evaluation cases")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/evaluation_results.json"),
    )
    args = parser.parse_args()
    rows = run_evaluation(args.output)
    for row in rows:
        print(
            f"{row['case']}: route={row['route']} "
            f"sources={row['source_count']} latency_ms={row['latency_ms']}"
        )


if __name__ == "__main__":
    main()
