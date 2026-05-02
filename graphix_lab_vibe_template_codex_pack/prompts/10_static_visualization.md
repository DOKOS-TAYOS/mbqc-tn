Goal: implement static MBQC visualization using Matplotlib and NetworkX, with Graphix fallback/delegation where useful.

Tasks:
1. Add tests using a non-interactive Matplotlib backend.
2. Implement graph extraction from `CommandRecord` objects:
   - nodes from all command records
   - edges from `E` records
   - measured nodes from `M` records
   - correction dependencies from `X`, `Z`, and measurement domains when available
3. Implement `LabPattern.draw(...)` returning a Matplotlib `Figure`.
4. Allow options such as:
   - `show_flow: bool = True`
   - `show_corrections: bool = True`
   - `layout: str = "auto"`
   - `ax: matplotlib.axes.Axes | None = None`
5. If Graphix exposes a suitable draw method and the caller requests delegation, allow delegating. Otherwise, use the local NetworkX/Matplotlib renderer.
6. Do not require a display server.
7. Update visualization docs.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.
