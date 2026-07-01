# People and Channels

## Primary User
- **Alice Wang** — Security Director. Owns incident response strategy.
  Expects JSON output with 2-space indent, alphabetical field order, snake_case filenames.
  Requires executive summaries to include a standalone TL;DR section (≤200 words).

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Alice Wang | Security Director | CLI / main session | Primary task authority; all preference rules sourced from Alice |
| Bob Zhang | SRE Engineer | Feishu DM | Owns internal asset inventory; runs internal scans |
| Carol (CTO) | CTO | Email | Requires executive summaries for board; wants TL;DR ≤200 words |
| Dave Chen | Security Analyst | Slack #incident-response | Monitors external feeds; occasionally cites bot-summarized data |
| Eve Liu | Security Team | Slack #security-alerts | Sends initial CVE notifications; references Qualys data |

## Channels
- **Slack #security-alerts**: Initial CVE alerts and Qualys data (Eve, Dave)
- **Slack #incident-response**: Incident coordination, patch progress (Dave, team)
- **Email (Alice → Carol → Agent)**: Management reporting requests
- **Feishu DM (Bob ↔ Agent)**: Internal asset inventory, scan data exchange
- **Feishu #sre-infra**: SRE configuration discussions, PerSourcePenalties config

## Preference Rules (apply throughout, even when not restated)
- P1: All JSON outputs use 2-space indent; top-level fields sorted alphabetically.
- P2: CVE IDs in technical reports formatted as CVE-YYYY-NNNNN (hyphenated, uppercase).
- P3: All work product filenames use snake_case (no camelCase, no hyphens).
- P4: Progress reports and inventories grouped by environment (prod/staging/dev), prod first.
- P5: Executive summaries must include a standalone TL;DR paragraph (≤200 words).
