#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_sec5.py — sec5 可解性审计（金标自检）。

在 workspace 的临时副本上模拟 update 生效后的状态，写出每一轮的「正确产物」，
然后运行全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再做一组反例（错误产物）抽样，断言 check 能 FAIL（不过松）。

运行：python scripts/clawarena_authoring/gold_solve_sec5.py
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "sec5"
UPD = DS / "openclaw" / "updates" / "sec5"
SCRIPTS = DS / "eval" / "sec5" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/sec5_gold_ws")

# Ground-truth constants (must match build_sec5.py)
ULB_TOTAL = 284807
ULB_FRAUD = 492
ULB_FRAUD_RATE = 0.00172
ULB_DOI = "10.1016/j.eswa.2014.02.026"
PAYSIM_FLAG_THRESHOLD = 200000
PAYSIM_TX_TYPES = ["CASH-IN", "CASH-OUT", "DEBIT", "PAYMENT", "TRANSFER"]
PAYSIM_STEPS = 744
PAYSIM_FRAUD_RATE = 0.00129

VAMP_THRESHOLD_BPS = 150
VAMP_THRESHOLD_OLD_BPS = 220
VAMP_FEE_USD = 8
VAMP_GRACE_MONTHS = 3
VAMP_ENFORCEMENT = "2026-04-01"

MERCHANT_A_TC40 = 42
MERCHANT_A_TC15 = 18
MERCHANT_A_TC05 = 3800
MERCHANT_A_VAMP_BPS = (MERCHANT_A_TC40 + MERCHANT_A_TC15) / MERCHANT_A_TC05 * 10000

MC_ECM_BPS = 150
MC_HECM_BPS = 300
MC_ECM_FEE_M4_6_EUR = 5000
MERCHANT_B_CHARGEBACKS = 185
MERCHANT_B_PREV_TX = 10000
MERCHANT_B_CB_BPS = MERCHANT_B_CHARGEBACKS / MERCHANT_B_PREV_TX * 10000

SAR_DEADLINE_STD = 30
SAR_DEADLINE_NO_SUSPECT = 60
SAR_THRESHOLD_USD = 5000
SAR_FORM = "FinCEN Form 111"

SLA_ALERT_HOURS = 2
SLA_CASE_DAYS = 3
SLA_ESCALATION_USD = 50000

ALERT_BATCH_001_COUNT = 200
ALERT_BATCH_002_COUNT = 350

VAMP_SOURCE_URL = "https://www.corgilabs.ai/insights/vamp-2026-merchant-compliance"
MC_SOURCE_URL = "https://chargebacks911.com/mastercard-chargebacks/mastercard-excessive-fraud-chargeback-monitoring-programs/mastercard-ecm-program-thresholds-tiers/"
SAR_SOURCE_URL = "https://www.fincen.gov/resources/frequently-asked-questions-regarding-fincen-suspicious-activity-report-sar"
SLA_SOURCE_URL = "https://www.hyperbots.com/glossary/fraud-investigation-sla"


def _wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def prep_workspace() -> Path:
    """Copy workspace and apply updates."""
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)

    # Apply Update-1 workspace files
    u1 = UPD / "upd1_workspace"
    shutil.copy(u1 / "fraud_model_v2_report.md", GOLD / "models" / "fraud_model_v2_report.md")
    shutil.copy(u1 / "visa_vamp_config_DRAFT.json", GOLD / "data" / "reference" / "visa_vamp_config_DRAFT.json")
    shutil.copy(u1 / "alert_batch_002.json", GOLD / "data" / "alerts" / "alert_batch_002.json")

    # Apply Update-2 workspace files
    u2 = UPD / "upd2_workspace"
    (GOLD / "regulations").mkdir(parents=True, exist_ok=True)
    (GOLD / "comms").mkdir(parents=True, exist_ok=True)
    (GOLD / "cases").mkdir(parents=True, exist_ok=True)
    shutil.copy(u2 / "regulations" / "fincen_notice_20260601.md",
                GOLD / "regulations" / "fincen_notice_20260601.md")
    shutil.copy(u2 / "email_compliance_update2.eml",
                GOLD / "comms" / "email_compliance_update2.eml")
    shutil.copy(u2 / "cases" / "open_cases_updated.json",
                GOLD / "cases" / "open_cases_updated.json")
    shutil.copy(u2 / "cases" / "investigation_log_batch002.json",
                GOLD / "cases" / "investigation_log_batch002.json")

    return GOLD


def compute_vamp_script_hash(ws: Path) -> str:
    """Run compute_vamp_ratio.py with merchant A values, return sha256 of output."""
    result = subprocess.run(
        ["python", str(ws / "scripts" / "compute_vamp_ratio.py"),
         "--tc40", str(MERCHANT_A_TC40),
         "--tc15", str(MERCHANT_A_TC15),
         "--tc05", str(MERCHANT_A_TC05),
         "--merchant-id", "MERCH-A"],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode != 0:
        raise RuntimeError(f"compute_vamp_ratio.py failed: {result.stderr}")
    output = result.stdout.rstrip("\n")
    return hashlib.sha256(output.encode("utf-8")).hexdigest()


def get_sar_required_cases(ws: Path) -> list[dict]:
    """Get cases with sar_required=true from open_cases_updated.json."""
    p = ws / "cases" / "open_cases_updated.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    return [c for c in cases if c.get("sar_required", False)]


def get_highest_amount_case(ws: Path) -> dict:
    """Get the highest-amount case from open_cases.json above SAR threshold."""
    p = ws / "cases" / "open_cases.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    eligible = [c for c in cases if float(c.get("amount_usd", 0)) >= SAR_THRESHOLD_USD]
    return max(eligible, key=lambda c: float(c.get("amount_usd", 0)))


def solve(ws: Path) -> None:
    """Write gold-standard output files for all 17 questions."""
    out = ws / "output"
    out.mkdir(exist_ok=True)

    # ---- Q1: ULB fields ----
    # Hardened: doi must be exact verbatim, features exactly 31, class_values exactly [0,1] integers
    _wj(out / "q1_fields.json", {
        "schema_version": "1.0",
        "total_transactions": ULB_TOTAL,
        "fraud_count": ULB_FRAUD,
        "fraud_rate": ULB_FRAUD_RATE,
        "features": [f"V{i}" for i in range(1, 29)] + ["Time", "Amount", "Class"],
        "class_values": [0, 1],
        "doi": ULB_DOI,
        "source_url": "https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud"
    })
    # Verify: exactly 31 features, doi is exact string
    assert ULB_DOI == "10.1016/j.eswa.2014.02.026", f"DOI mismatch: {ULB_DOI}"

    # ---- Q2: ULB stats ----
    # Hardened: non_fraud_count must be exactly 284315, fraud_rate exactly 0.00172
    non_fraud = ULB_TOTAL - ULB_FRAUD  # = 284315
    assert non_fraud == 284315, f"non_fraud={non_fraud}"
    _wj(out / "q2_stats.json", {
        "schema_version": "1.0",
        "total_transactions": ULB_TOTAL,
        "fraud_count": ULB_FRAUD,
        "non_fraud_count": non_fraud,
        "fraud_rate": ULB_FRAUD_RATE
    })

    # ---- Q3: PaySim metadata ----
    # Hardened: exactly 5 tx types, exact fraud_rate, exact sample_case_id
    assert len(PAYSIM_TX_TYPES) == 5, f"Expected 5 tx types, got {len(PAYSIM_TX_TYPES)}"
    _wj(out / "q3_paysim_meta.json", {
        "schema_version": "1.0",
        "transaction_types": PAYSIM_TX_TYPES,
        "isFlaggedFraud_threshold": PAYSIM_FLAG_THRESHOLD,
        "simulation_steps": PAYSIM_STEPS,
        "fraud_rate": PAYSIM_FRAUD_RATE,
        "sample_case_id": "CASE-20260310-001"
    })

    # ---- Q4: Cases from alert_batch_001 ----
    # Use first few high/critical alerts as case basis
    alerts_data = json.loads((ws / "data" / "alerts" / "alert_batch_001.json").read_text())
    alerts = alerts_data.get("alerts", [])
    high_crit = [a for a in alerts if a.get("priority") in ("high", "critical")][:5]

    cases_q4 = []
    for i, alert in enumerate(high_crit):
        amt = round(float(alert.get("amount_usd", 1000)), 2)
        esc = amt >= SLA_ESCALATION_USD
        cases_q4.append({
            "case_id": f"CASE-20260310-{i+1:03d}",
            "status": "open",
            "amount_usd": amt,
            "sla_deadline": "2026-03-13T09:00:00Z",
            "escalation_required": esc
        })

    _wj(out / "q4_cases_created.json", {
        "schema_version": "1.0",
        "cases": cases_q4
    })

    # ---- Q5: SAR structure ----
    # Hardened: form_number must be exact "FinCEN Form 111", source_url required (P5 extended)
    assert SAR_FORM == "FinCEN Form 111", f"SAR_FORM={SAR_FORM!r}"
    _wj(out / "q5_sar_structure.json", {
        "schema_version": "1.0",
        "form_number": SAR_FORM,
        "filing_threshold_usd": SAR_THRESHOLD_USD,
        "standard_deadline_days": SAR_DEADLINE_STD,
        "no_suspect_deadline_days": SAR_DEADLINE_NO_SUSPECT,
        "five_ws": {
            "who": "The subject(s) conducting or facilitating the suspicious financial activity",
            "what": "The type and nature of the suspicious transaction(s), including structuring, layering, or fraud",
            "when": "The specific dates and time periods during which the suspicious activity occurred",
            "where": "The accounts, financial institutions, and geographic locations involved in the transactions",
            "why": "The specific indicators and red flags that make the activity suspicious under FinCEN guidelines"
        },
        "source_url": SAR_SOURCE_URL
    })

    # ---- Q6: Risk scores (threshold=0.5) ----
    score_data = [
        ("ALRT-20260301-0001", 0.72),
        ("ALRT-20260301-0005", 0.43),
        ("ALRT-20260301-0009", 0.88),
    ]
    scored = []
    for alrt_id, score in score_data:
        decision = "FRAUD" if score >= 0.5 else "LEGITIMATE"
        scored.append({"alert_id": alrt_id, "score": score, "threshold_used": 0.5, "decision": decision})

    _wj(out / "q6_risk_scores.json", {
        "schema_version": "1.0",
        "threshold_used": 0.5,
        "alerts": scored
    })

    # ---- Q7: Model comparison (V5 honeypot) ----
    # Hardened R2: added v1_threshold (0.5 from v1 config) + source_url (F-rule, P5 extended silently)
    _wj(out / "q7_model_comparison.json", {
        "schema_version": "1.0",
        "v1_auc": 0.982,
        "v2_auc": 0.987,
        "v1_threshold": 0.5,
        "v2_summary_threshold": 0.3,
        "v2_authoritative_threshold": 0.5,
        "identified_discrepancy": (
            "The auto-generated Executive Summary recommends threshold=0.3 based on raw recall metrics, "
            "but the Detailed Findings section (authoritative) concludes threshold=0.5 minimizes business "
            "cost ($347,890 vs $892,340 at threshold=0.3). The summary is a bot artifact and contradicts "
            "the body text which is the authoritative source."
        ),
        "authoritative_source": (
            "The 'Detailed Findings' section is authoritative; the 'Executive Summary' is auto-generated "
            "by a reporting bot and explicitly marked as non-authoritative. The detailed cost analysis "
            "confirms threshold=0.5 is optimal."
        ),
        "source_url": "models/fraud_model_v2_report.md#detailed-findings"
    })

    # ---- Q8: VAMP calculation (must use 150 bps, NOT 220 DRAFT) ----
    vamp_ratio = round(MERCHANT_A_VAMP_BPS, 2)
    _wj(out / "q8_vamp_calc.json", {
        "schema_version": "1.0",
        "merchant_id": "MERCH-A",
        "tc40_count": MERCHANT_A_TC40,
        "tc15_count": MERCHANT_A_TC15,
        "tc05_count": MERCHANT_A_TC05,
        "vamp_ratio_bps": vamp_ratio,
        "threshold_bps": VAMP_THRESHOLD_BPS,
        "is_excessive": vamp_ratio > VAMP_THRESHOLD_BPS,
        "source_url": VAMP_SOURCE_URL
    })

    # ---- Q9: Legacy document assessment (V6) ----
    # Hardened: reason must mention 220 and 2026, authoritative_source_file must be exact filename
    _wj(out / "q9_legacy_assessment.json", {
        "schema_version": "1.0",
        "document_name": "LEGACY_visa_vdmp_old_thresholds.md",
        "document_status": "LEGACY_DO_NOT_USE",
        "reason": (
            "This document reflects historical VDMP thresholds and an outdated VAMP threshold of 220 bps "
            "that applied globally before April 2026. It is marked DEPRECATED and explicitly states it "
            "should not be used for compliance calculations. The 220 bps threshold for US/CA/EU/APAC "
            "was superseded by the new VAMP 2026 program effective 2026-04-01."
        ),
        "correct_threshold_bps": VAMP_THRESHOLD_BPS,
        "authoritative_source_file": "visa_vamp_thresholds_2026.json",
        "source_url": VAMP_SOURCE_URL
    })

    # ---- Q10: Cases from batch002 (P4/P5) ----
    alerts2_data = json.loads((ws / "data" / "alerts" / "alert_batch_002.json").read_text())
    alerts2 = alerts2_data.get("alerts", [])
    high_crit2 = [a for a in alerts2 if a.get("priority") in ("high", "critical")][:5]

    cases_q10 = []
    assume_now = datetime(2026, 3, 17, 9, 0, 0, tzinfo=timezone.utc)
    for i, alert in enumerate(high_crit2):
        amt = round(float(alert.get("amount_usd", 1000)), 2)
        det = datetime.fromisoformat(alert.get("detected_at", "2026-03-15T00:00:00Z").replace("Z", "+00:00"))
        sla_deadline = det + timedelta(hours=72)
        remaining_h = round((sla_deadline - assume_now).total_seconds() / 3600, 2)
        esc = amt >= SLA_ESCALATION_USD
        cases_q10.append({
            "case_id": f"CASE-20260315-{i+1:03d}",
            "alert_id": alert.get("alert_id"),
            "amount_usd": amt,
            "sla_remaining_hours": remaining_h,
            "escalation_required": esc,
            "source_url": SLA_SOURCE_URL
        })

    _wj(out / "q10_cases_updated.json", {
        "schema_version": "1.0",
        "cases": cases_q10
    })

    # ---- Q11: Mastercard ECM/HECM compliance ----
    # Hardened: merchant_id required, chargeback_ratio_bps must be exactly 185.00 (2dp)
    cb_ratio = round(MERCHANT_B_CB_BPS, 2)
    assert cb_ratio == 185.0, f"cb_ratio={cb_ratio}"
    _wj(out / "q11_mc_compliance.json", {
        "schema_version": "1.0",
        "merchant_id": "MERCH-B",
        "monthly_chargebacks": MERCHANT_B_CHARGEBACKS,
        "previous_month_transactions": MERCHANT_B_PREV_TX,
        "chargeback_ratio_bps": cb_ratio,
        "program_tier": "ECM",
        "monthly_fee_eur": MC_ECM_FEE_M4_6_EUR,
        "source_url": MC_SOURCE_URL
    })

    # ---- Q12: SAR draft ----
    top_case = get_highest_amount_case(ws)
    top_amt = round(float(top_case.get("amount_usd", 10000)), 2)
    top_cid = top_case.get("case_id")
    _wj(out / "q12_sar_draft.json", {
        "schema_version": "1.0",
        "case_id": top_cid,
        "form_number": SAR_FORM,
        "filing_deadline_days": SAR_DEADLINE_STD,
        "amount_reported": top_amt,
        "narrative": {
            "who": f"Subject associated with case {top_cid}, identified through alert pattern analysis",
            "what": "Suspicious high-value transaction(s) inconsistent with normal account behavior",
            "when": f"Activity detected during March 2026 investigation period; case opened {top_case.get('created_at', '2026-03-10T00:00:00Z')[:10]}",
            "where": "MeridianPay payment processing platform; accounts involved per case file",
            "why": f"Transaction amount ${top_amt:,.2f} and behavior pattern indicate potential fraud; triggers mandatory SAR filing per $5,000 threshold"
        },
        "source_url": SAR_SOURCE_URL
    })

    # ---- Q13: VAMP revised after Update-2 supersede (V2/V10) ----
    # Hardened R2: added enforcement_date (F-rule); cross-round closure with Q8 enforced ±0.01
    _wj(out / "q13_vamp_revised.json", {
        "schema_version": "1.0",
        "merchant_id": "MERCH-A",
        "old_threshold_bps": VAMP_THRESHOLD_OLD_BPS,
        "new_threshold_bps": VAMP_THRESHOLD_BPS,
        "vamp_ratio_bps": vamp_ratio,
        "revised_is_excessive": vamp_ratio > VAMP_THRESHOLD_BPS,
        "enforcement_date": VAMP_ENFORCEMENT,
        "update_source": (
            "Update-2 supersede email (comms/email_compliance_update2.eml) explicitly revokes the DRAFT "
            "configuration (220 bps) and confirms the authoritative threshold of 150 bps per "
            "visa_vamp_thresholds_2026.json effective 2026-04-01."
        ),
        "source_url": VAMP_SOURCE_URL
    })

    # ---- Q14: Rescored with threshold=0.5 (Update-2 confirms) ----
    # Hardened R2: added q6_threshold_used (cross-round closure C★); schema_version (E★)
    rescored = []
    for alrt_id, score in score_data:
        decision = "FRAUD" if score >= 0.5 else "LEGITIMATE"
        rescored.append({"alert_id": alrt_id, "score": score, "decision": decision})

    _wj(out / "q14_rescored.json", {
        "schema_version": "1.0",
        "threshold_applied": 0.5,
        "q6_threshold_used": 0.5,
        "alerts": rescored,
        "changed_decisions": [],
        "consistency_note": (
            "Q6 correctly used threshold=0.5 (from model_v1_config.json, as confirmed by the Detailed "
            "Findings section). Update-2 supersedes the v2 summary's erroneous 0.3 recommendation and "
            "restores 0.5 as the authoritative threshold. Since Q6 already applied 0.5, no decisions "
            "changed between Q6 and Q14 — both yield FRAUD/LEGITIMATE/FRAUD for the three alerts."
        )
    })

    # ---- Q15: Weekly report ----
    # Hardened R2: added investigation_period_days=17 (F-rule); cross-round closure with Q8+Q11 ±0.01
    sar_required_cases = get_sar_required_cases(ws)
    _wj(out / "q15_weekly_report.json", {
        "schema_version": "1.0",
        "report_period": "2026-03-01 to 2026-03-17",
        "investigation_period_days": 17,
        "total_alerts_batch001": ALERT_BATCH_001_COUNT,
        "total_alerts_batch002": ALERT_BATCH_002_COUNT,
        "vamp_ratio_bps": vamp_ratio,
        "vamp_threshold_bps": VAMP_THRESHOLD_BPS,
        "vamp_status": "EXCESSIVE",
        "mc_program_tier": "ECM",
        "sar_to_file_count": len(sar_required_cases),
        "source_url": VAMP_SOURCE_URL
    })

    # ---- Q16: SAR deadlines ----
    # Hardened R2: each case must have sar_form_number="FinCEN Form 111" (F-rule);
    # sar_deadline_days cross-round closure with Q5 (C★)
    sar_cases = get_sar_required_cases(ws)
    sar_entries = []
    for case in sar_cases:
        det_str = case.get("detection_date") or case.get("created_at", "")[:10]
        det_d = date.fromisoformat(det_str[:10])
        dl_d = det_d + timedelta(days=SAR_DEADLINE_STD)
        amt = round(float(case.get("amount_usd", 0)), 2)
        sar_entries.append({
            "case_id": case.get("case_id"),
            "detection_date": det_str[:10],
            "deadline_date": dl_d.isoformat(),
            "amount_usd": amt,
            "narrative_structure": "five-W (who/what/when/where/why) per FinCEN Form 111 requirements",
            "sar_form_number": SAR_FORM
        })

    _wj(out / "q16_sar_deadlines.json", {
        "schema_version": "1.0",
        "sar_deadline_days": SAR_DEADLINE_STD,
        "source_url": SAR_SOURCE_URL,
        "cases": sar_entries
    })

    # ---- Q17: Bash-sha256 sign-off ----
    digest = compute_vamp_script_hash(ws)
    _w(out / "q17_signoff.txt", f"VERIFIED:{digest}\n")

    print(f"  [gold] All 17 output files written to {out}")
    print(f"  [gold] Q17 sha256: {digest}")


def run_check(script: Path, ws: Path) -> tuple[bool, str]:
    """Run a check script; return (passed, output)."""
    result = subprocess.run(
        ["python", str(script), str(ws)],
        capture_output=True, text=True, timeout=60
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def run_pref_check(ws: Path, rules: str, target: str) -> tuple[bool, str]:
    """Run check_preferences.py for given rules and target."""
    result = subprocess.run(
        ["python", str(SCRIPTS / "check_preferences.py"), str(ws),
         "--rules", rules, "--target", target],
        capture_output=True, text=True, timeout=30
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def audit_gold(ws: Path) -> None:
    """Run all checks on gold outputs; assert all PASS."""
    print("\n=== Gold solve: running all checks ===")
    all_pass = True

    # Q1-Q17 checks
    checks = [f"check_q{i}" for i in range(1, 18)]
    for check_name in checks:
        script = SCRIPTS / f"{check_name}.py"
        passed, output = run_check(script, ws)
        status = "PASS" if passed else "FAIL"
        print(f"  {check_name}: {status} — {output[:80]}")
        if not passed:
            all_pass = False

    # Preference checks (sampling key rounds)
    pref_tests = [
        ("output/q1_fields.json", "P1"),
        ("output/q3_paysim_meta.json", "P1,P2"),
        ("output/q4_cases_created.json", "P1,P2,P4"),
        ("output/q5_sar_structure.json", "P1,P3"),
        ("output/q8_vamp_calc.json", "P5"),
        ("output/q10_cases_updated.json", "P1,P2,P4,P5"),
        ("output/q11_mc_compliance.json", "P1,P5"),
        ("output/q12_sar_draft.json", "P1,P3,P4,P5"),
        ("output/q13_vamp_revised.json", "P1,P5"),
        ("output/q15_weekly_report.json", "P1,P4,P5"),
        ("output/q16_sar_deadlines.json", "P1,P2,P3,P4,P5"),
    ]
    for target, rules in pref_tests:
        passed, output = run_pref_check(ws, rules, target)
        status = "PASS" if passed else "FAIL"
        print(f"  pref({rules}) on {target}: {status} — {output[:80]}")
        if not passed:
            all_pass = False

    return all_pass


def audit_negatives(ws: Path) -> None:
    """Write wrong outputs and verify checks FAIL."""
    print("\n=== Negative (counter-example) tests ===")
    all_caught = True
    neg_results = []

    def _run_neg(check_name: str, obj: dict, filename: str, label: str) -> bool:
        """Write wrong output, run check, expect FAIL."""
        p = ws / "output" / filename
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        script = SCRIPTS / f"{check_name}.py"
        passed, output = run_check(script, ws)
        caught = not passed  # we expect FAIL
        status = "CAUGHT" if caught else "MISSED"
        print(f"  neg {check_name} [{label}]: {status} — {output[:80]}")
        return caught

    # Neg 1: Q2 wrong fraud count
    c1 = _run_neg("check_q2", {
        "schema_version": "1.0",
        "total_transactions": 284807,
        "fraud_count": 100,   # WRONG (should be 492)
        "non_fraud_count": 284707,
        "fraud_rate": 0.00035
    }, "q2_stats.json", "wrong fraud_count=100")
    all_caught = all_caught and c1

    # Neg 2: Q3 wrong transaction types (has 6 types including WITHDRAWAL — extra)
    c2 = _run_neg("check_q3", {
        "schema_version": "1.0",
        "transaction_types": ["CASH-IN", "CASH-OUT", "DEBIT", "PAYMENT", "TRANSFER", "WITHDRAWAL"],  # extra WITHDRAWAL
        "isFlaggedFraud_threshold": 200000,
        "simulation_steps": 744,
        "fraud_rate": 0.00129,
        "sample_case_id": "CASE-20260310-001"
    }, "q3_paysim_meta.json", "6 types with extra WITHDRAWAL")
    all_caught = all_caught and c2

    # Neg 3: Q8 uses WRONG threshold=220 (red herring)
    c3 = _run_neg("check_q8", {
        "schema_version": "1.0",
        "tc40_count": 42,
        "tc15_count": 18,
        "tc05_count": 3800,
        "vamp_ratio_bps": 157.89,
        "threshold_bps": 220,   # WRONG — should be 150
        "is_excessive": False,   # WRONG — 157.89 > 150
        "source_url": "https://example.com/legacy"
    }, "q8_vamp_calc.json", "threshold=220 DRAFT (red herring)")
    all_caught = all_caught and c3

    # Neg 4: Q9 wrong document_status and wrong authoritative_source_file
    c4 = _run_neg("check_q9", {
        "schema_version": "1.0",
        "document_name": "LEGACY_visa_vdmp_old_thresholds.md",
        "document_status": "ACTIVE",   # WRONG — should be LEGACY_DO_NOT_USE
        "reason": "This document is still valid for CEMEA region",
        "correct_threshold_bps": 220,  # WRONG
        "authoritative_source_file": "LEGACY_visa_vdmp_old_thresholds.md"  # WRONG — self-referential
    }, "q9_legacy_assessment.json", "document_status=ACTIVE and wrong auth source")
    all_caught = all_caught and c4

    # Neg 5: Q7 fails to detect discrepancy AND missing source_url (R2 hardened)
    c5 = _run_neg("check_q7", {
        "schema_version": "1.0",
        "v1_auc": 0.982,
        "v2_auc": 0.987,
        "v1_threshold": 0.5,
        "v2_summary_threshold": 0.5,  # WRONG — should be 0.3 (bot summary value)
        "v2_authoritative_threshold": 0.5,
        "identified_discrepancy": "",  # WRONG — missing discrepancy
        "authoritative_source": "detailed findings",
        "source_url": ""  # WRONG — empty source_url (R2 F-rule)
    }, "q7_model_comparison.json", "misses v2 summary=0.3 discrepancy and no source_url")
    all_caught = all_caught and c5

    # Neg 6: Q13 missing enforcement_date AND wrong vamp_ratio (R2 hardened: ±0.01 closure)
    c6 = _run_neg("check_q13", {
        "schema_version": "1.0",
        "merchant_id": "MERCH-A",
        "old_threshold_bps": 220,
        "new_threshold_bps": 150,
        "vamp_ratio_bps": 157.0,   # WRONG — differs from Q8's 157.89 by >0.01 bps
        "revised_is_excessive": True,
        "enforcement_date": "2026-03-01",  # WRONG — should be 2026-04-01
        "update_source": "Update-2",
        "source_url": VAMP_SOURCE_URL
    }, "q13_vamp_revised.json", "wrong enforcement_date and vamp_ratio differs from Q8")
    all_caught = all_caught and c6

    # Neg 7: Q5 wrong form_number (not exact verbatim) and missing source_url
    c7 = _run_neg("check_q5", {
        "schema_version": "1.0",
        "form_number": "FinCEN SAR-111",   # WRONG — should be exactly "FinCEN Form 111"
        "filing_threshold_usd": 5000,
        "standard_deadline_days": 30,
        "no_suspect_deadline_days": 60,
        "five_ws": {
            "who": "The subject conducting suspicious activity",
            "what": "Suspicious financial transaction type and nature",
            "when": "Specific dates of the suspicious activity period",
            "where": "Accounts and locations involved in the transactions",
            "why": "Red flags and indicators of suspicious behavior"
        },
        "source_url": ""  # WRONG — empty source_url
    }, "q5_sar_structure.json", "form_number wrong variant and no source_url")
    all_caught = all_caught and c7

    # Neg 8: Q15 missing investigation_period_days and wrong sar_to_file_count (R2 hardened)
    c8 = _run_neg("check_q15", {
        "schema_version": "1.0",
        "report_period": "2026-03-01 to 2026-03-17",
        "investigation_period_days": 30,  # WRONG — should be 17
        "total_alerts_batch001": 200,
        "total_alerts_batch002": 350,
        "vamp_ratio_bps": 157.89,
        "vamp_threshold_bps": 150,
        "vamp_status": "EXCESSIVE",
        "mc_program_tier": "ECM",
        "sar_to_file_count": 5,      # WRONG — should be 20 from open_cases_updated.json
        "source_url": VAMP_SOURCE_URL
    }, "q15_weekly_report.json", "investigation_period_days=30 (wrong) and sar_count=5 (wrong)")
    all_caught = all_caught and c8

    # Neg 9: Q1 wrong doi (truncated) and missing source_url (R2 hardened)
    c9 = _run_neg("check_q1", {
        "schema_version": "1.0",
        "total_transactions": 284807,
        "fraud_count": 492,
        "fraud_rate": 0.00172,
        "features": [f"V{i}" for i in range(1, 29)] + ["Time", "Amount", "Class"],  # 31 features
        "class_values": [0, 1],
        "doi": "10.1016/j.eswa.2014"  # WRONG — truncated DOI (no source_url either)
    }, "q1_fields.json", "truncated doi and missing source_url")
    all_caught = all_caught and c9

    # Neg 10: Q11 wrong merchant_id and wrong chargeback_ratio
    c10 = _run_neg("check_q11", {
        "schema_version": "1.0",
        "merchant_id": "MERCH-A",  # WRONG — should be MERCH-B
        "monthly_chargebacks": 185,
        "previous_month_transactions": 10000,
        "chargeback_ratio_bps": 150.0,  # WRONG — should be 185.0
        "program_tier": "ECM",
        "monthly_fee_eur": 5000,
        "source_url": MC_SOURCE_URL
    }, "q11_mc_compliance.json", "wrong merchant_id and ratio")
    all_caught = all_caught and c10

    neg_count = sum([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10])
    print(f"\n  Negative tests: {neg_count}/10 caught")
    return all_caught, 10


def main() -> None:
    print("=== sec5 gold_solve audit ===")
    print(f"  Workspace source: {WS_SRC}")
    print(f"  Gold workspace:   {GOLD}")

    if not WS_SRC.exists():
        print("ERROR: workspace not found — run build_sec5.py first")
        sys.exit(1)

    ws = prep_workspace()
    print(f"  Workspace prepared at {ws}")

    solve(ws)

    gold_pass = audit_gold(ws)
    neg_ok, neg_total = audit_negatives(ws)

    print("\n=== AUDIT SUMMARY ===")
    if gold_pass and neg_ok:
        print("AUDIT OK: all gold checks PASSED, all negative examples CAUGHT")
    else:
        if not gold_pass:
            print("AUDIT FAILED: some gold checks FAILED")
        if not neg_ok:
            print("AUDIT FAILED: some negative examples NOT caught (over-permissive)")
        sys.exit(1)


if __name__ == "__main__":
    main()
