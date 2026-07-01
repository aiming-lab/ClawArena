# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session |
| `sessions_history` | Read a specific history session | Use in main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to run scripts and write deliverables |

## Rules
- Files under `data/`, `regulations/`, and `models/` are read-only source material.
- Create deliverables under `output/` using `exec`.
- In history sessions, use only `read` and light `exec`.
