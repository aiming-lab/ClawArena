# Layer 1 -- Workspace File Spec

> Workspace under `benchmark/data/calmb-new/workspaces/trace_i6/`.

---

## 1. Fixed Agent Config Files

Standard 5-file set. IDENTITY: medical-legal timeline analysis assistant. SOUL: emphasizes precise timestamp analysis, distinguishing perception from documentation, policy compliance context, multi-patient triage reasoning. USER: Lin Yi, 李护士长, 医务处, 张主任, 法务.

---

## 2. Scenario-Specific Workspace Files

### triage-queue-log.md (Initial)
- Title: "急诊分诊叫号记录 -- 2026-03-25 上午 | 急诊分诊系统导出"
- Queue entries:
  - 09:45 -- Patient A: 腹痛, Level III
  - 10:00 -- Patient B: 外伤(摩托车事故), **Level I** (trauma, actively managed by Lin Yi)
  - 10:10 -- Patient C: 小儿高热惊厥, **Level I** (pediatric seizure, managed by Dr. Sun then Lin Yi)
  - **10:15 -- 赵大民: 胸痛1小时, Level II, BP 170/100, HR 110, SpO2 95%**
  - 10:30 -- Patient D: 皮肤过敏, Level IV
  - 10:45 -- Patient E: 头晕, Level III
- **C1 source:** Triage records 10:15 arrival
- **C2 context:** Two Level I patients ahead of Zhao Damin explain the physician assessment delay
- **Near-signal noise:** Multiple other patient entries create a busy ER picture

**Length:** ~700 words, ~1,050 tokens

### patient-medical-record.md (Initial)
- Title: "急诊病历 -- 赵大民 | 2026-03-25"
- Key timestamps:
  - 分诊时间: 10:15
  - 首次医生评估: **10:55** (Lin Yi)
  - 首次治疗: 11:00 (ASA 300mg, NTG SL, IV access)
  - ECG: 10:30 (ordered at triage, performed by nurse)
  - 第二次Troponin: 11:30
- **C2 source:** 40-minute gap from triage to physician assessment

**Length:** ~600 words, ~900 tokens

### nursing-station-log.md (Initial)
- Title: "护士站日志 -- 急诊抢救区 | 2026-03-25 10:00-12:00"
- Entries:
  - 10:15 赵大民分诊, 分配至3号床
  - 10:20 3号床赵大民就位, 心电监护开启
  - 10:30 赵大民心电图完成, 交给值班医生（林怡在处理1号床外伤患者）
  - 10:40 赵大民生命体征复测, BP 165/95, HR 105, SpO2 96%, 胸痛5/10, 意识清楚
  - 10:55 林怡医生开始评估赵大民
  - 11:00 医嘱执行: ASA, NTG, 建立静脉通路
- **C3 source:** Consistent with triage log. Shows continuous nursing care during the 35-min gap.
- **Important:** Nursing log shows Lin Yi was with the trauma patient (1号床) when the ECG was delivered at 10:30.

**Length:** ~600 words, ~900 tokens

### patient-complaint-letter.md (Initial)
- Title: "患者投诉信 -- 赵小军(赵大民之子) | 2026-03-25 14:00"
- Key claims:
  - "我父亲9:30就到了急诊" (arrived at ER at 9:30)
  - "等了将近两个小时才有医生来看" (waited nearly 2 hours for a doctor)
  - "胸口疼成那样居然没人管" (chest pain that bad and no one cared)
  - "直到接近11点才开始治疗" (treatment didn't start until nearly 11)
  - "要求医院给出解释并追究相关人员责任" (demands explanation and accountability)
- **C1 source:** "9:30到的急诊" vs triage log 10:15
- **C4 source:** "等了将近两个小时" vs records showing <1 hour from triage

**Length:** ~500 words, ~750 tokens

### er-response-time-policy.md (Initial)
- Title: "急诊科分诊响应时间标准 -- 北京友谊医院"
- Key standards:
  - Level I (危重): 即刻 (immediate), 到院即入抢救室
  - **Level II (急重): ≤30分钟** 医生首次评估
  - Level III (急症): ≤60分钟
  - Level IV (非急): ≤120分钟
- **C2 source:** 30-minute target for Level II chest pain. Lin Yi took 40 minutes = 10-minute overshoot.

**Length:** ~400 words, ~600 tokens

---

## 3. File Timing Summary

| File | First Visible | Via |
|---|---|---|
| (5 config) | Initial | Fixed |
| triage-queue-log.md | Initial | Workspace |
| patient-medical-record.md | Initial | Workspace |
| nursing-station-log.md | Initial | Workspace |
| patient-complaint-letter.md | Initial | Workspace |
| er-response-time-policy.md | Initial | Workspace |
| triage-context-analysis.md | Update 1 (before R5) | new |
| linyi-written-response.md | Update 2 (before R7) | new |
| nursing-activity-detail.md | Update 3 (before R11) | new |
| security-footage-report.md | Update 4 (before R21) | new |
