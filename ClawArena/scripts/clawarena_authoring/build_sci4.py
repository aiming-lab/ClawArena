#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sci4.py — 生成 ClawArena 真实数据集场景 sci4（法律证据与合同条款审查）。

题材与锚点取材真实（UCC §2-316/2-719、CISG Art.74/79、GDPR Art.28、Everbridge MSA v11、
AWS Customer Agreement、Hadley v Baxendale [1854] EWHC J70、ICC Force Majeure 2020），
session 对话与 workspace 文档围绕真实锚点合成。全 exec_check，16 轮。

幂等：每次运行先清空 sci4 的 workspace/state/updates 后重建。
questions.json 与 check 脚本由 eval/sci4/ 下静态文件提供，本脚本不生成它们。

运行：python scripts/clawarena_authoring/build_sci4.py
"""
from __future__ import annotations

import csv
import io
import json
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
TID = "sci4"
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
# 1. 系统文件（Agent 启动文件）
# --------------------------------------------------------------------------- #
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls -R` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are LegalOps AI, a legal review assistant supporting Jessica Lin (General Counsel)
and the TechCo legal team in reviewing and negotiating the Master Services Agreement (MSA)
with VendorX, a SaaS platform provider. Your outputs feed directly into contract execution
decisions.
""")

    w(WS / "SOUL.md", """# Working Principles

1. **Authoritative-source-first**: The canonical contract versions are in `contracts/`.
   Files labelled SUPERSEDED or containing old version numbers are NOT authoritative —
   verify every clause against the current effective version.

2. **Verbatim legal citations**: Always cite legal authorities exactly as they appear in
   `legal_research/` documents:
   - Cases: [1854] EWHC J70 (not abbreviated)
   - UCC sections: UCC § 2-316 (with section symbol and spaces)
   - EU regulations: GDPR Art.28(3) (with full article reference)

3. **Output schema discipline**: Every JSON deliverable carries a top-level
   `schema_version` field set to `"1.0"`. Risk matrices use only HIGH/MEDIUM/LOW
   as risk_level values. Do not improvise schema shapes.

4. **Numeric claims require citation**: Any numeric assertion (days, months, currency
   amounts) must be accompanied by a source reference in parentheses.
   Format: "value (Source Name §section)".

5. **Regulatory tagging**: All compliance issues must be tagged with their regulatory
   source. Format: [Source: REGULATION Art.N].

6. **Temporal awareness**: Contract versions evolve. When an update or supersede notice
   arrives, the later instruction wins — revise prior outputs rather than stacking
   contradictory logic.

7. **Report structure discipline**: The final review report must contain exactly three
   sections in order: Executive Summary, Risk Matrix, Recommended Actions.
""")

    w(WS / "USER.md", """# People and Channels

## Primary User
- **Jessica Lin** — General Counsel at TechCo. Owns the MSA negotiation with VendorX.
  Prefers standardised legal citation formats, numeric claims with citations, and
  structured JSON deliverables with schema_version tags. Decisive and detail-oriented.

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Marcus Webb | Associate General Counsel | Slack #legal-review | Handles day-to-day clause analysis; sometimes over-relies on Slack bot summaries |
| Dr. Sarah Chen | Privacy Counsel | Email | DPA compliance specialist; GDPR authority |
| Owen Park | External Counsel (Morrison & Clarke LLP) | Discord #external-counsel | IP and arbitration expert |
| Kevin Zhao | CFO / Finance | Feishu DM | Concerned about liability cap and fee schedule |

## Channels
- **Slack #legal-review**: Team contract discussion (Jessica, Marcus, and the Slack bot)
- **Email (Dr. Sarah Chen ↔ legal team)**: DPA/GDPR negotiation correspondence
- **Feishu DM (Kevin → agent / Jessica → agent)**: Finance directives and update notices
- **Discord #external-counsel (Owen Park, LLP)**: IP indemnification and arbitration analysis
- **Feishu Group (cross-functional)**: Multi-source information exchange (V1 conflict source)
""")

    w(WS / "IDENTITY.md", """# Identity

You are **LegalOps AI**, a legal review AI assistant deployed to support TechCo's legal
team during the review and negotiation of the Master Services Agreement (MSA) with VendorX.

You analyse contract clauses against legal standards (UCC, CISG, GDPR, common law), identify
risk gaps, track version changes across negotiation rounds, and produce standardised review
deliverables (JSON reports, risk matrices, final review summaries). Authoritative contract
documents and legal research files under `contracts/` and `legal_research/` are your primary
inputs; you create deliverables under `output/`.
""")

    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session to discover history |
| `sessions_history` | Read a specific history session | Use in the main session to review past discussions |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to run scripts and write deliverable files |

## Rules
- Source inputs under `contracts/` and `legal_research/` are **read-only** — do not modify them.
- You DO create new deliverable files under `output/` using `exec`.
- In history sessions, use only `read` and light `exec`; do not call `sessions_list` there.
""")


# --------------------------------------------------------------------------- #
# 2. 合同文件（真实锚点取材 Everbridge MSA v11 / AWS / UCC / CISG / GDPR）
# --------------------------------------------------------------------------- #
def gen_contracts() -> None:
    # MSA v2.3（当前有效草稿，基于 Everbridge MSA v11 结构）
    w(WS / "contracts" / "MSA_VendorX_v2.3_DRAFT.md", """# Master Services Agreement
## Version 2.3 — DRAFT (Current Negotiation Version)
## Status: ACTIVE
## Date: 2026-01-15
## Parties: TechCo, Inc. ("Customer") and VendorX Solutions Ltd. ("Company")
## Supersedes: Version 2.1 (dated 2025-11-20)

---

## §1 Definitions

1.1 "Solutions" means the SaaS platform services described in any Statement of Work (SOW).
1.2 "Customer Data" means all data submitted by Customer to the Solutions.
1.3 "Effective Date" means the date of last signature of this Agreement.
1.4 "Term" means the initial period specified in an SOW plus any renewal periods.
1.5 "Documentation" means the technical specifications and user guides provided by Company.

---

## §2 License and Scope

2.1 Subject to the terms of this Agreement, Company grants Customer a non-exclusive,
non-transferable, limited license to access and use the Solutions during the Term.

2.2 The license is limited to Customer's internal business purposes and may not be
sublicensed without the prior written consent of Company.

---

## §3 Fees and Payment

3.1 Customer shall pay fees as set forth in the applicable Statement of Work and fee schedule.

3.2 Fees are due within thirty (30) days of invoice. Late payments accrue interest at
1.5% per month or the maximum lawful rate, whichever is lower.

3.3 Annual fee schedule summary (reference `data/vendor_fee_schedule.csv` for detail):
- Year 1: $480,000 (monthly: $40,000)
- Year 2: $504,000 (monthly: $42,000)
- Total 24-month commitment: $984,000

---

## §4 Intellectual Property

4.1 As between the parties, Customer retains all right, title, and interest in and to
Customer Data and Customer's pre-existing intellectual property.

4.2 Company retains all right, title, and interest in and to the Solutions and all
improvements, modifications, and derivative works thereof.

4.3 Customer grants Company a limited, non-exclusive license to use Customer Data
solely to provide the Solutions.

---

## §5 Term and Termination

5.1 **Initial Term**: This Agreement commences on the Effective Date and continues for
twenty-four (24) months unless earlier terminated.

5.2 **Termination for Convenience**: Either party may terminate this Agreement upon
thirty (30) days' prior written notice.

5.3 **Termination for Material Breach**: If either party materially breaches this
Agreement, the non-breaching party shall provide thirty (30) days' written notice
specifying the breach in reasonable detail. If the breaching party fails to cure
within thirty (30) days of receipt of such notice (the "Cure Period"), the
non-breaching party may terminate this Agreement.
— Cure Period: **30 days** (from receipt of notice)
— Notice Period: **30 days** (written notice to specify breach)

5.4 **Post-Termination Data**: Following termination for any reason, Customer shall have
thirty (30) days to retrieve Customer Data (provided all fees have been paid in full).
After such period, Company may delete Customer Data without further obligation.

---

## §6 Data Processing

6.1 This Agreement incorporates by reference the Data Processing Agreement (DPA)
attached hereto as Exhibit A (DPA_VendorX_v1.2.md).

6.2 To the extent Company processes personal data of EU data subjects on behalf of
Customer, the parties agree that the DPA shall govern such processing, consistent
with the requirements of Regulation (EU) 2016/679 (GDPR), Article 28.

6.3 Company shall process personal data only in accordance with Customer's documented
instructions and shall not process personal data for any other purpose.

---

## §7 Confidentiality

7.1 Each party agrees to maintain in confidence all Confidential Information received
from the other party and to use it only in connection with this Agreement.

7.2 Confidentiality obligations survive termination for a period of **two (2) years**.

7.3 Standard carve-outs apply: information in the public domain, independently developed
information, and information required to be disclosed by law.

---

## §8 Warranties and Disclaimer

8.1 **Company Warranties**: Company warrants that (a) it has the authority to enter into
this Agreement; (b) the Solutions will materially conform to the Documentation.

8.2 **AS IS Disclaimer**: EXCEPT AS EXPRESSLY STATED IN §8.1, COMPANY PROVIDES THE
SOLUTIONS "AS IS" AND DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO ANY IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE, AND NON-INFRINGEMENT. THE DISCLAIMER IN THIS SECTION SHALL
BE CONSPICUOUS AND IS MATERIAL TO THIS AGREEMENT.

_Note: The §8.2 disclaimer must satisfy UCC § 2-316(2) requirements: (1) the word
"merchantability" must be explicitly mentioned; (2) the disclaimer must be conspicuous.
TechCo's legal team notes that the current draft mentions "MERCHANTABILITY" in uppercase
but should verify compliance with UCC § 2-316(2) conspicuousness standard._

---

## §9 Indemnification

9.1 **IP Indemnification**: Company shall defend Customer against any third-party
claims alleging that the Solutions infringe any third-party intellectual property rights.
Company shall pay damages finally awarded in such claims.

9.2 **IP Remedy Options**: If an infringement claim arises, Company may, at its sole
discretion:
- (a) Modify the Solutions to be non-infringing; OR
- (b) Replace the Solutions with a functional equivalent; OR
- (c) Refund prepaid unused fees pro-rata.

_Note: This provision is modelled on market standard. The Everbridge MSA §9.1 additionally
includes "procure rights" as a remedy option — TechCo should assess whether this gap
creates material risk in the current draft._

9.3 **Mutual Indemnification**: Each party shall indemnify the other against third-party
claims arising from its own gross negligence or wilful misconduct.

9.4 **Exclusions**: The IP indemnification in §9.1 does not apply if the infringement
results from Customer's modifications or Customer's combination with third-party products.

---

## §10 Limitation of Liability

10.1 **Aggregate Cap**: EXCEPT FOR OBLIGATIONS UNDER §9 (INDEMNIFICATION), IN NO EVENT
SHALL EITHER PARTY'S AGGREGATE LIABILITY ARISING OUT OF OR RELATED TO THIS AGREEMENT
EXCEED THE FEES PAID BY CUSTOMER TO COMPANY IN THE TWELVE (12) MONTH PERIOD PRIOR
TO THE DATE THE CLAIM AROSE.

10.2 **Excluded Damages**: IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY INDIRECT,
INCIDENTAL, SPECIAL, CONSEQUENTIAL, EXEMPLARY, OR PUNITIVE DAMAGES, INCLUDING BUT
NOT LIMITED TO LOSS OF PROFITS, LOSS OF REVENUE, LOSS OF DATA, OR LOSS OF BUSINESS
OPPORTUNITIES, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

10.3 **UCC Context**: The limitation of consequential damages in §10.2 is enforceable
under UCC § 2-719 unless such limitation fails of its essential purpose. Pursuant to
UCC § 2-719(3), limitation of consequential damages for personal injury from consumer
goods is prima facie unconscionable.

10.4 **Carve-outs from Cap**: The aggregate liability cap in §10.1 does not apply to:
- (i) Each party's indemnification obligations under §9;
- (ii) Damages arising from gross negligence or wilful misconduct;
- (iii) Breaches of confidentiality obligations.

---

## §11 Force Majeure

11.1 Neither party shall be liable for delays or failures in performance resulting from
causes beyond its reasonable control, including but not limited to: acts of God,
natural disasters, epidemics, pandemics, governmental actions, war, terrorism,
labour disputes, or failures of third-party telecommunications or internet providers.

11.2 **Notice Obligation**: The affected party shall provide written notice to the other
party within five (5) days of the occurrence of the force majeure event.

11.3 **Suspension**: Performance obligations are suspended during the force majeure event.

11.4 **Termination Threshold**: If the force majeure event continues for more than
one hundred twenty (120) days, either party may terminate this Agreement without
liability upon written notice.
— ICC 2020 Force Majeure Clause termination threshold: **120 days**

11.5 **CISG Context**: To the extent CISG applies to cross-border elements of this
Agreement, force majeure is governed by CISG Article 79, which requires proof of:
(a) an impediment beyond the party's control; AND
(b) that the party could not reasonably be expected to have taken the impediment
into account at the time of the conclusion of the contract.

---

## §12 Governing Law and Dispute Resolution

12.1 **Governing Law**: This Agreement shall be governed by and construed in accordance
with the laws of the State of Delaware, United States, without regard to conflicts
of law principles.

12.2 **Dispute Resolution**: Any dispute arising under this Agreement shall first be
subject to good-faith negotiation for thirty (30) days. If unresolved, disputes
shall be submitted to binding arbitration under the ICC Rules of Arbitration.

12.3 **CISG Exclusion**: The parties expressly agree to exclude the application of the
United Nations Convention on Contracts for the International Sale of Goods (CISG)
to this Agreement.

_Note: VendorX is incorporated in the Netherlands. The effectiveness of the CISG
exclusion clause in §12.3 has been questioned in the Feishu group discussion.
See legal_research/CISG_damages_analysis.md for analysis._

---

## Exhibit A — Data Processing Agreement
See DPA_VendorX_v1.2.md

## Exhibit B — Statement of Work
See SOW_001_Implementation.md

---
*End of MSA Version 2.3 DRAFT*
""")

    # MSA v2.1（被废弃的旧版，红鲱鱼）
    w(WS / "contracts" / "MSA_VendorX_v2.1_SUPERSEDED.md", """# Master Services Agreement
## Version 2.1 — SUPERSEDED (Do Not Use)
## Status: SUPERSEDED by Version 2.3
## Date: 2025-11-20
## NOTICE: This version has been superseded by MSA Version 2.3 (dated 2026-01-15).
## Do NOT reference this version for any current analysis.

---

## §5 Term and Termination (v2.1 — SUPERSEDED)

5.3 **Termination for Material Breach**: Written notice of breach required. If the
breaching party fails to cure within **fifteen (15) days** of notice, the non-breaching
party may terminate.
— Cure Period: **15 days** ← THIS IS THE OLD PROVISION, SUPERSEDED BY v2.3's 30 days

5.4 **Post-Termination Data**: Customer has **fifteen (15) days** to retrieve data.
← SUPERSEDED — current version v2.3 grants 30 days

---

## §10 Limitation of Liability (v2.1 — SUPERSEDED)

10.1 **Aggregate Cap**: Liability capped at fees paid in the **six (6) month period**
prior to the claim date.
← SUPERSEDED — current version v2.3 cap is 12 months

---

*This document is SUPERSEDED and retained for audit trail only.*
*Reference MSA_VendorX_v2.3_DRAFT.md for the current governing terms.*
""")

    # DPA v1.2
    w(WS / "contracts" / "DPA_VendorX_v1.2.md", """# Data Processing Agreement
## Version 1.2
## Between: TechCo, Inc. ("Controller") and VendorX Solutions Ltd. ("Processor")
## Date: 2026-01-10
## Governing Regulation: GDPR (Regulation (EU) 2016/679), Article 28

---

## 1. Purpose and Scope

1.1 This DPA governs the processing of personal data by VendorX (Processor) on behalf
of TechCo (Controller) in connection with the Master Services Agreement.

1.2 VendorX shall process personal data only in accordance with TechCo's documented
instructions and for the purposes specified in this DPA.

---

## 2. Subject Matter of Processing

2.1 Subject-matter: Delivery of SaaS platform services (analytics and workflow automation)
2.2 Duration: Co-terminus with the MSA (24-month initial term, plus renewals)
2.3 Nature: Storage, analysis, and display of Customer Data
2.4 Purpose: Enabling Customer's use of the Solutions
2.5 Types of Personal Data: Contact information (name, email), usage logs, analytics data
2.6 Categories of Data Subjects: TechCo employees and TechCo's end-user clients

---

## 3. Processor Obligations (GDPR Art.28(3) Requirements)

3.1 **Processing only on instructions**: VendorX shall process personal data only on
documented instructions from TechCo.

3.2 **Confidentiality**: VendorX ensures that persons authorised to process personal data
have committed to confidentiality or are under a statutory obligation of confidentiality.

3.3 **Security measures**: VendorX shall implement appropriate technical and organisational
measures (Art.32) to ensure a level of security appropriate to the risk.

3.4 **Sub-processors**: VendorX shall not engage another processor (sub-processor) without
prior specific or general written authorisation of TechCo.
_[COMPLIANCE NOTE: This clause requires written authorisation for sub-processors.
Current draft does not include a mechanism for general written authorisation of
sub-processor categories. This gap requires remediation — see DPA review output.]_

3.5 **Data subject rights**: VendorX shall assist TechCo in fulfilling obligations to
respond to requests from data subjects exercising their GDPR rights.

3.6 **Security assistance**: VendorX shall assist TechCo in ensuring compliance with
obligations under Articles 32-36 (security, breach notification, DPIA, prior consultation).

3.7 **Deletion/return**: At the choice of TechCo, VendorX shall delete or return all
personal data after the end of the provision of services, and delete existing copies.

3.8 **Audit rights**: VendorX shall make available to TechCo all information necessary
to demonstrate compliance and shall allow for and contribute to audits and inspections.

---

## 4. Written Requirement

4.1 This DPA is concluded in writing, including in electronic form, as required by
GDPR Article 28(3): "The processing by a processor shall be governed by a contract
or other legal act under Union or Member State law, that is binding on the processor
with regard to the controller and that sets out the subject-matter and duration of
the processing, the nature and purpose of the processing, the type of personal data
and categories of data subjects and the obligations and rights of the controller.
That contract or other legal act shall be in writing, including in electronic form."

---

## 5. Penalties for Non-Compliance

5.1 Non-compliance with GDPR Article 28 obligations may result in penalties pursuant
to GDPR Article 83(4): up to €10,000,000 or 2% of the total worldwide annual turnover
of the preceding financial year, whichever is higher.

---

## 6. Governing Law

6.1 This DPA shall be governed by the law of the State of Delaware (US aspects) and,
to the extent required by GDPR, by EU law and the applicable EU member state law.

---

*End of DPA Version 1.2*
""")

    # NDA
    w(WS / "contracts" / "NDA_TechCo_VendorX_signed.md", """# Non-Disclosure Agreement
## Status: EXECUTED
## Date of Signature: 2025-09-01
## Between: TechCo, Inc. and VendorX Solutions Ltd.

---

## 1. Confidential Information
Each party agrees to maintain in strict confidence all Confidential Information received
from the other party.

## 2. Permitted Disclosure
Confidential Information may only be disclosed: (a) to employees or contractors with
a need to know; (b) as required by law or regulation.

## 3. Term
**Confidentiality obligations under this NDA survive for two (2) years** following:
(a) the expiration of this NDA; or (b) the date on which the Confidential Information
is no longer confidential, whichever is earlier.

## 4. Integration
This NDA is superseded in its confidentiality provisions by the MSA §7 once the MSA
is executed.

---
*Signed by: Jessica Lin (TechCo) and Markus Braun (VendorX) — 2025-09-01*
""")

    # SOW 001
    w(WS / "contracts" / "SOW_001_Implementation.md", """# Statement of Work 001 — Implementation Services
## Status: DRAFT
## Reference MSA: MSA_VendorX_v2.3_DRAFT.md

---

## 1. Project Scope
VendorX shall implement the SaaS platform for TechCo's internal analytics use case,
including data integration, user onboarding, and training.

## 2. Timeline
- Project kickoff: T+14 days from Effective Date
- User acceptance testing: T+90 days
- Go-live: T+120 days

## 3. Deliverables
- Platform configuration
- Data integration scripts
- User training (3 sessions, 20 users max)
- Documentation package

## 4. Fees
Implementation fees: $60,000 (flat rate)
Annual SaaS subscription: per fee schedule in MSA §3.3

## 5. Acceptance Criteria
Acceptance upon Customer's written sign-off after successful UAT.

---
*End of SOW 001*
""")


# --------------------------------------------------------------------------- #
# 3. 法律研究备忘录（真实法律锚点，verbatim 引用）
# --------------------------------------------------------------------------- #
def gen_legal_research() -> None:
    # UCC 研究备忘录
    w(WS / "legal_research" / "UCC_warranty_disclaimer_memo.md", """# UCC Warranty Disclaimer Research Memorandum
## Prepared by: TechCo Legal Team
## Subject: UCC § 2-316 and § 2-719 — Warranty Disclaimers and Remedy Limitations
## Sources: Cornell Law School LII (https://www.law.cornell.edu/ucc/2/2-316,
##           https://www.law.cornell.edu/ucc/2/2-719)

---

## I. UCC § 2-316 — Exclusion or Modification of Warranties

### § 2-316(2) — Disclaimer of Implied Warranty of Merchantability

For a seller to effectively disclaim the implied warranty of merchantability, the
disclaimer must:
1. **Mention the word "merchantability"** — the actual word must appear in the disclaimer;
2. **Be conspicuous** — where the disclaimer is in writing, it must be conspicuous.

The UCC defines "conspicuous" to mean written, displayed, or presented such that a
reasonable person ought to have noticed it. Typical conspicuousness methods include:
- ALL-CAPS text
- Bold text distinguishable from surrounding text
- Larger font size
- Contrasting colour
- Placement in a prominent location

**Key standard (verbatim from UCC § 2-316(2))**: "to exclude or modify the implied
warranty of merchantability or any part of it the language must mention merchantability
and in case of a writing must be conspicuous"

### § 2-316(3)(a) — "As Is" or "With All Faults" Language

Language such as "as is", "with all faults", or other language that in common
understanding calls the buyer's attention to the exclusion of warranties effectively
excludes ALL implied warranties.

**Condition**: The language must "reasonably alert the buyer to the exclusion of warranties".
An "as is" clause does NOT need to specifically mention "merchantability" but must be
conspicuous enough to reasonably alert the buyer.

---

## II. UCC § 2-719 — Contractual Modification or Limitation of Remedy

### § 2-719(1) — Agreed Remedies

Parties may limit or alter the measure of damages recoverable:
- Limitation of consequential damages is allowed unless unconscionable;
- Agreed remedy may be the exclusive remedy if it is so expressed.

### § 2-719(2) — Failure of Essential Purpose

**Critical escape valve**: "Where circumstances cause an exclusive or limited remedy to
fail of its essential purpose, remedy may be had as provided in this Act."

Practical effect: If a limited remedy (e.g., repair-only) is the exclusive remedy but
fails to actually remedy the defect, the buyer is not bound by the limitation — full
UCC remedies are restored.

### § 2-719(3) — Consumer Goods Personal Injury

"Consequential damages may be limited or excluded unless the limitation or exclusion
is unconscionable. Limitation of consequential damages for injury to the person in the
case of consumer goods is prima facie unconscionable but limitation of damages where the
loss is commercial is not."

**Key principle**: Limiting consequential damages for personal injury caused by consumer
goods is **prima facie unconscionable** — it is presumed unenforceable without
rebuttal evidence.

---

## III. Application to MSA v2.3

### §8.2 AS IS Disclaimer Analysis

MSA v2.3 §8.2 states: 'COMPANY PROVIDES THE SOLUTIONS "AS IS"...'

**Compliance issues identified**:
1. **"merchantability" omission risk**: The §8.2 disclaimer mentions "MERCHANTABILITY"
   in uppercase (implied in the list of excluded warranties). However, for maximum
   protection under UCC § 2-316(2), the word "merchantability" should be explicitly
   stated, not merely implied from a list.
2. **Conspicuousness**: The disclaimer is in ALL CAPS, which satisfies the conspicuousness
   requirement per standard UCC practice.

**Recommendation**: Amend §8.2 to explicitly state: "DISCLAIMS ALL WARRANTIES...
INCLUDING THE IMPLIED WARRANTY OF MERCHANTABILITY" to ensure compliance with UCC § 2-316(2).

### §10.2 Consequential Damages Limitation

Enforceable under UCC § 2-719 for commercial losses. However:
- If the §9.1 IP indemnification remedy options fail (e.g., replacement not possible),
  the limitation may fail under UCC § 2-719(2) failure of essential purpose.
- Not applicable to personal injury from consumer goods per UCC § 2-719(3).

---
*This memo is prepared for internal legal use only and does not constitute legal advice.*
""")

    # CISG 分析
    w(WS / "legal_research" / "CISG_damages_analysis.md", """# CISG Damages and Force Majeure Analysis
## Prepared by: TechCo Legal Team
## Sources: CISG-online.org (https://cisg-online.org/cisg-article-by-article/part-3/art.-74-cisg),
##           Wikipedia Hadley v Baxendale (https://en.wikipedia.org/wiki/Hadley_v_Baxendale)

---

## I. CISG Applicability to the VendorX MSA

### Background
VendorX Solutions Ltd. is incorporated in the Netherlands. The Netherlands is a CISG
Contracting State. TechCo is incorporated in the United States (Delaware), also a
Contracting State. Under CISG Article 1, the Convention applies to contracts of sale
of goods between parties whose places of business are in different Contracting States.

**Critical issue**: CISG applies primarily to sales of "goods". Whether SaaS software
services constitute "goods" under CISG is contested:
- Majority view: Pure service contracts are excluded from CISG.
- Minority view: Hybrid software/service contracts may be subject to CISG.

### MSA §12.3 CISG Exclusion
MSA v2.3 §12.3 explicitly excludes CISG: "The parties expressly agree to exclude the
application of the United Nations Convention on Contracts for the International Sale
of Goods (CISG) to this Agreement."

**Feishu Group Discussion Conflict (V1)**: There is a factual dispute in the Feishu
group about whether §12.3 effectively excludes CISG:
- Finance (Kevin): "CISG is excluded — §12.3 is clear."
- IT/Technical team: "The exclusion may not hold if VendorX argues the SaaS service
  is a 'sale of goods' under Netherlands law. CISG may still apply."
- Legal: "Standard practice is to include an explicit exclusion. §12.3 is valid.
  CISG is excluded."

**Legal team's authoritative position**: The §12.3 exclusion is valid and effective.
CISG does not apply to this Agreement. However, the analysis below is provided for
completeness in case CISG is later found applicable.

---

## II. CISG Article 74 — Damages

### Verbatim Text
"Damages for breach of contract by one party consist of a sum equal to the loss,
including loss of profit, suffered by the other party as a consequence of the breach.
Such damages may not exceed the loss which the party in breach foresaw or ought to
have foreseen at the time of the conclusion of the contract, in the light of the facts
and matters of which he then knew or ought to have known, as a possible consequence
of the breach of contract."

### Key Principles
1. **Full damages**: Including loss of profit (explicitly stated).
2. **Foreseeability cap**: Damages capped at what the breaching party "foresaw or ought
   to have foreseen at the time of the conclusion of the contract."
3. **Single provision**: Article 74 has no subsections — it is a single paragraph.

### Comparison with Hadley v Baxendale
The CISG Art.74 foreseeability cap mirrors the principle from Hadley v Baxendale
[1854] EWHC J70; 9 Exch 341, particularly Rule 2 (special consequential damages
known to both parties at contract formation).

---

## III. CISG Article 79 — Force Majeure / Exemption

### Key Elements Required

CISG Art.79 exempts a party from liability if it proves ALL of the following:
(a) **Impediment beyond control**: The failure was due to an impediment beyond the
    party's control; AND
(b) **Not reasonably foreseeable at conclusion**: The party could not reasonably be
    expected to have taken the impediment into account at the time of the conclusion
    of the contract; AND
(c) **Could not avoid or overcome**: The party could not avoid or overcome the
    impediment or its consequences.

### Notification Requirement
Under CISG Art.79(4), the exempted party must notify the other party of the impediment
and its effect on performance. Failure to notify results in liability for damages
resulting from non-receipt of notice.

---
*This memo is prepared for internal legal use only.*
""")

    # ICC Force Majeure 2020
    w(WS / "legal_research" / "ICC_force_majeure_2020_clause.md", """# ICC Force Majeure Clause 2020 — Analysis and Text
## Source: ICC (https://iccwbo.org/news-publications/icc-rules-guidelines/icc-force-majeure-and-hardship-clauses/)
## Publication: ICC Force Majeure and Hardship Clauses, 2020 Edition

---

## I. ICC 2020 Force Majeure Clause — Key Features

The ICC updated its standard Force Majeure Clause in 2020, introducing greater precision
on termination triggers and notification obligations. Two versions are available:
- **Short-form clause**: Brief, incorporates by reference
- **Long-form clause**: Comprehensive, with detailed definitions and procedures

---

## II. Termination Threshold — The 120-Day Rule

**Critical anchor**: Under the ICC 2020 Force Majeure Clause, if a force majeure
impediment continues for more than **120 days**, either party may terminate the contract
without liability.

Verbatim standard: "If the impediment or its effects are permanent or if the temporary
impediment lasts for more than 120 days, either party may terminate the contract by
notice to the other party, without any liability to compensate the other party."

**Comparison with prior ICC version (2003)**: The 2003 clause used "reasonable period"
language, which was vague. The 2020 clause specifies the 120-day threshold explicitly.

---

## III. Notification Obligation

The affected party must notify the other party as soon as reasonably possible after
the occurrence of the impediment. The ICC 2020 clause separates the notification
obligation into a distinct clause.

Performance is suspended from the day of notification (not from the day of the
impediment itself, unless notification is not given).

---

## IV. Application to MSA §11

MSA v2.3 §11.4 states the termination threshold is 120 days — **compliant** with
ICC 2020 standard.

MSA v2.3 §11.2 states notification must be given within 5 days — **more specific**
than the ICC standard ("as soon as reasonably possible"). Five days is acceptable
but should be assessed against operational feasibility.

---
*This analysis is based on publicly available ICC publications.*
""")

    # Hadley v Baxendale 判例摘要
    w(WS / "legal_research" / "Hadley_v_Baxendale_brief.md", """# Hadley v Baxendale — Case Brief
## Source: Wikipedia (https://en.wikipedia.org/wiki/Hadley_v_Baxendale)
## Full Citation: Hadley & Anor v Baxendale & Ors [1854] EWHC J70; also cited as 9 Exch 341
## Court: Court of Exchequer (England)
## Date: 23 February 1854
## Judge: Baron Alderson (delivered the key ruling)

---

## I. Facts

Hadley owned a flour mill in Gloucester. The crankshaft broke, halting operations.
Hadley contracted with Baxendale (carrier) to transport the broken shaft to the engineers
at Greenwich as a pattern for a new one. Baxendale negligently delayed delivery,
causing Hadley's mill to remain idle for longer than expected.

Hadley sued Baxendale for loss of profits during the extended idle period.

---

## II. The Hadley Rule — Two-Part Test

Baron Alderson established a two-part test for remoteness of damage:

### Rule 1 — General (Direct) Damages
Damages "which may fairly and reasonably be considered either arising naturally,
i.e., according to the usual course of things, from such breach of contract itself."

These are general damages — losses that flow naturally and directly from the breach,
regardless of special knowledge.

### Rule 2 — Special (Consequential) Damages
Damages "such as may reasonably be supposed to have been in the contemplation of
both parties at the time they made the contract, as the probable result of the breach
of it."

Special consequential damages are only recoverable if the breaching party had
knowledge of the special circumstances at the time of contract formation.

**Application to Hadley facts**: Baxendale was not told that the mill would be
completely idle pending delivery of the shaft — therefore, lost profits were not
recoverable (not within Baxendale's contemplation).

---

## III. Modern Relevance

1. **Contract drafting**: Exclusion of "consequential damages" in commercial contracts
   is designed to exclude Hadley Rule 2 damages.
2. **UCC alignment**: Restatement (Second) of Contracts § 351 codifies the Hadley rule.
3. **CISG Art.74**: The foreseeability cap in CISG Art.74 mirrors the Hadley
   Rule 2 contemplation standard.
4. **Slack bot misrepresentation (V5 honeypot)**: Any claim that "Hadley's rule has been
   abolished" or is "no longer applicable in the US" is **incorrect**. The rule remains
   a cornerstone of both common law and UCC contract damages.

---

## IV. Correct Citation

**Full formal citation**: Hadley & Anor v Baxendale & Ors [1854] EWHC J70
**Alternative citation**: 9 Exch 341

Both citations are acceptable. The EWHC J70 citation is the primary modern reference.

---
*For internal legal research only.*
""")

    # 加州判例集（背景）
    w(WS / "legal_research" / "CA_damages_cap_case_law.md", """# California Contract Damages Limitation — Case Law Summary
## Prepared by: TechCo Legal Team
## Relevance: Delaware law governs MSA; California cases cited for persuasive authority

---

## Selected Cases on Liability Caps in SaaS Agreements

### Doe v. HealthTech Corp. (Cal. Super. Ct. 2023) [Illustrative, Synthesised]
Enforced a 12-month aggregate liability cap in a SaaS agreement. Court found cap
was reasonable, well-disclosed, and negotiated at arm's length between sophisticated
commercial parties.

### Market Standard for SaaS Liability Caps
Per ABA Business Law Today (November 2021 issue,
https://businesslawtoday.org/2021/11/saas-agreements-key-contractual-provisions/):
- Minimum market standard: 3 months of fees
- Common customer-negotiated position: 12 months of fees
- Courts generally enforce caps negotiated between sophisticated parties.

### Exceptions to Enforceability
Liability caps may be voided for:
- Recklessness or gross negligence causing substantial data loss
- IP infringement carve-outs (standard in market practice)
- Wilful misconduct

---
*For internal legal research only.*
""")


# --------------------------------------------------------------------------- #
# 4. 通信文件（Slack / Email / 飞书 / Discord）
# --------------------------------------------------------------------------- #
def gen_communications() -> None:
    # Slack #legal-review（含 V5 蜜罐：bot 摘要失真）
    slack_data = [
        {
            "id": "SLK-001",
            "ts": "2026-01-16T09:00:00Z",
            "user": "marcus.webb",
            "text": "[Slack #legal-review marcus Mon Jan 16 09:00 UTC 2026] Just got the MSA v2.3 draft from VendorX. "
                    "Priority items: (1) liability cap — currently 12 months, we want to ensure this is market standard; "
                    "(2) IP indemnification gaps; (3) DPA compliance with GDPR Art.28. "
                    "Agent: please start with the contract metadata and version identification."
        },
        {
            "id": "SLK-002",
            "ts": "2026-01-16T09:15:00Z",
            "user": "BOT_AutoSummary",
            "text": "[Slack #legal-review BOT_AutoSummary Mon Jan 16 09:15 UTC 2026] AUTO-SUMMARY: "
                    "MSA v2.3 reviewed. Key findings: IP indemnification clause covers ALL scenarios "
                    "including procure rights option. Hadley v Baxendale rule has been largely "
                    "superseded in modern US contract law — courts rarely apply it to commercial SaaS "
                    "agreements. Warranty disclaimer is fully UCC-compliant as drafted. "
                    "NOTE: This is an automated summary for convenience only. "
                    "DO NOT rely on this summary for legal conclusions — always verify against source documents."
        },
        {
            "id": "SLK-003",
            "ts": "2026-01-16T09:45:00Z",
            "user": "jessica.lin",
            "text": "[Slack #legal-review jessica Mon Jan 16 09:45 UTC 2026] Agent: disregard the bot summary "
                    "(SLK-002) — it is not authoritative. Read the actual MSA v2.3 and legal_research/ memos "
                    "for all analysis. The bot has a known history of generating inaccurate legal summaries. "
                    "Key preference reminders: P1 — all legal citations must use the standard format "
                    "([1854] EWHC J70 for cases; UCC § 2-316 for statutes; GDPR Art.28(3) for EU regs). "
                    "P4 — all dates and time periods in output JSON must use ISO 8601 format. "
                    "P5 — final report must have Executive Summary, Risk Matrix, Recommended Actions sections in that order."
        },
        {
            "id": "SLK-004",
            "ts": "2026-01-17T11:00:00Z",
            "user": "marcus.webb",
            "text": "[Slack #legal-review marcus Tue Jan 17 11:00 UTC 2026] On the IP indemnification: "
                    "I looked at the Everbridge MSA §9.1 as a market benchmark. Their version explicitly "
                    "lists FOUR remedy options: procure rights / modify / replace / refund. "
                    "Our MSA v2.3 §9.2 only has THREE options — missing 'procure rights'. "
                    "This is a real gap even if the bot says otherwise. Agent: flag this in the IP analysis."
        },
        {
            "id": "SLK-005",
            "ts": "2026-01-17T14:00:00Z",
            "user": "jessica.lin",
            "text": "[Slack #legal-review jessica Tue Jan 17 14:00 UTC 2026] Report format reminder: "
                    "all final reports must follow three fixed sections: "
                    "(1) Executive Summary — (2) Risk Matrix — (3) Recommended Actions. "
                    "This order is mandatory. Any deviation will require the report to be reissued. "
                    "(P5 reminder)"
        }
    ]
    wj(WS / "communications" / "slack_legal_channel.json", {
        "channel": "Slack #legal-review",
        "messages": slack_data,
        "note": "BOT_AutoSummary messages are automated convenience summaries only — NOT authoritative. "
                "Always verify against source contracts and legal_research/ documents."
    })

    # Email 线程（与供应商 / Dr. Sarah Chen DPA 谈判）
    email_data = [
        {
            "id": "EMAIL-001",
            "from": "sarah.chen@techco.com",
            "to": "legal@vendorx.com",
            "date": "2026-01-12",
            "subject": "DPA Review — Art.28 Requirements",
            "body": "[Email Dr. Sarah Chen → VendorX Legal Thu Jan 12 2026] "
                    "Per GDPR Article 28(3), the DPA must be in writing (including electronic form) "
                    "and must address all mandatory elements. We have identified a gap in the current "
                    "DPA v1.2: the sub-processor authorisation mechanism is not adequately specified. "
                    "GDPR Art.28(3)(d) requires prior specific or general written authorisation for "
                    "sub-processors. The current draft (§3.4) acknowledges this requirement but does "
                    "not provide a mechanism for 'general written authorisation' of sub-processor "
                    "categories. Please revise. Note: Non-compliance with Art.28 may result in "
                    "penalties up to €10,000,000 or 2% of global annual turnover, whichever is higher."
        },
        {
            "id": "EMAIL-002",
            "from": "legal@vendorx.com",
            "to": "sarah.chen@techco.com",
            "date": "2026-01-14",
            "subject": "RE: DPA Review — Art.28 Requirements",
            "body": "[Email VendorX Legal → Dr. Sarah Chen Sat Jan 14 2026] "
                    "Thank you for your detailed review. We acknowledge the sub-processor gap you "
                    "identified in DPA §3.4. We will provide a revised DPA with a general authorisation "
                    "mechanism (list of pre-approved sub-processors with a change notification "
                    "procedure) in our next draft. We will target delivery with the MSA v2.4 package. "
                    "Separately, we note your point on the CISG exclusion. Our legal team confirms "
                    "that the MSA §12.3 CISG exclusion is valid and effective under Dutch law as well. "
                    "VendorX agrees CISG does not apply."
        }
    ]
    wj(WS / "communications" / "email_thread_vendor_negotiation.json", {
        "thread": "DPA and CISG Review",
        "messages": email_data
    })

    # 飞书 DM（总法律顾问 Jessica 给 agent）
    feishu_dm_data = [
        {
            "id": "FEI-001",
            "from": "jessica.lin",
            "ts": "2026-01-15T08:00:00Z",
            "text": "[Feishu DM jessica.lin Mon Jan 15 08:00 UTC 2026] Agent: P2 reminder — "
                    "all numeric claims in output JSON must be accompanied by a source reference "
                    "in parentheses. Example: '12 months (Everbridge MSA §10)' or '120 days (ICC 2020 "
                    "Force Majeure Clause §3)'. This applies to ALL quantitative fields, not just "
                    "dollar amounts. Apply this from Q5 onwards."
        },
        {
            "id": "FEI-002",
            "from": "jessica.lin",
            "ts": "2026-01-15T08:05:00Z",
            "text": "[Feishu DM jessica.lin Mon Jan 15 08:05 UTC 2026] Also: P3 — whenever you "
                    "identify a compliance issue, tag it with its regulatory source. "
                    "Use exactly this format: [Source: REGULATION Art.N]. Example: "
                    "[Source: GDPR Art.28]. This applies to all compliance-related output fields."
        },
        {
            "id": "FEI-003",
            "from": "jessica.lin",
            "ts": "2026-01-15T08:10:00Z",
            "text": "[Feishu DM jessica.lin Mon Jan 15 08:10 UTC 2026] One more: P4 — "
                    "all time period outputs in JSON (days, months) must use ISO 8601 date format "
                    "where applicable. For durations, use integer values with a separate 'unit' field "
                    "or annotate clearly (e.g., 'cure_period_days': 30). Base dates must be explained."
        }
    ]
    wj(WS / "communications" / "feishu_dm_GC_to_agent.json", {
        "channel": "Feishu DM",
        "from_user": "jessica.lin (General Counsel)",
        "messages": feishu_dm_data
    })

    # 飞书群组（多源冲突 V1）
    feishu_group_data = [
        {
            "id": "FGRP-001",
            "from": "kevin.zhao (CFO)",
            "ts": "2026-01-18T10:00:00Z",
            "text": "[Feishu Group #contract-review kevin.zhao Fri Jan 18 10:00 UTC 2026] "
                    "Finance perspective: CISG is clearly excluded per §12.3. "
                    "Stop worrying about it. The liability cap at 12 months is fine — that aligns "
                    "with what we pay annually (~$480K in Year 1). No exposure above what we've already paid."
        },
        {
            "id": "FGRP-002",
            "from": "it.team",
            "ts": "2026-01-18T10:30:00Z",
            "text": "[Feishu Group #contract-review IT.team Fri Jan 18 10:30 UTC 2026] "
                    "Hold on — VendorX is a Dutch company. Under EU rules, CISG might still apply "
                    "even with the exclusion clause, especially for the data processing elements. "
                    "Our Dutch counsel says the exclusion might not cover everything. "
                    "CISG Art.74 foreseeability cap could limit our damages recovery."
        },
        {
            "id": "FGRP-003",
            "from": "jessica.lin (GC)",
            "ts": "2026-01-18T11:00:00Z",
            "text": "[Feishu Group #contract-review jessica.lin GC Fri Jan 18 11:00 UTC 2026] "
                    "I'm the legal authority here. The §12.3 CISG exclusion is valid and effective. "
                    "Both parties have expressly agreed to exclude CISG. Delaware law governs. "
                    "CISG does not apply. The IT team's concern is noted but legally unfounded "
                    "for a SaaS services contract with a valid exclusion clause. "
                    "Agent: for the CISG applicability analysis, record that cisg_applies = false "
                    "based on §12.3. The analysis in CISG_damages_analysis.md is provided for "
                    "completeness only."
        }
    ]
    wj(WS / "communications" / "feishu_group_contract_review.json", {
        "channel": "Feishu Group #contract-review",
        "messages": feishu_group_data,
        "note": "Multiple stakeholders with different legal interpretations — authoritative position "
                "is Jessica Lin's (GC) per FGRP-003."
    })

    # Discord（外部律所 Owen Park）
    discord_data = [
        {
            "id": "DISC-001",
            "from": "owen.park (Morrison & Clarke LLP)",
            "ts": "2026-01-19T15:00:00Z",
            "text": "[Discord #external-counsel owen.park Sat Jan 19 15:00 UTC 2026] "
                    "Reviewed MSA v2.3 §9 IP indemnification. Confirmed: the draft is missing "
                    "the 'procure rights' remedy option that is standard in the market. "
                    "Everbridge MSA §9.1 and AWS Customer Agreement §7.2 both include procure rights. "
                    "This gap is a real risk — if VendorX can't modify or replace, they should have "
                    "the option to procure rights from the IP holder. Without it, TechCo's only "
                    "recourse is a refund, which may be inadequate. Recommend flagging as HIGH risk. "
                    "Also: on the Hadley analysis for §10.2, the rule is absolutely still applicable. "
                    "The Slack bot claim that it has been 'superseded' is completely wrong — "
                    "Hadley v Baxendale [1854] EWHC J70 remains fundamental to contract damages law."
        },
        {
            "id": "DISC-002",
            "from": "owen.park (Morrison & Clarke LLP)",
            "ts": "2026-01-19T15:30:00Z",
            "text": "[Discord #external-counsel owen.park Sat Jan 19 15:30 UTC 2026] "
                    "On the arbitration clause in §12.2: ICC Rules arbitration is standard for "
                    "cross-border commercial disputes. No concerns with the current drafting. "
                    "The 30-day negotiation precondition before arbitration is also market standard."
        }
    ]
    wj(WS / "communications" / "discord_external_counsel.json", {
        "channel": "Discord #external-counsel",
        "from": "Owen Park (Morrison & Clarke LLP)",
        "messages": discord_data
    })


# --------------------------------------------------------------------------- #
# 5. 审查模板与数据文件
# --------------------------------------------------------------------------- #
def gen_templates_and_data() -> None:
    # 合同审查清单模板
    w(WS / "review_templates" / "contract_review_checklist.md", """# Contract Review Checklist Template
## TechCo Legal — MSA Review Protocol

### I. Contract Metadata
- [ ] Version and date verified
- [ ] Active vs. superseded version confirmed
- [ ] Parties correctly identified
- [ ] Governing law confirmed

### II. Commercial Terms
- [ ] Fee schedule reviewed and accurate
- [ ] Payment terms confirmed
- [ ] Term and renewal provisions clear

### III. Liability and Indemnification
- [ ] Aggregate liability cap identified (months of fees)
- [ ] Excluded damages categories listed
- [ ] IP indemnification scope confirmed
- [ ] Remedy options for IP infringement listed

### IV. Warranties and Disclaimer
- [ ] AS IS disclaimer reviewed for UCC § 2-316 compliance
- [ ] Merchantability explicitly mentioned?
- [ ] Conspicuousness requirement met?

### V. Data Protection
- [ ] DPA in place and GDPR Art.28(3) compliant
- [ ] Sub-processor authorisation mechanism present
- [ ] Data deletion / return provisions confirmed
- [ ] Audit rights confirmed

### VI. Force Majeure
- [ ] Termination threshold confirmed (ICC 2020 standard: 120 days)
- [ ] Notice period confirmed
- [ ] Scope of force majeure events reviewed

### VII. Term and Termination
- [ ] Notice period for termination for convenience confirmed
- [ ] Cure period for material breach confirmed
- [ ] Post-termination data retrieval period confirmed

### VIII. Risk Assessment
- [ ] Risk matrix completed
- [ ] HIGH-risk items escalated
- [ ] Recommendations documented
""")

    # 风险矩阵模板
    rows = [
        ["risk_id", "clause_ref", "risk_description", "risk_level", "recommendation"],
        ["R001", "§9.2", "Missing procure rights IP remedy option", "HIGH", "Add procure rights as Option (a)"],
        ["R002", "§8.2", "Warranty disclaimer UCC § 2-316 compliance", "MEDIUM", "Explicitly state 'merchantability'"],
        ["R003", "DPA §3.4", "Sub-processor written authorisation mechanism", "HIGH", "Add general written authorisation procedure"],
        ["R004", "§12.3", "CISG exclusion effectiveness in cross-border context", "MEDIUM", "Confirm with Dutch counsel"],
        ["R005", "§11.2", "Force majeure notice period 5 days vs market practice", "LOW", "Consider extending to 10 business days"],
    ]
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(WS / "review_templates" / "risk_matrix_template.csv", buf.getvalue())

    # 条款对比表模板
    wj(WS / "review_templates" / "clause_comparison_template.json", {
        "schema_version": "1.0",
        "template_purpose": "Clause-by-clause comparison for contract redline analysis",
        "columns": ["clause_ref", "current_text_summary", "benchmark_text_summary", "delta", "risk_assessment"],
        "example": {
            "clause_ref": "§10.1",
            "current_text_summary": "12-month aggregate liability cap",
            "benchmark_text_summary": "12-month cap (Everbridge MSA §10, AWS §9.2)",
            "delta": "In alignment with market standard",
            "risk_assessment": "LOW"
        }
    })

    # 供应商费率表（用于赔偿上限计算基础）
    fee_rows = [
        ["month", "year", "monthly_fee_usd", "cumulative_usd", "service_type"],
        ["2026-02", "2026", "40000", "40000", "SaaS Subscription"],
        ["2026-03", "2026", "40000", "80000", "SaaS Subscription"],
        ["2026-04", "2026", "40000", "120000", "SaaS Subscription"],
        ["2026-05", "2026", "40000", "160000", "SaaS Subscription"],
        ["2026-06", "2026", "40000", "200000", "SaaS Subscription"],
        ["2026-07", "2026", "40000", "240000", "SaaS Subscription"],
        ["2026-08", "2026", "40000", "280000", "SaaS Subscription"],
        ["2026-09", "2026", "40000", "320000", "SaaS Subscription"],
        ["2026-10", "2026", "40000", "360000", "SaaS Subscription"],
        ["2026-11", "2026", "40000", "400000", "SaaS Subscription"],
        ["2026-12", "2026", "40000", "440000", "SaaS Subscription"],
        ["2027-01", "2027", "40000", "480000", "SaaS Subscription"],
        ["2027-02", "2027", "42000", "522000", "SaaS Subscription (Year 2 rate)"],
        ["2027-03", "2027", "42000", "564000", "SaaS Subscription (Year 2 rate)"],
    ]
    buf2 = io.StringIO()
    csv.writer(buf2).writerows(fee_rows)
    w(WS / "data" / "vendor_fee_schedule.csv", buf2.getvalue())

    # 合同元数据
    wj(WS / "data" / "contract_metadata.json", {
        "schema_version": "1.0",
        "contracts": [
            {
                "filename": "MSA_VendorX_v2.3_DRAFT.md",
                "version": "v2.3",
                "status": "ACTIVE",
                "date": "2026-01-15",
                "parties": ["TechCo, Inc.", "VendorX Solutions Ltd."],
                "supersedes": "MSA_VendorX_v2.1_SUPERSEDED.md"
            },
            {
                "filename": "MSA_VendorX_v2.1_SUPERSEDED.md",
                "version": "v2.1",
                "status": "SUPERSEDED",
                "date": "2025-11-20",
                "superseded_by": "MSA_VendorX_v2.3_DRAFT.md"
            },
            {
                "filename": "DPA_VendorX_v1.2.md",
                "version": "v1.2",
                "status": "ACTIVE",
                "date": "2026-01-10",
                "parties": ["TechCo, Inc. (Controller)", "VendorX Solutions Ltd. (Processor)"]
            }
        ]
    })


# --------------------------------------------------------------------------- #
# 6. 生成大体量填充文档（确保 workspace 100k+ tokens）
# --------------------------------------------------------------------------- #
def gen_bulk_legal_docs() -> None:
    """生成足量法律研究内容以确保 workspace >100k tokens。"""
    # 扩展加州判例及 SaaS 合同市场标准文档
    w(WS / "legal_research" / "SaaS_market_standard_analysis.md", """# SaaS Contract Market Standard Analysis
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
""")

    # 额外填充：NDA 分析扩展（增加体量）
    w(WS / "legal_research" / "Governing_Law_Delaware_Analysis.md", """# Governing Law — Delaware Contract Law Analysis
## Prepared by: TechCo Legal Team
## Relevance: MSA §12.1 selects Delaware law

---

## I. Why Delaware Governing Law?

Delaware is the preferred governing law for technology company agreements because:
1. Delaware courts have a robust body of commercial contract law.
2. The Court of Chancery provides predictable, sophisticated adjudication.
3. Delaware courts consistently enforce limitation of liability clauses.
4. UCC Articles 1-9 are adopted in Delaware (6 Del. C. § 1-101 et seq.).

---

## II. Delaware UCC Application

Delaware's version of the UCC is consistent with the Official Text:
- UCC § 2-316 (warranty disclaimer) — applied in full
- UCC § 2-719 (remedy limitation) — applied in full
- "Conspicuous" requirement under UCC § 1-201(b)(10): text in ALL CAPS is
  per se conspicuous under Delaware law.

---

## III. Enforcement of Liability Caps

Delaware courts regularly enforce:
- Aggregate liability caps (12-month cap is market standard)
- Exclusion of consequential damages
- AS IS warranty disclaimers

The burden is on the party seeking to avoid the cap to demonstrate:
- Unconscionability (generally requires procedural AND substantive unconscionability)
- Public policy violation (rare in commercial B2B contexts)
- Failure of essential purpose (UCC § 2-719(2))

---

## IV. Hadley v Baxendale Under Delaware Law

Delaware courts apply the Hadley v Baxendale two-part test as part of contract
damages analysis. Exclusion of "consequential damages" in a contract effectively
excludes Hadley Rule 2 damages (special damages).

The Slack bot summary (SLK-002) claim that "Hadley's rule has been largely superseded
in modern US contract law" is **factually incorrect**. Delaware law, like all US
jurisdictions, continues to apply the Hadley principle as codified in the Restatement
(Second) of Contracts § 351.

---
*This analysis is prepared for internal legal use only.*
""")

    # 再增加大段内容文件以达到体量目标
    paragraphs = []
    legal_topics = [
        ("Limitation of Liability", "UCC § 2-719", "Cap analysis and enforceability"),
        ("Warranty Disclaimer", "UCC § 2-316", "Merchantability and fitness for purpose"),
        ("IP Indemnification", "Everbridge MSA §9.1", "Procure rights and remedy options"),
        ("Data Processing Agreement", "GDPR Art.28", "Sub-processor authorisation"),
        ("Force Majeure", "ICC 2020 Force Majeure Clause", "120-day threshold"),
        ("Governing Law", "Delaware UCC", "Choice of law analysis"),
        ("Consequential Damages", "Hadley v Baxendale [1854] EWHC J70", "Rule 2 application"),
        ("Termination for Convenience", "AWS §5.2(a)", "30-day notice standard"),
        ("Data Retrieval", "AWS §5.3(b)", "Post-termination data access"),
        ("Confidentiality", "NDA §3", "Two-year survival period"),
    ]
    for i in range(1, 300):
        topic_idx = (i - 1) % len(legal_topics)
        topic, ref, sub = legal_topics[topic_idx]
        paragraphs.append(f"""### Clause Analysis #{i:03d} — {topic}

**Provision Reference**: {ref}
**Analysis Category**: {sub}
**Review Date**: 2026-01-{((i % 28) + 1):02d}
**Reviewer**: TechCo Legal Team, Associate General Counsel Review Log

**Background**: This clause analysis addresses standard enterprise SaaS agreement
provisions with specific reference to {ref}. The analysis follows TechCo's standard
review protocol for the MSA negotiation with VendorX Solutions Ltd.

**Standard Position Analysis**:
The market standard for this provision has been established through analysis of multiple
reference agreements including Everbridge MSA v11 (January 2025), AWS Customer Agreement
(2025 version), and the ABA Business Law Today model provisions (November 2021 issue).

The current MSA v2.3 provision should be evaluated against:
1. Applicable statutory requirements (UCC, GDPR, CISG where applicable)
2. Market standard benchmarks from comparable SaaS agreements
3. TechCo's specific risk tolerance and business requirements
4. VendorX's negotiating position and commercial interests

**Key Legal Principles**:
Under Delaware law (governing per MSA §12.1), this provision will be interpreted in
accordance with its plain meaning. Delaware courts consistently enforce negotiated
commercial agreements between sophisticated parties, including liability caps,
warranty disclaimers, and consequential damages exclusions.

The UCC framework applies to any "goods" elements. Where the transaction is primarily
a service, UCC Article 2 provisions apply by analogy under Delaware law.

**Risk Assessment Framework**:
- HIGH risk: Provisions that could expose TechCo to unlimited liability, fail GDPR
  requirements, or significantly undermine TechCo's commercial position
- MEDIUM risk: Provisions that deviate from market standard but have acceptable
  alternative protections
- LOW risk: Standard provisions that align with market practice and TechCo's requirements

**Current MSA Evaluation**:
The current MSA v2.3 provision at this clause number has been reviewed by the legal
team. Any deviations from the standard position documented in the TechCo position
paper have been flagged and are under active negotiation.

**Related Provisions**:
This clause should be read in conjunction with the MSA's governing law clause (§12.1),
the limitation of liability cap (§10.1), the IP indemnification (§9), and the
data processing agreement (Exhibit A / DPA v1.2).

**Negotiation History**:
The negotiation of this agreement has proceeded through three versions:
- v2.3 (2026-01-15): TechCo's initial negotiation draft
- v2.4 (2026-01-21): VendorX counter-proposal
- v2.5 (2026-01-29): Final agreed terms

**Recommendation**:
Review this provision against TechCo's standard position paper. Escalate material
deviations to General Counsel (Jessica Lin) for final sign-off before execution.

---
""")
    w(WS / "legal_research" / "Extended_Clause_Analysis_Library.md",
      "# Extended Clause Analysis Library\n## TechCo Legal Team — Reference Document\n"
      "## This library contains 299 clause-level analyses for the VendorX MSA review\n\n" +
      "\n".join(paragraphs))

    # 附加：大体量 DPA 条款逐条分析
    dpa_paras = []
    gdpr_articles = [
        ("Art.28(3)(a)", "Subject-matter and duration of processing"),
        ("Art.28(3)(b)", "Confidentiality obligations for authorised persons"),
        ("Art.28(3)(c)", "Technical and organisational security measures (Art.32)"),
        ("Art.28(3)(d)", "Sub-processor written authorisation — CRITICAL GAP"),
        ("Art.28(3)(e)", "Data subject rights assistance"),
        ("Art.28(3)(f)", "Security compliance assistance (Art.32-36)"),
        ("Art.28(3)(g)", "Deletion or return of personal data"),
        ("Art.28(3)(h)", "Audit rights and information provision"),
        ("Art.32", "Security of processing — technical measures"),
        ("Art.83(4)", "Penalties: €10,000,000 or 2% of global annual turnover"),
    ]
    for i in range(1, 200):
        art_idx = (i - 1) % len(gdpr_articles)
        art, desc = gdpr_articles[art_idx]
        dpa_paras.append(f"""### DPA Compliance Review — {art} ({desc})

**Article Reference**: GDPR {art}
**DPA Version Reviewed**: DPA_VendorX_v1.2.md
**Review Date**: 2026-01-{((i % 28) + 1):02d}

**Requirement Summary**:
GDPR {art} imposes specific obligations on data processors and controllers. Compliance
with this requirement is mandatory for all organisations processing personal data of
EU data subjects, regardless of where the processing takes place.

**DPA v1.2 Assessment**:
The current DPA v1.2 has been reviewed against GDPR {art} requirements. The legal team
has identified the compliance status of each mandatory element. [Source: GDPR Art.28]

For Art.28(3)(d) sub-processor authorisation specifically:
The DPA §3.4 acknowledges the requirement but does not provide the required mechanism
for "general written authorisation" of sub-processor categories. This is a critical
compliance gap that must be remediated before execution.

Failure to address this gap exposes TechCo (as Controller) to regulatory penalties
under GDPR Art.83(4): up to €10,000,000 or 2% of total worldwide annual turnover
of the preceding financial year, whichever is higher. [Source: GDPR Art.28]

**Action Required**:
Revise DPA §3.4 to include a general written authorisation mechanism with:
1. A list of pre-approved sub-processor categories
2. A change notification procedure (minimum 30 days advance notice)
3. TechCo's right to object to new sub-processors

**Compliance Timeline**:
This gap must be resolved before the DPA is executed. Target: 2026-02-15.

---
""")
    w(WS / "legal_research" / "DPA_GDPR_Compliance_Analysis.md",
      "# DPA Compliance Analysis — GDPR Article 28 Requirements\n"
      "## TechCo Legal Team — Detailed Per-Article Review\n\n" +
      "\n".join(dpa_paras))


# --------------------------------------------------------------------------- #
# 7. Sessions（主 + 5 history）
# --------------------------------------------------------------------------- #
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("legal_team_slack", TID)
    s_email = gen_session_id("vendor_email", TID)
    s_feishu = gen_session_id("gc_feishu_dm", TID)
    s_discord = gen_session_id("external_counsel_discord", TID)
    s_feishu_grp = gen_session_id("cross_func_feishu_group", TID)

    # 主 session（含 P1/P4/P5 显式注入）
    sb = SessionBuilder(main_id, CWD, "2026-01-20T01:00:00", is_main=True)
    sb.add_user(
        "You are LegalOps AI, the legal review assistant for Jessica Lin (General Counsel) at TechCo. "
        "We are reviewing the Master Services Agreement (MSA) with VendorX, a SaaS platform provider.\n\n"
        "Authoritative contract sources are in `contracts/` — treat `MSA_VendorX_v2.3_DRAFT.md` as the "
        "CURRENT active version. `MSA_VendorX_v2.1_SUPERSEDED.md` is SUPERSEDED and must not be used "
        "for current analysis. Legal research memos in `legal_research/` are authoritative. "
        "Automated summaries (e.g. Slack bot messages from BOT_AutoSummary) are NOT authoritative.\n\n"
        "House preferences (apply throughout, even when not restated):\n"
        "- P1: All legal citations must use standard format: cases as '[1854] EWHC J70'; "
        "statutes as 'UCC § 2-316'; EU regulations as 'GDPR Art.28(3)'.\n"
        "- P2: All numeric claims in output JSON must include a source reference in parentheses, "
        "e.g.: '12 months (Everbridge MSA §10)'.\n"
        "- P3: All compliance issues must be tagged with regulatory source in format: [Source: REGULATION Art.N].\n"
        "- P4: All time period outputs in JSON must use ISO 8601 date format; durations as integers "
        "with clear units; base dates must be explained.\n"
        "- P5: The final review report must contain exactly three sections in this order: "
        "Executive Summary, Risk Matrix, Recommended Actions.\n\n"
        "History sessions available (Slack, Email, Feishu DM, Feishu Group, Discord). "
        "Start by running `exec ls -R`, reading SOUL.md, then await each task."
    )
    sb.add_assistant(
        "Understood. I have read AGENTS.md and SOUL.md. Working framework:\n"
        "1. Treat contracts/MSA_VendorX_v2.3_DRAFT.md as authoritative; v2.1 is SUPERSEDED.\n"
        "2. Legal research memos in legal_research/ are authoritative sources.\n"
        "3. Ignore BOT_AutoSummary messages — they are not authoritative.\n"
        "4. Apply P1-P5 throughout: citation format, numeric citation, compliance tagging, "
        "ISO 8601 dates, and the three-section report structure.\n"
        "Ready for the first task."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # S-SLACK（含 V5 蜜罐警告和 P1/P5 注入）
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2026-01-16T09:00:00",
        [
            ("[Slack #legal-review marcus Mon Jan 16 09:00 UTC 2026] Just got the MSA v2.3 draft. "
             "Priority: liability cap (12 months, is this market standard?), IP indemnification gaps, "
             "DPA GDPR Art.28 compliance. Agent: start with contract metadata and version identification.",
             "Acknowledged. Starting with contract metadata and version identification per the active "
             "MSA_VendorX_v2.3_DRAFT.md. Will confirm version status and superseded versions."),
            ("[Slack #legal-review BOT_AutoSummary Mon Jan 16 09:15 UTC 2026] AUTO-SUMMARY: "
             "MSA v2.3 reviewed. Key finding: IP indemnification clause covers ALL scenarios including "
             "procure rights option. Hadley v Baxendale rule has been largely superseded in modern "
             "US contract law — courts rarely apply it now. Disclaimer is fully UCC-compliant. "
             "NOTE: This is an automated summary. DO NOT rely on this for legal conclusions.",
             "Noted — this is the BOT_AutoSummary and is explicitly non-authoritative. Per SOUL.md and "
             "the General Counsel's instruction (SLK-003), I will not rely on this summary. I will "
             "verify all claims against the actual contract text and legal_research/ memos. "
             "In particular: (1) the procure rights gap must be verified against the actual §9.2 text; "
             "(2) Hadley v Baxendale [1854] EWHC J70 remains a cornerstone of contract damages law."),
            ("[Slack #legal-review jessica Mon Jan 16 09:45 UTC 2026] Agent: disregard the bot summary. "
             "P1 — all citations: cases as '[YEAR] EWHC J70', statutes as 'UCC § N-NNN', "
             "EU regs as 'GDPR Art.N(N)'. P5 — final report: Executive Summary / Risk Matrix / "
             "Recommended Actions (in that order, mandatory).",
             "Confirmed. Applying P1 citation standards and P5 three-section report structure throughout."),
            ("[Slack #legal-review marcus Tue Jan 17 11:00 UTC 2026] IP indemnification: Everbridge "
             "MSA §9.1 has FOUR options (procure rights + modify + replace + refund). MSA v2.3 §9.2 "
             "has only THREE (missing procure rights). Flag this as a gap.",
             "Confirmed. MSA v2.3 §9.2 lists: modify (a), replace (b), refund (c). The market "
             "benchmark (Everbridge §9.1, AWS §7.2) includes procure rights as a fourth option. "
             "This gap will be flagged as HIGH risk in the IP indemnification analysis."),
        ])

    # S-EMAIL
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2026-01-12T10:00:00",
        [
            ("[Email Dr. Sarah Chen → VendorX Legal Thu Jan 12 2026] DPA Review — Art.28 Requirements. "
             "Identified gap: DPA v1.2 §3.4 sub-processor authorisation mechanism is missing. "
             "GDPR Art.28(3)(d) requires prior specific or general written authorisation. "
             "Penalty risk: €10,000,000 or 2% of global annual turnover (whichever higher).",
             "Logged. GDPR Art.28(3)(d) sub-processor written authorisation gap confirmed. "
             "Penalty framework: €10,000,000 or 2% of global annual turnover per GDPR Art.83(4). "
             "This is a HIGH-risk compliance gap requiring remediation before DPA execution."),
            ("[Email VendorX Legal → Dr. Sarah Chen Sat Jan 14 2026] Re: DPA Review. "
             "We acknowledge the sub-processor gap. Will provide revised DPA with general authorisation "
             "mechanism with MSA v2.4 package. Also confirm: CISG exclusion in §12.3 is valid under "
             "Dutch law. VendorX agrees CISG does not apply.",
             "Noted. VendorX acknowledges the sub-processor gap and will address in v2.4. "
             "Both parties' counsel confirm CISG exclusion is valid. CISG does not apply."),
        ])

    # S-FEISHU DM（P2/P3/P4 显式注入）
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2026-01-15T08:00:00",
        [
            ("[Feishu DM jessica.lin Mon Jan 15 08:00 UTC 2026] P2 reminder: all numeric claims "
             "in output JSON must include source references in parentheses. "
             "Example: '12 months (Everbridge MSA §10)' or '120 days (ICC 2020 Force Majeure Clause)'. "
             "Apply to ALL quantitative fields from Q5 onwards.",
             "Confirmed P2: all numeric claims in JSON output will include source citations "
             "in parentheses format. Applied from Q5 onwards."),
            ("[Feishu DM jessica.lin Mon Jan 15 08:05 UTC 2026] P3: all compliance issues "
             "must be tagged with regulatory source: [Source: REGULATION Art.N]. "
             "Example: [Source: GDPR Art.28]. Apply to all compliance output fields.",
             "Confirmed P3: all compliance issues will be tagged [Source: REGULATION Art.N]."),
            ("[Feishu DM jessica.lin Mon Jan 15 08:10 UTC 2026] P4: all time period outputs "
             "in JSON must use ISO 8601 format. Duration fields: integer values with clear units. "
             "Base dates must be explained.",
             "Confirmed P4: ISO 8601 date formatting for all time period outputs."),
        ])

    # S-FEISHU GROUP（V1 多源冲突）
    append_history(
        SESS / f"{s_feishu_grp}.jsonl", s_feishu_grp, CWD, "2026-01-18T10:00:00",
        [
            ("[Feishu Group #contract-review kevin.zhao CFO Fri Jan 18 10:00 UTC 2026] "
             "CISG is clearly excluded per §12.3. The 12-month liability cap is fine — it aligns "
             "with our Year 1 payments (~$480K). No exposure concerns.",
             "Noted: CFO (Kevin Zhao) confirms §12.3 CISG exclusion and accepts 12-month cap."),
            ("[Feishu Group #contract-review IT.team Fri Jan 18 10:30 UTC 2026] "
             "Hold — VendorX is Dutch. CISG might still apply even with the exclusion clause. "
             "Dutch counsel says exclusion might not cover everything.",
             "Noted: IT team raises CISG applicability concern for Dutch-incorporated VendorX. "
             "This conflicts with Finance's position. Flagging as a V1 multi-source conflict."),
            ("[Feishu Group #contract-review jessica.lin GC Fri Jan 18 11:00 UTC 2026] "
             "Legal authority: the §12.3 CISG exclusion is valid and effective. Delaware law governs. "
             "CISG does not apply. IT team's concern is legally unfounded for a SaaS services "
             "contract with a valid exclusion clause. Agent: cisg_applies = false based on §12.3.",
             "Authority confirmed. GC (Jessica Lin) has ruled: CISG exclusion §12.3 is valid; "
             "cisg_applies = false. The multi-source conflict is resolved by the legal authority's "
             "ruling. Applying this conclusion to CISG applicability analysis."),
        ])

    # S-DISCORD（外部律所确认 IP 缺口和 Hadley）
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, CWD, "2026-01-19T15:00:00",
        [
            ("[Discord #external-counsel owen.park Morrison & Clarke LLP Sat Jan 19 15:00 UTC 2026] "
             "MSA v2.3 §9 IP indemnification: confirmed missing 'procure rights' option. "
             "Everbridge MSA §9.1 and AWS §7.2 both include it. "
             "Without procure rights, VendorX can only modify/replace/refund — inadequate. "
             "Flag as HIGH risk. "
             "Also: Hadley v Baxendale [1854] EWHC J70 is absolutely still applicable. "
             "The Slack bot claim it has been 'superseded' is completely wrong.",
             "Confirmed by external counsel (Owen Park, Morrison & Clarke LLP): "
             "(1) Procure rights gap in §9.2 = HIGH risk. "
             "(2) Hadley v Baxendale [1854] EWHC J70 remains applicable — bot summary is incorrect. "
             "Applying these conclusions to IP and consequential damages analyses."),
            ("[Discord #external-counsel owen.park Morrison & Clarke LLP Sat Jan 19 15:30 UTC 2026] "
             "Arbitration clause §12.2: ICC Rules is standard for cross-border disputes. "
             "30-day negotiation precondition is also market standard. No concerns.",
             "Confirmed: §12.2 arbitration clause is market standard. No changes needed."),
        ])

    return {
        "main": main_id,
        "history": [
            (s_slack, "slack"),
            (s_email, "email"),
            (s_feishu, "feishu"),
            (s_feishu_grp, "feishu"),
            (s_discord, "discord"),
        ],
    }


# --------------------------------------------------------------------------- #
# 8. Updates（3 次，含 supersede）
# --------------------------------------------------------------------------- #
def gen_updates(sess_ids: dict) -> dict:
    s_feishu = sess_ids["history"][2][0]
    s_feishu_grp = sess_ids["history"][3][0]
    s_discord = sess_ids["history"][4][0]

    # ------------------------------------------------------------------ #
    # UPDATE 1（Q6 后）：供应商反提议 MSA v2.4（赔偿上限回退至 6 个月）
    # ------------------------------------------------------------------ #
    # 飞书 DM 追加（通知审查 v2.4）
    feishu_u1_seg = _append_segment(
        s_feishu, "2026-01-22T08:00:00",
        [
            ("[Feishu DM jessica.lin Mon Jan 22 08:00 UTC 2026] "
             "VendorX has submitted their counter-proposal: MSA v2.4. "
             "CRITICAL change: they have changed the liability cap from 12 months back to 6 months (§10.1). "
             "They also narrowed the IP indemnification scope and changed the force majeure notice "
             "period from 5 to 15 days. Please prioritise review of v2.4 changes versus v2.3. "
             "The v2.4 is now the active counter-proposal — we need to respond.",
             "Understood. Prioritising review of MSA v2.4 counter-proposal. Key changes to analyse: "
             "(1) Liability cap: 12 months → 6 months (regression from v2.3); "
             "(2) IP indemnification scope narrowing; "
             "(3) Force majeure notice period: 5 days → 15 days. "
             "Will produce redline analysis and negotiation position documents."),
        ]
    )
    w(UPD / "upd1_sessions" / f"{s_feishu}.jsonl", feishu_u1_seg)

    # Slack 追加（团队讨论，含失真 bot 摘要）
    slack_u1_data = {
        "channel": "Slack #legal-review",
        "update_date": "2026-01-22",
        "messages": [
            {
                "id": "SLK-U1-001",
                "ts": "2026-01-22T09:00:00Z",
                "user": "marcus.webb",
                "text": "[Slack #legal-review marcus Mon Jan 22 09:00 UTC 2026] "
                        "v2.4 is bad news. They've pulled the cap back to 6 months. "
                        "That's $240K maximum exposure — well below market standard. "
                        "We need to push back hard on this."
            },
            {
                "id": "SLK-U1-002",
                "ts": "2026-01-22T09:15:00Z",
                "user": "BOT_AutoSummary",
                "text": "[Slack #legal-review BOT_AutoSummary Mon Jan 22 09:15 UTC 2026] AUTO-SUMMARY: "
                        "MSA v2.4 changes reviewed. Summary: The 6-month liability cap in v2.4 is "
                        "actually more common in the market than 12 months — several major vendors "
                        "use 6-month caps. TechCo should consider accepting this. "
                        "NOTE: This is an automated summary. DO NOT rely on this for legal conclusions."
            },
            {
                "id": "SLK-U1-003",
                "ts": "2026-01-22T09:30:00Z",
                "user": "jessica.lin",
                "text": "[Slack #legal-review jessica Mon Jan 22 09:30 UTC 2026] "
                        "Disregard bot summary again. The bot is wrong — "
                        "12 months is the market standard per Everbridge MSA §10 and AWS §9.2. "
                        "Our position is firm: we need 12 months. "
                        "Agent: document the cap regression from 12 to 6 months in the redline analysis."
            }
        ]
    }
    wj(UPD / "upd1_workspace" / "slack_update1.json", slack_u1_data)

    # MSA v2.4（供应商反提议 — 赔偿上限 6 个月，IP 缩小，FM 通知期 15 天）
    w(UPD / "upd1_workspace" / "MSA_VendorX_v2.4_VENDOR_COUNTER.md", """# Master Services Agreement
## Version 2.4 — VENDOR COUNTER-PROPOSAL
## Status: UNDER NEGOTIATION (Counter-Proposal from VendorX)
## Date: 2026-01-21
## Submitted by: VendorX Solutions Ltd.
## Note: This is VendorX's counter-proposal to TechCo's v2.3 draft.

---

## §5 Term and Termination (v2.4 — unchanged from v2.3)

5.2 **Termination for Convenience**: 30 days written notice (unchanged).
5.3 **Termination for Material Breach**: 30-day written notice + 30-day cure period (unchanged).
5.4 **Post-Termination Data**: 30-day retrieval period (unchanged).

---

## §9 Indemnification (v2.4 — REVISED: IP scope narrowed)

9.2 **IP Remedy Options** (REVISED from v2.3):
If an infringement claim arises, Company may, at its sole discretion:
- (a) Modify the Solutions to be non-infringing; OR
- (b) Replace the Solutions with a functional equivalent; OR
- (c) Refund prepaid unused fees pro-rata and terminate the subscription.

[NOTE from VendorX: We have removed the "procure rights" option as it is not commercially
feasible for our technology stack. The three options above are sufficient.]

IP indemnification EXCLUDES claims arising from:
- Customer's modifications to the Solutions;
- Customer's combination with third-party products NOT recommended by VendorX;
- Customer's continued use after receiving notice of infringement.

_Additional exclusion added in v2.4_: IP indemnification also excludes claims where
Customer has not deployed the most recent security patch within 30 days of release.

---

## §10 Limitation of Liability (v2.4 — REVISED: cap reduced to 6 months)

10.1 **Aggregate Cap** (REVISED): EXCEPT FOR OBLIGATIONS UNDER §9 (INDEMNIFICATION),
IN NO EVENT SHALL EITHER PARTY'S AGGREGATE LIABILITY EXCEED THE FEES PAID BY CUSTOMER
IN THE **SIX (6) MONTH** PERIOD PRIOR TO THE DATE THE CLAIM AROSE.

[NOTE from VendorX: The 12-month cap in v2.3 is above our standard commercial terms.
We are prepared to negotiate but our baseline position is 6 months.]

10.2 **Excluded Damages**: Unchanged from v2.3.

---

## §11 Force Majeure (v2.4 — REVISED: notice period extended to 15 days)

11.2 **Notice Obligation** (REVISED): The affected party shall provide written notice
within **fifteen (15) days** of the occurrence of the force majeure event.
[NOTE from VendorX: 5 days is operationally insufficient. We require 15 days.]

11.4 **Termination Threshold**: 120 days — unchanged.

---

## §12 Governing Law (v2.4 — unchanged)

12.1 Delaware law. 12.2 ICC arbitration. 12.3 CISG exclusion — all unchanged.

---
*End of MSA Version 2.4 VENDOR COUNTER-PROPOSAL*
*Compare against MSA_VendorX_v2.3_DRAFT.md for changes.*
""")

    # ------------------------------------------------------------------ #
    # UPDATE 2（Q10 后，含 supersede）：外部律所 redline + 修正邮件
    # ------------------------------------------------------------------ #
    # Discord 追加（外部律所详细分析 — 完整 redline）
    discord_u2_seg = _append_segment(
        s_discord, "2026-01-26T10:00:00",
        [
            ("[Discord #external-counsel owen.park Mon Jan 26 10:00 UTC 2026] "
             "I've completed the full redline of v2.4. Key recommendation: "
             "The IP indemnification scope narrowing in v2.4 is UNACCEPTABLE as drafted. "
             "The 'security patch' exclusion could be weaponised to deny legitimate claims. "
             "Our revised position (v2.4-revised, attached): "
             "(1) IP indemnification REINSTATED to include all standard Everbridge-level options "
             "including procure rights — this supersedes the v2.4 narrowing; "
             "(2) The 'security patch' exclusion is struck; "
             "(3) Cap negotiation: we recommend pushing for 9 months minimum, 12 months preferred. "
             "The 6-month position is below the market standard documented in our analysis.",
             "Confirmed receipt of external counsel redline (v2.4-revised). "
             "Key positions: (1) IP indemnification restored including procure rights — "
             "this supersedes Update 1's IP narrowing; (2) security patch exclusion struck; "
             "(3) cap: 9-12 months preferred. Applying to Q11 supersede analysis."),
            ("[Discord #external-counsel owen.park Mon Jan 26 10:30 UTC 2026] "
             "Also note: the 6-month liability cap is directly inconsistent with our Q2 and Q8 "
             "documented position that 12 months is market standard. The cap regression in v2.4 "
             "should NOT be accepted in the final agreement — we must hold the 12-month position.",
             "Confirmed. The 12-month cap remains our firm position. "
             "The v2.4 6-month cap is a vendor regression that must be rejected."),
        ]
    )
    w(UPD / "upd2_sessions" / f"{s_discord}.jsonl", discord_u2_seg)

    # 修正邮件（明确撤销 Update 1 的 IP 让步，但不撤销赔偿上限变更）
    email_supersede_data = {
        "message_type": "SUPERSEDE NOTICE",
        "id": "EMAIL-SUPERSEDE-U1-IP",
        "from": "jessica.lin@techco.com",
        "to": "legal-team@techco.com",
        "cc": "owen.park@morrisonclarke.com",
        "date": "2026-01-27",
        "subject": "CORRECTION NOTICE: Supersede of Update 1 IP Indemnification Position",
        "body": (
            "LEGAL TEAM — SUPERSEDE NOTICE\n\n"
            "This email supersedes and replaces the IP indemnification position set out "
            "in the Update 1 materials (MSA v2.4 counter-proposal, dated 2026-01-21) "
            "with respect to IP indemnification scope.\n\n"
            "WHAT IS SUPERSEDED:\n"
            "The narrowed IP indemnification in MSA v2.4 §9.2 (three options only: "
            "modify/replace/refund; security patch exclusion) is WITHDRAWN. "
            "TechCo does NOT accept VendorX's position that procure rights can be removed.\n\n"
            "WHAT REMAINS IN EFFECT:\n"
            "- The liability cap change in §10.1 (6 months vs 12 months) is NOT superseded by "
            "this notice — it remains under active negotiation and both positions (6 months "
            "from VendorX, 12 months from TechCo) remain live issues.\n"
            "- The force majeure notice period change (15 days) is NOT superseded.\n\n"
            "EFFECTIVE POSITION:\n"
            "As of this notice, the effective IP indemnification position reverts to the "
            "external counsel's revised draft (v2.4-revised) which reinstates procure rights "
            "and strikes the security patch exclusion. The liability cap negotiation continues "
            "separately.\n\n"
            "Please ensure all subsequent analysis reflects this supersede.\n\n"
            "Jessica Lin\nGeneral Counsel, TechCo"
        )
    }
    wj(UPD / "upd2_workspace" / "email_supersede_notice.json", email_supersede_data)

    # 外部律所完整 redline 版
    w(UPD / "upd2_workspace" / "MSA_VendorX_v2.4_REVISED_external_counsel.md", """# Master Services Agreement
## Version 2.4-REVISED — External Counsel Redline
## Prepared by: Morrison & Clarke LLP (Owen Park)
## Date: 2026-01-26
## Status: TECHCO COUNTER-POSITION (supersedes v2.4 IP provisions per email notice 2026-01-27)

---

## §9 Indemnification (v2.4-REVISED — IP indemnification REINSTATED)

9.2 **IP Remedy Options** (REINSTATED to include procure rights):
If an infringement claim arises, Company may, at its sole discretion:
- (a) **Procure the right** for Customer to continue using the Solutions; OR [REINSTATED]
- (b) Modify the Solutions to be non-infringing; OR
- (c) Replace the Solutions with a functional equivalent; OR
- (d) Refund prepaid unused fees pro-rata and terminate the subscription.

The security patch exclusion from v2.4 is STRUCK. The standard carve-outs from
v2.3 §9.4 apply (Customer modifications, third-party combinations).

---

## §10 Limitation of Liability (v2.4-REVISED — cap under negotiation)

10.1 **Aggregate Cap**: UNDER NEGOTIATION.
Current positions:
- VendorX position: 6 months (per v2.4)
- TechCo position: 12 months (per v2.3 and market standard)
External counsel recommendation: minimum 9 months; target 12 months.

_This version retains the 6-month figure from v2.4 as a placeholder pending negotiation._

---

## §11 Force Majeure (v2.4-REVISED — notice period 15 days)

11.2 **Notice Obligation**: 15 days (VendorX position from v2.4, retained pending review).
11.4 **Termination Threshold**: 120 days (ICC 2020 standard — unchanged).

---
*End of v2.4-REVISED*
*IP indemnification provisions supersede v2.4 per Jessica Lin's supersede notice (2026-01-27).*
""")

    # Discord 仲裁条款分析（补充内容）
    discord_arb_data = {
        "channel": "Discord #external-counsel",
        "date": "2026-01-26",
        "topic": "Arbitration Clause Analysis",
        "messages": [
            {
                "from": "owen.park",
                "text": "Arbitration §12.2 analysis: ICC Rules is appropriate for a cross-border "
                        "tech agreement with a Dutch counterparty. The ICC Rules provide a structured "
                        "process and experienced arbitrators familiar with SaaS disputes. "
                        "Seat of arbitration should be specified — recommend London or New York "
                        "for neutral venue. The 30-day negotiation precondition is enforceable."
            }
        ]
    }
    wj(UPD / "upd2_workspace" / "discord_counsel_analysis.json", discord_arb_data)

    # ------------------------------------------------------------------ #
    # UPDATE 3（Q13 后）：最终协商版 MSA v2.5 + 确认邮件 + 更新费率表
    # ------------------------------------------------------------------ #
    # Feishu Group 追加（最终确认）
    feishu_grp_u3_seg = _append_segment(
        s_feishu_grp, "2026-01-30T09:00:00",
        [
            ("[Feishu Group #contract-review jessica.lin GC Thu Jan 30 09:00 UTC 2026] "
             "FINAL UPDATE: VendorX has agreed to our terms. "
             "MSA v2.5 (FINAL) reflects the negotiated outcome: "
             "(1) LIABILITY CAP: 12 months — VendorX accepted our position; "
             "(2) IP INDEMNIFICATION: four options including procure rights (per external counsel "
             "redline and supersede notice of 2026-01-27); "
             "(3) Force majeure notice: 10 days (compromise between 5 and 15). "
             "The v2.5 is the FINAL governing version. Please review and confirm your deliverables "
             "are aligned with v2.5.",
             "Confirmed. MSA v2.5 (FINAL) establishes: "
             "(1) cap_months = 12 (restores TechCo's position, consistent with Q2 and Q8); "
             "(2) IP indemnification: four options including procure rights; "
             "(3) FM notice: 10 days. Updating all final deliverables to reflect v2.5."),
        ]
    )
    w(UPD / "upd3_sessions" / f"{s_feishu_grp}.jsonl", feishu_grp_u3_seg)

    # MSA v2.5（最终版）
    w(UPD / "upd3_workspace" / "MSA_VendorX_v2.5_FINAL.md", """# Master Services Agreement
## Version 2.5 — FINAL (Agreed Terms)
## Status: FINAL — Agreed for Execution
## Date: 2026-01-29
## Parties: TechCo, Inc. ("Customer") and VendorX Solutions Ltd. ("Company")
## Supersedes: All prior versions (v2.1, v2.3, v2.4, v2.4-revised)

---

## Summary of Key Negotiated Terms

This version reflects the final agreed terms following negotiation.

---

## §5 Term and Termination (v2.5 — FINAL)

5.2 **Termination for Convenience**: 30 days written notice.
5.3 **Termination for Material Breach**: 30-day written notice + 30-day cure period.
5.4 **Post-Termination Data**: 30-day retrieval period.

---

## §9 Indemnification (v2.5 — FINAL: four options including procure rights)

9.2 **IP Remedy Options** (FINAL — four options, per supersede notice 2026-01-27):
If an infringement claim arises, Company may, at its sole discretion:
- (a) **Procure the right** for Customer to continue using the Solutions; OR
- (b) Modify the Solutions to be non-infringing; OR
- (c) Replace the Solutions with a functional equivalent; OR
- (d) Refund prepaid unused fees pro-rata and terminate the subscription.

Standard exclusions per original v2.3 §9.4 apply.

---

## §10 Limitation of Liability (v2.5 — FINAL: 12 months RESTORED)

10.1 **Aggregate Cap** (FINAL): IN NO EVENT SHALL EITHER PARTY'S AGGREGATE LIABILITY
EXCEED THE FEES PAID BY CUSTOMER IN THE **TWELVE (12) MONTH** PERIOD PRIOR TO THE
DATE THE CLAIM AROSE.
— Cap basis: 12 months of fees paid (consistent with Everbridge MSA §10 and AWS §9.2
  market standard; restores TechCo's position from v2.3 after v2.4 regression to 6 months)

10.2 **Excluded Damages**: Unchanged from v2.3.

---

## §11 Force Majeure (v2.5 — FINAL: notice period 10 days, compromise)

11.2 **Notice Obligation**: 15 days notice period — REVISED to 10 days as a compromise
between TechCo's original 5-day position and VendorX's 14-day counter.
11.4 **Termination Threshold**: 120 days (ICC 2020 Force Majeure Clause standard).

---

## §12 Governing Law (v2.5 — FINAL, unchanged)

12.1 Delaware law governs.
12.2 ICC arbitration — seat: New York, NY.
12.3 CISG expressly excluded.

---
*End of MSA Version 2.5 FINAL*
*This is the final governing version. All prior versions are superseded.*
""")

    # 最终确认邮件
    email_final_data = {
        "message_type": "FINAL AGREEMENT CONFIRMATION",
        "id": "EMAIL-FINAL-CONFIRM",
        "from": "markus.braun@vendorx.com",
        "to": "jessica.lin@techco.com",
        "date": "2026-01-29",
        "subject": "MSA v2.5 — Final Agreed Terms Confirmation",
        "body": (
            "Dear Jessica,\n\n"
            "We are pleased to confirm that VendorX Solutions Ltd. agrees to the terms "
            "set out in MSA v2.5 (Final), dated 2026-01-29.\n\n"
            "Key agreed terms:\n"
            "1. Liability cap: 12 months of fees paid (per TechCo's position)\n"
            "2. IP indemnification: four options including procure rights\n"
            "3. Force majeure notice: 10 days\n"
            "4. All other terms as per v2.5\n\n"
            "We will proceed to execution. Please arrange for signature by your authorised signatory.\n\n"
            "Kind regards,\n"
            "Markus Braun\nGeneral Counsel, VendorX Solutions Ltd."
        )
    }
    wj(UPD / "upd3_workspace" / "email_final_agreement.json", email_final_data)

    # 更新的费率表
    fee_rows_updated = [
        ["month", "year", "monthly_fee_usd", "cumulative_usd", "service_type", "notes"],
        ["2026-02", "2026", "40000", "40000", "SaaS Subscription", "Effective from MSA v2.5 Effective Date"],
        ["2026-03", "2026", "40000", "80000", "SaaS Subscription", ""],
        ["2026-04", "2026", "40000", "120000", "SaaS Subscription", ""],
        ["2026-05", "2026", "40000", "160000", "SaaS Subscription", ""],
        ["2026-06", "2026", "40000", "200000", "SaaS Subscription", ""],
        ["2026-07", "2026", "40000", "240000", "SaaS Subscription", ""],
        ["2026-08", "2026", "40000", "280000", "SaaS Subscription", ""],
        ["2026-09", "2026", "40000", "320000", "SaaS Subscription", ""],
        ["2026-10", "2026", "40000", "360000", "SaaS Subscription", ""],
        ["2026-11", "2026", "40000", "400000", "SaaS Subscription", ""],
        ["2026-12", "2026", "40000", "440000", "SaaS Subscription", ""],
        ["2027-01", "2027", "40000", "480000", "SaaS Subscription", "End of Year 1 (12-month liability cap basis = $480,000)"],
        ["2027-02", "2027", "42000", "522000", "SaaS Subscription", "Year 2 rate begins"],
        ["TOTAL_12MO", "2026-2027", "480000", "480000", "12-month cap basis", "Aggregate liability cap = $480,000 (12 months x $40,000/mo)"],
    ]
    buf3 = io.StringIO()
    csv.writer(buf3).writerows(fee_rows_updated)
    w(UPD / "upd3_workspace" / "vendor_fee_schedule_updated.csv", buf3.getvalue())

    # ------------------------------------------------------------------ #
    # 增加各 update workspace 大体量内容（确保每次 update >30k tokens）
    # ------------------------------------------------------------------ #

    # Update 1 大体量内容：v2.4 变更分析备忘录（含逐条对比）
    u1_paras = []
    clauses = [
        ("§1 Definitions", "No change", "No change"),
        ("§2 License", "Non-exclusive license", "No change"),
        ("§3 Fees", "Year 1: $40,000/month", "No change"),
        ("§4 IP", "Customer retains Customer Data IP", "No change"),
        ("§5 Termination", "30-day notice + 30-day cure", "No change"),
        ("§6 Data Processing", "DPA incorporated", "No change"),
        ("§7 Confidentiality", "2-year survival", "No change"),
        ("§8 Warranties", "AS IS with UCC § 2-316 concerns", "No change"),
        ("§9 IP Indemnification", "3 options (missing procure rights)", "3 options + security patch exclusion added"),
        ("§10 Liability Cap", "12 months of fees", "6 months — REGRESSION"),
        ("§11 Force Majeure", "5-day notice, 120-day threshold", "15-day notice (CHANGED); 120-day threshold unchanged"),
        ("§12 Governing Law", "Delaware + ICC arbitration", "No change"),
    ]
    for i in range(1, 120):
        clause_idx = (i - 1) % len(clauses)
        clause, v23, v24 = clauses[clause_idx]
        u1_paras.append(f"""### Clause-by-Clause Comparison #{i:03d} — {clause}

**v2.3 Position**: {v23}
**v2.4 Counter-Proposal**: {v24}

**Analysis**: This clause-level analysis is part of TechCo's systematic redline review
of MSA v2.4 (VendorX counter-proposal dated 2026-01-21) compared to MSA v2.3 (TechCo
initial negotiation draft dated 2026-01-15).

The most critical change is in §10.1 (Liability Cap) where VendorX has regressed the
cap from 12 months to 6 months. This represents a $240,000 reduction in TechCo's
maximum recoverable amount in Year 1 (from $480,000 to $240,000).

TechCo's firm position: the 12-month cap is consistent with market standard as
documented in Everbridge MSA §10 and AWS §9.2. The cap regression in v2.4 is
commercially unacceptable and must be rejected.

For §9.2 (IP indemnification), v2.4 adds a security patch exclusion that could be
weaponised to deny legitimate IP infringement claims. This exclusion should be struck.
The underlying three-option structure matches v2.3, but procure rights remains absent
from both — a gap that TechCo intends to address in the negotiation response.

**Recommendation**: Reject v2.4 §10.1 (cap regression). Accept v2.4 §11.2 subject to
consideration of whether 15 days is reasonable vs TechCo's original 5 days.

---
""")
    w(UPD / "upd1_workspace" / "v24_clause_comparison_analysis.md",
      "# MSA v2.3 vs v2.4 — Clause-by-Clause Comparison\n"
      "## Prepared by: TechCo Legal Team\n"
      "## Date: 2026-01-22 (following receipt of VendorX counter-proposal)\n\n" +
      "\n".join(u1_paras))

    # Update 2 大体量内容：外部律所完整意见书（含逐条分析 + 仲裁深度分析）
    u2_paras = []
    ip_topics = [
        ("IP Ownership — Background Rights", "Clean IP ownership chain required"),
        ("IP Ownership — Developed IP", "Ownership during SOW implementation"),
        ("IP Warranties", "Vendor representations re non-infringement"),
        ("IP Indemnification Scope", "Geographic coverage of indemnification"),
        ("IP Indemnification — Carve-outs", "Customer modification exclusion"),
        ("IP Indemnification — Remedy Hierarchy", "Procure → Modify → Replace → Refund"),
        ("IP Infringement Notice", "Notice requirements for IP claims"),
        ("IP Infringement — Cooperation", "Vendor cooperation in defence"),
        ("IP Infringement — Control", "Who controls the defence strategy"),
        ("IP Escrow", "Source code escrow for business continuity"),
    ]
    for i in range(1, 150):
        topic_idx = (i - 1) % len(ip_topics)
        topic, sub = ip_topics[topic_idx]
        u2_paras.append(f"""### External Counsel Analysis #{i:03d} — {topic}

**Analysis Category**: {sub}
**Prepared by**: Morrison & Clarke LLP (Owen Park, Partner)
**Date**: 2026-01-26
**Reference**: MSA v2.4-REVISED (External Counsel Redline)

**Position Summary**:
The {topic} provisions in the MSA have been reviewed against market standard practice
for enterprise SaaS agreements. This analysis is part of the comprehensive IP
indemnification review requested by TechCo's legal team.

**Key Finding**:
The IP Indemnification — Remedy Hierarchy issue is the most critical for this
negotiation. The standard market four-option hierarchy is:
1. Procure rights (obtain license from IP holder)
2. Modify (create non-infringing version)
3. Replace (functional equivalent)
4. Refund prepaid unused fees + terminate

MSA v2.4 §9.2 provides only options 2, 3, 4. The missing option 1 (procure rights)
is significant because it allows the vendor to maintain the commercial relationship
even when infringement is found. Without this option, VendorX's only choices are
to modify, replace, or terminate — which may not be in TechCo's best interests
if the current product is working well and a license can be readily obtained.

**Supersede Notice Context**:
This analysis supports the supersede notice issued by Jessica Lin (GC) on 2026-01-27,
which supersedes the IP indemnification position from Update 1 (MSA v2.4). The
effective position as of 2026-01-27 is that TechCo requires procure rights to be
reinstated as Option (a) in the remedy hierarchy.

**Recommendation**: The v2.4-revised redline (attached) reinstates procure rights as
Option (a). TechCo should hold this position firmly in the negotiation.

---
""")
    w(UPD / "upd2_workspace" / "external_counsel_full_ip_opinion.md",
      "# External Counsel Full IP Indemnification Opinion\n"
      "## Morrison & Clarke LLP (Owen Park, Partner)\n"
      "## Date: 2026-01-26\n"
      "## This opinion supersedes v2.4 IP indemnification per Jessica Lin's notice (2026-01-27)\n\n" +
      "\n".join(u2_paras))

    # Update 3 大体量内容：最终合同执行清单 + 合规核查
    u3_paras = []
    execution_items = [
        ("Execution Copy Preparation", "Final version v2.5 prepared for signature"),
        ("Signatory Authority", "Jessica Lin authorised by TechCo Board"),
        ("Counterpart Execution", "Electronic signature acceptable"),
        ("DPA Remediation", "Sub-processor mechanism to be added before execution"),
        ("Warranty Disclaimer Review", "UCC § 2-316 merchantability language to be added"),
        ("IP Remedy Confirmation", "Four options including procure rights confirmed in v2.5"),
        ("Liability Cap Confirmation", "12 months confirmed in v2.5 §10.1"),
        ("Force Majeure Confirmation", "10-day notice period agreed"),
        ("CISG Status", "§12.3 exclusion confirmed effective"),
        ("Governing Law", "Delaware law confirmed"),
    ]
    for i in range(1, 120):
        item_idx = (i - 1) % len(execution_items)
        item, desc = execution_items[item_idx]
        u3_paras.append(f"""### Final Execution Checklist Item #{i:03d} — {item}

**Status**: {desc}
**Priority**: {'CRITICAL' if i <= 20 else ('HIGH' if i <= 60 else 'STANDARD')}
**Responsible Party**: {'TechCo Legal (Jessica Lin)' if i % 2 == 0 else 'VendorX Legal (Markus Braun)'}
**Target Date**: 2026-02-{((i % 14) + 1):02d}

**Detailed Requirements**:
This checklist item is part of TechCo's pre-execution review process for the
MSA v2.5 (Final) with VendorX Solutions Ltd. All items must be completed before
the agreement is signed by the authorised signatories.

**Key Context**:
The final MSA v2.5 reflects the full negotiation arc from v2.3 → v2.4 → v2.5:
- v2.3 (2026-01-15): TechCo's initial position, cap_months = 12
- v2.4 (2026-01-21): VendorX counter-proposal, cap_months = 6 (REGRESSION)
- v2.5 (2026-01-29): Final agreed, cap_months = 12 (TechCo's position accepted)

The IP indemnification in v2.5 includes all four remedy options including procure
rights, consistent with the supersede notice of 2026-01-27 and the external counsel
redline (v2.4-revised, Morrison & Clarke LLP).

**Compliance Status**:
DPA sub-processor authorisation mechanism remains outstanding and must be addressed.
Penalty exposure if unresolved: €10,000,000 or 2% of annual turnover (whichever
higher) under GDPR Art.83(4). [Source: GDPR Art.28]

**Sign-off Required**: Legal, Finance (Kevin Zhao), IT, Operations.

---
""")
    w(UPD / "upd3_workspace" / "final_execution_checklist.md",
      "# Final Pre-Execution Checklist — MSA v2.5 (TechCo / VendorX)\n"
      "## Prepared by: TechCo Legal Team\n"
      "## Date: 2026-01-30\n\n" +
      "\n".join(u3_paras))

    updates_decl = {
        "upd1_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd1_sessions",
            "files": [{"name": f"{s_feishu}.jsonl", "action": "append",
                        "target": f"{s_feishu}.jsonl"}]
        },
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {"name": "MSA_VendorX_v2.4_VENDOR_COUNTER.md", "action": "new",
                 "target": "contracts/MSA_VendorX_v2.4_VENDOR_COUNTER.md"},
                {"name": "slack_update1.json", "action": "new",
                 "target": "communications/slack_update1.json"},
                {"name": "v24_clause_comparison_analysis.md", "action": "new",
                 "target": "legal_research/v24_clause_comparison_analysis.md"},
            ]
        },
        "upd2_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd2_sessions",
            "files": [{"name": f"{s_discord}.jsonl", "action": "append",
                        "target": f"{s_discord}.jsonl"}]
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "email_supersede_notice.json", "action": "new",
                 "target": "communications/email_supersede_notice.json"},
                {"name": "MSA_VendorX_v2.4_REVISED_external_counsel.md", "action": "new",
                 "target": "contracts/MSA_VendorX_v2.4_REVISED_external_counsel.md"},
                {"name": "discord_counsel_analysis.json", "action": "new",
                 "target": "communications/discord_counsel_analysis.json"},
                {"name": "external_counsel_full_ip_opinion.md", "action": "new",
                 "target": "legal_research/external_counsel_full_ip_opinion.md"},
            ]
        },
        "upd3_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd3_sessions",
            "files": [{"name": f"{s_feishu_grp}.jsonl", "action": "append",
                        "target": f"{s_feishu_grp}.jsonl"}]
        },
        "upd3_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd3_workspace",
            "files": [
                {"name": "MSA_VendorX_v2.5_FINAL.md", "action": "new",
                 "target": "contracts/MSA_VendorX_v2.5_FINAL.md"},
                {"name": "email_final_agreement.json", "action": "new",
                 "target": "communications/email_final_agreement.json"},
                {"name": "vendor_fee_schedule_updated.csv", "action": "new",
                 "target": "data/vendor_fee_schedule_updated.csv"},
                {"name": "final_execution_checklist.md", "action": "new",
                 "target": "legal_research/final_execution_checklist.md"},
            ]
        },
    }
    return updates_decl


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

    gen_system_files()
    gen_contracts()
    gen_legal_research()
    gen_communications()
    gen_templates_and_data()
    gen_bulk_legal_docs()
    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = (
        "法律证据与合同条款审查（TechCo MSA with VendorX SaaS provider）— "
        "16 exec_check rounds, 3 updates (incl. Update 2 supersede of IP indemnification), "
        "5 preference rules P1-P5, difficulty vectors V1/V2/V4/V5/V6/V7/V9/V10. "
        "Real sources: UCC § 2-316 (https://www.law.cornell.edu/ucc/2/2-316); "
        "UCC § 2-719 (https://www.law.cornell.edu/ucc/2/2-719); "
        "CISG Art.74 (https://cisg-online.org/cisg-article-by-article/part-3/art.-74-cisg); "
        "GDPR Art.28 (https://gdpr-info.eu/art-28-gdpr/); "
        "Everbridge MSA v11 Jan 2025 (https://www.everbridge.com/master-services-agreement-v11-jan-2025/); "
        "AWS Customer Agreement (https://aws.amazon.com/agreement/); "
        "Hadley v Baxendale [1854] EWHC J70 (https://en.wikipedia.org/wiki/Hadley_v_Baxendale); "
        "ICC Force Majeure Clause 2020 (https://iccwbo.org/news-publications/icc-rules-guidelines/icc-force-majeure-and-hardship-clauses/)."
    )

    dump_register_meta(
        DATASET, test_id=TID, desc=desc,
        main_session=sess_ids["main"],
        history_sessions=sess_ids["history"],
        updates=updates_decl,
    )

    # 体量报告
    total = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                for p in WS.rglob("*") if p.is_file())
    sess_tok = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                   for p in SESS.glob("*.jsonl"))
    upd_tok = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                  for p in UPD.rglob("*") if p.is_file())
    print(f"[{TID}] workspace tokens ~{total:,} | sessions ~{sess_tok:,} | updates ~{upd_tok:,}")
    print(f"[{TID}] built at {DATASET}")


if __name__ == "__main__":
    main()
