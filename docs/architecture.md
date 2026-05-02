# Architecture

## High-Level Shape

This template uses a library-first structure with a thin CLI on top.

- `domain`: stable concepts and immutable metadata
- `app`: orchestration and use-case services
- `infrastructure`: adapters for filesystem and process execution when needed
- `cli.py`: presentation layer for command-line entrypoints

## MVC Guidance

Not every software library needs a visible Model-View-Controller folder tree on day one. Instead, this template keeps MVC as a growth rule:

- model-like concepts live in `domain`
- controller-like orchestration lives in `app`
- views or user-facing adapters live in CLI, APIs, or future UI layers

This avoids empty scaffolding while keeping separation of responsibilities clear.

## Bootstrap Strategy

The template starts with placeholder metadata and a placeholder package name. Bootstrap:

1. validates user answers
2. rewrites tracked text files
3. renames `src/project_name`
4. writes the chosen project license

Relative imports inside the package reduce the amount of fragile rename logic.
