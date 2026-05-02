from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _cli_env() -> dict[str, str]:
    repo_root = Path(__file__).resolve().parents[2]
    src_dir = repo_root / "src"
    environment = os.environ.copy()
    existing_path = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = (
        str(src_dir) if not existing_path else os.pathsep.join([str(src_dir), existing_path])
    )
    return environment


def test_cli_clean_dry_run_command_runs_successfully() -> None:
    completed_process = subprocess.run(
        [sys.executable, "-m", "graphix_lab.cli", "clean", "--dry-run"],
        check=False,
        capture_output=True,
        text=True,
        env=_cli_env(),
    )

    assert completed_process.returncode == 0
    assert "Would remove" in completed_process.stdout


def test_cli_help_lists_expected_commands() -> None:
    completed_process = subprocess.run(
        [sys.executable, "-m", "graphix_lab.cli", "--help"],
        check=False,
        capture_output=True,
        text=True,
        env=_cli_env(),
    )

    assert completed_process.returncode == 0
    assert "bootstrap" in completed_process.stdout
    assert "clean" in completed_process.stdout
    assert "licenses" in completed_process.stdout
    assert "demo" not in completed_process.stdout
