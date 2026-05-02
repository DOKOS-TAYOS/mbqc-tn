# Graphix integration contract

## Principle

Graphix Lab delegates MBQC semantics to Graphix.

Do not reimplement:

- circuit-to-pattern transpilation
- measurement calculus rewriting
- flow, gflow, or pauli-flow discovery
- statevector, density matrix, tensor network, or MPS simulation
- Graphix graph-state optimization passes

## Capability adapter

Implement `infrastructure/graphix_capabilities.py` to detect available Graphix APIs at runtime.

Suggested dataclass:

```python
@dataclass(frozen=True, slots=True)
class GraphixCapabilities:
    version: str
    has_circuit: bool
    has_pattern_simulate_pattern: bool
    has_pattern_draw_graph: bool
    has_pattern_draw_flow: bool
    has_pattern_draw_xzcorrections: bool
    has_pattern_standardize: bool
    has_pattern_shift_signals: bool
    has_pattern_perform_pauli_measurements: bool
    supported_backends: tuple[str, ...]
```

Use `importlib.metadata.version("graphix")` and `hasattr` checks. Avoid assuming Graphix minor versions have identical visualization names.

## Command extraction

Graphix command objects should be normalized into Graphix Lab `CommandRecord` objects.

Expected command kinds:

- `N`: preparation
- `E`: entanglement
- `M`: measurement
- `X`: X correction
- `Z`: Z correction
- `C`: local Clifford
- unknown command fallback

The adapter should extract fields defensively:

- node
- nodes / edge
- measurement plane
- measurement angle
- s-domain
- t-domain
- correction domain
- raw representation

## Simulation

Preferred simulation path:

1. If pattern has `simulate_pattern`, call it.
2. Otherwise, instantiate `graphix.simulator.PatternSimulator` if available.
3. Raise `GraphixCompatibilityError` with a clear message if neither path works.

Supported backend names should include only what the installed Graphix version exposes or what the adapter can verify. Do not promise custom GPU/MPI support.
