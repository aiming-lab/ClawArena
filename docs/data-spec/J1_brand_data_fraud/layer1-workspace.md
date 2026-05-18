# Layer 1 -- Workspace File Spec

> All workspace files under `benchmark/data/calmb-new/workspaces/trace_j1/`.
> Content in Chinese (simplified). Eval questions in English.
> Files simulate platform analytics exports, MCN reports, brand communications, contracts.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md
```markdown
# Agent 启动流程
1. 阅读 `SOUL.md` 了解工作原则。
2. 阅读 `USER.md` 了解你交互的人和频道。
3. 运行 `exec ls` 查看当前 workspace 文件。
4. 使用 `sessions_list` 和 `sessions_history` 读取历史会话。

你是周芳的内容创作数据分析助手，帮助她调查 MCN 数据报告与平台真实数据之间的差异。
```

### IDENTITY.md
```markdown
# Identity
你是 **CreatorOps AI**，一个内容创作者数据分析和合同合规助手，部署在周芳（生活方式博主，成都，小红书+bilibili）的工作环境中。

你帮助周芳分析小红书和 bilibili 创作者后台数据、MCN结案报告、品牌方收到的数据、合同条款——跨私聊（刘姐/MCN、赵敏/品牌方）进行多源数据交叉验证。
```

### SOUL.md
```markdown
# 工作原则
1. **数据溯源优先**：平台官方后台数据（API导出）> MCN报告 > 截图。每个数据点必须追溯到原始来源。
2. **跨源对比**：同一指标在不同来源的差异必须量化（百分比、倍数）并标注。
3. **合同合规**：数据报告必须满足合同约定的"verified data"标准。
4. **模式识别**：单一数据差异可能是误差；跨平台、跨创作者的一致性差异可能是系统性行为。
5. **非对抗原则**：分析聚焦于事实和数据，不做动机推断（除非有直接证据）。
6. **创作者权益**：创作者有权知道自己数据的真实呈现方式。
```

### USER.md
```markdown
# 人员和频道
## 主要用户
- **周芳 (Zhou Fang)** -- 生活方式博主（成都），28岁，小红书+bilibili双平台。调查MCN数据虚报事件。偏好视觉对比（并排表格），平台名前缀命名，关键发现优先，比率和百分比对比，清晰非对抗语言。

## 关键人物
| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 刘姐 | MCN商务对接（星芒传媒）| 微信私聊 | 提交了虚假数据报告；声称"统计口径不同" |
| 赵敏 | 品牌方市场负责人（清新茶饮）| 微信私聊 | 收到了MCN的虚假数据；配合调查 |
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

文件命名：平台名前缀（小红书_分析导出.md, bilibili_分析.md），符合周芳 P2 偏好。
```

---

## 2. Scenario-Specific Workspace Files

### xiaohongshu-analytics-export.md (Initial)

**Content key points:**
- Title: `小红书创作者后台数据导出 -- 周芳 (XHS UID: zf_lifestyle_028) -- 导出日期 2026-03-10`
- Format: Simulates creator backend analytics export with API documentation excerpt
- **Key data (C1 Source A):**
  - 笔记 ID: XHS-20260215-ZF-001
  - 发布日期: 2026-02-15
  - 合作标记: 清新茶饮 (品牌合作笔记)
  - 截至 2026-03-10 数据:
    - 播放量: 50,234
    - 点赞: 3,812
    - 收藏: 1,423
    - 评论: 287
    - 分享: 156
  - 数据增长曲线: Day 1: 5K, Day 7: 28K, Day 14: 42K, Day 18 (Mar 5): 45K, Day 23 (Mar 10): 50K
  - **API 文档摘录 (C2 Source B):** "小红书创作者数据 API v3.2: `note.views` -- 视频笔记的播放量，定义为视频被用户主动播放的次数，包括首页推荐、搜索结果和个人主页访问。此为唯一官方播放统计口径。不存在其他播放量统计维度。"
- **C1 source:** Official backend data = 50,234 views. Ground truth.
- **C2 source:** API doc explicitly states single definition of 播放量.
- **Near-signal noise:** Other notes' analytics, account-level metrics (followers, engagement rate), trending keywords.

**Length estimate:** ~900 words, ~1,350 tokens

---

### mcn-brand-report.md (Initial)

**Content key points:**
- Title: `星芒传媒 -- 清新茶饮 x 周芳 合作复盘报告 (2026年2月) -- 报告日期 2026-03-05`
- Format: Simulates MCN's official brand partnership report
- **Key data (C1 Source B):**
  - 合作创作者: 周芳
  - 平台: 小红书
  - 发布日期: 2026-02-15
  - 核心数据:
    - 小红书视频播放量: 120,000
    - 点赞: 8,500
    - 收藏: 3,200
    - 互动率: 9.3%
  - bilibili 视频播放量: 65,000
  - 数据来源标注: "平台数据统计"
  - 报告落款: "星芒传媒数据分析部"
- **C1 inflated data:** All metrics inflated: views 2.4x (50K->120K), likes 2.2x (3.8K->8.5K), saves 2.2x (1.4K->3.2K)
- **Near-signal noise:** Brand exposure analysis, content performance rating, recommendation for follow-up cooperation, creative brief compliance check, ROI calculation based on inflated numbers.

**Length estimate:** ~700 words, ~1,050 tokens

---

### brand-received-data.md (Update 1, before R5)

**Content key points:**
- Title: `品牌方收到的合作数据材料 -- 转发自赵敏 (2026-03-12)`
- Format: Simulates brand manager forwarding MCN-submitted materials
- **Key evidence (C4 Source B):**
  - 赵敏转发说明: "周芳你好，以下是MCN提交给我们的全部合作数据材料。"
  - 材料清单:
    - 合作复盘报告 PDF (same as mcn-brand-report.md)
    - "小红书数据截图" -- **关键：这是一张图片文件，不是 API 数据导出。截图显示类似小红书后台界面，播放量 120,000。但没有提供后台数据链接、API 导出文件或数据验证 token。**
    - MCN 自制的投放效果分析表
  - 赵敏备注: "我们通常不会逐一核实创作者后台数据，依赖MCN的报告。但如果数据有问题，我们需要了解。"
- **C4 evidence:** MCN used a screenshot (not verifiable API data) to report 120K. The screenshot does not constitute "verified data" under contract terms.

**Length estimate:** ~400 words, ~600 tokens

---

### mcn-contract-excerpt.md (Update 2, before R6)

**Content key points:**
- Title: `星芒传媒经纪合约摘要 -- 周芳签约合同 (数据条款) + 品牌合作协议 (数据条款)`
- Format: Contract clause excerpts
- **Key clauses (C4 Source A):**
  - 经纪合约第 7.3 条: "乙方（MCN）在品牌合作中提供的效果数据，须以平台官方后台数据或经平台验证的第三方监测工具数据为准。截图、自制报表等不作为合同约定的'verified data'。"
  - 品牌合作协议第 4.2 条: "合作数据须为 verified data，即平台官方数据 API 导出或经双方确认的第三方监测报告。"
  - 经纪合约第 9.1 条: "乙方如在品牌合作中提供虚假数据或误导性信息，甲方（创作者）有权单方面解除合约并追究违约责任。"
- **C4 evidence:** MCN's screenshot submission violates both the agency contract (7.3) and brand agreement (4.2).

**Length estimate:** ~400 words, ~600 tokens

---

### bilibili-analytics.md (Initial)

**Content key points:**
- Title: `bilibili创作者后台数据导出 -- 周芳 (B站 UID: zf_lifestyle) -- 导出日期 2026-03-10`
- Format: Simulates bilibili creator analytics export
- **Key data:**
  - 视频 BV号: BV1xx-20260215-ZF
  - 发布日期: 2026-02-15
  - 截至 2026-03-10:
    - 播放量: 32,178
    - 点赞: 2,145
    - 评论: 198
    - 弹幕: 89
    - 分享: 67
  - MCN report claims bilibili views: 65,000 (2.0x inflation)
- **Update 4 evidence:** Cross-platform inflation pattern. Same video, same MCN, both platforms inflated by ~2x.
- **Near-signal noise:** Other video metrics, account growth data, audience demographics.

**Length estimate:** ~500 words, ~750 tokens

---

## 3. File Timing Summary

| File | First Visible | Purpose |
|---|---|---|
| xiaohongshu-analytics-export.md | Initial | C1 Source A (50K), C2 Source B (API definition) |
| mcn-brand-report.md | Initial | C1 Source B (120K), C3 (report date) |
| bilibili-analytics.md | Initial | Cross-platform data (32K), bilibili inflation evidence |
| brand-received-data.md | Update 1 (before R5) | C4 Source B (screenshot, not API data) |
| mcn-contract-excerpt.md | Update 2 (before R6) | C4 Source A (verified data requirement) |

---

## 4. Near-Signal Noise Design

### mcn-brand-report.md
- **Why it looks relevant:** Professional report with comprehensive data.
- **Why it should not settle C1:** The report's "平台数据统计" label looks authoritative but is not backed by verifiable source data.
- **Noise risk:** Agent may treat MCN report as equally authoritative as creator backend.

### xiaohongshu-analytics-export.md
- **Why it looks relevant:** Official platform data with API documentation.
- **Why API section may be missed:** The API documentation excerpt is embedded within the larger analytics export. An agent reading only the headline metrics might miss the single-definition clarification.

---

## 5. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | ~2,000 tokens |
| Initial scenario files (3 files) | ~3,150 tokens |
| Update files (2 files) | ~1,200 tokens |
| **Total workspace** | **10 files** | **~6,350 tokens** |
