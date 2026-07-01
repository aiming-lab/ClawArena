# Working Principles

1. **Authoritative-source-first**: The canonical SLA policy lives in
   `policy/sla_matrix_v1.json` (and later v2). Archived files named `ARCHIVED_*`
   and auto-generated summaries (e.g. `sessions/email_thread_sla_review.json`
   auto-summary section) are NOT authoritative — verify all numbers against the
   official policy files and reference documents.

2. **Update-aware**: When an update or official notice supersedes a prior instruction,
   the later instruction wins. Revisit and revise prior outputs rather than stacking
   contradictory logic. The supersede chain: sla_matrix_v1 → sla_matrix_v2 → reverted
   for L2 by Update-2 feishu notice.

3. **Output schema discipline**: Every JSON deliverable carries a top-level
   `schema_version` field set to `"1.0"`. Field names use snake_case.

4. **Numeric precision**: Percentage and duration fields are stored as numbers
   (not strings). Percentages are reported to two decimal places.

5. **Temporal precision**: All datetime fields use ISO 8601 format
   (YYYY-MM-DDTHH:MM:SSZ). Duration fields are in minutes (integer or float).

6. **Metadata block**: Every report file (not raw data files) carries a top-level
   `metadata` block containing `generated_at`, `agent_id`, and `schema_version`.
