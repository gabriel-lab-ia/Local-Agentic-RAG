from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class ToolCallValidationError(ValueError):
    """Raised when a model-generated tool call violates the contract."""


class ToolName(StrEnum):
    LIST_DIRECTORY = "list_directory"
    READ_FILE = "read_file"
    SEARCH_CODE = "search_code"
    QUERY_RAG = "query_rag"
    GIT_STATUS = "git_status"
    RUN_TESTS = "run_tests"
    RUN_LINTER = "run_linter"
    FINAL_ANSWER = "final_answer"


@dataclass(frozen=True, slots=True)
class ToolCall:
    tool: ToolName
    arguments: dict[str, Any]
    reason: str


_REQUIRED_FIELDS = {
    "tool",
    "arguments",
    "reason",
}


def _reject_markdown_fences(raw: str) -> None:
    if "```" in raw:
        raise ToolCallValidationError(
            "A chamada de ferramenta deve conter JSON puro, sem Markdown."
        )


def _validate_final_answer(arguments: dict[str, Any]) -> None:
    expected_fields = {"content"}

    if set(arguments) != expected_fields:
        raise ToolCallValidationError("final_answer aceita somente o campo 'content'.")

    content = arguments.get("content")

    if not isinstance(content, str) or not content.strip():
        raise ToolCallValidationError(
            "final_answer exige 'content' como string não vazia."
        )


def parse_tool_call(raw: str) -> ToolCall:
    """Parse and strictly validate a JSON tool call produced by the model."""
    if not isinstance(raw, str) or not raw.strip():
        raise ToolCallValidationError("A resposta do modelo está vazia.")

    _reject_markdown_fences(raw)

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ToolCallValidationError(f"JSON inválido: {exc.msg}.") from exc

    if not isinstance(payload, dict):
        raise ToolCallValidationError("A raiz da chamada deve ser um objeto JSON.")

    received_fields = set(payload)

    missing_fields = _REQUIRED_FIELDS - received_fields
    extra_fields = received_fields - _REQUIRED_FIELDS

    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ToolCallValidationError(f"Campos obrigatórios ausentes: {missing}.")

    if extra_fields:
        extra = ", ".join(sorted(extra_fields))
        raise ToolCallValidationError(f"Campos não permitidos: {extra}.")

    raw_tool = payload["tool"]

    if not isinstance(raw_tool, str):
        raise ToolCallValidationError("O campo 'tool' deve ser uma string.")

    try:
        tool = ToolName(raw_tool)
    except ValueError as exc:
        allowed = ", ".join(tool_name.value for tool_name in ToolName)
        raise ToolCallValidationError(
            f"Ferramenta desconhecida: {raw_tool!r}. Permitidas: {allowed}."
        ) from exc

    arguments = payload["arguments"]

    if not isinstance(arguments, dict):
        raise ToolCallValidationError("O campo 'arguments' deve ser um objeto JSON.")

    reason = payload["reason"]

    if not isinstance(reason, str) or not reason.strip():
        raise ToolCallValidationError("O campo 'reason' deve ser uma string não vazia.")

    if tool is ToolName.FINAL_ANSWER:
        _validate_final_answer(arguments)

    return ToolCall(
        tool=tool,
        arguments=arguments,
        reason=reason.strip(),
    )
