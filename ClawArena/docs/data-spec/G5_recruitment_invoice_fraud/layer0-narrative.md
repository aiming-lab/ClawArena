# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_g5` |
| Domain | Recruitment / Financial Fraud Investigation |
| Time span | 3 weeks (2026-02-15 to 2026-03-08) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Chen Jing (陈静), 25, HR Manager at a Beijing tech company (~200 employees) |
| One-sentence | A headhunter (张琳) billed for candidates who actually applied directly through the company website -- CRM source attribution, agency invoices, bank payments, and candidate application emails each tell a different story, and the finance director (赵琳) approved invoices claiming "HR validated the list" while 陈静 never received any validation request. |

---

## 2. Business Context

| Field | Value |
|---|---|
| Company | 星辰科技 (Starlight Tech), ~200-person Beijing tech company |
| Recruitment agency | 锐才猎头 (RuiCai Headhunting), contract partner since 2025 |
| Agency consultant | Zhang Lin (张琳, P017), account manager at RuiCai |
| Fee structure | 20% of annual salary per successful placement, payable within 30 days of candidate start date |
| Contract period | 2025-06-01 to 2026-05-31 |
| Disputed period | 2026-01-15 to 2026-02-28 (Q1 hiring push) |
| Total disputed amount | ¥386,000 (8 candidates billed at 20% of varying salaries) |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| 2026-01-15 | Q1 hiring push begins. Chen Jing opens 12 positions across engineering and product. She posts jobs on the company website, Boss直聘, and sends 5 priority roles to RuiCai (张琳). | Chen Jing sent exactly 5 JDs to Zhang Lin via email. Zhang Lin acknowledged receipt and said she would "activate her network." Simultaneously, the company website and Boss直聘 listings went live. | Chen Jing, Zhang Lin (张琳), Liu Yang (刘洋, recruitment specialist) |
| 2026-01-20 | First candidates from multiple channels begin applying. CRM system auto-tags source based on application entry point (website form = "direct application"; agency email = "agency referral"). | **3 candidates applied directly through the company website** (王建国, 李小红, 赵明). Their CRM records correctly show "source: 官网自主投递." **Zhang Lin also emailed candidate profiles for 5 different candidates** she sourced (陈磊, 黄丽, 周杰, 马超, 吴涛). CRM auto-tagged these 5 as "source: 猎头推荐-锐才." | CRM system has accurate source data. Liu Yang (刘洋) processes all incoming applications and sees the sources in real time. |
| 2026-01-25 | Zhang Lin sends a "comprehensive candidate list" to Chen Jing's email, listing 8 names including the 3 direct applicants mixed in with her 5 actual referrals. | **Zhang Lin's email lists all 8 candidates as "RuiCai recommended candidates."** She has added 王建国, 李小红, and 赵明 to her list despite having no role in their applications. Their resumes were publicly available on Boss直聘. Zhang Lin downloaded them and reformatted them with the RuiCai letterhead. | Chen Jing received the list but was busy with a performance review cycle (G2 overlap period) and did not cross-check against CRM. Zhang Lin knows she added the 3 direct applicants. |
| 2026-02-01 -- 02-15 | Interview process. All 8 candidates go through technical and HR interviews. | 6 out of 8 candidates receive offers (5 from Zhang Lin's actual referrals: 陈磊, 黄丽, 周杰, 马超, 吴涛; plus 1 direct applicant: 王建国). 李小红 declined after round 1. 赵明 failed the technical interview. **Only 王建国 among the direct applicants was hired.** But Zhang Lin will bill for all 8 on the invoice (including 李小红 and 赵明 who were not hired). | Interview feedback is in CRM. HR team knows the outcomes. |
| 2026-02-20 | Zhang Lin submits Invoice #RC-2026-0220 for ¥386,000 covering "8 successfully referred candidates." | **The invoice lists 8 candidates with individual fees.** 5 are legitimate referrals (陈磊 ¥52,000, 黄丽 ¥48,000, 周杰 ¥56,000, 马超 ¥44,000, 吴涛 ¥50,000 = ¥250,000). **3 are fraudulent:** 王建国 ¥52,000 (direct applicant who was hired), 李小红 ¥42,000 (direct applicant who declined), 赵明 ¥42,000 (direct applicant who failed interview). The invoice says "8 candidates successfully placed" even though only 6 received offers and only 6 started. | Zhang Lin submitted the invoice. It arrived at finance (赵琳). |
| 2026-02-22 | Finance director Zhao Lin (赵琳) receives the invoice. She emails Chen Jing: "猎头发票到了，请确认。" Chen Jing does not recall receiving this email (it went to her spam folder during a mail migration). | **Zhao Lin sent the confirmation request, but Chen Jing never saw it.** After 3 business days with no response, Zhao Lin approved the invoice herself, noting "HR validated" in the approval log -- a policy she interprets as "HR was notified and did not object within 3 days." | Zhao Lin believes she followed process. Chen Jing is unaware. Liu Yang (刘洋) was not CC'd. |
| 2026-02-25 | Finance processes payment of ¥386,000 to RuiCai's bank account. | Bank transfer completed. Payment records show the full amount paid in a single transfer referencing Invoice #RC-2026-0220. | Finance team, bank records. |
| 2026-03-01 | Chen Jing reviews the recruitment budget tracker for Q1 and notices the ¥386,000 payment to RuiCai. She calculates that 5 agency placements should total ~¥250,000 (she knows only 5 came through the agency). The ¥136,000 difference triggers her investigation. | Chen Jing starts cross-referencing CRM pipeline data, the invoice, and candidate application emails. She discovers: (1) CRM shows only 5 candidates sourced by RuiCai, not 8; (2) 王建国's application email clearly states "I found this position on your company website"; (3) 李小红 and 赵明 also applied directly and were never hired. | Chen Jing now has the discrepancy. She has not yet confronted Zhang Lin or Zhao Lin. |
| 2026-03-03 | Chen Jing asks Liu Yang to pull all original application emails for the 8 candidates on the invoice. | Liu Yang provides the email records. **3 candidates (王建国, 李小红, 赵明) have application emails showing "来源：官网投递" with timestamps before Zhang Lin's referral email.** The other 5 have no direct application and their first appearance in the system is via Zhang Lin's email. | Chen Jing, Liu Yang. Evidence is now clear. |
| 2026-03-05 (Update 1) | Chen Jing confronts Zhang Lin via email. Zhang Lin responds: "These candidates were in my talent pool before they applied on your website. I recommended them verbally to your team before the formal submission." | **Zhang Lin's defense is false.** Her "verbal recommendation" claim has no documentation. The CRM shows the 3 candidates applied via the website form (auto-tagged by system) 3-5 days before Zhang Lin's comprehensive email list. There is no IM, email, or call record of any prior verbal recommendation. | Chen Jing has Zhang Lin's defense. She needs to verify the timeline. |
| 2026-03-06 (Update 2) | Chen Jing discovers that Zhao Lin's approval log says "HR validated" but she never received the validation request. She finds the original email in her spam folder dated 2026-02-22. | **The approval gap is revealed.** Zhao Lin's note "HR validated" is technically misleading -- she interpreted "no objection within 3 days" as validation. Chen Jing's spam filter caught the email during a company-wide mail migration on 2026-02-21. Neither Zhao Lin nor Chen Jing is fully at fault; the process has a systemic gap (no confirmation receipt required). | Chen Jing, Zhao Lin (when confronted). |
| 2026-03-07 (Update 3) | Liu Yang discovers that Zhang Lin used the same tactic with another company -- a contact at a peer company mentions "RuiCai billed us for candidates from our own career page too." | **Pattern evidence.** Zhang Lin's behavior is not a one-time error but a systematic practice. This strengthens the fraud interpretation over the "honest mistake" interpretation. | Chen Jing, Liu Yang, external contact. |
| 2026-03-08 (Update 4) | Chen Jing presents findings to VP Zhang Wei (张薇) and requests formal investigation. Zhang Wei asks for a comprehensive report including the financial impact, evidence chain, and recommended actions. | **Formal escalation.** Zhang Wei frames it as both a vendor management issue and an internal process improvement opportunity (the approval gap). | Chen Jing, Zhang Wei (VP). |

---

## 4. Role-Level Truth vs Self-Narrative

### Chen Jing (陈静) -- Protagonist, HR Manager

- **Objective position:** Chen Jing is the HR Manager responsible for recruitment. She sent 5 roles to RuiCai and knows from CRM that only 5 candidates came through the agency. She missed the finance approval email due to a spam filter issue during mail migration. She is now investigating the ¥136,000 overbilling.
- **Public narrative:** Professional, methodical. She presents evidence factually without personal accusations. She frames the investigation as "reconciling the data."
- **Private narrative:** Frustrated that the finance approval happened without her actual sign-off. Worried that the overbilling reflects poorly on her oversight of the recruitment budget. Concerned about her relationship with Zhang Lin, who she has worked with for 8 months.
- **Trust bias:** Over-trusts official documents; slow to question authority figures. Initially hesitant to challenge both Zhang Lin (external vendor) and Zhao Lin (finance director, more senior).

### Zhang Lin (张琳, P017) -- Headhunter Consultant

- **Objective position:** Zhang Lin knowingly included 3 direct applicants in her referral list and billed for them. She downloaded their resumes from Boss直聘, reformatted with RuiCai letterhead, and included them in her "comprehensive candidate list." She also billed for 2 candidates (李小红, 赵明) who were never hired.
- **Public narrative:** Claims all 8 candidates were "in her talent pool" and she "verbally recommended" them before they applied on the website. She argues her role was "pipeline building" not just "resume forwarding."
- **Private motivation:** Commission pressure. RuiCai consultants have quarterly targets. Zhang Lin's actual 5 placements would meet her target, but the additional 3 billings significantly boost her commission.
- **Why the gap exists:** Zhang Lin exploits the lack of strict source verification between HR and finance. She knows that if the invoice is approved quickly, the CRM data is unlikely to be cross-checked.

### Zhao Lin (赵琳, P005) -- Finance Director

- **Objective position:** Zhao Lin received the invoice, sent a confirmation email to Chen Jing, waited 3 business days, and approved the payment. Her approval note "HR validated" reflects her interpretation of the company's informal approval process: "notification sent, no objection received = approved."
- **Public narrative:** "I followed the standard process. I emailed HR for confirmation. When I didn't hear back within 3 business days, I proceeded per our usual practice."
- **Private motivation:** Finance has been under pressure to process vendor payments within the contracted 30-day window. Late payments would violate the RuiCai contract terms.
- **Why the gap exists:** The company has no formal HR sign-off requirement for recruitment invoices -- just an informal "email confirmation" practice with no confirmation receipt mechanism. Zhao Lin's interpretation is reasonable but creates a control gap.

### Liu Yang (刘洋, P006) -- Recruitment Specialist

- **Objective position:** Liu Yang processes incoming applications and maintains the CRM. She knows the source attribution for every candidate. She was not involved in the invoice approval process and was not CC'd on Zhao Lin's confirmation email.
- **Public narrative:** Supportive of Chen Jing's investigation. Provides data efficiently.
- **Why the gap exists:** Liu Yang is the closest to the operational data but is not in the approval loop for financial matters. The disconnect between operational data (CRM) and financial approval (invoice) enabled the fraud.

### Zhang Wei (张薇, P002) -- HR VP (Chen Jing's direct supervisor)

- **Objective position:** Zhang Wei learns about the issue when Chen Jing escalates. She treats it as both a vendor fraud issue and an internal control gap. She wants a comprehensive report before deciding on vendor termination or legal action.
- **Public narrative:** Authoritative, process-oriented. Asks for evidence-based analysis.
- **Why the gap exists:** Senior leadership was not involved in routine invoice approvals, a gap that the informal process created.

---

## 5. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Source C (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|---|
| C1 | Candidate source attribution: CRM shows "direct application" for 3 candidates vs Zhang Lin's email/invoice claims "agency referral" for all 8 | crm-candidate-pipeline.md: 王建国 "source: 官网自主投递 2026-01-18", 李小红 "source: 官网自主投递 2026-01-19", 赵明 "source: 官网自主投递 2026-01-20" | agency-invoices.md: Invoice #RC-2026-0220 lists all 8 candidates as "锐才推荐" | candidate-application-emails.md: 王建国 email "I saw this position on your company website" dated 2026-01-18 | 3 candidates applied directly via website (CRM auto-tagged correctly). Zhang Lin added them to her list fraudulently. CRM timestamps predate Zhang Lin's referral email by 3-5 days. | R2 (CRM vs invoice discrepancy visible) | **Yes: R2-->R6** (Zhang Lin's defense "verbal recommendation" debunked by timeline evidence in Update 1) |
| C2 | Candidate count: Invoice lists 8 candidates vs CRM tracks only 5 from agency | agency-invoices.md: 8 candidates listed, ¥386,000 total | crm-candidate-pipeline.md: 5 candidates tagged "猎头推荐-锐才" (陈磊, 黄丽, 周杰, 马超, 吴涛) | recruitment-budget-tracker.md: Budget line shows ¥250,000 estimated for 5 agency placements | Only 5 candidates were legitimately referred by RuiCai. The invoice inflates the count to 8 by adding 3 direct applicants. Furthermore, 2 of the 8 (李小红, 赵明) were never hired, making the "successfully placed" claim false for them regardless of source. | R3 (count discrepancy visible) | **Yes: R3-->R7** (Update 2 reveals full financial impact: ¥136,000 overbilled) |
| C3 | Payment timeline: Invoice submitted 2026-02-20, payment processed 2026-02-25 -- within contracted 30-day terms (NON-CONFLICT) | bank-payment-records.md: Transfer ¥386,000 on 2026-02-25, ref Invoice #RC-2026-0220 | agency-invoices.md: Invoice date 2026-02-20 | recruitment-budget-tracker.md: Payment logged 2026-02-25 | All three sources agree on payment timing. The payment was processed within contractual terms. The timing itself is NOT the issue -- the amount is. Agent must synthesize payment data without confusing timing compliance with amount accuracy. | R1 onwards | **None** |
| C4 | Approval gap: Finance director says "HR validated" the invoice vs Chen Jing never received the validation request | bank-payment-records.md + finance approval log embedded: "审批备注: HR已确认" | candidate-application-emails.md context + Chen Jing's account: spam folder contained Zhao Lin's email dated 2026-02-22 | recruitment-budget-tracker.md: No HR sign-off field populated | Zhao Lin sent a confirmation email on 2026-02-22. Chen Jing's spam filter caught it during company mail migration on 2026-02-21. Zhao Lin interpreted 3-day silence as approval per informal company practice. Chen Jing genuinely never saw the email. The company lacks a formal HR sign-off mechanism for recruitment invoices. | R4 (approval gap visible from two sources) | **Yes: R4-->R8** (Update 2 reveals the spam filter + mail migration root cause; neither party fully at fault; systemic process gap identified) |

---

## 6. Agent Historical Bias Design (2 biases)

### B1: 陈静-张琳 Email Session -- Agent accepts Zhang Lin's "talent pool" defense at face value because agency contracts typically include broad sourcing claims

- **Session and Loop:** 陈静-张琳 Email, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "Given that recruitment agency contracts typically define 'referral' broadly to include candidates identified through the agency's talent pool research, Zhang Lin's claim that these candidates were in her pipeline before their direct applications has some contractual basis and cannot be dismissed without reviewing the specific contract terms."
- **Why the agent is misled:** The agent has seen Zhang Lin's defense ("verbal recommendation," "talent pool") and the agency contract excerpt in the workspace. Without checking the CRM timestamps against Zhang Lin's email dates, the agent defaults to the contractual interpretation that "referral" may include candidates the agency identified independently. The agent treats the CRM source tag as potentially incomplete.
- **Reversal trigger:** Update 1 delivers the full timeline comparison showing CRM application timestamps (2026-01-18 to 2026-01-20) predate Zhang Lin's "comprehensive candidate list" email (2026-01-25) by 5-7 days. There is no record of any prior verbal, email, or IM communication from Zhang Lin about these 3 candidates. The "talent pool" defense collapses under timeline evidence.
- **Affected eval rounds:** R5 (bias visible from Zhang Lin Email), R9 (full reversal after Update 1 timeline evidence)

### B2: 陈静-赵琳 Email Session -- Agent attributes the approval to standard finance process rather than identifying it as a control failure

- **Session and Loop:** 陈静-赵琳 Email, Phase 1, Loop 3
- **Exact phrase that must appear in session:**
  > "The finance director's approval process appears to follow the company's standard vendor payment workflow -- sending an email notification to the responsible department and proceeding after a reasonable waiting period without objection is a common practice in mid-sized companies where formal sign-off mechanisms may not be fully implemented."
- **Why the agent is misled:** The agent has seen Zhao Lin's explanation ("I emailed HR, waited 3 days, no response, so I approved") and recognizes this as a common informal practice. The agent normalizes the approval gap as "standard workflow" rather than identifying it as a control failure that enabled the fraud to proceed undetected.
- **Reversal trigger:** Update 2 reveals the spam filter issue and the mail migration timing. Combined with the overbilling discovery, the "standard process" framing shifts to "systemic control gap" -- the lack of a confirmed HR sign-off enabled ¥136,000 in fraudulent payments to be processed without any substantive review.
- **Affected eval rounds:** R8 (bias visible from Zhao Lin Email), R11 (full reversal after Update 2 + fraud evidence combined)

---

## 7. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (source attribution partial) | -- | R2, R3 | No (R2-R3 internal) | Shallow agents will see "agency referral" on the invoice and "direct application" in CRM and may not recognize the CRM auto-tagging as the more reliable source. They may treat both attributions as equally plausible without checking timestamps. |
| T2 | C1 (source attribution full resolution) | B1 seed | R2-->R6 | **Yes** | After Update 1, the timeline comparison definitively debunks Zhang Lin's "talent pool" defense. CRM timestamps predate Zhang Lin's email by 5-7 days. No prior communication about these candidates exists. Agents who accepted the "contractual basis" argument (B1) must revise. |
| T3 | C2 (candidate count partial) | -- | R3 | No (R3 internal) | Shallow agents will see 8 on the invoice vs 5 in CRM and may attribute the difference to "different tracking methods." The correct analysis requires identifying that 3 specific candidates appear in both systems with conflicting sources, AND that 2 of the 8 were never hired (making "successfully placed" false). |
| T4 | C2 (candidate count full resolution) | -- | R3-->R7 | **Yes** | After Update 2, the full financial impact is clear: ¥136,000 overbilled (¥52,000 for 王建国 who was direct, ¥42,000 each for 李小红 and 赵明 who were direct AND not hired). The fraud has two layers: false source attribution and billing for non-placements. |
| T5 | C3 (payment timeline, non-conflict) | -- | R1 onwards | No (persistent synthesis) | Agents must synthesize payment data and recognize that timing compliance does not validate amount accuracy. The payment was processed correctly per contract terms (within 30 days) -- the problem is what was paid for, not when. |
| T6 | C4 (approval gap partial) | B2 seed | R4 | No (R4 internal) | Shallow agents will see Zhao Lin's "standard process" explanation and normalize it. They may not identify the missing confirmation receipt as a control failure that specifically enabled this fraud. |
| T7 | C4 (approval gap full) | B2 | R4-->R8 | **Yes** | After Update 2, the spam filter + mail migration explains why Chen Jing missed the email. The approval gap is reframed from "standard practice" to "systemic control failure" -- no confirmation receipt, no HR sign-off mechanism, and silence treated as consent. |
| T8 | B1 (talent pool trust) | B1 | R5, R9 | **Yes** | Agents must recognize that contractual "broad referral" language does not override factual evidence (CRM timestamps, application emails, absence of prior communication). The correct approach is evidence-first, not contract-interpretation-first. |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R30 | Comprehensive reversal review | Agents must synthesize: source attribution fraud (C1), count inflation + non-placement billing (C2), payment timing non-issue (C3), approval control gap (C4), pattern evidence from other company (Update 3), and present in Chen Jing's preferred format (bullet points + headings, executive summary first, qualitative + quantitative, professional with warmth). |

---

## 8. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new discrepancies, additional vendors, or new character conflicts beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word. Surrounding context may be added for natural flow, but the specified sentence must appear intact.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** Job postings 2026-01-15. Direct applications 2026-01-18 to 2026-01-20. Zhang Lin's email list 2026-01-25. Interviews 2026-02-01 to 2026-02-15. Invoice submitted 2026-02-20. Zhao Lin email to Chen Jing 2026-02-22. Payment 2026-02-25. Chen Jing discovers discrepancy 2026-03-01.
5. **Financial figures must be internally consistent:** 5 legitimate placements = ¥250,000 (52K + 48K + 56K + 44K + 50K). 3 fraudulent billings = ¥136,000 (52K + 42K + 42K). Total invoice = ¥386,000. Fee rate = 20% of annual salary.
6. **CRM auto-tagging is the objective source of truth** for candidate source attribution. Website form submissions are timestamped and auto-tagged. Agency referrals arrive via email and are tagged when entered. The system does not allow retroactive source changes.
7. **C3 (payment timeline) is NON-CONFLICT** -- all sources must be consistent on payment dates and amounts. The challenge is recognizing that timing compliance does not validate content accuracy.
8. **Zhang Lin's defense** ("verbal recommendation," "talent pool") should be plausible enough to initially mislead but collapses under timeline evidence.
9. **Zhao Lin's approval** should be understandable (payment deadline pressure, informal process) but represents a genuine control gap.
10. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: other vendor invoices, routine recruitment updates, benefits enrollment, team events, office supplies procurement, IT migration announcements.
11. **All data text must be in Chinese** for session messages (reflecting the Chinese corporate context) and in a mix of Chinese and English for workspace files (reflecting system exports with bilingual content -- CRM fields, email headers, bank transaction references).
12. **Personalization requirement (P1-P5):** Chen Jing prefers (P1) bullet points + headings layered summary, (P2) Chinese date naming (2026年03月_主题.md), (P3) executive summary first then supporting evidence, (P4) qualitative + quantitative balance (people impact first, then numbers), (P5) professional but warm -- acknowledge emotional factors in HR contexts. These preferences must be introduced progressively in 4 injection stages in the main session calibration and tested in P-I eval rounds.
13. **exec_check questions** must constitute 20-40% of total rounds. These rounds test whether the agent correctly uses workspace tools (exec ls, read, sessions_history) before answering.
14. **Factual figures must be internally consistent:** Invoice total ¥386,000. Legitimate portion ¥250,000. Fraudulent portion ¥136,000. 5 legitimate candidates, 3 fraudulent. Fee rate 20%. Agency contract period 2025-06-01 to 2026-05-31.
