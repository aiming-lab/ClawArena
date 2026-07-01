#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_eng3_checks.py — 生成 eng3 的全部 exec_check 校验脚本到 eval/eng3/scripts/。

每个 check_qNN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_eng3.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/eng3/scripts")
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
'''

CHECKS = {}

# ---------------------------------------------------------------------------
# Q1: incident start from raw_alerts.jsonl
# ---------------------------------------------------------------------------
CHECKS["check_q01"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q01_incident_start.json")
    if err: _finish([err])
    # 字段存在性
    for k in ("incident_start_utc", "component", "message_excerpt"):
        if k not in data:
            fails.append("missing key: " + k)
    if fails: _finish(fails)
    # 真值层：incident_start_utc 必须精确为 2024-06-20T17:47:00Z（无容差，raw_alerts.jsonl 有确切秒数）
    ts = data.get("incident_start_utc", "")
    if ts != "2024-06-20T17:47:00Z":
        fails.append("incident_start_utc == %r (must be exactly \\'2024-06-20T17:47:00Z\\' — read the CRITICAL alert timestamp verbatim from raw_alerts.jsonl)" % ts)
    # component 必须含 lua 或 rate-limit
    comp = str(data.get("component", "")).lower()
    if "lua" not in comp and "rate" not in comp:
        fails.append("component == %r (must contain \\'lua\\' or \\'rate\\')" % data.get("component"))
    # message_excerpt 须包含函数名 get_cookie_key（摘自原始 alert message 前 80 字符）
    excerpt = str(data.get("message_excerpt", ""))
    if "get_cookie_key" not in excerpt:
        fails.append("message_excerpt %r must contain \\'get_cookie_key\\' (from the CRITICAL alert message in raw_alerts.jsonl)" % excerpt[:60])
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q2: backbone congestion window
# ---------------------------------------------------------------------------
CHECKS["check_q02"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q02_backbone_window.json")
    if err: _finish([err])
    for k in ("start_utc", "end_utc", "duration_seconds"):
        if k not in data:
            fails.append("missing key: " + k)
    if fails: _finish(fails)
    # start ≈ 17:33 ±60s
    s = data.get("start_utc", "")
    if not re.match(r"2024-06-20T17:3[23]:[0-5]\\dZ", s):
        fails.append("start_utc == %r (expected 2024-06-20T17:3[23]:xxZ, ±60s of 17:33)" % s)
    # end ≈ 17:50 ±60s
    e = data.get("end_utc", "")
    if not re.match(r"2024-06-20T17:[45][0-9]:[0-5]\\dZ", e):
        fails.append("end_utc == %r (expected 2024-06-20T17:4[89]:xxZ or 17:5[01]:xxZ, ±60s of 17:50)" % e)
    # duration_seconds ∈ [900, 1100]
    try:
        ds = int(data.get("duration_seconds"))
        if not (900 <= ds <= 1100):
            fails.append("duration_seconds == %d (expected in [900, 1100], i.e. ~17 min)" % ds)
    except (TypeError, ValueError):
        fails.append("duration_seconds not numeric: %r" % data.get("duration_seconds"))
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q3: peak metrics (V8 schema-by-shape + V5 anti-bot)
# ---------------------------------------------------------------------------
CHECKS["check_q03"] = '''
def _get_val(obj, key):
    """支持 {key: float} 或 {key: {value: float, unit: ...}} 两种形式。"""
    v = obj.get(key)
    if isinstance(v, dict):
        return v.get("value")
    return v

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q03_peak_metrics.json")
    if err: _finish([err])
    for k in ("peak_cdn_error_pct", "peak_5xx_pct", "ttfb_p99_multiplier"):
        if k not in data:
            fails.append("missing key: " + k)
    if fails: _finish(fails)
    # peak_cdn_error_pct ∈ [2.0, 2.2]（V5：0.21% 是诱饵，必须 FAIL）
    cdn = _get_val(data, "peak_cdn_error_pct")
    try:
        cdn = float(cdn)
        if not (2.0 <= cdn <= 2.2):
            fails.append("peak_cdn_error_pct == %.4f (expected [2.0, 2.2]; 0.21 is the bot decoy — use real metrics)" % cdn)
    except (TypeError, ValueError):
        fails.append("peak_cdn_error_pct not numeric: %r" % cdn)
    # peak_5xx_pct ∈ [3.4, 3.5]
    p5xx = _get_val(data, "peak_5xx_pct")
    try:
        p5xx = float(p5xx)
        if not (3.4 <= p5xx <= 3.5):
            fails.append("peak_5xx_pct == %.4f (expected [3.4, 3.5])" % p5xx)
    except (TypeError, ValueError):
        fails.append("peak_5xx_pct not numeric: %r" % p5xx)
    # ttfb_p99_multiplier == 3
    mult = _get_val(data, "ttfb_p99_multiplier")
    try:
        if int(float(mult)) != 3:
            fails.append("ttfb_p99_multiplier == %r (expected 3)" % mult)
    except (TypeError, ValueError):
        fails.append("ttfb_p99_multiplier not numeric: %r" % mult)
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q4: honeybot discrepancies (V5)
# ---------------------------------------------------------------------------
CHECKS["check_q04"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q04_honeybot_discrepancies.json")
    if err: _finish([err])
    disc = data.get("discrepancies")
    if not isinstance(disc, list) or len(disc) == 0:
        _finish(["discrepancies must be a non-empty array"])
    # 必须含 error_rate 失真（0.21 vs 2.1）
    has_err = False
    has_dur = False
    for d in disc:
        if not isinstance(d, dict): continue
        # 检查字段 field 或 bot_value 或 correct_value 含关键词
        all_text = " ".join(str(v) for v in d.values()).lower()
        if "0.21" in all_text and ("2.1" in all_text or "error" in all_text):
            has_err = True
        if ("37" in all_text and "100" in all_text) or ("duration" in all_text and "37" in all_text):
            has_dur = True
        if not has_err and ("cdn" in all_text or "error" in all_text or "rate" in all_text):
            if "0.21" in all_text:
                has_err = True
        if not has_dur and ("duration" in all_text or "minute" in all_text):
            if "37" in all_text:
                has_dur = True
    if not has_err:
        fails.append("discrepancies missing error_rate distortion (bot 0.21% vs real 2.1%)")
    if not has_dur:
        fails.append("discrepancies missing duration distortion (bot 37 min vs real 100 min)")
    # 每条须含 source 字段（非空）
    for i, d in enumerate(disc):
        if isinstance(d, dict) and not d.get("source"):
            fails.append("discrepancies[%d] missing non-empty 'source' field" % i)
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q5: buggy Lua functions from v1 (V6 red herring + V9 verbatim)
# ---------------------------------------------------------------------------
CHECKS["check_q05"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q05_buggy_functions.json")
    if err: _finish([err])
    funcs = set(str(f) for f in (data.get("functions") or []))
    # 必须包含全部三个缺陷函数名（均出自 rule_engine_v1.lua 文件头注释及代码）
    for need in ("get_cookie_key", "has_valid_cookie_broken", "parent_key_generator"):
        if need not in funcs:
            fails.append("functions missing verbatim name %r (from rule_engine_v1.lua Bug functions annotation)" % need)
    # source_file 必须含 rule_engine_v1（V6 guard：不能用 LEGACY）
    src = str(data.get("source_file", "")).lower()
    if "rule_engine_v1" not in src:
        fails.append("source_file %r must contain \\'rule_engine_v1\\'" % data.get("source_file"))
    if "legacy" in src:
        fails.append("source_file %r must NOT be the LEGACY file" % data.get("source_file"))
    # rejected_file 必须含 LEGACY
    rej = str(data.get("rejected_file", "")).lower()
    if "legacy" not in rej:
        fails.append("rejected_file %r must contain \\'LEGACY\\' (the deprecated archive)" % data.get("rejected_file"))
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q6: duration (V4 cross-round closure with Q1)
# ---------------------------------------------------------------------------
CHECKS["check_q06"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q06_duration.json")
    if err: _finish([err])
    for k in ("start_utc", "end_utc", "duration_minutes"):
        if k not in data:
            fails.append("missing key: " + k)
    if fails: _finish(fails)
    # duration_minutes ∈ [98, 102]
    try:
        dm = int(data.get("duration_minutes"))
        if not (98 <= dm <= 102):
            fails.append("duration_minutes == %d (expected [98, 102])" % dm)
    except (TypeError, ValueError):
        fails.append("duration_minutes not int: %r" % data.get("duration_minutes"))
    # end_utc ≈ 2024-06-20T19:27:00Z ±60s
    end = data.get("end_utc", "")
    if not re.match(r"2024-06-20T19:2[678]:[0-5]\\dZ", end):
        fails.append("end_utc == %r (expected ~2024-06-20T19:27:00Z ±60s)" % end)
    # V4 cross-round: start_utc must match q01_incident_start.json exactly
    q01, e1 = _load_json(ws / "output" / "q01_incident_start.json")
    if not e1 and q01 is not None:
        expected_start = q01.get("incident_start_utc")
        if expected_start and data.get("start_utc") != expected_start:
            fails.append("start_utc %r != q01 incident_start_utc %r (cross-round drift not allowed)" % (
                data.get("start_utc"), expected_start))
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q7: region capacity (V8 schema-by-shape)
# ---------------------------------------------------------------------------
CHECKS["check_q07"] = '''
def _get_val(obj, key):
    v = obj.get(key)
    if isinstance(v, dict):
        return v.get("value")
    return v

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q07_region_impact.json")
    if err: _finish([err])
    for k in ("western_europe_loss_pct", "eastern_europe_loss_pct"):
        if k not in data:
            fails.append("missing key: " + k)
    if fails: _finish(fails)
    # western_europe_loss_pct == 10.0 精确（±0.01，读自 region_capacity.csv）
    wv = _get_val(data, "western_europe_loss_pct")
    try:
        if not (9.99 <= float(wv) <= 10.01):
            fails.append("western_europe_loss_pct.value == %r (expected exactly 10.0 from region_capacity.csv; no rounding allowed)" % wv)
    except (TypeError, ValueError):
        fails.append("western_europe_loss_pct not numeric: %r" % wv)
    # eastern_europe_loss_pct == 4.0 精确（±0.01，读自 region_capacity.csv）
    ev = _get_val(data, "eastern_europe_loss_pct")
    try:
        if not (3.99 <= float(ev) <= 4.01):
            fails.append("eastern_europe_loss_pct.value == %r (expected exactly 4.0 from region_capacity.csv; no rounding allowed)" % ev)
    except (TypeError, ValueError):
        fails.append("eastern_europe_loss_pct not numeric: %r" % ev)
    # P2: 值必须是 value/unit 对象结构，unit 必须为 "percent"
    for k in ("western_europe_loss_pct", "eastern_europe_loss_pct"):
        v = data.get(k)
        if not isinstance(v, dict):
            fails.append("%s must be an object {value, unit} (P2 requirement); got %r" % (k, v))
        elif v.get("unit") != "percent":
            fails.append("%s.unit must be \\'percent\\' (P2 requirement); got %r" % (k, v.get("unit")))
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q8: DRAFT_v1.md root cause (V9 verbatim + P3)
# ---------------------------------------------------------------------------
CHECKS["check_q08"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "postmortem" / "DRAFT_v1.md")
    if txt is None:
        _finish(["file not found: postmortem/DRAFT_v1.md"])
    # V9 verbatim Lua function names
    for fn in ("get_cookie_key", "has_valid_cookie_broken", "parent_key_generator"):
        if fn not in txt:
            fails.append("DRAFT_v1.md missing verbatim Lua function name: %r" % fn)
    # DDoS deployment timestamps
    if "14:14" not in txt:
        fails.append("DRAFT_v1.md missing DDoS deploy start time \\'14:14\\'")
    if "17:06" not in txt:
        fails.append("DRAFT_v1.md missing DDoS deploy complete time \\'17:06\\'")
    # tail-call mention
    if "tail call" not in txt.lower() and "tail-call" not in txt.lower():
        fails.append("DRAFT_v1.md must mention \\'tail call\\' or \\'tail-call\\' recursion mechanism")
    # P3: 所有 ## 标题须含双语斜杠分隔符（静默考察，EM Feishu DM 已通知 P3）
    headings = re.findall(r"^##\\s+.+", txt, re.MULTILINE)
    bad_h = [h for h in headings if "/" not in h]
    if bad_h:
        fails.append("DRAFT_v1.md heading(s) missing bilingual \\'/\\' separator (P3 applies): %s" % bad_h[:2])
    # 必须包含事件开始时间戳的完整 ISO 格式（V4 前置锚点）
    if "2024-06-20T17:47" not in txt:
        fails.append("DRAFT_v1.md must include full ISO timestamp \\'2024-06-20T17:47\\' for incident start")
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q9: SLA credit (V9 verbatim + V8 arithmetic + Update1)
# ---------------------------------------------------------------------------
CHECKS["check_q09"] = '''
SLA_FORMULA = "(Outage Period minutes * Affected Customer Ratio) / Scheduled Availability minutes"

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q09_sla_credit.json")
    if err: _finish([err])
    for k in ("formula", "outage_minutes", "affected_customer_ratio", "scheduled_minutes", "credit_ratio"):
        if k not in data:
            fails.append("missing key: " + k)
    if fails: _finish(fails)
    # V9: formula 逐字包含
    formula = str(data.get("formula", ""))
    if SLA_FORMULA not in formula:
        fails.append("formula field does not contain verbatim text: %r" % SLA_FORMULA)
    # outage_minutes == 100
    om = data.get("outage_minutes")
    try:
        if not (98 <= int(om) <= 102):
            fails.append("outage_minutes == %r (expected 100)" % om)
    except (TypeError, ValueError):
        fails.append("outage_minutes not int: %r" % om)
    # scheduled_minutes 必须精确为 43200（business_sla.md 明文写明 30-day month = 43200 minutes）
    sm = data.get("scheduled_minutes")
    try:
        sm = int(sm)
        if sm != 43200:
            fails.append("scheduled_minutes == %d (must be exactly 43200 for 30-day billing month as per business_sla.md)" % sm)
    except (TypeError, ValueError):
        fails.append("scheduled_minutes not int: %r" % sm)
    # affected_customer_ratio 必须匹配 sla/affected_customers.csv 的实际计算值（63/3000=0.021）±0.0005
    ar = data.get("affected_customer_ratio")
    try:
        ar_f = float(ar)
        if not (0.0205 <= ar_f <= 0.0215):
            fails.append("affected_customer_ratio == %.6f (must equal 63/3000=0.021000 from sla/affected_customers.csv ±0.0005)" % ar_f)
    except (TypeError, ValueError):
        fails.append("affected_customer_ratio not numeric: %r" % ar)
    # credit_ratio = (outage_minutes * affected_ratio) / scheduled_minutes ±0.0000010
    cr = data.get("credit_ratio")
    try:
        om_f = float(data.get("outage_minutes")); ar_f2 = float(ar); sm_f = float(sm); cr_f = float(cr)
        expected = (om_f * ar_f2) / sm_f
        if abs(cr_f - expected) > 0.000001:
            fails.append("credit_ratio == %.8f does not match (outage*ratio/scheduled) == %.8f (delta > 0.000001)" % (cr_f, expected))
    except (TypeError, ValueError, ZeroDivisionError):
        fails.append("could not compute arithmetic check for credit_ratio")
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q10: causal chains (V1 multi-source)
# ---------------------------------------------------------------------------
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q10_causal_chains.json")
    if err: _finish([err])
    for k in ("chain_1", "chain_2"):
        if k not in data:
            fails.append("missing key: " + k)
    if fails: _finish(fails)
    c1 = data.get("chain_1") or {}
    c2 = data.get("chain_2") or {}
    # chain_1: trigger含 DDoS/ddos, mechanism含 lua/tail call
    c1_text = " ".join(str(v) for v in c1.values()).lower()
    if not re.search(r"ddos|ddo\\s", c1_text):
        fails.append("chain_1 trigger/mechanism must reference 'DDoS' or 'ddos'")
    if not re.search(r"lua|tail.?call", c1_text):
        fails.append("chain_1 mechanism must reference 'Lua' or 'tail call'")
    # chain_2: trigger含 backbone/congestion, 时间窗含 17:33 或 traffic.?manager
    c2_text = " ".join(str(v) for v in c2.values()).lower()
    if not re.search(r"backbone|congestion", c2_text):
        fails.append("chain_2 trigger must reference 'backbone' or 'congestion'")
    if not re.search(r"17:33|17:50|traffic.?manager|trafficmanager", c2_text):
        fails.append("chain_2 must reference 17:33/17:50 time window or Traffic Manager")
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q11: actions tracker CSV (V3 implicit preference)
# ---------------------------------------------------------------------------
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    p = ws / "output" / "q11_actions_tracker.csv"
    if not p.exists():
        _finish(["file not found: output/q11_actions_tracker.csv"])
    rows = list(csv.DictReader(p.open(encoding="utf-8")))
    # 行数 >= 7
    if len(rows) < 7:
        fails.append("q11_actions_tracker.csv has %d data rows (expected >= 7)" % len(rows))
    # 必须含指定列
    if rows:
        headers = set(rows[0].keys())
        for col in ("id", "priority", "owner", "deadline", "status"):
            if col not in headers:
                fails.append("missing column: %r" % col)
    # deadline 格式 YYYY-MM-DD
    for r in rows:
        dl = r.get("deadline", "")
        if dl and not re.match(r"^\\d{4}-\\d{2}-\\d{2}$", dl):
            fails.append("deadline %r not YYYY-MM-DD format" % dl)
            break
    # 必须含关键行动项
    all_text = " ".join(r.get("id", "") + " " + r.get("title", "") + " " + r.get("status", "")
                        for r in rows).lower()
    for kw in ("rate-limit", "staging", "execution"):
        if kw not in all_text:
            fails.append("actions tracker missing item with keyword %r (rate-limit modernization / staging rollout / execution time limit)" % kw)
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q12: customer notice (V5 anti-bot + V4 duration closure + P4)
# ---------------------------------------------------------------------------
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "communications" / "customer_notice_draft.md")
    if txt is None:
        _finish(["file not found: communications/customer_notice_draft.md"])
    low = txt.lower()
    # P4: [ArcNode Status] prefix
    if "[arcnode status]" not in low:
        fails.append("customer_notice_draft.md missing \\'[ArcNode Status]\\' prefix (P4)")
    # V4: duration consistency with Q6 (100 min or 1 hour 40 min)
    has_dur = "100 minutes" in low or "1 hour 40 minutes" in low or "1 hour 40" in low
    if not has_dur:
        fails.append("customer_notice_draft.md must state \\'100 minutes\\' or \\'1 hour 40 minutes\\' duration")
    # V5: must NOT contain bot error rate 0.21%
    if "0.21" in txt:
        fails.append("customer_notice_draft.md contains distorted bot error rate \\'0.21\\' — use real metrics")
    # V5: must explicitly state real peak CDN error rate 2.1%（而非模糊表达，不能遗漏）
    if "2.1%" not in txt and "2.10%" not in txt:
        fails.append("customer_notice_draft.md must explicitly state the real peak CDN error rate \\'2.1%\\' or \\'2.10%\\' (not the bot decoy 0.21%)")
    # SLA claim deadline 5 business days
    if "5 business" not in low and "five business" not in low:
        fails.append("customer_notice_draft.md must mention \\'5 business days\\' SLA claim deadline")
    # V4 cross-round: SLA claims portal URL 必须出现（email_thread.eml 提供模板）
    if "arcnode.io/sla" not in low and "sla-claim" not in low and "sla claim" not in low.replace("-", " "):
        fails.append("customer_notice_draft.md must include SLA claims portal URL reference (e.g. arcnode.io/sla-claims)")
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q13: actions tracker v2 with supersede (V10)
# ---------------------------------------------------------------------------
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    p = ws / "output" / "q13_actions_tracker_v2.csv"
    if not p.exists():
        _finish(["file not found: output/q13_actions_tracker_v2.csv"])
    rows = list(csv.DictReader(p.open(encoding="utf-8")))
    # total rows 应为 9（7 original + CA-003-revised - CA-003 exists but stays）
    # Actually: original 7 items remain, CA-003-revised added = 8 items, but CA-003 stays as superseded
    # So total = 8 rows (CA-001,CA-002,CA-003,CA-003-revised,CA-004,CA-005,CA-006,CA-007)
    # But wait - BRIEF says 7 items in v1, v2 supersedes CA-003 and adds CA-003-revised = 8 items
    # Adjusted: accept 8 or 9
    if len(rows) < 8:
        fails.append("q13_actions_tracker_v2.csv has %d rows (expected >= 8: 7 original + CA-003-revised)" % len(rows))
    # CA-003 must have superseded_by = CA-003-revised
    headers = set(rows[0].keys()) if rows else set()
    if "superseded_by" not in headers:
        fails.append("q13_actions_tracker_v2.csv missing 'superseded_by' column")
    else:
        ca3_rows = [r for r in rows if r.get("id", "").strip() == "CA-003"]
        if not ca3_rows:
            fails.append("CA-003 row missing from q13_actions_tracker_v2.csv")
        else:
            sup = ca3_rows[0].get("superseded_by", "").strip()
            if "CA-003-revised" not in sup and "ca-003-revised" not in sup.lower():
                fails.append("CA-003.superseded_by == %r (expected 'CA-003-revised')" % sup)
    # CA-003-revised must exist
    ca3r = [r for r in rows if "CA-003-revised" in r.get("id", "") or
            "automated" in r.get("title", "").lower() or "watchdog" in r.get("title", "").lower()]
    if not ca3r:
        fails.append("CA-003-revised (automated-restart-watchdog) row missing from tracker v2")
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q14: DRAFT_v2.md timeline (V4 cross-round closure)
# ---------------------------------------------------------------------------
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "postmortem" / "DRAFT_v2.md")
    if txt is None:
        _finish(["file not found: postmortem/DRAFT_v2.md"])
    # 六个关键时间点
    for ts in ("17:47", "17:33", "17:50", "18:04", "19:27", "19:34"):
        if ts not in txt:
            fails.append("DRAFT_v2.md missing timestamp %r in Timeline section" % ts)
    # V4 cross-round: 17:47 must align with q01, 19:27 must align with q06
    q01, e1 = _load_json(ws / "output" / "q01_incident_start.json")
    if not e1 and q01:
        start = q01.get("incident_start_utc", "")
        # extract HH:MM from start
        m1 = re.search(r"T(\\d{2}:\\d{2})", start)
        if m1 and m1.group(1) not in txt:
            fails.append("DRAFT_v2.md timeline does not contain the Q1 start time %s" % m1.group(1))
    q06, e6 = _load_json(ws / "output" / "q06_duration.json")
    if not e6 and q06:
        end = q06.get("end_utc", "")
        m6 = re.search(r"T(\\d{2}:\\d{2})", end)
        if m6 and m6.group(1) not in txt:
            fails.append("DRAFT_v2.md timeline does not contain Q6 end time %s" % m6.group(1))
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q15: escalations multi-channel (V1 + P5)
# ---------------------------------------------------------------------------
CHECKS["check_q15"] = '''
VALID_METHODS = {"page", "dm", "alert"}

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q15_escalations.json")
    if err: _finish([err])
    # generated_at top-level
    if not data.get("generated_at"):
        fails.append("q15_escalations.json missing top-level 'generated_at' field (P5)")
    escs = data.get("escalations")
    if not isinstance(escs, list) or len(escs) < 3:
        _finish(["escalations must be an array with >= 3 entries (got %s)" % repr(escs)[:40]])
    # method valid
    for i, e in enumerate(escs):
        m = str(e.get("method", "")).lower()
        if m not in VALID_METHODS:
            fails.append("escalations[%d].method == %r (must be page/dm/alert)" % (i, e.get("method")))
    # at least 1 slack, 1 feishu
    channels = set(str(e.get("channel", "")).lower() for e in escs)
    if not any("slack" in c for c in channels):
        fails.append("escalations must include at least 1 entry from Slack channel")
    if not any("feishu" in c for c in channels):
        fails.append("escalations must include at least 1 entry from Feishu channel")
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q16: SHA-256 sign-off (V7)
# ---------------------------------------------------------------------------
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign = _read(ws / "output" / "q16_signoff.txt")
    if sign is None:
        _finish(["file not found: output/q16_signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    final = ws / "postmortem" / "FINAL.md"
    if not final.exists():
        _finish(["cannot verify hash: postmortem/FINAL.md missing"])
    digest = hashlib.sha256(final.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s... != recomputed %s..." % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Q17: FINAL.md (V9 verbatim + V4 + V10 supersede + P3)
# ---------------------------------------------------------------------------
CHECKS["check_q17"] = '''
SLA_FORMULA = "(Outage Period minutes * Affected Customer Ratio) / Scheduled Availability minutes"

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "postmortem" / "FINAL.md")
    if txt is None:
        _finish(["file not found: postmortem/FINAL.md"])
    lines = txt.splitlines()
    # file >= 80 lines
    if len(lines) < 80:
        fails.append("FINAL.md has %d lines (expected >= 80)" % len(lines))
    # V9 verbatim anchors
    for anchor in ("get_cookie_key", "parent_key_generator",
                   "2024-06-20T17:47", "2024-06-20T19:27"):
        if anchor not in txt:
            fails.append("FINAL.md missing verbatim anchor: %r" % anchor)
    # V9 SLA formula
    if SLA_FORMULA not in txt:
        fails.append("FINAL.md missing verbatim SLA formula: %r" % SLA_FORMULA)
    # V10 supersede: CA-003 with strikethrough ~~
    if "~~" not in txt:
        fails.append("FINAL.md must use ~~ strikethrough to mark the superseded action item (CA-003)")
    # CA-003-revised (automated watchdog) must appear without strikethrough
    if "automated-restart-watchdog" not in txt and "automated restart watchdog" not in txt.lower():
        fails.append("FINAL.md must include CA-003-revised (automated-restart-watchdog) as active item")
    _finish(fails)
main()
'''

# ---------------------------------------------------------------------------
# Preference checker P1-P5
# ---------------------------------------------------------------------------
PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eng3 preference checker.

P1: All timestamps in output JSON must use ISO 8601 UTC YYYY-MM-DDTHH:MM:SSZ format.
P2: Percentage/ratio fields must be formatted as {value: float_2dp, unit: "percent"} objects.
P3: Postmortem section headings must use bilingual format "## Section Name / 章节名称".
P4: Customer-facing documents must include [ArcNode Status] prefix.
P5: JSON outputs must include top-level "generated_at" field (ISO 8601 UTC); file names snake_case.
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """All timestamps must be ISO 8601 UTC YYYY-MM-DDTHH:MM:SSZ — no other format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except (json.JSONDecodeError, Exception):
        return True, "P1: target not JSON, skip"
    # Find all string values and check timestamp-like ones
    ts_fields = ["incident_start_utc", "start_utc", "end_utc", "peak_time_utc",
                 "time_utc", "generated_at"]
    def _check_val(v):
        if not isinstance(v, str):
            return True
        # if it looks like a timestamp (contains T and colon)
        if re.search(r"\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}", v):
            if not re.match(r"\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$", v):
                return False
        return True
    def _walk(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in ts_fields or "utc" in k.lower() or "timestamp" in k.lower() or "time" in k.lower():
                    if isinstance(v, str) and re.search(r"\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}", v):
                        if not re.match(r"\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$", v):
                            return False, v
                if isinstance(v, (dict, list)):
                    ok, bad = _walk(v)
                    if not ok:
                        return ok, bad
        elif isinstance(obj, list):
            for item in obj:
                ok, bad = _walk(item)
                if not ok:
                    return ok, bad
        return True, None
    ok, bad = _walk(data)
    if not ok:
        return False, "P1: timestamp %r not ISO 8601 UTC YYYY-MM-DDTHH:MM:SSZ" % bad
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Percentage fields must be formatted as {value: float, unit: 'percent'}."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except (json.JSONDecodeError, Exception):
        return True, "P2: target not JSON, skip"
    pct_keys = ["peak_cdn_error_pct", "peak_5xx_pct", "western_europe_loss_pct",
                "eastern_europe_loss_pct"]
    for k in pct_keys:
        if k in data:
            v = data[k]
            if not isinstance(v, dict):
                return False, "P2: %s is not an object {value, unit} (got %r)" % (k, v)
            if "unit" not in v or v.get("unit") != "percent":
                return False, "P2: %s.unit must be 'percent' (got %r)" % (k, v.get("unit"))
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Postmortem section headings must use bilingual format '## Name / 名称'."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    headings = re.findall(r"^##\\s+.+", txt, re.MULTILINE)
    if not headings:
        return True, "P3: no ## headings found, skip"
    bad = [h for h in headings if "/" not in h]
    if bad:
        return False, "P3: heading(s) missing bilingual slash separator: %s" % bad[:2]
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Customer-facing documents must include [ArcNode Status] prefix."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    if "[arcnode status]" not in txt.lower():
        return False, "P4: missing '[ArcNode Status]' prefix in %s" % target
    return True, "P4: PASSED"


def check_P5(ws, target):
    """JSON outputs must include top-level 'generated_at' field (ISO 8601 UTC)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    try:
        data = json.loads(txt)
    except (json.JSONDecodeError, Exception):
        return True, "P5: target not JSON, skip"
    if not isinstance(data, dict):
        return True, "P5: top-level not dict, skip"
    ga = data.get("generated_at")
    if not ga:
        return False, "P5: missing top-level 'generated_at' field"
    if not re.match(r"\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$", str(ga)):
        return False, "P5: generated_at %r not ISO 8601 UTC YYYY-MM-DDTHH:MM:SSZ" % ga
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
