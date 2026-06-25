import pytest

from src.agent.schemas.tool_call import (
    ToolCallValidationError,
    ToolName,
    parse_tool_call,
)


def test_parses_valid_tool_call() -> None:
    raw = """
    {
        "tool": "read_file",
        "arguments": {"path": "README.md"},
        "reason": "Preciso entender o projeto."
    }
    """

    tool_call = parse_tool_call(raw)

    assert tool_call.tool is ToolName.READ_FILE
    assert tool_call.arguments == {"path": "README.md"}
    assert tool_call.reason == "Preciso entender o projeto."


def test_parses_valid_final_answer() -> None:
    raw = """
    {
        "tool": "final_answer",
        "arguments": {"content": "Tarefa concluída."},
        "reason": "Não são necessárias outras ferramentas."
    }
    """

    tool_call = parse_tool_call(raw)

    assert tool_call.tool is ToolName.FINAL_ANSWER
    assert tool_call.arguments["content"] == "Tarefa concluída."


def test_rejects_markdown_code_fence() -> None:
    raw = """```json
    {
        "tool": "git_status",
        "arguments": {},
        "reason": "Verificar o repositório."
    }
    ```"""

    with pytest.raises(
        ToolCallValidationError,
        match="JSON puro",
    ):
        parse_tool_call(raw)


def test_rejects_invalid_json() -> None:
    with pytest.raises(
        ToolCallValidationError,
        match="JSON inválido",
    ):
        parse_tool_call("{invalid}")


def test_rejects_unknown_tool() -> None:
    raw = """
    {
        "tool": "delete_everything",
        "arguments": {},
        "reason": "Teste."
    }
    """

    with pytest.raises(
        ToolCallValidationError,
        match="Ferramenta desconhecida",
    ):
        parse_tool_call(raw)


def test_rejects_missing_field() -> None:
    raw = """
    {
        "tool": "git_status",
        "arguments": {}
    }
    """

    with pytest.raises(
        ToolCallValidationError,
        match="Campos obrigatórios ausentes",
    ):
        parse_tool_call(raw)


def test_rejects_extra_field() -> None:
    raw = """
    {
        "tool": "git_status",
        "arguments": {},
        "reason": "Verificar estado.",
        "command": "sudo rm -rf /"
    }
    """

    with pytest.raises(
        ToolCallValidationError,
        match="Campos não permitidos",
    ):
        parse_tool_call(raw)


def test_rejects_non_object_arguments() -> None:
    raw = """
    {
        "tool": "read_file",
        "arguments": "README.md",
        "reason": "Ler arquivo."
    }
    """

    with pytest.raises(
        ToolCallValidationError,
        match="'arguments' deve ser um objeto",
    ):
        parse_tool_call(raw)


def test_rejects_empty_reason() -> None:
    raw = """
    {
        "tool": "git_status",
        "arguments": {},
        "reason": " "
    }
    """

    with pytest.raises(
        ToolCallValidationError,
        match="'reason' deve ser uma string não vazia",
    ):
        parse_tool_call(raw)


def test_rejects_invalid_final_answer_arguments() -> None:
    raw = """
    {
        "tool": "final_answer",
        "arguments": {"message": "Concluído."},
        "reason": "Fim da tarefa."
    }
    """

    with pytest.raises(
        ToolCallValidationError,
        match="somente o campo 'content'",
    ):
        parse_tool_call(raw)
