# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session |
| `sessions_history` | Read a specific history session | Use in the main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to inspect files and write deliverables |

## Rules
- Source inputs under `company/`, `legal/`, `pip_case/`, `layoff/` are READ-ONLY reference.
- Create deliverables under `reports/` and `legal/` (output files).
- Use `exec` (e.g., heredoc or Python) to write JSON/Markdown output files.
