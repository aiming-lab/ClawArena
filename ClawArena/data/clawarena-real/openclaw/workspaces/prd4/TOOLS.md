# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Main session only |
| `sessions_history` | Read a specific history session | Main session only |
| `read` | Read a workspace file | All sessions |
| `exec` | Execute a shell command | Write deliverable files, run scripts |

## Rules
- `policy/`, `tickets/`, `reference/`, `scripts/` are read-only inputs.
- Create deliverables under `output/` using `exec`.
- Do not modify source files.
