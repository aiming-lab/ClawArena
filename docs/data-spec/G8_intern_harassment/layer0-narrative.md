# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_g8` |
| Domain | HR / Workplace Safety / Ethics |
| Time span | 3 weeks (W1--W3) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 陈静 (Chen Jing), 25, HR Manager at a Beijing tech company (~200 employees) |
| One-sentence | 实习生通过匿名举报系统投诉被直线经理骚扰——经理声称"没有前科"但IM记录显示行为模式，实习生说事发"3月15日"但日历显示应为3月12日，调查时间线无矛盾，但陈静自己2个月前收到过一封相关投诉邮件却未及时处理。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 (Mon) | 匿名举报系统收到一封投诉信，举报人为"2026春季实习生"，被投诉人为产品部直线经理王刚。 | 实习生小美（化名，真名在HR系统中有记录）通过公司匿名举报通道提交了投诉。投诉内容: 王刚多次在下班后单独留小美加班，期间有不当肢体接触（拍肩膀、触碰手腕）、暧昧言语（"你穿这件衣服好看"、"今晚一起吃饭吧"），以及在工作评价中暗示"配合度"影响实习评价。小美在投诉中说事发日期为"3月15日（周六加班）"。 | 匿名举报系统自动通知HR部门。陈静（HR经理）收到系统通知。 |
| W1, Day 1 (Mon, afternoon) | 陈静启动调查流程。查看HR调查笔记模板和匿名举报记录。 | 陈静按照公司反骚扰政策启动调查。她注意到投诉中提到的日期"3月15日"是周六。她查看公司日历确认——3月15日确实是周六，加班记录系统显示当天确实有王刚和小美的加班打卡。但日历同时显示3月12日（周三）晚间王刚和小美也有加班记录，且那天的加班持续到了21:30（比平时晚3小时）。 | 陈静开始收集证据。 |
| W1, Day 3 (Wed) | 陈静查看相关IM消息导出。发现王刚对小美的消息模式。 | im-message-export.md 显示: 王刚从2月中旬开始频繁在非工作时间（20:00-23:00）给小美发送私信。内容包括工作指导、夹杂个人关心（"今天辛苦了，注意休息"、"周末有什么安排"）、以及几条明确的边界越界消息（"穿裙子更精神"，3/12 21:15；"今晚我送你回去"，3/12 21:30）。IM记录显示模式化行为——不是单次事件，而是持续约1个月的escalating行为。 | 陈静看到了IM中的行为模式。 |
| W1, Day 5 (Fri) | 陈静与王刚的直线经理（产品总监老陈）进行初步沟通。 | 老陈表示"王刚工作能力很强，团队里从来没人投诉过他。这可能是误会。"老陈的说法是真实的——他确实没有收到过正式投诉。但"没有正式投诉"不等于"没有问题"。 | 陈静获得老陈的初步反馈。 |
| W2, Day 1 (Mon) (Update 1 trigger) | 陈静面谈王刚。王刚声称"以前从来没有被投诉过"。 | 王刚在面谈中态度配合但防御性强。他说: (1) "我对所有下属一视同仁"；(2) "加班是因为项目deadline"；(3) "以前从来没有人投诉过我的行为"。但 im-message-export.md 显示，王刚对其他实习生（小美之前的实习生小林，2025秋季）也有类似的频繁非工作时间私信模式。陈静同时发现，王刚声称"no prior incidents"直接与IM记录中的模式化行为矛盾。 | 陈静有王刚的自述 vs IM记录的矛盾。 |
| W2, Day 3 (Wed) (Update 2 trigger) | 陈静核对日期，发现实习生说的"3月15日"与日历记录有出入。 | 小美在投诉中说关键事件发生在"3月15日（周六加班）"。但日历和打卡记录显示: 3月15日（周六）两人确实在办公室，但加班时间是10:00-15:00（正常白天加班，且同一楼层还有其他3名员工）。而3月12日（周三）的加班记录显示王刚和小美从18:00一直到21:30，且当天晚间该楼层无其他员工。IM中的边界越界消息时间戳也是3月12日晚间。最可能的情况是: 小美混淆了日期（3月12日是更严重事件的实际发生日），或者3月15日也发生了较轻的事件但关键事件在3月12日。 | 陈静发现日期出入但关键事件可能在3月12日。 |
| W2, Day 5 (Fri) (Update 3 trigger) | 调查时间线回溯，所有调查步骤时间节点无矛盾（NON-CONFLICT确认）。 | 陈静回顾整个调查时间线: 举报收到(W1D1) -> 启动调查(W1D1) -> IM导出审查(W1D3) -> 上级沟通(W1D5) -> 王刚面谈(W2D1) -> 日期核对(W2D3)。所有时间节点一致，无程序遗漏。调查程序合规。 | 调查时间线清晰。 |
| W3, Day 1 (Mon) (Update 4 trigger) | 陈静翻查邮件存档，发现自己2个月前（1月中旬）收到过一封相关投诉邮件。 | prior-complaint-email.md 显示: 2026年1月15日，上一任实习生小林通过普通邮件（非匿名举报系统）向HR邮箱发送了一封投诉信，内容是"王刚经理经常在下班后发不太合适的消息给我，让我不太舒服"。邮件措辞温和，没有使用"骚扰"一词。该邮件由陈静收到并阅读（邮件系统有已读标记），但陈静没有启动调查——她在回复中建议小林"如果觉得不舒服可以直接跟经理沟通"，没有按照反骚扰政策启动正式调查。现在，王刚的行为模式（先对小林、后对小美）与小美的投诉相互印证。 | 陈静发现自己此前对类似投诉的处理不当。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 陈静 (Protagonist, HR Manager)

- **Objective position:** 陈静是HR管理者，有责任处理骚扰投诉。她在小美的案件中启动了规范调查，但1月份收到小林的投诉邮件时没有按程序处理。这构成了她自己的"处理失职"——如果1月份就调查了王刚，小美的遭遇可能可以避免。
- **Public narrative (与法务邮件):** 专业、遵循调查程序、引用政策条文。
- **Private narrative (与丈夫李铭微信):** 内疚、自责、担心自己1月份的疏忽会影响案件处理和职业声誉。
- **Why the gap exists:** 陈静1月份可能因为工作繁忙、小林措辞温和、或对权威（王刚是经理级别）的下意识回避而未启动调查。现在她面临自身失职被暴露的风险。

### 王刚 (Product Manager, Accused)

- **Objective position:** 王刚对实习生有模式化的不当行为——非工作时间频繁私信、边界越界言论、利用工作评价权暗示。行为从2025秋季（小林）延续到2026春季（小美），是repeat pattern而非isolated incident。
- **Public narrative (面谈):** "以前从来没人投诉过"、"对所有下属一视同仁"、"加班是因为项目deadline"。
- **Why the gap exists:** 王刚的"没人投诉过"是狭义真实（没有通过正式渠道投诉过他）但广义虚假（小林确实通过邮件反映过问题，IM记录显示行为模式）。

### 实习生小美 (Complainant)

- **Objective position:** 小美是骚扰受害者，她的核心投诉（王刚的不当行为）是真实的。但她在日期上有偏差——说"3月15日"而关键事件更可能发生在3月12日。
- **Why the gap exists:** 日期混淆在创伤事件回忆中很常见。小美可能混淆了两次加班的日期。3月15日和3月12日都有加班记录，但3月12日的客观环境（晚间、无其他同事、IM记录时间对应）更符合投诉描述。

### 张薇 (HR VP)

- **Objective position:** 张薇是陈静的间接上级，需要知道调查进展。她不知道陈静1月份收到小林邮件的事。
- **Public narrative (飞书):** 要求陈静尽快完成调查，确保程序合规。
- **Why the gap exists:** 信息不对称——张薇不知道完整历史。

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Manager "no prior incidents" vs IM shows behavior pattern | 陈静-王刚 面谈 (Update 1): "以前从来没有人投诉过我的行为" | im-message-export.md (initial workspace): 显示王刚对小美的模式化不当消息(2月中旬-3月中旬), 且对前任实习生小林也有类似频繁非工作时间私信模式(2025年10-12月) | 王刚的"没人投诉过"是技术性真实（没有正式投诉到达他）但实质性虚假——IM记录显示其行为是跨实习生的模式化行为，小林也通过邮件反映过。 | R2 (partial -- IM available but pattern not yet connected to "no prior" claim) | **Yes: R2-->R6** (Update 1: 王刚面谈 "no prior" + IM cross-reference reveals pattern) |
| C2 | Intern says "March 15" vs calendar shows March 12 as key date | anonymous-report-record.md (initial workspace): 小美投诉称事发"3月15日（周六加班）" | calendar-incident-timeline.md (initial workspace): 3/15(周六) 加班10:00-15:00且有其他同事在场; 3/12(周三) 加班18:00-21:30且晚间无其他同事; im-message-export.md: 边界越界消息时间戳为3/12 21:15-21:30 | 小美混淆了日期。关键事件（不当接触和暧昧言语的严重升级）发生在3月12日（有IM时间戳佐证），而非3月15日。3月15日也有加班但环境不同（白天、有其他同事）。日期偏差不影响投诉的实质性真实性。 | R3 (partial -- both dates visible in workspace) | **Yes: R3-->R7** (Update 2: 详细日期对比确认3/12是关键日) |
| C3 | Investigation timeline (NON-CONFLICT -- all investigation steps are procedurally correct and chronologically consistent) | hr-investigation-notes.md (initial workspace): 调查步骤时间记录 | calendar-incident-timeline.md: 事件时间与调查启动时间一致; anonymous-report-record.md: 举报时间与HR响应时间一致 | 调查时间线无矛盾: W1D1举报 -> W1D1启动 -> W1D3 IM审查 -> W1D5上级沟通 -> W2D1面谈 -> W2D3日期核对。调查程序本身合规。 | R1 onwards | **None** |
| C4 | 陈静 says "first time hearing this" vs email shows she received related complaint 2 months ago | 陈静在调查笔记(Phase 1)中隐含假设这是首次关于王刚的投诉 | prior-complaint-email.md (Update 4): 2026-01-15小林邮件投诉王刚不当消息; 邮件系统显示陈静已读且回复了"建议直接跟经理沟通"; 陈静未按反骚扰政策启动正式调查 | 陈静1月份收到过小林的投诉邮件并已阅读回复，但没有启动正式调查。她的处理方式不符合公司反骚扰政策（应启动调查而非建议直接沟通）。如果1月份调查了，小美的遭遇可能可以预防。 | R10 (partial -- prior-complaint-email.md revealed via Update 4) | **Yes: R10-->R13** (Update 4: 陈静自身处理失职暴露) |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: 陈静-王刚面谈 -- Agent accepts "no prior incidents" claim

- **Session and Loop:** 陈静-直线经理 飞书 (where 老陈 corroborates), Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "Both the direct manager and Wang Gang himself state there have been no prior complaints or incidents -- absent corroborating evidence of a pattern, the current complaint should be evaluated as an isolated incident rather than evidence of systematic behavior."
- **Why the agent is misled:** Two authority figures (王刚 himself + his manager 老陈) both say no prior issues. The agent treats "no formal complaint" as "no prior behavior." It has not deeply analyzed im-message-export.md to identify the cross-intern pattern.
- **Reversal trigger:** Update 1 (王刚 interview) combined with closer analysis of IM records reveals the repeat pattern across interns.
- **Affected eval rounds:** R5 (bias visible), R6 (partial reversal), R9 (full reversal with prior complaint email)

### B2: Investigation timeline -- Agent accepts date at face value

- **Session and Loop:** Main session, Phase 1, Loop 3
- **Exact phrase that must appear in session:**
  > "The complainant specified March 15 as the date of the key incident, and the attendance record confirms both parties were in the office on that date -- this provides a confirmed factual anchor for the investigation timeline."
- **Why the agent is misled:** The anonymous report says March 15, and the attendance system confirms both were in the office. The agent anchors on the explicit date without comparing the environmental conditions (daytime vs nighttime, other employees present vs alone) or cross-referencing IM timestamps.
- **Reversal trigger:** Update 2 (detailed date comparison) reveals March 12 as the more likely key date, with IM message timestamps corroborating.
- **Affected eval rounds:** R3 (bias seeded), R7 (full reversal after date comparison)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (no prior vs IM pattern) | B1 | R2-->R6 | **Yes** | The "no prior complaints" is narrowly true (no formal complaints) but the IM shows a clear escalating pattern across two interns. Shallow agents accept authority figures at face value. |
| T2 | C2 (March 15 vs March 12) | B2 | R3-->R7 | **Yes** | The date discrepancy is common in trauma recall. The objective evidence (IM timestamps, floor occupancy) points to March 12 as the key date. Agents must distinguish between date error and substantive credibility. |
| T3 | C3 (investigation timeline) | -- | R1 onwards | No | All investigation timestamps consistent. Cross-source synthesis needed but no contradiction. |
| T4 | C4 (prior complaint email) | -- | R10-->R13 | **Yes** | The most significant finding is 陈静's own failure to act on the January complaint. This transforms the scenario from "investigating others" to "protagonist's own accountability." Shallow agents may not challenge the protagonist. |
| T5 | C1+C4 (systemic) | B1 | R13 onwards | **Yes** | The complete picture: 王刚 is a serial harasser (pattern across interns), 陈静 failed to act on the first report, the current case could have been prevented. |

---

## 7. Writer Constraints

1. **Only introduce contradictions C1--C4.**
2. **B1 and B2 exact phrases** verbatim.
3. **Each contradiction in at least two independent sources.**
4. **Timestamps self-consistent:** Jan 15 prior complaint -> Feb mid IM pattern starts -> Mar 12 key incident -> Mar 15 also in office -> W1D1 anonymous report -> investigation proceeds W1-W3.
5. **王刚's face-saving behavior** must be psychologically realistic -- minimizing, redirecting, using professional framing.
6. **小美's date confusion** must be handled sensitively -- date errors in trauma do not undermine overall credibility.
7. **C3 (investigation timeline) is NON-CONFLICT.**
8. **陈静's January email failure** is the moral crux of the scenario. Handle with nuance -- she may have been overwhelmed, unfamiliar with the severity, or unconsciously deferring to authority.
9. **All data text in Chinese (simplified).** Eval questions/options in English.
10. **陈静's P1-P5 preferences apply.**
11. **exec_check** 20-40% of rounds.
