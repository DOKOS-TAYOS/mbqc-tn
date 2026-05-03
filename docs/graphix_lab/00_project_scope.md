# Project Scope

## Mission

Graphix Lab makes Graphix easier to use for learning, teaching, debugging, and
small-to-medium MBQC experimentation.

The current public flow is intentionally small:

```python
from graphix_lab import circuit

pattern = circuit(2).h(0).cnot(0, 1).compile().standardize()

print(pattern.summary())
print(pattern.explain())

report = pattern.compare_backends(backends=("statevector",))
print(report)
```

## In Scope For The MVP

- Small public Python API
- Wrappers around Graphix `Circuit` and `Pattern` objects
- Graphix capability and backend detection
- Command introspection into stable `CommandRecord` objects
- Pattern summaries and resource estimates
- Graphix-delegated simulation and backend comparison
- Syntactic execution traces
- Static graph visualization with Matplotlib and NetworkX
- Slider-based trace visualization with `matplotlib.widgets.Slider`
- Script examples under `examples/`

## Out Of Scope For The MVP

- Implementing a new MBQC compiler
- Implementing a new tensor-network simulator
- GPU, MPI, CUDA-Q, cuQuantum, or distributed execution
- Full Qiskit feature parity
- Heavy GUI frameworks
- Notebook-first workflows before the script examples are stable

## Design Principle

When Graphix already does something, Graphix Lab should delegate to it and add
clarity, diagnostics, and educational presentation around it.
