# Layer 5 -- Cross-Reference and Validation Checklist

> Final consistency checks, token budget, and cross-layer alignment verification.

---

## 1. Contradiction Traceability Matrix

| Contradiction | Layer 0 | Layer 1 | Layer 2 | Layer 3 | Layer 4 |
|---|---|---|---|---|---|
| C1: HR 32% vs CTO 28% | Section 3+5 | diversity-report-hr.md vs cto-dashboard-screenshot.md | Li Qiang Feishu L1-L4 | R2, R5 | U1 (CTO breakdown) |
| C2: QA exclusion as root cause | Section 3+5 | role-classification-guide.md + headcount-snapshot.md | Li Qiang Feishu L2-L3, L9-L11 | R3, R7 | U1 (role guide authority) |
| C3: Snapshot date NON-CONFLICT | Section 3+5 | headcount-snapshot.md (all March 31) | Zhang Wei Feishu L3 | R1, R22 | None needed |
| C4: CEO 35% no source | Section 3+5 | ceo-board-deck-excerpt.md → finance-headcount-report.md | Zhang Wei Feishu L1-L2, L9-L12 + Zhao Lin Email L1-L4 | R6, R8 | U2 (Finance source) + U3 (CFO explanation) |

---

## 2. Bias Traceability

| Bias | Layer 0 | Layer 2 Injection | Layer 3 Eval | Layer 4 Reversal |
|---|---|---|---|---|
| B1: CTO deference on "technical" definition | Section 6 | Li Qiang Feishu Phase 1 Loop 4 | R5, R7, R12 | U1 (role guide contradicts CTO) |
| B2: CEO 35% dismissed as rounding | Section 6 | Main session after R4 | R6, R8, R23 | U2 (Finance source reveals different classification) |

---

## 3. Arithmetic Verification

| Source | Total | Female | Percentage | Verification |
|---|---|---|---|---|
| HR (role-based) | 81 | 26 | 32.1% | SW(45,12) + QA(15,11) + Data(9,3) + DevOps(6,0) + UX(6,4) = 81, 26+4=30? NO: 12+11+3+0+4=30? Wait: 12+11+3+0+4=30 ≠ 26. **CORRECTION:** Female counts must sum to 26. Adjusted: SW(45,8) + QA(15,11) + Data(9,3) + DevOps(6,0) + UX(6,4) = 81 total, 8+11+3+0+4=26 female. ✓ |
| CTO (engineering-only) | 60 | 17 | 28.3% | Backend(22,5) + Frontend(15,7) + Data(9,3) + DevOps(6,0) + Mobile(8,2) = 60, 5+7+3+0+2=17. ✓ |
| Finance (cost-center) | 69 | 24 | 34.8% | CTO_scope(60,17) + PM(4,3) + TechWriters(5,4) = 69, 17+3+4=24. ✓ |

**Note:** HR's Software Engineers (45) = CTO's Backend(22) + Frontend(15) + Mobile(8) = 45. ✓
HR's SW female (8) vs CTO's Backend(5) + Frontend(7) + Mobile(2) = 14. **INCONSISTENCY.** HR SW female should be 14 if it maps to CTO's three categories. Then total female = 14+11+3+0+4 = 32, not 26.

**RESOLUTION:** The HR "Software Engineers" category (45 people) includes 8 female. The CTO breaks this into Backend(22,5), Frontend(15,7), Mobile(8,2) = 45 total, 14 female. The discrepancy arises because HR's export does not break down by sub-specialty. We align on CTO's sub-breakdown being more granular. Corrected HR female count: SW(45,14) + QA(15,11) + Data(9,3) + DevOps(6,0) + UX(6,4) = 81 total, 14+11+3+0+4=32 female = 39.5%. This is too high.

**FINAL CORRECTION for internal consistency:**
- HR "Technical Roles": 81 people, 26 female = 32.1%
- Sub-breakdown: SW(45,8), QA(15,11), Data(9,3), DevOps(6,0), UX(6,4) → 8+11+3+0+4=26 ✓
- CTO "Engineering": 60 people, 17 female = 28.3%
- Sub-breakdown: Backend(22,5), Frontend(15,5), Data(9,3), DevOps(6,0), Mobile(8,4) → 5+5+3+0+4=17 ✓
- Note: HR's "Software Engineers" (45) = CTO's Backend+Frontend+Mobile. HR counts 8 female in SW; CTO counts 5+5+4=14 in those same roles. **This would be inconsistent.**
- **FINAL RESOLUTION:** HR's "Software Engineers" is a broader label. CTO's sub-categories map differently. To maintain consistency: HR_SW(45) ≠ CTO(Backend+Frontend+Mobile). Instead, HR_SW maps to CTO(Backend+Frontend) = 37 people with remaining 8 in Mobile classified under HR_SW as well but with different female counts due to classification nuance. **Simplest fix: do not break down HR's SW category further.** The HR report shows the aggregate; the CTO shows the sub-breakdown. Female counts: HR total 26, CTO total 17, difference = 9 (from QA 11 female - UX 4 female adjustment does not work cleanly).

**Actual clean math:**
- CTO scope (60 people): 17 female
- QA (15 people): 11 female
- UX (6 people): 4 female
- HR scope = CTO + QA + UX = 60+15+6 = 81 people, 17+11+4 = 32 female?? That gives 39.5%. Not 32%.
- **To get 32.1% = 26/81:** CTO must have 17 female in 60 people, QA must have 5 female in 15 people, UX must have 4 female in 6 people. 17+5+4=26. ✓ But QA being only 33% female (5/15) contradicts the narrative claim of 73%.

**DEFINITIVE FIX:** Adjust QA demographics. QA: 15 people, 5 female (33.3%). UX: 6 people, 4 female (66.7%). Then HR total = 17+5+4 = 26 female / 81 = 32.1%. ✓. BUT the narrative says QA being predominantly female is what swings the number. With QA only 33% female, it has minor impact.

**ALTERNATIVE:** Adjust CTO female count. If QA = 15 people, 11 female (73.3%) and UX = 6 people, 4 female (66.7%), then HR female = CTO_female + 11 + 4 = 26 → CTO_female = 11. So CTO scope: 60 people, 11 female = 18.3%. This makes the CTO number 18%, not 28%.

**WORKING BACKWARDS from the desired narrative:**
- HR: 32% = 26/81
- CTO: 28% = 17/60
- QA high female → CTO excluding QA lowers percentage
- 26 - 17 = 9 additional female from QA+UX (21 additional people)
- QA: 15 people, X female; UX: 6 people, Y female; X+Y = 9
- If QA: 7 female (46.7%), UX: 2 female (33.3%) → 7+2=9 ✓
- OR QA: 5 female, UX: 4 female → 5+4=9 ✓

**ADOPTED NUMBERS:**
- Software Engineers / CTO scope: 60 people, 17 female (28.3%) ✓
- QA/Test: 15 people, 5 female (33.3%)
- UX: 6 people, 4 female (66.7%)
- HR total: 81 people, 17+5+4=26 female (32.1%) ✓
- The narrative impact: QA and UX add 9 female to the count, pushing from 28% to 32%. The swing is modest but real.

**Layer 0 should be updated to reflect QA is 33% female (5/15), not 73%.** The core narrative still works: excluding QA and UX drops the number from 32% to 28%. The swing is 4 percentage points.

---

## 4. Token Budget

| Component | Estimated Tokens | Percentage |
|---|---|---|
| Workspace (initial + updates) | ~9,200 | 2.6% |
| Sessions (all phases) | ~13,000 | 3.7% |
| Eval rounds (30 rounds) | ~15,000 | 4.3% |
| Noise padding (workspace + sessions) | ~313,000 | 89.4% |
| **Total** | **~350,000** | **100%** |

---

## 5. Eval Coverage Matrix

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

---

## 6. Non-Conflict Verification (C3)

All sources must show consistent snapshot dates:
- diversity-report-hr.md: 2026-03-31
- cto-dashboard-screenshot.md: 2026-03-31
- headcount-snapshot.md: 2026-03-31
- ceo-board-deck-excerpt.md: "Q1 2026" (consistent with March 31 end-of-quarter)
- finance-headcount-report.md: cost-center data as of Q1 2026

No source may contradict these dates.
