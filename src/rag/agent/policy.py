from __future__ import annotations

from dataclasses import dataclass


RECENT_TERMS = {
    "latest",
    "most recent",
    "recent",
    "today",
    "this week",
    "this month",
    "current",
    "now",
    "2025",
    "2026",
    "último",
    "mais recente",
    "hoje",
    "atual",
    "agora",
}

LOCAL_TERMS = {
    "documento",
    "documentos",
    "interno",
    "private",
    "privado",
    "chroma",
    "chromadb",
    "rag",
    "pytorch",
    "torchrl",
    "gymnasium",
    "reinforcement learning",
    "livro",
    "pressman",
    "ética",
    "algoritmos",
}

PYTHON_TERMS = {
    "calculate",
    "compute",
    "calcule",
    "calcular",
    "resultado de",
    "execute",
    "rodar",
    "run this code",
    "validar código",
    "validate code",
    "python",
}

WEB_TERMS = {
    "web",
    "internet",
    "notícia",
    "news",
    "site",
    "release",
    "versão",
    "benchmark atual",
    "preço",
    "lei",
}


@dataclass(frozen=True)
class SourceSelectionPolicy:
    prefer_local_first: bool = True
    allow_web_for_unknown: bool = True
    require_clarification_for_short_unknown: bool = True
    min_unknown_query_terms: int = 3

    def classify(self, query: str) -> dict[str, bool]:
        normalized = query.casefold()
        term_count = len(normalized.split())
        has_math_operator = any(
            operator in normalized for operator in ["+", "-", "*", "/", "%", "```"]
        )

        return {
            "recent": _contains_any(normalized, RECENT_TERMS),
            "local": _contains_any(normalized, LOCAL_TERMS),
            "python": _contains_any(normalized, PYTHON_TERMS) or has_math_operator,
            "web": _contains_any(normalized, WEB_TERMS),
            "short_unknown": term_count < self.min_unknown_query_terms,
        }


def _contains_any(text: str, terms: set[str]) -> bool:
    return any(term in text for term in terms)
