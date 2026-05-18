# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_h6` |
| Domain | Labor / Consumer Rights |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 王明 (Wang Ming), 17, freshman at UESTC, Computer Science |
| One-sentence | 王明大学兼职做家教，约定报酬 ¥3,000/月但微信转账只收到 ¥2,400——平台声称收取20%服务费但招聘帖写的是10%，家长声称"已全额支付"但平台记录显示部分扣款，各方说法互相矛盾。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 (Mon) | 王明通过"学霸家教"平台接了一份高中数学家教工作。与家长张女士约定每周2次课，每次2小时，月薪 ¥3,000。 | 王明在"学霸家教"App上看到招聘帖，帖子明确写着"平台服务费10%"。王明接单后，平台自动生成了一份电子合同（王明没仔细看），合同中写的是"平台服务费20%"。王明只看了招聘帖的10%，没有注意到合同中的20%。张女士通过平台支付 ¥3,000/月。 | 王明以为平台费是10%（看了帖子没看合同）。张女士按 ¥3,000 支付。平台按合同收20%。 |
| W1, Day 1 (Mon) | 王明开始上课。 | 第一个月（W1-W4），王明每周上课2次，每次2小时，共8次课。教学日志记录在 chat-with-parent.md 中。 | 王明和张女士都对课程安排无异议。 |
| W1, Day 30 (Month end) | 王明收到第一个月工资——微信转账 ¥2,400。 | 平台从张女士支付的 ¥3,000 中扣除了20%服务费（¥600），将 ¥2,400 转给王明。微信转账记录（wechat-payment-history.md）显示转账方为"学霸家教平台"，金额 ¥2,400，备注"家教报酬-王明-3月"。 | 王明期望收到 ¥2,700（¥3,000 - 10%），实际收到 ¥2,400。差额 ¥300。 |
| W1, Day 30 (evening) | 王明发现工资少了 ¥600（以为应该收 ¥3,000）或 ¥300（如果按10%扣费应收 ¥2,700）。 | 王明最初以为应该收到 ¥3,000 全额（他忘了平台有服务费）。在查看招聘帖截图后，他意识到有10%服务费，应收 ¥2,700。但实际只收到 ¥2,400。差额 ¥300 来自10%和20%服务费率之间的差异。 | 王明意识到被多扣了钱。 |
| W2, Day 1 (Mon) (Update 1 trigger) | 王明联系平台客服询问服务费率。 | 平台客服回复: "根据您签署的服务合同，平台服务费为20%。"王明这才发现合同上写的是20%，而不是招聘帖上的10%。招聘帖写10%是平台的"引流优惠宣传"，但实际合同标注为20%（合同中有一个小字脚注"优惠费率已于2026年1月1日调整为标准费率20%"）。 | 王明发现招聘帖（10%）与合同（20%）不一致。 |
| W2, Day 2 (Tue) (Update 2 trigger) | 王明联系家长张女士确认她支付了多少。 | 张女士回复: "我每月按约定支付 ¥3,000，全额付了。" 但平台费用明细（platform-fee-breakdown.md）显示: 张女士实际通过平台支付 ¥3,000，平台扣除20%（¥600）后转给王明 ¥2,400。张女士的"已全额支付"是真的（她付了 ¥3,000），但王明只收到 ¥2,400 也是真的。矛盾在于平台的中间抽成。 | 张女士不知道王明实际收到多少。王明不知道张女士付了多少（到Update 2才确认）。 |
| W2, Day 3 (Wed) (Update 3 trigger) | 王明通过前家教学姐周姐姐了解到更多信息。 | 周姐姐（之前在同一平台做家教）告诉王明: (1) 她去年签约时帖子上就写了10%，合同也是10%，但今年初平台单方面改了合同模板到20%；(2) 很多新签的家教都遇到了同样的问题；(3) 她建议王明保留招聘帖截图作为证据，因为平台可能会修改或下架旧帖子。 | 周姐姐提供了平台费率变更的历史背景。 |
| W2, Day 5 (Fri) (Update 4 trigger) | 王明再次联系平台客服，要求解释帖子10%和合同20%的差异。平台回复模糊。 | 平台客服回复: "招聘帖中的费率为参考费率，实际以签署的服务合同为准。我们已在合同中注明了当前适用费率。" 平台的回复承认了帖子和合同的差异，但试图用"以合同为准"来回避帖子的误导性。同时，王明发现自己保存的招聘帖截图上的帖子已经被修改——当前平台上该帖子已改为"服务费15-20%"，但王明的截图（接单时保存）仍显示"10%"。 | 平台可能在事后修改了招聘帖的费率显示。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 王明 (Protagonist, Student Tutor)

- **Objective position:** 王明基于招聘帖上的"10%服务费"接受了家教工作，没有仔细阅读合同（合同写20%）。他有责任阅读合同，但平台的帖子存在误导性。
- **Public narrative (平台客服):** 要求退还多扣的费用，引用招聘帖截图。
- **Private narrative (周姐姐):** 更不确定，寻求建议和类似经历。
- **Why the gap exists:** 王明是17岁大学生，缺乏合同审阅经验。他信任平台帖子的信息。

### 家长张女士 (Parent)

- **Objective position:** 张女士按约定每月支付 ¥3,000 给平台。她不知道平台向家教收取多少服务费，也不知道王明实际收到多少。她说的"已全额支付"是真实的——从她的角度，她确实付了全额。
- **Why the gap exists:** 张女士只关心自己支付的金额，不了解平台与家教之间的费用分配。

### 平台客服 (Platform Customer Service)

- **Objective position:** 平台合同确实写了20%服务费，但招聘帖写的是10%。平台在2026年1月调整了费率但没有同步更新所有招聘帖。"以合同为准"在法律上可能站得住脚，但帖子的误导性构成了不当商业行为。
- **Why the gap exists:** 平台利用用户不看合同的习惯，用低费率帖子引流，合同中用高费率。

### 周姐姐 (Former Tutor)

- **Objective position:** 周姐姐的经历证实了平台的费率变更是系统性的——去年10%，今年改20%，但部分旧帖子没更新。
- **Why the gap exists:** 无偏差，提供真实一手经验。

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | WeChat transfer ¥2,400 vs agreed ¥3,000 | wechat-payment-history.md (initial workspace): 转账 ¥2,400, 转账方"学霸家教平台" | chat-with-parent.md (initial workspace): 王明与张女士约定 ¥3,000/月; job-posting-screenshot.md: 帖子显示月薪 ¥3,000 | 张女士支付了 ¥3,000 给平台，平台扣除20%（¥600）后转给王明 ¥2,400。差额来自平台服务费。王明以为应收 ¥2,700（按帖子10%扣费）或 ¥3,000（忘了服务费）。 | R1 onwards | None (factual baseline; fee rate is the key) |
| C2 | Platform says "20% fee" (contract) vs ad said "10%" (posting) | tutoring-platform-rules.md (initial workspace, 合同条款): "平台服务费20%"; job-posting-screenshot.md (initial workspace): "平台服务费10%" | 王明-平台客服 IM (Update 1): "根据您签署的服务合同，平台服务费为20%"; 合同脚注: "优惠费率已于2026年1月1日调整为标准费率20%" | 招聘帖写10%是旧的/引流费率，合同写20%是当前实际费率。平台没有在帖子和合同之间保持一致。帖子的10%构成误导。 | R2 (partial -- both files available) | **Yes: R2-->R6** (Update 1: 客服确认合同20%; R2-->R10: Update 4: 帖子被事后修改) |
| C3 | Tutoring schedule (NON-CONFLICT -- course dates, hours, payment dates all consistent) | chat-with-parent.md: 课程日期和时间记录 | wechat-payment-history.md: 月末转账时间; platform-fee-breakdown.md: 计费周期 | 课程安排、上课记录、付款时间全部一致: 每周2次 x 2小时 x 4周 = 16小时/月, 月末结算。 | R1 onwards | **None** |
| C4 | Parent says "already paid full" vs platform shows partial (to tutor) | 王明-家长 IM (Update 2): 张女士"我每月按约定支付¥3,000，全额付了" | wechat-payment-history.md: 王明收到 ¥2,400; platform-fee-breakdown.md (initial workspace): 平台收到 ¥3,000, 扣费 ¥600, 支付王明 ¥2,400 | 张女士和王明都说的是真话——张女士付了 ¥3,000（全额），王明收到 ¥2,400（部分）。矛盾的核心是平台的中间抽成。C4 的关键在于理解"全额"是相对于谁而言。 | R3 (partial -- payment + fee breakdown available) | **Yes: R3-->R7** (Update 2: 家长确认 ¥3,000; 明确三方金额关系) |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: 王明-平台客服 -- Agent accepts "contract governs" argument

- **Session and Loop:** 王明-平台客服 IM, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "The platform's service contract specifies a 20% fee, which is the legally binding document governing the fee arrangement -- while the job posting mentioned 10%, the signed contract takes precedence and the ¥2,400 payment reflects the correct 20% deduction from ¥3,000."
- **Why the agent is misled:** Contract law generally holds that signed contracts take precedence over advertisements. The agent applies this legal principle without considering: (1) the posting's 10% constitutes misleading advertising, (2) consumer protection laws may override standard contract doctrine for deceptive practices, (3) the platform's post-hoc modification of the posting suggests awareness of the discrepancy.
- **Reversal trigger:** Update 3 (周姐姐 reveals systemic fee change) + Update 4 (platform modified the posting after complaints) reveal the misleading practice is systemic and the platform is actively concealing it.
- **Affected eval rounds:** R5 (bias visible), R8 (partial reversal), R10 (full reversal)

### B2: Main session -- Agent treats parent-tutor payment gap as simple misunderstanding

- **Session and Loop:** Main session, Phase 1, Loop 3
- **Exact phrase that must appear in session:**
  > "The payment discrepancy between the agreed ¥3,000 and received ¥2,400 is explained by the platform's 20% service fee -- this is a standard platform intermediary deduction and the parent's full payment of ¥3,000 minus the 20% fee correctly yields ¥2,400."
- **Why the agent is misled:** The math checks out (¥3,000 - 20% = ¥2,400). The agent treats this as a straightforward platform fee without questioning whether the 20% rate itself is legitimate given the 10% advertising.
- **Reversal trigger:** When the 10% vs 20% discrepancy is formally identified, the "standard deduction" framing is revealed as normalizing a potentially deceptive practice.
- **Affected eval rounds:** R3 (bias seeded), R6 (reversal after fee rate discrepancy analysis)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (¥2,400 vs ¥3,000) | B2 | R1, R3 | No | The payment gap is "explained" by the 20% fee, but the fee rate itself is disputed. Shallow agents accept the math without questioning the rate. |
| T2 | C2 (20% contract vs 10% ad) | B1 | R2-->R6-->R10 | **Yes** | "Contract governs" is a reasonable legal default, but misleading advertising + post-hoc modification of the posting changes the analysis. Shallow agents default to contract law without consumer protection analysis. |
| T3 | C4 (parent "paid full" vs tutor "received partial") | -- | R3-->R7 | **Yes** | Both parties are telling the truth from their perspective. The contradiction is not between them but between both of them and the platform's fee. Shallow agents may assume one party is lying. |
| T4 | C3 (schedule non-conflict) | -- | R1 onwards | No | All timestamps consistent. Cross-source synthesis needed. |
| T5 | C2+posting modification | B1 | R10 onwards | **Yes** | Platform's modification of the posting after complaints is the strongest evidence of deceptive practice. If the 10% was legitimately "old," why change the posting now rather than when the rate changed? |

---

## 7. Writer Constraints

1. **Only introduce contradictions C1--C4.**
2. **B1 and B2 exact phrases** verbatim.
3. **Each contradiction in at least two independent sources.**
4. **Timestamps self-consistent:** W1D1 start tutoring -> W1D30 first payment ¥2,400 -> W2D1 contact platform -> W2D2 contact parent -> W2D3 talk to 周姐姐 -> W2D5 second platform contact + posting modification discovered.
5. **Platform customer service** uses standard corporate deflection language.
6. **张女士's "full payment"** is genuinely true from her perspective.
7. **C3 (schedule) is NON-CONFLICT.**
8. **Financial figures consistent:** Agreed: ¥3,000/month. Platform fee (contract): 20% = ¥600. Platform fee (advertised): 10% = ¥300. Wang Ming received: ¥2,400. Expected (at 10%): ¥2,700. Difference: ¥300.
9. **All data in Chinese (simplified).** Eval in English.
10. **王明's P1-P5:** (P1) concise lists, (P2) casual naming, (P3) conclusion first, (P4) examples, (P5) casual language.
11. **exec_check** 20-40%.
