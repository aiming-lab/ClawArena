#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_prd3_checks.py — 生成 prd3 的全部 exec_check 校验脚本到 eval/prd3/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_prd3.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/prd3/scripts")
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

# Q1: 指标公式提取 (V9) — 加难 A: gmv_formula 须含 × 符号（非 *）；要求 source_url（非裸 source）
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "metric_glossary.json")
    if err: _finish([err])
    # 顶层须有 source_url（不接受裸 source 字段，须为权威 URL）
    if "source_url" not in data:
        fails.append("metric_glossary.json 缺少 source_url 字段（须为权威来源 URL，如 wallstreetprep.com；裸 source 字段不满足要求）")
    # gmv_formula 须含 transactions、AOV，且须使用 × 乘号（不接受 * 号）
    gmv_raw = str(data.get("gmv_formula") or "")
    gmv = gmv_raw.lower()
    if "transaction" not in gmv or "aov" not in gmv:
        fails.append("gmv_formula == %r (须包含 'transactions' 和 'AOV')" % gmv_raw)
    if "×" not in gmv_raw and "×" not in gmv_raw:
        fails.append("gmv_formula == %r (须使用 × 乘号（Unicode ×），公式须与 metric_definitions.md 中 verbatim 一致；不接受 * 号)" % gmv_raw)
    # inventory_days_multiplier 须为 360
    mult = data.get("inventory_days_multiplier")
    try:
        mult = int(mult)
    except (TypeError, ValueError):
        mult = None
    if mult != 360:
        fails.append("inventory_days_multiplier == %r (expected 360, JD 官方口径, 非 365)" % mult)
    # take_rate_formula 须含 commission 和 GMV（大小写不敏感）
    trf = str(data.get("take_rate_formula") or "").lower()
    if "commission" not in trf or "gmv" not in trf:
        fails.append("take_rate_formula == %r (须包含 'commission' 和 'GMV')" % data.get("take_rate_formula"))
    _finish(fails)
main()
'''

# Q2: 口径冲突清单 (V1)
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "conflicts.json")
    if err: _finish([err])
    cc = data.get("conflict_count")
    try:
        cc = int(cc)
    except (TypeError, ValueError):
        cc = 0
    if cc < 3:
        fails.append("conflict_count == %r (expected >= 3: 补贴口径 + 360/365分母 + GMV同比增速三条冲突)" % data.get("conflict_count"))
    conflicts = data.get("conflicts") or []
    if not isinstance(conflicts, list) or len(conflicts) < 3:
        fails.append("conflicts array 须含至少 3 条")
    # 检查是否含补贴冲突
    all_text = " ".join(str(c) for c in conflicts).lower()
    if not any(kw in all_text for kw in ("subsid", "补贴", "platform subsidy")):
        fails.append("conflicts 中未发现 GMV 补贴口径冲突（须含 subsid/补贴 关键词）")
    if not any(kw in all_text for kw in ("360", "365")):
        fails.append("conflicts 中未发现 360 vs 365 库存天数分母冲突")
    if not any(kw in all_text for kw in ("增速", "growth", "yoy", "同比", "22.5", "15.2")):
        fails.append("conflicts 中未发现 GMV 同比增速冲突（bot 摘要 22.5%% vs Daxue 权威 15.2%%）")
    # 每条须有 from 字段
    for i, c in enumerate(conflicts):
        if isinstance(c, dict) and not c.get("from"):
            fails.append("conflicts[%d] 缺少 'from' 字段（P2 要求标注 session 来源）" % i)
    _finish(fails)
main()
'''

# Q3: GMV v1 闭合校验 (V7) — 加难 A: 增加 delta_pct 须在 4%-8% 范围（脚本真实输出，不能随意填 0）
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "gmv_validation_v1.json")
    if err: _finish([err])
    status = data.get("status")
    if status != "FAIL":
        fails.append("status == %r (expected FAIL; v1 数据含 Method 1 口径污染，校验须返回 FAIL)" % status)
    # delta_pct 须在 4%-8% 范围（calc_gmv.py 真实输出；不得填 0 或占位值）
    dp = data.get("delta_pct")
    try:
        dp = float(dp)
        if not (4.0 <= dp <= 8.0):
            fails.append("delta_pct == %.2f (expected 4%%–8%% 范围；须实际运行 scripts/calc_gmv.py 获取真实差异，不得填 0 或估计值)" % dp)
    except (TypeError, ValueError):
        fails.append("delta_pct 须为数值（须实际运行 calc_gmv.py 脚本获得，取绝对差异百分比）")
    # affected_date_range 须存在且 start/end 在 2025-05-13 ~ 2025-05-22 范围
    adr = data.get("affected_date_range")
    if not isinstance(adr, dict):
        fails.append("affected_date_range 须为含 start/end 的对象（status=FAIL 时必须记录日期范围）")
    else:
        start = str(adr.get("start") or "")
        end = str(adr.get("end") or "")
        if not start.startswith("2025-05"):
            fails.append("affected_date_range.start == %r (expected 2025-05-xx)" % start)
        if not end.startswith("2025-05"):
            fails.append("affected_date_range.end == %r (expected 2025-05-xx)" % end)
    _finish(fails)
main()
'''

# Q4: Method 1 日期识别 (V1, V6)
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "data_quality_report.json")
    if err: _finish([err])
    dates = data.get("jd_method1_dates") or []
    if not isinstance(dates, list) or len(dates) < 3:
        fails.append("jd_method1_dates 须为含至少 3 个日期的列表（实际：%r）" % dates)
    else:
        # 须在 2025-05-13 ~ 2025-05-22 范围内
        valid = [d for d in dates if isinstance(d, str) and d.startswith("2025-05-")]
        if len(valid) < 3:
            fails.append("jd_method1_dates 中至少 3 个须为 2025-05-xx 格式（在 bug 日期范围内）")
    correct = str(data.get("correct_method") or "").lower()
    if "method 2" not in correct and "method2" not in correct:
        fails.append("correct_method == %r (expected 'Method 2')" % data.get("correct_method"))
    _finish(fails)
main()
'''

# Q5: 退货率分析 (V9, V8)
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "return_rate_analysis.json")
    if err: _finish([err])
    cats = data.get("categories") or []
    if not isinstance(cats, list) or len(cats) < 2:
        fails.append("categories 须为含至少 2 个品类的列表")
    found_apparel = found_electronics = False
    for cat in cats:
        if not isinstance(cat, dict):
            continue
        name = str(cat.get("category") or "").lower()
        rr = cat.get("return_rate_pct")
        try:
            rr = float(rr)
        except (TypeError, ValueError):
            fails.append("品类 %r return_rate_pct 不是数值" % name)
            continue
        if "apparel" in name or "服装" in name:
            found_apparel = True
            if not (20.0 <= rr <= 40.0):
                fails.append("apparel return_rate_pct == %.2f (expected 20-40%%)" % rr)
        if "electron" in name or "电子" in name:
            found_electronics = True
            if not (8.0 <= rr <= 15.0):
                fails.append("electronics return_rate_pct == %.2f (expected 8-15%%, 修订前基准)" % rr)
        # flagged 字段须为 bool
        flagged = cat.get("flagged")
        if flagged is not None and not isinstance(flagged, bool):
            fails.append("品类 %r flagged 须为 bool 类型（不得仅用文字说明）" % name)
    if not found_apparel:
        fails.append("categories 中未找到 apparel 品类")
    if not found_electronics:
        fails.append("categories 中未找到 electronics 品类")
    _finish(fails)
main()
'''

# Q6: 库存天数（JD 口径）(V4, V9)
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "inventory_days_618.json")
    if err: _finish([err])
    # formula_used 须含 360 和 5 quarters
    fu = str(data.get("formula_used") or "").lower()
    if "360" not in fu:
        fails.append("formula_used 未包含 '360': %r" % data.get("formula_used"))
    if "5 quarter" not in fu and "five quarter" not in fu and "5q" not in fu:
        fails.append("formula_used 未包含 '5 quarters': %r" % data.get("formula_used"))
    # inventory_days 须为 LinkMart 618 实算值 32.4（avg_5q/ttm_cogs×360），排除 JD 历史诱饵 31.5
    inv = data.get("inventory_days")
    try:
        inv = float(inv)
    except (TypeError, ValueError):
        _finish(["inventory_days 不是数值: %r" % data.get("inventory_days")])
    if not (32.0 <= inv <= 32.8):
        fails.append("inventory_days == %.1f (expected 32.4 = LinkMart 618 实算值 avg_5q/ttm_cogs×360; 勿用 JD Q4 2024 历史诱饵 31.5)" % inv)
    # multiplier 须为 360
    mult = data.get("multiplier")
    try:
        mult = int(mult)
    except (TypeError, ValueError):
        mult = None
    if mult != 360:
        fails.append("multiplier == %r (expected 360)" % mult)
    _finish(fails)
main()
'''

# Q7: 蜜罐识别 (V5)
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "honeypot_flags.json")
    if err: _finish([err])
    if data.get("honeypot_identified") is not True:
        fails.append("honeypot_identified == %r (expected true)" % data.get("honeypot_identified"))
    # wrong_metric 须识别为 gmv_growth_rate（失真字段）
    wm = str(data.get("wrong_metric") or "").lower()
    if "growth" not in wm and "gmv" not in wm:
        fails.append("wrong_metric == %r (expected 'gmv_growth_rate' 或类似)" % data.get("wrong_metric"))
    # correct_value_source 须指向 data/reference 或 industry_benchmarks
    cvs = str(data.get("correct_value_source") or "").lower()
    if "industry_benchmark" not in cvs and "reference" not in cvs and "daxue" not in cvs:
        fails.append("correct_value_source == %r (expected 指向 industry_benchmarks.json 或 Daxue 来源)" % data.get("correct_value_source"))
    _finish(fails)
main()
'''

# Q8: 平台份额 v1 (V9, V8) — 加难 A+D: 要求 douyin_share_pct / kuaishou_share_pct 单独列出（不能仅 content_platforms 合并）
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "platform_gmv_share.json")
    if err: _finish([err])
    def _pct(key, lo, hi):
        v = data.get(key)
        try:
            v = float(v)
        except (TypeError, ValueError):
            fails.append("%s 不是数值: %r" % (key, v)); return
        if not (lo <= v <= hi):
            fails.append("%s == %.2f (expected %.1f-%.1f%%)" % (key, v, lo, hi))
    _pct("tmall_share_pct", 45.0, 56.0)
    _pct("jd_share_pct", 15.0, 25.0)
    _pct("content_platforms_share_pct", 20.0, 40.0)
    # 加难：Douyin 和 Kuaishou 须单独列出占比字段（Update 2 supersede 的前置要求，内容平台须可拆分）
    douyin = data.get("douyin_share_pct")
    if douyin is None:
        fails.append("缺少 douyin_share_pct 字段（须单独列出 Douyin 平台份额；仅列合并的 content_platforms_share_pct 不满足要求——Update 2 后 Douyin 须独立追踪）")
    kuaishou = data.get("kuaishou_share_pct")
    if kuaishou is None:
        fails.append("缺少 kuaishou_share_pct 字段（须单独列出快手平台份额；与 Douyin 分开列报以满足审计追踪要求）")
    dv = str(data.get("data_version") or "")
    if dv != "v1":
        fails.append("data_version == %r (expected 'v1' 此阶段使用 v1 数据)" % dv)
    _finish(fails)
main()
'''

# Q9: GMV v2 修正 (V2) — 加难 A+B: reason 须包含 pm_correction_note.md 文件名引用（来源文件须明确标注）
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "gmv_revision_v2.json")
    if err: _finish([err])
    v1 = data.get("v1_total_gmv")
    v2 = data.get("v2_total_gmv")
    try:
        v1 = float(v1); v2 = float(v2)
    except (TypeError, ValueError):
        _finish(["v1_total_gmv / v2_total_gmv 须为数值"])
    # delta_pct 须在 -5% 到 -8% 范围（v2 比 v1 低 5-8%）
    dp = data.get("delta_pct")
    try:
        dp = float(dp)
    except (TypeError, ValueError):
        fails.append("delta_pct 不是数值: %r" % data.get("delta_pct"))
        dp = None
    if dp is not None:
        if not (-8.0 <= dp <= -5.0):
            fails.append("delta_pct == %.2f (expected -5%% to -8%%, v2 须比 v1 低 5-8%%)" % dp)
    # reason 须含 Method 2 和 subsidy excluded
    reason = str(data.get("reason") or "").lower()
    if "method 2" not in reason and "method2" not in reason:
        fails.append("reason 未包含 'Method 2': %r" % data.get("reason"))
    if "subsidy" not in reason:
        fails.append("reason 未包含 'subsidy excluded': %r" % data.get("reason"))
    # 加难：reason 须引用 pm_correction_note.md 作为口径修正依据（Update 1 注入的说明文件）
    if "pm_correction_note" not in reason:
        fails.append("reason 未引用 'pm_correction_note.md'（Update 1 的 PM 修正说明文件，须在 reason 中明确引用该文件名作为修正依据）: %r" % data.get("reason"))
    _finish(fails)
main()
'''

# Q10: 转化漏斗 (V4, V8)
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "conversion_funnel_v2.json")
    if err: _finish([err])
    def _pct(key, lo, hi, dp=2):
        v = data.get(key)
        try:
            v = float(v)
        except (TypeError, ValueError):
            fails.append("%s 不是数值: %r" % (key, v)); return None
        if not (lo <= v <= hi):
            fails.append("%s == %.{0}f (expected %.1f-%.1f)".format(dp) % (key, v, lo, hi))
        return v
    _pct("overall_conversion_rate", 1.5, 5.0)
    _pct("add_to_cart_rate", 5.0, 10.0)
    _pct("cart_to_checkout_rate", 55.0, 75.0)
    # 每个字段须有 calculation 字段
    for key in ("overall_conversion_rate", "add_to_cart_rate", "cart_to_checkout_rate"):
        calc_key = key + "_calculation" if key + "_calculation" in data else None
        # 也接受嵌套对象形式
        v = data.get(key)
        if isinstance(v, dict) and not v.get("calculation"):
            fails.append("嵌套对象 %s 须含 calculation 字段" % key)
    _finish(fails)
main()
'''

# Q11: KPI Dashboard 跨轮闭合 (V4, V8)
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "kpi_dashboard.json")
    if err: _finish([err])
    # data_version 须为 v2
    dv = str(data.get("data_version") or "")
    if dv != "v2":
        fails.append("data_version == %r (expected 'v2')" % dv)
    # inventory_days 须与 Q6 完全一致（cross-round drift = fail）
    q6, e6 = _load_json(ws / "output" / "inventory_days_618.json")
    if not e6 and q6 is not None:
        q6_inv = q6.get("inventory_days")
        q11_inv = data.get("inventory_days")
        try:
            q6_inv = float(q6_inv); q11_inv = float(q11_inv)
            if abs(q6_inv - q11_inv) > 0.05:
                fails.append("inventory_days drift: Q11=%s != Q6=%s (须完全一致)" % (q11_inv, q6_inv))
        except (TypeError, ValueError):
            fails.append("inventory_days 须为数值")
    # gmv_total 须与 Q9 v2_total_gmv 一致（±1% 容差）
    q9, e9 = _load_json(ws / "output" / "gmv_revision_v2.json")
    if not e9 and q9 is not None:
        q9_gmv = q9.get("v2_total_gmv")
        q11_gmv = data.get("gmv_total")
        try:
            q9_gmv = float(q9_gmv); q11_gmv = float(q11_gmv)
            if abs(q9_gmv - q11_gmv) / max(q9_gmv, 1) > 0.01:
                fails.append("gmv_total drift: Q11=%s != Q9 v2=%s (须一致，容差 1%%)" % (q11_gmv, q9_gmv))
        except (TypeError, ValueError):
            fails.append("gmv_total 须为数值")
    # return_rate_overall 须在合理区间
    rr = data.get("return_rate_overall")
    try:
        rr = float(rr)
        if not (5.0 <= rr <= 30.0):
            fails.append("return_rate_overall == %.2f (expected 5-30%%)" % rr)
    except (TypeError, ValueError):
        fails.append("return_rate_overall 须为数值")
    _finish(fails)
main()
'''

# Q12: Supersede 辨别 (V10, V2) — 加难 A: superseded_rule 须同时包含 finance_audit_memo（撤销来源）
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "platform_gmv_share_v3.json")
    if err: _finish([err])
    # douyin_gmv 须为独立字段（数值 > 0）
    dg = data.get("douyin_gmv")
    try:
        dg = float(dg)
        if dg <= 0:
            fails.append("douyin_gmv == %s (expected > 0, 独立字段)" % dg)
    except (TypeError, ValueError):
        fails.append("douyin_gmv 须为数值（独立字段，非 content_platforms 合计的一部分）")
    # superseded_rule 须包含 pm_correction_note.md 和 channel_aggregation
    sr = str(data.get("superseded_rule") or "").lower()
    if "pm_correction_note" not in sr:
        fails.append("superseded_rule 须包含 'pm_correction_note.md': %r" % data.get("superseded_rule"))
    if "channel_aggregation" not in sr and "channel" not in sr:
        fails.append("superseded_rule 须包含 'channel_aggregation': %r" % data.get("superseded_rule"))
    # 加难：superseded_rule 须同时标注 finance_audit_memo.md（Update 2 中实际发出撤销指令的文件）
    if "finance_audit_memo" not in sr:
        fails.append("superseded_rule 须包含 'finance_audit_memo.md'（Update 2 的财务审计备忘录，该文件才是发出 supersede 指令的权威来源；仅标注 pm_correction_note.md 不完整）: %r" % data.get("superseded_rule"))
    # data_version 须为 v2
    dv = str(data.get("data_version") or "")
    if dv != "v2":
        fails.append("data_version == %r (expected 'v2')" % dv)
    _finish(fails)
main()
'''

# Q13: 红鲱鱼标记 (V6, V9)
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "legacy_report_flags.json")
    if err: _finish([err])
    if data.get("is_legacy") is not True:
        fails.append("is_legacy == %r (expected true)" % data.get("is_legacy"))
    # wrong_formula 须含 365（旧版错误乘数）
    wf = str(data.get("wrong_formula") or "").lower()
    if "365" not in wf:
        fails.append("wrong_formula 须包含 '365'（旧版 ×365 错误公式）: %r" % data.get("wrong_formula"))
    # correct_formula 须含 360 和 5 quarters
    cf = str(data.get("correct_formula") or "").lower()
    if "360" not in cf:
        fails.append("correct_formula 须包含 '360'（JD 官方乘数）: %r" % data.get("correct_formula"))
    if "5 quarter" not in cf and "five quarter" not in cf and "5q" not in cf:
        fails.append("correct_formula 须包含 '5 quarters': %r" % data.get("correct_formula"))
    _finish(fails)
main()
'''

# Q14: 修订退货率基准 (V2, V3)
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "return_rate_analysis_v2.json")
    if err: _finish([err])
    # electronics_benchmark_source 须为 China platform (revised)
    ebs = str(data.get("electronics_benchmark_source") or "").lower()
    if "china" not in ebs and "revised" not in ebs:
        fails.append("electronics_benchmark_source == %r (expected 'China platform (revised)')" % data.get("electronics_benchmark_source"))
    # electronics_upper_bound 须为 25（修订后基准）
    eub = data.get("electronics_upper_bound")
    try:
        eub = float(eub)
        if abs(eub - 25.0) > 0.5:
            fails.append("electronics_upper_bound == %s (expected 25, 修订后中国平台基准，非原 15)" % eub)
    except (TypeError, ValueError):
        fails.append("electronics_upper_bound 须为数值（25）")
    # 须有 flagged 字段在某品类中
    cats = data.get("categories") or []
    has_flagged = any(isinstance(c, dict) and "flagged" in c for c in cats)
    if not has_flagged and not data.get("flagged"):
        fails.append("须有 flagged: true 字段标记异常品类（P3 要求）")
    _finish(fails)
main()
'''

# Q15: 最终报告 (V9, V3)
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "final_report_draft.md")
    if txt is None:
        _finish(["file not found: output/final_report_draft.md"])
    low = txt.lower()
    lines = txt.splitlines()
    if len(lines) < 100:
        fails.append("final_report_draft.md 仅 %d 行（需 > 100 行）" % len(lines))
    if "gmv = transactions" not in low and "gmv=transactions" not in low:
        fails.append("须包含字符串 'GMV = transactions × AOV'（verbatim 引用）")
    if "360" not in txt:
        fails.append("须包含 '×360' 或 '× 360'（JD 库存天数口径）")
    if "method 2" not in low and "method2" not in low:
        fails.append("须包含 'Method 2'（GMV 口径说明）")
    if "data_version" not in low or "v2" not in low:
        fails.append("须包含 'data_version: v2' 或类似字样")
    _finish(fails)
main()
'''

# Q16: 闭合验证表 (V4)
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "closure_check.json")
    if err: _finish([err])
    # inventory_days_matches_q6 须为 true
    imq6 = data.get("inventory_days_matches_q6")
    if imq6 is not True:
        fails.append("inventory_days_matches_q6 == %r (expected true; Q6 和 Q11 库存天数须一致)" % imq6)
    # gmv_version_matches_q9 须为 true
    gmq9 = data.get("gmv_version_matches_q9")
    if gmq9 is not True:
        fails.append("gmv_version_matches_q9 == %r (expected true; Q9 和 Q11 GMV 总量须一致)" % gmq9)
    # all_consistent 须为 true（或至少 bool 类型）
    ac = data.get("all_consistent")
    if ac is not True and not (isinstance(ac, list) and len(ac) == 0):
        # 如果是 False 或非空列表，视为存在不一致
        if ac is False:
            fails.append("all_consistent == false (须解决不一致问题)")
    # 验证 Q6 和 Q11 实际闭合
    q6, e6 = _load_json(ws / "output" / "inventory_days_618.json")
    q11, e11 = _load_json(ws / "output" / "kpi_dashboard.json")
    if not e6 and not e11 and q6 and q11:
        try:
            q6_inv = float(q6.get("inventory_days"))
            q11_inv = float(q11.get("inventory_days"))
            if abs(q6_inv - q11_inv) > 0.05:
                fails.append("实际 inventory_days 不一致: Q6=%s != Q11=%s" % (q6_inv, q11_inv))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
'''

# Q17: SHA-256 验证 token (V7)
CHECKS["check_q17"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    token_path = ws / "output" / "verification_token.txt"
    if not token_path.exists():
        _finish(["file not found: output/verification_token.txt"])
    line = token_path.read_text(encoding="utf-8").strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["verification_token.txt 须为 VERIFIED:[a-f0-9]{64} 格式（实际: %r）" % line[:80]])
    kpi_path = ws / "output" / "kpi_dashboard.json"
    if not kpi_path.exists():
        _finish(["无法验证哈希：output/kpi_dashboard.json 不存在"])
    digest = hashlib.sha256(kpi_path.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("SHA-256 不匹配: token=%s... != 实算=%s..." % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

# Q18: 提交清单 (V8, V4)
CHECKS["check_q18"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "submission_manifest.json")
    if err: _finish([err])
    # total_files >= 12
    tf = data.get("total_files")
    try:
        tf = int(tf)
        if tf < 12:
            fails.append("total_files == %d (expected >= 12)" % tf)
    except (TypeError, ValueError):
        fails.append("total_files 须为整数")
    # files 数组每条须含 path/schema_valid/data_version
    files = data.get("files") or []
    if not isinstance(files, list) or len(files) < 12:
        fails.append("files 数组须含至少 12 条（实际: %d）" % len(files))
    for i, f in enumerate(files[:5]):  # 检查前 5 条
        if not isinstance(f, dict):
            continue
        for key in ("path", "schema_valid", "data_version"):
            if key not in f:
                fails.append("files[%d] 缺少字段 '%s'" % (i, key))
        if f.get("schema_valid") is not True:
            fails.append("files[%d].schema_valid == %r (expected true)" % (i, f.get("schema_valid")))
    # verification_token 须与 output/verification_token.txt 一致
    vt_file = ws / "output" / "verification_token.txt"
    if vt_file.exists():
        expected_vt = vt_file.read_text(encoding="utf-8").strip()
        manifest_vt = str(data.get("verification_token") or "").strip()
        if manifest_vt != expected_vt:
            fails.append("verification_token 与 output/verification_token.txt 不一致")
    # generated_at 须存在（ISO 8601）
    ga = data.get("generated_at")
    if not ga:
        fails.append("generated_at 字段缺失（P1 要求 ISO 8601 时间戳）")
    _finish(fails)
main()
'''

# ── Preference checker ─────────────────────────────────────────────────────
PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prd3 preference checker (P1 source_url+generated_at / P2 from-field / P3 flagged:true /
P4 decimal precision / P5 report sections)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Every JSON output must have source_url (or source) AND generated_at."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P1: top-level must be a JSON object"
    has_source = ("source_url" in data or "source" in data)
    has_ts = ("generated_at" in data)
    if not has_source:
        return False, "P1: missing source_url (or source) field"
    if not has_ts:
        return False, "P1: missing generated_at ISO 8601 timestamp field"
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Conflicts/anomaly items must have 'from' field."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P2: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P2: not an object, skip"
    # Check conflicts array
    conflicts = data.get("conflicts") or data.get("categories") or []
    if isinstance(conflicts, list):
        for i, item in enumerate(conflicts):
            if isinstance(item, dict) and "conflict" in str(item).lower():
                if not item.get("from"):
                    return False, "P2: conflicts[%d] missing 'from' field (session source required)" % i
    # Also check top-level from
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Anomalous categories must use flagged: true, not just text."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P3: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P3: not an object, skip"
    cats = data.get("categories") or []
    if not isinstance(cats, list):
        return True, "P3: no categories array, skip"
    for i, cat in enumerate(cats):
        if not isinstance(cat, dict):
            continue
        # If flagged key present, it must be bool
        flagged = cat.get("flagged")
        if flagged is not None and not isinstance(flagged, bool):
            return False, "P3: categories[%d].flagged == %r (must be bool true/false)" % (i, flagged)
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Numeric precision: inventory-level 1dp, percentages 2dp."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P4: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P4: not an object, skip"
    # Check inventory_days precision (should be 1dp)
    inv = data.get("inventory_days")
    if inv is not None:
        try:
            inv_f = float(inv)
            # Accept if it's naturally 1dp (e.g. 32.4 or 32.0)
            inv_str = str(inv)
            if "." in inv_str and len(inv_str.split(".")[1]) > 1:
                return False, "P4: inventory_days = %s (should be 1 decimal place, e.g. 32.4)" % inv_str
        except (TypeError, ValueError):
            pass
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Final Markdown must contain three H2 sections."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    required = ["## 数据来源", "## 口径说明", "## 异常标记"]
    missing = [s for s in required if s not in txt]
    if missing:
        return False, "P5: final report missing H2 sections: %s" % missing
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
        (OUT / f"{name}.py").write_text(HEADER + "\n" + body.strip() + "\n", encoding="utf-8")
    (OUT / "check_preferences.py").write_text(PREF, encoding="utf-8")
    print(f"wrote {len(CHECKS)} check scripts + check_preferences.py to {OUT}")


if __name__ == "__main__":
    main()
