# Working Principles

1. **Authoritative-source-first**: The canonical reference for GitHub Actions syntax is the
   official GitHub documentation (https://docs.github.com). For GitLab CI, use
   https://docs.gitlab.com/ci/yaml/. Auto-generated bot summaries and chat messages may
   contain errors — always verify against official sources or the actual config files.

2. **Verbatim field names**: Use exact YAML field names and values as documented
   (e.g. `id-token: write`, `optional: true`, `policy: pull`). Never abbreviate or paraphrase.

3. **Schema discipline**: Every JSON deliverable carries a top-level `schema_version` field
   set to `"1.0"`. All JSON field names use snake_case (never camelCase).

4. **Backup before modify**: Before modifying any configuration file, back it up in the same
   directory with a `.bak` suffix (e.g., `ci.yml` → `ci.yml.bak`).

5. **Stage-split discipline**: GitLab CI configurations must be organized by stage into
   separate include files under `.gitlab/ci/`. Do not consolidate all jobs into root
   `.gitlab-ci.yml`.

6. **Documentation style**: All Markdown documents use bilingual headings at level 1 and 2:
   format is `# 中文标题 / English Title`.

7. **Script versioning**: All Python scripts carry a version comment in the header:
   format is `# version: X.Y`.

8. **Temporal awareness**: When an Update or corrected instruction supersedes an earlier one,
   the later instruction wins — always revise prior outputs rather than stacking contradictions.
