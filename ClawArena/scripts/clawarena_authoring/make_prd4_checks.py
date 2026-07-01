#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_prd4_checks.py — 生成 prd4 的全部 exec_check 校验脚本到 eval/prd4/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_prd4.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5。生成器内容即评测逻辑，可逐脚本审阅。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/prd4/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
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

# Q1: policy_summary.json — L1=30, L2=120, L3=480, L4=1440, uptime=99.95, all 4 credit_tiers, sla_policy_version=v1
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "policy_summary.json")
    if err: _finish([err])
    # 结构层：必须有 response_sla
    rs = data.get("response_sla")
    if not isinstance(rs, dict):
        _finish(["response_sla must be an object"])
    # 字段层：L1 response
    l1 = rs.get("L1")
    if isinstance(l1, dict):
        l1_val = l1.get("response_minutes")
    else:
        l1_val = l1
    try:
        l1_int = int(l1_val)
    except (TypeError, ValueError):
        _finish(["L1 response_minutes not a number: %r" % l1_val])
    if l1_int != 30:
        fails.append("L1 response_minutes == %d (expected 30, not 60/1h which is Premium)" % l1_int)
    # L2 response
    l2 = rs.get("L2")
    if isinstance(l2, dict):
        l2_val = l2.get("response_minutes")
    else:
        l2_val = l2
    try:
        l2_int = int(l2_val)
    except (TypeError, ValueError):
        _finish(["L2 response_minutes not a number: %r" % l2_val])
    if l2_int != 120:
        fails.append("L2 response_minutes == %d (expected 120 = 2h)" % l2_int)
    # L3 response
    l3 = rs.get("L3")
    if isinstance(l3, dict):
        l3_val = l3.get("response_minutes")
    else:
        l3_val = l3
    try:
        l3_int = int(l3_val)
        if l3_int != 480:
            fails.append("L3 response_minutes == %d (expected 480 = 8h)" % l3_int)
    except (TypeError, ValueError):
        fails.append("L3 response_minutes not a number or missing: %r" % l3_val)
    # L4 response
    l4 = rs.get("L4")
    if isinstance(l4, dict):
        l4_val = l4.get("response_minutes")
    else:
        l4_val = l4
    try:
        l4_int = int(l4_val)
        if l4_int != 1440:
            fails.append("L4 response_minutes == %d (expected 1440 = 24h)" % l4_int)
    except (TypeError, ValueError):
        fails.append("L4 response_minutes not a number or missing: %r" % l4_val)
    # sla_policy_version must be "v1"
    ver = str(data.get("sla_policy_version") or "")
    if ver != "v1":
        fails.append("sla_policy_version == %r (expected exactly \'v1\')" % ver)
    # plan must reference "Enterprise"
    plan = str(data.get("plan") or "")
    if "Enterprise" not in plan and "enterprise" not in plan.lower():
        fails.append("plan == %r (expected to contain \'Enterprise\')" % plan)
    # 真值层：availability uptime
    upt = data.get("availability_commitment_pct")
    try:
        upt_f = float(upt)
    except (TypeError, ValueError):
        _finish(["availability_commitment_pct not numeric: %r" % upt])
    if abs(upt_f - 99.95) > 0.01:
        fails.append("availability_commitment_pct == %r (expected 99.95)" % upt_f)
    # credit tiers: find tier0 (5% for 99.90-99.95)
    tiers = data.get("credit_tiers") or []
    tier0_found = False
    for t in tiers:
        if isinstance(t, dict):
            pct = t.get("credit_pct")
            rng = str(t.get("uptime_range") or "")
            if pct is not None:
                try:
                    if int(pct) == 5 and ("99.90" in rng or "99.9" in rng):
                        tier0_found = True
                except (ValueError, TypeError):
                    pass
    if not tier0_found:
        fails.append("credit_tiers missing the Enterprise-exclusive 5% tier for 99.90-99.95% range")
    # credit tiers must have all 4 tiers (including tier for < 95.00% at 50%)
    tier50_found = any(
        isinstance(t, dict) and t.get("credit_pct") is not None and
        (lambda v: v == 50)(int(t.get("credit_pct", 0)))
        for t in tiers
    )
    if not tier50_found:
        fails.append("credit_tiers missing the 50%% tier for < 95.00%% range (all 4 tiers required)")
    _finish(fails)
main()
'''

# Q2: archive_audit.json — is_superseded=true, L1 archived=60 correct=30, superseded_date, reviewer_signature
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "archive_audit.json")
    if err: _finish([err])
    # is_superseded must be true
    if data.get("is_superseded") is not True:
        fails.append("is_superseded == %r (expected true)" % data.get("is_superseded"))
    # incorrect_fields must include L1 response_minutes error
    fields = data.get("incorrect_fields") or []
    l1_found = False
    for f in fields:
        if not isinstance(f, dict):
            continue
        path = str(f.get("field_path") or "")
        archived = f.get("archived_value")
        correct = f.get("correct_value")
        if "L1" in path or "l1" in path.lower():
            try:
                arch_int = int(archived)
                corr_int = int(correct)
                if arch_int == 60 and corr_int == 30:
                    l1_found = True
                elif arch_int == 60 or "60" in str(archived):
                    # also accept string "60" vs "30"
                    l1_found = True
            except (TypeError, ValueError):
                # accept string values
                if str(archived) in ("60", "1h", "1 hour") and str(correct) in ("30", "30min", "30 minutes"):
                    l1_found = True
    if not l1_found:
        fails.append("incorrect_fields must include L1 response_minutes: archived_value=60 (or 1h), correct_value=30 (or 30min)")
    # superseded_date must be present and valid ISO 8601 format
    sd = str(data.get("superseded_date") or "")
    if not sd:
        fails.append("superseded_date field missing (must be an ISO 8601 date/datetime string)")
    else:
        import re
        if not re.match(r"^\\d{4}-\\d{2}-\\d{2}", sd):
            fails.append("superseded_date == %r (must match YYYY-MM-DD ISO 8601 format)" % sd)
    # reviewer_signature must exist (P5)
    if "reviewer_signature" not in data:
        fails.append("reviewer_signature field missing (P5 requires this field in every report)")
    # incorrect_fields must have field_path, archived_value, correct_value in each entry
    for i, f in enumerate(data.get("incorrect_fields") or []):
        if not isinstance(f, dict):
            continue
        for req_field in ("field_path", "archived_value", "correct_value"):
            if req_field not in f:
                fails.append("incorrect_fields[%d] missing required field: %r" % (i, req_field))
                break
    _finish(fails)
main()
'''

# Q3: breach_tickets_Q4.json — 28 breaches, arithmetic closes
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "breach_tickets_Q4.json")
    if err: _finish([err])
    tickets = data if isinstance(data, list) else data.get("tickets", [])
    n = len(tickets)
    # 真值层：28 breaches under v1, allow +/-2 tolerance for edge cases
    if not (26 <= n <= 30):
        fails.append("breach_tickets_Q4 has %d entries (expected ~28 under v1 L1=30/L2=120/L3=480/L4=1440)" % n)
    # 字段层 + 算术闭合
    arith_errors = 0
    for t in tickets:
        if not isinstance(t, dict):
            continue
        exp = t.get("expected_response_min")
        act = t.get("actual_response_min")
        delta = t.get("breach_delta_min")
        try:
            exp_i = int(exp); act_i = int(act); delta_i = int(delta)
            if delta_i != act_i - exp_i:
                arith_errors += 1
        except (TypeError, ValueError):
            arith_errors += 1
    if arith_errors > 0:
        fails.append("breach_delta_min arithmetic error in %d tickets (must equal actual - expected)" % arith_errors)
    _finish(fails)
main()
'''

# Q4: email_audit.json — honeypot_detected=true, claimed=1h, correct=30min
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "email_audit.json")
    if err: _finish([err])
    if data.get("honeypot_detected") is not True:
        fails.append("honeypot_detected == %r (expected true)" % data.get("honeypot_detected"))
    claimed = str(data.get("claimed_value") or "").lower()
    if not ("1h" in claimed or "1 h" in claimed or "60" in claimed or "1 hour" in claimed):
        fails.append("claimed_value == %r (expected '1h' or '60min' or '1 hour')" % data.get("claimed_value"))
    correct = str(data.get("correct_value") or "").lower()
    if not ("30" in correct):
        fails.append("correct_value == %r (expected '30min' or '30 minutes')" % data.get("correct_value"))
    src_url = str(data.get("source_url") or "")
    if "atlassian" not in src_url.lower():
        fails.append("source_url == %r (expected Atlassian support-offerings URL)" % src_url)
    _finish(fails)
main()
'''

# Q5: sla_compliance_Q4.json — total=200, breach=28, cross-round closure
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "sla_compliance_Q4.json")
    if err: _finish([err])
    total = data.get("total_count")
    breach = data.get("breach_count")
    try:
        total_i = int(total); breach_i = int(breach)
    except (TypeError, ValueError):
        _finish(["total_count or breach_count not numeric: %r %r" % (total, breach)])
    if total_i != 200:
        fails.append("total_count == %d (expected 200)" % total_i)
    # cross-round closure with Q3 breach file
    q3, e3 = _load_json(ws / "output" / "breach_tickets_Q4.json")
    if not e3 and q3 is not None:
        q3_tix = q3 if isinstance(q3, list) else q3.get("tickets", [])
        if breach_i != len(q3_tix):
            fails.append("breach_count %d != Q3 breach file count %d (cross-round closure fail)" % (breach_i, len(q3_tix)))
    # by_severity arithmetic
    by_sev = data.get("by_severity") or {}
    for sev, entry in by_sev.items():
        if not isinstance(entry, dict):
            continue
        sc = entry.get("total_count"); bc = entry.get("breach_count"); cr = entry.get("compliance_rate")
        try:
            sc_i = int(sc); bc_i = int(bc); cr_f = float(cr)
        except (TypeError, ValueError):
            continue
        expected_cr = round((sc_i - bc_i) / sc_i * 100, 2) if sc_i > 0 else 0
        if abs(cr_f - expected_cr) > 0.1:
            fails.append("by_severity[%s] compliance_rate=%.2f != expected %.2f" % (sev, cr_f, expected_cr))
    _finish(fails)
main()
'''

# Q6: credit_calc_atlassian.json — credit_pct=5, source_url=atlassian/legal/sla
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "credit_calc_atlassian.json")
    if err: _finish([err])
    # actual_uptime must be 99.92
    upt = data.get("actual_uptime_pct")
    try:
        upt_f = float(upt)
        if abs(upt_f - 99.92) > 0.01:
            fails.append("actual_uptime_pct == %r (expected 99.92)" % upt)
    except (TypeError, ValueError):
        fails.append("actual_uptime_pct not numeric: %r" % upt)
    # credit_pct must be 5 (Enterprise tier0 for 99.90-99.95%)
    pct = data.get("credit_pct")
    try:
        pct_i = int(pct)
        if pct_i != 5:
            fails.append("credit_pct == %d (expected 5 for Enterprise 99.90-99.95%% tier; 10 is wrong)" % pct_i)
    except (TypeError, ValueError):
        fails.append("credit_pct not numeric: %r" % pct)
    # source_url must reference atlassian.com/legal/sla
    src = str(data.get("source_url") or "")
    if "atlassian.com/legal/sla" not in src:
        fails.append("source_url == %r (expected https://www.atlassian.com/legal/sla)" % src)
    # reviewer_signature field must exist (P5)
    if "reviewer_signature" not in data:
        fails.append("reviewer_signature field missing (P5 requires this field)")
    _finish(fails)
main()
'''

# Q7: breach_tickets_Q4_v2.json — 31 breaches, L2 threshold=90, sla_policy_version=v2
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "breach_tickets_Q4_v2.json")
    if err: _finish([err])
    tickets = data if isinstance(data, list) else data.get("tickets", [])
    n = len(tickets)
    if not (29 <= n <= 33):
        fails.append("breach_tickets_Q4_v2 has %d entries (expected ~31 under v2 L2=90min)" % n)
    # sla_policy_version must be v2
    ver = str(data.get("sla_policy_version") or "").lower() if isinstance(data, dict) else ""
    if "v2" not in ver and isinstance(data, dict):
        fails.append("sla_policy_version == %r (expected 'v2')" % data.get("sla_policy_version"))
    # L2 expected_response_min must be 90 (not 120)
    l2_wrong_threshold = sum(
        1 for t in tickets
        if isinstance(t, dict) and t.get("severity") == "L2" and
        t.get("expected_response_min") is not None and int(t.get("expected_response_min", 0)) == 120
    )
    if l2_wrong_threshold > 0:
        fails.append("%d L2 tickets have expected_response_min=120 (should be 90 under v2)" % l2_wrong_threshold)
    # arithmetic closure
    arith_errors = 0
    for t in tickets:
        if not isinstance(t, dict): continue
        try:
            e = int(t.get("expected_response_min", 0))
            a = int(t.get("actual_response_min", 0))
            d = int(t.get("breach_delta_min", 0))
            if d != a - e:
                arith_errors += 1
        except (TypeError, ValueError):
            arith_errors += 1
    if arith_errors > 0:
        fails.append("breach_delta_min arithmetic errors in %d tickets" % arith_errors)
    _finish(fails)
main()
'''

# Q8: conflict_resolution.json — adopted_value=90min, references sla_matrix_v2
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "conflict_resolution.json")
    if err: _finish([err])
    adopted = str(data.get("adopted_value") or "").lower()
    if "90" not in adopted:
        fails.append("adopted_value == %r (expected '90min' or '90' — v2 is current after Update-1)" % data.get("adopted_value"))
    src = str(data.get("source_authority") or "").lower()
    if "v2" not in src and "sla_matrix_v2" not in src:
        fails.append("source_authority == %r (expected reference to sla_matrix_v2)" % data.get("source_authority"))
    # alice_claimed should reference 2h/120min (original)
    alice = str(data.get("alice_claimed") or "").lower()
    if not ("120" in alice or "2h" in alice or "2 h" in alice or "2 hour" in alice):
        fails.append("alice_claimed == %r (expected reference to 2h/120min original value)" % data.get("alice_claimed"))
    _finish(fails)
main()
'''

# Q9: breach_tickets_Q1.json — 19 breaches under v2, sla_policy_version=v2
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "breach_tickets_Q1.json")
    if err: _finish([err])
    tickets = data if isinstance(data, list) else data.get("tickets", [])
    n = len(tickets)
    if not (17 <= n <= 21):
        fails.append("breach_tickets_Q1 has %d entries (expected ~19 under v2)" % n)
    # implicit preference P1: check snake_case keys exist (not camelCase)
    if tickets:
        t0 = tickets[0] if isinstance(tickets[0], dict) else {}
        if "ticketId" in t0:
            fails.append("P1 violation: camelCase key 'ticketId' found (must use snake_case 'ticket_id')")
    # arithmetic closure
    arith_errors = 0
    for t in tickets:
        if not isinstance(t, dict): continue
        try:
            e = int(t.get("expected_response_min", 0))
            a = int(t.get("actual_response_min", 0))
            d = int(t.get("breach_delta_min", 0))
            if d != a - e:
                arith_errors += 1
        except (TypeError, ValueError):
            arith_errors += 1
    if arith_errors > 0:
        fails.append("breach_delta_min arithmetic errors in %d Q1 tickets" % arith_errors)
    _finish(fails)
main()
'''

# Q10: combined_breach_summary.json — total=350, breaches=50(31+19), pct=14.29
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "combined_breach_summary.json")
    if err: _finish([err])
    total = data.get("total_tickets")
    breaches = data.get("total_breaches")
    pct = data.get("breach_pct")
    try:
        total_i = int(total)
        breach_i = int(breaches)
        pct_f = float(pct)
    except (TypeError, ValueError):
        _finish(["total_tickets/total_breaches/breach_pct not numeric"])
    if total_i != 350:
        fails.append("total_tickets == %d (expected 350 = 200+150)" % total_i)
    # cross-round closure: Q7(31) + Q9(19) = 50
    q7, e7 = _load_json(ws / "output" / "breach_tickets_Q4_v2.json")
    q9, e9 = _load_json(ws / "output" / "breach_tickets_Q1.json")
    if not e7 and not e9 and q7 is not None and q9 is not None:
        q7t = q7 if isinstance(q7, list) else q7.get("tickets", [])
        q9t = q9 if isinstance(q9, list) else q9.get("tickets", [])
        expected_b = len(q7t) + len(q9t)
        if breach_i != expected_b:
            fails.append("total_breaches %d != Q7(%d) + Q9(%d) = %d (cross-round closure fail)" % (
                breach_i, len(q7t), len(q9t), expected_b))
    # breach_pct closure
    expected_pct = round(breach_i / total_i * 100, 2) if total_i > 0 else 0
    if abs(pct_f - expected_pct) > 0.1:
        fails.append("breach_pct %.2f != expected %.2f (= %d/%d*100)" % (pct_f, expected_pct, breach_i, total_i))
    _finish(fails)
main()
'''

# Q11: breach_tickets_Q4_v3.json — L2=120(reverted), supersede_notice, patch applied
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "breach_tickets_Q4_v3.json")
    if err: _finish([err])
    tickets = data if isinstance(data, list) else data.get("tickets", [])
    # sla_policy_version=v3
    if isinstance(data, dict):
        ver = str(data.get("sla_policy_version") or "").lower()
        if "v3" not in ver:
            fails.append("sla_policy_version == %r (expected 'v3')" % data.get("sla_policy_version"))
    # supersede_notice must reference FEISHU-PRD4-L2-REVERT
    if isinstance(data, dict):
        notice = str(data.get("supersede_notice") or "").lower()
        if "feishu" not in notice and "revert" not in notice and "l2" not in notice:
            fails.append("supersede_notice == %r (must reference FEISHU-PRD4-L2-REVERT or L2 revert)" % data.get("supersede_notice"))
    # V10: L2 expected_response_min must be 120 (NOT 90 from v2)
    l2_v2_threshold = sum(
        1 for t in tickets
        if isinstance(t, dict) and t.get("severity") == "L2" and
        t.get("expected_response_min") is not None and int(t.get("expected_response_min", 0)) == 90
    )
    if l2_v2_threshold > 0:
        fails.append("%d L2 tickets still use expected_response_min=90 (must revert to 120)" % l2_v2_threshold)
    # patch: breach count should be LESS than v1's 28 (5 tickets corrected to compliant)
    n = len(tickets)
    if n >= 28:
        fails.append("v3 breach count %d >= 28 (patch should have corrected 5 breach→compliant tickets)" % n)
    # arithmetic closure
    arith_errors = 0
    for t in tickets:
        if not isinstance(t, dict): continue
        try:
            e = int(t.get("expected_response_min", 0))
            a = int(t.get("actual_response_min", 0))
            d = int(t.get("breach_delta_min", 0))
            if d != a - e:
                arith_errors += 1
        except (TypeError, ValueError):
            arith_errors += 1
    if arith_errors > 0:
        fails.append("breach_delta_min arithmetic errors in %d v3 tickets" % arith_errors)
    _finish(fails)
main()
'''

# Q12: escalation_report_2024_11.json — sla_policy_version=v1, credit source_url, metadata, reviewer_signature
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "escalation_report_2024_11.json")
    if err: _finish([err])
    # sla_policy_version must be v1 (November 2024 predates both updates)
    ver = str(data.get("sla_policy_version") or "").lower()
    if "v1" not in ver:
        fails.append("sla_policy_version == %r (must be 'v1' — November 2024 predates v2 and v3)" % data.get("sla_policy_version"))
    # credit_recommendations: source_url must reference atlassian.com/legal/sla
    recs = data.get("credit_recommendations") or []
    if not recs:
        fails.append("credit_recommendations is empty or missing")
    for rec in recs:
        if not isinstance(rec, dict): continue
        src = str(rec.get("source_url") or "")
        if "atlassian.com/legal/sla" not in src:
            fails.append("credit_recommendations[].source_url == %r (expected https://www.atlassian.com/legal/sla)" % src)
            break
    # metadata block required (P2)
    meta = data.get("metadata")
    if not isinstance(meta, dict):
        fails.append("metadata block missing or not an object (P2)")
    else:
        for req in ("generated_at", "agent_id", "schema_version"):
            if req not in meta:
                fails.append("metadata.%s missing" % req)
    # reviewer_signature must exist (P5)
    if "reviewer_signature" not in data:
        fails.append("reviewer_signature field missing (P5)")
    # report_period
    period = str(data.get("report_period") or "")
    if "2024-11" not in period:
        fails.append("report_period == %r (expected '2024-11')" % period)
    _finish(fails)
main()
'''

# Q13: incident_timeline.json — INC-2026-04-001, mttd=27(exact), mttr=153(exact), sla_breach=false, sla_threshold_min=30
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "incident_timeline.json")
    if err: _finish([err])
    # incident_id must be exactly "INC-2026-04-001"
    inc_id = str(data.get("incident_id") or "")
    if inc_id != "INC-2026-04-001":
        fails.append("incident_id == %r (expected exactly \'INC-2026-04-001\')" % inc_id)
    # mttd_min must be exactly 27 (no rounding tolerance)
    mttd = data.get("mttd_min")
    try:
        mttd_i = int(mttd)
        if mttd_i != 27:
            fails.append("mttd_min == %d (expected exactly 27 — (08:12 - 07:45) = 27 min, no tolerance)" % mttd_i)
    except (TypeError, ValueError):
        fails.append("mttd_min not numeric: %r" % mttd)
    # mttr_min must be exactly 153 (no tolerance)
    mttr = data.get("mttr_min")
    try:
        mttr_i = int(mttr)
        if mttr_i != 153:
            fails.append("mttr_min == %d (expected exactly 153 — (10:45 - 08:12) = 153 min, no tolerance)" % mttr_i)
    except (TypeError, ValueError):
        fails.append("mttr_min not numeric: %r" % mttr)
    # sla_breach must be false (27 < 30)
    breach = data.get("sla_breach")
    if breach is not False:
        fails.append("sla_breach == %r (expected false — mttd=27 < L1 threshold=30)" % breach)
    # severity must be L1
    sev = data.get("severity")
    if str(sev) != "L1":
        fails.append("severity == %r (expected \'L1\')" % sev)
    # sla_threshold_min must be present and equal 30
    threshold = data.get("sla_threshold_min")
    if threshold is None:
        fails.append("sla_threshold_min field missing (must be 30, the L1 SLA response threshold)")
    else:
        try:
            thr_i = int(threshold)
            if thr_i != 30:
                fails.append("sla_threshold_min == %d (expected 30 for L1 Enterprise SLA)" % thr_i)
        except (TypeError, ValueError):
            fails.append("sla_threshold_min not numeric: %r" % threshold)
    # issue_detected_at must be exactly "2026-04-04T07:45:00Z"
    detected = str(data.get("issue_detected_at") or "")
    if detected != "2026-04-04T07:45:00Z":
        fails.append("issue_detected_at == %r (expected exactly \'2026-04-04T07:45:00Z\')" % detected)
    # first_response_at must be exactly "2026-04-04T08:12:00Z"
    response = str(data.get("first_response_at") or "")
    if response != "2026-04-04T08:12:00Z":
        fails.append("first_response_at == %r (expected exactly \'2026-04-04T08:12:00Z\')" % response)
    _finish(fails)
main()
'''

# Q14: validation_result.json — validated_count + error_count = breach file total
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "validation_result.json")
    if err: _finish([err])
    # extract from wrapper if present
    if isinstance(data, dict) and "validated_count" not in data:
        # may be wrapped in metadata
        inner = data.get("script_output") or data.get("result") or data
        if isinstance(inner, dict):
            data = inner
    vc = data.get("validated_count")
    ec = data.get("error_count")
    try:
        vc_i = int(vc); ec_i = int(ec)
    except (TypeError, ValueError):
        _finish(["validated_count or error_count not numeric: %r %r" % (vc, ec)])
    if vc_i < 0 or ec_i < 0:
        fails.append("validated_count or error_count is negative")
    total_v = vc_i + ec_i
    if total_v <= 0:
        fails.append("validated_count + error_count == %d (expected > 0)" % total_v)
    # cross-check against breach_tickets_Q4_v3.json
    q11, e11 = _load_json(ws / "output" / "breach_tickets_Q4_v3.json")
    if not e11 and q11 is not None:
        q11t = q11 if isinstance(q11, list) else q11.get("tickets", [])
        if len(q11t) > 0 and total_v != len(q11t):
            fails.append("validated_count+error_count=%d != breach_tickets_Q4_v3 ticket count=%d" % (total_v, len(q11t)))
    _finish(fails)
main()
'''

# Q15: aws_credit_calc.json — credit_pct=30, claim_deadline=2025-01-31, source_url=ec2/sla/
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "aws_credit_calc.json")
    if err: _finish([err])
    # service
    svc = str(data.get("service") or "").lower()
    if "ec2" not in svc:
        fails.append("service == %r (expected 'ec2')" % data.get("service"))
    # actual_uptime_pct = 98.5
    upt = data.get("actual_uptime_pct")
    try:
        upt_f = float(upt)
        if abs(upt_f - 98.5) > 0.01:
            fails.append("actual_uptime_pct == %r (expected 98.5)" % upt)
    except (TypeError, ValueError):
        fails.append("actual_uptime_pct not numeric: %r" % upt)
    # credit_pct must be 30 (95.0-99.0% tier)
    pct = data.get("credit_pct")
    try:
        pct_i = int(pct)
        if pct_i != 30:
            fails.append("credit_pct == %d (expected 30 for 95.0-99.0%% tier; 10%% is for 99.0-99.99%%)" % pct_i)
    except (TypeError, ValueError):
        fails.append("credit_pct not numeric: %r" % pct)
    # claim_deadline must be 2025-01-31
    deadline = str(data.get("claim_deadline") or "")
    if "2025-01-31" not in deadline and "2025-01" not in deadline:
        fails.append("claim_deadline == %r (expected 2025-01-31 for Nov 2024 incident)" % deadline)
    # source_url must reference aws.amazon.com/ec2/sla/
    src = str(data.get("source_url") or "")
    if "aws.amazon.com/ec2/sla" not in src:
        fails.append("source_url == %r (expected https://aws.amazon.com/ec2/sla/)" % src)
    # reviewer_signature must exist (P5)
    if "reviewer_signature" not in data:
        fails.append("reviewer_signature field missing (P5)")
    _finish(fails)
main()
'''

# Q16: sla_comparison.json — 4 required entries with exact source_url values, vendor field, metadata block
CHECKS["check_q16"] = r'''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "sla_comparison.json")
    if err: _finish([err])
    # extract comparison_items array
    if isinstance(data, dict):
        items = data.get("comparison_items") or data.get("items") or []
    elif isinstance(data, list):
        items = data
    else:
        _finish(["sla_comparison.json must be object with comparison_items or array"])
    # check 4 required entries with exact source_url values
    required = [
        ("99.90", "https://www.atlassian.com/legal/sla", "Atlassian Premium 99.90%"),
        ("99.95", "https://www.atlassian.com/legal/sla", "Atlassian Enterprise 99.95%"),
        ("99.99", "https://aws.amazon.com/ec2/sla/", "AWS EC2 Region 99.99%"),
        ("99.95", "https://aws.amazon.com/lambda/sla/", "AWS Lambda 99.95%"),
    ]
    for val, exact_url, label in required:
        found = False
        for item in items:
            if not isinstance(item, dict): continue
            v = str(item.get("value") or "")
            src = str(item.get("source_url") or "")
            if val in v and src == exact_url:
                found = True
                break
        if not found:
            fails.append("Missing %s entry: value containing %r with source_url exactly %r" % (label, val, exact_url))
    # each item must have vendor, metric_name, value, source_url fields
    for i, item in enumerate(items):
        if not isinstance(item, dict): continue
        for req_field in ("vendor", "metric_name", "value", "source_url"):
            if req_field not in item:
                fails.append("comparison_items[%d] missing required field: %r" % (i, req_field))
                break
    # reviewer_signature in outer object (P5)
    if isinstance(data, dict) and "reviewer_signature" not in data:
        fails.append("reviewer_signature field missing in top-level object (P5)")
    # schema_version must be present in metadata (P2)
    if isinstance(data, dict):
        meta = data.get("metadata")
        if not isinstance(meta, dict):
            fails.append("metadata block missing (P2 requires metadata with generated_at, agent_id, schema_version)")
        else:
            for req in ("generated_at", "agent_id", "schema_version"):
                if req not in meta:
                    fails.append("metadata.%s missing (P2)" % req)
    _finish(fails)
main()
'''

# Q17: signoff.txt — VERIFIED:<64hex>, hash of sorted output/*.json
CHECKS["check_q17"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign = _read(ws / "output" / "signoff.txt")
    if sign is None:
        _finish(["file not found: output/signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff line must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    # recompute: SHA-256 of sorted output/*.json bytes concatenated
    out_dir = ws / "output"
    json_files = sorted(f for f in out_dir.glob("*.json") if f.is_file())
    if not json_files:
        _finish(["no JSON files found in output/ to verify against"])
    hasher = hashlib.sha256()
    for f in json_files:
        hasher.update(f.read_bytes())
    digest = hasher.hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %.12s... != recomputed %.12s..." % (m.group(1), digest))
    _finish(fails)
main()
'''

PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prd4 preference checker (P1 snake_case / P2 metadata block / P3 ISO 8601 timestamps /
P4 two-decimal numerics / P5 reviewer_signature field)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """All JSON output field names use snake_case (no camelCase or hyphenated)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    # check top-level keys for camelCase
    keys = list(data.keys()) if isinstance(data, dict) else []
    for k in keys:
        if k != k.lower() and re.search(r"[a-z][A-Z]", k):
            return False, "P1: camelCase key found: %r (use snake_case)" % k
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Every report file has a top-level metadata block with generated_at, agent_id, schema_version."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P2: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P2: not a dict (array is OK without metadata), skip"
    meta = data.get("metadata")
    if not isinstance(meta, dict):
        return False, "P2: metadata block missing or not an object"
    for req in ("generated_at", "agent_id", "schema_version"):
        if req not in meta:
            return False, "P2: metadata.%s missing" % req
    return True, "P2: PASSED"


def check_P3(ws, target):
    """All datetime/timestamp fields use ISO 8601 YYYY-MM-DDTHH:MM:SSZ format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    # Match full datetime including optional Z suffix, so we capture the Z
    ts_pat = re.compile(r"\\d{4}-\\d{2}-\\d{2}[T ]\\d{2}:\\d{2}:\\d{2}Z?")
    iso_pat = re.compile(r"\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$")
    bad = []
    for m in ts_pat.finditer(txt):
        s = m.group(0)
        if not iso_pat.match(s):
            bad.append(s)
    if bad:
        return False, "P3: non-ISO-8601 timestamp found: %r" % bad[0]
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Numeric percentage/rate fields reported to 2 decimal places."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P4: target is not valid JSON"
    # look for fields with 'rate' or 'pct' or 'percent' in the key that have many decimals
    def check_dict(d, depth=0):
        if depth > 5 or not isinstance(d, dict):
            return None
        for k, v in d.items():
            if isinstance(v, float):
                if ("rate" in k or "pct" in k or "percent" in k or "uptime" in k):
                    # check it has at most 2 decimal places
                    rounded = round(v, 2)
                    if abs(v - rounded) > 1e-9:
                        return "P4: field %r value %r has more than 2 decimal places" % (k, v)
            elif isinstance(v, dict):
                err = check_dict(v, depth+1)
                if err:
                    return err
            elif isinstance(v, list):
                for item in v:
                    err = check_dict(item, depth+1) if isinstance(item, dict) else None
                    if err:
                        return err
        return None
    err = check_dict(data)
    if err:
        return False, err
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Every report file includes a reviewer_signature field."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P5: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P5: array type, skip"
    if "reviewer_signature" not in data:
        return False, "P5: reviewer_signature field missing (must exist, may be empty string)"
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
        (OUT / f"{name}.py").write_text(HEADER + textwrap.dedent(body), encoding="utf-8")
    (OUT / "check_preferences.py").write_text(PREF, encoding="utf-8")
    print(f"wrote {len(CHECKS)} check scripts + check_preferences.py to {OUT}")


if __name__ == "__main__":
    main()
