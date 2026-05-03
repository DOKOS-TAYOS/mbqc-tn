from __future__ import annotations

from graphix_lab import BackendComparisonReport, circuit


def main() -> None:
    report: BackendComparisonReport = circuit(2).h(0).cnot(0, 1).compile().compare_backends()

    print("Backend comparison example")
    print(report)
    print(f"Runs recorded: {len(report.runs)}")


if __name__ == "__main__":
    main()
