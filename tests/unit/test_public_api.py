from __future__ import annotations

import tomllib
from pathlib import Path

from project_name import TemplateMetadata, get_template_metadata
from project_name import __name__ as package_module_name


def test_public_api_exposes_template_metadata() -> None:
    metadata = get_template_metadata()
    repo_root = Path(__file__).resolve().parents[2]
    pyproject_data = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))
    vibe_template_data = pyproject_data["tool"]["vibe_template"]
    project_data = pyproject_data["project"]

    assert isinstance(metadata, TemplateMetadata)
    assert metadata.package_name == package_module_name
    assert metadata.package_name == str(vibe_template_data["package_name"])
    assert metadata.distribution_name == str(project_data["name"])
    assert metadata.project_title == str(vibe_template_data["project_title"])
    assert metadata.bootstrap_required is bool(vibe_template_data["bootstrap_required"])
    assert metadata.scope_summary == str(vibe_template_data["project_scope"])
    assert metadata.cli_commands == ("bootstrap", "quality", "test", "clean", "licenses")
