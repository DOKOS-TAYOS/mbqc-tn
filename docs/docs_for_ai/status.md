# Status

- Phase: Template hardened for Windows-first bootstrap and maintenance
- Last update: test isolation, cleanup walking, bootstrap guardrails, wrapper/runtime behavior, fresh-copy CI smoke coverage, and public-template licensing were tightened
- Next step: Create a project from the template and run bootstrap once
- Blockers: None in template state
- License: MIT

## Checklist

- [x] Library-first package structure exists
- [x] CLI commands exist
- [x] Human documentation baseline exists
- [x] AI documentation baseline exists
- [x] Bootstrap resyncs the editable install
- [x] Bootstrap refuses re-running after template setup is complete
- [x] CI validates a fresh template copy through bootstrap plus quality
- [x] Minimal stable wrappers exist
- [x] Cleanup command protects `.venv`
- [x] Cleanup tolerates inaccessible subtrees conservatively
- [ ] Project-specific bootstrap completed
- [ ] Third-party license inventory regenerated after dependency install
