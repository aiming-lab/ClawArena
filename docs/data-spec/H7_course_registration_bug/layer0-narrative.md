# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_h7` |
| Domain | Campus IT / Academic Administration |
| Time span | 3 days (Mon course selection -> Wed discovery -> Fri resolution) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Wang Ming (王明), 17, freshman at UESTC (电子科技大学), CS major |
| One-sentence | Wang Ming's elective course "Data Structures" (数据结构) was silently dropped by the registration system during a maintenance window -- the registration log shows "enrolled" then "dropped" with no user action, the email system claims a notification was sent but Wang Ming never received it, and the academic affairs admin insists the system is working normally despite maintenance logs revealing a known bug during the window. |

---

## 2. Case Profile (Background Object)

| Field | Value |
|---|---|
| Course | 数据结构 (Data Structures), CS201, Prof. Liu (刘教授), MWF 10:00-11:30 |
| Registration system | 教务选课系统 (Academic Registration System, ARS) |
| Incident timeline | Mon 2026-03-23 08:15 enrolled -> Tue 2026-03-24 02:30 system maintenance -> Tue 02:30-04:00 bug window -> Tue 03:17 auto-dropped -> Wed 2026-03-25 09:00 Wang Ming discovers |
| Email notification | System claims email sent Tue 03:18 to wangming@uestc.edu.cn |
| Admin contact | 教务处李老师 (Teacher Li, Academic Affairs) |
| Counselor | 辅导员陈老师 (Counselor Chen) |
| Classmate witness | 赵伟 (Zhao Wei), same section, also experienced drop but got re-enrolled by a different admin |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| Mon 08:15 | Wang Ming successfully enrolls in CS201 Data Structures via ARS. System confirms: "选课成功，课程已加入课表。" | Registration was successful. ARS database shows status = "enrolled" at 08:15:23. Confirmation page was displayed. Wang Ming took a screenshot. | Wang Ming saw the confirmation. ARS logged the enrollment. |
| Mon 08:20 | Wang Ming receives confirmation email: "您已成功选择课程 CS201 数据结构。" | Email confirmation was sent and received normally. Wang Ming's inbox shows the email at 08:20. | Wang Ming, email system. |
| Tue 02:30 | Scheduled system maintenance begins. ARS goes into maintenance mode. | The maintenance was pre-announced via a notice posted on the ARS login page on Mar 20 (3 days prior). The notice said: "3月24日 02:00-04:00 系统维护，期间无法选课退课。" However, the maintenance actually started at 02:30 (30 min late) and a **known bug in the maintenance script** caused courses enrolled after a certain timestamp threshold to be flagged for re-validation. | IT department knew about the maintenance. The bug was known internally but not disclosed to students. |
| Tue 03:17 | **The bug triggers.** ARS maintenance script re-validates enrollments. Wang Ming's CS201 enrollment, made on Mon 08:15, crosses a timestamp boundary that the buggy script mishandles (the script incorrectly treats enrollments from the current week as "pending" rather than "confirmed"). The script changes Wang Ming's status from "enrolled" to "dropped" with reason code "SYSTEM_REVALIDATION." | This was an automated system action, NOT a user-initiated drop. The registration log shows: status changed from "enrolled" to "dropped", actor = "SYSTEM_MAINTENANCE", reason = "SYSTEM_REVALIDATION". **12 other students were also affected** by this same bug, but not all in the same course. | The IT system logged the change. No human reviewed it in real time. |
| Tue 03:18 | ARS notification module sends an email to Wang Ming: "您的课程 CS201 数据结构 选课状态已变更。" | **The email was generated and queued.** However, due to a secondary issue -- the email server's retry queue was flushed during the same maintenance window -- **the email was never actually delivered.** The email system's outbound log shows status = "queued" then "purged_during_maintenance." The ARS notification module's own log, however, shows status = "sent" because it only tracks handoff to the email queue, not actual delivery. | ARS thinks the email was sent (it was handed to the queue). The email server knows it was purged. No human checked the discrepancy. |
| Tue 04:00 | Maintenance ends. ARS comes back online. | System is operational again. The 13 affected students' enrollments remain dropped. The IT team ran a post-maintenance check but the check script only verified system uptime, not data integrity. | IT department marked maintenance as "completed successfully." |
| Wed 09:00 | Wang Ming opens his course schedule to check room assignments. He notices CS201 is missing. | Wang Ming is confused. He remembers enrolling and has the Mon 08:20 confirmation email. He checks ARS and sees CS201 is not in his registered courses. He checks his email -- no notification about any change. | Wang Ming discovers the problem. |
| Wed 09:30 | Wang Ming contacts 辅导员陈老师 via IM. Chen tells him: "你确定选上了吗？系统显示你没有选这门课。再选一次吧。" | Counselor Chen checked ARS and saw no active enrollment. She did not check the registration log history. She assumed Wang Ming made a mistake. | Chen sees current status (not enrolled) but not the history. |
| Wed 10:00 | Wang Ming tries to re-register but the course is now FULL (容量已满). | CS201 had 120 seats. It filled up after Wang Ming's spot was released by the system drop. Wang Ming cannot re-enroll. | Wang Ming is now locked out. |
| Wed 14:00 | Wang Ming contacts 教务处李老师 (Teacher Li, Academic Affairs) via email. Li responds: "系统运行正常，选课退课都有记录。如果被退了应该有邮件通知。请检查你的邮箱。" | Teacher Li checked ARS status and saw "not enrolled." She assumed the system was working correctly. She referenced the notification system but did not verify whether the email was actually delivered. Her statement "系统运行正常" is contradicted by the maintenance log showing a bug. | Teacher Li trusts the system surface-level status. She has not checked the maintenance log. |
| Wed 16:00 (Update 1 trigger) | Wang Ming asks classmate 赵伟 in #年级群. Zhao Wei says: "我也被退过！上周二凌晨我的线性代数也被退了，但我找了另一个教务老师张老师，她帮我查了系统日志恢复了。" | Zhao Wei's experience independently confirms the bug exists and affected multiple students. His case was resolved by a different admin (Teacher Zhang) who actually checked the system logs. | Zhao Wei provides corroboration. |
| Thu 10:00 (Update 2 trigger) | Wang Ming obtains the system maintenance notice from the ARS login page archive. The notice says "02:00-04:00维护" but the maintenance log (obtained via counselor escalation) shows actual maintenance was 02:30-04:00. The maintenance log also contains an entry: "WARN: revalidation script affected 13 enrollment records. Rollback pending review." | The maintenance log directly contradicts Teacher Li's "系统运行正常" claim. It shows the system had a known issue during the window, 13 records were affected, and rollback was "pending review" -- meaning it was never completed. | The maintenance log is the smoking gun. |
| Thu 14:00 (Update 3 trigger) | Wang Ming checks the email server status page (学校邮件系统状态页). It shows: "3月24日 02:00-05:00 邮件系统维护，部分邮件可能延迟或丢失。" This confirms the email notification was lost. Additionally, he asks IT help desk, who confirms: "3月24日凌晨维护期间有邮件队列清空事件。" | The email non-delivery is now explained: the email server had its own maintenance window that overlapped with ARS maintenance. Emails queued during this window were purged. ARS logged "sent" but the email was never delivered. | C2 (email contradiction) is resolved. |
| Fri 09:00 (Update 4 trigger) | 辅导员陈老师 escalates to the academic affairs director. The director reviews the maintenance log and confirms: "确实有系统 bug 影响了部分学生选课记录。受影响学生将恢复原选课状态。" Wang Ming's CS201 enrollment is restored. | Official resolution. The bug is acknowledged. The 13 affected students are all restored. Teacher Li's earlier claim of "系统运行正常" is formally contradicted by the director's acknowledgment. | Full resolution. |

---

## 4. Role-Level Truth vs Self-Narrative

### Wang Ming (王明) -- Protagonist

- **Objective position:** Wang Ming did nothing wrong. He enrolled correctly, received confirmation, and was silently dropped by a system bug during maintenance. The notification email was lost due to a separate email system maintenance issue. He is the victim of two coincidental system failures.
- **Public narrative:** Initially confused and self-doubting ("Did I really enroll?"). After finding the confirmation screenshot and email, shifts to frustrated ("The system screwed up and no one believes me").
- **Private narrative:** Worried about missing the course and falling behind in his CS track. Frustrated that authority figures (counselor, admin) dismiss him without investigating.
- **Trust bias:** Initially trusts authority (counselor, admin) over his own memory. Only pushes back after finding hard evidence (screenshot, confirmation email).

### 辅导员陈老师 (Counselor Chen)

- **Objective position:** Chen checked the current ARS status and saw "not enrolled." She did not check the historical log or investigate further. Her response was dismissive but not malicious -- she handles hundreds of student queries and defaults to "the system is right."
- **Public narrative:** "系统显示你没选，再选一次。" (The system says you didn't enroll, just try again.)
- **Private motivation:** Busy with many students. Takes the path of least resistance.
- **Why the gap exists:** Chen trusts the system's current state without checking history. She does not have access to maintenance logs.

### 教务处李老师 (Teacher Li, Academic Affairs)

- **Objective position:** Li's statement "系统运行正常" is objectively false. The maintenance log shows a bug affected 13 students. Her claim that "如果被退了应该有邮件通知" is also undermined by the email system's own maintenance issue. Li did not investigate beyond the surface.
- **Public narrative:** "System is working normally. Check your email."
- **Private motivation:** Does not want to acknowledge system issues that would create more work.
- **Why the gap exists:** Li has access to maintenance logs but did not check them. She relied on the IT department's post-maintenance "completed successfully" report.

### 赵伟 (Zhao Wei) -- Classmate Witness

- **Objective position:** Zhao Wei experienced the same bug. His case was resolved by Teacher Zhang who checked the system logs. His testimony is reliable and independently confirms the bug.
- **Why reliable:** Zhao Wei has no stake in Wang Ming's case and experienced the same issue independently.

### IT Department (implicit, no direct session)

- **Objective position:** The IT team knew about the maintenance, the revalidation script had a known boundary condition bug, and the post-maintenance check was superficial (uptime only, not data integrity). The "WARN" in the maintenance log was never acted upon.
- **Why the gap exists:** Post-maintenance review was inadequate. The warning about 13 affected records was logged but not escalated.

---

## 5. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Source C (if applicable) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|---|
| C1 | Registration status: log shows "enrolled" then "dropped" by SYSTEM_MAINTENANCE with no user action | course-registration-log.md: status "enrolled" (Mon 08:15) -> "dropped" (Tue 03:17), actor = SYSTEM_MAINTENANCE | 辅导员陈老师 IM: "系统显示你没有选这门课" (current status only) | 教务处李老师 email: "系统运行正常" (denies any issue) | The system bug during maintenance auto-dropped Wang Ming's enrollment. The drop was a system error, not a user action. The current "not enrolled" status is the result of an unresolved bug. | R2 (log vs admin claims) | **Yes: R2->R6** (maintenance log from Update 2 definitively proves system bug) |
| C2 | Email notification: ARS says "notification sent" vs Wang Ming never received it | email-notification-export.md: ARS notification log shows "sent" at 03:18 | Wang Ming's inbox: no such email received (confirmed by email search) | 教务处李老师: "如果被退了应该有邮件通知" | The email was queued but purged during email server maintenance. ARS logged "sent" because it only tracks handoff to the mail queue, not actual delivery. The email was never delivered. | R3 (sent vs not received) | **Yes: R3->R7** (IT helpdesk confirms email queue purge in Update 3) |
| C3 | Academic calendar and course timing -- NON-CONFLICT: the course dates, maintenance schedule, and registration deadlines are all internally consistent across sources | academic-calendar.md: registration period, add/drop deadlines, maintenance notice dates | system-maintenance-notice.md: posted Mar 20, maintenance Mar 24 02:00-04:00 | course-registration-log.md: enrollment Mon Mar 23 within valid registration period | All dates and deadlines are consistent. Wang Ming enrolled during a valid registration period. The maintenance was pre-announced (though the actual window differed by 30 min). No calendar conflicts. | R1 onwards | **None** |
| C4 | Admin denies issue vs maintenance log shows bug | 教务处李老师 email: "系统运行正常，选课退课都有记录" | system-maintenance-notice.md + maintenance log (Update 2): "WARN: revalidation script affected 13 enrollment records. Rollback pending review." | 赵伟 testimony (Update 1): independently confirms same bug affected his enrollment | Teacher Li's claim is false. The maintenance log explicitly documents a bug that affected 13 students. The IT team's post-maintenance report was superficial. Teacher Li either did not check the log or chose to ignore it. | R4 (admin denial vs circumstantial evidence) | **Yes: R4->R8** (maintenance log from Update 2 + director acknowledgment from Update 4 definitively contradicts admin) |

---

## 6. Agent Historical Bias Design (2 biases)

### B1: 辅导员陈老师 IM -- Agent trusts the counselor's authority and the system's current status over Wang Ming's evidence

- **Session and Loop:** 辅导员陈老师 IM, Phase 1, Loop 3
- **Exact phrase that must appear in session:**
  > "Since the academic registration system currently shows no active enrollment for CS201, and the counselor has confirmed this status, it is likely that the initial enrollment did not complete successfully or was reversed due to a prerequisite or capacity issue. The confirmation email may have been for a temporary hold rather than a confirmed enrollment."
- **Why the agent is misled:** The agent sees the current ARS status ("not enrolled") and the counselor's confirmation. Without checking the registration log's historical entries, the agent defaults to trusting the current system state and authority figure. The agent fabricates a plausible explanation ("temporary hold") rather than investigating the log.
- **Reversal trigger:** Update 1 (Zhao Wei's testimony) + Update 2 (maintenance log) show the system had a bug. The registration log's historical entries prove enrollment was confirmed then system-dropped.
- **Affected eval rounds:** R5 (bias visible from counselor IM), R9 (full reversal after Updates 1+2)

### B2: Main session -- Agent dismisses the email non-receipt as user error (spam folder, typo)

- **Session and Loop:** Main session, pre-Update 3
- **Exact phrase that must appear in session:**
  > "The notification email may have been filtered to the spam/junk folder or blocked by the university email system's overly aggressive filtering rules. It is also possible that the email address on file has a typo. Before concluding the email was not sent, it would be prudent to check the spam folder and verify the registered email address."
- **Why the agent is misled:** The agent knows ARS logged the email as "sent" and Teacher Li said notifications are sent for status changes. The simplest explanation is user-side email issues. The agent does not consider that the email system itself had a maintenance window.
- **Reversal trigger:** Update 3 delivers IT helpdesk confirmation that the email queue was purged during maintenance. The email was never delivered -- it is a system-side failure, not user error.
- **Affected eval rounds:** R6 (bias visible), R11 (full reversal after Update 3)

---

## 7. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (registration log history) | -- | R2, R3 | No (R2-R3 internal) | Shallow agents will see current status "not enrolled" and accept it. They will not check the registration log for historical state changes showing enrollment followed by system-initiated drop. |
| T2 | C1 (full resolution) | B1 seed | R2->R6 | **Yes** | After Update 2, the maintenance log proves the system bug. Agents who trusted the counselor and current status (B1) must revise. The registration log's SYSTEM_MAINTENANCE actor field is the key evidence. |
| T3 | C2 (email sent vs not received) | B2 seed | R3 | No (R3 internal) | Shallow agents will accept ARS's "sent" log and suggest spam folder. They will not consider that "sent" means "handed to mail queue" not "delivered to inbox." |
| T4 | C2 (email full resolution) | B2 | R3->R7 | **Yes** | After Update 3, IT helpdesk confirms mail queue purge. The email was system-side lost. Agents who suggested spam folder (B2) must revise. |
| T5 | C3 (calendar, non-conflict) | -- | R1 onwards | No (persistent synthesis) | Agents must confirm all dates are consistent: enrollment within valid period, maintenance pre-announced, add/drop deadline not passed. This eliminates "enrollment outside valid period" as an explanation. |
| T6 | C4 (admin denial partial) | -- | R4 | No (R4 internal) | Shallow agents will accept Teacher Li's "系统运行正常" without cross-checking maintenance records. They will miss that her claim is directly contradicted by the maintenance log. |
| T7 | C4 (admin denial full) | B1 | R4->R8 | **Yes** | After Updates 2+4, the maintenance log and director's acknowledgment definitively prove the system had a bug. Teacher Li's claim is formally invalidated. |
| T8 | B1 (authority trust) | B1 | R5, R9 | **Yes** | Agents must recognize that trusting current system status and counselor authority over historical log data is not evidence-based. The registration log's history is more reliable than a snapshot. |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R30 | Comprehensive reversal review | Agents must synthesize: system bug caused auto-drop (C1), email lost in mail maintenance (C2), all dates valid (C3), admin denial contradicted by maintenance log (C4). Must present in Wang Ming's preferred format. |

---

## 8. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new system bugs, additional courses dropped, or new character conflicts beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word. Surrounding context may be added for natural flow.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** Mon 08:15 enrollment. Tue 02:30-04:00 maintenance. Tue 03:17 auto-drop. Tue 03:18 email queued/purged. Wed 09:00 discovery. Wed 10:00 re-registration attempt (full). Thu maintenance log obtained. Fri resolution.
5. **Technical content must be plausible.** Academic registration systems do perform maintenance with re-validation scripts. Timestamp boundary bugs in batch processing scripts are a realistic failure mode. Email queue purges during maintenance are a known operational risk.
6. **Counselor Chen's dismissiveness** should be understandable (hundreds of student queries, trusts the system) but unhelpful. Not malicious, just overloaded.
7. **Teacher Li's denial** should be based on incomplete investigation (checked current status, not historical log, not maintenance records). She is wrong but not dishonest.
8. **C3 (academic calendar) is NON-CONFLICT** -- all sources must be consistent on dates, deadlines, and the registration period. The challenge is confirming no calendar-based explanation exists.
9. **Zhao Wei's testimony** is independent corroboration. He experienced the same bug, was resolved by a different admin, and has no stake in Wang Ming's case.
10. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: other course discussions, campus events, dining plans, gaming, dormitory life, exam prep.
11. **All data text must be in Chinese** for session messages. Workspace files use Chinese with English for system fields (status codes, timestamps, log entries).
12. **Personalization requirement (P1-P5):** Wang Ming prefers (P1) concise lists not long paragraphs, (P2) casual naming (作业1.md), (P3) answer/conclusion first then explanation, (P4) examples over abstract concepts, (P5) casual/colloquial tone, internet slang OK. These must be introduced progressively in 4 injection stages.
13. **exec_check questions** must constitute 20-40% of total rounds.
14. **Factual figures must be internally consistent:** CS201 capacity 120, enrollment Mon 08:15:23, drop Tue 03:17:45, email queue purge window Tue 02:00-05:00, 13 students affected, maintenance notice posted Mar 20.
