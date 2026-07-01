#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_sci3.py — sci3 可解性审计（金标自检）。

在 workspace 临时副本上应用 update 后写金标产物，
跑全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再用 ≥4 个反例（错误产物）断言 check 能 FAIL。

运行：python scripts/clawarena_authoring/gold_solve_sci3.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "sci3"
UPD = DS / "openclaw" / "updates" / "sci3"
SCRIPTS = DS / "eval" / "sci3" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/sci3_gold_ws")


# Ground-truth constants (from real regulations)
LEGAL_RATIOS = {"ICU": 2, "Med/Surg": 5, "Step-Down": 3, "Telemetry": 4, "ED": 4, "Psychiatric": 6}
FIRST_VIOLATION_FEE = 15000   # H&SC § 1280.3
SUBSEQUENT_VIOLATION_FEE = 30000
SB596_EFFECTIVE_DATE = "2026-01-01"

# October 2024 violations (from CDPH letter, build_sci3.py injection)
# 3 ICU charge nurse errors + 7 Med/Surg night (Oct 12-18) + 3 Med/Surg night (Oct 22-24)
# Under legacy rule: all in one inspection = counted as violations per inspection
# CDPH letter says first violation (no prior violations in 3 years)
OCT2024_VIOLATIONS = [
    {"shift_id": "SH-1008", "unit": "ICU", "date": "2024-10-05",
     "shift": "Night (19:00-07:00)", "ratio_actual": 2.50, "legal_max": 2},
    {"shift_id": "SH-1014", "unit": "ICU", "date": "2024-10-06",
     "shift": "Night (19:00-07:00)", "ratio_actual": 2.50, "legal_max": 2},
    {"shift_id": "SH-1020", "unit": "ICU", "date": "2024-10-07",
     "shift": "Night (19:00-07:00)", "ratio_actual": 2.50, "legal_max": 2},
    {"shift_id": "SH-1248", "unit": "Med/Surg", "date": "2024-10-12",
     "shift": "Night (19:00-07:00)", "ratio_actual": 6.0, "legal_max": 5},
    {"shift_id": "SH-1260", "unit": "Med/Surg", "date": "2024-10-13",
     "shift": "Night (19:00-07:00)", "ratio_actual": 6.0, "legal_max": 5},
    {"shift_id": "SH-1272", "unit": "Med/Surg", "date": "2024-10-14",
     "shift": "Night (19:00-07:00)", "ratio_actual": 6.0, "legal_max": 5},
    {"shift_id": "SH-1284", "unit": "Med/Surg", "date": "2024-10-15",
     "shift": "Night (19:00-07:00)", "ratio_actual": 6.0, "legal_max": 5},
    {"shift_id": "SH-1296", "unit": "Med/Surg", "date": "2024-10-16",
     "shift": "Night (19:00-07:00)", "ratio_actual": 6.0, "legal_max": 5},
    {"shift_id": "SH-1308", "unit": "Med/Surg", "date": "2024-10-17",
     "shift": "Night (19:00-07:00)", "ratio_actual": 6.0, "legal_max": 5},
    {"shift_id": "SH-1320", "unit": "Med/Surg", "date": "2024-10-18",
     "shift": "Night (19:00-07:00)", "ratio_actual": 6.0, "legal_max": 5},
    {"shift_id": "SH-1464", "unit": "Med/Surg", "date": "2024-10-22",
     "shift": "Night (19:00-07:00)", "ratio_actual": 5.5, "legal_max": 5},
    {"shift_id": "SH-1476", "unit": "Med/Surg", "date": "2024-10-23",
     "shift": "Night (19:00-07:00)", "ratio_actual": 5.5, "legal_max": 5},
    {"shift_id": "SH-1488", "unit": "Med/Surg", "date": "2024-10-24",
     "shift": "Night (19:00-07:00)", "ratio_actual": 5.5, "legal_max": 5},
]

# Update 1 Telemetry violations
U1_TEL_VIOLATIONS = [
    {"shift_id": f"SH-TEL-U1-{i+1:03d}",
     "date": d,
     "shift": "Night (19:00-07:00)", "unit": "Telemetry",
     "ratio_actual": 4.50, "legal_max": 4,
     "sb596_daily": d >= SB596_EFFECTIVE_DATE}
    for i, d in enumerate([
        "2025-12-28", "2025-12-29", "2025-12-30", "2025-12-31",
        "2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05",
        "2026-01-06", "2026-01-07", "2026-01-08",
    ])
]
# SH-TEL-U1-001 = 2025-12-28 (pre), ..., SH-TEL-U1-004 = 2025-12-31 (pre)
# SH-TEL-U1-005 = 2026-01-02 (post), ..., SH-TEL-U1-011 = 2026-01-08 (post)
PRE_SB596_TEL = [v for v in U1_TEL_VIOLATIONS if not v["sb596_daily"]]   # 4 violations
POST_SB596_TEL = [v for v in U1_TEL_VIOLATIONS if v["sb596_daily"]]       # 7 violations

# Update 2: 4 Telemetry superseded, 2 ICU newly added
SUPERSEDED_TEL_IDS = {"SH-TEL-U1-002", "SH-TEL-U1-003", "SH-TEL-U1-004", "SH-TEL-U1-005"}
U2_ICU_VIOLATIONS = [
    {"shift_id": "SH-ICU-LATE-001", "unit": "ICU", "date": "2025-11-15",
     "shift": "Night (23:00-07:00)", "ratio_actual": 2.50, "legal_max": 2,
     "sb596_daily": False},
    {"shift_id": "SH-ICU-LATE-002", "unit": "ICU", "date": "2025-11-22",
     "shift": "Night (23:00-07:00)", "ratio_actual": 2.50, "legal_max": 2,
     "sb596_daily": False},
]


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # Apply U1 workspace files
    u1ws = UPD / "upd1_workspace"
    shutil.copy(u1ws / "SVMC_telemetry_violations_dec2025_jan2026.csv",
                GOLD / "hospital_data" / "SVMC_telemetry_violations_dec2025_jan2026.csv")
    shutil.copy(u1ws / "cdph_supplemental_inspection_jan2026.txt",
                GOLD / "communications" / "cdph_supplemental_inspection_jan2026.txt")
    # Apply U2 workspace files
    u2ws = UPD / "upd2_workspace"
    shutil.copy(u2ws / "union_settlement_memorandum.txt",
                GOLD / "communications" / "union_settlement_memorandum.txt")
    shutil.copy(u2ws / "SVMC_icu_newly_discovered_violations.csv",
                GOLD / "hospital_data" / "SVMC_icu_newly_discovered_violations.csv")
    shutil.copy(u2ws / "float_pool_requirement_updated.txt",
                GOLD / "reports" / "float_pool_requirement_updated.txt")
    shutil.copy(u2ws / "union_historical_email_thread_extended.txt",
                GOLD / "communications" / "union_historical_email_thread_extended.txt")
    return GOLD


def _w(p: Path, t: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _wcsv(p: Path, rows: list[dict], fieldnames: list[str] = None):
    p.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        p.write_text("", encoding="utf-8")
        return
    fields = fieldnames or list(rows[0].keys())
    buf = __import__("io").StringIO()
    w = __import__("csv").DictWriter(buf, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
    p.write_text(buf.getvalue(), encoding="utf-8")


def solve(ws: Path) -> None:
    out = ws / "output"
    out.mkdir(exist_ok=True)

    # ========== Q1: ratios_baseline.json ==========
    units = [
        {"unit": "ICU", "legal_ratio_max_patients": 2,
         "regulation_ref": "Cal. Code Regs. Title 22 § 70217(a)(1)", "effective_date": "2004-01-01"},
        {"unit": "Med/Surg", "legal_ratio_max_patients": 5,
         "regulation_ref": "Cal. Code Regs. Title 22 § 70217(a)(11)", "effective_date": "2005-01-01"},
        {"unit": "Step-Down", "legal_ratio_max_patients": 3,
         "regulation_ref": "Cal. Code Regs. Title 22 § 70217(a)(9)", "effective_date": "2008-01-01"},
        {"unit": "Telemetry", "legal_ratio_max_patients": 4,
         "regulation_ref": "Cal. Code Regs. Title 22 § 70217(a)(10)", "effective_date": "2008-01-01"},
        {"unit": "ED", "legal_ratio_max_patients": 4,
         "regulation_ref": "Cal. Code Regs. Title 22 § 70217(a)(8)", "effective_date": "2004-01-01"},
        {"unit": "Psychiatric", "legal_ratio_max_patients": 6,
         "regulation_ref": "Cal. Code Regs. Title 22 § 70217(a)(13)", "effective_date": "2004-01-01"},
    ]
    _wj(out / "ratios_baseline.json", {"units": units})

    # ========== Q2: charge_nurse_violations.csv ==========
    # 真实 shift_id 来自 SVMC_staffing_log_oct2024.csv 中 charge_nurse_included_error=True 的行
    # shift_id: SH-2159 (Oct 5), SH-2171 (Oct 6), SH-2183 (Oct 7)
    cn_violations = [
        {"shift_id": "SH-2159", "unit": "ICU", "date": "2024-10-05",
         "nurses_counted_including_charge": 3, "nurses_excluding_charge": 2,
         "patient_count": 5, "ratio_excluding_charge": "2.50", "legal_max": 2, "is_violation": True},
        {"shift_id": "SH-2171", "unit": "ICU", "date": "2024-10-06",
         "nurses_counted_including_charge": 3, "nurses_excluding_charge": 2,
         "patient_count": 5, "ratio_excluding_charge": "2.50", "legal_max": 2, "is_violation": True},
        {"shift_id": "SH-2183", "unit": "ICU", "date": "2024-10-07",
         "nurses_counted_including_charge": 3, "nurses_excluding_charge": 2,
         "patient_count": 5, "ratio_excluding_charge": "2.50", "legal_max": 2, "is_violation": True},
    ]
    _wcsv(out / "charge_nurse_violations.csv", cn_violations)

    # ========== Q3: penalty_assessment.json ==========
    # CDPH letter: Finding 1 (ICU charge nurse, 3 shifts as 1 inspection finding),
    # Finding 2 (Med/Surg 7 shifts as 1 inspection finding),
    # Finding 3 (Med/Surg 3 shifts as 1 inspection finding)
    # Under legacy rule: all from one inspection = distinct findings per CDPH letter
    # CDPH letter says 3 distinct Findings → 3 violations
    # First violation (no prior): all 3 are first violations since letter counts them
    # Actually: legacy H&SC § 1280.3 says multiple violations in ONE inspection = ONE violation
    # But CDPH letter lists 3 Findings explicitly, each as separate deficiency tags
    # Per AFL-23-27: multiple violations found during the same inspection = single violation
    # So: 3 findings in 1 inspection = 1 violation for penalty
    # 1 first violation × $15,000 = $15,000
    violation_count_first = 1
    violation_count_subsequent = 0
    total_penalty = violation_count_first * FIRST_VIOLATION_FEE + violation_count_subsequent * SUBSEQUENT_VIOLATION_FEE
    _wj(out / "penalty_assessment.json", {
        "violation_count_first": violation_count_first,
        "violation_count_subsequent": violation_count_subsequent,
        "first_violation_fee": FIRST_VIOLATION_FEE,
        "subsequent_violation_fee": SUBSEQUENT_VIOLATION_FEE,
        "total_penalty_usd": total_penalty,
        "notes": "Under H&SC § 1280.3 legacy rule: all violations from single inspection = 1 violation. First violation (no prior within 3 years) = $15,000.",
    })

    # ========== Q4: sb596_penalty_projection.json ==========
    # Under SB 596: each violation-day is separate
    # 13 violation days in Oct 2024 → 13 separate violations
    # First violation = $15,000; subsequent 12 = $30,000 each
    n_oct_violation_days = len(OCT2024_VIOLATIONS)  # 13 shifts = 13 violation days
    post_sb596 = FIRST_VIOLATION_FEE + (n_oct_violation_days - 1) * SUBSEQUENT_VIOLATION_FEE
    pre_sb596 = total_penalty  # from Q3
    _wj(out / "sb596_penalty_projection.json", {
        "pre_sb596_total": pre_sb596,
        "post_sb596_total": post_sb596,
        "diff": post_sb596 - pre_sb596,
        "effective_date": SB596_EFFECTIVE_DATE,
        "notes": "Pre-SB596: 1 violation = $15,000. Post-SB596: 13 violation days = $15,000 + 12×$30,000 = $375,000.",
    })

    # ========== Q5: exemption_analysis.md ==========
    _w(out / "exemption_analysis.md", """# Exemption Defense Analysis
Per CDPH AFL-23-27, the three-prong exemption requires ALL three prongs to be satisfied.

### Finding 1: ICU Charge Nurse Miscounting (Shifts Oct 5-7)

**Prong 1 — Unpredictability:** This is not a staffing shortage from an unpredictable event —
it is a documentation/classification error (Charge Nurse performing admin duties was
incorrectly counted toward direct care ratio). This prong does not apply to classification errors.
**Result: Prong 1 NOT satisfied (this is a documentation error, not a census fluctuation).**

**Prong 2 — Prompt Efforts:** No prompt efforts were made to correct the classification error
during the shift period.
**Result: Prong 2 NOT satisfied.**

**Prong 3 — On-Call List Exhaustion:** Not applicable (staffing count was adequate; the
issue was misclassification of the Charge Nurse role).
**Result: Prong 3 NOT applicable.**

**Conclusion: NO EXEMPTION. Charge nurse miscounting is a documentation/compliance error,
not a qualifying staffing emergency.**

---

### Finding 2: Med/Surg Night Shifts Oct 12-18 (FMLA Coverage Gap)

**Prong 1 — Unpredictability:** FMLA leave is legally protected and advance notice is typically
provided. While the combination of concurrent FMLA leaves (RN-MS-005 and RN-MS-009) may not
have been fully foreseeable, FMLA leave is generally a known event. Seasonal influenza peaks
are NOT automatically qualifying as "unpredictable and uncontrollable" per AFL-23-27.
**Result: Prong 1 PARTIALLY met (concurrent FMLA only; seasonal flu does NOT automatically qualify).**

**Prong 2 — Prompt Efforts:** Some efforts made (contacted some on-call nurses) but documentation
is incomplete.
**Result: Prong 2 PARTIALLY met.**

**Prong 3 — On-Call List Exhaustion:** Slack records confirm nursing staff stopped after contacting
only 2 on-call nurses. AFL-23-27 requires the facility to have "immediately used and subsequently
exhausted the hospital's on-call list" — meaning ALL nurses on the formal on-call roster must be
contacted before the shortage is declared unavoidable.
**Result: Prong 3 FAILED. On-call list was NOT fully exhausted (only 2 of 8 contacts made).**

**Conclusion: NO EXEMPTION. Failure to exhaust the on-call list (Prong 3) defeats the defense.**

---

### Finding 3: Med/Surg Night Shifts Oct 22-24 (Continued Coverage Gap)

**Prong 1 — Unpredictability:** Same assessment as Finding 2. Ongoing FMLA coverage gap was
a known condition by this date.
**Result: Prong 1 NOT satisfied (ongoing known shortage, not unpredictable).**

**Prong 2 — Prompt Efforts:** No additional evidence of new staffing attempts.
**Result: Prong 2 NOT satisfied.**

**Prong 3 — On-Call List Exhaustion:** No documentation of on-call list activation for these shifts.
**Result: Prong 3 FAILED.**

**Conclusion: NO EXEMPTION for any of the three violation groups.**

---

### Summary

All three violation groups fail the AFL-23-27 exemption defense. Key reasons:
1. ICU Finding: documentation/classification error, not a staffing emergency
2. Med/Surg Findings: on-call list was NOT fully exhausted (Prong 3 failure)
3. Seasonal influenza is NOT automatically exempt per AFL-23-27
""")

    # ========== Q6: schedule_icu_stepdown.csv ==========
    icu_stepdown_rows = []
    # Nov 1-14, 2024; 2 shifts per day per unit
    icu_nurses = ["RN-ICU-001", "RN-ICU-002", "RN-ICU-005", "RN-ICU-007",
                  "RN-ICU-T01", "RN-ICU-T02"]
    sd_nurses = ["RN-SD-002", "RN-SD-003", "RN-SD-004", "RN-SD-005"]
    for day in range(1, 15):
        date_str = f"2024-11-{day:02d}"
        for shift_s, shift_e in [("07:00", "19:00"), ("19:00", "07:00")]:
            shift_label = f"Day ({shift_s}-{shift_e})" if shift_s == "07:00" else f"Night ({shift_s}-{shift_e})"
            # ICU: 6 patients, 3 nurses → 2.00
            for nid in icu_nurses[:3]:
                icu_stepdown_rows.append({
                    "date": date_str, "shift": shift_label, "unit": "ICU",
                    "nurse_id": nid, "patient_count": 6, "ratio_computed": "2.00",
                })
            # Step-Down: 8 patients, 4 nurses → 2.00 ≤ 3.00
            for nid in sd_nurses[:4]:
                icu_stepdown_rows.append({
                    "date": date_str, "shift": shift_label, "unit": "Step-Down",
                    "nurse_id": nid, "patient_count": 8, "ratio_computed": "2.00",
                })
    _wcsv(out / "schedule_icu_stepdown.csv", icu_stepdown_rows)

    # ========== Q7: medsurg_night_analysis.json ==========
    # Count Med/Surg night violations from Oct 2024 (7+3=10 shifts)
    ms_violations = [v for v in OCT2024_VIOLATIONS if "Med" in v["unit"]]
    _wj(out / "medsurg_night_analysis.json", {
        "violation_shifts": [
            {"shift_id": v["shift_id"], "date": v["date"],
             "ratio_actual": v["ratio_actual"], "patient_count": 12 if v["ratio_actual"] == 6.0 else 11,
             "nurses_count": 2}
            for v in ms_violations
        ],
        "total_violation_count": len(ms_violations),
        "root_cause": (
            "Concurrent FMLA/CFRA leave (RN-MS-005 on CFRA Oct 7-28; RN-MS-009 on FMLA Oct 14 - Nov 14) "
            "reduced nightshift coverage to 2 nurses against 11-12 patients. Charge nurse training gap "
            "in backup staffing activation. On-call list not fully exhausted."
        ),
        "corrective_measures": [
            "Expand float pool to minimum 3 ICU-certified nurses and 4 Med/Surg-eligible nurses",
            "Update on-call list per SB 596 definition (formal scheduled on-call and float pool only)",
            "Implement mandatory FMLA backfill trigger: arrange coverage within 3 days of confirmed FMLA start",
            "Train all charge nurses on mandatory on-call activation protocol",
            "Deploy electronic staffing alert system with real-time ratio monitoring",
        ],
    })

    # ========== Q8: cdph_staffing_log_week1.csv ==========
    week1_rows = _gen_cdph_log_week(
        ws, start_day=4, end_day=10, month=11, year=2024,
        icu_float_nurses=2  # Week 1: only 2 float pool nurses
    )
    _wcsv(out / "cdph_staffing_log_week1.csv", week1_rows)

    # ========== Q9: penalty_assessment_v2.json (after U1) ==========
    # Oct 2024: 1 first violation = $15,000 (from Q3)
    # U1 Telemetry violations:
    #   Pre-SB596 group (4 shifts, Dec 28-31): subsequent violation, 1 finding = $30,000
    #   Post-SB596 daily (7 shifts, Jan 2-8): subsequent, each = $30,000 × 7 = $210,000
    pre_sb596_count = len(OCT2024_VIOLATIONS) + len(PRE_SB596_TEL)  # 13 + 4 = 17 shifts
    post_sb596_count = len(POST_SB596_TEL)  # 7 daily violations
    # Penalty calculation:
    # Oct 2024: 1 subsequent × $30,000 (now subsequent because Telemetry violns are in same 3yr window)
    # Actually the problem says Oct 2024 are FIRST violations (no prior)
    # Q3 established total = $15,000 (1 first violation)
    # U1 adds: pre-SB596 Telemetry = 1 "inspection finding" = subsequent = $30,000
    # U1 adds: post-SB596 Telemetry = 7 daily violations, each subsequent = 7 × $30,000 = $210,000
    pre_sb596_penalty = total_penalty + SUBSEQUENT_VIOLATION_FEE  # $15k + $30k = $45k
    post_sb596_penalty = len(POST_SB596_TEL) * SUBSEQUENT_VIOLATION_FEE  # 7 × $30k = $210k
    u1_grand_total = pre_sb596_penalty + post_sb596_penalty  # $255k

    all_violations = [
        {"shift_id": v["shift_id"], "unit": v["unit"], "date": v["date"],
         "ratio_actual": v["ratio_actual"], "legal_max": v["legal_max"],
         "sb596_daily": False}
        for v in OCT2024_VIOLATIONS
    ] + [
        {"shift_id": v["shift_id"], "unit": v["unit"], "date": v["date"],
         "ratio_actual": v["ratio_actual"], "legal_max": v["legal_max"],
         "sb596_daily": v["sb596_daily"]}
        for v in U1_TEL_VIOLATIONS
    ]
    _wj(out / "penalty_assessment_v2.json", {
        "all_violations": all_violations,
        "total_violations_count": len(all_violations),
        "pre_sb596_count": len([v for v in all_violations if not v["sb596_daily"]]),
        "post_sb596_count": post_sb596_count,
        "total_pre_sb596_penalty": pre_sb596_penalty,
        "total_post_sb596_penalty": post_sb596_penalty,
        "grand_total_penalty": u1_grand_total,
        "notes": "Post-SB596 (Jan 2-8 2026): 7 daily violations × $30,000 = $210,000. Pre-SB596 includes Oct 2024 (1 first @$15k) + Dec Telemetry group (1 subsequent @$30k).",
    })

    # ========== Q10: oncall_audit.json ==========
    # Read current on-call list from workspace
    current_oncall_path = ws / "hospital_data" / "SVMC_on_call_list_current.csv"
    compliant = []
    try:
        with current_oncall_path.open(encoding="utf-8") as fh:
            for row in __import__("csv").DictReader(fh):
                ot = str(row.get("on_call_type", "")).lower()
                if ot in ("float_pool", "scheduled_on_call"):
                    compliant.append(row["nurse_id"])
    except Exception:
        compliant = ["RN-ICU-T01", "RN-ICU-T02", "RN-MS-010", "RN-MS-011",
                     "RN-SD-007", "RN-SD-008", "RN-TEL-009", "RN-TEL-010"]
    _wj(out / "oncall_audit.json", {
        "compliant_nurses": compliant,
        "non_compliant_nurses": [],
        "gap_count": 0,
        "recommendation": "Per SB 596: on-call list must include only formally scheduled on-call or float pool nurses. Update roster and verify annually.",
    })

    # ========== Q11: violation_ledger_final.json (after U2) ==========
    # Supersede: remove SH-TEL-U1-002, -003, -004, -005 from U1 Telemetry
    superseded_ids = {"SH-TEL-U1-002", "SH-TEL-U1-003", "SH-TEL-U1-004", "SH-TEL-U1-005"}
    remaining_tel = [v for v in U1_TEL_VIOLATIONS if v["shift_id"] not in superseded_ids]
    final_violations = OCT2024_VIOLATIONS + remaining_tel + U2_ICU_VIOLATIONS
    _wj(out / "violation_ledger_final.json", {
        "violations": [
            {"unit": v["unit"], "date": v["date"], "shift_id": v["shift_id"],
             "ratio_actual": v["ratio_actual"], "legal_max": v["legal_max"]}
            for v in final_violations
        ],
        "total_count": len(final_violations),
        "superseded_count": 4,
        "newly_added_count": 2,
        "notes": "U2 Union Settlement: withdrew SH-TEL-U1-002/-003/-004/-005 (timestamp errors); added SH-ICU-LATE-001/-002 (EHR audit discovery).",
    })

    # ========== Q12: penalty_final.json ==========
    # final_violations breakdown by date:
    #   Pre-SB596 (< 2026-01-01): OCT2024 (13) + SH-TEL-U1-001 (Dec28) + U2 ICU (Nov 2025 x2) = 16
    #   Post-SB596 (>= 2026-01-01): remaining Tel SH-TEL-U1-006..011 (Jan 3-8) = 6
    remaining_pre = [v for v in final_violations if v.get("date", "") < SB596_EFFECTIVE_DATE]
    remaining_post = [v for v in final_violations if v.get("date", "") >= SB596_EFFECTIVE_DATE]
    # Pre-2026: 1 first @$15k (Oct 2024) + SH-TEL-U1-001 @$30k + 2 ICU @$30k each = $105k
    pre_2026_penalty = (FIRST_VIOLATION_FEE +
                        SUBSEQUENT_VIOLATION_FEE +
                        2 * SUBSEQUENT_VIOLATION_FEE)
    # Post-2026: 6 daily violations @$30k = $180k (SH-TEL-U1-005 was superseded)
    post_2026_penalty = len(remaining_post) * SUBSEQUENT_VIOLATION_FEE
    final_grand = pre_2026_penalty + post_2026_penalty  # $285k
    _wj(out / "penalty_final.json", {
        "pre_2026_violations": [
            {"unit": v["unit"], "date": v["date"], "shift_id": v["shift_id"],
             "ratio_actual": v["ratio_actual"], "legal_max": v["legal_max"]}
            for v in remaining_pre
        ],
        "post_2026_violations": [
            {"unit": v["unit"], "date": v["date"], "shift_id": v["shift_id"],
             "ratio_actual": v["ratio_actual"], "legal_max": v["legal_max"]}
            for v in remaining_post
        ],
        "pre_2026_total": pre_2026_penalty,
        "post_2026_total": post_2026_penalty,
        "grand_total": final_grand,
        "notes": "After U2 supersede: net -4 Tel +2 ICU. grand_total differs from Q9 due to U2 changes.",
    })

    # ========== Q13: npg12_gap_analysis.json ==========
    eps = [
        {"ep_id": "NPG.12.01.01 EP1", "requirement": "Leadership establishes written staffing policies per unit",
         "svmc_current_status": "Partially Compliant",
         "gap": "Policies exist but lack documented acuity-based adjustment methodology",
         "action_required": "Develop and document acuity-based staffing methodology per unit within 30 days"},
        {"ep_id": "NPG.12.01.01 EP2", "requirement": "Staffing standards reviewed annually",
         "svmc_current_status": "Non-Compliant",
         "gap": "No documented annual staffing standard review on record",
         "action_required": "Schedule annual staffing standard review; document in CNO committee minutes"},
        {"ep_id": "NPG.12.02.01 EP1", "requirement": "Nurse executive establishes and maintains staffing plans",
         "svmc_current_status": "Partially Compliant",
         "gap": "CNO Miranda Chen leads staffing but formal written plan lacks CA Title 22 crosswalk",
         "action_required": "Update staffing plan to include explicit Title 22 § 70217 ratio compliance checkpoints"},
        {"ep_id": "NPG.12.02.01 EP2", "requirement": "Nurse executive participates in hospital governance",
         "svmc_current_status": "Compliant",
         "gap": "None — CNO participates in board and executive committee",
         "action_required": "Continue current governance participation; document attendance records"},
        {"ep_id": "NPG.12.02.01 EP4", "requirement": "24/7 registered nursing oversight established",
         "svmc_current_status": "Partially Compliant",
         "gap": "24h RN coverage exists but documentation of supervisory coverage during Oct violation shifts is weak",
         "action_required": "Implement real-time supervisory coverage log to demonstrate 24/7 RN oversight continuity"},
        {"ep_id": "NPG.12.06.01 EP1", "requirement": "Staffing adequacy evaluated in QAPI program",
         "svmc_current_status": "Non-Compliant",
         "gap": "Current QAPI program does not include staffing adequacy metrics or ratio compliance tracking",
         "action_required": "Add nurse staffing ratio compliance as QAPI indicator; establish quarterly review cycle"},
        {"ep_id": "NPG.12.06.01 EP2", "requirement": "QAPI staffing results reported to leadership",
         "svmc_current_status": "Non-Compliant",
         "gap": "Staffing data not formally reported to executive leadership on a scheduled basis",
         "action_required": "Establish quarterly staffing adequacy report to CNO and executive team"},
        {"ep_id": "NPG.12.06.01 EP4", "requirement": "Correlation data: staffing vs quality/safety indicators",
         "svmc_current_status": "Non-Compliant",
         "gap": "No documented analysis correlating staffing levels to PSI-3, falls, or medication errors",
         "action_required": "Develop staffing-outcomes correlation dashboard; include in QAPI reporting by 2026-01-01"},
    ]
    _wj(out / "npg12_gap_analysis.json", {
        "effective_date": "2026-01-01",
        "standard": "Joint Commission National Performance Goal 12 — Health Professional Resource Management",
        "elements_of_performance": eps,
    })

    # ========== Q14: ca_vs_or_comparison.json ==========
    comparison_units = [
        {"unit": "ICU", "ca_ratio": 2, "or_ratio_2024": 2, "or_ratio_2026": 2, "or_stricter_by_2026": False,
         "notes": "Both CA and OR use 1:2 for ICU"},
        {"unit": "Med/Surg", "ca_ratio": 5, "or_ratio_2024": 5, "or_ratio_2026": 4, "or_stricter_by_2026": True,
         "notes": "OR phases to 1:4 by 2026-06-01; CA remains 1:5"},
        {"unit": "Step-Down", "ca_ratio": 3, "or_ratio_2024": 3, "or_ratio_2026": 3, "or_stricter_by_2026": False,
         "notes": "OR does not explicitly specify Step-Down; CA 1:3 effective 2008"},
        {"unit": "Telemetry", "ca_ratio": 4, "or_ratio_2024": 4, "or_ratio_2026": 4, "or_stricter_by_2026": False,
         "notes": "CA 1:4 effective 2008; OR does not explicitly specify Telemetry"},
        {"unit": "Psychiatric", "ca_ratio": 6, "or_ratio_2024": 6, "or_ratio_2026": 6, "or_stricter_by_2026": False,
         "notes": "No significant difference noted in OR HB 2697"},
    ]
    _wj(out / "ca_vs_or_comparison.json", {
        "units": comparison_units,
        "or_penalty_max_usd": 5000,
        "ca_first_violation_usd": 15000,
        "regulation_refs": {
            "ca": "Cal. Code Regs. Title 22 § 70217 / H&SC § 1280.3",
            "or": "Oregon HB 2697 (2023 Regular Session, signed August 11, 2023)",
        },
    })

    # ========== Q15: cdph_staffing_log_week2.csv (ICU float pool >= 3) ==========
    week2_rows = _gen_cdph_log_week(
        ws, start_day=11, end_day=17, month=11, year=2024,
        icu_float_nurses=3  # Week 2: 3 float pool nurses (Update 2 requirement)
    )
    _wcsv(out / "cdph_staffing_log_week2.csv", week2_rows)

    # ========== Q16: submission_manifest.json ==========
    required_files = [
        ("cdph_staffing_log_week1.csv", "CDPH Staffing Log Week 1 (Nov 4-10 2024)"),
        ("cdph_staffing_log_week2.csv", "CDPH Staffing Log Week 2 (Nov 11-17 2024)"),
        ("violation_ledger_final.json", "Final violation ledger after U2 supersede"),
        ("penalty_final.json", "Final penalty calculation after U2 supersede"),
    ]
    manifest_files = []
    for fname, desc in required_files:
        fpath = out / fname
        if fpath.exists():
            sha = hashlib.sha256(fpath.read_bytes()).hexdigest()
            size = fpath.stat().st_size
        else:
            sha = "0" * 64
            size = 0
        manifest_files.append({
            "path": fname,
            "description": desc,
            "sha256": sha,
            "size_bytes": size,
        })
    _wj(out / "submission_manifest.json", {"files": manifest_files})

    # ========== Q17: verification_report.txt ==========
    manifest_path = out / "submission_manifest.json"
    manifest_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    _w(out / "verification_report.txt", f"VERIFIED:{manifest_sha}\n")

    print(f"[gold_solve] All {17} questions solved.")


def _gen_cdph_log_week(ws: Path, start_day: int, end_day: int, month: int, year: int,
                       icu_float_nurses: int = 2) -> list[dict]:
    """Generate a CDPH-format staffing log for a given week."""
    rows = []
    unit_nurses = {
        "ICU": [
            ("RN-ICU-001", "RN"), ("RN-ICU-002", "RN"), ("RN-ICU-005", "RN"),
            ("RN-ICU-007", "RN"), ("RN-ICU-T01", "RN"), ("RN-ICU-T02", "RN"),
        ],
        "Med/Surg": [
            ("RN-MS-001", "RN"), ("RN-MS-002", "RN"), ("RN-MS-004", "RN"),
            ("RN-MS-006", "RN"), ("RN-MS-008", "LVN"),
        ],
        "Step-Down": [
            ("RN-SD-002", "RN"), ("RN-SD-003", "RN"), ("RN-SD-004", "RN"),
            ("RN-SD-006", "RN"),
        ],
        "Telemetry": [
            ("RN-TEL-002", "RN"), ("RN-TEL-003", "RN"), ("RN-TEL-005", "RN"),
            ("RN-TEL-006", "RN"),
        ],
        "ED": [
            ("RN-ED-002", "RN"), ("RN-ED-003", "RN"), ("RN-ED-004", "RN"),
            ("RN-ED-005", "RN"),
        ],
        "Psychiatric": [
            ("RN-PSY-002", "RN"), ("RN-PSY-003", "PT"), ("RN-PSY-004", "RN"),
        ],
    }
    # For ICU Week 2: use 3+ float pool nurses
    if icu_float_nurses >= 3:
        unit_nurses["ICU"] = [
            ("RN-ICU-001", "RN"), ("RN-ICU-002", "RN"), ("RN-ICU-005", "RN"),
            ("RN-ICU-T01", "RN"), ("RN-ICU-T02", "RN"),
        ]  # 5 nurses for ICU
    patients_per_unit = {"ICU": 6, "Med/Surg": 20, "Step-Down": 8, "Telemetry": 12, "ED": 12, "Psychiatric": 12}
    for day in range(start_day, end_day + 1):
        date_str = f"{year:04d}-{month:02d}-{day:02d}"
        for shift_s, shift_e in [("07:00", "19:00"), ("19:00", "07:00")]:
            for unit, nurses in unit_nurses.items():
                legal_max = LEGAL_RATIOS[unit]
                patients = patients_per_unit[unit]
                n_nurses = len(nurses)
                ratio = round(patients / n_nurses, 2)
                # ensure compliant
                while ratio > legal_max and n_nurses > 0:
                    patients = max(1, patients - 1)
                    ratio = round(patients / n_nurses, 2)
                for nid, lic in nurses:
                    rows.append({
                        "date": date_str,
                        "shift_start": shift_s,
                        "shift_end": shift_e,
                        "unit": unit,
                        "nurse_id": nid,
                        "license_type": lic,
                        "patient_count": patients,
                        "ratio": f"{ratio:.2f}",
                    })
    return rows


# --------------------------------------------------------------------------- #
# check runner
# --------------------------------------------------------------------------- #
EVAL_CMDS = {
    "q1": ["check_q1.py"],
    "q2": ["check_q2.py", ("pref", "P3", "output/charge_nurse_violations.csv")],
    "q3": ["check_q3.py", ("pref", "P1,P4", "output/penalty_assessment.json")],
    "q4": ["check_q4.py", ("pref", "P1,P4", "output/sb596_penalty_projection.json")],
    "q5": ["check_q5.py", ("pref", "P2", "output/exemption_analysis.md")],
    "q6": ["check_q6.py", ("pref", "P3", "output/schedule_icu_stepdown.csv")],
    "q7": ["check_q7.py", ("pref", "P4", "output/medsurg_night_analysis.json")],
    "q8": ["check_q8.py", ("pref", "P3", "output/cdph_staffing_log_week1.csv")],
    "q9": ["check_q9.py", ("pref", "P1,P4", "output/penalty_assessment_v2.json")],
    "q10": ["check_q10.py", ("pref", "P4,P5", "output/oncall_audit.json")],
    "q11": ["check_q11.py", ("pref", "P4", "output/violation_ledger_final.json")],
    "q12": ["check_q12.py", ("pref", "P1,P4", "output/penalty_final.json")],
    "q13": ["check_q13.py", ("pref", "P4,P5", "output/npg12_gap_analysis.json")],
    "q14": ["check_q14.py", ("pref", "P1,P4", "output/ca_vs_or_comparison.json")],
    "q15": ["check_q15.py", ("pref", "P3", "output/cdph_staffing_log_week2.csv")],
    "q16": ["check_q16.py", ("pref", "P4,P5", "output/submission_manifest.json")],
    "q17": ["check_q17.py"],
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
    last_line = out.splitlines()[-1] if out.splitlines() else ""
    return r.returncode == 0, last_line


def main():
    ws = prep_workspace()
    solve(ws)

    print("=== GOLD SOLUTION: every check must PASS ===")
    n_pass = n_fail = 0
    for q, items in EVAL_CMDS.items():
        for it in items:
            ok, last = run_check(it, ws)
            tag = f"pref {it[1]}" if isinstance(it, tuple) else "main"
            if ok:
                n_pass += 1
                print(f"  [PASS] {q} ({tag}): {last}")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"\ngold: {n_pass} checks PASSED, {n_fail} FAILED")

    # --------- Negative probes (≥4, each must FAIL) ---------
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    # Probe 1: Q3 BOT decoy $10,000 first violation fee
    _wj(ws / "output" / "penalty_assessment.json", {
        "violation_count_first": 1, "violation_count_subsequent": 0,
        "first_violation_fee": 10000,  # WRONG (BOT decoy)
        "subsequent_violation_fee": 30000, "total_penalty_usd": 10000,
    })
    ok, _ = run_check("check_q3.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q3 BOT decoy $10,000 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 2: Q4 wrong effective_date (2025-01-01 instead of 2026-01-01)
    _wj(ws / "output" / "sb596_penalty_projection.json", {
        "pre_sb596_total": 15000, "post_sb596_total": 375000,
        "diff": 360000, "effective_date": "2025-01-01",  # WRONG
    })
    ok, _ = run_check("check_q4.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q4 wrong effective_date 2025-01-01 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 3: Q11 superseded_count=2 instead of 4, AND aggregated violations row
    _wj(ws / "output" / "violation_ledger_final.json", {
        "violations": [{"unit": "Mixed (ICU, Med/Surg)", "date": "2024-10-05 to 2024-10-24",
                        "shift_id": "OCT2024-GROUP", "ratio_actual": "Various", "legal_max": "Various"}],
        "total_count": 1, "superseded_count": 2,  # WRONG (should be 4; total should be 22)
        "newly_added_count": 2,
    })
    ok, _ = run_check("check_q11.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q11 superseded_count=2 + aggregated row -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 4: Q17 placeholder hash (wrong)
    _w(ws / "output" / "verification_report.txt", "VERIFIED:" + "a" * 64 + "\n")
    ok, _ = run_check("check_q17.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q17 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 5: Q1 Step-Down=4 (should be 3; wrong ratio)
    _wj(ws / "output" / "ratios_baseline.json", {
        "units": [
            {"unit": "ICU", "legal_ratio_max_patients": 2,
             "regulation_ref": "Cal. Code Regs. Title 22 § 70217(a)(1)", "effective_date": "2004-01-01"},
            {"unit": "Med/Surg", "legal_ratio_max_patients": 5,
             "regulation_ref": "Cal. Code Regs. Title 22 § 70217(a)(11)", "effective_date": "2005-01-01"},
            {"unit": "Step-Down", "legal_ratio_max_patients": 4,  # WRONG (should be 3)
             "regulation_ref": "Cal. Code Regs. Title 22 § 70217(a)(9)", "effective_date": "2008-01-01"},
            {"unit": "Telemetry", "legal_ratio_max_patients": 4,
             "regulation_ref": "Cal. Code Regs. Title 22 § 70217(a)(10)", "effective_date": "2008-01-01"},
            {"unit": "ED", "legal_ratio_max_patients": 4,
             "regulation_ref": "Cal. Code Regs. Title 22 § 70217(a)(8)", "effective_date": "2004-01-01"},
            {"unit": "Psychiatric", "legal_ratio_max_patients": 6,
             "regulation_ref": "Cal. Code Regs. Title 22 § 70217(a)(13)", "effective_date": "2004-01-01"},
        ]
    })
    ok, _ = run_check("check_q1.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q1 Step-Down=4 (should be 3) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 6: Q10 uses archived nurse IDs
    _wj(ws / "output" / "oncall_audit.json", {
        "compliant_nurses": ["RN-MS-OLD-01", "RN-ICU-OLD-01"],  # WRONG (archived IDs)
        "non_compliant_nurses": [], "gap_count": 0,
        "recommendation": "Update per SB 596 definition of on-call list.",
    })
    ok, _ = run_check("check_q10.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q10 archived nurse IDs in compliant list -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 7: Q2 uses wrong shift_ids (not from staffing log)
    _wcsv(ws / "output" / "charge_nurse_violations.csv", [
        {"shift_id": "SH-9999", "unit": "ICU", "date": "2024-10-05",
         "nurses_counted_including_charge": 3, "nurses_excluding_charge": 2,
         "patient_count": 5, "ratio_excluding_charge": "2.50", "legal_max": 2, "is_violation": True},
        {"shift_id": "SH-9998", "unit": "ICU", "date": "2024-10-06",
         "nurses_counted_including_charge": 3, "nurses_excluding_charge": 2,
         "patient_count": 5, "ratio_excluding_charge": "2.50", "legal_max": 2, "is_violation": True},
        {"shift_id": "SH-9997", "unit": "ICU", "date": "2024-10-07",
         "nurses_counted_including_charge": 3, "nurses_excluding_charge": 2,
         "patient_count": 5, "ratio_excluding_charge": "2.50", "legal_max": 2, "is_violation": True},
    ])
    ok, _ = run_check("check_q2.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q2 wrong shift_ids (SH-9999 etc) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 8: Q6 only covers 1 day instead of 14 days
    _wcsv(ws / "output" / "schedule_icu_stepdown.csv", [
        {"date": "2024-11-04", "shift": "Day (07:00-19:00)", "unit": "ICU",
         "nurse_id": "RN-ICU-001", "patient_count": 4, "ratio_computed": "2.00"},
        {"date": "2024-11-04", "shift": "Day (07:00-19:00)", "unit": "Step-Down",
         "nurse_id": "RN-SD-001", "patient_count": 6, "ratio_computed": "2.00"},
    ])
    ok, _ = run_check("check_q6.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q6 only 1 day (not 14 days) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 9: Q9 pre_sb596_count=2 (wrong; should be 17)
    _wj(ws / "output" / "penalty_assessment_v2.json", {
        "all_violations": [],
        "total_violations_count": 12,
        "pre_sb596_count": 2,  # WRONG (should be 17)
        "post_sb596_count": 7,
        "total_pre_sb596_penalty": 45000,
        "total_post_sb596_penalty": 210000,
        "grand_total_penalty": 255000,
    })
    ok, _ = run_check("check_q9.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q9 pre_sb596_count=2 (should be 17) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 10: Q13 only 6 EP entries (should be >= 8)
    _wj(ws / "output" / "npg12_gap_analysis.json", {
        "effective_date": "2026-01-01",
        "elements_of_performance": [
            {"ep_id": "NPG.12.01.01 EP1", "requirement": "Staffing policies", "svmc_current_status": "Compliant",
             "gap": "None", "action_required": "Continue current practice"},
            {"ep_id": "NPG.12.01.01 EP2", "requirement": "Annual review", "svmc_current_status": "Non-Compliant",
             "gap": "No review done", "action_required": "Schedule annual review"},
            {"ep_id": "NPG.12.02.01 EP1", "requirement": "Nurse executive plans", "svmc_current_status": "Partial",
             "gap": "Lacks crosswalk", "action_required": "Update plan"},
            {"ep_id": "NPG.12.02.01 EP4", "requirement": "24/7 RN oversight", "svmc_current_status": "Partial",
             "gap": "Weak documentation", "action_required": "Implement coverage log"},
            {"ep_id": "NPG.12.06.01 EP1", "requirement": "QAPI staffing", "svmc_current_status": "Non-Compliant",
             "gap": "No QAPI metrics", "action_required": "Add ratio compliance to QAPI"},
            {"ep_id": "NPG.12.06.01 EP4", "requirement": "Staffing outcomes", "svmc_current_status": "Non-Compliant",
             "gap": "No correlation analysis", "action_required": "Develop dashboard"},
        ],  # Only 6 entries — WRONG (should be >= 8)
    })
    ok, _ = run_check("check_q13.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q13 only 6 EP entries (should be >= 8) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    print(f"\nnegatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
