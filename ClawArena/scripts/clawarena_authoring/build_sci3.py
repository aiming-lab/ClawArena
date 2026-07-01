#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sci3.py — 生成 ClawArena 真实数据集场景 sci3（医疗排班与护患比危机）。

题材与锚点取材真实（California Title 22 § 70217 / H&SC § 1280.3 / AFL-23-27 / SB 596 / Oregon HB 2697）。
全 exec_check，17 轮，2 次 update（含 1 次 supersede）。

幂等：每次运行先清空 sci3 的 workspace/state/updates 后重建，再落 _register.json。
questions.json 与 check 脚本由 eval/sci3/ 下静态文件提供，本脚本不生成它们。

运行：python scripts/clawarena_authoring/build_sci3.py
"""
from __future__ import annotations

import calendar
import csv
import hashlib
import io
import json
import random
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, est_tokens, gen_session_id,
    dump_register_meta,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "sci3"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# 1. 系统文件（OpenClaw agent 启动文件）
# --------------------------------------------------------------------------- #
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles and source hierarchy.
2. Read `USER.md` to learn about the people and communication channels.
3. Run `exec ls -R` to inspect current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a Healthcare Compliance AI assistant supporting Miranda Chen, Chief Nursing Officer (CNO)
at Sutter Valley Medical Center (SVMC), a 350-bed General Acute Care Hospital in California.
Your role is to help resolve a nurse staffing ratio crisis under California law.
""")

    w(WS / "SOUL.md", """# Working Principles

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
""")

    w(WS / "USER.md", """# People and Channels

## Primary User
- **Miranda Chen** — Chief Nursing Officer (CNO), Sutter Valley Medical Center (SVMC).
  Responsible for nursing compliance with California Title 22 § 70217 and CDPH oversight.
  Prefers integer dollar amounts, snake_case JSON, and Markdown reports with ### headings.

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Dr. James Okafor | ICU Medical Director | Slack DM | Claims ICU scheduling was always compliant |
| Patricia Lowe | Med/Surg Head Nurse | Slack #nursing-ops | Acknowledges night shift ratio violations |
| Kevin Torres | Nurse Union Rep (SEIU) | Email | Claims violations started Oct 2023 (before hospital claims) |
| Dr. Aisha Rahman | Compliance Consultant | Feishu 「合规应急」group | Group bot auto-summary contains distorted figures |
| Inspector Linda Wu | CDPH Compliance Officer | Official Email/Letter | Issued Statement of Deficiencies; set 30-day remediation deadline |

## Channels
- **Slack #nursing-ops**: Internal nursing operations discussion
- **Slack DM (Miranda ↔ Dr. Okafor)**: ICU compliance dispute
- **Email (Union ↔ Hospital HR)**: Violation timeline and settlement negotiations
- **Feishu 「合规应急」**: Compliance consultants — bot auto-summary contains ERRORS
- **CDPH Official Letters**: Authoritative regulatory correspondence
""")

    w(WS / "IDENTITY.md", """# Identity

You are **HealthOps AI**, a healthcare compliance assistant deployed to support Miranda Chen
(CNO) at Sutter Valley Medical Center during a nurse staffing ratio crisis.

Your responsibilities include:
- Analyzing nurse-to-patient ratio compliance under California Title 22 § 70217
- Calculating administrative penalties per H&SC § 1280.3 and CDPH AFL-23-27
- Reviewing scheduling data to identify violations and corrective actions
- Preparing CDPH-required staffing logs and submission documents
- Advising on multi-state regulatory comparisons (California, Oregon, Massachusetts)

Source documents under `regulations/` and `hospital_data/` are authoritative inputs.
Chat summaries (especially the Feishu bot auto-summary) may contain errors — always
verify numbers against the primary regulation documents.
""")

    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session |
| `sessions_history` | Read a specific history session | Use in main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to write deliverable files |

## Rules
- Regulation documents under `regulations/` are read-only authoritative sources.
- Hospital data under `hospital_data/` are read-only input records.
- Create deliverables under `output/` using `exec`.
- Do NOT modify source files under `regulations/` or `hospital_data/`.
""")


# --------------------------------------------------------------------------- #
# 2. 法规文件（真实锚点）
# --------------------------------------------------------------------------- #
def gen_regulations() -> None:
    # Cal. Code Regs. Title 22 § 70217 全文（真实锚点 A1-A11, A18）
    w(WS / "regulations" / "CA_Title22_§70217_full.txt", """
California Code of Regulations, Title 22, Division 5, Chapter 1
MINIMUM NURSE-TO-PATIENT STAFFING RATIOS
§ 70217. Nursing Service Staff.

Source: Cal. Code Regs. Tit. 22, § 70217
URL: https://www.law.cornell.edu/regulations/california/Cal-Code-Regs-Tit-22-SS-70217

(a) MINIMUM NURSE-TO-PATIENT RATIOS. No general acute care hospital shall assign a
licensed nurse to a patient care unit unless the following minimum nurse-to-patient
ratios are maintained at all times:

(1) Intensive Care Unit (ICU) — Critical Care, including Intensive Care Unit,
    Coronary Care Unit, Burn Unit, Acute Respiratory Care Unit, and
    Neonatal Intensive Care Unit:
    Maximum of TWO (2) patients per licensed nurse.
    Ratio: 1:2 (one nurse per two patients maximum).
    EFFECTIVE DATE: January 1, 2004.

(2) [Reserved]

(3) Postanesthesia care unit (PACU): 1:2

(4) Pediatric ICU: 1:2

(5) Neonatal ICU: Varies by acuity (see subsection)

(6) Labor and Delivery: 1:2 (active labor); 1:1 (delivery/immediate post-partum)

(7) Antepartum: 1:4

(8) Emergency Department:
    (A) General ED: Maximum of FOUR (4) patients per nurse. Ratio: 1:4.
    (B) Critical/Trauma patients: Maximum of ONE (1) per nurse (RN only).
        Only a Registered Nurse (RN) may be assigned a critical trauma patient.
    EFFECTIVE DATE: January 1, 2004.

(9) Step-Down Unit (Intermediate Care / Progressive Care):
    Patients experiencing moderate-to-severe physiological instability who require
    technical monitoring support but do NOT require artificial life support:
    Maximum of THREE (3) patients per nurse. Ratio: 1:3.
    EFFECTIVE DATE: January 1, 2008.

(10) Telemetry Unit:
    Patients requiring continuous cardiac monitoring in a stable condition:
    Maximum of FOUR (4) patients per nurse. Ratio: 1:4.
    EFFECTIVE DATE: January 1, 2008.

(11) Medical/Surgical Unit (Med/Surg):
    PHASE-IN SCHEDULE:
    - January 1, 2004: Maximum 6 patients per nurse (1:6)
    - January 1, 2005: Maximum 5 patients per nurse (1:5) — CURRENT
    Maximum of FIVE (5) patients per nurse. Ratio: 1:5.
    EFFECTIVE DATE: January 1, 2005.

(12) [Reserved — Gynecology: see acute care]

(13) Psychiatric Unit:
    Maximum of SIX (6) patients per nurse. Ratio: 1:6.
    NOTE: In psychiatric units only, a Psychiatric Technician (PT) may be counted
    toward the nurse-to-patient ratio and may substitute for a Licensed Vocational
    Nurse (LVN) position.
    EFFECTIVE DATE: January 1, 2004.

(14) Operating Room: 1:1 minimum (circulating RN)

(b) APPLICABILITY. These ratios apply at ALL times, including during meal periods and
breaks. No averaging of patients and nurses is permitted. When the licensed nurse is
on break or meal, a replacement nurse must be provided to maintain the ratio.

(c) CHARGE NURSE. A Charge Nurse shall be counted toward the nurse-to-patient ratio
ONLY when that Charge Nurse is actively engaged in the direct care of patients.
When the Charge Nurse is performing administrative or supervisory duties exclusively,
that nurse shall NOT be counted in the nurse-to-patient ratio calculation.

(d) RECORD-KEEPING REQUIREMENTS. Every general acute care hospital shall maintain
records of its actual nurse-to-patient assignments on a day-to-day, shift-by-shift
basis. These records shall be maintained for a period of not less than ONE (1) YEAR
and shall be made immediately available to the Department upon request during an
inspection or survey.

(e) WAIVERS. Rural hospitals qualifying under § 70059.1 may apply for limited waivers.
Urban general acute care hospitals (including SVMC) are NOT eligible for rural waivers.

INTERPRETIVE NOTES (CDPH Guidance):
- The ratios are MINIMUMS; hospitals must assign additional nurses based on documented
  patient acuity, illness severity, and care complexity scores.
- Unlicensed personnel CANNOT perform RN nursing functions including medication
  administration, venipuncture, or invasive procedures.
- "No averaging" means: if 5 patients are admitted to Med/Surg and only 1 RN is on duty,
  that is a 1:5 ratio — adding a 6th patient makes it 1:6 (violation), regardless of
  other nurses on other units.

CROSS-REFERENCES:
- California Health & Safety Code § 1276.4 (statutory authority)
- H&SC § 1280.3 (administrative penalties)
- CDPH AFL-23-27 (enforcement guidance, September 2023)
- California SB 596 (effective January 1, 2026 — daily penalty amendment)
""")

    # H&SC § 1276.4 注释版
    w(WS / "regulations" / "CA_HSC_§1276.4_annotated.txt", """
California Health & Safety Code § 1276.4
MINIMUM NURSE STAFFING RATIOS (Statutory Authority)

Source: California Health & Safety Code § 1276.4
URL: https://law.onecle.com/california/health/1276.4.html

(a) PURPOSE. The Legislature finds and declares that there is substantial evidence that
the quality of patient care in hospitals is related to the skill level and the number of
nursing staff providing that care, and that inadequate nurse-to-patient ratios can have
adverse consequences for the health and safety of hospital patients.

(b) DIRECTIVE TO CDPH. Notwithstanding any other provision of law, the State Department
of Health Care Services [now CDPH] shall adopt regulations no later than January 1, 2002,
that establish minimum, specific, and numerical licensed nurse-to-patient ratios by licensed
nurse classification and by hospital unit for all licensed general acute care hospitals.

(c) SCOPE. Applies to general acute care hospitals as defined in subdivision (a), (b),
and (f) of Section 1250.

(d) IMPLEMENTATION. CDPH adopted Title 22 § 70217 to fulfill this mandate.

AMENDMENT HISTORY:
- Original enactment: 1999
- Amended by Stats. 2012, Ch. 24 (AB 1470), effective June 27, 2012
- AB 1470 clarified rural hospital waiver procedures per § 70059.1

ENFORCEMENT MECHANISM:
- Initial inspections: CDPH conducts unannounced periodic inspections
- Statement of Deficiencies (Form CDPH-2567) issued for confirmed violations
- Administrative penalties under H&SC § 1280.3
- Enforcement guidance: CDPH AFL-23-27 (September 2023)
- Enhanced penalties (SB 596, effective 2026-01-01): daily violations

NOTE ON SVMC APPLICABILITY:
Sutter Valley Medical Center is a 350-bed General Acute Care Hospital licensed under
§ 1250(a). All provisions of § 1276.4 and Title 22 § 70217 apply without exception.
Rural waiver provisions under § 70059.1 do NOT apply to SVMC.
""")

    # H&SC § 1280.3 罚款条款
    w(WS / "regulations" / "CA_HSC_§1280.3_penalties.txt", """
California Health & Safety Code § 1280.3
ADMINISTRATIVE PENALTIES FOR STAFFING RATIO VIOLATIONS

Source: California H&SC § 1280.3 (Justia 2024)
URL: https://law.justia.com/codes/california/code-hsc/division-2/chapter-2/article-3/section-1280-3/

(a) PENALTY AMOUNTS.

(1) FIRST VIOLATION: $15,000 (fifteen thousand dollars) administrative penalty.

(2) SECOND AND SUBSEQUENT VIOLATIONS: $30,000 (thirty thousand dollars) each.
    A violation is "subsequent" if it occurs within THREE (3) years of the most
    recent prior violation finding by CDPH.
    If the most recent prior violation occurred more than 3 years ago, the next
    violation is treated as a FIRST violation (reset to $15,000).

(3) SAME INSPECTION RULE (PRE-SB 596): Multiple violations found during a single
    CDPH inspection are counted as ONE (1) violation for penalty purposes.
    NOTE: This rule is AMENDED by SB 596 effective January 1, 2026 — see § 70217
    and CA_SB596_2025_daily_penalty.txt for updated treatment.

(b) ADDITIONAL PENALTY. CDPH may assess an additional civil penalty if it determines
that the facility's inadequate staffing directly resulted in harm to a patient.

(c) ESTABLISHMENT. This penalty structure was established by SB 227 (Chaptered October
12, 2019). Prior to SB 227, monetary penalties for staffing ratio violations were
not expressly authorized under § 1280.3.

(d) CDPH ENFORCEMENT PROCEDURES.
CDPH conducts unannounced periodic inspections and targeted complaint investigations.
Upon finding a violation, CDPH issues:
(1) A Statement of Deficiencies (CMS-2567 or CDPH-2567 form)
(2) A Plan of Correction deadline (typically 30 days for initial CAP)
(3) Written Notice of Administrative Penalty

(e) APPEAL RIGHTS. Facilities may appeal penalty determinations within 30 days of
receipt of the penalty notice.

IMPORTANT NOTE ON PENALTY CALCULATION:
- "Subsequent" means occurring within the 3-year lookback window.
- If SVMC has no prior violations within the past 3 years: first violation = $15,000.
- Any additional violations within the same 3-year window = $30,000 each.
- Under legacy rules (pre-SB 596): violations from a SINGLE inspection inspection
  count as ONE violation for penalty purposes, regardless of how many shifts are affected.
""")

    # AFL-23-27 执法指导（含豁免三要件）
    w(WS / "regulations" / "CA_AFL-23-27_enforcement.txt", """
STATE OF CALIFORNIA — CALIFORNIA DEPARTMENT OF PUBLIC HEALTH
ALL FACILITIES LETTER (AFL) 23-27

Subject: Enforcement Guidance — Nurse-to-Patient Staffing Ratio Administrative Penalties
Date: September 2023
URL: https://www.cdph.ca.gov/Programs/CHCQ/LCP/Pages/AFL-23-27.aspx

SUMMARY:
This All Facilities Letter provides guidance to licensed general acute care hospitals
regarding the administrative penalty structure for nurse staffing ratio violations under
California Health & Safety Code § 1280.3.

I. PENALTY STRUCTURE CONFIRMED

The penalty structure established by SB 227 (2019) is as follows:
- First violation: $15,000
- Subsequent violations (within 3 years): $30,000 each

CDPH confirms these are the operative amounts effective statewide.

IMPORTANT — DISTORTED FIGURE WARNING:
Some secondary summaries have incorrectly cited a $10,000 first-violation penalty.
THIS IS INCORRECT. The correct first violation penalty is $15,000 per H&SC § 1280.3.
Do not rely on secondary summaries for penalty calculations.

II. THREE-PRONG EXEMPTION DEFENSE

A hospital may assert an affirmative defense to a penalty assessment if it can
demonstrate ALL THREE of the following elements:

PRONG 1 — UNPREDICTABILITY: The patient census fluctuation or staffing shortage was
unpredictable and uncontrollable. The facility must demonstrate that the event causing
the shortage could not have been anticipated with reasonable diligence.

PRONG 2 — PROMPT EFFORTS: The facility made prompt efforts to maintain or restore
compliant staffing levels as soon as the shortage was identified.

PRONG 3 — ON-CALL LIST EXHAUSTION: The facility "immediately used and subsequently
exhausted the hospital's on-call list" before declaring the shortage unavoidable.
The on-call list must include both scheduled on-call staff and float pool nurses.

ALL THREE PRONGS must be satisfied simultaneously. Failing any single prong defeats
the exemption claim.

III. SEASONAL FLUCTUATIONS — NOT AUTOMATICALLY EXEMPT

CDPH explicitly states: Seasonal influenza peaks and other foreseeable recurring
events do NOT automatically qualify as "unpredictable and uncontrollable" under
Prong 1. Hospitals are expected to prepare in advance for known seasonal demand
increases. The influenza season is a known, recurring, predictable event.

Similarly, scheduled FMLA/CFRA leave, while unavoidable for individual employees,
is FORESEEABLE and must be planned for. However, a combination of FMLA leave AND
an additional unexpected event (e.g., sudden resignation) may qualify if documented.

IV. DOCUMENTATION REQUIREMENTS FOR EXEMPTION CLAIM

To support an exemption defense, the facility must maintain contemporaneous records:
1. Documentation showing when the shortage was identified
2. Records showing which on-call nurses were contacted, in sequence
3. Confirmation that ALL nurses on the on-call list were contacted
4. The specific basis for concluding the situation was unpredictable

V. PATIENT HARM ADDITIONAL PENALTY

If CDPH determines that the staffing deficiency directly resulted in patient harm,
an additional civil penalty may be assessed above the standard amounts.

VI. SB 596 — UPCOMING CHANGE

SB 596 (signed October 13, 2025, effective January 1, 2026) will change the
penalty calculation methodology. Beginning 2026-01-01, each calendar day of
non-compliance will constitute a separate and distinct violation. The prior rule
under which multiple violations in a single inspection counted as one violation
will no longer apply to violations on or after January 1, 2026.
""")

    # SB 596 日罚款
    w(WS / "regulations" / "CA_SB596_2025_daily_penalty.txt", """
CALIFORNIA SENATE BILL 596
Health Facilities: Administrative Penalties
Signed: October 13, 2025
Effective: January 1, 2026

Source: California SB 596
URL: https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260SB596

SUMMARY OF KEY PROVISIONS:

1. DAILY VIOLATION RULE (effective 2026-01-01):
   Each CALENDAR DAY on which a healthcare facility fails to comply with nurse staffing
   ratio requirements constitutes a SEPARATE AND DISTINCT VIOLATION.
   This means: if a facility has a ratio violation on 5 separate days in a month,
   it faces 5 separate violations, each with its own penalty calculation.

   CONTRAST with pre-SB 596 rule: Under the prior law (H&SC § 1280.3 as enacted by
   SB 227), multiple violations found in a SINGLE inspection counted as one violation.
   SB 596 eliminates this "single inspection = one violation" rule for violations
   occurring on or after January 1, 2026.

2. REVISED ON-CALL LIST DEFINITION:
   SB 596 amends the definition of "on-call list" for exemption purposes.
   An "on-call list" means ONLY nurses who are:
   (a) Scheduled to be on-call for that specific shift and unit, OR
   (b) Nurses in a regularly scheduled float pool for that unit

   EXCLUDED: Facilities CANNOT satisfy the on-call exhaustion requirement by contacting
   nurses who are not on the FORMAL on-call roster. Casual phone calls to off-duty
   nurses who happen to be available do not substitute for exhausting the on-call list.

3. SCOPE: Applies to all general acute care hospitals, acute psychiatric hospitals,
   and special hospitals licensed under the Health and Safety Code.

4. RETROACTIVITY: Does NOT apply retroactively. Violations occurring BEFORE January 1,
   2026 are assessed under the prior rules (H&SC § 1280.3 as of SB 227).

APPLICABILITY TO SVMC:
Any Telemetry unit violations identified in CDPH's supplemental inspection that fall
on or after January 1, 2026 will be counted as separate daily violations under SB 596.
""")

    # Oregon HB 2697 全文（A12-A14）
    w(WS / "regulations" / "OR_HB2697_enrolled.txt", """
OREGON 82nd LEGISLATIVE ASSEMBLY
HOUSE BILL 2697 (ENROLLED)
2023 Regular Session
Signed: August 11, 2023
Chapter: Chapter 421, Oregon Laws 2023

Source: Oregon HB 2697
URL: https://olis.oregonlegislature.gov/liz/2023R1/Downloads/MeasureDocument/HB2697/Enrolled

SAFE NURSE STAFFING LAW

SECTION 1. LEGISLATIVE FINDINGS.
The Legislative Assembly finds that:
(1) Oregon patients deserve safe nurse-to-patient staffing levels in hospitals.
(2) California's landmark staffing law (enacted 1999) demonstrates the feasibility
    of mandatory minimum staffing ratios.
(3) Oregon becomes the second state to mandate minimum nurse staffing ratios.

SECTION 2. MANDATORY NURSE-TO-PATIENT STAFFING RATIOS.
Oregon hospitals must maintain the following minimum nurse-to-patient ratios:

INTENSIVE CARE UNIT (ICU):
Maximum of TWO (2) patients per nurse. Ratio: 1:2.
Effective: June 1, 2024.
NOTE: This matches California's ratio under Title 22 § 70217(a)(1).

MEDICAL/SURGICAL UNIT — PHASE-IN SCHEDULE:
Phase 1: Maximum FIVE (5) patients per nurse (1:5). Effective: June 1, 2024.
Phase 2: Maximum FOUR (4) patients per nurse (1:4). Effective: June 1, 2026.
NOTE: California remains at 1:5 (maximum 5 patients per nurse) for Med/Surg.
Oregon will be STRICTER than California in Med/Surg effective June 1, 2026.

EMERGENCY DEPARTMENT:
Average staffing: 1:4 per shift. Hard maximum: 1:5.
Trauma/critical patients: 1:1.
NOTE: Oregon ED 1:5 hard max differs from California's uniform 1:4.

CNA (Certified Nursing Assistant) RATIOS:
Day shift: 1:7. Night shift: 1:11.

SECTION 3. ELIMINATION OF BUDDY BREAK SYSTEM.
The "buddy break" system (in which one nurse covers another's patients during breaks)
is eliminated. Breaks must be covered by dedicated relief nurses.

SECTION 4. ENFORCEMENT.
(a) IMPLEMENTATION DATE: June 1, 2024.
(b) ENFORCEMENT (investigations and penalties) begins: June 1, 2025.
(c) PENALTY STRUCTURE: Fines of up to $5,000 (five thousand dollars) for repeated
    violations. This is substantially lower than California's $15,000 first-violation
    and $30,000 subsequent-violation penalties under H&SC § 1280.3.

COMPARISON SUMMARY (California vs Oregon):
| Unit          | California (Title 22 § 70217)   | Oregon (HB 2697)                    |
|---------------|----------------------------------|-------------------------------------|
| ICU           | 1:2 (since 2004-01-01)          | 1:2 (since 2024-06-01)              |
| Med/Surg      | 1:5 (since 2005-01-01)          | 1:5 (2024-06-01) → 1:4 (2026-06-01)|
| Telemetry     | 1:4 (since 2008-01-01)          | Not explicitly specified             |
| Step-Down     | 1:3 (since 2008-01-01)          | Not explicitly specified             |
| Penalty (1st) | $15,000 (H&SC § 1280.3)         | Up to $5,000 (repeated violations)  |

Oregon penalty maximum ($5,000) is far below California first-violation penalty ($15,000).
""")

    # Joint Commission NPG 12 参考文档（A17）
    w(WS / "regulations" / "JC_NPG12_Health_Professional_Resource_Management.txt", """
JOINT COMMISSION NATIONAL PERFORMANCE GOAL 12
Health Professional Resource Management

Source: The Joint Commission — National Performance Goal 12
URL: https://aihc-assn.org/nurse-staffing-as-national-performance-goal-12/
Effective: January 1, 2026

═══════════════════════════════════════════════════════════════════════
OVERVIEW
═══════════════════════════════════════════════════════════════════════

The Joint Commission (TJC) has established National Performance Goal 12 (NPG 12)
as part of its 2026 accreditation standards. This is the FIRST TIME that nurse
staffing adequacy has been tied to formal hospital accreditation requirements.
Prior accreditation standards addressed staffing in general terms; NPG 12 creates
specific, measurable, and auditable expectations.

Effective Date: January 1, 2026
Standard Chapter: Health Professional Resource Management (replaces former NPSG chapter)

═══════════════════════════════════════════════════════════════════════
NPG.12.01.01 — LEADERSHIP STAFFING STANDARDS
═══════════════════════════════════════════════════════════════════════

STANDARD: Leadership ensures an adequate number and mix of qualified healthcare
professionals based on patient needs, care complexity, and organizational goals.

EP (Elements of Performance):
EP1: Hospital leadership establishes written policies defining minimum staffing standards
     for each patient care unit based on patient acuity, care complexity, and unit type.
EP2: Staffing standards are reviewed and updated at least annually and whenever
     significant operational changes occur.
EP3: Leadership allocates sufficient resources to meet staffing standards including
     budget, recruitment support, float pool maintenance, and agency contingency contracts.

SCORING: EP1-EP3 are all scored elements. All must be in compliance for full credit.

═══════════════════════════════════════════════════════════════════════
NPG.12.02.01 — NURSE EXECUTIVE LEADERSHIP
═══════════════════════════════════════════════════════════════════════

STANDARD: The nurse executive (CNO or equivalent) directs the development and
maintenance of staffing plans and participates in hospital governance related to
staffing decisions.

EP1: The nurse executive is responsible for establishing and maintaining staffing plans
     that address patient needs, care complexity, and regulatory requirements.
     REGULATORY NOTE: For California hospitals, staffing plans must meet or exceed
     the minimum ratios established in Title 22 § 70217.

EP2: The nurse executive participates in hospital governance and committee structures
     that influence staffing decisions (e.g., board committees, executive leadership team).

EP3: Staffing decisions and variance reporting are documented and traceable to the
     nurse executive's oversight function.

EP4: 24-hour, 7-day-per-week registered nursing oversight is established and maintained.
     Interpretation: There must be a registered nurse with supervisory authority
     available at all times in every patient care area.

EP5: Documentation of staffing decisions, variances, and corrective actions is
     maintained and available for accreditation review.

APPLICABILITY TO SVMC:
Miranda Chen (CNO) is the nurse executive responsible for NPG.12.02.01 compliance.
Her corrective action plan must demonstrate EP1-EP5 compliance beginning January 1, 2026.

═══════════════════════════════════════════════════════════════════════
NPG.12.06.01 — QUALITY AND SAFETY INTEGRATION (QAPI)
═══════════════════════════════════════════════════════════════════════

STANDARD: Staffing adequacy is evaluated as part of the Quality Assurance and
Performance Improvement (QAPI) program, with results reported to hospital leadership
and the governing body.

EP1: The QAPI program includes regular evaluation of staffing adequacy across all
     patient care units, with defined metrics and thresholds.

EP2: QAPI evaluation results related to staffing are formally reported to hospital
     leadership (executive team) at least quarterly.

EP3: QAPI evaluation results related to staffing are formally reported to the governing
     body (Board of Directors or equivalent) at least annually.

EP4: The QAPI program maintains correlation data linking staffing levels to quality and
     safety indicators, including but not limited to:
     - Pressure ulcer rates (PSI-3)
     - Patient fall rates
     - Medication error rates
     - Patient satisfaction scores
     - 30-day readmission rates
     Documentation requirement: Variance reports when staffing deviates from plan;
     correlation analysis between staffing levels and quality indicators.

═══════════════════════════════════════════════════════════════════════
DOCUMENTATION REQUIREMENTS SUMMARY
═══════════════════════════════════════════════════════════════════════

To demonstrate NPG 12 compliance, hospitals must maintain:

1. WRITTEN STAFFING PLANS (NPG.12.01.01):
   - Unit-specific staffing standards
   - Acuity-based adjustment methodology
   - On-call and float pool protocols

2. NURSE EXECUTIVE DOCUMENTATION (NPG.12.02.01):
   - Evidence of CNO participation in governance
   - Staffing plan sign-offs
   - Variance reporting records
   - 24/7 RN oversight verification

3. QAPI INTEGRATION (NPG.12.06.01):
   - Quarterly staffing adequacy evaluation reports
   - Correlation analyses (staffing vs. safety outcomes)
   - Reports to leadership and governing body
   - Corrective action documentation for identified gaps

4. ACUITY-BASED STAFFING ANALYSIS:
   - Patient classification system documenting acuity scores
   - Evidence that staffing assignments are informed by acuity data
   - Variance documentation when assignments deviate from acuity guidance

CURRENT SVMC STATUS vs NPG 12 REQUIREMENTS (preliminary gap analysis):
- EP NPG.12.01.01: Partially compliant — written policies exist but lack acuity methodology
- EP NPG.12.02.01 EP1-2: Compliant — CNO directs staffing and participates in governance
- EP NPG.12.02.01 EP4: PARTIALLY COMPLIANT — 24/7 RN oversight exists but documentation
  of supervisory coverage gaps during October violations is weak
- EP NPG.12.06.01 EP1: NON-COMPLIANT — QAPI does not currently include staffing metrics
- EP NPG.12.06.01 EP2-3: NON-COMPLIANT — staffing not reported to leadership/board quarterly
- EP NPG.12.06.01 EP4: NON-COMPLIANT — no correlation analysis linking staffing to outcomes

═══════════════════════════════════════════════════════════════════════
TRANSITION TIMELINE
═══════════════════════════════════════════════════════════════════════

NPG 12 becomes effective January 1, 2026. All Joint Commission accredited hospitals
must be in full compliance by their first survey date on or after January 1, 2026.

SVMC's next Joint Commission survey is scheduled for Q2 2026. The corrective action
plan prepared for CDPH should also incorporate NPG 12 gap remediation to ensure
accreditation readiness.
""")

    # CDPH Enforcement Actions データセット参考（A11に関連）
    w(WS / "regulations" / "CDPH_enforcement_actions_reference.txt", "\n".join([
        "CDPH HEALTH FACILITIES STATE ENFORCEMENT ACTIONS — REFERENCE DATA",
        "Source: CHHS Open Data Portal",
        "URL: https://data.chhs.ca.gov/dataset/healthcare-facility-state-enforcement-actions",
        "Coverage: July 1, 1997 through June 30, 2024",
        "",
        "DATASET FIELDS:",
        "enforcement_action_type, violation_category, penalty_amount, violation_date,",
        "appeal_status, facility_name, facility_type, county, license_number",
        "",
        "VIOLATION CATEGORIES RELEVANT TO SVMC:",
        "- NURSE STAFFING RATIOS (§ 70217): Most common category post-2019 (SB 227)",
        "- NHPPD (Nursing Hours Per Patient Day): Related tracking metric",
        "- RECORD KEEPING (§ 70217(d)): Failure to maintain shift-by-shift records",
        "",
        "HISTORICAL PENALTY DATA (sample, California 2020-2024):",
    ] + [
        f"Record {i:04d}: {['General Acute Care Hospital', 'Skilled Nursing Facility', 'Acute Psychiatric'][i % 3]}, "
        f"County: {['Los Angeles', 'San Diego', 'Orange', 'Riverside', 'Santa Clara', 'Sacramento'][i % 6]}, "
        f"Violation: {'NURSE STAFFING RATIOS' if i % 3 == 0 else 'NHPPD' if i % 3 == 1 else 'RECORD KEEPING'}, "
        f"Penalty: {'$15,000' if i % 5 != 0 else '$30,000'}, "
        f"Year: 202{(i // 50) % 5}, Status: {'Final' if i % 4 != 0 else 'Under Appeal'}"
        for i in range(1, 800)
    ]))

    # Massachusetts ICU 法规
    w(WS / "regulations" / "MA_ICU_958CMR8.00.txt", """
MASSACHUSETTS DEPARTMENT OF PUBLIC HEALTH
958 CMR 8.00 — ICU PATIENT ASSIGNMENT LAW

Source: Massachusetts MGL c. 111 § 231 / 958 CMR 8.00
URL: https://masshpc.gov/regulations-guidance/icu-nurse-staffing

STATUTORY BASIS: Chapter 155 of the Acts of 2014 (MGL c. 111 § 231)
REGULATION EFFECTIVE: July 3, 2015

SECTION 8.03 — MINIMUM ICU NURSE STAFFING RATIOS.

(1) NO hospital shall assign a registered nurse (RN) to provide direct patient care
    to more than two (2) patients simultaneously in an intensive care unit.

(2) ACUITY-BASED ASSIGNMENT:
    (a) STABLE ICU PATIENT: An ICU RN may be assigned to a maximum of TWO (2) patients
        if both patients are assessed as "stable" by the hospital's certified acuity tool.
    (b) UNSTABLE ICU PATIENT: An ICU RN assigned to an unstable patient shall have a
        maximum assignment of ONE (1) patient.
    (c) Assessment must use a DPH-certified acuity measurement tool.

(3) ABSOLUTE PROHIBITION: Assigning THREE (3) or more patients to a single ICU RN is
    STRICTLY PROHIBITED under any circumstances, including:
    - Staffing emergencies
    - Short notice absences
    - Natural disasters
    - Any other circumstances

COMPARISON WITH CALIFORNIA AND OREGON:
- Massachusetts: 1:1 or 1:2 based on patient stability (acuity tool required); hard ban on 1:3
- California: 1:2 maximum (Title 22 § 70217(a)(1)); acuity tool not explicitly required
- Oregon: 1:2 maximum (HB 2697 Section 2); matches California

KEY DIFFERENCE: Massachusetts requires a certified acuity tool to determine the 1:1 vs 1:2
assignment, whereas California and Oregon set a uniform maximum of 1:2 without acuity tiering.
""")


# --------------------------------------------------------------------------- #
# 3. 医院数据 CSV（确定性合成，注入真实质量问题和违规班次）
# --------------------------------------------------------------------------- #

UNITS = ["ICU", "Med/Surg", "Step-Down", "Telemetry", "ED", "Psychiatric"]
LEGAL_RATIOS = {"ICU": 2, "Med/Surg": 5, "Step-Down": 3, "Telemetry": 4, "ED": 4, "Psychiatric": 6}
SHIFTS = ["Day (07:00-19:00)", "Night (19:00-07:00)"]


def _iso_date(year, month, day):
    return f"{year:04d}-{month:02d}-{day:02d}"


def gen_nurse_roster(path: Path, seed: int = 101) -> list[dict]:
    """生成护士名册（含 charge nurse 标记，用于 Q2 的识别）。"""
    rng = random.Random(seed)
    nurses = []
    # ICU 护士（8 名在编 + 2 名差旅）
    icu_names = [
        ("RN-ICU-001", "Sarah Mitchell", "RN", "ICU", 1.0, False),
        ("RN-ICU-002", "James Park", "RN", "ICU", 1.0, False),
        ("RN-ICU-003", "Maria Gonzalez", "RN", "ICU", 1.0, True),   # Charge Nurse
        ("RN-ICU-004", "Kevin Walsh", "RN", "ICU", 1.0, False),
        ("RN-ICU-005", "Angela Reyes", "RN", "ICU", 0.9, False),
        ("RN-ICU-006", "Thomas Chen", "RN", "ICU", 1.0, False),
        ("RN-ICU-007", "Priya Sharma", "RN", "ICU", 1.0, False),
        ("RN-ICU-008", "David Okonkwo", "RN", "ICU", 0.8, False),
        ("RN-ICU-T01", "Jessica Brooks", "RN", "ICU", 1.0, False),  # Travel
        ("RN-ICU-T02", "Ryan Martinez", "RN", "ICU", 1.0, False),   # Travel
    ]
    # Med/Surg 护士（12 名在编）
    ms_names = [
        ("RN-MS-001", "Patricia Lowe", "RN", "Med/Surg", 1.0, True),   # Charge Nurse / Head Nurse
        ("RN-MS-002", "Donna Carter", "RN", "Med/Surg", 1.0, False),
        ("RN-MS-003", "Robert Kim", "LVN", "Med/Surg", 1.0, False),
        ("RN-MS-004", "Susan Walsh", "RN", "Med/Surg", 1.0, False),
        ("RN-MS-005", "Michael Brown", "RN", "Med/Surg", 0.9, False),
        ("RN-MS-006", "Lisa Nguyen", "RN", "Med/Surg", 1.0, False),
        ("RN-MS-007", "Carlos Ruiz", "LVN", "Med/Surg", 1.0, False),
        ("RN-MS-008", "Tamara Jackson", "RN", "Med/Surg", 1.0, False),
        ("RN-MS-009", "Wei Zhang", "RN", "Med/Surg", 0.8, False),
        ("RN-MS-010", "Helen Foster", "RN", "Med/Surg", 1.0, False),
        ("RN-MS-011", "George Thompson", "RN", "Med/Surg", 1.0, False),
        ("RN-MS-012", "Nancy Liu", "RN", "Med/Surg", 0.9, False),
    ]
    # Step-Down 护士（8 名）
    sd_names = [
        ("RN-SD-001", "Frank Morrison", "RN", "Step-Down", 1.0, True),  # Charge Nurse
        ("RN-SD-002", "Cindy Lee", "RN", "Step-Down", 1.0, False),
        ("RN-SD-003", "Barry White", "RN", "Step-Down", 1.0, False),
        ("RN-SD-004", "Alma Cruz", "RN", "Step-Down", 1.0, False),
        ("RN-SD-005", "Phil Owens", "RN", "Step-Down", 0.9, False),
        ("RN-SD-006", "Dana Ross", "RN", "Step-Down", 1.0, False),
        ("RN-SD-007", "Troy Watts", "RN", "Step-Down", 1.0, False),
        ("RN-SD-008", "Iris Bell", "RN", "Step-Down", 1.0, False),
    ]
    # Telemetry 护士（10 名）
    tel_names = [
        ("RN-TEL-001", "Vera Torres", "RN", "Telemetry", 1.0, True),   # Charge Nurse
        ("RN-TEL-002", "Sam Holt", "RN", "Telemetry", 1.0, False),
        ("RN-TEL-003", "Gina Evans", "RN", "Telemetry", 1.0, False),
        ("RN-TEL-004", "Nick Cooper", "RN", "Telemetry", 0.9, False),
        ("RN-TEL-005", "Lily Chang", "RN", "Telemetry", 1.0, False),
        ("RN-TEL-006", "Omar Hassan", "RN", "Telemetry", 1.0, False),
        ("RN-TEL-007", "Fran Murphy", "RN", "Telemetry", 1.0, False),
        ("RN-TEL-008", "Aaron Scott", "RN", "Telemetry", 0.8, False),
        ("RN-TEL-009", "Beth Flores", "RN", "Telemetry", 1.0, False),
        ("RN-TEL-010", "Don Gibson", "RN", "Telemetry", 1.0, False),
    ]
    # ED + Psych
    ed_names = [
        ("RN-ED-001", "Jack Stone", "RN", "ED", 1.0, True),
        ("RN-ED-002", "Cath Dennis", "RN", "ED", 1.0, False),
        ("RN-ED-003", "Mike Chan", "RN", "ED", 1.0, False),
        ("RN-ED-004", "Rosa Diaz", "RN", "ED", 1.0, False),
        ("RN-ED-005", "Al Newton", "RN", "ED", 0.9, False),
        ("RN-ED-006", "Lena Fox", "LVN", "ED", 1.0, False),
    ]
    psych_names = [
        ("RN-PSY-001", "Ben Cole", "RN", "Psychiatric", 1.0, True),
        ("RN-PSY-002", "Amy West", "RN", "Psychiatric", 1.0, False),
        ("RN-PSY-003", "Raj Patel", "PT", "Psychiatric", 1.0, False),  # Psych Tech
        ("RN-PSY-004", "Nina Green", "RN", "Psychiatric", 1.0, False),
        ("RN-PSY-005", "Leo Burns", "LVN", "Psychiatric", 1.0, False),
    ]

    for grp in [icu_names, ms_names, sd_names, tel_names, ed_names, psych_names]:
        for nid, name, lic, unit, fte, is_charge in grp:
            nurses.append({
                "nurse_id": nid,
                "name": name,
                "license_type": lic,
                "unit": unit,
                "fte": fte,
                "is_charge_nurse": is_charge,
            })

    buf = io.StringIO()
    w_csv = csv.DictWriter(buf, fieldnames=["nurse_id", "name", "license_type", "unit",
                                             "fte", "is_charge_nurse"])
    w_csv.writeheader()
    w_csv.writerows(nurses)
    w(path, buf.getvalue())
    return nurses


def gen_staffing_log(path: Path, nurses: list[dict], seed: int = 202) -> list[dict]:
    """生成 4 个月（2024-07 ~ 2024-10）每日每班次每护士一行的详细排班日志。
    返回班次记录列表（用于后续 check 锚点）。目标：~60k+ tokens。"""
    rng = random.Random(seed)
    rows = []
    shift_id = 1000

    # 建立护士索引
    unit_nurses = {}
    for n in nurses:
        unit_nurses.setdefault(n["unit"], []).append(n)

    # 月份 7-10（4个月，每月约31天）
    months = [(2024, 7), (2024, 8), (2024, 9), (2024, 10)]
    for year, month in months:
        days_in_month = calendar.monthrange(year, month)[1]
        for day in range(1, days_in_month + 1):
            date_str = _iso_date(year, month, day)
            for shift_idx, shift_name in enumerate(SHIFTS):
                for unit_idx, unit in enumerate(UNITS):
                    shift_id += 1
                    unit_nur = unit_nurses.get(unit, [])
                    legal_max = LEGAL_RATIOS[unit]
                    available = [n for n in unit_nur if not n["is_charge_nurse"]]
                    charge_nurses = [n for n in unit_nur if n["is_charge_nurse"]]

                    n_staff = max(2, len(available) // 2) + rng.randint(0, 1)
                    is_violation = False
                    has_charge_error = False

                    # 仅 10 月注入特定违规（CDPH 检查期）
                    if month == 10:
                        # ICU 夜班 Day 5-7：charge nurse 被错误纳入比率
                        if unit == "ICU" and shift_name.startswith("Night") and 5 <= day <= 7:
                            n_staff_recorded = 3  # 错误记录（含 charge）
                            patients = 5
                            has_charge_error = True
                            is_violation = True
                            nurses_on_shift = [
                                charge_nurses[0] if charge_nurses else available[0],
                                available[0], available[1] if len(available) > 1 else available[0]
                            ]
                        # Med/Surg 夜班 Day 12-18：超过 1:5
                        elif unit == "Med/Surg" and shift_name.startswith("Night") and 12 <= day <= 18:
                            n_staff_recorded = 2
                            patients = 12
                            is_violation = True
                            nurses_on_shift = available[:2] if len(available) >= 2 else available
                        # Med/Surg 夜班 Day 22-24
                        elif unit == "Med/Surg" and shift_name.startswith("Night") and 22 <= day <= 24:
                            n_staff_recorded = 2
                            patients = 11
                            is_violation = True
                            nurses_on_shift = available[2:4] if len(available) >= 4 else available[:2]
                        else:
                            n_staff_recorded = n_staff
                            patients = max(1, n_staff_recorded * legal_max - rng.randint(0, 2))
                            nurses_on_shift = available[:n_staff_recorded]
                    else:
                        n_staff_recorded = n_staff
                        patients = max(1, n_staff_recorded * legal_max - rng.randint(0, 3))
                        nurses_on_shift = available[:n_staff_recorded]

                    if not nurses_on_shift:
                        nurses_on_shift = available[:1] if available else unit_nur[:1]

                    # 每个护士单独一行（详细日志）
                    per_nurse_patients = round(patients / max(len(nurses_on_shift), 1), 2)
                    for nurse in nurses_on_shift:
                        rows.append({
                            "shift_id": f"SH-{shift_id:04d}",
                            "date": date_str,
                            "shift": shift_name,
                            "unit": unit,
                            "nurse_id": nurse["nurse_id"],
                            "nurse_name": nurse["name"],
                            "license_type": nurse["license_type"],
                            "is_charge_nurse": nurse["is_charge_nurse"],
                            "nurses_on_duty_total": len(nurses_on_shift),
                            "unit_patient_count": patients,
                            "nurse_patient_assignment": int(per_nurse_patients) if per_nurse_patients == int(per_nurse_patients) else per_nurse_patients,
                            "ratio_as_recorded": round(patients / max(len(nurses_on_shift), 1), 2),
                            "charge_nurse_included_error": has_charge_error and nurse["is_charge_nurse"],
                            "is_shift_violation": is_violation,
                            "legal_max_ratio": legal_max,
                            "notes": "CHARGE NURSE IN ADMIN ROLE — should not count toward ratio" if (has_charge_error and nurse["is_charge_nurse"]) else (
                                     "VIOLATION: ratio exceeds legal maximum" if is_violation and not nurse["is_charge_nurse"] else ""),
                        })

    buf = io.StringIO()
    fieldnames = ["shift_id", "date", "shift", "unit", "nurse_id", "nurse_name",
                  "license_type", "is_charge_nurse", "nurses_on_duty_total",
                  "unit_patient_count", "nurse_patient_assignment", "ratio_as_recorded",
                  "charge_nurse_included_error", "is_shift_violation", "legal_max_ratio", "notes"]
    w_csv = csv.DictWriter(buf, fieldnames=fieldnames)
    w_csv.writeheader()
    w_csv.writerows(rows)
    w(path, buf.getvalue())
    return rows


def gen_census_data(path: Path, seed: int = 303) -> None:
    """生成 10 月各科室日均患者数。"""
    rng = random.Random(seed)
    rows = []
    avg_census = {"ICU": 8, "Med/Surg": 28, "Step-Down": 12, "Telemetry": 14, "ED": 18, "Psychiatric": 14}
    for day in range(1, 32):
        date_str = _iso_date(2024, 10, day)
        for unit in UNITS:
            base = avg_census[unit]
            census = base + rng.randint(-2, 2)
            rows.append({"date": date_str, "unit": unit, "patient_census": max(1, census)})

    buf = io.StringIO()
    w_csv = csv.DictWriter(buf, fieldnames=["date", "unit", "patient_census"])
    w_csv.writeheader()
    w_csv.writerows(rows)
    w(path, buf.getvalue())


def gen_on_call_lists(ws: Path, seed: int = 404) -> None:
    """生成在职 on-call 名单（含 float pool）和废弃旧版名单（V6 红鲱鱼）。"""
    rng = random.Random(seed)
    # 当前版本 on-call 名单
    current = [
        {"nurse_id": "RN-ICU-T01", "name": "Jessica Brooks", "unit": "ICU",
         "on_call_type": "float_pool", "available_shifts": "Night,Day"},
        {"nurse_id": "RN-ICU-T02", "name": "Ryan Martinez", "unit": "ICU",
         "on_call_type": "float_pool", "available_shifts": "Night,Day"},
        {"nurse_id": "RN-MS-010", "name": "Helen Foster", "unit": "Med/Surg",
         "on_call_type": "scheduled_on_call", "available_shifts": "Night"},
        {"nurse_id": "RN-MS-011", "name": "George Thompson", "unit": "Med/Surg",
         "on_call_type": "scheduled_on_call", "available_shifts": "Night"},
        {"nurse_id": "RN-SD-007", "name": "Troy Watts", "unit": "Step-Down",
         "on_call_type": "float_pool", "available_shifts": "Day,Night"},
        {"nurse_id": "RN-SD-008", "name": "Iris Bell", "unit": "Step-Down",
         "on_call_type": "float_pool", "available_shifts": "Day,Night"},
        {"nurse_id": "RN-TEL-009", "name": "Beth Flores", "unit": "Telemetry",
         "on_call_type": "scheduled_on_call", "available_shifts": "Night"},
        {"nurse_id": "RN-TEL-010", "name": "Don Gibson", "unit": "Telemetry",
         "on_call_type": "scheduled_on_call", "available_shifts": "Night"},
    ]
    buf = io.StringIO()
    w_csv = csv.DictWriter(buf, fieldnames=["nurse_id", "name", "unit", "on_call_type", "available_shifts"])
    w_csv.writeheader()
    w_csv.writerows(current)
    w(ws / "hospital_data" / "SVMC_on_call_list_current.csv", buf.getvalue())

    # 废弃的旧版 on-call 名单 v2023-10（V6 红鲱鱼）
    # 包含已离职的护士
    obsolete = [
        {"nurse_id": "RN-MS-OLD-01", "name": "Amanda Price (RESIGNED)", "unit": "Med/Surg",
         "on_call_type": "scheduled_on_call", "available_shifts": "Night",
         "status": "OBSOLETE - nurse resigned 2024-03-15"},
        {"nurse_id": "RN-ICU-OLD-01", "name": "Steven Marsh (FMLA)", "unit": "ICU",
         "on_call_type": "float_pool", "available_shifts": "Day",
         "status": "OBSOLETE - on FMLA leave indefinite"},
        {"nurse_id": "RN-TEL-OLD-01", "name": "Carol Adams (TERMINATED)", "unit": "Telemetry",
         "on_call_type": "scheduled_on_call", "available_shifts": "Night",
         "status": "OBSOLETE - contract terminated 2024-06-01"},
        {"nurse_id": "RN-SD-OLD-01", "name": "Pete Murray (TRANSFERRED)", "unit": "Step-Down",
         "on_call_type": "float_pool", "available_shifts": "Day",
         "status": "OBSOLETE - transferred to St. Joseph's 2024-08-20"},
    ]
    buf2 = io.StringIO()
    fields2 = ["nurse_id", "name", "unit", "on_call_type", "available_shifts", "status"]
    w_csv2 = csv.DictWriter(buf2, fieldnames=fields2)
    w_csv2.writeheader()
    w_csv2.writerows(obsolete)
    # 标注：旧版名单（2023年10月）— 已废弃，不得用于合规计算
    content = f"# ARCHIVE VERSION: SVMC_on_call_list_v2023-10.csv\n"
    content += "# WARNING: THIS FILE IS OBSOLETE (archived 2024-09-01)\n"
    content += "# Do NOT use for current on-call calculations. Use SVMC_on_call_list_current.csv\n"
    content += buf2.getvalue()
    w(ws / "hospital_data" / "SVMC_on_call_list_v2023-10_ARCHIVED.csv", content)


def gen_fmla_schedule(path: Path) -> None:
    """FMLA/CFRA 请假计划（ICU 空缺 3 人的原因）。"""
    rows = [
        {"nurse_id": "RN-ICU-004", "name": "Kevin Walsh", "unit": "ICU",
         "leave_type": "FMLA", "start_date": "2024-09-15", "end_date": "2024-11-30",
         "fte_gap": 1.0, "backfill_status": "Travel nurse RN-ICU-T01 covers partial"},
        {"nurse_id": "RN-ICU-006", "name": "Thomas Chen", "unit": "ICU",
         "leave_type": "FMLA", "start_date": "2024-10-01", "end_date": "2024-12-15",
         "fte_gap": 1.0, "backfill_status": "Travel nurse RN-ICU-T02 covers partial"},
        {"nurse_id": "RN-ICU-VACANCY", "name": "[VACANCY - resigned 2024-09-01]", "unit": "ICU",
         "leave_type": "VACANCY", "start_date": "2024-09-01", "end_date": "TBD",
         "fte_gap": 1.0, "backfill_status": "Recruitment in progress - no backfill yet"},
        {"nurse_id": "RN-MS-005", "name": "Michael Brown", "unit": "Med/Surg",
         "leave_type": "CFRA", "start_date": "2024-10-07", "end_date": "2024-10-28",
         "fte_gap": 0.9, "backfill_status": "No backfill arranged"},
        {"nurse_id": "RN-MS-009", "name": "Wei Zhang", "unit": "Med/Surg",
         "leave_type": "FMLA", "start_date": "2024-10-14", "end_date": "2024-11-14",
         "fte_gap": 0.8, "backfill_status": "No backfill arranged"},
    ]
    buf = io.StringIO()
    w_csv = csv.DictWriter(buf, fieldnames=["nurse_id", "name", "unit", "leave_type",
                                             "start_date", "end_date", "fte_gap", "backfill_status"])
    w_csv.writeheader()
    w_csv.writerows(rows)
    w(path, buf.getvalue())


def gen_travel_nurse_contracts(path: Path) -> None:
    """临时/差旅护士合同摘要。"""
    rows = [
        {"contract_id": "TN-2024-001", "nurse_id": "RN-ICU-T01", "name": "Jessica Brooks",
         "unit": "ICU", "agency": "Medical Staffing Network", "start_date": "2024-09-20",
         "end_date": "2024-12-20", "hourly_rate": 85, "icu_certified": True,
         "float_pool_eligible": True, "notes": "ICU-certified, float pool eligible"},
        {"contract_id": "TN-2024-002", "nurse_id": "RN-ICU-T02", "name": "Ryan Martinez",
         "unit": "ICU", "agency": "AMN Healthcare", "start_date": "2024-10-05",
         "end_date": "2025-01-05", "hourly_rate": 92, "icu_certified": True,
         "float_pool_eligible": True, "notes": "ICU-certified, float pool eligible"},
    ]
    buf = io.StringIO()
    w_csv = csv.DictWriter(buf, fieldnames=["contract_id", "nurse_id", "name", "unit",
                                             "agency", "start_date", "end_date", "hourly_rate",
                                             "icu_certified", "float_pool_eligible", "notes"])
    w_csv.writeheader()
    w_csv.writerows(rows)
    w(path, buf.getvalue())


# --------------------------------------------------------------------------- #
# 4. 通讯记录与文档
# --------------------------------------------------------------------------- #
def gen_communications(ws: Path) -> None:
    # Slack DM — CNO ↔ Dr. Okafor ICU 合规争论
    slack_dm = {
        "channel": "slack_dm_miranda_okafor",
        "participants": ["Miranda Chen (CNO)", "Dr. James Okafor (ICU Medical Director)"],
        "messages": [
            {"timestamp": "2024-10-28T09:15:00", "sender": "Miranda Chen",
             "text": "James, CDPH has flagged three ICU night shifts in early October as potential ratio violations. Shifts SH-1008, SH-1014, SH-1020. The inspector says the charge nurse RN-ICU-003 (Maria Gonzalez) was counted as a direct care nurse when she was actually doing administrative rounds. Have you reviewed?"},
            {"timestamp": "2024-10-28T09:32:00", "sender": "Dr. James Okafor",
             "text": "Miranda, I reviewed those shifts personally. Maria was PROVIDING direct patient care on those nights — she was doing both charge duties AND bedside care. So she absolutely counts toward the ratio. We were compliant. The inspector is wrong."},
            {"timestamp": "2024-10-28T09:45:00", "sender": "Miranda Chen",
             "text": "The regulation is clear — Title 22 § 70217(c) says the charge nurse only counts when 'actively engaged in the direct care of patients', not when performing administrative duties. The staffing log shows her as 'Charge/Admin Rounds' for those shifts. We need to correct the log and acknowledge the violations."},
            {"timestamp": "2024-10-28T10:02:00", "sender": "Dr. James Okafor",
             "text": "I'll defer to Legal's interpretation. But for the record, I believe those shifts were compliant based on what I observed."},
        ]
    }
    wj(ws / "communications" / "slack_cno_dm_history.json", slack_dm)

    # 工会 Email — 违规时间线争论
    union_email = {
        "thread_subject": "SVMC Nursing Ratio Violations — Union Grievance Timeline",
        "participants": ["Kevin Torres (SEIU Union Rep)", "Miranda Chen (CNO)", "HR Director Tom Bradley"],
        "emails": [
            {"date": "2024-10-30", "from": "Kevin Torres",
             "to": ["Miranda Chen", "Tom Bradley"],
             "body": "Dear Ms. Chen, The union has documented nurse-to-patient ratio violations at SVMC dating back to OCTOBER 2023 — a full year before the recent CDPH inspection. Our records show Med/Surg night shift violations beginning October 12, 2023. We are attaching historical staffing records. This is not a recent crisis — it is a systemic failure. We demand full disclosure and retroactive penalty assessment. The attached 2023-10 on-call list (v2023-10) shows inadequate float pool coverage was already evident a year ago.",
             "attachments": ["staffing_oct2023_union_records.pdf",
                             "SVMC_on_call_list_v2023-10_union_copy.csv"]},
            {"date": "2024-10-31", "from": "Tom Bradley",
             "to": ["Kevin Torres"],
             "cc": ["Miranda Chen"],
             "body": "Mr. Torres, We dispute the characterization of these violations as dating back to October 2023. Our internal records show compliant staffing during that period. The union's 2023 on-call list attachment references ARCHIVED data (v2023-10) that was superseded. CDPH's current inspection covers only October 2024 violations. We are not conceding a 12-month violation history.",
             "attachments": []},
            {"date": "2024-11-02", "from": "Kevin Torres",
             "to": ["Miranda Chen", "Tom Bradley"],
             "body": "For your reference: the 2023-10 on-call list we attached shows that Carol Adams (RN-TEL-OLD-01), Pete Murray (RN-SD-OLD-01), and Amanda Price (RN-MS-OLD-01) were listed as available — all three have since departed. This 33% attrition of the on-call pool is precisely what caused the 2024 violations. Using the 2023 roster to claim adequacy is inappropriate — the CURRENT on-call list must be used.",
             "attachments": []}
        ]
    }
    wj(ws / "communications" / "email_nurse_union_oct2024.json", union_email)

    # 飞书合规顾问群（含失真摘要）— V5 诱饵
    feishu = {
        "group_name": "合规应急",
        "members": ["Dr. Aisha Rahman", "Compliance Officer Chen Li", "Legal Counsel Wei Huang", "Miranda Chen (CNO)"],
        "messages": [
            {"timestamp": "2024-10-29T14:00:00", "sender": "Chen Li",
             "text": "大家好，我刚整理了一下加州罚款金额。根据 BOT 自动摘要，首次违规罚款是 $10,000，再次违规是 $30,000。大家确认一下这个数字？"},
            {"timestamp": "2024-10-29T14:15:00", "sender": "Dr. Aisha Rahman",
             "text": "等一下，我需要核实一下。BOT 摘要有时会出错。我记得 AFL-23-27 里的数字不是 $10,000…"},
            {"timestamp": "2024-10-29T14:30:00", "sender": "Wei Huang",
             "text": "对，根据我查到的 AFL-23-27 原文，首次违规应该是 $15,000，不是 $10,000。BOT 摘要数字有误。请以原始法规文件为准。"},
            {"timestamp": "2024-10-29T14:45:00", "sender": "Chen Li",
             "text": "还有一个问题：医院今年冬天流感季人手不够，能否以'季节性流感不可预见'为由豁免？"},
            {"timestamp": "2024-10-29T15:00:00", "sender": "Dr. Aisha Rahman",
             "text": "CDPH AFL-23-27 明确指出：季节性流感高峰期不自动构成'不可预见且不可控'情形。医院被期望提前为已知的季节性需求做好准备。这个豁免理由不成立。"},
            {"timestamp": "2024-10-29T15:10:00", "sender": "Miranda Chen",
             "text": "已记录：首次违规 $15,000（非 $10,000），季节性流感不自动豁免。以 AFL-23-27 原文为准。"},
        ],
        "bot_auto_summary": {
            "WARNING": "BOT AUTO-SUMMARY — NOT AUTHORITATIVE. Contains known errors.",
            "summary": "讨论要点：首次违规罚款 $10,000（[ERROR: actual is $15,000]），季节性流感'可能豁免'（[ERROR: AFL-23-27 explicitly states seasonal flu is NOT automatically exempt]）。此摘要仅供参考，请以原始法规文件为准。",
            "generated_at": "2024-10-29T15:30:00",
            "note": "This bot summary contains DISTORTED figures. Do NOT use for compliance calculations."
        }
    }
    wj(ws / "communications" / "feishu_compliance_group.json", feishu)

    # CDPH 检查来函
    w(ws / "communications" / "cdph_inspection_letter.txt", """
CALIFORNIA DEPARTMENT OF PUBLIC HEALTH
Health Facility Evaluation Branch

DATE: October 25, 2024
TO: Sutter Valley Medical Center (SVMC)
    350 Valley Medical Drive, Sacramento, CA 95814
FROM: Inspector Linda Wu, CDPH Health Facilities Evaluation Branch
RE: Statement of Deficiencies Following Unannounced Inspection (October 22-23, 2024)
FACILITY LICENSE NO.: 050123-SVMC

STATEMENT OF DEFICIENCIES (CMS-2567 / CDPH-2567)

Following an unannounced inspection conducted October 22-23, 2024, the following
deficiencies have been identified at Sutter Valley Medical Center:

DEFICIENCY TAG F-701 — NURSE STAFFING RATIOS (Title 22 § 70217)

FINDING 1: ICU UNIT — CHARGE NURSE MISCOUNTING
Review of staffing records for October 5-7, 2024 (Night Shifts SH-1008, SH-1014, SH-1020)
revealed that the facility incorrectly counted a Charge Nurse performing administrative
rounds toward the direct patient care ratio. Per Title 22 § 70217(c), a Charge Nurse is
counted in the ratio ONLY when actively engaged in direct patient care.

After correcting for this error:
- Shift SH-1008 (Oct 5, Night): 2 direct-care RNs, 5 ICU patients → ratio 1:2.5 (VIOLATION)
- Shift SH-1014 (Oct 6, Night): 2 direct-care RNs, 5 ICU patients → ratio 1:2.5 (VIOLATION)
- Shift SH-1020 (Oct 7, Night): 2 direct-care RNs, 5 ICU patients → ratio 1:2.5 (VIOLATION)
Legal maximum for ICU: 1:2 (§ 70217(a)(1))

FINDING 2: MED/SURG UNIT — NIGHT SHIFT RATIO VIOLATIONS (Oct 12-18)
Staffing records for Med/Surg Night Shifts October 12-18, 2024 show:
- 7 consecutive night shifts with 2 RNs covering 11-12 patients each
- Legal maximum: 1:5 (§ 70217(a)(11)); actual ratios ranged from 1:5.5 to 1:6.0
- Violations attributed to concurrent FMLA leave (RN-MS-005 and RN-MS-009)
- On-call list was NOT fully exhausted per records — Nurses RN-MS-010 and RN-MS-011
  were on the on-call list but records show only one contact attempt each

FINDING 3: MED/SURG UNIT — ADDITIONAL NIGHT VIOLATIONS (Oct 22-24)
3 additional Med/Surg night shift violations identified (2 RNs, 11 patients each)

PENALTY NOTICE:
This is SVMC's FIRST documented nurse staffing ratio violation under H&SC § 1280.3
(no prior violations on record within the past 3 years).
Administrative penalties will be assessed per H&SC § 1280.3.

REMEDIATION DEADLINE:
A Corrective Action Plan (CAP) must be submitted within THIRTY (30) days
(by November 22, 2024).

REQUIRED DOCUMENTATION:
1. Updated staffing logs for all units (Title 22 § 70217(d))
2. Revised on-call list showing SB 596-compliant float pool composition
3. Two-week prospective staffing schedule demonstrating compliance

Inspector: Linda Wu
CDPH Health Facilities Evaluation Branch
Date: October 25, 2024
""")


def gen_reports_and_scripts(ws: Path) -> None:
    """生成初始报告草稿和验证脚本。"""
    w(ws / "reports" / "SVMC_staffing_deficiency_report_draft.txt", """
DRAFT — SVMC STAFFING DEFICIENCY CORRECTIVE ACTION REPORT
Prepared by: Office of the Chief Nursing Officer
Date: October 28, 2024
Status: DRAFT (pending CNO review)

EXECUTIVE SUMMARY:
Sutter Valley Medical Center acknowledges the staffing ratio deficiencies identified
by CDPH during the October 22-23, 2024 inspection. This report documents the root
causes and proposed corrective measures.

SECTION 1: VIOLATIONS IDENTIFIED
[Pending completion — agent to analyze staffing log and CDPH letter]

SECTION 2: ROOT CAUSE ANALYSIS
Primary factors contributing to violations:
1. ICU staffing gap: 3 FTE deficit due to concurrent FMLA leaves (2 nurses) and 1 vacancy
2. Med/Surg night: FMLA coverage gaps compounded by insufficient on-call pool
3. Charge nurse miscounting: Training gap in charge nurse documentation

SECTION 3: PENALTY ASSESSMENT
[Pending — agent to calculate per H&SC § 1280.3 and AFL-23-27]

SECTION 4: CORRECTIVE MEASURES
[Pending completion]
""")

    w(ws / "reports" / "SVMC_corrective_action_plan_draft.txt", """
DRAFT — CORRECTIVE ACTION PLAN (CAP)
Facility: Sutter Valley Medical Center (SVMC)
Submission Deadline: November 22, 2024

IMMEDIATE ACTIONS (within 7 days):
1. Update staffing documentation to reflect correct charge nurse classification
2. Audit all October 2024 shifts for Charge Nurse miscounting
3. Update on-call list to comply with SB 596 definition (formal on-call roster only)

SHORT-TERM ACTIONS (within 30 days):
1. Recruit 2 permanent ICU RNs to fill vacancy and FMLA backfill positions
2. Expand float pool to include minimum 3 ICU-certified nurses
3. Implement mandatory monthly staffing ratio audit
4. Train all charge nurses on documentation requirements under § 70217(c)

MEDIUM-TERM ACTIONS (within 90 days):
1. Implement electronic staffing management system with real-time ratio alerts
2. Develop weather/seasonal staffing contingency plans (influenza season prep)
3. Establish formal FMLA coverage protocol with mandatory backfill trigger at day 14

CERTIFICATION:
[Pending CNO signature]
""")

    # validate_ratios.py 脚本
    w(ws / "scripts" / "validate_ratios.py", """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
validate_ratios.py — Validates that all shifts in a staffing CSV comply with
California Title 22 § 70217 nurse-to-patient ratio requirements.

Usage: python validate_ratios.py <staffing_log.csv>
\"\"\"
import csv
import sys
from pathlib import Path

LEGAL_RATIOS = {
    "ICU": 2,
    "Med/Surg": 5,
    "Step-Down": 3,
    "Telemetry": 4,
    "ED": 4,
    "Psychiatric": 6,
}

def validate(log_path: str) -> None:
    violations = []
    with open(log_path, encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            unit = row.get("unit", "")
            legal_max = LEGAL_RATIOS.get(unit)
            if legal_max is None:
                continue
            try:
                nurses = int(row.get("nurses_on_duty_count", 0))
                patients = int(row.get("patient_count", 0))
            except ValueError:
                continue
            if nurses <= 0:
                continue
            ratio = patients / nurses
            if ratio > legal_max:
                violations.append({
                    "shift_id": row.get("shift_id"),
                    "unit": unit,
                    "ratio": round(ratio, 2),
                    "legal_max": legal_max,
                })
    if violations:
        print(f"VIOLATIONS FOUND: {len(violations)}")
        for v in violations:
            print(f"  {v['shift_id']} ({v['unit']}): actual {v['ratio']}:1, legal max 1:{v['legal_max']}")
    else:
        print("NO VIOLATIONS — all shifts compliant")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: validate_ratios.py <staffing_log.csv>")
        sys.exit(1)
    validate(sys.argv[1])
""")

    w(ws / "scripts" / "generate_cdph_log.py", """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
generate_cdph_log.py — Generates a CDPH-format staffing log CSV from raw
scheduling data, per Title 22 § 70217(d) record-keeping requirements.

Usage: python generate_cdph_log.py <input.csv> <output.csv>
\"\"\"
import csv
import sys

FIELDNAMES = ["date", "shift_start", "shift_end", "unit", "nurse_id",
              "license_type", "patient_count", "ratio"]

def generate_log(input_path: str, output_path: str) -> None:
    rows = []
    with open(input_path, encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            shift_parts = row.get("shift", "").split(" ")
            shift_start = shift_parts[1].split("-")[0] if len(shift_parts) > 1 else "07:00"
            shift_end = shift_parts[1].split("-")[1] if len(shift_parts) > 1 else "19:00"
            try:
                nurses = int(row.get("nurses_on_duty_count", 1))
                patients = int(row.get("patient_count", 0))
                ratio = round(patients / max(nurses, 1), 2)
            except ValueError:
                ratio = 0.0
            for nid in row.get("nurse_ids", "").split(","):
                nid = nid.strip()
                if not nid:
                    continue
                rows.append({
                    "date": row.get("date"),
                    "shift_start": shift_start,
                    "shift_end": shift_end,
                    "unit": row.get("unit"),
                    "nurse_id": nid,
                    "license_type": row.get("license_type", "RN"),
                    "patient_count": patients,
                    "ratio": f"{ratio:.2f}",
                })
    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated {len(rows)} entries in {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: generate_cdph_log.py <input.csv> <output.csv>")
        sys.exit(1)
    generate_log(sys.argv[1], sys.argv[2])
""")


# --------------------------------------------------------------------------- #
# 5. Sessions（主 + 4 history）
# --------------------------------------------------------------------------- #
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("slack_nursing_ops", TID)
    s_email = gen_session_id("union_email_hr", TID)
    s_feishu = gen_session_id("feishu_compliance", TID)
    s_cdph = gen_session_id("cdph_official", TID)

    # 主 session：背景 + 工作框架
    sb = SessionBuilder(main_id, CWD, "2024-10-28T08:00:00", is_main=True)
    sb.add_user(
        "You are HealthOps AI, the healthcare compliance assistant for Miranda Chen "
        "(Chief Nursing Officer) at Sutter Valley Medical Center (SVMC), Sacramento, CA.\n\n"
        "SVMC is a 350-bed General Acute Care Hospital. We are under pressure from a CDPH "
        "Statement of Deficiencies issued October 25, 2024. Key issues:\n"
        "- ICU night shifts Oct 5-7: charge nurse incorrectly counted toward ratio\n"
        "- Med/Surg night shifts Oct 12-18 and Oct 22-24: nurse shortage caused ratio violations\n"
        "- 30-day deadline to submit Corrective Action Plan (by Nov 22, 2024)\n\n"
        "Authoritative sources in workspace:\n"
        "- `regulations/CA_Title22_§70217_full.txt` — nurse-to-patient ratios\n"
        "- `regulations/CA_HSC_§1280.3_penalties.txt` — administrative penalties\n"
        "- `regulations/CA_AFL-23-27_enforcement.txt` — CDPH enforcement guidance\n"
        "- `hospital_data/SVMC_staffing_log_oct2024.csv` — October 2024 staffing log\n"
        "- `hospital_data/SVMC_nurse_roster.csv` — nurse roster with charge nurse flags\n\n"
        "IMPORTANT: The Feishu compliance group bot auto-summary (feishu_compliance_group.json) "
        "contains ERRORS (e.g. $10,000 first violation — WRONG; it is $15,000). "
        "Always verify numbers against the regulation files.\n\n"
        "House preferences (apply throughout, even when not restated):\n"
        "- P1: All currency amounts as integers in USD, no decimal points, no thousand separators "
        "(e.g., 15000, not $15,000.00 or 15,000).\n"
        "- P2: Markdown reports — every case/shift uses ### (level-3) heading, NOT ## (level-2).\n"
        "- P3: CSV files — UTF-8 encoding, date fields YYYY-MM-DD, ratio fields two decimal places.\n"
        "- P4: All JSON field names in snake_case; array fields use plural names "
        "(e.g., violations, files, corrective_measures).\n"
        "- P5: recommendation/action fields — plain text only, no nested JSON, max 150 chars.\n\n"
        "History sessions available: Slack #nursing-ops, Union Email thread, "
        "Feishu compliance group, CDPH official correspondence. "
        "Start with `exec ls -R` and reading SOUL.md, then await each task."
    )
    sb.add_assistant(
        "Understood. I have reviewed AGENTS.md and SOUL.md. Working framework:\n\n"
        "1. Authoritative sources: regulation files under `regulations/`. "
        "Feishu bot auto-summary is explicitly flagged as containing errors ($10,000 is WRONG — "
        "the correct first-violation penalty is $15,000 per H&SC § 1280.3 and AFL-23-27).\n\n"
        "2. Charge nurse rule (§ 70217(c)): counts toward ratio ONLY when providing direct "
        "patient care — not during administrative/supervisory duties.\n\n"
        "3. SB 596 temporal boundary: violations before 2026-01-01 use legacy single-inspection "
        "rule; violations on/after 2026-01-01 are separate daily violations.\n\n"
        "4. Update awareness: if new CDPH notices or settlement agreements supersede prior data, "
        "the later document controls.\n\n"
        "5. Preferences: P1 (integer USD), P2 (### headings in MD), P3 (CSV format), "
        "P4 (snake_case JSON), P5 (plain text recommendations ≤ 150 chars).\n\n"
        "Ready for the first task. Running `exec ls -R` to inspect workspace."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # S2 Slack #nursing-ops — ICU charge nurse 合规争论 + Med/Surg 承认违规
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2024-10-26T09:00:00",
        [
            ("[Slack #nursing-ops Dr. James Okafor Sun Oct 27 09:00 PDT 2024] "
             "I've reviewed the CDPH findings. I categorically disagree with the charge nurse "
             "finding. Nurse Maria Gonzalez (RN-ICU-003) was doing BOTH admin rounds AND direct "
             "patient care on those ICU shifts. She should count. We were at 1:2 or better.",
             "Noted. Per § 70217(c), the Charge Nurse counts toward the ratio ONLY when "
             "'actively engaged in the direct care of patients' — not when also performing "
             "administrative duties. The staffing log entries show 'Charge/Admin Rounds' for "
             "those shifts. I will analyze the log data and apply the regulation verbatim."),
            ("[Slack #nursing-ops Patricia Lowe Sun Oct 27 10:15 PDT 2024] "
             "Miranda, I have to be honest — the Med/Surg night shifts in October were "
             "really bad. When Wei Zhang and Michael Brown both went on FMLA/CFRA in the "
             "same two weeks, we had only 2 nurses covering 11-12 patients on nights. "
             "That's clearly over the 1:5 limit. We tried calling the on-call list but "
             "I don't think we called every name — we stopped after two calls.",
             "Confirmed. Med/Surg night violations appear to stem from concurrent FMLA/CFRA "
             "absences without adequate on-call coverage. The failure to exhaust the full "
             "on-call list before declaring the shift understaffed is significant for the "
             "exemption defense under AFL-23-27 Prong 3 — the list must be fully exhausted."),
            ("[Slack #nursing-ops Miranda Chen Mon Oct 28 08:30 PDT 2024] "
             "Patricia, thank you for being transparent. That on-call list exhaustion failure "
             "will likely defeat the exemption claim for those shifts. We need to document "
             "exactly which nurses were called and which were not, for every violation shift.",
             "Understood. The AFL-23-27 three-prong exemption requires exhausting ALL on-call "
             "nurses. Partial contact (stopping after 2 calls) fails Prong 3. I will flag "
             "the specific shifts where on-call list was not fully exhausted in the analysis."),
        ])

    # S3 Union Email — 违规时间线争论（引用旧版 on-call 名单作为红鲱鱼）
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2024-10-30T10:00:00",
        [
            ("[Email union-kevin-torres → hr-bradley Mon Oct 30 10:00 PDT 2024] "
             "Tom, Our records confirm SVMC has been in violation since October 2023. "
             "We are attaching the archived on-call list from October 2023 "
             "(SVMC_on_call_list_v2023-10_ARCHIVED.csv). Even with that roster, the float pool "
             "was inadequate. Three nurses on that list are no longer available. "
             "We dispute that violations only began in October 2024.",
             "The union references the archived v2023-10 on-call list as evidence. However, "
             "per our workspace files, that list is explicitly marked OBSOLETE (archived 2024-09-01). "
             "The current authoritative on-call list is SVMC_on_call_list_current.csv. "
             "Using the obsolete roster for current compliance analysis would be an error."),
            ("[Email hr-bradley → union-kevin-torres Tue Oct 31 09:00 PDT 2024] "
             "Kevin, the 2023-10 on-call list you attached is an archived historical document, "
             "clearly marked OBSOLETE. Current compliance must be assessed using the current "
             "roster. Three nurses on that list (Amanda Price, Carol Adams, Pete Murray) "
             "have departed for various reasons. Their absence affects historical analysis "
             "only, not the current corrective action plan.",
             "Confirmed hospital HR position: v2023-10 archive is not operative for current "
             "compliance analysis. Current roster (SVMC_on_call_list_current.csv) controls. "
             "This distinction is important — SB 596 defines on-call list as only formally "
             "scheduled on-call or float pool nurses."),
        ])

    # S4 Feishu 合规应急群 — 合规顾问讨论（含 $10,000 失真诱饵和流感豁免错误）
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2024-10-29T14:00:00",
        [
            ("[Feishu 合规应急 Chen Li Tue Oct 29 14:00 CST 2024] "
             "大家注意：我们讨论罚款金额的时候，我们的 BOT 摘要显示首次违规是 $10,000。"
             "我认为这个数字不对，需要验证。",
             "请注意：BOT 自动摘要中的 $10,000 数字有误。根据 H&SC § 1280.3 和 AFL-23-27，"
             "首次违规正确罚款为 $15,000（一万五千美元）。$10,000 是错误数字，不得用于计算。"),
            ("[Feishu 合规应急 Dr. Aisha Rahman Tue Oct 29 14:15 CST 2024] "
             "我核实了。AFL-23-27 原文明确写明：首次违规 $15,000，不是 $10,000。"
             "BOT 摘要的错误已经被确认。此外，季节性流感高峰不自动构成豁免理由。"
             "AFL-23-27 明确说明了这一点。",
             "已记录两个关键确认：(1) 首次违规 = $15,000，非 $10,000；"
             "(2) 季节性流感高峰不自动构成'不可预见且不可控'情形，不适用 Prong 1 豁免。"),
        ])

    # S5 CDPH 官方往来
    append_history(
        SESS / f"{s_cdph}.jsonl", s_cdph, CWD, "2024-10-25T15:00:00",
        [
            ("[CDPH Official Letter from Inspector Linda Wu Fri Oct 25 15:00 PDT 2024] "
             "Per attached Statement of Deficiencies: SVMC has 30 days to submit a Corrective "
             "Action Plan. All violations are FIRST violations under H&SC § 1280.3 "
             "(no prior violations on record within the 3-year lookback period). "
             "Administrative penalty assessments will follow upon CAP review.",
             "CDPH official position confirmed: all violations are first-violation tier "
             "($15,000 each under H&SC § 1280.3). No prior violations within 3-year window. "
             "30-day CAP deadline: November 22, 2024. I will track this deadline."),
            ("[CDPH Official Email from Inspector Linda Wu Mon Oct 28 09:00 PDT 2024] "
             "Supplemental note: Please ensure your CAP addresses the on-call list exhaustion "
             "failure documented in Finding 2. Your corrective on-call protocol must comply "
             "with SB 596's revised definition of 'on-call list' (effective January 1, 2026). "
             "Early compliance is strongly recommended.",
             "Acknowledged. CAP must include: (1) updated on-call list per SB 596 definition "
             "(formally scheduled on-call + float pool only); (2) documentation showing full "
             "on-call list exhaustion protocol. I will incorporate these requirements."),
        ])

    return {
        "main": main_id,
        "history": [
            (s_slack, "slack"),
            (s_email, "email"),
            (s_feishu, "feishu"),
            (s_cdph, "im"),
        ],
    }


# --------------------------------------------------------------------------- #
# 6. Updates（U1 + U2 含 supersede）
# --------------------------------------------------------------------------- #
def gen_updates(sess_ids: dict) -> dict:
    """生成两次 update 及其文件。"""
    # ---- UPDATE 1: CDPH 补充检查通知 + Telemetry 违规数据 ----
    u1_ws = UPD / "upd1_workspace"
    u1_sess_dir = UPD / "upd1_sessions"

    # Telemetry 补充违规数据（12 班次，跨越 2026-01-01 生效日）
    # 前 5 班次：2025-12-28 - 2026-01-01（旧规则适用，pre-SB596）
    # 后 7 班次：2026-01-02 - 2026-01-08（SB596 日罚款生效，post-SB596）
    tel_violations = []
    # Pre-SB596（2025-12-28 到 2025-12-31，共 5 班次：night shifts）
    pre_sb596_dates = [
        "2025-12-28", "2025-12-29", "2025-12-30", "2025-12-31",
    ]
    # 加上一班 2026-01-01 零点跨越（仍算 pre）
    for i, d in enumerate(pre_sb596_dates):
        tel_violations.append({
            "shift_id": f"SH-TEL-U1-{i+1:03d}",
            "date": d,
            "shift": "Night (19:00-07:00)",
            "unit": "Telemetry",
            "nurses_on_duty_count": 2,
            "patient_count": 9,
            "ratio_actual": 4.50,
            "legal_max": 4,
            "is_violation": True,
            "sb596_daily": False,
            "notes": "Pre-SB596: night shift, 2 nurses, 9 patients → 1:4.5 (violation)"
        })
    # Post-SB596（2026-01-02 到 2026-01-08，共 7 班次）
    post_sb596_dates = [
        "2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05",
        "2026-01-06", "2026-01-07", "2026-01-08",
    ]
    for i, d in enumerate(post_sb596_dates):
        tel_violations.append({
            "shift_id": f"SH-TEL-U1-{i+5:03d}",
            "date": d,
            "shift": "Night (19:00-07:00)",
            "unit": "Telemetry",
            "nurses_on_duty_count": 2,
            "patient_count": 9,
            "ratio_actual": 4.50,
            "legal_max": 4,
            "is_violation": True,
            "sb596_daily": True,
            "notes": "Post-SB596 (eff. 2026-01-01): each day = separate violation"
        })

    buf = io.StringIO()
    w_csv = csv.DictWriter(buf, fieldnames=list(tel_violations[0].keys()))
    w_csv.writeheader()
    w_csv.writerows(tel_violations)
    w(u1_ws / "SVMC_telemetry_violations_dec2025_jan2026.csv", buf.getvalue())

    # CDPH 补充检查通知（大型文档，撑起 >30k token 体量）
    cdph_supplement_text = _gen_cdph_supplement_letter(tel_violations)
    w(u1_ws / "cdph_supplemental_inspection_jan2026.txt", cdph_supplement_text)

    # Update 1 session: 追加 CDPH 来函到 cdph session
    s_cdph = sess_ids["history"][3][0]
    sb_u1 = SessionBuilder(s_cdph, CWD, "2026-01-10T09:00:00", is_main=False)
    sb_u1.add_user(
        "[CDPH Official Letter from Inspector Linda Wu Fri Jan 10 2026 09:00 PST] "
        "SUPPLEMENTAL INSPECTION NOTICE — SVMC Ref# 050123-SVMC-SUP-01. "
        "A supplemental inspection conducted December 27, 2025 – January 9, 2026 identified "
        "additional Telemetry unit violations. See attached: "
        "cdph_supplemental_inspection_jan2026.txt and SVMC_telemetry_violations_dec2025_jan2026.csv. "
        "Total new violations: 12 Telemetry night shifts (4 pre-2026-01-01, 7 post-2026-01-01 "
        "under SB 596 daily-violation rule, plus 1 spanning the boundary). "
        "Post-2026-01-01 violations are each counted as separate violations per SB 596. "
        "Your penalty assessment must be updated to reflect these additional findings."
    )
    sb_u1.add_assistant(
        "CDPH Supplemental inspection notice received and documented. Key changes to track:\n"
        "1. 12 additional Telemetry violations (4 pre-SB596 + 7 post-SB596 daily violations + "
        "1 boundary date counted as pre-SB596 = 5 pre + 7 post total).\n"
        "2. Post-2026-01-01 Telemetry violations: each calendar day = separate violation under SB 596.\n"
        "3. Penalty assessment must be updated (Q9 will recalculate total with Telemetry added).\n"
        "I will update the violation ledger and penalty totals to reflect this supplemental finding."
    )
    sb_u1.write(u1_sess_dir / f"{s_cdph}.jsonl")

    # ---- UPDATE 2: 工会和解协议（supersede U1 中 4 个 Telemetry 违规 + 新增 2 ICU 深夜违规）----
    u2_ws = UPD / "upd2_workspace"
    u2_sess_dir = UPD / "upd2_sessions"

    # 工会和解备忘录 + 修订排班
    settlement_text = _gen_union_settlement_memo()
    w(u2_ws / "union_settlement_memorandum.txt", settlement_text)

    # 新增 2 个 ICU 深夜违规（此前未发现）
    icu_night_violations = [
        {"shift_id": "SH-ICU-LATE-001", "date": "2025-11-15", "shift": "Night (23:00-07:00)",
         "unit": "ICU", "nurses_on_duty_count": 2, "patient_count": 5,
         "ratio_actual": 2.50, "legal_max": 2, "is_violation": True,
         "discovery_date": "2026-01-20", "notes": "Deep night shift; discovered via audit of EHR records"},
        {"shift_id": "SH-ICU-LATE-002", "date": "2025-11-22", "shift": "Night (23:00-07:00)",
         "unit": "ICU", "nurses_on_duty_count": 2, "patient_count": 5,
         "ratio_actual": 2.50, "legal_max": 2, "is_violation": True,
         "discovery_date": "2026-01-20", "notes": "Deep night shift; discovered via audit of EHR records"},
    ]

    buf2 = io.StringIO()
    w_csv2 = csv.DictWriter(buf2, fieldnames=list(icu_night_violations[0].keys()))
    w_csv2.writeheader()
    w_csv2.writerows(icu_night_violations)
    w(u2_ws / "SVMC_icu_newly_discovered_violations.csv", buf2.getvalue())

    # 修订 float pool 要求文件
    w(u2_ws / "float_pool_requirement_updated.txt", """
SVMC FLOAT POOL REVISED REQUIREMENT
Effective: Per Union Settlement Agreement (January 2026)
Authority: Union Settlement Memorandum + CDPH AFL-23-27 Corrective Action

REVISED REQUIREMENT:
The float pool must include a minimum of THREE (3) ICU-certified registered nurses
at all times. This supersedes the prior informal requirement of two (2) ICU float pool nurses.

RATIONALE:
- ICU staffing gap of 3 FTE requires backup capacity to maintain 1:2 ratio
- Travel nurse contracts are temporary; permanent float pool coverage is required
- Union settlement requires this as a condition of the corrective action plan

IMPLEMENTATION TIMELINE:
- Immediate: Confirm current 2 travel nurses (RN-ICU-T01, RN-ICU-T02) are ICU-certified
  and counted toward float pool (confirmed: both ICU-certified per TN-2024-001 and TN-2024-002)
- Within 30 days: Recruit 1 additional ICU-certified float pool RN
- Within 60 days: Establish minimum 3 ICU-certified float pool nurses permanently

This requirement applies starting with the second remediation week (Q15 staffing log).
""")

    # 附加历史邮件线程（撑体量）
    historical_email = _gen_historical_email_thread()
    w(u2_ws / "union_historical_email_thread_extended.txt", historical_email)

    # Update 2 session: 新的工会和解 session
    s_union_settle = gen_session_id("union_settlement_feishu", TID)
    sb_u2 = SessionBuilder(s_union_settle, CWD, "2026-01-22T10:00:00", is_main=False)
    sb_u2.add_user(
        "[Feishu 合规应急 Union Settlement Notice Thu Jan 22 2026 10:00 CST] "
        "NOTICE: The Union-Hospital Settlement Agreement has been finalized. "
        "Key terms affecting the violation ledger:\n"
        "1. SUPERSEDE (partial): Four (4) Telemetry violation shifts from U1 "
        "(SH-TEL-U1-002, SH-TEL-U1-003, SH-TEL-U1-004, SH-TEL-U1-005) are WITHDRAWN. "
        "The union's time-stamp audit confirmed these 4 shifts had documented nurse coverage "
        "that was not captured in the original CDPH records (clerical timestamping error). "
        "These 4 violations are REMOVED from the ledger.\n"
        "2. NEW VIOLATIONS: 2 previously undiscovered ICU deep-night violations added: "
        "SH-ICU-LATE-001 (2025-11-15) and SH-ICU-LATE-002 (2025-11-22).\n"
        "3. FLOAT POOL: Minimum 3 ICU-certified float pool RNs required going forward.\n"
        "See union_settlement_memorandum.txt and SVMC_icu_newly_discovered_violations.csv."
    )
    sb_u2.add_assistant(
        "Union Settlement Agreement acknowledged. Updating violation ledger per settlement terms:\n"
        "SUPERSEDE (partial): Removing 4 Telemetry violations from U1 "
        "(SH-TEL-U1-002, SH-TEL-U1-003, SH-TEL-U1-004, SH-TEL-U1-005). "
        "This is NOT additive — these 4 violations are WITHDRAWN from the total count.\n"
        "NEW: Adding 2 ICU deep-night violations (SH-ICU-LATE-001, SH-ICU-LATE-002).\n"
        "NET CHANGE: -4 Telemetry + 2 ICU = net -2 violations from the U1 total.\n"
        "FLOAT POOL: Minimum 3 ICU-certified nurses required — to be reflected in Week 2 log.\n"
        "I will revise the final violation ledger (Q11) accordingly."
    )
    sb_u2.write(u2_sess_dir / f"{s_union_settle}.jsonl")

    updates_decl = {
        "upd1_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd1_sessions",
            "files": [{"name": f"{s_cdph}.jsonl", "action": "append",
                       "target": f"{s_cdph}.jsonl"}],
        },
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {"name": "SVMC_telemetry_violations_dec2025_jan2026.csv", "action": "new",
                 "target": "hospital_data/SVMC_telemetry_violations_dec2025_jan2026.csv"},
                {"name": "cdph_supplemental_inspection_jan2026.txt", "action": "new",
                 "target": "communications/cdph_supplemental_inspection_jan2026.txt"},
            ],
        },
        "upd2_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd2_sessions",
            "files": [{"name": f"{s_union_settle}.jsonl", "action": "new",
                       "target": f"{s_union_settle}.jsonl", "channel": "feishu"}],
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "union_settlement_memorandum.txt", "action": "new",
                 "target": "communications/union_settlement_memorandum.txt"},
                {"name": "SVMC_icu_newly_discovered_violations.csv", "action": "new",
                 "target": "hospital_data/SVMC_icu_newly_discovered_violations.csv"},
                {"name": "float_pool_requirement_updated.txt", "action": "new",
                 "target": "reports/float_pool_requirement_updated.txt"},
                {"name": "union_historical_email_thread_extended.txt", "action": "new",
                 "target": "communications/union_historical_email_thread_extended.txt"},
            ],
        },
    }
    return updates_decl


def _gen_cdph_supplement_letter(tel_violations: list[dict]) -> str:
    """生成 CDPH 补充检查来函（大体量，~35k tokens 目标）。"""
    intro = """
CALIFORNIA DEPARTMENT OF PUBLIC HEALTH
Health Facility Evaluation Branch

SUPPLEMENTAL INSPECTION NOTICE
DATE: January 10, 2026
TO: Sutter Valley Medical Center (SVMC)
    350 Valley Medical Drive, Sacramento, CA 95814
FROM: Inspector Linda Wu, CDPH Health Facilities Evaluation Branch
RE: Supplemental Statement of Deficiencies — Telemetry Unit Violations
    Inspection Period: December 27, 2025 – January 9, 2026
FACILITY LICENSE NO.: 050123-SVMC-SUP-01
REFERENCE: October 2024 SOD (050123-SVMC-OCT24)

═══════════════════════════════════════════════════════════════════════
SECTION 1: SUPPLEMENTAL FINDINGS
═══════════════════════════════════════════════════════════════════════

Following a supplemental inspection of SVMC's Telemetry Unit during the period
December 27, 2025 through January 9, 2026, the following additional deficiencies
have been identified under Title 22 § 70217(a)(10):

TELEMETRY UNIT — LEGAL MAXIMUM RATIO: 1:4 (maximum 4 patients per nurse)
Reference: Cal. Code Regs. Title 22 § 70217(a)(10), effective January 1, 2008

DETAILED VIOLATION LOG:
"""
    rows_text = ""
    for v in tel_violations:
        sb_note = " [SB 596 DAILY VIOLATION — separate count]" if v["sb596_daily"] else " [Pre-SB596: same-inspection rule]"
        rows_text += f"""
  Shift ID: {v['shift_id']}
  Date: {v['date']}
  Shift: {v['shift']}
  Unit: Telemetry
  Nurses on Duty: {v['nurses_on_duty_count']}
  Patient Count: {v['patient_count']}
  Actual Ratio: 1:{v['ratio_actual']}
  Legal Maximum: 1:{v['legal_max']}
  Status: VIOLATION{sb_note}
  Notes: {v['notes']}
"""

    sb596_section = """
═══════════════════════════════════════════════════════════════════════
SECTION 2: SB 596 APPLICABILITY ANALYSIS
═══════════════════════════════════════════════════════════════════════

IMPORTANT: California SB 596 (signed October 13, 2025) took effect January 1, 2026.
Under SB 596, each calendar day of non-compliance constitutes a separate and distinct
violation. This changes the penalty calculation methodology for violations on or after
January 1, 2026.

CLASSIFICATION OF TELEMETRY VIOLATIONS:

PRE-SB596 VIOLATIONS (December 28-31, 2025 = 4 violations):
These violations occurred BEFORE January 1, 2026. Under H&SC § 1280.3 legacy rules
(as established by SB 227/2019), violations from a single inspection inspection are
counted as ONE (1) violation. However, since these are part of a SUPPLEMENTAL inspection
distinct from the October 2024 inspection, they are counted as separate instances.
Penalty tier: SUBSEQUENT (within 3-year window from Oct 2024 finding) = $30,000 each.

NOTE: The 4 pre-SB596 Telemetry violations are grouped under the same supplemental
inspection (Dec 27 – Jan 9, 2026). Under legacy § 1280.3, all violations found in
ONE inspection count as ONE violation. However, the supplemental inspection spans
two calendar years — CDPH will treat the pre-SB596 group (Dec 27-31) as one sub-count
and the post-SB596 group (Jan 1-9) under SB 596 rules separately.

For simplicity in penalty assessment, treat:
- 4 pre-SB596 violations (Dec 28-31) as: 4 separate shifts but 1 "inspection finding"
  under legacy rule = still 1 subsequent violation = $30,000
- 7 post-SB596 violations (Jan 2-8) as: 7 separate daily violations = $30,000 each
  (all subsequent, within 3-year window from October 2024 violations)

TOTAL TELEMETRY SUPPLEMENTAL PENALTY CALCULATION (for reference):
  Pre-SB596 group: 1 subsequent violation × $30,000 = $30,000
  Post-SB596 daily violations: 7 violations × $30,000 = $210,000
  Telemetry subtotal: $240,000

═══════════════════════════════════════════════════════════════════════
SECTION 3: CUMULATIVE PENALTY UPDATE
═══════════════════════════════════════════════════════════════════════

October 2024 Initial Violations (as previously calculated):
  [Pending agent calculation from Q3/Q4]

Supplemental Telemetry Violations (this notice):
  [See Section 2 above]

CDPH will issue final penalty assessment after receipt and review of CAP.

═══════════════════════════════════════════════════════════════════════
SECTION 4: REGULATORY FRAMEWORK REFERENCE
═══════════════════════════════════════════════════════════════════════

RELEVANT REGULATIONS:
1. Cal. Code Regs. Title 22 § 70217(a)(10) — Telemetry maximum ratio 1:4
   Effective: January 1, 2008
   Source: https://www.law.cornell.edu/regulations/california/Cal-Code-Regs-Tit-22-SS-70217

2. California H&SC § 1280.3 — Administrative penalties
   First violation: $15,000
   Subsequent (within 3 years): $30,000
   Source: https://law.justia.com/codes/california/code-hsc/division-2/chapter-2/article-3/section-1280-3/

3. CDPH AFL-23-27 — Enforcement guidance (September 2023)
   Source: https://www.cdph.ca.gov/Programs/CHCQ/LCP/Pages/AFL-23-27.aspx

4. California SB 596 (effective January 1, 2026)
   Daily violation rule for post-2026-01-01 non-compliance
   Source: https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260SB596

═══════════════════════════════════════════════════════════════════════
SECTION 5: CDPH INSPECTION METHODOLOGY NOTES
═══════════════════════════════════════════════════════════════════════

"""
    # 添加大量内容以达到体量目标
    methodology = ""
    for unit in UNITS:
        methodology += f"""
UNIT: {unit}
Inspection period: December 27, 2025 – January 9, 2026
Legal maximum ratio: 1:{LEGAL_RATIOS[unit]}
Reference: Cal. Code Regs. Title 22 § 70217

Staffing records reviewed: 28 shifts (14 days × 2 shifts per day)
Methodology: CDPH inspectors reviewed electronic staffing assignments, compared
against patient census records, cross-referenced on-call activation logs.

For each shift, inspectors verified:
(a) Number of licensed nurses assigned to the unit at shift start
(b) Patient census at shift start and peak during shift
(c) Charge nurse status during shift (direct care vs. administrative duties)
(d) Any on-call activations during the shift period
(e) Float pool utilization records

Findings for {unit}: {'Violations found (see Telemetry section above)' if unit == 'Telemetry' else 'No violations found during supplemental inspection period'}

"""

    footer = """
═══════════════════════════════════════════════════════════════════════
RESPONSE REQUIRED
═══════════════════════════════════════════════════════════════════════

SVMC must submit an updated Corrective Action Plan (CAP) addressing the supplemental
Telemetry violations within FIFTEEN (15) days of receipt of this notice.

The updated CAP must include:
1. Explanation of root cause for Telemetry under-staffing during December 27 – January 9
2. Updated on-call list demonstrating SB 596 compliance
3. Prospective 2-week staffing schedule for Telemetry unit showing 1:4 compliance
4. Updated penalty assessment reflecting all violations (initial + supplemental)

Inspector: Linda Wu
CDPH Health Facilities Evaluation Branch
Signed: January 10, 2026

END OF SUPPLEMENTAL INSPECTION NOTICE
Ref: 050123-SVMC-SUP-01
"""

    # 添加更多内容以撑起 >30k token 体量
    appendix = _gen_regulatory_appendix()

    return intro + rows_text + sb596_section + methodology + footer + appendix


def _gen_regulatory_appendix() -> str:
    """生成法规附录（撑体量）。"""
    text = """
═══════════════════════════════════════════════════════════════════════
APPENDIX A: FULL TITLE 22 § 70217 RATIO TABLE (CDPH REFERENCE)
═══════════════════════════════════════════════════════════════════════

The following table summarizes all nurse-to-patient ratios under California Title 22,
Division 5, Chapter 1, § 70217, as applicable to SVMC and all general acute care
hospitals in California.

UNIT TYPE                          | MAX PATIENTS/NURSE | EFFECTIVE DATE
------------------------------------|---------------------|----------------
Critical Care/ICU (§70217(a)(1))   | 2                  | January 1, 2004
Coronary Care Unit (§70217(a)(2))  | 2                  | January 1, 2004
Post-Anesthesia Care (§70217(a)(3))| 2                  | January 1, 2004
Pediatric ICU (§70217(a)(4))       | 2                  | January 1, 2004
Neonatal ICU (§70217(a)(5))        | 1-2 (acuity)       | January 1, 2004
Labor & Delivery (§70217(a)(6))    | 2 (active) 1(del)  | January 1, 2004
Antepartum (§70217(a)(7))          | 4                  | January 1, 2004
Emergency Department (§70217(a)(8))| 4 (general)        | January 1, 2004
  - Critical Trauma (RN only)      | 1                  | January 1, 2004
Step-Down/Intermediate (§70217(a)(9))| 3               | January 1, 2008
Telemetry (§70217(a)(10))          | 4                  | January 1, 2008
Medical/Surgical (§70217(a)(11))   | 5                  | January 1, 2005
  (Initial phase: 6)               |                    | January 1, 2004
Psychiatric (§70217(a)(13))        | 6                  | January 1, 2004

KEY NOTES ON APPLICABILITY:
1. These ratios apply AT ALL TIMES — not just at shift start or during planned census.
2. NO AVERAGING: The ratio must be maintained for each individual nurse at all times.
   A nurse covering breaks for another nurse while simultaneously caring for their own
   patients is in violation during the break coverage period.
3. CHARGE NURSE (§70217(c)): Counted only when actively providing direct patient care.
4. LICENSED VOCATIONAL NURSES (LVNs): Count toward ratios in most units. However,
   in psychiatric units, Psychiatric Technicians (PTs) may substitute for LVNs.
5. UNLICENSED PERSONNEL: Cannot be counted toward licensed nurse ratios regardless of
   their training or assigned duties.

═══════════════════════════════════════════════════════════════════════
APPENDIX B: AFL-23-27 THREE-PRONG EXEMPTION DETAIL
═══════════════════════════════════════════════════════════════════════

The following is an expanded discussion of the three-prong exemption defense under
CDPH AFL-23-27 (September 2023). This appendix is provided for SVMC's reference
in preparing exemption claims for any qualifying shifts.

PRONG 1 — UNPREDICTABILITY AND UNCONTROLLABILITY

The facility must demonstrate that the circumstances causing the staffing shortage
could not have been anticipated through the exercise of reasonable diligence in
planning and operations.

QUALIFYING SCENARIOS (examples):
- Sudden illness or injury of a scheduled nurse immediately before shift start
  (same-day call-out, not foreseeable at time of scheduling)
- Mass casualty event causing sudden patient surge beyond typical census
- Natural disaster preventing staff from reporting to work
- Previously unknown illness outbreak in the community causing unusual census spike

NON-QUALIFYING SCENARIOS (per AFL-23-27):
- SEASONAL INFLUENZA PEAKS: Influenza season is a known, recurring, predictable event.
  Hospitals are expected to prepare in advance. Filing an exemption based solely on
  seasonal flu surge will be denied under Prong 1.
- SCHEDULED FMLA LEAVE: While FMLA leave is unavoidable for the individual employee,
  the leave schedule is KNOWN in advance. Hospitals must plan for coverage.
  Note: A combination of known FMLA leave PLUS an unexpected additional absence
  MAY qualify if the combination was not foreseeable at the time of scheduling.
- SCHEDULED VACATIONS: Not unpredictable. Must be covered in advance scheduling.
- CHRONIC UNDERSTAFFING: An ongoing vacancy that has persisted for multiple months
  is not "unpredictable" — it is a management failure to recruit.

PRONG 2 — PROMPT EFFORTS

The facility must show it "made prompt efforts to maintain or restore compliant staffing."
Documentation must include:
- Precise timestamps showing when the shortage was identified
- Timestamped records of every action taken to secure replacement staff
- Evidence that management was notified within a reasonable time

Acceptable prompt efforts include:
- Activating the on-call system within minutes of identifying the shortage
- Contacting float pool supervisors for emergency deployment
- Reaching out to agency staffing services with a time-sensitive request

Unacceptable "prompt efforts":
- Waiting hours before notifying management or activating on-call
- Only contacting a subset of available options
- Relying on informal word-of-mouth rather than the formal on-call system

PRONG 3 — ON-CALL LIST EXHAUSTION

This prong requires that the facility "immediately used and subsequently exhausted
the hospital's on-call list" before the shift remained understaffed.

"EXHAUSTED" means: every nurse on the formal on-call list for that unit and shift
was contacted. PARTIAL exhaustion (stopping after 2-3 calls when 8 names are on the list)
does NOT satisfy Prong 3 under AFL-23-27.

SB 596 UPDATE TO ON-CALL LIST DEFINITION:
Effective January 1, 2026, SB 596 limits the on-call list to:
(a) Nurses formally SCHEDULED to be on-call for that specific shift and unit, or
(b) Nurses in a REGULARLY SCHEDULED float pool for that unit.

CONSEQUENCE: A hospital cannot satisfy Prong 3 under SB 596 by informally calling
nurses who are not on the formal on-call roster, even if those nurses agree to come in.
The on-call system must be the formal, documented, pre-scheduled mechanism.

═══════════════════════════════════════════════════════════════════════
APPENDIX C: SB 596 IMPLEMENTATION GUIDANCE
═══════════════════════════════════════════════════════════════════════

California SB 596 (effective January 1, 2026) introduces the following changes:

1. DAILY VIOLATION RULE
   Pre-SB596: Multiple violations in one inspection = 1 violation count.
   Post-SB596: Each calendar day of non-compliance = 1 separate violation.

   Example: A Telemetry unit with ratio violations on January 2, 3, 4, 5, 6, 7, and 8
   (7 separate days) = 7 separate violations, each assessed independently.
   If all are subsequent violations: 7 × $30,000 = $210,000.

   Previously (pre-SB596): Those same 7 days found in one inspection = 1 violation = $30,000.

2. REVISED ON-CALL LIST DEFINITION
   Under SB 596, "on-call list" means ONLY:
   (a) Nurses scheduled on the formal on-call system for that specific shift/unit, or
   (b) Nurses in a regularly scheduled float pool.

   NOT included: Casual calls to off-duty nurses who are not on the formal roster.

3. RETROACTIVITY: SB 596 does NOT apply retroactively to violations before 2026-01-01.

4. SCOPE: General acute care hospitals, acute psychiatric hospitals, special hospitals.

═══════════════════════════════════════════════════════════════════════
APPENDIX D: JOINT COMMISSION NPG 12 OVERVIEW
═══════════════════════════════════════════════════════════════════════

Joint Commission National Performance Goal 12 — Health Professional Resource Management
Effective: January 1, 2026

NPG.12.01.01: Leadership ensures adequate number and mix of qualified staff based on
patient needs and organizational goals.

NPG.12.02.01 EP1: Nurse executive (CNO) establishes and maintains a staffing plan.
NPG.12.02.01 EP2: Nurse executive participates in hospital governance related to staffing.
NPG.12.02.01 EP4: 24/7 registered nursing oversight is in place.
NPG.12.02.01 EP5: Staffing decisions are documented and traceable to patient acuity.

NPG.12.06.01 EP1: Staffing adequacy is evaluated as part of QAPI (Quality Assurance and
Performance Improvement) program.
NPG.12.06.01 EP2: Results of staffing evaluation are reported to hospital leadership.
NPG.12.06.01 EP3: Results of staffing evaluation are reported to governing body.
NPG.12.06.01 EP4: Data linking staffing to quality/safety indicators is maintained.

Documentation Required:
- Acuity-based staffing analysis
- Variance reports when staffing deviates from plan
- Correlation data linking staffing levels to quality indicators (e.g., pressure ulcers,
  falls, medication errors, patient satisfaction)

Implication for SVMC:
SVMC must align its corrective action plan with NPG 12 requirements effective 2026-01-01.
The nurse executive (Miranda Chen, CNO) must directly participate in governance regarding
the staffing compliance crisis and document corrective actions per NPG.12.02.01.

═══════════════════════════════════════════════════════════════════════
APPENDIX E: CDPH ENFORCEMENT ACTIONS DATASET REFERENCE
═══════════════════════════════════════════════════════════════════════

For context, CDPH maintains an enforcement actions dataset at:
https://data.chhs.ca.gov/dataset/healthcare-facility-state-enforcement-actions

This dataset covers enforcement actions from July 1, 1997 through June 30, 2024.
Fields include: enforcement action type, violation category, penalty amount,
violation date, appeal status, facility name.

SVMC Penalty History (per CDPH records):
- No prior staffing ratio violations on record within the past 3 years
- This is SVMC's first formal staffing ratio enforcement action under § 1280.3
- All violations identified in the October 2024 inspection are FIRST violations

NOTE: The supplemental January 2026 violations (this notice) occur WITHIN 3 years
of the October 2024 first violations. Therefore, all supplemental Telemetry violations
are SUBSEQUENT violations ($30,000 each).

═══════════════════════════════════════════════════════════════════════
END OF APPENDICES
═══════════════════════════════════════════════════════════════════════
"""
    # 追加更多补充内容以确保体量
    extra = "\n".join([
        f"SUPPLEMENTAL DATA ROW {i:04d}: Telemetry staffing data point {i} — "
        f"date 2025-12-{(i % 30) + 1:02d}, shift {'Day' if i % 2 == 0 else 'Night'}, "
        f"nurses {(i % 3) + 2}, patients {(i % 5) + 6}, "
        f"ratio {round(((i % 5) + 6) / ((i % 3) + 2), 2)}, "
        f"compliant {((i % 5) + 6) / ((i % 3) + 2) <= 4.0}"
        for i in range(1, 600)
    ])
    return text + extra


def _gen_union_settlement_memo() -> str:
    """生成工会和解备忘录（撑体量，~40k tokens 目标）。"""
    memo = """
MEMORANDUM OF UNDERSTANDING
UNION-HOSPITAL SETTLEMENT AGREEMENT

PARTIES:
Service Employees International Union (SEIU) Healthcare Workers West
Sutter Valley Medical Center (SVMC)

DATE: January 20, 2026
EFFECTIVE: January 22, 2026

BACKGROUND:
Following the CDPH Statement of Deficiencies (October 2024) and Supplemental Inspection
Notice (January 2026), SEIU and SVMC have reached the following settlement agreement
regarding the nurse staffing ratio violations.

═══════════════════════════════════════════════════════════════════════
ARTICLE 1: TELEMETRY VIOLATION WITHDRAWAL (SUPERSEDE)
═══════════════════════════════════════════════════════════════════════

1.1 SCOPE OF WITHDRAWAL
The union's independent audit of SVMC electronic health records (EHR) and staffing
management system logs has identified a clerical timestamping error in the Telemetry
unit records for the period December 29-31, 2025 and January 1, 2026.

Specifically, four (4) Telemetry violation shifts identified in the CDPH Supplemental
Inspection Notice are being WITHDRAWN from the violation ledger:

SHIFT SH-TEL-U1-002 (Date: 2025-12-29, Night):
  Finding: EHR records confirm that Nurse Don Gibson (RN-TEL-010) was documented as
  present for the full shift starting 18:45 PM, not 19:30 PM as originally recorded.
  With 3 nurses on duty, the 9-patient count results in ratio 1:3.0 — COMPLIANT.
  WITHDRAWAL: This shift is NO LONGER a violation.

SHIFT SH-TEL-U1-003 (Date: 2025-12-30, Night):
  Finding: Float pool nurse Beth Flores (RN-TEL-009) was deployed to Telemetry at
  19:15 PM but the on-call activation was not recorded until 20:00 PM.
  With 3 nurses on duty, ratio 1:3.0 — COMPLIANT.
  WITHDRAWAL: This shift is NO LONGER a violation.

SHIFT SH-TEL-U1-004 (Date: 2025-12-31, Night):
  Finding: Charge nurse Vera Torres (RN-TEL-001) was performing direct patient care
  (not administrative duties) on this shift per nursing notes review.
  With 3 nurses on duty (including charge), ratio 1:3.0 — COMPLIANT.
  WITHDRAWAL: This shift is NO LONGER a violation.

SHIFT SH-TEL-U1-005 (Date: 2026-01-01, Night):
  Finding: Three nurses on duty per corrected EHR records (timestamping error in
  original CDPH records). Ratio 1:3.0 — COMPLIANT.
  WITHDRAWAL: This shift is NO LONGER a violation.

1.2 NET EFFECT OF WITHDRAWALS
Four (4) Telemetry violations from the CDPH Supplemental Inspection are removed.
These are NOT to be added to any new violation count — they are DELETED.
This represents a SUPERSEDE of the prior CDPH count, not an additive adjustment.

═══════════════════════════════════════════════════════════════════════
ARTICLE 2: NEWLY DISCOVERED ICU VIOLATIONS
═══════════════════════════════════════════════════════════════════════

2.1 IDENTIFICATION OF NEW VIOLATIONS
The union's audit of EHR records also discovered two (2) previously unreported ICU
deep-night violations (between 23:00 and 07:00 hours):

SHIFT SH-ICU-LATE-001 (Date: 2025-11-15, Night 23:00-07:00):
  Unit: ICU
  Nurses on duty: 2
  Patient count: 5
  Actual ratio: 1:2.5
  Legal maximum: 1:2 (§ 70217(a)(1))
  STATUS: VIOLATION — confirmed by EHR audit
  Discovery date: 2026-01-20 (newly discovered)

SHIFT SH-ICU-LATE-002 (Date: 2025-11-22, Night 23:00-07:00):
  Unit: ICU
  Nurses on duty: 2
  Patient count: 5
  Actual ratio: 1:2.5
  Legal maximum: 1:2 (§ 70217(a)(1))
  STATUS: VIOLATION — confirmed by EHR audit
  Discovery date: 2026-01-20 (newly discovered)

2.2 PENALTY CLASSIFICATION
These violations occurred on November 15 and 22, 2025 — BEFORE SB 596 effective date
(January 1, 2026). Therefore, legacy penalty rules apply.

Both violations are within the 3-year window from October 2024 violations.
Classification: SUBSEQUENT violations — $30,000 each.

═══════════════════════════════════════════════════════════════════════
ARTICLE 3: FLOAT POOL REQUIREMENT
═══════════════════════════════════════════════════════════════════════

3.1 MINIMUM ICU FLOAT POOL REQUIREMENT
As part of this settlement and consistent with SVMC's Corrective Action Plan,
SVMC agrees to maintain a minimum of THREE (3) ICU-certified registered nurses
in the float pool at all times.

This SUPERSEDES any prior informal arrangement providing for two (2) ICU float pool nurses.

Current status:
- RN-ICU-T01 (Jessica Brooks): ICU-certified, float pool eligible per contract TN-2024-001
- RN-ICU-T02 (Ryan Martinez): ICU-certified, float pool eligible per contract TN-2024-002
- VACANCY: One additional ICU-certified float pool RN must be recruited within 30 days

SVMC shall report compliance with this requirement in its weekly staffing logs
beginning with the Week 2 log (Q15 in the compliance reporting schedule).

3.2 REPORTING REQUIREMENT
SVMC shall document the names and certifications of all three ICU float pool nurses
in each CDPH staffing log beginning with the remediation Period Week 2.

═══════════════════════════════════════════════════════════════════════
ARTICLE 4: HISTORICAL EMAIL RECORD
═══════════════════════════════════════════════════════════════════════

The following is a record of union-management communications spanning October 2023
through January 2026, provided as context for this settlement:

"""
    # 生成大量历史邮件行（撑体量）
    import random
    rng = random.Random(999)
    topics = [
        "staffing ratio review", "float pool expansion proposal", "FMLA coverage protocol",
        "on-call list update", "charge nurse training", "agency nurse utilization",
        "overtime cap discussion", "electronic staffing system RFP", "acuity tool evaluation",
        "CDPH audit preparation", "Joint Commission readiness", "NPG 12 compliance gap",
        "Med/Surg night coverage", "ICU travel nurse contract", "Telemetry census projections",
    ]
    senders = ["Kevin Torres (Union)", "Miranda Chen (CNO)", "Tom Bradley (HR)", "Patricia Lowe (Head Nurse)"]
    for i in range(1, 301):
        date = f"202{3 + i // 120}-{((i // 10) % 12) + 1:02d}-{(i % 28) + 1:02d}"
        sender = rng.choice(senders)
        topic = rng.choice(topics)
        memo += (f"EMAIL {i:03d} | Date: {date} | From: {sender}\n"
                 f"Subject: Re: {topic}\n"
                 f"Summary: {sender} addressed concerns regarding {topic} at SVMC. "
                 f"Key point {i}: {'Compliance maintained' if i % 3 != 0 else 'Concern raised re: staffing gap'}.\n\n")

    memo += """
═══════════════════════════════════════════════════════════════════════
ARTICLE 5: SIGNATURES
═══════════════════════════════════════════════════════════════════════

FOR SEIU HEALTHCARE WORKERS WEST:
Kevin Torres, Union Representative
Date: January 20, 2026

FOR SUTTER VALLEY MEDICAL CENTER:
Miranda Chen, Chief Nursing Officer
Tom Bradley, HR Director
Date: January 20, 2026

CDPH ACKNOWLEDGMENT:
Inspector Linda Wu (witness only — CDPH does not endorse settlement terms)
Date: January 22, 2026

END OF SETTLEMENT MEMORANDUM
"""
    return memo


def _gen_historical_email_thread() -> str:
    """生成扩展历史邮件线程（撑 Update 2 体量）。"""
    text = "UNION-HOSPITAL EXTENDED EMAIL ARCHIVE\n\nDate range: October 2023 – January 2026\n\n"
    import random
    rng = random.Random(123)
    for i in range(1, 400):
        month = (i % 15) + 1 if (i % 15) < 12 else (i % 12) + 1
        year = 2023 + (i // 120)
        day = (i % 28) + 1
        text += (f"MESSAGE {i:04d}\n"
                 f"Date: {year:04d}-{month:02d}-{day:02d}\n"
                 f"From: {'Kevin Torres (SEIU)' if i % 2 == 0 else 'Tom Bradley (SVMC HR)'}\n"
                 f"Body: Message {i} regarding SVMC staffing compliance efforts, FMLA coverage "
                 f"protocols, and on-call list maintenance. Reference shift data from "
                 f"{year:04d}-{month:02d}-{day:02d}. Acknowledged by CNO Miranda Chen. "
                 f"Thread {i % 30 + 1} of 30 active threads.\n\n")
    return text


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()
    gen_regulations()
    nurses = gen_nurse_roster(WS / "hospital_data" / "SVMC_nurse_roster.csv")
    gen_staffing_log(WS / "hospital_data" / "SVMC_staffing_log_oct2024.csv", nurses)
    gen_census_data(WS / "hospital_data" / "SVMC_unit_census_oct2024.csv")
    gen_on_call_lists(WS)
    gen_fmla_schedule(WS / "hospital_data" / "SVMC_FMLA_leave_schedule.csv")
    gen_travel_nurse_contracts(WS / "hospital_data" / "SVMC_travel_nurse_contracts.csv")
    gen_communications(WS)
    gen_reports_and_scripts(WS)

    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = (
        "Medical staffing ratio crisis: SVMC nurse-to-patient ratio compliance, CDPH enforcement, "
        "CA Title 22 § 70217 / H&SC § 1280.3 / AFL-23-27 / SB 596 daily penalty / OR HB 2697 comparison. "
        "17 exec_check rounds, 2 updates (U2 supersedes 4 Telemetry violations from U1), "
        "5 preference rules P1-P5, difficulty vectors V1/V2/V4/V5/V6/V7/V8/V9/V10. "
        "Real sources: "
        "CA Title 22 § 70217 (https://www.law.cornell.edu/regulations/california/Cal-Code-Regs-Tit-22-SS-70217); "
        "H&SC § 1280.3 (https://law.justia.com/codes/california/code-hsc/division-2/chapter-2/article-3/section-1280-3/); "
        "AFL-23-27 (https://www.cdph.ca.gov/Programs/CHCQ/LCP/Pages/AFL-23-27.aspx); "
        "SB 596 (https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260SB596); "
        "OR HB 2697 (https://olis.oregonlegislature.gov/liz/2023R1/Downloads/MeasureDocument/HB2697/Enrolled)."
    )

    dump_register_meta(
        DATASET, test_id=TID, desc=desc,
        main_session=sess_ids["main"],
        history_sessions=sess_ids["history"],
        updates=updates_decl,
    )

    # 体量报告
    total = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                for p in WS.rglob("*") if p.is_file())
    sess_tok = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                   for p in SESS.glob("*.jsonl"))
    upd_tok = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                  for p in UPD.rglob("*") if p.is_file())
    print(f"[sci3] workspace tokens ~{total:,} | sessions ~{sess_tok:,} | updates ~{upd_tok:,}")
    print(f"[sci3] built at {DATASET}")


if __name__ == "__main__":
    main()
