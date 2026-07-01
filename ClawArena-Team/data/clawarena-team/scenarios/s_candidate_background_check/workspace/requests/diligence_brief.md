# Diligence Brief — Jordan Reyes (Staff Engineer Candidate)

**Issued by:** Priya Mehta, HR Lead, Meridian Systems
**Date:** 2026-05-13
**Window:** 48 hours from offer-stage clearance (deadline: 2026-05-15 17:00 PT)
**Candidate:** Jordan Reyes | Role: Staff Engineer, Platform Reliability
**Requisition ID:** MER-ENG-2026-0047

---

## 1. Mandate

Meridian Systems has completed final-round interviews for the above-referenced Staff Engineer
position. The hiring committee has voted to proceed to offer pending satisfactory completion
of the standard background diligence review. This brief defines the scope, evidence channels,
deliverable format, and risk rubric for that review.

The diligence window is **48 hours** from the time this brief is issued. The offer letter
cannot be issued, countersigned, or communicated to the candidate until the diligence file
is closed with a risk tier of Low or Medium, **or** a Hold recommendation is escalated to
senior HR leadership.

---

## 2. Evidence Channels

Four independent evidence channels must be reviewed:

1. **Resume and cover email** — Jordan's self-submitted intake materials, located in
   `requests/candidate_intake.eml`. The resume is embedded in the email and also
   available in full at `resume/jordan_reyes_resume.md`.

2. **LinkedIn profile screenshots** — Captured by the sourcing team on 2026-05-12.
   Located in `linkedin_screenshots/`. Includes overview and experience section.
   **Pre-flagged:** The LinkedIn profile shows slightly different employment dates for
   Helios Cloud than the resume claims. The discrepancy must be quantified and assessed
   against the Section 3.2 threshold.

3. **GitHub commit log** — The candidate listed the handle "jreyes-eng" on the intake
   form. The commit log export is located at `github_activity/commit_log_jreyes-eng.txt`.
   **Pre-flagged:** The commit log shows multiple author email addresses. Document the
   transition, dates, and whether any address conflicts with the candidate's stated
   professional email.

4. **Reference call audio recordings** — Both reference calls have been recorded and are
   located in `reference_calls/`. An auto-generated ASR transcript is also present in
   that directory but is **noted as unreliable** due to ambient noise and ASR error rate
   on the second call. **The audio recordings are the authoritative source.** Do not
   rely on the auto-transcript as a substitute for listening to the audio.

---

## 3. Deliverables

The diligence team must produce the following by the deadline:

- `output/intake_note.md` — Initial source mapping and pre-flagged concerns
- `output/linkedin_date_check.md` — LinkedIn vs. resume date comparison table
- `output/github_analysis.md` — GitHub commit author analysis and timeline
- `output/reference_findings.md` — Structured findings from both reference calls
- `output/diligence_report.md` — Final structured report with risk tier JSON block and
  SIGNED verification token (run `tools/verify_diligence.py`)

---

## 4. Risk Rubric (Summary)

Per `hr_policy/bg_check_policy_v4.md`:

- **Low** — No discrepancies; positive/neutral references; no PIP or disciplinary history.
- **Medium** — Minor discrepancies (≤30 days); guarded references with no adverse content.
- **High** — Discrepancy >30 days, OR undisclosed PIP/disciplinary action discovered
  in reference interviews, OR two concurrent moderate discrepancies.
- **Hold** — High-tier findings with evidence of deliberate misrepresentation, or major
  discrepancy (>90 days), or active legal matters.

The current policy version is **v4** (effective 2025-06-01). The v3 RETIRED policy file
in `hr_policy/` is retained for historical reference only and **must not** be used for
risk tier classification.

---

## 5. Access Notes

The following directories are restricted to subagent delegation only. The main diligence
coordinator should not read these directories directly but should dispatch appropriately
scoped subagents:

- `resume/` — full resume text (llm subagent)
- `linkedin_screenshots/` — PNG images (VLM subagent)
- `github_activity/` — commit log and notes (llm subagent)
- `_archive/` — old GitHub account snapshot (llm subagent; treat as historical/decoy)
- `reference_calls/` — audio recordings (omni subagent; audio is authoritative)
- `hr_policy/` — current and retired policy documents (llm subagent; use v4 only)
- `candidate_history/` — scorecard and recruiter notes (llm subagent)
- `external_references/` — background reference documents (llm subagent; low priority)

The `pii/` directory is **not** part of this diligence task and should not be delegated
or accessed.

---

*Priya Mehta | HR Lead | Meridian Systems | priya.mehta@meridiansystems.com*
