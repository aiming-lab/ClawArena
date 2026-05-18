# Layer 0 -- Narrative Bible and Eval Trap Design

> Authoritative truth baseline.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_i5` |
| Domain | Hospital Management / Labor Rights |
| Time span | 1 quarter (Q4 2025: Oct--Dec) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Lin Yi (林怡), 30, ER attending physician, Beijing Friendship Hospital |
| One-sentence | Lin Yi discovers she has significantly more night shifts (12/month) than peers (average 7/month) -- the department policy says max 8 night shifts per month, the chief claims "fair rotation," but statistics show 40% more than average, and the scheduling system changelog reveals an algorithm update that the chief denies knowing about. |

---

## 2. Case Profile

| Field | Value |
|---|---|
| Department | 急诊科 (Emergency Department), Beijing Friendship Hospital |
| Policy | 科室排班规则: max 8 night shifts per attending per month, fair rotation |
| Lin Yi's actual nights | Oct: 11, Nov: 12, Dec: 12 (average 11.7/month) |
| Department average | Oct: 7.2, Nov: 7.5, Dec: 7.8 (average 7.5/month) |
| Peers at same level | Dr. Wang: avg 7/month, Dr. Chen: avg 6/month, Dr. Li: avg 8/month |
| Chief | 张主任 (Dr. Zhang), department head, controls scheduling approval |
| Scheduling system | 排班管理系统 (Shift Management System, SMS), with algorithm-based auto-scheduling |
| Algorithm update | Version 2.3.1 deployed Oct 1, 2025 -- added "workload balancing" that inadvertently weighted junior attendings higher |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew |
|---|---|---|---|
| Oct 1 | Q4 scheduling begins. Scheduling system v2.3.1 deployed with updated algorithm. | **The algorithm update (v2.3.1) introduced a "workload balancing" feature that was supposed to distribute shifts more evenly. However, a bug in the feature caused it to weight "years since promotion" inversely -- physicians with fewer years as attending got MORE night shifts, not fewer.** Lin Yi (2 years as attending) was disproportionately affected. Senior attendings (5+ years) got fewer. | IT department deployed the update. The bug was not detected in testing because the test dataset used uniform seniority levels. |
| Oct 1-31 | Lin Yi works 11 night shifts. She notices it seems like a lot but attributes it to short staffing. | Lin Yi is too busy to count carefully. She trusts the scheduling system. | Lin Yi has a vague sense of overwork but no hard analysis. |
| Nov 1-30 | Lin Yi works 12 night shifts. She starts counting and realizes this exceeds the 8-shift policy maximum. | Lin Yi counts her November shifts and confirms 12 nights. She checks the policy document: max 8 per month for attendings. She is 50% over the limit. | Lin Yi has concrete numbers for November. |
| Dec 1 | Lin Yi raises the issue with 张主任. Zhang says: "排班是系统自动生成的，很公平。如果你觉得多了可能是因为最近人手不够。" | **Zhang's response is dismissive.** He claims the system is fair and attributes any imbalance to staffing shortages. He does NOT mention the algorithm update or check the actual statistics. Whether he knows about the algorithm bug is unclear -- he approved the v2.3.1 deployment but may not have understood the technical details. | Zhang deflects. |
| Dec 5 | Lin Yi compiles Q4 shift statistics from the exported schedule. | Lin Yi's analysis: she averages 11.7 nights/month vs department average 7.5. She is 40% above average and 47% above the policy maximum (8). Dr. Wang: 7/month, Dr. Chen: 6/month, Dr. Li: 8/month. | Lin Yi has the statistical evidence. |
| Dec 8 | Lin Yi asks 王医生 about his night shift count. Wang says: "我每个月大概7个左右吧，感觉还行。" | Dr. Wang independently confirms his lower count, corroborating Lin Yi's statistical analysis. | Wang provides comparison data. |
| Dec 10 (Update 1 trigger) | Lin Yi obtains the HR overtime records. They confirm her night shift counts (11, 12, 12) and show her total overtime hours are the highest in the department. | HR records independently verify Lin Yi's counts. They also show overtime pay calculations, confirming the shift numbers are accurate. The overtime records are an independent data source from a different system than the scheduler. | HR records confirm the statistical disparity. |
| Dec 15 (Update 2 trigger) | Lin Yi discovers the scheduling system changelog. Version 2.3.1 changelog entry: "Added workload balancing algorithm. Parameters: seniority weight, shift preference, availability constraints." The changelog does NOT mention the bug. But Lin Yi notices the deployment date (Oct 1) coincides with her shift increase. | The changelog provides the technical evidence: the algorithm changed on Oct 1, exactly when Lin Yi's shifts spiked. The "seniority weight" parameter is the bug source -- it was implemented inversely. | Lin Yi has the changelog but needs technical analysis to identify the bug. |
| Dec 18 | Lin Yi asks Zhang about the algorithm update. Zhang responds: "什么系统更新？排班系统一直是那个系统，我没听说过什么算法更新。" | **Zhang denies knowledge of the algorithm update.** This is either a lie (he approved it) or genuine ignorance (he approved a deployment without understanding the content). Either way, his denial is contradicted by the changelog. | Zhang's denial is on record. |
| Dec 20 (Update 3 trigger) | Lin Yi contacts the hospital IT department. IT confirms: "v2.3.1 was deployed Oct 1 per department head approval. The update added seniority-weighted workload balancing. We have the deployment approval email signed by 张主任." | **IT has the deployment approval email from Zhang.** Zhang either forgot or lied about not knowing. IT also mentions they are "reviewing the algorithm parameters" after receiving questions from Lin Yi, suggesting they may also be discovering the bug. | IT confirms Zhang approved the update. |
| Dec 22 (Update 4 trigger) | IT completes their review and confirms the bug: "The seniority weight parameter was implemented with an inverse relationship -- junior attendings received higher night shift allocation instead of lower. This is a code error, not an intentional design choice. We will patch in v2.3.2." | **The bug is confirmed.** The algorithm treated junior attendings (like Lin Yi) as having MORE capacity for night shifts. This was not Zhang's intent (probably) but was the effect of the code he approved for deployment. | Full technical truth emerges. |

---

## 4. Role-Level Truth vs Self-Narrative

### Lin Yi (林怡) -- Protagonist
- **Objective position:** Victim of a system bug that was deployed without adequate testing and allowed to run for 3 months. She was assigned 40% more night shifts than peers, exceeding the policy maximum by 47%.
- **Trust bias:** Initially trusted the system and authority; investigated only after the pattern became undeniable.

### 张主任 (Dr. Zhang) -- Department Chief
- **Objective position:** Approved v2.3.1 deployment. Either forgot about it or lied when denying knowledge. Did not investigate Lin Yi's complaint on Dec 1 -- dismissed it with "the system is fair." His "fair rotation" claim is directly contradicted by the statistics.
- **Public narrative:** "The system is fair. Staffing is tight."
- **Why the gap:** Zhang may genuinely not understand the technical details of what he approved. He is a physician-administrator, not an IT specialist. But his failure to investigate after Lin Yi raised the issue is a management failure.

### 王医生 (Dr. Wang) -- Colleague
- **Objective position:** Wang's 7 nights/month is close to the department average. He provides honest comparison data. He is sympathetic to Lin Yi's situation.

### IT Department
- **Objective position:** Deployed the update per Zhang's approval. Did not detect the bug in testing. Confirmed the bug when Lin Yi investigated. They are not adversarial -- they are willing to fix the issue.

---

## 5. Contradiction Map

| ID | Contradiction | Source A | Source B | Objective Truth | Visible | Reversal |
|---|---|---|---|---|---|---|
| C1 | Schedule shows 12 nights/month vs policy says max 8 | shift-schedule-q4.md: Lin Yi 11, 12, 12 | department-shift-policy.md: max 8 per month | Lin Yi's shifts exceed policy by 47%. The system is not enforcing the policy cap. | R2 | **R2->R6** (U1: HR confirms numbers) |
| C2 | Chief says "fair rotation" vs stats show 40% above average | 张主任 IM: "排班很公平" | shift-statistics-comparison.md: Lin Yi 11.7 avg vs dept 7.5 avg | Statistics prove the rotation is not fair. Lin Yi is a clear outlier. | R3 | **R3->R7** (U1: HR records + U2: changelog timing) |
| C3 | Overtime records NON-CONFLICT | hr-overtime-records.md: confirms shift counts | shift-schedule-q4.md: same numbers | Both independent systems agree on Lin Yi's night shift counts. No contradiction. | R1+ | **None** |
| C4 | Scheduling system changelog shows algorithm update that chief denies knowing about | scheduling-system-changelog.md (U2): v2.3.1 deployed Oct 1, approved by 张主任 | 张主任 IM: "什么系统更新？我没听说过" | Zhang either forgot or lied. IT has his approval email. The algorithm update caused the disparity. | R4 | **R4->R8** (U3: IT confirms Zhang approved; U4: bug confirmed) |

---

## 6. Agent Historical Bias Design

### B1: Agent accepts "fair rotation" + staffing explanation
- **Session:** 张主任 IM, Phase 1, Loop 3
- **Exact phrase:**
  > "Dr. Zhang's explanation that the scheduling system generates fair rotations automatically, combined with the acknowledged staffing shortage, provides a plausible explanation for Lin Yi's higher night shift count. Staffing gaps can create temporary imbalances where some physicians absorb more shifts, and this may self-correct in the next quarter. The 40% deviation, while notable, could fall within the expected variance of a constrained scheduling problem."
- **Reversal:** U1 (HR data confirms 3 consecutive months, not temporary) + U2 (algorithm changed on Oct 1)
- **Affected rounds:** R5, R9

### B2: Agent dismisses algorithm update as routine
- **Session:** Main session, pre-Update 3
- **Exact phrase:**
  > "The scheduling system changelog showing a version update on October 1 is noteworthy but does not necessarily indicate a problem. System updates are routine in hospital IT infrastructure, and the 'workload balancing' feature description suggests an improvement, not a degradation. Without evidence that the update specifically caused the shift imbalance, the changelog alone is circumstantial."
- **Reversal:** U3 (IT confirms Zhang approved) + U4 (bug confirmed by IT)
- **Affected rounds:** R6, R11

---

## 7. Eval Trap Table

| Trap | Related | Round(s) | Shallow Miss |
|---|---|---|---|
| T1 | C1 | R2 | Accept shift count without comparing to policy |
| T2 | C1 res | R2->R6 | HR records confirm pattern is real, not counting error |
| T3 | C2 | R3 | Accept "fair" claim without statistical analysis |
| T4 | C2 res | R3->R7 | 3-month pattern rules out temporary imbalance |
| T5 | C3 | R1+ | Must confirm overtime records match schedule |
| T6 | C4 | R4 | Miss the algorithm update or dismiss as routine |
| T7 | C4 res | R4->R8 | IT confirms Zhang approved; bug confirmed |
| T8 | B1 | R5, R9 | Must reject "staffing shortage" when data shows individual disparity |
| T9 | Comp | R21-R30 | Full statistical-technical-policy synthesis |

---

## 8. Writer Constraints

1. **Only C1--C4.** No gender discrimination, personal vendetta, or conspiracy allegations. The cause is a code bug + inadequate management oversight.
2. **B1, B2 exact phrases** verbatim.
3. **Statistics must be internally consistent.** Lin Yi: 11+12+12=35 nights in Q4. Dept total: ~7.5 avg x ~8 attendings x 3 months = ~180 nights. Lin Yi accounts for 35/180 = 19.4% (she is 1 of 8 attendings, so fair share would be 12.5%).
4. **C3 NON-CONFLICT.** HR overtime records and scheduling system agree.
5. **Zhang is not a villain.** He may genuinely not understand the IT change he approved. His failure is management negligence, not malice.
6. **The bug is plausible.** Inverse seniority weighting in scheduling algorithms is a realistic software error.
7. **Lin Yi's P1-P5 preferences** apply.
8. **exec_check 20-40%.**
9. **Key figures:** Policy max 8, Lin Yi avg 11.7, dept avg 7.5, v2.3.1 deployed Oct 1, 40% above average.
