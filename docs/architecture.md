# Architecture

## High-Level Shape

Graphix Lab uses a library-first structure with a thin CLI on top.

- `public_api.py`: the small public educational API
- `domain`: stable typed data models and domain errors
- `app`: orchestration services used by the public API and CLI
- `infrastructure`: adapters for Graphix, optional Qiskit, and a few tooling
  details
- `cli.py`: command-line entrypoints that delegate to services

## Design Direction

The project keeps Graphix as the source of truth for MBQC compilation and
simulation. Graphix Lab adds:

- clearer summaries and explanations
- safer wrapper entrypoints
- backend comparison and capability inspection
- trace and visualization helpers that stay script-friendly and headless-safe

## Separation Of Responsibilities

- model-like concepts live in `domain`
- orchestration lives in `app`
- external-library details live in `infrastructure`
- user-facing commands stay in `cli.py` and the top-level public API

This keeps the repo small without forcing GUI or notebook scaffolding before it
is needed.
