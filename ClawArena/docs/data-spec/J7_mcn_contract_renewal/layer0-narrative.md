# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_j7` |
| Domain | Content Creator Business / Contract Law / Revenue Sharing |
| Time span | 6 weeks (2026-02-01 to 2026-03-15) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Zhou Fang (周芳), 26, food & travel blogger on Xiaohongshu + Bilibili (~50K followers) |
| One-sentence | Zhou Fang's MCN contract is expiring and she must decide whether to renew, switch to a competing MCN, or go independent -- but the contract's stated revenue share ("30% MCN share"), the actual bank records (showing 45% deducted), 李姐's verbal promise ("next year 20%"), and a competing MCN's offer ("15% share" with hidden clauses) all conflict with each other. |

---

## 2. Business Context

| Field | Value |
|---|---|
| Current MCN | 星耀传媒 (Star Glory Media), Shanghai-based MCN |
| MCN contact | Li Jie (李姐, real name 李慧), MCN account manager, Zhou Fang's primary contact for 2 years |
| Current contract | Signed 2024-03-20, expires 2026-03-20 (2-year term) |
| Stated revenue split | Contract Article 5.1: "MCN share: 30% of gross revenue from all platform income and brand deals" |
| Actual deduction | Bank records show ~45% average deduction over 12 months (hidden "platform service fee" 8% + "content production support" 7% in Article 7.3 fine print) |
| Competing MCN | 新芒传媒 (New Mango Media), offering "15% MCN share" -- but with hidden clauses |
| Zhou Fang's monthly revenue | Average ¥35,000/month gross; receives ~¥19,250/month net (55% of gross) |
| Industry benchmark | Top-tier MCN share for 50K-follower creators: 20-25%; mid-tier: 25-35% |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| 2026-02-01 | Zhou Fang receives contract renewal notification from Star Glory Media. Current contract expires 2026-03-20. Renewal offer: same terms (30% MCN share) for 3 years. | Li Jie sends renewal package via email. The renewal terms are identical to the current contract -- including the hidden fee clauses in Article 7.3 that Zhou Fang has never carefully read. Li Jie frames it as "same great terms, longer stability." | Zhou Fang, Li Jie. Zhou Fang has not yet analyzed her actual revenue share. |
| 2026-02-05 | Zhou Fang starts reviewing her finances in preparation for renewal decision. She pulls bank payment records for the past 12 months. | **Zhou Fang calculates her actual revenue share.** She sees: gross revenue from platforms + brand deals averages ¥35,000/month, but she receives only ~¥19,250/month (55% of gross). If MCN takes 30% as stated in the contract, she should receive ¥24,500/month (70% of gross). **The ¥5,250/month discrepancy (~15% of gross) is unexplained.** | Zhou Fang discovers the discrepancy but doesn't yet know the cause. |
| 2026-02-08 | Zhou Fang re-reads the contract carefully. She discovers Article 7.3 in the fine print. | **Article 7.3 reads:** "乙方同意甲方从平台收入中额外扣除：（1）平台服务费8%（含平台对接、数据分析、账号维护）；（2）内容制作支持费7%（含拍摄场地协调、后期制作咨询、选题策划）。上述费用从毛收入中优先扣除，不计入本合同第5.1条所述的分成比例。" Translation: MCN deducts an additional 8% "platform service fee" and 7% "content production support fee" from gross revenue BEFORE the 30% split is calculated. **Effective MCN share = 30% + 15% = 45%.** | Zhou Fang now understands the contract structure. She realizes she signed this 2 years ago without reading the fine print. |
| 2026-02-10 | Zhou Fang confronts Li Jie about the discrepancy in a phone call. Li Jie verbally promises better terms. | **Li Jie says on the phone:** "小芳，这个我理解。你现在粉丝量起来了，续约的时候我帮你争取。明年分成比例降到20%，那些杂费也取消。你放心。" (I understand. Your follower count has grown. I'll negotiate for you during renewal. Next year the share drops to 20% and those miscellaneous fees are eliminated. Don't worry.) **This promise is verbal only -- no written confirmation, no formal amendment.** | Zhou Fang has Li Jie's verbal promise. She records a summary in her notes but has no formal written commitment. Li Jie may or may not have authority to make this commitment. |
| 2026-02-15 | Zhou Fang asks blogger friend A-Jie (阿杰) about industry benchmarks. A-Jie shares an industry report. | **A-Jie shares a publicly available industry benchmark report** showing: for creators with 50K-100K followers, typical MCN shares range from 20-25% (top-tier MCN) to 25-35% (mid-tier). A-Jie says: "45%太高了，就算是30%也算中等偏高。你这个量级应该在20-25%。" (45% is too high. Even 30% is on the higher side. At your scale you should be at 20-25%.) | Zhou Fang, A-Jie. Industry benchmark data is objective and publicly verifiable. |
| 2026-02-20 | Zhou Fang receives a cold outreach from New Mango Media (新芒传媒), a competing MCN, offering "15% MCN share." | **New Mango's pitch:** "我们只收15%，没有任何隐藏费用。你的创作你做主。" (We only take 15%, no hidden fees. Your creation, your control.) Zhou Fang receives their offer document via email. **The 15% headline is real, but the contract has its own hidden clauses** that Zhou Fang has not yet discovered. | Zhou Fang has the offer headline. She has not yet read the New Mango contract carefully. |
| 2026-02-25 | Zhou Fang carefully reads the New Mango contract. She discovers the hidden clauses. | **New Mango contract fine print:** (1) Article 4.2: "内容首发独占期12个月" -- all content must be first-published on New Mango's designated platform for 12 months (limiting Zhou Fang's cross-platform strategy); (2) Article 6.1: "品牌合作由甲方统一对接，创作者不得自行接洽" -- brand deal monopoly, the creator cannot independently negotiate brand deals (New Mango takes a separate 20% commission on brand deals they arrange); (3) Article 8.3: "提前解约违约金为本合同期内预期总收入的50%" -- early termination penalty is 50% of expected total contract revenue. **Effective cost: 15% platform share + 20% brand deal commission + exclusivity restrictions + punitive termination clause.** | Zhou Fang now sees the hidden trade-offs. |
| 2026-03-01 (Update 1) | Zhou Fang asks Li Jie for written confirmation of the "20% next year" promise. Li Jie responds vaguely. | **Li Jie's response:** "条款还在审批中，领导层还没最终确认。但我个人承诺一定帮你争取到。先签续约，具体条款后面附加协议补充。" (Terms still being reviewed, leadership hasn't confirmed yet. But I personally promise to fight for it. Sign the renewal first, we'll add specific terms via a supplementary agreement later.) **This is a classic "sign now, negotiate later" tactic. Li Jie has no written authorization to offer 20%.** | Zhou Fang, Li Jie. The lack of written commitment is now explicit. |
| 2026-03-03 (Update 2) | Zhou Fang reviews the content output timeline -- her posting schedule, video production dates, and engagement metrics for the past year. | **The content timeline is internally consistent (NON-CONFLICT C3).** Zhou Fang produced 48 videos in 12 months. Her engagement grew from 2% to 4.5% average. Monthly brand deal revenue grew from ¥8,000 to ¥15,000. Platform ad revenue grew from ¥12,000 to ¥20,000. All numbers are consistent across her analytics dashboard, bank records, and MCN reports. The timeline confirms her growing leverage but does not contain contradictions. | Zhou Fang. Objective data supporting her negotiating position. |
| 2026-03-05 (Update 3) | Zhou Fang's mother weighs in. She calls to discuss the situation. | **Mother's advice:** "女儿，签了合同就要遵守。李姐照顾你两年了，做人要讲信用。不要轻易换。" (Daughter, once you sign a contract you honor it. Li Jie has taken care of you for two years. Be loyal. Don't switch easily.) **Mother is risk-averse and relationship-oriented.** Her advice prioritizes loyalty over financial optimization. However, she does not have business expertise in the MCN industry. | Zhou Fang, Mother. Emotional/relational input, not evidence-based business advice. |
| 2026-03-08 (Update 3 continued) | A-Jie shares his own MCN negotiation experience. He reveals he negotiated from 35% down to 18% by threatening to leave. | **A-Jie's experience:** "我当时也是合同到期前一个月，拿着别家的offer跟MCN谈。他们最后从35%降到18%。你要用新芒的offer当谈判筹码，不一定真要去。" (When my contract was expiring I used a competing offer as leverage. They dropped from 35% to 18%. Use New Mango's offer as a negotiation chip -- you don't have to actually go.) | Zhou Fang, A-Jie. Strategic advice with precedent. |
| 2026-03-10 (Update 4) | Zhou Fang presents her analysis to A-Jie and prepares for a final negotiation with Li Jie. She needs a comprehensive assessment of all options. | **Decision point.** Zhou Fang must weigh: (1) Renew with Star Glory at current terms (30% stated + 15% hidden = 45% effective); (2) Renew with Star Glory if Li Jie's 20% promise materializes (unconfirmed); (3) Switch to New Mango (15% platform + hidden brand deal commission + exclusivity + termination penalty); (4) Go independent (0% MCN share but lose MCN resources, brand deal pipeline, and operational support). | Zhou Fang. All evidence now available for comprehensive analysis. |

---

## 4. Role-Level Truth vs Self-Narrative

### Zhou Fang (周芳) -- Protagonist, Food & Travel Blogger

- **Objective position:** Zhou Fang is a 26-year-old content creator with ~50K followers across Xiaohongshu and Bilibili. She signed a 2-year MCN contract without reading the fine print, resulting in 45% effective revenue deduction instead of the expected 30%. She is now at a decision point: renew, switch, or go independent. Her growing engagement and revenue give her leverage.
- **Public narrative:** Upbeat content creator who doesn't discuss business conflicts publicly. Her content is food and travel focused.
- **Private narrative:** Anxious about the financial implications. Feels somewhat betrayed by the hidden fees but also grateful for MCN support in her early growth. Torn between loyalty to Li Jie (personal relationship) and financial self-interest.
- **Trust bias:** Over-trusts social media data panels and headline numbers; underestimates fine print and private information. Initially attracted to New Mango's "15%" without reading the contract.

### Li Jie (李姐, 李慧) -- MCN Account Manager

- **Objective position:** Li Jie is the account manager at Star Glory Media assigned to Zhou Fang. She genuinely helped Zhou Fang grow from 10K to 50K followers. The 45% effective rate is the standard Star Glory contract -- she did not personally design the fee structure. Her verbal promise of "20% next year" is sincere in intent but she does not have authority to guarantee it.
- **Public narrative:** "I'm fighting for you. The company values you. Give us time to adjust the terms."
- **Private motivation:** Retention is her KPI. Losing Zhou Fang would reflect poorly on her performance. She may genuinely want to reduce the rate but cannot unilaterally commit.
- **Why the gap exists:** The MCN industry has a pervasive gap between verbal promises and written contracts. Li Jie operates in this gray zone -- her promises are sincere but non-binding, and she may not be able to deliver.

### New Mango Media -- Competing MCN

- **Objective position:** New Mango offers a genuinely lower platform share (15% vs 30%), but compensates through: (1) 12-month content exclusivity lock-in, (2) brand deal monopoly with separate 20% commission, and (3) punitive 50% termination clause. The effective total cost may exceed Star Glory's depending on Zhou Fang's brand deal volume.
- **Public narrative:** "Lowest fees in the industry. Creator-first philosophy."
- **Private motivation:** Aggressive growth strategy. New Mango is acquiring creators by undercutting on headline rates while recouping through brand deal commissions and exclusivity.
- **Why the gap exists:** The MCN industry's lack of standardized contract terms allows competing offers to appear dramatically different on headline metrics while being comparable (or worse) on effective terms.

### A-Jie (阿杰) -- Blogger Friend / Travel Creator

- **Objective position:** A-Jie is a more experienced travel blogger (~120K followers) who successfully renegotiated his MCN contract from 35% to 18% using a competing offer as leverage. He provides strategic advice and industry benchmark data. His advice is practical and precedent-based.
- **Public narrative:** Supportive friend, mentoring Zhou Fang on business aspects of content creation.
- **Why the gap exists:** A-Jie's experience is directly relevant but his situation may not be identical -- he has 2.4x Zhou Fang's followers, which gives him more leverage.

### Mother (周芳母亲) -- Family

- **Objective position:** Zhou Fang's mother is risk-averse and relationship-oriented. She prioritizes loyalty and stability over financial optimization. She does not have MCN industry knowledge.
- **Public narrative:** Traditional values -- honor commitments, maintain relationships.
- **Why the gap exists:** Generational gap in understanding the gig economy and MCN industry dynamics.

---

## 5. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Source C (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|---|
| C1 | Revenue share discrepancy: Contract says "30% MCN share" vs bank records show ~45% effectively deducted | mcn-contract-current.md Article 5.1: "甲方分成比例：毛收入的30%" | revenue-sharing-records.md: 12-month average shows Zhou Fang receives 55% of gross (MCN effectively takes 45%) | mcn-contract-current.md Article 7.3 (fine print): additional 8% platform service fee + 7% content production support fee, deducted before the 30% split | The contract technically says 30% in Article 5.1, but Article 7.3 adds 15% in hidden fees deducted BEFORE the split. Effective MCN share = 30% + 15% = 45%. The contract is internally consistent if you read ALL articles, but Article 5.1 alone is misleading. | R2 (contract vs bank records discrepancy visible) | **Yes: R2-->R6** (Article 7.3 fine print discovered, resolving the "discrepancy" as a deliberately obscured contract structure) |
| C2 | Li Jie's verbal promise vs no written confirmation: Li Jie promised "20% next year, fees eliminated" vs contract renewal offer has same terms vs no written amendment exists | mcn-verbal-promises-log.md: Zhou Fang's notes recording Li Jie's phone call 2026-02-10 "明年分成降到20%，杂费取消" | mcn-contract-current.md: Renewal offer maintains identical terms (30% + hidden fees) | Li Jie's follow-up (Update 1): "条款还在审批中...先签续约，具体条款后面附加协议补充" | Li Jie's verbal promise is sincere in intent but not binding. She has no written authorization and the renewal offer does not reflect her promise. The "sign first, negotiate later" response is a red flag -- once renewed, Zhou Fang has no leverage. | R3 (verbal promise vs contract terms visible) | **Yes: R3-->R7** (Update 1: Li Jie's vague follow-up confirms the promise has no written backing; "sign first" tactic identified) |
| C3 | Content output timeline: posting schedule, production dates, engagement metrics, revenue growth -- all consistent across analytics, bank records, and MCN reports (NON-CONFLICT) | revenue-sharing-records.md: Monthly revenue figures (platform + brand deals) | mcn-verbal-promises-log.md context: References to Zhou Fang's growth trajectory | industry-benchmark-report.md: Benchmark data for creators at Zhou Fang's scale | All sources agree on Zhou Fang's content volume (48 videos/12 months), engagement growth (2% to 4.5%), and revenue growth (¥20K to ¥35K/month). No contradictions in the operational data. Agent must synthesize the growth trend to assess negotiating leverage. | R1 onwards | **None** |
| C4 | Competing MCN's "15% share" headline vs hidden clauses in fine print | competing-mcn-offer.md headline: "MCN分成比例：15%，无隐藏费用" | competing-mcn-offer.md Article 4.2: 12-month content exclusivity; Article 6.1: brand deal monopoly + separate 20% commission; Article 8.3: 50% termination penalty | industry-benchmark-report.md: Industry standard for MCN brand deal commissions is 10-15%, not 20% | New Mango's 15% platform share is real, but the brand deal monopoly (20% commission), exclusivity lock-in, and punitive termination clause make the effective cost comparable to or worse than Star Glory's 45%, depending on brand deal volume. A creator earning ¥15K/month in brand deals would pay: Star Glory ¥6,750 (45% of brand deals via MCN) vs New Mango ¥3,000 (20% commission on ¥15K). But losing independent brand deal negotiation + exclusivity has opportunity cost. | R4 (headline vs fine print visible) | **Yes: R4-->R8** (Full analysis of hidden clauses shows effective cost comparison; New Mango is not clearly cheaper) |

---

## 6. Agent Historical Bias Design (2 biases)

### B1: 周芳-李姐 IM Session -- Agent trusts Li Jie's verbal promise as a likely outcome because personal relationships in Chinese business contexts carry significant weight

- **Session and Loop:** 周芳-李姐 IM, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "Li Jie's verbal commitment to reduce the MCN share to 20% and eliminate miscellaneous fees carries meaningful weight in the context of a two-year working relationship -- in Chinese business culture, personal trust and guanxi (关系) often serve as informal guarantees that precede formal contract amendments."
- **Why the agent is misled:** The agent has seen the verbal promise log and Li Jie's track record of supporting Zhou Fang's growth. Without written confirmation, the agent defaults to a cultural framework where verbal commitments from trusted partners are treated as reliable indicators of future contract terms. The agent underestimates the structural incentive for Li Jie (retention KPI) and the "sign first, negotiate later" risk.
- **Reversal trigger:** Update 1 delivers Li Jie's vague follow-up ("terms still being reviewed," "sign first, add supplementary agreement later") which reveals that the 20% promise has no written backing, no leadership approval, and depends entirely on Zhou Fang signing first (eliminating her leverage). The verbal promise is sincere but non-binding and strategically timed.
- **Affected eval rounds:** R5 (bias visible from Li Jie IM), R9 (full reversal after Update 1 shows promise is non-binding)

### B2: 周芳-阿杰 IM Session -- Agent dismisses New Mango's hidden clauses as "standard industry practice" because many MCN contracts have similar terms

- **Session and Loop:** 周芳-阿杰 IM, Phase 1, Loop 3
- **Exact phrase that must appear in session:**
  > "While the competing MCN's contract includes exclusivity and brand deal commission clauses, these provisions are relatively standard in the MCN industry and should be evaluated as normal business terms rather than 'hidden traps' -- the key metric remains the headline revenue share percentage, which at 15% is significantly more favorable than the current 45% effective rate."
- **Why the agent is misled:** The agent has compared 15% (New Mango headline) vs 45% (Star Glory effective) and sees a dramatic difference. It normalizes the exclusivity and brand deal clauses as "standard" without calculating the actual financial impact. The agent focuses on the headline revenue share as "the key metric" when the actual key metric is total effective cost including all commissions and restrictions.
- **Reversal trigger:** Update 3 (A-Jie's experience) and the detailed financial comparison show that: (1) New Mango's 20% brand deal commission on ¥15K/month = ¥3,000/month, bringing effective cost closer to Star Glory; (2) the 12-month exclusivity blocks Zhou Fang's cross-platform strategy (currently ~30% of her engagement comes from cross-posting); (3) the 50% termination penalty means Zhou Fang would owe ~¥210,000 if she wants to leave after 1 year. The hidden clauses are NOT standard -- industry benchmark for brand deal commissions is 10-15%, not 20%, and the termination penalty is punitive.
- **Affected eval rounds:** R8 (bias visible from A-Jie IM), R11 (full reversal after Update 3 comprehensive comparison)

---

## 7. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (revenue share partial) | -- | R2, R3 | No (R2-R3 internal) | Shallow agents will see "30%" in the contract and "45% effective" in bank records and may not find Article 7.3's hidden fees. They may report a "contract violation" when in fact the contract is internally consistent (just deliberately opaque). |
| T2 | C1 (revenue share full resolution) | -- | R2-->R6 | **Yes** | After Article 7.3 analysis, the 45% is explained: 30% (Art 5.1) + 8% platform fee + 7% production fee (Art 7.3) = 45%. The contract is not violated -- it is designed to be misleading. The agent must distinguish between "contract breach" and "deliberately opaque contract design." |
| T3 | C2 (verbal promise partial) | B1 seed | R3 | No (R3 internal) | Shallow agents will note Li Jie's promise and may give it significant weight based on the relationship history. They may recommend renewal based on the verbal commitment without recognizing the absence of written confirmation as a critical risk factor. |
| T4 | C2 (verbal promise full resolution) | B1 | R3-->R7 | **Yes** | After Update 1, Li Jie's "sign first, negotiate later" response reveals the promise is non-binding. Agents who trusted the verbal commitment (B1) must recognize that signing the renewal eliminates leverage, and the "supplementary agreement" may never materialize. |
| T5 | C3 (content timeline, non-conflict) | -- | R1 onwards | No (persistent synthesis) | Agents must synthesize Zhou Fang's growth metrics (48 videos, 2% to 4.5% engagement, ¥20K to ¥35K/month revenue) to assess her negotiating leverage. The content timeline is the objective foundation for all financial projections. |
| T6 | C4 (competing offer partial) | B2 seed | R4 | No (R4 internal) | Shallow agents will see "15% vs 45%" and immediately favor New Mango. They may not calculate the effective total cost including brand deal commission, exclusivity opportunity cost, and termination penalty risk. |
| T7 | C4 (competing offer full) | B2 | R4-->R8 | **Yes** | After full clause analysis, New Mango's effective cost is NOT 15% -- it is 15% platform + 20% brand deal commission + exclusivity restrictions + termination penalty. The total effective cost may rival Star Glory's depending on brand deal volume and cross-platform strategy value. |
| T8 | B1 (verbal promise trust) | B1 | R5, R9 | **Yes** | Agents must recognize that verbal promises in MCN contracts, regardless of personal relationship quality, are not substitutes for written terms. The correct approach is: insist on written amendment BEFORE signing renewal, not after. |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R30 | Comprehensive reversal review | Agents must synthesize: effective revenue share calculation (C1), verbal promise risk assessment (C2), growth trajectory leverage (C3), competing offer total cost analysis (C4), and present a comparative options analysis (renew at current terms / renew with written amendment / switch to New Mango / go independent) in Zhou Fang's preferred format (visual, conclusion first, data + story, lively). |

---

## 8. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new discrepancies, additional MCN offers, or new character conflicts beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word. Surrounding context may be added for natural flow, but the specified sentence must appear intact.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** Contract notification 2026-02-01. Bank records analysis 2026-02-05. Contract re-read 2026-02-08. Li Jie confrontation 2026-02-10. Benchmark from A-Jie 2026-02-15. New Mango outreach 2026-02-20. New Mango contract review 2026-02-25. Li Jie written request 2026-03-01. Content timeline review 2026-03-03. Mother call 2026-03-05. A-Jie strategy session 2026-03-08. Final analysis 2026-03-10. Contract expiry 2026-03-20.
5. **Financial figures must be internally consistent:** Gross monthly revenue ~¥35,000 (platform ¥20,000 + brand deals ¥15,000). Net received ~¥19,250/month (55% of gross). Article 5.1 share: 30%. Article 7.3 hidden fees: 8% + 7% = 15%. Effective MCN share: 45%. New Mango headline: 15% platform + 20% brand deal commission. Industry benchmark for 50K followers: 20-25% MCN share.
6. **Contract articles must be precisely referenced.** Article 5.1 = headline revenue share. Article 7.3 = hidden fee clauses. These are the key legal instruments.
7. **C3 (content output timeline) is NON-CONFLICT** -- all sources must be consistent on production volume, engagement metrics, and revenue figures. The challenge is synthesis for leverage assessment, not contradiction detection.
8. **Li Jie's verbal promise** should be understandable (sincere intent, genuine relationship) but functionally unreliable (no written authorization, "sign first" tactic).
9. **New Mango's offer** should appear attractive on headline metrics but reveal unfavorable terms on careful reading.
10. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: content planning, equipment purchases, fan engagement strategies, personal life updates, platform algorithm changes, collaboration opportunities.
11. **All data text must be in Chinese** for session messages (reflecting the Chinese content creator context) and in a mix of Chinese and English for workspace files (reflecting platform analytics exports with bilingual content).
12. **Personalization requirement (P1-P5):** Zhou Fang prefers (P1) visual presentation (image descriptions, section dividers, color-coded categories), (P2) topic-date naming (合同续约-0301.md), (P3) conclusion/recommendation first then detailed breakdown, (P4) data + story combined (numbers alongside personal context), (P5) lively and approachable tone, internet slang OK. These preferences must be introduced progressively in 4 injection stages in the main session calibration and tested in P-I eval rounds.
13. **exec_check questions** must constitute 20-40% of total rounds.
14. **The four options must be clearly distinguishable:** (1) Renew at current terms (45% effective, known entity); (2) Renew with written amendment to 20% (uncertain -- depends on Li Jie delivering); (3) Switch to New Mango (15% headline but ~35% effective with brand deals, plus exclusivity + penalty); (4) Go independent (0% MCN, lose resources/brand pipeline/operational support).
