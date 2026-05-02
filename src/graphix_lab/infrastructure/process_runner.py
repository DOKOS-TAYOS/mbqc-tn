from __future__ import annotations

import subprocess
from pathlib import Path


def run_process(command: list[str], root: Path) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(command, check=False, cwd=root)
