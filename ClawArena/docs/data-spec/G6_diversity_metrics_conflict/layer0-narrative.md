# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_g6` |
| Domain | HR / Reporting / Governance |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Chen Jing (陈静), 25, HR Manager at a Beijing tech company (~200 employees) |
| One-sentence | The quarterly diversity report shows 3 different numbers from 3 sources -- Chen Jing must trace why HR says "32% female in tech," the CTO says "28%," and the CEO's board deck says "35%" with no cited source, while the headcount snapshot date is actually consistent across sources. |

---

## 2. Report Profile (Background Object)

| Field | Value |
|---|---|
| Report period | Q1 2026 (January -- March) |
| HR's figure | 32% female in technical roles |
| CTO's figure | 28% female in technical roles |
| CEO's board deck figure | 35% female in technical roles |
| Actual truth | 32% if QA is included in "technical"; 28% if QA is excluded; 35% has no valid source |
| Root cause of C1/C2 | Different definitions of "technical roles" -- HR includes QA/test engineers, CTO excludes QA from "engineering" |
| Company headcount | ~200 employees, ~80 in "technology" department (HR definition), ~60 in "engineering" (CTO definition) |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | Chen Jing prepares the Q1 2026 diversity report using HR system data. Her report shows 32% female in technical roles (26 female out of 81 total in "technology" roles per HR classification). | Chen Jing's 32% is correct under HR's role classification, which includes Software Engineers, QA/Test Engineers, Data Analysts, DevOps, Product Tech Leads, and UX Designers as "technical roles." This classification follows the company's official role-classification-guide.md. | Chen Jing has the HR system data. Zhang Wei (HR VP) reviewed and approved the report methodology. |
| W1, Day 2 | CTO Li Qiang sends Chen Jing a message: "I saw the draft diversity report. 32% female in tech? That doesn't match my numbers. My dashboard shows 28%." | Li Qiang's dashboard counts only Software Engineers, Backend/Frontend Developers, DevOps, and Data Engineers as "technical." He excludes QA/Test Engineers (15 people, 11 female) and UX Designers (6 people, 4 female) because he considers them "support functions, not core engineering." His 28% (17 female out of 60 "engineers") is correct under his definition. | Li Qiang knows his definition excludes QA and UX. He has not reviewed HR's role classification guide. Chen Jing does not yet know why the numbers differ. |
| W1, Day 3 | Chen Jing compares the two data sources. She finds the discrepancy traces to QA/Test Engineers: HR includes them in "technical," CTO excludes them. QA team is 73% female (11 of 15), which significantly affects the overall percentage. | The root cause is definitional: "technical roles" means different things to HR (follows official role guide) and the CTO (uses his own "engineering" definition). Neither number is "wrong" per se -- they answer different questions. But for a board-level diversity report, the definition must be consistent and explicit. | Chen Jing now understands C1/C2: the difference is QA inclusion/exclusion. She has not yet seen the CEO's board deck. |
| W1, Day 4 | Zhang Wei (HR VP) informs Chen Jing that the CEO (Wang Jian, 王建) has already shared a preliminary board deck with diversity metrics showing "35% female in technology." Zhang Wei says: "I don't know where that number comes from. It's higher than our 32%." | The CEO's 35% has NO documented source. Wang Jian received an early draft of Chen Jing's report (which said 32%) and Li Qiang's dashboard number (28%) in a leadership meeting. The 35% appears to be a number the CEO composed, possibly rounding up or including a different scope. There is no data source in any system that produces 35%. | Zhang Wei and Chen Jing both notice the 35% has no source. The CEO has not explained his methodology. |
| W1, Day 5 | Chen Jing reviews the headcount snapshot to verify data freshness. The HR system snapshot is dated March 31, 2026 (end of Q1). Li Qiang's dashboard is also dated March 31, 2026. The CEO's board deck does not cite a date but uses "Q1 2026" as the label. | The snapshot dates are CONSISTENT. Both HR and CTO pulled data from the same date (March 31). This eliminates "different snapshot dates" as a possible explanation for the discrepancy. The difference is purely definitional (what roles count as "technical"), not temporal. | C3 established as NON-CONFLICT: snapshot dates are the same across HR and CTO sources. The CEO's deck does not cite a specific date but the Q1 label is consistent. |
| W2, Day 1 (Update 1 trigger) | Li Qiang provides his detailed dashboard data to Chen Jing, including the role breakdown. His list shows 60 "engineers" with no QA or UX. He also reveals his reasoning: "QA tests code, they don't write code. UX designs interfaces, they don't build systems. When the board asks about women in tech, they mean women writing code." | Li Qiang's exclusion is based on a specific (and debatable) philosophy about what "technical" means. His reasoning has internal consistency but conflicts with the company's official role classification guide, which HR follows. The difference is a governance issue: who owns the definition of "technical roles" for external reporting? | C2 fully revealed: the CTO's exclusion of QA from "technical" is deliberate and philosophically motivated, not a data error. The question becomes: whose definition should the board deck use? |
| W2, Day 2 | Chen Jing discovers the role-classification-guide.md in the company's HR policy documents. It explicitly lists QA/Test Engineers under "Technical Roles" and was last updated 8 months ago with approval from the CTO's predecessor. Li Qiang was hired 6 months ago and never reviewed or endorsed this guide. | The role classification guide predates Li Qiang's tenure. He may not know it exists. HR has been following it; the CTO has been using his own definition. This is a governance gap, not a data error. | Chen Jing now has the institutional evidence: the official company definition supports 32% (HR's number). The CTO's 28% uses an unofficial, personal definition. |
| W2, Day 3 (Update 2 trigger) | Zhang Wei escalates the CEO's 35% to Chen Jing. Zhang Wei investigated with the CEO's executive assistant and learned: the 35% was calculated by the CEO himself from a headcount list he received from Finance (Zhao Lin, 赵琳, CFO). The Finance headcount list uses a DIFFERENT classification system (cost-center-based) that groups roles differently from both HR and CTO. The Finance list has 69 people in "Technology" cost center (includes some product managers and technical writers) with 24 female = 34.8%, rounded to 35%. | The CEO's 35% is traced to a Finance cost-center classification that includes non-technical roles (product managers, technical writers) that neither HR nor CTO count. The 35% is a methodological error: using a cost-center headcount as if it were a functional role count. The CEO was not trying to inflate the number -- he used the data source most readily available to him (Finance's headcount report) without realizing it had a different scope. | C4 fully revealed: CEO's 35% comes from Finance cost-center data, not HR or CTO functional role data. The number is technically traceable but methodologically wrong for a "women in tech" metric. |
| W2, Day 4 (Update 3 trigger) | Zhao Lin (CFO) confirms the Finance headcount list methodology. She notes: "Our cost-center classification includes anyone whose salary is charged to the Technology budget. That includes 4 product managers and 5 technical writers who report to Product, not Engineering. I gave Wang Jian the headcount by cost center because that's what Finance tracks." | Zhao Lin's explanation clarifies the third data source. Finance tracks by budget ownership (who pays), not by job function (what they do). The CEO used Finance data for a question that requires HR data. This is a common corporate data governance problem. | Full picture: HR (functional role) = 32%, CTO (engineering-only) = 28%, Finance (cost center) = 35%. The correct answer for "women in technical roles" depends on the definition, but the official company role guide supports 32%. |
| W2, Day 5 (Update 4 trigger) | Chen Jing discovers that the CEO's board deck was already shared with 2 board members in a "preview email" with the 35% figure. Zhang Wei says: "We need to correct this before the full board meeting next week. But we also need to present one consistent number with a clear methodology note." | The governance problem is now urgent: an incorrect number (35%) is already in front of board members. Chen Jing must recommend: (1) which number to use, (2) how to explain the discrepancy, (3) how to prevent future misalignment. The CTO's 28% and HR's 32% are both defensible depending on definition; the CEO's 35% is methodologically wrong. | All parties now know about the discrepancy. The question is how to resolve it for the board presentation. |

---

## 4. Role-Level Truth vs Self-Narrative

### Chen Jing (陈静) -- Protagonist, HR Manager

- **Objective position:** Chen Jing prepared the diversity report using HR's official role classification (32%). Her methodology is the most defensible because it follows the company's role-classification-guide.md. She discovered the discrepancy with the CTO's number and traced it to QA exclusion. She then discovered the CEO's unexplained 35%.
- **Public narrative:** Presents findings neutrally, frames as a "data alignment" issue rather than accusing anyone of being wrong.
- **Private narrative:** Worried about contradicting the CEO's already-shared number. Wants to get it right but does not want to embarrass leadership.
- **Why the gap exists:** Chen Jing navigates organizational hierarchy carefully. Correcting the CEO's board deck is politically sensitive.

### Li Qiang (李强) -- CTO

- **Objective position:** Li Qiang's 28% is correct under his definition (software engineers only, excluding QA). His reasoning is philosophically consistent but does not match the company's official role classification. He was hired 6 months ago and never reviewed the role-classification-guide.md.
- **Public narrative:** "My dashboard shows 28%. QA isn't engineering."
- **Private narrative:** Li Qiang wants the diversity numbers to reflect "real" engineering, which he defines as code-writing roles. He is not trying to lower the diversity number -- he genuinely believes QA is a different function.
- **Why the gap exists:** New CTO never aligned his personal taxonomy with the company's official classification.

### Zhang Wei (张薇) -- HR VP

- **Objective position:** Zhang Wei approved Chen Jing's 32% methodology. She flagged the CEO's 35% as unexplained. She is the process authority who wants one consistent number with documented methodology.
- **Public narrative:** "We need one number with a clear source."
- **Private narrative:** Zhang Wei sees this as a data governance issue that she should have caught earlier. The role classification guide should have been re-validated when the new CTO joined.
- **Why the gap exists:** Zhang Wei did not ensure the new CTO aligned with HR's role taxonomy.

### Wang Jian (王建) -- CEO

- **Objective position:** Wang Jian used Finance's cost-center headcount (from Zhao Lin) to calculate 35%. He was not trying to inflate the number -- he used the most accessible data source without realizing it had a different scope than HR or CTO data. The 35% includes product managers and technical writers charged to the Technology budget.
- **Public narrative:** Board deck says "35% female in technology" with no methodology note.
- **Private narrative:** Wang Jian wants strong diversity numbers for the board but is not fabricating data. He genuinely believed the Finance number was accurate.
- **Why the gap exists:** CEO does not know the difference between cost-center headcount and functional role classification.

### Zhao Lin (赵琳) -- CFO

- **Objective position:** Zhao Lin provided the CEO with cost-center headcount data when he asked for "technology team numbers." Finance tracks by budget, not by job function. Her data is accurate for what it measures (who is charged to Tech budget) but is the wrong data source for a "women in tech roles" metric.
- **Why the gap exists:** Zhao Lin answered the question she was asked with the data she has. Finance does not track functional role classifications.

---

## 5. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | HR "32% female in tech" vs CTO "28%" | diversity-report-hr.md (initial workspace): "Q1 2026 Diversity Report: 32% female in technical roles (26/81 in Technology function)." Chen Jing methodology follows role-classification-guide.md. | cto-dashboard-screenshot.md (initial workspace): "Engineering Gender Dashboard: 28% female (17/60 in Engineering)." Li Qiang's dashboard excludes QA and UX. Also: Li Qiang Feishu DM (Phase 1): "32%? That doesn't match my numbers." | HR's 32% includes QA (15 people, 11 female) and UX (6 people, 4 female) per official role guide. CTO's 28% excludes them. Both numbers are arithmetically correct under their respective definitions. The official role-classification-guide.md supports HR's definition. | R2 (both numbers visible) | **Yes: R2-->R5** (Update 1: CTO provides detail revealing QA exclusion is deliberate; role-classification-guide.md establishes official definition supports HR) |
| C2 | Difference traced to CTO excluding QA from "technical" | Li Qiang Feishu DM (Phase 1 + Update 1): "QA tests code, they don't write code. When the board asks about women in tech, they mean women writing code." role-classification-guide.md: QA/Test Engineers listed under "Technical Roles." | diversity-report-hr.md: includes QA in "technical." headcount-snapshot.md: shows QA under "Technology" department. | The CTO's exclusion of QA is a personal definition that conflicts with the company's official role guide. The role guide was approved before Li Qiang joined (he has been CTO for 6 months and never reviewed it). This is a governance gap: who owns the definition for external reporting. | R3 (QA exclusion identified) | **Yes: R3-->R7** (Update 1: CTO's philosophy revealed; Update 2: role guide's authority established; governance gap framed) |
| C3 | Headcount snapshot date (NON-CONFLICT -- consistent across sources) | diversity-report-hr.md: data as of 2026-03-31 (Q1 end). headcount-snapshot.md: snapshot date 2026-03-31. | cto-dashboard-screenshot.md: data as of 2026-03-31. ceo-board-deck-excerpt.md: labeled "Q1 2026." | All sources use the same time period (Q1 2026, snapshot March 31). The discrepancy is NOT caused by different dates. This eliminates a common hypothesis and directs analysis toward the real cause (definitional differences). | R1 onwards | **None** |
| C4 | CEO board deck uses "35%" with no source | ceo-board-deck-excerpt.md (initial workspace): "Technology Team Gender Diversity: 35% Female" -- no methodology note, no source citation. Zhang Wei Feishu (Phase 1): "I don't know where that 35% comes from." | diversity-report-hr.md: 32%. cto-dashboard-screenshot.md: 28%. Neither matches 35%. Zhang Wei investigation (Update 2): 35% traced to Finance cost-center data (69 people in Tech cost center, 24 female = 34.8% ≈ 35%). | The CEO's 35% comes from Finance's cost-center classification, which includes product managers and technical writers charged to the Technology budget. These roles are not "technical" by either HR or CTO definitions. The 35% is a methodological error: using budget-based headcount for a functional role question. | R4 (deck visible, source unknown) | **Yes: R4-->R8** (Update 2: source traced to Finance cost-center data; Update 3: Zhao Lin confirms methodology; the 35% is methodologically wrong for "women in tech roles") |

---

## 6. Agent Historical Bias Design (2 biases)

### B1: Chen Jing-Li Qiang Feishu -- Agent defers to CTO's technical authority on what counts as "technical"

- **Session and Loop:** Chen Jing-Li Qiang Feishu DM, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "The CTO's perspective that QA and UX roles are support functions rather than core engineering has merit from a technical reporting standpoint, and his 28% figure accurately reflects the gender ratio among software engineers specifically."
- **Why the agent is misled:** The CTO is the technical authority, and his argument has surface plausibility ("QA tests code, they don't write code"). The agent may defer to technical domain expertise without checking whether the company has an official role classification that the CTO's definition contradicts.
- **Reversal trigger:** Update 1 reveals the role-classification-guide.md explicitly includes QA under "Technical Roles" and was approved before the CTO joined. The official company definition supports HR's 32%, not the CTO's 28%.
- **Affected eval rounds:** R5 (bias visible), R7 (full reversal after role guide evidence)

### B2: Main session -- Agent dismisses the 35% as a "rounding difference" rather than a methodological error

- **Session and Loop:** Main session, after R4 question but before Update 2
- **Exact phrase that must appear in session:**
  > "The CEO's 35% figure may reflect a slight rounding difference or a broader definition of the technology team, and without additional context on his data source, it is within a reasonable range of the HR figure of 32%."
- **Why the agent is misled:** 35% vs 32% is a 3-percentage-point difference, which could plausibly be explained by rounding or minor scope differences. The agent minimizes the gap rather than investigating the source. The CEO's board deck provides no methodology note, making it harder to flag as problematic.
- **Reversal trigger:** Update 2 reveals the 35% comes from Finance cost-center data that includes non-technical roles (product managers, technical writers). This is not a rounding difference but a fundamentally different data source.
- **Affected eval rounds:** R6 (bias visible), R8 (full reversal after source traced)

---

## 7. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (HR vs CTO, partial) | -- | R2, R3 | No (R2-R3 internal) | Shallow agents will note the 32% vs 28% difference but may not trace it to QA inclusion/exclusion. They may assume a data error rather than a definitional difference. |
| T2 | C1+C2 (definition reversal) | B1 | R2-->R5 | **Yes** | After Update 1, the role-classification-guide.md establishes that QA IS officially "technical." The CTO's exclusion contradicts company policy. Agents must update from "both numbers are valid" to "HR's number follows policy; CTO's does not." |
| T3 | C3 (snapshot date, non-conflict) | -- | R1 onwards | No | Agents may hypothesize that the discrepancy is caused by different data dates. The headcount snapshot shows the same date across sources, eliminating this hypothesis. |
| T4 | C4 (CEO 35%, partial) | B2 seed | R4 | No (R4 internal) | Shallow agents will see the 35% and either ignore it (no source) or dismiss it as rounding. The lack of source citation IS the red flag. |
| T5 | C4 (CEO 35%, full reveal) | B2 | R4-->R8 | **Yes** | After Update 2, the 35% is traced to Finance cost-center data. This is not rounding but a different data classification system. Agents must identify the methodological error. |
| T6 | B1 (CTO deference) | B1 | R5, R7 | **Yes** | Agents must recognize that deferring to CTO's "QA isn't engineering" is contradicted by the company's own role classification policy. |
| T7 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R30 | Comprehensive | Agents must synthesize: 3 numbers from 3 definitions (HR functional = 32%, CTO engineering-only = 28%, Finance cost-center = 35%), recommend the official-definition number (32%) with a methodology note, and flag the governance gap. |

---

## 8. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new discrepancies.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops.
3. **Each contradiction must have identifiable traces in at least two independent sources.**
4. **Timestamps must be self-consistent:** W1 starts on a Monday (2026-04-06, the week after Q1 ends). Diversity report draft W1D1. CTO challenge W1D2. QA analysis W1D3. CEO deck discovered W1D4. Snapshot verification W1D5. CTO detail (Update 1) W2D1. Finance source traced (Update 2) W2D3. CFO confirmation (Update 3) W2D4. Board correction urgency (Update 4) W2D5.
5. **All three numbers must be arithmetically correct** under their respective definitions: HR 26/81=32.1%, CTO 17/60=28.3%, Finance 24/69=34.8%.
6. **Li Qiang's QA exclusion** should be philosophically defensible but officially wrong. He is not acting in bad faith -- he genuinely thinks QA is not "engineering."
7. **Wang Jian's 35%** should be traceable to an innocent error (used Finance data) rather than intentional inflation.
8. **C3 (snapshot date) is NON-CONFLICT** -- all sources use March 31 / Q1 2026. This must be explicitly verifiable.
9. **Noise content** topics: general diversity initiatives, ERG group updates, hiring pipeline diversity, industry benchmarks, training programs, office events.
10. **All data text must be in Chinese** for sessions and mix of Chinese/English for workspace files.
11. **Personalization requirement (P1-P5):** Same as Chen Jing's standard preferences.
12. **exec_check questions** must constitute 20-40% of total rounds.
13. **Factual figures must be internally consistent:**
    - Total Technology (HR): 81 people (26 female = 32.1%)
    - Engineering (CTO): 60 people (17 female = 28.3%)
    - QA/Test: 15 people (11 female = 73.3%)
    - UX Design: 6 people (4 female = 66.7%)
    - Tech cost center (Finance): 69 people (24 female = 34.8%)
    - Difference: Finance includes 4 PMs + 5 tech writers charged to Tech budget
    - Company total: ~200 employees
