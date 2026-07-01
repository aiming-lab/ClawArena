#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_sec5_checks.py — 生成 sec5 的全部 exec_check 校验脚本到 eval/sec5/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），锚点对齐 build_sec5.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5。

第二轮加难手段：
  C★ 跨轮闭合连锁：Q13 精确比对 Q8 vamp_ratio；Q15 精确比对 Q8/Q11；Q14 须读取 Q6 threshold；
                    Q16 须与 Q5 deadline 一致
  E★ 静默 P1/P5 并入更多轮 eval（Q1/Q2/Q7/Q9/Q13/Q14 的 eval command 现在包含 P1）
  F  Q7 新增 source_url 必填；Q13 新增 enforcement_date 字段；Q15 新增 investigation_period_days；
     Q16 每 case 须有 sar_form_number="FinCEN Form 111"；Q12 新增 case_id 字段来自数据文件
  G  撤脚手架：不在 question 里提醒 schema_version（check 里静默考核）
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/sec5/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, subprocess
from pathlib import Path
from datetime import date, timedelta

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)
'''

CHECKS = {}

# Q1: ULB fields output
# 加难 E★: schema_version 静默检查（eval 内置，question 无提醒）
# 加难 F: 新增 source_url 必须是 kaggle URL
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q1_fields.json")
    if err: _finish([err])

    # Layer 1: structure — schema_version silently checked (E-rule: no reminder in question)
    if data.get("schema_version") != "1.0":
        fails.append(f"schema_version={data.get('schema_version')!r} must be '1.0' (session-wide requirement)")

    for k in ("total_transactions", "fraud_count", "fraud_rate", "features", "class_values", "doi"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    # Layer 2: field types
    if not isinstance(data.get("features"), list):
        fails.append("features must be a list")
    if not isinstance(data.get("class_values"), list):
        fails.append("class_values must be a list")

    # Layer 3: true values
    if data.get("total_transactions") != 284807:
        fails.append(f"total_transactions={data.get('total_transactions')} (expected 284807)")
    if data.get("fraud_count") != 492:
        fails.append(f"fraud_count={data.get('fraud_count')} (expected 492)")
    rate = float(data.get("fraud_rate", 0))
    if abs(rate - 0.00172) > 0.00001:
        fails.append(f"fraud_rate={rate:.6f} (expected exactly 0.00172, tolerance ±0.00001)")

    # Verbatim V1-V28 features present
    feats = [str(f) for f in (data.get("features") or [])]
    for vi in range(1, 29):
        fname = f"V{vi}"
        if fname not in feats:
            fails.append(f"features missing verbatim field {fname!r}")
    for must in ("Time", "Amount", "Class"):
        if must not in feats:
            fails.append(f"features missing {must!r}")

    # Exact feature count: V1-V28 (28) + Time + Amount + Class = 31
    if len(feats) != 31:
        fails.append(f"features list must have exactly 31 elements (V1-V28 + Time + Amount + Class), got {len(feats)}")

    # class_values must contain exactly [0, 1] (integers, not strings)
    cv = data.get("class_values") or []
    if set(cv) != {0, 1} or len(cv) != 2:
        fails.append(f"class_values must be exactly [0, 1] (two integer values), got {cv!r}")

    # DOI must be exactly "10.1016/j.eswa.2014.02.026" (exact match, not substring)
    doi = str(data.get("doi", ""))
    if doi != "10.1016/j.eswa.2014.02.026":
        fails.append(f"doi must be exactly '10.1016/j.eswa.2014.02.026', got {doi!r}")

    # source_url must reference the Kaggle dataset (F-rule: verbatim source citation)
    su = str(data.get("source_url", "")).strip()
    if not su:
        fails.append("source_url is missing — must cite the Kaggle dataset URL from README")
    elif "kaggle" not in su.lower():
        fails.append(f"source_url={su!r} must reference the Kaggle dataset (from README_datasets.md)")

    _finish(fails)
main()
'''

# Q2: ULB stats with arithmetic closure
# 加难 E★: schema_version 静默检查（eval 内置）
# 加难 F: 新增 source_url 必须不为空
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q2_stats.json")
    if err: _finish([err])

    # E-rule: schema_version silently checked
    if data.get("schema_version") != "1.0":
        fails.append(f"schema_version={data.get('schema_version')!r} must be '1.0'")

    for k in ("total_transactions", "fraud_count", "fraud_rate", "non_fraud_count"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    if data.get("total_transactions") != 284807:
        fails.append(f"total_transactions={data.get('total_transactions')} (expected 284807)")
    if data.get("fraud_count") != 492:
        fails.append(f"fraud_count={data.get('fraud_count')} (expected 492)")

    rate = float(data.get("fraud_rate", 0))
    if abs(rate - 0.00172) > 0.00001:
        fails.append(f"fraud_rate={rate:.6f} (expected exactly 0.00172, tolerance ±0.00001)")

    non_fraud = data.get("non_fraud_count", 0)
    if non_fraud != 284315:
        fails.append(f"non_fraud_count={non_fraud} (expected exactly 284315 = 284807 - 492)")

    total = data.get("total_transactions", 0)
    fraud = data.get("fraud_count", 0)
    if isinstance(total, int) and isinstance(fraud, int) and isinstance(non_fraud, int):
        if fraud + non_fraud != total:
            fails.append(f"closure failed: fraud({fraud}) + non_fraud({non_fraud}) != total({total})")
    else:
        fails.append("total_transactions/fraud_count/non_fraud_count must be integers")

    _finish(fails)
main()
'''

# Q3: PaySim metadata (exact 5-type list, exact fraud_rate, exact sample_case_id)
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q3_paysim_meta.json")
    if err: _finish([err])

    for k in ("transaction_types", "isFlaggedFraud_threshold", "simulation_steps",
               "fraud_rate", "sample_case_id"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    ttypes = [str(t) for t in (data.get("transaction_types") or [])]
    REQUIRED_TYPES = ["CASH-IN", "CASH-OUT", "DEBIT", "PAYMENT", "TRANSFER"]
    for need in REQUIRED_TYPES:
        if need not in ttypes:
            fails.append(f"transaction_types missing verbatim value {need!r}")
    if len(ttypes) != 5:
        fails.append(f"transaction_types must have exactly 5 entries (got {len(ttypes)}): {REQUIRED_TYPES}")

    if int(data.get("isFlaggedFraud_threshold", 0)) != 200000:
        fails.append(f"isFlaggedFraud_threshold={data.get('isFlaggedFraud_threshold')} (expected 200000)")

    if int(data.get("simulation_steps", 0)) != 744:
        fails.append(f"simulation_steps={data.get('simulation_steps')} (expected 744)")

    fr = float(data.get("fraud_rate", 0))
    if abs(fr - 0.00129) > 0.00001:
        fails.append(f"fraud_rate={fr:.6f} (expected exactly 0.00129 per README, tolerance ±0.00001)")

    cid = str(data.get("sample_case_id", ""))
    if cid != "CASE-20260310-001":
        fails.append(f"sample_case_id must be exactly 'CASE-20260310-001' (got {cid!r})")

    _finish(fails)
main()
'''

# Q4: Cases created from alert_batch_001
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q4_cases_created.json")
    if err: _finish([err])

    cases = data.get("cases") or data.get("case_records") or []
    if not isinstance(cases, list):
        if isinstance(data, list):
            cases = data
        else:
            fails.append("no cases list found in q4_cases_created.json")
            _finish(fails)

    if len(cases) < 3:
        fails.append(f"expected ≥3 case records, got {len(cases)}")

    for i, case in enumerate(cases[:10]):
        cid = str(case.get("case_id", ""))
        if not re.fullmatch(r"CASE-\\d{8}-\\d{3}", cid):
            fails.append(f"case[{i}].case_id {cid!r} does not match CASE-YYYYMMDD-NNN")

        amt = case.get("amount_usd")
        if amt is not None:
            parts = f"{float(amt):.10f}".rstrip("0").split(".")
            dp = len(parts[1]) if len(parts) > 1 else 0
            if dp > 2:
                fails.append(f"case[{i}].amount_usd={amt} has >2 decimal places")

        esc = case.get("escalation_required")
        if esc is not None and not isinstance(esc, bool):
            fails.append(f"case[{i}].escalation_required must be bool, got {type(esc).__name__}")

        if amt is not None and float(amt) >= 50000 and esc is False:
            fails.append(f"case[{i}].escalation_required should be true for amount={amt}>=50000")

    _finish(fails)
main()
'''

# Q5: SAR structure (exact form_number, source_url required, five_ws min length)
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q5_sar_structure.json")
    if err: _finish([err])

    for k in ("form_number", "filing_threshold_usd", "standard_deadline_days",
               "no_suspect_deadline_days", "five_ws", "source_url"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    fn = str(data.get("form_number", ""))
    if fn != "FinCEN Form 111":
        fails.append(f"form_number={fn!r} must be exactly 'FinCEN Form 111' (verbatim, no extra text)")

    if int(data.get("filing_threshold_usd", 0)) != 5000:
        fails.append(f"filing_threshold_usd={data.get('filing_threshold_usd')} (expected 5000)")

    if int(data.get("standard_deadline_days", 0)) != 30:
        fails.append(f"standard_deadline_days={data.get('standard_deadline_days')} (expected 30)")

    if int(data.get("no_suspect_deadline_days", 0)) != 60:
        fails.append(f"no_suspect_deadline_days={data.get('no_suspect_deadline_days')} (expected 60)")

    five_ws = data.get("five_ws") or {}
    if not isinstance(five_ws, dict):
        fails.append("five_ws must be a dict/object")
    else:
        for w_key in ("who", "what", "when", "where", "why"):
            val = str(five_ws.get(w_key, "")).strip()
            if not val:
                fails.append(f"five_ws.{w_key} is missing or empty")
            elif len(val) < 10:
                fails.append(f"five_ws.{w_key}={val!r} is too brief (must be ≥10 chars, not a placeholder)")

    su = str(data.get("source_url", "")).strip()
    if not su:
        fails.append("source_url is empty — must reference FinCEN FAQ URL (P5)")
    elif "fincen" not in su.lower() and "fluxforce" not in su.lower():
        fails.append(f"source_url={su!r} does not look like a FinCEN source (expected fincen.gov or equivalent)")

    _finish(fails)
main()
'''

# Q6: Risk scores with threshold=0.5
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q6_risk_scores.json")
    if err: _finish([err])

    alerts = data.get("alerts") or data.get("scores") or []
    if isinstance(data, list):
        alerts = data

    if len(alerts) < 3:
        fails.append(f"expected 3 scored alerts, got {len(alerts)}")

    lookup = {}
    for a in alerts:
        lookup[str(a.get("alert_id", ""))] = a

    thresholds = set()
    for a in alerts:
        t = a.get("threshold_used")
        if t is not None:
            thresholds.add(float(t))
    if thresholds and thresholds != {0.5}:
        fails.append(f"threshold_used must be 0.5 (got {thresholds}); do not use the bot summary's 0.3")

    expected = {
        "ALRT-20260301-0001": ("FRAUD", 0.72),
        "ALRT-20260301-0005": ("LEGITIMATE", 0.43),
        "ALRT-20260301-0009": ("FRAUD", 0.88),
    }
    for alrt_id, (exp_decision, exp_score) in expected.items():
        entry = lookup.get(alrt_id)
        if entry is None:
            fails.append(f"missing alert {alrt_id}")
            continue
        dec = str(entry.get("decision", "")).upper()
        if dec != exp_decision:
            fails.append(f"{alrt_id}: decision={dec!r} (expected {exp_decision!r})")

    _finish(fails)
main()
'''

# Q7: Model comparison
# 加难 E★: schema_version + source_url 静默检查（eval 内置，question 无提醒）
# 加难 F: 新增 v1_threshold 必须=0.5，source_url 必须非空
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q7_model_comparison.json")
    if err: _finish([err])

    # E-rule: schema_version silently checked (no reminder in question)
    if data.get("schema_version") != "1.0":
        fails.append(f"schema_version={data.get('schema_version')!r} must be '1.0'")

    for k in ("v1_auc", "v2_auc", "v1_threshold", "v2_summary_threshold",
               "v2_authoritative_threshold", "identified_discrepancy",
               "authoritative_source", "source_url"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    # v1_threshold must be exactly 0.5 (from models/fraud_model_v1_config.json)
    v1_t = float(data.get("v1_threshold", 0))
    if abs(v1_t - 0.5) > 0.01:
        fails.append(f"v1_threshold={v1_t} (expected 0.5 from fraud_model_v1_config.json)")

    # Auto-summary says 0.3, authoritative says 0.5
    v2_sum = float(data.get("v2_summary_threshold", 0))
    if abs(v2_sum - 0.3) > 0.01:
        fails.append(f"v2_summary_threshold={v2_sum} (expected 0.3 — the distorted bot summary value)")

    v2_auth = float(data.get("v2_authoritative_threshold", 0))
    if abs(v2_auth - 0.5) > 0.01:
        fails.append(f"v2_authoritative_threshold={v2_auth} (expected 0.5 from Detailed Findings)")

    disc = str(data.get("identified_discrepancy", "")).strip()
    if not disc:
        fails.append("identified_discrepancy is empty — must explain the 0.3 vs 0.5 contradiction")
    elif len(disc) < 20:
        fails.append(f"identified_discrepancy too brief ({len(disc)} chars) — must substantively explain contradiction")

    if not str(data.get("authoritative_source", "")).strip():
        fails.append("authoritative_source is empty")

    # F-rule: source_url must be non-empty (P5 extended silently to this round)
    su = str(data.get("source_url", "")).strip()
    if not su:
        fails.append("source_url is missing — regulatory analysis must cite sources")

    _finish(fails)
main()
'''

# Q8: VAMP calculation (must use 150 bps, NOT 220 DRAFT)
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q8_vamp_calc.json")
    if err: _finish([err])

    for k in ("tc40_count", "tc15_count", "tc05_count", "vamp_ratio_bps",
               "threshold_bps", "is_excessive", "source_url"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    if int(data.get("tc40_count", -1)) != 42:
        fails.append(f"tc40_count={data.get('tc40_count')} (expected 42)")
    if int(data.get("tc15_count", -1)) != 18:
        fails.append(f"tc15_count={data.get('tc15_count')} (expected 18)")
    if int(data.get("tc05_count", -1)) != 3800:
        fails.append(f"tc05_count={data.get('tc05_count')} (expected 3800)")

    ratio = float(data.get("vamp_ratio_bps", 0))
    expected_ratio = (42 + 18) / 3800 * 10000  # = 157.8947...
    if abs(ratio - expected_ratio) > 0.1:
        fails.append(f"vamp_ratio_bps={ratio:.4f} (expected {expected_ratio:.4f}, tolerance ±0.1 bps)")

    # Must use 150 bps, NOT the DRAFT 220 bps
    thr = int(data.get("threshold_bps", 0))
    if thr == 220:
        fails.append("threshold_bps=220 — this is from the DRAFT (red herring); must use 150 from visa_vamp_thresholds_2026.json")
    elif thr != 150:
        fails.append(f"threshold_bps={thr} (expected 150 from authoritative file)")

    # is_excessive must be True (157.89 > 150)
    if data.get("is_excessive") is not True:
        fails.append(f"is_excessive={data.get('is_excessive')} (expected True — 157.89 > 150 bps)")

    if not str(data.get("source_url", "")).strip():
        fails.append("source_url is empty — P5 requires regulatory citations include source_url")

    _finish(fails)
main()
'''

# Q9: Legacy document assessment
# 加难 E★: schema_version 静默检查（eval 内置）
# 加难 F: reason 必须精确包含 "2026-04-01" 而非仅 "2026"
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q9_legacy_assessment.json")
    if err: _finish([err])

    # E-rule: schema_version silently checked
    if data.get("schema_version") != "1.0":
        fails.append(f"schema_version={data.get('schema_version')!r} must be '1.0'")

    for k in ("document_name", "document_status", "reason", "correct_threshold_bps",
               "authoritative_source_file"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    dname = str(data.get("document_name", ""))
    if dname != "LEGACY_visa_vdmp_old_thresholds.md":
        fails.append(f"document_name={dname!r} (expected 'LEGACY_visa_vdmp_old_thresholds.md')")

    status = str(data.get("document_status", ""))
    if status != "LEGACY_DO_NOT_USE":
        fails.append(f"document_status={status!r} (must be exactly 'LEGACY_DO_NOT_USE')")

    thr = data.get("correct_threshold_bps")
    try:
        thr_int = int(thr)
    except (TypeError, ValueError):
        thr_int = -1
    if thr_int != 150:
        fails.append(f"correct_threshold_bps={thr} (expected 150 — the 2026-04-01 authoritative threshold)")

    # F-rule: reason must explicitly contain "2026-04-01" (not just "2026") and "220"
    reason = str(data.get("reason", "")).strip()
    if not reason:
        fails.append("reason is empty — must explain why the LEGACY document is deprecated")
    else:
        if "220" not in reason:
            fails.append(f"reason must mention the superseded 220 bps threshold; got: {reason[:120]!r}")
        if "2026-04-01" not in reason:
            fails.append(f"reason must state the exact effective date '2026-04-01' of the new threshold; got: {reason[:120]!r}")

    VALID_SOURCES = {
        "visa_vamp_thresholds_2026.json",
        "visa_vamp_fact_sheet_summary.md",
    }
    src = str(data.get("authoritative_source_file", "")).strip()
    if not src:
        fails.append("authoritative_source_file is empty")
    elif src not in VALID_SOURCES:
        fails.append(f"authoritative_source_file={src!r} must be one of {sorted(VALID_SOURCES)}")

    _finish(fails)
main()
'''

# Q10: Cases updated from batch002 (P4/P5)
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q10_cases_updated.json")
    if err: _finish([err])

    cases = data.get("cases") or data.get("case_records") or []
    if isinstance(data, list):
        cases = data

    if len(cases) < 3:
        fails.append(f"expected ≥3 case records, got {len(cases)}")

    for i, case in enumerate(cases[:10]):
        cid = str(case.get("case_id", ""))
        if not re.fullmatch(r"CASE-\\d{8}-\\d{3}", cid):
            fails.append(f"case[{i}].case_id {cid!r} does not match CASE-YYYYMMDD-NNN")

        amt = case.get("amount_usd")
        if amt is not None:
            parts = f"{float(amt):.10f}".rstrip("0").split(".")
            dp = len(parts[1]) if len(parts) > 1 else 0
            if dp > 2:
                fails.append(f"case[{i}].amount_usd={amt} has >2 decimal places (P4)")

        esc = case.get("escalation_required")
        if amt is not None and float(amt) >= 50000 and esc is False:
            fails.append(f"case[{i}].escalation_required should be true for amount={amt}")

        su = str(case.get("source_url", "")).strip()
        if not su:
            fails.append(f"case[{i}].source_url missing (P5 requires regulatory source URLs)")

    _finish(fails)
main()
'''

# Q11: Mastercard ECM/HECM compliance (exact ratio ±0.01, merchant_id required)
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q11_mc_compliance.json")
    if err: _finish([err])

    for k in ("monthly_chargebacks", "previous_month_transactions", "chargeback_ratio_bps",
               "program_tier", "monthly_fee_eur", "source_url", "merchant_id"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    mid = str(data.get("merchant_id", ""))
    if not any(kw in mid.upper() for kw in ("MERCH-B", "MERCHANT-B", "MERCHANT_B", "B")):
        fails.append(f"merchant_id={mid!r} does not identify Merchant B")

    if int(data.get("monthly_chargebacks", -1)) != 185:
        fails.append(f"monthly_chargebacks={data.get('monthly_chargebacks')} (expected 185)")
    if int(data.get("previous_month_transactions", -1)) != 10000:
        fails.append(f"previous_month_transactions={data.get('previous_month_transactions')} (expected 10000)")

    ratio = float(data.get("chargeback_ratio_bps", 0))
    expected = 185.0
    if abs(ratio - expected) > 0.01:
        fails.append(f"chargeback_ratio_bps={ratio:.4f} (expected exactly {expected:.2f}, tolerance ±0.01)")

    ratio_str = str(data.get("chargeback_ratio_bps", ""))
    if "." in ratio_str:
        dp = len(ratio_str.split(".")[1])
        if dp > 2:
            fails.append(f"chargeback_ratio_bps={ratio_str} has >2 decimal places (P4)")

    tier = str(data.get("program_tier", "")).strip()
    if tier not in ("ECM", "HECM", "none"):
        fails.append(f"program_tier={tier!r} must be 'ECM', 'HECM', or 'none'")
    if tier != "ECM":
        fails.append(f"program_tier={tier!r} — 185 bps (150-299 range) with 185 chargebacks (100-299) = ECM")

    fee = data.get("monthly_fee_eur")
    try:
        fee_int = int(fee)
    except (TypeError, ValueError):
        fee_int = -1
    if fee_int != 5000:
        fails.append(f"monthly_fee_eur={fee} (expected 5000 for ECM month 4-6)")

    if not str(data.get("source_url", "")).strip():
        fails.append("source_url is empty (P5)")

    _finish(fails)
main()
'''

# Q12: SAR draft
# 加难 C★: 新增 case_id 字段，必须精确匹配 open_cases.json 中最高金额案件（cross-round）
# 加难 F: filing_deadline_days 须与 Q5 的 standard_deadline_days 一致（跨轮读取）
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q12_sar_draft.json")
    if err: _finish([err])

    for k in ("case_id", "form_number", "filing_deadline_days", "amount_reported",
               "narrative", "source_url"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    # Verbatim form number
    fn = str(data.get("form_number", ""))
    if "FinCEN Form 111" not in fn:
        fails.append(f"form_number={fn!r} must contain 'FinCEN Form 111' verbatim")

    # C-rule: filing_deadline_days must match Q5 standard_deadline_days (cross-round closure)
    q5_data, q5_err = _load_json(ws / "output" / "q5_sar_structure.json")
    if q5_err:
        fails.append(f"cannot verify cross-round deadline — Q5 output missing: {q5_err}")
    else:
        q5_deadline = q5_data.get("standard_deadline_days") if q5_data else None
        q12_deadline = data.get("filing_deadline_days")
        if q5_deadline is not None and q12_deadline is not None:
            if int(q12_deadline) != int(q5_deadline):
                fails.append(
                    f"filing_deadline_days={q12_deadline} does not match Q5.standard_deadline_days={q5_deadline} "
                    f"— cross-round consistency required"
                )
        elif int(data.get("filing_deadline_days", 0)) != 30:
            fails.append(f"filing_deadline_days={data.get('filing_deadline_days')} (expected 30)")

    # C-rule: case_id must exactly match the highest-amount case in open_cases.json
    oc_data, oc_err = _load_json(ws / "cases" / "open_cases.json")
    if oc_err:
        fails.append(f"cannot verify case_id — open_cases.json missing: {oc_err}")
    else:
        oc_cases = oc_data.get("cases", []) if oc_data else []
        eligible = [c for c in oc_cases if float(c.get("amount_usd", 0)) >= 5000]
        if eligible:
            top_case = max(eligible, key=lambda c: float(c.get("amount_usd", 0)))
            expected_cid = top_case.get("case_id")
            got_cid = str(data.get("case_id", ""))
            if expected_cid and got_cid != expected_cid:
                fails.append(
                    f"case_id={got_cid!r} — must be exactly {expected_cid!r} (highest-amount case "
                    f"${float(top_case.get('amount_usd',0)):,.2f} from open_cases.json)"
                )

    # amount_reported >= 5000, exactly 2dp
    amt = data.get("amount_reported")
    if amt is None:
        fails.append("amount_reported is missing")
    else:
        try:
            amt_f = float(amt)
        except (TypeError, ValueError):
            fails.append(f"amount_reported={amt!r} is not a number")
            amt_f = 0
        if amt_f < 5000:
            fails.append(f"amount_reported={amt_f} must be >= 5000 (SAR threshold)")
        parts = f"{amt_f:.10f}".rstrip("0").split(".")
        dp = len(parts[1]) if len(parts) > 1 else 0
        if dp > 2:
            fails.append(f"amount_reported={amt_f} has >2 decimal places (P4)")

    # Narrative five-W structure
    narrative = data.get("narrative") or {}
    if not isinstance(narrative, dict):
        fails.append("narrative must be an object with who/what/when/where/why keys")
    else:
        for w_key in ("who", "what", "when", "where", "why"):
            val = narrative.get(w_key)
            if not val or not str(val).strip():
                fails.append(f"narrative.{w_key} is missing or empty (P3: five-W structure required)")

    if not str(data.get("source_url", "")).strip():
        fails.append("source_url is empty (P5)")

    _finish(fails)
main()
'''

# Q13: VAMP revised after Update-2/supersede
# 加难 C★: vamp_ratio_bps 须精确匹配 Q8 产物（容差 ±0.01 bps，而非原来的 ±1.0）
# 加难 F: 新增 enforcement_date 字段，必须是 "2026-04-01"
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q13_vamp_revised.json")
    if err: _finish([err])

    for k in ("old_threshold_bps", "new_threshold_bps", "vamp_ratio_bps",
               "revised_is_excessive", "update_source", "source_url", "enforcement_date"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    old_t = int(data.get("old_threshold_bps", 0))
    if old_t != 220:
        fails.append(f"old_threshold_bps={old_t} (expected 220 — the superseded DRAFT value)")

    new_t = int(data.get("new_threshold_bps", 0))
    if new_t != 150:
        fails.append(f"new_threshold_bps={new_t} (expected 150 — authoritative after Update-2)")

    # C★ cross-round closure: vamp_ratio_bps must precisely match Q8 output (tolerance ±0.01)
    q8_data, q8_err = _load_json(ws / "output" / "q8_vamp_calc.json")
    if q8_err:
        # Fall back to direct calculation check
        ratio = float(data.get("vamp_ratio_bps", 0))
        expected = (42 + 18) / 3800 * 10000
        if abs(ratio - expected) > 0.01:
            fails.append(f"vamp_ratio_bps={ratio:.4f} (expected {expected:.4f}, tolerance ±0.01 bps)")
    else:
        q8_ratio = float(q8_data.get("vamp_ratio_bps", 0)) if q8_data else 0
        q13_ratio = float(data.get("vamp_ratio_bps", 0))
        if abs(q13_ratio - q8_ratio) > 0.01:
            fails.append(
                f"vamp_ratio_bps={q13_ratio:.4f} does not match Q8.vamp_ratio_bps={q8_ratio:.4f} "
                f"(cross-round closure requires exact match, tolerance ±0.01 bps)"
            )

    if data.get("revised_is_excessive") is not True:
        fails.append(f"revised_is_excessive={data.get('revised_is_excessive')} (expected True)")

    if not str(data.get("update_source", "")).strip():
        fails.append("update_source is empty — must reference Update-2 or the supersede email")

    if not str(data.get("source_url", "")).strip():
        fails.append("source_url is empty (P5)")

    # F-rule: enforcement_date must be exactly "2026-04-01" from the authoritative threshold file
    ed = str(data.get("enforcement_date", "")).strip()
    if ed != "2026-04-01":
        fails.append(f"enforcement_date={ed!r} must be exactly '2026-04-01' (from visa_vamp_thresholds_2026.json)")

    _finish(fails)
main()
'''

# Q14: Re-scored with threshold=0.5 (Update-2 confirms)
# 加难 C★: 新增 q6_threshold_used 字段，必须读取 Q6 产物并精确引用（跨轮闭合）
# 加难 E★: schema_version 静默检查（eval 内置）
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q14_rescored.json")
    if err: _finish([err])

    # E-rule: schema_version silently checked
    if data.get("schema_version") != "1.0":
        fails.append(f"schema_version={data.get('schema_version')!r} must be '1.0'")

    for k in ("threshold_applied", "alerts", "changed_decisions", "consistency_note",
               "q6_threshold_used"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    t = float(data.get("threshold_applied", 0))
    if abs(t - 0.5) > 0.01:
        fails.append(f"threshold_applied={t} (must be 0.5 — Update-2 confirmed 0.5; do not use 0.3)")

    alerts = data.get("alerts") or []
    if len(alerts) != 3:
        fails.append(f"expected exactly 3 alerts, got {len(alerts)}")

    q14_lookup = {}
    for a in alerts:
        q14_lookup[str(a.get("alert_id", ""))] = str(a.get("decision", "")).upper()

    EXPECTED = {
        "ALRT-20260301-0001": "FRAUD",
        "ALRT-20260301-0005": "LEGITIMATE",
        "ALRT-20260301-0009": "FRAUD",
    }
    for alrt_id, exp_dec in EXPECTED.items():
        dec = q14_lookup.get(alrt_id)
        if dec is None:
            fails.append(f"alert {alrt_id} missing from Q14 alerts list")
        elif dec != exp_dec:
            fails.append(f"{alrt_id}: Q14 decision={dec!r} (expected {exp_dec!r} at threshold=0.5)")

    # C★ cross-round closure: Q14 decisions must match Q6 decisions exactly
    q6_data, q6_err = _load_json(ws / "output" / "q6_risk_scores.json")
    if q6_err:
        fails.append(f"cannot verify cross-round consistency — Q6 output missing: {q6_err}")
    else:
        q6_alerts = q6_data.get("alerts") or q6_data.get("scores") or []
        q6_lookup = {}
        for a in q6_alerts:
            q6_lookup[str(a.get("alert_id", ""))] = str(a.get("decision", "")).upper()
        for alrt_id in EXPECTED:
            q6_dec = q6_lookup.get(alrt_id)
            q14_dec = q14_lookup.get(alrt_id)
            if q6_dec and q14_dec and q6_dec != q14_dec:
                fails.append(
                    f"cross-round inconsistency: {alrt_id} Q6={q6_dec!r} vs Q14={q14_dec!r} — "
                    "both use threshold=0.5 so decisions must be identical"
                )

    # C★ q6_threshold_used must match actual Q6 threshold (cross-round field reference)
    q6_threshold_in_q14 = data.get("q6_threshold_used")
    if q6_threshold_in_q14 is None:
        fails.append("q6_threshold_used is missing — must state the threshold Q6 actually used")
    else:
        try:
            q6t = float(q6_threshold_in_q14)
        except (TypeError, ValueError):
            q6t = -1
        if abs(q6t - 0.5) > 0.01:
            fails.append(f"q6_threshold_used={q6_threshold_in_q14} (Q6 used 0.5; this field must reflect actual Q6 threshold)")
        # Also verify it matches Q6 output
        if not q6_err and q6_data:
            q6_alerts_list = q6_data.get("alerts") or []
            q6_ts = set()
            for a in q6_alerts_list:
                t_val = a.get("threshold_used")
                if t_val is not None:
                    q6_ts.add(float(t_val))
            top_t = q6_data.get("threshold_used")
            if top_t is not None:
                q6_ts.add(float(top_t))
            if q6_ts and abs(q6t - list(q6_ts)[0]) > 0.01:
                fails.append(
                    f"q6_threshold_used={q6t} does not match Q6 output threshold {list(q6_ts)[0]} "
                    f"— must read Q6 output, not assume"
                )

    cd = data.get("changed_decisions")
    if not isinstance(cd, list):
        fails.append(f"changed_decisions must be a list (may be empty), got {type(cd).__name__}")

    cn = str(data.get("consistency_note", "")).strip()
    if not cn:
        fails.append("consistency_note is missing or empty")
    else:
        if "0.5" not in cn:
            fails.append(f"consistency_note must reference threshold '0.5'; got: {cn[:100]!r}")
        if "Q6" not in cn and "q6" not in cn:
            fails.append(f"consistency_note must reference 'Q6' to explain cross-round consistency; got: {cn[:100]!r}")

    _finish(fails)
main()
'''

# Q15: Weekly report
# 加难 C★: vamp_ratio_bps 精确匹配 Q8（容差 ±0.01）；mc_program_tier 精确匹配 Q11
# 加难 F: 新增必填字段 investigation_period_days (int=17) + total_sar_amount_usd
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q15_weekly_report.json")
    if err: _finish([err])

    for k in ("total_alerts_batch001", "total_alerts_batch002", "vamp_ratio_bps",
               "vamp_threshold_bps", "vamp_status", "mc_program_tier",
               "sar_to_file_count", "source_url", "report_period",
               "investigation_period_days"):
        if k not in data:
            fails.append(f"missing key: {k}")
    if fails: _finish(fails)

    rp = str(data.get("report_period", "")).strip()
    if rp != "2026-03-01 to 2026-03-17":
        fails.append(f"report_period={rp!r} (expected exactly '2026-03-01 to 2026-03-17')")

    if int(data.get("total_alerts_batch001", -1)) != 200:
        fails.append(f"total_alerts_batch001={data.get('total_alerts_batch001')} (expected 200)")
    if int(data.get("total_alerts_batch002", -1)) != 350:
        fails.append(f"total_alerts_batch002={data.get('total_alerts_batch002')} (expected 350)")

    # F-rule: investigation_period_days must be exactly 17 (2026-03-01 to 2026-03-17 inclusive)
    ipd = data.get("investigation_period_days")
    try:
        ipd_int = int(ipd)
    except (TypeError, ValueError):
        ipd_int = -1
    if ipd_int != 17:
        fails.append(f"investigation_period_days={ipd} (expected 17 — calendar days from 2026-03-01 to 2026-03-17 inclusive)")

    # C★ cross-round closure: vamp_ratio_bps must precisely match Q8 (tolerance ±0.01)
    q8_data, q8_err = _load_json(ws / "output" / "q8_vamp_calc.json")
    if q8_err:
        ratio = float(data.get("vamp_ratio_bps", 0))
        expected = (42 + 18) / 3800 * 10000
        if abs(ratio - expected) > 0.01:
            fails.append(f"vamp_ratio_bps={ratio:.4f} (expected {expected:.4f}, tolerance ±0.01 bps)")
    else:
        q8_ratio = float(q8_data.get("vamp_ratio_bps", 0)) if q8_data else 0
        q15_ratio = float(data.get("vamp_ratio_bps", 0))
        if abs(q15_ratio - q8_ratio) > 0.01:
            fails.append(
                f"vamp_ratio_bps={q15_ratio:.4f} does not match Q8.vamp_ratio_bps={q8_ratio:.4f} "
                f"(cross-round closure, tolerance ±0.01 bps)"
            )

    # vamp_ratio_bps must be exactly 2dp
    ratio_val = data.get("vamp_ratio_bps", 0)
    ratio_str = str(ratio_val)
    if "." in ratio_str:
        dp = len(ratio_str.split(".")[1])
        if dp > 2:
            fails.append(f"vamp_ratio_bps={ratio_str} has >2 decimal places (P4)")

    thr = int(data.get("vamp_threshold_bps", 0))
    if thr == 220:
        fails.append("vamp_threshold_bps=220 — Update-2 superseded this; must use 150")
    elif thr != 150:
        fails.append(f"vamp_threshold_bps={thr} (expected 150)")

    status = str(data.get("vamp_status", "")).upper()
    if status not in ("EXCESSIVE", "COMPLIANT"):
        fails.append(f"vamp_status={status!r} must be 'EXCESSIVE' or 'COMPLIANT'")
    if status != "EXCESSIVE":
        fails.append(f"vamp_status={status!r} — 157.89 bps > 150 bps threshold → should be EXCESSIVE")

    # C★ cross-round closure: mc_program_tier must exactly match Q11.program_tier
    q11_data, q11_err = _load_json(ws / "output" / "q11_mc_compliance.json")
    if q11_err:
        tier = str(data.get("mc_program_tier", "")).strip()
        if tier.upper() != "ECM":
            fails.append(f"mc_program_tier={tier!r} (expected 'ECM' per Q11)")
    else:
        q11_tier = str(q11_data.get("program_tier", "")).strip() if q11_data else ""
        q15_tier = str(data.get("mc_program_tier", "")).strip()
        if q11_tier and q15_tier.upper() != q11_tier.upper():
            fails.append(
                f"mc_program_tier={q15_tier!r} must exactly match Q11.program_tier={q11_tier!r} (cross-round consistency)"
            )
        if q15_tier.upper() != "ECM":
            fails.append(f"mc_program_tier={q15_tier!r} (expected 'ECM' per Q11)")

    sar_count = data.get("sar_to_file_count")
    try:
        sar_count_int = int(sar_count)
    except (TypeError, ValueError):
        sar_count_int = -1
    ocu_path = ws / "cases" / "open_cases_updated.json"
    if ocu_path.exists():
        import json as _json
        ocu = _json.loads(ocu_path.read_text(encoding="utf-8"))
        true_count = sum(1 for c in ocu.get("cases", []) if c.get("sar_required", False))
        if sar_count_int != true_count:
            fails.append(
                f"sar_to_file_count={sar_count_int} but open_cases_updated.json has {true_count} "
                f"sar_required=true cases — must match exactly"
            )
    else:
        if sar_count_int <= 0:
            fails.append(f"sar_to_file_count={sar_count_int} (expected a positive integer)")

    if not str(data.get("source_url", "")).strip():
        fails.append("source_url is empty (P5)")

    _finish(fails)
main()
'''

# Q16: SAR deadlines
# 加难 C★: sar_deadline_days 须与 Q5.standard_deadline_days 精确一致（跨轮）
# 加难 F: 每个 case 须有 sar_form_number="FinCEN Form 111"
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q16_sar_deadlines.json")
    if err: _finish([err])

    if "sar_deadline_days" not in data:
        fails.append("missing key: sar_deadline_days")
    if "source_url" not in data:
        fails.append("missing key: source_url")
    if fails: _finish(fails)

    # C★ cross-round closure: sar_deadline_days must match Q5.standard_deadline_days exactly
    q5_data, q5_err = _load_json(ws / "output" / "q5_sar_structure.json")
    if q5_err:
        fails.append(f"cannot verify cross-round deadline — Q5 output missing: {q5_err}")
        if int(data.get("sar_deadline_days", 0)) != 30:
            fails.append(f"sar_deadline_days={data.get('sar_deadline_days')} (expected 30 per FinCEN)")
    else:
        q5_std = q5_data.get("standard_deadline_days") if q5_data else None
        q16_days = data.get("sar_deadline_days")
        if q5_std is not None and q16_days is not None:
            if int(q16_days) != int(q5_std):
                fails.append(
                    f"sar_deadline_days={q16_days} does not match Q5.standard_deadline_days={q5_std} "
                    f"— cross-round closure required"
                )
        elif int(data.get("sar_deadline_days", 0)) != 30:
            fails.append(f"sar_deadline_days={data.get('sar_deadline_days')} (expected 30 per FinCEN)")

    if not str(data.get("source_url", "")).strip():
        fails.append("source_url is empty (P5)")

    cases = data.get("cases") or data.get("sar_cases") or []
    if not isinstance(cases, list):
        fails.append("no cases list in q16_sar_deadlines.json")
        _finish(fails)

    if len(cases) == 0:
        fails.append("sar_deadlines has no cases (expected ≥1 sar_required=true case)")

    for i, case in enumerate(cases[:20]):
        cid = str(case.get("case_id", ""))
        if not re.fullmatch(r"CASE-\\d{8}-\\d{3}", cid):
            fails.append(f"case[{i}].case_id {cid!r} does not match CASE-YYYYMMDD-NNN (P2)")

        amt = case.get("amount_usd")
        if amt is not None:
            parts = f"{float(amt):.10f}".rstrip("0").split(".")
            dp = len(parts[1]) if len(parts) > 1 else 0
            if dp > 2:
                fails.append(f"case[{i}].amount_usd={amt} has >2 decimal places (P4)")

        det = case.get("detection_date") or case.get("detected_date")
        dl = case.get("deadline_date") or case.get("sar_filing_deadline")
        if det and dl:
            try:
                det_d = date.fromisoformat(str(det)[:10])
                dl_d = date.fromisoformat(str(dl)[:10])
                expected_dl = det_d + timedelta(days=30)
                if dl_d != expected_dl:
                    fails.append(f"case[{i}] deadline_date={dl_d} != detection_date({det_d})+30={expected_dl}")
            except ValueError:
                fails.append(f"case[{i}] invalid date format: detection={det!r}, deadline={dl!r}")

        ns = str(case.get("narrative_structure", "")).lower()
        if not any(kw in ns for kw in ("five", "5w", "who", "what", "when", "where", "why")):
            fails.append(f"case[{i}].narrative_structure does not reference five-W framework (P3)")

        # F-rule: each case must have sar_form_number="FinCEN Form 111" (verbatim, from Q5)
        sfn = str(case.get("sar_form_number", "")).strip()
        if not sfn:
            fails.append(f"case[{i}].sar_form_number is missing — must be 'FinCEN Form 111'")
        elif sfn != "FinCEN Form 111":
            fails.append(f"case[{i}].sar_form_number={sfn!r} must be exactly 'FinCEN Form 111' (verbatim from Q5)")

    _finish(fails)
main()
'''

# Q17: Bash-sha256 sign-off (V7)
CHECKS["check_q17"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign_path = ws / "output" / "q17_signoff.txt"
    if not sign_path.exists():
        _finish(["file not found: output/q17_signoff.txt"])

    content = sign_path.read_text(encoding="utf-8").strip()

    if not content.startswith("VERIFIED:"):
        fails.append(f"q17_signoff.txt must start with 'VERIFIED:' (got {content[:30]!r})")
        _finish(fails)

    hexpart = content[len("VERIFIED:"):].strip()
    if not re.fullmatch(r"[0-9a-f]{64}", hexpart):
        fails.append(f"SHA-256 portion is not 64 lowercase hex chars: {hexpart!r}")
        _finish(fails)

    script_path = ws / "scripts" / "compute_vamp_ratio.py"
    if not script_path.exists():
        fails.append("scripts/compute_vamp_ratio.py not found — cannot verify hash")
        _finish(fails)

    try:
        result = subprocess.run(
            ["python", str(script_path), "--tc40", "42", "--tc15", "18", "--tc05", "3800",
             "--merchant-id", "MERCH-A"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            fails.append(f"compute_vamp_ratio.py exited {result.returncode}: {result.stderr[:200]}")
            _finish(fails)
        script_output = result.stdout
        script_output_stripped = script_output.rstrip("\\n")
        expected_hash = hashlib.sha256(script_output_stripped.encode("utf-8")).hexdigest()
        if hexpart.lower() != expected_hash.lower():
            expected_hash2 = hashlib.sha256(script_output.encode("utf-8")).hexdigest()
            if hexpart.lower() != expected_hash2.lower():
                fails.append(
                    f"SHA-256 mismatch: got {hexpart[:16]}... expected {expected_hash[:16]}... "
                    f"(hash of compute_vamp_ratio.py output with TC40=42/TC15=18/TC05=3800)"
                )
    except subprocess.TimeoutExpired:
        fails.append("compute_vamp_ratio.py timed out (>15s)")
    except Exception as e:
        fails.append(f"error running compute_vamp_ratio.py: {e}")

    _finish(fails)
main()
'''

# Preferences check
PREFS = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_preferences.py — sec5 preference rule checker.

Usage:
    python check_preferences.py <workspace> --rules P1,P2 --target output/foo.json
    python check_preferences.py <workspace> --rules P1 --target path/to/file.py

P1: every output JSON includes top-level schema_version="1.0"
P2: case IDs follow CASE-YYYYMMDD-NNN format
P3: SAR narrative has who/what/when/where/why five-W structure
P4: all amount_usd fields formatted to exactly 2 decimal places
P5: regulatory threshold citations include source_url field
"""
import sys, json, re, argparse
from pathlib import Path


def check_p1(ws: Path, target: str) -> list[str]:
    """P1: output JSON has top-level schema_version='1.0'."""
    fails = []
    p = ws / target
    if not p.exists():
        return [f"P1: file not found: {target}"]
    if not target.endswith(".json"):
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"P1: invalid JSON in {target}: {e}"]
    sv = data.get("schema_version")
    if sv != "1.0":
        fails.append(f"P1: schema_version={sv!r} (expected '1.0') in {target}")
    return fails


def check_p2(ws: Path, target: str) -> list[str]:
    """P2: case IDs in JSON follow CASE-YYYYMMDD-NNN pattern."""
    fails = []
    p = ws / target
    if not p.exists():
        return []
    if not target.endswith(".json"):
        return []
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        return []
    found_ids = re.findall(r'"case_id"\\s*:\\s*"([^"]+)"', text)
    for cid in found_ids:
        if not re.fullmatch(r"CASE-\\d{8}-\\d{3}", cid):
            fails.append(f"P2: case_id {cid!r} in {target} does not match CASE-YYYYMMDD-NNN")
    return fails


def check_p3(ws: Path, target: str) -> list[str]:
    """P3: SAR narrative has five-W structure."""
    fails = []
    p = ws / target
    if not p.exists():
        return []
    if not target.endswith(".json"):
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []
    narrative = data.get("narrative") or data.get("five_ws")
    if narrative is None:
        return []
    if not isinstance(narrative, dict):
        return [f"P3: narrative/five_ws must be a dict in {target}"]
    for w_key in ("who", "what", "when", "where", "why"):
        if not str(narrative.get(w_key, "")).strip():
            fails.append(f"P3: narrative.{w_key} missing or empty in {target} (five-W structure required)")
    return fails


def check_p4(ws: Path, target: str) -> list[str]:
    """P4: amount fields in JSON have exactly 2 decimal places."""
    fails = []
    p = ws / target
    if not p.exists():
        return []
    if not target.endswith(".json"):
        return []
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        return []
    amt_pattern = re.compile(r'"(?:amount_usd|amount_reported|vamp_ratio_bps|chargeback_ratio_bps)"\\s*:\\s*([\\d.]+)')
    for m in amt_pattern.finditer(text):
        val_str = m.group(1)
        try:
            val_f = float(val_str)
        except ValueError:
            continue
        if "." in val_str:
            dp = len(val_str.split(".")[1])
            if dp > 2:
                fails.append(f"P4: field value {val_str} in {target} has >2 decimal places")
    return fails


def check_p5(ws: Path, target: str) -> list[str]:
    """P5: regulatory threshold references include source_url."""
    fails = []
    p = ws / target
    if not p.exists():
        return []
    if not target.endswith(".json"):
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []
    threshold_keys = {"threshold_bps", "vamp_threshold_bps", "chargeback_ratio_bps",
                      "filing_deadline_days", "filing_threshold_usd", "mc_program_tier"}
    has_threshold = any(k in data for k in threshold_keys)
    if not has_threshold:
        return []
    su = str(data.get("source_url", "")).strip()
    if not su:
        fails.append(f"P5: source_url missing in {target} (regulatory threshold citations require source_url)")
    return fails


RULE_MAP = {
    "P1": check_p1,
    "P2": check_p2,
    "P3": check_p3,
    "P4": check_p4,
    "P5": check_p5,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    parser.add_argument("--rules", required=True, help="Comma-separated rule IDs, e.g. P1,P2")
    parser.add_argument("--target", required=True, help="Relative path to file within workspace")
    args = parser.parse_args()

    ws = Path(args.workspace)
    rules = [r.strip() for r in args.rules.split(",")]
    fails = []
    for rule in rules:
        fn = RULE_MAP.get(rule)
        if fn is None:
            continue
        fails.extend(fn(ws, args.target))

    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
'''


def write_check(name: str, body: str) -> Path:
    p = OUT / f"{name}.py"
    src = HEADER + textwrap.dedent(body)
    p.write_text(src, encoding="utf-8")
    return p


def main() -> None:
    for name, body in CHECKS.items():
        p = write_check(name, body)
        print(f"  wrote {p}")

    # Preferences
    (OUT / "check_preferences.py").write_text(PREFS, encoding="utf-8")
    print(f"  wrote {OUT / 'check_preferences.py'}")

    print(f"\nAll {len(CHECKS) + 1} check scripts written to {OUT}")


if __name__ == "__main__":
    main()
