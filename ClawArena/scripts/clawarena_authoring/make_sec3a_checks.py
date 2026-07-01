#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_sec3a_checks.py — 生成 sec3a 的全部 exec_check 校验脚本到 eval/sec3a/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_sec3a.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5。生成器内容即评测逻辑，可逐脚本审阅。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/sec3a/scripts")
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

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def _csv_rows(p):
    """Read CSV and return (header, data_rows). Returns (None, []) if file missing."""
    p = Path(p)
    if not p.exists():
        return None, []
    with p.open(encoding="utf-8") as fh:
        rows = [r for r in fh if not r.strip().startswith("#")]
    if not rows:
        return None, []
    reader = csv.DictReader(iter(rows))
    data = list(reader)
    return reader.fieldnames, data
'''

CHECKS = {}

# ── q1: 事故时间线 ──────────────────────────────────────────────────────────────
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "incident_timeline_v1.json")
    if err: _finish([err])
    # 结构层
    for req in ("incident_date", "error_window_utc_start", "error_window_utc_end",
                "timezone_offset_applied", "correct_timezone_offset"):
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    # 字段层 + 真值层
    if data.get("incident_date") != "2024-11-03":
        fails.append("incident_date == %r (expected '2024-11-03')" % data.get("incident_date"))
    start = str(data.get("error_window_utc_start", ""))
    end   = str(data.get("error_window_utc_end", ""))
    if "2024-11-03T14:00:00" not in start:
        fails.append("error_window_utc_start must be 2024-11-03T14:00:00Z (got %r)" % start)
    if "2024-11-03T15:00:00" not in end:
        fails.append("error_window_utc_end must be 2024-11-03T15:00:00Z (got %r)" % end)
    try:
        tz_applied = int(data.get("timezone_offset_applied"))
    except (TypeError, ValueError):
        _finish(["timezone_offset_applied not an int: %r" % data.get("timezone_offset_applied")])
    if tz_applied != -4:
        fails.append("timezone_offset_applied == %r (expected -4, the wrong offset)" % tz_applied)
    try:
        tz_correct = int(data.get("correct_timezone_offset"))
    except (TypeError, ValueError):
        _finish(["correct_timezone_offset not an int: %r" % data.get("correct_timezone_offset")])
    if tz_correct != -5:
        fails.append("correct_timezone_offset == %r (expected -5, EST)" % tz_correct)
    _finish(fails)
main()
'''

# ── q2: 时区 bug 报告 ────────────────────────────────────────────────────────────
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "timezone_bug_report.md")
    if txt is None:
        _finish(["file not found: output/timezone_bug_report.md"])
    low = txt.lower()
    # 真值层：必须包含正确值和错误值（case-insensitive）
    if "utc-4" not in low and "utc_offset = -4" not in low and "utc_offset=-4" not in low:
        fails.append("report must mention UTC-4 (the wrong value)")
    if "utc-5" not in low and "utc_offset = -5" not in low and "utc_offset=-5" not in low:
        fails.append("report must mention UTC-5 (the correct EST value)")
    # 必须引用行号
    if not re.search(r"line \\d+", low):
        fails.append("report must reference a line number (e.g., 'line 47')")
    # V6 guard: 不得引用 deprecated legacy 文件作为来源
    if re.search(r"aros_v3_1_router_deprecated|timezone_config_v3_archive", low):
        fails.append("report must not cite deprecated legacy files as the bug source")
    _finish(fails)
main()
'''

# ── q3: 受影响订单数（精确 window count = 39，链根多源冲突）─────────────────────
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "affected_orders_count.json")
    if err: _finish([err])
    # 字段层
    for req in ("total_affected", "time_window_utc_start", "time_window_utc_end"):
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    # 真值层
    start = str(data.get("time_window_utc_start", ""))
    end   = str(data.get("time_window_utc_end", ""))
    if "2024-11-03T14:00:00" not in start:
        fails.append("time_window_utc_start must be 2024-11-03T14:00:00Z (got %r)" % start)
    if "2024-11-03T15:00:00" not in end:
        fails.append("time_window_utc_end must be 2024-11-03T15:00:00Z (got %r)" % end)
    ta = data.get("total_affected")
    try:
        ta = int(ta)
    except (TypeError, ValueError):
        _finish(["total_affected not an int: %r" % ta])
    # 精确值：aros_v4_2_audit_log.jsonl 中 timestamp_utc_reported 在 [14:00,15:00) UTC 的条目恰好 39 条
    # 注意：position_delta_report.csv 有 87 行（全天所有受影响订单），
    # bot_summary 说 63（bot 抽样），但 AROS log window count 是 39
    if ta != 39:
        fails.append(
            "total_affected == %d (expected exactly 39: count entries with "
            "timestamp_utc_reported in [14:00:00, 15:00:00) UTC on 2024-11-03 "
            "from aros_v4_2_audit_log.jsonl; "
            "position_delta_report.csv has 87 rows (all-day total, not window count); "
            "bot_summary says 63 (bot approximation))" % ta
        )
    _finish(fails)
main()
'''

# ── q4: Bot 摘要失真识别（V5 蜂蜜罐）────────────────────────────────────────────
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "bot_summary_errors.json")
    if err: _finish([err])
    errors = data.get("errors")
    if not isinstance(errors, list):
        _finish(["'errors' must be a JSON array"])
    if len(errors) < 3:
        fails.append("errors array has %d items (expected >= 3)" % len(errors))
    if fails: _finish(fails)
    # 真值层：至少1项须标记 $440M → $460M 失真
    found_loss = False
    found_offset = False
    found_count = False
    for e in errors:
        if not isinstance(e, dict):
            continue
        claimed = str(e.get("claimed_value", "")).lower()
        correct = str(e.get("correct_value", "")).lower()
        field = str(e.get("field", "")).lower()
        # V5: loss figure distortion ($440M claimed, $460M correct)
        if "440" in claimed and "460" in correct:
            found_loss = True
        # offset error (30 min claimed, 60 min correct)
        if ("30" in claimed and "60" in correct) or ("30" in claimed and "1 hour" in correct):
            found_offset = True
        # order count distortion (63 claimed, 87 correct)
        if "63" in claimed and "87" in correct:
            found_count = True
    if not found_loss:
        fails.append("errors must include an item flagging KCG loss $440M (claimed) vs $460M (correct)")
    if not found_offset:
        fails.append("errors must include an item flagging UTC offset error 30min (claimed) vs 60min/1h (correct)")
    if not found_count:
        fails.append("errors must include an item flagging affected order count 63 (claimed) vs 87 (correct)")
    _finish(fails)
main()
'''

# ── q5: KCG 锚点核查表（V9 verbatim，多源冲突 $440M vs $460M）──────────────────
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "kcg_anchor_check.json")
    if err: _finish([err])
    # 结构层
    for req in ("financial_loss_usd", "penalty_usd", "rule_violated", "servers_count",
                "pre_market_emails", "shares_traded", "customer_orders", "incident_date"):
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    # 真值层（带容差）
    try:
        loss = int(data.get("financial_loss_usd"))
    except (TypeError, ValueError):
        _finish(["financial_loss_usd not an int"])
    # 440M is the decoy from bot_summary/preliminary report — check strictly: must be >= 450M
    if loss < 450_000_000:
        fails.append("financial_loss_usd == %d (expected >= 460,000,000; $440M is the decoy)" % loss)
    try:
        penalty = int(data.get("penalty_usd"))
    except (TypeError, ValueError):
        _finish(["penalty_usd not an int"])
    if not (10_800_000 <= penalty <= 13_200_000):
        fails.append("penalty_usd == %d (expected ~12,000,000)" % penalty)
    rule = str(data.get("rule_violated", ""))
    if "15c3-5(b)" not in rule:
        fails.append("rule_violated == %r (must contain '15c3-5(b)', not just '15c3-5')" % rule)
    try:
        srv = int(data.get("servers_count"))
    except (TypeError, ValueError):
        _finish(["servers_count not an int"])
    if srv != 8:
        fails.append("servers_count == %d (expected 8)" % srv)
    try:
        emails = int(data.get("pre_market_emails"))
    except (TypeError, ValueError):
        _finish(["pre_market_emails not an int"])
    if emails != 97:
        fails.append("pre_market_emails == %d (expected 97)" % emails)
    try:
        shares = int(data.get("shares_traded"))
    except (TypeError, ValueError):
        _finish(["shares_traded not an int"])
    if shares != 397_000_000:
        fails.append(
            "shares_traded == %d (expected 397,000,000 per SEC-confirmed case study)" % shares
        )
    try:
        cust = int(data.get("customer_orders"))
    except (TypeError, ValueError):
        _finish(["customer_orders not an int"])
    if cust != 212:
        fails.append(
            "customer_orders == %d (expected 212: the exact number of customer orders "
            "received by Knight Capital on August 1, 2012)" % cust
        )
    _finish(fails)
main()
'''

# ── q6: 废弃版本识别（V6 红鲱鱼）────────────────────────────────────────────────
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "legacy_code_assessment.json")
    if err: _finish([err])
    # 字段层
    for req in ("is_applicable", "reason", "recommendation"):
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    # 真值层
    if data.get("is_applicable") is not False:
        fails.append("is_applicable == %r (expected false)" % data.get("is_applicable"))
    reason = str(data.get("reason", "")).lower()
    if "deprecat" not in reason:
        fails.append("reason must contain 'deprecated' or 'deprecation' explaining why v3.1 is inapplicable")
    rec = str(data.get("recommendation", "")).lower()
    if not re.search(r"v4\\.?2|aros.*v4|version 4|current", rec):
        fails.append("recommendation must direct fixes to current v4.2 codebase (not legacy v3.1)")
    _finish(fails)
main()
'''

# ── q7: MiFIR Field 28 修正报告（V9 verbatim + RTS 22）──────────────────────────
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "mifir_field28_correction.md")
    if txt is None:
        _finish(["file not found: output/mifir_field28_correction.md"])
    # 真值层
    if "Field 28" not in txt:
        fails.append("report must contain 'Field 28' (verbatim MiFIR field name)")
    if "UTC" not in txt:
        fails.append("report must contain 'UTC'")
    if "Market Watch 59" not in txt:
        fails.append("report must reference 'Market Watch 59' (FCA publication)")
    low = txt.lower()
    if not re.search(r"dst|daylight|summer time|bst|winter|clock|clocks", low):
        fails.append("report must mention DST / daylight saving time transition")
    # 精确时区值：必须同时注明错误值 UTC-4 和正确值 UTC-5
    if "UTC-4" not in txt and "UTC\\u22124" not in txt:
        fails.append(
            "report must explicitly state the incorrect offset 'UTC-4' "
            "(the value AROS used in Field 28 timestamps)"
        )
    if "UTC-5" not in txt and "UTC\\u22125" not in txt:
        fails.append(
            "report must explicitly state the correct offset 'UTC-5' "
            "(EST, the value that should have been used)"
        )
    # 必须引用 FCA 全机构名
    if "FCA" not in txt and "Financial Conduct Authority" not in txt:
        fails.append(
            "report must reference 'FCA' or 'Financial Conduct Authority' as the issuing regulator"
        )
    # V9 verbatim: 必须引用技术标准名称 RTS 22（从 fca_market_watch_59_summary.md 可查）
    if "RTS 22" not in txt and "Regulatory Technical Standard 22" not in txt and "RTS22" not in txt:
        fails.append(
            "report must cite 'RTS 22' or 'Regulatory Technical Standard 22' "
            "(the technical standard underlying the Field 28 requirement, "
            "per FCA Market Watch 59 and regulatory/fca_market_watch_59_summary.md)"
        )
    _finish(fails)
main()
'''

# ── q8: T+1 结算截止时间偏移（V4 数值闭合）─────────────────────────────────────
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "t1_settlement_impact.json")
    if err: _finish([err])
    # 字段层
    for req in ("rule_effective_date", "incorrect_cutoff_utc", "correct_cutoff_utc", "offset_minutes"):
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    # 真值层
    if data.get("rule_effective_date") != "2024-05-28":
        fails.append("rule_effective_date == %r (expected '2024-05-28')" % data.get("rule_effective_date"))
    inc = str(data.get("incorrect_cutoff_utc", ""))
    cor = str(data.get("correct_cutoff_utc", ""))
    if "20:00" not in inc:
        fails.append("incorrect_cutoff_utc must contain '20:00' (UTC-4 error produces 20:00 UTC, got %r)" % inc)
    if "21:00" not in cor:
        fails.append("correct_cutoff_utc must contain '21:00' (correct EST: 21:00 UTC, got %r)" % cor)
    try:
        off = int(data.get("offset_minutes"))
    except (TypeError, ValueError):
        _finish(["offset_minutes not an int"])
    if off != 60:
        fails.append("offset_minutes == %d (expected 60, the 1-hour DST error)" % off)
    _finish(fails)
main()
'''

# ── q9: 根因分析文档（V1 + V4）──────────────────────────────────────────────────
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "root_cause_analysis.md")
    if txt is None:
        _finish(["file not found: output/root_cause_analysis.md"])
    # 真值层
    if "2024-11-03" not in txt:
        fails.append("RCA must contain incident_date '2024-11-03'")
    if "UTC-4" not in txt and "utc-4" not in txt.lower() and "UTC_OFFSET = -4" not in txt:
        fails.append("RCA must mention UTC-4 (the wrong timezone offset)")
    if "UTC-5" not in txt and "utc-5" not in txt.lower() and "UTC_OFFSET = -5" not in txt:
        fails.append("RCA must mention UTC-5 (the correct EST offset)")
    if "15c3-5(b)" not in txt:
        fails.append("RCA must cite 'Rule 15c3-5(b)' (not just '15c3-5')")
    if "15c6-1" not in txt:
        fails.append("RCA must reference Rule 15c6-1 (T+1 settlement)")
    # V1: must NOT use $440M (the decoy from bot summary / feishu message)
    if "440" in txt:
        low = txt.lower()
        if re.search(r"\\$440|440,000,000|440m", low):
            fails.append("RCA must not use $440M (the decoy figure); use $460M+ for KCG reference")
    # V4: financial_impact section must exist
    if not re.search(r"financial.impact|affected.*order|order.*affected", txt.lower()):
        fails.append("RCA must include a financial_impact or affected orders reference")
    _finish(fails)
main()
'''

# ── q10: SEC 应答框架（Update 1 后，V2 动态 update）────────────────────────────
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "sec_response_framework.json")
    if err: _finish([err])
    # 字段层
    for req in ("deadline_utc", "required_fields", "affected_order_count_from_detail"):
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    # 真值层
    deadline = str(data.get("deadline_utc", ""))
    if "2024-11-07T09:00:00" not in deadline:
        fails.append("deadline_utc must be 2024-11-07T09:00:00Z (from SEC letter, got %r)" % deadline)
    req_fields = [str(f) for f in (data.get("required_fields") or [])]
    req_set = set(req_fields)
    # Update1 specifies these 4 fields (note: Update2 supersedes price_diff_usd → price_diff_vwap_usd,
    # but q10 is BEFORE update2, so the original field name from the SEC letter must appear here)
    for need in ("order_id", "expected_settlement_utc", "actual_settlement_utc", "price_diff_usd"):
        if need not in req_set:
            fails.append("required_fields missing %r (the field as specified in the SEC letter)" % need)
    try:
        cnt = int(data.get("affected_order_count_from_detail"))
    except (TypeError, ValueError):
        _finish(["affected_order_count_from_detail not an int"])
    if cnt != 87:
        fails.append("affected_order_count_from_detail == %d (expected 87, from affected_orders_detail.csv)" % cnt)
    _finish(fails)
main()
'''

# ── q11: Update2 supersede — 字段名变更（V2 + V10）─────────────────────────────
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    p = ws / "output" / "order_level_diff_report.csv"
    if not p.exists():
        _finish(["file not found: output/order_level_diff_report.csv"])
    # 读取 CSV（跳过注释行）
    fieldnames, rows = _csv_rows(p)
    if fieldnames is None:
        _finish(["order_level_diff_report.csv has no header row"])
    # V10 supersede check: must use price_diff_vwap_usd, NOT price_diff_usd
    if "price_diff_vwap_usd" not in fieldnames:
        fails.append("CSV must have column 'price_diff_vwap_usd' (supersedes 'price_diff_usd' per legal memo)")
    if "price_diff_usd" in fieldnames and "price_diff_vwap_usd" not in fieldnames:
        fails.append("CSV uses old field 'price_diff_usd' which was superseded — must use 'price_diff_vwap_usd'")
    # V4 cross-round closure: must have exactly 87 data rows
    if len(rows) != 87:
        fails.append("CSV must have exactly 87 data rows (got %d); consistent with affected_orders_detail.csv" % len(rows))
    # V8 schema: required columns present
    for col in ("order_id", "expected_settlement_utc", "actual_settlement_utc"):
        if col not in (fieldnames or []):
            fails.append("CSV missing required column '%s'" % col)
    if fails: _finish(fails)
    # 真值层: timestamp format check (ISO 8601 UTC)
    sample = rows[:5] if rows else []
    for r in sample:
        for col in ("expected_settlement_utc", "actual_settlement_utc"):
            v = r.get(col, "")
            if v and not re.match(r"\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(Z|\\+00:00)", v):
                fails.append("column %s value %r is not ISO 8601 UTC format" % (col, v))
    _finish(fails)
main()
'''

# ── q12: SHA-256 sign-off（V7 Bash sign-off）────────────────────────────────────
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign = _read(ws / "output" / "report_signoff.txt")
    if sign is None:
        _finish(["file not found: output/report_signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff line must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    csv_path = ws / "output" / "order_level_diff_report.csv"
    if not csv_path.exists():
        _finish(["cannot verify hash: output/order_level_diff_report.csv missing"])
    digest = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s != recomputed %s" % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

# ── q13: 合规整改计划（V3 P4 隐式 + V9 verbatim）───────────────────────────────
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "corrective_action_plan.md")
    if txt is None:
        _finish(["file not found: output/corrective_action_plan.md"])
    low = txt.lower()
    # 结构层: 含 incident_ref
    if "2024-11-03" not in txt:
        fails.append("CAP must reference incident_ref (2024-11-03)")
    # 真值层: Rule citations
    if "15c3-5(b)" not in txt:
        fails.append("CAP must cite 'Rule 15c3-5(b)' (not just 'Rule 15c3-5')")
    if "15c6-1" not in txt:
        fails.append("CAP must cite 'Rule 15c6-1' (T+1 settlement)")
    # V9: timezone automation fix must be present
    if not re.search(r"timezone|dst|utc.?offset|daylight", low):
        fails.append("CAP must include a timezone/DST automation remediation item")
    # P4 隐式: owner field in each item — check at least 4 owner mentions
    owner_count = len(re.findall(r"\\bowner\\b", low))
    if owner_count < 4:
        fails.append("CAP must have >= 4 remediation items each with an 'owner' field (found %d 'owner' mentions)" % owner_count)
    # deadline_days: positive integer must appear
    deadlines = re.findall(r"deadline.?days[^\\d]*(\\d+)", low)
    if not deadlines:
        fails.append("CAP must include deadline_days fields with positive int values")
    else:
        for d in deadlines:
            if int(d) <= 0:
                fails.append("deadline_days value %r must be a positive integer" % d)
    _finish(fails)
main()
'''

# ── q14: 监管提交摘要（V3 P5 隐式字段顺序 + V4 数值闭合 + q3 window count 连锁）──
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "regulatory_submission_summary.json")
    if txt is None:
        _finish(["file not found: output/regulatory_submission_summary.json"])
    try:
        data = json.loads(txt)
    except json.JSONDecodeError as e:
        _finish(["invalid JSON: " + str(e)])
    # P5: field order check (incident_date must come before rule_violated, before financial_impact, ...)
    required_order = ["incident_date", "rule_violated", "financial_impact", "remediation_count", "submission_date"]
    keys = [k for k in data.keys() if k in set(required_order)]
    order_idx = [required_order.index(k) for k in keys if k in required_order]
    if order_idx != sorted(order_idx):
        fails.append("P5 field order violated: required incident_date->rule_violated->financial_impact->remediation_count->submission_date (got %s)" % keys)
    # 真值层
    for req in required_order:
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    rule = str(data.get("rule_violated", ""))
    if "15c3-5(b)" not in rule:
        fails.append("rule_violated must contain '15c3-5(b)' (got %r)" % rule)
    try:
        rc = int(data.get("remediation_count"))
    except (TypeError, ValueError):
        _finish(["remediation_count not an int"])
    if rc < 4:
        fails.append("remediation_count == %d (expected >= 4)" % rc)
    if data.get("incident_date") != "2024-11-03":
        fails.append("incident_date == %r (expected '2024-11-03')" % data.get("incident_date"))
    # V4 cross-round closure: financial_impact must reference the AROS audit log window count (39)
    fi = str(data.get("financial_impact", ""))
    if "39" not in fi:
        fails.append(
            "financial_impact must reference '39' (the AROS audit log window count from q3 — "
            "entries with timestamp_utc_reported in 14:00-15:00 UTC on 2024-11-03); "
            "do not use the position_delta_report.csv total (87) or bot_summary figure (63)"
        )
    _finish(fails)
main()
'''

# ── q15: 回测结果（V4 数值闭合 + V8 schema）────────────────────────────────────
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "backtest_result.json")
    if err: _finish([err])
    # 字段层
    for req in ("config_timezone_offset", "simulated_settlement_utc",
                "expected_settlement_utc", "match", "script_version"):
        if req not in data:
            fails.append("missing field: " + req)
    if fails: _finish(fails)
    # 真值层
    try:
        tz_off = int(data.get("config_timezone_offset"))
    except (TypeError, ValueError):
        _finish(["config_timezone_offset not an int"])
    if tz_off != -5:
        fails.append("config_timezone_offset == %d (expected -5 for correct EST)" % tz_off)
    if data.get("match") is not True:
        fails.append("match == %r (expected true)" % data.get("match"))
    sim = str(data.get("simulated_settlement_utc", ""))
    if "2024-11-03T21:00:00" not in sim:
        fails.append("simulated_settlement_utc must contain '2024-11-03T21:00:00' (CME 15:00 CT = 21:00 UTC in EST, got %r)" % sim)
    exp = str(data.get("expected_settlement_utc", ""))
    if "2024-11-03T21:00:00" not in exp:
        fails.append("expected_settlement_utc must contain '2024-11-03T21:00:00Z' (got %r)" % exp)
    _finish(fails)
main()
'''

# ── q16: 最终提交签名（V7 终轮 sign-off）────────────────────────────────────────
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign = _read(ws / "output" / "final_submission_signoff.txt")
    if sign is None:
        _finish(["file not found: output/final_submission_signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff line must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    backtest_p = ws / "output" / "backtest_result.json"
    cap_p = ws / "output" / "corrective_action_plan.md"
    if not backtest_p.exists():
        _finish(["cannot verify hash: output/backtest_result.json missing"])
    if not cap_p.exists():
        _finish(["cannot verify hash: output/corrective_action_plan.md missing"])
    # 两文件字节串拼接后 SHA-256（backtest first, then CAP）
    combined = backtest_p.read_bytes() + cap_p.read_bytes()
    digest = hashlib.sha256(combined).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s != recomputed %s" % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

# ── Preference checker (P1-P5) ──────────────────────────────────────────────────
PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sec3a preference checker:
P1 — all JSON output uses snake_case field names (no camelCase/PascalCase)
P2 — all JSON deliverables carry top-level schema_version == "1.0"
P3 — regulatory citations include specific sub-paragraph (e.g., 'Rule 15c3-5(b)')
P4 — CAP items each include an owner field
P5 — regulatory submission JSON field order: incident_date → rule_violated → financial_impact → remediation_count → submission_date
"""
import sys, re, json, argparse
from pathlib import Path

P5_ORDER = ["incident_date", "rule_violated", "financial_impact", "remediation_count", "submission_date"]


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """All JSON outputs must carry top-level schema_version == '1.0'."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P1: top-level is not object, skip"
    if str(data.get("schema_version")) != "1.0":
        return False, "P1: missing top-level schema_version == \\"1.0\\" (got %r)" % data.get("schema_version")
    return True, "P1: PASSED"


def check_P2(ws, target):
    """All JSON field names must be snake_case (no camelCase or PascalCase)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    if not target.endswith(".json"):
        return True, "P2: not a JSON file, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P2: target is not valid JSON"
    # Flatten all keys recursively
    def all_keys(obj):
        if isinstance(obj, dict):
            for k in obj.keys():
                yield k
                yield from all_keys(obj[k])
        elif isinstance(obj, list):
            for item in obj:
                yield from all_keys(item)
    bad = []
    for k in all_keys(data):
        if k in ("schema_version",):
            continue
        # camelCase: starts with lowercase, has uppercase letter inside
        if re.match(r"[a-z][a-z0-9]*[A-Z]", k):
            bad.append(k)
        # PascalCase: starts with uppercase
        if re.match(r"[A-Z]", k):
            bad.append(k)
    if bad:
        return False, "P2: non-snake_case field names found: %s" % bad[:5]
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Regulatory citations must include sub-paragraph (e.g., '15c3-5(b)' not '15c3-5' alone)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    # If the file mentions 15c3-5 at all, it must include the sub-paragraph (b)
    if re.search(r"15c3-5", txt):
        if not re.search(r"15c3-5\\([a-z]\\)", txt) and not re.search(r"15c3-5\\(b\\)", txt):
            return False, "P3: found '15c3-5' without sub-paragraph; must cite '15c3-5(b)'"
    return True, "P3: PASSED"


def check_P4(ws, target):
    """CAP items each must include an 'owner' field."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    # For markdown CAP files: at least 4 'owner' mentions
    low = txt.lower()
    count = len(re.findall(r"\\bowner\\b", low))
    if count < 4:
        return False, "P4: fewer than 4 'owner' mentions in CAP (found %d); each item must have an owner" % count
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Regulatory submission JSON must have top-level fields in fixed order."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P5: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P5: not a JSON object, skip"
    present = [k for k in data.keys() if k in set(P5_ORDER)]
    idx = [P5_ORDER.index(k) for k in present]
    if idx != sorted(idx):
        return False, "P5: field order wrong: required incident_date→rule_violated→financial_impact→remediation_count→submission_date (got %s)" % present
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
