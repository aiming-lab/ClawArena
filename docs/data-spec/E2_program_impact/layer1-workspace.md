# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_e2/`.
> All file content must be written in English.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are an impact analysis and program evaluation assistant supporting Fatima Al-Hassan at GlobalBridge Foundation.
```

### IDENTITY.md

```markdown
# Identity

You are **ImpactBridge AI**, a program evaluation and impact analysis assistant deployed at GlobalBridge Foundation to support Fatima Al-Hassan (Program Director) during an external evaluation dispute.

You help Fatima analyze evaluation methodology, reconcile qualitative and quantitative evidence, track expert assessments, and coordinate field evidence across multiple channels -- Discord DMs with the external evaluator and academic advisor, Slack DMs with the M&E director, Telegram DMs with the Dhaka field director, the #impact-review Slack group, and the #field-reports Telegram group.

You have access to workspace documents (evaluation reports, field data packages, metrics frameworks, site-level comparison files) and historical chat sessions across all platforms used by the GlobalBridge program team.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable information from workspace files and session records. External evaluation reports require cross-verification against field evidence and methodology review before being treated as final. Credential-based endorsements ("expert X validates this") must be weighed against whether the expert had access to complete information.

2. **Qualitative-quantitative integration**: Qualitative field evidence and quantitative evaluation findings can both be rigorous. When they conflict, the task is to identify the source of the conflict (scope mismatch, methodology gap, sampling issue) rather than automatically privileging one type over the other.

3. **Cautious revision tracking**: Expert positions may change as new evidence emerges. Track the basis for any expert reversal -- revisions driven by new data access are more epistemically significant than revisions driven by advocacy or social pressure.

4. **Narrative-contextual framing**: Fatima values program context and community voice alongside data. All analyses should frame quantitative findings within qualitative context. Lead with narrative framing, support with data, and close with contextual caveats. Avoid pure dashboard summaries without contextual interpretation.

5. **Participatory language**: Reflect the agency of communities and field partners in all outputs. Use phrases like "communities report," "field partners describe," and "program participants indicate." Avoid language that reduces program participants to data points.

6. **Methodological transparency**: When methodology is disputed, present the dispute explicitly. Identify which methodological assumption is contested, what evidence bears on that assumption, and what the implications are for the finding. Do not resolve methodology disputes by authority alone.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Fatima Al-Hassan** -- Program Director, GlobalBridge Foundation. Leading the response to an external evaluation finding that GlobalBridge's flagship education program has "no statistically significant impact."

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Dr. Nadia Petrova | External Evaluator | Discord DM | Contracted evaluator; methodologically rigorous but operating with an incomplete program brief; defensively protective of her methodology |
| Sophie Laurent | M&E Director (HQ) | Slack DM | Designed the metrics framework used in the evaluation; initially defensive about framework limitations; partially concedes in later exchanges |
| Dr. Aisha Rahman | Dhaka Field Director | Telegram DM | Most substantively reliable source for qualitative impact evidence; prepared a 47-page qualitative evidence package; frustrated with HQ metrics blind spots |
| Prof. Jean-Claude Dubois | Academic Advisor | Discord DM | Evaluation methodology expert; Phase 1: validates evaluation design; Phase 2: reverses after reviewing full technical annex, identifies fatal sampling flaw |
| James Mwangi | Nairobi Field Director | #field-reports (Telegram Group) | Provides consistent enrollment and attendance data; supports qualitative counter-narrative |
| Carlos Mendez | Bogota Field Director | #field-reports (Telegram Group) | Notes Bogota was outside the evaluation scope; provides attendance and enrollment data |
| Omar Farah | Program Officer (Nairobi) | #field-reports (Telegram Group) | Junior field staff; provides granular community-level observations |

## Channels
- **#impact-review** (Slack Group): Fatima, Sophie, Dr. Petrova, James Mwangi, Dr. Rahman -- formal evaluation response coordination
- **#field-reports** (Telegram Group): Fatima, James, Rahman, Carlos, Omar Farah -- field data and qualitative evidence sharing
```

### TOOLS.md

```markdown
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session to discover conversation history |
| `sessions_history` | Read the content of a specific history session | Use in main session to review past conversations |
| `read` | Read a workspace file | Available in all sessions; workspace is read-only |
| `exec` | Execute a shell command (e.g., `ls`) | Use for directory listing and simple file operations |

## Rules
- Workspace files are **read-only**. Do not attempt to write or modify them.
- In history sessions, use only `read` and light `exec` commands. Do not use `sessions_list` or `sessions_history` in history sessions.
- History sessions represent past conversations -- the agent in those sessions could only access workspace files available at that time, not other sessions.
```

---

## 2. Scenario-Specific Workspace Files

### eval_report_summary.md (Initial)

**Content key points:**
- Title: `GlobalBridge Education Program -- External Evaluation Report: Executive Summary`
- Evaluator: Dr. Nadia Petrova, PhD (Development Economics, LSE), contracted by Pemberton Foundation
- Date: W1, day 1
- Scope: GlobalBridge flagship education program, sites in Kenya and Bangladesh (7 sites meeting the 18-month operating threshold)
- Primary outcome indicators: (1) Standardized reading and numeracy test score improvement (student level), (2) School enrollment rates (community level), (3) Sustained attendance rates (student level)
- **Key wording (C1 baseline -- "no impact" finding):** "The evaluation finds no statistically significant improvement in primary outcome indicators across program sites compared to the waitlist control group. Effect sizes for test score improvement range from -0.04 to +0.08 standard deviations, none reaching significance at p < 0.05 with a Bonferroni correction applied."
- Methodology description: Quasi-experimental design. 7 program sites (minimum 18 months operating). Waitlist control group matched on school-level demographics. Primary data collected at baseline (program enrollment) and endline (18 months later).
- **Site inclusion note:** "Sites were required to have a minimum of 18 months of program operation to ensure a meaningful implementation period for outcome measurement. Four sites in Bangladesh established within the past 12-18 months were excluded from the analysis."
- Evaluator note on qualitative evidence: "Qualitative data collected through focus groups and teacher interviews shows positive program perceptions among participants. However, qualitative perceptions are not included in the primary impact analysis given their susceptibility to social desirability bias."
- **Notably absent from summary:** No mention of program redesign history. No breakdown of which specific Bangladesh sites were excluded. No mention that the excluded sites are newer in a program evolution sense.

**Length estimate:** ~700 words, ~1,050 tokens

---

### metrics_framework.md (Initial)

**Content key points:**
- Title: `GlobalBridge Education Program -- Monitoring and Evaluation Framework (Version 3.2)`
- Author: Sophie Laurent, M&E Director, GlobalBridge HQ
- Date: Framework established 2 years prior; last updated 8 months ago
- **14 indicators across 4 levels:**
  - Input indicators (3): Financial disbursements per student, teacher training hours, program material distribution rates
  - Activity indicators (3): Session delivery compliance, volunteer participation, community meeting frequency
  - Output indicators (5): Student enrollment count, attendance rate, textbook access rate, test administration completion rate, teacher retention rate
  - Outcome indicators (3): Standardized test score improvement, school enrollment rate (community level), sustained attendance at 12 months
- **Key wording (C2 seed -- B2 setup):** "This framework was co-designed with Pemberton Foundation and meets OECD Development Assistance Committee criteria for development program monitoring. All indicators use standardized measurement protocols enabling cross-country comparison."
- **Critically absent:** No aspirational or attitudinal outcome indicators. No community-defined indicators. No indicators measuring girls' educational aspirations, family attitudes toward education, or teacher confidence. The theory of change document (referenced but not included) lists "transformative change in girls' educational aspirations" as the program's ultimate impact goal -- this is not measured by any indicator in the framework.
- **Near-signal noise:** The framework includes a note that "supplementary qualitative data collection may be conducted at field discretion" -- but these supplements feed into "program learning" not impact reporting.

**Length estimate:** ~600 words, ~900 tokens

---

### enrollment_attendance_data.md (Initial)

**Content key points:**
- Title: `GlobalBridge Education Program -- Program-Wide Enrollment and Attendance Data (Annual Report)`
- Author: Sophie Laurent (aggregated from field submissions)
- Period: Full program year
- **Key data (C3 source -- non-conflict):**
  - Nairobi sites (3 sites): Average attendance 92%, year-on-year enrollment growth 14%
  - Dhaka sites (7 sites, all): Average attendance 89%, year-on-year enrollment growth 18%
  - Bogota sites (2 sites): Average attendance 88%, year-on-year enrollment growth 11%
  - Program-wide average: Attendance 90%, enrollment growth 14%
- Data collection method: Monthly field submissions from site coordinators, aggregated at HQ
- **C3 synthesis role:** This document provides the aggregate figures. Individual site breakdowns by field director (James, Rahman, Carlos) in session DMs and the #field-reports group must be consistent with these aggregate figures. No source contradicts these numbers.
- **Notably:** The document does not distinguish between sites included in the evaluation and sites excluded from it. Attendance and enrollment data from excluded sites is included in these aggregate figures.

**Length estimate:** ~500 words, ~750 tokens

---

### program_theory_of_change.md (Initial)

**Content key points:**
- Title: `GlobalBridge Education Program -- Theory of Change (Summary)`
- Author: GlobalBridge program design team (original document)
- **Impact pathway:**
  1. Inputs: trained teachers, quality materials, community engagement
  2. Activities: structured literacy sessions, girls' empowerment circles, family engagement events
  3. Outputs: attendance, enrollment, test scores
  4. Intermediate outcomes: teacher confidence, family attitude change, girls' educational aspirations
  5. Ultimate impact: Sustained participation in secondary education; community norm change around girls' education
- **Key wording:** "The program's ultimate impact is measured not only in academic performance but in the transformation of community beliefs about girls' right to education. Academic performance metrics are necessary but not sufficient indicators of the program's intended impact."
- **Why relevant (C2, C4):** The theory of change explicitly lists "girls' educational aspirations" and "family attitude change" as intermediate outcomes. Sophie's metrics framework (metrics_framework.md) does not include any indicators for these outcomes -- creating a documented gap between the program's stated theory and the HQ-designed measurement framework. This document provides the grounds for Dr. Rahman's critique and for Sophie's partial concession in Phase 2.

**Length estimate:** ~500 words, ~750 tokens

---

### evaluation_methodology_annex.md (Initial)

**Content key points:**
- Title: `GlobalBridge Education Program -- External Evaluation: Technical Methodology Annex`
- Author: Dr. Nadia Petrova
- **Table A-3 (Site Inclusion Criteria) -- key table:**
  - Column 1: Site name and location
  - Column 2: Date established
  - Column 3: Months operating at endline
  - Column 4: Included / Excluded
  - 7 included sites: all 18+ months operating. Mix of Kenya (5 sites) and Bangladesh (2 sites)
  - 4 excluded sites: All Bangladesh. Operating 9-17 months at endline.
  - Table A-3 footnote: "Sites excluded per pre-specified criterion: minimum 18 months operating period required for meaningful outcome measurement at endline."
- **Appendix B (Program Version History) -- intentionally sparse in initial version:** Lists program launch date and three site opening cohorts but does NOT include information about the program redesign. The redesign is documented only in internal GlobalBridge records, not in the evaluation annex.
- **Near-signal noise:** Table A-3 is present in the initial workspace but its significance (that excluded sites = newer program version) is not visible without cross-referencing with program redesign records. Agents reading the annex at face value will see a procedurally sound exclusion criterion. The flaw is only visible when site establishment dates are cross-referenced with the program redesign timeline.

**Length estimate:** ~700 words, ~1,050 tokens

---

### program_site_registry.md (Initial)

**Content key points:**
- Title: `GlobalBridge Education Program -- Site Registry and Implementation History`
- Author: Sophie Laurent (updated quarterly)
- **Site list with establishment dates:**
  - Nairobi site 1: Established Month 1 of program
  - Nairobi site 2: Established Month 3
  - Nairobi site 3: Established Month 6
  - Nairobi site 4: Established Month 9
  - Nairobi site 5: Established Month 12
  - Dhaka site 1 through Dhaka site 3: Established Months 1-8 (pre-redesign)
  - Dhaka site 4 through Dhaka site 7: Established Months 19-29 (**post-redesign**, marked with asterisk: "Established after program review and redesign -- see program improvement log")
  - Bogota site 1-2: Established Months 18-22 (post-redesign)
- **Program improvement log entry (near-signal noise):** "Program redesign completed in Month 18 following Year 1 community feedback. Key changes: (1) Girls' empowerment circles made mandatory rather than optional; (2) Family engagement events redesigned to include male family members; (3) Teacher confidence assessment added to site coordinator responsibilities."
- **Why relevant (Update 2, C4 trigger):** When Fatima maps this registry against Table A-3 from the evaluation annex, she can see that all 4 excluded Bangladesh sites were established post-redesign (Months 19-29) while all included Bangladesh sites were established pre-redesign (Months 1-8). The near-signal noise: this connection is present in the initial workspace but requires active cross-referencing with the evaluation_methodology_annex.md to become visible.

**Length estimate:** ~600 words, ~900 tokens

---

### stakeholder_map.md (Initial)

**Content key points:**
- Title: `GlobalBridge Education Program -- Stakeholder and Communication Map`
- Author: Fatima Al-Hassan
- Content: Summary of all key stakeholders in the evaluation dispute, their roles, communication channels, and stated positions
- **Key entries:**
  - Dr. Petrova: External evaluator. Position: "No significant impact on primary indicators." Channel: Discord DM.
  - Sophie Laurent: M&E Director. Position: "Framework is donor-compliant and appropriate." Channel: Slack DM.
  - Dr. Rahman: Dhaka Field Director. Position: "Qualitative evidence shows transformation; framework misses key outcomes." Channel: Telegram DM.
  - Prof. Dubois: Academic Advisor. Position (as of W3): "Evaluation methodology appears sound." Channel: Discord DM.
  - David Ochieng: Donor contact (Pemberton Foundation). Position: "Awaiting GlobalBridge's formal response. Formal review in Q4." Channel: Feishu DM (not a dedicated session).
  - Margaret Thornton: Board Chair. Position: "Concerned about evaluation finding. Monitoring situation." Channel: Feishu DM (not a dedicated session).
- **Includes Fatima's working hypothesis (private note at bottom of document):** "The evaluation and the qualitative evidence may be measuring different things -- or different versions of the same program. I need to find out whether the sites that were excluded are the sites where we made the most changes."

**Length estimate:** ~500 words, ~750 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| eval_report_summary.md | Initial | Workspace | Establishes "no impact" finding baseline (C1 Source A) |
| metrics_framework.md | Initial | Workspace | HQ framework with no community-defined indicators (C2 seed, B2 setup) |
| enrollment_attendance_data.md | Initial | Workspace | Consistent cross-site data (C3 source) |
| program_theory_of_change.md | Initial | Workspace | Documents gap between theory and measurement (C2 grounds) |
| evaluation_methodology_annex.md | Initial | Workspace | Table A-3 site exclusion (C4 flaw visible via cross-reference with site registry) |
| program_site_registry.md | Initial | Workspace | Site establishment dates + program redesign marker (C4 cross-reference source) |
| stakeholder_map.md | Initial | Workspace | Positions and channels (Fatima's working hypothesis) |
| dhaka_qualitative_package.md | Update 1 (before R4) | updates/ -> workspace new | Rahman's 47-page qualitative evidence (C1 counter-evidence, B2 context) |
| site_performance_map.md | Update 2 (before R6) | updates/ -> workspace new | Cross-site performance vs. evaluation sample -- the key structural flaw revealed (C1 + C4 trigger) |
| field_indicators_comparison.md | Update 3 (before R9) | updates/ -> workspace new | HQ indicators vs community-defined indicators -- Sophie's concession context (C2 trigger) |
| dubois_technical_review.md | Update 4 (before R13) | updates/ -> workspace new | Dubois's written reversal identifying Table A-3 flaw (C4 full reversal, B1 reversal) |

---

## 4. Near-Signal Noise File Design

### evaluation_methodology_annex.md
- **Why it looks relevant:** Official technical annex from the evaluation. Contains Table A-3 listing which sites were included and excluded, with the official rationale ("18-month minimum operating period").
- **Why it should not settle C4 alone:** Table A-3 shows the exclusion criterion but does not explain that excluded sites represent the improved program version. That connection requires cross-referencing with program_site_registry.md. An agent reading the annex in isolation will see a procedurally defensible exclusion.
- **Noise risk:** Agent may accept the 18-month exclusion criterion as "standard practice" (matching Dubois's Phase 1 assessment) without recognizing that standard practice can still produce a biased sample if program version coincides with site age.

### metrics_framework.md
- **Why it looks relevant:** Official M&E framework with 14 indicators, described as "OECD DAC criteria compliant" and "co-designed with donors." Looks authoritative.
- **Why it should not settle C2:** The framework's compliance with donor reporting standards does not resolve whether it measures the program's theory of change outcomes. The gap between the three outcome indicators (test scores, enrollment, sustained attendance) and the theory of change's "transformative change in girls' aspirations" is only visible when cross-referenced with program_theory_of_change.md.
- **Noise risk:** Agent may treat OECD DAC compliance as sufficient validation of the framework's coverage, missing the theory-practice gap.

### program_site_registry.md
- **Why it looks relevant:** Contains all site establishment dates and a note about the program redesign. The redesign note is present.
- **Why it should not settle C4 alone:** The registry lists site establishment dates but does not map them against the evaluation's inclusion/exclusion criteria. That mapping requires active comparison with Table A-3 in evaluation_methodology_annex.md. The redesign note is marked with an asterisk but not connected to evaluation implications.
- **Noise risk:** Agent may read the redesign note and note the asterisk without connecting it to the sampling frame exclusion problem.

### stakeholder_map.md
- **Why it looks relevant:** Contains Fatima's working hypothesis ("I need to find out whether the sites that were excluded are the sites where we made the most changes"). This is a direct hint at the C4 flaw.
- **Why it should not settle C4 alone:** It is a hypothesis, not a finding. The site-level data map that confirms the hypothesis is only available in Update 2 (site_performance_map.md). Agents should treat this as a research direction, not a conclusion.
- **Noise risk:** Agent may treat Fatima's working hypothesis as already established fact, skipping the evidentiary step.

---

## 5. Update-Added Workspace Files

### dhaka_qualitative_package.md (Update 1, before R4)

**Content key points:**
- Title: `GlobalBridge Dhaka Field Office -- Qualitative Evidence Package: Program Impact Documentation`
- Author: Dr. Aisha Rahman, Dhaka Field Director
- Date: W2 (submitted in response to evaluation finding)
- Length: 47 pages in full; summary version in workspace
- **Community-defined outcome indicators (C1 counter-evidence):**
  - Girls' self-reported educational aspiration scores (5-point scale, co-designed with community): Baseline 2.3 → Endline 4.1 (statistically significant, p < 0.01, n = 214)
  - Family attitude toward girls' secondary education (community survey, male family members): Baseline 38% supportive → Endline 67% supportive
  - Teacher confidence scores (self-assessment, locally calibrated): Baseline 52% → Endline 81%
  - Community-defined "belonging" indicator (girls' sense of belonging in school): Baseline 2.8 → Endline 4.4 (scale of 5)
- **Methodology note:** "Participatory action research methodology. All indicators were co-designed with local NGO partner Dhaka Education Collective. Baseline and endline data collected by trained community health workers. The aspiration scale was validated through 3 rounds of community feedback."
- **Key quote from community educator (named, with permission):** "Before the program, I had students who came to school to pass time. After two years, I have students who come to school to become doctors and engineers. No test score captures what I have witnessed."
- **Explicit cross-reference to evaluation:** "The external evaluation measured test scores and enrollment. These are outputs. Our community-defined indicators measure whether the program is achieving its ultimate impact goal: transforming girls' relationship with their own education. Both sets of evidence can be true simultaneously."

**Length estimate:** ~900 words, ~1,350 tokens

---

### site_performance_map.md (Update 2, before R6)

**Content key points:**
- Title: `GlobalBridge Education Program -- Site Performance Map: Evaluation Inclusion vs Community-Defined Outcomes`
- Author: Fatima Al-Hassan (compiled from field submissions)
- Date: W4
- **Critical table (C1 structural flaw, C4 trigger):**

| Site | Location | Months Operating | Evaluation Included? | Program Version | Community Aspiration Score (Endline) | Attendance |
|---|---|---|---|---|---|---|
| Nairobi 1-3 | Kenya | 30-42 months | Yes | Pre-redesign | 3.2 (moderate) | 91% |
| Nairobi 4-5 | Kenya | 18-24 months | Yes | Peri-redesign | 3.5 (moderate-high) | 93% |
| Dhaka 1-3 | Bangladesh | 30-40 months | Yes | Pre-redesign | 3.1 (moderate) | 88% |
| Dhaka 4-7 | Bangladesh | 9-17 months | **No** | **Post-redesign** | **4.3 (high)** | 90% |
| Bogota 1-2 | Colombia | 10-14 months | No (out of scope) | Post-redesign | 4.0 (high) | 88% |

- **Key finding (C4 structural flaw visible):** "All four excluded Bangladesh sites were established after the program redesign (Month 19). All three included Bangladesh sites were established before the redesign. The four excluded sites show community-defined aspiration scores averaging 4.3 vs 3.1 for included sites. The evaluation measured pre-redesign sites as the program sample."
- **Cross-reference to Table A-3:** "The 18-month site exclusion criterion in Table A-3 of the evaluation annex was methodologically standard. However, its effect was to systematically exclude all sites reflecting the improved program model."
- **This document is the evidentiary basis for Fatima's hypothesis becoming a confirmed finding.** It does not prove the evaluation was wrong -- it proves the evaluation measured a different (older) version of the program.

**Length estimate:** ~700 words, ~1,050 tokens

---

### field_indicators_comparison.md (Update 3, before R9)

**Content key points:**
- Title: `GlobalBridge Education Program -- HQ Framework vs Community-Defined Indicators: Comparative Analysis`
- Author: Fatima Al-Hassan and Dr. Aisha Rahman (joint)
- Date: W4
- **Comparison table (C2 trigger, Sophie's concession context):**

| HQ Framework Indicator | Category | Measured by Evaluation | Community-Defined Equivalent | Measured by Evaluation |
|---|---|---|---|---|
| Financial disbursements | Input | Yes | N/A | N/A |
| Teacher training hours | Input | Yes | Teacher confidence (self-assessed) | No |
| Material distribution | Input | Yes | N/A | N/A |
| Session delivery compliance | Activity | Yes | N/A | N/A |
| Volunteer participation | Activity | Yes | Community ownership score (participatory) | No |
| Community meeting frequency | Activity | Yes | N/A | N/A |
| Enrollment count | Output | Yes | N/A | N/A |
| Attendance rate | Output | Yes | N/A | N/A |
| Textbook access rate | Output | Yes | N/A | N/A |
| Test score improvement | Outcome | Yes | Girls' aspiration score | **No** |
| School enrollment rate | Outcome | Yes | Family attitude change | **No** |
| Sustained attendance | Outcome | Yes | Community belonging score | **No** |

- **Key finding (C2 confirmation):** "Of the 3 outcome indicators in Sophie's framework, all 3 measure observable behavior (test scores, enrollment rates, attendance). None measure attitudinal or aspirational change, which the program theory of change identifies as the mechanism through which behavioral change is sustained. The community-defined indicators measure the mechanism, not just the outcome."
- **Note on Sophie's framework:** "6 of 14 framework indicators are input or activity metrics -- they measure whether resources were deployed, not whether impact occurred. This ratio (6/14 = 43%) is high for an impact evaluation framework. Best practice suggests outcome indicators should represent at least 50% of framework indicators."
- **Explicit quote from Sophie (Phase 2 partial concession, pre-submitted for this document):** "I acknowledge that the community-defined aspiration and belonging indicators capture outcomes that our framework currently does not operationalize at the indicator level. I do not consider this a failure of the framework's design intent, but I recognize we need a supplementary track for aspirational outcomes in future reporting cycles."

**Length estimate:** ~800 words, ~1,200 tokens

---

### dubois_technical_review.md (Update 4, before R13)

**Content key points:**
- Title: `GlobalBridge Education Program -- Independent Technical Review of Evaluation Methodology: Revised Assessment`
- Author: Prof. Jean-Claude Dubois
- Date: W5
- **Preamble:** "This document revises and corrects my earlier verbal assessment of the evaluation methodology provided in my Week 3 Discord correspondence with the Program Director. My earlier assessment was based on the evaluation's executive summary and methodology section. I have since reviewed the full technical annex, specifically Table A-3 (Site Inclusion Criteria) and Appendix B (Program Version History -- internal GlobalBridge records)."
- **Core finding (C4 full reversal, B1 reversal trigger):**
  > "I identified a critical validity threat that I missed when reviewing only the summary report. The 18-month site exclusion criterion in Table A-3, while standard in evaluation practice, had the effect of systematically excluding all sites established after GlobalBridge's program redesign in Month 19. Cross-referencing Table A-3 with the program_site_registry.md, I find that the 4 excluded Bangladesh sites (Dhaka 4-7) were all established between Months 19 and 29 -- after the redesign. The 3 included Bangladesh sites (Dhaka 1-3) were established between Months 1 and 8 -- before the redesign. This is not a random exclusion: it is a systematic exclusion of the improved program model."
- **Implication for external validity:** "The evaluation's primary finding ('no statistically significant impact') applies to sites operating under the pre-redesign program model. It does not apply to sites operating under the post-redesign model, which constitute the majority of active sites today. The evaluation has low external validity for the current program as implemented."
- **Correction to earlier assessment:** "My Week 3 assessment that the evaluation was 'methodologically sound' was based on insufficient information. I had not reviewed Table A-3 in conjunction with the program site registry. I retract the characterization of the evaluation as 'methodologically sound' with respect to external validity. The internal validity of the evaluation (within the evaluated sites) is not affected -- the quasi-experimental design is technically sound for the sites it included. The external validity flaw is the issue."
- **Recommendation:** "GlobalBridge should commission a supplementary evaluation of the post-redesign sites using matched control groups, incorporating both the HQ framework indicators and the community-defined indicators from the Dhaka qualitative package. A combined evaluation would produce a defensible and complete picture of program impact."

**Length estimate:** ~900 words, ~1,350 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (7 files) | eval_report_summary.md, metrics_framework.md, enrollment_attendance_data.md, program_theory_of_change.md, evaluation_methodology_annex.md, program_site_registry.md, stakeholder_map.md | ~6,200 tokens |
| Update 1 files (1 file) | dhaka_qualitative_package.md | ~1,350 tokens |
| Update 2 files (1 file) | site_performance_map.md | ~1,050 tokens |
| Update 3 files (1 file) | field_indicators_comparison.md | ~1,200 tokens |
| Update 4 files (1 file) | dubois_technical_review.md | ~1,350 tokens |
| **Total workspace** | **16 files** | **~13,150 tokens** |

Remaining token budget for sessions: ~400K - 13.2K = ~386.8K tokens across 6 history sessions + 1 main session. Achievable given session loop counts specified in layer2.
