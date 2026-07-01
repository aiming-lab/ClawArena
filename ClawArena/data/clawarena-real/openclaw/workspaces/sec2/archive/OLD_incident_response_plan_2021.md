# NovaBridge Incident Response Plan — 2021 Edition

**STATUS: DEPRECATED AND SUPERSEDED**
**This document was superseded by `policies/incident_response_plan.md` in 2023.**
**DO NOT reference this document for current procedures.**

---

## ARCHIVED CONTENT (Historical Reference Only)

### AWS Key Containment (2021 — OUTDATED)
- For any compromised AWS key: revoke immediately via root account
- Key prefix identification: NOT documented in this version
- STS credential handling: NOT covered in 2021 edition (added in 2023 policy)

### GitHub Secret Scanning (2021 — OUTDATED)
- GitHub Secret Scanning was not yet widely available in 2021
- This plan does not address GitHub SS alert fields
- Validity enum values were not documented in this version

### Remediation Timeline (2021 — OUTDATED)
- Old target: revoke secrets within 24 hours of detection
- [Superseded by current policy: initiate containment within 1 hour]

### CircleCI Reference (2021 — OUTDATED)
- The CircleCI supply chain incident of January 2023 postdates this document
- Do NOT use this archive for CircleCI incident dates or SHA256 values

---

*This file is retained for historical audit purposes only.*
*All operational procedures must use the current 2023+ policies.*
