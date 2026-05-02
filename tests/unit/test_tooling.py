from __future__ import annotations

import sys
from pathlib import Path

from graphix_lab.app.tooling_service import (
    build_bootstrap_resync_command,
    build_license_command,
    build_quality_commands,
    build_test_command,
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
