from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class TemporaryWorkspace:
    path: Path
    selected_root: Path
    used_fallback_root: bool

    def cleanup(self, *, ignore_errors: bool = False) -> None:
        if not self.path.exists():
            return
        shutil.rmtree(self.path, ignore_errors=ignore_errors)


def create_temporary_workspace(
    *,
    prefix: str,
    fallback_root: Path,
    system_root: Path | None = None,
) -> TemporaryWorkspace:
    resolved_system_root = system_root or Path(tempfile.gettempdir())
    candidate_roots = _candidate_roots(
        system_root=resolved_system_root,
        fallback_root=fallback_root,
    )
    last_error: OSError | None = None

    for candidate_root, used_fallback_root in candidate_roots:
        try:
            _probe_temp_root(candidate_root)
            workspace_path = _make_temp_directory(root=candidate_root, prefix=prefix)
        except OSError as error:
            last_error = error
            continue

        return TemporaryWorkspace(
            path=workspace_path,
            selected_root=candidate_root,
            used_fallback_root=used_fallback_root,
        )

    raise OSError(
        "Could not create a usable temporary workspace in either the system temp root or the "
        "configured fallback root."
    ) from last_error


def _candidate_roots(
    *,
    system_root: Path,
    fallback_root: Path,
) -> tuple[tuple[Path, bool], ...]:
    normalized_candidates: list[tuple[Path, bool]] = []

    for root, used_fallback_root in (
        (system_root.resolve(), False),
        (fallback_root.resolve(), True),
    ):
        if any(existing_root == root for existing_root, _ in normalized_candidates):
            continue
        normalized_candidates.append((root, used_fallback_root))

    return tuple(normalized_candidates)


def _probe_temp_root(root: Path) -> None:
    probe_directory = _make_temp_directory(root=root, prefix="graphix-lab-probe-")
    try:
        probe_file = probe_directory / "probe.txt"
        probe_file.write_text("probe", encoding="utf-8")
        probe_file.unlink()
    finally:
        shutil.rmtree(probe_directory, ignore_errors=False)


def _make_temp_directory(*, root: Path, prefix: str) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    for _ in range(16):
        candidate = root / f"{prefix}{uuid4().hex}"
        try:
            candidate.mkdir()
        except FileExistsError:
            continue
        return candidate

    raise FileExistsError(f"Could not create a unique temporary directory under {root}.")
