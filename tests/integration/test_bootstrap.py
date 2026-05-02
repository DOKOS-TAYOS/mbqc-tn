from __future__ import annotations

import argparse
import re
import shutil
import tomllib
from pathlib import Path
from subprocess import CompletedProcess

import pytest

import graphix_lab.cli as cli_module
from graphix_lab.app.bootstrap_service import (
    SKIP_DIRECTORIES,
    SKIP_DIRECTORY_GLOBS,
    TEXT_FILE_NAMES,
    TEXT_FILE_SUFFIXES,
    BootstrapAnswers,
    BootstrapResult,
    PlannedChange,
    bootstrap_template,
)
from graphix_lab.infrastructure.text_files import iter_text_files


def _template_project_title() -> str:
    return " ".join(("Project", "Title", "Pending"))


def _template_distribution_name() -> str:
    return "-".join(("project", "name"))


def _template_package_name() -> str:
    return "_".join(("project", "name"))


def _template_author_name() -> str:
    return " ".join(("Alejandro", "Mata", "Ali"))


def _template_initial_version() -> str:
    return ".".join(("0", "0", "0"))


def _template_project_scope() -> str:
    return "_".join(("PROJECT", "SCOPE", "PENDING"))


def _template_license_id() -> str:
    return "".join(("M", "I", "T"))


def _bootstrap_required_assignment(value: bool) -> str:
    bool_value = "true" if value else "false"
    return f"bootstrap_required = {bool_value}"


def _bootstrap_required_metadata_value(value: bool) -> str:
    bool_value = "True" if value else "False"
    return f"bootstrap_required={bool_value}"


def _restore_template_metadata_scope_summary(content: str) -> str:
    pattern = re.compile(r"(?ms)^(?P<indent>\s*)scope_summary=.*?^(?P=indent)cli_commands=")

    def replace(match: re.Match[str]) -> str:
        indent = match.group("indent")
        return f'{indent}scope_summary="{_template_project_scope()}",\n{indent}cli_commands='

    return pattern.sub(replace, content, count=1)


def _copy_template_workspace(source_root: Path, workspace: Path) -> None:
    bootstrap_ignored_patterns = (*SKIP_DIRECTORIES, *SKIP_DIRECTORY_GLOBS)
    shutil.copytree(
        source_root,
        workspace,
        ignore=shutil.ignore_patterns(*bootstrap_ignored_patterns),
    )
    _restore_public_template_state(workspace)


def _load_vibe_template_data(workspace: Path) -> dict[str, object]:
    pyproject_path = workspace / "pyproject.toml"
    pyproject_data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    return pyproject_data["tool"]["vibe_template"]


def _restore_public_template_state(workspace: Path) -> None:
    current_state = _load_vibe_template_data(workspace)
    text_replacements = [
        (str(current_state["project_title"]), _template_project_title()),
        (str(current_state["distribution_name"]), _template_distribution_name()),
        (str(current_state["package_name"]), _template_package_name()),
        (str(current_state["initial_version"]), _template_initial_version()),
        (str(current_state["project_scope"]), _template_project_scope()),
        (_bootstrap_required_assignment(value=False), _bootstrap_required_assignment(value=True)),
        (
            _bootstrap_required_metadata_value(value=False),
            _bootstrap_required_metadata_value(value=True),
        ),
    ]
    for path in iter_text_files(
        workspace_root=workspace,
        suffixes=TEXT_FILE_SUFFIXES,
        file_names=TEXT_FILE_NAMES,
        skip_directories=SKIP_DIRECTORIES,
        skip_directory_globs=SKIP_DIRECTORY_GLOBS,
    ):
        if path.name == "THIRD_PARTY_LICENSES":
            continue
        original_content = path.read_text(encoding="utf-8")
        updated_content = original_content
        for old_value, new_value in text_replacements:
            updated_content = updated_content.replace(old_value, new_value)
        if path.as_posix().endswith("domain/template_metadata.py"):
            updated_content = _restore_template_metadata_scope_summary(updated_content)
        if path.name == "pyproject.toml":
            updated_content = updated_content.replace(
                f'license = {{ text = "{current_state["license_id"]}" }}',
                f'license = {{ text = "{_template_license_id()}" }}',
            )
            updated_content = updated_content.replace(
                f'authors = [{{ name = "{current_state["author_name"]}" }}]',
                f'authors = [{{ name = "{_template_author_name()}" }}]',
            )
            updated_content = updated_content.replace(
                f'author_name = "{current_state["author_name"]}"',
                f'author_name = "{_template_author_name()}"',
            )
            updated_content = updated_content.replace(
                f'license_id = "{current_state["license_id"]}"',
                f'license_id = "{_template_license_id()}"',
            )
        if path.as_posix().endswith("docs/docs_for_ai/status.md"):
            updated_content = updated_content.replace(
                f"- License: {current_state['license_id']}",
                f"- License: {_template_license_id()}",
            )
        if updated_content != original_content:
            path.write_text(updated_content, encoding="utf-8")

    current_package_name = str(current_state["package_name"])
    current_package_path = workspace / "src" / current_package_name
    template_package_path = workspace / "src" / _template_package_name()
    if (
        current_package_name != _template_package_name()
        and current_package_path.exists()
        and not template_package_path.exists()
    ):
        current_package_path.rename(template_package_path)

    (workspace / "LICENSE").write_text(
        (
            "MIT License\n\n"
            "Copyright (c) 2026 Alejandro Mata Ali\n\n"
            "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
            'of this software and associated documentation files (the "Software"), to deal\n'
            "in the Software without restriction, including without limitation the rights\n"
            "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
            "copies of the Software, and to permit persons to whom the Software is\n"
            "furnished to do so, subject to the following conditions:\n\n"
            "The above copyright notice and this permission notice shall be included in all\n"
            "copies or substantial portions of the Software.\n\n"
            'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n'
            "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
            "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
            "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
            "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
            "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
            "SOFTWARE.\n"
        ),
        encoding="utf-8",
    )


def _write_bootstrap_required_pyproject(workspace: Path, bootstrap_required: bool) -> None:
    bootstrap_required_value = str(bootstrap_required).lower()
    (workspace / "pyproject.toml").write_text(
        (f"[tool.vibe_template]\nbootstrap_required = {bootstrap_required_value}\n"),
        encoding="utf-8",
    )


def test_bootstrap_template_updates_metadata_and_package_name(temp_dir: Path) -> None:
    source_root = Path(__file__).resolve().parents[2]
    workspace = temp_dir / "workspace"
    _copy_template_workspace(source_root, workspace)

    answers = BootstrapAnswers(
        project_title="Sample Project",
        distribution_name="sample-project",
        package_name="sample_project",
        author_name="Ada Lovelace",
        initial_version="0.1.0",
        project_scope="Tooling library for reliable experiments.",
        license_id="MIT",
    )

    result = bootstrap_template(workspace_root=workspace, answers=answers, dry_run=False)

    assert result.changed is True
    assert (workspace / "src" / "sample_project").is_dir()
    assert not (workspace / "src" / _template_package_name()).exists()

    pyproject_content = (workspace / "pyproject.toml").read_text(encoding="utf-8")
    readme_content = (workspace / "README.md").read_text(encoding="utf-8")
    status_content = (workspace / "docs" / "docs_for_ai" / "status.md").read_text(encoding="utf-8")
    template_metadata_path = (
        workspace / "src" / "sample_project" / "domain" / "template_metadata.py"
    )
    template_metadata_content = template_metadata_path.read_text(encoding="utf-8")

    assert "sample-project" in pyproject_content
    assert "Ada Lovelace" in pyproject_content
    assert "0.1.0" in pyproject_content
    assert "Tooling library for reliable experiments." in readme_content
    assert "License: MIT" in status_content
    assert "example.invalid" not in pyproject_content
    assert "Pending" not in readme_content
    assert "bootstrap_required=False" in template_metadata_content


def test_bootstrap_template_dry_run_leaves_files_unchanged(temp_dir: Path) -> None:
    source_root = Path(__file__).resolve().parents[2]
    workspace = temp_dir / "workspace"
    _copy_template_workspace(source_root, workspace)

    answers = BootstrapAnswers(
        project_title="Dry Run Project",
        distribution_name="dry-run-project",
        package_name="dry_run_project",
        author_name="Grace Hopper",
        initial_version="0.2.0",
        project_scope="Dry run validation for template bootstrap.",
        license_id="Apache-2.0",
    )

    original_pyproject = (workspace / "pyproject.toml").read_text(encoding="utf-8")

    result = bootstrap_template(workspace_root=workspace, answers=answers, dry_run=True)

    assert result.changed is False
    assert (workspace / "src" / _template_package_name()).exists()
    assert (workspace / "pyproject.toml").read_text(encoding="utf-8") == original_pyproject
    assert any("pyproject.toml" in change.path.as_posix() for change in result.changes)


def test_bootstrap_template_rejects_already_bootstrapped_workspace(temp_dir: Path) -> None:
    source_root = Path(__file__).resolve().parents[2]
    workspace = temp_dir / "workspace"
    _copy_template_workspace(source_root, workspace)
    answers = BootstrapAnswers(
        project_title="Stable Project",
        distribution_name="stable-project",
        package_name="stable_project",
        author_name="Margaret Hamilton",
        initial_version="0.4.0",
        project_scope="Reusable template hardening validation.",
        license_id="MIT",
    )

    bootstrap_template(workspace_root=workspace, answers=answers, dry_run=False)

    with pytest.raises(ValueError, match="already been bootstrapped"):
        bootstrap_template(workspace_root=workspace, answers=answers, dry_run=True)


def test_bootstrap_template_keeps_third_party_license_inventory_stable_for_public_mit_template(
    temp_dir: Path,
) -> None:
    source_root = Path(__file__).resolve().parents[2]
    workspace = temp_dir / "workspace"
    _copy_template_workspace(source_root, workspace)
    original_third_party_licenses = (workspace / "THIRD_PARTY_LICENSES").read_text(encoding="utf-8")

    answers = BootstrapAnswers(
        project_title="Apache Project",
        distribution_name="apache-project",
        package_name="apache_project",
        author_name="Grace Hopper",
        initial_version="0.5.0",
        project_scope="Template publication regression coverage.",
        license_id="Apache-2.0",
    )

    bootstrap_template(workspace_root=workspace, answers=answers, dry_run=False)

    pyproject_content = (workspace / "pyproject.toml").read_text(encoding="utf-8")
    status_content = (workspace / "docs" / "docs_for_ai" / "status.md").read_text(encoding="utf-8")
    license_content = (workspace / "LICENSE").read_text(encoding="utf-8")
    updated_third_party_licenses = (workspace / "THIRD_PARTY_LICENSES").read_text(encoding="utf-8")

    assert 'license = { text = "Apache-2.0" }' in pyproject_content
    assert 'authors = [{ name = "Grace Hopper" }]' in pyproject_content
    assert "License: Apache-2.0" in status_content
    assert license_content.startswith("Apache License")
    assert updated_third_party_licenses == original_third_party_licenses


def test_bootstrap_template_wraps_long_scope_summary_in_generated_metadata(
    temp_dir: Path,
) -> None:
    source_root = Path(__file__).resolve().parents[2]
    workspace = temp_dir / "workspace"
    _copy_template_workspace(source_root, workspace)
    long_scope = (
        "This bootstrap scope is intentionally long so the generated template metadata keeps "
        "a readable Python layout while still preserving the exact project description text."
    )

    answers = BootstrapAnswers(
        project_title="Wrapped Scope Project",
        distribution_name="wrapped-scope-project",
        package_name="wrapped_scope_project",
        author_name="Lynn Conway",
        initial_version="0.6.0",
        project_scope=long_scope,
        license_id="MIT",
    )

    bootstrap_template(workspace_root=workspace, answers=answers, dry_run=False)

    template_metadata_content = (
        workspace / "src" / "wrapped_scope_project" / "domain" / "template_metadata.py"
    ).read_text(encoding="utf-8")

    assert "scope_summary=(" in template_metadata_content
    assert max(len(line) for line in template_metadata_content.splitlines()) <= 100


def test_bootstrap_cli_reinstalls_for_the_new_package_name(
    temp_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    workspace = temp_dir / "workspace"
    workspace.mkdir()
    _write_bootstrap_required_pyproject(workspace, True)
    planned_change = PlannedChange(
        path=workspace / "src" / "bootstrap_cli_project",
        description="Rename package directory from graphix_lab to bootstrap_cli_project",
    )

    def fake_bootstrap_template(
        workspace_root: Path,
        answers: BootstrapAnswers,
        dry_run: bool,
    ) -> BootstrapResult:
        del workspace_root, answers, dry_run
        return BootstrapResult(changed=True, changes=(planned_change,))

    def fake_subprocess_run(
        command: list[str],
        check: bool,
        cwd: Path,
    ) -> CompletedProcess[bytes]:
        assert check is False
        assert cwd == workspace
        return CompletedProcess(args=command, returncode=0)

    monkeypatch.chdir(workspace)
    monkeypatch.setattr(
        cli_module,
        "bootstrap_template",
        fake_bootstrap_template,
    )
    monkeypatch.setattr(cli_module.subprocess, "run", fake_subprocess_run)

    def unexpected_prompt(label: str, default: str | None = None) -> str:
        pytest.fail(f"Unexpected prompt for {label} with {default}")

    monkeypatch.setattr(cli_module, "_prompt", unexpected_prompt)

    args = argparse.Namespace(
        project_title="Bootstrap CLI Project",
        distribution_name="bootstrap-cli-project",
        package_name=None,
        author_name="Katherine Johnson",
        initial_version="0.3.0",
        project_scope="End-to-end bootstrap verification for the template.",
        license_id="MIT",
        dry_run=False,
    )

    return_code = cli_module._handle_bootstrap(args)
    stdout = capsys.readouterr().out

    assert return_code == 0
    assert "bootstrap_cli_project" in stdout
    assert "pip install -e .[dev]" in stdout


def test_bootstrap_cli_fails_without_prompting_when_template_is_already_bootstrapped(
    temp_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    workspace = temp_dir / "workspace"
    workspace.mkdir()
    _write_bootstrap_required_pyproject(workspace, False)

    def unexpected_prompt(label: str, default: str | None = None) -> str:
        pytest.fail(f"Unexpected prompt for {label} with {default}")

    monkeypatch.chdir(workspace)
    monkeypatch.setattr(cli_module, "_prompt", unexpected_prompt)

    args = argparse.Namespace(
        project_title=None,
        distribution_name=None,
        package_name=None,
        author_name=None,
        initial_version=None,
        project_scope=None,
        license_id=None,
        dry_run=True,
    )

    return_code = cli_module._handle_bootstrap(args)
    stdout = capsys.readouterr().out

    assert return_code == 1
    assert "already been bootstrapped" in stdout
