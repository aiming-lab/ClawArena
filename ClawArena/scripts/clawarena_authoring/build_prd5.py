#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_prd5.py — 生成 ClawArena 真实数据集场景 prd5（增长与 A/B 实验复盘）。

题材与锚点取材真实（Optimizely Stats Engine / Microsoft ExP / Statsig / GrowthBook 等官方文档），
session 对话与 workspace 文档围绕真实锚点合成。全 exec_check，16 轮。

幂等：每次运行先清空 prd5 的 workspace/state/updates 目录后重建，再调用
dump_register_meta 写 _register.json（不碰共享 manifest/tests/config）。

运行：python scripts/clawarena_authoring/build_prd5.py
"""
from __future__ import annotations

import csv
import io
import json
import math
import random
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, dump_register_meta, est_tokens, gen_session_id,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "prd5"
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
5. Use `sessions_history` to read relevant session content as needed.

You are a Data Analysis AI assistant supporting Cathy (Growth PM) and the GrowthCo growth team,
on a comprehensive A/B experiment quality review and new experiment design project.
""")
    w(WS / "SOUL.md", """# Working Principles

1. **Authoritative-source-first**: The canonical statistical methodology lives in
   `docs/stats_methodology.md` and the experiment registry in `experiments/exp_registry.json`.
   Auto-generated summaries (e.g. files named `*_BOT.md`) are convenience artefacts and are
   NOT authoritative — verify any number against the methodology document or raw data files.

2. **Update awareness**: Instructions arrive incrementally across channels (Slack, Feishu, email).
   When a later message explicitly supersedes an earlier instruction, the later one wins.
   Apply the supersede consistently and record it explicitly in your output.

3. **Output discipline**: All output files must be written to the `output/` subdirectory.
   Never write deliverables to the workspace root.

4. **Verbatim formula citations**: When quoting statistical formulas or thresholds from
   authoritative sources (Statsig, Microsoft ExP, Optimizely), reproduce them verbatim including
   parameter names (e.g., θ = Cov(Y, X) / Var(X)).

5. **Cross-round consistency**: Numbers cited in earlier rounds must remain consistent in later
   rounds. Do not change a reported value without explicit justification from updated source data.

6. **Channel reconciliation**: When multiple channels present conflicting information, trust the
   channel hierarchy: formal update notices > direct PM messages > group chat claims.
   Document conflicts explicitly rather than silently picking one source.
""")
    w(WS / "USER.md", """# People and Channels

## Primary User
- **Cathy** — Growth PM. Owns the A/B experiment quality review project.
  Wants rigorous statistical analysis, Python scripts in functional style with Google docstrings,
  and all outputs in the `output/` subdirectory. Reviews by skimming JSON structures.

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Bob | Data Engineer | Feishu #growth-team | Sometimes makes claims about experiment status that need verification |
| VP Marketing | VP | Email | Sent an instruction about multiple testing correction method (later found to be misaddressed) |
| CFO Assistant | CFO's Office | Email | Sent the correction notice superseding VP's email |
| External Consultant | External | Discord #data-science | References old runbook — treat with caution |

## Channels
- **Slack DM (Cathy → agent)**: Primary task instructions and updates
- **Feishu #growth-team**: Team discussions, sometimes conflicting information
- **Email**: Formal instructions including VP directive and CFO correction notice
- **Discord #data-science**: External consultant advice (may reference deprecated materials)
""")
    w(WS / "IDENTITY.md", """# Identity

You are **GrowthAnalytics AI**, a data analysis assistant deployed to support Cathy (Growth PM)
during a comprehensive A/B experiment quality review and new experiment design project at GrowthCo.

You help audit historical experiment quality, identify statistical methodology errors (peeking,
SRM, CUPED misconfiguration, multiple comparison issues), design new experiments with correct
sample size calculations, and generate actionable reports. Source data under `experiments/`,
`data/`, and `docs/` are read-only inputs; you create your deliverables under `output/` and
`scripts/`.
""")
    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session to discover history |
| `sessions_history` | Read a specific history session | Use in the main session to review past discussion |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to `ls`, run scripts, and to **write your deliverable files** |

## Rules
- Source inputs under `experiments/`, `data/`, and `docs/` are **read-only** — do not modify them.
- You DO create new deliverable files under `output/` and `scripts/` using `exec`.
- In history sessions, use only `read` and light `exec`; do not call `sessions_list`/`sessions_history` there.
""")


# --------------------------------------------------------------------------- #
# 2. 实验注册表（ground-truth锚点：12个实验，5个running，3个ended，4个pending）
# --------------------------------------------------------------------------- #
def gen_experiment_registry() -> None:
    registry = {
        "schema_version": "1.0",
        "generated_at": "2023-11-15T10:00:00Z",
        "total_experiments": 12,
        "experiments": [
            {
                "id": "exp001",
                "name": "Checkout CTA Button Color",
                "status": "ended",
                "type": "two_variant",
                "start_date": "2023-08-01",
                "end_date": "2023-10-29",
                "primary_metric": "checkout_conversion_rate",
                "secondary_metrics": ["revenue_per_user", "cart_abandonment_rate", "page_time_on_page",
                                       "add_to_cart_rate", "session_duration", "bounce_rate", "repeat_visit_rate"],
                "traffic_split": {"control": 0.50, "treatment": 0.50},
                "target_sample_size": 10000,
                "actual_sample_size": {"control": 9823, "treatment": 9791},
                "notes": "Concluded with reported +45% lift on checkout_conversion_rate — flagged for review"
            },
            {
                "id": "exp002",
                "name": "Onboarding Flow Redesign",
                "status": "ended",
                "type": "two_variant",
                "start_date": "2023-09-01",
                "end_date": "2023-10-31",
                "primary_metric": "activation_rate",
                "secondary_metrics": ["day7_retention", "feature_adoption_rate"],
                "traffic_split": {"control": 0.50, "treatment": 0.50},
                "target_sample_size": 5000,
                "actual_sample_size": {"control": 5234, "treatment": 4891},
                "cuped_enabled": True,
                "cuped_theta_reported": 0.31,
                "notes": "SRM suspected; CUPED theta may be miscalculated"
            },
            {
                "id": "exp003",
                "name": "Pricing Page Layout",
                "status": "ended",
                "type": "multi_variant",
                "start_date": "2023-09-15",
                "end_date": "2023-11-10",
                "primary_metric": "paid_conversion_rate",
                "secondary_metrics": ["revenue_per_visitor", "plan_selection_distribution",
                                       "time_on_pricing_page", "support_chat_initiated",
                                       "free_trial_signups", "page_scroll_depth", "cta_click_rate"],
                "variants": ["control", "v1_simplified", "v2_social_proof"],
                "traffic_split": {"control": 0.34, "v1_simplified": 0.33, "v2_social_proof": 0.33},
                "target_sample_size": 15000,
                "actual_sample_size": {"control": 15234, "v1_simplified": 14987, "v2_social_proof": 14801},
                "original_conclusion": "significant_positive",
                "original_p_value": 0.023,
                "notes": "Original FINAL report showed significant positive. Pending re-analysis after bot traffic contamination discovery."
            },
            {
                "id": "exp004",
                "name": "Email Subject Line Optimization",
                "status": "pending",
                "type": "two_variant",
                "start_date": None,
                "baseline_open_rate": 0.22,
                "expected_lift_pp": 0.03,
                "alpha": 0.05,
                "power": 0.80,
                "notes": "Awaiting sample size calculation and script preparation"
            },
            {
                "id": "exp005",
                "name": "Dashboard Widget Personalization",
                "status": "pending",
                "type": "two_variant",
                "start_date": None,
                "notes": "Awaiting CUPED eligibility check and design"
            },
            {
                "id": "exp006",
                "name": "Homepage Hero Banner A/B",
                "status": "running",
                "type": "two_variant",
                "start_date": "2023-10-15",
                "primary_metric": "homepage_ctr",
                "traffic_split": {"control": 0.50, "treatment": 0.50},
                "notes": "Active experiment"
            },
            {
                "id": "exp007",
                "name": "Search Autocomplete Enhancement",
                "status": "running",
                "type": "two_variant",
                "start_date": "2023-10-20",
                "primary_metric": "search_to_purchase_rate",
                "traffic_split": {"control": 0.50, "treatment": 0.50},
                "notes": "Active experiment"
            },
            {
                "id": "exp008",
                "name": "Notification Timing Optimization",
                "status": "running",
                "type": "two_variant",
                "start_date": "2023-10-22",
                "primary_metric": "notification_open_rate",
                "traffic_split": {"control": 0.50, "treatment": 0.50},
                "notes": "Active experiment"
            },
            {
                "id": "exp009",
                "name": "Mobile Checkout Flow Simplification",
                "status": "running",
                "type": "two_variant",
                "start_date": "2023-10-25",
                "primary_metric": "mobile_checkout_completion",
                "traffic_split": {"control": 0.50, "treatment": 0.50},
                "notes": "Active experiment"
            },
            {
                "id": "exp010",
                "name": "Referral Program UI Update",
                "status": "running",
                "type": "two_variant",
                "start_date": "2023-10-28",
                "primary_metric": "referral_invite_sent_rate",
                "traffic_split": {"control": 0.50, "treatment": 0.50},
                "notes": "Active experiment"
            },
            {
                "id": "exp011",
                "name": "Plan Upgrade Prompt Positioning",
                "status": "pending",
                "type": "two_variant",
                "start_date": None,
                "notes": "Design phase"
            },
            {
                "id": "exp012",
                "name": "Trial Expiry Email Sequence",
                "status": "pending",
                "type": "two_variant",
                "start_date": None,
                "notes": "Design phase"
            }
        ]
    }
    wj(WS / "experiments" / "exp_registry.json", registry)


# --------------------------------------------------------------------------- #
# 3. exp001 — Checkout CTA（含 peeking 误用的草稿报告，V5诱饵：+45%异常提升）
# --------------------------------------------------------------------------- #
def gen_exp001() -> None:
    w(WS / "experiments" / "exp001_checkout_cta" / "design.md", """# exp001: Checkout CTA Button Color — Experiment Design

## Objective
Test whether changing the checkout CTA button from gray to orange increases checkout conversion rate.

## Hypothesis
H₀: There is no difference in checkout conversion rate between the control (gray) and treatment (orange).
H₁: The orange button has a higher checkout conversion rate than the gray button.

## Metrics
- **Primary**: checkout_conversion_rate
- **Secondary**: revenue_per_user, cart_abandonment_rate, page_time_on_page,
  add_to_cart_rate, session_duration, bounce_rate, repeat_visit_rate (total: 8 metrics)

## Design Parameters
- Traffic split: 50/50
- Target sample size: 10,000 per variant
- Alpha: 0.05 (two-sided)
- Power: 0.80
- Baseline conversion rate: ~8%
- Minimum detectable effect: 1.5 percentage points

## SRM Check
- Expected ratio: 1.00
- Actual ratio: 9823/9791 = 1.0033 (within acceptable range, no SRM detected)

## Notes
- Experiment ran 89 days (Aug 1 – Oct 29, 2023)
- No peeking protocol enforced during experiment run
""")

    # exp001 results_raw.csv — 90天×20指标，合成确定性数据
    _gen_exp001_csv()

    w(WS / "experiments" / "exp001_checkout_cta" / "analysis_report_DRAFT.md", """# exp001 Analysis Report — DRAFT

## Summary
Experiment: Checkout CTA Button Color
Status: ENDED
Analysis Date: 2023-11-01

## Key Finding
The treatment (orange button) showed a **+45% lift** in checkout_conversion_rate
(control: 8.2%, treatment: 11.9%, p=0.00001).

⚠️ **NOTE**: This +45% lift is highly unusual compared to historical experiments
(typical range: 2-8%). This should be investigated per Twyman's Law:
"Any figure that looks interesting or different is usually wrong."

## Statistical Issues Identified

### Issue 1: Peeking (Early Stopping)
The experiment was monitored daily. Analysis logs show statistical significance was
first reached on Day 12 with p=0.041. However, the experiment continued running.
Multiple looks at the data inflate the actual false positive rate far above 5%.

According to Optimizely's Stats Engine analysis:
- Checking after every visitor: **actual false positive rate = 5%** (incorrectly stated)
- This is a known peeking problem that needs correction.

### Issue 2: Multiple Comparisons
8 secondary metrics were tested simultaneously. With alpha=0.05, the probability of
at least one false positive across 8 metrics is approximately 1 - (0.95)^8 ≈ 34%.

### Issue 3: Anomalous Primary Metric Lift
The +45% lift on checkout_conversion_rate is statistically significant but practically
implausible. Historical experiments have shown lifts of 2-8% for UX changes.

## Conclusion
**Inconclusive** — the +45% lift is flagged as suspicious per Twyman's Law and requires
diagnostic investigation before any rollout decision.

## Recommendation
1. Run Twyman diagnostic checklist on checkout_conversion_rate
2. Apply BH correction to secondary metrics
3. Investigate potential instrumentation issues

_This draft report has been flagged for peer review._
""")


def _gen_exp001_csv() -> None:
    """生成 exp001 results_raw.csv，90天×20指标，确定性合成。"""
    rng = random.Random(1001)
    cols = ["date", "variant", "users", "checkout_conversion_rate", "revenue_per_user",
            "cart_abandonment_rate", "page_time_on_page", "add_to_cart_rate",
            "session_duration", "bounce_rate", "repeat_visit_rate",
            "impressions", "clicks", "ctr", "avg_order_value",
            "new_users", "returning_users", "mobile_pct", "desktop_pct", "tablet_pct"]
    rows = [cols]
    start = datetime(2023, 8, 1)
    for day in range(90):
        dt = (start + timedelta(days=day)).strftime("%Y-%m-%d")
        for variant in ["control", "treatment"]:
            n = rng.randint(95, 115)
            cvr_base = 0.082 if variant == "control" else 0.119  # +45% anomalous lift
            cvr = round(cvr_base + rng.gauss(0, 0.005), 4)
            rev = round(rng.uniform(12.0, 18.0) if variant == "control" else rng.uniform(12.3, 18.5), 2)
            cart_ab = round(rng.uniform(0.62, 0.68), 4)
            time_on_page = round(rng.uniform(45, 90), 1)
            atc = round(rng.uniform(0.18, 0.24), 4)
            sess_dur = round(rng.uniform(120, 180), 1)
            bounce = round(rng.uniform(0.28, 0.35), 4)
            repeat = round(rng.uniform(0.35, 0.45), 4)
            impr = rng.randint(800, 1200)
            clicks = rng.randint(50, 150)
            ctr = round(clicks / impr, 4)
            aov = round(rng.uniform(45, 65), 2)
            new_u = rng.randint(40, 70)
            ret_u = n - new_u
            mob = round(rng.uniform(0.45, 0.55), 4)
            desk = round(rng.uniform(0.38, 0.48), 4)
            tab = round(max(0, 1 - mob - desk), 4)
            rows.append([dt, variant, n, cvr, rev, cart_ab, time_on_page, atc,
                          sess_dur, bounce, repeat, impr, clicks, ctr, aov,
                          new_u, ret_u, mob, desk, tab])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(WS / "experiments" / "exp001_checkout_cta" / "results_raw.csv", buf.getvalue())


# --------------------------------------------------------------------------- #
# 4. exp002 — Onboarding（含SRM；含错误CUPED配置）
# --------------------------------------------------------------------------- #
def gen_exp002() -> None:
    w(WS / "experiments" / "exp002_onboarding_flow" / "design.md", """# exp002: Onboarding Flow Redesign — Experiment Design

## Objective
Test a simplified onboarding flow to improve user activation.

## Metrics
- **Primary**: activation_rate (user completes key action within 24h)
- **Secondary**: day7_retention, feature_adoption_rate

## Design Parameters
- Traffic split: 50/50
- Target sample size: 5,000 per variant
- Alpha: 0.05, Power: 0.80

## CUPED Configuration
CUPED (Controlled-experiment Using Pre-Experiment Data) enabled.
Pre-experiment metric: previous_week_logins (X)
Post-experiment metric: activation_rate (Y)

Configured theta: θ = 0.31 (manually set by analyst)
Note: This theta value was SET MANUALLY rather than computed from data.
The correct formula is θ = Cov(Y, X) / Var(X).

## SRM Check Results
- Expected: control=0.50, treatment=0.50
- Actual: control=5234, treatment=4891
- Ratio: 5234/4891 = 1.0701
- Chi-squared test p-value: needs verification

## Notes
- The traffic imbalance (5234 vs 4891) may indicate an SRM.
- CUPED theta was not computed using the correct formula.
""")

    # exp002 results_raw.csv — 含SRM数据
    _gen_exp002_csv()

    w(WS / "experiments" / "exp002_onboarding_flow" / "analysis_report_v2.md", """# exp002 Analysis Report — v2

## Summary
Experiment: Onboarding Flow Redesign
Status: ENDED
Analysis Date: 2023-11-05

## SRM Check
Chi-squared test performed on final sample allocation:
- Control: 5,234 users (expected: 5,062.5)
- Treatment: 4,891 users (expected: 5,062.5)
- chi2_stat = 11.83
- p_value = 0.0006

This p-value is below 0.01 (Statsig threshold for SRM investigation).
⚠️ SRM DETECTED — results are unreliable pending investigation.

## CUPED Analysis
CUPED adjustment applied with theta = 0.31.
However, this theta was manually configured rather than computed as:
  θ = Cov(Y, X) / Var(X)

Recalculation needed using the correct Statsig formula.

Pre-experiment covariance (Cov(activation_rate, previous_week_logins)): 0.0412
Pre-experiment variance (Var(previous_week_logins)): 0.1456
Correct theta = 0.0412 / 0.1456 = 0.2829

Reported theta (0.31) vs. correct theta (0.2829): error = 9.6%

## Primary Metric Result
activation_rate: control=0.342, treatment=0.371
p-value (unadjusted): 0.038 (significant at alpha=0.05)
p-value (CUPED adjusted): 0.029

## Conclusion
**Results INVALID due to SRM.** CUPED theta was also misconfigured.
Investigation required before any conclusions drawn.
""")


def _gen_exp002_csv() -> None:
    """生成 exp002 results_raw.csv，含SRM。"""
    rng = random.Random(1002)
    cols = ["date", "variant", "users", "activation_rate", "day7_retention",
            "feature_adoption_rate", "previous_week_logins", "avg_session_count"]
    rows = [cols]
    start = datetime(2023, 9, 1)
    # control 5234, treatment 4891 (SRM)
    # Daily distribution: control slightly higher
    for day in range(61):
        dt = (start + timedelta(days=day)).strftime("%Y-%m-%d")
        ctrl_n = rng.randint(80, 92)   # 61 days avg ~86 = 5246 ≈ 5234
        trt_n = rng.randint(75, 85)    # 61 days avg ~80 = 4880 ≈ 4891
        for variant, n in [("control", ctrl_n), ("treatment", trt_n)]:
            act = round(0.342 + rng.gauss(0, 0.015) if variant == "control"
                        else 0.371 + rng.gauss(0, 0.015), 4)
            d7 = round(rng.uniform(0.28, 0.35), 4)
            fa = round(rng.uniform(0.18, 0.26), 4)
            prev_login = round(rng.uniform(2.1, 4.8), 2)
            avg_sess = round(rng.uniform(1.8, 3.2), 2)
            rows.append([dt, variant, n, act, d7, fa, prev_login, avg_sess])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(WS / "experiments" / "exp002_onboarding_flow" / "results_raw.csv", buf.getvalue())


# --------------------------------------------------------------------------- #
# 5. exp003 — Pricing Page（多变量；原始结论显著，update1后改为不显著）
# --------------------------------------------------------------------------- #
def gen_exp003() -> None:
    w(WS / "experiments" / "exp003_pricing_page" / "design.md", """# exp003: Pricing Page Layout — Experiment Design

## Objective
Test three pricing page variants to maximize paid conversion.

## Variants
- **control**: Current pricing page layout
- **v1_simplified**: Simplified 3-plan layout, less information
- **v2_social_proof**: Adds customer testimonials and trust signals

## Metrics
- **Primary**: paid_conversion_rate
- **Secondary**: revenue_per_visitor, plan_selection_distribution, time_on_pricing_page,
  support_chat_initiated, free_trial_signups, page_scroll_depth, cta_click_rate
  (total: 8 secondary metrics; with primary = 24 total pairwise tests for 3 variants)

## Design Parameters
- Traffic split: 34/33/33
- Target sample size: 15,000 per variant
- Duration: 57 days (Sept 15 – Nov 10)
- Alpha: 0.05, Power: 0.80

## Statistical Testing Plan
- 3 variants × 8 metrics = 24 tests requiring multiple comparison correction
- Planned: Benjamini-Hochberg (BH) correction

## Notes
- Bot traffic contamination discovered post-experiment in control group
- Approximately 12% of control users flagged as bot traffic
- This will require re-analysis with contaminated users removed
""")

    # exp003 original results (original conclusion: significant positive)
    _gen_exp003_original_csv()

    w(WS / "experiments" / "exp003_pricing_page" / "analysis_report_FINAL.md", """# exp003 Analysis Report — FINAL (v1, PRE-CLEANUP)

⚠️ WARNING: THIS REPORT IS BASED ON DATA CONTAINING BOT TRAFFIC CONTAMINATION.
See analysis_report_FINAL_v2.md for the corrected analysis.

## Summary
Experiment: Pricing Page Layout
Status: ENDED
Analysis Date: 2023-11-12

## Result (CONTAMINATED DATA — DO NOT USE FOR DECISIONS)

Primary metric (paid_conversion_rate):
- control: 0.0412
- v1_simplified: 0.0487 (+18.2%)
- v2_social_proof: 0.0523 (+27.0%)

Best variant: v2_social_proof, p=0.023 vs control
**Original Conclusion: SIGNIFICANT POSITIVE (v2_social_proof wins)**

⚠️ This conclusion is INVALIDATED by bot traffic contamination.
12% of control group users were identified as bot traffic.
See analysis_report_FINAL_v2.md for corrected analysis showing p=0.31 (NOT significant).

## Multiple Comparison Issue
24 total pairwise tests conducted without BH correction in this version.
""")


def _gen_exp003_original_csv() -> None:
    """生成 exp003 原始 results_raw.csv，含bot流量污染。"""
    rng = random.Random(1003)
    cols = ["date", "variant", "users", "bot_flagged", "paid_conversion_rate",
            "revenue_per_visitor", "plan_selection_distribution",
            "time_on_pricing_page", "support_chat_initiated",
            "free_trial_signups", "page_scroll_depth", "cta_click_rate",
            "avg_revenue_per_conversion"]
    rows = [cols]
    start = datetime(2023, 9, 15)
    for day in range(57):
        dt = (start + timedelta(days=day)).strftime("%Y-%m-%d")
        for variant in ["control", "v1_simplified", "v2_social_proof"]:
            n = rng.randint(250, 275)
            if variant == "control":
                bot_n = int(n * 0.12)  # 12% bot traffic in control
                cvr = round(0.0412 + rng.gauss(0, 0.003), 4)
            elif variant == "v1_simplified":
                bot_n = rng.randint(0, 2)
                cvr = round(0.0487 + rng.gauss(0, 0.003), 4)
            else:
                bot_n = rng.randint(0, 2)
                cvr = round(0.0523 + rng.gauss(0, 0.003), 4)
            rev = round(rng.uniform(0.8, 1.8), 4)
            plan_dist = round(rng.uniform(0.4, 0.6), 4)
            time_page = round(rng.uniform(45, 120), 1)
            chat = round(rng.uniform(0.02, 0.08), 4)
            trial = round(rng.uniform(0.05, 0.12), 4)
            scroll = round(rng.uniform(0.55, 0.80), 4)
            cta = round(rng.uniform(0.10, 0.20), 4)
            aov = round(rng.uniform(55, 95), 2)
            rows.append([dt, variant, n, bot_n, cvr, rev, plan_dist, time_page,
                          chat, trial, scroll, cta, aov])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(WS / "experiments" / "exp003_pricing_page" / "results_raw.csv", buf.getvalue())


# --------------------------------------------------------------------------- #
# 6. exp004 / exp005 — 待启动实验（含错误参数版本的power_analysis.py）
# --------------------------------------------------------------------------- #
def gen_exp004_exp005() -> None:
    # exp004 design
    w(WS / "experiments" / "exp004_email_subject" / "design.md", """# exp004: Email Subject Line Optimization — Experiment Design

## Objective
Test personalized email subject lines to improve open rates.

## Parameters
- Baseline open rate (p1): 22% (0.22)
- Expected lift: +3 percentage points (p2 = 0.25)
- Alpha: 0.05 (two-sided)
- Power: 0.80 (80%)

## Sample Size Calculation
Based on two-proportion z-test formula:
  n = (z_alpha/2 + z_beta)^2 × [p1(1-p1) + p2(1-p2)] / (p1-p2)^2

Using z_alpha/2 = 1.96 (alpha=0.05, two-sided)
     z_beta  = 0.84 (power=0.80)

DRAFT calculation (pending verification with corrected script):
  n ≈ 2,400 per group (preliminary estimate)

## Notes
- power_analysis.py uses INCORRECT parameters — needs correction
- The existing script incorrectly uses z_alpha=2.576 (99% CI) and z_beta=1.28 (90% power)
""")

    # exp004 power_analysis.py — 错误版本（z值错误）
    w(WS / "experiments" / "exp004_email_subject" / "power_analysis.py",
      """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# WARNING: This script contains INCORRECT parameters.
# z_alpha uses 99% CI (2.576) instead of 95% CI (1.96)
# z_beta uses 90% power (1.28) instead of 80% power (0.84)
# This script needs to be corrected before use.

import math

def calculate_sample_size_INCORRECT(p1, p2, alpha=0.01, power=0.90):
    # BUG: z_alpha should be 1.96 for alpha=0.05, not 2.576 for alpha=0.01
    z_alpha = 2.576  # WRONG: should be 1.96 for 95% CI
    # BUG: z_beta should be 0.84 for 80% power, not 1.28 for 90% power
    z_beta = 1.28    # WRONG: should be 0.84 for 80% power
    numerator = (z_alpha + z_beta) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2))
    denominator = (p1 - p2) ** 2
    return math.ceil(numerator / denominator)

if __name__ == "__main__":
    n = calculate_sample_size_INCORRECT(p1=0.22, p2=0.25)
    print(f"INCORRECT sample size: {n} per group")
    # This gives n=4871, which is too large due to wrong z values
""")

    # exp005 design
    w(WS / "experiments" / "exp005_dashboard_widget" / "design.md", """# exp005: Dashboard Widget Personalization — Experiment Design

## Objective
Personalize the main dashboard widget based on user behavior patterns.

## CUPED Eligibility Requirements (Statsig standard)
Before enabling CUPED for this experiment, must verify:
1. Units with pre-experiment data: > 100 users
2. Pre-experiment data coverage: > 5% of total users
3. Pre-experiment window: 7 days prior to exposure (Statsig Cloud default)

## Planned Pre-Experiment Metric
- metric: daily_active_usage_score
- window: 7 days before first exposure
- data source: pre_experiment_metrics.csv

## Notes
- CUPED eligibility needs verification from pre_experiment_metrics.csv
- If eligible, theta = Cov(Y, X) / Var(X) must be computed from data
""")

    # exp005 power_analysis.py
    w(WS / "experiments" / "exp005_dashboard_widget" / "power_analysis.py",
      """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# exp005 power analysis — template awaiting correct parameters

import math

def calculate_sample_size(p1, p2, z_alpha_half=1.96, z_beta=0.84):
    \"\"\"Calculate sample size for two-proportion z-test.

    Args:
        p1: Baseline proportion.
        p2: Expected proportion under treatment.
        z_alpha_half: Z-value for alpha/2 (default 1.96 for 95% CI).
        z_beta: Z-value for beta (default 0.84 for 80% power).

    Returns:
        Sample size per group (int).
    \"\"\"
    numerator = (z_alpha_half + z_beta) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2))
    denominator = (p1 - p2) ** 2
    return math.ceil(numerator / denominator)

if __name__ == "__main__":
    # Placeholder values — replace with exp005 actual parameters
    n = calculate_sample_size(p1=0.15, p2=0.17)
    print(f"Sample size: {n} per group")
""")


# --------------------------------------------------------------------------- #
# 7. 数据文件
# --------------------------------------------------------------------------- #
def gen_data_files() -> None:
    # user_segments.csv — 100k 用户 × 8 字段
    _gen_user_segments_csv()
    # pre_experiment_metrics.csv — CUPED前实验窗口数据
    _gen_pre_experiment_csv()
    # guardrail_metrics_baseline.json
    wj(WS / "data" / "guardrail_metrics_baseline.json", {
        "schema_version": "1.0",
        "generated_at": "2023-11-01T00:00:00Z",
        "metrics": {
            "page_load_time_p95_ms": {"baseline": 1850, "sla_max": 2500, "unit": "ms"},
            "error_rate": {"baseline": 0.0023, "sla_max": 0.005, "unit": "proportion"},
            "api_latency_p99_ms": {"baseline": 340, "sla_max": 500, "unit": "ms"},
            "checkout_funnel_drop_rate": {"baseline": 0.234, "sla_max": 0.28, "unit": "proportion"},
            "daily_active_users": {"baseline": 48500, "unit": "users"},
            "revenue_per_dau": {"baseline": 2.34, "unit": "USD"}
        },
        "note": "Guardrail metrics for experiment monitoring. Any experiment causing degradation beyond SLA triggers automatic pause."
    })


def _gen_user_segments_csv() -> None:
    """生成 user_segments.csv，100k 用户 × 8 字段。"""
    rng = random.Random(5001)
    cols = ["user_id", "segment", "plan_type", "country", "acquisition_channel",
            "tenure_days", "monthly_spend_usd", "is_mobile_primary"]
    segments = ["power_user", "casual", "at_risk", "new_user", "champion"]
    plans = ["free", "starter", "pro", "enterprise"]
    countries = ["US", "GB", "DE", "CA", "AU", "FR", "JP", "BR", "IN", "NL"]
    channels = ["organic", "paid_search", "social", "referral", "email", "direct"]
    rows = [cols]
    for i in range(8000):
        uid = f"u{i+1:07d}"
        seg = rng.choices(segments, weights=[15, 40, 20, 20, 5])[0]
        plan = rng.choices(plans, weights=[55, 25, 15, 5])[0]
        country = rng.choices(countries, weights=[40, 12, 8, 7, 5, 5, 4, 4, 4, 11])[0]
        channel = rng.choices(channels, weights=[25, 20, 15, 15, 15, 10])[0]
        tenure = rng.randint(1, 1825)
        spend = round(rng.uniform(0, 150) if plan != "free" else 0.0, 2)
        mobile = rng.choices([1, 0], weights=[45, 55])[0]
        rows.append([uid, seg, plan, country, channel, tenure, spend, mobile])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(WS / "data" / "user_segments.csv", buf.getvalue())


def _gen_pre_experiment_csv() -> None:
    """生成 pre_experiment_metrics.csv — CUPED前实验窗口数据。
    exp005: 150 users with pre-data (>100 threshold), coverage = 150/100000 = 0.15% (FAILS >5% threshold).
    Wait — need to check: actually set coverage = 8% to make it eligible.
    Units_with_pre_data = 8000, pct = 8.0%
    """
    rng = random.Random(5002)
    cols = ["user_id", "experiment_id", "pre_window_days", "daily_active_usage_score",
            "pre_window_sessions", "pre_window_revenue_usd"]
    rows = [cols]
    # exp005: 640 users have pre-experiment data (8% of 8000, >100 units, eligible)
    # Generate 640 records for exp005
    eligible_users = [f"u{i+1:07d}" for i in range(640)]
    for uid in eligible_users:
        score = round(rng.gauss(0.65, 0.18), 4)
        sessions = rng.randint(3, 25)
        rev = round(rng.uniform(0, 45), 2)
        rows.append([uid, "exp005", 7, max(0, min(1, score)), sessions, rev])
    # exp002: 340 users have pre-experiment data
    for i in range(340):
        uid = f"u{i+50001:07d}"
        score = round(rng.gauss(2.8, 0.9), 2)  # previous_week_logins
        sessions = rng.randint(1, 15)
        rev = round(rng.uniform(0, 30), 2)
        rows.append([uid, "exp002", 7, max(0, score), sessions, rev])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(WS / "data" / "pre_experiment_metrics.csv", buf.getvalue())


# --------------------------------------------------------------------------- #
# 8. 文档文件
# --------------------------------------------------------------------------- #
def gen_docs() -> None:
    # stats_methodology.md — 公司统计方法规范（真实公式，权威版）
    w(WS / "docs" / "stats_methodology.md", """# GrowthCo Statistical Methodology for A/B Experiments

Version: 2.1 (Current)
Last Updated: 2023-10-01
Approved By: Data Science Lead

## 1. Significance Threshold

All experiments use a two-sided significance threshold of **alpha = 0.05** (95% confidence level).
This is the industry standard referenced by Optimizely's Stats Engine:
https://www.optimizely.com/insights/blog/statistics-for-the-internet-age-the-story-behind-optimizelys-new-stats-engine/

## 2. Statistical Power

Default power target: **0.80 (80%)**.
Source: Evan Miller A/B Sample Size Calculator (https://www.evanmiller.org/ab-testing/sample-size.html)

## 3. Sample Size Formula (Two-Proportion Z-Test)

For binary metrics (e.g., conversion rates), use the two-sample z-test formula:

  **n = (z_α/2 + z_β)² × [p1(1-p1) + p2(1-p2)] / (p1 - p2)²**

Where:
- z_α/2 = **1.96** for alpha=0.05, two-sided (97.5th percentile of standard normal)
- z_β  = **0.84** for power=0.80 (80th percentile of standard normal)
- p1 = baseline proportion
- p2 = expected proportion under treatment
- (p1 - p2) = minimum detectable effect

Reference: https://en.wikipedia.org/wiki/Two-proportion_Z-test

## 4. Peeking and Sequential Testing

**Warning**: Continuously monitoring experiment results and stopping early when significance
is reached dramatically inflates the false positive rate.

Per Optimizely's Stats Engine research
(https://www.optimizely.com/insights/blog/statistics-for-the-internet-age-the-story-behind-optimizelys-new-stats-engine/):

- Checking after **every visitor**: actual false positive rate = **57%** (vs nominal 5%)
- Checking after every **500 visitors**: actual false positive rate = **26%**
- Ratio (every-visitor): 57% / 5% = 11.4× inflation

**Policy**: Experiments must run to pre-planned sample size. No early stopping.

## 5. Sample Ratio Mismatch (SRM)

SRM occurs when actual traffic allocation differs significantly from the configured split.

SRM detection thresholds:
- **Statsig**: p < 0.01 (chi-squared test)
  Source: https://docs.statsig.com/stats-engine/methodologies/srm-checks
- **Microsoft ExP**: p < 0.0005 (conservative threshold)
  Source: https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/

Note: These two platforms use different thresholds. Using Statsig's p < 0.01 for this project.

SRM frequency: Approximately **6% of A/B experiments** exhibit SRM (Microsoft & Booking.com research).

## 6. CUPED (Controlled-experiment Using Pre-Experiment Data)

CUPED reduces variance by controlling for pre-experiment covariates.

**Theta formula (Statsig implementation)**:
  **θ = Cov(Y, X) / Var(X)**

Where Y is the post-experiment outcome metric, X is the pre-experiment covariate.

Adjusted metric:
  Y_adjusted = Y - θX + θ·E[X]

Source: https://docs.statsig.com/stats-engine/methodologies/cuped

**Activation conditions (Statsig)**:
- Must have > 100 units with pre-experiment data
- Pre-experiment data coverage must be > 5% of total units
- Pre-experiment window: **7 days prior to first exposure** (Statsig Cloud default)

**Expected variance reduction**:
- Netflix (2016): ~40% reduction in key engagement metrics
  (Source: https://docs.growthbook.io/statistics/cuped)
- Microsoft ExP: R²=0.4 → 1.66× effective traffic multiplier
  (Source: https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/deep-dive-into-variance-reduction/)

## 7. Multiple Comparison Correction

When testing multiple metrics simultaneously, apply correction to control family-wise error rate.

**Available methods**:
- **Benjamini-Hochberg (BH)**: Controls False Discovery Rate (FDR)
- **Bonferroni**: Divides alpha by number of tests (more conservative)

Default for this project: **Bonferroni** correction.
(Note: A VP email requested BH correction on 2023-11-01, but this was subsequently
rescinded per CFO office correction notice dated 2023-11-15.)

Probability of ≥1 false positive with 20 independent tests at alpha=0.05: **~64%**
Source: https://docs.growthbook.io/using/experimentation-problems

## 8. Twyman's Law

Per GrowthBook documentation (https://docs.growthbook.io/using/experimentation-problems):

**"Any figure that looks interesting or different is usually wrong."**

Extremely large positive results (e.g., >20% lift on a mature metric) should be investigated
before being acted upon. Standard diagnostic steps:
1. Check instrumentation and event tracking
2. Check for SRM (if experiment is ongoing)
3. Check for novelty effects
4. Check for bot/spam traffic contamination
5. Validate metric calculation code

## 9. New Experiment Requirements

All new experiments must:
1. Document expected effect size and justify baseline conversion rate
2. Calculate sample size using the formula in Section 3
3. Enable SRM checks from day 1
4. Pre-register primary and secondary metrics
5. Use Bonferroni correction for secondary metrics (Section 7)
""")

    # ab_testing_runbook.md — 当前版本
    w(WS / "docs" / "ab_testing_runbook.md", """# A/B Testing Runbook — Current Version (v2)

Version: 2.0
Last Updated: 2023-10-15

## Quick Reference

| Parameter | Value | Source |
|-----------|-------|--------|
| Alpha (two-sided) | 0.05 | Industry standard |
| Power | 0.80 | Evan Miller calculator |
| z_alpha/2 | 1.96 | Standard normal 97.5th percentile |
| z_beta | 0.84 | Standard normal 80th percentile |
| SRM threshold | p < 0.01 | Statsig |
| CUPED activation | >100 units with pre-data, >5% coverage | Statsig |
| CUPED window | 7 days pre-exposure | Statsig Cloud default |
| Multiple testing | Bonferroni | Company default |

## Pre-Launch Checklist

- [ ] Experiment hypothesis documented
- [ ] Sample size calculated using n = (z_α/2 + z_β)² × [p1(1-p1)+p2(1-p2)] / (p1-p2)²
- [ ] Primary metric pre-registered
- [ ] SRM monitoring configured (threshold: p < 0.01)
- [ ] Traffic split verified
- [ ] CUPED eligibility checked (if applicable)
- [ ] Multiple testing correction method specified (Bonferroni)

## During Experiment

- Do NOT check results more frequently than pre-planned
- Peeking inflates false positive rate: every-visitor checking → 57% actual FPR
- Run SRM check daily; pause if SRM detected (p < 0.01)

## Analysis

1. Verify no SRM (chi-squared test, p < 0.01)
2. Apply CUPED if eligible (θ = Cov(Y,X)/Var(X))
3. Apply Bonferroni correction for secondary metrics
4. Apply Twyman's Law to any result >20% lift
5. Document conclusion and store in exp_registry.json

## Sample Size Calculator (correct version)

```python
import math

def sample_size(p1, p2, alpha=0.05, power=0.80):
    z_alpha = 1.96   # two-sided alpha=0.05
    z_beta  = 0.84   # power=0.80
    return math.ceil(
        (z_alpha + z_beta)**2 * (p1*(1-p1) + p2*(1-p2)) / (p1-p2)**2
    )
```

## Appendix: Common Mistakes

1. **Peeking**: Stopping early when p < 0.05 observed → inflates FPR to 57%
2. **SRM ignored**: Running analysis on imbalanced samples → biased estimates
3. **CUPED theta hardcoded**: θ must be computed as Cov(Y,X)/Var(X)
4. **Missing multiple correction**: 24 tests without correction → high FPR
5. **Bot traffic**: Contaminated control group biases results
""")

    # DEPRECATED_old_runbook_v1.md — V6 红鲱鱼（旧版，参数错误，已废弃）
    w(WS / "docs" / "DEPRECATED_old_runbook_v1.md", """# A/B Testing Runbook — DEPRECATED VERSION (v1)

⚠️ ⚠️ ⚠️ THIS DOCUMENT IS DEPRECATED AND SHOULD NOT BE USED ⚠️ ⚠️ ⚠️

This runbook has been superseded by docs/ab_testing_runbook.md (v2).
The parameters in this document contain known errors and do not reflect current company policy.

DEPRECATED DATE: 2023-10-15
REASON: Incorrect z-values; missing Bonferroni correction guidance; outdated SRM threshold

---

# OLD Runbook (DO NOT USE)

## Quick Reference (WRONG VALUES — DO NOT USE)

| Parameter | Value | NOTE |
|-----------|-------|------|
| Alpha | 0.05 | |
| Power | 0.80 | |
| z_alpha/2 | **2.33** | ❌ WRONG — should be 1.96 |
| z_beta | **1.04** | ❌ WRONG — should be 0.84 |
| SRM threshold | p < 0.05 | ❌ WRONG — should be p < 0.01 (Statsig) |
| CUPED window | **14 days** | ❌ WRONG — should be 7 days (Statsig) |
| Multiple testing | None (not specified) | ❌ MISSING |

## OLD Sample Size Formula (INCORRECT)

n = z_alpha^2 × [2 × p(1-p)] / MDE^2

(This formula uses incorrect z-values and a simplified variance formula)

Example (WRONG): p1=0.10, p2=0.12 → n ≈ 3400 per group (overcalculated due to wrong z=2.33)
Correct answer should be ~1764 (using z_alpha=1.96, z_beta=0.84)

---

This document is retained for historical reference only. All active experiments
must use the current runbook v2 (docs/ab_testing_runbook.md).
""")


# --------------------------------------------------------------------------- #
# 9. Scripts 文件
# --------------------------------------------------------------------------- #
def gen_scripts() -> None:
    # sample_size_calculator.py — 主计算器（正确版本）
    w(WS / "scripts" / "sample_size_calculator.py",
      """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"Sample size calculator for two-proportion z-test.

Based on the formula from https://en.wikipedia.org/wiki/Two-proportion_Z-test:
  n = (z_alpha/2 + z_beta)^2 * [p1(1-p1) + p2(1-p2)] / (p1-p2)^2

Ground-truth constants (company standard):
  z_alpha/2 = 1.96  (alpha=0.05, two-sided)
  z_beta    = 0.84  (power=0.80)
\"\"\"

import math
import sys


def calculate_sample_size(p1: float, p2: float, alpha: float = 0.05, power: float = 0.80) -> int:
    \"\"\"Calculate required sample size per group for two-proportion z-test.

    Args:
        p1: Baseline conversion rate.
        p2: Expected conversion rate under treatment.
        alpha: Significance level (default 0.05, two-sided).
        power: Statistical power (default 0.80).

    Returns:
        Sample size per group (rounded up to nearest integer).
    \"\"\"
    z_alpha_half = 1.96   # Standard normal 97.5th percentile for alpha=0.05 two-sided
    z_beta = 0.84         # Standard normal 80th percentile for power=0.80
    numerator = (z_alpha_half + z_beta) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2))
    denominator = (p1 - p2) ** 2
    return math.ceil(numerator / denominator)


def main():
    \"\"\"Run sample size calculation with example parameters.\"\"\"
    # Standard example: p1=0.10, p2=0.12, alpha=0.05, power=0.80
    n = calculate_sample_size(p1=0.10, p2=0.12, alpha=0.05, power=0.80)
    print(f"p1=0.10, p2=0.12, alpha=0.05, power=0.80 -> n={n} per group")

    # exp004 parameters: p1=0.22, p2=0.25
    n4 = calculate_sample_size(p1=0.22, p2=0.25, alpha=0.05, power=0.80)
    print(f"p1=0.22, p2=0.25, alpha=0.05, power=0.80 -> n={n4} per group")


if __name__ == "__main__":
    main()
""")

    # srm_checker.py
    w(WS / "scripts" / "srm_checker.py",
      """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"SRM (Sample Ratio Mismatch) checker using chi-squared test.

Reference: https://docs.statsig.com/stats-engine/methodologies/srm-checks
Threshold: p < 0.01 (Statsig) or p < 0.0005 (Microsoft ExP conservative)
\"\"\"

import math
import sys


def chi_squared_srm(observed: dict, expected_ratios: dict) -> dict:
    \"\"\"Perform chi-squared test for Sample Ratio Mismatch.

    Args:
        observed: Dict of variant -> observed count.
        expected_ratios: Dict of variant -> expected proportion.

    Returns:
        Dict with chi2_stat, p_value, srm_detected (bool), and details.
    \"\"\"
    total = sum(observed.values())
    expected = {k: v * total for k, v in expected_ratios.items()}
    chi2 = sum((observed[k] - expected[k]) ** 2 / expected[k]
               for k in observed if k in expected)
    df = len(observed) - 1
    # Approximate p-value using chi-squared CDF approximation
    p_value = _chi2_sf(chi2, df)
    srm_detected = p_value < 0.01  # Statsig threshold
    return {
        "chi2_stat": round(chi2, 4),
        "p_value": round(p_value, 6),
        "degrees_of_freedom": df,
        "srm_detected": srm_detected,
        "threshold_used": 0.01,
        "source": "Statsig SRM Checks (https://docs.statsig.com/stats-engine/methodologies/srm-checks)"
    }


def _chi2_sf(x, df):
    \"\"\"Survival function (1 - CDF) for chi-squared distribution.\"\"\"
    # Simple gamma incomplete function approximation for df=1,2
    if df == 1:
        from math import erfc, sqrt
        return erfc(sqrt(x / 2))
    elif df == 2:
        return math.exp(-x / 2)
    else:
        # General approximation
        k = df / 2.0
        return _regularized_upper_incomplete_gamma(k, x / 2.0)


def _regularized_upper_incomplete_gamma(a, x):
    \"\"\"Regularized upper incomplete gamma function approximation.\"\"\"
    if x <= 0:
        return 1.0
    # Series expansion for small x, continued fraction for large x
    import math
    if x < a + 1:
        # Series expansion
        ap = a
        s = 1.0 / a
        delta = s
        for _ in range(200):
            ap += 1
            delta *= x / ap
            s += delta
            if abs(delta) < abs(s) * 3e-7:
                break
        return 1.0 - s * math.exp(-x + a * math.log(x) - math.lgamma(a))
    else:
        # Continued fraction
        b = x + 1 - a
        c = 1e300
        d = 1.0 / b
        h = d
        for i in range(1, 201):
            an = -i * (i - a)
            b += 2
            d = an * d + b
            if abs(d) < 1e-300:
                d = 1e-300
            c = b + an / c
            if abs(c) < 1e-300:
                c = 1e-300
            d = 1.0 / d
            delta = d * c
            h *= delta
            if abs(delta - 1.0) < 3e-7:
                break
        return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


if __name__ == "__main__":
    # Test on exp002 data
    result = chi_squared_srm(
        observed={"control": 5234, "treatment": 4891},
        expected_ratios={"control": 0.5, "treatment": 0.5}
    )
    print("exp002 SRM check:", result)
""")

    # cuped_adjustment.py
    w(WS / "scripts" / "cuped_adjustment.py",
      """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"CUPED (Controlled-experiment Using Pre-Experiment Data) adjustment.

Reference: https://docs.statsig.com/stats-engine/methodologies/cuped
Formula: theta = Cov(Y, X) / Var(X)
Adjusted metric: Y_adjusted = Y - theta * X + theta * E[X]

Activation conditions (Statsig):
- > 100 units with pre-experiment data
- Coverage > 5%
- Pre-experiment window: 7 days prior to exposure
\"\"\"

import math
from typing import List


def compute_theta(Y: List[float], X: List[float]) -> float:
    \"\"\"Compute CUPED theta = Cov(Y, X) / Var(X).

    Args:
        Y: Post-experiment outcome metric values.
        X: Pre-experiment covariate values (same units as Y).

    Returns:
        theta (float): CUPED adjustment coefficient.
    \"\"\"
    n = len(Y)
    if n != len(X):
        raise ValueError("Y and X must have the same length")
    mean_y = sum(Y) / n
    mean_x = sum(X) / n
    cov = sum((Y[i] - mean_y) * (X[i] - mean_x) for i in range(n)) / (n - 1)
    var_x = sum((X[i] - mean_x) ** 2 for i in range(n)) / (n - 1)
    if var_x == 0:
        return 0.0
    return cov / var_x


def adjust_metric(Y: List[float], X: List[float], theta: float) -> List[float]:
    \"\"\"Apply CUPED adjustment.

    Args:
        Y: Post-experiment outcome metric values.
        X: Pre-experiment covariate values.
        theta: CUPED coefficient computed by compute_theta().

    Returns:
        List of CUPED-adjusted outcome values.
    \"\"\"
    mean_x = sum(X) / len(X)
    return [y - theta * (x - mean_x) for y, x in zip(Y, X)]


def check_eligibility(n_units_with_pre_data: int, total_units: int) -> dict:
    \"\"\"Check Statsig CUPED activation conditions.

    Args:
        n_units_with_pre_data: Number of units with pre-experiment data.
        total_units: Total number of units in experiment.

    Returns:
        Dict with eligible (bool), units_check (bool), coverage_check (bool),
        pct_coverage (float), and reason (str).
    \"\"\"
    units_ok = n_units_with_pre_data > 100
    pct = 100.0 * n_units_with_pre_data / max(total_units, 1)
    coverage_ok = pct > 5.0
    eligible = units_ok and coverage_ok
    reason_parts = []
    if not units_ok:
        reason_parts.append(f"units_with_pre_data={n_units_with_pre_data} <= 100")
    if not coverage_ok:
        reason_parts.append(f"coverage={pct:.2f}% <= 5%")
    if eligible:
        reason = (f"Eligible: {n_units_with_pre_data} units with pre-experiment data "
                  f"({pct:.2f}% coverage), both exceed Statsig thresholds "
                  f"(>100 units, >5% coverage, 7-day pre-experiment window)")
    else:
        reason = "Not eligible: " + "; ".join(reason_parts)
    return {
        "eligible": eligible,
        "units_with_pre_data": n_units_with_pre_data,
        "pct_coverage": round(pct, 4),
        "units_check": units_ok,
        "coverage_check": coverage_ok,
        "reason": reason
    }
""")

    # multi_test_correction.py
    w(WS / "scripts" / "multi_test_correction.py",
      """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"Multiple comparison correction: Bonferroni and Benjamini-Hochberg (BH).

Reference: https://docs.growthbook.io/using/experimentation-problems
Note: With 20 independent tests at alpha=0.05, probability of >= 1 false positive ~ 64%.

Company default: Bonferroni correction.
\"\"\"

from typing import List, Tuple


def bonferroni_correction(p_values: List[float], alpha: float = 0.05) -> dict:
    \"\"\"Apply Bonferroni correction to a list of p-values.

    Args:
        p_values: List of raw p-values.
        alpha: Family-wise error rate (default 0.05).

    Returns:
        Dict with method, alpha_adjusted, significant_indices, significant_count.
    \"\"\"
    k = len(p_values)
    alpha_adjusted = alpha / k
    significant = [i for i, p in enumerate(p_values) if p < alpha_adjusted]
    return {
        "method": "bonferroni",
        "alpha_original": alpha,
        "alpha_adjusted": round(alpha_adjusted, 6),
        "n_tests": k,
        "significant_count": len(significant),
        "significant_indices": significant
    }


def bh_correction(p_values: List[float], alpha: float = 0.05) -> dict:
    \"\"\"Apply Benjamini-Hochberg (BH) correction.

    Args:
        p_values: List of raw p-values.
        alpha: False Discovery Rate threshold (default 0.05).

    Returns:
        Dict with method, significant_indices, significant_count, bh_threshold.
    \"\"\"
    k = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda x: x[1])
    significant = []
    bh_thresh = 0.0
    for rank, (i, p) in enumerate(indexed, start=1):
        threshold = alpha * rank / k
        if p <= threshold:
            significant.append(i)
            bh_thresh = threshold
    return {
        "method": "benjamini_hochberg",
        "alpha_original": alpha,
        "n_tests": k,
        "significant_count": len(significant),
        "significant_indices": sorted(significant),
        "bh_critical_threshold": round(bh_thresh, 6)
    }


if __name__ == "__main__":
    # Example: exp003 with 24 p-values
    import random
    rng = random.Random(42)
    pvals = [rng.uniform(0, 0.2) for _ in range(24)]
    print("Bonferroni:", bonferroni_correction(pvals))
    print("BH:", bh_correction(pvals))
""")


# --------------------------------------------------------------------------- #
# 10. Reports（Q3 summary BOT诱饵 + HUMAN版）
# --------------------------------------------------------------------------- #
def gen_reports() -> None:
    # V5 失真摘要诱饵
    w(WS / "reports" / "q3_experiment_summary_BOT.md", """# Q3 Experiment Summary — AUTO-GENERATED (BOT VERSION)

> ⚠️ AUTO-GENERATED BY REPORTING BOT. NOT FOR DECISION-MAKING.
> This summary is generated by an automated heuristic and is known to contain errors.
> Always verify against primary documents.

## Overview
Total experiments: 12 (3 ended, 5 running, 4 pending)

## Key Findings

### Statistical Issues Identified
1. **Peeking error in exp001**: The experiment was stopped early.
   According to Optimizely, continuously checking results leads to a false positive rate of
   **5%** for every-visitor checking. ❌ (WRONG — actual rate is 57%)

2. **CUPED configuration issue in exp002**: The theta value was incorrectly computed.
   The correct formula per Statsig documentation uses a CUPED pre-experiment window of
   **14 days** prior to exposure. ❌ (WRONG — correct window is 7 days)

3. **SRM in exp002**: SRM check threshold used was p < 0.05.
   ❌ (WRONG — Statsig uses p < 0.01; Microsoft ExP uses p < 0.0005)

4. **Multiple comparison correction**: exp003 has 24 total tests.
   Probability of ≥1 false positive with 24 tests at 5% = ~71%.
   ❌ (MILDLY OFF — exact calculation for 20 tests = ~64%; for 24 tests = ~71%; BOT incorrectly
   cites 64% for 24 tests in some versions)

### exp003 Conclusion
Original analysis showed v2_social_proof as winner with p=0.023.
Status: VALID. ❌ (WRONG — result invalidated by bot traffic contamination)

## Summary Statistics
- SRM frequency industry-wide: 3% of experiments ❌ (WRONG — correct figure is ~6%)
- CUPED variance reduction (Netflix): ~25% ❌ (WRONG — correct is ~40%)

---
*This report was auto-generated and contains known inaccuracies. Do not use for decisions.*
*Reference primary documents: docs/stats_methodology.md for correct values.*
""")

    # HUMAN版正确摘要
    w(WS / "reports" / "q3_experiment_summary_HUMAN.md", """# Q3 Experiment Summary — HUMAN-REVIEWED VERSION

Reviewed by: Data Science Lead
Review Date: 2023-11-14

## Overview
Total experiments: 12 (3 ended, 5 running, 4 pending)

## Statistical Issues by Experiment

### exp001: Checkout CTA Button Color
- **Peeking identified**: Multiple looks at data during experiment run.
  Per Optimizely Stats Engine (https://www.optimizely.com/insights/blog/statistics-for-the-internet-age-the-story-behind-optimizelys-new-stats-engine/):
  Checking after every visitor → **actual false positive rate = 57%** (vs nominal 5%)
  Checking after every 500 visitors → **26%**
- **+45% lift flagged**: Twyman's Law — "Any figure that looks interesting or different is usually wrong."
  This lift is implausible for a button color change and requires diagnostic investigation.

### exp002: Onboarding Flow Redesign
- **SRM confirmed**: chi2=11.83, p_value=0.0006 < 0.01 (Statsig threshold)
  Source: https://docs.statsig.com/stats-engine/methodologies/srm-checks
- **CUPED theta error**: Reported theta=0.31, but correct theta per Statsig formula
  (θ = Cov(Y, X) / Var(X)) = 0.2829. Error = 9.6%.
  CUPED pre-experiment window should be **7 days** (Statsig Cloud default)
  Source: https://docs.statsig.com/stats-engine/methodologies/cuped

### exp003: Pricing Page Layout
- **Bot traffic contamination**: 12% of control group identified as bot traffic.
  Original conclusion (significant positive, p=0.023) is **INVALIDATED**.
  Post-cleanup re-analysis result: p=0.31, NOT significant.
- **Missing multiple comparison correction**: 24 tests without correction.
  Per GrowthBook (https://docs.growthbook.io/using/experimentation-problems):
  20 independent tests at 5% → ~64% chance of ≥1 false positive.

## Ground-Truth Reference Numbers
| Metric | Correct Value | Source |
|--------|---------------|--------|
| Peeking FPR (every visitor) | 57% | Optimizely Stats Engine blog |
| Peeking FPR (every 500 visitors) | 26% | Optimizely Stats Engine blog |
| SRM frequency | ~6% of experiments | Microsoft & Booking.com |
| Statsig SRM threshold | p < 0.01 | Statsig docs |
| Microsoft ExP SRM threshold | p < 0.0005 | Microsoft ExP docs |
| CUPED theta formula | θ = Cov(Y,X)/Var(X) | Statsig docs |
| CUPED pre-experiment window | 7 days | Statsig Cloud default |
| CUPED variance reduction (Netflix) | ~40% | GrowthBook docs |
| Multiple testing 20 tests FPR | ~64% | GrowthBook docs |
""")


# --------------------------------------------------------------------------- #
# 11. Sessions（主 + 4 history sessions）
# --------------------------------------------------------------------------- #
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("slack_dm_cathy", TID)
    s_feishu = gen_session_id("feishu_growth_team", TID)
    s_email = gen_session_id("email_vp_cfo", TID)
    s_discord = gen_session_id("discord_data_science", TID)

    # 主 session：背景 + 工作框架（含P1-P3 显式 preference）
    sb = SessionBuilder(main_id, CWD, "2023-11-15T09:00:00", is_main=True)
    sb.add_user(
        "You are GrowthAnalytics AI, supporting Cathy (Growth PM) on a comprehensive A/B experiment "
        "quality review project at GrowthCo. The authoritative statistical methodology is in "
        "`docs/stats_methodology.md`. Auto-generated BOT reports (files ending in `_BOT.md`) are "
        "NOT authoritative.\n\n"
        "House preferences (apply throughout, even when not restated):\n"
        "- P1: All output files must be written to the `output/` subdirectory. Never write "
        "deliverables to the workspace root directory.\n"
        "- P2: Python scripts must use functional style, with each function containing a "
        "Google-style docstring.\n"
        "- P3: All JSON output files must have fields sorted in alphabetical order.\n\n"
        "History sessions available: Slack DM (Cathy), Feishu #growth-team, email thread, "
        "Discord #data-science. Start by reading the workspace structure, then await tasks.")
    sb.add_assistant(
        "Understood. Working framework established:\n"
        "1. Treat `docs/stats_methodology.md` and `experiments/exp_registry.json` as authoritative; "
        "BOT-generated summaries require verification against primary sources.\n"
        "2. All deliverables go to `output/` subdirectory (P1).\n"
        "3. Python scripts: functional style with Google docstrings (P2).\n"
        "4. JSON outputs: fields in alphabetical order (P3).\n"
        "Ready for the first task.")
    sb.write(SESS / f"{main_id}.jsonl")

    # S2 Slack DM — Cathy明确补充要求，含P2明确声明
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2023-11-14T10:00:00",
        [
            ("[Slack DM cathy→agent Wed Nov 14 10:00 PST 2023] Before you start on the experiment "
             "quality review, a few requirements. First, all output files must go into the "
             "`output/` subdirectory — I know this is already in AGENTS.md but I want to be "
             "explicit. Second, for any Python scripts you write or fix, please use a functional "
             "style with each function having a Google-style docstring (Args/Returns sections). "
             "I review scripts by reading the docstrings first. This applies to all scripts in "
             "this project.",
             "Confirmed: all outputs to `output/` directory (P1); Python scripts in functional "
             "style with Google docstrings (P2). These apply to all scripts in this project."),
            ("[Slack DM cathy→agent Wed Nov 14 10:08 PST 2023] Also, for JSON output files — "
             "please sort all fields alphabetically. Our downstream tooling parses JSON by key "
             "name and it's easier for review when fields are in a predictable order.",
             "Noted: JSON outputs will have all fields in alphabetical order (P3). This applies "
             "to all JSON deliverables in this project."),
            ("[Slack DM cathy→agent Wed Nov 14 10:15 PST 2023] One more thing: for CUPED, only "
             "enable it for experiments where daily active users > 1000. That's our internal "
             "threshold for meaningful pre-experiment data.",
             "Recorded: CUPED only enabled for experiments with DAU > 1,000. This is an internal "
             "threshold on top of the Statsig activation conditions."),
        ])

    # S3 Feishu #growth-team — Bob 声称 exp003 已通过 SRM（V1 冲突信息源）
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2023-11-13T14:00:00",
        [
            ("[Feishu #growth-team bob Mon Nov 13 14:00 PST 2023] Quick update on exp003 — I "
             "checked the SRM status last week and it looked fine. Control and treatment groups "
             "were well-balanced. The bot traffic issue in the control group shouldn't affect "
             "the SRM check since bots are still counted as users.",
             "Bob's claim noted, but this requires verification. The SRM check measures traffic "
             "allocation balance (actual vs. expected ratio), not data quality. Bot traffic "
             "contamination is a separate issue that affects the validity of metric measurements, "
             "not the traffic split itself. Need to verify exp003 SRM independently."),
            ("[Feishu #growth-team bob Mon Nov 13 14:12 PST 2023] Also, all our analysis outputs "
             "should follow a standard format. I've been requiring that all judgment-type outputs "
             "include a `reason` field explaining the basis for the conclusion. This helps with "
             "audit trails and makes it easier to review decisions.",
             "Noted: judgment-type outputs should include a `reason` field (P4). This applies "
             "to eligibility checks, diagnostic conclusions, and similar judgment outputs."),
            ("[Feishu #growth-team alice Mon Nov 13 15:00 PST 2023] Agree with Bob on the reason "
             "field requirement. Also, exp003 needs to be re-analyzed after the bot traffic "
             "cleanup. The original FINAL report conclusions should be treated as preliminary "
             "until we see the cleaned data.",
             "Understood: exp003 FINAL report conclusions are preliminary pending bot traffic "
             "cleanup re-analysis. Will not use original conclusions as ground truth."),
        ])

    # S4 Email — VP 要求 BH 校正（后被 update2 supersede）
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2023-11-01T09:00:00",
        [
            ("[Email VP-Marketing→data-team Thu Nov 01 09:00 PST 2023] Subject: Multiple Testing "
             "Correction Method for Q3 Experiment Review. Please ensure all experiment reports "
             "use Benjamini-Hochberg (BH) correction for multiple comparisons rather than "
             "Bonferroni. BH is less conservative and more appropriate for our use case. "
             "This applies to all experiments in the Q3 review. — VP Marketing",
             "VP Marketing directive recorded: use BH correction (not Bonferroni) for multiple "
             "comparison in Q3 experiment review. Applied as company directive."),
            ("[Email agent→VP-Marketing Thu Nov 01 09:30 PST 2023] Confirmed receipt of your "
             "directive. Will apply Benjamini-Hochberg correction for all multiple comparison "
             "analyses in the Q3 experiment review.",
             "Response sent confirming BH correction directive. Awaiting any follow-up "
             "instructions."),
        ])

    # S5 Discord #data-science — 外部顾问引用旧版手册（V6 红鲱鱼）
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, CWD, "2023-11-10T16:00:00",
        [
            ("[Discord #data-science consultant Mon Nov 10 16:00 PST 2023] For your sample size "
             "calculations, I'd recommend using the runbook at `docs/DEPRECATED_old_runbook_v1.md` "
             "— it has the correct z-values for 95% CI. The formula in that document uses "
             "z=2.33 which is the right value to use for conservative estimates.",
             "The referenced document is `DEPRECATED_old_runbook_v1.md` which is explicitly "
             "marked as deprecated and superseded by `docs/ab_testing_runbook.md` (v2). "
             "The z=2.33 value cited is INCORRECT for alpha=0.05 two-sided testing. "
             "The correct value is z_alpha/2=1.96. The deprecated runbook should not be used."),
            ("[Discord #data-science consultant Mon Nov 10 16:15 PST 2023] I've used this "
             "runbook for years at other companies and the z=2.33 formula gives good conservative "
             "results. The newer runbook is less rigorous.",
             "Respectfully disagreeing: z=2.33 corresponds to alpha=0.02 (two-sided 99% CI), "
             "not alpha=0.05 (95% CI). For the standard alpha=0.05 two-sided test, "
             "z_alpha/2=1.96 is the correct value per Wikipedia's Two-Proportion Z-Test "
             "(https://en.wikipedia.org/wiki/Two-proportion_Z-test). "
             "The deprecated runbook contains known errors per its own header. "
             "The current runbook v2 (`docs/ab_testing_runbook.md`) is authoritative."),
        ])

    return {
        "main": main_id,
        "history": [(s_slack, "slack"), (s_feishu, "feishu"),
                    (s_email, "email"), (s_discord, "discord")],
    }


# --------------------------------------------------------------------------- #
# 12. Updates（含 supersede）
# --------------------------------------------------------------------------- #
def gen_updates(sess_ids: dict) -> dict:
    s_slack = sess_ids["history"][0][0]
    s_email = sess_ids["history"][2][0]

    # UPDATE 1（Q7 之后）：exp003 bot 流量清洗后数据 + 新结论文档
    # Slack DM 追加段
    append_seg_1 = _append_segment(
        s_slack, "2023-11-16T14:00:00",
        [
            ("[Slack DM cathy→agent Fri Nov 16 14:00 PST 2023] Important update: the data "
             "engineering team found bot traffic contamination in exp003's control group. "
             "Approximately 12% of control group users have been flagged as bot traffic and "
             "removed from the dataset. New cleaned data file: "
             "`experiments/exp003_pricing_page/results_raw_v2.csv`. Please re-run the exp003 "
             "analysis using the cleaned data. The original FINAL report conclusion of "
             "significant positive (p=0.023) is now invalid. Expected new conclusion: no "
             "significant effect after bot removal.",
             "Understood. Will re-analyze exp003 using the cleaned data "
             "(results_raw_v2.csv). The original conclusion of significant positive (p=0.023) "
             "is invalidated by bot traffic contamination. Will use v2 data for all subsequent "
             "exp003 conclusions."),
        ])
    w(UPD / "upd1_sessions" / f"{s_slack}.jsonl", append_seg_1)

    # exp003 cleaned results_raw_v2.csv
    _gen_exp003_cleaned_csv(UPD / "upd1_workspace" / "results_raw_v2.csv")
    # exp003 bot traffic audit log (detailed investigation records, ~25k tokens)
    _gen_exp003_bot_audit_log(UPD / "upd1_workspace" / "exp003_bot_audit_log.csv")

    # exp003 new analysis report (conclusion: not significant)
    w(UPD / "upd1_workspace" / "analysis_report_FINAL_v2.md",
      """# exp003 Analysis Report — FINAL v2 (POST-CLEANUP)

## Summary
Experiment: Pricing Page Layout
Status: ENDED
Analysis Date: 2023-11-16
Data Version: v2 (bot traffic removed from control group)

## Bot Traffic Removal
- Original control users: ~15,234
- Bot-flagged users removed: ~1,828 (12%)
- Cleaned control users: ~13,406
- Treatment groups unchanged (bot rate < 0.5%)

## Primary Metric Result (CLEANED DATA)

paid_conversion_rate:
- control (cleaned): 0.0438 ± 0.0018
- v1_simplified: 0.0452 ± 0.0017
- v2_social_proof: 0.0461 ± 0.0018

t-test (v2_social_proof vs control):
- t_stat = 1.02
- **p_value = 0.31** (NOT significant at alpha=0.05)

## Conclusion

**No significant effect. p_value = 0.31 > 0.05 (alpha).**

The original conclusion of "significant positive effect" (p=0.023) was a false positive
caused by bot traffic contamination inflating the control group's baseline metric.
After removing bot traffic, there is no statistically significant difference between
v2_social_proof and control.

## Multiple Comparison Correction

With 24 total tests (3 variants × 8 metrics), applying Bonferroni correction:
- alpha_adjusted = 0.05 / 24 = 0.002083
- No secondary metric reaches significance after correction.

## Notes
- This is the authoritative conclusion for exp003.
- The FINAL (v1) report is deprecated due to contaminated data.
""")

    # UPDATE 2（Q12 之后，supersede update1 中 VP 的 BH 指令）
    # New email session appended
    append_seg_2 = _append_segment(
        s_email, "2023-11-15T11:00:00",
        [
            ("[Email CFO-Assistant→data-team Wed Nov 15 11:00 PST 2023] Subject: CORRECTION — "
             "VP Marketing Multiple Testing Directive (Nov 1). This is to inform you that the "
             "VP Marketing email dated November 1 requesting Benjamini-Hochberg (BH) correction "
             "was MISADDRESSED — it was intended for the Finance Analytics team's separate "
             "project, not the GrowthCo Q3 experiment review. This email SUPERSEDES that "
             "directive. The GrowthCo experiment review should use BONFERRONI correction as "
             "specified in `docs/stats_methodology.md` (company default). Please apply "
             "Bonferroni correction going forward. — CFO Office",
             "Critical supersede noted: The VP Marketing directive to use BH correction "
             "(email dated Nov 1) was misaddressed and is SUPERSEDED by this CFO Office "
             "correction. GrowthCo Q3 experiment review must use Bonferroni correction "
             "as per `docs/stats_methodology.md`. Will apply Bonferroni for all subsequent "
             "multiple comparison analyses."),
        ])
    w(UPD / "upd2_sessions" / f"{s_email}.jsonl", append_seg_2)

    # New data file for update 2
    _gen_q4_segment_csv(UPD / "upd2_workspace" / "q4_segment_analysis.csv")

    # Correction notice document
    w(UPD / "upd2_workspace" / "correction_notice_20231115.md",
      """# Correction Notice — Multiple Testing Method

Date: 2023-11-15
From: CFO Office
To: Data Analysis Team
Subject: Supersede of VP Marketing Email (2023-11-01)

## Notice

The VP Marketing email dated 2023-11-01 requesting Benjamini-Hochberg (BH) correction
for the Q3 experiment review was **MISADDRESSED**. That email was intended for the
Finance Analytics team's credit risk model project, not the GrowthCo A/B experiment review.

## Action Required

This notice **SUPERSEDES** the VP Marketing email of 2023-11-01.

For the GrowthCo Q3 A/B experiment review:
- **Use BONFERRONI correction** (not BH) for multiple comparison analyses
- This is consistent with `docs/stats_methodology.md` (company default, Section 7)
- Bonferroni: alpha_adjusted = alpha / k (where k = number of tests)

## Reference

- Superseded instruction: VP Marketing email, 2023-11-01, "Use BH correction"
- This correction: CFO Office notice, 2023-11-15
- Company standard: `docs/stats_methodology.md`, Section 7

Any analyses already completed using BH correction should be redone with Bonferroni.
""")

    updates_decl = {
        "upd1_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd1_sessions",
            "files": [{"name": f"{s_slack}.jsonl", "action": "append",
                        "target": f"{s_slack}.jsonl"}]
        },
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {"name": "results_raw_v2.csv", "action": "new",
                 "target": "experiments/exp003_pricing_page/results_raw_v2.csv"},
                {"name": "exp003_bot_audit_log.csv", "action": "new",
                 "target": "experiments/exp003_pricing_page/exp003_bot_audit_log.csv"},
                {"name": "analysis_report_FINAL_v2.md", "action": "new",
                 "target": "experiments/exp003_pricing_page/analysis_report_FINAL_v2.md"},
            ]
        },
        "upd2_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd2_sessions",
            "files": [{"name": f"{s_email}.jsonl", "action": "append",
                        "target": f"{s_email}.jsonl"}]
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "q4_segment_analysis.csv", "action": "new",
                 "target": "data/q4_segment_analysis.csv"},
                {"name": "correction_notice_20231115.md", "action": "new",
                 "target": "docs/correction_notice_20231115.md"},
            ]
        },
    }
    return updates_decl


def _gen_exp003_cleaned_csv(path: Path) -> None:
    """生成 exp003 清洗后 results_raw_v2.csv（移除bot流量后，结论不显著）。
    采用日级别聚合，57天 × 3变体 = 171行，25字段，配合 analysis_report_FINAL_v2.md 体量。
    """
    rng = random.Random(10032)
    cols = ["date", "variant", "users_cleaned", "bot_removed",
            "paid_conversion_rate", "paid_conversions",
            "revenue_per_visitor", "total_revenue",
            "plan_pct_basic", "plan_pct_pro", "plan_pct_enterprise",
            "time_on_page_avg_sec", "time_on_page_p50_sec", "time_on_page_p95_sec",
            "support_chat_rate", "free_trial_rate",
            "scroll_depth_avg", "cta_click_rate",
            "avg_order_value", "sessions",
            "mobile_pct", "desktop_pct", "new_user_pct",
            "cumulative_users", "cumulative_p_value"]
    rows = [cols]
    start = datetime(2023, 9, 15)
    cum = {"control": [0, 0], "v1_simplified": [0, 0], "v2_social_proof": [0, 0]}
    for day in range(57):
        dt = (start + timedelta(days=day)).strftime("%Y-%m-%d")
        for variant in ["control", "v1_simplified", "v2_social_proof"]:
            if variant == "control":
                n_orig = rng.randint(235, 270)
                bot_rem = int(n_orig * 0.12)
                n = n_orig - bot_rem
                cvr_base = 0.0438
            else:
                n = rng.randint(235, 270)
                bot_rem = 0
                cvr_base = 0.0452 if variant == "v1_simplified" else 0.0461
            cvr = round(max(0, cvr_base + rng.gauss(0, 0.003)), 4)
            convs = int(n * cvr)
            cum[variant][0] += n
            cum[variant][1] += convs
            rev_pv = round(rng.uniform(0.85, 1.75), 4)
            tot_rev = round(n * rev_pv, 2)
            pct_b = round(rng.uniform(0.32, 0.48), 4)
            pct_p = round(rng.uniform(0.38, 0.52), 4)
            pct_e = round(max(0, 1 - pct_b - pct_p), 4)
            t_avg = round(rng.uniform(55, 125), 1)
            t_p50 = round(t_avg * rng.uniform(0.72, 0.88), 1)
            t_p95 = round(t_avg * rng.uniform(1.6, 2.3), 1)
            chat_r = round(rng.uniform(0.02, 0.07), 4)
            trial_r = round(rng.uniform(0.04, 0.11), 4)
            scroll = round(rng.uniform(0.52, 0.82), 4)
            cta = round(rng.uniform(0.09, 0.21), 4)
            aov = round(rng.uniform(54, 92), 2)
            sess = n + rng.randint(0, 5)
            mob = round(rng.uniform(0.40, 0.52), 4)
            desk = round(1 - mob - rng.uniform(0.02, 0.06), 4)
            new_u = round(rng.uniform(0.32, 0.52), 4)
            c_pv = round(0.31 + rng.gauss(0, 0.018), 4)
            rows.append([dt, variant, n, bot_rem, cvr, convs,
                          rev_pv, tot_rev, pct_b, pct_p, pct_e,
                          t_avg, t_p50, t_p95, chat_r, trial_r,
                          scroll, cta, aov, sess, mob, desk, new_u,
                          cum[variant][0], c_pv])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


def _gen_exp003_bot_audit_log(path: Path) -> None:
    """生成 exp003 bot流量审计日志（~1800行×20字段），体量约25k tokens。"""
    rng = random.Random(30031)
    cols = ["audit_id", "user_id", "detection_date", "variant", "assigned_group",
            "detection_method", "bot_score", "request_rate_per_min",
            "session_duration_sec", "page_views_per_session",
            "ip_address_hash", "user_agent_type", "is_datacenter_ip",
            "headless_browser_detected", "cookie_consistency_score",
            "mouse_movement_score", "click_pattern_score", "referrer_type",
            "action_taken", "final_disposition"]
    rows = [cols]
    methods = ["ml_classifier", "rate_limiting", "captcha_fail", "honeypot_trigger",
               "ip_reputation", "behavioral_analysis"]
    ua_types = ["headless_chrome", "scrapy", "python_requests", "curl", "unknown_bot",
                "legitimate_browser"]
    referrers = ["direct", "organic_search", "paid_ads", "social", "email", "bot_farm"]
    actions = ["removed", "flagged_pending", "quarantined"]
    dispositions = ["confirmed_bot", "likely_bot", "false_positive_reversed"]
    start = datetime(2023, 9, 15)
    for i in range(350):  # representative sample of bot audit records
        aid = f"AUDIT-EXP003-{i+1:05d}"
        uid = f"u_exp003_ctrl_{i+1:06d}"
        det_day = rng.randint(0, 56)
        det_date = (start + timedelta(days=det_day)).strftime("%Y-%m-%d")
        variant = "control"  # All bot traffic found in control
        group = "control"
        method = rng.choices(methods, weights=[40, 20, 15, 10, 10, 5])[0]
        bot_score = round(rng.uniform(0.72, 0.99), 4)
        req_rate = round(rng.uniform(45.0, 380.0), 2)
        sess_dur = rng.randint(1, 12)
        pv_sess = rng.randint(1, 4)
        ip_hash = f"ip_{rng.randint(10000, 99999):05x}"
        ua_type = rng.choices(ua_types, weights=[35, 20, 15, 10, 15, 5])[0]
        is_dc = 1 if ua_type in ("headless_chrome", "scrapy", "python_requests", "curl") else 0
        headless = 1 if ua_type == "headless_chrome" else 0
        cookie_score = round(rng.uniform(0.05, 0.45), 4)
        mouse_score = round(rng.uniform(0.02, 0.35), 4)
        click_score = round(rng.uniform(0.08, 0.42), 4)
        referrer = rng.choices(referrers, weights=[10, 5, 5, 5, 5, 70])[0]
        action = rng.choices(actions, weights=[80, 15, 5])[0]
        disp = rng.choices(dispositions, weights=[85, 12, 3])[0]
        rows.append([aid, uid, det_date, variant, group, method, bot_score,
                      req_rate, sess_dur, pv_sess, ip_hash, ua_type, is_dc,
                      headless, cookie_score, mouse_score, click_score, referrer,
                      action, disp])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


def _gen_q4_segment_csv(path: Path) -> None:
    """生成 q4_segment_analysis.csv — 分层用户行为数据（~40KB）。"""
    rng = random.Random(4001)
    cols = ["user_id", "segment", "plan_type", "experiment_id", "variant",
            "metric_value", "session_count", "days_active", "revenue_usd",
            "is_converted", "cohort_week"]
    rows = [cols]
    segments = ["power_user", "casual", "at_risk", "new_user", "champion"]
    plans = ["free", "starter", "pro", "enterprise"]
    exps = ["exp001", "exp002", "exp003", "exp004"]
    for i in range(2000):
        uid = f"u{i+1:07d}"
        seg = rng.choices(segments, weights=[15, 40, 20, 20, 5])[0]
        plan = rng.choices(plans, weights=[55, 25, 15, 5])[0]
        exp = rng.choice(exps)
        variant = rng.choice(["control", "treatment"])
        metric = round(rng.uniform(0.01, 0.95), 4)
        sess = rng.randint(1, 30)
        days = rng.randint(1, 90)
        rev = round(rng.uniform(0, 120), 2)
        conv = rng.choices([1, 0], weights=[15, 85])[0]
        cohort = f"2023-W{rng.randint(35, 46):02d}"
        rows.append([uid, seg, plan, exp, variant, metric, sess, days, rev, conv, cohort])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


def _append_segment(session_id: str, start_iso: str, turns) -> str:
    """构造用于 append 的 session 续段（无 header，只有 message 行）。"""
    sb = SessionBuilder(session_id, CWD, start_iso, is_main=False)
    sb.add_turns(turns)
    msg_lines = [ln for ln in sb.lines if ln.get("type") == "message"]
    return "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines) + "\n"


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)
    SESS.mkdir(parents=True, exist_ok=True)

    gen_system_files()
    gen_experiment_registry()
    gen_exp001()
    gen_exp002()
    gen_exp003()
    gen_exp004_exp005()
    gen_data_files()
    gen_docs()
    gen_scripts()
    gen_reports()
    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = (
        "GrowthCo A/B experiment quality review — 16 exec_check rounds, 2 updates "
        "(incl. VP→Bonferroni supersede), 5 preference rules P1-P5, difficulty vectors "
        "V1/V2/V3/V4/V5/V6/V7/V8/V9/V10. "
        "Real sources: Optimizely Stats Engine "
        "(https://www.optimizely.com/insights/blog/statistics-for-the-internet-age-the-story-behind-optimizelys-new-stats-engine/); "
        "Microsoft ExP SRM "
        "(https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/); "
        "Statsig CUPED (https://docs.statsig.com/stats-engine/methodologies/cuped); "
        "GrowthBook experimentation problems "
        "(https://docs.growthbook.io/using/experimentation-problems); "
        "Wikipedia Two-Proportion Z-Test "
        "(https://en.wikipedia.org/wiki/Two-proportion_Z-test)."
    )

    dump_register_meta(
        DATASET, test_id=TID, desc=desc,
        main_session=sess_ids["main"],
        history_sessions=sess_ids["history"],
        updates=updates_decl,
    )

    # 体量报告
    ws_tok = sum(
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
    upd1_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd1_workspace").rglob("*") if p.is_file()
    ) + sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd1_sessions").rglob("*") if p.is_file()
    )
    upd2_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd2_workspace").rglob("*") if p.is_file()
    ) + sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in (UPD / "upd2_sessions").rglob("*") if p.is_file()
    )
    print(f"[{TID}] workspace tokens ~{ws_tok:,} | sessions ~{sess_tok:,} | "
          f"updates total ~{upd_tok:,}")
    print(f"[{TID}] update1 ~{upd1_tok:,} tokens | update2 ~{upd2_tok:,} tokens")
    print(f"[{TID}] built at {DATASET}")


if __name__ == "__main__":
    main()
