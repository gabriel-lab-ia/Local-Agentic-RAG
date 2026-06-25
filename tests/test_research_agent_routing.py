from __future__ import annotations

from src.rag.agent.policy import SourceSelectionPolicy
from src.rag.agent.router import ResearchAgent, ResearchPolicy, RouteKind
from src.rag.agent.sources import Source
from src.rag.agent.tools import MockWebSearchTool


class StaticLocalRetriever:
    def search(self, query: str, top_k: int = 5) -> list[Source]:
        return [
            Source(
                title="Local technical source",
                content=f"Local answer material for {query}",
                kind="local",
                metadata={"collection": "ai_engineering_knowledge"},
                score=0.1,
            )
        ][:top_k]


def deterministic_answer(question: str, sources: list[Source]) -> str:
    citations = " ".join(
        f"[Fonte {index}]"
        for index in range(1, len(sources) + 1)
    )
    return f"Resposta para: {question}. {citations}".strip()


def make_agent(policy: ResearchPolicy | None = None) -> ResearchAgent:
    return ResearchAgent(
        local_retriever=StaticLocalRetriever(),
        web_search=MockWebSearchTool(),
        answer_generator=deterministic_answer,
        policy=policy or ResearchPolicy(log_path=None),
    )


def test_recent_query_routes_to_web() -> None:
    agent = make_agent()

    route = agent.route("What is the latest Qwen release in 2026?")

    assert route.kind == RouteKind.WEB
    assert route.use_web
    assert "external_or_recent_signal" in route.reasons


def test_private_document_query_routes_to_chromadb() -> None:
    agent = make_agent()

    route = agent.route("Explique torchrl nos documentos internos")

    assert route.kind == RouteKind.LOCAL
    assert route.use_local
    assert not route.use_web


def test_mixed_query_routes_to_hybrid() -> None:
    agent = make_agent()

    route = agent.route(
        "Compare os documentos internos de PyTorch com a versão atual da API"
    )

    assert route.kind == RouteKind.HYBRID
    assert route.use_local
    assert route.use_web


def test_math_query_routes_to_python_tool_path() -> None:
    agent = make_agent()

    result = agent.answer("Calcule 128 * 32 / 4")

    assert result.route.kind == RouteKind.PYTHON
    assert result.sources[0].kind == "python"
    assert "Resultado: 1024.0" in result.sources[0].content
    assert result.decisions[0].tool == "python_tool"


def test_unknown_short_query_asks_for_clarification() -> None:
    agent = make_agent()

    result = agent.answer("Transformers?")

    assert result.route.kind == RouteKind.CLARIFY
    assert result.route.needs_clarification
    assert result.sources == []
    assert "mais contexto" in result.answer


def test_unknown_query_uses_web_when_policy_allows() -> None:
    policy = ResearchPolicy(
        source_selection=SourceSelectionPolicy(
            allow_web_for_unknown=True,
            require_clarification_for_short_unknown=False,
        ),
        log_path=None,
    )
    agent = make_agent(policy)

    result = agent.answer("Tell me about an unfamiliar external research topic")

    assert result.route.kind == RouteKind.WEB
    assert result.sources[0].kind == "web"
    assert result.decisions[0].tool == "mock_web_search"
