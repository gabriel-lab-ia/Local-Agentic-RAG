from unittest.mock import Mock, patch

import pytest

from src.agent.core.model import (
    AgentModelError,
    build_tool_prompt,
    request_tool_call,
)
from src.agent.schemas.tool_call import ToolName


def test_build_tool_prompt_contains_task() -> None:
    prompt = build_tool_prompt("Leia o README.")

    assert "Leia o README." in prompt
    assert "responda somente com JSON puro" in prompt


@patch("src.agent.core.model.requests.post")
def test_request_tool_call_parses_model_response(
    mock_post: Mock,
) -> None:
    response = Mock()
    response.json.return_value = {
        "response": (
            '{"tool":"read_file",'
            '"arguments":{"path":"README.md"},'
            '"reason":"Entender o projeto."}'
        )
    }
    response.raise_for_status.return_value = None
    mock_post.return_value = response

    call = request_tool_call("Leia o README.")

    assert call.tool is ToolName.READ_FILE
    assert call.arguments == {"path": "README.md"}


@patch("src.agent.core.model.requests.post")
def test_request_tool_call_rejects_invalid_output(
    mock_post: Mock,
) -> None:
    response = Mock()
    response.json.return_value = {"response": "Isto não é JSON."}
    response.raise_for_status.return_value = None
    mock_post.return_value = response

    with pytest.raises(
        AgentModelError,
        match="chamada inválida",
    ):
        request_tool_call("Leia o README.")


def test_request_tool_call_rejects_empty_task() -> None:
    with pytest.raises(
        AgentModelError,
        match="string não vazia",
    ):
        request_tool_call(" ")
