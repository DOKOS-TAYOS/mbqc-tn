Goal: implement a syntactic MBQC command trace independent of Graphix simulator internals.

Tasks:
1. Add tests for `LabPattern.trace()` on a small pattern.
2. Implement `RunTrace` construction from `CommandRecord` objects.
3. Each `TraceFrame` should capture:
   - step index
   - command kind
   - current node or nodes
   - measured nodes so far
   - pending nodes
   - active correction notes
   - readable description
4. For `M` commands, mark the node as measured after the frame or during the frame consistently and document the convention.
5. For `X` and `Z` commands, add correction dependency descriptions from domains.
6. Do not claim that this trace is the exact internal Graphix simulation trajectory. It is a conceptual/syntactic trace of the command list.
7. Integrate `trace=True` in `LabPattern.run(...)` if not already done.
## Completion requirements

- Add or update tests first where behavior changes.
- Run the smallest relevant tests during development.
- Before finishing, run the template quality wrapper if available.
- Update `CHANGELOG.md` and `docs/docs_for_ai/status.md` for meaningful changes.
- Do not claim completion if tests or type checks fail; report the exact blocker.
