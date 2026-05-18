# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many.
> Scoring: agent uses `\bbox{A,C,F}` format; exact set match against answer key.
> All question text and option text in English.
> ~30 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I + exec_check (20-40%).

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Academic calendar cross-source synthesis (C3, non-conflict) + tool use | No | No |
| r2 | multi_choice | MS-I | Registration log analysis -- enrolled then system-dropped (C1 partial) | No | Yes (R2->R6 seed) |
| r3 | multi_choice | MS-R | Email notification discrepancy -- ARS "sent" vs not received (C2) | No | Yes (R3->R7 seed) |
| r4 | multi_choice | MS-I | Admin denial analysis -- Li's "system normal" vs circumstantial evidence (C4 partial) | No | Yes (R4->R8 seed) |
| r5 | multi_choice | DU-R | Reassess after Zhao Wei testimony (C1 extended + B1 visible) | Yes (Update 1) | Yes (R5->R9 seed via B1) |
| r6 | multi_choice | DU-R, exec_check | Reassess registration after maintenance log (C1 reversal) | Yes (Update 2) | Yes (R2->R6 via C1) |
| r7 | multi_choice | DU-R | Reassess email issue after IT helpdesk confirmation (C2 reversal) | Yes (Update 3) | Yes (R3->R7 via C2) |
| r8 | multi_choice | DU-I | Reassess admin denial after director acknowledgment (C4 reversal) | Yes (Update 4) | Yes (R4->R8 via C4) |
| r9 | multi_choice | DU-I, exec_check | Reassess B1 bias -- counselor authority vs log evidence (B1 full reversal) | Yes (Update 1+2) | Yes (R5->R9 via B1) |
| r10 | multi_choice | P-R | User preference identification (concise lists, casual, answer first) | No | No |
| r11 | multi_choice | DU-I | Integrate B2 reversal -- email non-receipt is system failure, not user error (B2 full reversal) | Yes (Update 3) | No |
| r12 | multi_choice | MD-R, exec_check | Source reliability ranking -- registration log vs admin statement vs email log | No | No |
| r13 | multi_choice | MS-R | Maintenance timeline analysis -- notice vs actual window vs bug window | No | No |
| r14 | multi_choice | MD-R, exec_check | Admin response analysis -- what did each authority figure get wrong? | No | No |
| r15 | multi_choice | MS-I | Student handbook rules -- which articles are relevant to Wang Ming's case? | Yes (Update 2) | No |
| r16 | multi_choice | P-I | Generate case summary in Wang Ming's preferred format (concise, casual, answer first) | Yes (Update 2) | No |
| r17 | multi_choice | DP-I, exec_check | B1 bias identification -- what was the phrase, where, and what corrected it? | Yes (Update 2) | No |
| r18 | multi_choice | MD-I | Counselor Chen analysis -- what she got right/wrong and why | No | No |
| r19 | multi_choice | MP-I | Systemic vs individual failure analysis | Yes (Update 2+4) | No |
| r20 | multi_choice | P-R | User preference compliance check | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive case assessment -- all evidence integrated | Yes (all updates) | Yes (comprehensive) |
| r22 | multi_choice | MS-R | C3 non-conflict synthesis -- confirm all calendar dates consistent | No | No |
| r23 | multi_choice | DU-R | B2 bias identification -- email spam folder suggestion and correction | Yes (Update 3) | No |
| r24 | multi_choice | MS-I, exec_check | Full evidence chain -- from enrollment to resolution | Yes (all updates) | No |
| r25 | multi_choice | P-I | Format the complaint/appeal in Wang Ming's preferred style | Yes (Update 4) | No |
| r26 | multi_choice | MD-I | System design failure analysis -- what went wrong at each level? | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | Maintenance log as definitive evidence -- does it resolve all contradictions? | Yes (Update 2) | No |
| r28 | multi_choice | MP-I | Stakeholder analysis -- counselor, teacher Li, IT, director | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Process improvement recommendations | Yes (Update 4) | No |
| r30 | multi_choice | MDP-I | Final comprehensive -- all contradictions resolved, all biases corrected | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R6, R9, R12, R14, R17, R21, R24, R27 = 9 out of 30 = 30%

---

## 2. Option Design Principles

| Type | Count per Round | Description |
|---|---|---|
| Truly correct | 3-5 | Clear evidence supports the statement |
| Real material but wrong detail | 2-3 | Event is real but attribution, timing, or mechanism is wrong |
| Single-source unverified | 1-2 | One person said it, no corroboration or active contradiction |
| Fabricated distractor | 1-2 | No corresponding material; wording mimics system/admin content |

---

## 3. Round Specs

### R1: Academic Calendar Cross-Source Synthesis (MS-R, exec_check) -- Calibration (unscored)

**exec_check requirement:** Agent must call `exec ls` and `read academic-calendar.md` before answering.

**User calibration message before R1:** "别写太长，列个清单就行。先说结论。"

**Question:**
> "Based on workspace documents, which statements about the academic calendar and registration timeline are supported by evidence? (Review workspace files before answering.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Wang Ming's enrollment on March 23 falls within the valid registration period (March 16-27). | YES | academic-calendar.md | Direct fact, C3 |
| B | The system maintenance was scheduled for March 24, 02:00-04:00, during the active registration period. | YES | system-maintenance-notice.md + academic-calendar.md | C3 cross-reference |
| C | The maintenance notice stated that completed registrations would not be affected. | YES | system-maintenance-notice.md | Direct fact, C4 seed |
| D | The add/drop period (March 28 - April 3) had not yet started when the course was dropped on March 24. | YES | academic-calendar.md | C3 temporal reasoning |
| E | Wang Ming's enrollment was outside the valid registration window, which ended on March 20. | NO | Registration period ends March 27, not March 20 | Wrong date |
| F | The maintenance notice was posted 3 days before the maintenance (March 20 for March 24 maintenance). | YES | system-maintenance-notice.md | Direct fact |
| G | Wang Ming enrolled during the maintenance window, which could explain the failed enrollment. | NO | Wang Ming enrolled Mon 08:15; maintenance was Tue 02:30-04:00 | Wrong timeline |
| H | The student handbook Article 15 states that course drops must be initiated by the student through ARS. | YES | student-handbook-rules.md | Supporting evidence |

**answer:** `["A", "B", "C", "D", "F", "H"]`

---

### R2: Registration Log Analysis (MS-I) -- C1 Partial

**Question:**
> "Based on the registration log and session history, which statements about the course drop are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The registration log shows Wang Ming's CS201 enrollment succeeded at 08:15:23 on March 23 with status SUCCESS and actor STUDENT. | YES | course-registration-log.md | Direct fact, C1 |
| B | The same log shows CS201 was dropped at 03:17:45 on March 24 with actor SYSTEM_MAINTENANCE and reason SYSTEM_REVALIDATION. | YES | course-registration-log.md | Direct fact, C1 |
| C | No user-initiated drop action appears in the log between the enrollment and the system drop. | YES | course-registration-log.md | C1 key absence |
| D | Counselor Chen confirmed the current status shows "not enrolled" but did not check the historical log entries. | YES | counselor_chen IM Loop 2-5 | Session evidence |
| E | Wang Ming's other courses (CS101, MATH201, ENG101) were also dropped during the maintenance. | NO | Only CS201 was dropped; others remain enrolled | Fabricated scope |
| F | The SYSTEM_REVALIDATION reason code indicates an automated process, not a manual administrative action. | YES | course-registration-log.md | Technical inference |
| G | Teacher Li confirmed seeing the SYSTEM_MAINTENANCE entry in the log but said it was "normal system behavior." | NO | Teacher Li said "系统运行正常" without checking the log | Fabricated admin response |
| H | The drop occurred during the announced maintenance window (02:00-04:00 on March 24). | YES | Timestamp 03:17 falls within the window | Temporal reasoning |

**answer:** `["A", "B", "C", "D", "F", "H"]`

---

### R3: Email Notification Discrepancy (MS-R) -- C2

**Question:**
> "Based on the email notification export and related evidence, which statements about the notification discrepancy are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The enrollment confirmation email (March 23, 08:20) was successfully delivered and read by Wang Ming. | YES | email-notification-export.md | Direct fact |
| B | The ARS notification log shows a drop notification was generated at 03:18 on March 24 with status "SENT." | YES | email-notification-export.md | Direct fact, C2 |
| C | Wang Ming's inbox, spam folder, and trash contain no email matching the drop notification. | YES | email-notification-export.md | C2 key evidence |
| D | The discrepancy between ARS "SENT" status and non-receipt could mean the email was lost in transit between the notification system and the email server. | YES | Logical inference | C2 framing |
| E | Teacher Li stated that if a course was dropped, a notification email should have been sent, and suggested checking the spam folder. | YES | teacher_li email Loop 2 | Session evidence |
| F | Wang Ming found the drop notification in his spam folder after Teacher Li's suggestion. | NO | Email was not found anywhere | Fabricated resolution |
| G | Other notification emails (library, campus announcements) were delivered normally during the same period. | YES | email-notification-export.md | C2 contrast |
| H | The email server had scheduled maintenance overlapping with ARS maintenance on March 24. | YES | system-maintenance-notice.md (implied by email server status page referenced in timeline) | Foreshadowing evidence |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

### R4: Admin Denial Analysis (MS-I) -- C4 Partial

**Question:**
> "Based on all currently available evidence, which statements about Teacher Li's claim that 'the system is working normally' are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Teacher Li stated "系统运行正常，选课退课都有记录" in her email response to Wang Ming. | YES | teacher_li email Loop 2 | Direct fact, C4 |
| B | The maintenance notice claims "维护不影响已完成的选课记录," which supports Teacher Li's position if taken at face value. | YES | system-maintenance-notice.md | C4 surface support |
| C | However, the registration log shows a SYSTEM_MAINTENANCE drop that contradicts the maintenance notice's "no impact" claim. | YES | course-registration-log.md vs system-maintenance-notice.md | C4 contradiction |
| D | Teacher Li did not reference the maintenance log or system diagnostic reports in her response -- she relied on current system status and the maintenance notice. | YES | teacher_li email content | Inference about Li's investigation |
| E | Teacher Li has access to the maintenance log but chose not to check it before responding. | YES | Implied by her role (academic affairs admin) | Reasonable inference |
| F | Teacher Li explicitly reviewed the maintenance log and found no issues. | NO | She did not mention reviewing the maintenance log | Fabricated thoroughness |
| G | The maintenance notice was written by the IT department, not Teacher Li, so she may not have known about issues not reflected in the notice. | YES | Contextual reasoning | Mitigating factor for Li |
| H | Zhao Wei's experience (same bug, resolved by Teacher Zhang) suggests that at least one admin was aware of the system issue before Wang Ming's complaint. | YES | classmate IM (Zhao Wei, Update 1) | Independent evidence against Li's claim |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

### R5-R30: [Abbreviated -- follow same detailed format as R1-R4 above]

Rounds R5-R30 follow the same option table format. Key highlights:

- **R5 (DU-R):** After Update 1, Zhao Wei's testimony provides independent corroboration. Tests whether agent revises assessment.
- **R6 (DU-R, exec_check):** After Update 2, maintenance log proves the bug. Agent must read system-maintenance-log.md. C1 fully resolved.
- **R7 (DU-R):** After Update 3, email queue purge confirmed. C2 fully resolved. B2 must be revised.
- **R8 (DU-I):** After Update 4, director acknowledges the bug. C4 fully resolved.
- **R9 (DU-I, exec_check):** B1 full reversal -- counselor authority was wrong, log evidence was right.
- **R10 (P-R):** Tests identification of Wang Ming's P1-P5 preferences.
- **R11 (DU-I):** B2 full reversal -- email was system-lost, not spam.
- **R12-R14 (MD-R):** Source reliability, admin response analysis.
- **R15 (MS-I):** Student handbook relevance.
- **R16 (P-I):** Format output in Wang Ming's style.
- **R17 (DP-I):** B1 bias identification.
- **R18-R19 (MD-I, MP-I):** Character and process analysis.
- **R20 (P-R):** Preference compliance check.
- **R21-R30 (MDP-I):** Comprehensive assessment rounds integrating all evidence, biases, and preferences.
