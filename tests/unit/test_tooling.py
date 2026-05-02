from __future__ import annotations

import sys
from pathlib import Path
from subprocess import CompletedProcess

import pytest

import graphix_lab.app.tooling_service as tooling_service
from graphix_lab.app.tooling_service import (
    build_bootstrap_resync_command,
    build_license_command,
    build_quality_commands,
    build_test_command,
    run_commands,
)


def test_quality_commands_cover_lint_format_test_and_typecheck() -> None:
    commands = build_quality_commands(include_format_fix=True)

    assert commands == [
        [sys.executable, "-m", "ruff", "check", ".", "--fix"],
        [sys.executable, "-m", "ruff", "format", "."],
        [sys.executable, "-m", "pytest"],
        [sys.executable, "-m", "pyright"],
    ]


def test_license_command_generates_compact_inventory() -> None:
    command = build_license_command(
        output_file=Path("THIRD_PARTY_LICENSES"),
        distribution_name="graphix-lab",
    )

    assert command == [
        sys.executable,
        "-m",
        "piplicenses",
        "--python",
        sys.executable,
        "--format=markdown",
        "--with-urls",
        "--ignore-packages",
        "graphix-lab",
        "--output-file",
        "THIRD_PARTY_LICENSES",
    ]


def test_test_command_uses_active_interpreter() -> None:
    command = build_test_command()

    assert command == [sys.executable, "-m", "pytest"]


def test_bootstrap_resync_command_uses_active_interpreter() -> None:
    command = build_bootstrap_resync_command()

    assert command == [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-e",
        ".[dev]",
    ]


def test_run_commands_uses_subprocess_with_workspace_root(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[list[str], bool, Path]] = []

    def fake_subprocess_run(
        command: list[str],
        check: bool,
        cwd: Path,
    ) -> CompletedProcess[bytes]:
        calls.append((command, check, cwd))
        return CompletedProcess(args=command, returncode=0)

    monkeypatch.setattr(tooling_service.subprocess, "run", fake_subprocess_run)

    results = run_commands([["cmd-one"], ["cmd-two"]], root=Path("workspace"))

    assert [result.command for result in results] == [("cmd-one",), ("cmd-two",)]
    assert [result.returncode for result in results] == [0, 0]
    assert calls == [
        (["cmd-one"], False, Path("workspace")),
        (["cmd-two"], False, Path("workspace")),
    ]


def test_run_commands_stops_after_the_first_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[list[str]] = []

    def fake_subprocess_run(
        command: list[str],
        check: bool,
        cwd: Path,
    ) -> CompletedProcess[bytes]:
        del check, cwd
        calls.append(command)
        return_code = 1 if command == ["cmd-one"] else 0
        return CompletedProcess(args=command, returncode=return_code)

    monkeypatch.setattr(tooling_service.subprocess, "run", fake_subprocess_run)

    results = run_commands([["cmd-one"], ["cmd-two"]], root=Path("workspace"))

    assert [result.command for result in results] == [("cmd-one",)]
    assert [result.returncode for result in results] == [1]
    assert calls == [["cmd-one"]]
