# Roadmap

## Sprint 0: template bootstrap

- Create repo from `DOKOS-TAYOS/vibe_template`.
- Run bootstrap once with Graphix Lab identity.
- Confirm quality wrapper passes.

## Sprint 1: core wrapper MVP

- Graphix capability adapter.
- Public API shell.
- `LabCircuit` and `LabPattern` wrappers.
- Command records.
- Summary and explanation methods.
- Statevector simulation wrapper.

## Sprint 2: visualization and trace

- Syntactic command trace.
- NetworkX/Matplotlib graph extraction.
- Static drawing.
- Slider-based trace viewer.

## Sprint 3: backend comparison

- Compare available Graphix backends.
- Report timing, result type, errors, and warnings.
- Do not interpret approximate accuracy unless a meaningful metric is implemented.

## Sprint 4: Qiskit import

- Optional dependency.
- Small gate subset.
- Radian-to-π-unit conversion.
- Clear unsupported-gate errors.

## Sprint 5: examples and release hardening

- Examples for one-qubit rotation, Bell-like circuit, small MBQC trace, backend comparison, and Qiskit import.
- Documentation polish.
- Release checklist.

## Later research spikes

- Better Graphix trace hooks if Graphix exposes simulation events.
- More advanced flow/gflow visualization.
- Optional symbolic support.
- Optional GPU/TN acceleration only if Graphix or another dependency exposes a stable API.
