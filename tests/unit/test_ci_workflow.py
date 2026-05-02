from __future__ import annotations

from pathlib import Path


def test_ci_workflow_does_not_run_template_bootstrap_smoke_for_bootstrapped_library() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    workflow_content = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "template-smoke:" not in workflow_content
    assert "python scripts/bootstrap_smoke.py" not in workflow_content


def test_repository_no_longer_ships_template_bootstrap_smoke_helper() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    assert not (repo_root / "scripts" / "bootstrap_smoke.py").exists()
