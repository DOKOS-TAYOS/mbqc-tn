# README addendum for Graphix Lab

Merge this text into the root `README.md` after bootstrap.

## Graphix Lab

Graphix Lab is a small educational usability layer over Graphix for measurement-based quantum computing. It wraps Graphix circuits and patterns with readable summaries, command introspection, simulation reports, conceptual traces, and Matplotlib/NetworkX visualizations.

Graphix Lab does not replace Graphix. It delegates MBQC transpilation, pattern manipulation, flow/gflow logic, and simulation backends to Graphix.

## Minimal example

```python
from graphix_lab import circuit

lab = (
    circuit(2)
    .h(0)
    .cnot(0, 1)
    .compile()
    .standardize()
    .shift_signals()
)

print(lab.summary())
fig = lab.draw()
report = lab.run(backend="statevector", seed=123, trace=True)
```

## Development

Use the template wrappers:

```bash
./bin/quality.sh
```

On Windows:

```powershell
bin\quality.cmd
```
