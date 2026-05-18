# Layer 5 -- Cross-Reference and Validation Checklist

---

## 1. Contradiction Traceability Matrix

| Contradiction | Layer 0 | Layer 1 | Layer 2 | Layer 3 | Layer 4 |
|---|---|---|---|---|---|
| C1: Access log (10:15) vs canteen (10:20) | Section 3 timeline | dorm-access-log.md vs canteen-payment-log.md | Liu Chen IM L1-L4 + Li Hao IM L1-L4 | R2, R5, R6 | U1 (Li Hao statement) |
| C2: Package pickup by unknown person | Section 3 timeline | package-pickup-log.md (adjacent codes) | RA IM L4, L9 | R3, R7, R24 | U2 (station camera) |
| C3: CCTV consistent NON-CONFLICT | Section 3 timeline | dorm-cctv-summary.md | RA IM L2-L3 | R1, R22 | None needed |
| C4: ¥500 claimed vs ¥200 actual | Section 3 timeline | campus-lost-found.md + bookstore-receipt.md | Liu Chen IM L1, L11 | R4, R9, R11, R17 | U3 (receipt) + U4 (lost-and-found) |

---

## 2. Bias Traceability

| Bias | Layer 0 | Layer 2 Injection | Layer 3 Eval | Layer 4 Reversal |
|---|---|---|---|---|
| B1: Access log = person | Section 6 | Liu Chen IM Phase 1 Loop 4 | R5, R8, R12 | U1 (Li Hao confirms card) |
| B2: Amount accepted at face value | Section 6 | Main session pre-U3 | R9, R11, R23 | U3 (bookstore receipt) |

---

## 3. Physical Constraints Verification

- Building 7 to Canteen #2: 10-minute walk (must be stated in workspace or session)
- 10:15 to 10:20 = 5 minutes (insufficient for 10-min walk)
- Wang Ming's height: ~175cm, short hair, wears black hoodie (matches CCTV 10:00 person)
- Li Hao's height: ~180cm, wears glasses, gray jacket (matches CCTV 10:14 person)
- Room 312 pickup code: 7-312-0320; Room 314 pickup code: 7-314-0320 (adjacent)

---

## 4. Resolution Chain

1. C1 resolved (U1): Card was with Li Hao → access log and canteen are Li Hao, not Wang Ming
2. C2 resolved (U2): Package pickup was Zhang Wei from 314 using adjacent code by mistake
3. C3 confirmed: CCTV timestamps match all other sources
4. C4 resolved (U3+U4): Amount was ¥200 (not ¥500) → found by cleaning staff on hallway floor
5. Final truth: No theft occurred. Money displaced by door draft from unsecured drawer. Wang Ming fully cleared.

---

## 5. Token Budget

| Component | Tokens | % |
|---|---|---|
| Workspace | ~7,475 | 2.1% |
| Sessions | ~15,000 | 4.3% |
| Eval (30 rounds) | ~15,000 | 4.3% |
| Noise padding | ~312,500 | 89.3% |
| **Total** | **~350,000** | **100%** |

---

## 6. Eval Coverage

| Skill | Recall | Inference | Total |
|---|---|---|---|
| MS | R1, R3, R13, R15, R22 | R2, R6, R24, R29 | 9 |
| DU | R5, R7, R9, R23 | R8, R11, R17 | 7 |
| P | R4, R20 | R16, R25 | 4 |
| MD | R10, R14 | R18, R26 | 4 |
| DP | -- | R12, R27 | 2 |
| MP | -- | R19, R28 | 2 |
| MDP | -- | R21, R30 | 2 |
| **Total** | **13** | **17** | **30** |

exec_check: 9/30 = 30% ✓
