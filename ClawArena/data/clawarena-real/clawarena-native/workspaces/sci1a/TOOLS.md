# Available Tools

| Tool | Purpose |
|---|---|
| `sessions_list` | List all available history sessions |
| `sessions_history` | Read a specific history session |
| `read` | Read a workspace file |
| `exec` | Execute a shell command (write deliverables, run analysis) |

## Rules
- Source files under `cases/` and `protocols/` are **read-only** inputs.
- Deliver outputs under `reports/wip/` (draft) and `reports/final/` (finalised).
- In history sessions, use `read` and `exec` only; do not call `sessions_list`/`sessions_history` there.
