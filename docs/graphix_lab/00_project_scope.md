# Project scope

## Mission

Graphix Lab makes Graphix easier to use for learning, teaching, debugging, and small-to-medium MBQC experimentation.

The project should let a user write code like:

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
lab.draw()
result = lab.run(backend="statevector", seed=123, trace=True)
result.trace.animate()
```

## In scope for MVP

- Small public Python API.
- Wrappers around Graphix `Circuit` and `Pattern` objects.
- Graphix capability/version adapter.
- Command introspection into stable `CommandRecord` objects.
- Pattern summaries and resource estimates.
- Graphix-delegated simulation runner for supported backends.
- Syntactic execution trace of commands.
- Static graph visualization with Matplotlib and NetworkX.
- Slider-based trace visualization with `matplotlib.widgets.Slider`.
- Examples and tests.

## Out of scope for MVP

- Implementing a new MBQC compiler.
- Implementing a new tensor-network simulator.
- GPU, MPI, CUDA-Q, cuQuantum, or distributed execution.
- Full Qiskit feature parity.
- Full symbolic pattern support beyond what Graphix already exposes.
- Heavy GUI frameworks.

## Design principle

When Graphix already does something, delegate to Graphix. Graphix Lab should add clarity, diagnostics, affordances, and educational presentation.
