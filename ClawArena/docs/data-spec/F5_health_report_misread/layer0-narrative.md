# Layer 0 -- Narrative Bible and Eval Trap Design

> Authoritative truth baseline. Does not appear in any data file.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_f5` |
| Domain | 健康 / 家庭沟通 |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 赵磊 (Zhao Lei), 34, independent quantitative trader based in Shanghai |
| One-sentence | 赵磊年度体检结果在健康App（正常）、医院系统（LDL偏高，标记异常）和母亲的理解（恐慌，联想遗传病）之间呈现三种不同解读——实际原因是仪器校准偏差导致的假阳性，陈医生在邮件中解释了但赵磊当时没仔细读；同时药房根据医院系统的标记开了降脂药，但陈医生说不需要用药。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 赵磊完成年度体检，收到健康App（Apple Watch + 手环数据汇总）的健康摘要："各项指标正常。" | 赵磊的可穿戴设备（Apple Watch + 小米手环）持续监测的数据显示：静息心率62bpm、血压118/76、睡眠7.2小时、日均步数8,500。这些数据在正常范围内。但可穿戴设备不检测血脂（LDL/HDL），所以健康App的"各项指标正常"只是基于它能测量的指标——不包含血脂。 | 赵磊认为自己体检全部正常。 |
| W1, Day 2 | 医院体检中心发布正式化验报告，赵磊收到短信通知"报告已出"。 | 医院化验报告 (hospital-lab-results.md) 显示：LDL-C = 4.2 mmol/L，标注"↑偏高"（参考范围 < 3.4 mmol/L）。其他血脂指标正常（HDL 1.5, TG 1.2, TC 5.1）。实际情况：该批次化验仪器 (Beckman AU5800) 在 2026-10-01 至 2026-10-05 期间存在校准偏差，导致 LDL-C 测量值系统性偏高约 0.8-1.0 mmol/L。赵磊的真实 LDL-C 约 3.2-3.4 mmol/L（正常或临界，不需要药物治疗）。陈医生在 10 月 6 日发现了校准问题并已通知受影响的患者——但赵磊没仔细读陈医生的邮件。 | 医院系统标记LDL偏高。陈医生知道是校准问题。赵磊看到了"偏高"标记但没看医生邮件。 |
| W1, Day 3 | 赵磊的母亲（退休医生）打电话问体检结果。赵磊提到LDL偏高。母亲恐慌。 | 赵磊的母亲（P204）是退休心内科医生。听到"LDL偏高"后，她立即联想到赵磊父亲的病史：赵父 55 岁时因冠心病做了支架手术，有家族性高胆固醇血症倾向。母亲说："你爸当年也是这样开始的，先是LDL高，后来就动脉硬化了。你赶紧去复查，可能需要开始吃他汀。" 母亲的担忧从医学角度并非完全无理（家族史确实是风险因素），但她不知道这次LDL偏高是仪器校准问题导致的假阳性。 | 母亲恐慌，认为遗传风险。赵磊被母亲的反应吓到了。陈医生已发了解释邮件但赵磊没读。 |
| W1, Day 4 | 赵磊去医院附近药房取体检报告建议的处方。药房根据医院系统的LDL标记配了阿托伐他汀（降脂药）。 | 医院体检系统有自动处方建议功能：当 LDL-C > 4.0 mmol/L 时，系统自动建议"降脂治疗"并生成预处方。药房根据系统的预处方配了阿托伐他汀钙片 20mg。药房配药记录 (pharmacy-dispensing-record.md) 显示：处方来源"体检系统自动建议"，不是陈医生的手动处方。陈医生实际上在邮件中明确说"不需要用药，复查即可。" | 药房配了药。陈医生说不需要用药（但赵磊没读邮件）。 |
| W1, Day 5 | 赵磊终于读了陈医生的邮件（W1D2发��的）。邮件解释了校准偏差。 | 陈医生的邮件 (doctor-email-thread.md) 发送于 W1D2 17:00，内容："赵先生，您好。我们发现 10 月 1-5 日期间 Beckman AU5800 化验仪的 LDL-C 模块存在校准偏差，测量值系统性偏高约 0.8-1.0 mmol/L。您的检测日期在此范围内。校正后您的 LDL-C 预计约 3.2-3.4 mmol/L，属正常/临界范围，不需要药物治疗。建议 1 个月后复查确认。如有疑问请回复此邮件。" 赵磊在 W1D5 才读到这封邮件。 | 赵磊现在知道了校准偏差。但他已经取了药，母亲已经恐慌，整个情况已经escalate了。 |
| W2, Day 1 (Update 1 trigger) | 赵磊把陈医生的邮件转发给母亲，并告知药房配药情况。 | 赵磊试图让母亲冷静：邮件说是仪器问题，不需要用药。但母亲不完全相信："仪器校准问题？那为什么药房还给你开了药？宁可信其有，先吃药观察。" 母亲的逻辑：药房开药 = 有医学依据 → 应该吃药。但实际上药房是根据系统自动建议配药，不是医生判断。 | 母亲部分接受但仍怀疑。赵磊夹在医生和母亲之间。 |
| W2, Day 2 (Update 2 trigger) | 赵磊联系陈医生确认：是否需要吃药？药房开的处方是否有效？ | 陈医生回复："阿托伐他汀是体检系统自动建议的预处方，不是我开的。您的校正后 LDL 约 3.2-3.4，不需要药物治疗。请不要服用。1 个月后复查 LDL 即可。如果复查仍偏高，再讨论药物方案。" 陈医生还提供了校准偏差的技术文件摘要。 | 陈医生明确否定用药需求。药房处方来源是系统而非医生。 |
| W2, Day 3 (Update 3 trigger) | 赵磊把陈医生的回复给母亲看。母亲仍不完全放心但接受"先复查"方案。 | 母亲最终说："好吧，先复查。但你要注意饮食，少吃油腻的。你爸那时候要是早发现早控制就好了。" 母亲从恐慌转为关切但不再坚持用药。 | 初步解决。等待复查。 |
| W2, Day 5 (Update 4 trigger) | 赵磊收到医院的复查预约确认和校准偏差的正式通报。 | 医院正式通报：确认 10/1-10/5 期间 LDL-C 检测存在系统性偏差，所有受影响患者将获得免费复查。赵磊的复查预约：11 月 15 日。通报还附带了 Beckman AU5800 的校准报告摘要，技术性地解释了偏差原因（试剂批次更换后未及时校准）。 | 全部真相确认。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 赵磊 (Protagonist)
- **Objective position:** 赵磊的LDL可能在正常/临界范围。仪器校准偏差是唯一的异常原因。他忽略了陈医生的邮件几天，导致信息延迟和不必要的焦虑。
- **Private narrative:** 被母亲的恐慌影响，一度考虑是否真的遗传了父亲的高胆固醇。数据驱动思维让他想找到"确定性答案"但面对医学不确定性不适应。

### 母亲 (P204, Retired Cardiologist)
- **Objective position:** 母亲的家族史担忧从医学角度不完全无理，但她过度将当前情况与赵父的病史类比。她不知道仪器校准问题。
- **Public narrative (SMS/电话):** "你爸当年也是这样开始的...你赶紧吃药...宁可信其有。"
- **Why the gap exists:** 母亲的专业背景让她的判断看起来权威，但她基于不完整信息（不知道校准偏差）做出了过度反应。

### 陈医生 (P216, Attending Physician)
- **Objective position:** 陈医生是最可靠的信息源。他及时发现了校准偏差并通知了患者，解释了不需要用药，提供了技术文件。他的邮件是客观、准确的。
- **Public narrative (邮件):** 专业、清晰、直接说明校准问题和建议。

### 药房
- **Objective position:** 药房根据医院体检系统的自动预处方配药，技术上没有违规——系统生成了处方建议，药房执行了。但系统的自动建议基于未校正的LDL值，本不应被执行。

---

## 4. Contradiction Map

| ID | Contradiction | Source A | Source B | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Health app says "normal" vs hospital flags "LDL elevated." | health-app-summary.md (initial): "各项健康指标正常。心率、血压、睡眠均在健康范围内。" Overall status: ✅ 正常. | hospital-lab-results.md (initial): LDL-C = 4.2 mmol/L ↑偏高 (ref < 3.4). 其他血脂指标正常. | Both are technically correct within their scope: the health app only monitors what wearable devices can measure (heart rate, BP, sleep, steps) — it does NOT measure blood lipids. The hospital lab measures blood lipids but the specific LDL reading is inflated by ~0.8-1.0 mmol/L due to instrument calibration drift. Neither source is "wrong" — they have different scopes and one has a measurement error. | R1 onwards | **Yes: R1-->R5** (calibration explanation resolves) |
| C2 | Mother says "your father had the same thing" (implying genetic risk) vs doctor says "calibration artifact, no clinical significance." | 母亲 SMS (Phase 1, Loop 3): "你爸55岁的时候就是先LDL高，后来冠心病做了支架。这是遗传的，你赶紧去看医生开他汀。" | doctor-email-thread.md (initial, but read by 赵磊 only on W1D5): "校正后您的 LDL-C 预计约 3.2-3.4 mmol/L，属正常/临界范围，不需要药物治疗...校准偏差导致测量值系统性偏高约 0.8-1.0 mmol/L。" | Mother's genetic concern is medically legitimate as a risk factor, but her conclusion ("start statins now") is premature because (1) the current LDL reading is artificially elevated by calibration error, (2) the corrected value is normal/borderline, (3) family history alone does not mandate immediate medication without confirmed elevated LDL. The doctor's assessment is correct: recheck in 1 month, no medication now. | R3 (mother's panic); R5 (doctor's explanation) | **Yes: R3-->R5** |
| C3 | Appointment and checkup timeline (NON-CONFLICT — calendar, app records, hospital report dates all consistent). | health-app-summary.md: checkup date 2026-10-03. health-tracking-notes.md: "10/3 体检" entry. | hospital-lab-results.md: sample collection date 2026-10-03. doctor-email-thread.md: sent 2026-10-04 (next day). calendar entries consistent. | All timeline sources agree: checkup on Oct 3, results on Oct 4, doctor email on Oct 4, 赵磊 reads email on Oct 8 (W1D5). No contradictions in timing. The challenge is synthesis. | R1 onwards | **None** |
| C4 | Pharmacy dispensed lipid medication vs doctor says "no medication needed." | pharmacy-dispensing-record.md (initial): Dispensed: 阿托伐他汀钙片 20mg, 30天用量. 处方来源: "体检系统自动建议." Date: 2026-10-07. | doctor-email-thread.md (initial): "不需要药物治疗。建议1个月后复查确认。" Also: Update 2 doctor reply: "阿托伐他汀是体检系统自动建议的预处方，不是我开的。请不要服用。" | The pharmacy dispensed medication based on the hospital system's auto-generated prescription (triggered by LDL > 4.0), NOT based on the doctor's judgment. The doctor explicitly says no medication is needed. The auto-prescription system did not account for the calibration error. | R4 (pharmacy record visible); R7 (doctor clarifies auto-prescription) | **Yes: R4-->R7** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: 赵磊-母亲 SMS — Agent gives undue weight to family history

- **Session and Loop:** 赵磊-母亲 SMS, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "母亲's concern about familial hypercholesterolemia is medically significant — given 赵磊's father's history of coronary artery disease at age 55, the elevated LDL-C of 4.2 mmol/L in the hospital report aligns with a genetic predisposition pattern that warrants immediate clinical attention and possibly statin therapy."
- **Why the agent is misled:** Mother is a retired cardiologist — her professional background gives her opinion significant credibility. The family history (father with CAD at 55) is a genuine risk factor. The agent weights her medical expertise highly and the LDL reading of 4.2 appears genuinely concerning. The doctor's calibration email exists but has not been foregrounded.
- **Reversal trigger:** Update 1 foregrounds the doctor's calibration explanation, showing the 4.2 is artifactual (true LDL ~3.2-3.4).
- **Affected eval rounds:** R3 (bias visible), R5 (reversed)

### B2: Pharmacy-doctor contradiction — Agent treats pharmacy dispensing as medical validation

- **Session and Loop:** Main session, Phase 1, Loop 5
- **Exact phrase that must appear in session:**
  > "The pharmacy dispensing record shows atorvastatin 20mg was dispensed based on a prescription linked to 赵磊's checkup results — the fact that a licensed pharmacy filled this prescription provides additional clinical validation that the LDL elevation may require pharmacological intervention."
- **Why the agent is misled:** Pharmacies are licensed healthcare providers; a filled prescription appears to confirm medical necessity. The agent does not initially distinguish between a doctor-written prescription and a system-generated auto-suggestion. The phrase "处方来源: 体检系统自动建议" is in the pharmacy record but is easy to overlook.
- **Reversal trigger:** Update 2 delivers the doctor's explicit clarification that the prescription is system-generated, not his.
- **Affected eval rounds:** R4 (bias visible), R7 (reversed)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (app vs hospital) | — | R1, R2 | No | Agents may assume the app and hospital contradict each other, missing that they measure different things (wearables vs blood lab). |
| T2 | C1 (calibration resolves) | — | R1-->R5 | **Yes** | After calibration explanation, both sources are correct within scope — the hospital's LDL is a measurement artifact, not true elevation. |
| T3 | C2 (family history) | B1 | R3 | No | Agents will weight mother's medical authority and the family history, endorsing the genetic risk interpretation. |
| T4 | C2 (calibration reversal) | B1 | R3-->R5 | **Yes** | After calibration data, the LDL is ~3.2-3.4 (normal/borderline), making the genetic risk interpretation premature. |
| T5 | C3 (timeline, non-conflict) | — | R1 onwards | No | Timeline synthesis across health app, hospital, doctor email, pharmacy dates. |
| T6 | C4 (pharmacy vs doctor) | B2 | R4, R7 | **Yes** | Agents may treat the pharmacy dispensing as medical validation without checking the "处方来源" field (system auto-suggestion, not doctor). |
| T7 | Comprehensive | B1, B2 | R21-R30 | Comprehensive | Full resolution: calibration artifact, family history premature, pharmacy auto-prescription, no medication needed. |

---

## 7. Writer Constraints

1. **Only contradictions C1–C4.** No additional health scares or character conflicts.
2. **B1 and B2 exact phrases** verbatim in specified loops.
3. **Medical figures consistent:** Reported LDL: 4.2 mmol/L. Calibration offset: +0.8–1.0 mmol/L. Corrected LDL: ~3.2–3.4 mmol/L. Reference range: < 3.4 mmol/L. Other lipids: HDL 1.5, TG 1.2, TC 5.1 (all normal). Medication: atorvastatin 20mg. Instrument: Beckman AU5800. Affected dates: 2026-10-01 to 2026-10-05. Checkup date: 2026-10-03.
4. **母亲's medical background** must be convincing — she's not a layperson, she's a retired cardiologist. Her concerns are grounded but based on incomplete information.
5. **陈医生's emails** are professional, clear, and provide the definitive correct information.
6. **Pharmacy record** must show "处方来源: 体检系统自动建议" — this detail is the key to distinguishing system prescription from doctor prescription.
7. **C3 (timeline) is NON-CONFLICT.**
8. **All data in Chinese (simplified).** Eval in English.
9. **P1-P5 personalization** per 赵磊.
10. **exec_check 20-40% of rounds.**
