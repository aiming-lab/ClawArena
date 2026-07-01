# Available Tools

| Tool | Purpose |
|------|---------|
| `sessions_list` | List all available history sessions |
| `sessions_history` | Read a specific history session |
| `read` | Read a workspace file |
| `exec` | Execute a shell command (write deliverables via heredoc/python) |

## Rules
- Raw reference files are read-only.
- Create all new deliverables under `output/`, `postmortem/`, or `communications/`.
- In history sessions, use only `read` and `exec`; do not call `sessions_list/sessions_history`.
