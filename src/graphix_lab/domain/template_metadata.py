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
        package_name="graphix_lab",
        distribution_name="graphix-lab",
        project_title="Graphix Lab",
        bootstrap_required=False,
        scope_summary=(
            "A small, educational usability layer over Graphix for measurement-based quantum "
            "computing experiments. The project wraps Graphix patterns and circuits with "
            "clearer summaries, command introspection, simulation reports, "
            "Matplotlib/NetworkX visualizations, step traces, and optional Qiskit import "
            "helpers without reimplementing Graphix core backends."
        ),
        cli_commands=("bootstrap", "quality", "test", "clean", "licenses"),
    )
