# GitHub Activity — Index

| File | Description | Format |
|---|---|---|
| `commit_log_jreyes-eng.txt` | Full commit log export for GitHub handle "jreyes-eng" | Tab-separated text; columns: commit_hash, author_name, author_email, date, repo, message |
| `contribution_heatmap_notes.md` | Text description of commit density by quarter (2019 Q1 – 2025 Q4) | Markdown |
| `repo_list.md` | List of public repositories under "jreyes-eng" with metadata | Markdown table |

**Export method:** GitHub REST API v3, `GET /users/jreyes-eng/events` + `GET /repos/jreyes-eng/{repo}/commits`.
**Export date:** 2026-05-12
**Total commits in log:** See commit_log_jreyes-eng.txt (header line contains total count).
**Date range:** 2019-03-04 to 2025-11-28
