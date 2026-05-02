from __future__ import annotations

from pathlib import Path


def test_temp_dir_uses_a_system_temporary_location(temp_dir: Path) -> None:
    repo_root = Path(__file__).resolve().parents[2]

    assert not temp_dir.is_relative_to(repo_root)
