from __future__ import annotations

import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class CommandExecutionResult:
    command: tuple[str, ...]
    returncode: int


def _build_module_command(module_name: str, *args: str) -> list[str]:
    return [sys.executable, "-m", module_name, *args]


def build_quality_commands(include_format_fix: bool = True) -> list[list[str]]:
    commands: list[list[str]] = [_build_module_command("ruff", "check", ".")]
    if include_format_fix:
        commands[0].append("--fix")
        commands.append(_build_module_command("ruff", "format", "."))
    else:
        commands.append(_build_module_command("ruff", "format", ".", "--check"))
    commands.extend(
        [
            _build_module_command("pytest"),
            _build_module_command("pyright"),
        ]
    )
    return commands


def build_test_command() -> list[str]:
    return _build_module_command("pytest")


def build_bootstrap_resync_command() -> list[str]:
    return [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-e",
        ".[dev]",
    ]


def load_distribution_name(project_root: Path) -> str:
    pyproject_data = tomllib.loads((project_root / "pyproject.toml").read_text(encoding="utf-8"))
    return str(pyproject_data["project"]["name"])


def build_license_command(output_file: Path, distribution_name: str) -> list[str]:
    return [
        sys.executable,
        "-m",
        "piplicenses",
        "--python",
        sys.executable,
        "--format=markdown",
        "--with-urls",
        "--ignore-packages",
        distribution_name,
        "--output-file",
        str(output_file),
    ]


def run_commands(commands: list[list[str]], root: Path) -> list[CommandExecutionResult]:
    results: list[CommandExecutionResult] = []
    for command in commands:
        completed_process = subprocess.run(command, check=False, cwd=root)
        results.append(
            CommandExecutionResult(
                command=tuple(command),
                returncode=completed_process.returncode,
            )
        )
        if completed_process.returncode != 0:
            break
    return results
