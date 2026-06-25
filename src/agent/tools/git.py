from __future__ import annotations

import subprocess
from pathlib import Path


COMMAND_TIMEOUT = 15


def git_status(workspace: Path) -> dict[str, object]:
    workspace = workspace.resolve()

    result = subprocess.run(
        ["git", "status", "--short", "--branch"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=COMMAND_TIMEOUT,
        check=False,
    )

    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "success": result.returncode == 0,
    }
