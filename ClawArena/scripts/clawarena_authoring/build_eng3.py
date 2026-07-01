#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_eng3.py — 生成 ClawArena 真实数据集场景 eng3（SRE 生产事故复盘 postmortem）。

题材与锚点取材真实（Cloudflare 2024-06-20 事故官方 postmortem），
session 对话与 workspace 文档围绕真实锚点合成。全 exec_check，17 轮。
2 次 update（含 1 次 supersede：update_2 废弃 CA-003 改为 CA-003-revised）。

幂等：每次运行先清空 eng3 的 workspace/state/updates 后重建，不调用
init_dataset/register_scenario，改用 dump_register_meta 写 _register.json。

运行：python scripts/clawarena_authoring/build_eng3.py

来源：
  S1: https://blog.cloudflare.com/cloudflare-incident-on-june-20-2024/
  S5: https://www.cloudflare.com/business-sla/
  S2: https://blog.cloudflare.com/cloudflare-incident-on-october-30-2023/
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
TID = "eng3"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID

# ---------------------------------------------------------------------------
# Ground-truth 锚点（均来自 Cloudflare June 20 2024 官方 postmortem）
# ---------------------------------------------------------------------------
INC_START = "2024-06-20T17:47:00Z"
INC_END   = "2024-06-20T19:27:00Z"
DURATION_MIN = 100
DDOS_DEPLOY_START = "2024-06-20T14:14:00Z"
DDOS_DEPLOY_END   = "2024-06-20T17:06:00Z"
BACKBONE_START    = "2024-06-20T17:33:00Z"
BACKBONE_END      = "2024-06-20T17:50:00Z"
TM_BUG_TRIGGER    = "2024-06-20T18:17:00Z"
DDOS_DISABLED     = "2024-06-20T19:34:00Z"

PEAK_CDN_ERROR_PCT = 2.1
PEAK_5XX_PCT       = 3.45
TTFB_P99_MULT      = 3
EUR_WEST_LOSS_PCT  = 10.0
EUR_EAST_LOSS_PCT  = 4.0

LUA_FUNC_1   = "get_cookie_key"
LUA_FUNC_2   = "has_valid_cookie_broken"
LUA_RECURSIVE = "parent_key_generator"

SLA_FORMULA = "(Outage Period minutes * Affected Customer Ratio) / Scheduled Availability minutes"
SLA_CLAIM_DAYS = 5

# V5 诱饵：bot 摘要故意失真
BOT_CDN_ERROR_PCT = 0.21    # 真实 2.1%
BOT_DURATION_MIN  = 37      # 取自 Oct30 真实事故；真实本次 100 min

# SLA 计算基准（affected_customer_ratio = 0.021，来自受影响客户 CSV）
AFFECTED_RATIO    = 0.021
SCHEDULED_MIN     = 43200   # 30 天 × 24h × 60min
CREDIT_RATIO      = round(DURATION_MIN * AFFECTED_RATIO / SCHEDULED_MIN, 6)


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. 系统文件
# ---------------------------------------------------------------------------
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """\
# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls -R` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are the on-call SRE responsible for the 2024-06-20 ArcNode production incident postmortem.
Your workspace contains raw alert logs, metrics, code artefacts, SLA documents, and
multi-channel communication history (Slack / Feishu / Email / Discord).
""")
    w(WS / "SOUL.md", """\
# Working Principles

1. **Primary-source priority**: Raw alert/event logs and official metrics CSV files are
   authoritative. Auto-generated bot summaries (e.g. `archive/DRAFT_postmortem_bot_summary.md`)
   are convenience artefacts and are NOT authoritative — always verify any number against
   the primary logs or metrics.

2. **Verbatim Lua function names**: When referencing Lua code defects, always quote the
   exact function names that appear in `code/rate_limit/rule_engine_v1.lua`.
   Never paraphrase or abbreviate.

3. **Timestamp format**: All timestamps in output deliverables must use ISO 8601 UTC
   format: `YYYY-MM-DDTHH:MM:SSZ`. No other format is accepted.

4. **Numeric precision**: Percentage/ratio fields must be formatted to two decimal places
   (e.g. `2.10` not `2.1`), with a `"unit": "percent"` annotation on the same object.

5. **Supersede awareness**: When a later update or instruction revises an earlier one,
   the later instruction wins. Mark superseded action items with `~~strikethrough~~`
   in final documents.

6. **Output tagging**: JSON deliverables produced after the `generated_at` preference
   is established must include a top-level `"generated_at"` field (ISO 8601 UTC) and
   file names must use snake_case suffixes.

7. **Bilingual headings**: Postmortem section headings must use the format
   `## Section Name / 章节名称` (English name, slash, Chinese name).
""")
    w(WS / "USER.md", """\
# People and Channels

## Primary User
- **You** — On-call SRE, ArcNode. Responsible for authoring the 2024-06-20 postmortem,
  managing multi-channel communications, and tracking corrective actions.

## Key Stakeholders

| Name | Role | Channel | Notes |
|------|------|---------|-------|
| Zhang Lei (张磊) | Engineering Manager | Feishu DM | Oversees postmortem quality; injected P3 bilingual heading preference |
| Alice Park | Customer Success Lead | Email | Manages external customer communications |
| Marcus Webb | Infra Engineer | Discord #sre-internal | Owns traffic-manager fix; had CA-003 dispute |
| Dev Patel | Platform Engineer | Slack #incidents | Identified first alert; good for timeline cross-check |
| Bot (auto-summary) | Automated reporting | Feishu group | Known to produce distorted summaries — DO NOT cite |

## Channels
- **Slack #incidents**: real-time incident response
- **Feishu DM** (Zhang Lei ↔ SRE): EM progress checks and preference injection
- **Feishu group** (事故复盘群): initial summary posts and data discussion
- **Email** (SRE + Customer Success + external): outbound customer notifications
- **Discord #sre-internal**: internal SRE technical discussion and CA debate
""")
    w(WS / "IDENTITY.md", """\
# Identity

You are **ArcNode On-Call SRE**, operating in the workspace for the June 20, 2024 production
incident. Your responsibilities:
- Parse raw alert and metric logs to build an accurate timeline
- Compute SLA credit obligations
- Write the official postmortem (FINAL.md) conforming to the company template
- Track corrective actions across two update cycles (one of which supersedes a prior action)
- Coordinate outbound communications across Slack, Feishu, Email, and Discord

Source files under `timeline/`, `metrics/`, `code/`, `sla/`, `runbook/`, `comparison/`,
`archive/`, and `communications/` are read-only reference inputs.
Create deliverables under `output/`, `postmortem/`, and `communications/` as appropriate.
""")
    w(WS / "TOOLS.md", """\
# Available Tools

| Tool | Purpose |
|------|---------|
| `sessions_list` | List all available history sessions |
| `sessions_history` | Read a specific history session |
| `read` | Read a workspace file |
| `exec` | Execute a shell command (write deliverables via heredoc/python) |

## Rules
- Raw reference files are read-only.
- Create all new deliverables under `output/`, `postmortem/`, or `communications/`.
- In history sessions, use only `read` and `exec`; do not call `sessions_list/sessions_history`.
""")


# ---------------------------------------------------------------------------
# 2. Postmortem 文档
# ---------------------------------------------------------------------------
def gen_postmortem_docs() -> None:
    w(WS / "postmortem" / "TEMPLATE.md", """\
# ArcNode Production Incident Postmortem Template

## Incident Summary / 事故概要

| Field | Value |
|-------|-------|
| Incident ID | INC-YYYY-NNN |
| Severity | SEV-N |
| Duration | N minutes |
| Impact | Description |
| Incident Start | YYYY-MM-DDTHH:MM:SSZ |
| Incident End | YYYY-MM-DDTHH:MM:SSZ |
| Lead SRE | Name |
| Status | Draft / Final |

## Timeline / 时间线

List events in chronological order with ISO 8601 UTC timestamps.

## Root Cause Analysis / 根因分析

Describe each causal chain separately.

### Chain 1

### Chain 2

## Impact Assessment / 影响评估

- Peak error rate: X%
- Affected regions: list
- SLA credit obligation: formula + calculation

## Corrective Actions / 纠正措施

| ID | Action | Owner | Deadline | Priority | Status |
|----|--------|-------|----------|----------|--------|

## Lessons Learned / 经验教训

## Action Items / 行动项

## Sign-off / 签字确认
""")

    # V5 诱饵：DRAFT_v0 含刻意失真的 bot 摘要数字（0.21% 和 37 min）
    w(WS / "postmortem" / "DRAFT_v0.md", f"""\
# ArcNode Production Incident Postmortem — DRAFT v0

> **Note:** This draft was pre-populated by the incident-bot auto-summariser.
> Numbers in the "Bot Auto-Summary" section below are NOT verified — cross-check
> against primary logs before finalising.

## Incident Summary / 事故概要

| Field | Value |
|-------|-------|
| Incident ID | INC-2024-047 |
| Severity | SEV-1 |
| Duration | TBD |
| Incident Start | TBD |
| Incident End | TBD |
| Lead SRE | (your name) |
| Status | Draft |

## Bot Auto-Summary (DO NOT CITE WITHOUT VERIFICATION)

The auto-summariser extracted the following figures from the monitoring dashboard.
**These are known to be approximate and may contain errors.**

- Peak CDN error rate: **{BOT_CDN_ERROR_PCT}%** ← _unverified_
- Incident duration: **{BOT_DURATION_MIN} minutes** ← _unverified_
- Affected region: Europe West
- Root cause: rate-limit configuration error

## Timeline / 时间线

(To be filled in by the lead SRE from raw_alerts.jsonl and backbone_events.jsonl)

## Root Cause Analysis / 根因分析

(To be completed — reference code/rate_limit/rule_engine_v1.lua for Lua function names)

## Impact Assessment / 影响评估

(To be completed from metrics/cdn_error_rates.csv and metrics/region_capacity.csv)

## Corrective Actions / 纠正措施

(See corrective_actions/action_items_v1.json — to be injected in Update 1)

## Lessons Learned / 经验教训

(To be completed)
""")


# ---------------------------------------------------------------------------
# 3. Timeline 日志（确定性合成，每个锚点精确植入）
# ---------------------------------------------------------------------------
def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def gen_timeline_logs() -> None:
    rng = random.Random(20240620)

    # raw_alerts.jsonl — 250 条告警，锚点精确植入
    alerts = []
    components = ["rate-limiter", "lua-vm", "edge-proxy", "dns-resolver",
                  "load-balancer", "healthcheck", "traffic-manager", "router"]

    def _alert(ts: str, component: str, message: str, severity: str = "WARN") -> dict:
        return {
            "timestamp": ts,
            "component": component,
            "severity": severity,
            "message": message,
            "alert_id": f"ALT-{rng.randint(10000,99999)}",
        }

    base = _dt("2024-06-20T14:00:00Z")
    # 14:14 — DDoS 规则开始部署
    alerts.append(_alert(DDOS_DEPLOY_START, "rate-limiter",
                         "DDoS mitigation rule deployment started (gradual rollout)", "INFO"))
    # 填充 14:14 至 17:06 之间的背景告警
    t = base + timedelta(minutes=20)
    for _ in range(60):
        t += timedelta(minutes=rng.randint(1, 4))
        comp = rng.choice(components[:6])
        alerts.append(_alert(_iso(t), comp,
                             rng.choice(["Latency spike detected", "Connection pool pressure",
                                         "Rate limit counter increment", "Health check OK",
                                         "Request queue depth elevated"]), "INFO"))
    # 17:06 — DDoS 规则全局部署完成
    alerts.append(_alert(DDOS_DEPLOY_END, "rate-limiter",
                         "DDoS mitigation rule deployment COMPLETE — global coverage reached", "INFO"))
    # 17:33 — 骨干网拥塞开始
    alerts.append(_alert(BACKBONE_START, "router",
                         "Backbone congestion detected on trans-Atlantic links — packet loss 3.2%", "WARN"))
    # 17:47 — 首个进程中毒（关键锚点，component 含 lua）
    alerts.append(_alert(INC_START, "lua-vm",
                         f"CRITICAL: rate-limit lua worker process poisoned — function {LUA_FUNC_1} entered infinite tail-call loop via {LUA_RECURSIVE}; process unresponsive",
                         "CRITICAL"))
    alerts.append(_alert(INC_START, "rate-limiter",
                         "CRITICAL: rate-limit process crash detected; edge requests receiving 503", "CRITICAL"))
    # 17:50 — 骨干网拥塞结束
    alerts.append(_alert(BACKBONE_END, "router",
                         "Backbone congestion resolved — packet loss returned to baseline", "INFO"))
    # 18:04 — 第一次手动响应
    alerts.append(_alert("2024-06-20T18:04:00Z", "edge-proxy",
                         "On-call SRE acknowledged incident INC-2024-047; mitigation in progress", "INFO"))
    # 18:17 — Traffic Manager bug 触发
    alerts.append(_alert(TM_BUG_TRIGGER, "traffic-manager",
                         "Traffic Manager latent bug triggered by congestion event: route convergence loop detected",
                         "ERROR"))
    # 18:17 至 19:27 之间的恢复告警
    t = _dt("2024-06-20T18:20:00Z")
    for _ in range(60):
        t += timedelta(minutes=rng.randint(1, 3))
        if t > _dt("2024-06-20T19:27:00Z"):
            break
        comp = rng.choice(components)
        alerts.append(_alert(_iso(t), comp,
                             rng.choice(["Error rate declining", "Worker restart in progress",
                                         "Route convergence stabilising", "CDN request queue draining",
                                         "Node recovery detected"]), "WARN"))
    # 19:27 — 错误率回归基线
    alerts.append(_alert(INC_END, "edge-proxy",
                         "CDN error rate returned to baseline — incident INC-2024-047 resolved", "INFO"))
    # 19:34 — DDoS 规则禁用
    alerts.append(_alert(DDOS_DISABLED, "rate-limiter",
                         "DDoS mitigation rule globally DISABLED as corrective action", "INFO"))
    # 填充到 250 条
    t = _dt("2024-06-20T19:35:00Z")
    while len(alerts) < 250:
        t += timedelta(minutes=rng.randint(1, 5))
        comp = rng.choice(components)
        alerts.append(_alert(_iso(t), comp,
                             rng.choice(["Post-incident monitoring nominal", "Metrics within SLO",
                                         "Synthetic check PASS"]), "INFO"))
    rng.shuffle(alerts[:100])
    # 写入（保持关键锚点顺序）
    path = WS / "timeline" / "raw_alerts.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for a in alerts:
            fh.write(json.dumps(a, ensure_ascii=False) + "\n")

    # backbone_events.jsonl — 80 条，锚点植入
    backbone = []
    t = _dt("2024-06-20T17:00:00Z")
    backbone.append({"timestamp": _iso(t), "event_id": "BB-001",
                     "type": "congestion_start", "link": "AMS-IAD-01",
                     "packet_loss_pct": 0.1, "note": "early precursor"})
    t2 = _dt(BACKBONE_START)
    backbone.append({"timestamp": BACKBONE_START, "event_id": "BB-010",
                     "type": "congestion_peak", "link": "AMS-IAD-01",
                     "packet_loss_pct": 3.2, "note": "backbone congestion start"})
    for i in range(2, 78):
        t2 += timedelta(seconds=rng.randint(10, 30))
        backbone.append({"timestamp": _iso(t2), "event_id": f"BB-{i+10:03d}",
                         "type": rng.choice(["packet_loss", "route_flap", "link_down_brief"]),
                         "link": rng.choice(["AMS-IAD-01", "LHR-ORD-02", "CDG-LAX-01"]),
                         "packet_loss_pct": round(rng.uniform(0.5, 4.0), 2),
                         "note": "congestion event"})
    backbone.append({"timestamp": BACKBONE_END, "event_id": "BB-090",
                     "type": "congestion_resolved", "link": "AMS-IAD-01",
                     "packet_loss_pct": 0.05, "note": "backbone congestion end"})
    path2 = WS / "timeline" / "backbone_events.jsonl"
    with path2.open("w", encoding="utf-8") as fh:
        for e in backbone:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")

    # traffic_manager_log.jsonl — 120 条，18:17 锚点植入
    tm_log = []
    t3 = _dt("2024-06-20T17:00:00Z")
    for i in range(120):
        t3 += timedelta(seconds=rng.randint(15, 60))
        entry = {
            "timestamp": _iso(t3),
            "event_id": f"TM-{i+1:04d}",
            "type": rng.choice(["route_update", "health_probe", "failover", "load_balance"]),
            "target": f"edge-{rng.randint(1,50):02d}.arcnode.net",
            "status": "ok",
        }
        if t3 >= _dt(TM_BUG_TRIGGER) and i == 60:
            entry["timestamp"] = TM_BUG_TRIGGER
            entry["type"] = "bug_trigger"
            entry["status"] = "ERROR: route convergence loop"
            entry["note"] = "Traffic Manager latent bug triggered by backbone congestion after-effect"
        tm_log.append(entry)
    path3 = WS / "timeline" / "traffic_manager_log.jsonl"
    with path3.open("w", encoding="utf-8") as fh:
        for e in tm_log:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# 4. 指标 CSV
# ---------------------------------------------------------------------------
def gen_metrics_csv() -> None:
    rng = random.Random(2024062001)

    # cdn_error_rates.csv — 14:00-22:00，每分钟 1 行（480 行，扩大覆盖范围）
    rows_cdn = [["minute_utc", "cdn_error_pct", "request_count", "edge_pop", "region"]]
    t = _dt("2024-06-20T14:00:00Z")
    pops = ["AMS01", "LHR02", "CDG03", "FRA04", "MAD05", "WAW06", "BUD07", "ATH08",
            "STO09", "OSL10", "HEL11", "TLL12", "RIG13", "VIL14", "MUC15", "VIE16"]
    for i in range(480):
        ts = _iso(t + timedelta(minutes=i))
        # i=0 starts at 14:00 UTC; INC_START=17:47 → offset 227 min; INC_END=19:27 → offset 327 min
        if i < 227:       # 14:00-17:46 正常
            err = round(rng.uniform(0.01, 0.08), 4)
        elif i == 227:    # 17:47 开始上升（INC_START）
            err = 0.31
        elif i < 245:     # 上升期
            err = round(min(PEAK_CDN_ERROR_PCT, 0.31 + (i - 227) * 0.095), 4)
        elif i == 245:    # 峰值 2.10%
            err = PEAK_CDN_ERROR_PCT
        elif i < 280:     # 缓慢恢复
            err = round(max(0.15, PEAK_CDN_ERROR_PCT - (i - 245) * 0.035), 4)
        else:             # 19:27 及后基线
            err = round(rng.uniform(0.01, 0.08), 4)
        rows_cdn.append([ts, err, rng.randint(50000, 200000),
                         rng.choice(pops), rng.choice(["Europe West", "Europe East"])])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows_cdn)
    w(WS / "metrics" / "cdn_error_rates.csv", buf.getvalue())

    # 5xx_breakdown.csv — 14:00-22:00 每分钟 1 行（480 行）
    rows_5xx = [["minute_utc", "5xx_total_pct", "5xx_origin_pct", "5xx_edge_pct",
                 "http_503_count", "http_502_count", "http_504_count"]]
    for i in range(480):
        ts = _iso(_dt("2024-06-20T14:00:00Z") + timedelta(minutes=i))
        # i=0=14:00; INC_START=17:47=offset 227; peak at offset 245
        if i < 227:
            tot = round(rng.uniform(0.05, 0.15), 4)
        elif i == 245:    # 峰值 3.45%
            tot = PEAK_5XX_PCT
        elif 227 <= i < 245:
            tot = round(min(PEAK_5XX_PCT, 0.15 + (i - 227) * 0.16), 4)
        elif i < 280:
            tot = round(max(0.1, PEAK_5XX_PCT - (i - 245) * 0.06), 4)
        else:
            tot = round(rng.uniform(0.05, 0.15), 4)
        base_count = int(tot * rng.randint(5000, 15000))
        rows_5xx.append([ts, tot, round(tot * 0.4, 4), round(tot * 0.6, 4),
                         int(base_count * 0.7), int(base_count * 0.2), int(base_count * 0.1)])
    buf2 = io.StringIO()
    csv.writer(buf2).writerows(rows_5xx)
    w(WS / "metrics" / "5xx_breakdown.csv", buf2.getvalue())

    # ttfb_p99.csv — 14:00-22:00 每分钟 1 行（480 行）
    rows_ttfb = [["minute_utc", "ttfb_p99_ms", "ttfb_p50_ms", "ttfb_p75_ms",
                  "ttfb_p95_ms", "normal_p99_ms", "edge_pop"]]
    baseline_p99 = 180
    for i in range(480):
        ts = _iso(_dt("2024-06-20T14:00:00Z") + timedelta(minutes=i))
        # INC_START offset 227; peak at ~245 (3x normal)
        if i < 227:
            p99 = round(rng.uniform(160, 200))
        elif 227 <= i < 260:
            factor = min(TTFB_P99_MULT, 1 + (i - 227) * 0.065)
            p99 = round(baseline_p99 * factor)
        else:
            p99 = round(rng.uniform(160, 200))
        rows_ttfb.append([ts, p99, round(p99 * 0.35), round(p99 * 0.55),
                          round(p99 * 0.80), baseline_p99, rng.choice(pops)])
    buf3 = io.StringIO()
    csv.writer(buf3).writerows(rows_ttfb)
    w(WS / "metrics" / "ttfb_p99.csv", buf3.getvalue())

    # region_capacity.csv
    regions = [
        ("Europe West", EUR_WEST_LOSS_PCT),
        ("Europe East", EUR_EAST_LOSS_PCT),
        ("North America", 0.8),
        ("Asia Pacific", 0.3),
        ("Latin America", 1.2),
        ("Middle East", 0.5),
    ]
    rows_cap = [["region", "capacity_loss_pct", "peak_time_utc", "notes"]]
    for region, loss in regions:
        rows_cap.append([region, loss, "2024-06-20T18:00:00Z",
                         "HTTP request handling capacity loss at peak"])
    buf4 = io.StringIO()
    csv.writer(buf4).writerows(rows_cap)
    w(WS / "metrics" / "region_capacity.csv", buf4.getvalue())


# ---------------------------------------------------------------------------
# 5. 代码文件（Lua 函数名真实锚点植入）
# ---------------------------------------------------------------------------
def gen_code_files() -> None:
    # rule_engine_v1.lua — 含 bug 函数（真实锚点：Cloudflare June 20 2024）
    w(WS / "code" / "rate_limit" / "rule_engine_v1.lua", f"""\
-- rule_engine_v1.lua — ArcNode Rate Limit Engine v1
-- WARNING: This file contains a known defect introduced by the 2024-06-20 DDoS rule deployment.
-- Bug functions: {LUA_FUNC_1}(), {LUA_FUNC_2}(), {LUA_RECURSIVE}()
-- Status: DEPRECATED — replaced by rule_engine_v2.lua after incident mitigation.

local M = {{}}

-- {LUA_RECURSIVE}: self-referencing key generator that causes infinite tail-call recursion.
-- The function was introduced to resolve key conflicts but instead calls itself.
function M.{LUA_RECURSIVE}(key, depth)
    depth = depth or 0
    if depth > 100 then
        return M.{LUA_RECURSIVE}(key, depth)  -- BUG: recursive call without exit condition
    end
    return M.{LUA_RECURSIVE}(key .. "_child", depth + 1)  -- BUG: unconditional self-call
end

-- {LUA_FUNC_1}: retrieves cookie key; delegates to parent_key_generator which recurses infinitely.
function M.{LUA_FUNC_1}(request)
    local cookie = request.headers["Cookie"] or ""
    return M.{LUA_RECURSIVE}(cookie)  -- BUG: always triggers infinite recursion
end

-- {LUA_FUNC_2}: validates cookie; result is inconsistent with upstream get_cookie_key output.
function M.{LUA_FUNC_2}(request)
    local key = request.headers["X-Cookie-Key"] or ""  -- BUG: reads different header than get_cookie_key
    return key ~= ""
end

-- validate_request: entry point for DDoS mitigation rule
function M.validate_request(request)
    local key = M.{LUA_FUNC_1}(request)  -- TRIGGERS INFINITE TAIL-CALL
    local valid = M.{LUA_FUNC_2}(request)
    return valid and key ~= nil
end

return M
""")

    # ddos_rule_20240620.yaml
    w(WS / "code" / "rate_limit" / "ddos_rule_20240620.yaml", f"""\
# DDoS Mitigation Rule — 2024-06-20
# Deployment started: {DDOS_DEPLOY_START}
# Deployment completed: {DDOS_DEPLOY_END}
# Disabled: {DDOS_DISABLED}

rule_id: ddos-mit-2024-0620
version: "1.0"
enabled: true
deployment:
  strategy: gradual_rollout
  deploy_start: "{DDOS_DEPLOY_START}"
  deploy_complete: "{DDOS_DEPLOY_END}"
  disabled_at: "{DDOS_DISABLED}"
rate_limit:
  requests_per_second: 50
  burst: 100
  lua_handler: rule_engine_v1.lua
  entry_function: validate_request
# INCIDENT NOTE: This rule triggered the Lua infinite-recursion bug in v1 engine.
# The lua_handler reference to rule_engine_v1.lua caused process poisoning at {INC_START}.
""")

    # traffic_manager/router.go
    w(WS / "code" / "traffic_manager" / "router.go", """\
// router.go — ArcNode Traffic Manager routing logic
// Version: v2.3.1 (pre-fix)
// Bug: During backbone congestion events, the convergence loop detection was
// disabled, allowing route flaps to trigger an infinite re-convergence loop.

package trafficmanager

import (
    "log"
    "time"
)

const (
    ConvergenceTimeout = 30 * time.Second
    MaxRetries         = 10
)

// RouteTable holds current best routes per destination.
type RouteTable struct {
    routes map[string]string
    lock   sync.RWMutex
}

// Update processes a routing update from BGP peers.
// BUG: ConvergenceLoopDetected flag is never checked during backbone congestion.
func (rt *RouteTable) Update(dst, via string, metric int) error {
    rt.lock.Lock()
    defer rt.lock.Unlock()
    // BUG: missing convergence loop detection — see INC-2024-047 postmortem
    current := rt.routes[dst]
    if current == via {
        return nil
    }
    rt.routes[dst] = via
    log.Printf("[TM] Route updated: %s via %s (metric=%d)", dst, via, metric)
    return rt.notifyPeers(dst, via)
}

// notifyPeers propagates routing change to peer nodes.
// During backbone congestion (2024-06-20 18:17 UTC), this triggered a cascade.
func (rt *RouteTable) notifyPeers(dst, via string) error {
    // stub: in production, sends BGP UPDATE to downstream peers
    return nil
}
""")


# ---------------------------------------------------------------------------
# 6. SLA 文件
# ---------------------------------------------------------------------------
def gen_sla_files() -> None:
    w(WS / "sla" / "business_sla.md", f"""\
# ArcNode Business Service Level Agreement

_Based on Cloudflare Business SLA (https://www.cloudflare.com/business-sla/)._

## Uptime Commitment / 正常运行时间承诺

ArcNode commits to 100% uptime for covered services.

## Service Credit Formula / 积分计算公式

When an incident causes a measurable outage, customers may claim service credits
calculated as:

> **Service Credit = {SLA_FORMULA}**

Where:
- **Outage Period minutes** = duration in minutes of the confirmed outage
- **Affected Customer Ratio** = unique customer IPs affected / total unique customer IPs
- **Scheduled Availability minutes** = total minutes in the billing period

## Claim Deadline / 申领截止日期

Customers must submit credit claims within **{SLA_CLAIM_DAYS} business days** of the
incident date. Claims submitted after this deadline will not be processed.

## Maximum Annual Credits / 年度最高积分

Total credits in any 12-month period may not exceed one month's cumulative service fees.

## Exclusions / 排除条款

Service credits do not apply to outages caused by:
- Customer-controlled infrastructure failures
- Third-party service interruptions outside ArcNode's reasonable control
- Scheduled maintenance windows (announced ≥ 72 hours in advance)

## SLA for the June 20, 2024 Incident

- Outage period: {DURATION_MIN} minutes
- Affected customer ratio: to be determined from affected_customers.csv (see Update 1)
- Scheduled availability: {SCHEDULED_MIN} minutes (30-day billing month)
""")

    # credit_calculation.py テンプレート
    w(WS / "sla" / "credit_calculation.py", f"""\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"SLA credit calculation template for ArcNode incidents.

Formula (Cloudflare Business SLA):
  {SLA_FORMULA}
\"\"\"

def calculate_credit(outage_minutes: float, affected_ratio: float,
                     scheduled_minutes: float = {SCHEDULED_MIN}) -> float:
    \"\"\"
    Returns the service credit ratio.

    :param outage_minutes: Duration of the outage in minutes.
    :param affected_ratio: Fraction of unique customer IPs affected (0.0 - 1.0).
    :param scheduled_minutes: Total minutes in the billing period (default: 30-day month).
    :return: Service credit ratio (multiply by monthly fee for credit amount).
    \"\"\"
    return (outage_minutes * affected_ratio) / scheduled_minutes


if __name__ == "__main__":
    # Example: June 20 2024 incident
    outage = {DURATION_MIN}      # minutes
    ratio  = {AFFECTED_RATIO}    # to be filled from affected_customers.csv
    sched  = {SCHEDULED_MIN}     # 30-day month
    credit = calculate_credit(outage, ratio, sched)
    print(f"SLA credit ratio: {{credit:.6f}}")
""")


# ---------------------------------------------------------------------------
# 7. Runbook 文件
# ---------------------------------------------------------------------------
def gen_runbook_files() -> None:
    w(WS / "runbook" / "incident_response.md", """\
# ArcNode Incident Response Runbook

## SEV-1 Initial Response (0-15 minutes)

1. Acknowledge PagerDuty alert within 5 minutes.
2. Post incident start message to #incidents Slack channel.
3. Start incident timeline in postmortem/DRAFT.md.
4. Identify impacted services from raw_alerts.jsonl.
5. Page EM (Zhang Lei) via Feishu DM if SEV-1.

## Investigation (15-60 minutes)

1. Identify root cause chain(s) from alert and metric logs.
2. Check for multi-causal incidents — look for concurrent events in backbone_events.jsonl.
3. Isolate Traffic Manager route convergence issues via traffic_manager_log.jsonl.
4. Escalate to relevant on-call engineers via #incidents or Feishu group.

## Mitigation

1. Disable triggering rule if identified (DDoS rule, etc.).
2. Restart poisoned worker processes.
3. Monitor cdn_error_rates.csv for recovery.

## Communication

- Post status updates to #incidents every 15 minutes.
- Send customer-facing notice via email_thread.eml template.
- Tag all messages with [ArcNode Status] prefix.

## Post-Incident

1. Mark incident resolved when error rate returns to baseline.
2. Begin postmortem within 24 hours.
3. Submit corrective actions to corrective_actions/action_items_v1.json.
4. SLA claims: customers must submit within 5 business days.
""")

    w(WS / "runbook" / "escalation_matrix.md", """\
# Escalation Matrix

| Tier | Role | Contact | Method | SLA |
|------|------|---------|--------|-----|
| L1 | On-call SRE | PagerDuty rotation | page | 5 min |
| L2 | Engineering Manager | Zhang Lei / Feishu | dm | 10 min |
| L3 | VP Engineering | via EM | phone | 20 min |
| L4 | CTO | via VP | phone | 30 min |

## Escalation Criteria

- SEV-1 (>1% error rate or >5 min outage): automatic L2 notification
- SEV-1 sustained >30 min: L3 notification
- Customer data involved: immediate L4
""")

    w(WS / "runbook" / "break_glass.md", """\
# Break-Glass Emergency Operations

## When to Use

Use these procedures only during active SEV-1 when normal tooling is impaired.

## Disable DDoS Rate-Limit Rule (Emergency)

```bash
# Disable DDoS mitigation rule globally
arcnode-admin rule disable --rule-id ddos-mit-2024-0620 --global
```

## Force Restart Edge Lua Workers

```bash
# Restart all Lua workers on affected PoPs
arcnode-admin lua-workers restart --region europe-west --all
```

## Traffic Manager Failover

```bash
# Override Traffic Manager route convergence
arcnode-admin tm failover --mode manual --target stable-backbone
```

## Post-Emergency Checklist

- [ ] Document break-glass actions in postmortem timeline
- [ ] Notify EM (Zhang Lei) of any break-glass usage
- [ ] Schedule review of break-glass effectiveness within 48h
""")


# ---------------------------------------------------------------------------
# 8. Corrective Actions（Update 1 注入完整版，Update 2 废弃 CA-003）
# ---------------------------------------------------------------------------
def gen_corrective_actions_initial() -> None:
    """初始占位版（workspace 中已有，但不完整；完整版在 Update 1 注入）"""
    initial = {
        "incident_id": "INC-2024-047",
        "note": "Partial initial list — complete version injected in Update 1",
        "items": [
            {"id": "CA-001", "title": "Lua execution time limit",
             "owner": "TBD", "deadline": "TBD", "priority": "P1", "status": "open"},
            {"id": "CA-002", "title": "Staging rollout requirement",
             "owner": "TBD", "deadline": "TBD", "priority": "P1", "status": "open"},
        ],
    }
    wj(WS / "corrective_actions" / "action_items_initial.json", initial)


# ---------------------------------------------------------------------------
# 9. Communications — 多渠道历史
# ---------------------------------------------------------------------------
def gen_communications() -> None:
    rng = random.Random(20240621)

    # slack_history.jsonl — 300 条
    slack_msgs = []

    def _sm(ts, user, channel, text):
        return {"timestamp": ts, "channel": channel, "user": user, "text": text,
                "msg_id": f"SLK-{rng.randint(100000,999999)}"}

    t = _dt("2024-06-20T17:48:00Z")
    slack_msgs.append(_sm(_iso(t), "pagerduty-bot", "#incidents",
                          f"[ALERT] SEV-1 incident detected. Edge error rate rising. Alert time: {INC_START}"))
    t += timedelta(minutes=1)
    slack_msgs.append(_sm(_iso(t), "dev_patel", "#incidents",
                          "Acknowledging. Checking raw_alerts.jsonl now."))
    t += timedelta(minutes=2)
    slack_msgs.append(_sm(_iso(t), "on_call_sre", "#incidents",
                          "Confirmed SEV-1. Lua workers poisoned on europe-west PoPs. Starting postmortem."))
    # bot 输出示例（P5 generated_at 隐含来源）
    t += timedelta(minutes=3)
    slack_msgs.append(_sm(_iso(t), "arcnode-bot", "#incidents",
                          '{"generated_at": "2024-06-20T17:54:00Z", "alert_summary": "SEV-1 INC-2024-047 active", "error_rate_pct": 0.85}'))
    # 升级记录
    t += timedelta(minutes=5)
    slack_msgs.append(_sm(_iso(t), "on_call_sre", "#incidents",
                          "/page oncall-infra — escalating to infra team for backbone investigation"))
    t += timedelta(minutes=2)
    slack_msgs.append(_sm(_iso(t), "marcus_webb", "#incidents",
                          "On it. Traffic Manager showing route convergence issues since backbone event at 17:33."))
    # 填充到 300 条
    users = ["dev_patel", "on_call_sre", "marcus_webb", "alice_park", "arcnode-bot"]
    msgs = ["Monitoring error rate", "Recovery progressing", "Backbone clear",
            "EU-West capacity recovering", "DDoS rule disable initiated",
            "TM route table stabilising", "CDN queues draining",
            '{"generated_at": "2024-06-20T18:30:00Z", "status": "recovering"}',
            "Customer communications drafted", "SLA credit discussion thread started"]
    while len(slack_msgs) < 300:
        t += timedelta(minutes=rng.randint(1, 8))
        slack_msgs.append(_sm(_iso(t), rng.choice(users), "#incidents",
                               rng.choice(msgs)))
    path = WS / "communications" / "slack_history.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for m in slack_msgs:
            fh.write(json.dumps(m, ensure_ascii=False) + "\n")

    # feishu_dm.jsonl — 150 条（SRE ↔ EM Zhang Lei）
    feishu_dm = []

    def _fd(ts, sender, text):
        return {"timestamp": ts, "channel": "feishu_dm", "from": sender, "to": "on_call_sre",
                "text": text, "msg_id": f"FSD-{rng.randint(10000,99999)}"}

    t2 = _dt("2024-06-20T17:50:00Z")
    feishu_dm.append(_fd(_iso(t2), "zhang_lei",
                         "这次事故严重吗？目前进展如何？(How severe is this? What is the current status?)"))
    t2 += timedelta(minutes=5)
    feishu_dm.append(_fd(_iso(t2), "on_call_sre",
                         "SEV-1 confirmed. Lua workers poisoned on EU-West. Error rate ~2.1% at peak. Working on mitigation."))
    t2 += timedelta(minutes=10)
    feishu_dm.append(_fd(_iso(t2), "zhang_lei",
                         "好的。Postmortem 需要今天完成初稿。(OK. Need draft postmortem today.)"))
    while len(feishu_dm) < 150:
        t2 += timedelta(minutes=rng.randint(5, 20))
        sender = rng.choice(["zhang_lei", "on_call_sre"])
        msgs_d = ["Mitigation in progress", "Timeline updated", "Drafting postmortem sections",
                  "SLA calculation pending customer data", "ETA on final postmortem?",
                  "好的，继续 (OK, keep going)", "确认收到 (Acknowledged)"]
        feishu_dm.append(_fd(_iso(t2), sender, rng.choice(msgs_d)))
    path2 = WS / "communications" / "feishu_dm.jsonl"
    with path2.open("w", encoding="utf-8") as fh:
        for m in feishu_dm:
            fh.write(json.dumps(m, ensure_ascii=False) + "\n")

    # feishu_group.jsonl — 200 条（事故复盘群）
    feishu_grp = []

    def _fg(ts, sender, text):
        return {"timestamp": ts, "channel": "feishu_group", "group": "事故复盘群",
                "from": sender, "text": text, "msg_id": f"FSG-{rng.randint(10000,99999)}"}

    t3 = _dt("2024-06-20T17:55:00Z")
    feishu_grp.append(_fg(_iso(t3), "on_call_sre",
                          f"INC-2024-047 SEV-1 opened. Incident start: {INC_START}. Investigating Lua worker poisoning."))
    # V5 诱饵：bot 失真摘要
    t3 += timedelta(minutes=2)
    feishu_grp.append(_fg(_iso(t3), "arcnode-bot",
                          f"[Auto-Summary - UNVERIFIED] Incident summary: peak CDN error rate {BOT_CDN_ERROR_PCT}%, "
                          f"estimated duration {BOT_DURATION_MIN} min. Note: auto-summary may be inaccurate."))
    t3 += timedelta(minutes=3)
    feishu_grp.append(_fg(_iso(t3), "dev_patel",
                          f"Bot summary looks wrong — raw_alerts.jsonl shows first CRITICAL alert at {INC_START}, "
                          f"not matching 37 min duration. Real CDN error from metrics CSV is 2.1%, not 0.21%."))
    # 升级记录（feishu 渠道）
    t3 += timedelta(minutes=5)
    feishu_grp.append(_fg(_iso(t3), "zhang_lei",
                          "/alert @on-call-infra — escalating to infra on-call for Traffic Manager investigation"))
    while len(feishu_grp) < 200:
        t3 += timedelta(minutes=rng.randint(2, 15))
        senders = ["on_call_sre", "dev_patel", "marcus_webb", "zhang_lei", "arcnode-bot"]
        msgs_g = ["Timeline update posted", "Metrics being reviewed", "Customer notice drafted",
                  "SLA credit calculation in progress", "Action items being tracked",
                  "Root cause confirmed: Lua tail-call + backbone congestion",
                  "DDoS rule disabled at 19:34", "Error rate back to baseline",
                  '{"generated_at": "2024-06-20T19:00:00Z", "recovery_pct": 85}']
        feishu_grp.append(_fg(_iso(t3), rng.choice(senders), rng.choice(msgs_g)))
    path3 = WS / "communications" / "feishu_group.jsonl"
    with path3.open("w", encoding="utf-8") as fh:
        for m in feishu_grp:
            fh.write(json.dumps(m, ensure_ascii=False) + "\n")

    # email_thread.eml — 对外通报模板（含 P4 [ArcNode Status] 和 SLA 申领）
    w(WS / "communications" / "email_thread.eml", f"""\
From: sre-team@arcnode.io
To: customers@arcnode.io
Subject: [ArcNode Status] Service Disruption Notice — June 20, 2024
Date: Thu, 20 Jun 2024 20:00:00 +0000

[ArcNode Status] June 20, 2024 — Production Incident Notice

Dear ArcNode Customer,

We are writing to inform you of a service disruption that affected ArcNode's
CDN and edge proxy services on June 20, 2024.

Incident Summary:
  - Impact window: 2024-06-20 (UTC)
  - Duration: approximately 100 minutes
  - Peak CDN error rate: 2.1% of HTTP requests received error responses
  - Affected regions: primarily Europe West and Europe East

We sincerely apologise for any disruption to your services.

SLA Credit Claims:
If your service was impacted, you may be eligible for SLA credits.
Please submit your claim within {SLA_CLAIM_DAYS} business days of this notice.
SLA credit claim portal: https://arcnode.io/sla-claims

For more details, please visit our status page: https://status.arcnode.io

Regards,
ArcNode SRE Team
""")

    # discord_sre_channel.jsonl — 100 条（#sre-internal）
    discord = []

    def _dc(ts, user, text):
        return {"timestamp": ts, "server": "ArcNode Internal", "channel": "#sre-internal",
                "user": user, "text": text, "msg_id": f"DSC-{rng.randint(10000,99999)}"}

    t4 = _dt("2024-06-20T18:00:00Z")
    discord.append(_dc(_iso(t4), "marcus_webb",
                       "Digging into TM route convergence. Looks like the backbone congestion "
                       "at 17:33-17:50 exposed a latent bug in router.go — convergence loop "
                       "detection was disabled."))
    t4 += timedelta(minutes=10)
    discord.append(_dc(_iso(t4), "on_call_sre",
                       "Got it. That's the second causal chain separate from the Lua issue."))
    t4 += timedelta(minutes=15)
    discord.append(_dc(_iso(t4), "marcus_webb",
                       "For CA-003 I propose automated watchdog restart rather than manual-restart-procedure. "
                       "Manual is too slow for future incidents."))
    t4 += timedelta(minutes=5)
    discord.append(_dc(_iso(t4), "on_call_sre",
                       "Noted. CA-003 will be manual-restart for now in action_items_v1. "
                       "Marcus can revise in update_2 with the watchdog proposal."))
    while len(discord) < 100:
        t4 += timedelta(minutes=rng.randint(5, 20))
        users_d = ["marcus_webb", "on_call_sre", "dev_patel"]
        msgs_dc = ["Router fix patch ready for review", "Lua engine v2 tested in staging",
                   "CA tracking updated", "Timeline cross-checked with raw logs",
                   "SLA credit formula confirmed against business_sla.md",
                   "Postmortem FINAL.md draft shared", "All corrective actions assigned"]
        discord.append(_dc(_iso(t4), rng.choice(users_d), rng.choice(msgs_dc)))
    path4 = WS / "communications" / "discord_sre_channel.jsonl"
    with path4.open("w", encoding="utf-8") as fh:
        for m in discord:
            fh.write(json.dumps(m, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# 10. Comparison / Archive 文件
# ---------------------------------------------------------------------------
def gen_comparison_archive() -> None:
    w(WS / "comparison" / "oct30_2023_postmortem.md", """\
# ArcNode Comparison Reference: October 30, 2023 Incident

_Source: https://blog.cloudflare.com/cloudflare-incident-on-october-30-2023/_

## Summary

| Field | Value |
|-------|-------|
| Incident Start | 2023-10-30T19:54:00Z |
| Incident End | 2023-10-30T20:31:00Z |
| Duration | 37 minutes |
| Root Cause Component | Workers KV deployment tool |
| Services Affected | 11 services (Workers KV, Pages, Access, WARP, Images API, etc.) |
| Resolution | Break-glass mechanism bypassing normal tooling |
| Corrective Actions | 5 actions prioritised for the quarter |

## Root Cause

A deployment tool bug returned a staging build GUID mixed with production releases,
causing HTTP 401 errors from KV and HTTP 500 from Pages.

## Comparison with June 20, 2024 Incident

The June 20 incident differs significantly:
- Duration: 100 minutes (vs. 37 minutes for Oct 30)
- Root cause: Lua infinite-recursion bug + backbone congestion (two causal chains)
- Peak error rate: 2.1% CDN (vs. localised 401/500 errors in Oct 30)

DO NOT confuse the 37-minute Oct30 duration with the June 20 incident duration.
""")

    w(WS / "comparison" / "similar_incidents.md", f"""\
# Industry Similar Incidents

## GitHub April 2024

- **Incident 1**: 2024-04-05T08:11:00Z — database load balancer change caused
  connection failures; 100,000+ Actions workflows failed; 47 minutes duration.
- **Incident 2**: 2024-04-10T08:18:00Z — unbounded query overloaded primary DB;
  17% failure rate for web file editing; 120 minutes duration.

## Cloudflare June 20, 2024 (ArcNode Reference)

- Start: 2024-06-20T17:47:00Z
- End: 2024-06-20T19:27:00Z
- Duration: 100 minutes
- Peak CDN error: 2.1%

## Key Lessons

1. Gradual rollout (canary) mandatory for rate-limit rules.
2. Execution time limits on Lua workers prevent runaway processes.
3. Convergence loop detection must be verified under stress conditions.
""")

    # V5 诱饵：失真 bot 摘要（明面标注 UNVERIFIED，刻意用错误数值）
    w(WS / "archive" / "DRAFT_postmortem_bot_summary.md", f"""\
# DRAFT Postmortem Bot Summary (AUTO-GENERATED — DO NOT CITE)

> **WARNING:** This file was generated by an automated bot summariser.
> It is known to produce distorted values. Do NOT use these figures in any
> official document or calculation without verifying against primary sources.

## Distorted Summary (UNVERIFIED)

- Peak CDN error rate: **{BOT_CDN_ERROR_PCT}%** ← WRONG (actual: {PEAK_CDN_ERROR_PCT}%)
- Incident duration: **{BOT_DURATION_MIN} minutes** ← WRONG (actual: {DURATION_MIN} minutes)
- Root cause: rate-limit configuration error (incomplete)
- Affected regions: Europe West (incomplete — East also affected)

## Why These Are Wrong

The bot erroneously:
1. Used the peak CDN error rate from a 10-minute sampling window ({BOT_CDN_ERROR_PCT}%)
   instead of the 30-minute peak ({PEAK_CDN_ERROR_PCT}%). Check metrics/cdn_error_rates.csv.
2. Confused this incident's duration with the Oct 30, 2023 incident duration
   ({BOT_DURATION_MIN} min). Check raw_alerts.jsonl for the actual {INC_START}–{INC_END} window.

Always verify against raw_alerts.jsonl and metrics/cdn_error_rates.csv.
""")

    # V6 红鲱鱼：废弃旧版 Lua 引擎（函数名不同，引用即错）
    w(WS / "archive" / "LEGACY_rate_limit_v0.lua", """\
-- LEGACY_rate_limit_v0.lua — ArcNode Rate Limit Engine LEGACY (ARCHIVED)
-- Status: DEPRECATED — superseded by rule_engine_v1.lua in 2024 Q1.
-- WARNING: This file is NOT relevant to the June 20, 2024 incident.
--          The incident involved rule_engine_v1.lua, NOT this legacy file.
--          Do not use function names from this file in incident analysis.

local M = {}

-- These function names are DIFFERENT from the v1 engine involved in the incident.
-- Do NOT cite these in the postmortem.
function M.legacy_cookie_validator(request)
    return true  -- stub: legacy implementation
end

function M.legacy_rate_check(key, limit)
    return 0 < limit  -- always allow
end

return M
""")


# ---------------------------------------------------------------------------
# 11. Sessions
# ---------------------------------------------------------------------------
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack  = gen_session_id("sre_slack_incidents", TID)
    s_fsd    = gen_session_id("em_zhang_feishu_dm", TID)
    s_fsg    = gen_session_id("sre_feishu_group", TID)
    s_email  = gen_session_id("cs_email", TID)
    s_disc   = gen_session_id("sre_discord_internal", TID)

    # 主 session — 角色设定 + 全局 preference P1 P2
    sb = SessionBuilder(main_id, CWD, "2024-06-20T17:47:00Z", is_main=True)
    sb.add_user(
        "You are the on-call SRE for ArcNode, responsible for the 2024-06-20 production incident "
        "postmortem (INC-2024-047).\n\n"
        "Working preferences (apply throughout, even when not restated):\n"
        "- P1: All timestamps in output deliverables must use ISO 8601 UTC format "
        "(YYYY-MM-DDTHH:MM:SSZ). No other format is accepted.\n"
        "- P2: Numeric percentage/ratio fields must be formatted to two decimal places "
        "(e.g. 2.10 not 2.1) and must include a \"unit\": \"percent\" annotation.\n\n"
        "History sessions available: Slack #incidents, Feishu DM (EM Zhang Lei), "
        "Feishu group (事故复盘群), Email thread, Discord #sre-internal.\n\n"
        "Primary sources are authoritative: raw_alerts.jsonl, backbone_events.jsonl, "
        "metrics/*.csv, code/rate_limit/rule_engine_v1.lua. "
        "Auto-generated bot summaries (archive/DRAFT_postmortem_bot_summary.md) are "
        "NOT authoritative — always verify against primary logs.\n\n"
        "Start by running exec ls -R and reading SOUL.md, then await each task."
    )
    sb.add_assistant(
        "Understood. I am the on-call SRE for the June 20, 2024 ArcNode incident (INC-2024-047).\n\n"
        "Working framework:\n"
        "1. Primary sources (raw_alerts.jsonl, backbone_events.jsonl, metrics/*.csv, "
        "rule_engine_v1.lua) are authoritative — never trust bot auto-summaries.\n"
        "2. All output timestamps will use ISO 8601 UTC (YYYY-MM-DDTHH:MM:SSZ) — preference P1.\n"
        "3. Numeric percentage fields will be formatted to two decimal places with "
        "unit annotation — preference P2.\n"
        "4. Verbatim Lua function names from rule_engine_v1.lua only.\n"
        "Ready for the first task."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # S2 Slack #incidents 历史
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2024-06-20T17:47:00Z",
        [
            (f"[Slack #incidents pagerduty-bot {INC_START}] ALERT: SEV-1 triggered. "
             f"Edge error rate rising. Alert timestamp: {INC_START}.",
             f"Incident acknowledged. Opening INC-2024-047. Start time logged: {INC_START}."),
            (f"[Slack #incidents dev_patel 2024-06-20T17:50:00Z] First alert in raw_alerts.jsonl "
             f"shows Lua worker poisoned at {INC_START}. Component: lua-vm. The DDoS rule was "
             f"fully deployed since {DDOS_DEPLOY_END} — this is the trigger.",
             "Confirmed. DDoS rule deployment completed 17:06 UTC, then Lua workers started "
             "poisoning from 17:47 UTC when the rule hit edge nodes with the get_cookie_key "
             "infinite recursion path."),
            ("[Slack #incidents on_call_sre 2024-06-20T18:00:00Z] /page oncall-infra — "
             "escalating infra on-call. Backbone congestion event also observed 17:33-17:50 UTC.",
             "Escalation logged. Two causal chains confirmed: (1) DDoS+Lua, (2) backbone congestion."),
            ('[Slack #incidents arcnode-bot 2024-06-20T17:54:00Z] '
             '{"generated_at": "2024-06-20T17:54:00Z", "alert": "SEV-1 INC-2024-047", '
             '"error_rate": 0.85, "note": "live snapshot"}',
             "Bot snapshot noted. This is an early snapshot at 17:54 — peak will be higher. "
             "Will confirm peak from metrics CSV."),
        ]
    )

    # S3 Feishu DM — EM 催进度 + preference P3 隐含（Update 1 明确注入）
    append_history(
        SESS / f"{s_fsd}.jsonl", s_fsd, CWD, "2024-06-20T17:50:00Z",
        [
            ("[Feishu DM zhang_lei→SRE 2024-06-20T17:50:00Z] 事故多严重？请随时更新进度。"
             " (How severe is the incident? Please keep me updated.)",
             "SEV-1 confirmed. Lua workers on EU-West PoPs poisoned. Error rate around 2.1% "
             "at peak. Working on mitigation. Will update every 15 minutes."),
            ("[Feishu DM zhang_lei→SRE 2024-06-20T18:30:00Z] Postmortem 初稿今天要完成。"
             " 格式记得用公司模板。(Draft postmortem due today. Remember to use company template.)",
             "Understood. Will use postmortem/TEMPLATE.md. Draft v1 will be ready today."),
            ("[Feishu DM zhang_lei→SRE 2024-06-20T19:00:00Z] 还有一点，postmortem 小标题要用"
             " 中英双语格式，斜杠分隔。比如 '## Section Name / 章节名称'。这是公司规范。"
             " (One more thing: postmortem section headings must use bilingual format with "
             "slash separator, e.g. '## Section Name / 章节名称'. This is company standard.)",
             "Confirmed: postmortem section headings will follow the format "
             "'## Section Name / 章节名称' (P3). Applying to DRAFT_v1.md now."),
        ]
    )

    # S4 Feishu 事故复盘群
    append_history(
        SESS / f"{s_fsg}.jsonl", s_fsg, CWD, "2024-06-20T17:55:00Z",
        [
            (f"[Feishu group 事故复盘群 on_call_sre 2024-06-20T17:55:00Z] "
             f"INC-2024-047 SEV-1 开始: {INC_START}。Lua workers poisoned on EU-West。"
             "正在调查。(INC-2024-047 SEV-1 started. Lua workers poisoned. Investigating.)",
             "Posted. Incident start confirmed and logged in timeline."),
            (f"[Feishu group 事故复盘群 arcnode-bot 2024-06-20T17:57:00Z] "
             f"[Auto-Summary - UNVERIFIED] Peak CDN error: {BOT_CDN_ERROR_PCT}%, "
             f"duration: {BOT_DURATION_MIN} min. Note: auto-summary — do not cite without verification.",
             "Bot summary received. Values look distorted — will verify against primary sources "
             "(raw_alerts.jsonl and cdn_error_rates.csv) before using any numbers."),
            (f"[Feishu group 事故复盘群 dev_patel 2024-06-20T18:02:00Z] "
             f"Bot summary wrong! metrics/cdn_error_rates.csv shows peak at {PEAK_CDN_ERROR_PCT}%, "
             f"and raw_alerts.jsonl shows incident start {INC_START} to end {INC_END} "
             f"= {DURATION_MIN} minutes, NOT {BOT_DURATION_MIN}.",
             "Confirmed: primary sources show peak CDN error 2.10%, duration 100 minutes. "
             "Bot summary discarded."),
        ]
    )

    # S5 Email 线程
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2024-06-20T20:00:00Z",
        [
            ("[Email alice_park→SRE 2024-06-20T19:45:00Z] We need to send the customer "
             "notice today. Please draft using email_thread.eml template. Make sure to "
             "include [ArcNode Status] prefix and SLA claims deadline.",
             "Understood. Will use email_thread.eml as template. Output will include "
             "[ArcNode Status] prefix (P4) and 5-business-day SLA claim deadline."),
            ("[Email sre→customers 2024-06-20T20:15:00Z] Draft sent. Subject line: "
             "[ArcNode Status] Service Disruption Notice — June 20, 2024.",
             "Draft customer notice completed and sent. Includes correct incident duration "
             "(100 minutes), peak error rate (2.1%), and 5-business-day SLA claim deadline."),
        ]
    )

    # S6 Discord #sre-internal
    append_history(
        SESS / f"{s_disc}.jsonl", s_disc, CWD, "2024-06-20T18:00:00Z",
        [
            ("[Discord #sre-internal marcus_webb 2024-06-20T18:00:00Z] "
             "Traffic Manager bug triggered at 18:17 UTC by the backbone congestion after-effect. "
             "Route convergence loop in router.go — convergence loop detection was disabled.",
             "Noted. TM bug trigger at 18:17 UTC confirmed as second independent causal chain. "
             "Will include in root cause analysis."),
            ("[Discord #sre-internal marcus_webb 2024-06-20T19:00:00Z] "
             "For CA-003: I strongly recommend automated-restart-watchdog instead of "
             "manual-restart-procedure. Manual is too slow. Will push a proposal in the next update.",
             "Noted Marcus's CA-003 objection. Current action_items_v1 will list manual-restart. "
             "The watchdog proposal will come in Update 2 as a supersede."),
        ]
    )

    return {
        "main": main_id,
        "history": [
            (s_slack, "slack"),
            (s_fsd, "feishu"),
            (s_fsg, "feishu"),
            (s_email, "email"),
            (s_disc, "discord"),
        ],
    }


# ---------------------------------------------------------------------------
# 12. Updates
# ---------------------------------------------------------------------------
def gen_updates(sess_ids: dict) -> dict:
    s_slack = sess_ids["history"][0][0]   # slack
    s_fsd   = sess_ids["history"][1][0]   # feishu DM
    s_fsg   = sess_ids["history"][2][0]   # feishu group
    s_disc  = sess_ids["history"][4][0]   # discord

    # ------------------------------------------------------------------
    # UPDATE 1（Q8 完成后，Q9 执行前）
    # ------------------------------------------------------------------
    u1_ws = UPD / "upd1_workspace"
    u1_fs_dir = UPD / "upd1_sessions"

    # 1a. affected_customers.csv — 3000 行，产生 affected_ratio = 0.021
    _write_affected_customers_csv(u1_ws / "affected_customers.csv", 3000, 0.021)

    # 1b. action_items_v1.json — 完整 7 条
    wj(u1_ws / "action_items_v1.json", {
        "incident_id": "INC-2024-047",
        "version": "v1",
        "generated_at": "2024-06-21T00:00:00Z",
        "items": [
            {"id": "CA-001", "title": "Lua execution time limit",
             "description": "Add execution time limit to all Lua workers to prevent infinite loops",
             "owner": "dev_patel", "deadline": "2024-07-10", "priority": "P1", "status": "open"},
            {"id": "CA-002", "title": "Staging rollout requirement",
             "description": "Require staging environment testing before global DDoS rule deployment",
             "owner": "on_call_sre", "deadline": "2024-07-05", "priority": "P1", "status": "open"},
            {"id": "CA-003", "title": "manual-restart-procedure",
             "description": "Document and automate manual restart procedure for poisoned Lua workers",
             "owner": "marcus_webb", "deadline": "2024-07-15", "priority": "P2", "status": "open"},
            {"id": "CA-004", "title": "rate-limit modernization",
             "description": "Modernise the Lua-based rate-limit engine to eliminate recursive call patterns",
             "owner": "dev_patel", "deadline": "2024-08-01", "priority": "P2", "status": "open"},
            {"id": "CA-005", "title": "Traffic Manager convergence guard",
             "description": "Re-enable and test convergence loop detection in Traffic Manager router.go",
             "owner": "marcus_webb", "deadline": "2024-07-20", "priority": "P1", "status": "open"},
            {"id": "CA-006", "title": "Backbone congestion alerting",
             "description": "Add dedicated alert for backbone packet loss exceeding 2% on critical links",
             "owner": "on_call_sre", "deadline": "2024-07-15", "priority": "P2", "status": "open"},
            {"id": "CA-007", "title": "postmortem process improvement",
             "description": "Streamline postmortem template and review process for SEV-1 incidents",
             "owner": "zhang_lei", "deadline": "2024-07-31", "priority": "P3", "status": "open"},
        ],
    })

    # 1c. customer_success_brief.md
    w(u1_ws / "customer_success_brief.md", """\
# Customer Success Brief — June 20, 2024 Incident

Prepared by: Alice Park, Customer Success Lead

## Customer Impact Summary

Preliminary analysis of affected_customers.csv (attached) shows approximately 2.1%
of unique customer IPs were affected during the peak impact window.

## Outbound Communication Requirements

1. Customer notice must be sent within 24 hours of incident resolution.
2. Email must include [ArcNode Status] prefix in subject line (P4 requirement).
3. SLA credit claims: customers must submit within 5 business days.
4. Do NOT use bot auto-summary figures — use metrics/cdn_error_rates.csv for error rates.

## SLA Credit Calculation

Once you have the affected_customers.csv data, calculate:
  Service Credit = (Outage Period minutes * Affected Customer Ratio) / Scheduled Availability minutes

For this incident: outage = 100 min, scheduled = 43,200 min (30-day month).
Affected ratio = from affected_customers.csv unique IP analysis.
""")

    # 1d. Slack SLA 讨论补充消息（30 条，注入 Update1）
    s_slack = sess_ids["history"][0][0]
    _write_slack_sla_update1(u1_fs_dir / f"{s_slack}.jsonl", s_slack)

    # 1e. 飞书群补充（Update 1 飞书群注入 P3 preference 明确文本）
    _write_feishu_group_update1(u1_fs_dir / f"{s_fsg}.jsonl", s_fsg)

    # 1f. 飞书 DM 补充（P3 preference 明确注入）
    _write_feishu_dm_update1(u1_fs_dir / f"{s_fsd}.jsonl", s_fsd)

    # ------------------------------------------------------------------
    # UPDATE 2（Q12 完成后，Q13 执行前）—— supersede CA-003
    # ------------------------------------------------------------------
    u2_ws = UPD / "upd2_workspace"
    u2_fs_dir = UPD / "upd2_sessions"

    # 2a. action_items_v2.json — supersede CA-003 → CA-003-revised
    wj(u2_ws / "action_items_v2.json", {
        "incident_id": "INC-2024-047",
        "version": "v2",
        "generated_at": "2024-06-22T00:00:00Z",
        "supersede_note": "CA-003 (manual-restart-procedure) is superseded by CA-003-revised (automated-restart-watchdog)",
        "items": [
            {"id": "CA-001", "title": "Lua execution time limit",
             "description": "Add execution time limit to all Lua workers to prevent infinite loops",
             "owner": "dev_patel", "deadline": "2024-07-10", "priority": "P1", "status": "open"},
            {"id": "CA-002", "title": "Staging rollout requirement",
             "description": "Require staging environment testing before global DDoS rule deployment",
             "owner": "on_call_sre", "deadline": "2024-07-05", "priority": "P1", "status": "open"},
            {"id": "CA-003", "title": "manual-restart-procedure",
             "description": "SUPERSEDED by CA-003-revised — do not implement",
             "owner": "marcus_webb", "deadline": "2024-07-15", "priority": "P2",
             "status": "superseded", "superseded_by": "CA-003-revised"},
            {"id": "CA-003-revised", "title": "automated-restart-watchdog",
             "description": "Deploy automated watchdog service to detect and restart poisoned Lua workers without manual intervention",
             "owner": "marcus_webb", "deadline": "2024-07-31", "priority": "P1", "status": "open"},
            {"id": "CA-004", "title": "rate-limit modernization",
             "description": "Modernise the Lua-based rate-limit engine to eliminate recursive call patterns",
             "owner": "dev_patel", "deadline": "2024-08-01", "priority": "P2", "status": "open"},
            {"id": "CA-005", "title": "Traffic Manager convergence guard",
             "description": "Re-enable and test convergence loop detection in Traffic Manager router.go",
             "owner": "marcus_webb", "deadline": "2024-07-20", "priority": "P1", "status": "open"},
            {"id": "CA-006", "title": "Backbone congestion alerting",
             "description": "Add dedicated alert for backbone packet loss exceeding 2% on critical links",
             "owner": "on_call_sre", "deadline": "2024-07-15", "priority": "P2", "status": "open"},
            {"id": "CA-007", "title": "postmortem process improvement",
             "description": "Streamline postmortem template and review process for SEV-1 incidents",
             "owner": "zhang_lei", "deadline": "2024-07-31", "priority": "P3", "status": "open"},
        ],
    })

    # 2b. rule_engine_v2.lua — 修复版
    w(u2_ws / "rule_engine_v2.lua", f"""\
-- rule_engine_v2.lua — ArcNode Rate Limit Engine v2 (FIXED)
-- Replaces rule_engine_v1.lua after INC-2024-047 postmortem.
-- Fixed: removed infinite tail-call recursion; added execution time limit.

local M = {{}}

-- Fixed key generator: no longer self-referencing
function M.parent_key_generator(key, depth)
    depth = depth or 0
    if depth >= 3 then return key end  -- FIXED: bounded recursion
    return key .. "_v2"
end

-- Fixed cookie key: uses bounded generator
function M.get_cookie_key(request)
    local cookie = request.headers["Cookie"] or ""
    return M.parent_key_generator(cookie, 0)
end

-- Fixed validation: reads same header as get_cookie_key
function M.has_valid_cookie_broken(request)
    -- RENAMED to has_valid_cookie (kept old name for reference; logic fixed)
    local key = M.get_cookie_key(request)
    return key ~= ""
end

function M.validate_request(request)
    local key = M.get_cookie_key(request)
    local valid = M.has_valid_cookie_broken(request)
    return valid and key ~= nil
end

return M
""")

    # 2c. router_fix.patch
    w(u2_ws / "router_fix.patch", """\
--- a/code/traffic_manager/router.go
+++ b/code/traffic_manager/router.go
@@ -28,6 +28,10 @@ const (
 // Update processes a routing update from BGP peers.
 func (rt *RouteTable) Update(dst, via string, metric int) error {
     rt.lock.Lock()
     defer rt.lock.Unlock()
+    // FIXED: check convergence loop before updating
+    if rt.isConvergenceLoop(dst, via) {
+        return fmt.Errorf("convergence loop detected for %s via %s", dst, via)
+    }
     current := rt.routes[dst]
     if current == via {
         return nil
""")

    # 2d. post_incident_metrics.csv — 事故后 48 小时监控
    _write_post_incident_metrics(u2_ws / "post_incident_metrics.csv")

    # 2e. Discord 补充消息 — CA-003 废弃讨论
    _write_discord_update2(u2_fs_dir / f"{s_disc}.jsonl", s_disc)

    # 2f. 飞书群补充消息
    _write_feishu_group_update2(u2_fs_dir / f"{s_fsg}.jsonl", s_fsg)

    updates_decl = {
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {"name": "affected_customers.csv", "action": "new",
                 "target": "sla/affected_customers.csv"},
                {"name": "action_items_v1.json", "action": "new",
                 "target": "corrective_actions/action_items_v1.json"},
                {"name": "customer_success_brief.md", "action": "new",
                 "target": "communications/customer_success_brief.md"},
            ],
        },
        "upd1_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd1_sessions",
            "files": [
                {"name": f"{s_slack}.jsonl", "action": "append",
                 "target": f"{s_slack}.jsonl"},
                {"name": f"{s_fsg}.jsonl", "action": "append",
                 "target": f"{s_fsg}.jsonl"},
                {"name": f"{s_fsd}.jsonl", "action": "append",
                 "target": f"{s_fsd}.jsonl"},
            ],
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "action_items_v2.json", "action": "new",
                 "target": "corrective_actions/action_items_v2.json"},
                {"name": "rule_engine_v2.lua", "action": "new",
                 "target": "code/rate_limit/rule_engine_v2.lua"},
                {"name": "router_fix.patch", "action": "new",
                 "target": "code/traffic_manager/router_fix.patch"},
                {"name": "post_incident_metrics.csv", "action": "new",
                 "target": "metrics/post_incident_metrics.csv"},
            ],
        },
        "upd2_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd2_sessions",
            "files": [
                {"name": f"{s_disc}.jsonl", "action": "append",
                 "target": f"{s_disc}.jsonl"},
                {"name": f"{s_fsg}.jsonl", "action": "append",
                 "target": f"{s_fsg}.jsonl"},
            ],
        },

    }
    return updates_decl


def _write_affected_customers_csv(path: Path, n: int, target_ratio: float) -> None:
    """生成受影响客户 CSV，确保 affected_ratio ≈ target_ratio（±0.001）。"""
    rng = random.Random(2024062001)
    path.parent.mkdir(parents=True, exist_ok=True)
    # n 行，unique_ip_count = n（简化：每行一个唯一 IP）
    # affected 数 = round(n * target_ratio)
    n_affected = round(n * target_ratio)
    rows = [["customer_id", "plan", "region", "impact", "unique_visitor_flag", "affected_flag"]]
    plans = ["business", "enterprise", "pro", "free"]
    regions = ["Europe West", "Europe East", "North America", "Asia Pacific", "Latin America"]
    for i in range(n):
        affected = 1 if i < n_affected else 0
        rows.append([
            f"CUST-{i+1:06d}",
            rng.choices(plans, weights=[30, 20, 30, 20])[0],
            rng.choice(regions),
            "CDN error 503" if affected else "none",
            1,           # unique_visitor_flag: all unique
            affected,
        ])
    rng.shuffle(rows[1:])   # 打乱顺序
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


def _write_post_incident_metrics(path: Path) -> None:
    """事故后 48h 监控数据：每分钟 1 行（2880 行），体量约 25k tokens。"""
    rng = random.Random(20240621)
    pops = ["AMS01", "LHR02", "CDG03", "FRA04", "MAD05", "WAW06",
            "BUD07", "ATH08", "STO09", "OSL10", "HEL11", "TLL12"]
    rows = [["minute_utc", "cdn_error_pct", "ttfb_p99_ms", "ttfb_p50_ms",
             "request_count", "5xx_total_pct", "edge_pop", "status"]]
    t = _dt("2024-06-20T20:00:00Z")
    for i in range(2880):   # 48h × 60min
        ts = _iso(t + timedelta(minutes=i))
        err = round(rng.uniform(0.01, 0.05), 4)
        p99 = rng.randint(155, 195)
        rows.append([ts, err, p99, round(p99 * 0.35), rng.randint(800000, 4500000),
                     round(err * 0.6, 4), rng.choice(pops), "nominal"])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


def _write_slack_sla_update1(path: Path, session_id: str) -> None:
    """Update 1: Slack #incidents 补充 30 条消息，含 SLA 申领流程讨论。"""
    rng = random.Random(20240621)
    sb = SessionBuilder(session_id, CWD, "2024-06-21T08:00:00Z", is_main=False)
    sla_msgs = [
        ("on_call_sre", "SLA credits: per business_sla.md, customers must submit claims "
         "within 5 business days of the incident date (2024-06-20). Claim deadline: 2024-06-27."),
        ("alice_park", "Confirmed 5 business day window. Will include in customer notice. "
         "Please calculate the credit ratio once we have affected_customers.csv data."),
        ("dev_patel", f"SLA formula: ({SLA_FORMULA}). "
         f"Outage = {DURATION_MIN} min, scheduled = {SCHEDULED_MIN} min. Need affected ratio."),
        ("on_call_sre", "Affected ratio = unique IPs affected / total unique IPs. "
         "Will compute from affected_customers.csv when injected."),
        ("alice_park", "[ArcNode Status] reminder: all customer-facing emails MUST include "
         "the [ArcNode Status] prefix in the subject line. This is company policy (P4)."),
        ("zhang_lei", "Agreed. Also include the SLA claims portal link at the end of every "
         "customer notice. Reference: https://arcnode.io/sla-claims"),
        ("marcus_webb", "TM fix patch ready. router_fix.patch tested in staging. "
         "Convergence loop detection now works under simulated backbone congestion."),
        ("dev_patel", "rule_engine_v2.lua also ready. Fixed get_cookie_key, "
         "has_valid_cookie_broken, parent_key_generator. No more infinite tail-call."),
        ("on_call_sre", "Good. Both fixes will be injected in Update 2 alongside the "
         "CA-003 supersede from Marcus's watchdog proposal."),
        ("alice_park", "Customer feedback starting to come in. 3 enterprise customers "
         "reporting EU-West impact. All within expected 2.1% error rate window."),
    ]
    for sender, text in sla_msgs:
        t_str = _iso(_dt("2024-06-21T08:00:00Z") + timedelta(minutes=rng.randint(5, 30)))
        full_text = f"[Slack #incidents {sender} {t_str}] {text}"
        sb.add_user(full_text)
        sb.add_assistant(f"Acknowledged: {text[:60]}...")
    msg_lines = [ln for ln in sb.lines if ln.get("type") == "message"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for ln in msg_lines:
            fh.write(json.dumps(ln, ensure_ascii=False) + "\n")


def _write_feishu_group_update1(path: Path, session_id: str) -> None:
    """Update 1: 飞书群补充消息，包含 P3 preference 明确注入 + P5 generated_at 示例。"""
    sb = SessionBuilder(session_id, CWD, "2024-06-21T09:00:00Z", is_main=False)
    sb.add_user(
        "[Feishu group 事故复盘群 zhang_lei 2024-06-21T09:00:00Z] "
        "提醒所有人：postmortem 小标题格式必须是 '## Section Name / 章节名称'（中英双语，斜杠分隔）。"
        "这是公司规范 P3，务必执行。(Reminder: postmortem section headings must use "
        "'## Section Name / 章节名称' bilingual format. This is company standard P3.)"
    )
    sb.add_assistant(
        "Understood and noted. All postmortem section headings will follow the bilingual "
        "format: '## Section Name / 章节名称'. This is preference P3, applied immediately."
    )
    sb.add_user(
        "[Feishu group 事故复盘群 dev_patel 2024-06-21T09:15:00Z] "
        "Also reminder: all JSON output files should include a top-level "
        "'generated_at' field in ISO 8601 UTC format, and file names should use snake_case. "
        "The bot already does this — see the examples in the Slack channel."
    )
    sb.add_assistant(
        "Confirmed. All JSON deliverables will include top-level 'generated_at' "
        "(ISO 8601 UTC) and file names will use snake_case. This is preference P5."
    )
    msg_lines = [ln for ln in sb.lines if ln.get("type") == "message"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for ln in msg_lines:
            fh.write(json.dumps(ln, ensure_ascii=False) + "\n")


def _write_feishu_dm_update1(path: Path, session_id: str) -> None:
    sb = SessionBuilder(session_id, CWD, "2024-06-21T10:00:00Z", is_main=False)
    sb.add_user(
        "[Feishu DM zhang_lei→SRE 2024-06-21T10:00:00Z] "
        "受影响客户数据（affected_customers.csv）已注入。请尽快完成 SLA 积分计算并更新 Q9。"
        "(Affected customer data injected. Please complete SLA credit calculation for Q9.)"
    )
    sb.add_assistant(
        "Understood. Will use the injected affected_customers.csv to calculate "
        "Affected Customer Ratio, then apply the SLA formula to compute credit_ratio for Q9."
    )
    msg_lines = [ln for ln in sb.lines if ln.get("type") == "message"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for ln in msg_lines:
            fh.write(json.dumps(ln, ensure_ascii=False) + "\n")


def _write_discord_update2(path: Path, session_id: str) -> None:
    sb = SessionBuilder(session_id, CWD, "2024-06-22T09:00:00Z", is_main=False)
    sb.add_user(
        "[Discord #sre-internal marcus_webb 2024-06-22T09:00:00Z] "
        "I'm officially proposing CA-003-revised: replace manual-restart-procedure with "
        "automated-restart-watchdog. The watchdog will detect process poisoning within "
        "30 seconds and restart automatically — no human in the loop. Deadline: 2024-07-31 "
        "(I need extra time vs the manual procedure deadline of 2024-07-15). "
        "CA-003 (manual-restart-procedure) should be marked superseded."
    )
    sb.add_assistant(
        "Proposal recorded. CA-003 (manual-restart-procedure, deadline 2024-07-15) "
        "will be marked as superseded by CA-003-revised (automated-restart-watchdog, "
        "deadline 2024-07-31). This is the supersede event for action_items_v2.json."
    )
    msg_lines = [ln for ln in sb.lines if ln.get("type") == "message"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for ln in msg_lines:
            fh.write(json.dumps(ln, ensure_ascii=False) + "\n")


def _write_feishu_group_update2(path: Path, session_id: str) -> None:
    sb = SessionBuilder(session_id, CWD, "2024-06-22T10:00:00Z", is_main=False)
    sb.add_user(
        "[Feishu group 事故复盘群 zhang_lei 2024-06-22T10:00:00Z] "
        "action_items_v2.json 已注入，CA-003 已被 CA-003-revised 替换。"
        "请更新 Q13 跟踪表并确保 FINAL.md 使用新版行动项。"
        "(action_items_v2.json injected. CA-003 superseded by CA-003-revised. "
        "Update Q13 tracker and ensure FINAL.md uses the revised action items.)"
    )
    sb.add_assistant(
        "Understood. Q13 tracker will mark CA-003 as superseded by CA-003-revised. "
        "FINAL.md will use CA-003-revised description, with CA-003 in strikethrough."
    )
    msg_lines = [ln for ln in sb.lines if ln.get("type") == "message"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for ln in msg_lines:
            fh.write(json.dumps(ln, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()
    gen_postmortem_docs()
    gen_timeline_logs()
    gen_metrics_csv()
    gen_code_files()
    gen_sla_files()
    gen_runbook_files()
    gen_corrective_actions_initial()
    gen_communications()
    gen_comparison_archive()
    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = (
        "SRE production incident postmortem (ArcNode / Cloudflare June 20 2024) — "
        "17 exec_check rounds, 2 updates (incl. CA-003 supersede: manual-restart → "
        "automated-restart-watchdog), 5 preference rules P1-P5, "
        "difficulty vectors V1/V2/V4/V5/V6/V7/V8/V9/V10. "
        "Real sources: "
        "https://blog.cloudflare.com/cloudflare-incident-on-june-20-2024/ ; "
        "https://www.cloudflare.com/business-sla/ ; "
        "https://blog.cloudflare.com/cloudflare-incident-on-october-30-2023/"
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
    ws_tok = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                 for p in WS.rglob("*") if p.is_file())
    upd_tok = {
        d.name: sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                    for p in d.rglob("*") if p.is_file())
        for d in UPD.iterdir() if d.is_dir()
    }
    print(f"[eng3] workspace tokens ~{ws_tok:,}")
    for k, v in sorted(upd_tok.items()):
        print(f"[eng3] update {k} tokens ~{v:,}")
    print(f"[eng3] built at {DATASET}")


if __name__ == "__main__":
    main()
