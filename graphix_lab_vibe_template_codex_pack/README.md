# Graphix Lab Codex Pack for `vibe_template`

This pack contains prompts and repo markdowns for implementing **Graphix Lab** as a usability, visualization, tracing, and education layer on top of Graphix, starting from:

```text
https://github.com/DOKOS-TAYOS/vibe_template
```

The important pivot is that Codex must not create a project from scratch. The template already supplies a `src` layout, a thin CLI, wrappers in `bin/`, test/quality tooling, CI, human docs, and AI handoff docs. Codex should bootstrap the template once, then evolve the bootstrapped package into `graphix_lab`.

## Recommended bootstrap identity

Use these values unless you explicitly decide otherwise:

| Field | Value |
|---|---|
| Project title | `Graphix Lab` |
| Distribution name | `graphix-lab` |
| Package name | `graphix_lab` |
| Initial version | `0.1.0` |
| License | `MIT` |
| Scope | `A small, educational usability layer over Graphix for measurement-based quantum computing experiments. The project wraps Graphix patterns and circuits with clearer summaries, command introspection, simulation reports, Matplotlib/NetworkX visualizations, step traces, and optional Qiskit import helpers without reimplementing Graphix core backends.` |

The author name can remain your preferred public author name.

## How to use this pack

1. Create the new repo from `DOKOS-TAYOS/vibe_template`.
2. Give Codex `prompts/00_template_bootstrap.md` first.
3. Copy the markdowns under `repo_docs_to_copy/` into the bootstrapped repo, preserving their paths.
4. Continue with the prompts in `prompts/MASTER_SEQUENCE.md`.
5. Use `prompts/REVIEW_PROMPT.md` before accepting an MVP branch.

The first sprint should usually stop after prompt `08_simulation_runner.md` or `10_static_visualization.md`. Qiskit, backend comparison, docs polish, and release work can come afterwards.
