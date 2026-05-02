from __future__ import annotations

from graphix_lab import CommandRecord, GraphixCapabilities, LabPattern, circuit, graphix_info


def test_graphix_info_reports_real_runtime_capabilities() -> None:
    capabilities = graphix_info()

    assert isinstance(capabilities, GraphixCapabilities)
    assert capabilities.version.startswith("0.3.")
    assert capabilities.has_circuit is True
    assert capabilities.has_pattern_standardize is True
    assert capabilities.has_pattern_shift_signals is True
    assert capabilities.has_pattern_perform_pauli_measurements is True


def test_real_graphix_compile_and_command_introspection_work_together() -> None:
    lab_pattern = circuit(2).h(0).cnot(0, 1).compile()
    graphix_pattern = lab_pattern.to_graphix()
    commands = lab_pattern.commands()

    assert isinstance(lab_pattern, LabPattern)
    assert type(graphix_pattern).__module__.startswith("graphix")
    assert isinstance(commands, tuple)
    assert commands
    assert all(isinstance(command, CommandRecord) for command in commands)
    assert [command.index for command in commands] == list(range(len(commands)))
    assert all(command.raw for command in commands)
    assert all(command.kind != "UNKNOWN" for command in commands)
    assert {"N", "E", "M"}.issubset({command.kind for command in commands})
