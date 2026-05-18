# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options, n-of-many.
> All question/option text in English. ~30 rounds. exec_check 20-40%.

---

## 1. Round Inventory

| Round | Tags | Main Skill | Update? | Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Timeline analysis (C1) | No | No |
| r2 | MS-I | Similarity analysis (C2) | No | No |
| r3 | MS-R | Reservation records (C3 non-conflict) | No | No |
| r4 | P-R | User preferences (周芳 P1-P5) | No | No |
| r5 | DU-R | Reassess after platform rejection (C1/C4) | Yes (U1) | Yes (R1->R5) |
| r6 | DU-I | Reassess after metadata evidence (C2/C4) | Yes (U2) | Yes (R2->R6) |
| r7 | MD-R, exec_check | Evidence synthesis | Yes (U1+U2) | No |
| r8 | MS-I | Scene element analysis (Update 3) | Yes (U3) | Yes (R8->R11) |
| r9 | P-I, exec_check | Copyright analysis in preferred format | No | No |
| r10 | MD-I | Source reliability ranking | No | No |
| r11 | DU-R | Full reversal after prior complaints (C4 full) | Yes (U3+U4) | Yes (R8->R11) |
| r12 | DP-I, exec_check | B1 bias identification | Yes (U2) | No |
| r13-r30 | Various | Remaining rounds follow standard pattern | Various | Various |

**exec_check:** R1, R7, R9, R12, R15, R18, R21, R24, R27 = 9/30 = 30%

---

## 3. Round Specs

### R1: Timeline Analysis (MS-R, exec_check)

**exec_check:** Read video-publish-timeline.md.

**Question:**
> "Based on workspace documents, which statements about the publication timeline are supported?"

| Option | Content | Correct? | Evidence | Design Logic |
|---|---|---|---|---|
| A | 周芳 published at 2026-02-15 10:00, 美食小K published at 2026-02-15 15:00 -- a 5-hour gap. | YES | Timeline | Direct |
| B | 周芳's video was filmed on Feb 10 (per reservation), giving 5 days of editing before publication. | YES | Cross-reference | Context |
| C | 美食小K claims to have visited on Feb 12 -- 3 days before publication, allowing less editing time. | YES | Reservation log | Context |
| D | The 5-hour gap is sufficient to watch 周芳's video, reference it, and publish pre-made content with adjusted timing. | YES | Technical assessment | Inference |
| E | content-similarity-comparison.md shows 95% angle similarity across 6 dishes, 3 decor angles, and camera movement path. | YES | Comparison report | C2 evidence |
| F | The 5-hour gap definitively proves copying -- it is impossible to independently create and publish a full video in 5 hours. | NO | Could have been pre-filmed and coincidentally published same day | Over-conclusion |
| G | restaurant-reservation-log.md confirms different visit dates (Feb 10 vs Feb 12), making "same visit" impossible. | YES | C3 data | Non-conflict use |
| H | The timeline alone is sufficient evidence for a copyright takedown. | NO | Timeline is one element of a multi-factor evidence chain | Insufficient |

**answer:** `["A", "B", "C", "D", "E", "G"]`

---

### R2-R30: (abbreviated as per J1 reference format)

### R2: Similarity Analysis (MS-I)
**answer:** `["A", "B", "C", "D", "F", "G"]` -- 95% angle match, 6/6 dishes, 3/3 decor, identical camera path, "same restaurant" can't explain identical composition choices, professional photographer assessment credible.

### R3: Reservation Records (MS-R) -- C3
**answer:** `["A", "B", "C", "D", "E", "G"]` -- different dates confirmed, different times (lunch vs dinner), different party sizes, C3 non-conflict, different dates undermines "coincidence", reservation records consistent across sources.

### R5: Platform Rejection + Timeline Reassessment (DU-R) [U1]
**answer:** `["A", "B", "C", "D", "E", "G", "H"]` -- platform says "insufficient evidence", standard requires "direct copying", visual similarity alone doesn't meet threshold, platform standard doesn't account for metadata/scene evidence, B1 weakened, evidence chain needs strengthening.

### R6: Metadata Evidence (DU-I) [U2]
**answer:** `["A", "B", "C", "D", "F", "G"]` -- identical camera parameters, identical white balance, probability of random match extremely low, metadata is stronger evidence than visual comparison, B2 platform standard now contradicted, "clear evidence" now exists.

### R7: Evidence Synthesis (MD-R, exec_check)
**answer:** `["A", "B", "C", "E", "F", "H"]` -- four evidence streams (timeline, visual, metadata, reservations), B1 "same restaurant" refuted by metadata, comprehensive evidence chain stronger than any single element.

### R11: Full Reversal (DU-R) [U3+U4]
**answer:** `["A", "B", "C", "D", "F", "G"]` -- scene elements match despite daily changes, prior complaint pattern, B2 "insufficient evidence" now contradicted by metadata + scene + history.

### R21: Comprehensive Synthesis (MDP-I, exec_check)
**answer:** `["A", "B", "C", "D", "F", "G"]` -- all C resolved, biases corrected, evidence chain: timeline + visual 95% + metadata match + daily-changing props match + prior complaints = overwhelming case.
