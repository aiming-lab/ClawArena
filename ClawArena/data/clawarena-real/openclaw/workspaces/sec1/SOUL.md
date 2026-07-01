# Working Principles

1. **Source primacy**: The canonical ground-truth for vulnerability details lives in
   `assets/advisories/NVD_CVE-2024-6387.json` and `assets/advisories/GHSA-2x8c-95vh-gfv4.json`.
   Auto-generated bot summaries (files containing "BOT_" in the name, or marked as
   "auto-summarized") are NOT authoritative — verify any number or date against the primary
   advisory files or the Qualys technical report.

2. **Verbatim field values**: Always reference official identifiers exactly as they appear in
   the source documents (e.g., CVE-2024-6387, CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H,
   GHSA-2x8c-95vh-gfv4). Do not abbreviate or paraphrase CVE IDs or CVSS vectors in
   structured JSON output.

3. **Output conventions**: All JSON deliverables use 2-space indentation. Top-level fields
   are sorted in alphabetical order. File names use snake_case exclusively.

4. **Supersede awareness**: When a later instruction or update explicitly revokes an earlier
   decision, the later instruction wins. Record the supersede relationship explicitly.

5. **Temporal discipline**: The disclosure date is 2024-07-01. All remediation timelines
   are calculated from this anchor. Do not conflate the disclosure date with the regression
   introduction date (2020-10-16).

6. **Cross-round consistency**: Numbers you compute in one round (e.g., prod host count,
   vulnerable_count) must remain consistent with any later round that references them.
