#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_prd2_checks.py — 生成 prd2 的全部 exec_check 校验脚本到 eval/prd2/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace（policy_engine 根目录的上一级，即 workspace 根）；
PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_prd2.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5。生成器内容即评测逻辑，可逐脚本审阅。

workspace 约定：所有路径相对 workspace 根（policy_engine/ 目录在 workspace 根下）。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/prd2/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
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

# Q1: 建立平台政策索引
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []

    # YouTube index.json
    data, err = _load_json(pe / "platforms" / "youtube" / "index.json")
    if err: _finish([err])
    cats = data.get("policy_categories") or []
    if len(cats) < 5:
        fails.append("youtube index: policy_categories must have >=5 entries (got %d)" % len(cats))
    if data.get("strike_window_days") != 90:
        fails.append("youtube index: strike_window_days must be 90 (got %r)" % data.get("strike_window_days"))

    # Meta index.json
    data2, err2 = _load_json(pe / "platforms" / "meta" / "index.json")
    if err2: _finish([err2])
    pcc = data2.get("policy_category_count")
    if pcc != 27:
        fails.append("meta index: policy_category_count must be 27 (got %r)" % pcc)

    # TikTok index.json
    data3, err3 = _load_json(pe / "platforms" / "tiktok" / "index.json")
    if err3: _finish([err3])
    if "safety_civility" not in data3:
        fails.append("tiktok index: missing safety_civility field (verbatim category key required)")

    # Reddit index.json
    data4, err4 = _load_json(pe / "platforms" / "reddit" / "index.json")
    if err4: _finish([err4])
    for fld in ("rule1", "rule2", "rule5"):
        if fld not in data4:
            fails.append("reddit index: missing '%s' field" % fld)

    _finish(fails)
main()
'''

# Q2: YouTube 违规阶梯 JSON
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    data, err = _load_json(pe / "platforms" / "youtube" / "strike_system.json")
    if err: _finish([err])

    # warning.expiry_days = 90
    warn = data.get("warning") or {}
    if warn.get("expiry_days") != 90:
        fails.append("warning.expiry_days must be 90 (got %r)" % warn.get("expiry_days"))

    # strike1.freeze_days = 7
    s1 = data.get("strike1") or {}
    if s1.get("freeze_days") != 7:
        fails.append("strike1.freeze_days must be 7 (got %r, not 10)" % s1.get("freeze_days"))

    # strike2.freeze_days = 14
    s2 = data.get("strike2") or {}
    if s2.get("freeze_days") != 14:
        fails.append("strike2.freeze_days must be 14 (got %r)" % s2.get("freeze_days"))

    # strike3.consequence = 'channel_permanent_removal'
    s3 = data.get("strike3") or {}
    cons = str(s3.get("consequence") or "")
    if "channel_permanent_removal" not in cons:
        fails.append("strike3.consequence must contain 'channel_permanent_removal' (got %r)" % cons)

    # window_days = 90
    if data.get("window_days") != 90:
        fails.append("window_days must be 90 (got %r)" % data.get("window_days"))

    _finish(fails)
main()
'''

# Q3: Meta 违规阶梯 JSON (V1: email 声称 strike7=3天 → 错误，官方值=1天)
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    data, err = _load_json(pe / "platforms" / "meta" / "strike_system.json")
    if err: _finish([err])

    strikes = data.get("strikes") or {}

    # strike_7.content_ban_days = 1 (NOT 3 — email/bot error)
    s7 = strikes.get("strike_7") or {}
    s7_days = s7.get("content_ban_days")
    try:
        if int(s7_days) != 1:
            fails.append("strike_7.content_ban_days must be 1 (the email claiming 3 days is WRONG; official value is 1 day; got %r)" % s7_days)
    except (TypeError, ValueError):
        fails.append("strike_7.content_ban_days must be int 1 (got %r)" % s7_days)

    # strike_8.content_ban_days = 3
    s8 = strikes.get("strike_8") or {}
    s8_days = s8.get("content_ban_days")
    try:
        if int(s8_days) != 3:
            fails.append("strike_8.content_ban_days must be 3 (got %r)" % s8_days)
    except (TypeError, ValueError):
        fails.append("strike_8.content_ban_days must be int 3 (got %r)" % s8_days)

    # strike_9.content_ban_days = 7
    s9 = strikes.get("strike_9") or {}
    s9_days = s9.get("content_ban_days")
    try:
        if int(s9_days) != 7:
            fails.append("strike_9.content_ban_days must be 7 (got %r)" % s9_days)
    except (TypeError, ValueError):
        fails.append("strike_9.content_ban_days must be int 7 (got %r)" % s9_days)

    # strike_10plus.content_ban_days = 30
    s10 = strikes.get("strike_10plus") or {}
    s10_days = s10.get("content_ban_days")
    try:
        if int(s10_days) != 30:
            fails.append("strike_10plus.content_ban_days must be 30 (got %r)" % s10_days)
    except (TypeError, ValueError):
        fails.append("strike_10plus.content_ban_days must be int 30 (got %r)" % s10_days)

    _finish(fails)
main()
'''

# Q4: Reddit 执行阶梯 JSON + H1 2025 数据 (V4 + V9)
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    data, err = _load_json(pe / "platforms" / "reddit" / "enforcement_tiers.json")
    if err: _finish([err])

    tiers = data.get("tiers") or []
    if len(tiers) < 3:
        _finish(["enforcement_tiers.json: expected at least 3 tiers, got %d" % len(tiers)])

    # tiers[0].action = 'warning'
    t0_action = str(tiers[0].get("action") or "")
    if "warning" not in t0_action:
        fails.append("tiers[0].action must contain 'warning' (got %r)" % t0_action)

    # tiers[1].suspend_days = 3
    t1_days = tiers[1].get("suspend_days")
    try:
        if int(t1_days) != 3:
            fails.append("tiers[1].suspend_days must be 3 (got %r)" % t1_days)
    except (TypeError, ValueError):
        fails.append("tiers[1].suspend_days must be int 3 (got %r)" % t1_days)

    # tiers[2].suspend_days = 7
    t2_days = tiers[2].get("suspend_days")
    try:
        if int(t2_days) != 7:
            fails.append("tiers[2].suspend_days must be 7 (got %r)" % t2_days)
    except (TypeError, ValueError):
        fails.append("tiers[2].suspend_days must be int 7 (got %r)" % t2_days)

    # h1_2025.harassment.removed = 68550 (±10%)
    h1 = data.get("h1_2025") or {}
    har = h1.get("harassment") or {}
    removed = har.get("removed")
    try:
        removed = int(removed)
        if not (61695 <= removed <= 75405):
            fails.append("h1_2025.harassment.removed must be ~68550 (±10%%), got %d" % removed)
    except (TypeError, ValueError):
        fails.append("h1_2025.harassment.removed must be numeric (got %r)" % removed)

    # h1_2025.hateful.appeal_reversal_rate ≈ 0.300 (±10%)
    hat = h1.get("hateful") or {}
    rev_rate = hat.get("appeal_reversal_rate")
    try:
        rev_rate = float(rev_rate)
        if not (0.270 <= rev_rate <= 0.330):
            fails.append("h1_2025.hateful.appeal_reversal_rate must be ~0.300 (±10%%), got %.4f" % rev_rate)
    except (TypeError, ValueError):
        fails.append("h1_2025.hateful.appeal_reversal_rate must be numeric (got %r)" % rev_rate)

    # rule1_verbatim: must contain the key phrase (V9)
    r1 = str(data.get("rule1_verbatim") or "").lower()
    if "incite violence" not in r1 and "promote hate" not in r1:
        fails.append("rule1_verbatim must contain verbatim Reddit Rule 1 text ('incite violence' or 'promote hate')")

    _finish(fails)
main()
'''

# Q5: TikTok Q1 2025 指标 JSON (V4 + V8)
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    data, err = _load_json(pe / "platforms" / "tiktok" / "q1_2025_report.json")
    if err: _finish([err])

    # videos_removed = 211000000 (±1%)
    vr = data.get("videos_removed")
    try:
        vr = int(vr)
        if not (208890000 <= vr <= 213110000):
            fails.append("videos_removed must be ~211000000 (±1%%), got %d" % vr)
    except (TypeError, ValueError):
        fails.append("videos_removed must be numeric (got %r)" % vr)

    # automated_removed = 184378987 (±1%)
    ar = data.get("automated_removed")
    try:
        ar = int(ar)
        if not (182535197 <= ar <= 186222777):
            fails.append("automated_removed must be ~184378987 (±1%%), got %d" % ar)
    except (TypeError, ValueError):
        fails.append("automated_removed must be numeric (got %r)" % ar)

    # reinstated = 7525184 (±1%)
    ri = data.get("reinstated")
    try:
        ri = int(ri)
        if not (7449932 <= ri <= 7600436):
            fails.append("reinstated must be ~7525184 (±1%%), got %d" % ri)
    except (TypeError, ValueError):
        fails.append("reinstated must be numeric (got %r)" % ri)

    # proactive_rate ≈ 0.990 (±1%)
    pr = data.get("proactive_rate")
    try:
        pr = float(pr)
        if not (0.980 <= pr <= 1.000):
            fails.append("proactive_rate must be ~0.990 (±1%%), got %.4f" % pr)
    except (TypeError, ValueError):
        fails.append("proactive_rate must be numeric (got %r)" % pr)

    # within_24h_rate ≈ 0.943 (±1%)
    hr = data.get("within_24h_rate")
    try:
        hr = float(hr)
        if not (0.934 <= hr <= 0.952):
            fails.append("within_24h_rate must be ~0.943 (±1%%), got %.4f" % hr)
    except (TypeError, ValueError):
        fails.append("within_24h_rate must be numeric (got %r)" % hr)

    _finish(fails)
main()
'''

# Q6: 四平台 SLA 对照表 (V4 + V5: bot 声称 YT 申诉 3 个月 → 蜜罐)
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    data, err = _load_json(pe / "internal" / "platform_sla.json")
    if err: _finish([err])

    yt = data.get("youtube") or {}

    # youtube.appeal_window_strike_months = 6.0 (NOT 3 months — bot decoy)
    aws = yt.get("appeal_window_strike_months")
    try:
        aws = float(aws)
        if not (5.5 <= aws <= 6.5):
            fails.append("youtube.appeal_window_strike_months must be ~6.0 (not 3.0 from bot decoy; got %.1f)" % aws)
    except (TypeError, ValueError):
        fails.append("youtube.appeal_window_strike_months must be numeric ~6.0 (got %r)" % aws)

    # youtube.appeal_window_content_months = 12.0
    awc = yt.get("appeal_window_content_months")
    try:
        awc = float(awc)
        if not (11.5 <= awc <= 12.5):
            fails.append("youtube.appeal_window_content_months must be ~12.0 (got %.1f)" % awc)
    except (TypeError, ValueError):
        fails.append("youtube.appeal_window_content_months must be numeric ~12.0 (got %r)" % awc)

    # reddit.appeal_window_months = 6.0
    rd = data.get("reddit") or {}
    raw = rd.get("appeal_window_months")
    try:
        raw = float(raw)
        if not (5.5 <= raw <= 6.5):
            fails.append("reddit.appeal_window_months must be ~6.0 (got %.1f)" % raw)
    except (TypeError, ValueError):
        fails.append("reddit.appeal_window_months must be numeric ~6.0 (got %r)" % raw)

    # tiktok.strike_expiry_days = 90
    tt = data.get("tiktok") or {}
    sed = tt.get("strike_expiry_days")
    try:
        if int(sed) != 90:
            fails.append("tiktok.strike_expiry_days must be 90 (got %r)" % sed)
    except (TypeError, ValueError):
        fails.append("tiktok.strike_expiry_days must be int 90 (got %r)" % sed)

    _finish(fails)
main()
'''

# Q7: 废弃旧版合规报告标记 (V6: 红鲱鱼)
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    data, err = _load_json(pe / "reports" / "deprecation_log.json")
    if err: _finish([err])

    entries = data.get("entries") or []
    if not isinstance(entries, list):
        _finish(["deprecation_log.json: 'entries' must be a list"])

    # Must have an entry for meta_strike_7 with deprecated=true
    meta_s7_entry = None
    for e in entries:
        key = str(e.get("field") or e.get("key") or e.get("id") or "").lower()
        if "meta" in key and ("strike_7" in key or "strike7" in key):
            meta_s7_entry = e
            break
    if meta_s7_entry is None:
        fails.append("deprecation_log: no entry found for meta strike_7 (e.g. field='meta_strike_7_duration')")
    elif meta_s7_entry.get("deprecated") is not True:
        fails.append("deprecation_log: meta strike_7 entry must have deprecated=true (got %r)" % meta_s7_entry.get("deprecated"))

    # Must have an entry for youtube appeal window with deprecated=true
    yt_appeal_entry = None
    for e in entries:
        key = str(e.get("field") or e.get("key") or e.get("id") or "").lower()
        if "youtube" in key and "appeal" in key:
            yt_appeal_entry = e
            break
    if yt_appeal_entry is None:
        fails.append("deprecation_log: no entry found for youtube appeal window (e.g. field='youtube_appeal_window_strike')")
    elif yt_appeal_entry.get("deprecated") is not True:
        fails.append("deprecation_log: youtube appeal window entry must have deprecated=true (got %r)" % yt_appeal_entry.get("deprecated"))

    _finish(fails)
main()
'''

# Q8: 四平台违规分级对比文档 (V1 + V9; P4 静默考察)
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    txt = _read(pe / "internal" / "policy_matrix_summary.md")
    if txt is None:
        _finish(["file not found: policy_engine/internal/policy_matrix_summary.md"])

    # Must have 4 platform headings
    for plat in ("YouTube", "Meta", "TikTok", "Reddit"):
        if ("## " + plat) not in txt:
            fails.append("policy_matrix_summary.md: missing '## %s' heading" % plat)

    low = txt.lower()

    # YouTube Strike 1 = 7 days freeze (allow table format: "strike 1 | ... | 7 days")
    if not re.search(r"strike.{0,10}1.{0,60}7.{0,20}day|7.{0,20}day.{0,60}strike.{0,10}1", low):
        fails.append("policy_matrix_summary.md: YouTube Strike 1 = 7 days not clearly stated")

    # Meta Strike 7 = 1 day (NOT 3 — V1 error guard)
    if not re.search(r"strike.{0,20}7.{0,30}1.{0,20}day|1.{0,20}day.{0,30}strike.{0,10}7", low):
        fails.append("policy_matrix_summary.md: Meta Strike 7 = 1 day not clearly stated")

    # Reddit Tier 2 = 3 day suspension
    if not re.search(r"tier.{0,20}2.{0,30}3.{0,20}day|3.{0,20}day.{0,30}tier.{0,10}2|3.{0,5}day.{0,15}suspen", low):
        fails.append("policy_matrix_summary.md: Reddit Tier 2 = 3-day suspension not clearly stated")

    # TikTok three-strike permanent ban (NOT two — V1 error guard from feishu DM)
    if not re.search(r"three.{0,20}strike|3.{0,20}strike.{0,30}permanent|thr[ée].{0,20}strik", low):
        fails.append("policy_matrix_summary.md: TikTok 3-strike permanent ban not stated (must say THREE, not two)")

    # P4: [^N] footnote format present
    if "[^" not in txt:
        fails.append("policy_matrix_summary.md: missing [^N] footnote citations (P4 requirement)")

    # P4: ## 参考来源 or ## References section
    if not re.search(r"^## (参考来源|references|sources)", txt, re.IGNORECASE | re.MULTILINE):
        fails.append("policy_matrix_summary.md: missing ## 参考来源 / ## References section (P4 requirement)")

    _finish(fails)
main()
'''

# Q9: 处理申诉案例批次 (update_1 后) (V2 + V8)
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    data, err = _load_json(pe / "internal" / "appeal_tracker.json")
    if err: _finish([err])

    cases = data.get("cases") or {}

    # New cases from update_1 must exist: T-001..T-007, Y-001..Y-006, M-001..M-005, R-001..R-002
    new_case_ids = (
        ["T-%03d" % i for i in range(1, 8)] +
        ["Y-%03d" % i for i in range(1, 7)] +
        ["M-%03d" % i for i in range(1, 6)] +
        ["R-%03d" % i for i in range(1, 3)]
    )
    missing_new = [k for k in new_case_ids if k not in cases]
    if missing_new:
        fails.append("appeal_tracker: missing new cases from update_1: %s" % missing_new[:5])

    # Check new cases have required fields
    for cid in new_case_ids:
        c = cases.get(cid)
        if c is None:
            continue
        for fld in ("status", "platform", "violation_type"):
            if not c.get(fld):
                fails.append("case %s: missing or empty field '%s'" % (cid, fld))
                break

    # Platform coverage: all 4 platforms represented
    new_plats = set()
    for cid in new_case_ids:
        c = cases.get(cid)
        if c:
            new_plats.add(str(c.get("platform", "")).lower())
    for plat in ("youtube", "meta", "tiktok", "reddit"):
        if plat not in new_plats:
            fails.append("appeal_tracker: platform '%s' missing from new cases" % plat)

    # Legacy cases OLD-0050/0051/0052 must be under_review (V2)
    for cid in ("OLD-0050", "OLD-0051", "OLD-0052"):
        c = cases.get(cid)
        if c is None:
            fails.append("appeal_tracker: missing legacy case %s" % cid)
        elif str(c.get("status", "")).lower() != "under_review":
            fails.append("case %s: status must be 'under_review' (update_1 changed it; got %r)" % (cid, c.get("status")))

    # total_cases field must exist
    if "total_cases" not in data:
        fails.append("appeal_tracker: missing 'total_cases' field")

    _finish(fails)
main()
'''

# Q10: 信息冲突分析报告 (V1 + V5)
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    data, err = _load_json(pe / "internal" / "conflict_report.json")
    if err: _finish([err])

    conflicts = data.get("conflicts") or []
    if len(conflicts) < 3:
        fails.append("conflict_report: must have at least 3 conflict records (got %d)" % len(conflicts))

    # Each record must have required fields
    required_fields = ("source_channel", "claimed_value", "official_value", "official_url")
    for i, c in enumerate(conflicts[:5]):
        for fld in required_fields:
            if not c.get(fld):
                fails.append("conflict_report entry[%d]: missing or empty field '%s'" % (i, fld))
                break

    # Meta Strike 7 conflict must be identified
    meta_s7_found = False
    for c in conflicts:
        topic = str(c.get("topic") or c.get("field") or c.get("id") or "").lower()
        claimed = str(c.get("claimed_value") or "").lower()
        official = str(c.get("official_value") or "").lower()
        if "meta" in topic and "strike" in topic and "7" in topic:
            meta_s7_found = True
            break
        if "meta" in str(c).lower() and "strike" in str(c).lower() and (
            "3" in claimed and "1" in official or "strike_7" in str(c).lower()
        ):
            meta_s7_found = True
            break
    if not meta_s7_found:
        fails.append("conflict_report: Meta Strike 7 conflict (3 days vs 1 day) not identified")

    # YouTube appeal window conflict must be identified
    yt_appeal_found = False
    for c in conflicts:
        blob = str(c).lower()
        if "youtube" in blob and "appeal" in blob and ("3" in blob or "6" in blob):
            yt_appeal_found = True
            break
    if not yt_appeal_found:
        fails.append("conflict_report: YouTube appeal window conflict (3 months bot vs 6 months official) not identified")

    # TikTok permanent ban conflict must be identified
    tt_ban_found = False
    for c in conflicts:
        blob = str(c).lower()
        if "tiktok" in blob and ("permanent" in blob or "ban" in blob) and (
            "two" in blob or "2" in blob or "three" in blob or "3" in blob
        ):
            tt_ban_found = True
            break
    if not tt_ban_found:
        fails.append("conflict_report: TikTok permanent ban threshold conflict (2 vs 3 strikes) not identified")

    _finish(fails)
main()
'''

# Q11: 跨轮数值闭合校验 (V4)
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    data, err = _load_json(pe / "reports" / "cross_validation.json")
    if err: _finish([err])

    yt = data.get("youtube") or {}
    meta = data.get("meta") or {}
    tt = data.get("tiktok") or {}

    # youtube.strike1_freeze_days must be 7 (from Q2 file)
    s1d = yt.get("strike1_freeze_days")
    try:
        if int(s1d) != 7:
            fails.append("cross_validation: youtube.strike1_freeze_days must be 7 (got %r)" % s1d)
    except (TypeError, ValueError):
        fails.append("cross_validation: youtube.strike1_freeze_days must be int 7 (got %r)" % s1d)

    # meta.strike9_ban_days must be 7 (from Q3 file)
    s9d = meta.get("strike9_ban_days")
    try:
        if int(s9d) != 7:
            fails.append("cross_validation: meta.strike9_ban_days must be 7 (got %r)" % s9d)
    except (TypeError, ValueError):
        fails.append("cross_validation: meta.strike9_ban_days must be int 7 (got %r)" % s9d)

    # tiktok.videos_removed_q1_2025 must be 211000000 (±1%)
    tvr = tt.get("videos_removed_q1_2025")
    try:
        tvr = int(tvr)
        if not (208890000 <= tvr <= 213110000):
            fails.append("cross_validation: tiktok.videos_removed_q1_2025 must be ~211000000 (±1%%), got %d" % tvr)
    except (TypeError, ValueError):
        fails.append("cross_validation: tiktok.videos_removed_q1_2025 must be numeric (got %r)" % tvr)

    # Cross-verify against actual source files (V4 closure)
    yt_src, yt_err = _load_json(pe / "platforms" / "youtube" / "strike_system.json")
    if not yt_err and yt_src:
        actual_s1 = (yt_src.get("strike1") or {}).get("freeze_days")
        try:
            if int(actual_s1) != int(s1d):
                fails.append("cross_validation drift: youtube.strike1_freeze_days %r != actual %r in strike_system.json" % (s1d, actual_s1))
        except (TypeError, ValueError):
            pass

    tt_src, tt_err = _load_json(pe / "platforms" / "tiktok" / "q1_2025_report.json")
    if not tt_err and tt_src:
        actual_vr = tt_src.get("videos_removed")
        try:
            if int(actual_vr) != int(tvr):
                fails.append("cross_validation drift: tiktok.videos_removed_q1_2025 %r != actual %r in q1_2025_report.json" % (tvr, actual_vr))
        except (TypeError, ValueError):
            pass

    _finish(fails)
main()
'''

# Q12: update_2 supersede — TikTok 案例回滚 (V2 + V10)
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []

    # appeal_tracker: T-001..T-007 must be pending (superseded)
    at, err = _load_json(pe / "internal" / "appeal_tracker.json")
    if err: _finish([err])
    cases = at.get("cases") or {}

    for cid in ("T-001", "T-002", "T-003", "T-004", "T-005", "T-006", "T-007"):
        c = cases.get(cid)
        if c is None:
            fails.append("appeal_tracker: TikTok case %s missing (must exist and be pending)" % cid)
        elif str(c.get("status", "")).lower() != "pending":
            fails.append("case %s: status must be 'pending' (superseded by Discord notice; got %r)" % (cid, c.get("status")))

    # YouTube cases Y-001..Y-006 must NOT be pending (V10: only TikTok subset superseded)
    for cid in ("Y-001", "Y-002", "Y-003", "Y-004", "Y-005", "Y-006"):
        c = cases.get(cid)
        if c is not None and str(c.get("status", "")).lower() == "pending":
            fails.append("case %s: YouTube case should NOT be reset to pending (only TikTok T-001..T-007 were superseded)" % cid)

    # q3_2025_report.json must exist with quarter field containing 'Q3_2025'
    q3, err2 = _load_json(pe / "platforms" / "tiktok" / "q3_2025_report.json")
    if err2: _finish([err2])
    q3_quarter = str(q3.get("quarter") or "")
    if "Q3_2025" not in q3_quarter and "Q3" not in q3_quarter:
        fails.append("q3_2025_report.json: quarter field must contain 'Q3_2025' (got %r)" % q3_quarter)

    _finish(fails)
main()
'''

# Q13: 违规案例数据集统计 (V3 + V8; P5 文件命名静默考察)
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []

    # Find the violation stats file — must follow P5 naming convention
    reports_dir = pe / "reports"
    # Accept: violation_stats_latest.json or violation_stats_YYYY-MM.json
    import re as _re
    candidates = list(reports_dir.glob("violation_stats*.json"))
    if not candidates:
        _finish(["reports/ dir missing violation_stats*.json file (must follow P5 naming: violation_stats_latest.json or violation_stats_YYYY-MM.json)"])

    # Also reject bare 'violation_stats.json' (P5 violation)
    bare = reports_dir / "violation_stats.json"
    if bare.exists() and not (reports_dir / "violation_stats_latest.json").exists():
        # Bare name without date/latest suffix
        has_good = any(f.name != "violation_stats.json" for f in candidates)
        if not has_good:
            fails.append("violation_stats.json: P5 violation — must use violation_stats_latest.json or violation_stats_YYYY-MM.json naming")

    # Use the best-named candidate
    good = [f for f in candidates if f.name != "violation_stats.json"]
    target = good[0] if good else candidates[0]

    data, err = _load_json(target)
    if err: _finish([err])

    # Must have platform data for all 4 platforms
    platforms = data.get("platforms") or data.get("by_platform") or {}
    if not isinstance(platforms, dict):
        # Try looking for platform keys at top level
        plat_keys = {"youtube", "meta", "tiktok", "reddit"}
        platforms = {k: v for k, v in data.items() if k in plat_keys}

    for plat in ("youtube", "meta", "tiktok", "reddit"):
        if plat not in platforms:
            fails.append("violation stats: missing '%s' platform data" % plat)

    # Each platform must have a total_count
    for plat, plat_data in platforms.items():
        if plat not in ("youtube", "meta", "tiktok", "reddit"):
            continue
        if isinstance(plat_data, dict):
            tc = plat_data.get("total_count") or plat_data.get("total") or plat_data.get("count")
            if tc is None:
                fails.append("violation stats: platform '%s' missing total_count field" % plat)

    _finish(fails)
main()
'''

# Q14: 内部执行 SOP 文档 (V3: P4 静默考察; V9)
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    txt = _read(pe / "internal" / "sop_enforcement.md")
    if txt is None:
        _finish(["file not found: policy_engine/internal/sop_enforcement.md"])

    # Must have 4 platform headings
    for plat in ("YouTube", "Meta", "TikTok", "Reddit"):
        if ("## " + plat) not in txt:
            fails.append("sop_enforcement.md: missing '## %s' heading" % plat)

    low = txt.lower()

    # YouTube appeal window: must mention 6 months for strikes
    if not re.search(r"6.{0,10}month|six.{0,10}month", low):
        fails.append("sop_enforcement.md: YouTube/Reddit appeal window of 6 months not stated")

    # Reddit appeal window: must mention 6 months
    # (combined check above is sufficient; check for Reddit section specifically)
    reddit_idx = low.find("## reddit")
    if reddit_idx >= 0:
        reddit_section = low[reddit_idx:]
        if not re.search(r"6.{0,10}month|six.{0,10}month", reddit_section):
            fails.append("sop_enforcement.md: Reddit section missing 6-month appeal window")

    # ## 来源参考 section must exist
    if not re.search(r"^## (来源参考|参考来源|references|sources)", txt, re.IGNORECASE | re.MULTILINE):
        fails.append("sop_enforcement.md: missing ## 来源参考 (References) section (P4 + requirement)")

    # At least 4 source URLs in the references section
    urls = re.findall(r"https?://\\S+", txt)
    if len(urls) < 4:
        fails.append("sop_enforcement.md: ## 来源参考 must contain at least 4 source URLs (found %d)" % len(urls))

    _finish(fails)
main()
'''

# Q15: update_3 EU DSA 监管合规 (V9 + V2 supersede: Reddit not affected)
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []
    data, err = _load_json(pe / "internal" / "regulatory_addendum.json")
    if err: _finish([err])

    # regulation = 'EU_DSA'
    reg = str(data.get("regulation") or "")
    if "EU_DSA" not in reg and "EU DSA" not in reg and "DSA" not in reg:
        fails.append("regulatory_addendum: regulation field must contain 'EU_DSA' (got %r)" % reg)

    # affected_platforms: must contain youtube, meta, tiktok
    affected = [str(p).lower() for p in (data.get("affected_platforms") or [])]
    for plat in ("youtube", "meta", "tiktok"):
        if plat not in affected:
            fails.append("regulatory_addendum: affected_platforms must include '%s'" % plat)

    # reddit must NOT be in affected_platforms (supersede: Reddit is not VLOP)
    if "reddit" in affected:
        fails.append("regulatory_addendum: reddit must NOT be in affected_platforms (final email confirms Reddit is not a VLOP; supersedes early draft)")

    # article_reference: must include 'Art. 34' and 'Art. 35' (V9 verbatim)
    articles = [str(a) for a in (data.get("article_reference") or [])]
    for art in ("Art. 34", "Art. 35"):
        if art not in articles:
            fails.append("regulatory_addendum: article_reference must contain verbatim '%s' (got %s)" % (art, articles))

    # non_affected_platforms: must contain reddit
    non_affected = [str(p).lower() for p in (data.get("non_affected_platforms") or [])]
    if "reddit" not in non_affected:
        fails.append("regulatory_addendum: non_affected_platforms must include 'reddit'")

    _finish(fails)
main()
'''

# Q16: 最终合规报告 + sha256 sign-off (V7)
CHECKS["check_q16"] = '''
import hashlib

def main():
    ws = Path(sys.argv[1])
    pe = ws / "policy_engine"
    fails = []

    # compliance_report_final.md must exist and have platform content
    report_path = pe / "reports" / "compliance_report_final.md"
    if not report_path.exists():
        _finish(["file not found: policy_engine/reports/compliance_report_final.md"])
    report_txt = report_path.read_text(encoding="utf-8")
    low = report_txt.lower()
    for plat in ("youtube", "meta", "tiktok", "reddit"):
        if plat not in low:
            fails.append("compliance_report_final.md: missing %s platform data" % plat)
    if not re.search(r"appeal.{0,30}window|appeal.{0,30}time|6.{0,20}month", low):
        fails.append("compliance_report_final.md: missing appeal window table/summary")
    if not re.search(r"conflict|discrepanc", low):
        fails.append("compliance_report_final.md: missing conflicts/discrepancy summary section")

    # compliance_signoff.json must exist with sha256 field matching actual file hash
    signoff_path = pe / "reports" / "compliance_signoff.json"
    signoff, err = _load_json(signoff_path)
    if err: _finish([err])

    sha_val = str(signoff.get("sha256") or "")
    if not re.fullmatch(r"[a-f0-9]{64}", sha_val):
        _finish(["compliance_signoff.json: sha256 field must be a 64-char lowercase hex digest (got %r)" % sha_val[:80]])

    # signed_file field must be present
    if not signoff.get("signed_file"):
        fails.append("compliance_signoff.json: missing 'signed_file' field")

    # Recompute sha256 and compare (V7)
    actual_digest = hashlib.sha256(report_path.read_bytes()).hexdigest()
    if sha_val != actual_digest:
        fails.append("compliance_signoff.json: sha256 mismatch — recorded %s... != recomputed %s..." % (sha_val[:12], actual_digest[:12]))

    _finish(fails)
main()
'''

# check_preferences.py — P1-P5 preference checker
PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prd2 preference checker (P1: JSON 2-space indent + snake_case / P2: _source_url companion /
P3: time limits in months 1 decimal / P4: [^N] footnote citations / P5: reports/ naming convention)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """JSON files must use 2-space indentation and snake_case keys (no camelCase)."""
    p = Path(ws) / target
    if not p.exists():
        return True, "P1: target missing, skip"
    if p.suffix not in (".json",):
        return True, "P1: non-JSON target, skip"
    txt = _read(p)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    # Check for camelCase keys (any key with a lowercase letter followed by uppercase)
    all_keys = _collect_keys(data)
    camel = [k for k in all_keys if re.search(r"[a-z][A-Z]", k)]
    if camel:
        return False, "P1: camelCase keys detected: %s (use snake_case)" % camel[:3]
    # Check indentation (2-space): re-serialize and compare
    canonical = json.dumps(data, ensure_ascii=False, indent=2) + "\\n"
    if txt.strip() != canonical.strip():
        # Allow minor whitespace differences but flag drastically different indent
        lines = [l for l in txt.splitlines() if l.startswith("  ") and not l.startswith("   ")]
        three_indent = [l for l in txt.splitlines() if l.startswith("   ") and not l.startswith("    ")]
        if three_indent:
            return False, "P1: JSON indentation appears to be 3+ spaces (should be 2-space)"
    return True, "P1: PASSED"


def _collect_keys(obj, depth=0):
    keys = []
    if depth > 5:
        return keys
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys.append(k)
            keys.extend(_collect_keys(v, depth + 1))
    elif isinstance(obj, list):
        for item in obj:
            keys.extend(_collect_keys(item, depth + 1))
    return keys


def check_P2(ws, target):
    """Numeric fields in JSON must have a companion _source_url field at the same level."""
    p = Path(ws) / target
    if not p.exists():
        return True, "P2: target missing, skip"
    if p.suffix not in (".json",):
        return True, "P2: non-JSON target, skip"
    txt = _read(p)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P2: target is not valid JSON"
    # Check that numeric fields have _source_url companions
    issues = _check_source_urls(data)
    if issues:
        return False, "P2: numeric fields without _source_url companions: %s" % issues[:3]
    return True, "P2: PASSED"


def _check_source_urls(obj, parent_key="", depth=0):
    """Return list of numeric field names lacking a _source_url sibling."""
    if depth > 6:
        return []
    issues = []
    if isinstance(obj, dict):
        keys = set(obj.keys())
        for k, v in obj.items():
            if k.endswith("_source_url") or k.endswith("_url") or k.startswith("_"):
                continue
            if isinstance(v, (int, float)) and v not in (0, 1) and k not in (
                "schema_version", "tier", "strikes_required", "automation_rate",
                "videos_removed_pct_of_uploads",
            ):
                companion = k + "_source_url"
                if companion not in keys:
                    issues.append("%s.%s (missing %s)" % (parent_key, k, companion))
            if isinstance(v, (dict, list)):
                issues.extend(_check_source_urls(v, parent_key + "." + k if parent_key else k, depth + 1))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            issues.extend(_check_source_urls(item, parent_key + "[%d]" % i, depth + 1))
    return issues


def check_P3(ws, target):
    """Time-limit values use months as primary unit, 1 decimal place."""
    p = Path(ws) / target
    if not p.exists():
        return True, "P3: target missing, skip"
    if p.suffix not in (".json",):
        return True, "P3: non-JSON target, skip"
    txt = _read(p)
    if txt is None:
        return True, "P3: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P3: target is not valid JSON"
    # Check month fields: must be float-like with 1 decimal (e.g. 6.0, 12.0, 3.0)
    issues = _check_month_fields(data)
    if issues:
        return False, "P3: month fields not using 1 decimal: %s" % issues[:3]
    return True, "P3: PASSED"


def _check_month_fields(obj, depth=0):
    if depth > 5:
        return []
    issues = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if "month" in k and "url" not in k:
                if isinstance(v, (int, float)):
                    # Must be representable as X.Y (1 decimal)
                    if isinstance(v, int) and v > 0:
                        issues.append("%s=%r (should be float e.g. %.1f)" % (k, v, float(v)))
            if isinstance(v, (dict, list)):
                issues.extend(_check_month_fields(v, depth + 1))
    elif isinstance(obj, list):
        for item in obj:
            issues.extend(_check_month_fields(item, depth + 1))
    return issues


def check_P4(ws, target):
    """Markdown documents must use [^N] footnote format and include ## 参考来源 section."""
    p = Path(ws) / target
    if not p.exists():
        return True, "P4: target missing, skip"
    if p.suffix not in (".md",):
        return True, "P4: non-Markdown target, skip"
    txt = _read(p)
    if txt is None:
        return True, "P4: target missing, skip"
    if "[^" not in txt:
        return False, "P4: missing [^N] footnote citations in Markdown document"
    if not re.search(r"^## (参考来源|references|来源参考|sources)", txt, re.IGNORECASE | re.MULTILINE):
        return False, "P4: missing ## 参考来源 / ## References section at document end"
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Files in reports/ must follow {type}_{yyyy-mm}.json or {type}_latest.json naming."""
    p = Path(ws) / target
    if p.is_file():
        files = [p]
    elif p.is_dir():
        files = list(p.glob("*.json"))
    else:
        return True, "P5: target missing, skip"
    pat_date = re.compile(r"^[a-z][a-z0-9_]*_\\d{4}-\\d{2}\\.json$")
    pat_latest = re.compile(r"^[a-z][a-z0-9_]*_latest\\.json$")
    bad = []
    for f in files:
        if f.name in ("cross_validation.json", "deprecation_log.json",
                      "compliance_signoff.json", "compliance_report_final.json"):
            continue
        if "violation_stats" in f.name or "compliance" in f.name:
            if not (pat_date.match(f.name) or pat_latest.match(f.name)):
                bad.append(f.name)
    if bad:
        return False, "P5: reports/ files not matching {type}_{yyyy-mm}.json or {type}_latest.json: %s" % bad
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="policy_engine/internal/")
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
