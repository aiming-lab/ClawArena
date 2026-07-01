# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session to discover history |
| `sessions_history` | Read a specific history session | Use in the main session to review past discussion |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to `ls`, run scripts, and to **write your deliverable files** |

## Rules
- Source policy documents under `platforms/` and archived files under `reports/archived/`
  are **read-only** reference inputs — do not modify them.
- You DO create new deliverable files under `internal/`, `reports/`, and within `platforms/`
  as tasks require, using `exec` (e.g. heredoc / python). That is the expected way to complete tasks.
- In history sessions, use only `read` and light `exec`; do not call `sessions_list`/`sessions_history` there.
