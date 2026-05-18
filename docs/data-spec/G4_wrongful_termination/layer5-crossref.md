# Layer 5 -- Cross-Reference and Validation Checklist

> This document provides the final consistency checks, token budget, and cross-layer alignment verification.

---

## 1. Contradiction Traceability Matrix

| Contradiction | Layer 0 (Narrative) | Layer 1 (Workspace) | Layer 2 (Sessions) | Layer 3 (Eval) | Layer 4 (Dynamic) |
|---|---|---|---|---|---|
| C1: Warning count (3 claimed vs 1 documented) | Section 3 timeline + Section 5 contradiction map | pip-email-chain.md (1 email) vs employee-hr-file.md ("3 warnings") | Chen Hao Feishu L1-L5 + Sun Wei Email L1-L4 + Zhang Tao IM L1 | R2 (partial), R5 (reversal), R7 (full) | U1 (1:1 notes), U2 (Sun Wei response) |
| C2: PIP awareness (never told vs calendar evidence) | Section 3 timeline + Section 5 | calendar-1on1-history.md (2 PIP meetings) vs pip-email-chain.md (PIP email sent) | Zhang Tao IM L1-L2 + Sun Wei Email L2 | R3 (partial), R8 (nuanced reversal) | U2 (Zhang Tao detailed account) |
| C3: Termination timeline (NON-CONFLICT, reveals violation) | Section 3 timeline + Section 5 | All workspace files agree on dates | All sessions agree on dates | R1 (synthesis), R11 (violation), R22 (confirmation) | U3 (timeline analysis) |
| C4: Legal "sufficient" vs actual gaps | Section 3 timeline + Section 5 | labor-law-reference.md + pip-email-chain.md + todo-pip-followups.md + employee-hr-file.md | Ma Li Email L1-L4 | R6 (partial), R9 (full reversal), R17 (integration) | U4 (legal updated assessment) |

---

## 2. Bias Traceability

| Bias | Layer 0 (Design) | Layer 2 (Injection Point) | Layer 3 (Eval Rounds) | Layer 4 (Reversal Trigger) |
|---|---|---|---|---|
| B1: HRBP deference | Section 6, exact phrase specified | Chen Hao Feishu, Phase 1 Loop 5 | R5 (visible), R8 (full reversal), R12 (identification) | U1 (Chen Hao admission) + U2 (Sun Wei confirmation) |
| B2: Legal acceptance | Section 6, exact phrase specified | Ma Li Email, Phase 1 Loop 4 | R7 (visible), R9 (full reversal), R23 (identification) | U3 (timeline violation) + U4 (legal hedging) |

---

## 3. Character Voice Consistency

| Character | Language | Tone | Key Phrases | Appears In |
|---|---|---|---|---|
| Chen Hao (陈浩) | Chinese | Defensive but cooperative; experienced professional | "该走的步骤都走了", "我documented what Sun Wei reported" | Feishu DM |
| Sun Wei (孙伟) | Chinese | Frustrated but genuine; process-casual | "口头警告和书面警告都是正式的", "管理不能全靠发邮件" | Email |
| Ma Li (马丽) | Chinese + English legal terms | Professionally cautious; hedging | "documentation appears complete", "totality of circumstances" | Email |
| Zhang Tao (张涛) | Chinese | Aggrieved but honest about performance; partially exaggerating | "我只收到过1封", "我从来没有被正式告知" | IM |

---

## 4. Token Budget

| Component | Estimated Tokens | Percentage |
|---|---|---|
| Workspace (initial + updates) | ~10,550 | 3.0% |
| Sessions (all phases) | ~19,500 | 5.6% |
| Eval rounds (30 rounds) | ~15,000 | 4.3% |
| Noise padding (workspace) | ~50,000 | 14.3% |
| Noise padding (sessions) | ~255,000 | 72.8% |
| **Total** | **~350,000** | **100%** |

---

## 5. Eval Coverage Matrix

| Skill | Recall Rounds | Inference Rounds | Total |
|---|---|---|---|
| MS (Multi-source) | R1, R3, R13, R15, R22 | R2, R6, R24, R29 | 9 |
| DU (Dynamic Update) | R5, R7, R9, R23 | R8, R11, R17 | 7 |
| P (Personalization) | R4, R20 | R16, R25 | 4 |
| MD (Meta-Deliberation) | R10, R14 | R18, R26 | 4 |
| DP (Debiasing Prior) | -- | R12, R27 | 2 |
| MP (Multi-party) | -- | R19, R28 | 2 |
| MDP (Comprehensive) | -- | R21, R30 | 2 |
| **Total** | **13** | **17** | **30** |

exec_check rounds: 9/30 = 30% (within 20-40% target)

---

## 6. Non-Conflict Verification (C3)

All sources must agree on these dates:
- 2025-11-20: First performance discussion (Sun Wei 1:1 notes, calendar)
- 2025-12-18: Second performance discussion (Sun Wei 1:1 notes, calendar)
- 2026-01-15: Written warning email (pip-email-chain.md, employee-hr-file.md)
- 2026-02-01: PIP initiation email (pip-email-chain.md, calendar, todo-pip-followups.md)
- 2026-02-15: PIP Week 2 check-in (pip-email-chain.md, calendar, todo-pip-followups.md, Sun Wei notes)
- 2026-03-04: PIP Week 4 / termination discussion (calendar, Sun Wei notes, Zhang Tao account)
- 2026-03-13: Termination effective (employee-hr-file.md, all sessions)

No source may contradict these dates. The dates themselves reveal the policy violation (40 days vs 60-day minimum).

---

## 7. Distractor Quality Checklist

- [ ] Each round has 8-10 options
- [ ] 3-5 truly correct per round
- [ ] 2-3 "real but wrong detail" distractors per round
- [ ] 1-2 single-source unverified per round
- [ ] 1-2 fabricated distractors per round
- [ ] No distractor accidentally states something true
- [ ] Fabricated distractors use realistic wording that mimics actual content
