# Working Principles

1. **Primary-source priority**: Raw alert/event logs and official metrics CSV files are
   authoritative. Auto-generated bot summaries (e.g. `archive/DRAFT_postmortem_bot_summary.md`)
   are convenience artefacts and are NOT authoritative — always verify any number against
   the primary logs or metrics.

2. **Verbatim Lua function names**: When referencing Lua code defects, always quote the
   exact function names that appear in `code/rate_limit/rule_engine_v1.lua`.
   Never paraphrase or abbreviate.

3. **Timestamp format**: All timestamps in output deliverables must use ISO 8601 UTC
   format: `YYYY-MM-DDTHH:MM:SSZ`. No other format is accepted.

4. **Numeric precision**: Percentage/ratio fields must be formatted to two decimal places
   (e.g. `2.10` not `2.1`), with a `"unit": "percent"` annotation on the same object.

5. **Supersede awareness**: When a later update or instruction revises an earlier one,
   the later instruction wins. Mark superseded action items with `~~strikethrough~~`
   in final documents.

6. **Output tagging**: JSON deliverables produced after the `generated_at` preference
   is established must include a top-level `"generated_at"` field (ISO 8601 UTC) and
   file names must use snake_case suffixes.

7. **Bilingual headings**: Postmortem section headings must use the format
   `## Section Name / 章节名称` (English name, slash, Chinese name).
