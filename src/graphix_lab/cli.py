from __future__ import annotations

import argparse
import os
import shlex
import subprocess
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
    build_security_audit_command,
    build_test_command,
    load_distribution_name,
    run_commands,
)

# Keep the host path implementation stable even if tests monkeypatch os.name.
_RUNTIME_PATH_CLS = type(Path())


def main(argv: str | Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(_normalize_argv(argv))

    if args.command == "bootstrap":
        return _handle_bootstrap(args)
    if args.command == "quality":
        return _handle_quality(args)
    if args.command == "test":
        return _handle_test(args)
    if args.command == "security":
        return _handle_security(args)
    if args.command == "clean":
        return _handle_clean(args)
    if args.command == "licenses":
        return _handle_licenses(args)
    parser.print_help()
    return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Graphix Lab CLI for quality checks, cleanup, licensing, and template bootstrap."
        )
    )
    subparsers = parser.add_subparsers(dest="command")

    bootstrap_parser = subparsers.add_parser(
        "bootstrap",
        help="Configure a fresh template copy and rename the package.",
    )
    bootstrap_parser.add_argument("--project-title")
    bootstrap_parser.add_argument("--distribution-name")
    bootstrap_parser.add_argument("--package-name")
    bootstrap_parser.add_argument("--author-name")
    bootstrap_parser.add_argument("--initial-version")
    bootstrap_parser.add_argument("--project-scope")
    bootstrap_parser.add_argument("--license-id", choices=SUPPORTED_LICENSE_IDS)
    bootstrap_parser.add_argument("--dry-run", action="store_true")

    quality_parser = subparsers.add_parser(
        "quality",
        help="Run Ruff, package import and CLI smoke checks, pytest, and pyright.",
    )
    quality_parser.add_argument("--check-only", action="store_true")

    subparsers.add_parser("test", help="Run pytest.")
    subparsers.add_parser(
        "security",
        help="Run a dependency vulnerability audit with pip-audit.",
    )

    clean_parser = subparsers.add_parser(
        "clean",
        help="Remove caches and temporary artifacts without touching .venv.",
    )
    clean_parser.add_argument("--dry-run", action="store_true")

    licenses_parser = subparsers.add_parser(
        "licenses",
        help="Regenerate THIRD_PARTY_LICENSES from the active interpreter.",
    )
    licenses_parser.add_argument("--output", default="THIRD_PARTY_LICENSES")
    return parser


def _normalize_argv(argv: str | Sequence[str] | None) -> list[str] | None:
    if argv is None:
        return None
    if isinstance(argv, str):
        return _split_command_string(argv)
    return list(argv)


def _uses_windows_argument_splitting() -> bool:
    return os.name == "nt"


def _split_command_string(command_line: str) -> list[str]:
    if _uses_windows_argument_splitting():
        return [_strip_wrapping_quotes(token) for token in shlex.split(command_line, posix=False)]
    return shlex.split(command_line, posix=True)


def _strip_wrapping_quotes(token: str) -> str:
    if len(token) >= 2 and token[0] == token[-1] and token[0] in {'"', "'"}:
        return token[1:-1]
    return token


def _current_working_directory() -> Path:
    return _RUNTIME_PATH_CLS.cwd()


def _path_from_cli_value(path_value: str) -> Path:
    return _RUNTIME_PATH_CLS(path_value)


def _handle_bootstrap(args: argparse.Namespace) -> int:
    project_root = _current_working_directory()
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
    print(f"- {' '.join(resync_command)}")
    completed_process = subprocess.run(resync_command, check=False, cwd=project_root)  # noqa: S603
    if completed_process.returncode != 0:
        print("Automatic resync failed. Run this command manually:")
        print(f"- {' '.join(resync_command)}")
        return completed_process.returncode or 1
    print("Editable install resynced successfully.")
    return 0


def _handle_quality(args: argparse.Namespace) -> int:
    project_root = _current_working_directory()
    commands = build_quality_commands(
        project_root=project_root,
        include_format_fix=not args.check_only,
    )
    results = run_commands(commands, root=project_root)
    for result in results:
        print(f"{' '.join(result.command)} -> {result.returncode}")
        if result.returncode != 0:
            return result.returncode
    return 0


def _handle_test(args: argparse.Namespace) -> int:
    del args
    completed_process = subprocess.run(  # noqa: S603
        build_test_command(),
        check=False,
        cwd=_current_working_directory(),
    )
    return completed_process.returncode


def _handle_security(args: argparse.Namespace) -> int:
    del args
    completed_process = subprocess.run(  # noqa: S603
        build_security_audit_command(),
        check=False,
        cwd=_current_working_directory(),
    )
    return completed_process.returncode


def _handle_clean(args: argparse.Namespace) -> int:
    current_working_directory = _current_working_directory()
    result = run_clean(root=current_working_directory, dry_run=args.dry_run)
    action_text = "Would remove" if args.dry_run else "Removed"
    print(f"{action_text} {len(result.planned_paths)} path(s).")
    for path in result.planned_paths:
        print(f"- {path.relative_to(current_working_directory)}")
    if result.failed_paths:
        print("Failed to remove:")
        for path in result.failed_paths:
            print(f"- {path.relative_to(current_working_directory)}")
        return 1
    return 0


def _handle_licenses(args: argparse.Namespace) -> int:
    project_root = _current_working_directory()
    distribution_name = load_distribution_name(project_root)
    completed_process = subprocess.run(  # noqa: S603
        build_license_command(
            output_file=_path_from_cli_value(args.output),
            project_root=project_root,
            distribution_name=distribution_name,
        ),
        check=False,
        cwd=project_root,
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


if __name__ == "__main__":
    raise SystemExit(main())
