from __future__ import annotations

from dataclasses import dataclass

from src.rag.agent.router import ResearchAgent, RouteKind


@dataclass(frozen=True)
class RouteDecision:
    primary_tool: str
    reason: str


def route_query(query: str) -> RouteDecision:
    route = ResearchAgent().route(query)
    tool_by_route = {
        RouteKind.LOCAL: "local_rag",
        RouteKind.WEB: "web_search",
        RouteKind.HYBRID: "hybrid_rag_web",
        RouteKind.PYTHON: "python",
        RouteKind.CLARIFY: "clarification",
    }
    return RouteDecision(
        primary_tool=tool_by_route[route.kind],
        reason=", ".join(route.reasons),
    )
