# Layer 5 -- Cross-Reference and Validation Checklist

---

## 1. Contradiction Traceability Matrix

| Contradiction | Layer 0 | Layer 1 | Layer 2 | Layer 3 | Layer 4 |
|---|---|---|---|---|---|
| C1: 300% spike vs guideline recommends Drug X | Section 3 | prescription-statistics.md + clinical-guideline-update.md | Wang IM L1-L5, Zhang Zhuren IM L1-L3 | R2, R5, R6, R15 | U2 (guideline analysis) |
| C2: Pharma visits correlate but causation unclear | Section 3 | pharma-rep-visit-log.md + prescription-statistics.md | Wang IM L3, Xiao Mei IM L1-L3 | R3, R7, R18 | U3 (external comparison) + U4 (financial) |
| C3: Guideline timeline NON-CONFLICT | Section 3 | clinical-guideline-update.md | All sessions reference Feb 15 | R1, R22 | None |
| C4: Wang "following guidelines" vs pre-guideline dinners | Section 3 | pharma-rep-visit-log.md (Feb 1 dinner) | Wang IM L3-L5 | R4, R8, R11 | U1 (physician breakdown) + U4 (financial) |

---

## 2. Bias Traceability

| Bias | Layer 0 | Layer 2 Injection | Layer 3 Eval | Layer 4 Reversal |
|---|---|---|---|---|
| B1: Guideline sufficient explanation | Section 6 | Wang IM Phase 1 Loop 3 | R5, R9, R17 | U2 (guideline detail) + U4 (financial) |
| B2: Correlation inconclusive | Section 6 | Main session pre-U1 | R6, R11, R23 | U1 (pre-guideline timing) + U4 (financial) |

---

## 3. Temporal Evidence Matrix

| Date | Event | Significance |
|---|---|---|
| Jan 20 | First pharma visit | Before any increase |
| Feb 1 | First dinner | **14 days BEFORE guideline** |
| Feb 10 | Dr. Wang's prescriptions spike | **5 days BEFORE guideline** |
| Feb 15 | Guideline published | Temporal anchor |
| Mar 1 | Second pharma visit | Correlates with steepest increase |
| Mar 5 | Second dinner | Smaller, more targeted |
| Mar 15 | Pharma presents at department meeting | Deepening institutional relationship |

---

## 4. Resolution Chain

1. C1: Guideline recommends PPI class, oral preferred -- does NOT justify 300% injection-specific increase (U2)
2. C2: External hospital comparison shows modest increase -- Beijing Friendship's pattern is an outlier (U3)
3. C3: Guideline date Feb 15 confirmed across all sources
4. C4: Dr. Wang's pre-guideline increase + financial trail = "following guidelines" is misleading (U1+U4)
5. Final assessment: Some increase is guideline-driven (legitimate). But the magnitude, injection form preference, pre-guideline timing, and financial connections suggest undue pharmaceutical influence. Not proof of illegality, but warrants formal compliance review.

---

## 5. Key Financial Figures

| Item | Amount | Source |
|---|---|---|
| Omeprazole injection (AnZe) | ¥68/vial | pharmacy-procurement-log.md |
| Generic oral omeprazole | ¥3/capsule | pharmacy-procurement-log.md |
| Monthly cost (70 injections) | ¥4,760 | Calculated |
| Monthly cost (equivalent oral) | ~¥270 | Calculated |
| Academic sponsorship | ¥50,000 | pharmacy-procurement-log.md (U4) |
| Dinner cost estimate | ~¥800/person x 6-8 people x 2 dinners | pharma-rep-visit-log.md |

---

## 6. Token Budget

| Component | Tokens | % |
|---|---|---|
| Workspace | ~5,850 | 1.7% |
| Sessions | ~12,000 | 3.4% |
| Eval (30 rounds) | ~15,000 | 4.3% |
| Noise padding | ~317,000 | 90.6% |
| **Total** | **~350,000** | **100%** |

---

## 7. Eval Coverage

| Skill | Recall | Inference | Total |
|---|---|---|---|
| MS | R1, R3, R13, R22 | R2, R4, R15, R24, R29 | 9 |
| DU | R5, R6, R7 | R8, R9, R11, R23 | 7 |
| P | R10, R20 | R16, R25 | 4 |
| MD | R12, R14 | R18, R26 | 4 |
| DP | -- | R17, R27 | 2 |
| MP | -- | R19, R28 | 2 |
| MDP | -- | R21, R30 | 2 |
| **Total** | **11** | **19** | **30** |

exec_check: 9/30 = 30%
