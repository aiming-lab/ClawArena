---
name: do-not-retry-without-diagnosis
description: Common mistake — retrying the same failing command or API call without understanding why it failed. Always diagnose the root cause before retrying anything.
category: common_mistakes
---

# Do Not Retry Without Diagnosis

**Mistake pattern:** Tool call fails → retry the same call → fails again → repeat.

**Fix:** After the first failure, read the error message carefully and diagnose the root cause before retrying.

**Questions to ask:**
- Is this a transient error (network timeout, rate limit)? Retry with backoff.
- Is this a permanent error (wrong input, missing resource, permission denied)? Fix the cause.

**Anti-pattern:** Blindly retrying or escalating without examining the error output.
