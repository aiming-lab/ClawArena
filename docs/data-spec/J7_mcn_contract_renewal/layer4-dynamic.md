# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R6 | Deliver Li Jie's "sign first" response -- triggers C2 full resolution (verbal promise is non-binding) and C1 context reinforcement (Article 7.3 analysis); B1 reversal | Yes: Li Jie IM Phase 2 append (confrontation + vague response) | Yes: lijie-written-response.md | R3->R7 (C2: verbal promise definitively unreliable; "sign first" tactic identified); R5->R9 (B1: guanxi trust overridden by evidence of non-commitment) |
| U2 | Before R8 | Deliver content timeline analytics (NON-CONFLICT C3) -- provides growth data for leverage assessment and supports C4 analysis (cross-platform engagement value at risk from exclusivity) | No session append | Yes: content-timeline-analytics.md | No direct reversal; provides objective data anchor for options comparison and C4 exclusivity cost calculation |
| U3 | Before R11 | Deliver A-Jie's negotiation experience + family input + full New Mango analysis -- triggers C4 full resolution (hidden clauses are NOT standard) and B2 reversal | Yes: A-Jie IM Phase 2 append (strategy session) + Mother IM Phase 2 append (emotional input) | Yes: family-and-strategy-input.md | R4->R8 complete (C4: New Mango effective cost fully calculated; hidden clauses above industry standard); B2 reversal (headline rate is NOT the key metric; total effective cost comparison required) |
| U4 | Before R21 | Deliver decision framework -- triggers comprehensive assessment with four-option comparison | No session append | Yes: decision-framework.md | Enables comprehensive R21-R30 assessment; frames all four options with complete evidence |

---

## 2. Action Lists

### Update 1 (before R6)

**Trigger timing:** After R5 answer is submitted, before R6 question is injected.
**Purpose:** Introduces Li Jie's response to the written confirmation request. Li Jie reveals: "terms still being reviewed," "personal promise," "sign first, supplementary agreement later." This confirms the verbal promise has no institutional backing and exposes the "sign first" leverage elimination tactic. Also appends Phase 2 content to Li Jie IM session (confrontation, vague response, emotional appeal, New Mango warning).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "lijie-written-response.md",
    "source": "updates/lijie-written-response.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LIJIE_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LIJIE_IM_UUID.jsonl"
  }
]
```

### Update 2 (before R8)

**Trigger timing:** After R7 answer is submitted, before R8 question is injected.
**Purpose:** Introduces comprehensive content timeline analytics confirming C3 (non-conflict). The analytics data shows consistent growth across all metrics and provides: (1) objective foundation for leverage assessment (5x follower growth, 80% revenue growth); (2) cross-platform engagement data showing ~30% comes from multi-platform posting (critical for C4 exclusivity cost calculation); (3) revenue trend supporting financial projections for all four options.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "content-timeline-analytics.md",
    "source": "updates/content-timeline-analytics.md"
  }
]
```

### Update 3 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Introduces A-Jie's detailed negotiation experience (35% to 18% with leverage), mother's emotional input, and comprehensive New Mango analysis showing hidden clause costs exceed industry standards. This triggers C4 full resolution (New Mango effective cost ~¥11,250+/month vs Star Glory ¥15,750) and B2 reversal (hidden clauses are NOT standard; brand deal commission is 5-10% above benchmark; exclusivity cost is quantifiable). Also provides the leverage strategy: use competing offer to negotiate written Star Glory terms.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "family-and-strategy-input.md",
    "source": "updates/family-and-strategy-input.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_AJIE_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_AJIE_IM_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_MOTHER_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_MOTHER_IM_UUID.jsonl"
  }
]
```

### Update 4 (before R21)

**Trigger timing:** After R20 answer is submitted, before R21 question is injected.
**Purpose:** Introduces the decision framework workspace file with a structured four-option comparison template and Zhou Fang's personal priority notes. This triggers the comprehensive assessment rounds R21-R30 where the agent must evaluate all four options (renew at current terms, renew with written amendment, switch to New Mango, go independent) across all dimensions (financial, strategic, relational, risk).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "decision-framework.md",
    "source": "updates/decision-framework.md"
  }
]
```

---

## 3. Source File Content Summaries

### updates/lijie-written-response.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C2 (full resolution -- verbal promise non-binding), B1 reversal trigger
**Content key points:**
- Title: "微信对话截图导出 -- 李姐回复书面确认请求 | 2026-03-01"
- Li Jie's three key phrases: "条款还在审批中" (terms being reviewed), "个人承诺" (personal promise), "先签续约" (sign first)
- Analysis of each phrase: no institutional commitment, no authority, leverage elimination tactic
- Comparison with historical pattern: three verbal promises (2024, 2025, 2026), zero written amendments
- Zhou Fang's note: "看来书面确认是拿不到了" (looks like written confirmation isn't coming)

**Length estimate:** ~500 words, ~750 tokens

---

### updates/content-timeline-analytics.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C3 (non-conflict -- growth data), supports C4 exclusivity cost assessment
**Content key points:**
- Title: "内容产出时间线 + 互动数据导出 -- 周芳 | 2025-03 to 2026-02"
- 48 videos over 12 months (4-5/month average)
- Engagement: 2.0% -> 4.5% (average across platforms)
- Revenue: ¥20,000 -> ¥36,000/month gross
- Platform split: Xiaohongshu 60% / Bilibili 40% of total engagement
- Cross-platform posting: ~30% of engagement comes from simultaneous multi-platform distribution
- Brand deal growth: ¥8,000 -> ¥15,000/month
- All metrics consistent across platform analytics, bank records, MCN reports

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/family-and-strategy-input.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C4 (full resolution -- New Mango hidden clause analysis), B2 reversal trigger
**Content key points:**
- Title: "决策参考 -- 母亲意见 + 阿杰谈判经验 | 2026-03-05/08"
- **Mother's input:** "李姐照顾你两年了，做人要讲信用。不要轻易换。" Risk-averse, loyalty-based, no industry knowledge.
- **A-Jie's analysis of New Mango:**
  - Brand deal commission: 20% vs industry standard 10-15% (5-10% above benchmark)
  - 12-month exclusivity: would eliminate ~30% of Zhou Fang's cross-platform engagement
  - Termination penalty: ~¥210,000 based on ¥35K/month × 12 months × 50%
  - Conclusion: "新芒没有他们说的那么好" (New Mango isn't as good as they claim)
- **A-Jie's negotiation strategy:**
  - Use New Mango offer as leverage (don't actually sign)
  - Demand written Star Glory terms: 25% or below, no hidden fees, 2-year max, main contract
  - Precedent: A-Jie negotiated from 35% to 18% with this approach
- **Side-by-side comparison table:** Four options with monthly cost, risk level, control level, brand deal access

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/decision-framework.md (Update 4)

**File type:** workspace new
**Associated contradictions:** Comprehensive trigger for R21-R30
**Content key points:**
- Title: "最终决策分析框架 -- 周芳合同续约选项对比 | 2026-03-10"
- **Four-option comparison:**
  - Option 1: Renew current (45% effective, 3yr, known, ¥15,750/month cost)
  - Option 2: Renew amended (20% if achieved, unknown timeline, ¥7,000/month cost IF delivered)
  - Option 3: New Mango (15% platform + 20% brand + exclusivity + penalty, ~¥11,250/month + opportunity cost)
  - Option 4: Independent (0% MCN, self-manage everything, ¥5-8K/month operational cost)
- **Zhou Fang's priority notes:**
  - Creative freedom: High priority (exclusivity is a concern)
  - Financial sustainability: Critical (need to optimize effective rate)
  - Relationship preservation: Important but secondary to financial fairness
  - Risk tolerance: Moderate (prefers negotiated certainty over dramatic change)
- **Decision deadline:** 2026-03-20 (contract expiry)

**Length estimate:** ~600 words, ~900 tokens

---

## 4. Runtime Checks

After all updates are applied:
- [ ] C1 has evidence in contract (Art 5.1 = 30%, Art 7.3 = +15%), bank records (45% effective), and industry benchmarks (20-25% for her tier)
- [ ] C2 has evidence in verbal promise log (3 unfulfilled promises), lijie-written-response.md ("sign first" tactic), and A-Jie's corroboration (verbal unreliable)
- [ ] C3 has NO contradictions -- growth metrics consistent across all sources (48 videos, 2%->4.5% engagement, ¥20K->¥36K revenue)
- [ ] C4 has evidence in competing offer (15% headline vs Art 4.2 exclusivity, Art 6.1 brand monopoly 20%, Art 8.3 penalty 50%), benchmarks (brand commission 10-15% standard vs 20%), and A-Jie's analysis (hidden clauses above industry standard)
- [ ] B1 phrase appears verbatim in Li Jie IM Loop 4
- [ ] B2 phrase appears verbatim in A-Jie IM Loop 3
- [ ] All 4 updates have correct action type/path/source fields
- [ ] Financial figures consistent: Gross ¥35K/month, Art 5.1 = 30%, Art 7.3 = 15% (8%+7%), effective MCN = 45%, net = ¥19,250 (55%), Li Jie promise = 20%, New Mango headline = 15%, New Mango brand commission = 20%, termination penalty = 50% of remaining revenue
- [ ] Timeline consistent: Renewal notice 02-01, bank analysis 02-05, contract re-read 02-08, Li Jie phone 02-10, benchmarks 02-15, New Mango outreach 02-20, New Mango contract review 02-25, written request 03-01, content review 03-03, mother call 03-05, A-Jie strategy 03-08, final analysis 03-10, contract expiry 03-20
