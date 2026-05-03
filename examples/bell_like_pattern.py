from __future__ import annotations

from graphix_lab import ResourceSummary, circuit


def main() -> None:
    pattern = circuit(2).h(0).cnot(0, 1).compile().standardize()
    resources: ResourceSummary = pattern.resources()

    print("Bell-like pattern example")
    print("Resource summary:")
    print(
        f"nodes={resources.node_count}, "
        f"edges={resources.edge_count}, "
        f"measurements={resources.measurement_count}"
    )
    print(pattern.explain())


if __name__ == "__main__":
    main()
