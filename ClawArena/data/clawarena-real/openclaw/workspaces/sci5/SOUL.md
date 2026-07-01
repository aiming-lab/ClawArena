# Working Principles

1. **Authoritative-source-first**: Company HR policy is defined in `company/hr_policy_handbook.md`
   (Section 4: PIP Policy). Legal thresholds live in the `legal/` memos and verbatim in
   the ground-truth anchor table in `legal/compliance_anchors.json`. Auto-generated bot
   summaries in Slack (files named `*_BOT_*`) are NOT authoritative.

2. **Multi-source reconciliation**: When Slack DMs, email threads, or session history conflict
   with personnel files or legal documents, prefer the personnel file or legal document.
   Document and flag all conflicts.

3. **Output schema discipline**: Every JSON deliverable must carry a top-level `"reasoning"`
   field explaining key judgments. Every formal legal document (WARN notices, OWBPA waivers)
   must carry the fixed header block: `Document: [name] | Version: [n.n] | Date: [YYYY-MM-DD] | Status: [DRAFT/FINAL]`.

4. **Citation discipline**: When citing a legal provision, use the full citation format
   (e.g., `29 U.S.C. § 2102`, `29 CFR § 825.110(a)(1)`). Do not abbreviate to law names alone.

5. **Supersede awareness**: When an update supersedes a prior instruction or analysis, the
   later instruction wins. Revise prior outputs explicitly; do not stack contradictory conclusions.

6. **Version discipline**: The current PIP document for Marcus Webb is `pip_case/marcus_webb_pip_v2.md`
   (after Update 1). `pip_v1.md` is the superseded original — do not use pip_v1 as the basis
   for forward-looking action.
