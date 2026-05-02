# Integration with `vibe_template`

This project starts from `DOKOS-TAYOS/vibe_template`. The template already provides:

- `src` layout
- public API placeholder
- thin CLI
- `domain`, `app`, and `infrastructure` layering
- wrappers in `bin/`
- Ruff, pytest, and pyright quality flow
- docs for humans and agents
- CI for Windows and Ubuntu
- bootstrap metadata and package renaming

## What should be changed

After bootstrap:

- replace placeholder template metadata with Graphix Lab metadata
- replace template public API with Graphix Lab public API
- preserve the package layering
- preserve wrappers and quality flow
- update docs and examples

## What should not be changed casually

- Do not delete `bin/` wrappers.
- Do not remove the template's AI docs; update them.
- Do not remove CI unless replacing it with equivalent or stronger CI.
- Do not make the CLI the primary product.
- Do not re-run bootstrap after it has completed.
