#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_sci5_checks.py — 生成 sci5 的全部 exec_check 校验脚本到 eval/sci5/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_sci5.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5（与 sci5 使用的 P1/P2/P3/P4/P5 对应）。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/sci5/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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

# Q1 — FMLA 资格核查
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "fmla_eligibility_check.json")
    if err: _finish([err])
    # 结构层
    for key in ("employer_covered", "employee_eligible", "weeks_entitled"):
        if key not in data:
            fails.append("missing key: " + key)
    if fails: _finish(fails)
    # 字段层
    if data.get("employer_covered") is not True:
        fails.append("employer_covered must be true (320 employees > 50 threshold)")
    if data.get("employee_eligible") is not True:
        fails.append("employee_eligible must be true (tenure 4.5 yrs, hours 1310 > 1250)")
    we = data.get("weeks_entitled")
    try:
        if int(we) != 12:
            fails.append("weeks_entitled == %r (expected 12)" % we)
    except (TypeError, ValueError):
        fails.append("weeks_entitled not an int: %r" % we)
    _finish(fails)
main()
'''

# Q2 — PIP 合规分析（pip_v1，21天，违反公司政策30天）
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "pip_compliance.json")
    if err: _finish([err])
    dd = data.get("duration_days")
    try:
        if int(dd) != 21:
            fails.append("duration_days == %r (expected 21 from pip_v1)" % dd)
    except (TypeError, ValueError):
        fails.append("duration_days not an int: %r" % dd)
    if data.get("compliant") is not False:
        fails.append("compliant == %r (expected false — 21 days < 30-day company policy minimum)" % data.get("compliant"))
    mr = data.get("minimum_required_days")
    try:
        if int(mr) != 30:
            fails.append("minimum_required_days == %r (expected 30 per HR Handbook Section 4.3)" % mr)
    except (TypeError, ValueError):
        fails.append("minimum_required_days not an int: %r" % mr)
    # V9: policy_source must reference company handbook / Section 4.3
    ps = str(data.get("policy_source") or "").lower()
    if not (re.search(r"section\\s*4\\.3", ps) or re.search(r"hr\\s*handbook", ps) or re.search(r"handbook", ps)):
        fails.append("policy_source must reference HR Handbook Section 4.3 (got: %r)" % data.get("policy_source"))
    _finish(fails)
main()
'''

# Q3 — FMLA 保护期与解雇时间线（V1 多源冲突：Slack DM 声称09-10，personnel file 是09-12）
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "fmla_timeline.json")
    if err: _finish([err])
    # fmla_start_date
    fsd = str(data.get("fmla_start_date") or "")
    if "2025-08-15" not in fsd:
        fails.append("fmla_start_date must contain 2025-08-15 (got %r)" % fsd)
    # fmla_end_date: 12 weeks = 84 days from 2025-08-15 = 2025-11-07
    fed = str(data.get("fmla_end_date") or "")
    if "2025-11-07" not in fed:
        fails.append("fmla_end_date must contain 2025-11-07 (12 weeks from 2025-08-15; got %r)" % fed)
    # termination_date: must be 2025-09-12 (personnel file), NOT 2025-09-10 (Slack DM — V1 decoy)
    td = str(data.get("termination_date") or "")
    if "2025-09-12" not in td:
        fails.append("termination_date must be 2025-09-12 per personnel file (not 2025-09-10 from Slack DM — that is a V1 multi-source conflict; personnel file is authoritative)")
    # in_protection_window
    if data.get("in_protection_window") is not True:
        fails.append("in_protection_window must be true (2025-09-12 is within 2025-08-15 to 2025-11-07)")
    # risk_level
    rl = str(data.get("risk_level") or "").upper()
    if rl != "HIGH":
        fails.append("risk_level must be HIGH (got %r)" % data.get("risk_level"))
    _finish(fails)
main()
'''

# Q4 — 伪装性解雇评估（V5：BOT 摘要声称承包商在 Marcus 离职后才开始）
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "pretext_risk_assessment.json")
    if err: _finish([err])
    cod = data.get("contractor_overlap_days")
    try:
        cod = int(cod)
        # CTR-2025-041 started 2025-09-02; termination 2025-09-12; gap = 10 days
        # allow 8-12 to accommodate ±2 day parsing variance
        if not (8 <= cod <= 12):
            fails.append("contractor_overlap_days == %d (expected ~10; CTR-2025-041 started 2025-09-02, termination 2025-09-12)" % cod)
    except (TypeError, ValueError):
        fails.append("contractor_overlap_days not an int: %r" % cod)
    pr = data.get("performance_rating_2024_q3")
    try:
        prf = float(pr)
        # Q3 rating 2.1, allow ±0.2
        if not (1.9 <= prf <= 2.3):
            fails.append("performance_rating_2024_q3 == %s (expected ~2.1)" % pr)
    except (TypeError, ValueError):
        fails.append("performance_rating_2024_q3 not numeric: %r" % pr)
    pi = data.get("pretext_indicators")
    if not isinstance(pi, list) or len(pi) < 2:
        fails.append("pretext_indicators must be a list with >= 2 items (got %r)" % pi)
    rs = data.get("risk_score")
    try:
        if int(rs) < 70:
            fails.append("risk_score == %d (expected >= 70)" % int(rs))
    except (TypeError, ValueError):
        fails.append("risk_score not an int: %r" % rs)
    _finish(fails)
main()
'''

# Q5 — 联邦 WARN Act 分析（V5：GC v1 memo 声称 500 人阈值）
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "warn_federal.json")
    if err: _finish([err])
    if data.get("employer_qualifies") is not True:
        fails.append("employer_qualifies must be true (320 employees > 100 threshold per 29 U.S.C. § 2101(a)(1); NOT 500 — the GC v1 memo error)")
    ea = data.get("employees_affected")
    try:
        if int(ea) != 58:
            fails.append("employees_affected == %r (expected 58 from restructuring_plan_v1.md)" % ea)
    except (TypeError, ValueError):
        fails.append("employees_affected not an int: %r" % ea)
    nd = data.get("notice_days_required")
    try:
        if int(nd) != 60:
            fails.append("notice_days_required == %r (expected 60 per 29 U.S.C. § 2102)" % nd)
    except (TypeError, ValueError):
        fails.append("notice_days_required not an int: %r" % nd)
    # applicable_rule must reference plant closing or mass layoff (not just "warn act")
    ar = str(data.get("applicable_rule") or "").lower()
    if not (re.search(r"plant.clos", ar) or re.search(r"mass.layoff", ar)):
        fails.append("applicable_rule must reference 'plant closing' or 'mass layoff' (got %r)" % data.get("applicable_rule"))
    # must NOT just reference the 500-person threshold
    if re.search(r"500.*(threshold|employer)", ar):
        fails.append("applicable_rule appears to use the GC v1 erroneous 500-person threshold")
    _finish(fails)
main()
'''

# Q6 — Cal-WARN 分析（V9：精确引用 Labor Code §1400）
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "warn_california.json")
    if err: _finish([err])
    if data.get("applies") is not True:
        fails.append("applies must be true (320 employees > 75 Cal-WARN threshold)")
    et = data.get("employer_threshold")
    try:
        if int(et) != 75:
            fails.append("employer_threshold == %r (expected 75 per California Labor Code § 1400)" % et)
    except (TypeError, ValueError):
        fails.append("employer_threshold not an int: %r" % et)
    tt = data.get("trigger_threshold")
    try:
        if int(tt) != 50:
            fails.append("trigger_threshold == %r (expected 50 — Cal-WARN has no 33%% ratio requirement, unlike federal)" % tt)
    except (TypeError, ValueError):
        fails.append("trigger_threshold not an int: %r" % tt)
    nd = data.get("notice_days")
    try:
        if int(nd) != 60:
            fails.append("notice_days == %r (expected 60)" % nd)
    except (TypeError, ValueError):
        fails.append("notice_days not an int: %r" % nd)
    # additional_obligations must mention California EDD
    ao = data.get("additional_obligations") or []
    ao_text = " ".join(str(x) for x in ao).lower()
    if not re.search(r"(edd|employment development|california employment)", ao_text):
        fails.append("additional_obligations must mention California Employment Development Department (EDD)")
    _finish(fails)
main()
'''

# Q7 — NYS WARN Act 分析 v1（将被 Q12 supersede）
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "warn_nys_v1.json")
    if err: _finish([err])
    nd = data.get("notice_days")
    try:
        if int(nd) != 90:
            fails.append("notice_days == %r (expected 90 per NY Labor Law § 860-b 2023 amendment)" % nd)
    except (TypeError, ValueError):
        fails.append("notice_days not an int: %r" % nd)
    th = data.get("threshold")
    try:
        if int(th) != 25:
            fails.append("threshold == %r (expected 25 — NYS WARN plant closing trigger, lower than federal 50)" % th)
    except (TypeError, ValueError):
        fails.append("threshold not an int: %r" % th)
    # F: ny_employees_affected must be exactly 11 (from restructuring_plan_v1.md NY office)
    ny_ea = data.get("ny_employees_affected")
    try:
        if int(ny_ea) != 11:
            fails.append("ny_employees_affected == %r (expected 11 — restructuring_plan_v1.md NY office headcount)" % ny_ea)
    except (TypeError, ValueError):
        fails.append("ny_employees_affected not an int: %r" % ny_ea)
    # F: triggered must be false (11 < 25)
    if data.get("triggered") is not False:
        fails.append("triggered must be false (11 NY employees < 25 plant closing threshold under Plan v1)")
    _finish(fails)
main()
'''

# Q8 — ADEA / OWBPA 合规（V1：Slack DM 误引 45 天，正确是 21 天个人解雇）
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "adea_compliance.json")
    if err: _finish([err])
    age = data.get("employee_age")
    try:
        if int(age) != 42:
            fails.append("employee_age == %r (expected 42 from employee_roster.csv EMP-0042)" % age)
    except (TypeError, ValueError):
        fails.append("employee_age not an int: %r" % age)
    if data.get("adea_protected") is not True:
        fails.append("adea_protected must be true (age 42 >= 40)")
    cd = data.get("consideration_days")
    try:
        if int(cd) != 21:
            fails.append("consideration_days == %r (expected 21 for INDIVIDUAL termination; 45 days is for GROUP terminations — Marcus\\'s Slack DM claim of 45 days is incorrect)" % cd)
    except (TypeError, ValueError):
        fails.append("consideration_days not an int: %r" % cd)
    rd = data.get("revocation_days")
    try:
        if int(rd) != 7:
            fails.append("revocation_days == %r (expected 7 — irrevocable)" % rd)
    except (TypeError, ValueError):
        fails.append("revocation_days not an int: %r" % rd)
    _finish(fails)
main()
'''

# Q9 — EEOC 申诉期（V4：日期从 Q3 延续）
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "eeoc_deadline.json")
    if err: _finish([err])
    if data.get("state_agency_exists") is not True:
        fails.append("state_agency_exists must be true (California CRD exists)")
    fdd = data.get("filing_deadline_days")
    try:
        if int(fdd) != 300:
            fails.append("filing_deadline_days == %r (expected 300 — California is a deferral state)" % fdd)
    except (TypeError, ValueError):
        fails.append("filing_deadline_days not an int: %r" % fdd)
    # deadline_date must be 2026-07-08 (300 days from 2025-09-12)
    dd = str(data.get("deadline_date") or "")
    if "2026-07-08" not in dd:
        fails.append("deadline_date must contain 2026-07-08 (300 days from 2025-09-12; got %r)" % dd)
    # statute_basis must reference Title VII and ADEA
    sb = str(data.get("statute_basis") or "").lower()
    if "title vii" not in sb and "42 u.s.c" not in sb and "2000e" not in sb:
        fails.append("statute_basis must reference Title VII / 42 U.S.C. § 2000e (got %r)" % data.get("statute_basis"))
    if "adea" not in sb and "age discrimination" not in sb:
        fails.append("statute_basis must reference ADEA (got %r)" % data.get("statute_basis"))
    _finish(fails)
main()
'''

# Q10 — 联邦 WARN 通知起草（V3/V9：文件头格式 P2；footer P3；29 U.S.C. § 2102）
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "warn_notice_federal_final.md")
    if txt is None:
        _finish(["file not found: warn_notice_federal_final.md"])
    low = txt.lower()
    # 60 天通知期
    if not re.search(r"\\b60\\b", txt):
        fails.append("notice must contain '60' (days notice period)")
    # 受影响员工数 >= 50
    nums = [int(x) for x in re.findall(r"\\b(\\d+)\\b", txt) if 50 <= int(x) <= 500]
    if not nums:
        fails.append("notice must reference employee count >= 50")
    # plant closing 或 mass layoff
    if not (re.search(r"plant.clos", low) or re.search(r"mass.layoff", low)):
        fails.append("notice must reference 'plant closing' or 'mass layoff'")
    # V9: 29 U.S.C. § 2102
    if not re.search(r"29\\s*u\\.s\\.c\\.?\\s*[§s]\\s*2102", low):
        fails.append("notice must cite 29 U.S.C. § 2102 (verbatim statutory citation required)")
    # P2: document header block
    if not re.search(r"document:.*version:.*date:.*status:", low):
        fails.append("document must carry header: Document: [...] | Version: [...] | Date: [...] | Status: [...]")
    # P3: footer
    if not re.search(r"prepared by.*people operations", low):
        fails.append("document must carry footer: Prepared by: People Operations | Review required before distribution")
    _finish(fails)
main()
'''

# Q11 — Cal-WARN 通知（V9：California Employment Development Department 全称）
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "warn_notice_cal_final.md")
    if txt is None:
        _finish(["file not found: warn_notice_cal_final.md"])
    low = txt.lower()
    # V9: verbatim full name — "california employment development department"
    if "california employment development department" not in low:
        fails.append("document must contain 'California Employment Development Department' (exact full name — not just 'EDD')")
    # 60 days
    if not re.search(r"\\b60\\b", txt):
        fails.append("notice must contain '60' (days notice period)")
    # trigger: 50
    if not re.search(r"\\b50\\b", txt):
        fails.append("notice must reference '50' (Cal-WARN trigger threshold)")
    # P2: document header
    if not re.search(r"document:.*version:.*date:.*status:", low):
        fails.append("document must carry header: Document: [...] | Version: [...] | Date: [...] | Status: [...]")
    # P3: footer
    if not re.search(r"prepared by.*people operations", low):
        fails.append("document must carry footer: Prepared by: People Operations | Review required before distribution")
    _finish(fails)
main()
'''

# Q12 — NYS WARN v2 + supersede_log（V2/V10：Update 2 反转）
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    # warn_nys_v2.json
    v2, err = _load_json(ws / "reports" / "warn_nys_v2.json")
    if err: _finish([err])
    ea = v2.get("employees_affected")
    try:
        if int(ea) != 31:
            fails.append("warn_nys_v2: employees_affected == %r (expected 31 from restructuring_plan_v2.md)" % ea)
    except (TypeError, ValueError):
        fails.append("warn_nys_v2: employees_affected not an int: %r" % ea)
    th = v2.get("threshold")
    try:
        if int(th) != 25:
            fails.append("warn_nys_v2: threshold == %r (expected 25)" % th)
    except (TypeError, ValueError):
        fails.append("warn_nys_v2: threshold not an int: %r" % th)
    if v2.get("triggered") is not True:
        fails.append("warn_nys_v2: triggered must be true (31 >= 25)")
    nd = v2.get("notice_days")
    try:
        if int(nd) != 90:
            fails.append("warn_nys_v2: notice_days == %r (expected 90)" % nd)
    except (TypeError, ValueError):
        fails.append("warn_nys_v2: notice_days not an int: %r" % nd)
    # F: plan_version must reference "v2"
    pv = str(v2.get("plan_version") or "")
    if "v2" not in pv.lower():
        fails.append("warn_nys_v2: plan_version must reference 'v2' (got %r)" % pv)
    # supersede_log.json — V10: must record Q7 superseded
    sl, err2 = _load_json(ws / "reports" / "supersede_log.json")
    if err2:
        fails.append("supersede_log.json: " + err2)
    else:
        log_text = json.dumps(sl).lower()
        if not (re.search(r"q7|warn_nys_v1|warn.nys.v1", log_text)):
            fails.append("supersede_log.json must reference Q7 or warn_nys_v1 as superseded by Q12 or warn_nys_v2")
        # C: supersede_log must mention the changed triggered status or employee count
        if not (re.search(r"31|false.*true|true.*false|trigger", log_text)):
            fails.append("supersede_log.json must record the substantive change: triggered status changed from false (v1: 11<25) to true (v2: 31>=25)")
    _finish(fails)
main()
'''

# Q13 — 风险矩阵 CSV（V4 数值一致性 + C★ 跨轮引用；P5 UTF-8 BOM）
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    p = ws / "reports" / "risk_matrix_final.csv"
    if not p.exists():
        _finish(["file not found: reports/risk_matrix_final.csv"])
    # P5: UTF-8 with BOM
    raw = p.read_bytes()
    if not raw.startswith(b"\\xef\\xbb\\xbf"):
        fails.append("risk_matrix_final.csv must begin with UTF-8 BOM bytes (\\xef\\xbb\\xbf) per P5")
    # parse CSV
    try:
        text = raw[3:].decode("utf-8") if raw.startswith(b"\\xef\\xbb\\xbf") else raw.decode("utf-8")
        rows = list(csv.DictReader(text.splitlines()))
    except Exception as e:
        _finish(["CSV parse error: " + str(e)])
    # A: >= 8 data rows (expanded from 6 — covers all major risk areas in this scenario)
    if len(rows) < 8:
        fails.append("risk_matrix_final.csv must have >= 8 data rows covering all major risk areas (got %d)" % len(rows))
    # severity values
    valid_sev = {"HIGH", "MEDIUM", "LOW"}
    for r in rows:
        sev = str(r.get("severity") or "").strip().upper()
        if sev not in valid_sev:
            fails.append("row %r has invalid severity %r (must be HIGH, MEDIUM, or LOW)" % (r.get("risk_id"), sev))
        # D: recommended_action must not be empty
        ra = str(r.get("recommended_action") or "").strip()
        if not ra:
            fails.append("row %r has empty recommended_action (every risk row must include a concrete action)" % r.get("risk_id"))
    # FMLA row must be HIGH
    fmla_rows = [r for r in rows if re.search(r"fmla", str(r.get("law") or "") + str(r.get("risk_description") or ""), re.I)]
    if not fmla_rows:
        fails.append("no FMLA risk row found in risk_matrix_final.csv")
    else:
        for r in fmla_rows:
            if str(r.get("severity") or "").strip().upper() != "HIGH":
                fails.append("FMLA risk row must have severity HIGH (got %r)" % r.get("severity"))
    # Cal-WARN row must be HIGH
    cal_rows = [r for r in rows if re.search(r"cal.warn|california.warn|cal_warn", str(r.get("law") or "") + str(r.get("risk_description") or ""), re.I)]
    if not cal_rows:
        fails.append("no Cal-WARN risk row found in risk_matrix_final.csv")
    else:
        for r in cal_rows:
            if str(r.get("severity") or "").strip().upper() != "HIGH":
                fails.append("Cal-WARN risk row must have severity HIGH (got %r)" % r.get("severity"))
    # D: must include a NYS WARN row
    nys_rows = [r for r in rows if re.search(r"nys.warn|new york.warn|ny.warn|nys_warn", str(r.get("law") or "") + str(r.get("risk_description") or ""), re.I)]
    if not nys_rows:
        fails.append("no NYS WARN risk row found in risk_matrix_final.csv")
    else:
        # C: NYS WARN row must reflect v2 analysis (31 employees, 90-day notice)
        nys_combined = " ".join(str(r.get("law") or "") + " " + str(r.get("risk_description") or "") + " " + str(r.get("recommended_action") or "") for r in nys_rows)
        if not re.search(r"\\b31\\b", nys_combined):
            fails.append("NYS WARN row must reference '31' (NY employees under restructuring_plan_v2.md — v2 supersedes v1's 11 employees)")
        if not re.search(r"\\b90\\b", nys_combined):
            fails.append("NYS WARN row must reference '90' (days notice required under NY Labor Law § 860-b 2023 amendment)")
    # D: must include an EEOC/deadline row
    eeoc_rows = [r for r in rows if re.search(r"eeoc|filing.deadline|civil rights department|crd", str(r.get("law") or "") + str(r.get("risk_description") or ""), re.I)]
    if not eeoc_rows:
        fails.append("no EEOC filing deadline risk row found in risk_matrix_final.csv")
    else:
        # C: EEOC row must carry the exact deadline date from Q9 (cross-round consistency)
        eeoc_combined = " ".join(str(r.get("law") or "") + " " + str(r.get("risk_description") or "") + " " + str(r.get("recommended_action") or "") for r in eeoc_rows)
        if "2026-07-08" not in eeoc_combined:
            fails.append("EEOC risk row must include the exact deadline date '2026-07-08' (300 days from 2025-09-12 — cross-round consistency with Q9 eeoc_deadline.json)")
    _finish(fails)
main()
'''

# Q14 — OWBPA 豁免协议（V3/V9：21天/7天/ADEA全称/律师咨询条款）
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "legal" / "owbpa_waiver_marcus.md")
    if txt is None:
        _finish(["file not found: legal/owbpa_waiver_marcus.md"])
    low = txt.lower()
    # 21 days (individual consideration period)
    if not re.search(r"\\b21\\s+days?\\b", low):
        fails.append("owbpa_waiver_marcus.md must contain '21 days' (OWBPA individual consideration period)")
    # 7 days (revocation period)
    if not re.search(r"\\b7\\s+days?\\b", low):
        fails.append("owbpa_waiver_marcus.md must contain '7 days' (OWBPA revocation period)")
    # V9: Age Discrimination in Employment Act (full official name)
    if "age discrimination in employment act" not in low:
        fails.append("owbpa_waiver_marcus.md must contain 'Age Discrimination in Employment Act' (full official name)")
    # attorney consultation advice (mandatory per 29 U.S.C. § 626(f)(1)(E))
    if not (re.search(r"consult.*(attorney|counsel|lawyer)", low) or re.search(r"(attorney|counsel|lawyer).*consult", low)):
        fails.append("owbpa_waiver_marcus.md must contain explicit written advice to consult an attorney (29 U.S.C. § 626(f)(1)(E))")
    # P2: document header block
    if not re.search(r"document:.*version:.*date:.*status:", low):
        fails.append("document must carry header: Document: [...] | Version: [...] | Date: [...] | Status: [...]")
    _finish(fails)
main()
'''

# Q15 — EEOC 投诉草稿（V4：filing_deadline 从 Q9 延续；V8 JSON 结构；C：complainant + date_of_harm 跨轮）
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "legal" / "eeoc_complaint_draft.json")
    if err: _finish([err])
    # bases_of_discrimination must include age AND FMLA retaliation
    bases = [str(x).lower() for x in (data.get("bases_of_discrimination") or [])]
    bases_text = " ".join(bases)
    if not re.search(r"age|adea", bases_text):
        fails.append("bases_of_discrimination must include age discrimination / ADEA")
    if not re.search(r"fmla.retaliat|retaliat.*fmla", bases_text):
        fails.append("bases_of_discrimination must include FMLA retaliation")
    # C: complainant must identify Marcus Webb with employee ID EMP-0042
    complainant = str(data.get("complainant") or "")
    if not re.search(r"marcus.webb", complainant, re.I):
        fails.append("complainant must reference \\'Marcus Webb\\' (got %r)" % complainant)
    if "EMP-0042" not in complainant:
        fails.append("complainant must include employee ID \\'EMP-0042\\' (required for record identification; got %r)" % complainant)
    # filing_deadline must match Q9 output (2026-07-08) — V4 cross-round closure
    fd = str(data.get("filing_deadline") or "")
    # also check Q9 output for cross-round consistency
    q9, e9 = _load_json(ws / "reports" / "eeoc_deadline.json")
    if not e9 and q9 is not None:
        q9_dd = str(q9.get("deadline_date") or "")
        if fd and q9_dd and fd != q9_dd:
            fails.append("filing_deadline %r does not match Q9 eeoc_deadline.deadline_date %r (cross-round consistency required)" % (fd, q9_dd))
    if "2026-07-08" not in fd:
        fails.append("filing_deadline must contain 2026-07-08 (300 days from 2025-09-12; got %r)" % fd)
    # C: date_of_harm must match termination_date from Q3 fmla_timeline.json
    doh = str(data.get("date_of_harm") or "")
    q3, e3 = _load_json(ws / "reports" / "fmla_timeline.json")
    if not e3 and q3 is not None:
        q3_term = str(q3.get("termination_date") or "")
        if doh and q3_term and doh != q3_term:
            fails.append("date_of_harm %r does not match Q3 fmla_timeline.termination_date %r (cross-round consistency: use the personnel file date, not the Slack DM date)" % (doh, q3_term))
    if "2025-09-12" not in doh:
        fails.append("date_of_harm must be 2025-09-12 (Marcus Webb\\'s termination date per personnel file; got %r)" % doh)
    _finish(fails)
main()
'''

# Q16 — SHA-256 sign-off（V7：必须真正运行哈希）
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign = _read(ws / "reports" / "signoff.txt")
    if sign is None:
        _finish(["file not found: reports/signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff line must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    # recompute digest of risk_matrix_final.csv
    csv_path = ws / "reports" / "risk_matrix_final.csv"
    if not csv_path.exists():
        _finish(["cannot verify hash: reports/risk_matrix_final.csv missing"])
    digest = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s... != recomputed %s..." % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

# preference checker — P1/P2/P3/P4/P5
PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sci5 preference checker.

P1 — every JSON output must contain a top-level `reasoning` field.
P2 — formal legal documents must carry the fixed header block.
P3 — all WARN notice drafts must carry the standard footer.
P4 — legal citations must use full citation format (e.g., 29 U.S.C. § 2102).
P5 — CSV files must use UTF-8 with BOM encoding.
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Every JSON output must contain a top-level `reasoning` field."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P1: top-level must be a JSON object"
    if "reasoning" not in data or not data["reasoning"]:
        return False, "P1: missing or empty top-level \\"reasoning\\" field (required in every JSON output)"
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Formal legal documents must carry the fixed header block."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    low = txt.lower()
    # Header: Document: [...] | Version: [...] | Date: [...] | Status: [...]
    if not re.search(r"document:.*version:.*date:.*status:", low):
        return False, "P2: formal legal document missing header block `Document: [...] | Version: [n.n] | Date: [YYYY-MM-DD] | Status: [DRAFT/FINAL]`"
    return True, "P2: PASSED"


def check_P3(ws, target):
    """All WARN notice drafts must carry the standard footer."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    low = txt.lower()
    if not re.search(r"prepared by.*people operations", low):
        return False, "P3: WARN notice missing footer `Prepared by: People Operations | Review required before distribution`"
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Legal citations must use full citation format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    low = txt.lower()
    # If the document references a law by name only (e.g., "the WARN Act says...")
    # without a proper citation, flag it.  We check for common patterns.
    # If it mentions a statute at all, it should have a citation with §
    mentions_law = bool(re.search(
        r"warn act|fmla|adea|owbpa|title vii|cal.warn|29 cfr|29 u\\.s\\.c|42 u\\.s\\.c", low
    ))
    has_citation = bool(re.search(r"§|u\\.s\\.c|cfr|labor code|new york labor", low))
    if mentions_law and not has_citation:
        return False, "P4: document references statutes but lacks full citation format (e.g., 29 U.S.C. § 2102)"
    return True, "P4: PASSED"


def check_P5(ws, target):
    """CSV files must use UTF-8 with BOM encoding."""
    p = Path(ws) / target
    if not p.exists():
        return True, "P5: target missing, skip"
    raw = p.read_bytes()
    if not raw.startswith(b"\\xef\\xbb\\xbf"):
        return False, "P5: CSV file must begin with UTF-8 BOM bytes (\\xef\\xbb\\xbf)"
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="reports/")
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
