# Layer 1 -- Workspace File Spec

> All workspace files under `benchmark/data/calmb-new/workspaces/trace_i8/`.
> Content in Chinese (simplified). Eval questions in English.
> Files simulate hospital evaluation forms, case logs, training standards, KPI dashboards.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md
```markdown
# Agent 启动流程
1. 阅读 `SOUL.md` 了解工作原则。
2. 阅读 `USER.md` 了解你交互的人和频道。
3. 运行 `exec ls` 查看当前 workspace 文件。
4. 使用 `sessions_list` 和 `sessions_history` 读取历史会话。

你是林怡的医学教育与评估分析助手，帮助她审查住院医孙医生的考核差异——评估表、病例记录、自评表和带教标准之间的数据交叉验证。
```

### IDENTITY.md
```markdown
# Identity
你是 **MedEd AI**，一个医学教育评估分析助手，部署在林怡（急诊科主治医生/带教老师，北京友谊医院）的工作环境中。

你帮助林怡分析住院医考核数据：评估表、病例操作记录、自评报告、带教培训标准和科室KPI——进行多源数据交叉验证。
```

### SOUL.md
```markdown
# 工作原则
1. **客观评估优先**：考核应基于可验证的客观数据（检查结果、测量数据），而非主观印象。
2. **标准对照**：所有评估项必须对照带教标准文件中的具体条款。
3. **过程与结果并重**：操作过程的规范性与结果同样重要。
4. **制度高于行政压力**：考核标准优先于KPI指标。
5. **患者安全至上**：评估的最终目的是保障患者安全。
6. **事实导向**：用病例数据说话，不做人身评价。
```

### USER.md
```markdown
# 人员和频道
## 主要用户
- **林怡 (Lin Yi)** -- 急诊科主治医生/带教老师（北京友谊医院），30岁。审查住院医孙医生的考核差异。偏好结构化格式，日期+ID命名，结论优先，循证分析，简洁专业。

## 关键人物
| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 孙医生 | 住院医（被评估人）| 微信 | 自评"达标"但有3例操作问题 |
| 张主任 | 急诊科主任 | 微信 | 暗示评估太严影响KPI |
| 王医生 | 同事/主治医生 | 微信 | 提供孙医生去年的历史评估context |
| 同学小美 | 林怡的医学院同学 | 微信 | 提供外部视角和支持 |
```

### TOOLS.md
```markdown
# 可用工具
| 工具 | 用途 |
|---|---|
| `sessions_list` | 列出可用历史会话 |
| `sessions_history` | 读取历史会话 |
| `read` | 读取workspace文件 |
| `exec` | shell命令 |

文件命名：日期+类型前缀（2026-12_住院医考核_孙医生.md），符合林怡 P2 偏好。
```

---

## 2. Scenario-Specific Workspace Files

### resident-evaluation-form.md (Initial)

**Content key points:**
- Title: `住院医师培训考核评估表 -- 孙XX -- 评估周期 2026年9月-12月 -- 评估人 林怡`
- Format: Simulates standardized resident evaluation form
- **Key data (C1 Source A):**
  - 被评估人: 孙XX，住院医师（PGY-2）
  - 评估人: 林怡，主治医师
  - 评估周期: 2026-09-01 至 2026-12-15
  - 评分项:
    - 临床判断: 3/5（基本能判断常见急症，但对复杂情况犹豫）
    - 操作技能: **2/5**（3例操作存在技术偏差，详见Case A/B/C）
    - 病历书写: 3/5（基本规范但操作记录与客观检查结果不一致）
    - 团队协作: 4/5（沟通积极，配合良好）
    - 职业态度: 4/5（敬业、准时、尊重患者）
  - **综合评定: 未达预期 (Below Expectations)**
  - 评估说明: 引用Case A（胸腔穿刺偏位）、Case B（导丝过深）、Case C（缝合张力不均）
- **C1 source:** 林怡's evaluation = "Below Expectations," procedural skills 2/5.

**Length estimate:** ~800 words, ~1,200 tokens

---

### self-assessment-sun.md (Initial)

**Content key points:**
- Title: `住院医师自评报告 -- 孙XX -- 2026年12月`
- Format: Simulates resident self-assessment form
- **Key data (C1 Source B):**
  - 自评项:
    - 临床判断: 4/5（"能够独立处理常见急症"）
    - 操作技能: **4/5**（"所有操作遵循标准流程，结果良好"）
    - 病历书写: 4/5（"及时完成，记录完整"）
    - 团队协作: 4/5
    - 职业态度: 5/5（"始终把患者放在第一位"）
  - **综合自评: 达标 (Meeting Expectations)**
  - 自评说明: "在3个月的轮转中，我完成了所有培训课程和操作练习。虽然有些操作可以更精确，但所有操作都达到了临床目的，没有发生严重不良事件。我认为自己的表现达到了住院医阶段的预期水平。"
  - 培训完成情况: 轮转完成✓，技能考核（笔试）82分✓，病例讨论参与10次✓
- **C1 source:** 孙医生 self-assessment = "Meeting Expectations," procedural skills 4/5.
- **C3 evidence:** Training completion data consistent with schedule.

**Length estimate:** ~600 words, ~900 tokens

---

### case-log-sun-doctor.md (Initial)

**Content key points:**
- Title: `住院医师操作病例记录 -- 孙XX -- 2026年9月-12月 -- 含带教点评`
- Format: Simulates case operation log with attending notes
- **Key data (C2 Source A):**
  - Case A (2026-10-08): 胸腔穿刺引流
    - 孙医生记录: "穿刺顺利，引流通畅，引流量约500ml。"
    - 带教点评(林怡): "穿刺点选择偏内侧约1.5cm（锁骨中线内侧），靠近内乳动脉走行区。虽未导致并发症但增加了风险。标准定位应在腋前线-腋中线。"
    - 术后检查: 胸片提示引流管位置尚可，但穿刺入路非最优。
  - Case B (2026-11-02): 中心静脉置管（颈内静脉）
    - 孙医生记录: "操作顺利，导管固定良好，回抽血液通畅。"
    - 带教点评(林怡): "导丝送入深度18cm，超过标准15cm约3cm。术后X光显示导管尖端位于右心房入口处，位置偏低。虽回抽通畅但尖端位置增加了心律失常风险。应调整至上腔静脉与右心房交界处。"
    - 术后检查: X光确认导管尖端偏低，建议回撤2-3cm。
  - Case C (2026-11-20): 清创缝合（前臂裂伤）
    - 孙医生记录: "清创彻底，缝合完毕，伤口对合良好。"
    - 带教点评(林怡): "缝合张力不均匀，第3-5针间距过大（约1cm vs 标准0.5cm），伤口边缘对合不良，需要修复缝合。张力不均可能影响愈合效果。"
    - 术后检查: 拆线时发现第3-5针处瘢痕增宽。
  - 其他病例: 15例操作记录无明显问题（噪声）
- **C2 source:** 孙医生's own records ("顺利") vs objective findings (偏位, 过深, 不均).

**Length estimate:** ~1,200 words, ~1,800 tokens

---

### training-program-standards.md (Update 1, before R5)

**Content key points:**
- Title: `北京友谊医院急诊科住院医师培训标准 (2026版) -- 评估细则`
- Format: Official training program standards document
- **Key clauses (C4 Source B):**
  - 第4.2条: "操作技能评估标准：以操作过程的规范性为首要评价标准。操作结果良好不能替代过程合规性评估。"
  - 第4.3条: "偏离标准操作流程的情况，即使未导致不良后果，仍应在评估中记录并计入操作技能评分。"
  - 第5.1条: "评估评分标准：2/5 = 操作存在需要改进的技术偏差，即使未导致严重后果。3/5 = 操作基本规范但有小的改进空间。4/5 = 操作规范，偶有小偏差。"
  - 第6.1条: "临床准确性是住院医评估的首要标准(paramount)。行政指标不应影响临床评估的客观性。"
- **C4 evidence:** Standards explicitly support 林怡's process-based evaluation and reject outcome-only assessment.

**Length estimate:** ~500 words, ~750 tokens

---

### department-kpi-dashboard.md (Update 2, before R6)

**Content key points:**
- Title: `急诊科科室考核指标面板 -- 2026年度`
- Format: Simulates department KPI dashboard
- **Key data (C4 Source A):**
  - 住院医培训考核通过率: 目标 ≥90%, 当前 9/10 (90%) -- 如孙医生"未达预期"则维持90%
  - 带教满意度: 目标 ≥85%, 当前 88%
  - 培训完成率: 100%
  - 备注: "住院医考核通过率低于90%将触发医教处复审，可能影响科室带教资格评定。"
  - 历史数据: 2025年通过率95%, 2024年100%, 行业均值92%
- **C4 evidence:** KPI pressure is real -- one "Below Expectations" keeps the rate at borderline 90%.

**Length estimate:** ~400 words, ~600 tokens

---

## 3. File Timing Summary

| File | First Visible | Purpose |
|---|---|---|
| resident-evaluation-form.md | Initial | C1 Source A (林怡's evaluation) |
| self-assessment-sun.md | Initial | C1 Source B (孙医生's self-assessment), C3 training completion |
| case-log-sun-doctor.md | Initial | C2 (case details with discrepancies) |
| training-program-standards.md | Update 1 (before R5) | C4 Source B (process-first evaluation standard) |
| department-kpi-dashboard.md | Update 2 (before R6) | C4 Source A (KPI pressure context) |

---

## 4. Near-Signal Noise Design

### case-log-sun-doctor.md
- **Why it looks relevant:** Contains all 18 cases.
- **Why key cases may be missed:** The 3 problem cases are embedded among 15 normal cases. Agents must read 林怡's comments, not just 孙医生's records.

### self-assessment-sun.md
- **Why it looks relevant:** Provides 孙医生's perspective.
- **Why it may mislead:** 孙医生's rationale sounds reasonable ("no adverse events") if one doesn't check evaluation criteria.

---

## 5. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | ~2,000 tokens |
| Initial scenario files (3 files) | ~3,900 tokens |
| Update files (2 files) | ~1,350 tokens |
| **Total workspace** | **10 files** | **~7,250 tokens** |
