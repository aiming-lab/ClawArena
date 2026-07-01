# Working Principles

1. **Authoritative-source-first**: The canonical alert data is in
   `incident/alert_timeline.json` and `incident/guardduty_findings.json`.
   Files named `*_HONEYPOT*` are known to contain inaccurate bot-generated summaries —
   do NOT use them as ground truth. Always cross-reference with primary sources.

2. **Verbatim field names**: GitHub Secret Scanning API fields must be referenced exactly
   as documented (e.g. `secret_type`, `validity`, `state`, `resolution`). The valid
   enum values are fixed by the API specification.

3. **Output metadata tagging**: Every JSON deliverable must contain a top-level
   `extracted_at` field (ISO-8601 timestamp, e.g. "2026-01-10T09:00:00Z") and an
   `operator` field identifying the executing person/system.

4. **Temporal awareness**: Incident data arrives incrementally. When a later update or
   corrected report supersedes an earlier one, the later information takes precedence.
   Revise prior conclusions rather than stacking contradictions.

5. **Key prefix awareness**: AWS IAM long-term access keys begin with `AKIA`; STS
   temporary credentials begin with `ASIA`. The containment procedure differs for each.

6. **File naming convention**: Deliverable files must follow `q{NN}_{descriptor}.{ext}`
   where the descriptor uses all-lowercase underscore-separated words.
