# Working Principles

1. **Authoritative-source-first**: The canonical FTC regulatory texts live under
   `regulatory/`. Auto-generated summaries (files named `*_DECOY*` or `*_SUMMARY_BOT*`)
   are NOT authoritative — they may contain deliberate errors. Always verify numbers
   against the primary regulatory documents.

2. **Verbatim citation**: When quoting statutory or regulatory text, reproduce the exact
   wording from the source document. Never paraphrase §255.5 or §465.2 in legal deliverables.

3. **Output schema discipline**: Every JSON deliverable carries a top-level
   `"schema_version": "1.0"` field (P1). Every compliance issue entry carries a
   `"ftc_citation"` field formatted exactly as `"16 CFR §XXX.X"` (P2).

4. **Markdown heading hierarchy** (P3, active from Q4 feedback onward):
   H1 = document title / file name; H2 = claim category; H3 = specific provision.

5. **Temporal awareness**: When a later communication (update, revised letter) supersedes
   an earlier one, the later document controls — revisit prior conclusions accordingly.

6. **Severity tagging** (P4, active from Q4 feedback onward):
   Prohibited-term replacement tables must include a `severity` column (high/medium/low)
   corresponding to FTC enforcement priority.

7. **File naming in `final/`** (P5): All documents placed under the `final/` directory
   must follow the convention `{document_type}_final_YYYYMMDD.{ext}`.
