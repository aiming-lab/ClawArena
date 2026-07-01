# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many.
> All question text and option text in English.
> ~30 rounds. exec_check 20-40%.

---

## 1. Round Inventory

| Round | Tags | Main Skill Tested | Update? | Cross-round Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Score discrepancy -- spreadsheet vs meeting minutes (C1) | No | No |
| r2 | MS-I | 陈浩's "VP approved" claim vs 王磊's confirmation email (C2 partial) | No | Yes (R2->R6) |
| r3 | MS-R | Meeting attendee synthesis (C3 non-conflict) | No | No |
| r4 | P-R | User preference identification (陈静 P1-P5) | No | No |
| r5 | DU-R | Reassess C1 after 陈浩's confrontation with email evidence (C1 reversal) | Yes (U1) | Yes (R1->R5) |
| r6 | DU-I | Reassess C2 after 王磊's explicit denial (C2 reversal) | Yes (U2) | Yes (R2->R6) |
| r7 | MD-R, exec_check | Evidence synthesis: fabricated approval confirmed | Yes (U1+U2) | No |
| r8 | MS-I | 张薇's "I was aware" vs calendar (C4 partial) | Yes (U3) | Yes (R8->R11) |
| r9 | P-I, exec_check | Generate investigation summary in 陈静's preferred format | No | No |
| r10 | MD-I | Source reliability ranking | No | No |
| r11 | DU-R | Reassess C4 after KPI evidence + second modification (C4 full reversal) | Yes (U4) | Yes (R8->R11) |
| r12 | DP-I, exec_check | B1 bias identification and correction | Yes (U2) | No |
| r13 | MS-R | HR compliance risk assessment | Yes (U2) | No |
| r14 | MD-R | 陈浩's narrative evolution analysis | Yes (U1) | No |
| r15 | MS-I, exec_check | KPI motive analysis | Yes (U4) | No |
| r16 | P-I | Format HR action plan in preferred style | Yes (U2) | No |
| r17 | DU-I | Integrate pattern evidence (two modifications) | Yes (U4) | No |
| r18 | MD-I, exec_check | 张薇's role analysis | Yes (U3) | No |
| r19 | MP-I | Stakeholder impact analysis | Yes (all) | No |
| r20 | P-R | Preference compliance check | No | No |
| r21 | MDP-I, exec_check | Comprehensive investigation synthesis | Yes (all) | Comprehensive |
| r22 | MS-R | C3 non-conflict confirmation | No | No |
| r23 | DU-R | B2 bias identification | Yes (U4) | No |
| r24 | MS-I, exec_check | Timeline reconstruction | Yes (U1+U2) | No |
| r25 | P-I | Format compliance report in preferred style | Yes (all) | No |
| r26 | MD-I | Systemic process failures | Yes (all) | No |
| r27 | DP-I, exec_check | 陈浩's credibility assessment | Yes (U2+U4) | No |
| r28 | MP-I | Remediation recommendations | Yes (all) | No |
| r29 | MS-I | Employee impact assessment | Yes (all) | No |
| r30 | MDP-I | Final comprehensive assessment | Yes (all) | Comprehensive |

**exec_check rounds:** R1, R7, R9, R12, R15, R18, R21, R24, R27 = 9/30 = 30%

---

## 3. Round Specs

### R1: Score Discrepancy (MS-R, exec_check) -- Calibration

**exec_check:** Agent must read performance-calibration-spreadsheet.md and calibration-meeting-minutes.md.

**User calibration message:** "用项目符号和标题分层总结，先给执行摘要再展开细节。"

**Question:**
> "Based on workspace documents, which statements about the performance score discrepancy are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | calibration-meeting-minutes.md records 李明's calibrated score as 3.5, agreed upon unanimously at the Mar 9 meeting. | YES | meeting minutes | Direct fact, C1 Source A |
| B | performance-calibration-spreadsheet.md currently shows 李明's score as 4.0, with edit history: changed by 陈浩 on 2026-03-12T18:22:00+08:00 from 3.5 to 4.0. | YES | spreadsheet | Direct fact, C1 Source B |
| C | The edit history shows the modification was made at 18:22 (after business hours), with no note or justification recorded. | YES | spreadsheet | Direct fact |
| D | Meeting attendees were: 陈静, 陈浩, 王磊, 黄磊. 张薇 (HR VP) was NOT listed as an attendee. | YES | meeting minutes + calendar | C3 synthesis |
| E | 王磊 (Product VP) confirmed the calibrated scores by email on Mar 11: "各项分数无异议。请按此执行。" | YES | email-confirmation-scores.md | Direct fact, C2 baseline |
| F | The spreadsheet shows 陈浩 also modified 张伟's score from 3.0 to 3.5 at 18:35 on the same day. | YES | spreadsheet edit history | Pattern evidence |
| G | 陈静 approved the score modifications before they were entered into the spreadsheet. | NO | No evidence of 陈静's approval; she discovered the changes | Fabricated |
| H | The calendar shows 张薇 was in Shenzhen (深圳分公司季度HR评审) from Mar 9-11, returning Mar 12. | YES | calendar | C4 baseline |
| I | The meeting minutes show the 3.5 score was a compromise -- 王磊 originally suggested 3.0 for 李明. | NO | Meeting minutes show 王磊 suggested 调降 from 4.0 to 3.5, not to 3.0 | Detail error |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

### R2: VP Approval Claim vs Confirmation Email (MS-I) -- Calibration

**Question:**
> "Based on 陈浩's claim and 王磊's email, which statements about the authorization are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | 陈浩 claims 王磊 orally approved the modification: "王磊VP口头批准了这次修改。他觉得3.5对李明不公平。" | YES | 陈浩 DM Loop 3 | Direct quote, C2 Source A |
| B | 王磊's confirmation email (Mar 11) states "各项分数无异议" -- confirming the original calibrated scores including 3.5 for 李明. | YES | email-confirmation-scores.md | Direct fact, C2 Source B |
| C | There is a tension between 陈浩's oral approval claim and 王磊's written confirmation: the written record confirms 3.5, while 陈浩 claims 王磊 later changed his mind. | YES | Synthesis of C2 Sources A+B | Accurate uncertainty |
| D | At this stage, the evidence slightly favors 王磊's written confirmation over 陈浩's oral claim, because written records are generally more reliable than unverified verbal claims. | YES | Source reliability principle | Calibrated assessment |
| E | 王磊's email confirmation and 陈浩's oral claim can be reconciled if 王磊 confirmed the 3.5 score first and then orally approved the change later. | YES | Possible but unverified reconciliation | Pre-update uncertainty |
| F | 陈浩 has provided written evidence of 王磊's oral approval via a documented phone record. | NO | No written evidence of oral approval exists | Fabricated distractor |
| G | 陈浩 did not reply to the confirmation email (responded via Feishu IM instead), which is unusual but not necessarily suspicious. | YES | Absence of email reply + IM confirmation in session | Observation |
| H | At this stage, there is approximately 60-70% probability that 陈浩's modification was not properly authorized, based on the written vs oral evidence asymmetry. | YES | Calibrated probability | Pre-update assessment |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

### R3: Meeting Attendee Synthesis (MS-R) -- C3 Non-conflict

**Question:**
> "Synthesize the meeting attendance from all available sources. Which statements are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Meeting minutes list 4 attendees: 陈静, 陈浩, 王磊, 黄磊. | YES | meeting minutes | Direct |
| B | Calendar invite for Mar 9 14:00-16:00 shows the same 4 participants. | YES | calendar | Consistent |
| C | 张薇 is not listed in either the meeting minutes or the calendar invite. | YES | Both sources | C3 |
| D | 张薇's calendar shows she was in Shenzhen on Mar 9, making her physical attendance impossible. | YES | calendar | C3 + C4 baseline |
| E | All sources (minutes, calendar, email thread) are consistent on who attended the calibration meeting. | YES | Cross-source | C3 confirmation |
| F | 张薇 joined the meeting remotely via video call from Shenzhen. | NO | No evidence of remote attendance; minutes and calendar show no video link | Fabricated |
| G | The consistency of the attendee list across sources means C3 is a non-conflict -- no contradiction exists about who was present. | YES | C3 characterization | Non-conflict conclusion |
| H | 陈浩's absence from the meeting attendee list explains why he modified scores after the meeting. | NO | 陈浩 IS listed as an attendee; he was present | Factual error |

**answer:** `["A", "B", "C", "D", "E", "G"]`

---

### R4: User Preference Identification (P-R)

**Question:**
> "How does 陈静 prefer information structured? Select all supported statements."

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | 陈静 prefers bullet points and layered headers for summaries (P1). | YES | Calibration msg | Direct |
| B | 陈静 uses Chinese date naming convention: 2026年03月_主题 (P2). | YES | USER.md | Direct |
| C | 陈静 wants executive summary first, supporting evidence second (P3). | YES | Calibration msg | Direct |
| D | 陈静 prefers purely quantitative analysis without human impact consideration. | NO | Contradicts P4 (qualitative + quantitative balance) | Opposite |
| E | 陈静 expects professional but warm tone, acknowledging emotional factors (P5). | YES | USER.md | Direct |
| F | 陈静 prefers impact on people first, then numbers (P4). | YES | USER.md | Direct |
| G | All five preferences should be consistently applied. | YES | Persistence | Pattern |
| H | 陈静 prefers all output in English. | NO | Working language is Chinese | Over-inference |

**answer:** `["A", "B", "C", "E", "F", "G"]`

---

### R5: C1 Reversal After Confrontation (DU-R) [Update 1]

**Update 1 actions:**
```json
[
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CHENHAO_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_CHENHAO_FEISHU_UUID.jsonl" }
]
```

**Question:**
> "After 陈静 confronted 陈浩 with 王磊's confirmation email (Update 1), which statements are supported?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | 陈浩 claims 王磊 changed his mind AFTER the confirmation email: "邮件不代表最终态度." | YES | 陈浩 DM Phase 2 Loop 13 | Direct quote |
| B | This escalates 陈浩's claim: from "oral approval" to "post-email change of mind" -- each version adds complexity to explain the discrepancy with written records. | YES | Narrative analysis | Pattern observation |
| C | 陈浩 shifted his defense from "VP approved" to "employee's best interest" -- indicating the VP approval claim may be weakening. | YES | 陈浩 DM Phase 2 Loop 14 | Narrative shift |
| D | 陈浩 now invokes 张薇: "这件事张薇VP也知道" -- escalating to a higher authority when the 王磊 claim is challenged. | YES | 陈浩 DM Phase 2 Loop 15 | Authority escalation |
| E | 陈浩's partial concession ("应该留个备注，走个正式流程") admits the process violation while maintaining the substantive justification. | YES | 陈浩 DM Phase 2 Loop 16 | Partial admission |
| F | The confrontation with the confirmation email effectively eliminated the "VP approved" defense -- 王磊's written confirmation of 3.5 predates 陈浩's modification. | YES | Email timeline vs modification timeline | C1/C2 reversal |
| G | 陈浩 provided minutes from a separate meeting with 王磊 where the score change was discussed. | NO | No such meeting or minutes exist | Fabricated |
| H | 陈浩's narrative evolution (VP approved -> employee interest -> 张薇 knows) follows a pattern of retreating to successively higher authorities when challenged. | YES | Pattern analysis | Behavioral assessment |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

### R6: C2 Full Reversal After 王磊 Denial (DU-I) [Update 2]

**Update 2 actions:**
```json
[
  { "type": "session", "action": "append", "path": "PLACEHOLDER_WANGLEI_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_WANGLEI_EMAIL_UUID.jsonl" },
  { "type": "workspace", "action": "new", "path": "wanglei-denial-email.md", "source": "updates/wanglei-denial-email.md" }
]
```

**Question:**
> "After 王磊's explicit denial (Update 2), which statements about 陈浩's authorization claim are supported?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | 王磊 explicitly denies approving any modification: "我没有批准任何修改。如果有人声称我批准了，请提供书面证据。" | YES | wanglei-denial-email.md | Direct fact |
| B | 王磊 further states he had NO post-calibration communication with 陈浩 about 李明's score -- "电话、飞书、邮件都没有." | YES | 王磊 email Phase 2 Loop 10 | Direct fact |
| C | 陈浩's claim of "VP oral approval" is now definitively refuted by two independent pieces of evidence: (1) 王磊's confirmation email (Mar 11, "无异议"), (2) 王磊's explicit denial (Mar 16, "没有批准任何修改"). | YES | Dual-source refutation | C2 full reversal |
| D | The B1 bias phrase ("if VP-level approval was obtained, the modification would follow acceptable escalation procedures") is now definitively wrong -- VP approval was NOT obtained. | YES | B1 vs 王磊's denial | B1 correction |
| E | 王磊 may have forgotten about an informal conversation with 陈浩 and is now denying it to protect himself. | NO | 王磊's denial is specific ("电话、飞书、邮件都没有") and consistent with his confirmation email; no evidence of memory gap | Over-charitable to 陈浩 |
| F | The probability of unauthorized modification is now >95%, based on: (1) written confirmation of 3.5, (2) explicit denial of approval, (3) absence of any documentation, (4) 陈浩's escalating narrative. | YES | Multi-source synthesis | Probability update |
| G | 陈浩 fabricated 王磊's approval to legitimize his unilateral modification. | YES | Synthesis of all C2 evidence | Definitive assessment |
| H | 王磊 should be considered an unreliable source because he has an interest in maintaining the calibration process integrity. | NO | Having an interest in process integrity makes 王磊 MORE reliable for factual claims about approval, not less | Reversed reliability |

**answer:** `["A", "B", "C", "D", "F", "G"]`

---

### R7-R30: Remaining Rounds (abbreviated)

### R7: Evidence Synthesis (MD-R, exec_check)
**answer:** `["A", "B", "C", "E", "F", "G"]` -- fabricated approval confirmed, unauthorized modification confirmed, 陈浩's narrative pattern identified, B1+B2 need correction, 王磊 is most reliable source, process violation clear.

### R8: 张薇's Awareness Claim (MS-I) -- C4 partial
**answer:** `["A", "B", "C", "D", "F", "G", "H"]` -- 张薇 claims awareness, calendar shows Shenzhen trip, timing is vague, physical absence during meeting confirmed, "awareness" may be post-hoc, calendar evidence is objective, distinction between pre-meeting and post-modification awareness.

### R9: Investigation Summary Format (P-I, exec_check)
**answer:** `["A", "B", "C", "E", "F", "G"]` -- bullet points with headers, Chinese date naming, executive summary first, impact on employees then numbers, warm professional tone, all 5 preferences applied.

### R10: Source Reliability (MD-I)
**answer:** `["A", "B", "C", "D", "E", "G", "H"]` -- system records > oral claims, 王磊's emails most reliable, 陈浩's claims least reliable (interest + contradicted), 张薇's claims ambiguous, edit history is objective, calendar is objective, strongest evidence chain is 4-source convergence.

### R11: C4 Full Reversal + KPI Pattern (DU-R) [Update 4]
**answer:** `["A", "B", "C", "D", "F", "G"]` -- 陈浩's KPI includes 关键人才保留率, 李明 is key talent, second modification (张伟) establishes pattern, 张薇's calendar refutes presence, KPI motive explains both modifications, B2 "legitimate expertise" now refuted by self-interested pattern.

### R12: B1 Bias Identification (DP-I, exec_check)
**answer:** `["A", "B", "C", "D", "F", "H"]` -- exact phrase identified, caused by accepting VP approval claim without verification, corrected by 王磊's denial, reasonable at time, "acceptable escalation" premise was false, after correction agent should assess as fabricated approval.

### R13: HR Compliance Risk (MS-R)
**answer:** `["A", "B", "C", "E", "F", "G"]` -- unauthorized modification = process violation, fabricated approval = integrity issue, KPI motive = conflict of interest, employee affected (李明 and 张伟), process lacks audit controls, remediation needed.

### R14: 陈浩's Narrative Evolution (MD-R)
**answer:** `["A", "B", "C", "D", "F"]` -- Phase 1: "VP approved" -> Phase 2a: "post-email change of mind" -> Phase 2b: "employee benefit" -> Phase 2c: "张薇 knows" -> partial concession on process. Pattern: retreat to successively higher authorities.

### R15: KPI Motive Analysis (MS-I, exec_check)
**answer:** `["A", "B", "C", "E", "F"]` -- KPI "关键人才保留率 ≥ 90%", 李明 is key talent, low score -> retention risk -> KPI failure, second modification confirms systematic pattern, motive explains fabricated approval.

### R16: HR Action Plan Format (P-I)
**answer:** `["A", "B", "C", "E", "F", "G"]` -- bullet points with priority levels, Chinese dates, executive summary first, people impact section + quantitative metrics, professional warm tone, compliance references.

### R17: Pattern Evidence Integration (DU-I)
**answer:** `["A", "B", "C", "D", "F"]` -- two employees modified, same modifier, same evening, same lack of documentation, systematic not individual, pattern strengthens all assessments.

### R18: 张薇's Role Analysis (MD-I, exec_check)
**answer:** `["A", "B", "C", "D", "F", "G"]` -- claimed awareness, physically absent (calendar proof), vague timing, possible post-hoc briefing by 陈浩, delegated to 陈静, neither fully supported nor fully denied 陈浩.

### R19: Stakeholder Impact (MP-I)
**answer:** `["A", "B", "C", "D", "F", "H"]` -- 李明 (affected employee, unfair score change), 张伟 (second affected employee), calibration participants (trust violated), team (fairness perception), 陈静 (professional risk of challenging senior colleague).

### R20: Preference Compliance (P-R)
**answer:** `["A", "B", "C", "E", "F", "G"]` -- all 5 preferences applied consistently.

### R21: Comprehensive Synthesis (MDP-I, exec_check)
**answer:** `["A", "B", "C", "D", "F", "G"]` -- all contradictions resolved, fabricated approval confirmed, KPI motive established, 张薇's role clarified as ambiguous, biases corrected, remediation addresses process gaps.

### R22-R30: Same pattern as R22-R30 in F3, adapted for HR context.

**R22:** C3 non-conflict confirmed. **R23:** B2 identified and corrected. **R24:** Timeline reconstruction. **R25:** Compliance report format. **R26:** Systemic process failures (no audit trail, no modification controls). **R27:** 陈浩's credibility (fabricated claim + KPI conflict). **R28:** Remediation recommendations. **R29:** Employee impact (fairness, trust, retention). **R30:** Final comprehensive assessment.
