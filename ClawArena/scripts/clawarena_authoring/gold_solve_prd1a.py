#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_prd1a.py — prd1a 可解性审计（金标自检）。

在 workspace 的临时副本上模拟 update 生效后的状态，写出每一轮的「正确产物」，
然后运行全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再做一组反例（错误产物）抽样，断言 check 能 FAIL（不过松）。

用途：证明每个 ground-truth 可由真实数据解出、check 不过严也不过松。
运行：python scripts/clawarena_authoring/gold_solve_prd1a.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "prd1a"
UPD = DS / "openclaw" / "updates" / "prd1a"
SCRIPTS = DS / "eval" / "prd1a" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/prd1a_gold_ws")


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # 应用 Update 1 workspace 文件
    upd1_ws = UPD / "upd1_workspace"
    shutil.copy(
        upd1_ws / "ftc_penalty_offenses_brief_v1.md",
        GOLD / "regulatory" / "ftc_penalty_offenses_brief_v1.md",
    )
    # Update 1 的 CSV 数据文件
    upd1_csv = upd1_ws / "ftc_670_companies_penalty_offenses.csv"
    if upd1_csv.exists():
        (GOLD / "research").mkdir(parents=True, exist_ok=True)
        shutil.copy(upd1_csv, GOLD / "research" / "ftc_670_companies_penalty_offenses.csv")
    # 应用 Update 2 workspace 文件
    upd2_ws = UPD / "upd2_workspace"
    shutil.copy(
        upd2_ws / "ftc_enforcement_cases_2024.md",
        GOLD / "regulatory" / "ftc_enforcement_cases_2024.md",
    )
    shutil.copy(
        upd2_ws / "green_claims_test_reports.md",
        GOLD / "research" / "green_claims_test_reports.md",
    )
    upd2_csv = upd2_ws / "clinical_evidence_assessment_database.csv"
    if upd2_csv.exists():
        shutil.copy(upd2_csv, GOLD / "research" / "clinical_evidence_assessment_database.csv")
    return GOLD


def _w(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# 金标产物写出
# --------------------------------------------------------------------------- #
def solve(ws: Path) -> None:
    # 创建必要目录
    for d in ("reports", "policies", "templates", "training", "final"):
        (ws / d).mkdir(parents=True, exist_ok=True)

    # --- Q1: compliance_issues_q1.json ---
    # 6 个禁用限定语 + 至少 2 条其他违规；共 8 条
    _wj(ws / "reports" / "compliance_issues_q1.json", {
        "schema_version": "1.0",
        "issues": [
            {
                "issue_id": "CI-001",
                "claim_text": "Clinically demonstrated to support immune function with our 30B CFU probiotic blend",
                "violated_rule": "Proof claim without product-specific RCT; 'clinically demonstrated' requires adequate substantiation",
                "citable_section": "FTC Health Products Compliance Guidance (Dec 2022)",
                "ftc_citation": "16 CFR §255.1",
                "severity": "high",
            },
            {
                "issue_id": "CI-002",
                "claim_text": "May help support digestive health and comfort",
                "violated_rule": "'may' is an insufficient qualifier per FTC Health Products Compliance Guidance",
                "citable_section": "FTC Health Products Compliance Guidance (Dec 2022)",
                "ftc_citation": "16 CFR §255.1",
                "severity": "high",
            },
            {
                "issue_id": "CI-003",
                "claim_text": "Based on promising preliminary clinical results, ProBio+ supports your immune system",
                "violated_rule": "'promising' and 'preliminary' are prohibited qualifiers per FTC guidance",
                "citable_section": "FTC Health Products Compliance Guidance (Dec 2022)",
                "ftc_citation": "16 CFR §255.1",
                "severity": "high",
            },
            {
                "issue_id": "CI-004",
                "claim_text": "B-vitamins scientifically proven to support energy metabolism",
                "violated_rule": "'scientifically proven' without adequate substantiation is a penalty offense under Notice of Penalty Offenses",
                "citable_section": "FTC Health Products Compliance Guidance (Dec 2022)",
                "ftc_citation": "16 CFR §255.1",
                "severity": "high",
            },
            {
                "issue_id": "CI-005",
                "claim_text": "Initial studies show remarkable outcomes for gut health",
                "violated_rule": "'initial' is a prohibited qualifier per FTC Health Products Compliance Guidance",
                "citable_section": "FTC Health Products Compliance Guidance (Dec 2022)",
                "ftc_citation": "16 CFR §255.1",
                "severity": "high",
            },
            {
                "issue_id": "CI-006",
                "claim_text": "Our pilot study found ProBio+ reduces inflammation markers",
                "violated_rule": "'pilot' is a prohibited qualifier; pilot studies without control groups are insufficient",
                "citable_section": "FTC Health Products Compliance Guidance (Dec 2022)",
                "ftc_citation": "16 CFR §255.1",
                "severity": "high",
            },
            {
                "issue_id": "CI-007",
                "claim_text": "As seen on Dr. Wellness Network (undisclosed paid endorsement)",
                "violated_rule": "Material connection between endorser and advertiser not disclosed; undisclosed paid endorsement",
                "citable_section": "16 CFR Part 255 Endorsement Guides (2023)",
                "ftc_citation": "16 CFR §255.5",
                "severity": "high",
            },
            {
                "issue_id": "CI-008",
                "claim_text": "Doctor-formulated for maximum bioavailability",
                "violated_rule": "'Doctor-formulated' implies expert endorsement requiring disclosure and adequate substantiation",
                "citable_section": "FTC Health Products Compliance Guidance (Dec 2022)",
                "ftc_citation": "16 CFR §255.3",
                "severity": "high",
            },
        ],
    })

    # --- Q2: disclosure_check_q2.json ---
    _wj(ws / "reports" / "disclosure_check_q2.json", {
        "schema_version": "1.0",
        "issues": [
            {
                "draft_id": "Draft_A",
                "disclosure_adequate": False,
                "material_connection_type": "monetary compensation plus free product",
                "issue_description": (
                    "@drwellnessnetwork receives $5,000 plus 6 months of free product. "
                    "Per 16 CFR §255.5, a connection between the endorser and the seller of the "
                    "advertised product that might materially affect the weight or credibility of the "
                    "endorsement must be clearly and conspicuously disclosed. No disclosure appears "
                    "in the proposed post."
                ),
                "recommendation": "Add '#ad' or 'Ad:' at the very BEGINNING of the post caption before any other content.",
                "ftc_citation": "16 CFR §255.5",
                "estimated_penalty_per_violation": 51744,
            },
            {
                "draft_id": "Draft_B",
                "disclosure_adequate": False,
                "material_connection_type": "gifted product plus affiliate commission",
                "issue_description": (
                    "@healthcoach_jay receives gifted product and affiliate commission. "
                    "Disclosure '#giftedpartnership' buried at end of hashtag list is insufficient per "
                    "FTC .com Disclosures (2013) — disclosures in hashtag chains at the end of captions "
                    "may be missed by consumers."
                ),
                "recommendation": "Move '#ad' to the very beginning of the caption; remove reliance on hashtag-only disclosure.",
                "ftc_citation": "16 CFR §255.5",
                "estimated_penalty_per_violation": 51744,
            },
            {
                "draft_id": "Draft_C",
                "disclosure_adequate": True,
                "material_connection_type": "monetary compensation",
                "issue_description": "@nutritionbyjessica uses 'Ad:' at the very beginning of each caption. This is compliant.",
                "recommendation": "No change required. Maintain current disclosure format.",
                "ftc_citation": "16 CFR §255.5",
                "estimated_penalty_per_violation": 0,
            },
        ],
    })

    # --- Q3: evidence_assessment_q3.json ---
    _wj(ws / "reports" / "evidence_assessment_q3.json", {
        "schema_version": "1.0",
        "claims": [
            {
                "claim_id": "EV-001",
                "claim_text": "ProBio+ supports immune health (Lactobacillus rhamnosus GG component)",
                "evidence_type": "RCT",
                "meets_ftc_standard": True,
                "basis": "LGG has 3 randomized, controlled human clinical trials demonstrating statistically significant immune markers improvement. This meets the FTC gold standard of randomized, controlled human clinical testing (RCT).",
            },
            {
                "claim_id": "EV-002",
                "claim_text": "ProBio+ supports digestive comfort (Lactobacillus acidophilus NCFM component)",
                "evidence_type": "RCT",
                "meets_ftc_standard": True,
                "basis": "L. acidophilus NCFM has 2 RCTs demonstrating GI comfort improvement. Meets FTC RCT standard.",
            },
            {
                "claim_id": "EV-003",
                "claim_text": "Bifidobacterium lactis Bi-07 supports immune function",
                "evidence_type": "in vitro study",
                "meets_ftc_standard": False,
                "basis": "Bi-07 evidence consists of 1 pilot study (n=45, no control group) and 2 in vitro cell studies. Per FTC Health Products Compliance Guidance (Dec 2022), in vitro studies and pilot studies without control groups cannot standalone substantiate health claims for human use.",
            },
            {
                "claim_id": "EV-004",
                "claim_text": "Lactobacillus plantarum 299v supports immune health",
                "evidence_type": "animal study",
                "meets_ftc_standard": False,
                "basis": "L. plantarum 299v evidence consists of 1 animal study and 1 in vitro study. Animal studies do not demonstrate efficacy in humans and cannot standalone substantiate health claims per FTC guidance.",
            },
            {
                "claim_id": "EV-005",
                "claim_text": "ProBio+ Daily clinically demonstrated to support immune function (full blend)",
                "evidence_type": "pilot study",
                "meets_ftc_standard": False,
                "basis": "The full blend lacks a product-specific RCT. Individual strain RCTs (LGG, NCFM) do not substitute for a finished-product trial. Per FTC Health Products Compliance Guidance, the finished product formulation must be tested.",
            },
        ],
    })

    # --- Q4: prohibited_terms_q4.md ---
    _w(ws / "reports" / "prohibited_terms_q4.md", """\
# Prohibited Qualifier Replacement Guide — ProBio+ Daily Press Release

## Health Claim Prohibited Qualifiers

### Replacement Recommendations Per FTC Health Products Compliance Guidance (Dec 2022)

| original_sentence | prohibited_term | replacement_sentence | severity | ftc_basis |
|---|---|---|---|---|
| "May help support digestive health and comfort" | may | "Supports digestive health and comfort, as demonstrated in 2 randomized controlled trials" | high | Health Products Compliance Guidance (Dec 2022) |
| "ProBio+ helps maintain your gut microbiome" | helps | "ProBio+ contains live cultures that contribute to normal gut microbiome balance" | high | Health Products Compliance Guidance (Dec 2022) |
| "Based on promising preliminary clinical results, ProBio+ supports your immune system" | promising | "In a 12-week randomized trial of 120 healthy adults, LGG supplementation significantly improved immune markers" | high | Health Products Compliance Guidance (Dec 2022) |
| "Preliminary studies show ProBio+ reduces inflammation" | preliminary | "Remove claim; preliminary evidence does not meet FTC substantiation standard" | high | Health Products Compliance Guidance (Dec 2022) |
| "Initial studies show remarkable outcomes for gut health" | initial | "Remove claim; initial findings without control groups are insufficient per FTC guidance" | high | Health Products Compliance Guidance (Dec 2022) |
| "Our pilot study found ProBio+ reduces inflammation markers" | pilot | "Remove claim; pilot studies lack control groups required by FTC Health Products Compliance Guidance" | high | Health Products Compliance Guidance (Dec 2022) |
""")

    # --- Q5: review_management_policy_q5.md ---
    _w(ws / "policies" / "review_management_policy_q5.md", """\
# ProBio+ Daily — Review Management Policy

## Overview

This policy governs all consumer review collection and management activities for ProBio+ Daily
under 16 CFR Part 465 (Consumer Reviews and Testimonials Rule, effective October 21, 2024).
The civil penalty for violations is $51,744 per violation (2024 adjusted rate).

## Prohibited Fake Reviews

### Verbatim Prohibition — 16 CFR §465.2(a)

It is an unfair or deceptive act or practice and a violation of this part for a business to
write, create, or sell a consumer review, consumer testimonial, or celebrity testimonial that
materially misrepresents, expressly or by implication:
(1) That the reviewer or testimonialist exists;
(2) That the reviewer or testimonialist used or otherwise had experience with the product,
service, or business; or
(3) The reviewer's or testimonialist's experience with the product, service, or business.

## Prohibited Review Suppression

### Verbatim Prohibition — 16 CFR §465.7

It is prohibited to use unfounded or groundless legal threat, a physical threat, intimidation,
or a public false accusation directed at a reviewer or potential reviewer, in an attempt to:
(1) Prevent a review or any portion thereof from being written or created; or
(2) Cause a review or any portion thereof to be removed.

### Prohibited Conduct Examples

VitaCore personnel must NOT:
- Send cease-and-desist letters without legitimate legal basis to reviewers
- Threaten legal action against reviewers for opinions
- Publicly accuse reviewers of dishonesty to discourage further reviews
- Use any form of intimidation to suppress negative reviews

## Prohibited Actions List (§§465.2–465.8)

- §465.2: Writing, creating, or procuring fake or false consumer reviews
- §465.4: Purchasing reviews conditioned on positive content
- §465.5: Company insiders (officers, managers, employees, agents, immediate family)
  writing reviews without clearly disclosing their material connection to VitaCore
- §465.6: Operating a controlled review website without conspicuous disclosure of company control
- §465.7: Suppressing reviews through threats, intimidation, or false accusations
- §465.8: Buying or procuring fake social media indicators (followers, likes, views)

## Insider Review Disclosure Requirement (§465.5)

Per §465.5, any VitaCore employee, officer, manager, agent, or their immediate family member
who posts a review of ProBio+ Daily or any VitaCore product MUST prominently disclose their
material connection (e.g., "I am a [role] at VitaCore Inc."). Failure to disclose constitutes
a violation subject to $51,744 civil penalty per occurrence.

## Internal Approval Workflow

1. All influencer or paid review programs must be reviewed by Compliance (Dr. Santos) before launch.
2. Any cease-and-desist letter related to reviews requires sign-off from General Counsel (Sarah Chen).
3. Review platform moderation decisions must be documented and reviewed monthly.

## Disclosure Templates

For company insiders posting reviews: "Note: I am an employee/officer at VitaCore Inc. and
received this product as part of my employment."
""")

    # --- Q6: label_compliance_q6.json ---
    _wj(ws / "reports" / "label_compliance_q6.json", {
        "schema_version": "1.0",
        "mia_claim_present": True,
        "mia_standard_met": False,
        "supporting_facts": [
            "ProBio+ Daily's front panel states 'Made in USA'.",
            "Key probiotic strains are sourced from Chr. Hansen A/S (Høje-Taastrup, Denmark), a Danish company.",
            "Chr. Hansen's probiotic strains (LGG, NCFM, Bi-07, 299v) are the core functional ingredients.",
            "16 CFR Part 323 'all or virtually all' standard requires all significant components to be of US origin.",
            "Danish-sourced probiotic strains are 'significant' components — they define the product's primary health benefit.",
            "15% imported packaging components add additional concern.",
            "Conclusion: The 'all or virtually all' standard is NOT met. A qualified claim is required.",
        ],
        "recommendation": "Replace unqualified 'Made in USA' with qualified claim: 'Encapsulated in the USA from domestic and imported ingredients.' Remove unqualified 'Made in USA' from front panel until supply chain is restructured.",
        "reference_cases": [
            {
                "case": "Kubota North America Corporation",
                "date": "January 2024",
                "penalty": "$2 million",
                "penalty_amount_usd": 2000000,
                "rule": "16 CFR Part 323",
                "note": "LARGEST Made in USA penalty ever imposed. Kubota labeled tractors as 'Made in USA' when components were imported.",
            }
        ],
    })

    # --- Q7: slack_synthesis_q7.json ---
    _wj(ws / "reports" / "slack_synthesis_q7.json", {
        "conflict_identified": True,
        "correct_position": (
            "Sarah Chen's position is correct. The $51,744 per violation figure is the 2024 "
            "adjusted civil penalty rate under 16 CFR Part 465 (Consumer Reviews and Testimonials "
            "Rule). 'May help support' is explicitly listed as a prohibited qualifier in FTC Health "
            "Products Compliance Guidance. The 'results not typical' safe harbor was abolished in "
            "the 2009 revision of the Endorsement Guides and does not exist under current law."
        ),
        "correct_penalty_usd": 51744,
        "discarded_position": (
            "Mike Torres' position is incorrect on all three points. (1) The $45,000 penalty figure "
            "comes from the non-authoritative bot summary (DECOY file), not from the regulatory text. "
            "The actual 2024 rate per 16 CFR Part 465 is $51,744. (2) 'May help support' cannot rescue "
            "an inadequately substantiated claim — the FTC specifically identifies 'may' as an "
            "insufficient qualifier. (3) The 'results not typical' safe harbor no longer exists."
        ),
        "safe_harbor_status": (
            "ABOLISHED. The 'results not typical' safe harbor existed in the FTC's 1980 Endorsement "
            "Guides but was abolished in the 2009 revision. It does not appear in the current 2023 "
            "Endorsement Guides (effective July 26, 2023). Relying on this disclaimer provides no "
            "protection from FTC enforcement action."
        ),
    })

    # --- Q8: revised_compliance_q8.json ---
    # After Update 1 — CEO withdrew 'clinically demonstrated' language but FTC standards unchanged
    _wj(ws / "reports" / "revised_compliance_q8.json", {
        "schema_version": "1.0",
        "claims": [
            {
                "claim_id": "RC-001",
                "claim_text": "Clinically demonstrated to support immune function (REMOVED from v2)",
                "evidence_type": "No product-specific RCT for full blend",
                "original_status": "VIOLATION — proof claim without adequate RCT",
                "revised_status": "REMOVED from draft v2 per CEO Update 1. FTC standard for 'clinically demonstrated' still requires product-specific RCT — CEO withdrawal is procedural, not a finding of compliance.",
                "change_reason": "CEO Park formally withdrew this claim via Feishu (Update 1). The claim was removed from press_release_draft_v2.md. This does not alter the underlying FTC standard.",
                "ftc_citation": "16 CFR §255.1",
            },
            {
                "claim_id": "RC-002",
                "claim_text": "Supports immune health based on our proprietary blend (revised language in v2)",
                "evidence_type": "Partial RCT (strain-specific, not product-specific)",
                "original_status": "UNDER REVIEW",
                "revised_status": "STILL REQUIRES SUBSTANTIATION — 'proprietary blend' framing does not excuse need for product-level RCT per FTC Health Products Compliance Guidance.",
                "change_reason": "CEO proposed this as replacement language. However, FTC guidance requires substantiation for the specific finished product, not just individual ingredients.",
                "ftc_citation": "16 CFR §255.1",
            },
            {
                "claim_id": "RC-003",
                "claim_text": "Bifidobacterium lactis Bi-07 immune support (in vitro evidence)",
                "evidence_type": "in vitro study",
                "original_status": "VIOLATION — in vitro evidence insufficient per FTC",
                "revised_status": "STILL NON-COMPLIANT — in vitro evidence remains insufficient per FTC Health Products Compliance Guidance regardless of draft revision.",
                "change_reason": "No new evidence presented. In vitro studies cannot standalone substantiate health claims.",
                "ftc_citation": "16 CFR §255.1",
            },
            {
                "claim_id": "RC-004",
                "claim_text": "Doctor-formulated claim (still under review in v2)",
                "evidence_type": "Expert endorsement — material connection review pending",
                "original_status": "UNDER REVIEW per initial external audit conditional permission",
                "revised_status": "STILL UNDER REVIEW — initial Compliance Counsel LLC conditional permission remains in effect pending Update 2 revised opinion.",
                "change_reason": "No change from Update 1 for this claim. Awaiting revised audit opinion.",
                "ftc_citation": "16 CFR §255.3",
            },
        ],
    })

    # --- Q9: disclosure_script_q9.md ---
    _w(ws / "templates" / "disclosure_script_q9.md", """\
# Influencer Disclosure Script Templates — VitaCore ProBio+ Campaign

These templates implement 16 CFR §255.5 (effective July 26, 2023) material connection disclosure
requirements. The §255.5 material connection definition requires disclosure when there exists
"a connection between the endorser and the seller of the advertised product that might materially
affect the weight or credibility of the endorsement."

## Video Script Templates

### Video Oral + On-Screen Disclosure (Compliant Format)

**Verbal script (first 30 seconds):**
"[VERBAL, spoken at beginning of video] Hi everyone — this video is sponsored by VitaCore.
I received payment and free product to create this content. With that disclosure made..."
[continue with product content]

**On-screen text overlay:**
"[ON SCREEN TEXT during entire review segment] PAID PARTNERSHIP WITH VITACORE"

## Social Media Post Templates

### Social Media Post — Compliant Format

**Template:**
"Ad: I've been taking ProBio+ Daily for 8 weeks as part of a paid partnership with VitaCore.
[product content follows] #ProBioPlus #VitaCore #wellness"

Note: '#ad' or 'Ad:' MUST appear at the BEGINNING of the post caption, before any substantive
content begins. This is the only compliant placement per FTC .com Disclosures guidance (2013).

### Alternative Compliant Format:
"#ad Partnered with @VitaCore — my honest 8-week review of ProBio+ Daily..."

## Hashtag-Only Format — INSUFFICIENT PER FTC GUIDANCE

**The following format is EXPLICITLY INSUFFICIENT and must NOT be used:**
"I've been loving ProBio+ Daily for gut health support! [content] #health #wellness #probiotics
#ad #gifted #sponsored #VitaCore"

**Why it is insufficient**: Disclosures buried at the end of hashtag lists may be missed by
consumers who do not read the full caption. FTC guidance requires that disclosures be difficult
to miss and easily understandable by ordinary consumers. Placement in a hashtag chain fails
this standard. This format is insufficient per FTC guidance.

---
Reference: 16 CFR Part 255 Endorsement Guides, effective July 26, 2023.
""")

    # --- Q10: audit_integration_q10.json ---
    _wj(ws / "reports" / "audit_integration_q10.json", {
        "schema_version": "1.0",
        "valid_recommendations": [
            "Remove 'clinically demonstrated to support immune function' — requires product-specific RCT.",
            "Treat 'may help support immune function' as a warning — 'may' is an insufficient qualifier.",
            "Made in USA claim is at high risk — Danish Chr. Hansen probiotic strains as key functional components likely fail the 'all or virtually all' standard.",
            "Doctor-formulated claim requires physician verification, adequate substantiation, and material connection disclosure.",
        ],
        "superseded_recommendations": [
            "Reference to 2009 Endorsement Guides §255.1(b) 'results not typical' safe harbor as providing protection for atypical testimonials.",
        ],
        "reason_superseded": [
            "The 'results not typical' safe harbor was ABOLISHED in the 2009 revision of the Endorsement Guides (the same revision the counsel cited). It does not exist in the current 2023 Guides (effective July 26, 2023). Any legal opinion relying on this safe harbor as currently valid is based on outdated guidance. The external auditors themselves noted this was included in error and retracted it in their revised opinion v2.",
        ],
    })

    # --- Q11: green_claims_q11.json ---
    _wj(ws / "reports" / "green_claims_q11.json", {
        "schema_version": "1.0",
        "claims": [
            {
                "claim": "Biodegradable Capsule Shells",
                "compliant": False,
                "qualification_required": True,
                "basis": "Per 16 CFR §260.8, unqualified biodegradable claims require complete breakdown within one year after customary disposal. ASTM D5338 and ISO 14855 test results show BioTherm HDPE capsule shells achieve only 1.8-2.3% degradation in 12 months under any disposal conditions. The one-year standard is NOT met. The unqualified claim is deceptive.",
                "ftc_citation": "16 CFR §260.8",
            },
            {
                "claim": "Eco-Friendly Packaging",
                "compliant": False,
                "qualification_required": True,
                "basis": "Per 16 CFR §260.1, unqualified general environmental benefit claims ('eco-friendly', 'green', 'sustainable') imply comprehensive environmental benefits rarely achievable. The packaging mix (HDPE bottle, paperboard carton, foil liner) has mixed environmental profiles. The unqualified claim must be replaced with a specific qualified claim identifying what environmental benefit is actually provided.",
                "ftc_citation": "16 CFR §260.1",
            },
            {
                "claim": "Recyclable Packaging",
                "compliant": False,
                "qualification_required": True,
                "basis": "Per 16 CFR §260.12, unqualified 'recyclable' claims require 60% of consumers/communities to have access to relevant recycling facilities. The foil liner component is recyclable in only approximately 15% of US communities, which falls well below the 60% threshold. The complete packaging unit does not qualify for an unqualified recyclable claim. A qualified claim limited to the bottle and carton is permissible.",
                "ftc_citation": "16 CFR §260.12",
            },
        ],
    })

    # --- Q12: final_compliance_q12.json ---
    _wj(ws / "reports" / "final_compliance_q12.json", {
        "schema_version": "1.0",
        "update_source": "email_revised_audit_v2",
        "doctor_formulated_requires_substantiation": True,
        "superseded_items": [
            "Initial Compliance Counsel LLC opinion (May 28, 2026) conditional permission for 'Doctor-formulated' claim — now withdrawn and superseded by revised opinion v2.",
            "Initial opinion reference to 2009 Endorsement Guides 'results not typical' safe harbor — formally retracted in revised opinion v2.",
            "CEO Park's informal Feishu guidance that 'supports immune health based on our proprietary blend' may be acceptable without formal substantiation — overridden by revised opinion confirming FTC standards cannot be superseded by internal officer guidance.",
        ],
        "active_items": [
            "Remove 'clinically demonstrated to support immune function' — no product-specific RCT.",
            "Remove 'may help support' and all other prohibited qualifier language (may, helps, promising, preliminary, initial, pilot).",
            "Doctor-formulated requires substantiation — substantial competent scientific evidence + physician involvement verification + material connection disclosure.",
            "Biodegradable Capsule Shells: requires independent testing documentation showing one-year breakdown per §260.8, or remove claim.",
            "Made in USA: qualified claim required; Danish probiotic strains fail 'all or virtually all' standard.",
            "All influencer posts must begin with '#ad' or 'Ad:'; platform Paid Partnership tool alone is insufficient.",
            "Results not typical disclaimer: provides no safe harbor (abolished 2009); remove from all materials.",
        ],
    })

    # --- Q13: ad_compliance_card_q13.md ---
    _w(ws / "training" / "ad_compliance_card_q13.md", """\
# VitaCore Ad Compliance Quick Reference Card

## Prohibited Qualifiers (FTC Health Products Compliance Guidance, Dec 2022)

The following terms are INSUFFICIENT qualifiers for health claims based on emerging science:

| Prohibited Term | Example (Not Permitted) | severity |
|---|---|---|
| may | "may help support immune function" | high |
| helps | "helps maintain digestive health" (without adequate substantiation) | high |
| promising | "based on promising clinical results" | high |
| preliminary | "preliminary studies show improvement" | high |
| initial | "initial results indicate better gut health" | high |
| pilot | "our pilot study found..." | high |

## What NOT to Say (Requires Proof-Level Substantiation)

These claim types require at minimum one well-controlled RCT before use:

1. "Clinically demonstrated" — requires product-specific RCT, not just ingredient studies
2. "Scientifically proven" — requires competent and reliable scientific evidence per FTC standards
3. "Doctor-formulated/recommended" — requires physician verification + material connection disclosure

## Disclosure Rules — 16 CFR Part 255 (Effective July 26, 2023)

Compliant social media disclosure example:
**"Ad: I received payment from VitaCore to share my experience with ProBio+ Daily..."**

OR: **"#ad My 8-week ProBio+ Daily journey..."**

CRITICAL: '#ad' or 'Ad:' MUST be at the BEGINNING of the post. Hashtag-only disclosures at the
end of captions are INSUFFICIENT per FTC guidance.

## File Naming Convention

All final output files: `{document_type}_final_YYYYMMDD.{ext}`
""")

    # --- Q14: final/press_release_final_20260603.md ---
    pr_text = """\
# ProBio+ Daily — Revised Launch Press Release

## Compliance Review Summary

This press release has been reviewed against FTC Truth in Advertising standards. The following
issues from the initial compliance review (Q1) have been resolved:

- CI-001: Proof claim without product-specific RCT — REMOVED
- CI-002: Prohibited qualifier 'may' — REPLACED with evidence-based language
- CI-003: Prohibited qualifiers 'promising' and 'preliminary' — REMOVED
- CI-004: Proof language without adequate evidence — REPLACED
- CI-005: Prohibited qualifier 'initial' — REMOVED
- CI-006: Prohibited qualifier 'pilot' and uncontrolled study reference — REMOVED
- CI-007: Undisclosed endorsement — DISCLOSURE ADDED
- CI-008: Expert endorsement claim — MODIFIED with proper disclosure and substantiation note

Total violations identified in Q1: 8
Total violations resolved: 8

## Approved Claims (Post-Compliance Review)

VitaCore Inc. announces the US launch of **ProBio+ Daily**, a multi-strain probiotic and
B-vitamin complex dietary supplement formulated to support digestive and immune health.

### Immune Support

In a 12-week randomized, controlled trial of 120 healthy adults, supplementation with
Lactobacillus rhamnosus GG (LGG) was associated with statistically significant improvement
in immune function markers. This study meets FTC evidentiary standards for health claims.

### Digestive Health

Two randomized, controlled clinical trials demonstrate that Lactobacillus acidophilus NCFM
supports digestive comfort. VitaCore ProBio+ Daily contains 8 billion CFU of L. acidophilus NCFM.

### B-Vitamin Energy Support

ProBio+ Daily contains the full B-vitamin complex (B1, B2, B3, B5, B6, B7, B9, B12) at
100-1000% of Daily Value. B-vitamins play a well-established role in cellular energy metabolism,
as documented in peer-reviewed nutritional biochemistry literature.

## FTC Basis Summary

ftc_basis_summary: This press release complies with FTC Health Products Compliance Guidance
(December 2022), 16 CFR Part 255 (Endorsement Guides, effective July 26, 2023), 16 CFR Part 465
(Consumer Reviews Rule, effective October 21, 2024), and 16 CFR Part 323 (Made in USA Labeling Rule).

## Review Information

compliance_reviewed_by: ComplianceAI / Dr. Maria Santos, CCO, VitaCore Inc.
review_date: 2026-06-03
"""
    _w(ws / "final" / "press_release_final_20260603.md", pr_text)

    # --- Q15: final/signoff_final_20260603.txt ---
    pr_bytes = (ws / "final" / "press_release_final_20260603.md").read_bytes()
    digest = hashlib.sha256(pr_bytes).hexdigest()
    _w(ws / "final" / "signoff_final_20260603.txt",
       f"VERIFIED:{digest}:press_release_final_20260603.md\n")

    # --- Q16: final/compliance_summary_q16.json ---
    _wj(ws / "final" / "compliance_summary_q16.json", {
        "schema_version": "1.0",
        "total_violations_identified": 8,
        "violations_resolved": 8,
        "active_penalty_risk_usd": 51744,
        "governing_regulations": [
            "16 CFR Part 255",
            "16 CFR Part 465",
            "16 CFR Part 260",
            "16 CFR Part 323",
        ],
        "review_date": "2026-06-03",
    })

    # --- Q17: reports/decision_timeline_q17.json ---
    _wj(ws / "reports" / "decision_timeline_q17.json", {
        "events": [
            {
                "event_id": "EVT-001",
                "timestamp": "2026-05-26T10:00:00",
                "channel": "slack",
                "actor": "Sarah Chen (In-house Counsel)",
                "decision": "Flagged 'clinically demonstrated' and 'may help support' as violations; cited $51,744 penalty rate per 16 CFR Part 465.",
                "supersedes_event_id": None,
            },
            {
                "event_id": "EVT-002",
                "timestamp": "2026-05-26T10:30:00",
                "channel": "slack",
                "actor": "Mike Torres (Marketing Director)",
                "decision": "Contested findings citing $45,000 from bot summary; claimed 'results not typical' safe harbor still valid.",
                "supersedes_event_id": None,
            },
            {
                "event_id": "EVT-003",
                "timestamp": "2026-05-27T16:00:00",
                "channel": "feishu",
                "actor": "James Park (CEO)",
                "decision": "Informally approved 'supports immune health based on our proprietary blend' language and referenced 'results not typical' disclaimer as valid.",
                "supersedes_event_id": None,
            },
            {
                "event_id": "EVT-004",
                "timestamp": "2026-05-28T08:00:00",
                "channel": "email",
                "actor": "Compliance Counsel LLC",
                "decision": "Initial formal compliance opinion: conditionally permitted 'Doctor-formulated' claim; erroneously referenced 2009 'results not typical' safe harbor.",
                "supersedes_event_id": None,
            },
            {
                "event_id": "EVT-005",
                "timestamp": "2026-05-30T08:00:00",
                "channel": "feishu",
                "actor": "James Park (CEO)",
                "decision": "Formally withdrew request to keep 'clinically demonstrated to support immune function' in press release. Update 1 supersede.",
                "supersedes_event_id": "EVT-003",
            },
            {
                "event_id": "EVT-006",
                "timestamp": "2026-06-01T09:00:00",
                "channel": "main",
                "actor": "ComplianceAI / Dr. Maria Santos",
                "decision": "Q7 synthesis confirmed Sarah Chen's position correct; $51,744 penalty confirmed; 'results not typical' safe harbor confirmed abolished.",
                "supersedes_event_id": "EVT-002",
            },
            {
                "event_id": "EVT-007",
                "timestamp": "2026-06-02T09:00:00",
                "channel": "email",
                "actor": "Compliance Counsel LLC",
                "decision": "Revised opinion (email_revised_audit_v2): withdrew conditional permission for 'Doctor-formulated'; added Biodegradable capsule finding; retracted 'results not typical' safe harbor reference; indirectly superseded CEO's informal guidance (FTC rules override internal officer guidance).",
                "supersedes_event_id": "EVT-004",
            },
            {
                "event_id": "EVT-008",
                "timestamp": "2026-06-03T10:00:00",
                "channel": "main",
                "actor": "ComplianceAI / Dr. Maria Santos",
                "decision": "Final compliance summary completed; all 8 violations resolved; press release cleared for launch subject to final legal review.",
                "supersedes_event_id": None,
            },
        ],
    })


# --------------------------------------------------------------------------- #
# 运行 check
# --------------------------------------------------------------------------- #
EVAL_CMDS = {
    "q1": [
        "check_q1.py",
        ("pref", "P1,P2", "reports/compliance_issues_q1.json"),
    ],
    "q2": [
        "check_q2.py",
        ("pref", "P1,P2", "reports/disclosure_check_q2.json"),
    ],
    "q3": ["check_q3.py"],
    "q4": [
        "check_q4.py",
        ("pref", "P3,P4", "reports/prohibited_terms_q4.md"),
    ],
    "q5": [
        "check_q5.py",
        ("pref", "P3", "policies/review_management_policy_q5.md"),
    ],
    "q6": [
        "check_q6.py",
        ("pref", "P1", "reports/label_compliance_q6.json"),
    ],
    "q7": ["check_q7.py"],
    "q8": [
        "check_q8.py",
        ("pref", "P1,P2", "reports/revised_compliance_q8.json"),
    ],
    "q9": [
        "check_q9.py",
        ("pref", "P3", "templates/disclosure_script_q9.md"),
    ],
    "q10": [
        "check_q10.py",
        ("pref", "P1", "reports/audit_integration_q10.json"),
    ],
    "q11": [
        "check_q11.py",
        ("pref", "P1,P2", "reports/green_claims_q11.json"),
    ],
    "q12": [
        "check_q12.py",
        ("pref", "P1,P2", "reports/final_compliance_q12.json"),
    ],
    "q13": [
        "check_q13.py",
        ("pref", "P3,P4", "training/ad_compliance_card_q13.md"),
    ],
    "q14": [
        "check_q14.py",
        ("pref", "P3,P5", "final/press_release_final_20260603.md"),
    ],
    "q15": [
        "check_q15.py",
        ("pref", "P5", "final/signoff_final_20260603.txt"),
    ],
    "q16": [
        "check_q16.py",
        ("pref", "P1", "final/compliance_summary_q16.json"),
    ],
    "q17": ["check_q17.py"],
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
                print(f"  [PASS] {q} ({tag})")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"gold: {n_pass} checks PASSED, {n_fail} FAILED")

    # 反例抽样：错误产物必须 FAIL（不过松）
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    # 反例 1: Q7 — DECOY penalty $45,000
    _wj(ws / "reports" / "slack_synthesis_q7.json", {
        "conflict_identified": True,
        "correct_position": "Sarah Chen's position",
        "correct_penalty_usd": 45000,
        "discarded_position": "Mike Torres relied on bot summary.",
        "safe_harbor_status": "abolished in 2009",
    })
    ok, _ = run_check("check_q7.py", ws)
    probes += 1
    caught += int(not ok)
    print(f"  q7 DECOY penalty 45000 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 反例 2: Q12 — wrong update_source
    _wj(ws / "reports" / "final_compliance_q12.json", {
        "schema_version": "1.0",
        "update_source": "email_initial_audit_v1",
        "doctor_formulated_requires_substantiation": True,
        "superseded_items": ["results not typical"],
        "active_items": ["some finding"],
    })
    ok, _ = run_check("check_q12.py", ws)
    probes += 1
    caught += int(not ok)
    print(f"  q12 wrong update_source -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 反例 3: Q15 — placeholder hash (wrong SHA256)
    _w(ws / "final" / "signoff_final_20260603.txt",
       "VERIFIED:" + "a" * 64 + ":press_release_final_20260603.md\n")
    ok, _ = run_check("check_q15.py", ws)
    probes += 1
    caught += int(not ok)
    print(f"  q15 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 反例 4: Q16 — governing_regulations missing 16 CFR Part 465
    _wj(ws / "final" / "compliance_summary_q16.json", {
        "schema_version": "1.0",
        "total_violations_identified": 8,
        "violations_resolved": 8,
        "active_penalty_risk_usd": 51744,
        "governing_regulations": ["16 CFR Part 255"],
        "review_date": "2026-06-03",
    })
    ok, _ = run_check("check_q16.py", ws)
    probes += 1
    caught += int(not ok)
    print(f"  q16 missing 16 CFR Part 465 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 反例 5: Q5 — missing $51,744 penalty mention (uses wrong $45,000)
    _w(ws / "policies" / "review_management_policy_q5.md",
       "# Review Policy\n\nDo not write fake reviews.\nPenalty: $45,000 per violation.\n"
       "write, create, or sell a consumer review that materially misrepresents.\n"
       "unfounded or groundless legal threat is prohibited.\n§465.5 insiders must disclose.\n")
    ok, _ = run_check("check_q5.py", ws)
    probes += 1
    caught += int(not ok)
    print(f"  q5 wrong $45,000 penalty -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    print(f"negatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
