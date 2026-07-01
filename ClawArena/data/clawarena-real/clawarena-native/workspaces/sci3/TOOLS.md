# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session |
| `sessions_history` | Read a specific history session | Use in main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to write deliverable files |

## Rules
- Regulation documents under `regulations/` are read-only authoritative sources.
- Hospital data under `hospital_data/` are read-only input records.
- Create deliverables under `output/` using `exec`.
- Do NOT modify source files under `regulations/` or `hospital_data/`.
