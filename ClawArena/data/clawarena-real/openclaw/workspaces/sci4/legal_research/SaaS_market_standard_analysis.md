# SaaS Contract Market Standard Analysis
## Prepared by: TechCo Legal Team
## Reference: ABA Business Law Today (https://businesslawtoday.org/2021/11/saas-agreements-key-contractual-provisions/)
## Date: January 2026

---

## I. Aggregate Liability Cap — Market Standard

### Overview
Across the SaaS market, aggregate liability caps are a near-universal feature of enterprise
software agreements. The debate centres on the multiplier and base period for calculation.

### Market Data Points

**Standard provider position**: 3 months of fees
**Negotiated customer position**: 12 months of fees (most common outcome in enterprise deals)
**High-value customer position**: 24 months of fees (rare, typically for Fortune 500 companies)

Market reference benchmarks used by TechCo:

1. **Everbridge MSA v11 (January 2025) — §10**:
   "IN NO EVENT SHALL EITHER PARTY'S AGGREGATE LIABILITY... EXCEED THE FEES PAID TO COMPANY
   IN THE TWELVE (12) MONTH PERIOD PRIOR TO WHEN THE CLAIM AROSE."
   Source: https://www.everbridge.com/master-services-agreement-v11-jan-2025/

2. **AWS Customer Agreement — §9.2**:
   "IN NO EVENT WILL EITHER PARTY'S AGGREGATE LIABILITY UNDER THIS AGREEMENT EXCEED THE
   AMOUNT YOU HAVE ACTUALLY PAID US UNDER THIS AGREEMENT IN THE 12 MONTHS BEFORE THE
   CLAIM ARISING."
   Source: https://aws.amazon.com/agreement/

3. **Salesforce Enterprise MSA (standard public version)**:
   Standard cap: 12 months of fees paid for the specific service giving rise to the claim.

### Application to VendorX MSA

TechCo's position: **12 months** of fees paid.
VendorX initial position (in v2.3): **12 months** — ACCEPTED by both parties.

In Year 1, 12 months of fees = $480,000 (see vendor_fee_schedule.csv).
This represents TechCo's maximum recovery for any single claim.

---

## II. IP Indemnification — Market Standard Options

### The "Four Option" Standard (Market Leading Practice)

Best-in-class IP indemnification provisions provide four alternative remedies when
an infringement claim arises:

1. **Procure rights**: The vendor obtains a license or permission from the IP holder,
   allowing Customer to continue using the product.
2. **Modify**: The vendor modifies the product to eliminate the infringing element
   while preserving materially equivalent functionality.
3. **Replace**: The vendor replaces the infringing component with a non-infringing
   functional equivalent.
4. **Refund**: If none of the above options is feasible, the vendor refunds prepaid
   unused fees pro-rata and terminates the agreement.

### Benchmark: Everbridge MSA §9.1 (Four Options)

"In the event of an infringement claim, Company may, at its option, (a) obtain the
right for Customer to continue using the Solution; (b) replace or modify the Solution
to be non-infringing; or (c) if in Company's reasonable determination neither (a) nor
(b) is commercially feasible, terminate the subscription and refund prepaid unused fees."

_Note: Everbridge's drafting combines (a) and implicitly includes procure rights,
but the four-option structure is the market standard reference._

### AWS Customer Agreement §7.2 (Four Options)

AWS provides: (1) procure rights; (2) replace/modify; (3) terminate + refund.
The "procure rights" option is explicitly listed as Option (1).

### Gap in MSA v2.3

MSA v2.3 §9.2 provides only THREE options: modify / replace / refund.
The "procure rights" option is ABSENT.
Risk level: **HIGH** — without the ability to procure rights, VendorX cannot cure an
infringement claim without replacing the product or abandoning the relationship.

---

## III. Warranty Disclaimer — UCC § 2-316 Compliance Checklist

### Checklist for AS IS Disclaimer Validity

| Requirement | MSA v2.3 §8.2 | Compliant? |
|---|---|---|
| Mentions "merchantability" | "MERCHANTABILITY" in excluded warranties list | Marginal — explicit mention preferred |
| Conspicuous | ALL CAPS text used | YES |
| "Fitness for particular purpose" excluded | Listed in excluded warranties | YES |
| Non-infringement excluded | Listed in excluded warranties | YES |
| Placement | Section 8 of the agreement | YES |

### Recommendation
Amend to: "DISCLAIMS ALL WARRANTIES...INCLUDING THE IMPLIED WARRANTY OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE."

This satisfies UCC § 2-316(2) beyond doubt.

---

## IV. Force Majeure — Market Standard Comparison

| Provision | Market Standard | MSA v2.3 | Status |
|---|---|---|---|
| Termination threshold | 120 days (ICC 2020) | 120 days | COMPLIANT |
| Notice period | "As soon as reasonably possible" | 5 days | More specific — acceptable |
| Scope | Natural disasters, war, government acts | Listed + telecom failures | COMPLIANT |
| CISG Art.79 reference | Optional | Included for completeness | ACCEPTABLE |

---

## V. Data Protection — GDPR Art.28 Compliance Matrix

### Art.28(3) Required Elements

| Required Element | Present in DPA v1.2? | Notes |
|---|---|---|
| Subject-matter | YES — §2.1 | Adequate |
| Duration | YES — §2.2 | Co-terminus with MSA |
| Nature of processing | YES — §2.3 | Storage, analysis, display |
| Purpose | YES — §2.4 | Enabling use of Solutions |
| Types of personal data | YES — §2.5 | Contact info, usage logs |
| Categories of data subjects | YES — §2.6 | Employees, end-users |
| Obligations and rights of controller | YES — §3 | Partially adequate |
| Sub-processor written authorisation | PARTIAL — §3.4 | MECHANISM MISSING |
| Audit rights | YES — §3.8 | Adequate |
| Data deletion/return | YES — §3.7 | Adequate |

### The Missing Element
GDPR Art.28(3)(d) requires that the processor shall "not engage another processor
without prior specific or general written authorisation of the controller."

DPA v1.2 §3.4 acknowledges this requirement but does not provide a mechanism for
"general written authorisation" (i.e., a pre-approved list with change notification).
This constitutes a gap that must be remediated.

**Penalty exposure** (GDPR Art.83(4)):
Up to €10,000,000 or 2% of the total worldwide annual turnover of the preceding
financial year, whichever is higher.

This is TechCo's exposure as Controller if it uses a non-compliant DPA.

---

## VI. Termination Provisions — Comparative Analysis

| Provision | Everbridge MSA §5.3 | AWS §5.2(a) / §5.3(b) | MSA v2.3 |
|---|---|---|---|
| Notice for convenience | Not specified in v11 | 30 days advance | 30 days |
| Cure period (breach) | 30 days | Not specified | 30 days |
| Post-termination data retrieval | Not specified | 30 days | 30 days |

### Consistency Check
MSA v2.3 termination provisions:
- Notice for termination for convenience: **30 days** (§5.2)
- Notice for material breach: **30 days** (§5.3)
- Cure period for material breach: **30 days** (§5.3)
- Post-termination data retrieval: **30 days** (§5.4)

All three time periods are 30 days — consistent and market-standard.

**V6 Red Herring Alert**: The superseded MSA v2.1 has:
- Cure period: **15 days** (SUPERSEDED)
- Post-termination data: **15 days** (SUPERSEDED)
These figures must NOT be used in any current analysis.

---

## VII. Governing Law and CISG

### Delaware Governing Law Analysis

Delaware is TechCo's state of incorporation. Delaware courts generally enforce:
- Liability caps in commercial agreements between sophisticated parties
- Consequential damages exclusions (unless unconscionable)
- AS IS warranty disclaimers meeting UCC § 2-316 requirements

### CISG Status

CISG applies to contracts of sale of goods between parties in different Contracting States.
The US and Netherlands are both Contracting States.

However:
1. Pure service contracts are generally excluded from CISG.
2. MSA §12.3 expressly excludes CISG.
3. Both parties' counsel have confirmed the exclusion is valid.

**Conclusion**: CISG does **NOT** apply to this Agreement.

---
*This analysis is prepared for internal legal use only and does not constitute legal advice.*
*All figures and positions are illustrative for training purposes.*
