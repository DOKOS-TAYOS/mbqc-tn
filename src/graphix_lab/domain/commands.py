from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CommandRecord:
    index: int
    kind: str
    node: int | None = None
    nodes: tuple[int, ...] = ()
    angle: float | None = None
    plane: str | None = None
    s_domain: tuple[int, ...] = ()
    t_domain: tuple[int, ...] = ()
    domain: tuple[int, ...] = ()
    raw: str = ""


def _iter_command_nodes(command: CommandRecord) -> tuple[int, ...]:
    if command.nodes:
        return command.nodes
    if command.node is None:
        return ()
    return (command.node,)


def _collect_command_related_nodes(command: CommandRecord) -> frozenset[int]:
    nodes: set[int] = set(_iter_command_nodes(command))
    nodes.update(command.domain)
    nodes.update(command.s_domain)
    nodes.update(command.t_domain)
    if command.node is not None:
        nodes.add(command.node)
    return frozenset(nodes)
