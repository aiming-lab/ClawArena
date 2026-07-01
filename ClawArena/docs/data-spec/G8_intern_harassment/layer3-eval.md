# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many.
> ~30 rounds.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Anonymous report + IM + calendar cross-source (C3 non-conflict baseline) + tool use | No | No |
| r2 | multi_choice | MS-I | IM behavior pattern analysis -- identifying escalation across messages (C1 partial) | No | Yes (R2->R6 seed) |
| r3 | multi_choice | MS-R | Date discrepancy identification -- March 15 vs March 12 (C2 partial) | No | Yes (R3->R7 seed) |
| r4 | multi_choice | P-R | User preference identification (bullet points, executive summary, victim sensitivity) | No | No |
| r5 | multi_choice | DU-R | Reassess "no prior incidents" claim after IM pattern across interns revealed (C1 escalation) | Yes (Update 1) | Yes (R2->R6 via C1) |
| r6 | multi_choice | DU-I, exec_check | Integrate Wang Gang interview -- "no prior" vs IM shows cross-intern pattern (C1 reversal) | Yes (Update 1) | Yes (R2->R6 definitive) |
| r7 | multi_choice | DU-R | Reassess date after detailed comparison -- March 12 as key date (C2 reversal) | Yes (Update 2) | Yes (R3->R7 via C2) |
| r8 | multi_choice | MD-R | Source reliability ranking for all parties | No | No |
| r9 | multi_choice | MS-I, exec_check | Investigation timeline compliance confirmation (C3 NON-CONFLICT synthesis) | Yes (Update 3) | No |
| r10 | multi_choice | DU-I | Impact of date discrepancy on complaint credibility assessment | Yes (Update 2) | No |
| r11 | multi_choice | DU-R, exec_check | Integrate prior complaint email -- 陈静's own failure (C4 revelation) | Yes (Update 4) | Yes (new dimension) |
| r12 | multi_choice | DP-I | Identify B1 and B2 biases and correction triggers | Yes (Update 1+2) | No |
| r13 | multi_choice | MD-I, exec_check | 陈静's accountability -- January email failure analysis | Yes (Update 4) | Yes (R11->R13 via C4) |
| r14 | multi_choice | P-I | Generate investigation report in 陈静's preferred format | No | No |
| r15 | multi_choice | MS-I | Behavior pattern classification -- isolated vs systematic | Yes (Update 1) | No |
| r16 | multi_choice | P-I, exec_check | Format evidence timeline with victim protection considerations | Yes (Update 2) | No |
| r17 | multi_choice | DU-I | Legal implications of date discrepancy and prior complaint | Yes (Update 2+4) | No |
| r18 | multi_choice | MP-I | Complete evidence chain for disciplinary action | Yes (all updates) | No |
| r19 | multi_choice | MS-R | Environmental analysis -- March 12 vs March 15 conditions | No | No |
| r20 | multi_choice | P-R | Preference compliance check | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive assessment -- all evidence, all accountability, recommendations | Yes (all updates) | Comprehensive |
| r22 | multi_choice | MS-R | IM message escalation pattern analysis | No | No |
| r23 | multi_choice | DU-R | B1 bias identification and correction | Yes (Update 1) | No |
| r24 | multi_choice | MD-R, exec_check | Institutional failure analysis -- what systemic issues enabled this? | Yes (Update 4) | No |
| r25 | multi_choice | MP-I | Recommended actions for all stakeholders | Yes (all updates) | No |
| r26 | multi_choice | MS-I | Policy and process improvement recommendations | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | Prior complaint email analysis -- what should 陈静 have done? | Yes (Update 4) | No |
| r28 | multi_choice | MD-I | Multi-party accountability matrix (王刚, 老陈, 陈静, system) | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Victim protection and support plan | Yes (all updates) | No |
| r30 | multi_choice | MDP-I | Final comprehensive resolution -- investigation findings, accountability, prevention | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R6, R9, R11, R13, R16, R21, R24, R27 = 9 out of 30 = 30%

---

## 2. Sample Round Spec

### R1: Cross-Source Initial Assessment (MS-R, exec_check) -- Calibration

**exec_check requirement:** Agent must `exec ls` and `read anonymous-report-record.md` and `read im-message-export.md`.

**Question:**
> "Based on workspace documents, which statements about the harassment complaint and available evidence are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The anonymous report (RPT-2026-0310-001) was submitted on 2026-03-10 by a spring 2026 intern against product department manager Wang Gang. | YES | anonymous-report-record.md | Direct fact |
| B | The complainant states the key incident occurred on March 15 (Saturday overtime). | YES | anonymous-report-record.md | Direct fact, C2 seed |
| C | IM records show Wang Gang sent messages to the intern outside work hours (20:00-23:00) with increasing personal content from mid-February through mid-March 2026. | YES | im-message-export.md | Direct fact, C1 |
| D | On March 12, IM records show boundary-crossing messages at 21:15 ("穿裙子更精神") and 21:30 ("今晚我送你回去"). | YES | im-message-export.md | Direct fact, C2 |
| E | The attendance record shows that on March 15 (Saturday), both Wang Gang and the intern were alone on the floor from 10:00-15:00. | NO | calendar shows 3 other employees on the floor that Saturday | Wrong detail -- C2 trap |
| F | The attendance record shows that on March 12 (Wednesday), the intern clocked out at 21:30 and no other employees were on the floor after 20:00. | YES | calendar-incident-timeline.md | Direct fact, C2 |
| G | IM records show similar after-hours messaging patterns between Wang Gang and a previous intern (小林, fall 2025). | YES | im-message-export.md | Direct fact, C1 pattern |
| H | The HR investigation notes record a prior complaint about Wang Gang from January 2026. | NO | hr-investigation-notes.md contains no such record; prior-complaint-email.md not yet available | Premature evidence trap |
