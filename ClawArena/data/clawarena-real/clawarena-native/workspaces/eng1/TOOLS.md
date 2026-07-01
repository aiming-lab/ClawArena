# Available Tools

| Tool | Purpose | Usage Notes |
|------|---------|-------------|
| `sessions_list` | List all available history sessions | Use in the main session to discover history |
| `sessions_history` | Read a specific history session | Use in the main session to review past discussion |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to run scripts, write deliverable files |

## Rules
- Source inputs under `src/requests/` are the subject of the CVE patch — you ARE expected to modify `src/requests/utils.py`.
- Write all analysis JSON under `analysis/`, test files under `tests/`, test results under `test_results/`, docs under `docs/`, and signoff under `signoff/`.
- In history sessions, use only `read` and light `exec`; do not call `sessions_list`/`sessions_history` there.
