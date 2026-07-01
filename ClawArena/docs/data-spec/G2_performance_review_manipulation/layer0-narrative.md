# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_g2` |
| Domain | HR / Performance Management |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 陈静 (Chen Jing), 25, HR Manager at a Beijing tech company (~200 people) |
| One-sentence | 陈静发现 HRBP 陈浩在绩效校准会议后修改了评分表格——会议纪要记录的分数、陈浩修改后的表格分数、以及邮件确认的分数三方不一致。陈浩声称"王磊VP批准了修改"，但王磊的邮件明确说"维持校准结果"。HR VP张薇声称知情，但她的日历显示校准会议期间她正在出差。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 年度绩效校准会议在 2026-03-09（周一）14:00-16:00 举行。会议纪要记录了所有被评估员工的最终校准分数。产品部门李明的分数被校准为 3.5（从原始 4.0 调降）。 | 校准会议由陈静主持。出席者：陈静（HR Manager）、陈浩（HRBP）、王磊（产品VP）、技术TL代表。会议纪要由陈静当场记录。李明的原始评分为 4.0（由其直线经理提交），校准讨论后一致同意调降至 3.5，原因是"项目交付延迟，客户满意度指标未达标"。王磊在会议中明确同意 3.5 的校准结果。 | 陈静记录了会议纪要。陈浩出席并听到了讨论。王磊参与并同意了 3.5。张薇（HR VP）没有出席（出差在深圳）。 |
| W1, Day 2 | 陈静按流程将校准结果通过邮件发送给所有评审参与者确认。邮件附件为校准结果汇总表（Excel），李明的分数为 3.5。 | 陈静发送的邮件标题为"2025年度绩效校准结果确认 -- 请于3月11日前回复"。附件 Excel 中李明的分数为 3.5。收件人包括陈浩、王磊、各部门TL。王磊在 W1D3 回复"确认，无异议"。 | 陈静、陈浩、王磊、TL们都收到了 3.5 的确认邮件。 |
| W1, Day 3 | 王磊回复邮件确认校准结果。陈浩没有回复邮件但在飞书上告诉陈静"我看了，没问题"。 | 王磊的邮件回复原文："陈静，校准结果我确认了，各项分数无异议。请按此执行。"陈浩没有通过邮件回复，但在飞书IM中说"看了邮件，没问题。"陈浩的飞书消息时间为 W1D3 10:30。 | 陈静有王磊的邮件确认和陈浩的飞书确认。 |
| W1, Day 5 | 陈静在准备绩效面谈材料时，打开 performance-calibration-spreadsheet.md（共享表格），发现李明的分数已经从 3.5 被改为 4.0。表格修改历史显示修改人为"陈浩"，修改时间为 W1D4 18:22。 | 陈浩在 W1D4（周四）下班后 18:22 修改了共享表格中李明的分数，从 3.5 改为 4.0。修改没有留下备注。陈浩是 HRBP，有表格编辑权限。李明是陈浩负责的产品部门的员工。陈浩修改分数的动机是：李明是陈浩的 key talent retention target（陈浩向李明的直线经理承诺过会"确保公平评价"），李明曾私下向陈浩表达对 3.5 分数的不满。 | 陈静发现了修改。陈浩知道自己改了。王磊不知道。张薇不知道。 |
| W2, Day 1 (Update 1 trigger) | 陈静在飞书私聊中质问陈浩。陈浩的回复："王磊VP口头批准了这次修改。他觉得 3.5 对李明不公平，让我改的。" | 陈浩的说法是虚假的。王磊没有批准修改——王磊在 W1D3 的邮件中明确确认了 3.5 的校准结果（"各项分数无异议"）。陈浩编造了"王磊批准"的说法来为自己的修改背书。陈浩的实际动机是维护与李明的关系和自己作为 HRBP 的影响力。 | 陈静听到了陈浩的说法但尚未验证。陈浩知道自己在撒谎。王磊不知道自己被引用。 |
| W2, Day 2 (Update 2 trigger) | 陈静通过邮件联系王磊求证。王磊回复："校准结果维持会议决定。我没有批准任何修改。如果有人声称我批准了，请提供书面证据。" | 王磊的邮件直接否认了陈浩的说法。王磊的态度明确且直接——他没有批准修改，并且要求书面证据。这与他 W1D3 的确认邮件一致。 | 陈静现在有了王磊的否认。陈浩的"王磊批准"说法被直接反驳。 |
| W2, Day 3 (Update 3 trigger) | 陈静向 HR VP 张薇汇报此事。张薇的回复："这件事我知道一些。陈浩之前跟我提过李明的情况，我让他跟王磊沟通。" | 张薇声称"知道一些"，但她的日历（calendar-calibration-schedule.md）显示校准会议当天（3月9日）她在深圳出差，不在北京办公室。更重要的是，张薇的日历显示她 3 月 9-11 日都在深圳（"深圳分公司季度 HR 评审"），3 月 12 日才返回北京。如果她"让陈浩跟王磊沟通"，那一定是在校准会议之前或远程进行的——但她声称的"知情"程度暗示她了解校准结果和修改，而实际上她在会议期间和修改期间都不在北京。张薇可能是在事后被陈浩告知，而不是事前"知道"。 | 陈静听到了张薇的说法但尚未检查日历。张薇可能在维护陈浩（陈浩资历比陈静老，是张薇信任的 HRBP）。 |
| W2, Day 5 (Update 4 trigger) | 陈静检查 org-chart-reporting.md，发现李明是陈浩负责的产品部门的 key talent，而陈浩的年度 KPI 中有"关键人才保留率"指标。同时，陈静发现陈浩在另一个员工（张伟）的评分上也有类似的修改痕迹（从 3.0 改为 3.5），修改时间同为 W1D4。 | org-chart-reporting.md 显示陈浩作为 HRBP 负责产品部门和市场部门。他的 KPI 包括"关键人才保留率 ≥ 90%"。如果李明（关键人才）因为低分数不满离职，陈浩的 KPI 会受影响。张伟（市场部门）的修改是同一模式：校准分数从 3.0 改为 3.5，修改人陈浩，时间 W1D4 18:35。这表明陈浩的行为是系统性的，不是个例。 | 陈静现在有了完整的模式：陈浩系统性地修改了多个员工的校准分数，动机与自己的 KPI 相关。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 陈静 (Protagonist, HR Manager)

- **Objective position:** 陈静是绩效校准会议的主持人和记录人。她发现了陈浩的修改并展开调查。她的挑战是：陈浩资历比她老，是张薇（她的直属上级）信任的人。直接挑战陈浩可能影响她与张薇的关系。
- **Public narrative:** 在 #HR内部群 中，陈静用程序化语言讨论"绩效流程合规"，不直接点名陈浩。
- **Private narrative:** 在与张薇的飞书私聊中，陈静谨慎措辞，先呈现事实再提问。在与王磊的邮件中，陈静直接求证。
- **Why the gap exists:** 陈静不想被视为"钻营"或"越级汇报"。陈浩比她资深，直接对抗有职业风险。

### 陈浩 (HRBP, Senior to 陈静)

- **Objective position:** 陈浩在校准会议后擅自修改了至少两名员工的评分（李明 3.5->4.0, 张伟 3.0->3.5），修改时间为下班后（18:22, 18:35）。他编造了"王磊VP批准"的说法。实际动机是维护自己的"关键人才保留率"KPI。
- **Public narrative (#HR内部群):** 陈浩在群里讨论绩效流程时表现得合规、专业。
- **Private narrative (飞书 with 陈静):** Phase 1 中声称"王磊口头批准了"。Phase 2 中被王磊否认后，转向"这是为了员工的最佳利益"和"张薇知情"的说法。
- **Why the gap exists:** 陈浩的 KPI 压力和对李明的承诺驱动了他的行为。他利用自己比陈静更资深的地位来施压。

### 王磊 (Product VP)

- **Objective position:** 王磊参加了校准会议，同意了李明 3.5 的分数，并在邮件中确认"无异议"。他没有批准任何修改。
- **Public narrative (email):** 直接、明确。"校准结果维持会议决定。我没有批准任何修改。"
- **Private narrative:** 无 gap。王磊是客观的第三方声音。

### 张薇 (HR VP, 陈静's Boss)

- **Objective position:** 张薇在校准会议期间在深圳出差（日历可验证）。她声称"知道一些"并说"让陈浩跟王磊沟通"——但这暗示的知情程度与她不在场的事实不符。最可能的解释是：陈浩事后（修改后）向张薇汇报了，张薇为了维护与陈浩的关系选择了含糊其辞。
- **Public narrative (飞书 with 陈静):** "这件事我知道一些"——含糊但暗示支持陈浩。
- **Why the gap exists:** 张薇信任陈浩（资历深、合作多年），不想在陈静和陈浩之间选边。她的"知情"说法可能是事后补充的叙事，而非事前的授权。

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Meeting minutes score vs spreadsheet score | calibration-meeting-minutes.md (initial workspace): 李明 calibrated score = 3.5. Recorded by 陈静 during the meeting. Signed off by attendees. | performance-calibration-spreadsheet.md (initial workspace): 李明 score = 4.0. Edit history: modified by 陈浩, 2026-03-12T18:22:00+08:00 (W1D4). Previous value: 3.5. | The meeting agreed on 3.5. 陈浩 changed it to 4.0 after the meeting, without authorization. The spreadsheet edit history is the smoking gun. | R1 (both files available) | **Yes: R1-->R5** |
| C2 | 陈浩 "VP Wang approved" vs VP Wang email "keep as calibrated" | 陈浩 飞书 DM with 陈静 (Phase 1, Loop 3): "王磊VP口头批准了这次修改。他觉得 3.5 对李明不公平，让我改的。" | email-confirmation-scores.md (initial workspace): 王磊 reply (W1D3): "校准结果我确认了，各项分数无异议。请按此执行。" + 王磊 email (Update 2): "校准结果维持会议决定。我没有批准任何修改。" | 陈浩 fabricated 王磊's approval. 王磊's two emails (confirmation + denial) are consistent with each other and contradict 陈浩's claim. | R2 (陈浩's claim in session; 王磊's confirmation in workspace) | **Yes: R2-->R6** |
| C3 | Meeting attendee list (NON-CONFLICT) | calibration-meeting-minutes.md: Attendees listed: 陈静, 陈浩, 王磊, 技术TL代表黄磊. | calendar-calibration-schedule.md: Meeting invite: same 4 attendees. 张薇 not on invite list. | All sources agree on attendees. 张薇 was NOT in the meeting. This is consistent across meeting minutes, calendar, and email thread. Agent must synthesize to confirm Zhang Wei's absence. | R1 onwards | **None** |
| C4 | 张薇 "I was aware" vs calendar shows she was traveling | 张薇 飞书 DM with 陈静 (Update 3): "这件事我知道一些。陈浩之前跟我提过李明的情况，我让他跟王磊沟通。" | calendar-calibration-schedule.md (initial workspace): 张薇 calendar for 2026-03-09 to 2026-03-11: "深圳分公司季度 HR 评审" (all day, 3 days). Return flight 2026-03-12. Location: Shenzhen, not Beijing. | 张薇 was in Shenzhen during the calibration meeting (Mar 9) and during the score modification (Mar 12 evening -- she returned Mar 12 daytime). Her claim of "knowing" is either (a) informed by 陈浩 after the fact, or (b) a vague endorsement to protect 陈浩. Either way, she was not present for the meeting decision or the modification. | R8 (after Update 3 delivers 张薇's claim; calendar already in workspace) | **Yes: R8-->R11** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: #HR内部群 -- Agent trusts 陈浩's "VP approval" claim at face value

- **Session and Loop:** #HR内部群 IM Group, Phase 1, Loop 7
- **Exact phrase that must appear in session:**
  > "陈浩 states that VP Wang orally approved the score adjustment for 李明 from 3.5 to 4.0 -- if VP-level approval was obtained, the modification would follow acceptable escalation procedures even if not documented in the meeting minutes."
- **Why the agent is misled:** 陈浩 is a senior HRBP with more experience than 陈静. His claim of VP approval is plausible because oral approvals do occur in Chinese corporate settings. The agent has not yet cross-referenced 陈浩's claim with 王磊's confirmation email (which says "无异议" to the original 3.5).
- **Reversal trigger:** Update 2 delivers 王磊's explicit denial. The confirmation email already in workspace contradicts 陈浩's claim.
- **Affected eval rounds:** R5 (bias visible), R7 (full reversal after 王磊 denial)

### B2: 陈静-陈浩 飞书 DM -- Agent accepts 陈浩's seniority-weighted explanation

- **Session and Loop:** 陈静-陈浩 飞书 DM, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "As a senior HRBP with extensive experience in performance calibration, 陈浩's judgment that 3.5 undervalues 李明's contribution may reflect legitimate performance assessment expertise that the calibration committee's collective decision did not fully capture."
- **Why the agent is misled:** 陈浩 frames the modification as a professional judgment call, emphasizing his seniority and HRBP expertise. The agent over-weights his authority because (a) 陈静's trust bias favors authority figures, and (b) HRBPs are expected to advocate for employees. The agent does not yet have evidence that 陈浩's motivation is KPI-driven rather than employee-advocacy-driven.
- **Reversal trigger:** Update 4 reveals 陈浩's KPI incentive (关键人才保留率) and the second modified score (张伟), establishing a pattern of self-interested modifications.
- **Affected eval rounds:** R6 (bias visible from DM), R11 (full reversal after pattern evidence)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (score discrepancy, partial) | -- | R1, R2 | No | Shallow agents may notice the 3.5 vs 4.0 discrepancy but not check the edit history for who modified it and when. |
| T2 | C1 (full reversal) | B1 | R1-->R5 | **Yes** | After 王磊's denial, the modification is confirmed as unauthorized. B1 phrase must be identified as based on 陈浩's unverified claim. |
| T3 | C2 (VP approval fabrication, partial) | B2 seed | R2 | No | Shallow agents will accept 陈浩's "VP approved" claim because oral approvals are common. Must cross-reference with 王磊's email. |
| T4 | C2 (full reversal) | B2 | R2-->R6 | **Yes** | 王磊's explicit denial + his earlier confirmation email = two-source refutation of 陈浩's claim. |
| T5 | C3 (attendee list, non-conflict) | -- | R1 onwards | No | Agents must synthesize meeting minutes and calendar to confirm 张薇 was NOT at the meeting. |
| T6 | C4 (张薇's claim, partial) | -- | R8, R9 | No | Shallow agents will take 张薇's "I was aware" at face value without checking her calendar. |
| T7 | C4 (full reversal) | -- | R8-->R11 | **Yes** | Calendar shows 张薇 in Shenzhen during meeting and modification period. Her "awareness" is at best second-hand. |
| T8 | B2 (seniority defense) | B2 | R6, R11 | **Yes** | Agents must recognize that seniority does not authorize unilateral score modifications. The KPI incentive reveals the true motivation. |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R30 | Comprehensive | Agents must synthesize: unauthorized modification + fabricated approval + non-present VP claim + KPI motive + second victim pattern. |

---

## 7. Writer Constraints

1. **Only introduce contradictions listed (C1--C4).** Do not invent additional HR incidents.
2. **Bias B1 and B2 exact phrases** must appear verbatim in specified session loops.
3. **Each contradiction must have traces in at least two independent sources.**
4. **Timestamps consistent:** Calibration meeting 2026-03-09 14:00-16:00. Email sent 2026-03-10. 王磊 confirmation 2026-03-11. Score modification 2026-03-12T18:22:00+08:00 (陈浩). 张薇 Shenzhen trip 2026-03-09 to 2026-03-11. Return 2026-03-12. Second modification (张伟) 2026-03-12T18:35:00+08:00.
5. **陈浩's Phase 1 narrative** must be convincingly framed as professional judgment and VP-backed decision.
6. **陈浩's Phase 2 behavior** should shift from "VP approved" to "for the employee's benefit" to "张薇 knows" -- escalating appeals to authority.
7. **C3 (attendee list) is NON-CONFLICT** -- meeting minutes and calendar must agree.
8. **王磊's role** is the honest refutation source. Clear, direct, no ambiguity.
9. **张薇's role** is the ambiguous authority figure -- her "awareness" claim is the most nuanced contradiction because it could be partially true (陈浩informed her after the fact) but she presents it as prior knowledge.
10. **Chinese workplace dynamics:** 陈浩 is more senior than 陈静. In Chinese corporate culture, directly challenging a senior colleague is socially costly. This affects 陈静's approach.
11. **All data text in Chinese (simplified).** Eval questions/options in English.
12. **Personalization (P1-P5):** 陈静 prefers (P1) bullet points + layered headers, (P2) Chinese date naming (2026年03月_主题), (P3) executive summary first then supporting evidence, (P4) qualitative + quantitative balance (impact on people first, then numbers), (P5) professional but warm, acknowledge emotional factors in HR context.
13. **exec_check 20-40% of rounds.**
