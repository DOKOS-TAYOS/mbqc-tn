from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    src_dir = repo_root / "src"
    environment = os.environ.copy()
    existing_python_path = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = (
        str(src_dir)
        if not existing_python_path
        else os.pathsep.join([str(src_dir), existing_python_path])
    )
    completed_process = subprocess.run(
        [sys.executable, "-m", "graphix_lab.cli", "clean", "--dry-run"],
        check=True,
        capture_output=True,
        text=True,
        cwd=repo_root,
        env=environment,
    )
    print("CLI example output:")
    print(completed_process.stdout.strip())


if __name__ == "__main__":
    main()
