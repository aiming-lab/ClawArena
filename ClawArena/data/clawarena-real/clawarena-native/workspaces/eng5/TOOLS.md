# Available Tools

| Tool | Purpose | Usage Notes |
|------|---------|-------------|
| `sessions_list` | List all available history sessions | Use in the main session to discover history |
| `sessions_history` | Read a specific history session | Use in the main session to review past discussion |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to inspect files and write deliverable files |

## Rules
- Configuration files are the primary artifacts; always back up before modifying.
- Deliverable JSON reports go under `audit/`; scripts under `scripts/`.
- In history sessions, use only `read` and light `exec`.
