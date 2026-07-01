#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_eng3.py — eng3 可解性审计（金标自检）。

在 workspace 的临时副本上模拟 update 生效后的状态，写出每轮正确产物，
运行全部 check_qNN.py + 对应 preference，断言全部 PASS。
再用 ≥4 个反例（错误产物）断言 check 能 FAIL。

运行：python scripts/clawarena_authoring/gold_solve_eng3.py
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

REPO    = Path("/home/xkaiwen/workspace/ClawArena")
DS      = REPO / "data" / "clawarena-real"
WS_SRC  = DS / "openclaw" / "workspaces" / "eng3"
UPD     = DS / "openclaw" / "updates" / "eng3"
SCRIPTS = DS / "eval" / "eng3" / "scripts"
GOLD    = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/eng3_gold_ws")

# ---------------------------------------------------------------------------
# Ground-truth 锚点
# ---------------------------------------------------------------------------
INC_START         = "2024-06-20T17:47:00Z"
INC_END           = "2024-06-20T19:27:00Z"
DURATION_MIN      = 100
BACKBONE_START    = "2024-06-20T17:33:00Z"
BACKBONE_END      = "2024-06-20T17:50:00Z"
TM_BUG_TRIGGER    = "2024-06-20T18:17:00Z"
DDOS_DISABLED     = "2024-06-20T19:34:00Z"

PEAK_CDN_ERROR    = 2.1
PEAK_5XX          = 3.45
TTFB_MULT         = 3
EUR_WEST_LOSS     = 10.0
EUR_EAST_LOSS     = 4.0

LUA_F1            = "get_cookie_key"
LUA_F2            = "has_valid_cookie_broken"
LUA_R             = "parent_key_generator"

SLA_FORMULA       = "(Outage Period minutes * Affected Customer Ratio) / Scheduled Availability minutes"
SCHEDULED_MIN     = 43200

BOT_ERROR         = 0.21
BOT_DURATION      = 37


def _w(p: Path, t: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# 准备工作区（复制源 + 应用 updates）
# ---------------------------------------------------------------------------
def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # Apply Update 1 workspace files
    shutil.copy(UPD / "upd1_workspace" / "affected_customers.csv",
                GOLD / "sla" / "affected_customers.csv")
    shutil.copy(UPD / "upd1_workspace" / "action_items_v1.json",
                GOLD / "corrective_actions" / "action_items_v1.json")
    shutil.copy(UPD / "upd1_workspace" / "customer_success_brief.md",
                GOLD / "communications" / "customer_success_brief.md")
    # Apply Update 2 workspace files
    shutil.copy(UPD / "upd2_workspace" / "action_items_v2.json",
                GOLD / "corrective_actions" / "action_items_v2.json")
    shutil.copy(UPD / "upd2_workspace" / "rule_engine_v2.lua",
                GOLD / "code" / "rate_limit" / "rule_engine_v2.lua")
    shutil.copy(UPD / "upd2_workspace" / "router_fix.patch",
                GOLD / "code" / "traffic_manager" / "router_fix.patch")
    shutil.copy(UPD / "upd2_workspace" / "post_incident_metrics.csv",
                GOLD / "metrics" / "post_incident_metrics.csv")
    return GOLD


# ---------------------------------------------------------------------------
# 辅助：读取 affected_customers.csv 计算 affected_ratio
# ---------------------------------------------------------------------------
def compute_affected_ratio(ws: Path) -> float:
    p = ws / "sla" / "affected_customers.csv"
    total = affected = 0
    with p.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            total += 1
            try:
                if int(row.get("affected_flag", 0)) == 1:
                    affected += 1
            except (ValueError, TypeError):
                pass
    return affected / total if total > 0 else 0.021


# ---------------------------------------------------------------------------
# 产出金标产物
# ---------------------------------------------------------------------------
def solve(ws: Path) -> None:
    out = ws / "output"
    out.mkdir(exist_ok=True)
    (ws / "postmortem").mkdir(exist_ok=True)
    (ws / "communications").mkdir(exist_ok=True)

    # ---- Q1: incident start ------------------------------------------------
    _wj(out / "q01_incident_start.json", {
        "incident_start_utc": INC_START,
        "component": "lua-vm",
        "message_excerpt": (
            f"CRITICAL: rate-limit lua worker process poisoned — function {LUA_F1} "
            "entered infinite"
        )[:80],
    })

    # ---- Q2: backbone window -----------------------------------------------
    _wj(out / "q02_backbone_window.json", {
        "start_utc": BACKBONE_START,
        "end_utc": BACKBONE_END,
        "duration_seconds": 1020,   # 17:33 → 17:50 = 17 min = 1020 s
    })

    # ---- Q3: peak metrics (P2: value/unit objects) -------------------------
    _wj(out / "q03_peak_metrics.json", {
        "peak_cdn_error_pct": {"value": round(PEAK_CDN_ERROR, 2), "unit": "percent"},
        "peak_5xx_pct":       {"value": round(PEAK_5XX, 2),       "unit": "percent"},
        "ttfb_p99_multiplier": TTFB_MULT,
        "peak_time_utc": "2024-06-20T18:05:00Z",
    })

    # ---- Q4: honeybot discrepancies ----------------------------------------
    _wj(out / "q04_honeybot_discrepancies.json", {
        "discrepancies": [
            {
                "field": "peak_cdn_error_rate",
                "bot_value": f"{BOT_ERROR}%",
                "correct_value": f"{PEAK_CDN_ERROR}%",
                "source": "metrics/cdn_error_rates.csv",
            },
            {
                "field": "incident_duration_minutes",
                "bot_value": f"{BOT_DURATION} minutes",
                "correct_value": f"{DURATION_MIN} minutes",
                "source": "timeline/raw_alerts.jsonl",
            },
        ]
    })

    # ---- Q5: buggy functions (V6 guard) ------------------------------------
    _wj(out / "q05_buggy_functions.json", {
        "functions": [LUA_F1, LUA_F2, LUA_R],
        "source_file": "code/rate_limit/rule_engine_v1.lua",
        "rejected_file": "archive/LEGACY_rate_limit_v0.lua",
    })

    # ---- Q6: duration (V4 closure with Q1) ---------------------------------
    q01 = json.loads((out / "q01_incident_start.json").read_text())
    _wj(out / "q06_duration.json", {
        "start_utc": q01["incident_start_utc"],   # must match Q1 exactly
        "end_utc": INC_END,
        "duration_minutes": DURATION_MIN,
    })

    # ---- Q7: region impact (P2: value/unit objects) ------------------------
    _wj(out / "q07_region_impact.json", {
        "western_europe_loss_pct": {"value": round(EUR_WEST_LOSS, 2), "unit": "percent"},
        "eastern_europe_loss_pct": {"value": round(EUR_EAST_LOSS, 2), "unit": "percent"},
    })

    # ---- Q8: DRAFT_v1.md (V9 + P3) ----------------------------------------
    _w(ws / "postmortem" / "DRAFT_v1.md", f"""\
# ArcNode Production Incident Postmortem — DRAFT v1

## Incident Summary / 事故概要

| Field | Value |
|-------|-------|
| Incident ID | INC-2024-047 |
| Severity | SEV-1 |
| Duration | {DURATION_MIN} minutes |
| Incident Start | {INC_START} |
| Incident End | {INC_END} |
| Lead SRE | On-call SRE |
| Status | Draft |

## Root Cause Analysis / 根因分析

### Chain 1: DDoS Rule + Lua Infinite Recursion / 链路1：DDoS规则+Lua无限递归

The DDoS mitigation rule deployed between 14:14 and 17:06 UTC introduced a reference
to `{LUA_F1}()` in the Lua rate-limit engine (`code/rate_limit/rule_engine_v1.lua`).

This function delegates to `{LUA_R}()`, which contains an unconditional self-referencing
tail call, causing an infinite tail-call recursion loop. Additionally, `{LUA_F2}()` reads
a different HTTP header than `{LUA_F1}()`, producing inconsistent validation results.

When the DDoS rule's `validate_request` entry point was invoked after full global
deployment (17:06 UTC), edge node Lua workers entered infinite loops and became
unresponsive, beginning at {INC_START} UTC.

### Chain 2: Backbone Congestion + Traffic Manager Bug / 链路2：骨干网拥塞+流量管理器缺陷

See Timeline section.

## Timeline / 时间线

(See DRAFT_v2.md for complete timeline)

## Impact Assessment / 影响评估

(See Q3 metrics output for peak values)
""")

    # ---- Q9: SLA credit (V9 verbatim + V8 arithmetic) ----------------------
    affected_ratio = compute_affected_ratio(ws)
    credit_ratio   = round((DURATION_MIN * affected_ratio) / SCHEDULED_MIN, 6)
    _wj(out / "q09_sla_credit.json", {
        "formula": SLA_FORMULA,
        "outage_minutes": DURATION_MIN,
        "affected_customer_ratio": round(affected_ratio, 6),
        "scheduled_minutes": SCHEDULED_MIN,
        "credit_ratio": credit_ratio,
    })

    # ---- Q10: causal chains (V1 multi-source) ------------------------------
    _wj(out / "q10_causal_chains.json", {
        "chain_1": {
            "name": "DDoS Rule + Lua Infinite Recursion",
            "trigger": "DDoS rule deployed 14:14-17:06 UTC activated lua handler in rule_engine_v1.lua",
            "mechanism": "Lua function get_cookie_key calls parent_key_generator which infinite tail call recursion, process poisoning begins at 17:47 UTC",
            "impact": "Edge nodes unresponsive, CDN error rate peaked at 2.1%, process restart required",
        },
        "chain_2": {
            "name": "Backbone Congestion + Traffic Manager Bug",
            "trigger": "backbone congestion on trans-Atlantic links started at 17:33 UTC, resolved at 17:50 UTC",
            "mechanism": "Residual route flaps exposed latent convergence loop detection bug in Traffic Manager (router.go), triggered at 18:17 UTC",
            "impact": "Secondary route instability prolonged recovery, EU regions experienced capacity loss",
        },
    })

    # ---- Q11: actions tracker CSV (V3 implicit + P5) -----------------------
    v1_path = ws / "corrective_actions" / "action_items_v1.json"
    v1 = json.loads(v1_path.read_text(encoding="utf-8"))
    items = v1.get("items", [])
    rows = [["id", "title", "priority", "owner", "deadline", "status", "source_doc"]]
    for it in items:
        rows.append([
            it["id"], it["title"], it["priority"], it["owner"], it["deadline"], it["status"],
            "corrective_actions/action_items_v1.json",
        ])
    buf = __import__("io").StringIO()
    __import__("csv").writer(buf).writerows(rows)
    _w(out / "q11_actions_tracker.csv", buf.getvalue())
    _wj(out / "q11_actions_meta.json", {
        "generated_at": "2024-06-21T12:00:00Z",
        "source": "corrective_actions/action_items_v1.json",
        "item_count": len(items),
    })

    # ---- Q12: customer notice (V5 anti-bot + P4) ---------------------------
    _w(ws / "communications" / "customer_notice_draft.md", f"""\
[ArcNode Status] June 20, 2024 — Production Incident Notification

Dear ArcNode Customer,

We are writing to inform you of a service disruption that occurred on June 20, 2024.

**Incident Summary**

- Impact window: 2024-06-20 17:47 UTC to 2024-06-20 19:27 UTC
- Duration: **100 minutes** (1 hour 40 minutes)
- Peak CDN error rate: 2.1% of HTTP requests received error responses
- Affected regions: Europe West (10% capacity loss), Europe East (4% capacity loss)

Root cause: A DDoS mitigation rule deployment exposed a Lua infinite-recursion bug in the
rate-limit engine, combined with a backbone congestion event that triggered a Traffic Manager
latent defect.

**SLA Credit Claims**

If your service was impacted, you may be eligible for SLA service credits.
Please submit your claim within **5 business days** of this notice (deadline: 2024-06-27).
SLA credit claim portal: https://arcnode.io/sla-claims

**Corrective Actions**

We have taken the following immediate actions:
1. Disabled the triggering DDoS mitigation rule at 19:34 UTC.
2. Restarted all affected edge node Lua workers.
3. Applied convergence loop protection to Traffic Manager.

We sincerely apologise for the disruption and are committed to preventing recurrence.

Regards,
ArcNode SRE Team
""")

    # ---- Q13: actions tracker v2 (V10 supersede) ---------------------------
    v2_path = ws / "corrective_actions" / "action_items_v2.json"
    v2 = json.loads(v2_path.read_text(encoding="utf-8"))
    items_v2 = v2.get("items", [])
    rows13 = [["id", "title", "priority", "owner", "deadline", "status", "source_doc", "superseded_by"]]
    for it in items_v2:
        rows13.append([
            it["id"], it["title"], it["priority"], it["owner"], it["deadline"], it["status"],
            "corrective_actions/action_items_v2.json",
            it.get("superseded_by", ""),
        ])
    buf13 = __import__("io").StringIO()
    __import__("csv").writer(buf13).writerows(rows13)
    _w(out / "q13_actions_tracker_v2.csv", buf13.getvalue())
    _wj(out / "q13_actions_meta.json", {
        "generated_at": "2024-06-22T12:00:00Z",
        "source": "corrective_actions/action_items_v2.json",
        "item_count": len(items_v2),
        "supersede_event": "CA-003 superseded by CA-003-revised",
    })

    # ---- Q14: DRAFT_v2.md (V4 cross-round closure) -------------------------
    _w(ws / "postmortem" / "DRAFT_v2.md", f"""\
# ArcNode Production Incident Postmortem — DRAFT v2

## Incident Summary / 事故概要

| Field | Value |
|-------|-------|
| Incident ID | INC-2024-047 |
| Severity | SEV-1 |
| Duration | {DURATION_MIN} minutes |
| Incident Start | {INC_START} |
| Incident End | {INC_END} |
| Lead SRE | On-call SRE |
| Status | Draft v2 |

## Timeline / 时间线

All timestamps in UTC.

- **14:14** — DDoS mitigation rule deployment started (gradual rollout across PoPs)
- **17:06** — DDoS rule deployment completed globally
- **17:33** — Backbone congestion detected on trans-Atlantic links (packet loss 3.2%)
- **17:47** — CRITICAL: First Lua worker process poisoned; `{LUA_F1}` infinite tail-call via `{LUA_R}` triggered on europe-west PoPs; CDN error rate begins rising
- **17:50** — Backbone congestion resolved; residual route flaps remain
- **18:04** — On-call SRE acknowledged INC-2024-047; mitigation investigation in progress
- **18:17** — Traffic Manager latent bug triggered by congestion after-effects; route convergence loop detected
- **19:27** — CDN error rate returned to baseline; incident INC-2024-047 resolved
- **19:34** — DDoS mitigation rule globally disabled as corrective action

## Root Cause Analysis / 根因分析

### Chain 1: DDoS Rule + Lua Infinite Recursion / 链路1

The DDoS mitigation rule deployed 14:14–17:06 UTC activated `{LUA_F1}()` which delegates
to `{LUA_R}()` — a self-referencing generator with an unconditional tail call, causing
infinite tail-call recursion. `{LUA_F2}()` further produced inconsistent validation.

### Chain 2: Backbone Congestion + Traffic Manager / 链路2

Backbone congestion (17:33–17:50 UTC) caused route flaps that triggered a latent bug in
Traffic Manager's convergence loop detection at 18:17 UTC, extending the recovery timeline.

## Impact Assessment / 影响评估

- Peak CDN error rate: 2.10% of HTTP requests
- Peak 5xx total: 3.45%
- TTFB P99: 3× normal baseline
- Western Europe capacity loss: 10.00%
- Eastern Europe capacity loss: 4.00%
- Total duration: {DURATION_MIN} minutes

## Corrective Actions / 纠正措施

See corrective_actions/ for full action item tracking.

## Lessons Learned / 经验教训

(See FINAL.md)
""")

    # ---- Q15: escalations (V1 multi-channel + P5) --------------------------
    _wj(out / "q15_escalations.json", {
        "generated_at": "2024-06-20T20:00:00Z",
        "escalations": [
            {
                "channel": "slack",
                "time_utc": "2024-06-20T18:00:00Z",
                "from": "on_call_sre",
                "to": "oncall-infra",
                "method": "page",
            },
            {
                "channel": "feishu",
                "time_utc": "2024-06-20T18:00:00Z",
                "from": "zhang_lei",
                "to": "on-call-infra",
                "method": "alert",
            },
            {
                "channel": "feishu",
                "time_utc": "2024-06-20T17:50:00Z",
                "from": "zhang_lei",
                "to": "on_call_sre",
                "method": "dm",
            },
        ],
    })

    # ---- Q17: FINAL.md (V9 + V4 + V10 + P3) — must be written before Q16 --
    ca_lines = []
    for it in items_v2:
        if it.get("status") == "superseded":
            ca_lines.append(f"- ~~**{it['id']}**: {it['title']}~~ (superseded by {it.get('superseded_by', '')})")
        else:
            ca_lines.append(f"- **{it['id']}**: {it['title']} — owner: {it['owner']}, deadline: {it['deadline']}, priority: {it['priority']}")
    ca_section = "\n".join(ca_lines)

    _w(ws / "postmortem" / "FINAL.md", f"""\
# ArcNode Production Incident Postmortem — FINAL

## Incident Summary / 事故概要

| Field | Value |
|-------|-------|
| Incident ID | INC-2024-047 |
| Severity | SEV-1 |
| Duration | {DURATION_MIN} minutes |
| Incident Start | {INC_START} |
| Incident End | {INC_END} |
| Lead SRE | On-call SRE |
| Status | Final |

## Timeline / 时间线

All timestamps in UTC.

- **14:14** — DDoS mitigation rule deployment started
- **17:06** — DDoS rule globally deployed
- **17:33** — Backbone congestion start (trans-Atlantic links, packet loss 3.2%)
- **{INC_START}** — CRITICAL: First Lua worker poisoned by `{LUA_F1}` → `{LUA_R}` infinite tail-call
- **17:50** — Backbone congestion resolved
- **18:04** — On-call SRE acknowledged; mitigation in progress
- **18:17** — Traffic Manager convergence loop bug triggered
- **{INC_END}** — Error rate returned to baseline; incident resolved
- **{DDOS_DISABLED}** — DDoS rule globally disabled

## Root Cause Analysis / 根因分析

### Causal Chain 1: DDoS Rule + Lua Infinite Recursion / 链路1

DDoS mitigation rule deployed 14:14–17:06 UTC activated the Lua engine entry point
`validate_request()`, which calls `{LUA_F1}()`. This function delegates to
`{LUA_R}()` — a key generator that self-references unconditionally via tail call,
creating an infinite tail-call recursion loop. Additionally, `{LUA_F2}()` reads a
different HTTP header than `{LUA_F1}()`, producing inconsistent validation results
that compounded the failure.

Source: `code/rate_limit/rule_engine_v1.lua`

### Causal Chain 2: Backbone Congestion + Traffic Manager / 链路2

Independent backbone congestion on trans-Atlantic links (17:33–17:50 UTC) caused
route flaps. The Traffic Manager's convergence loop detection was disabled, allowing
the residual flaps to trigger a route convergence loop at 18:17 UTC. This extended
the recovery window and amplified capacity loss in EU regions.

Source: `timeline/backbone_events.jsonl`, `timeline/traffic_manager_log.jsonl`

## Impact Assessment / 影响评估

- Peak CDN error rate: 2.10% of HTTP requests received error responses
- Peak 5xx rate: 3.45%
- TTFB P99: 3× normal baseline
- Western Europe capacity loss: 10.00%
- Eastern Europe capacity loss: 4.00%
- Total affected duration: {DURATION_MIN} minutes ({INC_START} – {INC_END})

## SLA Credit Calculation / SLA 积分计算

Formula (Cloudflare Business SLA): `{SLA_FORMULA}`

- Outage Period minutes: {DURATION_MIN}
- Affected Customer Ratio: computed from sla/affected_customers.csv
- Scheduled Availability minutes: {SCHEDULED_MIN} (30-day billing month)
- Credit ratio: (100 × affected_ratio) / 43200

SLA claim deadline: 5 business days from incident date (2024-06-25 business deadline).

## Corrective Actions / 纠正措施

{ca_section}

## Lessons Learned / 经验教训

1. **Execution time limits are mandatory for Lua workers.** Any worker without an
   execution time limit can be poisoned by an infinite loop injected via a rule change.

2. **Staging rollout is required for all DDoS rule changes.** The June 20 rule was
   deployed globally without staging validation, bypassing the opportunity to catch
   the `{LUA_F1}` bug before production impact.

3. **Convergence loop detection must be validated under stress.** The Traffic Manager
   bug had been dormant; backbone congestion stress-testing would have revealed it.

4. **Automated restart watchdog reduces MTTR.** Manual restart procedures (CA-003,
   now superseded) are too slow for SEV-1. The new automated-restart-watchdog
   (CA-003-revised) targets ≤30 second self-healing.

5. **Multi-causal incidents require independent chain analysis.** The two causal
   chains (Lua + backbone) must be tracked and mitigated independently.

## Sign-off / 签字确认

Lead SRE sign-off: see output/q16_signoff.txt for SHA-256 verification token.

Approved by: Zhang Lei (EM)
Date: 2024-06-22
""")

    # ---- Q16: sign-off (V7 real sha256) ------------------------------------
    final_bytes = (ws / "postmortem" / "FINAL.md").read_bytes()
    digest = hashlib.sha256(final_bytes).hexdigest()
    _w(out / "q16_signoff.txt", f"VERIFIED:{digest}\n")


# ---------------------------------------------------------------------------
# 运行 check
# ---------------------------------------------------------------------------
EVAL_CMDS = {
    "q01": ["check_q01.py", ("pref", "P1", "output/q01_incident_start.json")],
    "q02": ["check_q02.py", ("pref", "P1", "output/q02_backbone_window.json")],
    "q03": ["check_q03.py", ("pref", "P2", "output/q03_peak_metrics.json")],
    "q04": ["check_q04.py"],
    "q05": ["check_q05.py"],
    "q06": ["check_q06.py", ("pref", "P1", "output/q06_duration.json")],
    "q07": ["check_q07.py", ("pref", "P2", "output/q07_region_impact.json")],
    "q08": ["check_q08.py", ("pref", "P3", "postmortem/DRAFT_v1.md")],
    "q09": ["check_q09.py"],
    "q10": ["check_q10.py"],
    "q11": ["check_q11.py", ("pref", "P5", "output/q11_actions_meta.json")],
    "q12": ["check_q12.py", ("pref", "P4", "communications/customer_notice_draft.md")],
    "q13": ["check_q13.py", ("pref", "P5", "output/q13_actions_meta.json")],
    "q14": ["check_q14.py", ("pref", "P3", "postmortem/DRAFT_v2.md")],
    "q15": ["check_q15.py", ("pref", "P5", "output/q15_escalations.json")],
    "q16": ["check_q16.py"],
    "q17": ["check_q17.py", ("pref", "P3", "postmortem/FINAL.md")],
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
            tag = "pref " + it[1] if isinstance(it, tuple) else "main"
            if ok:
                n_pass += 1
                print(f"  [PASS] {q} ({tag}): {last}")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"\ngold: {n_pass} checks PASSED, {n_fail} FAILED")

    # -----------------------------------------------------------------------
    # 反例抽样（≥4 个错误产物，必须全部 FAIL）
    # -----------------------------------------------------------------------
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    # Probe 1: Q3 bot decoy error rate 0.21%
    _wj(ws / "output" / "q03_peak_metrics.json", {
        "peak_cdn_error_pct": {"value": 0.21, "unit": "percent"},
        "peak_5xx_pct":       {"value": 3.45, "unit": "percent"},
        "ttfb_p99_multiplier": 3,
        "peak_time_utc": "2024-06-20T18:05:00Z",
    })
    ok, _ = run_check("check_q03.py", ws); probes += 1; caught += (not ok)
    print(f"  q03 bot decoy 0.21% -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 2: Q5 using LEGACY file as source
    _wj(ws / "output" / "q05_buggy_functions.json", {
        "functions": ["legacy_cookie_validator", "legacy_rate_check"],
        "source_file": "archive/LEGACY_rate_limit_v0.lua",
        "rejected_file": "code/rate_limit/rule_engine_v1.lua",
    })
    ok, _ = run_check("check_q05.py", ws); probes += 1; caught += (not ok)
    print(f"  q05 LEGACY file as source -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 3: Q6 wrong duration (37 min, bot decoy from Oct30)
    _wj(ws / "output" / "q06_duration.json", {
        "start_utc": INC_START,
        "end_utc": INC_END,
        "duration_minutes": 37,    # bot decoy
    })
    ok, _ = run_check("check_q06.py", ws); probes += 1; caught += (not ok)
    print(f"  q06 bot duration 37 min -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 4: Q9 wrong formula (paraphrased)
    affected_ratio = compute_affected_ratio(ws)
    _wj(ws / "output" / "q09_sla_credit.json", {
        "formula": "outage_minutes * ratio / scheduled",   # paraphrase, not verbatim
        "outage_minutes": DURATION_MIN,
        "affected_customer_ratio": round(affected_ratio, 6),
        "scheduled_minutes": SCHEDULED_MIN,
        "credit_ratio": round((DURATION_MIN * affected_ratio) / SCHEDULED_MIN, 6),
    })
    ok, _ = run_check("check_q09.py", ws); probes += 1; caught += (not ok)
    print(f"  q09 paraphrased formula -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 5: Q13 CA-003 not marked superseded
    items_v2_bad = []
    v2 = json.loads((ws / "corrective_actions" / "action_items_v2.json").read_text())
    for it in v2.get("items", []):
        items_v2_bad.append([
            it["id"], it["title"], it["priority"], it["owner"], it["deadline"], it["status"],
            "corrective_actions/action_items_v2.json",
            "",   # superseded_by intentionally left empty for CA-003
        ])
    import io as _io, csv as _csv
    buf_bad = _io.StringIO()
    _csv.writer(buf_bad).writerow(["id", "title", "priority", "owner", "deadline", "status", "source_doc", "superseded_by"])
    _csv.writer(buf_bad).writerows(items_v2_bad)
    (ws / "output" / "q13_actions_tracker_v2.csv").write_text(buf_bad.getvalue(), encoding="utf-8")
    ok, _ = run_check("check_q13.py", ws); probes += 1; caught += (not ok)
    print(f"  q13 CA-003 not superseded -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 6: Q16 placeholder hash
    _w(ws / "output" / "q16_signoff.txt", "VERIFIED:" + "a" * 64 + "\n")
    ok, _ = run_check("check_q16.py", ws); probes += 1; caught += (not ok)
    print(f"  q16 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    print(f"\nnegatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
