---
name: input-validation-and-sanitization
description: Use this skill when implementing any endpoint, form handler, CLI tool, or function that accepts external input. Validate and sanitize all untrusted data before processing — never assume input is safe.
category: security
---

# Input Validation and Sanitization

**Validation principles:**
- Validate at the system boundary (API layer, form handler) — not deep in business logic.
- Validate type, range, length, and format explicitly.
- Reject unexpected input by default (allowlist > denylist).

**SQL injection prevention:** Always use parameterized queries or an ORM.

**XSS prevention:** Escape HTML output; use Content-Security-Policy headers; avoid `innerHTML` with user data.

**Path traversal prevention:** Resolve paths to canonical form and verify they are under the expected directory.

```python
import os
base = '/allowed/dir'
canonical = os.path.realpath(os.path.join(base, user_input))
assert canonical.startswith(base + os.sep)
```
