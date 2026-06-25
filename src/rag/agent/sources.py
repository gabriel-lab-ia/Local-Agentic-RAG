from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


SourceKind = Literal["local", "web", "python"]


@dataclass(frozen=True)
class Source:
    title: str
    content: str
    kind: SourceKind
    metadata: dict[str, Any] = field(default_factory=dict)
    url: str | None = None
    score: float | None = None

    def citation_label(self, index: int) -> str:
        return f"[Fonte {index}]"

    def to_context_block(self, index: int) -> str:
        lines = [
            self.citation_label(index),
            f"Tipo: {self.kind}",
            f"Título: {self.title}",
        ]

        if self.url:
            lines.append(f"URL: {self.url}")

        if self.score is not None:
            lines.append(f"Score: {self.score:.4f}")

        for key, value in sorted(self.metadata.items()):
            if value is None or key in {"text", "document"}:
                continue
            lines.append(f"{key}: {value}")

        lines.extend(["", self.content])
        return "\n".join(lines)


def build_cited_context(sources: list[Source]) -> str:
    return "\n\n---\n\n".join(
        source.to_context_block(index)
        for index, source in enumerate(sources, start=1)
    )
