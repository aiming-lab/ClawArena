---
name: debug-systematically
description: Use this skill when diagnosing a bug, unexpected behavior, test failure, or any situation where code does not behave as expected. Follow a structured debugging process instead of randomly changing code.
category: coding
---

# Debug Systematically

**Process:**
1. **Reproduce** the bug with the smallest possible input.
2. **Isolate** — narrow down which component/function causes it.
3. **Hypothesize** — form a specific, falsifiable hypothesis.
4. **Test** — verify or disprove the hypothesis with a minimal experiment.
5. **Fix** — address the root cause, not just the symptom.
6. **Verify** — re-run the failing test and related tests.

**Useful tools:** `print`/`logging`, `pdb`/`ipdb`, unit tests, `git bisect`.

**Anti-patterns:**
- Changing multiple things at once and not knowing what fixed it.
- Ignoring related test failures.
- Commenting out code instead of understanding it.
