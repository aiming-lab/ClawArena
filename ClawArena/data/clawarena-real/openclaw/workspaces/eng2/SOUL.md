# Working Principles

1. **Authoritative-source-first**: The canonical field definitions and dataset-level
   statistics live in `data/reference/dataset_profile.json` and `docs/data_dictionary_excerpt.md`.
   Auto-generated summaries (e.g. files named `*_BOT_*` / `BOT_SUMMARY_*`) are convenience
   artefacts and are NOT authoritative — verify any number against the profile or the raw data.

2. **Verbatim field names**: Always reference official column names exactly as they appear in
   the data dictionary (e.g. `tpep_pickup_datetime`, never `pickup_datetime`). Renaming or
   abbreviating a field is a defect.

3. **Output schema tagging**: Every JSON deliverable carries a top-level `schema_version` field
   set to `"1.0"` — the lakehouse registry keys artefacts by it and rejects untagged files.

4. **Reproducibility**: Prefer re-runnable scripts under `scripts/` and `pipeline/` over
   one-off hand calculations, so that every headline number has a single source of truth.

5. **Temporal awareness**: Migration decisions arrive incrementally. When an operations notice
   or a corrected rule supersedes an earlier instruction, the later instruction wins — revisit
   and revise prior outputs rather than stacking contradictory logic.

6. **Schema discipline**: Quality reports follow a fixed field order. Pipeline scripts carry the
   standard interpreter + encoding header. Do not improvise schema shapes.
