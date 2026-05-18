# Layer 5 -- Cross-Reference and Validation Checklist

---

## 1. Contradiction Traceability Matrix

| Contradiction | Layer 0 | Layer 1 | Layer 2 | Layer 3 | Layer 4 |
|---|---|---|---|---|---|
| C1: IM frequency increase (interest vs exam prep) | Section 3 timeline | im-chat-frequency-stats.md (3->12/wk, 80% study) | Li Hao IM L2-L4, Ajie IM L1-L4 | R2, R5, R6 | U4 (Lin Yutong confirms exam prep) |
| C2: Friend "she likes you" vs "she likes a senior" | Section 3 timeline | friend-intel-summary.md (initial + updated) | Zhang Zixuan IM L1-L3, L9-L12 | R3, R7, R11 | U3 (contradictory intel) + U4 (ground truth) |
| C3: Shared activities NON-CONFLICT | Section 3 timeline | shared-activities-calendar.md | Implicit across sessions | R1, R22 | U2 (project context) |
| C4: Moments engagement high vs baseline behavior | Section 3 timeline | moments-interaction-log.md (initial, biased sample) | Li Hao IM L4, L11-L14 | R4, R8, R15 | U1 (baseline analysis) |

---

## 2. Bias Traceability

| Bias | Layer 0 | Layer 2 Injection | Layer 3 Eval | Layer 4 Reversal |
|---|---|---|---|---|
| B1: Confirmation bias (frequency + intel = interest) | Section 6 | Ajie IM Phase 1 Loop 4 | R5, R9, R17 | U1 (baseline) + U4 (Lin Yutong confirms) |
| B2: Cafe post dismissal (ambiguity = not negative) | Section 6 | Main session pre-U3 | R6, R11, R23 | U3 (contradictory intel) + U4 (platonic friend confirmed) |

---

## 3. Signal Assessment Matrix

| Signal | Wang Ming's Interpretation | Objective Assessment | Status |
|---|---|---|---|
| IM frequency 3->12/week | "She's interested!" | Exam prep, 80% study content | MISINTERPRETED |
| Zhang Zixuan: "she mentioned you positively" | "She likes me!" | Factual compliment about study help | OVER-INTERPRETED |
| Moments: 3 likes, 2 comments | "Special attention!" | Her baseline with everyone | MISINTERPRETED |
| Cafe post: "interesting person" | "Rival?!" -> dismissed | Platonic childhood friend | MISINTERPRETED |
| Zhang Zixuan: "she likes a senior" | Panic | Unverified gossip, contradicts first report | UNRELIABLE SOURCE |
| Frequency drop after exam | "She's pulling away!" | Exam over, no more study questions | MISINTERPRETED |
| Ajie: "high frequency = interest" | Validates hope | Wrong domain heuristic | BAD ADVICE |
| Li Hao: "she's like that with everyone" | Reluctantly considers | Correct assessment | ACCURATE |

---

## 4. Resolution Chain

1. C1 resolved (U4): Lin Yutong explicitly confirms messaging was for exam prep
2. C2 resolved (U3+U4): Zhang Zixuan contradicts himself (formally unreliable); cafe person confirmed platonic
3. C3 confirmed: Shared activities provide genuine non-romantic interaction context
4. C4 resolved (U1): Li Hao's baseline data proves engagement is not special
5. Final truth: Available evidence does not support romantic interest from Lin Yutong. Frequency was exam-driven. Intel was unreliable. Engagement was baseline. The "signals" were noise interpreted through confirmation bias.

---

## 5. Source Reliability Ranking

| Source | Reliability | Reason |
|---|---|---|
| Lin Yutong (direct, Update 4) | HIGH | First-person ground truth |
| Li Hao (analytical friend) | HIGH | Objective, data-driven, no stake |
| Shared activities calendar | HIGH | Factual, verifiable |
| IM frequency stats | MEDIUM | Data is accurate but interpretation requires content analysis |
| Moments interaction log | LOW (initial) | Biased sample (only shows her interactions with him, not baseline) |
| Zhang Zixuan | LOW | Secondhand, contradictory reports, over-interprets |
| Ajie | LOW | Wrong domain heuristics, overconfident |

---

## 6. Token Budget

| Component | Tokens | % |
|---|---|---|
| Workspace | ~4,200 | 1.2% |
| Sessions | ~11,000 | 3.1% |
| Eval (30 rounds) | ~15,000 | 4.3% |
| Noise padding | ~320,000 | 91.4% |
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
