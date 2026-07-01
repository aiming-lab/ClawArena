# Working Principles

1. **Authoritative-source-first**: Ground-truth anchors live in
   `regulatory/` documents and `reference/` files. Auto-generated
   bot summaries (e.g. `reports/bot_summary_*.md`) are convenience
   artefacts only — verify every claimed number against the original source.

2. **UTC is the reporting standard**: MiFIR Field 28 and all settlement
   timestamps must be expressed in UTC, never local time. DST transitions
   affect the UTC offset and must be handled explicitly.

3. **snake_case JSON fields**: All JSON deliverables use snake_case field
   naming throughout (never camelCase or PascalCase).

4. **Regulatory citation precision**: When referencing regulatory rules,
   include the specific sub-clause (e.g. "Rule 15c3-5(b)", not just
   "Rule 15c3-5"). FCA Market Watch 59 requires explicit Field 28 citation.

5. **Temporal awareness**: Updates arriving mid-session may supersede
   prior instructions. When a later instruction contradicts an earlier
   one, the later instruction takes precedence — revise prior outputs.

6. **Schema discipline**: Compliance action plans require an `owner`
   field per remediation item. Regulatory submission JSON must follow
   the fixed field order: incident_date → rule_violated →
   financial_impact → remediation_count → submission_date.
