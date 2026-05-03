from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pytest

import graphix_lab.infrastructure.temporary_workspaces as temporary_workspaces
from graphix_lab.infrastructure.temporary_workspaces import create_temporary_workspace


def _repo_local_workspace(name: str) -> Path:
    repo_root = Path(__file__).resolve().parents[2]
    workspace_root = repo_root / "test-artifacts" / f"{name}-{uuid4().hex}"
    workspace_root.mkdir(parents=True)
    return workspace_root


def test_create_temporary_workspace_prefers_the_system_root_when_it_is_usable() -> None:
    workspace_root = _repo_local_workspace("test-harness-system-root")
    system_root = workspace_root / "system"
    fallback_root = workspace_root / "fallback"

    temporary_workspace = create_temporary_workspace(
        prefix="graphix-lab-tests-",
        system_root=system_root,
        fallback_root=fallback_root,
    )
    try:
        assert temporary_workspace.path.is_dir()
        assert temporary_workspace.path.is_relative_to(system_root)
        assert temporary_workspace.selected_root == system_root
        assert temporary_workspace.used_fallback_root is False
    finally:
        temporary_workspace.cleanup(ignore_errors=True)


def test_create_temporary_workspace_falls_back_when_the_system_root_is_not_usable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace_root = _repo_local_workspace("test-harness-fallback-root")
    system_root = workspace_root / "system"
    fallback_root = workspace_root / "fallback"
    original_probe = temporary_workspaces._probe_temp_root

    def fake_probe_temp_root(root: Path) -> None:
        if root == system_root:
            raise PermissionError(f"blocked: {root}")
        original_probe(root)

    monkeypatch.setattr(temporary_workspaces, "_probe_temp_root", fake_probe_temp_root)

    temporary_workspace = create_temporary_workspace(
        prefix="graphix-lab-tests-",
        system_root=system_root,
        fallback_root=fallback_root,
    )
    try:
        assert temporary_workspace.path.is_dir()
        assert temporary_workspace.path.is_relative_to(fallback_root)
        assert temporary_workspace.selected_root == fallback_root
        assert temporary_workspace.used_fallback_root is True
    finally:
        temporary_workspace.cleanup(ignore_errors=True)


def test_temp_dir_is_a_usable_workspace_path(temp_dir: Path) -> None:
    probe_file = temp_dir / "probe.txt"

    probe_file.write_text("probe", encoding="utf-8")

    assert temp_dir.is_dir()
    assert probe_file.read_text(encoding="utf-8") == "probe"
