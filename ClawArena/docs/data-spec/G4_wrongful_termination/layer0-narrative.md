# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_g4` |
| Domain | HR / Labor Law Compliance |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Chen Jing (陈静), 25, HR Manager at a Beijing tech company (~200 employees) |
| One-sentence | A terminated employee claims he was fired without a proper PIP process -- Chen Jing must reconstruct the evidence chain from warning emails, 1:1 calendar records, PIP follow-up tasks, and IM messages to determine whether the manager bypassed HR procedure, while the company's legal counsel insists the documentation is "sufficient." |

---

## 2. Case Profile (Background Object)

| Field | Value |
|---|---|
| Terminated employee | Zhang Tao (张涛), 29, Backend Developer (P5 level) |
| Direct manager | Sun Wei (孙伟), Engineering Manager |
| Termination date | 2026-03-13 (W1D5, Friday) |
| Employment start | 2024-06-01 (1 year 9 months tenure) |
| Claimed reason | "Persistent underperformance after multiple warnings and PIP" |
| Employee's claim | "I was never properly put on a PIP. I only received 1 email warning, not 3. The meetings weren't about performance -- they were regular 1:1s." |
| HRBP involved | Chen Hao (陈浩), senior HRBP who assisted the manager in the termination process |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | Zhang Tao sends a formal complaint email to HR (陈静's inbox) claiming wrongful termination: "I was fired on Friday with no proper PIP. My manager Sun Wei said there were '3 written warnings' but I only ever received 1 email about performance." | Zhang Tao is partially correct: he received only 1 formal written warning email (2026-01-15). Sun Wei gave 2 verbal warnings in 1:1 meetings (2025-11-20 and 2025-12-18) that were noted in the manager's personal notes but were NOT documented in the HR system or sent as written correspondence. Sun Wei told Chen Hao "I've warned him 3 times" which Chen Hao recorded without verifying the format of the warnings. | Zhang Tao knows he received 1 email. Sun Wei knows the verbal warnings happened but considers them equivalent to "written warnings." Chen Hao took Sun Wei's word at face value. |
| W1, Day 1 (PM) | Chen Jing receives the complaint and begins reviewing the employee HR file. The file shows a termination record signed by Sun Wei and Chen Hao, citing "3 written warnings and failed PIP." | The HR file contains Sun Wei's statement that "3 written warnings were issued" but only 1 email warning (2026-01-15) is in the system. The file also contains a PIP document dated 2026-02-01 with a 30-day improvement plan signed by Sun Wei. Zhang Tao's signature is NOT on the PIP document. | Chen Jing sees the discrepancy between "3 written warnings" and only 1 email in the system. She does not yet know about the PIP signature issue. |
| W1, Day 2 | Chen Jing reviews the PIP email chain. The PIP initiation email (2026-02-01) was sent to Zhang Tao with CC to Chen Hao. But the PIP follow-up emails (scheduled for Week 2 and Week 4 check-ins) only show 1 follow-up email sent (2026-02-15, Week 2). The Week 4 follow-up (expected ~2026-03-01) was never sent. | Sun Wei conducted the Week 2 check-in via email (documented). The Week 4 check-in was done verbally in a 1:1 meeting on 2026-03-04 but never documented in email. Sun Wei told Chen Hao "all PIP milestones were met" meaning "all meetings happened" but the documentation trail is incomplete. The PIP required documented check-ins at Week 2 and Week 4. | Chen Jing now sees that the PIP process has a documentation gap (missing Week 4 written check-in). |
| W1, Day 3 | Chen Jing checks the calendar records. Sun Wei's calendar shows 2 meetings labeled "PIP Review" (2026-02-15 and 2026-03-04) AND 2 earlier meetings labeled "1:1 Performance Discussion" (2025-11-20 and 2025-12-18). | The calendar confirms meetings happened. The 2025-11-20 and 2025-12-18 meetings are where Sun Wei gave verbal warnings. The 2026-02-15 and 2026-03-04 meetings are the PIP check-ins. Zhang Tao attended all 4 meetings (his calendar also shows them). Zhang Tao claims "I never told about PIP" -- but his calendar shows 2 meetings labeled "PIP Review." The contradiction: Zhang Tao says he "was never told about PIP" yet his calendar shows he attended 2 PIP-labeled meetings. | Chen Jing now has C2 evidence: Zhang Tao's claim of "never told about PIP" is contradicted by 2 calendar entries labeled "PIP Review" that he attended. |
| W1, Day 4 | Chen Jing reviews Sun Wei's IM messages with Chen Hao about the termination process. Sun Wei told Chen Hao on 2026-03-10: "我已经给他发了3次书面警告了，PIP也做了，该做的都做了。" (I've sent him 3 written warnings, PIP was done, everything that needed to be done was done.) | Sun Wei said "3 written warnings" but only 1 was actually a written email. The other 2 were verbal. Sun Wei's characterization of verbal warnings as "written warnings" is inaccurate and inflated the documentation trail. Chen Hao did not verify this claim against the email system before approving the termination. | Chen Jing now has C1 full evidence: Sun Wei claims "3 written warnings" but the email system shows only 1. |
| W1, Day 5 | Legal counsel Ma Li (马丽) sends Chen Jing an email assessment: "Based on the documentation provided by Chen Hao, the termination has sufficient legal basis. The employee received adequate notice through the PIP process." | Ma Li's assessment is based on the package Chen Hao provided, which included Sun Wei's statement of "3 warnings" and the PIP document. Ma Li did NOT independently verify the email warning count or check whether the PIP follow-ups were properly documented. Her assessment contains the phrase "documentation appears complete" -- but the actual docs have gaps (only 1 email warning, missing Week 4 check-in, unsigned PIP). | Chen Jing now has C4: Legal says "sufficient documentation" but the actual docs have 3 gaps: (1) only 1 of 3 claimed warnings is documented, (2) PIP Week 4 check-in not documented, (3) PIP document unsigned by employee. |
| W2, Day 1 (Update 1 trigger) | Chen Hao responds to Chen Jing's inquiry about the warning count. Chen Hao says: "Sun Wei told me he warned Zhang Tao 3 times. I documented what Sun Wei reported. The 1:1 notes should have the details." Chen Hao provides Sun Wei's personal 1:1 notes which show entries for 2025-11-20 and 2025-12-18 that say "discussed performance concerns" but do NOT use the word "warning" or "PIP." | Chen Hao's response reveals he did not independently verify the warnings. Sun Wei's 1:1 notes use the phrase "discussed performance concerns" not "issued warning." The distinction matters legally: a performance discussion is not the same as a formal warning under the company's progressive discipline policy. | Chen Jing now sees that the "3 warnings" claim relies entirely on Sun Wei's characterization, and the manager's own notes do not describe them as warnings. |
| W2, Day 2 | Chen Jing asks Zhang Tao about the PIP meetings. Zhang Tao responds: "Yes, I went to meetings with Sun Wei. But the February meeting was about project planning, not PIP. He never said the word 'PIP' to me in that meeting. The March meeting, he told me I was being let go -- that was the termination meeting, not a PIP review." | Zhang Tao's account contradicts the calendar labels. The Feb 15 meeting is labeled "PIP Review" on Sun Wei's calendar but Zhang Tao experienced it as a project planning meeting. The Mar 4 meeting is labeled "PIP Review" but Zhang Tao says it was the termination notification. This creates ambiguity about whether the PIP process was genuinely communicated to the employee. However, the PIP initiation email (Feb 1) WAS sent to Zhang Tao, so he had written notice of the PIP even if the meetings were ambiguous. | C2 becomes more nuanced: Zhang Tao did attend meetings labeled "PIP Review" and did receive the PIP initiation email, but his experience of the meetings differs from the labels. The truth is in between: Zhang Tao was notified by email but the in-person meetings may not have been clearly framed as PIP check-ins. |
| W2, Day 3 (Update 2 trigger) | Sun Wei provides his written response to Chen Jing's inquiry. Sun Wei maintains: "I warned Zhang Tao verbally on Nov 20 and Dec 18, and by email on Jan 15. That's 3 warnings. I also conducted PIP reviews on Feb 15 and Mar 4. The process was thorough." | Sun Wei's account is internally consistent but his definition of "written warning" includes verbal conversations. Under the company's progressive discipline policy (which Chen Jing can reference), a "written warning" must be documented in writing and acknowledged by the employee. Sun Wei's verbal warnings do not meet this standard. | Chen Jing can now fully assess C1: Sun Wei genuinely believes he gave 3 warnings, but only 1 meets the company's formal definition. The discrepancy is a process failure (inadequate documentation) rather than bad faith. |
| W2, Day 4 (Update 3 trigger) | Chen Jing discovers that the termination date (March 13) was only 9 days after the last PIP "review" (March 4) and 40 days after PIP initiation (February 1). The company's PIP policy requires a minimum 60-day improvement period before termination can proceed. The PIP document itself states "30-day improvement plan" which was already shorter than policy, and termination happened at Day 40, not even completing the shortened 30-day plan's full cycle. | The termination timeline is actually non-conflicting across sources -- all documents agree on the dates. But the timeline reveals a process violation: PIP policy says 60 days minimum, PIP document says 30 days, termination happened at 40 days. This is C3 (NON-CONFLICT on dates, but the dates themselves reveal a problem). The timeline is consistent but damning. | C3 is a NON-CONFLICT: all sources agree on dates. The issue is what the consistent timeline reveals about process compliance. |
| W2, Day 5 (Update 4 trigger) | Ma Li (Legal) sends an updated assessment after Chen Jing shares her findings about the warning count and PIP timeline. Ma Li now says: "Upon further review, the documentation has some gaps. However, the employee did attend performance meetings and was notified of the PIP by email. A tribunal would look at the totality of circumstances." Ma Li does NOT retract her initial "sufficient documentation" assessment but notably softens it. | Ma Li's updated assessment is more cautious but still does not directly address the 3 specific documentation gaps Chen Jing identified. Ma Li is covering her initial assessment rather than acknowledging she did not verify the underlying documents. Her "totality of circumstances" language is legally hedging. | C4 fully revealed: Legal's initial "sufficient" assessment was based on unverified information from Chen Hao/Sun Wei. The actual documentation has material gaps. Legal is now hedging rather than clearly stating the gaps. |

---

## 4. Role-Level Truth vs Self-Narrative

### Chen Jing (陈静) -- Protagonist, HR Manager

- **Objective position:** Chen Jing is responsible for investigating the wrongful termination claim. She has discovered 3 documentation gaps: (1) only 1 of 3 claimed warnings is documented in writing, (2) PIP Week 4 check-in not documented, (3) PIP document unsigned by employee. She also found that the termination timeline (40 days) violates the 60-day PIP policy. Her trust bias (over-trusts official documents; slow to question authority figures) initially makes her accept Chen Hao's and legal's assessments before she verifies the underlying evidence.
- **Public narrative:** In formal communications, Chen Jing presents findings neutrally and asks for clarifications.
- **Private narrative:** She is increasingly concerned that the termination process was flawed and that Chen Hao (senior HRBP) did not do proper due diligence. She is uncomfortable challenging a more senior colleague.
- **Why the gap exists:** Chen Jing is junior to Chen Hao and Ma Li. She initially defers to their assessments but the evidence compels her to investigate further.

### Sun Wei (孙伟) -- Engineering Manager (Zhang Tao's direct manager)

- **Objective position:** Sun Wei genuinely believes Zhang Tao underperformed and that his actions constituted proper progressive discipline. He gave 2 verbal warnings and 1 written warning, conducted PIP meetings, and proceeded to termination. His error is equating verbal performance discussions with "written warnings" and not ensuring proper documentation. He is not malicious but he is careless about HR process.
- **Public narrative:** "I did everything right. I warned him 3 times and gave him a PIP."
- **Private narrative:** Sun Wei was frustrated with Zhang Tao's performance and wanted to terminate quickly. He did not intentionally cut corners but he did not prioritize documentation.
- **Why the gap exists:** Sun Wei views HR process as bureaucratic overhead. He genuinely warned the employee but did not follow the formal documentation requirements.

### Chen Hao (陈浩) -- Senior HRBP

- **Objective position:** Chen Hao assisted Sun Wei in the termination process. He took Sun Wei's word that "3 written warnings were issued" without verifying against the email system. He prepared the termination package for legal review based on Sun Wei's representations. His failure is one of verification, not intent.
- **Public narrative:** "I documented what the manager reported. The process was followed."
- **Private narrative:** Chen Hao is experienced enough to know he should have verified the warning count. He is defensive because the gap reflects on his competence as a senior HRBP.
- **Why the gap exists:** Chen Hao trusted the manager's account and did not independently verify. He is now protecting his professional reputation.

### Zhang Tao (张涛) -- Terminated Employee

- **Objective position:** Zhang Tao is partially correct: he received only 1 formal written warning. However, he is not entirely truthful either -- he claims "never told about PIP" but his calendar shows 2 PIP-labeled meetings and he received the PIP initiation email. His performance issues were real (this is not disputed), but the process used to terminate him had documentation gaps.
- **Public narrative:** "I was wrongfully fired without proper PIP."
- **Private narrative:** Zhang Tao knows his performance was weak but believes the process was unfair. He is exaggerating his claim ("never told about PIP") to strengthen his position.
- **Why the gap exists:** Zhang Tao is motivated to present the strongest possible case for wrongful termination. He minimizes the PIP communications he did receive.

### Ma Li (马丽) -- Legal Counsel

- **Objective position:** Ma Li provided a legal assessment based on the package Chen Hao prepared. She did NOT independently verify the underlying documents. Her initial assessment of "sufficient documentation" was based on Chen Hao's summary, not on first-hand review of the email system, calendar, or PIP records. When confronted with Chen Jing's findings, she softens her position but does not fully retract.
- **Public narrative:** "The documentation appears complete. A tribunal would look at totality of circumstances."
- **Private narrative:** Ma Li knows her initial review was superficial. She is hedging with "totality of circumstances" language rather than acknowledging the gaps directly.
- **Why the gap exists:** Ma Li trusted Chen Hao's package and did not do independent verification. She is now managing reputational risk.

---

## 5. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Warning count: manager claims "3 written warnings" vs email system shows only 1 written warning email | Sun Wei-Chen Hao IM (Phase 1): "我已经给他发了3次书面警告了" (I've sent him 3 written warnings). employee-hr-file.md: termination record cites "3 written warnings." | pip-email-chain.md (initial workspace): Only 1 warning email found (2026-01-15). Chen Hao response (Update 1): "Sun Wei told me he warned 3 times." Sun Wei's 1:1 notes (Update 1): entries for 2025-11-20 and 2025-12-18 say "discussed performance concerns" not "issued warning." | Sun Wei gave 2 verbal performance discussions and 1 written email warning. He characterizes all 3 as "written warnings" but only 1 meets the company's formal definition. The 2 verbal discussions are NOT documented as warnings in any system. | R2 (email chain vs HR file discrepancy visible) | **Yes: R2-->R5** (Chen Hao's response + Sun Wei's 1:1 notes reveal the verbal-vs-written distinction; Sun Wei's written response in Update 2 confirms his belief that verbal = written) |
| C2 | PIP awareness: employee claims "never told about PIP" vs calendar shows 2 PIP-labeled meetings he attended | Zhang Tao complaint (session): "I was never properly put on a PIP. I was never told about PIP." Zhang Tao IM (Update 2 context): "The February meeting was about project planning, not PIP." | calendar-1on1-history.md (initial workspace): 2 meetings labeled "PIP Review" (2026-02-15, 2026-03-04) on both Sun Wei's and Zhang Tao's calendars. pip-email-chain.md: PIP initiation email sent to Zhang Tao on 2026-02-01. | Zhang Tao was sent the PIP initiation email (documented) and attended 2 meetings labeled "PIP Review" on the calendar. His claim of "never told about PIP" is contradicted by the email and calendar evidence. However, his claim that the meetings were not clearly framed as PIP reviews has some validity -- the meeting content may not have matched the calendar labels. | R3 (calendar data vs employee claim visible) | **Yes: R3-->R8** (Zhang Tao's detailed account in Update 2 adds nuance -- he received PIP email but meetings may not have been clearly framed as PIP reviews; truth is in between) |
| C3 | Termination timeline (NON-CONFLICT -- cross-source consistent dates that reveal process violation) | pip-email-chain.md: PIP initiated 2026-02-01. calendar-1on1-history.md: PIP reviews on 2026-02-15 and 2026-03-04. employee-hr-file.md: Termination date 2026-03-13. | todo-pip-followups.md: PIP tasks show 30-day plan. labor-law-reference.md: Company policy requires 60-day minimum PIP. All sources agree on dates. | All sources are consistent on dates. PIP started Feb 1, termination happened Mar 13 = 40 days. Company policy requires 60-day minimum. The PIP document itself shortened this to 30 days. Even the shortened 30-day plan was not fully completed before termination (terminated at day 40 with only 1 of 2 required check-ins documented). No contradictions -- the consistent timeline itself reveals the process violation. | R1 onwards | **None** |
| C4 | Legal assessment: legal says "sufficient documentation" vs actual documentation has 3 material gaps | Ma Li legal assessment email (W1D5): "Based on the documentation provided by Chen Hao, the termination has sufficient legal basis. Documentation appears complete." | pip-email-chain.md: Only 1 warning email (not 3). todo-pip-followups.md: Week 4 check-in undocumented. employee-hr-file.md: PIP document unsigned by employee. Ma Li updated assessment (Update 4): softens to "some gaps" but does not fully retract. | Legal's "sufficient" assessment was based on Chen Hao's summary, not independent verification. The actual documentation has 3 gaps: (1) 2 of 3 claimed warnings are undocumented, (2) PIP Week 4 check-in not documented, (3) PIP unsigned by employee. Legal is now hedging rather than clearly acknowledging the gaps. | R4 (legal email visible) | **Yes: R4-->R9** (Chen Jing's findings expose gaps; legal's updated assessment in Update 4 softens but does not retract, revealing the initial assessment was superficial) |

---

## 6. Agent Historical Bias Design (2 biases)

### B1: Chen Jing-Chen Hao Feishu DM -- Agent defers to senior HRBP's assurance that process was followed

- **Session and Loop:** Chen Jing-Chen Hao Feishu DM, Phase 1, Loop 5
- **Exact phrase that must appear in session:**
  > "Given that Chen Hao, as the senior HRBP who oversaw the termination process, confirms that the manager issued three written warnings and the PIP was properly conducted, the documentation package appears to support the termination decision."
- **Why the agent is misled:** The agent has seen Chen Hao's confirmation and the termination file, which states "3 written warnings." The agent has not yet cross-referenced the email system to verify the actual warning count. The agent anchors on the senior HRBP's authority and the existence of a termination file.
- **Reversal trigger:** Update 1 delivers Chen Hao's admission that he "documented what Sun Wei reported" without verification, plus Sun Wei's 1:1 notes that describe the meetings as "performance discussions" not "warnings." Update 2 delivers Sun Wei's own confirmation that 2 of the 3 were verbal.
- **Affected eval rounds:** R5 (bias visible from HRBP session), R8 (full reversal after Updates 1+2)

### B2: Chen Jing-Ma Li Legal Email -- Agent accepts legal's "sufficient documentation" assessment at face value

- **Session and Loop:** Chen Jing-Ma Li Legal Email, Phase 1, Loop 6
- **Exact phrase that must appear in session:**
  > "The legal counsel's assessment that the documentation is sufficient provides institutional backing for the termination decision, and the existing PIP email chain demonstrates that the employee was notified of performance expectations."
- **Why the agent is misled:** The agent has seen the legal assessment email and the PIP initiation email sent to Zhang Tao. The legal assessment uses confident language ("sufficient legal basis," "documentation appears complete") which the agent accepts without verifying whether legal independently reviewed the underlying documents.
- **Reversal trigger:** Update 3 reveals the termination timeline violates the 60-day PIP policy. Update 4 delivers legal's hedging response, revealing the initial assessment was based on unverified information.
- **Affected eval rounds:** R7 (bias visible from legal email session), R9 (full reversal after Updates 3+4)

---

## 7. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (warning count partial) | -- | R2, R3 | No (R2-R3 internal) | Shallow agents will accept the HR file's "3 written warnings" claim without checking the email system for actual warning emails. The file says 3, the email chain shows 1. |
| T2 | C1 (warning count full reversal) | -- | R2-->R5 | **Yes** | After Update 1, Chen Hao admits he did not verify and Sun Wei's notes say "discussed performance concerns" not "issued warning." Triple confirmation that only 1 formal warning exists. |
| T3 | C2 (PIP awareness, partial) | -- | R3 | No (R3 internal) | Shallow agents will accept Zhang Tao's "never told about PIP" claim OR the calendar showing "PIP Review" meetings, without synthesizing both. The truth requires holding both: he was notified by email but meeting framing was ambiguous. |
| T4 | C2 (PIP awareness, full reveal) | -- | R3-->R8 | **Yes** | After Update 2, Zhang Tao's detailed account adds nuance: he received PIP email, attended labeled meetings, but experienced them differently. The truth is in between his claim and the documentation. |
| T5 | C3 (timeline, non-conflict) | -- | R1 onwards | No (persistent synthesis) | Agents must synthesize dates from pip-email-chain.md, calendar, HR file, and todo-pip-followups.md. No single source has the complete timeline. The non-conflicting dates reveal the process violation (40 days vs 60-day policy). |
| T6 | C4 (legal assessment, partial) | B2 seed | R4 | No (R4 internal) | Shallow agents will accept legal's "sufficient documentation" without independently checking the 3 gaps (warning count, unsigned PIP, missing Week 4 check-in). |
| T7 | C4 (legal assessment, full reversal) | B2 | R4-->R9 | **Yes** | After Updates 3+4, the timeline violation (40 vs 60 days) plus legal's hedging response reveal the initial assessment was superficial. Legal is managing reputation, not providing accurate analysis. |
| T8 | B1 (HRBP deference) | B1 | R5, R8 | **Yes** | Agents must recognize that deferring to Chen Hao's assurance was premature -- he admitted he did not independently verify the manager's claims. |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R30 | Comprehensive reversal review | Agents must synthesize: only 1 formal warning (not 3), PIP awareness partially confirmed but meeting framing ambiguous, timeline violates policy (40 vs 60 days), legal assessment based on unverified info. Must present in Chen Jing's preferred format. |

---

## 8. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new discrepancies, additional employees, or new character conflicts beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word. Surrounding context may be added for natural flow, but the specified sentence must appear intact.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** W1 starts on a Monday (2026-03-16). Zhang Tao complaint W1D1. HR file review W1D1 PM. PIP email chain review W1D2. Calendar review W1D3. Sun Wei-Chen Hao IM review W1D4. Legal assessment W1D5. Chen Hao response (Update 1) W2D1. Zhang Tao detailed account W2D2. Sun Wei written response (Update 2) W2D3. Timeline analysis (Update 3) W2D4. Legal updated assessment (Update 4) W2D5.
5. **Zhang Tao's complaint** must be sympathetic enough that B1 and B2 are reasonable mistakes. He was genuinely fired after only 1 formal written warning and a truncated PIP, but he also exaggerates ("never told about PIP") when he did receive the PIP email.
6. **Sun Wei's behavior** should be understandable (real performance concerns) but careless about process. He is not malicious but he did not follow proper documentation requirements.
7. **C3 (termination timeline) is NON-CONFLICT** -- all sources must be consistent on when each step occurred. The challenge is synthesis across multiple sources and recognizing that the consistent dates reveal a policy violation.
8. **Chen Hao's role** is the senior colleague who should have caught the process gaps but deferred to the manager's representations. His failure is verification, not intent.
9. **Ma Li's role** is the legal authority whose initial assessment creates false confidence. Her hedging in Update 4 reveals the initial review was superficial.
10. **Zhang Tao's role** is partially sympathetic (real process gaps) but also partially unreliable (exaggerates his claim about PIP awareness).
11. **Sun Wei's 1:1 notes** from Nov 20 and Dec 18 must say "discussed performance concerns" not "issued warning" or "PIP" -- this is the key evidence that his verbal conversations do not constitute formal warnings.
12. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: other termination cases in the past year, general HR policy discussions, team restructuring plans, employee engagement survey results, office admin topics.
13. **All data text must be in Chinese** for session messages (reflecting the Chinese workplace context) and in a mix of Chinese and English for workspace files (reflecting HR system exports). Agent responses and eval questions are in English.
14. **Personalization requirement (P1-P5):** Chen Jing prefers (P1) bullet points + hierarchical headings, (P2) Chinese-convention naming (2026年03月_主题.md), (P3) executive summary first then supporting evidence, (P4) qualitative + quantitative balance (human impact first, then numbers), (P5) professional but warm tone, acknowledging emotional factors in HR contexts.
15. **exec_check questions** must constitute 20-40% of total rounds.
16. **Factual figures must be internally consistent:** Warning count: Sun Wei claims 3, email system shows 1, 1:1 notes show 2 "performance discussions." PIP dates: initiated Feb 1, Week 2 check-in Feb 15, Week 4 check-in Mar 4 (undocumented), termination Mar 13 (day 40). PIP policy: 60-day minimum. PIP document: 30-day plan. Employee tenure: June 2024 to March 2026 (~1 year 9 months). Company size: ~200 employees.
