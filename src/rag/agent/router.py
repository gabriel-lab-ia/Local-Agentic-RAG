from __future__ import annotations

import argparse
import json
import logging
import time
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Callable, Protocol

import requests

from src.rag.agent.policy import SourceSelectionPolicy
from src.rag.agent.sources import Source, build_cited_context
from src.rag.agent.tools import (
    ChromaTechnicalRetriever,
    LocalRetriever,
    PythonTool,
    SafePythonTool,
    UnconfiguredWebSearchTool,
    WebSearchTool,
)
from src.rag.chat_technical import (
    CHAT_MODEL,
    OLLAMA_BASE_URL,
    REQUEST_TIMEOUT,
    build_system_prompt,
)


LOGGER = logging.getLogger(__name__)


class RouteKind(StrEnum):
    LOCAL = "local"
    WEB = "web"
    HYBRID = "hybrid"
    PYTHON = "python"
    CLARIFY = "clarify"


@dataclass(frozen=True)
class QueryRoute:
    kind: RouteKind
    reasons: list[str]
    use_local: bool = False
    use_web: bool = False
    use_python: bool = False
    needs_clarification: bool = False


@dataclass(frozen=True)
class ToolDecision:
    tool: str
    action: str
    reason: str
    latency_ms: int
    source_count: int


@dataclass(frozen=True)
class ResearchAnswer:
    question: str
    route: QueryRoute
    answer: str
    sources: list[Source]
    decisions: list[ToolDecision]
    latency_ms: int
    quality: dict[str, float | int | str] = field(default_factory=dict)

    def to_log_record(self) -> dict[str, object]:
        return {
            "question": self.question,
            "route": asdict(self.route),
            "decisions": [asdict(decision) for decision in self.decisions],
            "sources": [
                {
                    "title": source.title,
                    "kind": source.kind,
                    "url": source.url,
                    "score": source.score,
                    "metadata": source.metadata,
                }
                for source in self.sources
            ],
            "latency_ms": self.latency_ms,
            "quality": self.quality,
        }


class AnswerGenerator(Protocol):
    def __call__(self, question: str, sources: list[Source]) -> str: ...


@dataclass
class ResearchPolicy:
    source_selection: SourceSelectionPolicy = field(
        default_factory=SourceSelectionPolicy
    )
    local_top_k: int = 5
    web_max_results: int = 5
    log_path: Path | None = Path("logs/research_agent.jsonl")


class ResearchAgent:
    def __init__(
        self,
        *,
        local_retriever: LocalRetriever | None = None,
        web_search: WebSearchTool | None = None,
        python_tool: PythonTool | None = None,
        answer_generator: AnswerGenerator | None = None,
        policy: ResearchPolicy | None = None,
    ) -> None:
        self.local_retriever = local_retriever or ChromaTechnicalRetriever()
        self.web_search = web_search or UnconfiguredWebSearchTool()
        self.python_tool = python_tool or SafePythonTool()
        self.answer_generator = answer_generator or qwen_answer_generator
        self.policy = policy or ResearchPolicy()

    def route(self, query: str) -> QueryRoute:
        signals = self.policy.source_selection.classify(query)
        reasons: list[str] = []

        if signals["python"]:
            reasons.append("calculation_or_code_signal")
            return QueryRoute(
                kind=RouteKind.PYTHON,
                reasons=reasons,
                use_python=True,
            )

        if signals["local"] and (signals["recent"] or signals["web"]):
            reasons.extend(["local_domain_signal", "external_or_recent_signal"])
            return QueryRoute(
                kind=RouteKind.HYBRID,
                reasons=reasons,
                use_local=True,
                use_web=True,
            )

        if signals["local"]:
            reasons.append("local_domain_signal")
            return QueryRoute(
                kind=RouteKind.LOCAL,
                reasons=reasons,
                use_local=True,
            )

        if signals["recent"] or signals["web"]:
            reasons.append("external_or_recent_signal")
            return QueryRoute(
                kind=RouteKind.WEB,
                reasons=reasons,
                use_web=True,
            )

        if (
            signals["short_unknown"]
            and self.policy.source_selection.require_clarification_for_short_unknown
        ):
            reasons.append("ambiguous_short_query")
            return QueryRoute(
                kind=RouteKind.CLARIFY,
                reasons=reasons,
                needs_clarification=True,
            )

        if self.policy.source_selection.allow_web_for_unknown:
            reasons.append("unknown_query_web_allowed")
            return QueryRoute(
                kind=RouteKind.WEB,
                reasons=reasons,
                use_web=True,
            )

        reasons.append("unknown_query_needs_clarification")
        return QueryRoute(
            kind=RouteKind.CLARIFY,
            reasons=reasons,
            needs_clarification=True,
        )

    def answer(self, question: str) -> ResearchAnswer:
        started = time.perf_counter()
        route = self.route(question)
        sources: list[Source] = []
        decisions: list[ToolDecision] = []

        if route.needs_clarification:
            answer = (
                "Preciso de mais contexto para escolher uma fonte com segurança. "
                "Você quer que eu consulte documentos locais, web recente ou execute uma ferramenta?"
            )
            result = ResearchAnswer(
                question=question,
                route=route,
                answer=answer,
                sources=[],
                decisions=[],
                latency_ms=_elapsed_ms(started),
                quality=_quality(answer, []),
            )
            self._log(result)
            return result

        if route.use_local:
            retrieved, decision = self._time_tool(
                tool="local_chromadb",
                action=lambda: self.local_retriever.search(
                    question,
                    top_k=self.policy.local_top_k,
                ),
                reason="consulta à base local ChromaDB",
            )
            sources.extend(retrieved)
            decisions.append(decision)

        if route.use_web:
            retrieved, decision = self._time_tool(
                tool=self.web_search.name,
                action=lambda: self.web_search.search(
                    question,
                    max_results=self.policy.web_max_results,
                ),
                reason="consulta web para informação externa/recente",
            )
            sources.extend(retrieved)
            decisions.append(decision)

        if route.use_python:
            source, decision = self._time_tool(
                tool=self.python_tool.name,
                action=lambda: [self.python_tool.run(question)],
                reason="execução local para cálculo ou validação de código",
            )
            sources.extend(source)
            decisions.append(decision)

        answer = self.answer_generator(question, sources)
        result = ResearchAnswer(
            question=question,
            route=route,
            answer=answer,
            sources=sources,
            decisions=decisions,
            latency_ms=_elapsed_ms(started),
            quality=_quality(answer, sources),
        )
        self._log(result)
        return result

    def _time_tool(
        self,
        *,
        tool: str,
        action: Callable[[], list[Source]],
        reason: str,
    ) -> tuple[list[Source], ToolDecision]:
        started = time.perf_counter()
        sources = action()
        decision = ToolDecision(
            tool=tool,
            action="search_or_execute",
            reason=reason,
            latency_ms=_elapsed_ms(started),
            source_count=len(sources),
        )
        LOGGER.info("tool_decision=%s", asdict(decision))
        return sources, decision

    def _log(self, result: ResearchAnswer) -> None:
        if not self.policy.log_path:
            return

        self.policy.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.policy.log_path.open("a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(result.to_log_record(), ensure_ascii=False))
            log_file.write("\n")


def qwen_answer_generator(question: str, sources: list[Source]) -> str:
    context = build_cited_context(sources)
    user_prompt = f"""
CONTEXTO RECUPERADO:

{context}

PERGUNTA:

{question}

Produza uma resposta fundamentada. Cite fontes no formato [Fonte 1],
[Fonte 2] e identifique quando uma fonte veio de web, ChromaDB local
ou execução Python.
""".strip()

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": CHAT_MODEL,
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": build_system_prompt(),
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            "options": {
                "temperature": 0.2,
                "num_ctx": 8192,
            },
        },
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    payload = response.json()
    return str(payload["message"]["content"]).strip()


def _quality(answer: str, sources: list[Source]) -> dict[str, float | int | str]:
    cited = sum(
        1 for index in range(1, len(sources) + 1) if f"[Fonte {index}]" in answer
    )
    citation_coverage = cited / len(sources) if sources else 0.0
    return {
        "source_count": len(sources),
        "answer_chars": len(answer),
        "citation_coverage": round(citation_coverage, 3),
        "has_answer": int(bool(answer.strip())),
    }


def _elapsed_ms(started: float) -> int:
    return int((time.perf_counter() - started) * 1000)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Routed research agent")
    parser.add_argument("question", nargs="?", help="Pergunta a responder")
    parser.add_argument("--no-log", action="store_true", help="Desativa JSONL logs")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    question = args.question or input("Pergunta: ").strip()
    policy = ResearchPolicy(
        log_path=None if args.no_log else Path("logs/research_agent.jsonl")
    )
    agent = ResearchAgent(policy=policy)
    result = agent.answer(question)

    print(result.answer)
    print()
    print("Rota:", result.route.kind)
    for decision in result.decisions:
        print(
            f"- {decision.tool}: {decision.source_count} fonte(s), "
            f"{decision.latency_ms} ms"
        )


if __name__ == "__main__":
    main()
