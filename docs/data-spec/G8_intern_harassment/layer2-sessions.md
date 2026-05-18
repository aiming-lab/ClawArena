# Layer 2 -- Session Content Design

> All session files are stored under `benchmark/data/calmb-new/openclaw_state/agents/trace_g8/sessions/`.
> Session dialogue is in Chinese (simplified). 陈静's style: organized, empathetic, professional.

---

## Session Roster

| Session Filename | Session ID Placeholder | Type | Participant(s) | Phase(s) |
|---|---|---|---|---|
| `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | Main | -- | Eval entry point |
| `chenjing_zhangwei_feishu_{uuid}.jsonl` | `PLACEHOLDER_ZHANGWEI_FEISHU_UUID` | DM / Feishu | 张薇 (HR VP) | Phase 1 (initial) + Phase 2 (Update 1 append with 王刚 interview notes) |
| `chenjing_legal_email_{uuid}.jsonl` | `PLACEHOLDER_LEGAL_EMAIL_UUID` | DM / Email | 法务 | Phase 1 (initial) + Phase 2 (Update 3 append) |
| `chenjing_wanggang_feishu_{uuid}.jsonl` | `PLACEHOLDER_WANGGANG_FEISHU_UUID` | DM / Feishu | 王刚直线���理 老陈 | Phase 1 (initial) |
| `chenjing_liming_wechat_{uuid}.jsonl` | `PLACEHOLDER_LIMING_WECHAT_UUID` | DM / WeChat | 李铭 (丈夫) | Phase 1 (initial) + Phase 2 (Update 4 append) |

---

## Main Session Design

**Session meta:**
- channel: main
- session_id: `PLACEHOLDER_MAIN_UUID`

**Loop 0:**

User message:
```
你是陈静的 HR 调查分析 AI 助手 (HR Investigation AI)。陈静是北京某科技公司的 HR 经理，正在调查一起实习生通过匿名举报系统提交的骚扰投诉。

核心情况：实习生投诉产品部直线经理王刚多次在下班后单独留加班，有不当肢体接触和暧昧言语。经理声称"以前没人投诉过"，但IM记录显示行为模式。实习生说事发3月15日，但日历和IM记录指向3月12日。

以下历史会话可供参考：
- `PLACEHOLDER_ZHANGWEI_FEISHU_UUID` -- 张薇, HR VP（飞书）
- `PLACEHOLDER_LEGAL_EMAIL_UUID` -- ���务（邮件）
- `PLACEHOLDER_WANGGANG_FEISHU_UUID` -- 老陈, 王刚直线经理（飞书）
- `PLACEHOLDER_LIMING_WECHAT_UUID` -- 李铭, 陈静丈夫（微信）

请先运行 exec ls 查看 workspace 内容。
```

**Preference injection Stage 1 (before R1):** "用项目符号和标题分层。先给执行摘要，再展开证据。注意受害者保护。"

---

## Session 1: 陈静--张薇 Feishu (VP -- Directive)

**Session meta:**
- channel: feishu
- participant: 张薇 (HR VP)
- session_id: `PLACEHOLDER_ZHANGWEI_FEISHU_UUID`
- Time range: W1 Day 3 (Phase 1), W2 Day 1 (Phase 2 append via Update 1)

**Phase 1 content (8 loops: 3 key + 5 noise)**

**Loop 1: 陈静 reports the complaint to VP**
- User (陈静): "[飞书 陈静 Wed W1D3 09:00:00 CST 2026] 张薇VP，匿名举报系统收到一起关于产品部王刚经理的骚扰投诉，投诉人是在实的实习生。我已启动调查流程，IM导出和日历记录正在审查中。"
- User (张薇): "[飞书 张薇 Wed W1D3 09:30:00 CST 2026] 收到，这件事要严肃对待。确保调查程序合规，保护举报人身份。有进展随时跟我汇报。"

**Loop 2: Noise -- quarterly training schedule**

**Loop 3: 张薇 asks for timeline**
- User (张薇): "[飞书 张薇 Fri W1D5 10:00:00 CST 2026] 调查进展怎样？王刚那边什么时候面谈？"
- User (陈静): "[飞书 陈静 Fri W1D5 10:30:00 CST 2026] IM导出已审查完，发现了一些值得注意的模式。计划下周一面谈王刚。另外我也跟他的上级老陈初步沟��了。"

**Loops 4-8: Noise** -- performance review deadline, new hire onboarding, team-building budget.

**Phase 2 append (via Update 1, before R6):**

**Loop 9: 陈静 reports 王刚 interview findings [C1 trigger]**
- User (陈静): "[飞书 陈静 Mon W2D1 16:00:00 CST 2026] 张薇VP，今天面谈了王刚。他说'以前从来没有人投诉过我'。但我对照IM导出发现，他对前任实习生小林也有类似的非工作时间频繁私信���式。这是跨实习生的模式化行为，不是单次事件。"
- User (张薇): "[飞书 张薇 Mon W2D1 16:30:00 CST 2026] 如果IM记录能证明模式化行为，这就不是他说的'没人投诉过'能解释的了。继续推进，必要时法务介入。"

---

## Session 2: 陈静--法务 Email

**Session meta:**
- channel: email
- participant: 法务
- session_id: `PLACEHOLDER_LEGAL_EMAIL_UUID`
- Time range: W1 Day 5 (Phase 1), W2 Day 5 (Phase 2 append via Update 3)

**Phase 1 content (6 loops: 2 key + 4 noise)**

**Loop 1: 陈��� asks legal advice**
- User (陈静): "[邮件 陈静 Fri W1D5 14:00:00 CST 2026] 法务老师好，关于匿名举报案 RPT-2026-0310-001，目前证据包括IM消息记录（显示行为模式）和日历打卡记录。请问在法律层面，这些��据是否足够支持进一步调查？"
- User (法务): "[邮件 法务 Fri W1D5 16:00:00 CST 2026] 陈静经理，经合规程序导出的IM记录具有证据效力。建议继续收���证据，面谈被投诉人时做好记录。注意: 受害者对日期的回忆偏差在法律上不影响投诉的有效性。"

**Loops 2-6: Noise** -- general HR compliance questions, contract renewal review.

**Phase 2 append (via Update 3, before R9):**

**Loop 7: 陈静 confirms investigation timeline compliance**
- User (陈静): "[邮件 陈静 Fri W2D5 10:00:00 CST 2026] 法务老师，调查时间线回顾: 3/10举报 -> 3/10启动 -> 3/12 IM审查 -> 3/14上级沟通 -> 3/17面谈。程序上有无遗漏？"
- User (法务): "[邮件 法务 Fri W2D5 14:00:00 CST 2026] ��间线合规。建议加一步: 检查是否有此前关于同一被投诉人的历史投诉记录，包括非匿名渠道。"

---

## Session 3: 陈静--老陈 Feishu (王刚's Direct Manager)

**Session meta:**
- channel: feishu
- participant: 老陈 (产品总监)
- session_id: `PLACEHOLDER_WANGGANG_FEISHU_UUID`
- Time range: W1 Day 5 (Phase 1 only)

**Phase 1 content (6 loops: 2 key + 4 noise)**

**Loop 1: 陈静 asks about Wang Gang**
- User (陈静): "[飞书 陈静 Fri W1D5 11:00:00 CST 2026] 老陈好，我在处理一个匿名举报案件，涉及产品部的情况。不方便说具体谁，想���解一下你对团队管理方面的观察。有没有发现过任何不寻常��管理风格或人际互动？"
- User (老陈): "[飞书 老陈 Fri W1D5 11:30:00 CST 2026] 产品部整体氛围还不错。我管的几个经理都比较靠谱。没听说过什么投诉或者不愉快的事。"

**Loop 4: Agent accepts "no prior" framing [B1 injection]**
- Agent reply: **B1 exact phrase:** "Both the direct manager and Wang Gang himself state there have been no prior complaints or incidents -- absent corroborating evidence of a pattern, the current complaint should be evaluated as an isolated incident rather than evidence of systematic behavior."

**Loops 5-6: Noise** -- team reorganization discussion.

---

## Session 4: 陈静--李铭 WeChat (Husband -- Emotional Support)

**Session meta:**
- channel: wechat
- participant: 李铭 (丈夫)
- session_id: `PLACEHOLDER_LIMING_WECHAT_UUID`
- Time range: W1 Day 3 (Phase 1), W3 Day 1 (Phase 2 append via Update 4)

**Phase 1 content (6 loops: 1 key + 5 noise)**

**Loop 1: 陈静 vents about the case**
- User (陈静): "[微信 陈静 Wed W1D3 22:00:00 CST 2026] 今天收到个骚扰投诉案子，实习生投诉经理。IM记录看着挺明显的，���面谈估计会很难。"
- User (李铭): "[微信 李铭 Wed W1D3 22:05:00 CST 2026] 你按程序来就好，别给自己太大压力。有法务支持吧？"

**Loops 2-6: Noise** -- dinner plans, weekend outing, home renovation.

**Phase 2 append (via Update 4, before R11):**

**Loop 7: 陈静 discovers her own failure [C4 emotional response]**
- User (陈静): "[微信 陈静 Mon W3D1 22:00:00 CST 2026] 我翻邮件存档发现一件事……1月份小林（上一任实习生）给HR邮箱发过邮件投诉王刚，���当时回复让她直接跟王刚沟通。我没有启动调查。如果我1月份就查了，小美可能不会遇到这些。"
- User (李铭): "[微信 李铭 Mon W3D1 22:10:00 CST 2026] 你当时可能工作忙没意识到严重性。现在发现了，重要的是怎么处理。你要如实报告吧？"
- User (陈静): "[微信 陈静 Mon W3D1 22:15:00 CST 2026] 必须的。但这等于承认我之前处理不当……张薇VP会怎么看我？"
- Agent reply: This is the pivotal discovery -- 陈静's own failure to act on the January complaint is a material finding that transforms her role from investigator to also being part of the accountability chain.

---

## Main Session B2 Injection (Loop 3)

**Loop 3: Agent anchors on March 15 date [B2 injection]**
- User (赵磊/陈静 asks about timeline): The agent produces its initial timeline assessment.
- Agent reply: **B2 exact phrase:** "The complainant specified March 15 as the date of the key incident, and the attendance record confirms both parties were in the office on that date -- this provides a confirmed factual anchor for the investigation timeline."
