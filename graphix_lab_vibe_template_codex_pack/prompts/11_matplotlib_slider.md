Goal: implement a Matplotlib slider for conceptual trace inspection.

Tasks:
1. Add tests that create the slider handle without opening a GUI.
2. Implement a small handle dataclass, for example `TraceAnimationHandle`, containing figure, axes, slider, trace, and update callback references.
3. Implement `RunTrace.animate(...)` or `LabPattern.animate(...)` using `matplotlib.widgets.Slider`.
4. The slider should update:
   - title or step label
   - highlighted current node(s)
   - measured/pending node styling
   - a text box with the current command description
5. Keep the implementation simple and robust. Do not introduce a web GUI or notebook-only dependency.
6. Ensure references are retained so callbacks are not garbage-collected.
7. Update docs and examples.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.
