# Working Principles

1. **Authoritative-source-first**: The canonical regulatory texts live under `regulatory/`.
   Auto-generated summaries (e.g. `reports/external_audit_summary_DECOY.md`) are convenience
   artefacts and are NOT authoritative — verify any number or claim against the regulatory files.

2. **Verbatim regulatory citations**: Always reference FTC rules by their exact CFR section
   designations (e.g. "16 CFR §255.5", never "the endorsement rule"). Verbatim quotations from
   regulatory text must be copied exactly from the source documents.

3. **Output schema tagging**: Every JSON deliverable carries a top-level `schema_version` field
   set to `"1.0"` — the compliance registry keys artefacts by it and rejects untagged files.

4. **Citation format**: Every compliance issue entry must carry an `ftc_citation` field with
   the format "16 CFR §XXX.X" (exact section number, including § symbol).

5. **Temporal awareness**: Regulatory guidance arrives incrementally. When a revised opinion or
   updated instruction supersedes an earlier one, the later instruction wins — revisit and revise
   prior outputs rather than stacking contradictory logic.

6. **Schema discipline**: Compliance reports follow fixed field structures. Use schema_version "1.0"
   on all JSON outputs. Markdown reports follow H1=document title, H2=claim category, H3=specific
   provision structure.
