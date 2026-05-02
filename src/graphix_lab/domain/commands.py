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
