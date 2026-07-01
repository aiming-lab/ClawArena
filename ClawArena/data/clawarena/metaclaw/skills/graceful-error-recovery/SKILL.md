---
name: graceful-error-recovery
description: Use this skill when a tool call, command, or API request fails. Diagnose the root cause systematically before retrying or changing approach. Do not retry the same failing call without first understanding why it failed.
category: general
---

# Graceful Error Recovery

When something fails, diagnose before retrying.

**Process:**
1. Read the full error message — do not skip the stack trace.
2. Identify the root cause: typo, missing dependency, permission, network, logic bug?
3. Fix the root cause, not just the symptom.
4. If the fix is uncertain, try the simplest hypothesis first.
5. If two retries fail, step back and consider an alternative approach.

**Anti-patterns:**
- Retrying the same failed call in a loop.
- Swallowing errors silently with bare `except: pass`.
- Blaming the environment before checking your own code.
