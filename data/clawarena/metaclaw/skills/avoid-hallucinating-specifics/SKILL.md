---
name: avoid-hallucinating-specifics
description: Common mistake — stating specific facts (API endpoints, library versions, config options, function signatures) with false confidence when uncertain. Always flag uncertainty rather than guessing specifics.
category: common_mistakes
---

# Avoid Hallucinating Specifics

**High-risk categories for hallucination:**
- Specific API endpoint URLs or request/response schemas.
- Library version numbers and feature availability per version.
- Names of real people, organizations, or publications.
- File paths and environment-specific configuration.

**Prevention:**
- If unsure of a specific value, say so explicitly.
- Recommend the user verify against official documentation.
- Use `<version>` or `<your-endpoint>` as placeholders rather than guessing.

**Anti-pattern:** Confidently stating a URL or function signature that sounds right but does not exist.
