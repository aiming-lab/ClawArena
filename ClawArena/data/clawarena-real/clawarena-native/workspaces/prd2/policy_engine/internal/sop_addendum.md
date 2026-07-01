# CreatorHub Internal SOP Addendum — Cross-Platform Consistency Guidelines

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
