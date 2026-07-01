# Working Principles

1. **Authoritative-source-first**: The canonical ground truth for CVE details lives in NVD
   (https://nvd.nist.gov/vuln/detail/CVE-2024-47081) and the official GitHub PR #6965
   (https://github.com/psf/requests/pull/6965). Auto-generated Slack bot summaries and
   draft emails may contain errors — always verify critical figures against the primary source.

2. **Snake_case JSON fields**: Every JSON deliverable uses snake_case field names.
   camelCase is forbidden in any output JSON file (P1 preference, enforced throughout).

3. **Supersede awareness**: When a later update explicitly supersedes or corrects an earlier
   instruction, the later instruction wins. Revise any prior outputs accordingly rather than
   accumulating contradictory state.

4. **Verbatim precision**: Function names, commit SHAs, CVE IDs, CVSS vectors must be
   copied verbatim from the authoritative source — do not paraphrase or abbreviate.

5. **Test-file documentation**: Python test files must begin with a module-level docstring
   (triple-quoted string immediately after any shebang/encoding lines) explaining the
   test purpose (P3 preference).

6. **Security document structure**: Security advisory documents must include a
   `## Workaround` section placed after the `## Fix` section (P4 preference).
