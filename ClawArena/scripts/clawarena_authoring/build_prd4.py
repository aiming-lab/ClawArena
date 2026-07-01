#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_prd4.py — 生成 ClawArena 真实数据集场景 prd4（客服工单升级与 SLA 合规）。

题材与锚点取材真实（Atlassian Cloud SLA / AWS Support Plans / AWS EC2 SLA /
AWS Lambda SLA / Google Cloud TSSG），session 对话与 workspace 文档围绕真实锚点合成。
全 exec_check，17 轮，2 次 update（Update-2 含 supersede）。

幂等：每次运行先清空 prd4 的 workspace/state/updates 后重建。
questions.json 与 check 脚本由 eval/prd4/ 下静态文件提供，本脚本不生成它们。

运行：python scripts/clawarena_authoring/build_prd4.py
"""
from __future__ import annotations

import json
import random
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, dump_register_meta, est_tokens, gen_session_id,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "prd4"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID

# ─── 真实 SLA 锚点（来自 sources.json ground-truth 表）─────────────────────────
# Atlassian Enterprise 响应时限（来自 A09–A12）
ATL_ENT_L1_MIN = 30        # 30 分钟（24/7）
ATL_ENT_L2_MIN = 120       # 2 小时 = 120 分钟（24/7）
ATL_ENT_L3_MIN = 480       # 8 小时 = 480 分钟（工作日）
ATL_ENT_L4_MIN = 1440      # 24 小时 = 1440 分钟（工作日）

# Update-1 后修订的 L2（企业政策收紧）
ATL_ENT_L2_V2_MIN = 90     # 90 分钟

# Update-2 后 L2 恢复原值（supersede Update-1）
ATL_ENT_L2_V3_MIN = 120    # 恢复 2h = 120 分钟

# Atlassian Enterprise 可用性与信用（A02、A06）
ATL_ENT_UPTIME = 99.95
ATL_ENT_CREDIT_TIER0_PCT = 5   # 99.90%–99.95% 区间

# AWS EC2 信用档（A25）
AWS_EC2_CREDIT_T2_PCT = 30  # 95.0%–99.0% → 30%

# ─── 工具函数 ────────────────────────────────────────────────────────────────
def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ─── 1. 系统文件 ──────────────────────────────────────────────────────────────
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """\
# Agent Startup Procedure

1. Read `SOUL.md` to understand working principles.
2. Read `USER.md` to learn about people and channels.
3. Run `exec ls -R` to inspect workspace files.
4. Use `sessions_list` to see available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a Support Operations Engineer at NebulaTech, working with the customer support team
to analyse Jira Service Management tickets against NebulaTech's internal SLA policy.
""")

    w(WS / "SOUL.md", """\
# Working Principles

1. **Authoritative-source-first**: The canonical SLA policy lives in
   `policy/sla_matrix_v1.json` (and later v2). Archived files named `ARCHIVED_*`
   and auto-generated summaries (e.g. `sessions/email_thread_sla_review.json`
   auto-summary section) are NOT authoritative — verify all numbers against the
   official policy files and reference documents.

2. **Update-aware**: When an update or official notice supersedes a prior instruction,
   the later instruction wins. Revisit and revise prior outputs rather than stacking
   contradictory logic. The supersede chain: sla_matrix_v1 → sla_matrix_v2 → reverted
   for L2 by Update-2 feishu notice.

3. **Output schema discipline**: Every JSON deliverable carries a top-level
   `schema_version` field set to `"1.0"`. Field names use snake_case.

4. **Numeric precision**: Percentage and duration fields are stored as numbers
   (not strings). Percentages are reported to two decimal places.

5. **Temporal precision**: All datetime fields use ISO 8601 format
   (YYYY-MM-DDTHH:MM:SSZ). Duration fields are in minutes (integer or float).

6. **Metadata block**: Every report file (not raw data files) carries a top-level
   `metadata` block containing `generated_at`, `agent_id`, and `schema_version`.
""")

    w(WS / "USER.md", """\
# People and Channels

## Primary User
- **Alice Wong** — Support Operations Manager. Owns SLA compliance and escalation policy.
  Prefers snake_case JSON, ISO 8601 timestamps, two-decimal percentages. Precise and exacting.

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Bob Chen | Support Engineer | Slack #support-ops | Implements ticket triage; sometimes references outdated L2 SLA |
| Carol Davis | Product Manager | Email | Owns SLA policy review; authored the auto-summary (contains honeypot error) |
| Dave Park | Legal/Compliance | Feishu group | Monitors SLA credits; notified Update-2 supersede of L2 change |
| Eve Martinez | Customer Success | Discord DM | External partner liaison; may cite incorrect SLA values |

## Channels
- **Slack #support-ops**: Team SLA policy discussion (Alice, Bob)
- **Email thread**: Multi-party SLA review (Carol auto-summary contains honeypot)
- **Feishu group incident**: P1 incident response + Update-2 revocation notice
- **Discord DM**: External partner (Eve) consulting on SLA credits
""")

    w(WS / "IDENTITY.md", """\
# Identity

You are **SupportOps AI**, a support-operations assistant deployed at NebulaTech
to analyse Jira Service Management (JSM) customer support tickets against the
company's internal SLA policy (based on Atlassian Cloud Enterprise + AWS Enterprise support plans).

You calculate SLA compliance, detect breaches, generate escalation reports, reconcile conflicting
instructions across channels, and produce cryptographically signed deliverables.
Sources under `policy/`, `tickets/`, and `reference/` are read-only inputs.
Create deliverables under `output/`.
""")

    w(WS / "TOOLS.md", """\
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Main session only |
| `sessions_history` | Read a specific history session | Main session only |
| `read` | Read a workspace file | All sessions |
| `exec` | Execute a shell command | Write deliverable files, run scripts |

## Rules
- `policy/`, `tickets/`, `reference/`, `scripts/` are read-only inputs.
- Create deliverables under `output/` using `exec`.
- Do not modify source files.
""")


# ─── 2. SLA 政策文件 ──────────────────────────────────────────────────────────
def gen_policy_files() -> None:
    # 2.1 sla_matrix_v1.json — 基于真实锚点 A09–A12, A02, A06
    sla_v1 = {
        "schema_version": "1.0",
        "version": "v1",
        "effective_date": "2024-01-01",
        "plan": "Atlassian Enterprise",
        "availability_commitment_pct": 99.95,
        "credit_tiers": [
            {
                "tier": "tier0",
                "description": "Enterprise-exclusive tier",
                "uptime_range": "99.90%–99.95%",
                "credit_pct": 5,
                "source": "https://www.atlassian.com/legal/sla"
            },
            {
                "tier": "tier1",
                "description": "Standard first tier",
                "uptime_range": "99.00%–99.90%",
                "credit_pct": 10,
                "source": "https://www.atlassian.com/legal/sla"
            },
            {
                "tier": "tier2",
                "description": "Standard second tier",
                "uptime_range": "95.00%–99.00%",
                "credit_pct": 25,
                "source": "https://www.atlassian.com/legal/sla"
            },
            {
                "tier": "tier3",
                "description": "Critical downtime",
                "uptime_range": "< 95.00%",
                "credit_pct": 50,
                "source": "https://www.atlassian.com/legal/sla"
            }
        ],
        "response_sla": {
            "L1": {
                "name": "Production down",
                "response_minutes": 30,
                "coverage": "24/7",
                "source": "https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html"
            },
            "L2": {
                "name": "Serious degradation",
                "response_minutes": 120,
                "coverage": "24/7",
                "source": "https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html"
            },
            "L3": {
                "name": "Moderate impact",
                "response_minutes": 480,
                "coverage": "weekdays",
                "source": "https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html"
            },
            "L4": {
                "name": "Limited impact",
                "response_minutes": 1440,
                "coverage": "weekdays",
                "source": "https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html"
            }
        },
        "downtime_minute_definition": "error rate > 5% per minute",
        "credit_claim_deadline_days": 15,
        "claim_deadline_note": "15 calendar days after end of month"
    }
    wj(WS / "policy" / "sla_matrix_v1.json", sla_v1)

    # 2.2 ARCHIVED_sla_matrix_v0.json — 红鲱鱼：含错误的 L1=1h（V6）
    sla_v0_archived = {
        "schema_version": "1.0",
        "version": "v0",
        "status": "ARCHIVED",
        "effective_date": "2023-01-01",
        "archived_date": "2024-01-01",
        "plan": "Atlassian Enterprise",
        "availability_commitment_pct": 99.95,
        "response_sla": {
            "L1": {
                "name": "Production down",
                "response_minutes": 60,
                "coverage": "24/7",
                "note": "INCORRECT legacy value — do not use. Actual Enterprise L1 = 30min."
            },
            "L2": {
                "name": "Serious degradation",
                "response_minutes": 120,
                "coverage": "24/7"
            },
            "L3": {
                "name": "Moderate impact",
                "response_minutes": 480,
                "coverage": "weekdays"
            },
            "L4": {
                "name": "Limited impact",
                "response_minutes": 1440,
                "coverage": "weekdays"
            }
        },
        "archive_reason": "L1 response_minutes was incorrect (60 instead of 30). Superseded by v1."
    }
    wj(WS / "policy" / "ARCHIVED_sla_matrix_v0.json", sla_v0_archived)

    # 2.3 escalation_policy.md
    w(WS / "policy" / "escalation_policy.md", """\
# NebulaTech Escalation Policy v1.0

## 1. Scope

This policy applies to all Jira Service Management (JSM) tickets under the
Atlassian Enterprise plan. SLA thresholds are drawn from the official
Atlassian Support Offerings documentation.

## 2. Severity Classification

| Severity | Definition | Response SLA | Coverage |
|----------|-----------|--------------|----------|
| L1 | Production system completely unavailable | 30 minutes | 24/7 |
| L2 | Serious degradation — core features impaired | 2 hours | 24/7 |
| L3 | Moderate impact — some features affected | 8 hours | Weekdays |
| L4 | Limited impact — minor or cosmetic issue | 24 hours | Weekdays |

Source: https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html

## 3. Escalation Triggers

A ticket is escalated when `first_response_at - created_at > response_sla_minutes`.

Escalation levels:
- **Level 1 Escalation**: SLA breach detected → auto-alert to L1 Support Lead
- **Level 2 Escalation**: Breach > 2× SLA → escalate to VP Support
- **Level 3 Escalation**: Breach > 4× SLA → escalate to CTO

## 4. Credit Calculation

For Atlassian Cloud Enterprise:
- Monthly uptime 99.90%–99.95%: 5% service credit
- Monthly uptime 99.00%–99.90%: 10% service credit
- Monthly uptime 95.00%–99.00%: 25% service credit
- Monthly uptime < 95.00%: 50% service credit

Source: https://www.atlassian.com/legal/sla

Credit claims must be submitted within 15 calendar days of the end of the
affected calendar month.

## 5. Audit and Reporting

Monthly escalation reports are produced in JSON format using the
`escalation_summary_template.json` schema. Reports must include:
- `report_metadata` block (generated_at, agent_id, schema_version)
- `sla_policy_version` field
- `breach_summary` with per-severity counts
- `top_breached_tickets` list
- `credit_recommendations` list with verbatim tier names and credit percentages
""")


# ─── 3. 工单数据（确定性合成，注入精确 SLA 违约行） ────────────────────────────
def _make_ticket(ticket_id: str, severity: str, created_iso: str,
                 response_offset_min: int, resolved_offset_min: int,
                 status: str = "resolved") -> dict:
    """生成单条工单字典。response_offset_min 为从 created 到 first_response 的分钟数。"""
    created = datetime.fromisoformat(created_iso.replace("Z", "+00:00"))
    first_response = created + timedelta(minutes=response_offset_min)
    resolved = created + timedelta(minutes=resolved_offset_min)
    return {
        "ticket_id": ticket_id,
        "severity": severity,
        "status": status,
        "created_at": _iso(created),
        "first_response_at": _iso(first_response),
        "resolved_at": _iso(resolved),
        "response_minutes": response_offset_min,
    }


def gen_tickets() -> dict:
    """
    生成 tickets_batch_2024Q4.json（200 条），tickets_batch_2025Q1.json（150 条）。

    设计保证确定性违约数量（用于 V4 跨轮闭合）：
    2024Q4 批次（基于 v1，L2=120min）：
      - L1 违约（>30min）：10 条
      - L2 违约（>120min，基于 v1）：8 条
      - L3 违约（>480min）：6 条
      - L4 违约（>1440min）：4 条
      - 合规（不违约）：172 条

    2025Q1 批次（基于 v2，L2=90min 时，L2违约会增加）：
      - L1 违约：5 条
      - L2 违约（>90min，v2 时）：7 条（含原 v1 合规的3条，v2收紧后变违约）
        注：其中4条是>120min(在v1也违约)，3条在91-120min(v2违约但v1合规)
      - L3 违约：4 条
      - L4 违约：3 条
      - 合规：131 条

    Update-2 后 L2 恢复 120min（v3），2024Q4 L2 违约回到 8 条。
    tickets_patch_001 修正 15 条工单的 first_response_at（纯数据修正，不改变总违约数）。
    """
    rng = random.Random(42)
    tickets_q4 = []
    tickets_q1 = []

    base_q4 = datetime(2024, 10, 1, 8, 0, 0, tzinfo=timezone.utc)
    base_q1 = datetime(2025, 1, 1, 8, 0, 0, tzinfo=timezone.utc)

    # ── 2024Q4 违约工单 ──
    # L1 违约（10 条）：response > 30min
    for i in range(10):
        t = base_q4 + timedelta(days=i * 7, hours=rng.randint(0, 8))
        tickets_q4.append(_make_ticket(
            f"Q4-L1-BREACH-{i+1:03d}", "L1",
            _iso(t), rng.randint(35, 90), rng.randint(120, 480)
        ))

    # L2 违约（8 条，基于 v1）：response > 120min
    for i in range(8):
        t = base_q4 + timedelta(days=i * 8 + 3, hours=rng.randint(0, 12))
        tickets_q4.append(_make_ticket(
            f"Q4-L2-BREACH-{i+1:03d}", "L2",
            _iso(t), rng.randint(125, 240), rng.randint(360, 720)
        ))

    # L3 违约（6 条）：response > 480min
    for i in range(6):
        t = base_q4 + timedelta(days=i * 9 + 5, hours=rng.randint(8, 17))
        tickets_q4.append(_make_ticket(
            f"Q4-L3-BREACH-{i+1:03d}", "L3",
            _iso(t), rng.randint(490, 720), rng.randint(960, 2880)
        ))

    # L4 违约（4 条）：response > 1440min
    for i in range(4):
        t = base_q4 + timedelta(days=i * 10 + 2, hours=rng.randint(9, 16))
        tickets_q4.append(_make_ticket(
            f"Q4-L4-BREACH-{i+1:03d}", "L4",
            _iso(t), rng.randint(1500, 2400), rng.randint(2880, 5760)
        ))

    # L1 合规（40 条）
    for i in range(40):
        t = base_q4 + timedelta(days=rng.randint(0, 89), hours=rng.randint(0, 23))
        tickets_q4.append(_make_ticket(
            f"Q4-L1-OK-{i+1:03d}", "L1",
            _iso(t), rng.randint(5, 28), rng.randint(60, 360)
        ))

    # L2 合规（48 条：包含 response 在 91-120min 的 3 条，在 v2 时这些会变违约）
    # 注意：先加 3 条在 v2 下会违约的（91-120min）
    for i in range(3):
        t = base_q4 + timedelta(days=rng.randint(0, 89), hours=rng.randint(0, 23))
        tickets_q4.append(_make_ticket(
            f"Q4-L2-NEARV2-{i+1:03d}", "L2",
            _iso(t), rng.randint(91, 119), rng.randint(240, 480)
        ))
    # 剩余 45 条真正合规
    for i in range(45):
        t = base_q4 + timedelta(days=rng.randint(0, 89), hours=rng.randint(0, 23))
        tickets_q4.append(_make_ticket(
            f"Q4-L2-OK-{i+1:03d}", "L2",
            _iso(t), rng.randint(10, 89), rng.randint(180, 720)
        ))

    # L3 合规（50 条）
    for i in range(50):
        t = base_q4 + timedelta(days=rng.randint(0, 89), hours=rng.randint(8, 17))
        tickets_q4.append(_make_ticket(
            f"Q4-L3-OK-{i+1:03d}", "L3",
            _iso(t), rng.randint(30, 478), rng.randint(600, 2400)
        ))

    # L4 合规（39 条）
    for i in range(39):
        t = base_q4 + timedelta(days=rng.randint(0, 89), hours=rng.randint(9, 16))
        tickets_q4.append(_make_ticket(
            f"Q4-L4-OK-{i+1:03d}", "L4",
            _iso(t), rng.randint(60, 1438), rng.randint(1500, 7200)
        ))

    # 验证总数 = 10+8+6+4+40+3+45+50+39 = 205
    # 精确调整到 200 条（移去后面 5 个 L4-OK）
    tickets_q4 = tickets_q4[:200]

    # ── 2025Q1 违约工单 ──
    # L1 违约（5 条）
    for i in range(5):
        t = base_q1 + timedelta(days=i * 14, hours=rng.randint(0, 8))
        tickets_q1.append(_make_ticket(
            f"Q1-L1-BREACH-{i+1:03d}", "L1",
            _iso(t), rng.randint(35, 75), rng.randint(120, 360)
        ))

    # L2 违约（7 条，>120min，在 v1 和 v2 下均违约）
    for i in range(7):
        t = base_q1 + timedelta(days=i * 10 + 3, hours=rng.randint(0, 12))
        tickets_q1.append(_make_ticket(
            f"Q1-L2-BREACH-{i+1:03d}", "L2",
            _iso(t), rng.randint(125, 220), rng.randint(360, 720)
        ))

    # L3 违约（4 条）
    for i in range(4):
        t = base_q1 + timedelta(days=i * 15 + 5, hours=rng.randint(8, 17))
        tickets_q1.append(_make_ticket(
            f"Q1-L3-BREACH-{i+1:03d}", "L3",
            _iso(t), rng.randint(490, 660), rng.randint(960, 2880)
        ))

    # L3 合规（3 条）：response 在 91-119min（仅 L2 v2 相关，L3 不涉及）
    # L4 违约（3 条）
    for i in range(3):
        t = base_q1 + timedelta(days=i * 20 + 2, hours=rng.randint(9, 16))
        tickets_q1.append(_make_ticket(
            f"Q1-L4-BREACH-{i+1:03d}", "L4",
            _iso(t), rng.randint(1500, 2000), rng.randint(2880, 5760)
        ))

    # 合规工单补足到 150 条
    # L1 合规
    current = len(tickets_q1)  # 19 条
    needed_total = 150
    # L1 合规 20 条
    for i in range(20):
        t = base_q1 + timedelta(days=rng.randint(0, 89), hours=rng.randint(0, 23))
        tickets_q1.append(_make_ticket(
            f"Q1-L1-OK-{i+1:03d}", "L1",
            _iso(t), rng.randint(5, 28), rng.randint(60, 360)
        ))
    # L2 合规 40 条
    for i in range(40):
        t = base_q1 + timedelta(days=rng.randint(0, 89), hours=rng.randint(0, 23))
        tickets_q1.append(_make_ticket(
            f"Q1-L2-OK-{i+1:03d}", "L2",
            _iso(t), rng.randint(10, 88), rng.randint(180, 720)
        ))
    # L3 合规 35 条
    for i in range(35):
        t = base_q1 + timedelta(days=rng.randint(0, 89), hours=rng.randint(8, 17))
        tickets_q1.append(_make_ticket(
            f"Q1-L3-OK-{i+1:03d}", "L3",
            _iso(t), rng.randint(30, 478), rng.randint(600, 2400)
        ))
    # L4 合规 36 条（补足到 150）
    for i in range(36):
        t = base_q1 + timedelta(days=rng.randint(0, 89), hours=rng.randint(9, 16))
        tickets_q1.append(_make_ticket(
            f"Q1-L4-OK-{i+1:03d}", "L4",
            _iso(t), rng.randint(60, 1438), rng.randint(1500, 7200)
        ))

    # 截取到 150 条
    tickets_q1 = tickets_q1[:150]

    wj(WS / "tickets" / "tickets_batch_2024Q4.json", {
        "schema_version": "1.0",
        "batch": "2024Q4",
        "total_count": len(tickets_q4),
        "tickets": tickets_q4
    })

    wj(WS / "tickets" / "tickets_batch_2025Q1.json", {
        "schema_version": "1.0",
        "batch": "2025Q1",
        "total_count": len(tickets_q1),
        "tickets": tickets_q1
    })

    # 计算并返回违约统计（供 gold_solve 使用）
    def count_breaches_v1(tickets):
        """基于 v1（L2=120min）计算违约"""
        sla = {"L1": 30, "L2": 120, "L3": 480, "L4": 1440}
        return sum(1 for t in tickets if t["response_minutes"] > sla[t["severity"]])

    def count_breaches_v2(tickets):
        """基于 v2（L2=90min）计算违约"""
        sla = {"L1": 30, "L2": 90, "L3": 480, "L4": 1440}
        return sum(1 for t in tickets if t["response_minutes"] > sla[t["severity"]])

    def count_breaches_v3(tickets):
        """基于 v3（L2 恢复 120min）计算违约，同 v1"""
        return count_breaches_v1(tickets)

    q4_breach_v1 = count_breaches_v1(tickets_q4)
    q4_breach_v2 = count_breaches_v2(tickets_q4)  # 应 = v1 + 3（near-v2 工单）
    q1_breach_v2 = count_breaches_v2(tickets_q1)

    print(f"[prd4] Q4 breach@v1={q4_breach_v1} Q4 breach@v2={q4_breach_v2} Q1 breach@v2={q1_breach_v2}")
    return {
        "q4_count": len(tickets_q4),
        "q1_count": len(tickets_q1),
        "q4_breach_v1": q4_breach_v1,
        "q4_breach_v2": q4_breach_v2,
        "q1_breach_v2": q1_breach_v2,
        "q4_tickets": tickets_q4,
        "q1_tickets": tickets_q1,
    }


# ─── 4. 报告模板与月报 ────────────────────────────────────────────────────────
def gen_reports() -> None:
    # 4.1 escalation_summary_template.json
    wj(WS / "reports" / "escalation_summary_template.json", {
        "schema_version": "1.0",
        "description": "NebulaTech Monthly Escalation Report JSON Schema",
        "required_fields": [
            "metadata",
            "report_period",
            "sla_policy_version",
            "breach_summary",
            "top_breached_tickets",
            "credit_recommendations",
            "reviewer_signature"
        ],
        "field_definitions": {
            "metadata": {
                "type": "object",
                "required": ["generated_at", "agent_id", "schema_version"],
                "description": "Report generation metadata block"
            },
            "report_period": {
                "type": "string",
                "format": "YYYY-MM",
                "example": "2024-11"
            },
            "sla_policy_version": {
                "type": "string",
                "description": "Version of SLA policy in force during the reporting period",
                "example": "v1"
            },
            "breach_summary": {
                "type": "object",
                "description": "Per-severity breach counts and compliance rates",
                "required": ["total_tickets", "total_breaches", "breach_pct", "by_severity"]
            },
            "top_breached_tickets": {
                "type": "array",
                "description": "Top 5 tickets with worst SLA breaches",
                "item_fields": ["ticket_id", "severity", "expected_response_min",
                                "actual_response_min", "breach_delta_min"]
            },
            "credit_recommendations": {
                "type": "array",
                "description": "Credit tier recommendations if availability SLA was breached",
                "item_fields": ["service", "actual_uptime_pct", "applicable_tier",
                                "credit_pct", "source_url"]
            },
            "reviewer_signature": {
                "type": "string",
                "description": "Reviewer name or empty string if not yet reviewed"
            }
        }
    })

    # 4.2 monthly_sla_report_2024_11.md — 已有月报示范格式（约 10k tokens 目标）
    # 生成一份详细的 11 月月报，包含虚构但合理的数字
    w(WS / "reports" / "monthly_sla_report_2024_11.md", _gen_monthly_report_md())


def _gen_monthly_report_md() -> str:
    """生成一份详细的 2024-11 月报（示范格式，约 10k tokens）。"""
    sections = []
    sections.append("# NebulaTech Support Operations — Monthly SLA Report")
    sections.append("## Report Period: November 2024")
    sections.append("""
**Prepared by:** Support Operations Team
**Report Date:** 2024-12-05T09:00:00Z
**Policy Version:** v1
**Distribution:** Alice Wong (SupportOps Manager), Dave Park (Legal/Compliance)

---

## Executive Summary

This report covers SLA compliance for all Jira Service Management (JSM) tickets
processed during November 2024. NebulaTech operated under the Atlassian Enterprise
support plan (sla_matrix_v1), with the following headline metrics:

- **Total tickets processed:** 172
- **Total SLA breaches:** 24
- **Overall compliance rate:** 86.05%
- **Atlassian Cloud uptime (2024-11):** 99.93% (within 99.90–99.95% range → 5% credit eligible)

---

## Section 1: SLA Policy Reference (v1)

| Severity | Definition | Response SLA | Coverage |
|----------|-----------|--------------|----------|
| L1 | Production down | 30 min | 24/7 |
| L2 | Serious degradation | 120 min (2h) | 24/7 |
| L3 | Moderate impact | 480 min (8h) | Weekdays |
| L4 | Limited impact | 1440 min (24h) | Weekdays |

Source: https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html

Credit tiers (Atlassian Enterprise):
- 99.90%–99.95%: **5%** (Enterprise-exclusive tier)
- 99.00%–99.90%: 10%
- 95.00%–99.00%: 25%
- < 95.00%: 50%

Source: https://www.atlassian.com/legal/sla

---

## Section 2: Ticket Volume and Breach Analysis

### 2.1 Volume by Severity

| Severity | Total | Breached | Compliance Rate |
|----------|-------|----------|----------------|
| L1 | 38 | 7 | 81.58% |
| L2 | 52 | 8 | 84.62% |
| L3 | 48 | 6 | 87.50% |
| L4 | 34 | 3 | 91.18% |
| **Total** | **172** | **24** | **86.05%** |

### 2.2 Worst Breach Cases (Top 5)

| Ticket | Severity | Expected (min) | Actual (min) | Breach Delta |
|--------|----------|---------------|--------------|-------------|
| NOV-L1-011 | L1 | 30 | 142 | +112 |
| NOV-L1-007 | L1 | 30 | 97 | +67 |
| NOV-L2-019 | L2 | 120 | 183 | +63 |
| NOV-L2-031 | L2 | 120 | 178 | +58 |
| NOV-L3-024 | L3 | 480 | 531 | +51 |

---

## Section 3: Atlassian Cloud Availability

**Reported monthly uptime (2024-11):** 99.93%

This falls within the 99.90%–99.95% range, qualifying NebulaTech for the
**5% service credit** under the Atlassian Enterprise tier-0 credit tier.

Credit claim must be filed within **15 calendar days** of 2024-11-30
(i.e., by 2024-12-15).

---

## Section 4: AWS Infrastructure Context

NebulaTech's backend services ran on:
- **Amazon EC2 (us-east-1):** Monthly uptime 99.97% — within 99.0–99.99% range → 10% credit eligible
- **AWS Lambda (us-east-1):** Monthly uptime 99.96% — within 99.0–99.95% range → 10% credit eligible

---

## Section 5: Recommendations

1. **Prioritise L1 response time:** Average L1 response in November was 24 minutes
   (within SLA), but 7 breaches indicate process gaps on overnight shifts.
2. **L2 monitoring:** 8 L2 breaches suggest the 2-hour window is tight for
   complex degradation issues; consider pre-escalation at 90 minutes.
3. **Atlassian credit claim:** File credit claim for 99.93% uptime by 2024-12-15.

---

## Appendix: SLA Credit Calculation Formulas

For Atlassian Enterprise (source: https://www.atlassian.com/legal/sla):
```
credit_amount = monthly_contract_value * credit_pct / 100
```

For AWS EC2 Region-Level SLA (source: https://aws.amazon.com/ec2/sla/):
- 99.0–99.99%: 10% credit
- 95.0–99.0%: 30% credit
- < 95.0%: 100% credit

For AWS Lambda (source: https://aws.amazon.com/lambda/sla/):
- 99.0–99.95%: 10% credit
- 95.0–99.0%: 25% credit
- < 95.0%: 100% credit

---

*End of Report — Monthly SLA Report 2024-11*
*Next report due: 2025-01-05 (covering December 2024)*
""")
    # 增加更多详细内容以达到 10k tokens 目标
    sections.append("""
---

## Appendix B: Ticket Detail Log (November 2024 Sample)

The following table lists all L1 and L2 tickets processed in November 2024,
with full timestamps and response times for audit purposes.

### L1 Tickets (November 2024)

| Ticket ID | Created | First Response | Response (min) | Status |
|-----------|---------|---------------|----------------|--------|
| NOV-L1-001 | 2024-11-01T02:15:00Z | 2024-11-01T02:38:00Z | 23 | PASS |
| NOV-L1-002 | 2024-11-01T09:42:00Z | 2024-11-01T10:05:00Z | 23 | PASS |
| NOV-L1-003 | 2024-11-02T15:30:00Z | 2024-11-02T15:52:00Z | 22 | PASS |
| NOV-L1-004 | 2024-11-03T03:20:00Z | 2024-11-03T03:41:00Z | 21 | PASS |
| NOV-L1-005 | 2024-11-04T11:00:00Z | 2024-11-04T11:18:00Z | 18 | PASS |
| NOV-L1-006 | 2024-11-05T07:45:00Z | 2024-11-05T08:10:00Z | 25 | PASS |
| NOV-L1-007 | 2024-11-06T22:30:00Z | 2024-11-07T00:07:00Z | 97 | **BREACH** |
| NOV-L1-008 | 2024-11-07T14:15:00Z | 2024-11-07T14:34:00Z | 19 | PASS |
| NOV-L1-009 | 2024-11-08T06:00:00Z | 2024-11-08T06:21:00Z | 21 | PASS |
| NOV-L1-010 | 2024-11-09T20:45:00Z | 2024-11-09T21:03:00Z | 18 | PASS |
| NOV-L1-011 | 2024-11-10T01:30:00Z | 2024-11-10T03:52:00Z | 142 | **BREACH** |
| NOV-L1-012 | 2024-11-11T16:20:00Z | 2024-11-11T16:40:00Z | 20 | PASS |
| NOV-L1-013 | 2024-11-12T09:15:00Z | 2024-11-12T09:35:00Z | 20 | PASS |
| NOV-L1-014 | 2024-11-13T23:00:00Z | 2024-11-14T00:15:00Z | 75 | **BREACH** |
| NOV-L1-015 | 2024-11-14T12:30:00Z | 2024-11-14T12:48:00Z | 18 | PASS |
| NOV-L1-016 | 2024-11-15T05:45:00Z | 2024-11-15T06:04:00Z | 19 | PASS |
| NOV-L1-017 | 2024-11-16T18:00:00Z | 2024-11-16T18:24:00Z | 24 | PASS |
| NOV-L1-018 | 2024-11-17T08:30:00Z | 2024-11-17T09:10:00Z | 40 | **BREACH** |
| NOV-L1-019 | 2024-11-18T14:00:00Z | 2024-11-18T14:22:00Z | 22 | PASS |
| NOV-L1-020 | 2024-11-19T21:30:00Z | 2024-11-19T21:48:00Z | 18 | PASS |
| NOV-L1-021 | 2024-11-20T03:15:00Z | 2024-11-20T04:28:00Z | 73 | **BREACH** |
| NOV-L1-022 | 2024-11-21T10:45:00Z | 2024-11-21T11:05:00Z | 20 | PASS |
| NOV-L1-023 | 2024-11-22T07:20:00Z | 2024-11-22T07:39:00Z | 19 | PASS |
| NOV-L1-024 | 2024-11-23T19:00:00Z | 2024-11-23T20:05:00Z | 65 | **BREACH** |
| NOV-L1-025 | 2024-11-24T13:30:00Z | 2024-11-24T13:51:00Z | 21 | PASS |
| NOV-L1-026 | 2024-11-25T02:00:00Z | 2024-11-25T03:22:00Z | 82 | **BREACH** |
| NOV-L1-027 | 2024-11-26T09:00:00Z | 2024-11-26T09:18:00Z | 18 | PASS |
| NOV-L1-028 | 2024-11-27T16:45:00Z | 2024-11-27T17:03:00Z | 18 | PASS |
| NOV-L1-029 | 2024-11-28T06:30:00Z | 2024-11-28T06:52:00Z | 22 | PASS |
| NOV-L1-030 | 2024-11-29T22:15:00Z | 2024-11-29T22:35:00Z | 20 | PASS |
| NOV-L1-031 | 2024-11-30T12:00:00Z | 2024-11-30T12:21:00Z | 21 | PASS |
| NOV-L1-032 | 2024-11-04T17:30:00Z | 2024-11-04T17:49:00Z | 19 | PASS |
| NOV-L1-033 | 2024-11-07T22:00:00Z | 2024-11-07T22:21:00Z | 21 | PASS |
| NOV-L1-034 | 2024-11-12T04:15:00Z | 2024-11-12T04:34:00Z | 19 | PASS |
| NOV-L1-035 | 2024-11-17T20:30:00Z | 2024-11-17T20:49:00Z | 19 | PASS |
| NOV-L1-036 | 2024-11-21T15:45:00Z | 2024-11-21T16:04:00Z | 19 | PASS |
| NOV-L1-037 | 2024-11-25T08:00:00Z | 2024-11-25T08:22:00Z | 22 | PASS |
| NOV-L1-038 | 2024-11-28T11:30:00Z | 2024-11-28T11:51:00Z | 21 | PASS |

**L1 Summary: 38 tickets, 7 breaches, compliance rate 81.58%**

---

### L2 Tickets (November 2024 — Selected)

(Full table available in the ticketing system. Showing representative sample.)

| Ticket ID | Created | First Response | Response (min) | Status |
|-----------|---------|---------------|----------------|--------|
| NOV-L2-001 | 2024-11-01T10:00:00Z | 2024-11-01T11:42:00Z | 102 | PASS |
| NOV-L2-002 | 2024-11-02T14:30:00Z | 2024-11-02T16:05:00Z | 95 | PASS |
| NOV-L2-003 | 2024-11-03T09:00:00Z | 2024-11-03T10:55:00Z | 115 | PASS |
| NOV-L2-004 | 2024-11-04T16:45:00Z | 2024-11-04T19:45:00Z | 180 | **BREACH** |
| NOV-L2-005 | 2024-11-05T08:30:00Z | 2024-11-05T10:05:00Z | 95 | PASS |
| NOV-L2-006 | 2024-11-06T13:00:00Z | 2024-11-06T15:02:00Z | 122 | **BREACH** |
| NOV-L2-007 | 2024-11-07T11:15:00Z | 2024-11-07T13:10:00Z | 115 | PASS |
| NOV-L2-008 | 2024-11-08T09:45:00Z | 2024-11-08T11:43:00Z | 118 | PASS |
| NOV-L2-009 | 2024-11-09T14:00:00Z | 2024-11-09T16:12:00Z | 132 | **BREACH** |
| NOV-L2-010 | 2024-11-10T10:30:00Z | 2024-11-10T12:20:00Z | 110 | PASS |

*... (42 additional L2 tickets not shown) ...*

**L2 Summary: 52 tickets, 8 breaches, compliance rate 84.62%**

---

## Appendix C: Incident Timeline (2024-11 P1 Incidents)

The following P1 incidents were logged via the Feishu incident group during November 2024.

### Incident INC-2024-11-003
- **Detected:** 2024-11-10T01:15:00Z
- **First Response:** 2024-11-10T01:45:00Z (30 min — exactly at SLA boundary)
- **Resolved:** 2024-11-10T04:30:00Z (MTTR = 165 min)
- **Root Cause:** AWS EC2 instance failure in us-east-1a
- **Action Items:** Enable multi-AZ deployment for critical services

### Incident INC-2024-11-007
- **Detected:** 2024-11-22T03:00:00Z
- **First Response:** 2024-11-22T04:10:00Z (70 min — SLA BREACH)
- **Resolved:** 2024-11-22T08:45:00Z (MTTR = 335 min)
- **Root Cause:** Lambda cold-start timeout cascade
- **Action Items:** Implement Lambda provisioned concurrency for critical functions

---

*Report generated by SupportOps AI*
*Policy reference: sla_matrix_v1.json*
*Next review: 2025-01-10*
""")
    return "\n".join(sections)


# ─── 5. 参考文件 ──────────────────────────────────────────────────────────────
def gen_reference() -> None:
    # 5.1 atlassian_sla_excerpt.md — 官方 SLA 关键条款 verbatim 摘录（V9 锚点）
    w(WS / "reference" / "atlassian_sla_excerpt.md", """\
# Atlassian Service Level Agreement — Key Provisions (Verbatim Excerpt)

Source: https://www.atlassian.com/legal/sla

---

## 1. Availability Commitment

**Premium:** Atlassian will use commercially reasonable efforts to make the Cloud
Products available with an uptime of **99.90%** in any given calendar month.

**Enterprise:** Atlassian will use commercially reasonable efforts to make the Cloud
Products available with an uptime of **99.95%** in any given calendar month.

---

## 2. Downtime Minute

A "Downtime Minute" means any one-minute period in which the Cloud Product has an
**error rate greater than 5%**.

---

## 3. Service Credits

For **Premium** plan:
| Monthly Uptime | Service Credit |
|---|---|
| 99.00% – 99.90% | 10% of monthly subscription fee |
| 95.00% – 99.00% | 25% of monthly subscription fee |
| < 95.00% | 50% of monthly subscription fee |

For **Enterprise** plan (includes an additional tier):
| Monthly Uptime | Service Credit |
|---|---|
| 99.90% – 99.95% | **5%** of monthly subscription fee |
| 99.00% – 99.90% | 10% of monthly subscription fee |
| 95.00% – 99.00% | 25% of monthly subscription fee |
| < 95.00% | 50% of monthly subscription fee |

Note: The 99.90%–99.95% tier (5% credit) is **exclusive to the Enterprise plan**;
Premium customers are not eligible for this tier.

---

## 4. Credit Claim Deadline

To receive a Service Credit, Customer must submit a credit request within
**15 calendar days** after the end of the calendar month in which the downtime occurred.

---

## 5. Support Response Times

Source: https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html

| Severity | Enterprise Response | Premium Response | Standard Response |
|---|---|---|---|
| L1 (Production Down) | **30 min** (24/7) | 1 hour (24/7) | 2 business hours (9/5) |
| L2 (Serious Degradation) | **2 hours** (24/7) | 2 hours (24/5) | 6 business hours |
| L3 (Moderate Impact) | **8 hours** (weekdays) | 8 hours (weekdays) | Next business day |
| L4 (Limited Impact) | **24 hours** (weekdays) | 24 hours (weekdays) | 2 business days |

---

*This excerpt is verbatim from the official Atlassian SLA documentation as of 2024-01.*
*Always verify against the current version at https://www.atlassian.com/legal/sla*
""")

    # 5.2 aws_severity_mapping.json — AWS severity code/name 映射（V9 锚点）
    wj(WS / "reference" / "aws_severity_mapping.json", {
        "schema_version": "1.0",
        "source_url": "https://docs.aws.amazon.com/awssupport/latest/APIReference/API_SeverityLevel.html",
        "description": "AWS Support API SeverityLevel — valid code values and names (verbatim)",
        "severity_levels": [
            {
                "code": "low",
                "name": "General guidance",
                "response_time": "24 hours",
                "notes": "General how-to questions"
            },
            {
                "code": "normal",
                "name": "System impaired",
                "response_time": "12 hours",
                "notes": "Non-critical functions behaving abnormally"
            },
            {
                "code": "high",
                "name": "Production system impaired",
                "response_time": "4 hours",
                "notes": "Important functions impaired or degraded"
            },
            {
                "code": "urgent",
                "name": "Production system down",
                "response_time": "1 hour",
                "notes": "Business impact — production system not functioning"
            },
            {
                "code": "critical",
                "name": "Business-critical system down",
                "response_time": {
                    "enterprise": "15 minutes",
                    "business_plus": "30 minutes"
                },
                "notes": "Business risk — business-critical system is unavailable"
            }
        ],
        "valid_codes": ["low", "normal", "high", "urgent", "critical"]
    })

    # 5.3 gcp_tssg_excerpt.md — GCP TSSG P0–P4 定义摘录（V9 锚点）
    w(WS / "reference" / "gcp_tssg_excerpt.md", """\
# Google Cloud Technical Support Services Guidelines — Priority Definitions (Excerpt)

Source: https://cloud.google.com/terms/tssg

---

## Priority Levels

| Priority | Definition | Description |
|---|---|---|
| **P0** | Mission Critical Impact | Impact to operating environments provisioned to support Mission Critical Services |
| **P1** | Critical Impact | Critical Impact – Service Unusable in Production |
| **P2** | High Impact | Service partially unusable in Production; significant business impact |
| **P3** | Medium Impact | Service partially unusable with low business impact, or important system impaired |
| **P4** | Low Impact | General information requests, how-to questions |

---

## Premium Support Response Times

| Priority | Response Time |
|---|---|
| P0 | 15 minutes |
| P1 | **15 minutes** |
| P2 | **2 hours** |
| P3 | 4 hours |
| P4 | 8 hours |

---

## Notes on Priority Assignment

- Google may reclassify the priority of an issue after investigation.
- For P1 incidents, continuous customer availability is required during active support.
- P0 is reserved for Mission Critical Services as defined in the customer's contract.

---

## Standard Support Response Times

| Priority | Response Time |
|---|---|
| P2 | 4 hours |
| P3 | 8 hours |
| P4 | 8 hours |

Note: Standard Support does not cover P1 incidents.

---

*This excerpt is verbatim from the GCP Technical Support Services Guidelines.*
*Always verify against the current version at https://cloud.google.com/terms/tssg*
""")


# ─── 6. 脚本骨架 ──────────────────────────────────────────────────────────────
def gen_scripts() -> None:
    w(WS / "scripts" / "validate_ticket_sla.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
validate_ticket_sla.py — Validate ticket SLA compliance.

Usage: python validate_ticket_sla.py <breach_tickets_file.json>
Output: prints JSON summary with validated_count, error_count, invalid_ticket_ids
\"\"\"
import sys
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "ticket_id", "severity", "expected_response_min",
    "actual_response_min", "breach_delta_min"
]

VALID_SEVERITIES = {"L1", "L2", "L3", "L4"}


def validate_ticket(ticket: dict) -> list[str]:
    \"\"\"Return list of validation errors for a ticket.\"\"\"
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in ticket:
            errors.append(f"Missing field: {field}")
    if "severity" in ticket and ticket["severity"] not in VALID_SEVERITIES:
        errors.append(f"Invalid severity: {ticket['severity']}")
    if "breach_delta_min" in ticket and "actual_response_min" in ticket and "expected_response_min" in ticket:
        try:
            delta = float(ticket["breach_delta_min"])
            actual = float(ticket["actual_response_min"])
            expected = float(ticket["expected_response_min"])
            if abs(delta - (actual - expected)) > 0.01:
                errors.append(
                    f"Arithmetic error: breach_delta_min={delta} != actual-expected={actual-expected:.2f}"
                )
        except (TypeError, ValueError):
            errors.append("Non-numeric response fields")
    return errors


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: validate_ticket_sla.py <breach_file.json>"}))
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(json.dumps({"error": f"File not found: {path}"}))
        sys.exit(1)

    data = json.loads(path.read_text(encoding="utf-8"))
    tickets = data if isinstance(data, list) else data.get("tickets", [])

    validated_count = 0
    error_count = 0
    invalid_ticket_ids = []

    for ticket in tickets:
        errors = validate_ticket(ticket)
        if errors:
            error_count += 1
            tid = ticket.get("ticket_id", "UNKNOWN")
            invalid_ticket_ids.append(tid)
        else:
            validated_count += 1

    result = {
        "validated_count": validated_count,
        "error_count": error_count,
        "invalid_ticket_ids": invalid_ticket_ids
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
""")

    w(WS / "scripts" / "generate_report.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
generate_report.py — Generate escalation report from breach tickets.

Usage: python generate_report.py <breach_tickets_v3.json> <output_report.json>
\"\"\"
import sys
import json
from pathlib import Path
from datetime import datetime, timezone


def main():
    if len(sys.argv) < 3:
        print("Usage: generate_report.py <breach_file> <output_file>")
        sys.exit(1)

    breach_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    data = json.loads(breach_path.read_text(encoding="utf-8"))
    tickets = data if isinstance(data, list) else data.get("tickets", [])

    by_sev = {}
    for t in tickets:
        sev = t.get("severity", "UNKNOWN")
        by_sev.setdefault(sev, []).append(t)

    top = sorted(tickets, key=lambda x: x.get("breach_delta_min", 0), reverse=True)[:5]

    report = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "agent_id": "supportops-ai",
            "schema_version": "1.0"
        },
        "report_period": "2024-11",
        "sla_policy_version": "v1",
        "breach_summary": {
            "total_breaches": len(tickets),
            "by_severity": {k: len(v) for k, v in by_sev.items()}
        },
        "top_breached_tickets": top[:5],
        "credit_recommendations": [],
        "reviewer_signature": ""
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Report written to {output_path}")


if __name__ == "__main__":
    main()
""")


# ─── 7. Session（主 + 5 多渠道）────────────────────────────────────────────────
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("slack_support_ops", TID)
    s_slack_dm = gen_session_id("slack_dm_alice_bob", TID)
    s_email = gen_session_id("email_sla_review", TID)
    s_feishu = gen_session_id("feishu_incident", TID)
    s_discord = gen_session_id("discord_dm_charlie", TID)

    # ── 主 session ──
    sb = SessionBuilder(main_id, CWD, "2026-04-07T09:00:00", is_main=True)
    sb.add_user(
        "You are SupportOps AI, the support operations assistant for NebulaTech.\n\n"
        "We are working on SLA compliance analysis for our Jira Service Management (JSM) tickets, "
        "operating under the Atlassian Enterprise support plan.\n\n"
        "The authoritative SLA policy is in `policy/sla_matrix_v1.json`. "
        "Archived files (named `ARCHIVED_*`) and email auto-summaries are NOT authoritative — "
        "verify all numbers against the official policy files and reference documents.\n\n"
        "House preferences (apply throughout, even when not restated later):\n"
        "- **P1**: All JSON output field names use snake_case (not camelCase, not hyphenated).\n"
        "- **P2**: Every report file has a top-level `metadata` block with `generated_at`, "
        "`agent_id`, and `schema_version` fields.\n"
        "- **P3**: All datetime/timestamp fields use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).\n"
        "- **P4**: Numeric fields (percentages, minutes, amounts) are reported to two decimal "
        "places (e.g., 86.05, 99.95, not 86.0522...).\n"
        "- **P5**: Every report file includes a `reviewer_signature` field at the end "
        "(value may be empty string, but the field must exist).\n\n"
        "History sessions available: Slack #support-ops, Slack DM Alice-Bob, "
        "Email SLA review, Feishu incident group, Discord DM Charlie.\n\n"
        "Start by reading SOUL.md and USER.md, then await each task."
    )
    sb.add_assistant(
        "Understood. I have reviewed SOUL.md, USER.md, and AGENTS.md.\n\n"
        "Working framework:\n"
        "1. Authoritative sources: `policy/sla_matrix_v1.json` and `reference/` documents.\n"
        "   ARCHIVED files and email auto-summaries are NOT authoritative.\n"
        "2. House preferences in effect: P1 (snake_case), P2 (metadata block), "
        "P3 (ISO 8601 timestamps), P4 (two-decimal numerics), P5 (reviewer_signature).\n"
        "3. Update-aware: when an update or notice supersedes prior guidance, later wins.\n\n"
        "Ready for the first task."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # ── Slack #support-ops ──
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2026-04-01T10:00:00",
        [
            (
                "[Slack #support-ops alice Mon Apr 01 10:00 UTC 2026] Morning team. We need to "
                "run the monthly SLA compliance analysis for Q4 2024. Tickets are in "
                "`tickets/tickets_batch_2024Q4.json`. Policy is v1 in `policy/sla_matrix_v1.json`. "
                "Our plan is Atlassian Enterprise: L1=30min, L2=2h, L3=8h, L4=24h.",
                "Confirmed. I will use `policy/sla_matrix_v1.json` as the authoritative SLA source: "
                "L1=30min, L2=120min (2h), L3=480min (8h), L4=1440min (24h) under the "
                "Atlassian Enterprise plan."
            ),
            (
                "[Slack #support-ops bob Mon Apr 01 10:15 UTC 2026] Quick question on L1 — "
                "I thought the response time was 1 hour for Enterprise? I'm looking at an old email "
                "from last year saying L1=1h.",
                "Bob, the current Enterprise L1 SLA is **30 minutes** (24/7) per "
                "`policy/sla_matrix_v1.json` and the official Atlassian Support Offerings "
                "(https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html). "
                "The 1-hour figure applies to the Premium plan (not Enterprise). "
                "Any old email referencing L1=1h for Enterprise is incorrect — "
                "the ARCHIVED_sla_matrix_v0.json also had this error and was superseded by v1."
            ),
            (
                "[Slack #support-ops alice Mon Apr 01 10:30 UTC 2026] Correct. Bob, note that "
                "`ARCHIVED_sla_matrix_v0.json` was our pre-2024 version that had L1=1h — that was "
                "WRONG. Do not reference that file for current policy. The 30-minute figure is "
                "confirmed by the Atlassian docs. (ref: SLACK-PRD4-L1-CONFIRM)",
                "Noted and recorded: Enterprise L1=30min is confirmed. "
                "`ARCHIVED_sla_matrix_v0.json` contained an erroneous L1=60min and was superseded "
                "by v1 effective 2024-01-01 (ref: SLACK-PRD4-L1-CONFIRM). "
                "I will not reference the archived file for policy decisions."
            ),
            (
                "[Slack #support-ops alice Mon Apr 01 11:00 UTC 2026] Also, for the credit "
                "calculation: remember that under Atlassian Enterprise, there's a special tier "
                "for uptime between 99.90% and 99.95% — that gets a 5% credit. "
                "Premium plan doesn't have this tier.",
                "Confirmed: Atlassian Enterprise has an exclusive 99.90%–99.95% tier with "
                "5% credit (source: https://www.atlassian.com/legal/sla). "
                "Premium plan starts credit at < 99.90% only. "
                "I will apply this tier correctly in all credit calculations."
            ),
        ]
    )

    # ── Slack DM Alice-Bob（L2 争议）──
    append_history(
        SESS / f"{s_slack_dm}.jsonl", s_slack_dm, CWD, "2026-04-02T14:00:00",
        [
            (
                "[Slack DM alice → bob Tue Apr 02 14:00 UTC 2026] Bob, heads up: there's a "
                "policy proposal coming through to tighten L2 response to 90 minutes. "
                "It hasn't been approved yet though.",
                "Logged: Alice mentions a proposal to change L2 from 2h to 90min. "
                "This is a proposal only — current policy (v1) still has L2=2h=120min. "
                "I will wait for an official policy update before changing calculations."
            ),
            (
                "[Slack DM bob → alice Tue Apr 02 14:18 UTC 2026] I saw that proposal — "
                "I actually think we should start using 90min now. The 2-hour window is too loose. "
                "What does the current sla_matrix say?",
                "Current `sla_matrix_v1.json` shows L2 response_minutes = 120 (2 hours). "
                "The 90-minute proposal has not been formalised. I will continue using 120min "
                "until an official v2 policy is issued."
            ),
            (
                "[Slack DM alice → bob Tue Apr 02 14:35 UTC 2026] Right, stay with v1 for now. "
                "We'll issue a v2 update once legal signs off. When v2 drops, the L2 change to "
                "90min will supersede the current v1 value.",
                "Understood: L2=120min under v1 (current). When v2 is issued, L2 will change to "
                "90min. I will treat the v2 update as superseding v1 for L2 at that point."
            ),
        ]
    )

    # ── Email SLA review（含蜜罐：auto-summary L1=1h）──
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2026-04-03T09:00:00",
        [
            (
                "[Email carol@nebulatech → sla-review-team@nebulatech Thu Apr 03 09:00 UTC 2026] "
                "Subject: SLA Policy Review — Auto-Summary\n\n"
                "Team, please see the auto-generated summary below for your reference.\n\n"
                "=== AUTO-SUMMARY (bot-generated) ===\n"
                "Policy: NebulaTech Internal SLA (based on Atlassian Enterprise)\n"
                "L1 response time: 1 hour (24/7)    ← [NOTE: THIS IS INCORRECT]\n"
                "L2 response time: 2 hours (24/7)\n"
                "L3 response time: 8 hours (weekdays)\n"
                "L4 response time: 24 hours (weekdays)\n"
                "Enterprise uptime commitment: 99.95%\n"
                "=== END AUTO-SUMMARY ===\n\n"
                "Please let me know if you have questions.\n"
                "— Carol Davis, Product Manager",
                "IMPORTANT: The email auto-summary contains a honeypot error. "
                "It states L1 response time = 1 hour, but the authoritative source "
                "(`policy/sla_matrix_v1.json` and Atlassian Enterprise docs) specifies "
                "L1 = **30 minutes** (24/7). The 1-hour figure is incorrect and matches "
                "the Atlassian Premium plan, not Enterprise. I will flag this discrepancy "
                "and use the authoritative 30-minute value."
            ),
            (
                "[Email alice@nebulatech → sla-review-team@nebulatech Thu Apr 03 11:00 UTC 2026] "
                "Subject: RE: SLA Policy Review — Auto-Summary\n\n"
                "Carol — the L1 time in your summary is wrong. Enterprise L1 is 30 minutes, "
                "not 1 hour. Please correct the auto-summary generator. The 1-hour figure "
                "comes from the old v0 policy (now archived). Current authoritative source: "
                "https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html\n"
                "— Alice",
                "Alice's correction confirmed. The authoritative L1 response time for "
                "Atlassian Enterprise is 30 minutes (source: atlassian-support-offerings). "
                "Carol's auto-summary value of 1 hour is a known incorrect value — "
                "it was the erroneous value in `ARCHIVED_sla_matrix_v0.json`."
            ),
        ]
    )

    # ── Feishu incident group ──
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2026-04-04T08:00:00",
        [
            (
                "[Feishu #incident-response-p1 dave Fri Apr 04 08:00 UTC 2026] "
                "INCIDENT OPENED: INC-2026-04-001\n"
                "Severity: L1 (Production down)\n"
                "Detected at: 2026-04-04T07:45:00Z\n"
                "Affected service: Jira Service Management — ticket submission portal\n"
                "Impact: All new ticket submissions failing. Customer-facing.",
                "Incident INC-2026-04-001 logged. Severity L1. SLA: first response required "
                "within 30 minutes of detection (2026-04-04T07:45:00Z), i.e., by 2026-04-04T08:15:00Z."
            ),
            (
                "[Feishu #incident-response-p1 dave Fri Apr 04 08:12 UTC 2026] "
                "First response sent to customer at 2026-04-04T08:12:00Z. "
                "Within 30-minute SLA (27 minutes from detection).",
                "First response at 2026-04-04T08:12:00Z confirmed. "
                "MTTD = 2026-04-04T08:12:00Z - 2026-04-04T07:45:00Z = 27 minutes. "
                "SLA status: PASSED (27 min < 30 min threshold)."
            ),
            (
                "[Feishu #incident-response-p1 dave Fri Apr 04 10:45:00 UTC 2026] "
                "Incident resolved at 2026-04-04T10:45:00Z. Root cause: AWS Lambda cold-start "
                "cascade in JSM webhook handler. Fix: provisioned concurrency enabled.",
                "Incident INC-2026-04-001 resolved at 2026-04-04T10:45:00Z.\n"
                "MTTR = resolved_at - first_response_at = 2026-04-04T10:45:00Z - 2026-04-04T08:12:00Z "
                "= 153 minutes.\n"
                "SLA breach: No (L1 first response within 30 min)."
            ),
        ]
    )

    # ── Discord DM Charlie（外部合作方咨询）──
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, CWD, "2026-04-05T15:00:00",
        [
            (
                "[Discord DM charlie_partner Sat Apr 05 15:00 UTC 2026] Hi, I'm trying to "
                "understand NebulaTech's SLA credit policy. For Atlassian Enterprise, if the "
                "uptime is 99.92% in a given month, what credit percentage applies? "
                "I've heard it might be 10% from the standard tier.",
                "For Atlassian Enterprise at 99.92% uptime: the applicable tier is "
                "the Enterprise-exclusive 99.90%–99.95% tier, which provides a **5% credit** "
                "(not 10%). The 10% tier applies to uptime below 99.90%. "
                "Source: https://www.atlassian.com/legal/sla"
            ),
            (
                "[Discord DM charlie_partner Sat Apr 05 15:10 UTC 2026] Interesting — so the "
                "5% tier is specific to Enterprise, not Premium? And what about AWS EC2 — "
                "if our EC2 uptime is 98.5%, what credit percentage would that get?",
                "Correct: the 5% credit tier (99.90%–99.95%) is Enterprise-exclusive. "
                "Premium plan starts credit at < 99.90% (10% tier).\n\n"
                "For AWS EC2 at 98.5% uptime: this falls in the 95.0%–99.0% range, "
                "which qualifies for a **30% service credit** "
                "(source: https://aws.amazon.com/ec2/sla/). "
                "This is higher than the 10% tier (99.0%–99.99%) and lower than "
                "the 100% tier (< 95.0%)."
            ),
            (
                "[Discord DM charlie_partner Sat Apr 05 15:20 UTC 2026] Got it. One more: "
                "when is the AWS EC2 credit claim deadline?",
                "AWS EC2 credit claim deadline: end of the **second billing cycle** following "
                "the incident month (source: https://aws.amazon.com/ec2/sla/). "
                "For an incident in 2024-11, the second billing cycle ends 2025-01-31."
            ),
        ]
    )

    return {
        "main": main_id,
        "history": [
            (s_slack, "slack"),
            (s_slack_dm, "slack"),
            (s_email, "email"),
            (s_feishu, "feishu"),
            (s_discord, "discord"),
        ],
    }


# ─── 8a. Update-2 辅助函数 ───────────────────────────────────────────────────
def _gen_update2_audit_records(path: Path) -> None:
    """生成 Q4 工单补丁审计记录（JSONL 格式，~20k tokens）。"""
    rng = random.Random(7654)
    sla_map = {"L1": 30, "L2": 120, "L3": 480, "L4": 1440}
    severities = ["L1", "L2", "L3", "L4"]
    base = datetime(2024, 10, 1, 8, 0, 0, tzinfo=timezone.utc)

    lines = []
    auditors = ["alice.wong", "bob.chen", "carol.davis", "dave.park"]
    audit_types = [
        "timestamp_validation",
        "arithmetic_check",
        "severity_classification_review",
        "response_time_verification",
        "data_entry_correction",
        "cross_reference_check",
    ]

    for i in range(500):
        sev = rng.choice(severities)
        sla = sla_map[sev]
        t = base + timedelta(days=rng.randint(0, 91), hours=rng.randint(0, 23))
        resp = rng.randint(5, 250)
        breach = resp > sla
        audit_t = t + timedelta(days=rng.randint(1, 14))
        corrected_resp = None
        correction_note = None
        if rng.random() < 0.1:
            # 需要修正
            corrected_resp = resp - rng.randint(5, 30)
            correction_note = rng.choice([
                "Timestamp recorded in local timezone, converted to UTC",
                "First response was auto-acknowledgment, corrected to human response time",
                "Response logged incorrectly due to JSM configuration issue",
                "Time sync issue between engineer laptop and JSM server",
            ])

        entry = {
            "audit_record_id": f"AUD-PATCH-2024Q4-{i+1:04d}",
            "ticket_id": f"Q4-{sev}-RECORD-{i+1:04d}",
            "severity": sev,
            "created_at": _iso(t),
            "first_response_at": _iso(t + timedelta(minutes=resp)),
            "response_minutes_original": resp,
            "sla_threshold_minutes": sla,
            "breach_status_original": "BREACH" if breach else "PASS",
            "audit_type": rng.choice(audit_types),
            "audited_by": rng.choice(auditors),
            "audited_at": _iso(audit_t),
            "correction_required": corrected_resp is not None,
            "corrected_response_minutes": corrected_resp,
            "correction_note": correction_note,
            "breach_status_post_correction": (
                "BREACH" if corrected_resp is not None and corrected_resp > sla
                else ("PASS" if corrected_resp is not None else ("BREACH" if breach else "PASS"))
            ),
            "policy_version": "v1",
            "audit_passed": True,
            "notes": f"Routine audit record {i+1} for Q4 2024 compliance verification",
        }
        lines.append(json.dumps(entry, ensure_ascii=False))

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ─── 8. Updates ───────────────────────────────────────────────────────────────
def gen_updates(sess_ids: dict, ticket_stats: dict) -> dict:
    s_feishu = sess_ids["history"][3][0]

    # ── Update-1（Q7 前）：sla_matrix_v2（L2: 2h→90min）+ 大体量 ticket/文档 ──
    # sla_matrix_v2.json（L2 收紧为 90min）
    sla_v2 = {
        "schema_version": "1.0",
        "version": "v2",
        "effective_date": "2025-02-01",
        "plan": "Atlassian Enterprise",
        "availability_commitment_pct": 99.95,
        "credit_tiers": [
            {
                "tier": "tier0",
                "description": "Enterprise-exclusive tier",
                "uptime_range": "99.90%–99.95%",
                "credit_pct": 5,
                "source": "https://www.atlassian.com/legal/sla"
            },
            {
                "tier": "tier1",
                "description": "Standard first tier",
                "uptime_range": "99.00%–99.90%",
                "credit_pct": 10,
                "source": "https://www.atlassian.com/legal/sla"
            },
            {
                "tier": "tier2",
                "description": "Standard second tier",
                "uptime_range": "95.00%–99.00%",
                "credit_pct": 25,
                "source": "https://www.atlassian.com/legal/sla"
            },
            {
                "tier": "tier3",
                "description": "Critical downtime",
                "uptime_range": "< 95.00%",
                "credit_pct": 50,
                "source": "https://www.atlassian.com/legal/sla"
            }
        ],
        "response_sla": {
            "L1": {
                "name": "Production down",
                "response_minutes": 30,
                "coverage": "24/7",
                "source": "https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html"
            },
            "L2": {
                "name": "Serious degradation",
                "response_minutes": 90,
                "coverage": "24/7",
                "note": "REVISED from 120min (v1) to 90min effective 2025-02-01 — internal policy tightening",
                "source": "NebulaTech internal policy revision v2 (based on Atlassian Enterprise baseline)"
            },
            "L3": {
                "name": "Moderate impact",
                "response_minutes": 480,
                "coverage": "weekdays",
                "source": "https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html"
            },
            "L4": {
                "name": "Limited impact",
                "response_minutes": 1440,
                "coverage": "weekdays",
                "source": "https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html"
            }
        },
        "downtime_minute_definition": "error rate > 5% per minute",
        "credit_claim_deadline_days": 15,
        "change_log": "v2 changes: L2 response_minutes revised from 120 to 90 (internal tightening)"
    }
    wj(UPD / "upd1_workspace" / "sla_matrix_v2.json", sla_v2)

    # escalation_policy v2（修订 L2 章节）
    w(UPD / "upd1_workspace" / "escalation_policy_v2.md", """\
# NebulaTech Escalation Policy v2.0 (Revised)

## Change Log

v2.0 (2025-02-01): L2 response time tightened from 2 hours to **90 minutes** based on
internal capacity review. New escalation trigger added for L2 at 90-minute threshold.

## 1. Scope

This policy applies to all Jira Service Management (JSM) tickets under the
Atlassian Enterprise plan. SLA thresholds are drawn from the official
Atlassian Support Offerings documentation, with NebulaTech internal adjustments.

## 2. Severity Classification (v2)

| Severity | Definition | Response SLA | Coverage |
|----------|-----------|--------------|----------|
| L1 | Production system completely unavailable | 30 minutes | 24/7 |
| L2 | Serious degradation — core features impaired | **90 minutes** (revised from 2h) | 24/7 |
| L3 | Moderate impact — some features affected | 8 hours | Weekdays |
| L4 | Limited impact — minor or cosmetic issue | 24 hours | Weekdays |

## 3. L2 Upgrade Trigger (NEW in v2)

A ticket is automatically escalated to Level 1 when L2 first response has not been
received within **90 minutes** of ticket creation. This is tighter than the Atlassian
Enterprise baseline of 2 hours, reflecting NebulaTech's internal customer commitment.

## 4. Escalation Triggers (all severities)

A ticket is escalated when `first_response_at - created_at > response_sla_minutes`.

Escalation levels:
- **Level 1 Escalation**: SLA breach detected → auto-alert to L1 Support Lead
- **Level 2 Escalation**: Breach > 2× SLA → escalate to VP Support
- **Level 3 Escalation**: Breach > 4× SLA → escalate to CTO

## 5. Credit Calculation

(Unchanged from v1 — credit tiers based on Atlassian Enterprise SLA)

For Atlassian Cloud Enterprise:
- Monthly uptime 99.90%–99.95%: 5% service credit
- Monthly uptime 99.00%–99.90%: 10% service credit
- Monthly uptime 95.00%–99.00%: 25% service credit
- Monthly uptime < 95.00%: 50% service credit

Source: https://www.atlassian.com/legal/sla
""")

    # Update-1：大体量附加文档（SLA v2 深度分析报告，~30k tokens）
    w(UPD / "upd1_workspace" / "sla_v2_impact_analysis.md", _gen_v2_impact_analysis())

    # Update-1 追加大批量 Q1 补充工单（用于 Q9，体量 ~5k tokens）
    rng = random.Random(2025)
    base_q1_extra = datetime(2025, 2, 1, 8, 0, 0, tzinfo=timezone.utc)
    extra_tickets = []
    for i in range(300):  # 增加到 300 条以提升体量
        sev = rng.choice(["L1", "L2", "L3", "L4"])
        sla_v2_map = {"L1": 30, "L2": 90, "L3": 480, "L4": 1440}
        t = base_q1_extra + timedelta(days=rng.randint(0, 59), hours=rng.randint(0, 23))
        # 大约 30% 违约
        if rng.random() < 0.3:
            resp = sla_v2_map[sev] + rng.randint(10, 120)
        else:
            resp = rng.randint(5, max(5, sla_v2_map[sev] - 1))
        extra_tickets.append(_make_ticket(
            f"Q1-EXTRA-{i+1:03d}", sev, _iso(t), resp, resp + rng.randint(60, 1440)
        ))
    wj(UPD / "upd1_workspace" / "tickets_batch_2025Q1_extra.json", {
        "schema_version": "1.0",
        "batch": "2025Q1_extra",
        "total_count": len(extra_tickets),
        "tickets": extra_tickets
    })

    # ── Update-2（Q11 前，含 supersede）──
    # feishu 新群消息：撤销 Update-1 的 L2=90min，恢复 L2=2h
    s_ops = gen_session_id("ops_feishu_revoke", TID)
    ops_seg = SessionBuilder(s_ops, CWD, "2026-04-06T09:00:00", is_main=False)
    ops_seg.add_user(
        "[Feishu #support-ops-management dave Mon Apr 06 09:00 UTC 2026] "
        "MANAGEMENT NOTICE (supersedes Update-1 L2 change): After review, the customer "
        "support team has determined that the internal L2 response SLA of 90 minutes "
        "is not achievable with current staffing levels. Effective immediately, "
        "the L2 response SLA is REVERTED to 2 hours (120 minutes), as per the "
        "original Atlassian Enterprise baseline. The `sla_matrix_v2.json` L2 value of "
        "90 minutes is SUPERSEDED — use 120 minutes for all L2 calculations going forward. "
        "Updated `sla_matrix_v2.json` will be re-issued. (ref: FEISHU-PRD4-L2-REVERT)"
    )
    ops_seg.add_assistant(
        "SUPERSEDE NOTICE APPLIED. The management notice from Feishu #support-ops-management "
        "(ref: FEISHU-PRD4-L2-REVERT) supersedes the Update-1 change to L2=90min. "
        "Effective immediately: L2 response SLA is reverted to 120 minutes (2 hours), "
        "the Atlassian Enterprise baseline. I will use L2=120min for all subsequent "
        "calculations, and will not apply the 90-minute value from `sla_matrix_v2.json`."
    )
    ops_seg.write(UPD / "upd2_sessions" / f"{s_ops}.jsonl")

    # Update-2 追加大量详细的 Q4 历史工单复核记录（增加体量到 >30k）
    _gen_update2_audit_records(UPD / "upd2_workspace" / "q4_patch_audit_records.jsonl")

    # tickets_patch_001.json — 修正 15 条工单的 first_response_at
    # 从 Q4 批次中取前 15 个违约工单，修正它们的 response 时间（让其中 5 条改为合规）
    q4_tickets = ticket_stats["q4_tickets"]
    breach_tickets = [t for t in q4_tickets if t["response_minutes"] > {"L1": 30, "L2": 120, "L3": 480, "L4": 1440}[t["severity"]]]
    patched = []
    for i, orig in enumerate(breach_tickets[:15]):
        sla_map = {"L1": 30, "L2": 120, "L3": 480, "L4": 1440}
        sla = sla_map[orig["severity"]]
        # 前 5 条修正为合规（减少 breach delta），后 10 条保留违约但修正具体时间
        if i < 5:
            new_resp = sla - 5  # 现在合规
        else:
            new_resp = orig["response_minutes"] - 3  # 仍违约，但时间略有修正
        created = datetime.fromisoformat(orig["created_at"].replace("Z", "+00:00"))
        new_first_response = created + timedelta(minutes=new_resp)
        patched.append({
            "ticket_id": orig["ticket_id"],
            "patch_reason": "data_entry_correction",
            "original_first_response_at": orig["first_response_at"],
            "corrected_first_response_at": _iso(new_first_response),
            "original_response_minutes": orig["response_minutes"],
            "corrected_response_minutes": new_resp,
        })
    wj(UPD / "upd2_workspace" / "tickets_patch_001.json", {
        "schema_version": "1.0",
        "patch_id": "patch_001",
        "applied_to_batch": "2024Q4",
        "patch_count": len(patched),
        "patches": patched,
        "note": "Corrects data entry errors in first_response_at for 15 tickets"
    })

    # Update-2：大体量文档（L2 恢复分析报告 + 详细的变更影响评估，~30k tokens）
    w(UPD / "upd2_workspace" / "l2_revert_impact_analysis.md", _gen_l2_revert_analysis())

    # 更新版 2024-11 月报草稿（V4 闭合数字更新）
    w(UPD / "upd2_workspace" / "monthly_sla_report_2024_11_draft_v2.md", """\
# NebulaTech Support Operations — Monthly SLA Report Draft v2
## Report Period: November 2024

**Draft Status:** Updated after tickets_patch_001 application
**Prepared by:** Support Operations Team
**Draft Date:** 2026-04-06T09:30:00Z

---

## Change from Draft v1

This draft incorporates corrections from `tickets_patch_001.json`:
- 5 tickets previously classified as L1 breaches corrected (were data entry errors)
- 10 L2/L3 tickets have slightly corrected response times

Updated headline figures:
- Total tickets processed: 172 (unchanged)
- Total SLA breaches: 19 (revised from 24, after 5 breach corrections)
- Overall compliance rate: 88.95% (revised from 86.05%)

All other analysis pending final confirmation. L2 SLA reverted to 2h per
management notice FEISHU-PRD4-L2-REVERT.

---

*This is a working draft pending Alice's review.*
""")

    updates_decl = {
        "upd2_audit": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "q4_patch_audit_records.jsonl", "action": "new",
                 "target": "docs/q4_patch_audit_records.jsonl"},
            ]
        },
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {"name": "sla_matrix_v2.json", "action": "new",
                 "target": "policy/sla_matrix_v2.json"},
                {"name": "escalation_policy_v2.md", "action": "new",
                 "target": "policy/escalation_policy_v2.md"},
                {"name": "tickets_batch_2025Q1_extra.json", "action": "new",
                 "target": "tickets/tickets_batch_2025Q1_extra.json"},
            ]
        },
        "upd2_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd2_sessions",
            "files": [
                {"name": f"{s_ops}.jsonl", "action": "new",
                 "target": f"{s_ops}.jsonl", "channel": "feishu"}
            ]
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "tickets_patch_001.json", "action": "new",
                 "target": "tickets/tickets_patch_001.json"},
                {"name": "monthly_sla_report_2024_11_draft_v2.md", "action": "new",
                 "target": "reports/monthly_sla_report_2024_11_draft_v2.md"},
            ]
        },
    }
    return updates_decl


# ─── 9. 补充大体量文档（撑起 100k+ token 要求）────────────────────────────────
def gen_bulk_docs() -> None:
    """生成大体量 Markdown 文档（合规审计手册、SLA 知识库、工单操作规范），
    每份 ~15-25k tokens，确保 workspace 总体量 > 100k。"""

    # 9.1 SLA 合规审计手册（~25k tokens）
    w(WS / "docs" / "sla_compliance_audit_manual.md", _gen_audit_manual())

    # 9.2 SLA 知识库（~20k tokens）
    w(WS / "docs" / "sla_knowledge_base.md", _gen_knowledge_base())

    # 9.3 工单操作规范手册（~15k tokens）
    w(WS / "docs" / "ticket_operations_handbook.md", _gen_ticket_handbook())

    # 9.4 历史 SLA 违约事件日志（~15k tokens）— 大型 JSONL 格式的审计日志
    _gen_audit_log(WS / "docs" / "sla_breach_audit_log_2024.jsonl")

    # 9.6 完整工单操作规程（更大体量，~20k tokens）
    w(WS / "docs" / "full_ticket_sop.md", _gen_full_sop())

    # 9.5 AWS SLA 参考指南（~10k tokens）
    w(WS / "docs" / "aws_sla_reference_guide.md", _gen_aws_guide())


def _gen_audit_manual() -> str:
    """生成 SLA 合规审计手册全文（~25k tokens）。"""
    sections = []
    sections.append("# NebulaTech SLA Compliance Audit Manual v3.0\n")
    sections.append("""
**Effective Date:** 2024-01-01
**Revision:** 3.0
**Owner:** Support Operations Team
**Approved By:** Alice Wong, Support Operations Manager

---

## Table of Contents

1. Introduction and Scope
2. SLA Policy Framework
3. Ticket Classification and Severity Levels
4. Response Time Measurement Methodology
5. SLA Breach Detection Procedures
6. Credit Calculation and Claim Procedures
7. Escalation Procedures
8. Reporting Requirements
9. Audit Trail Requirements
10. Governance and Accountability
11. Appendix A: SLA Matrix Quick Reference
12. Appendix B: Credit Calculation Examples
13. Appendix C: Escalation Contact Directory
14. Appendix D: Tool Integration Guide

---

## 1. Introduction and Scope

### 1.1 Purpose

This manual defines the standards, procedures, and responsibilities for ensuring
SLA (Service Level Agreement) compliance in NebulaTech's customer support operations.
It applies to all customer support tickets processed through the Jira Service Management
(JSM) platform.

### 1.2 Scope

This manual covers:
- All customer support tickets for NebulaTech Cloud products (JSM)
- SLA measurement and breach detection
- Credit calculation and claim procedures
- Escalation and reporting requirements
- Audit trail maintenance

### 1.3 Policy Framework

NebulaTech's SLA policy is based on:
- **Primary:** Atlassian Cloud Enterprise SLA (https://www.atlassian.com/legal/sla)
- **Support Response:** Atlassian Support Offerings (https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html)
- **Infrastructure:** AWS Enterprise Support (https://aws.amazon.com/premiumsupport/plans/)
- **Google Cloud:** Technical Support Services Guidelines (https://cloud.google.com/terms/tssg)

---

## 2. SLA Policy Framework

### 2.1 Atlassian Cloud Enterprise SLA

NebulaTech operates on the Atlassian Cloud Enterprise plan, which provides:

#### 2.1.1 Availability Commitment
- **Monthly Uptime Target:** 99.95%
- **Downtime Minute Definition:** Any minute in which the error rate exceeds 5%

#### 2.1.2 Service Credit Tiers (Enterprise)

The following credit tiers apply to Enterprise plan subscribers:

| Monthly Uptime | Credit Percentage | Notes |
|---|---|---|
| ≥ 99.95% | 0% | SLA met |
| 99.90% – 99.95% | **5%** | Enterprise-exclusive tier |
| 99.00% – 99.90% | 10% | Standard tier 1 |
| 95.00% – 99.00% | 25% | Standard tier 2 |
| < 95.00% | 50% | Critical tier |

**IMPORTANT:** The 99.90%–99.95% tier (5% credit) is **exclusive to Enterprise**.
Premium plan customers are NOT eligible for this tier.

Source: https://www.atlassian.com/legal/sla

#### 2.1.3 Credit Claim Deadline
Credits must be requested within **15 calendar days** after the end of the
calendar month in which the downtime occurred.

### 2.2 Atlassian Support Response Times

| Severity | Enterprise SLA | Premium SLA | Standard SLA |
|---|---|---|---|
| L1 | 30 min (24/7) | 1 hour (24/7) | 2 business hours (9/5) |
| L2 | 2 hours (24/7) | 2 hours (24/5) | 6 business hours |
| L3 | 8 hours (weekdays) | 8 hours (weekdays) | Next business day |
| L4 | 24 hours (weekdays) | 24 hours (weekdays) | 2 business days |

Source: https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html

**Common Misunderstanding:** L1 = 30 minutes for Enterprise; 1 hour for Premium.
Do NOT confuse these. Historical records may show the incorrect 1-hour value
from before January 2024 (the ARCHIVED v0 policy contained this error).

### 2.3 AWS Enterprise Support Response Times

| Severity Code | Severity Name | Response Time (Enterprise) |
|---|---|---|
| critical | Business-critical system down | < 15 minutes |
| urgent | Production system down | < 1 hour |
| high | Production system impaired | < 4 hours |
| normal | System impaired | < 12 hours |
| low | General guidance | < 24 hours |

Source: https://aws.amazon.com/premiumsupport/plans/
Source (codes): https://docs.aws.amazon.com/awssupport/latest/APIReference/API_SeverityLevel.html

### 2.4 AWS EC2 SLA

| Level | Monthly Uptime Target | Credit Tiers |
|---|---|---|
| Region Level | 99.99% | 10% (99.0–99.99%), 30% (95.0–99.0%), 100% (< 95.0%) |
| Instance Level | 99.5% | 10% (99.0–99.5%), 30% (95.0–99.0%), 100% (< 95.0%) |

Source: https://aws.amazon.com/ec2/sla/

Automatic Credit: EC2 provides automatic service credits (no claim needed)
if an instance is unavailable for more than 6 minutes within a clock hour.

### 2.5 AWS Lambda SLA

| Monthly Uptime | Credit Percentage |
|---|---|
| ≥ 99.95% | 0% |
| 99.00% – 99.95% | 10% |
| 95.00% – 99.00% | 25% |
| < 95.00% | 100% |

Availability Interval: 5-minute measurement periods
Error Definition: HTTP 500 or 503 status codes (excluding custom codes from function code)
Source: https://aws.amazon.com/lambda/sla/

### 2.6 Google Cloud TSSG

| Priority | Definition |
|---|---|
| P0 | Impact to operating environments provisioned to support Mission Critical Services |
| P1 | Critical Impact – Service Unusable in Production |
| P2 | High Impact — Severely Impaired |
| P3 | Medium Impact — Partially Impaired |
| P4 | Low Impact — Fully Usable |

Premium Support Response Times:
- P1: 15 minutes
- P2: 2 hours
- P3: 4 hours
- P4: 8 hours

Source: https://cloud.google.com/terms/tssg

---

## 3. Ticket Classification and Severity Levels

### 3.1 Severity Classification Criteria

#### L1 — Production Down (Critical)
**Trigger Conditions:**
- Complete service unavailability affecting all users
- Authentication system failure
- Data loss or corruption risk
- Revenue-impacting system outage

**Examples:**
- JSM portal completely inaccessible
- All ticket submissions failing
- Customer portal returning 500/503 errors for all users
- Database connection pool exhausted

**Response Requirement:** First response within 30 minutes (24/7)

#### L2 — Serious Degradation (High)
**Trigger Conditions:**
- Core features unavailable for a subset of users
- Significant performance degradation (> 5x baseline latency)
- Critical workflow broken but workaround exists

**Examples:**
- Ticket search returning incorrect results
- Email notifications not delivered to 30%+ of users
- Reporting dashboard timing out for large datasets
- API rate limiting causing intermittent failures

**Response Requirement:** First response within 2 hours (24/7)
[Note: Internal policy may adjust this threshold; see current sla_matrix version]

#### L3 — Moderate Impact (Medium)
**Trigger Conditions:**
- Non-critical features impaired
- Performance degradation affecting subset of workflows
- Workaround available with moderate effort

**Examples:**
- SLA reports generating with incorrect formatting
- Bulk ticket import processing slowly
- Notification templates not rendering custom fields
- Search autocomplete not working

**Response Requirement:** First response within 8 hours (weekdays only)

#### L4 — Limited Impact (Low)
**Trigger Conditions:**
- Cosmetic issues
- Feature requests masquerading as bugs
- Minor usability concerns
- How-to questions incorrectly logged as incidents

**Examples:**
- Button misalignment in the UI
- PDF export missing custom logo
- Incorrect tooltip text
- Field label typos

**Response Requirement:** First response within 24 hours (weekdays only)

### 3.2 Severity Escalation

Initial severity assignments may be escalated by:
1. The customer (via severity upgrade request)
2. The support engineer (if impact assessment increases)
3. Automated monitoring (if system metrics cross thresholds)
4. Management review (during SLA compliance audits)

Severity can be downgraded only by a senior support engineer or manager,
with documented justification.

### 3.3 Severity Assessment Data Model

Tickets are stored in JSON format with the following required fields:

```json
{
  "ticket_id": "string",
  "severity": "L1|L2|L3|L4",
  "status": "open|in_progress|resolved|closed",
  "created_at": "ISO8601_timestamp",
  "first_response_at": "ISO8601_timestamp",
  "resolved_at": "ISO8601_timestamp",
  "response_minutes": "integer"
}
```

---

## 4. Response Time Measurement Methodology

### 4.1 Clock Start

The response time clock starts at `created_at` — the exact timestamp when the
ticket was created in JSM, regardless of time of day or day of week.

For L1 and L2 (24/7 coverage), the clock runs continuously.
For L3 and L4 (weekday coverage), business hours rules apply but for simplicity
NebulaTech measures wall-clock minutes from creation for audit purposes.

### 4.2 Clock Stop

The clock stops at `first_response_at` — the timestamp of the first substantive
response from a NebulaTech support engineer (not an auto-acknowledgment).

### 4.3 Breach Determination

A ticket is in SLA breach if:
```
response_minutes > expected_response_minutes_for_severity
```

Where `expected_response_minutes_for_severity` is:
- L1: 30 minutes
- L2: 120 minutes (v1 policy) or as per current policy version
- L3: 480 minutes
- L4: 1440 minutes

### 4.4 Breach Delta Calculation

```
breach_delta_min = actual_response_min - expected_response_min
```

For breached tickets, this value is positive (indicates how many minutes over SLA).
For compliant tickets, this would be negative (not typically reported).

### 4.5 Important Note on Policy Updates

When the SLA policy is updated (e.g., L2 threshold changes from 120min to 90min),
all breach calculations must use the policy version that was **in effect at the time
of the ticket creation**.

For tickets created before a policy update:
- Use the old policy version to determine breach status
- Re-analysis under the new policy version requires creating a new report file

---

## 5. SLA Breach Detection Procedures

### 5.1 Automated Detection

The JSM platform is configured to flag potential SLA breaches via:
1. Real-time SLA countdown timers (visible in JSM ticket view)
2. Automated alerts at 50%, 75%, 90%, and 100% of SLA threshold
3. Webhook notifications to the #support-ops Slack channel

### 5.2 Manual Audit

Manual SLA audits are conducted:
- Daily: spot-check of L1 tickets from the previous 24 hours
- Weekly: full review of L2 and L3 breaches
- Monthly: comprehensive audit for reporting

### 5.3 Audit Process

For each ticket batch:
1. Load ticket data from JSON batch file
2. Apply the policy version in effect during the batch period
3. Compare `response_minutes` to severity SLA threshold
4. Flag tickets where `response_minutes > SLA_threshold`
5. Calculate `breach_delta_min = response_minutes - SLA_threshold`
6. Generate breach report file

### 5.4 Data Quality Checks

Before running breach analysis:
1. Verify all required fields are present
2. Confirm ISO 8601 timestamp format
3. Validate severity codes (L1, L2, L3, L4 only)
4. Verify arithmetic: `response_minutes ≈ (first_response_at - created_at) / 60`
5. Check for data entry errors (common: first_response_at recorded in wrong timezone)

---

## 6. Credit Calculation and Claim Procedures

### 6.1 Atlassian Cloud Credits

#### 6.1.1 Eligibility Determination

To determine credit eligibility:
1. Obtain the monthly uptime percentage from Atlassian's status page
2. Compare against the Enterprise credit tier table
3. If uptime falls in 99.90%–99.95% range: 5% credit applies (Enterprise only)
4. Calculate credit amount: `credit_pct × monthly_contract_value / 100`

#### 6.1.2 Example Calculation

Monthly uptime: 99.92%
Credit tier: 99.90%–99.95% → 5% credit
Monthly contract: $10,000
Credit amount: $10,000 × 0.05 = $500

#### 6.1.3 Claim Submission

1. Log into Atlassian account portal
2. Navigate to: Account → Billing → SLA Credits
3. Submit credit request with:
   - Affected month and year
   - Documented uptime percentage
   - Reference to Atlassian status page incident report
4. **Deadline: 15 calendar days after end of the affected month**

### 6.2 AWS EC2 Credits

#### 6.2.1 Credit Tiers (Region Level)

| Monthly Uptime | Credit Percentage |
|---|---|
| 99.0% – 99.99% | 10% |
| 95.0% – 99.0% | **30%** |
| < 95.0% | 100% |

Source: https://aws.amazon.com/ec2/sla/

#### 6.2.2 Automatic Credits

AWS provides automatic service credits (no claim needed) for EC2 instances
that are unavailable for more than **6 minutes within a clock hour**.

#### 6.2.3 Claim Deadline

For credits not automatically applied: submit claim before the **end of the second
billing cycle following the month of the incident**.

Example: Incident in 2024-11 → deadline is 2025-01-31.

### 6.3 AWS Lambda Credits

| Monthly Uptime | Credit Percentage |
|---|---|
| 99.0% – 99.95% | 10% |
| 95.0% – 99.0% | 25% |
| < 95.0% | 100% |

Measurement: Per 5-minute interval
Error threshold: > 5% of requests returning 500/503 errors
Source: https://aws.amazon.com/lambda/sla/

---

## 7. Escalation Procedures

### 7.1 L1 Escalation Triggers

| Trigger | Action | Timeline |
|---|---|---|
| 30-min SLA approaching (50% elapsed) | Alert to on-call engineer | At 15 min |
| SLA breach detected | Page Support Lead | Immediately |
| 2× SLA breach (>60 min no response) | Escalate to VP Support | Immediately |
| 4× SLA breach (>120 min no response) | Escalate to CTO | Immediately |

### 7.2 L2 Escalation Triggers

| Trigger | Action | Timeline |
|---|---|---|
| L2 SLA approaching (75% elapsed) | Alert to support team | At 90 min (v1) |
| SLA breach detected | Notify Support Lead | Within 15 min |
| 2× SLA breach | Escalate to VP Support | Immediately |

### 7.3 Escalation Contact Matrix

| Level | Contact | Channel | Response SLA |
|---|---|---|---|
| L1 On-Call | On-call rotation | PagerDuty | 5 min |
| Support Lead | Alice Wong | Slack DM | 10 min |
| VP Support | (confidential) | Slack DM | 15 min |
| CTO | (confidential) | Phone + Slack | 5 min |

---

## 8. Reporting Requirements

### 8.1 Monthly Escalation Report

A formal escalation report is produced monthly with the following structure:

```json
{
  "metadata": {
    "generated_at": "ISO8601_timestamp",
    "agent_id": "string",
    "schema_version": "1.0"
  },
  "report_period": "YYYY-MM",
  "sla_policy_version": "string",
  "breach_summary": {
    "total_tickets": "int",
    "total_breaches": "int",
    "breach_pct": "float (2 decimal places)",
    "by_severity": {
      "L1": {"total": "int", "breached": "int", "compliance_rate": "float"},
      "L2": {"total": "int", "breached": "int", "compliance_rate": "float"},
      "L3": {"total": "int", "breached": "int", "compliance_rate": "float"},
      "L4": {"total": "int", "breached": "int", "compliance_rate": "float"}
    }
  },
  "top_breached_tickets": [
    {
      "ticket_id": "string",
      "severity": "string",
      "expected_response_min": "int",
      "actual_response_min": "int",
      "breach_delta_min": "int"
    }
  ],
  "credit_recommendations": [
    {
      "service": "string",
      "actual_uptime_pct": "float",
      "applicable_tier": "string",
      "credit_pct": "int",
      "source_url": "string"
    }
  ],
  "reviewer_signature": "string"
}
```

### 8.2 Report Naming Convention

Monthly reports: `escalation_report_YYYY_MM.json`
Draft reports: `escalation_report_YYYY_MM_draft.json`

### 8.3 Distribution List

Reports are distributed to:
- Alice Wong (Support Operations Manager)
- Dave Park (Legal/Compliance)
- VP Support
- Finance (for credit calculation purposes)

---

## 9. Audit Trail Requirements

### 9.1 Required Audit Records

For each SLA compliance cycle:
1. Original ticket data file (tickets_batch_YYYYQN.json)
2. SLA policy version in effect (sla_matrix_vN.json)
3. Breach calculation output (breach_tickets_QN.json)
4. Compliance statistics (sla_compliance_QN.json)
5. Final escalation report (escalation_report_YYYY_MM.json)
6. SHA-256 sign-off (signoff.txt with VERIFIED:<hash>)

### 9.2 Version Control

All policy documents and analysis files must include version identifiers.
Policy changes must be recorded with:
- Previous version reference
- New version designation
- Effective date
- Supersede notice (if replacing an earlier instruction)

### 9.3 Data Integrity

To verify the integrity of deliverable files:
1. Compute SHA-256 digest of the JSON file bytes
2. Record as `VERIFIED:<64-character hex digest>`
3. Verification script must be executed (not hand-calculated)

---

## 10. Governance and Accountability

### 10.1 Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Support Operations Manager | Owns SLA policy and reporting; signs off on monthly reports |
| Support Engineers | First-line SLA compliance; escalates per defined triggers |
| Legal/Compliance | Reviews credit claims and regulatory compliance |
| SupportOps AI | Automates analysis, generates reports, maintains audit trail |

### 10.2 Policy Change Management

All changes to the SLA policy (including response time changes) require:
1. Written approval from the Support Operations Manager
2. 2-week advance notice to the support team
3. Updated `sla_matrix_vN.json` (with version increment)
4. Updated `escalation_policy.md`
5. Communication to all affected parties

Emergency policy changes (e.g., due to staffing constraints) may be issued
via official channel notice (Slack #support-ops-management, Feishu) with
immediate effect, but must be documented in writing within 24 hours.

### 10.3 Audit Review Cadence

| Review Type | Frequency | Owner |
|---|---|---|
| SLA breach review | Daily (L1 only) | Support Lead |
| Compliance report | Weekly | Support Operations Manager |
| Monthly audit | Monthly | Support Operations Manager + Legal |
| Annual policy review | Annually | VP Support + Legal |

---

## Appendix A: SLA Matrix Quick Reference

### Atlassian Enterprise (Current — policy/sla_matrix_v1.json)

| Severity | Response SLA | Coverage | Breach Threshold (min) |
|---|---|---|---|
| L1 | 30 minutes | 24/7 | 30 |
| L2 | 2 hours | 24/7 | 120 |
| L3 | 8 hours | Weekdays | 480 |
| L4 | 24 hours | Weekdays | 1440 |

### Credit Tier Reference (Enterprise)

| Monthly Uptime | Credit | Notes |
|---|---|---|
| ≥ 99.95% | 0% | SLA met |
| 99.90% – 99.95% | **5%** | Enterprise-exclusive |
| 99.00% – 99.90% | 10% | |
| 95.00% – 99.00% | 25% | |
| < 95.00% | 50% | |

### AWS EC2 Credit Reference

| Monthly Uptime | Credit |
|---|---|
| 99.0% – 99.99% | 10% |
| 95.0% – 99.0% | **30%** |
| < 95.0% | 100% |

### AWS Lambda Credit Reference

| Monthly Uptime | Credit |
|---|---|
| 99.0% – 99.95% | 10% |
| 95.0% – 99.0% | 25% |
| < 95.0% | 100% |

---

## Appendix B: Credit Calculation Examples

### Example 1: Atlassian Enterprise at 99.92%

```
actual_uptime_pct = 99.92
tier = "99.90%-99.95% (Enterprise-exclusive)"
credit_pct = 5
monthly_contract = 10000
credit_amount = 10000 * 5 / 100 = 500.00
```

### Example 2: AWS EC2 at 98.5%

```
actual_uptime_pct = 98.5
tier = "95.0%-99.0%"
credit_pct = 30
monthly_ec2_spend = 5000
credit_amount = 5000 * 30 / 100 = 1500.00
claim_deadline_note = "End of second billing cycle after incident month"
```

For incident in November 2024:
- First billing cycle: December 2024 (ends 2024-12-31)
- Second billing cycle: January 2025 (ends 2025-01-31)
- **Claim deadline: 2025-01-31**

### Example 3: AWS Lambda at 97.0%

```
actual_uptime_pct = 97.0
tier = "95.0%-99.0%"
credit_pct = 25
```

---

## Appendix C: Escalation Contact Directory

(Contacts redacted for privacy — refer to internal directory)

| Level | Team/Role | Contact Method |
|---|---|---|
| L1 First Response | On-call Support | PagerDuty rotation |
| L1 Escalation | Support Lead (Alice Wong) | Slack: @alice-wong |
| L2 Escalation | VP Support | Slack: @vp-support |
| AWS Cases | AWS TAM (Technical Account Manager) | AWS Support portal |
| Atlassian Cases | Atlassian Enterprise Support | JSM premium portal |
| Legal Review | Dave Park | Feishu: Dave Park |
| External Partners | Partner Success | Email: partner@nebulatech.com |

---

## Appendix D: Tool Integration Guide

### Jira Service Management Integration

NebulaTech uses JSM REST API for automated ticket processing:

```python
# Example: fetch ticket details
import requests
headers = {"Authorization": f"Bearer {API_TOKEN}"}
resp = requests.get(
    f"https://nebulatech.atlassian.net/rest/api/3/issue/{ticket_id}",
    headers=headers
)
ticket = resp.json()
created_at = ticket["fields"]["created"]
first_response_at = ticket["fields"]["resolutiondate"]  # JSM SLA first response
```

### SLA Calculation Script Integration

Use `scripts/validate_ticket_sla.py` for batch validation:

```bash
python scripts/validate_ticket_sla.py output/breach_tickets_Q4_v3.json
```

Output format:
```json
{
  "validated_count": 185,
  "error_count": 2,
  "invalid_ticket_ids": ["Q4-L2-BREACH-007", "Q4-L1-BREACH-003"]
}
```

---

*End of SLA Compliance Audit Manual v3.0*
*Next revision due: 2025-01-01*
*Questions: sla-policy@nebulatech.com*
""")
    return "\n".join(sections)


def _gen_knowledge_base() -> str:
    """生成 SLA 知识库文档（~20k tokens）。"""
    return """\
# NebulaTech SLA Knowledge Base
## Customer Support SLA Reference — Comprehensive Guide

**Version:** 2.3
**Last Updated:** 2024-11-01
**Maintained by:** Support Operations Team

---

## Section 1: Frequently Asked Questions

### Q1: What is NebulaTech's SLA for L1 (Production Down) tickets?

**A:** First response within **30 minutes** (24/7), under the Atlassian Enterprise plan.

This is a common source of confusion because:
- Atlassian **Premium** plan has L1 = 1 hour (24/7)
- Atlassian **Standard** plan has L1 = 2 business hours (9/5)
- Our **Enterprise** plan has L1 = **30 minutes** (24/7)

Reference: https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html

The old (archived) v0 policy contained an error showing L1 = 1 hour for Enterprise.
This has been corrected in v1 (effective 2024-01-01). Do not reference the
archived document.

### Q2: When does a 5% credit apply for Atlassian Enterprise?

**A:** When monthly uptime falls between 99.90% and 99.95% (exclusive of 99.95%).

This tier is **Enterprise-exclusive** — Premium plan starts credit only at < 99.90%.

Reference: https://www.atlassian.com/legal/sla

### Q3: How is "Downtime Minute" defined for Atlassian?

**A:** A Downtime Minute is any one-minute period in which the Cloud Product has an
**error rate greater than 5%** (i.e., more than 5% of requests return errors).

### Q4: What is the deadline for filing Atlassian credit claims?

**A:** **15 calendar days** after the end of the calendar month in which downtime occurred.

Example: For downtime in November 2024, deadline is December 15, 2024.

### Q5: How are AWS EC2 SLA credits calculated?

**A:** AWS EC2 provides two types of credits:
1. **Automatic credits:** For instances unavailable > 6 minutes per clock hour — no claim needed.
2. **Claim-required credits:** Based on monthly uptime percentage:
   - 99.0%–99.99% → 10% credit
   - 95.0%–99.0% → **30% credit**
   - < 95.0% → 100% credit

Source: https://aws.amazon.com/ec2/sla/

Claim deadline: **End of the second billing cycle** after the month of the incident.

### Q6: What defines a Lambda "error" for SLA purposes?

**A:** AWS Lambda errors (for SLA calculation) are HTTP **500 or 503 status codes**,
excluding custom error codes generated by the function code itself.

Availability is measured per **5-minute interval**.

Source: https://aws.amazon.com/lambda/sla/

### Q7: What are GCP P0 and P1 definitions?

**A:**
- **P0:** Impact to operating environments provisioned to support **Mission Critical Services**
- **P1:** **Critical Impact – Service Unusable in Production**

GCP Premium Support response time for P1: **15 minutes**
GCP Premium Support response time for P2: **2 hours**

Source: https://cloud.google.com/terms/tssg

---

## Section 2: SLA Policy Versions and Change History

### Version History

| Version | Effective Date | Key Changes |
|---|---|---|
| v0 (ARCHIVED) | 2023-01-01 | Original policy; contained error: Enterprise L1 = 1 hour (incorrect) |
| **v1 (current)** | 2024-01-01 | Corrected Enterprise L1 to 30 minutes; added credit tier details |
| v2 (proposed/superseded) | 2025-02-01 | L2 tightened to 90 min; later reverted by management notice |

### Version Supersede Chain

```
v0 (L1=60min WRONG)
  → superseded by v1 (L1=30min CORRECT) on 2024-01-01
v1 (L2=120min)
  → partially superseded by v2 (L2=90min) on 2025-02-01
v2 L2 change (90min)
  → superseded by management notice FEISHU-PRD4-L2-REVERT (L2 reverted to 120min)
```

**Key principle:** When a supersede notice is issued, ALL calculations for affected
periods must use the newly applicable policy. Do not "stack" old and new — the
superseding instruction fully replaces the prior one for its scope.

---

## Section 3: Breach Analysis Methodology

### 3.1 Standard Breach Report Format

Each breach report (breach_tickets_QN.json) must contain:

```json
{
  "schema_version": "1.0",
  "metadata": {
    "generated_at": "YYYY-MM-DDTHH:MM:SSZ",
    "agent_id": "supportops-ai",
    "schema_version": "1.0"
  },
  "sla_policy_version": "v1",
  "batch": "2024Q4",
  "breach_count": 28,
  "tickets": [
    {
      "ticket_id": "Q4-L1-BREACH-001",
      "severity": "L1",
      "expected_response_min": 30,
      "actual_response_min": 47,
      "breach_delta_min": 17
    }
  ]
}
```

### 3.2 Compliance Rate Calculation

```
compliance_rate = (total - breached) / total * 100
```

Expressed as a percentage to **two decimal places** (e.g., 86.00, not 86.0 or 86.005).

### 3.3 Cross-Round Data Closure

When generating a combined summary across multiple ticket batches:

```
total_breaches = Q4_breaches + Q1_breaches + ...
total_tickets = Q4_total + Q1_total + ...
breach_pct = total_breaches / total_tickets * 100
```

The numbers must be arithmetically consistent across all output files.
If Q3 report shows 28 Q4 breaches, the Q5 combined report must use the same 28.

### 3.4 Impact of Policy Updates on Historical Data

When a policy update changes an SLA threshold (e.g., L2 from 120min to 90min):
- **Historical tickets** (created before policy effective date): use the OLD threshold
- **New tickets** (created after policy effective date): use the NEW threshold
- **Re-analysis reports** (e.g., Q7 re-analysis): explicitly state which policy version

---

## Section 4: Ticket Data Quality Guidelines

### 4.1 Common Data Entry Errors

1. **Timezone mismatch:** first_response_at stored in local timezone, not UTC
   → Correction: standardize all timestamps to UTC (YYYY-MM-DDTHH:MM:SSZ)

2. **Wrong severity classification:** ticket downgraded from L1 to L2 after resolution
   → Audit rule: use severity at time of creation

3. **Auto-response counted as first response:** System acknowledgment counted
   → Policy: only substantive human responses count for SLA clock

4. **Rounding error in response_minutes:** calculated from timestamps with seconds
   → Policy: round to nearest minute; breach threshold is exact

### 4.2 Patch Process

When data entry errors are identified:
1. Create a patch file (tickets_patch_NNN.json) with corrected values
2. Record original and corrected values
3. Document reason for correction
4. Re-run breach analysis with patched data
5. Generate updated breach report (breach_tickets_QN_vN.json)

---

## Section 5: Multi-Cloud SLA Reference Quick Card

### Atlassian Cloud Enterprise

| Metric | Value | Source |
|---|---|---|
| Monthly uptime | 99.95% | https://www.atlassian.com/legal/sla |
| L1 response | 30 min (24/7) | https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html |
| L2 response | 2 hours (24/7) | https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html |
| L3 response | 8 hours (weekdays) | https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html |
| L4 response | 24 hours (weekdays) | https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html |
| Credit 99.90–99.95% | 5% | https://www.atlassian.com/legal/sla |
| Credit 99.00–99.90% | 10% | https://www.atlassian.com/legal/sla |
| Credit 95.00–99.00% | 25% | https://www.atlassian.com/legal/sla |
| Credit < 95.00% | 50% | https://www.atlassian.com/legal/sla |
| Credit claim deadline | 15 days | https://www.atlassian.com/legal/sla |
| Downtime definition | Error rate > 5%/min | https://www.atlassian.com/legal/sla |

### AWS EC2

| Metric | Value | Source |
|---|---|---|
| Region uptime | 99.99% | https://aws.amazon.com/ec2/sla/ |
| Instance uptime | 99.5% | https://aws.amazon.com/ec2/sla/ |
| Credit 99.0–99.99% | 10% | https://aws.amazon.com/ec2/sla/ |
| Credit 95.0–99.0% | 30% | https://aws.amazon.com/ec2/sla/ |
| Credit < 95.0% | 100% | https://aws.amazon.com/ec2/sla/ |
| Auto credit trigger | 6 min/clock hour | https://aws.amazon.com/ec2/sla/ |
| Claim deadline | End 2nd billing cycle | https://aws.amazon.com/ec2/sla/ |

### AWS Lambda

| Metric | Value | Source |
|---|---|---|
| Monthly uptime | 99.95% | https://aws.amazon.com/lambda/sla/ |
| Credit 99.0–99.95% | 10% | https://aws.amazon.com/lambda/sla/ |
| Credit 95.0–99.0% | 25% | https://aws.amazon.com/lambda/sla/ |
| Credit < 95.0% | 100% | https://aws.amazon.com/lambda/sla/ |
| Error definition | HTTP 500/503 | https://aws.amazon.com/lambda/sla/ |
| Measurement interval | 5 minutes | https://aws.amazon.com/lambda/sla/ |

### Google Cloud (Premium Support)

| Metric | Value | Source |
|---|---|---|
| P0 definition | Mission Critical Services impact | https://cloud.google.com/terms/tssg |
| P1 definition | Critical Impact – Service Unusable in Production | https://cloud.google.com/terms/tssg |
| P1 response | 15 minutes | https://cloud.google.com/terms/tssg |
| P2 response | 2 hours | https://cloud.google.com/terms/tssg |
| P3 response | 4 hours | https://cloud.google.com/terms/tssg |
| P4 response | 8 hours | https://cloud.google.com/terms/tssg |

---

## Section 6: Honeypot and Decoy Awareness

### Known Incorrect Values

Support engineers must be aware of common incorrect values that appear in
unofficial documents:

| Context | Incorrect Value | Correct Value | Source of Error |
|---|---|---|---|
| Enterprise L1 response | 1 hour | **30 minutes** | ARCHIVED v0 policy; email auto-summary |
| Enterprise L1 response | 60 minutes | **30 minutes** | ARCHIVED v0 policy |
| EC2 credit at 98.5% | 10% | **30%** | Confusing tier1 with tier2 |

### ARCHIVED_sla_matrix_v0.json

This file is retained for audit trail purposes only. **Do not use it for policy decisions.**
Key error: L1 response_minutes = 60 (should be 30).

The email auto-summary from Carol Davis (Product Manager) also contains the incorrect
L1 = 1 hour value. This is a known error in the auto-summary generator and was
corrected in Alice's reply of 2026-04-03.

---

*End of SLA Knowledge Base*
*Maintained by: Support Operations Team*
*Questions: sla-policy@nebulatech.com*
"""


def _gen_ticket_handbook() -> str:
    """生成工单操作规范手册（~15k tokens）。"""
    return """\
# NebulaTech Ticket Operations Handbook
## Jira Service Management Operations Guide

**Version:** 1.4
**Effective Date:** 2024-06-01
**Owner:** Support Operations

---

## Chapter 1: Ticket Lifecycle

### 1.1 Ticket States

```
[New] → [In Progress] → [Pending Customer] → [Resolved] → [Closed]
           ↓                                       ↑
       [Escalated] ────────────────────────────────┘
```

### 1.2 State Definitions

| State | Description | SLA Clock |
|---|---|---|
| New | Created, awaiting first response | Running |
| In Progress | Engineer assigned, response sent | Stopped for first response |
| Pending Customer | Awaiting customer information | Paused |
| Resolved | Solution delivered | Final |
| Closed | Confirmed resolved by customer | Final |
| Escalated | Escalated to senior/management | Running (separate escalation SLA) |

### 1.3 SLA Clock Rules

The response SLA clock runs from `created_at` to `first_response_at`.

**Clock starts:** Immediately at ticket creation (no grace period)
**Clock stops:** First substantive response from a NebulaTech engineer
**Auto-ACK:** System acknowledgment emails do NOT stop the SLA clock
**Pending pause:** When ticket moves to "Pending Customer" state, the clock pauses

---

## Chapter 2: Severity Classification Guide

### 2.1 Decision Matrix

Use this matrix to assign severity:

```
Is the system completely unavailable for ALL users?
  YES → L1 (Production Down)
  NO  → Continue...

Are CORE features unavailable for SOME users?
  YES → L2 (Serious Degradation)
  NO  → Continue...

Is there a moderate impact with a workaround?
  YES → L3 (Moderate Impact)
  NO  → L4 (Limited Impact)
```

### 2.2 L1 Qualifying Scenarios

**Must classify as L1:**
- All ticket submissions failing (server error or timeout)
- Authentication system down
- Customer portal returning 500 for all users
- Data loss occurring or imminent
- Payments processing failing

**Do NOT classify as L1:**
- Single user unable to access (investigate individual issue)
- Intermittent errors affecting < 10% of users
- Non-production/staging environment issues
- Scheduled maintenance (planned downtime)

### 2.3 L2 Qualifying Scenarios

**Must classify as L2:**
- Ticket search returning incorrect results (all users)
- Email notifications failing for 30%+ of users
- Critical workflow blocked (e.g., approval process)
- Dashboard timeouts affecting all users

**Borderline L2/L3 cases:**
- Email notifications failing for < 10% of users → L3
- Intermittent API failures (< 5% error rate) → L3

---

## Chapter 3: Ticket Data Format

### 3.1 JSON Ticket Schema

All tickets are stored in the standardised JSON format:

```json
{
  "ticket_id": "STRING — unique identifier, format: {BATCH}-{SEVERITY}-{TYPE}-{NNN}",
  "severity": "ENUM: L1|L2|L3|L4",
  "status": "ENUM: open|in_progress|resolved|closed",
  "created_at": "ISO8601: YYYY-MM-DDTHH:MM:SSZ",
  "first_response_at": "ISO8601: YYYY-MM-DDTHH:MM:SSZ",
  "resolved_at": "ISO8601: YYYY-MM-DDTHH:MM:SSZ",
  "response_minutes": "INTEGER: ceil((first_response_at - created_at) / 60)"
}
```

### 3.2 Ticket ID Conventions

Format: `{BATCH}-{SEVERITY}-{TYPE}-{NNN}`

Examples:
- `Q4-L1-BREACH-001` — Q4 batch, L1 ticket, SLA breach, first ticket
- `Q4-L2-OK-005` — Q4 batch, L2 ticket, within SLA, fifth ticket
- `Q1-L3-BREACH-003` — Q1 batch, L3 ticket, SLA breach, third ticket
- `Q4-L2-NEARV2-001` — Q4 batch, L2 ticket, near threshold under v2 policy

### 3.3 Timestamp Standards

All timestamps in NebulaTech ticket data:
- **Format:** ISO 8601, always UTC, always with 'Z' suffix
- **Pattern:** `YYYY-MM-DDTHH:MM:SSZ`
- **Example:** `2024-10-15T14:23:00Z`

Non-conforming formats cause validation errors:
- `2024-10-15 14:23:00` (space separator) → INVALID
- `2024-10-15T14:23:00+05:30` (non-UTC) → INVALID (must convert to UTC)
- `2024-10-15` (date only) → INVALID

### 3.4 response_minutes Calculation

```python
def calc_response_minutes(created_at: str, first_response_at: str) -> int:
    from datetime import datetime
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    t_created = datetime.strptime(created_at, fmt)
    t_first = datetime.strptime(first_response_at, fmt)
    delta = t_first - t_created
    return int(delta.total_seconds() / 60)  # floor division
```

---

## Chapter 4: SLA Breach Report Format

### 4.1 Breach Ticket Entry Format

Each entry in breach_tickets_*.json:

```json
{
  "ticket_id": "string",
  "severity": "L1|L2|L3|L4",
  "expected_response_min": "int (30|90|120|480|1440 depending on version)",
  "actual_response_min": "int",
  "breach_delta_min": "int — must equal actual - expected"
}
```

**Critical:** `breach_delta_min = actual_response_min - expected_response_min`
If this arithmetic does not close, the entry fails validation.

### 4.2 Compliance Summary Format

```json
{
  "schema_version": "1.0",
  "metadata": {
    "generated_at": "ISO8601",
    "agent_id": "string",
    "schema_version": "1.0"
  },
  "sla_policy_version": "v1|v2|v3",
  "batch": "2024Q4|2025Q1",
  "total_tickets": "int",
  "by_severity": {
    "L1": {
      "total_count": "int",
      "breach_count": "int",
      "compliance_rate": "float (2 decimal places)"
    }
  }
}
```

### 4.3 Patch Application Process

When applying a patch (tickets_patch_NNN.json):

1. For each patch entry, update the ticket record:
   - `first_response_at` → use `corrected_first_response_at`
   - `response_minutes` → use `corrected_response_minutes`
2. Re-evaluate SLA breach status for patched tickets
3. Regenerate breach report with suffix `_v{N+1}` (e.g., breach_tickets_Q4_v3.json)

---

## Chapter 5: Escalation Report Requirements

### 5.1 Mandatory Fields

The monthly escalation report (escalation_report_YYYY_MM.json) MUST include:

1. `metadata` block (generated_at, agent_id, schema_version)
2. `report_period` (YYYY-MM format)
3. `sla_policy_version` (exact version in force during period)
4. `breach_summary` (total + by_severity breakdown)
5. `top_breached_tickets` (top 5 worst breaches)
6. `credit_recommendations` (with source URLs)
7. `reviewer_signature` (empty string or name)

### 5.2 sla_policy_version Accuracy

The `sla_policy_version` field must reflect the policy version **in force during
the reporting period**, not the current version.

Example:
- November 2024 tickets → use `sla_matrix_v1.json` (in effect until 2025-02-01)
- `sla_policy_version: "v1"` (correct)
- `sla_policy_version: "v2"` (WRONG — v2 was not in effect in November 2024)

### 5.3 Credit Recommendation Format

```json
{
  "service": "atlassian_cloud | ec2 | lambda",
  "actual_uptime_pct": "float (2 decimal places)",
  "applicable_tier": "string — verbatim tier description",
  "credit_pct": "int",
  "source_url": "string — exact URL from official documentation"
}
```

Source URLs must be exact:
- Atlassian: `https://www.atlassian.com/legal/sla`
- EC2: `https://aws.amazon.com/ec2/sla/`
- Lambda: `https://aws.amazon.com/lambda/sla/`

---

## Chapter 6: SHA-256 Sign-off Procedure

### 6.1 Purpose

All final deliverable sets are signed with a SHA-256 digest to ensure integrity.
This provides an audit trail that the filed report matches what was computed.

### 6.2 Sign-off Format

The sign-off file (`output/signoff.txt`) contains exactly one line:

```
VERIFIED:<64-character lowercase hex SHA-256 digest>
```

Example:
```
VERIFIED:a3f2c1d4e5b6a7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3
```

### 6.3 Computing the Digest

**Method:** SHA-256 of all JSON output files (sorted by path), concatenated:

```python
import hashlib
from pathlib import Path
import json

def compute_signoff(output_dir: Path) -> str:
    json_files = sorted(output_dir.glob("*.json"))
    hasher = hashlib.sha256()
    for f in json_files:
        hasher.update(f.read_bytes())
    return "VERIFIED:" + hasher.hexdigest()
```

**IMPORTANT:** The digest must be computed by actually executing the script.
Hand-typed or placeholder hashes will not match and will fail validation.

---

*End of Ticket Operations Handbook*
"""


def _gen_audit_log(path: Path) -> None:
    """生成大型 SLA 违约审计日志（JSONL 格式，~15k tokens）。"""
    rng = random.Random(2024)
    severities = ["L1", "L2", "L3", "L4"]
    sla_map = {"L1": 30, "L2": 120, "L3": 480, "L4": 1440}

    lines = []
    base = datetime(2024, 1, 1, 8, 0, 0, tzinfo=timezone.utc)
    for i in range(300):
        sev = rng.choice(severities)
        sla = sla_map[sev]
        t = base + timedelta(days=rng.randint(0, 364), hours=rng.randint(0, 23), minutes=rng.randint(0, 59))
        # 30% breach
        if rng.random() < 0.30:
            resp = sla + rng.randint(5, 300)
            status = "BREACH"
        else:
            resp = rng.randint(5, sla - 1)
            status = "PASS"
        entry = {
            "audit_id": f"AUD-2024-{i+1:04d}",
            "ticket_id": f"HIST-{sev}-{i+1:04d}",
            "severity": sev,
            "created_at": _iso(t),
            "first_response_at": _iso(t + timedelta(minutes=resp)),
            "response_minutes": resp,
            "expected_response_min": sla,
            "sla_status": status,
            "breach_delta_min": max(0, resp - sla),
            "policy_version": "v1",
            "audited_at": _iso(t + timedelta(days=1)),
        }
        lines.append(json.dumps(entry, ensure_ascii=False))

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _gen_full_sop() -> str:
    """生成完整工单标准操作规程（~20k tokens）。"""
    # 生成一个详细的 SOP 文档，涵盖所有日常运营场景
    lines = ["# NebulaTech Support Operations — Full Standard Operating Procedure (SOP)\n"]
    lines.append("**Version:** 4.2 | **Date:** 2024-10-01 | **Owner:** Alice Wong\n")

    # 生成大量详细的操作步骤章节
    procedures = [
        ("P001", "L1 Incident Response", "L1", 30),
        ("P002", "L2 Ticket Triage", "L2", 120),
        ("P003", "L3 Standard Processing", "L3", 480),
        ("P004", "L4 Routine Handling", "L4", 1440),
        ("P005", "SLA Breach Escalation", "ALL", 0),
        ("P006", "Credit Claim Filing", "ALL", 0),
        ("P007", "Monthly Report Generation", "ALL", 0),
        ("P008", "Ticket Patch Processing", "ALL", 0),
        ("P009", "Policy Update Communication", "ALL", 0),
        ("P010", "Audit Trail Maintenance", "ALL", 0),
    ]

    sla_map = {"L1": 30, "L2": 120, "L3": 480, "L4": 1440}

    for proc_id, title, sev, sla in procedures:
        lines.append(f"\n## {proc_id}: {title}\n")
        lines.append(f"**Severity:** {sev} | **SLA Threshold:** {sla} min (if applicable)\n")
        if sev in sla_map:
            lines.append(f"\n### Trigger\nTicket created with severity {sev}. ")
            lines.append(f"SLA clock starts immediately. First response required within **{sla} minutes**.\n")
        lines.append("\n### Steps\n")
        for step_n in range(1, 16):
            lines.append(f"{step_n}. [Step {step_n} for {proc_id}] Perform standard check #{step_n}: "
                         f"verify ticket fields, check severity classification, confirm timestamps in "
                         f"ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ), validate response_minutes arithmetic.\n")
        lines.append(f"\n### Verification Checklist for {proc_id}\n")
        for check_n in range(1, 12):
            lines.append(f"- [ ] Verification item {check_n}: {'Confirmed' if check_n % 3 != 0 else 'Pending review'}\n")
        lines.append("\n### Common Errors\n")
        lines.append("- Timestamp not in UTC (must have 'Z' suffix)\n")
        lines.append("- response_minutes arithmetic mismatch\n")
        lines.append("- Wrong SLA threshold applied (check policy version)\n")
        lines.append(f"\n### Reference Documents\n")
        lines.append("- `policy/sla_matrix_v1.json` (current policy)\n")
        lines.append("- `reference/atlassian_sla_excerpt.md`\n")
        lines.append("- `docs/sla_compliance_audit_manual.md`\n")

    # 添加大量历史工单样例
    lines.append("\n## Appendix: Historical Ticket Samples\n")
    lines.append("The following samples illustrate correct ticket formats for training purposes.\n")
    rng = random.Random(9999)
    severities = ["L1", "L2", "L3", "L4"]
    sla_thresholds = {"L1": 30, "L2": 120, "L3": 480, "L4": 1440}
    base_dt = datetime(2024, 6, 1, 9, 0, 0, tzinfo=timezone.utc)

    for sample_n in range(1, 151):
        sev = rng.choice(severities)
        sla = sla_thresholds[sev]
        t = base_dt + timedelta(days=rng.randint(0, 150), hours=rng.randint(0, 23))
        if rng.random() < 0.25:
            resp = sla + rng.randint(5, 200)
            status = "BREACH"
        else:
            resp = rng.randint(5, max(5, sla - 2))
            status = "PASS"
        lines.append(f"\n### Sample Ticket {sample_n:03d}\n")
        lines.append(f"```json\n")
        sample = {
            "ticket_id": f"SAMPLE-{sev}-{sample_n:03d}",
            "severity": sev,
            "status": "resolved",
            "created_at": _iso(t),
            "first_response_at": _iso(t + timedelta(minutes=resp)),
            "resolved_at": _iso(t + timedelta(minutes=resp + rng.randint(60, 2880))),
            "response_minutes": resp,
            "sla_status": status,
            "expected_response_min": sla,
            "breach_delta_min": max(0, resp - sla),
        }
        lines.append(json.dumps(sample, ensure_ascii=False, indent=2))
        lines.append("\n```\n")
        lines.append(f"**Analysis:** Severity {sev}, SLA = {sla} min, actual = {resp} min → **{status}**\n")

    lines.append("\n---\n*End of Full SOP*\n")
    return "".join(lines)


def _gen_v2_impact_analysis() -> str:
    """生成 v2 政策影响分析报告（~30k tokens）。"""
    lines = []
    lines.append("# SLA Policy v2 Impact Analysis Report\n")
    lines.append("**Prepared by:** Support Operations Team\n")
    lines.append("**Date:** 2025-02-01\n")
    lines.append("**Subject:** Impact Analysis of L2 Response Time Change (120min → 90min)\n\n")

    lines.append("""## Executive Summary

This document analyses the operational impact of tightening the L2 response time SLA
from 2 hours (120 minutes) to 90 minutes under `sla_matrix_v2.json`, effective 2025-02-01.

**Key Finding:** The change from L2=120min to L2=90min will reclassify tickets whose
actual response time falls between 91 and 120 minutes from "compliant" to "breach" status.
This analysis quantifies this impact using historical Q4 2024 data.

**IMPORTANT:** This analysis is prepared for the Q7 round of analysis. At this point,
`sla_matrix_v2.json` is in force. However, a subsequent management notice (FEISHU-PRD4-L2-REVERT)
may supersede this change. Always check for the most recent policy update before applying.

---

## Section 1: Policy Change Summary

### 1.1 Change Details

| Field | Old Value (v1) | New Value (v2) | Delta |
|---|---|---|---|
| L2 response_minutes | 120 | **90** | -30 minutes |
| L2 coverage | 24/7 | 24/7 | Unchanged |
| All other levels | Unchanged | Unchanged | — |

### 1.2 Rationale

The tightening of the L2 SLA from 2 hours to 90 minutes was approved as part of
NebulaTech's customer commitment upgrade program (Q4 2024 roadmap item #17).

Rationale:
- Customer satisfaction surveys indicated L2 responses between 90-120 minutes
  were perceived as "slow" by 73% of affected customers
- Competitive analysis shows most Enterprise-tier competitors have L2 SLAs ≤ 90 minutes
- Support team capacity analysis (September 2024) indicated 90-minute compliance
  was achievable at 94% rate with current staffing

---

## Section 2: Q4 2024 Historical Impact Analysis

### 2.1 Tickets in the 91-120 Minute Range (L2 Only)

Under v1 (L2=120min), tickets with L2 response between 91-120 minutes were COMPLIANT.
Under v2 (L2=90min), these same tickets become BREACHED.

The following Q4 2024 L2 tickets are affected by this reclassification:

| Ticket ID | Created | Response (min) | v1 Status | v2 Status |
|---|---|---|---|---|
| Q4-L2-NEARV2-001 | (see batch file) | 91-119 | PASS | BREACH |
| Q4-L2-NEARV2-002 | (see batch file) | 91-119 | PASS | BREACH |
| Q4-L2-NEARV2-003 | (see batch file) | 91-119 | PASS | BREACH |

**Impact on Q4 L2 Breach Count:**
- Under v1: 8 L2 breaches (response > 120 min)
- Under v2: 11 L2 breaches (response > 90 min; includes the 3 near-threshold tickets)
- Net increase: **+3 breach tickets** due to threshold tightening

**Impact on Q4 Total Breach Count:**
- Under v1: 28 total breaches
- Under v2: 31 total breaches

### 2.2 Compliance Rate Impact

| Metric | v1 (L2=120min) | v2 (L2=90min) | Change |
|---|---|---|---|
| Q4 Total breaches | 28 | 31 | +3 |
| Q4 L2 compliance | 86.78% (48/55 compliant) | 81.82% (45/55 compliant) | -4.96% |
| Q4 Overall compliance | 86.00% | 84.50% | -1.50% |

### 2.3 Forward-Looking Q1 2025 Analysis

For Q1 2025 tickets, the v2 threshold applies from the start of the quarter.
Estimated Q1 L2 compliance under v2: see breach_tickets_Q1.json after analysis.

---

## Section 3: Operational Impact Assessment

### 3.1 Staffing Requirements

Based on Q4 2024 data, achieving 90-minute L2 response at 95% compliance rate requires:

| Shift | Current Coverage | Required Coverage | Gap |
|---|---|---|---|
| Business hours (09:00-18:00) | 8 engineers | 8 engineers | None |
| Evening (18:00-00:00) | 3 engineers | 5 engineers | -2 |
| Overnight (00:00-09:00) | 2 engineers | 4 engineers | -2 |
| Weekend days | 4 engineers | 6 engineers | -2 |
| Weekend nights | 1 engineer | 3 engineers | -2 |

**Staffing gap:** 8 additional FTE-equivalent coverage slots required.

**NOTE:** This gap analysis is the basis for the subsequent management decision
to revert the L2 change (ref: FEISHU-PRD4-L2-REVERT). The 90-minute target
could not be met with existing staffing levels.

### 3.2 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| L2 breach rate increase | High (due to staffing gap) | High (SLA penalties) | Revert to 120min |
| Customer dissatisfaction at 90min target | Low | Medium | Monitor CSAT |
| Escalation rate increase | Medium | Medium | Auto-escalation at 75min |

---

## Section 4: Detailed Ticket Analysis by Severity

### 4.1 L1 Tickets (Q4 2024 — No Change Under v2)

L1 threshold remains 30 minutes. All L1 analysis unchanged.

| Metric | Q4 2024 Value |
|---|---|
| Total L1 tickets | 50 (approx.) |
| L1 breaches | 10 |
| L1 compliance rate | 80.00% |
| Worst L1 breach (min) | 87-90 min (approx.) |

### 4.2 L2 Tickets (Q4 2024 — Affected by v2)

| Category | Count | Notes |
|---|---|---|
| L2 breaches under v1 (>120min) | 8 | Clear breaches regardless of version |
| L2 near-threshold (91-120min) | 3 | Compliant under v1; breach under v2 |
| L2 compliant under v2 (<91min) | 45 | Compliant under both versions |
| **Total L2 breaches under v2** | **11** | |

### 4.3 L3 Tickets (Q4 2024 — No Change Under v2)

L3 threshold remains 480 minutes (8 hours).

| Metric | Q4 2024 Value |
|---|---|
| Total L3 tickets | 56 (approx.) |
| L3 breaches | 6 |
| L3 compliance rate | 89.29% |

### 4.4 L4 Tickets (Q4 2024 — No Change Under v2)

L4 threshold remains 1440 minutes (24 hours).

| Metric | Q4 2024 Value |
|---|---|
| Total L4 tickets | 43 (approx.) |
| L4 breaches | 4 |
| L4 compliance rate | 90.70% |

---

## Section 5: Q1 2025 Forward Projection (Under v2)

### 5.1 Expected Breach Counts

Based on Q4 2024 patterns and staffing constraints:

| Severity | Q1 Total (est.) | Q1 Breach (est.) | Rate |
|---|---|---|---|
| L1 | 45 | 5 | 88.89% |
| L2 | 55 | 10-12 | 78-82% |
| L3 | 30 | 4 | 86.67% |
| L4 | 20 | 3 | 85.00% |

### 5.2 Year-over-Year Comparison

| Quarter | Total Tickets | Total Breaches | Compliance |
|---|---|---|---|
| Q3 2024 (v1) | 185 | 22 | 88.11% |
| Q4 2024 (v1) | 200 | 28 | 86.00% |
| Q1 2025 (v2) | 150 | ~22 | ~85.33% |

---

## Appendix A: Per-Ticket Analysis Detail (Q4 2024 L2)

The following lists all Q4 2024 L2 tickets with their response times and
status under both v1 and v2 policies:

### L2 Breach Tickets Under v1 (>120 min)
""")
    # 生成 L2 违约工单详细分析表格（增加体量）
    rng_detail = random.Random(12345)
    for i in range(8):
        resp = rng_detail.randint(125, 240)
        lines.append(f"| Q4-L2-BREACH-{i+1:03d} | {resp} | BREACH (v1) | BREACH (v2) | delta={resp-120} (v1), delta={resp-90} (v2) |\n")

    lines.append("\n### L2 Near-Threshold Tickets (91-120 min)\n")
    for i in range(3):
        resp = rng_detail.randint(91, 119)
        lines.append(f"| Q4-L2-NEARV2-{i+1:03d} | {resp} | PASS (v1) | BREACH (v2) | delta=N/A (v1), delta={resp-90} (v2) |\n")

    lines.append("\n### L2 Compliant Tickets Under Both Policies (<91 min)\n")
    for i in range(45):
        resp = rng_detail.randint(10, 89)
        lines.append(f"| Q4-L2-OK-{i+1:03d} | {resp} | PASS (v1) | PASS (v2) | |\n")

    lines.append("""
---

## Appendix B: Policy Version Comparison Table

| Field | v0 (ARCHIVED) | v1 (Effective 2024-01-01) | v2 (Effective 2025-02-01) | v2-reverted |
|---|---|---|---|---|
| L1 response | 60 min (ERROR) | **30 min** | 30 min | 30 min |
| L2 response | 120 min | 120 min | **90 min** | **120 min (reverted)** |
| L3 response | 480 min | 480 min | 480 min | 480 min |
| L4 response | 1440 min | 1440 min | 1440 min | 1440 min |
| L2 coverage | 24/7 | 24/7 | 24/7 | 24/7 |

Notes:
- v0 L1=60min was an ERROR. Do not reference v0 for any current analysis.
- v2 L2=90min was approved but subsequently REVERTED by management notice FEISHU-PRD4-L2-REVERT.
- After the revert, L2=120min (same as v1) applies.

---

## Appendix C: SLA Calculation Reference Tables

### Response Time Thresholds (All Versions)

| Severity | v1 | v2 | v2-reverted |
|---|---|---|---|
| L1 | 30 | 30 | 30 |
| L2 | **120** | **90** | **120** |
| L3 | 480 | 480 | 480 |
| L4 | 1440 | 1440 | 1440 |

### Credit Tiers (Atlassian Enterprise — Unchanged Across All Versions)

| Uptime | Credit |
|---|---|
| 99.90%–99.95% | 5% |
| 99.00%–99.90% | 10% |
| 95.00%–99.00% | 25% |
| < 95.00% | 50% |

---

## Appendix D: Staffing Analysis Detail

### Current vs Required Coverage (per 4-hour block)

| Time Block | Day | Current | Required | Gap |
|---|---|---|---|---|
| 00:00-04:00 | Mon-Fri | 2 | 4 | -2 |
| 04:00-08:00 | Mon-Fri | 2 | 3 | -1 |
| 08:00-12:00 | Mon-Fri | 8 | 8 | 0 |
| 12:00-16:00 | Mon-Fri | 8 | 8 | 0 |
| 16:00-20:00 | Mon-Fri | 5 | 7 | -2 |
| 20:00-24:00 | Mon-Fri | 3 | 5 | -2 |
| 00:00-12:00 | Sat-Sun | 2 | 4 | -2 |
| 12:00-24:00 | Sat-Sun | 2 | 4 | -2 |

**Total coverage gap: equivalent to 8-10 additional FTEs**

Conclusion: Without additional hiring or shift adjustments, the 90-minute L2 SLA
target is not achievable at the required 95% compliance rate. This is the primary
driver for the management decision to revert L2 to 120 minutes.

---

*End of SLA Policy v2 Impact Analysis Report*
*Prepared by: Support Operations Team, NebulaTech*
""")
    return "".join(lines)


def _gen_l2_revert_analysis() -> str:
    """生成 L2 恢复分析报告（~30k tokens）。"""
    lines = []
    lines.append("# L2 SLA Revert Impact Analysis and Post-Revert Operations Guide\n")
    lines.append("**Prepared by:** Dave Park (Compliance) + Alice Wong (Support Ops)\n")
    lines.append("**Date:** 2026-04-06\n")
    lines.append("**Subject:** Impact of reverting L2 from 90 min back to 120 min\n\n")
    lines.append("**Ref:** FEISHU-PRD4-L2-REVERT\n\n")

    lines.append("""## 1. Background

Following the issuance of management notice FEISHU-PRD4-L2-REVERT on 2026-04-06,
the L2 response SLA has been reverted from 90 minutes (introduced in sla_matrix_v2,
effective 2025-02-01) back to 120 minutes (the original Atlassian Enterprise baseline).

This document:
1. Explains the supersede chain and the authoritative interpretation
2. Provides re-analysis guidance for Q4 2024 breach calculations
3. Documents the data patch requirements (tickets_patch_001.json)
4. Provides the final v3 breach analysis methodology

---

## 2. Supersede Chain Summary

The following sequence of policy changes applies:

```
[v1] L2 = 120 min (effective 2024-01-01)
  ↓ superseded by:
[v2] L2 = 90 min (effective 2025-02-01, via sla_matrix_v2.json)
  ↓ superseded by:
[FEISHU-PRD4-L2-REVERT] L2 = 120 min (effective immediately, via feishu notice)
```

**Current status:** L2 = 120 minutes. The v2 change has been superseded.

**Key principle:** When calculating SLA compliance, use the policy version in force
AT THE TIME OF THE TICKET CREATION, not the current policy version.

Since all Q4 2024 and Q1 2025 tickets were created before the v2 update (2025-02-01),
they should use v1 (L2=120min) for the primary analysis.
After FEISHU-PRD4-L2-REVERT, revert any v2-based analyses back to 120min.

---

## 3. Data Patch Application (tickets_patch_001.json)

Simultaneously with the L2 revert, `tickets_patch_001.json` corrects 15 tickets
in the Q4 2024 batch that had data entry errors in `first_response_at`.

### 3.1 Patch Summary

- 15 tickets patched
- 5 tickets corrected from breach → compliant status
- 10 tickets have corrected timestamps but remain in breach

### 3.2 Patched Ticket Analysis

After applying patches:

| Category | Before Patch | After Patch | Delta |
|---|---|---|---|
| Q4 Total breaches (v1/v3) | 28 | 23 | -5 |
| Q4 Total tickets | 200 | 200 | 0 |
| Q4 Compliance rate | 86.00% | 88.50% | +2.50% |

### 3.3 Breach Tickets v3 Format

The output `breach_tickets_Q4_v3.json` must:
1. Apply the data corrections from tickets_patch_001.json
2. Use L2=120min (v3/reverted — same as v1)
3. Recalculate breach status for all 15 patched tickets
4. Include only tickets that REMAIN in breach after patches

---

## 4. Q4 v3 Expected Breach Counts

After applying both the L2 revert (back to 120min) and the data patch:

| Severity | Total Tickets | Breaches (v1, pre-patch) | After Patch (v3) |
|---|---|---|---|
| L1 | ~50 | 10 | 5 (5 were data errors, now corrected) |
| L2 | ~55 | 8 | 8 (no patch corrections apply to L2 breaches >120min) |
| L3 | ~56 | 6 | 6 |
| L4 | ~43 | 4 | 4 |
| **Total** | **200** | **28** | **23** |

Note: The 5 corrections are from the first 5 entries in tickets_patch_001.json.
Verify the exact ticket IDs against the patch file.

---

## 5. Validation Requirements for v3 Analysis

### 5.1 script validate_ticket_sla.py

Use `scripts/validate_ticket_sla.py` to validate breach_tickets_Q4_v3.json:

```bash
python scripts/validate_ticket_sla.py output/breach_tickets_Q4_v3.json
```

Expected output structure:
```json
{
  "validated_count": <int>,
  "error_count": 0,
  "invalid_ticket_ids": []
}
```

- `validated_count + error_count = total tickets in breach file`
- `error_count` should be 0 if all patches applied correctly

### 5.2 Arithmetic Closure Checks

For each breach ticket entry:
- `breach_delta_min = actual_response_min - expected_response_min`
- `expected_response_min` for L2 tickets = **120** (NOT 90)
- `actual_response_min` must match the corrected value from patch where applicable

---

## 6. Combined Summary Impact

### 6.1 Effect on Q10 Combined Breach Summary

After all corrections and reverts, the combined Q4+Q1 summary must reflect:

| Metric | Value |
|---|---|
| Q4 total tickets | 200 |
| Q4 breaches (v3, post-patch) | 23 |
| Q1 total tickets | 150 |
| Q1 breaches (v1 = same as v3) | 19 |
| **Combined total tickets** | **350** |
| **Combined total breaches** | **42** |
| **Combined breach_pct** | **12.00%** |

### 6.2 Effect on November 2024 Monthly Report

The formal escalation report for November 2024 covers only the Q4 batch tickets
from that month. The exact ticket count and breach count will differ from the full
Q4 batch totals. See `reports/monthly_sla_report_2024_11.md` for the November subset.

---

## 7. Policy Update Communication History

### 7.1 Official Communication Log

| Date | From | To | Subject | Key Message |
|---|---|---|---|---|
| 2025-02-01 | Alice Wong | All Support | sla_matrix_v2 effective | L2 changes to 90min |
| 2026-04-02 | Alice Wong | Bob Chen (DM) | L2 proposal discussion | Still proposal, use v1 |
| 2026-04-06 | Dave Park | Feishu group | FEISHU-PRD4-L2-REVERT | L2 reverts to 120min |

### 7.2 Session Evidence References

| Session | Ref | Content |
|---|---|---|
| Slack DM Alice-Bob | 2026-04-02T14:35Z | Alice confirms v1 applies until v2 officially issued |
| Feishu #support-ops-management | FEISHU-PRD4-L2-REVERT | Official revert notice |

---

## Appendix A: Full Comparison Table — v1/v2/v3

| Field | v0 (ARCHIVED) | v1 | v2 (interim) | v3/reverted |
|---|---|---|---|---|
| L1 | 60 min ERROR | 30 min | 30 min | **30 min** |
| L2 | 120 min | 120 min | 90 min (superseded) | **120 min** |
| L3 | 480 min | 480 min | 480 min | **480 min** |
| L4 | 1440 min | 1440 min | 1440 min | **1440 min** |
| Status | ARCHIVED | Superseded by v2 | Superseded by revert | **CURRENT** |

---

## Appendix B: Re-analysis Checklist

For engineers re-running breach analysis after the L2 revert:

- [ ] Confirm you have read FEISHU-PRD4-L2-REVERT notice
- [ ] Confirm L2 threshold = 120 min (not 90 min)
- [ ] Apply tickets_patch_001.json corrections before running analysis
- [ ] For each patched ticket, use corrected_response_minutes (not original)
- [ ] Re-evaluate breach status for all 15 patched tickets
- [ ] Output breach_tickets_Q4_v3.json (not _v2)
- [ ] Verify: total_tickets_in_v3 = correct count (not all 200)
- [ ] Verify arithmetic: breach_delta_min = actual - expected for each entry

---

## Appendix C: tickets_patch_001 Application Worked Example

### Original Ticket (before patch)

```json
{
  "ticket_id": "Q4-L1-BREACH-001",
  "severity": "L1",
  "created_at": "2024-10-01T08:00:00Z",
  "first_response_at": "2024-10-01T08:40:00Z",
  "response_minutes": 40,
  "sla_threshold": 30
}
```

### Patch Entry

```json
{
  "ticket_id": "Q4-L1-BREACH-001",
  "patch_reason": "data_entry_correction",
  "original_first_response_at": "2024-10-01T08:40:00Z",
  "corrected_first_response_at": "2024-10-01T08:25:00Z",
  "original_response_minutes": 40,
  "corrected_response_minutes": 25
}
```

### After Patch Application

```json
{
  "ticket_id": "Q4-L1-BREACH-001",
  "severity": "L1",
  "created_at": "2024-10-01T08:00:00Z",
  "first_response_at": "2024-10-01T08:25:00Z",
  "response_minutes": 25,
  "sla_threshold": 30,
  "sla_status": "PASS"  // Was BREACH before patch
}
```

This ticket is now COMPLIANT (25 min < 30 min threshold) and should be EXCLUDED
from breach_tickets_Q4_v3.json.

---

*End of L2 SLA Revert Impact Analysis*
*Reference: FEISHU-PRD4-L2-REVERT*
*Next review: Upon next policy update*
""")
    # 添加更多内容以确保体量
    lines.append("\n## Appendix D: Historical Ticket Impact Traces\n")
    lines.append("The following traces document the analysis path for key tickets across all policy versions.\n\n")
    rng_trace = random.Random(54321)
    sev_list = ["L1", "L2", "L3", "L4"]
    sla_v1 = {"L1": 30, "L2": 120, "L3": 480, "L4": 1440}
    sla_v2_map = {"L1": 30, "L2": 90, "L3": 480, "L4": 1440}
    base_trace = datetime(2024, 10, 1, 8, 0, 0, tzinfo=timezone.utc)
    for trace_n in range(1, 101):
        sev = rng_trace.choice(sev_list)
        resp = rng_trace.randint(20, 200)
        t = base_trace + timedelta(days=rng_trace.randint(0, 89), hours=rng_trace.randint(0, 23))
        v1_status = "BREACH" if resp > sla_v1[sev] else "PASS"
        v2_status = "BREACH" if resp > sla_v2_map[sev] else "PASS"
        lines.append(f"### Trace {trace_n:03d}: {sev} ticket, response={resp}min\n")
        lines.append(f"- Created: {_iso(t)}\n")
        lines.append(f"- Response: {resp} minutes\n")
        lines.append(f"- v1 ({sla_v1[sev]}min threshold): **{v1_status}**\n")
        lines.append(f"- v2 ({sla_v2_map[sev]}min threshold): **{v2_status}**\n")
        lines.append(f"- v3 ({sla_v1[sev]}min threshold, same as v1): **{v1_status}**\n")
        if v1_status != v2_status:
            lines.append(f"  → This ticket changes status between v1 and v2!\n")
        lines.append("\n")

    lines.append("---\n*End of Appendix D*\n")
    return "".join(lines)


def _gen_aws_guide() -> str:
    """生成 AWS SLA 参考指南（~10k tokens）。"""
    return """\
# AWS SLA Reference Guide for NebulaTech

## Overview

This guide summarises AWS SLA terms relevant to NebulaTech's infrastructure.
NebulaTech uses Amazon EC2 (us-east-1, us-west-2) and AWS Lambda for backend services.

---

## Amazon EC2 SLA

**Source:** https://aws.amazon.com/ec2/sla/

### Availability Commitments

| Level | Monthly Uptime Percentage |
|---|---|
| Region Level (multi-AZ) | **99.99%** |
| Instance Level | **99.5%** |

### Service Credit Schedule

| Monthly Uptime Percentage | Service Credit |
|---|---|
| 99.0% – 99.99% | **10%** |
| 95.0% – 99.0% | **30%** |
| < 95.0% | **100%** |

Both Region-Level and Instance-Level SLAs use the same credit schedule.

### Automatic Credit

AWS automatically provides service credits when an EC2 instance is unavailable
for more than **6 minutes** within a single clock hour. No claim is required for
this automatic credit.

### Claim Deadline

For service credits requiring a claim: submit before the **end of the second
billing cycle after the month** in which the outage occurred.

Example calculation:
- Outage month: November 2024 (billing cycle: December 2024)
- Second billing cycle: January 2025
- Claim deadline: **2025-01-31**

### Credit Calculation Example

Scenario: EC2 Region Level, monthly uptime = 98.5%

```
Uptime: 98.5% falls in range [95.0%, 99.0%)
Credit tier: 30%
Monthly EC2 cost: $8,500
Credit amount: $8,500 × 30% = $2,550.00
Claim deadline: end of second billing cycle after incident
```

---

## AWS Lambda SLA

**Source:** https://aws.amazon.com/lambda/sla/

### Availability Commitment

Monthly Uptime Percentage: **99.95%** per region

### Error Definition

An "Error" for Lambda SLA purposes is:
- HTTP status code **500** (Internal Server Error)
- HTTP status code **503** (Service Unavailable)

**Exclusion:** Custom status codes generated by function code are **NOT** counted
as Lambda errors for SLA purposes, even if they indicate a function-level failure.

### Measurement Interval

Availability is calculated per **5-minute interval**. If within any 5-minute period
the error rate exceeds the threshold, that interval is counted as unavailable.

### Service Credit Schedule

| Monthly Uptime Percentage | Service Credit |
|---|---|
| 99.0% – 99.95% | **10%** |
| 95.0% – 99.0% | **25%** |
| < 95.0% | **100%** |

Note: Minimum credit balance is $1 USD.

### Credit Calculation Example

Scenario: Lambda, monthly uptime = 97.2%

```
Uptime: 97.2% falls in range [95.0%, 99.0%)
Credit tier: 25%
Monthly Lambda cost: $1,200
Credit amount: $1,200 × 25% = $300.00
```

---

## AWS Support Plans

**Source:** https://aws.amazon.com/premiumsupport/plans/

### Response Times by Severity (Enterprise Plan)

| Severity | Definition | Response Time |
|---|---|---|
| Critical | Business-critical system down | **< 15 minutes** |
| Urgent | Production system down | < 1 hour |
| High | Production system impaired | < 4 hours |
| Normal | System impaired | < 12 hours |
| Low | General guidance | < 24 hours |

**AWS Support API Severity Codes (verbatim):**

Source: https://docs.aws.amazon.com/awssupport/latest/APIReference/API_SeverityLevel.html

| code | name |
|---|---|
| `critical` | Business-critical system down |
| `urgent` | Production system down |
| `high` | Production system impaired |
| `normal` | System impaired |
| `low` | General guidance |

Valid code values: `low | normal | high | urgent | critical`

---

## SLA Comparison: Atlassian vs AWS vs GCP

| Vendor | P1/L1/Critical Response | Uptime Commitment | Key Source |
|---|---|---|---|
| Atlassian Enterprise | 30 min (24/7) | 99.95% | https://www.atlassian.com/legal/sla |
| AWS Enterprise | 15 min | (per service) | https://aws.amazon.com/premiumsupport/plans/ |
| GCP Premium | 15 min | (per service) | https://cloud.google.com/terms/tssg |

### Atlassian Premium vs Enterprise

| Metric | Premium | Enterprise |
|---|---|---|
| Uptime commitment | **99.90%** | **99.95%** |
| L1 response | 1 hour (24/7) | **30 min (24/7)** |
| L2 response | 2 hours (24/5) | 2 hours (24/7) |
| Credit 99.90–99.95% | NOT available | **5%** (exclusive) |
| Credit 99.00–99.90% | 10% | 10% |
| Credit 95.00–99.00% | 25% | 25% |
| Credit < 95.00% | 50% | 50% |

---

## NebulaTech Infrastructure SLA Summary (2024)

| Service | Region | Monthly Uptime Target | SLA Source |
|---|---|---|---|
| Atlassian JSM Cloud | Global (Atlassian-managed) | 99.95% | https://www.atlassian.com/legal/sla |
| Amazon EC2 (us-east-1) | US East | 99.99% (region-level) | https://aws.amazon.com/ec2/sla/ |
| AWS Lambda (us-east-1) | US East | 99.95% | https://aws.amazon.com/lambda/sla/ |
| AWS RDS (us-east-1) | US East | 99.95% | (separate SLA) |

---

*This document is maintained by the DevOps team and reviewed quarterly.*
*For questions: infrastructure@nebulatech.com*
"""


# ─── main ─────────────────────────────────────────────────────────────────────
def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()
    gen_policy_files()
    ticket_stats = gen_tickets()
    gen_reports()
    gen_reference()
    gen_scripts()
    gen_bulk_docs()
    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids, ticket_stats)

    desc = (
        "NebulaTech 客服工单升级与 SLA 合规分析 — 17 exec_check 轮，2 次 update（含 L2 supersede），"
        "5 条 preference 规则 P1-P5，难度向量 V1/V2/V4/V5/V6/V7/V8/V9/V10。"
        "真实来源：Atlassian Cloud SLA (https://www.atlassian.com/legal/sla)；"
        "Atlassian Support Offerings (https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html)；"
        "AWS Support Plans (https://aws.amazon.com/premiumsupport/plans/)；"
        "AWS EC2 SLA (https://aws.amazon.com/ec2/sla/)；"
        "AWS Lambda SLA (https://aws.amazon.com/lambda/sla/)；"
        "Google Cloud TSSG (https://cloud.google.com/terms/tssg)。"
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
    sess_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in SESS.glob("*.jsonl")
    )
    upd_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in UPD.rglob("*") if p.is_file()
    )
    print(f"[prd4] workspace tokens ~{total:,} | sessions ~{sess_tok:,} | updates ~{upd_tok:,}")
    print(f"[prd4] Q4 breach stats: {ticket_stats['q4_breach_v1']} (v1), {ticket_stats['q4_breach_v2']} (v2)")
    print(f"[prd4] built at {DATASET}")


if __name__ == "__main__":
    main()
