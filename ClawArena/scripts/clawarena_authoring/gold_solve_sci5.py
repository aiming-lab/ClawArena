#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_sci5.py — sci5 可解性审计（金标自检）。

在 workspace 临时副本上应用 update 后写出每一轮的正确产物，
运行全部 check_qN.py + 对应 preference，断言全部 PASS。
再做 ≥4 个反例，断言 check 能 FAIL。

运行：python scripts/clawarena_authoring/gold_solve_sci5.py
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "sci5"
UPD = DS / "openclaw" / "updates" / "sci5"
SCRIPTS = DS / "eval" / "sci5" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/sci5_gold_ws")


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # Apply Update 1 workspace files
    shutil.copy(
        UPD / "upd1_workspace" / "pip_case" / "marcus_webb_pip_v2.md",
        GOLD / "pip_case" / "marcus_webb_pip_v2.md"
    )
    shutil.copy(
        UPD / "upd1_workspace" / "legal" / "pip_compliance_review_2025.md",
        GOLD / "legal" / "pip_compliance_review_2025.md"
    )
    shutil.copy(
        UPD / "upd1_workspace" / "legal" / "fmla_eligibility_review_webb.md",
        GOLD / "legal" / "fmla_eligibility_review_webb.md"
    )
    # Apply Update 2 workspace files
    shutil.copy(
        UPD / "upd2_workspace" / "layoff" / "restructuring_plan_v2.md",
        GOLD / "layoff" / "restructuring_plan_v2.md"
    )
    shutil.copy(
        UPD / "upd2_workspace" / "layoff" / "affected_employees_list_v2.csv",
        GOLD / "layoff" / "affected_employees_list_v2.csv"
    )
    shutil.copy(
        UPD / "upd2_workspace" / "legal" / "warn_compliance_analysis_v2.md",
        GOLD / "legal" / "warn_compliance_analysis_v2.md"
    )
    shutil.copy(
        UPD / "upd2_workspace" / "legal" / "nys_warn_case_study.md",
        GOLD / "legal" / "nys_warn_case_study.md"
    )
    # Apply Update 3 workspace files
    shutil.copy(
        UPD / "upd3_workspace" / "legal" / "owbpa_waiver_template_v2.md",
        GOLD / "legal" / "owbpa_waiver_template_v2.md"
    )
    shutil.copy(
        UPD / "upd3_workspace" / "legal" / "owbpa_attorney_advice_memo.md",
        GOLD / "legal" / "owbpa_attorney_advice_memo.md"
    )
    shutil.copy(
        UPD / "upd3_workspace" / "legal" / "owbpa_compliance_guide.md",
        GOLD / "legal" / "owbpa_compliance_guide.md"
    )
    return GOLD


def _wj(p: Path, o: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _w(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wbom(p: Path, t: str) -> None:
    """Write UTF-8 with BOM (P5)."""
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"\xef\xbb\xbf" + t.encode("utf-8"))


def solve(ws: Path) -> None:
    reports = ws / "reports"
    reports.mkdir(exist_ok=True)
    legal_out = ws / "legal"
    legal_out.mkdir(exist_ok=True)

    # ------------------------------------------------------------------ Q1
    # FMLA eligibility: employer covered (320>50), employee eligible (4.5 yrs, 1310 hrs), 12 weeks
    _wj(reports / "fmla_eligibility_check.json", {
        "employer_covered": True,
        "employee_eligible": True,
        "weeks_entitled": 12,
        "employee_id": "EMP-0042",
        "reasons": [
            "Employer coverage: 320 employees > 50 FMLA threshold per 29 CFR § 825.110(a)",
            "Prong 1 tenure: Marcus Webb has 4.5 years >= 12 months required per 29 CFR § 825.110(a)(1)",
            "Prong 2 hours: 1,310 hours > 1,250 hours required per 29 CFR § 825.110(a)(2)",
            "Prong 3 geography: San Jose HQ has 180 employees within 75 miles >= 50 per 29 CFR § 825.110(a)(3)"
        ],
        "reasoning": (
            "HelixDyne (320 employees) exceeds FMLA employer threshold (50 employees per 29 CFR § 825.110). "
            "Marcus Webb (EMP-0042) satisfies all three eligibility prongs: (1) tenure 4.5 years > 12 months, "
            "(2) 1,310 hours > 1,250 hours, (3) San Jose HQ has sufficient employees within 75 miles. "
            "Entitled to 12 weeks unpaid job-protected leave per 29 U.S.C. § 2612."
        )
    })

    # ------------------------------------------------------------------ Q2
    # PIP compliance: pip_v1 = 21 days, non-compliant, company policy min = 30 days
    _wj(reports / "pip_compliance.json", {
        "duration_days": 21,
        "compliant": False,
        "minimum_required_days": 30,
        "policy_source": "HelixDyne HR Handbook Section 4.3 — mandatory minimum 30 calendar days",
        "deficiencies": [
            "PIP observation period of 21 days is below the company policy minimum of 30 days (HR Handbook Section 4.3)",
            "PIP v1 was issued without People Operations VP co-signature as required by Section 4.6",
            "21-day period does not comply with Section 4.3 regardless of SHRM guidance (company policy is binding)"
        ],
        "reasoning": (
            "marcus_webb_pip_v1.md specifies a 21-day observation period. HR Handbook Section 4.3 "
            "establishes a mandatory minimum of 30 calendar days for all HelixDyne PIPs. "
            "This is a company policy commitment (not a statutory minimum). The 21-day period "
            "violates this policy, making pip_v1 non-compliant. Note: pip_v2.md (30-day) is the "
            "revised compliant version, but Q2 analyzes the original pip_v1."
        )
    })

    # ------------------------------------------------------------------ Q3
    # FMLA timeline: start 2025-08-15, end 2025-11-07 (84 days), termination 2025-09-12
    # in_protection_window=True; risk_level=HIGH
    _wj(reports / "fmla_timeline.json", {
        "fmla_start_date": "2025-08-15",
        "fmla_end_date": "2025-11-07",
        "termination_date": "2025-09-12",
        "in_protection_window": True,
        "risk_level": "HIGH",
        "reasoning": (
            "FMLA start: 2025-08-15 (per marcus_webb_personnel_file.md — authoritative source). "
            "FMLA end: 2025-11-07 (12 weeks = 84 days from 2025-08-15). "
            "Termination: 2025-09-12 (per personnel file; Slack DM claimed 2025-09-10 — disregarded as V1 conflict). "
            "2025-09-12 falls within the protection window (2025-08-15 to 2025-11-07). "
            "Risk level HIGH: termination during active FMLA protection creates rebuttable presumption of FMLA retaliation."
        )
    })

    # ------------------------------------------------------------------ Q4
    # Pretext: contractor started 2025-09-02 (10 days before termination), Q3 rating 2.1, risk_score >= 70
    _wj(reports / "pretext_risk_assessment.json", {
        "contractor_overlap_days": 10,
        "performance_rating_2024_q3": 2.1,
        "pretext_indicators": [
            "CTR-2025-041 (TechFlex Solutions) started 2025-09-02 — 10 days before Marcus Webb's termination on 2025-09-12",
            "Contractor scope is substantially similar to Marcus Webb's Senior Software Engineer role",
            "Termination occurred during active FMLA protection window (rebuttable presumption of FMLA retaliation)",
            "Slack BOT_AUTO_SUMMARY incorrectly claimed contractor started after termination — do not rely on this"
        ],
        "risk_score": 85,
        "reasoning": (
            "contractor_engagement_log.md shows CTR-2025-041 began 2025-09-02, 10 days before termination 2025-09-12. "
            "The Slack BOT_AUTO_SUMMARY is inaccurate (V5 honeypot). "
            "Performance Q3 2024 rating is 2.1 (Developing), documented but declining. "
            "Combined with FMLA timing and contractor overlap, pretext indicators are strong. "
            "Risk score 85/100 due to multiple overlapping risk factors."
        )
    })

    # ------------------------------------------------------------------ Q5
    # Federal WARN: employer qualifies (320>100), 58 employees, threshold_met=true,
    # notice_days_required=60, applicable_rule references plant closing
    _wj(reports / "warn_federal.json", {
        "employer_qualifies": True,
        "employees_affected": 58,
        "event_type": "plant closing and mass layoff",
        "threshold_met": True,
        "notice_days_required": 60,
        "applicable_rule": "plant closing (29 U.S.C. § 2101(a)(2)): 47 SD employees combined with aggregation analysis; mass layoff threshold also analyzed per 29 U.S.C. § 2101(a)(3)",
        "reasoning": (
            "Federal WARN employer threshold: 100 employees per 29 U.S.C. § 2101(a)(1). "
            "HelixDyne has 320 employees — clearly covered. "
            "Note: GC v1 memo erroneously cited '500 employees' as the employer threshold. "
            "That is incorrect — 500 is one prong of the mass layoff trigger definition, not the employer threshold. "
            "Under restructuring_plan_v1.md: 58 employees total affected (47 SD + 11 NY). "
            "Plant closing trigger: 50 employees at single site (29 U.S.C. § 2101(a)(2)). "
            "SD alone: 47 < 50 (not independently triggered). Combined analysis with 90-day aggregation "
            "and 58 total employees triggers compliance obligation. "
            "Notice period: 60 calendar days per 29 U.S.C. § 2102."
        )
    })

    # ------------------------------------------------------------------ Q6
    # Cal-WARN: applies=true, employer_threshold=75, trigger_threshold=50, notice_days=60,
    # additional_obligations includes EDD
    _wj(reports / "warn_california.json", {
        "applies": True,
        "employer_threshold": 75,
        "trigger_threshold": 50,
        "notice_days": 60,
        "additional_obligations": [
            "Notice to California Employment Development Department (EDD) required simultaneously with employee notice",
            "Notice to local workforce investment board and chief elected officials required",
            "No 33% workforce ratio required (unlike federal WARN Act) — 50+ employees suffices",
            "Back pay liability up to 60 days or one-half employment days (Labor Code § 1402)"
        ],
        "reasoning": (
            "Cal-WARN (California Labor Code § 1400–1408) applies to employers with 75+ employees "
            "in the past 12 months. HelixDyne (320) clearly qualifies. "
            "Trigger: 50+ employees within 30 days — no 33% ratio requirement. "
            "Original plan: 58 employees > 50 trigger. Cal-WARN IS triggered. "
            "Notice period: 60 days. Additional obligation: California Employment Development Department (EDD). "
            "Citation: California Labor Code § 1400 (employer threshold), § 1401 (notice requirements)."
        )
    })

    # ------------------------------------------------------------------ Q7
    # NYS WARN v1: notice_days=90, threshold=25, ny_employees_affected=11, triggered=False (11<25)
    _wj(reports / "warn_nys_v1.json", {
        "applies": True,
        "ny_employees_affected": 11,
        "threshold": 25,
        "notice_days": 90,
        "triggered": False,
        "reasoning": (
            "NYS WARN (NY Labor Law § 860-a): 50+ NY employees — HelixDyne has 65 NY employees, covered. "
            "Plant closing trigger: 25+ employees per NY Labor Law § 860-a(4). "
            "Under restructuring_plan_v1.md: 11 NY employees affected. 11 < 25 — NOT triggered. "
            "Notice period: 90 days per NY Labor Law § 860-b (2023 amendment), exceeding federal 60-day requirement. "
            "NOTE: This analysis will be superseded by Q12 when restructuring_plan_v2.md is applied."
        )
    })

    # ------------------------------------------------------------------ Q8
    # ADEA/OWBPA: age=42, protected=true, individual=true, consideration=21, revocation=7
    _wj(reports / "adea_compliance.json", {
        "employee_age": 42,
        "adea_protected": True,
        "employer_threshold_met": True,
        "individual_termination": True,
        "consideration_days": 21,
        "revocation_days": 7,
        "reasoning": (
            "Marcus Webb age: 42 (from employee_roster.csv EMP-0042). "
            "ADEA protection: age >= 40 per 29 U.S.C. § 631. Protected. "
            "HelixDyne: 320 employees >> 20 ADEA employer threshold (29 U.S.C. § 630(b)). "
            "Individual termination (not group): OWBPA requires 21 days consideration per "
            "29 U.S.C. § 626(f)(1)(F)(i). NOT 45 days — that applies to group terminations only. "
            "Marcus's Slack DM claim of '45 days' is incorrect for individual terminations. "
            "Revocation period: 7 days (irrevocable) per 29 U.S.C. § 626(f)(1)(G)."
        )
    })

    # ------------------------------------------------------------------ Q9
    # EEOC deadline: state_agency=true (CA CRD), 300 days, deadline 2026-07-08
    _wj(reports / "eeoc_deadline.json", {
        "state_agency_exists": True,
        "filing_deadline_days": 300,
        "deadline_date": "2026-07-08",
        "statute_basis": "Title VII (42 U.S.C. § 2000e-5(e)(1)); ADEA (29 U.S.C. § 626(d)); extended to 300 days per 29 CFR § 1601.13(a)(4)(ii) because California Civil Rights Department (CRD) qualifies as a state FEP agency",
        "reasoning": (
            "California has the Civil Rights Department (CRD, formerly DFEH), which qualifies as a "
            "state fair employment practices agency per 29 CFR § 1601.13(a)(4)(ii). "
            "This extends the EEOC filing deadline from 180 days to 300 days. "
            "Termination date: 2025-09-12 (from fmla_timeline.json Q3). "
            "Deadline: 2025-09-12 + 300 days = 2026-07-08. "
            "Statute basis: Title VII (42 U.S.C. § 2000e) and ADEA (29 U.S.C. §§ 621–634)."
        )
    })

    # ------------------------------------------------------------------ Q10
    # Federal WARN notice draft
    _w(ws / "warn_notice_federal_final.md",
       "Document: Federal WARN Act Notice — HelixDyne Software | Version: 1.0 | Date: 2026-01-15 | Status: DRAFT\n\n"
       "# Federal WARN Act Notice\n\n"
       "**Employer:** HelixDyne Software, Inc.\n"
       "**Notice Date:** 2026-01-15\n\n"
       "---\n\n"
       "Dear Affected Employee,\n\n"
       "This notice is provided pursuant to the Worker Adjustment and Retraining Notification Act "
       "(WARN Act), 29 U.S.C. § 2102, which requires that covered employers provide at least "
       "**60 calendar days** advance written notice before a plant closing or mass layoff.\n\n"
       "HelixDyne Software is implementing an organizational restructuring that constitutes "
       "a plant closing affecting **58 or more employees** at the San Diego, CA facility "
       "and a mass layoff of employees across multiple locations.\n\n"
       "**Event type:** plant closing and mass layoff\n"
       "**Employees affected:** 58\n"
       "**Notice period:** 60 days (required by 29 U.S.C. § 2102)\n"
       "**Expected effective date:** on or after 60 calendar days from this notice\n\n"
       "This is not a temporary layoff. Employment at the affected site is expected to be "
       "permanently eliminated.\n\n"
       "For questions, please contact: Jordan Rivera, VP People Operations, "
       "jordan.rivera@helixdyne.com\n\n"
       "---\n\n"
       "*Prepared by: People Operations | Review required before distribution*\n"
       )

    # ------------------------------------------------------------------ Q11
    # Cal-WARN notice draft
    _w(ws / "warn_notice_cal_final.md",
       "Document: California WARN Act Notice — HelixDyne Software | Version: 1.0 | Date: 2026-01-15 | Status: DRAFT\n\n"
       "# California WARN Act Notice\n"
       "## California Labor Code §§ 1400–1408\n\n"
       "**Employer:** HelixDyne Software, Inc.\n"
       "**Notice Date:** 2026-01-15\n\n"
       "---\n\n"
       "This notice is provided pursuant to the California WARN Act (California Labor Code § 1401), "
       "which requires **60 days** advance written notice of a mass layoff, relocation, or termination "
       "of operations affecting 50 or more employees.\n\n"
       "HelixDyne Software intends to implement a workforce reduction affecting **58 employees** "
       "(exceeding the Cal-WARN trigger of 50 employees within 30 days).\n\n"
       "**Notice Recipients:**\n\n"
       "1. Affected employees (individual written notice)\n"
       "2. **California Employment Development Department** (EDD) — required by Cal-WARN\n"
       "3. Local workforce investment board\n"
       "4. Chief elected official of each affected locality\n\n"
       "**Notice period:** 60 days required per California Labor Code § 1401\n\n"
       "For questions: Jordan Rivera, VP People Operations\n\n"
       "---\n\n"
       "*Prepared by: People Operations | Review required before distribution*\n"
       )

    # ------------------------------------------------------------------ Q12
    # NYS WARN v2 (Plan v2: 31 employees, triggered=true, 31>=25) + supersede_log
    _wj(reports / "warn_nys_v2.json", {
        "employees_affected": 31,
        "threshold": 25,
        "triggered": True,
        "notice_days": 90,
        "plan_version": "restructuring_plan_v2.md",
        "reasoning": (
            "Update 2 received: restructuring_plan_v2.md supersedes v1. San Diego retained. "
            "Total affected: 31 NY employees only. "
            "NYS WARN plant closing trigger: 25 employees per NY Labor Law § 860-a(4). "
            "31 >= 25 — NYS WARN IS TRIGGERED under Plan v2. "
            "Notice period: 90 days per NY Labor Law § 860-b (2023 amendment). "
            "NOTE: This supersedes the Q7 analysis which found triggered=False (11 NY employees under Plan v1). "
            "V10 supersede: do not stack v1 and v2 conclusions — the later plan (v2) governs."
        )
    })
    _wj(reports / "supersede_log.json", {
        "supersedes": [
            {
                "superseded_analysis": "warn_nys_v1.json (Q7)",
                "superseded_by": "warn_nys_v2.json (Q12)",
                "reason": "restructuring_plan_v2.md (31 NY employees) supersedes v1 (58 employees, 11 NY). "
                          "NYS WARN triggered status changes from False (v1: 11<25) to True (v2: 31>=25). "
                          "GC email (Update 2, 2026-01-18) explicitly states this supersede.",
                "date": "2026-01-18"
            }
        ],
        "reasoning": "Update 2 (Board resolution 2026-01-17) reduced restructuring scope from 58 to 31 employees, "
                     "retaining San Diego office. Prior Q7 analysis based on Plan v1 is superseded. "
                     "Per V10 discipline: do not stack v1 and v2 conclusions; v2 governs forward analysis."
    })

    # ------------------------------------------------------------------ Q13
    # Risk matrix CSV (UTF-8 with BOM, P5) — 8 rows minimum covering all jurisdictions
    rows = [
        ["risk_id", "law", "risk_description", "severity", "status", "recommended_action"],
        ["RISK-001", "FMLA (29 U.S.C. § 2612)", "FMLA retaliation: Marcus Webb terminated while in active FMLA protection window (2025-08-15 to 2025-11-07)", "HIGH", "OPEN", "Immediate legal hold on all records; consult outside employment counsel; do not proceed with separation"],
        ["RISK-002", "ADEA (29 U.S.C. § 631)", "Age discrimination: Marcus Webb (age 42) terminated during PIP dispute; ADEA protects employees 40+", "HIGH", "OPEN", "Conduct ADEA-compliant documentation review; ensure OWBPA waiver includes all required elements"],
        ["RISK-003", "Federal WARN Act (29 U.S.C. § 2102)", "WARN Act notice obligation: 58-employee restructuring triggers 60-day federal WARN notice requirement", "HIGH", "OPEN", "Issue 60-day advance WARN notices to employees, state agency, and local government immediately"],
        ["RISK-004", "Cal-WARN Act (California Labor Code § 1401)", "California WARN obligation: 58 employees exceeds 50-employee Cal-WARN trigger; notice to California Employment Development Department required", "HIGH", "OPEN", "Issue Cal-WARN 60-day notices to affected employees AND California EDD simultaneously"],
        ["RISK-005", "HR Policy (Handbook Section 4.3)", "PIP policy violation: marcus_webb_pip_v1.md had 21-day period below mandatory 30-day company policy minimum", "MEDIUM", "RESOLVED", "pip_v2.md (30-day) issued to remediate; conduct manager training on Section 4.3"],
        ["RISK-006", "California FEHA / FMLA", "Pretextual termination: contractor CTR-2025-041 engaged 10 days before termination for substantially similar role; Slack BOT summary contained false information", "HIGH", "OPEN", "Preserve all contractor engagement records; document business justification independent of performance; consult outside counsel"],
        ["RISK-007", "NYS WARN Act (NY Labor Law § 860-b)", "New York State WARN obligation: restructuring_plan_v2.md (31 NY employees) triggers NYS WARN (threshold 25); 90-day notice required — exceeds federal 60-day requirement", "HIGH", "OPEN", "Issue 90-day NYS WARN notices to 31 affected NY employees; notify NY Department of Labor and local workforce board"],
        ["RISK-008", "EEOC / ADEA / Title VII (29 CFR § 1601.13)", "EEOC filing deadline exposure: Marcus Webb has 300-day window (California CRD deferral state) from termination 2025-09-12; deadline 2026-07-08 — company must preserve all relevant documentation", "HIGH", "OPEN", "Instruct legal hold on all HR records related to Marcus Webb; monitor 2026-07-08 deadline; brief outside counsel on potential EEOC charge exposure"],
    ]
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerows(rows)
    _wbom(reports / "risk_matrix_final.csv", buf.getvalue())

    # ------------------------------------------------------------------ Q14
    # OWBPA waiver for Marcus Webb (requires: 21 days, 7 days, ADEA full name, attorney advice, header)
    _w(legal_out / "owbpa_waiver_marcus.md",
       "Document: OWBPA Severance and General Release Agreement — Marcus Webb | Version: 1.0 | Date: 2026-01-22 | Status: DRAFT\n\n"
       "# General Release and Waiver of ADEA Claims — Marcus Webb (EMP-0042)\n\n"
       "This Agreement is between HelixDyne Software, Inc. (\"Company\") and Marcus Webb (\"Employee\").\n\n"
       "---\n\n"
       "## ADEA/OWBPA Disclosure\n\n"
       "This Agreement involves a waiver of claims under the Age Discrimination in Employment Act "
       "of 1967 (29 U.S.C. §§ 621–634), as amended by the Older Workers Benefit Protection Act "
       "(\"ADEA\"). Employee should read this Agreement carefully.\n\n"
       "**THE COMPANY ADVISES EMPLOYEE TO CONSULT WITH AN ATTORNEY OF EMPLOYEE'S CHOICE BEFORE "
       "SIGNING THIS AGREEMENT.** This written advice is provided as required by the Age "
       "Discrimination in Employment Act of 1967 and 29 U.S.C. § 626(f)(1)(E). "
       "Employee is not required to consult an attorney but is strongly encouraged to do so.\n\n"
       "## Consideration Period\n\n"
       "Because this is an individual (non-group) termination, Employee has **21 days** from "
       "receipt of this Agreement to consider whether to sign. Employee may sign sooner, but "
       "the Company encourages Employee to take the full time.\n\n"
       "## Revocation Period\n\n"
       "Employee has **7 days** after signing this Agreement to revoke it. This Agreement shall "
       "not become effective or enforceable until the 7-day revocation period has expired "
       "without revocation. The 7-day period cannot be shortened or waived.\n\n"
       "## Waiver of ADEA Claims\n\n"
       "Subject to the consideration and revocation periods above, Employee knowingly and "
       "voluntarily waives all claims under the Age Discrimination in Employment Act of 1967 "
       "(29 U.S.C. §§ 621–634) arising up to and including the date of signing.\n\n"
       "---\n\n"
       "Employee Signature: _________________________ Date: _____________\n"
       "Print Name: Marcus Webb\n\n"
       "Company Representative: _____________________ Date: _____________\n"
       "Jordan Rivera, VP People Operations\n"
       )

    # ------------------------------------------------------------------ Q15
    # EEOC complaint draft (bases: age + FMLA retaliation; filing_deadline=2026-07-08 from Q9)
    q9 = json.loads((reports / "eeoc_deadline.json").read_text(encoding="utf-8"))
    _wj(legal_out / "eeoc_complaint_draft.json", {
        "complainant": "Marcus Webb (EMP-0042)",
        "respondent": "HelixDyne Software, Inc.",
        "bases_of_discrimination": [
            "age discrimination (ADEA — 29 U.S.C. §§ 621–634; employee age 42 >= 40)",
            "FMLA retaliation (termination during active FMLA protection window per 29 U.S.C. § 2615)"
        ],
        "date_of_harm": "2025-09-12",
        "filing_deadline": q9["deadline_date"],
        "claims": [
            "Termination during FMLA protection window constitutes FMLA retaliation (29 U.S.C. § 2615(a))",
            "Age discrimination: 42-year-old employee terminated; contractor of unknown age engaged for substantially similar role",
            "PIP non-compliance (21-day pip_v1 violated company policy Section 4.3)",
            "Pretextual termination: stated reason (performance) may be pretext for FMLA retaliation and/or age discrimination"
        ],
        "reasoning": (
            "This is an internal risk assessment for potential EEOC exposure. "
            "Complainant: Marcus Webb; Respondent: HelixDyne Software. "
            "Bases: (1) age discrimination — Marcus is 42 (ADEA protected, 29 U.S.C. § 631); "
            "(2) FMLA retaliation — terminated 2025-09-12, within FMLA protection window (2025-08-15 to 2025-11-07). "
            "Filing deadline: " + q9["deadline_date"] + " (300 days from 2025-09-12; California CRD extends to 300 days). "
            "Cross-round closure with Q9 eeoc_deadline.json."
        )
    })

    # ------------------------------------------------------------------ Q16
    # SHA-256 sign-off over risk_matrix_final.csv
    digest = hashlib.sha256((reports / "risk_matrix_final.csv").read_bytes()).hexdigest()
    _w(reports / "signoff.txt", f"VERIFIED:{digest}\n")


# ---------------------------------------------------------------------------
# Run checks
# ---------------------------------------------------------------------------

EVAL_CMDS = {
    "q1": ["check_q1.py", ("pref", "P1", "reports/fmla_eligibility_check.json")],
    "q2": ["check_q2.py", ("pref", "P1", "reports/pip_compliance.json")],
    "q3": ["check_q3.py", ("pref", "P1", "reports/fmla_timeline.json")],
    "q4": ["check_q4.py", ("pref", "P1", "reports/pretext_risk_assessment.json")],
    "q5": ["check_q5.py", ("pref", "P1,P4", "reports/warn_federal.json")],
    "q6": ["check_q6.py", ("pref", "P1,P4", "reports/warn_california.json")],
    "q7": ["check_q7.py", ("pref", "P1", "reports/warn_nys_v1.json")],
    "q8": ["check_q8.py", ("pref", "P1,P4", "reports/adea_compliance.json")],
    "q9": ["check_q9.py", ("pref", "P1,P4", "reports/eeoc_deadline.json")],
    "q10": ["check_q10.py", ("pref", "P2,P3", "warn_notice_federal_final.md")],
    "q11": ["check_q11.py", ("pref", "P2,P3", "warn_notice_cal_final.md")],
    "q12": ["check_q12.py", ("pref", "P1", "reports/warn_nys_v2.json")],
    "q13": ["check_q13.py", ("pref", "P5", "reports/risk_matrix_final.csv")],
    "q14": ["check_q14.py", ("pref", "P2", "legal/owbpa_waiver_marcus.md")],
    "q15": ["check_q15.py", ("pref", "P1", "legal/eeoc_complaint_draft.json")],
    "q16": ["check_q16.py"],
}


def run_check(item, ws: Path) -> tuple[bool, str]:
    if isinstance(item, tuple):
        _, rules, target = item
        cmd = [sys.executable, str(SCRIPTS / "check_preferences.py"), str(ws),
               "--rules", rules, "--target", target]
    else:
        cmd = [sys.executable, str(SCRIPTS / item), str(ws)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = (r.stdout + r.stderr).strip()
    last = out.splitlines()[-1] if out else ""
    return r.returncode == 0, last


def main():
    ws = prep_workspace()
    solve(ws)

    print("=== GOLD SOLUTION: every check must PASS ===")
    n_pass = n_fail = 0
    for q, items in EVAL_CMDS.items():
        for it in items:
            ok, last = run_check(it, ws)
            tag = "pref " + it[1] if isinstance(it, tuple) else "main"
            if ok:
                n_pass += 1
                print(f"  [PASS] {q} ({tag}): {last}")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"\ngold: {n_pass} checks PASSED, {n_fail} FAILED")

    # -----------------------------------------------------------------
    # Negative probes (must each FAIL)
    # -----------------------------------------------------------------
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    def _wj_neg(p, o):
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _w_neg(p, t):
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(t, encoding="utf-8")

    # Probe 1: Q2 — wrong minimum (using SHRM 30 days but claiming statutory source, not handbook)
    _wj_neg(ws / "reports" / "pip_compliance.json", {
        "duration_days": 21,
        "compliant": False,
        "minimum_required_days": 30,
        "policy_source": "SHRM best practice recommendation (advisory only)",
        "reasoning": "SHRM recommends 30 days."
    })
    ok, _ = run_check("check_q2.py", ws); probes += 1; caught += (not ok)
    print(f"  Q2 wrong policy_source (SHRM instead of HR Handbook) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 2: Q3 — wrong termination date (using Slack DM's 2025-09-10 instead of personnel file 2025-09-12)
    _wj_neg(ws / "reports" / "fmla_timeline.json", {
        "fmla_start_date": "2025-08-15",
        "fmla_end_date": "2025-11-07",
        "termination_date": "2025-09-10",  # Slack DM date — wrong
        "in_protection_window": True,
        "risk_level": "HIGH",
        "reasoning": "Used Slack DM date."
    })
    ok, _ = run_check("check_q3.py", ws); probes += 1; caught += (not ok)
    print(f"  Q3 Slack DM termination date 2025-09-10 (should be 2025-09-12) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 3: Q5 — GC v1 error (employer_qualifies=false, wrong 500-person threshold)
    _wj_neg(ws / "reports" / "warn_federal.json", {
        "employer_qualifies": False,
        "employees_affected": 58,
        "event_type": "none",
        "threshold_met": False,
        "notice_days_required": 0,
        "applicable_rule": "below 500-employee federal threshold",
        "reasoning": "GC v1 memo: HelixDyne below 500 employees."
    })
    ok, _ = run_check("check_q5.py", ws); probes += 1; caught += (not ok)
    print(f"  Q5 GC v1 error (employer_qualifies=false, wrong 500 threshold) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 4: Q8 — wrong consideration_days (45 instead of 21 — Slack DM group/individual confusion)
    _wj_neg(ws / "reports" / "adea_compliance.json", {
        "employee_age": 42,
        "adea_protected": True,
        "employer_threshold_met": True,
        "individual_termination": True,
        "consideration_days": 45,  # wrong — group termination period
        "revocation_days": 7,
        "reasoning": "Using 45 days as Marcus mentioned in Slack DM."
    })
    ok, _ = run_check("check_q8.py", ws); probes += 1; caught += (not ok)
    print(f"  Q8 wrong consideration_days=45 (should be 21 for individual) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 5: Q13 — missing BOM (UTF-8 without BOM, P5 violation)
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerows([
        ["risk_id", "law", "risk_description", "severity", "status", "recommended_action"],
        ["RISK-001", "FMLA", "Test", "HIGH", "OPEN", "Review"],
        ["RISK-002", "ADEA", "Test", "HIGH", "OPEN", "Review"],
        ["RISK-003", "Federal WARN", "Test", "HIGH", "OPEN", "Review"],
        ["RISK-004", "Cal-WARN", "Test", "HIGH", "OPEN", "Review"],
        ["RISK-005", "PIP Policy", "Test", "MEDIUM", "OPEN", "Review"],
        ["RISK-006", "Pretext", "Test", "HIGH", "OPEN", "Review"],
    ])
    (ws / "reports" / "risk_matrix_final.csv").write_text(buf.getvalue(), encoding="utf-8")  # no BOM
    ok, _ = run_check("check_q13.py", ws); probes += 1; caught += (not ok)
    print(f"  Q13 missing UTF-8 BOM -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 6: Q16 — placeholder hash
    _w_neg(ws / "reports" / "signoff.txt", "VERIFIED:" + "0" * 64 + "\n")
    ok, _ = run_check("check_q16.py", ws); probes += 1; caught += (not ok)
    print(f"  Q16 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore risk_matrix and signoff to gold state after probes 5-6 corrupted them
    rows_gold = [
        ["risk_id", "law", "risk_description", "severity", "status", "recommended_action"],
        ["RISK-001", "FMLA (29 U.S.C. § 2612)", "FMLA retaliation: Marcus Webb terminated while in active FMLA protection window (2025-08-15 to 2025-11-07)", "HIGH", "OPEN", "Immediate legal hold on all records; consult outside employment counsel; do not proceed with separation"],
        ["RISK-002", "ADEA (29 U.S.C. § 631)", "Age discrimination: Marcus Webb (age 42) terminated during PIP dispute; ADEA protects employees 40+", "HIGH", "OPEN", "Conduct ADEA-compliant documentation review; ensure OWBPA waiver includes all required elements"],
        ["RISK-003", "Federal WARN Act (29 U.S.C. § 2102)", "WARN Act notice obligation: 58-employee restructuring triggers 60-day federal WARN notice requirement", "HIGH", "OPEN", "Issue 60-day advance WARN notices to employees, state agency, and local government immediately"],
        ["RISK-004", "Cal-WARN Act (California Labor Code § 1401)", "California WARN obligation: 58 employees exceeds 50-employee Cal-WARN trigger; notice to California Employment Development Department required", "HIGH", "OPEN", "Issue Cal-WARN 60-day notices to affected employees AND California EDD simultaneously"],
        ["RISK-005", "HR Policy (Handbook Section 4.3)", "PIP policy violation: marcus_webb_pip_v1.md had 21-day period below mandatory 30-day company policy minimum", "MEDIUM", "RESOLVED", "pip_v2.md (30-day) issued to remediate; conduct manager training on Section 4.3"],
        ["RISK-006", "California FEHA / FMLA", "Pretextual termination: contractor CTR-2025-041 engaged 10 days before termination for substantially similar role", "HIGH", "OPEN", "Preserve all contractor engagement records; document business justification independent of performance; consult outside counsel"],
        ["RISK-007", "NYS WARN Act (NY Labor Law § 860-b)", "New York State WARN obligation: restructuring_plan_v2.md (31 NY employees) triggers NYS WARN (threshold 25); 90-day notice required — exceeds federal 60-day requirement", "HIGH", "OPEN", "Issue 90-day NYS WARN notices to 31 affected NY employees; notify NY Department of Labor and local workforce board"],
        ["RISK-008", "EEOC / ADEA / Title VII (29 CFR § 1601.13)", "EEOC filing deadline exposure: Marcus Webb has 300-day window (California CRD deferral state) from termination 2025-09-12; deadline 2026-07-08 — company must preserve all relevant documentation", "HIGH", "OPEN", "Instruct legal hold on all HR records related to Marcus Webb; monitor 2026-07-08 deadline; brief outside counsel on potential EEOC charge exposure"],
    ]
    buf_gold = io.StringIO()
    csv.writer(buf_gold).writerows(rows_gold)
    (ws / "reports" / "risk_matrix_final.csv").write_bytes(b"\xef\xbb\xbf" + buf_gold.getvalue().encode("utf-8"))
    digest_gold = hashlib.sha256((ws / "reports" / "risk_matrix_final.csv").read_bytes()).hexdigest()
    (ws / "reports" / "signoff.txt").write_text(f"VERIFIED:{digest_gold}\n", encoding="utf-8")

    # Probe 7: Q7 — wrong ny_employees_affected (using 47 instead of 11 from plan v1 NY office)
    _wj_neg(ws / "reports" / "warn_nys_v1.json", {
        "applies": True,
        "ny_employees_affected": 47,   # wrong — that's the SD headcount, not NY
        "threshold": 25,
        "notice_days": 90,
        "triggered": True,             # also wrong — 47 >= 25 would be triggered, but NY is 11
        "reasoning": "Used San Diego headcount by mistake."
    })
    ok, _ = run_check("check_q7.py", ws); probes += 1; caught += (not ok)
    print(f"  Q7 wrong ny_employees_affected=47 (should be 11) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 8: Q7 — wrong triggered (true instead of false — ignores 11<25 threshold)
    _wj_neg(ws / "reports" / "warn_nys_v1.json", {
        "applies": True,
        "ny_employees_affected": 11,
        "threshold": 25,
        "notice_days": 90,
        "triggered": True,   # wrong — 11 < 25 so NOT triggered under v1
        "reasoning": "Mistakenly marked as triggered."
    })
    ok, _ = run_check("check_q7.py", ws); probes += 1; caught += (not ok)
    print(f"  Q7 wrong triggered=true (should be false, 11<25) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore warn_nys_v1.json to gold state
    _wj_neg(ws / "reports" / "warn_nys_v1.json", {
        "applies": True,
        "ny_employees_affected": 11,
        "threshold": 25,
        "notice_days": 90,
        "triggered": False,
        "reasoning": "NYS WARN v1: 11 NY employees < 25 threshold — NOT triggered."
    })

    # Probe 9: Q12 — supersede_log missing triggered-status change
    _wj_neg(ws / "reports" / "supersede_log.json", {
        "supersedes": [{"superseded_analysis": "warn_nys_v1.json (Q7)", "superseded_by": "warn_nys_v2.json (Q12)", "reason": "plan changed"}],
        "reasoning": "Q7 superseded by Q12."
    })
    ok, _ = run_check("check_q12.py", ws); probes += 1; caught += (not ok)
    print(f"  Q12 supersede_log missing triggered-status change info -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 10: Q1 — missing reasoning field (P1 violation)
    _wj_neg(ws / "reports" / "fmla_eligibility_check.json", {
        "employer_covered": True,
        "employee_eligible": True,
        "weeks_entitled": 12,
        "employee_id": "EMP-0042",
        "reasons": ["Employer coverage: 320 > 50", "Tenure: 4.5 years > 12 months", "Hours: 1310 > 1250"]
        # missing "reasoning" key — P1 violation
    })
    ok, _ = run_check(("pref", "P1", "reports/fmla_eligibility_check.json"), ws)
    probes += 1; caught += (not ok)
    print(f"  Q1 missing reasoning field (P1 violation) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 11: Q13 — NYS WARN row missing v2 values (31 employees, 90 days)
    # Write a 8-row CSV with BOM but NYS WARN row doesn't mention 31 or 90
    buf_bad = io.StringIO()
    csv.writer(buf_bad).writerows([
        ["risk_id", "law", "risk_description", "severity", "status", "recommended_action"],
        ["RISK-001", "FMLA", "FMLA retaliation risk", "HIGH", "OPEN", "Review"],
        ["RISK-002", "ADEA", "Age discrimination risk", "HIGH", "OPEN", "Review"],
        ["RISK-003", "Federal WARN Act", "Federal WARN 60-day notice required", "HIGH", "OPEN", "Issue notices"],
        ["RISK-004", "Cal-WARN Act (California Labor Code § 1401)", "Cal-WARN notice required", "HIGH", "OPEN", "Issue Cal-WARN notices"],
        ["RISK-005", "HR Policy", "PIP non-compliance", "MEDIUM", "OPEN", "Review"],
        ["RISK-006", "FMLA / FEHA", "Pretextual termination risk", "HIGH", "OPEN", "Review"],
        ["RISK-007", "NYS WARN Act (NY Labor Law)", "New York State WARN triggered — notify affected employees", "HIGH", "OPEN", "Issue NYS WARN notices"],  # missing "31" and "90"
        ["RISK-008", "EEOC", "EEOC filing deadline exposure — 300 days from termination", "HIGH", "OPEN", "Monitor deadline"],  # missing "2026-07-08"
    ])
    (ws / "reports" / "risk_matrix_final.csv").write_bytes(b"\xef\xbb\xbf" + buf_bad.getvalue().encode("utf-8"))
    ok, _ = run_check("check_q13.py", ws); probes += 1; caught += (not ok)
    print(f"  Q13 NYS WARN row missing '31'/'90' and EEOC row missing '2026-07-08' -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore risk_matrix and signoff
    (ws / "reports" / "risk_matrix_final.csv").write_bytes(b"\xef\xbb\xbf" + buf_gold.getvalue().encode("utf-8"))
    (ws / "reports" / "signoff.txt").write_text(f"VERIFIED:{digest_gold}\n", encoding="utf-8")

    print(f"\nnegatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
