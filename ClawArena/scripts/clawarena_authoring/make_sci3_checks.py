#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_sci3_checks.py — 生成 sci3 的全部 exec_check 校验脚本到 eval/sci3/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_sci3.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5。生成器内容即评测逻辑，可逐脚本审阅。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/sci3/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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

def _read_csv(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        with p.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        return rows, None
    except Exception as e:
        return None, "CSV error in " + p.name + ": " + str(e)

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)
'''

CHECKS = {}

# Q1: ratios_baseline.json — ICU=2, Med/Surg=5, Step-Down=3, Telemetry=4, ED=4, Psych=6
# regulation_ref contains "§ 70217"; effective dates correct
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "ratios_baseline.json")
    if err: _finish([err])
    # 结构层：units 数组
    units = data.get("units") or data.get("ratios") or []
    if not isinstance(units, list) or len(units) < 6:
        fails.append("units array must have at least 6 entries (got %r)" % len(units))
        _finish(fails)
    # 建立 unit -> entry 索引（支持多种 unit 名写法）
    def norm(s):
        s = str(s).lower().replace("-", "").replace("/", "").replace(" ", "")
        return s
    by_unit = {}
    for e in units:
        if isinstance(e, dict):
            u = norm(e.get("unit", ""))
            by_unit[u] = e
    # 真值层：每个科室最大患者数
    EXPECTED = {
        "icu": 2, "intensivecareunit": 2, "criticalcare": 2,
        "medsurg": 5, "medicalsurgical": 5, "medicalsurg": 5,
        "stepdown": 3, "intermediatecareunit": 3, "progressivecare": 3,
        "telemetry": 4,
        "ed": 4, "emergencydepartment": 4, "emergency": 4,
        "psychiatric": 6, "psych": 6, "psychiatricunit": 6,
    }
    UNIT_ALIASES = {
        "icu": ["icu", "intensivecareunit", "criticalcare"],
        "medsurg": ["medsurg", "medicalsurgical", "medicalsurg"],
        "stepdown": ["stepdown", "intermediatecareunit", "progressivecare", "stepdownunit"],
        "telemetry": ["telemetry"],
        "ed": ["ed", "emergencydepartment", "emergency"],
        "psych": ["psychiatric", "psych", "psychiatricunit"],
    }
    for canonical, aliases in UNIT_ALIASES.items():
        entry = None
        for a in aliases:
            if a in by_unit:
                entry = by_unit[a]
                break
        if entry is None:
            fails.append("no entry found for unit group %r" % canonical)
            continue
        max_p = None
        for k in ("legal_ratio_max_patients", "max_patients", "ratio_max_patients", "max"):
            if k in entry:
                try:
                    max_p = int(entry[k])
                except (ValueError, TypeError):
                    pass
                break
        expected = EXPECTED[aliases[0]]
        if max_p is None:
            fails.append("%s: could not find legal_ratio_max_patients field" % canonical)
        elif max_p != expected:
            fails.append("%s: legal_ratio_max_patients == %r (expected %d)" % (canonical, max_p, expected))
        # regulation_ref must contain "§ 70217"
        ref = str(entry.get("regulation_ref", ""))
        if "70217" not in ref:
            fails.append("%s: regulation_ref %r does not contain '§ 70217' or '70217'" % (canonical, ref[:50]))
    # effective_date checks
    for e in units:
        if not isinstance(e, dict):
            continue
        u = norm(e.get("unit", ""))
        ed = str(e.get("effective_date", ""))
        if u in ("icu", "intensivecareunit", "criticalcare"):
            if ed and ed != "2004-01-01":
                fails.append("ICU effective_date == %r (expected 2004-01-01)" % ed)
        if u in ("stepdown", "stepdownunit", "intermediatecareunit"):
            if ed and ed != "2008-01-01":
                fails.append("Step-Down effective_date == %r (expected 2008-01-01)" % ed)
        if u in ("telemetry",):
            if ed and ed != "2008-01-01":
                fails.append("Telemetry effective_date == %r (expected 2008-01-01)" % ed)
    _finish(fails)
main()
'''

# Q2: charge_nurse_violations.csv — at least 3 ICU night shifts Oct 5-7 with ratio > 2
# 加难 A：shift_id 必须精确匹配 SVMC_staffing_log_oct2024.csv 中真实的 shift_id（SH-2159/SH-2171/SH-2183）
# 同时 date 精确匹配：2024-10-05, 2024-10-06, 2024-10-07
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    rows, err = _read_csv(ws / "output" / "charge_nurse_violations.csv")
    if err: _finish([err])
    if not rows:
        _finish(["charge_nurse_violations.csv is empty"])
    # 结构层：必要字段
    req_fields = {"shift_id", "unit", "date"}
    for rf in req_fields:
        if rf not in rows[0]:
            fails.append("missing column %r" % rf)
    if fails: _finish(fails)
    # 字段层：ICU 班次存在
    icu_rows = [r for r in rows if "ICU" in str(r.get("unit", "")).upper()]
    if len(icu_rows) < 3:
        fails.append("fewer than 3 ICU rows with charge nurse error (got %d)" % len(icu_rows))
    # 真值层：ratio_excluding_charge > 2.0 for ICU rows
    icu_violation_count = 0
    for r in icu_rows:
        ratio_field = None
        for k in ("ratio_excluding_charge", "ratio_excl_charge", "actual_ratio", "ratio"):
            if k in r and r[k] not in ("", None):
                ratio_field = k
                break
        if ratio_field:
            try:
                ratio = float(r[ratio_field])
                if ratio > 2.0:
                    icu_violation_count += 1
            except (ValueError, TypeError):
                pass
    if icu_violation_count < 3:
        fails.append("fewer than 3 ICU charge-nurse-corrected shifts with ratio > 2.0 (got %d)" % icu_violation_count)
    # is_violation must be truthy for violation rows
    viol_col = None
    for k in ("is_violation", "violation", "is_shift_violation"):
        if k in rows[0]:
            viol_col = k
            break
    if viol_col:
        icu_true = [r for r in icu_rows if str(r.get(viol_col, "")).lower() in ("true", "1", "yes")]
        if len(icu_true) < 3:
            fails.append("fewer than 3 ICU rows with %s=True (got %d)" % (viol_col, len(icu_true)))
    # 真值层 (A加难)：shift_id 必须来自 SVMC_staffing_log_oct2024.csv 的真实记录
    # 源数据中 charge_nurse_included_error=True 的班次 ID 为 SH-2159, SH-2171, SH-2183
    EXPECTED_SHIFT_IDS = {"SH-2159", "SH-2171", "SH-2183"}
    found_ids = {str(r.get("shift_id", "")).strip() for r in icu_rows}
    missing_ids = EXPECTED_SHIFT_IDS - found_ids
    if missing_ids:
        fails.append(
            "shift_id mismatch: expected shift_ids %s from SVMC_staffing_log_oct2024.csv "
            "(charge_nurse_included_error=True rows), but not found. Got: %s" % (
                sorted(missing_ids), sorted(found_ids)[:5]))
    # 真值层 (A加难)：date 必须精确匹配 2024-10-05, 2024-10-06, 2024-10-07
    EXPECTED_DATES = {"2024-10-05", "2024-10-06", "2024-10-07"}
    found_dates = {str(r.get("date", "")).strip() for r in icu_rows}
    missing_dates = EXPECTED_DATES - found_dates
    if missing_dates:
        fails.append("missing expected violation dates %s (ICU charge nurse error dates from staffing log)" % sorted(missing_dates))
    _finish(fails)
main()
'''

# Q3: penalty_assessment.json — first_violation_fee=15000 (not 10000), total is integer
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "penalty_assessment.json")
    if err: _finish([err])
    # 字段层
    for fld in ("first_violation_fee", "subsequent_violation_fee", "total_penalty_usd"):
        if fld not in data:
            fails.append("missing field %r" % fld)
    if fails: _finish(fails)
    # 真值层：first_violation_fee = 15000
    fvf = data.get("first_violation_fee")
    try:
        fvf_int = int(fvf)
        if fvf_int == 10000:
            fails.append("first_violation_fee == 10000 (the Feishu BOT decoy value); correct value is 15000")
        elif fvf_int != 15000:
            fails.append("first_violation_fee == %d (expected 15000)" % fvf_int)
    except (TypeError, ValueError):
        fails.append("first_violation_fee not an integer: %r" % fvf)
    # subsequent_violation_fee = 30000
    svf = data.get("subsequent_violation_fee")
    try:
        if int(svf) != 30000:
            fails.append("subsequent_violation_fee == %r (expected 30000)" % svf)
    except (TypeError, ValueError):
        fails.append("subsequent_violation_fee not an integer: %r" % svf)
    # total_penalty_usd must be positive integer
    tp = data.get("total_penalty_usd")
    try:
        tp_int = int(tp)
        if tp_int <= 0:
            fails.append("total_penalty_usd must be positive (got %d)" % tp_int)
    except (TypeError, ValueError):
        fails.append("total_penalty_usd not an integer: %r" % tp)
    # V5 guard: total must not be based on $10,000 first violation
    # If there's 1 first violation and N subsequent, $10k base would give 10000 + N*30000
    # We check total is not exactly what $10,000 base would give (for common violation counts 1-5)
    vc_first = data.get("violation_count_first", 1)
    try:
        vc_first_int = int(vc_first)
        vc_subseq_int = int(data.get("violation_count_subsequent", 0))
        decoy_total = 10000 * vc_first_int + 30000 * vc_subseq_int
        if int(tp) == decoy_total and decoy_total != (15000 * vc_first_int + 30000 * vc_subseq_int):
            fails.append("total_penalty_usd appears to use $10,000 first-violation rate (decoy); use $15,000")
    except (TypeError, ValueError):
        pass
    _finish(fails)
main()
'''

# Q4: sb596_penalty_projection.json — effective_date=2026-01-01; post > pre; diff = post - pre
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "sb596_penalty_projection.json")
    if err: _finish([err])
    # 结构层
    for fld in ("effective_date", "pre_sb596_total", "post_sb596_total", "diff"):
        if fld not in data:
            fails.append("missing field %r" % fld)
    if fails: _finish(fails)
    # 真值层
    ed = str(data.get("effective_date", ""))
    if ed != "2026-01-01":
        fails.append("effective_date == %r (expected '2026-01-01')" % ed)
    try:
        pre = int(data["pre_sb596_total"])
        post = int(data["post_sb596_total"])
        diff = int(data["diff"])
        if post <= pre:
            fails.append("post_sb596_total (%d) must be > pre_sb596_total (%d)" % (post, pre))
        if diff != post - pre:
            fails.append("diff (%d) != post_sb596_total - pre_sb596_total (%d)" % (diff, post - pre))
    except (TypeError, ValueError) as exc:
        fails.append("pre/post/diff must be integers: %s" % exc)
    # cross-round closure: pre_sb596_total must match Q3 total (if Q3 exists)
    q3, e3 = _load_json(ws / "output" / "penalty_assessment.json")
    if not e3 and q3 is not None:
        q3_total = q3.get("total_penalty_usd")
        try:
            if int(data["pre_sb596_total"]) != int(q3_total):
                fails.append("pre_sb596_total (%d) != Q3 total_penalty_usd (%d) (cross-round closure)" % (
                    int(data["pre_sb596_total"]), int(q3_total)))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
'''

# Q5: exemption_analysis.md — no flu auto-exempt; Prong 3 failure; verbatim AFL-23-27 quote
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "exemption_analysis.md")
    if txt is None:
        _finish(["file not found: output/exemption_analysis.md"])
    low = txt.lower()
    # 真值层 1: seasonal flu NOT auto-exempt
    if not (re.search(r"flu|influenza", low) and re.search(r"not.{0,30}(auto|exempt)|cannot.{0,30}exempt", low)):
        # alternate phrasing
        if not re.search(r"(seasonal|influenza|flu).{0,60}not.{0,30}(automatically|auto).{0,30}(exempt|qualify|qualif)", low):
            fails.append("must state seasonal flu/influenza does NOT automatically qualify as exempt (AFL-23-27)")
    # 真值层 2: Prong 3 failure (on-call list not exhausted)
    if not re.search(r"prong.{0,5}3|on.call.{0,15}list.{0,30}(not|exhaust|fail)", low):
        fails.append("must identify Prong 3 failure: on-call list was not fully exhausted for Med/Surg")
    # 真值层 3: verbatim AFL-23-27 language (near-verbatim)
    afl_phrase = "immediately used and subsequently exhausted"
    if afl_phrase not in low:
        # relax: accept paraphrase with key words
        if not (re.search(r"exhaust.{0,20}on.call", low) and re.search(r"immedi", low)):
            fails.append("must include AFL-23-27 language: 'immediately used and subsequently exhausted the ... on-call list'")
    # 结构层: at least 2 sections (one per violation group)
    h3_count = len(re.findall(r"^### ", txt, re.MULTILINE))
    if h3_count < 2:
        fails.append("fewer than 2 ### headings (expected one per violation group)")
    _finish(fails)
main()
'''

# Q6: schedule_icu_stepdown.csv — all ICU ratio ≤ 2.00; Step-Down ≤ 3.00
# 加难 A：日期范围必须覆盖 2024-11-01 到 2024-11-14 全部 14 天
# 每个 unit 至少有 14 个不同日期的记录（一个 2 周完整排班才有意义）
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    rows, err = _read_csv(ws / "output" / "schedule_icu_stepdown.csv")
    if err: _finish([err])
    if not rows:
        _finish(["schedule_icu_stepdown.csv is empty"])
    req = {"date", "shift", "unit", "nurse_id", "patient_count", "ratio_computed"}
    missing = req - set(rows[0].keys())
    if missing:
        fails.append("missing columns: %s" % sorted(missing))
    if fails: _finish(fails)
    # 真值层：ratio limits
    for r in rows:
        unit = str(r.get("unit", "")).upper()
        ratio_str = str(r.get("ratio_computed", "")).strip()
        try:
            ratio = float(ratio_str)
        except (ValueError, TypeError):
            continues = True  # skip non-numeric
            continue
        if "ICU" in unit and ratio > 2.00 + 1e-9:
            fails.append("ICU shift ratio_computed == %.2f > 2.00 (date=%s)" % (ratio, r.get("date", "")))
        if "STEP" in unit and ratio > 3.00 + 1e-9:
            fails.append("Step-Down shift ratio_computed == %.2f > 3.00 (date=%s)" % (ratio, r.get("date", "")))
    # must have both units
    units_seen = {str(r.get("unit", "")).upper() for r in rows}
    if not any("ICU" in u for u in units_seen):
        fails.append("no ICU rows found in schedule")
    if not any("STEP" in u or "DOWN" in u for u in units_seen):
        fails.append("no Step-Down rows found in schedule")
    # 真值层 (A加难)：日期范围必须覆盖 2024-11-01 到 2024-11-14 全部 14 天
    import datetime
    expected_dates = set()
    d = datetime.date(2024, 11, 1)
    for _ in range(14):
        expected_dates.add(d.strftime("%Y-%m-%d"))
        d += datetime.timedelta(days=1)
    found_dates = {str(r.get("date", "")).strip() for r in rows}
    missing_dates = expected_dates - found_dates
    if missing_dates:
        fails.append(
            "schedule must cover all 14 days Nov 1-14 2024; missing dates: %s" % sorted(missing_dates)[:5])
    # 真值层 (A加难)：ICU 和 Step-Down 各有 ≥ 14 个不同日期
    icu_dates = {str(r.get("date","")) for r in rows if "ICU" in str(r.get("unit","")).upper()}
    sd_dates = {str(r.get("date","")) for r in rows if "STEP" in str(r.get("unit","")).upper() or "DOWN" in str(r.get("unit","")).upper()}
    if len(icu_dates) < 14:
        fails.append("ICU schedule covers only %d distinct dates (must cover all 14 days Nov 1-14)" % len(icu_dates))
    if len(sd_dates) < 14:
        fails.append("Step-Down schedule covers only %d distinct dates (must cover all 14 days Nov 1-14)" % len(sd_dates))
    _finish(fails)
main()
'''

# Q7: medsurg_night_analysis.json — violation_count >= 5, FMLA in root_cause, float pool in corrective
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "medsurg_night_analysis.json")
    if err: _finish([err])
    # 结构层
    for fld in ("violation_shifts", "total_violation_count", "root_cause", "corrective_measures"):
        if fld not in data:
            # try plural/singular variants
            alt = fld.rstrip("s") if fld.endswith("s") else fld + "s"
            if alt not in data:
                fails.append("missing field %r (or %r)" % (fld, alt))
    if fails: _finish(fails)
    # 字段层
    vc_key = "total_violation_count" if "total_violation_count" in data else "violation_count"
    vs_key = "violation_shifts" if "violation_shifts" in data else "violations"
    cm_key = "corrective_measures" if "corrective_measures" in data else "corrective_actions"
    try:
        vc = int(data.get(vc_key, 0))
        if vc < 5:
            fails.append("total_violation_count == %d (expected >= 5)" % vc)
    except (TypeError, ValueError):
        fails.append("total_violation_count not an int: %r" % data.get(vc_key))
    # 真值层：root_cause mentions FMLA or CFRA
    rc = str(data.get("root_cause", "")).lower()
    if "fmla" not in rc and "cfra" not in rc and "family.medical" not in rc:
        fails.append("root_cause does not mention FMLA or CFRA")
    # corrective_measures contains float pool and on-call list
    cm = data.get(cm_key, [])
    cm_text = " ".join(str(c) for c in cm).lower() if isinstance(cm, list) else str(cm).lower()
    if "float" not in cm_text and "pool" not in cm_text:
        fails.append("corrective_measures does not mention float pool expansion")
    if ("on-call" not in cm_text and "on.call" not in cm_text and
            "on_call" not in cm_text and "oncall" not in cm_text):
        fails.append("corrective_measures does not mention on-call list update")
    _finish(fails)
main()
'''

# Q8: cdph_staffing_log_week1.csv — all ratios ≤ legal max; license_type valid; PT only in Psych
CHECKS["check_q8"] = '''
LEGAL_MAX = {"ICU": 2.0, "Med/Surg": 5.0, "Step-Down": 3.0, "Telemetry": 4.0,
             "ED": 4.0, "Psychiatric": 6.0}

def _get_legal_max(unit_str):
    u = str(unit_str).strip()
    for k, v in LEGAL_MAX.items():
        if k.lower() in u.lower() or u.lower() in k.lower():
            return v
    return None

def main():
    ws = Path(sys.argv[1]); fails = []
    rows, err = _read_csv(ws / "output" / "cdph_staffing_log_week1.csv")
    if err: _finish([err])
    if not rows:
        _finish(["cdph_staffing_log_week1.csv is empty"])
    req = {"date", "unit", "nurse_id", "license_type", "patient_count", "ratio"}
    missing = req - set(rows[0].keys())
    if missing:
        fails.append("missing columns: %s" % sorted(missing))
    if fails: _finish(fails)
    valid_lic = {"RN", "LVN", "PT"}
    for i, r in enumerate(rows):
        lic = str(r.get("license_type", "")).strip().upper()
        if lic not in valid_lic:
            fails.append("row %d: license_type %r not in {RN, LVN, PT}" % (i+1, lic))
            continue
        unit = str(r.get("unit", ""))
        if lic == "PT" and "psych" not in unit.lower() and "psychiatric" not in unit.lower():
            fails.append("row %d: PT license_type in non-Psychiatric unit %r" % (i+1, unit))
        # ratio check (skip admin Charge Nurse rows with patient_count=0)
        try:
            pc = int(r.get("patient_count", 0))
        except (ValueError, TypeError):
            pc = 0
        if pc == 0:
            continue  # admin duty row, skip ratio check
        lm = _get_legal_max(unit)
        if lm is None:
            continue
        ratio_str = str(r.get("ratio", "")).strip()
        try:
            ratio = float(ratio_str)
            if ratio > lm + 1e-9:
                fails.append("row %d: ratio %.2f > legal max %.1f for unit %r" % (i+1, ratio, lm, unit))
        except (ValueError, TypeError):
            fails.append("row %d: ratio %r not numeric" % (i+1, ratio_str))
    _finish(fails)
main()
'''

# Q9: penalty_assessment_v2.json — post_sb596_count=7; grand_total > Q3; pre/post structure
# 加难 A：pre_sb596_count 必须精确等于 17（13 Oct 违规 + 4 pre-SB596 Telemetry Dec28-31）
# 加难 C：grand_total_penalty 必须精确等于 255000（验证完整计算路径）
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "penalty_assessment_v2.json")
    if err: _finish([err])
    for fld in ("post_sb596_count", "grand_total_penalty", "pre_sb596_count"):
        if fld not in data:
            fails.append("missing field %r" % fld)
    if fails: _finish(fails)
    # 真值层：post_sb596_count = 7 (the 7 daily violations Jan 2-8)
    psc = data.get("post_sb596_count")
    try:
        psc_int = int(psc)
        if psc_int != 7:
            fails.append("post_sb596_count == %d (expected 7 — the 7 daily violations Jan 2-8 2026)" % psc_int)
    except (TypeError, ValueError):
        fails.append("post_sb596_count not an int: %r" % psc)
    # 真值层 (A加难)：pre_sb596_count 必须精确等于 17
    # 说明：Oct 2024 有 13 个违规班次 (SH-1008 to SH-1488)；pre-SB596 Telemetry 有 4 个 (Dec 28-31)
    # 总共 17 个 pre-SB596 违规计数。注意 SB 596 生效日期为 2026-01-01，
    # 因此 Dec 2025 的 Telemetry 违规（4 次）均属于 pre-SB596 范畴。
    # 浅做的模型可能只统计 Oct 2024 违规 (13)，或者误将 Dec Telemetry 作为 post 计算。
    pre_count = data.get("pre_sb596_count")
    try:
        pre_int = int(pre_count)
        if pre_int != 17:
            fails.append(
                "pre_sb596_count == %d (expected 17: 13 Oct-2024 violation shifts + 4 pre-SB596 "
                "Telemetry Dec 28-31 2025; SB 596 effective 2026-01-01)" % pre_int)
    except (TypeError, ValueError):
        fails.append("pre_sb596_count not an int: %r" % pre_count)
    # grand_total > Q3 total
    q3, e3 = _load_json(ws / "output" / "penalty_assessment.json")
    gtp = data.get("grand_total_penalty")
    try:
        gtp_int = int(gtp)
        if not e3 and q3 is not None:
            q3t = int(q3.get("total_penalty_usd", 0))
            if gtp_int <= q3t:
                fails.append("grand_total_penalty (%d) must be > Q3 total (%d) — new violations added" % (gtp_int, q3t))
        # 真值层 (C加难)：grand_total 精确验证
        # 计算: pre-SB596 penalty = $15k (Oct first) + $30k (Dec Tel group) = $45k
        # post-SB596 penalty = 7 × $30k = $210k; grand_total = $45k + $210k = $255k
        if gtp_int != 255000:
            fails.append(
                "grand_total_penalty == %d (expected 255000: "
                "pre=$45k [Oct first@$15k + Dec-Tel@$30k] + post=$210k [7 daily@$30k])" % gtp_int)
    except (TypeError, ValueError):
        fails.append("grand_total_penalty not an int: %r" % gtp)
    _finish(fails)
main()
'''

# Q10: oncall_audit.json — use current list; compliant_nurses present; recommendation mentions SB 596
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "oncall_audit.json")
    if err: _finish([err])
    for fld in ("compliant_nurses", "non_compliant_nurses", "gap_count", "recommendation"):
        if fld not in data:
            fails.append("missing field %r" % fld)
    if fails: _finish(fails)
    # 字段层
    cn = data.get("compliant_nurses", [])
    if not isinstance(cn, list) or len(cn) == 0:
        fails.append("compliant_nurses must be a non-empty list")
    # recommendation references SB 596
    rec = str(data.get("recommendation", "")).lower()
    if "sb 596" not in rec and "sb596" not in rec and "sb-596" not in rec:
        fails.append("recommendation must reference SB 596 on-call definition")
    # recommendation length ≤ 150 chars
    if len(str(data.get("recommendation", ""))) > 150:
        fails.append("recommendation exceeds 150 characters (P5 violation)")
    # gap_count must be non-negative int
    gc = data.get("gap_count")
    try:
        if int(gc) < 0:
            fails.append("gap_count must be >= 0")
    except (TypeError, ValueError):
        fails.append("gap_count not an int: %r" % gc)
    # V6 guard: make sure the archived list was NOT used
    # (archived nurses should not appear as compliant)
    archived_ids = {"RN-MS-OLD-01", "RN-ICU-OLD-01", "RN-TEL-OLD-01", "RN-SD-OLD-01"}
    cn_set = set(str(x) for x in cn)
    overlap = archived_ids & cn_set
    if overlap:
        fails.append("compliant_nurses contains archived/obsolete nurse IDs %s (use current list, not v2023-10)" % sorted(overlap))
    _finish(fails)
main()
'''

# Q11: violation_ledger_final.json — superseded_count=4; newly_added_count=2; total = q9 - 4 + 2
# 加难 A：total_count 必须精确等于 18（13 Oct + 11 Tel - 4 superseded + 2 ICU new = 22; 但 Q9 Tel=11, supersede 4 → 22-4+2=20? 不对
# 正确：从 Q9 all_violations 共 (13+11)=24 项，supersede 4 → 24-4+2=22；但 Q9 的 Telemetry 是 11 条
# 实际上 gold_solve 里: OCT2024=13, U1_TEL=11 (total 24 in Q9); supersede 4 → remaining=20; +2 ICU = 22
# Wait: OCT2024 = 13, U1_TEL_VIOLATIONS = 11 (Dec28-Jan8 共11天), superseded IDs = 4 (TEL-002..005)
# remaining_tel = 11 - 4 = 7; final = 13 + 7 + 2 = 22
# 加难 A+C：total_count 必须精确等于 22；violations 数组不能有聚合行（每行必须是单个独立班次）
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "violation_ledger_final.json")
    if err: _finish([err])
    for fld in ("violations", "total_count", "superseded_count", "newly_added_count"):
        if fld not in data:
            fails.append("missing field %r" % fld)
    if fails: _finish(fails)
    # 真值层：superseded_count = 4
    sc = data.get("superseded_count")
    try:
        sc_int = int(sc)
        if sc_int != 4:
            fails.append("superseded_count == %d (expected 4 — the 4 Telemetry violations withdrawn by U2)" % sc_int)
    except (TypeError, ValueError):
        fails.append("superseded_count not an int: %r" % sc)
    # newly_added_count = 2
    nac = data.get("newly_added_count")
    try:
        nac_int = int(nac)
        if nac_int != 2:
            fails.append("newly_added_count == %d (expected 2 — the 2 ICU violations added by U2)" % nac_int)
    except (TypeError, ValueError):
        fails.append("newly_added_count not an int: %r" % nac)
    # total_count closure: must not be q9 count + 2 (that would be additive not supersede)
    tc = data.get("total_count")
    violations = data.get("violations", [])
    try:
        tc_int = int(tc)
        # cross-check with violations list length
        if isinstance(violations, list) and len(violations) > 0:
            if tc_int != len(violations):
                fails.append("total_count (%d) != len(violations) (%d)" % (tc_int, len(violations)))
        # 真值层 (A加难)：total_count 必须精确等于 22
        # 计算：Q9 violations = 13 (Oct2024) + 11 (U1 Telemetry Dec28-Jan8)= 24 total
        # U2 supersedes 4 Telemetry (SH-TEL-U1-002..005) → 24-4=20 remaining
        # U2 adds 2 ICU (SH-ICU-LATE-001, -002) → 20+2=22 final violations
        if tc_int != 22:
            fails.append(
                "total_count == %d (expected 22: 13 Oct-2024 + 11 U1-Telemetry - 4 superseded + 2 new ICU = 22); "
                "a common error is grouping Oct violations into 1 aggregate row or miscounting supersede" % tc_int)
    except (TypeError, ValueError):
        fails.append("total_count not an int: %r" % tc)
    # violations array: each entry must have unit, date, shift_id
    if isinstance(violations, list):
        for i, v in enumerate(violations[:3]):
            for fk in ("unit", "date"):
                if fk not in v:
                    fails.append("violations[%d] missing field %r" % (i, fk))
    # 真值层 (C加难)：每个 violation entry 必须是单个独立班次（不得聚合）
    # 检查：unit 字段不能含 "mixed"/"group" 等聚合词；date 字段不能是区间（含 "to"）
    if isinstance(violations, list):
        for i, v in enumerate(violations):
            if not isinstance(v, dict):
                continue
            unit_str = str(v.get("unit", "")).lower()
            date_str = str(v.get("date", "")).lower()
            if "mixed" in unit_str or "group" in unit_str or "various" in unit_str:
                fails.append(
                    "violations[%d] has aggregated unit=%r; each entry must represent a single shift, "
                    "not a group (Oct 2024 has 13 individual shifts)" % (i, v.get("unit")))
                break
            if " to " in date_str or "through" in date_str or "range" in date_str:
                fails.append(
                    "violations[%d] has date range %r; each entry must represent a single shift date" % (i, v.get("date")))
                break
    _finish(fails)
main()
'''

# Q12: penalty_final.json — arithmetic closure; post_2026_total > 0 (daily violations);
# grand_total != Q9 total (because violations changed via U2 supersede)
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "penalty_final.json")
    if err: _finish([err])
    for fld in ("pre_2026_total", "post_2026_total", "grand_total"):
        if fld not in data:
            fails.append("missing field %r" % fld)
    if fails: _finish(fails)
    try:
        pre = int(data["pre_2026_total"])
        post = int(data["post_2026_total"])
        gt = int(data["grand_total"])
        if pre + post != gt:
            fails.append("arithmetic: pre_2026_total (%d) + post_2026_total (%d) != grand_total (%d)" % (pre, post, gt))
        if pre <= 0:
            fails.append("pre_2026_total must be positive (got %d)" % pre)
        if post <= 0:
            fails.append("post_2026_total must be positive — post-SB596 daily violations remain after supersede")
        if gt <= 0:
            fails.append("grand_total must be positive (got %d)" % gt)
    except (TypeError, ValueError) as exc:
        fails.append("pre/post/grand_total must be integers: %s" % exc)
        _finish(fails)
    # Q12 grand_total must differ from Q9 (U2 supersede changed violation count)
    q9, e9 = _load_json(ws / "output" / "penalty_assessment_v2.json")
    if not e9 and q9 is not None:
        q9_gt = q9.get("grand_total_penalty")
        try:
            if int(data["grand_total"]) == int(q9_gt):
                fails.append("grand_total (%d) equals Q9 total — U2 supersede must change the penalty" % int(data["grand_total"]))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
'''

# Q13: npg12_gap_analysis.json — has NPG.12.02.01 EP4 and NPG.12.06.01 EP1; effective_date 2026-01-01; ≥8 entries
# 加难 D：EP entries 从 ≥6 提高到 ≥8（要求覆盖更多 NPG 12 要求，gemma 往往只填最少量）
# 同时强化：action_required 字段必须存在于每个 EP 条目中（不能省略）
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "npg12_gap_analysis.json")
    if err: _finish([err])
    # elements array
    eps = data.get("elements_of_performance") or data.get("elements") or data.get("eps") or []
    if not isinstance(eps, list):
        _finish(["elements_of_performance must be an array"])
    # 真值层 (D加难)：至少 8 个 EP 条目（NPG 12 共有多个 EP，全面分析需要覆盖 8+ 个）
    if len(eps) < 8:
        fails.append(
            "elements_of_performance has %d entries (expected >= 8; "
            "JC NPG 12 requires analysis of at least 8 Elements of Performance across "
            "NPG.12.01, NPG.12.02, and NPG.12.06 standards)" % len(eps))
    # must have EP NPG.12.02.01 EP4
    found_1202_ep4 = any(
        "12.02.01" in str(e.get("ep_id", "")) and "ep4" in str(e.get("ep_id", "")).lower()
        for e in eps if isinstance(e, dict)
    )
    if not found_1202_ep4:
        # also accept it embedded in requirement text
        found_1202_ep4 = any(
            "12.02.01" in str(e.get("ep_id", "")) and (
                "24" in str(e.get("requirement", "")) or "rn oversight" in str(e.get("requirement", "")).lower()
            )
            for e in eps if isinstance(e, dict)
        )
    if not found_1202_ep4:
        fails.append("no EP entry with ep_id containing 'NPG.12.02.01' and EP4 (24/7 RN oversight)")
    # must have EP NPG.12.06.01 EP1
    found_1206_ep1 = any(
        "12.06.01" in str(e.get("ep_id", ""))
        for e in eps if isinstance(e, dict)
    )
    if not found_1206_ep1:
        fails.append("no EP entry with ep_id containing 'NPG.12.06.01' (QAPI integration)")
    # effective_date 2026-01-01 somewhere in the data
    data_str = json.dumps(data)
    if "2026-01-01" not in data_str and "2026" not in data_str:
        fails.append("effective_date '2026-01-01' not found anywhere in npg12_gap_analysis.json")
    # 真值层 (D加难)：每个 EP 条目必须包含 action_required 字段
    eps_missing_action = [
        str(e.get("ep_id", "ep[%d]" % i))
        for i, e in enumerate(eps)
        if isinstance(e, dict) and not e.get("action_required")
    ]
    if eps_missing_action:
        fails.append(
            "EP entries missing action_required field: %s (all EP entries must include a concrete action)" % eps_missing_action[:3])
    _finish(fails)
main()
'''

# Q14: ca_vs_or_comparison.json — ICU both=2; Med/Surg ca=5, or2024=5, or2026=4, stricter=true; penalties
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "ca_vs_or_comparison.json")
    if err: _finish([err])
    # top-level penalty fields
    or_pen = data.get("or_penalty_max_usd")
    ca_pen = data.get("ca_first_violation_usd")
    try:
        if int(or_pen) != 5000:
            fails.append("or_penalty_max_usd == %r (expected 5000 per OR HB 2697)" % or_pen)
    except (TypeError, ValueError):
        fails.append("or_penalty_max_usd not an int: %r" % or_pen)
    try:
        if int(ca_pen) != 15000:
            fails.append("ca_first_violation_usd == %r (expected 15000 per H&SC § 1280.3)" % ca_pen)
    except (TypeError, ValueError):
        fails.append("ca_first_violation_usd not an int: %r" % ca_pen)
    # units array
    units = data.get("units") or []
    if not isinstance(units, list) or len(units) < 2:
        fails.append("units array must have at least 2 entries")
        _finish(fails)
    def norm(s): return str(s).lower().replace("-", "").replace("/", "").replace(" ", "")
    by_unit = {norm(e.get("unit", "")): e for e in units if isinstance(e, dict)}
    # ICU: ca=2, or2024=2, or2026=2
    icu = None
    for k in ("icu", "intensivecareunit", "criticalcare"):
        if k in by_unit:
            icu = by_unit[k]; break
    if icu:
        for field, expected in [("ca_ratio", 2), ("or_ratio_2024", 2), ("or_ratio_2026", 2)]:
            try:
                if int(icu.get(field, -1)) != expected:
                    fails.append("ICU %s == %r (expected %d)" % (field, icu.get(field), expected))
            except (TypeError, ValueError):
                fails.append("ICU %s not an int: %r" % (field, icu.get(field)))
    else:
        fails.append("no ICU entry in units array")
    # Med/Surg: ca=5, or2024=5, or2026=4, or_stricter_by_2026=true
    ms = None
    for k in ("medsurg", "medicalsurgical", "medicalsurg"):
        if k in by_unit:
            ms = by_unit[k]; break
    if ms:
        for field, expected in [("ca_ratio", 5), ("or_ratio_2024", 5), ("or_ratio_2026", 4)]:
            try:
                if int(ms.get(field, -1)) != expected:
                    fails.append("Med/Surg %s == %r (expected %d)" % (field, ms.get(field), expected))
            except (TypeError, ValueError):
                fails.append("Med/Surg %s not an int: %r" % (field, ms.get(field)))
        if ms.get("or_stricter_by_2026") is not True:
            fails.append("Med/Surg or_stricter_by_2026 must be true (OR goes to 1:4 in 2026, CA stays 1:5)")
    else:
        fails.append("no Med/Surg entry in units array")
    _finish(fails)
main()
'''

# Q15: cdph_staffing_log_week2.csv — same as Q8 but ICU must show ≥3 float pool nurses
CHECKS["check_q15"] = '''
LEGAL_MAX = {"ICU": 2.0, "Med/Surg": 5.0, "Step-Down": 3.0, "Telemetry": 4.0,
             "ED": 4.0, "Psychiatric": 6.0}

def _get_legal_max(unit_str):
    u = str(unit_str).strip()
    for k, v in LEGAL_MAX.items():
        if k.lower() in u.lower() or u.lower() in k.lower():
            return v
    return None

def main():
    ws = Path(sys.argv[1]); fails = []
    rows, err = _read_csv(ws / "output" / "cdph_staffing_log_week2.csv")
    if err: _finish([err])
    if not rows:
        _finish(["cdph_staffing_log_week2.csv is empty"])
    req = {"date", "unit", "nurse_id", "license_type", "patient_count", "ratio"}
    missing = req - set(rows[0].keys())
    if missing:
        fails.append("missing columns: %s" % sorted(missing))
    if fails: _finish(fails)
    valid_lic = {"RN", "LVN", "PT"}
    for i, r in enumerate(rows):
        lic = str(r.get("license_type", "")).strip().upper()
        if lic not in valid_lic:
            fails.append("row %d: license_type %r not valid" % (i+1, lic))
            continue
        unit = str(r.get("unit", ""))
        try:
            pc = int(r.get("patient_count", 0))
        except (ValueError, TypeError):
            pc = 0
        if pc == 0:
            continue
        lm = _get_legal_max(unit)
        if lm is None:
            continue
        ratio_str = str(r.get("ratio", "")).strip()
        try:
            ratio = float(ratio_str)
            if ratio > lm + 1e-9:
                fails.append("row %d: ratio %.2f > legal max %.1f for unit %r" % (i+1, ratio, lm, unit))
        except (ValueError, TypeError):
            fails.append("row %d: ratio %r not numeric" % (i+1, ratio_str))
    # Update 2 requirement: ICU must have >= 3 float pool nurses per shift
    # Check: count distinct nurse_ids in ICU with patient_count > 0
    from collections import defaultdict
    icu_shift_nurses = defaultdict(set)
    for r in rows:
        if "icu" not in str(r.get("unit", "")).lower():
            continue
        try:
            pc = int(r.get("patient_count", 0))
        except (ValueError, TypeError):
            pc = 0
        if pc > 0:
            shift_key = (str(r.get("date", "")), str(r.get("shift_start", "")))
            icu_shift_nurses[shift_key].add(str(r.get("nurse_id", "")))
    if icu_shift_nurses:
        max_icu_nurses = max(len(v) for v in icu_shift_nurses.values())
        if max_icu_nurses < 3:
            fails.append("ICU must have >= 3 nurses per shift (Update 2 float pool requirement); max found: %d" % max_icu_nurses)
    else:
        fails.append("no ICU rows found in week2 log")
    _finish(fails)
main()
'''

# Q16: submission_manifest.json — contains 4 required files; sha256 hashes correct
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "submission_manifest.json")
    if err: _finish([err])
    files = data.get("files", [])
    if not isinstance(files, list) or len(files) == 0:
        _finish(["files array is empty"])
    # required files
    required = {
        "cdph_staffing_log_week1.csv",
        "cdph_staffing_log_week2.csv",
        "violation_ledger_final.json",
        "penalty_final.json",
    }
    found_paths = set()
    for entry in files:
        if isinstance(entry, dict):
            p = str(entry.get("path", ""))
            found_paths.add(Path(p).name)
    missing_req = required - found_paths
    if missing_req:
        fails.append("missing required files in manifest: %s" % sorted(missing_req))
    # sha256 hashes must match actual file content
    for entry in files:
        if not isinstance(entry, dict):
            continue
        p_str = str(entry.get("path", ""))
        sha_manifest = str(entry.get("sha256", "")).lower().strip()
        if not sha_manifest:
            fails.append("entry %r has no sha256" % p_str)
            continue
        # resolve path
        target = ws / "output" / Path(p_str).name
        if not target.exists():
            # try as relative path from workspace
            target2 = ws / p_str
            if target2.exists():
                target = target2
            else:
                fails.append("manifest file %r not found at %s or %s" % (p_str, target, target2))
                continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if sha_manifest != actual:
            fails.append("sha256 mismatch for %s: manifest=%s actual=%s" % (
                Path(p_str).name, sha_manifest[:12], actual[:12]))
    _finish(fails)
main()
'''

# Q17: verification_report.txt — first line VERIFIED:<sha256 of submission_manifest.json>
CHECKS["check_q17"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "verification_report.txt")
    if txt is None:
        _finish(["file not found: output/verification_report.txt"])
    first_line = txt.strip().splitlines()[0] if txt.strip() else ""
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", first_line)
    if not m:
        _finish(["first line must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % first_line[:80]])
    # recompute hash of submission_manifest.json
    manifest_path = ws / "output" / "submission_manifest.json"
    if not manifest_path.exists():
        _finish(["cannot verify: output/submission_manifest.json missing"])
    actual = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    if m.group(1) != actual:
        fails.append("sha256 mismatch: report=%s recomputed=%s" % (m.group(1)[:12], actual[:12]))
    _finish(fails)
main()
'''

# check_preferences.py — P1-P5
PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sci3 preference checker (P1-P5).

P1: all monetary JSON fields are integers (no decimal, no thousand separator)
P2: Markdown reports use ### (level-3) headings, not ## (level-2)
P3: CSV files UTF-8, date fields YYYY-MM-DD, ratio fields two decimal places
P4: JSON field names snake_case; array fields plural
P5: recommendation/action fields plain text, no nested JSON, <= 150 chars
"""
import sys, re, json, argparse, csv
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Monetary fields in JSON must be integers (no float/string with decimal)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    if not target.endswith(".json"):
        return True, "P1: not a JSON file, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    # Find any key that looks currency-related
    money_keys = re.compile(r"(fee|usd|penalty|total|amount|fine)", re.I)
    fails = []
    def _check_val(key, val, path):
        if money_keys.search(key):
            if isinstance(val, float):
                fails.append("P1: field %s is a float (%.6g); monetary fields must be integers" % (path, val))
            elif isinstance(val, str) and re.match(r"[\\$]", val.strip()):
                fails.append("P1: field %s contains currency symbol %r; use plain integer" % (path, val[:20]))
    def _walk(obj, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                _check_val(k, v, prefix + k)
                _walk(v, prefix + k + ".")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                _walk(v, prefix + "[%d]." % i)
    _walk(data)
    if fails:
        return False, "P1: " + "; ".join(fails[:2])
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Markdown reports must use ### (not ##) for case/shift headings."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    if not target.endswith(".md"):
        return True, "P2: not a Markdown file, skip"
    # Look for ## headings that are NOT ### (i.e., exactly 2 hashes at line start)
    bad = re.findall(r"^## (?!#)", txt, re.MULTILINE)
    if bad:
        return False, "P2: found %d ## (level-2) headings; all case/shift sections must use ### (level-3)" % len(bad)
    h3 = re.findall(r"^### ", txt, re.MULTILINE)
    if not h3:
        return False, "P2: no ### (level-3) headings found in Markdown file"
    return True, "P2: PASSED"


def check_P3(ws, target):
    """CSV files: UTF-8, date YYYY-MM-DD, ratio two decimal places."""
    p = ws / target
    if not p.exists():
        return True, "P3: target missing, skip"
    if not target.endswith(".csv"):
        return True, "P3: not a CSV file, skip"
    try:
        with p.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
    except UnicodeDecodeError:
        return False, "P3: CSV is not UTF-8 encoded"
    except Exception as e:
        return False, "P3: CSV read error: %s" % e
    if not rows:
        return True, "P3: empty CSV, skip"
    # Date fields: check YYYY-MM-DD
    date_re = re.compile(r"^\\d{4}-\\d{2}-\\d{2}$")
    date_fields = [k for k in rows[0].keys() if "date" in k.lower()]
    for r in rows[:50]:  # sample first 50
        for df in date_fields:
            v = str(r.get(df, "")).strip()
            if v and not date_re.match(v):
                return False, "P3: date field %r has value %r (expected YYYY-MM-DD)" % (df, v)
    # Ratio fields: check two decimal places
    ratio_fields = [k for k in rows[0].keys() if "ratio" in k.lower()]
    ratio_re = re.compile(r"^-?\\d+\\.\\d{2}$")
    for r in rows[:50]:
        for rf in ratio_fields:
            v = str(r.get(rf, "")).strip()
            if v and v not in ("", "0"):
                if not ratio_re.match(v):
                    return False, "P3: ratio field %r has value %r (expected two decimal places like 2.50)" % (rf, v)
    return True, "P3: PASSED"


def check_P4(ws, target):
    """JSON field names must be snake_case; array fields plural."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    if not target.endswith(".json"):
        return True, "P4: not a JSON file, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P4: target is not valid JSON"
    camel_re = re.compile(r"[a-z][A-Z]")  # camelCase detector
    fails = []
    def _check_keys(obj, prefix=""):
        if isinstance(obj, dict):
            for k in obj.keys():
                if camel_re.search(k):
                    fails.append("key %r contains camelCase (use snake_case)" % k)
                # array fields should be plural — light check: if value is a list, key should end with s
                if isinstance(obj[k], list) and len(obj[k]) > 0:
                    if k.endswith("_list") or k == "list":
                        fails.append("array field %r should use plural noun, not *_list suffix" % k)
                _check_keys(obj[k], prefix + k + ".")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                _check_keys(v, prefix + "[%d]." % i)
    _check_keys(data)
    if fails:
        return False, "P4: " + "; ".join(fails[:2])
    return True, "P4: PASSED"


def check_P5(ws, target):
    """recommendation/action fields: plain text, no nested JSON, <= 150 chars."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    if not target.endswith(".json"):
        return True, "P5: not a JSON file, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P5: target is not valid JSON"
    rec_keys = re.compile(r"(recommendation|action_required|action)", re.I)
    fails = []
    def _check_rec(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if rec_keys.match(k):
                    if isinstance(v, dict) or isinstance(v, list):
                        fails.append("field %r must be plain text string, not nested JSON" % k)
                    elif isinstance(v, str):
                        if len(v) > 150:
                            fails.append("field %r exceeds 150 chars (got %d)" % (k, len(v)))
                else:
                    _check_rec(v)
        elif isinstance(obj, list):
            for v in obj:
                _check_rec(v)
    _check_rec(data)
    if fails:
        return False, "P5: " + "; ".join(fails[:2])
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="output/")
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
        content = HEADER + "\n" + body.strip() + "\nmain()\n"
        (OUT / f"{name}.py").write_text(content, encoding="utf-8")
    (OUT / "check_preferences.py").write_text(PREF, encoding="utf-8")
    print(f"wrote {len(CHECKS)} check scripts + check_preferences.py to {OUT}")


if __name__ == "__main__":
    main()
