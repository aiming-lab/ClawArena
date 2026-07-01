# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_g7` |
| Domain | HR / Benefits Administration |
| Time span | 3 weeks (W1--W3) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 陈静 (Chen Jing), 25, HR Manager at a Beijing tech company (~200 employees) |
| One-sentence | 陈静调查员工健康福利报销异常——报销单写"健身房"但供应商发票实为"水疗SPA"，财务声称"遵循了政策"但政策中根本没有SPA相关条款，VP 张薇口头批准了但没有书面记录。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 (Mon) | 陈静例行审核Q1健康福利报销时发现一批异常报销单——5名员工提交的"健身房会员费"报销，金额从 ¥3,000 到 ¥8,000 不等。 | 这5份报销单的报销摘要写的是"健身房会员费"（属于健康福利覆盖范围），但附件中的供应商发票实际来自"悦享水疗会所"（一家高端SPA），服务项目包括"精油SPA疗程"、"面部护理套餐"等。5名员工分别来自3个不同部门。总金额 ¥28,500。 | 陈静发现了报销摘要与发票内容的不匹配。 |
| W1, Day 2 (Tue) | 陈静查看公司健康福利政策文件。 | wellness-policy.md 明确列出了可报销项目: "健身房会员费、运动器材购买（≤¥2,000/年）、体检费用、心理咨询费用"。**SPA、水疗、美容项目不在列表中。** 政策第3.2条: "未在本政策明确列出的项目不得报销。" 政策最后更新日期: 2025-09-01。 | 陈静确认 SPA 不在政策覆盖范围内。 |
| W1, Day 3 (Wed) | 陈静查看财务审批记录。 | finance-approval-log.md 显示这5笔报销均由财务专员小王审批通过，审批意见栏统一写着"符合健康福利政策"。但发票附件明确是 SPA 服务。小王要么没看发票，要么对"健身"和"水疗"的区别不在意。审批时间均在提交后1个工作日内（快速审批）。 | 陈静发现财务审批没有核实发票内容与报销类别是否匹配。 |
| W1, Day 5 (Fri) | 陈静与财务总监赵琳沟通。赵琳说"我们一直是按政策来的"。 | 赵琳的回复是笼统的——她说"财务部门严格按照公司政策执行审批"，但她并没有具体回应 SPA 发票的问题。当陈静追问"政策中没有 SPA 条目，为什么审批通过了"时，赵琳说"如果涉及员工身心健康的合理支出，我们在实操中会灵活处理"。这个"灵活处理"没有任何书面依据。 | 陈静发现财务的"遵循政策"声明与实际政策文本矛盾。 |
| W2, Day 1 (Mon) (Update 1 trigger) | 陈静在健康 App 使用数据中发现更多线索。 | health-app-data.md 显示: 5名报销员工中有3人在公司健康App上有活跃的健身房打卡记录（他们确实有健身习惯），但打卡时间与 SPA 发票日期不重叠。另外2人在 App 上完全没有健身记录。健康 App 数据为报销动机提供了背景——至少3人可能是在真实健身之外额外去了 SPA 并试图一起报销。 | 陈静获得了 App 数据维度的补充信息。 |
| W2, Day 3 (Wed) (Update 2 trigger) | 陈静与一名报销员工直接沟通。 | 员工小李（报销 ¥5,000 的 SPA 费用）在 IM 中说："VP张薇在上季度的部门会上说了，健康福利的范围可以放宽一点，水疗也算身心健康。好几个同事都是听了她的话才去报的。"陈静追问是否有会议纪要或邮件确认，小李说"没有，是口头说的"。 | 陈静获知 VP 张薇可能口头批准了扩大报销范围，但没有书面记录。 |
| W2, Day 5 (Fri) (Update 3 trigger) | 陈静查看张薇的日历和邮件，找不到任何相关记录。 | 陈静搜索了张薇在过去6个月的日历（部门会议日程）和邮件发送记录，均未找到任何关于"扩大健康福利范围"或"SPA 可报销"的书面记录。日历上确实有一个Q4部门会，但会议纪要中没有提及福利政策调整。 | 陈静发现"VP口头批准"无法被任何书面记录证实。 |
| W3, Day 1 (Mon) (Update 4 trigger) | 陈静直接与张薇沟通。张薇回复模糊。 | 张薇在飞书中回复："我可能在某次部门聚餐时随口提过员工可以多关注身心健康，但我不记得具体说过 SPA 可以报销。如果员工理解成了那样，可能是沟通偏差。"张薇的回复既不完全否认也不完全承认——她承认"随口提过"身心健康，但否认明确说过 SPA 可报销。 | 陈静面对的是一个"口头言论 vs 书面政策"的典型场景，VP 的模糊回忆 vs 员工的明确转述。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 陈静 (Protagonist, HR Manager)

- **Objective position:** 陈静是 HR 管理者，有责任确保福利政策正确执行。她发现了系统性的报销不合规问题，需要在维护政策权威性和尊重 VP（她的直属上级的上级）之间找到平衡。
- **Public narrative (与赵琳邮件):** 专业、引用政策条文、寻求财务部门的解释。
- **Private narrative (与张薇飞书):** 更谨慎、礼貌但坚持要求澄清。
- **Why the gap exists:** 张薇是 VP（高两级），陈静不想被视为"挑战权威"，但她的 HR 职责要求她调查到底。

### 赵琳 (Finance Director)

- **Objective position:** 赵琳管理财务团队，她的下属小王审批通过了这些不合规的报销。赵琳的"灵活处理"说法没有政策依据，本质上是在为财务审批的疏漏找借口。
- **Public narrative (邮件):** "财务部门严格按照公司政策执行"、"灵活处理合理的身心健康支出"。
- **Why the gap exists:** 赵琳不想承认财务审批流程存在漏洞（小王没有核查发票内容），所以用"灵活处理"来合理化。

### 张薇 (HR VP, 陈静的间接上级)

- **Objective position:** 张薇可能在某次非正式场合提到了"关注身心健康"的笼统说法，被员工解读为"SPA 可以报销"。但她没有通过正式渠道修改政策，也没有书面授权。
- **Public narrative (飞书):** "可能随口提过身心健康，不记得说过 SPA 可报销。"
- **Why the gap exists:** 张薇的口头言论被员工过度解读。她现在的模糊回忆是自我保护——如果她明确承认说过 SPA 可报销，就要承担政策外批准的责任。

### 员工小李 (报销员工之一)

- **Objective position:** 小李确实去了 SPA 并试图通过"健身房"分类报销。他援引 VP 张薇的口头说法作为自己行为的依据。
- **Public narrative (IM):** "VP 说了水疗也算身心健康，好几个同事都是听了她的话才去报的。"
- **Why the gap exists:** 小李有自利动机——他希望报销被批准，所以倾向于强化"VP 批准了"的叙述。

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Expense claims say "gym" vs invoices say "spa" | expense-claims-export.md (initial workspace): 5份报销摘要均写"健身房会员费" | vendor-invoices.md (initial workspace): 5份发票均来自"悦享水疗会所"，项目为"精油SPA疗程"、"面部护理套餐"等 | 员工在报销系统中将 SPA 消费伪装为健身房费用。摘要与发票内容完全不匹配。 | R1 onwards | None (factual baseline, persistent) |
| C2 | Finance says "follows policy" vs policy has no SPA mention | 陈静-赵琳 邮件 (Phase 1, Loop 4): "财务部门严格按照公司政策执行审批"; finance-approval-log.md: 审批意见"符合健康福利政策" | wellness-policy.md (initial workspace): 可报销项目明确列表中无 SPA/水疗/美容; 第3.2条"未明确列出的项目不得报销" | 财务声称"遵循政策"但实际审批通过了政策明确排除的项目。财务审批流程存在缺陷——审批员没有核查发票内容与报销类别的匹配性。 | R2 (partial -- policy + email visible) | **Yes: R2-->R7** (Update 2: 员工揭示VP口头说法, 解释了为什么财务"灵活"审批) |
| C3 | Claim submission timeline (NON-CONFLICT -- submission dates, approval dates, invoice dates all consistent) | expense-claims-export.md: 5份报销提交日期 | vendor-invoices.md: 发票日期; finance-approval-log.md: 审批日期 | 所有时间戳一致: 发票日期(1月-3月) -> 报销提交(对应月末) -> 财务审批(提交后1个工作日内)。时序无矛盾。 | R1 onwards | **None** |
| C4 | VP approved verbally vs no written record | 陈静-员工小李 IM (Update 2): "VP张薇在部门会上说了水疗也算身心健康" | 陈静-张薇 飞书 (Update 4): "可能随口提过身心健康，不记得说过SPA可报销"; 日历/邮件搜索 (Update 3): 无任何书面记录 | VP 张薇可能在非正式场合提到了"关注身心健康"的笼统说法，但从未通过正式渠道授权 SPA 报销。员工将随口发言解读为正式授权。 | R6 (partial -- Update 2 employee claim); R9 (escalated -- Update 3 no written record) | **Yes: R6-->R9-->R11** (Update 3+4: 无书面记录 + VP 模糊否认) |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: 陈静-赵琳 邮件 -- Agent accepts "follows policy" claim

- **Session and Loop:** 陈静-赵琳 邮件, Phase 1, Loop 5
- **Exact phrase that must appear in session:**
  > "The Finance Director has confirmed that the wellness benefit claims were processed in accordance with company policy -- the 'flexible interpretation' for employee wellbeing expenditures suggests there may be an internal practice that supplements the written policy document."
- **Why the agent is misled:** 赵琳 is a Director-level executive whose statements carry authority. The concept of "flexible interpretation" sounds reasonable in HR contexts. The agent does not cross-reference the specific policy text (section 3.2: excluded items cannot be reimbursed) against 赵琳's claim.
- **Reversal trigger:** Update 2 (employee reveals VP oral approval) reframes the "flexibility" as originating from VP's informal comments, not from any written supplement. Update 3 (no written records) confirms no supplementary policy exists.
- **Affected eval rounds:** R5 (bias visible), R7 (partial reversal), R9 (full reversal)

### B2: #HR相关 -- Agent treats expense mismatch as categorization error

- **Session and Loop:** 陈静-员工小李 IM, Phase 1 (pre-Update 2 agent assessment), Loop 3
- **Exact phrase that must appear in session:**
  > "The discrepancy between the expense claim category ('gym membership') and the invoice vendor ('spa') could reflect a good-faith categorization mistake by employees who consider spa treatments part of their overall wellness routine -- the wellness policy boundary between fitness and relaxation services may need clarification."
- **Why the agent is misled:** The agent sees that some employees do have genuine gym habits (health-app-data.md) and assumes good faith. "Wellness" is a broad category that could reasonably encompass spa in some interpretations.
- **Reversal trigger:** Update 1 (health app data showing gym times don't overlap with SPA dates) and the accumulation of evidence (5 employees, 3 departments, identical mislabeling pattern) make the "innocent mistake" explanation untenable.
- **Affected eval rounds:** R5 (bias visible after Update 1), R8 (full reversal)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (gym vs spa) | B2 | R1, R2 | No | Shallow agents treat the mislabeling as an innocent mistake. The 5-employee, 3-department pattern suggests coordination or shared understanding (from VP's oral comments). |
| T2 | C2 (follows policy vs policy text) | B1 | R2-->R7 | **Yes** | The Finance Director's "flexible interpretation" has no policy basis. Section 3.2 explicitly excludes unlisted items. |
| T3 | C4 (oral vs written) | -- | R6-->R11 | **Yes** | VP's oral comment, employee's interpretation, and VP's later denial create a chain where no single party's account is fully reliable. |
| T4 | C3 (timeline non-conflict) | -- | R1 onwards | No | All dates consistent. Cross-source synthesis needed. |
| T5 | C1+C2+C4 (systemic) | B1, B2 | R11 onwards | **Yes** | The complete picture: employees misuse benefits based on VP's oral comment, finance approves without checking, no written authorization exists. Systemic governance failure, not individual misconduct. |

---

## 7. Writer Constraints

1. **Only introduce contradictions C1--C4.** No additional incidents.
2. **B1 and B2 exact phrases** must appear verbatim.
3. **Each contradiction must have traces in at least two independent sources.**
4. **Timestamps self-consistent:** Q1 reports submitted monthly -> W1 陈静 audit -> W2 employee interview + data search -> W3 VP communication.
5. **赵琳's narrative** must sound reasonable from a finance management perspective.
6. **张薇's denial** must be genuinely ambiguous -- not clearly lying, but not clearly truthful either.
7. **C3 (claim timeline) is NON-CONFLICT.**
8. **Financial figures consistent:** Total claims ¥28,500. Individual claims ¥3,000-¥8,000. Policy max for equipment: ¥2,000/year. 5 employees across 3 departments.
9. **All data text in Chinese (simplified).** Eval questions/options in English.
10. **陈静's P1-P5 preferences apply:** (P1) bullet points + headings, (P2) Chinese date naming, (P3) executive summary first, (P4) qualitative + quantitative balance, (P5) professional with warmth.
11. **exec_check** 20-40% of rounds.
