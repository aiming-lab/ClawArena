#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_prd2.py — 生成 ClawArena 真实数据集场景 prd2（内容审核政策执行）。

题材与锚点取材真实（YouTube / Meta / TikTok / Reddit 公开合规文件），
session 对话与 workspace 文档围绕真实锚点合成。全 exec_check，16 轮。

幂等：每次运行先清空 prd2 的 workspace/state/updates 后重建，再注册元数据。
questions.json 与 check 脚本由 eval/prd2/ 下静态文件提供，本脚本不生成它们。

运行：python scripts/clawarena_authoring/build_prd2.py
"""
from __future__ import annotations

import csv
import io
import json
import random
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, est_tokens, gen_session_id,
    dump_register_meta,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "prd2"
CWD = f"/workspace/{TID}/policy_engine"
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

1. Read `SOUL.md` to understand your working principles as Compliance Engineer.
2. Read `USER.md` to learn about the team and communication channels.
3. Run `exec ls -R` to inspect the current workspace files under `policy_engine/`.
4. Use `sessions_list` to see all available history sessions (Slack, Feishu, Email, Discord).
5. Use `sessions_history` to read relevant session content as needed.

You are a Compliance Engineering AI assistant supporting the CreatorHub content policy team.
Your primary task is to build and maintain a unified content moderation compliance engine
that aligns with YouTube, Meta, TikTok, and Reddit community guidelines.
""")

    w(WS / "SOUL.md", """# Working Principles

1. **Authoritative-source-first**: The canonical policy definitions and ground-truth figures
   live in `platforms/{platform}/strike_system.json`, official platform documentation files,
   and `internal/` reference files. Auto-generated bot summaries (e.g. files prefixed with
   `BOT_SUMMARY_`) and archived reports under `reports/archived/` are NOT authoritative —
   verify any quoted number against the official platform files.

2. **Verbatim policy references**: Always reference official policy category names and
   rule text exactly as they appear in the platform documentation. Renaming, paraphrasing,
   or abbreviating is a defect.

3. **JSON formatting discipline (P1)**: Every JSON deliverable uses 2-space indentation
   and snake_case key names. No camelCase keys.

4. **Source attribution (P2)**: All numeric fields in JSON deliverables carry a
   companion `_source_url` field at the same JSON level documenting the authoritative URL.

5. **Temporal awareness**: Policy updates arrive incrementally via multiple channels.
   When a Discord modops notice or a subsequent email supersedes an earlier instruction,
   the later instruction wins — revisit and revise prior outputs rather than stacking
   contradictory logic.

6. **Unit discipline (P3)**: Time-limit values are expressed in months as the primary
   unit, retaining 1 decimal place (e.g. `3.0` months, `0.5` months for 14 days).

7. **Citation format (P4)**: Markdown documents use `[^N]` footnote references and
   include a `## 参考来源` (or `## References`) section at the document end.

8. **Report naming (P5)**: Files under `reports/` follow the naming convention
   `{type}_{yyyy-mm}.json`. When no specific month applies, use `latest`.
""")

    w(WS / "USER.md", """# People and Channels

## Primary User
- **Lin Wei** — Head of Compliance Engineering. Oversees the CreatorHub policy engine.
  Expects precise numerical citations, verbatim policy references, and clean JSON schemas.

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Alex Torres | Policy Analyst | Slack #compliance | Tracks platform policy updates; sometimes relays bot-summarised stats |
| Maya Patel | Legal Counsel | Feishu DM | Provides legal interpretation of policy clauses; occasionally cites outdated documents |
| Jordan Kim | Product Manager | Email | Sends platform execution data; has been known to misquote Meta strike durations |
| Sam Rivera | Moderation Ops Lead | Discord #mod-ops | Manages appeal case batches; issues supersede notices for case-status changes |

## Channels
- **Slack #compliance**: Platform policy version discussions (Alex, policy bot summaries)
- **Feishu DM (Maya → agent)**: Legal counsel on rule verbatim text and citations
- **Email (Jordan → agent)**: Meta/TikTok execution metrics and strike data
- **Discord #mod-ops (Sam)**: Appeal case updates, moderation operations notices
""")

    w(WS / "IDENTITY.md", """# Identity

You are **PolicyOps AI**, a compliance engineering assistant deployed to support the
CreatorHub content moderation team. You help build and validate a unified policy engine
that maps YouTube, Meta, TikTok, and Reddit community guidelines to internal enforcement
tiers, SLA commitments, and appeal procedures.

You maintain the `policy_engine/` workspace: platform policy JSONs, violation logs,
appeal trackers, and compliance reports. Source documents under `platforms/` and `internal/`
are reference inputs; you create deliverables by writing or updating files in this workspace.
""")

    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session to discover history |
| `sessions_history` | Read a specific history session | Use in the main session to review past discussion |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to `ls`, run scripts, and to **write your deliverable files** |

## Rules
- Source policy documents under `platforms/` and archived files under `reports/archived/`
  are **read-only** reference inputs — do not modify them.
- You DO create new deliverable files under `internal/`, `reports/`, and within `platforms/`
  as tasks require, using `exec` (e.g. heredoc / python). That is the expected way to complete tasks.
- In history sessions, use only `read` and light `exec`; do not call `sessions_list`/`sessions_history` there.
""")


# --------------------------------------------------------------------------- #
# 2. Platform Policy 参考文件（真实锚点）
# --------------------------------------------------------------------------- #
def gen_platform_docs() -> None:
    pe = WS / "policy_engine"

    # ---------- YouTube ----------
    yt = pe / "platforms" / "youtube"
    w(yt / "community_guidelines.md", """# YouTube Community Guidelines

*Source: https://support.google.com/youtube/answer/9288567?hl=en*
*Source: https://support.google.com/youtube/answer/2802032?hl=en*

YouTube's Community Guidelines define the rules for content on the platform.
All content — videos, comments, links, thumbnails — is subject to these guidelines.
Violations result in strikes or channel termination depending on severity and recurrence.

## Policy Categories

YouTube organizes its content policies into **5 main categories**:

### 1. Spam & Deceptive Practices
Includes misleading metadata, fake engagement, impersonation, scams, and coordinated inauthentic
behavior. Sub-policies: External Links Policy, Fake Engagement Policy, Impersonation Policy,
Misleading Metadata Policy, Scams and Fraud Policy.

### 2. Sensitive Content
Covers content that may be appropriate only for some audiences. Sub-policies: Child Safety Policy,
Custom Thumbnails Policy, Firearms Policy, Harassment and Cyberbullying Policy, Hate Speech Policy,
Suicide and Self-Injury Policy, Violent or Graphic Content Policy, Vulgar Language Policy.

### 3. Violent or Dangerous Content
Addresses threats, dangerous acts, and content promoting violence. Sub-policies: Dangerous Challenges
and Pranks Policy, Extremism Policy, Harassment and Cyberbullying Policy, Hateful Content Policy,
Violent Criminal Organizations Policy, Violent or Graphic Content Policy.

### 4. Regulated Goods
Covers regulated products and services. Sub-policies: Firearms Policy, Illegal or Regulated Goods
or Services Policy.

### 5. Misinformation
Addresses false, misleading or deceptive content. Sub-policies: Elections Misinformation Policy,
Medical Misinformation Policy, Misinformation Policy.

---

## Strike System Overview

YouTube uses a three-strike system within a rolling **90-day window**.

| Level | Action | Duration |
|-------|--------|----------|
| Warning | No restrictions; policy training course available | Expires 90 days after issuance |
| Strike 1 | Upload/post/live-stream/thumbnail/playlist creation disabled | 1 week (7 days) |
| Strike 2 | All posting features disabled | 2 weeks (14 days) |
| Strike 3 | Channel permanently removed | Permanent |

**Critical**: All three strikes must occur within the same 90-day window for channel removal
to trigger. A warning does NOT count as a strike.

---

## Appeal Procedures

- **Strikes and warnings**: Must be appealed within **6 months** of the notification.
- **Content removals** (videos, posts, playlists, thumbnails, URLs): Must be appealed within
  **1 year** of the removal.
- Each strike or violation may be appealed **only once**.
- A rejected appeal does **not** result in additional penalties.
- Outcomes: reinstated, age-restricted, or upheld.

*Source: https://support.google.com/youtube/answer/185111?hl=en*

---

## Transparency FAQ Highlights

- Human reviewers operate 24 hours a day, 7 days a week.
- Flagged content is NOT automatically removed — it is reviewed first.
- Creators retain the right to appeal except for privacy-based removals.

*Source: https://support.google.com/transparencyreport/answer/9209072?hl=en*
""")

    wj(yt / "strike_system.json", {
        "platform": "youtube",
        "schema_version": "1.0",
        "_source_url": "https://support.google.com/youtube/answer/2802032?hl=en",
        "window_days": 90,
        "window_days_source_url": "https://support.google.com/youtube/answer/2802032?hl=en",
        "warning": {
            "expiry_days": 90,
            "expiry_days_source_url": "https://support.google.com/youtube/answer/2802032?hl=en",
            "restrictions": "none",
            "policy_training_available": True,
            "note": "First violation; not a strike; expires 90 days or upon completing policy training"
        },
        "strike1": {
            "freeze_days": 7,
            "freeze_days_source_url": "https://support.google.com/youtube/answer/2802032?hl=en",
            "actions_disabled": ["upload", "post", "live_stream", "thumbnail", "playlist_create"],
            "note": "1-week posting ban; all permissions restored automatically after 7 days"
        },
        "strike2": {
            "freeze_days": 14,
            "freeze_days_source_url": "https://support.google.com/youtube/answer/2802032?hl=en",
            "actions_disabled": ["upload", "post", "live_stream", "thumbnail", "playlist_create"],
            "note": "2-week ban; must occur within same 90-day window as strike 1"
        },
        "strike3": {
            "consequence": "channel_permanent_removal",
            "consequence_source_url": "https://support.google.com/youtube/answer/2802032?hl=en",
            "note": "All 3 strikes must fall within a single 90-day rolling window"
        },
        "appeal": {
            "window_strike_months": 6,
            "window_strike_months_source_url": "https://support.google.com/youtube/answer/185111?hl=en",
            "window_content_months": 12,
            "window_content_months_source_url": "https://support.google.com/youtube/answer/185111?hl=en",
            "appeals_per_violation": 1,
            "note": "Each violation appealable once; rejected appeal carries no additional penalty"
        }
    })

    w(yt / "appeal_procedures.md", """# YouTube Appeal Procedures

*Source: https://support.google.com/youtube/answer/185111?hl=en*

## Overview

YouTube provides creators with a formal appeal mechanism for both strikes/warnings
and content removals. The appeal process is designed to be transparent and fair.

## Appeal Windows

| Content Type | Appeal Window |
|---|---|
| Strikes (all) | **6 months** from notification date |
| Warnings | **6 months** from notification date |
| Videos | **1 year** from removal date |
| Posts | **1 year** from removal date |
| Playlists | **1 year** from removal date |
| Thumbnails | **1 year** from removal date |
| URLs | **1 year** from removal date |

**Important**: Appeals outside these windows will not be accepted.

## Appeal Limits

Each strike or warning may be **appealed only once**. If your appeal is rejected,
you cannot submit another appeal for the same violation. However, a rejected appeal
does **not** result in additional penalties or restrictions.

## Possible Outcomes

After YouTube reviews your appeal:
1. **Reinstated**: The content is restored and the strike/violation is removed.
2. **Age-restricted**: The content remains but is restricted to appropriate audiences.
3. **Upheld**: The original decision stands.

## How to Appeal

1. Sign in to YouTube Studio.
2. Navigate to the notification about the violation.
3. Click "Appeal" and follow the instructions.
4. YouTube will review and send a decision to your email.

## Privacy-Based Removals

Privacy-based content removals are **not eligible for the standard appeal process**.
These are handled through YouTube's separate privacy complaint procedure.
""")

    w(yt / "enforcement_faq.md", """# YouTube Community Guidelines Enforcement FAQ

*Source: https://support.google.com/transparencyreport/answer/9209072?hl=en*

## How does YouTube enforce its Community Guidelines?

YouTube uses a combination of machine learning and human reviewers to enforce its policies.
Human reviewers operate 24 hours a day, 7 days a week.

## Are flagged videos automatically removed?

No. Flagged content is NOT automatically removed. Content flagged by users or detected
by automated systems is routed to human reviewers who apply YouTube's policies.

## What happens when a video violates the guidelines?

1. The content is removed or age-restricted.
2. The creator receives a notification explaining the policy violated.
3. For severe violations, a Community Guidelines strike is issued.
4. The creator can appeal the decision within the applicable window.

## What is a Community Guidelines strike?

A Community Guidelines strike is a formal penalty issued when a video violates
YouTube's policies. The strike remains on the account for 90 days from the date
of issuance. Strikes carry posting restrictions as defined in the strike system.

## Warning vs. Strike

A **warning** is issued for a first-time violation and carries no restrictions
(though a policy training course is available). A **strike** is issued for subsequent
violations or severe first-time violations, and carries posting restrictions.

## Three-Strike Accumulation

For permanent channel removal to occur, **3 strikes must be issued within the same
90-day rolling window**. Strikes older than 90 days do not count toward this threshold.
""")

    # ---------- Meta ----------
    meta = pe / "platforms" / "meta"
    w(meta / "community_standards.md", """# Meta Community Standards

*Source: https://transparency.meta.com/policies/community-standards/*

Meta's Community Standards apply to all content on Facebook and Instagram. They are
organized around four core values: **authenticity, safety, privacy, and dignity**.

As of 2025, Meta's Community Standards contain **27 policy categories**.

## Policy Categories (US English, 2025)

### Violence and Criminal Behavior
1. **Violence and Incitement** — Prohibits content that incites violence or encourages
   real-world harm. Includes calls for action and statements of intent.
2. **Dangerous Organizations and Individuals** — Prohibits terrorist organizations,
   hate groups, and individuals who promote violence.
3. **Coordinating Harm and Promoting Crime** — Addresses coordination of offline harm,
   sale of regulated goods, and promotion of criminal activity.
4. **Restricted Goods and Services** — Covers firearms, drugs, pharmaceutical, tobacco,
   and other regulated items.
5. **Human Exploitation** — Prohibits human trafficking, forced labor, and sexual servitude.
6. **Fraud and Deception** — Addresses scams, fraud, fake accounts, and deceptive practices.

### Safety
7. **Suicide and Self-Injury** — Protects individuals from harmful content while supporting
   survivors and mental health discussions.
8. **Child Sexual Abuse and Nudity (CSAM)** — Zero-tolerance policy for any sexual content
   involving minors. Results in immediate account termination and referral to NCMEC.
9. **Sexual Exploitation of Adults** — Prohibits non-consensual sexual content and
   sextortion.
10. **Bullying and Harassment** — Addresses targeted attacks, unwanted contact, and
    coordinated harassment campaigns.
11. **Privacy Violations and Image Privacy Rights** — Protects personal information and
    prohibits sharing private images without consent.
12. **Violent and Graphic Content** — Prohibits gratuitous violence, glorification of
    suffering, or content designed to shock.

### Objectionable Content
13. **Hate Speech** — Prohibits content that dehumanizes people based on protected
    characteristics including race, ethnicity, religion, gender, sexual orientation, etc.
14. **Violent and Graphic Content** (see #12 above — includes graphic imagery).
15. **Adult Nudity and Sexual Activity** — Defines acceptable and unacceptable sexual content.
16. **Sexual Solicitation** — Prohibits solicitation of sexual services.

### Integrity and Authenticity
17. **Spam** — Addresses unsolicited bulk messaging, fake engagement, and disruptive behavior.
18. **Cybersecurity** — Covers malware, hacking, and unauthorized data collection.
19. **Inauthentic Behavior** — Prohibits fake accounts, coordinated inauthentic behavior,
    and impersonation.
20. **False News** — Addresses misinformation and disputed content.
21. **Memorialization** — Governs memorial accounts and posthumous content requests.

### Intellectual Property
22. **Intellectual Property** — Addresses copyright and trademark infringement.

### User Requests
23. **User Requests** — Handles self-harm reporting and euthanasia/end-of-life requests.

### Additional Policies
24. **Additional Protection for Minors** — Extra safeguards for content involving children.
25. **Regulated Goods** — See #4; expanded for specific contexts.
26. **Account Integrity and Authentic Identity** — Covers real-name policy and account
    verification requirements.
27. **Payments** — Governs transactions conducted through Meta's payment platforms.

**Total: 27 policy categories** as documented in Meta's US English Community Standards.

---

## Enforcement Philosophy

Meta's enforcement is based on four core values:
- **Authenticity**: Content should be genuine and not mislead users.
- **Safety**: Meta is committed to preventing harm.
- **Privacy**: Users control their personal data and how it is shared.
- **Dignity**: All users deserve equal treatment and respect.
""")

    wj(meta / "strike_system.json", {
        "platform": "meta",
        "schema_version": "1.0",
        "_source_url": "https://transparency.meta.com/enforcement/taking-action/restricting-accounts/",
        "description": "Meta strike-based account restriction ladder (Facebook and Instagram)",
        "strikes": {
            "strike_1": {
                "content_ban_days": 0,
                "content_ban_days_source_url": "https://transparency.meta.com/enforcement/taking-action/restricting-accounts/",
                "action": "warning",
                "note": "First violation: warning only, no additional restrictions"
            },
            "strike_2_to_6": {
                "action": "feature_restriction",
                "action_source_url": "https://transparency.meta.com/enforcement/taking-action/restricting-accounts/",
                "restricted_features": ["group_posting", "page_posting"],
                "note": "Strikes 2-6: restricted from specific features (e.g. group posting) for a limited time"
            },
            "strike_7": {
                "content_ban_days": 1,
                "content_ban_days_source_url": "https://transparency.meta.com/enforcement/taking-action/restricting-accounts/",
                "scope": "all_content_creation",
                "note": "7th strike: 1-day ban from all content creation (posting, commenting, creating pages)"
            },
            "strike_8": {
                "content_ban_days": 3,
                "content_ban_days_source_url": "https://transparency.meta.com/enforcement/taking-action/restricting-accounts/",
                "scope": "all_content_creation",
                "note": "8th strike: 3-day ban from all content creation"
            },
            "strike_9": {
                "content_ban_days": 7,
                "content_ban_days_source_url": "https://transparency.meta.com/enforcement/taking-action/restricting-accounts/",
                "scope": "all_content_creation",
                "note": "9th strike: 7-day ban from all content creation"
            },
            "strike_10plus": {
                "content_ban_days": 30,
                "content_ban_days_source_url": "https://transparency.meta.com/enforcement/taking-action/restricting-accounts/",
                "scope": "all_content_creation",
                "note": "10th+ strike: 30-day restriction from all content creation"
            }
        },
        "severe_violations": {
            "note": "CSAM, dangerous organizations trigger longer restrictions from Strike 1",
            "source_url": "https://transparency.meta.com/enforcement/taking-action/restricting-accounts/"
        }
    })

    wj(meta / "q3_2025_metrics.json", {
        "platform": "meta",
        "period": "Q3_2025",
        "schema_version": "1.0",
        "_source_url": "https://transparency.meta.com/reports/integrity-reports-q3-2025/",
        "facebook": {
            "enforcement_precision_pct": ">90%",
            "enforcement_precision_pct_source_url": "https://transparency.meta.com/reports/integrity-reports-q3-2025/",
            "content_removed_incorrectly_pct": "<0.1%",
            "note": "Approximately 1 in 10 removed pieces were errors, but <1 in 1000 overall content"
        },
        "instagram": {
            "enforcement_precision_pct": ">87%",
            "enforcement_precision_pct_source_url": "https://transparency.meta.com/reports/integrity-reports-q3-2025/",
            "note": "Instagram enforcement precision Q3 2025"
        },
        "ncmec_reports": {
            "total": "2M+",
            "inappropriate_child_interactions": 486000,
            "csam_imagery": 1600000,
            "source_url": "https://transparency.meta.com/reports/integrity-reports-q3-2025/"
        },
        "q4_2025_violence_fb_prevalence": {
            "range": "0.15%-0.16%",
            "range_source_url": "https://transparency.meta.com/reports/community-standards-enforcement/",
            "note": "Q4 2025 data from H2 2025 report; decreased from 0.19%-0.20% in Q3"
        }
    })

    w(meta / "enforcement_actions.md", """# Meta Account Restriction and Enforcement Actions

*Source: https://transparency.meta.com/enforcement/taking-action/restricting-accounts/*

## Overview

When someone violates Meta's Community Standards, actions are taken based on the
severity and frequency of violations. Meta uses a graduated "strike" system for
most violations.

## Strike Ladder (Standard Violations)

| Strike Number | Action |
|---|---|
| Strike 1 | Warning only — no additional restrictions |
| Strikes 2–6 | Restricted from specific features (e.g. group posting) for a limited time |
| Strike 7 | Cannot create content for **1 day** |
| Strike 8 | Cannot create content for **3 days** |
| Strike 9 | Cannot create content for **7 days** |
| Strike 10+ | Cannot create content for **30 days** |

"Content creation" includes posting, commenting, creating pages, and other publishing actions.

## Severe Policy Violations

For severe violations (such as CSAM, content from dangerous organizations), additional
longer restrictions apply from Strike 1 onward. These violations may result in immediate
account termination regardless of prior strike count.

## Important Notes

- The strike ladder applies to **standard** policy violations.
- **Strike 7 = 1 day ban** (common confusion point — NOT 3 days).
- Strike 8 is the 3-day ban.
- Restrictions automatically lift after the specified time period.
""")

    # ---------- TikTok ----------
    tt = pe / "platforms" / "tiktok"
    w(tt / "community_guidelines.md", """# TikTok Community Guidelines

*Source: https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans*

TikTok's Community Guidelines establish the rules for content on the platform.
Violations result in graduated enforcement actions up to and including permanent account bans.

## Violation Categories

TikTok organizes content violations into the following major categories:

### Safety & Civility (`safety_civility`)
Content that promotes violence, harassment, bullying, or endangers physical safety.
Includes threats, cyberbullying, and content that incites harm against individuals or groups.
Accounted for **11.5%** of Q1 2025 removed videos.

### Sensitive & Mature Content (`sensitive_mature`)
Content deemed inappropriate for general audiences, including adult themes, graphic imagery,
or content that may disturb viewers. Accounted for **30.1%** of Q1 2025 removed videos.

### Misinformation (`misinformation`)
False or misleading content including health misinformation, election misinformation,
and conspiracy theories. Accounted for **45.5%** of Q1 2025 removed videos.

### Edited Media & AI-Generated Content (`edited_media_ai`)
Deepfakes, manipulated media, and synthetic AI-generated content used to deceive.
Accounted for **13.8%** of Q1 2025 removed videos.

### Privacy & Security (`privacy_security`)
Unauthorized sharing of personal information, doxxing, and privacy violations.
Accounted for **15.6%** of Q1 2025 removed videos.

---

## Strike System

TikTok uses a **three-strike policy** leading to permanent account ban:

| Action | Description |
|---|---|
| Video Removal | Individual video removed; creator notified |
| Shadowban / Reach Reduction | Account visibility reduced without explicit notification |
| Account Warning + Strike | Formal warning with strike added to account |
| Permanent Ban | Account permanently disabled |

**Strike Expiry**: Strikes expire from the account record after **90 days** from issuance.
A permanent ban is triggered by **three strikes** within the active window.

*Source: https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans*

---

## Appeal Process

To appeal a content removal or account action:
1. Tap "Appeal" in the notification you receive.
2. TikTok's safety team reviews the content against Community Guidelines.
3. If appeal is successful, the content is reinstated and the penalty is removed.
""")

    wj(tt / "strike_system.json", {
        "platform": "tiktok",
        "schema_version": "1.0",
        "_source_url": "https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans",
        "strike_expiry_days": 90,
        "strike_expiry_days_source_url": "https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans",
        "permanent_ban_threshold": {
            "strikes_required": 3,
            "strikes_required_source_url": "https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans",
            "note": "Three strikes within the active 90-day window triggers permanent account ban"
        },
        "enforcement_actions": [
            "video_removal",
            "shadowban_reach_reduction",
            "account_warning_with_strike",
            "permanent_ban"
        ],
        "appeal": {
            "method": "tap_appeal_in_notification",
            "reviewer": "safety_team",
            "outcome_if_successful": "content_reinstated_penalty_removed"
        }
    })

    wj(tt / "q1_2025_report.json", {
        "platform": "tiktok",
        "period": "Q1_2025",
        "schema_version": "1.0",
        "_source_url": "https://www.tiktok.com/transparency/en/community-guidelines-enforcement-2025-1",
        "videos_removed": 211000000,
        "videos_removed_source_url": "https://www.tiktok.com/transparency/en/community-guidelines-enforcement-2025-1",
        "videos_removed_pct_of_uploads": 0.009,
        "automated_removed": 184378987,
        "automated_removed_source_url": "https://www.tiktok.com/transparency/en/community-guidelines-enforcement-2025-1",
        "automation_rate": 0.874,
        "reinstated": 7525184,
        "reinstated_source_url": "https://www.tiktok.com/transparency/en/community-guidelines-enforcement-2025-1",
        "proactive_rate": 0.990,
        "proactive_rate_source_url": "https://www.tiktok.com/transparency/en/community-guidelines-enforcement-2025-1",
        "within_24h_rate": 0.943,
        "within_24h_rate_source_url": "https://www.tiktok.com/transparency/en/community-guidelines-enforcement-2025-1",
        "violation_breakdown": {
            "sensitive_mature_pct": 0.301,
            "misinformation_pct": 0.455,
            "edited_media_ai_pct": 0.138,
            "safety_civility_pct": 0.115,
            "privacy_security_pct": 0.156
        }
    })

    # ---------- Reddit ----------
    rd = pe / "platforms" / "reddit"
    w(rd / "content_policy.md", """# Reddit Content Policy

*Source: https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals*
*Source: https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf*

Reddit's content policy consists of rules that apply to all users and communities on the platform.

## Reddit Rules

### Rule 1: Remember the Human
Reddit prohibits **communities and users that incite violence or that promote hate based on
identity or vulnerability**.

This rule covers content that dehumanizes people, promotes discrimination, or calls for
violence against individuals or groups based on protected characteristics including race,
ethnicity, religion, gender, sexual orientation, disability, and nationality.

### Rule 2: Abide by Community Rules and Reddiquette
Users must **do not cheat or engage in content manipulation (including spamming, vote
manipulation, ban evasion, or subscriber fraud)**.

This rule addresses coordinated inauthentic behavior, vote brigading, and systematic
attempts to circumvent community moderation.

### Rule 3: Respect Privacy
Do not share others' personal information (doxxing) without their consent.

### Rule 4: Do Not Post Sexual Content Involving Minors (CSAM)
Zero tolerance for child sexual abuse material. Violators are immediately permanently banned
and reported to the National Center for Missing & Exploited Children (NCMEC).

### Rule 5: Do Not Knowingly Spread Misinformation
Users must not share **sharing manipulated content** or knowingly spread false information
that could deceive others or cause real-world harm.

### Rule 6: Ensure People Feel Safe
Do not threaten, harass, bully, or target people to make them feel unsafe.

### Rule 7: Keep it Legal
Do not post illegal content or use Reddit to facilitate illegal activities.

---

## Enforcement Tiers

Reddit uses a graduated enforcement model for policy violations:

| Tier | Action | Duration |
|---|---|---|
| Tier 1 | Warning | No suspension |
| Tier 2 | Suspension | **3 days** |
| Tier 3 | Suspension | **7 days** |
| Tier 4 | Permanent Ban | Permanent |

**Note**: Certain categories of violations (e.g. CSAM, terrorism) trigger immediate permanent
ban regardless of prior history, bypassing the warning/suspension tiers.

---

## Appeal Process

- Users may appeal enforcement actions within **6 months** of the notification.
- Appeals are processed in a timely, non-discriminatory, diligent, non-arbitrary manner.
- Notifications include the specific rule violated and instructions for filing an appeal.

*Source: https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals*
""")

    wj(rd / "enforcement_tiers.json", {
        "platform": "reddit",
        "schema_version": "1.0",
        "_source_url": "https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals",
        "tiers": [
            {
                "tier": 1,
                "action": "warning",
                "action_source_url": "https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals",
                "suspend_days": 0,
                "note": "First tier: warning with no suspension"
            },
            {
                "tier": 2,
                "action": "suspension",
                "action_source_url": "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf",
                "suspend_days": 3,
                "suspend_days_source_url": "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf",
                "note": "Second tier: 3-day suspension"
            },
            {
                "tier": 3,
                "action": "suspension",
                "action_source_url": "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf",
                "suspend_days": 7,
                "suspend_days_source_url": "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf",
                "note": "Third tier: 7-day suspension"
            },
            {
                "tier": 4,
                "action": "permanent_ban",
                "action_source_url": "https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals",
                "suspend_days": None,
                "note": "Fourth tier: permanent ban"
            }
        ],
        "immediate_permanent_ban_categories": ["CSAM", "terrorism", "child_exploitation"],
        "appeal": {
            "window_months": 6,
            "window_months_source_url": "https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals",
            "note": "Users may submit appeal within 6 months of notification"
        }
    })

    wj(rd / "h1_2025_metrics.json", {
        "platform": "reddit",
        "period": "H1_2025",
        "schema_version": "1.0",
        "_source_url": "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf",
        "report_name": "Reddit New York S895B/A6789B Terms of Service Report, January 2026",
        "enforcement": {
            "harassment": {
                "removed": 68550,
                "removed_source_url": "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf",
                "automated_pct": 0.586,
                "appeals_filed": 71114,
                "appeal_reversal_rate": 0.407,
                "appeal_reversal_rate_source_url": "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf",
                "account_level_appeal_reversal_rate": 0.250
            },
            "hateful_content": {
                "removed": 98798,
                "removed_source_url": "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf",
                "automated_pct": 0.772,
                "appeals_filed": 53021,
                "appeal_reversal_rate": 0.300,
                "appeal_reversal_rate_source_url": "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf",
                "account_level_appeal_reversal_rate": 0.276
            },
            "terrorism": {
                "removed": 980,
                "removed_source_url": "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf",
                "automated_pct": 0.810,
                "actionability_rate": 0.480,
                "appeals_filed": 364,
                "appeal_reversal_rate": 0.005,
                "appeal_reversal_rate_source_url": "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf",
                "account_level_appeal_reversal_rate": 0.005
            }
        },
        "rules": {
            "rule1_verbatim": "communities and users that incite violence or that promote hate based on identity or vulnerability",
            "rule1_source_url": "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf",
            "rule2_verbatim": "do not cheat or engage in content manipulation (including spamming, vote manipulation, ban evasion, or subscriber fraud)",
            "rule2_source_url": "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf",
            "rule5_verbatim": "sharing manipulated content",
            "rule5_source_url": "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf"
        }
    })


# --------------------------------------------------------------------------- #
# 2b. 扩展 Platform Policy 文档（增加体量至 100k+ tokens）
# --------------------------------------------------------------------------- #
def gen_extended_platform_docs() -> None:
    pe = WS / "policy_engine"

    # YouTube: 扩展社区准则（详细子政策，~15k tokens）
    yt_extra = pe / "platforms" / "youtube"
    w(yt_extra / "policy_details.md", _gen_yt_policy_details())

    # Meta: 扩展 community_standards（27类详细条款，~25k tokens）
    meta_extra = pe / "platforms" / "meta"
    w(meta_extra / "community_standards_detailed.md", _gen_meta_standards_detailed())

    # TikTok: 扩展指南（~12k tokens）
    tt_extra = pe / "platforms" / "tiktok"
    w(tt_extra / "guidelines_detailed.md", _gen_tiktok_guidelines_detailed())

    # Reddit: 扩展内容政策（Rule 1-7 完整，~10k tokens）
    rd_extra = pe / "platforms" / "reddit"
    w(rd_extra / "content_policy_detailed.md", _gen_reddit_policy_detailed())

    # Internal: 扩展 SOP（~8k tokens 额外附录）
    internal = pe / "internal"
    w(internal / "sop_addendum.md", _gen_sop_addendum())
    w(internal / "escalation_matrix.md", _gen_escalation_matrix())
    w(internal / "training_guide.md", _gen_training_guide())


def _gen_yt_policy_details() -> str:
    return """# YouTube Community Guidelines — Detailed Policy Reference

*Source: https://support.google.com/youtube/answer/9288567?hl=en*
*Source: https://support.google.com/youtube/answer/2802032?hl=en*
*Source: https://support.google.com/transparencyreport/answer/9209072?hl=en*

This document provides detailed reference information for YouTube's Community Guidelines
as implemented in the CreatorHub policy engine. All values are derived from official
YouTube documentation.

---

## Section 1: Spam and Deceptive Practices

### 1.1 Misleading Metadata Policy
YouTube prohibits content that uses misleading titles, thumbnails, descriptions, or tags
to deceive users into watching content. This includes clickbait, sensationalist headlines,
and thumbnails that don't reflect the video content.

**Enforcement Actions**:
- First offense: Content removed, warning issued
- Repeat offense: Strike applied

**Detection Methods**:
- Automated classifier (title/thumbnail correlation)
- User reports
- Manual review

### 1.2 Fake Engagement Policy
YouTube prohibits artificially inflating view counts, likes, comments, or subscribers
through bots, click farms, or coordinated inauthentic behavior. Purchased engagement
violates this policy.

**Enforcement Actions**:
- Content metrics reset (removal of fake engagement)
- Warning or strike depending on severity
- Channel termination for systematic abuse

### 1.3 Impersonation Policy
Creating a channel or profile that impersonates another creator, public figure, or
organization is prohibited. The impersonation policy distinguishes between:
- Parody/satire channels (may be allowed if clearly labeled)
- Genuine impersonation (prohibited)

**Enforcement**: Immediate removal of impersonating content; channel termination for
systematic impersonation.

### 1.4 Scams and Fraud Policy
Content that promotes or facilitates financial fraud, phishing, or scams is prohibited.
This includes cryptocurrency scams, investment fraud, and romance scams.

---

## Section 2: Sensitive Content

### 2.1 Child Safety Policy
YouTube maintains a zero-tolerance policy for content that sexualizes minors or exposes
them to inappropriate material. All CSAM-related content results in immediate channel
termination and referral to NCMEC.

**Always prohibited**:
- Content that sexually exploits minors
- Grooming behavior depicted or encouraged
- Content designed to attract minors for exploitation

**May be allowed (with restrictions)**:
- Educational content about child safety (age-gated)
- News reporting on child exploitation issues

### 2.2 Harassment and Cyberbullying Policy
YouTube prohibits content that maliciously targets individuals with the intent to harass,
bully, or cause distress. The policy distinguishes between:
- Public figures (higher threshold for criticism and satire)
- Private individuals (stronger protection)

**Prohibited harassment includes**:
- Sustained targeting of specific individuals
- Encouraging others to harass
- Revealing private information (doxxing)
- Non-consensual intimate imagery

### 2.3 Hate Speech Policy
YouTube prohibits content that promotes hatred, discrimination, or violence against
individuals or groups based on protected characteristics:
- Race, ethnicity, national origin
- Religion
- Gender identity and expression
- Sexual orientation
- Age
- Disability status

**Enforcement gradient**:
- Mild hate speech: Content removed, warning
- Severe hate speech: Strike issued
- Organized hate (e.g., promoting designated hate groups): Channel termination

### 2.4 Violent or Graphic Content Policy
YouTube restricts graphic violence based on context:
- Gratuitous violence (no redemptive value): Removed
- Graphic violence with educational/documentary context: May be age-gated
- War footage, news reporting: Context-dependent

### 2.5 Suicide and Self-Injury Policy
YouTube follows safe messaging guidelines for content about suicide and self-injury.
The policy prohibits:
- Content that encourages, glorifies, or provides methods for self-harm
- Pro-eating-disorder content

Allowed (with care):
- Mental health discussions following safe messaging guidelines
- Survivor stories
- Educational content about prevention

---

## Section 3: Violent or Dangerous Content

### 3.1 Extremism Policy
YouTube prohibits content created by or promoting terrorist organizations, violent extremist
groups, or ideologies that advocate violence. This includes:
- Recruitment material
- Propaganda
- Content glorifying terrorist attacks
- Content promoting genocide

**Enforcement**: Immediate removal; channel termination; referral to law enforcement
where legally required.

### 3.2 Dangerous Challenges and Pranks Policy
Content that promotes dangerous activities that could result in serious harm or death
is prohibited. This policy is particularly strict for content targeting minors.

### 3.3 Firearms Policy
YouTube restricts content related to firearms:
- Content promoting illegal sales or modifications: Prohibited
- Educational content about legal firearm use: Generally allowed
- Content promoting bump stocks or other illegal modifications: Prohibited

---

## Section 4: Regulated Goods

### 4.1 Illegal or Regulated Goods Policy
YouTube prohibits content that facilitates illegal sales of:
- Drugs and controlled substances
- Wildlife and exotic animals
- Counterfeit products
- Human body parts
- Tobacco and alcohol (to minors)

### 4.2 Gambling Content Policy
YouTube requires age-gating for gambling content and prohibits:
- Online gambling promotion without proper licensing disclosures
- Content promoting gambling to minors

---

## Section 5: Misinformation

### 5.1 Elections Misinformation Policy
YouTube prohibits content that:
- Discourages participation in elections
- Misrepresents how voting works
- Claims elections are fraudulent without substantiation
- Promotes voter intimidation

### 5.2 Medical Misinformation Policy
YouTube prohibits health misinformation that contradicts authoritative health guidance,
including COVID-19 misinformation, vaccine misinformation, and cancer cure misinformation.

**Enforcement**: Removals with educational overlays; channel strikes for systematic health misinformation.

### 5.3 General Misinformation Policy
YouTube prohibits demonstrably false claims intended to deceive users and that could
have real-world harm (e.g., conspiracy theories about natural disasters, climate denial
presented as established fact in misleading ways).

---

## Strike System — Detailed Mechanics

### Warning Period
The initial warning is issued for a first-time violation. Key characteristics:
- **No restrictions** on channel activities
- **Duration**: 90 days from issuance
- **Reset mechanism**: Completing the YouTube policy training course resets the warning timer
- **Nature**: Educational; not a strike
- **Does not count** toward the 3-strike threshold for channel removal

### Strike 1 — One Week Freeze
Upon receiving a first strike:
- **Upload** functionality disabled
- **Live stream** functionality disabled
- **Story creation** disabled
- **Post creation** (community posts) disabled
- **Thumbnail upload** disabled
- **Playlist creation** disabled
- **Duration**: 7 days (1 week) from strike issuance
- **Restoration**: All functionality automatically restored after 7 days
- **Strike expiry**: Strike disappears from account record 90 days after issuance

### Strike 2 — Two Week Freeze
Upon receiving a second strike:
- All same restrictions as Strike 1
- **Duration**: 14 days (2 weeks) from strike issuance
- **Critical requirement**: Strike 2 MUST occur within the same 90-day window as Strike 1
  to count toward the three-strike termination threshold

### Strike 3 — Channel Permanent Removal
Upon receiving a third strike:
- **Channel permanently removed**
- All videos, playlists, and channel data deleted
- **Critical requirement**: All 3 strikes must fall within the same rolling 90-day window
- Monetization and partnerships terminated
- Account may continue to exist but channel is deleted

---

## Appeal Procedures — Complete Reference

### Strike and Warning Appeals
- **Eligibility**: All strikes and warnings (not privacy-based removals)
- **Time limit**: **6 months** from the notification date
- **Limit**: Each violation appealable exactly **once**
- **Consequence of rejected appeal**: No additional penalties
- **Possible outcomes**:
  1. Strike/warning overturned → Removed from account
  2. Content age-restricted → Strike removed, content restricted
  3. Appeal upheld → Original decision stands

### Content Removal Appeals
- **Eligible content types**: Videos, posts, playlists, thumbnails, URLs
- **Time limit**: **1 year** (12 months) from removal date
- **Limit**: Each removal appealable exactly once

### Privacy-Based Removals
- **NOT eligible** for standard appeal process
- Handle through YouTube's separate privacy complaint mechanism

---

## Transparency Reporting — Key Metrics

YouTube publishes transparency reports quarterly covering:
- Videos removed by policy category
- Appeals filed and outcomes
- Proactive detection rates
- Human review volumes
- Government removal requests
- Copyright claim data

All enforcement actions by YouTube's human review team, which operates 24 hours per day,
7 days per week, across multiple time zones and languages.

---

*Last updated: 2025 Q4 | Source verification date: 2025-10-01*
"""


def _gen_meta_standards_detailed() -> str:
    return """# Meta Community Standards — Detailed Policy Reference

*Source: https://transparency.meta.com/policies/community-standards/*
*Source: https://transparency.meta.com/enforcement/taking-action/restricting-accounts/*
*Source: https://transparency.meta.com/reports/integrity-reports-q3-2025/*

This document provides comprehensive reference information for Meta's Community Standards
across Facebook and Instagram, as implemented in the CreatorHub policy engine.

---

## Overview: 27 Policy Categories

Meta's Community Standards are organized into the following 27 categories
(US English version, 2025):

1. Violence and Incitement
2. Dangerous Organizations and Individuals
3. Coordinating Harm and Promoting Crime
4. Restricted Goods and Services
5. Human Exploitation
6. Fraud and Deception
7. Suicide and Self-Injury
8. Child Sexual Abuse and Nudity (CSAM)
9. Sexual Exploitation of Adults
10. Bullying and Harassment
11. Privacy Violations and Image Privacy Rights
12. Violent and Graphic Content
13. Hate Speech
14. Adult Nudity and Sexual Activity
15. Sexual Solicitation
16. Spam
17. Cybersecurity
18. Inauthentic Behavior
19. False News
20. Memorialization
21. Intellectual Property
22. User Requests
23. Additional Protection for Minors
24. Regulated Goods (extended)
25. Account Integrity and Authentic Identity
26. Payments
27. Additional Community Standards

---

## Detailed Category Analysis

### Category 1: Violence and Incitement

Meta prohibits content that facilitates or encourages violence. The policy covers:

**Prohibited**:
- Statements of intent to commit violence against specific individuals or groups
- Calls for others to commit violence
- Glorification or celebration of violence
- Detailed plans or instructions for violence
- Content recruiting others for violent acts

**Allowed with educational/news context**:
- Reporting on violence
- Documentary footage
- Educational discussion of historical violence

**Enforcement**: Strike 1 (warning) for mild incitement; higher strikes for explicit calls to violence;
immediate account termination for systematic promotion of violence.

**Prevalence (Q4 2025)**: Violent and graphic content appeared in **0.15%–0.16%** of Facebook
content views (decreased from 0.19%–0.20% in Q3 2025 due to proactive detection improvements).

*Source: https://transparency.meta.com/reports/community-standards-enforcement/*

### Category 2: Dangerous Organizations and Individuals

Meta prohibits content from, celebrating, or promoting:
- Designated terrorist organizations
- Designated hate organizations
- Mass murderers and their manifestos
- Designated criminal organizations

**Terrorist organizations**: Organizations designated by governments or international bodies
as terrorist organizations are prohibited from using Meta platforms.

**Hate organizations**: Groups that attack people based on protected characteristics are
prohibited. Meta maintains an internal list of designated hate organizations.

**Enforcement**: Immediate account termination; referral to law enforcement where required.

### Category 3: Coordinating Harm and Promoting Crime

Covers:
- Content planning or facilitating offline harm
- Content promoting crimes against people (robbery, fraud)
- Content facilitating illegal access to services

**Enforcement**: Graduated strikes based on severity; up to account termination.

### Category 4: Restricted Goods and Services

Meta restricts the sale or promotion of:
- Firearms (illegal sales or illegal modifications)
- Drugs (illegal drugs; prescription drugs without valid prescription)
- Alcohol and tobacco (to minors; without age gating)
- Gambling services (without appropriate disclosures)
- Endangered wildlife
- Historical artifacts

### Category 5: Human Exploitation

Zero tolerance for content that facilitates or promotes:
- Human trafficking
- Forced labor
- Sexual servitude
- Commercial sexual exploitation of minors

**Enforcement**: Immediate account termination; mandatory law enforcement referral.

### Category 6: Fraud and Deception

Prohibits:
- Romance scams
- Financial fraud schemes
- Counterfeit currency promotion
- Fake documents
- Phishing attempts
- Impersonation for deceptive purposes

### Category 7: Suicide and Self-Injury

Meta follows safe messaging guidelines:

**Prohibited**:
- Content providing methods for self-harm
- Content glorifying or encouraging suicide
- Pro-eating-disorder content
- Weight-loss content targeting minors

**Allowed**:
- Awareness and prevention content
- Personal recovery stories
- Mental health support communities

**Special provisions**: If someone expresses intent to self-harm, Meta connects them to
mental health resources and crisis services.

### Category 8: Child Sexual Abuse and Nudity (CSAM)

**Zero tolerance policy**:
- Any sexual content depicting minors: Immediate account termination
- Grooming behavior: Account termination
- Content facilitating exploitation of minors: Account termination
- Mandatory reporting to NCMEC for all CSAM

**Q3 2025 Data**:
- Over 2 million NCMEC reports filed
- 486,000+ reports of inappropriate interactions with children
- 1.6 million+ reports of CSAM imagery

*Source: https://transparency.meta.com/reports/integrity-reports-q3-2025/*

### Category 9: Sexual Exploitation of Adults

Prohibits:
- Non-consensual sharing of intimate images (NCII)
- Sextortion
- Content sexualizing adults without consent
- Intimate images shared without consent

**Enforcement**: Immediate removal; account restrictions; higher strikes for systematic violations.

### Category 10: Bullying and Harassment

**Prohibited directed harassment**:
- Targeted attacks on specific individuals
- Coordinated harassment campaigns
- Unwanted contact or communication
- Non-consensual intimate imagery

**Public figures receive less protection** for public roles (politicians, celebrities in their
public capacity) but full protection for private matters.

**Private individuals receive full protection** from all forms of targeted harassment.

**Enforcement**: Warning for first offense; escalating restrictions; account termination for
systematic harassment.

**Q3 2025 data**: Increases in bullying and harassment enforcement observed.

### Category 11: Privacy Violations and Image Privacy Rights

Prohibits:
- Sharing personal contact information without consent
- Doxxing (revealing private information to facilitate harassment)
- Sharing private images without consent
- Content designed to locate individuals against their will

**Enforcement**: Immediate removal; account strikes; in severe cases, immediate account termination.

### Category 12: Violent and Graphic Content

Meta restricts graphic violence based on context and newsworthiness:

**Always prohibited**:
- Gratuitous violence for shock value
- Videos depicting violent deaths for entertainment
- Animal cruelty for entertainment

**May be allowed with context**:
- War footage with journalistic value
- Accident footage with safety messaging
- Medical procedures with educational context

**Q4 2025 Data**: Facebook violent/graphic content prevalence: **0.15%–0.16%** (decreased
from prior quarter due to proactive detection improvements).

*Source: https://transparency.meta.com/reports/community-standards-enforcement/*

### Category 13: Hate Speech

Meta prohibits content that:
- Dehumanizes people based on protected characteristics
- Calls for discrimination
- Portrays protected groups as subhuman
- Uses slurs to attack protected groups

**Protected characteristics**:
- Race and ethnicity
- National origin
- Religion
- Gender identity and expression
- Sexual orientation
- Age
- Disability
- Serious disease or disorder
- Caste
- Veteran status

**Enforcement Precision (Q3 2025)**:
- Facebook: **>90%** enforcement precision
- Instagram: **>87%** enforcement precision

*Source: https://transparency.meta.com/reports/integrity-reports-q3-2025/*

### Category 14: Adult Nudity and Sexual Activity

Meta distinguishes between acceptable and unacceptable sexual content:

**Prohibited**:
- Full nudity (unless in artistic, documentary, or medical context)
- Sexual acts
- Sexually explicit content (outside designated adult platforms)

**Allowed in context**:
- Breastfeeding images
- Post-mastectomy images
- Artistic nudity
- Medical/educational nudity

**Q3 2025 data**: Instagram adult nudity prevalence increased slightly in Q3 2025.

### Category 15: Sexual Solicitation

Prohibits:
- Solicitation of sexual services
- Content promoting prostitution or sex work on unregulated platforms
- Explicit sexual requests

### Category 16: Spam

Prohibits:
- Mass unsolicited commercial messages
- Fake accounts for engagement manipulation
- Artificial inflation of reach or engagement
- Clickbait for advertising revenue
- Malware distribution

### Category 17: Cybersecurity

Prohibits:
- Malware distribution
- Hacking tools and services
- Unauthorized account access
- Data theft facilitation

### Category 18: Inauthentic Behavior

Prohibits:
- Fake account networks
- Coordinated inauthentic behavior (CIB)
- Influence operations
- Impersonation of real individuals or organizations

**Meta actively removes CIB networks** and publishes monthly reports on dismantled operations.

### Category 19: False News

Meta doesn't remove most misinformation but does:
- Partner with third-party fact-checkers
- Reduce distribution of content rated false or misleading
- Apply informational labels
- Prohibit demonstrably false claims in political advertising

### Category 20: Memorialization

Meta provides memorial account status for deceased users' accounts:
- Memorial accounts are managed by a designated legacy contact
- Original content remains visible per privacy settings
- New content creation is prohibited on memorial accounts

### Category 21: Intellectual Property

Meta responds to copyright and trademark claims:
- DMCA process for copyright claims
- Trademark infringement reporting
- Repeat infringer policy (account termination after multiple valid DMCA notices)

### Categories 22-27

22. **User Requests**: Processes for suicide prevention resources and end-of-life requests
23. **Additional Protection for Minors**: Extra safeguards for content involving children under 18
24. **Regulated Goods (extended)**: Cannabis, pharmaceuticals, and emerging regulated categories
25. **Account Integrity and Authentic Identity**: Real-name policy and verification requirements
26. **Payments**: Meta Pay policies and financial transaction standards
27. **Additional Community Standards**: Catch-all for emerging policy areas

---

## Enforcement Metrics (Q3 2025)

### Enforcement Volume
- **<1%** of total content removed for policy violations
- **<0.1%** of content removed incorrectly (false positives)
- Approximately **1 in 10** removed pieces were errors
- But **<1 in 1000** overall content was an error

### Precision by Platform
| Platform | Enforcement Precision |
|---|---|
| Facebook | **>90%** |
| Instagram | **>87%** |

*Source: https://transparency.meta.com/reports/integrity-reports-q3-2025/*

### Q4 2025 Updates
- Violent/graphic content on Facebook decreased to **0.15%–0.16%** prevalence
- This is a decrease from **0.19%–0.20%** in Q3 2025
- Decrease attributed to improvements in proactive detection technology
- Adult nudity on Instagram increased slightly in Q4 2025
- False positives increased >100% briefly in Q4 due to a classification bug (since fixed)

*Source: https://transparency.meta.com/reports/community-standards-enforcement/*

---

## Strike System — Complete Reference

*Source: https://transparency.meta.com/enforcement/taking-action/restricting-accounts/*

### Standard Strike Ladder

| Strike | Action | Duration | Content Ban |
|--------|--------|----------|-------------|
| 1 | Warning | N/A | **0 days** — no restrictions |
| 2–6 | Feature restriction | Limited period | Group posting, page management, etc. |
| 7 | Content creation ban | **1 day** | All posting, commenting, page creation |
| 8 | Content creation ban | **3 days** | All content creation |
| 9 | Content creation ban | **7 days** | All content creation |
| 10+ | Content creation ban | **30 days** | All content creation |

### Critical Notes
- **Strike 7 = 1-day ban** (NOT 3 days — this is a common error)
- **Strike 8 = 3-day ban** (the first 3-day restriction)
- Feature restrictions (Strikes 2–6) are less severe than full content creation bans
- "Content creation" includes: posting, commenting, creating pages, reactions in some cases

### Severe Violations
For serious policy violations (CSAM, dangerous organizations):
- Additional longer restrictions from Strike 1
- May result in immediate permanent account termination
- No standard strike ladder applies

---

*Last updated: 2025 Q4 | Source verification date: 2025-10-01*
"""


def _gen_tiktok_guidelines_detailed() -> str:
    return """# TikTok Community Guidelines — Detailed Policy Reference

*Source: https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans*
*Source: https://www.tiktok.com/transparency/en/community-guidelines-enforcement-2025-1*

This document provides comprehensive reference information for TikTok's Community Guidelines
as implemented in the CreatorHub policy engine.

---

## Content Violation Categories

TikTok's Community Guidelines organize violations into the following major categories,
each tracked separately in enforcement transparency reports:

### 1. Safety & Civility (`safety_civility`)

**Coverage**: Content that promotes violence, harassment, or endangers physical safety.

**Prohibited content**:
- Direct threats of violence against individuals or groups
- Coordinated harassment campaigns
- Cyberbullying targeting specific individuals
- Content inciting self-harm or harm to others
- Content promoting dangerous activities without appropriate safety context
- Hate speech based on protected characteristics

**Enforcement data (Q1 2025)**:
- Accounted for **11.5%** of removed videos in Q1 2025
- High proactive detection rate (content removed before user reports)

### 2. Sensitive & Mature Content (`sensitive_mature`)

**Coverage**: Content inappropriate for general audiences.

**Prohibited or restricted**:
- Explicit sexual content
- Graphic violence
- Content depicting illegal acts
- Content using extreme profanity
- Content glorifying crime or criminal behavior
- Substance use glorification

**Enforcement data (Q1 2025)**:
- Accounted for **30.1%** of removed videos in Q1 2025 (largest single category)

### 3. Misinformation (`misinformation`)

**Coverage**: False or misleading content.

**Prohibited**:
- Health misinformation (medical claims contradicting scientific consensus)
- Election misinformation
- Climate change denial misrepresented as fact
- Synthetic media used to spread false information
- Conspiracy theories presented as fact

**Enforcement data (Q1 2025)**:
- Accounted for **45.5%** of removed videos in Q1 2025 (highest proportion)

### 4. Edited Media & AI-Generated Content (`edited_media_ai`)

**Coverage**: Manipulated or synthetic content used deceptively.

**Prohibited**:
- Deepfakes used to mislead or harass
- AI-generated content presenting false events as real
- Manipulated media misrepresenting public figures
- Synthetic voice or image used to spread misinformation

**Enforcement data (Q1 2025)**:
- Accounted for **13.8%** of removed videos in Q1 2025

### 5. Privacy & Security (`privacy_security`)

**Coverage**: Content violating personal privacy or security.

**Prohibited**:
- Doxxing (sharing personal information without consent)
- Non-consensual intimate imagery
- Content facilitating unauthorized account access
- Phishing content
- Identity theft facilitation

**Enforcement data (Q1 2025)**:
- Accounted for **15.6%** of removed videos in Q1 2025

Note: Percentages may exceed 100% as videos can be categorized under multiple violation types.

---

## Strike System — Detailed Mechanics

*Source: https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans*

### Strike Issuance and Expiry

TikTok uses a graduated strike system:

1. **Video Removal**: The violating video is removed. A notification is sent to the creator.
   This may or may not include a formal strike depending on severity.

2. **Reach Reduction / Shadowban**: For borderline content, TikTok may reduce the account's
   reach (limiting recommendations) without explicitly notifying the creator.

3. **Account Warning + Strike**: For clear policy violations, a formal strike is added to
   the creator's account. The creator receives an in-app notification.

4. **Permanent Account Ban**: After accumulating three strikes within the active window,
   the account is permanently banned.

### Strike Expiry

- **Strike lifetime**: Each strike expires from the account record **90 days** after issuance.
- An expired strike does not count toward the three-strike permanent ban threshold.
- Only strikes active within the rolling 90-day window are counted.

### Permanent Ban Threshold

- **Threshold**: **3 active strikes** within the 90-day rolling window
- Permanent ban = all content deleted, account cannot be recovered, creator banned from TikTok
- Note: Some violations trigger immediate permanent ban regardless of strike count
  (e.g., CSAM)

**Common confusion point**: The permanent ban threshold is **THREE strikes**, not two.
Historical internal documents claiming two strikes are incorrect.

### Enforcement Actions Summary

| Action | Trigger | Creator Notified |
|---|---|---|
| Video removal | Policy violation detected | Yes |
| Reach reduction | Borderline content | Not always |
| Account warning | Minor violation | Yes |
| Strike | Clear policy violation | Yes |
| Permanent ban | 3 strikes within 90 days | Yes |

---

## Q1 2025 Transparency Report — Full Data

*Source: https://www.tiktok.com/transparency/en/community-guidelines-enforcement-2025-1*

### Overall Enforcement Volume

| Metric | Value |
|---|---|
| Total videos removed | **211,000,000** |
| Removed as % of uploads | **~0.9%** |
| Automated detection | **184,378,987** (~87.4%) |
| Manual review removals | ~26,621,013 (~12.6%) |
| Reinstated after review | **7,525,184** |
| Proactive removal rate | **99.0%** |
| Removed within 24 hours | **94.3%** |

### Violation Breakdown (% of removed videos)

| Category | Percentage |
|---|---|
| Misinformation | 45.5% |
| Sensitive/Mature Content | 30.1% |
| Privacy & Security | 15.6% |
| Edited Media & AI-Generated | 13.8% |
| Safety & Civility | 11.5% |

*Note: Total exceeds 100% as multiple violations may apply per video.*

### Key Performance Indicators

- **Proactive rate (99.0%)**: 99 out of 100 removed videos were taken down BEFORE
  any user reported them — detected by TikTok's automated systems.

- **24-hour rate (94.3%)**: 94.3% of removed videos were removed within 24 hours of
  uploading, demonstrating rapid detection capabilities.

- **Reinstatement rate**: 7,525,184 videos reinstated after further review, representing
  approximately 3.6% of removed content — indicating a meaningful false-positive rate.

---

## Appeal Process

**Step 1**: Creator receives in-app notification of content removal with reason cited.

**Step 2**: Creator taps "Appeal" in the notification.

**Step 3**: TikTok's Safety Team reviews the appeal against Community Guidelines.

**Step 4**: Decision communicated to creator:
- **Appeal approved**: Content reinstated, penalty removed
- **Appeal denied**: Original decision stands

TikTok does not publicly specify an appeal window duration (unlike YouTube's 6 months or
Reddit's 6 months). The appeal option remains available for a reasonable period after
the enforcement action.

---

## CSAM Policy

TikTok maintains zero tolerance for child sexual abuse material:
- Immediate account permanent ban
- Content removed and flagged
- Mandatory reporting to NCMEC
- Law enforcement cooperation where legally required

---

*Last updated: 2025 Q4 | Source verification date: 2025-10-01*
"""


def _gen_reddit_policy_detailed() -> str:
    return """# Reddit Content Policy — Detailed Policy Reference

*Source: https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals*
*Source: https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf*

This document provides comprehensive reference information for Reddit's content policies
as implemented in the CreatorHub policy engine, including H1 2025 enforcement data.

---

## Reddit's Seven Rules — Complete Reference

Reddit's Sitewide Rules establish the baseline content standards for all communities.

### Rule 1: Remember the Human — No Hate Based on Identity or Vulnerability

**Verbatim from NY S895B/A6789B Report (January 2026)**:
Reddit prohibits **"communities and users that incite violence or that promote hate based
on identity or vulnerability."**

**Protected characteristics under Rule 1**:
- Actual or perceived race, color, or ethnicity
- National origin or immigration status
- Gender identity and expression
- Sexual orientation
- Age
- Disability status
- Religion or belief
- Socioeconomic status

**What Rule 1 prohibits**:
- Content dehumanizing individuals or groups based on protected characteristics
- Calls for violence against people based on identity
- Subreddits organized around hatred toward protected groups
- Content designed to make people feel unsafe based on their identity

**Enforcement (H1 2025)**:
- **68,550** harassment-related posts/comments removed by admins
- **71,114** appeals filed against harassment removals
- **40.7%** reversal rate for harassment content-level appeals
- **25.0%** reversal rate for harassment account-level appeals

*Source: https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf*

**Hateful content enforcement (H1 2025)**:
- **98,798** hateful content pieces removed by admins (77.2% automated)
- **53,021** appeals filed
- **30.0%** reversal rate for content-level appeals
- **27.6%** reversal rate for account-level appeals

*Source: https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf*

---

### Rule 2: Abide by Community Rules and Reddiquette — No Content Manipulation

**Verbatim from NY S895B/A6789B Report (January 2026)**:
Reddit requires users to **"do not cheat or engage in content manipulation (including
spamming, vote manipulation, ban evasion, or subscriber fraud)."**

**What Rule 2 prohibits**:
- **Spamming**: Bulk posting, repetitive self-promotion, automated posting
- **Vote manipulation**: Using bots, alt accounts, or coordination to inflate/deflate votes
- **Ban evasion**: Creating new accounts after being banned from subreddits or site-wide
- **Subscriber fraud**: Artificially inflating subscriber counts

**Enforcement considerations**:
- Vote manipulation is detected through pattern analysis
- Ban evasion triggers automatic detection systems
- Systematic content manipulation may result in immediate permanent ban

---

### Rule 3: Respect Privacy — No Personal Information Without Consent

Reddit prohibits sharing others' personal information (doxxing) without their consent.

**Prohibited**:
- Real names with identifying information for pseudonymous users
- Home or work addresses
- Phone numbers
- Email addresses (without consent)
- Financial information
- Personally identifying photos

**Exception**: Information already widely public may be discussed in context, but
compiling profiles designed for harassment is prohibited.

---

### Rule 4: Do Not Post Sexual Content Involving Minors (CSAM)

**Zero-tolerance policy**:
- Any sexual content involving minors: Immediate permanent ban
- Mandatory reporting to NCMEC
- No appeal available for CSAM violations

**Account-level actions**:
- Account permanently terminated
- IP-level bans may be applied
- Law enforcement referrals where applicable

---

### Rule 5: Do Not Knowingly Spread Misinformation

**Verbatim from NY S895B/A6789B Report (January 2026)**:
Users are prohibited from **"sharing manipulated content."**

**What Rule 5 prohibits**:
- Knowingly sharing false information designed to deceive
- Sharing manipulated images or videos misrepresented as authentic
- Coordinated misinformation campaigns
- Content designed to undermine trust in institutions without factual basis

**Rule 5 does NOT prohibit**:
- Satire (when clearly labeled)
- Opinion and commentary
- Good-faith sharing of information later found to be inaccurate

---

### Rule 6: Ensure People Feel Safe — No Threats or Harassment

Reddit prohibits content that makes people feel unsafe:
- Direct threats of violence
- Targeted harassment campaigns
- Content designed to cause fear
- Stalking behavior facilitated through Reddit

This rule works in conjunction with Rule 1 but covers general safety threats beyond
identity-based hate.

---

### Rule 7: Keep It Legal — No Illegal Content

Reddit prohibits:
- Content violating applicable laws
- Facilitating illegal transactions
- Copyright infringement
- Sharing CSAM (also Rule 4)
- Content supporting human trafficking

---

## Enforcement Tiers — Complete Reference

*Sources: Reddit Help Center + NY S895B/A6789B Report*

Reddit uses a four-tier graduated enforcement system:

### Tier 1: Warning

**Action**: Formal warning issued to the user
**Duration**: No suspension period
**Trigger**: Minor first-time violations of site rules
**Format**: In-app notification with rule citation and appeal instructions

### Tier 2: 3-Day Suspension

**Action**: Account suspended — cannot post, comment, vote, or message
**Duration**: **3 days** (72 hours) from suspension issuance
**Trigger**: More serious violations or repeated minor violations
**Format**: Email + in-app notification; appeal available

*Verbatim from official documentation: "a 3-day suspension"*

### Tier 3: 7-Day Suspension

**Action**: Account suspended — all participation disabled
**Duration**: **7 days** from suspension issuance
**Trigger**: Serious violations or pattern of policy violations
**Format**: Email + in-app notification; appeal available

*Verbatim from official documentation: "7-day suspension"*

### Tier 4: Permanent Ban

**Action**: Account permanently banned from Reddit
**Duration**: Permanent; no automatic expiry
**Trigger**: Most serious violations OR exhaustion of lower tiers
**Immediate triggers** (skip Tiers 1-3): CSAM, terrorism, organized crime coordination

**What permanent ban means**:
- Account cannot log in or participate
- All content may remain or be removed depending on violation
- User must not create new accounts (ban evasion = immediate new ban)
- Appeal available within 6-month window

---

## Appeal Process

*Source: https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals*

### Appeal Window
- **6 months** from the notification date
- Appeals filed after 6 months are not accepted

### Appeal Standards
Reddit commits to processing appeals in a:
- Timely manner
- Non-discriminatory manner
- Diligent manner
- Non-arbitrary manner

### Appeal Process Steps
1. User receives notification of enforcement action (removal reason + appeal link)
2. User submits appeal within 6-month window
3. Reddit reviews appeal against the applicable Community Guidelines
4. Decision communicated to user

### Appeal Outcomes (H1 2025 Data)

| Category | Appeals Filed | Reversal Rate (Content) | Reversal Rate (Account) |
|---|---|---|---|
| Harassment | 71,114 | **40.7%** | 25.0% |
| Hateful Content | 53,021 | **30.0%** | 27.6% |
| Terrorism | 364 | **0.5%** | 0.5% |

*Source: https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf*

### Notable Statistics

The **40.7% reversal rate** for harassment content appeals is notably high, suggesting
that:
- Automated detection has meaningful false-positive rates for harassment
- Human review frequently overturns automated decisions
- Context is important for harassment determinations

The **0.5% reversal rate** for terrorism appeals reflects the high confidence in
terrorism enforcement decisions.

---

## H1 2025 Enforcement Overview

Data from NY S895B/A6789B Report, January 2026:

### Admin Enforcement Summary (H1 2025)

| Violation Type | Removed | Automated % | Appeals | Reversal Rate |
|---|---|---|---|---|
| Harassment | **68,550** | 58.6% | 71,114 | 40.7% |
| Hateful Content | **98,798** | 77.2% | 53,021 | 30.0% |
| Terrorism | **980** | 81.0% | 364 | 0.5% |

### Key Observations

1. **Hateful content** has the highest removal volume (98,798), significantly more than
   harassment (68,550) despite lower appeal volumes.

2. **Terrorism** has the highest automation rate (81.0%) and lowest reversal rate (0.5%),
   indicating high-confidence automated detection.

3. **Harassment** has the highest reversal rate (40.7%), suggesting automated harassment
   detection is less reliable than terrorism detection.

4. **Actionability rate for terrorism**: 48.0% — meaning 48% of terrorism-related content
   flagged by automated systems was determined to be actionable upon human review.

---

## Reddit User Agreement Key Points

The Reddit User Agreement (effective June 28, 2025) establishes:
- Platform terms applicable to all users
- Community moderation rights reserved to subreddit moderators within site-wide rules
- Platform-level moderation authority for site-wide rule violations
- Arbitration clause for dispute resolution

---

*Last updated: 2025 Q4 | Source verification date: 2025-10-01*
"""


def _gen_sop_addendum() -> str:
    return """# CreatorHub Internal SOP Addendum — Cross-Platform Consistency Guidelines

## Purpose

This addendum to the main SOP (`sop_enforcement.md`) provides additional guidance for
maintaining consistency across the four-platform compliance engine, handling edge cases,
and escalation procedures.

---

## Cross-Platform Comparison Matrix (Operational Reference)

### Appeal Windows

| Platform | Strike/Warning Appeals | Content Removal Appeals |
|---|---|---|
| YouTube | **6 months** | **12 months** |
| Meta | Not publicly specified | Not publicly specified |
| TikTok | Not publicly specified | Not publicly specified |
| Reddit | **6 months** | **6 months** |

**Operational guideline**: For platforms with unspecified appeal windows, CreatorHub
engineers should treat appeals as time-sensitive and escalate within 30 days of
case creation to preserve optionality.

### Strike Expiry

| Platform | Strike Expiry | Consequence |
|---|---|---|
| YouTube | **90 days** from issuance | Strike removed from account |
| Meta | Not specified | N/A (cumulative system) |
| TikTok | **90 days** from issuance | Strike removed; doesn't count toward permanent ban |
| Reddit | Not specified (by tier) | Escalation possible with pattern |

### Permanent Ban Thresholds

| Platform | Threshold |
|---|---|
| YouTube | **3 strikes** within 90-day window |
| Meta | Varies; account termination for severe violations or prolonged misconduct |
| TikTok | **3 strikes** within 90-day window |
| Reddit | **Tier 4** action; immediate for CSAM/terrorism |

---

## Common Misquotations and Corrections

The following data points are frequently misquoted by automated systems and third-party
summaries. Engineers must verify against official platform files before using.

### 1. YouTube Appeal Window for Strikes
- **Misquoted value**: 3 months
- **Correct value**: **6 months**
- **Source**: https://support.google.com/youtube/answer/185111?hl=en
- **Impact**: Using 3 months would cause CreatorHub to reject valid appeals

### 2. Meta Strike 7 Duration
- **Misquoted value**: 3 days (from internal summaries, bot digests, PM emails)
- **Correct value**: **1 day**
- **Source**: https://transparency.meta.com/enforcement/taking-action/restricting-accounts/
- **Impact**: Critical for case resolution timelines

### 3. TikTok Permanent Ban Threshold
- **Misquoted value**: 2 strikes
- **Correct value**: **3 strikes**
- **Source**: https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans
- **Impact**: Premature permanent ban recommendation

### 4. Reddit Appeal Window
- **Misquoted value**: 3 months (from 2023 internal documents)
- **Correct value**: **6 months**
- **Source**: https://support.reddithelp.com/hc/en-us/articles/23511059871252
- **Impact**: Rejecting valid appeals prematurely

---

## Escalation Procedures

### Level 1 — Standard Case
**Criteria**: Single violation, clear policy match, standard enforcement tier
**Handling**: Automated system applies appropriate tier; case logged in appeal_tracker
**SLA**: Resolution within 5 business days

### Level 2 — Policy Ambiguity
**Criteria**: Violation falls in gray area; multiple policies potentially applicable;
context-dependent (e.g., satire vs. hate speech)
**Handling**: Human reviewer with policy expertise; cross-platform comparison if needed
**SLA**: Resolution within 10 business days

### Level 3 — Legal or Regulatory Involvement
**Criteria**: Government removal requests; law enforcement cooperation; DSA Article 34
risk categories; CSAM or terrorism content
**Handling**: Legal team (Maya Patel) + Compliance team; mandatory documentation
**SLA**: CSAM within 24 hours; other regulatory matters within 5 business days

### Level 4 — Crisis Protocol
**Criteria**: Mass violation events; coordinated inauthentic behavior campaigns;
emerging harmful content trends requiring immediate policy response
**Handling**: Executive team involvement; cross-platform rapid response
**SLA**: Initial response within 2 hours; resolution plan within 24 hours

---

## Data Quality Standards

### Numerical Citations
All numerical data in compliance reports must:
1. Include a `_source_url` field pointing to the authoritative source
2. Be verifiable against the source within 10% margin of error
3. Include the reporting period (Q1/Q2/Q3/Q4 or H1/H2 with year)
4. Note if data is from a preliminary or final report

### Version Control
- Platform policy files must be versioned (schema_version field)
- Deprecated values must be marked in `reports/archived/` not updated in place
- Policy changes must be noted in the `sop_enforcement.md` with effective date

---

*Last updated: 2025-10-01 | Author: PolicyOps AI | Review cycle: Quarterly*
"""


def _gen_escalation_matrix() -> str:
    lines = ["# Escalation Matrix — Platform Policy Engine\n\n"]
    lines.append("## Purpose\n\n")
    lines.append(
        "This matrix defines the escalation paths for different violation types "
        "across all four monitored platforms. It supplements the SOP and SOP Addendum.\n\n"
    )

    platforms = ["YouTube", "Meta", "TikTok", "Reddit"]
    violation_types = [
        ("CSAM", "Level 4 - Immediate", "24h", "Legal + Law Enforcement"),
        ("Terrorism/Extremism", "Level 4 - Immediate", "24h", "Legal + Law Enforcement"),
        ("Violence Incitement", "Level 3", "48h", "Legal Review"),
        ("Hate Speech", "Level 2", "72h", "Policy Expert"),
        ("Harassment", "Level 1-2", "5 days", "Standard Review"),
        ("Misinformation", "Level 1", "5 days", "Standard Review"),
        ("Spam/Manipulation", "Level 1", "5 days", "Automated"),
        ("Privacy Violation", "Level 2", "48h", "Privacy Team"),
        ("Copyright", "Level 1", "10 days", "Legal"),
        ("Fraud/Scam", "Level 2", "48h", "Trust & Safety"),
    ]

    for plat in platforms:
        lines.append(f"## {plat}\n\n")
        lines.append("| Violation Type | Level | SLA | Handler |\n")
        lines.append("|---|---|---|---|\n")
        for vtype, level, sla, handler in violation_types:
            lines.append(f"| {vtype} | {level} | {sla} | {handler} |\n")
        lines.append("\n")

    lines.append("## Contact Directory\n\n")
    lines.append("| Role | Contact | Available |\n")
    lines.append("|---|---|---|\n")
    lines.append("| Head of Compliance | Lin Wei | Business hours |\n")
    lines.append("| Policy Analyst | Alex Torres | Business hours |\n")
    lines.append("| Legal Counsel | Maya Patel | Business hours + emergency |\n")
    lines.append("| Moderation Ops Lead | Sam Rivera | 24/7 on-call |\n")
    lines.append("| Product Manager | Jordan Kim | Business hours |\n")

    return "".join(lines)


def _gen_training_guide() -> str:
    sections = []
    sections.append("# PolicyOps AI Training Guide — Platform Policy Reference\n\n")
    sections.append("## Introduction\n\n")
    sections.append(
        "This training guide provides detailed worked examples for common policy "
        "scenarios across YouTube, Meta, TikTok, and Reddit. Engineers should review "
        "these examples when uncertain about appropriate enforcement tier selection.\n\n"
    )

    platforms_data = {
        "YouTube": [
            ("Spam Example 1", "Creator uses clickbait thumbnail misrepresenting video content",
             "Warning (first offense)", "Misleading Metadata Policy"),
            ("Spam Example 2", "Creator purchases 50,000 fake views using bot service",
             "Strike 1 (7-day freeze)", "Fake Engagement Policy"),
            ("Hate Speech Example 1", "Video contains mild ethnic slur in context not targeting anyone",
             "Warning; age restriction", "Hate Speech Policy"),
            ("Hate Speech Example 2", "Channel dedicated to promoting ethnic hatred",
             "Strike 1 or channel removal depending on severity", "Hate Speech Policy"),
            ("CSAM Example", "Any content sexualizing minors",
             "Immediate channel termination + NCMEC referral", "Child Safety Policy"),
            ("Misinformation Example 1", "Health claim contradicting WHO guidance on vaccine safety",
             "Warning; informational panel added", "Medical Misinformation Policy"),
            ("Strike Escalation Example", "Creator receives Strike 1, then 10 days later Strike 2",
             "Both within 90-day window; next violation triggers Strike 3 (channel removal)",
             "Three-Strike Policy"),
            ("Appeal Example", "Creator appeals Strike 1 within 6 months",
             "YouTube reviews; possible outcomes: reinstated/age-restricted/upheld",
             "Appeal Procedures"),
        ],
        "Meta": [
            ("Strike 1 Example", "User posts mildly inflammatory content about political group",
             "Warning (Strike 1) — no restrictions", "Violence and Incitement (mild)"),
            ("Strike 7 Example", "User on seventh violation; posts harassment content",
             "1-day content creation ban", "Bullying and Harassment"),
            ("Strike 8 Example", "User on eighth violation",
             "3-day content creation ban", "Repeat violator"),
            ("Strike 10+ Example", "User on eleventh violation",
             "30-day content creation ban", "Repeat violator"),
            ("CSAM Example", "Any content involving minors sexually",
             "Immediate account termination + NCMEC referral", "CSAM Policy"),
            ("Hate Speech Q3 2025", "Content removed for hate speech",
             "Facebook precision >90%; Instagram >87%",
             "Q3 2025 Enforcement Data"),
        ],
        "TikTok": [
            ("Strike 1 Example", "Video contains mild violence or graphic content",
             "Video removed; Strike 1 added (expires 90 days from issuance)",
             "Sensitive/Mature Content"),
            ("Strike 3 Example", "Creator accumulates 3 strikes within 90-day window",
             "Permanent account ban", "Three-Strike Policy"),
            ("Permanent Ban Without Strikes", "Creator posts CSAM",
             "Immediate permanent ban regardless of prior strikes",
             "CSAM Policy"),
            ("Appeal Example", "Creator appeals video removal",
             "Creator taps Appeal in notification; safety team reviews; "
             "successful appeal reinstates content and removes penalty",
             "Appeal Process"),
            ("Q1 2025 Scale", "211 million videos removed in one quarter",
             "87.4% by automated systems; 99.0% before user reports",
             "Q1 2025 Transparency Report"),
        ],
        "Reddit": [
            ("Tier 1 Example", "User posts mildly rule-violating comment (first offense)",
             "Warning (Tier 1) — no suspension", "Site Rules — minor violation"),
            ("Tier 2 Example", "User engages in vote manipulation",
             "3-day suspension", "Rule 2 — Content Manipulation"),
            ("Tier 3 Example", "User repeatedly harasses specific individual",
             "7-day suspension", "Rule 1/Rule 6 — Harassment"),
            ("Tier 4 Example", "User posts CSAM",
             "Immediate permanent ban + NCMEC referral", "Rule 4 — CSAM"),
            ("Appeal within Window", "User appeals 3-day suspension within 6 months",
             "Reddit reviews appeal; H1 2025 harassment reversal rate: 40.7%",
             "Appeal Process"),
            ("Appeal Out of Window", "User attempts appeal after 6 months",
             "Appeal rejected — outside the 6-month window",
             "Appeal Process"),
        ],
    }

    for plat, examples in platforms_data.items():
        sections.append(f"## {plat} Scenarios\n\n")
        for title, scenario, action, policy in examples:
            sections.append(f"### {title}\n\n")
            sections.append(f"**Scenario**: {scenario}\n\n")
            sections.append(f"**Enforcement Action**: {action}\n\n")
            sections.append(f"**Applicable Policy**: {policy}\n\n")
        sections.append("\n")

    sections.append("## Common Mistakes Checklist\n\n")
    mistakes = [
        ("YouTube appeal window", "3 months", "6 months",
         "https://support.google.com/youtube/answer/185111?hl=en"),
        ("Meta Strike 7 duration", "3 days", "1 day",
         "https://transparency.meta.com/enforcement/taking-action/restricting-accounts/"),
        ("TikTok permanent ban threshold", "2 strikes", "3 strikes",
         "https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans"),
        ("Reddit appeal window", "3 months", "6 months",
         "https://support.reddithelp.com/hc/en-us/articles/23511059871252"),
        ("Reddit Tier 2 suspension", "7 days", "3 days",
         "https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf"),
    ]
    sections.append("| Field | Wrong Value | Correct Value | Source |\n")
    sections.append("|---|---|---|---|\n")
    for field, wrong, correct, source in mistakes:
        sections.append(f"| {field} | {wrong} | {correct} | [link]({source}) |\n")

    return "".join(sections)


# --------------------------------------------------------------------------- #
# 3. Internal 参考文件（合成大体量素材）
# --------------------------------------------------------------------------- #
def gen_internal_docs() -> None:
    pe = WS / "policy_engine"
    internal = pe / "internal"

    # policy_matrix.csv — 200行 × 20列 四平台政策横向对比
    rng = random.Random(2025)
    categories = [
        ("Violence & Incitement", "Violent or Dangerous Content", "Safety & Civility",
         "Violent Content", "Violent Criminals"),
        ("Hate Speech", "Sensitive Content", "Safety & Civility", "Hateful Content", "Rule 1"),
        ("Spam & Deceptive", "Spam & Deceptive Practices", "Inauthentic Behavior",
         "Spam", "Rule 2"),
        ("Misinformation", "Misinformation", "False News", "Misinformation",
         "Rule 5"),
        ("CSAM", "Child Safety", "CSAM", "CSAM", "Rule 4"),
        ("Adult Sexual Content", "Sensitive Content", "Adult Sexual Exploitation",
         "Adult Nudity", "Explicit Content"),
        ("Harassment", "Sensitive Content", "Bullying and Harassment",
         "Safety & Civility", "Rule 6"),
        ("Privacy Violations", "Sensitive Content", "Privacy Violations",
         "Privacy & Security", "Rule 3"),
        ("Terrorism", "Violent or Dangerous Content", "Dangerous Organizations",
         "Safety & Civility", "Rule 4"),
        ("Cybersecurity", "Regulated Goods", "Cybersecurity",
         "Privacy & Security", "Rule 7"),
    ] * 40  # repeat to get 400 rows

    platforms = ["YouTube", "Meta", "TikTok", "Reddit"]
    actions_map = {
        "YouTube": ["warning", "strike_1_7d", "strike_2_14d", "channel_removal"],
        "Meta": ["warning", "feature_restrict", "content_ban_1d", "content_ban_30d"],
        "TikTok": ["warning", "shadowban", "strike_90d", "perm_ban"],
        "Reddit": ["warning", "suspend_3d", "suspend_7d", "perm_ban"],
    }
    appeal_windows = {
        "YouTube": "6 months (strikes) / 12 months (content)",
        "Meta": "Not publicly specified (varies)",
        "TikTok": "Not publicly specified",
        "Reddit": "6 months",
    }

    buf = io.StringIO()
    writer = csv.writer(buf)
    header = ["row_id", "category_name", "yt_category", "meta_category", "tt_category",
              "reddit_category", "severity", "yt_first_action", "meta_first_action",
              "tt_first_action", "reddit_first_action", "yt_repeat_action",
              "meta_repeat_action", "tt_repeat_action", "reddit_repeat_action",
              "yt_appeal_window", "meta_appeal_window", "tt_appeal_window",
              "reddit_appeal_window", "notes"]
    writer.writerow(header)
    for i, cats in enumerate(categories[:400], 1):
        cn, yt_cat, meta_cat, tt_cat, rd_cat = cats
        sev = rng.choice(["low", "medium", "high", "critical"])
        row = [
            f"PM-{i:04d}", cn, yt_cat, meta_cat, tt_cat, rd_cat, sev,
            rng.choice(actions_map["YouTube"]),
            rng.choice(actions_map["Meta"]),
            rng.choice(actions_map["TikTok"]),
            rng.choice(actions_map["Reddit"]),
            rng.choice(actions_map["YouTube"][1:]),
            rng.choice(actions_map["Meta"][1:]),
            rng.choice(actions_map["TikTok"][1:]),
            rng.choice(actions_map["Reddit"][1:]),
            appeal_windows["YouTube"],
            appeal_windows["Meta"],
            appeal_windows["TikTok"],
            appeal_windows["Reddit"],
            f"Cross-platform comparison row {i}"
        ]
        writer.writerow(row)
    w(internal / "policy_matrix.csv", buf.getvalue())

    # violation_log_2025.csv — 500条模拟违规案例
    buf2 = io.StringIO()
    writer2 = csv.writer(buf2)
    viol_header = ["case_id", "platform", "violation_type", "severity", "date", "action_taken",
                   "appeal_status", "appeal_deadline", "status", "reviewer", "notes"]
    writer2.writerow(viol_header)
    violation_types = {
        "youtube": ["spam", "misinformation", "hate_speech", "violent_content", "child_safety"],
        "meta": ["spam", "hate_speech", "csam", "violent_graphic", "adult_nudity",
                 "bullying_harassment", "dangerous_orgs"],
        "tiktok": ["safety_civility", "sensitive_mature", "misinformation",
                   "edited_media_ai", "privacy_security"],
        "reddit": ["rule1_hate", "rule2_manipulation", "rule4_csam", "rule5_misinfo", "rule6_safety"],
    }
    plat_actions = {
        "youtube": ["warning", "strike_1", "strike_2", "channel_removal"],
        "meta": ["warning", "feature_restrict", "content_ban_1d", "content_ban_3d",
                 "content_ban_7d", "content_ban_30d"],
        "tiktok": ["warning", "video_removal", "shadowban", "permanent_ban"],
        "reddit": ["warning", "suspend_3d", "suspend_7d", "permanent_ban"],
    }
    statuses = ["closed", "under_review", "approved", "pending"]
    rng2 = random.Random(42)
    for i in range(1, 1001):
        plat = rng2.choice(["youtube", "meta", "tiktok", "reddit"])
        vtype = rng2.choice(violation_types[plat])
        sev = rng2.choice(["low", "medium", "high"])
        month = rng2.randint(1, 6)
        day = rng2.randint(1, 28)
        date = f"2025-{month:02d}-{day:02d}"
        action = rng2.choice(plat_actions[plat])
        appeal_status = rng2.choice(["not_appealed", "appealed_pending", "appealed_denied",
                                      "appealed_approved"])
        if month <= 3:
            deadline_m = month + 6
            deadline = f"2025-{deadline_m:02d}-{day:02d}"
        else:
            deadline = f"2025-{min(month+6, 12):02d}-{day:02d}"
        status = rng2.choice(statuses)
        reviewer = rng2.choice(["human_review", "automated", "escalated"])
        writer2.writerow([
            f"VIOL-{i:05d}", plat, vtype, sev, date, action, appeal_status,
            deadline, status, reviewer, f"Case {i} ({plat})"
        ])
    w(internal / "violation_log_2025.csv", buf2.getvalue())

    # appeal_tracker.json — 当前申诉状态
    rng3 = random.Random(99)
    appeal_cases = {}
    old_case_ids = [f"OLD-{i:04d}" for i in range(40, 60)]
    for i, cid in enumerate(old_case_ids):
        plat = rng3.choice(["youtube", "meta", "tiktok", "reddit"])
        st = "approved" if i < 10 else ("denied" if i < 15 else "pending")
        if cid in ["OLD-0050", "OLD-0051", "OLD-0052"]:
            st = "approved"  # update_1 will change these to under_review
        appeal_cases[cid] = {
            "platform": plat,
            "status": st,
            "filed_date": f"2025-0{rng3.randint(1,9)}-{rng3.randint(10,28):02d}",
            "violation_type": rng3.choice(["spam", "hate_speech", "misinformation"]),
            "notes": f"Legacy appeal case {cid}"
        }
    wj(internal / "appeal_tracker.json", {
        "schema_version": "1.0",
        "last_updated": "2025-09-15",
        "total_cases": len(appeal_cases),
        "cases": appeal_cases
    })

    # sop_enforcement.md — 内部执行 SOP
    w(internal / "sop_enforcement.md", """# CreatorHub 内部内容审核 SOP（Standard Operating Procedure）

## 总则

本 SOP 规定了 CreatorHub 内容审核合规引擎针对 YouTube、Meta、TikTok、Reddit 四大平台
政策的执行标准、申诉处理流程及 SLA 承诺。所有数值引用须以平台官方文件为准。

## YouTube 执行流程

### 违规阶梯

1. **警告（Warning）**：首次轻微违规，无权限限制，可完成政策培训课程重置倒计时。
   警告在 90 天后自动过期。
2. **一级违规（Strike 1）**：上传、发帖、直播、缩略图及播放列表创建功能暂停 **7 天**。
3. **二级违规（Strike 2）**：所有发布功能暂停 **14 天**（须在同一 90 天窗口内累积）。
4. **三级违规（Strike 3）**：频道**永久删除**（须在同一 90 天窗口内累积三次违规）。

### 申诉 SLA

- 违规/警告申诉窗口：**6 个月**
- 内容移除申诉窗口：**12 个月**（视频/帖子/播放列表/缩略图/URL）
- 每次违规仅可申诉一次

## Meta 执行流程

### 违规阶梯

| 违规次数 | 限制措施 |
|---------|---------|
| 第 1 次 | 仅警告，无额外限制 |
| 第 2–6 次 | 特定功能受限（如群组发帖）持续一段时间 |
| 第 7 次 | 禁止内容创建 **1 天** |
| 第 8 次 | 禁止内容创建 **3 天** |
| 第 9 次 | 禁止内容创建 **7 天** |
| 第 10+ 次 | 禁止内容创建 **30 天** |

注意：**第 7 次违规限制为 1 天**（非 3 天）。第 8 次才是 3 天。

### 申诉 SLA

Meta 申诉流程由平台内部处理，时限未公开具体数字，但平台承诺在合理时间内回应。

## TikTok 执行流程

### 违规阶梯

TikTok 采用三步式违规阶梯制度：
1. 单次视频移除（内容层面）
2. 账户警告 + 违规记录（有效期 **90 天**）
3. 第三次违规 → **永久封禁**

**重要**：违规记录 90 天后从账户记录中消失。永久封禁需要在有效期内累积 **3 次**违规，
而非 2 次。

### 申诉 SLA

TikTok 申诉通过通知栏提交，安全团队人工审核。

## Reddit 执行流程

### 执行阶梯

| 阶段 | 动作 |
|------|------|
| Tier 1 | 警告（无暂停） |
| Tier 2 | **3 天暂停** |
| Tier 3 | **7 天暂停** |
| Tier 4 | 永久封禁 |

特殊类别（如 CSAM、恐怖主义）直接触发永久封禁，跳过前三阶段。

### 申诉 SLA

申诉窗口：**6 个月**（自通知之日起计算）

## 来源参考

- YouTube 违规阶梯: https://support.google.com/youtube/answer/2802032?hl=en
- YouTube 申诉流程: https://support.google.com/youtube/answer/185111?hl=en
- Meta 账户限制: https://transparency.meta.com/enforcement/taking-action/restricting-accounts/
- TikTok 违规与封禁: https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans
- Reddit 执行与申诉: https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals
""")

    # platform_sla.json — 各平台 SLA 承诺对照
    wj(internal / "platform_sla.json", {
        "schema_version": "1.0",
        "_source_note": "SLA values derived from official platform documentation",
        "youtube": {
            "appeal_window_strike_months": 6,
            "appeal_window_strike_months_source_url": "https://support.google.com/youtube/answer/185111?hl=en",
            "appeal_window_content_months": 12,
            "appeal_window_content_months_source_url": "https://support.google.com/youtube/answer/185111?hl=en",
            "strike_window_days": 90,
            "strike1_freeze_days": 7,
            "strike2_freeze_days": 14,
            "warning_expiry_days": 90
        },
        "meta": {
            "appeal_window_months": None,
            "appeal_window_note": "Not publicly specified; Meta handles appeals internally",
            "strike7_ban_days": 1,
            "strike7_ban_days_source_url": "https://transparency.meta.com/enforcement/taking-action/restricting-accounts/"
        },
        "tiktok": {
            "strike_expiry_days": 90,
            "strike_expiry_days_source_url": "https://support.tiktok.com/en/safety-hc/account-and-user-safety/content-violations-and-bans",
            "permanent_ban_strikes": 3,
            "appeal_window_months": None,
            "appeal_window_note": "Not publicly specified"
        },
        "reddit": {
            "appeal_window_months": 6,
            "appeal_window_months_source_url": "https://support.reddithelp.com/hc/en-us/articles/23511059871252-Content-Moderation-Enforcement-and-Appeals",
            "tier2_suspend_days": 3,
            "tier3_suspend_days": 7
        }
    })


# --------------------------------------------------------------------------- #
# 4. 诱饵 / 红鲱鱼 文件（V5/V6）
# --------------------------------------------------------------------------- #
def gen_decoy_files() -> None:
    pe = WS / "policy_engine"

    # V5 诱饵：Slack bot 摘要声称 YT 申诉窗口 3 个月（官方 6 个月）
    # 这个内容会在 session 中出现，workspace 也留一份 bot 摘要文件
    w(pe / "internal" / "BOT_SUMMARY_POLICY_UPDATES.md", """# BOT SUMMARY: Policy Updates Digest (Auto-generated)

> ⚠️ This is an automated summary generated by PolicyBot v2.1. Convenience reference only.
> DO NOT use for authoritative citations — verify against official platform files.

## YouTube Appeal Windows (Bot Summary — MAY BE INACCURATE)
- Strike/Warning appeal window: **~3 months**
- Content removal appeal window: ~1 year

## Meta Strike 7 (Bot Summary)
- Strike 7: content ban for **3 days**
- Strike 8: content ban for **7 days**

## TikTok Permanent Ban Threshold
- Permanent ban triggers after **3 strikes** in 90-day window

## Reddit Appeal Window
- Estimated: ~6 months (per community help documentation)

---
*PolicyBot processes policy documents using heuristic extraction. Known inaccuracies:*
*YT appeal window may be understated; Meta strike durations frequently misquoted.*
*Always verify numerical values against official_platform_files/ documents.*
""")

    # V6 红鲱鱼：旧版合规报告（archived）
    reports_archived = pe / "reports" / "archived"
    w(reports_archived / "compliance_report_v0.md", """# CreatorHub Compliance Report v0 (ARCHIVED — DO NOT CITE)

**Status**: ARCHIVED | **Last Updated**: 2024-03-01 | **Superseded by**: compliance_report_draft.md

> ⚠️ This document is ARCHIVED and contains outdated data from 2024 platform policies.
> Several values have been superseded by updated platform documentation.
> DO NOT use this document as a reference for current compliance work.

---

## Platform Strike Durations (2024 Data — OUTDATED)

### YouTube
- Warning expiry: 90 days ✓ (unchanged)
- Strike 1 freeze: 7 days ✓ (unchanged)
- **Appeal window for strikes: 3 months** ← OUTDATED (current: 6 months)

### Meta
- Strike 7 content ban: **3 days** ← OUTDATED (current: 1 day)
- Strike 8 content ban: 3 days (was also 3; now: 3 ✓)
- Strike 9: 7 days ✓ (unchanged)
- Strike 10+: 30 days ✓ (unchanged)

### TikTok
- Strike expiry: 90 days ✓ (unchanged)
- Permanent ban threshold: 3 strikes ✓ (unchanged)

### Reddit
- Tier 2 suspension: 3 days ✓ (unchanged)
- Tier 3 suspension: 7 days ✓ (unchanged)

---

*This archive is retained for historical audit purposes only.*
*Deprecation recorded: META_STRIKE7 (was 3d → now 1d); YT_APPEAL_STRIKE (was 3mo → now 6mo).*
""")

    # draft_compliance_report.md
    w(pe / "reports" / "draft_compliance_report.md", """# CreatorHub Compliance Report — Draft

*Version: DRAFT | Status: In Progress | Author: PolicyOps AI*

This document serves as the working draft for the quarterly compliance report.
It will be finalized in Q16 with sha256 sign-off.

## Summary

This report covers the four major platforms (YouTube, Meta, TikTok, Reddit) and
their content moderation policies as relevant to CreatorHub's compliance engine.

[To be completed by Agent based on policy analysis tasks Q1-Q15]
""")


# --------------------------------------------------------------------------- #
# 5. Sessions（主 + 4 history）
# --------------------------------------------------------------------------- #
def gen_sessions() -> dict:
    pe_cwd = f"/workspace/{TID}/policy_engine"
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("compliance_slack", TID)
    s_feishu = gen_session_id("legal_feishu", TID)
    s_email = gen_session_id("pm_jordan_email", TID)
    s_discord = gen_session_id("modops_discord", TID)

    # ---- 主 session ----
    sb = SessionBuilder(main_id, pe_cwd, "2025-10-01T09:00:00", is_main=True)
    sb.add_user(
        "You are PolicyOps AI, the compliance engineering assistant for CreatorHub's content "
        "moderation team. We are building a unified policy engine that aligns with YouTube, Meta, "
        "TikTok, and Reddit community guidelines.\n\n"
        "The authoritative policy definitions live in `policy_engine/platforms/{platform}/` "
        "files. Auto-generated bot summaries (prefixed BOT_SUMMARY_) and archived reports "
        "under `reports/archived/` are NOT authoritative — always verify against the platform "
        "files.\n\n"
        "House preferences (apply throughout, even when not restated):\n"
        "- P1: All JSON files use 2-space indentation and snake_case key names (no camelCase).\n"
        "- P2: All numeric fields carry a companion `_source_url` field documenting the "
        "authoritative URL for that value.\n"
        "- P3: Time-limit values are expressed in months as the primary unit, with 1 decimal "
        "place (e.g. `6.0` months for 6 months, `0.5` months for 14 days).\n"
        "- P4: Markdown documents use `[^N]` footnote references and include a `## 参考来源` "
        "section at the document end.\n"
        "- P5: Files under `reports/` follow naming convention `{type}_{yyyy-mm}.json`; "
        "when no specific month applies, use `latest` (e.g. `violation_stats_latest.json`).\n\n"
        "History sessions available (Slack #compliance, Feishu DM, Email, Discord #mod-ops). "
        "Start by running `exec ls -R` and reading SOUL.md, then await each task."
    )
    sb.add_assistant(
        "Understood. I have reviewed AGENTS.md, SOUL.md, and USER.md. Working framework:\n"
        "1. Treat `platforms/{platform}/` JSON and MD files as authoritative; ignore BOT_SUMMARY "
        "numbers and archived reports under `reports/archived/`.\n"
        "2. Use verbatim policy category names; tag all JSON with snake_case keys (P1); add "
        "`_source_url` companions for numeric fields (P2).\n"
        "3. Express time limits in months with 1 decimal (P3); use footnote citations in Markdown (P4).\n"
        "4. Name report files as `{type}_{yyyy-mm}.json` or `{type}_latest.json` (P5).\n"
        "Ready for the first task."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # ---- Slack #compliance — 包含 V5 蜜罐（bot 摘要 YT 申诉窗口 3 个月）和 TikTok 永封次数讨论 ----
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, pe_cwd, "2025-09-28T10:00:00",
        [
            ("[Slack #compliance alex Mon Sep 28 10:00 PST 2025] Hey team, kicking off our "
             "policy engine update. I've run the PolicyBot digest — see the BOT_SUMMARY file. "
             "Quick note from the bot: YouTube's appeal window for strikes is about 3 months. "
             "Can someone verify that before we lock in the SLA table?",
             "Noted. The BOT_SUMMARY digest suggests 3 months for YouTube strike appeals — "
             "but I'll verify against the official YouTube Help page "
             "(https://support.google.com/youtube/answer/185111) before using this in any "
             "deliverable. Bot summaries are explicitly non-authoritative per our SOUL.md."),
            ("[Slack #compliance alex Mon Sep 28 10:15 PST 2025] Also, I'm getting confused "
             "about TikTok's permanent ban threshold. Is it 2 strikes or 3? Our old SOP says 2.",
             "The official TikTok Support page at https://support.tiktok.com/en/safety-hc/"
             "account-and-user-safety/content-violations-and-bans clearly states a "
             "three-strike policy leading to permanent ban. The old SOP value of 2 is incorrect. "
             "I'll use 3 strikes as the authoritative value."),
            ("[Slack #compliance alex Tue Sep 29 09:00 PST 2025] PolicyBot update: it's also "
             "claiming Meta Strike 7 = 3-day ban. That matches what Jordan said in email. "
             "Should we go with that for our matrix?",
             "I cannot confirm that. The official Meta Transparency page "
             "(https://transparency.meta.com/enforcement/taking-action/restricting-accounts/) "
             "states Strike 7 = 1-day content creation ban. Strike 8 is the 3-day ban. "
             "The bot summary and Jordan's email appear to have the days wrong. "
             "I will use the official value: Strike 7 = 1 day."),
        ]
    )

    # ---- Feishu DM — 法律顾问提供 Reddit Rule 原文建议，但含一处过时引用（V1 辅线）----
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, pe_cwd, "2025-09-30T14:00:00",
        [
            ("[Feishu Maya Wed Sep 30 14:00 PST 2025] For the Reddit section, I recommend "
             "quoting Rule 1 verbatim: 'communities and users that incite violence or that "
             "promote hate based on identity or vulnerability'. That's the exact language from "
             "the NY transparency report (S895B/A6789B, January 2026).",
             "Confirmed. I'll use that exact verbatim text for Reddit Rule 1 in any policy "
             "documentation. Source: NY S895B/A6789B report, January 2026 "
             "(https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf)."),
            ("[Feishu Maya Wed Sep 30 14:10 PST 2025] Also for Rule 2 — the text is "
             "'do not cheat or engage in content manipulation (including spamming, vote "
             "manipulation, ban evasion, or subscriber fraud)'. And for Rule 5 it's about "
             "'sharing manipulated content'.",
             "Noted. Reddit Rule 2 verbatim: 'do not cheat or engage in content manipulation "
             "(including spamming, vote manipulation, ban evasion, or subscriber fraud)'. "
             "Rule 5 covers 'sharing manipulated content'. These will be quoted verbatim."),
            ("[Feishu Maya Thu Oct 01 09:00 PST 2025] One note: I have an old internal "
             "document from 2023 saying Reddit's appeal window is 3 months. But looking at "
             "the current Help Center it says 6 months. Use the current official value.",
             "Understood — using the current official value of 6 months for Reddit appeal "
             "window, per https://support.reddithelp.com/hc/en-us/articles/"
             "23511059871252-Content-Moderation-Enforcement-and-Appeals. "
             "The 3-month figure from the 2023 internal document is outdated."),
        ]
    )

    # ---- Email — PM 传送 Meta 数据，含 Strike 7 错误值（V1 蜜罐）----
    append_history(
        SESS / f"{s_email}.jsonl", s_email, pe_cwd, "2025-09-29T11:00:00",
        [
            ("[Email jordan@pm → compliance-team@creatorhub Tue Sep 29 11:00 PST 2025] "
             "Subject: Meta Strike Data for Policy Engine\n"
             "Hi team, attaching the Meta execution data we collected from the transparency "
             "center. Key data point: Meta Strike 7 = **3-day** content creation ban. "
             "Strike 8 = 7 days. Please use these in the policy matrix.\n"
             "Also: Meta had >90% enforcement precision on Facebook and >87% on Instagram "
             "in Q3 2025 per their Integrity Report.",
             "Received Jordan's email. Note: the values for Strike 7 (3 days) and Strike 8 "
             "(7 days) in this email CONFLICT with the official Meta Transparency page which "
             "states Strike 7 = 1 day and Strike 8 = 3 days. I will use the official values "
             "from https://transparency.meta.com/enforcement/taking-action/restricting-accounts/ "
             "and flag this discrepancy in the conflict report.\n"
             "The Q3 2025 precision figures (>90% FB, >87% IG) match the official Integrity "
             "Report and will be used as-is."),
            ("[Email jordan@pm → compliance-team@creatorhub Wed Sep 30 15:30 PST 2025] "
             "Subject: RE: TikTok Q1 2025 Data\n"
             "Also FYI — TikTok removed 211 million videos in Q1 2025, about 0.9% of uploads. "
             "Automated detection caught about 87.4% (184,378,987 videos). "
             "Proactive removal rate was 99.0% and within-24h rate was 94.3%.",
             "Confirmed. These TikTok Q1 2025 figures match the official TikTok Transparency "
             "Report (https://www.tiktok.com/transparency/en/community-guidelines-enforcement-2025-1). "
             "I'll use these values in the Q1 2025 metrics file: 211,000,000 removed, "
             "184,378,987 automated, 99.0% proactive, 94.3% within 24h."),
        ]
    )

    # ---- Discord #mod-ops — 申诉案例更新，含 update_2 supersede 预告 ----
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, pe_cwd, "2025-10-01T16:00:00",
        [
            ("[Discord #mod-ops sam Wed Oct 01 16:00 PST 2025] Hey PolicyOps, heads up — "
             "we're sending a batch of 20 new appeal cases for processing. These are "
             "Cases T-001 through T-007 (TikTok), Y-001 through Y-006 (YouTube), "
             "M-001 through M-005 (Meta), and R-001 through R-002 (Reddit). "
             "Process them as update_1 provides.",
             "Acknowledged. Standing by for update_1 with the 20 new appeal cases "
             "(T-001 to T-007 TikTok, Y-001 to Y-006 YouTube, M-001 to M-005 Meta, "
             "R-001 to R-002 Reddit). I will update the appeal_tracker.json accordingly."),
            ("[Discord #mod-ops sam Thu Oct 02 10:00 PST 2025] Quick heads-up: after we "
             "process update_1, there may be a need to revisit the TikTok cases. "
             "The platform policy version used for those 7 cases (T-001 to T-007) is "
             "under review. Stand by for possible update_2 instructions.",
             "Understood. I'll flag the TikTok cases T-001 through T-007 as potentially "
             "subject to revision pending update_2. YouTube, Meta, and Reddit cases "
             "from update_1 are not affected."),
        ]
    )

    return {
        "main": main_id,
        "history": [
            (s_slack, "slack"),
            (s_feishu, "feishu"),
            (s_email, "email"),
            (s_discord, "discord"),
        ],
    }


# --------------------------------------------------------------------------- #
# 6. Updates（含 supersede）
# --------------------------------------------------------------------------- #
def gen_updates(sess_ids: dict) -> dict:
    s_discord = sess_ids["history"][3][0]
    pe_cwd = f"/workspace/{TID}/policy_engine"

    # ----- UPDATE 1: Q9 后，20 个申诉案例 + Slack 更新 -----
    u1_dir = UPD / "upd1"
    u1_dir.mkdir(parents=True, exist_ok=True)

    # 20 个申诉案例文件
    appeal_cases_new = {}
    # TikTok cases T-001 to T-007
    for i in range(1, 8):
        cid = f"T-{i:03d}"
        appeal_cases_new[cid] = {
            "platform": "tiktok",
            "status": "approved",
            "filed_date": "2025-10-05",
            "violation_type": "safety_civility",
            "reviewer": "human_review",
            "notes": f"TikTok appeal case T-{i:03d}"
        }
    # YouTube cases Y-001 to Y-006
    for i in range(1, 7):
        cid = f"Y-{i:03d}"
        appeal_cases_new[cid] = {
            "platform": "youtube",
            "status": "approved",
            "filed_date": "2025-10-05",
            "violation_type": "spam",
            "reviewer": "human_review",
            "notes": f"YouTube appeal case Y-{i:03d}"
        }
    # Meta cases M-001 to M-005
    for i in range(1, 6):
        cid = f"M-{i:03d}"
        appeal_cases_new[cid] = {
            "platform": "meta",
            "status": "approved" if i <= 3 else "denied",
            "filed_date": "2025-10-05",
            "violation_type": "hate_speech",
            "reviewer": "human_review",
            "notes": f"Meta appeal case M-{i:03d}"
        }
    # Reddit cases R-001 to R-002
    for i in range(1, 3):
        cid = f"R-{i:03d}"
        appeal_cases_new[cid] = {
            "platform": "reddit",
            "status": "pending",
            "filed_date": "2025-10-05",
            "violation_type": "rule1_hate",
            "reviewer": "human_review",
            "notes": f"Reddit appeal case R-{i:03d}"
        }

    # update_1 appeal_tracker: merge old + new, old cases 050/051/052 → under_review
    rng4 = random.Random(99)
    old_cases = {}
    for i, cid in enumerate([f"OLD-{j:04d}" for j in range(40, 60)]):
        plat = ["youtube", "meta", "tiktok", "reddit"][i % 4]
        st = "approved" if i < 10 else ("denied" if i < 15 else "pending")
        if cid in ["OLD-0050", "OLD-0051", "OLD-0052"]:
            st = "under_review"  # update_1 changes these
        old_cases[cid] = {
            "platform": plat,
            "status": st,
            "filed_date": f"2025-0{rng4.randint(1,9)}-{rng4.randint(10,28):02d}",
            "violation_type": rng4.choice(["spam", "hate_speech", "misinformation"]),
            "notes": f"Legacy appeal case {cid}"
        }
    all_cases = {**old_cases, **appeal_cases_new}

    updated_tracker = {
        "schema_version": "1.0",
        "last_updated": "2025-10-07",
        "total_cases": len(all_cases),
        "cases": all_cases
    }
    wj(u1_dir / "appeal_tracker.json", updated_tracker)

    # update_1 的额外 violation_log 追加（500 行，~30k tokens 目标）
    buf_u1 = io.StringIO()
    writer_u1 = csv.writer(buf_u1)
    violation_types_u1 = {
        "youtube": ["spam", "misinformation", "hate_speech", "violent_content",
                    "child_safety", "harassment", "extremism"],
        "meta": ["spam", "hate_speech", "dangerous_orgs", "violent_graphic",
                 "adult_nudity", "bullying_harassment", "csam", "fraud_deception",
                 "inauthentic_behavior", "cybersecurity"],
        "tiktok": ["safety_civility", "sensitive_mature", "misinformation",
                   "edited_media_ai", "privacy_security", "spam_manipulation"],
        "reddit": ["rule1_hate", "rule2_manipulation", "rule4_csam",
                   "rule5_misinfo", "rule6_safety", "rule7_illegal"],
    }
    plat_actions_u1 = {
        "youtube": ["warning", "strike_1", "strike_2", "channel_removal"],
        "meta": ["warning", "feature_restrict", "content_ban_1d",
                 "content_ban_3d", "content_ban_7d", "content_ban_30d"],
        "tiktok": ["warning", "video_removal", "shadowban", "permanent_ban"],
        "reddit": ["warning", "suspend_3d", "suspend_7d", "permanent_ban"],
    }
    rng5 = random.Random(55)
    viol_hdr = ["case_id", "platform", "violation_type", "severity", "date", "action_taken",
                "appeal_status", "appeal_deadline", "status", "reviewer",
                "policy_reference", "channel_context", "automated_flag", "human_reviewed",
                "escalated", "notes"]
    writer_u1.writerow(viol_hdr)
    for i in range(1001, 1501):
        plat = rng5.choice(["youtube", "meta", "tiktok", "reddit"])
        vtype = rng5.choice(violation_types_u1[plat])
        sev = rng5.choice(["low", "medium", "high", "critical"])
        day = rng5.randint(1, 15)
        policy_ref = f"policy_ref_{plat}_{vtype}"
        channel_ctx = rng5.choice(["gaming", "news", "education", "entertainment",
                                    "politics", "science", "sports", "music", "finance"])
        automated = rng5.choice(["true", "false"])
        human_rev = rng5.choice(["true", "false", "pending"])
        escalated = "true" if sev == "critical" else "false"
        writer_u1.writerow([
            f"VIOL-{i:05d}", plat, vtype, sev, f"2025-10-{day:02d}",
            rng5.choice(plat_actions_u1[plat]), "not_appealed",
            f"2026-04-{rng5.randint(1,28):02d}", "pending", "human_review",
            policy_ref, channel_ctx, automated, human_rev, escalated,
            f"New batch case {i} detected via automated monitoring. "
            f"Violation: {vtype}. Platform: {plat}. "
            f"Content removed pending review completion. "
            f"Case severity: {sev}. Escalation status: {escalated}."
        ])
    w(u1_dir / "violation_log_append.csv", buf_u1.getvalue())

    # update_1: 附加平台政策更新分析文档（扩充 u1 体量）
    w(u1_dir / "policy_update_analysis.md", _gen_policy_update_analysis())

    # update_1: Slack bot 摘要（再次声称 Meta Strike 7 = 3 天）
    s_slack_id = sess_ids["history"][0][0]
    sb_u1 = SessionBuilder(s_slack_id, pe_cwd, "2025-10-07T09:00:00")
    sb_u1.add_user(
        "[Slack #compliance alex Wed Oct 07 09:00 PST 2025] PolicyBot daily digest: "
        "Reminder that Meta Strike 7 = 3-day content ban per our internal tracking sheet. "
        "Also: old cases OLD-0050, OLD-0051, OLD-0052 have been moved to under_review status.",
        )
    sb_u1.add_assistant(
        "Noted. The old cases OLD-0050, OLD-0051, OLD-0052 are now under_review. "
        "However, the PolicyBot claim that Meta Strike 7 = 3 days remains INCORRECT — "
        "the official value is 1 day per Meta Transparency. This is a known bot error."
    )
    msg_lines_u1 = [ln for ln in sb_u1.lines if ln.get("type") == "message"]
    w(u1_dir / f"{s_slack_id}_append.jsonl",
      "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines_u1) + "\n")

    # ----- UPDATE 2: Q12 后，supersede TikTok 子集 + TikTok Q3 2025 报告 -----
    u2_dir = UPD / "upd2"
    u2_dir.mkdir(parents=True, exist_ok=True)

    # update_2 appeal_tracker: TikTok T-001~T-007 回滚至 pending（supersede）
    # YouTube/Meta/Reddit 保持 update_1 状态
    u2_cases = dict(all_cases)
    for i in range(1, 8):
        cid = f"T-{i:03d}"
        u2_cases[cid]["status"] = "pending"  # supersede: roll back from approved
        u2_cases[cid]["notes"] = (
            f"TikTok appeal T-{i:03d}: SUPERSEDED by update_2 — status reset to pending "
            "pending policy version verification (TikTok cases only)"
        )
    u2_tracker = {
        "schema_version": "1.0",
        "last_updated": "2025-10-14",
        "total_cases": len(u2_cases),
        "cases": u2_cases
    }
    wj(u2_dir / "appeal_tracker.json", u2_tracker)

    # TikTok Q3 2025 合成透明报告（替代 Q1 2025）
    wj(u2_dir / "tiktok_q3_2025_report.json", {
        "platform": "tiktok",
        "quarter": "Q3_2025",
        "schema_version": "1.0",
        "_source_url": "https://www.tiktok.com/transparency/en/community-guidelines-enforcement-2025-3",
        "videos_removed": 198000000,
        "videos_removed_source_url": "https://www.tiktok.com/transparency/en/community-guidelines-enforcement-2025-3",
        "videos_removed_pct_of_uploads": 0.0087,
        "automated_removed": 175440000,
        "automation_rate": 0.886,
        "reinstated": 6980000,
        "proactive_rate": 0.991,
        "within_24h_rate": 0.948,
        "violation_breakdown": {
            "sensitive_mature_pct": 0.288,
            "misinformation_pct": 0.447,
            "edited_media_ai_pct": 0.152,
            "safety_civility_pct": 0.121,
            "privacy_security_pct": 0.144
        },
        "note": "Q3 2025 transparency report; supersedes Q1 2025 data for current reporting period"
    })

    # update_2: 新增违规案例批次分析（填充 u2 体量）
    w(u2_dir / "tiktok_policy_review.md", _gen_tiktok_policy_review())
    # update_2: 添加 Q3 2025 分析报告和新违规案例（补足体量到 >30k tokens）
    _gen_upd2_violation_log(u2_dir / "violation_log_q3_2025.csv")

    # update_2: Discord mod-ops 通告（supersede TikTok 子集）
    s_discord_id = sess_ids["history"][3][0]
    sb_u2 = SessionBuilder(s_discord_id, pe_cwd, "2025-10-14T10:00:00")
    sb_u2.add_user(
        "[Discord #mod-ops sam Tue Oct 14 10:00 PST 2025] OPERATIONS NOTICE (supersedes "
        "update_1 for TikTok cases): After review, TikTok appeal cases T-001 through T-007 "
        "that were approved in update_1 must be RESET to 'pending' status. The policy version "
        "used to evaluate these cases is under verification. This ONLY affects TikTok cases "
        "T-001 to T-007. YouTube cases (Y-001 to Y-006), Meta cases (M-001 to M-005), and "
        "Reddit cases (R-001 to R-002) from update_1 are NOT affected — keep their statuses. "
        "Also attaching TikTok Q3 2025 transparency report to replace the Q1 2025 data."
    )
    sb_u2.add_assistant(
        "Understood. Operations notice applied: "
        "- TikTok cases T-001 to T-007: status reset to 'pending' (SUPERSEDES update_1 approval). "
        "- YouTube Y-001 to Y-006: status unchanged (approved). "
        "- Meta M-001 to M-003: status unchanged (approved); M-004 to M-005: unchanged (denied). "
        "- Reddit R-001 to R-002: status unchanged (pending). "
        "TikTok Q3 2025 report received and will replace the Q1 2025 data file."
    )
    msg_lines_u2 = [ln for ln in sb_u2.lines if ln.get("type") == "message"]
    w(u2_dir / f"{s_discord_id}_append.jsonl",
      "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines_u2) + "\n")

    # 新增监管审查清单（填充 u2 体量）
    _gen_regulatory_checklist(u2_dir / "regulatory_review_checklist.md")

    # ----- UPDATE 3: Q15 后，EU DSA 合规要求 -----
    u3_dir = UPD / "upd3"
    u3_dir.mkdir(parents=True, exist_ok=True)

    # EU DSA 合成文档（20k tokens 目标）
    _gen_eu_dsa_doc(u3_dir / "eu_dsa_compliance.md")

    # update_3: email 线程（VLOP 分类讨论）
    s_email_id = sess_ids["history"][2][0]
    sb_u3 = SessionBuilder(s_email_id, pe_cwd, "2025-11-01T10:00:00")
    sb_u3.add_user(
        "[Email legal@creatorhub → compliance-team Sat Nov 01 10:00 PST 2025] "
        "Subject: EU DSA VLOP Compliance Requirements\n\n"
        "Team, the EU Digital Services Act (DSA) requires Very Large Online Platforms (VLOPs) "
        "to conduct annual systemic risk assessments under Article 34 and implement risk "
        "mitigation measures under Article 35. The platforms we track that qualify as VLOPs "
        "are YouTube (Google), Meta (Facebook/Instagram), and TikTok. "
        "Reddit does NOT currently meet the 45M EU active user VLOP threshold. "
        "Please update the regulatory addendum accordingly.\n\n"
        "Key DSA requirements for VLOPs:\n"
        "- Art. 34: Annual systemic risk assessment\n"
        "- Art. 35: Risk mitigation measures\n"
        "- Art. 40: Data access for researchers\n"
        "- Art. 42: Transparency reporting obligations\n\n"
        "Action: Create `internal/regulatory_addendum.json` with the affected platforms "
        "and article references."
    )
    sb_u3.add_assistant(
        "Understood. EU DSA compliance task recorded:\n"
        "- Affected platforms (VLOP threshold): YouTube, Meta, TikTok\n"
        "- Reddit: does NOT meet 45M EU active user VLOP threshold → NOT affected\n"
        "- Key articles: Art. 34 (risk assessment), Art. 35 (mitigation), "
        "Art. 40 (researcher data access), Art. 42 (transparency reporting)\n"
        "Will create `internal/regulatory_addendum.json` with these details."
    )
    msg_lines_u3 = [ln for ln in sb_u3.lines if ln.get("type") == "message"]
    w(u3_dir / f"{s_email_id}_append.jsonl",
      "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines_u3) + "\n")

    # update_3: 追加 DSA 条款对照表（填充体量）
    _gen_dsa_articles_reference(u3_dir / "dsa_articles_reference.json")
    # update_3: VLOP 分析报告（填充 u3 体量）
    w(u3_dir / "vlop_analysis_report.md", _gen_vlop_analysis_report())
    # update_3: 添加监管合规邮件线程文档（补足体量到 >30k tokens）
    w(u3_dir / "legal_email_thread.md", _gen_legal_email_thread())
    _gen_upd3_dsa_case_log(u3_dir / "dsa_compliance_cases.csv")

    updates_decl = {
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1",
            "files": [
                {"name": "appeal_tracker.json", "action": "new",
                 "target": "policy_engine/internal/appeal_tracker.json"},
                {"name": "violation_log_append.csv", "action": "append",
                 "target": "policy_engine/internal/violation_log_2025.csv"},
                {"name": "policy_update_analysis.md", "action": "new",
                 "target": "policy_engine/internal/policy_update_analysis.md"},
            ]
        },
        "upd1_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd1",
            "files": [
                {"name": f"{s_slack_id}_append.jsonl", "action": "append",
                 "target": f"{s_slack_id}.jsonl"}
            ]
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2",
            "files": [
                {"name": "appeal_tracker.json", "action": "new",
                 "target": "policy_engine/internal/appeal_tracker.json"},
                {"name": "tiktok_q3_2025_report.json", "action": "new",
                 "target": "policy_engine/platforms/tiktok/q3_2025_report.json"},
                {"name": "regulatory_review_checklist.md", "action": "new",
                 "target": "policy_engine/internal/regulatory_review_checklist.md"},
                {"name": "tiktok_policy_review.md", "action": "new",
                 "target": "policy_engine/internal/tiktok_policy_review.md"},
                {"name": "violation_log_q3_2025.csv", "action": "new",
                 "target": "policy_engine/internal/violation_log_q3_2025.csv"},
            ]
        },
        "upd2_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd2",
            "files": [
                {"name": f"{s_discord_id}_append.jsonl", "action": "append",
                 "target": f"{s_discord_id}.jsonl"}
            ]
        },
        "upd3_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd3",
            "files": [
                {"name": "eu_dsa_compliance.md", "action": "new",
                 "target": "policy_engine/internal/eu_dsa_compliance.md"},
                {"name": "dsa_articles_reference.json", "action": "new",
                 "target": "policy_engine/internal/dsa_articles_reference.json"},
                {"name": "vlop_analysis_report.md", "action": "new",
                 "target": "policy_engine/internal/vlop_analysis_report.md"},
                {"name": "legal_email_thread.md", "action": "new",
                 "target": "policy_engine/internal/legal_email_thread.md"},
                {"name": "dsa_compliance_cases.csv", "action": "new",
                 "target": "policy_engine/internal/dsa_compliance_cases.csv"},
            ]
        },
        "upd3_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd3",
            "files": [
                {"name": f"{s_email_id}_append.jsonl", "action": "append",
                 "target": f"{s_email_id}.jsonl"}
            ]
        },
    }
    return updates_decl


def _gen_policy_update_analysis() -> str:
    """生成政策更新分析文档（~20k tokens，填充 update_1 体量）。"""
    sections = []
    sections.append("# Content Policy Update Analysis — Batch Processing Report\n\n")
    sections.append("*Generated: 2025-10-07 | Analyst: PolicyOps AI | Batch: update_1*\n\n")
    sections.append(
        "This document analyzes 500 new violation cases (VIOL-01001 through VIOL-01500) "
        "processed as part of update_1. Cases span all four monitored platforms.\n\n"
    )

    # 平台别分析
    platforms_analysis = {
        "YouTube": {
            "case_range": "VIOL-01001 to VIOL-01250 (subset)",
            "total": 125,
            "distribution": {
                "spam": 28, "misinformation": 31, "hate_speech": 22,
                "violent_content": 18, "child_safety": 8, "harassment": 12,
                "extremism": 6
            },
            "action_distribution": {
                "warning": 45, "strike_1": 52, "strike_2": 21, "channel_removal": 7
            },
            "avg_severity": "medium",
            "escalated": 14,
            "key_findings": [
                "Medical misinformation continues to be a dominant violation type",
                "Strike escalation rate is 22% (strike_2 as % of all strikes)",
                "7 channel removals due to third strike within 90-day window",
                "Child safety violations account for 6.4% — higher than baseline",
            ]
        },
        "Meta": {
            "case_range": "VIOL-01251 to VIOL-01400 (subset)",
            "total": 150,
            "distribution": {
                "spam": 32, "hate_speech": 28, "dangerous_orgs": 12,
                "violent_graphic": 18, "adult_nudity": 15, "bullying_harassment": 22,
                "csam": 3, "fraud_deception": 11, "inauthentic_behavior": 5,
                "cybersecurity": 4
            },
            "action_distribution": {
                "warning": 38, "feature_restrict": 42,
                "content_ban_1d": 31, "content_ban_3d": 22,
                "content_ban_7d": 11, "content_ban_30d": 6
            },
            "avg_severity": "medium",
            "escalated": 19,
            "key_findings": [
                "CSAM cases (3) handled immediately with NCMEC referral",
                "Hate speech accounts for 18.7% of Meta cases",
                "content_ban_1d (Strike 7 threshold) is the most common ban type",
                "Q4 2025 reduction in violent/graphic cases consistent with Meta H2 2025 report",
            ]
        },
        "TikTok": {
            "case_range": "VIOL-01401 to VIOL-01450 (subset)",
            "total": 125,
            "distribution": {
                "safety_civility": 14, "sensitive_mature": 38,
                "misinformation": 57, "edited_media_ai": 17, "privacy_security": 21
            },
            "action_distribution": {
                "warning": 22, "video_removal": 68, "shadowban": 24, "permanent_ban": 11
            },
            "avg_severity": "medium-high",
            "escalated": 24,
            "key_findings": [
                "Misinformation (45.6%) remains the top violation category — consistent with Q1 2025 report",
                "11 permanent bans issued (all three-strike cases within 90-day window)",
                "Proactive detection rate exceeds 95% for this batch",
                "AI-generated manipulated content rising as % of violations",
            ]
        },
        "Reddit": {
            "case_range": "VIOL-01451 to VIOL-01500 (subset)",
            "total": 100,
            "distribution": {
                "rule1_hate": 38, "rule2_manipulation": 19,
                "rule4_csam": 2, "rule5_misinfo": 16,
                "rule6_safety": 18, "rule7_illegal": 7
            },
            "action_distribution": {
                "warning": 24, "suspend_3d": 31, "suspend_7d": 29, "permanent_ban": 16
            },
            "avg_severity": "medium",
            "escalated": 18,
            "key_findings": [
                "Rule 1 (hate content) remains highest-volume violation for Reddit",
                "16 permanent bans including 2 CSAM (immediate) and 14 repeat violators",
                "Hateful content automation rate (77.2% per H1 2025 data) reflected in batch",
                "40.7% historical harassment reversal rate suggests significant human review demand",
            ]
        },
    }

    for plat, data in platforms_analysis.items():
        sections.append(f"## {plat} Analysis\n\n")
        sections.append(f"**Case Range**: {data['case_range']}\n")
        sections.append(f"**Total Cases**: {data['total']}\n")
        sections.append(f"**Avg Severity**: {data['avg_severity']}\n")
        sections.append(f"**Escalated**: {data['escalated']}\n\n")

        sections.append("### Violation Distribution\n\n")
        for vtype, count in data['distribution'].items():
            pct = 100 * count / data['total']
            sections.append(f"- {vtype}: {count} cases ({pct:.1f}%)\n")
        sections.append("\n")

        sections.append("### Action Distribution\n\n")
        for action, count in data['action_distribution'].items():
            pct = 100 * count / data['total']
            sections.append(f"- {action}: {count} ({pct:.1f}%)\n")
        sections.append("\n")

        sections.append("### Key Findings\n\n")
        for finding in data['key_findings']:
            sections.append(f"- {finding}\n")
        sections.append("\n")

    sections.append("## Cross-Platform Comparison\n\n")
    sections.append("### Severity Distribution (all platforms)\n\n")
    sections.append("| Severity | YouTube | Meta | TikTok | Reddit |\n")
    sections.append("|---|---|---|---|---|\n")
    for sev, yt, me, tt, rd in [
        ("low", "28%", "22%", "15%", "18%"),
        ("medium", "45%", "48%", "42%", "44%"),
        ("high", "21%", "24%", "31%", "28%"),
        ("critical", "6%", "6%", "12%", "10%"),
    ]:
        sections.append(f"| {sev} | {yt} | {me} | {tt} | {rd} |\n")
    sections.append("\n")

    sections.append("### Appeal Window Reference (for case deadline calculation)\n\n")
    sections.append("| Platform | Strike/Account Appeal | Content Removal Appeal |\n")
    sections.append("|---|---|---|\n")
    sections.append("| YouTube | 6 months | 12 months |\n")
    sections.append("| Meta | Not publicly specified | Not publicly specified |\n")
    sections.append("| TikTok | Not publicly specified | Not publicly specified |\n")
    sections.append("| Reddit | 6 months | 6 months |\n\n")

    sections.append("## Cases Requiring Immediate Action\n\n")
    sections.append(
        "The following cases from this batch require immediate attention based on "
        "severity classification or policy type:\n\n"
    )
    urgent_cases = [
        ("VIOL-01008", "TikTok", "CSAM", "critical", "Immediate permanent ban + NCMEC referral"),
        ("VIOL-01043", "Meta", "CSAM", "critical", "Immediate termination + NCMEC referral"),
        ("VIOL-01087", "Reddit", "CSAM", "critical", "Immediate permanent ban + NCMEC referral"),
        ("VIOL-01112", "YouTube", "Extremism", "critical", "Channel removal; law enforcement referral"),
        ("VIOL-01156", "TikTok", "Terrorism", "critical", "Permanent ban; law enforcement referral"),
        ("VIOL-01198", "Meta", "Dangerous Orgs", "critical", "Account termination"),
        ("VIOL-01234", "Reddit", "Rule 4 CSAM", "critical", "Immediate permanent ban"),
        ("VIOL-01267", "YouTube", "Violent extremism", "high", "Strike 2; escalated review"),
        ("VIOL-01312", "TikTok", "Health misinformation", "high", "Video removal; 3rd strike warning"),
        ("VIOL-01389", "Meta", "Coordinated harassment", "high", "content_ban_7d"),
    ]
    sections.append("| Case ID | Platform | Type | Severity | Recommended Action |\n")
    sections.append("|---|---|---|---|---|\n")
    for case_id, plat, vtype, sev, action in urgent_cases:
        sections.append(f"| {case_id} | {plat} | {vtype} | {sev} | {action} |\n")
    sections.append("\n")

    sections.append("## Status Change Notifications\n\n")
    sections.append(
        "The following legacy cases had status changes applied as part of update_1 processing:\n\n"
    )
    sections.append("| Case ID | Previous Status | New Status | Reason |\n")
    sections.append("|---|---|---|---|\n")
    sections.append("| OLD-0050 | approved | under_review | New evidence submitted |\n")
    sections.append("| OLD-0051 | approved | under_review | Policy interpretation review |\n")
    sections.append("| OLD-0052 | approved | under_review | Reviewer escalation |\n")
    sections.append("\n")

    sections.append("## Note on TikTok Cases T-001 to T-007\n\n")
    sections.append(
        "TikTok appeal cases T-001 through T-007 have been processed as 'approved' "
        "in this batch based on review findings under the current policy version. "
        "However, per Discord #mod-ops notification from Sam Rivera (Oct 02), "
        "these cases may be subject to review under update_2 if the TikTok policy "
        "version used is found to be under verification. Engineers should monitor "
        "for update_2 instructions.\n\n"
        "YouTube cases Y-001 to Y-006: approved.\n"
        "Meta cases M-001 to M-003: approved; M-004 to M-005: denied.\n"
        "Reddit cases R-001 to R-002: pending further review.\n\n"
    )

    sections.append("---\n\n")
    sections.append("*End of update_1 analysis report*\n")

    return "".join(sections)


def _gen_tiktok_policy_review() -> str:
    """生成 TikTok 政策审查文档（~20k tokens，填充 update_2 体量）。"""
    sections = []
    sections.append("# TikTok Policy Version Review — Case Batch T-001 to T-007\n\n")
    sections.append(
        "*Generated: 2025-10-14 | Analyst: PolicyOps AI | "
        "Status: SUPERSEDE NOTICE APPLIED*\n\n"
    )
    sections.append(
        "This document records the policy review triggered by Sam Rivera's Discord "
        "#mod-ops notice (2025-10-14), which instructed that TikTok appeal cases "
        "T-001 through T-007 approved in update_1 must be reset to 'pending' status.\n\n"
        "**Scope of supersede**: TikTok cases T-001 to T-007 ONLY.\n"
        "**Not affected**: YouTube Y-001 to Y-006, Meta M-001 to M-005, "
        "Reddit R-001 to R-002.\n\n"
    )

    sections.append("## Background\n\n")
    sections.append(
        "During update_1 processing, TikTok appeal cases T-001 through T-007 were "
        "reviewed and approved based on the policy version then current. Subsequent "
        "investigation identified that the specific policy version used for these "
        "7 cases may not be the current authoritative version. The TikTok Community "
        "Guidelines document used for review is pending version verification.\n\n"
    )

    sections.append("## Affected Cases\n\n")
    sections.append("| Case ID | Platform | Previous Status (update_1) | New Status (update_2) | Reason |\n")
    sections.append("|---|---|---|---|---|\n")
    for i in range(1, 8):
        sections.append(
            f"| T-{i:03d} | TikTok | approved | **pending** | "
            f"Policy version verification required |\n"
        )
    sections.append("\n")

    sections.append("## Non-Affected Cases\n\n")
    sections.append(
        "The following cases from update_1 are NOT affected by this supersede notice "
        "and retain their update_1 status:\n\n"
    )
    sections.append("| Case ID | Platform | Status | Notes |\n")
    sections.append("|---|---|---|---|\n")
    for i in range(1, 7):
        sections.append(f"| Y-{i:03d} | YouTube | approved | Unchanged — YT policy version unaffected |\n")
    for i in range(1, 4):
        sections.append(f"| M-{i:03d} | Meta | approved | Unchanged — Meta policy version unaffected |\n")
    for i in range(4, 6):
        sections.append(f"| M-{i:03d} | Meta | denied | Unchanged — Meta policy version unaffected |\n")
    for i in range(1, 3):
        sections.append(f"| R-{i:03d} | Reddit | pending | Unchanged — Reddit policy version unaffected |\n")
    sections.append("\n")

    sections.append("## TikTok Policy Version History\n\n")
    sections.append(
        "TikTok periodically updates its Community Guidelines. The following table "
        "documents known version changes relevant to safety_civility enforcement:\n\n"
    )
    sections.append("| Date | Version | Key Change | Relevant to Batch |\n")
    sections.append("|---|---|---|---|\n")
    sections.append("| 2025-01-01 | v3.0 | Expanded safety_civility definitions | Yes |\n")
    sections.append("| 2025-03-15 | v3.1 | Clarified edited_media_ai scope | No |\n")
    sections.append("| 2025-06-01 | v3.2 | Updated strike expiry mechanics | Possible |\n")
    sections.append("| 2025-09-01 | v3.3 | Revised misinformation criteria | No |\n")
    sections.append("\n")

    sections.append("## TikTok Q3 2025 Report — Update to Q1 2025 Data\n\n")
    sections.append(
        "Alongside this supersede notice, update_2 provides the TikTok Q3 2025 "
        "Transparency Report data to replace the Q1 2025 data as the current reference. "
        "Key comparison:\n\n"
    )
    sections.append("| Metric | Q1 2025 | Q3 2025 | Change |\n")
    sections.append("|---|---|---|---|\n")
    sections.append("| Videos Removed | 211,000,000 | 198,000,000 | -6.2% |\n")
    sections.append("| Automation Rate | 87.4% | 88.6% | +1.2pp |\n")
    sections.append("| Reinstated | 7,525,184 | 6,980,000 | -7.2% |\n")
    sections.append("| Proactive Rate | 99.0% | 99.1% | +0.1pp |\n")
    sections.append("| Within 24h Rate | 94.3% | 94.8% | +0.5pp |\n")
    sections.append("\n")

    sections.append("## Q3 2025 Violation Breakdown\n\n")
    sections.append("| Category | Q1 2025 | Q3 2025 | Trend |\n")
    sections.append("|---|---|---|---|\n")
    sections.append("| Sensitive/Mature | 30.1% | 28.8% | Decreasing |\n")
    sections.append("| Misinformation | 45.5% | 44.7% | Stable |\n")
    sections.append("| Edited Media/AI | 13.8% | 15.2% | Increasing |\n")
    sections.append("| Safety & Civility | 11.5% | 12.1% | Slight increase |\n")
    sections.append("| Privacy & Security | 15.6% | 14.4% | Decreasing |\n\n")

    sections.append("## Processing Instructions for Affected Cases\n\n")
    sections.append(
        "Cases T-001 through T-007 must remain in 'pending' status until:\n\n"
        "1. TikTok policy version verification is complete\n"
        "2. Cases are re-reviewed under the verified policy version\n"
        "3. A new determination (approved/denied) is made under the verified policy\n\n"
        "Engineers must not approve these cases under update_1 guidance until "
        "the policy version issue is resolved. Reopening these cases for re-review "
        "is authorized by the update_2 supersede notice.\n\n"
    )

    sections.append("---\n\n*End of TikTok policy review document*\n")
    return "".join(sections)


def _gen_vlop_analysis_report() -> str:
    """生成 VLOP 分析报告（~15k tokens，填充 update_3 体量）。"""
    sections = []
    sections.append("# VLOP Designation Analysis — EU DSA Compliance Report\n\n")
    sections.append(
        "*Generated: 2025-11-01 | Analyst: PolicyOps AI | Context: update_3*\n\n"
    )
    sections.append(
        "This report analyzes the VLOP (Very Large Online Platform) designation "
        "implications of the EU Digital Services Act (DSA) for the four platforms "
        "monitored by CreatorHub's compliance engine.\n\n"
    )

    sections.append("## VLOP Designation Summary\n\n")
    sections.append("| Platform | EU Monthly Active Users (Est.) | VLOP Designated | DSA Art. 34/35 Applies |\n")
    sections.append("|---|---|---|---|\n")
    sections.append("| YouTube (Google) | ~450M | **Yes** | **Yes** |\n")
    sections.append("| Facebook (Meta) | ~310M | **Yes** | **Yes** |\n")
    sections.append("| Instagram (Meta) | ~250M | **Yes** | **Yes** |\n")
    sections.append("| TikTok | ~150M | **Yes** | **Yes** |\n")
    sections.append("| Reddit | ~15-25M (est.) | **No** | **No** |\n\n")

    sections.append("## Platform-by-Platform DSA Analysis\n\n")

    platform_dsa = {
        "YouTube (Google/Alphabet)": {
            "vlop": True,
            "eu_users": "~450 million",
            "designation_date": "April 2023",
            "art34_requirements": [
                "Annual systemic risk assessment covering fundamental rights, civic discourse, "
                "psychological well-being, public security",
                "Assessment must address algorithmic amplification of harmful content",
                "Assessment must consider minors' rights and gender-based violence risks",
            ],
            "art35_measures": [
                "Enhanced content moderation with additional human review capacity",
                "Algorithm adjustments to reduce harmful content amplification",
                "User empowerment tools (content preference controls)",
                "Crisis response protocols for disinformation during elections or crises",
            ],
            "art42_reporting": "Semi-annual transparency reports; enforcement metrics; "
                               "human review statistics",
            "compliance_status": "In compliance; Google annual DSA risk assessment published Q3 2024",
        },
        "Meta (Facebook + Instagram)": {
            "vlop": True,
            "eu_users": "~310M (Facebook) + ~250M (Instagram)",
            "designation_date": "April 2023",
            "art34_requirements": [
                "Annual systemic risk assessment (both Facebook and Instagram separately)",
                "Assessment of algorithmic recommendation systems impact",
                "Assessment of potential amplification of terrorist content",
                "Assessment of risks to democratic processes",
            ],
            "art35_measures": [
                "Content moderation enhancements for EU users",
                "Improved appeal mechanisms per DSA Article 16",
                "User interface adjustments per DSA Article 38",
                "Crisis protocol activation capability per DSA Article 36",
            ],
            "art42_reporting": "Semi-annual transparency reports; already publishes "
                               "Community Standards Enforcement Reports",
            "compliance_status": "In compliance; Q3 2025 Integrity Report addresses DSA requirements",
        },
        "TikTok": {
            "vlop": True,
            "eu_users": "~150 million",
            "designation_date": "April 2023",
            "art34_requirements": [
                "Annual systemic risk assessment with EU-specific scope",
                "Assessment of content recommendation algorithm risks for young users",
                "Assessment of misinformation amplification (45.5% of Q1 2025 removals)",
                "Assessment of AI-generated content risks (growing violation category)",
            ],
            "art35_measures": [
                "Enhanced safety tools for users under 18",
                "Algorithm transparency for recommendation systems",
                "Researcher data access protocol per Article 40",
                "EU-specific content moderation team",
            ],
            "art42_reporting": "Semi-annual transparency reports; existing Q1/Q2/Q3/Q4 "
                               "Community Guidelines reports partially satisfy this",
            "compliance_status": "Under review; EC conducted formal investigation in 2024",
        },
        "Reddit": {
            "vlop": False,
            "eu_users": "~15-25 million (estimated; not officially disclosed)",
            "designation_date": "Not designated",
            "standard_dsa_obligations": [
                "Article 14: Notice-and-action mechanism for illegal content",
                "Article 15: Statement of reasons for content restrictions",
                "Article 16: Internal complaint-handling system",
                "Article 17: Out-of-court dispute settlement access",
            ],
            "compliance_status": "Standard DSA obligations apply; VLOP obligations do NOT apply",
            "note": "Reddit's EU user base is estimated at 15-25M, "
                    "well below the 45M threshold for VLOP designation. "
                    "Reddit must comply with standard DSA obligations (Art. 14-18) "
                    "but is exempt from VLOP-specific requirements (Art. 34, 35, 40, 42).",
        },
    }

    for plat, data in platform_dsa.items():
        sections.append(f"### {plat}\n\n")
        sections.append(f"**VLOP Designated**: {'Yes' if data['vlop'] else 'No'}\n")
        sections.append(f"**EU Monthly Active Users**: {data.get('eu_users', 'N/A')}\n")
        if data['vlop']:
            sections.append(f"**Designation Date**: {data.get('designation_date', 'N/A')}\n\n")
            sections.append("**Article 34 Requirements**:\n")
            for req in data.get('art34_requirements', []):
                sections.append(f"- {req}\n")
            sections.append("\n**Article 35 Measures**:\n")
            for measure in data.get('art35_measures', []):
                sections.append(f"- {measure}\n")
            sections.append(f"\n**Article 42 Reporting**: {data.get('art42_reporting', 'N/A')}\n")
        else:
            sections.append("\n**Standard DSA Obligations Only**:\n")
            for oblig in data.get('standard_dsa_obligations', []):
                sections.append(f"- {oblig}\n")
            sections.append(f"\n**Note**: {data.get('note', '')}\n")
        sections.append(f"\n**Compliance Status**: {data.get('compliance_status', 'N/A')}\n\n")

    sections.append("## CreatorHub Compliance Engine Impact\n\n")
    sections.append(
        "The DSA creates differentiated obligations for the platforms CreatorHub monitors:\n\n"
    )
    sections.append("| Obligation | YouTube | Meta | TikTok | Reddit |\n")
    sections.append("|---|---|---|---|---|\n")
    sections.append("| Art. 14 Notice-Action | Required | Required | Required | Required |\n")
    sections.append("| Art. 15 Reason Statement | Required | Required | Required | Required |\n")
    sections.append("| Art. 16 Internal Complaint | Required | Required | Required | Required |\n")
    sections.append("| Art. 34 Risk Assessment | **Required** | **Required** | **Required** | Not Required |\n")
    sections.append("| Art. 35 Mitigation | **Required** | **Required** | **Required** | Not Required |\n")
    sections.append("| Art. 40 Researcher Access | **Required** | **Required** | **Required** | Not Required |\n")
    sections.append("| Art. 42 Transparency | **Required** | **Required** | **Required** | Not Required |\n\n")

    sections.append("## Regulatory_addendum.json Template\n\n")
    sections.append(
        "Based on this analysis, the `internal/regulatory_addendum.json` should contain:\n\n"
        "```json\n"
        "{\n"
        '  "regulation": "EU_DSA",\n'
        '  "regulation_ref": "Regulation (EU) 2022/2065",\n'
        '  "affected_platforms": ["youtube", "meta", "tiktok"],\n'
        '  "non_affected_platforms": ["reddit"],\n'
        '  "article_reference": ["Art. 34", "Art. 35", "Art. 40", "Art. 42"],\n'
        '  "rationale": "Reddit does not meet the 45M EU active user VLOP threshold"\n'
        "}\n"
        "```\n\n"
    )

    sections.append("---\n\n*End of VLOP analysis report*\n")
    return "".join(sections)


def _gen_upd2_violation_log(path: Path) -> None:
    """生成 Q3 2025 违规日志（400行 × 详细列，填充 update_2 体量）。"""
    rng = random.Random(303)
    buf = io.StringIO()
    writer = csv.writer(buf)
    header = [
        "case_id", "platform", "violation_type", "severity", "quarter",
        "date", "action_taken", "appeal_status", "appeal_outcome",
        "automated_flag", "human_reviewed", "escalated", "policy_version",
        "reviewer_id", "processing_time_hours", "content_type",
        "channel_context", "geographic_region", "notes"
    ]
    writer.writerow(header)
    violation_types = {
        "tiktok": ["safety_civility", "sensitive_mature", "misinformation",
                   "edited_media_ai", "privacy_security"],
        "youtube": ["spam", "misinformation", "hate_speech", "violent_content", "harassment"],
        "meta": ["spam", "hate_speech", "bullying_harassment", "violent_graphic", "adult_nudity"],
        "reddit": ["rule1_hate", "rule2_manipulation", "rule5_misinfo", "rule6_safety"],
    }
    actions = {
        "tiktok": ["video_removal", "shadowban", "strike", "permanent_ban"],
        "youtube": ["warning", "strike_1", "strike_2", "channel_removal"],
        "meta": ["warning", "feature_restrict", "content_ban_1d", "content_ban_3d"],
        "reddit": ["warning", "suspend_3d", "suspend_7d", "permanent_ban"],
    }
    regions = ["EU", "US", "APAC", "LATAM", "MEA", "Global"]
    content_types = ["video", "comment", "post", "story", "live_stream", "image"]
    contexts = ["gaming", "news", "education", "entertainment", "politics",
                "sports", "music", "science", "health", "technology"]
    for i in range(2001, 2401):
        plat = rng.choice(["tiktok", "youtube", "meta", "reddit"])
        vtype = rng.choice(violation_types[plat])
        sev = rng.choice(["low", "medium", "high", "critical"])
        day = rng.randint(1, 90)
        month = 7 + (day - 1) // 30
        date_str = f"2025-{month:02d}-{((day - 1) % 30) + 1:02d}"
        action = rng.choice(actions[plat])
        appeal = rng.choice(["not_appealed", "appealed_pending",
                              "appealed_approved", "appealed_denied"])
        outcome = "approved" if "approved" in appeal else ("denied" if "denied" in appeal else "")
        automated = rng.choice(["true", "false"])
        human_rev = "true" if automated == "false" else rng.choice(["true", "false"])
        escalated = "true" if sev in ("critical", "high") and rng.random() < 0.3 else "false"
        policy_ver = rng.choice(["v3.1", "v3.2", "v3.3"]) if plat == "tiktok" else "current"
        reviewer_id = f"REV-{rng.randint(100, 999)}"
        proc_time = rng.randint(1, 72)
        ctype = rng.choice(content_types)
        ctx = rng.choice(contexts)
        region = rng.choice(regions)
        writer.writerow([
            f"Q3-{i:05d}", plat, vtype, sev, "Q3_2025",
            date_str, action, appeal, outcome,
            automated, human_rev, escalated, policy_ver,
            reviewer_id, proc_time, ctype,
            ctx, region,
            f"Q3 2025 case {i}: {vtype} on {plat}. "
            f"Detected {'automatically' if automated == 'true' else 'via user report'}. "
            f"Processing time: {proc_time}h. "
            f"Policy version: {policy_ver}. Region: {region}."
        ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(buf.getvalue(), encoding="utf-8")


def _gen_legal_email_thread() -> str:
    """生成法律团队邮件线程文档（~20k tokens，填充 update_3 体量）。"""
    emails = []
    emails.append("# Legal Team Email Thread — EU DSA VLOP Compliance\n\n")
    emails.append("*Thread: DSA Compliance Requirements for Monitored Platforms*\n\n")
    emails.append("*Date Range: October 25, 2025 – November 1, 2025*\n\n")
    emails.append("---\n\n")

    thread = [
        ("2025-10-25 09:00", "maya.patel@creatorhub.com",
         "compliance-team@creatorhub.com, lin.wei@creatorhub.com",
         "EU DSA VLOP Compliance Requirements — Action Required",
         """Team,

Following our review of the European Commission's VLOP designation list (updated August 2025),
I need to flag several urgent compliance items for our policy engine.

**Platforms Designated as VLOPs (45M+ EU monthly users)**:
- YouTube (Google): ~450M EU users — VLOP, Art. 34/35 APPLY
- Facebook (Meta): ~310M EU users — VLOP, Art. 34/35 APPLY
- Instagram (Meta): ~250M EU users — VLOP, Art. 34/35 APPLY
- TikTok: ~150M EU users — VLOP, Art. 34/35 APPLY

**Platforms NOT Meeting VLOP Threshold**:
- Reddit: estimated 15-25M EU users — NOT a VLOP; Art. 34/35 do NOT apply

Key DSA articles requiring immediate attention:
- **Article 34**: Annual systemic risk assessment (all VLOPs)
- **Article 35**: Risk mitigation measures (all VLOPs)
- **Article 40**: Researcher data access (all VLOPs)
- **Article 42**: Semi-annual transparency reporting (all VLOPs)

Action required: Please update `internal/regulatory_addendum.json` to reflect these
requirements. Specifically:
1. `affected_platforms`: ["youtube", "meta", "tiktok"]
2. `article_reference`: ["Art. 34", "Art. 35", "Art. 40", "Art. 42"]
3. `non_affected_platforms`: ["reddit"] with rationale

The regulatory_addendum should reference the DSA regulation: Regulation (EU) 2022/2065.

Maya Patel | Legal Counsel | CreatorHub
"""),
        ("2025-10-25 14:30", "jordan.kim@creatorhub.com",
         "compliance-team@creatorhub.com",
         "RE: EU DSA VLOP Compliance Requirements — Action Required",
         """Maya,

Quick note on Reddit: I initially thought Reddit might qualify under DSA based on
older 2023 user count estimates that showed ~35M EU users. However, the current
EC designation list (2025) does not include Reddit, confirming they are below the
45M threshold.

So the affected platforms list is: YouTube, Meta (FB + IG), TikTok.
Reddit falls under standard DSA obligations only (Art. 14-18).

Jordan Kim | Product Manager | CreatorHub
"""),
        ("2025-10-26 09:15", "maya.patel@creatorhub.com",
         "compliance-team@creatorhub.com, jordan.kim@creatorhub.com",
         "RE: EU DSA VLOP Compliance Requirements — Confirmed",
         """Jordan,

Confirmed. Reddit is NOT a VLOP. The 2023 estimates were extrapolated and
the actual 2024-2025 EC designation process confirmed Reddit did not meet the 45M
EU active user threshold.

For our regulatory_addendum.json:
- affected_platforms: youtube, meta, tiktok (only these three)
- reddit: in non_affected_platforms with note about VLOP threshold

Key DSA articles for the three VLOPs:
- Art. 34: Risk assessment — requires annual systemic analysis of fundamental rights risks,
  civic discourse risks, psychological well-being risks, public security risks
- Art. 35: Mitigation — requires implementation of reasonable, proportionate measures
  to address Art. 34 risks
- Art. 40: Researcher access — vetted researchers must be given data access
- Art. 42: Transparency — semi-annual reports with enforcement statistics

Maya Patel | Legal Counsel | CreatorHub
"""),
        ("2025-10-28 10:00", "lin.wei@creatorhub.com",
         "compliance-team@creatorhub.com",
         "RE: EU DSA VLOP Compliance Requirements — Engine Update Required",
         """Team,

Based on Maya's analysis, I'm formally instructing the compliance team to:

1. Create `internal/regulatory_addendum.json` with:
   - regulation: "EU_DSA"
   - affected_platforms: ["youtube", "meta", "tiktok"]
   - article_reference: At minimum Art. 34 and Art. 35
   - non_affected_platforms: ["reddit"] with VLOP threshold rationale

2. Ensure `internal/eu_dsa_compliance.md` is updated (update_3 provides this)

3. Update SOP to reflect differentiated obligations

4. Cross-reference DSA Art. 34 risk categories with our existing platform policies

The regulatory_addendum.json is the authoritative compliance record for DSA
obligations in our engine. Other documents (email threads, analysis reports)
are supplementary only.

Lin Wei | Head of Compliance Engineering | CreatorHub
"""),
        ("2025-11-01 10:00", "legal@creatorhub.com",
         "compliance-team@creatorhub.com",
         "FINAL: EU DSA VLOP Compliance Requirements",
         """All,

This email formally transmits the EU DSA compliance requirements as the final
instructional document for update_3 compliance work.

VLOP Platforms (Art. 34/35 APPLY):
- YouTube (Google/Alphabet): VLOP designated April 2023
- Facebook (Meta Platforms): VLOP designated April 2023
- Instagram (Meta Platforms): VLOP designated April 2023
- TikTok (ByteDance): VLOP designated April 2023

NON-VLOP Platforms (Art. 14-18 only):
- Reddit: Does NOT meet 45M EU active user threshold

Key Articles for regulatory_addendum.json:
- Art. 34: Annual systemic risk assessment
- Art. 35: Risk mitigation measures
- Art. 40: Data access for researchers
- Art. 42: Transparency reporting obligations

Regulation reference: EU Digital Services Act, Regulation (EU) 2022/2065

Action: PolicyOps AI should create internal/regulatory_addendum.json with:
{
  "regulation": "EU_DSA",
  "affected_platforms": ["youtube", "meta", "tiktok"],
  "article_reference": ["Art. 34", "Art. 35"],
  "article_reference_extended": ["Art. 34", "Art. 35", "Art. 40", "Art. 42"]
}

Legal Team | CreatorHub
"""),
    ]

    for date, sender, recipients, subject, body in thread:
        emails.append(f"### From: {sender}\n")
        emails.append(f"**To**: {recipients}\n")
        emails.append(f"**Date**: {date}\n")
        emails.append(f"**Subject**: {subject}\n\n")
        emails.append(body)
        emails.append("\n---\n\n")

    # Add DSA compliance checklist details
    emails.append("## DSA Compliance Checklist — PolicyOps Engine\n\n")
    emails.append(
        "Based on the email thread above, the following items must be completed:\n\n"
    )
    items = [
        ("regulatory_addendum.json created", "Required", "In Progress"),
        ("affected_platforms: youtube, meta, tiktok", "Required", "Pending"),
        ("article_reference: Art. 34, Art. 35 minimum", "Required", "Pending"),
        ("non_affected_platforms: reddit", "Required", "Pending"),
        ("VLOP rationale documented", "Required", "Pending"),
        ("SOP updated for DSA obligations", "Recommended", "Not Started"),
        ("Art. 40 researcher access protocol", "Required for VLOPs", "Not Started"),
        ("Art. 42 transparency reporting template", "Required for VLOPs", "Not Started"),
    ]
    emails.append("| Item | Priority | Status |\n")
    emails.append("|---|---|---|\n")
    for item, priority, status in items:
        emails.append(f"| {item} | {priority} | {status} |\n")
    emails.append("\n")

    emails.append("## DSA Article 34 Risk Categories — Reference\n\n")
    emails.append(
        "Per Regulation (EU) 2022/2065, Article 34, VLOPs must assess the following "
        "systemic risks annually:\n\n"
    )
    risks = [
        ("1. Fundamental Rights", "Freedom of expression, human dignity, privacy, "
         "non-discrimination, consumer protection rights"),
        ("2. Civic Discourse", "Democratic participation, election integrity, "
         "political advertising transparency"),
        ("3. Psychological Well-Being", "Behavioral effects on users, "
         "addiction patterns, mental health impacts"),
        ("4. Public Security", "Terrorism facilitation, CSAM distribution, "
         "organized crime coordination, weapon trafficking"),
        ("5. Gender-Based Violence", "Content disproportionately affecting women, "
         "online harassment targeting women"),
        ("6. Minors' Rights", "Age-inappropriate content, grooming facilitation, "
         "educational harm, developmental impact"),
    ]
    for risk_id, desc in risks:
        emails.append(f"### {risk_id}\n\n{desc}\n\n")

    return "".join(emails)


def _gen_upd3_dsa_case_log(path: Path) -> None:
    """生成 DSA 合规案例日志（300行，填充 update_3 体量）。"""
    rng = random.Random(404)
    buf = io.StringIO()
    writer = csv.writer(buf)
    header = [
        "case_id", "platform", "dsa_article", "risk_category",
        "date", "severity", "status", "vlop_applicable",
        "assessment_type", "mitigation_required", "reporter",
        "notes"
    ]
    writer.writerow(header)
    dsa_articles = ["Art. 34", "Art. 35", "Art. 40", "Art. 42", "Art. 14", "Art. 15", "Art. 16"]
    risk_cats = ["fundamental_rights", "civic_discourse", "psychological_wellbeing",
                 "public_security", "gender_based_violence", "minors_rights"]
    for i in range(3001, 3501):
        plat = rng.choice(["youtube", "meta", "tiktok", "reddit"])
        article = rng.choice(dsa_articles)
        if plat == "reddit":
            article = rng.choice(["Art. 14", "Art. 15", "Art. 16"])
        risk = rng.choice(risk_cats)
        vlop = "yes" if plat != "reddit" else "no"
        sev = rng.choice(["low", "medium", "high"])
        assess_type = rng.choice(["annual_risk", "incident_response",
                                   "regulatory_inquiry", "self_assessment"])
        mitigation = rng.choice(["required", "not_required", "pending"])
        day = rng.randint(1, 30)
        month = rng.randint(10, 11)
        date_str = f"2025-{month:02d}-{day:02d}"
        writer.writerow([
            f"DSA-{i:05d}", plat, article, risk,
            date_str, sev, "open", vlop,
            assess_type, mitigation,
            rng.choice(["legal_team", "compliance_team", "external_auditor"]),
            f"DSA case {i}: {article} compliance check for {plat}. "
            f"Risk category: {risk}. VLOP applicable: {vlop}. "
            f"Assessment type: {assess_type}."
        ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(buf.getvalue(), encoding="utf-8")


def _gen_regulatory_checklist(path: Path) -> None:
    """生成监管审查清单（填充 u2 体量）。"""
    lines = ["# Moderation Operations Regulatory Review Checklist\n\n"]
    platforms = ["YouTube", "Meta", "TikTok", "Reddit"]
    categories = [
        "Violent Content", "Hate Speech", "Spam", "Misinformation",
        "CSAM", "Privacy Violations", "Harassment", "Terrorism",
        "Adult Content", "Dangerous Organizations", "Cybersecurity",
        "Coordinated Inauthentic Behavior", "Fraud", "Self-Harm Content",
        "Election Misinformation", "Health Misinformation",
        "Manipulated Media", "Copyright Violations",
        "Account Takeover", "Doxxing"
    ]
    review_criteria = [
        "Policy language is current and matches official documentation",
        "Enforcement thresholds are correctly configured",
        "Appeal timelines comply with platform SLA",
        "Human review escalation paths are defined",
        "Automated detection accuracy meets minimum threshold",
        "Cross-platform consistency verified",
        "Regulatory compliance (DSA/GDPR) documented",
        "Transparency report data incorporated",
        "Edge case handling procedures documented",
        "Audit trail requirements met"
    ]
    for plat in platforms:
        lines.append(f"## {plat}\n\n")
        for cat in categories:
            lines.append(f"### {cat}\n\n")
            for crit in review_criteria:
                status = "[ ]"
                lines.append(f"- {status} {crit}\n")
            lines.append("\n")
        lines.append("\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(lines), encoding="utf-8")


def _gen_eu_dsa_doc(path: Path) -> None:
    """生成 EU DSA 合规合成文档（~20k tokens）。"""
    content = """# EU Digital Services Act (DSA) Compliance Reference

*Regulation (EU) 2022/2065 of the European Parliament and of the Council*
*Effective: February 17, 2024 (full application for VLOPs: August 25, 2023)*

---

## Overview

The Digital Services Act (DSA) establishes a comprehensive regulatory framework for
digital services in the European Union. It introduces tiered obligations based on the
size and type of digital service, with the most stringent requirements applying to
**Very Large Online Platforms (VLOPs)** and **Very Large Online Search Engines (VLOSEs)**.

### VLOP Designation Threshold

A platform is designated as a VLOP if it has **45 million or more average monthly active
recipients** in the European Union (approximately 10% of the EU population). The European
Commission designates VLOPs and VLOSEs annually.

**Currently Designated VLOPs (as of 2024):**
- Facebook (Meta)
- Instagram (Meta)
- YouTube (Google/Alphabet)
- TikTok
- X (formerly Twitter)
- LinkedIn (Microsoft)
- Pinterest
- Snapchat
- Wikipedia
- Amazon Marketplace
- Booking.com
- AliExpress (Alibaba)
- Apple App Store
- Google Maps
- Google Play
- Google Shopping
- Zalando (challenged; court ruling pending)

**Important**: Reddit has NOT been designated as a VLOP as it does not meet the 45M EU
active user threshold. Reddit's EU user base is estimated well below this threshold.

---

## Key DSA Articles for Content Moderation

### Article 14 — Notice-and-Action Mechanisms
Platforms must provide easy-to-access mechanisms for users to notify illegal content.
Notifications must be processed without undue delay. Platforms must inform the notifier
of the decision and their right to appeal.

### Article 15 — Statement of Reasons
When a platform restricts content (removes, limits, suspends, etc.), it must provide
a clear and specific statement of reasons including:
- The policy basis for the decision
- The specific content affected
- Information about redress mechanisms

### Article 16 — Internal Complaint-Handling
Platforms must provide an internal complaint-handling system that is:
- Free of charge
- Accessible
- Concluded within a reasonable timeframe

### Article 17 — Out-of-Court Dispute Settlement
Users have the right to bring complaints to certified out-of-court dispute settlement bodies.
Platforms must cooperate in good faith and implement decisions of certified bodies.

### Article 18 — Trusted Flaggers
Platforms must prioritize notifications from "trusted flaggers" — expert organizations
certified by Digital Services Coordinators. Trusted flaggers receive expedited processing.

### Article 34 — Systemic Risk Assessment (VLOPs only)

**Applies to: YouTube, Meta, TikTok (and other designated VLOPs)**
**Does NOT apply to: Reddit (not a VLOP)**

VLOPs must conduct at least one annual systemic risk assessment covering:
1. **Fundamental Rights Risks**: Risks to freedom of expression, human dignity, privacy,
   non-discrimination, and consumer protection.
2. **Civic Discourse and Electoral Processes**: Risks to democratic participation.
3. **Psychological Well-Being**: Risks related to behavioral effects on users.
4. **Public Security**: Risks of content facilitating terrorism, CSAM, organized crime.
5. **Gender-Based Violence**: Specific assessment of risks to women.
6. **Minors' Rights**: Specific assessment of content risks to children.

The assessment must consider:
- The design of algorithmic systems and their potential amplification of harmful content
- Accessibility of content moderation tools for users
- Interface design and targeted advertising
- The interaction between services and how risks may be amplified across platforms

Risk assessments must be provided to the European Commission and Digital Services Coordinators.

### Article 35 — Risk Mitigation Measures (VLOPs only)

**Applies to: YouTube, Meta, TikTok (and other designated VLOPs)**
**Does NOT apply to: Reddit (not a VLOP)**

VLOPs must put in place reasonable, proportionate mitigation measures addressing the
risks identified in Article 34 assessments. Measures may include:

1. **Content Moderation Enhancements**: Additional human review capacity, faster response
   times for high-risk content, specialized review teams.
2. **Algorithmic Adjustments**: Modifications to recommendation systems to reduce
   amplification of harmful content.
3. **User Empowerment Tools**: Providing users with options to customize their content
   experience, access content explanations, and report concerns.
4. **Transparency Measures**: Publishing detailed information about content moderation
   decisions, appeals, and outcomes.
5. **Crisis Protocols**: Emergency response procedures for acute crises that may generate
   disinformation or harmful content at scale.
6. **Researcher Access**: Ensuring compliance with Article 40 data access requirements.

### Article 40 — Data Access for Researchers (VLOPs only)

VLOPs and VLOSEs must provide vetted researchers with access to platform data necessary
for studying systemic risks. Requests are processed by Digital Services Coordinators.

Requirements:
- Data access protocols published and maintained
- Researcher vetting process documented
- Annual reporting on data access requests granted/denied
- Privacy-preserving techniques applied to shared data

### Article 42 — Transparency Reporting (VLOPs only)

VLOPs must publish detailed transparency reports at least twice per year, including:
1. Number of content moderation decisions (removals, restrictions, suspensions, bans)
2. Number of notices received under Article 14
3. Number of appeals filed and outcomes
4. Number of complaints to out-of-court settlement bodies
5. Human review capacity and qualifications
6. Automated content moderation tools used
7. Fundamental rights assessments

---

## DSA Compliance Checklist for VLOPs

### YouTube (VLOP)
- [ ] Art. 34 systemic risk assessment: annual, documented
- [ ] Art. 35 mitigation measures: implemented and proportionate
- [ ] Art. 40 researcher data access: protocol established
- [ ] Art. 42 transparency reports: semi-annual publication
- [ ] Art. 14-18 notice/action/complaint: user-facing systems compliant

### Meta (Facebook + Instagram, VLOP)
- [ ] Art. 34 systemic risk assessment: annual, documented
- [ ] Art. 35 mitigation measures: implemented and proportionate
- [ ] Art. 40 researcher data access: protocol established
- [ ] Art. 42 transparency reports: semi-annual publication
- [ ] Art. 14-18 notice/action/complaint: user-facing systems compliant

### TikTok (VLOP)
- [ ] Art. 34 systemic risk assessment: annual, documented
- [ ] Art. 35 mitigation measures: implemented and proportionate
- [ ] Art. 40 researcher data access: protocol established
- [ ] Art. 42 transparency reports: semi-annual publication
- [ ] Art. 14-18 notice/action/complaint: user-facing systems compliant

### Reddit (NOT a VLOP — standard DSA obligations only)
- [ ] Art. 14-18 notice/action/complaint: user-facing systems compliant
- [ ] Art. 15 statement of reasons: implemented
- [ ] Art. 16 internal complaint-handling: free, accessible, timely

---

## Implementation Timeline for CreatorHub

As a compliance engine serving content on VLOP-designated platforms, CreatorHub
must ensure its policy mappings reflect the additional DSA requirements for
YouTube, Meta, and TikTok. The following internal milestones apply:

| Milestone | Target Date | Status |
|---|---|---|
| VLOP platform identification complete | 2025-Q3 | ✓ Complete |
| Art. 34 risk category mapping | 2025-Q4 | In Progress |
| Art. 35 mitigation measures integration | 2026-Q1 | Planned |
| Art. 40 data access protocol | 2026-Q1 | Planned |
| Art. 42 reporting templates | 2025-Q4 | In Progress |
| Reddit DSA standard compliance verification | 2025-Q4 | In Progress |

---

## Relevant DSA Recitals for Content Moderation

**Recital 47**: Platforms should not be required to monitor content proactively, but
must act expeditiously upon obtaining actual knowledge of illegal content.

**Recital 52**: The statement of reasons obligation is essential for users to understand
decisions and exercise their right to redress.

**Recital 80**: Risk assessments must be thorough, analytical, and structured to ensure
that VLOPs can effectively identify and mitigate systemic risks to fundamental rights.

**Recital 84**: Mitigation measures should be effective, proportionate, and non-discriminatory,
with particular attention to the protection of fundamental rights of users.

**Recital 107**: The designation of trusted flaggers should be based on objective criteria
ensuring their independence, expertise, and diligence.

---

*Source: Regulation (EU) 2022/2065 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R2065*
*DSA Entry into Force: November 16, 2022*
*Full Application Date: February 17, 2024*
*VLOP Obligations: August 25, 2023*
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _gen_dsa_articles_reference(path: Path) -> None:
    """生成 DSA 条款对照表 JSON（填充 u3 体量）。"""
    articles = []
    dsa_data = [
        ("Art. 1", "Subject Matter and Scope", "Defines the scope and objectives of the DSA"),
        ("Art. 2", "Definitions", "Key definitions including 'illegal content', 'recipient', 'trader'"),
        ("Art. 14", "Notice-and-Action Mechanisms", "Requirements for user notification of illegal content"),
        ("Art. 15", "Statement of Reasons", "Mandatory explanation for content restrictions"),
        ("Art. 16", "Internal Complaint-Handling System", "Free, accessible internal appeals process"),
        ("Art. 17", "Out-of-Court Dispute Settlement", "Right to bring complaints to certified bodies"),
        ("Art. 18", "Trusted Flaggers", "Priority processing for certified expert organizations"),
        ("Art. 34", "Risk Assessment by Very Large Online Platforms",
         "Annual systemic risk assessment covering fundamental rights, civic discourse, psychological well-being"),
        ("Art. 35", "Mitigation of Risks",
         "Reasonable and proportionate measures to address Art. 34 risks; algorithmic adjustments, human review"),
        ("Art. 36", "Crisis Response Mechanism", "Emergency protocols during crisis situations"),
        ("Art. 37", "Independent Audit", "Annual third-party audit of risk assessments and mitigation measures"),
        ("Art. 38", "Recommender Systems", "Transparency and user control over recommendation algorithms"),
        ("Art. 39", "Advertising Transparency", "Requirements for online advertising databases"),
        ("Art. 40", "Data Access for Researchers", "Vetted researcher access to VLOP data for systemic risk research"),
        ("Art. 42", "Transparency Reporting", "Semi-annual transparency reports including moderation statistics"),
        ("Art. 45", "Codes of Conduct", "Voluntary codes at European level for DSA implementation"),
        ("Art. 46", "Crisis Protocols", "Commission can activate emergency protocols for acute crises"),
        ("Art. 74", "Penalties", "Infringement fines up to 6% of global annual turnover"),
        ("Art. 82", "Right to Judicial Remedy", "Users' right to judicial redress for DSA violations"),
        ("Art. 86", "Entry into Force", "Regulation enters into force 20 days after publication"),
    ]
    for ref, title, desc in dsa_data:
        articles.append({
            "article": ref,
            "title": title,
            "description": desc,
            "applies_to_vlop": ref in ["Art. 34", "Art. 35", "Art. 36", "Art. 37",
                                        "Art. 38", "Art. 39", "Art. 40", "Art. 42"],
            "applies_to_reddit": ref not in ["Art. 34", "Art. 35", "Art. 36", "Art. 37",
                                              "Art. 38", "Art. 39", "Art. 40", "Art. 42"],
        })

    obj = {
        "regulation": "EU Digital Services Act",
        "regulation_ref": "Regulation (EU) 2022/2065",
        "schema_version": "1.0",
        "_source_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R2065",
        "vlop_threshold_eu_users": 45000000,
        "vlop_platforms": ["youtube", "meta_facebook", "meta_instagram", "tiktok"],
        "non_vlop_platforms": ["reddit"],
        "vlop_non_vlop_rationale": {
            "reddit": "Reddit does not meet the 45 million EU active user threshold for VLOP designation",
            "source_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R2065"
        },
        "articles": articles
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()
    gen_platform_docs()
    gen_extended_platform_docs()
    gen_internal_docs()
    gen_decoy_files()
    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = (
        "Content moderation policy engine for YouTube/Meta/TikTok/Reddit — "
        "16 exec_check rounds, 3 updates (incl. TikTok appeal supersede), "
        "5 preference rules P1-P5, difficulty vectors V1/V2/V3/V4/V5/V6/V7/V8/V9/V10. "
        "Real sources: YouTube strike system "
        "(https://support.google.com/youtube/answer/2802032?hl=en); "
        "Meta enforcement "
        "(https://transparency.meta.com/enforcement/taking-action/restricting-accounts/); "
        "TikTok Q1 2025 "
        "(https://www.tiktok.com/transparency/en/community-guidelines-enforcement-2025-1); "
        "Reddit NY S895B report "
        "(https://ag.ny.gov/sites/default/files/social-media-policy-report/2025-q3-reddit-inc-policy.pdf)."
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
    pe = WS / "policy_engine"
    total = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                for p in pe.rglob("*") if p.is_file())
    # 加上系统文件
    sys_tok = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                  for p in WS.glob("*.md") if p.is_file())
    total += sys_tok
    sess_tok = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                   for p in SESS.glob("*.jsonl"))
    upd_tok = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                  for p in UPD.rglob("*") if p.is_file())
    print(f"[prd2] workspace tokens ~{total + sess_tok:,} | sessions ~{sess_tok:,} | updates ~{upd_tok:,}")
    print(f"[prd2] policy_engine files ~{total:,} tokens")
    print(f"[prd2] built at {DATASET}")


if __name__ == "__main__":
    main()
