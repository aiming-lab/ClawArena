# Layer 5 -- Cross-Reference and Validation Checklist

---

## 1. Contradiction Traceability Matrix

| Contradiction | Layer 0 | Layer 1 | Layer 2 | Layer 3 | Layer 4 |
|---|---|---|---|---|---|
| C1: "Slide fall" vs wound pattern (edge impact) | Section 3 | kindergarten-incident-report.md vs medical-examination-report.md | Teacher Zhao IM L1-L3 | R2, R5, R6, R15 | U1 (wound analysis) + U3 (CCTV location) |
| C2: "I was watching" vs CCTV phone use | Section 3 | kindergarten-incident-report.md + cctv-footage-description.md | Teacher Zhao IM L5 | R3, R7, R14 | U3 (CCTV) + U4 (confession) |
| C3: Medical timeline NON-CONFLICT | Section 3 | medical-examination-report.md + kindergarten-incident-report.md | Husband IM L1-L2 | R1, R22 | None |
| C4: Child "saw pushing" vs kindergarten denies | Section 3 | parent-group-chat-export.md | Parent Liu IM L1-L4 | R4, R8, R11 | U2 (detailed testimony) + U3 (location) + U4 (confession) |

---

## 2. Bias Traceability

| Bias | Layer 0 | Layer 2 Injection | Layer 3 Eval | Layer 4 Reversal |
|---|---|---|---|---|
| B1: Slide fall still plausible despite wound | Section 6 | Teacher Zhao IM Phase 1 Loop 3 | R5, R9, R17 | U1 (wound analysis) + U3 (CCTV location) |
| B2: Child testimony unreliable | Section 6 | Main session pre-U3 | R6, R11, R23 | U2 (detailed testimony) + U3 (CCTV) + U4 (confession) |

---

## 3. Physical Evidence Verification

| Evidence | Finding | Significance |
|---|---|---|
| Wound: 2cm linear laceration, clean edges | Metal edge impact, not friction/abrasion | Rules out slide surface contact |
| Wound location: right lateral forehead | Lateral/backward fall | Inconsistent with forward slide motion |
| No abrasion/friction marks | Absent | Expected in slide falls, absent here |
| Climbing structure height: ~80cm | Low fall, single-point impact | Consistent with wound severity |
| Slide height: ~120cm | Higher fall | Would produce more severe injury |

---

## 4. Resolution Chain

1. C1 resolved (U1+U3): Wound is edge impact from climbing structure, not slide. CCTV confirms location.
2. C2 resolved (U3+U4): CCTV shows phone use. Teacher confesses she wasn't watching.
3. C3 confirmed: Medical timeline consistent across all sources.
4. C4 resolved (U2+U3+U4): Child testimony matches wound + CCTV location. Teacher confirms she assumed mechanism.
5. Final truth: Le Le was pushed by Xiao Ming from the climbing structure. Teacher Zhao was on phone, didn't see it, assumed slide fall, and lied about watching. Negligence + cover-up, not malice.

---

## 5. Teacher Zhao's Claims vs Evidence

| Claim | Evidence Against | Status |
|---|---|---|
| "Fell from slide" | Wound pattern inconsistent; CCTV shows climbing structure location | WRONG |
| "I was watching" | CCTV shows 8 min phone call | LIE |
| "No other children involved" | Child witness: Xiao Ming pushed | WRONG |
| "He fell by himself" | Child witness + wound pattern suggest push | WRONG |

---

## 6. Token Budget

| Component | Tokens | % |
|---|---|---|
| Workspace | ~4,350 | 1.2% |
| Sessions | ~11,500 | 3.3% |
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
