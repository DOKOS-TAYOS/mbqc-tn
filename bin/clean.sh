#!/usr/bin/env sh
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python"

if [ -x "$VENV_PYTHON" ]; then
    "$VENV_PYTHON" "$PROJECT_ROOT/scripts/run_template_command.py" clean "$@"
elif command -v python >/dev/null 2>&1; then
    python "$PROJECT_ROOT/scripts/run_template_command.py" clean "$@"
else
    python3 "$PROJECT_ROOT/scripts/run_template_command.py" clean "$@"
fi
