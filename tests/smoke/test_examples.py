from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest


def _example_env() -> dict[str, str]:
    repo_root = Path(__file__).resolve().parents[2]
    src_dir = repo_root / "src"
    environment = os.environ.copy()
    existing_path = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = (
        str(src_dir) if not existing_path else os.pathsep.join([str(src_dir), existing_path])
    )
    return environment


def _run_example(example_name: str) -> subprocess.CompletedProcess[str]:
    repo_root = Path(__file__).resolve().parents[2]
    example_path = repo_root / "examples" / example_name
    return subprocess.run(
        [sys.executable, str(example_path)],
        check=False,
        capture_output=True,
        text=True,
        env=_example_env(),
    )


@pytest.mark.parametrize(
    ("example_name", "headline", "detail"),
    [
        ("one_qubit_rotation.py", "One-qubit rotation example", "Command count:"),
        ("bell_like_pattern.py", "Bell-like pattern example", "Resource summary:"),
        ("trace_slider.py", "Trace slider example", "Trace frames:"),
        ("trace_animation.py", "Trace animation prepared", "Graphix Lab Trace Inspection"),
        ("backend_comparison.py", "Backend comparison example", "Runs recorded:"),
        ("library_usage.py", "Library example using", "Pattern summary tracks"),
        ("cli_usage.py", "CLI example output:", "Would remove"),
    ],
)
def test_example_runs(example_name: str, headline: str, detail: str) -> None:
    completed_process = _run_example(example_name)

    assert completed_process.returncode == 0, completed_process.stderr
    assert headline in completed_process.stdout
    assert detail in completed_process.stdout


def test_qiskit_import_example_runs() -> None:
    completed_process = _run_example("qiskit_import.py")

    assert completed_process.returncode == 0, completed_process.stderr
    assert "Qiskit import example" in completed_process.stdout
    assert (
        "Imported command kinds:" in completed_process.stdout
        or "Qiskit is not installed" in completed_process.stdout
    )
