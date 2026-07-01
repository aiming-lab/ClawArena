# Available Tools

| Tool | Purpose | Notes |
|---|---|---|
| `sessions_list` | Enumerate available history sessions | Use in main session |
| `sessions_history` | Read a specific history session | Use to review past discussion |
| `read` | Read workspace file | Available in all sessions |
| `exec` | Execute shell commands | Use to write deliverable files |

## Rules
- Source documents under `cases/`, `regulations/`, and `templates/` are read-only reference inputs.
- Write all deliverable files to `rca_outputs/` using `exec`.
- In history sessions, use only `read` and light `exec`.
