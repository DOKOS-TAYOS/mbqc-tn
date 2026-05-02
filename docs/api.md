# API Overview

## Public Python API

The template keeps the public Python API intentionally small.

```python
from graphix_lab import TemplateMetadata, get_template_metadata
```

### `TemplateMetadata`

Immutable dataclass describing the current template metadata:

- `package_name`
- `distribution_name`
- `project_title`
- `bootstrap_required`
- `scope_summary`
- `cli_commands`

### `get_template_metadata()`

Returns the current `TemplateMetadata` snapshot.

## Public CLI

- `bootstrap`
- `quality`
- `test`
- `clean`
- `licenses`

### CLI behavior notes

- `bootstrap` is for a fresh template copy only. Once `bootstrap_required` becomes `False`, the command exits with an error instead of prompting again.
- `quality` runs Ruff, pytest, and pyright through the active interpreter, which keeps `.venv` resolution consistent on Windows and Linux.
- `test` runs pytest through the active interpreter.
- `clean` removes caches and temporary artifacts, but stays conservative around `.venv`, `.git`, and inaccessible subtrees.
- `licenses` regenerates `THIRD_PARTY_LICENSES` from the active interpreter and excludes the local template package.

During template stage, `graphix_lab` is still a placeholder package name. After bootstrap, the module path changes. The `bin/` wrappers are the stable user-facing entrypoints across that rename.

Treat everything outside `src/graphix_lab/__init__.py` and the CLI subcommands as internal implementation detail.
