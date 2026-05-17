from __future__ import annotations

from pathlib import Path


def test_dependabot_config_tracks_python_and_github_actions() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    dependabot_content = (repo_root / ".github" / "dependabot.yml").read_text(encoding="utf-8")

    assert 'package-ecosystem: "pip"' in dependabot_content
    assert 'package-ecosystem: "github-actions"' in dependabot_content
    assert 'directory: "/"' in dependabot_content
    assert 'timezone: "Europe/Madrid"' in dependabot_content


def test_dependabot_config_groups_python_runtime_and_development_updates() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    dependabot_content = (repo_root / ".github" / "dependabot.yml").read_text(encoding="utf-8")

    assert "runtime-dependencies:" in dependabot_content
    assert 'dependency-type: "production"' in dependabot_content
    assert "development-dependencies:" in dependabot_content
    assert 'dependency-type: "development"' in dependabot_content
