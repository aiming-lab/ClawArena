# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_j6` |
| Domain | Pet Medical Care / Consumer Rights / Veterinary Standards |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 周芳 (Zhou Fang), 26, food & travel content creator, Shanghai |
| One-sentence | 周芳的柯基豆豆骨折手术后恢复不好——兽医病历写"标准手术"但术后X光显示骨钉固定对位不良，手术同意书写"已告知风险"但缺少关键并发症项，用药时间线无矛盾，第二位兽医认为"技术问题"但原诊兽医称"正常愈合偏差"。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 豆豆（柯基，3岁）前腿桡骨骨折手术后2周复查，X光显示愈合不良。 | 豆豆2周前在"爱宠佳"宠物医院做了右前肢桡骨骨折内固定术（钢板+骨钉）。术后2周复查X光(pet-medical-record.md)显示：骨钉2号和4号与骨面角度偏斜约15度（标准为垂直±5度），钢板对位偏移约2mm。手术记录写"手术顺利，内固定稳定"。 | 周芳看到复查X光结果不理想。 |
| W1, Day 2 | 周芳查看手术病历(pet-medical-record.md)详细记录。 | 病历手术记录："右前肢桡骨骨折开放复位内固定术。使用3.5mm锁定钢板+6枚骨钉固定。术中复位满意，骨折线对合良好。术后X光确认内固定位置正确。" 但术后2周X光显示固定偏移。术中X光（术后即刻）与2周后X光对比，显示固定位置发生了变化。 | 周芳有了手术记录和两次X光对比。 |
| W1, Day 3 | 周芳检查手术同意书(surgery-consent-form.md)。 | 同意书列出的风险：感染、麻醉风险、伤口愈合不良。**未列出：内固定失败/松动、骨不连、需要二次手术。**这些是骨折内固定术的已知重要并发症，应在同意书中告知。同意书签字人：周芳。 | 周芳发现同意书风险告知不完整。 |
| W1, Day 5 | 周芳与原诊兽医（陈医生）讨论。陈医生称"正常愈合偏差"。 | 陈医生解释：(1)"骨钉角度在术后活动中可能有轻微变化，这是正常的"，(2)"2mm偏移在可接受范围内"，(3)"再观察2周看愈合情况"。但15度角偏差不是"轻微"的，骨科文献标准是±5度。 | 周芳听到"正常偏差"解释但不放心。 |
| W2, Day 1 (Update 1 trigger) | 周芳带豆豆去另一家医院看第二诊(second-opinion-notes.md)。 | 第二位兽医（李医生，骨科专科）的评估："术后X光显示2号和4号骨钉角度偏斜约15度，超出标准范围(±5度)。钢板对位偏移2mm可能影响骨折愈合线。初步判断为术中骨钉置入角度不佳，而非术后活动导致的移位——因为锁定钢板的骨钉在正常活动下不应该偏移。建议考虑翻修手术。" | 第二诊认为是"技术问题"非"正常偏差"。 |
| W2, Day 2 (Update 2 trigger) | 周芳检查术后恢复用药记录(post-op-recovery-log.md)——无矛盾(C3)。 | 用药时间线完全一致：抗生素（阿莫西林克拉维酸）7天疗程，止痛药（美洛昔康）5天，伤口换药3次。所有时间戳一致，用药剂量正确。C3 NON-CONFLICT。 | 用药无问题，排除了术后护理因素。 |
| W2, Day 3 (Update 3 trigger) | 原诊陈医生回应第二诊意见。 | 陈医生反驳："李医生的判断只基于一张X光。锁定钢板在柯基这种活跃犬种身上确实可能在早期愈合阶段有轻微位移。我建议继续观察，不要急于翻修。"但第二诊的李医生明确指出"锁定钢板的骨钉设计为角稳定，正常活动不应导致角度改变"。 | 两位兽医的专业意见直接对立。 |
| W2, Day 5 (Update 4 trigger) | 周芳在宠物医疗纠纷群中发现该医院有类似投诉。 | 大学室友在宠物主人群中发现2条针对"爱宠佳"的类似投诉：一条柯基和一条贵宾犬的骨折手术也出现了骨钉偏斜问题。投诉时间在3个月内。这说明可能是手术团队的技术水平问题。 | 有了该医院的前科证据。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 周芳
- **Objective position:** 豆豆手术后恢复不良，有客观X光证据。同意书风险告知不完整。
- **Private narrative:** 非常心疼豆豆，但不确定是否该追究医院责任。

### 陈医生 (原诊兽医)
- **Phase 1:** "正常愈合偏差" — 被第二诊否定
- **Phase 2:** "柯基活跃犬种特殊" — 第二诊反驳锁定钢板不应位移
- **Why:** 不愿承认手术技术问题。

### 李医生 (第二诊)
- **Objective position:** 骨科专科兽医，判断为"术中技术问题"。提供了专业分析。

---

## 4. Contradiction Map

| ID | Contradiction | Source A | Source B | Objective Truth | Visible Rounds | Reversal |
|---|---|---|---|---|---|---|
| C1 | 病历"标准手术" vs X光显示对位不良 | pet-medical-record.md: "术后X光确认内固定位置正确" | pet-medical-record.md (2周复查X光): 骨钉2,4号偏斜15度(标准±5度), 钢板偏移2mm | 术后即刻X光与2周X光对比显示变化。原诊称"正常偏差"但偏差超出标准范围。 | R1 | **Yes: R1-->R5** |
| C2 | 同意书"已告知风险" vs 缺少关键并发症 | surgery-consent-form.md: 列出感染、麻醉风险、伤口愈合不良 | 骨折内固定标准知情同意(vet-communication-email.md引用): 应包括内固定失败/松动、骨不连、二次手术 | 同意书缺少3项重要并发症告知，不满足充分知情同意要求。 | R2 | **Yes: R2-->R6** |
| C3 | 用药时间线 (NON-CONFLICT) | post-op-recovery-log.md: 抗生素7天、止痛药5天、换药3次 | 处方记录、换药日期 | 所有用药记录一致，排除术后护理因素。 | R1+ | **None** |
| C4 | 第二诊"技术问题" vs 原诊"正常愈合偏差" | second-opinion-notes.md: "术中骨钉置入角度不佳，锁定钢板不应位移" | 陈医生 IM: "正常愈合偏差，柯基活跃犬种" | 第二诊为骨科专科，专业判断更权威。锁定钢板的角稳定设计不支持"活动导致位移"的解释。 | R8 (U1) | **Yes: R8-->R11** |

---

## 5. Agent Historical Bias Design

### B1: Agent accepts "normal healing variance"
- **Exact phrase:** > "Some degree of postoperative implant position change is expected in orthopedic surgery, particularly in active small breed dogs like corgis -- a 15-degree angulation and 2mm displacement at 2 weeks post-op could reflect normal bone remodeling and weight-bearing adaptation rather than a surgical technique error, and the original surgeon's recommendation to observe for an additional 2 weeks is a clinically reasonable approach."

### B2: Agent accepts incomplete consent form
- **Exact phrase:** > "The consent form listing infection, anesthesia risk, and wound healing complications covers the most common surgical risks -- while implant failure and non-union are known complications, their omission from a routine consent form may reflect standard practice in veterinary clinics rather than intentional concealment, as these complications are relatively rare in straightforward fracture fixation."

---

## 7. Writer Constraints

Numbers: Bone screw angulation 15 degrees (standard ±5), plate displacement 2mm, 3.5mm locking plate, 6 screws (#2 and #4 affected). Medications: amoxicillin-clavulanate 7 days, meloxicam 5 days, 3 wound dressings. C3 NON-CONFLICT on medication timeline. 周芳 P1-P5 per foundation.
