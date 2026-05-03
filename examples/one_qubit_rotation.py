from __future__ import annotations

from graphix_lab import PatternSummary, circuit


def main() -> None:
    pattern = circuit(1).rx(0, 0.25).compile()
    summary: PatternSummary = pattern.summary()

    print("One-qubit rotation example")
    print(f"Command count: {summary.command_count}")
    print(f"Command kinds: {', '.join(summary.command_kinds)}")
    print(pattern.explain())


if __name__ == "__main__":
    main()
