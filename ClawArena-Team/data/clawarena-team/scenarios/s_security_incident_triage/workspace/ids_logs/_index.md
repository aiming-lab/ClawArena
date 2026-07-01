# ids_logs/ — Intrusion Detection System Alerts

| File | Content |
|---|---|
| ids_alerts.ndjson | Suricata IDS alert stream (53 events) |
| ids_summary.md | IDS analyst summary |

**Sub-agent scope**: Read `ids_logs/` only.
Summarize critical alerts to `audit/partial_ids.md`.
Identify: attacker IP, C2 beacon, exfil attempt status.
Do NOT access secrets/, pii/, or employee_data/.
