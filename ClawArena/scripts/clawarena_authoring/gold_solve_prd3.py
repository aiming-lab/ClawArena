#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_prd3.py — prd3 可解性审计（金标自检）。

在 workspace 的临时副本上模拟 update 生效后的状态，写出每一轮的「正确产物」，
然后运行全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再做 4 个反例（错误产物），断言 check 能 FAIL（不过松）。

运行：python scripts/clawarena_authoring/gold_solve_prd3.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "prd3"
UPD = DS / "openclaw" / "updates" / "prd3"
SCRIPTS = DS / "eval" / "prd3" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/prd3_gold_ws")

NOW_ISO = "2026-03-16T12:00:00Z"


def _wj(p: Path, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _w(p: Path, t: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def prep_workspace() -> Path:
    """复制 workspace 并应用 update 文件。"""
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)

    # 应用 Update 1 workspace 文件
    upd1 = UPD / "upd1_workspace"
    for fname, target in [
        ("pm_correction_note.md", "data/updates/pm_correction_note.md"),
        ("gmv_daily_618_v2.csv", "data/raw/gmv_daily_618_v2.csv"),
        ("v1_v2_reconciliation_detail.csv", "data/processed/v1_v2_reconciliation_detail.csv"),
        ("update_slack_thread.md", "data/updates/update_slack_thread.md"),
    ]:
        src = upd1 / fname
        dst = GOLD / target
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)

    # 应用 Update 2 workspace 文件
    upd2 = UPD / "upd2_workspace"
    for fname, target in [
        ("finance_audit_memo.md", "data/updates/finance_audit_memo.md"),
        ("revised_category_benchmarks.json", "data/reference/revised_category_benchmarks.json"),
        ("legacy_report_v0.md", "data/processed/legacy_report_v0.md"),
        ("channel_reconciliation_detailed.md", "data/updates/channel_reconciliation_detailed.md"),
    ]:
        src = upd2 / fname
        dst = GOLD / target
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)

    return GOLD


def read_gmv_v1_totals(ws: Path) -> dict:
    """读取 v1 GMV CSV 计算总量和 Method 1 日期。"""
    path = ws / "data" / "raw" / "gmv_daily_618_v1.csv"
    total = 0.0
    method1_dates = set()
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                total += float(row["gmv_rmb_million"])
                if row.get("gmv_method") == "method1":
                    method1_dates.add(row["date"])
            except (ValueError, KeyError):
                pass
    return {"total": round(total, 2), "method1_dates": sorted(method1_dates)}


def read_gmv_v2_totals(ws: Path) -> dict:
    """读取 v2 GMV CSV 计算总量和渠道份额。"""
    path = ws / "data" / "raw" / "gmv_daily_618_v2.csv"
    total = 0.0
    channel_totals: dict[str, float] = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                gmv = float(row["gmv_rmb_million"])
                total += gmv
                chan = row.get("channel", "")
                channel_totals[chan] = channel_totals.get(chan, 0.0) + gmv
            except (ValueError, KeyError):
                pass
    # 计算份额
    tmall_share = round(100.0 * channel_totals.get("tmall", 0) / max(total, 1), 2)
    jd_share = round(100.0 * channel_totals.get("jd", 0) / max(total, 1), 2)
    douyin_share = round(100.0 * channel_totals.get("douyin", 0) / max(total, 1), 2)
    kuaishou_share = round(100.0 * channel_totals.get("kuaishou", 0) / max(total, 1), 2)
    content_share = round(douyin_share + kuaishou_share, 2)
    return {
        "total": round(total, 2),
        "by_channel": channel_totals,
        "tmall_share": tmall_share,
        "jd_share": jd_share,
        "douyin_share": douyin_share,
        "kuaishou_share": kuaishou_share,
        "content_platforms_share": content_share,
    }


def read_traffic_totals(ws: Path) -> dict:
    """读取流量数据计算转化率。"""
    path = ws / "data" / "raw" / "channel_traffic_metrics.csv"
    total_sessions = 0
    total_atc = 0
    total_checkouts = 0
    total_orders = 0
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                total_sessions += int(row["sessions"])
                total_atc += int(row["add_to_cart"])
                total_checkouts += int(row["checkouts"])
                total_orders += int(row["orders"])
            except (ValueError, KeyError):
                pass
    conv = round(100.0 * total_orders / max(total_sessions, 1), 2)
    atc_rate = round(100.0 * total_atc / max(total_sessions, 1), 2)
    ctc_rate = round(100.0 * total_checkouts / max(total_atc, 1), 2)
    return {
        "overall_conversion_rate": conv,
        "add_to_cart_rate": atc_rate,
        "cart_to_checkout_rate": ctc_rate,
    }


def read_returns(ws: Path) -> dict:
    """读取退货记录计算品类退货率。"""
    path = ws / "data" / "raw" / "returns_log_618.csv"
    # 订单数从 returns_log 的隐含订单数（使用预设值）
    cat_returns: dict[str, int] = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            cat = row.get("category", "")
            cat_returns[cat] = cat_returns.get(cat, 0) + 1
    # 品类订单数（与 gen_returns_log 中一致）
    cat_orders = {
        "apparel": 1200, "electronics": 1000, "beauty": 800, "home": 600, "food": 500
    }
    results = {}
    for cat in cat_orders:
        orders = cat_orders[cat]
        returns = cat_returns.get(cat, 0)
        results[cat] = round(100.0 * returns / max(orders, 1), 2)
    total_returns = sum(cat_returns.values())
    total_orders = sum(cat_orders.values())
    overall = round(100.0 * total_returns / max(total_orders, 1), 2)
    return {"by_cat": results, "overall": overall}


def read_inventory_calc(ws: Path) -> dict:
    """读取库存周转计算表。"""
    path = ws / "data" / "processed" / "inventory_turnover_calc.csv"
    data = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.reader(fh):
            if len(row) >= 2 and row[0] != "quarter":
                data[row[0]] = row[1]
    avg_inv = float(data.get("avg_5q", "960"))
    ttm_cogs = float(data.get("ttm_cogs", "10666"))
    inv_days = round(avg_inv / ttm_cogs * 360, 1)
    return {
        "inventory_days": inv_days,
        "avg_inventory_5q": avg_inv,
        "ttm_cogs": ttm_cogs,
        "multiplier": 360,
    }


def solve(ws: Path) -> dict:
    """生成全部 18 轮正确产物。返回关键数值供反例测试。"""
    out = ws / "output"
    out.mkdir(exist_ok=True)

    # 读取 source 数据
    v1 = read_gmv_v1_totals(ws)
    v2 = read_gmv_v2_totals(ws)
    traffic = read_traffic_totals(ws)
    returns = read_returns(ws)
    inv = read_inventory_calc(ws)

    delta_pct = round(100.0 * (v2["total"] - v1["total"]) / max(v1["total"], 1), 2)

    # Q1: 指标公式（V9 verbatim）
    _wj(out / "metric_glossary.json", {
        "source_url": "https://www.wallstreetprep.com/knowledge/gross-merchandise-value-gmv/",
        "generated_at": NOW_ISO,
        "gmv_formula": "GMV = transactions × AOV",
        "inventory_days_multiplier": 360,
        "take_rate_formula": "Take Rate (%) = commission / GMV",
        "inventory_days_formula_jd": "(avg_inventory_5q / ttm_cogs) × 360",
        "return_rate_formula": "Return Rate = (returns / orders) × 100",
    })

    # Q2: 冲突清单（V1）—— 金标更新：须包含 3 条冲突（新增 GMV 增速冲突）
    _wj(out / "conflicts.json", {
        "source_url": "https://www.speedwellmemos.com/p/accounting-insights-alibaba-jd-and",
        "generated_at": NOW_ISO,
        "conflict_count": 3,
        "conflicts": [
            {
                "from": "slack_data_team",
                "topic": "GMV 是否含平台补贴",
                "description": "Slack #data-team 中 chen_hao 指出 v1 数据将平台补贴计入 GMV（subsidy included），但 Method 2 口径要求排除（subsidy excluded）。v1 数据在 5/13-5/22 期间存在此问题。",
                "resolution": "使用 Method 2 口径（v2 数据），排除 platform subsidy"
            },
            {
                "from": "slack_data_team",
                "topic": "库存天数分母 360 vs 365",
                "description": "Slack 讨论中提及初稿报告使用 ×365（通用公式），但 LinkMart 采用 JD 官方口径 ×360（5 季度平均库存）。两者计算结果相差约 1.4%。",
                "resolution": "统一使用 JD 官方口径 ×360，5 季度平均"
            },
            {
                "from": "email_bot_summary",
                "topic": "GMV 同比增速（YoY Growth Rate）",
                "description": "data/processed/email_bot_summary_618.md 自动摘要声称 618 GMV 同比增速为 22.5%（基于历史趋势外推），而 data/reference/industry_benchmarks.json 引用 Daxue Consulting 权威数据显示真实值为 15.2%。差距约 7.3 个百分点。",
                "wrong_value": 22.5,
                "correct_value": 15.2,
                "correct_value_source": "data/reference/industry_benchmarks.json (Daxue Consulting 618 2025)",
                "resolution": "使用 industry_benchmarks.json 中的 15.2%（Daxue Consulting）作为权威值"
            }
        ]
    })

    # Q3: GMV v1 校验（V7 bash run）
    method1_dates = v1["method1_dates"]
    _wj(out / "gmv_validation_v1.json", {
        "status": "FAIL",
        "delta_pct": 5.5,
        "method1_row_count": len(method1_dates) * 5 * 4,  # dates × cats × channels
        "affected_date_range": {
            "start": method1_dates[0] if method1_dates else "2025-05-13",
            "end": method1_dates[-1] if method1_dates else "2025-05-22"
        },
        "reason": "v1 数据在 2025-05-13 至 2025-05-22 期间使用了 Method 1 口径（gmv_method='method1'），导致 GMV 虚高约 5.5%。"
    })

    # Q4: Method 1 日期识别（V1, V6）
    _wj(out / "data_quality_report.json", {
        "source_url": "https://www.speedwellmemos.com/p/accounting-insights-alibaba-jd-and",
        "generated_at": NOW_ISO,
        "jd_method1_dates": method1_dates[:10],
        "correct_method": "Method 2",
        "bug_description": "v1 CSV 中 gmv_method='method1' 的行集中在 2025-05-13 至 2025-05-22"
    })

    # Q5: 退货率分析（V9, V8）- 使用 Update 2 前的 NRF 基准
    cats_rr = []
    benchmarks = {
        "apparel": (20.0, 40.0),
        "electronics": (8.0, 15.0),
        "beauty": (4.0, 12.0),
        "home": (15.0, 23.0),
        "food": (1.0, 5.0),
    }
    for cat, (lo, hi) in benchmarks.items():
        rr = returns["by_cat"].get(cat, 0)
        cats_rr.append({
            "category": cat,
            "return_rate_pct": rr,
            "benchmark_low": lo,
            "benchmark_high": hi,
            "flagged": rr > hi or rr < lo,
            "from": "data/raw/returns_log_618.csv"
        })
    _wj(out / "return_rate_analysis.json", {
        "source_url": "https://nrf.com/research/2025-retail-returns-landscape",
        "generated_at": NOW_ISO,
        "benchmark_version": "NRF 2025 + Richpanel global",
        "categories": cats_rr
    })

    # Q6: 库存天数（V4, V9）
    _wj(out / "inventory_days_618.json", {
        "source_url": "https://www.globenewswire.com/news-release/2025/03/06/3037984/0/en/JD-com-Announces-Fourth-Quarter-and-Full-Year-2024-Results-and-Annual-Dividend.html",
        "generated_at": NOW_ISO,
        "formula_used": "(avg_inventory_5q / ttm_cogs) × 360 (5 quarters average, JD official)",
        "inventory_days": inv["inventory_days"],
        "multiplier": 360,
        "avg_inventory_5q": inv["avg_inventory_5q"],
        "ttm_cogs": inv["ttm_cogs"],
        "jd_reference_q4_2024": 31.5
    })
    saved_inv_days = inv["inventory_days"]

    # Q7: 蜜罐识别（V5）
    _wj(out / "honeypot_flags.json", {
        "source_url": "https://daxueconsulting.com/618-2025-results/",
        "generated_at": NOW_ISO,
        "honeypot_identified": True,
        "wrong_metric": "gmv_growth_rate",
        "wrong_value": 22.5,
        "correct_value": 15.2,
        "correct_value_source": "data/reference/industry_benchmarks.json",
        "from": "finance_wang_email",
        "note": "Bot summary 声称 YoY growth = 22.5%，实际 Daxue Consulting / Syntun 618 2025 = 15.2%"
    })

    # Q8: 平台份额 v1（V9, V8）— 金标更新：新增 douyin_share_pct / kuaishou_share_pct 单独字段
    v1_by_chan: dict[str, float] = {}
    with (ws / "data" / "raw" / "gmv_daily_618_v1.csv").open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                chan = row.get("channel", "")
                v1_by_chan[chan] = v1_by_chan.get(chan, 0.0) + float(row["gmv_rmb_million"])
            except (ValueError, KeyError):
                pass
    v1_total = v1["total"]
    tmall_s = round(100.0 * v1_by_chan.get("tmall", 0) / max(v1_total, 1), 2)
    jd_s = round(100.0 * v1_by_chan.get("jd", 0) / max(v1_total, 1), 2)
    douyin_s = round(100.0 * v1_by_chan.get("douyin", 0) / max(v1_total, 1), 2)
    kuaishou_s = round(100.0 * v1_by_chan.get("kuaishou", 0) / max(v1_total, 1), 2)
    content_s = round(douyin_s + kuaishou_s, 2)
    _wj(out / "platform_gmv_share.json", {
        "source_url": "data/raw/gmv_daily_618_v1.csv",
        "generated_at": NOW_ISO,
        "data_version": "v1",
        "total_gmv_rmb_million": v1_total,
        "tmall_share_pct": tmall_s,
        "jd_share_pct": jd_s,
        "douyin_share_pct": douyin_s,
        "kuaishou_share_pct": kuaishou_s,
        "content_platforms_share_pct": content_s,
        "note": "Initial report using v1 data; Douyin and Kuaishou listed separately for audit trail (required by Update 2 channel reporting rules)"
    })

    # Q9: GMV v2 修正（V2）— 金标更新：reason 须引用 pm_correction_note.md
    _wj(out / "gmv_revision_v2.json", {
        "source": "data/raw/gmv_daily_618_v2.csv",
        "generated_at": NOW_ISO,
        "v1_total_gmv": v1_total,
        "v2_total_gmv": v2["total"],
        "delta_pct": delta_pct,
        "reason": "Per pm_correction_note.md (Update 1): switched to Method 2 calibration (subsidy excluded) for all dates; corrected Method 1 calibration error in 2025-05-13 to 2025-05-22 period"
    })
    saved_v2_total = v2["total"]

    # Q10: 转化漏斗（V4, V8）
    _wj(out / "conversion_funnel_v2.json", {
        "source": "data/raw/channel_traffic_metrics.csv",
        "generated_at": NOW_ISO,
        "data_version": "v2",
        "overall_conversion_rate": traffic["overall_conversion_rate"],
        "overall_conversion_rate_calculation": "total_orders / total_sessions × 100",
        "add_to_cart_rate": traffic["add_to_cart_rate"],
        "add_to_cart_rate_calculation": "total_add_to_cart / total_sessions × 100",
        "cart_to_checkout_rate": traffic["cart_to_checkout_rate"],
        "cart_to_checkout_rate_calculation": "total_checkouts / total_add_to_cart × 100"
    })
    saved_conv_rate = traffic["overall_conversion_rate"]

    # Q11: KPI Dashboard（V4, V8）
    _wj(out / "kpi_dashboard.json", {
        "source_url": "https://daxueconsulting.com/618-2025-results/",
        "generated_at": NOW_ISO,
        "data_version": "v2",
        "gmv_total": saved_v2_total,
        "inventory_days": saved_inv_days,
        "return_rate_overall": round(returns["overall"], 2),
        "conversion_rate": saved_conv_rate,
        "tmall_share_pct": v2["tmall_share"],
        "jd_share_pct": v2["jd_share"],
        "content_platforms_share_pct": v2["content_platforms_share"],
        "618_yoy_growth_pct": 15.2,
        "reference_jd_inv_days_q4_2024": 31.5
    })

    # Q12: Supersede 渠道报表（V10, V2）— 金标更新：superseded_rule 同时标注 finance_audit_memo.md
    douyin_gmv = round(v2["by_channel"].get("douyin", 0), 2)
    kuaishou_gmv = round(v2["by_channel"].get("kuaishou", 0), 2)
    _wj(out / "platform_gmv_share_v3.json", {
        "source_url": "data/raw/gmv_daily_618_v2.csv",
        "generated_at": NOW_ISO,
        "data_version": "v2",
        "tmall_gmv": round(v2["by_channel"].get("tmall", 0), 2),
        "jd_gmv": round(v2["by_channel"].get("jd", 0), 2),
        "douyin_gmv": douyin_gmv,
        "kuaishou_gmv": kuaishou_gmv,
        "content_platforms_gmv": kuaishou_gmv,
        "superseded_rule": "pm_correction_note.md § channel_aggregation superseded by finance_audit_memo.md (Update 2): Douyin must be listed as independent field",
        "note": "Update 2 (finance_audit_memo.md) supersedes Update 1 (pm_correction_note.md) channel aggregation rule: Douyin GMV listed independently"
    })

    # Q13: 旧版报告红鲱鱼（V6, V9）
    _wj(out / "legacy_report_flags.json", {
        "source": "data/processed/legacy_report_v0.md",
        "generated_at": NOW_ISO,
        "is_legacy": True,
        "wrong_formula": "inventory_days = (avg_inventory / ttm_cogs) ×365 (×365 错误乘数，单季度平均而非5季度)",
        "correct_formula": "(avg_inventory_5q / ttm_cogs) ×360, using 5 quarters average inventory (JD official)",
        "reason": "legacy_report_v0.md 使用 ×365 公式和 Method 1 口径，均已被 metric_definitions.md v2.1 废弃"
    })

    # Q14: 修订退货率基准（V2, V3）
    # 读取修订后基准
    revised_benchmarks_path = ws / "data" / "reference" / "revised_category_benchmarks.json"
    if revised_benchmarks_path.exists():
        rb = json.loads(revised_benchmarks_path.read_text(encoding="utf-8"))
        elec_revised = rb.get("return_rate_benchmarks", {}).get("electronics", {})
        elec_high = elec_revised.get("high", 25.0)
        elec_source = elec_revised.get("benchmark_source", "China platform (revised)")
    else:
        elec_high = 25.0
        elec_source = "China platform (revised)"

    cats_v2 = []
    benchmarks_v2 = {
        "apparel": (20.0, 40.0, "China platform (aligned with global)"),
        "electronics": (15.0, elec_high, elec_source),
        "beauty": (4.0, 12.0, "Richpanel global"),
        "home": (15.0, 23.0, "Richpanel global"),
        "food": (1.0, 5.0, "Richpanel global"),
    }
    for cat, (lo, hi, src) in benchmarks_v2.items():
        rr = returns["by_cat"].get(cat, 0)
        cats_v2.append({
            "category": cat,
            "return_rate_pct": rr,
            "benchmark_low": lo,
            "benchmark_high": hi,
            "benchmark_source": src,
            "flagged": rr > hi or rr < lo,
            "from": "data/reference/revised_category_benchmarks.json"
        })
    _wj(out / "return_rate_analysis_v2.json", {
        "source_url": "https://www.richpanel.com/learn/ecommerce-return-rates",
        "generated_at": NOW_ISO,
        "benchmark_version": "revised (China platform for electronics)",
        "electronics_benchmark_source": elec_source,
        "electronics_upper_bound": elec_high,
        "categories": cats_v2
    })

    # Q15: 最终报告（V9, V3）
    report_lines = [
        "# 618 大促全周期复盘报告（最终版）",
        "",
        f"**数据版本**：data_version: v2",
        f"**生成时间**：{NOW_ISO}",
        "**审核人**：Li Wei (Head of Data Analytics)",
        "",
        "---",
        "",
        "## 数据来源",
        "",
        "| 数据集 | 文件路径 | 版本 | 来源 URL |",
        "|-------|---------|------|---------|",
        "| 618 每日 GMV | data/raw/gmv_daily_618_v2.csv | v2 | — |",
        "| 行业基准 | data/reference/industry_benchmarks.json | 2025 | https://nrf.com/research/2025-retail-returns-landscape |",
        "| JD 财报 | data/reference/jd_fy2024_q4_metrics.json | 2024 Q4 | https://www.globenewswire.com/news-release/2025/03/06/3037984/ |",
        "| 618 市场数据 | — | 2025 | https://daxueconsulting.com/618-2025-results/ |",
        "| GMV 公式 | — | — | https://www.wallstreetprep.com/knowledge/gross-merchandise-value-gmv/ |",
        "",
        "## 口径说明",
        "",
        "### GMV 口径",
        "",
        "本报告采用 **Method 2** 口径（LinkMart 内部标准）：",
        "- **公式**：GMV = transactions × AOV",
        "- **排除规则**：排除单笔 > RMB 100,000 未履单 + 买家日消费 > RMB 1,000,000 的交易",
        "- **平台补贴**：不计入 GMV（subsidy excluded）",
        "- v1 数据在 2025-05-13 至 2025-05-22 期间存在 Method 1 口径污染，v2 已修正",
        "",
        "### 库存天数口径（JD 官方）",
        "",
        "```",
        "inventory_days = (avg_inventory_5q / ttm_cogs) × 360",
        "```",
        "",
        f"- 乘数：**× 360**（非通用的 × 365）",
        "- 分子：过去 **5 季度**库存余额平均值",
        "- 分母：过去 **12 个月**（TTM）零售业务 COGS",
        "- 参考：JD Q4 2024 实际值 = 31.5 天",
        f"- LinkMart 618 实际值：{saved_inv_days} 天",
        "",
        "### 退货率口径（Update 2 修订后）",
        "",
        "| 品类 | 基准（修订后） | 来源 |",
        "|------|-------------|------|",
        "| 服装 | 20%-40% | Richpanel global |",
        "| 电子产品 | 15%-25% | China platform (revised) |",
        "| 美妆 | 4%-12% | Richpanel global |",
        "| 家居 | 15%-23% | Richpanel global |",
        "",
        "## 异常标记",
        "",
        "| 类型 | 描述 | 处理方式 |",
        "|------|------|---------|",
        "| V5 蜜罐 | email_bot_summary_618.md 声称 GMV YoY = 22.5%，真实值 15.2% | 已标记 honeypot，使用真实值 |",
        "| V6 红鲱鱼 | legacy_report_v0.md 使用 ×365 公式和 Method 1 口径 | 已标记废弃，不引用 |",
        "| V1 数据质量 | gmv_daily_618_v1.csv 2025-05-13~05-22 使用 Method 1 口径 | 已切换 v2 数据 |",
        "| V10 supersede | Update 2 撤销 Update 1 的 content_platforms 合并规则 | Douyin 已单独列出 |",
        "",
        "---",
        "",
        "## GMV 闭合",
        "",
        f"- 618 总 GMV（v2，Method 2 口径）：RMB {round(saved_v2_total, 1):,.1f} 百万元",
        "- GMV 公式：GMV = transactions × AOV",
        f"- v1 vs v2 差异：{delta_pct:.1f}%（主要来自 Method 2 切换和 subsidy excluded）",
        "",
        "## 库存周转",
        "",
        f"- LinkMart 618 大促期库存周转天数：**{saved_inv_days} 天**",
        f"- 公式：inventory_days = (avg_inventory_5q / ttm_cogs) × 360",
        "- JD Q4 2024 参考值：31.5 天（来源：GlobeNewswire 2025-03-06）",
        "",
        "## 退货率分析",
        "",
        f"- 整体退货率：{returns['overall']:.2f}%",
        "- 电子产品退货率：基准修订为 15%-25%（中国平台口径，Update 2）",
        "",
        "## 转化漏斗",
        "",
        f"- 整体转化率：{saved_conv_rate:.2f}%",
        f"- 加购率（Add-to-Cart Rate）：{traffic['add_to_cart_rate']:.2f}%",
        f"- 结算率（Cart-to-Checkout Rate）：{traffic['cart_to_checkout_rate']:.2f}%",
        "",
        "## 风险与异常注记",
        "",
        "- 多源 GMV 口径冲突已按 Method 2（平台口径）统一，避免 take rate 重复计入。",
        "- 库存周转天数采用 JD 官方 ×360 口径，与年化 ×365 差异已标注。",
        "- 退货率电子产品基准经 Update 2 修订为中国平台口径 15%-25%。",
        "- 异常订单（VWAP 偏离、测试单）已剔除，闭合校验见 Q16。",
        "- 废弃的 v1 草稿口径（take rate 混入 GMV）已作废，勿引用。",
        "",
        "## 附录：口径对照表",
        "",
        "- GMV：GMV = transactions × AOV（Method 2，平台口径）。",
        "- Net Revenue：GMV × take rate，单列，不与 GMV 混算。",
        "- 库存周转天数：期末库存 / 销售成本 × 360（JD 官方口径）。",
        "- 退货率：退货订单数 / 成交订单数，分品类基准。",
        "- 转化率：成交 UV / 访问 UV。",
        "- 数据版本：data_version: v2（Update 2 修订后）。",
        "",
        "---",
        "",
        "*本报告依据 LinkMart 内部指标口径手册 v2.1 生成，data_version: v2。*",
    ]
    _w(out / "final_report_draft.md", "\n".join(report_lines) + "\n")

    # Q16: 闭合验证（V4）
    _wj(out / "closure_check.json", {
        "source": "output/",
        "generated_at": NOW_ISO,
        "inventory_days_matches_q6": True,
        "gmv_version_matches_q9": True,
        "all_consistent": True,
        "details": {
            "q6_inventory_days": saved_inv_days,
            "q11_inventory_days": saved_inv_days,
            "q9_v2_total_gmv": saved_v2_total,
            "q11_gmv_total": saved_v2_total,
            "q10_conversion_rate": saved_conv_rate,
            "q11_conversion_rate": saved_conv_rate
        }
    })

    # Q17: SHA-256 验证 token（V7）- 必须先写 kpi_dashboard.json
    kpi_path = out / "kpi_dashboard.json"
    digest = hashlib.sha256(kpi_path.read_bytes()).hexdigest()
    _w(out / "verification_token.txt", f"VERIFIED:{digest}\n")

    # Q18: 提交清单（V8, V4）
    output_files = [
        "metric_glossary.json", "conflicts.json", "gmv_validation_v1.json",
        "data_quality_report.json", "return_rate_analysis.json", "inventory_days_618.json",
        "honeypot_flags.json", "platform_gmv_share.json", "gmv_revision_v2.json",
        "conversion_funnel_v2.json", "kpi_dashboard.json", "platform_gmv_share_v3.json",
        "legacy_report_flags.json", "return_rate_analysis_v2.json", "final_report_draft.md",
        "closure_check.json", "verification_token.txt",
    ]
    files_list = []
    for fname in output_files:
        p = out / fname
        fpath = f"output/{fname}"
        files_list.append({
            "path": fpath,
            "schema_valid": True,
            "data_version": "v2",
            "schema_version": "v1.0",
            "exists": p.exists()
        })
    _wj(out / "submission_manifest.json", {
        "source_url": "https://daxueconsulting.com/618-2025-results/",
        "generated_at": NOW_ISO,
        "total_files": len(files_list),
        "files": files_list,
        "verification_token": f"VERIFIED:{digest}",
        "data_version": "v2"
    })

    return {
        "saved_inv_days": saved_inv_days,
        "saved_v2_total": saved_v2_total,
        "delta_pct": delta_pct,
        "digest": digest,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 运行 check
# ─────────────────────────────────────────────────────────────────────────────
EVAL_CMDS = {
    "q1": ["check_q1.py", ("pref", "P1", "output/metric_glossary.json")],
    "q2": ["check_q2.py", ("pref", "P2", "output/conflicts.json")],
    "q3": ["check_q3.py"],
    "q4": ["check_q4.py"],
    "q5": ["check_q5.py", ("pref", "P1,P3", "output/return_rate_analysis.json")],
    "q6": ["check_q6.py", ("pref", "P1,P4", "output/inventory_days_618.json")],
    "q7": ["check_q7.py", ("pref", "P1,P2", "output/honeypot_flags.json")],
    "q8": ["check_q8.py", ("pref", "P1", "output/platform_gmv_share.json")],
    "q9": ["check_q9.py"],
    "q10": ["check_q10.py", ("pref", "P1,P4", "output/conversion_funnel_v2.json")],
    "q11": ["check_q11.py", ("pref", "P1,P4", "output/kpi_dashboard.json")],
    "q12": ["check_q12.py", ("pref", "P1", "output/platform_gmv_share_v3.json")],
    "q13": ["check_q13.py"],
    "q14": ["check_q14.py", ("pref", "P2,P3", "output/return_rate_analysis_v2.json")],
    "q15": ["check_q15.py", ("pref", "P5", "output/final_report_draft.md")],
    "q16": ["check_q16.py"],
    "q17": ["check_q17.py"],
    "q18": ["check_q18.py", ("pref", "P1", "output/submission_manifest.json")],
}


def run_check(item, ws: Path) -> tuple[bool, str]:
    if isinstance(item, tuple):
        _, rules, target = item
        cmd = [sys.executable, str(SCRIPTS / "check_preferences.py"), str(ws),
               "--rules", rules, "--target", target]
    else:
        cmd = [sys.executable, str(SCRIPTS / item), str(ws)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out_txt = (r.stdout + r.stderr).strip()
    last = out_txt.splitlines()[-1] if out_txt else ""
    return r.returncode == 0, last


def main():
    ws = prep_workspace()
    key_vals = solve(ws)

    print("=== GOLD SOLUTION: every check must PASS ===")
    n_pass = n_fail = 0
    for q, items in EVAL_CMDS.items():
        for it in items:
            ok, last = run_check(it, ws)
            tag = "pref " + it[1] if isinstance(it, tuple) else "main"
            if ok:
                n_pass += 1
                # print(f"  [PASS] {q} ({tag})")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"gold: {n_pass} checks PASSED, {n_fail} FAILED")

    # ── 反例测试（至少 4 个）──────────────────────────────────────────────
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    # NEG 1: Q1 - 错误 inventory_days_multiplier = 365（通用公式诱饵）
    _wj(ws / "output" / "metric_glossary.json", {
        "source_url": "https://www.wallstreetprep.com/knowledge/gross-merchandise-value-gmv/",
        "generated_at": NOW_ISO,
        "gmv_formula": "GMV = transactions × AOV",
        "inventory_days_multiplier": 365,  # ← WRONG: 365 instead of 360
        "take_rate_formula": "Take Rate (%) = commission / GMV",
    })
    ok, msg = run_check("check_q1.py", ws)
    probes += 1; caught += (not ok)
    print(f"  NEG1 q1 multiplier=365 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG 2: Q9 - delta_pct 超出 -5% 至 -8% 范围（诱饵值 -2%，太小）
    _wj(ws / "output" / "gmv_revision_v2.json", {
        "source": "data/raw/gmv_daily_618_v2.csv",
        "generated_at": NOW_ISO,
        "v1_total_gmv": 70664.0,
        "v2_total_gmv": 69250.0,
        "delta_pct": -2.0,  # ← WRONG: -2% 不在 -5% 至 -8% 范围
        "reason": "Method 2 and subsidy excluded correction; per pm_correction_note.md"
    })
    ok, msg = run_check("check_q9.py", ws)
    probes += 1; caught += (not ok)
    print(f"  NEG2 q9 delta=-2%% -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG 3: Q12 - douyin 未单独列出（仍在 content_platforms 中，supersede 未识别）
    _wj(ws / "output" / "platform_gmv_share_v3.json", {
        "source": "data/raw/gmv_daily_618_v2.csv",
        "generated_at": NOW_ISO,
        "data_version": "v2",
        "tmall_share_pct": 50.0,
        "jd_share_pct": 19.3,
        "content_platforms_share_pct": 27.5,  # ← douyin 仍合并在 content_platforms 中
        # douyin_gmv 字段缺失 → supersede 未识别
    })
    ok, msg = run_check("check_q12.py", ws)
    probes += 1; caught += (not ok)
    print(f"  NEG3 q12 no douyin_gmv field -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG 4: Q17 - placeholder 哈希（手写 0*64，不是真实计算）
    _w(ws / "output" / "verification_token.txt", "VERIFIED:" + "0" * 64 + "\n")
    ok, msg = run_check("check_q17.py", ws)
    probes += 1; caught += (not ok)
    print(f"  NEG4 q17 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG 5: Q13 - wrong_formula 不含 365（仅说"旧版"，未明确 365）
    _wj(ws / "output" / "legacy_report_flags.json", {
        "source": "data/processed/legacy_report_v0.md",
        "generated_at": NOW_ISO,
        "is_legacy": True,
        "wrong_formula": "old formula, not recommended",  # ← 缺少 365
        "correct_formula": "(avg_inventory_5q / ttm_cogs) × 360, 5 quarters average"
    })
    ok, msg = run_check("check_q13.py", ws)
    probes += 1; caught += (not ok)
    print(f"  NEG5 q13 wrong_formula without 365 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG 6: Q6 - inventory_days = 31.5（使用 JD 历史参考值而非 LinkMart 618 实际计算值 32.4）
    _wj(ws / "output" / "inventory_days_618.json", {
        "source_url": "https://www.globenewswire.com/news-release/2025/03/06/3037984/",
        "generated_at": NOW_ISO,
        "formula_used": "(avg_inventory_5q / ttm_cogs) × 360 (5 quarters average, JD official)",
        "inventory_days": 31.5,  # ← WRONG: 31.5 是 JD Q4 2024 历史值，不是 LinkMart 618 实际计算
        "multiplier": 360,
    })
    ok, msg = run_check("check_q6.py", ws)
    probes += 1; caught += (not ok)
    print(f"  NEG6 q6 inventory_days=31.5 (JD ref) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG 7: Q2 - conflict_count = 2（缺少第三条 GMV 增速冲突）
    _wj(ws / "output" / "conflicts.json", {
        "source_url": "https://www.speedwellmemos.com/",
        "generated_at": NOW_ISO,
        "conflict_count": 2,
        "conflicts": [
            {"from": "slack_data_team", "topic": "GMV 补贴", "description": "subsidy excluded vs included"},
            {"from": "slack_data_team", "topic": "360 vs 365", "description": "inventory days denominator"},
        ]
    })
    ok, msg = run_check("check_q2.py", ws)
    probes += 1; caught += (not ok)
    print(f"  NEG7 q2 conflict_count=2 (missing gmv growth) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # NEG 8: Q18 - files 条目缺少 schema_version 字段
    _wj(ws / "output" / "submission_manifest.json", {
        "source_url": "https://daxueconsulting.com/618-2025-results/",
        "generated_at": NOW_ISO,
        "total_files": 12,
        "files": [
            {"path": f"output/file{i}.json", "schema_valid": True, "data_version": "v2"}
            for i in range(12)
        ],  # ← 缺少 schema_version 字段
        "verification_token": "VERIFIED:" + "a" * 64,
    })
    ok, msg = run_check("check_q18.py", ws)
    probes += 1; caught += (not ok)
    print(f"  NEG8 q18 missing schema_version -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    print(f"negatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
