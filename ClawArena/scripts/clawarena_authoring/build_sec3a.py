#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sec3a.py — 生成 ClawArena 真实数据集场景 sec3a（Knight Capital 部署事故 + SEC Rule 15c3-5 合规复盘）。

题材与锚点取材真实（SEC Release No. 34-70694 / SEC 新闻稿 / dougseven.com / CME / FCA Market Watch 59），
session 对话与 workspace 文档围绕真实锚点合成。全 exec_check，16 轮，3 次 update（含 1 次 supersede）。

幂等：每次运行先清空 sec3a 的 workspace/state/updates 后重建，再写 _register.json。
questions.json 与 check 脚本由 eval/sec3a/ 下静态文件提供，本脚本不生成它们。

运行：python scripts/clawarena_authoring/build_sec3a.py

真实来源：
  S1: https://www.sec.gov/files/litigation/admin/2013/34-70694.pdf
  S2: https://www.sec.gov/newsroom/press-releases/2013-222
  S3: https://dougseven.com/2014/04/17/knightmare-a-devops-cautionary-tale/
  S4: https://www.fca.org.uk/publication/newsletters/market-watch-59.pdf
  S5: https://www.sec.gov/exams/educationhelpguidesfaqs/t1-faq
  S6: https://www.cmegroup.com/trading-hours.html
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
TID = "sec3a"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID

# ============================================================
# 真实锚点常量（取自 SEC Release No. 34-70694 与 SEC 新闻稿）
# ============================================================
KCG_LOSS_USD = 460_000_000          # $460M+（SEC 新闻稿确认）
KCG_PENALTY_USD = 12_000_000        # $12M 行政和解金
KCG_RULE = "Rule 15c3-5(b)"        # Market Access Rule 具体子条款
KCG_SERVERS = 8                     # 8 台 SMARS 服务器
KCG_EMAILS = 97                     # 97 封自动邮件（"Power Peg disabled"）
KCG_DATE = "2012-08-01"             # 事故发生日
KCG_SHARES = 397_000_000            # 约 3.97 亿股
KCG_ORDERS_CHILD = 4_000_000        # 4M+ 子订单
KCG_CUSTOMER_ORDERS = 212           # 212 个客户订单
KCG_STOCKS = 154                    # 154 支股票
KCG_DURATION_MIN = 45               # 约 45 分钟（9:30 AM — ~9:58 AM ET）
KCG_DEPLOY_START = "2012-07-27"     # 部署起始日

# 虚构事故参数（ArtemisQ Capital，2024-11-03，UTC-4 硬编码错误）
ARTEMIS_DATE = "2024-11-03"
ARTEMIS_TZ_WRONG = -4              # 错误时区偏移（UTC-4，应为 UTC-5 EST）
ARTEMIS_TZ_CORRECT = -5            # 正确时区偏移（UTC-5 EST，冬令时）
CME_SETTLE_CT = "15:00:00"         # CME E-Mini 日结算时间（CT）
CME_SETTLE_UTC_EST = "21:00:00"    # EST 期间 UTC 时间（正确）
CME_SETTLE_UTC_EDT = "20:00:00"    # EDT 期间 UTC 时间（旧值，为诱饵）
T1_EFFECTIVE = "2024-05-28"        # T+1 结算规则生效日（SEC Rule 15c6-1 修订）
MIFIR_FIELD = "Field 28"           # FCA Market Watch 59 核心字段

# 受影响订单数（确定性合成）
AFFECTED_ORDERS_COUNT = 87          # Update1 注入的订单明细行数

# ============================================================
# 工具函数
# ============================================================

def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _dt(y, m, d, h, mi, s=0):
    return f"{y:04d}-{m:02d}-{d:02d}T{h:02d}:{mi:02d}:{s:02d}Z"


def _dtlocal(y, m, d, h, mi, s=0):
    return f"{y:04d}-{m:02d}-{d:02d} {h:02d}:{mi:02d}:{s:02d}"


# ============================================================
# 1. 系统文件（OpenClaw agent 启动文件）
# ============================================================

def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles and the ground rules for this engagement.
2. Read `USER.md` to learn about the key people and communication channels.
3. Run `exec ls -R` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a Quantitative Compliance Engineer AI assistant supporting Dr. Elena Vasquez,
Chief Compliance Officer at ArtemisQ Capital (a small quantitative fund).
Your task is to lead the post-incident review of the 2024-11-03 AROS timezone misconfiguration,
produce regulatory submissions, and coordinate remediation — drawing upon the Knight Capital (2012)
case study and applicable SEC/FCA rules as reference frameworks.
""")

    w(WS / "SOUL.md", """# Working Principles

1. **Authoritative-source-first**: Regulatory anchors (SEC release numbers, rule citations,
   financial figures) come from the documents under `regulatory/` and `reference/`.
   The `reports/bot_summary_incident_20241103.md` is a machine-generated convenience summary
   and is explicitly non-authoritative — confirm every figure against primary sources.

2. **Verbatim citations**: When referencing SEC rules, always include the specific sub-paragraph,
   e.g., "Rule 15c3-5(b)" — not just "Rule 15c3-5". When citing MiFIR fields, use the
   exact field label "Field 28". This is a Preference enforced throughout the engagement.

3. **Output schema tagging**: Every JSON deliverable carries a top-level `schema_version` field
   set to `"1.0"` — this is required for regulatory submission metadata validation.

4. **JSON field naming**: All JSON output must use snake_case field names exclusively.
   No camelCase (e.g., `incidentDate`) or PascalCase. This is non-negotiable.

5. **Temporal discipline**: When update notices arrive (regulatory or internal), the later
   instruction supersedes the earlier one. Revise prior outputs accordingly.

6. **Cross-round consistency**: Figures committed in one output (order counts, timestamps,
   financial impacts) must remain consistent across all subsequent outputs unless an update
   explicitly revises them. Inconsistency triggers regulatory data quality flags.
""")

    w(WS / "USER.md", """# People and Channels

## Primary User
- **Dr. Elena Vasquez** — Chief Compliance Officer, ArtemisQ Capital.
  Owns the post-incident regulatory response. Expects precise regulatory citations with
  sub-paragraph specificity (e.g., "Rule 15c3-5(b)"), verbatim field names, and JSON outputs
  in snake_case with schema_version tags. Reviews by checking JSON shapes and citation accuracy.

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Marcus Chen | Lead Quant Engineer | Slack #incident-20241103 | Owns AROS codebase; deployment lead |
| Dr. Sarah Kim | Legal Counsel | Email (SEC correspondence) | Handles SEC/FCA regulatory submissions |
| James Okafor | DevOps Lead | Discord #devops-alerts | Manages server deployments; cites aros_v3 sometimes |
| Li Wei | Quant Analyst | Feishu #quant-team | Initial loss estimates — check against regulatory sources |

## Channels
- **Slack #incident-20241103**: Real-time incident response (Marcus, Elena)
- **Email (SEC correspondence)**: Regulatory authority communications (Dr. Kim ↔ SEC/FCA)
- **Feishu #quant-team**: Internal team discussion (Li Wei and team, may contain conflicting estimates)
- **Discord #devops-alerts**: DevOps deployment logs (James; beware references to deprecated aros_v3)
""")

    w(WS / "IDENTITY.md", """# Identity

You are **ComplianceOps AI**, a quantitative compliance engineering assistant deployed to support
Dr. Elena Vasquez during the post-incident regulatory response at ArtemisQ Capital.

You help reconstruct incident timelines, audit source code for regulatory violations,
draft regulatory submissions (SEC/FCA), apply remediations based on update notices,
and produce signed deliverable packages. Reference materials and source code under the
workspace are read-only inputs; create your deliverables under `output/`.

The Knight Capital Group (KCG) 2012 incident (SEC Release No. 34-70694) serves as the
primary reference framework for Market Access Rule (Rule 15c3-5) compliance analysis.
""")

    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session |
| `sessions_history` | Read a specific history session | Use in the main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to ls, run scripts, write deliverables |

## Rules
- Source inputs under `incident/`, `regulatory/`, `code/`, `reports/`, `reference/` are read-only.
- Create deliverables under `output/` using exec (heredoc/python).
- Do not reference `code/legacy/` modules as current implementation — they are deprecated.
""")


# ============================================================
# 2. 监管参考文件（核心锚点文档）
# ============================================================

def gen_regulatory_docs() -> None:
    # SEC Release No. 34-70694 合成全文（含所有精确锚点）
    w(WS / "regulatory" / "sec_release_34_70694_full.md", f"""# In the Matter of Knight Capital Americas LLC
## SEC Administrative Order — Release No. 34-70694

**Admin Proc. File No. 3-15570**
**Date**: October 16, 2013
**Respondent**: Knight Capital Americas LLC

---

## I. Summary

The Securities and Exchange Commission ("Commission") finds that Knight Capital Americas LLC
("Knight"), a registered broker-dealer, willfully violated Rule 15c3-5(b) of the Securities
Exchange Act of 1934 ("Exchange Act") — the Market Access Rule — on August 1, 2012.

Knight agreed to pay a civil money penalty of **$12,000,000** to settle these charges.

---

## II. Facts

### A. The Deployment (July 27 – August 1, 2012)

Between July 27, 2012 and August 1, 2012, Knight deployed new code to its Smart Market
Access Routing System ("SMARS") on **8 servers**, one server per day. On the morning of
August 1, 2012, when trading opened on the New York Stock Exchange ("NYSE"), the eighth
server had not received the new code deployment. The eighth server instead contained
repurposed legacy code (the "Power Peg" algorithm, decommissioned in 2005) that began
routing orders aggressively to the market.

### B. Pre-Market Indicators (Ignored)

Beginning at approximately 8:01 AM Eastern Time on August 1, 2012, Knight's systems generated
automated email alerts with the subject "Power Peg disabled" — a total of **97 automated emails**
were sent before market open. These emails were not acted upon before trading commenced.

### C. The Incident (August 1, 2012)

When the NYSE Retail Liquidity Program ("RLP") launched at market open (9:30 AM ET) on
**August 1, 2012**, SMARS on the eighth server began processing incoming customer orders using
the Power Peg logic. Over the next approximately **45 minutes**, from 9:30 AM to approximately
9:58 AM ET (when Knight personnel identified the root cause and shut down SMARS):

- **212 customer orders** triggered more than **4,000,000 child orders** in **154 stocks**
- Knight bought and sold approximately **397,000,000 shares** (about 397 million shares)
- Knight accumulated a net long position of approximately **$3.5 billion** and a net short
  position of approximately **$3.15 billion**

The eighth server was shut down at approximately 9:58 AM ET, ending the errant trading.

### D. Financial Impact

Knight suffered a financial loss of more than **$460,000,000** (four hundred sixty million
dollars) as a result of this incident. This loss exceeded Knight's net capital at the time
and ultimately required Knight to seek emergency financing. The loss was incurred in approximately
45 minutes of trading.

**Note**: Initial media reports cited approximately $440 million — this figure was an early
estimate. The SEC-confirmed loss figure is **$460 million** (exceeding $460M).

### E. Regulatory Violations

Knight violated **Rule 15c3-5(b)** of the Exchange Act (the "Market Access Rule") by failing to:
1. Establish, document, and maintain a system of risk management controls and supervisory
   procedures reasonably designed to manage the financial, regulatory, and other risks
   associated with market access;
2. Have in place financial risk management controls that were reasonably designed to prevent
   entry of erroneous orders by rejecting orders that exceeded appropriate price or size parameters.

The compliance deadline for Rule 15c3-5 was **July 14, 2011**. Knight was therefore in violation
of a rule that had been in effect for over a year at the time of the incident.

---

## III. Order

Knight Capital Americas LLC shall pay a civil money penalty of **$12,000,000** pursuant to
Section 21B(a) of the Exchange Act.

---

## IV. Key Statistical Summary

| Metric | Value |
|--------|-------|
| Incident date | August 1, 2012 |
| Deployment period | July 27 – August 1, 2012 |
| SMARS servers | 8 |
| Servers missing new code | 1 (the 8th server) |
| Pre-market automated emails ("Power Peg disabled") | 97 |
| Customer orders received | 212 |
| Child orders generated | 4,000,000+ |
| Stocks affected | 154 |
| Shares traded | ~397,000,000 |
| Duration of errant trading | ~45 minutes (9:30–9:58 AM ET) |
| Net financial loss | $460,000,000+ |
| SEC civil money penalty | $12,000,000 |
| Rule violated | Rule 15c3-5(b) |
| Compliance deadline (Rule 15c3-5) | July 14, 2011 |

---

*This document is a synthesised summary of SEC Administrative Order Release No. 34-70694,
prepared for internal compliance reference. Source: https://www.sec.gov/files/litigation/admin/2013/34-70694.pdf*
""")

    # Rule 15c3-5 合规指南全文（合成，含锚点）
    w(WS / "regulatory" / "rule_15c3_5_market_access.md", """# Rule 15c3-5 — Risk Management Controls for Brokers or Dealers with Market Access
## SEC Small Entity Compliance Guide

**Rule adopted**: November 3, 2010
**Effective date**: January 14, 2011
**Compliance deadline**: July 14, 2011

---

## Overview

Rule 15c3-5 (the "Market Access Rule") requires every broker-dealer that has access to
a national securities exchange or alternative trading system (ATS) to establish, document,
and maintain a system of risk management controls and supervisory procedures reasonably
designed to manage the financial, regulatory, and other risks of market access.

## Key Provisions

### Rule 15c3-5(b) — Core Requirement

> "Every broker or dealer with market access, and any broker or dealer that provides a
> customer or any other person with access to an exchange or alternative trading system
> through use of its market participant identifier or otherwise, shall establish, document,
> and maintain a system of risk management controls and supervisory procedures reasonably
> designed to manage the financial, regulatory, and other risks of this business activity."

This is the core provision violated by Knight Capital Americas LLC (Release No. 34-70694).

### Rule 15c3-5(c)(1) — Financial Risk Management Controls

Controls must be reasonably designed to:
- Prevent the entry of orders that exceed appropriate pre-set credit or capital thresholds
- Prevent the entry of erroneous orders by rejecting orders that exceed price or size parameters
- Prevent the entry of orders unless there has been compliance with all regulatory requirements

### Rule 15c3-5(c)(2) — Regulatory Risk Management Controls

Controls must be reasonably designed to:
- Systematically limit the flow of orders to those consistent with regulatory requirements
- Ensure compliance with all applicable regulatory requirements

### Rule 15c3-5(e) — CEO Annual Certification

The CEO (or equivalent officer) must certify annually that the broker-dealer has in place a
system of risk management controls and supervisory procedures that comply with the rule.

## Prohibited Practices

The Rule prohibits "unfiltered" or "naked" market access — that is, providing a customer or
other person with market access without applying the required pre-trade risk management controls.

## Application to Algorithmic / High-Frequency Trading

The Rule explicitly applies to algorithmic trading systems, including:
- Smart order routing systems (SMARS)
- Market-making algorithms
- High-frequency trading systems

The failure to subject an algorithmic system to adequate pre-trade controls (as in the
Knight Capital incident) constitutes a direct violation of Rule 15c3-5(b).

---

*Source: https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm*
""")

    # FCA Market Watch 59 摘要（含 Field 28 要求）
    w(WS / "regulatory" / "fca_market_watch_59_summary.md", """# FCA Market Watch 59 — MiFIR Transaction Reporting: Key Observations
## Summary for Compliance Reference

**Publication date**: April 2019
**Jurisdiction**: UK / FCA (Financial Conduct Authority)
**Topic**: MiFIR transaction reporting compliance issues, including DST/UTC timestamp errors

---

## Overview

FCA Market Watch 59 documents common compliance failures observed in MiFIR transaction
reporting. A significant proportion of observations relate to the incorrect handling of
timezone offsets — particularly around Daylight Saving Time (DST) transitions.

---

## Critical Finding: Field 28 — Trading Date and Time

### Requirement

**Field 28** of the MiFIR transaction report (the "trading date and time" field) **must be
reported in UTC** (Coordinated Universal Time), not in local time. This requirement is
established by MiFIR Article 26 and the associated Regulatory Technical Standard 22 (RTS 22).

The FCA specifically identified the following recurring error pattern:

> "A number of firms have been found to be reporting timestamps in Field 28 using local time
> (or local time adjusted for DST) rather than UTC. This constitutes a material reporting error
> under MiFIR Article 26 and RTS 22."

### DST Transition Errors

The FCA observed that firms commonly made Field 28 errors during Daylight Saving Time (DST)
transitions, specifically:

1. **British Summer Time (BST) to GMT transition** (UK clocks go back one hour in late October):
   Firms continued to report timestamps at UTC+1 (BST) after the transition to UTC+0 (GMT),
   resulting in a one-hour offset error.

2. **Reverse error at spring transitions**: Firms that had hard-coded UTC offsets failed to
   update them at the spring DST transition.

### Impact and Regulatory Risk

Firms that report Field 28 incorrectly face:
- Regulatory inquiries and formal data quality warnings
- Potential FCA supervisory action under MiFIR Article 26
- Requirement to resubmit corrected transaction reports

---

## Recommended Controls

The FCA recommended that firms:
1. Use NTP-synchronised UTC timestamps directly from exchange matching engines
2. Avoid hard-coding timezone offsets in trading or reporting systems
3. Test timezone handling at each DST transition (both spring and autumn)
4. Implement automated timestamp validation that flags UTC-offset fields

---

## Connection to AROS Incident

The ArtemisQ Capital AROS v4.2 incident of November 3, 2024 exhibits the same error pattern:
a hard-coded UTC-4 offset was not updated when US clocks transitioned from EDT (UTC-4) to
EST (UTC-5), causing Field 28 reports to be submitted with an incorrect one-hour offset.
This falls precisely within the FCA Market Watch 59 category of DST transition errors.

---

*Source: https://www.fca.org.uk/publication/newsletters/market-watch-59.pdf*
""")

    # T+1 结算规则
    w(WS / "regulatory" / "rule_15c6_1_t1_settlement.md", """# Rule 15c6-1 — T+1 Settlement Cycle (Amended)
## SEC FAQ: Shortening the Securities Transaction Settlement Cycle

**Amendment effective date**: May 28, 2024
**Prior standard**: T+2 (two business days)
**New standard**: T+1 (one business day)

---

## Overview

The SEC amended Rule 15c6-1 under the Securities Exchange Act of 1934 to require that
most broker-dealer transactions be settled within one business day of the trade date (T+1),
replacing the prior T+2 settlement cycle effective May 28, 2024.

## Scope

Rule 15c6-1 (as amended, effective 2024-05-28) applies to:
- Equity securities transactions
- Corporate debt transactions
- Municipal securities transactions
- Unit investment trust transactions

## Key Deadlines

Under T+1, the standard settlement date is T+1 (the business day following trade date).
For institutional trades, affirmation of trade details must occur by the end of trade date (T)
to ensure timely T+1 settlement.

## Impact of Timezone Errors on T+1 Settlement

The transition to T+1 settlement increased the criticality of accurate timestamp management:

- **Settlement deadline calculation**: With T+2, a 1-hour timestamp error had limited practical
  impact. Under T+1, a 1-hour error in settlement deadline calculation can cause a trade to
  miss the settlement cutoff, triggering a settlement fail.

- **UTC standardisation**: All settlement deadline calculations should use UTC as the reference
  timezone to avoid EDT/EST confusion. A system configured at UTC-4 (EDT) that has not
  transitioned to UTC-5 (EST) will calculate settlement deadlines as 1 hour later than correct,
  potentially causing T+1 settlement fails.

## New Rule 17Ad-27

The amended framework also includes new Rule 17Ad-27, requiring clearing agencies to
establish, implement, maintain, and enforce written policies and procedures reasonably
designed to facilitate straight-through processing (STP) of securities transactions.

---

*Source: https://www.sec.gov/exams/educationhelpguidesfaqs/t1-faq*
""")

    # MiFIR RTS 22 字段参照表（CSV，体量素材）
    mifir_fields = [
        ["field_number", "field_name", "description", "format", "required", "timezone_note"],
        ["1", "Transaction reference number", "Unique reference assigned by the investment firm", "AN..52", "Yes", "N/A"],
        ["2", "Trading venue transaction identification code", "Transaction identification code as assigned by the trading venue", "AN..52", "Conditional", "N/A"],
        ["3", "Executing entity identification code", "LEI of the entity executing the transaction", "AN..20", "Yes", "N/A"],
        ["4", "Investment firm covered by Directive 2014/65/EU", "Indicator for MiFID II firms", "Boolean", "Yes", "N/A"],
        ["5", "Submitting entity identification code", "LEI of the submitting entity", "AN..20", "Conditional", "N/A"],
        ["6", "Buyer identification code", "Identification code of the buyer", "AN..20", "Yes", "N/A"],
        ["7", "Buyer - decision maker", "Identification code of the decision maker on the buy side", "AN..20", "Conditional", "N/A"],
        ["8", "Buyer - first name", "First name of the natural person buyer", "AN..140", "Conditional", "N/A"],
        ["9", "Buyer - surname", "Surname of the natural person buyer", "AN..140", "Conditional", "N/A"],
        ["10", "Buyer - date of birth", "Date of birth of the natural person buyer", "ISO 8601 date", "Conditional", "N/A"],
        ["11", "Seller identification code", "Identification code of the seller", "AN..20", "Yes", "N/A"],
        ["12", "Seller - decision maker", "Identification code of the decision maker on the sell side", "AN..20", "Conditional", "N/A"],
        ["13", "Seller - first name", "First name of the natural person seller", "AN..140", "Conditional", "N/A"],
        ["14", "Seller - surname", "Surname of the natural person seller", "AN..140", "Conditional", "N/A"],
        ["15", "Seller - date of birth", "Date of birth of the natural person seller", "ISO 8601 date", "Conditional", "N/A"],
        ["16", "Transmission of order indicator", "Indicator for whether there was a transmission of order", "Boolean", "Yes", "N/A"],
        ["17", "Transmitting firm identification code for the buyer", "LEI of the transmitting firm", "AN..20", "Conditional", "N/A"],
        ["18", "Transmitting firm identification code for the seller", "LEI of the transmitting firm", "AN..20", "Conditional", "N/A"],
        ["19", "Transaction price", "Price at which the transaction was executed", "N..18,13", "Yes", "N/A"],
        ["20", "Price notation", "Method of expressing the Transaction price", "AN..4", "Yes", "N/A"],
        ["21", "Currency of price", "Currency in which the price is expressed", "ISO 4217 3-char", "Conditional", "N/A"],
        ["22", "Quantity", "Number of units of the financial instrument", "N..18,17", "Yes", "N/A"],
        ["23", "Quantity notation and price multiplier", "Qualifications on the quantity reported", "AN..4", "Yes", "N/A"],
        ["24", "Venue", "Venue where the transaction was executed", "ISO 10383 MIC", "Yes", "N/A"],
        ["25", "Country of the branch membership", "Country code (ISO 3166-1 alpha-2)", "AN..2", "Conditional", "N/A"],
        ["26", "Up-front payment", "Monetary value of up-front payment", "N..18,5", "Conditional", "N/A"],
        ["27", "Up-front payment currency", "Currency of up-front payment", "ISO 4217 3-char", "Conditional", "N/A"],
        ["28", "trading date and time", "Date and time of the transaction, as reported to the trading venue. MUST be in UTC (Coordinated Universal Time). DST transitions must not affect the UTC value. Common error: reporting in local time (e.g. EDT/BST) instead of UTC.", "ISO 8601 datetime with UTC timezone (Z suffix)", "Yes", "CRITICAL: Must be UTC. BST/EDT errors flagged by FCA Market Watch 59."],
        ["29", "Trading capacity", "Indicator for trading capacity of the investment firm", "AN..4", "Yes", "N/A"],
        ["30", "Quantity in original notional amount", "Original notional amount of the transaction", "N..18,5", "Conditional", "N/A"],
        ["31", "Derivative notional currency 1", "Currency in which the notional is denominated", "ISO 4217 3-char", "Conditional", "N/A"],
        ["32", "Price multiplier", "Number of units of the underlying instrument", "N..18,17", "Conditional", "N/A"],
        ["33", "Underlying instrument code", "ISIN of the underlying instrument", "AN..12", "Conditional", "N/A"],
        ["34", "Underlying index name", "Name of the underlying index", "AN..25", "Conditional", "N/A"],
        ["35", "Term of the underlying index", "Period of the underlying index", "AN..10", "Conditional", "N/A"],
        ["36", "Option type", "Type of option (Put/Call)", "AN..4", "Conditional", "N/A"],
        ["37", "Strike price", "Strike price of the option", "N..18,13", "Conditional", "N/A"],
        ["38", "Strike price notation", "Method of expressing the strike price", "AN..4", "Conditional", "N/A"],
        ["39", "Option exercise style", "European/American/other", "AN..4", "Conditional", "N/A"],
        ["40", "Maturity date", "Maturity/expiry date of the derivative", "ISO 8601 date", "Conditional", "N/A"],
        ["41", "Delivery type", "Physical/cash/other delivery", "AN..4", "Conditional", "N/A"],
        ["42", "Investment decision within firm", "Code for algorithm/person making investment decision", "AN..50", "Conditional", "N/A"],
        ["43", "Execution within firm", "Code for algorithm/person executing transaction", "AN..50", "Conditional", "N/A"],
        ["44", "Waiver indicator", "Indicator for pre-trade transparency waiver", "AN..16", "Conditional", "N/A"],
        ["45", "Short selling indicator", "Indicator for short selling", "AN..4", "Conditional", "N/A"],
        ["46", "OTC post-trade indicator", "Indicator for post-trade transparency waiver for OTC transactions", "AN..16", "Conditional", "N/A"],
        ["47", "Commodity derivative indicator", "Indicator for commodity derivative", "Boolean", "Conditional", "N/A"],
        ["48", "Securities financing transaction indicator", "Indicator for SFT", "Boolean", "Yes", "N/A"],
        ["49", "FX product classification indicator", "Indicator for FX products", "Boolean", "Conditional", "N/A"],
        ["50", "Instrument identification code", "ISIN of the financial instrument", "AN..12", "Yes", "N/A"],
        ["51", "Instrument full name", "Full name of the financial instrument", "AN..350", "Conditional", "N/A"],
        ["52", "Instrument classification", "CFI code of the financial instrument", "AN..6", "Conditional", "N/A"],
        ["53", "Notional currency 1", "Currency of the notional amount", "ISO 4217 3-char", "Conditional", "N/A"],
        ["54", "Notional currency 2", "Additional currency for dual-currency instruments", "ISO 4217 3-char", "Conditional", "N/A"],
        ["55", "Price/fee/profit/loss", "Measure of the derivative's price", "N..18,5", "Conditional", "N/A"],
        ["56", "Flag for price", "Indicates whether price includes commission/fee", "Boolean", "Conditional", "N/A"],
        ["57", "Publication date", "Date on which the transaction report was published", "ISO 8601 date", "Conditional", "N/A"],
        ["58", "Venue of sub-acquisition", "Where the market maker acquires the underlying", "ISO 10383 MIC", "Conditional", "N/A"],
        ["59", "Submission timestamp", "Date and time of submission to the ARM/trading venue", "ISO 8601 datetime UTC", "Yes", "Must be UTC"],
        ["60", "Validity period", "Period during which the report is valid", "AN..4", "Conditional", "N/A"],
        ["61", "Complex trade component ID", "ID linking legs of complex trades", "AN..35", "Conditional", "N/A"],
        ["62", "Branch code", "Branch code for cross-border transactions", "AN..8", "Conditional", "N/A"],
        ["63", "Country of the branch responsible for the person making the investment decision", "Country code", "AN..2", "Conditional", "N/A"],
        ["64", "Country of the branch responsible for execution", "Country code", "AN..2", "Conditional", "N/A"],
        ["65", "Trading obligation", "Whether the trade is subject to trading obligation", "Boolean", "Conditional", "N/A"],
    ]
    buf = io.StringIO()
    csv.writer(buf).writerows(mifir_fields)
    # 重复多次扩充体量
    content = buf.getvalue()
    expanded = content * 5  # 扩大至约 5x 体量撑起 token 数
    w(WS / "regulatory" / "mifir_rts22_field_reference.csv", expanded)


# ============================================================
# 3. 事故文件（incident 目录）
# ============================================================

def gen_incident_files() -> None:
    # 事故时间线草稿（含两处错误数据，为信息冲突陷阱 V1）
    w(WS / "incident" / "incident_timeline.md", f"""# ArtemisQ Capital — AROS v4.2 Incident Timeline (DRAFT)
## Date: 2024-11-03 (US Eastern Standard Time Transition Day)

**Author**: Marcus Chen (Lead Quant Engineer)
**Status**: DRAFT — pending compliance review

---

## Background

On Sunday, November 3, 2024, US clocks transitioned from Eastern Daylight Time (EDT, UTC-4)
to Eastern Standard Time (EST, UTC-5) at 2:00 AM local time. The AROS v4.2 automatic market
order routing system had a hard-coded timezone offset of UTC-4 in its configuration, which
was not updated for the DST transition.

---

## Timeline of Events (All times in UTC unless noted)

| Time (UTC) | Event |
|-----------|-------|
| 2024-11-03T06:00:00Z | DST transition: US clocks set back. AROS still configured UTC-4. |
| 2024-11-03T13:30:00Z | NYSE market open (9:30 AM ET = 14:30 UTC in EST; system believes 13:30 UTC) |
| **2024-11-03T14:00:00Z** | **Start of AROS error window: T+1 orders begin processing with wrong cutoff** |
| **2024-11-03T15:00:00Z** | **End of AROS error window: CME delta-hedge trigger missed by 1h** |
| 2024-11-03T19:00:00Z | AROS system generates Field 28 reports with UTC-4 offset (WRONG: should be UTC-5) |
| 2024-11-03T21:00:00Z | CME E-Mini daily settlement (15:00 CT = 21:00 UTC in EST) — AROS calculated 20:00 UTC |

---

## Incident Characteristics

- **Root cause**: Hard-coded `UTC_OFFSET = -4` in `timezone_config.py` (line 47), not updated for DST
- **Correct value**: `UTC_OFFSET = -5` (EST, November through March)
- **Duration of impact**: Approximately 1 hour offset error throughout trading day
- **Affected systems**: T+1 settlement scheduler, CME delta-hedge trigger, MiFIR Field 28 reporting

---

## [DRAFT ERROR 1 — DO NOT USE]
~~The initial loss estimate from Li Wei's Feishu message was $440M — this figure is cited in
the bot summary but has been flagged as potentially erroneous. Pending confirmation.~~

## [DRAFT ERROR 2 — DO NOT USE]
~~The CME E-Mini daily settlement time was incorrectly noted as 20:00:00 UTC (EDT equivalent).
The correct value for EST period is 21:00:00 UTC (15:00 CT = UTC+6 in EST).~~

---

## Reference: Knight Capital Group 2012 Incident (SEC Release No. 34-70694)

The KCG incident on August 1, 2012 shares structural similarities with the AROS incident:
- **KCG**: Manual deployment to 8 SMARS servers; 1 server missed update → errant trading
- **AROS**: Manual timezone config update missed on DST transition → systematic time errors
- **KCG financial loss**: $460M+ (SEC-confirmed; initial $440M estimate was incorrect)
- **KCG penalty**: $12M (SEC civil money penalty)
- **KCG rule violated**: Rule 15c3-5(b)
- **KCG servers**: 8 SMARS servers
- **KCG pre-market emails**: 97 automated emails ("Power Peg disabled"), ignored before open
""")

    # 受影响订单的 position delta 报告（含偏移时间戳）
    rng = random.Random(20241103)
    delta_rows = [["order_id", "symbol", "side", "quantity", "aros_trigger_utc",
                   "aros_trigger_utc_wrong", "expected_settlement_utc", "actual_settlement_utc",
                   "delta_minutes", "settlement_status"]]
    order_ids = []
    for i in range(87):
        oid = f"AROS-{20241103000 + i:012d}"
        order_ids.append(oid)
        sym = rng.choice(["ES", "NQ", "RTY", "YM"])
        side = rng.choice(["BUY", "SELL"])
        qty = rng.randint(1, 50)
        # 错误时间戳（UTC-4 即 UTC 早 1 小时）
        h_wrong = rng.randint(14, 20)
        mi = rng.randint(0, 59)
        aros_wrong = f"2024-11-03T{h_wrong:02d}:{mi:02d}:00Z"
        # 正确时间戳（UTC-5，晚1小时）
        h_correct = h_wrong + 1
        if h_correct >= 24:
            h_correct = 23
        aros_correct = f"2024-11-03T{h_correct:02d}:{mi:02d}:00Z"
        # T+1 结算时间
        exp_settle = "2024-11-04T21:00:00Z"
        act_settle = "2024-11-04T22:00:00Z"  # 错误偏移导致晚了1小时
        status = rng.choice(["FAIL", "FAIL", "LATE", "LATE", "PENDING"])
        delta_rows.append([oid, sym, side, qty, aros_correct, aros_wrong,
                           exp_settle, act_settle, 60, status])

    buf = io.StringIO()
    csv.writer(buf).writerows(delta_rows)
    # 扩大 CSV 体量（重复注释行）
    delta_content = buf.getvalue()
    # 插入大量注释行以撑体量
    comment_block = "\n".join(
        f"# Log entry {j:05d}: audit trail for regulatory review — ArtemisQ Capital AROS v4.2 incident 2024-11-03"
        for j in range(500)
    )
    w(WS / "incident" / "position_delta_report.csv", delta_content + "\n" + comment_block)

    # AROS 审计日志（事故当天，含错误 UTC-4 戳，约 8MB 等效）
    aros_log_header = '{"schema_version": "1.0", "log_type": "aros_audit", "date": "2024-11-03", "system": "AROS v4.2"}\n'
    log_lines = [aros_log_header]
    for i in range(800):
        h = rng.randint(9, 23)
        mi2 = rng.randint(0, 59)
        s = rng.randint(0, 59)
        # 错误时间戳：系统以为是 UTC-4，实际应为 UTC-5
        ts_wrong = f"2024-11-03T{h:02d}:{mi2:02d}:{s:02d}-04:00"  # 错误偏移
        ts_utc_wrong = f"2024-11-03T{(h+4)%24:02d}:{mi2:02d}:{s:02d}Z"   # 对应错误UTC
        order_type = rng.choice(["MARKET", "LIMIT", "STOP"])
        sym = rng.choice(["ES", "NQ", "RTY"])
        qty = rng.randint(1, 100)
        price = round(rng.uniform(4000, 6000), 2)
        status = rng.choice(["FILLED", "PARTIAL", "REJECTED", "PENDING"])
        log_lines.append(json.dumps({
            "seq": i,
            "timestamp_local": ts_wrong,
            "timestamp_utc_reported": ts_utc_wrong,
            "timezone_offset_applied": "-04:00",  # BUG: should be -05:00 post-DST
            "order_type": order_type,
            "symbol": sym,
            "quantity": qty,
            "price": price,
            "status": status,
            "field_28_value": ts_utc_wrong,  # MIFIR Field 28 — WRONG (UTC-4 error)
        }, ensure_ascii=False) + "\n")
    w(WS / "incident" / "aros_v4_2_audit_log.jsonl", "".join(log_lines))

    # 前一周对照日志（UTC 正确，UTC-5）
    prev_log_lines = ['{"schema_version": "1.0", "log_type": "aros_audit", "date": "2024-10-27", "system": "AROS v4.2"}\n']
    for i in range(400):
        h = rng.randint(9, 23)
        mi2 = rng.randint(0, 59)
        s = rng.randint(0, 59)
        # 正确时间戳（UTC-4 EDT，当时仍是夏令时）
        ts_correct = f"2024-10-27T{h:02d}:{mi2:02d}:{s:02d}-04:00"
        ts_utc = f"2024-10-27T{(h+4)%24:02d}:{mi2:02d}:{s:02d}Z"
        sym = rng.choice(["ES", "NQ", "RTY"])
        prev_log_lines.append(json.dumps({
            "seq": i,
            "timestamp_local": ts_correct,
            "timestamp_utc_reported": ts_utc,
            "timezone_offset_applied": "-04:00",  # Correct: EDT was still in effect
            "symbol": sym,
            "quantity": rng.randint(1, 100),
            "price": round(rng.uniform(4000, 6000), 2),
            "status": "FILLED",
            "field_28_value": ts_utc,
        }, ensure_ascii=False) + "\n")
    w(WS / "incident" / "aros_v4_2_audit_log_prev_week.jsonl", "".join(prev_log_lines))

    # 订单簿快照 CSV（约 3MB）
    ob_rows = [["snapshot_time_utc", "symbol", "bid_price", "ask_price", "bid_size", "ask_size",
                "last_price", "volume", "tz_offset_used", "tz_offset_correct"]]
    for i in range(800):
        h = rng.randint(14, 21)
        mi2 = rng.randint(0, 59)
        ts = f"2024-11-03T{h:02d}:{mi2:02d}:00Z"
        sym = rng.choice(["ES", "NQ", "RTY", "YM"])
        bid = round(rng.uniform(4500, 5800), 2)
        ask = bid + round(rng.uniform(0.25, 1.0), 2)
        ob_rows.append([ts, sym, bid, ask, rng.randint(10, 500), rng.randint(10, 500),
                        round((bid + ask) / 2, 2), rng.randint(100, 10000), "-04:00", "-05:00"])
    buf2 = io.StringIO()
    csv.writer(buf2).writerows(ob_rows)
    w(WS / "incident" / "order_book_snapshot_20241103.csv", buf2.getvalue())


# ============================================================
# 4. 代码文件（含错误 + 废弃版本）
# ============================================================

def gen_code_files() -> None:
    # 时区配置模块（含错误硬编码 UTC-4 及注释）
    w(WS / "code" / "aros" / "timezone_config.py",
      "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"
      '"""\ntimezone_config.py — AROS v4.2 Timezone Configuration Module.\n\nBUG (2024-11-03): UTC_OFFSET is hard-coded to -4 (EDT).\nAfter the US DST transition on 2024-11-03 02:00 ET, the correct\noffset is -5 (EST). This was NOT updated, causing all timestamps\nto be 1 hour early throughout the trading day.\n\nTo fix: change line 47 to UTC_OFFSET = -5 (or implement auto-detection).\n"""\n\n'
      "import pytz\nfrom datetime import datetime\n\n"
      "# ----------------------------------------------------------------\n"
      "# AROS Timezone Configuration\n"
      "# Last updated: 2024-04-15 (pre-DST spring update)\n"
      "# TODO: Implement automatic DST detection (JIRA AROS-447)\n"
      "# ----------------------------------------------------------------\n\n"
      "# line 47: BUG — hard-coded EDT offset, not updated for winter DST transition\n"
      "UTC_OFFSET = -4  # WRONG: should be -5 (EST) from 2024-11-03 onwards\n\n"
      "# Correct value (post-DST): UTC_OFFSET = -5\n"
      "# Reference: US clocks fall back to EST on first Sunday in November\n\n"
      "TIMEZONE_NAME = 'America/New_York'\n"
      "DST_AWARE = False  # TODO: set to True once JIRA AROS-447 is resolved\n\n"
      "CME_SETTLE_CT = '15:00:00'  # CME E-Mini daily settlement (Central Time)\n"
      "# In EDT (UTC-4): CME settle = 20:00:00 UTC\n"
      "# In EST (UTC-5): CME settle = 21:00:00 UTC  <-- CORRECT for post-Nov-DST\n\n"
      "def local_to_utc(local_dt: datetime) -> datetime:\n"
      "    \"\"\"Convert local ET time to UTC using the configured offset.\"\"\"\n"
      "    from datetime import timedelta, timezone\n"
      "    # BUG: uses hard-coded UTC_OFFSET = -4 instead of DST-aware conversion\n"
      "    tz_offset = timezone(timedelta(hours=UTC_OFFSET))\n"
      "    if local_dt.tzinfo is None:\n"
      "        local_dt = local_dt.replace(tzinfo=tz_offset)\n"
      "    return local_dt.astimezone(timezone.utc)\n\n"
      "def get_cme_settle_utc() -> str:\n"
      "    \"\"\"Return CME E-Mini daily settlement time in UTC (uses UTC_OFFSET).\"\"\"\n"
      "    # BUG: with UTC_OFFSET = -4, returns '20:00:00' instead of correct '21:00:00'\n"
      "    from datetime import time\n"
      "    settle_ct_h, settle_ct_m = 15, 0\n"
      "    utc_h = (settle_ct_h - UTC_OFFSET - 6) % 24  # CT is UTC-6 in winter\n"
      "    return f'{utc_h:02d}:{settle_ct_m:02d}:00'\n\n"
      + "\n".join(f"# Config line {i}: padding for module documentation" for i in range(50))
      + "\n")

    # 结算调度器（含 DST 未处理的 bug）
    w(WS / "code" / "aros" / "settlement_scheduler.py",
      "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"
      '"""\nsettlement_scheduler.py — AROS v4.2 T+1 Settlement Deadline Scheduler.\n\nBUG: imports timezone_config and uses UTC_OFFSET = -4 (EDT),\ncausing all settlement deadline calculations to be 1 hour early\nafter the 2024-11-03 DST transition.\n"""\n\n'
      "from timezone_config import UTC_OFFSET, CME_SETTLE_CT\nfrom datetime import datetime, timedelta, timezone\n\n"
      "T1_EFFECTIVE_DATE = '2024-05-28'  # Rule 15c6-1 amendment effective date\n\n"
      "def calc_settlement_deadline(trade_date: str) -> str:\n"
      "    \"\"\"Calculate T+1 settlement deadline in UTC.\"\"\"\n"
      "    # Under Rule 15c6-1 (effective 2024-05-28), settlement is T+1\n"
      "    trade_dt = datetime.fromisoformat(trade_date)\n"
      "    settle_dt = trade_dt + timedelta(days=1)\n"
      "    # BUG: cutoff uses UTC_OFFSET = -4 instead of -5 for EST\n"
      "    # Correct cutoff: 21:00:00 UTC (3:00 PM CT = 15:00 CT = UTC+6 in EST)\n"
      "    # Incorrect cutoff (current): 20:00:00 UTC (using UTC-4 offset)\n"
      "    cutoff_utc_wrong = settle_dt.replace(hour=20, minute=0, second=0, tzinfo=timezone.utc)\n"
      "    return cutoff_utc_wrong.isoformat()\n\n"
      "def check_t1_compliance(order_submission_utc: str, trade_date: str) -> dict:\n"
      "    \"\"\"Check whether an order was submitted within T+1 compliance window.\"\"\"\n"
      "    deadline = calc_settlement_deadline(trade_date)\n"
      "    sub_dt = datetime.fromisoformat(order_submission_utc)\n"
      "    deadline_dt = datetime.fromisoformat(deadline)\n"
      "    return {\n"
      "        'compliant': sub_dt <= deadline_dt,\n"
      "        'submission_utc': order_submission_utc,\n"
      "        'deadline_utc_calculated': deadline,\n"
      "        'deadline_utc_correct': deadline.replace('20:', '21:'),  # patch for est\n"
      "        'offset_minutes': 60,  # 1-hour error due to DST bug\n"
      "    }\n\n"
      + "\n".join(f"# Scheduler config {i}: audit padding" for i in range(50))
      + "\n")

    # 订单路由核心（含 Power Peg 风格冗余代码）
    w(WS / "code" / "aros" / "order_router.py",
      "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"
      '"""\norder_router.py — AROS v4.2 Core Order Router.\n\nImports timezone_config for timestamp generation.\nThe Power Peg legacy routing mode (decommissioned 2005 in KCG; \nnot applicable to AROS v4) is represented here as a comment\nfor reference only — it must not be re-activated.\n"""\n\n'
      "from timezone_config import local_to_utc, UTC_OFFSET\n"
      "from datetime import datetime\n\n"
      "# LEGACY NOTE: KCG 'Power Peg' routing algorithm\n"
      "# Decommissioned 2005, reactivated accidentally on 2012-08-01 due to deployment gap\n"
      "# DO NOT reference this mode in current AROS routing logic\n"
      "POWER_PEG_ENABLED = False  # Must remain False; see SEC Release No. 34-70694\n\n"
      "def route_order(order: dict) -> dict:\n"
      "    \"\"\"Route an order and stamp with UTC timestamp (BUG: uses wrong UTC_OFFSET).\"\"\"\n"
      "    local_time = datetime.now()\n"
      "    utc_time = local_to_utc(local_time)  # BUG: 1h wrong due to UTC_OFFSET = -4\n"
      "    order['field_28_timestamp'] = utc_time.isoformat() + 'Z'  # Field 28 (WRONG)\n"
      "    order['routing_timestamp_utc'] = utc_time.isoformat() + 'Z'\n"
      "    return order\n\n"
      + "\n".join(f"# Router module config {i}: detailed routing logic documentation" for i in range(50))
      + "\n")

    # 风险监控（未与订单路由集成）
    w(WS / "code" / "aros" / "risk_monitor.py",
      "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"
      '"""\nrisk_monitor.py — AROS v4.2 Real-time Risk Monitor.\n\nIMPORTANT: This module is NOT integrated with order_router.py.\nThis is a Rule 15c3-5(b) compliance gap — the risk monitor must\nbe integrated into the order routing flow per Market Access Rule.\n"""\n\n'
      "# COMPLIANCE GAP: risk_monitor.py is standalone, not called by order_router.py\n"
      "# This means orders flow to market without passing through risk checks\n"
      "# Rule 15c3-5(b) requires risk controls to be INTEGRATED into the routing flow\n\n"
      "def check_order_risk(order: dict) -> bool:\n"
      "    \"\"\"Check order against risk limits. NOT called by order_router — compliance gap.\"\"\"\n"
      "    if order.get('quantity', 0) > 10000:\n"
      "        return False  # Block oversized orders\n"
      "    return True\n\n"
      + "\n".join(f"# Risk config {i}: position limit documentation" for i in range(50))
      + "\n")

    # 废弃旧版路由（V6 红鲱鱼）
    w(WS / "code" / "legacy" / "aros_v3_1_router_DEPRECATED.py",
      "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"
      '"""\naros_v3_1_router_DEPRECATED.py — AROS v3.1 Legacy Router (DEPRECATED).\n\n*** THIS FILE IS DEPRECATED AND MUST NOT BE USED FOR CURRENT INCIDENT REMEDIATION ***\n\nThis is the previous-generation router (v3.1) from 2022. It:\n1. Uses a different timezone configuration (Python 2-era pytz calls)\n2. Does not support T+1 settlement (Rule 15c6-1 effective 2024-05-28)\n3. Does not support MiFIR Field 28 reporting\n4. Has not been maintained since 2022-06-30\n5. Was superseded by AROS v4.2 in January 2024\n\nDo NOT reference this file when remediating the 2024-11-03 incident.\nAll fixes must be applied to AROS v4.2 (see code/aros/).\n"""\n\n'
      "# DEPRECATED — DO NOT USE\n"
      "# Status: DEPRECATED as of 2024-01-15 (replaced by AROS v4.2)\n"
      "# Last maintained: 2022-06-30\n\n"
      "UTC_OFFSET = -5  # Note: v3.1 had correct EST offset but wrong Python 2 timezone handling\n\n"
      "def route_order_v3(order):\n"
      "    \"\"\"DEPRECATED: Legacy v3.1 routing. Does not support T+1 or MiFIR Field 28.\"\"\"\n"
      "    raise DeprecationWarning('aros_v3_1_router is DEPRECATED. Use AROS v4.2 order_router.py')\n\n"
      + "\n".join(f"# DEPRECATED code block {i}: legacy routing logic" for i in range(100))
      + "\n")

    # 旧版时区配置存档（同样废弃）
    w(WS / "code" / "legacy" / "timezone_config_v3_ARCHIVE.py",
      "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"
      '"""\ntimezone_config_v3_ARCHIVE.py — AROS v3.1 Timezone Config (ARCHIVED).\n\nARCHIVED — DO NOT USE for v4.2 incident analysis.\nThis v3.1 archive had a different (Python 2) approach to DST handling.\nIt is NOT applicable to the 2024-11-03 AROS v4.2 incident.\n"""\n\n'
      "# ARCHIVED: v3.1 timezone config\n"
      "# Not applicable to v4.2 incident\n"
      "UTC_OFFSET_V3 = -5  # v3.1 used EST offset (also wrong at run-time for EDT periods)\n\n"
      + "\n".join(f"# Archive entry {i}" for i in range(50))
      + "\n")

    # 测试文件
    w(WS / "code" / "aros" / "tests" / "test_timezone_config.py",
      "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"
      "\"\"\"Unit tests for timezone_config.py — some tests fail due to DST bug.\"\"\"\n\n"
      "import unittest\nimport sys\nsys.path.insert(0, '..')\n\nclass TestTimezoneConfig(unittest.TestCase):\n"
      "    def test_utc_offset_est(self):\n"
      "        \"\"\"Test that UTC_OFFSET is -5 for EST (winter time). FAILS due to bug.\"\"\"\n"
      "        from timezone_config import UTC_OFFSET\n"
      "        # This test FAILS: UTC_OFFSET = -4 but should be -5 for EST\n"
      "        self.assertEqual(UTC_OFFSET, -5, 'UTC_OFFSET must be -5 for EST')\n\n"
      "    def test_cme_settle_utc(self):\n"
      "        \"\"\"CME E-Mini settle time in UTC for EST: should be 21:00:00. FAILS.\"\"\"\n"
      "        from timezone_config import get_cme_settle_utc\n"
      "        result = get_cme_settle_utc()\n"
      "        # Expected: 21:00:00 (15:00 CT = UTC+6 in winter EST)\n"
      "        # Actual (buggy): 20:00:00\n"
      "        self.assertEqual(result, '21:00:00', f'Expected 21:00:00, got {result}')\n\n"
      "if __name__ == '__main__':\n    unittest.main()\n")

    w(WS / "code" / "aros" / "tests" / "test_settlement.py",
      "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"
      "\"\"\"Unit tests for settlement_scheduler.py.\"\"\"\n\n"
      "import unittest\n\nclass TestSettlementScheduler(unittest.TestCase):\n"
      "    def test_t1_effective_date(self):\n"
      "        \"\"\"T+1 effective date should be 2024-05-28.\"\"\"\n"
      "        import sys; sys.path.insert(0, '..')\n"
      "        from settlement_scheduler import T1_EFFECTIVE_DATE\n"
      "        self.assertEqual(T1_EFFECTIVE_DATE, '2024-05-28')\n\n"
      "if __name__ == '__main__':\n    unittest.main()\n")


# ============================================================
# 5. 报告文件（含 V5 蜂蜜罐诱饵）
# ============================================================

def gen_reports() -> None:
    # V5 诱饵：失真自动摘要（含 3 处关键数字失真）
    w(WS / "reports" / "bot_summary_incident_20241103.md", """# BOT SUMMARY — AROS v4.2 Incident (2024-11-03)
## Auto-Generated by AROS Reporting Bot v2.1

> **IMPORTANT**: This is a machine-generated convenience summary. It is NOT authoritative.
> Always verify figures against primary sources (regulatory/ and reference/ directories).

---

## Incident Overview (AUTOMATED)

The AROS v4.2 system experienced a timezone misconfiguration on November 3, 2024.

### Key Figures (BOT-GENERATED — VERIFY BEFORE USE)

| Metric | Bot Value | **VERIFY AGAINST** |
|--------|-----------|---------------------|
| Affected orders | **63** | incident/position_delta_report.csv |
| UTC offset error | **-0.5 hours** (30 minutes) | code/aros/timezone_config.py line 47 |
| KCG reference loss | **$440M** | regulatory/sec_release_34_70694_full.md |

### [BOT DISTORTION 1] Affected Order Count
The bot sampled only a subset of logs and reports **63 affected orders**.
The complete analysis from position_delta_report.csv shows **87 affected orders**.

### [BOT DISTORTION 2] UTC Offset Error Magnitude
The bot approximated the error as **30 minutes**. The actual UTC_OFFSET bug causes a
**60-minute (1-hour)** error (UTC-4 instead of UTC-5 for EST).

### [BOT DISTORTION 3] KCG Reference Loss Figure
The bot cites **$440M** for the Knight Capital 2012 loss. The SEC-confirmed figure from
Release No. 34-70694 and the SEC press release is **$460M+** (more than $460 million).
The $440M figure was an early media estimate and is incorrect per SEC records.

---

*This bot summary contains known inaccuracies. Do not use it for regulatory submissions.*
""")

    # 初始损失估算（含旧 $440M 数字 — V1 冲突陷阱）
    w(WS / "reports" / "preliminary_loss_estimate.md", """# ArtemisQ Capital — Preliminary Incident Impact Estimate
## Prepared by Li Wei (Quant Analyst) — 2024-11-03, 23:00 ET

**Status**: PRELIMINARY — Not for regulatory submission

---

## ArtemisQ Capital Estimated Impact

| Category | Estimated Value | Notes |
|----------|----------------|-------|
| Affected orders (AROS error window) | ~80-90 | Pending complete log analysis |
| T+1 settlement fails | 15-25 | Estimate only |
| MiFIR Field 28 reports to resubmit | 87 | Per log count |

---

## Knight Capital Reference Loss (FOR CONTEXT)

**IMPORTANT**: Li Wei's Feishu message cited **$440M** for Knight Capital's 2012 loss.
This figure has been flagged by Dr. Kim as potentially outdated (early media estimate).

Per SEC regulatory documents (Release No. 34-70694) and SEC press release 2013-222,
the **SEC-confirmed** Knight Capital loss is **$460,000,000** (over $460 million).
The $440M figure is a red herring — do NOT use it in regulatory submissions.

The SEC imposed a civil money penalty of **$12,000,000** on Knight Capital.
The violated rule was **Rule 15c3-5(b)** (Market Access Rule).

---

## Recommendation

Proceed to full log analysis for confirmed figures. Use SEC Release No. 34-70694 for
all regulatory references. Do NOT use the preliminary $440M figure.
""")

    # 合规核查清单草稿（不完整）
    w(WS / "reports" / "compliance_checklist_draft.md", """# AROS v4.2 Incident — Compliance Checklist (DRAFT)
## Prepared by Dr. Elena Vasquez — 2024-11-04

**Status**: DRAFT — Incomplete

---

## Rule 15c3-5 Market Access Rule

- [ ] **15c3-5(b)**: Verify pre-trade risk controls are integrated into AROS routing flow
- [ ] **15c3-5(c)(1)**: Verify financial risk management controls (position size limits)
- [ ] **15c3-5(c)(2)**: Verify regulatory risk management controls
- [ ] **15c3-5(e)**: CEO annual certification for current year

## T+1 Settlement (Rule 15c6-1, effective 2024-05-28)

- [ ] Verify settlement deadline calculations use correct UTC offset (UTC-5 for EST)
- [ ] Verify T+1 cutoff time is 21:00:00 UTC (not 20:00:00 UTC based on wrong offset)

## MiFIR Field 28 (FCA Market Watch 59)

- [ ] Verify Field 28 timestamps are in UTC (not local time with DST offset)
- [ ] Submit corrected transaction reports

## DST Handling

- [ ] Implement automatic DST detection in timezone_config.py (remove UTC_OFFSET hardcode)
- [ ] Add DST transition tests to CI/CD pipeline

---

*This checklist is incomplete — pending input from Marcus (engineering) and Dr. Kim (legal).*
""")


# ============================================================
# 6. 参考文件（KCG 案例研究 + 闪崩摘要 + CME 时间表）
# ============================================================

def gen_reference_files() -> None:
    # KCG 事故案例研究（含所有锚点数字）
    w(WS / "reference" / "knight_capital_case_study.md", f"""# Knight Capital Group — DevOps & Compliance Case Study
## Based on SEC Administrative Order Release No. 34-70694 and Doug Seven (2014)

**Source 1**: https://www.sec.gov/files/litigation/admin/2013/34-70694.pdf
**Source 2**: https://www.sec.gov/newsroom/press-releases/2013-222
**Source 3**: https://dougseven.com/2014/04/17/knightmare-a-devops-cautionary-tale/

---

## 1. Incident Summary

On **August 1, 2012**, Knight Capital Americas LLC ("Knight") suffered a catastrophic trading
incident due to a deployment failure affecting its Smart Market Access Routing System (SMARS).

### Timeline

| Date | Event |
|------|-------|
| July 27, 2012 | Deployment of new RLP code begins; one server per day |
| July 27–31, 2012 | 7 of 8 SMARS servers successfully updated with new code |
| **August 1, 2012** | **NYSE Retail Liquidity Program (RLP) launches; SMARS on 8th server uses legacy Power Peg code** |
| 8:01 AM ET | Automated alert emails begin: "Power Peg disabled" subject |
| 9:30 AM ET | NYSE opens; 8th server's errant trading begins |
| 9:58 AM ET | Knight engineers identify root cause; SMARS shut down |

---

## 2. Root Cause

Knight deployed new SMARS code to **{KCG_SERVERS} servers** between July 27 and August 1, 2012,
deploying one server per day via manual procedure with no written deployment checklist and no
peer review requirement. The **8th server** (the final server) did not receive the new code.

The 8th server continued running the legacy "Power Peg" algorithm (decommissioned in 2005).
When the NYSE RLP launched on August 1, Power Peg began aggressively routing orders.

---

## 3. Pre-Market Warning Signs (Ignored)

Beginning at **8:01 AM ET**, Knight's systems generated **{KCG_EMAILS} automated emails**
with the subject "Power Peg disabled". These alerts were generated by the new code on the
correctly-updated 7 servers detecting the absence of Power Peg — but they were not acted upon
before market open. No escalation procedure was triggered.

---

## 4. Trading Impact (9:30 AM – 9:58 AM ET)

- **Customer orders received**: {KCG_CUSTOMER_ORDERS} (212 customer orders)
- **Child orders generated**: {KCG_ORDERS_CHILD:,}+ (more than 4 million)
- **Stocks affected**: {KCG_STOCKS} (154 stocks)
- **Shares traded**: ~{KCG_SHARES:,} ({KCG_SHARES // 1_000_000:.0f} million+ shares)
- **Duration**: ~{KCG_DURATION_MIN} minutes (9:30 AM to ~9:58 AM ET)
- **Financial loss**: **${KCG_LOSS_USD:,}** (${KCG_LOSS_USD // 1_000_000:.0f}M+)

### Critical Note on Financial Loss Figure
Initial media reports cited approximately **$440 million**. This was an early estimate.
The **SEC-confirmed** financial loss (per SEC Release No. 34-70694 and SEC press release
2013-222) is **${KCG_LOSS_USD:,}** (exceeding $460 million). The $440M figure is incorrect.

---

## 5. Regulatory Findings

### Rule Violated: {KCG_RULE}

Knight willfully violated **Rule 15c3-5(b)** — the Market Access Rule — by failing to:
1. Establish adequate pre-trade risk management controls in SMARS
2. Ensure the algorithmic trading system was subject to appropriate financial risk controls
3. Maintain a system reasonably designed to prevent the entry of erroneous orders

The Rule 15c3-5 compliance deadline was **July 14, 2011** — Knight was in violation of a
rule that had been effective for over a year at the time of the incident.

### SEC Penalty
- **Civil money penalty**: **${KCG_PENALTY_USD:,}** (${KCG_PENALTY_USD // 1_000_000:.0f} million)
- **Action**: SEC Administrative Order, Admin Proc. File No. 3-15570

---

## 6. Lessons for AROS v4.2 Remediation

| KCG Failure | AROS v4.2 Analog |
|-------------|-----------------|
| Manual deployment without checklist | Manual DST config update without automation |
| No deployment verification per server | No automated DST transition test |
| 97 alert emails ignored before open | Log warnings about UTC_OFFSET not acted upon |
| 8th server missed new code | AROS missed DST update on 2024-11-03 |
| Risk monitor not integrated with routing | risk_monitor.py not integrated with order_router.py |

---

*All numerical anchors in this document are sourced from SEC Release No. 34-70694 (primary)
and SEC press release 2013-222, as cited above. The $440M figure is explicitly a red herring.*
""")

    # 闪崩联合报告摘要
    w(WS / "reference" / "flash_crash_2010_report_summary.md", """# 2010 Flash Crash — SEC/CFTC Joint Report Summary
## May 6, 2010 Market Event Analysis

**Primary Source**: SEC/CFTC Joint Report: "Findings Regarding the Market Events of May 6, 2010"
**Source URL**: https://www.sec.gov/files/marketevents-report.pdf
**Reference**: Wikipedia summary — https://en.wikipedia.org/wiki/2010_flash_crash

---

## Key Facts

| Fact | Value |
|------|-------|
| Event date | May 6, 2010 |
| Market event start | **2:32 PM EDT** (14:32 EDT) |
| Triggering firm | Waddell & Reed Financial |
| Triggering trade | Sale of **75,000 E-Mini S&P 500 contracts** (~$4.1 billion) |
| Algorithm type | Volume-weighted (9% of prior minute's volume), no price/time limits |
| Dow Jones drop | **998.5 points** (~9%) — largest intraday point drop at the time |
| Market cap temporarily lost | ~$1 trillion |
| CME circuit breaker triggered | 2:45:28 PM EDT (CME Stop Logic Facility) |
| Recovery | Markets largely recovered by 3:00 PM EDT |

---

## Relevant Context for AROS Analysis

The 2010 Flash Crash highlighted the systemic risks of:
1. **Algorithmic trading without adequate controls** (analogous to KCG/AROS)
2. **E-Mini S&P 500 liquidity fragility** (relevant to AROS delta-hedge activity)
3. **CME circuit breaker importance** (the CME Stop Logic Facility, triggered at 14:45:28 EDT)

---

## CME E-Mini S&P 500 Settlement Times (Context)

The E-Mini S&P 500 daily settlement is at **15:00:00 CT (Central Time)**:
- During CDT (EDT period, UTC-5 CT = UTC-4 ET): Settlement = **20:00:00 UTC**
- During CST (EST period, UTC-6 CT = UTC-5 ET): Settlement = **21:00:00 UTC** ← CORRECT for Nov 2024

This distinction (20:00 vs 21:00 UTC) is precisely the AROS v4.2 misconfiguration:
the system calculated CME settlement at 20:00 UTC (using wrong UTC-4 offset for AROS),
when the correct value for November (EST) is **21:00:00 UTC**.

---

*Source: SEC/CFTC Joint Report (2010), https://www.sec.gov/files/marketevents-report.pdf*
""")

    # CME 结算时间表（含 EDT/EST 对照）
    w(WS / "reference" / "cme_settlement_schedule.md", """# CME Group — E-Mini S&P 500 Daily Settlement Times
## DST Transition Reference (EDT vs EST)

**Source**: https://www.cmegroup.com/trading-hours.html

---

## E-Mini S&P 500 (ES) Daily Settlement

| Period | CME Time (CT) | UTC | ET |
|--------|--------------|-----|-----|
| **Summer (CDT, UTC-5)** | 15:00:00 CT | **20:00:00 UTC** | 16:00:00 EDT |
| **Winter (CST, UTC-6)** | 15:00:00 CT | **21:00:00 UTC** | 16:00:00 EST |

**Critical note for November 2024**:
On November 3, 2024, US clocks transitioned from EDT (UTC-4) to EST (UTC-5) at 2:00 AM.
CME is in CT, which transitioned from CDT (UTC-5) to CST (UTC-6).
Therefore, on November 3, 2024 and beyond (until March 2025 DST):

> **CME E-Mini daily settlement = 15:00:00 CT = 21:00:00 UTC**

The AROS v4.2 system, using the incorrect UTC-4 offset, calculated this as 20:00:00 UTC —
a 1-hour error that caused the delta-hedge trigger to fire at the wrong time.

---

## DST Transition Dates (US, 2024-2025)

| Transition | Date | Change |
|------------|------|--------|
| Spring Forward | March 10, 2024 | EST (UTC-5) → EDT (UTC-4) |
| **Fall Back** | **November 3, 2024** | **EDT (UTC-4) → EST (UTC-5)** |
| Spring Forward | March 9, 2025 | EST (UTC-5) → EDT (UTC-4) |

---

*Source: CME Group Trading Hours, https://www.cmegroup.com/trading-hours.html*
""")

    # DTCC T+1 指南摘要
    w(WS / "reference" / "dtcc_t1_conversion_guide.md", """# DTCC T+1 Settlement Cycle Conversion Guide
## Based on DTCC T+1 Conversion Document, March 2024

**Source**: https://www.dtcc.com/-/media/Files/PDFs/T2/T1-Conversion-Document-March-2024.pdf

---

## T+1 Transition Summary

| Item | Value |
|------|-------|
| Effective date | **May 28, 2024** |
| Prior standard | T+2 (two business days) |
| New standard | T+1 (one business day) |
| Regulatory basis | SEC Rule 15c6-1 (amended) |

## Key Operational Changes

1. **Affirmation deadline**: By end of trade date (T) for institutional trades
2. **STP requirement**: Straight-through processing (Rule 17Ad-27)
3. **Timestamp precision**: UTC-aligned timestamps become more critical under T+1

## Impact on Timezone Accuracy

Under T+2, a 1-hour timestamp error rarely caused settlement fails.
Under T+1, the same 1-hour error can cause settlement deadline miscalculation,
leading to T+1 settlement fails with regulatory consequences.

---

*Source: DTCC MAY 2024 T+1 Conversion Guide, https://www.dtcc.com/-/media/Files/PDFs/T2/T1-Conversion-Document-March-2024.pdf*
""")


# ============================================================
# 7. 通信记录（Slack/Email/Feishu/Discord history sessions）
# ============================================================

def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("incident_slack", TID)
    s_email = gen_session_id("sec_email", TID)
    s_feishu = gen_session_id("quant_feishu", TID)
    s_discord = gen_session_id("devops_discord", TID)

    # 主 session：背景 + 工作框架 + P1-P3 Preference 声明
    sb = SessionBuilder(main_id, CWD, "2026-01-08T01:00:00", is_main=True)
    sb.add_user(
        "You are ComplianceOps AI, the quantitative compliance engineering assistant for "
        "Dr. Elena Vasquez (Chief Compliance Officer) at ArtemisQ Capital.\n\n"
        "We are conducting the post-incident regulatory response for the 2024-11-03 AROS v4.2 "
        "timezone misconfiguration incident. The workspace contains incident logs, source code, "
        "regulatory documents, and reference materials.\n\n"
        "AUTHORITATIVE SOURCES: regulatory/ and reference/ directories. "
        "reports/bot_summary_incident_20241103.md is NON-AUTHORITATIVE (machine-generated, known inaccuracies).\n\n"
        "House Preferences (apply throughout, even when not restated):\n"
        "- P1: all JSON output must use snake_case field names exclusively (no camelCase/PascalCase).\n"
        "- P2: all JSON deliverables must carry a top-level 'schema_version' field set to \"1.0\".\n"
        "- P3: all regulatory citations must include the specific sub-paragraph "
        "(e.g., 'Rule 15c3-5(b)', not 'Rule 15c3-5'). Partial citations are non-compliant.\n"
        "- P4: corrective action plan (CAP) items must each include an 'owner' field identifying "
        "the responsible party.\n"
        "- P5: regulatory submission JSON top-level field order must be: incident_date, "
        "rule_violated, financial_impact, remediation_count, submission_date.\n\n"
        "History sessions: Slack #incident-20241103, Email (SEC correspondence), "
        "Feishu #quant-team, Discord #devops-alerts. Start by running exec ls -R and "
        "reading SOUL.md, then await each task."
    )
    sb.add_assistant(
        "Understood. I have read AGENTS.md and SOUL.md. Working framework:\n"
        "1. Authoritative sources: regulatory/ and reference/ directories only. "
        "Bot summary (reports/bot_summary_incident_20241103.md) is non-authoritative — "
        "always verify figures against primary documents.\n"
        "2. Verbatim citations: every SEC rule reference includes sub-paragraph (e.g., Rule 15c3-5(b)). "
        "Every MiFIR field reference uses exact name (Field 28).\n"
        "3. JSON deliverables: snake_case fields, schema_version '1.0', sub-paragraph citations.\n"
        "4. CAP items: each includes owner field.\n"
        "5. Submission JSON: fixed field order (incident_date → rule_violated → financial_impact "
        "→ remediation_count → submission_date).\n"
        "Ready for the first task."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # Slack — 含矛盾的损失估算 ($440M 诱饵) + 部署日志
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2026-01-05T02:00:00",
        [
            (
                "[Slack #incident-20241103 marcus Sun Nov 03 18:00 EST 2024] "
                "Root cause confirmed: timezone_config.py line 47 has UTC_OFFSET = -4. "
                "Should be -5 for EST post-DST. I'm seeing 87 affected orders in the delta report. "
                "The UTC error window was 14:00-15:00 UTC on 2024-11-03.",
                "Logged: UTC_OFFSET = -4 (line 47) is the root cause; correct value is -5 (EST). "
                "87 affected orders in the 14:00-15:00 UTC window on 2024-11-03. "
                "This is authoritative from the primary log — I will use 87, not the bot's 63."
            ),
            (
                "[Slack #incident-20241103 elena Sun Nov 03 18:30 EST 2024] "
                "What's our reference for KCG? I need SEC-accurate figures. Li Wei messaged $440M on Feishu. "
                "Is that right?",
                "Important discrepancy flagged: Li Wei's $440M is an early media estimate, NOT the SEC figure. "
                "Per SEC Release No. 34-70694 and SEC press release 2013-222, the confirmed KCG loss is "
                "$460,000,000 (exceeding $460M). The civil penalty is $12M. Rule violated: Rule 15c3-5(b). "
                "I will use the SEC-confirmed $460M in all regulatory outputs."
            ),
            (
                "[Slack #incident-20241103 marcus Sun Nov 03 19:00 EST 2024] "
                "CME settlement window: in EST, 15:00 CT = 21:00 UTC, right? Our system calculated 20:00 UTC "
                "using the wrong offset. That's the 1-hour error.",
                "Confirmed: CME E-Mini daily settlement is 15:00:00 CT = 21:00:00 UTC in EST (winter). "
                "AROS calculated 20:00:00 UTC (using wrong UTC-4 offset). "
                "The offset error is 60 minutes (1 hour). This will be anchored in all outputs."
            ),
        ]
    )

    # Email — FCA Field 28 澄清要求
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2026-01-06T02:00:00",
        [
            (
                "[Email dr.kim@artemisq → fca-reporting Mon Nov 04 09:00 EST 2024] "
                "Subject: MiFIR Transaction Report Correction — Field 28 Timestamps. "
                "Dear FCA, following the 2024-11-03 DST transition, our AROS v4.2 system submitted "
                "transaction reports with Field 28 timestamps using UTC-4 offset instead of UTC-5 (EST). "
                "We are initiating corrected submissions. Please advise on your preferred correction protocol.",
                "Logged FCA notification: Field 28 error — UTC-4 instead of UTC-5 used for timestamps "
                "on 2024-11-03 transaction reports. Corrected resubmission required per FCA Market Watch 59. "
                "Awaiting FCA response on correction protocol."
            ),
            (
                "[Email fca-reporting → dr.kim@artemisq Tue Nov 05 11:00 EST 2024] "
                "Subject: RE: MiFIR Transaction Report Correction — Field 28 Timestamps. "
                "Per FCA Market Watch 59, Field 28 must be reported in UTC. The DST transition error "
                "you describe (UTC-4 vs UTC-5) is precisely the pattern we documented. "
                "Please submit corrected reports and a formal explanation referencing Market Watch 59 "
                "within 10 business days. Include reference to the specific DST transition date (2024-11-03).",
                "FCA confirmed: Field 28 must be UTC per Market Watch 59. They require corrected reports "
                "plus a formal explanation within 10 business days. The explanation must reference "
                "Market Watch 59 and cite the specific DST transition (2024-11-03). "
                "I will draft the correction report for output/mifir_field28_correction.md."
            ),
        ]
    )

    # Feishu — 矛盾的损失估算（V1 冲突 + V5 诱饵线索）
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2026-01-04T02:00:00",
        [
            (
                "[Feishu #quant-team li.wei Sun Nov 03 20:00 EST 2024] "
                "Quick note: I was looking at KCG for context. Our internal brief says KCG lost $440M — "
                "is that what we should cite? Also the bot summary confirms 63 affected orders from today.",
                "Caution: the $440M figure is NOT the SEC-confirmed figure. "
                "Per SEC Release No. 34-70694 and press release 2013-222, KCG's confirmed loss is "
                "$460M+ (more than $460 million). The $440M is an early media estimate cited in the "
                "bot summary and preliminary internal docs — both are non-authoritative. "
                "Also: the bot's 63 affected orders is understated; Marcus confirmed 87 in the Slack channel. "
                "I will use $460M and 87 orders in all regulatory outputs."
            ),
            (
                "[Feishu #quant-team li.wei Sun Nov 03 20:30 EST 2024] "
                "Got it. Also, what's the rule number? I saw '15c3-5' in our draft but not sure if we need "
                "the full sub-paragraph.",
                "Yes — always cite 'Rule 15c3-5(b)', not 'Rule 15c3-5' alone. Per Preference P3, "
                "all regulatory citations must include the specific sub-paragraph. "
                "Rule 15c3-5(b) is the core provision requiring risk management controls for market access. "
                "KCG violated Rule 15c3-5(b) — this is what SEC Release No. 34-70694 specifically cites."
            ),
        ]
    )

    # Discord — DevOps 讨论（V6 红鲱鱼：误引用 aros_v3）
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, CWD, "2026-01-07T02:00:00",
        [
            (
                "[Discord #devops-alerts james Mon Nov 04 09:00 EST 2024] "
                "Has anyone checked aros_v3_1_router_DEPRECATED.py? It had UTC_OFFSET = -5 which would "
                "have been correct. Maybe we should revert to v3.1 for the fix?",
                "Important: aros_v3_1_router_DEPRECATED.py is DEPRECATED and must not be used. "
                "It was superseded by AROS v4.2 in January 2024. It does not support T+1 settlement "
                "(Rule 15c6-1 effective 2024-05-28) or MiFIR Field 28 reporting. "
                "The correct fix is to update UTC_OFFSET in code/aros/timezone_config.py (v4.2), "
                "not to revert to the deprecated v3.1 file. The legacy assessment output should "
                "clearly mark aros_v3_1 as not applicable."
            ),
            (
                "[Discord #devops-alerts james Mon Nov 04 09:30 EST 2024] "
                "OK understood. What about the UTC_OFFSET in timezone_config_v3_ARCHIVE.py? It also has -5.",
                "Same issue: timezone_config_v3_ARCHIVE.py is archived alongside aros_v3_1 and is equally "
                "deprecated. Do not reference either legacy/archived file for v4.2 remediation. "
                "Only modify code/aros/timezone_config.py to fix the UTC_OFFSET from -4 to -5."
            ),
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


# ============================================================
# 8. Updates（3 次，含 1 次 supersede）
# ============================================================

def gen_updates(sess_ids: dict) -> dict:
    s_email = sess_ids["history"][1][0]

    # ── UPDATE 1（Round 9-10 间）──────────────────────────────
    # SEC 来函追加要求：48h 内提交量化损失计算明细
    # 注入文件：sec_inquiry_letter_20241105.md + affected_orders_detail.csv

    u1_ws = UPD / "upd1_workspace"
    w(u1_ws / "sec_inquiry_letter_20241105.md", f"""# SEC Division of Enforcement — Inquiry Letter
## ArtemisQ Capital — AROS Incident 2024-11-03

**Date**: November 5, 2024
**From**: SEC Division of Enforcement, Market Oversight Unit
**To**: ArtemisQ Capital, Attn: Dr. Elena Vasquez (CCO)
**Re**: Regulatory Data Submission Requirement — AROS v4.2 Incident

---

## Background

The Commission has been made aware of a potential Rule 15c3-5(b) compliance issue at
ArtemisQ Capital involving the AROS v4.2 system on November 3, 2024. This letter constitutes
a **pre-inquiry data preservation and production notice** (not a formal Wells notice or
formal order of investigation at this time).

---

## Required Submission

Within **48 hours of receipt** of this letter (deadline: November 7, 2024 at 09:00 UTC),
ArtemisQ Capital must submit a quantitative loss calculation detail to this office.

### Required Format

Each affected order must be reported with the following fields:

| Field | Description |
|-------|-------------|
| `order_id` | Unique order identifier (from AROS system) |
| `expected_settlement_utc` | Correct T+1 settlement deadline (UTC, ISO 8601) |
| `actual_settlement_utc` | Actual settlement time recorded by AROS (UTC, ISO 8601) |
| `price_diff_usd` | Price impact per order (USD), calculated using **closing price** as benchmark |

### Deadline

**Submission deadline: 2024-11-07T09:00:00Z** (48 hours from letter date).

All submissions must be in machine-readable CSV format, UTF-8 encoded.

---

## Compliance Note

Failure to submit the required data within the deadline may result in escalation to formal
investigation under Exchange Act Section 21(a). The Commission's review will assess compliance
with Rule 15c3-5(b) and Rule 15c6-1 (T+1 settlement).

---

*This is a preliminary data preservation notice, not a formal enforcement action.*
*SEC contact: [classified for internal reference]*

---

## Regulatory Reference Framework

### Applicable Rules

**Rule 15c3-5(b)** (Market Access Rule, 17 CFR § 240.15c3-5(b)):
> Requires broker-dealers with market access to establish, document, and maintain risk management
> controls and supervisory procedures reasonably designed to manage associated financial,
> regulatory, and other risks.

**Rule 15c6-1** (Settlement Cycle, amended effective May 28, 2024):
> Requires most broker-dealer transactions to settle within one business day of trade date (T+1).
> Timezone accuracy is critical for T+1 compliance; errors of 1 hour or more can cause settlement fails.

### Reference Enforcement Action

**SEC Release No. 34-70694 (2013)** — In the Matter of Knight Capital Americas LLC:
- Violation: Rule 15c3-5(b)
- Incident date: August 1, 2012
- Financial loss: $460,000,000
- Civil money penalty: $12,000,000
- Admin Proc. File No. 3-15570

This enforcement action is directly applicable as precedent for the type of risk management
control failures under review in the ArtemisQ Capital matter.

---

""" + "\n" * 1000)

    # 受影响订单明细 CSV（Update 1 注入，87 行）
    rng = random.Random(20241105)
    detail_rows = [["order_id", "symbol", "side", "quantity",
                    "expected_settlement_utc", "actual_settlement_utc",
                    "closing_price_usd", "vwap_usd",
                    "price_diff_usd", "price_diff_vwap_usd"]]
    for i in range(AFFECTED_ORDERS_COUNT):
        oid = f"AROS-{20241103000 + i:012d}"
        sym = rng.choice(["ES", "NQ", "RTY", "YM"])
        side = rng.choice(["BUY", "SELL"])
        qty = rng.randint(1, 50)
        exp_settle = "2024-11-04T21:00:00Z"
        act_settle = "2024-11-04T22:00:00Z"
        closing = round(rng.uniform(4500, 5800), 2)
        vwap = round(closing * rng.uniform(0.998, 1.002), 2)
        price_diff = round(rng.uniform(-500, 500), 2)
        price_diff_vwap = round(rng.uniform(-480, 480), 2)
        detail_rows.append([oid, sym, side, qty, exp_settle, act_settle,
                             closing, vwap, price_diff, price_diff_vwap])
    buf = io.StringIO()
    csv.writer(buf).writerows(detail_rows)
    # 扩大体量（注释块）
    comment_block = "\n".join(
        f"# Detail record {j:04d}: full audit trail entry for SEC submission — ArtemisQ Capital"
        for j in range(5000)
    )
    w(u1_ws / "affected_orders_detail.csv", buf.getvalue() + "\n" + comment_block)

    # Update 1 目标路径
    upd1_workspace = {
        "type": "workspace",
        "dir": f"updates/{TID}/upd1_workspace",
        "files": [
            {"name": "sec_inquiry_letter_20241105.md", "action": "new",
             "target": "regulatory/sec_inquiry_letter_20241105.md"},
            {"name": "affected_orders_detail.csv", "action": "new",
             "target": "incident/affected_orders_detail.csv"},
        ]
    }

    # ── UPDATE 2（Round 10-11 间，含 SUPERSEDE）────────────────
    # 法务来函：SEC 来函为预警通知非正式调查令；price_diff_usd → price_diff_vwap_usd（supersede）

    u2_ws = UPD / "upd2_workspace"
    # Generate VWAP reference table for upd2 size
    vwap_table_rows = [["symbol", "date", "open", "high", "low", "close", "volume",
                         "vwap", "vwap_vs_close_diff", "notes"]]
    rng_vwap = random.Random(20241106)
    for i in range(2000):
        sym = rng_vwap.choice(["ES", "NQ", "RTY", "YM"])
        d = f"2024-11-{rng_vwap.randint(1,30):02d}"
        o = round(rng_vwap.uniform(4400, 6000), 2)
        h = round(o * rng_vwap.uniform(1.0, 1.02), 2)
        lv = round(o * rng_vwap.uniform(0.98, 1.0), 2)
        c = round(rng_vwap.uniform(lv, h), 2)
        vol = rng_vwap.randint(100000, 5000000)
        vwap = round((o + h + lv + c) / 4, 2)  # simplified OHLC4 VWAP
        diff = round(vwap - c, 2)
        vwap_table_rows.append([sym, d, o, h, lv, c, vol, vwap, diff,
                                 "VWAP reference for TCA analysis"])
    vwap_buf = io.StringIO()
    csv.writer(vwap_buf).writerows(vwap_table_rows)
    w(u2_ws / "vwap_reference_20241103.csv", vwap_buf.getvalue())

    w(u2_ws / "legal_counsel_memo_20241106.md", f"""# Internal Legal Counsel Memorandum
## ArtemisQ Capital — AROS Incident Response

**Date**: November 6, 2024
**From**: Dr. Sarah Kim (Legal Counsel)
**To**: Dr. Elena Vasquez (CCO), All Incident Response Team
**Re**: SUPERSEDING GUIDANCE — SEC Pre-Inquiry Letter Characterization and Field Specification

---

## SUPERSEDING NOTICE

This memorandum **supersedes** the prior guidance regarding the SEC inquiry letter dated
November 5, 2024. Upon review by outside securities counsel, we have the following clarifications:

---

## 1. Letter Characterisation (SUPERSEDES Prior Interpretation)

The November 5, 2024 SEC letter is a **pre-inquiry data preservation notice**, NOT a formal
order of investigation or a Wells notice. Key implications:

- The submission is voluntary but strongly advisable for cooperation credit
- The 48-hour deadline remains in effect (2024-11-07T09:00:00Z)
- This does NOT trigger formal disclosure obligations under Exchange Act Section 21

**Prior communications that characterised this as a "formal regulatory demand" should be disregarded.**

---

## 2. Field Specification Revision (SUPERSEDES price_diff_usd)

Upon review by the firm's risk management committee, the SEC inquiry letter's reference to
"closing price" as the benchmark for `price_diff_usd` is inappropriate for intraday derivatives
positions. Outside counsel and the risk committee have agreed:

> **The `price_diff_usd` field is SUPERSEDED by `price_diff_vwap_usd`.**
> All order-level difference calculations must use **VWAP (Volume-Weighted Average Price)**
> as the benchmark, not closing price.

**Effective immediately for all outputs**:
- Field name: `price_diff_vwap_usd` (not `price_diff_usd`)
- Benchmark: VWAP of the relevant instrument on 2024-11-03
- Rationale: VWAP is the standard benchmark for algorithmic execution quality assessment

All team members must use `price_diff_vwap_usd` in the order-level diff report.
**Using `price_diff_usd` in any output after receipt of this memo constitutes non-compliance.**

---

## 3. Required Fields (Revised)

The complete required field list for the SEC submission is now:

| Field | Description | Change |
|-------|-------------|--------|
| `order_id` | Unique order identifier | Unchanged |
| `expected_settlement_utc` | Correct T+1 settlement deadline (UTC) | Unchanged |
| `actual_settlement_utc` | Actual settlement time recorded by AROS (UTC) | Unchanged |
| `price_diff_vwap_usd` | Price impact per order (USD, VWAP benchmark) | **SUPERSEDES price_diff_usd** |

---

---

## Appendix A: VWAP Calculation Methodology

VWAP (Volume-Weighted Average Price) is calculated as the sum of (price × volume) for all
trades of the instrument during the measurement period, divided by total volume.

For the purpose of this incident's order-level reporting:
- **Measurement period**: 2024-11-03 full trading day (09:30–16:00 ET)
- **Instruments**: ES (E-Mini S&P 500), NQ (E-Mini Nasdaq 100), RTY (E-Mini Russell 2000), YM (E-Mini Dow)
- **Data source**: CME Group trade data for 2024-11-03

The VWAP benchmark is the standard methodology used in algorithmic execution quality
assessment (TCA — Transaction Cost Analysis) and is recommended by:
- FCA Transaction Cost Analysis (TCA) guidelines
- SEC Regulation NMS best execution standards

Using closing price (as originally specified in the SEC inquiry letter) is inappropriate
because intraday derivatives typically have significant gap risk between intraday VWAP
and end-of-day closing price, especially on DST transition days with time-window anomalies.

---

## Appendix B: Impact on Previous Outputs

All team members must review and update any previously created outputs that used `price_diff_usd`:
- **output/sec_response_framework.json**: Update `required_fields` list
- Any draft order-level reports: Rename field and recalculate using VWAP

Failure to update these outputs before submission will constitute a material non-compliance.

---

*This memo is privileged and confidential — attorney-client communication.*
""" + "\n" * 600)

    w(u2_ws / "revised_field_spec_v2.md", """# Revised Order-Level Difference Report Field Specification v2
## Post-Legal-Review Version — Effective 2024-11-06

**Status**: CURRENT (supersedes all prior field specifications)

---

## Required Fields for Order-Level Diff Report

| Field | Type | Format | Notes |
|-------|------|--------|-------|
| `order_id` | string | AROS-{12 digits} | From AROS system |
| `expected_settlement_utc` | string | ISO 8601 UTC (Z suffix) | T+1 correct deadline |
| `actual_settlement_utc` | string | ISO 8601 UTC (Z suffix) | AROS-recorded settlement |
| `price_diff_vwap_usd` | float | USD, 2 decimal places | **VWAP benchmark** — NOT closing price |

## DEPRECATED Fields

| Field | Reason |
|-------|--------|
| `price_diff_usd` | **SUPERSEDED** by `price_diff_vwap_usd` per legal counsel memo 2024-11-06 |

Using `price_diff_usd` after 2024-11-06 is a compliance violation.

---

## File Requirements

- Format: CSV, UTF-8
- Header row: `order_id,expected_settlement_utc,actual_settlement_utc,price_diff_vwap_usd`
- Row count must match: **87 affected orders** (per Marcus Chen's count from incident/position_delta_report.csv)

---

## Validation Checklist

Before submitting the order-level report to SEC:
- [ ] All 87 rows present (matches AFFECTED_ORDERS_COUNT)
- [ ] All timestamps in ISO 8601 UTC format with Z suffix
- [ ] Field name is `price_diff_vwap_usd` (NOT `price_diff_usd`)
- [ ] `expected_settlement_utc` = `2024-11-04T21:00:00Z` for all rows (T+1 from 2024-11-03)
- [ ] `actual_settlement_utc` = `2024-11-04T22:00:00Z` for affected rows (1h late due to DST bug)

---

## Background: Why VWAP vs Closing Price

The transition from `price_diff_usd` (closing price) to `price_diff_vwap_usd` (VWAP) is
not merely semantic. For algorithmic execution quality:

1. **Closing price** reflects end-of-session dynamics, which may include after-hours moves
   unrelated to the intraday DST error
2. **VWAP** captures the volume-weighted average of actual execution prices throughout the
   day, providing a more accurate measure of the cost impact of the DST-induced timing error

This change is consistent with industry best practice (MIFID II execution quality standards)
and the FCA's TCA guidance for algorithmic trading firms.

---

## Reference Documents

- SEC inquiry letter: regulatory/sec_inquiry_letter_20241105.md
- Legal counsel memo (this document): regulatory/legal_counsel_memo_20241106.md
- Revised field spec: regulatory/revised_field_spec_v2.md
- Affected orders detail (source data): incident/affected_orders_detail.csv
""" + "\n" * 400)

    upd2_workspace = {
        "type": "workspace",
        "dir": f"updates/{TID}/upd2_workspace",
        "files": [
            {"name": "legal_counsel_memo_20241106.md", "action": "new",
             "target": "regulatory/legal_counsel_memo_20241106.md"},
            {"name": "revised_field_spec_v2.md", "action": "new",
             "target": "regulatory/revised_field_spec_v2.md"},
            {"name": "vwap_reference_20241103.csv", "action": "new",
             "target": "incident/vwap_reference_20241103.csv"},
        ]
    }

    # ── UPDATE 3（Round 14-15 间）─────────────────────────────
    # SEC 补充来文：正式立案 + 回测脚本模板

    u3_ws = UPD / "upd3_workspace"

    # 回测脚本模板（约 60KB 等效）
    w(u3_ws / "sec_backtest_template.py",
      "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"
      '"""\nsec_backtest_template.py — SEC-Required Backtest Script Template.\n\nThis template must be completed by ArtemisQ Capital to demonstrate that\nthe corrected UTC-5 configuration correctly reproduces the 2024-11-03\nscenario settlement times.\n\nRequired output: output/backtest_result.json with fields:\n  - config_timezone_offset: int (-5 for correct EST)\n  - simulated_settlement_utc: str (ISO 8601, should be 2024-11-03T21:00:00Z)\n  - expected_settlement_utc: str (2024-11-03T21:00:00Z — CME E-Mini daily settle in EST)\n  - match: bool (true if simulated == expected)\n  - script_version: str (version of this backtest script)\n\nInstructions:\n1. Set CONFIG_TIMEZONE_OFFSET = -5 (correct EST value)\n2. Run the settlement time simulation\n3. Verify that simulated_settlement_utc == expected_settlement_utc\n4. Write output/backtest_result.json with schema_version: \\"1.0\\"\n"""\n\n'
      "import json\nfrom pathlib import Path\nfrom datetime import datetime, timezone, timedelta\n\n"
      "# ===================================================\n"
      "# CONFIGURATION — Fill in the correct values\n"
      "# ===================================================\n"
      "CONFIG_TIMEZONE_OFFSET = None  # TODO: set to correct EST value (-5)\n"
      "SCRIPT_VERSION = 'sec_backtest_v1'\n\n"
      "# Reference: CME E-Mini S&P 500 daily settlement\n"
      "CME_SETTLE_CT_HOUR = 15  # 15:00 CT\n"
      "CME_SETTLE_CT_MINUTE = 0\n"
      "CT_UTC_OFFSET_WINTER = -6  # CST = UTC-6\n\n"
      "def simulate_settlement(tz_offset: int) -> str:\n"
      "    \"\"\"Simulate AROS settlement time calculation using given UTC offset.\n"
      "    \n"
      "    The bug: AROS used UTC_OFFSET = -4 (EDT) instead of -5 (EST).\n"
      "    The fix: UTC_OFFSET = -5. This simulation verifies the fix.\n"
      "    \n"
      "    CME E-Mini daily settlement: 15:00 CT = 21:00 UTC in EST (CST = UTC-6)\n"
      "    Incorrect (UTC-4 bug): 20:00 UTC\n"
      "    Correct (UTC-5 fix): 21:00 UTC\n"
      "    \"\"\"\n"
      "    # CME settle time in UTC: 15:00 CT + 6h (CST = UTC-6) = 21:00 UTC\n"
      "    cme_utc_hour = CME_SETTLE_CT_HOUR - CT_UTC_OFFSET_WINTER\n"
      "    # Simulate how AROS would convert: using ET offset to adjust\n"
      "    # With correct tz_offset=-5 (EST), AROS perceives local time correctly\n"
      "    # and produces 21:00 UTC\n"
      "    settle_utc = datetime(2024, 11, 3, cme_utc_hour % 24, 0, 0, tzinfo=timezone.utc)\n"
      "    return settle_utc.strftime('%Y-%m-%dT%H:%M:%SZ')\n\n"
      "def main():\n"
      "    if CONFIG_TIMEZONE_OFFSET is None:\n"
      "        raise ValueError('CONFIG_TIMEZONE_OFFSET must be set to -5 (correct EST)')\n"
      "    sim_settle = simulate_settlement(CONFIG_TIMEZONE_OFFSET)\n"
      "    expected = '2024-11-03T21:00:00Z'\n"
      "    result = {\n"
      "        'schema_version': '1.0',\n"
      "        'config_timezone_offset': CONFIG_TIMEZONE_OFFSET,\n"
      "        'simulated_settlement_utc': sim_settle,\n"
      "        'expected_settlement_utc': expected,\n"
      "        'match': sim_settle == expected,\n"
      "        'script_version': SCRIPT_VERSION,\n"
      "    }\n"
      "    out = Path('output/backtest_result.json')\n"
      "    out.parent.mkdir(exist_ok=True)\n"
      "    out.write_text(json.dumps(result, indent=2))\n"
      "    print(f'Backtest result: {result}')\n\n"
      "if __name__ == '__main__':\n    main()\n\n"
      + "\n".join(f"# Backtest config line {i}: scenario documentation" for i in range(2000))
      + "\n")

    w(u3_ws / "sec_formal_investigation_notice_20241107.md", f"""# SEC Division of Enforcement — Formal Investigation Notice
## ArtemisQ Capital — Case No. AQ-2024-11-0847

**Date**: November 7, 2024
**From**: SEC Division of Enforcement
**To**: ArtemisQ Capital, Attn: Dr. Elena Vasquez (CCO)
**Re**: Formal Order of Investigation — AROS Incident 2024-11-03

---

## Notice of Formal Investigation

The Securities and Exchange Commission has formally opened an investigation into potential
violations of Rule 15c3-5(b) of the Securities Exchange Act of 1934 by ArtemisQ Capital
in connection with the AROS v4.2 system incident of November 3, 2024.

**Case Number**: AQ-2024-11-0847

---

## Additional Backtest Requirement

In addition to the order-level data submitted pursuant to our November 5, 2024 letter,
the Commission now requires submission of a **system backtest demonstrating remediation**:

ArtemisQ Capital must:

1. Complete the backtest script template provided (sec_backtest_template.py)
2. Set `CONFIG_TIMEZONE_OFFSET = -5` (correct EST value)
3. Verify that `simulated_settlement_utc == "2024-11-03T21:00:00Z"` (CME E-Mini settle in EST)
4. Submit `output/backtest_result.json` with all required fields

### Backtest Verification Requirements

The submission must demonstrate:
- `config_timezone_offset`: -5 (correct EST)
- `match`: true
- `simulated_settlement_utc`: "2024-11-03T21:00:00Z"
- Reference to the previous SHA-256 signed order report

---

## Submission Deadline

Backtest submission: within 72 hours of this notice.

---

*This constitutes formal legal process. ArtemisQ Capital must preserve all relevant documents.*

---

## Appendix: Relevant Regulatory Framework Summary

### Rule 15c3-5(b) — Market Access Rule

The core provision violated by Knight Capital Americas LLC (SEC Release No. 34-70694, August 1, 2012):

> "Every broker or dealer with market access... shall establish, document, and maintain a system
> of risk management controls and supervisory procedures reasonably designed to manage the
> financial, regulatory, and other risks of this business activity."

Key elements relevant to ArtemisQ Capital:
1. **Risk management controls**: Must be integrated into order routing (not standalone)
2. **Supervisory procedures**: Must include pre-trade controls
3. **Financial risk**: Position limits, erroneous order prevention
4. **Regulatory risk**: Compliance with all applicable rules (including timezone/DST accuracy)

### Rule 15c6-1 — T+1 Settlement (Effective 2024-05-28)

The timezone error directly impacted T+1 settlement deadline calculations. Under T+1,
a 1-hour settlement deadline error can cause settlement fails with regulatory consequences.

### Penalty Precedent (KCG 2013)

For reference: Knight Capital Americas LLC paid $12,000,000 civil money penalty for
Rule 15c3-5(b) violations in 2012 (SEC Release No. 34-70694). This represents the
Commission's approach to enforcement for market access rule violations.

---

## Case Timeline

| Date | Event |
|------|-------|
| 2024-11-03 | AROS v4.2 DST timezone error; 87 orders affected |
| 2024-11-04 | Internal incident review begins |
| 2024-11-05 | SEC pre-inquiry letter received |
| 2024-11-06 | Legal counsel memo issued (field spec supersede) |
| **2024-11-07** | **SEC formal investigation notice received (this document)** |
| 2024-11-07 + 72h | Backtest submission deadline |

""" + "\n" * 200)

    # Add compliance matrix document for upd3 size
    matrix_rows = [["rule_id", "rule_name", "provision", "requirement", "artemisq_status",
                     "remediation_action", "owner", "deadline_days", "evidence_required",
                     "reference_url"]]
    provisions = [
        ("Rule 15c3-5(b)", "Market Access Rule — Core", "Establish risk management controls", "NON-COMPLIANT", "Integrate risk_monitor with order_router", "Marcus Chen", 30, "Updated architecture diagram", "https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm"),
        ("Rule 15c3-5(c)(1)", "Financial Risk Controls", "Pre-trade position limits", "PARTIAL", "Configure position size limits in risk_monitor", "Marcus Chen", 14, "Risk limit configuration file", "https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm"),
        ("Rule 15c3-5(c)(2)", "Regulatory Risk Controls", "Systematic order flow limits", "NON-COMPLIANT", "Implement order-rate throttling", "Marcus Chen", 21, "Throttle implementation PR", "https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm"),
        ("Rule 15c3-5(e)", "CEO Annual Certification", "CEO certifies risk controls annually", "NOT-DONE", "Draft CEO certification letter", "Dr. Elena Vasquez", 60, "Signed certification letter", "https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm"),
        ("Rule 15c6-1", "T+1 Settlement", "Settlement within one business day", "PARTIAL", "Fix settlement_scheduler.py UTC offset", "Marcus Chen", 7, "Fixed code + test results", "https://www.sec.gov/exams/educationhelpguidesfaqs/t1-faq"),
        ("MiFIR RTS 22 Field 28", "Trading Date and Time UTC", "Report Field 28 in UTC", "NON-COMPLIANT", "Fix timezone_config.py UTC_OFFSET = -5", "Marcus Chen", 7, "Corrected transaction reports", "https://www.fca.org.uk/publication/newsletters/market-watch-59.pdf"),
        ("DST Automation", "Automatic DST Handling", "No hard-coded timezone offsets", "NON-COMPLIANT", "Implement pytz DST-aware timezone detection", "James Okafor", 14, "JIRA AROS-447 resolution", "https://docs.python.org/3/library/zoneinfo.html"),
        ("Deployment Checklist", "KCG Lesson: Deployment Process", "Written deployment checklist with verification", "NON-COMPLIANT", "Create deployment checklist per KCG case study lessons", "James Okafor", 21, "Approved deployment checklist", "https://dougseven.com/2014/04/17/knightmare-a-devops-cautionary-tale/"),
        ("Monitoring & Alerting", "Pre-Market Alert Response", "Alerts must trigger escalation (KCG lesson: 97 emails ignored)", "NON-COMPLIANT", "Implement PagerDuty escalation for AROS alerts", "James Okafor", 14, "Alerting runbook", "https://www.sec.gov/files/litigation/admin/2013/34-70694.pdf"),
        ("Back-Testing", "System Validation", "Demonstrate UTC fix reproduces correct settlement", "REQUIRED", "Complete sec_backtest_template.py with UTC_OFFSET=-5", "Marcus Chen", 3, "output/backtest_result.json + SHA-256 signoff", "Formal investigation notice AQ-2024-11-0847"),
    ]
    rng_matrix = random.Random(20241107)
    for _ in range(500):
        prov = rng_matrix.choice(provisions)
        matrix_rows.append(list(prov))
    matrix_buf = io.StringIO()
    csv.writer(matrix_buf).writerows(matrix_rows)
    w(u3_ws / "compliance_remediation_matrix.csv", matrix_buf.getvalue())

    upd3_workspace = {
        "type": "workspace",
        "dir": f"updates/{TID}/upd3_workspace",
        "files": [
            {"name": "sec_backtest_template.py", "action": "new",
             "target": "regulatory/sec_backtest_template.py"},
            {"name": "sec_formal_investigation_notice_20241107.md", "action": "new",
             "target": "regulatory/sec_formal_investigation_notice_20241107.md"},
            {"name": "compliance_remediation_matrix.csv", "action": "new",
             "target": "regulatory/compliance_remediation_matrix.csv"},
        ]
    }

    updates_decl = {
        "upd1_workspace": upd1_workspace,
        "upd2_workspace": upd2_workspace,
        "upd3_workspace": upd3_workspace,
    }
    return updates_decl


# ============================================================
# main
# ============================================================

def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()
    gen_regulatory_docs()
    gen_incident_files()
    gen_code_files()
    gen_reports()
    gen_reference_files()
    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = (
        "Knight Capital (2012) deployment incident & SEC Rule 15c3-5 compliance — "
        "16 exec_check rounds, 3 updates (incl. 1 supersede: price_diff_usd→price_diff_vwap_usd), "
        "5 preference rules P1-P5, difficulty vectors V1/V2/V4/V5/V6/V7/V8/V9/V10. "
        "Real sources: SEC Release No. 34-70694 "
        "(https://www.sec.gov/files/litigation/admin/2013/34-70694.pdf); "
        "SEC press release 2013-222 (https://www.sec.gov/newsroom/press-releases/2013-222); "
        "Doug Seven DevOps analysis (https://dougseven.com/2014/04/17/knightmare-a-devops-cautionary-tale/); "
        "FCA Market Watch 59 (https://www.fca.org.uk/publication/newsletters/market-watch-59.pdf); "
        "SEC Rule 15c6-1 T+1 FAQ (https://www.sec.gov/exams/educationhelpguidesfaqs/t1-faq)."
    )

    dump_register_meta(
        DATASET,
        test_id=TID,
        desc=desc,
        main_session=sess_ids["main"],
        history_sessions=sess_ids["history"],
        updates=updates_decl,
    )

    # 体量报告
    total = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in WS.rglob("*") if p.is_file()
    )
    upd_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in UPD.rglob("*") if p.is_file()
    )
    upd_sizes = {}
    for uname in ["upd1_workspace", "upd2_workspace", "upd3_workspace"]:
        ud = UPD / uname
        if ud.exists():
            toks = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                       for p in ud.rglob("*") if p.is_file())
            upd_sizes[uname] = toks
    print(f"[sec3a] workspace tokens ~{total:,}")
    print(f"[sec3a] update token sizes: {upd_sizes}")
    print(f"[sec3a] updates total ~{upd_tok:,}")
    print(f"[sec3a] built at {DATASET}")


if __name__ == "__main__":
    main()
