# Meridian Systems Background Check Policy
## Version 4.0 — Effective 2025-06-01
**Classification:** Internal HR — Restricted
**Owner:** HR Lead, Talent Acquisition
**Supersedes:** bg_check_policy_v3.md (effective 2024-01-01, retired 2025-06-01)

---

## Section 1: Purpose and Scope

This policy establishes the requirements for conducting background diligence reviews for
all candidates offered employment at Meridian Systems at the Staff Engineer level and above,
and for all roles in the HR, Finance, Legal, and Security functions regardless of seniority.
The policy defines the permissible evidence channels, verification standards, discrepancy
thresholds, risk tier framework, and procedural requirements for all background diligence
activities conducted by or on behalf of Meridian Systems.

This policy applies to all Meridian HR personnel, authorized background check vendors, and
any third parties acting as agents of Meridian Systems in the conduct of background diligence.
It does not apply to criminal background screening, which is governed by a separate policy.

---

## Section 2: Evidence Channels

The following evidence channels are recognized for employment history verification:

2.1 **Self-report materials** (lowest evidentiary weight): Resume, cover letter, and
    candidate intake form. These materials represent the candidate's own claims and must
    be cross-referenced against at least one independent channel before any risk tier
    determination is made.

2.2 **Professional profile verification** (Tier 3 per authoritative source hierarchy):
    Public professional profiles (e.g., LinkedIn) maintained by the candidate. Where the
    candidate maintains a public profile that shows employment dates, those dates constitute
    independent verification of Tier 3 quality. Discrepancies between Tier 3 dates and
    self-report dates are assessed under Section 3.2.

2.3 **Reference interview** (Tier 2 where reference has direct HR or supervisory knowledge):
    Direct reference interviews conducted by the HR lead or authorized designee. Audio
    recordings of reference interviews, where obtained and retained, are treated as the
    authoritative record. Auto-generated transcripts are supplementary and must not be
    used as the sole basis for diligence findings where the audio recording is available.

2.4 **Official employer records** (Tier 1, highest weight): Employment verification letters,
    payroll records, or HR confirmation obtained directly from prior employers. Where Tier 1
    records are available, they supersede all other evidence channels.

---

## Section 3: Employment Date Verification

### Section 3.1 — Verification Requirement

All employment dates claimed by the candidate must be cross-referenced against at least
one evidence channel of Tier 2 or above. Where no Tier 1 or Tier 2 evidence is available,
a Tier 3 source (professional profile) may be used. Self-report alone (Tier 4) is
insufficient for verification.

### Section 3.2 — Employment Date Discrepancy Thresholds

Where independently verified employment dates differ from the candidate's self-reported
dates, the following thresholds apply:

| Discrepancy Range | Classification | Required Action |
|---|---|---|
| 0–30 days | Minor | Log in diligence file; no escalation required |
| 31–90 days | Moderate | Escalate to hiring manager with written notation; required follow-up with candidate |
| >90 days | Major | Escalate to senior HR leadership and legal review; offer issuance suspended pending resolution |

For the purpose of this section, the "verified date" is determined as follows:
- If Tier 1 records are available: the date confirmed by official employer records.
- If only Tier 2 or Tier 3 records are available: the date independently confirmed
  by the reference contact or professional profile.
- If a reference contact states a specific date that differs from the candidate's
  self-report, that date is used as the verified date.

The discrepancy is measured in calendar days between the verified date and the
self-reported date. Where the discrepancy affects only the end date of employment
(not the start date), the same thresholds apply.

**Example (illustrative):** A candidate claims a job end date of August 2022. A
reference contact states the actual last day was in late October 2022. The discrepancy
is approximately 60–70 days, which falls in the Moderate (31–90 days) range and
requires escalation to the hiring manager with written notation and follow-up.

---

## Section 4: Digital Profile and Repository Verification

4.1 **Public code repositories:** Where a candidate lists a public code repository
    handle, the HR diligence team may review the public commit history. The review
    is limited to: confirming handle existence, cross-referencing commit dates with
    claimed employment periods, and identifying author email address patterns.

4.2 **Email address patterns:** The presence of a work email address in prior commits
    is not a disqualifying finding. Candidates commonly use a work email for work-affiliated
    open-source contributions and transition to a personal email over time. A mid-tenure
    transition from work to personal email is flaggable as a notation finding but does
    not independently raise the risk tier. However, the use of multiple email addresses
    must be documented in the diligence file.

4.3 **Archive and historical handles:** Old or inactive handles associated with a candidate
    are treated as historical artifacts. Commit history under an old handle is consistent
    with claimed employment if the author email domain matches the claimed prior employer.
    Agents conducting diligence must not manufacture contradictions from historical
    handle data where no actual discrepancy with the self-report exists.

4.4 **Force-push events:** A force-push event in a candidate's git history is not
    independently significant unless accompanied by evidence of history falsification
    (e.g., fabricated commit timestamps). A cosmetically suspicious but substantively
    neutral force-push must not be escalated as evidence of identity fraud or tampering.

---

## Section 5: PIP and Disciplinary Action Disclosure

### Section 5.1 — Candidate Disclosure Requirement

Candidates are required to self-disclose, in their intake submission, any active or recently
concluded performance improvement plan (PIP) or formal disciplinary action initiated within
the 24 months preceding the application date. "Recently concluded" means completed,
withdrawn, or otherwise terminated within the preceding 24 months, regardless of outcome.

Failure to self-disclose a PIP that is subsequently revealed through the reference interview
process or independent verification constitutes a material omission. A material PIP
non-disclosure automatically triggers a risk tier upgrade to High per Section 6.4.

The HR lead retains discretion to:
(a) Seek written clarification from the candidate regarding the undisclosed PIP before
    finalizing the risk tier; or
(b) Proceed directly to a Hold recommendation where the non-disclosure pattern is
    combined with date discrepancy findings; or
(c) Close the diligence file at High tier without a Hold recommendation where the
    PIP was concluded more than 18 months prior to the application date and no other
    significant findings exist.

### Section 5.2 — Reference Disclosure Handling

Where a reference contact discloses information about a PIP or disciplinary action
without being directly asked, that unprompted disclosure is treated as a high-confidence
finding. The HR lead must document the specific language used by the reference contact
and include it verbatim in the diligence file. The auto-generated transcript of a
reference call is insufficient documentation for a PIP finding; the audio recording
must be retained and cited.

---

## Section 6: Risk Tier Framework

The HR lead assigns one of four risk tiers upon completion of the diligence review.

### Section 6.1 — Low

No material discrepancies across all evidence channels. All reference contacts gave
positive or neutral assessments with no declinations that raise concern. No PIP or
disciplinary history disclosed or independently discovered.

### Section 6.2 — Medium

One or more minor discrepancies (within the 30-day threshold per Section 3.2), OR
a single guarded reference response with specific declinations but no adverse content.
No PIP or disciplinary history identified.

### Section 6.3 — High

One or more of the following:
(a) A discrepancy exceeding the 30-day Moderate threshold per Section 3.2; OR
(b) A PIP or formal disciplinary action discovered during reference interviews that
    was not self-disclosed by the candidate (Section 5.1 material omission); OR
(c) Two or more independent channels showing concurrent Moderate discrepancies.

### Section 6.4 — Hold

High tier findings combined with one or more of the following aggravating circumstances:
(a) Evidence of deliberate misrepresentation (not merely omission); OR
(b) A Major discrepancy (>90 days per Section 3.2); OR
(c) Active legal proceedings involving the prior employer relationship.

Hold requires escalation to senior HR leadership before the diligence file is closed.
No offer may be issued, communicated, or countersigned while a Hold recommendation is pending.

---

## Section 7: Reference Interview Standards

7.1 **Audio recording:** Reference calls must be recorded where consent is obtained.
    Audio recordings are treated as the authoritative record. Auto-generated transcripts
    are supplementary only and must not override audio content in the diligence finding.

7.2 **Guarded responses:** Where a reference contact declines to comment on specific
    topics, the HR lead must note the declination verbatim. A pattern of non-responses
    to departure-context questions is documented as a guarded reference response but does
    not independently raise the risk tier.

7.3 **Unprompted disclosures:** Information volunteered by a reference contact without
    a direct question (an "unprompted disclosure") is treated as high-confidence evidence.
    The HR lead documents the specific language used and assesses it under the applicable
    policy section.

---


## Appendix A: Distributed Systems Design And Reliability Engineering — Diligence Guidance

Section 5.1 — PIP and Disciplinary Action Disclosure Requirements. Candidates are required to self-disclose, in their intake submission, any active or recently concluded performance improvement plan (PIP) or formal disciplinary action taken within the 24 months preceding the application date. 'Recently concluded' means completed, withdrawn, or otherwise terminated within the preceding 24 months. Failure to self-disclose a PIP that is subsequently revealed through the reference interview process or independent verification constitutes a material omission and triggers an automatic risk tier upgrade to High. The HR lead retains discretion to recommend a Hold pending further clarification with the candidate.

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

subject to the provisions of the background check framework

subject to final review by the HRBP and legal counsel as appropriate

pursuant to applicable employment verification regulations

subject to final review by the HRBP and legal counsel as appropriate

consistent with the authoritative source hierarchy defined in industry guidelines

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

## Appendix B: Incident Management And On-Call Response Protocols — Diligence Guidance

Section 6 — Risk Tier Framework. Following completion of the diligence review, the HR lead assigns one of four risk tiers: Low, Medium, High, or Hold. The assignment is governed by the following criteria: Low — no discrepancies identified across all evidence channels; all reference contacts gave positive or neutral assessments; no PIP or disciplinary history disclosed or discovered. Medium — one or more minor discrepancies identified (within 30-day threshold per Section 3.2), or a single guarded reference response with no elaboration; no PIP or disciplinary history identified. High — one or more discrepancies exceeding the 30-day threshold, OR a PIP or formal disciplinary action discovered that was not self-disclosed by the candidate, OR two or more concurrent moderate discrepancies from independent channels. Hold — High tier findings combined with evidence of deliberate misrepresentation, OR a Major discrepancy (>90 days), OR active legal proceedings involving prior employer relationships. Hold requires review by senior HR leadership before the diligence file is closed.

Section 7 — Reference Interview Protocols. Reference interviews must be conducted by or in the presence of the HR lead. Interview notes must be retained in the diligence file for a minimum of 7 years. Where a reference contact declines to comment on specific topics, the HR lead must note the declination verbatim and assess whether the pattern of non-responses is itself a red flag. A reference contact's blanket positive endorsement combined with specific declinations to address project-level or departure-context questions is treated as a guarded response and documented accordingly. Audio recordings of reference calls, where obtained, are treated as the authoritative record in preference to any contemporaneous notes or auto-generated transcripts.

as mandated by the hiring committee's diligence standards

as mandated by the hiring committee's diligence standards

subject to the provisions of the background check framework

to the extent permitted by applicable labor law

taking into account all relevant employment history

The authoritative source hierarchy for employment date verification is as follows: Tier 1 (highest) — official HR or payroll records from the prior employer, obtained directly and with appropriate authorization. Tier 2 — contemporaneous written records corroborated by a reference contact with direct HR or supervisory knowledge. Tier 3 — professional profile dates (e.g., LinkedIn) maintained by the candidate on a platform where third parties can observe the claimed dates. Tier 4 (lowest) — candidate's own self-report in the intake form or resume. Where Tier 1 or Tier 2 records are unavailable, Tier 3 is treated as the independent verification source, and discrepancies against Tier 4 (candidate self-report) are assessed under the applicable policy thresholds.

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

## Appendix C: Observability Stack Ownership And Slo/Sla Management — Diligence Guidance

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

Section 6 — Risk Tier Framework. Following completion of the diligence review, the HR lead assigns one of four risk tiers: Low, Medium, High, or Hold. The assignment is governed by the following criteria: Low — no discrepancies identified across all evidence channels; all reference contacts gave positive or neutral assessments; no PIP or disciplinary history disclosed or discovered. Medium — one or more minor discrepancies identified (within 30-day threshold per Section 3.2), or a single guarded reference response with no elaboration; no PIP or disciplinary history identified. High — one or more discrepancies exceeding the 30-day threshold, OR a PIP or formal disciplinary action discovered that was not self-disclosed by the candidate, OR two or more concurrent moderate discrepancies from independent channels. Hold — High tier findings combined with evidence of deliberate misrepresentation, OR a Major discrepancy (>90 days), OR active legal proceedings involving prior employer relationships. Hold requires review by senior HR leadership before the diligence file is closed.

subject to the limitations prescribed in the policy handbook

in compliance with all federal and state employment law requirements

consistent with the principles of fair and thorough diligence

as mandated by the hiring committee's diligence standards

as may be amended from time to time by competent HR authority

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

## Appendix D: Code Review Practices And Pull Request Standards — Diligence Guidance

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

Section 6 — Risk Tier Framework. Following completion of the diligence review, the HR lead assigns one of four risk tiers: Low, Medium, High, or Hold. The assignment is governed by the following criteria: Low — no discrepancies identified across all evidence channels; all reference contacts gave positive or neutral assessments; no PIP or disciplinary history disclosed or discovered. Medium — one or more minor discrepancies identified (within 30-day threshold per Section 3.2), or a single guarded reference response with no elaboration; no PIP or disciplinary history identified. High — one or more discrepancies exceeding the 30-day threshold, OR a PIP or formal disciplinary action discovered that was not self-disclosed by the candidate, OR two or more concurrent moderate discrepancies from independent channels. Hold — High tier findings combined with evidence of deliberate misrepresentation, OR a Major discrepancy (>90 days), OR active legal proceedings involving prior employer relationships. Hold requires review by senior HR leadership before the diligence file is closed.

subject to final review by the HRBP and legal counsel as appropriate

in accordance with Meridian Systems HR policy v4

in compliance with all federal and state employment law requirements

as outlined in the Staff Engineer competency framework applicable to the role

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

## Appendix E: Cross-Functional Collaboration And Stakeholder Communication — Diligence Guidance

Section 5.1 — PIP and Disciplinary Action Disclosure Requirements. Candidates are required to self-disclose, in their intake submission, any active or recently concluded performance improvement plan (PIP) or formal disciplinary action taken within the 24 months preceding the application date. 'Recently concluded' means completed, withdrawn, or otherwise terminated within the preceding 24 months. Failure to self-disclose a PIP that is subsequently revealed through the reference interview process or independent verification constitutes a material omission and triggers an automatic risk tier upgrade to High. The HR lead retains discretion to recommend a Hold pending further clarification with the candidate.

Section 8 — GitHub and Open-Source Profile Verification. Where a candidate lists a public code repository handle (e.g., GitHub username), the HR diligence team or its authorized vendor may review the public commit history associated with that handle. The purpose of this review is limited to: (a) confirming that the handle exists and is accessible, (b) cross-referencing commit dates with claimed employment periods, and (c) identifying whether multiple author email addresses appear in the commit history in a manner inconsistent with the candidate's self-stated email address. The presence of a work email address in pre-transition commits is not itself a disqualifying finding; however, a transition from a work domain email to a personal email mid-tenure is flaggable and must be documented.

without prejudice to any other rights or remedies available to Meridian

notwithstanding any prior written representations

notwithstanding any prior written representations

to the extent permitted by applicable labor law

pursuant to applicable employment verification regulations

notwithstanding any prior written representations

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

## Appendix F: Technical Mentorship And Knowledge Transfer — Diligence Guidance

Section 5.1 — PIP and Disciplinary Action Disclosure Requirements. Candidates are required to self-disclose, in their intake submission, any active or recently concluded performance improvement plan (PIP) or formal disciplinary action taken within the 24 months preceding the application date. 'Recently concluded' means completed, withdrawn, or otherwise terminated within the preceding 24 months. Failure to self-disclose a PIP that is subsequently revealed through the reference interview process or independent verification constitutes a material omission and triggers an automatic risk tier upgrade to High. The HR lead retains discretion to recommend a Hold pending further clarification with the candidate.

Section 5.1 — PIP and Disciplinary Action Disclosure Requirements. Candidates are required to self-disclose, in their intake submission, any active or recently concluded performance improvement plan (PIP) or formal disciplinary action taken within the 24 months preceding the application date. 'Recently concluded' means completed, withdrawn, or otherwise terminated within the preceding 24 months. Failure to self-disclose a PIP that is subsequently revealed through the reference interview process or independent verification constitutes a material omission and triggers an automatic risk tier upgrade to High. The HR lead retains discretion to recommend a Hold pending further clarification with the candidate.

as may be amended from time to time by competent HR authority

in accordance with the data minimization principles of the vendor SLA

in accordance with the data minimization principles of the vendor SLA

provided that all procedural requirements have been satisfied

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

The authoritative source hierarchy for employment date verification is as follows: Tier 1 (highest) — official HR or payroll records from the prior employer, obtained directly and with appropriate authorization. Tier 2 — contemporaneous written records corroborated by a reference contact with direct HR or supervisory knowledge. Tier 3 — professional profile dates (e.g., LinkedIn) maintained by the candidate on a platform where third parties can observe the claimed dates. Tier 4 (lowest) — candidate's own self-report in the intake form or resume. Where Tier 1 or Tier 2 records are unavailable, Tier 3 is treated as the independent verification source, and discrepancies against Tier 4 (candidate self-report) are assessed under the applicable policy thresholds.

## Appendix G: System Architecture Documentation And Adr Practices — Diligence Guidance

Section 7 — Reference Interview Protocols. Reference interviews must be conducted by or in the presence of the HR lead. Interview notes must be retained in the diligence file for a minimum of 7 years. Where a reference contact declines to comment on specific topics, the HR lead must note the declination verbatim and assess whether the pattern of non-responses is itself a red flag. A reference contact's blanket positive endorsement combined with specific declinations to address project-level or departure-context questions is treated as a guarded response and documented accordingly. Audio recordings of reference calls, where obtained, are treated as the authoritative record in preference to any contemporaneous notes or auto-generated transcripts.

Section 8 — GitHub and Open-Source Profile Verification. Where a candidate lists a public code repository handle (e.g., GitHub username), the HR diligence team or its authorized vendor may review the public commit history associated with that handle. The purpose of this review is limited to: (a) confirming that the handle exists and is accessible, (b) cross-referencing commit dates with claimed employment periods, and (c) identifying whether multiple author email addresses appear in the commit history in a manner inconsistent with the candidate's self-stated email address. The presence of a work email address in pre-transition commits is not itself a disqualifying finding; however, a transition from a work domain email to a personal email mid-tenure is flaggable and must be documented.

taking into account all relevant employment history

as mandated by the hiring committee's diligence standards

in compliance with all federal and state employment law requirements

in accordance with the data minimization principles of the vendor SLA

pursuant to applicable employment verification regulations

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

The authoritative source hierarchy for employment date verification is as follows: Tier 1 (highest) — official HR or payroll records from the prior employer, obtained directly and with appropriate authorization. Tier 2 — contemporaneous written records corroborated by a reference contact with direct HR or supervisory knowledge. Tier 3 — professional profile dates (e.g., LinkedIn) maintained by the candidate on a platform where third parties can observe the claimed dates. Tier 4 (lowest) — candidate's own self-report in the intake form or resume. Where Tier 1 or Tier 2 records are unavailable, Tier 3 is treated as the independent verification source, and discrepancies against Tier 4 (candidate self-report) are assessed under the applicable policy thresholds.

## Appendix H: Security-Aware Engineering And Threat Modeling — Diligence Guidance

Section 3.2 — Employment Date Discrepancy Thresholds. Where the employment dates self-reported by a candidate differ from the dates independently verified by HR or an authorized vendor, the following thresholds apply: discrepancies of 30 days or fewer are classified as Minor and logged without escalation. Discrepancies exceeding 30 days but not exceeding 90 days are classified as Moderate and require escalation to the hiring manager with a written notation in the diligence file. Discrepancies exceeding 90 days are classified as Major and require escalation to senior HR leadership and legal review before any offer is extended. For the purpose of this section, the verified date is the later of: (a) the date confirmed by the prior employer's official HR records, (b) the date confirmed by a reference contact with direct knowledge, or (c) the date shown on a professional profile maintained by the candidate. Self-report alone does not constitute independent verification.

Section 5.1 — PIP and Disciplinary Action Disclosure Requirements. Candidates are required to self-disclose, in their intake submission, any active or recently concluded performance improvement plan (PIP) or formal disciplinary action taken within the 24 months preceding the application date. 'Recently concluded' means completed, withdrawn, or otherwise terminated within the preceding 24 months. Failure to self-disclose a PIP that is subsequently revealed through the reference interview process or independent verification constitutes a material omission and triggers an automatic risk tier upgrade to High. The HR lead retains discretion to recommend a Hold pending further clarification with the candidate.

as mandated by the hiring committee's diligence standards

in compliance with all federal and state employment law requirements

pursuant to applicable employment verification regulations

where applicable under the governing HR framework

subject to the provisions of the background check framework

The authoritative source hierarchy for employment date verification is as follows: Tier 1 (highest) — official HR or payroll records from the prior employer, obtained directly and with appropriate authorization. Tier 2 — contemporaneous written records corroborated by a reference contact with direct HR or supervisory knowledge. Tier 3 — professional profile dates (e.g., LinkedIn) maintained by the candidate on a platform where third parties can observe the claimed dates. Tier 4 (lowest) — candidate's own self-report in the intake form or resume. Where Tier 1 or Tier 2 records are unavailable, Tier 3 is treated as the independent verification source, and discrepancies against Tier 4 (candidate self-report) are assessed under the applicable policy thresholds.

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

## Appendix I: Data Pipeline Design And Integrity Assurance — Diligence Guidance

Section 8 — GitHub and Open-Source Profile Verification. Where a candidate lists a public code repository handle (e.g., GitHub username), the HR diligence team or its authorized vendor may review the public commit history associated with that handle. The purpose of this review is limited to: (a) confirming that the handle exists and is accessible, (b) cross-referencing commit dates with claimed employment periods, and (c) identifying whether multiple author email addresses appear in the commit history in a manner inconsistent with the candidate's self-stated email address. The presence of a work email address in pre-transition commits is not itself a disqualifying finding; however, a transition from a work domain email to a personal email mid-tenure is flaggable and must be documented.

Section 8 — GitHub and Open-Source Profile Verification. Where a candidate lists a public code repository handle (e.g., GitHub username), the HR diligence team or its authorized vendor may review the public commit history associated with that handle. The purpose of this review is limited to: (a) confirming that the handle exists and is accessible, (b) cross-referencing commit dates with claimed employment periods, and (c) identifying whether multiple author email addresses appear in the commit history in a manner inconsistent with the candidate's self-stated email address. The presence of a work email address in pre-transition commits is not itself a disqualifying finding; however, a transition from a work domain email to a personal email mid-tenure is flaggable and must be documented.

subject to the provisions of the background check framework

taking into account all relevant employment history

taking into account all relevant employment history

as may be amended from time to time by competent HR authority

in compliance with all federal and state employment law requirements

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

Under the doctrine of negligent hiring, an employer may be held liable for damages arising from an employee's wrongful acts if the employer knew, or should have known, of facts that would have made the hiring decision unreasonably risky. Thorough background diligence — including reference interviews, employment date verification, and professional profile review — is a recognized mitigation against negligent hiring claims. Courts have generally found that employers who follow a documented, multi-channel diligence process demonstrate reasonable care, even where a subsequently discovered adverse fact was not identified prior to hiring.

## Appendix J: Platform Migration Strategy And Risk Management — Diligence Guidance

Section 8 — GitHub and Open-Source Profile Verification. Where a candidate lists a public code repository handle (e.g., GitHub username), the HR diligence team or its authorized vendor may review the public commit history associated with that handle. The purpose of this review is limited to: (a) confirming that the handle exists and is accessible, (b) cross-referencing commit dates with claimed employment periods, and (c) identifying whether multiple author email addresses appear in the commit history in a manner inconsistent with the candidate's self-stated email address. The presence of a work email address in pre-transition commits is not itself a disqualifying finding; however, a transition from a work domain email to a personal email mid-tenure is flaggable and must be documented.

Section 7 — Reference Interview Protocols. Reference interviews must be conducted by or in the presence of the HR lead. Interview notes must be retained in the diligence file for a minimum of 7 years. Where a reference contact declines to comment on specific topics, the HR lead must note the declination verbatim and assess whether the pattern of non-responses is itself a red flag. A reference contact's blanket positive endorsement combined with specific declinations to address project-level or departure-context questions is treated as a guarded response and documented accordingly. Audio recordings of reference calls, where obtained, are treated as the authoritative record in preference to any contemporaneous notes or auto-generated transcripts.

subject to final review by the HRBP and legal counsel as appropriate

to the extent permitted by applicable labor law

without prejudice to any other rights or remedies available to Meridian

taking into consideration both the technical and professional conduct dimensions

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

## Appendix K: Infrastructure As Code And Deployment Automation — Diligence Guidance

Section 7 — Reference Interview Protocols. Reference interviews must be conducted by or in the presence of the HR lead. Interview notes must be retained in the diligence file for a minimum of 7 years. Where a reference contact declines to comment on specific topics, the HR lead must note the declination verbatim and assess whether the pattern of non-responses is itself a red flag. A reference contact's blanket positive endorsement combined with specific declinations to address project-level or departure-context questions is treated as a guarded response and documented accordingly. Audio recordings of reference calls, where obtained, are treated as the authoritative record in preference to any contemporaneous notes or auto-generated transcripts.

Section 6 — Risk Tier Framework. Following completion of the diligence review, the HR lead assigns one of four risk tiers: Low, Medium, High, or Hold. The assignment is governed by the following criteria: Low — no discrepancies identified across all evidence channels; all reference contacts gave positive or neutral assessments; no PIP or disciplinary history disclosed or discovered. Medium — one or more minor discrepancies identified (within 30-day threshold per Section 3.2), or a single guarded reference response with no elaboration; no PIP or disciplinary history identified. High — one or more discrepancies exceeding the 30-day threshold, OR a PIP or formal disciplinary action discovered that was not self-disclosed by the candidate, OR two or more concurrent moderate discrepancies from independent channels. Hold — High tier findings combined with evidence of deliberate misrepresentation, OR a Major discrepancy (>90 days), OR active legal proceedings involving prior employer relationships. Hold requires review by senior HR leadership before the diligence file is closed.

in compliance with all federal and state employment law requirements

taking into account all relevant employment history

notwithstanding any prior written representations

in compliance with all federal and state employment law requirements

as outlined in the Staff Engineer competency framework applicable to the role

Under the doctrine of negligent hiring, an employer may be held liable for damages arising from an employee's wrongful acts if the employer knew, or should have known, of facts that would have made the hiring decision unreasonably risky. Thorough background diligence — including reference interviews, employment date verification, and professional profile review — is a recognized mitigation against negligent hiring claims. Courts have generally found that employers who follow a documented, multi-channel diligence process demonstrate reasonable care, even where a subsequently discovered adverse fact was not identified prior to hiring.

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

## Appendix L: Capacity Planning And Cost Optimization — Diligence Guidance

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

Section 7 — Reference Interview Protocols. Reference interviews must be conducted by or in the presence of the HR lead. Interview notes must be retained in the diligence file for a minimum of 7 years. Where a reference contact declines to comment on specific topics, the HR lead must note the declination verbatim and assess whether the pattern of non-responses is itself a red flag. A reference contact's blanket positive endorsement combined with specific declinations to address project-level or departure-context questions is treated as a guarded response and documented accordingly. Audio recordings of reference calls, where obtained, are treated as the authoritative record in preference to any contemporaneous notes or auto-generated transcripts.

in a manner consistent with prior diligence findings at comparable firms

consistent with the authoritative source hierarchy defined in industry guidelines

to the extent permitted by applicable labor law

notwithstanding any prior written representations

in compliance with all federal and state employment law requirements

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

## Appendix M: Open-Source Contribution And Community Engagement — Diligence Guidance

Section 6 — Risk Tier Framework. Following completion of the diligence review, the HR lead assigns one of four risk tiers: Low, Medium, High, or Hold. The assignment is governed by the following criteria: Low — no discrepancies identified across all evidence channels; all reference contacts gave positive or neutral assessments; no PIP or disciplinary history disclosed or discovered. Medium — one or more minor discrepancies identified (within 30-day threshold per Section 3.2), or a single guarded reference response with no elaboration; no PIP or disciplinary history identified. High — one or more discrepancies exceeding the 30-day threshold, OR a PIP or formal disciplinary action discovered that was not self-disclosed by the candidate, OR two or more concurrent moderate discrepancies from independent channels. Hold — High tier findings combined with evidence of deliberate misrepresentation, OR a Major discrepancy (>90 days), OR active legal proceedings involving prior employer relationships. Hold requires review by senior HR leadership before the diligence file is closed.

Section 6 — Risk Tier Framework. Following completion of the diligence review, the HR lead assigns one of four risk tiers: Low, Medium, High, or Hold. The assignment is governed by the following criteria: Low — no discrepancies identified across all evidence channels; all reference contacts gave positive or neutral assessments; no PIP or disciplinary history disclosed or discovered. Medium — one or more minor discrepancies identified (within 30-day threshold per Section 3.2), or a single guarded reference response with no elaboration; no PIP or disciplinary history identified. High — one or more discrepancies exceeding the 30-day threshold, OR a PIP or formal disciplinary action discovered that was not self-disclosed by the candidate, OR two or more concurrent moderate discrepancies from independent channels. Hold — High tier findings combined with evidence of deliberate misrepresentation, OR a Major discrepancy (>90 days), OR active legal proceedings involving prior employer relationships. Hold requires review by senior HR leadership before the diligence file is closed.

in accordance with the data minimization principles of the vendor SLA

taking into consideration both the technical and professional conduct dimensions

taking into account all relevant employment history

where applicable under the governing HR framework

in accordance with the data minimization principles of the vendor SLA

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

## Appendix N: Agile Ceremony Participation And Estimation Accuracy — Diligence Guidance

Section 6 — Risk Tier Framework. Following completion of the diligence review, the HR lead assigns one of four risk tiers: Low, Medium, High, or Hold. The assignment is governed by the following criteria: Low — no discrepancies identified across all evidence channels; all reference contacts gave positive or neutral assessments; no PIP or disciplinary history disclosed or discovered. Medium — one or more minor discrepancies identified (within 30-day threshold per Section 3.2), or a single guarded reference response with no elaboration; no PIP or disciplinary history identified. High — one or more discrepancies exceeding the 30-day threshold, OR a PIP or formal disciplinary action discovered that was not self-disclosed by the candidate, OR two or more concurrent moderate discrepancies from independent channels. Hold — High tier findings combined with evidence of deliberate misrepresentation, OR a Major discrepancy (>90 days), OR active legal proceedings involving prior employer relationships. Hold requires review by senior HR leadership before the diligence file is closed.

Section 3.2 — Employment Date Discrepancy Thresholds. Where the employment dates self-reported by a candidate differ from the dates independently verified by HR or an authorized vendor, the following thresholds apply: discrepancies of 30 days or fewer are classified as Minor and logged without escalation. Discrepancies exceeding 30 days but not exceeding 90 days are classified as Moderate and require escalation to the hiring manager with a written notation in the diligence file. Discrepancies exceeding 90 days are classified as Major and require escalation to senior HR leadership and legal review before any offer is extended. For the purpose of this section, the verified date is the later of: (a) the date confirmed by the prior employer's official HR records, (b) the date confirmed by a reference contact with direct knowledge, or (c) the date shown on a professional profile maintained by the candidate. Self-report alone does not constitute independent verification.

consistent with the authoritative source hierarchy defined in industry guidelines

subject to the limitations prescribed in the policy handbook

subject to the limitations prescribed in the policy handbook

subject to final review by the HRBP and legal counsel as appropriate

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

## Appendix O: Sre Principles And Error Budget Management — Diligence Guidance

Section 3.2 — Employment Date Discrepancy Thresholds. Where the employment dates self-reported by a candidate differ from the dates independently verified by HR or an authorized vendor, the following thresholds apply: discrepancies of 30 days or fewer are classified as Minor and logged without escalation. Discrepancies exceeding 30 days but not exceeding 90 days are classified as Moderate and require escalation to the hiring manager with a written notation in the diligence file. Discrepancies exceeding 90 days are classified as Major and require escalation to senior HR leadership and legal review before any offer is extended. For the purpose of this section, the verified date is the later of: (a) the date confirmed by the prior employer's official HR records, (b) the date confirmed by a reference contact with direct knowledge, or (c) the date shown on a professional profile maintained by the candidate. Self-report alone does not constitute independent verification.

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

in a manner reasonably calculated to achieve compliance

taking into account all relevant employment history

consistent with the authoritative source hierarchy defined in industry guidelines

in furtherance of the objectives set out in the diligence brief

to the extent permitted by applicable labor law

Under the doctrine of negligent hiring, an employer may be held liable for damages arising from an employee's wrongful acts if the employer knew, or should have known, of facts that would have made the hiring decision unreasonably risky. Thorough background diligence — including reference interviews, employment date verification, and professional profile review — is a recognized mitigation against negligent hiring claims. Courts have generally found that employers who follow a documented, multi-channel diligence process demonstrate reasonable care, even where a subsequently discovered adverse fact was not identified prior to hiring.

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

## Appendix P: Api Design And Backward Compatibility Standards — Diligence Guidance

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

notwithstanding any prior written representations

where applicable under the governing HR framework

in furtherance of the objectives set out in the diligence brief

notwithstanding any prior written representations

subject to the limitations prescribed in the policy handbook

as determined by the HR lead and diligence coordinator

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

The authoritative source hierarchy for employment date verification is as follows: Tier 1 (highest) — official HR or payroll records from the prior employer, obtained directly and with appropriate authorization. Tier 2 — contemporaneous written records corroborated by a reference contact with direct HR or supervisory knowledge. Tier 3 — professional profile dates (e.g., LinkedIn) maintained by the candidate on a platform where third parties can observe the claimed dates. Tier 4 (lowest) — candidate's own self-report in the intake form or resume. Where Tier 1 or Tier 2 records are unavailable, Tier 3 is treated as the independent verification source, and discrepancies against Tier 4 (candidate self-report) are assessed under the applicable policy thresholds.

## Appendix Q: Build System Configuration And Ci/Cd Pipeline Ownership — Diligence Guidance

Section 8 — GitHub and Open-Source Profile Verification. Where a candidate lists a public code repository handle (e.g., GitHub username), the HR diligence team or its authorized vendor may review the public commit history associated with that handle. The purpose of this review is limited to: (a) confirming that the handle exists and is accessible, (b) cross-referencing commit dates with claimed employment periods, and (c) identifying whether multiple author email addresses appear in the commit history in a manner inconsistent with the candidate's self-stated email address. The presence of a work email address in pre-transition commits is not itself a disqualifying finding; however, a transition from a work domain email to a personal email mid-tenure is flaggable and must be documented.

Section 5.1 — PIP and Disciplinary Action Disclosure Requirements. Candidates are required to self-disclose, in their intake submission, any active or recently concluded performance improvement plan (PIP) or formal disciplinary action taken within the 24 months preceding the application date. 'Recently concluded' means completed, withdrawn, or otherwise terminated within the preceding 24 months. Failure to self-disclose a PIP that is subsequently revealed through the reference interview process or independent verification constitutes a material omission and triggers an automatic risk tier upgrade to High. The HR lead retains discretion to recommend a Hold pending further clarification with the candidate.

subject to the limitations prescribed in the policy handbook

subject to the provisions of the background check framework

in a manner consistent with prior diligence findings at comparable firms

where applicable under the governing HR framework

as mandated by the hiring committee's diligence standards

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

Under the doctrine of negligent hiring, an employer may be held liable for damages arising from an employee's wrongful acts if the employer knew, or should have known, of facts that would have made the hiring decision unreasonably risky. Thorough background diligence — including reference interviews, employment date verification, and professional profile review — is a recognized mitigation against negligent hiring claims. Courts have generally found that employers who follow a documented, multi-channel diligence process demonstrate reasonable care, even where a subsequently discovered adverse fact was not identified prior to hiring.

## Appendix R: Dependency Management And Vulnerability Response — Diligence Guidance

Section 8 — GitHub and Open-Source Profile Verification. Where a candidate lists a public code repository handle (e.g., GitHub username), the HR diligence team or its authorized vendor may review the public commit history associated with that handle. The purpose of this review is limited to: (a) confirming that the handle exists and is accessible, (b) cross-referencing commit dates with claimed employment periods, and (c) identifying whether multiple author email addresses appear in the commit history in a manner inconsistent with the candidate's self-stated email address. The presence of a work email address in pre-transition commits is not itself a disqualifying finding; however, a transition from a work domain email to a personal email mid-tenure is flaggable and must be documented.

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

in light of the candidate's self-submitted materials and independent evidence channels

where applicable under the governing HR framework

in compliance with all federal and state employment law requirements

without prejudice to any other rights or remedies available to Meridian

consistent with the authoritative source hierarchy defined in industry guidelines

Under the doctrine of negligent hiring, an employer may be held liable for damages arising from an employee's wrongful acts if the employer knew, or should have known, of facts that would have made the hiring decision unreasonably risky. Thorough background diligence — including reference interviews, employment date verification, and professional profile review — is a recognized mitigation against negligent hiring claims. Courts have generally found that employers who follow a documented, multi-channel diligence process demonstrate reasonable care, even where a subsequently discovered adverse fact was not identified prior to hiring.

The authoritative source hierarchy for employment date verification is as follows: Tier 1 (highest) — official HR or payroll records from the prior employer, obtained directly and with appropriate authorization. Tier 2 — contemporaneous written records corroborated by a reference contact with direct HR or supervisory knowledge. Tier 3 — professional profile dates (e.g., LinkedIn) maintained by the candidate on a platform where third parties can observe the claimed dates. Tier 4 (lowest) — candidate's own self-report in the intake form or resume. Where Tier 1 or Tier 2 records are unavailable, Tier 3 is treated as the independent verification source, and discrepancies against Tier 4 (candidate self-report) are assessed under the applicable policy thresholds.

## Appendix S: Load Testing Methodology And Performance Benchmarking — Diligence Guidance

Section 7 — Reference Interview Protocols. Reference interviews must be conducted by or in the presence of the HR lead. Interview notes must be retained in the diligence file for a minimum of 7 years. Where a reference contact declines to comment on specific topics, the HR lead must note the declination verbatim and assess whether the pattern of non-responses is itself a red flag. A reference contact's blanket positive endorsement combined with specific declinations to address project-level or departure-context questions is treated as a guarded response and documented accordingly. Audio recordings of reference calls, where obtained, are treated as the authoritative record in preference to any contemporaneous notes or auto-generated transcripts.

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

consistent with the principles of fair and thorough diligence

to the extent permitted by applicable labor law

in accordance with the data minimization principles of the vendor SLA

in compliance with all federal and state employment law requirements

in a manner reasonably calculated to achieve compliance

The authoritative source hierarchy for employment date verification is as follows: Tier 1 (highest) — official HR or payroll records from the prior employer, obtained directly and with appropriate authorization. Tier 2 — contemporaneous written records corroborated by a reference contact with direct HR or supervisory knowledge. Tier 3 — professional profile dates (e.g., LinkedIn) maintained by the candidate on a platform where third parties can observe the claimed dates. Tier 4 (lowest) — candidate's own self-report in the intake form or resume. Where Tier 1 or Tier 2 records are unavailable, Tier 3 is treated as the independent verification source, and discrepancies against Tier 4 (candidate self-report) are assessed under the applicable policy thresholds.

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

## Appendix T: Runbook Authorship And Operational Documentation — Diligence Guidance

Section 7 — Reference Interview Protocols. Reference interviews must be conducted by or in the presence of the HR lead. Interview notes must be retained in the diligence file for a minimum of 7 years. Where a reference contact declines to comment on specific topics, the HR lead must note the declination verbatim and assess whether the pattern of non-responses is itself a red flag. A reference contact's blanket positive endorsement combined with specific declinations to address project-level or departure-context questions is treated as a guarded response and documented accordingly. Audio recordings of reference calls, where obtained, are treated as the authoritative record in preference to any contemporaneous notes or auto-generated transcripts.

Section 5.1 — PIP and Disciplinary Action Disclosure Requirements. Candidates are required to self-disclose, in their intake submission, any active or recently concluded performance improvement plan (PIP) or formal disciplinary action taken within the 24 months preceding the application date. 'Recently concluded' means completed, withdrawn, or otherwise terminated within the preceding 24 months. Failure to self-disclose a PIP that is subsequently revealed through the reference interview process or independent verification constitutes a material omission and triggers an automatic risk tier upgrade to High. The HR lead retains discretion to recommend a Hold pending further clarification with the candidate.

in light of the candidate's self-submitted materials and independent evidence channels

in accordance with the data minimization principles of the vendor SLA

as outlined in the Staff Engineer competency framework applicable to the role

in accordance with Meridian Systems HR policy v4

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

## Appendix U: On-Call Escalation Judgment And Incident Communication — Diligence Guidance

Section 5.1 — PIP and Disciplinary Action Disclosure Requirements. Candidates are required to self-disclose, in their intake submission, any active or recently concluded performance improvement plan (PIP) or formal disciplinary action taken within the 24 months preceding the application date. 'Recently concluded' means completed, withdrawn, or otherwise terminated within the preceding 24 months. Failure to self-disclose a PIP that is subsequently revealed through the reference interview process or independent verification constitutes a material omission and triggers an automatic risk tier upgrade to High. The HR lead retains discretion to recommend a Hold pending further clarification with the candidate.

Section 5.1 — PIP and Disciplinary Action Disclosure Requirements. Candidates are required to self-disclose, in their intake submission, any active or recently concluded performance improvement plan (PIP) or formal disciplinary action taken within the 24 months preceding the application date. 'Recently concluded' means completed, withdrawn, or otherwise terminated within the preceding 24 months. Failure to self-disclose a PIP that is subsequently revealed through the reference interview process or independent verification constitutes a material omission and triggers an automatic risk tier upgrade to High. The HR lead retains discretion to recommend a Hold pending further clarification with the candidate.

in compliance with all federal and state employment law requirements

in compliance with all federal and state employment law requirements

consistent with established background check precedent

as may be amended from time to time by competent HR authority

as may be amended from time to time by competent HR authority

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

Under the doctrine of negligent hiring, an employer may be held liable for damages arising from an employee's wrongful acts if the employer knew, or should have known, of facts that would have made the hiring decision unreasonably risky. Thorough background diligence — including reference interviews, employment date verification, and professional profile review — is a recognized mitigation against negligent hiring claims. Courts have generally found that employers who follow a documented, multi-channel diligence process demonstrate reasonable care, even where a subsequently discovered adverse fact was not identified prior to hiring.

## Appendix V: Post-Mortem Facilitation And Corrective Action Tracking — Diligence Guidance

Section 6 — Risk Tier Framework. Following completion of the diligence review, the HR lead assigns one of four risk tiers: Low, Medium, High, or Hold. The assignment is governed by the following criteria: Low — no discrepancies identified across all evidence channels; all reference contacts gave positive or neutral assessments; no PIP or disciplinary history disclosed or discovered. Medium — one or more minor discrepancies identified (within 30-day threshold per Section 3.2), or a single guarded reference response with no elaboration; no PIP or disciplinary history identified. High — one or more discrepancies exceeding the 30-day threshold, OR a PIP or formal disciplinary action discovered that was not self-disclosed by the candidate, OR two or more concurrent moderate discrepancies from independent channels. Hold — High tier findings combined with evidence of deliberate misrepresentation, OR a Major discrepancy (>90 days), OR active legal proceedings involving prior employer relationships. Hold requires review by senior HR leadership before the diligence file is closed.

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

as mandated by the hiring committee's diligence standards

without prejudice to any other rights or remedies available to Meridian

notwithstanding any prior written representations

in accordance with the data minimization principles of the vendor SLA

where applicable under the governing HR framework

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

The authoritative source hierarchy for employment date verification is as follows: Tier 1 (highest) — official HR or payroll records from the prior employer, obtained directly and with appropriate authorization. Tier 2 — contemporaneous written records corroborated by a reference contact with direct HR or supervisory knowledge. Tier 3 — professional profile dates (e.g., LinkedIn) maintained by the candidate on a platform where third parties can observe the claimed dates. Tier 4 (lowest) — candidate's own self-report in the intake form or resume. Where Tier 1 or Tier 2 records are unavailable, Tier 3 is treated as the independent verification source, and discrepancies against Tier 4 (candidate self-report) are assessed under the applicable policy thresholds.

## Appendix W: Site Reliability Metrics Dashboard Design — Diligence Guidance

Section 7 — Reference Interview Protocols. Reference interviews must be conducted by or in the presence of the HR lead. Interview notes must be retained in the diligence file for a minimum of 7 years. Where a reference contact declines to comment on specific topics, the HR lead must note the declination verbatim and assess whether the pattern of non-responses is itself a red flag. A reference contact's blanket positive endorsement combined with specific declinations to address project-level or departure-context questions is treated as a guarded response and documented accordingly. Audio recordings of reference calls, where obtained, are treated as the authoritative record in preference to any contemporaneous notes or auto-generated transcripts.

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

to the extent permitted by applicable labor law

pursuant to applicable employment verification regulations

subject to final review by the HRBP and legal counsel as appropriate

consistent with the authoritative source hierarchy defined in industry guidelines

pursuant to applicable employment verification regulations

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

Under the doctrine of negligent hiring, an employer may be held liable for damages arising from an employee's wrongful acts if the employer knew, or should have known, of facts that would have made the hiring decision unreasonably risky. Thorough background diligence — including reference interviews, employment date verification, and professional profile review — is a recognized mitigation against negligent hiring claims. Courts have generally found that employers who follow a documented, multi-channel diligence process demonstrate reasonable care, even where a subsequently discovered adverse fact was not identified prior to hiring.

## Appendix X: Resource Governance And Quota Management In Cloud Environments — Diligence Guidance

Section 3.2 — Employment Date Discrepancy Thresholds. Where the employment dates self-reported by a candidate differ from the dates independently verified by HR or an authorized vendor, the following thresholds apply: discrepancies of 30 days or fewer are classified as Minor and logged without escalation. Discrepancies exceeding 30 days but not exceeding 90 days are classified as Moderate and require escalation to the hiring manager with a written notation in the diligence file. Discrepancies exceeding 90 days are classified as Major and require escalation to senior HR leadership and legal review before any offer is extended. For the purpose of this section, the verified date is the later of: (a) the date confirmed by the prior employer's official HR records, (b) the date confirmed by a reference contact with direct knowledge, or (c) the date shown on a professional profile maintained by the candidate. Self-report alone does not constitute independent verification.

Section 6 — Risk Tier Framework. Following completion of the diligence review, the HR lead assigns one of four risk tiers: Low, Medium, High, or Hold. The assignment is governed by the following criteria: Low — no discrepancies identified across all evidence channels; all reference contacts gave positive or neutral assessments; no PIP or disciplinary history disclosed or discovered. Medium — one or more minor discrepancies identified (within 30-day threshold per Section 3.2), or a single guarded reference response with no elaboration; no PIP or disciplinary history identified. High — one or more discrepancies exceeding the 30-day threshold, OR a PIP or formal disciplinary action discovered that was not self-disclosed by the candidate, OR two or more concurrent moderate discrepancies from independent channels. Hold — High tier findings combined with evidence of deliberate misrepresentation, OR a Major discrepancy (>90 days), OR active legal proceedings involving prior employer relationships. Hold requires review by senior HR leadership before the diligence file is closed.

consistent with established background check precedent

provided that all procedural requirements have been satisfied

in a manner reasonably calculated to achieve compliance

consistent with established background check precedent

where applicable under the governing HR framework

subject to final review by the HRBP and legal counsel as appropriate

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

## Appendix Y: Configuration Drift Detection And Remediation — Diligence Guidance

Section 6 — Risk Tier Framework. Following completion of the diligence review, the HR lead assigns one of four risk tiers: Low, Medium, High, or Hold. The assignment is governed by the following criteria: Low — no discrepancies identified across all evidence channels; all reference contacts gave positive or neutral assessments; no PIP or disciplinary history disclosed or discovered. Medium — one or more minor discrepancies identified (within 30-day threshold per Section 3.2), or a single guarded reference response with no elaboration; no PIP or disciplinary history identified. High — one or more discrepancies exceeding the 30-day threshold, OR a PIP or formal disciplinary action discovered that was not self-disclosed by the candidate, OR two or more concurrent moderate discrepancies from independent channels. Hold — High tier findings combined with evidence of deliberate misrepresentation, OR a Major discrepancy (>90 days), OR active legal proceedings involving prior employer relationships. Hold requires review by senior HR leadership before the diligence file is closed.

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

in furtherance of the objectives set out in the diligence brief

taking into consideration both the technical and professional conduct dimensions

to the extent permitted by applicable labor law

taking into account all relevant employment history

where applicable under the governing HR framework

Under the doctrine of negligent hiring, an employer may be held liable for damages arising from an employee's wrongful acts if the employer knew, or should have known, of facts that would have made the hiring decision unreasonably risky. Thorough background diligence — including reference interviews, employment date verification, and professional profile review — is a recognized mitigation against negligent hiring claims. Courts have generally found that employers who follow a documented, multi-channel diligence process demonstrate reasonable care, even where a subsequently discovered adverse fact was not identified prior to hiring.

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

## Appendix Z: Distributed Systems Design And Reliability Engineering — Diligence Guidance

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

Section 7 — Reference Interview Protocols. Reference interviews must be conducted by or in the presence of the HR lead. Interview notes must be retained in the diligence file for a minimum of 7 years. Where a reference contact declines to comment on specific topics, the HR lead must note the declination verbatim and assess whether the pattern of non-responses is itself a red flag. A reference contact's blanket positive endorsement combined with specific declinations to address project-level or departure-context questions is treated as a guarded response and documented accordingly. Audio recordings of reference calls, where obtained, are treated as the authoritative record in preference to any contemporaneous notes or auto-generated transcripts.

in a manner consistent with prior diligence findings at comparable firms

where applicable under the governing HR framework

as may be amended from time to time by competent HR authority

in accordance with the data minimization principles of the vendor SLA

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

## Appendix [: Incident Management And On-Call Response Protocols — Diligence Guidance

Section 5.1 — PIP and Disciplinary Action Disclosure Requirements. Candidates are required to self-disclose, in their intake submission, any active or recently concluded performance improvement plan (PIP) or formal disciplinary action taken within the 24 months preceding the application date. 'Recently concluded' means completed, withdrawn, or otherwise terminated within the preceding 24 months. Failure to self-disclose a PIP that is subsequently revealed through the reference interview process or independent verification constitutes a material omission and triggers an automatic risk tier upgrade to High. The HR lead retains discretion to recommend a Hold pending further clarification with the candidate.

Section 8 — GitHub and Open-Source Profile Verification. Where a candidate lists a public code repository handle (e.g., GitHub username), the HR diligence team or its authorized vendor may review the public commit history associated with that handle. The purpose of this review is limited to: (a) confirming that the handle exists and is accessible, (b) cross-referencing commit dates with claimed employment periods, and (c) identifying whether multiple author email addresses appear in the commit history in a manner inconsistent with the candidate's self-stated email address. The presence of a work email address in pre-transition commits is not itself a disqualifying finding; however, a transition from a work domain email to a personal email mid-tenure is flaggable and must be documented.

without prejudice to any other rights or remedies available to Meridian

as may be amended from time to time by competent HR authority

subject to final review by the HRBP and legal counsel as appropriate

as mandated by the hiring committee's diligence standards

Under the doctrine of negligent hiring, an employer may be held liable for damages arising from an employee's wrongful acts if the employer knew, or should have known, of facts that would have made the hiring decision unreasonably risky. Thorough background diligence — including reference interviews, employment date verification, and professional profile review — is a recognized mitigation against negligent hiring claims. Courts have generally found that employers who follow a documented, multi-channel diligence process demonstrate reasonable care, even where a subsequently discovered adverse fact was not identified prior to hiring.

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

## Appendix \: Observability Stack Ownership And Slo/Sla Management — Diligence Guidance

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

Section 3.2 — Employment Date Discrepancy Thresholds. Where the employment dates self-reported by a candidate differ from the dates independently verified by HR or an authorized vendor, the following thresholds apply: discrepancies of 30 days or fewer are classified as Minor and logged without escalation. Discrepancies exceeding 30 days but not exceeding 90 days are classified as Moderate and require escalation to the hiring manager with a written notation in the diligence file. Discrepancies exceeding 90 days are classified as Major and require escalation to senior HR leadership and legal review before any offer is extended. For the purpose of this section, the verified date is the later of: (a) the date confirmed by the prior employer's official HR records, (b) the date confirmed by a reference contact with direct knowledge, or (c) the date shown on a professional profile maintained by the candidate. Self-report alone does not constitute independent verification.

consistent with established background check precedent

pursuant to applicable employment verification regulations

subject to the provisions of the background check framework

as mandated by the hiring committee's diligence standards

where applicable under the governing HR framework

in light of the candidate's self-submitted materials and independent evidence channels

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

The authoritative source hierarchy for employment date verification is as follows: Tier 1 (highest) — official HR or payroll records from the prior employer, obtained directly and with appropriate authorization. Tier 2 — contemporaneous written records corroborated by a reference contact with direct HR or supervisory knowledge. Tier 3 — professional profile dates (e.g., LinkedIn) maintained by the candidate on a platform where third parties can observe the claimed dates. Tier 4 (lowest) — candidate's own self-report in the intake form or resume. Where Tier 1 or Tier 2 records are unavailable, Tier 3 is treated as the independent verification source, and discrepancies against Tier 4 (candidate self-report) are assessed under the applicable policy thresholds.

## Appendix ]: Code Review Practices And Pull Request Standards — Diligence Guidance

Section 3.2 — Employment Date Discrepancy Thresholds. Where the employment dates self-reported by a candidate differ from the dates independently verified by HR or an authorized vendor, the following thresholds apply: discrepancies of 30 days or fewer are classified as Minor and logged without escalation. Discrepancies exceeding 30 days but not exceeding 90 days are classified as Moderate and require escalation to the hiring manager with a written notation in the diligence file. Discrepancies exceeding 90 days are classified as Major and require escalation to senior HR leadership and legal review before any offer is extended. For the purpose of this section, the verified date is the later of: (a) the date confirmed by the prior employer's official HR records, (b) the date confirmed by a reference contact with direct knowledge, or (c) the date shown on a professional profile maintained by the candidate. Self-report alone does not constitute independent verification.

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

in compliance with all federal and state employment law requirements

taking into consideration both the technical and professional conduct dimensions

subject to the limitations prescribed in the policy handbook

provided that all procedural requirements have been satisfied

pursuant to applicable employment verification regulations

Employment verification law in the United States is primarily governed by the Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681 et seq., which imposes disclosure and authorization requirements on employers who use consumer reporting agencies (CRAs) to conduct background checks. Where an employer conducts background diligence using only in-house HR personnel and direct reference interviews — without engaging a CRA — the FCRA's procedural requirements do not apply. However, employers remain subject to applicable state employment verification laws, anti-discrimination statutes, and the implied covenant of fair dealing in their jurisdictions.

Under the doctrine of negligent hiring, an employer may be held liable for damages arising from an employee's wrongful acts if the employer knew, or should have known, of facts that would have made the hiring decision unreasonably risky. Thorough background diligence — including reference interviews, employment date verification, and professional profile review — is a recognized mitigation against negligent hiring claims. Courts have generally found that employers who follow a documented, multi-channel diligence process demonstrate reasonable care, even where a subsequently discovered adverse fact was not identified prior to hiring.

## Appendix ^: Cross-Functional Collaboration And Stakeholder Communication — Diligence Guidance

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

All candidates for Staff Engineer and above must pass a comprehensive background diligence review prior to offer issuance. The diligence review covers employment history verification, educational credential verification where applicable, and professional reference interviews. The review must be completed within 48 hours of offer-stage clearance to prevent undue delay to the candidate or the hiring team.

consistent with established background check precedent

to the extent permitted by applicable labor law

in accordance with Meridian Systems HR policy v4

taking into account all relevant employment history

where applicable under the governing HR framework

in light of the candidate's self-submitted materials and independent evidence channels

State-level restrictions on the use of criminal background information in hiring decisions ('ban the box' legislation) are distinct from employment history verification and PIP disclosure review. The s_candidate_background_check diligence process does not involve criminal background screening and is therefore outside the scope of ban the box statutes in most jurisdictions. The diligence process addresses only employment date verification, professional reference interviews, and publicly available digital profile review.

Under the doctrine of negligent hiring, an employer may be held liable for damages arising from an employee's wrongful acts if the employer knew, or should have known, of facts that would have made the hiring decision unreasonably risky. Thorough background diligence — including reference interviews, employment date verification, and professional profile review — is a recognized mitigation against negligent hiring claims. Courts have generally found that employers who follow a documented, multi-channel diligence process demonstrate reasonable care, even where a subsequently discovered adverse fact was not identified prior to hiring.