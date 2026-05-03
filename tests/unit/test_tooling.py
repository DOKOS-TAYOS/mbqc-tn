from __future__ import annotations

import shutil
import sys
import tomllib
from pathlib import Path
from subprocess import CompletedProcess

import pytest

import graphix_lab.app.tooling_service as tooling_service
from graphix_lab.app.tooling_service import (
    build_bootstrap_resync_command,
    build_cli_help_command,
    build_import_smoke_command,
    build_license_command,
    build_quality_commands,
    build_test_command,
    load_package_name,
    run_commands,
)


def _repo_local_workspace(name: str) -> Path:
    repo_root = Path(__file__).resolve().parents[2]
    workspace_root = repo_root / "test-artifacts" / name
    if workspace_root.exists():
        shutil.rmtree(workspace_root)
    workspace_root.mkdir(parents=True)
    return workspace_root


def test_quality_commands_cover_lint_format_release_smoke_test_and_typecheck() -> None:
    workspace_root = _repo_local_workspace("tooling-quality-commands")
    (workspace_root / "pyproject.toml").write_text(
        """
[tool.vibe_template]
package_name = "graphix_lab"
""".strip(),
        encoding="utf-8",
    )

    commands = build_quality_commands(project_root=workspace_root, include_format_fix=True)

    assert commands == [
        [sys.executable, "-m", "ruff", "check", ".", "--fix"],
        [sys.executable, "-m", "ruff", "format", "."],
        [sys.executable, "-c", "import graphix_lab; print(graphix_lab.__all__)"],
        [sys.executable, "-m", "graphix_lab.cli", "--help"],
        [sys.executable, "-m", "pytest"],
        [sys.executable, "-m", "pyright"],
    ]


def test_release_smoke_commands_use_the_requested_package_name() -> None:
    assert build_import_smoke_command("graphix_lab") == [
        sys.executable,
        "-c",
        "import graphix_lab; print(graphix_lab.__all__)",
    ]
    assert build_cli_help_command("graphix_lab") == [
        sys.executable,
        "-m",
        "graphix_lab.cli",
        "--help",
    ]


def test_license_command_generates_compact_inventory() -> None:
    command = build_license_command(
        output_file=Path("THIRD_PARTY_LICENSES"),
        project_root=Path("workspace"),
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


def test_license_command_ignores_repo_local_editable_aliases(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace_root = _repo_local_workspace("tooling-license-command")

    class FakeDistribution:
        def __init__(self, name: str, direct_url_text: str | None) -> None:
            self.metadata = {"Name": name}
            self._direct_url_text = direct_url_text

        def read_text(self, filename: str) -> str | None:
            assert filename == "direct_url.json"
            return self._direct_url_text

    project_url = f'{{"dir_info": {{"editable": true}}, "url": "{workspace_root.as_uri()}"}}'
    other_url = '{"dir_info": {"editable": true}, "url": "file:///tmp/other-project"}'

    monkeypatch.setattr(
        tooling_service.metadata,
        "distributions",
        lambda: [
            FakeDistribution("graphix-lab", project_url),
            FakeDistribution("project-name", project_url),
            FakeDistribution("other-project", other_url),
            FakeDistribution("no-direct-url", None),
        ],
    )

    command = build_license_command(
        output_file=Path("THIRD_PARTY_LICENSES"),
        project_root=workspace_root,
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
        "project-name",
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


def test_load_package_name_defaults_to_graphix_lab_when_pyproject_is_missing() -> None:
    workspace_root = _repo_local_workspace("tooling-package-name-default")

    assert load_package_name(workspace_root) == "graphix_lab"


def test_pyproject_release_metadata_keeps_urls_and_dependencies_separate() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    pyproject_data = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))
    project_data = pyproject_data["project"]

    assert project_data["urls"] == {
        "Homepage": "https://github.com/DOKOS-TAYOS/mbqc-tn",
        "Repository": "https://github.com/DOKOS-TAYOS/mbqc-tn",
        "Issues": "https://github.com/DOKOS-TAYOS/mbqc-tn/issues",
    }
    assert "graphix>=0.3.5,<0.4" in project_data["dependencies"]


def test_pyproject_disables_cacheprovider_for_portable_pytest_runs() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    pyproject_data = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))

    assert "-p no:cacheprovider" in pyproject_data["tool"]["pytest"]["ini_options"]["addopts"]


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
