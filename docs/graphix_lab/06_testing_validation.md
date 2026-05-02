# Testing and validation

## Test strategy

Use TDD. Every behavior prompt should add tests before implementation.

## Test categories

### Unit tests

- domain dataclasses
- command normalization
- resource summaries
- trace construction
- error messages
- angle conversion

### Integration tests with Graphix

- create a one-qubit circuit
- create a two-qubit Bell-like circuit
- transpile through Graphix
- standardize and shift signals
- simulate with `statevector`
- verify command summaries are stable enough without relying on private Graphix internals

### Visualization tests

Use Matplotlib's non-interactive backend in tests.

Check:

- a figure is returned
- axes exist
- slider handle exists
- no GUI display is required

### Optional Qiskit tests

Use `pytest.importorskip("qiskit")`.

## Quality gate

Before a task is complete, run the template quality wrapper:

```bash
./bin/quality.sh
```

or on Windows:

```powershell
bin\quality.cmd
```

If unavailable, run:

```bash
ruff check . --fix
ruff format .
pytest
pyright
```
