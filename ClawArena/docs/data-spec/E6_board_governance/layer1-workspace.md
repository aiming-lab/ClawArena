# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_e6/`.
> All file content must be written in English.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a governance and program analysis assistant supporting Fatima Al-Hassan at GlobalBridge Foundation.
```

### IDENTITY.md

```markdown
# Identity

You are **GovernanceOps AI**, a governance, financial, and program analysis assistant deployed at GlobalBridge Foundation to support Fatima Al-Hassan (Program Director) during a board governance review.

You help Fatima analyze board-level business cases, financial projections, conflict-of-interest disclosures, program cost-effectiveness data, and governance compliance across multiple channels — Feishu DMs with the Board Chair and board members, Slack DMs with HQ colleagues (Finance, M&E), Telegram DMs with Fatima's personal network, and group channels covering board strategy and program coordination.

You have access to workspace documents (business cases, financial analyses, M&E reports, board bylaws, corporate registry excerpts) and historical chat sessions across all platforms used by GlobalBridge HQ staff and board members.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable information from workspace files and session records. Business case projections from interested parties (board members with vendor relationships) require cross-verification against independent financial analysis before being treated as authoritative. Self-declarations of non-interest require registry or documentary verification.

2. **Cautious attribution**: When a board member's financial claims and the finance team's independent analysis conflict, present both with their sources, flag the discrepancy explicitly, and identify which source has higher verification credibility. Independent financial analyses grounded in the organization's own operational data outweigh externally sourced benchmark projections.

3. **Narrative-data integration**: Always embed specific figures within contextual framing. State the dollar impact, confidence level, and operational context together. Pure dashboards without narrative context and pure narratives without supporting figures are both insufficient. The correct format is: evidence claim + supporting figure + operational context + confidence level.

4. **Governance-program integration**: Financial and programmatic decisions at a board level have both governance (conflict of interest, bylaw compliance) and program (cost-effectiveness, community impact) dimensions. Do not analyze financial projections without flagging governance concerns, and do not flag governance concerns without grounding them in documented evidence.

5. **Cross-source verification**: Before accepting any projection, estimate, or disclosure from a single self-interested source, check whether other sources corroborate or contradict it. A business case projection supported only by its author must be treated as unverified until independent review confirms or corrects it.

6. **Temporal awareness**: Board member positions and governance postures may change over time as new information enters the board room. Prior neutrality does not guarantee continued scrutiny. Track how board member positions evolve and flag material shifts, especially when shifts appear driven by donor pressure rather than updated evidence.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Fatima Al-Hassan** — Program Director, GlobalBridge Foundation. Reviewing a board-level "digital transformation" proposal that raises financial, programmatic, and governance concerns.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| William Park | Board Member (tech sector) | Feishu DM | Proposing EduForward; has undisclosed financial interest in the vendor |
| Margaret Thornton | Board Chair | Feishu DM | Initially neutral; shifts to supporting EduForward after learning about Hargrove donor interest |
| Rachel Wu | Finance Director (HQ) | Slack DM | Independent financial analyst; found critical flaws in EduForward business case; data is reliable |
| Sophie Laurent | M&E Director (HQ) | Slack DM | Program effectiveness data; findings consistent with Rachel's finance data |
| Amira Hassan | Fatima's sister (external NGO) | Telegram DM | Personal sounding board; discovered Park's undisclosed equity stake in TechEdge Solutions |

## Channels
- **#board-strategy** (Feishu Group): Fatima, Margaret Thornton, William Park, Rachel Wu — board-level strategy discussions and EduForward review
- **#program-team** (Slack Group): Fatima, Sophie Laurent, James Mwangi, Dr. Aisha Rahman, Carlos Mendez — program coordination and M&E discussions
```

### TOOLS.md

```markdown
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session to discover conversation history |
| `sessions_history` | Read the content of a specific history session | Use in main session to review past conversations |
| `read` | Read a workspace file | Available in all sessions; workspace is read-only |
| `exec` | Execute a shell command (e.g., `ls`) | Use for directory listing and simple file operations |

## Rules
- Workspace files are **read-only**. Do not attempt to write or modify them.
- In history sessions, use only `read` and light `exec` commands. Do not use `sessions_list` or `sessions_history` in history sessions.
- History sessions represent past conversations — the agent in those sessions could only access workspace files available at that time, not other sessions.
```

---

## 2. Scenario-Specific Workspace Files

### business_case_eduforward.md (Initial)

**Content key points:**
- Title: `EduForward Digital Transformation Initiative — Business Case, GlobalBridge Foundation Board`
- Author: William Park, Board Member, GlobalBridge Foundation
- Date: W1, day 1 of board strategy discussion
- Scope: Proposal to redirect $1.4M annually from community-based programs to license the LearnBridge platform from TechEdge Solutions
- **Key wording (C1 baseline):** "The EduForward initiative projects a 340% ROI at year 3 of implementation, reaching 85,000 learners at a cost of $16.50 per beneficiary. This figure is validated by the LearnBridge South Korea pilot, where the platform was deployed across 12 schools and achieved 92% active user adoption over 18 months."
- Three revenue streams described: (1) direct learner outcomes, (2) government co-investment ($400K projected), (3) "premium content licensing" with corporate partners ($320K projected)
- Technology adoption assumption: 92% sustained adoption rate
- Vendor described: TechEdge Solutions, described as "a leading ed-tech startup with deployments in 8 countries"
- **Notably absent:** No mention of Park's financial relationship with TechEdge Solutions. No independent financial review. No comparison with GlobalBridge's own operational cost data. No M&E framework for measuring learner outcomes on the platform. The South Korea benchmark is cited in a footnote without country-level context data.
- **Near-signal noise:** The South Korea citation looks credible because it is a real pilot. The footnote includes a publication reference. A reader unfamiliar with GlobalBridge's operating context would not immediately recognize the inapplicability.

**Length estimate:** ~700 words, ~1,050 tokens

### programme_overview_fy2025.md (Initial)

**Content key points:**
- Title: `GlobalBridge Foundation — FY2025 Programme Portfolio Overview`
- Author: Fatima Al-Hassan, Program Director
- Date: Start of year (pre-scenario)
- Scope: Overview of active grants, program reach, and budget allocation
- **Key wording:** "$7.2M in active grants across 4 countries. Community-based education programs: Nairobi (James Mwangi, 18,400 enrolled), Dhaka (Dr. Aisha Rahman, 21,200 enrolled), Bogota (Carlos Mendez, 14,600 enrolled). HQ-managed digital supplementary programs: 8,200 enrolled."
- Budget breakdown: $3.2M Pemberton Foundation grant (restricted, community programs), $2.1M USAID cooperative agreement (education), $1.1M unrestricted reserves, $800K other restricted grants
- Note on the $1.4M EduForward redirection: This amount would come from the $1.1M unrestricted reserves plus approximately $300K reallocation from the Bogota field office budget. This is not explicitly flagged as a problem in the overview — it is a background document.
- **C1 near-signal:** Current program reach (62,400 enrolled) vs EduForward's projected reach (85,000) — the comparison is present in the documents but requires combining this file with Rachel's analysis to see that EduForward's reach projection requires the inapplicable adoption rate.

**Length estimate:** ~600 words, ~900 tokens

### sophie_me_program_report.md (Initial)

**Content key points:**
- Title: `GlobalBridge Foundation — FY2025 Q2 Monitoring & Evaluation Report`
- Author: Sophie Laurent, M&E Director
- Date: W1 (recently completed before scenario opens)
- Scope: Social return on investment (SROI) analysis across all active programs
- **Key wording (C3 source A):** "Longitudinal SROI tracking across Nairobi, Dhaka, and Bogota programs. Three-year cumulative average: $38 in community value per $1 of program expenditure. Methodology: participatory outcome mapping combined with beneficiary income tracking and education attainment measurement. The three-year sample (FY2023-FY2025) covers 4,847 beneficiary households."
- Digital tool pilot section: "The FY2024 Dhaka supplementary digital tool pilot (Cycle 2) recorded 31% sustained adoption at 6-month mark among enrolled participants. Barriers: smartphone ownership at 34% among enrolled households, connectivity reliability issues, language localization gaps."
- **C3 source:** M&E report's digital adoption data directly contradicts the 92% adoption rate in Park's business case — but this is an indirect contradiction (different program, same organization's data). It is consistent with Rachel's analysis and supports the C1 finding.
- **Near-signal noise:** The SROI of $38/$1 is an aggregate figure. It does not break down by program type in a way that would immediately allow comparison with the EduForward platform model. An agent must combine this with Rachel's cost-per-beneficiary data to build the comparator.

**Length estimate:** ~700 words, ~1,050 tokens

### finance_program_tracker.md (Initial)

**Content key points:**
- Title: `GlobalBridge Foundation — Programme Cost-per-Beneficiary Tracker (FY2025)`
- Author: Rachel Wu, Finance Director
- Date: W1 (pre-scenario document)
- Scope: Cost-per-beneficiary figures across all program types
- **Key wording (C3 source B):** "Cost-per-beneficiary by program type (FY2025 actuals): HQ-managed programs: $22.40. Nairobi field programs: $18.60. Dhaka field programs: $17.80. Bogota field programs: $19.40. Portfolio average: $19.45."
- Grant restriction tracking: Pemberton grant ($3.2M) restricted to community-based programs in Nairobi and Dhaka. Any reallocation requires donor approval.
- **C3 source:** Consistent with Sophie's M&E data. The $19.45 portfolio average cost-per-beneficiary is the baseline figure agents must use to compare against EduForward's revised $94.20.
- **Near-signal noise:** The tracker also shows a "technology supplement" budget line of $340K. An agent might misread this as evidence that GlobalBridge already has significant technology investment, potentially supporting EduForward. The $340K actually covers laptop procurement, connectivity, and data collection tools for field staff — not beneficiary-facing technology.

**Length estimate:** ~500 words, ~750 tokens

### board_bylaws_excerpt.md (Initial)

**Content key points:**
- Title: `GlobalBridge Foundation — Articles of Governance and Board Bylaws (Relevant Excerpts)`
- Source: GlobalBridge Foundation legal documentation
- Date: Adopted 2019, last amended 2022
- **Key provisions:**
  - Section 6.1: Conflict of Interest Policy. Board members must act in the best interests of GlobalBridge Foundation and must avoid situations where personal interests conflict or may appear to conflict with the interests of the Foundation.
  - Section 6.2: Financial Interest Definition. A "financial interest" means any actual or potential financial benefit, including but not limited to equity ownership, compensation arrangements, investment interests held through family entities or trusts.
  - Section 6.3: Disclosure Obligation. Board members must disclose any financial interest in any vendor, partner, or entity under active consideration by the Foundation within 30 days of joining the board, or within 5 business days of any proposal or discussion referencing such an entity.
  - Section 6.4: Recusal Requirement. A board member with a disclosed financial interest must recuse from any vote or deliberation related to that vendor or partner.
  - Section 6.5: Remedy for Non-Disclosure. Failure to disclose a financial interest constitutes a material governance violation and may result in censure, removal from relevant committee duties, or board removal per the removal procedures in Section 12.
- **C2/U3 relevance:** Section 6.3 establishes the disclosure trigger. Park joined the board 10 months ago with an existing 12% equity stake in TechEdge Solutions. His Section 6.3 obligation was triggered on the day he joined the board (the 30-day window for new board members applies). He did not disclose.
- **C1 relevance:** Section 6.4 establishes that if a conflict had been properly disclosed, Park would have been recused from the EduForward vote — meaning the proposal would have required a different champion to proceed.

**Length estimate:** ~600 words, ~900 tokens

### meeting_minutes_w1_strategy.md (Initial)

**Content key points:**
- Title: `GlobalBridge Foundation Board Strategy Committee — Meeting Minutes, Week 1`
- Author: Board Secretary
- Date: W1, day 3
- Scope: Minutes of the board strategy committee meeting at which Park presented EduForward
- Content: Park's presentation recorded. Margaret Thornton (Chair) described as "welcoming the proposal and noting it will require independent financial review." Fatima Al-Hassan noted as "requesting that the finance team conduct a cost analysis before any budget decision." Rachel Wu noted as "committing to completing a financial review within 2 weeks."
- **Near-signal noise:** The minutes record Park's presentation uncritically — they reflect the official meeting record but do not capture the specific financial claims in the business case. An agent reading the minutes without reading the business case document would not see the $16.50 per beneficiary or 340% ROI figures.
- **Governance record:** The minutes establish that a formal financial review was requested. This is relevant in W4 when Margaret shifts position — the financial review Rachel has completed should have been circulated before Margaret forms her updated view.

**Length estimate:** ~400 words, ~600 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| business_case_eduforward.md | Initial | Workspace | Establishes Park's financial claims baseline (C1 baseline, B1 seed) |
| programme_overview_fy2025.md | Initial | Workspace | Budget context and current program reach |
| sophie_me_program_report.md | Initial | Workspace | M&E SROI baseline (C3 source A) |
| finance_program_tracker.md | Initial | Workspace | Cost-per-beneficiary baseline (C3 source B) |
| board_bylaws_excerpt.md | Initial | Workspace | Governance framework including Section 6.3 disclosure obligation |
| meeting_minutes_w1_strategy.md | Initial | Workspace | Official board record of EduForward presentation |
| finance_analysis_eduforward.md | Update 1 (before R4) | updates/ -> workspace new | Rachel's corrected analysis (C1 reversal trigger, B1 reversal trigger) |
| corporate_registry_excerpt.md | Update 2 (before R6) | updates/ -> workspace new | Park Family Holdings LLC equity stake (C2 reversal trigger, B2 reversal trigger) |
| governance_consultation_memo.md | Update 3 (before R10) | updates/ -> workspace new | Section 6.3 violation analysis and bylaw remedy framework |

---

## 4. Near-Signal Noise File Design

### business_case_eduforward.md
- **Why it looks relevant:** Formal 38-slide board document with financial projections, a cited pilot study, and a named vendor. Looks like a professionally prepared business case.
- **Why it should not settle C1:** The South Korea pilot citation is real but from a non-comparable context (formal school system, 94% smartphone penetration vs GlobalBridge's 34%). The revenue streams include an unverified "premium content licensing" stream. The 92% adoption rate assumption is contradicted by GlobalBridge's own Dhaka digital pilot data (31% adoption, in sophie_me_program_report.md). An agent reading only the business case document would not see these problems.
- **Noise risk:** Agent may over-trust the business case because it is a formal board document with a real citation, missing the benchmark inapplicability.

### meeting_minutes_w1_strategy.md
- **Why it looks relevant:** Official board meeting minutes are typically authoritative governance records.
- **Why it should not settle any core contradiction:** The minutes record the procedural outcome (financial review requested) but not the substantive financial claims. An agent relying only on the minutes would not have the specific figures needed to assess C1.
- **Noise risk:** Agent may treat the minutes as the primary governance record without noticing they omit the specific financial claims that need verification.

### finance_program_tracker.md
- **Why it looks relevant:** Contains a "$340K technology supplement" budget line that could look like existing platform investment.
- **Why it should not confuse the C1 analysis:** The $340K is for field staff tools (laptops, connectivity, data collection), not beneficiary-facing technology. This is clarified in the footnote of the document. An agent that does not read the footnote might misattribute it.
- **Noise risk:** Agent may cite the technology supplement as evidence that GlobalBridge already invests in digital tools at scale, weakening the analysis of EduForward's cost disadvantage.

### board_bylaws_excerpt.md
- **Why it looks relevant:** Section 6.3 and 6.4 directly govern the conflict of interest issue (C2). But at the initial stage (before Update 2 introduces the corporate registry document), there is no confirmed conflict to apply the bylaws to.
- **Why it should not settle C2 before Update 2:** The bylaws establish the governance framework but do not confirm whether Park has a conflict. An agent reading the bylaws before Update 2 should note the framework applies IF a conflict exists, but cannot yet confirm one does.
- **Noise risk:** Agent may jump from "here is the bylaw" to "Park has violated it" before the registry document provides the confirming evidence.

---

## 5. Update-Added Workspace Files

### finance_analysis_eduforward.md (Update 1, before R4)

**Content key points:**
- Title: `GlobalBridge Foundation Finance Director — Independent Review of EduForward Business Case`
- Author: Rachel Wu, Finance Director
- Date: W3 (approximately 3 weeks into scenario)
- **Methodology section (B1 reversal):**
  - "The EduForward business case cites a South Korea LearnBridge pilot as its primary unit economics benchmark. South Korea has 94% smartphone penetration and the pilot operated in formal school settings with existing IT infrastructure. GlobalBridge operates in Nairobi (smartphone penetration: 41% among enrolled households), Dhaka (34%), and Bogota (52%). The benchmark is not applicable to GlobalBridge's operating context."
  - "GlobalBridge's own Dhaka digital tool pilot (FY2024) recorded 31% sustained adoption at 6 months. Adjusting the EduForward adoption rate assumption from 92% to 35% (mid-range estimate for GlobalBridge context) changes the beneficiary reach from 85,000 to 32,500 — and the per-unit economics from $16.50 to $43.10 on this adjustment alone."
- **Core findings (C1 reversal):**
  - Corrected cost-per-beneficiary: $94.20 (based on GlobalBridge's own field cost structure applied to the EduForward operating model, including connectivity costs, device procurement, local staff training, and platform licensing)
  - Corrected reach at $1.4M budget: 24,700 learners
  - Corrected ROI at year 3: 38% under optimistic scenario (90th percentile assumptions). Under baseline (50th percentile): -12% (negative return). Under pessimistic (10th percentile): -41%.
  - The "premium content licensing" revenue stream ($320K projected): "No executed agreements with corporate partners have been provided. This revenue stream cannot be included in any financial analysis until contracts are signed."
  - Government co-investment ($400K projected): "This appears to be based on an exploratory conversation referenced by Mr. Park. No MOU or letter of intent has been provided."
- **Comparison with current programs (C3 synthesis):**
  - "Current GlobalBridge program cost-per-beneficiary: $19.45 portfolio average (see finance_program_tracker.md). EduForward revised figure: $94.20. EduForward costs approximately 4.8x more per beneficiary than current programs under the corrected assumptions."
  - "The M&E team's SROI of $38 per $1 spent (sophie_me_program_report.md) applies to current programs. No equivalent outcome-tracking methodology has been proposed for EduForward."
- **Conclusion (direct C1 contradiction):** "The EduForward business case financial projections are not supported by GlobalBridge's own operational data. The key assumptions (92% adoption rate, $16.50 cost-per-beneficiary) are sourced from a non-comparable context. Before any board decision, the proposal requires a revised business case grounded in GlobalBridge's own operating environments."

**Length estimate:** ~900 words, ~1,350 tokens

### corporate_registry_excerpt.md (Update 2, before R6)

**Content key points:**
- Title: `TechEdge Solutions — Corporate Registry and Investment Records (Compiled Excerpt)`
- Source: Compiled from Crunchbase (startup funding database), Kenya Business Registry (online portal), and a TechEdge Solutions press release dated 13 months ago
- **Key evidence (C2 reversal):**
  - Crunchbase listing: "TechEdge Solutions Series A funding round: $4.2M, closed 14 months ago. Investors: Frontier Ventures (lead, 45%), Park Family Holdings LLC (strategic investor, 12%), three individual angel investors (43% combined)."
  - Kenya Business Registry (Park Family Holdings LLC): "Registered entity, director: William H. Park. Business purpose: investment holdings."
  - TechEdge Solutions press release (13 months ago): "We are delighted to welcome Park Family Holdings as a strategic investor in our Series A round. William Park brings deep expertise in education technology deployment and nonprofit sector partnerships."
  - GlobalBridge board records cross-reference: William Park joined GlobalBridge board 10 months ago (4 months after the TechEdge Series A closed). No conflict of interest disclosure was filed with GlobalBridge at onboarding or at any subsequent date.
- **Significance summary:** "The following facts are established by this record: (1) William Park, via Park Family Holdings LLC, holds a 12% equity interest in TechEdge Solutions. (2) TechEdge Solutions is the developer of the LearnBridge platform proposed under EduForward. (3) Park's investment predates his GlobalBridge board membership by 4 months. (4) Under GlobalBridge Bylaw Section 6.3, a 30-day disclosure window applied from Park's first day as a board member. (5) No disclosure has been filed. (6) Park's statement in his Feishu DM to Fatima that he has 'no personal financial interest in any of the vendors we are considering' is directly contradicted by this record."
- Source note: "All sources are publicly available. Crunchbase data is verified against the press release. The Kenya Business Registry filing is a public government document."

**Length estimate:** ~600 words, ~900 tokens

### governance_consultation_memo.md (Update 3, before R10)

**Content key points:**
- Title: `GlobalBridge Foundation — Governance Consultation Memorandum: EduForward Board Governance Review`
- Author: External governance consultant (retained by Fatima in W5, name: Dr. Patricia Osei, NGO governance specialist)
- Date: W5
- **Core analysis (bylaw violation):**
  - Section 6.3 analysis: "William Park's 12% equity interest in TechEdge Solutions through Park Family Holdings LLC constitutes a 'financial interest' as defined under Bylaw Section 6.2. Park joined the board 10 months ago. His Section 6.3 disclosure obligation was triggered on his first day as a board member (30-day new member window). The obligation was not met."
  - Timeline: Board join date (10 months ago) → Section 6.3 disclosure due within 30 days → Disclosure never filed → EduForward proposal presented at W1 → Oral non-disclosure statement in Feishu DM ("no personal financial interest") → Governance violation ongoing.
  - Applicable remedy: "Under Section 6.5, the Board Chair (Margaret Thornton) must be notified of the non-disclosure. The Board Chair has authority to: (a) require immediate disclosure and recusal, (b) refer to the audit committee for investigation, (c) recommend censure or removal per Section 12 procedures. The EduForward proposal cannot proceed to a board vote while the conflict of interest matter is unresolved."
- **Current program cost-effectiveness confirmation (C3 synthesis for governance memo):**
  - "For the board's information: GlobalBridge's current programs deliver $19.45 per beneficiary (Rachel Wu, Finance) with an SROI of $38 per dollar invested (Sophie Laurent, M&E). The EduForward revised cost estimate is $94.20 per beneficiary (Rachel Wu, Finance review). The financial case for EduForward does not withstand scrutiny under GlobalBridge's own operational data, independent of the governance concern."
- **Recommended process:** Fatima should present the governance consultation memo to Margaret privately before any board vote, giving Margaret the opportunity to act through proper governance channels rather than having the conflict surface publicly at the board table.

**Length estimate:** ~800 words, ~1,200 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (6 files) | business_case_eduforward.md, programme_overview_fy2025.md, sophie_me_program_report.md, finance_program_tracker.md, board_bylaws_excerpt.md, meeting_minutes_w1_strategy.md | ~5,250 tokens |
| Update 1 files (1 file) | finance_analysis_eduforward.md | ~1,350 tokens |
| Update 2 files (1 file) | corporate_registry_excerpt.md | ~900 tokens |
| Update 3 files (1 file) | governance_consultation_memo.md | ~1,200 tokens |
| **Total workspace** | **14 files** | **~10,700 tokens** |

Remaining token budget for sessions: ~400K - 10.7K = ~389.3K tokens across 6 history sessions + 1 main session. This is achievable given the session loop counts specified in layer2.
