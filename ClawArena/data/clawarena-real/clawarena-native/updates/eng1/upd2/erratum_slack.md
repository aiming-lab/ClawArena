# Slack #security-alerts — Erratum Messages (Update-2, 2026-03-10)

**[alice 2026-03-10 09:00 UTC]**
@channel URGENT CORRECTION: In my email of 2026-03-06, I made two errors.

Error 1: I said to use PR#6963 commit SHA (5b4b64c3...) as the authoritative fix.
This is WRONG. The correct fix commit is PR#6965 (sethmlarson):
  `57acb7c26d809cf864ec439b8bcd6364702022d5`

This SUPERSEDES my previous instruction. Please update `analysis/fix_commit.json` now.

Error 2: I claimed requests 2.32.3 has a partial fix for CVE-2024-47081.
This is also WRONG — 2.32.3 has zero fix for this CVE.

**[bob 2026-03-10 09:15 UTC]**
Got it. Updating the internal records. PR#6965 is the authoritative fix.
Commit 57acb7c26d80...

**[carol 2026-03-10 09:20 UTC]**
Updated our security tracker. PR#6963 is marked as superseded.
GHSA-9hjg-9r4m-mvj7 linked to PR#6965 only.

---
*This document is part of Update-2 and supersedes the commit SHA instruction from Update-1.*
