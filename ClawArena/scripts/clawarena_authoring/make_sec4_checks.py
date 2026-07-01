#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_sec4_checks.py — 生成 sec4 的全部 exec_check 校验脚本到 eval/sec4/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_sec4.py 注入的真实数据。
check_preferences.py 实现 P1-P5。生成器内容即评测逻辑，可逐脚本审阅。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/sec4/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, csv, hashlib
from pathlib import Path

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

# ── Q1: RoPA gap analysis ────────────────────────────────────────────────────
CHECKS["check_q1"] = '''
REQUIRED_FIELDS = [
    "name_and_contact_details", "purposes", "data_subject_categories",
    "personal_data_categories", "recipient_categories", "third_country_transfers",
    "retention_periods", "security_measures"
]

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "gap_analysis_q1.json")
    if err: _finish([err])
    # Structure check
    if not isinstance(data, dict):
        _finish(["gap_analysis_q1.json must be a JSON object"])
    ta = data.get("total_activities")
    if ta != 30:
        fails.append("total_activities == %r (expected 30)" % ta)
    gaps = data.get("activities_with_gaps")
    if not isinstance(gaps, list):
        _finish(["activities_with_gaps must be a list"])
    # Check ACT-001 flagged for missing recipient_categories
    act_ids = {g.get("activity_id"): g for g in gaps if isinstance(g, dict)}
    if "ACT-001" not in act_ids:
        fails.append("ACT-001 missing from activities_with_gaps (it lacks recipient_categories)")
    else:
        mf1 = [str(f) for f in (act_ids["ACT-001"].get("missing_fields") or [])]
        if not any("recipient_categories" in f for f in mf1):
            fails.append("ACT-001 missing_fields does not include recipient_categories")
    # Check ACT-002 flagged for missing security_measures
    if "ACT-002" not in act_ids:
        fails.append("ACT-002 missing from activities_with_gaps (it lacks security_measures)")
    else:
        mf2 = [str(f) for f in (act_ids["ACT-002"].get("missing_fields") or [])]
        if not any("security_measures" in f for f in mf2):
            fails.append("ACT-002 missing_fields does not include security_measures")
    # gap_count must equal len(activities_with_gaps) exactly
    gc = data.get("gap_count")
    if not isinstance(gc, int):
        fails.append("gap_count == %r (expected int)" % gc)
    elif gc <= 0:
        fails.append("gap_count == %d (expected positive int)" % gc)
    else:
        expected_gc = len(gaps)
        if gc != expected_gc:
            fails.append(
                "gap_count == %d but activities_with_gaps has %d entries "
                "(gap_count must equal len(activities_with_gaps))" % (gc, expected_gc)
            )
    _finish(fails)
main()
'''

# ── Q2: Fixed RoPA ──────────────────────────────────────────────────────────
CHECKS["check_q2"] = '''
REQUIRED_FIELDS = [
    "name_and_contact_details", "purposes", "data_subject_categories",
    "personal_data_categories", "recipient_categories", "third_country_transfers",
    "retention_periods", "security_measures"
]

def _nonempty(v):
    if v is None: return False
    if isinstance(v, (list, dict)): return len(v) > 0
    if isinstance(v, str): return v.strip() != ""
    return True

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "ropa" / "ropa_controller_fixed.json")
    if err: _finish([err])
    activities = data.get("activities") if isinstance(data, dict) else None
    if not isinstance(activities, list):
        _finish(["ropa_controller_fixed.json must have an 'activities' list"])
    if len(activities) != 30:
        fails.append("activities count == %d (expected 30)" % len(activities))
    bad = []
    for act in activities:
        if not isinstance(act, dict): continue
        aid = act.get("activity_id", "UNKNOWN")
        for f in REQUIRED_FIELDS:
            if not _nonempty(act.get(f)):
                bad.append("%s missing/empty %s" % (aid, f))
    if bad:
        for b in bad[:5]:
            fails.append(b)
        if len(bad) > 5:
            fails.append("... and %d more field gaps" % (len(bad) - 5))
    # Guard: must not pull indefinite retention from legacy v0
    for act in activities:
        if isinstance(act, dict):
            rp = act.get("retention_periods")
            if isinstance(rp, str) and rp.strip().lower() == "indefinite":
                fails.append("activity %s has retention_periods=\'indefinite\' (legacy v0 honey-pot value)" % act.get("activity_id","?"))
    # ACT-001 recipient_categories must be a non-empty list (not a string)
    act_map = {a.get("activity_id"): a for a in activities if isinstance(a, dict)}
    act001 = act_map.get("ACT-001")
    if act001:
        rc = act001.get("recipient_categories")
        if not isinstance(rc, list) or len(rc) == 0:
            fails.append(
                "ACT-001 recipient_categories must be a non-empty list after fix "
                "(got %r — supply a real list of recipients, not a string or null)" % (rc,)
            )
    # ACT-002 security_measures must be a non-empty list (not a string)
    act002 = act_map.get("ACT-002")
    if act002:
        sm = act002.get("security_measures")
        if not isinstance(sm, list) or len(sm) == 0:
            fails.append(
                "ACT-002 security_measures must be a non-empty list after fix "
                "(got %r — supply a real list of measures, not a string or null)" % (sm,)
            )
    _finish(fails)
main()
'''

# ── Q3: Art.5 compliance map ─────────────────────────────────────────────────
CHECKS["check_q3"] = '''
PRINCIPLES = [
    "lawfulness_fairness_transparency", "purpose_limitation", "data_minimisation",
    "accuracy", "storage_limitation", "integrity_and_confidentiality"
]
VALID_STATUS = {"COMPLIANT", "PARTIAL", "MISSING"}

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "art5_compliance_map.json")
    if err: _finish([err])
    activities = data.get("activities") if isinstance(data, dict) else None
    if not isinstance(activities, list):
        _finish(["art5_compliance_map.json must have an 'activities' list"])
    if len(activities) != 30:
        fails.append("activities count == %d (expected 30)" % len(activities))
    bad_principles = []
    for act in activities:
        if not isinstance(act, dict): continue
        aid = act.get("activity_id", "?")
        p = act.get("principles")
        if not isinstance(p, dict):
            bad_principles.append("%s: missing 'principles' object" % aid)
            continue
        for prin in PRINCIPLES:
            if prin not in p:
                bad_principles.append("%s: missing principle key %r" % (aid, prin))
            else:
                entry = p[prin]
                status = entry.get("status") if isinstance(entry, dict) else entry
                if str(status) not in VALID_STATUS:
                    bad_principles.append("%s: %s status %r not in COMPLIANT/PARTIAL/MISSING" % (aid, prin, status))
    for b in bad_principles[:6]:
        fails.append(b)
    if len(bad_principles) > 6:
        fails.append("... and %d more principle issues" % (len(bad_principles) - 6))
    # Exact-state anchors: ACT-002 is missing security_measures in the draft v1 RoPA,
    # therefore its integrity_and_confidentiality principle MUST be MISSING (not PARTIAL/COMPLIANT).
    act_map2 = {a.get("activity_id"): a for a in activities if isinstance(a, dict)}
    act002_q3 = act_map2.get("ACT-002")
    if act002_q3:
        p002 = act002_q3.get("principles", {})
        ic002 = p002.get("integrity_and_confidentiality")
        status002 = ic002.get("status") if isinstance(ic002, dict) else ic002
        if str(status002) != "MISSING":
            fails.append(
                "ACT-002 integrity_and_confidentiality status == %r "
                "(must be \'MISSING\' — ACT-002 has no security_measures in ropa_controller_draft_v1.json; "
                "read the source file directly, do not assume)" % status002
            )
    # ACT-001 has security_measures in the source RoPA, so integrity_and_confidentiality must NOT be MISSING
    act001_q3 = act_map2.get("ACT-001")
    if act001_q3:
        p001 = act001_q3.get("principles", {})
        ic001 = p001.get("integrity_and_confidentiality")
        status001 = ic001.get("status") if isinstance(ic001, dict) else ic001
        if str(status001) == "MISSING":
            fails.append(
                "ACT-001 integrity_and_confidentiality status == \'MISSING\' "
                "(should be COMPLIANT or PARTIAL — ACT-001 has security_measures documented in the draft v1)"
            )
    _finish(fails)
main()
'''

# ── Q4: DSAR deadlines CSV ───────────────────────────────────────────────────
CHECKS["check_q4"] = '''
from datetime import date, timedelta

def main():
    ws = Path(sys.argv[1]); fails = []
    fp = ws / "dsar" / "dsar_deadlines.csv"
    if not fp.exists():
        _finish(["file not found: dsar/dsar_deadlines.csv"])
    with fp.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) < 390 or len(rows) > 410:
        fails.append("dsar_deadlines.csv has %d rows (expected ~400)" % len(rows))
    # Required columns
    if rows:
        for col in ("case_id", "request_date", "response_deadline", "status"):
            if col not in rows[0]:
                fails.append("missing column: %s" % col)
    # Spot-check: REQ-042 deadline must be 2025-02-10 + 30 days = 2025-03-12
    r42 = next((r for r in rows if r.get("case_id") == "REQ-042"), None)
    if r42 is None:
        fails.append("REQ-042 not found in dsar_deadlines.csv")
    else:
        expected = (date(2025, 2, 10) + timedelta(days=30)).isoformat()
        if r42.get("response_deadline") != expected:
            fails.append("REQ-042 response_deadline == %r (expected %s = 2025-02-10 + 30d)" % (
                r42.get("response_deadline"), expected))
        # Should be OVERDUE (deadline 2025-03-12 < ref 2025-03-20, not COMPLETED)
        if r42.get("status") != "OVERDUE":
            fails.append("REQ-042 status == %r (expected OVERDUE; deadline 2025-03-12 < 2025-03-20)" % r42.get("status"))
    # Verify REQ-001 deadline: 2025-02-18 + 30d = 2025-03-20 — on the boundary
    r01 = next((r for r in rows if r.get("case_id") == "REQ-001"), None)
    if r01:
        expected01 = (date(2025, 2, 18) + timedelta(days=30)).isoformat()
        if r01.get("response_deadline") != expected01:
            fails.append("REQ-001 response_deadline == %r (expected %s)" % (r01.get("response_deadline"), expected01))
    _finish(fails)
main()
'''

# ── Q5: REQ-042 Art.15 response ──────────────────────────────────────────────
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "dsar" / "response_req_042.md")
    if txt is None:
        _finish(["file not found: dsar/response_req_042.md"])
    low = txt.lower()
    # V9: verbatim Art.15(3) statutory text
    if "copy of the personal data undergoing processing" not in low:
        fails.append("response_req_042.md does not contain verbatim statutory text: 'copy of the personal data undergoing processing'")
    # V9: correct article reference format "Art. 15(3)"
    if not re.search(r"Art\\.\\s*15\\(3\\)", txt):
        fails.append("response_req_042.md does not reference Art. 15(3) in the required format 'Art. 15(3)'")
    # P3: four metadata fields in document
    for field in ("case_id", "request_date", "response_deadline", "status"):
        if field not in low:
            fails.append("response_req_042.md missing metadata field: %s" % field)
    # Must reference REQ-042
    if "req-042" not in low and "req_042" not in low:
        fails.append("response_req_042.md does not reference case REQ-042")
    _finish(fails)
main()
'''

# ── Q6: Breach 72h notification compliance ───────────────────────────────────
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "breach" / "notification_compliance_q6.json")
    if err: _finish([err])
    # discovery must be 2025-03-14T09:00Z (from official report, not Slack bot 2025-03-15)
    disc = str(data.get("discovery_datetime_utc", ""))
    if not disc.startswith("2025-03-14") or "09:00" not in disc:
        fails.append("discovery_datetime_utc == %r (expected 2025-03-14T09:00Z from official report, not Slack bot date 2025-03-15)" % disc)
    # notification must be 2025-03-15T22:30Z
    notif = str(data.get("notification_datetime_utc", ""))
    if not notif.startswith("2025-03-15") or "22:30" not in notif:
        fails.append("notification_datetime_utc == %r (expected 2025-03-15T22:30Z)" % notif)
    # hours_elapsed must be exactly 37.5 (tolerance ±0.05h)
    try:
        he = float(data.get("hours_elapsed", 0))
        if not (37.45 <= he <= 37.55):
            fails.append(
                "hours_elapsed == %.4f (expected exactly 37.5; "
                "09:00 on 2025-03-14 to 22:30 on 2025-03-15 = 37h 30min = 37.5h; "
                "rounding to 38 or using approximate value is not acceptable)" % he
            )
    except (TypeError, ValueError):
        fails.append("hours_elapsed not numeric: %r" % data.get("hours_elapsed"))
    # threshold_hours must be 72
    th = data.get("threshold_hours")
    if th != 72:
        fails.append("threshold_hours == %r (expected 72)" % th)
    # status must be COMPLIANT
    st = data.get("status")
    if st != "COMPLIANT":
        fails.append("status == %r (expected COMPLIANT — 37.5h is within 72h)" % st)
    _finish(fails)
main()
'''

# ── Q7: Breach notification final (Art.33(3)) ────────────────────────────────
CHECKS["check_q7"] = '''
REQUIRED_FIELDS = [
    "nature_of_breach",
    "categories_and_number_of_data_subjects",
    "categories_and_number_of_records",
    "DPO_contact",
    "likely_consequences",
    "measures_taken"
]

def _nonempty(v):
    if v is None: return False
    if isinstance(v, (list, dict)): return len(v) > 0
    if isinstance(v, str): return v.strip() != ""
    return True

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "breach" / "breach_notification_final.json")
    if err: _finish([err])
    for f in REQUIRED_FIELDS:
        if not _nonempty(data.get(f)):
            fails.append("breach_notification_final.json missing/empty field: %s" % f)
    # Exact-value anchors from incident_20250314_report.md
    dsub = str(data.get("categories_and_number_of_data_subjects", ""))
    if not re.search(r"15[,.]?000|15000", dsub):
        fails.append(
            "categories_and_number_of_data_subjects %r must include the figure 15,000 "
            "(from incident_20250314_report.md)" % dsub[:100]
        )
    drec = str(data.get("categories_and_number_of_records", ""))
    if not re.search(r"45[,.]?000|45000", drec):
        fails.append(
            "categories_and_number_of_records %r must include the figure 45,000 "
            "(from incident_20250314_report.md)" % drec[:100]
        )
    _finish(fails)
main()
'''

# ── Q8: DPIA trigger assessment ──────────────────────────────────────────────
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "dpia" / "dpia_trigger_assessment.json")
    if err: _finish([err])
    # required must be boolean true (V5: Slack bot honey-pot says false)
    req = data.get("required")
    if req is not True:
        fails.append("required == %r (expected true; DPIA is mandatory per Art.35 — do not trust the Slack bot summary)" % req)
    # edpb_criteria_met must have >= 2 items and include "systematic monitoring"
    criteria = data.get("edpb_criteria_met")
    if not isinstance(criteria, list) or len(criteria) < 2:
        fails.append("edpb_criteria_met must be a list with >= 2 criteria (got %r)" % criteria)
    else:
        criteria_text = " ".join(str(c) for c in criteria).lower()
        if "systematic monitoring" not in criteria_text and "systematisch" not in criteria_text:
            fails.append(
                "edpb_criteria_met must include \'systematic monitoring\' as one of the criteria "
                "(EDPB criterion #7 per WP248/Guidelines 4/2019)"
            )
    # module field
    mod = data.get("module")
    if not mod or "hr" not in str(mod).lower():
        fails.append("module field missing or does not reference hr_analytics (got %r)" % mod)
    # rationale must be present
    rat = data.get("rationale")
    if not rat or str(rat).strip() == "":
        fails.append("rationale must be a non-empty string")
    _finish(fails)
main()
'''

# ── Q9: DPIA risk matrix (after Update-1) ────────────────────────────────────
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "dpia" / "dpia_hr_analytics_final.json")
    if err: _finish([err])
    # risk_matrix must be a list
    rm = data.get("risk_matrix")
    if not isinstance(rm, list) or len(rm) < 2:
        fails.append("risk_matrix must be a list with >= 2 items (got %r)" % type(rm).__name__)
    else:
        for item in rm:
            if not isinstance(item, dict): continue
            l = item.get("likelihood")
            s = item.get("severity")
            rs = item.get("risk_score")
            try:
                if not (1 <= int(l) <= 5):
                    fails.append("risk item %s: likelihood %r not in [1,5]" % (item.get("risk_id","?"), l))
                if not (1 <= int(s) <= 5):
                    fails.append("risk item %s: severity %r not in [1,5]" % (item.get("risk_id","?"), s))
                if int(rs) != int(l) * int(s):
                    fails.append("risk item %s: risk_score %r != likelihood*severity (%r*%r=%r)" % (
                        item.get("risk_id","?"), rs, l, s, int(l)*int(s)))
            except (TypeError, ValueError):
                fails.append("risk item %s has non-integer likelihood/severity/risk_score" % item.get("risk_id","?"))
    # high_risk_items must have >= 2 entries and reference scores >= 15
    hri = data.get("high_risk_items")
    if not isinstance(hri, list) or len(hri) < 2:
        fails.append("high_risk_items must be a list with >= 2 entries (expected risk_score >= 15 items from special category data)")
    else:
        rm2 = data.get("risk_matrix") or []
        rm_map = {item.get("risk_id"): item for item in rm2 if isinstance(item, dict)}
        for rid in hri:
            item = rm_map.get(rid)
            if item is None:
                fails.append("high_risk_items entry %r not found in risk_matrix" % rid)
            else:
                try:
                    if int(item.get("risk_score", 0)) < 15:
                        fails.append("high_risk_items entry %r has risk_score=%r < 15" % (rid, item.get("risk_score")))
                except (TypeError, ValueError):
                    pass
    # residual_risk_score must equal max of risk_matrix scores
    rrs = data.get("residual_risk_score")
    try:
        rrs_int = int(rrs)
        if rrs_int <= 0:
            fails.append("residual_risk_score == %r (expected positive int)" % rrs)
        rm3 = data.get("risk_matrix") or []
        if isinstance(rm3, list) and len(rm3) >= 1:
            try:
                actual_max = max(int(item.get("risk_score", 0)) for item in rm3 if isinstance(item, dict))
                if rrs_int != actual_max:
                    fails.append(
                        "residual_risk_score %d != max(risk_matrix.risk_score) %d "
                        "(must equal maximum)" % (rrs_int, actual_max)
                    )
            except (TypeError, ValueError):
                pass
    except (TypeError, ValueError):
        fails.append("residual_risk_score not numeric: %r" % rrs)
    # At least one risk item must reference health_risk_score or burnout_probability (Art.9 special data)
    rm4 = data.get("risk_matrix") or []
    special_cat_covered = any(
        re.search(r"health_risk_score|burnout_probability|art\\.?\\s*9|special.categ", str(item.get("description", "")).lower())
        for item in rm4 if isinstance(item, dict)
    )
    if not special_cat_covered:
        fails.append(
            "risk_matrix must include at least one item referencing \'health_risk_score\' or "
            "\'burnout_probability\' (or Art. 9) — confirmed by Update-1"
        )
    # dpo_consultation_required and sa_prior_consultation_required must be true
    if data.get("dpo_consultation_required") is not True:
        fails.append("dpo_consultation_required must be true (special category + high residual risk)")
    if data.get("sa_prior_consultation_required") is not True:
        fails.append("sa_prior_consultation_required must be true (Art.36 prior consultation required)")
    _finish(fails)
main()
'''

# ── Q10: DPO appointment check ───────────────────────────────────────────────
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "dpo_appointment_check.json")
    if err: _finish([err])
    # mandatory must be "TRUE" string (P4)
    mand = data.get("mandatory")
    if mand != "TRUE":
        fails.append("mandatory == %r (expected string \\"TRUE\\"; 800k users + systematic monitoring triggers Art.37(1)(b))" % mand)
    # criterion_met must reference "Art. 37(1)(b)" verbatim (P2)
    cm = str(data.get("criterion_met", ""))
    if not re.search(r"Art\\.\\s*37\\(1\\)\\(b\\)", cm):
        fails.append("criterion_met == %r (expected verbatim \\"Art. 37(1)(b)\\" format; do not use Discord old memo)" % cm)
    # dpo_name must match exactly "Lena Fischer" from company/org_chart.json
    dpo_name = str(data.get("dpo_name", "")).strip()
    if not dpo_name:
        fails.append("dpo_name must be non-empty")
    elif dpo_name.lower() != "lena fischer":
        fails.append(
            "dpo_name == %r (expected verbatim \\"Lena Fischer\\" from company/org_chart.json; "
            "read the file — do not invent or abbreviate the name)" % dpo_name
        )
    _finish(fails)
main()
'''

# ── Q11: Art.83 penalty exposure ─────────────────────────────────────────────
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "penalty_exposure.json")
    if err: _finish([err])
    # Turnover must be exactly 320,000,000 (from company/company_financials.json, no approximation)
    try:
        wt = int(data.get("worldwide_turnover_eur", 0))
        if wt != 320_000_000:
            fails.append(
                "worldwide_turnover_eur == %d (expected exactly 320,000,000 as recorded in "
                "company/company_financials.json; read the source file — do not estimate or round)" % wt
            )
    except (TypeError, ValueError):
        fails.append("worldwide_turnover_eur not an int: %r" % data.get("worldwide_turnover_eur"))
    # tier1_max exactly 10,000,000
    try:
        t1 = int(data.get("tier1_max_eur", 0))
        if t1 != 10_000_000:
            fails.append("tier1_max_eur == %d (expected exactly 10,000,000)" % t1)
    except (TypeError, ValueError):
        fails.append("tier1_max_eur not an int: %r" % data.get("tier1_max_eur"))
    # tier2_max exactly 20,000,000
    try:
        t2 = int(data.get("tier2_max_eur", 0))
        if t2 != 20_000_000:
            fails.append("tier2_max_eur == %d (expected exactly 20,000,000)" % t2)
    except (TypeError, ValueError):
        fails.append("tier2_max_eur not an int: %r" % data.get("tier2_max_eur"))
    # tier1_percentage_amount exactly 6,400,000
    try:
        t1p = int(data.get("tier1_percentage_amount_eur", 0))
        if t1p != 6_400_000:
            fails.append("tier1_percentage_amount_eur == %d (expected exactly 6,400,000)" % t1p)
    except (TypeError, ValueError):
        fails.append("tier1_percentage_amount_eur not an int")
    # tier2_percentage_amount exactly 12,800,000
    try:
        t2p = int(data.get("tier2_percentage_amount_eur", 0))
        if t2p != 12_800_000:
            fails.append("tier2_percentage_amount_eur == %d (expected exactly 12,800,000)" % t2p)
    except (TypeError, ValueError):
        fails.append("tier2_percentage_amount_eur not an int")
    _finish(fails)
main()
'''

# ── Q12: RoPA version decision ───────────────────────────────────────────────
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "ropa_version_decision.json")
    if err: _finish([err])
    sv = data.get("selected_version")
    if str(sv).strip().lower() not in ("v1", "ropa_controller_draft_v1", "draft_v1"):
        fails.append("selected_version == %r (expected \\"v1\\")" % sv)
    rv = data.get("rejected_version")
    if str(rv).strip().lower() not in ("v0", "ropa_controller_legacy_v0", "legacy_v0"):
        fails.append("rejected_version == %r (expected \\"v0\\")" % rv)
    reason = str(data.get("reason", "")).lower()
    # Keyword check: must include 'legacy' or 'supersed' (covers superseded/supersedes)
    if "legacy" not in reason and "supersed" not in reason:
        fails.append("reason must include 'legacy' or 'superseded' (got: %r)" % data.get("reason",""))
    sf = data.get("source_file", "")
    if not sf or "v1" not in str(sf).lower():
        fails.append("source_file must reference the v1 RoPA file (got %r)" % sf)
    _finish(fails)
main()
'''

# ── Q13: RoPA v2 with AI addendum ────────────────────────────────────────────
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "ropa" / "ropa_controller_v2.json")
    if err: _finish([err])
    activities = data.get("activities") if isinstance(data, dict) else None
    if not isinstance(activities, list):
        _finish(["ropa_controller_v2.json must have an 'activities' list"])
    if len(activities) != 31:
        fails.append("total activities == %d (expected 31: 30 original + ACT-021 from addendum)" % len(activities))
    # There must be an activity with purposes containing 'personalisation' and
    # legal_ground/art6_basis referencing 'legitimate_interests' (the AI addendum activity)
    ai_act = None
    for a in activities:
        if not isinstance(a, dict):
            continue
        purposes_str = str(a.get("purposes", "")).lower()
        if "personalisation" in purposes_str or "personalization" in purposes_str:
            lg = str(a.get("legal_ground", "")).lower()
            a6 = str(a.get("art6_basis", "")).lower()
            if "legitimate_interests" in lg or "legitimate interests" in lg or \
               "legitimate_interests" in a6 or "legitimate interests" in a6:
                ai_act = a
                break
    if ai_act is None:
        fails.append("No AI recommendation engine activity found with purposes containing "
                     "'personalisation' AND legal_ground/art6_basis referencing 'legitimate_interests'")
    _finish(fails)
main()
'''

# ── Q14: Compliance summary ──────────────────────────────────────────────────
CHECKS["check_q14"] = '''
VALID_OVERALL = {"COMPLIANT", "PARTIALLY_COMPLIANT", "NON_COMPLIANT"}

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "compliance_summary.json")
    if err: _finish([err])
    # total_processing_activities must be 31
    tpa = data.get("total_processing_activities")
    if tpa != 31:
        fails.append("total_processing_activities == %r (expected 31: 30 original + ACT-021)" % tpa)
    # dsar_overdue_count must match Q4 output exactly (cross-round closure, zero tolerance)
    doc = data.get("dsar_overdue_count")
    try:
        doc = int(doc)
        if doc <= 0:
            fails.append("dsar_overdue_count == %d (expected positive int)" % doc)
        # Cross-check against Q4 output: must be exact match (tolerance = 0)
        q4_path = ws / "dsar" / "dsar_deadlines.csv"
        if q4_path.exists():
            with q4_path.open(encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            q4_overdue = sum(1 for r in rows if r.get("status") == "OVERDUE")
            if q4_overdue > 0 and doc != q4_overdue:
                fails.append(
                    "dsar_overdue_count %d != Q4 dsar_deadlines.csv OVERDUE count %d "
                    "(cross-round closure: must use exact count from dsar/dsar_deadlines.csv)" % (doc, q4_overdue)
                )
    except (TypeError, ValueError):
        fails.append("dsar_overdue_count not an int: %r" % data.get("dsar_overdue_count"))
    # breach_notification_status must be COMPLIANT (from Q6)
    bns = data.get("breach_notification_status")
    if bns not in ("COMPLIANT", "LATE"):
        fails.append("breach_notification_status == %r (expected COMPLIANT or LATE)" % bns)
    # dpia_required_modules must be a list with at least hr_analytics
    drm = data.get("dpia_required_modules")
    if not isinstance(drm, list) or len(drm) < 1:
        fails.append("dpia_required_modules must be a non-empty list")
    elif not any("hr" in str(m).lower() or "analytics" in str(m).lower() for m in drm):
        fails.append("dpia_required_modules must include hr_analytics module")
    # dpo_mandatory must be string "TRUE" (P4)
    dm = data.get("dpo_mandatory")
    if dm != "TRUE":
        fails.append("dpo_mandatory == %r (expected string \\"TRUE\\")" % dm)
    # overall_status must be valid enum (P5)
    os_ = data.get("overall_status")
    if os_ not in VALID_OVERALL:
        fails.append("overall_status == %r (must be one of COMPLIANT/PARTIALLY_COMPLIANT/NON_COMPLIANT)" % os_)
    _finish(fails)
main()
'''

# ── Q15: Penalty mapping ─────────────────────────────────────────────────────
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "penalty_mapping.json")
    if err: _finish([err])
    gaps = data.get("gaps") if isinstance(data, dict) else None
    if not isinstance(gaps, list):
        _finish(["penalty_mapping.json must have a 'gaps' list"])
    if len(gaps) < 7:
        fails.append(
            "gaps list has %d items (expected >= 7; include Art.30 RoPA gaps, DSAR deadline failures, "
            "DPIA absence, security documentation, AI register omission, Art.5 principle gaps)" % len(gaps)
        )
    tier2_count = 0
    for g in gaps:
        if not isinstance(g, dict): continue
        av = str(g.get("article_violated", ""))
        tier = g.get("tier")
        # V9: article_violated must use format "Art. X(Y)(Z)" or "Art. X(Y)"
        if not re.search(r"Art\\.\\s*\\d+\\(\\d+\\)", av):
            fails.append("gap %s: article_violated %r does not use format \'Art. X(Y)(Z)\'" % (g.get("gap_id","?"), av))
        try:
            if int(tier) == 2:
                tier2_count += 1
        except (TypeError, ValueError):
            fails.append("gap %s: tier %r is not an int" % (g.get("gap_id","?"), tier))
    if tier2_count < 4:
        fails.append(
            "only %d tier-2 gaps (expected >= 4 substantive violations under Art. 83(5))" % tier2_count
        )
    _finish(fails)
main()
'''

# ── Q16: SHA-256 sign-off ────────────────────────────────────────────────────
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "final_report_signoff.json")
    if err: _finish([err])
    signoff = str(data.get("signoff", ""))
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", signoff)
    if not m:
        _finish(["signoff field must match VERIFIED:[a-f0-9]{64} (got %r)" % signoff[:80]])
    # Recompute SHA-256 of compliance_summary.json
    target = ws / "audit" / "compliance_summary.json"
    if not target.exists():
        _finish(["cannot verify: audit/compliance_summary.json not found"])
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    if m.group(1) != actual:
        fails.append("sha256 mismatch: signoff has %s... but recomputed is %s..." % (
            m.group(1)[:12], actual[:12]))
    # target_file field
    tf = data.get("target_file", "")
    if "compliance_summary" not in str(tf):
        fails.append("target_file %r should reference compliance_summary.json" % tf)
    _finish(fails)
main()
'''

# ── Q17: DSAR deadlines v2 (supersede, strict 30-day) ────────────────────────
CHECKS["check_q17"] = '''
from datetime import date, timedelta

def main():
    ws = Path(sys.argv[1]); fails = []
    fp = ws / "dsar" / "dsar_deadlines_v2.csv"
    if not fp.exists():
        _finish(["file not found: dsar/dsar_deadlines_v2.csv"])
    with fp.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) < 390 or len(rows) > 410:
        fails.append("dsar_deadlines_v2.csv has %d rows (expected ~400)" % len(rows))
    if rows:
        for col in ("case_id", "request_date", "response_deadline", "status"):
            if col not in rows[0]:
                fails.append("missing column: %s" % col)
    # Spot-check REQ-042: strict 30 days from 2025-02-10 = 2025-03-12
    r42 = next((r for r in rows if r.get("case_id") == "REQ-042"), None)
    if r42 is None:
        fails.append("REQ-042 not found in dsar_deadlines_v2.csv")
    else:
        expected = (date(2025, 2, 10) + timedelta(days=30)).isoformat()
        if r42.get("response_deadline") != expected:
            fails.append("REQ-042 response_deadline == %r (expected strict 30d: %s; Update-2 supersedes any extension)" % (
                r42.get("response_deadline"), expected))
        if r42.get("status") != "OVERDUE":
            fails.append("REQ-042 status must be OVERDUE in v2 (strict 30d rule per BayLDA memo)")
    # Verify the strict 30-day computation for several spot-check cases
    for r in rows[:20]:
        try:
            rd = date.fromisoformat(r.get("request_date",""))
            expected_dl = (rd + timedelta(days=30)).isoformat()
            if r.get("response_deadline") != expected_dl:
                fails.append("row %s: response_deadline %r != strict 30d %s (Update-2 supersedes extensions)" % (
                    r.get("case_id","?"), r.get("response_deadline"), expected_dl))
                break
        except ValueError:
            fails.append("row %s: invalid request_date %r" % (r.get("case_id","?"), r.get("request_date","")))
            break
    _finish(fails)
main()
'''

# ── Q18: Final GDPR audit certificate ────────────────────────────────────────
CHECKS["check_q18"] = '''
VALID_OVERALL = {"COMPLIANT", "PARTIALLY_COMPLIANT", "NON_COMPLIANT"}
BOOL_FIELDS = ["article_30_compliant", "article_33_compliant", "article_37_compliant"]
REQUIRED_KEYS = [
    "audit_date", "company_id", "dpo_name", "overall_status",
    "article_30_compliant", "article_33_compliant", "article_37_compliant",
    "article_83_max_exposure_eur", "signoff"
]

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "gdpr_audit_certificate.json")
    if err: _finish([err])
    # All required keys present
    for k in REQUIRED_KEYS:
        if k not in data:
            fails.append("missing required key: %s" % k)
    # Boolean fields must be string "TRUE" or "FALSE" (P4)
    for f in BOOL_FIELDS:
        v = data.get(f)
        if v not in ("TRUE", "FALSE"):
            fails.append("%s == %r (must be string \\"TRUE\\" or \\"FALSE\\")" % (f, v))
    # overall_status must be valid enum (P5)
    os_ = data.get("overall_status")
    if os_ not in VALID_OVERALL:
        fails.append("overall_status == %r (must be COMPLIANT/PARTIALLY_COMPLIANT/NON_COMPLIANT)" % os_)
    # article_83_max_exposure_eur must be 20,000,000 (tier2_max from Q11)
    try:
        exp = int(data.get("article_83_max_exposure_eur", 0))
        if not (19_000_000 <= exp <= 21_000_000):
            fails.append("article_83_max_exposure_eur == %d (expected 20,000,000 from Q11 tier2_max)" % exp)
    except (TypeError, ValueError):
        fails.append("article_83_max_exposure_eur not an int")
    # signoff must match VERIFIED:<sha256> and cross-check with Q16
    signoff = str(data.get("signoff", ""))
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", signoff)
    if not m:
        fails.append("signoff must match VERIFIED:[a-f0-9]{64} (got %r)" % signoff[:80])
    else:
        # Cross-round closure: verify against compliance_summary.json
        target = ws / "audit" / "compliance_summary.json"
        if target.exists():
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            if m.group(1) != actual:
                fails.append("signoff sha256 mismatch with compliance_summary.json (cross-round closure violation)")
    # company_id must reference VeritasCloud
    cid = str(data.get("company_id", ""))
    if "veritascloud" not in cid.lower() and "veritas" not in cid.lower():
        fails.append("company_id %r does not reference VeritasCloud GmbH" % cid)
    # dpo_name must be non-empty
    if not data.get("dpo_name") or str(data.get("dpo_name","")).strip() == "":
        fails.append("dpo_name must be non-empty")
    _finish(fails)
main()
'''

# ── Preference checker ────────────────────────────────────────────────────────
PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sec4 preference checker (P1-P5).

P1: All structured JSON outputs must be valid JSON with snake_case field names.
P2: Article references must use format "Art. X(Y)(Z)" (dot + parentheses).
P3: DSAR response/deadline files must carry case_id, request_date, response_deadline, status.
P4: Boolean conclusion fields must use uppercase string "TRUE"/"FALSE", not JSON true/false.
P5: overall_status must be one of COMPLIANT / PARTIALLY_COMPLIANT / NON_COMPLIANT.
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Valid JSON with snake_case keys."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError as e:
        return False, "P1: target is not valid JSON: %s" % e
    # Walk keys and check snake_case (allow all-lowercase + underscores + digits)
    def _walk(obj):
        if isinstance(obj, dict):
            for k in obj.keys():
                if re.search(r"[A-Z]", k) and k not in ("DPO_contact", "DRAFT_NOTE"):
                    # Allow DPO_contact as it is part of a required field name in GDPR spec
                    if not k.startswith("DPO"):
                        return "P1: key %r is not snake_case" % k
            for v in obj.values():
                r = _walk(v)
                if r: return r
        elif isinstance(obj, list):
            for item in obj:
                r = _walk(item)
                if r: return r
        return None
    err = _walk(data)
    if err:
        return False, err
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Article references must use format 'Art. X(Y)(Z)'."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    # Look for bad patterns: "Article X" or "#X" that reference GDPR articles
    bad = re.findall(r"Article\\s+\\d+", txt)
    if bad:
        return False, "P2: found non-standard article reference format: %s (use 'Art. X(Y)(Z)')" % bad[:3]
    # Check for hash-style references like "#33" when followed by a parenthetical
    bad2 = re.findall(r"#\\d+\\(\\d+\\)", txt)
    if bad2:
        return False, "P2: found hash-style article reference: %s (use 'Art. X(Y)(Z)')" % bad2[:3]
    return True, "P2: PASSED"


def check_P3(ws, target):
    """DSAR response/deadline files must carry four metadata fields."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    low = txt.lower()
    missing = []
    for field in ("case_id", "request_date", "response_deadline", "status"):
        if field not in low:
            missing.append(field)
    if missing:
        return False, "P3: DSAR file missing metadata fields: %s" % missing
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Boolean conclusion fields must be uppercase string TRUE/FALSE."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P4: target is not valid JSON"
    # Check specific boolean-conclusion fields that should be strings
    BOOL_KEYS = {
        "mandatory", "dpo_mandatory", "article_30_compliant",
        "article_33_compliant", "article_37_compliant",
    }
    def _walk(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in BOOL_KEYS and isinstance(v, bool):
                    return "P4: field %r uses JSON bool %r (must be string \\"TRUE\\" or \\"FALSE\\")" % (k, v)
            for v in obj.values():
                r = _walk(v)
                if r: return r
        elif isinstance(obj, list):
            for item in obj:
                r = _walk(item)
                if r: return r
        return None
    err = _walk(data)
    if err:
        return False, err
    return True, "P4: PASSED"


def check_P5(ws, target):
    """overall_status must be one of three valid enum values."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P5: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P5: not a JSON object, skip"
    if "overall_status" not in data:
        return True, "P5: no overall_status field, skip"
    VALID = {"COMPLIANT", "PARTIALLY_COMPLIANT", "NON_COMPLIANT"}
    os_ = data.get("overall_status")
    if os_ not in VALID:
        return False, "P5: overall_status == %r (must be COMPLIANT / PARTIALLY_COMPLIANT / NON_COMPLIANT)" % os_
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="audit/")
    a = ap.parse_args()
    ws = Path(a.workspace)
    rules = [r.strip() for r in a.rules.split(",") if r.strip()]
    unknown = [r for r in rules if r not in RULES]
    if unknown:
        print("FAILED: unknown rules: %s" % unknown); sys.exit(1)
    fails = []
    for r in rules:
        ok, msg = RULES[r](ws, a.target)
        print(msg)
        if not ok:
            fails.append(msg)
    if fails:
        for m in fails:
            print("FAILED: " + m)
        sys.exit(1)
    print("PASSED"); sys.exit(0)


if __name__ == "__main__":
    main()
'''


def main():
    for name, body in CHECKS.items():
        (OUT / f"{name}.py").write_text(HEADER + textwrap.dedent(body), encoding="utf-8")
    (OUT / "check_preferences.py").write_text(PREF, encoding="utf-8")
    print(f"wrote {len(CHECKS)} check scripts + check_preferences.py to {OUT}")


if __name__ == "__main__":
    main()
