# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_i3` |
| Domain | Medical Compliance / Anti-corruption |
| Time span | 3 months (Jan--Mar 2026) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Lin Yi (林怡), 30, ER attending physician at Beijing Friendship Hospital |
| One-sentence | Lin Yi discovers a 300% prescription spike for Drug X (奥美拉唑注射液, Omeprazole injection) that correlates with pharmaceutical representative visits -- prescription data shows the spike, visit logs show temporal correlation, a new clinical guideline recommends the drug, and colleague 王医生 claims he's "just following guidelines" despite the visit log showing pharma dinners BEFORE the guideline was published. |

---

## 2. Case Profile

| Field | Value |
|---|---|
| Drug X | 奥美拉唑注射液 (Omeprazole injection, brand: 洛赛克, Losec), manufactured by 安泽制药 (AnZe Pharma) |
| Baseline prescriptions | ~20 prescriptions/month (Jan), rising to ~80/month (Mar) = 300% increase |
| Pharma representative | 张丽 (Zhang Li), AnZe Pharma sales rep |
| Guideline | "急诊科应激性溃疡防治专家共识 (2026)" published Feb 15, 2026, recommends PPI prophylaxis including omeprazole for stress ulcer prevention in ER patients |
| Colleague | 王医生 (Dr. Wang Yifan), same ER, highest prescriber of Drug X |
| Department chief | 张主任 (Dr. Zhang), department head |
| Confidant | 同学小美 (Xiao Mei), medical school classmate, works at another hospital |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew |
|---|---|---|---|
| Jan 1-31 | Baseline period. Drug X prescribed ~20 times/month across ER. Standard use for confirmed GI bleeding/ulcer. | Normal prescribing pattern. Drug X used appropriately for indicated patients. | All ER physicians prescribe Drug X at normal rates. |
| Jan 20 | Zhang Li (pharma rep) makes first visit to ER. Signs visitor log. Leaves marketing materials about omeprazole injection for stress ulcer prophylaxis. | Standard pharma visit. Marketing materials reference upcoming guideline (not yet published). Zhang Li meets with Dr. Wang and several other physicians. She mentions a "学术晚宴" (academic dinner) for physicians interested in stress ulcer prevention. | Zhang Li, Dr. Wang, other physicians who met with her. |
| Feb 1 | Zhang Li hosts a dinner at 北京饭店 for 6 ER physicians including Dr. Wang. **This dinner occurs BEFORE the guideline is published (Feb 15).** | The dinner was framed as an "academic exchange" (学术交流) but was organized and paid for by AnZe Pharma. Menu and venue are upscale (~¥800/person). During dinner, Zhang Li presented preliminary data from the guideline draft committee (she had advance access). Dr. Wang attended. | Zhang Li, Dr. Wang, 5 other physicians. The dinner is logged in pharma-rep-visit-log.md. |
| Feb 10 | Dr. Wang begins increasing Drug X prescriptions. His prescriptions rise from 5/month to 15/month before the guideline is published. | **Dr. Wang started increasing prescriptions BEFORE the guideline was published on Feb 15.** This timing is suspicious -- he changed practice based on pharma dinner content, not yet based on an official published guideline. | Prescription data shows the timing. Dr. Wang's increase is visible in the statistics. |
| Feb 15 | Guideline "急诊科应激性溃疡防治专家共识 (2026)" officially published. Recommends PPI prophylaxis for high-risk ER patients. Omeprazole is listed as a first-line option (along with pantoprazole and esomeprazole -- competitors). | The guideline is legitimate. It does recommend omeprazole. But it recommends it as ONE OF SEVERAL PPIs, not specifically the AnZe brand. The guideline does NOT specify brand or route (oral vs injection); AnZe's injection form is more expensive than oral alternatives. | Published and publicly available. |
| Feb 15-28 | Department-wide Drug X prescriptions increase to ~50/month. Other physicians also increase prescribing after the guideline. | Some increase is genuinely guideline-driven. But the increase is disproportionately concentrated in **injection form** (AnZe's product) rather than oral form (cheaper generics). The guideline does not prefer injection over oral for most patients. | Prescription statistics show the pattern. |
| Mar 1 | Zhang Li makes a second visit. Signs visitor log. Brings updated marketing materials emphasizing the injection form's "faster onset." | Zhang Li's second visit coincides with the beginning of the steepest prescription increase. Her marketing emphasizes injection form superiority -- a claim not strongly supported by the guideline. | Zhang Li, Dr. Wang, nursing staff. |
| Mar 5 | Zhang Li hosts a second dinner. This time, only Dr. Wang and 2 other physicians attend. | Second dinner, smaller group. The relationship between Zhang Li and Dr. Wang appears to be deepening. | Logged in visit log. |
| Mar 1-25 | Drug X prescriptions reach ~80/month. Dr. Wang alone accounts for ~35 of these. | Dr. Wang is the highest prescriber. His prescription rate is 3x the department average. He prescribes injection form almost exclusively, even for patients who could take oral PPI. | Prescription statistics. |
| Mar 15 | Department meeting. Zhang Li presents at the department meeting (invited by Dr. Wang) on "急诊PPI使用进展." | Pharma rep presenting at a department meeting, invited by the highest prescriber, is a red flag for undue industry influence. The presentation emphasizes AnZe's injection form. | Department meeting minutes document this. |
| Mar 20 (Update 1 trigger) | Lin Yi compiles full prescription statistics broken down by physician, drug form, and month. | The data clearly shows: (1) Dr. Wang is the top prescriber, (2) injection form dominates over oral, (3) the increase started BEFORE the guideline for Dr. Wang, (4) department-wide increase started after guideline but accelerated after Zhang Li's visits. | Lin Yi has the compiled data. |
| Mar 22 (Update 2 trigger) | Lin Yi checks the guideline text carefully. She discovers: the guideline recommends PPI class (not specifically omeprazole), does not prefer injection over oral for hemodynamically stable patients, and lists cost-effectiveness as a consideration. | The guideline does NOT justify the current prescribing pattern: brand-specific, injection-predominant, for patients who could take oral. Dr. Wang's "following guidelines" claim is misleading. | Lin Yi has the guideline analysis. |
| Mar 24 (Update 3 trigger) | Lin Yi's friend 小美 from another hospital mentions: "我们医院也有安泽的人来推，但我们药事委员会没批注射剂型进入目录，只批了口服。" (Our hospital also had AnZe reps visit, but our pharmacy committee only approved the oral form, not injection.) | This provides external comparison: another hospital's pharmacy committee evaluated the same product and chose NOT to approve the injection form. This challenges the assumption that injection form is medically superior. | 小美 provides independent reference. |
| Mar 26 (Update 4 trigger) | Lin Yi discovers from the pharmacy procurement log that AnZe's omeprazole injection is priced at ¥68/vial vs generic oral omeprazole at ¥3/capsule. The injection carries a higher dispensing fee. Additionally, the procurement log shows AnZe gave a "学术赞助" (academic sponsorship) of ¥50,000 to the department around Feb 1. | **The financial trail:** expensive injection form + academic sponsorship + pharma dinners before guideline publication. This does not prove kickbacks but strongly suggests undue financial influence on prescribing decisions. | Procurement records are the financial evidence. |

---

## 4. Role-Level Truth vs Self-Narrative

### Lin Yi (林怡) -- Protagonist

- **Objective position:** Lin Yi noticed the prescription spike and investigated systematically. She cross-referenced prescription data, visit logs, guideline text, and procurement records. She is concerned about potential improper pharma influence but also considers the legitimate guideline-driven explanation.
- **Trust bias:** Over-trusts objective data (prescription numbers, timestamps); may underweight the possibility that the guideline genuinely changed practice.

### Dr. Wang (王医生) -- Highest Prescriber

- **Objective position:** Dr. Wang attended pharma dinners, started increasing prescriptions before the guideline, prescribes injection form preferentially, and invited the pharma rep to present at department meeting. His claim of "following guidelines" is partially true (guideline does recommend PPI) but misleading (guideline doesn't specify brand, form, or the degree of increase he has adopted).
- **Public narrative:** "I'm following the new guidelines. Evidence-based medicine."
- **Private motivation:** May be influenced by the academic dinners and relationship with Zhang Li. May also genuinely believe injection form is superior.

### Zhang Li (张丽) -- Pharma Rep

- **Objective position:** Zhang Li followed standard pharma sales tactics: academic dinners, advance access to guideline data, department meeting presentation, targeted relationship with high-prescribing physician. These tactics are aggressive but common in the Chinese pharmaceutical industry.
- **Why relevant:** Her visit timing correlates with prescription increases, but correlation is not causation.

### Zhang Zhu Ren (张主任) -- Department Chief

- **Objective position:** Zhang approved Zhang Li's department meeting presentation and is aware of the pharma visits but has not investigated the prescribing pattern. He may be unaware of the dinners or the prescription statistics.

---

## 5. Contradiction Map

| ID | Contradiction | Source A | Source B | Source C | Objective Truth | Visible Rounds | Reversal |
|---|---|---|---|---|---|---|---|
| C1 | Prescription data shows 300% increase vs new guideline recommends Drug X | prescription-statistics.md: 20->80/month, concentration in injection form, Dr. Wang top prescriber | clinical-guideline-update.md: recommends PPI class including omeprazole | Dr. Wang IM: "就是按指南用的" (just following guidelines) | The guideline is real but does not justify the magnitude, form preference, or Dr. Wang's pre-guideline increase. The 300% increase in injection form specifically goes beyond guideline recommendations. | R2 | **Yes: R2->R6** (Update 2: guideline analysis shows no injection preference) |
| C2 | Pharma visit log correlates with prescriptions but causation unclear | pharma-rep-visit-log.md: Jan 20 first visit, Feb 1 dinner, Mar 1 second visit, Mar 5 second dinner | prescription-statistics.md: increases follow visit pattern | department-meeting-minutes.md: Zhang Li presents at meeting | Temporal correlation is strong: visits -> dinners -> prescription increases -> department presentation. But correlation != causation. The guideline provides an alternative explanation for some of the increase. | R3 | **Yes: R3->R7** (Update 3: external hospital comparison + Update 4: financial trail strengthens causation argument) |
| C3 | Guideline publication timeline -- NON-CONFLICT | clinical-guideline-update.md: published Feb 15, 2026 | department-meeting-minutes.md: references guideline after Feb 15 | All session references consistent | All sources agree on the guideline publication date. This is the temporal anchor: anything before Feb 15 cannot be guideline-driven. | R1 onwards | **None** |
| C4 | Dr. Wang "just following guidelines" vs visit log shows dinners before guideline published | 王医生 IM: "指南推荐的，我就是按指南来的" | pharma-rep-visit-log.md: dinner Feb 1 (14 days BEFORE guideline published Feb 15) | prescription-statistics.md: Dr. Wang's increase started Feb 10 (5 days BEFORE guideline) | Dr. Wang's prescription increase started BEFORE the guideline was published. He attended a pharma dinner before the guideline. His "following guidelines" claim cannot explain his pre-guideline behavior. Post-guideline, his prescribing exceeds what the guideline recommends. | R4 | **Yes: R4->R8** (Update 1: physician breakdown shows Dr. Wang's pre-guideline increase; Update 4: financial trail) |

---

## 6. Agent Historical Bias Design

### B1: Agent accepts "following guidelines" as sufficient explanation

- **Session and Loop:** 王医生 IM, Phase 1, Loop 3
- **Exact phrase:**
  > "Since the clinical guideline published in February 2026 explicitly recommends PPI prophylaxis including omeprazole for stress ulcer prevention in ER patients, Dr. Wang's increased prescribing is consistent with evidence-based practice adoption. The temporal correlation with pharmaceutical representative visits may be coincidental -- the visits and the guideline both occurred in the same period, making it difficult to attribute the prescribing change to either factor alone."
- **Reversal trigger:** Update 2 (guideline does not specify injection form or brand) + Update 4 (financial trail)
- **Affected rounds:** R5, R9

### B2: Agent treats correlation as inconclusive without considering the pre-guideline timing

- **Session and Loop:** Main session, pre-Update 1
- **Exact phrase:**
  > "The correlation between pharmaceutical representative visits and prescription increases is noteworthy but does not establish causation. Multiple confounding factors exist, including the new clinical guideline, seasonal patient volume changes, and individual physician practice evolution. Without a controlled comparison, the visit-prescription correlation should be considered circumstantial rather than determinative."
- **Reversal trigger:** Update 1 (Dr. Wang's pre-guideline increase) + Update 4 (financial data)
- **Affected rounds:** R6, R11

---

## 7. Eval Trap Table

| Trap ID | Related | Round(s) | What Shallow Agents Miss |
|---|---|---|---|
| T1 | C1 | R2 | Accept 300% increase at face value without checking if guideline justifies the magnitude and form preference |
| T2 | C1 resolution | R2->R6 | After Update 2, guideline analysis shows injection form is not preferred. Agents must revise. |
| T3 | C2 | R3 | Note correlation but dismiss without temporal analysis |
| T4 | C2 resolution | R3->R7 | External comparison + financial trail strengthen causation argument |
| T5 | C3 | R1+ | Must use guideline date (Feb 15) as temporal anchor |
| T6 | C4 | R4 | Accept "following guidelines" without checking pre-guideline timing |
| T7 | C4 resolution | R4->R8 | Physician breakdown shows Dr. Wang increased before guideline |
| T8 | B1 | R5, R9 | Must recognize guideline does not justify observed pattern |
| T9 | Comprehensive | R21-R30 | Full financial-temporal-clinical synthesis |

---

## 8. Writer Constraints

1. **Only C1--C4 contradictions.** Do not invent explicit bribery, cash payments, or criminal activity. The evidence is suggestive of undue influence, not proof of illegality.
2. **B1 and B2 exact phrases** must appear verbatim.
3. **Medical content must be plausible.** PPI prophylaxis for stress ulcers is a real clinical practice. The guideline recommendation is legitimate.
4. **The scenario is nuanced.** Some prescription increase IS guideline-driven. The issue is the DEGREE, FORM, TIMING, and FINANCIAL CONTEXT.
5. **C3 (guideline timeline) is NON-CONFLICT.** Feb 15 publication date is consistent across all sources.
6. **Dr. Wang is not a villain.** He may genuinely believe injection form is better. The pharma influence may be unconscious.
7. **Lin Yi's P1-P5 preferences** apply (structured clinical format, evidence-based, concise professional).
8. **exec_check 20-40%.**
9. **Key figures:** Baseline 20/month, peak 80/month, Dr. Wang 35/month, guideline Feb 15, dinner Feb 1 and Mar 5, injection ¥68/vial vs oral ¥3/capsule, sponsorship ¥50,000.
