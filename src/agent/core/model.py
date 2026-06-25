from __future__ import annotations

import requests

from src.agent.schemas.tool_call import ToolCall, parse_tool_call


OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen3:4b"
REQUEST_TIMEOUT = 180


class AgentModelError(RuntimeError):
    """Raised when the agent model cannot produce a valid tool call."""


def build_tool_prompt(task: str) -> str:
    return f"""
Você é o roteador de um agente local de engenharia de software.

Escolha exatamente uma ferramenta e responda somente com JSON puro.

Ferramentas:
- list_directory: lista arquivos e diretórios.
- read_file: lê um arquivo UTF-8.
- search_code: pesquisa texto no workspace.
- git_status: consulta o estado do Git.
- final_answer: encerra com uma resposta ao usuário.

Contrato obrigatório:
{{
  "tool": "nome_da_ferramenta",
  "arguments": {{}},
  "reason": "motivo curto"
}}

Exemplos de argumentos:
- list_directory: {{"path": "."}}
- read_file: {{"path": "README.md"}}
- search_code: {{"query": "FastAPI", "path": "src"}}
- git_status: {{}}
- final_answer: {{"content": "resposta final"}}

Não use Markdown.
Não use blocos de código.
Não escreva texto antes ou depois do JSON.

Tarefa:
{task}
""".strip()


def request_tool_call(
    task: str,
    *,
    model: str = DEFAULT_MODEL,
) -> ToolCall:
    if not isinstance(task, str) or not task.strip():
        raise AgentModelError("A tarefa deve ser uma string não vazia.")

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": model,
            "prompt": build_tool_prompt(task),
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.0,
                "num_ctx": 4096,
            },
        },
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    payload = response.json()
    raw_response = payload.get("response")

    if not isinstance(raw_response, str):
        raise AgentModelError("O Ollama não retornou conteúdo textual válido.")

    try:
        return parse_tool_call(raw_response)
    except ValueError as exc:
        raise AgentModelError(f"O modelo produziu uma chamada inválida: {exc}") from exc
