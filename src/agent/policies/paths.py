from __future__ import annotations

from pathlib import Path


class PathPolicyError(ValueError):
    """Raised when a requested path escapes the allowed workspace."""


def resolve_workspace_path(
    workspace: Path,
    requested_path: str,
) -> Path:
    if not isinstance(requested_path, str) or not requested_path.strip():
        raise PathPolicyError("O caminho deve ser uma string não vazia.")

    workspace = workspace.resolve()
    candidate = (workspace / requested_path).resolve()

    try:
        candidate.relative_to(workspace)
    except ValueError as exc:
        raise PathPolicyError(
            "O caminho solicitado está fora do workspace permitido."
        ) from exc

    return candidate
