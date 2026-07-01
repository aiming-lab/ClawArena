# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session |
| `sessions_history` | Read a specific history session | Use in the main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to write deliverable files and run scripts |

## Rules
- Source inputs under `incident/`, `regulatory/`, `code/`, `reports/`, `reference/` are READ-ONLY.
- Create deliverables under `output/` using `exec`.
- Run SHA-256 checksums with `exec sha256sum <file>` or Python hashlib — do NOT guess hashes.
- When running backtest scripts: `exec python regulatory/sec_backtest_template.py`
