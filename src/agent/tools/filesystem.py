from __future__ import annotations

from pathlib import Path

from src.agent.policies.paths import resolve_workspace_path


MAX_FILE_BYTES = 256_000
MAX_DIRECTORY_ENTRIES = 500
MAX_SEARCH_RESULTS = 100


def list_directory(
    workspace: Path,
    path: str = ".",
) -> dict[str, object]:
    target = resolve_workspace_path(workspace, path)

    if not target.exists():
        raise FileNotFoundError(f"Diretório não encontrado: {path}")

    if not target.is_dir():
        raise NotADirectoryError(f"O caminho não é um diretório: {path}")

    entries = sorted(
        target.iterdir(),
        key=lambda item: (not item.is_dir(), item.name.casefold()),
    )

    truncated = len(entries) > MAX_DIRECTORY_ENTRIES
    entries = entries[:MAX_DIRECTORY_ENTRIES]

    return {
        "path": str(target.relative_to(workspace.resolve())) or ".",
        "entries": [
            {
                "name": entry.name,
                "type": "directory" if entry.is_dir() else "file",
            }
            for entry in entries
        ],
        "truncated": truncated,
    }


def read_file(
    workspace: Path,
    path: str,
) -> dict[str, object]:
    target = resolve_workspace_path(workspace, path)

    if not target.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    if not target.is_file():
        raise IsADirectoryError(f"O caminho não é um arquivo: {path}")

    size = target.stat().st_size

    if size > MAX_FILE_BYTES:
        raise ValueError(f"Arquivo excede o limite de {MAX_FILE_BYTES} bytes.")

    try:
        content = target.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            "A ferramenta read_file aceita apenas arquivos UTF-8."
        ) from exc

    return {
        "path": str(target.relative_to(workspace.resolve())),
        "size_bytes": size,
        "content": content,
    }


def search_code(
    workspace: Path,
    query: str,
    path: str = ".",
) -> dict[str, object]:
    if not isinstance(query, str) or not query.strip():
        raise ValueError("A consulta deve ser uma string não vazia.")

    root = resolve_workspace_path(workspace, path)

    if not root.exists():
        raise FileNotFoundError(f"Caminho não encontrado: {path}")

    if not root.is_dir():
        raise NotADirectoryError(f"O caminho não é um diretório: {path}")

    normalized_query = query.casefold()
    matches: list[dict[str, object]] = []

    ignored_directories = {
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        "data/chroma",
    }

    for candidate in root.rglob("*"):
        if len(matches) >= MAX_SEARCH_RESULTS:
            break

        relative = candidate.relative_to(workspace.resolve())

        if any(ignored in relative.parts for ignored in ignored_directories):
            continue

        if not candidate.is_file():
            continue

        if candidate.stat().st_size > MAX_FILE_BYTES:
            continue

        try:
            lines = candidate.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue

        for line_number, line in enumerate(lines, start=1):
            if normalized_query not in line.casefold():
                continue

            matches.append(
                {
                    "path": str(relative),
                    "line": line_number,
                    "text": line.strip(),
                }
            )

            if len(matches) >= MAX_SEARCH_RESULTS:
                break

    return {
        "query": query,
        "path": path,
        "matches": matches,
        "truncated": len(matches) >= MAX_SEARCH_RESULTS,
    }
