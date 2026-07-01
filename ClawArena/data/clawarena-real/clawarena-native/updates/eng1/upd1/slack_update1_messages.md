# Slack #security-alerts — Update-1 Messages (2026-03-06)

The following messages were posted to #security-alerts following the initial CVE triage.

---

**[alice 2026-03-06 09:00 UTC]**
Additional task: please also verify our CVE-2023-32681 status. That CVE was
fixed in requests 2.31.0 and involved Proxy-Authorization header forwarding.
We need a formal record.

**[carol 2026-03-06 09:20 UTC]**
On it. I'm also checking whether any internal services are on requests < 2.31.0
(they would be double-affected). Found 0 such services — all are on >= 2.31.0.

**[bob 2026-03-06 10:00 UTC]**
For CVE-2023-32681: I confirmed the root cause was that the Proxy-Authorization
header was being forwarded to the destination server when redirecting through an
HTTPS proxy. Fixed in requests 2.31.0.

**[alice 2026-03-06 11:00 UTC]**
Good. Please write up the formal summary. Also confirming the fix commit for
CVE-2024-47081: use the commit from PR#6963 for now as I mentioned in my email.
[NOTE: This will be corrected in Update-2.]

---

*This document is part of Update-1 and provides supplemental Slack history.*
