from __future__ import annotations

import json
import keyword
import re
import tomllib
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ..infrastructure.text_files import iter_text_files

SUPPORTED_LICENSE_IDS: tuple[str, ...] = (
    "MIT",
    "Apache-2.0",
    "BSD-3-Clause",
    "MPL-2.0",
    "Proprietary",
)
BOOTSTRAP_ALREADY_COMPLETED_MESSAGE = (
    "This project has already been bootstrapped. Create a fresh copy of the template "
    "to run bootstrap again."
)
TEXT_FILE_SUFFIXES: tuple[str, ...] = (
    ".py",
    ".toml",
    ".md",
    ".yml",
    ".yaml",
    ".cff",
    ".txt",
    ".sh",
    ".cmd",
)
TEXT_FILE_NAMES: tuple[str, ...] = (
    ".gitignore",
    ".editorconfig",
    ".gitattributes",
    "LICENSE",
    "THIRD_PARTY_LICENSES",
    "CONTRIBUTING",
    "CONTRIBUTING.md",
)
SKIP_DIRECTORIES: tuple[str, ...] = (
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
)


@dataclass(frozen=True, slots=True)
class BootstrapAnswers:
    project_title: str
    distribution_name: str
    package_name: str
    author_name: str
    initial_version: str
    project_scope: str
    license_id: str


@dataclass(frozen=True, slots=True)
class PlannedChange:
    path: Path
    description: str


@dataclass(frozen=True, slots=True)
class BootstrapResult:
    changed: bool
    changes: tuple[PlannedChange, ...]


@dataclass(frozen=True, slots=True)
class TemplateState:
    project_title: str
    distribution_name: str
    package_name: str
    author_name: str
    initial_version: str
    project_scope: str
    license_id: str
    bootstrap_required: bool


def bootstrap_required_for_workspace(workspace_root: Path) -> bool:
    vibe_template_data = _load_vibe_template_data(workspace_root)
    return bool(vibe_template_data.get("bootstrap_required", False))


def bootstrap_template(
    workspace_root: Path,
    answers: BootstrapAnswers,
    dry_run: bool = False,
) -> BootstrapResult:
    state = _load_template_state(workspace_root)
    if not state.bootstrap_required:
        raise ValueError(BOOTSTRAP_ALREADY_COMPLETED_MESSAGE)
    validated_answers = _validate_answers(answers)
    replacements = _build_replacements(state, validated_answers)
    changes = list(_collect_text_changes(workspace_root, replacements, state, validated_answers))
    changes.extend(
        _collect_package_rename_changes(
            workspace_root,
            state.package_name,
            validated_answers.package_name,
        )
    )
    changes.append(
        PlannedChange(
            path=workspace_root / "LICENSE",
            description=f"Write {validated_answers.license_id} license text",
        )
    )

    if dry_run:
        return BootstrapResult(changed=False, changes=tuple(changes))

    _apply_text_replacements(workspace_root, replacements, state, validated_answers)
    _rename_package_directory(
        workspace_root,
        state.package_name,
        validated_answers.package_name,
    )
    _write_license_file(
        workspace_root / "LICENSE",
        validated_answers.license_id,
        validated_answers.author_name,
    )
    return BootstrapResult(changed=bool(changes), changes=tuple(changes))


def derive_package_name(distribution_name: str) -> str:
    normalized = distribution_name.strip().replace("-", "_").replace(".", "_")
    normalized = re.sub(r"[^a-zA-Z0-9_]", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized.lower()


def _validate_answers(answers: BootstrapAnswers) -> BootstrapAnswers:
    if not answers.project_title.strip():
        raise ValueError("Project title is required.")
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", answers.distribution_name):
        raise ValueError(
            "Distribution name must use lowercase letters, numbers, dots, dashes, or underscores."
        )
    if not answers.package_name.isidentifier() or keyword.iskeyword(answers.package_name):
        raise ValueError("Package name must be a valid Python identifier.")
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][a-zA-Z0-9.]+)?", answers.initial_version):
        raise ValueError("Initial version must follow a simple semantic version like 0.1.0.")
    if not answers.author_name.strip():
        raise ValueError("Author name is required.")
    if not answers.project_scope.strip():
        raise ValueError("Project scope is required.")
    if answers.license_id not in SUPPORTED_LICENSE_IDS:
        supported = ", ".join(SUPPORTED_LICENSE_IDS)
        raise ValueError(
            f"Unsupported license '{answers.license_id}'. Supported values: {supported}."
        )
    return answers


def _load_template_state(workspace_root: Path) -> TemplateState:
    vibe_template_data = _load_vibe_template_data(workspace_root)
    return TemplateState(
        project_title=str(vibe_template_data["project_title"]),
        distribution_name=str(vibe_template_data["distribution_name"]),
        package_name=str(vibe_template_data["package_name"]),
        author_name=str(vibe_template_data["author_name"]),
        initial_version=str(vibe_template_data["initial_version"]),
        project_scope=str(vibe_template_data["project_scope"]),
        license_id=str(vibe_template_data["license_id"]),
        bootstrap_required=bool(vibe_template_data["bootstrap_required"]),
    )


def _load_vibe_template_data(workspace_root: Path) -> dict[str, Any]:
    pyproject_data = tomllib.loads((workspace_root / "pyproject.toml").read_text(encoding="utf-8"))
    return pyproject_data["tool"]["vibe_template"]


def _build_replacements(state: TemplateState, answers: BootstrapAnswers) -> list[tuple[str, str]]:
    return [
        (state.project_title, answers.project_title),
        (state.distribution_name, answers.distribution_name),
        (state.package_name, answers.package_name),
        (state.initial_version, answers.initial_version),
        (state.project_scope, answers.project_scope),
        (
            _bootstrap_required_assignment(value=True),
            _bootstrap_required_assignment(value=False),
        ),
        (
            _bootstrap_required_metadata_value(value=True),
            _bootstrap_required_metadata_value(value=False),
        ),
    ]


def _collect_text_changes(
    workspace_root: Path,
    replacements: list[tuple[str, str]],
    state: TemplateState,
    answers: BootstrapAnswers,
) -> list[PlannedChange]:
    changes: list[PlannedChange] = []
    for path in _iter_text_files(workspace_root):
        original_content = path.read_text(encoding="utf-8")
        updated_content = _updated_text_content(
            path, original_content, replacements, state, answers
        )
        if updated_content != original_content:
            changes.append(PlannedChange(path=path, description="Update template placeholders"))
    return changes


def _iter_text_files(workspace_root: Path) -> list[Path]:
    return iter_text_files(
        workspace_root=workspace_root,
        suffixes=TEXT_FILE_SUFFIXES,
        file_names=TEXT_FILE_NAMES,
        skip_directories=SKIP_DIRECTORIES,
    )


def _replace_text(content: str, replacements: list[tuple[str, str]]) -> str:
    updated_content = content
    for old_value, new_value in replacements:
        updated_content = updated_content.replace(old_value, new_value)
    return updated_content


def _bootstrap_required_assignment(value: bool) -> str:
    bool_value = "true" if value else "false"
    return f"bootstrap_required = {bool_value}"


def _bootstrap_required_metadata_value(value: bool) -> str:
    bool_value = "True" if value else "False"
    return f"bootstrap_required={bool_value}"


def _updated_text_content(
    path: Path,
    content: str,
    replacements: list[tuple[str, str]],
    state: TemplateState,
    answers: BootstrapAnswers,
) -> str:
    if path.name == "THIRD_PARTY_LICENSES":
        return content

    updated_content = _replace_text(content, replacements)
    if path.name == "pyproject.toml":
        updated_content = _replace_text(
            updated_content,
            [
                (
                    f'license = {{ text = "{state.license_id}" }}',
                    f'license = {{ text = "{answers.license_id}" }}',
                ),
                (
                    f'authors = [{{ name = "{state.author_name}" }}]',
                    f'authors = [{{ name = "{answers.author_name}" }}]',
                ),
                (
                    f'author_name = "{state.author_name}"',
                    f'author_name = "{answers.author_name}"',
                ),
                (
                    f'license_id = "{state.license_id}"',
                    f'license_id = "{answers.license_id}"',
                ),
            ],
        )
    if path.as_posix().endswith("domain/template_metadata.py"):
        updated_content = _replace_template_metadata_scope_summary(
            updated_content,
            answers.project_scope,
        )
    if path.as_posix().endswith("docs/docs_for_ai/status.md"):
        updated_content = _replace_text(
            updated_content,
            [(f"- License: {state.license_id}", f"- License: {answers.license_id}")],
        )
    return updated_content


def _apply_text_replacements(
    workspace_root: Path,
    replacements: list[tuple[str, str]],
    state: TemplateState,
    answers: BootstrapAnswers,
) -> None:
    for path in _iter_text_files(workspace_root):
        original_content = path.read_text(encoding="utf-8")
        updated_content = _updated_text_content(
            path, original_content, replacements, state, answers
        )
        if updated_content != original_content:
            path.write_text(updated_content, encoding="utf-8")


def _replace_template_metadata_scope_summary(content: str, scope_summary: str) -> str:
    pattern = re.compile(r"(?ms)^(?P<indent>\s*)scope_summary=.*?^(?P=indent)cli_commands=")

    def replace(match: re.Match[str]) -> str:
        indent = match.group("indent")
        formatted_scope_summary = _format_scope_summary_assignment(scope_summary, indent)
        return f"{formatted_scope_summary}\n{indent}cli_commands="

    return pattern.sub(replace, content, count=1)


def _format_scope_summary_assignment(scope_summary: str, indent: str) -> str:
    quoted_scope_summary = json.dumps(scope_summary)
    single_line_assignment = f"{indent}scope_summary={quoted_scope_summary},"
    if len(single_line_assignment) <= 100:
        return single_line_assignment

    continuation_indent = f"{indent}    "
    wrapped_scope_parts = _wrap_prose_text(
        scope_summary,
        max_width=100 - len(continuation_indent) - 2,
    )
    wrapped_scope_literal = "\n".join(
        f"{continuation_indent}{json.dumps(scope_part)}" for scope_part in wrapped_scope_parts
    )
    return f"{indent}scope_summary=(\n{wrapped_scope_literal}\n{indent}),"


def _wrap_prose_text(text: str, max_width: int) -> list[str]:
    words = text.split(" ")
    wrapped_lines: list[str] = []
    current_line = ""

    for word in words:
        candidate = word if not current_line else f"{current_line} {word}"
        if len(candidate) <= max_width or not current_line:
            current_line = candidate
            continue
        wrapped_lines.append(f"{current_line} ")
        current_line = word

    if current_line or not wrapped_lines:
        wrapped_lines.append(current_line)
    return wrapped_lines


def _collect_package_rename_changes(
    workspace_root: Path,
    current_package_name: str,
    target_package_name: str,
) -> list[PlannedChange]:
    current_path = workspace_root / "src" / current_package_name
    target_path = workspace_root / "src" / target_package_name
    if current_path == target_path or not current_path.exists():
        return []
    return [
        PlannedChange(
            path=target_path,
            description=(
                f"Rename package directory from {current_package_name} to {target_package_name}"
            ),
        )
    ]


def _rename_package_directory(
    workspace_root: Path,
    current_package_name: str,
    target_package_name: str,
) -> None:
    current_path = workspace_root / "src" / current_package_name
    target_path = workspace_root / "src" / target_package_name
    if current_path == target_path or not current_path.exists():
        return
    if target_path.exists():
        raise FileExistsError(f"Target package path already exists: {target_path}")
    current_path.rename(target_path)


def _write_license_file(path: Path, license_id: str, author_name: str) -> None:
    current_year = datetime.now(tz=UTC).year
    path.write_text(
        _license_text(
            license_id=license_id,
            author_name=author_name,
            current_year=current_year,
        ),
        encoding="utf-8",
    )


def _license_text(license_id: str, author_name: str, current_year: int) -> str:
    if license_id == "MIT":
        return (
            "MIT License\n\n"
            f"Copyright (c) {current_year} {author_name}\n\n"
            "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
            'of this software and associated documentation files (the "Software"), to deal\n'
            "in the Software without restriction, including without limitation the rights\n"
            "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
            "copies of the Software, and to permit persons to whom the Software is\n"
            "furnished to do so, subject to the following conditions:\n\n"
            "The above copyright notice and this permission notice shall be included in all\n"
            "copies or substantial portions of the Software.\n\n"
            'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n'
            "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
            "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
            "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
            "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
            "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
            "SOFTWARE.\n"
        )
    if license_id == "Apache-2.0":
        return (
            "Apache License\n"
            "Version 2.0, January 2004\n"
            "http://www.apache.org/licenses/\n\n"
            f"Copyright {current_year} {author_name}\n\n"
            'Licensed under the Apache License, Version 2.0 (the "License");\n'
            "you may not use this file except in compliance with the License.\n"
            "You may obtain a copy of the License at\n\n"
            "    http://www.apache.org/licenses/LICENSE-2.0\n\n"
            "Unless required by applicable law or agreed to in writing, software\n"
            'distributed under the License is distributed on an "AS IS" BASIS,\n'
            "WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
            "See the License for the specific language governing permissions and\n"
            "limitations under the License.\n"
        )
    if license_id == "BSD-3-Clause":
        return (
            "BSD 3-Clause License\n\n"
            f"Copyright (c) {current_year}, {author_name}\n"
            "All rights reserved.\n\n"
            "Redistribution and use in source and binary forms, with or without\n"
            "modification, are permitted provided that the following conditions are met:\n\n"
            "1. Redistributions of source code must retain the above copyright notice,\n"
            "   this list of conditions and the following disclaimer.\n"
            "2. Redistributions in binary form must reproduce the above copyright notice,\n"
            "   this list of conditions and the following disclaimer in the documentation\n"
            "   and/or other materials provided with the distribution.\n"
            "3. Neither the name of the copyright holder nor the names of its\n"
            "   contributors may be used to endorse or promote products derived from\n"
            "   this software without specific prior written permission.\n\n"
            'THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"\n'
            "AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE\n"
            "IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\n"
            "DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE\n"
            "FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL\n"
            "DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR\n"
            "SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER\n"
            "CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,\n"
            "OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE\n"
            "OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n"
        )
    if license_id == "MPL-2.0":
        return (
            "Mozilla Public License Version 2.0\n\n"
            f"Copyright (c) {current_year} {author_name}\n\n"
            "This Source Code Form is subject to the terms of the Mozilla Public\n"
            "License, v. 2.0. If a copy of the MPL was not distributed with this\n"
            "file, You can obtain one at https://mozilla.org/MPL/2.0/.\n"
        )
    return (
        "All Rights Reserved\n\n"
        f"Copyright (c) {current_year} {author_name}\n\n"
        "This project is proprietary. You may not use, copy, modify, distribute,\n"
        "or sublicense this software without explicit written permission from the\n"
        "copyright holder.\n"
    )
