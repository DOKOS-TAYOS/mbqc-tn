from __future__ import annotations

from pathlib import Path


def test_ci_workflow_does_not_run_template_bootstrap_smoke_for_bootstrapped_library() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    workflow_content = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "template-smoke:" not in workflow_content
    assert "python scripts/bootstrap_smoke.py" not in workflow_content


def test_ci_workflow_uses_read_only_repository_permissions() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    workflow_content = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "\npermissions:\n  contents: read\n" in workflow_content


def test_ci_workflow_uses_current_first_party_action_versions() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    workflow_content = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "actions/checkout@v7" in workflow_content
    assert "actions/setup-python@v6" in workflow_content
    assert "actions/checkout@v6" not in workflow_content
    assert "actions/setup-python@v5" not in workflow_content


def test_ci_workflow_runs_editable_install_and_release_smoke_checks() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    workflow_content = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "pip install -e .[dev]" in workflow_content
    assert "import graphix_lab; print(graphix_lab.__all__)" in workflow_content
    assert "graphix_lab.cli --help" in workflow_content


def test_ci_workflow_keeps_optional_qiskit_checks_in_an_isolated_job() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    workflow_content = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "qiskit-optional:" in workflow_content
    assert "pip install -e .[qiskit,dev]" in workflow_content
    assert "tests/unit/test_qiskit_adapter.py" in workflow_content
    assert "-k qiskit" in workflow_content


def test_ci_workflow_runs_dependency_vulnerability_audit() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    workflow_content = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "dependency-audit:" in workflow_content
    assert "python -m graphix_lab.cli security" in workflow_content


def test_repository_no_longer_ships_template_bootstrap_smoke_helper() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    assert not (repo_root / "scripts" / "bootstrap_smoke.py").exists()
