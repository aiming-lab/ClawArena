#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_sec4.py — sec4 可解性审计（金标自检）。

在 workspace 的临时副本上模拟 update 生效后的状态，写出每一轮的「正确产物」，
然后运行全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再做一组反例（错误产物）抽样，断言 check 能 FAIL（不过松）。

用途：证明每个 ground-truth 可由真实数据解出、check 不过严也不过松。
运行：python scripts/clawarena_authoring/gold_solve_sec4.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "sec4"
UPD = DS / "openclaw" / "updates" / "sec4"
SCRIPTS = DS / "eval" / "sec4" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/sec4_gold_ws")

# Art. 30(1) controller required fields
REQUIRED_FIELDS = [
    "name_and_contact_details", "purposes", "data_subject_categories",
    "personal_data_categories", "recipient_categories", "third_country_transfers",
    "retention_periods", "security_measures"
]

# Art. 5(1) six principles (verbatim)
ART5_PRINCIPLES = [
    "lawfulness_fairness_transparency", "purpose_limitation", "data_minimisation",
    "accuracy", "storage_limitation", "integrity_and_confidentiality"
]


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # Apply update workspace files
    upd1_ws = UPD / "upd1_workspace"
    upd2_ws = UPD / "upd2_workspace"
    # upd1: hr analytics data dictionary and new feature file
    (GOLD / "company").mkdir(parents=True, exist_ok=True)
    for fname in ("hr_analytics_data_dictionary.md", "hr_analytics_new_feature.md"):
        src = upd1_ws / fname
        if src.exists():
            shutil.copy(src, GOLD / "company" / fname)
    # upd2: supervisory authority letter, legal memo, RoPA addendum
    (GOLD / "legal").mkdir(parents=True, exist_ok=True)
    for fname in ("supervisory_authority_letter_20250501.md", "legal_memo_dsar_deadline.md"):
        src = upd2_ws / fname
        if src.exists():
            shutil.copy(src, GOLD / "legal" / fname)
    src_ai = upd2_ws / "ropa_controller_ai_addendum.json"
    if src_ai.exists():
        shutil.copy(src_ai, GOLD / "ropa" / "ropa_controller_ai_addendum.json")
    return GOLD


def _nonempty(v) -> bool:
    if v is None:
        return False
    if isinstance(v, (list, dict)):
        return len(v) > 0
    if isinstance(v, str):
        return v.strip() != ""
    return True


def _w(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2), encoding="utf-8")


def solve(ws: Path) -> None:
    audit = ws / "audit"; audit.mkdir(exist_ok=True)
    dsar_dir = ws / "dsar"; dsar_dir.mkdir(exist_ok=True)
    breach_dir = ws / "breach"; breach_dir.mkdir(exist_ok=True)
    dpia_dir = ws / "dpia"; dpia_dir.mkdir(exist_ok=True)
    ropa_dir = ws / "ropa"; ropa_dir.mkdir(exist_ok=True)

    # ── Load source data ────────────────────────────────────────────────────
    ropa_v1 = json.loads((ws / "ropa" / "ropa_controller_draft_v1.json").read_text(encoding="utf-8"))
    activities_v1 = ropa_v1.get("activities", [])

    with (ws / "dsar" / "dsar_queue.csv").open(encoding="utf-8") as fh:
        dsar_rows = list(csv.DictReader(fh))

    financials = json.loads((ws / "company" / "company_financials.json").read_text(encoding="utf-8"))
    org = json.loads((ws / "company" / "org_chart.json").read_text(encoding="utf-8"))
    dpo_name = org["data_protection"]["dpo_name"]
    turnover = financials["total_worldwide_annual_turnover_eur"]

    # ── Q1: Gap analysis ────────────────────────────────────────────────────
    gaps = []
    for act in activities_v1:
        missing = [f for f in REQUIRED_FIELDS if not _nonempty(act.get(f))]
        if missing:
            gaps.append({"activity_id": act["activity_id"], "missing_fields": missing})
    _wj(audit / "gap_analysis_q1.json", {
        "total_activities": 30,
        "activities_with_gaps": gaps,
        "gap_count": len(gaps),
    })

    # ── Q2: Fixed RoPA ──────────────────────────────────────────────────────
    import copy
    fixed_activities = []
    for act in activities_v1:
        a = copy.deepcopy(act)
        # ACT-001: missing recipient_categories
        if not _nonempty(a.get("recipient_categories")):
            a["recipient_categories"] = ["AWS EU (processor)", "Salesforce EU (sub-processor)"]
        # ACT-002: missing security_measures
        if not _nonempty(a.get("security_measures")):
            a["security_measures"] = [
                "Encryption at rest (AES-256)", "TLS 1.2+ in transit",
                "Role-based access control", "Audit logging",
            ]
        # Ensure all other fields are non-empty (patch generically)
        if not _nonempty(a.get("retention_periods")):
            a["retention_periods"] = "As determined by applicable legal obligation"
        if not _nonempty(a.get("third_country_transfers")):
            a["third_country_transfers"] = {"transfer": False, "mechanism": None}
        fixed_activities.append(a)

    ropa_fixed = copy.deepcopy(ropa_v1)
    ropa_fixed["activities"] = fixed_activities
    _wj(ropa_dir / "ropa_controller_fixed.json", ropa_fixed)

    # ── Q3: Art.5 compliance map ─────────────────────────────────────────────
    art5_activities = []
    for act in activities_v1:
        principles = {}
        for p in ART5_PRINCIPLES:
            if p == "storage_limitation":
                rp = act.get("retention_periods")
                status = "MISSING" if not _nonempty(rp) else ("PARTIAL" if "indefinite" in str(rp).lower() else "COMPLIANT")
                note = "Retention period defined per Art. 5(1)(e)" if status == "COMPLIANT" else "Retention period missing or indefinite — review required"
            elif p == "integrity_and_confidentiality":
                sm = act.get("security_measures")
                # Exact derivation: MISSING if security_measures absent/empty (e.g. ACT-002), COMPLIANT otherwise
                status = "MISSING" if not _nonempty(sm) else "COMPLIANT"
                note = "Security measures documented per Art. 5(1)(f)" if status == "COMPLIANT" else "Security measures not documented in draft v1 — gap identified per Art. 5(1)(f)"
            elif p == "purpose_limitation":
                status = "COMPLIANT" if _nonempty(act.get("purposes")) else "MISSING"
                note = "Purposes specified per Art. 5(1)(b)"
            elif p == "lawfulness_fairness_transparency":
                status = "COMPLIANT" if _nonempty(act.get("legal_ground")) else "PARTIAL"
                note = "Legal ground documented per Art. 5(1)(a)"
            elif p == "data_minimisation":
                status = "PARTIAL"
                note = "Data categories listed; minimisation review recommended per Art. 5(1)(c)"
            else:  # accuracy
                status = "PARTIAL"
                note = "Accuracy controls assumed; formal review recommended per Art. 5(1)(d)"
            principles[p] = {"status": status, "note": note}
        art5_activities.append({"activity_id": act["activity_id"], "principles": principles})

    _wj(audit / "art5_compliance_map.json", {"activities": art5_activities})

    # ── Q4: DSAR deadlines CSV ───────────────────────────────────────────────
    ref_date = date(2025, 3, 20)
    deadline_rows = []
    for r in dsar_rows:
        rd = date.fromisoformat(r["request_date"])
        dl = rd + timedelta(days=30)
        orig_status = r["status"]
        if orig_status == "COMPLETED":
            status = "COMPLETED"
        elif dl < ref_date:
            status = "OVERDUE"
        else:
            status = orig_status
        deadline_rows.append({
            "case_id": r["case_id"],
            "request_date": r["request_date"],
            "response_deadline": dl.isoformat(),
            "status": status,
        })
    with (dsar_dir / "dsar_deadlines.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["case_id", "request_date", "response_deadline", "status"])
        w.writeheader()
        w.writerows(deadline_rows)
    dsar_overdue_count = sum(1 for r in deadline_rows if r["status"] == "OVERDUE")

    # ── Q5: REQ-042 Art.15 response ─────────────────────────────────────────
    r42 = next(r for r in dsar_rows if r["case_id"] == "REQ-042")
    dl42 = (date.fromisoformat(r42["request_date"]) + timedelta(days=30)).isoformat()
    _w(dsar_dir / "response_req_042.md", f"""# Data Subject Access Request Response

---
**case_id**: REQ-042
**request_date**: {r42['request_date']}
**response_deadline**: {dl42}
**status**: OVERDUE

---

Dear Mr. Heinrich Braun,

We are writing in response to your data subject access request received on {r42['request_date']}.

Under **Art. 15(3)** GDPR, the controller shall provide a copy of the personal data undergoing processing.
This right entitles you to receive a copy of all personal data we hold about you.

We have identified the following personal data held in our CRM system:
- Name, email address, company affiliation, and interaction history records
- All data processed in connection with your B2B account relationship

We provide this information in accordance with **Art. 15(3)** GDPR.

Yours sincerely,
VeritasCloud GmbH Data Protection Office
DPO: Lena Fischer | dpo@veritascloud.de
""")

    # ── Q6: Breach notification compliance ──────────────────────────────────
    _wj(breach_dir / "notification_compliance_q6.json", {
        "discovery_datetime_utc": "2025-03-14T09:00:00Z",
        "notification_datetime_utc": "2025-03-15T22:30:00Z",
        "hours_elapsed": 37.5,
        "threshold_hours": 72,
        "status": "COMPLIANT",
    })

    # ── Q7: Breach notification final ────────────────────────────────────────
    _wj(breach_dir / "breach_notification_final.json", {
        "notification_reference": "BayLDA-NOT-2025-0315-001",
        "notification_type": "Art. 33 GDPR Supervisory Authority Notification",
        "controller": "VeritasCloud GmbH",
        "dpo_contact": "Lena Fischer | dpo@veritascloud.de | +49 69 4433 8800",
        "DPO_contact": "Lena Fischer | dpo@veritascloud.de | +49 69 4433 8800",
        "incident_reference": "INC-2025-0314",
        "discovery_datetime_utc": "2025-03-14T09:00:00Z",
        "notification_datetime_utc": "2025-03-15T22:30:00Z",
        "hours_elapsed": 37.5,
        "nature_of_breach": "Unauthorised read access to CRM production database (EU-West-1); no confirmed exfiltration; ~54 hours of exposure between 2025-03-12 02:00Z and 2025-03-14 08:50Z",
        "categories_and_number_of_data_subjects": "B2B client contacts — approximately 15,000 individuals",
        "categories_and_number_of_records": "Approximately 45,000 records (Name, email address, phone number — 3 fields x 15,000 subjects)",
        "likely_consequences": "Low-to-medium risk of phishing or business email compromise targeting B2B contacts; no financial or special category data exposed",
        "measures_taken": "Access revoked 2025-03-14T10:30Z; affected credentials rotated; full forensic analysis completed; access control hardening initiated; all affected individuals to be notified",
    })

    # ── Q8: DPIA trigger assessment ──────────────────────────────────────────
    _wj(dpia_dir / "dpia_trigger_assessment.json", {
        "module": "hr_analytics",
        "edpb_criteria_met": [
            "Systematic monitoring of employees at large scale",
            "Processing of employee data in an employment context at scale",
        ],
        "required": True,
        "rationale": (
            "The HR Analytics module performs large-scale systematic monitoring of employees "
            "(EDPB criterion: systematic monitoring) and processes employee personal data at scale "
            "(EDPB criterion: large-scale processing). At least two of the nine EDPB criteria are met, "
            "triggering a mandatory DPIA under Art. 35 GDPR."
        ),
    })

    # ── Q9: DPIA risk matrix (after Update-1, includes special category data) ─
    risk_matrix = [
        {"risk_id": "R-001", "description": "Health_risk_score leakage — special category Art.9 data exposed", "likelihood": 3, "severity": 5, "risk_score": 15},
        {"risk_id": "R-002", "description": "Burnout_probability automated profiling without Art.22 safeguards", "likelihood": 4, "severity": 4, "risk_score": 16},
        {"risk_id": "R-003", "description": "Large-scale systematic monitoring of employees without explicit consent", "likelihood": 3, "severity": 4, "risk_score": 12},
        {"risk_id": "R-004", "description": "Retention of health-derived ML training data beyond legal basis", "likelihood": 2, "severity": 4, "risk_score": 8},
    ]
    high_risk_items = [r["risk_id"] for r in risk_matrix if r["risk_score"] >= 15]
    residual = max(r["risk_score"] for r in risk_matrix)
    _wj(dpia_dir / "dpia_hr_analytics_final.json", {
        "module": "hr_analytics",
        "risk_matrix": risk_matrix,
        "high_risk_items": high_risk_items,
        "residual_risk_score": residual,
        "dpo_consultation_required": True,
        "sa_prior_consultation_required": True,
    })

    # ── Q10: DPO appointment check ────────────────────────────────────────────
    _wj(audit / "dpo_appointment_check.json", {
        "dpo_name": dpo_name,
        "criterion_met": "Art. 37(1)(b)",
        "mandatory": "TRUE",
        "rationale": (
            "VeritasCloud GmbH has approximately 800,000 registered users and operates the HR Analytics "
            "module which performs large-scale systematic monitoring of individuals. This triggers "
            "Art. 37(1)(b) GDPR — mandatory DPO appointment. Note: the Discord memo citing '<500 employees "
            "= no DPO' applies an outdated and incorrect interpretation; Art. 37(1) sub-clauses govern."
        ),
    })

    # ── Q11: Art.83 penalty exposure ─────────────────────────────────────────
    tier1_pct = int(turnover * 0.02)
    tier1_fixed = 10_000_000
    tier1_max = max(tier1_fixed, tier1_pct)
    tier2_pct = int(turnover * 0.04)
    tier2_fixed = 20_000_000
    tier2_max = max(tier2_fixed, tier2_pct)
    _wj(audit / "penalty_exposure.json", {
        "worldwide_turnover_eur": turnover,
        "tier1_percentage_amount_eur": tier1_pct,
        "tier1_fixed_eur": tier1_fixed,
        "tier1_max_eur": tier1_max,
        "tier2_percentage_amount_eur": tier2_pct,
        "tier2_fixed_eur": tier2_fixed,
        "tier2_max_eur": tier2_max,
    })

    # ── Q12: RoPA version decision (Update-2 triggers this round) ────────────
    _wj(audit / "ropa_version_decision.json", {
        "selected_version": "v1",
        "rejected_version": "v0",
        "reason": (
            "ropa_controller_legacy_v0.json is a legacy document explicitly marked as superseded by "
            "ropa_controller_draft_v1.json. The legacy v0 contains known deficiencies (indefinite retention, "
            "missing fields) and must not be used for Art.30 submission."
        ),
        "source_file": "ropa/ropa_controller_draft_v1.json",
    })

    # ── Q13: RoPA v2 with AI addendum ────────────────────────────────────────
    ai_addendum = json.loads((ws / "ropa" / "ropa_controller_ai_addendum.json").read_text(encoding="utf-8"))
    ropa_v2 = copy.deepcopy(ropa_fixed)
    act_21 = ai_addendum["activities"][0]
    ropa_v2["activities"].append(act_21)
    ropa_v2["total_activities"] = 31
    _wj(ropa_dir / "ropa_controller_v2.json", ropa_v2)

    # ── Q14: Compliance summary ───────────────────────────────────────────────
    _wj(audit / "compliance_summary.json", {
        "total_processing_activities": 31,
        "dsar_overdue_count": dsar_overdue_count,
        "breach_notification_status": "COMPLIANT",
        "dpia_required_modules": ["hr_analytics"],
        "dpo_mandatory": "TRUE",
        "overall_status": "PARTIALLY_COMPLIANT",
    })

    # ── Q15: Penalty mapping ──────────────────────────────────────────────────
    _wj(audit / "penalty_mapping.json", {
        "gaps": [
            {
                "gap_id": "GAP-001",
                "description": "ACT-001 missing recipient_categories in Art.30 RoPA",
                "article_violated": "Art. 30(1)(d)",
                "tier": 1,
            },
            {
                "gap_id": "GAP-002",
                "description": "ACT-002 missing security_measures in Art.30 RoPA",
                "article_violated": "Art. 30(1)(g)",
                "tier": 1,
            },
            {
                "gap_id": "GAP-003",
                "description": "DSAR backlog: multiple requests past 30-day response deadline",
                "article_violated": "Art. 12(3)",
                "tier": 2,
            },
            {
                "gap_id": "GAP-004",
                "description": "HR Analytics processes special category data (Art.9) without completed DPIA",
                "article_violated": "Art. 35(1)",
                "tier": 2,
            },
            {
                "gap_id": "GAP-005",
                "description": "integrity_and_confidentiality principle not documented for some processing activities",
                "article_violated": "Art. 5(1)(f)",
                "tier": 2,
            },
            {
                "gap_id": "GAP-006",
                "description": "AI recommendation engine added to RoPA late — not in initial Art.30 register",
                "article_violated": "Art. 30(1)(b)",
                "tier": 2,
            },
            {
                "gap_id": "GAP-007",
                "description": "ACT-002 storage_limitation not fully documented — retention basis for applicant data unclear",
                "article_violated": "Art. 5(1)(e)",
                "tier": 2,
            },
        ]
    })

    # ── Q16: SHA-256 sign-off ─────────────────────────────────────────────────
    summary_bytes = (audit / "compliance_summary.json").read_bytes()
    digest = hashlib.sha256(summary_bytes).hexdigest()
    signoff_str = f"VERIFIED:{digest}"
    _wj(audit / "final_report_signoff.json", {
        "target_file": "audit/compliance_summary.json",
        "signoff": signoff_str,
    })

    # ── Q17: DSAR deadlines v2 (strict 30-day, supersede extension) ──────────
    deadline_v2_rows = []
    for r in dsar_rows:
        rd = date.fromisoformat(r["request_date"])
        dl = rd + timedelta(days=30)
        orig_status = r["status"]
        if orig_status == "COMPLETED":
            status = "COMPLETED"
        elif dl < ref_date:
            status = "OVERDUE"
        else:
            status = orig_status
        deadline_v2_rows.append({
            "case_id": r["case_id"],
            "request_date": r["request_date"],
            "response_deadline": dl.isoformat(),
            "status": status,
        })
    with (dsar_dir / "dsar_deadlines_v2.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["case_id", "request_date", "response_deadline", "status"])
        w.writeheader()
        w.writerows(deadline_v2_rows)

    # ── Q18: Final GDPR audit certificate ────────────────────────────────────
    _wj(audit / "gdpr_audit_certificate.json", {
        "audit_date": "2025-05-15",
        "company_id": "VeritasCloud GmbH",
        "dpo_name": dpo_name,
        "overall_status": "PARTIALLY_COMPLIANT",
        "article_30_compliant": "TRUE",
        "article_33_compliant": "TRUE",
        "article_37_compliant": "TRUE",
        "article_83_max_exposure_eur": tier2_max,
        "signoff": signoff_str,
    })


# ── Run checks ────────────────────────────────────────────────────────────────

# Maps each round to its check scripts + optional pref checks
EVAL_CMDS: dict[str, list] = {
    "q1": ["check_q1.py", ("pref", "P1", "audit/gap_analysis_q1.json")],
    "q2": ["check_q2.py", ("pref", "P1", "ropa/ropa_controller_fixed.json")],
    "q3": ["check_q3.py", ("pref", "P2", "audit/art5_compliance_map.json")],
    "q4": ["check_q4.py", ("pref", "P3", "dsar/dsar_deadlines.csv")],
    "q5": ["check_q5.py", ("pref", "P2,P3", "dsar/response_req_042.md")],
    "q6": ["check_q6.py", ("pref", "P1", "breach/notification_compliance_q6.json")],
    "q7": ["check_q7.py"],
    "q8": ["check_q8.py"],
    "q9": ["check_q9.py"],
    "q10": ["check_q10.py", ("pref", "P2,P4", "audit/dpo_appointment_check.json")],
    "q11": ["check_q11.py", ("pref", "P1", "audit/penalty_exposure.json")],
    "q12": ["check_q12.py"],
    "q13": ["check_q13.py", ("pref", "P1", "ropa/ropa_controller_v2.json")],
    "q14": ["check_q14.py", ("pref", "P4,P5", "audit/compliance_summary.json")],
    "q15": ["check_q15.py", ("pref", "P2", "audit/penalty_mapping.json")],
    "q16": ["check_q16.py", ("pref", "P1", "audit/final_report_signoff.json")],
    "q17": ["check_q17.py", ("pref", "P3", "dsar/dsar_deadlines_v2.csv")],
    "q18": ["check_q18.py", ("pref", "P1,P2,P4,P5", "audit/gdpr_audit_certificate.json")],
}


def run_check(item, ws: Path) -> tuple[bool, str]:
    if isinstance(item, tuple):
        _, rules, target = item
        cmd = [sys.executable, str(SCRIPTS / "check_preferences.py"),
               str(ws), "--rules", rules, "--target", target]
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
                print(f"  [PASS] {q} ({tag})")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"gold: {n_pass} checks PASSED, {n_fail} FAILED")

    # ── Negative probes: wrong products must FAIL ─────────────────────────────
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0; caught = 0

    # Probe 1: Q1 — use legacy v0 RoPA data (ACT-001 has recipient_categories in v0)
    import json as _json
    v0 = _json.loads((ws / "ropa" / "ropa_controller_legacy_v0.json").read_text())
    _wj(ws / "audit" / "gap_analysis_q1.json", {
        "total_activities": 30,
        "activities_with_gaps": [],  # legacy v0 has recipient_categories so gap missed
        "gap_count": 0,
    })
    ok, _ = run_check("check_q1.py", ws); probes += 1; caught += (not ok)
    print(f"  q1 no-gaps (missed ACT-001/ACT-002) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q1 gold
    gaps_gold = []
    activities_v1 = _json.loads((ws / "ropa" / "ropa_controller_draft_v1.json").read_text())["activities"]
    for act in activities_v1:
        missing = [f for f in REQUIRED_FIELDS if not _nonempty(act.get(f))]
        if missing:
            gaps_gold.append({"activity_id": act["activity_id"], "missing_fields": missing})
    _wj(ws / "audit" / "gap_analysis_q1.json", {
        "total_activities": 30, "activities_with_gaps": gaps_gold, "gap_count": len(gaps_gold)
    })

    # Probe 2: Q6 — wrong discovery date 2025-03-15 (Slack bot decoy)
    _wj(ws / "breach" / "notification_compliance_q6.json", {
        "discovery_datetime_utc": "2025-03-15T09:00:00Z",  # Slack bot decoy date
        "notification_datetime_utc": "2025-03-15T22:30:00Z",
        "hours_elapsed": 13.5,
        "threshold_hours": 72,
        "status": "COMPLIANT",
    })
    ok, _ = run_check("check_q6.py", ws); probes += 1; caught += (not ok)
    print(f"  q6 Slack-bot decoy date 2025-03-15 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q6 gold
    _wj(ws / "breach" / "notification_compliance_q6.json", {
        "discovery_datetime_utc": "2025-03-14T09:00:00Z",
        "notification_datetime_utc": "2025-03-15T22:30:00Z",
        "hours_elapsed": 37.5, "threshold_hours": 72, "status": "COMPLIANT",
    })

    # Probe 3: Q8 — required = false (Slack bot honey-pot)
    _wj(ws / "dpia" / "dpia_trigger_assessment.json", {
        "module": "hr_analytics",
        "edpb_criteria_met": [],
        "required": False,  # Slack bot decoy
        "rationale": "No DPIA required per Slack bot summary",
    })
    ok, _ = run_check("check_q8.py", ws); probes += 1; caught += (not ok)
    print(f"  q8 required=false (Slack bot decoy) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q8 gold
    _wj(ws / "dpia" / "dpia_trigger_assessment.json", {
        "module": "hr_analytics",
        "edpb_criteria_met": ["Systematic monitoring of employees at large scale", "Processing of employee data at scale"],
        "required": True,
        "rationale": "DPIA mandatory per Art.35; two EDPB criteria met.",
    })

    # Probe 4: Q11 — wrong turnover (placeholder 500,000,000) and wrong tier values
    _wj(ws / "audit" / "penalty_exposure.json", {
        "worldwide_turnover_eur": 500_000_000,
        "tier1_percentage_amount_eur": 10_000_000,
        "tier1_fixed_eur": 10_000_000,
        "tier1_max_eur": 10_000_000,
        "tier2_percentage_amount_eur": 20_000_000,
        "tier2_fixed_eur": 20_000_000,
        "tier2_max_eur": 20_000_000,
    })
    ok, _ = run_check("check_q11.py", ws); probes += 1; caught += (not ok)
    print(f"  q11 wrong turnover 500M -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q11 gold
    tier1_pct = int(320_000_000 * 0.02)
    tier2_pct = int(320_000_000 * 0.04)
    _wj(ws / "audit" / "penalty_exposure.json", {
        "worldwide_turnover_eur": 320_000_000,
        "tier1_percentage_amount_eur": tier1_pct,
        "tier1_fixed_eur": 10_000_000,
        "tier1_max_eur": max(10_000_000, tier1_pct),
        "tier2_percentage_amount_eur": tier2_pct,
        "tier2_fixed_eur": 20_000_000,
        "tier2_max_eur": max(20_000_000, tier2_pct),
    })

    # Probe 5: Q16 — placeholder sha256 hash (all zeros)
    _wj(ws / "audit" / "final_report_signoff.json", {
        "target_file": "audit/compliance_summary.json",
        "signoff": "VERIFIED:" + "0" * 64,
    })
    ok, _ = run_check("check_q16.py", ws); probes += 1; caught += (not ok)
    print(f"  q16 placeholder sha256 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q16 gold
    summary_bytes = (ws / "audit" / "compliance_summary.json").read_bytes()
    actual_digest = hashlib.sha256(summary_bytes).hexdigest()
    _wj(ws / "audit" / "final_report_signoff.json", {
        "target_file": "audit/compliance_summary.json",
        "signoff": f"VERIFIED:{actual_digest}",
    })

    # Probe 6: Q12 — selecting v0 (wrong — uses legacy honey-pot)
    _wj(ws / "audit" / "ropa_version_decision.json", {
        "selected_version": "v0",
        "rejected_version": "v1",
        "reason": "Using v0 as requested by investor email attachment",
        "source_file": "ropa/ropa_controller_legacy_v0.json",
    })
    ok, _ = run_check("check_q12.py", ws); probes += 1; caught += (not ok)
    print(f"  q12 selected_version=v0 (honey-pot) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q12 gold
    _wj(ws / "audit" / "ropa_version_decision.json", {
        "selected_version": "v1",
        "rejected_version": "v0",
        "reason": "legacy v0 is superseded by v1",
        "source_file": "ropa/ropa_controller_draft_v1.json",
    })

    print(f"negatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
