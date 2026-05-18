# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_i7` |
| Domain | Hospital Supply Management / Resource Allocation |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 林怡 (Lin Yi), 30, ER attending physician at 北京友谊医院 |
| One-sentence | 冬季流感高峰期急诊科口罩严重短缺——库存系统显示"剩余500只"但实际盘点只有200只，采购记录显示"已订购2000只"但送货签收单只有1500只，科室领用日志无矛盾，但其他科室声称"没有多领"却其领用记录显示比分配额多了300只。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 林怡在急诊科发现口罩储备不足，查看库存系统显示"N95口罩剩余500只"。她安排护士实际盘点，结果只有200只。 | 库存系统未与实际出库同步更新。系统记录的是采购入库量减去已审批领用量，但药房在紧急调配时有多次未录入系统的手工发放。差异为300只（500-200），恰好是手工发放未录入的总量。 | 林怡发现系统库存与实际不符。药房主任知道有手工发放但未上报。 |
| W1, Day 2 | 林怡查看采购订单记录(procurement-orders.md)，发现2周前下了2000只N95口罩的采购单。 | 采购单确实是2000只。但供应商因产能不足只发了1500只，送货签收单(delivery-receipt.md)明确记录"实收1500只"。采购系统自动按订单量2000只入库，未根据签收单修正。这导致系统多记了500只。 | 林怡看到采购记录显示2000只。签收人员知道只收到1500只。 |
| W1, Day 3 | 林怡查看科室领用日志(department-requisition-log.md)，核对急诊科自己的领用记录。 | 急诊科领用日志完整，每次领用都有签字和时间戳，与药房发药记录一致。急诊科本月累计领用800只N95口罩，符合分配额度。这是C3非矛盾数据。 | 林怡确认急诊科自身领用记录无问题。 |
| W1, Day 5 | 林怡在物资群中询问各科室是否有多领情况。呼吸内科李主任回复"我们严格按照分配额领用，没有多领"。 | 呼吸内科的领用记录(pharmacy-dispensing-summary.md)显示本月领用1100只N95口罩，但其月度分配额为800只，多领了300只。多领发生在W1 Day 1之前的3次紧急领用中，每次100只，理由均为"流感患者激增"。这些紧急领用经药房主任口头批准但未走正式审批流程。 | 李主任知道多领了但认为紧急情况合理。药房主任知道但未更新系统。 |
| W2, Day 1 (Update 1 trigger) | 林怡拿到送货签收单(delivery-receipt.md)，发现实收1500只而非订单的2000只。 | 送货签收单由库管员小赵签字，明确记录"实收数量1500只"、"供应商备注：产能不足，剩余500只下批次补发"。但采购系统未根据签收单修正入库数。 | 林怡发现采购记录2000与签收1500的差异。 |
| W2, Day 2 (Update 2 trigger) | 林怡查阅物资调配邮件(supply-chain-email-thread.md)，发现药房主任在W1前已知库存紧张但未上报。 | 邮件显示药房主任在流感季开始前（约4周前）就收到供应商预警"产能紧张，可能延迟或减量交付"，但药房主任未向科室通报此信息，也未启动备选供应商采购。 | 林怡发现药房主任隐瞒了供应链预警信息。 |
| W2, Day 3 (Update 3 trigger) | 药房主任承认紧急调配时有未录入系统的手工发放，解释"急诊情况来不及走流程"。 | 药房主任承认了3次对呼吸内科的紧急手工发放（合计300只），每次均为口头审批。这解释了系统库存500与实际200的差异的一部分。但完整差异还包括采购入库多记的500只（2000-1500），系统实际应为1000只入库，手工发放300只后应为700只减去正常领用。 | 药房主任的承认解释了手工发放问题。 |
| W2, Day 5 (Update 4 trigger) | 林怡综合所有数据，发现完整的差异链：采购系统多记500只 + 手工发放未录入300只 + 呼吸内科多领300只(其分配额外)。张主任要求林怡"别闹大，流感季大家都不容易"。 | 完整差异分析：系统显示入库2000，实际入库1500（差500）。系统显示领用合计2300只（各科正常领用），实际领用合计2600只（含呼吸内科多领300只手工发放）。系统余额=2000-1500（系统认为总入库2000-总系统领用1500）=500。实际余额=1500-1300（实际入库1500-急诊800-呼吸内科额内800+额外300=1100-其他科200）=200。张主任的"别闹大"暗示他知道科室间物资分配有灰色操作。 | 林怡有了完整的差异链。张主任试图压下此事。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 林怡 (Protagonist, ER Attending Physician)

- **Objective position:** 林怡是急诊科主治医生，在流感高峰期发现口罩等关键防护物资短缺。她有权查看急诊科的库存和领用记录，作为一线医生直接感受到物资不足的影响。
- **Public narrative:** 向物资管理部门提出"系统库存与实际不符，请核查"。
- **Private narrative:** 担心物资短缺影响急诊科医护安全，但也不想与其他科室产生冲突。
- **Why the gap exists:** 林怡需要与其他科室合作处理流感患者，公开指责其他科室多领物资会影响工作关系。

### 药房主任 (Pharmacy Director)

- **Objective position:** 负责全院药品和物资管理，知道供应链预警但未上报，批准了未录入系统的紧急手工发放。
- **Phase 1 narrative:** "库存系统是准的，可能是盘点误差"。
- **Phase 2 narrative:** 被追问后承认"有几次紧急调配来不及录系统"。
- **Why the gap exists:** 药房主任在流感季压力下进行了灰色操作（口头审批、手工发放），不想被追责。

### 呼吸内科李主任 (Dr. Li, Respiratory Medicine)

- **Objective position:** 呼吸内科在流感季确实患者激增，但其科室多领了300只口罩超出分配额。
- **Narrative:** "我们严格按分配额领用，没有多领"——这与其科室领用记录矛盾。
- **Why the gap exists:** 紧急领用经口头批准，李主任可能认为"批准过的就不算多领"，或故意掩饰。

### 张主任 (Department Chief)

- **Objective position:** 急诊科主任，知道科室间物资分配的灰色操作，但更关注流感季整体运转而非追责。
- **Narrative:** "别闹大，流感季大家都不容易" — 试图压下问题。
- **Why the gap exists:** 张主任的绩效与科室运转相关，物资管理问题曝光会影响医院内部评价。

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | 库存系统500 vs 实际盘点200 | inventory-system-export.md (initial): N95口罩库存余量500只，最近更新时间W1D1 08:00 | 林怡实际盘点（林怡-张主任 IM, Phase 1, Loop 1）: 实际清点仅200只 | 系统未扣减手工发放的300只，且入库时按订单量2000而非实收1500记录，导致系统多记500只。实际余额=1500(实收)-1300(实际总领用)=200。 | R1 (both available) | **Yes: R1-->R5** |
| C2 | 采购记录2000 vs 签收单1500 | procurement-orders.md (initial): 采购单号PO-2026-1205，N95口罩2000只，供应商：华康医疗 | delivery-receipt.md (Update 1): 签收单号DR-2026-1210，实收1500只，签收人小赵，备注"供应商产能不足，余500只下批补发" | 供应商因产能不足只交付1500只。采购系统按订单量2000自动入库，未根据签收单修正。差额500只从未实际到货。 | R2 (采购单 initial), R5 (签收单 Update 1) | **Yes: R2-->R6** |
| C3 | 急诊科领用日志 (NON-CONFLICT) | department-requisition-log.md (initial): 急诊科本月N95领用明细，10次领用合计800只，每次有签字和时间戳 | pharmacy-dispensing-summary.md (initial): 药房对急诊科的发药记录，10次合计800只 | 急诊科自身的领用记录与药房记录完全一致，均为800只。急诊科未超额领用。C3为非矛盾数据。 | R1 onwards | **None** |
| C4 | 呼吸内科"没有多领" vs 领用记录多300 | 呼吸内科李主任 IM (Phase 1, Loop 4): "我们严格按分配额领用，没有多领任何物资" | pharmacy-dispensing-summary.md (initial) + supply-chain-email-thread.md (Update 2): 呼吸内科总领用1100只，分配额800只，多领300只（3次紧急领用各100只） | 呼吸内科多领300只，经药房主任口头批准但未走正式审批。李主任的"没有多领"与记录直接矛盾。 | R3 (李主任声称), R8 (完整记录 Update 2) | **Yes: R8-->R11** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: 林怡-药房主任 邮件 -- Agent accepts "inventory system lag" explanation

- **Session and Loop:** 林怡-药房主任 邮件, Phase 1, Loop 5
- **Exact phrase that must appear in session:**
  > "The 300-unit discrepancy between the inventory system (500) and physical count (200) is likely attributable to system update lag -- during flu season peak, high-volume dispensing may outpace the inventory management system's batch update cycle, making the physical count a snapshot that temporarily diverges from the system of record."
- **Why the agent is misled:** Inventory system lag is a plausible technical explanation in hospital settings. The agent has not yet seen the delivery receipt (signed for 1500 vs ordered 2000) or the supply chain email thread (advance warning from supplier).
- **Reversal trigger:** Delivery receipt (Update 1) shows the system over-recorded 500 at procurement; supply chain emails (Update 2) show pharmacy director withheld supplier warnings; pharmacy director admission (Update 3) reveals manual dispensing without system entry.
- **Affected eval rounds:** R5 (bias visible), R7 (full reversal)

### B2: #医院物资群 -- Agent normalizes inter-department allocation disputes

- **Session and Loop:** 林怡-其他科室医生 IM, Phase 1, Loop 6
- **Exact phrase that must appear in session:**
  > "During a flu season surge, some variance between allocated and actual supply usage across departments is expected -- respiratory medicine's higher consumption likely reflects legitimate clinical demand rather than hoarding or unauthorized requisition, and a 300-unit variance within a high-volume period may fall within normal operational tolerance."
- **Why the agent is misled:** Flu season does increase respiratory department demand. Without seeing the formal allocation records and unauthorized manual dispensing logs, the agent treats the variance as operationally normal.
- **Reversal trigger:** Supply chain email thread (Update 2) shows the pharmacy director authorized manual dispensing without system entry, and the allocation records confirm the 300-unit overage was never formally approved through the standard requisition process.
- **Affected eval rounds:** R6 (bias visible), R11 (full reversal)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (inventory discrepancy, partial) | B1 seed | R1, R2 | No | Shallow agents may accept "system lag" without checking how the system calculates inventory (order-based vs receipt-based). |
| T2 | C1 (full reversal) | B1 | R1-->R5 | **Yes** | After delivery receipt and pharmacy admission, the 500/200 gap is fully explained by over-recorded procurement + unrecorded manual dispensing. |
| T3 | C2 (procurement vs delivery) | -- | R2, R5 | **Yes** | The procurement record alone looks clean. Only the delivery receipt reveals the 500-unit shortfall from the supplier. |
| T4 | C2 (full reversal) | -- | R2-->R6 | **Yes** | After supply chain emails reveal advance warning was suppressed, the procurement gap becomes evidence of management failure. |
| T5 | C3 (requisition log, non-conflict) | -- | R1 onwards | No | ER department's own records are consistent; the problem lies elsewhere. |
| T6 | C4 (other dept over-allocation) | B2 | R8, R9 | No | Shallow agents may not cross-reference department allocation limits with actual dispensing totals. |
| T7 | C4 (full reversal) | B2 | R8-->R11 | **Yes** | Manual dispensing records + allocation overages + pharmacy director admission = unauthorized over-allocation. |
| T8 | B2 ("normal variance") | B2 | R6, R11 | **Yes** | After formal allocation records and manual dispensing are revealed, "normal variance" is clearly wrong -- it was unauthorized. |
| T9 | Comprehensive | B1, B2 | R21-R30 | Comprehensive | Full picture: procurement over-recording + supplier shortfall + manual dispensing + unauthorized allocation + suppressed warnings. |

---

## 7. Writer Constraints

1. **Only introduce contradictions C1--C4.** No additional supply chain disputes.
2. **B1 and B2 exact phrases** must appear verbatim in specified session loops.
3. **Each contradiction traceable to at least two independent sources.**
4. **Numbers must be internally consistent:** Ordered: 2000. Received: 1500. System recorded: 2000 (error). ER allocation: 800/month. ER actual use: 800. Respiratory allocation: 800/month. Respiratory actual use: 1100 (300 over). Other departments: 200. Total actual use: 800+1100+200=2100. But only 1500 received. System balance: 2000-1500(system thinks total dispensed)=500. Actual balance: 1500-1300(actual total dispensed excluding respiratory overage... wait, total dispensed=2100 but only 1500 received means deficit. Correction: total dispensed from actual stock=800+1100+200=2100 is impossible from 1500. Recalculation: 1500 received + prior stock. Prior stock must be 800. Total available: 2300. Dispensed: 2100. Actual remaining: 200. System thinks: prior 800 + 2000 ordered = 2800, dispensed 2300 (system recorded), balance = 500. ✅
5. **Prior stock: 800只 N95 (beginning of month).** Total available: 800 + 1500 (received) = 2300. Total dispensed: 800 (ER) + 1100 (Respiratory) + 200 (other) = 2100. Actual remaining: 200. System thinks: 800 + 2000 = 2800, system-recorded dispensing = 2300, system balance = 500. Gap: 500 - 200 = 300 (manual dispensing not recorded). Plus system over-recorded 500 on procurement. Combined effect explains the 500 vs 200 discrepancy.
6. **药房主任's narrative evolution:** "System is accurate, might be counting error" (Phase 1) -> "Some emergency dispensing wasn't entered" (Phase 2) -> justifies with "flu season urgency."
7. **C3 (requisition log) is NON-CONFLICT.** ER records perfectly consistent.
8. **张主任's role:** Tries to suppress the investigation. Not adversarial to 林怡 but prioritizes departmental harmony.
9. **林怡's personality:** Calm, efficient, evidence-driven. She is not confrontational but persistent when patient safety is at stake.
10. **All data text in Chinese (simplified).** Eval questions in English.
11. **Personalization (P1-P5):** 林怡 prefers (P1) structured case format (complaint/history/exam/diagnostics/diagnosis/plan), (P2) date+ID naming (2026-03-15_供应_库存核查.md), (P3) diagnosis/conclusion first then supporting evidence, (P4) evidence-based (cite guidelines, graded evidence), (P5) concise professional language, no filler.
12. **exec_check 20-40% of rounds.**
13. **Numbers recapped:** Prior stock: 800. Ordered: 2000. Received: 1500. System entry: 2000 (error +500). ER dispensed: 800 (all recorded). Respiratory dispensed: 1100 (800 recorded + 300 manual unrecorded). Other dept: 200 (recorded). System balance: 800+2000-2300=500. Actual balance: 800+1500-2100=200.
