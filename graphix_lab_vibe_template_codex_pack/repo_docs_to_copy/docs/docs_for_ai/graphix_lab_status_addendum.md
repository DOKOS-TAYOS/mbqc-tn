# Graphix Lab AI status addendum

Use this together with `docs/docs_for_ai/status.md`.

## Current intended architecture

Graphix Lab is a usability layer over Graphix. It should delegate MBQC semantics to Graphix and expose clearer educational APIs.

## Current MVP target

- `graphix_lab.circuit`
- `LabCircuit`
- `LabPattern`
- command introspection
- pattern summary and explanation
- Graphix-delegated simulation
- syntactic trace
- static visualization
- slider-based trace visualization

## Current blockers to check

- Installed Graphix version and available methods.
- Visualization API differences between Graphix versions.
- Whether the selected PyPI distribution name is still available before publishing.

## Handoff rule

After every meaningful change, update the main status file with:

- current phase
- next step
- blockers
- tests added
- quality command result
