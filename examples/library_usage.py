from __future__ import annotations

from graphix_lab import CommandRecord, PatternSummary


def main() -> None:
    command = CommandRecord(index=0, kind="N", node=0, nodes=(0,), raw="N(0)")
    summary = PatternSummary(
        command_count=3,
        node_count=2,
        input_nodes=(0,),
        output_nodes=(1,),
        measurement_count=1,
        command_kinds=(command.kind, "E", "M"),
    )
    print(f"Library example using {type(command).__name__}")
    print(
        f"Pattern summary tracks {summary.command_count} commands across "
        f"{summary.node_count} nodes."
    )


if __name__ == "__main__":
    main()
