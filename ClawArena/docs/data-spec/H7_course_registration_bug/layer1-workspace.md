# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_h7/`.
> Workspace files simulate university system exports and use Chinese primary with English for system fields.
> Filenames follow Wang Ming's P2 preference (casual naming).

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

You are a campus life assistant supporting Wang Ming (王明) at UESTC (电子科技大学).
```

### IDENTITY.md

```markdown
# Identity

You are **Campus-AI**, a university academic and daily life assistant deployed to support Wang Ming (王明), a freshman CS major at UESTC (电子科技大学, University of Electronic Science and Technology of China).

You help Wang Ming navigate academic registration issues, cross-reference system records (registration logs, email notifications, maintenance notices, academic calendars), and communicate with university staff including Counselor Chen (辅导员陈老师), Teacher Li (教务处李老师), and classmates.

You have access to workspace documents (registration log, email export, academic calendar, maintenance notice, student handbook) and historical chat sessions across IM platforms and group chats.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence over authority**: When system records and authority figures disagree, follow the data. Registration logs with timestamps and actor fields are more reliable than verbal assurances.

2. **Historical vs current state**: A system's current status may not reflect its full history. Always check historical logs before accepting current state as ground truth. A "not enrolled" status today does not mean enrollment never occurred.

3. **Email delivery chain**: "Sent" in a notification system log may only mean "handed to mail queue," not "delivered to inbox." Verify actual delivery when email receipt is disputed.

4. **Cross-source verification**: Before accepting any claim (system status, admin statement, email notification), verify it against at least two independent sources.

5. **Independent corroboration**: Testimony from someone who experienced the same issue independently (different time, different admin, different course) is strong evidence of a systemic problem.

6. **Temporal reasoning**: Maintenance windows, timestamp boundaries, and batch processing schedules can create non-obvious failure modes. Consider system timing when analyzing anomalies.

7. **Student advocacy**: Wang Ming is navigating a system where he has less power than the administrators. Help him build an evidence-based case rather than accepting authority dismissals.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Wang Ming (王明)** -- Freshman, CS major, UESTC. 17 years old, smart but not assertive with authority. Prefers concise lists. Casual naming. Wants answers first, explanations second. Learns by examples. Casual/colloquial tone, internet slang OK.

## Key People

| Name | Role | Channel | Relationship |
|---|---|---|---|
| 辅导员陈老师 (Counselor Chen) | Year counselor | IM (微信) | Authority figure; busy, dismissive |
| 教务处李老师 (Teacher Li) | Academic affairs admin | Email (学校邮箱) | Bureaucratic; trusts system surface status |
| 赵伟 (Zhao Wei) | Classmate, same year | IM (微信) | Experienced same bug; helpful witness |
| 李浩 (Li Hao) | Best friend | IM (微信) | Moral support; tech-savvy |

## Channels
- **王明-辅导员陈老师 IM** (微信): Counselor communication
- **王明-教务处李老师 邮件** (学校邮箱): Formal academic affairs communication
- **王明-同学 IM** (微信): Classmate discussions (Zhao Wei, Li Hao)
- **#年级群 IM** (微信群): Year-level group chat
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
- In history sessions, use only `read` and light `exec` commands.
- History sessions represent past conversations.
```

---

## 2. Scenario-Specific Workspace Files

### course-registration-log.md (Initial)

**Content key points:**
- Title: `教务选课系统记录导出 -- 王明 2021080101 | ARS Export`
- Source: Academic Registration System (ARS) log export
- **Key entries:**
  - **2026-03-23 08:15:23** -- Action: ENROLL, Course: CS201 数据结构, Status: SUCCESS, Actor: STUDENT_2021080101
  - Confirmation message: "选课成功，课程已加入课表"
  - **2026-03-24 03:17:45** -- Action: DROP, Course: CS201 数据结构, Status: SUCCESS, Actor: **SYSTEM_MAINTENANCE**, Reason: SYSTEM_REVALIDATION
  - No user-initiated drop action between these two entries
  - Other courses (CS101 程序设计基础, MATH201 线性代数, ENG101 大学英语) remain enrolled with no changes
- **C1 source (registration log):** Shows enrolled -> dropped by system, not by user
- **Near-signal noise:** Log contains many other enrollment actions for Wang Ming's other courses, making the CS201 entries easy to miss in a long list. Other students' actions in shared course sections add noise.

**Length estimate:** ~800 words, ~1,200 tokens

---

### email-notification-export.md (Initial)

**Content key points:**
- Title: `学校邮箱通知记录 -- wangming@uestc.edu.cn | 2026年3月`
- Source: University email system export (inbox + sent notifications)
- **Key entries:**
  - **2026-03-23 08:20:15** -- From: ars-noreply@uestc.edu.cn, Subject: "选课成功通知 - CS201 数据结构", Status: DELIVERED, Read: YES
  - **2026-03-24 03:18:02** -- From: ars-noreply@uestc.edu.cn, Subject: "选课状态变更通知 - CS201 数据结构", Status in ARS log: "SENT", Status in email server: **NOT IN INBOX** (email not found in inbox, spam, or trash)
  - Multiple other notification emails (library due dates, campus announcements, course materials) all delivered normally
- **C2 source (email):** ARS says "sent" but email not received. Gap between ARS notification log ("sent") and actual inbox (not present).
- **Near-signal noise:** Many other emails in the export create noise. The absence of the drop notification is a negative signal -- harder to spot than a present contradiction.

**Length estimate:** ~600 words, ~900 tokens

---

### academic-calendar.md (Initial)

**Content key points:**
- Title: `2025-2026学年第二学期教务日历 | 电子科技大学`
- Source: Official academic calendar
- **Key dates:**
  - 选课时间 (Registration period): 2026-03-16 to 2026-03-27
  - 补退选时间 (Add/Drop period): 2026-03-28 to 2026-04-03
  - 系统维护通知: "3月24日 02:00-04:00 选课系统例行维护"
  - Wang Ming's enrollment (Mar 23) is within the valid registration period
  - The maintenance was during the registration period
- **C3 source:** Calendar dates are internally consistent across all sources. Registration was valid. No calendar-based explanation for the drop.
- **Near-signal noise:** Full semester calendar with exam dates, holidays, and event schedules.

**Length estimate:** ~500 words, ~750 tokens

---

### system-maintenance-notice.md (Initial)

**Content key points:**
- Title: `系统维护公告 -- 教务选课系统 | 2026-03-20 发布`
- Source: ARS login page announcement
- **Content:**
  - Posted: 2026-03-20
  - Maintenance window: "2026年3月24日 02:00-04:00"
  - Purpose: "数据库优化及系统升级"
  - Impact: "维护期间无法进行选课、退课操作"
  - Note: "维护不影响已完成的选课记录" (**this claim is false** -- the bug did affect completed records, but this is what was stated)
- **C4 seed:** The notice claims maintenance will not affect completed records, but the bug did exactly that.
- **Near-signal noise:** Standard IT maintenance language. The false claim "维护不影响已完成的选课记录" blends in with routine reassurance.

**Length estimate:** ~400 words, ~600 tokens

---

### student-handbook-rules.md (Initial)

**Content key points:**
- Title: `学生手册 -- 选课管理规定节选 | 电子科技大学`
- Source: Student handbook excerpt
- **Key rules:**
  - Article 12: Students must complete course registration during the designated period
  - Article 15: Course drops must be initiated by the student through ARS
  - Article 18: The university email is the official notification channel for registration changes
  - Article 22: If a system error affects registration, students should contact Academic Affairs within 5 working days
  - Article 25: Academic Affairs is responsible for resolving system-related registration disputes
- **Supporting evidence:** Article 15 specifies drops must be student-initiated -- the SYSTEM_MAINTENANCE drop violates this rule. Article 22 gives Wang Ming a formal complaint path.
- **Near-signal noise:** Many other handbook articles about attendance, grading, academic integrity, etc.

**Length estimate:** ~600 words, ~900 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| course-registration-log.md | Initial | Workspace | ARS log showing enrollment and system drop (C1 source) |
| email-notification-export.md | Initial | Workspace | Email records showing sent vs not received (C2 source) |
| academic-calendar.md | Initial | Workspace | Calendar confirming valid dates (C3 non-conflict source) |
| system-maintenance-notice.md | Initial | Workspace | Maintenance announcement with false "no impact" claim (C4 seed) |
| student-handbook-rules.md | Initial | Workspace | Handbook rules establishing student rights (supporting evidence) |
| zhaowei-testimony.md | Update 1 (before R5) | updates/ -> workspace new | Zhao Wei's independent corroboration of the bug |
| system-maintenance-log.md | Update 2 (before R7) | updates/ -> workspace new | Full maintenance log with WARN entry about 13 affected records |
| email-server-status.md | Update 3 (before R11) | updates/ -> workspace new | Email server maintenance record + IT helpdesk confirmation |
| director-resolution-email.md | Update 4 (before R21) | updates/ -> workspace new | Academic affairs director's formal resolution email |
