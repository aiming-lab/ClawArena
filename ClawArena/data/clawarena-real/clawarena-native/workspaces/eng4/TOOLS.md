# Available Tools

| Tool               | Purpose                                   | Notes |
|--------------------|-------------------------------------------|-------|
| `sessions_list`    | List all available history sessions       | Main session only |
| `sessions_history` | Read a specific history session           | Main session only |
| `read`             | Read a workspace file                     | All sessions |
| `exec`             | Execute a shell command                   | Use to write deliverable files |

## Rules
- All inputs under `db/`, `reports/`, `configs/`, `scripts/`, `archive/` are **read-only**.
- Write ALL deliverables under `work/` using `exec` (heredoc / python).
- In history sessions, use only `read` and light `exec`; do not call session tools there.
