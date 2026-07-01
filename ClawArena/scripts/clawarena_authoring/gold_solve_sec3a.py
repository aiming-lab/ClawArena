#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_sec3a.py — sec3a 可解性审计（金标自检）。

在 workspace 的临时副本上模拟全部 update 生效后的状态，写出每一轮的「正确产物」，
然后运行全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再做一组反例（错误产物）抽样，断言 check 能 FAIL（不过松）。

用途：证明每个 ground-truth 可由真实数据解出、check 不过严也不过松。
运行：python scripts/clawarena_authoring/gold_solve_sec3a.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "sec3a"
UPD = DS / "openclaw" / "updates" / "sec3a"
SCRIPTS = DS / "eval" / "sec3a" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/sec3a_gold_ws")

# ── Ground truth constants (must match build_sec3a.py) ──────────────────────────
INCIDENT_DATE = "2024-11-03"
ERROR_WINDOW_START = "2024-11-03T14:00:00Z"
ERROR_WINDOW_END = "2024-11-03T15:00:00Z"
TZ_WRONG = -4
TZ_CORRECT = -5
KCG_LOSS_USD = 460_000_000
KCG_PENALTY_USD = 12_000_000
KCG_RULE = "Rule 15c3-5(b)"
KCG_SERVERS = 8
KCG_EMAILS = 97
KCG_SHARES = 397_000_000
KCG_CUSTOMER_ORDERS = 212
KCG_DATE = "2012-08-01"
T1_EFFECTIVE = "2024-05-28"
CME_SETTLE_WRONG_UTC = "2024-11-03T20:00:00Z"   # UTC-4 error
CME_SETTLE_CORRECT_UTC = "2024-11-03T21:00:00Z"  # correct EST
AFFECTED_COUNT = 87


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # 应用所有 update workspace 文件
    for upd_name, targets in [
        ("upd1_workspace", [
            ("sec_inquiry_letter_20241105.md", "regulatory/sec_inquiry_letter_20241105.md"),
            ("affected_orders_detail.csv", "incident/affected_orders_detail.csv"),
        ]),
        ("upd2_workspace", [
            ("legal_counsel_memo_20241106.md", "regulatory/legal_counsel_memo_20241106.md"),
            ("revised_field_spec_v2.md", "regulatory/revised_field_spec_v2.md"),
            ("vwap_reference_20241103.csv", "incident/vwap_reference_20241103.csv"),
        ]),
        ("upd3_workspace", [
            ("sec_backtest_template.py", "regulatory/sec_backtest_template.py"),
            ("sec_formal_investigation_notice_20241107.md",
             "regulatory/sec_formal_investigation_notice_20241107.md"),
            ("compliance_remediation_matrix.csv", "regulatory/compliance_remediation_matrix.csv"),
        ]),
    ]:
        ud = UPD / upd_name
        if not ud.exists():
            continue
        for fname, target in targets:
            src = ud / fname
            dst = GOLD / target
            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(src, dst)
    return GOLD


def _w(p: Path, t: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _count_aros_log_entries_in_window(ws: Path) -> int:
    """Count AROS log entries with timestamp_utc_reported in 14:00-15:00 UTC."""
    log_path = ws / "incident" / "aros_v4_2_audit_log.jsonl"
    if not log_path.exists():
        return 0
    count = 0
    for line in log_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            rec = json.loads(line)
            ts = str(rec.get("timestamp_utc_reported", ""))
            # Window: 14:00:00 to 14:59:59 UTC (inclusive start, exclusive 15:00)
            m = re.match(r"2024-11-03T(\d{2}):", ts)
            if m and int(m.group(1)) == 14:
                count += 1
        except (json.JSONDecodeError, ValueError):
            pass
    return count


def _count_detail_csv_rows(ws: Path) -> int:
    """Count data rows in affected_orders_detail.csv."""
    p = ws / "incident" / "affected_orders_detail.csv"
    if not p.exists():
        return 0
    count = 0
    header_seen = False
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("#") or not line.strip():
            continue
        if not header_seen:
            header_seen = True
            continue
        count += 1
    return count


def solve(ws: Path) -> None:
    out = ws / "output"
    out.mkdir(exist_ok=True)

    # ── q1: 事故时间线 ───────────────────────────────────────────────────────────
    _wj(out / "incident_timeline_v1.json", {
        "schema_version": "1.0",
        "incident_date": INCIDENT_DATE,
        "error_window_utc_start": ERROR_WINDOW_START,
        "error_window_utc_end": ERROR_WINDOW_END,
        "timezone_offset_applied": TZ_WRONG,
        "correct_timezone_offset": TZ_CORRECT,
    })

    # ── q2: 时区 bug 报告 ────────────────────────────────────────────────────────
    _w(out / "timezone_bug_report.md",
       "# AROS v4.2 Timezone Bug Report\n\n"
       "**File**: `code/aros/timezone_config.py`\n"
       "**Line 47**: `UTC_OFFSET = -4`  ← BUG: hard-coded EDT offset not updated for DST\n\n"
       "## Error Details\n\n"
       "- **Incorrect value**: UTC-4 (EDT, valid only during summer)\n"
       "- **Correct value**: UTC-5 (EST, valid from November DST transition)\n"
       "- **Impact**: All timestamps 1 hour early; CME settlement calculated at "
       "20:00:00 UTC instead of correct 21:00:00 UTC\n\n"
       "## Affected Function\n\n"
       "The function `get_cme_settle_utc()` in `timezone_config.py` returns '20:00:00' "
       "when the correct EST value is '21:00:00'.\n\n"
       "## Fix\n\n"
       "Change line 47 from `UTC_OFFSET = -4` to `UTC_OFFSET = -5`.\n"
       "Long-term: implement automatic DST detection (JIRA AROS-447).\n"
    )

    # ── q3: 受影响订单数 ─────────────────────────────────────────────────────────
    aros_count = _count_aros_log_entries_in_window(ws)
    # 精确值：aros_v4_2_audit_log.jsonl 中 timestamp_utc_reported 在 [14:00,15:00) 的条目恰好 39 条
    _wj(out / "affected_orders_count.json", {
        "schema_version": "1.0",
        "total_affected": aros_count,  # exact count = 39
        "time_window_utc_start": ERROR_WINDOW_START,
        "time_window_utc_end": ERROR_WINDOW_END,
    })

    # ── q4: Bot 摘要失真识别 ──────────────────────────────────────────────────────
    _wj(out / "bot_summary_errors.json", {
        "schema_version": "1.0",
        "errors": [
            {
                "field": "kcg_financial_loss",
                "claimed_value": "$440M",
                "correct_value": "$460M+",
                "source": "SEC Release No. 34-70694 and SEC press release 2013-222",
            },
            {
                "field": "utc_offset_error_magnitude",
                "claimed_value": "30 minutes",
                "correct_value": "60 minutes (1 hour)",
                "source": "code/aros/timezone_config.py line 47: UTC_OFFSET = -4 vs correct -5",
            },
            {
                "field": "affected_order_count",
                "claimed_value": "63",
                "correct_value": "87",
                "source": "incident/position_delta_report.csv full analysis",
            },
        ],
    })

    # ── q5: KCG 锚点核查表 ───────────────────────────────────────────────────────
    _wj(out / "kcg_anchor_check.json", {
        "schema_version": "1.0",
        "financial_loss_usd": KCG_LOSS_USD,
        "penalty_usd": KCG_PENALTY_USD,
        "rule_violated": KCG_RULE,
        "servers_count": KCG_SERVERS,
        "pre_market_emails": KCG_EMAILS,
        "shares_traded": KCG_SHARES,
        "customer_orders": KCG_CUSTOMER_ORDERS,
        "incident_date": KCG_DATE,
    })

    # ── q6: 废弃版本识别 ─────────────────────────────────────────────────────────
    _wj(out / "legacy_code_assessment.json", {
        "is_applicable": False,
        "reason": (
            "aros_v3_1_router_DEPRECATED.py is DEPRECATED as of 2024-01-15 and superseded "
            "by AROS v4.2. It does not support T+1 settlement (Rule 15c6-1 effective "
            "2024-05-28) or MiFIR Field 28 reporting. Although it contains UTC_OFFSET = -5, "
            "its Python 2-era timezone handling is incompatible with v4.2 and it was "
            "explicitly marked DEPRECATED — it must not be used for current incident remediation."
        ),
        "recommendation": (
            "All fixes must be applied to the current AROS v4.2 codebase "
            "(code/aros/timezone_config.py). Change UTC_OFFSET from -4 to -5 "
            "and implement automatic DST detection. Do not reference the deprecated v3.1 files."
        ),
    })

    # ── q7: MiFIR Field 28 修正报告 ──────────────────────────────────────────────
    _w(out / "mifir_field28_correction.md",
       "# MiFIR Field 28 Timestamp Error — Formal Correction Report\n\n"
       "## Error Description\n\n"
       "On 2024-11-03, ArtemisQ Capital's AROS v4.2 system submitted MiFIR transaction reports "
       "with **Field 28** (trading date and time) timestamps using UTC-4 offset (EDT) instead "
       "of UTC-5 (EST, the correct offset after the DST transition). This resulted in all "
       "Field 28 values being 1 hour early relative to UTC.\n\n"
       "## Regulatory Citation\n\n"
       "Per **FCA Market Watch 59** (April 2019), Field 28 (trading date and time) must be "
       "reported in **UTC** (Coordinated Universal Time) as required by MiFIR Article 26 and "
       "**RTS 22** (Regulatory Technical Standard 22). The FCA specifically identified "
       "DST transition errors as a common compliance failure under RTS 22. The error observed "
       "at ArtemisQ Capital matches precisely the pattern described in Market Watch 59: a "
       "hard-coded timezone offset not updated after the autumn DST clock change.\n\n"
       "## DST Transition Context\n\n"
       "On November 3, 2024 at 02:00 ET, US clocks fell back from EDT (UTC-4) to EST (UTC-5). "
       "AROS v4.2 did not update its hard-coded UTC_OFFSET, causing all Field 28 timestamps "
       "to be reported as UTC-4 instead of the correct UTC-5 throughout the trading day.\n\n"
       "## Correction Plan\n\n"
       "1. Resubmit all 2024-11-03 transaction reports with corrected Field 28 timestamps "
       "(UTC-5 applied)\n"
       "2. Fix timezone_config.py: set UTC_OFFSET = -5 (EST)\n"
       "3. Implement automatic DST detection to prevent recurrence\n"
       "4. Test timezone handling at each DST transition per FCA Market Watch 59 and RTS 22 guidance\n\n"
       "## Action Items\n\n"
       "- Submit corrected reports within 10 business days per FCA requirement\n"
       "- Implement automated UTC timestamp validation in AROS reporting pipeline\n"
       "- Add DST transition test to CI/CD pipeline\n"
    )

    # ── q8: T+1 结算截止时间偏移 ─────────────────────────────────────────────────
    _wj(out / "t1_settlement_impact.json", {
        "schema_version": "1.0",
        "rule_effective_date": T1_EFFECTIVE,
        "incorrect_cutoff_utc": CME_SETTLE_WRONG_UTC,
        "correct_cutoff_utc": CME_SETTLE_CORRECT_UTC,
        "offset_minutes": 60,
    })

    # ── q9: 根因分析 ─────────────────────────────────────────────────────────────
    aros_count_for_rca = max(aros_count, 1)
    _w(out / "root_cause_analysis.md",
       f"# Root Cause Analysis — AROS v4.2 Incident\n\n"
       f"**incident_date**: {INCIDENT_DATE}\n\n"
       f"## root_cause\n\n"
       f"Hard-coded `UTC_OFFSET = -4` in `code/aros/timezone_config.py` (line 47). "
       f"After the 2024-11-03 DST transition, the correct value is UTC-5 (EST). "
       f"The -1 hour discrepancy (UTC-4 vs UTC-5) propagated through all time-sensitive "
       f"operations including T+1 settlement deadline calculation and MiFIR Field 28 reporting.\n\n"
       f"## contributing_factors\n\n"
       f"1. Manual DST configuration update process with no automated verification\n"
       f"2. `risk_monitor.py` not integrated with `order_router.py` (Rule 15c3-5(b) compliance gap)\n"
       f"3. No deployment checklist for DST transition procedures (cf. KCG 2012: 97 alert emails ignored)\n"
       f"4. No automated UTC timestamp validation in the reporting pipeline\n\n"
       f"## timeline\n\n"
       f"- 2024-11-03T06:00:00Z: DST transition; AROS retains UTC-4\n"
       f"- 2024-11-03T{ERROR_WINDOW_START[11:]}: AROS error window begins (T+1 deadline miscalculation)\n"
       f"- 2024-11-03T{ERROR_WINDOW_END[11:]}: AROS error window ends\n"
       f"- 2024-11-03T{CME_SETTLE_WRONG_UTC[11:]}: AROS calculates CME settle (WRONG; correct is {CME_SETTLE_CORRECT_UTC[11:]})\n\n"
       f"## financial_impact\n\n"
       f"Approximately **{aros_count_for_rca} orders** affected within the 14:00-15:00 UTC window "
       f"(per incident log analysis). This is an ArtemisQ Capital-specific impact.\n\n"
       f"**Reference (KCG 2012)**: Knight Capital Americas LLC suffered a financial loss of "
       f"**$460,000,000** (SEC-confirmed) due to an analogous deployment control failure. "
       f"The KCG civil money penalty was $12,000,000 under Rule 15c3-5(b).\n\n"
       f"## regulatory_violations\n\n"
       f"- **Rule 15c3-5(b)** (Market Access Rule): risk_monitor.py not integrated with order routing; "
       f"pre-trade risk controls not applied to all AROS orders.\n"
       f"- **Rule 15c6-1** (T+1 Settlement, effective 2024-05-28): settlement deadline miscalculated "
       f"by 60 minutes due to DST offset error.\n"
       f"- **MiFIR RTS 22 Field 28**: UTC timestamps incorrectly reported (UTC-4 used instead of UTC-5).\n"
    )

    # ── q10: SEC 应答框架（Update 1 — uses original price_diff_usd field） ────────
    detail_count = _count_detail_csv_rows(ws)
    _wj(out / "sec_response_framework.json", {
        "schema_version": "1.0",
        "deadline_utc": "2024-11-07T09:00:00Z",
        "required_fields": [
            "order_id",
            "expected_settlement_utc",
            "actual_settlement_utc",
            "price_diff_usd",
        ],
        "affected_order_count_from_detail": detail_count if detail_count > 0 else AFFECTED_COUNT,
    })

    # ── q11: 订单级别差异报告（Update 2 supersede — price_diff_vwap_usd）──────────
    detail_path = ws / "incident" / "affected_orders_detail.csv"
    if detail_path.exists():
        # Read source CSV and build output with correct field names
        rows_out = []
        header_seen = False
        reader_rows = []
        for line in detail_path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("#") or not line.strip():
                continue
            reader_rows.append(line)
        if reader_rows:
            import io
            reader = csv.DictReader(io.StringIO("\n".join(reader_rows)))
            for r in reader:
                rows_out.append(r)
    else:
        rows_out = []
        import random
        rng = random.Random(20241105)
        for i in range(AFFECTED_COUNT):
            rows_out.append({
                "order_id": f"AROS-{20241103000 + i:012d}",
                "expected_settlement_utc": "2024-11-04T21:00:00Z",
                "actual_settlement_utc": "2024-11-04T22:00:00Z",
                "price_diff_vwap_usd": str(round(rng.uniform(-500, 500), 2)),
            })

    # Write CSV with superseded field name price_diff_vwap_usd
    diff_path = out / "order_level_diff_report.csv"
    diff_path.parent.mkdir(parents=True, exist_ok=True)
    with diff_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=[
            "order_id", "expected_settlement_utc", "actual_settlement_utc", "price_diff_vwap_usd"
        ])
        writer.writeheader()
        for r in rows_out[:AFFECTED_COUNT]:
            writer.writerow({
                "order_id": r.get("order_id", ""),
                "expected_settlement_utc": r.get("expected_settlement_utc", "2024-11-04T21:00:00Z"),
                "actual_settlement_utc": r.get("actual_settlement_utc", "2024-11-04T22:00:00Z"),
                "price_diff_vwap_usd": r.get("price_diff_vwap_usd", r.get("price_diff_usd", "0.00")),
            })

    # ── q12: SHA-256 sign-off ────────────────────────────────────────────────────
    digest_q12 = hashlib.sha256(diff_path.read_bytes()).hexdigest()
    _w(out / "report_signoff.txt", f"VERIFIED:{digest_q12}\n")

    # ── q13: 合规整改计划 ─────────────────────────────────────────────────────────
    _w(out / "corrective_action_plan.md",
       "# Corrective Action Plan — AROS v4.2 Incident\n\n"
       f"**incident_ref**: {INCIDENT_DATE}\n\n"
       "## root_cause_summary\n\n"
       "Hard-coded UTC_OFFSET = -4 in timezone_config.py was not updated for the 2024-11-03 "
       "DST transition, causing a 1-hour error in all time-sensitive operations. "
       "Additionally, risk_monitor.py is not integrated with order_router.py, creating "
       "a Rule 15c3-5(b) pre-trade risk controls gap.\n\n"
       "## remediation_items\n\n"
       "### Item 1 — Timezone Automation\n"
       "- **action**: Implement automatic DST-aware timezone detection in timezone_config.py "
       "(remove hard-coded UTC_OFFSET; use Python zoneinfo.ZoneInfo('America/New_York'))\n"
       "- **owner**: Marcus Chen (Lead Quant Engineer)\n"
       "- **deadline_days**: 7\n\n"
       "### Item 2 — Risk Monitor Integration (Rule 15c3-5(b) Compliance)\n"
       "- **action**: Integrate risk_monitor.py into order_router.py order flow so that "
       "all orders pass through pre-trade risk controls before routing, as required by "
       "Rule 15c3-5(b) (Market Access Rule)\n"
       "- **owner**: Marcus Chen (Lead Quant Engineer)\n"
       "- **deadline_days**: 14\n\n"
       "### Item 3 — Deployment Checklist (KCG Lesson)\n"
       "- **action**: Create a written deployment checklist (inspired by Knight Capital 2012 case study "
       "lessons) covering DST transition verification, post-deployment checks for each server, "
       "and alert escalation procedures for pre-market warnings\n"
       "- **owner**: James Okafor (DevOps Lead)\n"
       "- **deadline_days**: 21\n\n"
       "### Item 4 — MiFIR Field 28 Corrected Submissions\n"
       "- **action**: Resubmit all 2024-11-03 transaction reports with corrected Field 28 "
       "timestamps (UTC-5 applied), per FCA Market Watch 59 guidance\n"
       "- **owner**: Dr. Sarah Kim (Legal Counsel)\n"
       "- **deadline_days**: 10\n\n"
       "### Item 5 — T+1 Settlement Validation (Rule 15c6-1)\n"
       "- **action**: Fix settlement_scheduler.py to use UTC-5 (EST) offset for T+1 "
       "deadline calculations post-November DST; add automated test validating correct "
       "settlement deadline matches Rule 15c6-1 (effective 2024-05-28)\n"
       "- **owner**: Marcus Chen (Lead Quant Engineer)\n"
       "- **deadline_days**: 7\n\n"
       "### Item 6 — CEO Annual Certification (Rule 15c3-5(e))\n"
       "- **action**: Prepare and obtain CEO certification for Rule 15c3-5(b) compliance "
       "per Rule 15c3-5(e) annual certification requirement\n"
       "- **owner**: Dr. Elena Vasquez (CCO)\n"
       "- **deadline_days**: 60\n"
    )

    # ── q14: 监管提交摘要（P5 字段顺序固定）────────────────────────────────────────
    # Must use OrderedDict-style via ordered Python dict (Python 3.7+ preserves insertion order)
    sub_data = {}
    sub_data["incident_date"] = INCIDENT_DATE
    sub_data["rule_violated"] = KCG_RULE  # "Rule 15c3-5(b)"
    sub_data["financial_impact"] = (
        f"39 orders in the 14:00-15:00 UTC AROS error window (from aros_v4_2_audit_log.jsonl); "
        f"87 total orders in position_delta_report.csv affected by DST offset error; "
        f"CME settlement cutoff error of 60 minutes (UTC-4 vs UTC-5). "
        f"KCG reference penalty: $12,000,000 (SEC Release No. 34-70694, Rule 15c3-5(b) violation)."
    )
    sub_data["remediation_count"] = 6
    sub_data["submission_date"] = "2024-11-07"
    sub_data["schema_version"] = "1.0"
    _wj(out / "regulatory_submission_summary.json", sub_data)

    # ── q15: 回测结果 ─────────────────────────────────────────────────────────────
    _wj(out / "backtest_result.json", {
        "schema_version": "1.0",
        "config_timezone_offset": TZ_CORRECT,      # -5
        "simulated_settlement_utc": CME_SETTLE_CORRECT_UTC,  # "2024-11-03T21:00:00Z"
        "expected_settlement_utc": CME_SETTLE_CORRECT_UTC,
        "match": True,
        "script_version": "sec_backtest_v1",
    })

    # ── q16: 最终提交签名（backtest + CAP 拼接后 SHA-256）───────────────────────────
    backtest_bytes = (out / "backtest_result.json").read_bytes()
    cap_bytes = (out / "corrective_action_plan.md").read_bytes()
    digest_q16 = hashlib.sha256(backtest_bytes + cap_bytes).hexdigest()
    _w(out / "final_submission_signoff.txt", f"VERIFIED:{digest_q16}\n")


# ── 运行 check ──────────────────────────────────────────────────────────────────
EVAL_CMDS = {
    "q1":  ["check_q1.py",  ("pref", "P1,P2", "output/incident_timeline_v1.json")],
    "q2":  ["check_q2.py"],
    "q3":  ["check_q3.py",  ("pref", "P1,P2", "output/affected_orders_count.json")],
    "q4":  ["check_q4.py",  ("pref", "P1,P2", "output/bot_summary_errors.json")],
    "q5":  ["check_q5.py",  ("pref", "P1,P2", "output/kcg_anchor_check.json")],
    "q6":  ["check_q6.py"],
    "q7":  ["check_q7.py",  ("pref", "P3", "output/mifir_field28_correction.md")],
    "q8":  ["check_q8.py",  ("pref", "P1,P2", "output/t1_settlement_impact.json")],
    "q9":  ["check_q9.py",  ("pref", "P3", "output/root_cause_analysis.md")],
    "q10": ["check_q10.py", ("pref", "P1,P2", "output/sec_response_framework.json")],
    "q11": ["check_q11.py"],
    "q12": ["check_q12.py"],
    "q13": ["check_q13.py", ("pref", "P3,P4", "output/corrective_action_plan.md")],
    "q14": ["check_q14.py", ("pref", "P1,P2,P3,P5", "output/regulatory_submission_summary.json")],
    "q15": ["check_q15.py", ("pref", "P1,P2", "output/backtest_result.json")],
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
    last = (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr) else ""
    return r.returncode == 0, last


def main():
    ws = prep_workspace()
    solve(ws)
    print("=== GOLD SOLUTION: every check must PASS ===")
    n_pass = n_fail = 0
    for q, items in EVAL_CMDS.items():
        for it in items:
            ok, last = run_check(it, ws)
            tag = f"pref {it[1]}" if isinstance(it, tuple) else "main"
            status = "PASS" if ok else "FAIL"
            if ok:
                n_pass += 1
            else:
                n_fail += 1
                print(f"  [{status}] {q} ({tag}): {last}")
    print(f"gold: {n_pass} checks PASSED, {n_fail} FAILED")

    # ── 反例抽样（错误产物须 FAIL）────────────────────────────────────────────────
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    def probe(label, q_key, item, modify_fn):
        nonlocal probes, caught
        modify_fn()
        ok, _ = run_check(item, ws)
        probes += 1
        caught += (not ok)
        print(f"  {label} -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 1. q1: wrong timezone offset (-3 instead of -4)
    probe(
        "q1 wrong tz_applied=-3",
        "q1", "check_q1.py",
        lambda: _wj(ws / "output" / "incident_timeline_v1.json", {
            "schema_version": "1.0",
            "incident_date": INCIDENT_DATE,
            "error_window_utc_start": ERROR_WINDOW_START,
            "error_window_utc_end": ERROR_WINDOW_END,
            "timezone_offset_applied": -3,
            "correct_timezone_offset": TZ_CORRECT,
        })
    )

    # 1b. q3: wrong total_affected (87 from detail CSV, not 39 from AROS log)
    probe(
        "q3 total_affected=87 (wrong: detail CSV count, not AROS log window count)",
        "q3", "check_q3.py",
        lambda: _wj(ws / "output" / "affected_orders_count.json", {
            "schema_version": "1.0",
            "total_affected": 87,   # WRONG — should be 39 from AROS log
            "time_window_utc_start": ERROR_WINDOW_START,
            "time_window_utc_end": ERROR_WINDOW_END,
        })
    )

    # 1c. q7: missing UTC-4 explicit mention
    probe(
        "q7 missing UTC-4 explicit mention",
        "q7", "check_q7.py",
        lambda: _w(
            ws / "output" / "mifir_field28_correction.md",
            "# MiFIR Field 28 Correction\n\n"
            "The incorrect timezone offset caused Field 28 timestamps to be wrong. "
            "The correct offset is UTC-5 (EST). FCA Market Watch 59 requires UTC reporting. "
            "DST transition caused the error on 2024-11-03.\n"
        )
    )

    # 2. q5: decoy $440M loss figure
    probe(
        "q5 KCG loss $440M decoy",
        "q5", "check_q5.py",
        lambda: _wj(ws / "output" / "kcg_anchor_check.json", {
            "schema_version": "1.0",
            "financial_loss_usd": 440_000_000,  # WRONG
            "penalty_usd": KCG_PENALTY_USD,
            "rule_violated": KCG_RULE,
            "servers_count": KCG_SERVERS,
            "pre_market_emails": KCG_EMAILS,
            "shares_traded": KCG_SHARES,
            "customer_orders": KCG_CUSTOMER_ORDERS,
            "incident_date": KCG_DATE,
        })
    )

    # 2b. q5: wrong shares_traded (common approximation 400M instead of 397M)
    probe(
        "q5 shares_traded=400000000 (wrong approximation)",
        "q5", "check_q5.py",
        lambda: _wj(ws / "output" / "kcg_anchor_check.json", {
            "schema_version": "1.0",
            "financial_loss_usd": KCG_LOSS_USD,
            "penalty_usd": KCG_PENALTY_USD,
            "rule_violated": KCG_RULE,
            "servers_count": KCG_SERVERS,
            "pre_market_emails": KCG_EMAILS,
            "shares_traded": 400_000_000,   # WRONG — correct is 397,000,000
            "customer_orders": KCG_CUSTOMER_ORDERS,
            "incident_date": KCG_DATE,
        })
    )

    # 3. q8: wrong offset_minutes=30 (bot decoy)
    probe(
        "q8 offset_minutes=30 (bot decoy)",
        "q8", "check_q8.py",
        lambda: _wj(ws / "output" / "t1_settlement_impact.json", {
            "schema_version": "1.0",
            "rule_effective_date": T1_EFFECTIVE,
            "incorrect_cutoff_utc": CME_SETTLE_WRONG_UTC,
            "correct_cutoff_utc": CME_SETTLE_CORRECT_UTC,
            "offset_minutes": 30,  # WRONG
        })
    )

    # 4. q11: uses old superseded field name price_diff_usd
    def _write_old_field_csv():
        diff_path = ws / "output" / "order_level_diff_report.csv"
        diff_path.parent.mkdir(parents=True, exist_ok=True)
        import random
        rng = random.Random(999)
        with diff_path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=[
                "order_id", "expected_settlement_utc", "actual_settlement_utc", "price_diff_usd"  # OLD
            ])
            writer.writeheader()
            for i in range(AFFECTED_COUNT):
                writer.writerow({
                    "order_id": f"AROS-{20241103000 + i:012d}",
                    "expected_settlement_utc": "2024-11-04T21:00:00Z",
                    "actual_settlement_utc": "2024-11-04T22:00:00Z",
                    "price_diff_usd": str(round(rng.uniform(-500, 500), 2)),
                })
    probe(
        "q11 uses superseded field price_diff_usd",
        "q11", "check_q11.py",
        _write_old_field_csv
    )

    # 5. q12: placeholder hash after restoring correct CSV
    solve_csv_again = True
    if solve_csv_again:
        # Restore the correct CSV first, then write bad signoff
        diff_path = ws / "output" / "order_level_diff_report.csv"
        # Regenerate correct CSV
        detail_path = ws / "incident" / "affected_orders_detail.csv"
        rows_out = []
        if detail_path.exists():
            import io as _io
            reader_rows = []
            for line in detail_path.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("#") or not line.strip():
                    continue
                reader_rows.append(line)
            if reader_rows:
                reader = csv.DictReader(_io.StringIO("\n".join(reader_rows)))
                for r in reader:
                    rows_out.append(r)
        with diff_path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=[
                "order_id", "expected_settlement_utc", "actual_settlement_utc", "price_diff_vwap_usd"
            ])
            writer.writeheader()
            for r in rows_out[:AFFECTED_COUNT]:
                writer.writerow({
                    "order_id": r.get("order_id", ""),
                    "expected_settlement_utc": r.get("expected_settlement_utc", "2024-11-04T21:00:00Z"),
                    "actual_settlement_utc": r.get("actual_settlement_utc", "2024-11-04T22:00:00Z"),
                    "price_diff_vwap_usd": r.get("price_diff_vwap_usd", r.get("price_diff_usd", "0.00")),
                })

    probe(
        "q12 placeholder hash 0*64",
        "q12", "check_q12.py",
        lambda: _w(ws / "output" / "report_signoff.txt", "VERIFIED:" + "0" * 64 + "\n")
    )

    # 6. q15: wrong config_timezone_offset=-4 (the bug, not the fix)
    probe(
        "q15 config_timezone_offset=-4 (unfixed)",
        "q15", "check_q15.py",
        lambda: _wj(ws / "output" / "backtest_result.json", {
            "schema_version": "1.0",
            "config_timezone_offset": -4,   # WRONG — should be -5
            "simulated_settlement_utc": CME_SETTLE_WRONG_UTC,  # 20:00 (wrong)
            "expected_settlement_utc": CME_SETTLE_CORRECT_UTC,
            "match": False,
            "script_version": "sec_backtest_v1",
        })
    )

    # 7. q16: placeholder final hash
    # Restore correct backtest result first
    _wj(ws / "output" / "backtest_result.json", {
        "schema_version": "1.0",
        "config_timezone_offset": TZ_CORRECT,
        "simulated_settlement_utc": CME_SETTLE_CORRECT_UTC,
        "expected_settlement_utc": CME_SETTLE_CORRECT_UTC,
        "match": True,
        "script_version": "sec_backtest_v1",
    })
    probe(
        "q16 placeholder final hash 0*64",
        "q16", "check_q16.py",
        lambda: _w(ws / "output" / "final_submission_signoff.txt", "VERIFIED:" + "0" * 64 + "\n")
    )

    # 8. q7: missing RTS 22 citation (has all else correct but omits the technical standard)
    probe(
        "q7 missing RTS 22 citation (has UTC-4/UTC-5/Field28/MarketWatch59 but not RTS 22)",
        "q7", "check_q7.py",
        lambda: _w(
            ws / "output" / "mifir_field28_correction.md",
            "# MiFIR Field 28 Timestamp Error — Formal Correction Report\n\n"
            "On 2024-11-03, AROS v4.2 reported Field 28 timestamps using UTC-4 instead of "
            "UTC-5 (EST). This violates FCA Market Watch 59 requirements. DST transition was "
            "not handled correctly. The incorrect offset UTC-4 must be replaced with UTC-5.\n"
            "FCA action: resubmit corrected reports.\n"
        )
    )

    # 9. q14: financial_impact missing '39' (uses 87 but not 39 from AROS log window)
    probe(
        "q14 financial_impact references 87 but omits AROS window count 39",
        "q14", "check_q14.py",
        lambda: _wj(ws / "output" / "regulatory_submission_summary.json", {
            "incident_date": INCIDENT_DATE,
            "rule_violated": KCG_RULE,
            "financial_impact": (
                "87 orders affected; CME settlement cutoff error of 60 minutes "
                "(UTC-4 vs UTC-5). KCG reference penalty: $12,000,000."
            ),
            "remediation_count": 6,
            "submission_date": "2024-11-07",
            "schema_version": "1.0",
        })
    )

    print(f"negatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
