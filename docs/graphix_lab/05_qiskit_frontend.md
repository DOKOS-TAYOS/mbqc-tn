# Qiskit Frontend

The Qiskit frontend is optional and is not required for the core library.

## Dependency

```toml
[project.optional-dependencies]
qiskit = ["qiskit>=2,<3"]
```

Install it in the active `.venv` when needed:

```bash
python -m pip install -e .[qiskit,dev]
```

## Supported Gate Subset

The current adapter supports only:

- `h`
- `x`
- `y`
- `z`
- `s`
- `rx`
- `ry`
- `rz`
- `cx` / `cnot`

Unsupported instructions raise `UnsupportedGateError` with the gate name and
zero-based instruction index.

## Angle Units

Qiskit rotation gates use radians. Graphix Lab converts them into Graphix's pi
units with:

```python
angle_pi_units = angle_radians / math.pi
```

Advanced users may pass `angle_units="pi"` when their source parameters are
already expressed that way.

## Qubit Ordering

Imported qubit indices come from `QuantumCircuit.find_bit(qubit).index` and are
reused directly as `LabCircuit` node indices.

Measurement and classical-register semantics remain out of scope for the
current adapter.

## Example

`examples/qiskit_import.py` demonstrates the frontend and prints a friendly
message when `qiskit` is not installed yet.

## Testing

Real Qiskit tests should continue to use `pytest.importorskip("qiskit")`.
