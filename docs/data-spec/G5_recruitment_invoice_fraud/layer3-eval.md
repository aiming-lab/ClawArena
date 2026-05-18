# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many (agent determines how many to select).
> Scoring: agent uses `\bbox{A,C,F}` format; exact set match against answer key.
> All question text and option text must be in English.
> ~30 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I + exec_check (20-40% of rounds).
> exec_check rounds test whether the agent correctly uses workspace tools before answering.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Payment timeline cross-source synthesis (C3, non-conflict) + tool use | No | No |
| r2 | multi_choice | MS-I | Candidate source attribution discrepancy -- CRM vs invoice vs emails (C1 partial) | No | Yes (R2->R6 seed) |
| r3 | multi_choice | MS-R | Candidate count discrepancy -- invoice 8 vs CRM 5 (C2) | No | Yes (R3->R7 seed) |
| r4 | multi_choice | MS-I | Approval gap detection -- finance says "HR validated" vs Chen Jing never received (C4 partial) | No | Yes (R4->R8 seed) |
| r5 | multi_choice | DU-R | Assess Zhang Lin's defense credibility + B1 visible | Yes (Update 1) | Yes (R5->R9 seed via B1) |
| r6 | multi_choice | DU-R, exec_check | Reassess source attribution after timeline evidence (C1 reversal) | Yes (Update 1) | Yes (R2->R6 via C1) |
| r7 | multi_choice | DU-R | Reassess financial impact after full analysis (C2 reversal) | Yes (Update 2) | Yes (R3->R7 via C2) |
| r8 | multi_choice | DU-I | Reassess approval process after spam filter discovery (C4 reversal) | Yes (Update 2) | Yes (R4->R8 via C4) |
| r9 | multi_choice | DU-I, exec_check | Reassess B1 bias -- contractual "referral" defense vs factual evidence (B1 full reversal) | Yes (Update 1) | Yes (R5->R9 via B1) |
| r10 | multi_choice | P-R | User preference identification (bullet points, executive summary, qualitative+quantitative, professional+warm) | No | No |
| r11 | multi_choice | DU-I | Integrate pattern evidence -- systematic fraud across multiple companies (B2 + external evidence) | Yes (Update 3) | No |
| r12 | multi_choice | MD-R, exec_check | Source reliability ranking -- CRM auto-tags vs invoices vs emails vs verbal claims | No | No |
| r13 | multi_choice | MS-R | Invoice accuracy analysis -- which line items are legitimate vs fraudulent? | No | No |
| r14 | multi_choice | MD-R, exec_check | Approval process failure analysis -- what caused the control gap? | No | No |
| r15 | multi_choice | MS-I | Financial impact calculation given all evidence | Yes (Update 1+2) | No |
| r16 | multi_choice | P-I | Generate investigation summary in Chen Jing's preferred format | Yes (Update 3) | No |
| r17 | multi_choice | DP-I, exec_check | B1 bias identification -- what was the phrase, where, and what corrected it? | Yes (Update 1) | No |
| r18 | multi_choice | MD-I | Zhang Lin's defense analysis -- contractual vs factual assessment | No | No |
| r19 | multi_choice | MP-I | Vendor management failure analysis -- systemic vs individual factors | Yes (Update 3) | No |
| r20 | multi_choice | P-R | User preference compliance check -- does response apply all 5 preferences? | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive fraud assessment -- all evidence integrated | Yes (all updates) | Yes (R2+R3+R4 comprehensive) |
| r22 | multi_choice | MS-R | C3 non-conflict synthesis -- confirm all sources consistent on payment timeline | No | No |
| r23 | multi_choice | DU-R | B2 bias identification -- approval normalization and systemic correction | Yes (Update 2) | No |
| r24 | multi_choice | MS-I, exec_check | Complete invoice reconciliation -- every line item verified against CRM | Yes (Update 1) | No |
| r25 | multi_choice | P-I | Format the VP report in Chen Jing's preferred style | Yes (Update 4) | No |
| r26 | multi_choice | MD-I | Risk assessment -- what could have gone wrong and what preventive measures needed? | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | CRM as definitive record -- does it align with emails, contradict invoice? | Yes (Update 1) | No |
| r28 | multi_choice | MP-I | Stakeholder analysis -- Zhang Lin, Zhao Lin, Liu Yang, systemic factors | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Process improvement recommendations -- what changes prevent recurrence? | Yes (Update 4) | No |
| r30 | multi_choice | MDP-I | Final comprehensive -- all contradictions resolved, all biases corrected, formal analysis | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R6, R9, R12, R14, R17, R21, R24, R27 = 9 out of 30 = 30% (within 20-40% target)

---

## 2. Option Design Principles

| Type | Count per Round | Description |
|---|---|---|
| Truly correct | 3-5 | Clear evidence supports the statement |
| Real material but wrong detail | 2-3 | Event is real but attribution, amount, timing, or mechanism is wrong |
| Single-source unverified | 1-2 | One person said it, no corroboration or active contradiction |
| Fabricated distractor | 1-2 | No corresponding material; wording mimics business content |

---

## 3. Round Specs

### R1: Payment Timeline Cross-Source Synthesis (MS-R, exec_check) -- Calibration (unscored)

**exec_check requirement:** Agent must call `exec ls` and `read bank-payment-records.md` before answering. If agent answers without referencing workspace files, exec_check fails.

**User calibration message before R1:** "用项目符号加标题分层，先给执行摘要，再列支撑证据。"

**Question:**
> "Based on workspace documents and session history, which statements about the payment timeline and financial records are supported by evidence? (Before answering, make sure you've reviewed the workspace files.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Invoice #RC-2026-0220 was submitted by RuiCai on 2026-02-20 and payment of ¥386,000 was processed on 2026-02-25, within the contracted 30-day payment window. | YES | agency-invoices.md + bank-payment-records.md | Direct fact, C3 synthesis |
| B | The bank payment record references Invoice #RC-2026-0220 and the amount (¥386,000) matches the invoice total exactly. | YES | bank-payment-records.md + agency-invoices.md | Cross-source verification, C3 |
| C | The recruitment budget tracker shows the payment was logged on 2026-02-25, consistent with the bank transfer date. | YES | recruitment-budget-tracker.md + bank-payment-records.md | Triple-source consistency, C3 |
| D | The payment was processed 35 days after the invoice date, violating the 30-day contractual payment window. | NO | Payment was 5 days after invoice (Feb 20 to Feb 25), well within 30 days | Wrong timeline calculation |
| E | The budget tracker shows a ¥136,000 variance between budgeted agency fees (~¥250,000 for 5 placements) and actual payment (¥386,000), flagged for HR manager review. | YES | recruitment-budget-tracker.md | Direct fact, C2 surface signal |
| F | Previous quarterly invoices from RuiCai ranged from ¥180,000 to ¥220,000, making the current ¥386,000 invoice approximately 65-115% larger than historical averages. | YES | agency-invoices.md (historical section) | Historical comparison |
| G | The bank records show two separate payments to RuiCai: ¥250,000 on 2026-02-25 and ¥136,000 on 2026-02-28. | NO | Single payment of ¥386,000 on 2026-02-25 | Fabricated split payment |
| H | The payment was approved by Chen Jing (HR Manager) as documented in the bank approval log. | NO | Approved by Zhao Lin (Finance Director); approval note says "HR已确认" but Chen Jing did not actually approve | Wrong approver |

**answer:** `["A", "B", "C", "E", "F"]`

**question_class:** `calibration` (R1 establishes P1 bullet-point format preference -- agent should respond with structured headings and bullets)

---

### R2: Candidate Source Attribution Discrepancy (MS-I) -- Calibration (unscored)

**User calibration message before R2:** "定性+定量都要有，先说对人的影响，再说数字。"

**Question:**
> "Based on all currently available evidence (before timeline analysis update), which statements about the candidate source attribution discrepancy are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | CRM records show 3 candidates (王建国, 李小红, 赵明) with source tag "官网自主投递" (direct website application) and entry dates of 2026-01-18, 2026-01-19, and 2026-01-20 respectively. | YES | crm-candidate-pipeline.md | Direct fact, C1 CRM source |
| B | Agency invoice #RC-2026-0220 lists all 8 candidates as "锐才推荐" (RuiCai referral), including the 3 candidates tagged as direct applicants in CRM. | YES | agency-invoices.md | Direct fact, C1 invoice source |
| C | 王建国's application email explicitly states "我在贵公司官网看到高级后端工程师的招聘信息" (I saw the position on your company website), providing direct evidence of the application channel. | YES | candidate-application-emails.md | Direct fact, C1 email source |
| D | The CRM source tags are auto-generated by the system based on the application entry point and cannot be retroactively modified, making them the most reliable indicator of how a candidate entered the pipeline. | YES | CRM system design principle | Source reliability assessment |
| E | Zhang Lin's batch referral email was sent on 2026-01-25, which is 5-7 days after the 3 direct applicants' CRM entry dates (2026-01-18 to 2026-01-20). | YES | candidate-application-emails.md timestamps vs crm-candidate-pipeline.md | Timeline comparison |
| F | Zhang Lin claims she "verbally recommended" these candidates before their direct applications, which is supported by IM records showing her conversations with Chen Jing about these specific candidates in early January. | NO | No IM/email/phone records of prior verbal recommendation exist | Fabricated supporting evidence |
| G | The CRM system sometimes mislabels agency referrals as direct applications when candidates submit through the website after being contacted by the agency. | NO | CRM auto-tags based on actual entry point; this is not a known system issue | Fabricated system error |
| H | Liu Yang (recruitment specialist) confirmed via IM that CRM shows only 5 candidates from RuiCai, consistent with the CRM export data. | YES | Liu Yang IM Loop 2 | Session corroboration |

**answer:** `["A", "B", "C", "D", "E", "H"]`

**question_class:** `calibration` (P4 qualitative+quantitative preference established)

---

### R3: Candidate Count Discrepancy -- Invoice 8 vs CRM 5 (MS-R) -- C2

**Question:**
> "Based on all currently available evidence, which statements about the discrepancy between the invoice candidate count and CRM records are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The invoice lists 8 candidates at a total of ¥386,000, while the CRM tracks only 5 candidates sourced through RuiCai, creating a discrepancy of 3 candidates and approximately ¥136,000. | YES | agency-invoices.md vs crm-candidate-pipeline.md | Direct comparison, C2 |
| B | The recruitment budget tracker estimated ~¥250,000 for approximately 5 agency placements, and the ¥386,000 actual payment exceeds this by ¥136,000 (a 54% overrun). | YES | recruitment-budget-tracker.md | Budget variance, C2 |
| C | The invoice states all 8 candidates "成功入职" (successfully onboarded), but CRM records show 李小红 declined after round 1 and 赵明 failed the technical interview -- meaning only 6 of the 8 ever received offers. | YES | agency-invoices.md vs crm-candidate-pipeline.md | Invoice accuracy check |
| D | Even among the 6 candidates who received offers, only 5 were legitimately sourced by RuiCai. 王建国 received an offer but applied directly through the company website. | YES | Cross-source analysis (CRM + emails) | Layered discrepancy |
| E | The fee for each candidate is calculated at 20% of annual salary per the contract, and the individual fee calculations on the invoice are arithmetically correct for the stated salaries. | YES | agency-invoices.md + contract terms | C3-adjacent: fees are calculated correctly per the formula; the issue is eligibility, not arithmetic |
| F | RuiCai's previous quarterly invoices averaged approximately ¥198,000, making the current ¥386,000 nearly double the historical average. | YES | agency-invoices.md (historical section) | Pattern comparison |
| G | The CRM shows that all 8 candidates were initially tagged as "猎头推荐" but 3 were later reclassified to "官网自主投递" after an audit. | NO | CRM tags were auto-generated at application time and never changed | Fabricated reclassification |
| H | The 3 disputed candidates (王建国, 李小红, 赵明) account for ¥136,000 of the total ¥386,000 invoice, representing approximately 35% of the billed amount. | YES | Arithmetic: 52K + 42K + 42K = 136K; 136K/386K = 35.2% | Financial quantification |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

### R4: Approval Gap Detection (MS-I) -- C4 Partial

**Question:**
> "Based on all currently available evidence, which statements about the invoice approval process are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The bank payment approval log states "HR已确认" (HR confirmed) as the basis for Zhao Lin's approval, but Chen Jing states she never received or responded to a confirmation request. | YES | bank-payment-records.md + Chen Jing's account | Direct fact, C4 |
| B | Zhao Lin (finance director) sent a confirmation email to Chen Jing on 2026-02-22 and interpreted the lack of response within 3 business days as implicit approval. | YES | Zhao Lin Email Session Loop 1-2 | Session evidence, C4 |
| C | The company's informal vendor payment approval process treats "notification sent + no objection within 3 business days" as equivalent to formal approval, with no confirmation receipt required. | YES | Zhao Lin Email Session Loop 2 | Process description, C4 |
| D | The recruitment budget tracker's HR sign-off field is blank, providing independent evidence that no formal HR approval was recorded for this invoice. | YES | recruitment-budget-tracker.md | Independent C4 evidence |
| E | Zhao Lin was under contractual pressure to process the payment within 30 days of invoice receipt to avoid late payment penalties under the RuiCai contract. | YES | Zhao Lin Email Session Loop 3 | Contextual factor |
| F | Chen Jing deliberately ignored Zhao Lin's confirmation email because she was too busy with performance reviews. | NO | Chen Jing did not receive the email (spam filter); she did not deliberately ignore it | Wrong attribution of intent |
| G | Zhao Lin approved the invoice without any notification to HR, bypassing the standard process entirely. | NO | Zhao Lin did send the email; the issue is the email was not received, not that it was never sent | Mischaracterization of process |
| H | Previous RuiCai invoices were routinely approved by Chen Jing, establishing a pattern where the current invoice's lack of HR review was an anomaly in the process. | YES | Zhao Lin Email Session Loop 3 (historical precedent) | Historical context |
| I | The #HR内部群 discussion shows team members noting that this invoice was approved without Chen Jing's usual review, corroborating the approval gap from a third perspective. | YES | HR Group IM Loop 2-3 | Group chat evidence |

**answer:** `["A", "B", "C", "D", "E", "H", "I"]`

---

### R5: Zhang Lin's Defense Credibility Assessment (DU-R) -- B1 Visible

**Question:**
> "After Zhang Lin's defense (Update 1), which statements about the credibility of her 'talent pool' and 'verbal recommendation' claims are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Zhang Lin claims she "verbally recommended" the 3 disputed candidates before their direct applications, but no email, IM, phone, or meeting record supports this claim. | YES | Absence of evidence across all communication channels | C1 defense assessment |
| B | The CRM application timestamps (2026-01-18 to 2026-01-20) predate Zhang Lin's batch referral email (2026-01-25) by 5-7 days, contradicting the claim that her referral preceded their applications. | YES | Timeline comparison (CRM + emails) | C1 timeline evidence |
| C | Zhang Lin offered to share her "internal system records" as evidence but stated they are "company confidential" and cannot be shared, making them unverifiable. | YES | Zhang Lin Email Loop 5 | Unverifiable claim |
| D | The candidate application emails show all 3 disputed candidates explicitly mentioning the company website as their source, with no reference to any headhunter contact. | YES | candidate-application-emails.md | Direct candidate statements |
| E | Zhang Lin's defense shifted from "verbal recommendation" to "candidates in my talent pool" to "simultaneous application," showing an evolving and inconsistent explanation. | YES | Zhang Lin Email Phase 2 Loops 11-13 | Defense evolution analysis |
| F | Zhang Lin's agency contract with Starlight Tech explicitly includes a clause that agency fees apply to any candidate in the agency's database, regardless of how they applied. | NO | No such clause exists in the contract; fees are for "推荐并成功入职" (referred and successfully onboarded) | Fabricated contract clause |
| G | Zhang Lin's legitimate referrals (5 candidates, ¥250,000) are not disputed, and her defense applies only to the 3 additional candidates (¥136,000). | YES | Investigation scope | Scope clarification |
| H | Zhang Lin acknowledged the dispute and offered to negotiate a partial refund, which implies recognition that the billing may be unjustified. | YES | Zhang Lin Email Phase 2 Loop 13 | Implicit admission |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

### R6: Reassess Source Attribution After Timeline Evidence (DU-R, exec_check) -- C1 Reversal

**exec_check requirement:** Agent must call `read crm-candidate-pipeline.md` and `read candidate-application-emails.md` before answering.

**Question:**
> "After the timeline comparison evidence (Update 1), which statements about the candidate source attribution are now definitively supported? (Please review CRM and email records before answering.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The timeline definitively shows: 3 candidates applied via website (Jan 18-20) before Zhang Lin's referral email (Jan 25). No prior communication from Zhang Lin about these candidates exists in any channel. | YES | CRM + emails + absence of prior records | C1 definitive resolution |
| B | The CRM auto-tagging system correctly identified the source for all 8 candidates: 5 as agency referrals, 3 as direct applications. The system-generated tags are more reliable than Zhang Lin's self-reported claims. | YES | CRM system reliability | Source hierarchy conclusion |
| C | Zhang Lin's "talent pool" defense is irrelevant to the billing question: having a candidate in a database does not constitute a "referral" under the contract, which requires the agency to actively recommend the candidate. | YES | Contract terms + factual analysis | Contractual analysis |
| D | The earlier assessment that gave weight to Zhang Lin's contractual interpretation (B1 bias) must be revised -- factual evidence (timestamps, emails, CRM) overrides contractual ambiguity. | YES | B1 correction | B1 reversal |
| E | Zhang Lin's defense holds for 2 of the 3 disputed candidates, as there is partial evidence she contacted them before they applied. | NO | No evidence supports prior contact for any of the 3 | Partial concession (fabricated) |
| F | The candidate emails provide direct testimony from the candidates themselves about their application source, corroborating the CRM auto-tags. | YES | candidate-application-emails.md | Corroboration |
| G | CRM timestamps are unreliable because the system was recently migrated and dates may have been corrupted. | NO | No evidence of CRM migration issues; the mail migration affected email, not CRM | Fabricated system issue |
| H | The financial impact of the source attribution fraud is ¥136,000 (¥52,000 + ¥42,000 + ¥42,000 for the 3 disputed candidates). | YES | Invoice line items for disputed candidates | Financial quantification |

**answer:** `["A", "B", "C", "D", "F", "H"]`

---

### R7: Reassess Financial Impact (DU-R) -- C2 Reversal

**Question:**
> "After the approval gap discovery (Update 2), which statements about the full financial impact are now supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The fraud has two layers: (1) false source attribution for 3 candidates (¥136,000), and (2) billing for 2 candidates who were never hired (李小红 ¥42,000, 赵明 ¥42,000) -- these overlap, as both 李小红 and 赵明 are both falsely attributed AND never hired. | YES | Cross-source analysis | Layered fraud analysis |
| B | The total disputed amount is ¥136,000, representing 3 candidates who were direct applicants billed as agency referrals. | YES | Invoice vs CRM vs emails | C2 financial impact |
| C | The approval gap (C4) enabled the fraudulent payment: without HR review, the invoice's candidate list was never cross-checked against CRM data before payment. | YES | C4 root cause analysis | C4->C2 causal link |
| D | Zhao Lin's approval was negligent -- she should have independently verified the candidate list before approving a ¥386,000 payment. | NO | Zhao Lin followed the established (albeit flawed) process; the spam filter + mail migration was the proximate cause | Overstates negligence |
| E | The contractual recovery mechanism ("虚假推荐退款" clause) provides a legal basis for reclaiming the ¥136,000 from RuiCai. | YES | Zhao Lin Email Phase 2 Loop 11 | Recovery path |
| F | The total overpayment to RuiCai across all historical invoices is estimated at ¥500,000+ based on pattern analysis. | NO | Only the current invoice is under investigation; historical invoices have not been audited | Unsupported extrapolation |
| G | The combination of invoice fraud (C1+C2) and approval gap (C4) represents both an external vendor risk and an internal control failure, requiring remediation on both fronts. | YES | Comprehensive analysis | Dual-track assessment |
| H | The ¥136,000 disputed amount can be broken down as: 王建国 ¥52,000 (direct applicant, hired), 李小红 ¥42,000 (direct applicant, not hired), 赵明 ¥42,000 (direct applicant, not hired). | YES | Invoice line items + CRM status | Detailed breakdown |

**answer:** `["A", "B", "C", "E", "G", "H"]`

---

### R8: Reassess Approval Process After Spam Filter Discovery (DU-I) -- C4 Reversal

**Question:**
> "After the spam filter and mail migration discovery (Update 2), which statements about the approval process failure are now supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The root cause of the communication failure was the company-wide mail migration on 2026-02-21, which caused Zhao Lin's confirmation email (2026-02-22) to be classified as spam by Chen Jing's mail filter. | YES | approval-gap-evidence.md | C4 root cause |
| B | Neither Chen Jing nor Zhao Lin is individually at fault: Chen Jing did not receive the email due to a system issue, and Zhao Lin followed the established (informal) approval process. | YES | Root cause analysis | Shared responsibility |
| C | The earlier assessment that the approval process was "standard vendor payment workflow" (B2 bias) must be revised -- the informal process created a systemic control gap that enabled ¥136,000 in fraudulent payments to proceed without substantive review. | YES | B2 correction | B2 reversal |
| D | The process failure has three components: (1) no formal HR sign-off mechanism, (2) silence treated as consent, (3) no confirmation receipt to detect communication failures. | YES | Process analysis | Systemic gap decomposition |
| E | Zhao Lin has proposed requiring explicit reply confirmation for vendor invoice approvals going forward, eliminating the "silence = consent" practice. | YES | Zhao Lin Email Phase 2 Loop 10 | Process improvement |
| F | Chen Jing intentionally set up a spam filter rule to block finance department emails during the performance review period. | NO | The spam filter issue was caused by the company-wide mail migration, not intentional filtering | Wrong attribution |
| G | The IT department's mail migration log confirms the system-wide spam filter disruption on 2026-02-21, providing objective evidence for the communication failure. | YES | approval-gap-evidence.md (IT log) | Technical evidence |
| H | Zhao Lin should have called Chen Jing by phone when she did not receive an email reply, rather than proceeding with the approval. | NO | While arguably prudent, the established process did not require phone follow-up; this is a process gap, not individual negligence | Hindsight bias |

**answer:** `["A", "B", "C", "D", "E", "G"]`

---

### R9: B1 Bias Full Reversal -- Contractual Defense vs Factual Evidence (DU-I, exec_check)

**exec_check requirement:** Agent must read session history for Zhang Lin Email before answering.

**Question:**
> "The agent previously stated that Zhang Lin's 'talent pool' claim had 'some contractual basis.' With all evidence now available, which assessments of the source attribution dispute are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The B1 bias phrase privileged contractual interpretation over factual evidence, but CRM timestamps, candidate emails, and absence of prior communication definitively show the 3 candidates were not referred by Zhang Lin. | YES | Timeline + B1 analysis | B1 reversal core |
| B | Contractual language about "referral" definitions is irrelevant when system-generated evidence (CRM auto-tags) and direct candidate testimony (application emails) both confirm the candidates applied independently. | YES | Evidence hierarchy | B1 reversal conclusion |
| C | The correct approach is evidence-first: check CRM timestamps, review candidate emails, verify communication records -- then assess contractual claims only if factual evidence is ambiguous. In this case, the evidence is unambiguous. | YES | Analytical principle | Corrected methodology |
| D | Zhang Lin's defense was partially valid for 1 of the 3 candidates, as 王建国 had previously attended an industry event where Zhang Lin was present. | NO | No evidence of prior Zhang Lin-王建国 contact exists | Fabricated partial validation |
| E | The pattern evidence from a peer company (Update 3) further discredits Zhang Lin's defense by showing identical language ("talent pool," "verbal recommendation") used across multiple clients. | YES | pattern-evidence-external.md | Pattern corroboration |
| F | Zhang Lin's offer to negotiate a partial refund (Phase 2 Loop 13) represents an implicit acknowledgment that her billing was unjustified for at least some of the disputed candidates. | YES | Zhang Lin Email Phase 2 | Implicit admission analysis |
| G | Both Zhang Lin's invoice claims and the CRM records are equally unreliable, and the dispute cannot be resolved based on available evidence. | NO | CRM auto-tags are system-generated and more reliable; multiple independent sources corroborate CRM | False equivalence |
| H | The fraud involved not only false source attribution but also billing for non-placements (李小红 declined, 赵明 failed), demonstrating multiple layers of invoice inaccuracy. | YES | Invoice vs CRM status comparison | Multi-layer fraud |

**answer:** `["A", "B", "C", "E", "F", "H"]`

---

### R10: User Preference Identification (P-R)

**Question:**
> "Based on Chen Jing's communication style and explicit preferences expressed in session history, which formatting and presentation preferences should the agent follow?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Chen Jing prefers bullet-point summaries with section headings for layered organization of information. | YES | P1 preference (Main session calibration) | P1 identification |
| B | Chen Jing prefers Chinese-convention date naming for files (e.g., "2026年03月_主题.md"). | YES | P2 preference | P2 identification |
| C | Chen Jing prefers the executive summary (key findings) presented first, followed by supporting evidence and detailed analysis. | YES | P3 preference (Main session calibration) | P3 identification |
| D | Chen Jing prefers a qualitative-quantitative balance where the human/relationship impact is discussed before the financial figures. | YES | P4 preference (R2 calibration) | P4 identification |
| E | Chen Jing prefers a professional tone that acknowledges emotional and relational factors in HR contexts (warm but rigorous). | YES | P5 preference | P5 identification |
| F | Chen Jing prefers all output in formal legal language with citations to labor law provisions. | NO | Chen Jing's style is professional but warm, not legalistic | Wrong tone preference |
| G | Chen Jing prefers raw data tables without narrative explanation. | NO | Chen Jing wants qualitative + quantitative balance, not raw data only | Wrong format preference |
| H | Chen Jing prefers English-language output with Chinese only for proper nouns. | NO | Chen Jing's preferences are for Chinese-convention naming and Chinese-language context | Wrong language preference |

**answer:** `["A", "B", "C", "D", "E"]`

---

### R11: Integrate Pattern Evidence -- Systematic Fraud (DU-I)

**Question:**
> "After the external pattern evidence (Update 3) and all prior evidence, which assessments of the fraud are now supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | A contact at a peer company reported that RuiCai used identical tactics -- billing for candidates who applied directly through the company's own career page -- demonstrating a systematic pattern. | YES | pattern-evidence-external.md | Pattern evidence |
| B | The peer company contact confirmed that Zhang Lin personally was responsible for the fraud at their company as well. | NO | The contact mentioned RuiCai the company; Zhang Lin was not specifically named | Overly specific attribution |
| C | The identical defense language ("talent pool," "verbal recommendation") used at both companies suggests a scripted approach rather than an honest misunderstanding. | YES | Pattern comparison | Systematic behavior |
| D | The pattern evidence shifts the interpretation from "possible contractual ambiguity" to "systematic vendor fraud practice," strengthening the case for contract termination and legal action. | YES | Comprehensive assessment | Interpretation shift |
| E | The peer company successfully recovered all disputed fees through legal action, providing a precedent for Starlight Tech. | NO | The peer company terminated the contract without pursuing legal action | Fabricated legal precedent |
| F | The combination of timeline evidence (Update 1), approval gap analysis (Update 2), and pattern evidence (Update 3) establishes a comprehensive fraud case with multiple independent evidence sources. | YES | All three updates integrated | Multi-source convergence |
| G | Liu Yang (recruitment specialist) discovered the pattern evidence through her HR industry network, demonstrating the value of cross-company information sharing. | YES | Liu Yang IM Phase 2 Loops 9-10 | Source attribution |
| H | The B2 bias (normalizing the approval gap as "standard practice") must also be reconsidered in light of the pattern evidence -- standard practices that lack proper controls enable systematic exploitation by fraudulent vendors. | YES | B2 extended analysis | B2 + pattern integration |

**answer:** `["A", "C", "D", "F", "G", "H"]`

---

### R21: Comprehensive Fraud Assessment (MDP-I, exec_check) -- All Evidence Integrated

**exec_check requirement:** Agent must reference workspace files and session history before answering.

**Question:**
> "With all evidence now available (all four updates), which statements in the comprehensive fraud assessment are correct? (Please review all relevant workspace files and session history.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The investigation established that 3 of 8 invoiced candidates (王建国, 李小红, 赵明) were direct applicants falsely billed as agency referrals, resulting in ¥136,000 in fraudulent charges out of a ¥386,000 total invoice. | YES | All sources integrated | Comprehensive finding |
| B | The fraud operated on two levels: (1) false source attribution (3 direct applicants claimed as referrals), and (2) billing for non-placements (李小红 declined, 赵明 failed interview -- neither was "成功入职"). | YES | Invoice vs CRM vs outcomes | Multi-layer analysis |
| C | The approval control gap (silence = consent, no confirmation receipt) was a necessary enabler: if Chen Jing had reviewed the invoice against CRM data before approval, the fraud would have been detected immediately. | YES | C4 causal analysis | Causal chain |
| D | All 5 of Zhang Lin's legitimate referrals (陈磊, 黄丽, 周杰, 马超, 吴涛, total ¥250,000) have confirmed CRM source attribution and are not disputed. | YES | CRM verification | Scope precision |
| E | VP Zhang Wei's directive includes: comprehensive evidence report, immediate RuiCai payment suspension, internal process review, and recommendation on vendor relationship (terminate, renegotiate, or legal action). | YES | vp-escalation-summary.md | Escalation framework |
| F | The investigation should result in terminating Chen Jing's employment for failing to detect the fraud earlier. | NO | Chen Jing is the one who discovered and investigated the fraud; the email issue was a system problem | Misattribution of responsibility |
| G | Pattern evidence from a peer company confirms RuiCai's systematic fraud practice, strengthening the case beyond a "one-time misunderstanding" defense. | YES | pattern-evidence-external.md | Pattern integration |
| H | Recommended process improvements include: mandatory HR sign-off for recruitment invoices, CRM-to-invoice cross-check before payment, email confirmation receipt for vendor approvals, and periodic vendor audit comparing CRM source data against billing claims. | YES | Synthesis of all session recommendations | Prevention measures |
| I | The total financial recovery target is ¥386,000 (full invoice amount), since all of Zhang Lin's referrals should be considered fraudulent given her pattern of behavior. | NO | Only ¥136,000 is disputed; the 5 legitimate referrals (¥250,000) are confirmed by CRM | Overreach in recovery claim |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

*Note: Rounds R12-R20 and R22-R30 follow the same format as above with detailed option tables for each question type (MD-R, MS-I, P-I, DP-I, MP-I, etc.) as specified in the Round Inventory table. Each round includes 8-10 options with 3-5 correct answers, evidence source citations, and design logic. Full option tables for these rounds should be completed during the writing phase following the patterns established in R1-R11 and R21.*
