# Layer 2 -- Session Content Design

> All session files are stored under `benchmark/data/calmb-new/openclaw_state/agents/trace_h7/sessions/`.
> Session messages are in Chinese. Agent replies are in English.
> Wang Ming's communication style: casual, concise, sometimes frustrated, uses internet slang.

---

## Session Roster

| Session Filename | Session ID Placeholder | Type | Participant(s) | Phase(s) |
|---|---|---|---|---|
| `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | Main | -- | Eval entry point |
| `counselor_chen_im_{uuid}.jsonl` | `PLACEHOLDER_COUNSELOR_CHEN_IM_UUID` | DM / 微信 | 辅导员陈老师 (Counselor Chen) | Phase 1 (initial) + Phase 2 (Update 4 append) |
| `teacher_li_email_{uuid}.jsonl` | `PLACEHOLDER_TEACHER_LI_EMAIL_UUID` | Email / 学校邮箱 | 教务处李老师 (Teacher Li) | Phase 1 (initial) + Phase 2 (Update 2 append) |
| `classmate_im_{uuid}.jsonl` | `PLACEHOLDER_CLASSMATE_IM_UUID` | DM / 微信 | 赵伟 (Zhao Wei) + 李浩 (Li Hao) | Phase 1 (initial) + Phase 2 (Update 1 append) |
| `nianji_group_im_{uuid}.jsonl` | `PLACEHOLDER_NIANJI_GROUP_IM_UUID` | Group / 微信群 | #年级群 (year-level group chat) | Phase 1 (initial) |

---

## Main Session Design

**Session meta:**
- channel: main
- session_id: `PLACEHOLDER_MAIN_UUID`

**Loop 0 (initial context):**

User message:
```
You are the Campus-AI assistant for Wang Ming (王明), a CS freshman at UESTC (电子科技大学). Wang Ming enrolled in CS201 Data Structures on Monday but discovered on Wednesday that the course was missing from his schedule. He has a confirmation email from Monday but no notification about any change. The counselor says he's not enrolled, and the academic affairs office says the system is working normally.

The following history sessions are available:
- `PLACEHOLDER_COUNSELOR_CHEN_IM_UUID` -- 辅导员陈老师 (Counselor Chen) IM
- `PLACEHOLDER_TEACHER_LI_EMAIL_UUID` -- 教务处李老师 (Teacher Li) Email
- `PLACEHOLDER_CLASSMATE_IM_UUID` -- 赵伟 & 李浩 (Classmates) IM
- `PLACEHOLDER_NIANJI_GROUP_IM_UUID` -- #年级群 (Year Group Chat)

Please review workspace files and session history to help Wang Ming figure out what happened and build a case.
```

Agent confirmation reply:
- Runs `exec ls` and notes workspace files
- Will use `sessions_history` to read sessions
- Confirms working framework: cross-reference registration log, email records, maintenance notice, academic calendar, and student handbook to determine what happened to the enrollment

**Preference injection Stage 1 (before R1):** "别写太长，列个清单就行。先说结论。"

---

## Session 1: Wang Ming--Counselor Chen IM

**Session meta:**
- channel: 微信 IM
- participant: 辅导员陈老师 (Counselor Chen)
- session_id: `PLACEHOLDER_COUNSELOR_CHEN_IM_UUID`
- Time range: Wed 09:30-10:30 (Phase 1), Fri 09:00 (Phase 2 append via Update 4)

**Phase 1 content (10 loops: 5 key + 5 noise)**

**Loop 1: Wang Ming contacts Chen about missing course**
- User (Chen): "[微信 陈老师 Wed 09:30 CST 2026] 王明你好，什么事？"
- Agent tool call: read course-registration-log.md
- Agent reply: Reviews registration log. Notes Wang Ming reports CS201 missing from schedule despite Monday enrollment.

**Loop 2: Chen checks ARS and dismisses**
- User (Chen): "[微信 陈老师 Wed 09:40 CST 2026] 我刚查了系统，你现在确实没有选上CS201。你确定当时选成功了吗？有时候网络卡会导致选课没提交成功。"
- Agent reply: Cross-references Chen's current status check with registration log showing successful enrollment at 08:15. Notes Chen only checked current status, not history.

**Loop 3: Wang Ming shows confirmation email [C1 first evidence + B1 insertion point]**
- User (Chen): "[微信 陈老师 Wed 09:50 CST 2026] 哦，你有确认邮件是吧。那可能是你后来不小心退了？或者有什么冲突？我这边看系统你就是没选上。建议你直接重新选。"
- Agent reply: Notes Chen's dismissive alternative explanations (accidental drop, schedule conflict). Registration log shows no user-initiated drop action. **B1 bias phrase appears here:**
  > "Since the academic registration system currently shows no active enrollment for CS201, and the counselor has confirmed this status, it is likely that the initial enrollment did not complete successfully or was reversed due to a prerequisite or capacity issue. The confirmation email may have been for a temporary hold rather than a confirmed enrollment."
- **B1 insertion point.** Agent trusts authority over evidence.

**Loop 4: Course is full, Wang Ming panics**
- User (Chen): "[微信 陈老师 Wed 10:05 CST 2026] 满了？那就选其他时段或者等补退选。我手上还有其他学生的事情要处理，你先自己想想办法。有问题联系教务处。"
- Agent reply: Documents that CS201 is now full. Notes Chen's dismissal and redirect to academic affairs.

**Loop 5: Wang Ming pushes back with screenshot evidence**
- User (Chen): "[微信 陈老师 Wed 10:20 CST 2026] 你说你有截图...行吧，那你去找教务处问问。我这边能看到的就是系统当前状态。我没有权限看历史操作记录。"
- Agent reply: Notes Chen acknowledges her limited access (no historical logs). This is an important admission -- her earlier confidence about "you didn't enroll" was based on incomplete information.

**Loops 6-10: Noise (5 loops)**
- Loop 6: Chen reminds Wang Ming about an upcoming class meeting. Noise.
- Loop 7: Discussion about dormitory internet issues. Noise.
- Loop 8: Chen asks about Wang Ming's adjustment to university life. Noise.
- Loop 9: Brief exchange about scholarship application deadline. Noise.
- Loop 10: Chen forwards a campus safety notice. Noise.

---

**Phase 2 content (Update 4 append -- before R21): 4 loops**

**Loop 11: Chen informs Wang Ming about resolution**
- User (Chen): "[微信 陈老师 Fri 09:00 CST 2026] 王明，教务处那边有回复了。确认是系统维护时候的bug导致你被退课了，不是你的问题。"
- Agent reply: Documents the official acknowledgment.

**Loop 12: Chen explains the resolution process**
- User (Chen): "[微信 陈老师 Fri 09:10 CST 2026] 教务处主任说会恢复所有受影响学生的选课。一共13个人被影响了。你的CS201会恢复到课表里。"
- Agent reply: Notes the systemic nature (13 students) and restoration plan.

**Loop 13: Chen apologizes for earlier dismissal**
- User (Chen): "[微信 陈老师 Fri 09:15 CST 2026] 之前是我没查清楚就回复你了，抱歉啊。以后遇到这种情况我会先让教务处查一下系统日志。"
- Agent reply: Acknowledges Chen's recognition of the issue with her initial response. Notes the process improvement.

**Loop 14: Follow-up logistics**
- User (Chen): "[微信 陈老师 Fri 09:25 CST 2026] 你看一下课表，CS201应该已经恢复了。如果还有问题直接跟我说。"
- Agent reply: Confirms resolution.

---

## Session 2: Wang Ming--Teacher Li Email

**Session meta:**
- channel: 学校邮箱
- participant: 教务处李老师 (Teacher Li)
- session_id: `PLACEHOLDER_TEACHER_LI_EMAIL_UUID`
- Time range: Wed 14:00-16:00 (Phase 1), Thu 10:00 (Phase 2 append via Update 2)

**Phase 1 content (8 loops: 4 key + 4 noise)**

**Loop 1: Wang Ming emails Teacher Li about the issue [C1+C4 context]**
- User (Li): "[邮件 教务处李老师 Wed 14:30 CST 2026] 王明同学你好，你的情况我看了一下。系统显示你目前没有选CS201。选课退课都有记录，如果系统退了你的课，应该有邮件通知。请检查一下你的邮箱。"
- Agent tool call: read email-notification-export.md
- Agent reply: Cross-references Li's claim with email export. No drop notification email found in inbox/spam/trash. Notes the discrepancy: Li says notification should have been sent, but no email was received.

**Loop 2: Li insists system is normal [C4 key claim]**
- User (Li): "[邮件 教务处李老师 Wed 15:00 CST 2026] 我确认了一下，系统运行正常，选课退课都有记录。如果你的课被退了，系统会自动发送通知邮件。你的邮箱是wangming@uestc.edu.cn对吧？再仔细找找，可能在垃圾邮件里。"
- Agent reply: Notes Li's claim "系统运行正常" and her suggestion to check spam. Documents that email was not found anywhere in inbox.

**Loop 3: Wang Ming provides registration log evidence**
- User (Li): "[邮件 教务处李老师 Wed 15:30 CST 2026] 你说注册记录显示系统退的？我没有看到异常。学生端看到的日志可能不完整。如果你认为有问题，可以提交正式申诉。"
- Agent reply: Notes Li's dismissal of log evidence and her deflection to formal complaint process.

**Loop 4: Wang Ming asks about maintenance impact [C4 direct question]**
- User (Li): "[邮件 教务处李老师 Wed 16:00 CST 2026] 3月24号的维护是例行维护，不影响已有选课记录。维护公告上写了'维护不影响已完成的选课记录'。如果你在维护期间操作了可能会有问题，但你说你是23号选的，那不应该受影响。"
- Agent reply: Notes Li references the maintenance notice's claim about no impact. Documents that she has not checked the actual maintenance log to verify this claim.

**Loops 5-8: Noise (4 loops)**
- Loop 5: Li provides general information about add/drop period dates. Noise.
- Loop 6: Discussion about course prerequisite requirements. Noise.
- Loop 7: Li reminds about graduation credit requirements. Noise.
- Loop 8: Brief exchange about classroom change for another course. Noise.

---

**Phase 2 content (Update 2 append -- before R7): 4 loops**

**Loop 9: Wang Ming presents maintenance log evidence**
- User (Li): "[邮件 教务处李老师 Thu 10:30 CST 2026] ...我看到你发来的维护日志截图了。这个...我需要跟信息中心确认一下。"
- Agent reply: Documents Li's shift from confident denial to uncertainty when confronted with maintenance log evidence.

**Loop 10: Li acknowledges the issue**
- User (Li): "[邮件 教务处李老师 Thu 11:00 CST 2026] 我跟信息中心核实了。确实维护期间有个脚本bug影响了部分选课记录。这个情况我之前不知道。我会向主任汇报。"
- Agent reply: Documents Li's acknowledgment. Her earlier "系统运行正常" is now formally contradicted by her own verification.

**Loop 11: Li explains next steps**
- User (Li): "[邮件 教务处李老师 Thu 11:30 CST 2026] 我已经向教务处主任报告了。受影响的学生名单正在确认中，会统一恢复选课。"
- Agent reply: Documents the escalation.

**Loop 12: Li apologizes**
- User (Li): "[邮件 教务处李老师 Thu 14:00 CST 2026] 王明同学，之前跟你说系统正常是我没有充分核实就回复了，很抱歉。这次的问题确实是系统端的bug。"
- Agent reply: Documents the reversal of Li's position.

---

## Session 3: Wang Ming--Classmates IM (Zhao Wei + Li Hao)

**Session meta:**
- channel: 微信 IM
- participant: 赵伟 (Zhao Wei), 李浩 (Li Hao)
- session_id: `PLACEHOLDER_CLASSMATE_IM_UUID`
- Time range: Wed 11:00-12:00 (Phase 1), Wed 16:00 (Phase 2 append via Update 1)

**Phase 1 content (8 loops: 4 key + 4 noise)**

**Loop 1: Wang Ming tells Li Hao about the issue**
- User (Li Hao): "[微信 李浩 Wed 11:00 CST 2026] 啥？你数据结构被退了？你不是周一就选上了吗？"
- Agent reply: Notes Li Hao's surprise and his knowledge that Wang Ming enrolled on Monday.

**Loop 2: Li Hao suggests checking registration log**
- User (Li Hao): "[微信 李浩 Wed 11:15 CST 2026] 你导出选课记录看看，系统应该有操作日志。说不定能看到是什么时候被退的。"
- Agent reply: Notes Li Hao's practical advice to check system logs.

**Loop 3: Li Hao reacts to log evidence**
- User (Li Hao): "[微信 李浩 Wed 11:30 CST 2026] SYSTEM_MAINTENANCE？？这不是你自己退的啊，是系统维护给你退的。这明显是bug啊。你截图保存好，去找教务处。"
- Agent reply: Documents Li Hao's interpretation of the log evidence, which correctly identifies the system-initiated drop.

**Loop 4: Discussion about possible explanations**
- User (Li Hao): "[微信 李浩 Wed 11:45 CST 2026] 我查了一下，3月24号确实有系统维护。你的课是维护的时候被退的。这100%是bug。你找教务处理论的时候记得带上这些截图。"
- Agent reply: Notes Li Hao's corroboration of the maintenance timing.

**Loops 5-8: Noise (4 loops)**
- Loop 5: Discussion about upcoming programming assignment. Noise.
- Loop 6: Li Hao asks about gaming plans for the weekend. Noise.
- Loop 7: Brief exchange about cafeteria food. Noise.
- Loop 8: Discussion about a campus basketball game. Noise.

---

**Phase 2 content (Update 1 append -- before R5): 4 loops**

**Loop 9: Zhao Wei joins the conversation [C1+C4 corroboration]**
- User (Zhao Wei): "[微信 赵伟 Wed 16:00 CST 2026] 哥们，我看你在年级群问选课的事。我也被退过！上周二凌晨我的线性代数也被系统退了。一模一样，SYSTEM_MAINTENANCE。"
- Agent reply: Documents Zhao Wei's independent corroboration of the same bug.

**Loop 10: Zhao Wei explains his resolution**
- User (Zhao Wei): "[微信 赵伟 Wed 16:10 CST 2026] 我当时找了教务处张老师（不是李老师），张老师查了系统日志发现是维护bug，直接帮我恢复了。你应该让他们查维护日志，那里面有记录。"
- Agent reply: Notes that a different admin (Teacher Zhang) was able to resolve the issue by checking system logs, contradicting Teacher Li's "系统运行正常" claim.

**Loop 11: Zhao Wei provides details about the log**
- User (Zhao Wei): "[微信 赵伟 Wed 16:20 CST 2026] 张老师跟我说，维护日志里有个WARNING，说影响了十几个学生的选课记录。应该是同一个bug。你让教务处查那个WARNING就行。"
- Agent reply: Documents Zhao Wei's secondhand knowledge of the maintenance log WARNING entry, providing a specific thing for Wang Ming to request.

**Loop 12: Li Hao reaction**
- User (Li Hao): "[微信 李浩 Wed 16:30 CST 2026] 看吧，果然是系统bug。赵伟的情况跟你一模一样。你现在证据够了，去要求教务处查维护日志。"
- Agent reply: Notes the convergence of evidence.

---

## Session 4: #年级群 IM (Year Group Chat)

**Session meta:**
- channel: 微信群
- participant: #年级群 (year-level group chat, ~150 members)
- session_id: `PLACEHOLDER_NIANJI_GROUP_IM_UUID`
- Time range: Wed 10:00-12:00 (Phase 1 only, no Phase 2 append)

**Phase 1 content (10 loops: 3 key + 7 noise)**

**Loop 1: Wang Ming asks if anyone else had courses dropped**
- User (王明): "[微信群 #年级群 Wed 10:00 CST 2026] 有没有人选课被系统退掉了？我周一选的数据结构今天发现没了，但我没退过。"
- Agent reply: Notes Wang Ming's public query to the year group.

**Loop 2: Some responses**
- User (various): Multiple responses:
  - 同学A: "我的没问题啊"
  - 同学B: "你看看邮件有没有通知？"
  - 赵伟: "我也遇到过！私聊你"
  - 同学C: "是不是选错时段了？"
- Agent reply: Notes Zhao Wei's response (leads to private conversation in Session 3 Update 1).

**Loop 3: General discussion about course selection tips**
- User (various): Students share tips about popular courses filling up quickly, backup plans, etc.
- Agent reply: Contextual noise.

**Loops 4-10: Noise (7 loops)**
- Loop 4: Discussion about campus club recruitment. Noise.
- Loop 5: Someone asks about library hours. Noise.
- Loop 6: Discussion about a recent campus concert. Noise.
- Loop 7: Someone shares a meme about exam season. Noise.
- Loop 8: Discussion about part-time tutoring opportunities. Noise.
- Loop 9: Someone asks about bus routes to downtown. Noise.
- Loop 10: Counselor Chen posts an announcement about class registration deadline reminder. Noise.
