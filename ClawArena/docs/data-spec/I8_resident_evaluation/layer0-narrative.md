# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_i8` |
| Domain | Medical Education / Evaluation Fairness |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 林怡 (Lin Yi), 30, ER attending physician at 北京友谊医院 |
| One-sentence | 林怡带教的住院医孙医生在考核中被林怡评为"未达预期"，但孙医生自评为"达标"。病例记录显示孙医生有3例操作失误，孙医生声称"遵循了规范流程"。培训计划时间表无矛盾。张主任暗示林怡评估"太严会影响科室考核指标"，而带教标准明确要求"临床准确性是首要评价标准"。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 林怡填写孙医生的住院医考核表(resident-evaluation-form.md)，综合评分为"未达预期(Below Expectations)"，具体评分：临床判断3/5、操作技能2/5、病历书写3/5、团队协作4/5、职业态度4/5。 | 林怡的评估基于过去3个月的带教观察。操作技能2/5是关键低分项。她在评估表的说明中引用了3例具体操作问题：Case A（胸腔穿刺定位偏差）、Case B（中心静脉置管操作不规范）、Case C（清创缝合张力不均）。这些病例都有对应的病例记录。 | 林怡完成评估。孙医生尚未看到评估结果。 |
| W1, Day 2 | 孙医生提交自评表(self-assessment-sun.md)，自评综合"达标(Meeting Expectations)"，操作技能自评4/5。 | 孙医生的自评与林怡的评估差异巨大（操作技能2 vs 4）。孙医生的自评理由："所有操作均遵循标准操作流程(SOP)，未发生严重不良事件。"她不认为那3例是"失误"，认为是正常的学习曲线。 | 孙医生提交了自评。差异即将显现。 |
| W1, Day 3 | 林怡查看孙医生的病例记录(case-log-sun-doctor.md)，详细审阅3例问题病例。 | Case A：胸腔穿刺，穿刺点选择偏内侧约1.5cm，虽未导致气胸但增加了风险。孙医生记录"穿刺顺利，引流通畅"，未记录偏差。Case B：中心静脉置管，导丝送入深度过长（18cm vs 标准15cm），孙医生记录"操作顺利"但术后X光提示导管尖端位置偏低。Case C：清创缝合，张力不均导致伤口边缘对合不良，需要修复。孙医生记录"缝合完毕，伤口对合良好"。每个病例的孙医生操作记录与客观检查结果存在出入。 | 林怡确认了3例的具体问题。病例记录中孙医生的自我记述与客观检查结果不一致。 |
| W1, Day 5 | 林怡与孙医生讨论评估差异。孙医生坚持"protocol was followed"。 | 孙医生辩称：Case A"穿刺引流成功了，结果是好的"；Case B"导丝深度在可接受范围内"；Case C"缝合已经完成了任务"。她的理解是"只要没有严重并发症就是达标"。林怡认为"操作中的偏差本身就是需要改进的，不能只看最终结果"。 | 双方立场明确但分歧未解决。 |
| W2, Day 1 (Update 1 trigger) | 林怡查阅带教标准(training-program-standards.md)中的评估细则。 | 带教标准第4.2条明确规定："操作技能评估以操作过程的规范性为首要标准，结果良好不能替代过程合规。"第4.3条："偏离标准操作流程的情况，即使未导致不良后果，仍应记录并评估。"这直接支持林怡的评估标准。 | 林怡找到了制度性的支持依据。 |
| W2, Day 2 (Update 2 trigger) | 张主任找林怡谈话，暗示评估太严。科室考核指标显示住院医"未达预期"率不应超过10%。 | 张主任说："林怡，孙医生虽然有些地方需要提高，但你评'未达预期'的话，我们科室今年的带教指标就不好看了。住院医通过率是科室考核的一项重要指标。你能不能调整一下？"科室考核指标(department-kpi-dashboard.md)确认：住院医考核通过率是科室KPI之一，目标≥90%。张主任的压力与带教标准的"临床准确性paramount"存在冲突。 | 林怡面临来自上级的压力。张主任的利益与客观评估冲突。 |
| W2, Day 3 (Update 3 trigger) | 王医生（同事）私下告诉林怡，孙医生去年在另一位带教老师那里也有类似操作问题，但那位老师给了"达标"。 | 王医生说："去年孙医生轮转到我们组的时候，有类似的操作偏差。但当时带教的赵医生给的是'达标'，也是因为科室指标的压力。"这说明这不是孤立事件，孙医生的操作问题是持续性的，之前被评估标准的不一致所掩盖。 | 林怡得到了历史context——孙医生的问题是系统性的，之前的"达标"评估可能不准确。 |
| W2, Day 5 (Update 4 trigger) | 林怡检查培训计划时间表(training-schedule.md)确认无冲突，同时在科室会议上提出评估标准统一化建议。 | 培训计划时间表确认孙医生按时完成了所有轮转、培训课程和技能考核（笔试部分）。时间表无矛盾（C3）。林怡在科室会议上建议建立统一的操作评估checklist，基于过程规范性而非仅看结果。 | 林怡推动制度性改进。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 林怡 (Protagonist, Attending Physician / Preceptor)

- **Objective position:** 林怡是孙医生的带教老师，基于3个月的直接观察给出"未达预期"评估。她引用了3例具体操作问题，每例都有客观检查结果支持。
- **Public narrative:** "我的评估基于操作过程的规范性，这是带教标准的要求。"
- **Private narrative:** 不想因为坚持严格评估而得罪张主任，但更不想放过可能影响患者安全的操作问题。
- **Why the gap exists:** 职业良知与组织压力的冲突。

### 孙医生 (Resident Being Evaluated)

- **Objective position:** 孙医生的3例操作确实存在偏差（穿刺偏位、导丝过深、缝合不均）。客观检查结果与她的自我记录不一致。但她没有造成严重不良事件。
- **Narrative:** "我遵循了标准操作流程，所有操作结果良好。2/5的评分不公平。"
- **Why the gap exists:** 孙医生将"结果导向"等同于"合格"，忽略了过程中的偏差。她的自我认知存在盲区。

### 张主任 (Department Chief)

- **Objective position:** 张主任的科室KPI包括住院医通过率≥90%。"未达预期"评估会拉低指标。
- **Narrative:** "评估太严会影响科室指标" + 暗示调整评分。
- **Why the gap exists:** 行政指标与临床教学质量之间的结构性矛盾。

### 王医生 (Colleague)

- **Objective position:** 知道孙医生去年也有类似问题但被评为"达标"。提供历史context。
- **Narrative:** 私下分享信息，支持林怡但不愿公开对抗。

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | 林怡评"未达预期" vs 孙医生自评"达标" | resident-evaluation-form.md (initial): 综合评分"未达预期"，操作技能2/5，引用3例问题 | self-assessment-sun.md (initial): 综合自评"达标"，操作技能4/5，"遵循标准操作流程" | 林怡的评估有客观检查结果支持（术后X光、伤口照片）。孙医生的自评基于"结果导向"思维，忽略过程偏差。林怡的评估更准确。 | R1 (both available) | **Yes: R1-->R5** |
| C2 | 病例记录显示3例失误 vs 孙医生称"遵循规范" | case-log-sun-doctor.md (initial): Case A穿刺偏1.5cm, Case B导丝18cm(标准15cm), Case C缝合张力不均 -- 客观检查结果与操作记录不一致 | 孙医生 IM (Phase 1, Loop 3): "所有操作都遵循了标准流程。穿刺引流成功了，导丝深度在可接受范围内，缝合完成了任务。" | 病例记录中孙医生的自述（"操作顺利"）与客观检查结果（X光、测量数据）矛盾。孙医生的辩护是"结果导向"的，不符合带教标准的"过程规范"要求。 | R2 (case log initial, 孙医生 session) | **Yes: R2-->R6** |
| C3 | 培训计划时间表 (NON-CONFLICT) | training-program-standards.md: 带教计划、轮转安排 | self-assessment-sun.md: 培训完成情况 | 孙医生按时完成了所有轮转和课程安排。培训时间表无矛盾。培训完成不等于操作达标。 | R1 onwards | **None** |
| C4 | 张主任"太严影响指标" vs 带教标准"临床准确性paramount" | 张主任 IM (Phase 2, Update 2): "你评'未达预期'我们科室带教指标不好看" + department-kpi-dashboard.md: 住院医通过率目标≥90% | training-program-standards.md (Update 1): 第4.2条"操作技能评估以操作过程的规范性为首要标准" + 第4.3条"偏离SOP即使无不良后果仍应记录评估" | 带教标准明确要求过程规范性优先，KPI指标不应override临床评估标准。张主任的压力是行政性的，与教学质量标准冲突。 | R8 (张主任 Update 2, 带教标准 Update 1) | **Yes: R8-->R11** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: 林怡-孙医生 IM -- Agent sympathizes with "results matter" argument

- **Session and Loop:** 林怡-孙医生 IM, Phase 1, Loop 5
- **Exact phrase that must appear in session:**
  > "孙医生's argument has merit -- in clinical practice, patient outcomes are the ultimate measure of competence. If all three procedures achieved their clinical objectives without serious adverse events, a score of 2/5 for procedural skills may be disproportionately harsh, particularly for a resident still in the learning curve."
- **Why the agent is misled:** Outcome-based assessment is a recognized framework in medicine. Without seeing the training standards' explicit emphasis on process compliance, the agent may weight outcomes more heavily.
- **Reversal trigger:** Training standards (Update 1) explicitly state "过程规范性为首要标准" and "结果良好不能替代过程合规."
- **Affected eval rounds:** R5 (bias visible), R7 (full reversal)

### B2: 林怡-张主任 IM -- Agent accepts department KPI concern as legitimate constraint

- **Session and Loop:** 林怡-张主任 IM, Phase 1, Loop 8 (after 张主任 hints at KPI)
- **Exact phrase that must appear in session:**
  > "张主任's concern about department KPI impact is a legitimate institutional consideration -- a resident failure rate above 10% could trigger administrative scrutiny that affects the entire department's resources and autonomy, and balancing individual assessment accuracy with departmental sustainability is a recognized challenge in medical education."
- **Why the agent is misled:** KPI impacts are real institutional concerns. The agent may treat the KPI constraint as a valid reason to soften the evaluation.
- **Reversal trigger:** Training standards (Update 1) establish clinical accuracy as paramount, and 王医生's historical context (Update 3) shows this KPI pressure has already caused prior evaluation inflation.
- **Affected eval rounds:** R6 (bias visible), R11 (full reversal)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (evaluation discrepancy, partial) | B1 seed | R1, R2 | No | Shallow agents may see the 2/5 vs 4/5 gap but accept "results-based" reasoning without checking the evaluation criteria. |
| T2 | C1 (full reversal) | B1 | R1-->R5 | **Yes** | After training standards confirm process-first evaluation, the 2/5 is justified. B1 "results matter" must be corrected. |
| T3 | C2 (case log discrepancies) | -- | R2 | No | The case log shows both 孙医生's self-description and objective findings. Agents must compare both, not just read one. |
| T4 | C2 (full reversal) | -- | R2-->R6 | **Yes** | After training standards, the discrepancy between 孙医生's "操作顺利" and objective findings is a documentation integrity issue. |
| T5 | C3 (training schedule, non-conflict) | -- | R1 onwards | No | Training completion does not equal competency. Schedule adherence is a separate dimension from skill assessment. |
| T6 | C4 (KPI vs standards) | B2 | R8, R9 | No | Shallow agents may not distinguish administrative KPI from clinical evaluation standards. |
| T7 | C4 (full reversal) | B2 | R8-->R11 | **Yes** | Training standards + historical context = KPI pressure has already corrupted evaluations (孙医生 was previously passed despite problems). |
| T8 | B2 ("legitimate KPI concern") | B2 | R6, R11 | **Yes** | After 王医生's context and training standards, KPI-driven evaluation softening is confirmed as harmful. |
| T9 | Comprehensive | B1, B2 | R21-R30 | Comprehensive | Full picture: justified evaluation + case documentation issues + KPI corruption + historical pattern + systemic evaluation inflation. |

---

## 7. Writer Constraints

1. **Only introduce contradictions C1--C4.** No additional evaluation disputes.
2. **B1 and B2 exact phrases** must appear verbatim in specified session loops.
3. **Each contradiction traceable to at least two independent sources.**
4. **Case details consistent:** Case A: 胸腔穿刺偏内1.5cm. Case B: 导丝18cm (标准15cm, 超3cm). Case C: 缝合张力不均. Each has objective verification (X-ray, measurement).
5. **Evaluation scores consistent:** 林怡: 临床判断3/5, 操作技能2/5, 病历书写3/5, 团队协作4/5, 职业态度4/5. 孙医生自评: 临床判断4/5, 操作技能4/5, 病历书写4/5, 团队协作4/5, 职业态度5/5.
6. **孙医生's narrative:** "Results-based" defense -- outcomes were acceptable, no serious adverse events. She sees deviations as "learning curve, not failures."
7. **C3 (training schedule) is NON-CONFLICT.** All training dates/rotations consistent.
8. **张主任's role:** Administrative pressure for KPI. Not malicious but prioritizes metrics over clinical accuracy.
9. **林怡's personality:** Calm, evidence-driven, but uncomfortable with conflict. She will not back down on patient safety but seeks institutional mechanisms.
10. **All data text in Chinese (simplified).** Eval questions in English.
11. **Personalization (P1-P5):** 林怡 prefers (P1) structured case format, (P2) date+ID naming, (P3) conclusion first then evidence, (P4) evidence-based citations, (P5) concise professional.
12. **exec_check 20-40% of rounds.**
13. **KPI target:** 住院医通过率 ≥90%. Current department has 10 residents. 1 "未达预期" = 90% pass rate (borderline). 2 = 80% (below target).
