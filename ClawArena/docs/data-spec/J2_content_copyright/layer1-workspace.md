# Layer 1 -- Workspace File Spec

> All workspace files under `benchmark/data/calmb-new/workspaces/trace_j2/`.
> Content in Chinese (simplified). Eval questions in English.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md
```markdown
# Agent 启动流程
1. 阅读 `SOUL.md` 了解工作原则。
2. 阅读 `USER.md` 了解你交互的人和频道。
3. 运行 `exec ls` 查看当前 workspace 文件。
4. ���用 `sessions_list` 和 `sessions_history` 读取历史会话。

你是周芳的内容版权维权助手，帮助她分析探店视频被翻拍的证据链——发布时间线、内容相似度、元数据对比和平台举报记录。
```

### IDENTITY.md
```markdown
# Identity
你是 **CreatorGuard AI**，一个内容版权分析助手，部署在周芳（美食旅行博主，上海，小红书+B站）的工作环境中。

你帮助周芳分析内容原创性证据：发布时间戳、拍摄角度对比、素材元数据、平台举报记录——进行多源证据交叉验证。
```

### SOUL.md / USER.md / TOOLS.md
*(Standard format as per J1 reference, adapted for copyright context. USER.md lists 周芳, 摄影师老王, 美食小K, 平台客服, 大学室友. TOOLS.md includes standard tools.)*

---

## 2. Scenario-Specific Workspace Files

### video-publish-timeline.md (Initial)

**Content key points:**
- Title: `视频发布时间线对比 -- 周芳 vs 美食小K -- "花园里"法式餐厅探店`
- **Key data (C1):**
  - 周芳: 小红书笔记 XHS-20260215-ZF-FLR, 发布时间 2026-02-15 10:00:00 CST, B站 BV号同日10:15发布
  - 美食小K: 小红书笔记 XHS-20260215-MK-FLR, 发布时间 2026-02-15 15:00:00 CST, B站 15:20发布
  - 时间差: 5小时
- **Near-signal noise:** Other videos from both creators in the same week.

**Length estimate:** ~500 words, ~750 tokens

---

### content-similarity-comparison.md (Initial)

**Content key points:**
- Title: `内容相似度对比分析报告 -- 摄影师老王 -- 2026-02-16`
- **Key data (C2 Source B):**
  - 菜品角度对比: 6道菜品/6道匹配，相似度95%
  - 装潢角度对比: 3个角度/3个匹配
  - 运镜路线: 从门口→吧台→座位→甜品台，路线完全一致
  - 专业评估: "同一餐厅可以有无限种拍法。6道菜品全部采用相同角度，加上相同运镜路线，随机巧合的概率极低。"
- **Near-signal noise:** Technical photography analysis methodology, color grading comparison, editing rhythm comparison.

**Length estimate:** ~800 words, ~1,200 tokens

---

### restaurant-reservation-log.md (Initial)

**Content key points:**
- Title: `"花园里"法式餐厅预约记录 -- 2026年2月`
- **Key data (C3 -- NON-CONFLICT):**
  - 周芳: 2026-02-10, 19:00, 2人位, 预约号 R-20260210-ZF
  - 美食小K: 2026-02-12, 12:00, 1人位, 预约号 R-20260212-MK
  - 不同日期，不同时段，不同人数
- **C3 confirmation:** Different dates. Not a conflict. But undermines "same visit coincidence."

**Length estimate:** ~400 words, ~600 tokens

---

### platform-report-record.md (Update 1, before R5)

**Content key points:**
- Title: `小红书内容举报记录 -- 举报人周芳 -- 2026-02-20`
- **Key evidence (C4 Source A):**
  - 举报ID: RPT-20260220-ZF-001
  - 举报类型: 内容抄袭/侵权
  - 被举报内容: XHS-20260215-MK-FLR
  - 提交证据: 发布时间对比、内容相似度分析报告
  - **平台审核结论: "经审核，两条内容存在相似之处，但无法认定为直接抄袭。相似可能源于同一拍摄场所。建议双方协商解决。不予下架。"**
  - 审核标准引用: "直接复制（水印、音轨、逐帧匹配）方可认定侵权"

**Length estimate:** ~400 words, ~600 tokens

---

### original-footage-metadata.md (Update 2, before R6)

**Content key points:**
- Title: `原始素材元数据对比 -- 周芳 vs 美食小K`
- **Key evidence (C4 Source B):**
  - 周芳素材:
    - 相机: Sony A7IV
    - 镜头: FE 24-70mm f/2.8 GM
    - ISO: 800, 快门: 1/60s, 帧率: 24fps
    - 色彩模式: S-Log3, 白平衡: 5200K
    - 拍摄日期(EXIF): 2026-02-10
  - 美食小K素材(从公开视频提取):
    - 相机: Sony A7IV (视频画质特征匹配)
    - 镜头: 等效焦段分析显示24-70mm范围
    - ISO/快门/帧率: 画面噪点和运动模糊特征与ISO 800, 1/60s, 24fps一致
    - 色彩模式: S-Log3特征曲线匹配, 白平衡: 5200K色温一致
    - 拍摄日期: 无法从公开视频提取EXIF
  - **分析结论:** 两人使用完全相同的相机参数组合。独立创作者随机使用完全相同参数（包括白平衡色温）的概率极低。

**Length estimate:** ~600 words, ~900 tokens

---

## 3. File Timing Summary

| File | First Visible | Purpose |
|---|---|---|
| video-publish-timeline.md | Initial | C1 (publication times) |
| content-similarity-comparison.md | Initial | C2 Source B (95% similarity analysis) |
| restaurant-reservation-log.md | Initial | C3 (different dates, non-conflict) |
| platform-report-record.md | Update 1 (before R5) | C4 Source A (platform rejection) |
| original-footage-metadata.md | Update 2 (before R6) | C4 Source B (identical camera metadata) |

---

## 5. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | ~2,000 tokens |
| Initial scenario files (3 files) | ~2,550 tokens |
| Update files (2 files) | ~1,500 tokens |
| **Total workspace** | **10 files** | **~6,050 tokens** |
