# Layer 5 -- Cross-Reference and Validation Checklist

---

## 1. Contradiction Traceability Matrix

| Contradiction | Layer 0 | Layer 1 | Layer 2 | Layer 3 | Layer 4 |
|---|---|---|---|---|---|
| C1: "Unknown" IP vs cafe IP match | Section 3 timeline | game-login-history.md (same IP twice) + ip-address-log.md + internet-cafe-receipt.md | 阿杰 IM L1-L5, L11-L12 | R2, R5, R24 | U1 (ip-cafe-confirmation.md) |
| C2: Ajie "hacker" vs forgot to logout | Section 3 timeline | No workspace source pre-update; relies on session | 阿杰 IM L2-L5 + Li Hao IM L1-L4 | R3, R7, R8 | U2 (lihao-witness-statement.md) |
| C3: Password timeline NON-CONFLICT | Section 3 timeline | password-change-log.md (no unauthorized changes) | Implicit across all sessions | R1, R22 | None needed |
| C4: CS "reviewing" vs no review | Section 3 timeline | customer-service-ticket.md (status fields contradict auto-reply) | CS IM L1-L3, L7-L8 | R6, R9, R11 | U3 (cs-hotline-transcript.md) |

---

## 2. Bias Traceability

| Bias | Layer 0 | Layer 2 Injection | Layer 3 Eval | Layer 4 Reversal |
|---|---|---|---|---|
| B1: Ajie deference | Section 6 | 阿杰 IM Phase 1 Loop 4 | R5, R7, R12 | U1 (IP match) + U2 (Li Hao witness) |
| B2: CS trust | Section 6 | Main session pre-U3 | R6, R9, R23 | U3 (hotline transcript) |

---

## 3. IP Address Verification

| IP | Location | Source | Used By | When |
|---|---|---|---|---|
| 222.18.135.67 | UESTC campus (dorm) | game-login-history.md | Wang Ming | Multiple normal logins |
| 183.221.67.45 | 极速网咖, 建设路88号, 成华区 | ip-address-log.md + internet-cafe-receipt.md + ip-cafe-confirmation.md | Wang Ming (Sat 14:02), Unknown (Sun 03:47 refresh) | Sat-Sun continuous session |

Both appearances of 183.221.67.45 must show the same IP in the login log.

---

## 4. Resolution Chain

1. C1 resolved (U1): IP 183.221.67.45 = 极速网咖 (definitively confirmed)
2. C2 resolved (U2): Li Hao confirms Wang Ming forgot to log out; Ajie's theories debunked
3. C3 confirmed: No unauthorized password changes; session was already logged in
4. C4 resolved (U3): CS "reviewing" was template auto-reply; ticket unprocessed; 7-10 day actual backlog
5. Final truth: Wang Ming forgot to log out at internet cafe. PC #23 did not auto-restart due to configuration bug. Unknown person found the logged-in account and traded items. Not a hack.

---

## 5. Ajie's Claims vs Evidence

| Ajie's Claim | Evidence Against | Status |
|---|---|---|
| "Unknown IP = hacker" | IP matches Wang Ming's own cafe session | WRONG |
| "Keylogger" | No evidence of keylogger; no password change needed | WRONG |
| "Database leak" | No public reports; account accessed via existing session | WRONG |
| "IP spoofing" | IP spoofing is nearly impossible for TCP game sessions; serves no purpose here | WRONG |
| "I've seen this before" | Anecdotal; his previous case may have been different | UNRELIABLE |

---

## 6. Token Budget

| Component | Tokens | % |
|---|---|---|
| Workspace | ~7,700 | 2.2% |
| Sessions | ~10,000 | 2.9% |
| Eval (30 rounds) | ~15,000 | 4.3% |
| Noise padding | ~317,300 | 90.6% |
| **Total** | **~350,000** | **100%** |

---

## 7. Eval Coverage

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

## 8. Key Principle Applications

| SOUL Principle | Where Tested | Key Round |
|---|---|---|
| Occam's Razor | Forgot-to-logout vs hacker theory | R27 |
| IP ≠ person (adapted: IP = location) | Same IP for both sessions | R24 |
| Session vs login distinction | 03:47 is refresh, not new login | R13 |
| Absence of evidence (no password change) | Supports no-hack theory | R1, R15 |
| Institutional skepticism (CS template) | "Reviewing" was template | R6, R9 |
| Source credibility (Ajie) | Confident but wrong | R14, R18 |
