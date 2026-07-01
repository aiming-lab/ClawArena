# Layer 1 -- Workspace File Spec

> All workspace files under `benchmark/data/calmb-new/workspaces/trace_j4/`.

---

## 1. Fixed Agent Configuration Files
*(Standard: AGENTS.md, IDENTITY.md (**FollowerOps AI**, follower analytics assistant), SOUL.md, USER.md (周芳, 李姐/MCN, 小美/blogger friend, 粉丝群管��员), TOOLS.md)*

---

## 2. Scenario-Specific Workspace Files

### platform-follower-history.md (Initial)
- Title: `小红书粉丝变化记录 -- 周芳 -- 2026年3月`
- **C1 Source A:** 3月15日新增3,012, 来源"推荐页", 无异常标记. 正常日增20-50.
- Growth chart: 52K→55K overnight, then stable.
- Near-signal noise: daily growth metrics for past 30 days.
- **Length:** ~600 words, ~900 tokens

### third-party-analytics.md (Initial)
- Title: `第三方数据��控报告 -- 新榜分析 -- 周芳账号 -- 2026-03-16`
- **C1 Source B:** 新增3,012粉丝画像: 78%无头像, 85%无内容发布, 注册日期92%在最近30天, 地域山东65%, ���跃度<5%. 评级："高风险，疑似非自然增长"
- Near-signal noise: engagement rate analysis, content performance metrics.
- **Length:** ~700 words, ~1,050 tokens

### mcn-growth-report.md (Initial)
- Title: `星芒传媒旗下创作者增长月报 -- 2026���3月`
- **C2 Source B seed:** 推广活动列���：活动A(3月3日品牌联动), 活动B(3月10日内容互推). **无3月15日前后的推广活动记录。**
- Near-signal noise: other creators' growth data, budget allocation.
- **Length:** ~600 words, ~900 tokens

### platform-announcement.md (Update 1, before R5)
- Title: `小红书平台公告 -- 账号质量维护 -- 2026-03-18`
- **C2 Source B:** "本平台于2026年3月18日完成���月账号质量维护，清理违规注册和异常关注关系。" 周芳粉丝掉落2,500与此公告时间完全匹配。
- **Length:** ~300 words, ~450 tokens

### follower-demographics.md (Update 2, before R6)
- Title: `粉丝画像深度分析 -- 周芳 -- 涨粉前后对比`
- **C1 deepening:** 涨粉前正常粉丝画像 vs ��增粉丝画像对比。正常��女性72%, 18-35岁85%, 上海/北京/杭州Top3. 新增：性��未填88%, 年龄未填90%, 山东65%.
- **Length:** ~500 words, ~750 tokens

---

## 3. File Timing Summary

| File | First Visible | Purpose |
|---|---|---|
| platform-follower-history.md | Initial | C1 Source A (platform "normal") |
| third-party-analytics.md | Initial | C1 Source B (bot indicators) |
| mcn-growth-report.md | Initial | C2 (no matching campaign) |
| platform-announcement.md | Update 1 (before R5) | C2 (cleanup timing match) |
| follower-demographics.md | Update 2 (before R6) | C1 deepening (demographic mismatch) |

---

## 5. Total Workspace Token Estimate

| Category | Token Estimate |
|---|---|
| Fixed agent config | ~2,000 |
| Initial scenario files (3) | ~2,850 |
| Update files (2) | ~1,200 |
| **Total** | **~6,050 tokens** |
