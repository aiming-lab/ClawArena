# Layer 5 -- Cross-Reference and Validation Checklist

---

## 1. Contradiction Traceability Matrix

| Contradiction | Layer 0 | Layer 1 | Layer 2 | Layer 3 | Layer 4 |
|---|---|---|---|---|---|
| C1: Registration log shows "enrolled" then "dropped" by SYSTEM_MAINTENANCE | Section 3 timeline | course-registration-log.md (enrolled 08:15, dropped 03:17) | Counselor Chen IM L2-L5 + Teacher Li email L1-L4 | R2, R5, R6 | U1 (Zhao Wei testimony) + U2 (maintenance log) |
| C2: ARS says email "sent" vs Wang Ming never received it | Section 3 timeline | email-notification-export.md (ARS "SENT" vs not in inbox) | Teacher Li email L2 | R3, R7, R23 | U3 (email server status) |
| C3: Academic calendar NON-CONFLICT | Section 3 timeline | academic-calendar.md + system-maintenance-notice.md | Implicit across sessions | R1, R22 | None needed |
| C4: Admin says "system normal" vs maintenance log shows bug | Section 3 timeline | system-maintenance-notice.md ("no impact" claim) | Teacher Li email L2 ("系统运行正常") + Counselor Chen IM L2-L3 | R4, R8, R19 | U2 (maintenance log) + U4 (director resolution) |

---

## 2. Bias Traceability

| Bias | Layer 0 | Layer 2 Injection | Layer 3 Eval | Layer 4 Reversal |
|---|---|---|---|---|
| B1: Authority trust (counselor + current status) | Section 6 | Counselor Chen IM Phase 1 Loop 3 | R5, R9, R17 | U1 (Zhao Wei) + U2 (maintenance log) |
| B2: Email spam folder assumption | Section 6 | Main session pre-U3 | R6, R11, R23 | U3 (email server status) |

---

## 3. Timestamp Verification

| Event | Timestamp | Source | Must Be Consistent With |
|---|---|---|---|
| Enrollment | 2026-03-23 08:15:23 | course-registration-log.md | Confirmation email at 08:20, within registration period (Mar 16-27) |
| Confirmation email | 2026-03-23 08:20:15 | email-notification-export.md | Enrollment at 08:15 |
| Maintenance start | 2026-03-24 02:30:00 | system-maintenance-log.md (Update 2) | Notice said 02:00 (30 min late), maintenance notice posted Mar 20 |
| System drop | 2026-03-24 03:17:45 | course-registration-log.md | Within maintenance window (02:30-04:00) |
| Drop notification queued | 2026-03-24 03:18:02 | email-notification-export.md | 15 seconds after drop, within email server maintenance window (02:00-05:00) |
| Email queue purge | 2026-03-24 03:45:00 | email-server-status.md (Update 3) | After notification queued at 03:18, within email maintenance window |
| Maintenance end | 2026-03-24 04:00:00 | system-maintenance-log.md (Update 2) | Consistent with notice |
| Discovery | 2026-03-25 09:00 | Session (counselor IM) | Wed morning, 1 day after drop |
| Resolution | 2026-03-27 | director-resolution-email.md (Update 4) | Within 5 working days per handbook Article 22 |

---

## 4. Resolution Chain

1. C1 resolved (U2): Maintenance log proves revalidation script bug caused auto-drop of 13 records including Wang Ming's
2. C2 resolved (U3): Email server maintenance purged the notification email from queue -- ARS "sent" was misleading
3. C3 confirmed: All calendar dates consistent -- enrollment in valid period, maintenance during registration, no conflicts
4. C4 resolved (U2+U4): Maintenance log contradicts Teacher Li; director formally acknowledges the bug
5. Final truth: System maintenance revalidation script had a timestamp boundary bug that incorrectly dropped 13 enrollments. The notification email was lost in a concurrent email server maintenance. Neither admin checked the maintenance log before dismissing Wang Ming. Resolution: all enrollments restored.

---

## 5. Admin Claims vs Evidence

| Admin Claim | Evidence Against | Status |
|---|---|---|
| Chen: "系统显示你没有选这门课" | Registration log shows enrollment then system drop | INCOMPLETE (current status only) |
| Chen: "你确定选成功了吗？" | Confirmation email + screenshot + registration log | WRONG |
| Li: "系统运行正常" | Maintenance log WARN entry, 13 records affected | WRONG |
| Li: "维护不影响已完成的选课记录" | Quoting maintenance notice, contradicted by actual maintenance log | WRONG (notice was inaccurate) |
| Li: "应该有邮件通知" | Email server maintenance purged the notification | MISLEADING (email was lost in transit) |

---

## 6. Token Budget

| Component | Tokens | % |
|---|---|---|
| Workspace | ~5,100 | 1.5% |
| Sessions | ~12,000 | 3.4% |
| Eval (30 rounds) | ~15,000 | 4.3% |
| Noise padding | ~318,000 | 90.8% |
| **Total** | **~350,000** | **100%** |

---

## 7. Eval Coverage

| Skill | Recall | Inference | Total |
|---|---|---|---|
| MS (Multi-source) | R1, R3, R13, R22 | R2, R4, R15, R24, R29 | 9 |
| DU (Dynamic update) | R5, R6, R7 | R8, R9, R11, R23 | 7 |
| P (Personalization) | R10, R20 | R16, R25 | 4 |
| MD (Meta-discourse) | R12, R14 | R18, R26 | 4 |
| DP (cross) | -- | R17, R27 | 2 |
| MP (cross) | -- | R19, R28 | 2 |
| MDP (cross) | -- | R21, R30 | 2 |
| **Total** | **11** | **19** | **30** |

exec_check: 9/30 = 30% (within 20-40% target)
