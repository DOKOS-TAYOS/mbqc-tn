from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _example_env() -> dict[str, str]:
    repo_root = Path(__file__).resolve().parents[2]
    src_dir = repo_root / "src"
    environment = os.environ.copy()
    existing_path = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = (
        str(src_dir) if not existing_path else os.pathsep.join([str(src_dir), existing_path])
    )
    return environment


def test_library_example_runs() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    example_path = repo_root / "examples" / "library_usage.py"

    completed_process = subprocess.run(
        [sys.executable, str(example_path)],
        check=False,
        capture_output=True,
        text=True,
        env=_example_env(),
    )

    assert completed_process.returncode == 0
    assert "Library example using CommandRecord" in completed_process.stdout
    assert "Pattern summary tracks 3 commands across 2 nodes." in completed_process.stdout


def test_cli_example_runs() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    example_path = repo_root / "examples" / "cli_usage.py"

    completed_process = subprocess.run(
        [sys.executable, str(example_path)],
        check=False,
        capture_output=True,
        text=True,
        env=_example_env(),
    )

    assert completed_process.returncode == 0
    assert "Would remove" in completed_process.stdout
