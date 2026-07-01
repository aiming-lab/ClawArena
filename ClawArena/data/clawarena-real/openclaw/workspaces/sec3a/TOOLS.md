# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session |
| `sessions_history` | Read a specific history session | Use in the main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to ls, run scripts, write deliverables |

## Rules
- Source inputs under `incident/`, `regulatory/`, `code/`, `reports/`, `reference/` are read-only.
- Create deliverables under `output/` using exec (heredoc/python).
- Do not reference `code/legacy/` modules as current implementation — they are deprecated.
