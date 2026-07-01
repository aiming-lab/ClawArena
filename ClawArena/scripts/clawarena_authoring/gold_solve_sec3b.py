#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_sec3b.py — sec3b 可解性审计（金标自检）。

在 workspace 的临时副本上应用 update 后写出每一轮的「正确产物」，
然后运行全部 check_qN.py + check_preferences.py，断言正解全部 PASS。
再用 ≥4 个反例（错误产物）断言 check 能 FAIL。

运行：python scripts/clawarena_authoring/gold_solve_sec3b.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "sec3b"
UPD = DS / "openclaw" / "updates" / "sec3b"
SCRIPTS = DS / "eval" / "sec3b" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/sec3b_gold_ws")


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # 应用 Update 1 workspace 文件
    shutil.copy(
        UPD / "upd1_workspace" / "regulatory" / "sec_inquiry_letter_20241105.md",
        GOLD / "regulatory" / "sec_inquiry_letter_20241105.md"
    )
    shutil.copy(
        UPD / "upd1_workspace" / "incident" / "affected_orders_detail.csv",
        GOLD / "incident" / "affected_orders_detail.csv"
    )
    # 应用 Update 2 workspace 文件
    (GOLD / "regulatory").mkdir(parents=True, exist_ok=True)
    shutil.copy(
        UPD / "upd2_workspace" / "regulatory" / "legal_counsel_memo_20241106.md",
        GOLD / "regulatory" / "legal_counsel_memo_20241106.md"
    )
    shutil.copy(
        UPD / "upd2_workspace" / "regulatory" / "revised_field_spec_v2.md",
        GOLD / "regulatory" / "revised_field_spec_v2.md"
    )
    # 应用 Update 3 workspace 文件
    shutil.copy(
        UPD / "upd3_workspace" / "regulatory" / "sec_formal_investigation_20241110.md",
        GOLD / "regulatory" / "sec_formal_investigation_20241110.md"
    )
    shutil.copy(
        UPD / "upd3_workspace" / "regulatory" / "sec_backtest_template.py",
        GOLD / "regulatory" / "sec_backtest_template.py"
    )
    return GOLD


def _w(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def count_csv_data_rows(path: Path) -> int:
    """Count data rows in CSV (excluding header)."""
    with path.open(encoding="utf-8") as fh:
        return sum(1 for _ in csv.DictReader(fh))


def solve(ws: Path) -> None:
    out = ws / "output"
    out.mkdir(exist_ok=True)

    # ------------------------------------------------------------------
    # q1 — 事故时间线 JSON
    # ------------------------------------------------------------------
    _wj(out / "incident_timeline_v1.json", {
        "incident_date": "2024-11-03",
        "event_time_utc": "2024-11-03T14:30:00Z",
        "timezone_offset": -4,
        "correct_timezone_offset": -5,
    })

    # ------------------------------------------------------------------
    # q2 — 时区 bug 报告 MD（含 UTC-4/UTC-5 + 行号）
    # ------------------------------------------------------------------
    _w(out / "timezone_bug_report.md", (
        "# Timezone Bug Report — AROS v4.2 timezone_config.py\n\n"
        "## Bug Identification\n\n"
        "- **File**: `code/aros/timezone_config.py`\n"
        "- **Line 42**: `UTC_OFFSET = -4`\n"
        "- **Error value**: UTC-4 (America/New_York EDT — incorrect after 2024-11-03 DST switch)\n"
        "- **Correct value**: UTC-5 (America/New_York EST — correct after 2024-11-03 switch)\n\n"
        "## Root Cause\n\n"
        "The UTC offset was hardcoded at deployment (2024-10-15, during EDT/UTC-4 period) "
        "and was not updated when US Eastern time switched from EDT (UTC-4) to EST (UTC-5) "
        "on 2024-11-03 at 02:00 local time.\n\n"
        "The `DST_AWARE` flag on line ~30 is `False`, confirming no automatic DST handling.\n\n"
        "## Fix Required\n\n"
        "Replace `UTC_OFFSET = -4` with a DST-aware timezone library call (e.g. `pytz` or `zoneinfo`).\n"
        "The deprecated `code/legacy/aros_v3_1_router_DEPRECATED.py` must NOT be used.\n"
    ))

    # ------------------------------------------------------------------
    # q3 — 受影响订单计数 JSON（新增 audit_log_total_scanned 字段）
    # ------------------------------------------------------------------
    # Count ANOMALY_DST_MISMATCH entries AND total non-empty lines in the audit log
    audit_log = ws / "incident" / "aros_v4_2_audit_log.jsonl"
    total_affected = 0
    audit_log_total_scanned = 0
    with audit_log.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            audit_log_total_scanned += 1
            try:
                entry = json.loads(line)
                if entry.get("status") == "ANOMALY_DST_MISMATCH":
                    total_affected += 1
            except json.JSONDecodeError:
                pass

    _wj(out / "affected_orders_count.json", {
        "total_affected": total_affected,
        "time_window_utc_start": "2024-11-03T14:00:00Z",
        "time_window_utc_end": "2024-11-03T15:00:00Z",
        "audit_log_total_scanned": audit_log_total_scanned,
    })

    # ------------------------------------------------------------------
    # q4 — bot 摘要错误识别 JSON（V5 蜂蜜罐）
    # ------------------------------------------------------------------
    _wj(out / "bot_summary_errors.json", {
        "errors": [
            {
                "field": "kcg_financial_loss",
                "claimed_value": "$440M",
                "correct_value": "$460,000,000+ (exceeding $460M)",
                "source": "regulatory/sec_release_34_70694_full.md (SEC Release 34-70694) / "
                          "SEC Press Release 2013-222",
                "severity": "high",
            },
            {
                "field": "cme_settlement_utc",
                "claimed_value": "20:00:00 UTC",
                "correct_value": "21:00:00 UTC (15:00 CT = 21:00 UTC in EST after DST switch)",
                "source": "reference/cme_settlement_schedule.md",
                "severity": "high",
            },
            {
                "field": "utc_offset_assessment",
                "claimed_value": "UTC-4 was correct for the period",
                "correct_value": "UTC-4 was INCORRECT after 2024-11-03 DST switch; correct offset is UTC-5 (EST)",
                "source": "code/aros/timezone_config.py (line 42)",
                "severity": "medium",
            },
        ]
    })

    # ------------------------------------------------------------------
    # q5 — KCG 锚点核查 JSON（新增 case_number 精确原文字段）
    # ------------------------------------------------------------------
    _wj(out / "kcg_anchor_check.json", {
        "financial_loss_usd": 460000000,
        "penalty_usd": 12000000,
        "rule_violated": "Rule 15c3-5(b)",
        "servers_count": 8,
        "pre_market_emails": 97,
        "shares_traded_millions": 397.0,
        "case_number": "Admin. Proc. File No. 3-15570",
    })

    # ------------------------------------------------------------------
    # q6 — 废弃代码评估 JSON（V6 红鲱鱼）
    # ------------------------------------------------------------------
    _wj(out / "legacy_code_assessment.json", {
        "is_applicable": False,
        "reason": (
            "The file code/legacy/aros_v3_1_router_DEPRECATED.py is deprecated as of "
            "2023-06-01. It does not implement the MiFIR Field 28 UTC reporting requirement "
            "(reports local time instead of UTC, violating FCA Market Watch 59). It is also "
            "incompatible with the T+1 settlement rule (Rule 15c6-1, effective 2024-05-28) "
            "and uses an obsolete CME API. The DEPRECATED designation means it must not "
            "be referenced for incident remediation."
        ),
        "recommendation": (
            "Use code/aros/timezone_config.py (AROS v4.2) as the base for the fix. "
            "Replace the hardcoded UTC_OFFSET = -4 on line 42 with a DST-aware "
            "implementation using Python's `zoneinfo` or `pytz` library."
        ),
    })

    # ------------------------------------------------------------------
    # q7 — MiFIR Field 28 修正报告 MD（V9 + P3）
    # ------------------------------------------------------------------
    _w(out / "mifir_field28_correction.md", (
        "# MiFIR Field 28 — UTC Timestamp Correction Report\n\n"
        "## ArtemisQ Capital — Incident 2024-11-03\n\n"
        "## Error Description\n\n"
        "On 2024-11-03, the AROS v4.2 automated routing system submitted MiFIR "
        "transaction reports with **Field 28** (trading date and time) timestamps "
        "expressed in local Eastern time (UTC-4) rather than the mandatory **UTC** format.\n\n"
        "This error occurred because the system's UTC offset remained hardcoded at -4 "
        "after the US Eastern timezone transitioned from EDT (UTC-4) to EST (UTC-5) "
        "at 02:00 local time on 2024-11-03 (the annual DST fall-back transition).\n\n"
        "## Regulatory Citation\n\n"
        "**FCA Market Watch 59** (April 2019) explicitly identifies DST/BST transition "
        "errors as the most common compliance failure in **Field 28** transaction reporting. "
        "Per Market Watch 59 and RTS 22, Field 28 must be reported in **UTC** — not local time. "
        "This requirement replaced the MiFID I approach of reporting in local time.\n\n"
        "The affected transactions are in breach of:\n"
        "- Article 26 of MiFIR (transaction reporting obligation)\n"
        "- RTS 22 Field 28 specification (ISO 8601 UTC format mandatory)\n\n"
        "## Affected Period\n\n"
        "All Field 28 timestamps for transactions on 2024-11-03 between "
        "09:30:00 UTC and 22:00:00 UTC are offset by +1 hour from the correct UTC values.\n\n"
        "Example: A transaction at 14:30:00 UTC was reported as "
        "`2024-11-03T14:30:00-04:00` (local EDT time) instead of "
        "the correct `2024-11-03T14:30:00Z` (UTC).\n\n"
        "## Remediation Actions\n\n"
        "1. Submit corrected MiFIR transaction reports by 2024-11-12 (FCA deadline)\n"
        "2. Replace hardcoded `UTC_OFFSET = -4` in `timezone_config.py` with "
        "a DST-aware implementation (e.g. `zoneinfo.ZoneInfo('America/New_York')`)\n"
        "3. Implement automated DST transition testing in the pre-deployment checklist\n"
        "4. Add UTC conversion validation to MiFIR report generation module\n"
    ))

    # ------------------------------------------------------------------
    # q8 — T+1 结算截止时间偏移 JSON
    # ------------------------------------------------------------------
    _wj(out / "t1_settlement_impact.json", {
        "rule_effective_date": "2024-05-28",
        "incorrect_cutoff_utc": "2024-11-04T01:00:00Z",  # 21:00 ET with UTC-4: 21+4=25=01:00 next day
        "correct_cutoff_utc": "2024-11-04T02:00:00Z",    # 21:00 ET with UTC-5: 21+5=26=02:00 next day
        "offset_minutes": 60,
    })

    # ------------------------------------------------------------------
    # q9 — 根因分析 MD（C★ 加难：引用 q3 的 audit_log_total_scanned，
    #       q5 的 financial_loss_usd 精确值，Rule 15c6-1 生效日期）
    # ------------------------------------------------------------------
    _w(out / "root_cause_analysis.md", (
        "# Root Cause Analysis — AROS v4.2 Timezone Misconfiguration\n\n"
        "## Incident Date: 2024-11-03\n\n"
        "## Root Cause\n\n"
        "The AROS v4.2 automated routing system hardcoded `UTC_OFFSET = -4` in "
        "`code/aros/timezone_config.py` (line 42). This was correct during the EDT period "
        "(UTC-4), but was not updated when US Eastern time switched from EDT (UTC-4) to "
        "EST (UTC-5) on 2024-11-03 at 02:00 local time.\n\n"
        "The 1-hour discrepancy between UTC-4 (incorrect) and UTC-5 (correct) caused:\n"
        "1. T+1 settlement cutoff computed 60 minutes early (Rule 15c6-1, effective 2024-05-28)\n"
        "2. CME daily settlement reference at 20:00 UTC instead of correct 21:00 UTC\n"
        "3. MiFIR Field 28 timestamps submitted as local time instead of UTC (FCA Market Watch 59)\n\n"
        "## Contributing Factors (severity descending)\n\n"
        "1. **DST_AWARE = False** in timezone_config.py — no automatic DST detection\n"
        "2. **Missing deployment checklist item** — no DST transition update procedure\n"
        "3. **Risk monitor disconnected** from order router — Rule 15c3-5(b) integration gap\n"
        "4. **No pre-DST-transition testing** — DST switch day not in test calendar\n\n"
        "## Timeline\n\n"
        "| UTC Time | Event |\n"
        "|----------|-------|\n"
        "| 2024-11-03T07:00:00Z | DST switch already occurred at 07:00 UTC; UTC-5 now correct |\n"
        "| 2024-11-03T09:30:00Z | Market open; AROS using UTC-4 (wrong) |\n"
        "| 2024-11-03T14:00:00Z | Anomaly window begins — T+1 orders in wrong window |\n"
        "| 2024-11-03T14:30:00Z | First mis-timed T+1 settlement order |\n"
        "| 2024-11-03T20:00:00Z | System triggers CME delta-hedge 1 hour early |\n"
        "| 2024-11-03T21:00:00Z | Correct CME settlement time (15:00 CT = 21:00 UTC in EST) |\n"
        "| 2024-11-03T22:00:00Z | AROS halted; UTC_OFFSET error confirmed |\n\n"
        "## Audit Scope\n\n"
        f"Audit log analysis: {audit_log_total_scanned} total entries scanned in "
        f"incident/aros_v4_2_audit_log.jsonl. Of these, {total_affected} entries "
        "had status ANOMALY_DST_MISMATCH (anomaly window 2024-11-03T14:00:00Z to 2024-11-03T15:00:00Z).\n\n"
        "## Financial Impact\n\n"
        f"Total affected orders (ANOMALY_DST_MISMATCH): {total_affected}\n\n"
        "## Regulatory Violations\n\n"
        "- Rule 15c3-5(b): financial risk management controls not robust to DST transitions\n"
        "- Rule 15c6-1 (effective 2024-05-28): T+1 settlement cutoff mis-calculated\n"
        "- MiFIR Field 28 (FCA Market Watch 59): UTC timestamps not used\n\n"
        "## Reference Comparison: Knight Capital Group (2012)\n\n"
        "The KCG incident (SEC Release 34-70694, Admin. Proc. File No. 3-15570) resulted in "
        f"a trading loss of 460000000 USD ($460,000,000+) and a $12,000,000 penalty for "
        "Rule 15c3-5(b) violations. The AROS v4.2 incident presents a similar category of "
        "risk management system failure (hardcoded/static configuration without operational validation).\n"
    ))

    # ------------------------------------------------------------------
    # q10 — SEC 询问框架 JSON（Update 1 后，price_diff_usd 仍是正确字段）
    # ------------------------------------------------------------------
    detail_csv = ws / "incident" / "affected_orders_detail.csv"
    affected_order_count = count_csv_data_rows(detail_csv) if detail_csv.exists() else 7200

    _wj(out / "sec_response_framework.json", {
        "deadline_utc": "2024-11-07T15:00:00Z",
        "required_fields": [
            "order_id",
            "expected_settlement_utc",
            "actual_settlement_utc",
            "price_diff_usd",
        ],
        "affected_order_count_from_detail": affected_order_count,
    })

    # ------------------------------------------------------------------
    # q11 — 订单级别差异报告 CSV（Update 2 后：price_diff_vwap_usd）
    # ------------------------------------------------------------------
    # Read affected orders detail
    diff_rows = [["order_id", "expected_settlement_utc", "actual_settlement_utc", "price_diff_vwap_usd"]]
    if detail_csv.exists():
        with detail_csv.open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                ts_str = row.get("event_time_utc", "2024-11-03T14:00:00Z")
                # Correct cutoff: 2024-11-04T02:00:00Z (UTC-5)
                # System cutoff: 2024-11-04T01:00:00Z (UTC-4)
                expected = "2024-11-04T02:00:00Z"
                actual = "2024-11-04T01:00:00Z"
                # VWAP-based price diff (simplified: use execution price - avg VWAP)
                try:
                    price = float(row.get("price", 4560.0))
                    qty = int(row.get("qty", 1))
                    vwap_ref = 4562.50  # approximate VWAP for the period
                    price_diff_vwap = round((price - vwap_ref) * qty, 2)
                except (ValueError, TypeError):
                    price_diff_vwap = 0.0
                diff_rows.append([
                    row.get("order_id", ""),
                    expected,
                    actual,
                    price_diff_vwap,
                ])
    else:
        # Fallback if detail CSV not available
        for i in range(7200):
            diff_rows.append([
                f"ORD-{20241103000000 + i:016d}",
                "2024-11-04T02:00:00Z",
                "2024-11-04T01:00:00Z",
                round((4562.5 - 4562.5), 2),
            ])

    import io
    buf = io.StringIO()
    csv.writer(buf).writerows(diff_rows)
    _w(out / "order_level_diff_report.csv", buf.getvalue())

    # ------------------------------------------------------------------
    # q12 — 报告 SHA-256 签名
    # ------------------------------------------------------------------
    csv_bytes = (out / "order_level_diff_report.csv").read_bytes()
    digest_q12 = hashlib.sha256(csv_bytes).hexdigest()
    _w(out / "report_signoff.txt", f"VERIFIED:{digest_q12}\n")

    # ------------------------------------------------------------------
    # q13 — 合规整改计划 MD（P3 sub-clause + P4 owner）
    # ------------------------------------------------------------------
    _w(out / "corrective_action_plan.md", (
        "# Corrective Action Plan (CAP) — AROS v4.2 Timezone Incident\n\n"
        "## Incident Reference\n\n"
        "**incident_ref**: AQ-2024-1103-DST\n"
        "**Date**: 2024-11-03\n"
        "**System**: AROS v4.2\n\n"
        "## Root Cause Summary\n\n"
        "Hardcoded UTC_OFFSET = -4 in timezone_config.py line 42 was not updated after "
        "US Eastern DST transition from EDT (UTC-4) to EST (UTC-5) on 2024-11-03. "
        "This caused T+1 settlement cutoffs (Rule 15c6-1) and CME settlement reference "
        "times to be 60 minutes off, and MiFIR Field 28 UTC timestamps to be incorrect "
        "per FCA Market Watch 59. Root cause is analogous to the KCG deployment error "
        "pattern (Rule 15c3-5(b) — SEC Release 34-70694).\n\n"
        "## Remediation Items\n\n"
        "### 1. Timezone Automation — DST-Aware Library\n"
        "- **action**: Replace hardcoded UTC_OFFSET in timezone_config.py with "
        "DST-aware implementation using Python zoneinfo or pytz library. "
        "Implement automatic timezone detection for America/New_York.\n"
        "- **owner**: Marcus Chen (Lead Quant Engineer)\n"
        "- **deadline_days**: 5\n\n"
        "### 2. Rule 15c3-5(b) — Risk Management Controls Review\n"
        "- **action**: Conduct full review of pre-trade financial risk management "
        "controls per Rule 15c3-5(b) (Market Access Rule). Ensure risk_monitor.py "
        "is integrated with order_router.py to prevent siloed risk management.\n"
        "- **owner**: Elena Vasquez (Chief Compliance Officer)\n"
        "- **deadline_days**: 30\n\n"
        "### 3. Rule 15c6-1 — T+1 Settlement UTC Calculation Audit\n"
        "- **action**: Audit all T+1 settlement cutoff calculations to confirm "
        "they use DST-aware UTC offset per Rule 15c6-1 (effective 2024-05-28). "
        "Test all calculations on DST transition dates.\n"
        "- **owner**: Yuki Tanaka (Risk Quant)\n"
        "- **deadline_days**: 14\n\n"
        "### 4. MiFIR Field 28 UTC Compliance Testing\n"
        "- **action**: Implement automated test suite to validate Field 28 UTC "
        "conversion for all DST transition dates (FCA Market Watch 59 requirement). "
        "Submit corrected transaction reports to FCA by 2024-11-12.\n"
        "- **owner**: Sophie Devereux (Regulatory Affairs Manager)\n"
        "- **deadline_days**: 7\n\n"
        "### 5. Deployment Checklist Update\n"
        "- **action**: Update AROS deployment checklist to include DST transition "
        "verification step: confirm UTC_OFFSET matches current local timezone offset "
        "before market-open on first Monday after any DST change date.\n"
        "- **owner**: Kenji Nakamura (DevOps Lead)\n"
        "- **deadline_days**: 10\n\n"
        "## Notes\n\n"
        "- The deprecated code/legacy/aros_v3_1_router_DEPRECATED.py must NOT be "
        "referenced or used in any remediation (see legacy_code_assessment.json).\n"
        "- Annual CEO certification to be updated to reflect Rule 15c3-5(b) "
        "remediation scope.\n"
    ))

    # ------------------------------------------------------------------
    # q14 — 监管提交摘要 JSON（P5 字段顺序固定；C★ 加难：
    #       financial_impact 包含 audit_log_total_scanned；
    #       新增 kcg_reference_loss_usd 精确引用 q5 输出）
    # ------------------------------------------------------------------
    import collections
    reg_summary = collections.OrderedDict()
    reg_summary["incident_date"] = "2024-11-03"
    reg_summary["rule_violated"] = "Rule 15c3-5(b) (Market Access Rule) and Rule 15c6-1 (T+1 Settlement, effective 2024-05-28)"
    reg_summary["financial_impact"] = (
        f"Total affected orders: {total_affected} (ANOMALY_DST_MISMATCH). "
        f"Audit log scope: {audit_log_total_scanned} entries scanned. "
        "T+1 settlement mis-classification due to 60-minute UTC offset error. "
        "MiFIR Field 28 UTC timestamps incorrect for full trading day."
    )
    reg_summary["remediation_count"] = 5
    reg_summary["submission_date"] = "2024-11-12"
    reg_summary_dict = dict(reg_summary)
    reg_summary_dict["kcg_reference_loss_usd"] = 460000000
    _wj(out / "regulatory_submission_summary.json", reg_summary_dict)

    # ------------------------------------------------------------------
    # q15 — 回测验证（E★ 加难：backtest_result.json 必须包含 schema_version="1.0"）
    # ------------------------------------------------------------------
    # Write the correct backtest result directly, including schema_version
    # (The backtest template script may not include schema_version — gold solve writes it correctly)
    _wj(out / "backtest_result.json", {
        "config_timezone_offset": -5,
        "trade_date": "2024-11-03",
        "simulated_settlement_utc": "2024-11-03T21:00:00Z",
        "expected_settlement_utc": "2024-11-03T21:00:00Z",
        "match": True,
        "script_version": "1.0-template",
        "schema_version": "1.0",
    })

    # ------------------------------------------------------------------
    # q16 — 最终签名（SHA-256 of backtest_result.json + corrective_action_plan.md）
    # ------------------------------------------------------------------
    f1_bytes = (out / "backtest_result.json").read_bytes()
    f2_bytes = (out / "corrective_action_plan.md").read_bytes()
    combined = f1_bytes + f2_bytes
    digest_q16 = hashlib.sha256(combined).hexdigest()
    _w(out / "final_submission_signoff.txt", f"VERIFIED:{digest_q16}\n")


# --------------------------------------------------------------------------- #
# 运行 check
# --------------------------------------------------------------------------- #
EVAL_CMDS = {
    "q1": ["check_q1.py", ("pref", "P1", "output/incident_timeline_v1.json")],
    "q2": ["check_q2.py"],
    "q3": ["check_q3.py", ("pref", "P1", "output/affected_orders_count.json")],
    "q4": ["check_q4.py", ("pref", "P1,P2", "output/bot_summary_errors.json")],
    "q5": ["check_q5.py", ("pref", "P1", "output/kcg_anchor_check.json")],
    "q6": ["check_q6.py"],
    "q7": ["check_q7.py", ("pref", "P3", "output/mifir_field28_correction.md")],
    "q8": ["check_q8.py", ("pref", "P1", "output/t1_settlement_impact.json")],
    "q9": ["check_q9.py", ("pref", "P2,P3", "output/root_cause_analysis.md")],
    "q10": ["check_q10.py", ("pref", "P1", "output/sec_response_framework.json")],
    "q11": ["check_q11.py"],
    "q12": ["check_q12.py"],
    "q13": ["check_q13.py", ("pref", "P3,P4", "output/corrective_action_plan.md")],
    "q14": ["check_q14.py", ("pref", "P1,P3,P5", "output/regulatory_submission_summary.json")],
    "q15": ["check_q15.py", ("pref", "P1", "output/backtest_result.json")],
    "q16": ["check_q16.py"],
}


def run_check(item, ws: Path) -> tuple[bool, str]:
    if isinstance(item, tuple):
        _, rules, target = item
        cmd = [sys.executable, str(SCRIPTS / "check_preferences.py"), str(ws),
               "--rules", rules, "--target", target]
    else:
        cmd = [sys.executable, str(SCRIPTS / item), str(ws)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    lines = (r.stdout + r.stderr).strip().splitlines()
    last = lines[-1] if lines else ""
    return r.returncode == 0, last


def main():
    ws = prep_workspace()
    solve(ws)

    print("=== GOLD SOLUTION: every check must PASS ===")
    n_pass = n_fail = 0
    for q, items in EVAL_CMDS.items():
        for it in items:
            ok, last = run_check(it, ws)
            tag = "pref " + it[1] if isinstance(it, tuple) else "main"
            if ok:
                n_pass += 1
                print(f"  [PASS] {q} ({tag}): {last}")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"\ngold: {n_pass} checks PASSED, {n_fail} FAILED")

    # ------------------------------------------------------------------
    # 反例抽样（>=4 个，每个必须 FAIL）
    # ------------------------------------------------------------------
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    # Probe 1: q1 wrong timezone_offset (decoy -5 instead of -4)
    _wj(ws / "output" / "incident_timeline_v1.json", {
        "incident_date": "2024-11-03",
        "event_time_utc": "2024-11-03T14:30:00Z",
        "timezone_offset": -5,  # WRONG: should be -4 (the bug value)
        "correct_timezone_offset": -5,
    })
    ok, _ = run_check("check_q1.py", ws); probes += 1; caught += (not ok)
    print(f"  q1 wrong_offset (-5 for bug) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q1
    _wj(ws / "output" / "incident_timeline_v1.json", {
        "incident_date": "2024-11-03",
        "event_time_utc": "2024-11-03T14:30:00Z",
        "timezone_offset": -4,
        "correct_timezone_offset": -5,
    })

    # Probe 2: q5 KCG loss = 440M (bot decoy)
    _wj(ws / "output" / "kcg_anchor_check.json", {
        "financial_loss_usd": 440000000,  # WRONG: bot decoy, correct is 460M
        "penalty_usd": 12000000,
        "rule_violated": "Rule 15c3-5(b)",
        "servers_count": 8,
        "pre_market_emails": 97,
        "shares_traded_millions": 397.0,
    })
    ok, _ = run_check("check_q5.py", ws); probes += 1; caught += (not ok)
    print(f"  q5 KCG_loss_440M (bot decoy) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q5
    _wj(ws / "output" / "kcg_anchor_check.json", {
        "financial_loss_usd": 460000000,
        "penalty_usd": 12000000,
        "rule_violated": "Rule 15c3-5(b)",
        "servers_count": 8,
        "pre_market_emails": 97,
        "shares_traded_millions": 397.0,
    })

    # Probe 3: q6 is_applicable = true (deprecated code referenced)
    _wj(ws / "output" / "legacy_code_assessment.json", {
        "is_applicable": True,  # WRONG: deprecated code must not be used
        "reason": "The v3.1 router has UTC_OFFSET=-5 which is correct",
        "recommendation": "Copy timezone logic from aros_v3_1_router_DEPRECATED.py",
    })
    ok, _ = run_check("check_q6.py", ws); probes += 1; caught += (not ok)
    print(f"  q6 is_applicable=true (V6 red herring) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q6
    _wj(ws / "output" / "legacy_code_assessment.json", {
        "is_applicable": False,
        "reason": "The file is deprecated as of 2023-06-01 and does not meet MiFIR requirements.",
        "recommendation": "Use code/aros/timezone_config.py with DST-aware zoneinfo library.",
    })

    # Probe 4: q11 uses superseded column price_diff_usd (not vwap)
    import io
    bad_rows = [["order_id", "expected_settlement_utc", "actual_settlement_utc", "price_diff_usd"]]  # SUPERSEDED
    for i in range(100):
        bad_rows.append([f"ORD-{i:016d}", "2024-11-04T02:00:00Z", "2024-11-04T01:00:00Z", "0.0"])
    buf2 = io.StringIO()
    csv.writer(buf2).writerows(bad_rows)
    _w(ws / "output" / "order_level_diff_report.csv", buf2.getvalue())
    ok, _ = run_check("check_q11.py", ws); probes += 1; caught += (not ok)
    print(f"  q11 superseded price_diff_usd column -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q11
    buf3 = io.StringIO()
    # Rebuild original diff report
    detail_csv = ws / "incident" / "affected_orders_detail.csv"
    diff_rows = [["order_id", "expected_settlement_utc", "actual_settlement_utc", "price_diff_vwap_usd"]]
    if detail_csv.exists():
        with detail_csv.open(encoding="utf-8") as fh:
            rdr = csv.DictReader(fh)
            for row in rdr:
                try:
                    price = float(row.get("price", 4560.0))
                    qty = int(row.get("qty", 1))
                    price_diff_vwap = round((price - 4562.50) * qty, 2)
                except (ValueError, TypeError):
                    price_diff_vwap = 0.0
                diff_rows.append([
                    row.get("order_id", ""),
                    "2024-11-04T02:00:00Z",
                    "2024-11-04T01:00:00Z",
                    price_diff_vwap,
                ])
    else:
        for i in range(7200):
            diff_rows.append([f"ORD-{20241103000000 + i:016d}", "2024-11-04T02:00:00Z", "2024-11-04T01:00:00Z", 0.0])
    csv.writer(buf3).writerows(diff_rows)
    _w(ws / "output" / "order_level_diff_report.csv", buf3.getvalue())
    # Recompute q12 sign after restoring
    _w(ws / "output" / "report_signoff.txt",
       "VERIFIED:" + hashlib.sha256((ws / "output" / "order_level_diff_report.csv").read_bytes()).hexdigest() + "\n")

    # Probe 5: q16 placeholder hash
    _w(ws / "output" / "final_submission_signoff.txt", "VERIFIED:" + "0" * 64 + "\n")
    ok, _ = run_check("check_q16.py", ws); probes += 1; caught += (not ok)
    print(f"  q16 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q16
    f1_b = (ws / "output" / "backtest_result.json").read_bytes()
    f2_b = (ws / "output" / "corrective_action_plan.md").read_bytes()
    _w(ws / "output" / "final_submission_signoff.txt",
       "VERIFIED:" + hashlib.sha256(f1_b + f2_b).hexdigest() + "\n")

    # Probe 6: q8 wrong offset_minutes=30 (should be 60)
    _wj(ws / "output" / "t1_settlement_impact.json", {
        "rule_effective_date": "2024-05-28",
        "incorrect_cutoff_utc": "2024-11-04T01:00:00Z",
        "correct_cutoff_utc": "2024-11-04T01:30:00Z",  # WRONG: 30min not 60min
        "offset_minutes": 30,
    })
    ok, _ = run_check("check_q8.py", ws); probes += 1; caught += (not ok)
    print(f"  q8 wrong_offset_30min -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q8
    _wj(ws / "output" / "t1_settlement_impact.json", {
        "rule_effective_date": "2024-05-28",
        "incorrect_cutoff_utc": "2024-11-04T01:00:00Z",
        "correct_cutoff_utc": "2024-11-04T02:00:00Z",
        "offset_minutes": 60,
    })

    # Probe 7: q3 missing audit_log_total_scanned field (agent only filled anomaly count)
    # Read correct values from the ws output file (written by solve())
    import json as _json
    _q3_data = _json.loads((ws / "output" / "affected_orders_count.json").read_text(encoding="utf-8"))
    _total_affected = int(_q3_data["total_affected"])
    _audit_log_total_scanned = int(_q3_data["audit_log_total_scanned"])
    _wj(ws / "output" / "affected_orders_count.json", {
        "total_affected": _total_affected,
        "time_window_utc_start": "2024-11-03T14:00:00Z",
        "time_window_utc_end": "2024-11-03T15:00:00Z",
        # audit_log_total_scanned intentionally MISSING
    })
    ok, _ = run_check("check_q3.py", ws); probes += 1; caught += (not ok)
    print(f"  q3 missing audit_log_total_scanned -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q3 with correct value including audit_log_total_scanned
    _wj(ws / "output" / "affected_orders_count.json", {
        "total_affected": _total_affected,
        "time_window_utc_start": "2024-11-03T14:00:00Z",
        "time_window_utc_end": "2024-11-03T15:00:00Z",
        "audit_log_total_scanned": _audit_log_total_scanned,
    })

    # Probe 8: q7 missing Article 26 and RTS 22 citations
    _w(ws / "output" / "mifir_field28_correction.md", (
        "# MiFIR Field 28 Correction\n\n"
        "The AROS system submitted timestamps in local time instead of UTC.\n"
        "FCA Market Watch 59 requires Field 28 in UTC format.\n"
        "DST transition caused the error.\n"
        "Remediation: replace hardcoded offset with zoneinfo library.\n"
    ))
    ok, _ = run_check("check_q7.py", ws); probes += 1; caught += (not ok)
    print(f"  q7 missing Article 26 + RTS 22 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q7
    _w(ws / "output" / "mifir_field28_correction.md", (
        "# MiFIR Field 28 — UTC Timestamp Correction Report\n\n"
        "## ArtemisQ Capital — Incident 2024-11-03\n\n"
        "## Error Description\n\n"
        "On 2024-11-03, AROS v4.2 submitted MiFIR transaction reports with "
        "**Field 28** timestamps expressed in local Eastern time (UTC-4) rather than UTC.\n"
        "DST transition caused the error.\n\n"
        "## Regulatory Citation\n\n"
        "**Article 26 of MiFIR** establishes the transaction reporting obligation.\n"
        "**RTS 22 Field 28** specifies the ISO 8601 UTC format for Field 28.\n"
        "**FCA Market Watch 59** identifies DST transition errors as the most common Field 28 failure.\n"
        "BST/standard-time transitions require validated UTC conversion.\n\n"
        "## Remediation Actions\n\n"
        "1. Submit corrected MiFIR reports by 2024-11-12\n"
        "2. Replace hardcoded UTC_OFFSET with DST-aware zoneinfo library\n"
        "3. Add automated UTC validation to Field 28 generation\n"
    ))

    # Probe 9: q9 missing CME times and total_affected from q3
    _w(ws / "output" / "root_cause_analysis.md", (
        "# Root Cause Analysis\n\n"
        "## Incident Date: 2024-11-03\n\n"
        "The AROS system used UTC-4 instead of UTC-5 after DST switch.\n"
        "Rule 15c3-5(b) violated.\n"
    ))
    ok, _ = run_check("check_q9.py", ws); probes += 1; caught += (not ok)
    print(f"  q9 missing CME times + q3 count -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q9 (with all required cross-round citations)
    _w(ws / "output" / "root_cause_analysis.md", (
        "# Root Cause Analysis — AROS v4.2 Timezone Misconfiguration\n\n"
        "## Incident Date: 2024-11-03\n\n"
        "## Root Cause\n\n"
        "UTC_OFFSET = -4 was not updated after DST switch from EDT (UTC-4) to EST (UTC-5).\n\n"
        "The 1-hour discrepancy caused:\n"
        "1. T+1 settlement cutoff 60 minutes early (Rule 15c6-1, effective 2024-05-28)\n"
        "2. CME settlement triggered at 20:00 UTC instead of correct 21:00 UTC\n"
        "3. MiFIR Field 28 timestamps incorrect (FCA Market Watch 59)\n\n"
        "## Contributing Factors (severity descending)\n\n"
        "1. DST_AWARE = False — no automatic DST detection\n"
        "2. Risk monitor disconnected — Rule 15c3-5(b) integration gap\n\n"
        "## Audit Scope\n\n"
        f"Audit log analysis: {_audit_log_total_scanned} total entries scanned. "
        f"Of these, {_total_affected} had status ANOMALY_DST_MISMATCH.\n\n"
        "## Financial Impact\n\n"
        f"Total affected orders (ANOMALY_DST_MISMATCH): {_total_affected}\n\n"
        "## Regulatory Violations\n\n"
        "- Rule 15c3-5(b): financial risk management controls not robust to DST\n"
        "- Rule 15c6-1 (effective 2024-05-28): T+1 settlement cutoff mis-calculated\n"
        "- MiFIR Field 28 (FCA Market Watch 59): UTC timestamps not used\n\n"
        "## KCG Reference\n\n"
        f"KCG incident (SEC Release 34-70694): financial_loss_usd = 460000000, "
        "$12,000,000 penalty for Rule 15c3-5(b) violations.\n"
    ))

    # Probe 10: q10 contains price_diff_vwap_usd (Update 2 name — wrong at this round)
    _wj(ws / "output" / "sec_response_framework.json", {
        "deadline_utc": "2024-11-07T15:00:00Z",
        "required_fields": [
            "order_id",
            "expected_settlement_utc",
            "actual_settlement_utc",
            "price_diff_vwap_usd",  # WRONG: Update 2 hasn't arrived yet
        ],
        "affected_order_count_from_detail": 1200,
    })
    ok, _ = run_check("check_q10.py", ws); probes += 1; caught += (not ok)
    print(f"  q10 vwap field at round 10 (Update 2 not yet issued) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q10
    _wj(ws / "output" / "sec_response_framework.json", {
        "deadline_utc": "2024-11-07T15:00:00Z",
        "required_fields": [
            "order_id",
            "expected_settlement_utc",
            "actual_settlement_utc",
            "price_diff_usd",
        ],
        "affected_order_count_from_detail": 1200,
    })

    # Probe 11: q14 missing kcg_reference_loss_usd and audit_log_total_scanned in financial_impact
    import collections
    bad_summary = collections.OrderedDict()
    bad_summary["incident_date"] = "2024-11-03"
    bad_summary["rule_violated"] = "Rule 15c3-5(b)"
    bad_summary["financial_impact"] = f"Total affected orders: {_total_affected}. No audit log scope cited."
    # Missing: audit_log_total_scanned in financial_impact; missing kcg_reference_loss_usd
    bad_summary["remediation_count"] = 5
    bad_summary["submission_date"] = "2024-11-12"
    # kcg_reference_loss_usd intentionally MISSING
    _wj(ws / "output" / "regulatory_submission_summary.json", dict(bad_summary))
    ok, _ = run_check("check_q14.py", ws); probes += 1; caught += (not ok)
    print(f"  q14 missing audit_log_total_scanned + kcg_reference_loss_usd -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q14
    import collections as _coll
    reg_summary2 = _coll.OrderedDict()
    reg_summary2["incident_date"] = "2024-11-03"
    reg_summary2["rule_violated"] = "Rule 15c3-5(b) (Market Access Rule) and Rule 15c6-1 (T+1 Settlement, effective 2024-05-28)"
    reg_summary2["financial_impact"] = (
        f"Total affected orders: {_total_affected} (ANOMALY_DST_MISMATCH). "
        f"Audit log scope: {_audit_log_total_scanned} entries scanned. "
        "T+1 settlement mis-classification due to 60-minute UTC offset error."
    )
    reg_summary2["remediation_count"] = 5
    reg_summary2["submission_date"] = "2024-11-12"
    reg_summary2_dict = dict(reg_summary2)
    reg_summary2_dict["kcg_reference_loss_usd"] = 460000000
    _wj(ws / "output" / "regulatory_submission_summary.json", reg_summary2_dict)

    # Probe 12: q5 missing case_number field
    _wj(ws / "output" / "kcg_anchor_check.json", {
        "financial_loss_usd": 460000000,
        "penalty_usd": 12000000,
        "rule_violated": "Rule 15c3-5(b)",
        "servers_count": 8,
        "pre_market_emails": 97,
        "shares_traded_millions": 397.0,
        # case_number intentionally MISSING
    })
    ok, _ = run_check("check_q5.py", ws); probes += 1; caught += (not ok)
    print(f"  q5 missing case_number -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q5
    _wj(ws / "output" / "kcg_anchor_check.json", {
        "financial_loss_usd": 460000000,
        "penalty_usd": 12000000,
        "rule_violated": "Rule 15c3-5(b)",
        "servers_count": 8,
        "pre_market_emails": 97,
        "shares_traded_millions": 397.0,
        "case_number": "Admin. Proc. File No. 3-15570",
    })

    # Probe 13: q15 missing schema_version
    _wj(ws / "output" / "backtest_result.json", {
        "config_timezone_offset": -5,
        "trade_date": "2024-11-03",
        "simulated_settlement_utc": "2024-11-03T21:00:00Z",
        "expected_settlement_utc": "2024-11-03T21:00:00Z",
        "match": True,
        "script_version": "1.0-template",
        # schema_version intentionally MISSING
    })
    ok, _ = run_check("check_q15.py", ws); probes += 1; caught += (not ok)
    print(f"  q15 missing schema_version -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore q15 (and recompute q16 hash since backtest_result.json changed)
    _wj(ws / "output" / "backtest_result.json", {
        "config_timezone_offset": -5,
        "trade_date": "2024-11-03",
        "simulated_settlement_utc": "2024-11-03T21:00:00Z",
        "expected_settlement_utc": "2024-11-03T21:00:00Z",
        "match": True,
        "script_version": "1.0-template",
        "schema_version": "1.0",
    })
    # Recompute q16 final sign after restoring backtest_result.json
    f1_b2 = (ws / "output" / "backtest_result.json").read_bytes()
    f2_b2 = (ws / "output" / "corrective_action_plan.md").read_bytes()
    _w(ws / "output" / "final_submission_signoff.txt",
       "VERIFIED:" + hashlib.sha256(f1_b2 + f2_b2).hexdigest() + "\n")

    print(f"\nnegatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
