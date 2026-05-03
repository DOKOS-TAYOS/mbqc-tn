from __future__ import annotations

from pathlib import Path
from subprocess import CompletedProcess
from typing import cast

import pytest

import graphix_lab.cli as cli_module
from graphix_lab.app.clean_service import CleanResult


def test_main_accepts_help_as_string(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as sequence_exit:
        cli_module.main(["--help"])
    sequence_output = capsys.readouterr().out

    with pytest.raises(SystemExit) as string_exit:
        cli_module.main("--help")
    string_output = capsys.readouterr().out

    assert sequence_exit.value.code == 0
    assert string_exit.value.code == 0
    assert string_output == sequence_output


def test_main_accepts_clean_dry_run_as_string(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run_clean(root: Path, dry_run: bool) -> CleanResult:
        assert root == Path.cwd()
        assert dry_run is True
        return CleanResult(
            removed_paths=(),
            planned_paths=(),
            failed_paths=(),
        )

    monkeypatch.setattr(
        cli_module,
        "run_clean",
        fake_run_clean,
    )

    assert cli_module.main("clean --dry-run") == 0


def test_main_strips_windows_quotes_from_programmatic_string_arguments(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_output_path: Path | None = None

    def fake_build_license_command(output_file: Path, distribution_name: str) -> list[str]:
        nonlocal captured_output_path
        captured_output_path = output_file
        assert distribution_name == "graphix-lab"
        return ["fake-license-command"]

    def fake_subprocess_run(
        command: list[str],
        *,
        check: bool,
        cwd: Path,
    ) -> CompletedProcess[str]:
        assert command == ["fake-license-command"]
        assert check is False
        assert cwd == Path.cwd()
        return CompletedProcess(args=command, returncode=0)

    monkeypatch.setattr(cli_module, "_uses_windows_argument_splitting", lambda: True)
    monkeypatch.setattr(cli_module, "load_distribution_name", lambda _project_root: "graphix-lab")
    monkeypatch.setattr(cli_module, "build_license_command", fake_build_license_command)
    monkeypatch.setattr(cli_module.subprocess, "run", cast(object, fake_subprocess_run))

    assert cli_module.main('licenses --output "THIRD PARTY.md"') == 0
    assert captured_output_path == Path("THIRD PARTY.md")
