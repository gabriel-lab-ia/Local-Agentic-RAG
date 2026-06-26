from pathlib import Path

import pytest

from src.agent.policies.paths import (
    PathPolicyError,
    resolve_workspace_path,
)
from src.agent.schemas.tool_call import ToolCall, ToolName
from src.agent.tools.filesystem import (
    list_directory,
    read_file,
    search_code,
)
from src.agent.tools.registry import ToolRegistry


def test_resolve_workspace_path_rejects_escape(
    tmp_path: Path,
) -> None:
    with pytest.raises(PathPolicyError):
        resolve_workspace_path(tmp_path, "../secret.txt")


def test_read_file_reads_utf8_file(tmp_path: Path) -> None:
    target = tmp_path / "README.md"
    target.write_text("agentic core", encoding="utf-8")

    result = read_file(tmp_path, "README.md")

    assert result["content"] == "agentic core"
    assert result["size_bytes"] == len("agentic core")


def test_list_directory_returns_entries(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "README.md").write_text("test", encoding="utf-8")

    result = list_directory(tmp_path)

    assert result["entries"] == [
        {"name": "src", "type": "directory"},
        {"name": "README.md", "type": "file"},
    ]


def test_search_code_returns_matching_lines(
    tmp_path: Path,
) -> None:
    source = tmp_path / "example.py"
    source.write_text(
        "def hello():\n    return 'agentic core'\n",
        encoding="utf-8",
    )

    result = search_code(tmp_path, "agentic")

    assert result["matches"] == [
        {
            "path": "example.py",
            "line": 2,
            "text": "return 'agentic core'",
        }
    ]


def test_search_code_ignores_local_vector_store(
    tmp_path: Path,
) -> None:
    chroma_dir = tmp_path / "data" / "chroma"
    chroma_dir.mkdir(parents=True)
    (chroma_dir / "chroma.sqlite3").write_text("agentic secret", encoding="utf-8")
    safe_file = tmp_path / "notes.md"
    safe_file.write_text("agentic public note", encoding="utf-8")

    result = search_code(tmp_path, "agentic")

    assert result["matches"] == [
        {
            "path": "notes.md",
            "line": 1,
            "text": "agentic public note",
        }
    ]


def test_registry_executes_read_file(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "private agent",
        encoding="utf-8",
    )

    registry = ToolRegistry(tmp_path)

    result = registry.execute(
        ToolCall(
            tool=ToolName.READ_FILE,
            arguments={"path": "README.md"},
            reason="Entender o projeto.",
        )
    )

    assert result["success"] is True
    assert result["result"]["content"] == "private agent"


def test_registry_returns_controlled_tool_error(
    tmp_path: Path,
) -> None:
    registry = ToolRegistry(tmp_path)

    result = registry.execute(
        ToolCall(
            tool=ToolName.READ_FILE,
            arguments={"path": "missing.txt"},
            reason="Ler arquivo.",
        )
    )

    assert result["success"] is False
    assert "não encontrado" in result["error"]


def test_registry_handles_final_answer(tmp_path: Path) -> None:
    registry = ToolRegistry(tmp_path)

    result = registry.execute(
        ToolCall(
            tool=ToolName.FINAL_ANSWER,
            arguments={"content": "Concluído."},
            reason="Tarefa terminada.",
        )
    )

    assert result == {
        "tool": "final_answer",
        "success": True,
        "result": {"content": "Concluído."},
    }
