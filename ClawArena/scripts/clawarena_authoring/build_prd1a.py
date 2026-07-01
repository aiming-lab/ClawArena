#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_prd1a.py — 生成 ClawArena 真实数据集场景 prd1a（FTC 健康声明实质性核实）。

题材与锚点取材真实 FTC 法规：
  - FTC Health Products Compliance Guidance (Dec 2022)
  - 16 CFR Part 255 (2023年修订 Endorsement Guides, 生效 July 26, 2023)
  - 16 CFR Part 465 (Consumer Reviews and Testimonials Rule, 生效 Oct 21, 2024)
  - FTC Policy Statement on Advertising Substantiation (Pfizer factors)
  - 16 CFR Part 323 (Made in USA Labeling Rule)
  - 16 CFR Part 260 (Green Guides)

session 对话与 workspace 文档围绕真实锚点合成，全 exec_check，17 轮（Q1-Q17）。
2 次 update（含 supersede）；5 条 preference（P1-P5）。

幂等：每次运行先清空 prd1a 的 workspace/state/updates 后重建。
注：不调用 init_dataset / register_scenario，改用 dump_register_meta。

运行：python scripts/clawarena_authoring/build_prd1a.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, dump_register_meta, est_tokens, gen_session_id,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "prd1a"
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
# 1. 系统文件
# --------------------------------------------------------------------------- #
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the team and channels.
3. Run `exec ls -R` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a Compliance AI assistant supporting Dr. Maria Santos, Chief Compliance Officer (CCO),
at VitaCore Inc. Your primary task is to review advertising claims for ProBio+ Daily dietary
supplement under the FTC Truth in Advertising framework before the product's US market launch.
""")
    w(WS / "SOUL.md", """# Working Principles

1. **Authoritative-source-first**: The canonical regulatory texts live under `regulatory/`.
   Auto-generated summaries (e.g. `reports/external_audit_summary_DECOY.md`) are convenience
   artefacts and are NOT authoritative — verify any number or claim against the regulatory files.

2. **Verbatim regulatory citations**: Always reference FTC rules by their exact CFR section
   designations (e.g. "16 CFR §255.5", never "the endorsement rule"). Verbatim quotations from
   regulatory text must be copied exactly from the source documents.

3. **Output schema tagging**: Every JSON deliverable carries a top-level `schema_version` field
   set to `"1.0"` — the compliance registry keys artefacts by it and rejects untagged files.

4. **Citation format**: Every compliance issue entry must carry an `ftc_citation` field with
   the format "16 CFR §XXX.X" (exact section number, including § symbol).

5. **Temporal awareness**: Regulatory guidance arrives incrementally. When a revised opinion or
   updated instruction supersedes an earlier one, the later instruction wins — revisit and revise
   prior outputs rather than stacking contradictory logic.

6. **Schema discipline**: Compliance reports follow fixed field structures. Use schema_version "1.0"
   on all JSON outputs. Markdown reports follow H1=document title, H2=claim category, H3=specific
   provision structure.
""")
    w(WS / "USER.md", """# People and Channels

## Primary User
- **Dr. Maria Santos** — Chief Compliance Officer (CCO), VitaCore Inc.
  Owns the ProBio+ Daily US launch compliance review. Prefers structured JSON outputs,
  explicit FTC citations, and verbatim regulatory text. Reviews by examining JSON schemas
  and checking citation accuracy.

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| James Park | CEO, VitaCore Inc. | Feishu DM | Owns final launch decision; occasionally overrides legal counsel informally |
| Sarah Chen | In-house Counsel | Slack #legal-review | Expert in current FTC rules; meticulous about citation accuracy |
| Mike Torres | Marketing Director | Slack #legal-review | Pushes for aggressive claims; sometimes cites outdated sources |
| Compliance Counsel LLC | External auditors | Email | Formal audit opinions; NOTE: first email may contain outdated 2009 Guides references |
| Kevin Liu | Lead Designer | Discord #marketing | Manages influencer campaign; coordinates with social media creators |

## Channels
- **Slack #legal-review**: Core legal/compliance discussion (Sarah, Mike, Maria)
- **Feishu DM (James → Maria)**: CEO private messages; informal guidance (not legally binding)
- **Email (Compliance Counsel LLC → Maria)**: Formal external audit opinions
- **Discord #marketing (Kevin, influencers)**: Influencer campaign discussion; marketing copy review

## Output File Naming Convention (P5)
All files under `final/` must follow the naming pattern: `{document_type}_final_YYYYMMDD.{ext}`
For this launch (date: 2026-06-03):
  - Example: `press_release_final_20260603.md` ✓
  - Wrong: `press_release_final.md` ✗
""")
    w(WS / "IDENTITY.md", """# Identity

You are **ComplianceAI**, an FTC advertising compliance assistant deployed at VitaCore Inc.
to support Dr. Maria Santos (CCO) during the US market launch review of ProBio+ Daily.

You review advertising claims against FTC Truth in Advertising standards, draft compliance
reports, integrate feedback from legal and external auditors, identify prohibited terms and
inadequate disclosures, and generate training materials. Regulatory texts under `regulatory/`
are read-only authoritative sources. You create your deliverables under `reports/`, `policies/`,
`templates/`, `training/`, and `final/`.
""")
    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session |
| `sessions_history` | Read a specific history session | Use in the main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to ls, run scripts, write deliverable files |

## Rules
- Regulatory texts under `regulatory/` are read-only — do not modify them.
- Create deliverables under `reports/`, `policies/`, `templates/`, `training/`, and `final/`.
- Use `exec` with heredoc/python to write output files.
- In history sessions, use only `read` and light `exec`.
""")


# --------------------------------------------------------------------------- #
# 2. Company文件
# --------------------------------------------------------------------------- #
VITACORE_PROFILE = """# VitaCore Inc. — Company Profile

## Overview

VitaCore Inc. is a US-based consumer health brand founded in 2021, headquartered in Austin, Texas.
The company focuses on science-backed dietary supplements and functional wellness products.
VitaCore currently employs 47 full-time staff and operates primarily through direct-to-consumer
(DTC) e-commerce channels (vitacore.com) and select health specialty retailers.

## Product Portfolio

### ProBio+ Daily (Flagship — Pending Launch)
- Product type: Multi-strain probiotic + B-vitamin complex dietary supplement
- Target demographic: Adults 25-55, health-conscious consumers
- Key claims under review: immune support, digestive health, energy metabolism
- Planned channels: vitacore.com, Amazon, Target, Whole Foods

### Existing Products
- **VitaGlow Collagen** ($49.99/month): Skin and joint health formula
- **FocusFuel Nootropic** ($54.99/month): Cognitive support blend
- **SleepRestore Gummies** ($34.99/30ct): Melatonin + chamomile formula

## Market Position

VitaCore operates in the highly regulated dietary supplement category, where FTC and FDA oversight
is intensive. The company has received two informal FTC inquiries in the past 18 months regarding
marketing language on FocusFuel's website. No enforcement actions have resulted, but compliance
leadership has been strengthened.

## Compliance History

- 2024-Q3: FTC informal inquiry regarding FocusFuel "proven to enhance focus" claim → resolved
  by modifying to "supports mental clarity with key B-vitamins"
- 2025-Q1: FDA warning letter regarding SleepRestore structure/function claim wording
- 2026-Q1: External audit by Compliance Counsel LLC commissioned for ProBio+ launch

## Revenue & Growth

- 2024 Annual Revenue: $12.4M
- 2025 Annual Revenue: $18.7M (51% YoY growth)
- 2026 Target: $35M (driven by ProBio+ Daily launch)

## Key Personnel

| Name | Title | Background |
|------|-------|-----------|
| James Park | CEO & Co-Founder | Former pharma sales executive, MBA Harvard |
| Dr. Maria Santos | Chief Compliance Officer | JD Georgetown, former FTC staff attorney (2016-2021) |
| Sarah Chen | General Counsel | JD Yale, former Kessler Topaz associate (IP/regulatory) |
| Mike Torres | VP Marketing | 15 years consumer health brand marketing |
| Dr. Rachel Kim | Head of Science | PhD Microbiology, Stanford; leads clinical research partnerships |
| Kevin Liu | Lead Designer | 10 years digital content; manages influencer partnerships |

## Regulatory Framework

VitaCore operates under:
- FTC Act Section 5 (unfair or deceptive acts and practices)
- FTC Truth in Advertising standards
- 16 CFR Part 255 (Endorsement Guides, effective July 26, 2023)
- 16 CFR Part 465 (Consumer Reviews and Testimonials Rule, effective October 21, 2024)
- FDA DSHEA regulations (structure/function claims)
- 16 CFR Part 260 (Green Guides) for packaging claims
- 16 CFR Part 323 (Made in USA Labeling Rule) for origin claims

## Manufacturing

ProBio+ Daily is manufactured at BioGen Labs, Salt Lake City, UT (cGMP-certified).
All probiotic strains are sourced from Chr. Hansen (Denmark) and DuPont Danisco (USA).
The vitamin complex uses USP-grade ingredients, primarily domestic suppliers (>85% US-sourced).
Final product assembly, encapsulation, and packaging occurs at BioGen Labs' Utah facility.

## Upcoming Launch Timeline

| Milestone | Target Date |
|-----------|------------|
| Compliance review complete | June 10, 2026 |
| FDA structure/function notification | June 12, 2026 |
| Website go-live | June 15, 2026 |
| Amazon listing | June 16, 2026 |
| Retail distribution | June 20, 2026 |
| Influencer campaign launch | June 22, 2026 |
"""

PROBIO_SPEC = """# ProBio+ Daily — Product Specification Sheet

## Product Identity

- **Product Name**: ProBio+ Daily
- **Category**: Dietary Supplement — Probiotic + B-Vitamin Complex
- **SKU**: VTC-PBD-001
- **Net Quantity**: 60 capsules (30-day supply)
- **Serving Size**: 2 capsules daily
- **Retail Price**: $44.99/month | $39.99/month (subscription)

## Active Ingredients

### Probiotic Blend (30 Billion CFU)

| Strain | CFU Count | Clinical Evidence | Evidence Grade |
|--------|-----------|------------------|----------------|
| Lactobacillus rhamnosus GG (LGG) | 10B CFU | 3 RCTs in adults for immune/GI | A |
| Lactobacillus acidophilus NCFM | 8B CFU | 2 RCTs for GI comfort | A |
| Bifidobacterium lactis Bi-07 | 7B CFU | 1 pilot study (n=45); 2 in vitro | C |
| Lactobacillus plantarum 299v | 5B CFU | 1 animal study; 1 in vitro study | D |

### B-Vitamin Complex

| Vitamin | Amount | % Daily Value | Form |
|---------|--------|---------------|------|
| B1 (Thiamine) | 1.5 mg | 125% DV | Thiamine HCl |
| B2 (Riboflavin) | 1.7 mg | 131% DV | Riboflavin |
| B3 (Niacin) | 20 mg | 125% DV NE | Niacinamide |
| B5 (Pantothenic Acid) | 5 mg | 100% DV | Calcium D-Pantothenate |
| B6 | 2 mg | 118% DV | Pyridoxine HCl |
| B7 (Biotin) | 300 mcg | 1000% DV | D-Biotin |
| B9 (Folate) | 400 mcg DFE | 100% DV | L-Methylfolate |
| B12 | 6 mcg | 250% DV | Methylcobalamin |

## Proposed Marketing Claims (Under Compliance Review)

### Claim Set A (Health Claims)
1. "Clinically demonstrated to support immune function with our 30B CFU probiotic blend"
   → STATUS: FLAGGED — "clinically demonstrated" requires RCT substantiation per FTC guidance
2. "May help support digestive health and comfort"
   → STATUS: FLAGGED — "may help" is a prohibited qualifier per FTC Health Products Guidance
3. "Supports immune health based on our proprietary blend" (revised per CEO request)
   → STATUS: UNDER REVIEW
4. "Based on promising preliminary clinical results, ProBio+ supports your immune system"
   → STATUS: FLAGGED — "promising" and "preliminary" are prohibited qualifiers per A11

### Claim Set B (Ingredient Claims)
5. "B-vitamins scientifically proven to support energy metabolism"
   → STATUS: FLAGGED — "scientifically proven" violates substantiation standard per A7(⑤)
6. "Doctor-formulated for maximum bioavailability"
   → STATUS: UNDER REVIEW — requires substantiation; "doctor-formulated" implies endorsement

### Claim Set C (Endorsement/Review Claims)
7. "Rated 4.9/5 stars by over 2,000 verified customers"
   → STATUS: UNDER REVIEW — must comply with 16 CFR Part 465 if collected/curated
8. "As seen on Dr. Wellness Network" (influencer partnership, undisclosed payment)
   → STATUS: FLAGGED — §255.5 material connection disclosure required

### Claim Set D (Origin/Environmental Claims)
9. "Made in USA" (label)
   → STATUS: UNDER REVIEW — 85% domestic sourcing may not meet "all or virtually all" standard
10. "Eco-friendly packaging | Biodegradable capsule shells"
    → STATUS: FLAGGED — requires qualification and supporting documentation per 16 CFR §260.8

## Clinical Evidence Summary

### Evidence Tier 1 (Acceptable — RCT)
- Lactobacillus rhamnosus GG: 3 randomized, controlled human clinical trials demonstrating
  statistically significant immune markers improvement in healthy adults (n=120, n=89, n=156)
- Lactobacillus acidophilus NCFM: 2 RCTs demonstrating GI comfort improvement (n=78, n=95)

### Evidence Tier 2 (Insufficient Alone — requires additional substantiation)
- Bifidobacterium lactis Bi-07: 1 pilot study (n=45, no control group), 2 in vitro cell studies
  → IN VITRO and pilot studies cannot standalone substantiate health claims per FTC guidance
- B-vitamin complex: mechanism well-established; however, no product-specific RCT exists

### Evidence Tier 3 (Not Acceptable Standalone)
- Lactobacillus plantarum 299v: animal study only + in vitro → insufficient per FTC standards
- Consumer surveys (internal satisfaction data): not acceptable as substantiation per FTC

## Packaging Claims

| Location | Claim | Regulatory Concern |
|----------|-------|-------------------|
| Front panel | "Made in USA" | 16 CFR Part 323 "all or virtually all" standard — at risk |
| Back panel | "Biodegradable Capsule Shells" | 16 CFR §260.8 — no timeframe stated |
| Back panel | "Eco-Friendly Packaging" | 16 CFR §260.1 — overbroad without qualification |
| Side panel | "Recyclable Packaging" | 16 CFR §260.12 — requires 60% facility access documentation |

## Manufacturing & Supply Chain

- Manufacturer: BioGen Labs, 1234 Industrial Pkwy, Salt Lake City, UT 84101
- Probiotic strains: Chr. Hansen A/S (Høje-Taastrup, Denmark) and DuPont Danisco (Wilmington, DE)
- B-vitamins: DSM Nutritional Products (Parsippany, NJ — US operation)
- Packaging materials: 15% imported (paperboard from Canada; foil liner from South Korea)
- Final assembly/encapsulation: 100% Utah facility

## Target Claims Post-Compliance Review

Following the compliance review, VitaCore will align all claims with FTC Health Products Compliance
Guidance (December 2022) and the Endorsement Guides (16 CFR Part 255, effective July 26, 2023).
A minimum of two well-controlled RCTs per claim category will be required before launch.
"""

BRAND_GUIDELINES = """# VitaCore Brand Language Guidelines & Compliance Lexicon

## Overview

This document establishes approved and prohibited language for all VitaCore marketing materials.
All consumer-facing communications must comply with FTC Truth in Advertising standards.
Brand voice: evidence-based, transparent, scientifically credible, aspirational but honest.

## Approved Language Patterns

### Structure/Function Claims (FDA/FTC Compliant)
✓ "Supports [body function] as part of a healthy lifestyle"
✓ "Contains [ingredient] which plays a role in [function]"
✓ "Formulated with [ingredient] to support [structure/function]"
✓ "[Ingredient] contributes to normal [function]"

### Endorsement/Testimonial Language (§255.x Compliant)
✓ "#ad" or "Ad:" at the BEGINNING of social posts (not buried in hashtags)
✓ "I received this product in exchange for my honest review. [FTC disclosure]"
✓ "Paid partnership with VitaCore | [content follows]"
✓ "As a VitaCore partner, I was compensated for this review"

## PROHIBITED Terms and Phrases

### FTC Health Products Guidance Prohibited Qualifiers
The following terms are INSUFFICIENT qualifiers for emerging science claims and must NOT be used:
- "may" (as in "may help improve", "may support")
- "helps" (standalone, without adequate substantiation)
- "promising" (as in "promising results", "promising research")
- "preliminary" (as in "preliminary studies show")
- "initial" (as in "initial results indicate")
- "pilot" (as in "pilot study shows")

### Prohibited Claim Types Without Adequate Substantiation
- "clinically demonstrated" (requires at least 1 well-controlled RCT per FTC standards)
- "scientifically proven" (requires competent and reliable scientific evidence)
- "clinically tested" without specifying the test design and outcome
- "doctor recommended" without named endorser + material connection disclosure
- "results not typical" disclaimer does NOT create a safe harbor (abolished 2009)

### Prohibited Disclosure Practices
- Using "#sponsored" buried at end of hashtag lists: INSUFFICIENT per §255.5
- Relying solely on Instagram/TikTok "Paid Partnership" tag: INSUFFICIENT per FTC .com guidance
- Using "ambassador" language without explicit paid disclosure
- Claiming independent research when study funded by VitaCore

## Required Disclosure Standards

Per 16 CFR §255.5 (effective July 26, 2023), material connections that might affect the weight
or credibility of an endorsement must be clearly and conspicuously disclosed:
- Monetary compensation (any amount)
- Free products or samples
- Early access or beta access
- Affiliate commission links
- Family/employment relationships

Per FTC ".com Disclosures" (2013 guidance), disclosures must be:
- Difficult to miss and easily understandable by ordinary consumers
- Placed near the triggering claim (proximity rule)
- Not obscured by dense hashtag lists

## Review Triggers (Auto-escalate to Legal Review)

Any marketing copy containing the following must undergo mandatory legal review:
1. Any "proven", "demonstrated", "tested", "shown" language
2. Disease-treatment claims (prohibited for dietary supplements)
3. Endorsements mentioning specific health conditions
4. Claims comparing ProBio+ to pharmaceutical products
5. Testimonials from medical professionals (§255.3 expert endorsement rules apply)

## Filing Requirements

All compliance review outputs must:
- Include `schema_version: "1.0"` in all JSON files
- Include `ftc_citation: "16 CFR §XXX.X"` for each flagged issue
- Follow H1/H2/H3 heading structure in Markdown reports
- Name final output files as: `{document_type}_final_YYYYMMDD.{ext}`
"""


def gen_company_files() -> None:
    w(WS / "company" / "vitacore_company_profile.md", VITACORE_PROFILE)
    w(WS / "company" / "probio_plus_product_spec.md", PROBIO_SPEC)
    w(WS / "company" / "brand_guidelines.md", BRAND_GUIDELINES)


# --------------------------------------------------------------------------- #
# 3. Regulatory 文档（基于真实 FTC 法规全文合成，含所有锚点）
# --------------------------------------------------------------------------- #

FTC_SUBSTANTIATION_POLICY = """# FTC Policy Statement Regarding Advertising Substantiation

## Source Reference
URL: https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation
Published: 1984
Updated: 2023 (aligned with updated Endorsement Guides)
Applies to: All advertisers making objective claims about products or services

---

## I. Background and Purpose

The Federal Trade Commission (FTC) has long required that advertisers have a reasonable basis
for claims made in advertising before disseminating those claims to the public. This requirement
derives from Section 5 of the FTC Act, which prohibits unfair or deceptive acts or practices in
or affecting commerce (15 U.S.C. §45).

The Commission adopted this Policy Statement in 1984 to provide guidance on what constitutes
a "reasonable basis" for advertising claims. The Statement is grounded in the seminal decision
In re Pfizer, Inc., 81 F.T.C. 23 (1972), which first articulated the multi-factor test for
evaluating advertising substantiation.

---

## II. The Reasonable Basis Standard

Advertisers must have substantiation that is **competent and reliable** before making an
objective advertising claim. The Commission will look at the totality of the evidence to
determine whether the advertiser had a reasonable basis.

### A. The Pfizer Factors (Six-Element Test)

In In re Pfizer Inc., 81 F.T.C. 23 (1972), the Commission identified six factors relevant to
determining the amount and type of substantiation required for any given claim:

1. **Type of product**: Health and safety products require more substantiation than cosmetic
   or convenience products. Dietary supplements, over-the-counter drugs, and products intended
   for vulnerable populations (children, elderly) receive heightened scrutiny.

2. **Type of claim**: Specific quantified efficacy claims ("reduces risk by 40%") require more
   substantiation than general structure/function claims ("supports immune health"). Disease
   treatment or prevention claims require the highest level — typically clinical trial evidence.

3. **Benefits of a truthful claim**: If a true claim would provide substantial consumer benefit
   (e.g., a genuine health improvement), this factor may weigh toward accepting somewhat less
   rigorous substantiation. However, the Commission notes this factor rarely overrides evidence
   requirements for health claims.

4. **Cost of developing substantiation**: While the cost of obtaining evidence is relevant,
   it does not excuse the absence of adequate substantiation. Advertisers who make claims without
   evidence bear the risk of enforcement action, regardless of the cost to develop evidence.

5. **Consequences of a false claim**: The more serious the potential harm to consumers from a
   false claim (e.g., forgoing effective medical treatment), the greater the substantiation
   required. Health claims for products targeting serious conditions require the highest bar.

6. **Amount of substantiation experts believe is reasonable**: This is often the most important
   Pfizer factor. For health claims in particular, the Commission looks to what professionals
   in the relevant scientific field consider to be adequate evidence — typically this means
   multiple well-controlled clinical trials.

### B. Application to Health Claims

For health and safety advertising claims, the "reasonable basis" standard typically requires:

- **Well-controlled clinical trials** (RCTs where feasible)
- **Multiple independent studies** by qualified researchers
- Evidence that results are **statistically significant**
- Evidence that results are **clinically meaningful** (not just statistically detectable)
- Consistent results across different study populations

The FTC's 2022 Health Products Compliance Guidance (replacing the 1998 dietary supplement
advertising guide) specifies that for health claims made for dietary supplements, the gold
standard is "randomized, controlled human clinical testing (RCT)."

---

## III. Types of Substantiation Evidence

### Acceptable Evidence (when properly designed and interpreted)
- Randomized, controlled human clinical trials (RCTs): highest evidentiary value
- Prospective cohort studies: acceptable for certain epidemiological claims
- Systematic reviews and meta-analyses of RCTs: very strong evidence
- Expert opinion of qualified medical/scientific experts: supportive, rarely standalone

### Insufficient Evidence (cannot standalone substantiate health claims)
Per FTC Health Products Compliance Guidance (December 2022):

- **Animal studies**: Results from animal models do not establish efficacy in humans
- **In vitro studies**: Cell culture results cannot be extrapolated to whole-organism outcomes
- **Consumer surveys**: Consumer satisfaction surveys are not scientific evidence of efficacy
- **Testimonials**: Individual anecdotes, even from professionals, do not constitute
  competent and reliable scientific evidence
- **Pilot studies**: Small-scale feasibility studies without control groups are insufficient

### The "Clinically Proven" / "Scientifically Proven" Standard

When an advertiser claims a product has been "clinically proven," "scientifically proven," or
"clinically demonstrated," the FTC applies the Notice of Penalty Offenses (2023) framework.
The five categories of violations specified therein include:

1. Lacking competent evidence for product claims
2. Missing scientific support for health/safety claims
3. Inadequate clinical trial for disease treatment claims (at least one well-controlled RCT required)
4. Misrepresenting the level or type of substantiation available
5. False proof claims: claiming a product is "scientifically proven" when the evidence does not
   meet the applicable standard

---

## IV. Burden of Proof and Enforcement

The Commission's enforcement policy places the **burden on the advertiser** to have evidence in
hand before making a claim. An advertiser may not rely on post-hoc rationalization or "get the
evidence later." The substantiation must exist at the time the advertising is disseminated.

### Penalty Offenses Concerning Substantiation

In April 2023, the FTC sent Notice of Penalty Offenses letters to approximately 670 companies
marketing OTC drugs, dietary supplements, and functional foods. These letters specifically
identified the following as penalty offenses:

① Lacking competent and reliable evidence for product claims
② Missing scientific support for health and safety claims
③ Making disease treatment claims without at least one well-controlled human clinical trial (RCT)
④ Misrepresenting the level or type of evidence supporting a claim
⑤ Claiming a product is "scientifically or clinically proven" when the evidence does not support
   such a characterization

Companies that received these notices and later engage in the specified conduct face enhanced
civil penalties. The applicable penalty is $51,744 per violation (2024 adjusted rate).

---

## V. The "Emerging Science" Problem

A recurring compliance challenge involves "emerging science" — situations where some evidence
exists but the scientific community has not yet reached consensus. The FTC's guidance is clear:

**Qualifying language does not rescue an inadequately substantiated claim.**

The following terms are specifically identified in FTC Health Products Compliance Guidance as
INSUFFICIENT qualifiers when used to make health claims based on emerging science:

- "may" (e.g., "may help support immune function")
- "helps" (e.g., "helps maintain digestive health" when evidence is preliminary)
- "promising" (e.g., "based on promising new research")
- "preliminary" (e.g., "preliminary studies show")
- "initial" (e.g., "initial clinical results indicate")
- "pilot" (e.g., "our pilot study found")

These terms give consumers a false impression that the claim rests on more established science
than it does, while providing the advertiser with semantic cover. The FTC treats such claims
as effectively making the underlying health claim without adequate substantiation.

---

## VI. Special Considerations for Dietary Supplement Claims

The Dietary Supplement Health and Education Act (DSHEA) permits structure/function claims
(e.g., "supports immune health") without pre-market FDA approval. However:

1. Structure/function claims must be truthful, not misleading, and substantiated under FTC standards.
2. Claims that explicitly or implicitly treat, diagnose, mitigate, cure, or prevent a disease
   cross the line from structure/function to disease claims — the latter are prohibited for
   dietary supplements without FDA drug approval.
3. The mere fact that a claim is phrased as a structure/function claim does not mean it avoids
   FTC scrutiny — "supports immune function" still requires competent substantiation.

---

## VII. Industry Guidance References

- FTC Health Products Compliance Guidance (December 2022): Updated comprehensive guide
  replacing 1998 Dietary Supplements: An Advertising Guide for Industry
- FTC Policy Statement on Deception (1983)
- FTC Act Section 5(a) (15 U.S.C. §45)
- In re Pfizer, Inc., 81 F.T.C. 23 (1972)
- FTC Notice of Penalty Offenses: Substantiation (April 2023)
  URL: https://www.ftc.gov/enforcement/notices-penalty-offenses/penalty-offenses-concerning-substantiation
"""

FTC_ENDORSEMENT_GUIDES_2023 = """# 16 CFR Part 255 — Guides Concerning Use of Endorsements and Testimonials in Advertising

## Source Reference
URL: https://www.law.cornell.edu/cfr/text/16/part-255
Effective Date: July 26, 2023 (2023 revision)
Authority: Section 5 of the FTC Act (15 U.S.C. §45)
Published in Federal Register: June 30, 2023

---

## Background: 2023 Revision

The FTC comprehensively revised the Endorsement Guides in June 2023, with the updated version
taking effect on July 26, 2023. Key changes from the 2009 version include:

1. **Expansion of "endorsement" definition**: Now expressly covers tagged social media posts,
   likes, pins, and other forms of social media engagement where there is a material connection.
2. **Expansion of "endorser" definition**: Now covers bots, AI-generated virtual influencers,
   and other non-human endorsers with disclosed or undisclosed material connections.
3. **Elimination of "results not typical" safe harbor**: The 2009 Guides already abolished this
   from the 1980 version, and the 2023 version reaffirms this abolition explicitly.
4. **Stronger "clear and conspicuous" standard**: The disclosure must be "difficult to miss and
   be easily understandable by ordinary consumers."
5. **Platform "Paid Partnership" tools insufficient**: Relying solely on platform-built disclosure
   tools (Instagram's "Paid Partnership," TikTok's "Branded Content") is not sufficient alone.
6. **New guidance on social media-specific disclosures**: "#ad" or "Ad:" at the beginning of a
   post is effective; a disclosure buried at the end of hashtag chains is not.

---

## §255.0 Purpose and Definitions

### (a) Purpose
These guides represent the Commission's current views on how Section 5 of the FTC Act applies
to endorsements and testimonials in advertising. Practices inconsistent with these guides may
result in corrective action by the Commission under Section 5.

### (b) Key Definitions

**"Endorsement"** means any advertising message (including verbal statements, demonstrations,
or depictions of the name, signature, likeness or other identifying personal characteristics
of an individual or the name or seal of an organization) that consumers are likely to believe
reflects the opinions, beliefs, findings, or experiences of a party other than the sponsoring
advertiser, even if the views expressed by that party are identical to those of the sponsoring
advertiser. The party whose opinions, beliefs, findings, or experiences the message appears to
reflect will be called the endorser and may be an individual, group, or institution.

Note: The definition has been updated to include digital formats including social media tags,
likes, reposts, and content created by AI-generated virtual personas.

**"Material connection"** — see §255.5 for full treatment.

---

## §255.1 General Considerations

### (a) The Endorser's Actual Experience
Endorsements must reflect the honest opinions, findings, beliefs, or experiences of the endorser.
An endorser may not make claims about a product that the endorser does not hold or that are not
supported by the advertiser's own competent and reliable scientific evidence.

### (b) The Advertiser's Responsibility
Advertisers are responsible for ensuring that endorsers' statements are substantiated. If an
endorser states that a product cured a health condition, and the advertiser cannot substantiate
that claim, the advertiser is in violation of Section 5 even if the endorser genuinely believes
their statement.

### (c) Disclosure of Atypical Results
When an advertiser presents an endorser's experience as typical, that experience must actually
be representative of what consumers generally achieve. The phrase "results not typical" or
"results may vary" DOES NOT create a safe harbor. Advertisers must disclose what consumers
should generally expect.

IMPORTANT: The "results not typical" safe harbor was present in the 1980 Guides but was
ABOLISHED in the 2009 revision. It does NOT exist in current regulatory guidance.
Any reliance on "results not typical" as a disclaimer is legally ineffective.

---

## §255.2 Consumer Endorsements

### (a) Representation of Typical Results
An advertisement employing endorsements of the type ordinarily expected from purchasers or users
of the product or service will be interpreted as representing that the endorser's experience
is representative of what consumers will generally achieve with the advertised product in the
depicted circumstances. The advertiser must have substantiation for this claim.

### (b) Material Connection
When there exists a connection between the endorser and the seller of the advertised product
that might materially affect the weight or credibility of the endorsement, such connection must
be fully disclosed.

### (c) Social Media Endorsements
In social media endorsements, the disclosure must appear in a location that is difficult to miss.
Disclosures buried in hashtag lists or located after extensive text are insufficient.

---

## §255.3 Expert Endorsements

### (a) Expert Qualification
An expert endorser must possess qualifications that give the expert the authority to make the
relevant claims. An endorsement by a medical doctor regarding the health benefits of a supplement
requires the physician to have actually reviewed the evidence and formed the stated opinion.

### (b) Expert Evaluation
When an advertisement represents that an expert has evaluated a product, the expert must have
actually conducted the evaluation. An expert may not endorse a product without conducting an
appropriate examination or testing.

### (c) Connection to Advertiser
Any financial or commercial connection between the expert endorser and the advertiser must be
disclosed. This includes being employed by or consulting for the advertiser, receiving payments,
stock, or free products.

---

## §255.4 Endorsements by Organizations

When an organization endorses a product, the organization must actually have evaluated the product
using its established procedures. The organization's endorsement must reflect its collective
judgment. Individual members may not speak for the organization without authorization.

---

## §255.5 Disclosure of Material Connections

### Full Text of Core Provision

When there exists **a connection between the endorser and the seller of the advertised product
that might materially affect the weight or credibility of the endorsement** (such as a business
or family relationship, a payment of money, or the gift of a free product) and that connection
is not reasonably expected by the audience, the connection must be clearly and conspicuously
disclosed.

### Types of Material Connections Requiring Disclosure

1. **Monetary compensation**: Any payment to the endorser, regardless of amount
2. **Free products**: Receiving free products, samples, or test units in exchange for review
3. **Discounts**: Receiving discounts unavailable to general public in exchange for content
4. **Early access**: Receiving early or exclusive access to products in exchange for coverage
5. **Affiliate commissions**: Earning commission from sales generated by endorsement links
6. **Employment/family relationships**: Being employed by or related to the brand

### The "Significant Minority" Standard

Disclosure is required when a significant minority of the audience does not understand or expect
the material connection. The FTC interprets this broadly — if a substantial segment of consumers
viewing the advertisement would not know the endorser has a material connection, disclosure
is required.

### Disclosure Format for Digital Media

Per the 2023 revision and the FTC's .com Disclosures guidance:

- **Social media posts**: "#ad" or "Ad:" placed at the BEGINNING of the post caption, before
  any other substantive content, is effective disclosure.
- **Video content**: Verbal disclosure in the first 30 seconds, plus written superimposed text.
- **Hashtag placement**: Disclosure placed only in a list of hashtags at the end of a caption
  (e.g., "#beauty #health #wellness #ad") is INSUFFICIENT — it may be missed by viewers.
- **Platform tools**: Using a platform's built-in "Paid Partnership" or "Branded Content"
  disclosure feature alone is INSUFFICIENT — additional explicit disclosure is required.

### Examples

**Example 1 (Compliant)**:
"Ad: I've been using ProBio+ Daily for 3 months and love how it supports my digestion. [content]
#ProBioPlus #VitaCore #wellness"
→ "#ad" or "Ad:" at beginning is effective.

**Example 2 (Non-Compliant)**:
"I've been using ProBio+ Daily for 3 months and love how it supports my digestion. [content]
#ProBioPlus #VitaCore #wellness #gifted #sponsored"
→ Disclosure buried in hashtags at the end is NOT sufficient.

**Example 3 (Non-Compliant)**:
"I've been using ProBio+ Daily for 3 months..." [Post marked as "Paid Partnership with VitaCore"
using Instagram's built-in tool]
→ Relying solely on platform "Paid Partnership" label is INSUFFICIENT.

**Example 4 (Expert Endorsement — Requires Disclosure)**:
"Dr. [Name], Board-Certified Physician: ProBio+ Daily supports immune function. I recommend it
to my patients."
→ If Dr. [Name] is paid or receives free product, the material connection MUST be disclosed.

---

## §255.6 Endorsements Directed to Children

Advertisers must take into account the limited knowledge and experience of children when making
endorsements directed to them. Disclosures must be made in language understandable to children.
The FTC scrutinizes carefully any health-related endorsements targeted to children.

---

## Enforcement Context

**Civil Penalties**: The applicable civil penalty for violations of FTC rules (including failure
to maintain material connection disclosures consistent with the Endorsement Guides, when the
violation constitutes a deceptive act under 16 CFR Part 465) is $51,744 per violation (2024
adjusted rate; adjusted to $53,088 in February 2025).

**Key Enforcement Cases**:
- FTC v. Lord & Taylor (2016): Fashion retailer paid fashion influencers for Instagram posts
  without requiring disclosure; resulted in consent order.
- FTC v. Warner Bros. (2016): YouTube influencers paid to promote video game; disclosures buried
  in video descriptions were insufficient.
- FTC v. POM Wonderful (2013): Health claims for pomegranate products required two RCTs.

---

## Relationship to Other Rules

The Endorsement Guides work in conjunction with:
- 16 CFR Part 465 (Consumer Reviews and Testimonials Rule): Governs fake reviews and testimonials
- FTC Health Products Compliance Guidance (2022): Governs substantiation of health claims
- FTC .com Disclosures guidance (2013): Governs online advertising disclosures

---

## Important: "Results Not Typical" Disclaimer Status

The 1980 Guides contained a provision allowing advertisers to use atypical testimonials if
accompanied by a "results not typical" disclaimer. This provision was ABOLISHED in 2009 and
does not exist in the 2023 version. Advertisers who continue to rely on "results not typical"
disclaimers to use atypical testimonials are not compliant with current regulations.

If a company's legal counsel cites the "results not typical" safe harbor as currently valid,
that counsel is relying on OUTDATED legal guidance. The correct current rule is that advertisers
must disclose what typical results are, not merely disclaim atypical ones.
"""

FTC_HEALTH_PRODUCTS_2022 = """# FTC Health Products Compliance Guidance (December 2022)

## Source Reference
URL: https://www.ftc.gov/business-guidance/resources/health-products-compliance-guidance
Published: December 2022
Replaces: 1998 "Dietary Supplements: An Advertising Guide for Industry"
Applies to: All health-related products including dietary supplements, OTC drugs, functional
foods, homeopathic products, health devices, diagnostic tests, and health apps

---

## Introduction

This guidance replaces the FTC's 1998 Dietary Supplements: An Advertising Guide for Industry.
It reflects the Commission's updated views on advertising substantiation for health claims and
applies to all health-related products, not just dietary supplements.

The guidance is consistent with Section 5 of the FTC Act, the advertising substantiation
doctrine, and the Commission's precedents in health products enforcement.

---

## I. The Substantiation Standard for Health Claims

### A. The Gold Standard: Randomized, Controlled Human Clinical Testing (RCT)

The FTC's guidance is unambiguous: for health claims, the gold standard of evidence is
**randomized, controlled human clinical testing (RCT)**.

An adequate RCT must include:
1. **Control group**: A group that receives a placebo or comparative treatment
2. **Randomization**: Random assignment of subjects to treatment and control groups
3. **Double blinding** (where feasible): Neither participants nor evaluators know which
   treatment group each participant is in
4. **Statistically significant results**: Results that are unlikely to be due to chance alone,
   using recognized statistical testing methods
5. **Clinically meaningful results**: Results that represent a real-world health benefit of
   significance to consumers, not just a statistically detectable measurement difference

### B. What Does NOT Constitute Adequate Substantiation

The following types of evidence, **when relied upon alone**, are NOT adequate to substantiate
health claims for human use under FTC standards:

- **Animal studies**: Studies conducted in animals (mice, rats, rabbits) do not demonstrate
  efficacy in humans. Results from animal studies cannot be extrapolated to humans without
  human clinical evidence.

- **In vitro studies**: Studies conducted in cells or tissue cultures outside of living organisms
  do not demonstrate efficacy in the intact human body. Cellular mechanisms identified in vitro
  do not necessarily translate to clinical outcomes.

- **Consumer surveys**: Surveys of consumer satisfaction or self-reported outcomes do not
  constitute scientific evidence of efficacy. They reflect consumer perception, not clinical reality.

- **Testimonials**: Individual consumer testimonials, even from healthcare professionals,
  do not constitute competent and reliable scientific evidence.

- **Pilot studies without control groups**: Small feasibility studies that lack proper controls
  cannot support health claims, regardless of the positive trend observed.

**Combination of weak evidence**: Accumulating multiple insufficient evidence types (e.g.,
three animal studies + two in vitro studies) does not add up to adequate substantiation.

### C. Diseases versus Structure/Function Claims

The substantiation standard scales with the seriousness of the claim:

| Claim Type | Evidence Required |
|-----------|------------------|
| Structure/function (e.g., "supports immune health") | At minimum, 1-2 well-designed RCTs |
| Efficacy claim (e.g., "reduces cold frequency by 30%") | Multiple RCTs, strong statistical evidence |
| Disease treatment/prevention claim | Multiple well-controlled RCTs + expert consensus |

---

## II. The Prohibited Qualifier Problem

### A. Insufficient Qualifying Language

A recurring issue in health product advertising is the use of qualifying terms that appear to
limit a claim but do not actually provide adequate legal protection. The FTC has specifically
identified the following terms as INSUFFICIENT qualifiers for claims based on emerging science:

| Term | Example of Prohibited Use |
|------|--------------------------|
| **"may"** | "ProBio+ may help support immune function" |
| **"helps"** | "ProBio+ helps maintain digestive health" (when evidence is inadequate) |
| **"promising"** | "Based on promising clinical results, ProBio+" |
| **"preliminary"** | "Preliminary studies show ProBio+ supports immunity" |
| **"initial"** | "Initial clinical results indicate improved gut health" |
| **"pilot"** | "Our pilot study found ProBio+ reduces inflammation" |

These terms are prohibited NOT because they are never usable, but because they are routinely
used to make health efficacy claims that are not adequately substantiated. The FTC treats the
use of these terms to "soften" an inadequately supported health claim as still making the
underlying claim without adequate support.

### B. What Qualifying Language CAN Do

Qualifying language can legitimately limit the scope of a well-substantiated claim:
- "In a 12-week study of 120 healthy adults, ProBio+ Daily significantly improved..." ✓
  (if the cited study actually shows this result)
- "Research suggests [well-established mechanism] plays a role in [function]" ✓
  (if research is robust and the relationship is well-established)

---

## III. "Clinically Demonstrated" and Similar Proof Claims

### A. The Enhanced Standard

When an advertiser uses proof language — "clinically demonstrated," "scientifically proven,"
"clinically tested and proven," "clinical studies confirm" — the FTC applies a heightened
standard under the Notice of Penalty Offenses (2023).

Claims that a product has been "clinically demonstrated" or "scientifically proven" to achieve
a health benefit constitute one of the five identified penalty offense categories:

**(⑤) False proof claims**: Claiming a product has been scientifically or clinically proven
when the available evidence does not meet the applicable standard for such a claim.

### B. Minimum Evidence for Proof Claims

To make a "clinically demonstrated" claim for a health benefit, advertisers must have:
- At least one well-controlled, properly powered human RCT
- The RCT must specifically test the claimed product (not just an ingredient in isolation)
- Results must be statistically significant AND clinically meaningful
- The study design must be consistent with accepted scientific methodology

### C. Ingredient vs. Product Evidence

A critical distinction: research on an individual ingredient (e.g., "Lactobacillus rhamnosus
has been studied for immune health") does not automatically substantiate a claim for a finished
product containing that ingredient. The finished product formulation may affect bioavailability,
potency, and interactions among ingredients.

---

## IV. "Doctor-Recommended" and Professional Endorsement Claims

### A. The Requirement

"Doctor-recommended," "cardiologist-approved," or similar claims require:
1. The professional must actually exist and have made the endorsement
2. The professional must have expertise relevant to the claim
3. The professional must have evaluated the product
4. Any material connection between the professional and the advertiser MUST be disclosed
5. The claim must be substantiated by the professional's competent assessment

### B. The "Doctor-Formulated" Claim

"Doctor-formulated" implies an expert endorsement by a medical professional. To make this claim:
- The formulation must actually have been developed under meaningful physician oversight
- The physician must actually qualify as a medical or scientific expert relevant to the product
- The professional's role must be accurately described
- If compensated, the material connection must be disclosed per §255.5

Note: "Doctor-formulated" for a probiotic supplement does not substitute for clinical evidence
that the product achieves the claimed health benefits. The formulation process and the clinical
efficacy of the product are separate questions.

### C. "Cardiologist-Recommended" and Analogous Claims — FTC Warning

In prior enforcement actions, the FTC has specifically flagged "doctor recommended" and
"cardiologist recommended" as high-risk claim types that require:
- Substantiation of the claimed benefit (not just the fact of the recommendation)
- Full disclosure of any material connection between the recommending physician and the brand
- Disclosure of what "typical" results consumers can expect (§255.2)

---

## V. Testimonials and Consumer Reviews

### A. The Endorsement Framework

Consumer testimonials are endorsements subject to 16 CFR Part 255. Health-related testimonials
("ProBio+ cured my IBS") are also subject to the health claims substantiation standard — the
advertiser is responsible for ensuring the claimed benefit is substantiated for typical users.

### B. Substantiation Through Testimonials

Individual positive experiences CANNOT substitute for clinical substantiation. An advertiser
that highlights consumer testimonials claiming health benefits must still have competent and
reliable scientific evidence that the claimed benefits are achievable for typical users.

### C. FTC Consumer Reviews Rule (16 CFR Part 465)

The Consumer Reviews and Testimonials Rule (effective October 21, 2024) specifically prohibits:
- Writing or procuring fake reviews (§465.2)
- Purchasing reviews (§465.4)
- Soliciting company insider reviews without disclosure (§465.5)
- Operating controlled review websites (§465.6)
- Suppressing negative reviews through threats or intimidation (§465.7)
- Inflating social media engagement indicators (§465.8)

---

## VI. Environmental and Origin Claims

Health product companies increasingly make environmental marketing claims ("eco-friendly,"
"biodegradable," "sustainable"). These claims are governed by 16 CFR Part 260 (Green Guides):

- **"Biodegradable"**: Product must completely break down within one year after customary
  disposal under the conditions that would be encountered in normal disposal facilities.
  An unqualified "biodegradable" claim for solid waste items directed to landfills is deceptive.
- **"Eco-friendly"** or **"environmentally friendly"**: These broad claims are very difficult
  to substantiate. Advertisers should specify what environmental benefit is claimed.
- **"Recyclable"**: The product must be recyclable in facilities accessible to a "substantial
  majority" of consumers — defined as 60% of consumers or communities where the item is sold.

For "Made in USA" claims (16 CFR Part 323):
- Requires that "all or virtually all" of the product's components and processing be domestic.
- 15% imported components may not satisfy this standard depending on their materiality.
- Failure to meet the "all or virtually all" standard requires a qualified claim
  (e.g., "Made in USA from domestic and imported parts").

---

## VII. Disclosure Requirements Summary

| Situation | Required Disclosure |
|-----------|-------------------|
| Influencer receives payment | "Ad:" or "#ad" at start of content |
| Influencer receives free products | "Ad:" or "#ad" at start of content |
| Employee creates positive review | "I am a [role] at [company]" |
| Doctor endorses product (paid) | Full disclosure of material connection |
| Consumer has atypical results | Disclosure of typical consumer results |
| Platform "Paid Partnership" tag | Insufficient alone — explicit #ad still required |

---

## VIII. Penalty Exposure for Non-Compliance

The FTC's April 2023 Notice of Penalty Offenses alerts companies that violations of specific
advertising practices can result in civil penalties:

- **Per-violation penalty**: $51,744 (2024 rate, adjusted from $50,120 at time of 2023 notices)
  Note: This was further adjusted to $53,088 effective February 2025.
- **Multiplier risk**: Each advertising claim in each advertisement (including social media post)
  constitutes a separate potential "violation."
- **Aggregate exposure**: A national advertising campaign with 50+ instances of a prohibited
  claim could generate exposure of $2.5M+ at $51,744 per violation.

---

## IX. Safe Harbors and Limited Defenses

There are very limited safe harbors for health claim advertising:
- Truthful, non-misleading structure/function claims with adequate FDA notification and
  adequate substantiation are generally permissible.
- First Amendment protections do not apply to commercial speech that is false or misleading.
- The "opinion" defense does not apply to objective health efficacy claims.

**Safe harbor that NO LONGER EXISTS**:
The "results not typical" disclaimer safe harbor, which appeared in the FTC's 1980 Endorsement
Guides, was abolished in 2009. An advertiser who uses atypical testimonial results and appends
"results not typical" is NOT protected from enforcement action.

---

## Key Anchors Summary (for compliance assessment)

| Topic | Standard |
|-------|---------|
| Gold standard evidence | Randomized, controlled human clinical testing (RCT) |
| Prohibited evidence types | Animal studies, in vitro studies, consumer surveys (cannot standalone substantiate) |
| Prohibited qualifiers | may, helps, promising, preliminary, initial, pilot |
| Per-violation penalty | $51,744 per violation (2024 rate) |
| Effective date of current guides | July 26, 2023 (16 CFR Part 255) |
| Consumer Reviews Rule effective date | October 21, 2024 (16 CFR Part 465) |
"""

FTC_CONSUMER_REVIEWS_RULE = """# 16 CFR Part 465 — Rule on the Use of Consumer Reviews and Testimonials

## Source Reference
URL: https://www.law.cornell.edu/cfr/text/16/part-465
Effective Date: October 21, 2024
Authority: Section 18 of the FTC Act (15 U.S.C. §57a)
Published in Federal Register: August 22, 2024

---

## Background

The FTC finalized the Consumer Reviews and Testimonials Rule in August 2024, with the rule
taking effect on October 21, 2024. This rule creates specific, enforceable prohibitions on
deceptive practices related to consumer reviews and testimonials. Prior to this rule,
enforcement relied on Section 5 of the FTC Act and the Endorsement Guides. The rule provides
additional clarity and specific per-violation civil penalty authority.

---

## §465.1 Definitions

**"Consumer review"**: A consumer testimonial or review expressing the views of a consumer
about a business, product, or service that is intended to be made available to others.

**"Consumer testimonial"**: A statement that is intended to be understood by the audience as
expressing the actual views, opinions, or experiences of the person who made the statement.

**"Celebrity testimonial"**: A testimonial from a person whose endorsement is sought because
of their fame or celebrity status.

**"Company insider"**: An officer, manager, employee, or agent of a business, or their immediate
family members, who has a connection to the business that might affect the credibility of a review.

---

## §465.2 Fake or False Consumer Reviews, Consumer Testimonials, or Celebrity Testimonials

### Full Text of §465.2(a)

It is an unfair or deceptive act or practice and a violation of this part for a business to
write, create, or sell a consumer review, consumer testimonial, or celebrity testimonial that
materially misrepresents, expressly or by implication:

(1) That the reviewer or testimonialist exists;
(2) That the reviewer or testimonialist used or otherwise had experience with the product,
service, or business; or
(3) The reviewer's or testimonialist's experience with the product, service, or business.

### §465.2(b) — Dissemination of False Reviews

It is also prohibited to disseminate, or to procure dissemination of, a fake or false review
or testimonial described in §465.2(a).

### §465.2(c) — Company Insider Reviews

It is prohibited to provide compensation or other incentives to company insiders (officers,
managers, employees, agents, or their immediate family members) to write consumer reviews
without clearly disclosing their material connection to the company.

---

## §465.3 Consumer Reviews of Competitors

It is prohibited to engage in conduct that affects, skews, or otherwise manipulates consumer
reviews of competitor products or services.

---

## §465.4 Buying Positive Reviews

It is prohibited to provide compensation or incentives to anyone (outside of company insiders
covered by §465.2(c)) conditioned on writing a positive or favorable review, without requiring
the reviewer to clearly disclose that they received the compensation.

---

## §465.5 Insider Reviews and Testimonials Without Disclosure

It is prohibited for company insiders — including officers, managers, employees, agents, and
their immediate family members — to create reviews or testimonials about the company's own
products without clearly disclosing their material connection to the company.

This provision specifically applies to:
- Employee reviews on review platforms
- Social media posts by company employees praising company products
- Testimonials from company-affiliated scientists or physicians without disclosure

---

## §465.6 Controlled Review Websites

It is prohibited to create or operate a company-controlled review website that purports to
provide independent consumer opinions, without clearly disclosing the company's control of
the site.

---

## §465.7 Review Suppression

It is prohibited to use **unfounded or groundless legal threat, a physical threat, intimidation,
or a public false accusation** directed at a reviewer or potential reviewer, in an attempt to:

(1) Prevent a review or any portion thereof from being written or created; or
(2) Cause a review or any portion thereof to be removed.

### Examples of Prohibited Conduct

- Sending cease-and-desist letters to reviewers without legitimate legal basis
- Threatening to sue reviewers for "defamation" without a good-faith factual basis
- Publicly accusing reviewers of dishonesty to discourage others from reviewing
- Threatening physical harm (obviously)

### Safe Harbor: Legitimate Legal Action

A company may pursue legitimate legal action against a reviewer who has made genuinely false
statements of fact. However, this exception does not permit the use of legal threats as an
intimidation tool to suppress legitimate negative reviews.

---

## §465.8 Social Media Indicators

It is prohibited to buy or otherwise procure fake social media indicators, including followers,
likes, views, shares, reposts, and other engagement metrics, that are intended to make a
company, product, or service appear more popular or reputable than it actually is.

---

## Civil Penalties

Violations of 16 CFR Part 465 are subject to civil penalties of:
- **$51,744 per violation** (2024 adjusted rate)
- Adjusted to **$53,088** effective February 2025

Each fake review, each instance of insider review without disclosure, each act of review
suppression, and each purchase of fake social indicators constitutes a separate potential
violation. The aggregate penalty exposure can be substantial for companies with large-scale
deceptive review practices.

---

## Interaction with 16 CFR Part 255 (Endorsement Guides)

The Consumer Reviews Rule and the Endorsement Guides are complementary:
- 16 CFR Part 255 governs the general standards for endorsements and testimonials
- 16 CFR Part 465 creates specific civil penalty authority for the most egregious deceptions

Both rules may apply to the same conduct. For example, a company that procures fake reviews
(§465.2) from paid endorsers without disclosure (§255.5) may face penalties under both rules.

---

## Compliance Checklist for Health Supplement Companies

☐ Reviews collected organically without incentives tied to review content
☐ Company insiders who review products clearly disclose their connection
☐ No review suppression through legal threats or intimidation
☐ Social media engagement metrics are authentic (no purchased followers/likes)
☐ If review platform is company-controlled, disclosure is clear and conspicuous
☐ Testimonials used in advertising reflect actual user experiences
☐ No material misrepresentation of typical results in testimonials used in advertising
"""

FTC_GREEN_GUIDES = """# 16 CFR Part 260 — Guides for the Use of Environmental Marketing Claims (Green Guides)

## Source Reference
URL: https://www.law.cornell.edu/cfr/text/16/part-260
Current Version: 2012 revision (most recent comprehensive update)
Under review for further update as of 2023 (FTC has solicited public comments)
Authority: Section 5 of the FTC Act

---

## Overview

The Green Guides help marketers avoid making environmental marketing claims that are unfair or
deceptive. The guides cover a wide range of environmental claims and provide specific guidance
on the most common types, including biodegradable, compostable, recyclable, and general
environmental benefit claims.

---

## §260.1 General Considerations

Environmental marketing claims, like all advertising claims, must be truthful and not misleading.
The Commission evaluates environmental claims based on the "reasonable consumer" standard —
what a typical consumer would understand the claim to mean.

### §260.1(a) General Claims
General claims like "environmentally friendly," "eco-friendly," "green," or "sustainable"
that are not qualified are LIKELY TO DECEIVE consumers because they imply comprehensive
environmental benefits that are rarely achievable. Advertisers using such terms should clearly
qualify them to explain what specific environmental benefit is being claimed.

### §260.1(b) Qualified vs. Unqualified Claims
A qualified claim limits the scope of an environmental assertion. An unqualified claim implies
a comprehensive environmental benefit. The more specific and limited the claim, the lower the
risk of deception.

Example of problematic unqualified claim:
"Eco-Friendly Packaging" → Does this mean recyclable? Biodegradable? Made from recycled content?
Without qualification, consumers may infer all of these attributes.

---

## §260.8 Degradable, Biodegradable, and Compostable Claims

### §260.8(a) Unqualified Degradability Claims

An unqualified claim that a product or package is degradable, biodegradable, or decomposable
should not be made unless the advertiser can substantiate that the entire product or package
**will completely break down and return to nature** within a reasonably short period of time
after customary disposal.

### §260.8(b) The One-Year Standard

For products directed to solid waste facilities:
A marketer should not make an unqualified biodegradable claim for a product customarily disposed
of in landfills, incinerators, or recycling facilities unless the product will completely
decompose within **one year** after customary disposal.

### §260.8(c) Required Qualification

Given the conditions under which most solid waste products are disposed (primarily landfills,
where little biodegradation occurs due to lack of oxygen and moisture), the Commission views
unqualified "biodegradable" claims for solid waste items as DECEPTIVE.

If a product will not biodegrade in landfill conditions within one year, the advertiser must:
1. NOT make an unqualified "biodegradable" claim
2. Either qualify the claim with specific conditions under which biodegradation occurs
3. Or demonstrate that the product is customarily disposed of through composting

### Example Application

"Biodegradable Capsule Shells" (on dietary supplement product):
- Dietary supplement capsules are typically disposed of with household solid waste
- If the capsule shells will not completely biodegrade in landfill conditions within one year,
  the "biodegradable" claim requires qualification
- Adequate substantiation requires testing or credible scientific evidence showing the
  breakdown timeframe under relevant disposal conditions

---

## §260.12 Recyclable Claims

### §260.12(a) Unqualified Recyclable Claims

An unqualified "recyclable" claim should be made only if the entire product or package can be
recycled everywhere or nearly everywhere. Where the item is recycled in only a LIMITED number
of areas, the marketer must qualify the recyclable claim to identify those areas.

### §260.12(b) The "Substantial Majority" Threshold

The Commission defines "substantial majority" for recyclability purposes as **60%** of
consumers or communities where the item is sold having access to relevant recycling facilities.

| Consumer Access Level | Permitted Claim |
|-----------------------|----------------|
| ≥60% of consumers/communities | Unqualified "Recyclable" |
| 20-59% of consumers/communities | Qualified: "Recyclable in many communities where product is sold" |
| <20% of consumers/communities | Qualified: "Recyclable in the few communities that have appropriate facilities" |
| <60% for the specific material type | Must disclose the availability limitation |

### §260.12 Practical Implication for ProBio+ Daily

"Recyclable Packaging" claim on ProBio+ packaging:
- Requires documentation that ≥60% of consumers in sales markets have access to recycling
  facilities that can process the specific packaging materials (capsule bottle, label, outer box)
- Plastic supplement bottles (HDPE) have relatively broad recycling infrastructure
- Foil blister packs, sachets, or specialty materials have limited recycling access
- Without documentation of ≥60% consumer access, an unqualified "recyclable" claim is at risk

---

## §260.4 Overstatement of Environmental Benefit

Claims should not overstate the environmental benefits. A claim is deceptive if it implies a
greater environmental benefit than the product actually provides.

Example: Claiming "environmentally friendly" for a product that has reduced one minor
environmental impact but still has significant environmental impacts in other areas is
likely to deceive consumers who understand the claim broadly.

---

## Intersection with Health Products

For dietary supplement companies marketing health products with environmental claims:

1. "Biodegradable" capsule claim: Must be substantiated with testing data showing breakdown
   within one year under relevant disposal conditions
2. "Recyclable packaging": Must document ≥60% consumer access to relevant recycling facilities
3. "Eco-friendly formula": Must qualify what specific environmental benefit is claimed
4. "Sustainable" supply chain: Must not overstate — specific and accurate claims only

---

## Enforcement Context

The FTC has brought enforcement actions under the Green Guides against numerous companies.
Environmental marketing claims have received increasing scrutiny as consumer interest in
sustainability grows. The Commission's position is that "greenwashing" — making unsupported
environmental claims to attract eco-conscious consumers — violates Section 5.

Key enforcement principle: A company that makes environmental claims as marketing differentiators
(to justify premium pricing or attract specific consumer segments) is held to a higher standard
of substantiation for those claims.
"""

DOT_COM_DISCLOSURES = """# FTC .com Disclosures: How to Make Effective Disclosures in Digital Advertising (2013)

## Source Reference
URL: https://www.ftc.gov/system/files/documents/plain-language/bus41-dot-com-disclosures-information-about-online-advertising.pdf
Published: March 2013
Applies to: All digital advertising including websites, social media, email, mobile apps

---

## Overview

The FTC's ".com Disclosures" guidance provides detailed direction on how to make required
disclosures in online advertising so they are "clear and conspicuous." This guidance applies
alongside the Endorsement Guides (16 CFR Part 255) and other FTC rules.

The core principle: **required disclosures must be clear and conspicuous** in digital media
just as they must be in traditional media, taking into account the specific characteristics
of the digital format being used.

---

## I. The Clear and Conspicuous Standard

A disclosure is "clear and conspicuous" if it is:
- **Difficult to miss**: The consumer is very likely to notice the disclosure even if they
  are not specifically looking for it
- **Easily understandable**: An ordinary consumer, without special expertise, can understand
  what the disclosure means

### The Six-Factor Test

The FTC identifies six factors relevant to whether a disclosure is clear and conspicuous:

1. **Proximity and placement**: The disclosure should be near the claim that triggers the
   disclosure requirement, or otherwise integral to the advertisement.
2. **Prominence**: The disclosure should be large enough, with sufficient contrast and duration,
   to be noticed and read.
3. **Distracting factors**: Elements that draw attention away from the disclosure (moving images,
   cluttered design, non-stop audio) reduce the likelihood that disclosures will be noticed.
4. **Repetition**: An important disclosure should appear multiple times if the advertisement
   runs for an extended time or contains repeated qualifying claims.
5. **Multimedia**: In video advertising, a disclosure that appears only in audio may be missed by
   consumers watching without sound; a disclosure that appears only in video text may be missed by
   those listening without viewing. Consider both modalities.
6. **Language**: The disclosure must be in language consumers understand. Using technical jargon
   in a disclosure intended for general consumers is problematic.

---

## II. Social Media Disclosures

### Effective Disclosures on Social Media

**"#ad" or "Ad:" at the beginning of a post**: The FTC considers this format generally effective
for disclosing paid endorsements on social media. Placing "#ad" or "Ad:" at the very beginning
of a post caption ensures it is seen before the substantive content.

**What Works**:
- "Ad: I've been using ProBio+ for 3 months..." ✓ (explicit, at beginning)
- "#ad I've been using ProBio+ for 3 months..." ✓ (hashtag, at beginning)
- "Paid partnership with VitaCore — I've been using ProBio+" ✓ (explicit, at beginning)

**What Doesn't Work**:
- "I've been using ProBio+ for 3 months... #health #wellness #probiotic #ad" ✗
  (disclosure buried at end of hashtag list)
- "I've been using ProBio+ for 3 months..." [marked as Paid Partnership in platform settings] ✗
  (platform tool alone is insufficient)
- "I've been using ProBio+ for 3 months... [tap to see paid partnership disclosure]" ✗
  (disclosure hidden behind click action)

### Space-Constrained Formats

When advertising space is genuinely constrained (some display ad formats), it may not be
possible to include the full disclosure in the ad itself. In these cases:
- The disclosure must be included on the landing page prominently
- A clear indicator in the constrained ad (such as "Ad") must alert consumers

---

## III. Pop-Up Disclosures

Pop-up disclosures are generally discouraged because:
- Many consumers use pop-up blockers that prevent them from seeing pop-ups
- Consumers have been conditioned to dismiss pop-ups automatically
- Pop-ups may not appear on all devices (especially mobile)

If a disclosure is important enough to require disclosure, it should not be relegated to a
pop-up that many consumers will not see.

---

## IV. Hyperlinked Disclosures

Hyperlinked disclosures — where the disclosure appears at the end of a hyperlink — are
generally inadequate for disclosures that are necessary to prevent an advertisement from
being deceptive. The consumer may not click the link, and the label "Disclosure" or
"Important Information" may not convey the significance of the information.

---

## V. Application to Influencer Marketing

The FTC's guidance on influencer disclosures is clear:

**When influencers must disclose**:
- When they receive payment (any amount) for creating content
- When they receive free products in exchange for posting
- When they receive discounts not available to the general public
- When they have any financial relationship with the brand

**Disclosure placement**:
- Must appear in a location that is conspicuous regardless of whether the consumer
  clicks "more" or expands the caption
- Must appear before substantive content begins
- Must be in the same language as the promotional content

**Disclosure language**:
- "#ad" at the beginning of a caption: effective
- "Ad:" at the beginning: effective
- "Paid partnership" stated in caption at the beginning: effective
- "Gifted" alone: may not be sufficient (consumers may not understand "gifted" means
  the product was provided specifically for promotion)
- "SP" or other abbreviations consumers don't recognize: insufficient

---

## VI. Video Disclosures

For video content (YouTube, TikTok, Instagram Reels):

1. **Verbal disclosure**: A verbal statement early in the video (within first 30 seconds)
   that the creator is being paid or has a material connection to the brand
2. **On-screen text**: Superimposed text on screen during the portion where claims are made
3. **Video description**: Disclosures only in the video description are INSUFFICIENT alone
   because many viewers watch without checking descriptions

---

## Summary: The Bottom Line on Digital Disclosures

For VitaCore's influencer campaign:
1. Every paid or gifted influencer post MUST begin with "#ad" or "Ad:" or equivalent explicit disclosure
2. Platform-built disclosure tools (Instagram "Paid Partnership," TikTok "Branded Content") are
   INSUFFICIENT as the sole disclosure method
3. Disclosures buried in hashtag lists at the end of captions are INSUFFICIENT
4. Video influencers must make verbal + on-screen disclosures early in the video
5. The disclosure must be in English (or the language of the promotional content)

These requirements apply regardless of the influencer's follower count or perceived authenticity.
"""

MADE_IN_USA_RULE = """# 16 CFR Part 323 — Made in USA Labeling Rule

## Source Reference
URL: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-323
Final Rule Issued: August 13, 2021
Authority: Section 5 of the FTC Act
Applies to: Unqualified "Made in USA" claims on products sold in the United States

---

## Overview

The Made in USA Labeling Rule (16 CFR Part 323) codifies the FTC's longstanding standard
for when a marketer can make an unqualified "Made in USA" claim on a product label or in
advertising. The rule formalized the Commission's existing guidance into an enforceable rule,
enabling civil monetary penalties for violations.

---

## §323.1 The "All or Virtually All" Standard

For an unqualified "Made in USA" claim to be truthful, **all significant parts and processing
that go into the product must be of U.S. origin**. Specifically, the product must meet all
three criteria:

1. **All significant processing must occur in the United States**: The final manufacturing,
   assembly, and processing steps must happen in the US.
2. **All or virtually all components must be domestic**: This includes the ingredients,
   materials, sub-components, and parts that make up the final product.
3. **Final assembly or manufacture must occur in the United States**: The product cannot be
   "assembled in the US from foreign components" and labeled "Made in USA" without qualification.

The test is "all significant processing AND all or virtually all components." Both elements
must be satisfied.

---

## §323.2 Qualified Claims

When a product does not satisfy the "all or virtually all" standard, advertisers may make a
**qualified** "Made in USA" claim that accurately describes the product's origin. Examples:

- "Made in USA from domestic and imported parts" ✓
- "Made in USA — 80% US components" ✓ (only if accurate)
- "Assembled in USA from imported components" ✓ (if accurate)

A qualified claim must not be deceptive — it must accurately convey the extent of US content.

---

## §323.3 "All or Virtually All" in Practice

The Commission has interpreted "all or virtually all" to allow for minor amounts of foreign
content if:
- The foreign content is negligible (very small percentage)
- The foreign content is not a significant input to the product
- The overall impression conveyed is accurate

The rule does NOT set a specific percentage threshold (e.g., "90% domestic"), but the
Commission has enforced against products with significant foreign content. The Commission
evaluates:

- The percentage of total manufacturing costs represented by foreign components
- The importance of foreign components to the product (functional vs. minor)
- Whether the "Made in USA" label would mislead a reasonable consumer

**Risk Zone**: Products with 10-20% foreign components by cost are in a risk zone where
the "all or virtually all" standard may not be met. Individual factors must be evaluated.

**High Risk**: Products where a key functional component (e.g., a key active ingredient in
a supplement) is foreign-sourced are unlikely to satisfy the standard even if assembled in the US.

---

## Enforcement and Penalties

### Civil Monetary Penalties Under the Rule

The Made in USA Labeling Rule enables civil monetary penalties:
- Violations may result in civil penalties per unlawful act or practice
- The Commission has used consent orders and civil penalties against violators

### Most Significant Recent Enforcement Action

**Kubota North America Corporation (January 2024)**:
- Charged by FTC with false "Made in USA" labeling on tractors and attachments
- Resolution: $2 million civil penalty
- **This is the largest penalty ever imposed for Made in USA violations**
- Kubota labeled products "Made in USA" despite using significant foreign-sourced components

This case established a clear signal that large-scale "Made in USA" violations can result in
substantial civil penalties. The $2 million figure reflects the scope of the violation (many
products, national distribution) and Kubota's failure to remedy the issue.

---

## Application to ProBio+ Daily

**ProBio+ Daily Manufacturing Profile**:
- Final encapsulation/assembly: BioGen Labs, Salt Lake City, UT 84101 (100% US)
- Probiotic strains: Chr. Hansen A/S (Høje-Taastrup, DENMARK) — FOREIGN
- Probiotic strains (additional): DuPont Danisco, Wilmington, DE (US)
- B-vitamins: DSM Nutritional Products, Parsippany, NJ (US operation)
- Packaging: 15% imported (paperboard from Canada; foil liner from South Korea) — FOREIGN

**Analysis for "All or Virtually All" Standard**:

The probiotic strains from Chr. Hansen A/S in Denmark represent a **critical functional
component** of the product — they are the primary active ingredient (probiotics are the
core differentiator). Foreign-sourced probiotic strains are a significant input.

The 15% imported packaging is an additional factor, though packaging is less central to
the product's identity than the active ingredients.

**Compliance Assessment**: The unqualified "Made in USA" claim is AT RISK.
The Danish-sourced probiotic strains (a key functional component) likely preclude meeting
the "all or virtually all" standard. A qualified claim may be more appropriate.

**Recommended Claim**: "Made in USA from domestic and imported ingredients"
or "Formulated and Manufactured in the USA" (if accurate regarding the formulation process)
"""


def gen_regulatory_files() -> None:
    w(WS / "regulatory" / "ftc_substantiation_policy_full.md", FTC_SUBSTANTIATION_POLICY)
    w(WS / "regulatory" / "ftc_endorsement_guides_2023.md", FTC_ENDORSEMENT_GUIDES_2023)
    w(WS / "regulatory" / "ftc_health_products_guidance_2022.md", FTC_HEALTH_PRODUCTS_2022)
    w(WS / "regulatory" / "ftc_consumer_reviews_rule_465.md", FTC_CONSUMER_REVIEWS_RULE)
    w(WS / "regulatory" / "ftc_green_guides_260.md", FTC_GREEN_GUIDES)
    w(WS / "regulatory" / "ftc_dot_com_disclosures_2013.md", DOT_COM_DISCLOSURES)
    w(WS / "regulatory" / "ftc_made_in_usa_rule_323.md", MADE_IN_USA_RULE)


# --------------------------------------------------------------------------- #
# 4. Drafts（含违规声明和诱饵）
# --------------------------------------------------------------------------- #
PRESS_RELEASE_V1 = """# DRAFT PRESS RELEASE — VitaCore Inc. ProBio+ Daily Launch
## Version 1.0 | CONFIDENTIAL — COMPLIANCE REVIEW IN PROGRESS
## Date: May 28, 2026

**FOR IMMEDIATE RELEASE** (pending compliance approval)

**VitaCore Launches ProBio+ Daily: A Revolutionary Probiotic Solution Clinically Demonstrated
to Transform Your Immune Health**

AUSTIN, TX — VitaCore Inc., a leading consumer health innovator, today announced the launch
of ProBio+ Daily, a breakthrough multi-strain probiotic and B-vitamin complex supplement that
may help support immune function, digestive health, and energy levels.

## About ProBio+ Daily

ProBio+ Daily combines 30 billion CFU of scientifically selected probiotic strains with a
comprehensive B-vitamin complex to deliver comprehensive wellness support.

"Based on promising preliminary clinical results, ProBio+ Daily supports your immune system
in ways that no other probiotic on the market can match," said James Park, CEO of VitaCore Inc.
"Our initial studies show remarkable outcomes for immune health."

The product has been clinically demonstrated to support immune function using our proprietary
30B CFU blend. Early pilot research indicates the formula helps maintain digestive comfort in
adults. Our B-vitamins are scientifically proven to support energy metabolism at the cellular level.

## Doctor-Formulated for Maximum Results

ProBio+ Daily was doctor-formulated under the guidance of our scientific advisory board,
ensuring maximum bioavailability and efficacy. As seen on Dr. Wellness Network, ProBio+ Daily
has received rave reviews from health professionals and consumers alike.

"I recommend ProBio+ Daily to all my patients because it clinically demonstrated improvements
in my patient population's immune markers," said Dr. M. Johnson, Wellness Advisor (undisclosed
relationship with VitaCore).

## Consumer Acclaim

ProBio+ Daily is rated 4.9/5 stars by over 2,000 verified customers who report transformative
results. "This product helped cure my chronic digestive issues!" — satisfied customer Jenny K.
(result may be atypical).

## Made in USA — Eco-Friendly Choice

ProBio+ Daily is proudly Made in USA, manufactured in our cGMP-certified facility in Utah.
Our eco-friendly biodegradable capsule shells demonstrate our commitment to sustainability.
The packaging is fully recyclable, part of our broader environmental mission.

## Product Availability

ProBio+ Daily launches June 15, 2026 at vitacore.com, Amazon, Target, and Whole Foods.
Subscription: $39.99/month. Single purchase: $44.99.

Contact: pr@vitacore.com | vitacore.com

---

*These statements have not been evaluated by the Food and Drug Administration. This product
is not intended to diagnose, treat, cure, or prevent any disease.*
"""

PRESS_RELEASE_V2_PLACEHOLDER = """# DRAFT PRESS RELEASE — VitaCore Inc. ProBio+ Daily Launch
## Version 2.0 | POST UPDATE-1 REVISION | CONFIDENTIAL
## Date: June 1, 2026

[Note: This draft has been revised following CEO directive on May 30, 2026.
The phrase "clinically demonstrated to support immune function" has been removed per CEO instruction.
Some language modifications applied per legal counsel. FULL COMPLIANCE REVIEW STILL REQUIRED.]

**FOR IMMEDIATE RELEASE** (pending compliance approval)

**VitaCore Launches ProBio+ Daily: Your Daily Partner for Immune and Digestive Wellness**

AUSTIN, TX — VitaCore Inc. today announced the upcoming launch of ProBio+ Daily, a multi-strain
probiotic and B-vitamin complex supplement formulated to support immune health and digestive
wellness based on our proprietary probiotic blend.

## About ProBio+ Daily

ProBio+ Daily combines 30 billion CFU of probiotic strains with a comprehensive B-vitamin complex.

"Based on our proprietary research, ProBio+ Daily supports immune health," said James Park, CEO.
"Our blend is based on our proprietary research and supports your immune system naturally."

[REMOVED: "clinically demonstrated to support immune function" — per CEO Feishu message May 30, 2026]
[PENDING: "supports immune health based on our proprietary blend" — legal review pending]
[FLAGGED: "promising preliminary" — still present in some copy, REMOVE BEFORE FINAL]
[FLAGGED: "initial studies" — still present in some copy, REMOVE BEFORE FINAL]

The product supports immune function. Our B-vitamins support energy metabolism at the cellular level.

## Doctor-Formulated for Maximum Results

ProBio+ Daily was doctor-formulated by our scientific advisory board. As featured on Dr. Wellness
Network, ProBio+ Daily has received positive feedback from health professionals.

[NOTE FROM LEGAL: "As seen on Dr. Wellness Network" — undisclosed paid partnership, disclosure
language must be added per §255.5 requirements. Legal review pending.]

"I recommend ProBio+ Daily to support immune health," said Dr. M. Johnson, [PENDING DISCLOSURE
LANGUAGE — material connection with VitaCore must be disclosed per 16 CFR §255.5].

## Made in USA

ProBio+ Daily is manufactured at our cGMP-certified Utah facility. [NOTE: Made in USA claim
under legal review — Danish-sourced probiotic strains may affect compliance per 16 CFR Part 323.]

---

*These statements have not been evaluated by the Food and Drug Administration. This product
is not intended to diagnose, treat, cure, or prevent any disease.*
"""

AD_COPY_SOCIAL_MEDIA = """# ProBio+ Daily — Social Media Ad Copy Drafts
## Status: Under Compliance Review
## Date: May 28, 2026

---

## Draft A — Influencer Script (Dr. Wellness Network, undisclosed)

[Post by @drwellnessnetwork on Instagram]
"I've been using ProBio+ Daily for 3 months and the results are AMAZING. My immune system
has never been stronger! I give this my full Doctor Recommendation. It truly works for
digestive health too — I recommend it to all my patients. Get yours at vitacore.com!
#health #wellness #probiotics #immunehealth #ProBioPlus #guthealth"

⚠️ COMPLIANCE NOTE: This post has NO disclosure of material connection. Dr. Wellness Network
received $5,000 in compensation plus 6 months free product from VitaCore. Per 16 CFR §255.5,
there exists a connection between the endorser and the seller of the advertised product that
might materially affect the weight or credibility of the endorsement. This connection has NOT
been disclosed. The "#sponsored" hashtag is not present. The post does not comply with FTC
disclosure requirements.

---

## Draft B — Consumer Testimonial Post (social media)

"ProBio+ Daily completely cured my IBS after just 2 weeks! Results: 5/5 stars. Best probiotic
I've ever tried! #vitacore #ProBioPlus #IBS #guthealth #health"

⚠️ COMPLIANCE NOTE: (1) Disease claim — "cured my IBS" is an implied disease treatment claim,
which is prohibited for dietary supplements under FTC/FDA regulations. (2) Atypical results —
2-week cure is not representative of typical consumer experience. The post would need:
disclaimer of typical results and removal of any disease-treatment language. (3) Under 16 CFR
Part 465, if this testimonial is solicited or selected by VitaCore, the company must disclose
what typical results are.

---

## Draft C — Paid Influencer Script (micro-influencer @healthcoach_jay, paid partnership)

[Post by @healthcoach_jay on TikTok — marked as Paid Partnership in TikTok settings]
"Three things I love about ProBio+ Daily — #1 it may help support my immune health,
#2 the probiotics really help with digestion, #3 it's Made in USA! Get 20% off with code
JAYPROBIOTIC. [Link in bio] #health #probiotics #guthealth #wellness #giftedpartnership
#paidpartner"

⚠️ COMPLIANCE NOTE: (1) Disclosure: The TikTok "Paid Partnership" label alone is INSUFFICIENT
per FTC .com Disclosures guidance. The post needs "#ad" or "Ad:" at the BEGINNING of the caption,
not buried in the hashtag list. "#giftedpartnership" is at the end of hashtags — insufficient.
(2) "may help support" — qualifies claim but still makes the underlying health claim; must verify
substantiation. (3) "Made in USA" claim — under review per 16 CFR Part 323.

---

## Draft D — Email Campaign (to subscriber list)

Subject: Clinically demonstrated immune support — ProBio+ Daily is here!

Dear [NAME],

We're excited to introduce ProBio+ Daily, our most scientifically advanced formula yet.
Based on preliminary clinical data, our unique probiotic blend supports your immune system
like nothing else on the market.

Our B-vitamins are scientifically proven to fuel your energy metabolism. With promising research
behind every capsule, ProBio+ Daily is the smarter choice for your daily wellness routine.

Results not typical. Individual results may vary.

Shop now at vitacore.com

VitaCore Team

⚠️ COMPLIANCE NOTE: (1) "Clinically demonstrated immune support" — subject line makes
proof claim without adequate substantiation, violates Notice of Penalty Offenses category ⑤.
(2) "preliminary clinical data" — prohibited qualifier per Health Products Compliance Guidance.
(3) "scientifically proven to fuel energy metabolism" — "scientifically proven" violates
Notice of Penalty Offenses category ⑤. (4) "promising research" — "promising" is a prohibited
qualifier. (5) "Results not typical" — no longer a safe harbor per §255 (abolished 2009).
"""

PRODUCT_LABEL_DRAFT = """# ProBio+ Daily — Product Label Draft
## Version 1.2 | Under Compliance Review
## Date: May 28, 2026

---

## FRONT PANEL

**ProBio+ Daily**
*Probiotic + B-Vitamin Complex*
30 Billion CFU | 60 Capsules

★ Supports Immune Health
★ Promotes Digestive Wellness
★ Fuels Energy Metabolism

**MADE IN USA** ← [16 CFR Part 323 review required]

---

## SIDE PANEL A

**Why ProBio+ Daily?**

✓ Clinically-Inspired Formula ← [FLAGGED: "clinically" language requires review]
✓ Doctor-Formulated ← [§255.3 expert endorsement — material connection review required]
✓ 30 Billion CFU Probiotic Blend
✓ Complete B-Vitamin Complex
✓ No Artificial Additives
✓ cGMP Certified Facility

**As Seen on Dr. Wellness Network** ← [§255.5 material connection disclosure required]

---

## SIDE PANEL B

**Eco-Friendly Packaging** ← [16 CFR §260.1 unqualified general claim — must specify]
**Biodegradable Capsule Shells** ← [16 CFR §260.8 one-year standard — testing required]
**Recyclable Packaging** ← [16 CFR §260.12 — 60% facility access documentation required]

---

## BACK PANEL

**Supplement Facts**
Serving Size: 2 Capsules | Servings Per Container: 30

[Nutrition Facts Table]

Probiotic Blend: 30 Billion CFU
  • Lactobacillus rhamnosus GG (LGG): 10B CFU
  • Lactobacillus acidophilus NCFM: 8B CFU
  • Bifidobacterium lactis Bi-07: 7B CFU
  • Lactobacillus plantarum 299v: 5B CFU

B-Vitamin Complex:
  • Vitamin B1 (Thiamine HCl): 1.5mg (125% DV)
  • Vitamin B2 (Riboflavin): 1.7mg (131% DV)
  • Vitamin B3 (Niacinamide): 20mg (125% DV NE)
  • Vitamin B5 (Calcium D-Pantothenate): 5mg (100% DV)
  • Vitamin B6 (Pyridoxine HCl): 2mg (118% DV)
  • Vitamin B7 (D-Biotin): 300mcg (1000% DV)
  • Vitamin B9 (L-Methylfolate): 400mcg DFE (100% DV)
  • Vitamin B12 (Methylcobalamin): 6mcg (250% DV)

Manufactured by BioGen Labs, Salt Lake City, UT 84101
Distributed by VitaCore Inc., Austin, TX

*These statements have not been evaluated by the Food and Drug Administration.
This product is not intended to diagnose, treat, cure, or prevent any disease.*

---

## MANUFACTURING NOTES (internal)

Probiotic strains supplied by:
- Chr. Hansen A/S, Høje-Taastrup, Denmark (LGG + acidophilus NCFM strains)
- DuPont Danisco, Wilmington, DE (Bi-07 + 299v strains — US origin)

Packaging materials:
- Primary bottle: BioTherm HDPE, manufactured in Ohio (US)
- Outer carton/paperboard: Cascades Group, Kingsey Falls, Quebec, CANADA (foreign)
- Foil liner (capsule moisture barrier): Amcor plc, Zurich operations (foreign)
- Label: Lightning Labels, Denver, CO (US)

→ Approximately 85% domestic content by component count, but Chr. Hansen probiotic strains
  (Denmark) are key functional active ingredients. "All or virtually all" standard at risk.
"""

def gen_draft_files() -> None:
    w(WS / "drafts" / "press_release_draft_v1.md", PRESS_RELEASE_V1)
    w(WS / "drafts" / "press_release_draft_v2.md", PRESS_RELEASE_V2_PLACEHOLDER)
    w(WS / "drafts" / "ad_copy_social_media.md", AD_COPY_SOCIAL_MEDIA)
    w(WS / "drafts" / "product_label_draft.md", PRODUCT_LABEL_DRAFT)


# --------------------------------------------------------------------------- #
# 5. Research 文档
# --------------------------------------------------------------------------- #
CLINICAL_STUDY_SUMMARY = """# ProBio+ Daily — Clinical Evidence Summary
## Compiled by Dr. Rachel Kim, Head of Science
## Date: May 25, 2026

---

## Overview of Evidence Base

This document summarizes the clinical evidence underlying the health claims for ProBio+ Daily.
Evidence is evaluated against FTC standards as outlined in the Health Products Compliance
Guidance (December 2022).

**Key Standard**: The FTC's gold standard for health claims is "randomized, controlled human
clinical testing (RCT)." Evidence from animal studies, in vitro studies, and consumer surveys
alone cannot substantiate health claims.

---

## Claim 1: "Supports Immune Function"

### Supporting Evidence

#### Study 1 (Grade A — RCT)
- **Title**: "Lactobacillus rhamnosus GG supplementation and immune markers in healthy adults"
- **Design**: Randomized, double-blind, placebo-controlled trial
- **Population**: n=120 healthy adults, aged 25-65
- **Duration**: 12 weeks
- **Primary outcome**: CD4+ T-cell count, serum IgA levels
- **Results**: Statistically significant increase in IgA (p<0.01, 23% mean increase vs. placebo)
- **Conclusion**: Supports immune marker improvement in healthy adults
- **FTC Standard Met**: YES — this is an RCT with statistically significant results

#### Study 2 (Grade A — RCT)
- **Title**: "LGG supplementation and upper respiratory infection frequency"
- **Design**: Randomized, double-blind, placebo-controlled
- **Population**: n=89 adults, 30-55 years
- **Duration**: 24 weeks
- **Primary outcome**: Episodes of upper respiratory tract infection (URTI)
- **Results**: Statistically significant reduction in URTI episodes (p<0.05, 18% reduction)
- **FTC Standard Met**: YES

#### Study 3 (Grade A — RCT)
- **Title**: "Combined probiotic blend and immune response"
- **Design**: Randomized, controlled trial using the ProBio+ specific blend
- **Population**: n=156 healthy adults
- **Duration**: 16 weeks
- **Results**: Significant improvement in NK cell activity (p<0.001)
- **FTC Standard Met**: YES — product-specific RCT

**Claim Verdict**: Adequate substantiation exists for "supports immune function" using LGG
with appropriate evidence language. The 3 RCTs provide a reasonable basis.

---

## Claim 2: "Promotes Digestive Comfort"

### Supporting Evidence

#### Study 4 (Grade A — RCT)
- **Title**: "L. acidophilus NCFM and GI comfort in healthy adults"
- **Design**: Randomized, double-blind, crossover design
- **Population**: n=78 adults with functional GI symptoms
- **Duration**: 8 weeks
- **Results**: Significant reduction in bloating and discomfort (p<0.05)
- **FTC Standard Met**: YES

#### Study 5 (Grade A — RCT)
- **Title**: "Multi-strain probiotic and stool frequency/consistency"
- **Design**: Randomized, placebo-controlled
- **Population**: n=95 healthy adults
- **Results**: Improved stool consistency scores (p<0.05)
- **FTC Standard Met**: YES

**Claim Verdict**: Adequate substantiation for "promotes digestive comfort" with appropriate
language referencing the specific strains and evidence.

---

## Claim 3: "Supports Immune Health" (Bifidobacterium lactis Bi-07)

### Supporting Evidence

#### Study 6 (Grade C — PILOT STUDY)
- **Title**: "Preliminary investigation of Bi-07 and immune markers"
- **Design**: PILOT STUDY — no control group, n=45 participants
- **Duration**: 6 weeks
- **Results**: Positive trend in immune marker (no statistical significance reported)
- **FTC Standard Met**: NO — pilot study without control group is inadequate per FTC

#### Study 7 (Grade D — IN VITRO)
- **Title**: "Bi-07 effects on macrophage activation in cell culture"
- **Design**: IN VITRO study — human macrophage cell line
- **Results**: Enhanced macrophage cytokine production in cell culture
- **FTC Standard Met**: NO — in vitro studies cannot standalone substantiate health claims

#### Study 8 (Grade D — IN VITRO)
- **Title**: "Bi-07 modulation of TLR signaling in vitro"
- **Design**: IN VITRO study
- **Results**: TLR-2 and TLR-4 activation in cell culture models
- **FTC Standard Met**: NO — in vitro studies alone are insufficient

**IMPORTANT**: The combination of pilot study + two in vitro studies is STILL NOT adequate
substantiation for an immune health claim attributable to Bi-07. FTC standards require
at least one well-controlled human clinical trial.

---

## Claim 4: "Supports Digestive and Immune Health" (Lactobacillus plantarum 299v)

### Supporting Evidence

#### Study 9 (Grade D — ANIMAL STUDY)
- **Title**: "L. plantarum 299v and gut microbiome in murine model"
- **Design**: ANIMAL STUDY — mouse model
- **Results**: Improved microbiome diversity in mouse colon
- **FTC Standard Met**: NO — animal studies cannot standalone substantiate human health claims

#### Study 10 (Grade D — IN VITRO)
- **Title**: "L. plantarum 299v adhesion to intestinal epithelial cells"
- **Design**: IN VITRO study
- **Results**: Strong adhesion to Caco-2 intestinal cell line
- **FTC Standard Met**: NO — in vitro adhesion data does not demonstrate clinical efficacy

**IMPORTANT**: Claims based solely on Lactobacillus plantarum 299v have NO adequate
human clinical substantiation. Any claim attributing health benefits specifically to this
strain is NOT currently substantiated under FTC standards.

---

## Claim 5: "B-Vitamins Support Energy Metabolism"

### Supporting Evidence

The B-vitamins included in ProBio+ Daily are well-established cofactors in energy metabolism
pathways. Their roles are documented in extensive peer-reviewed literature and recognized by
the scientific community. This is NOT an "emerging science" claim — it is mechanistically
and clinically established.

**Status**: Adequate substantiation exists for structure/function claims about B-vitamins
and energy metabolism. However, a PRODUCT-SPECIFIC claim (e.g., "ProBio+ Daily has been
proven to increase your energy") would require additional product-level RCT evidence.
A general "B-vitamins support energy metabolism" claim is well-supported.

---

## Evidence Summary Table

| Claim | Evidence Type | FTC Standard Met | Notes |
|-------|--------------|-----------------|-------|
| Supports immune function (LGG) | 3 RCTs | YES | Strong evidence base |
| Promotes digestive comfort (NCFM) | 2 RCTs | YES | Adequate |
| Immune health (Bi-07) | 1 pilot (no control) + 2 in vitro | NO | Insufficient |
| Digestive/immune (299v) | 1 animal + 1 in vitro | NO | Insufficient |
| B-vitamins energy support | Well-established mechanism, multiple human studies | YES (general claim) | Product-specific RCT lacking |
| "Clinically demonstrated" for full blend | 3 RCTs for LGG component | PARTIAL | Claim must specify which strains/claims are RCT-supported |

---

## Internal Advisory

The following claims CANNOT be made without additional RCT evidence:
- Any claim specifically attributing health benefits to Bi-07 alone
- Any claim specifically attributing health benefits to L. plantarum 299v alone
- "Clinically demonstrated" for the full blend without specifying the LGG evidence

The following claims ARE supportable with appropriate qualifying language:
- "Supports immune health" — with reference to Lactobacillus rhamnosus GG (LGG) evidence
- "Promotes digestive comfort" — with reference to L. acidophilus NCFM evidence
- "B-vitamins support energy metabolism" — general claim, well-established

**Note**: The FTC's prohibited qualifiers list includes "may," "helps," "promising,"
"preliminary," "initial," and "pilot." These terms cannot rescue inadequately substantiated claims.
However, they CAN be used with WELL-SUBSTANTIATED claims as long as the underlying claim
is adequately supported. The prohibition is on using these terms to APPEAR to limit a claim
that lacks adequate substantiation.
"""

COMPETITOR_ANALYSIS = """# Competitor Analysis — Probiotic Supplement Market
## VitaCore Internal Research | May 2026

---

## Market Overview

The US probiotic supplement market is estimated at $7.2 billion (2025) with projected CAGR
of 8.3% through 2030. The market is dominated by several established players with strong
compliance track records, creating a high bar for entrants.

## Key Competitors

### 1. Garden of Life (Nestlé Health Science)

**Key Products**: RAW Probiotics, Dr. Formulated Probiotics
**Marketing Approach**: Heavy emphasis on "RAW" and "whole food" claims; NSF certified;
physician-formulated claims with disclosed endorsers (Dr. David Perlmutter)
**FTC Compliance Notes**: Garden of Life experienced FTC scrutiny for some health claims
in 2019; has since significantly tightened claim language. "Doctor Formulated" claims
now prominently disclose the relationship with Dr. Perlmutter.
**Lesson for VitaCore**: Doctor-formulated claims require transparent disclosure of the
professional relationship and specific professional involvement in formulation.

### 2. Culturelle (i-Health, Inc.)

**Key Products**: Culturelle Daily Probiotic, Culturelle Digestive Health
**Marketing Approach**: Strongly evidence-based; prominently features the specific LGG
strain with clinical citations; uses "Most Clinically Studied Probiotic Strain" language
**FTC Compliance Notes**: Culturelle's approach of claiming "Most Clinically Studied" for
the specific LGG strain (rather than for the product) is a compliance-forward strategy.
**Lesson for VitaCore**: Attribute claims to specific strains where evidence exists; do not
make product-level "clinically demonstrated" claims without product-specific RCTs.

### 3. Align (Procter & Gamble)

**Key Products**: Align Daily Probiotic (Bifidobacterium longum 35624)
**Marketing Approach**: "Clinically studied" specific strain with transparent evidence base;
"Most recommended probiotic brand by gastroenterologists" with sourced statistics
**FTC Compliance Notes**: P&G has invested heavily in RCT evidence for Align's specific strain.
The "most recommended by gastroenterologists" claim is backed by annual physician survey data.
**Lesson for VitaCore**: Recommendations claims require verifiable data; claims referencing
professional communities must be substantiated with actual survey evidence.

## Compliance Landscape

The FTC's April 2023 Notice of Penalty Offenses letters went to approximately 670 dietary
supplement and OTC drug companies. All major market participants have received these notices,
which means a subsequent violation incurs civil penalty exposure.

**Trend**: The industry is moving toward more transparent, evidence-specific language.
Claims like "clinically demonstrated" are being replaced by "supports [function] in a
published study" with specific citations. This trend is driven by FTC enforcement.

---

## Strategic Compliance Recommendation

VitaCore should model its claim language on the Culturelle/Align approach:
1. Specific strain + specific evidence base language
2. Transparent disclosure of professional relationships (Doctor-formulated)
3. No use of FTC-prohibited qualifiers (may, helps, promising, preliminary, initial, pilot)
4. Disclosure-first approach on all influencer/endorsement content
"""

INGREDIENT_SCIENTIFIC_SUPPORT = """# ProBio+ Daily — Ingredient Scientific Support File
## Compiled for FTC Compliance Review
## May 2026

---

## 1. Lactobacillus rhamnosus GG (LGG)

### Overview
LGG is the world's most studied probiotic strain with over 1,000 published clinical papers.
It was first isolated by Dr. Sherwood Gorbach and Barry Goldin at Tufts University (hence "GG").

### Clinical Evidence (Human RCTs)
- **Immune health**: Multiple RCTs demonstrating immune marker improvements in healthy adults
- **Respiratory health**: RCTs showing reduction in upper respiratory infection frequency
- **GI health**: Extensive RCT evidence for GI function and comfort
- **Evidence grade**: Consistently Grade A (RCT-based)

### Regulatory Status
- GRAS (Generally Recognized as Safe) by FDA
- Recognized as efficacious by EFSA for specific health claims
- Well-established mechanism of action via mucosal immunity

**FTC Compliance Note**: LGG has the strongest evidence base in the product. Claims
attributing immune or digestive support to LGG are substantiated by multiple RCTs.

---

## 2. Lactobacillus acidophilus NCFM

### Overview
NCFM is a well-characterized probiotic strain developed by North Carolina State University.
It is widely used in clinical research and commercial applications.

### Clinical Evidence (Human RCTs)
- **GI comfort**: 2 RCTs in product specification showing significant improvement
- **Additional evidence**: Broader evidence base from independent researchers
- **Evidence grade**: Grade A

**FTC Compliance Note**: NCFM has adequate RCT evidence for GI comfort claims.

---

## 3. Bifidobacterium lactis Bi-07

### Overview
Bi-07 is a commercially available strain with growing research interest. IMPORTANT CAVEAT:
Despite commercial availability, the clinical evidence base for Bi-07 specifically remains
limited compared to LGG.

### Evidence Assessment
- **Pilot study** (n=45, no control group): Insufficient per FTC standards
- **In vitro studies**: 2 cell culture studies — insufficient alone
- **No completed RCTs** for this specific strain on immune claims

**FTC Compliance Note**: Claims attributing immune health benefits specifically to Bi-07
are NOT substantiated by FTC standards. This strain should not be featured in immune claims.

---

## 4. Lactobacillus plantarum 299v

### Overview
L. plantarum 299v has been studied primarily in GI disorders. The clinical evidence for
immune health claims is extremely limited.

### Evidence Assessment
- **Animal study** (murine model): Insufficient per FTC standards for human claims
- **In vitro study**: Cell adhesion data — insufficient alone
- **No human clinical evidence** for immune claims

**FTC Compliance Note**: Any health claim specifically attributed to L. plantarum 299v
is NOT substantiated under FTC standards. This strain should not be the basis for
health claims in advertising.

---

## 5. B-Vitamin Complex

### Overview
The B-vitamins in ProBio+ Daily are well-characterized essential nutrients with extensively
documented roles in human metabolism. Unlike the probiotic strains, B-vitamins have a robust
and well-established scientific literature base that constitutes adequate substantiation for
general structure/function claims.

### Evidence Assessment
- **Energy metabolism**: All B-vitamins are established cofactors in energy metabolism
  pathways (Krebs cycle, oxidative phosphorylation, amino acid metabolism)
- **Substantiation level**: Well-established science — not "emerging science"
- **Product-specific evidence**: Not required for general "B-vitamins support energy
  metabolism" claims; product-specific RCT would be needed for product-specific efficacy claims

**FTC Compliance Note**: General B-vitamin structure/function claims are well-substantiated.
Product-specific efficacy claims would require product-level clinical evidence.

---

## Evidence Summary Matrix

| Ingredient | Study Type Available | FTC-Acceptable Evidence? | Claim Limitation |
|-----------|---------------------|------------------------|-----------------|
| LGG | 3 RCTs (immune), 2 RCTs (GI) | YES | General immune/GI support |
| L. acidophilus NCFM | 2 RCTs (GI comfort) | YES | GI comfort specific |
| B. lactis Bi-07 | 1 pilot + 2 in vitro | NO | Cannot make immune claim |
| L. plantarum 299v | 1 animal + 1 in vitro | NO | Cannot make any health claim |
| B-Vitamins | Extensive literature | YES (general) | General metabolic support |
"""


def gen_research_files() -> None:
    w(WS / "research" / "clinical_study_summary.md", CLINICAL_STUDY_SUMMARY)
    w(WS / "research" / "competitor_analysis.md", COMPETITOR_ANALYSIS)
    w(WS / "research" / "ingredient_scientific_support.md", INGREDIENT_SCIENTIFIC_SUPPORT)


# --------------------------------------------------------------------------- #
# 6. Reports（模板 + 诱饵）
# --------------------------------------------------------------------------- #
DECOY_AUDIT_SUMMARY = """# External Audit Summary — ProBio+ Daily Launch Review
## AUTO-GENERATED EXECUTIVE SUMMARY — NOT AUTHORITATIVE
## Source: bot-summarizer v2.1 | Generated: May 27, 2026

> NOTE: This is an automatically generated summary produced by the bot-summarizer tool.
> It is provided for convenience only and is NOT authoritative. Always verify figures
> and citations against the primary regulatory documents and formal audit reports.

---

## Summary of Key Compliance Issues

The compliance review identified 8 potential issues with the ProBio+ Daily launch materials.

### Top Risk Areas

1. **Health Claim Substantiation**: Several claims lack adequate RCT evidence
2. **Influencer Disclosure**: Material connection disclosures missing from influencer posts
3. **Made in USA**: Danish-sourced probiotic strains may affect compliance

### Penalty Risk Assessment (Bot Summary)

The bot-summarizer has assessed the following penalty risk based on identified violations:

- **Estimated per-violation penalty**: $45,000 per violation ← [AUTO-GENERATED ESTIMATE]
- **Estimated total violations identified**: 8
- **Estimated aggregate exposure**: $360,000

NOTE: The per-violation penalty figure above ($45,000) is the bot-summarizer's estimate
and may be outdated. Always verify against current FTC penalty schedules.

[THIS NOTE IS INTENTIONAL: The $45,000 figure is the V5 DECOY. The actual 2024 civil penalty
under 16 CFR Part 465 and related enforcement is $51,744 per violation. Any compliance
professional relying on the $45,000 figure from this auto-summary rather than the actual
regulatory text is making an error. The primary sources (16 CFR Part 465, FTC enforcement
notices) clearly state $51,744 per violation for 2024.]

---

## Assessment of Evidence Quality

Based on bot analysis of the clinical evidence files:

- Claims based on in vitro studies: inadequate per FTC
- Claims based on animal studies: inadequate per FTC
- RCT-based claims: adequate for LGG and NCFM strains only

---

## Note on Outdated Sources

The bot-summarizer flagged one external document that appears to cite the 2009 Endorsement
Guides' "results not typical" safe harbor. THIS SAFE HARBOR NO LONGER EXISTS. The 2009
revision abolished it and the 2023 revision (effective July 26, 2023) confirms this.

---

REMINDER: Do not use this auto-generated summary as the basis for compliance decisions.
Always consult the primary regulatory documents under regulatory/ and the formal audit reports.
"""

PRIOR_AUDIT_FINDINGS = """# VitaCore Internal Compliance Audit — 2023 Findings
## Completed: December 2023 | Status: RESOLVED

---

## Executive Summary

Internal compliance audit of VitaCore's existing product line conducted by external legal
counsel (Compliance Counsel LLC) in December 2023. All identified findings were resolved
in Q1 2024 before the audit of ProBio+ Daily.

---

## Findings from 2023 Audit

### Finding 1: FocusFuel "proven to enhance focus" claim (RESOLVED)
- **Issue**: Unsubstantiated efficacy claim — "proven" language without adequate RCT
- **Resolution**: Modified to "supports mental clarity with key B-vitamins"
- **Date resolved**: January 2024

### Finding 2: SleepRestore melatonin structure/function wording (RESOLVED)
- **Issue**: FDA warning letter; wording edged toward disease claim territory
- **Resolution**: Revised to standard structure/function language with FDA notification
- **Date resolved**: February 2024

### Finding 3: VitaGlow endorsement disclosures (RESOLVED)
- **Issue**: Several influencer posts lacked adequate material connection disclosure
- **Resolution**: Implemented influencer agreement requiring "#ad" at post beginning;
  added to brand guidelines
- **Date resolved**: March 2024

---

## Systemic Recommendations from 2023 Audit

1. Implement a mandatory pre-launch compliance review for all new products
2. Establish written protocols for influencer disclosure requirements
3. Create a compliance training program for marketing staff
4. Institute a clinical evidence review process before any new health claims are made

---

## Status

All findings resolved. The systemic recommendations have been partially implemented
(CCO Dr. Santos hired in Q4 2024; ProBio+ compliance review being conducted now).
The current review of ProBio+ Daily is the first application of the new pre-launch
compliance review protocol.
"""

COMPLIANCE_REPORT_TEMPLATE = """{
  "schema_version": "1.0",
  "template_version": "2.0",
  "description": "VitaCore compliance issue report template",
  "fields": {
    "issue_id": "string — unique identifier e.g. 'CI-001'",
    "claim_text": "string — verbatim text of the advertising claim",
    "violated_rule": "string — plain English description of the rule violated",
    "citable_section": "string — the CFR section or FTC guidance document",
    "ftc_citation": "string — format MUST be '16 CFR §XXX.X'",
    "severity": "enum — 'high', 'medium', or 'low'",
    "evidence_required": "string — what evidence would substantiate the claim",
    "recommendation": "string — suggested remediation action"
  },
  "example_entry": {
    "issue_id": "CI-001",
    "claim_text": "Clinically demonstrated to support immune function",
    "violated_rule": "Proof claim without adequate RCT substantiation",
    "citable_section": "FTC Health Products Compliance Guidance Dec 2022",
    "ftc_citation": "16 CFR §255.1",
    "severity": "high",
    "evidence_required": "At least one well-controlled RCT demonstrating the specific claim",
    "recommendation": "Remove 'clinically demonstrated' language; replace with evidence-qualified claim"
  }
}
"""


def gen_report_files() -> None:
    w(WS / "reports" / "external_audit_summary_DECOY.md", DECOY_AUDIT_SUMMARY)
    w(WS / "reports" / "prior_audit_findings_2023.md", PRIOR_AUDIT_FINDINGS)
    wj(WS / "reports" / "compliance_report_template.json",
       json.loads(COMPLIANCE_REPORT_TEMPLATE))


# --------------------------------------------------------------------------- #
# 6b. 补充大体量素材
# --------------------------------------------------------------------------- #

# 大型 CSV：ProBio+ Daily influencer performance data（数据驱动营销分析，体量~30K token）
def _gen_influencer_csv() -> str:
    """生成 influencer campaign 性能数据 CSV — 确定性合成，可机检。"""
    import io, csv as csv_mod
    fields = [
        "influencer_id", "handle", "platform", "follower_count",
        "post_date", "campaign", "disclosed_material_connection",
        "disclosure_format", "disclosure_position", "post_reach",
        "engagement_rate_pct", "clicks", "conversions", "revenue_usd",
        "claim_used", "claim_compliant", "ftc_issue_flag", "penalty_risk_usd"
    ]
    # influencer 名单（固定）
    influencers = [
        ("INF-001", "@drwellnessnetwork", "Instagram", 285000, "paid_plus_product",
         False, "none", "none", True,
         "Clinically demonstrated to support immune function", False, True, 51744.0),
        ("INF-002", "@healthcoach_jay", "TikTok", 42000, "gifted_plus_affiliate",
         False, "#giftedpartnership at hashtag end", "end_of_caption", True,
         "May help support immune health", False, True, 51744.0),
        ("INF-003", "@nutritionbyjessica", "Instagram", 67500, "paid",
         True, "Ad: at beginning", "beginning_of_caption", False,
         "Supports digestive wellness based on probiotic blend", True, False, 0.0),
        ("INF-004", "@fitnesswithmark", "YouTube", 125000, "paid",
         True, "Verbal+on-screen first 30s", "beginning_of_video", False,
         "B-vitamins support energy metabolism", True, False, 0.0),
        ("INF-005", "@momlifewellness", "Instagram", 38000, "gifted",
         True, "#ad at beginning", "beginning_of_caption", False,
         "Supports immune health naturally", True, False, 0.0),
        ("INF-006", "@doctordave_wellness", "Instagram", 198000, "paid_plus_product",
         False, "none", "none", True,
         "Doctor recommended for immune function", False, True, 51744.0),
        ("INF-007", "@probioticlover", "TikTok", 28000, "gifted",
         False, "buried in hashtags", "end_of_caption", True,
         "May help support gut health", False, True, 51744.0),
        ("INF-008", "@wellnessmama_official", "Instagram", 412000, "paid",
         True, "Ad: at beginning", "beginning_of_caption", False,
         "Supports immune and digestive health", True, False, 0.0),
        ("INF-009", "@holistichealthguru", "YouTube", 88000, "paid",
         True, "Verbal+on-screen first 30s", "beginning_of_video", False,
         "Clinically inspired probiotic formula supports wellness", True, False, 0.0),
        ("INF-010", "@fitfoodienutritionist", "Instagram", 55000, "gifted_plus_affiliate",
         True, "#ad at beginning", "beginning_of_caption", False,
         "Supports digestive comfort", True, False, 0.0),
    ]
    # 模拟12周数据
    import random
    rng = random.Random(42)
    rows = [fields]
    week_offset = 0
    from datetime import date, timedelta
    start_date = date(2026, 6, 22)

    for week in range(52):
        campaign_date = start_date + timedelta(weeks=week)
        for inf in influencers:
            (inf_id, handle, platform, followers, payment_type,
             disclosed, disc_format, disc_pos, has_issue,
             claim, claim_ok, issue_flag, penalty) = inf
            post_date = campaign_date + timedelta(days=rng.randint(0, 6))
            reach = int(followers * rng.uniform(0.15, 0.45))
            eng = round(rng.uniform(1.8, 8.5), 2)
            clicks = int(reach * eng / 100 * rng.uniform(0.4, 0.8))
            conv = int(clicks * rng.uniform(0.012, 0.045))
            rev = round(conv * rng.uniform(39.99, 44.99), 2)
            disc_display = "YES" if disclosed else "NO"
            rows.append([
                inf_id, handle, platform, followers,
                post_date.isoformat(), f"ProBio+ Q{week // 4 + 1}",
                disc_display, disc_format, disc_pos, reach,
                eng, clicks, conv, rev, claim,
                "YES" if claim_ok else "NO",
                "YES" if issue_flag else "NO",
                penalty if issue_flag else 0.0
            ])

    buf = io.StringIO()
    csv_mod.writer(buf).writerows(rows)
    return buf.getvalue()


def _gen_claim_analysis_csv() -> str:
    """生成详细的声明分析数据 CSV。"""
    import io, csv as csv_mod
    fields = [
        "claim_id", "claim_text", "claim_type", "draft_source",
        "evidence_types_available", "rct_count", "animal_study_count",
        "in_vitro_count", "consumer_survey_count",
        "meets_ftc_standard", "prohibited_qualifier_present",
        "prohibited_qualifier_list", "proof_claim_flag",
        "recommended_action", "ftc_guidance_section",
        "penalty_risk_category", "estimated_penalty_usd"
    ]
    claims = [
        ("CL-001", "Clinically demonstrated to support immune function",
         "health_claim", "press_release_draft_v1.md",
         "3 RCTs (LGG only, not full blend)", 3, 0, 0, 0,
         "PARTIAL", "NO", "", "YES",
         "Remove 'clinically demonstrated'; use 'LGG in ProBio+ has been studied in 3 RCTs'",
         "FTC Health Products Compliance Guidance Dec 2022; Notice of Penalty Offenses (v)",
         "HIGH", 51744.0),
        ("CL-002", "May help support immune function",
         "health_claim", "press_release_draft_v1.md",
         "3 RCTs (LGG)", 3, 0, 0, 0,
         "PARTIAL", "YES", "may", "NO",
         "Remove 'may'; replace with specific evidence-qualified claim",
         "FTC Health Products Compliance Guidance Dec 2022 (prohibited qualifiers)",
         "HIGH", 51744.0),
        ("CL-003", "Based on promising preliminary clinical results",
         "health_claim", "press_release_draft_v1.md",
         "Pilot study (no RCT)", 0, 0, 0, 0,
         "NO", "YES", "promising; preliminary", "NO",
         "Remove entirely; cannot use promising/preliminary to soften inadequate claim",
         "FTC Health Products Compliance Guidance Dec 2022 (prohibited qualifiers)",
         "HIGH", 51744.0),
        ("CL-004", "B-vitamins scientifically proven to support energy metabolism",
         "health_claim", "press_release_draft_v1.md",
         "Established science (multiple human studies)", 15, 0, 0, 0,
         "YES (general mechanism)", "NO", "", "YES",
         "Remove 'scientifically proven'; replace with 'B-vitamins are essential cofactors in energy metabolism'",
         "Notice of Penalty Offenses category (v); FTC Health Products Compliance Guidance",
         "HIGH", 51744.0),
        ("CL-005", "Doctor-formulated for maximum bioavailability",
         "endorsement_claim", "press_release_draft_v1.md",
         "Advisory board physician involvement (undisclosed connection)",
         0, 0, 0, 0,
         "CONDITIONAL", "NO", "", "NO",
         "Disclose physician material connection; ensure adequate substantiation",
         "16 CFR §255.3; FTC Health Products Compliance Guidance (doctor-recommended)",
         "HIGH", 51744.0),
        ("CL-006", "As seen on Dr. Wellness Network (undisclosed $5,000 payment)",
         "endorsement_claim", "press_release_draft_v1.md",
         "N/A - disclosure issue", 0, 0, 0, 0,
         "N/A", "NO", "", "NO",
         "Add 'Ad:' at beginning of all posts; disclose material connection per §255.5",
         "16 CFR §255.5 material connection disclosure",
         "HIGH", 51744.0),
        ("CL-007", "Made in USA (with Danish-sourced Chr. Hansen probiotic strains)",
         "origin_claim", "product_label_draft.md",
         "Manufacturing documentation (85% domestic content, key ingredient foreign)",
         0, 0, 0, 0,
         "NO", "NO", "", "NO",
         "Replace with qualified claim: 'Made in USA from domestic and imported ingredients'",
         "16 CFR Part 323 §323.1 (all or virtually all standard)",
         "HIGH", 2000000.0),
        ("CL-008", "Biodegradable Capsule Shells (HDPE shells)",
         "environmental_claim", "product_label_draft.md",
         "HDPE biodegradation testing (2.3% in 12 months)", 0, 0, 0, 0,
         "NO", "NO", "", "NO",
         "Remove claim; HDPE does not biodegrade within 1 year under disposal conditions",
         "16 CFR §260.8 (one-year biodegradation standard)",
         "HIGH", 51744.0),
        ("CL-009", "Recyclable Packaging (composite incl. foil liner)",
         "environmental_claim", "product_label_draft.md",
         "Recycling facility access data (foil liner <15% access)", 0, 0, 0, 0,
         "NO", "NO", "", "NO",
         "Qualify: 'Bottle and carton recyclable where facilities available'",
         "16 CFR §260.12 (60% substantial majority threshold)",
         "MEDIUM", 51744.0),
        ("CL-010", "Rated 4.9/5 stars by over 2,000 verified customers",
         "review_claim", "press_release_draft_v1.md",
         "Internal review database (collection protocol under review)", 0, 0, 0, 0,
         "CONDITIONAL", "NO", "", "NO",
         "Verify review collection complies with 16 CFR Part 465; no company insider reviews without disclosure",
         "16 CFR §465.2; §465.5 (Consumer Reviews and Testimonials Rule)",
         "MEDIUM", 51744.0),
        ("CL-011", "Supports immune health based on our proprietary blend",
         "health_claim", "press_release_draft_v2.md",
         "3 RCTs (LGG), but claim refers to full 'proprietary blend'",
         3, 0, 0, 0,
         "PARTIAL", "NO", "", "NO",
         "Specify which strains are supported by RCT evidence; cannot claim for full blend without blend-specific RCT",
         "FTC Health Products Compliance Guidance Dec 2022",
         "MEDIUM", 51744.0),
        ("CL-012", "Initial studies show remarkable outcomes for immune health",
         "health_claim", "press_release_draft_v1.md",
         "Pilot study (no control, n=45)", 0, 0, 1, 0,
         "NO", "YES", "initial", "NO",
         "Remove entirely; 'initial' is prohibited qualifier; pilot study insufficient",
         "FTC Health Products Compliance Guidance Dec 2022 (prohibited qualifiers)",
         "HIGH", 51744.0),
        ("CL-013", "ProBio+ helps maintain digestive comfort",
         "health_claim", "drafts/ad_copy_social_media.md",
         "2 RCTs (NCFM strain)", 2, 0, 0, 0,
         "PARTIAL", "YES", "helps", "NO",
         "Remove 'helps' as standalone qualifier; use specific evidence language",
         "FTC Health Products Compliance Guidance Dec 2022 (prohibited qualifiers)",
         "MEDIUM", 51744.0),
        ("CL-014", "Results not typical disclaimer",
         "disclaimer", "press_release_draft_v1.md",
         "N/A - safe harbor status", 0, 0, 0, 0,
         "NO", "NO", "", "NO",
         "Remove entirely; 'results not typical' is NOT a safe harbor per current law (abolished 2009)",
         "16 CFR §255.1 (safe harbor abolished in 2009 revision)",
         "HIGH", 51744.0),
        ("CL-015", "Eco-Friendly Packaging (unqualified)",
         "environmental_claim", "product_label_draft.md",
         "N/A - unqualified general claim", 0, 0, 0, 0,
         "NO", "NO", "", "NO",
         "Must specify which environmental benefit is claimed; unqualified is deceptive per §260.1",
         "16 CFR §260.1 (general environmental benefit claims)",
         "MEDIUM", 51744.0),
    ]
    rows = [fields]
    for c in claims:
        rows.append(list(c))
    buf = io.StringIO()
    csv_mod.writer(buf).writerows(rows)
    return buf.getvalue()


def _gen_regulatory_crosswalk_csv() -> str:
    """生成法规交叉索引 CSV — 各法规条款与违规类型的对应关系。"""
    import io, csv as csv_mod
    fields = [
        "regulation_section", "regulation_title", "effective_date",
        "violation_type", "penalty_per_violation_usd", "penalty_notes",
        "applies_to_health_claims", "applies_to_endorsements",
        "applies_to_reviews", "applies_to_origin_claims",
        "applies_to_environmental_claims", "key_requirement_summary",
        "probio_plus_applicability"
    ]
    rows = [fields]
    entries = [
        ("16 CFR §255.1", "Endorsement Guides — General", "July 26, 2023",
         "False/misleading endorsement", 51744.0, "per violation per 16 CFR Part 465 enforcement",
         True, True, True, False, False,
         "Endorser's statements must be substantiated and reflect genuine views",
         "Dr. Wellness Network endorsement requires disclosure and substantiation"),
        ("16 CFR §255.2", "Consumer Endorsements", "July 26, 2023",
         "Atypical testimonial without disclosure", 51744.0, "per violation",
         True, True, True, False, False,
         "Testimonials must represent typical consumer results or disclose typical results",
         "4.9/5 stars claim; customer testimonial 'cured my IBS'"),
        ("16 CFR §255.3", "Expert Endorsements", "July 26, 2023",
         "Unsubstantiated expert claim; undisclosed material connection", 51744.0, "per violation",
         True, True, False, False, False,
         "Expert must have evaluated the product; material connection must be disclosed",
         "Doctor-formulated and Doctor-recommended claims"),
        ("16 CFR §255.5", "Disclosure of Material Connections", "July 26, 2023",
         "Undisclosed material connection", 51744.0, "per violation",
         False, True, False, False, False,
         "Connection that might materially affect credibility must be clearly and conspicuously disclosed",
         "All influencer partnerships; Dr. Wellness Network ($5k + product)"),
        ("16 CFR §465.2", "Fake or False Consumer Reviews", "October 21, 2024",
         "Fake/misrepresenting review", 51744.0, "per violation",
         False, False, True, False, False,
         "Prohibits writing/selling fake reviews misrepresenting existence or experience",
         "Review collection protocol must be verified; no fake reviews"),
        ("16 CFR §465.4", "Buying Positive Reviews", "October 21, 2024",
         "Compensated reviews without disclosure", 51744.0, "per violation",
         False, False, True, False, False,
         "Prohibits conditioned compensation for positive review content",
         "Influencer review incentive structure must not condition on positive content"),
        ("16 CFR §465.5", "Insider Reviews Without Disclosure", "October 21, 2024",
         "Employee review without disclosure", 51744.0, "per violation",
         False, False, True, False, False,
         "Company insiders must disclose material connection when reviewing company products",
         "In-house nutritionist proposed review must disclose employment"),
        ("16 CFR §465.7", "Review Suppression", "October 21, 2024",
         "Suppression through threats/intimidation", 51744.0, "per violation",
         False, False, True, False, False,
         "Prohibits unfounded legal threats or intimidation to suppress reviews",
         "VitaCore review management policy must explicitly prohibit this"),
        ("16 CFR §260.1", "Green Guides — General Claims", "2012 (current)",
         "Unqualified general environmental benefit claim", 51744.0, "per violation",
         False, False, False, False, True,
         "Unqualified eco-friendly/sustainable claims are likely deceptive",
         "Eco-Friendly Packaging claim on ProBio+ label"),
        ("16 CFR §260.8", "Biodegradable Claims", "2012 (current)",
         "Unqualified biodegradable claim that fails one-year test", 51744.0, "per violation",
         False, False, False, False, True,
         "Must completely break down within one year after customary disposal",
         "Biodegradable Capsule Shells claim — HDPE fails one-year standard"),
        ("16 CFR §260.12", "Recyclable Claims", "2012 (current)",
         "Unqualified recyclable claim below 60% facility access", 51744.0, "per violation",
         False, False, False, False, True,
         "Recyclable requires 60% (substantial majority) consumer access to recycling facilities",
         "Recyclable Packaging claim — foil liner not recyclable in most communities"),
        ("16 CFR §323.1", "Made in USA Labeling Rule — Standard", "August 13, 2021",
         "False all-or-virtually-all Made in USA claim", 2000000.0, "Kubota precedent (January 2024); $2M aggregate",
         False, False, False, True, False,
         "All significant processing and all or virtually all components must be US-origin",
         "Made in USA claim at risk — Danish Chr. Hansen strains are key foreign components"),
        ("FTC Act §5 / Penalty Offenses (i)", "Lacking Evidence for Product Claims", "April 2023 Notice",
         "Product claim without competent reliable evidence", 51744.0, "per violation after Notice of Penalty Offenses",
         True, False, False, False, False,
         "Advertisers must have evidence before making claims; post-hoc rationalization not acceptable",
         "All health claims for ProBio+ must be pre-substantiated"),
        ("FTC Act §5 / Penalty Offenses (v)", "False Proof Claims", "April 2023 Notice",
         "Scientifically/clinically proven without adequate evidence", 51744.0, "per violation",
         True, False, False, False, False,
         "Cannot claim 'clinically proven' or 'scientifically proven' without adequate RCT evidence",
         "Clinically demonstrated claim; scientifically proven B-vitamins claim"),
        ("16 CFR §255.5 / .com Disclosures", "Digital Disclosure Standards", "July 26, 2023",
         "Insufficient disclosure in digital advertising", 51744.0, "per violation",
         False, True, False, False, False,
         "Clear and conspicuous; difficult to miss; understandable by ordinary consumers",
         "Hashtag-buried disclosures and platform-tool-only disclosures are insufficient"),
    ]
    rows.extend(entries)
    buf = io.StringIO()
    csv_mod.writer(buf).writerows(rows)
    return buf.getvalue()


# 增补大型 FTC 执法案例数据库
FTC_ENFORCEMENT_DATABASE = """# FTC Enforcement Actions — Health Products Advertising Database
## Compiled for ComplianceAI Reference | VitaCore Internal Use Only
## Source: FTC press releases, consent orders, and court filings (public records)
## Last Updated: June 2026

---

## Section 1: Health Claim Substantiation Cases (2010–2024)

### Case HCS-001: FTC v. POM Wonderful LLC (2013)

**Background**: POM Wonderful, maker of pomegranate juice and supplements, made claims that
their products could "help prevent or reverse" heart disease, prostate cancer, and erectile
dysfunction, and that they were "clinically proven" to be effective.

**FTC Charges**:
- Deceptive health claims without competent and reliable scientific evidence
- "Clinically proven" claims where evidence did not support that characterization
- Failure to disclose that the clinical evidence was funded entirely by POM Wonderful

**Evidence Review**:
The Commission found that while POM Wonderful had funded approximately $35 million in research,
the studies did not establish that the products could treat, prevent, or reduce risk of disease.
No independent replications of positive findings existed. Several sponsored studies showed
no statistically significant benefit.

**Court Decision**: The D.C. Circuit upheld the FTC's substantiation requirements, holding that
"clinically proven" health claims for products require "well-controlled clinical testing"
(essentially RCTs). The case established that proprietary research funding does not create
adequate substantiation.

**Precedent for ProBio+**: VitaCore's "clinically demonstrated" claim for the full probiotic
blend is analogous to POM's "clinically proven" language. ProBio+ has RCT evidence for LGG
alone, not the full blend. The POM decision confirms this distinction matters.

---

### Case HCS-002: FTC v. Gerber Products Company (2014)

**Background**: Gerber claimed that its Good Start Protect formula would "reduce the risk of
your baby developing allergies" and was the "1st and only infant formula" to reduce allergy risk.

**FTC Charges**:
- Unsubstantiated health/disease prevention claims
- Misleading "first and only" superiority claim

**Resolution**: Consent order prohibiting Gerber from making claims that the product reduces
allergy risk unless supported by at least two adequate and well-controlled human clinical studies
conducted independently of the manufacturer.

**Key Takeaway**: The Commission required TWO independent RCTs for a disease risk reduction claim.
Single-study substantiation was insufficient for disease-related claims.

**Precedent for ProBio+**: Any claim that ProBio+ "reduces" a disease risk would require
multiple independent RCTs. A single positive pilot study (even if one existed) would not suffice.

---

### Case HCS-003: FTC v. Skechers USA (2012)

**Background**: Skechers claimed their Shape-Ups toning shoes would help wearers lose weight,
strengthen muscles, and provide cardiovascular benefits comparable to training.

**FTC Resolution**: $40 million consumer redress settlement

**Evidence Failure**: Skechers had some studies, but they were not well-controlled RCTs.
The Commission found that the available evidence did not support the specific claims made.

**Key Takeaway**: Having "some" evidence is not sufficient if it does not rise to the level
of "competent and reliable scientific evidence." The evidence standard applies to the specific
claims made, not just to vague health associations.

---

### Case HCS-004: FTC v. Reebok International (2011)

**Background**: Reebok's EasyTone and RunTone shoes were claimed to provide 28% more leg curl
muscle activation and 11% more tone than regular walking shoes.

**FTC Resolution**: $25 million consumer redress

**Key Takeaway**: Specific quantified benefit claims ("28% more activation") require the
highest level of substantiation — multiple well-controlled studies showing the specific numbers
claimed. An approximated or optimistic reading of limited data does not suffice.

---

### Case HCS-005: FTC v. Whole Health Products (2010)

**Background**: Weight loss supplement maker claimed products could cause "rapid and dramatic
weight loss," "permanent" results, and were "clinically proven."

**FTC Resolution**: Consent order + $9.8 million civil penalty (largest weight loss penalty at time)

**Evidence**: No competent and reliable scientific evidence whatsoever. Zero RCTs.

**Key Takeaway**: The civil penalty multiplied because the company had previously been warned
by the FTC and had received prior notice of penalty offenses. Repeat offenders face enhanced liability.

---

### Case HCS-006: FTC v. Luminosity (2015)

**Background**: Luminosity brain-training apps claimed to help prevent Alzheimer's disease,
improve cognitive performance in ways that "translate to real world performance," and "delay
and prevent" age-related cognitive decline.

**FTC Resolution**: $2 million civil penalty

**Evidence Failure**: The studies that existed showed improvements on specific cognitive tasks
but could not establish that the improvements "transferred" to real-world function. The claim
that Luminosity prevents Alzheimer's had essentially no credible evidence.

**Key Takeaway**: Even well-documented performance improvements on specific tests do not
automatically substantiate broader transfer claims. Evidence must specifically support the
claim as made.

---

## Section 2: Endorsement and Disclosure Cases (2016–2024)

### Case END-001: FTC v. Lord & Taylor (2016)

**Background**: Lord & Taylor paid 50 fashion influencers to post Instagram photos wearing
a specific dress, without requiring influencers to disclose the commercial relationship.

**FTC Charges**: Failure to require adequate material connection disclosures per §255.5.

**Resolution**: Consent order requiring a comprehensive disclosure compliance program.

**Key Takeaway**: Advertisers are responsible for ensuring their influencer partners disclose
material connections. "We didn't tell them not to disclose" is not a defense — affirmative
disclosure requirements must be built into influencer agreements.

**ProBio+ Application**: VitaCore must affirmatively require all influencers to disclose
material connections in their agreements, with specific language requirements.

---

### Case END-002: FTC v. Warner Bros. Home Entertainment (2016)

**Background**: Warner Bros. paid YouTube influencers (via the Machinima network) to post
positive reviews of the video game "Middle Earth: Shadow of Mordor" without disclosing the
commercial relationship. Disclosures, when present, were buried in video descriptions.

**FTC Charges**: Inadequate disclosure; failure to make disclosures clear and conspicuous.

**Key Takeaway**: Disclosures in YouTube video descriptions are NOT sufficient. The disclosure
must be visible without users having to click "show more" or navigate away from the main
viewing experience.

**ProBio+ Application**: @drwellnessnetwork's YouTube content must include verbal disclosure
in the first 30 seconds AND on-screen text, not just a description note.

---

### Case END-003: FTC v. Devumi LLC (2019)

**Background**: Devumi sold fake Twitter followers, views, comments, and likes to celebrities,
athletes, and businesses. The fake indicators made clients appear more popular than they were.

**FTC Resolution**: Consent order; Devumi's sole owner personally liable for $2.5 million

**Key Takeaway**: This case preceded 16 CFR Part 465 but established the principle later
codified in §465.8. Buying fake social indicators constitutes a deceptive practice.

---

### Case END-004: FTC Influencer Case — Fashion Nova (2022)

**Background**: Fashion Nova suppressed tens of thousands of negative reviews, routing them
away from its website while displaying a curated high-star rating based on positive reviews only.

**FTC Resolution**: $4.2 million settlement

**Key Takeaway**: Systematically suppressing negative reviews while displaying an aggregate
star rating based on a filtered dataset constitutes deceptive review practices. This case
predated §465.7 (effective October 21, 2024) but established the principle.

---

## Section 3: Made in USA Cases (2019–2024)

### Case MIA-001: Nectar Brand LLC (2023)

**Background**: Nectar, a mattress company, claimed its products were "Made in USA" while
mattresses were assembled in China.

**FTC Resolution**: $753,000 civil penalty

**Key Takeaway**: False "Made in USA" claims are specifically actionable under the 2021 Rule.
Even partial domestic assembly is insufficient for an unqualified claim.

---

### Case MIA-002: Kubota North America Corporation (January 2024)

**Background**: Kubota labeled tractors and attachments as "Made in USA" despite manufacturing
processes that included substantial foreign components.

**FTC Resolution**: $2 million civil penalty — LARGEST Made in USA penalty in FTC history.

**Key Takeaway**: Large companies with significant market presence face larger civil penalties.
The $2 million reflects the scale of Kubota's distribution and the number of violating products.

**ProBio+ Direct Application**: This is the most relevant Made in USA precedent. VitaCore's
Danish-sourced Chr. Hansen probiotic strains are key functional components — analogous to
Kubota's situation where essential foreign components precluded an unqualified "Made in USA" claim.

---

### Case MIA-003: Patriot Ordnance Factory (2021)

**Background**: POF-USA made "Made in USA" claims on gun parts while using imported components.

**FTC Resolution**: Consent order requiring modification of Made in USA claims.

**Key Takeaway**: Even companies that pride themselves on American manufacturing must rigorously
verify that ALL significant components meet the "all or virtually all" standard.

---

## Section 4: Consumer Reviews Cases (2020–2024)

### Case CRV-001: 1-800-Flowers.com (2024)

**Background**: Company requested reviews from customers who had made purchases but filtered
review submission to only display those from satisfied customers.

**Resolution**: FTC investigation and enforcement under 16 CFR Part 465 (effective 2024).
The case represented an early enforcement action under the new Consumer Reviews Rule.

**Key Takeaway**: Mechanically filtering which consumers can even submit reviews — routing
dissatisfied customers away from the review platform — constitutes deceptive review practices.

---

### Case CRV-002: Medical Spa Review Suppression (2024)

**Background**: A medical spa chain sent threatening letters to patients who left negative
reviews, claiming the reviews violated HIPAA confidentiality and threatening legal action.

**Resolution**: $1.2 million civil penalty under §465.7 (Review Suppression)

**Key Takeaway**: This was the first §465.7 enforcement action after the rule's effective date
(October 21, 2024). The FTC acted quickly to establish a precedent. Unfounded legal threats
to suppress reviews are specifically and heavily penalized.

**ProBio+ Application**: VitaCore's review management policy must explicitly prohibit using
legal threats or intimidation to suppress negative reviews. Any cease-and-desist to reviewers
must have a legitimate, good-faith legal basis.

---

## Section 5: Penalty Calculation Methodology

### Civil Penalty Framework

The $51,744 per violation rate (2024) applies to:
- Violations of 16 CFR Part 465 (Consumer Reviews Rule)
- Violations constituting deceptive acts under Section 5 after Notice of Penalty Offenses

**Multiplier Factors**: The FTC considers the following in penalty calculation:
1. Number of consumers exposed to the violation
2. Duration of the violating conduct
3. Whether the company had prior notice (including receipt of Notice of Penalty Offenses letter)
4. Company size and ability to pay
5. Degree of culpability (negligent vs. deliberate)

**ProBio+ Penalty Exposure Matrix** (illustrative, for legal analysis):

| Claim | Estimated Violations (8-week campaign) | Per-Violation Rate | Estimated Exposure |
|-------|---------------------------------------|-------------------|-------------------|
| 'Clinically demonstrated' (national campaign) | ~15,000 (across all channels) | $51,744 | $776,160,000 (theoretical max) |
| Undisclosed influencer posts (10 influencers x 12 posts) | 120 | $51,744 | $6,208,880 |
| 'Biodegradable' packaging claim (per unit sold) | Variable | $51,744 | Variable |
| 'Made in USA' (per unit sold, per Kubota precedent) | Variable | $2M aggregate (precedent) | Variable |

NOTE: The "theoretical max" for broad campaign violations is a legal construct; the FTC
typically seeks a consent order and reasonable penalties, not the mathematical maximum.
However, the first column illustrates why broad national advertising violations are so serious.

---

## Summary: Top Risk Areas for ProBio+ Daily

Based on the enforcement database review, the following claims carry enforcement risk
levels that warrant immediate action before launch:

| Risk Level | Claim/Practice | Applicable Rule | Estimated Exposure |
|-----------|---------------|----------------|-------------------|
| CRITICAL | 'Clinically demonstrated' for full blend | FTC Penalty Offenses (v) | Multi-million |
| CRITICAL | Made in USA with foreign key components | 16 CFR Part 323 | Up to $2M+ |
| HIGH | Undisclosed influencer partnerships | 16 CFR §255.5; §465.4 | $51,744 per post |
| HIGH | 'Results not typical' disclaimer reliance | 16 CFR §255.1 | $51,744 per violation |
| HIGH | 'Biodegradable' HDPE capsule shells | 16 CFR §260.8 | $51,744 per unit |
| MEDIUM | 'Doctor-formulated' without disclosure | 16 CFR §255.3 | $51,744 per violation |
| MEDIUM | Employee reviews without disclosure | 16 CFR §465.5 | $51,744 per review |
| MEDIUM | Hashtag-buried disclosure format | 16 CFR §255.5 | $51,744 per post |
"""


SLACK_LEGAL_CHANNEL_JSON_CONTENT = """# Slack #legal-review Channel — Complete Message Archive
## Export generated: June 2, 2026
## Channel: #legal-review | Workspace: VitaCore Inc.
## Participants: Dr. Maria Santos (CCO), Sarah Chen (Counsel), Mike Torres (VP Marketing)

---

## Thread 1: Press Release v1 Review (May 26, 2026)

**sarah_chen [10:00 AM May 26]**: I've reviewed press_release_draft_v1.md. Summary of major issues:

Issue 1 — "Clinically demonstrated to support immune function"
This is a PROOF CLAIM that triggers the Notice of Penalty Offenses category (v). We have RCT data
for LGG specifically (3 trials), but NOT for the full ProBio+ blend. A product-level "clinically
demonstrated" claim requires a product-specific RCT. The POM Wonderful case (2013) confirms this.
The language must come out.

Issue 2 — "May help support immune function"
"May" is EXPLICITLY listed in FTC Health Products Compliance Guidance (December 2022) as an
insufficient qualifier for emerging science claims. It does not provide legal protection;
it creates false consumer impressions. Must go.

Issue 3 — "Promising preliminary clinical results" / "initial studies"
BOTH "promising" AND "preliminary" are prohibited qualifiers per the same guidance.
AND "initial" is also on the list. Triple flag on this one sentence.

Issue 4 — Penalty risk
Per 16 CFR Part 465 (effective October 21, 2024) and Notice of Penalty Offenses:
$51,744 per violation in 2024. NOT $45,000 as the bot summary claims — always check
the primary source (regulatory/).

---

**mike_torres [10:30 AM May 26]**: Sarah, I think you're being overly conservative. A few points:

1. The bot summary says $45,000 per violation. We should use that for our risk model.
2. "May help support" is just standard hedging language in our industry. The 2009 Guides
   said you can add disclaimers like "results not typical" and that gives you coverage.
3. I checked with a friend at another supplement company and they use "may help" all the time.
4. The "clinically demonstrated" language is good marketing. Consumers expect it.

Can we just add "results not typical" and "these statements have not been evaluated by FDA"
and move forward?

---

**sarah_chen [10:45 AM May 26]**: Mike — I need to be direct:

RE: $45,000 penalty figure — The $45,000 figure is from the auto-generated DECOY summary
which explicitly states it is NOT authoritative. The ACTUAL figure per 16 CFR Part 465
(2024 adjusted rate) is $51,744 per violation. I confirmed this against the regulatory text.
We cannot build our legal risk model on an explicitly-flagged non-authoritative estimate.

RE: "Results not typical" safe harbor — This safe harbor DOES NOT EXIST in current law.
It was in the 1980 Endorsement Guides. It was ABOLISHED in the 2009 revision.
The 2023 Endorsement Guides (effective July 26, 2023) confirm its abolition.
What your friend's company is doing is not compliant — they may simply not have been
enforced against yet. Using a non-existent safe harbor is a compliance risk, not protection.

RE: "May help support" — Industry practice does not equal legal compliance. The FTC
specifically identified this as an insufficient qualifier precisely BECAUSE it is widely
misused. Its prevalence in the industry is the reason it's in the guidance.

RE: "Clinically demonstrated" — Our substantiation evidence is for LGG in isolation,
not the ProBio+ blend. The POM Wonderful case (FTC v. POM Wonderful LLC, 2013) directly
addresses this: ingredient-level evidence does not automatically substantiate product-level
"clinically proven" claims. We'd be repeating POM's mistake with forewarning.

---

**dr_maria_santos_CCO [11:15 AM May 26]**: Sarah's analysis is correct. For the compliance
record:

1. Per-violation penalty: $51,744 (2024 rate, 16 CFR Part 465) — not $45,000
2. "Results not typical" safe harbor: ABOLISHED since 2009 — does not exist in current law
3. FTC-prohibited qualifiers including "may," "helps," "promising," "preliminary," "initial,"
   and "pilot" cannot rescue inadequately substantiated health claims
4. Mike's reliance on the bot summary and on the 2009 Guides is incorrect

I am directing the compliance review to proceed with Sarah Chen's analysis as the authoritative
legal position. All final claims will require both Sarah's clearance and my sign-off.

---

## Thread 2: Influencer Disclosure Protocols (May 27, 2026)

**sarah_chen [9:00 AM May 27]**: Per the Discord conversation Kevin forwarded, a few corrections:

1. Platform "Paid Partnership" / "Branded Content" tags are INSUFFICIENT as the sole disclosure
   method per FTC .com Disclosures (2013) and the updated Endorsement Guides (2023).
   Both @drwellnessnetwork and @healthcoach_jay must use "#ad" or "Ad:" at the BEGINNING
   of their post captions. Not buried at the end of hashtag chains.

2. @drwellnessnetwork received $5,000 payment plus 6 months free product — this is a textbook
   material connection per §255.5: "a connection between the endorser and the seller of the
   advertised product that might materially affect the weight or credibility of the endorsement."
   Zero disclosure in their current draft = clear §255.5 violation.

3. @healthcoach_jay's "#giftedpartnership" buried in hashtags at the end of the caption
   is insufficient. Per the FTC's guidance, disclosures must appear "before the consumer
   clicks 'more'" and be "difficult to miss."

---

**mike_torres [9:30 AM May 27]**: Fine on the disclosure point, but I still think we can use
"Doctor Recommended" for the @drwellnessnetwork posts since he has "Doctor" in his handle.
And "Doctor-formulated" on the label should be okay as long as our advisory board reviewed it.

---

**sarah_chen [9:45 AM May 27]**: Two separate issues, Mike:

1. @drwellnessnetwork endorsement: The "Doctor" in his handle is an influencer brand name,
   not necessarily an indication of a licensed medical professional. To use "Doctor Recommended,"
   we would need: (a) verification that he is a licensed physician with relevant expertise,
   (b) evidence that he actually evaluated ProBio+ and formed the stated opinion, (c) disclosure
   of his material connection. None of these are currently documented.

2. "Doctor-formulated" label claim: Under 16 CFR §255.3 and FTC Health Products Compliance
   Guidance, "Doctor-formulated" implies expert endorsement. Requirements: (a) the physician
   must actually have conducted meaningful formulation oversight (not just reviewed a marketing deck),
   (b) the claim must be substantiated for the implied health benefit, (c) material connection
   must be disclosed. Currently, the advisory board physician's connection and role are not
   publicly documented. This is a conditional claim that requires documentation.

---

## Thread 3: Update After CEO Feishu Message (June 1, 2026)

**sarah_chen [10:00 AM Jun 1]**: FYI — CEO James Park sent a Feishu message last week saying
"results not typical" plus "supports immune health based on our proprietary blend" would be
fine based on advice from a non-VitaCore lawyer. For the compliance record:

CEO Park's informal position is noted but is NOT determinative for FTC compliance.
Informal guidance from a non-expert contact does not override:
(1) FTC statute and regulations
(2) CCO Dr. Santos' formal compliance authority
(3) Our external legal counsel Compliance Counsel LLC's formal opinion

The "results not typical" safe harbor is abolished regardless of what any informal source says.
The "supports immune health based on our proprietary blend" language still requires competent
and reliable scientific evidence for the specific claimed benefit — the "based on our proprietary
blend" phrasing does not create a new substantiation standard.

---

**dr_maria_santos_CCO [10:15 AM Jun 1]**: Recorded in the compliance log. Proceed with
the formal compliance analysis. Update me when we have CEO Park's formal Feishu sign-off
on withdrawing the original draft language (I understand this is coming this week).

---

## Thread 4: 16 CFR Part 465 Questions (May 28, 2026)

**mike_torres [2:00 PM May 28]**: When does the Consumer Reviews Rule actually apply?
Is it retroactive? Kevin mentioned we have some old influencer reviews from before October 2024.

**sarah_chen [2:15 PM May 28]**: The Consumer Reviews and Testimonials Rule (16 CFR Part 465)
was effective October 21, 2024. It is NOT retroactive — it applies to conduct occurring on or
after that date. Historical reviews (pre-October 21, 2024) are not directly covered.

HOWEVER: The rule's prohibitions largely codified pre-existing Section 5 enforcement standards.
Pre-October 2024 conduct that would violate Part 465 would likely also have violated Section 5.
The practical difference: post-October 2024 violations are subject to specific civil penalty
amounts ($51,744 per violation) without requiring the FTC to first go through a lengthy
deceptive practice proceeding.

For ProBio+ launch (June 2026): ALL new content is fully subject to Part 465.
All influencer agreements and review protocols must comply.

---
END OF EXPORTED SLACK CHANNEL LOG
"""


def _gen_ads_review_log_csv() -> str:
    """生成广告审核日志 CSV — 大体量确定性合成（~25k tokens）。"""
    import io, csv as csv_mod, random
    from datetime import date, timedelta
    rng = random.Random(2026)
    _ = timedelta  # noqa
    fields = [
        "review_id", "review_date", "reviewer", "document_reviewed",
        "claim_id", "claim_text_excerpt", "claim_type",
        "regulatory_section", "ftc_citation", "violation_detected",
        "violation_category", "severity", "evidence_tier",
        "rct_count", "animal_studies", "in_vitro_studies",
        "prohibited_qualifier", "proof_claim", "disclosure_issue",
        "recommended_action", "action_taken", "status",
        "estimated_penalty_usd", "review_notes"
    ]
    reviewers = ["Dr. Maria Santos (CCO)", "Sarah Chen (Counsel)", "Compliance Counsel LLC", "Dr. Rachel Kim (Science)"]
    documents = [
        "press_release_draft_v1.md", "ad_copy_social_media.md",
        "product_label_draft.md", "press_release_draft_v2.md",
        "brand_guidelines.md"
    ]
    claims_pool = [
        ("CL-001", "Clinically demonstrated to support immune function",
         "health_claim", "§255.1", True, "proof_claim", "high", "RCT (LGG only)", 3, 0, 0, False, True, False,
         "Remove or qualify with strain-specific language"),
        ("CL-002", "May help support immune function", "health_claim", "§255.1",
         True, "prohibited_qualifier", "high", "Partial RCT", 3, 0, 0, True, False, False,
         "Remove 'may'; rewrite with evidence-based language"),
        ("CL-003", "Promising preliminary clinical results", "health_claim", "§255.1",
         True, "prohibited_qualifier", "high", "None (pilot only)", 0, 0, 0, True, False, False,
         "Remove entirely"),
        ("CL-004", "B-vitamins scientifically proven to support energy", "health_claim", "§255.1",
         True, "proof_claim", "high", "Established science", 10, 0, 0, False, True, False,
         "Remove 'scientifically proven'; use 'well-established role'"),
        ("CL-005", "Doctor-formulated for maximum results", "endorsement_claim", "§255.3",
         True, "undisclosed_material_connection", "high", "N/A", 0, 0, 0, False, False, True,
         "Disclose physician connection; verify involvement"),
        ("CL-006", "As seen on Dr. Wellness Network (undisclosed)", "endorsement_claim", "§255.5",
         True, "undisclosed_material_connection", "high", "N/A", 0, 0, 0, False, False, True,
         "Add Ad: disclosure at beginning of all posts"),
        ("CL-007", "Made in USA (Danish probiotic strains)", "origin_claim", "§323.1",
         True, "false_origin_claim", "high", "N/A", 0, 0, 0, False, False, False,
         "Replace with qualified Made in USA claim"),
        ("CL-008", "Biodegradable Capsule Shells (HDPE)", "environmental_claim", "§260.8",
         True, "unsubstantiated_env_claim", "high", "Testing data", 0, 0, 0, False, False, False,
         "Remove; HDPE fails one-year standard"),
        ("CL-009", "Recyclable Packaging", "environmental_claim", "§260.12",
         True, "unsubstantiated_env_claim", "medium", "Facility access data", 0, 0, 0, False, False, False,
         "Qualify to specific recyclable components"),
        ("CL-010", "Results not typical disclaimer", "disclaimer", "§255.1",
         True, "invalid_safe_harbor", "high", "N/A", 0, 0, 0, False, False, False,
         "Remove; safe harbor abolished 2009"),
        ("CL-011", "Eco-Friendly Packaging", "environmental_claim", "§260.1",
         True, "unqualified_general_claim", "medium", "N/A", 0, 0, 0, False, False, False,
         "Qualify with specific environmental benefit"),
        ("CL-012", "Initial studies show remarkable outcomes", "health_claim", "§255.1",
         True, "prohibited_qualifier", "high", "Pilot (n=45)", 0, 0, 0, True, False, False,
         "Remove; pilot study insufficient, 'initial' prohibited qualifier"),
    ]
    rows = [fields]
    start = date(2026, 5, 20)
    actions = ["Flagged for revision", "Under review", "Pending legal sign-off", "Referred to CCO", "Resolved"]
    statuses = ["OPEN", "IN_REVIEW", "RESOLVED", "ESCALATED"]
    for review_idx in range(600):
        rd = start + timedelta(days=rng.randint(0, 20))
        reviewer = rng.choice(reviewers)
        doc = rng.choice(documents)
        cl = rng.choice(claims_pool)
        (cl_id, cl_text, cl_type, reg_sec, viol, viol_cat, sev, ev_tier,
         rct, animal, vitro, pq, pc, di, rec) = cl
        ftc_cit = f"16 CFR {reg_sec}"
        est_pen = 51744.0 if viol else 0.0
        if cl_id == "CL-007":
            est_pen = 2000000.0
        action = rng.choice(actions)
        status = rng.choice(statuses)
        notes = f"Review #{review_idx+1}: {viol_cat} flagged in {doc} by {reviewer.split('(')[0].strip()}"
        rows.append([
            f"RV-{review_idx+1:04d}", rd.isoformat(), reviewer, doc,
            cl_id, cl_text[:60], cl_type, reg_sec, ftc_cit,
            "YES" if viol else "NO", viol_cat if viol else "", sev,
            ev_tier, rct, animal, vitro,
            "YES" if pq else "NO", "YES" if pc else "NO", "YES" if di else "NO",
            rec, action, status, est_pen, notes
        ])
    buf = io.StringIO()
    csv_mod.writer(buf).writerows(rows)
    return buf.getvalue()


def _gen_influencer_agreement_data_csv() -> str:
    """生成影响者协议数据 CSV。"""
    import io, csv as csv_mod, random
    from datetime import date, timedelta
    rng = random.Random(777)
    fields = [
        "agreement_id", "influencer_handle", "platform", "follower_count",
        "compensation_type", "compensation_amount_usd", "free_product_value_usd",
        "affiliate_commission_pct", "material_connection_type",
        "disclosure_required", "disclosure_format_specified",
        "disclosure_format_detail", "compliant_disclosure_language",
        "platform_paid_partnership_tool", "additional_explicit_disclosure",
        "ftc_compliant", "ftc_section", "compliance_issue",
        "agreement_date", "campaign_start", "campaign_end",
        "content_type", "health_claims_allowed", "prohibited_terms_list",
        "review_approved_by", "status"
    ]
    influencers_data = [
        ("@drwellnessnetwork", "Instagram", 285000, "monetary", 5000, 1800, 0, "paid_plus_product",
         True, False, "none", "none", True, False, False, "§255.5",
         "No disclosure specified in agreement; undisclosed paid endorsement",
         "2026-05-15", "2026-06-22", "2026-08-22", "static_posts",
         True, "clinically demonstrated,scientifically proven,cures,treats",
         "PENDING", "NON_COMPLIANT"),
        ("@healthcoach_jay", "TikTok", 42000, "gifted", 0, 250, 8, "gifted_plus_affiliate",
         True, True, "#giftedpartnership hashtag at end of caption", "insufficient",
         True, False, False, "§255.5",
         "Hashtag-only disclosure at end of caption; platform tool alone insufficient",
         "2026-05-20", "2026-06-22", "2026-08-22", "video_reels",
         False, "clinically demonstrated,may help,promising,preliminary",
         "Sarah Chen", "NON_COMPLIANT"),
        ("@nutritionbyjessica", "Instagram", 67500, "monetary", 2000, 500, 0, "paid",
         True, True, "Ad: at very beginning of each caption", "Ad: [content]...",
         False, True, True, "§255.5",
         "Compliant — explicit Ad: disclosure at beginning",
         "2026-05-22", "2026-06-22", "2026-08-22", "static_posts",
         False, "clinically demonstrated,scientifically proven",
         "Sarah Chen", "COMPLIANT"),
        ("@fitnesswithmark", "YouTube", 125000, "monetary", 3500, 0, 5, "paid_plus_affiliate",
         True, True, "Verbal disclosure first 30s + on-screen text", "verbal+visual",
         False, True, True, "§255.5",
         "Compliant — verbal and visual disclosure at video beginning",
         "2026-05-22", "2026-06-22", "2026-08-22", "long_form_video",
         False, "clinically demonstrated,doctor recommended,results not typical",
         "Sarah Chen", "COMPLIANT"),
        ("@momlifewellness", "Instagram", 38000, "gifted", 0, 250, 0, "gifted",
         True, True, "#ad at beginning of caption", "#ad [content]...",
         False, True, True, "§255.5",
         "Compliant — #ad at beginning",
         "2026-05-25", "2026-06-22", "2026-08-22", "static_posts",
         False, "clinically demonstrated,proven,initial studies",
         "Dr. Maria Santos", "COMPLIANT"),
        ("@doctordave_wellness", "Instagram", 198000, "monetary", 4500, 1200, 0, "paid_plus_product",
         True, False, "none", "none", True, False, False, "§255.5",
         "No disclosure; doctor handle implies medical expertise without verification",
         "2026-05-18", "2026-06-22", "2026-08-22", "static_posts",
         True, "clinically demonstrated,doctor recommended,scientifically proven",
         "PENDING", "NON_COMPLIANT"),
        ("@probioticlover", "TikTok", 28000, "gifted", 0, 150, 0, "gifted",
         True, True, "#sponsored at end of hashtags", "insufficient",
         True, False, False, "§255.5",
         "Disclosure at end of hashtags; insufficient per FTC guidance",
         "2026-05-28", "2026-06-22", "2026-08-22", "video_reels",
         False, "may help,promising,preliminary",
         "PENDING", "NON_COMPLIANT"),
        ("@wellnessmama_official", "Instagram", 412000, "monetary", 6500, 0, 3, "paid_plus_affiliate",
         True, True, "Ad: at beginning + verbal in Stories", "multi-format",
         False, True, True, "§255.5",
         "Compliant — multi-format explicit disclosure",
         "2026-05-22", "2026-06-22", "2026-09-22", "static_plus_stories",
         False, "clinically demonstrated,proven,may help",
         "Sarah Chen", "COMPLIANT"),
    ]
    rows = [fields]
    for inf in influencers_data:
        (handle, platform, followers, comp_type, comp_amt, prod_val, aff_pct, mc_type,
         disc_req, disc_spec, disc_fmt, disc_lang, platform_tool, add_disc, compliant,
         ftc_sec, issue, agr_date, camp_start, camp_end, content_type,
         health_claims, prohibited, approver, status) = inf
        rows.append([
            f"AGR-{len(rows):03d}", handle, platform, followers,
            comp_type, comp_amt, prod_val, aff_pct, mc_type,
            "YES" if disc_req else "NO",
            "YES" if disc_spec else "NO",
            disc_fmt, disc_lang,
            "YES" if platform_tool else "NO",
            "YES" if add_disc else "NO",
            "YES" if compliant else "NO", ftc_sec, issue,
            agr_date, camp_start, camp_end, content_type,
            "YES" if health_claims else "NO", prohibited,
            approver, status
        ])
    buf = io.StringIO()
    csv_mod.writer(buf).writerows(rows)
    return buf.getvalue()


def gen_supplemental_files() -> None:
    """生成大体量补充数据文件以满足 100k token 体量要求。"""
    w(WS / "sessions" / "slack_legal_channel.md", SLACK_LEGAL_CHANNEL_JSON_CONTENT)
    w(WS / "research" / "ftc_enforcement_case_database.md", FTC_ENFORCEMENT_DATABASE)
    w(WS / "research" / "claim_analysis_matrix.csv", _gen_claim_analysis_csv())
    w(WS / "research" / "regulatory_crosswalk.csv", _gen_regulatory_crosswalk_csv())
    w(WS / "research" / "influencer_performance_data.csv", _gen_influencer_csv())
    w(WS / "reports" / "ads_review_log.csv", _gen_ads_review_log_csv())
    w(WS / "reports" / "influencer_agreement_log.csv", _gen_influencer_agreement_data_csv())


# --------------------------------------------------------------------------- #
# 7. sessions（主 + 4 history）
# --------------------------------------------------------------------------- #
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("legal_review_slack", TID)
    s_feishu = gen_session_id("cco_ceo_feishu", TID)
    s_email = gen_session_id("external_audit_email", TID)
    s_discord = gen_session_id("marketing_discord", TID)

    # 主 session（含 P1/P2/P5 显式 preference + CCO briefing）
    sb = SessionBuilder(main_id, CWD, "2026-05-28T09:00:00", is_main=True)
    sb.add_user(
        "You are ComplianceAI, the FTC advertising compliance assistant for Dr. Maria Santos, "
        "Chief Compliance Officer at VitaCore Inc. Your task is to complete the pre-launch "
        "compliance review of ProBio+ Daily before the US market launch on June 15, 2026.\n\n"
        "Regulatory documents are in `regulatory/`. Product materials are in `drafts/` and "
        "`company/`. Clinical evidence is in `research/`. History sessions are available via "
        "`sessions_list` (Slack, Feishu, Email, Discord).\n\n"
        "**Workspace Preferences (apply throughout, even when not restated):**\n"
        "- P1: Every JSON output file must carry a top-level field `schema_version` set to "
        "\"1.0\" — the compliance registry rejects untagged files.\n"
        "- P2: Every compliance issue entry must carry an `ftc_citation` field with format "
        "exactly \"16 CFR §XXX.X\" (§ symbol, section number).\n"
        "- P5: All files under `final/` must follow the naming pattern "
        "`{document_type}_final_YYYYMMDD.{ext}`. For this review (date: 20260603), use "
        "`press_release_final_20260603.md` and `signoff_final_20260603.txt`.\n\n"
        "Auto-generated summaries (e.g. `reports/external_audit_summary_DECOY.md`) are "
        "NOT authoritative — always verify numbers against primary regulatory documents.\n\n"
        "History sessions available (Slack #legal-review / Feishu DM / Email / Discord #marketing). "
        "Begin by running `exec ls -R` and reading SOUL.md, then await each task.")
    sb.add_assistant(
        "Understood. I have read AGENTS.md and SOUL.md. Working framework:\n"
        "1. Treat regulatory/ documents as authoritative; never rely on the DECOY summary for numbers.\n"
        "2. Every JSON file carries schema_version \"1.0\" (P1); every issue entry has ftc_citation "
        "in \"16 CFR §XXX.X\" format (P2).\n"
        "3. All final/ files named {document_type}_final_20260603.{ext} (P5).\n"
        "4. Civil penalty per violation: $51,744 (2024 rate per 16 CFR Part 465).\n"
        "Ready for the compliance review tasks.")
    sb.write(SESS / f"{main_id}.jsonl")

    # S2 Slack #legal-review — Sarah Chen vs Mike Torres 冲突（V1）+ bot summary 诱饵（V5）
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2026-05-26T10:00:00",
        [
            ("[Slack #legal-review sarah Mon May 26 10:00 EDT 2026] I've reviewed the press "
             "release draft v1. Multiple issues. The 'clinically demonstrated' claim for the full "
             "probiotic blend is the biggest red flag — we only have RCT data for LGG specifically, "
             "not the entire blend. Also, 'may help support' is explicitly listed as a prohibited "
             "qualifier in FTC Health Products Compliance Guidance. The penalty exposure is real: "
             "$51,744 per violation under 16 CFR Part 465 (2024 rate). We need to strip all the "
             "prohibited language before launch.",
             "Noted Sarah's analysis: 'clinically demonstrated' for full blend requires product-specific "
             "RCT; 'may help support' is a prohibited qualifier per FTC guidance. Penalty: $51,744 "
             "per violation. I will flag these in the compliance issues report."),
            ("[Slack #legal-review mike Mon May 26 10:30 EDT 2026] I disagree with Sarah's reading. "
             "The auto-bot summary says the estimated penalty is $45,000 per violation. And I think "
             "'may help support' is fine — it's just hedging language. The 2009 Endorsement Guides "
             "also allowed 'results not typical' disclaimers. Mike is comfortable with more aggressive "
             "claim language as long as we add disclaimers.",
             "I must flag important errors in Mike's analysis: (1) The $45,000 figure comes from the "
             "bot-summary DECOY file which is explicitly non-authoritative. The actual 2024 rate is "
             "$51,744 per violation per 16 CFR Part 465. (2) 'May help support' is listed as a "
             "PROHIBITED qualifier in FTC Health Products Compliance Guidance — it cannot rescue "
             "an inadequately substantiated claim. (3) The 2009 'results not typical' safe harbor "
             "was ABOLISHED — it does not exist in current law (2023 Guides, §255.1). "
             "Sarah Chen's analysis is correct; Mike Torres' relies on the outdated and "
             "non-authoritative bot summary."),
            ("[Slack #legal-review sarah Mon May 26 11:00 EDT 2026] Also note: 16 CFR Part 465 "
             "(Consumer Reviews Rule) is now effective as of October 21, 2024. The review collection "
             "protocol for ProBio+ must comply with it. The 'results not typical' safe harbor was "
             "abolished in the 2009 guides and the 2023 revision confirmed this — Mike is relying "
             "on a version that no longer exists.",
             "Confirmed: 16 CFR Part 465 effective October 21, 2024. 'Results not typical' safe "
             "harbor abolished since 2009. Mike Torres' position is based on outdated information."),
        ])

    # S3 Feishu DM — CCO ↔ CEO private（P3/P4 preference feedback; CEO 初始建议）
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2026-05-27T14:00:00",
        [
            ("[Feishu CCO-Maria Wed May 27 14:00 EDT 2026] After Q4 is done, I want feedback on "
             "all Markdown report formats. Going forward, H1 should be the document title/filename, "
             "H2 the claim category, H3 the specific provision being analyzed. This makes the reports "
             "easier to scan in the legal review meetings.",
             "Noted P3 heading structure: H1=document title, H2=claim category, H3=specific provision. "
             "I will apply this structure to all Markdown compliance reports from Q9 onward."),
            ("[Feishu CCO-Maria Wed May 27 14:10 EDT 2026] Also for the prohibited terms replacement "
             "tables (Q4 output), add a 'severity' column with values high/medium/low corresponding "
             "to FTC enforcement priority. High for proof claims and prohibited qualifiers, medium "
             "for disclosure issues, low for formatting/best practice issues.",
             "Noted P4 severity column requirement for prohibited terms tables. Will add "
             "severity: high/medium/low based on FTC enforcement priority in Q4 and Q13 outputs."),
            ("[Feishu CEO-James Wed May 27 16:00 EDT 2026] Maria, I had a call with a lawyer "
             "friend (not our legal counsel) who says 'supports immune health based on our "
             "proprietary blend' should be fine. He also said the 'results not typical' disclaimer "
             "is still valid under the old FTC guidelines. I'm comfortable proceeding with the "
             "original draft if we just add that disclaimer.",
             "I have noted CEO James Park's informal input: (1) 'supports immune health based on "
             "our proprietary blend' — needs formal legal analysis; the substantiation question "
             "turns on whether 'proprietary blend' language excuses the need for a product-specific "
             "RCT (it does not, per FTC guidance). (2) 'Results not typical' safe harbor — this "
             "safe harbor was ABOLISHED in 2009 and does not exist under the 2023 Guides. The CEO's "
             "lawyer friend is relying on pre-2009 Guides. This informal input is NOT determinative "
             "of FTC compliance requirements; formal legal analysis from Sarah Chen's team governs."),
        ])

    # S4 Email — Compliance Counsel LLC（含 2009 旧版引用 V6 红鲱鱼）
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2026-05-28T08:00:00",
        [
            ("[Email ComplianceCounselLLC → Dr.Santos Thu May 28 08:00 EDT 2026] "
             "Subject: Formal Compliance Opinion — ProBio+ Daily Launch Review\n\n"
             "Dear Dr. Santos,\n\n"
             "We have completed our initial review of the ProBio+ Daily launch materials. "
             "Summary of findings:\n\n"
             "1. 'Clinically demonstrated to support immune function' — PROHIBITED. "
             "Requires at least one well-controlled RCT for the specific product blend. "
             "The existing LGG-only RCTs do not support a product-level 'clinically demonstrated' claim.\n\n"
             "2. 'May help support immune function' — WARNING. While softening language, "
             "'may' is specifically identified in FTC Health Products Compliance Guidance "
             "as an insufficient qualifier for emerging science claims.\n\n"
             "3. 'Doctor-formulated' claim — CONDITIONALLY PERMITTED. This claim is "
             "conditionally permissible provided: (a) the physician actually participated "
             "in formulation; (b) there is adequate substantiation for the claimed benefits; "
             "(c) any material connection is disclosed per §255.5.\n\n"
             "4. 'Results not typical' disclaimer [OUTDATED GUIDANCE REFERENCE BELOW] — "
             "Under Section 255.1(b) of the 2009 Endorsement Guides, the 'results not typical' "
             "disclaimer provides safe harbor for atypical testimonials. [NOTE: This reference "
             "to the 2009 Guides is included in error — see our corrected opinion letter v2 "
             "for the current standard.]\n\n"
             "5. 'Made in USA' — HIGH RISK. The Danish-sourced Chr. Hansen probiotic strains "
             "are key functional components. The 'all or virtually all' standard is unlikely "
             "to be satisfied. We recommend a qualified claim.\n\n"
             "Regards,\nCompliance Counsel LLC",
             "Received Compliance Counsel LLC initial opinion. Key observations: Points 1, 2, 3, "
             "and 5 align with current FTC guidance. IMPORTANT FLAG: Point 4 cites the 2009 "
             "Endorsement Guides' 'results not typical' safe harbor — this guidance is OUTDATED. "
             "The safe harbor was abolished in 2009 and does not exist under the current 2023 "
             "Endorsement Guides (§255.1). The external auditors note themselves this is an error "
             "('see our corrected opinion letter v2'). This recommendation must be placed in "
             "'superseded_recommendations' pending the v2 corrected letter."),
        ])

    # S5 Discord #marketing — Kevin Liu 影响者脚本讨论（CEO 旧草稿批注）
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, CWD, "2026-05-27T09:00:00",
        [
            ("[Discord #marketing kevin Tue May 27 09:00 EDT 2026] We're working on the influencer "
             "campaign for ProBio+ launch. I have agreements with @drwellnessnetwork (paid, $5k + "
             "6mo free product) and @healthcoach_jay (gifted product, affiliate link). They'll post "
             "on Instagram and TikTok. I'm planning to have them mark posts as 'Paid Partnership' "
             "using the platform tools. That should cover our disclosure obligations, right?",
             "I need to flag a compliance issue with Kevin's disclosure plan: Using only the "
             "platform's 'Paid Partnership' feature is INSUFFICIENT per FTC guidance (.com "
             "Disclosures 2013 and 16 CFR §255.5). Both influencers must include '#ad' or 'Ad:' "
             "explicitly at the BEGINNING of their post captions. The platform tool alone does not "
             "satisfy FTC requirements. Both influencers have material connections (payment + free "
             "product for @drwellnessnetwork; gifted product + commission for @healthcoach_jay) "
             "that must be clearly and conspicuously disclosed per §255.5."),
            ("[Discord #marketing CEO-James annotating old draft Tue May 27 09:30 EDT 2026] "
             "[CEO annotation on draft ad copy v0.1] 'Love the clinically demonstrated language — "
             "keep it, and add results not typical disclaimer to cover us. The 2009 FTC rules allow "
             "this.' — James Park",
             "I must flag that CEO Park's annotation references the 2009 FTC Endorsement Guides. "
             "This is an outdated source: (1) The 'results not typical' safe harbor was ABOLISHED "
             "in the 2009 revision itself — the 2009 Guides removed this safe harbor that existed "
             "in the 1980 version. (2) The current governing rules are the 2023 Endorsement Guides "
             "(effective July 26, 2023) and 16 CFR Part 465 (effective October 21, 2024). "
             "The CEO's annotation contains two errors that could create significant FTC liability "
             "if implemented. The 'clinically demonstrated' language requires product-specific RCT "
             "substantiation and the 'results not typical' disclaimer provides NO protection."),
            ("[Discord #marketing kevin Tue May 27 10:00 EDT 2026] Also — can our in-house "
             "nutritionist write a review of ProBio+ for our website? She's excited about the "
             "product. Would not mention she works here.",
             "This would violate 16 CFR §465.5 (Consumer Reviews Rule, effective Oct 21, 2024). "
             "Company insiders — including employees and agents — are prohibited from writing "
             "reviews without clearly disclosing their material connection to the company. An "
             "undisclosed employee review would be a per se violation of Part 465 and could incur "
             "a civil penalty of $51,744. The nutritionist must either disclose her employment "
             "relationship prominently, or refrain from posting a review."),
        ])

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
# 8. Updates（2 次，含 supersede）
# --------------------------------------------------------------------------- #
def gen_updates(sess_ids: dict) -> dict:
    s_feishu_id = sess_ids["history"][1][0]

    # ── Update 1（Q7 后）：CEO 飞书撤回 "clinically demonstrated" 措辞 ──────────
    # feishu session 追加段
    u1_dir = UPD / "upd1_sessions"

    ceo_update_turns = [
        ("[Feishu CEO-James Fri May 30 08:00 EDT 2026] "
         "Maria — after reviewing the legal team's advice and the FTC enforcement cases, "
         "I'm formally withdrawing my request to keep 'clinically demonstrated to support "
         "immune function' in the press release. That language is too risky. Please proceed "
         "with Q8 review using the v2 draft which removes that phrase. The revised language "
         "'supports immune health based on our proprietary blend' is what I proposed — "
         "I understand this still needs formal compliance analysis. (supersedes my earlier "
         "Feishu message approving the original draft language)",
         "Noted. CEO Park's formal Feishu message supersedes his earlier informal approval of "
         "'clinically demonstrated' language. The Q8 review will use press_release_draft_v2.md "
         "and will evaluate 'supports immune health based on our proprietary blend' against "
         "current FTC substantiation standards. This supersede is recorded in the compliance log."),
        ("[Feishu CCO-Maria Fri May 30 09:00 EDT 2026] "
         "I want to confirm Sarah Chen's position on the 2009 'results not typical' safe harbor. "
         "She's been clear this was abolished. I'll note that for the record.",
         "Confirmed: Sarah Chen's analysis is correct. The 'results not typical' safe harbor "
         "was abolished in the 2009 revision of the Endorsement Guides and does not appear in "
         "the 2023 version (effective July 26, 2023). Any legal advice citing this safe harbor "
         "as currently valid is relying on superseded regulatory guidance. "
         "This has been flagged in the Slack analysis for Q7."),
    ]

    u1_seg = SessionBuilder(s_feishu_id, CWD, "2026-05-30T08:00:00", is_main=False)
    for u_text, a_text in ceo_update_turns:
        u1_seg.add_user(u_text)
        u1_seg.add_assistant(a_text)
    msg_lines = [ln for ln in u1_seg.lines if ln.get("type") == "message"]
    u1_feishu_seg = "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines) + "\n"
    w(u1_dir / f"{s_feishu_id}.jsonl", u1_feishu_seg)

    # Update 1 workspace 文件：press_release_draft_v2.md 已在初始 WS，此处提供补充 FTC notice
    u1_workspace_notice = """# FTC Notice of Penalty Offenses — Substantiation (Internal Brief)
## Prepared by Sarah Chen, In-house Counsel
## Date: May 30, 2026

This brief summarizes the FTC's April 2023 Notice of Penalty Offenses on Substantiation,
which VitaCore received on April 18, 2023, regarding OTC drugs, dietary supplements, and
functional food companies.

## Five Penalty Offense Categories

The FTC identified five categories of conduct that constitute penalty offenses:

① **Lacking competent evidence for product claims**: Making advertising claims without
   competent and reliable evidence to support them at the time the claims are made.

② **Missing scientific support for health/safety claims**: Making health or safety claims
   without adequate scientific support — typically requiring multiple well-controlled studies.

③ **Disease treatment without RCT**: Making disease treatment or prevention claims without
   at least one well-controlled human clinical trial (RCT) specifically supporting the claim.

④ **Misrepresenting substantiation level**: Claiming to have more rigorous evidence than
   actually exists (e.g., citing animal studies as if equivalent to RCT evidence).

⑤ **False proof claims**: Using "scientifically proven," "clinically demonstrated," or
   "clinically proven" when the available evidence does not meet the standard for such
   characterizations.

## Key Implications for ProBio+ Daily

- "Clinically demonstrated to support immune function" — CATEGORY ⑤ violation risk
  if product-specific RCT for the full blend does not exist
- "Scientifically proven to support energy metabolism" — CATEGORY ⑤ violation risk
- "Results not typical" disclaimer — does NOT provide safe harbor (abolished 2009)

## Penalty Level

The applicable civil penalty is **$51,744 per violation** (2024 adjusted rate).
Note: The rate was $50,120 at the time the April 2023 letters were sent; it was adjusted
to $51,744 for 2024 and subsequently to $53,088 effective February 2025.

For ProBio+ purposes, we use the 2024 baseline of $51,744 per violation.

---
Sarah Chen, Esq. | In-house Counsel | VitaCore Inc.
"""
    w(UPD / "upd1_workspace" / "ftc_penalty_offenses_brief_v1.md", u1_workspace_notice)

    # ── Update 2（Q11 后，双层 supersede）：外部审计修订函 + 2024 执法案例 ────
    u2_sessions_dir = UPD / "upd2_sessions"
    u2_workspace_dir = UPD / "upd2_workspace"

    # 新 session：外部审计修订函（从 email 渠道到 compliance）
    s_email_id = sess_ids["history"][2][0]
    revised_audit_sb = SessionBuilder(s_email_id, CWD, "2026-06-02T09:00:00", is_main=False)
    revised_audit_sb.add_user(
        "[Email ComplianceCounselLLC → Dr.Santos Mon Jun 02 09:00 EDT 2026] "
        "Subject: REVISED COMPLIANCE OPINION v2 — ProBio+ Daily (supersedes prior opinion)\n\n"
        "Dear Dr. Santos,\n\n"
        "This revised opinion (v2) supersedes our initial compliance opinion dated May 28, 2026.\n\n"
        "**CORRECTION — 'Doctor-Formulated' Claim (Point 3 of prior opinion REVISED)**:\n"
        "We are withdrawing our conditional permission for the 'Doctor-formulated' claim.\n"
        "Upon further review, we find that 'Doctor-formulated' implies an endorsement claim under "
        "16 CFR §255.3. Per FTC Health Products Compliance Guidance (December 2022), "
        "'doctor recommended' and analogous claims (including 'doctor-formulated') require:\n"
        "(a) Substantial competent scientific evidence that the product achieves the claimed benefit;\n"
        "(b) The formulating physician must have actually conducted a meaningful review;\n"
        "(c) Any material connection MUST be disclosed per §255.5.\n"
        "Given that the advisory board physician's material connection has not been disclosed "
        "in any marketing materials, and given that the product's current evidence base does not "
        "rise to 'substantial competent scientific evidence' for the immune claim, we now classify "
        "'Doctor-formulated' as REQUIRES_SUBSTANTIATION: true.\n\n"
        "**CORRECTION — 'Biodegradable Capsule Shells' Claim (NEW FINDING)**:\n"
        "We have reviewed the packaging claims and must add a new finding: "
        "The 'Biodegradable Capsule Shells' claim requires independent testing documentation "
        "demonstrating complete breakdown within one year after customary disposal per "
        "16 CFR §260.8. BioTherm HDPE capsule shells typically do not biodegrade within one year "
        "in landfill conditions. Without such testing documentation, the claim is at high risk.\n\n"
        "**CORRECTION — 'Results not typical' reference in prior opinion RETRACTED**:\n"
        "Our prior opinion erroneously referenced the 2009 Endorsement Guides' "
        "'results not typical' safe harbor. This safe harbor was abolished in the 2009 revision "
        "and does not exist under the current 2023 Endorsement Guides (effective July 26, 2023). "
        "We retract that portion of our prior opinion entirely.\n\n"
        "**Note on CEO Informal Guidance (indirect supersede)**:\n"
        "We are aware of informal guidance from VitaCore's CEO suggesting that 'supports immune "
        "health based on our proprietary blend' may be acceptable without formal substantiation. "
        "We must clarify that informal guidance from a non-legal internal officer does NOT "
        "override FTC regulatory requirements. 'Supports immune health' still requires competent "
        "and reliable scientific evidence (at minimum one well-controlled RCT for that specific claim).\n\n"
        "This opinion letter (v2) is identified in your compliance system as: email_revised_audit_v2\n\n"
        "Regards,\nCompliance Counsel LLC"
    )
    revised_audit_sb.add_assistant(
        "Received Compliance Counsel LLC Revised Opinion v2 (email_revised_audit_v2). "
        "Critical updates:\n"
        "1. SUPERSEDE: 'Doctor-formulated' conditional permission from initial email is REVOKED. "
        "Now classified requires_substantiation: true.\n"
        "2. NEW FINDING: 'Biodegradable Capsule Shells' requires independent test documentation "
        "per 16 CFR §260.8 one-year standard.\n"
        "3. RETRACTION: 'Results not typical' reference in prior opinion is formally retracted — "
        "safe harbor abolished in 2009, confirmed absent from 2023 Guides.\n"
        "4. INDIRECT SUPERSEDE: The revised opinion also implicitly overrides CEO Park's informal "
        "guidance on 'supports immune health based on proprietary blend' — FTC requirements "
        "cannot be overridden by internal officer guidance. This is the second layer of supersede."
    )
    revised_audit_sb.write(u2_sessions_dir / f"{s_email_id}.jsonl")

    # Update 2 workspace 文件
    ftc_enforcement_2024 = """# FTC Enforcement Cases 2024 — Dietary Supplements and Health Claims
## Compiled for ComplianceAI Reference
## Source: FTC press releases and consent orders (public documents)

---

## Overview

2024 saw significant FTC enforcement activity in health products advertising, building on the
April 2023 Notice of Penalty Offenses letters. Key enforcement themes:

1. Substantiation for immune and digestive health claims
2. "Clinically proven" language without adequate RCT evidence
3. Made in USA violations
4. Undisclosed endorsements and fake reviews

---

## Case 1: Kubota North America Corporation (January 2024)

**Charge**: False "Made in USA" labeling on tractors and attachments
**Rule**: 16 CFR Part 323 (Made in USA Labeling Rule)
**Resolution**: $2,000,000 civil penalty (consent order)
**Significance**: LARGEST Made in USA penalty ever imposed
**Implication for ProBio+**: VitaCore's Danish-sourced probiotic strains represent a
significant foreign functional component. The Kubota case signals FTC's willingness to
impose 7-figure penalties for major Made in USA violations. Risk level: HIGH.

---

## Case 2: Weight Loss Supplement Company (2024, name under enforcement order)

**Charge**: Made health claims including "clinically demonstrated to reduce body fat"
without adequate substantiation (2 in vitro studies only, no human RCT)
**Rule**: 16 CFR §255.1; FTC Health Products Compliance Guidance; Notice of Penalty Offenses
**Resolution**: $4.2 million restitution; prior notice penalty enhancement applied
**Significance**: First case where the April 2023 Notice of Penalty Offenses created
enhanced civil liability. The "clinically demonstrated" language with only in vitro evidence
was specifically cited as the core violation.
**Implication for ProBio+**: "Clinically demonstrated to support immune function" with
Bi-07/299v evidence (in vitro + animal only) would replicate the exact pattern.

---

## Case 3: Influencer Network Enforcement Action (2024)

**Charge**: National influencer network that facilitated undisclosed paid endorsements
for multiple dietary supplement brands
**Rule**: 16 CFR §255.5; §465.4 (purchased reviews)
**Resolution**: Consent orders; multiple individual influencers required to implement
disclosure compliance programs; brands fined $51,744 per undisclosed post
**Significance**: Confirms that platform "Paid Partnership" tags alone are insufficient.
The FTC specifically noted that "#sponsored" in hashtag lists at the end of captions
was NOT sufficient disclosure.
**Implication for ProBio+**: @drwellnessnetwork and @healthcoach_jay posts must have
"#ad" or "Ad:" explicitly at the BEGINNING of captions, not in hashtag chains.

---

## Case 4: Review Suppression Action (2024)

**Charge**: Company used cease-and-desist letters and review platform complaints to
suppress negative reviews without legitimate legal basis
**Rule**: 16 CFR §465.7 (Review Suppression — first enforcement action under this new rule)
**Resolution**: $1.2 million civil penalty + compliance program
**Significance**: First enforcement under §465.7 (Consumer Reviews Rule effective Oct 21, 2024).
Demonstrates FTC's intent to enforce the new rule aggressively.
**Implication for ProBio+**: VitaCore's review management policy must explicitly prohibit
unfounded legal threats or intimidation targeting reviewers.

---

## Penalty Schedule Reference (2024)

| Violation Type | Per-Violation Penalty (2024) |
|----------------|------------------------------|
| Any 16 CFR Part 465 violation | $51,744 |
| FTC Act Section 5 (post Notice of Penalty Offenses) | Civil penalty available |
| Made in USA violations (16 CFR Part 323) | Civil penalty; Kubota: $2M aggregate |

Note: $51,744 per violation reflects the 2024 adjusted rate. This was subsequently
adjusted to $53,088 effective February 2025. For all ProBio+ compliance analysis,
use the 2024 baseline of $51,744 per violation.

---

## Strategic Implications for ProBio+ Launch

Based on 2024 enforcement trends, the following claims carry the highest risk:

**CRITICAL RISK** (remove immediately):
- "Clinically demonstrated" without product-specific RCT
- "Scientifically proven" for any health benefit
- "Made in USA" with Danish-sourced key functional ingredients
- Influencer posts without "#ad" or "Ad:" at the beginning

**HIGH RISK** (modify before launch):
- "May help" / "helps" / "promising" / "preliminary" language
- "Doctor-formulated" without material connection disclosure
- "Biodegradable" without testing documentation
- "Recyclable" without 60% facility access documentation
"""
    w(u2_workspace_dir / "ftc_enforcement_cases_2024.md", ftc_enforcement_2024)

    green_claims_test_report = """# ProBio+ Daily — Green Claims Test Reports
## Prepared by: Packaging Compliance Team
## Date: June 1, 2026

---

## Executive Summary

This report documents testing and documentation review for the environmental claims
on ProBio+ Daily packaging. Required per Compliance Counsel LLC revised opinion (v2)
and 16 CFR Part 260 (Green Guides).

---

## Claim 1: "Biodegradable Capsule Shells"

### Regulatory Standard
Per 16 CFR §260.8: An unqualified biodegradable claim requires that the product
completely break down within **one year** after customary disposal.

### Testing Results

BioTherm HDPE Capsule Shell Biodegradation Assessment:
- Material type: High-Density Polyethylene (HDPE) — Class A plastic
- ASTM D5338 test (aerobic biodegradation in composting conditions): 12-month result: 2.3% degradation
- ISO 14855 test (aerobic biodegradation): 12-month result: 1.8% degradation
- Typical landfill conditions: Essentially zero biodegradation in 1 year

**FINDING**: HDPE capsule shells do NOT biodegrade within one year under any common
disposal condition (landfill, recycling, standard composting). The unqualified
"Biodegradable Capsule Shells" claim is NOT SUPPORTED and should be removed or
replaced with accurate language.

**Recommended alternative**: Remove claim entirely. If biodegradable capsule shell
material is desired, VitaCore should source HPMC (hydroxypropyl methylcellulose) or
plant-based cellulose capsule shells with documented biodegradation rates.

---

## Claim 2: "Eco-Friendly Packaging"

### Regulatory Standard
Per 16 CFR §260.1: Unqualified general environmental benefit claims are likely to
deceive consumers. Must be qualified with specific benefit claimed.

### Assessment
"Eco-Friendly Packaging" as used on ProBio+ label is unqualified. No specific
environmental benefit is stated. The packaging uses:
- HDPE bottle (recyclable where facilities available)
- Paperboard outer carton (partially recycled content — 40%)
- Foil liner (generally not recyclable)

**FINDING**: The unqualified "Eco-Friendly Packaging" claim is at risk under §260.1.
A qualified claim referencing the specific recyclable components would be permissible
if substantiated. The claim in current form should be modified.

---

## Claim 3: "Recyclable Packaging"

### Regulatory Standard
Per 16 CFR §260.12: Unqualified "recyclable" claim requires ≥60% of consumers/communities
to have access to facilities that can recycle the specific material.

### Assessment

| Component | Material | Recycling Access (US) |
|-----------|---------|----------------------|
| Primary bottle | HDPE (#2 plastic) | ~80% of US communities ✓ |
| Outer carton | Paperboard | ~75% of US communities ✓ |
| Foil liner | Aluminum + plastic laminate | ~15% of US communities ✗ |
| Label | Paper + adhesive | Varies |

The composite packaging assembly including the foil liner does not meet the 60% threshold
for the complete packaging unit. However, the primary bottle and outer carton individually
would meet the standard.

**FINDING**: An unqualified "Recyclable Packaging" claim (referring to the complete package)
is at risk because the foil liner is not recyclable in most communities. A qualified claim
is permissible: "Bottle and carton recyclable where facilities available."

---

## Recommendations

1. Remove unqualified "Biodegradable Capsule Shells" claim immediately — NOT substantiated
2. Modify "Eco-Friendly Packaging" to specify which environmental benefit is claimed
3. Qualify "Recyclable Packaging" to exclude foil liner from the claim scope
"""
    w(u2_workspace_dir / "green_claims_test_reports.md", green_claims_test_report)

    # Update 1 large data file — FTC industry-wide penalty tracking
    import io, csv as csv_mod, random as _random
    _rng1 = _random.Random(1001)
    upd1_fields = [
        "company_id", "company_name", "industry_segment", "notice_received_date",
        "notice_type", "violations_alleged", "penalty_per_violation_usd",
        "total_penalty_usd", "resolution_type", "resolution_date",
        "consent_order_provisions", "advertising_claims_flagged",
        "evidence_standard_failed", "disclosure_issues", "status"
    ]
    upd1_rows = [upd1_fields]
    company_types = [
        "probiotic_supplement", "weight_loss_supplement", "immune_supplement",
        "energy_supplement", "anti_aging_supplement", "digestive_supplement",
        "sleep_supplement", "cognitive_supplement", "beauty_supplement"
    ]
    violation_types = [
        "clinically demonstrated without RCT", "scientifically proven without evidence",
        "may help support (prohibited qualifier)", "promising results (prohibited qualifier)",
        "preliminary studies (prohibited qualifier)", "undisclosed paid endorsement",
        "results not typical disclaimer", "fake reviews", "insider reviews undisclosed",
        "review suppression", "Made in USA false claim", "biodegradable false claim"
    ]
    resolution_types = ["consent_order", "civil_penalty_settlement", "voluntary_correction",
                        "no_action_letter", "ongoing_investigation"]
    for i in range(670):  # 2023 April 670 companies received Notice of Penalty Offenses
        segment = _rng1.choice(company_types)
        viol_count = _rng1.randint(1, 8)
        viol_list = "; ".join(_rng1.sample(violation_types, min(viol_count, len(violation_types))))
        notice_date = f"2023-04-{_rng1.randint(10, 28):02d}"
        resolution = _rng1.choice(resolution_types)
        penalty = 51744.0 * _rng1.randint(1, 15) if resolution == "civil_penalty_settlement" else 0.0
        provisions = "Prohibition on further violations; compliance monitoring; consumer redress" if resolution != "no_action_letter" else "None"
        upd1_rows.append([
            f"CO-{i+1:04d}", f"Supplement Co. {i+1}", segment, notice_date,
            "Notice of Penalty Offenses (Substantiation)", viol_count, 51744.0,
            penalty, resolution, f"2024-{_rng1.randint(1, 12):02d}-{_rng1.randint(1, 28):02d}",
            provisions, viol_list,
            "RCT required but not available", _rng1.choice(["YES", "NO"]),
            _rng1.choice(["RESOLVED", "OPEN", "PENDING"])
        ])
    buf1 = io.StringIO()
    csv_mod.writer(buf1).writerows(upd1_rows)
    w(UPD / "upd1_workspace" / "ftc_670_companies_penalty_offenses.csv", buf1.getvalue())

    # Update 2 large data file — comprehensive evidence assessment database
    _rng2 = _random.Random(2002)
    upd2_fields = [
        "study_id", "product_tested", "ingredient", "study_type",
        "control_group", "randomized", "blinded", "sample_size",
        "duration_weeks", "primary_endpoint", "result_direction",
        "statistical_significance_p", "clinical_meaningful",
        "ftc_evidence_tier", "standalone_sufficient_for_claim",
        "claim_type_supported", "limitations", "funding_source",
        "publication_year", "journal", "ftc_assessment"
    ]
    upd2_rows = [upd2_fields]
    study_types = ["RCT", "open_label_trial", "cohort_study", "pilot_study",
                   "in_vitro", "animal_model", "consumer_survey", "meta_analysis"]
    endpoints = [
        "immune_markers_IgA", "NK_cell_activity", "URTI_frequency",
        "gut_microbiome_diversity", "stool_consistency", "bloating_score",
        "energy_levels_self_report", "cognitive_performance", "skin_hydration",
        "inflammatory_markers", "antioxidant_capacity", "bioavailability"
    ]
    ingredients = [
        "Lactobacillus rhamnosus GG", "Lactobacillus acidophilus NCFM",
        "Bifidobacterium lactis Bi-07", "Lactobacillus plantarum 299v",
        "Vitamin B6 (Pyridoxine HCl)", "Vitamin B12 (Methylcobalamin)",
        "Folate (L-Methylfolate)", "Biotin (D-Biotin)", "Niacin (Niacinamide)",
        "Pantothenic Acid", "Thiamine HCl", "Riboflavin"
    ]
    funding = ["Industry (manufacturer)", "Academic institution", "NIH grant",
               "EU research fund", "Industry + independent verification"]
    journals = ["JAMA", "NEJM", "Gut Microbes", "Nutrients", "Probiotics & Antimicrobials",
                "J Clinical Nutrition", "Am J Clinical Nutrition", "BMJ Open",
                "J Functional Foods", "Food Research International"]
    for i in range(350):
        ingredient = _rng2.choice(ingredients)
        study_type = _rng2.choice(study_types)
        has_control = study_type in ("RCT", "meta_analysis")
        is_rct = study_type == "RCT"
        blinded = is_rct and _rng2.random() > 0.2
        n = _rng2.randint(15, 450) if study_type != "in_vitro" else 0
        duration = _rng2.randint(4, 52) if study_type not in ("in_vitro", "animal_model") else _rng2.randint(1, 8)
        endpoint = _rng2.choice(endpoints)
        direction = _rng2.choice(["positive", "positive", "positive", "neutral", "negative"])
        p_val = round(_rng2.uniform(0.001, 0.25), 4) if direction != "neutral" else round(_rng2.uniform(0.1, 0.8), 4)
        sig = p_val < 0.05
        clin_meaningful = sig and _rng2.random() > 0.4 and is_rct
        if is_rct and has_control and sig:
            tier = "Tier_1_RCT"
            sufficient = "YES"
        elif study_type in ("pilot_study", "open_label_trial"):
            tier = "Tier_2_pilot"
            sufficient = "NO"
        elif study_type in ("in_vitro", "animal_model", "consumer_survey"):
            tier = "Tier_3_insufficient"
            sufficient = "NO"
        elif study_type == "meta_analysis":
            tier = "Tier_1_meta_analysis"
            sufficient = "YES"
        else:
            tier = "Tier_2_observational"
            sufficient = "CONDITIONAL"
        claim = "immune_function" if "immune" in endpoint or "IgA" in endpoint or "NK" in endpoint else \
                "digestive_health" if "gut" in endpoint or "stool" in endpoint or "bloating" in endpoint else \
                "energy_metabolism"
        limitations_text = "; ".join(_rng2.sample([
            "small sample size", "short duration", "no control group",
            "industry funded", "single center", "healthy volunteers only",
            "no product-specific testing", "surrogate endpoints only",
            "no blinding", "high dropout rate"
        ], _rng2.randint(1, 4)))
        upd2_rows.append([
            f"STU-{i+1:04d}", "ProBio+ Daily component", ingredient, study_type,
            "YES" if has_control else "NO",
            "YES" if is_rct else "NO",
            "YES" if blinded else "NO",
            n, duration, endpoint, direction, p_val,
            "YES" if clin_meaningful else "NO",
            tier, sufficient, claim, limitations_text,
            _rng2.choice(funding), _rng2.randint(2015, 2025),
            _rng2.choice(journals),
            f"{'Adequate' if sufficient == 'YES' else 'Insufficient'} for {claim} claim under FTC standards"
        ])
    buf2 = io.StringIO()
    csv_mod.writer(buf2).writerows(upd2_rows)
    w(UPD / "upd2_workspace" / "clinical_evidence_assessment_database.csv", buf2.getvalue())

    # updates 声明
    updates_decl = {
        "upd1_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd1_sessions",
            "files": [{
                "name": f"{s_feishu_id}.jsonl",
                "action": "append",
                "target": f"{s_feishu_id}.jsonl"
            }]
        },
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {
                    "name": "ftc_penalty_offenses_brief_v1.md",
                    "action": "new",
                    "target": "regulatory/ftc_penalty_offenses_brief_v1.md"
                },
                {
                    "name": "ftc_670_companies_penalty_offenses.csv",
                    "action": "new",
                    "target": "research/ftc_670_companies_penalty_offenses.csv"
                }
            ]
        },
        "upd2_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd2_sessions",
            "files": [{
                "name": f"{s_email_id}.jsonl",
                "action": "append",
                "target": f"{s_email_id}.jsonl"
            }]
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {
                    "name": "ftc_enforcement_cases_2024.md",
                    "action": "new",
                    "target": "regulatory/ftc_enforcement_cases_2024.md"
                },
                {
                    "name": "green_claims_test_reports.md",
                    "action": "new",
                    "target": "research/green_claims_test_reports.md"
                },
                {
                    "name": "clinical_evidence_assessment_database.csv",
                    "action": "new",
                    "target": "research/clinical_evidence_assessment_database.csv"
                },
            ]
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

    gen_system_files()
    gen_company_files()
    gen_regulatory_files()
    gen_draft_files()
    gen_research_files()
    gen_report_files()
    gen_supplemental_files()
    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = (
        "FTC健康声明实质性核实 (prd1a) — VitaCore ProBio+ Daily 产品发布合规审查，"
        "17 轮 exec_check，2 次 update（含双层 supersede），5 条 preference（P1-P5），"
        "难度向量 V1/V2/V3/V4/V5/V6/V7/V8/V9/V10。"
        "真实来源：FTC Health Products Compliance Guidance Dec 2022 "
        "(https://www.ftc.gov/business-guidance/resources/health-products-compliance-guidance)；"
        "16 CFR Part 255 Endorsement Guides 2023 "
        "(https://www.law.cornell.edu/cfr/text/16/part-255)；"
        "16 CFR Part 465 Consumer Reviews Rule "
        "(https://www.law.cornell.edu/cfr/text/16/part-465)；"
        "FTC Policy Statement on Advertising Substantiation "
        "(https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation)；"
        "16 CFR Part 323 Made in USA Rule "
        "(https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-323)；"
        "16 CFR Part 260 Green Guides "
        "(https://www.law.cornell.edu/cfr/text/16/part-260)"
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
    print(f"[prd1a] workspace tokens ~{ws_tok:,} | sessions ~{sess_tok:,} | updates ~{upd_tok:,}")
    print(f"[prd1a] built at {DATASET}")


if __name__ == "__main__":
    main()
