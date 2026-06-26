# Agentic Core

The Agentic Core is a read-only prototype for safe tool routing. It is designed to test the contract between a local model and deterministic tools before introducing any write capability.

## Model

`src/agent/core/model.py` calls Qwen 3 4B through Ollama:

- endpoint: `http://localhost:11434/api/generate`;
- default model: `qwen3:4b`;
- `format: json`;
- `think: false`;
- temperature `0.0`;
- request timeout.

Thinking is disabled for routing because the expected output is a compact JSON decision, not a chain-of-thought response.

## JSON Contract

The model must produce:

```json
{
  "tool": "git_status",
  "arguments": {},
  "reason": "Check repository state."
}
```

No Markdown, prose prefix, prose suffix, or fenced block is accepted.

## Parser

`parse_tool_call()` enforces:

- object root;
- exact required fields;
- no extra fields;
- string tool name;
- object arguments;
- non-empty reason;
- enum-backed tool names;
- final answer arguments limited to `content`.

Invalid model output raises `ToolCallValidationError`.

## ToolCall

`ToolCall` is an immutable dataclass with:

- `tool: ToolName`;
- `arguments: dict[str, Any]`;
- `reason: str`.

The parser converts raw strings into this typed object before execution.

## ToolRegistry

`ToolRegistry` maps validated tool names to implemented handlers. Current handlers:

- `list_directory`;
- `read_file`;
- `search_code`;
- `git_status`.

`final_answer` is handled as a terminal structured response. Planned enum values without handlers return controlled execution errors.

## Filesystem Tools

Filesystem tools are read-only and workspace-confined:

- `list_directory` caps directory entries.
- `read_file` accepts UTF-8 text and enforces a file-size limit.
- `search_code` searches text files, caps results, skips large files, and ignores local runtime/sensitive directories.
- all path arguments go through `resolve_workspace_path()`.

## Git Tool

The Git tool returns `git status --short --branch` only. It does not commit, push, reset, clean, checkout, or mutate history.

## Future Execution Loop

The next architectural step is an observation-action loop:

1. receive task;
2. choose read-only tool;
3. observe result;
4. choose next action or final answer;
5. stop on budget, error, or completion.

Write tools should come only after patch previews, user approval gates, diff validation, tests, and sandboxing are in place.
