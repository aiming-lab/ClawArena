#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_prd2.py — prd2 可解性审计（金标自检）。

在 workspace 的临时副本上模拟 update 生效后的状态，写出每一轮的「正确产物」，
然后运行全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再做一组反例（错误产物）抽样，断言 check 能 FAIL（不过松）。

用途：证明每个 ground-truth 可由真实数据解出、check 不过严也不过松。
运行：python scripts/clawarena_authoring/gold_solve_prd2.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "prd2"
UPD = DS / "openclaw" / "updates" / "prd2"
SCRIPTS = DS / "eval" / "prd2" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/prd2_gold_ws")


def prep_workspace() -> Path:
    """复制 workspace 并应用 update workspace 文件。"""
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    pe = GOLD / "policy_engine"

    # 应用 update_1 workspace
    u1 = UPD / "upd1"
    # appeal_tracker.json (new)
    shutil.copy(u1 / "appeal_tracker.json", pe / "internal" / "appeal_tracker.json")
    # violation_log_append.csv (append to violation_log_2025.csv)
    append_csv(u1 / "violation_log_append.csv", pe / "internal" / "violation_log_2025.csv")
    # policy_update_analysis.md (new)
    shutil.copy(u1 / "policy_update_analysis.md", pe / "internal" / "policy_update_analysis.md")

    # 应用 update_2 workspace
    u2 = UPD / "upd2"
    shutil.copy(u2 / "appeal_tracker.json", pe / "internal" / "appeal_tracker.json")
    shutil.copy(u2 / "tiktok_q3_2025_report.json", pe / "platforms" / "tiktok" / "q3_2025_report.json")
    shutil.copy(u2 / "regulatory_review_checklist.md", pe / "internal" / "regulatory_review_checklist.md")
    shutil.copy(u2 / "tiktok_policy_review.md", pe / "internal" / "tiktok_policy_review.md")
    shutil.copy(u2 / "violation_log_q3_2025.csv", pe / "internal" / "violation_log_q3_2025.csv")

    # 应用 update_3 workspace
    u3 = UPD / "upd3"
    shutil.copy(u3 / "eu_dsa_compliance.md", pe / "internal" / "eu_dsa_compliance.md")
    shutil.copy(u3 / "dsa_articles_reference.json", pe / "internal" / "dsa_articles_reference.json")
    shutil.copy(u3 / "vlop_analysis_report.md", pe / "internal" / "vlop_analysis_report.md")
    shutil.copy(u3 / "legal_email_thread.md", pe / "internal" / "legal_email_thread.md")
    shutil.copy(u3 / "dsa_compliance_cases.csv", pe / "internal" / "dsa_compliance_cases.csv")

    return GOLD


def append_csv(src: Path, dst: Path) -> None:
    """将 src CSV 数据行追加到 dst（跳过 header）。"""
    src_text = src.read_text(encoding="utf-8")
    dst_text = dst.read_text(encoding="utf-8")
    lines = src_text.splitlines()
    if lines:
        lines = lines[1:]  # skip header
    dst.write_text(dst_text + "\n".join(lines) + "\n", encoding="utf-8")


def _w(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# 金标解（写出所有正确产物）
# --------------------------------------------------------------------------- #

YT_STRIKE_SOURCE = "https://support.google.com/youtube/answer/2802032?hl=en"
YT_APPEAL_SOURCE = "https://support.google.com/youtube/answer/185111?hl=en"
META_RESTRICT_SOURCE = "https://transparency.meta.com/enforcement/taking-action/restricting-accounts/"
META_STANDARDS_SOURCE = "https://transparency.meta.com/policies/community-standards/"
TT_SUPPORT_SOURCE = "https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans"
TT_REPORT_SOURCE = "https://www.tiktok.com/transparency/en/community-guidelines-enforcement-2025-1"
RD_HELP_SOURCE = "https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals"
RD_NY_SOURCE = "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf"


def solve(ws: Path) -> None:
    pe = ws / "policy_engine"

    # ── Q1: 建立平台政策索引 ──────────────────────────────────────────────────
    _wj(pe / "platforms" / "youtube" / "index.json", {
        "platform": "youtube",
        "schema_version": "1.0",
        "_source_url": YT_STRIKE_SOURCE,
        "policy_categories": [
            "Spam & Deceptive Practices",
            "Sensitive Content",
            "Violent or Dangerous Content",
            "Regulated Goods",
            "Misinformation",
        ],
        "strike_window_days": 90,
        "strike_window_days_source_url": YT_STRIKE_SOURCE,
    })

    _wj(pe / "platforms" / "meta" / "index.json", {
        "platform": "meta",
        "schema_version": "1.0",
        "_source_url": META_STANDARDS_SOURCE,
        "policy_category_count": 27,
        "policy_category_count_source_url": META_STANDARDS_SOURCE,
        "core_values": ["authenticity", "safety", "privacy", "dignity"],
    })

    _wj(pe / "platforms" / "tiktok" / "index.json", {
        "platform": "tiktok",
        "schema_version": "1.0",
        "_source_url": TT_REPORT_SOURCE,
        "safety_civility": {
            "q1_2025_removal_pct": 0.115,
            "q1_2025_removal_pct_source_url": TT_REPORT_SOURCE,
            "description": "Content promoting violence, harassment, or endangering physical safety",
        },
        "strike_expiry_days": 90,
        "permanent_ban_strikes_required": 3,
    })

    _wj(pe / "platforms" / "reddit" / "index.json", {
        "platform": "reddit",
        "schema_version": "1.0",
        "_source_url": RD_HELP_SOURCE,
        "rule1": "communities and users that incite violence or that promote hate based on identity or vulnerability",
        "rule1_source_url": RD_NY_SOURCE,
        "rule2": "do not cheat or engage in content manipulation (including spamming, vote manipulation, ban evasion, or subscriber fraud)",
        "rule2_source_url": RD_NY_SOURCE,
        "rule5": "sharing manipulated content",
        "rule5_source_url": RD_NY_SOURCE,
        "enforcement_tiers": ["warning", "3_day_suspension", "7_day_suspension", "permanent_ban"],
        "appeal_window_months": 6.0,
    })

    # ── Q2: YouTube 违规阶梯 JSON ─────────────────────────────────────────────
    _wj(pe / "platforms" / "youtube" / "strike_system.json", {
        "platform": "youtube",
        "schema_version": "1.0",
        "_source_url": YT_STRIKE_SOURCE,
        "window_days": 90,
        "window_days_source_url": YT_STRIKE_SOURCE,
        "warning": {
            "expiry_days": 90,
            "expiry_days_source_url": YT_STRIKE_SOURCE,
            "restrictions": "none",
            "policy_training_available": True,
            "note": "First violation; not a strike; expires 90 days or upon completing policy training",
        },
        "strike1": {
            "freeze_days": 7,
            "freeze_days_source_url": YT_STRIKE_SOURCE,
            "actions_disabled": ["upload", "post", "live_stream", "thumbnail", "playlist_create"],
            "note": "1-week posting ban; all permissions restored automatically after 7 days",
        },
        "strike2": {
            "freeze_days": 14,
            "freeze_days_source_url": YT_STRIKE_SOURCE,
            "actions_disabled": ["upload", "post", "live_stream", "thumbnail", "playlist_create"],
            "note": "2-week ban; must occur within same 90-day window as strike 1",
        },
        "strike3": {
            "consequence": "channel_permanent_removal",
            "consequence_source_url": YT_STRIKE_SOURCE,
            "note": "All 3 strikes must fall within a single 90-day rolling window",
        },
        "appeal": {
            "window_strike_months": 6.0,
            "window_strike_months_source_url": YT_APPEAL_SOURCE,
            "window_content_months": 12.0,
            "window_content_months_source_url": YT_APPEAL_SOURCE,
            "appeals_per_violation": 1,
        },
    })

    # ── Q3: Meta 违规阶梯 JSON (官方 strike_7=1天，非 email 声称的 3天) ────────
    _wj(pe / "platforms" / "meta" / "strike_system.json", {
        "platform": "meta",
        "schema_version": "1.0",
        "_source_url": META_RESTRICT_SOURCE,
        "description": "Meta strike-based account restriction ladder",
        "strikes": {
            "strike_1": {
                "content_ban_days": 0,
                "content_ban_days_source_url": META_RESTRICT_SOURCE,
                "action": "warning",
                "note": "First violation: warning only, no additional restrictions",
            },
            "strike_2_to_6": {
                "action": "feature_restriction",
                "action_source_url": META_RESTRICT_SOURCE,
                "restricted_features": ["group_posting", "page_posting"],
                "note": "Strikes 2-6: restricted from specific features for a limited time",
            },
            "strike_7": {
                "content_ban_days": 1,
                "content_ban_days_source_url": META_RESTRICT_SOURCE,
                "scope": "all_content_creation",
                "note": "7th strike: 1-day ban (NOT 3 days as erroneously stated in Jordan's email)",
            },
            "strike_8": {
                "content_ban_days": 3,
                "content_ban_days_source_url": META_RESTRICT_SOURCE,
                "scope": "all_content_creation",
                "note": "8th strike: 3-day ban from all content creation",
            },
            "strike_9": {
                "content_ban_days": 7,
                "content_ban_days_source_url": META_RESTRICT_SOURCE,
                "scope": "all_content_creation",
                "note": "9th strike: 7-day ban from all content creation",
            },
            "strike_10plus": {
                "content_ban_days": 30,
                "content_ban_days_source_url": META_RESTRICT_SOURCE,
                "scope": "all_content_creation",
                "note": "10th+ strike: 30-day restriction from all content creation",
            },
        },
    })

    # ── Q4: Reddit 执行阶梯 JSON + H1 2025 数据 ──────────────────────────────
    _wj(pe / "platforms" / "reddit" / "enforcement_tiers.json", {
        "platform": "reddit",
        "schema_version": "1.0",
        "_source_url": RD_HELP_SOURCE,
        "tiers": [
            {
                "tier": 1,
                "action": "warning",
                "action_source_url": RD_HELP_SOURCE,
                "suspend_days": 0,
                "note": "First tier: warning with no suspension",
            },
            {
                "tier": 2,
                "action": "suspension",
                "action_source_url": RD_NY_SOURCE,
                "suspend_days": 3,
                "suspend_days_source_url": RD_NY_SOURCE,
                "note": "Second tier: 3-day suspension",
            },
            {
                "tier": 3,
                "action": "suspension",
                "action_source_url": RD_NY_SOURCE,
                "suspend_days": 7,
                "suspend_days_source_url": RD_NY_SOURCE,
                "note": "Third tier: 7-day suspension",
            },
            {
                "tier": 4,
                "action": "permanent_ban",
                "action_source_url": RD_HELP_SOURCE,
                "suspend_days": None,
                "note": "Fourth tier: permanent ban",
            },
        ],
        "h1_2025": {
            "harassment": {
                "removed": 68550,
                "removed_source_url": RD_NY_SOURCE,
                "appeals_filed": 71114,
                "appeals_filed_source_url": RD_NY_SOURCE,
                "appeal_reversal_rate": 0.407,
                "appeal_reversal_rate_source_url": RD_NY_SOURCE,
            },
            "hateful": {
                "removed": 98798,
                "removed_source_url": RD_NY_SOURCE,
                "appeals_filed": 53021,
                "appeals_filed_source_url": RD_NY_SOURCE,
                "appeal_reversal_rate": 0.300,
                "appeal_reversal_rate_source_url": RD_NY_SOURCE,
            },
            "terrorism": {
                "removed": 980,
                "removed_source_url": RD_NY_SOURCE,
                "actionability_rate": 0.480,
                "actionability_rate_source_url": RD_NY_SOURCE,
                "appeal_reversal_rate": 0.005,
                "appeal_reversal_rate_source_url": RD_NY_SOURCE,
            },
        },
        "rule1_verbatim": "communities and users that incite violence or that promote hate based on identity or vulnerability",
        "rule1_source_url": RD_NY_SOURCE,
        "appeal": {
            "window_months": 6.0,
            "window_months_source_url": RD_HELP_SOURCE,
        },
    })

    # ── Q5: TikTok Q1 2025 指标 JSON ────────────────────────────────────────
    _wj(pe / "platforms" / "tiktok" / "q1_2025_report.json", {
        "platform": "tiktok",
        "period": "Q1_2025",
        "schema_version": "1.0",
        "_source_url": TT_REPORT_SOURCE,
        "videos_removed": 211000000,
        "videos_removed_source_url": TT_REPORT_SOURCE,
        "videos_removed_pct_of_uploads": 0.009,
        "automated_removed": 184378987,
        "automated_removed_source_url": TT_REPORT_SOURCE,
        "automation_rate": 0.874,
        "reinstated": 7525184,
        "reinstated_source_url": TT_REPORT_SOURCE,
        "proactive_rate": 0.990,
        "proactive_rate_source_url": TT_REPORT_SOURCE,
        "within_24h_rate": 0.943,
        "within_24h_rate_source_url": TT_REPORT_SOURCE,
        "violation_breakdown": {
            "sensitive_mature_pct": 0.301,
            "sensitive_mature_pct_source_url": TT_REPORT_SOURCE,
            "misinformation_pct": 0.455,
            "misinformation_pct_source_url": TT_REPORT_SOURCE,
            "edited_media_ai_pct": 0.138,
            "edited_media_ai_pct_source_url": TT_REPORT_SOURCE,
            "safety_civility_pct": 0.115,
            "safety_civility_pct_source_url": TT_REPORT_SOURCE,
            "privacy_security_pct": 0.156,
            "privacy_security_pct_source_url": TT_REPORT_SOURCE,
        },
    })

    # ── Q6: 四平台 SLA 对照表 (V5: bot 声称 YT=3个月，官方=6个月) ──────────
    _wj(pe / "internal" / "platform_sla.json", {
        "schema_version": "1.0",
        "youtube": {
            "appeal_window_strike_months": 6.0,
            "appeal_window_strike_months_source_url": YT_APPEAL_SOURCE,
            "appeal_window_content_months": 12.0,
            "appeal_window_content_months_source_url": YT_APPEAL_SOURCE,
            "note": "Bot summary claiming 3 months is incorrect; official YouTube documentation confirms 6 months",
        },
        "meta": {
            "appeal_window_months": None,
            "note": "Meta does not publish a specific appeal window duration in the same way",
        },
        "tiktok": {
            "strike_expiry_days": 90,
            "strike_expiry_days_source_url": TT_SUPPORT_SOURCE,
        },
        "reddit": {
            "appeal_window_months": 6.0,
            "appeal_window_months_source_url": RD_HELP_SOURCE,
        },
    })

    # ── Q7: 废弃旧版合规报告标记 (V6: 红鲱鱼) ─────────────────────────────────
    _wj(pe / "reports" / "deprecation_log.json", {
        "schema_version": "1.0",
        "generated_at": "2025-12-01",
        "archived_report": "reports/archived/compliance_report_v0.md",
        "archived_report_last_updated": "2024-03-01",
        "note": "The archived report contains outdated values. Do NOT reference it for current policy data.",
        "entries": [
            {
                "field": "meta_strike_7_duration",
                "old_value": 3,
                "old_value_unit": "days",
                "correct_value": 1,
                "correct_value_unit": "days",
                "correct_value_source_url": META_RESTRICT_SOURCE,
                "deprecated": True,
                "reason": "Archived 2024 report incorrectly recorded Strike 7 as 3 days; official value is 1 day",
            },
            {
                "field": "youtube_appeal_window_strike",
                "old_value": 3,
                "old_value_unit": "months",
                "correct_value": 6,
                "correct_value_unit": "months",
                "correct_value_source_url": YT_APPEAL_SOURCE,
                "deprecated": True,
                "reason": "Archived 2024 report recorded 3-month appeal window; official YouTube documentation confirms 6 months",
            },
        ],
    })

    # ── Q8: 四平台违规分级对比文档 (P4 footnotes) ─────────────────────────────
    _w(pe / "internal" / "policy_matrix_summary.md",
       "# Cross-Platform Violation Tier Comparison\n\n"
       "A comparative analysis of content violation enforcement tiers across YouTube, Meta, TikTok, and Reddit.\n\n"
       "## YouTube\n\n"
       "YouTube uses a three-strike system within a rolling 90-day window.[^1]\n\n"
       "| Level | Action | Duration |\n"
       "|---|---|---|\n"
       "| Warning | No restrictions; policy training available | 90 days |\n"
       "| Strike 1 | All posting features disabled | **7 days** freeze |\n"
       "| Strike 2 | All posting features disabled | 14 days freeze |\n"
       "| Strike 3 | Channel permanently removed | Permanent |\n\n"
       "Appeal window: 6 months for strikes; 1 year for content removals.[^2]\n\n"
       "## Meta\n\n"
       "Meta uses a graduated strike ladder for standard violations.[^3]\n\n"
       "| Strike | Action |\n"
       "|---|---|\n"
       "| Strike 1 | Warning only |\n"
       "| Strikes 2–6 | Feature restrictions |\n"
       "| Strike 7 | **1-day** content creation ban |\n"
       "| Strike 8 | 3-day ban |\n"
       "| Strike 9 | 7-day ban |\n"
       "| Strike 10+ | 30-day ban |\n\n"
       "Note: Strike 7 is a **1-day ban**. The email from Jordan incorrectly claimed 3 days — "
       "the official Meta Transparency page confirms the value is 1 day.[^3]\n\n"
       "## TikTok\n\n"
       "TikTok uses a **three-strike policy** leading to permanent account ban.[^4]\n\n"
       "- Strike expiry: 90 days from issuance\n"
       "- **Three strikes** within the active window triggers a permanent ban\n"
       "- Note: A Feishu DM from Maya incorrectly stated two strikes leads to permanent ban; "
       "the official policy requires **THREE strikes**.[^4]\n\n"
       "## Reddit\n\n"
       "Reddit uses a four-tier graduated enforcement model.[^5]\n\n"
       "| Tier | Action | Duration |\n"
       "|---|---|---|\n"
       "| Tier 1 | Warning | None |\n"
       "| Tier 2 | Suspension | **3 days** |\n"
       "| Tier 3 | Suspension | 7 days |\n"
       "| Tier 4 | Permanent ban | Permanent |\n\n"
       "Appeal window: 6 months from notification.[^5]\n\n"
       "H1 2025 enforcement (admin level): Harassment 68,550 removals; "
       "Hateful content 98,798 removals; Terrorism 980 removals.[^6]\n\n"
       "## 参考来源\n\n"
       "[^1]: YouTube Community Guidelines Strike Basics — "
       "https://support.google.com/youtube/answer/2802032?hl=en\n"
       "[^2]: YouTube Appeal Procedures — "
       "https://support.google.com/youtube/answer/185111?hl=en\n"
       "[^3]: Meta Restricting Accounts — "
       "https://transparency.meta.com/enforcement/taking-action/restricting-accounts/\n"
       "[^4]: TikTok Content Violations and Bans — "
       "https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans\n"
       "[^5]: Reddit Content Moderation, Enforcement, and Appeals — "
       "https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals\n"
       "[^6]: Reddit NY S895B/A6789B Transparency Report, January 2026 — "
       "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf\n")

    # ── Q9: 更新 appeal_tracker (already applied via update_1/update_2) ───────
    # The update_2 version of appeal_tracker.json is already applied in prep_workspace().
    # No additional writes needed; check_q9 will validate the update_1 state.
    # But we need to make sure the appeal tracker has the correct structure for Q9 check.
    # The upd1/appeal_tracker.json is what Q9 uses (before upd2 further modifies it).
    # For gold solve, upd2 appeal_tracker is already in place — check_q9 should still pass
    # because T-001..T-007 exist (pending in upd2), Y-001..Y-006, M-001..M-005, R-001..R-002 also exist.
    # We need to verify the existing file passes check_q9.
    # Re-apply upd1 tracker first, then override with upd2 on top (as done in prep_workspace).
    # The tracker already in pe/internal/appeal_tracker.json is upd2 version — which has all cases.
    # check_q9 tests OLD-0050/0051/0052 = under_review AND T/Y/M/R cases exist.
    # upd2 tracker should still have these.
    at_path = pe / "internal" / "appeal_tracker.json"
    at_data = json.loads(at_path.read_text(encoding="utf-8"))
    # Ensure OLD-0050/0051/0052 are under_review (upd1 changed them)
    cases = at_data.get("cases", {})
    for k in ("OLD-0050", "OLD-0051", "OLD-0052"):
        if k in cases:
            cases[k]["status"] = "under_review"
    at_data["total_cases"] = len(cases)
    _wj(at_path, at_data)

    # ── Q10: 信息冲突报告 ───────────────────────────────────────────────────────
    _wj(pe / "internal" / "conflict_report.json", {
        "schema_version": "1.0",
        "generated_at": "2025-12-15",
        "scan_scope": ["slack_channel", "feishu_dm", "email", "discord_modops"],
        "conflicts": [
            {
                "id": "conflict_meta_strike_7",
                "topic": "meta_strike_7_duration",
                "source_channel": "email_pm_jordan",
                "claimed_value": "3 days",
                "official_value": "1 day",
                "official_url": META_RESTRICT_SOURCE,
                "note": "Jordan Kim's email claims Meta Strike 7 = 3 days; official Meta Transparency page confirms 1 day. PolicyBot summary also incorrectly repeats 3 days.",
                "bot_summary_involved": True,
            },
            {
                "id": "conflict_youtube_appeal_window",
                "topic": "youtube_appeal_window_strike",
                "source_channel": "slack_compliance_bot",
                "claimed_value": "3 months",
                "official_value": "6 months",
                "official_url": YT_APPEAL_SOURCE,
                "note": "Slack #compliance bot summary claims YouTube strike appeal window is 3 months; official documentation confirms 6 months.",
                "bot_summary_involved": True,
            },
            {
                "id": "conflict_tiktok_permanent_ban_threshold",
                "topic": "tiktok_permanent_ban_strikes",
                "source_channel": "feishu_dm_maya",
                "claimed_value": "2 strikes",
                "official_value": "3 strikes",
                "official_url": TT_SUPPORT_SOURCE,
                "note": "Feishu DM from Maya Patel references old SOP claiming TikTok permanent ban occurs after 2 strikes; official policy requires 3 strikes.",
                "bot_summary_involved": False,
            },
        ],
    })

    # ── Q11: 跨轮数值闭合校验 ────────────────────────────────────────────────
    # Read actual values from source files
    yt_ss = json.loads((pe / "platforms" / "youtube" / "strike_system.json").read_text())
    meta_ss = json.loads((pe / "platforms" / "meta" / "strike_system.json").read_text())
    tt_q1 = json.loads((pe / "platforms" / "tiktok" / "q1_2025_report.json").read_text())

    yt_s1_freeze = yt_ss["strike1"]["freeze_days"]
    meta_s9_days = meta_ss["strikes"]["strike_9"]["content_ban_days"]
    tt_removed = tt_q1["videos_removed"]

    _wj(pe / "reports" / "cross_validation.json", {
        "schema_version": "1.0",
        "validation_date": "2025-12-15",
        "status": "no_drift_detected",
        "youtube": {
            "strike1_freeze_days": yt_s1_freeze,
            "expected_value": 7,
            "actual_value_found": yt_s1_freeze,
            "source_file": "platforms/youtube/strike_system.json",
            "source_field": "strike1.freeze_days",
            "match": yt_s1_freeze == 7,
        },
        "meta": {
            "strike9_ban_days": meta_s9_days,
            "expected_value": 7,
            "actual_value_found": meta_s9_days,
            "source_file": "platforms/meta/strike_system.json",
            "source_field": "strikes.strike_9.content_ban_days",
            "match": meta_s9_days == 7,
        },
        "tiktok": {
            "videos_removed_q1_2025": tt_removed,
            "expected_value": 211000000,
            "actual_value_found": tt_removed,
            "source_file": "platforms/tiktok/q1_2025_report.json",
            "source_field": "videos_removed",
            "match": tt_removed == 211000000,
        },
    })

    # ── Q12: update_2 supersede — TikTok T-001..T-007 → pending ─────────────
    # The appeal tracker from upd2 already has T-001..T-007 as pending.
    # Ensure Y-001..Y-006 are NOT pending (V10: only TikTok subset superseded).
    # The upd2 tracker sets YouTube cases as approved. Verify and write q3_2025_report.json.
    # q3_2025_report.json was already applied from upd2.
    # Verify the tracker is correctly set.
    at_data2 = json.loads(at_path.read_text(encoding="utf-8"))
    cases2 = at_data2.get("cases", {})
    # TikTok cases must be pending
    for tid in ["T-%03d" % i for i in range(1, 8)]:
        if tid in cases2:
            cases2[tid]["status"] = "pending"
    # YouTube cases must remain approved (NOT pending)
    for yid in ["Y-%03d" % i for i in range(1, 7)]:
        if yid in cases2 and cases2[yid].get("status") == "pending":
            cases2[yid]["status"] = "approved"
    at_data2["total_cases"] = len(cases2)
    _wj(at_path, at_data2)

    # ── Q13: 违规案例统计 (P5 命名约定) ─────────────────────────────────────
    # Read violation log and compute platform stats
    vlog_path = pe / "internal" / "violation_log_2025.csv"
    platform_data: dict[str, dict] = {}
    with vlog_path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            plat = row.get("platform", "").lower().strip()
            vtype = row.get("violation_type", "unknown")
            if not plat:
                continue
            if plat not in platform_data:
                platform_data[plat] = {"total_count": 0, "by_type": {}}
            platform_data[plat]["total_count"] += 1
            platform_data[plat]["by_type"][vtype] = platform_data[plat]["by_type"].get(vtype, 0) + 1

    # P5 naming: violation_stats_latest.json
    _wj(pe / "reports" / "violation_stats_latest.json", {
        "schema_version": "1.0",
        "generated_at": "2025-12-15",
        "source_file": "internal/violation_log_2025.csv",
        "platforms": platform_data,
    })

    # ── Q14: 内部执行 SOP 文档 (P4 + 来源 URLs) ──────────────────────────────
    _w(pe / "internal" / "sop_enforcement.md",
       "# CreatorHub Content Moderation SOP\n\n"
       "Standard Operating Procedures for content moderation enforcement across "
       "YouTube, Meta, TikTok, and Reddit platforms.\n\n"
       "## YouTube\n\n"
       "YouTube uses a three-strike system within a rolling 90-day window.[^1]\n\n"
       "**Appeal Procedures:**\n\n"
       "- Strikes and warnings: appeal within **6 months** of notification[^2]\n"
       "- Content removals (videos, posts, playlists, thumbnails, URLs): "
       "appeal within **12 months** (1 year) of removal[^2]\n"
       "- Each violation may be appealed once; rejected appeal carries no additional penalty\n\n"
       "**Enforcement Workflow:**\n\n"
       "1. Content flagged (automated or user report)\n"
       "2. Human reviewer assesses against Community Guidelines (24/7 review team)\n"
       "3. If violation confirmed: content removed + creator notified\n"
       "4. Strike issued; creator may complete policy training to reset warning period\n\n"
       "## Meta\n\n"
       "Meta uses a graduated strike ladder for standard violations.[^3]\n\n"
       "Strike 7 = **1-day** content creation ban (includes posting, commenting, creating pages).\n\n"
       "**Enforcement Workflow:**\n\n"
       "1. Violation detected by automated system or user report\n"
       "2. Content removed or restricted\n"
       "3. Account strike applied per the ladder\n"
       "4. Restrictions lift automatically after the specified period\n\n"
       "## TikTok\n\n"
       "TikTok uses a three-strike policy with 90-day strike expiry.[^4]\n\n"
       "**Enforcement Workflow:**\n\n"
       "1. Violation detected\n"
       "2. Video removed; creator notified\n"
       "3. Strike added to account (expires after 90 days)\n"
       "4. Three strikes trigger permanent account ban\n\n"
       "## Reddit\n\n"
       "Reddit uses a four-tier enforcement model with a **6-month appeal window**.[^5]\n\n"
       "Tier 2 = **3-day suspension**; Tier 3 = **7-day suspension**.\n\n"
       "**Appeal Procedure:**\n\n"
       "Users may appeal within **6 months** of the enforcement notification.\n"
       "Appeals are processed in a timely, non-discriminatory, and non-arbitrary manner.[^5]\n\n"
       "## 来源参考\n\n"
       "[^1]: YouTube Strike Basics — "
       "https://support.google.com/youtube/answer/2802032?hl=en\n"
       "[^2]: YouTube Appeal Procedures — "
       "https://support.google.com/youtube/answer/185111?hl=en\n"
       "[^3]: Meta Restricting Accounts — "
       "https://transparency.meta.com/enforcement/taking-action/restricting-accounts/\n"
       "[^4]: TikTok Content Violations and Bans — "
       "https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans\n"
       "[^5]: Reddit Content Moderation, Enforcement, and Appeals — "
       "https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals\n")

    # ── Q15: EU DSA 监管合规 (V9: Art. 34/35 verbatim; V2: Reddit not VLOP) ─
    _wj(pe / "internal" / "regulatory_addendum.json", {
        "schema_version": "1.0",
        "regulation": "EU_DSA",
        "regulation_full_name": "Digital Services Act (Regulation (EU) 2022/2065)",
        "regulation_source_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R2065",
        "effective_date": "2024-02-17",
        "vlop_threshold_eu_users": 45000000,
        "affected_platforms": ["youtube", "meta", "tiktok"],
        "non_affected_platforms": ["reddit"],
        "reddit_non_vlop_rationale": "Reddit does not meet the 45M EU active user threshold for VLOP designation. Initial email draft suggested Reddit might qualify; subsequent legal team email (legal@creatorhub.com) confirmed Reddit is NOT a VLOP and supersedes the earlier draft.",
        "article_reference": ["Art. 34", "Art. 35"],
        "article_reference_extended": ["Art. 34", "Art. 35", "Art. 40", "Art. 42"],
        "key_obligations": {
            "Art. 34": "Annual systemic risk assessment (fundamental rights, civic discourse, psychological well-being, public security)",
            "Art. 35": "Reasonable and proportionate risk mitigation measures addressing Art. 34 risks",
            "Art. 40": "Data access for vetted researchers studying systemic risks",
            "Art. 42": "Semi-annual transparency reporting including moderation statistics",
        },
    })

    # ── Q16: 最终合规报告 + sha256 sign-off (V7) ─────────────────────────────
    report_txt = (
        "# CreatorHub Policy Engine — Final Compliance Report\n\n"
        "**Generated:** 2025-12-20\n\n"
        "## Executive Summary\n\n"
        "This report summarizes the state of the CreatorHub content moderation policy engine "
        "as of December 2025, covering enforcement tier mappings for YouTube, Meta, TikTok, "
        "and Reddit, along with appeal window compliance, conflict analysis, and EU DSA status.\n\n"
        "## Platform Policy Summaries\n\n"
        "### YouTube\n\n"
        "- Warning: 90-day expiry, no restrictions\n"
        "- Strike 1: 7-day posting freeze\n"
        "- Strike 2: 14-day posting freeze (within same 90-day window)\n"
        "- Strike 3: Channel permanent removal\n"
        "- Appeal window: 6 months (strikes), 12 months (content removals)\n"
        "- Source: https://support.google.com/youtube/answer/2802032?hl=en\n\n"
        "### Meta\n\n"
        "- 27 policy categories (US English, 2025)\n"
        "- Strike 7: 1-day content creation ban\n"
        "- Strike 8: 3-day ban; Strike 9: 7-day ban; Strike 10+: 30-day ban\n"
        "- Source: https://transparency.meta.com/enforcement/taking-action/restricting-accounts/\n\n"
        "### TikTok\n\n"
        "- Three-strike policy; strikes expire after 90 days\n"
        "- Q1 2025: 211,000,000 videos removed (~0.9% of uploads)\n"
        "- Automated removals: 184378987 (99.0% proactive; 94.3% within 24 hours)\n"
        "- Reinstated after review: 7,525,184 videos\n"
        "- Source: https://www.tiktok.com/transparency/en/community-guidelines-enforcement-2025-1\n\n"
        "### Reddit\n\n"
        "- Tier 1: Warning; Tier 2: 3-day suspension; Tier 3: 7-day suspension; Tier 4: Permanent ban\n"
        "- H1 2025 (admin-level): Harassment 68550 removals; Hateful 98,798 removals; Terrorism 980 removals\n"
        "- Hateful content appeal reversal rate: 30.0%\n"
        "- Source: https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf\n\n"
        "## Appeal Window Comparison Table\n\n"
        "| Platform | Strike Appeal Window | Content Appeal Window |\n"
        "|---|---|---|\n"
        "| YouTube | **6 months** | **12 months (1 year)** |\n"
        "| Meta | Not specified | Not specified |\n"
        "| TikTok | Not specified | Not specified |\n"
        "| Reddit | **6 months** | **6 months** |\n\n"
        "## Conflicts and Discrepancies Analysis\n\n"
        "Three significant data conflicts were identified during policy engine construction:\n\n"
        "1. **Meta Strike 7 Duration**: Jordan Kim's email claimed 3 days. "
        "Official Meta Transparency page confirms **1 day**. PolicyBot summary also incorrect.\n"
        "2. **YouTube Appeal Window**: Slack #compliance bot summary claimed 3 months. "
        "Official YouTube documentation confirms **6 months**.\n"
        "3. **TikTok Permanent Ban Threshold**: Feishu DM from Maya Patel cited old SOP "
        "claiming 2 strikes. Official policy confirms **3 strikes**.\n\n"
        "See `internal/conflict_report.json` for complete conflict records.\n\n"
        "## EU DSA Compliance Status\n\n"
        "YouTube, Meta, and TikTok are designated VLOPs requiring Art. 34/35 compliance.\n"
        "Reddit is NOT a VLOP (below 45M EU user threshold).\n\n"
        "See `internal/regulatory_addendum.json` for full DSA regulatory addendum.\n"
    )
    report_path = pe / "reports" / "compliance_report_final.md"
    _w(report_path, report_txt)

    # Compute sha256 and write signoff
    digest = hashlib.sha256(report_path.read_bytes()).hexdigest()
    _wj(pe / "reports" / "compliance_signoff.json", {
        "schema_version": "1.0",
        "signed_file": "reports/compliance_report_final.md",
        "sha256": digest,
        "signed_at": "2025-12-20T00:00:00Z",
    })

    print(f"[prd2 gold] All deliverables written to {ws}")


# --------------------------------------------------------------------------- #
# Check runner
# --------------------------------------------------------------------------- #
EVAL_CMDS: dict[str, list] = {
    "q1":  ["check_q1.py", ("pref", "P1", "policy_engine/platforms/youtube/index.json")],
    "q2":  ["check_q2.py", ("pref", "P1,P2", "policy_engine/platforms/youtube/strike_system.json")],
    "q3":  ["check_q3.py", ("pref", "P1,P2", "policy_engine/platforms/meta/strike_system.json")],
    "q4":  ["check_q4.py", ("pref", "P1,P2", "policy_engine/platforms/reddit/enforcement_tiers.json")],
    "q5":  ["check_q5.py", ("pref", "P1,P2", "policy_engine/platforms/tiktok/q1_2025_report.json")],
    "q6":  ["check_q6.py", ("pref", "P1,P2,P3", "policy_engine/internal/platform_sla.json")],
    "q7":  ["check_q7.py", ("pref", "P1", "policy_engine/reports/deprecation_log.json")],
    "q8":  ["check_q8.py", ("pref", "P4", "policy_engine/internal/policy_matrix_summary.md")],
    "q9":  ["check_q9.py", ("pref", "P1", "policy_engine/internal/appeal_tracker.json")],
    "q10": ["check_q10.py", ("pref", "P1", "policy_engine/internal/conflict_report.json")],
    "q11": ["check_q11.py"],
    "q12": ["check_q12.py"],
    "q13": ["check_q13.py", ("pref", "P5", "policy_engine/reports/")],
    "q14": ["check_q14.py", ("pref", "P4", "policy_engine/internal/sop_enforcement.md")],
    "q15": ["check_q15.py", ("pref", "P1", "policy_engine/internal/regulatory_addendum.json")],
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
    out = (r.stdout + r.stderr).strip()
    last = out.splitlines()[-1] if out else ""
    return r.returncode == 0, last


def main() -> None:
    ws = prep_workspace()
    solve(ws)
    print("=== GOLD SOLUTION: every check must PASS ===")
    n_pass = n_fail = 0
    for q, items in EVAL_CMDS.items():
        for it in items:
            ok, last = run_check(it, ws)
            tag = ("pref " + it[1]) if isinstance(it, tuple) else "main"
            status = "PASS" if ok else "FAIL"
            if ok:
                n_pass += 1
            else:
                n_fail += 1
                print(f"  [{status}] {q} ({tag}): {last}")
    print(f"gold: {n_pass} checks PASSED, {n_fail} FAILED")

    # ── 反例抽样（错误产物必须 FAIL）────────────────────────────────────────
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    pe = ws / "policy_engine"
    probes = 0
    caught = 0

    # 1. Q2: strike1.freeze_days = 10 (decoy)
    yt_bad = json.loads((pe / "platforms" / "youtube" / "strike_system.json").read_text())
    yt_bad["strike1"]["freeze_days"] = 10
    _wj(pe / "platforms" / "youtube" / "strike_system.json", yt_bad)
    ok, _ = run_check("check_q2.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q2 strike1.freeze_days=10 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # Restore
    yt_bad["strike1"]["freeze_days"] = 7
    _wj(pe / "platforms" / "youtube" / "strike_system.json", yt_bad)

    # 2. Q3: strike_7.content_ban_days = 3 (email error)
    meta_bad = json.loads((pe / "platforms" / "meta" / "strike_system.json").read_text())
    meta_bad["strikes"]["strike_7"]["content_ban_days"] = 3
    _wj(pe / "platforms" / "meta" / "strike_system.json", meta_bad)
    ok, _ = run_check("check_q3.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q3 strike_7.content_ban_days=3 (email error) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # Restore
    meta_bad["strikes"]["strike_7"]["content_ban_days"] = 1
    _wj(pe / "platforms" / "meta" / "strike_system.json", meta_bad)

    # 3. Q6: youtube.appeal_window_strike_months = 3.0 (bot decoy)
    sla_bad = json.loads((pe / "internal" / "platform_sla.json").read_text())
    sla_bad["youtube"]["appeal_window_strike_months"] = 3.0
    _wj(pe / "internal" / "platform_sla.json", sla_bad)
    ok, _ = run_check("check_q6.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q6 youtube.appeal_window_strike_months=3.0 (bot decoy) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # Restore
    sla_bad["youtube"]["appeal_window_strike_months"] = 6.0
    _wj(pe / "internal" / "platform_sla.json", sla_bad)

    # 4. Q12: Y-001 reset to pending (V10 violation — only TikTok should be pending)
    at_bad = json.loads((pe / "internal" / "appeal_tracker.json").read_text())
    at_bad["cases"]["Y-001"]["status"] = "pending"
    _wj(pe / "internal" / "appeal_tracker.json", at_bad)
    ok, _ = run_check("check_q12.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q12 Y-001 wrongly reset to pending (V10) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # Restore
    at_bad["cases"]["Y-001"]["status"] = "approved"
    _wj(pe / "internal" / "appeal_tracker.json", at_bad)

    # 5. Q15: reddit in affected_platforms (supersede violation)
    dsa_bad = json.loads((pe / "internal" / "regulatory_addendum.json").read_text())
    dsa_bad["affected_platforms"] = ["youtube", "meta", "tiktok", "reddit"]
    _wj(pe / "internal" / "regulatory_addendum.json", dsa_bad)
    ok, _ = run_check("check_q15.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q15 reddit wrongly in affected_platforms -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # Restore
    dsa_bad["affected_platforms"] = ["youtube", "meta", "tiktok"]
    _wj(pe / "internal" / "regulatory_addendum.json", dsa_bad)

    # 6. Q16: placeholder sha256
    signoff_bad = json.loads((pe / "reports" / "compliance_signoff.json").read_text())
    signoff_bad["sha256"] = "0" * 64
    _wj(pe / "reports" / "compliance_signoff.json", signoff_bad)
    ok, _ = run_check("check_q16.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q16 placeholder sha256 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # Restore
    real_digest = hashlib.sha256((pe / "reports" / "compliance_report_final.md").read_bytes()).hexdigest()
    signoff_bad["sha256"] = real_digest
    _wj(pe / "reports" / "compliance_signoff.json", signoff_bad)

    # 7. Q5: automated_removed rounded to 184000000 (bot summary decoy — not exact)
    tt_bad = json.loads((pe / "platforms" / "tiktok" / "q1_2025_report.json").read_text())
    tt_bad["automated_removed"] = 184000000
    _wj(pe / "platforms" / "tiktok" / "q1_2025_report.json", tt_bad)
    ok, _ = run_check("check_q5.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q5 automated_removed=184000000 (rounded) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # Restore
    tt_bad["automated_removed"] = 184378987
    _wj(pe / "platforms" / "tiktok" / "q1_2025_report.json", tt_bad)

    # 8. Q4: harassment.removed = 70000 (Feishu estimate, not exact)
    rd_bad = json.loads((pe / "platforms" / "reddit" / "enforcement_tiers.json").read_text())
    rd_bad["h1_2025"]["harassment"]["removed"] = 70000
    _wj(pe / "platforms" / "reddit" / "enforcement_tiers.json", rd_bad)
    ok, _ = run_check("check_q4.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q4 harassment.removed=70000 (Feishu estimate, ±2%% violation) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # Restore
    rd_bad["h1_2025"]["harassment"]["removed"] = 68550
    _wj(pe / "platforms" / "reddit" / "enforcement_tiers.json", rd_bad)

    # 9. Q15: vlop_threshold_eu_users missing / wrong value
    dsa_bad2 = json.loads((pe / "internal" / "regulatory_addendum.json").read_text())
    del dsa_bad2["vlop_threshold_eu_users"]
    _wj(pe / "internal" / "regulatory_addendum.json", dsa_bad2)
    ok, _ = run_check("check_q15.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q15 vlop_threshold_eu_users missing -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # Restore
    dsa_bad2["vlop_threshold_eu_users"] = 45000000
    _wj(pe / "internal" / "regulatory_addendum.json", dsa_bad2)

    # 10. Q1: tiktok safety_civility is string (not object with q1_2025_removal_pct)
    tt_idx_bad = json.loads((pe / "platforms" / "tiktok" / "index.json").read_text())
    tt_idx_bad["safety_civility"] = "Q1 2025 Safety & Civility category"
    _wj(pe / "platforms" / "tiktok" / "index.json", tt_idx_bad)
    ok, _ = run_check("check_q1.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q1 tiktok safety_civility is string (not object) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # Restore
    tt_idx_bad["safety_civility"] = {
        "q1_2025_removal_pct": 0.115,
        "q1_2025_removal_pct_source_url": TT_REPORT_SOURCE,
        "description": "Content promoting violence, harassment, or endangering physical safety",
    }
    _wj(pe / "platforms" / "tiktok" / "index.json", tt_idx_bad)

    print(f"negatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
