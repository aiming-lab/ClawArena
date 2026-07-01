# Available Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| `sessions_list` | List all history sessions | Use in main session |
| `sessions_history` | Read a specific session | Use in main session |
| `read` | Read a workspace file | All sessions |
| `exec` | Execute shell commands | Write deliverable files using this tool |

## Rules
- Files under `cases/` and `protocols/` are **read-only** primary sources.
- Create deliverables under `output/` and `reports/` using `exec`.
- Bot summaries under `communications/feishu/` are non-authoritative — always verify.
