from dataclasses import dataclass


@dataclass(frozen=True)
class RouteDecision:
    primary_tool: str
    reason: str


def route_query(query: str) -> RouteDecision:
    text = query.lower()

    recent_terms = ["recente", "recentes", "notícias", "hoje", "atual", "latest"]
    private_terms = ["meus documentos", "meu projeto", "qwen local", "chroma", "rag"]
    math_terms = ["calcule", "calcular", "*", "+", "-", "/", "equação"]

    if any(term in text for term in recent_terms):
        return RouteDecision("web_search", "Query depends on recent or external information.")

    if any(term in text for term in private_terms):
        return RouteDecision("local_rag", "Query likely depends on private/local project knowledge.")

    if any(term in text for term in math_terms):
        return RouteDecision("python", "Query requires calculation or tool execution.")

    return RouteDecision("direct_llm", "Query can be answered directly.")

