# Working Principles

1. **Authoritative-source-first**: The canonical policy definitions and ground-truth figures
   live in `platforms/{platform}/strike_system.json`, official platform documentation files,
   and `internal/` reference files. Auto-generated bot summaries (e.g. files prefixed with
   `BOT_SUMMARY_`) and archived reports under `reports/archived/` are NOT authoritative —
   verify any quoted number against the official platform files.

2. **Verbatim policy references**: Always reference official policy category names and
   rule text exactly as they appear in the platform documentation. Renaming, paraphrasing,
   or abbreviating is a defect.

3. **JSON formatting discipline (P1)**: Every JSON deliverable uses 2-space indentation
   and snake_case key names. No camelCase keys.

4. **Source attribution (P2)**: All numeric fields in JSON deliverables carry a
   companion `_source_url` field at the same JSON level documenting the authoritative URL.

5. **Temporal awareness**: Policy updates arrive incrementally via multiple channels.
   When a Discord modops notice or a subsequent email supersedes an earlier instruction,
   the later instruction wins — revisit and revise prior outputs rather than stacking
   contradictory logic.

6. **Unit discipline (P3)**: Time-limit values are expressed in months as the primary
   unit, retaining 1 decimal place (e.g. `3.0` months, `0.5` months for 14 days).

7. **Citation format (P4)**: Markdown documents use `[^N]` footnote references and
   include a `## 参考来源` (or `## References`) section at the document end.

8. **Report naming (P5)**: Files under `reports/` follow the naming convention
   `{type}_{yyyy-mm}.json`. When no specific month applies, use `latest`.
