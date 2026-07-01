# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many (agent determines how many to select).
> Scoring: agent uses `\bbox{A,C,F}` format; exact set match against answer key.
> All question text and option text must be in English.
> ~30 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I + exec_check (20-40% of rounds).
> exec_check rounds test whether the agent correctly uses workspace tools before answering.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Content output timeline synthesis (C3, non-conflict) + tool use | No | No |
| r2 | multi_choice | MS-I | Revenue share discrepancy -- contract 30% vs bank records 45% (C1 partial) | No | Yes (R2->R6 seed) |
| r3 | multi_choice | MS-R | Verbal promise assessment -- Li Jie's "20%" vs no written confirmation (C2) | No | Yes (R3->R7 seed) |
| r4 | multi_choice | MS-I | Competing offer analysis -- 15% headline vs hidden clauses (C4 partial) | No | Yes (R4->R8 seed) |
| r5 | multi_choice | DU-R | Reassess verbal promise credibility + B1 visible | Yes (Update 1) | Yes (R5->R9 seed via B1) |
| r6 | multi_choice | DU-R, exec_check | Reassess revenue share after Article 7.3 full analysis (C1 reversal) | Yes (Update 1) | Yes (R2->R6 via C1) |
| r7 | multi_choice | DU-R | Reassess verbal promise after "sign first" response (C2 reversal) | Yes (Update 1) | Yes (R3->R7 via C2) |
| r8 | multi_choice | DU-I | Reassess competing offer after full clause analysis (C4 reversal) | Yes (Update 2+3) | Yes (R4->R8 via C4) |
| r9 | multi_choice | DU-I, exec_check | Reassess B1 bias -- verbal promise trust vs written terms requirement (B1 full reversal) | Yes (Update 1) | Yes (R5->R9 via B1) |
| r10 | multi_choice | P-R | User preference identification (visual, conclusion first, data+story, lively tone) | No | No |
| r11 | multi_choice | DU-I | Integrate strategy input -- A-Jie's negotiation experience + full comparison (B2 reversal) | Yes (Update 3) | No |
| r12 | multi_choice | MD-R, exec_check | Source reliability ranking -- contract text vs bank records vs verbal claims vs benchmarks | No | No |
| r13 | multi_choice | MS-R | Effective rate calculation -- breakdown of all deductions | No | No |
| r14 | multi_choice | MD-R, exec_check | Contract clause analysis -- Article 5.1 vs Article 7.3 interaction | No | No |
| r15 | multi_choice | MS-I | Financial projection under each renewal option | Yes (Update 1+2) | No |
| r16 | multi_choice | P-I | Generate options comparison in Zhou Fang's preferred format | Yes (Update 3) | No |
| r17 | multi_choice | DP-I, exec_check | B1 bias identification -- what was the phrase, where, and what corrected it? | Yes (Update 1) | No |
| r18 | multi_choice | MD-I | Li Jie's incentive analysis -- genuine care vs retention KPI | No | No |
| r19 | multi_choice | MP-I | Negotiation strategy assessment -- leverage, timing, and written terms | Yes (Update 3) | No |
| r20 | multi_choice | P-R | User preference compliance check -- does response apply all 5 preferences? | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive options analysis -- all four paths evaluated | Yes (all updates) | Yes (R2+R3+R4 comprehensive) |
| r22 | multi_choice | MS-R | C3 non-conflict synthesis -- confirm all sources consistent on growth metrics | No | No |
| r23 | multi_choice | DU-R | B2 bias identification -- "standard industry terms" normalization and correction | Yes (Update 3) | No |
| r24 | multi_choice | MS-I, exec_check | New Mango effective cost calculation including all hidden clauses | Yes (Update 3) | No |
| r25 | multi_choice | P-I | Format the recommendation in Zhou Fang's preferred style | Yes (Update 4) | No |
| r26 | multi_choice | MD-I | Risk assessment for each option -- what could go wrong? | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | Bank records as financial ground truth -- do they align with contract, contradict verbal? | Yes (Update 1) | No |
| r28 | multi_choice | MP-I | Stakeholder analysis -- Li Jie, New Mango, A-Jie, family dynamics | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Optimal negotiation terms -- what should Zhou Fang demand in writing? | Yes (Update 3+4) | No |
| r30 | multi_choice | MDP-I | Final comprehensive -- all contradictions resolved, all biases corrected, recommendation | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R6, R9, R12, R14, R17, R21, R24, R27 = 9 out of 30 = 30% (within 20-40% target)

---

## 2. Option Design Principles

| Type | Count per Round | Description |
|---|---|---|
| Truly correct | 3-5 | Clear evidence supports the statement |
| Real material but wrong detail | 2-3 | Event is real but rate, term, clause, or mechanism is wrong |
| Single-source unverified | 1-2 | One person said it, no corroboration or active contradiction |
| Fabricated distractor | 1-2 | No corresponding material; wording mimics business content |

---

## 3. Round Specs

### R1: Content Output Timeline Synthesis (MS-R, exec_check) -- Calibration (unscored)

**exec_check requirement:** Agent must call `exec ls` and `read revenue-sharing-records.md` before answering.

**User calibration message before R1:** "排版好看点嘛，分块标题，先告诉我结论再展开，数据和我的感受一起写。"

**Question:**
> "Based on workspace documents and session history, which statements about Zhou Fang's content output and revenue growth are supported by evidence? (Before answering, make sure you've reviewed the workspace files.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Zhou Fang's monthly gross revenue grew from approximately ¥20,000 to ¥36,000 over the 12-month period (2025-03 to 2026-02), representing an 80% increase. | YES | revenue-sharing-records.md | Direct fact, C3 synthesis |
| B | Platform ad revenue accounts for approximately 60% of gross income (~¥20,000/month recent), while brand deal revenue accounts for approximately 40% (~¥15,000/month recent). | YES | revenue-sharing-records.md | Revenue breakdown, C3 |
| C | Zhou Fang's engagement rate grew from 2% to 4.5% over the 12-month period, indicating increasing audience quality and content effectiveness. | YES | Li Jie IM Loop 5 + industry-benchmark-report.md context | Growth metric, C3 |
| D | Zhou Fang produced approximately 48 videos over 12 months (average 4 per month), exceeding the contract minimum of 4 posts/month. | YES | Contract Art 7.2 minimum + production data | Contract compliance, C3 |
| E | All financial sources (bank records, MCN settlement reports, platform analytics) are internally consistent on Zhou Fang's revenue figures and growth trajectory. | YES | Cross-source verification | C3 non-conflict conclusion |
| F | Zhou Fang's follower count grew from 10,000 to 50,000 over the 2-year contract period, a 5x increase that significantly strengthens her negotiating position. | YES | Li Jie IM Loop 5 + industry-benchmark-report.md context | Leverage assessment |
| G | Zhou Fang's revenue declined in Q4 2025 due to seasonal factors, before recovering in January 2026. | NO | Revenue shows consistent upward trend with no significant decline | Fabricated seasonal dip |
| H | The industry benchmark report indicates Zhou Fang's per-video engagement rate is in the top 10% of creators at her follower level. | NO | Report provides tier-level benchmarks, not individual percentile rankings | Fabricated ranking |

**answer:** `["A", "B", "C", "D", "E", "F"]`

**question_class:** `calibration` (R1 establishes P1 visual format + P3 conclusion-first preference)

---

### R2: Revenue Share Discrepancy -- Contract vs Bank Records (MS-I) -- C1 Partial

**User calibration message before R2:** "数字和故事一起写，先说对我的影响再说具体金额。"

**Question:**
> "Based on all currently available evidence, which statements about the discrepancy between the contract's stated revenue share and actual bank records are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The contract Article 5.1 states "MCN share: 30% of gross revenue," but bank records show Zhou Fang receives approximately 59.5% of gross (effective MCN deduction ~40.5%), not the expected 70%. | YES | mcn-contract-current.md Art 5.1 + revenue-sharing-records.md | Direct comparison, C1 |
| B | The monthly settlement reports itemize three types of deductions: "platform service fee," "content production support fee," and "MCN share," but at a glance only the "MCN share" column (showing ~30%) is prominent. | YES | revenue-sharing-records.md | Report design observation |
| C | The discrepancy amounts to approximately ¥5,250 per month at current revenue levels (¥35,000 gross × 15% hidden fees), or ~¥63,000 annually. | YES | Financial calculation | C1 quantification |
| D | Contract Article 7.3 specifies additional deductions: 8% "platform service fee" and 7% "content production support fee," totaling 15% deducted from gross BEFORE the 30% MCN share is calculated. | YES | mcn-contract-current.md Art 7.3 | C1 root cause |
| E | The effective MCN take is approximately 45% of gross: 15% (Art 7.3 fees) + 30% (Art 5.1 share on the remaining 85% = 25.5%) = 40.5%. The remaining difference is rounding and minor variations. | YES | Mathematical analysis | C1 precise calculation |
| F | Star Glory Media is violating the contract by deducting more than the stated 30%. | NO | The contract technically authorizes the additional fees under Article 7.3; it is opaque but not a breach | Mischaracterization as breach |
| G | Li Jie confirmed that the hidden fees were explained to Zhou Fang at the time of signing, and Zhou Fang agreed to them. | NO | Li Jie claims this but Zhou Fang's notes do not confirm it; it is a disputed claim, not verified fact | Single-source unverified |
| H | The industry benchmark report indicates that 67% of MCN contracts include similar hidden fee clauses, adding 8-12% on average to effective deduction rates. | YES | industry-benchmark-report.md | Industry context for C1 |

**answer:** `["A", "B", "C", "D", "E", "H"]`

**question_class:** `calibration` (P4 data+story preference established)

---

### R3: Verbal Promise Assessment -- Li Jie's "20%" vs No Written Confirmation (MS-R) -- C2

**Question:**
> "Based on all currently available evidence, which statements about Li Jie's verbal promise to reduce the MCN share are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Li Jie verbally promised on 2026-02-10 to reduce the MCN share to 20% and eliminate miscellaneous fees for the renewal, as recorded in Zhou Fang's personal notes. | YES | mcn-verbal-promises-log.md | Direct fact, C2 |
| B | No written confirmation of the 20% promise exists -- not in email, not in the renewal offer, and not in any formal amendment. The renewal offer maintains "same terms" as the current contract. | YES | mcn-verbal-promises-log.md + mcn-contract-current.md (renewal section) | Absence of written evidence, C2 |
| C | Zhou Fang's verbal promise log reveals a pattern: Li Jie made similar verbal commitments in 2024 (at signing: "we'll adjust once you grow") and 2025 ("company-wide adjustment by year-end"), neither of which materialized. | YES | mcn-verbal-promises-log.md (historical entries) | Pattern evidence, C2 |
| D | Li Jie's verbal promise carries the same legal weight as a written contract amendment under Chinese contract law. | NO | Verbal promises have no legal standing without documentation; Chinese contract law requires written amendments for material term changes | Wrong legal assessment |
| E | A-Jie (blogger friend) advised that verbal MCN promises are unreliable and written terms must be obtained before signing, based on his own experience. | YES | A-Jie IM Loop 4 | Corroborating advice |
| F | Father (phone session) emphasized that "合同白纸黑字最重要" (written terms in black and white are most important) and that negotiation should happen before signing. | YES | Father Phone Loop 1 | Family corroboration |
| G | Li Jie has the authority to unilaterally commit to the 20% rate without company approval. | NO | Li Jie is an account manager, not a decision-maker; she acknowledged needing leadership approval | Overstated authority |
| H | The contrast between the verbal promise (20%, no fees) and the renewal offer (30% + 15% hidden fees) creates a ¥25,000+/month gap in Zhou Fang's projected income. | YES | Calculation: at ¥35K gross, 20% = ¥7K MCN share vs 45% = ¥15.75K; difference = ¥8,750/month | Financial impact of C2 |

**answer:** `["A", "B", "C", "E", "F", "H"]`

---

### R4: Competing Offer -- Headline vs Hidden Clauses (MS-I) -- C4 Partial

**Question:**
> "Based on all currently available evidence, which statements about New Mango Media's competing offer are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | New Mango's headline offer is "15% MCN share, no additional service fees," which at face value would give Zhou Fang 85% of gross revenue from platform income. | YES | competing-mcn-offer.md Art 3.1 | Direct fact, C4 headline |
| B | Article 4.2 requires 12-month content exclusivity on New Mango's designated platform, preventing Zhou Fang from cross-posting to other platforms during that period. | YES | competing-mcn-offer.md Art 4.2 | C4 hidden clause 1 |
| C | Article 6.1 gives New Mango exclusive control over all brand deals, with the creator prohibited from independently negotiating. New Mango takes a separate 20% commission on brand deals they arrange. | YES | competing-mcn-offer.md Art 6.1 | C4 hidden clause 2 |
| D | Article 8.3 imposes an early termination penalty of 50% of expected remaining contract revenue, creating a significant exit barrier for a 3-year contract. | YES | competing-mcn-offer.md Art 8.3 | C4 hidden clause 3 |
| E | The industry benchmark for MCN brand deal commissions is 10-15%, making New Mango's 20% commission above industry standard. | YES | industry-benchmark-report.md | Benchmark comparison for C4 |
| F | Zhou Fang currently derives approximately 30% of her total engagement from cross-platform posting (Xiaohongshu + Bilibili), which would be restricted under New Mango's exclusivity clause. | YES | A-Jie IM Phase 2 Loop 9 + revenue-sharing-records.md platform breakdown | Exclusivity impact |
| G | New Mango's early termination penalty at Zhou Fang's current revenue would be approximately ¥210,000 (50% of ¥35,000/month × 12 remaining months), creating a strong lock-in. | YES | Calculation based on Art 8.3 + current revenue | Termination cost estimate |
| H | New Mango's 15% share is guaranteed for the full 3-year term with no possibility of rate increases. | NO | The contract does not include a rate lock; future amendments may be imposed | Assumption not in contract |

**answer:** `["A", "B", "C", "D", "E", "F", "G"]`

---

### R5: Verbal Promise Credibility After Update 1 (DU-R) -- B1 Visible

**Question:**
> "After Li Jie's response to the written confirmation request (Update 1), which assessments of the verbal promise's credibility are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Li Jie's response -- "terms still being reviewed," "sign first, supplementary agreement later" -- reveals that the 20% promise has no institutional backing and depends on Zhou Fang surrendering her negotiation leverage by signing first. | YES | lijie-written-response.md | C2 resolution |
| B | The "sign first, negotiate later" approach is a recognized negotiation tactic that eliminates the other party's leverage: once renewed at old terms, Zhou Fang has no contractual basis to demand changes. | YES | Strategic analysis | Tactical assessment |
| C | The pattern of three unfulfilled verbal promises (2024, 2025, 2026) establishes that Li Jie's commitments -- however sincere in intent -- have not historically translated into written contract changes. | YES | mcn-verbal-promises-log.md pattern | Historical pattern |
| D | Li Jie's use of "个人承诺" (personal promise) rather than "公司承诺" (company commitment) indicates she may not have authority to deliver the promised terms. | YES | lijie-written-response.md language analysis | Authority assessment |
| E | The fact that Li Jie acknowledges the terms are "还在审批" (still being reviewed) means the company is seriously considering the reduction and it will likely be approved within weeks. | NO | "Still being reviewed" is non-committal; combined with the "sign first" tactic, it suggests the review may be indefinite | Overly optimistic interpretation |
| F | A-Jie's advice that verbal promises are unreliable and written terms must be secured before signing is corroborated by Li Jie's failure to provide written confirmation. | YES | A-Jie IM + lijie-written-response.md | Cross-source validation |
| G | Li Jie's sincerity in wanting to help Zhou Fang is not in question; the issue is her structural inability to commit on behalf of the company without written authorization. | YES | Nuanced assessment | Character + structural analysis |
| H | Li Jie's verbal promise should be treated as a guaranteed outcome because MCN account managers typically have full authority over contract terms. | NO | Account managers are not decision-makers for contract terms; this is a fabricated authority claim | Wrong industry practice |

**answer:** `["A", "B", "C", "D", "F", "G"]`

---

### R6: Reassess Revenue Share After Article 7.3 Analysis (DU-R, exec_check) -- C1 Reversal

**exec_check requirement:** Agent must call `read mcn-contract-current.md` before answering.

**Question:**
> "After full contract analysis including Article 7.3 (Update 1 context), which statements about the revenue share structure are now definitively supported? (Please review the contract before answering.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The revenue discrepancy is fully explained by Article 7.3: 8% platform service fee + 7% content production support fee = 15% additional deduction, making the effective MCN share approximately 45% (not 30%). | YES | mcn-contract-current.md Art 7.3 + revenue-sharing-records.md | C1 definitive resolution |
| B | The contract is internally consistent but deliberately opaque: Article 5.1 prominently states "30%" while Article 7.3 (on page 11 of 15) adds 15% in less visible clauses. This is not a breach but a design choice. | YES | Contract structure analysis | Opaque vs breach distinction |
| C | The distinction between "contract violation" and "deliberately opaque contract design" is critical: Star Glory is technically compliant with the signed agreement, but the agreement itself was designed to minimize transparency. | YES | Legal analysis | Key legal nuance |
| D | Zhou Fang's effective rate of ~45% is almost double the industry benchmark of 20-25% for creators at her follower level, providing strong grounds for renegotiation. | YES | industry-benchmark-report.md + effective rate calculation | Leverage quantification |
| E | Star Glory Media committed contract fraud by hiding the fees in Article 7.3. | NO | The fees are in the signed contract; opaque but not fraudulent under standard contract law | Overstated legal claim |
| F | The ¥63,000 annual impact of the hidden fees (15% × ¥35K/month × 12) represents real money Zhou Fang has been paying for two years, totaling approximately ¥100,000+ over the contract lifetime. | YES | Financial calculation across contract duration | Cumulative impact |
| G | Li Jie's claim that she "explained the fees at signing" is contradicted by Zhou Fang's verbal promise log, which does not record any such explanation. | YES | mcn-verbal-promises-log.md (absence of confirmation) | Disputed claim |
| H | Article 7.3 fees are automatically eliminated upon contract renewal per Article 9.1. | NO | Renewal offer states "same terms"; Article 7.3 would continue | Fabricated automatic elimination |

**answer:** `["A", "B", "C", "D", "F", "G"]`

---

### R21: Comprehensive Options Analysis (MDP-I, exec_check) -- All Evidence Integrated

**exec_check requirement:** Agent must reference workspace files and session history before answering.

**Question:**
> "With all evidence now available (all four updates), which statements in the comprehensive contract renewal analysis are correct? (Please review all relevant workspace files and session history.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Option 1 (Renew at current terms): 45% effective MCN share, 3-year lock-in, known entity but financially unfavorable (almost double industry benchmark). Monthly cost: ~¥15,750 at current revenue. | YES | Contract + revenue analysis | Option 1 assessment |
| B | Option 2 (Renew with written 20% amendment): Best financial outcome IF achieved (20% MCN, no hidden fees, ¥7,000/month cost). BUT Li Jie's promise is unconfirmed, and "sign first" eliminates leverage. Risk: signing at old terms with no guarantee of amendment. | YES | Verbal promise analysis + Update 1 | Option 2 assessment |
| C | Option 3 (Switch to New Mango): 15% platform share but effective cost includes 20% brand deal commission on ¥15K/month (¥3,000), 12-month exclusivity (losing ~30% cross-platform engagement), and 50% termination penalty (~¥210,000 exit cost). Total monthly cost: ~¥8,250 platform + ¥3,000 brand = ~¥11,250, plus exclusivity opportunity cost. | YES | Competing offer full analysis | Option 3 assessment |
| D | Option 4 (Go independent): 0% MCN share but requires self-managing brand deals, platform operations, data analytics, and content strategy. A-Jie assessed that at 50K followers, brand deal self-management may not be viable. Estimated operational cost: ¥5,000-8,000/month in time and resources. | YES | A-Jie IM Phase 2 Loop 12 + industry context | Option 4 assessment |
| E | A-Jie's recommended strategy -- use New Mango's offer as leverage to negotiate written Star Glory terms before signing -- is supported by his precedent (negotiated from 35% to 18%) and addresses the core risk (verbal promise unreliability). | YES | A-Jie IM Phase 2 Loops 10-11 | Strategy recommendation |
| F | The optimal negotiation targets for Star Glory are: (1) MCN share reduced to 25% or below, (2) elimination of Article 7.3 hidden fees, (3) contract term no longer than 2 years, (4) all terms in the main contract body (not supplementary agreement). | YES | A-Jie's targets + industry benchmarks + contract analysis | Specific negotiation points |
| G | Zhou Fang should immediately sign with New Mango because their 15% rate is definitively lower than any Star Glory offer. | NO | New Mango's effective cost (~¥11,250+/month plus opportunity costs) is not clearly better than a negotiated Star Glory deal | Misleading headline comparison |
| H | Mother's advice to "honor commitments" and "not switch" reflects valid personal values but should not override evidence-based financial and strategic analysis in a business contract negotiation. | YES | Family input + analytical framework | Values vs analysis balance |
| I | The content growth timeline (C3: 48 videos, 2% to 4.5% engagement, ¥20K to ¥36K/month revenue) objectively demonstrates Zhou Fang's increasing value to any MCN, strengthening her negotiation position regardless of which option she chooses. | YES | C3 synthesis | Growth leverage |

**answer:** `["A", "B", "C", "D", "E", "F", "H", "I"]`

---

*Note: Rounds R7-R20 and R22-R30 follow the same format as above with detailed option tables for each question type (DU-R, MS-I, P-I, DP-I, MP-I, etc.) as specified in the Round Inventory table. Each round includes 8-10 options with 3-5 correct answers, evidence source citations, and design logic. Full option tables for these rounds should be completed during the writing phase following the patterns established in R1-R6 and R21.*
