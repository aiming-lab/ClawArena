# Working Principles

1. **Authoritative-source-first**: Primary sources are the Data Colada technical reports
   (`cases/gino/datacolada_reports/`), the original paper datasets, and official retraction
   notices under `cases/gino/retraction_notices/`. Bot-generated summaries (files named
   `*_BOT_*` or `BOT_SUMMARY_*`) are convenience artefacts — NOT authoritative. Always
   verify any number against the primary documents.

2. **Verbatim DOI references**: Always cite DOIs exactly as they appear in the primary sources.
   Never abbreviate or reconstruct a DOI from memory.

3. **schema_version tagging**: Every JSON deliverable carries a top-level `schema_version`
   field set to `"1.0"`. The RIO filing system rejects untagged artefacts.

4. **Report naming convention**: All report files follow the pattern
   `YYYY-MM-DD_caseid_type.md` (e.g., `2023-07-12_gino_final_report.md`). Deviate and
   the filing system will reject the file.

5. **Report structure**: Every formal RIO case report must contain exactly four sections:
   `## Background`, `## Evidence`, `## Classification`, `## Recommendation`.
   Summarise in an executive summary of no more than 300 words.

6. **Temporal awareness**: When a superseding document arrives, the later instruction wins.
   Identify and discard outdated memos explicitly.

7. **Retraction pair logging**: For every retracted paper, record BOTH the original DOI
   and the retraction-notice DOI in separate fields.
