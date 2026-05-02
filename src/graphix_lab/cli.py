from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from .app.bootstrap_service import (
    BOOTSTRAP_ALREADY_COMPLETED_MESSAGE,
    SUPPORTED_LICENSE_IDS,
    BootstrapAnswers,
    bootstrap_required_for_workspace,
    bootstrap_template,
    derive_package_name,
)
from .app.clean_service import run_clean
from .app.tooling_service import (
    build_bootstrap_resync_command,
    build_license_command,
    build_quality_commands,
    build_test_command,
    load_distribution_name,
    run_commands,
)
from .infrastructure.process_runner import run_process


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.command == "bootstrap":
        return _handle_bootstrap(args)
    if args.command == "quality":
        return _handle_quality(args)
    if args.command == "test":
        return _handle_test(args)
    if args.command == "clean":
        return _handle_clean(args)
    if args.command == "licenses":
        return _handle_licenses(args)
    parser.print_help()
    return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Project template CLI for Python vibe coding projects."
    )
    subparsers = parser.add_subparsers(dest="command")

    bootstrap_parser = subparsers.add_parser(
        "bootstrap",
        help="Configure template metadata and rename the package.",
    )
    bootstrap_parser.add_argument("--project-title")
    bootstrap_parser.add_argument("--distribution-name")
    bootstrap_parser.add_argument("--package-name")
    bootstrap_parser.add_argument("--author-name")
    bootstrap_parser.add_argument("--initial-version")
    bootstrap_parser.add_argument("--project-scope")
    bootstrap_parser.add_argument("--license-id", choices=SUPPORTED_LICENSE_IDS)
    bootstrap_parser.add_argument("--dry-run", action="store_true")

    quality_parser = subparsers.add_parser("quality", help="Run Ruff, pytest, and pyright.")
    quality_parser.add_argument("--check-only", action="store_true")

    subparsers.add_parser("test", help="Run pytest.")

    clean_parser = subparsers.add_parser(
        "clean",
        help="Remove caches and temporary artifacts without touching .venv.",
    )
    clean_parser.add_argument("--dry-run", action="store_true")

    licenses_parser = subparsers.add_parser(
        "licenses",
        help="Regenerate THIRD_PARTY_LICENSES with pip-licenses.",
    )
    licenses_parser.add_argument("--output", default="THIRD_PARTY_LICENSES")
    return parser


def _handle_bootstrap(args: argparse.Namespace) -> int:
    project_root = Path.cwd()
    if not bootstrap_required_for_workspace(project_root):
        print(BOOTSTRAP_ALREADY_COMPLETED_MESSAGE)
        return 1
    distribution_name = args.distribution_name or _prompt("Distribution name", "graphix-lab")
    if args.package_name:
        package_name = args.package_name
    elif args.distribution_name:
        package_name = derive_package_name(distribution_name)
    else:
        package_name = _prompt(
            "Package name",
            derive_package_name(distribution_name),
        )
    answers = BootstrapAnswers(
        project_title=args.project_title or _prompt("Project title", "Graphix Lab"),
        distribution_name=distribution_name,
        package_name=package_name,
        author_name=args.author_name or _prompt("Author name"),
        initial_version=args.initial_version or _prompt("Initial version", "0.1.0"),
        project_scope=args.project_scope or _prompt("Project scope"),
        license_id=args.license_id or _prompt("License ID", "MIT"),
    )
    result = bootstrap_template(workspace_root=project_root, answers=answers, dry_run=args.dry_run)
    action_text = "Planned" if args.dry_run else "Applied"
    print(f"{action_text} {len(result.changes)} bootstrap changes.")
    for change in result.changes:
        print(f"- {change.path.relative_to(project_root)}: {change.description}")
    if args.dry_run:
        return 0

    resync_command = build_bootstrap_resync_command()
    print("Resyncing editable install:")
    print(f"- {_format_command(resync_command)}")
    completed_process = run_process(resync_command, root=project_root)
    if completed_process.returncode != 0:
        print("Automatic resync failed. Run this command manually:")
        print(f"- {_format_command(resync_command)}")
        return completed_process.returncode or 1
    print("Editable install resynced successfully.")
    return 0


def _handle_quality(args: argparse.Namespace) -> int:
    commands = build_quality_commands(include_format_fix=not args.check_only)
    results = run_commands(commands, root=Path.cwd())
    for result in results:
        print(f"{' '.join(result.command)} -> {result.returncode}")
        if result.returncode != 0:
            return result.returncode
    return 0


def _handle_test(args: argparse.Namespace) -> int:
    del args
    completed_process = run_process(build_test_command(), root=Path.cwd())
    return completed_process.returncode


def _handle_clean(args: argparse.Namespace) -> int:
    result = run_clean(root=Path.cwd(), dry_run=args.dry_run)
    action_text = "Would remove" if args.dry_run else "Removed"
    print(f"{action_text} {len(result.planned_paths)} path(s).")
    for path in result.planned_paths:
        print(f"- {path.relative_to(Path.cwd())}")
    if result.failed_paths:
        print("Failed to remove:")
        for path in result.failed_paths:
            print(f"- {path.relative_to(Path.cwd())}")
        return 1
    return 0


def _handle_licenses(args: argparse.Namespace) -> int:
    project_root = Path.cwd()
    distribution_name = load_distribution_name(project_root)
    completed_process = run_process(
        build_license_command(Path(args.output), distribution_name),
        root=project_root,
    )
    return completed_process.returncode


def _prompt(label: str, default: str | None = None) -> str:
    prompt_text = f"{label}"
    if default:
        prompt_text = f"{prompt_text} [{default}]"
    prompt_text = f"{prompt_text}: "
    value = input(prompt_text).strip()
    if value:
        return value
    if default is not None:
        return default
    raise ValueError(f"{label} is required.")


def _format_command(command: Sequence[str]) -> str:
    return " ".join(command)


if __name__ == "__main__":
    raise SystemExit(main())
