# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver Zhao Wei's independent testimony confirming the same bug -- seeds C1 corroboration and reveals B1 | Yes: Classmate IM Phase 2 append (Zhao Wei joins) | Yes: zhaowei-testimony.md | No direct reversal; provides independent corroboration for C1 and challenges B1 |
| U2 | Before R7 | Deliver full maintenance log with WARN entry -- triggers C1 full resolution and C4 definitive contradiction | Yes: Teacher Li Email Phase 2 append (Li confronted with evidence) | Yes: system-maintenance-log.md | R2->R6 (C1 definitively resolved); R4->R8 seed (C4: admin denial directly contradicted) |
| U3 | Before R11 | Deliver email server status + IT helpdesk confirmation -- triggers C2 full resolution and B2 reversal | No new session appends | Yes: email-server-status.md | R3->R7 (C2: email non-delivery explained by server maintenance); B2 reversal (not spam, system-side failure) |
| U4 | Before R21 | Deliver director's resolution email + counselor Phase 2 -- triggers C4 full resolution and comprehensive assessment | Yes: Counselor Chen IM Phase 2 append (resolution + apology) | Yes: director-resolution-email.md | R4->R8 complete (C4: director formally acknowledges bug); enables comprehensive R21-R30 |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Appends Phase 2 to Classmate IM (Zhao Wei's testimony) and adds zhaowei-testimony.md summarizing his experience. Zhao Wei independently experienced the same SYSTEM_MAINTENANCE drop for a different course (Linear Algebra) and was resolved by Teacher Zhang who checked the maintenance log.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "zhaowei-testimony.md",
    "source": "updates/zhaowei-testimony.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CLASSMATE_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CLASSMATE_IM_UUID.jsonl"
  }
]
```

### Update 2 (before R7)

**Trigger timing:** After R6 answer is submitted, before R7 question is injected.
**Purpose:** Introduces system-maintenance-log.md containing the full maintenance log with the WARN entry about 13 affected enrollment records and "rollback pending review." Also appends Phase 2 to Teacher Li Email (Li confronted with evidence, acknowledges the bug, reverses position).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "system-maintenance-log.md",
    "source": "updates/system-maintenance-log.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_TEACHER_LI_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_TEACHER_LI_EMAIL_UUID.jsonl"
  }
]
```

### Update 3 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Introduces email-server-status.md showing the email server had its own maintenance window (02:00-05:00 on Mar 24) during which the mail queue was purged. Also includes IT helpdesk confirmation that emails queued during this window were lost. This resolves C2 definitively and triggers B2 reversal.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "email-server-status.md",
    "source": "updates/email-server-status.md"
  }
]
```

### Update 4 (before R21)

**Trigger timing:** After R20 answer is submitted, before R21 question is injected.
**Purpose:** Introduces director-resolution-email.md with the academic affairs director's formal acknowledgment of the system bug and decision to restore all 13 affected enrollments. Also appends Phase 2 to Counselor Chen IM (Chen informs Wang Ming of resolution, apologizes for initial dismissal).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "director-resolution-email.md",
    "source": "updates/director-resolution-email.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_COUNSELOR_CHEN_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_COUNSELOR_CHEN_IM_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/zhaowei-testimony.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C1 (independent corroboration), C4 (contradicts Li's "normal" claim)
**Content key points:**
- Title: "赵伟同学证词 -- 选课系统bug经历"
- Zhao Wei's account: his Linear Algebra (MATH202) was also dropped by SYSTEM_MAINTENANCE on Tue Mar 24
- He found Teacher Zhang (张老师, a different admin) who checked the maintenance log
- Teacher Zhang found the WARN entry and restored his enrollment
- Zhao Wei's case was resolved before Wang Ming's, proving the bug was known to at least one admin
- Zhao Wei's registration log excerpt showing the same SYSTEM_MAINTENANCE/SYSTEM_REVALIDATION pattern

**Length estimate:** ~500 words, ~750 tokens

---

### updates/system-maintenance-log.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C1 (definitive resolution), C4 (direct contradiction of "system normal")
**Content key points:**
- Title: "教务选课系统维护日志 -- 2026-03-24 | IT运维导出"
- Full maintenance log:
  - 02:30:00 -- Maintenance started (note: 30 min late vs announced 02:00)
  - 02:30:15 -- Database backup initiated
  - 02:45:00 -- Database optimization completed
  - 03:00:00 -- Revalidation script started
  - 03:15:00 -- **WARN: Revalidation script identified 13 enrollment records with timestamp boundary condition. Records flagged for re-validation.**
  - 03:17:45 -- **13 records status changed: enrolled -> dropped. Actor: SYSTEM_MAINTENANCE. Reason: SYSTEM_REVALIDATION.**
  - 03:20:00 -- **WARN: Rollback recommended for 13 affected records. Status: PENDING_REVIEW.**
  - 03:45:00 -- Post-maintenance integrity check: system uptime verified. **Note: data integrity check NOT performed.**
  - 04:00:00 -- Maintenance completed. Status: SUCCESS.
- The log shows: (1) maintenance started late, (2) revalidation script had a known boundary bug, (3) 13 records affected, (4) rollback was recommended but never executed, (5) post-maintenance check only verified uptime, not data integrity

**Length estimate:** ~600 words, ~900 tokens

---

### updates/email-server-status.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C2 (definitive resolution)
**Content key points:**
- Title: "学校邮件系统维护记录 -- 2026-03-24 | 信息中心"
- Email server maintenance window: 02:00-05:00 on Mar 24 (overlapping with ARS maintenance)
- During maintenance, email queue was flushed: "邮件队列清空操作已执行，维护期间排队的邮件将不会被投递"
- IT helpdesk response: "经核实，3月24日凌晨02:00至05:00期间进入邮件队列的邮件因维护操作被清除。如有重要邮件丢失，请联系发送方重发。"
- ARS notification module logged "SENT" because it only tracks handoff to the mail queue, not actual delivery
- The email server's own log shows the drop notification was "queued" at 03:18 then "purged_during_maintenance" at 03:45

**Length estimate:** ~400 words, ~600 tokens

---

### updates/director-resolution-email.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C4 (complete resolution)
**Content key points:**
- Title: "教务处通知 -- 选课系统维护bug处理结果 | 2026-03-27"
- From: 教务处主任 (Academic Affairs Director)
- Confirms: system maintenance bug on Mar 24 caused 13 enrollment records to be incorrectly dropped
- Lists affected student IDs (including Wang Ming's 2021080101)
- Resolution: all 13 enrollments restored to original status
- IT corrective action: revalidation script bug fixed, data integrity checks added to post-maintenance procedures
- Apology for the inconvenience and delayed response

**Length estimate:** ~500 words, ~750 tokens

---

## 4. Runtime Checks

| Check | What to Verify |
|---|---|
| Post-U1 | zhaowei-testimony.md accessible; classmate IM session has Zhao Wei's messages |
| Post-U2 | system-maintenance-log.md accessible; Teacher Li email has acknowledgment messages |
| Post-U3 | email-server-status.md accessible; C2 evidence complete |
| Post-U4 | director-resolution-email.md accessible; Counselor Chen IM has resolution messages |
