# Layer 1 -- Workspace File Spec

> All workspace files under `benchmark/data/calmb-new/workspaces/trace_j8/`.

---

## 1. Fixed Agent Configuration Files
*(Standard: AGENTS.md, IDENTITY.md (**TravelLegal AI**, cross-border legal compliance assistant), SOUL.md (legal compliance priority, regulatory deadlines critical, distinguish commercial vs personal), USER.md (周芳, 旅行社, 李姐/MCN, 阿杰/travel blogger, 父亲), TOOLS.md)*

---

## 2. Scenario-Specific Workspace Files

### japan-filming-regulations.md (Initial)
- Title: `日本拍摄法规翻译 -- 文化財保護法相关条款 -- 京都市适用`
- **C1 Source B / C2 context:**
  - 《文化財保護法》第43条: 指定文化財区域内商業目的の撮影需事前许可
  - 定义"商業撮影": 用于商业发布、广告、网络商业内容的拍摄
  - "個人撮影"（旅游留念）: 不受限制
  - 许可申请: 向管理方提交，审批约7工作日，费用¥5,000-¥20,000 JPY
  - 违规: 首次警告+书面说明要求，重复违规可处罚款
- **Length:** ~600 words, ~900 tokens

### travel-agency-briefing.md (Initial)
- Title: `旅行社出发前说明 -- 日本京都文化之旅 -- 2026-03-03`
- **C1 Source A:**
  - "京都景点拍照自由，无特殊拍摄限制"
  - "注意事项：不使用三脚架，不阻碍通道，保持安静"
  - 无任何关于商业拍摄许可的提及
- **Length:** ~400 words, ~600 tokens

### warning-letter-translation.md (Initial)
- Title: `日方警告函翻译 -- 京都市文化財保護課 -- 2026-03-20`
- **C2 Source A / C4 Source B:**
  - 发函单位: 京都市文化財保護課
  - 事由: "未经许可在清水寺境内进行商业目的拍摄"
  - 证据: 工作人员目击+网络发布内容确认
  - **要求: "请于收到本函14个自然日内提交书面说明，说明拍摄目的、内容商业属性、及未申请许可之原因。"**
  - 逾期后果: "未在期限内回复将视为不配合，可能面临进一步行政措施"
- **Length:** ~500 words, ~750 tokens

### filming-location-photos.md (Initial)
- Title: `拍摄地点照片描述 + 行程时间表 -- 清水寺`
- **C3 NON-CONFLICT + signage detail:**
  - 行程: 3月5日10:00-12:00 清水寺，设备Sony A7IV+稳定器
  - 照片描述: 入口处标识"商業撮影は事前申請が必要です"——标识尺寸约A4纸大小，位于购票处侧面，日文，无英文/中文翻译
- **Length:** ~400 words, ~600 tokens

### mcn-legal-response.md (Update 2, before R6)
- Title: `MCN法务回复 -- 日本拍摄事件 -- 2026-03-22`
- **C4 Source A:**
  - MCN法务李律师建议: "发一封道歉信给日方，表示不知情，承诺下次申请。一般道歉就能解决。"
  - **未提及:** 14天行政期限、书面说明的格式要求、是否需要当地律师协助
- **Length:** ~400 words, ~600 tokens

---

## 3. File Timing Summary

| File | First Visible | Purpose |
|---|---|---|
| japan-filming-regulations.md | Initial | C1 Source B, C2 context |
| travel-agency-briefing.md | Initial | C1 Source A |
| warning-letter-translation.md | Initial | C2 Source A, C4 Source B |
| filming-location-photos.md | Initial | C3 (itinerary), signage |
| mcn-legal-response.md | Update 2 | C4 Source A |

## 5. Total: ~10 files, ~5,850 tokens
