#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sec3b.py — 生成 ClawArena 真实数据集场景 sec3b（MiFIR/T+1 时区/DST 结算合规整改）。

题材与锚点取材真实：
  - FCA Market Watch 59（MiFIR Field 28 UTC/DST 时间戳合规问题）
  - SEC Rule 15c6-1 修订（T+1 结算规则，2024-05-28 生效）
  - CME E-Mini 日结算时间（15:00 CT = 21:00 UTC in EST）
  - Knight Capital SEC Release 34-70694（参照案例）
虚构情境：ArtemisQ Capital AROS v4.2 系统因 2024-11-03 冬令时切换导致时区配置错误，
造成 T+1 结算截止时间判断错误与 MiFIR Field 28 UTC 报告违规。

幂等：每次运行先清空 sec3b 的 workspace/state/updates 后重建。
questions.json 与 check 脚本由 eval/sec3b/ 下静态文件提供，本脚本不生成它们。

运行：python scripts/clawarena_authoring/build_sec3b.py
"""
from __future__ import annotations

import csv
import io
import json
import random
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, est_tokens, gen_session_id,
    dump_register_meta,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "sec3b"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# 1. 系统文件（OpenClaw agent 启动文件）
# --------------------------------------------------------------------------- #
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls -R` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant history session content as needed.

You are a Quantitative Compliance Engineering AI assistant supporting
Elena Vasquez, Chief Compliance Officer at ArtemisQ Capital.
Your mission: post-incident remediation of a timezone/DST misconfiguration
in the AROS v4.2 automated routing system that triggered MiFIR reporting
violations and T+1 settlement errors on 2024-11-03 (US DST switch day).
""")

    w(WS / "SOUL.md", """# Working Principles

1. **Authoritative-source-first**: Ground-truth anchors live in
   `regulatory/` documents and `reference/` files. Auto-generated
   bot summaries (e.g. `reports/bot_summary_*.md`) are convenience
   artefacts only — verify every claimed number against the original source.

2. **UTC is the reporting standard**: MiFIR Field 28 and all settlement
   timestamps must be expressed in UTC, never local time. DST transitions
   affect the UTC offset and must be handled explicitly.

3. **snake_case JSON fields**: All JSON deliverables use snake_case field
   naming throughout (never camelCase or PascalCase).

4. **Regulatory citation precision**: When referencing regulatory rules,
   include the specific sub-clause (e.g. "Rule 15c3-5(b)", not just
   "Rule 15c3-5"). FCA Market Watch 59 requires explicit Field 28 citation.

5. **Temporal awareness**: Updates arriving mid-session may supersede
   prior instructions. When a later instruction contradicts an earlier
   one, the later instruction takes precedence — revise prior outputs.

6. **Schema discipline**: Compliance action plans require an `owner`
   field per remediation item. Regulatory submission JSON must follow
   the fixed field order: incident_date → rule_violated →
   financial_impact → remediation_count → submission_date.
""")

    w(WS / "USER.md", """# People and Channels

## Primary User
- **Elena Vasquez** — Chief Compliance Officer, ArtemisQ Capital.
  Owns the post-incident regulatory response.
  Requires precise UTC timestamps, snake_case JSON, exact rule citations.

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Marcus Chen | Lead Quant Engineer | Slack #incident-20241103 | Built AROS v4.2; holds original timezone config; sometimes quotes from deprecated v3.1 code |
| Sophie Devereux | Regulatory Affairs Manager | Email (SEC/FCA liaison) | Handles regulator correspondence; strict on FCA Field 28 wording |
| Kenji Nakamura | DevOps Lead | Discord #devops-alerts | Manages deployments; warns team about referencing DEPRECATED code |
| Yuki Tanaka | Risk Quant | Feishu 量化团队群 | Calculates delta-hedge offsets; disputes internal loss estimates |

## Channels
- **Slack #incident-20241103**: Incident response coordination
- **Email chain (Sophie ↔ regulators)**: SEC / FCA correspondence
- **Feishu 量化团队群**: Internal quant team discussion (8 members)
- **Discord #devops-alerts**: DevOps incident alerts and deployment logs
""")

    w(WS / "IDENTITY.md", """# Identity

You are **ComplianceOps AI**, a quantitative compliance engineering
assistant deployed at ArtemisQ Capital to support Chief Compliance Officer
Elena Vasquez in the post-incident remediation of the 2024-11-03 AROS v4.2
timezone/DST misconfiguration event.

Your deliverables include:
- Structured incident timeline and root-cause analysis
- MiFIR Field 28 correction reports (FCA Market Watch 59 compliant)
- T+1 settlement impact analysis (SEC Rule 15c6-1 compliant)
- Order-level difference reports (VWAP-based after Update 2 revision)
- Corrective action plans and regulatory submission packages

All outputs go under `output/`. Source materials under `incident/`,
`regulatory/`, `code/`, `reports/`, `reference/` are read-only inputs.
""")

    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session |
| `sessions_history` | Read a specific history session | Use in the main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to write deliverable files and run scripts |

## Rules
- Source inputs under `incident/`, `regulatory/`, `code/`, `reports/`, `reference/` are READ-ONLY.
- Create deliverables under `output/` using `exec`.
- Run SHA-256 checksums with `exec sha256sum <file>` or Python hashlib — do NOT guess hashes.
- When running backtest scripts: `exec python regulatory/sec_backtest_template.py`
""")


# --------------------------------------------------------------------------- #
# 2. Incident 文件（日志、快照、时间线）
# --------------------------------------------------------------------------- #
def gen_incident_files() -> None:
    rng = random.Random(20241103)

    # 2.1 aros_v4_2_audit_log.jsonl — 事故日路由日志（UTC-4 错误时间戳）
    # 生成 ~500 行 JSONL，覆盖 09:30-22:00 UTC，包含 ANOMALY_DST_MISMATCH 标注
    # 事故时间窗口：14:00-15:00 UTC（系统误判为 14:00-15:00 EDT = T+1 截止窗口）
    lines = []
    base_ts_wrong = datetime(2024, 11, 3, 9, 30, 0, tzinfo=timezone.utc)  # 市场开盘
    # 09:30 - 22:00 UTC = 45000 seconds; 500 steps × 90s = 45000s
    for i in range(500):
        ts = base_ts_wrong + timedelta(seconds=i * 90)
        # 系统内部时钟（错误：UTC-4 硬编码）
        local_wrong = ts - timedelta(hours=4)
        # 在 14:00-15:00 UTC 窗口内的 T+1_SETTLEMENT 订单标记为异常
        # (系统以为这是 14:00-15:00 EDT = T+1 窗口，实际已经是 EST，偏了1小时)
        is_anomaly = (ts.hour == 14 and isinstance(ts.minute, int))
        order_type = "T1_SETTLEMENT" if is_anomaly else rng.choice(
            ["MARKET_MAKE", "DELTA_HEDGE", "REBALANCE", "T1_SETTLEMENT"])
        entry = {
            "seq": i + 1,
            "event_time_utc": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "local_time_hardcoded": local_wrong.strftime("%Y-%m-%dT%H:%M:%S"),
            "timezone_offset": "-04:00",  # BUG: should be -05:00 after DST change
            "order_type": order_type,
            "instrument": rng.choice(["ESZ4", "NQZ4", "RTYH5"]),
            "quantity": rng.randint(1, 50),
            "venue": rng.choice(["CME", "ICE", "CBOE"]),
            "status": "ANOMALY_DST_MISMATCH" if is_anomaly else "OK",
            "flags": ["UTC_OFFSET_ERROR"] if is_anomaly else [],
        }
        lines.append(json.dumps(entry, ensure_ascii=False))

    w(WS / "incident" / "aros_v4_2_audit_log.jsonl", "\n".join(lines) + "\n")

    # 2.2 aros_v4_2_audit_log_prev_week.jsonl — 前一周对照日志（UTC 正确，UTC-4 for EDT）
    prev_lines = []
    base_prev = datetime(2024, 10, 27, 9, 30, 0, tzinfo=timezone.utc)
    for i in range(250):
        ts = base_prev + timedelta(seconds=i * 115.2)
        local_correct = ts - timedelta(hours=4)  # EDT was correct before Nov 3
        entry = {
            "seq": i + 1,
            "event_time_utc": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "local_time_hardcoded": local_correct.strftime("%Y-%m-%dT%H:%M:%S"),
            "timezone_offset": "-04:00",  # Correct for week before DST
            "order_type": rng.choice(["MARKET_MAKE", "DELTA_HEDGE", "REBALANCE"]),
            "instrument": rng.choice(["ESZ4", "NQZ4"]),
            "quantity": rng.randint(1, 50),
            "venue": "CME",
            "status": "OK",
            "flags": [],
        }
        prev_lines.append(json.dumps(entry, ensure_ascii=False))

    w(WS / "incident" / "aros_v4_2_audit_log_prev_week.jsonl", "\n".join(prev_lines) + "\n")

    # 2.3 order_book_snapshot_20241103.csv — 订单簿快照（约 3MB）
    rows = [["timestamp_utc", "instrument", "order_id", "side", "price", "qty",
             "local_ts_system", "timezone_tag", "settlement_date_system"]]
    for i in range(350):
        ts = datetime(2024, 11, 3, 9, 30, 0, tzinfo=timezone.utc) + timedelta(seconds=i * 82.3)
        # 系统使用错误 UTC-4 计算本地时间
        local_wrong = ts - timedelta(hours=4)
        # 结算日期判断：系统误以为在 T+1 截止前，实际已过截止（差 1 小时）
        settle_dt = "2024-11-04" if ts.hour < 20 else "2024-11-05"  # correct
        settle_dt_sys = "2024-11-04" if (ts - timedelta(hours=4)).hour < 16 else "2024-11-05"  # wrong
        rows.append([
            ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
            rng.choice(["ESZ4", "NQZ4", "RTYH5"]),
            f"ORD-{20241103000000 + i:016d}",
            rng.choice(["BUY", "SELL"]),
            round(rng.uniform(4500.0, 4700.0), 2),
            rng.randint(1, 20),
            local_wrong.strftime("%Y-%m-%dT%H:%M:%S"),
            "UTC-4",  # Bug: should be UTC-5 after DST change
            settle_dt_sys,
        ])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(WS / "incident" / "order_book_snapshot_20241103.csv", buf.getvalue())

    # 2.4 position_delta_report.csv — delta-hedge 平仓触发记录
    delta_rows = [["order_id", "trigger_time_utc", "trigger_time_system_local",
                   "timezone_offset_system", "cme_settle_reference_utc",
                   "delta_target", "delta_actual", "offset_minutes", "status"]]
    # CME 日结算：15:00:00 CT = 21:00:00 UTC（EST 期间，2024-11-03）
    # 系统误以为是 20:00:00 UTC（UTC-4 硬编码，实际 UTC-5）
    cme_settle_correct = datetime(2024, 11, 3, 21, 0, 0, tzinfo=timezone.utc)
    cme_settle_wrong = datetime(2024, 11, 3, 20, 0, 0, tzinfo=timezone.utc)
    for i in range(200):
        ts = cme_settle_wrong + timedelta(seconds=rng.randint(-1800, 1800))
        delta_rows.append([
            f"DHG-{i + 1:06d}",
            ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
            (ts - timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%S"),
            "-04:00",
            cme_settle_wrong.strftime("%Y-%m-%dT%H:%M:%SZ"),  # wrong reference
            round(rng.uniform(-2.5, 2.5), 4),
            round(rng.uniform(-2.5, 2.5), 4),
            60,  # 1-hour offset due to DST bug
            "OFFSET_DST_ERROR",
        ])
    buf2 = io.StringIO()
    csv.writer(buf2).writerows(delta_rows)
    w(WS / "incident" / "position_delta_report.csv", buf2.getvalue())

    # 2.5 incident_timeline.md — 内部事故时间线草稿（含两处错误数据，为信息冲突陷阱）
    # V1 冲突陷阱：
    #   - 错误1：bot summary 和本文件声称 KCG 损失为 $440M（正确 $460M+）
    #   - 错误2：描述 CME 结算 UTC 为 20:00（DST 错误值，正确为 21:00 in EST）
    w(WS / "incident" / "incident_timeline.md", """# ArtemisQ Capital — Incident Timeline (DRAFT)
## Event: AROS v4.2 Timezone Misconfiguration (2024-11-03)

> DRAFT — Subject to revision. Two data points below marked [VERIFY] are contested.

### Background
AROS v4.2 was deployed 2024-10-15. The timezone configuration was set to UTC-4
(America/New_York EDT) at deployment time. The US Eastern timezone switched from
EDT (UTC-4) to EST (UTC-5) on **2024-11-03 at 02:00 local time**.

AROS v4.2 hardcoded `UTC_OFFSET = -4` in `code/aros/timezone_config.py`.
No automatic DST adjustment was implemented.

### Timeline (UTC)

| Time (UTC) | Event |
|------------|-------|
| 2024-11-03T07:00:00Z | AROS v4.2 pre-market startup; timezone_config loads UTC-4 |
| 2024-11-03T09:30:00Z | NYSE/CME markets open |
| 2024-11-03T14:00:00Z | [ANOMALY START] System begins T+1 cutoff calculations using wrong offset |
| 2024-11-03T14:30:00Z | First mis-timed T+1 settlement order fired |
| 2024-11-03T19:00:00Z | System computes CME settle trigger at 20:00 UTC [VERIFY — may be 21:00] |
| 2024-11-03T20:00:00Z | System triggers delta-hedge closes, 1 hour early |
| 2024-11-03T21:00:00Z | Correct CME daily settlement time (15:00 CT = 21:00 UTC in EST) |
| 2024-11-03T21:30:00Z | Compliance team detects MiFIR Field 28 timestamp discrepancy |
| 2024-11-03T22:00:00Z | AROS v4.2 trading halted by manual override |
| 2024-11-04T08:00:00Z | Root cause identified: UTC_OFFSET hardcoded as -4 instead of -5 |

### Estimated Impact

**[VERIFY]** Some internal estimates put the loss from mis-timed orders at approximately
the same scale as the Knight Capital incident loss figure of **$440M** (KCG preliminary
estimate). This figure is UNCONFIRMED and disputed — the authoritative KCG SEC figure
should be consulted. The actual ArtemisQ event loss is separately estimated and
much smaller.

The UTC offset error caused:
1. T+1 settlement orders submitted outside correct window (60-minute offset)
2. CME delta-hedge triggered 1 hour early (at 20:00 UTC instead of 21:00 UTC)
3. MiFIR Field 28 timestamps reported as local time (UTC-4) instead of UTC

### Key Configuration Error
- **File**: `code/aros/timezone_config.py`, line 42
- **Error value**: `UTC_OFFSET = -4`
- **Correct value**: `UTC_OFFSET = -5` (EST, after 2024-11-03 02:00 switchover)
""")


# --------------------------------------------------------------------------- #
# 3. Regulatory 文件（真实锚点参照）
# --------------------------------------------------------------------------- #
def gen_regulatory_files() -> None:
    # 3.1 Rule 15c3-5 Market Access Rule（合成，基于 SEC 原文）
    w(WS / "regulatory" / "rule_15c3_5_market_access.md", """# Rule 15c3-5 — Risk Management Controls for Brokers or Dealers with Market Access
## (Market Access Rule)

**Source**: SEC Release No. 34-63241 (November 3, 2010)
**Effective Date**: January 14, 2011
**Compliance Deadline**: July 14, 2011

### Overview

Rule 15c3-5, adopted under the Securities Exchange Act of 1934,
requires broker-dealers with market access to implement risk management
controls and supervisory procedures reasonably designed to:

1. Systematically limit the financial exposure of the broker or dealer;
2. Ensure compliance with applicable regulatory requirements; and
3. Prevent erroneous orders that exceed appropriate pre-set capital thresholds.

### Rule 15c3-5(b) — Financial Risk Management Controls

**Rule 15c3-5(b)** specifically requires broker-dealers with market access
to establish, document, and maintain a system of risk management controls
and supervisory procedures that are **reasonably designed to manage the
financial risks** of that market access, including:

- Pre-trade capital thresholds and credit limits
- Order size/quantity limits per security
- Prevent accumulation of undue positions
- Prevent orders that appear to exceed capital thresholds

**Reference enforcement case**: In the Matter of Knight Capital Americas LLC
(SEC Release No. 34-70694), Knight Capital violated Rule 15c3-5(b) by
failing to maintain adequate financial risk management controls, resulting
in the deployment of legacy "Power Peg" code that generated 4,000,000+
child orders from 212 customer orders on August 1, 2012.

### Penalty Framework

- Administrative proceedings under the Securities Exchange Act
- Civil penalties up to applicable statutory limits
- Knight Capital Americas LLC agreed to pay **$12,000,000** to settle
  charges of violating Rule 15c3-5(b) (SEC Release No. 34-70694,
  Admin Proc. File No. 3-15570)

### Annual CEO Certification Requirement

Each broker-dealer subject to this rule must conduct an annual review
and the CEO (or equivalent) must certify compliance.

---

*Full text: https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm*
""")

    # 3.2 Rule 15c6-1 T+1 Settlement Rule（合成）
    w(WS / "regulatory" / "rule_15c6_1_t1_settlement.md", """# Rule 15c6-1 — T+1 Securities Settlement Cycle

**Source**: SEC Rule 15c6-1 Amendments (Securities Exchange Act of 1934)
**Effective Date**: **2024-05-28** (T+1 Settlement Cycle)
**Previous Rule**: T+2 settlement (in effect 2017-2024)

### Overview

On February 15, 2023, the SEC adopted amendments to Rule 15c6-1 under
the Securities Exchange Act of 1934, shortening the standard settlement
cycle for most broker-dealer transactions in securities from two business
days after the trade date (T+2) to **one business day after the trade
date (T+1)**.

The T+1 rule became effective on **May 28, 2024**.

### Scope of T+1 Rule

The following transaction types must settle T+1:
- Equities (stocks listed on U.S. national securities exchanges)
- Corporate bonds
- Unit investment trusts (UITs)
- Certain limited partnership interests traded on exchanges

### Settlement Cutoff Times (Eastern Time)

Under T+1, the standard settlement deadline is:
- **9:00 PM ET** on trade date for DTC-eligible securities
- Affirmation cutoff: **9:00 PM ET** same business day
- DTCC DTC settlement: following business day

### Impact on Automated Trading Systems

Systems computing T+1 settlement windows must:
1. Use correct UTC offset for Eastern Time (EDT: UTC-4; EST: UTC-5)
2. Account for DST transitions when computing settlement cutoffs
3. Report all timestamps in **UTC** for regulatory purposes (MiFIR Field 28)

**Critical DST note**: On the first Sunday of November each year,
US clocks fall back from EDT (UTC-4) to EST (UTC-5). Systems with
hardcoded UTC offsets will compute settlement cutoffs 1 hour incorrectly
until the offset is updated.

### New Requirements: Rule 17Ad-27

The SEC also adopted Rule 17Ad-27, requiring registered clearing agencies
to establish, implement, maintain, and enforce written policies and procedures
reasonably designed to facilitate straight-through processing (STP).

---

*Reference: https://www.sec.gov/exams/educationhelpguidesfaqs/t1-faq*
""")

    # 3.3 FCA Market Watch 59 Summary（含 Field 28 详细要求）
    w(WS / "regulatory" / "fca_market_watch_59_summary.md", """# FCA Market Watch 59 — MiFIR Transaction Reporting Observations

**Source**: Financial Conduct Authority, Market Watch Newsletter Issue 59
**Publication Date**: April 2019
**Reference URL**: https://www.fca.org.uk/publication/newsletters/market-watch-59.pdf

---

## Overview

Market Watch 59 sets out the FCA's observations on common errors in
MiFIR (Markets in Financial Instruments Regulation) transaction reporting.
The newsletter specifically addresses **UTC and DST timestamp compliance issues**
that were identified as a systemic problem across multiple firms.

---

## Field 28: Trading Date and Time — Key Requirements

**Field 28** (trading date & time) is one of the most frequently mis-reported
fields in MiFIR transaction reports submitted to the FCA.

### Mandatory Requirements for Field 28

1. **UTC mandatory**: Field 28 must be reported in **Coordinated Universal Time
   (UTC)**, not in local time. This requirement replaced the MiFID I approach
   of reporting in local time.

2. **ISO 8601 format**: The timestamp must be expressed in ISO 8601 format
   with UTC designator, e.g. `2024-11-03T21:00:00Z`.

3. **DST awareness**: During British Summer Time (BST, UTC+1), firms must
   **subtract 1 hour** from their local UK timestamps to convert to UTC
   before reporting. During GMT (UTC+0), local time equals UTC.
   Similarly, US-based firms must account for EDT (UTC-4) vs EST (UTC-5)
   transitions when computing UTC for Field 28.

4. **Precision**: Timestamps must include at minimum **second-level precision**;
   microsecond precision is required for high-frequency trading venues.

### Common DST Errors Identified by FCA

The FCA identified the following systemic errors in Field 28 reporting:

| Error Type | Description | Frequency |
|------------|-------------|-----------|
| BST/GMT confusion | Reporting BST local time as if it were UTC (1-hour error) | Most common |
| Hardcoded UTC offset | Systems with static UTC offset that does not update on DST switch | Common |
| Local time submission | Submitting local exchange time without UTC conversion | Moderate |
| Microsecond truncation | Reporting seconds-only when microseconds required for HFT | Moderate |

### Regulatory Consequence

Firms that report Field 28 with incorrect timestamps (e.g. local time instead
of UTC, or with wrong DST offset) are in breach of:
- **Article 26 of MiFIR** (transaction reporting obligation)
- **RTS 22** (regulatory technical standards on transaction reporting)

The FCA may issue data quality warnings, require resubmission, and in
repeated/serious cases, initiate supervisory action.

---

## MiFIR RTS 22 Field 28 Technical Specification

Per RTS 22 (Commission Delegated Regulation (EU) 2017/590):

- Field number: **28**
- Field name: **Trading date and time**
- Field description: Date and time when the transaction was executed
- Format: ISO 8601 date-time in UTC — `{YYYY}-{MM}-{DD}T{hh}:{mm}:{ss}[.{mmm}]Z`
- Applicability: All reportable transactions under Article 26 MiFIR

---

## Remediation Guidance

FCA Market Watch 59 recommends the following remediation steps for firms
with Field 28 compliance issues:

1. **Audit existing reporting infrastructure** for hardcoded UTC offsets
2. **Implement automatic DST detection** using OS-level timezone libraries
   (e.g. `pytz`, `zoneinfo`, `dateutil`) rather than static offsets
3. **Backfill corrected reports** for the affected reporting period
4. **Test UTC conversion logic** specifically around DST transition days
5. **Document the fix** in the firm's compliance testing procedures
""")

    # 3.4 SEC Release 34-70694 Full (KCG 行政令全文，含所有锚点)
    w(WS / "regulatory" / "sec_release_34_70694_full.md", """# In the Matter of Knight Capital Americas LLC
## SEC Administrative Order — Release No. 34-70694
## Admin Proc. File No. 3-15570

**Source**: U.S. Securities and Exchange Commission
**Reference URL**: https://www.sec.gov/files/litigation/admin/2013/34-70694.pdf
**Date**: October 16, 2013

---

## Summary of Violations

Knight Capital Americas LLC ("Knight") violated Rule **15c3-5(b)** of the
Securities Exchange Act of 1934 (the "Market Access Rule") by failing to
maintain adequate financial risk management controls and supervisory procedures.

Knight agreed to pay a civil penalty of **$12,000,000** and to undertake
certain remedial measures.

---

## Factual Findings

### The Deployment (July 27 – August 1, 2012)

Knight employed a manual, undocumented deployment procedure. Beginning on
**July 27, 2012**, over a period of multiple days, Knight deployed new
Retail Liquidity Provider (RLP) code to its **8 SMARS servers** (Smart Market
Access Routing System), deploying to one server per day.

On **August 1, 2012**, the 8th and final SMARS server had not received the
new RLP code. Instead, it retained dormant "Power Peg" code from approximately
2005, which had been deactivated but not removed.

### The August 1, 2012 Incident

On **August 1, 2012**, beginning at market open (9:30 AM ET):

- Knight's SMARS system received **212 customer orders** for various equities
- The 8th server, running the legacy Power Peg code, began generating child orders
  at approximately **18,868 child orders per parent order**
- Over approximately **45 minutes** (9:30 AM to ~9:58 AM ET), SMARS generated
  **4,000,000+ child orders** in **154 stocks**
- Total shares traded: **397,000,000+ shares** (approximately 3.97 billion shares)

### The Automated Emails

Beginning at **8:01 AM ET**, over 90 minutes before market open, Knight's
automated monitoring system sent **97 automated emails** with subject line
"Power Peg disabled" to Knight's personnel. These warning emails were
not escalated or acted upon prior to market open.

### Financial Impact

The incident resulted in a trading loss exceeding **$460,000,000** (four hundred
sixty million dollars). This figure represents the net loss after Knight attempted
to unwind its positions in the affected securities over the days following August 1, 2012.

**Note**: Some preliminary and media reports cited an initial estimate of approximately
$440 million. The **authoritative SEC-confirmed figure is $460,000,000+** as stated
in SEC Press Release 2013-222.

### Shutdown

Knight's engineers identified the root cause and manually disabled SMARS at
approximately **9:58 AM ET**, approximately 45 minutes after the erroneous
ordering had begun.

---

## Rule Violations

Knight Capital Americas LLC violated:

**Rule 15c3-5(b)** — Knight failed to establish, document, and maintain a system
of risk management controls and supervisory procedures reasonably designed to
manage the financial risks of its market access. Specifically:

- Knight lacked a mechanism to identify that the 8th SMARS server had not received
  the new RLP deployment
- Knight did not halt trading upon receiving the 97 automated "Power Peg disabled"
  emails (a clear signal of system misconfiguration)
- Knight's supervisory procedures were not reasonably designed to prevent the type
  of erroneous ordering that occurred

---

## Penalty and Remediation

Knight Capital Americas LLC agreed to:
1. **Cease and desist** from committing or causing any violations of Rule 15c3-5(b)
2. **Pay a civil money penalty** of **$12,000,000**
3. Undertake certain compliance undertakings, including annual CEO certification
   and enhanced deployment procedures

---

*Admin Proc. File No. 3-15570 | Release No. 34-70694 | October 16, 2013*
""")

    # 3.5 MiFIR RTS 22 Field Reference CSV（含 Field 28 定义）
    fields_rows = [
        ["field_number", "field_name", "format", "mandatory_utc", "notes"],
        ["1", "Transaction Reference Number", "Up to 52 alphanumeric", "N", "Unique identifier for the transaction"],
        ["2", "Trading Venue Transaction ID", "Up to 52 alphanumeric", "N", "Exchange-assigned ID"],
        ["3", "Executing Entity ID", "LEI 20 alphanumeric", "N", "Legal Entity Identifier"],
        ["4", "Investment Firm/Branch ID", "LEI 20 alphanumeric", "N", "Reporting entity LEI"],
        ["5", "Buyer/Seller LEI", "LEI 20 alphanumeric", "N", "Counterparty identifier"],
        ["14", "Buyer Client ID", "Up to 50 characters", "N", "Buy-side client reference"],
        ["16", "Seller Client ID", "Up to 50 characters", "N", "Sell-side client reference"],
        ["26", "Price", "Decimal up to 18,13", "N", "Transaction price"],
        ["27", "Price Currency", "ISO 4217 3-char", "N", "Currency of price field"],
        ["28", "Trading date and time", "ISO 8601 UTC datetime", "Y",
         "MANDATORY UTC. DST transitions must be converted. Format: YYYY-MM-DDTHH:MM:SS[.mmm]Z. "
         "MiFID I allowed local time; MiFIR requires UTC. FCA Market Watch 59 identifies Field 28 "
         "as the most commonly mis-reported timestamp field."],
        ["29", "Trade Date", "ISO 8601 date YYYY-MM-DD", "N", "Date portion of transaction"],
        ["30", "Trading Capacity", "DEAL/MTCH/AOTC", "N", "Proprietary/matched/agency"],
        ["31", "Quantity", "Integer or decimal", "N", "Number of units traded"],
        ["33", "Venue", "MIC code or XOFF/SINT", "N", "Trading venue identifier"],
        ["36", "Instrument Identification Code", "ISIN 12 chars", "N", "Financial instrument code"],
        ["44", "Transmission of Order", "True/False", "N", "Whether order was transmitted"],
        ["58", "Branch Membership Country", "ISO 3166-1 alpha-2", "N", "Country code"],
        ["60", "Total Commission", "Decimal", "N", "Transaction commission amount"],
        ["61", "FX Rate", "Decimal", "N", "Exchange rate if applicable"],
        ["63", "Complex Trade Component ID", "Up to 35 alphanumeric", "N", "For linked transactions"],
    ]
    buf = io.StringIO()
    csv.writer(buf).writerows(fields_rows)
    w(WS / "regulatory" / "mifir_rts22_field_reference.csv", buf.getvalue())


# --------------------------------------------------------------------------- #
# 4. Code 文件（时区配置模块 + 调度器 + 路由核心等）
# --------------------------------------------------------------------------- #
def gen_code_files() -> None:
    # 4.1 timezone_config.py（含错误硬编码 UTC-4 及注释）
    w(WS / "code" / "aros" / "timezone_config.py", '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aros/timezone_config.py — AROS v4.2 Timezone Configuration Module

WARNING: This file contains a known BUG introduced at deployment on 2024-10-15.
The UTC_OFFSET is hardcoded as -4 (America/New_York EDT) and does NOT
automatically update when the US Eastern timezone switches to EST (UTC-5)
on the first Sunday of November.

The BUG is on line 42: UTC_OFFSET = -4
The CORRECT value after 2024-11-03 02:00 local time should be: UTC_OFFSET = -5
"""

import datetime
import logging

logger = logging.getLogger(__name__)

# =============================================================================
# VERSION INFORMATION
# =============================================================================
AROS_VERSION = "4.2.1"
CONFIG_FILE_VERSION = "2024.10.15"
DEPLOYED_BY = "kenji.nakamura@artemisq.com"
DEPLOYMENT_DATE = "2024-10-15"

# =============================================================================
# TIMEZONE CONFIGURATION
# =============================================================================

# BUG: This value was set during EDT (UTC-4) and was NOT updated when
# US Eastern switched to EST (UTC-5) on 2024-11-03.
# See incident report: aros_v4_2_audit_log.jsonl events starting 2024-11-03T14:00:00Z
UTC_OFFSET = -4  # line 42 — BUG: should be -5 (EST) after 2024-11-03 switch

# The CORRECT timezone for post-DST-switch operation:
# UTC_OFFSET_CORRECT = -5  # EST (Eastern Standard Time), UTC-5

# Timezone abbreviation (also incorrect after switch)
TIMEZONE_ABBR = "EDT"  # BUG: should be "EST" after 2024-11-03
TIMEZONE_NAME = "America/New_York"

# DST awareness flag — DISABLED in this version
DST_AWARE = False  # Known deficiency; scheduled for v4.3 upgrade

# =============================================================================
# SETTLEMENT TIMING CONSTANTS
# =============================================================================

# CME E-Mini daily settlement: 15:00:00 CT
# In CDT (UTC-5 Central): 15:00 CDT = 20:00 UTC
# In CST (UTC-6 Central): 15:00 CST = 21:00 UTC
# NOTE: After US EST/EDT switch on 2024-11-03, ET becomes UTC-5,
# making CME Central Time UTC-6, so 15:00 CT = 21:00 UTC (NOT 20:00 UTC)
CME_DAILY_SETTLE_HOUR_CT = 15
CME_DAILY_SETTLE_MINUTE_CT = 0

# System's (incorrect) CME settlement UTC time
# BUG: system computes as 20:00 UTC because it uses UTC-4 offset for ET
# which then propagates to CT offset calculation
CME_SETTLE_UTC_HOUR_SYSTEM = 20  # BUG: should be 21 after DST switch

# T+1 Settlement cutoff (ET) per SEC Rule 15c6-1 (effective 2024-05-28)
T1_CUTOFF_HOUR_ET = 21  # 9:00 PM ET
T1_CUTOFF_MINUTE_ET = 0

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_utc_offset() -> int:
    """Return the configured UTC offset. WARNING: Does not handle DST."""
    logger.warning("UTC_OFFSET is static (%d); DST_AWARE=%s", UTC_OFFSET, DST_AWARE)
    return UTC_OFFSET


def local_to_utc(local_dt: datetime.datetime) -> datetime.datetime:
    """Convert local ET time to UTC using hardcoded offset. BUG: ignores DST."""
    utc = local_dt - datetime.timedelta(hours=UTC_OFFSET)
    logger.debug("local_to_utc: %s + (%d) = %s (DST-unaware)", local_dt, -UTC_OFFSET, utc)
    return utc


def utc_to_local(utc_dt: datetime.datetime) -> datetime.datetime:
    """Convert UTC to local ET time using hardcoded offset. BUG: ignores DST."""
    local = utc_dt + datetime.timedelta(hours=UTC_OFFSET)
    return local


def get_cme_settle_utc(trade_date: datetime.date) -> datetime.datetime:
    """
    Return CME daily settlement time in UTC for a given trade date.
    BUG: Returns 20:00 UTC on 2024-11-03 (should be 21:00 UTC after EST switch).
    """
    settle_local = datetime.datetime(
        trade_date.year, trade_date.month, trade_date.day,
        CME_DAILY_SETTLE_HOUR_CT, CME_DAILY_SETTLE_MINUTE_CT
    )
    # Approximate CT-to-UTC offset using ET offset - 1
    ct_utc_offset = UTC_OFFSET - 1
    settle_utc = settle_local - datetime.timedelta(hours=ct_utc_offset)
    return settle_utc


def get_t1_cutoff_utc(trade_date: datetime.date) -> datetime.datetime:
    """
    Return T+1 settlement cutoff in UTC for a given trade date.
    Under Rule 15c6-1 (effective 2024-05-28), cutoff is 21:00 ET.
    BUG: Returns wrong UTC time because UTC_OFFSET is -4 instead of -5.
    """
    cutoff_local = datetime.datetime(
        trade_date.year, trade_date.month, trade_date.day,
        T1_CUTOFF_HOUR_ET, T1_CUTOFF_MINUTE_ET
    )
    # BUG: uses UTC_OFFSET = -4; should use -5 (EST)
    cutoff_utc = cutoff_local - datetime.timedelta(hours=UTC_OFFSET)
    return cutoff_utc


# Legacy compatibility alias (do not use in new code)
OFFSET_HOURS = UTC_OFFSET
''')

    # 4.2 settlement_scheduler.py（含 DST 未处理的 bug）
    w(WS / "code" / "aros" / "settlement_scheduler.py", '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aros/settlement_scheduler.py — AROS v4.2 Settlement Scheduler

Manages T+1 settlement deadlines and CME daily settlement triggers.
Contains known DST bug: inherits UTC_OFFSET from timezone_config.py.
After 2024-11-03 DST switch, all settlement time calculations are
offset by +60 minutes from correct UTC.
"""

import datetime
import logging
from pathlib import Path

# Import the buggy timezone config
from .timezone_config import (
    UTC_OFFSET, CME_SETTLE_UTC_HOUR_SYSTEM,
    get_t1_cutoff_utc, get_cme_settle_utc,
    DST_AWARE,
)

logger = logging.getLogger(__name__)

# =============================================================================
# T+1 SETTLEMENT SCHEDULER
# =============================================================================

class SettlementScheduler:
    """
    Schedules T+1 settlement deadline checks per SEC Rule 15c6-1.
    Rule 15c6-1 amendments effective 2024-05-28 require T+1 settlement
    for equities, corporate debt, and unit investment trusts.

    BUG: DST-unaware — cutoff times will be 1 hour incorrect after
    November 3, 2024 DST transition until UTC_OFFSET is corrected.
    """

    def __init__(self, trade_date: datetime.date):
        self.trade_date = trade_date
        self._cutoff_utc = get_t1_cutoff_utc(trade_date)
        if not DST_AWARE:
            logger.warning(
                "SettlementScheduler initialized with DST_AWARE=False; "
                "UTC_OFFSET=%d may be stale after DST transition", UTC_OFFSET
            )

    @property
    def cutoff_utc(self) -> datetime.datetime:
        """T+1 settlement cutoff in UTC. BUG: 1 hour wrong after DST switch."""
        return self._cutoff_utc

    def is_within_window(self, order_time_utc: datetime.datetime) -> bool:
        """
        Check if an order timestamp is within the T+1 settlement window.
        Returns True if order_time_utc <= cutoff_utc.
        BUG: cutoff is 1 hour early after DST switch.
        """
        return order_time_utc <= self._cutoff_utc

    def get_settlement_date(self, order_time_utc: datetime.datetime) -> datetime.date:
        """
        Return settlement date (T+1) for an order.
        BUG: Window boundary calculation uses wrong UTC offset.
        """
        if self.is_within_window(order_time_utc):
            # Order is within T+1 window for trade_date
            return self.trade_date + datetime.timedelta(days=1)
        else:
            # Order misses today's T+1 window, settles T+2
            return self.trade_date + datetime.timedelta(days=2)

    def describe(self) -> dict:
        """Return a summary of scheduler configuration (for audit purposes)."""
        return {
            "trade_date": self.trade_date.isoformat(),
            "t1_rule": "Rule 15c6-1 (effective 2024-05-28)",
            "cutoff_utc_system": self._cutoff_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "utc_offset_used": UTC_OFFSET,
            "dst_aware": DST_AWARE,
            "known_bug": "UTC_OFFSET hardcoded; 1-hour error after 2024-11-03 DST switch",
        }
''')

    # 4.3 order_router.py（较长）
    w(WS / "code" / "aros" / "order_router.py", '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aros/order_router.py — AROS v4.2 Automated Order Router (Core)

Routes orders through venue selection, risk checks, and settlement scheduling.
References UTC-4 offset from timezone_config (bug source for 2024-11-03 incident).

This file is part of AROS v4.2. For the deprecated v3.1 router, see:
  code/legacy/aros_v3_1_router_DEPRECATED.py
  (DO NOT USE — deprecated 2023-06-01; incompatible with MiFIR Field 28 UTC requirement)
"""

import datetime
import hashlib
import json
import logging
from dataclasses import dataclass, field
from typing import Optional, List, Dict

from .timezone_config import UTC_OFFSET, get_t1_cutoff_utc, DST_AWARE
from .settlement_scheduler import SettlementScheduler

logger = logging.getLogger(__name__)

AROS_ROUTER_VERSION = "4.2.1"
SUPPORTED_INSTRUMENTS = ["ESZ4", "NQZ4", "RTYH5", "YMH5", "MES"]
SUPPORTED_VENUES = ["CME", "ICE", "CBOE", "NYSE"]

# Risk limits
MAX_ORDER_QTY = 200
MAX_NOTIONAL_USD = 10_000_000
DAILY_LOSS_LIMIT_USD = 500_000

# MiFIR reporting requirement
MIFIR_FIELD28_TZ = "UTC"  # Must be UTC per FCA Market Watch 59 / RTS 22 Field 28


@dataclass
class Order:
    order_id: str
    instrument: str
    side: str  # BUY or SELL
    quantity: int
    price: float
    order_type: str  # MARKET_MAKE, DELTA_HEDGE, T1_SETTLEMENT, REBALANCE
    submission_time_utc: datetime.datetime
    venue: str = "CME"
    settlement_date: Optional[datetime.date] = None
    mifir_field28: Optional[str] = None  # Must be UTC string
    flags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "instrument": self.instrument,
            "side": self.side,
            "quantity": self.quantity,
            "price": self.price,
            "order_type": self.order_type,
            "submission_time_utc": self.submission_time_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "venue": self.venue,
            "settlement_date": self.settlement_date.isoformat() if self.settlement_date else None,
            "mifir_field28": self.mifir_field28,
            "flags": self.flags,
        }


class OrderRouter:
    """
    AROS v4.2 core order router.

    BUG: Uses DST-unaware timezone_config for settlement window calculations.
    On 2024-11-03 after DST switch, T+1 settlement orders are 1 hour off.
    """

    def __init__(self, trade_date: datetime.date):
        self.trade_date = trade_date
        self.scheduler = SettlementScheduler(trade_date)
        self._order_count = 0
        self._rejected = 0
        logger.info(
            "OrderRouter v%s initialized; trade_date=%s; T1_cutoff_utc=%s; UTC_OFFSET=%d",
            AROS_ROUTER_VERSION, trade_date,
            self.scheduler.cutoff_utc.strftime("%Y-%m-%dT%H:%M:%SZ"), UTC_OFFSET
        )

    def _gen_order_id(self, instrument: str) -> str:
        ts = datetime.datetime.utcnow().isoformat()
        h = hashlib.md5(f"{instrument}:{ts}:{self._order_count}".encode()).hexdigest()[:12]
        return f"ORD-{h.upper()}"

    def _check_risk(self, order: Order) -> Optional[str]:
        """Pre-trade risk check. Returns rejection reason or None if OK."""
        if order.quantity > MAX_ORDER_QTY:
            return f"qty {order.quantity} exceeds max {MAX_ORDER_QTY}"
        if order.quantity * order.price > MAX_NOTIONAL_USD:
            return f"notional ${order.quantity * order.price:,.0f} exceeds limit"
        return None

    def route(self, instrument: str, side: str, qty: int, price: float,
              order_type: str = "MARKET_MAKE") -> Order:
        """Route a single order through risk checks and settlement scheduling."""
        self._order_count += 1
        now_utc = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

        order = Order(
            order_id=self._gen_order_id(instrument),
            instrument=instrument,
            side=side,
            quantity=qty,
            price=price,
            order_type=order_type,
            submission_time_utc=now_utc,
            venue="CME" if instrument.startswith("ES") else "ICE",
        )

        # Risk check
        rejection = self._check_risk(order)
        if rejection:
            self._rejected += 1
            order.flags.append(f"REJECTED:{rejection}")
            logger.warning("Order rejected: %s", rejection)
            return order

        # Settlement scheduling (buggy: uses UTC_OFFSET = -4 instead of -5)
        order.settlement_date = self.scheduler.get_settlement_date(now_utc)

        # MiFIR Field 28 — Must be UTC per FCA Market Watch 59
        # BUG: system was submitting LOCAL time (UTC-4) instead of UTC
        # This is the compliance violation identified in FCA inquiry
        order.mifir_field28 = now_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")  # Correct (UTC)
        # Pre-fix (buggy) version was:
        # order.mifir_field28 = (now_utc + timedelta(hours=UTC_OFFSET)).strftime(...)  # WRONG

        return order

    def get_stats(self) -> dict:
        return {
            "total_orders": self._order_count,
            "rejected": self._rejected,
            "utc_offset_used": UTC_OFFSET,
            "dst_aware": DST_AWARE,
        }


# --------------------------------------------------------------------------
# Standalone helpers (used by risk_monitor.py and backtest scripts)
# --------------------------------------------------------------------------

def compute_t1_cutoff_utc(trade_date: datetime.date, utc_offset: int) -> datetime.datetime:
    """
    Compute T+1 settlement cutoff in UTC given a UTC offset for ET.
    Rule 15c6-1: cutoff = 21:00 ET = (21:00 - utc_offset) UTC.

    Correct usage:
      compute_t1_cutoff_utc(date(2024, 11, 3), -5)  # EST → 02:00 UTC next day
    Bug usage (AROS v4.2):
      compute_t1_cutoff_utc(date(2024, 11, 3), -4)  # EDT → 01:00 UTC next day (wrong)
    """
    cutoff_local = datetime.datetime(
        trade_date.year, trade_date.month, trade_date.day, 21, 0, 0
    )
    return cutoff_local - datetime.timedelta(hours=utc_offset)
''')

    # 4.4 risk_monitor.py（较短）
    w(WS / "code" / "aros" / "risk_monitor.py", '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aros/risk_monitor.py — AROS v4.2 Real-Time Risk Monitor

Monitors portfolio risk metrics and P&L in real time.
Known gap: NOT integrated with order_router.py for pre-trade risk filtering.
This gap was identified as a contributing factor in the 2024-11-03 incident.
"""

import datetime
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

MONITOR_VERSION = "4.2.0"
P_AND_L_ALERT_THRESHOLD_USD = 250_000
POSITION_ALERT_THRESHOLD_LOTS = 500
DAILY_LOSS_HARD_LIMIT_USD = 500_000


class RiskMonitor:
    """
    Real-time risk monitor for AROS v4.2.

    Integration gap: This monitor is not wired into the order routing pipeline.
    Pre-trade checks in order_router.py and this post-trade monitor are
    separate, non-communicating systems (violates Rule 15c3-5(b) intent).
    """

    def __init__(self):
        self._positions: Dict[str, float] = {}
        self._realized_pnl: float = 0.0
        self._unrealized_pnl: float = 0.0
        self._alerts: List[dict] = []
        logger.info("RiskMonitor v%s initialized (WARNING: not integrated with OrderRouter)", MONITOR_VERSION)

    def update_position(self, instrument: str, delta: float, pnl: float) -> None:
        """Update position and P&L. Called after each fill — not before."""
        prev = self._positions.get(instrument, 0.0)
        self._positions[instrument] = prev + delta
        self._realized_pnl += pnl
        self._check_thresholds(instrument)

    def _check_thresholds(self, instrument: str) -> None:
        pos = abs(self._positions.get(instrument, 0.0))
        if pos > POSITION_ALERT_THRESHOLD_LOTS:
            self._alerts.append({
                "time": datetime.datetime.utcnow().isoformat() + "Z",
                "instrument": instrument,
                "alert_type": "POSITION_LIMIT",
                "position": pos,
            })
        if abs(self._realized_pnl) > P_AND_L_ALERT_THRESHOLD_USD:
            self._alerts.append({
                "time": datetime.datetime.utcnow().isoformat() + "Z",
                "instrument": instrument,
                "alert_type": "PNL_THRESHOLD",
                "pnl": self._realized_pnl,
            })

    def get_summary(self) -> dict:
        return {
            "positions": dict(self._positions),
            "realized_pnl_usd": round(self._realized_pnl, 2),
            "unrealized_pnl_usd": round(self._unrealized_pnl, 2),
            "alert_count": len(self._alerts),
            "integration_status": "DISCONNECTED_FROM_ROUTER",
        }
''')

    # 4.5 tests/test_timezone_config.py
    w(WS / "code" / "aros" / "tests" / "test_timezone_config.py", '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for aros/timezone_config.py.

KNOWN FAILING TESTS (marked with # FAIL):
  test_est_utc_offset — expects -5, gets -4 (DST bug)
  test_cme_settle_utc_est — expects 21:00 UTC, gets 20:00 UTC (DST bug)
"""

import datetime
import sys

# Simulate importing the buggy config
UTC_OFFSET_BUGGY = -4  # What AROS v4.2 has
UTC_OFFSET_CORRECT = -5  # What it should be (EST)


def test_edt_utc_offset():
    """EDT (summer): UTC-4 is correct."""
    assert UTC_OFFSET_BUGGY == -4, "EDT offset should be -4"
    print("PASS: test_edt_utc_offset (UTC-4 correct for EDT)")


def test_est_utc_offset():
    """EST (winter after Nov DST switch): UTC-5 is correct. CURRENTLY FAILS."""
    expected = -5
    actual = UTC_OFFSET_BUGGY  # FAIL: returns -4 not -5
    if actual == expected:
        print("PASS: test_est_utc_offset")
    else:
        print(f"FAIL: test_est_utc_offset — expected {expected}, got {actual} (DST bug)")


def test_cme_settle_utc_edt():
    """CME 15:00 CT during CDT = 20:00 UTC (CT is UTC-5 in CDT)."""
    # 15:00 CT + 5h = 20:00 UTC (CDT period: CT=UTC-5)
    expected_utc_hour = 20
    ct_offset = -5  # Central Time during CDT
    computed = 15 - ct_offset  # = 20
    assert computed == expected_utc_hour
    print("PASS: test_cme_settle_utc_edt (20:00 UTC correct for CDT period)")


def test_cme_settle_utc_est():
    """CME 15:00 CT during CST = 21:00 UTC (CT is UTC-6 in CST). CURRENTLY FAILS due to DST bug."""
    expected_utc_hour = 21
    # AROS v4.2 computes: 15 - (UTC_OFFSET_BUGGY - 1) = 15 - (-5) = 20 (WRONG)
    buggy_ct_offset = UTC_OFFSET_BUGGY - 1  # = -5
    buggy_result = 15 - buggy_ct_offset  # = 20
    # Correct: CT during CST = UTC-6; 15 - (-6) = 21
    correct_ct_offset = UTC_OFFSET_CORRECT - 1  # = -6
    correct_result = 15 - correct_ct_offset  # = 21

    if buggy_result == expected_utc_hour:
        print("PASS: test_cme_settle_utc_est")
    else:
        print(f"FAIL: test_cme_settle_utc_est — expected {expected_utc_hour}, "
              f"buggy_result={buggy_result}, correct_result={correct_result}")


def test_t1_cutoff_utc_edt():
    """T+1 cutoff 21:00 ET during EDT = 01:00 UTC next day. UTC-4: 21+4=25=01:00+1d."""
    cutoff_utc = 21 - UTC_OFFSET_BUGGY  # = 25 = 01:00 next day
    assert cutoff_utc % 24 == 1
    print("PASS: test_t1_cutoff_utc_edt (01:00 UTC next day)")


def test_t1_cutoff_utc_est():
    """T+1 cutoff 21:00 ET during EST = 02:00 UTC next day. UTC-5: 21+5=26=02:00+1d. FAILS."""
    expected_hour_next_day = 2
    buggy = (21 - UTC_OFFSET_BUGGY) % 24   # = 25 % 24 = 1 (01:00 UTC — WRONG)
    correct = (21 - UTC_OFFSET_CORRECT) % 24  # = 26 % 24 = 2 (02:00 UTC — CORRECT)
    if buggy == expected_hour_next_day:
        print("PASS: test_t1_cutoff_utc_est")
    else:
        print(f"FAIL: test_t1_cutoff_utc_est — expected {expected_hour_next_day}:00, "
              f"buggy={buggy}:00, correct={correct}:00 (1-hour DST error)")


if __name__ == "__main__":
    test_edt_utc_offset()
    test_est_utc_offset()
    test_cme_settle_utc_edt()
    test_cme_settle_utc_est()
    test_t1_cutoff_utc_edt()
    test_t1_cutoff_utc_est()
''')

    # 4.6 tests/test_settlement.py
    w(WS / "code" / "aros" / "tests" / "test_settlement.py", '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for aros/settlement_scheduler.py (T+1 settlement timing)."""

import datetime

TRADE_DATE = datetime.date(2024, 11, 3)

# UTC offsets
UTC_OFFSET_BUGGY = -4   # What AROS v4.2 uses (EDT — WRONG after Nov 3 switch)
UTC_OFFSET_CORRECT = -5  # What it should be (EST — CORRECT after Nov 3 switch)


def compute_cutoff(utc_offset: int) -> datetime.datetime:
    """Compute T+1 cutoff UTC for 21:00 ET on TRADE_DATE."""
    cutoff_et = datetime.datetime(2024, 11, 3, 21, 0, 0)
    return cutoff_et - datetime.timedelta(hours=utc_offset)


def test_cutoff_with_correct_offset():
    """With UTC-5 (EST), 21:00 ET = 02:00 UTC next day (2024-11-04T02:00:00Z)."""
    cutoff = compute_cutoff(UTC_OFFSET_CORRECT)
    expected = datetime.datetime(2024, 11, 4, 2, 0, 0)
    assert cutoff == expected, f"Expected {expected}, got {cutoff}"
    print(f"PASS: test_cutoff_with_correct_offset -> {cutoff.isoformat()}Z")


def test_cutoff_with_buggy_offset():
    """With UTC-4 (EDT/BUG), 21:00 ET = 01:00 UTC next day (2024-11-04T01:00:00Z)."""
    cutoff = compute_cutoff(UTC_OFFSET_BUGGY)
    expected = datetime.datetime(2024, 11, 4, 1, 0, 0)
    assert cutoff == expected, f"Expected {expected}, got {cutoff}"
    print(f"NOTE: test_cutoff_with_buggy_offset -> {cutoff.isoformat()}Z (1 hour too early!)")


def test_offset_delta():
    """The difference between correct and buggy cutoffs must be exactly 3600 seconds."""
    correct = compute_cutoff(UTC_OFFSET_CORRECT)
    buggy = compute_cutoff(UTC_OFFSET_BUGGY)
    delta_seconds = (correct - buggy).total_seconds()
    assert delta_seconds == 3600.0, f"Expected 3600, got {delta_seconds}"
    print(f"PASS: test_offset_delta -> {delta_seconds} seconds difference (exactly 1 hour)")


if __name__ == "__main__":
    test_cutoff_with_correct_offset()
    test_cutoff_with_buggy_offset()
    test_offset_delta()
''')

    # 4.7 legacy/aros_v3_1_router_DEPRECATED.py（V6 红鲱鱼）
    w(WS / "code" / "legacy" / "aros_v3_1_router_DEPRECATED.py", '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
legacy/aros_v3_1_router_DEPRECATED.py — DEPRECATED LEGACY CODE

WARNING: THIS FILE IS DEPRECATED AS OF 2023-06-01.
DO NOT USE THIS CODE FOR ANY PURPOSE.
DO NOT REFERENCE THIS CODE IN INCIDENT REMEDIATION.

Superseded by: code/aros/order_router.py (AROS v4.2)

Reasons for deprecation:
1. Does NOT implement MiFIR Field 28 UTC timestamp requirement
   (reports local time instead of UTC — non-compliant with FCA Market Watch 59)
2. Does NOT handle DST transitions for settlement scheduling
3. Incompatible with T+1 settlement rule (Rule 15c6-1, effective 2024-05-28)
4. Uses obsolete venue connectivity (pre-2022 CME API)
5. Power Peg-style order splitting not compliant with Rule 15c3-5(b) position limits

Archived for historical reference only. If you are reading this file during
an incident remediation, you are looking at the wrong code — use order_router.py.
"""

# LEGACY constants (do not use)
LEGACY_UTC_OFFSET = -5  # This was correct for v3.1 but lacks DST handling
LEGACY_VERSION = "3.1.7"
LEGACY_DEPRECATED_DATE = "2023-06-01"

# Legacy MiFIR field — INCORRECTLY reports local time (non-compliant)
LEGACY_MIFIR_TZ = "LOCAL"  # BUG: Should be "UTC" per Field 28 requirement

def legacy_route_order(instrument, qty, price, order_time_local):
    """
    DEPRECATED: Do not use.
    This function routes orders using local time for MiFIR Field 28 reporting,
    which is NON-COMPLIANT with FCA Market Watch 59 UTC requirement.
    """
    raise NotImplementedError(
        "aros_v3_1_router_DEPRECATED: This function is deprecated and must not be called. "
        "Use code.aros.order_router.OrderRouter instead."
    )


def legacy_compute_settlement(trade_time_local, utc_offset=-5):
    """
    DEPRECATED: Uses static UTC-5 offset without DST awareness.
    This is INCOMPATIBLE with T+1 settlement rule (Rule 15c6-1).
    """
    raise NotImplementedError("DEPRECATED")
''')

    # 4.8 legacy/timezone_config_v3_ARCHIVE.py
    w(WS / "code" / "legacy" / "timezone_config_v3_ARCHIVE.py", '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
legacy/timezone_config_v3_ARCHIVE.py — ARCHIVED (v3.1 era)

This archived config used UTC-5 (EST) as a static offset, which was
acceptable in v3.1 but:
1. Did not handle EDT (UTC-4) summer period correctly
2. Has been superseded by code/aros/timezone_config.py (AROS v4.2)

ARCHIVED: 2023-06-01. Do not use.
"""

# Archived: static EST offset only
LEGACY_OFFSET_ARCHIVE = -5
ARCHIVE_DATE = "2023-06-01"
''')


# --------------------------------------------------------------------------- #
# 5. Reports 文件（bot 摘要诱饵 + 初始损失估算 + 合规核查清单）
# --------------------------------------------------------------------------- #
def gen_reports() -> None:
    # 5.1 bot_summary_incident_20241103.md（V5 蜂蜜罐：含 3 处关键数字失真）
    # 失真1：CME 结算时间错报为 20:00 UTC（正确 21:00 UTC in EST）
    # 失真2：受影响订单数量夸大（实际需从日志统计）
    # 失真3：UTC 偏移错误描述为"系统正确地使用了 UTC-5"（实际是 UTC-4 导致问题）
    w(WS / "reports" / "bot_summary_incident_20241103.md", """# BOT SUMMARY REPORT — Incident 20241103 (AUTO-GENERATED)

> **AUTOMATED SUMMARY** — Generated by ArtemisQ internal reporting bot v2.1.
> This report is a CONVENIENCE ARTEFACT only.
> DO NOT use figures from this summary without verifying against primary sources.
> Bot summaries are known to contain computational errors and should NOT be treated as authoritative.

## Executive Summary

On 2024-11-03, the AROS v4.2 system experienced a timezone misconfiguration
following the US Eastern timezone DST transition. The following is an automated
summary of key facts (VERIFY ALL NUMBERS AGAINST PRIMARY SOURCES):

## Key Statistics (UNVERIFIED — BOT ESTIMATES)

| Metric | Bot Estimate | Source for Verification |
|--------|-------------|------------------------|
| CME Daily Settlement UTC time | **20:00:00 UTC** [VERIFY — may be different after DST] | `reference/cme_settlement_schedule.md` |
| UTC offset error | System used UTC-4; **bot analysis suggests this was actually correct for the period** [VERIFY — disputed] | `code/aros/timezone_config.py` |
| Estimated affected T+1 orders | **~8,500 orders** [VERIFY — raw count may differ] | `incident/aros_v4_2_audit_log.jsonl` |
| Knight Capital comparable loss | **$440M** [VERIFY — SEC press release has different figure] | `regulatory/sec_release_34_70694_full.md` |

## Timeline (BOT RECONSTRUCTION — MAY CONTAIN ERRORS)

The bot attempted to reconstruct the incident timeline from log fragments:
- 09:30 UTC: Market open, AROS starts routing
- 14:00 UTC: Bot detects timezone anomaly patterns
- 20:00 UTC: CME settlement reference reached [VERIFY — primary doc may show 21:00]
- 21:30 UTC: Compliance team notified

## Bot Analysis Notes

1. CME settlement time: The bot computed CME E-Mini settlement as **20:00:00 UTC**
   based on its internal CME schedule parser. This may reflect the CDT-period value;
   verify against `reference/cme_settlement_schedule.md` for EST-period.

2. UTC offset assessment: The bot's heuristic analysis concluded the UTC-4 offset
   was "within expected range" for the date. This is INCORRECT — after 2024-11-03
   02:00 local time, the correct offset is UTC-5 (EST). Do not rely on this assessment.

3. KCG comparison figure: The bot sourced $440M from an early news report.
   The authoritative SEC figure from Release No. 34-70694 / Press Release 2013-222
   should be used instead.

---
*Generated: 2024-11-04T06:00:00Z | Bot version: 2.1.0 | Confidence: LOW*
""")

    # 5.2 preliminary_loss_estimate.md（含旧 $440M 数字，V1 冲突陷阱）
    w(WS / "reports" / "preliminary_loss_estimate.md", """# Preliminary Loss Estimate — ArtemisQ Capital Incident 2024-11-03

## Status: PRELIMINARY — Subject to Revision

This document contains an initial assessment of trading losses from the
AROS v4.2 timezone misconfiguration incident.

### ArtemisQ Direct Losses (2024-11-03)

| Category | Preliminary Estimate | Status |
|----------|---------------------|--------|
| T+1 settlement errors (mis-timed orders) | ~$2.1M | Unconfirmed |
| Delta-hedge timing offset (CME) | ~$800K | Unconfirmed |
| MiFIR resubmission costs | ~$150K | Estimated |
| Total | **~$3.05M** | PRELIMINARY |

### KCG Reference Case (for regulatory context)

When drafting the regulatory response, some team members have cited the
Knight Capital Group incident loss of **$440M** as a reference point.

**IMPORTANT**: The $440M figure is an early preliminary estimate that
appeared in news reports on August 1-2, 2012. The **authoritative figure**
confirmed by the SEC in Press Release 2013-222 and in Release No. 34-70694
is **$460,000,000+** (exceeding $460 million). The $440M figure should NOT
be used in regulatory filings.

### Internal Dispute (See Also Feishu Thread)

The quantitative team (Feishu thread, 2024-11-04) disputed the $3.05M
estimate above. Yuki Tanaka argued the T+1 settlement error component
is closer to $1.8M; Marcus Chen estimated $2.4M. Final figures pending
forensic accounting review.

### UTC Offset Impact on Calculations

All loss calculations above must use UTC timestamps, not local time.
The UTC-4 vs UTC-5 discrepancy means that all trades in the 18:00-19:00 UTC
window on 2024-11-03 were executed under incorrect timezone assumptions.
""")

    # 5.3 compliance_checklist_draft.md（不完整，待整改）
    w(WS / "reports" / "compliance_checklist_draft.md", """# Compliance Remediation Checklist — DRAFT

## ArtemisQ Capital — AROS v4.2 Timezone Incident

Date: 2024-11-05 (DRAFT)
Status: INCOMPLETE — Items marked [?] require completion

---

### Section 1: Immediate Fixes

- [x] Trading halted at 22:00 UTC on 2024-11-03
- [x] Root cause identified: hardcoded UTC_OFFSET = -4 in timezone_config.py
- [ ] UTC_OFFSET corrected to -5 in production
- [?] DST-aware library (e.g. pytz/zoneinfo) replacement scheduled

### Section 2: Regulatory Reporting

- [ ] MiFIR Field 28 error report submitted to FCA (OVERDUE)
- [?] T+1 settlement error notification to SEC (deadline TBD)
- [ ] Corrective transaction reports resubmitted in UTC

### Section 3: Root Cause Analysis

- [ ] Full RCA document completed
- [ ] Contributing factors documented
- [ ] Financial impact quantified

### Section 4: Long-Term Remediation

- [?] Rule 15c3-5(b) compliance review
- [?] Rule 15c6-1 T+1 compliance audit
- [ ] DST transition testing protocol established
- [ ] Annual CEO certification updated

---
*This checklist is incomplete and requires completion by compliance team.*
""")


# --------------------------------------------------------------------------- #
# 6. Communications (Slack / Email / Feishu / Discord)
# --------------------------------------------------------------------------- #
def gen_communications() -> None:
    rng = random.Random(20241104)

    # 6.1 slack_incident_channel.json
    slack_msgs = [
        {"ts": "2024-11-03T22:05:00Z", "user": "kenji.nakamura", "channel": "#incident-20241103",
         "text": "AROS v4.2 manually halted. Root cause: UTC_OFFSET hardcoded to -4. "
                 "Should be -5 after EST switch."},
        {"ts": "2024-11-03T22:10:00Z", "user": "marcus.chen", "channel": "#incident-20241103",
         "text": "Confirmed: timezone_config.py line 42, UTC_OFFSET = -4. "
                 "DST_AWARE flag is False. CME settle was 1 hour early."},
        {"ts": "2024-11-03T22:15:00Z", "user": "elena.vasquez", "channel": "#incident-20241103",
         "text": "We need to file MiFIR correction. Field 28 timestamps were UTC-4 local "
                 "time, not UTC. This is a clear FCA Market Watch 59 violation."},
        {"ts": "2024-11-03T22:20:00Z", "user": "marcus.chen", "channel": "#incident-20241103",
         "text": "The v3.1 DEPRECATED router in code/legacy/ has UTC_OFFSET=-5 which "
                 "might look correct, but that file is DEPRECATED. DO NOT reference it."},
        {"ts": "2024-11-03T22:25:00Z", "user": "kenji.nakamura", "channel": "#incident-20241103",
         "text": "@marcus.chen agreed — legacy code is not applicable. v3.1 was deprecated "
                 "2023-06-01 and doesn't meet MiFIR Field 28 UTC or T+1 settlement requirements."},
        {"ts": "2024-11-03T22:30:00Z", "user": "elena.vasquez", "channel": "#incident-20241103",
         "text": "CME daily settlement is 15:00 CT. In EST (post-DST): 15:00 CT = 21:00 UTC. "
                 "System triggered at 20:00 UTC — 1 hour early. All delta-hedge closes are offset."},
        {"ts": "2024-11-04T09:00:00Z", "user": "sophie.devereux", "channel": "#incident-20241103",
         "text": "Draft the MiFIR Field 28 correction memo. Must cite FCA Market Watch 59 "
                 "explicitly. Field 28 requires UTC, not local time. DST errors are specifically "
                 "called out in Market Watch 59 as the most common compliance failure."},
        {"ts": "2024-11-04T09:15:00Z", "user": "marcus.chen", "channel": "#incident-20241103",
         "text": "T+1 rule: Rule 15c6-1 effective 2024-05-28. Cutoff is 21:00 ET. "
                 "With UTC-4 (wrong), cutoff UTC = 01:00 next day. "
                 "With UTC-5 (correct), cutoff UTC = 02:00 next day. "
                 "The 60-minute offset means some orders missed the correct T+1 window."},
        {"ts": "2024-11-04T09:30:00Z", "user": "kenji.nakamura", "channel": "#incident-20241103",
         "text": "For the regulatory response: KCG reference case penalty was $12M "
                 "(Rule 15c3-5(b) violation, Release 34-70694). Don't use the $440M loss figure — "
                 "SEC press release 2013-222 confirms $460M+."},
        {"ts": "2024-11-04T10:00:00Z", "user": "elena.vasquez", "channel": "#incident-20241103",
         "text": "Timeline: 2024-11-03T14:30:00Z was first mis-timed T+1 order. "
                 "Anomaly window: 14:00-15:00 UTC (system thought it was 14:00-15:00 EDT; "
                 "actually 14:00-15:00 EST after switch)."},
    ]
    wj(WS / "communications" / "slack_incident_channel.json", {
        "channel": "#incident-20241103",
        "workspace": "artemisq-capital",
        "messages": slack_msgs,
    })

    # 6.2 email_chain_regulator.eml（FCA/SEC 往来邮件）
    w(WS / "communications" / "email_chain_regulator.eml", """From: sophie.devereux@artemisq.com
To: transaction.reporting@fca.org.uk; sec-compliance@sec.gov
Subject: MiFIR Transaction Reporting Error — ArtemisQ Capital — Field 28 DST Misconfiguration
Date: Mon, 04 Nov 2024 09:45:00 +0000

Dear FCA Transaction Reporting Team,

ArtemisQ Capital is writing to notify you of a data quality issue
identified in our MiFIR transaction reports for 2024-11-03.

**Issue**: Field 28 (trading date and time) timestamps for transactions
executed between 09:30 UTC and 22:00 UTC on 2024-11-03 were submitted
using local Eastern time (UTC-4) instead of the required UTC format.
This is a violation of the UTC reporting requirement described in
FCA Market Watch 59 and RTS 22.

**Root Cause**: Our AROS v4.2 routing system hardcoded a UTC offset of -4
(EDT) which was not updated following the US Eastern DST transition on
2024-11-03 at 02:00 local time (07:00 UTC). After the switch, the correct
offset is -5 (EST).

**Impact**: All Field 28 timestamps for the affected period are offset by
+1 hour from the correct UTC values (e.g., a transaction at 14:30:00 UTC
was reported as 2024-11-03T14:30:00-04:00 instead of 2024-11-03T14:30:00Z).

**Remediation**: We will submit corrected transaction reports within 5
business days. We are implementing an automatic DST detection mechanism
to prevent recurrence.

We will provide a full correction report and compliance action plan to
both regulators within 48 hours.

Sincerely,
Sophie Devereux
Regulatory Affairs Manager, ArtemisQ Capital

---

From: fca-market-transaction-reporting@fca.org.uk
To: sophie.devereux@artemisq.com
Subject: RE: MiFIR Transaction Reporting Error — ArtemisQ Capital — Field 28 DST Misconfiguration
Date: Tue, 05 Nov 2024 10:30:00 +0000

Dear Ms. Devereux,

Thank you for the prompt notification regarding ArtemisQ Capital's Field 28
reporting error for 2024-11-03.

The FCA acknowledges receipt of your notification. Please note:

1. FCA Market Watch 59 clearly states that Field 28 must be reported in UTC.
   DST transition errors are among the most common compliance failures
   identified in our transaction reporting supervision.

2. You are required to submit corrected transaction reports with the correct
   UTC timestamps by 2024-11-12 (5 business days).

3. Please provide a written remediation plan including:
   - Root cause analysis
   - Description of the UTC conversion fix implemented
   - Testing procedures to prevent recurrence at future DST transitions

We are treating this as a data quality issue at this stage. Failure to
provide corrected reports by the deadline may result in formal supervisory action.

Regards,
FCA Transaction Reporting Supervision
Financial Conduct Authority

---

From: sec-mkt-access@sec.gov
To: sophie.devereux@artemisq.com; elena.vasquez@artemisq.com
Subject: RE: MiFIR Transaction Reporting Error — Inquiry re T+1 Settlement
Date: Tue, 05 Nov 2024 15:00:00 +0000

Dear Ms. Vasquez and Ms. Devereux,

The SEC Division of Trading and Markets has been made aware of ArtemisQ
Capital's November 3, 2024 systems incident in which timezone configuration
errors may have affected compliance with Rule 15c6-1 (T+1 settlement cycle,
effective May 28, 2024).

This communication is a PRELIMINARY INQUIRY NOTICE — not a formal
investigation order. Please provide the following within 48 hours of receipt:

1. A quantitative breakdown of affected T+1 orders, including for each:
   - order_id
   - expected_settlement_utc (correct, using UTC-5)
   - actual_settlement_utc (as determined by system with UTC-4 error)
   - price_diff_usd (price difference using end-of-day closing price basis)

2. Total count of affected orders

We are evaluating whether this constitutes a Rule 15c6-1 violation.
This notice does not constitute a formal investigation.

SEC Division of Trading and Markets
""")

    # 6.3 feishu_quant_team.json（含矛盾估算：$440M vs $460M；UTC 偏移值分歧）
    feishu_msgs = [
        {"ts": "2024-11-04T08:00:00Z", "user": "yuki.tanaka",
         "group": "量化团队群",
         "text": "[飞书量化团队群 Yuki Tanaka Mon Nov 04 08:00 UTC 2024] "
                 "我看了 bot_summary 报告，KCG 事故损失是 $440M，"
                 "我们应该用这个数字作为基准来说明我们事故规模相对较小。"},
        {"ts": "2024-11-04T08:10:00Z", "user": "marcus.chen",
         "group": "量化团队群",
         "text": "[飞书量化团队群 Marcus Chen Mon Nov 04 08:10 UTC 2024] "
                 "Yuki，bot 报告不是权威来源。SEC 新闻稿 2013-222 和 Release 34-70694 "
                 "确认的数字是 $460M+，不是 $440M。$440M 是当时的初步新闻报道估算。"},
        {"ts": "2024-11-04T08:15:00Z", "user": "yuki.tanaka",
         "group": "量化团队群",
         "text": "[飞书量化团队群 Yuki Tanaka Mon Nov 04 08:15 UTC 2024] "
                 "好的，我确认了，$460M+ 是正确的 SEC 数字，$440M 不准确。"
                 "另外，关于我们自己的事故：我估算受影响订单损失约 $1.8M，"
                 "但 Marcus 你算的是 $2.4M？"},
        {"ts": "2024-11-04T08:20:00Z", "user": "marcus.chen",
         "group": "量化团队群",
         "text": "[飞书量化团队群 Marcus Chen Mon Nov 04 08:20 UTC 2024] "
                 "我用的时间窗口是 14:00-15:00 UTC（UTC-4 错误窗口），"
                 "统计了 aros_v4_2_audit_log.jsonl 中 status=ANOMALY_DST_MISMATCH 的行数。"
                 "UTC 偏移错误是 -4 而不是正确的 -5，差了 60 分钟。"},
        {"ts": "2024-11-04T08:30:00Z", "user": "elena.vasquez",
         "group": "量化团队群",
         "text": "[飞书量化团队群 Elena Vasquez Mon Nov 04 08:30 UTC 2024] "
                 "暂停内部估算讨论。我们需要先完成 SEC 和 FCA 的正式合规文件。"
                 "MiFIR Field 28 修正报告必须引用 FCA Market Watch 59，"
                 "所有时间戳必须以 UTC 提交（ISO 8601 格式）。"},
        {"ts": "2024-11-04T09:00:00Z", "user": "kenji.nakamura",
         "group": "量化团队群",
         "text": "[飞书量化团队群 Kenji Nakamura Mon Nov 04 09:00 UTC 2024] "
                 "提醒大家：code/legacy/aros_v3_1_router_DEPRECATED.py 那个文件已经"
                 "废弃了（deprecated 2023-06-01），里面虽然有 UTC_OFFSET=-5 但那是"
                 "archive 代码，不符合 MiFIR Field 28 UTC 要求，不能用于修复。"},
    ]
    wj(WS / "communications" / "feishu_quant_team.json", {
        "platform": "Feishu",
        "group": "量化团队群（ArtemisQ Capital）",
        "members": ["elena.vasquez", "marcus.chen", "sophie.devereux",
                    "kenji.nakamura", "yuki.tanaka", "alex.wu",
                    "priya.sharma", "david.lee"],
        "messages": feishu_msgs,
    })

    # 6.4 discord_devops.json（含 v3 废弃版本误引用讨论，V6 红鲱鱼线索）
    discord_msgs = [
        {"ts": "2024-11-03T22:30:00Z", "user": "kenji.nakamura",
         "channel": "#devops-alerts",
         "text": "[Discord #devops-alerts kenji Mon Nov 03 22:30 UTC 2024] "
                 "AROS v4.2 halted. Root cause: UTC_OFFSET hardcoded -4. "
                 "Checking git history to see when this was introduced."},
        {"ts": "2024-11-03T22:45:00Z", "user": "alex.wu",
         "channel": "#devops-alerts",
         "text": "[Discord #devops-alerts alex Mon Nov 03 22:45 UTC 2024] "
                 "Hey I found that aros_v3_1_router_DEPRECATED.py has UTC_OFFSET=-5. "
                 "Maybe we can just copy the timezone logic from there to fix v4.2?"},
        {"ts": "2024-11-03T22:50:00Z", "user": "kenji.nakamura",
         "channel": "#devops-alerts",
         "text": "[Discord #devops-alerts kenji Mon Nov 03 22:50 UTC 2024] "
                 "@alex.wu ABSOLUTELY NOT. That file is DEPRECATED (2023-06-01). "
                 "It doesn't implement MiFIR Field 28 UTC requirement. "
                 "The UTC-5 in that file is a legacy static value without DST handling. "
                 "We need a proper fix using pytz or zoneinfo in v4.2 timezone_config.py."},
        {"ts": "2024-11-03T23:00:00Z", "user": "david.lee",
         "channel": "#devops-alerts",
         "text": "[Discord #devops-alerts david Mon Nov 03 23:00 UTC 2024] "
                 "Deployment log: v4.2 was deployed 2024-10-15 with UTC_OFFSET=-4 (EDT at the time). "
                 "No DST update procedure was in the deployment checklist. "
                 "v4.3 spec should include: 1) zoneinfo-based TZ, 2) DST test cases, "
                 "3) pre-DST-transition validation."},
        {"ts": "2024-11-04T08:00:00Z", "user": "priya.sharma",
         "channel": "#devops-alerts",
         "text": "[Discord #devops-alerts priya Tue Nov 04 08:00 UTC 2024] "
                 "CME settlement time confirmed: 15:00 CT. In EST (after Nov 3 switch): "
                 "CT is UTC-6, so 15:00 CT = 21:00 UTC. "
                 "System was using 20:00 UTC (1 hour early). "
                 "This matches the offset error in timezone_config.py."},
    ]
    wj(WS / "communications" / "discord_devops.json", {
        "platform": "Discord",
        "channel": "#devops-alerts",
        "server": "artemisq-devops",
        "messages": discord_msgs,
    })


# --------------------------------------------------------------------------- #
# 7. Reference 文件（KCG 案例研究 + 闪崩报告 + CME 时间表 + DTCC 指南）
# --------------------------------------------------------------------------- #
def gen_reference() -> None:
    # 7.1 knight_capital_case_study.md（含所有锚点数字）
    w(WS / "reference" / "knight_capital_case_study.md", """# Knight Capital Group — Incident Case Study

## Quantitative Trading Systems Failure: A Regulatory Compliance Reference

**Primary Source**: SEC Administrative Order, Release No. 34-70694 (October 16, 2013)
**Secondary Source**: SEC Press Release 2013-222
**Supplementary Analysis**: Doug Seven, "Knightmare: A DevOps Cautionary Tale" (April 17, 2014)

---

## Case Overview

Knight Capital Americas LLC ("KCG") experienced a catastrophic trading systems
failure on August 1, 2012 due to a software deployment error and inadequate
risk management controls. The incident resulted in the largest single-day trading
loss attributable to an algorithmic trading system error at the time.

---

## Key Facts and Anchors (SEC-Verified)

### Financial Impact
- **Total trading loss**: **$460,000,000+** (exceeding $460 million)
  - Source: SEC Press Release 2013-222
  - Note: Early news reports cited a preliminary estimate of $440 million.
    The **authoritative figure is $460M+** as confirmed by the SEC.
    Do NOT cite $440M in regulatory filings.

### Regulatory Penalty
- **Civil penalty**: **$12,000,000** (twelve million dollars)
  - Settlement with SEC, Admin Proc. File No. 3-15570
  - Rule violated: **Rule 15c3-5(b)** (Market Access Rule)

### Order Statistics
- **Customer orders received**: 212
- **Child orders generated**: 4,000,000+ (in approximately 45 minutes)
- **Stocks affected**: 154 NYSE-listed equities
- **Shares traded**: **397,000,000+** (approximately 3.97 billion shares)
- **Order ratio**: ~18,868 child orders per parent order

### Server Infrastructure
- **Total SMARS servers**: **8**
- **Servers correctly updated**: 7 (received new RLP code)
- **Servers NOT updated**: 1 (8th server retained legacy "Power Peg" code)
- **Deployment period**: July 27 – August 1, 2012 (one server per day)

### Pre-Market Warning Emails
- **Automated emails sent**: **97**
- **Email subject**: "Power Peg disabled"
- **Sent from**: 8:01 AM ET
- **Recipient action**: None taken before market open

### Incident Timeline
| Time | Event |
|------|-------|
| 2012-07-27 | Deployment begins (one server per day) |
| 2012-08-01 | 8th server not updated; NYSE RLP activation |
| 2012-08-01 08:01 AM ET | First automated email "Power Peg disabled" |
| 2012-08-01 09:30 AM ET | Market open; erroneous ordering begins |
| 2012-08-01 ~09:58 AM ET | Engineers identify root cause, disable SMARS |
| 2012-08-01 ~45 min duration | Total time of erroneous ordering |

---

## Rule Violations

**Rule 15c3-5(b)** — Knight failed to maintain adequate financial risk management
controls and supervisory procedures reasonably designed to manage the financial
risks of its market access.

Specific failures:
1. No mechanism to verify all 8 servers received the same code deployment
2. Failure to act on 97 "Power Peg disabled" automated emails
3. Legacy "Power Peg" code (deactivated ~2005) not removed from server
4. No pre-deployment validation environment testing

---

## Lessons for Quantitative Trading Systems

1. **Deployment validation**: Verify all nodes in a cluster received the update
   before market-open (analog: verify UTC_OFFSET correct on all AROS servers)
2. **Alert fatigue prevention**: Automated alerts that are routinely ignored become
   invisible (analog: DST_AWARE=False warning in timezone_config.py)
3. **Legacy code purging**: Deactivated code paths must be fully removed, not just
   commented out (analog: aros_v3_1_router_DEPRECATED.py must not be referenced)
4. **Risk management integration**: Pre-trade and post-trade controls must be
   connected, not siloed (analog: risk_monitor.py disconnected from order_router.py)

---

## Reference for ArtemisQ Capital Compliance Documentation

When citing this case study in regulatory submissions, use the SEC-verified figures:
- Financial loss: $460,000,000+ (NOT $440M)
- Penalty: $12,000,000
- Rule: Rule 15c3-5(b)
- Servers: 8
- Pre-market emails: 97
""")

    # 7.2 flash_crash_2010_report_summary.md
    w(WS / "reference" / "flash_crash_2010_report_summary.md", """# 2010 Flash Crash — Joint SEC/CFTC Report Summary

**Source**: SEC/CFTC Joint Advisory Committee Report, "Findings Regarding the
Market Events of May 6, 2010" (September 30, 2010)
**Reference URL**: https://www.sec.gov/files/marketevents-report.pdf

---

## Event Summary

On **May 6, 2010**, U.S. financial markets experienced one of the most severe
intraday price declines in history, known as the "Flash Crash."

### Key Facts

| Metric | Value |
|--------|-------|
| Date | 2010-05-06 |
| Crash start time | **14:32 EDT** |
| Trigger | Waddell & Reed automated sell order |
| Contracts sold | **75,000 E-Mini S&P 500 contracts** (~$4.1 billion notional) |
| Dow Jones drop | **998.5 points** (~9%) at intraday trough |
| Market cap lost | Approximately $1 trillion (temporarily) |
| CME circuit breaker | Triggered at 14:45:28 EDT |
| Recovery | Markets largely recovered within 36 minutes |

### Waddell & Reed's Algorithm

The sell order used a volume-based execution algorithm (VWAP-style) that
executed at 9% of the trading volume of the prior minute, with no price
or time limits. The algorithm was indifferent to price impact.

### CME Stop Logic Functionality

The CME Globex Stop Logic Functionality triggered at approximately
**14:45:28 PM EDT** on May 6, 2010, briefly pausing E-Mini trading
for approximately 5 seconds. This temporary pause allowed the market
to stabilize and prevented further precipitous decline.

---

## Relevance to Timezone/DST Compliance

The 2010 flash crash highlighted the importance of accurate UTC timestamping
for regulatory purposes:

1. SEC/CFTC post-event analysis relied heavily on precise UTC timestamps
   to reconstruct the sequence of market events
2. MiFIR Field 28 UTC requirement (FCA Market Watch 59) was partly motivated
   by the difficulty of cross-firm event reconstruction when different firms
   used different local-time reporting conventions
3. For CME E-Mini products specifically, settlement timing (15:00 CT) and
   circuit breaker trigger times are always expressed in CT, but must be
   converted to UTC for MiFIR regulatory reporting

---

## CME E-Mini S&P 500 — Settlement Time Reference

For ArtemisQ Capital's 2024-11-03 incident context:

- **CME daily settlement time**: 14:59:30-15:00:00 CT (Central Time)
- **During CDT (April–November, standard)**: CT = UTC-5, so 15:00 CT = **20:00 UTC**
- **During CST (November–March, after DST switch)**: CT = UTC-6, so 15:00 CT = **21:00 UTC**
- **2024-11-03 status**: DST switch occurred at 02:00 ET (07:00 UTC) on Nov 3, 2024;
  therefore for trades on Nov 3 AFTER 07:00 UTC, CT = UTC-6, and CME settlement = **21:00 UTC**

The AROS v4.2 bug caused the system to use 20:00 UTC as the CME settlement reference
on 2024-11-03 instead of the correct 21:00 UTC.
""")

    # 7.3 cme_settlement_schedule.md（含 EDT/EST 对照）
    w(WS / "reference" / "cme_settlement_schedule.md", """# CME Group — E-Mini S&P 500 Daily Settlement Schedule

**Source**: CME Group Trading Hours
**Reference URL**: https://www.cmegroup.com/trading-hours.html

---

## E-Mini S&P 500 Futures (Symbol: ES) — Daily Settlement

### Settlement Window

The daily settlement price for E-Mini S&P 500 futures is determined
during the window **14:59:30 to 15:00:00 CT (Central Time)**.

### UTC Conversion Table

| Period | CT = | CME Settlement CT | CME Settlement UTC |
|--------|------|-------------------|-------------------|
| CDT (summer; Apr–Nov 1st Sun) | UTC-5 | 15:00:00 CT | **20:00:00 UTC** |
| CST (winter; Nov 1st Sun–Mar) | UTC-6 | 15:00:00 CT | **21:00:00 UTC** |

### 2024 DST Transition Dates

| Event | Date | Local Time | UTC Time |
|-------|------|------------|----------|
| Spring Forward (EDT begins) | 2024-03-10 | 02:00 ET → 03:00 ET | 07:00 UTC |
| Fall Back (EST begins) | **2024-11-03** | **02:00 ET → 01:00 ET** | **07:00 UTC** |

### Impact on 2024-11-03 Settlement

On 2024-11-03, the US Eastern timezone switched from EDT (UTC-4) to EST (UTC-5)
at 02:00 local time (07:00 UTC). Therefore:

- All CME trading from **07:00 UTC onward** on 2024-11-03 occurred in the **EST** period
- Central Time = UTC-6 from 07:00 UTC onward on 2024-11-03
- CME daily settlement at 15:00:00 CT = **21:00:00 UTC** on 2024-11-03

**Any system that used UTC-5 for CT on 2024-11-03 (assuming CT=UTC-5 all day)
computed CME settlement as 20:00:00 UTC — exactly 1 hour early.**

### Verification Note

The AROS v4.2 system computed CME settlement as 20:00:00 UTC on 2024-11-03
because it hardcoded the ET offset as UTC-4, leading it to compute:
CT offset = ET offset - 1 = (-4) - 1 = -5
15:00 CT = 15:00 + 5h = 20:00 UTC  ← WRONG

Correct calculation:
CT offset = EST offset - 1 = (-5) - 1 = -6
15:00 CT = 15:00 + 6h = 21:00 UTC  ← CORRECT

---

## Trading Hours Summary (E-Mini S&P 500)

| Session | Hours (CT) | Note |
|---------|-----------|------|
| Pre-open | 17:00 prior day – 08:30 | Electronic access |
| Regular | 08:30 – 15:15 | NYSE synchronised open |
| Settlement window | 14:59:30 – 15:00:00 | Daily settlement reference |
| Post-close | 15:15 – 16:00 | Limited trading |
| Electronic | 17:00 – 16:00 next day | Nearly 24h with 1h break |
""")

    # 7.4 dtcc_t1_conversion_guide.md
    w(WS / "reference" / "dtcc_t1_conversion_guide.md", """# DTCC T+1 Settlement Conversion Guide (March 2024 Update)

**Source**: DTCC, "The Move to T+1: Conversion Guide," March 2024
**Reference URL**: https://www.dtcc.com/-/media/Files/PDFs/T2/T1-Conversion-Document-March-2024.pdf

---

## Overview

The US securities settlement cycle shortened from T+2 to T+1 effective
**May 28, 2024** under SEC Rule 15c6-1 (amended February 15, 2023).

## Key Metrics Post-T+1 Transition

| Metric | Pre-T+1 | Post-T+1 (YTD Dec 2024) |
|--------|---------|------------------------|
| Same-day affirmation rate | ~73% | **97%** |
| Fails rate | Baseline | Significantly reduced |
| Settlement cycle | T+2 | T+1 |

## Scope of T+1 Rule

Transactions that must now settle T+1:
- Exchange-listed equities (NYSE, NASDAQ, etc.)
- Corporate debt securities
- Unit investment trusts (UITs)
- Certain limited partnership interests traded on exchanges

Excluded from T+1 (remain T+2 or longer):
- Government securities (already T+1)
- Municipal bonds (separate Rule 15c6-1 provision)
- OTC derivatives

## Settlement Cutoff Times Under T+1

| Milestone | Time (ET) | Impact on UTC calculation |
|-----------|-----------|--------------------------|
| Trade execution | During market hours | Must use correct UTC-4/UTC-5 per season |
| Affirmation cutoff | 21:00 ET same day | UTC = 21:00 + abs(offset) |
| DTC settlement | 16:00 ET next business day | Settlement completion |

**DST impact on cutoff UTC**:
- EDT period (UTC-4): 21:00 ET cutoff = 01:00 UTC next calendar day
- EST period (UTC-5): 21:00 ET cutoff = 02:00 UTC next calendar day

Systems must account for DST transitions when computing settlement cutoffs.
The 1-hour difference between EDT and EST cutoff UTC times can cause orders
to be classified as T+1 vs T+2 incorrectly.

## Rule 17Ad-27 — Straight-Through Processing

The SEC also adopted Rule 17Ad-27, requiring registered clearing agencies
to maintain policies for straight-through processing (STP). DTCC's Target
STP rate post-T+1: maintain ≥97% same-day affirmation.

---

## Relevance to AROS v4.2 Incident

The 2024-11-03 AROS v4.2 incident occurred on the first day of the
post-DST EST period, approximately 5 months after T+1 became effective.
Systems that had adapted for T+1 but did not implement DST-aware UTC
computation faced precisely this scenario: correct T+1 logic but with
1-hour offset in the UTC cutoff calculation.

Reference settlement calculations:
- Trade date: 2024-11-03
- T+1 settlement date: 2024-11-04
- T+1 cutoff (correct, UTC-5 EST): 2024-11-04T02:00:00Z
- T+1 cutoff (wrong, UTC-4 bug): 2024-11-04T01:00:00Z
- Orders submitted between 01:00-02:00 UTC on 2024-11-04: missed T+1 window
  (were classified as T+1 by system, but are actually T+2 under correct calculation)
""")


# --------------------------------------------------------------------------- #
# 8. Sessions（主 + 4 history）
# --------------------------------------------------------------------------- #
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("incident_slack", TID)
    s_email = gen_session_id("regulator_email", TID)
    s_feishu = gen_session_id("quant_feishu", TID)
    s_discord = gen_session_id("devops_discord", TID)

    # 主 session：背景 + 工作框架 + Preference 声明
    sb = SessionBuilder(main_id, CWD, "2024-11-04T10:00:00Z", is_main=True)
    sb.add_user(
        "You are ComplianceOps AI, the quantitative compliance engineering assistant "
        "for Elena Vasquez (Chief Compliance Officer) at ArtemisQ Capital.\n\n"
        "Background: On 2024-11-03, the AROS v4.2 system experienced a timezone "
        "misconfiguration after the US Eastern DST transition (EDT UTC-4 → EST UTC-5). "
        "The system had hardcoded UTC_OFFSET = -4 and failed to update after the switch, "
        "causing T+1 settlement orders to use wrong cutoff times and MiFIR Field 28 "
        "timestamps to be submitted as local time instead of UTC.\n\n"
        "Your mission: post-incident remediation — incident timeline, root cause analysis, "
        "MiFIR Field 28 correction report, T+1 impact analysis, corrective action plan.\n\n"
        "House preferences (apply throughout, even when not restated):\n"
        "- P1: All JSON outputs must use snake_case field naming (never camelCase or PascalCase).\n"
        "- P2: All errors/issues arrays must be sorted by severity, descending (most severe first).\n"
        "- P3: All regulatory document citations must include the specific sub-clause or field "
        "number (e.g. 'Rule 15c3-5(b)', 'Field 28', not just 'Rule 15c3-5' or 'a Field').\n"
        "- P4: Corrective action plan items must each include an 'owner' field.\n"
        "- P5: Regulatory submission JSON must follow field order: incident_date → "
        "rule_violated → financial_impact → remediation_count → submission_date.\n\n"
        "History sessions available (Slack #incident-20241103 / Email chain / Feishu 量化团队群 / "
        "Discord #devops-alerts). Begin by reading SOUL.md and inspecting workspace files."
    )
    sb.add_assistant(
        "Understood. I have read AGENTS.md and SOUL.md. Working framework:\n"
        "1. All source documents under incident/, regulatory/, code/, reports/, reference/ "
        "are read-only inputs. Deliverables go under output/.\n"
        "2. MiFIR Field 28 requires UTC timestamps (FCA Market Watch 59). "
        "Bot summaries are not authoritative — verify all numbers against primary sources.\n"
        "3. T+1 rule: Rule 15c6-1 effective 2024-05-28. UTC offset error: -4 (wrong) vs -5 (correct, EST).\n"
        "4. House preferences applied: snake_case JSON (P1), severity-descending arrays (P2), "
        "sub-clause citations (P3), owner fields in CAP (P4), fixed field order for regulatory JSON (P5).\n"
        "Ready for the first task."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # S2 Slack — 事故响应协调
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2024-11-03T22:00:00Z",
        [
            ("[Slack #incident-20241103 kenji.nakamura Mon Nov 04 22:05 UTC 2024] "
             "AROS v4.2 manually halted. timezone_config.py line 42: UTC_OFFSET = -4 "
             "(should be -5 after Nov 3 DST switch). CME settlement triggered 1 hour early.",
             "Confirmed root cause: UTC_OFFSET = -4 hardcoded, not updated after EDT→EST switch. "
             "CME daily settlement at 15:00 CT = 21:00 UTC in EST (not 20:00 UTC). "
             "T+1 cutoff also offset by 60 minutes."),
            ("[Slack #incident-20241103 sophie.devereux Tue Nov 04 09:15 UTC 2024] "
             "MiFIR Field 28 correction required. FCA Market Watch 59 is explicit: "
             "Field 28 must be UTC, not local time. DST errors are the most common failure. "
             "KCG reference: penalty $12M, rule Rule 15c3-5(b), loss $460M+ (not $440M).",
             "Noted. Field 28 correction: affected period 2024-11-03T09:30:00Z to 22:00:00Z. "
             "All timestamps were offset by +1 hour (reported as UTC-4 local instead of UTC). "
             "KCG anchor: $460M+ loss (SEC 2013-222), $12M penalty, Rule 15c3-5(b)."),
            ("[Slack #incident-20241103 marcus.chen Tue Nov 04 09:30 UTC 2024] "
             "The deprecated v3.1 router in code/legacy/ has UTC_OFFSET=-5 but that file "
             "is DEPRECATED 2023-06-01 and doesn't meet MiFIR UTC requirements. "
             "It cannot be used to fix the current incident.",
             "Confirmed: aros_v3_1_router_DEPRECATED.py is deprecated 2023-06-01 "
             "and is not applicable to the current remediation. "
             "Fix must be in the current v4.2 codebase (code/aros/timezone_config.py)."),
        ]
    )

    # S3 Email — 监管往来邮件
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2024-11-04T09:45:00Z",
        [
            ("[Email sophie.devereux → fca Mon Nov 04 09:45 UTC 2024] "
             "Notifying FCA of Field 28 UTC timestamp error on 2024-11-03. "
             "Root cause: hardcoded UTC-4 offset not updated after DST switch.",
             "Email logged: FCA notification sent for Field 28 DST error. "
             "Affected period: 2024-11-03T09:30Z to 22:00Z. "
             "FCA response expected within 1 business day."),
            ("[Email fca → sophie.devereux Tue Nov 05 10:30 UTC 2024] "
             "FCA acknowledges Field 28 error. Corrected reports required by 2024-11-12. "
             "Provide: root cause analysis, UTC conversion fix, DST test procedures.",
             "FCA deadline noted: corrected reports by 2024-11-12 (5 business days). "
             "Required deliverables: RCA, UTC fix description, DST test procedures."),
            ("[Email sec-mkt-access → elena.vasquez Tue Nov 05 15:00 UTC 2024] "
             "SEC preliminary inquiry notice re T+1 settlement (Rule 15c6-1 effective 2024-05-28). "
             "Required within 48 hours: order-level breakdown with order_id, "
             "expected_settlement_utc, actual_settlement_utc, price_diff_usd. "
             "This is a PRELIMINARY INQUIRY NOTICE, not a formal investigation.",
             "SEC inquiry noted. 48-hour deadline. Required fields: "
             "order_id, expected_settlement_utc, actual_settlement_utc, price_diff_usd. "
             "Note: preliminary inquiry — not yet a formal investigation order."),
        ]
    )

    # S4 Feishu — 量化团队内部讨论
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2024-11-04T08:00:00Z",
        [
            ("[飞书量化团队群 Yuki Tanaka Mon Nov 04 08:00 UTC 2024] "
             "我看了 bot_summary，KCG 损失是 $440M 作为参照基准。",
             "提醒：bot_summary 不是权威来源。SEC 2013-222 确认 KCG 损失为 $460M+（不是 $440M）。"
             "请使用 regulatory/sec_release_34_70694_full.md 中的数字。"),
            ("[飞书量化团队群 Marcus Chen Mon Nov 04 08:20 UTC 2024] "
             "UTC 偏移错误：系统用 -4（EDT），应为 -5（EST）。"
             "T+1 截止时间：21:00 ET，UTC-4 时 = 01:00 UTC 次日，UTC-5 时 = 02:00 UTC 次日。"
             "差 60 分钟，影响 01:00-02:00 UTC 窗口内的订单。",
             "确认：UTC 偏移差值 = 60 分钟。受影响订单窗口：2024-11-04T01:00Z 至 02:00Z。"
             "这些订单在系统判断中属于 T+1，但按正确时区应属于 T+2。"),
            ("[飞书量化团队群 Kenji Nakamura Mon Nov 04 09:00 UTC 2024] "
             "code/legacy/aros_v3_1_router_DEPRECATED.py 已废弃（2023-06-01）。"
             "其中 UTC_OFFSET=-5 是旧静态值，不符合 MiFIR Field 28 UTC 要求，不可用于修复。",
             "确认：deprecated 代码不适用于当前修复。"
             "所有 V6 红鲱鱼：legacy 代码引用即错，is_applicable 须为 false。"),
        ]
    )

    # S5 Discord — DevOps 告警讨论
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, CWD, "2024-11-03T22:30:00Z",
        [
            ("[Discord #devops-alerts kenji Mon Nov 03 22:30 UTC 2024] "
             "AROS v4.2 halted. UTC_OFFSET hardcoded -4; should be -5 after DST switch. "
             "CME settlement: 15:00 CT = 21:00 UTC (EST), not 20:00 UTC.",
             "Confirmed: CME daily settlement 15:00 CT = 21:00 UTC in EST period. "
             "System error: used 20:00 UTC (1 hour early)."),
            ("[Discord #devops-alerts alex Tue Nov 03 22:45 UTC 2024] "
             "Found aros_v3_1_router_DEPRECATED.py has UTC_OFFSET=-5. "
             "Can we copy timezone logic from it to fix v4.2?",
             "No — aros_v3_1_router_DEPRECATED.py is DEPRECATED (2023-06-01). "
             "It does not implement MiFIR Field 28 UTC requirement. "
             "Not applicable to current remediation."),
            ("[Discord #devops-alerts david Tue Nov 04 08:00 UTC 2024] "
             "CME settlement confirmed: 15:00 CT in EST (post-Nov-3) = 21:00 UTC. "
             "Deployment log shows v4.2 deployed 2024-10-15 with UTC-4 (correct for EDT at the time). "
             "DST update procedure missing from deployment checklist.",
             "Root cause confirmed in deployment checklist gap. "
             "v4.3 spec must include DST-aware timezone library and pre-DST validation tests."),
        ]
    )

    return {
        "main": main_id,
        "history": [
            (s_slack, "slack"),
            (s_email, "email"),
            (s_feishu, "feishu"),
            (s_discord, "discord"),
        ],
    }


# --------------------------------------------------------------------------- #
# 9. Updates（含 supersede）
# --------------------------------------------------------------------------- #
def gen_updates(sess_ids: dict) -> dict:
    # UPDATE 1（Round 9-10 间）：SEC 追加要求 + 受影响订单明细 CSV
    # 约 160KB（~40k tokens）
    rng = random.Random(20241105)

    # 9.1 Update 1 — SEC 询问信 + 受影响订单明细
    w(UPD / "upd1_workspace" / "regulatory" / "sec_inquiry_letter_20241105.md", """# SEC Preliminary Inquiry Letter — ArtemisQ Capital
## Rule 15c6-1 T+1 Settlement Compliance Review
## Date: 2024-11-05

**From**: SEC Division of Trading and Markets
**To**: Elena Vasquez, Chief Compliance Officer, ArtemisQ Capital
**Re**: T+1 Settlement System Compliance — AROS v4.2 Incident 2024-11-03

**THIS IS A PRELIMINARY INQUIRY NOTICE — NOT A FORMAL INVESTIGATION ORDER**

---

## Background

The SEC has been informed that ArtemisQ Capital's AROS v4.2 automated routing
system experienced a timezone configuration error on 2024-11-03 that may have
affected compliance with Rule 15c6-1 (T+1 settlement cycle, effective 2024-05-28).

Specifically, a UTC offset error of 1 hour (system used UTC-4 instead of correct
UTC-5 for EST) may have caused T+1 settlement cutoff calculations to be off by
60 minutes, potentially causing orders to be misclassified between T+1 and T+2.

## Required Information — 48-Hour Deadline

Please provide the following information within 48 hours of receipt of this notice
(deadline: **2024-11-07T15:00:00Z**):

### Required Fields for Each Affected Order

For every order affected by the UTC offset error (orders in the period
2024-11-03T14:00:00Z to 2024-11-04T02:00:00Z), provide:

1. `order_id` — Unique order identifier
2. `expected_settlement_utc` — Correct T+1 settlement cutoff using UTC-5 (EST)
3. `actual_settlement_utc` — System-computed T+1 cutoff using UTC-4 (bug)
4. `price_diff_usd` — Price differential calculated using **end-of-day closing price**
   basis (not VWAP)

### Summary Statistics

- Total count of affected orders

### Format

Please provide the order-level data in CSV format with the header:
`order_id,expected_settlement_utc,actual_settlement_utc,price_diff_usd`

---

## Timeline Implications

Rule 15c6-1 requires T+1 settlement for:
- Equities (exchange-listed)
- Corporate debt
- Unit investment trusts

**Effective date**: 2024-05-28
**Key UTC cutoff**: 21:00 ET = **02:00 UTC (next calendar day)** using correct UTC-5 (EST)

Orders submitted after the correct T+1 cutoff (02:00 UTC on 2024-11-04) but
before the system's incorrect cutoff (01:00 UTC on 2024-11-04 + 60 minutes =
02:00 UTC but computed as 01:00 by bug) require analysis.

---

## Next Steps

This notice is a data collection request. The SEC will evaluate the response
before determining whether formal investigation proceedings are warranted.

SEC Division of Trading and Markets
2024-11-05T15:00:00Z
""")

    # 受影响订单明细 CSV（约 120KB）
    affected_rows = [["order_id", "event_time_utc", "instrument", "side",
                      "qty", "price", "venue",
                      "settlement_date_system", "settlement_date_correct",
                      "utc_offset_system", "utc_offset_correct"]]
    # 事故窗口：18:00-19:00 UTC（系统认为是 14:00-15:00 EDT，实为 14:00-15:00 EST）
    base_t = datetime(2024, 11, 3, 14, 0, 0, tzinfo=timezone.utc)
    cutoff_correct_dt = datetime(2024, 11, 4, 2, 0, 0, tzinfo=timezone.utc)
    for i in range(1200):
        ts = base_t + timedelta(seconds=i * 3.0)
        price = round(rng.uniform(4540.0, 4590.0), 2)
        qty = rng.randint(1, 10)
        # System (wrong): settlement date uses UTC-4 cutoff (01:00 UTC Nov 4)
        system_settle = "2024-11-04" if ts.hour < 25 else "2024-11-05"
        # Correct: cutoff is 02:00 UTC Nov 4 (21:00 ET with UTC-5)
        correct_settle = "2024-11-04" if ts < cutoff_correct_dt else "2024-11-05"
        affected_rows.append([
            f"ORD-{20241103000000 + i:016d}",
            ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
            rng.choice(["ESZ4", "NQZ4"]),
            rng.choice(["BUY", "SELL"]),
            qty,
            price,
            "CME",
            system_settle,
            correct_settle,
            "-04:00",
            "-05:00",
        ])
    buf = io.StringIO()
    csv.writer(buf).writerows(affected_rows)
    w(UPD / "upd1_workspace" / "incident" / "affected_orders_detail.csv", buf.getvalue())

    upd1_order_count = len(affected_rows) - 1  # minus header = 1200

    # UPDATE 2（Round 10-11 间，含 supersede）：
    # 法务撤销部分要求：price_diff_usd → price_diff_vwap_usd（VWAP 基准取代收盘价）
    w(UPD / "upd2_workspace" / "regulatory" / "legal_counsel_memo_20241106.md", f"""# Legal Counsel Memorandum — ArtemisQ Capital
## Re: SEC Preliminary Inquiry — Field Specification Revision
## Date: 2024-11-06

**From**: ArtemisQ Capital Legal Counsel (external)
**To**: Elena Vasquez, Chief Compliance Officer
**Re**: Revision to SEC Inquiry Response Field Specification

---

## URGENT — SUPERSEDES PRIOR INSTRUCTION

This memorandum **SUPERSEDES** the field specification in the SEC's
preliminary inquiry letter of 2024-11-05 regarding the calculation method
for price differentials.

### Background

Further review of the SEC preliminary inquiry letter (2024-11-05) confirms:
1. The letter is a **preliminary inquiry notice**, NOT a formal investigation order
2. The "price_diff_usd" field specified in the inquiry should be revised
   to use **VWAP (Volume Weighted Average Price) basis** rather than
   end-of-day closing price, as VWAP provides a more accurate representation
   of execution quality in automated market-making contexts

### Supersede Rule — CRITICAL

**Effective immediately, the field `price_diff_usd` is REPLACED by
`price_diff_vwap_usd` in all affected order reports.**

| Old Field (SUPERSEDED) | New Field (REQUIRED) | Basis |
|------------------------|---------------------|-------|
| `price_diff_usd` | `price_diff_vwap_usd` | VWAP, not closing price |

**Any report using `price_diff_usd` after receipt of this memo is NON-COMPLIANT
with our revised submission specification.**

### Revised Required Fields

For the order-level difference report (Round 11 deliverable), use:
```
order_id, expected_settlement_utc, actual_settlement_utc, price_diff_vwap_usd
```

NOT the old specification:
```
order_id, expected_settlement_utc, actual_settlement_utc, price_diff_usd  ← SUPERSEDED
```

### VWAP Calculation Basis

Price differentials should be calculated as:
`price_diff_vwap_usd = (execution_price - vwap_reference) * quantity`

Where `vwap_reference` is the 5-minute VWAP at the time of the affected order.
For the purposes of this regulatory submission, VWAP values are provided in
the revised field specification document.

---

Legal Counsel
ArtemisQ Capital
2024-11-06T10:00:00Z
""")

    w(UPD / "upd2_workspace" / "regulatory" / "revised_field_spec_v2.md", f"""# Revised Order-Level Report Field Specification — v2
## ArtemisQ Capital — SEC Response
## Issued: 2024-11-06 (supersedes v1 specification in SEC inquiry letter 2024-11-05)

---

## SUPERSEDE NOTICE

This document **supersedes** the field specification in the SEC preliminary
inquiry letter dated 2024-11-05. The key change is:

- `price_diff_usd` (closing price basis) → **`price_diff_vwap_usd`** (VWAP basis)

---

## Revised CSV Field Specification (v2)

The order-level difference report must use the following column names EXACTLY:

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | string | Unique order identifier |
| `expected_settlement_utc` | ISO 8601 UTC string | Correct T+1 cutoff (UTC-5, EST) |
| `actual_settlement_utc` | ISO 8601 UTC string | System cutoff (UTC-4 bug) |
| `price_diff_vwap_usd` | float | Price difference using VWAP basis (NOT closing price) |

**Column names must be verbatim. `price_diff_usd` is SUPERSEDED.**

---

## Affected Order Count

Total affected orders (from `incident/affected_orders_detail.csv`): **{upd1_order_count}**

---

## VWAP Reference Data

VWAP reference prices for the affected period (2024-11-03T14:00:00Z to 2024-11-03T15:00:00Z):

| 5-min Window Start | ESZ4 VWAP | NQZ4 VWAP |
|--------------------|-----------|-----------|
| 14:00:00Z | 4562.50 | 19840.25 |
| 14:05:00Z | 4563.75 | 19842.00 |
| 14:10:00Z | 4561.00 | 19839.50 |
| 14:15:00Z | 4564.25 | 19843.75 |
| 14:20:00Z | 4565.00 | 19845.00 |
| 14:25:00Z | 4562.25 | 19841.25 |
| 14:30:00Z | 4563.50 | 19840.75 |
| 14:35:00Z | 4564.75 | 19842.50 |
| 14:40:00Z | 4565.25 | 19844.25 |
| 14:45:00Z | 4563.00 | 19841.00 |
| 14:50:00Z | 4562.75 | 19840.50 |
| 14:55:00Z | 4564.00 | 19843.00 |

---

*Version: v2 | Issued: 2024-11-06 | Supersedes: v1 (SEC inquiry letter 2024-11-05)*
""")

    # Update 2 additional: VWAP reference CSV（体量撑起 >30k tokens）
    vwap_rng = random.Random(20241106)
    vwap_rows = [["window_start_utc", "instrument", "vwap_usd", "volume_lots",
                  "open_usd", "high_usd", "low_usd", "close_usd",
                  "num_trades", "tick_direction", "dst_correct_local",
                  "exchange_session", "circuit_breaker_active"]]
    instruments = ["ESZ4", "NQZ4", "RTYH5", "YMH5", "MES"]
    sessions = ["pre_open", "regular", "post_close"]
    # Generate 1-minute bars for affected window + context: ~120 minutes × 5 instruments = 600 rows
    for minute in range(120):
        ts = datetime(2024, 11, 3, 9, 0, 0, tzinfo=timezone.utc) + timedelta(minutes=minute)
        for instr in instruments:
            base_price = 4562.50 if instr == "ESZ4" else (19840.25 if instr == "NQZ4" else 2198.5)
            vwap_price = round(base_price + vwap_rng.uniform(-5.0, 5.0), 2)
            vol = vwap_rng.randint(50, 2000)
            o = round(vwap_price + vwap_rng.uniform(-1.5, 1.5), 2)
            h = round(max(o, vwap_price) + vwap_rng.uniform(0, 2.0), 2)
            lo = round(min(o, vwap_price) - vwap_rng.uniform(0, 2.0), 2)
            cl = round(vwap_price + vwap_rng.uniform(-1.0, 1.0), 2)
            # After DST switch (07:00 UTC = 02:00 ET), EST local = UTC-5
            local_est = ts - timedelta(hours=5)
            sess = "pre_open" if ts.hour < 14 else ("regular" if ts.hour < 21 else "post_close")
            vwap_rows.append([
                ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
                instr,
                vwap_price,
                vol,
                o, h, lo, cl,
                vwap_rng.randint(10, 500),
                vwap_rng.choice(["up", "down", "flat"]),
                local_est.strftime("%Y-%m-%dT%H:%M:%S"),
                sess,
                False,
            ])
    vwap_buf = io.StringIO()
    csv.writer(vwap_buf).writerows(vwap_rows)
    w(UPD / "upd2_workspace" / "incident" / "vwap_reference_20241103.csv", vwap_buf.getvalue())

    # Update 2 additional: VWAP methodology document (体量补充)
    w(UPD / "upd2_workspace" / "regulatory" / "vwap_methodology_note.md", """# VWAP Price Differential Methodology Note
## ArtemisQ Capital — SEC Response — 2024-11-06

## Overview

This note describes the Volume Weighted Average Price (VWAP) calculation
methodology to be applied in the revised order-level difference report,
per the legal counsel memorandum of 2024-11-06 which superseded the
closing-price basis initially specified in the SEC preliminary inquiry.

## Why VWAP Instead of Closing Price?

The original SEC preliminary inquiry letter (2024-11-05) specified
`price_diff_usd` using end-of-day closing price. Legal counsel has revised
this to VWAP basis (`price_diff_vwap_usd`) for the following reasons:

1. **Market-making context**: ArtemisQ Capital's AROS v4.2 is an automated
   market-making system. VWAP provides a more statistically appropriate
   baseline for evaluating execution quality in high-frequency market-making.

2. **Regulatory precedent**: VWAP-based trade analysis is standard in SEC
   and FCA enforcement proceedings involving automated trading systems.

3. **Reduced outlier sensitivity**: End-of-day closing prices on 2024-11-03
   may be affected by post-DST-transition volatility, making VWAP a more
   robust reference.

## VWAP Calculation Formula

For each affected order:
```
price_diff_vwap_usd = (execution_price - vwap_reference_price) * quantity
```

Where `vwap_reference_price` is the 5-minute VWAP for the instrument
at the time of order execution, as provided in the attached
`incident/vwap_reference_20241103.csv` file.

## Reference Data Schema

The VWAP reference data (`incident/vwap_reference_20241103.csv`) contains:

| Column | Type | Description |
|--------|------|-------------|
| `window_start_utc` | ISO 8601 UTC | Start of 1-minute bar in UTC |
| `instrument` | string | CME instrument code (ESZ4, NQZ4, etc.) |
| `vwap_usd` | float | Volume-weighted average price for the bar |
| `volume_lots` | int | Total volume in lots for the bar |
| `open_usd` | float | Bar open price |
| `high_usd` | float | Bar high price |
| `low_usd` | float | Bar low price |
| `close_usd` | float | Bar close price |
| `num_trades` | int | Number of trades in the bar |
| `tick_direction` | string | up/down/flat |
| `dst_correct_local` | ISO 8601 | Correct EST local time (UTC-5 after switch) |
| `exchange_session` | string | pre_open/regular/post_close |
| `circuit_breaker_active` | bool | CME circuit breaker status |

## VWAP Reference Values for Affected Period

The anomaly window (2024-11-03T14:00:00Z to 15:00:00Z) uses the
following VWAP reference prices (from 5-minute aggregation):

| Window (UTC) | ESZ4 VWAP | NQZ4 VWAP | RTYH5 VWAP |
|--------------|-----------|-----------|------------|
| 14:00 | 4562.50 | 19840.25 | 2197.80 |
| 14:05 | 4563.75 | 19842.00 | 2198.50 |
| 14:10 | 4561.00 | 19839.50 | 2197.20 |
| 14:15 | 4564.25 | 19843.75 | 2199.10 |
| 14:20 | 4565.00 | 19845.00 | 2200.00 |
| 14:25 | 4562.25 | 19841.25 | 2198.00 |
| 14:30 | 4563.50 | 19840.75 | 2197.90 |
| 14:35 | 4564.75 | 19842.50 | 2198.75 |
| 14:40 | 4565.25 | 19844.25 | 2199.50 |
| 14:45 | 4563.00 | 19841.00 | 2198.20 |
| 14:50 | 4562.75 | 19840.50 | 2197.80 |
| 14:55 | 4564.00 | 19843.00 | 2198.90 |

## Data Integrity Notes

- All VWAP timestamps in `vwap_reference_20241103.csv` are in UTC
- The `dst_correct_local` column shows the correct EST local time
  (UTC-5) for reference — contrast with the AROS system's incorrect
  UTC-4 local time during the incident
- Circuit breaker activity was NOT triggered during the affected period
  (2024-11-03T14:00-15:00 UTC)

---

*Issued: 2024-11-06 | Supersedes: closing price methodology from SEC inquiry 2024-11-05*
""")

    # UPDATE 3（Round 14-15 间）：SEC 正式立案 + 回测脚本模板
    w(UPD / "upd3_workspace" / "regulatory" / "sec_formal_investigation_20241110.md", """# SEC Formal Investigation Notice — ArtemisQ Capital
## SEC Division of Trading and Markets — Case No. TM-2024-1103-AQ
## Date: 2024-11-10

**From**: SEC Division of Trading and Markets
**To**: Elena Vasquez, Chief Compliance Officer, ArtemisQ Capital
**Re**: FORMAL INVESTIGATION — Rule 15c6-1 T+1 Compliance

---

## FORMAL INVESTIGATION ORDER

Following review of ArtemisQ Capital's response to our preliminary inquiry
notice of 2024-11-05, the SEC Division of Trading and Markets has determined
that a **formal investigation** under SEC Case No. TM-2024-1103-AQ is warranted.

## Additional Requirement: System Backtest Certification

In addition to the order-level data already submitted, ArtemisQ Capital is
required to provide a **system backtest certification** demonstrating that:

1. The corrected UTC-5 (EST) timezone configuration correctly computes
   T+1 settlement cutoffs and CME settlement reference times for the
   2024-11-03 trade date scenario

2. The certification must be in the form of a backtest script output
   showing the correct simulated settlement time matches the expected value

### Backtest Requirements

The backtest must demonstrate:
- Configuration: `config_timezone_offset = -5` (EST, correct)
- Expected CME settlement: **2024-11-03T21:00:00Z** (not the buggy 20:00 UTC)
- Expected T+1 cutoff: **2024-11-04T02:00:00Z** (not the buggy 01:00 UTC)
- `match = true` (simulated settlement matches expected)

A template backtest script is provided at:
`regulatory/sec_backtest_template.py`

### SHA-256 Reference Requirement

The backtest certification must reference the SHA-256 hash from your
previously submitted `output/report_signoff.txt` to confirm data chain
of custody.

### Deadline

Backtest certification due: **2024-11-17T15:00:00Z**

SEC Division of Trading and Markets
Case No. TM-2024-1103-AQ
2024-11-10T15:00:00Z
""")

    w(UPD / "upd3_workspace" / "regulatory" / "sec_backtest_template.py", '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sec_backtest_template.py — SEC Backtest Certification Script Template
ArtemisQ Capital — Case No. TM-2024-1103-AQ

Instructions:
  1. Fill in the CORRECT timezone offset (CONFIG_TIMEZONE_OFFSET = -5)
  2. Run this script to produce output/backtest_result.json
  3. Verify that simulated_settlement_utc matches expected_settlement_utc
  4. If match = true, the backtest is certified

Usage:
  python regulatory/sec_backtest_template.py
"""

import datetime
import json
import sys
from pathlib import Path

# ============================================================
# CONFIGURATION — Fill in the correct values
# ============================================================

# Timezone offset to test (correct EST value = -5)
# AROS v4.2 bug used: -4 (EDT, incorrect after DST switch)
CONFIG_TIMEZONE_OFFSET = -5  # Fill in: correct EST value

# Trade date for the incident scenario
TRADE_DATE = datetime.date(2024, 11, 3)

# CME E-Mini daily settlement: 15:00 CT
# CT = ET - 1; in EST period, CT = UTC-6; so 15:00 CT = 15:00 + 6 = 21:00 UTC
CME_SETTLE_HOUR_CT = 15
CME_SETTLE_MINUTE_CT = 0

SCRIPT_VERSION = "1.0-template"

# ============================================================
# COMPUTATION
# ============================================================

def compute_cme_settle_utc(utc_offset_et: int) -> datetime.datetime:
    """
    Compute CME E-Mini settlement UTC for the given ET UTC offset.
    CT = ET - 1 (Central is 1 hour behind Eastern).
    CME settlement = 15:00 CT = 15:00 + abs(CT_UTC_offset) in UTC.
    """
    ct_utc_offset = utc_offset_et - 1  # CT is 1h behind ET
    settle_ct = datetime.datetime(
        TRADE_DATE.year, TRADE_DATE.month, TRADE_DATE.day,
        CME_SETTLE_HOUR_CT, CME_SETTLE_MINUTE_CT, 0
    )
    # Convert CT to UTC: UTC = CT - ct_utc_offset
    settle_utc = settle_ct - datetime.timedelta(hours=ct_utc_offset)
    return settle_utc


def compute_t1_cutoff_utc(utc_offset_et: int) -> datetime.datetime:
    """
    Compute T+1 settlement cutoff UTC (21:00 ET per Rule 15c6-1).
    """
    cutoff_et = datetime.datetime(
        TRADE_DATE.year, TRADE_DATE.month, TRADE_DATE.day, 21, 0, 0
    )
    cutoff_utc = cutoff_et - datetime.timedelta(hours=utc_offset_et)
    return cutoff_utc


def main():
    simulated_settle = compute_cme_settle_utc(CONFIG_TIMEZONE_OFFSET)
    # Expected: 15:00 CT in EST = 21:00 UTC (because CT=UTC-6 in EST period)
    expected_settle = datetime.datetime(2024, 11, 3, 21, 0, 0)

    match = (simulated_settle == expected_settle)

    result = {
        "config_timezone_offset": CONFIG_TIMEZONE_OFFSET,
        "trade_date": TRADE_DATE.isoformat(),
        "simulated_settlement_utc": simulated_settle.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "expected_settlement_utc": expected_settle.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "match": match,
        "script_version": SCRIPT_VERSION,
    }

    out_path = Path(__file__).parent.parent / "output" / "backtest_result.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\\n", encoding="utf-8")

    print(f"Backtest result: match={match}")
    print(f"  simulated_settlement_utc: {result[\'simulated_settlement_utc\']}")
    print(f"  expected_settlement_utc:  {result[\'expected_settlement_utc\']}")
    print(f"  Written to: {out_path}")

    if not match:
        print("ERROR: Backtest FAILED. Check CONFIG_TIMEZONE_OFFSET.", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
''')

    # Update 3 additional: forensic analysis document (体量补充)
    w(UPD / "upd3_workspace" / "regulatory" / "sec_forensic_analysis_20241110.md", """# SEC Forensic Analysis — ArtemisQ Capital AROS v4.2 Incident
## Case No. TM-2024-1103-AQ — Forensic Technical Appendix
## Date: 2024-11-10

## Overview

This forensic analysis accompanies the formal investigation notice of
2024-11-10. It provides the SEC Division of Trading and Markets' technical
assessment of the AROS v4.2 timezone misconfiguration and its regulatory
implications under Rule 15c6-1 (T+1 Settlement) and Rule 15c3-5(b)
(Market Access Rule).

---

## Technical Findings

### 1. Root Cause Confirmation

The SEC's technical staff has independently confirmed the following:

**Configuration Error**: `timezone_config.py`, line 42
```python
UTC_OFFSET = -4  # Hardcoded EDT value; not updated after 2024-11-03 DST switch
```

**Required Correction**: `UTC_OFFSET = -5` (EST, effective after 2024-11-03 02:00 ET)

This error propagated through:
- `settlement_scheduler.py` → T+1 cutoff miscalculation
- `order_router.py` → Settlement date assignment error
- MiFIR reporting module → Field 28 UTC conversion error

### 2. T+1 Settlement Impact Analysis

Under Rule 15c6-1 (effective 2024-05-28), T+1 settlement cutoff is 21:00 ET.

| Timezone Config | ET Cutoff | UTC Cutoff (computed) | Status |
|-----------------|-----------|----------------------|--------|
| UTC-5 (correct, EST) | 21:00 ET | **2024-11-04T02:00:00Z** | Correct |
| UTC-4 (bug, EDT) | 21:00 ET | **2024-11-04T01:00:00Z** | **WRONG — 1 hour early** |

Orders submitted between 01:00:00 UTC and 02:00:00 UTC on 2024-11-04:
- **System classification**: Within T+1 window (system cutoff 01:00 UTC)
- **Correct classification**: Outside T+1 window (correct cutoff 02:00 UTC)
- **Regulatory status**: Potential T+1 violation under Rule 15c6-1

### 3. CME Settlement Reference Error

CME E-Mini S&P 500 daily settlement: 15:00:00 CT (Central Time)

| Period | CT = | CME Settlement UTC |
|--------|------|-------------------|
| CDT (summer) | UTC-5 | 15:00 CT = 20:00 UTC |
| **CST (winter, post-2024-11-03 DST)** | **UTC-6** | **15:00 CT = 21:00 UTC** |

AROS v4.2 computed CME settlement as 20:00 UTC instead of 21:00 UTC,
triggering delta-hedge closes 1 hour early.

### 4. MiFIR Field 28 Compliance Gap

Per FCA Market Watch 59, Field 28 (trading date and time) must be UTC.
AROS v4.2 was submitting UTC-4 local time for Field 28, specifically:

**Error pattern**: `2024-11-03T10:30:00-04:00` (local) submitted instead of
                  `2024-11-03T14:30:00Z` (UTC) — 4 hours off base, PLUS 1 hour DST error

**Affected transactions**: All trades 2024-11-03T09:30:00Z to 22:00:00Z

### 5. Comparison to Prior Enforcement Cases

The SEC finds similarities with:

**Knight Capital Group (SEC Release 34-70694, 2013)**:
- Rule 15c3-5(b) violation: inadequate pre-trade controls
- Hardcoded/static configuration without validation (Power Peg code)
- Penalty: $12,000,000
- KCG loss: $460,000,000+

The AROS v4.2 incident presents an analogous pattern of static system
configuration (hardcoded UTC offset) without operational validation at
a known trigger event (annual DST transition).

---

## Backtest Certification Requirements

To demonstrate remediation, ArtemisQ Capital must provide:

1. **Configuration proof**: `config_timezone_offset = -5` in the backtest output
2. **Settlement verification**: `simulated_settlement_utc = "2024-11-03T21:00:00Z"`
   (This is CME 15:00 CT in EST = UTC-6; 15 + 6 = 21:00 UTC)
3. **Match confirmation**: `match = true`
4. **Script version**: Documented in `script_version` field

The backtest template (`regulatory/sec_backtest_template.py`) automatically
computes and writes these values to `output/backtest_result.json`.

### Correct Computation Logic

```python
def compute_cme_settle_utc(utc_offset_et: int) -> datetime:
    # CT is 1 hour behind ET
    ct_utc_offset = utc_offset_et - 1   # EST: -5-1=-6; EDT: -4-1=-5
    # CME settlement: 15:00 CT; UTC = 15:00 - ct_utc_offset
    settle_utc_hour = 15 - ct_utc_offset
    return datetime(2024, 11, 3, settle_utc_hour % 24, 0, 0)

# With UTC-5 (correct):
# ct_utc_offset = -5 - 1 = -6
# settle_utc_hour = 15 - (-6) = 21 → 21:00 UTC ✓

# With UTC-4 (bug):
# ct_utc_offset = -4 - 1 = -5
# settle_utc_hour = 15 - (-5) = 20 → 20:00 UTC ✗
```

---

## Data Requirements for Formal Response

In your formal response to Case No. TM-2024-1103-AQ, provide:

1. Executed backtest output: `output/backtest_result.json`
2. Final consolidated corrective action plan: `output/corrective_action_plan.md`
3. SHA-256 sign-off over both files combined:
   `output/final_submission_signoff.txt` = VERIFIED:{sha256(backtest_json + cap_md)}

The SHA-256 must be computed over the concatenated bytes:
`concat(backtest_result.json bytes, corrective_action_plan.md bytes)`

---

## Regulatory Timeline Summary

| Date | Event |
|------|-------|
| 2024-05-28 | Rule 15c6-1 T+1 settlement effective |
| 2024-10-15 | AROS v4.2 deployed (UTC_OFFSET = -4 for EDT) |
| 2024-11-03 | US Eastern DST switch: EDT → EST (UTC-4 → UTC-5) |
| 2024-11-03 | AROS v4.2 fails to update UTC_OFFSET; incident begins |
| 2024-11-04 | Incident identified and AROS halted |
| 2024-11-05 | SEC preliminary inquiry notice issued |
| 2024-11-06 | Legal counsel memo: price_diff_usd superseded by price_diff_vwap_usd |
| 2024-11-10 | SEC formal investigation opened (Case TM-2024-1103-AQ) |
| 2024-11-17 | Backtest certification deadline |

SEC Division of Trading and Markets
Case No. TM-2024-1103-AQ
2024-11-10T15:00:00Z
""")

    # Update 3: additional evidence file (historical UTC conversion test cases)
    tz_test_rng = random.Random(20241110)
    tz_test_rows = [["test_id", "description", "input_et_datetime", "et_offset",
                     "expected_utc", "computed_utc_bug", "computed_utc_correct",
                     "pass_with_bug", "pass_with_fix", "rule_reference"]]
    test_cases = [
        ("TC-001", "CME settle EDT period (CDT)", "2024-06-15T15:00:00", -4,
         "2024-06-15T20:00:00Z", "2024-06-15T19:00:00Z", "2024-06-15T20:00:00Z",
         False, True, "CME settlement CDT"),
        ("TC-002", "CME settle EST period (CST) — incident scenario",
         "2024-11-03T15:00:00", -5,
         "2024-11-03T21:00:00Z", "2024-11-03T20:00:00Z", "2024-11-03T21:00:00Z",
         False, True, "CME settlement EST — KEY TEST"),
        ("TC-003", "T+1 cutoff EDT", "2024-06-15T21:00:00", -4,
         "2024-06-16T01:00:00Z", "2024-06-16T01:00:00Z", "2024-06-16T01:00:00Z",
         True, True, "Rule 15c6-1 EDT cutoff"),
        ("TC-004", "T+1 cutoff EST — incident scenario", "2024-11-03T21:00:00", -5,
         "2024-11-04T02:00:00Z", "2024-11-04T01:00:00Z", "2024-11-04T02:00:00Z",
         False, True, "Rule 15c6-1 EST cutoff — KEY TEST"),
        ("TC-005", "MiFIR Field 28 EDT", "2024-06-15T14:30:00", -4,
         "2024-06-15T18:30:00Z", "2024-06-15T18:30:00Z", "2024-06-15T18:30:00Z",
         True, True, "MiFIR Field 28 RTS 22"),
        ("TC-006", "MiFIR Field 28 EST — incident", "2024-11-03T14:30:00", -5,
         "2024-11-03T19:30:00Z", "2024-11-03T18:30:00Z", "2024-11-03T19:30:00Z",
         False, True, "MiFIR Field 28 EST — KEY TEST"),
    ]
    for tc in test_cases:
        tz_test_rows.append(list(tc))
    # Add more synthetic test cases for body
    for i in range(400):
        offset = tz_test_rng.choice([-4, -5])
        h = tz_test_rng.randint(9, 22)
        m = tz_test_rng.randint(0, 59)
        bug_utc_h = (h - (-4)) % 24
        correct_utc_h = (h - offset) % 24
        tz_test_rows.append([
            f"TC-{i + 7:03d}",
            f"UTC conversion test: {h:02d}:{m:02d} ET with offset {offset}",
            f"2024-11-03T{h:02d}:{m:02d}:00",
            offset,
            f"2024-11-03T{correct_utc_h:02d}:{m:02d}:00Z",
            f"2024-11-03T{bug_utc_h:02d}:{m:02d}:00Z",
            f"2024-11-03T{correct_utc_h:02d}:{m:02d}:00Z",
            (offset == -4),
            True,
            "UTC conversion validation",
        ])
    tz_buf = io.StringIO()
    csv.writer(tz_buf).writerows(tz_test_rows)
    w(UPD / "upd3_workspace" / "regulatory" / "utc_conversion_test_cases.csv", tz_buf.getvalue())

    updates_decl = {
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {"name": "regulatory/sec_inquiry_letter_20241105.md",
                 "action": "new",
                 "target": "regulatory/sec_inquiry_letter_20241105.md"},
                {"name": "incident/affected_orders_detail.csv",
                 "action": "new",
                 "target": "incident/affected_orders_detail.csv"},
            ],
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "regulatory/legal_counsel_memo_20241106.md",
                 "action": "new",
                 "target": "regulatory/legal_counsel_memo_20241106.md"},
                {"name": "regulatory/revised_field_spec_v2.md",
                 "action": "new",
                 "target": "regulatory/revised_field_spec_v2.md"},
                {"name": "regulatory/vwap_methodology_note.md",
                 "action": "new",
                 "target": "regulatory/vwap_methodology_note.md"},
                {"name": "incident/vwap_reference_20241103.csv",
                 "action": "new",
                 "target": "incident/vwap_reference_20241103.csv"},
            ],
        },
        "upd3_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd3_workspace",
            "files": [
                {"name": "regulatory/sec_formal_investigation_20241110.md",
                 "action": "new",
                 "target": "regulatory/sec_formal_investigation_20241110.md"},
                {"name": "regulatory/sec_backtest_template.py",
                 "action": "new",
                 "target": "regulatory/sec_backtest_template.py"},
                {"name": "regulatory/sec_forensic_analysis_20241110.md",
                 "action": "new",
                 "target": "regulatory/sec_forensic_analysis_20241110.md"},
                {"name": "regulatory/utc_conversion_test_cases.csv",
                 "action": "new",
                 "target": "regulatory/utc_conversion_test_cases.csv"},
            ],
        },
    }
    return updates_decl


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)
    WS.mkdir(parents=True, exist_ok=True)
    SESS.mkdir(parents=True, exist_ok=True)
    UPD.mkdir(parents=True, exist_ok=True)

    gen_system_files()
    gen_incident_files()
    gen_regulatory_files()
    gen_code_files()
    gen_reports()
    gen_communications()
    gen_reference()
    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = (
        "MiFIR/T+1 时区/DST 结算合规整改（ArtemisQ Capital AROS v4.2 2024-11-03 事故）— "
        "16 exec_check 轮次，3 次 update（含 1 次 supersede：price_diff_usd→price_diff_vwap_usd），"
        "5 条 preference 规则 P1-P5，难度向量 V1/V2/V3/V4/V5/V6/V7/V8/V9/V10。"
        "真实来源：FCA Market Watch 59 (https://www.fca.org.uk/publication/newsletters/market-watch-59.pdf)；"
        "SEC Rule 15c6-1 T+1 (https://www.sec.gov/exams/educationhelpguidesfaqs/t1-faq)；"
        "SEC Release 34-70694 Knight Capital (https://www.sec.gov/files/litigation/admin/2013/34-70694.pdf)；"
        "CME Group Trading Hours (https://www.cmegroup.com/trading-hours.html)."
    )

    dump_register_meta(
        DATASET, test_id=TID, desc=desc,
        main_session=sess_ids["main"],
        history_sessions=sess_ids["history"],
        updates=updates_decl,
    )

    # 体量报告
    total = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in WS.rglob("*") if p.is_file()
    )
    upd_files = list(UPD.rglob("*"))
    upd_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in upd_files if p.is_file()
    )
    upd1 = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd1_workspace").rglob("*") if p.is_file()
    ) if (UPD / "upd1_workspace").exists() else 0
    upd2 = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd2_workspace").rglob("*") if p.is_file()
    ) if (UPD / "upd2_workspace").exists() else 0
    upd3 = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd3_workspace").rglob("*") if p.is_file()
    ) if (UPD / "upd3_workspace").exists() else 0

    print(f"[sec3b] workspace tokens ~{total:,}")
    print(f"[sec3b] update1 ~{upd1:,} | update2 ~{upd2:,} | update3 ~{upd3:,} | total_upd ~{upd_tok:,}")
    print(f"[sec3b] built at {DATASET}")


if __name__ == "__main__":
    main()
