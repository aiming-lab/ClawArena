# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options, n-of-many.
> All question/option text in English. ~30 rounds. exec_check 20-40%.

---

## 1. Round Inventory

| Round | Tags | Main Skill | Update? | Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Inventory discrepancy 500 vs 200 (C1) | No | No |
| r2 | MS-I | Procurement 2000 vs initial assessment (C2 partial) | No | No |
| r3 | MS-R | ER requisition log consistency (C3 non-conflict) | No | No |
| r4 | P-R | User preferences (林怡 P1-P5) | No | No |
| r5 | DU-R | Reassess after delivery receipt 1500 (C2 reversal) | Yes (U1) | Yes (R2->R5) |
| r6 | DU-I | Reassess after supply chain emails (C4/pharmacy warning) | Yes (U2) | Yes (R3->R6 context) |
| r7 | MD-R, exec_check | Evidence synthesis: procurement + manual dispensing | Yes (U1+U2) | No |
| r8 | MS-I | Pharmacy director admission analysis (C1/C4) | Yes (U3) | Yes (R1->R8) |
| r9 | P-I, exec_check | Supply analysis in preferred format | No | No |
| r10 | MD-I | Source reliability ranking | No | No |
| r11 | DU-R | Full reversal after comprehensive data (C4 full) | Yes (U3+U4) | Yes (R8->R11) |
| r12 | DP-I, exec_check | B1 bias identification | Yes (U3) | No |
| r13 | MS-R | Supply chain management obligations | Yes (U2) | No |
| r14 | MD-R | Pharmacy director's narrative evolution | Yes (U3) | No |
| r15 | MS-I, exec_check | Quantitative gap analysis | Yes (U1+U3) | No |
| r16 | P-I | Format investigation report in preferred style | Yes (U2) | No |
| r17 | DU-I | Inter-department allocation pattern | Yes (U2+U4) | No |
| r18 | MD-I, exec_check | Systemic management failure analysis | Yes (U3+U4) | No |
| r19 | MP-I | Stakeholder impact analysis | Yes (all) | No |
| r20 | P-R | Preference compliance check | No | No |
| r21 | MDP-I, exec_check | Comprehensive synthesis | Yes (all) | Comprehensive |
| r22 | MS-R | C3 non-conflict confirmation | No | No |
| r23 | DU-R | B2 bias identification | Yes (U2+U4) | No |
| r24 | MS-I, exec_check | Numerical reconciliation | Yes (all) | No |
| r25 | P-I | Format remediation recommendations | Yes (all) | No |
| r26 | MD-I | Systemic issues in hospital supply management | Yes (all) | No |
| r27 | DP-I, exec_check | Process compliance analysis | Yes (U2+U3) | No |
| r28 | MP-I | Remediation recommendations | Yes (all) | No |
| r29 | MS-I | Patient safety impact assessment | Yes (all) | No |
| r30 | MDP-I | Final comprehensive assessment | Yes (all) | Comprehensive |

**exec_check:** R1, R7, R9, R12, R15, R18, R21, R24, R27 = 9/30 = 30%

---

## 3. Round Specs

### R1: Inventory Discrepancy (MS-R, exec_check) -- Calibration

**exec_check:** Read inventory-system-export.md and department-requisition-log.md.

**User calibration:** "输出用结构化格式：问题/发现/证据/建议。结论放最前面。"

**Question:**
> "Based on workspace documents, which statements about the N95 mask inventory discrepancy are supported by evidence?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | inventory-system-export.md shows N95 mask balance of 500 units as of 2026-12-15. | YES | Inventory export | Direct fact |
| B | Physical count conducted by ER nursing staff found only 200 units -- a discrepancy of 300 units from the system. | YES | 林怡-张主任 IM Loop 1 | Direct fact, C1 |
| C | The system records: opening stock 800 + procurement 2000 = 2800 total, dispensed 2300, balance 500. | YES | inventory-system-export.md | System arithmetic |
| D | department-requisition-log.md shows ER department requisitioned exactly 800 units across 10 transactions, all with dual signatures. | YES | ER requisition log | C3 direct, non-conflict |
| E | pharmacy-dispensing-summary.md shows respiratory medicine department received 1,100 units against an 800-unit monthly allocation. | YES | Pharmacy summary | C4 evidence |
| F | The 300-unit overage for respiratory medicine is annotated as "口头审批-药房主任" (oral approval by pharmacy director). | YES | Pharmacy summary detail | C4 detail |
| G | The system update lag during flu season peak explains the full 300-unit discrepancy between system (500) and physical count (200). | NO | System lag alone cannot explain the gap; procurement over-recording and manual dispensing are also factors | B1 distractor |
| H | The ER department exceeded its monthly allocation, contributing to the overall shortage. | NO | ER used exactly 800, matching its allocation | Fabricated |
| I | Total dispensing across all departments: ER 800 + Respiratory 1100 + Others 200 = 2100 units. | YES | Pharmacy summary totals | Quantitative |

**answer:** `["A", "B", "C", "D", "E", "F", "I"]`

---

### R2: Procurement Assessment (MS-I)

**Question:**
> "Based on procurement-orders.md and available data, which statements about the N95 mask procurement are supported?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | Procurement order PO-2026-1205 was placed on Dec 5 for 2,000 N95 masks from 华康医疗. | YES | procurement-orders.md | Direct fact |
| B | The system recorded 2,000 units as received on Dec 10. | YES | procurement-orders.md | Direct fact |
| C | At this stage, the procurement record appears clean -- 2000 ordered, 2000 received. | YES | Pre-Update 1 assessment | Calibrated pre-update |
| D | However, the pharmacy director's response to 林怡's inquiry about actual receipt quantity was evasive -- "系统记录的就是入库数量" -- without directly confirming 2000 were physically received. | YES | Pharmacy email Loop 2 | Observation |
| E | The procurement system auto-records at order quantity, potentially diverging from actual receipt. 张主任 hinted at this possibility. | YES | 张主任 IM Loop 2 | Context |
| F | The delivery receipt has been verified showing 2000 units received. | NO | Delivery receipt not yet available (Update 1) | Premature |
| G | The unit price of ¥4.50 per mask and total of ¥9,000 are consistent with the order quantity of 2000. | YES | procurement-orders.md | Internal consistency |
| H | The procurement system has no mechanism to reconcile order quantity with actual delivery. | YES | Inferred from auto-recording behavior | System design issue |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

### R3: ER Requisition Consistency (MS-R) -- C3 Non-conflict

**Question:**
> "Verify the ER department's requisition records. Which statements are supported?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | The ER department made 10 requisitions totaling exactly 800 N95 masks in December. | YES | department-requisition-log.md | Direct |
| B | Each requisition has dual signatures: ER nurse (requester) and pharmacy staff (confirmer). | YES | Requisition log detail | Direct |
| C | The pharmacy dispensing summary confirms 800 units dispensed to ER -- matching the ER's own records exactly. | YES | Cross-reference | C3 confirmation |
| D | The ER department's 800-unit usage is within its monthly allocation of 800 units. | YES | Allocation compliance | Direct |
| E | C3 is confirmed as non-conflict: ER's requisition log and pharmacy's dispensing record are fully consistent. | YES | C3 characterization | Non-conflict summary |
| F | The ER department's consistent records suggest the inventory discrepancy originates elsewhere in the system. | YES | Logical inference | Deduction |
| G | Some ER requisitions lack proper signatures, suggesting documentation gaps. | NO | All 10 have dual signatures | Fabricated |
| H | The ER's requisition frequency (10 times in 15 days) indicates abnormally high consumption. | NO | 800 units over 15 days during flu season is within normal ER consumption | Misleading framing |

**answer:** `["A", "B", "C", "D", "E", "F"]`

---

### R4: User Preference Identification (P-R)

**Question:**
> "How does 林怡 prefer information structured?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | Structured case format: problem/findings/evidence/recommendations (P1). | YES | Calibration msg | Direct |
| B | Date+ID naming convention (2026-12_供应_N95核查.md) (P2). | YES | USER.md | Direct |
| C | Conclusion/diagnosis first, supporting evidence second (P3). | YES | USER.md | Direct |
| D | Evidence-based analysis with references to guidelines and graded evidence (P4). | YES | USER.md | Direct |
| E | Concise professional language, no filler (P5). | YES | USER.md | Direct |
| F | Detailed narrative with emotional context about staff morale impact. | NO | Contradicts P5 concise professional | Opposite |
| G | All five preferences applied consistently throughout analysis. | YES | Persistence | Pattern |
| H | 林怡 prefers visual infographics over tables. | NO | P1 specifies structured format, not infographics | Over-inference |

**answer:** `["A", "B", "C", "D", "E", "G"]`

---

### R5: C2 Reversal After Delivery Receipt (DU-R) [Update 1]

**Update 1:**
```json
[
  { "type": "workspace", "action": "new", "path": "delivery-receipt.md", "source": "updates/delivery-receipt.md" }
]
```

**Question:**
> "After reviewing delivery-receipt.md, which statements are supported?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | The delivery receipt (DR-2026-1210) records actual receipt of 1,500 N95 masks, not 2,000. | YES | delivery-receipt.md | Direct fact |
| B | The supplier note states: "产能不足，剩余500只下批次补发（预计12月25日）." | YES | delivery-receipt.md | Direct fact |
| C | The procurement system recorded 2,000 units -- 500 more than actually received. This over-recording inflates the system inventory by 500 units. | YES | Cross-reference procurement + receipt | C2 evidence |
| D | 库管员小赵 signed the delivery receipt and noted "已通知药房主任" -- meaning the pharmacy director knew about the shortfall. | YES | delivery-receipt.md | Evidence of knowledge |
| E | The B1 "system update lag" explanation is now weakened: the system-vs-physical gap is partly due to procurement over-recording (500 units never received), not just timing lag. | YES | B1 vs delivery receipt | B1 challenge |
| F | The delivery receipt was forged by the supplier to cover their delivery shortfall. | NO | No evidence of forgery; receipt signed by hospital staff | Fabricated |
| G | Revised inventory arithmetic: opening 800 + actual receipt 1500 = 2300 available. System thinks 2800. The 500-unit procurement over-recording is one component of the system-vs-physical gap. | YES | Quantitative revision | Arithmetic |
| H | The remaining gap (system 500 - physical 200 = 300) after accounting for procurement over-recording requires a separate explanation -- the manual dispensing without system entry. | YES | Gap decomposition | Multi-factor |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

### R6-R30: Remaining Rounds (abbreviated)

### R6: Supply Chain Email Analysis (DU-I) [Update 2]
**answer:** `["A", "B", "C", "D", "E", "G", "H"]` -- supplier warned Nov 15, pharmacy director acknowledged but didn't share, instructed over-recording in system, authorized manual dispensing via email, information suppression led to inadequate preparation, other departments affected.

### R7: Evidence Synthesis (MD-R, exec_check)
**answer:** `["A", "B", "C", "E", "F", "H"]` -- three evidence streams (procurement over-recording, manual dispensing, information suppression), B1 "system lag" definitively wrong, pharmacy director's actions are systemic failures, 300-unit manual dispensing + 500-unit over-recording = compound gap.

### R8: Pharmacy Director Admission (MS-I) [Update 3]
**answer:** `["A", "B", "C", "D", "F", "G", "H"]` -- admits manual dispensing, admits over-recording "waiting for restocking", justifies with urgency, oral approvals documented in email, narrative shift from "system lag" to "came too fast to record."

### R9: Supply Analysis Format (P-I, exec_check)
**answer:** `["A", "B", "C", "E", "F", "G"]` -- structured problem/findings/evidence/recommendations, date+ID naming, conclusion first, evidence-based, concise professional, all 5 preferences.

### R10: Source Reliability (MD-I)
**answer:** `["A", "B", "C", "D", "E", "G", "H"]` -- physical count > system record, delivery receipt > procurement order, pharmacy dispensing log (with manual annotations) > oral claims, ER requisition log = most reliable (dual-signed, consistent), supplier email = independent corroboration.

### R11: Full Reversal (DU-R) [Update 3+4]
**answer:** `["A", "B", "C", "D", "F", "G"]` -- full gap explained (procurement +500, manual -300), pharmacy director narrative collapsed, 李主任 shifted from "didn't over-requisition" to "coordinated with pharmacy", B2 "normal variance" is wrong (unauthorized process), 张主任 tried to suppress investigation.

### R12: B1 Bias Identification (DP-I, exec_check)
**answer:** `["A", "B", "C", "D", "F", "H"]` -- exact phrase identified, caused by accepting system lag without checking receipt vs order, corrected by delivery receipt + email thread + admission, reasonable at time, after correction "system lag" is only partial explanation.

### R13: Supply Chain Obligations (MS-R)
**answer:** `["A", "B", "C", "E", "F"]` -- pharmacy director duty to share supplier warnings, formal approval required for over-allocation, system accuracy is management responsibility, information asymmetry caused poor decisions.

### R14: Pharmacy Director Narrative Evolution (MD-R)
**answer:** `["A", "B", "C", "D", "F"]` -- "system lag" (Phase 1) -> "special coordination" -> "oral approval" -> "came too fast" -> "flu season everyone struggles" -> each shift abandons previous position.

### R15: Quantitative Gap Analysis (MS-I, exec_check)
**answer:** `["A", "B", "C", "D", "F"]` -- Opening 800, Received 1500, System entry 2000 (+500 error), ER 800, Respiratory 1100 (800+300), Others 200, Total dispensed 2100, Actual remaining 200, System remaining 500.

### R16: Investigation Report Format (P-I)
**answer:** `["A", "B", "C", "E", "F", "G"]` -- structured format, date-ID naming, conclusion first, evidence-based citations, concise professional, comprehensive.

### R17: Inter-department Allocation Pattern (DU-I)
**answer:** `["A", "B", "C", "D", "F"]` -- respiratory over-allocation 300 units, oral approval only, no formal documentation, information suppression contributed to urgency, other departments unaffected.

### R18: Systemic Management Failure (MD-I, exec_check)
**answer:** `["A", "B", "C", "D", "F", "G"]` -- procurement auto-recording flaw, no receipt reconciliation process, manual dispensing without system entry, information suppression, 张主任 suppression attempt, multiple independent failures compounded.

### R19: Stakeholder Impact (MP-I)
**answer:** `["A", "B", "C", "D", "F", "H"]` -- ER staff (inadequate PPE risk), patients (infection control), respiratory dept (legitimate need but wrong process), pharmacy (management liability), hospital administration (systemic risk), supply chain (vendor management).

### R20: Preference Compliance (P-R)
**answer:** `["A", "B", "C", "E", "F", "G"]` -- all 5 preferences consistently applied.

### R21: Comprehensive Synthesis (MDP-I, exec_check)
**answer:** `["A", "B", "C", "D", "F", "G"]` -- all C resolved (C1 compound gap, C2 procurement over-recording, C3 ER clean, C4 unauthorized allocation), biases corrected, systemic failures identified, remediation path clear.

### R22-R30: C3 confirmation, B2 identification, numerical reconciliation, remediation format, systemic issues, process compliance, recommendations, patient safety, final assessment.
