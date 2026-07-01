# Working Principles

1. **Authoritative-source-first**: Regulatory anchors (SEC release numbers, rule citations,
   financial figures) come from the documents under `regulatory/` and `reference/`.
   The `reports/bot_summary_incident_20241103.md` is a machine-generated convenience summary
   and is explicitly non-authoritative — confirm every figure against primary sources.

2. **Verbatim citations**: When referencing SEC rules, always include the specific sub-paragraph,
   e.g., "Rule 15c3-5(b)" — not just "Rule 15c3-5". When citing MiFIR fields, use the
   exact field label "Field 28". This is a Preference enforced throughout the engagement.

3. **Output schema tagging**: Every JSON deliverable carries a top-level `schema_version` field
   set to `"1.0"` — this is required for regulatory submission metadata validation.

4. **JSON field naming**: All JSON output must use snake_case field names exclusively.
   No camelCase (e.g., `incidentDate`) or PascalCase. This is non-negotiable.

5. **Temporal discipline**: When update notices arrive (regulatory or internal), the later
   instruction supersedes the earlier one. Revise prior outputs accordingly.

6. **Cross-round consistency**: Figures committed in one output (order counts, timestamps,
   financial impacts) must remain consistent across all subsequent outputs unless an update
   explicitly revises them. Inconsistency triggers regulatory data quality flags.
