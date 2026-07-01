# Working Principles

1. **Authoritative-source-first**: The canonical metric definitions and reference anchors
   live in `context/metric_definitions.md` and `data/reference/`. Auto-generated summaries
   (e.g. files with suffix `_BOT_SUMMARY` or annotated "auto-generated") are NOT authoritative —
   always verify any number against the primary reference or raw data files.

2. **Verbatim formula references**: When citing formulas (GMV, Take Rate, inventory days),
   use the exact phrasing from `context/metric_definitions.md`. Do not paraphrase or combine
   formulas from different calibration standards.

3. **Output structure tagging**: Every JSON deliverable must carry top-level fields
   `source_url` (or `source`) AND `generated_at` (ISO 8601 timestamp). The downstream
   financial reconciliation system keys artefacts by these fields.

4. **Cross-round numerical consistency**: Once a metric value is computed and filed, all
   subsequent rounds must reference the same value. Drift (re-computing a different result
   for the same underlying metric) is treated as a data-quality defect.

5. **Temporal awareness**: Data and instructions arrive incrementally. When an update or
   correction notice supersedes an earlier instruction or dataset version, the later
   instruction wins — revisit and revise prior outputs accordingly.

6. **Conflict documentation**: When you encounter conflicting data or instructions across
   channels, document the conflict in the output JSON rather than silently choosing one.
   Use the `from` field to identify the session source.
