from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TemplateMetadata:
    package_name: str
    distribution_name: str
    project_title: str
    bootstrap_required: bool
    scope_summary: str
    cli_commands: tuple[str, ...]


def get_template_metadata() -> TemplateMetadata:
    return TemplateMetadata(
        package_name="project_name",
        distribution_name="project-name",
        project_title="Project Title Pending",
        bootstrap_required=True,
        scope_summary="PROJECT_SCOPE_PENDING",
        cli_commands=("bootstrap", "quality", "test", "clean", "licenses"),
    )
