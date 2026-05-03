from __future__ import annotations

from matplotlib import pyplot as plt

from graphix_lab import TraceAnimationHandle, circuit


def main() -> None:
    handle: TraceAnimationHandle = (
        circuit(2).h(0).cnot(0, 1).compile().animate(show_flow=False, layout="shell")
    )
    handle.update(len(handle.trace.frames) - 1)

    print("Trace slider example")
    print(f"Trace frames: {len(handle.trace.frames)}")
    print(handle.graph_axes.get_title())

    plt.close(handle.figure)


if __name__ == "__main__":
    main()
