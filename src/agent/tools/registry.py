from __future__ import annotations

from pathlib import Path
from typing import Callable

from src.agent.schemas.tool_call import ToolCall, ToolName
from src.agent.tools.filesystem import (
    list_directory,
    read_file,
    search_code,
)
from src.agent.tools.git import git_status


ToolHandler = Callable[..., dict[str, object]]


class ToolExecutionError(RuntimeError):
    """Raised when a validated tool call cannot be executed."""


class ToolRegistry:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()

        self._handlers: dict[ToolName, ToolHandler] = {
            ToolName.LIST_DIRECTORY: list_directory,
            ToolName.READ_FILE: read_file,
            ToolName.SEARCH_CODE: search_code,
            ToolName.GIT_STATUS: git_status,
        }

    def execute(self, call: ToolCall) -> dict[str, object]:
        if call.tool is ToolName.FINAL_ANSWER:
            return {
                "tool": call.tool.value,
                "success": True,
                "result": call.arguments,
            }

        handler = self._handlers.get(call.tool)

        if handler is None:
            raise ToolExecutionError(
                f"A ferramenta {call.tool.value!r} ainda não possui executor."
            )

        try:
            result = handler(
                workspace=self.workspace,
                **call.arguments,
            )
        except TypeError as exc:
            raise ToolExecutionError(
                f"Argumentos inválidos para {call.tool.value!r}: {exc}"
            ) from exc
        except Exception as exc:
            return {
                "tool": call.tool.value,
                "success": False,
                "error": str(exc),
            }

        return {
            "tool": call.tool.value,
            "success": True,
            "result": result,
        }

    def available_tools(self) -> tuple[str, ...]:
        return tuple(tool.value for tool in self._handlers)
