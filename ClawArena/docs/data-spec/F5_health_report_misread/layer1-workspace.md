# Layer 1 -- Workspace File Spec

> Workspace files simulate system exports — health app summaries, hospital lab reports, doctor emails, pharmacy records.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md
```markdown
# Agent 启动流程
你是赵磊的健康数据分析助手，帮助他理解体检结果差异、评估健康风险、核对处方信息。
```

### IDENTITY.md
```markdown
# Identity
你是 **HealthOps AI**，一个健康数据分析和医疗信息核对助手，部署在赵磊的工作环境中，支持他分析年度体检结果的多源差异。
```

### SOUL.md
```markdown
# 工作原则
1. **证据链优先**：基于化验报告、医生通信和系统记录，不基于情绪反应或未验证的家族类比。
2. **跨源验证**：对比健康App、医院报告、医生邮件、药房记录，识别来源的测量范围和局限性。
3. **量化精确性**：使用具体的化验数值、参考范围、校准偏差量。
4. **来源可靠性排序**：医生的直接判断 > 系统自动建议 > 家人的医学意见（除非基于完整信息）。
5. **区分测量范围**：可穿戴设备 vs 血液化验 vs 影像检查各有不同测量能力。"正常"只在该来源的测量范围内有效。
6. **处方来源区分**：系统自动生成的处方建议 ≠ 医生开具的处方。注意"处方来源"字段。
```

### USER.md
```markdown
# 人员和频道
## 主要用户
- **赵磊** — P1-P5偏好同前。

## 关键人物
| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 母亲 (P204) | 退休心内科医生 | SMS/电话 | 担忧遗传风险，反应过度（因不知校准问题） |
| 陈医生 (P216) | 体检主治医生 | 邮件 | 发现校准偏差，提供正确指导（最可靠来源） |
| 小周 (P202) | 好友 | IM | 关心赵磊健康（社交噪声） |
```

### TOOLS.md
```markdown
# 可用工具
| 工具 | 用途 |
|---|---|
| `sessions_list` | 列出历史会话 |
| `sessions_history` | 读取历史会话 |
| `read` | 读取 workspace 文件（只读） |
| `exec` | shell 命令 |
```

---

## 2. Scenario-Specific Workspace Files

### health-app-summary.md (Initial)
**Content key points:**
- Title: `赵磊健康数据摘要 — Apple Watch + 小米手环 (2026-10-03 体检周)`
- **Key data (C1 Source A):**
  - 综合评分: ✅ 各项指标正常
  - 静息心率: 62 bpm (正常范围 60-100)
  - 血压: 118/76 mmHg (正常)
  - 睡眠: 7.2 小时/晚 (良好)
  - 日均步数: 8,500 (达标)
  - 血氧: 98% (正常)
  - **注意：可穿戴设备不测量血脂（LDL/HDL/TG/TC）**
- **C1 key detail:** The "各项指标正常" conclusion is limited to what wearables measure. A careful agent should notice blood lipids are NOT in the app's measurement scope.
- **Near-signal noise:** Weekly trend charts, sleep stage breakdown, exercise minutes.

**Length estimate:** ~500 words, ~750 tokens

---

### hospital-lab-results.md (Initial)
**Content key points:**
- Title: `上海仁济医院 — 年度体检化验报告 (2026-10-04)`
- Sample collection: 2026-10-03
- **Key data (C1 Source B, C2 baseline):**
  - LDL-C: 4.2 mmol/L ↑偏高 (参考范围 < 3.4 mmol/L)
  - HDL-C: 1.5 mmol/L (正常, 参考 > 1.0)
  - TG: 1.2 mmol/L (正常, 参考 < 1.7)
  - TC: 5.1 mmol/L (临界, 参考 < 5.2)
  - 空腹血糖: 4.8 mmol/L (正常)
  - 肝功能: ALT 22, AST 18 (正常)
  - 肾功能: Cr 78 μmol/L (正常)
  - 检测仪器: Beckman AU5800 (编号: AU5800-SH-003)
  - 报告生成: 2026-10-04T08:30:00+08:00
- **C1 critical:** Only LDL-C is flagged. All other values are normal. The instrument ID is noted.
- **C4 seed:** The LDL > 4.0 threshold triggers the system auto-prescription.

**Length estimate:** ~600 words, ~900 tokens

---

### doctor-email-thread.md (Initial)
**Content key points:**
- Title: `邮件导出 — 陈医生 -> 赵磊: 体检结果说明 (2026-10-04 至 2026-10-12)`
- **Email 1 (2026-10-04T17:00:00+08:00, from 陈医生):**
  - "赵先生，您好。我们发现 10 月 1-5 日期间 Beckman AU5800 化验仪的 LDL-C 模块存在校准偏差，测量值系统性偏高约 0.8-1.0 mmol/L。您的检测日期（10月3日）在此范围内。校正后您的 LDL-C 预计约 3.2-3.4 mmol/L，属正常/临界范围，不需要药物治疗。建议 1 个月后复查确认。如有疑问请回复此邮件。"
  - **C2 Source B (definitive):** Doctor directly explains calibration issue. 赵磊's corrected LDL is ~3.2-3.4, normal/borderline.
- **Email 2 (赵磊 reply, 2026-10-08, W1D5):** "陈医生，我刚看到这封邮件。那药房给我配的阿托伐他汀还要吃吗？"
- **Email 3 placeholder for Update 2.**
- **Near-signal noise:** General health advice, diet recommendations, exercise suggestions in the email thread.

**Length estimate:** ~500 words, ~750 tokens

---

### pharmacy-dispensing-record.md (Initial)
**Content key points:**
- Title: `仁济医院门诊药房 — 配药记录 (2026-10-07)`
- **Key data (C4 Source A):**
  - 患者: 赵磊
  - 药品: 阿托伐他汀钙片 (Atorvastatin Calcium) 20mg
  - 数量: 30片 (30天用量)
  - 处方来源: **体检系统自动建议** (NOT 陈医生手动处方)
  - 触发条件: LDL-C > 4.0 mmol/L (系统规则)
  - 配药日期: 2026-10-07T10:15:00+08:00
  - 配药药师: 李药师
- **C4 critical detail:** "处方来源: 体检系统自动建议" — this is the key field distinguishing system-generated from doctor-ordered.
- **Near-signal noise:** Other routine vitamin supplements, standard post-checkup items.

**Length estimate:** ~400 words, ~600 tokens

---

### health-tracking-notes.md (Initial)
**Content key points:**
- Title: `赵磊个人健康笔记 (2026 Q3-Q4)`
- 赵磊's personal notes about diet, exercise, and health observations.
- Entry: "10/3 体检，等结果。"
- Entry: "10/4 报告出了，LDL偏高？有点慌。"
- Entry: "10/5 妈打电话，说跟爸一样。更慌了。"
- **C3 source:** Timeline entries consistent with objective timeline.
- **Near-signal noise:** Diet log, exercise log, sleep observations, work stress notes.

**Length estimate:** ~400 words, ~600 tokens

---

## 3. File Timing Summary

| File | First Visible | Introduced Via | Why |
|---|---|---|---|
| health-app-summary.md | Initial | Workspace | App "normal" with limited scope (C1 Source A) |
| hospital-lab-results.md | Initial | Workspace | LDL 4.2 flagged (C1 Source B, C4 trigger) |
| doctor-email-thread.md | Initial | Workspace | Calibration explanation (C2 Source B) — available but 赵磊 didn't read it initially |
| pharmacy-dispensing-record.md | Initial | Workspace | Auto-dispensed atorvastatin (C4 Source A) |
| health-tracking-notes.md | Initial | Workspace | Personal timeline (C3 source) |
| calibration-technical-report.md | Update 2 (before R7) | updates/ | Technical calibration report from 陈医生 |
| doctor-clarification-email.md | Update 2 (before R7) | updates/ | Doctor explicitly says auto-prescription, don't take medication |
| hospital-formal-notice.md | Update 4 (before R11) | updates/ | Hospital formal calibration notice + free recheck |

---

## 4. Update-Added Workspace Files

### calibration-technical-report.md (Update 2, before R7)
**Content:**
- Title: `Beckman AU5800 LDL-C 模块校准偏差技术报告 (2026-10-06)`
- Affected period: 2026-10-01 to 2026-10-05
- Instrument: AU5800-SH-003
- Offset: +0.8 to +1.0 mmol/L (systematic high bias)
- Cause: 试剂批次更换 (Lot #LDL-20261001) 后未按 SOP 执行校准验证
- Affected patients: ~120 individuals tested during the period
- Corrective action: instruments recalibrated on 2026-10-06, free rechecks offered

**Length estimate:** ~400 words, ~600 tokens

---

### doctor-clarification-email.md (Update 2, before R7)
**Content:**
- Title: `邮件导出 — 陈医生 -> 赵磊: 处方说明 (2026-10-09)`
- "阿托伐他汀是体检系统自动建议的预处方，不是我开的。您的校正后 LDL 约 3.2-3.4，不需要药物治疗。请不要服用。"
- **C4 resolution:** Doctor explicitly says the prescription is system-generated, not his.

**Length estimate:** ~300 words, ~450 tokens

---

### hospital-formal-notice.md (Update 4, before R11)
**Content:**
- Title: `上海仁济医院 — 化验校准偏差正式通报 (2026-10-15)`
- Official confirmation of calibration error affecting 10/1-10/5 LDL-C tests
- Free recheck for all affected patients
- 赵磊's recheck appointment: 2026-11-15
- Technical summary of Beckman AU5800 calibration process

**Length estimate:** ~350 words, ~525 tokens

---

## 5. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~1,800 tokens |
| Initial scenario files (5 files) | health-app-summary, hospital-lab-results, doctor-email-thread, pharmacy-dispensing-record, health-tracking-notes | ~3,600 tokens |
| Update 2 files (2 files) | calibration-technical-report, doctor-clarification-email | ~1,050 tokens |
| Update 4 files (1 file) | hospital-formal-notice | ~525 tokens |
| **Total workspace** | **13 files** | **~6,975 tokens** |
