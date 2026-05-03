from __future__ import annotations

from importlib import import_module

from graphix_lab import LabCircuit, from_qiskit
from graphix_lab.domain.errors import OptionalDependencyError


def main() -> None:
    print("Qiskit import example")

    try:
        qiskit_module = import_module("qiskit")
    except ModuleNotFoundError:
        print(
            "Qiskit is not installed in this environment. Install "
            "`python -m pip install -e .[qiskit,dev]` inside `.venv` to run this example."
        )
        return

    quantum_circuit_class = qiskit_module.QuantumCircuit
    quantum_circuit = quantum_circuit_class(2)
    quantum_circuit.h(0)
    quantum_circuit.cx(0, 1)

    try:
        imported: LabCircuit = from_qiskit(quantum_circuit)
    except OptionalDependencyError as error:
        print(str(error))
        return

    summary = imported.compile().summary()
    print(f"Imported circuit width: {imported.width}")
    print(f"Imported command kinds: {', '.join(summary.command_kinds)}")


if __name__ == "__main__":
    main()
