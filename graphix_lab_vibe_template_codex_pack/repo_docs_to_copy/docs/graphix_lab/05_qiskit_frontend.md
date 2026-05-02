# Qiskit frontend

The Qiskit frontend is optional and should not be required for installing the core library.

## Dependency

Add Qiskit under an optional extra, for example:

```toml
[project.optional-dependencies]
qiskit = ["qiskit>=2,<3"]
```

The exact lower bound can be adjusted after tests against the installed Qiskit version.

## Gate subset for first implementation

Support only a small, explicit subset:

- `h`
- `x`
- `y`
- `z`
- `s`
- `rx`
- `ry`
- `rz`
- `cx` / `cnot`

Unsupported instructions should raise `UnsupportedGateError` with the gate name and index.

## Angle units

Qiskit rotation gates use radians. Graphix rotation methods use angles in units of π. The adapter should convert:

```python
angle_pi_units = angle_radians / math.pi
```

Allow `angle_units="pi"` for advanced users who already provide Graphix-style units.

## Bit and qubit ordering

Qiskit and Graphix conventions may differ. The adapter should document the chosen convention and test it on small circuits.

## Testing

All Qiskit tests should be skipped when Qiskit is not installed.
