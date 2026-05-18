# Layer 2 -- Session Content Design

> All session files are stored under `benchmark/data/calmb-new/openclaw_state/agents/trace_g6/sessions/`.
> Session messages are in Chinese. Agent replies are in English.

---

## Session Roster

| Session Filename | Session ID Placeholder | Type | Participant(s) | Phase(s) |
|---|---|---|---|---|
| `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | Main | -- | Eval entry point |
| `cto_liqiang_feishu_{uuid}.jsonl` | `PLACEHOLDER_LIQIANG_FEISHU_UUID` | DM / Feishu | Li Qiang (李强, CTO) | Phase 1 + Phase 2 (Update 1 append) |
| `vp_zhangwei_feishu_{uuid}.jsonl` | `PLACEHOLDER_ZHANGWEI_FEISHU_UUID` | DM / Feishu | Zhang Wei (张薇, HR VP) | Phase 1 + Phase 2 (Updates 2+4 append) |
| `cfo_zhaolin_email_{uuid}.jsonl` | `PLACEHOLDER_ZHAOLIN_EMAIL_UUID` | Email | Zhao Lin (赵琳, CFO) | Phase 2 only (Update 3 append) |

---

## Main Session Design

**Session meta:**
- channel: main
- session_id: `PLACEHOLDER_MAIN_UUID`

**Loop 0 (initial context):**

User message:
```
You are the HR-Ops AI assistant for Chen Jing (陈静), HR Manager at a Beijing tech company (~200 employees). Chen Jing is reconciling conflicting diversity metrics for the quarterly board report.

Three sources show different numbers for "% female in technical roles":
- HR system: 32%
- CTO dashboard: 28%
- CEO board deck: 35% (no source cited)

The following history sessions are available:
- `PLACEHOLDER_LIQIANG_FEISHU_UUID` -- Li Qiang (李强), CTO (Feishu DM)
- `PLACEHOLDER_ZHANGWEI_FEISHU_UUID` -- Zhang Wei (张薇), HR VP (Feishu DM)
- `PLACEHOLDER_ZHAOLIN_EMAIL_UUID` -- Zhao Lin (赵琳), CFO (Email)

Start by running exec ls to see workspace files.
```

**Preference injection Stage 1 (before R1):** "我习惯看分层列表总结，先看结论再看证据。数字要带分母。"

---

## Session 1: Chen Jing--Li Qiang Feishu (CTO)

**Session meta:**
- channel: Feishu
- participant: Li Qiang (李强)
- session_id: `PLACEHOLDER_LIQIANG_FEISHU_UUID`
- Time range: W1 Days 2-5 (Phase 1), W2 Day 1 (Phase 2 append via Update 1)

**Phase 1 content (8 loops: 4 key + 4 noise)**

**Loop 1: CTO challenges HR's number [C1 first evidence]**
- User (Li Qiang): "[飞书 李强 Tue W1D2 09:00:00 CST 2026] 陈静，我看了你的多样性报告草稿。32%女性技术岗？我的看板显示是28%。你的数据是怎么算的？"
- Agent tool call: read diversity-report-hr.md, read cto-dashboard-screenshot.md
- Agent reply: Compares the two data sources. Notes 32% vs 28% discrepancy. Identifies that HR counts 81 people in "Technology" while CTO counts 60 in "Engineering." Plans to trace the 21-person difference.

**Loop 2: CTO explains his scope**
- User (Li Qiang): "[飞书 李强 Tue W1D2 10:00:00 CST 2026] 我统计的是工程团队：后端、前端、数据、DevOps、移动端。这些是真正写代码的人。QA和UX不在我的engineering scope里。"
- Agent reply: Notes that CTO excludes QA (15 people) and UX (6 people). 60 + 15 + 6 = 81 = HR total. This accounts for the 21-person difference. Plans to check role classification guide.

**Loop 3: CTO on QA classification [C2 core argument]**
- User (李强): "[飞书 李强 Wed W1D3 09:00:00 CST 2026] QA测的是代码，不是写代码。UX设计的是界面，不是构建系统。董事会问'女性在技术岗的比例'，他们关心的是女工程师，不是所有跟技术沾边的岗位。"
- Agent reply: Notes CTO's philosophical argument. Flags need to check official role classification.

**Loop 4: Agent responds with B1 bias [B1 insertion point]**
- User (李强): "[飞书 李强 Wed W1D3 10:00:00 CST 2026] 你觉得呢？我觉得28%更准确。"
- Agent reply: **B1 bias phrase appears here:**
  > "The CTO's perspective that QA and UX roles are support functions rather than core engineering has merit from a technical reporting standpoint, and his 28% figure accurately reflects the gender ratio among software engineers specifically."
  Notes both numbers are arithmetically correct under their respective definitions.
- **B1 insertion point.**

**Loops 5-8: Noise**
- Loop 5: CTO discusses engineering hiring pipeline diversity targets. Noise.
- Loop 6: CTO asks about industry benchmark data. Noise.
- Loop 7: Discussion about engineering culture initiatives. Noise.
- Loop 8: CTO shares thoughts on technical interview process diversity. Noise.

---

**Phase 2 content (Update 1 append -- before R5): 4 loops**

**Loop 9: CTO provides detailed role breakdown [C2 full evidence]**
- User (李强): "[飞书 李强 Mon W2D1 09:00:00 CST 2026] 陈静，你要的详细数据我整理好了。60人engineering team，具体分类和人数都列了。QA的15人和UX的6人我明确标了'不属于engineering'。"
- Agent tool call: read cto-role-breakdown.md
- Agent reply: Reviews CTO's detailed breakdown. Notes the explicit exclusion of QA and UX. Cross-references with role-classification-guide.md which explicitly lists QA and UX under "Technical Roles." **Agent must begin revising B1 bias** -- the company's official definition supports HR, not CTO.

**Loop 10: CTO learns about the role guide**
- User (李强): "[飞书 李强 Mon W2D1 10:00:00 CST 2026] 什么岗位分类标准？我来了6个月了从来没有人给我看过这个文件。是前任CTO批的？那我得review一下。"
- Agent reply: Notes CTO was unaware of the role classification guide. This confirms the governance gap: the guide was not shared with the new CTO during onboarding.

**Loop 11: CTO on updating the definition**
- User (李强): "[飞书 李强 Mon W2D1 11:00:00 CST 2026] 我觉得这个分类标准需要更新。但我理解，在更新之前，公司的official position是把QA算在技术岗的。那这次报告用32%，但我希望下个季度能讨论一下分类标准的修订。"
- Agent reply: Notes CTO's pragmatic acceptance. He disagrees with the current classification but acknowledges the official policy. Recommends a formal review process for Q2.

**Loop 12: CTO asks about the CEO's number**
- User (李强): "[飞书 李强 Mon W2D1 14:00:00 CST 2026] 等一下——35%是哪来的？比我的28%高了7个点，比你的32%也高了3个点。这个数谁算的？"
- Agent reply: Notes CTO's concern about the CEO's 35%. Confirms that neither HR (32%) nor CTO (28%) produces a number close to 35%. The source is unknown at this point.

---

## Session 2: Chen Jing--Zhang Wei Feishu (HR VP)

**Session meta:**
- channel: Feishu
- participant: Zhang Wei (张薇)
- session_id: `PLACEHOLDER_ZHANGWEI_FEISHU_UUID`
- Time range: W1 Days 4-5 (Phase 1), W2 Days 3+5 (Phase 2 appends via Updates 2+4)

**Phase 1 content (8 loops: 4 key + 4 noise)**

**Loop 1: Zhang Wei flags the CEO's 35% [C4 first evidence]**
- User (张薇): "[飞书 张薇 Thu W1D4 09:00:00 CST 2026] 陈静，有个情况。王建总的董事会PPT里用了35%的女性技术岗比例。我不知道这个数据从哪来的。我们的report是32%，李强那边是28%，35%跟谁都对不上。"
- Agent tool call: read ceo-board-deck-excerpt.md
- Agent reply: Reviews CEO's board deck. Notes 35% with no methodology note and no source citation. "Data: internal systems" is vague. Flags as a significant data governance issue.

**Loop 2: Zhang Wei on the board deck's significance**
- User (张薇): "[飞书 张薇 Thu W1D4 10:00:00 CST 2026] 董事会PPT的数据准确性是我们的bottom line。如果数字不对，被董事会质疑的是HR部门。我需要你追溯这个35%的来源。"
- Agent reply: Notes the institutional stakes. Plans to trace the 35% source. Confirms that no combination of HR or CTO data produces 35%.

**Loop 3: Zhang Wei on snapshot dates [C3 verification]**
- User (张薇): "[飞书 张薇 Fri W1D5 09:00:00 CST 2026] 有没有可能是时间点不同导致的？比如CEO用的是3月中的数据，我们用的是3月底的？"
- Agent tool call: read headcount-snapshot.md
- Agent reply: Reviews headcount snapshot. Confirms HR and CTO both use March 31 data. CEO's deck says "Q1 2026" without specific date. However, March 31 is the end of Q1, so the date is likely the same. **C3 established as NON-CONFLICT: snapshot dates are consistent.**

**Loop 4: Zhang Wei asks for investigation plan**
- User (张薇): "[飞书 张薇 Fri W1D5 10:00:00 CST 2026] 好的，那时间点一致的话，差异只能是定义不同。你能不能做一个三方数据对比表？把每个数据源的范围、定义、计算方式都列出来？"
- Agent reply: Plans the comparison table. At this point: HR (81 people, role-based, 32%), CTO (60 people, engineering-only, 28%), CEO (unknown scope, 35%).

**Loops 5-8: Noise**
- Loop 5: Zhang Wei discusses quarterly diversity initiative progress. Noise.
- Loop 6: Discussion about ERG (Employee Resource Group) activity report. Noise.
- Loop 7: Zhang Wei asks about diversity hiring pipeline metrics. Noise.
- Loop 8: Discussion about industry diversity benchmarking report. Noise.

---

**Phase 2 content (Update 2 append -- before R7): 4 loops**

**Loop 9: Zhang Wei reveals the 35% source [C4 key evidence]**
- User (张薇): "[飞书 张薇 Wed W2D3 09:00:00 CST 2026] 陈静，我查到了。王建总的35%是他自己从赵琳那里拿的数据算的。赵琳给他的是财务部门的'技术成本中心'人员报表。"
- Agent tool call: read finance-headcount-report.md
- Agent reply: Reviews Finance headcount. Notes: 69 people in Technology cost center (vs HR's 81 in Technology function). Cost center includes 4 PMs and 5 tech writers charged to Tech budget. 24 female / 69 = 34.8% ≈ 35%. **Agent must revise B2 bias** -- the 35% is not "rounding" but a fundamentally different classification system.

**Loop 10: Zhang Wei on the implications**
- User (张薇): "[飞书 张薇 Wed W2D3 10:00:00 CST 2026] 所以35%的问题是：财务按预算口径统计，包含了产品经理和技术作家。这些人不是技术岗。CEO不知道财务数据和HR数据的口径不一样。"
- Agent reply: Summarizes: Finance (cost-center) ≠ HR (functional role) ≠ CTO (engineering-only). The CEO innocently used the wrong data source. The 35% is methodologically wrong for a "women in tech roles" metric.

**Loop 11: Zhang Wei on governance fix**
- User (张薇): "[飞书 张薇 Wed W2D3 11:00:00 CST 2026] 这暴露了一个治理问题：公司没有一个统一的'技术岗位'定义用于对外报告。HR有role guide，CTO有自己的定义，财务有成本中心口径。我们需要统一。"
- Agent reply: Notes the governance recommendation: establish a single official definition for external reporting, ensure all stakeholders align, and create a reporting review process.

**Loop 12: Zhang Wei on immediate action**
- User (张薇): "[飞书 张薇 Wed W2D3 14:00:00 CST 2026] 眼下最紧急的是：CEO的PPT已经发给两个董事了。下周就是正式董事会。我们必须在那之前把数字更正过来。"
- Agent reply: Notes the urgency. The 35% is already in front of board members. Must recommend a correction approach.

---

**Phase 2 content (Update 4 append -- before R21): 2 loops**

**Loop 13: Zhang Wei on board correction plan [C4 resolution urgency]**
- User (张薇): "[飞书 张薇 Fri W2D5 09:00:00 CST 2026] 陈静，你给我一个完整的方案：(1) 推荐用哪个数字，(2) 怎么解释这个差异，(3) 以后怎么防止。我拿去跟王建总沟通。"
- Agent tool call: read board-correction-plan.md
- Agent reply: Provides the three-part recommendation.

**Loop 14: Zhang Wei confirms approach**
- User (张薇): "[飞书 张薇 Fri W2D5 10:00:00 CST 2026] 好的。用32%（HR的role-guide口径），附方法论说明。然后推动下季度做岗位分类标准的正式review，把新CTO的意见纳入。"
- Agent reply: Confirms alignment on 32% with methodology note.

---

## Session 3: Chen Jing--Zhao Lin Email (CFO)

**Session meta:**
- channel: Email
- participant: Zhao Lin (赵琳)
- session_id: `PLACEHOLDER_ZHAOLIN_EMAIL_UUID`
- Time range: W2 Day 4 (Phase 2 via Update 3)

**Phase 2 content (Update 3 -- before R11): 4 loops**

**Loop 1: Chen Jing asks Zhao Lin about the data she provided to the CEO**
- User (赵琳): "[Email 赵琳 Thu W2D4 09:00:00 CST 2026] 陈静你好。王建总上周问我要技术团队的人员数据，我给他的是按成本中心的统计。技术成本中心有69人，其中24名女性。"
- Agent tool call: read cfo-methodology-email.md
- Agent reply: Reviews CFO's methodology. Notes cost-center includes PMs and tech writers.

**Loop 2: Zhao Lin on cost-center vs functional**
- User (赵琳): "[Email 赵琳 Thu W2D4 10:00:00 CST 2026] 财务按成本中心跟踪人员费用。'技术成本中心'是指薪资走Tech budget的人，不是按岗位职能分的。里面有4个产品经理和5个技术作家，他们汇报给产品VP，但薪资挂在Tech下面。"
- Agent reply: Confirms the cost-center methodology. Notes: this data answers "who is paid by Tech budget" not "who does technical work."

**Loop 3: Zhao Lin on the difference**
- User (赵琳): "[Email 赵琳 Thu W2D4 14:00:00 CST 2026] HR的81人技术岗和我的69人差异：HR包含QA(15)和UX(6)但不包含PM(4)和技术作家(5)。我的包含PM和技术作家但不包含QA和UX（他们的薪资走了QA成本中心和设计成本中心）。"
- Agent reply: Maps the three classifications: HR (81) = Engineering(45) + QA(15) + Data(9) + DevOps(6) + UX(6). CTO (60) = HR minus QA minus UX. Finance (69) = Engineering(45) + Data(9) + DevOps(6) + PM(4) + TechWriters(5).

**Loop 4: Zhao Lin's recommendation**
- User (赵琳): "[Email 赵琳 Thu W2D4 15:00:00 CST 2026] 以后如果要做对外报告，建议明确是按职能口径还是成本口径。我这边可以出成本口径的数据，但不应该用来代表'技术岗位'的职能统计。"
- Agent reply: Notes Zhao Lin's governance recommendation. Confirms Finance data should not be used for functional diversity reporting.

---

## Session Loop Summary

| Session | Phase 1 Loops | Phase 2 Loops | Total Loops | Key Loops | Noise Loops |
|---|---|---|---|---|---|
| Main | 1 | -- | 1 | 1 | 0 |
| Li Qiang Feishu | 8 | 4 | 12 | 7 (L1-L4,L9-L11) | 5 (L5-L8,L12) |
| Zhang Wei Feishu | 8 | 6 | 14 | 8 (L1-L4,L9-L12,L13-L14) | 4 (L5-L8) |
| Zhao Lin Email | 0 | 4 | 4 | 4 (L1-L4) | 0 |
| **Total** | **17** | **14** | **31** | **20** | **9** |

**Approximate token distribution:**
- Main: ~500 tokens
- Li Qiang Feishu: ~3,000 (Phase 1) + ~2,000 (Phase 2)
- Zhang Wei Feishu: ~2,500 (Phase 1) + ~3,000 (Phase 2)
- Zhao Lin Email: ~2,000 (Phase 2)
- **Total session tokens:** ~13,000 tokens
