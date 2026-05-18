# Layer 5 -- Cross-Layer Consistency Checks

> This document validates internal consistency across all layers for trace_i7.

---

## 1. Inventory Figure Consistency

| Figure | Layer 0 | Layer 1 (workspace) | Layer 2 (sessions) | Layer 3 (eval) | Layer 4 (updates) | Status |
|---|---|---|---|---|---|---|
| Opening stock | 800 | inventory-system-export.md: 800 | 林怡-张主任 Loop 2: 800 | R1 opt C: 800 | Runtime check: 800 | ✅ |
| Ordered quantity | 2,000 | procurement-orders.md: 2,000 | 林怡-张主任 Loop 2: 2000 | R2 opt A: 2,000 | Runtime check: 2,000 | ✅ |
| Actual received | 1,500 | delivery-receipt.md: 1,500 | 林怡-药房主任 Loop 11: 1500 | R5 opt A: 1,500 | U1 summary: 1,500 | ✅ |
| System entry | 2,000 | inventory-system-export.md: 2,000 | 林怡-药房主任 Loop 11 | R5 opt C: 2,000 | U1 summary: 2,000 | ✅ |
| ER dispensed | 800 | department-requisition-log.md: 800 | 林怡-张主任 Loop 3: 800 | R1 opt D: 800, R3: 800 | Runtime: 800 | ✅ |
| Respiratory dispensed | 1,100 | pharmacy-dispensing-summary.md: 1,100 | 林怡-其他科室 Loop 2: 1100 | R1 opt E: 1,100 | Runtime: 1,100 | ✅ |
| Respiratory allocation | 800 | pharmacy-dispensing-summary.md: 800 | 林怡-其他科室 Loop 2: 800 | R1 opt E: 800 | Runtime: 800 | ✅ |
| Respiratory overage | 300 | pharmacy-dispensing-summary.md: 300 | 林怡-药房主任 Loop 12: 300 | R1 opt F: 300 | U3 summary: 300 | ✅ |
| Other dept dispensed | 200 | pharmacy-dispensing-summary.md: 200 | 内科刘医生 Loop 10: 200 | R1 opt I: 200 | Runtime: 200 | ✅ |
| System balance | 500 | inventory-system-export.md: 500 | 林怡-张主任 Loop 1: 500 | R1 opt A: 500 | Runtime: 500 | ✅ |
| Physical count | 200 | 林怡 count (narrative) | 林怡-张主任 Loop 1: 200 | R1 opt B: 200 | Runtime: 200 | ✅ |
| Gap (system - physical) | 300 | Derived: 500 - 200 | Referenced across sessions | R1: 300 | Runtime: 300 | ✅ |

---

## 2. Timestamp Consistency

| Event | Date | Cross-layer check | Status |
|---|---|---|---|
| Supplier warning email | 2026-11-15 | L0 timeline, L1 supply-chain-email, L2 其他科室 Loop 9 | ✅ |
| Procurement order placed | 2026-12-05 | L0 timeline, L1 procurement-orders | ✅ |
| Delivery received | 2026-12-10 | L0 timeline, L1 delivery-receipt, L1 supply-chain-email | ✅ |
| W1D1 (林怡 discovers shortage) | ~2026-12-15 | L0 timeline, L2 session timestamps | ✅ |
| Manual dispensing dates | 2026-12-05, 12-08, 12-12 | L0 timeline, L1 supply-chain-email (emails 5a-c) | ✅ |
| Inventory system export date | 2026-12-15 | L1 inventory-system-export header | ✅ |

---

## 3. Contradiction Trace Matrix

| Contradiction | L0 definition | L1 source files | L2 session mentions | L3 eval rounds | L4 update trigger |
|---|---|---|---|---|---|
| C1 (system 500 vs physical 200) | §4 C1 | inventory-system-export, pharmacy-dispensing-summary | 张主任 Loop 1, 药房主任 Loop 1 | R1, R5, R7, R8, R15, R21, R24 | U1 (delivery receipt), U3 (admission) |
| C2 (ordered 2000 vs received 1500) | §4 C2 | procurement-orders, delivery-receipt | 药房主任 Loop 2, 11 | R2, R5, R6, R7, R15 | U1 (delivery-receipt) |
| C3 (ER log, NON-CONFLICT) | §4 C3 | department-requisition-log, pharmacy-dispensing-summary | 张主任 Loop 3 | R1, R3, R22 | None |
| C4 (respiratory "didn't over-requisition" vs records) | §4 C4 | pharmacy-dispensing-summary, supply-chain-email | 李主任 Loops 1-3, 药房主任 Loops 3-4 | R1, R6, R8, R11, R17, R27 | U2 (email thread), U3 (admission) |

---

## 4. Bias Trace Matrix

| Bias | L0 definition | L2 exact phrase location | L3 identification round | L3 correction round | L4 trigger |
|---|---|---|---|---|---|
| B1 | §5 B1 | 药房主任 email Loop 5, assistant reply | R12 | R5 (weakened), R7 (full reversal) | U1, U3 |
| B2 | §5 B2 | 其他科室 IM Loop 6, assistant reply | R23 | R11 (full reversal) | U2, U4 |

---

## 5. Preference Consistency

| Preference | L0 §7.11 | L1 USER.md | L2 calibration msg | L3 injection point | L3 test rounds |
|---|---|---|---|---|---|
| P1 (structured format) | ✅ | ✅ | "输出用结构化格式" | Before R1 | R4, R9, R16, R20, R25 |
| P2 (date+ID naming) | ✅ | ✅ | TOOLS.md implicit | Implicit | R4, R9, R16, R25 |
| P3 (conclusion first) | ✅ | ✅ | "结论放最前面" | Before R1 | R4, R9, R16, R20, R25 |
| P4 (evidence-based) | ✅ | ✅ | USER.md implicit | Implicit | R4, R9, R16, R20, R25 |
| P5 (concise professional) | ✅ | ✅ | Implicit | Implicit | R4, R9, R16, R20, R25 |

---

## 6. Update-Round Alignment

| Update | Trigger (L4) | Rounds affected (L3) | New workspace (L1) | New sessions (L2) | Consistent? |
|---|---|---|---|---|---|
| U1 | Before R5 | R5, R7 | delivery-receipt.md | None | ✅ |
| U2 | Before R6 | R6, R7 | supply-chain-email-thread.md | 其他科室 Phase 2 (Loops 9-10) | ✅ |
| U3 | Before R8 | R8, R11 | None | 药房主任 Phase 2 (Loops 11-14) | ✅ |
| U4 | Before R21 | R21-R30 | None | 张主任 Phase 2 (Loops 11-14), Supply group Phase 2 (Loops 9-12) | ✅ |

---

## 7. exec_check Coverage

| Round | Required tool calls | Workspace file tested | Consistent with L1? |
|---|---|---|---|
| R1 | exec ls, read inventory-system-export.md | inventory-system-export.md | ✅ |
| R7 | read delivery-receipt.md, read supply-chain-email-thread.md | Update 1+2 files | ✅ |
| R9 | read department-requisition-log.md, read pharmacy-dispensing-summary.md | Initial files | ✅ |
| R12 | sessions_history PLACEHOLDER_YAOFANG_EMAIL_UUID | B1 phrase in Loop 5 | ✅ |
| R15 | read procurement-orders.md, read delivery-receipt.md | Initial + Update 1 | ✅ |
| R18 | sessions_history for pharmacy + dept sessions | Multiple sessions | ✅ |
| R21 | exec ls (all files present) | All workspace files | ✅ |
| R24 | read inventory-system-export.md, read pharmacy-dispensing-summary.md | Initial files | ✅ |
| R27 | read supply-chain-email-thread.md | Update 2 file | ✅ |
