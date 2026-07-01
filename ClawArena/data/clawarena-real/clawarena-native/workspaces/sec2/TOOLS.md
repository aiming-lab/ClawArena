# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session |
| `sessions_history` | Read a specific history session | Use in the main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to run scripts and write deliverable files |

## Rules
- Source inputs under `incident/`, `communications/`, `codebase/`, `policies/`, `archive/`
  are **read-only** — do not modify them.
- Create deliverable files under `output/` using `exec`.
- In history sessions, use only `read` and light `exec`.
