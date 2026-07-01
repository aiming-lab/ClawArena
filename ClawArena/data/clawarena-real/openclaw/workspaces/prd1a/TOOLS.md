# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session |
| `sessions_history` | Read a specific history session | Use in the main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to ls, run scripts, write deliverable files |

## Rules
- Regulatory texts under `regulatory/` are read-only — do not modify them.
- Create deliverables under `reports/`, `policies/`, `templates/`, `training/`, and `final/`.
- Use `exec` with heredoc/python to write output files.
- In history sessions, use only `read` and light `exec`.
