from __future__ import annotations

import ast
import io
import math
import re
import subprocess
import sys
import tempfile
import time
from contextlib import redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from src.rag.agent.sources import Source
from src.rag.chat_technical import (
    DEFAULT_TOP_K,
    RetrievedChunk,
    get_collection,
    retrieve_chunks,
)


class LocalRetriever(Protocol):
    def search(self, query: str, top_k: int = DEFAULT_TOP_K) -> list[Source]:
        ...


class WebSearchTool(Protocol):
    name: str

    def search(self, query: str, max_results: int = 5) -> list[Source]:
        ...


class PythonTool(Protocol):
    name: str

    def run(self, query: str) -> Source:
        ...


@dataclass
class ChromaTechnicalRetriever:
    domain: str | None = None

    def search(self, query: str, top_k: int = DEFAULT_TOP_K) -> list[Source]:
        collection = get_collection()
        chunks = retrieve_chunks(
            collection=collection,
            query=query,
            top_k=top_k,
            domain=self.domain,
        )
        return [source_from_chunk(chunk) for chunk in chunks]


def source_from_chunk(chunk: RetrievedChunk) -> Source:
    metadata = dict(chunk.metadata)
    title = str(metadata.get("title") or metadata.get("source") or "Local RAG chunk")
    url = metadata.get("url")
    return Source(
        title=title,
        content=chunk.document,
        kind="local",
        metadata=metadata,
        url=str(url) if url else None,
        score=chunk.distance,
    )


@dataclass
class MockWebSearchTool:
    fixtures: dict[str, list[Source]] | None = None
    name: str = "mock_web_search"

    def search(self, query: str, max_results: int = 5) -> list[Source]:
        if self.fixtures:
            normalized = query.casefold()
            for key, sources in self.fixtures.items():
                if key.casefold() in normalized:
                    return sources[:max_results]

        return [
            Source(
                title="Mock web result",
                content=(
                    "Resultado web simulado para testes locais. Configure um "
                    "provedor Tavily, Serper ou Firecrawl para busca real."
                ),
                kind="web",
                metadata={
                    "provider": self.name,
                    "query": query,
                    "privacy": "mock-only",
                },
                url="https://example.test/mock-web-result",
                score=1.0,
            )
        ][:max_results]


class UnconfiguredWebSearchTool:
    name = "unconfigured_web_search"

    def search(self, query: str, max_results: int = 5) -> list[Source]:
        raise RuntimeError(
            "Nenhum provedor de web search está configurado. "
            "Use MockWebSearchTool em testes ou implemente Tavily/Serper/Firecrawl."
        )


class SafePythonTool:
    name = "python_tool"

    def run(self, query: str) -> Source:
        started = time.perf_counter()
        expression = _extract_math_expression(query)

        if expression:
            result = _safe_eval_math(expression)
            content = f"Expressão avaliada: {expression}\nResultado: {result}"
        else:
            content = _run_python_snippet(query)

        latency_ms = int((time.perf_counter() - started) * 1000)
        return Source(
            title="Python/tool execution",
            content=content,
            kind="python",
            metadata={
                "tool": self.name,
                "latency_ms": latency_ms,
            },
        )


def _extract_math_expression(query: str) -> str | None:
    candidate = query.replace("^", "**").replace(",", "")
    matches = re.findall(r"[-+*/().%\d\s]+", candidate)
    expressions = [
        match.strip()
        for match in matches
        if any(char.isdigit() for char in match)
    ]
    if not expressions:
        return None
    expression = max(expressions, key=len)
    if not any(operator in expression for operator in ["+", "-", "*", "/", "%", "**"]):
        return None
    return expression


def _safe_eval_math(expression: str) -> int | float:
    tree = ast.parse(expression, mode="eval")
    return _eval_node(tree.body)


def _eval_node(node: ast.AST) -> int | float:
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        return node.value

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_node(node.operand)

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Mod):
            return left % right
        if isinstance(node.op, ast.Pow):
            if abs(right) > 10:
                raise ValueError("Expoente muito grande para execução segura.")
            return math.pow(left, right)

    raise ValueError("A expressão matemática não é suportada pelo executor seguro.")


def _run_python_snippet(query: str) -> str:
    code = _extract_code_block(query) or query
    if len(code) > 4000:
        raise ValueError("Snippet muito grande para execução local segura.")

    if "input(" in code or "__import__" in code:
        raise ValueError("Snippet usa recursos bloqueados pelo executor seguro.")

    with tempfile.TemporaryDirectory() as temp_dir:
        script = Path(temp_dir) / "snippet.py"
        script.write_text(code, encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, str(script)],
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

    output = io.StringIO()
    with redirect_stdout(output):
        print(f"Código executado com retorno {completed.returncode}.")
        if completed.stdout:
            print("stdout:")
            print(completed.stdout.strip())
        if completed.stderr:
            print("stderr:")
            print(completed.stderr.strip())

    return output.getvalue().strip()


def _extract_code_block(query: str) -> str | None:
    fence = "```"
    if fence not in query:
        return None

    parts = query.split(fence)
    if len(parts) < 3:
        return None

    body = parts[1]
    lines = body.splitlines()
    if lines and lines[0].strip().casefold() in {"python", "py"}:
        lines = lines[1:]
    return "\n".join(lines).strip()
