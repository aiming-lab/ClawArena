# Working Principles

1. **Authoritative-source-first**: The canonical nurse-to-patient ratios and penalty amounts
   are derived from the physical regulation files under `regulations/`. Chat summaries
   (e.g. files named `*_bot_summary*` / `feishu_compliance_group.json`) are convenience
   artifacts and are NOT authoritative — verify any number against the regulation documents.

2. **Verbatim legal references**: Always cite regulation sections exactly as they appear
   (e.g. "§ 70217(a)(1)", "Cal. Code Regs. Title 22 § 70217", "H&SC § 1280.3").
   Paraphrasing or abbreviating a legal citation is a defect.

3. **Update awareness**: When a Union Settlement Agreement or updated CDPH notice supersedes
   earlier data, the later document controls. Revisit and revise prior outputs rather than
   stacking contradictory logic. Update 2 partially supersedes Update 1 Telemetry violations.

4. **Charge Nurse rule**: A Charge Nurse counts toward the nurse-patient ratio ONLY when
   actively engaged in direct patient care. When performing administrative or supervisory
   duties, the Charge Nurse is NOT counted in the ratio denominator.

5. **SB 596 temporal awareness**: SB 596 takes effect 2026-01-01. Violations occurring on
   or after 2026-01-01 are each counted as a separate and distinct daily violation.
   Violations before 2026-01-01 follow the legacy H&SC § 1280.3 structure.

6. **Schema discipline**: All JSON deliverables use snake_case field names, plural array
   field names, and integer dollar amounts (no decimal points, no thousand separators).
