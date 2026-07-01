# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session |
| `sessions_history` | Read a specific history session | Use in the main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to write deliverables, run scripts |

## Rules
- Files under `assets/` are READ-ONLY reference inputs. Do not modify them.
- Create all deliverables under `work/` using `exec` (heredoc or python).
- History sessions contain relevant context from Slack, Email, and Feishu channels.
