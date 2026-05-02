from __future__ import annotations

from pathlib import Path


def test_ci_workflow_runs_fresh_template_smoke_job() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    workflow_content = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "template-smoke:" in workflow_content
    assert "os: [ubuntu-latest, windows-latest]" in workflow_content
    assert 'python-version: ["3.12"]' in workflow_content
    assert "python scripts/bootstrap_smoke.py" in workflow_content
