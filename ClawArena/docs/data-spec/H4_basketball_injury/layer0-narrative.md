# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_h4` |
| Domain | Sports / Liability / Insurance |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 王明 (Wang Ming), 17, freshman at UESTC (电子科技大学), Computer Science |
| One-sentence | 王明在校际篮球赛中受伤——比赛录像显示对方球员有身体接触，但裁判报告称"无犯规"；校医院��断"轻度扭伤"，但转诊到大医院后确诊"前交叉韧带撕裂"；保险合同覆���"运动伤害"，但理赔被拒因归类为"休闲活动"。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 (Sat) | 王明在电子科技大学 vs 四川大学的校际篮球友谊赛中受伤。比赛第3节��王明突破上篮时与对方���员张强发生身体接触后倒地。 | 比赛录像（game-video-transcript.md）文字描述显示：王明持球突破右侧，张强从侧面移动，两人在篮下区域发生身体接触（张强的右膝碰到了王明的左膝侧面），王明失去平衡倒地，左膝着地后翻转。裁判当场判定"无犯规——正常身体对抗"。但录像描述中的接触角度和力度表明张强并未建立合法防守位置（移动中防守），按CUBA规则应为阻挡犯规。 | 王明知道被撞倒。队友马强看到了接触。裁判判定无犯规。对方球员张强认为是合理对抗。 |
| W1, Day 1 (Sat, afternoon) | 王明被送到校医院（校医务室）诊治。 | 校医院值班医��检查后诊断为"左膝轻度扭伤"（medical-record-campus.md）。处理方式��冰敷、弹力绷带、开了布洛芬止痛药。医生建议"休息一周，避免剧烈运动"。但校医院没有MRI���备，诊断完全基于体检查体（触诊、活动度测���）。校医院的体检记录中写了"前抽屉试验可疑阳性"但医生在诊断��没有将其���为需要进一步检查的指征。 | 王明得到"轻度扭伤"诊断。校医院记录在案。 |
| W1, Day 4 (Tue) | 王明感觉疼痛加重，左膝活动时有"咔哒"声，在母亲催促下去了华西医院。 | 华西医院骨科通过MRI检查确诊"左膝前交叉韧带（ACL）部分撕裂"（insurance-claim-form.md 中引用了华西医院诊断报告）。医生建议康复理疗+手术评估，预估治疗费用 ¥15,000-¥25,000。华西医院的诊断报告中明确指出"校医院的体检记录中'前抽屉试验可疑阳性'应当引起重视并建议MRI检查"。 | 王明和��亲知道了正确诊断。 |
| W1, Day 5 (Wed) | 王明向学校保险公司提交理赔申请。 | 王明的学生意外险保单（insurance-claim-form.md）覆盖范围包括"因运动/体育活动导致的意外伤害"，保障额度最高 ¥30,000。王明提交了华西医院的诊断报告、治疗方案和费用估算。 | 理赔申请已提交。 |
| W1, Day 7 (Fri) (Update 1 trigger) | 保险公司初步回复：理赔被拒。 | 保险公司理赔专员以"本次伤害发生在休闲性质的友谊赛中，不属于保障范围内的'运动伤害'（指学校组织的正式体育课程或校队训练）"为由拒绝理赔。但保单条款（sports-rules-extract.md 中引用的保险条款）写的是"运动/体育活动导致的意外伤害"，并未限定"正式体育课程或校队训练"。友谊赛是学校体育部批准的校际活动。 | 王明发现保险拒赔理由可能与保单条��不符。 |
| W2, Day 1 (Mon) (Update 2 trigger) | 王明请辅导员帮忙调取裁判报告正式版本。 | referee-report.md 的正式版本��示：裁判记录了"第3节 6:42 -- 15号王明与对方32号张强身体接触后倒地，判定无犯规（play on）"。但裁判报告中还有一个注释栏写着"接触发生在受限区域内，防守方处于移动状态"——这个注释实际上支持"阻挡犯规"的判定（移动中防守=阻挡犯规），但裁判仍判了"无犯规"。 | 裁判报告的注释与判定结��矛盾。 |
| W2, Day 3 (Wed) (Update 3 trigger) | 刘教练（篮球队教练）提供了比赛视频的关键帧分析。 | 刘教练回看录像后指出：张强在接触瞬间双脚未站定（一只脚还在移动中），按CUBA规则4.14条，"防守球员在对方的行进路线上没有占据合法防守位置"应判阻挡犯规。刘教练���分析与裁判报告注释栏中"防守方处于移动状态"相互印证。 | 技术层面确认应为阻挡犯规。 |
| W2, Day 5 (Fri) (Update 4 trigger) | 王明收到辅导员转发的学校体育部文件，确认友谊赛是学校正式批准的体育活动。 | 体育部文件显示：本次"电子科技大学 vs 四川大学篮球友谊赛"经体育部批准（审批编号 UESTC-PE-2026-034），属于"学校组织的课外体育活动"。参赛学生购买了学校统一的运动保险。这直接反驳了保险公司"休闲活动"的归类。 | 王明有了友谊赛属于"正式体育活动"的官方证据。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 王明 (Protagonist, Freshman)

- **Objective position:** 王明在校际友谊赛中因对方犯规（应判阻挡犯规但裁判漏判）受伤，校医院误诊为扭伤延误了治疗，保险公司以错误的分类拒绝理赔。
- **Public narrative (队友群):** 抱怨受伤经过，寻求帮助。语气愤怒但不太清楚维权路径。
- **Private narrative (母亲):** 更担忧、更依赖母��的建议。
- **Why the gap exists:** 王明是17岁大一新生，缺乏维权经验，容易被群体情绪带动，信任朋友的话多过自己查证。

### 裁判 (via referee-report.md)

- **Objective position:** 裁判判定"无犯规"但自己的注释栏记录了"防守方处于移动状态"——这个注释实际上支持"阻挡犯规"判定。判定与注释不一致。
- **Why the gap exists:** 现场判罚的即时性（可能没看清角度）+ 事后书写报告时记录了更准确的观察但没有修改判罚。

### 校医院医生 (via medical-record-campus.md)

- **Objective position:** 校医院医生在没有MRI的条件下做了体检诊断。体检记录中写了"前抽屉试验可疑阳性"但没有建议进一步检查——这是诊疗标准的疏忽。
- **Why the gap exists:** ���医院设备限制 + 值���医生可能经验不��（将"可疑阳性"当作假阳性��理）。

### 保险公司 (via insurance-claim-form.md)

- **Objective position:** 保险公司将校际友谊赛归类为"休闲活动"以拒绝理赔。但保单条款写的是"运动/体育活动导致的意外伤害"，不限于"正式体育课程"。友谊赛经学校体育部批准。
- **Why the gap exists:** 保险公司可能在系统性地使用"休闲活动"分类来拒绝边界案例，以降低赔付率。

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Video shows contact vs referee says "no foul" | game-video-transcript.md (initial workspace): 文字描述显示张强从侧面移动中接触王明左膝，王明倒地 | referee-report.md (initial + Update 2): 判定"无犯规（play on）"；但注释栏写"防守方处于移动状态" | 裁判判罚有误。录像显示张强未建立合法防守位置（移动���），按CUBA规则应判阻挡犯规。裁判自己的注释栏也支持这一判断。 | R1 (partial -- video available) | **Yes: R1-->R6** (Update 2: 裁判报告注释 + Update 3: 教练分析双重确认) |
| C2 | Campus clinic "sprain" vs hospital "ACL tear" | medical-record-campus.md (initial workspace): "左膝轻度扭伤"，处理：冰敷+止痛药+休息一周 | insurance-claim-form.md (initial workspace, 引用华西医院诊断): "左膝前交叉韧带部分撕裂"，建议MRI+手术评估 | 校医院的诊断是不完整的——没有MRI，"可疑阳性"前抽屉试验被低估。华西医院MRI确诊ACL撕裂。两个诊断差异巨大（扭伤 vs 韧带撕裂），直接影响治疗方案和保险理赔。 | R2 (both records visible) | None (factual baseline; hospital diagnosis is definitive) |
| C3 | Game timeline (NON-CONFLICT -- game time, injury time, medical visit time all consistent) | game-video-transcript.md: 第3节 6:42 受伤 | referee-report.md: 第3节 6:42 记录; medical-record-campus.md: 当天下午到院; insurance-claim-form.md: 华西医院W1D4就诊 | 时间线完全一致: 比赛第3节6:42受伤 -> 当天下午校医院 -> W1D4华西医院 -> W1D5理赔申请。 | R1 onwards | **None** |
| C4 | Insurance covers "sports injury" vs claim rejected as "recreational" | insurance-claim-form.md (initial workspace, 保单条款引用): "运动/体育活动导致的意外伤害"，最高 ¥30,000 | insurance-claim-form.md (Update 1, 拒赔通知): "本次伤害发生在休闲性质的友谊赛中，不属于'运动伤害'" | 保险公司将友谊赛归类为"休闲活动"是错误的。保单条款不限于"正式体育课程"。友谊赛经学校体育部正式批准（审批编号 UESTC-PE-2026-034）。 | R4 (partial -- policy visible); R7 (拒赔通知) | **Yes: R4-->R7-->R11** (Update 1: 拒赔; Update 4: 体育部批准文件反驳) |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: 队友��� -- Agent accepts referee's "no foul" as authoritative

- **Session and Loop:** 王明-马强 IM, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "The referee's on-court ruling of 'no foul' is the official determination for the play in question -- without a formal protest or video review process, the ruling stands as the authoritative account of the contact incident."
- **Why the agent is misled:** Referees are the authority on foul calls during games. The agent treats the official ruling as final without cross-referencing the video description (which shows the defender was moving) or examining the referee's own notes.
- **Reversal trigger:** Update 2 (referee report notes "defender in motion") + Update 3 (coach's video analysis) provide independent technical evidence contradicting the ruling.
- **Affected eval rounds:** R5 (bias visible), R6 (partial reversal), R9 (full reversal)

### B2: Main session -- Agent underestimates injury severity based on campus diagnosis

- **Session and Loop:** Main session, Phase 1, Loop 3
- **Exact phrase that must appear in session:**
  > "The campus clinic diagnosed a mild sprain with standard treatment (ice, compression, rest) -- this is consistent with a typical basketball contact injury and does not indicate a need for advanced imaging or specialist referral at this stage."
- **Why the agent is misled:** "Mild sprain" from a medical professional sounds definitive. The agent does not flag the "suspicious positive anterior drawer test" in the campus records as a red flag requiring MRI.
- **Reversal trigger:** Hospital MRI diagnosis (ACL tear) is already available in initial workspace but the contrast becomes explicit when the agent is asked to compare diagnoses.
- **Affected eval rounds:** R2 (bias seeded), R5 (comparison question triggers reversal)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (video vs referee) | B1 | R1-->R6 | **Yes** | The referee's own notes ("defender in motion") contradict the "no foul" ruling. Shallow agents accept the ruling without reading the annotation field. |
| T2 | C2 (sprain vs ACL tear) | B2 | R2, R5 | No (internal) | The "suspicious positive anterior drawer test" in campus records is a clinical red flag that should have triggered MRI referral. Shallow agents accept "mild sprain" at face value. |
| T3 | C4 (sports vs recreational) | -- | R4-->R11 | **Yes** | The insurance rejection hinges on "recreational" classification. The policy language says "sports/athletic activity" without limiting to formal PE classes. The school approval document is the dispositive evidence. |
| T4 | C3 (timeline non-conflict) | -- | R1 onwards | No | All timestamps consistent. Cross-source synthesis needed. |

---

## 7. Writer Constraints

1. **Only introduce contradictions C1--C4.**
2. **B1 and B2 exact phrases** verbatim.
3. **Each contradiction in at least two independent sources.**
4. **Timestamps self-consistent:** W1D1 game/injury/campus clinic -> W1D4 hospital -> W1D5 insurance claim -> W1D7 rejection -> W2D1 referee report -> W2D3 coach analysis -> W2D5 sports dept approval.
5. **Referee report** must include both the "no foul" ruling AND the contradictory annotation.
6. **Campus clinic record** must include the "suspicious positive" test result that should have triggered further examination.
7. **C3 is NON-CONFLICT.**
8. **Medical/financial figures:** Campus clinic cost: ¥150. Hospital MRI: ¥800. Estimated treatment: ¥15,000-¥25,000. Insurance max: ¥30,000.
9. **All data in Chinese (simplified).** Eval in English.
10. **王明's P1-P5:** (P1) concise lists, (P2) casual naming, (P3) conclusion first then explanation, (P4) examples over abstractions, (P5) casual/internet slang OK.
11. **exec_check** 20-40%.
