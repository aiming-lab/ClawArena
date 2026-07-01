#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_prd1b.py — 生成 ClawArena 真实数据集场景 prd1b（评论真实性 + 披露合规，16 CFR Part 465/255）。

题材与锚点取材真实（FTC 16 CFR Part 465 Consumer Reviews and Testimonials Rule；
16 CFR Part 255 Endorsement Guides 2023修订版；FTC Health Products Compliance Guidance Dec 2022）。
Session 对话与 workspace 文档围绕真实锚点合成。全 exec_check，16 轮。

幂等：每次运行先清空 prd1b 的 workspace/state/updates 后重建。
questions.json 与 check 脚本由 eval/prd1b/ 下静态文件提供，本脚本不生成它们。

运行：python scripts/clawarena_authoring/build_prd1b.py
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
TID = "prd1b"
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
# Large content generators (volume padding with realistic legal/compliance text)
# --------------------------------------------------------------------------- #
def _gen_255_appendix_examples() -> str:
    """Generate ~25KB of endorsement guide examples and commentary."""
    rng = random.Random(255)
    platforms = ["Instagram", "TikTok", "YouTube", "Facebook", "Twitter/X", "Pinterest",
                 "LinkedIn", "Snapchat", "Reddit", "Twitch"]
    industries = ["dietary supplements", "skincare", "fitness equipment", "meal delivery",
                  "pet food", "organic produce", "protein powder", "herbal remedies",
                  "collagen supplements", "nootropics", "adaptogen products"]
    disclosure_forms = [
        "#ad (at beginning of post)",
        "Ad: [content]",
        "Sponsored: [content]",
        "[Paid partnership with Brand] at post start",
        "GIFTED: [content]",
        "Paid promotion disclosed verbally at video start",
    ]
    inadequate_forms = [
        "#ad buried after 20 hashtags",
        "Only relying on Instagram 'Paid Partnership' banner",
        "Footnote disclosure at bottom of long post",
        "Disclosure in bio rather than in the post itself",
        "Disclosure in the 'read more' collapsed section",
        "Click-through link to separate disclosure page",
    ]

    sections = []

    # Generate example scenarios
    for i in range(1, 31):
        platform = rng.choice(platforms)
        industry = rng.choice(industries)
        is_adequate = rng.random() > 0.5
        form = rng.choice(disclosure_forms if is_adequate else inadequate_forms)
        influencer_type = rng.choice(["micro-influencer (10K-100K)", "macro-influencer (100K-1M)",
                                      "mega-influencer (1M+)", "nano-influencer (<10K)",
                                      "celebrity (entertainment)", "expert (doctor/scientist)",
                                      "athlete/sports figure"])
        compensation = rng.choice(["monetary payment", "free product sample", "affiliate commission",
                                   "discount code", "early access", "prize/giveaway entry",
                                   "event invitation", "travel coverage", "co-branding deal"])
        verdict = "ADEQUATE" if is_adequate else "INADEQUATE"

        section = f"""#### Example {i}: {platform} — {influencer_type}

**Industry**: {industry}
**Compensation type**: {compensation}
**Disclosure form**: {form}
**§255.5 Assessment**: {verdict}

"""
        if is_adequate:
            section += (f"The disclosure form '{form}' satisfies §255.5's clear and conspicuous "
                        f"requirement for a {influencer_type} promoting {industry} on {platform}. "
                        f"The consumer can readily identify the commercial nature of the content "
                        f"before engaging with the promotional message. The FTC's 2023 Guides "
                        f"specifically endorse this approach for {platform}-style content. "
                        f"The {compensation} relationship is fully and adequately disclosed.\n\n")
        else:
            section += (f"The disclosure form '{form}' does NOT satisfy §255.5's clear and "
                        f"conspicuous requirement. When a {influencer_type} uses this approach "
                        f"on {platform} for {industry}, the material connection ({compensation}) "
                        f"is not obvious to ordinary consumers. The FTC's 2023 Guides specifically "
                        f"identify this pattern as inadequate. The {compensation} relationship "
                        f"creates an expectation of bias that must be clearly communicated. "
                        f"Without adequate disclosure, this endorsement is deceptive under §5 "
                        f"of the FTC Act and may attract civil penalties of $51,744 per violation.\n\n")

        sections.append(section)

    # Add regulatory commentary sections
    commentary_sections = [
        """### Application to AI-Generated Content

The 2023 revision to 16 CFR Part 255 explicitly addresses AI-generated endorsements
and virtual influencers. Key points:

1. **AI-generated endorsements must be disclosed**: If an AI system generates a
   testimonial or endorsement that appears to reflect the experience of a real consumer,
   the AI origin must be clearly disclosed.

2. **Virtual influencers**: A company-controlled virtual character (CGI avatar, AI persona)
   that endorses a product must disclose the commercial relationship just as a human
   influencer would. The disclosure must make clear that the "endorser" is not an
   independent real person.

3. **Generative AI content at scale**: Companies using large language models to
   generate consumer reviews or testimonials are creating "fake" reviews per §465.2,
   regardless of whether the AI is instructed to write positive or balanced reviews.
   The FTC has made clear this constitutes a §465.2(a) violation.

4. **Bot-generated social media activity**: Purchasing bot-generated likes, followers,
   and comments that misrepresent consumer acceptance of a product violates §465.8.

**Practical implication for VitaCore**: If VitaCore uses AI tools to draft social media
posts attributed to real consumers or influencers, those posts must clearly disclose
their AI-assisted origin AND the commercial relationship.

""",
        """### The Material Connection Spectrum

The concept of "material connection" under §255.5 spans a wide range of arrangements:

**Clearly material connections** (always require disclosure):
- Direct monetary payment for a specific post or campaign
- Free products provided with expectation of review or promotion
- Equity stake or financial interest in the company
- Employment relationship with the company or its affiliates
- Family relationship with company officers or directors

**Potentially material connections** (context-dependent):
- Deeply discounted products (below market value)
- Early access to products before general availability
- Invitation to exclusive brand events (travel, experiences)
- Entry into sweepstakes or contests contingent on posting
- Ongoing affiliate commission arrangements

**Generally not material connections**:
- A product purchased at full retail price with no other relationship
- An unsolicited free product where no review is requested or expected

**The test**: Would the connection "materially affect the weight or credibility" of
the endorsement in the eyes of the consumer? If yes, it must be disclosed.

Per §255.5 verbatim: "a connection between the endorser and the seller of the advertised
product that might materially affect the weight or credibility of the endorsement."

""",
        """### FTC's Clear and Conspicuous Standard — Detailed Analysis

The "clear and conspicuous" standard for disclosures is evaluated based on the
totality of the advertisement. Key factors:

**1. Proximity**
Disclosures must appear near the claims they qualify. A disclosure at the bottom
of a lengthy social media post fails if the promotional claims appear at the top.

**2. Prominence**
Font size, color contrast, and visual prominence must ensure the disclosure is
noticeable. In video content, both audio and visual disclosure are recommended.

**3. Placement in sequential order**
For multi-page or multi-screen content, disclosures should appear before claims,
not after. For social media, this means the disclosure should precede the content.

**4. The "difficult to miss" standard**
The FTC describes the standard as: disclosures must be "difficult to miss and be
easily understandable by ordinary consumers." This is a consumer-perspective test,
not a technical compliance checklist.

**5. Platform-specific considerations**
- Instagram posts with expandable text: disclosure must appear in the visible
  portion, not in the "more" section.
- YouTube videos: verbal disclosure at the opening AND on-screen text are recommended.
- Twitter/X: disclosure must fit within character limit and appear prominently.
- TikTok: verbal disclosure in first few seconds; text overlay recommended.

**6. Hashtag placement hierarchy**
If hashtags are used for disclosure:
- "#ad" at the very beginning of the post = adequate
- "#ad" first in the hashtag list (after content) = generally adequate
- "#ad" in the middle or end of a long hashtag list = inadequate
- "#sponsored" buried among topic hashtags = inadequate

""",
        """### Enforcement Patterns and Settlement Terms

FTC enforcement actions under 16 CFR Part 255 and Part 465 generally result in:

**Consent orders typically include**:
1. Prohibition on future violations for a defined period (often 20 years)
2. Implementation of a compliance monitoring program
3. Employee training requirements
4. Record-keeping obligations (3-5 years)
5. Reporting requirements to the FTC (periodic compliance certifications)

**Civil penalty factors**:
The Commission considers the following in determining penalty amounts:
- Duration of the violative practice
- Number of affected consumers
- Prior FTC contact (Notice of Penalty Offenses issued)
- Degree of consumer harm
- Company's compliance posture (cooperation vs. obstruction)

**Per-violation counting**:
Each fake review constitutes a separate violation.
Each inadequately disclosed influencer post constitutes a separate violation.
A campaign with 14 influencers each making 3 posts = 42 separate violations.
At $51,744 per violation: $2,173,248 in potential liability.

**Settlement ranges observed in 2024 enforcement actions**:
- Single-influencer disclosure violation: $51,744 (1 violation)
- Employee review campaign (200+ reviews): $10,348,800 (200 violations)
- Fake review purchase scheme (1,000+ reviews): Up to $51,744,000
- Hybrid (fake reviews + disclosure failures): $1–5 million range typical

""",
    ]

    header = """## Appendix C — Extended Examples and Commentary

### Overview

The following examples illustrate the application of §255.5 (Disclosure of Material
Connections) across various platforms, industries, and influencer types. These examples
supplement the core regulatory text and should be used to guide compliance assessments.

All examples reflect the state of FTC guidance as of the 2023 revision to 16 CFR Part 255
(effective July 26, 2023) and the 2024 effective date of 16 CFR Part 465.

"""
    return header + "\n".join(sections) + "\n".join(commentary_sections)


def _gen_465_appendix() -> str:
    """Generate ~20KB of Part 465 detailed commentary and case studies."""
    rng = random.Random(465)

    fake_companies_and_cases = []
    for i in range(1, 26):
        company = rng.choice([
            "NutraShield Corp.", "VitaBoost LLC", "PureForm Supplements", "BioEssentials Inc.",
            "HealthEdge Brands", "NaturePath Solutions", "WellMax Inc.", "CleanNutrition Corp.",
            "SupplePro LLC", "BioActive Health", "NutriPrime Inc.", "VitalSource Brands",
            "CoreHealth LLC", "PureLife Supplements", "ActiveNutrition Corp.",
        ])
        violation_type = rng.choice([
            "§465.2(a)(1) — Reviewer does not exist (entirely fabricated persona)",
            "§465.2(a)(2) — Reviewer never used the product (fictional experience)",
            "§465.2(a)(3) — Review misrepresents actual experience (paid to write positive despite negative experience)",
            "§465.3 — Insider review without disclosure (employee posting as customer)",
            "§465.4 — Company-controlled review site not disclosed as such",
            "§465.5 — Purchased social media followers for fake popularity indicators",
            "§465.6 — Selective review display (only 4-5 star reviews shown, 1-3 star suppressed)",
            "§465.7 — Review suppression by legal threat (cease and desist to negative reviewers)",
            "§465.8 — Purchased fake social media engagement metrics",
        ])
        penalty = rng.randint(1, 15) * 51744
        resolution = rng.choice([
            "Consent order with 20-year prohibition",
            "Settlement and compliance program",
            "Injunction with civil penalty",
            "Administrative order",
        ])
        fake_companies_and_cases.append(
            f"**{company}** (Case #{1000+i}): {violation_type}. "
            f"Penalty: ${penalty:,}. Resolution: {resolution}.\n\n"
        )

    sections = [
        """## Appendix A — Detailed Analysis of §465.2 Prohibitions

### §465.2(a)(1): Fabricated Reviewer Identity

The prohibition against creating reviews that misrepresent that the reviewer exists
covers the following practices:

**Explicitly prohibited**:
- Paying a third-party service to generate reviews using fictitious personas
- Creating company-controlled social media accounts that pose as ordinary consumers
- Using AI language models to generate reviews attributed to non-existent persons
- Purchasing reviews from review mills where reviewers are paid to fabricate experiences

**Key verbatim from §465.2(a)**:
"It is an unfair or deceptive act or practice and a violation of this part for a
business to write, create, or sell a consumer review, consumer testimonial, or celebrity
testimonial that materially misrepresents, expressly or by implication:
(1) That the reviewer or testimonialist exists..."

**The "exists" standard**: The reviewer must be a real person who actually exists.
A company cannot argue that an AI-generated persona "exists" as a digital entity —
the statute requires a real human consumer.

**Third-party liability**: A company that purchases fake reviews from a review mill
is liable even if it did not create the fake reviews itself. Both the buyer and seller
of fake reviews may be subject to penalty.

### §465.2(a)(2): False Experience Claims

This section prohibits representing that a reviewer used or had experience with
a product when they did not. This covers:

- Reviews from individuals who received a product but never opened or tested it
- Reviews from friends or family who were given a product with instructions to write
  positively, without actual use
- "Beta tester" reviews where the product was not available for testing

**Note on genuine employees**: An employee who genuinely uses a product may review it,
provided the employment relationship is clearly and conspicuously disclosed. §465.3
(insider reviews) requires this disclosure. The issue under §465.2(a)(2) arises only
when the claimed "experience" never occurred.

### §465.2(a)(3): Misrepresentation of Experience

This section addresses situations where a real consumer with real experience writes
a review that misrepresents their actual experience. This covers:

- A consumer paid to write a positive review despite having a negative experience
- A consumer who experienced product failure but is incentivized to write positively
- Review platforms that alter or filter consumer-submitted reviews to make them
  appear more positive

**The "materially misrepresents" standard**: The misrepresentation must be material —
it must affect consumer purchasing decisions. Almost any misrepresentation about
product satisfaction would qualify as material.

""",
        """## Appendix B — §465.7 Review Suppression in Detail

### The Threat Prohibition

§465.7 prohibits using threats to suppress reviews. The verbatim text:
"It is an unfair or deceptive act or practice for a business (directly or through
an agent) to use, or to threaten to use, an unfounded or groundless legal threat,
a physical threat, intimidation, or a public false accusation (including public shaming)
against any person in an attempt to:
(1) Prevent a review or any portion thereof from being written or created, or
(2) Cause a review or any portion thereof to be removed."

### What Constitutes an "Unfounded or Groundless Legal Threat"

A legal threat is "unfounded or groundless" if the underlying legal claim has no
reasonable basis in law or fact. Examples:

**Clearly unfounded threats**:
- Threatening defamation suit against a negative review that is factually accurate
- Threatening trade secret claims against a consumer who honestly describes their experience
- Threatening harassment or stalking claims against a legitimate reviewer
- Sending cease-and-desist letters without any actual legal basis

**Not covered by §465.7** (legitimate legal actions):
- Cease-and-desist for reviews containing verifiably false factual claims
- Legal action for reviews containing discriminatory or harassing content
- Removal requests for reviews violating platform terms of service

### The §465.6 Connection: Discriminatory Review Display

§465.6 prohibits selectively displaying only positive reviews while suppressing
negative ones. This is distinct from §465.7 (threat-based suppression):

- §465.6 applies to *how reviews are displayed* (filtering/curation)
- §465.7 applies to *actions taken against reviewers* (intimidation/threats)

A company may legally:
- Remove reviews that are fake (§465.2 violations)
- Remove reviews containing irrelevant or inappropriate content
- Display all genuine reviews in any order

A company may NOT:
- Show only reviews above a certain star rating while hiding lower-rated genuine reviews
- Manually curate reviews to present only the most favorable selection
- Suppress reviews that mention competitor products or comparative disadvantages

""",
        f"""## Appendix C — Enforcement Case Summaries

The following cases illustrate FTC enforcement priorities under 16 CFR Part 465.
All penalties reflect the $51,744 per-violation rate applicable in 2024.

{"".join(fake_companies_and_cases)}

""",
        """## Appendix D — Compliance Program Best Practices

### Recommended Internal Controls for Consumer Review Compliance

1. **Review Policy Statement**: Adopt a written policy prohibiting the creation,
   purchase, or solicitation of fake reviews. Distribute to all relevant personnel.

2. **Insider Review Disclosure Protocol**: Establish a process for employees,
   officers, and contractors to disclose their relationship when submitting reviews.
   The disclosure must appear in or adjacent to the review itself.

3. **Influencer Agreement Requirements**: All influencer contracts must:
   - Specify that the influencer will disclose the material connection
   - Prescribe the exact disclosure language ("#ad" or "Ad:" at post beginning)
   - Prohibit the influencer from relying solely on platform "Paid Partnership" tools
   - Grant the company the right to review posts before publication for compliance

4. **Review Monitoring Program**: Establish a monitoring program to:
   - Verify influencer posts include adequate disclosures
   - Detect any fake or fabricated reviews appearing for the company's products
   - Document removal of any reviews identified as fake (per §465.2)

5. **Review Display Audit**: Periodically audit all platforms where company reviews
   appear to ensure no discriminatory display is occurring (§465.6).

6. **Employee Training**: All marketing personnel, customer service staff, and
   executives with social media access should receive annual training on:
   - §465.2 prohibitions on fake reviews
   - §465.3 insider review disclosure requirements
   - §255.5 influencer disclosure requirements
   - The $51,744 per-violation penalty exposure

7. **Recordkeeping**: Maintain records of:
   - All influencer agreements and paid relationships (3 years minimum)
   - All disclosure compliance checks for influencer posts
   - All review removal decisions and the basis for each removal
   - All training completion records

""",
    ]

    return "\n".join(sections)


def _gen_ftc_case_law_digest() -> str:
    """Generate ~40KB FTC case law and enforcement digest for VitaCore compliance reference."""
    rng = random.Random(777)
    cases = []
    case_names = [
        ("Hana Financial Inc.", 2023, "Instagram influencer undisclosed payments", "§255.5", 825984),
        ("NuVasive Inc.", 2024, "Physician endorsements without disclosure of financial relationship", "§255.3", 1034880),
        ("Endo Pharmaceuticals", 2024, "Misleading testimonials about opioid safety", "§255.2", 2068640),
        ("Rimmel London", 2023, "AI-enhanced mascara images used without disclosure", "§255.1", 517440),
        ("Fashion Nova LLC", 2024, "Suppression of negative consumer reviews", "§465.6/§465.7", 4600000),
        ("1-800 Contacts Inc.", 2023, "Bought fake 5-star reviews from review mill", "§465.2", 1500000),
        ("Rennova Health Inc.", 2024, "Hospital patient review suppression scheme", "§465.7", 311040),
        ("BioBalance Corp.", 2024, "Probiotic 'clinically proven' claim without RCT", "§255.2/Health Guidance", 724416),
        ("Wellness Tomorrow LLC", 2023, "Employee reviews posted without disclosure", "§465.3", 414120),
        ("DigiNutrition Inc.", 2024, "Purchased 2.3M fake social media followers", "§465.8", 2010016),
        ("HerbWell Corp.", 2023, "Celebrity testimonial with undisclosed paid relationship", "§255.5", 1551720),
        ("PureNature LLC", 2024, "Company-controlled review website without disclosure", "§465.4", 258720),
        ("MaxBio Health", 2023, "Used 'may help' qualifier for unsubstantiated health claim", "Health Guidance", 310464),
        ("GreenLeaf Supplements", 2024, "False 'biodegradable' claim for capsules", "§260.8/§255.1", 517440),
        ("BodyFuel Inc.", 2023, "Sent legal threat letter to negative reviewer", "§465.7", 103488),
        ("VitaSphere Corp.", 2024, "Affiliate blogger failed to disclose commission", "§255.5", 206976),
        ("NutriCore Brands", 2023, "'Doctor recommended' without named physician", "§255.3", 414120),
        ("WellStart LLC", 2024, "Fake positive reviews purchased from offshore mill", "§465.2", 3103440),
        ("ProBiotics Plus Inc.", 2023, "Animal study used to claim 'clinically supported'", "Health Guidance/§255.2", 931392),
        ("Elevate Health Corp.", 2024, "Review display algorithm showed only 4+ stars", "§465.6", 724416),
    ]
    output = """# FTC Consumer Protection Enforcement — Case Law Digest for Compliance Reference

**Prepared by**: VitaCore In-House Compliance Team
**Date**: February 2026
**Purpose**: Precedent survey supporting pre-launch compliance review of ProBio+ Daily

This digest surveys FTC enforcement actions relevant to consumer review authenticity
(16 CFR Part 465) and endorsement/testimonial disclosure (16 CFR Part 255) from
2023-2024. The cases are selected for their applicability to dietary supplement and
consumer health product marketing practices.

---

## Section 1: Overview of Enforcement Environment

### 2023-2024 Enforcement Statistics

| Category | 2023 Actions | 2024 Actions | Total Penalties |
|----------|-------------|-------------|-----------------|
| Fake/false consumer reviews (§465.2) | 14 | 19 | $47.2M |
| Insider review violations (§465.3) | 8 | 12 | $12.1M |
| Influencer disclosure failures (§255.5) | 22 | 31 | $28.7M |
| Review suppression (§465.6/§465.7) | 6 | 9 | $19.4M |
| Health claim violations | 18 | 24 | $31.8M |
| Environmental claim violations (§260.8) | 4 | 7 | $6.2M |
| **Total** | **72** | **102** | **$145.4M** |

### Applicable Civil Penalty Rates

- **2024 base rate**: $51,744 per violation (governing for ProBio+ Daily analysis)
- **2025 adjusted rate**: $53,088 per violation (effective February 2025)
- Note: The $45,000 figure cited in informal communications is ERRONEOUS.

---

## Section 2: Case Summaries

"""
    for i, (company, year, violation_type, rule_section, penalty) in enumerate(cases, 1):
        violations = penalty // 51744
        output += f"""### Case {i}: FTC v. {company} ({year})

**Violation Category**: {violation_type}
**Regulatory Basis**: 16 CFR {rule_section}
**Civil Penalty**: ${penalty:,} ({violations} violations × $51,744)
**Year**: {year}

**Factual Summary**:
{company} engaged in {violation_type.lower()} affecting consumers of their health and
wellness products. The Commission determined that the conduct violated Section 5 of the
FTC Act (15 U.S.C. §45) and, where applicable, the specific provisions of 16 CFR Part 465
or 16 CFR Part 255 identified above.

**Key Compliance Lesson**:
Following this enforcement action, {company} was required to implement a comprehensive
compliance monitoring program, conduct employee training, and submit periodic compliance
reports to the Commission. The consent order remained in effect for 20 years.

**Applicability to VitaCore ProBio+ Daily**:
VitaCore's compliance analysis should treat this case as precedent when evaluating
its own practices related to {violation_type.lower()}.

---

"""

    output += """## Section 3: Penalty Calculation Framework

### Per-Violation Counting Methodology

The FTC applies the per-violation penalty rate ($51,744 in 2024) to each discrete
instance of a violative act. For VitaCore ProBio+ Daily's pre-launch risk assessment:

**Scenario 1: Employee Review Campaign**
- 40 employees post reviews without disclosure
- Each post = 1 violation under §465.3
- Exposure: 40 × $51,744 = $2,069,760

**Scenario 2: Influencer Non-Disclosure (14 influencers)**
- 14 influencer relationships currently lacking adequate disclosure
- Each inadequate post = 1 violation under §255.5
- If each influencer posts 3 times: 42 violations
- Exposure: 42 × $51,744 = $2,173,248

**Scenario 3: Fake Reviews (from hypothetical purchase)**
- If 100 fake reviews were purchased (not alleged — hypothetical only)
- Each fake review = 1 violation under §465.2
- Exposure: 100 × $51,744 = $5,174,400

**Scenario 4: Health Claim Violations (6 claims)**
- "May help support immune function" (1)
- "Promising preliminary research" (2 prohibited terms = 1 violation)
- "Clinically demonstrated" without RCT for B. longum (1)
- "Doctor-Formulated" without complete §255.3 compliance (1)
- "Backed by science" without specific evidence cited (1)
- Exposure: 6 × $51,744 = $310,464

**Combined Pre-Launch Exposure**: $9,727,872 (before mitigation)

### Mitigation Factors

The Commission considers the following in reducing penalties:
1. **Voluntary disclosure**: Self-reporting violations before enforcement action
2. **Swift remediation**: Promptly removing violative content and claims
3. **Cooperation**: Providing full cooperation during investigation
4. **Compliance program**: Demonstrating existence of a pre-existing compliance program
5. **No prior enforcement**: First offense in the relevant category

---

## Section 4: Implications for VitaCore ProBio+ Daily

### Critical Path to Compliant Launch

Based on the enforcement landscape documented above, VitaCore must:

1. **Eliminate all prohibited qualifying language** from press release and ad copy
   (see A11 prohibited terms: "may," "helps," "promising," "preliminary," "initial," "pilot")

2. **Establish influencer disclosure protocol** requiring "#ad" or "Ad:" at the
   beginning of all influencer posts — not buried in hashtag lists

3. **Prohibit employee reviews** without complete and clear disclosure of employment relationship

4. **Verify all health claims** against FTC Health Products Compliance Guidance (Dec 2022)
   evidence standard — specifically RCT support for each claimed benefit

5. **Document the "Doctor-Formulated" claim** with named, credentialed professional and
   clear disclosure of any compensation

6. **Review environmental claims** against 16 CFR Part 260 (Green Guides)

7. **Implement review monitoring** to detect and address any inadvertent non-compliance

### Timeline Consideration

16 CFR Part 465 became effective October 21, 2024. VitaCore's launch in 2026 means
the full rule applies. Additionally, VitaCore received the FTC's Notice of Penalty
Offenses in April 2023, establishing that the company cannot claim lack of notice.

---

## Section 5: Verbatim Regulatory Text Quick Reference

For compliance staff reference, key verbatim provisions:

### 16 CFR §465.2(a) — Fake Reviews Prohibition
"It is an unfair or deceptive act or practice and a violation of this part for a business
to write, create, or sell a consumer review, consumer testimonial, or celebrity testimonial
that materially misrepresents, expressly or by implication:
(1) That the reviewer or testimonialist exists;
(2) That the reviewer or testimonialist used or otherwise had experience with the product,
service, or business; or
(3) The reviewer's or testimonialist's experience with the product, service, or business."

### 16 CFR §465.7 — Review Suppression by Threat
"It is an unfair or deceptive act or practice for a business (directly or through an agent)
to use, or to threaten to use, an unfounded or groundless legal threat, a physical threat,
intimidation, or a public false accusation (including public shaming) against any person
in an attempt to:
(1) Prevent a review or any portion thereof from being written or created, or
(2) Cause a review or any portion thereof to be removed."

### 16 CFR §255.5 — Material Connection Disclosure Trigger
"a connection between the endorser and the seller of the advertised product that might
materially affect the weight or credibility of the endorsement"

### FTC Health Products Guidance — Gold Standard
"randomized, controlled human clinical testing (RCT)"

### FTC Health Products Guidance — Prohibited Qualifiers
The following terms do not adequately hedge unsubstantiated health claims:
"may," "helps," "promising," "preliminary," "initial," "pilot"

---

*Prepared by VitaCore In-House Compliance Team | Reviewed by CCO Jordan Ellis*
*Reference Date: February 2026*
"""
    return output


def _gen_influencer_policy_doc() -> str:
    """Generate ~20KB influencer relationship policy document."""
    rng = random.Random(888)
    influencer_names = [
        ("@wellnesswithjenna", "Jenna Martinez", 45000, "Instagram", "Lifestyle/Wellness"),
        ("@guthealth_guru", "David Kim", 28000, "TikTok", "Health/Science"),
        ("@probiotic_life", "Sarah O'Brien", 15000, "Instagram", "Fitness"),
        ("@nourishednaturally", "Alex Thompson", 78000, "YouTube", "Nutrition"),
        ("@vitamindiary", "Chris Patel", 12000, "Instagram", "Wellness"),
        ("@microbiome_maven", "Lisa Chen", 95000, "TikTok", "Health Education"),
        ("@supplementspro", "Marcus Williams", 33000, "Instagram", "Fitness/Supplements"),
        ("@holistic_health_hub", "Rachel Davis", 22000, "Blog/Instagram", "Holistic Health"),
        ("@fitandfueled", "Jake Morrison", 56000, "YouTube", "Fitness/Nutrition"),
        ("@cleanwellness", "Emma Rodriguez", 18000, "Instagram", "Clean Living"),
        ("@digestive_digest", "Noah Johnson", 41000, "TikTok", "Gut Health"),
        ("@immunity_insider", "Olivia Brown", 67000, "Instagram/Blog", "Immunity/Health"),
        ("@nutriscience", "Aiden Lee", 24000, "YouTube", "Nutrition Science"),
        ("@vitalitycoach", "Sophia Garcia", 38000, "Instagram", "Wellness Coaching"),
    ]

    output = """# VitaCore Inc. — Influencer Relationship Management Policy

**Policy Number**: MKT-2026-003
**Effective Date**: March 1, 2026
**Approved by**: CCO Jordan Ellis, Marketing VP Mike Torres
**Purpose**: Compliance with 16 CFR Part 255 (Endorsement Guides) and 16 CFR Part 465
(Consumer Reviews and Testimonials Rule)

---

## Section 1: Policy Statement

VitaCore Inc. is committed to full compliance with FTC regulations governing endorsements,
testimonials, and influencer marketing. This policy establishes binding requirements for
all influencer relationships to ensure that the company's marketing practices do not
constitute deceptive acts or practices under Section 5 of the FTC Act.

This policy supersedes any prior informal guidance on influencer disclosure and review
solicitation practices.

---

## Section 2: Legal Framework

### Governing Regulations

1. **16 CFR Part 255** (Endorsement Guides, effective July 26, 2023):
   Requires disclosure of material connections between endorsers and advertisers.

2. **16 CFR Part 465** (Consumer Reviews and Testimonials Rule, effective October 21, 2024):
   Prohibits fake reviews, undisclosed insider reviews, and review suppression.

3. **FTC Health Products Compliance Guidance** (December 2022):
   Governs substantiation requirements for health claims made in endorsements.

4. **FTC .com Disclosures Guidance** (2013):
   Provides guidance on effective disclosure in digital advertising.

### Penalty Risk

Civil penalty exposure under 16 CFR Part 465: $51,744 per violation (2024 rate).
For 14 influencer relationships with inadequate disclosures across 3 posts each:
Potential exposure = 42 violations × $51,744 = $2,173,248.

---

## Section 3: Definitions

**Influencer**: Any individual who has an audience on social media or other digital
platforms and who promotes VitaCore products in exchange for compensation, free products,
discounts, affiliate commissions, or other benefits.

**Material Connection**: Any relationship between an influencer and VitaCore that might
affect the credibility of the influencer's statements, including:
- Monetary payment or compensation
- Free products or samples
- Discounted products
- Affiliate commissions
- Early access to products
- Event invitations
- Prize or contest entry

**Adequate Disclosure**: A disclosure that is "difficult to miss and be easily
understandable by ordinary consumers" per FTC standards.

---

## Section 4: Required Disclosure Language

### Primary Approved Disclosure Forms (Mandatory)

**Option 1 (Preferred)**:
"Ad: [Content begins here]" — The label "Ad:" must appear as the first word/phrase
before any promotional content.

**Option 2 (Acceptable)**:
"#ad" as the very first text element in the post (before any other content or hashtags).

**Option 3 (For Video Content)**:
Verbal statement within the first 10 seconds: "This video is sponsored by VitaCore.
I was paid/received free products to share my experience." PLUS on-screen text overlay
reading "Sponsored by VitaCore" throughout the promotional portion of the video.

### Prohibited Disclosure Forms (Non-Compliant)

The following disclosure methods do NOT satisfy FTC requirements and must NOT be used:

1. **Hashtag burial**: "#ad" placed at the end of or within a list of topic hashtags
   (e.g., "#health #wellness #supplements #vitacore #nutrition #fitness #ad")
   — INADEQUATE per FTC .com Disclosures Guidance.

2. **Platform tool reliance**: Relying solely on Instagram's "Paid Partnership" banner,
   TikTok's "Paid promotion" label, or similar built-in platform disclosure tools
   — INADEQUATE standing alone per 16 CFR §255.5.

3. **Profile bio disclosure**: Placing a disclosure only in the influencer's bio
   ("This account receives free products from brands")
   — INADEQUATE for individual post requirements.

4. **End-of-post disclosure**: Placing disclosure text at the bottom of a long post
   that requires scrolling to reach — INADEQUATE.

5. **Click-through disclosure**: Requiring the consumer to click a link to view the
   material connection — INADEQUATE for material disclosures.

---

## Section 5: Current Influencer Roster — Compliance Status

The following table documents VitaCore's 14 current influencer relationships and
their compliance status as of March 2026:

"""
    for handle, name, followers, platform, niche in influencer_names:
        comp_status = rng.choice(["NON-COMPLIANT", "NON-COMPLIANT", "COMPLIANT", "PENDING REVIEW"])
        payment_type = rng.choice(["Monthly retainer ($500)", "Per-post fee ($200)", "Free products only",
                                    "Affiliate commission (8%)", "Free products + fee ($150/post)"])
        disclosure_method = rng.choice([
            "#ad buried in hashtags (NON-COMPLIANT)",
            "Platform Paid Partnership label only (NON-COMPLIANT)",
            "Ad: at beginning of post (COMPLIANT)",
            "No disclosure currently (NON-COMPLIANT)",
            "Verbal disclosure in video (COMPLIANT)",
        ])
        output += f"""### {handle} ({name})

| Attribute | Detail |
|-----------|--------|
| **Platform** | {platform} |
| **Followers** | {followers:,} |
| **Content Niche** | {niche} |
| **Compensation** | {payment_type} |
| **Current Disclosure** | {disclosure_method} |
| **Compliance Status** | **{comp_status}** |
| **Action Required** | {"Update disclosure to 'Ad:' format before next post" if comp_status != "COMPLIANT" else "None — current disclosure is adequate"} |

"""

    output += """---

## Section 6: Compliance Procedures

### Pre-Post Review Process

1. All influencer content must be submitted to Casey Park (Social Media Manager)
   at least 48 hours before scheduled publication.

2. Casey Park will review each post for adequate disclosure per Section 4.

3. Any post lacking adequate disclosure must be returned to the influencer for
   revision. The influencer may not publish without compliance team sign-off.

4. CCO Jordan Ellis must approve any posts by influencers making health claims
   (including references to immune support, digestive health, or specific ingredients).

### Health Claim Restrictions

Influencers may NOT make the following statements without explicit approval:

**Prohibited language**:
- "This product cured/treats/prevents [condition]" — disease claim, not permitted for supplements
- "Clinically proven/demonstrated" — requires specific RCT citation
- "May help support" — prohibited qualifying language per FTC Health Products Guidance
- "Promising preliminary results" — two prohibited qualifiers
- "Doctor recommended" — requires named, credentialed physician with disclosed relationship

**Permitted language** (with proper substantiation on file):
- "Supports immune health" (for L. acidophilus NCFM component, RCT-supported)
- "Supports gut microbiome balance" (for L. acidophilus NCFM, RCT-supported)
- "Part of my immune support routine" (personal testimonial, own experience)
- "I take this daily as part of my wellness routine" (personal, non-efficacy claim)

### Documentation Requirements

For each influencer post, the following must be retained for 3 years:
1. Influencer agreement specifying compensation and disclosure requirements
2. Screenshot of published post with visible disclosure
3. Date/time of publication
4. Compliance review sign-off record

---

## Section 7: Employee Review Policy

### Prohibition on Undisclosed Insider Reviews

VitaCore Inc. prohibits any employee, officer, contractor, or their immediate family
members from submitting consumer reviews of VitaCore products without clearly and
conspicuously disclosing their relationship with the company.

This prohibition applies to:
- Amazon product listings
- Vitacore.com (company website)
- Third-party retail platforms (Walmart.com, iHerb, etc.)
- Social media platforms (Instagram, TikTok, Facebook, etc.)
- App stores (if VitaCore has associated digital products)

### Required Disclosure for Insider Reviews

If an employee submits a genuine review based on actual product experience, the review
must include the following disclosure in the review text itself (not just in the profile):

"[Disclosure: I am an employee of VitaCore Inc. This review reflects my personal
experience with the product and was submitted voluntarily.]"

### Prohibited Actions

The following actions are explicitly prohibited and constitute violations of
16 CFR §465.3 and this policy:

1. Directing employees to post reviews without disclosure (violates §465.3)
2. Incentivizing employees to post positive reviews (violates §465.3 and potentially §465.2)
3. Creating fake consumer personas using company resources (violates §465.2)
4. Asking employees to post on behalf of fictional customers (violates §465.2)

### Disciplinary Consequences

Violations of this policy may result in disciplinary action up to and including
termination, and may expose VitaCore to civil penalties of $51,744 per violation.

---

## Section 8: Review Suppression Prohibition

### Prohibition on Review Suppression

VitaCore may NOT suppress, hide, or fail to display genuine consumer reviews for
any reason other than the following permitted grounds:

**Permitted grounds for review removal**:
- Review contains fake or fabricated content (§465.2 violation)
- Review contains irrelevant content (not related to the product)
- Review contains inappropriate content (obscenity, personal attacks)
- Review violates platform terms of service

**Prohibited grounds for review removal**:
- Review is negative (1-3 star ratings cannot be selectively suppressed)
- Review mentions a competitor product
- Review includes product criticism that is accurate but unflattering
- Review was submitted by an unsatisfied customer who did not receive compensation

### Prohibition on Legal Threats

VitaCore may NOT use legal threats, cease-and-desist letters, or intimidation tactics
to prevent or remove genuine consumer reviews, per 16 CFR §465.7.

Any negative review situation should be addressed by:
1. Contacting the reviewer directly (if possible) to understand their concern
2. Addressing the underlying product or service issue
3. Offering a replacement or refund through appropriate channels
4. Responding publicly to the review in a professional manner

---

*Policy Owner: Jordan Ellis, CCO*
*Next Review Date: March 1, 2027*
*Document Version: 2.1*
"""
    return output


def _gen_ad_tv_script() -> str:
    """Generate ~12KB TV/video ad script for review."""
    return """# ProBio+ Daily — Television and Video Advertisement Scripts

**Version**: Draft for Compliance Review
**Reviewed by**: Casey Park (Social Media), Mike Torres (Marketing)
**Pending approval by**: Jordan Ellis (CCO), Sarah Chen (In-House Counsel)

---

## Script 1: 30-Second Television Spot ("The Morning Routine")

### PRODUCTION VERSION (Pre-Compliance Review)

**[SCENE: Bright kitchen, morning light. Woman (35-45) prepares breakfast.]**

NARRATOR (V.O.):
"Starting your day right means supporting your immune health from the inside out."

**[SCENE: Close-up of ProBio+ Daily bottle on counter.]**

NARRATOR (V.O.):
"ProBio+ Daily may help support your immune function with a proprietary blend backed
by promising preliminary science."

**[SCENE: Woman takes capsules, smiles.]**

WOMAN (ON CAMERA):
"Since I started taking ProBio+ Daily, I have never felt better. My gut health
has completely transformed. And my doctor said this is the best formula she's seen!"

**[SCENE: Product shot with bottle rotating.]**

NARRATOR (V.O.):
"ProBio+ Daily — clinically demonstrated support for the immune system you deserve."

**SUPER**: "Results not typical. Individual results may vary."
**SUPER**: "*These statements have not been evaluated by the FDA. Not intended to diagnose,
treat, cure, or prevent any disease."

---

### COMPLIANCE REVIEW ANNOTATIONS

**[ANNOTATED BY SARAH CHEN, 2026-03-05]**

VIOLATION 1 (HIGH): "may help support" — PROHIBITED qualifying language per FTC Health
Products Compliance Guidance (Dec 2022). This phrasing does not make the claim compliant.
→ REPLACE WITH: "supports immune health" (if substantiated) or remove.

VIOLATION 2 (HIGH): "promising preliminary science" — DOUBLE VIOLATION. Both "promising"
and "preliminary" are prohibited qualifying terms per FTC Health Products Guidance.
→ REMOVE: Cannot hedge unsubstantiated claim with these terms.

VIOLATION 3 (HIGH): "My doctor said this is the best formula she's seen!" —
(a) If doctor is compensated, material connection must be disclosed.
(b) "Best formula" implies comparative efficacy claim requiring substantiation.
(c) Doctor's name and credentials must be identified per §255.3.
→ REMOVE until doctor is identified and relationship disclosed.

VIOLATION 4 (CRITICAL): "clinically demonstrated support for the immune system" —
"Clinically demonstrated" implies RCT-level evidence for the specific claim. B. longum
digestive wellness claim lacks RCT support. If this refers to the full formula (including
B. longum), this claim is unsupported.
→ REMOVE "clinically demonstrated" language. See CEO retraction CEO-RETRACT-20260312-01.

VIOLATION 5 (MEDIUM): "Results not typical. Individual results may vary." —
This disclaimer does NOT provide safe harbor per current FTC rules. The 2009 revision
abolished the "Results Not Typical" safe harbor. The disclaimer must be replaced with
disclosure of what results consumers should generally expect.
→ REPLACE WITH: Statement of typical results based on RCT data, or remove testimonial.

---

### COMPLIANT REVISION (Draft)

**[SCENE: Bright kitchen, morning light. Woman (35-45) prepares breakfast.]**

NARRATOR (V.O.):
"Starting your day right means supporting your immune health from the inside out."

**[SCENE: Close-up of ProBio+ Daily bottle on counter.]**

NARRATOR (V.O.):
"ProBio+ Daily supports immune health with clinically studied Lactobacillus acidophilus NCFM
combined with Vitamin D3, Vitamin C, and Zinc — four key ingredients with published
human clinical trial evidence for immune support."

**[SCENE: Woman takes capsules, smiles.]**

NARRATOR (V.O.):
"Real science. Real ingredients. Real immune support."

**[SCENE: Product shot with bottle rotating.]**

NARRATOR (V.O.):
"ProBio+ Daily — immune health support you can trust."

**SUPER**: "Ad | [Influencer Name] received ProBio+ Daily as part of a paid partnership."
(NOTE: Only appears if woman is a paid influencer. If actress, no disclosure needed
unless she represents genuine consumer experience.)

**SUPER**: "*These statements have not been evaluated by the FDA. Not intended to diagnose,
treat, cure, or prevent any disease."

---

## Script 2: 60-Second YouTube Pre-Roll Ad ("The Science")

### PRODUCTION VERSION (Pre-Compliance Review)

**[SCENE: Laboratory setting. Male in lab coat (40s) looks at papers.]**

DR. (ON CAMERA):
"Hi, I'm Dr. Johnson, and as a nutritional medicine specialist, I can tell you that
ProBio+ Daily represents a breakthrough in immune health supplementation. The science
behind this formula is some of the most exciting I've seen in my career."

NARRATOR (V.O.):
"ProBio+ Daily combines 15 billion CFU of clinically tested probiotic strains with
essential vitamins and minerals for comprehensive immune support."

**[SCENE: Animated graphic of gut with probiotics.]**

NARRATOR (V.O.):
"Our proprietary blend has shown initial promising results in helping your body build
stronger immune defenses naturally."

**[SCENE: Dr. holding bottle.]**

DR. (ON CAMERA):
"I recommend ProBio+ Daily to my patients because it delivers everything needed for
complete gut and immune health in a single daily supplement."

**[SCENE: Customer testimonials (5 different people)]**

TESTIMONIAL 1: "I lost 10 pounds and my immune system is incredible now!"
TESTIMONIAL 2: "My chronic gut issues are completely gone after just 2 weeks!"
TESTIMONIAL 3: "I haven't gotten sick once since starting ProBio+ Daily!"
TESTIMONIAL 4: "My energy is through the roof — I feel 20 years younger!"
TESTIMONIAL 5: "This cured my digestive problems when nothing else worked!"

---

### COMPLIANCE REVIEW ANNOTATIONS

**[ANNOTATED BY JORDAN ELLIS, CCO, 2026-03-06]**

VIOLATION 1 (CRITICAL): Dr. "Johnson" — Who is this person?
- Name not verified in our system. We have no physician named "Dr. Johnson" on staff.
- Is this a paid actor? If so, this is a FABRICATED EXPERT ENDORSEMENT — VIOLATION OF §255.3.
- If a real physician, a signed agreement and material connection disclosure required.
→ IDENTIFY: Determine if this is an actor (remove "doctor" framing) or real physician
  (obtain agreement, disclose relationship, verify credentials).

VIOLATION 2 (HIGH): "initial promising results" — DOUBLE PROHIBITED QUALIFIER.
Both "initial" and "promising" are prohibited qualifying terms.
→ REMOVE.

VIOLATION 3 (HIGH): "I recommend ProBio+ Daily to my patients" — Medical recommendation
claim that (a) implies the product is medically appropriate for all patients, and
(b) creates an implicit disease-treatment claim. Only substantiated with named physician
and disclosed relationship.
→ HOLD until compliance issue #1 resolved.

VIOLATION 4 (CRITICAL): All five testimonials are problematic.
- Testimonial 1: Weight loss claim — ProBio+ Daily is NOT substantiated for weight loss.
  This is a false/unsupported claim per §255.2 and Health Products Guidance.
- Testimonial 2: "Chronic gut issues completely gone" — disease treatment claim.
  Dietary supplements may NOT claim to treat, cure, or diagnose conditions.
- Testimonial 3: "Haven't gotten sick" — implies disease prevention.
  Not a permitted structure supplement claim without RCT for this specific outcome.
- Testimonial 4: "Feel 20 years younger" — anti-aging claim not substantiated.
- Testimonial 5: "Cured my digestive problems" — DISEASE CURE CLAIM. Strictly prohibited.
→ ALL FIVE testimonials must be replaced or substantially modified.

VIOLATION 5 (MEDIUM): No disclosure for testimonials — Are these real customers?
Paid actors? Were they compensated?
- If paid actors, must not be presented as real consumer testimonials.
- If real customers who received free products, material connection must be disclosed.
- Each testimonial requires individual assessment.

---

## Script 3: Influencer Script Template (Casey Park's 14 Partners)

### CURRENT TEMPLATE (Non-Compliant — Per Compliance Review)

**[Post text distributed to all 14 influencer partners by Casey Park, 2026-02-15]:**

"I've been taking ProBio+ Daily for the past month and I absolutely love it! 🌟
My gut health is so much better and I have way more energy now. If you want to try
the supplement that has actually made a difference for me, use my code [INFLUENCER_CODE]
for 15% off. My link in bio!

#health #wellness #probiotics #guthealth #immunesupport #supplements #vitacore
#vitalife #microbiome #nutrition #fitnessmotivation #healthylifestyle #ad"

---

### COMPLIANCE REVIEW FINDINGS

**[Reviewed by Jordan Ellis, CCO, 2026-03-07]**

PROBLEM 1 (CRITICAL): "#ad" appears as the LAST hashtag after 12 topic hashtags.
This is the "buried hashtag" pattern specifically identified as INADEQUATE by the FTC.
→ MOVE "#ad" to the very beginning of the post.

PROBLEM 2 (MEDIUM): "has actually made a difference" — this language implies efficacy.
If not substantiated for this influencer's specific experience, this may misrepresent
their experience per §465.2(a)(3).
→ QUALIFY or remove — influencers should describe their experience accurately.

PROBLEM 3 (LOW): The script is provided to all 14 influencers with identical text.
Multiple endorsers using the same scripted language may appear to be independent
reviews, but they all reflect a company-authored script.
→ ENCOURAGE individual voice while maintaining disclosure requirements.

---

### COMPLIANT REVISED TEMPLATE

**Mandatory preamble (must appear as first text in post):**
"Ad: VitaCore sponsored this post and I received ProBio+ Daily for free to try and share my thoughts."

**Suggested body (influencer should personalize):**
"I've been incorporating ProBio+ Daily into my morning routine for the past [X weeks/months].
[Personal experience description — must be accurate to influencer's actual experience].

The formula includes [ingredients they found interesting]. [Personal opinion — genuine assessment].

If you'd like to try it, use my code [INFLUENCER_CODE] for 15% off. Link in bio."

**Required hashtag placement:**
"#ad" (if not in preamble) followed by relevant topic hashtags.

**Health claim restrictions (for influencer awareness):**
- Do NOT claim the product cures or treats any condition
- Do NOT claim "may help" or "promising results"
- Limit claims to personal experience and FTC-cleared language
- Do NOT reference clinical studies unless cleared by VitaCore compliance team

---

## Document Control

| Version | Date | Changes | Reviewer |
|---------|------|---------|----------|
| 1.0 | 2026-02-15 | Initial distribution to influencer partners | Casey Park |
| 2.0 | 2026-03-06 | Compliance review annotations added | Jordan Ellis (CCO) |
| 2.1 | 2026-03-07 | Compliant revised template drafted | Sarah Chen (Counsel) |
| 3.0 (pending) | TBD | Final version pending all approvals | All |

*This document is CONFIDENTIAL — VitaCore Inc. internal use only*
"""


def _gen_compliance_faq() -> str:
    """Generate ~80KB compliance FAQ and training manual combining all FTC regulations."""
    qa_pairs = [
        ("What is the civil penalty for a fake consumer review under 16 CFR Part 465?",
         "The civil penalty is $51,744 per violation (2024 base rate). This rate is indexed to the Consumer Price Index and was adjusted to $53,088 in February 2025. For ProBio+ Daily's compliance analysis, the 2024 rate of $51,744 governs. Note: Some informal summaries (including the DECOY summary document) incorrectly state $45,000 — that figure is wrong. Always verify against 16 CFR Part 465 primary text."),
        ("When did 16 CFR Part 465 (Consumer Reviews and Testimonials Rule) become effective?",
         "16 CFR Part 465 became effective October 21, 2024. Prior to this date, the FTC's case-by-case enforcement under Section 5 of the FTC Act applied to fake review practices. The rule codified and made explicit what had already been prosecuted as deceptive practices. Companies that received the FTC's Notice of Penalty Offenses (approximately 670 companies in April 2023) cannot claim lack of notice that these practices were illegal."),
        ("What does §465.2(a) prohibit?",
         "Section 465.2(a) prohibits a business from writing, creating, or selling a consumer review, consumer testimonial, or celebrity testimonial that materially misrepresents, expressly or by implication: (1) That the reviewer or testimonialist exists; (2) That the reviewer or testimonialist used or otherwise had experience with the product, service, or business; or (3) The reviewer's or testimonialist's experience with the product, service, or business. This verbatim text is a ground-truth anchor for compliance analysis."),
        ("What is §465.7's prohibition on review suppression?",
         "Section 465.7 prohibits using an unfounded or groundless legal threat, a physical threat, intimidation, or a public false accusation (including public shaming) against any person in an attempt to: (1) Prevent a review or any portion thereof from being written or created, or (2) Cause a review or any portion thereof to be removed. This means cease-and-desist letters sent to discourage negative reviewers without a valid legal basis are prohibited."),
        ("When did 16 CFR Part 255 (Endorsement Guides) become effective in its 2023 revision?",
         "The 2023 revision to 16 CFR Part 255 became effective July 26, 2023. The previous version was revised in 2009. The 2023 revision extended coverage to virtual influencers, AI-generated content, and explicitly addressed new platforms and disclosure formats. The effective date of July 26, 2023 is a ground-truth anchor that must appear correctly in any compliance timeline."),
        ("What is the §255.5 material connection disclosure standard?",
         "Per §255.5, when there exists 'a connection between the endorser and the seller of the advertised product that might materially affect the weight or credibility of the endorsement,' that connection must be fully disclosed. This is the verbatim regulatory trigger for the disclosure requirement. Material connections include monetary payment, free products, discounts, affiliate commissions, early access, and family relationships with company personnel."),
        ("Is '#ad' buried among hashtags an adequate disclosure?",
         "No. The FTC's .com Disclosures Guidance and §255.5 require that disclosures be 'difficult to miss and be easily understandable by ordinary consumers.' When '#ad' appears as the last hashtag after 12-15 topic hashtags (e.g., '#probiotic #health #wellness #supplements #fitness #vitacore #ad'), it does not meet this standard. The '#ad' label must appear at the beginning of the post, before any promotional content, to constitute an adequate disclosure."),
        ("Is relying solely on Instagram's 'Paid Partnership' feature adequate?",
         "No. The FTC's 2023 Endorsement Guides explicitly address this: relying solely on a platform's built-in 'Paid Partnership' or similar labeling tool is insufficient as a standalone disclosure. Studies show many consumers do not notice or understand these platform-specific labels. The endorser must include an independent, clear disclosure — typically '#ad' or 'Ad:' at the beginning of the post."),
        ("What is the FTC's gold standard for health claims?",
         "Per the FTC's Health Products Compliance Guidance (December 2022), the gold standard for health-related advertising claims is 'randomized, controlled human clinical testing (RCT).' A qualifying RCT must include a control group, randomization, double blinding (where applicable), and produce statistically significant AND clinically meaningful results. Animal studies, in vitro studies, and consumer surveys cannot standalone substantiate health claims."),
        ("Can 'may help support' or 'promising' be used to qualify health claims?",
         "No. The FTC Health Products Compliance Guidance (December 2022) explicitly identifies the following as prohibited qualifying terms that do not adequately hedge an unsubstantiated health claim: 'may,' 'helps,' 'promising,' 'preliminary,' 'initial,' and 'pilot.' Using these terms does not transform an unsubstantiated claim into a compliant one. The claim still requires adequate scientific evidence regardless of these qualifiers."),
        ("Is 'Results Not Typical' still a safe harbor for testimonials?",
         "No. The 'Results Not Typical' disclaimer was a safe harbor under the original 1980 Endorsement Guides. It was definitively abolished in the 2009 revision. This abolition was reaffirmed in the 2023 revision. Currently, advertisers must prove that the endorsed results represent what consumers generally achieve, or disclose the typical results separately. This is a critical compliance trap — old-format testimonials still using 'Results Not Typical' are non-compliant."),
        ("What are the FTC's six Pfizer factors for 'reasonable basis'?",
         "From In re Pfizer Inc., 81 F.T.C. 23 (1972), the six factors are: (1) the type of product; (2) the type of claim; (3) the benefits of a truthful claim; (4) the cost of developing substantiation; (5) the consequences of a false claim; (6) the amount of substantiation experts in the field believe is reasonable. For health products, these factors typically require RCT-level evidence."),
        ("What is the 'all or virtually all' standard for Made in USA claims?",
         "Under 16 CFR Part 323, an unqualified 'Made in USA' claim requires that all significant processing occur in the United States, all or virtually all ingredients or components be of U.S. origin, and final assembly occur in the United States. The largest penalty for violation of this rule was $2 million imposed on Kubota North America Corporation in January 2024."),
        ("What is the §260.8 biodegradable claim standard?",
         "Under 16 CFR §260.8, a biodegradable claim requires that the product completely break down within a reasonably short period after customary disposal. The FTC considers one year after customary disposal to be the standard timeframe. Unqualified biodegradable claims for products typically disposed of in landfills or incinerators are deceptive because these items do not biodegrade within one year under these conditions. An independent laboratory test report is required to substantiate the claim."),
        ("What is the §260.12 recyclable claim standard?",
         "Under 16 CFR §260.12, an unqualified 'recyclable' claim requires that recycling facilities be available to a 'substantial majority' of consumers. The FTC defines 'substantial majority' as 60% of consumers or communities where the product is sold having access to recycling facilities for the relevant material. If recycling facilities are not available to at least 60% of consumers, the recyclable claim must be qualified to explain the limited availability."),
        ("What constitutes an 'insider' under §465.3?",
         "Under §465.3 and related definitions in 16 CFR Part 465, an 'insider' includes officers, managers, employees, agents of a company, and the immediate family members or household members of such persons. Any review by an insider must clearly and conspicuously disclose the insider's material connection to the business in or adjacent to the review itself. Company-wide solicitations for employee reviews without disclosure instructions violate this provision."),
        ("How does §465.6 govern review display practices?",
         "Section 465.6 prohibits suppressing or withholding consumer reviews in a discriminatory manner — specifically, displaying only positive reviews while suppressing or withholding negative reviews. A business may remove reviews that are fake or false (§465.2), contain irrelevant content, or contain inappropriate content. However, selectively filtering to show only 4-5 star reviews while hiding 1-3 star reviews violates §465.6."),
        ("What are the notice of penalty offenses five categories?",
         "The FTC's 2023 Notice of Penalty Offenses (sent to approximately 670 companies) identifies five categories: (1) lacking competent and reliable evidence supporting product claims; (2) missing scientific evidence for health or safety claims; (3) inadequate clinical trial for disease treatment claims (at least one well-controlled RCT required); (4) misrepresentation of the level or type of substantiation; (5) false proof claims (claiming 'scientifically proven' or 'clinically proven' without sufficient evidence)."),
        ("What documentation is required for a 'Doctor-Formulated' claim?",
         "A 'Doctor-Formulated' claim triggers §255.3 (Expert Endorsements) analysis. The claim requires: (1) the specific credentialed professional(s) must be identified by name; (2) their professional credentials must be verified and relevant to the product category; (3) any material connection (payment, equity, employment) must be disclosed; (4) the professional's endorsement scope must be accurate — they cannot endorse claims that exceed the evidence base; (5) per the revised audit opinion (email_revised_audit_v2), the underlying health claims must be substantiated by RCT-level evidence."),
        ("What is the FTC's Health Products Compliance Guidance (Dec 2022) replacing?",
         "The December 2022 Health Products Compliance Guidance replaces the 1998 publication 'Dietary Supplements: An Advertising Guide for Industry.' The 2022 guidance updated the substantiation standards to reflect modern clinical trial methodology and FTC enforcement priorities. References to the 1998 guide in current marketing materials represent reliance on superseded guidance."),
        ("Can a dietary supplement claim to 'cure' or 'treat' a disease?",
         "No. Dietary supplements may NOT claim to diagnose, treat, cure, or prevent any disease. Such claims transform the supplement into a drug under FDA regulations and additionally violate FTC advertising standards if the claims are not substantiated by the evidence required for pharmaceutical drugs. Health claims for supplements must be limited to structure/function claims (e.g., 'supports immune health') that are substantiated by adequate clinical evidence."),
        ("What disclosure is required for affiliate marketing links?",
         "Affiliate marketing arrangements — where an influencer earns a commission on sales through a trackable link or code — constitute a material connection per §255.5. The commission arrangement must be disclosed in the same post where the affiliate link appears, using language that is clear and conspicuous to ordinary consumers. A general statement in the influencer's bio is not sufficient for individual posts."),
        ("How does the 'clear and conspicuous' standard apply to video content?",
         "For video content, the FTC recommends both audible disclosure (spoken at the beginning of the video) and visible on-screen text disclosure (appearing during the promotional portion of the video). An audio-only disclosure that consumers might miss while watching, or a visual text disclosure that is too small or brief to read, does not meet the 'difficult to miss and easily understandable' standard. Both formats working together are the best practice."),
        ("What types of social media indicators constitute violations under §465.8?",
         "Section 465.8 prohibits buying, selling, or creating fake social media indicators that misrepresent the popularity or consumer acceptance of a product. This includes purchased Instagram likes, purchased YouTube views, purchased Facebook followers, TikTok engagement bots, and Reddit upvote manipulation. These practices are prohibited when the accounts generating the metrics do not represent genuine consumers."),
        ("Can a company ask satisfied customers to leave reviews without disclosure?",
         "A company may ASK satisfied customers to leave honest reviews, provided: (1) no compensation or incentive is offered that would create a material connection; (2) the request is made without conditions (e.g., not contingent on a positive review); (3) the process does not facilitate selection of only satisfied customers (which could constitute review manipulation under §465.6). If compensation is offered (discount code, entry into a sweepstake), that material connection must be disclosed in the review."),
    ]

    output = """# VitaCore ProBio+ Daily — FTC Compliance FAQ and Training Manual

**Prepared by**: CCO Jordan Ellis and In-House Counsel Sarah Chen
**Date**: March 2026
**Purpose**: Comprehensive reference guide for VitaCore marketing and compliance teams

---

## Introduction

This FAQ addresses the most common questions from VitaCore's marketing, legal, and
management teams regarding FTC regulations applicable to ProBio+ Daily's launch.
All answers reference primary regulatory sources — not secondary summaries or informal
communications. Where a secondary source (such as the external_audit_summary_DECOY.md
document) conflicts with the primary regulatory text, the primary regulatory text controls.

**Key regulatory documents referenced:**
- 16 CFR Part 465 (Consumer Reviews and Testimonials Rule, eff. Oct 21, 2024)
- 16 CFR Part 255 (Endorsement Guides, eff. July 26, 2023)
- FTC Health Products Compliance Guidance (December 2022)
- FTC .com Disclosures Guidance (2013)
- 16 CFR Part 260 (Green Guides)
- 16 CFR Part 323 (Made in USA Labeling Rule)

---

## Part 1: Consumer Review Compliance (16 CFR Part 465)

"""
    for i, (q, a) in enumerate(qa_pairs[:12], 1):
        output += f"### Q{i}: {q}\n\n**Answer**: {a}\n\n---\n\n"

    output += """## Part 2: Endorsement and Disclosure Compliance (16 CFR Part 255)

"""
    for i, (q, a) in enumerate(qa_pairs[12:20], 13):
        output += f"### Q{i}: {q}\n\n**Answer**: {a}\n\n---\n\n"

    output += """## Part 3: Health Claims and Substantiation

"""
    for i, (q, a) in enumerate(qa_pairs[20:], 21):
        output += f"### Q{i}: {q}\n\n**Answer**: {a}\n\n---\n\n"

    # Add a large training section
    output += """## Part 4: Comprehensive Compliance Training Scenarios

### Scenario 1: Employee Review Request

**Situation**: Marketing VP Mike Torres sends an email to all 150 VitaCore employees
saying: "As part of our launch strategy, please leave a 5-star review for ProBio+ Daily
on Amazon this week. Use your personal account (not your VitaCore account) so it looks
more authentic. Just share your genuine opinion — we trust our team to be positive!"

**Analysis**:
This scenario contains multiple FTC violations:

*Violation 1 (§465.3 — Insider Reviews)*:
Directing employees to post reviews without requiring disclosure of their employment
relationship violates §465.3. The instruction to use "personal" accounts explicitly
to make the reviews "look more authentic" compounds this into potential §465.2(a)(1)
and (a)(2) violations — the reviews would misrepresent the independence of the reviewer.

*Violation 2 (§465.2(a)(3))*:
Instructing employees to "be positive" creates an incentive structure that may cause
reviews to misrepresent the reviewers' actual experiences.

*Recommended Action*:
- Immediately rescind the email.
- Issue a corrective communication prohibiting undisclosed employee reviews.
- If employees wish to leave reviews voluntarily, they must include clear disclosure:
  "[Disclosure: I am a VitaCore employee. This review reflects my personal experience.]"
- Document the rescission and corrective action in compliance records.

*Estimated Penalty Exposure* (if 50 employees post before interception):
50 violations × $51,744 = $2,587,200

---

### Scenario 2: Influencer Template Review

**Situation**: Casey Park distributes the following template to all 14 influencer partners:

"Been loving ProBio+ Daily lately! 💪 My gut feels SO much better and my immune system
is thriving. Use code CASEY15 for 15% off! #probiotic #health #immunehealth #wellness
#guthealth #supplements #nutrition #vitacore #fitfam #goals #selfcare #productreview
#ad #probiotics #immunesupport"

**Analysis**:
*Problem 1 (§255.5 — Material Connection Disclosure)*:
The "#ad" label appears as the 13th hashtag in a 15-hashtag list. This is the classic
"buried hashtag" pattern identified by the FTC as inadequate. The "#ad" must appear at
the beginning of the post to constitute an adequate disclosure.

*Problem 2 (§255.2 — Consumer Endorsement Substantiation)*:
"My immune system is thriving" is an efficacy claim. If this represents a typical result,
it must be substantiated. If it represents only this influencer's experience (which may
be atypical), the post must disclose what results consumers generally achieve.

*Problem 3 (Identical scripting risk)*:
If all 14 influencers post essentially the same content, this may make the endorsements
appear inorganic. The FTC has noted that company-scripted testimonials require closer
scrutiny.

*Recommended Fix*:
- Move "#ad" to the very first position (before any other text).
- Example compliant opening: "Ad: VitaCore sponsored this post and I received ProBio+
  Daily for free to share my experience."
- Allow influencers to personalize the body text.
- Add disclosure of specific compensation (free product, affiliate code).

*Estimated Penalty Exposure per influencer* (if posted as-is):
Each inadequate post = 1 violation × $51,744 = $51,744
14 influencers posting 3 times each = 42 violations = $2,173,248

---

### Scenario 3: Health Claim Review

**Situation**: The press release draft v1 contains the following sentences:
(a) "ProBio+ Daily may help support immune function with promising preliminary research."
(b) "Clinically demonstrated to enhance digestive wellness."
(c) "Doctor-formulated by leading health professionals."

**Analysis**:
*Sentence (a)*:
Three violations of FTC Health Products Compliance Guidance:
1. "may help" = prohibited qualifying language
2. "promising" = prohibited qualifying language
3. "preliminary" = prohibited qualifying language
All three terms appear in the FTC's explicit list of prohibited qualifiers that fail
to adequately hedge unsubstantiated health claims.

*Sentence (b)*:
"Clinically demonstrated" implies RCT-level evidence for the specific claim of
"enhancing digestive wellness." The ProBio+ Daily formula includes B. longum, for which
the only available evidence is in vitro and animal studies. These do NOT constitute
"clinically demonstrated" evidence per FTC standards. This claim is unsupported for
B. longum-related digestive claims.

*Sentence (c)*:
"Doctor-formulated" triggers §255.3 (Expert Endorsements):
1. The specific professional(s) must be identified by name and credentials.
2. Any material connection (employment, payment) must be disclosed.
3. The claim implies endorsement of the product's health efficacy, requiring substantiation.
Per the revised external audit letter (email_revised_audit_v2, update_source must be
this value), this claim requires "substantial competent scientific evidence" and
identification of the specific professional.

*Required Actions*:
- Remove or replace (a): "Supports immune health" (substantiated by L. acidophilus NCFM RCTs)
- Remove (b): No equivalent compliant replacement available until B. longum RCT completed.
- Qualify (c): "Formulated by Dr. Priya Nair, PhD, Nutrition Science, VitaCore R&D Director"
  with disclosure if there is employment compensation.

---

### Scenario 4: Review Management Decision

**Situation**: VitaCore's Amazon product page has 847 reviews: 523 five-star, 201 four-star,
85 three-star, 31 two-star, and 7 one-star. The Amazon backend shows that 12 of the
1-star reviews contain the phrase "doesn't work," and the Marketing VP wants to remove them
because they're "hurting conversion."

**Analysis**:
*Permitted removal grounds (§465.6(b))*:
- Reviews that are fake or false (§465.2 violations)
- Reviews containing irrelevant content
- Reviews containing inappropriate content (obscenity, personal attacks)

*Prohibited removal grounds (§465.6)*:
- Reviews are negative (low star rating)
- Reviews criticize the product's efficacy in a way that hurts sales
- "Doesn't work" is a genuine consumer experience statement

The proposed removal of 1-star reviews simply because they contain negative sentiment
about product efficacy violates §465.6. The Marketing VP's rationale ("hurting conversion")
is explicitly the type of discriminatory basis prohibited by the rule.

*Required Action*:
- Do not remove the 1-star reviews.
- VitaCore may respond to them professionally on the platform.
- If any specific reviews can be shown to be fake (§465.2), document the evidence
  and follow platform's dispute resolution process.
- If the reviews reveal legitimate product issues, address the issues.

*Estimated Penalty Exposure*: Each improperly removed review = 1 violation × $51,744

---

### Scenario 5: External Audit Letter Conflict

**Situation**: The first external audit letter (email_external_audit.eml) from Compliance
Counsel LLC recommended: (1) using 'Results Not Typical' disclaimers for testimonials;
(2) conditionally permitting the 'Doctor-Formulated' claim with named credentials.

A revised letter (email_revised_audit_v2.eml) was later received:
(1) Did not address 'Results Not Typical' (implicitly sustained by Update 1 Slack confirmation).
(2) Revoked the conditional permit for 'Doctor-Formulated,' now requiring evidence per
    the revised standard.

**Question**: Which letter controls?

**Analysis**:
*Regarding 'Results Not Typical' recommendation (from first letter)*:
The first letter's recommendation to use 'Results Not Typical' is based on pre-2009
Endorsement Guides. The safe harbor was abolished in the 2009 revision (Sarah Chen's
Update 1 message confirms this). This recommendation represents superseded law and must
be categorized as a superseded_recommendation — do NOT follow it.

*Regarding 'Doctor-Formulated' (from both letters)*:
The revised letter (email_revised_audit_v2.eml) explicitly SUPERSEDES the first letter's
conditional permit. The update_source for compliance records must be recorded as
"email_revised_audit_v2" (exact string). The Doctor-Formulated claim now requires
requires_substantiation: true pending a qualifying RCT for B. longum.

*Rule*: Later communications supersede earlier ones where they directly address the
same subject. A compliance analysis must always identify the most recent authoritative
instruction on each topic.

---

### Scenario 6: SHA-256 Sign-Off

**Situation**: Jordan Ellis requests that the final press release file be cryptographically
signed off to confirm the compliance-reviewed version is the one released.

**Process**:
1. Produce the final press release at the specified path in the `final/` directory.
   Per P5, the filename must follow: `{document_type}_final_YYYYMMDD.{ext}`
   Example: `press_release_final_20260309.md`

2. Compute the SHA-256 hash of the exact bytes of the file:
   ```bash
   sha256sum final/press_release_final_20260309.md
   ```

3. Write the result to the sign-off file:
   ```
   VERIFIED:<64-hex-characters>:<filename>
   ```
   The hash must be computed from the actual file — a placeholder or estimated hash
   will not match when the validator recomputes it.

4. The validator will independently recompute sha256sum of the final press release file
   and compare it to the hash in the sign-off file.

This process ensures that the compliance-reviewed file is identical to the one that
will be published.

---

## Part 5: Quick Reference Cards

### Card A: Prohibited Terms (A11 — FTC Health Products Guidance)

| Term | Why Prohibited | FTC Authority |
|------|---------------|---------------|
| "may" | Insufficient qualifier for unsubstantiated claim | Health Products Guidance 2022 |
| "helps" | Insufficient qualifier for unsubstantiated claim | Health Products Guidance 2022 |
| "promising" | Cannot hedge claim with non-definitive descriptor | Health Products Guidance 2022 |
| "preliminary" | Signals insufficient evidence — admission against interest | Health Products Guidance 2022 |
| "initial" | Same as preliminary | Health Products Guidance 2022 |
| "pilot" | Pilot studies are insufficient for health claims | Health Products Guidance 2022 |

### Card B: Disclosure Formats

| Format | Adequate? | Where to Use |
|--------|-----------|-------------|
| "Ad:" at post beginning | YES | All platforms |
| "#ad" as first hashtag | YES | Social media |
| "#ad" buried in hashtag list | NO | — |
| Platform "Paid Partnership" label only | NO | — |
| "#sponsored" at post end | NO | — |
| Verbal disclosure in first 10 seconds (video) | YES | Video platforms |
| Profile bio disclosure | NO | — |

### Card C: Key Dates

| Date | Event |
|------|-------|
| July 26, 2023 | 16 CFR Part 255 (2023 revision) effective |
| October 21, 2024 | 16 CFR Part 465 effective |
| April 2023 | FTC Notice of Penalty Offenses sent to ~670 companies |
| December 2022 | FTC Health Products Compliance Guidance published |
| February 2025 | Civil penalty adjusted to $53,088 per violation |
| January 2024 | Kubota $2M Made in USA penalty |

### Card D: Civil Penalty Quick Calculator

| Violation | Per-Violation Rate | Example |
|-----------|-------------------|---------|
| Fake review | $51,744 | 10 fake reviews = $517,440 |
| Insider review without disclosure | $51,744 | 40 employees = $2,069,760 |
| Influencer non-disclosure | $51,744 | 14 influencers × 3 posts = $2,173,248 |
| Review suppression | $51,744 | Depends on count |

---

*Document Version: 1.0 | Date: March 2026 | Classification: Internal/Confidential*
*Authors: Jordan Ellis (CCO), Sarah Chen (In-House Counsel)*
*Next Review: March 2027*
"""
    return output


def _gen_influencer_audit_log() -> str:
    """Generate ~60KB influencer post audit log CSV."""
    rng = random.Random(9999)
    handles = [
        "@wellnesswithjenna", "@guthealth_guru", "@probiotic_life", "@nourishednaturally",
        "@vitamindiary", "@microbiome_maven", "@supplementspro", "@holistic_health_hub",
        "@fitandfueled", "@cleanwellness", "@digestive_digest", "@immunity_insider",
        "@nutriscience", "@vitalitycoach",
    ]
    platforms = ["Instagram", "TikTok", "YouTube", "Instagram Stories", "Reels"]
    disclosure_patterns = [
        "#ad buried as last hashtag", "No disclosure", "#ad at post beginning",
        "Platform Paid Partnership only", "Ad: at beginning", "#sponsored in middle",
        "Verbal only (video)", "#ad first hashtag", "Disclosure in bio only",
    ]
    compliance_status = [
        "NON-COMPLIANT", "NON-COMPLIANT", "NON-COMPLIANT", "COMPLIANT",
        "NON-COMPLIANT", "NON-COMPLIANT", "COMPLIANT", "COMPLIANT",
        "NON-COMPLIANT",
    ]
    health_claims = [
        "Supports immune health (compliant)", "may help immune function (PROHIBITED)",
        "Clinically demonstrated (PROHIBITED if no RCT)", "No health claim made (compliant)",
        "promising results (PROHIBITED)", "Doctor recommended (REQUIRES DISCLOSURE)",
        "Gut health support (compliant with RCT)", "preliminary research (PROHIBITED)",
        "Helps strengthen immunity (PROHIBITED - 'helps')", "supports gut microbiome (compliant)",
    ]

    lines = ["post_id,handle,platform,post_date,post_time_est,follower_count,impressions,"
             "engagement_rate,disclosure_pattern,compliance_status,health_claim_detected,"
             "health_claim_compliant,penalty_exposure_usd,review_date,reviewer,action_required,"
             "notes"]

    for i in range(1, 1201):
        handle = rng.choice(handles)
        platform = rng.choice(platforms)
        month = rng.randint(1, 3)
        day = rng.randint(1, 28)
        hour = rng.randint(8, 22)
        minute = rng.choice([0, 15, 30, 45])
        followers = rng.randint(12000, 95000)
        impressions = int(followers * rng.uniform(0.15, 0.45))
        engagement = round(rng.uniform(0.8, 6.2), 2)
        disc_idx = rng.randint(0, len(disclosure_patterns) - 1)
        disc = disclosure_patterns[disc_idx]
        comp = compliance_status[min(disc_idx, len(compliance_status) - 1)]
        claim = rng.choice(health_claims)
        claim_compliant = "Yes" if "compliant" in claim.lower() and "PROHIBITED" not in claim else "No"
        penalty = 51744 if comp == "NON-COMPLIANT" else 0
        review_month = min(month + 1, 3)
        reviewer = rng.choice(["Jordan Ellis", "Sarah Chen", "Casey Park"])
        action = "UPDATE DISCLOSURE" if comp == "NON-COMPLIANT" else "NONE"
        note = rng.choice([
            "Follow up required before next post",
            "Corrected in subsequent post",
            "Influencer agreement updated",
            "Compliant - no action needed",
            "Verbal reminder sent to influencer",
            "Formal notice issued",
        ])
        lines.append(
            f"POST-{i:04d},{handle},{platform},2026-{month:02d}-{day:02d},"
            f"{hour:02d}:{minute:02d}:00,{followers},{impressions},{engagement},"
            f"\"{disc}\",{comp},\"{claim}\",{claim_compliant},"
            f"{penalty},2026-{review_month:02d}-{min(day+5,28):02d},{reviewer},{action},{note}"
        )

    return "\n".join(lines) + "\n"


def _gen_review_monitoring_log() -> str:
    """Generate ~50KB consumer review monitoring log."""
    rng = random.Random(7777)
    platforms = ["Amazon", "iHerb", "Vitacore.com", "Walmart.com", "Google Reviews",
                 "Yelp", "Trustpilot", "Reddit", "Facebook", "App Store"]
    violation_types = [
        "None", "None", "None", "None",
        "§465.3 — Insider review (employee account detected)",
        "§465.2 — Suspected fake review (AI-generated text pattern)",
        "§465.6 — Review suppression candidate (negative review hidden)",
        "§465.7 — Reviewer reports legal threat received",
        "§465.2 — Review claims product cures disease (false representation)",
        "§465.5 — Reviewer appears to be social media bot (fake account)",
    ]
    actions = [
        "No action", "No action", "No action",
        "Review removed (fake content per §465.2)",
        "Insider disclosure added per §465.3",
        "Escalated to CCO for review",
        "Legal threat report investigated",
        "Platform dispute filed",
    ]

    lines = ["review_id,platform,review_date,star_rating,reviewer_handle,"
             "reviewer_account_age_days,review_text_length,verified_purchase,"
             "suspected_violation_type,action_taken,penalty_exposure_usd,"
             "investigated_by,investigation_date,outcome"]

    for i in range(1, 851):
        platform = rng.choice(platforms)
        month = rng.randint(10, 12)  # Q4 2024 (after rule effective Oct 21, 2024)
        day = rng.randint(1, 28)
        stars = rng.choices([1, 2, 3, 4, 5], weights=[5, 8, 12, 30, 45])[0]
        handle = f"customer_{rng.randint(10000, 99999)}"
        account_age = rng.randint(3, 2000)
        text_len = rng.randint(50, 500)
        verified = rng.choices(["Yes", "No"], weights=[70, 30])[0]
        viol_idx = rng.choices(range(len(violation_types)),
                               weights=[15, 15, 15, 15, 3, 2, 1, 1, 1, 1])[0]
        viol = violation_types[viol_idx]
        action = rng.choice(actions) if "None" not in viol else "No action"
        penalty = 51744 if "§465" in viol else 0
        investigator = rng.choice(["Jordan Ellis", "Sarah Chen", "Casey Park", "External Counsel"])
        inv_date = f"2024-{min(month + 1, 12):02d}-{min(day + 7, 28):02d}"
        outcome = rng.choice([
            "Genuine review — retained", "Removed per §465.2(a)(1) — no such reviewer",
            "Disclosure added", "No violation confirmed", "Escalated to FTC compliance file",
            "Platform notified", "Retained — outside FTC jurisdiction",
        ])
        lines.append(
            f"REV-{i:05d},{platform},2024-{month:02d}-{day:02d},{stars},{handle},"
            f"{account_age},{text_len},{verified},\"{viol}\",\"{action}\","
            f"{penalty},{investigator},{inv_date},{outcome}"
        )

    return "\n".join(lines) + "\n"


def _gen_compliance_tracker() -> str:
    """Generate ~40KB compliance issue tracking spreadsheet."""
    rng = random.Random(4654)
    categories = [
        "Health Claim", "Endorsement Disclosure", "Consumer Review",
        "Environmental Claim", "Expert Endorsement", "Made in USA",
        "Celebrity Testimonial", "Review Suppression",
    ]
    regulations = [
        "16 CFR §255.5", "16 CFR §465.2", "16 CFR §465.3", "16 CFR §465.7",
        "16 CFR §260.8", "16 CFR §260.12", "16 CFR Part 323",
        "FTC Health Products Guidance", "16 CFR §255.2", "16 CFR §255.3",
    ]
    statuses = ["OPEN", "IN PROGRESS", "RESOLVED", "ESCALATED", "MONITORING"]
    severity_levels = ["HIGH", "HIGH", "MEDIUM", "MEDIUM", "LOW"]
    assignees = ["Jordan Ellis", "Sarah Chen", "Casey Park", "Mike Torres", "Alex Rivera (Ext.)"]

    lines = ["issue_id,category,description,regulation,ftc_citation,severity,"
             "status,date_identified,date_due,assignee,penalty_exposure_usd,"
             "resolution_action,resolution_date,notes"]

    issue_descriptions = [
        ("Health Claim", "'May help support immune function' in press release v1",
         "FTC Health Products Guidance", "FTC Health Products Guidance", 51744),
        ("Health Claim", "'Promising preliminary research' in press release v1",
         "FTC Health Products Guidance", "FTC Health Products Guidance", 51744),
        ("Health Claim", "'Clinically demonstrated to enhance digestive wellness'",
         "FTC Health Products Guidance", "FTC Health Products Guidance", 103488),
        ("Endorsement Disclosure", "Template A: '#ad' buried in hashtag list",
         "16 CFR Part 255", "16 CFR §255.5", 724416),
        ("Endorsement Disclosure", "Template C: Platform Paid Partnership label only",
         "16 CFR Part 255", "16 CFR §255.5", 51744),
        ("Consumer Review", "Employee review solicitation without disclosure directive",
         "16 CFR Part 465", "16 CFR §465.3", 2069760),
        ("Expert Endorsement", "'Doctor-Formulated' without named professional",
         "16 CFR Part 255", "16 CFR §255.3", 310464),
        ("Expert Endorsement", "Physician testimonial (Dr. Johnson) — actor or real?",
         "16 CFR Part 255", "16 CFR §255.3", 51744),
        ("Environmental Claim", "'Biodegradable formula capsules' without test data",
         "16 CFR Part 260", "16 CFR §260.8", 51744),
        ("Environmental Claim", "'Eco-friendly packaging' without substantiation",
         "16 CFR Part 260", "16 CFR §260.4", 51744),
        ("Made in USA", "'Made in USA' claim on label — sourcing analysis incomplete",
         "16 CFR Part 323", "16 CFR Part 323", 2000000),
        ("Consumer Review", "CEO directive: employee Amazon reviews (CEO-DIR-20260306-01)",
         "16 CFR Part 465", "16 CFR §465.3", 2069760),
        ("Health Claim", "'Backed by science' — vague, no specific studies cited",
         "FTC Health Products Guidance", "FTC Health Products Guidance", 51744),
        ("Endorsement Disclosure", "Influencer @wellnesswithjenna: no '#ad' in recent post",
         "16 CFR Part 255", "16 CFR §255.5", 51744),
        ("Consumer Review", "B. longum 'digestive comfort' claim — no RCT evidence",
         "FTC Health Products Guidance", "FTC Health Products Guidance", 103488),
        ("Review Suppression", "Amazon listing showing only 4-5 star reviews",
         "16 CFR Part 465", "16 CFR §465.6", 517440),
        ("Celebrity Testimonial", "CEO quote in press release — self-endorsement context",
         "16 CFR Part 255", "16 CFR §255.1", 0),
        ("Health Claim", "'Helps strengthen the gut-immune axis' — 'helps' is prohibited",
         "FTC Health Products Guidance", "FTC Health Products Guidance", 51744),
        ("Environmental Claim", "'Recyclable PET bottle' — coverage analysis required",
         "16 CFR Part 260", "16 CFR §260.12", 0),
        ("Expert Endorsement", "'Doctor-Formulated' per revised audit (email_revised_audit_v2)",
         "16 CFR Part 255", "16 CFR §255.3", 310464),
    ]

    for i, (cat, desc, reg, citation, exposure) in enumerate(issue_descriptions, 1):
        severity = rng.choice(severity_levels)
        status = rng.choice(statuses)
        identified_month = rng.randint(12, 12)
        identified_day = rng.randint(1, 20)
        due_day = min(identified_day + rng.randint(7, 30), 28)
        assignee = rng.choice(assignees)
        resolution = rng.choice([
            "Remove claim from all materials",
            "Update disclosure to 'Ad:' format",
            "Obtain independent test report",
            "Name specific professional with credentials",
            "Update employee review policy",
            "Display all review ratings equally",
            "Pending: awaiting evidence collection",
            "Resolved: claim removed from v2 draft",
        ])
        res_date = f"2026-01-{min(due_day + 10, 28):02d}" if status in ["RESOLVED"] else "N/A"
        note = rng.choice([
            "Superseded by CEO retraction CEO-RETRACT-20260312-01",
            "See also related issue #" + str(rng.randint(1, 20)),
            "External counsel opinion requested",
            "High priority — launch blocker",
            "Track for post-launch monitoring",
        ])
        lines.append(
            f"COMP-{i:03d},{cat},\"{desc}\",{reg},{citation},"
            f"{severity},{status},2025-{identified_month:02d}-{identified_day:02d},"
            f"2026-01-{due_day:02d},{assignee},{exposure},\"{resolution}\","
            f"{res_date},\"{note}\""
        )

    # Add more rows for comprehensive tracking
    extra_categories = ["Health Claim", "Endorsement Disclosure", "Consumer Review"]
    for i in range(21, 201):
        cat = rng.choice(extra_categories)
        reg_citation = rng.choice(regulations)
        severity = rng.choice(severity_levels)
        status = rng.choice(statuses)
        exposure = rng.choice([0, 51744, 103488, 206976, 517440])
        lines.append(
            f"COMP-{i:03d},{cat},\"General compliance monitoring item {i}\","
            f"{reg_citation},{reg_citation},{severity},{status},"
            f"2026-01-{rng.randint(1,28):02d},2026-03-{rng.randint(1,28):02d},"
            f"{rng.choice(assignees)},{exposure},\"Under review\",N/A,\"Monitoring\""
        )

    return "\n".join(lines) + "\n"


def _gen_competitor_analysis() -> str:
    """Generate ~15KB competitor analysis document."""
    rng = random.Random(1776)
    companies = [
        ("Culturelle Pro", "Reckitt Benckiser", 45000),
        ("Florastor Daily Probiotic", "Biocodex", 38000),
        ("Garden of Life RAW Probiotics", "Nestlé Health Science", 52000),
        ("Renew Life Ultimate Flora", "Church & Dwight", 33000),
        ("Nature's Bounty Ultra Probiotic", "Nestlé Health Science", 28000),
        ("Align Probiotic", "Procter & Gamble", 71000),
        ("Seed Daily Synbiotic", "Seed Health", 89000),
        ("MegaFood MegaFlora", "MegaFood", 25000),
        ("Swanson Probiotics", "Swanson Health", 19000),
        ("Jarrow Formulas Ideal Bowel Support", "Jarrow Formulas", 31000),
    ]
    output = """# VitaCore ProBio+ Daily — Competitive Landscape Analysis

**Prepared by**: Marketing Strategy Team
**Date**: February 2026
**Purpose**: Competitive positioning and compliance benchmarking

---

## Market Overview

The U.S. probiotic supplement market was valued at approximately $6.8 billion in 2024,
with projected CAGR of 8.3% through 2030. Probiotic + vitamin combination products
represent the fastest-growing segment, with 24% year-over-year growth.

### Key Market Drivers

1. **Post-COVID immune health awareness**: Consumer demand for immune support products
   increased significantly following the COVID-19 pandemic.

2. **Gut-brain axis research**: Growing consumer awareness of the microbiome's role in
   mental health and cognitive function is driving premium probiotic adoption.

3. **Clean label trend**: Consumers increasingly prefer products with fewer, more
   recognizable ingredients.

4. **FTC compliance awareness**: Following the 2024 implementation of 16 CFR Part 465,
   several market leaders have updated their marketing practices to avoid penalties.

---

## Competitive Product Analysis

"""

    for i, (name, manufacturer, annual_revenue) in enumerate(companies, 1):
        cfus = rng.randint(5, 100)
        strain_count = rng.randint(2, 12)
        price = rng.uniform(24.99, 59.99)
        rating = rng.uniform(3.8, 4.7)
        review_count = rng.randint(1200, 45000)
        has_disclosure = rng.random() > 0.3
        output += f"""### {i}. {name} ({manufacturer})

**Annual Revenue (est.)**: ${annual_revenue:,}K
**CFU Count**: {cfus} billion (at manufacture)
**Strains**: {strain_count}
**Retail Price**: ${price:.2f}/30-day supply
**Average Rating**: {rating:.1f}/5.0 ({review_count:,} reviews)
**Influencer Disclosure Compliance**: {"Adequate" if has_disclosure else "Questionable — potential §255.5 issues observed"}

**Health Claims Analysis**:
- Primary claim: {"Clinically studied strains for digestive health" if rng.random() > 0.5 else "Supports gut health and immune function"}
- Evidence standard met: {"Yes — RCT citations provided" if rng.random() > 0.6 else "Unclear — no specific studies cited"}
- Prohibited qualifier detected: {"None observed" if rng.random() > 0.4 else "'May help' language observed — potential FTC concern"}

**Review Policy Observations**:
- Employee reviews: {"No evidence observed" if rng.random() > 0.3 else "Possible — several reviews from users with limited history"}
- Review display: {"All ratings displayed" if rng.random() > 0.5 else "Possible selective display — no 1-star reviews visible"}
- Influencer disclosures: {"#ad visible at post beginning" if has_disclosure else "Hashtag-buried or missing disclosures observed"}

"""

    output += f"""---

## VitaCore ProBio+ Daily Competitive Positioning

### Strengths
- Comprehensive vitamin + probiotic combination (differentiator)
- NCFM strain (clinically studied — meets FTC RCT standard for immune claims)
- Competitive price point ($39.99 planned retail)

### Regulatory Weaknesses (Pre-Compliance Review)
- B. longum digestive comfort claim lacks RCT support
- Prior influencer disclosure practices non-compliant with §255.5
- Employee review solicitation (withdrawn following compliance review)
- "Clinically demonstrated" language (removed following CEO retraction)

### Compliance Opportunity
Post-compliance-review, VitaCore can differentiate by being among the first brands
to fully implement 16 CFR Part 465 best practices and adopt "FTC Compliant Marketing"
as a brand attribute — a growing consumer value driver in the supplement sector.

---

## Review Authenticity Benchmarking

| Company | FTC-Compliant Disclosure | Fake Review Risk | Review Display |
|---------|------------------------|-----------------|----------------|
| Culturelle Pro | High | Low | All ratings |
| Seed Daily Synbiotic | High | Low | All ratings |
| Garden of Life RAW | Medium | Low | All ratings |
| Align Probiotic | High | Low | All ratings |
| Market Newcomers (avg) | Low | High | Often selective |
| **VitaCore (post-review)** | **High (target)** | **Low (target)** | **All (target)** |

---

## Key Compliance Recommendations from Competitive Analysis

1. **Adopt "Compliant by Design" marketing**: Position FTC compliance as a brand strength.
2. **Use RCT citations in all health claims**: Culturelle and Seed have successfully used
   this approach to credibly substantiate their claims.
3. **Implement influencer disclosure training**: All 14 influencer partners should receive
   specific FTC disclosure guidance before any campaign launch.
4. **Avoid "May help" and similar qualifiers**: These are red flags that trigger FTC review;
   competitors who have faced FTC action commonly used these terms.
5. **Establish a review monitoring program**: Following 16 CFR Part 465 implementation,
   proactive monitoring and removal of any inadvertent fake reviews is critical.
"""
    return output


def _gen_large_ingredient_analysis() -> str:
    """Generate ~18KB ingredient scientific support document."""
    return """# ProBio+ Daily — Ingredient Scientific Support Documentation

**Prepared by**: Dr. Priya Nair, PhD, Director of R&D, VitaCore Inc.
**Date**: January 2026
**Scope**: Regulatory-grade substantiation documentation for FTC compliance review

---

## Introduction

This document provides the comprehensive scientific support documentation for each
active ingredient in ProBio+ Daily. The assessment framework follows the FTC's Health
Products Compliance Guidance (December 2022), specifically evaluating evidence against
the randomized, controlled human clinical testing (RCT) gold standard.

---

## Ingredient 1: Lactobacillus acidophilus NCFM Strain

### Clinical Evidence Summary

**Study 1**: Smith JA, Jones BL, Williams CR, et al. (2018). "Lactobacillus acidophilus
NCFM supplementation and upper respiratory tract infection incidence in healthy adults:
a randomized, double-blind, placebo-controlled trial." *Journal of Clinical Gastroenterology*,
52(3), 245-253.

- **Design**: RCT; randomized, double-blind, placebo-controlled
- **Population**: N=120 healthy adults aged 18-65, no antibiotic use in prior 3 months
- **Intervention**: L. acidophilus NCFM 10B CFU/day vs. placebo for 12 weeks
- **Primary outcome**: Frequency of upper respiratory tract infections (URTIs)
- **Results**: Statistically significant reduction in URTI frequency in treatment group
  (p<0.01, 95% CI: -0.3 to -0.1 episodes). Cohen's d = 0.42 (moderate effect size).
- **Clinical significance**: Reduction is clinically meaningful per consensus criteria
- **FTC Assessment**: MEETS gold standard — RCT with statistically and clinically significant results

**Study 2**: Johnson MW, Lee SR (2020). "Effects of NCFM probiotic on gut microbiome
diversity in healthy adults: an 8-week randomized controlled trial." *Nutrients*, 12(8), 2341.

- **Design**: RCT; randomized, controlled
- **Population**: N=85 healthy adults, 25-65 years
- **Intervention**: L. acidophilus NCFM 10B CFU/day vs. control for 8 weeks
- **Primary outcome**: Shannon diversity index of gut microbiome
- **Results**: Statistically significant improvement in diversity (p<0.05, mean Δ=0.34)
- **FTC Assessment**: MEETS gold standard for "supports gut microbiome balance" claim

### Permitted Claims (Substantiated)
- "Supports immune health"
- "Supports gut microbiome balance"
- "Supports digestive wellness" (based on indirect microbiome → digestive health pathway, with appropriate qualification)

### Claims Requiring Qualification or Evidence
- "Clinically demonstrated to enhance digestive wellness" — this specific phrasing implies a direct
  clinical endpoint, but the NCFM evidence is for microbiome diversity, not a direct digestive
  symptom endpoint. QUALIFY OR REMOVE.

---

## Ingredient 2: Bifidobacterium longum

### Clinical Evidence Summary

**Study 1**: Chen XY, Liu RH, et al. (2019). "Adhesion properties of Bifidobacterium longum
to human intestinal epithelial cells: an in vitro mechanistic study." *Journal of Applied
Microbiology*, 127(4), 1103-1115.

- **Design**: In vitro cell culture model
- **Cells**: Caco-2 human intestinal epithelial cell line
- **Intervention**: B. longum exposure at varying concentrations
- **Results**: Increased bacterial adhesion (p<0.05), reduced pro-inflammatory cytokine IL-8
  secretion
- **FTC Assessment**: DOES NOT MEET gold standard. Per FTC Health Products Guidance:
  "animal studies, in vitro studies, and consumer surveys" cannot standalone substantiate
  health claims. This study cannot form the basis of any health claim.

**Study 2**: Martinez TP, Rodriguez JL, et al. (2021). "Bifidobacterium longum attenuates
DSS-induced colitis in a mouse model: implications for human digestive health."
*Frontiers in Microbiology*, 12, 678234.

- **Design**: Animal study (murine colitis model)
- **Population**: C57BL/6 mice, N=30 (15 treatment, 15 control)
- **Results**: Significant reduction in inflammatory markers (p<0.01), improved colon
  histology scores
- **FTC Assessment**: DOES NOT MEET gold standard. Per FTC Health Products Guidance,
  animal studies cannot standalone substantiate health claims. May be used as mechanistic
  support only if also supported by human RCT data.

### Permitted Claims (Substantiated)
- **None independently** — both available studies are in vitro or animal, which are
  explicitly listed as insufficient standalone evidence in the FTC Health Products Guidance.

### Required Action
Remove all claims attributing digestive comfort or health benefits specifically to
B. longum until a qualifying human RCT is completed. The ingredient may remain in the
formula, but no specific health claim may be made for it in advertising.

---

## Ingredient 3: Vitamin D3 (Cholecalciferol)

### Clinical Evidence Summary

**Primary Reference**: Martineau AR, Jolliffe DA, Hooper RL, et al. (2017).
"Vitamin D supplementation to prevent acute respiratory tract infections: systematic
review and meta-analysis of individual participant data." *BMJ*, 356, i6583.

- **Design**: Individual participant data (IPD) meta-analysis
- **Studies included**: 25 randomized controlled trials
- **Total participants**: N=11,321
- **Primary outcome**: Acute respiratory tract infection (ARTI) incidence
- **Results**: Vitamin D supplementation significantly reduced risk of ARTI (adjusted OR 0.88,
  95% CI 0.81-0.96; p=0.003). Effect was stronger in vitamin D-deficient participants.
- **FTC Assessment**: MEETS gold standard — this is among the strongest immune support
  evidence bases available for any dietary supplement ingredient.

**Additional support**:
- Holick MF, et al. (2012). "Evaluation, treatment, and prevention of vitamin D deficiency."
  *J Clin Endocrinol Metab*, 97(7), 1153-1998. (Mechanism basis)
- Multiple Cochrane reviews confirm immune support role.

### Permitted Claims (Substantiated)
- "Supports immune function" (vitamin D3 at adequate dose)
- "Supports healthy immune response"
- "Contributes to normal immune system function"

---

## Ingredient 4: Vitamin C (Ascorbic Acid)

### Clinical Evidence Summary

**Primary Reference**: Hemilä H, Chalker E (2013). "Vitamin C for preventing and treating
the common cold." *Cochrane Database of Systematic Reviews*, (1), CD000980.

- **Design**: Cochrane systematic review + meta-analysis
- **Studies**: 29 trial comparisons with 11,077 participants for prevention analysis
- **Results**: Regular vitamin C supplementation reduced cold duration (adults: -8%,
  children: -14%); reduced cold severity; protective effect in persons under heavy
  physical stress (RR 0.48, 95% CI: 0.35-0.64).
- **FTC Assessment**: MEETS gold standard for antioxidant and immune support claims.

**Additional support**: Vitamin C as an antioxidant is one of the most robustly
evidenced nutritional claims in the scientific literature.

### Permitted Claims (Substantiated)
- "Provides antioxidant support"
- "Supports immune health"
- "Contributes to normal immune function"
- "Powerful antioxidant" (with appropriate context)

---

## Ingredient 5: Zinc (Zinc Gluconate)

### Clinical Evidence Summary

**Primary Reference**: Singh M, Das RR (2011). "Zinc for the common cold."
*Cochrane Database of Systematic Reviews*, (2), CD001364.

- **Design**: Cochrane systematic review + meta-analysis
- **Studies**: 13 placebo-controlled trials
- **Results**: Zinc supplementation significantly reduced duration (MD -1.03 days,
  95% CI: -1.97 to -0.09) and severity of common cold; 1.4 times more likely to have
  resolved symptoms at 7 days.
- **FTC Assessment**: MEETS gold standard for immune function support.

**Additional**: IOM recommended dietary allowances establish zinc's role in immune
function as essential and well-documented.

### Permitted Claims (Substantiated)
- "Supports immune function" (zinc at adequate dose)
- "Essential mineral for immune health"

---

## Overall Evidence Assessment Matrix

| Ingredient | Evidence Type | FTC Standard | Permitted Claim | Action Required |
|-----------|--------------|-------------|-----------------|-----------------|
| L. acidophilus NCFM | 2 RCTs | MET | "Supports immune health" | None |
| B. longum | in vitro + animal | NOT MET | None independently | Remove or qualify all B. longum health claims |
| Vitamin D3 | RCT meta-analysis (25 RCTs) | MET | "Supports immune function" | None |
| Vitamin C | Cochrane review | MET | "Antioxidant/immune support" | None |
| Zinc | Cochrane review | MET | "Supports immune function" | None |

---

## Prohibited Language Analysis

The following language appears in current marketing materials and must be addressed:

| Term/Phrase | Location | Why Prohibited | Required Action |
|------------|---------|----------------|-----------------|
| "may help support" | Press release v1 | "may help" = prohibited qualifying language | Replace with "supports" (if substantiated) |
| "promising results" | Press release v1 | "promising" = prohibited qualifier | Remove — no conditional language for unsubstantiated claims |
| "preliminary research" | Press release v1 | "preliminary" = prohibited qualifier | Remove |
| "clinically demonstrated" | Press release v1 | Strong efficacy claim; B. longum has no RCT | Remove for B. longum-related claims |
| "pilot studies" | Press release v1 | "pilot" = prohibited qualifier | Remove |
| "helps strengthen" | Press release v1 | "helps" = prohibited qualifier | Replace with "supports" (if substantiated) |

Per FTC Health Products Compliance Guidance (Dec 2022), these terms cannot be used as
qualifiers to hedge unsubstantiated claims. They do not transform an unsubstantiated
claim into a compliant one.

---

## Conclusion and Compliance Certification

Based on this analysis, the following actions are required before launch:

1. Remove B. longum-specific health claims from all marketing materials.
2. Remove all prohibited qualifying language from press release and ad copy.
3. Ensure all remaining health claims are attributed specifically to ingredients with RCT support.
4. Maintain copies of all cited studies for FTC substantiation file.
5. Review and update claims annually as new evidence emerges.

*Prepared by Dr. Priya Nair, PhD, Nutrition Science*
*Reviewed by CCO Jordan Ellis*
*Date: January 2026*
"""


# --------------------------------------------------------------------------- #
# 1. 系统文件
# --------------------------------------------------------------------------- #
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles and output conventions.
2. Read `USER.md` to learn about the team members and communication channels.
3. Read `sessions/session_main_brief.md` for explicit output preferences (P1, P2, P5).
4. Run `exec ls -R` to inspect current workspace files.
5. Use `sessions_list` to discover all history sessions.
6. Use `sessions_history` to read session content as needed.

You are a Compliance AI assistant supporting Jordan Ellis, Chief Compliance Officer (CCO),
at VitaCore Inc., a consumer health supplement brand preparing to launch ProBio+ Daily
in the United States. Your primary mandate in this engagement is consumer review authenticity
and endorsement disclosure compliance under FTC regulations.
""")

    w(WS / "SOUL.md", """# Working Principles

1. **Authoritative-source-first**: The canonical FTC regulatory texts live under
   `regulatory/`. Auto-generated summaries (files named `*_DECOY*` or `*_SUMMARY_BOT*`)
   are NOT authoritative — they may contain deliberate errors. Always verify numbers
   against the primary regulatory documents.

2. **Verbatim citation**: When quoting statutory or regulatory text, reproduce the exact
   wording from the source document. Never paraphrase §255.5 or §465.2 in legal deliverables.

3. **Output schema discipline**: Every JSON deliverable carries a top-level
   `"schema_version": "1.0"` field (P1). Every compliance issue entry carries a
   `"ftc_citation"` field formatted exactly as `"16 CFR §XXX.X"` (P2).

4. **Markdown heading hierarchy** (P3, active from Q4 feedback onward):
   H1 = document title / file name; H2 = claim category; H3 = specific provision.

5. **Temporal awareness**: When a later communication (update, revised letter) supersedes
   an earlier one, the later document controls — revisit prior conclusions accordingly.

6. **Severity tagging** (P4, active from Q4 feedback onward):
   Prohibited-term replacement tables must include a `severity` column (high/medium/low)
   corresponding to FTC enforcement priority.

7. **File naming in `final/`** (P5): All documents placed under the `final/` directory
   must follow the convention `{document_type}_final_YYYYMMDD.{ext}`.
""")

    w(WS / "USER.md", """# People and Channels

## Primary User
- **Jordan Ellis** — Chief Compliance Officer (CCO), VitaCore Inc.
  Reviews all compliance deliverables; prefers concise JSON with explicit FTC citations.

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Sarah Chen | In-House Counsel | Slack #legal-review | Deeply versed in 2023 Endorsement Guides; authoritative on Part 255 |
| Mike Torres | Marketing VP | Slack #legal-review | Sometimes quotes outdated figures or the DECOY summary; double-check |
| Alex Rivera | External Compliance Counsel | Email | Compliance Counsel LLC; sent first opinion letter; later revised it |
| Casey Park | Social Media Manager | Discord #marketing | Manages influencer relationships and posting schedules |
| Wei Zhang | CEO | Feishu DM | Issues brand-level directives; informal guidance has no FTC legal force |

## Channels
- **Slack #legal-review**: Legal + marketing discussion on draft review policies
- **Email (Compliance Counsel LLC ↔ CCO)**: Formal external audit letters
- **Feishu DM (CEO Wei Zhang ↔ CCO)**: Executive directives and brand updates
- **Discord #marketing**: Influencer campaign scripts and content review
""")

    w(WS / "IDENTITY.md", """# Identity

You are **ComplianceOps AI**, deployed to support Jordan Ellis (CCO) at VitaCore Inc.
during the pre-launch compliance review of ProBio+ Daily.

Your mandate in this engagement focuses on:
1. Consumer review authenticity compliance (16 CFR Part 465, effective October 21, 2024).
2. Endorsement and testimonial disclosure compliance (16 CFR Part 255, effective July 26, 2023).
3. Disclosure adequacy for influencer and social media marketing.

Source documents under `regulatory/` and `sessions/` are reference inputs.
You create deliverables under `reports/`, `policies/`, `templates/`, `training/`, and `final/`.
""")

    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session |
| `sessions_history` | Read a specific session | Use to review past discussion |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to write deliverable files |

## Rules
- Source documents under `regulatory/`, `sessions/`, `research/` are read-only reference.
- Create deliverables under `reports/`, `policies/`, `templates/`, `training/`, `final/`.
- In history sessions, use only `read` and light `exec`.
""")

    # session_main_brief.md — P1/P2/P5 explicit preference declaration
    w(WS / "sessions" / "session_main_brief.md", """# VitaCore Compliance Engagement — Main Session Brief

## Engagement Scope

This engagement covers consumer review authenticity and endorsement disclosure compliance
for VitaCore Inc.'s ProBio+ Daily launch. Primary regulatory frameworks:

- **16 CFR Part 465** (Consumer Reviews and Testimonials Rule, effective October 21, 2024)
- **16 CFR Part 255** (Endorsement Guides, 2023 revision, effective July 26, 2023)
- **FTC Health Products Compliance Guidance** (December 2022)

## Mandatory Output Conventions (apply throughout all rounds)

### P1 — JSON Schema Version Tag
Every JSON deliverable MUST contain a top-level field:
```json
"schema_version": "1.0"
```
This field enables VitaCore's compliance registry to version-control deliverables
and will be validated automatically. Files missing this field will be rejected at upload.

### P2 — FTC Citation Format
Every compliance issue entry MUST include a field:
```json
"ftc_citation": "16 CFR §XXX.X"
```
The format is strictly `"16 CFR §"` followed by the section number (e.g., `"16 CFR §465.2"`).
No other citation format is acceptable for machine-readable deliverables.

### P5 — Final Directory File Naming
All files placed in the `final/` directory MUST follow the naming convention:
```
{document_type}_final_YYYYMMDD.{ext}
```
Examples: `press_release_final_20260309.md`, `compliance_summary_final_20260309.json`.
The date must reflect the actual document date in YYYYMMDD format.

## Reference Date
All deliverables in this engagement are dated: **2026-03-09** (ISO 8601: 2026-03-09).
""")


# --------------------------------------------------------------------------- #
# 2. Regulatory documents (真实锚点合成全文)
# --------------------------------------------------------------------------- #
_APPENDIX_255 = None
_APPENDIX_465 = None
_COMPETITOR_ANALYSIS = None
_INGREDIENT_ANALYSIS = None
_FTC_CASE_LAW = None
_INFLUENCER_POLICY = None
_AD_TV_SCRIPT = None
_COMPLIANCE_FAQ = None
_INFLUENCER_AUDIT_LOG = None
_REVIEW_MONITORING_LOG = None
_COMPLIANCE_TRACKER = None


def _init_large_content() -> None:
    global _APPENDIX_255, _APPENDIX_465, _COMPETITOR_ANALYSIS, _INGREDIENT_ANALYSIS
    global _FTC_CASE_LAW, _INFLUENCER_POLICY, _AD_TV_SCRIPT, _COMPLIANCE_FAQ
    global _INFLUENCER_AUDIT_LOG, _REVIEW_MONITORING_LOG, _COMPLIANCE_TRACKER
    _APPENDIX_255 = _gen_255_appendix_examples()
    _APPENDIX_465 = _gen_465_appendix()
    _COMPETITOR_ANALYSIS = _gen_competitor_analysis()
    _INGREDIENT_ANALYSIS = _gen_large_ingredient_analysis()
    _FTC_CASE_LAW = _gen_ftc_case_law_digest()
    _INFLUENCER_POLICY = _gen_influencer_policy_doc()
    _AD_TV_SCRIPT = _gen_ad_tv_script()
    _COMPLIANCE_FAQ = _gen_compliance_faq()
    _INFLUENCER_AUDIT_LOG = _gen_influencer_audit_log()
    _REVIEW_MONITORING_LOG = _gen_review_monitoring_log()
    _COMPLIANCE_TRACKER = _gen_compliance_tracker()


def gen_regulatory_docs() -> None:
    appendix_255 = _APPENDIX_255
    appendix_465 = _APPENDIX_465
    competitor_analysis = _COMPETITOR_ANALYSIS
    ingredient_analysis = _INGREDIENT_ANALYSIS

    # 16 CFR Part 255 — Endorsement Guides 2023
    w(WS / "regulatory" / "ftc_endorsement_guides_2023.md", """# 16 CFR Part 255 — Guides Concerning Use of Endorsements and Testimonials in Advertising

**Effective Date: July 26, 2023**
Source: https://www.law.cornell.edu/cfr/text/16/part-255

---

## §255.0 — Purpose and Definitions

(a) **Purpose.** These guides represent the Commission's current views on how Section 5 of the
Federal Trade Commission Act (15 U.S.C. 45) applies to the use of endorsements and testimonials
in advertising. Practices inconsistent with these guides may result in corrective action by the
Commission under Section 5 if, after investigation, the Commission has reason to believe that the
practices fall within the scope of conduct declared unlawful by the statute.

(b) **Definitions.**

*Endorsement* means any advertising message (including verbal statements, demonstrations, or
depictions of the name, signature, likeness, or other identifying personal characteristics of
an individual or the name or seal of an organization) that consumers are likely to believe
reflects the opinions, beliefs, findings, or experiences of a party other than the sponsoring
advertiser, even if the views expressed by that party are identical to those of the sponsoring
advertiser. The party whose opinions, beliefs, findings, or experiences the message appears to
reflect will be called the *endorser* and may be an individual, group, or institution.

*Virtual influencer* means a computer-generated character or avatar used in endorsements. The
2023 revision explicitly extends the guides' coverage to virtual influencers and AI-generated
content used in endorsements.

---

## §255.1 — General Considerations

(a) Endorsements must reflect the honest opinions, findings, beliefs, or experience of the
endorser. Furthermore, an endorsement may not convey any representation that would be deceptive
if made directly by the advertiser.

(b) The endorser must be a bona fide user of the advertised product at the time the endorsement
is given. An advertiser may not use an endorsement of an individual who is no longer a bona fide
user of the product if the advertiser has reason to believe that the individual is not a bona fide
user.

(c) Advertisements presenting endorsements by what are represented to be ordinary consumers
should clearly and conspicuously disclose unexpected results and the limited applicability
of the endorser's experience to what consumers may generally expect to achieve.

---

## §255.2 — Consumer Endorsements

(a) An advertisement employing endorsements by one or more consumers about the performance
of an advertised product or service will be interpreted as representing that the product or
service is effective for the purpose depicted in the advertisement. Therefore, the advertiser
must possess and rely upon adequate substantiation, including, when appropriate, competent and
reliable scientific evidence, to support such representation.

(b) If the advertised product or service does not perform as well for most users as depicted
in the advertisement, the advertisement should either clearly and conspicuously disclose what
the generally expected performance will be in the depicted circumstances or clearly and
conspicuously disclose the limited applicability of the endorser's experience to what
consumers may generally expect to achieve.

**Key 2023 Change:** The previous practice of using "Results Not Typical" or similar disclaimers
as a safe harbor was abolished in the 2009 revision (carryover to 2023). Advertisers must now
demonstrate the typical results consumers achieve, not merely disclaim atypical results.

---

## §255.3 — Expert Endorsements

(a) Whenever an advertisement represents, directly or by implication, that the endorser is
an expert with respect to the endorsement message, then the endorser's qualifications must in
fact give the endorser the expertise that he or she is represented as possessing with respect
to the endorsement.

(b) Although the expert may be well qualified to evaluate the advertised product, it should
be noted that the FTC does not consider "doctor recommended" or "cardiologist recommended"
claims to automatically imply RCT-level substantiation. Such claims trigger the "reasonable
basis" analysis and, for health claims, the Commission's health products guidance applies.

---

## §255.4 — Endorsements by Organizations

When an organization endorses a product, it must evaluate the product using objective criteria
and the endorsement must represent the collective judgment of the organization rather than any
individual member.

---

## §255.5 — Disclosure of Material Connections

When there exists a connection between the endorser and the seller of the advertised product
that might materially affect the weight or credibility of the endorsement (i.e., the connection
is not reasonably expected by the audience), such connection must be fully disclosed.

**Verbatim text of the material connection trigger:**
> "a connection between the endorser and the seller of the advertised product that might
> materially affect the weight or credibility of the endorsement"

**Connections requiring disclosure include:**
- Monetary payment or compensation of any kind
- Free products, samples, or discounts (including early access)
- Affiliate marketing arrangements (commission on sales)
- Employment relationship
- Family relationship with company personnel
- Potential to win prizes or awards

**Disclosure adequacy standards (Clear and Conspicuous requirement):**
The disclosure must be "difficult to miss and be easily understandable by ordinary consumers."

Specific guidance on placement:
1. "#ad" or "Ad:" placed at the **beginning** of the post is effective.
2. Hashtags buried among a long list of other hashtags (e.g., "#probiotic #health #wellness #ad")
   are generally **not adequate** — the disclosure is too easy to miss.
3. Relying solely on a platform's built-in "Paid Partnership" label or similar tool is
   **insufficient** — some consumers do not understand what it means.
4. In video content, verbal disclosure at the opening of the video is recommended.

**Examples illustrating the standard:**

*Example 3 (Medical Professional):* A physician endorses a supplement brand on social media
without disclosing a financial relationship with the manufacturer. Even if the physician
genuinely believes in the product, the undisclosed payment creates a material connection
that must be disclosed. Failure = deceptive endorsement.

*Example 6 (Paid Actor Posing as Consumer):* A company employs actors posing as ordinary
consumers on social media. The paid relationship must be disclosed. Use of AI-generated
personas that are not disclosed as AI also triggers this requirement.

*Example 11 (Blogger Affiliate Link):* A blogger posts a product review and earns a commission
on sales through an affiliate link. The commission arrangement is a material connection that
must be disclosed, even if the blogger genuinely likes the product.

---

## §255.6 — Endorsements Directed to Children

Special care must be taken when endorsements are directed to children. Children may have
limited ability to understand commercial intent and may place undue weight on endorsements
by characters or celebrities they admire. Advertisers must ensure disclosures are understandable
to the target child audience.

---

## Appendix A — Key 2023 Updates Summary

| Change | Prior Rule | 2023 Rule |
|--------|-----------|-----------|
| Virtual influencers | Not addressed | Explicitly covered |
| AI-generated content | Not addressed | Treated as endorsement if not clearly labeled |
| "Results Not Typical" disclaimer | Allowed as safe harbor (1980) | NOT a safe harbor (abolished 2009, reaffirmed 2023) |
| Platform "Paid Partnership" tool | Not addressed | Insufficient alone |
| Hashtag placement | Guidance limited | #ad must be prominent, not buried |
| Effective date | June 5, 2009 (prior revision) | **July 26, 2023** |

---

## Appendix B — Penalty Framework

Violations of these guides (when incorporated into a Commission order) may result in civil
penalties. For knowing violations of FTC orders, penalties apply per violation.

The applicable civil penalty amounts are indexed to the Consumer Price Index:
- **2024 base rate**: $51,744 per violation (16 CFR Part 465 and related enforcement)
- **2025 adjusted rate**: $53,088 per violation (effective February 2025)

Note: The 2024 base rate of $51,744 governs for ProBio+ Daily's compliance analysis.
""" + appendix_255)

    # 16 CFR Part 465 — Consumer Reviews and Testimonials Rule
    w(WS / "regulatory" / "ftc_consumer_reviews_rule_465.md", """# 16 CFR Part 465 — Rule on the Use of Consumer Reviews and Testimonials

**Effective Date: October 21, 2024**
Source: https://www.law.cornell.edu/cfr/text/16/part-465

---

## §465.1 — Definitions

**Consumer review** means a written, verbal, or video review of a product, service, or business
by a person who represents, explicitly or implicitly, that they used or have experience with
the product, service, or business.

**Consumer testimonial** means a written, verbal, or video statement by a person who represents,
explicitly or implicitly, that they are a customer of, or have personally used or had experience
with, a product, service, or business.

**Celebrity testimonial** means a written, verbal, or video statement by a person who is publicly
known that endorses or recommends a product, service, or business.

**Insider** means an officer, manager, employee, or agent of a company, or the immediate
family member or household member of such a person.

---

## §465.2 — Fake or False Consumer Reviews, Consumer Testimonials, or Celebrity Testimonials

(a) **Prohibition.** It is an unfair or deceptive act or practice and a violation of this part
for a business to write, create, or sell a consumer review, consumer testimonial, or celebrity
testimonial that materially misrepresents, expressly or by implication:

(1) That the reviewer or testimonialist exists;

(2) That the reviewer or testimonialist used or otherwise had experience with the product,
service, or business; or

(3) The reviewer's or testimonialist's experience with the product, service, or business.

(b) It is also an unfair or deceptive act or practice for a business to disseminate or cause
to be disseminated to any person a consumer review, consumer testimonial, or celebrity
testimonial that the business knows or should know is a fake or false review or testimonial,
regardless of whether the business created or purchased the review or testimonial.

(c) It is an unfair or deceptive act or practice for a business to buy or sell any positive
consumer review, or any negative consumer review for a competitor, whether directly or
through an intermediary.

---

## §465.3 — Insider Reviews and Consumer Testimonials

It is an unfair or deceptive act or practice for a business to solicit, create, or disseminate
a consumer review by an insider without clearly and conspicuously disclosing the insider's
material connection to the business in or adjacent to the review itself.

---

## §465.4 — Company-Controlled Review Websites

It is an unfair or deceptive act or practice for a business to operate or control a review
website or platform that publishes consumer reviews of its own products, services, or
businesses without clearly and conspicuously disclosing that the website or platform is
owned or controlled by the business being reviewed.

---

## §465.5 — Compensation for Social Media Indicators

It is an unfair or deceptive act or practice for a business to provide compensation or other
incentives in exchange for social media indicators (e.g., likes, followers, views, reposts)
from accounts that do not represent actual consumers who have purchased or used the product
or service.

---

## §465.6 — Prohibited Review Suppression

(a) It is an unfair or deceptive act or practice for a business to suppress or withhold
consumer reviews in a discriminatory manner by displaying only reviews that are positive
while suppressing or withholding negative reviews.

(b) A business may, however, remove reviews that are:
(1) Fake or false (as defined in §465.2);
(2) Contain irrelevant content; or
(3) Contain inappropriate content (e.g., obscenity, personal attacks unrelated to the product).

---

## §465.7 — Review Suppression by Threat or Intimidation

It is an unfair or deceptive act or practice for a business (directly or through an agent)
to use, or to threaten to use, an unfounded or groundless legal threat, a physical threat,
intimidation, or a public false accusation (including public shaming) against any person
in an attempt to:

(1) Prevent a review or any portion thereof from being written or created, or

(2) Cause a review or any portion thereof to be removed.

---

## §465.8 — False Social Media Indicators

It is an unfair or deceptive act or practice for a business to buy, sell, or create fake
social media indicators (followers, likes, views) to misrepresent the popularity or
consumer acceptance of a product, service, or business.

---

## Enforcement and Penalties

**Civil penalty per violation**: $51,744 (2024 base rate, adjusted annually per 15 U.S.C. 45).
The 2025 adjustment sets the rate at $53,088 per violation, effective February 2025.

For purposes of VitaCore Inc.'s pre-launch compliance analysis, the 2024 base rate of
**$51,744 per violation** governs.

**Knowing violations** of existing FTC orders attract enhanced scrutiny. The penalty applies
to each separate violation; a single campaign with multiple fake reviews may constitute
multiple violations.

---

## Effective Date Note

This rule became effective **October 21, 2024**. Businesses that were served with an FTC
Notice of Penalty Offenses in 2023 are on notice that similar conduct violates the FTC Act
and may face penalties without a prior order.

---

## Appendix — Sample Compliance Checklist

A business wishing to comply with 16 CFR Part 465 should ensure:

1. No fake or fabricated reviews are created, purchased, or disseminated (§465.2).
2. Insider reviews clearly disclose the material connection (§465.3).
3. Company-controlled review sites clearly identify the relationship (§465.4).
4. No paid social media indicator purchases from non-genuine accounts (§465.5).
5. Review display is not discriminatory (only positive reviews shown) (§465.6).
6. No threats or legal intimidation to suppress reviews (§465.7).
7. No fake social media followers or engagement purchased (§465.8).
""" + appendix_465)

    # .com Disclosures Guidance 2013
    w(WS / "regulatory" / "ftc_dot_com_disclosures_2013.md", """# FTC .com Disclosures: How to Make Effective Disclosures in Digital Advertising (2013)

Source: https://www.ftc.gov/system/files/documents/plain-language/bus41-dot-com-disclosures-information-about-online-advertising.pdf

---

## Overview

This guidance addresses how the FTC's general disclosure principles apply specifically to
digital and online advertising, including social media, mobile platforms, and websites.

---

## The Clear and Conspicuous Standard

A disclosure is "clear and conspicuous" if it is difficult to miss (i.e., easily noticeable)
and if it is easily understandable by ordinary consumers. Whether a disclosure meets this
standard is evaluated by reviewing the totality of the advertisement.

### The Six-Factor Test

1. **Proximity and Placement**: The disclosure should be near the claim it qualifies or
   modifies. Disclosures buried below the fold or at the bottom of a long webpage may
   not be seen by most consumers.

2. **Prominence**: The disclosure should be in a font size and color that makes it
   noticeable relative to the surrounding text.

3. **Distracting Factors**: Avoid surrounding the disclosure with elements (images,
   animations, competing text) that distract attention from it.

4. **Repetition**: If a qualifying claim appears multiple times, the disclosure should
   accompany each repetition or be otherwise unavoidable.

5. **Multimedia**: In video and audio advertising, the disclosure should be both audible
   and visually prominent. A text disclosure on screen simultaneously with competing
   audio may not be sufficient.

6. **Understandable Language**: The disclosure must be in plain language that ordinary
   consumers can understand without industry knowledge.

---

## Social Media Disclosures

### What Works

- **"#ad" or "Ad:" at the beginning of a post**: Placing "#ad" or "Ad:" at the start of
  a social media post (before any promotional content) is generally effective. Consumers
  can see it immediately without scrolling or expanding the text.

- **Verbal disclosure at the opening of a video**: Stating "This video is sponsored by
  [Brand]" in the first few seconds of a video, reinforced by on-screen text, satisfies
  the conspicuous standard.

### What Does Not Work

- **"#ad" buried among hashtags**: A disclosure like "#probiotic #health #wellness #ad
  #supplements #fitness" is inadequate. The "#ad" label is easy to miss among a series
  of topic hashtags.

- **Relying solely on "Paid Partnership" or similar platform tools**: Some platforms offer
  a "Paid Partnership" or "Sponsored" indicator. However, relying solely on these built-in
  platform tools is **insufficient** — studies show many consumers do not notice or
  understand them.

- **Pop-up disclosures**: Pop-up disclosures are often blocked by browsers or dismissed
  without reading. They are not an adequate disclosure mechanism.

- **Hyperlinked disclosures**: Requiring consumers to click a hyperlink to read a
  disclosure is generally not sufficient for material disclosures.

### Space-Constrained Ads

For advertisements in space-constrained formats (e.g., banner ads, short posts), the
advertiser must find a way to include the disclosure anyway. If space genuinely does
not permit an adequate disclosure, the advertisement should be restructured or not run.

---

## Practical Application to Influencer Marketing

When a company pays, provides free products to, or otherwise compensates an influencer:

1. The influencer must disclose the material connection.
2. The disclosure must be clear and conspicuous — not buried.
3. The advertiser is responsible for ensuring compliance, not just the influencer.
4. Ongoing monitoring of influencer posts is expected to catch inadequate disclosures.

---

## Hyperlinks and Landing Pages

If a disclosure is placed on a landing page linked from an advertisement, this is generally
inadequate for material disclosures that relate to the advertisement itself. The disclosure
must accompany the claim it modifies.
""")

    # FTC Health Products Compliance Guidance 2022 (partial, for RCT standard)
    w(WS / "regulatory" / "ftc_health_products_guidance_2022.md", """# FTC Health Products Compliance Guidance (December 2022)

Source: https://www.ftc.gov/business-guidance/resources/health-products-compliance-guidance

**Replaces:** 1998 Dietary Supplements: An Advertising Guide for Industry

---

## Overview

This guidance applies to all health-related products including food, OTC drugs, dietary
supplements, homeopathic products, health devices, diagnostic tests, and applications.

---

## Substantiation Standard for Health Claims

### The Gold Standard: Randomized Controlled Human Clinical Testing (RCT)

For health-related advertising claims, the FTC requires that claims be supported by
**"randomized, controlled human clinical testing (RCT)"** as the gold standard of evidence.

A qualifying RCT must include:
- A control group
- Randomization of subjects
- Double blinding (where applicable)
- Statistically significant AND clinically meaningful results

### Unacceptable Evidence Types (Cannot Standalone)

The following types of evidence, **by themselves**, do not constitute sufficient substantiation
for a health claim:
- Animal studies
- In vitro studies (cell/tissue studies)
- Consumer surveys

These may be supporting evidence, but cannot stand alone as the basis for a health claim.

### Prohibited Qualifying Language

The following modifiers do **not** adequately hedge an unsubstantiated health claim:
- "may"
- "helps"
- "promising"
- "preliminary"
- "initial"
- "pilot"

Using these qualifiers does not make an otherwise unsubstantiated claim compliant.
The claim still requires adequate scientific evidence regardless of these qualifiers.

---

## "Doctor-Formulated" and "Cardiologist Recommended" Claims

Claims such as "Doctor-Formulated" or "Doctor Recommended" are considered health-related
claims that trigger the substantiation analysis. They imply expert endorsement and expert
approval of the product's health efficacy.

Per the FTC's guidance:
1. The "doctor" or expert must be qualified in the relevant discipline.
2. The product must actually meet the standard the expert supposedly endorsed.
3. The claim may imply RCT-level evidence is not needed (expert's professional judgment
   suffices), but the Commission scrutinizes such shortcuts.

**Note**: A claim of "Doctor-Formulated" does not automatically satisfy the substantiation
requirement for the product's underlying health claims (e.g., "supports immune health").
The formula's clinical efficacy must still be substantiated separately.

---

## Penalty Notice Context

In April 2023, the FTC sent Notices of Penalty Offenses to approximately 670 companies
marketing OTC drugs, dietary supplements, and functional foods. Companies that received
these notices cannot later claim they were unaware that their conduct violates the FTC Act.

The five categories of penalty offenses:
1. Lack of competent and reliable evidence supporting product claims
2. Lack of scientific evidence for health or safety claims
3. No well-controlled human clinical trial for disease treatment claims
4. Misrepresentation of the level or type of substantiation
5. False proof claims (claiming "scientifically proven" without sufficient evidence)
""")

    # Advertising substantiation policy
    w(WS / "regulatory" / "ftc_substantiation_policy_full.md", """# FTC Policy Statement Regarding Advertising Substantiation

Source: https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation

---

## Overview

The FTC's substantiation doctrine, articulated in *In re Pfizer Inc.*, 81 F.T.C. 23 (1972),
requires that advertisers have a "reasonable basis" for objective advertising claims before
the claims are made.

---

## The Pfizer Factors (Reasonable Basis Analysis)

The six factors for evaluating whether substantiation is adequate:

**(1) Type of product**
Products with greater consumer risk (e.g., health products, supplements, drugs) require
more rigorous substantiation than low-risk consumer goods.

**(2) Type of claim**
Efficacy claims and health benefit claims require stronger evidence than claims about
product characteristics or comparisons.

**(3) Benefits of a truthful claim**
If the claim provides important benefits to consumers (e.g., health information), higher
substantiation standards may be warranted to ensure accuracy.

**(4) Cost of developing substantiation**
The Commission weighs the cost of obtaining adequate evidence against the consumer harm
from false claims, balancing innovation against consumer protection.

**(5) Consequences of a false claim**
For health and safety claims, the potential harm from a false claim (consumer reliance on
ineffective treatment, delayed treatment) raises the substantiation bar significantly.

**(6) Amount of substantiation experts in the field believe is reasonable**
The Commission considers the consensus of qualified experts in the relevant field when
determining what constitutes adequate evidence.

---

## Application to Dietary Supplements

For dietary supplements making health claims, the "reasonable basis" standard generally
requires the gold standard of competent and reliable scientific evidence — typically one
or more well-designed, well-conducted human clinical trials.

The FTC has consistently held that anecdotal evidence, testimonials, and case studies
alone do not constitute a "reasonable basis" for health benefit claims.

---

## Interaction with FDA Regulations

The FTC's substantiation doctrine operates independently of FDA regulations. A product
that complies with FDA labeling requirements may still violate FTC advertising law if
its advertising claims are not adequately substantiated.

---

## Verbatim Pfizer Factors (For Citation)

From *In re Pfizer*, 81 F.T.C. 23 (1972), the six factors are:

(1) the type of product;
(2) the type of claim;
(3) the benefits of a truthful claim;
(4) the cost of developing substantiation;
(5) the consequences of a false claim;
(6) the amount of substantiation experts in the field believe is reasonable.
""")

    # Green Guides partial (for Q11)
    w(WS / "regulatory" / "ftc_green_guides_260.md", """# 16 CFR Part 260 — Guides for the Use of Environmental Marketing Claims (Green Guides)

Source: https://www.law.cornell.edu/cfr/text/16/part-260

---

## §260.1 — Purpose

These guides apply to environmental claims included in labeling, advertising, promotional
materials, and all other forms of marketing, whether asserted directly or by implication,
through words, symbols, emblems, logos, depictions, product brand names, or through any
other means.

---

## §260.8 — Degradable (including Biodegradable)

(a) **Standard**: An unqualified claim that a product or package is "degradable" or
"biodegradable" should be substantiated by competent and reliable scientific evidence that
the entire product or package will completely break down and return to nature (i.e., decompose
into elements found in nature) within a reasonably short period of time after customary disposal.

(b) **What counts as a "reasonably short time"**: For most solid waste, the Commission
considers one year after customary disposal to be the applicable timeframe.

(c) **Deceptive practice**: Unqualified degradable/biodegradable claims for products typically
disposed of in landfills, incinerators, or recycling facilities are deceptive because these
items do not biodegrade within a reasonably short time in these environments.

(d) **Required qualification**: To avoid deception, a claim of biodegradability must either:
(1) Be limited to contexts where the product will actually biodegrade (e.g., compost),
    with that context clearly stated; or
(2) Be accompanied by competent and reliable scientific evidence that the product degrades
    within one year in the expected disposal environment.

---

## §260.12 — Recyclable

(a) **Standard**: A marketer may claim that a product or package is recyclable if the product
or package can be collected, separated, or otherwise recovered from the solid waste stream
for use in the form of raw materials in the manufacture or assembly of a new package or
product through an established recycling program.

(b) **Substantial majority standard**: An unqualified claim of "recyclable" is deceptive
unless recycling facilities are available to a **substantial majority** of consumers or
communities where the product is sold.

(c) **Definition of substantial majority**: The Commission has defined "substantial majority"
as **60%** of consumers or communities where the item is sold having access to recycling
facilities for the material in question.

(d) **Qualified recyclable claims**: If recycling facilities are not available to 60% of
consumers, the marketer must qualify the claim to explain the limited availability
(e.g., "Recyclable in the 40 communities where curbside recycling is available").

---

## Application to VitaCore ProBio+ Daily

ProBio+ Daily packaging uses:
1. "Eco-friendly packaging" — requires substantiation that the packaging has demonstrably
   lower environmental impact than conventional alternatives.
2. "Biodegradable formula" — requires documentation of degradation within one year under
   customary disposal conditions.
3. "Recyclable" — requires that recycling facilities be available to ≥60% of consumers
   in the markets where the product is sold.
""")


# --------------------------------------------------------------------------- #
# 3. Company files
# --------------------------------------------------------------------------- #
def gen_company_files() -> None:
    w(WS / "company" / "vitacore_company_profile.md", """# VitaCore Inc. — Company Profile

## Overview

VitaCore Inc. is a consumer health supplement startup founded in 2021 and headquartered
in Austin, Texas. The company develops and markets science-backed dietary supplements
targeting the wellness and immunity market segment.

**Flagship product**: ProBio+ Daily — a probiotic + vitamin complex supplement.

**Target market**: Health-conscious adults aged 25–55 in the United States.

**Annual revenue (2025 est.)**: $12.8 million.

**Regulatory posture**: VitaCore received the FTC's Notice of Penalty Offenses (April 2023)
covering substantiation violations, confirming the company is on notice for FTC liability.

---

## Organizational Structure

| Role | Name |
|------|------|
| CEO | Wei Zhang |
| CCO (Chief Compliance Officer) | Jordan Ellis |
| In-House Counsel | Sarah Chen |
| Marketing VP | Mike Torres |
| Social Media Manager | Casey Park |
| Director of R&D | Dr. Priya Nair |

---

## Regulatory History

- **2023**: Received FTC Notice of Penalty Offenses (substantiation).
- **2024**: Internal compliance audit initiated by CCO Jordan Ellis.
- **2026 (planned)**: ProBio+ Daily national launch, pending compliance clearance.

---

## Key Compliance Risks for ProBio+ Daily Launch

1. **Consumer review authenticity**: VitaCore's marketing team previously discussed
   soliciting reviews from employees without disclosure. This triggers §465.3 and §465.5.
2. **Influencer disclosure**: Casey Park manages relationships with 14 paid micro-influencers.
   Current influencer agreements do not specify disclosure language. This may violate §255.5.
3. **Health claims**: Product website uses "may help support immune function" and "promising
   preliminary research" — both flagged as prohibited qualifying language under FTC Health
   Products Guidance.
4. **Made in USA**: Product label states "Made in USA" but ingredient sourcing analysis
   is incomplete.
""")

    w(WS / "company" / "probio_plus_product_spec.md", """# ProBio+ Daily — Product Specification

## Product Description

ProBio+ Daily is a dietary supplement combining probiotic strains with vitamin D3, vitamin C,
and zinc to support gut health and immune function.

**SKU**: VTC-PBD-001
**Form**: Capsule, 30-count bottle
**Serving size**: 2 capsules daily

---

## Active Ingredients

| Ingredient | Amount | Function Claimed |
|-----------|--------|-----------------|
| Lactobacillus acidophilus (NCFM strain) | 10 billion CFU | Supports gut microbiome balance |
| Bifidobacterium longum | 5 billion CFU | Digestive comfort |
| Vitamin D3 (cholecalciferol) | 2000 IU | Immune support |
| Vitamin C (ascorbic acid) | 500 mg | Antioxidant, immune support |
| Zinc (zinc gluconate) | 15 mg | Immune function |

---

## Clinical Evidence Summary (Internal)

| Ingredient | Evidence Type | Meets FTC RCT Standard? |
|-----------|--------------|------------------------|
| L. acidophilus NCFM | 2 RCTs in healthy adults | Yes (for specific claims) |
| B. longum | In vitro + 1 animal study | No — insufficient alone |
| Vitamin D3 | Multiple RCTs | Yes (for immune support) |
| Vitamin C | Multiple RCTs | Yes (for antioxidant claims) |
| Zinc | Multiple RCTs | Yes (for immune function) |

**Note**: B. longum evidence is insufficient for standalone health claims.
"Digestive comfort" claims must be qualified or removed until RCT evidence is available.

---

## Draft Health Claims (Under Review)

The following claims appear in the current press release draft and are under compliance review:

1. "ProBio+ Daily may help support immune function." ← "may help" = prohibited qualifier
2. "Our proprietary blend has shown promising results in preliminary research." ← "promising" + "preliminary" both prohibited
3. "Clinically demonstrated to enhance digestive wellness." ← strong efficacy claim, requires RCT
4. "Doctor-formulated by leading nutritionists." ← triggers expert endorsement + substantiation analysis
5. "Backed by science." ← vague claim, requires specific substantiation identification

---

## Manufacturing

- **Capsule fill and packaging**: Austin, TX facility (domestic)
- **Probiotic ingredients**: Sourced from DuPont (USA) and Chr. Hansen (Denmark)
- **Vitamins**: Sourced primarily from DSM (Netherlands) and Lonza (USA)
- **Bottles and labels**: Manufactured in China (outsourced)

**Made in USA claim viability**: Incomplete. Foreign-sourced ingredients and bottles
represent a risk under 16 CFR Part 323's "all or virtually all" standard.

---

## Packaging Environmental Claims

- "Eco-friendly packaging" (claimed)
- "Biodegradable formula capsules" (claimed)
- "Recyclable bottle" (claimed — recycling availability analysis pending)
""")

    w(WS / "company" / "brand_guidelines.md", """# VitaCore Brand Language Guidelines

## Approved Claim Language

### Acceptable (with proper substantiation)
- "Supports immune health" (with RCT-backed ingredient documentation)
- "May reduce oxidative stress" (antioxidant claims with evidence)
- "Part of a healthy lifestyle" (general wellness)

### Requires Special Review Before Use
- Any claim using "proven," "clinically demonstrated," "scientifically tested"
- Any claim referencing doctor, physician, or medical professional endorsement
- Any claim comparing to pharmaceutical drugs

### Prohibited (Do Not Use in Any Marketing Material)
The following words and phrases are prohibited unless removed or replaced:
- "may help" / "may support" (FTC-prohibited qualifier)
- "promising" (prohibited qualifying language — Health Products Guidance)
- "preliminary" (prohibited qualifying language)
- "initial" (prohibited qualifying language)
- "pilot" (as in "pilot study results show")
- "helps" (as standalone efficacy verb without substantiation)

## Review and Approval Process
All external-facing marketing copy must be reviewed by In-House Counsel (Sarah Chen)
and approved by CCO (Jordan Ellis) before publication.

## Influencer Content Requirements
- All influencer posts must include visible disclosure: "Ad:" or "#ad" at the beginning.
- "Paid Partnership" labels alone are insufficient.
- Review agreements must specify disclosure language.
""")


# --------------------------------------------------------------------------- #
# 4. Drafts (声明草稿，含违规点)
# --------------------------------------------------------------------------- #
def gen_drafts() -> None:
    # Press release draft v1 — contains prohibited qualifiers (A11) and other issues
    w(WS / "drafts" / "press_release_draft_v1.md", """# DRAFT v1 — VitaCore ProBio+ Daily Launch Press Release

**FOR IMMEDIATE RELEASE**

**VitaCore Inc. Introduces ProBio+ Daily: Clinically Demonstrated Support for Immune Health**

Austin, Texas — VitaCore Inc. today announced the commercial launch of ProBio+ Daily,
a revolutionary dietary supplement that may help support immune function and digestive
wellness. The proprietary probiotic-vitamin complex has shown promising results in
preliminary research, demonstrating significant improvements in gut microbiome diversity.

"Our ProBio+ Daily formula is clinically demonstrated to enhance your body's natural
defenses," said Wei Zhang, CEO of VitaCore Inc. "Based on our proprietary blend, we
believe this represents a breakthrough in immune health supplementation."

**Doctor-Formulated for Maximum Efficacy**

ProBio+ Daily was formulated by leading nutritionists and health professionals. The
initial clinical data from our pilot studies shows statistically meaningful improvements
in markers associated with immune function. Our proprietary blend helps strengthen the
gut-immune axis through targeted probiotic colonization.

**Five-Star Reviews from Satisfied Customers**

Thousands of satisfied customers have already tried our products in beta testing.
Here is what they are saying:

"This product changed my life! 5 stars!" — ProBio+ Daily User, Austin TX
"I have never felt better since starting this supplement." — Verified Customer

[Note: The above reviews are from our employee beta testing program. Standard
"Results Not Typical" disclaimer applies to all testimonials.]

**Environmental Commitment**

VitaCore is committed to sustainability. ProBio+ Daily features:
- Eco-friendly packaging
- Biodegradable formula capsules
- Made in USA

For media inquiries, contact: press@vitacore-inc.com

---

*These statements have not been evaluated by the Food and Drug Administration.
This product is not intended to diagnose, treat, cure, or prevent any disease.*
""")

    # Press release draft v2 (will be injected in update_1)
    # Created here as placeholder, overwritten in updates
    w(WS / "drafts" / "ad_copy_social_media.md", """# VitaCore ProBio+ Daily — Social Media Ad Copy

## Influencer Post Templates

### Template A — Micro-Influencer (Casey Park's existing network)

**Instagram Post:**
"Loving my new morning routine with @VitaCore ProBio+ Daily! My gut has never
felt better and my energy is through the roof since I started taking these. Highly
recommend for anyone looking to level up their wellness game! 💪🌿 #probiotics
#guthealth #immunesupport #wellness #vitacore #supplements #healthylifestyle #ad"

*Issue: "#ad" is buried as the last hashtag in a long list. Not adequately conspicuous.*

### Template B — Lifestyle Blogger Partnership

**Blog Post Header:**
"I have been testing VitaCore's ProBio+ Daily for the past 30 days as part of
their ambassador program. Here are my honest thoughts..."

*Issue: No disclosure that compensation was received until end of post.*

### Template C — Celebrity Testimonial (Pending)

"As a physician, I formulated this exact type of product and I can tell you —
ProBio+ Daily is the real deal. [Paid Partnership on Instagram]"

*Issue: (1) Relying on Instagram's "Paid Partnership" label alone is insufficient.
(2) Physician endorsement implies expert opinion that requires substantiation.
Attributed to Dr. [Name Pending], engagement pending contract.*

### Template D — Employee Reviews

**Instructions to Marketing Team:**
"As part of our pre-launch campaign, please leave a 5-star review on our product
listing page. Use your personal accounts (not VitaCore accounts) for authenticity.
No need to disclose you work here — this is just sharing your genuine experience."

*Critical Issue: Soliciting employee reviews without disclosure violates §465.3.*

---

## Disclosure Language Options (Under Review)

### Option 1 (Proposed by Mike Torres):
"#vitacorebrand #ad" — buried in hashtags

### Option 2 (Proposed by Sarah Chen):
"[Paid Partnership with VitaCore Inc.] Ad: I received this product for free in
exchange for my honest review..."

Option 2 is compliant. Option 1 is not. See compliance memo Q2.
""")

    w(WS / "drafts" / "product_label_draft.md", """# ProBio+ Daily — Product Label Draft

## Front Panel

**ProBio+ Daily**
*Probiotic + Vitamin Complex*

"Made in USA" ← Under review for 16 CFR Part 323 compliance

30 Capsules | Dietary Supplement

---

## Back Panel

**Supplement Facts**
Serving Size: 2 Capsules | Servings Per Container: 15

| Ingredient | Amount Per Serving | % Daily Value |
|-----------|-------------------|---------------|
| Vitamin C | 500 mg | 556% |
| Vitamin D3 | 2000 IU (50 mcg) | 250% |
| Zinc | 15 mg | 136% |
| Proprietary Probiotic Blend | 15 Billion CFU | † |

† Daily Value not established.

**Other Ingredients**: Vegetable capsule, microcrystalline cellulose, silica.

---

## Eco-Claims Panel

**Environmental Commitment**
- "Eco-friendly packaging made from recycled materials"
- "Biodegradable capsules"
- "Recyclable PET bottle"

*Note: Recyclability claim requires verification that recycling facilities serve ≥60%
of markets where ProBio+ Daily is sold.*

---

## Disclaimer

These statements have not been evaluated by the Food and Drug Administration.
This product is not intended to diagnose, treat, cure, or prevent any disease.

*Manufactured in Austin, TX | VitaCore Inc., 2026*
""")


# --------------------------------------------------------------------------- #
# 5. Research files
# --------------------------------------------------------------------------- #
def gen_research() -> None:
    w(WS / "research" / "clinical_study_summary.md", """# ProBio+ Daily — Clinical Research Summary

## Summary of Evidence for Each Ingredient/Claim

### 1. L. acidophilus NCFM (10B CFU) — Immune Support

**Available evidence:**
- RCT-1: Smith et al. (2018), Journal of Clinical Gastroenterology.
  Randomized, double-blind, placebo-controlled, n=120 healthy adults, 12 weeks.
  Primary outcome: reduction in frequency of upper respiratory infections.
  Result: Statistically significant (p<0.01) reduction in infection frequency.
  → MEETS FTC RCT STANDARD for "supports immune health" claim.

- RCT-2: Johnson & Lee (2020), Nutrients.
  Randomized, controlled, n=85, 8 weeks.
  Outcome: Gut microbiome diversity scores.
  Result: Statistically significant improvement (p<0.05).
  → MEETS FTC RCT STANDARD for "supports gut microbiome balance" claim.

**FTC Standard Met**: YES for these specific claims.

---

### 2. B. longum — Digestive Comfort

**Available evidence:**
- In vitro study: Chen et al. (2019). Cell culture model of intestinal epithelium.
  Showed bacterial adhesion and anti-inflammatory cytokine modulation.
  → NOT sufficient standalone per FTC guidance (in vitro studies cannot standalone).

- Animal study: Martinez et al. (2021). Mouse model of colitis.
  Showed improvement in inflammation markers.
  → NOT sufficient standalone per FTC guidance (animal studies cannot standalone).

**FTC Standard Met**: NO — insufficient for "digestive comfort" health claim without human RCT.

---

### 3. Vitamin D3 — Immune Support

**Available evidence:**
- Multiple RCTs and meta-analyses. Well-established evidence base.
- Key: Martineau et al. (2017), BMJ meta-analysis of 25 RCTs, n=11,321.
  Result: Vitamin D supplementation significantly reduced risk of acute respiratory infection.
  → MEETS FTC RCT STANDARD.

**FTC Standard Met**: YES.

---

### 4. Vitamin C — Antioxidant/Immune Support

**Available evidence:**
- Hemilä & Chalker (2013), Cochrane Review. Comprehensive meta-analysis.
- Well-established evidence for antioxidant and immune support claims.
  → MEETS FTC RCT STANDARD.

**FTC Standard Met**: YES.

---

### 5. Zinc — Immune Function

**Available evidence:**
- Singh & Das (2011), Cochrane Review.
- Multiple RCTs demonstrating zinc's role in immune function.
  → MEETS FTC RCT STANDARD for immune function support claims.

**FTC Standard Met**: YES.

---

## Summary Table

| Claim | Evidence Type | FTC Standard Met |
|-------|--------------|-----------------|
| "Supports immune health" (L. acidophilus) | 2 RCTs | Yes |
| "Digestive comfort" (B. longum) | in vitro + animal | No |
| "Immune support" (Vitamin D3) | RCT meta-analysis | Yes |
| "Antioxidant" (Vitamin C) | Cochrane Review | Yes |
| "Immune function" (Zinc) | Cochrane Review | Yes |
| "Clinically demonstrated to enhance digestive wellness" | No qualifying RCT for this claim | No |

---

## Critical Gap

The claim "digestive comfort" (associated with B. longum) does **not** have adequate
substantiation under the FTC standard. This ingredient's evidence consists solely of
in vitro and animal studies, which the FTC's Health Products Compliance Guidance (Dec 2022)
explicitly identifies as insufficient standalone evidence.

**Action required**: Remove or substantially qualify the B. longum digestive comfort claim
until a human RCT is completed and demonstrates clinical significance.
""")

    w(WS / "research" / "competitor_analysis.md", _COMPETITOR_ANALYSIS)
    w(WS / "research" / "ingredient_scientific_support.md", _INGREDIENT_ANALYSIS)
    w(WS / "reports" / "ftc_case_law_digest.md", _FTC_CASE_LAW)
    w(WS / "regulatory" / "influencer_policy_procedures.md", _INFLUENCER_POLICY)
    w(WS / "drafts" / "ad_copy_tv_scripts.md", _AD_TV_SCRIPT)
    w(WS / "training" / "compliance_faq_training_manual.md", _COMPLIANCE_FAQ)
    w(WS / "data" / "influencer_post_audit_log.csv", _INFLUENCER_AUDIT_LOG)
    w(WS / "data" / "consumer_review_monitoring_log.csv", _REVIEW_MONITORING_LOG)
    w(WS / "data" / "compliance_issue_tracker.csv", _COMPLIANCE_TRACKER)

    # V5 Decoy: external audit summary with wrong penalty figure
    w(WS / "reports" / "external_audit_summary_DECOY.md", """# External Compliance Audit Summary — ProBio+ Daily Pre-Launch Review

**Prepared by**: (Auto-summarized from Compliance Counsel LLC email – NOT an authoritative document)
**Source**: Summarized by internal reporting bot from email_external_audit.eml
**WARNING**: This is a convenience summary only. Verify all figures against primary sources.

---

## Key Findings (Bot Summary)

### Consumer Review Issues
- **Employee reviews without disclosure**: Critical violation. Requires immediate remediation.
- **Fake/fabricated reviews**: No evidence found of created fake reviews, but the
  current draft template for employee reviews violates §465.3.
- **Review suppression**: No evidence of review suppression at this stage.

### Influencer Disclosure Issues
- **Template A disclosure**: "#ad" buried in hashtags — INADEQUATE under §255.5.
- **Template C disclosure**: Relying on platform "Paid Partnership" tool alone — INADEQUATE.
- **Estimated penalty exposure**: Up to **$45,000 per violation** under FTC Part 465.
  ← [BOT ERROR: This figure is incorrect. See primary source for accurate penalty amount.]

### Doctor-Formulated Claim
- The "Doctor-Formulated" claim in the press release has been tentatively APPROVED
  with conditions: must identify the specific credentialed professional(s).
  ← [This determination is from the first audit letter — see email_external_audit.eml]

### Environmental Claims
- "Biodegradable formula capsules": ADEQUATE — capsule material typically degrades.
  ← [DISPUTED: See §260.8 requirement for one-year degradation evidence]

---

## Critical Note

This document is a bot-generated summary and contains at least one confirmed factual error
(penalty figure). Do not cite this document in compliance reports. Always refer to:
1. Primary regulatory text under `regulatory/`
2. Formal opinion letters under `sessions/email_external_audit.eml`

The $45,000 figure in this document is incorrect. The accurate 2024 civil penalty rate
under 16 CFR Part 465 is found in the primary regulatory document.
""")

    w(WS / "reports" / "prior_audit_findings_2023.md", """# VitaCore Inc. — 2023 Internal Compliance Audit Findings

**Prepared by**: CCO Jordan Ellis
**Date**: December 2023
**Scope**: Advertising and marketing practices for ProBio+ Daily pre-launch review

---

## Summary of Findings

### Category A: Health Claims (HIGH PRIORITY)

1. **A-1**: "Clinically demonstrated to enhance digestive wellness"
   - Status: NON-COMPLIANT
   - Issue: No qualifying RCT supports this specific claim for B. longum component.
   - Recommendation: Remove or replace with qualified language.

2. **A-2**: "May help support immune function"
   - Status: NON-COMPLIANT
   - Issue: "May help" is a prohibited qualifying language per FTC Health Products Guidance.
   - Recommendation: Replace with "Supports immune health" (substantiated by RCT).

3. **A-3**: "Promising preliminary research"
   - Status: NON-COMPLIANT
   - Issue: "Promising" and "preliminary" are both prohibited qualifying terms.
   - Recommendation: Replace with specific evidence citation or remove.

### Category B: Consumer Review Compliance (HIGH PRIORITY)

4. **B-1**: Employee review solicitation
   - Status: NON-COMPLIANT
   - Issue: Soliciting employee reviews without disclosure violates §465.3.
   - Recommendation: All insider reviews must include clear disclosure of employment relationship.

5. **B-2**: Influencer post disclosure
   - Status: NON-COMPLIANT
   - Issue: "#ad" buried in hashtag list does not meet "clear and conspicuous" standard.
   - Recommendation: "#ad" or "Ad:" must appear at beginning of post.

### Category C: Expert Endorsement (MEDIUM PRIORITY)

6. **C-1**: "Doctor-Formulated" claim
   - Status: REQUIRES REVIEW
   - Issue: Claim must identify specific credentialed professional(s).
   - Recommendation: Pending external audit opinion.

### Category D: Environmental Claims (LOW PRIORITY)

7. **D-1**: "Biodegradable formula capsules"
   - Status: REQUIRES DOCUMENTATION
   - Issue: Must provide independent testing showing degradation within one year.
   - Recommendation: Obtain independent test report.

8. **D-2**: "Recyclable" bottle
   - Status: REQUIRES ANALYSIS
   - Issue: Must verify ≥60% of markets have recycling facilities for PET.
   - Recommendation: Commission market-level recycling availability study.

---

## Overall Risk Assessment

Combined penalty exposure from identified violations:
- Consumer review violations: 4 violations × $51,744 = $206,976
- Influencer disclosure violations: 14 influencers × $51,744 = $724,416
- Health claim violations: Estimated 3–6 violations × $51,744 = $155,232–$310,464

**Total estimated exposure**: $1,086,624 – $1,241,856
""")


# --------------------------------------------------------------------------- #
# 6. Sessions (主 + 4 history)
# --------------------------------------------------------------------------- #
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("legal_review_slack", TID)
    s_feishu = gen_session_id("cco_ceo_feishu", TID)
    s_email = gen_session_id("external_counsel_email", TID)
    s_discord = gen_session_id("marketing_discord", TID)

    # Main session
    sb = SessionBuilder(main_id, CWD, "2026-03-09T01:00:00", is_main=True)
    sb.add_user(
        "You are ComplianceOps AI, the compliance assistant for Jordan Ellis (CCO) at VitaCore Inc. "
        "We are conducting the pre-launch compliance review of ProBio+ Daily under FTC regulations, "
        "specifically focusing on consumer review authenticity (16 CFR Part 465) and endorsement "
        "disclosure (16 CFR Part 255).\n\n"
        "The authoritative FTC regulatory texts are under `regulatory/`. The file "
        "`reports/external_audit_summary_DECOY.md` is a bot-generated summary and is NOT "
        "authoritative — it contains known errors. Always verify numbers against primary sources.\n\n"
        "Mandatory output conventions (apply throughout all rounds, even when not restated):\n"
        "- P1: every JSON deliverable MUST contain top-level field `schema_version: \"1.0\"`.\n"
        "- P2: every compliance issue entry MUST contain `ftc_citation` formatted as "
        "\"16 CFR §XXX.X\" (e.g., \"16 CFR §465.2\").\n"
        "- P3: Markdown report headings: H1 = document title, H2 = claim category, H3 = specific "
        "provision. (Active from Q4 feedback onward.)\n"
        "- P4: Prohibited-term replacement tables MUST include a `severity` column "
        "(high/medium/low) per FTC enforcement priority. (Active from Q4 feedback onward.)\n"
        "- P5: All `final/` directory files MUST be named "
        "`{document_type}_final_YYYYMMDD.{ext}`. Reference date: 2026-03-09.\n\n"
        "History sessions: Slack #legal-review (Sarah Chen + Mike Torres), "
        "Feishu DM (CEO Wei Zhang), Email (Compliance Counsel LLC), Discord #marketing (Casey Park).\n\n"
        "Start by reading SOUL.md, USER.md, sessions/session_main_brief.md, then await the first task.")
    sb.add_assistant(
        "Understood. Working framework established:\n"
        "1. Primary authority: regulatory/ documents (16 CFR Part 465, Part 255, Health Products Guidance).\n"
        "2. external_audit_summary_DECOY.md is non-authoritative — will not cite it for figures.\n"
        "3. All JSON deliverables: schema_version=1.0 (P1); ftc_citation per entry (P2).\n"
        "4. Markdown heading hierarchy H1/H2/H3 (P3) and severity column (P4) from Q4 onward.\n"
        "5. final/ files follow {type}_final_YYYYMMDD.{ext} convention (P5).\n"
        "Ready for the first compliance task.")
    sb.write(SESS / f"{main_id}.jsonl")

    # S2 Slack #legal-review — Sarah Chen vs Mike Torres disagreement (V1 conflict)
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2026-03-05T09:00:00",
        [
            ("[Slack #legal-review sarah Mon Mar 05 09:00 EST 2026] I reviewed the current influencer "
             "templates. Template A has '#ad' buried as the last hashtag in a long list. That's a clear "
             "§255.5 violation — the FTC 2023 Guides require the disclosure to be at the beginning of the "
             "post, not buried. The '#ad' in Template A is NOT adequate.",
             "Noted from Sarah. Template A's '#ad' buried in hashtags does not satisfy the §255.5 "
             "clear and conspicuous requirement per the 2023 Endorsement Guides effective July 26, 2023."),
            ("[Slack #legal-review mike Mon Mar 05 09:15 EST 2026] Sarah, I think you're being too strict. "
             "Our internal compliance summary says the penalty exposure is only $45,000 per violation. "
             "If the risk is that low, maybe we don't need to overhaul all 14 influencer agreements. "
             "Let's just add a note to the post.",
             "Flagging Mike's citation: the figure '$45,000 per violation' does NOT match the primary "
             "regulatory source. The DECOY summary contains this error. I will verify against "
             "regulatory/ftc_consumer_reviews_rule_465.md before any penalty figures are used in reports."),
            ("[Slack #legal-review sarah Mon Mar 05 09:30 EST 2026] Mike, that $45,000 figure is wrong. "
             "Check the actual regulation — 16 CFR Part 465 clearly states $51,744 per violation "
             "(2024 rate). With 14 influencer agreements non-compliant, exposure is $51,744 × 14 = $724,416. "
             "This is material. And note: 'Results Not Typical' disclaimers are also NOT a safe harbor — "
             "that was abolished in 2009. The press release v1 can't use that either.",
             "Sarah is correct: $51,744 per violation (2024 base rate per 16 CFR Part 465). "
             "Mike's $45,000 figure is from the DECOY summary and is erroneous. "
             "Also confirmed: 'Results Not Typical' is not a safe harbor — abolished in 2009 revision, "
             "not restored in 2023. The press release v1 note about 'Results Not Typical' must be removed."),
            ("[Slack #legal-review mike Mon Mar 05 10:00 EST 2026] OK fine, I'll defer to Sarah on the "
             "penalty number. But I still think the 'Doctor-Formulated' claim is fine — we have Dr. Nair "
             "on our team and she reviewed the formula.",
             "Recorded: Mike defers to $51,744 on penalty. The 'Doctor-Formulated' question is separate — "
             "it turns on whether the physician endorsement is disclosed and whether it implies efficacy "
             "claims that require additional substantiation. Flagged for external audit review."),
        ])

    # S3 Feishu DM — CEO Wei Zhang
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2026-03-06T10:00:00",
        [
            ("[Feishu Wei Zhang Wed Mar 06 10:00 EST 2026] Jordan, I reviewed the compliance issues. "
             "I want us to keep 'clinically demonstrated to support immune function' in the press release. "
             "My lawyer friend from a small firm in Delaware said it's fine because we have RCT data for "
             "L. acidophilus. Also, he said we can use 'Doctor-Formulated' without issues because Dr. Nair "
             "is a legitimate nutritionist. Please update the compliance analysis accordingly. "
             "(ref: CEO-DIR-20260306-01)",
             "Received CEO directive (CEO-DIR-20260306-01). Recording for audit trail. Note: "
             "CEO informal guidance does not constitute a legal determination under FTC law. "
             "The compliance analysis will be based on 16 CFR Part 255 and Health Products Guidance, "
             "not informal attorney opinion. CEO's direction will be escalated to CCO Jordan Ellis "
             "for review before any change to compliance conclusions."),
            ("[Feishu Wei Zhang Wed Mar 06 10:30 EST 2026] Also, I want employee reviews to go up on "
             "our Amazon listing before launch. Our employees love the product and their reviews would "
             "help us get initial traction. Just have them post as regular customers.",
             "CRITICAL COMPLIANCE FLAG: Directing employees to post reviews without disclosing their "
             "employment relationship violates 16 CFR §465.3 (insider reviews). This practice cannot "
             "proceed. Even genuine employee reviews must clearly and conspicuously disclose the "
             "employment relationship. This item requires immediate CCO intervention."),
        ])

    # S4 Email — External audit (first letter, contains V6 red herring: 2009 "Results Not Typical" safe harbor)
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2026-03-07T09:00:00",
        [
            ("[Email alex.rivera@compliancecounsel.com → jordan.ellis@vitacore Mar 07 09:00 EST 2026] "
             "Subject: ProBio+ Daily Pre-Launch Compliance Opinion — Initial Review\n\n"
             "Dear Jordan,\n\n"
             "We have completed our initial review of the ProBio+ Daily launch materials. "
             "Summary of our findings:\n\n"
             "1. CONSUMER REVIEWS (16 CFR Part 465, eff. Oct 21, 2024):\n"
             "   - Employee review solicitation: VIOLATION. Insider reviews require clear disclosure.\n"
             "   - Penalty exposure: $51,744 per violation (2024 rate).\n\n"
             "2. INFLUENCER DISCLOSURES (16 CFR Part 255, eff. Jul 26, 2023):\n"
             "   - Template A ('#ad' in hashtag list): INADEQUATE.\n"
             "   - Template C (platform Paid Partnership tool only): INADEQUATE.\n\n"
             "3. TESTIMONIALS — 'RESULTS NOT TYPICAL' DISCLAIMER:\n"
             "   - Regarding the press release footnote applying a 'Results Not Typical' disclaimer:\n"
             "   - NOTE: Based on the original 1980 Endorsement Guides, 'Results Not Typical' "
             "served as a safe harbor for atypical testimonials.\n"
             "   - RECOMMENDATION: Include 'Results Not Typical' disclaimer for all testimonials.\n"
             "   ← [CAUTION: This recommendation is based on the 1980 Guides. The safe harbor "
             "was abolished in the 2009 revision. This recommendation is SUPERSEDED LAW.]\n\n"
             "4. 'DOCTOR-FORMULATED' CLAIM:\n"
             "   - Conditionally PERMITTED: If VitaCore identifies the specific credentialed "
             "professional(s) and the professional's credentials are verified, this claim is "
             "acceptable per §255.3 expert endorsement provisions.\n"
             "   - No additional RCT required beyond the current evidence base for this label claim.\n\n"
             "Regards,\nAlex Rivera, Compliance Counsel LLC",
             "Received first external audit opinion letter (March 7, 2026). Key observations:\n"
             "1. Confirms §465.3 violation and correct penalty figure ($51,744).\n"
             "2. Confirms Template A and C disclosure inadequacies.\n"
             "3. CRITICAL FLAG: The 'Results Not Typical' recommendation (#3) is based on "
             "the 1980 Endorsement Guides. This safe harbor was ABOLISHED in the 2009 revision "
             "and has not been restored. This recommendation constitutes superseded law (V6 red herring) "
             "and must NOT be followed.\n"
             "4. 'Doctor-Formulated' conditionally permitted — subject to further review."),
        ])

    # S5 Discord #marketing — Casey Park + CEO annotation
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, CWD, "2026-03-08T14:00:00",
        [
            ("[Discord #marketing casey Sat Mar 08 14:00 EST 2026] Hey team, just checking on "
             "the influencer script status. We have 14 influencers ready to post next week. "
             "I shared a draft script using the old template (results not typical disclaimer) "
             "since that's what our legal team used before. Should I proceed?",
             "HOLD: The 'Results Not Typical' disclaimer approach in the old template is NOT "
             "a valid safe harbor under current FTC rules. It was abolished in 2009. "
             "New disclosure approach required — specifically '#ad' or 'Ad:' at the beginning "
             "of each post, before any promotional content."),
            ("[Discord #marketing wei_zhang_ceo Sat Mar 08 14:20 EST 2026] @casey — I annotated "
             "the old draft script (attached as discord_draft_v1.md). I changed 'Results Not Typical' "
             "to 'Doctor-Recommended Formula' to sound more credible. This should work fine without "
             "additional disclosures for the doctor endorsement claim. (This is CEO Wei Zhang.)",
             "Flagged: CEO's annotation adds 'Doctor-Recommended Formula' claim, which triggers "
             "§255.3 expert endorsement requirements. If used, this claim requires: "
             "(1) named, credentialed professional; (2) professional's genuine endorsement; "
             "(3) material connection disclosed if payment exists. CEO's informal instruction "
             "does not override regulatory requirements."),
            ("[Discord #marketing casey Sat Mar 08 14:45 EST 2026] Got it. I also noticed the "
             "old template references a study from 2009 citing 'substantial scientific evidence' "
             "requirements from the 1998 Dietary Supplements guide. Is that still current?",
             "No. The 1998 Dietary Supplements: An Advertising Guide for Industry has been "
             "replaced by the FTC Health Products Compliance Guidance (December 2022). "
             "The 2022 guidance is the current authority. References to the 1998 guide "
             "are superseded and should not be cited."),
        ])

    return {
        "main": main_id,
        "history": [(s_slack, "slack"), (s_feishu, "feishu"),
                    (s_email, "email"), (s_discord, "discord")],
    }


# --------------------------------------------------------------------------- #
# 7. Updates (含 supersede)
# --------------------------------------------------------------------------- #
def _gen_supplemental_influencer_posts_csv() -> str:
    """Generate ~35k token supplemental influencer post dataset for update 1."""
    rng = random.Random(20260312)
    handles = [
        "@wellnesswithjenna", "@guthealth_guru", "@probiotic_life", "@nourishednaturally",
        "@vitamindiary", "@microbiome_maven", "@supplementspro", "@holistic_health_hub",
        "@fitandfueled", "@cleanwellness", "@digestive_digest", "@immunity_insider",
        "@nutriscience", "@vitalitycoach",
    ]
    platforms = ["Instagram", "TikTok", "YouTube", "Instagram Stories", "Reels", "Twitter/X",
                 "LinkedIn", "Pinterest", "Facebook", "Snapchat"]
    disclosure_patterns = [
        "#ad buried as last hashtag", "No disclosure", "#ad at post beginning",
        "Platform Paid Partnership only", "Ad: at beginning", "#sponsored in middle",
        "Verbal only (video)", "#ad first hashtag", "Disclosure in bio only",
        "Disclosure at post end", "No disclosure (first post)", "#gifted in hashtags",
        "Paid collab sticker only", "AD text overlay (video)", "FTC compliant verbal + text",
    ]
    health_claim_texts = [
        "Supports immune health (compliant with RCT)", "may help immune function (PROHIBITED: 'may')",
        "Clinically demonstrated to enhance immunity (PROHIBITED: requires RCT for all ingredients)",
        "No health claim made (compliant)", "promising results in gut health (PROHIBITED: 'promising')",
        "Doctor recommended for gut wellness (REQUIRES expert disclosure §255.3)",
        "Gut health support tested in human trials (compliant)", "preliminary research suggests (PROHIBITED)",
        "Helps strengthen immunity (PROHIBITED: 'helps')", "supports gut microbiome balance (compliant)",
        "may help digestive comfort (PROHIBITED: 'may' + B. longum lacks RCT)",
        "B. longum promotes digestive wellness (insufficient evidence - no human RCT)",
        "Vitamin D3 supports immune function (compliant - RCT supported)",
        "L. acidophilus NCFM for immune health (compliant - 2 human RCTs)",
        "ProBio+ clinically studied for immunity (compliant phrasing)",
        "initial pilot data shows gut improvement (PROHIBITED: 'initial' + 'pilot')",
        "Science-backed probiotic formula (compliant general claim)",
        "Probiotic of choice for digestive health (compliant general claim)",
        "Results Not Typical disclaimer applies (OBSOLETE safe harbor - abolished 2009)",
        "Doctor-Formulated for immunity (REQUIRES substantiation per revised audit letter)",
    ]
    resolution_actions = [
        "UPDATE DISCLOSURE", "REMOVE CLAIM", "OBTAIN LEGAL REVIEW", "ESCALATE TO CCO",
        "INFLUENCER NOTIFIED", "CONTRACT UPDATED", "COMPLIANT - NO ACTION", "MONITORING",
        "PENDING REVIEW", "FORMAL NOTICE ISSUED",
    ]

    # Extended fields for richer data
    lines = [
        "post_id,handle,platform,post_date,post_time_est,follower_count,impressions,"
        "engagement_rate,reach,clicks,link_clicks,saves,shares,comments,likes,"
        "disclosure_pattern,disclosure_type,disclosure_timing,compliance_status,"
        "health_claim_detected,health_claim_category,health_claim_compliant,"
        "violation_category,penalty_exposure_usd,review_date,reviewer,resolution_status,"
        "resolution_action,resolution_date,legal_hold,notes,campaign_id,content_type,"
        "paid_partnership_tag,verbal_disclosure,visual_disclosure"
    ]

    campaign_ids = [f"CAMP-2026-{i:03d}" for i in range(1, 20)]
    content_types = ["Static image", "Carousel", "Short video (<60s)", "Long video (>60s)",
                     "Story", "Reel", "Live session", "Blog post", "Podcast mention"]

    for i in range(1, 1401):
        handle = rng.choice(handles)
        platform = rng.choice(platforms)
        month = rng.randint(1, 3)
        day = rng.randint(1, 28)
        hour = rng.randint(7, 23)
        minute = rng.choice([0, 15, 30, 45])
        followers = rng.randint(10000, 120000)
        impressions = int(followers * rng.uniform(0.1, 0.55))
        reach = int(impressions * rng.uniform(0.7, 1.1))
        engagement = round(rng.uniform(0.5, 7.5), 2)
        clicks = int(impressions * rng.uniform(0.005, 0.08))
        link_clicks = int(clicks * rng.uniform(0.1, 0.6))
        saves = int(impressions * rng.uniform(0.001, 0.03))
        shares = int(impressions * rng.uniform(0.001, 0.015))
        comments = int(impressions * rng.uniform(0.002, 0.04))
        likes = int(impressions * rng.uniform(0.02, 0.15))
        disc_idx = rng.randint(0, len(disclosure_patterns) - 1)
        disc = disclosure_patterns[disc_idx]
        is_compliant = disc_idx in (2, 4, 6, 7, 14)
        disc_type = "adequate" if is_compliant else "inadequate"
        disc_timing = "pre-content" if is_compliant else "post-content or absent"
        comp_status = "COMPLIANT" if is_compliant else "NON-COMPLIANT"
        claim = rng.choice(health_claim_texts)
        claim_cat = "health_efficacy" if "RCT" in claim or "immune" in claim.lower() else "general_wellness"
        claim_ok = "Yes" if "(compliant" in claim else "No"
        violation_cat = "§255.5" if not is_compliant else "None"
        penalty = 51744 if not is_compliant else 0
        review_month = min(month + 1, 3)
        reviewer = rng.choice(["Jordan Ellis", "Sarah Chen", "Casey Park", "Alex Rivera (Ext.)"])
        res_status = "RESOLVED" if is_compliant else rng.choice(["PENDING", "OPEN", "IN_REVIEW"])
        res_action = "NONE" if is_compliant else rng.choice(resolution_actions[:8])
        res_date = f"2026-{review_month:02d}-{min(day+7, 28):02d}" if is_compliant else "N/A"
        legal_hold = "No"
        note = rng.choice([
            "Supplemental audit batch March 2026",
            "Post-CEO-retraction review round",
            "Influencer remediation tracking",
            "Post-update-1 compliance sweep",
            "Quarterly disclosure audit",
            "Sarah Chen escalation review",
            "Casey Park pre-launch clearance",
        ])
        campaign = rng.choice(campaign_ids)
        ctype = rng.choice(content_types)
        paid_tag = "Yes" if "Paid Partnership" in disc else "No"
        verbal = "Yes" if "Verbal" in disc else "No"
        visual = "Yes" if "Ad:" in disc or "#ad" in disc.lower() else "No"

        lines.append(
            f"SUPP-{i:04d},{handle},{platform},2026-{month:02d}-{day:02d},"
            f"{hour:02d}:{minute:02d}:00,{followers},{impressions},{engagement},"
            f"{reach},{clicks},{link_clicks},{saves},{shares},{comments},{likes},"
            f"\"{disc}\",{disc_type},{disc_timing},{comp_status},"
            f"\"{claim}\",{claim_cat},{claim_ok},"
            f"{violation_cat},{penalty},2026-{review_month:02d}-{min(day+3,28):02d},"
            f"{reviewer},{res_status},{res_action},{res_date},{legal_hold},"
            f"\"{note}\",{campaign},{ctype},{paid_tag},{verbal},{visual}"
        )

    return "\n".join(lines) + "\n"


def _gen_supplemental_review_analysis_csv() -> str:
    """Generate ~35k token supplemental review analysis dataset for update 2."""
    rng = random.Random(20260319)
    platforms = ["Amazon", "iHerb", "Vitacore.com", "Walmart.com", "Google Reviews",
                 "Yelp", "Trustpilot", "Reddit", "Facebook", "App Store", "CVS.com",
                 "Target.com", "Costco.com", "Whole Foods", "Sprouts", "Chewy",
                 "Instagram Review", "TikTok Comment", "YouTube Comment", "Twitter/X"]
    violation_types = [
        "None", "None", "None", "None", "None",
        "§465.3 — Insider review (employee account detected)",
        "§465.2 — Suspected fake review (AI-generated text pattern)",
        "§465.6 — Review suppression candidate (negative review hidden)",
        "§465.7 — Reviewer reports legal threat received",
        "§465.5 — Reviewer appears to be social media bot (fake account)",
        "§465.2 — Review claims product cures disease (false representation)",
        "§465.3 — Family member of employee (immediate family disclosure required)",
        "§465.4 — Company-controlled review site not disclosed",
        "§465.2 — Review paid for via third-party mill",
        "§465.5 — Coordinated review pattern (same IP address cluster)",
    ]
    action_types = ["No action", "Investigation opened", "Platform reported", "Legal hold",
                    "Review removed (with cause)", "Consent order monitoring", "Escalated to CCO",
                    "External counsel notified", "FTC voluntary disclosure prepared"]
    outcomes = ["No violation confirmed", "Violation confirmed", "Platform notified",
                "Disclosure added", "Review removed", "Settlement negotiated",
                "Monitoring ongoing", "Referral to enforcement", "Training triggered"]

    lines = [
        "review_id,platform,review_date,star_rating,reviewer_handle,reviewer_account_age_days,"
        "review_text_length,verified_purchase,num_helpful_votes,num_not_helpful_votes,"
        "suspected_violation_type,violation_confidence,violation_evidence,"
        "action_taken,action_date,penalty_exposure_usd,investigated_by,"
        "investigation_date,outcome,outcome_date,appeal_filed,notes,"
        "ip_cluster_id,device_type,country,state,review_source_type,"
        "contains_brand_comparison,contains_health_claim,health_claim_type,"
        "review_sentiment_score,verified_reviewer_age_months"
    ]

    for i in range(1, 1001):
        platform = rng.choice(platforms)
        month = rng.randint(10, 12) if rng.random() > 0.3 else rng.randint(1, 3)
        year = 2024 if month >= 10 else 2025
        day = rng.randint(1, 28)
        stars = rng.choices([1, 2, 3, 4, 5], weights=[8, 7, 10, 30, 45])[0]
        reviewer = f"customer_{rng.randint(10000, 99999)}"
        acct_age = rng.randint(30, 3650)
        text_len = rng.randint(50, 850)
        verified = rng.choice(["Yes", "No", "Yes", "Yes"])
        helpful = rng.randint(0, 45)
        not_helpful = rng.randint(0, 12)
        viol = rng.choices(violation_types, weights=[5, 5, 5, 5, 5, 2, 2, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5])[0]
        viol_confidence = "HIGH" if viol != "None" and rng.random() > 0.4 else ("MEDIUM" if viol != "None" else "N/A")
        viol_evidence = "Pattern analysis + IP correlation" if viol != "None" else "N/A"
        action = rng.choice(action_types) if viol != "None" else "No action"
        action_month = min(month + 1, 12)
        penalty = 51744 if viol not in ("None", "") else 0
        investigator = rng.choice(["Jordan Ellis", "Sarah Chen", "Alex Rivera (Ext.)", "Casey Park"])
        invest_month = min(month + 1, 12)
        outcome = rng.choice(outcomes) if viol != "None" else "No violation confirmed"
        outcome_month = min(invest_month + 1, 12)
        appeal = "No" if rng.random() > 0.05 else "Yes"
        note = rng.choice([
            "Post-launch monitoring wave 1",
            "Supplemental review audit (Update 2 batch)",
            "External counsel review triggered",
            "Doctor-Formulated claim context analysis",
            "Biodegradable claim review",
            "Employee review sweep",
            "Third-party platform audit",
        ])
        ip_cluster = f"CL-{rng.randint(1000, 9999)}" if viol != "None" else "N/A"
        device = rng.choice(["Mobile", "Desktop", "Tablet", "Unknown"])
        country = rng.choices(["US", "CA", "UK", "AU", "DE"], weights=[80, 8, 5, 4, 3])[0]
        state = rng.choice(["CA", "NY", "TX", "FL", "IL", "WA", "GA", "MA", "PA", "CO", "N/A"])
        src = rng.choice(["organic", "invited", "incentivized", "unknown", "organic", "organic"])
        has_comparison = rng.choice(["Yes", "No", "No", "No"])
        has_health = rng.choice(["Yes", "No", "No", "Yes", "No"])
        health_type = rng.choice(["immune", "digestive", "general_wellness", "N/A", "N/A"]) if has_health == "Yes" else "N/A"
        sentiment = round(rng.uniform(-1.0, 1.0), 3)
        reviewer_months = acct_age // 30

        lines.append(
            f"SREV-{i:04d},{platform},{year}-{month:02d}-{day:02d},{stars},"
            f"{reviewer},{acct_age},{text_len},{verified},{helpful},{not_helpful},"
            f"\"{viol}\",{viol_confidence},\"{viol_evidence}\","
            f"\"{action}\",{year}-{action_month:02d}-{min(day+5,28):02d},{penalty},"
            f"{investigator},{year}-{invest_month:02d}-{min(day+7,28):02d},"
            f"\"{outcome}\",{year}-{outcome_month:02d}-{min(day+14,28):02d},"
            f"{appeal},\"{note}\",{ip_cluster},{device},{country},{state},"
            f"{src},{has_comparison},{has_health},{health_type},{sentiment},{reviewer_months}"
        )

    return "\n".join(lines) + "\n"


def gen_updates(sess_ids: dict) -> dict:
    s_feishu = sess_ids["history"][1][0]
    s_email = sess_ids["history"][2][0]

    # UPDATE 1 (after Q7, before Q8): CEO撤回 + Slack legal 确认
    # CEO via Feishu retracts "clinically demonstrated" and acknowledges §465.3 issue
    u1_feishu_id = gen_session_id("cco_ceo_feishu_upd1", TID)
    sb_u1 = SessionBuilder(u1_feishu_id, CWD, "2026-03-12T09:00:00", is_main=False)
    sb_u1.add_user(
        "[Feishu Wei Zhang Thu Mar 12 09:00 EST 2026] Jordan, I spoke with our board attorney "
        "this morning. She confirmed that 'clinically demonstrated' language in the press release "
        "is too strong — it implies proven efficacy that we need RCT-level evidence for across "
        "all claimed benefits. I am formally retracting my earlier directive (CEO-DIR-20260306-01). "
        "Please mark 'clinically demonstrated' as a VIOLATION in the compliance analysis and "
        "update the draft to 'supports immune health' instead. "
        "Additionally, I withdraw the employee review request — I understand it violates §465.3. "
        "The 'Doctor-Formulated' claim may remain subject to proper naming disclosure. "
        "(ref: CEO-RETRACT-20260312-01 — SUPERSEDES CEO-DIR-20260306-01)")
    sb_u1.add_assistant(
        "CEO retraction received and recorded (CEO-RETRACT-20260312-01). This SUPERSEDES "
        "CEO-DIR-20260306-01. Effects on compliance analysis:\n"
        "1. 'Clinically demonstrated' → re-flagged as VIOLATION (consistent with FTC standards).\n"
        "2. Employee review program → confirmed abandoned; §465.3 violation risk eliminated.\n"
        "3. 'Doctor-Formulated' → remains subject to §255.3 expert endorsement requirements.\n"
        "Q8 must reflect that 'clinically demonstrated' is now unambiguously a violation.")
    sb_u1.write(UPD / "upd1_sessions" / f"{u1_feishu_id}.jsonl")

    # Slack legal update 1 — Sarah confirms 2009 safe harbor abolition
    u1_slack_id = gen_session_id("legal_review_slack_upd1", TID)
    sb_u1s = SessionBuilder(u1_slack_id, CWD, "2026-03-12T10:00:00", is_main=False)
    sb_u1s.add_user(
        "[Slack #legal-review sarah Thu Mar 12 10:00 EST 2026] Quick update: I reviewed the "
        "external audit letter. Their recommendation to use 'Results Not Typical' is wrong. "
        "That safe harbor was definitively abolished in the 2009 revision to the Endorsement "
        "Guides and has NOT been restored in the 2023 revision. Section §255.2 now requires "
        "advertisers to prove what results consumers generally achieve, not merely disclaim "
        "atypical results. Any compliance report should categorize the 'Results Not Typical' "
        "recommendation from the first audit letter as superseded law and discard it.")
    sb_u1s.add_assistant(
        "Confirmed. The first audit letter's 'Results Not Typical' recommendation is based "
        "on the 1980/pre-2009 Guides and constitutes superseded law. Per §255.2 (2023), "
        "the safe harbor no longer exists. This will be classified as a superseded_recommendation "
        "in Q10 output (along with any reliance on the 1998 Dietary Supplements Guide).")
    sb_u1s.write(UPD / "upd1_sessions" / f"{u1_slack_id}.jsonl")

    # UPDATE 1 workspace: press_release_draft_v2 + influencer_policy_v2 + ftc_case_digest_v2
    w(UPD / "upd1_workspace" / "press_release_draft_v2.md", """# DRAFT v2 — VitaCore ProBio+ Daily Launch Press Release
# (Revised per CEO-RETRACT-20260312-01 and Compliance Review)

**FOR IMMEDIATE RELEASE**

**VitaCore Inc. Introduces ProBio+ Daily: Science-Backed Support for Immune Health**

Austin, Texas — VitaCore Inc. today announced the commercial launch of ProBio+ Daily,
a dietary supplement combining clinically studied probiotic strains with essential vitamins
and minerals to support immune health and gut microbiome balance.

"ProBio+ Daily is formulated based on published human clinical research demonstrating
support for immune health," said Wei Zhang, CEO of VitaCore Inc.

**Formulated by Our R&D Team**

ProBio+ Daily was developed by VitaCore's internal research and development team, led by
Dr. Priya Nair, PhD, a credentialed nutrition scientist.

[PENDING: Dr. Nair disclosure language — must identify role and any compensation]

**Customer Experience Program**

VitaCore will be partnering with independent customers to gather real-world testimonials.
All testimonials will comply with FTC disclosure requirements.

[Note: Employee review program withdrawn. All reviews will be from independent consumers
with appropriate disclosures as required by 16 CFR Part 465.]

**Environmental Commitment**

ProBio+ Daily features packaging designed with sustainability in mind.
[Note: Environmental claims under independent verification — see compliance review Q11.]

---

*These statements have not been evaluated by the Food and Drug Administration.
This product is not intended to diagnose, treat, cure, or prevent any disease.*
""")
    # Large volume documents for update 1 (to meet 30k+ token target)
    w(UPD / "upd1_workspace" / "influencer_post_audit_supplemental.csv",
      _gen_supplemental_influencer_posts_csv())

    # UPDATE 2 (after Q11, before Q12): External audit revised letter + enforcement cases
    # This supersedes: (a) first audit letter's Doctor-Formulated conditional permit;
    # (b) CEO's informal guidance on Doctor-Formulated
    email_revised_content = """From: alex.rivera@compliancecounsel.com
To: jordan.ellis@vitacore.com
Subject: REVISED OPINION — ProBio+ Daily Pre-Launch Compliance (SUPERSEDES March 7 Letter)
Date: Thu, 19 Mar 2026 09:00:00 -0500

Dear Jordan,

After further review and consultation with FTC enforcement precedents, we must REVISE
our March 7, 2026 opinion letter in one critical respect.

RETRACTION AND REVISION:

Our March 7 letter conditionally permitted the "Doctor-Formulated" claim (item 4 of
that letter), subject to identification of specific credentialed professional(s).

We now revise this position as follows:

SUPERSEDED POSITION (March 7 letter):
"Doctor-Formulated" conditionally permitted with identification of credentials.

REVISED POSITION:
The claim "Doctor-Formulated" is a HEALTH CLAIM that triggers the FTC's
substantiation analysis under Health Products Compliance Guidance (Dec 2022).
The Commission has made clear that "doctor recommended" or "doctor formulated" claims
imply expert endorsement of the product's efficacy — not merely its safety or quality.
Under the FTC's reasonable basis standard, this requires:

(1) SUBSTANTIAL COMPETENT SCIENTIFIC EVIDENCE — specifically, the evidence standard
    expected for the health claims the "Doctor-Formulated" label implies.

(2) Since the product claims immune support and gut health benefits, the underlying
    claims must be supported by randomized controlled human clinical trials (RCT)
    for all ingredients associated with those benefits.

(3) B. longum's "digestive comfort" claim lacks qualifying RCT evidence.
    Therefore, "Doctor-Formulated" cannot be used to imply endorsement of this
    specific benefit without misleading consumers.

RECOMMENDATION:
"Doctor-Formulated" may be used only if:
(a) The specific professional is named and credentialed;
(b) The professional's endorsement scope is clearly limited to claims that have
    RCT support; and
(c) The B. longum digestive comfort claim is removed from the label, OR a qualifying
    human RCT is completed.

Absent these conditions, the claim requires_substantiation: true and must be flagged
as a potential violation pending completion of a qualifying RCT.

ADDITIONAL REVISION — BIODEGRADABLE CLAIM:
Our March 7 summary (via bot summary document) noted "biodegradable" as potentially
adequate. We now note: Per 16 CFR §260.8, a "biodegradable" claim requires independent
testing documentation demonstrating complete degradation within one year under customary
disposal conditions. A test report from an accredited laboratory is required.

This letter SUPERSEDES our March 7, 2026 opinion as to items 4 (Doctor-Formulated)
and the biodegradable claim assessment.

The update_source for your compliance records should be recorded as: email_revised_audit_v2

Regards,
Alex Rivera, Compliance Counsel LLC

"""
    w(UPD / "upd2_workspace" / "email_revised_audit_v2.eml", email_revised_content)

    # FTC enforcement cases 2024 (large document to meet token target)
    enforcement_cases = _gen_enforcement_cases_doc()
    w(UPD / "upd2_workspace" / "ftc_enforcement_cases_2024.md", enforcement_cases)

    # Green claims test reports
    green_reports = _gen_green_claims_report()
    w(UPD / "upd2_workspace" / "green_claims_test_reports.md", green_reports)

    # Large supplemental review analysis dataset for update 2 (to meet 30k+ token target)
    w(UPD / "upd2_workspace" / "consumer_review_analysis_supplemental.csv",
      _gen_supplemental_review_analysis_csv())

    updates_decl = {
        "upd1_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd1_sessions",
            "files": [
                {"name": f"{u1_feishu_id}.jsonl", "action": "new",
                 "target": f"{u1_feishu_id}.jsonl", "channel": "feishu"},
                {"name": f"{u1_slack_id}.jsonl", "action": "new",
                 "target": f"{u1_slack_id}.jsonl", "channel": "slack"},
            ],
        },
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {"name": "press_release_draft_v2.md", "action": "new",
                 "target": "drafts/press_release_draft_v2.md"},
                {"name": "influencer_post_audit_supplemental.csv", "action": "new",
                 "target": "data/influencer_post_audit_supplemental.csv"},
            ],
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "email_revised_audit_v2.eml", "action": "new",
                 "target": "sessions/email_revised_audit_v2.eml"},
                {"name": "ftc_enforcement_cases_2024.md", "action": "new",
                 "target": "regulatory/ftc_enforcement_cases_2024.md"},
                {"name": "green_claims_test_reports.md", "action": "new",
                 "target": "research/green_claims_test_reports.md"},
                {"name": "consumer_review_analysis_supplemental.csv", "action": "new",
                 "target": "data/consumer_review_analysis_supplemental.csv"},
            ],
        },
    }
    return updates_decl


def _gen_enforcement_cases_doc() -> str:
    """Generate a ~30KB FTC enforcement cases 2024 document."""
    rng = random.Random(465)

    def fake_company():
        prefixes = ["Vitality", "NutriCore", "BioWell", "PurePath", "NaturePlus",
                    "HealthFirst", "OrganicEdge", "WellnessMax", "PrimeBio", "CleanLabel"]
        suffixes = ["Inc.", "LLC", "Corp.", "Health", "Solutions", "Brands", "Naturals"]
        return rng.choice(prefixes) + " " + rng.choice(suffixes)

    def fake_violation():
        types = [
            "Fake consumer reviews — purchased via third-party review mill",
            "Insider reviews without disclosure — employees posting as customers",
            "Suppression of negative reviews — displaying only 4+ star ratings",
            "Fabricated testimonials — AI-generated reviewer personas",
            "Undisclosed influencer relationships — no '#ad' disclosure",
            "'Paid Partnership' label only — insufficient for material connection disclosure",
            "Fake social media followers — purchased from offshore bot farms",
            "Review intimidation — threatening negative reviewers with legal action",
        ]
        return rng.choice(types)

    cases = []
    base_year = 2024

    for i in range(1, 45):
        company = fake_company()
        penalty = rng.choice([51744, 103488, 206976, 310464, 517440, 724416, 1034880])
        violations = rng.randint(1, 8)
        month = rng.randint(1, 12)
        day = rng.randint(1, 28)
        product = rng.choice(["dietary supplement", "probiotic supplement", "vitamin complex",
                               "weight loss supplement", "immune support formula"])
        violation_desc = fake_violation()
        cases.append(
            f"### Case {i}: FTC v. {company} ({base_year}-{month:02d}-{day:02d})\n\n"
            f"**Product**: {product}\n"
            f"**Violation**: {violation_desc}\n"
            f"**Number of violations**: {violations}\n"
            f"**Civil penalty**: ${penalty:,} (${51744} per violation × {violations})\n"
            f"**Settlement**: Consent order with prohibition on future violations.\n\n"
            f"**Enforcement Context**: The company received the FTC's Notice of Penalty Offenses "
            f"(April 2023) but continued the violative practice. The 2024 base civil penalty rate "
            f"of $51,744 per violation was applied.\n\n"
            f"**Key Finding**: {violation_desc} constitutes a deceptive practice under Section 5 "
            f"of the FTC Act. The company's failure to implement adequate disclosure procedures "
            f"despite the Notice of Penalty Offenses justified enhanced enforcement action.\n\n"
        )

    # Add Kubota Made in USA case (real anchor A14)
    kubota_case = """### Special Case: FTC v. Kubota North America Corporation (January 2024)

**Product category**: Power equipment and farm equipment (not dietary supplement)
**Violation**: False "Made in USA" claims under 16 CFR Part 323
**Civil penalty**: $2,000,000 (Two Million Dollars)
**Settlement**: Consent order, January 2024

**Significance**: This is the **largest civil penalty** ever imposed for a Made in USA
labeling violation under 16 CFR Part 323. The "all or virtually all" standard requires that:
(1) all significant processing occur in the United States;
(2) all or virtually all ingredients/components be of U.S. origin;
(3) final assembly occur in the United States.

Kubota's equipment contained substantial foreign-made components, making the "Made in USA"
claim false under the Part 323 standard.

**Relevance to VitaCore**: VitaCore's ProBio+ Daily sources some vitamins from Netherlands
and Denmark, and bottles from China. The "Made in USA" claim on the current label draft
requires a thorough 16 CFR Part 323 analysis before use.

---

"""

    header = """# FTC Enforcement Cases — Consumer Review and Endorsement Violations (2024)

**Source**: FTC Enforcement Actions Database, updated March 2026
**Coverage**: Cases involving 16 CFR Part 465 (Consumer Reviews), 16 CFR Part 255 (Endorsements),
and 16 CFR Part 323 (Made in USA Labeling) enforcement actions in calendar year 2024.

**Note on penalties**: All 2024 cases apply the $51,744 per-violation base rate.
For 2025 cases, the adjusted rate of $53,088 applies (effective February 2025).

---

## Overview Statistics (2024)

- Total enforcement actions: 44
- Average penalty per action: $412,000
- Largest penalty (dietary supplement sector): $1,034,880 (20 violations × $51,744)
- Smallest penalty: $51,744 (1 violation)
- Most common violation: Fake/unverified consumer reviews (§465.2)

---

## Individual Cases

"""
    footer = """

---

## Key Takeaways for Compliance Practitioners

1. **$51,744 per violation (2024 base rate)** — this is the controlling figure for
   ProBio+ Daily's compliance analysis, not the $45,000 figure cited in bot summaries
   or informal communications.

2. **"Results Not Typical" is not a defense** — courts have consistently held that
   the 2009 abolition of the safe harbor controls; advertisers cannot rely on the
   pre-2009 Guides for this defense.

3. **Platform "Paid Partnership" tools are insufficient** — in every case reviewed,
   relying solely on built-in platform disclosure mechanisms was found inadequate.

4. **Insider reviews without disclosure** are treated as serious violations (§465.3);
   penalty compounded by number of reviews posted.

5. **Made in USA claims** require the "all or virtually all" standard per 16 CFR Part 323;
   the $2 million Kubota penalty demonstrates enforcement priority for this violation.
"""
    return header + kubota_case + "\n".join(cases) + footer


def _gen_green_claims_report() -> str:
    """Generate a ~15KB green claims test reports document."""
    return """# VitaCore ProBio+ Daily — Green Claims Independent Testing Report

**Prepared by**: EcoVerify Labs (Accredited Testing Laboratory)
**Date**: February 28, 2026
**Purpose**: Substantiation of environmental marketing claims under 16 CFR Part 260

---

## Executive Summary

EcoVerify Labs conducted independent testing of VitaCore's ProBio+ Daily packaging
and formula components to assess the validity of the following environmental claims:

1. "Eco-friendly packaging"
2. "Biodegradable formula capsules"
3. "Recyclable bottle"

**Overall Assessment**: Two of three claims require modification or qualification before use.

---

## Test 1: Biodegradability of Capsule Material

### Claim Under Review
"Biodegradable formula capsules"

### Applicable Standard
16 CFR §260.8 requires complete degradation within one year under customary disposal conditions.

### Test Methodology
- Test material: Vegetable-derived HPMC capsule shells
- Test environment: Simulated landfill conditions (ASTM D5511), composting conditions (ASTM D5338)
- Duration: 52 weeks (one year)
- Measurement: Percentage mass reduction, CO2 evolution

### Results

| Condition | Mass Remaining at 52 weeks | Compliant? |
|-----------|--------------------------|-----------|
| Landfill simulation | 67% remaining | NO — does not fully degrade |
| Industrial composting | 12% remaining | Conditional — requires industrial composting |
| Home composting | 81% remaining | NO — does not qualify |

### Conclusion
The capsule material does **not** fully degrade within one year under typical landfill
disposal conditions (the most common disposal pathway in the United States). The capsules
do degrade in industrial composting conditions, but this pathway is not widely available.

**Compliant Claim Options**:
- "Capsules are compostable in industrial composting facilities" (qualified claim)
- Remove "biodegradable" claim until a compliant capsule material is adopted

**Non-Compliant Claim**:
- "Biodegradable formula capsules" (unqualified) = DECEPTIVE under §260.8

**Requirement per Revised Audit Letter**: Independent test report documenting degradation
within one year is required. This report does NOT provide that documentation — instead,
it documents that degradation within one year does NOT occur under customary conditions.

---

## Test 2: Recyclability of PET Bottle

### Claim Under Review
"Recyclable PET bottle"

### Applicable Standard
16 CFR §260.12: Unqualified "recyclable" claim requires recycling facilities to be
available to a **substantial majority** (defined as **60%**) of consumers.

### Market Analysis

We surveyed the top 50 metropolitan markets (by population) where ProBio+ Daily
is planned for distribution:

| Metric | Finding |
|--------|---------|
| Markets with PET (#1) curbside recycling | 47/50 (94%) |
| Consumer population covered | 78% of planned distribution area |
| Rural/suburban markets without access | 22% |

### Conclusion
The "Recyclable PET bottle" claim IS substantiated for the planned distribution markets.
The 78% consumer coverage exceeds the 60% "substantial majority" threshold defined in
§260.12. A qualified claim is not required.

**Compliant Claim**: "Recyclable PET bottle" (unqualified acceptable)
**Supporting documentation**: Market analysis on file at EcoVerify Labs.

---

## Test 3: "Eco-Friendly Packaging" Assessment

### Claim Under Review
"Eco-friendly packaging made from recycled materials"

### Issue
The outer box contains 40% post-consumer recycled cardboard. The bottle cap is virgin
polypropylene. The label is non-recyclable laminated film.

### Applicable Standard
"Eco-friendly" is a general environmental benefit claim. Under 16 CFR §260.4, general
benefit claims require substantiation that all express and implied environmental benefits
have been demonstrated. A claim that the packaging is "eco-friendly" implies broad
environmental benefit.

### Findings
- Box: 40% PCR content — positive attribute, but does not make packaging "eco-friendly" overall
- Bottle cap: virgin PP — negative contributor
- Label material: non-recyclable laminate — negative contributor

### Conclusion
The unqualified "Eco-friendly packaging" claim is **not substantiated** based on the full
packaging lifecycle assessment. A qualified claim is acceptable:
- "Box made from 40% post-consumer recycled cardboard"
- Remove "eco-friendly packaging" or qualify significantly

---

## Summary Table

| Claim | Finding | Compliant (As-Is)? | Remediation Required |
|-------|---------|-------------------|---------------------|
| "Biodegradable formula capsules" | Fails §260.8 — no 1-year degradation | NO | Remove or qualify as "compostable in industrial composting facilities" |
| "Recyclable PET bottle" | Passes §260.12 — 78% coverage ≥ 60% threshold | YES | None required |
| "Eco-friendly packaging" | Unsupported general claim | NO | Remove or replace with specific PCR content claim |

---

## Required Documentation for Biodegradable Claim

Per the revised audit opinion from Compliance Counsel LLC (email_revised_audit_v2),
a biodegradable claim requires an independent test report from an accredited laboratory
documenting complete degradation within one year. This report provides evidence to the
**contrary** — the current capsule material does not meet this standard.

VitaCore must either:
1. Source a capsule material that degrades within one year under customary disposal, and
   obtain a new test report confirming compliance; or
2. Remove the "biodegradable" claim from all marketing materials.

---

**Laboratory Accreditation**: ISO/IEC 17025:2017 Accredited
**Report Reference**: EVL-2026-PBD-001
**Signatory**: Dr. Marcus Okafor, Director of Environmental Testing, EcoVerify Labs
"""


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> None:
    # 初始化大体量内容生成器
    _init_large_content()

    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()
    gen_regulatory_docs()
    gen_company_files()
    gen_drafts()
    gen_research()
    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = (
        "VitaCore ProBio+ Daily pre-launch compliance review: consumer review authenticity "
        "(16 CFR Part 465, eff. Oct 21, 2024) + endorsement disclosure (16 CFR Part 255, "
        "eff. Jul 26, 2023). 16 exec_check rounds, 2 updates (incl. CEO-directive supersede "
        "and external-audit-letter supersede), 5 preference rules P1-P5, difficulty vectors "
        "V1/V2/V3/V4/V5/V6/V7/V8/V9/V10. "
        "Real sources: 16 CFR Part 465 (https://www.law.cornell.edu/cfr/text/16/part-465); "
        "16 CFR Part 255 (https://www.law.cornell.edu/cfr/text/16/part-255); "
        "FTC Health Products Compliance Guidance Dec 2022 "
        "(https://www.ftc.gov/business-guidance/resources/health-products-compliance-guidance)."
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
    sess_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in SESS.glob("*.jsonl")
    )
    upd_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in UPD.rglob("*") if p.is_file()
    )
    print(f"[{TID}] workspace tokens ~{total:,} | sessions ~{sess_tok:,} | updates ~{upd_tok:,}")
    print(f"[{TID}] built at {DATASET}")


if __name__ == "__main__":
    main()
