from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
MAX_TRACKED_FILE_BYTES = 10 * 1024 * 1024

SENSITIVE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        "/" + "home/",
        r"api[_-]?key\s*=",
        r"secret\s*=",
        r"token\s*=",
        r"password\s*=",
    )
]
BLOCKED_TRACKED_PREFIXES = (
    "data/chroma/",
    "data/chroma-backup-",
    "data/archive/",
    "data/processed/",
    "logs/",
    "outputs/",
    "artifacts/",
    "checkpoints/",
    "models/",
    ".venv/",
    ".pytest_cache/",
    ".ruff_cache/",
    ".mypy_cache/",
    ".vscode/",
)
BLOCKED_SUFFIXES = (
    ".gguf",
    ".safetensors",
    ".pt",
    ".pth",
    ".pyc",
)


def main() -> int:
    tracked_files = _git_ls_files()
    failures: list[str] = []

    for relative_path in tracked_files:
        path = WORKSPACE / relative_path

        if relative_path.startswith(BLOCKED_TRACKED_PREFIXES):
            failures.append(f"blocked tracked path: {relative_path}")

        if relative_path.endswith(BLOCKED_SUFFIXES):
            failures.append(f"blocked tracked artifact: {relative_path}")

        if not path.is_file():
            continue

        size = path.stat().st_size
        if size > MAX_TRACKED_FILE_BYTES:
            failures.append(f"tracked file larger than 10 MiB: {relative_path}")

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append(f"non UTF-8 tracked file: {relative_path}")
            continue

        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(text):
                failures.append(
                    f"possible sensitive pattern {pattern.pattern!r}: {relative_path}"
                )

    if failures:
        print("Repository validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Repository validation passed for {len(tracked_files)} tracked files.")
    return 0


def _git_ls_files() -> list[str]:
    result = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
        ],
        cwd=WORKSPACE,
        capture_output=True,
        text=True,
        timeout=15,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


if __name__ == "__main__":
    sys.exit(main())
