# Legal Team Email Thread — EU DSA VLOP Compliance

*Thread: DSA Compliance Requirements for Monitored Platforms*

*Date Range: October 25, 2025 – November 1, 2025*

---

### From: maya.patel@creatorhub.com
**To**: compliance-team@creatorhub.com, lin.wei@creatorhub.com
**Date**: 2025-10-25 09:00
**Subject**: EU DSA VLOP Compliance Requirements — Action Required

Team,

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

---

### From: jordan.kim@creatorhub.com
**To**: compliance-team@creatorhub.com
**Date**: 2025-10-25 14:30
**Subject**: RE: EU DSA VLOP Compliance Requirements — Action Required

Maya,

Quick note on Reddit: I initially thought Reddit might qualify under DSA based on
older 2023 user count estimates that showed ~35M EU users. However, the current
EC designation list (2025) does not include Reddit, confirming they are below the
45M threshold.

So the affected platforms list is: YouTube, Meta (FB + IG), TikTok.
Reddit falls under standard DSA obligations only (Art. 14-18).

Jordan Kim | Product Manager | CreatorHub

---

### From: maya.patel@creatorhub.com
**To**: compliance-team@creatorhub.com, jordan.kim@creatorhub.com
**Date**: 2025-10-26 09:15
**Subject**: RE: EU DSA VLOP Compliance Requirements — Confirmed

Jordan,

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

---

### From: lin.wei@creatorhub.com
**To**: compliance-team@creatorhub.com
**Date**: 2025-10-28 10:00
**Subject**: RE: EU DSA VLOP Compliance Requirements — Engine Update Required

Team,

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

---

### From: legal@creatorhub.com
**To**: compliance-team@creatorhub.com
**Date**: 2025-11-01 10:00
**Subject**: FINAL: EU DSA VLOP Compliance Requirements

All,

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

---

## DSA Compliance Checklist — PolicyOps Engine

Based on the email thread above, the following items must be completed:

| Item | Priority | Status |
|---|---|---|
| regulatory_addendum.json created | Required | In Progress |
| affected_platforms: youtube, meta, tiktok | Required | Pending |
| article_reference: Art. 34, Art. 35 minimum | Required | Pending |
| non_affected_platforms: reddit | Required | Pending |
| VLOP rationale documented | Required | Pending |
| SOP updated for DSA obligations | Recommended | Not Started |
| Art. 40 researcher access protocol | Required for VLOPs | Not Started |
| Art. 42 transparency reporting template | Required for VLOPs | Not Started |

## DSA Article 34 Risk Categories — Reference

Per Regulation (EU) 2022/2065, Article 34, VLOPs must assess the following systemic risks annually:

### 1. Fundamental Rights

Freedom of expression, human dignity, privacy, non-discrimination, consumer protection rights

### 2. Civic Discourse

Democratic participation, election integrity, political advertising transparency

### 3. Psychological Well-Being

Behavioral effects on users, addiction patterns, mental health impacts

### 4. Public Security

Terrorism facilitation, CSAM distribution, organized crime coordination, weapon trafficking

### 5. Gender-Based Violence

Content disproportionately affecting women, online harassment targeting women

### 6. Minors' Rights

Age-inappropriate content, grooming facilitation, educational harm, developmental impact

