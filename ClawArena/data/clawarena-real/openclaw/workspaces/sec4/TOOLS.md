# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session to discover history |
| `sessions_history` | Read a specific history session | Use in the main session to review past discussion |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to run validation scripts and write deliverable files |

## Rules
- Source files under `ropa/`, `breach/`, `dpia/`, `policies/`, `company/` are read-only inputs.
- Create deliverable files under `audit/`, `dsar/` (response files), and `ropa/` (fixed versions).
- Scripts under `scripts/` are provided as utilities — use them when directed.
