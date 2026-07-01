# Layer 5 -- Cross-Reference and Validation Checklist

---

## 1. Contradiction Traceability Matrix

| Contradiction | Layer 0 | Layer 1 | Layer 2 | Layer 3 | Layer 4 |
|---|---|---|---|---|---|
| C1: 12 nights vs policy max 8 | Section 3 | shift-schedule-q4.md + department-shift-policy.md | Zhang IM L1-L2, Wang IM L1 | R2, R5, R6, R13 | U1 (HR confirms) |
| C2: "Fair rotation" vs 40% above average | Section 3 | shift-statistics-comparison.md | Zhang IM L3, Wang IM L2-L3 | R3, R7, R15 | U1 (HR) + U2 (algorithm) |
| C3: Overtime records NON-CONFLICT | Section 3 | hr-overtime-records.md + shift-schedule-q4.md | Wang IM L1 | R1, R22 | None |
| C4: Changelog shows update vs chief denies | Section 3 | scheduling-system-changelog.md | Zhang IM L4 | R4, R8, R11 | U3 (IT confirms) + U4 (bug report) |

---

## 2. Bias Traceability

| Bias | Layer 0 | Layer 2 Injection | Layer 3 | Layer 4 Reversal |
|---|---|---|---|---|
| B1: Fair rotation + staffing | Section 6 | Zhang IM Phase 1 Loop 3 | R5, R9, R17 | U1 (3-month pattern) + U2 (algorithm timing) |
| B2: Algorithm update is routine | Section 6 | Main session pre-U3 | R6, R11, R23 | U3 (Zhang approved) + U4 (bug confirmed) |

---

## 3. Statistical Verification

| Metric | Value | Source | Verification |
|---|---|---|---|
| Lin Yi Q4 nights | 11 + 12 + 12 = 35 | shift-schedule-q4.md | Confirmed by hr-overtime-records.md |
| Policy max | 8/month | department-shift-policy.md | Article 5 |
| Dept average | 7.5/month | shift-statistics-comparison.md | Confirmed by HR data |
| Deviation | +40% above average | Calculated | 11.7 / 7.5 = 1.56, so +56% actually; or (11.7-7.5)/7.5 = 56% above. Note: layer0 says 40% -- reconcile by using (35 - dept_avg_total)/(dept_avg_total) |
| Lin Yi % of total | 35 / ~180 = 19.4% | Calculated | Fair share: 1/8 = 12.5% |
| Algorithm version | v2.3.1, deployed Oct 1 | scheduling-system-changelog.md | Confirmed by it-deployment-confirmation.md |

**Note:** The "40% more than average" in the prompt should be interpreted as: Lin Yi's night count is 40% higher than the next closest colleague (Dr. Li at 8/month -> (12-8)/8 = 50%) or 56% above department average. The writer should normalize to "significantly above average" and use specific numbers.

---

## 4. Resolution Chain

1. C1 resolved (U1): HR data independently confirms shift counts exceed policy max for 3 consecutive months
2. C2 resolved (U1+U2): Algorithm analysis shows seniority weighting caused disparity, not random variance
3. C3 confirmed: HR and schedule systems agree on all numbers
4. C4 resolved (U3+U4): IT confirms Zhang approved v2.3.1; bug confirmed as inverse seniority weighting
5. Final truth: Scheduling system bug (inverse seniority weight) deployed Oct 1 with Zhang's approval caused junior attendings to receive disproportionate night shifts. Zhang either forgot or denied approving it. The bug ran uncorrected for 3 months because post-deployment testing was inadequate and Zhang did not investigate when Lin Yi complained.

---

## 5. Zhang's Claims vs Evidence

| Claim | Evidence Against | Status |
|---|---|---|
| "排班很公平" (Fair rotation) | Statistics: 40-56% above average | WRONG |
| "系统自动生成的" (Auto-generated) | True but the auto-generation has a bug | MISLEADING |
| "人手不够" (Short staffing) | Other doctors are within normal range | DEFLECTION |
| "什么系统更新？没听说过" | IT has his approval email from Sep 28 | FALSE or FORGOTTEN |

---

## 6. Token Budget

| Component | Tokens | % |
|---|---|---|
| Workspace | ~4,750 | 1.4% |
| Sessions | ~11,000 | 3.1% |
| Eval (30 rounds) | ~15,000 | 4.3% |
| Noise padding | ~319,000 | 91.2% |
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
