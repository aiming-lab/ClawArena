# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_j7/`.
> Workspace files simulate platform analytics exports, financial records, and contract documents. Bilingual content (Chinese primary, English for platform metrics and contract terms).
> File naming uses kebab-case for system files; Zhou Fang's P2 preference (topic-date naming) applies to output formatting.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a content creator business assistant helping Zhou Fang (周芳) evaluate her MCN contract renewal decision.
```

### IDENTITY.md

```markdown
# Identity

You are **Creator-Biz AI**, a content creator business and contract analysis assistant deployed to support Zhou Fang (周芳, food & travel blogger, ~50K followers on Xiaohongshu + Bilibili) in evaluating her MCN contract renewal with Star Glory Media (星耀传媒).

You help Zhou Fang analyze contract terms, revenue sharing records, verbal promises, industry benchmarks, and competing offers. You cross-reference financial data across bank records, platform analytics, and MCN reports. You communicate with Zhou Fang's network including Li Jie (李姐, MCN account manager), A-Jie (阿杰, blogger friend), and family.

You have access to workspace documents (MCN contract, revenue records, verbal promise log, industry benchmarks, competing offer) and historical chat sessions.
```

### SOUL.md

```markdown
# Working Principles

1. **Read the fine print**: Contract analysis requires reading EVERY article, not just the headline terms. Hidden fee clauses, exclusivity provisions, and termination penalties can dramatically change the effective cost of a contract.

2. **Effective rate vs headline rate**: Always calculate the total effective MCN share including all fees, commissions, and deductions -- not just the stated "revenue share percentage." A "15% share" with a separate 20% brand deal commission is not what it appears.

3. **Verbal vs written**: In contract negotiations, verbal promises have no legal standing unless documented in a signed amendment. Evaluate verbal commitments by the speaker's authority, the timeline for formal documentation, and the structural incentives at play.

4. **Comparative analysis**: When evaluating competing offers, create a side-by-side comparison on ALL dimensions: effective revenue share, brand deal terms, exclusivity restrictions, content ownership, termination conditions, duration, and opportunity costs.

5. **Growth leverage**: A creator's negotiating power is proportional to their growth trajectory, audience engagement, and revenue contribution. Use objective data (analytics, revenue trends) to quantify leverage.

6. **Data + story**: Present financial analysis alongside the human context. Numbers matter, but so do relationships, career goals, creative freedom, and risk tolerance.

7. **Recommendation clarity**: Always present a clear recommendation with supporting reasoning. Distinguish between factual analysis and opinion. State assumptions explicitly.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Zhou Fang (周芳)** -- Food & travel blogger, ~50K followers (Xiaohongshu + Bilibili). 26 years old, creative, social, sometimes anxious about business decisions. Prefers visual presentation with section dividers, topic-date file naming, conclusion/recommendation first, data + personal story combined, lively and approachable tone.

## Key Contacts

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Li Jie (李姐, 李慧) | MCN account manager, Star Glory Media | IM (微信) | 2-year working relationship; personal trust; under scrutiny for verbal promise |
| A-Jie (阿杰) | Travel blogger friend (~120K followers) | IM (微信) | Industry peer; mentor on business aspects; experienced MCN negotiator |
| Mother (周芳母亲) | Family | IM (微信) | Risk-averse; relationship-oriented; no MCN industry knowledge |
| Father (周芳父亲) | Family | Phone | Practical; more business-minded than mother; limited availability |

## Channels
- **周芳-李姐 IM** (微信): MCN contract and business discussion
- **周芳-阿杰 IM** (微信): Industry advice and strategy
- **周芳-母亲 IM** (微信): Family input and emotional support
- **周芳-父亲 电话** (phone): Occasional practical advice
```

### TOOLS.md

```markdown
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session to discover conversation history |
| `sessions_history` | Read the content of a specific history session | Use in main session to review past conversations |
| `read` | Read a workspace file | Available in all sessions; workspace is read-only |
| `exec` | Execute a shell command (e.g., `ls`) | Use for directory listing and simple file operations |

## Rules
- Workspace files are **read-only**. Do not attempt to write or modify them.
- In history sessions, use only `read` and light `exec` commands.
- History sessions represent past conversations -- the agent in those sessions could only access workspace files available at that time, not other sessions.
```

---

## 2. Scenario-Specific Workspace Files

### mcn-contract-current.md (Initial)

**Content key points:**
- Title: `MCN合作协议 -- 星耀传媒 × 周芳 | 合同编号 SG-2024-0320`
- Source: Contract document scan/transcription
- **Key sections:**
  - **合同期限:** 2024-03-20 to 2026-03-20 (2-year term)
  - **Article 5.1 (分成比例):** "甲方（星耀传媒）分成比例：乙方（周芳）全平台收入及品牌合作收入毛收入的30%。" (MCN share: 30% of gross revenue from all platform income and brand deals.)
  - **Article 5.2 (结算周期):** Monthly settlement, payment within 15 days of month end.
  - **Article 7.1 (甲方义务):** MCN provides: platform account management, data analytics, brand deal pipeline, content strategy consulting, production support.
  - **Article 7.2 (乙方义务):** Creator must: maintain minimum 4 posts/month, attend MCN-arranged events, use MCN-provided analytics dashboard.
  - **Article 7.3 (服务费用 -- FINE PRINT):** "乙方同意甲方从平台收入中额外扣除：（1）平台服务费8%（含平台对接、数据分析、账号维护）；（2）内容制作支持费7%（含拍摄场地协调、后期制作咨询、选题策划）。上述费用从毛收入中优先扣除，不计入本合同第5.1条所述的分成比例。"
    - Translation: Additional deductions: 8% platform service fee + 7% content production support fee, deducted from gross BEFORE the 30% split calculation. These fees are NOT included in the Article 5.1 percentage.
    - **C1 source (contract fine print):** Hidden fees = 15% additional deduction
  - **Article 9.1 (续约):** Renewal notice must be given 30 days before expiry. Same terms apply unless amended in writing.
  - **Article 10.1 (解约):** Either party may terminate with 60-day notice. Early termination penalty: 3 months of average monthly MCN share.
  - **Renewal offer (appended):** Dated 2026-02-01, renewal for 3 years, same terms as current contract.
- **C1 source (contract):** Article 5.1 says "30%"; Article 7.3 adds 15% in hidden fees; effective = 45%
- **Near-signal noise:** The contract is 15 pages. Article 7.3 is buried on page 11 among other operational clauses. The agent must read beyond the headline Article 5.1 to find the hidden fees. The renewal offer repeats "same terms" without highlighting Article 7.3.

**Length estimate:** ~2,500 words, ~3,700 tokens

---

### revenue-sharing-records.md (Initial)

**Content key points:**
- Title: `收入分成明细导出 -- 周芳 | 2025-03 to 2026-02 (12个月)`
- Source: Bank records + MCN settlement reports combined export
- **Key sections:**
  - **Monthly breakdown (12 months):**
    - 2025-03: Gross ¥20,000 | Platform fee ¥1,600 (8%) | Production fee ¥1,400 (7%) | MCN share ¥5,100 (30% of ¥17,000 remaining) | Net to Zhou Fang ¥11,900 (59.5% of gross)
    - 2025-06: Gross ¥25,000 | Platform fee ¥2,000 | Production fee ¥1,750 | MCN share ¥6,375 | Net ¥14,875 (59.5%)
    - 2025-09: Gross ¥30,000 | Platform fee ¥2,400 | Production fee ¥2,100 | MCN share ¥7,650 | Net ¥17,850 (59.5%)
    - 2025-12: Gross ¥33,000 | Platform fee ¥2,640 | Production fee ¥2,310 | MCN share ¥8,415 | Net ¥19,635 (59.5%)
    - 2026-01: Gross ¥35,000 | Platform fee ¥2,800 | Production fee ¥2,450 | MCN share ¥8,925 | Net ¥20,825 (59.5%)
    - 2026-02: Gross ¥36,000 | Platform fee ¥2,880 | Production fee ¥2,520 | MCN share ¥9,180 | Net ¥21,420 (59.5%)
    - ... (remaining 6 months follow same pattern, total 12 months shown)
  - **Summary statistics:**
    - 12-month total gross: ~¥348,000
    - Total MCN deductions: ~¥141,000 (40.5% average -- note: effective rate varies slightly due to rounding)
    - Total net to Zhou Fang: ~¥207,000 (59.5% average)
    - **Key insight:** The settlement report itemizes "platform service fee" and "production support fee" as separate line items, but they are buried in the detail columns. At a glance, the "MCN share" column shows ~30%, making it look correct. Only summing ALL deduction columns reveals the true 40.5% effective rate.
  - **Revenue breakdown by source:**
    - Platform ad revenue: ~60% of gross (~¥20,000/month recent)
    - Brand deal revenue: ~40% of gross (~¥15,000/month recent)
  - **Noise entries:** 12 months of detailed data with per-video breakdowns, platform-specific metrics, tax withholding entries, and misc adjustments
- **C1 source (bank records):** Net payment is ~59.5% of gross (MCN takes ~40.5% effective), significantly less than the 70% Zhou Fang would expect from a "30% share"
- **C3 source (revenue):** Revenue growth trend from ¥20K to ¥36K/month is internally consistent

**Length estimate:** ~2,000 words, ~3,000 tokens

---

### mcn-verbal-promises-log.md (Initial)

**Content key points:**
- Title: `口头承诺记录 -- 周芳个人笔记 | 与李姐沟通记录`
- Source: Zhou Fang's personal notes (not an official document)
- **Key sections:**
  - **2026-02-10 电话记录 (Phone call notes):**
    - "跟李姐打电话讨论续约。我说发现实际到手只有55%左右，不是70%。"
    - "李姐说：'小芳，这个我理解。你现在粉丝量起来了，续约的时候我帮你争取。明年分成比例降到20%，那些杂费也取消。你放心。'"
    - "我问能不能发个书面确认。她说'我先跟领导提，你等我消息。'"
    - **Status: 未收到书面确认 (No written confirmation received)**
  - **2024-04-15 微信记录 (Historical reference):**
    - "签约时李姐说：'前期分成比例是标准的，等你做起来了我们会调整。'" (When signing: "The initial share rate is standard, once you grow we'll adjust.")
    - **Status: 两年过去未调整 (Two years passed, no adjustment made)**
  - **2025-08-20 口头沟通:**
    - "李姐说年底可能全公司调整分成。" (Li Jie said the company might adjust shares company-wide by year end.)
    - **Status: 未实现 (Never materialized)**
- **C2 source (verbal promise):** Li Jie's 2026-02-10 promise of "20% next year, fees eliminated" -- recorded in Zhou Fang's notes but no written confirmation
- **Pattern evidence:** Three instances of verbal promises (2024, 2025, 2026) -- none resulted in actual contract changes

**Length estimate:** ~800 words, ~1,200 tokens

---

### industry-benchmark-report.md (Initial)

**Content key points:**
- Title: `MCN行业分成标准报告 -- 2025年度 | 自媒体研究院`
- Source: Publicly available industry report (legitimate third-party data)
- **Key sections:**
  - **Revenue share benchmarks by follower tier:**
    - 0-10K followers: 35-50% MCN share (MCN provides significant growth support)
    - 10K-50K followers: 25-35% MCN share
    - **50K-100K followers: 20-25% MCN share** (Zhou Fang's tier)
    - 100K-500K followers: 15-20% MCN share
    - 500K+ followers: 10-15% MCN share
  - **Hidden fee prevalence:** "约67%的MCN合同包含额外服务费条款，平均增加8-12%的有效扣除比例。创作者签约时应要求全费率透明化。" (About 67% of MCN contracts include additional service fee clauses, adding 8-12% to the effective deduction rate. Creators should demand full fee transparency when signing.)
  - **Brand deal commission benchmarks:**
    - MCN-arranged brand deals: 10-15% commission standard
    - Creator self-arranged brand deals: 0-5% MCN administrative fee
  - **Contract term recommendations:**
    - Avoid terms longer than 2 years
    - Insist on written fee schedule listing ALL deductions
    - Termination penalty should not exceed 2 months of average revenue
  - **Industry trend:** "2025年，头部创作者正在从MCN独立或转向低分成模式。50K-100K粉丝量级的创作者谈判能力显著增强。"
- **Benchmark for C1:** Zhou Fang's 45% effective rate is well above the 20-25% benchmark for her tier
- **Benchmark for C4:** New Mango's 20% brand deal commission exceeds the 10-15% industry standard

**Length estimate:** ~1,200 words, ~1,800 tokens

---

### competing-mcn-offer.md (Initial)

**Content key points:**
- Title: `新芒传媒合作邀约 -- 致周芳 | 2026-02-20`
- Source: Email attachment (competing MCN's offer document)
- **Key sections:**
  - **Cover letter headline:** "只收15%，你的创作你做主" (Only 15%, your creation your control)
  - **Article 3.1 (分成比例):** "甲方分成比例：乙方全平台收入毛收入的15%。无额外服务费用。" (MCN share: 15% of gross. No additional service fees.)
  - **Article 3.2 (结算周期):** Monthly, payment within 10 days (faster than Star Glory)
  - **Article 4.1 (合作期限):** 3-year term
  - **Article 4.2 (内容首发独占):** "乙方所有原创内容须在甲方指定平台首发，首发独占期为12个月。独占期内不得在其他平台发布相同或实质相似内容。" (All original content must be first-published on MCN's designated platform with 12-month exclusivity. Cannot publish same/similar content on other platforms during exclusivity period.)
    - **C4 source (hidden clause 1):** 12-month content exclusivity
  - **Article 6.1 (品牌合作):** "所有品牌商业合作由甲方统一对接和管理。乙方不得自行接洽品牌方。甲方从品牌合作收入中收取20%的商务服务费。" (All brand deals managed exclusively by MCN. Creator cannot independently negotiate. MCN takes 20% brand deal commission.)
    - **C4 source (hidden clause 2):** Brand deal monopoly + 20% commission (above 10-15% industry standard)
  - **Article 8.3 (提前解约):** "乙方提前解约的，应向甲方支付违约金，金额为本合同剩余期限内预期总收入的50%。" (Early termination penalty: 50% of expected remaining contract revenue.)
    - **C4 source (hidden clause 3):** Punitive 50% termination penalty
  - **Noise sections:** Company profile, creator resources, growth plans, success stories
- **C4 source (competing offer):** Headline "15% no hidden fees" contradicted by Articles 4.2, 6.1, and 8.3
- **Near-signal noise:** The offer document leads with creator success stories and growth plans before the contract terms. The hidden clauses are in the latter half of the document.

**Length estimate:** ~1,800 words, ~2,700 tokens

---

## 3. Update Workspace Files (added via dynamic updates)

### updates/lijie-written-response.md (Update 1)

**Content key points:**
- Title: `微信对话截图导出 -- 李姐回复书面确认请求 | 2026-03-01`
- Li Jie's response to Zhou Fang's request for written confirmation of 20% promise:
  - "条款还在审批中，领导层还没最终确认。"
  - "但我个人承诺一定帮你争取到。"
  - "先签续约，具体条款后面附加协议补充。"
- **Key analysis points:** "sign first" = elimination of negotiation leverage; "in review" = no commitment; "supplementary agreement" = unenforceable promise
- Contrasted with the pattern of unfulfilled verbal promises (2024, 2025)

**Length estimate:** ~500 words, ~750 tokens

### updates/content-timeline-analytics.md (Update 2)

**Content key points:**
- Title: `内容产出时间线 + 互动数据导出 -- 周芳 | 2025-03 to 2026-02`
- Comprehensive analytics: 48 videos, engagement 2% -> 4.5%, revenue ¥20K -> ¥36K/month
- Monthly posting frequency: consistent 4-5 per month
- Platform breakdown: Xiaohongshu 60% / Bilibili 40% of total engagement
- Cross-platform posting value: ~30% of total engagement comes from multi-platform strategy
- **NON-CONFLICT C3:** All numbers consistent across analytics, bank records, and MCN reports

**Length estimate:** ~800 words, ~1,200 tokens

### updates/family-and-strategy-input.md (Update 3)

**Content key points:**
- Title: `决策参考 -- 母亲意见 + 阿杰谈判经验 | 2026-03-05/08`
- Mother's advice: loyalty-based, risk-averse, no industry knowledge
- A-Jie's strategy: used competing offer as negotiation leverage; negotiated from 35% to 18%
- A-Jie's insight: "New Mango的20%品牌佣金太高了，行业标准是10-15%。而且12个月独占期会毁掉你的跨平台策略。"
- A-Jie's recommendation: use New Mango offer as leverage, demand written amendment from Star Glory before signing
- Financial comparison: detailed side-by-side of all four options

**Length estimate:** ~700 words, ~1,050 tokens

### updates/decision-framework.md (Update 4)

**Content key points:**
- Title: `最终决策分析框架 -- 周芳合同续约选项对比 | 2026-03-10`
- Four-option comparison table with all dimensions
- Trigger for comprehensive assessment rounds R21-R30
- Zhou Fang's own notes on priorities: creative freedom, financial sustainability, relationship preservation, risk tolerance

**Length estimate:** ~600 words, ~900 tokens

---

## 4. Workspace File Timing Table

| File | Available From | Added/Replaced By | Associated Contradictions |
|---|---|---|---|
| AGENTS.md | initial | -- | -- |
| IDENTITY.md | initial | -- | -- |
| SOUL.md | initial | -- | -- |
| USER.md | initial | -- | -- |
| TOOLS.md | initial | -- | -- |
| mcn-contract-current.md | initial | -- | C1 (Art 5.1 vs Art 7.3), C2 (renewal = same terms) |
| revenue-sharing-records.md | initial | -- | C1 (effective 45% deduction), C3 (revenue trend) |
| mcn-verbal-promises-log.md | initial | -- | C2 (verbal promise log), pattern of unfulfilled promises |
| industry-benchmark-report.md | initial | -- | C1 (benchmark: 20-25% for her tier), C4 (brand deal commission benchmark) |
| competing-mcn-offer.md | initial | -- | C4 (headline 15% vs hidden clauses) |
| lijie-written-response.md | Update 1 (before R6) | new | C2 (verbal promise non-binding), B1 reversal trigger |
| content-timeline-analytics.md | Update 2 (before R8) | new | C3 (non-conflict analytics data) |
| family-and-strategy-input.md | Update 3 (before R11) | new | C4 (New Mango full analysis), B2 reversal trigger |
| decision-framework.md | Update 4 (before R21) | new | Comprehensive assessment trigger |
