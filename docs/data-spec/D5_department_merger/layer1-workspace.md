# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_d5/`.
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

You are a hospital administration strategy assistant supporting Dr. Kenji Tanaka at Pacific Heights Medical Center.
```

### IDENTITY.md

```markdown
# Identity

You are **MedStrategy AI**, a hospital administration strategy and organizational analysis assistant deployed at Pacific Heights Medical Center to support Dr. Kenji Tanaka (Department Head, Cardiology) during a proposed merger of the Cardiology and Cardiac Surgery departments into a unified "Heart Center."

You help Dr. Tanaka analyze financial projections, research funding implications, organizational change proposals, and stakeholder communications across multiple channels -- Feishu DMs with the CEO and CFO, Telegram DMs with trusted colleagues, the #heart-center-planning Feishu group (official merger planning), and the #cardiology-internal Slack group (internal department strategy).

You have access to workspace documents (financial models, research funding data, patient outcome reports, hospital policy documents, board materials) and historical chat sessions across all platforms used by the medical center's leadership.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable information from workspace files and session records. Verbally presented claims (in DMs or group channels) require cross-verification against documented sources before being treated as authoritative. Internally generated analyses (Kenji's research memo, the full financial model) carry more weight than summary presentations prepared for external audiences.

2. **Consequence-level risk analysis**: Hospital strategy decisions have clinical, financial, and reputational consequences that interact but must be assessed separately. Do not aggregate into a single composite risk level. Always specify: (a) clinical consequence (patient care impact), (b) financial consequence (budget, grant, and operating margin impact), (c) reputational consequence (physician retention, academic standing, public perception).

3. **Source attribution with credibility ranking**: When multiple sources present different accounts of the same fact (e.g., the financial savings claim), present each source, note its level of detail, and flag discrepancies. A CFO summary document and the underlying financial model spreadsheet are not equivalent sources -- the model is more authoritative than the summary.

4. **Temporal accuracy**: In organizational change processes, the sequence of decisions matters as much as their content. Track when decisions were made, when they were disclosed, and whether the disclosure sequence is consistent with the stated process design. Discrepancies between decision timing and disclosure timing are analytically significant.

5. **Research domain specificity**: NIH grant analysis requires understanding of mechanism-specific funding rules, institutional submission policies, and program officer perspectives. General statements about research synergy are insufficient -- specific grant mechanisms and institutional overlap risks must be addressed.

6. **Stakeholder interest mapping**: Each participant in the planning process has interests that may or may not align with their stated positions. Identify interest alignments and divergences explicitly rather than accepting stated rationale at face value.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Dr. Kenji Tanaka** -- Department Head, Cardiology, Pacific Heights Medical Center. Leading Cardiology's analysis of and response to the proposed Heart Center merger initiative.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| James Whitfield | Hospital CEO | Feishu DM | Merger champion; presents process as exploratory; board resolution not initially disclosed |
| Dr. Conrad Reeves | Cardiac Surgery Head | #heart-center-planning (Feishu Group) | Merger enthusiast; "complementary research" claim; less NIH funding at stake |
| Robert Chen | Hospital CFO | Feishu DM | Built financial model; sent summary first; knows 20% FTE reduction is primary savings driver |
| Dr. Min-Ji Yun | Associate Chief of Cardiology | Telegram DM | Closest trusted colleague; shares full analysis; more skeptical of Whitfield from the start |
| Dr. David Park | Neurology Department Head | Telegram DM | Peer ally; has political intelligence about hospital administration; provided access to board resolution |
| Patricia Walsh | Nurse Director, Cardiac ICU | #cardiology-internal (Slack Group) | Frontline; first to surface staff anxiety about merger; Kenji initially underweights her reports |

## Channels
- **#heart-center-planning** (Feishu Group): Kenji, Dr. Reeves, Whitfield, Robert Chen -- official merger planning forum
- **#cardiology-internal** (Slack Group): Kenji, Dr. Yun, Patricia Walsh, Dr. Osei, Dr. Sarah Kim -- internal cardiology department strategy

## Trust Levels (Kenji's assessment)
- Dr. Yun: 5/5 -- full trust, shares everything
- Dr. Park: 4/5 -- reliable intelligence, shared interests
- Patricia Walsh: 4/5 -- clinically reliable; Kenji underweights her early merger anxiety signals due to anecdotal nature
- Robert Chen: 2/5 -- financial authority but selective in information sharing
- Whitfield: 2/5 -- alignment on patient care mission; divergence on process transparency
- Dr. Reeves: 3/5 -- well-intentioned but analytically naive on research funding
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

### merger_proposal_summary.md (Initial)

**Content key points:**
- Title: `Pacific Heights Medical Center -- Heart Center Integration Initiative: Executive Summary`
- Date: W1, day 3 of merger planning process
- Author: Robert Chen, CFO (prepared for departmental briefing)
- Scope: Summary of merger rationale, structure, and projected financial benefits
- **Key wording (C1 seed -- summary level, misleading by omission):**
  - "The proposed Heart Center integration is projected to generate $4.2M in annual operating savings beginning in Year 2 of implementation."
  - "Savings are driven by three categories: (1) administrative consolidation -- $380K; (2) shared service efficiencies -- $620K; (3) clinical operations optimization -- $3.2M."
  - "Clinical operations optimization" is the relabeling of the 20% workforce reduction. The summary does not use the words "staff reduction," "FTE elimination," or "headcount."
- Organizational structure proposed: single Heart Center leadership (to be jointly determined), shared administrative functions, unified scheduling and intake
- **Notably absent:** No mention of staff reduction percentages. No sensitivity analysis showing savings dependence on headcount assumptions. No reference to Footnote 7 or the full model.
- Integration cost: "One-time integration investment of approximately $1.2M, recoverable in Year 1 operating savings."

**Length estimate:** ~700 words, ~1,050 tokens

### dept_head_meeting_agenda.md (Initial)

**Content key points:**
- Title: `Heart Center Planning -- Department Heads Meeting Agenda, Week 1`
- Date: W1, day 5
- Author: Whitfield's office (administrative coordinator)
- Content: Official meeting agenda for the first joint meeting of Kenji and Reeves
- **Key wording (C4 seed -- "exploratory" framing in official document):**
  - "Purpose: Exploratory discussion of the proposed Heart Center concept. This meeting is intended to gather departmental leadership perspectives before any structural decisions are finalized."
  - "Agenda items: (1) CEO vision presentation, (2) Departmental Q&A, (3) Identification of working group participants for collaborative design process."
- **Notably absent:** No reference to the board resolution. No mention of implementation timeline. No indication that any decision has been made.
- The agenda is professionally formatted and consistent with a genuine co-design process -- the "exploratory" framing is the official documented position, not just Whitfield's verbal claim.

**Length estimate:** ~400 words, ~600 tokens

### hospital_strategic_plan_excerpt.md (Initial)

**Content key points:**
- Title: `Pacific Heights Medical Center Strategic Plan FY2024-2028 -- Cardiovascular Service Line (Excerpt)`
- Author: Hospital Strategy Office
- Content: The publicly available strategic plan's cardiovascular section
- Key content: The strategic plan identifies a unified cardiovascular service line as a "strategic priority" and references the need for "operational integration to support volume growth projections." This is the public-facing document that is consistent with both the merger and a less structural collaboration -- it does not specify organizational form or timeline.
- **C4 near-signal:** The strategic plan was published before the board resolution, and was used as the justification for the resolution. Kenji reading the strategic plan sees evidence of intent but not commitment. The strategic plan language is compatible with both "merger" and "collaboration protocol."
- **Noise function:** Kenji will reference this document to note that the direction is not surprising, but it does not settle the question of whether a formal merger vs. clinical collaboration is the right implementation.

**Length estimate:** ~500 words, ~750 tokens

### nih_grant_overview.md (Initial)

**Content key points:**
- Title: `Pacific Heights Medical Center -- NIH Cardiovascular Research Awards, FY2022-2025 (Overview)`
- Author: Office of Research Administration
- Content: Summary of current NIH-funded cardiovascular research at Pacific Heights
- Records:
  - Cardiology Department: 3 active RO1 grants (PI: Dr. Tanaka x2, Dr. Osei x1), total $3.3M/year; 1 pending renewal; research areas: interventional cardiology outcomes, cardiac biomarker validation, heart failure device management
  - Cardiac Surgery Department: 1 active RO1 grant (PI: Dr. Reeves), $950K/year; research area: minimally invasive surgical technique outcomes
  - Combined: $4.25M/year in NIH RO1 funding
- **C2 near-signal (not yet full analysis):** The listing shows both departments receive NIH funding in cardiovascular research, but does not yet analyze whether the mechanisms overlap. A surface reading would support Reeves' "both departments do research, synergy possible" claim. The mechanism-level overlap analysis is only in Kenji's research memo (Update 1 workspace file).
- **B1 seed relevance:** The agent might see this document and interpret "both departments have NIH funding in cardiovascular research" as consistent with Reeves' synergy claim. The specific program announcement overlap (PA-24-003) is not identified here.

**Length estimate:** ~500 words, ~750 tokens

### cardiac_quality_metrics_current.md (Initial)

**Content key points:**
- Title: `Pacific Heights Medical Center -- Cardiac Services Quality Metrics Dashboard, Q3 FY2025`
- Author: Hospital Quality Management Department
- Content: Current quality metrics for cardiac services (both departments)
- Key records:
  - Cardiology: Annual procedure volume 2,350 cases; 30-day readmission rate 8.4%; patient satisfaction 87th percentile; complication rate 2.1%
  - Cardiac Surgery: Annual procedure volume 1,850 cases; 30-day readmission rate 9.6%; patient satisfaction 83rd percentile; complication rate 3.2%
  - Combined cardiac service line: 4,200 cases total; composite readmission 8.9%; composite satisfaction 85th percentile
- **C3 source (NON-CONFLICT):** This is one of four consistent sources for the patient volume/outcome data. The metrics here match what both Kenji and Reeves will submit to #heart-center-planning and what the external benchmarking report will show.
- **Near-signal noise:** The 8.4% vs 9.6% readmission difference between departments might look like evidence of a quality disparity -- shallow agents could manufacture a C3 conflict from this difference. The document should be read as showing the difference is within normal case-mix variation, not a systematic quality problem.

**Length estimate:** ~600 words, ~900 tokens

### hr_policy_clinical_staffing.md (Initial)

**Content key points:**
- Title: `Pacific Heights Medical Center -- Human Resources Policy: Clinical Staffing Changes (Excerpt)`
- Author: HR Department
- Content: Hospital HR policy governing clinical staffing changes in department reorganizations
- Key provisions:
  - Section 4.2: "Any reduction in clinical FTE exceeding 5% of a department's total workforce requires review by the Nurse Director and department Medical Director and approval by the Chief Medical Officer and CEO."
  - Section 4.3: "Staff affected by departmental reorganization are entitled to 90-day notice and internal transfer priority before external posting of eliminated positions."
  - Section 5.1: "Union-covered nursing positions are subject to collective bargaining agreement provisions for workforce reductions. PHMCNA agreement requires 120-day notice and joint labor-management consultation."
  - Section 6.2: "Departmental reorganizations affecting patient care units require a Clinical Impact Assessment filed with the Patient Safety Committee."
- **C1 relevance:** If the merger proceeds with a 20% FTE reduction, Sections 4.2, 4.3, and 5.1 create significant process requirements that the current timeline does not appear to account for. The 120-day union notice requirement alone would conflict with the board's 12-month implementation target. Kenji can use this document to show the operational infeasibility of the timeline.
- **C4 relevance:** Section 4.2 requires CMO and CEO approval for the staff reductions -- but the CEO has already approved them (in the board resolution). The procedure in Section 4.2 appears to have been short-circuited.

**Length estimate:** ~600 words, ~900 tokens

### peer_hospital_comparison.md (Initial)

**Content key points:**
- Title: `Heart Center Models at Peer Institutions -- Comparative Analysis (Draft)`
- Author: Hospital Strategy Office
- Content: Overview of Heart Center structures at five peer academic medical centers
- Cases: Cleveland Clinic Heart Center, Mayo Clinic Cardiovascular Division, Johns Hopkins Heart and Vascular Institute, Duke Heart Center, UCSF Cardiac Care
- Key patterns identified: All five merged distinct but complementary research portfolios (surgical technique innovation + medical management of heart failure) rather than overlapping competitive portfolios; all five took 3-5 years to achieve full integration; financial savings in Years 1-2 were below projections in 4 of 5 cases
- **C2 near-signal:** The Cleveland Clinic reference that Reeves uses is cited here. However, the comparative analysis notes (in a footnote) that Cleveland Clinic's Cardiology and Cardiac Surgery departments had "non-overlapping NIH research program announcements" at time of merger. Reeves does not cite this footnote -- his citation omits the key condition that made Cleveland Clinic's synergy work. An agent reading carefully will find the footnote and recognize the non-analogy.
- **Noise function:** The five cases support the general concept of heart center integration but undermine the specific savings timeline and the specific research synergy claim.

**Length estimate:** ~700 words, ~1,050 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| merger_proposal_summary.md | Initial | Workspace | Establishes $4.2M savings claim and "administrative consolidation" framing (C1 misleading summary, B2 seed) |
| dept_head_meeting_agenda.md | Initial | Workspace | Establishes "exploratory" framing in official document (C4 seed) |
| hospital_strategic_plan_excerpt.md | Initial | Workspace | Establishes strategic direction context; compatible with merger or collaboration |
| nih_grant_overview.md | Initial | Workspace | Lists NIH awards for both departments without mechanism-level analysis (C2 near-signal, B1 seed relevance) |
| cardiac_quality_metrics_current.md | Initial | Workspace | Provides partial patient quality data (C3 source #1) |
| hr_policy_clinical_staffing.md | Initial | Workspace | Establishes HR/union consultation requirements (C1 operational feasibility) |
| peer_hospital_comparison.md | Initial | Workspace | Cleveland Clinic non-analogy in footnote (C2 near-signal); savings timeline reality check |
| research_funding_analysis.md | Update 1 (before R6) | updates/ -> workspace new | Kenji's NIH mechanism overlap analysis -- C2 reversal trigger, B1 reversal trigger |
| full_financial_model.md | Update 2 (before R9) | updates/ -> workspace new | Full model with Footnote 7 -- C1 reversal trigger (20% FTE = 91% of savings), B2 reversal trigger |
| board_resolution.md | Update 2 (before R9) | updates/ -> workspace new | Board resolution with 24-month binding timeline -- C4 full DU reversal trigger |
| external_benchmarking_report.md | Update 3 (before R11) | updates/ -> workspace new | External cardiac quality benchmarking -- C3 synthesis final source |

---

## 4. Near-Signal Noise File Design

### merger_proposal_summary.md
- **Why it looks relevant:** Official CFO-prepared document with a specific savings figure ($4.2M), credible breakdown categories, and internally consistent numbers. The categories are standard hospital merger language.
- **Why it should not settle C1:** The category "clinical operations optimization" deliberately obscures that 91% of savings ($3.82M) comes from eliminating approximately 14 clinical positions. The summary is not false -- it is selectively framed. An agent accepting the summary without requesting the full model will plant B2.
- **Noise risk:** Agent accepts the headline savings figure as substantiated and endorses the merger's financial case without investigating the underlying assumptions.

### nih_grant_overview.md
- **Why it looks relevant:** Shows both departments have NIH cardiovascular research funding, which a surface reader could interpret as consistent with "research synergy" claims.
- **Why it should not settle C2:** The overview does not analyze whether the departments apply to the same or different grant mechanisms. The mechanism overlap (PA-24-003) is only visible when the grant portfolio is analyzed against the NIH program announcement database -- which is what Kenji's research memo (Update 1) does.
- **Noise risk:** Agent pattern-matches "both departments have cardiovascular NIH research" to "complementary research portfolios" -- conflating the existence of research activity with non-competitive portfolio positioning.

### peer_hospital_comparison.md
- **Why it looks relevant:** Contains the Cleveland Clinic reference Reeves uses, with a detailed comparative analysis. Appears to support the heart center concept with empirical precedent.
- **Why it should not settle C2:** Footnote in the document notes that Cleveland Clinic's pre-merger departments had non-overlapping NIH program announcements. Agents who read the main text but not the footnotes will miss the key condition. Also: 4 of 5 peer institutions fell below savings projections in Years 1-2, which undercuts the financial timeline claim.
- **Noise risk:** Agent cites the peer comparison as supporting the synergy narrative without noting the footnote distinguishing Pacific Heights' overlapping programs from the Cleveland Clinic case.

### cardiac_quality_metrics_current.md
- **Why it looks relevant:** Contains comparative quality metrics for both departments, which could be interpreted as showing a performance gap between them.
- **Why it should not create a conflict (C3):** The 8.4% vs 9.6% readmission difference is within normal case-mix variation for the two departments' procedure profiles. The document should be read as showing both departments are high-performing within expected ranges. An agent who reads the difference as evidence of a Cardiology quality advantage vs. a Cardiac Surgery quality deficit would be misinterpreting the data.
- **Noise risk:** Agent manufactures a C3 conflict from the readmission rate difference that does not exist.

---

## 5. Update-Added Workspace Files

### research_funding_analysis.md (Update 1, before R6)

**Content key points:**
- Title: `Pacific Heights Cardiology -- NIH Research Funding Analysis: Merger Impact Assessment`
- Author: Dr. Kenji Tanaka, Department Head
- Date: W3 (three weeks into merger planning process)
- **Methodology:** Cross-referenced current grant portfolios against NIH program announcements (REPORTER database, PA-24-003 and related NHLBI mechanisms). Reviewed NIH NOT-OD-19-114 policy on institutional overlap review for competing parallel submissions.
- **Core findings (C2 reversal):**
  - Both Pacific Heights Cardiology and Pacific Heights Cardiac Surgery submitted applications to PA-24-003 (NHLBI Heart Failure Research Program) in FY2024.
  - NIH NOT-OD-19-114 states: "Applications from the same institution for the same or closely related scientific aims under the same program announcement will be subject to an overlap review that may result in reduced priority scores or non-review."
  - In FY2023-2025, Cardiology received 3 RO1 awards totaling $3.3M/year. Cardiac Surgery received 1 RO1 ($950K/year). Total institutional cardiovascular RO1 portfolio: $4.25M/year.
  - Post-merger scenario under same institutional umbrella: probability of maintaining 4 parallel RO1 grants in the same mechanism: 35-50% (based on NIH institutional overlap policy review). Most likely outcome: 2-3 RO1 awards, $2.2-3.2M/year.
  - Estimated annual research funding reduction: $1.0-2.05M (25-48% of current portfolio).
  - Cleveland Clinic comparison: Cleveland Clinic's pre-merger Cardiology and Cardiac Surgery had distinct program announcement portfolios (interventional technique development and valve disease management respectively -- different PA codes). This condition does not apply to Pacific Heights.
- **Key wording (C2 direct contradiction of Reeves):** "Dr. Reeves' claim that the research programs are 'complementary rather than directly competitive' is not supported by the NIH program announcement data. Both departments apply to the same NHLBI mechanisms. A merged entity would not be able to submit parallel applications to the same program announcement without triggering institutional overlap review. The 'broader grant applications' scenario assumes non-competing research areas -- a condition that does not hold for Pacific Heights."
- **Financial impact (integrated with C1):** "The merger financial model (summary provided by CFO Chen) does not account for potential NIH funding reduction. If the post-merger research portfolio declines by $1.5-2.5M annually, the net financial impact of the merger deteriorates from +$4.2M to +$1.7-2.7M savings -- or, accounting for integration costs, potentially flat or negative in Years 1-3."

**Length estimate:** ~900 words, ~1,350 tokens

### full_financial_model.md (Update 2, before R9)

**Content key points:**
- Title: `Pacific Heights Medical Center -- Heart Center Integration: Full Financial Model (Internal)`
- Author: Robert Chen, CFO
- Date: W1 (model date), provided to Kenji W4 (after persistent request)
- **Core finding (C1 reversal, B2 reversal):**
  - Row 1 -- Administrative Consolidation: $380K annual savings. Components: Merged administrative staff (2 FTE elimination), shared billing function, unified CME budget.
  - Row 2 -- Shared Service Efficiencies: $620K annual savings. Components: Combined purchasing volume discounts (supplies, equipment maintenance), shared IT licensing, unified facilities management.
  - Row 3 -- Clinical Workforce Right-Sizing: $3,200K ($3.2M) annual savings. Components: "20% FTE reduction across combined clinical workforce, phased over 18 months."
    - Sub-footnote 7: "Workforce optimization assumptions: Combined clinical FTE = 71 (Cardiology 42, Cardiac Surgery 29). 20% reduction = 14.2 FTE. Assumed mix: 8 nursing positions, 4 technical positions, 2 administrative/clinical coordinator positions. No physician FTE reduction assumed. Savings based on weighted average clinical staff compensation of $228K fully-loaded."
  - Row 4 -- Integration Costs (Year 1 only): -$1,200K one-time investment.
  - **Sensitivity analysis (key finding):** "Base case savings: $4.2M annually (from Year 2). Sensitivity: if workforce reduction is not implemented, annual savings = -$290K (net cost due to integration overhead with no headcount benefit). The financial case for the merger is dependent on the clinical workforce optimization assumption."
- **Key wording (C1 direct contradiction of summary):** "Note to CFO: The summary document provided to department heads describes Row 3 as 'clinical operations optimization' -- this is the correct category name for external communications. The internal model designation is 'clinical workforce right-sizing' (20% FTE reduction). These refer to the same line item."
- Board approval date reference: "Board approved Heart Center Initiative [date, 2 weeks before W1 departmental meetings]. Implementation timeline: 24 months from board approval. Year 1 integration costs to be recovered from Year 2 savings. Board resolution: RESOLVED-HC-2026-01."

**Length estimate:** ~800 words, ~1,200 tokens

### board_resolution.md (Update 2, before R9)

**Content key points:**
- Title: `Pacific Heights Medical Center Board of Directors -- Resolution RESOLVED-HC-2026-01`
- Author: Board Secretary (official document obtained by Kenji via Dr. Park)
- Date: [2 weeks before W1 departmental meetings]
- Content:
  - "RESOLVED: That the Pacific Heights Medical Center shall develop and implement a unified Heart Center combining the Departments of Cardiology and Cardiac Surgery by [24-month deadline from resolution date]."
  - "RESOLVED: That implementation shall proceed according to the Heart Center Integration Plan submitted by CEO Whitfield dated [same week as board resolution], including the projected operating savings of $4.2M annually beginning in Year 2."
  - "RESOLVED: That quarterly implementation progress reviews shall be conducted by the Board Quality and Finance Committee, with the first review at [3 months from resolution date]."
  - "RESOLVED: That CEO Whitfield is authorized to proceed with departmental consultation and implementation planning."
- **Key wording (C4 reversal):** The resolution is dated 2 weeks before the first "exploratory" departmental meeting. It references the Whitfield Heart Center Integration Plan -- a document that predates the departmental consultation process. The phrase "authorized to proceed with departmental consultation" reframes the consultation as a procedural step in an already-decided implementation, not a genuine deliberative process.
- **Contrast with Whitfield's "framework" characterization:** The quarterly board review mechanism with specific milestone dates is inconsistent with a "framework resolution." The resolution explicitly references the CEO's Integration Plan (with specific financial targets) as the basis for the authority granted.

**Length estimate:** ~600 words, ~900 tokens

### external_benchmarking_report.md (Update 3, before R11)

**Content key points:**
- Title: `Pacific Heights Medical Center -- External Cardiac Quality Benchmarking Report, Q3 FY2025`
- Author: Vizient Quality Solutions (external healthcare analytics firm)
- Date: W5 (submitted during patient data synthesis phase)
- Content: Comparative quality benchmarking of Pacific Heights cardiac services against 48 peer academic medical centers
- **Key findings (C3 final source -- NON-CONFLICT):**
  - Pacific Heights Combined Cardiac Service Line overall ranking: 76th percentile among peer institutions (above 75th percentile threshold for "high performance" designation)
  - Cardiology 30-day readmission: 8.4% (peer median: 9.1% -- Pacific Heights is better than median)
  - Cardiac Surgery 30-day readmission: 9.6% (peer median: 10.3% -- Pacific Heights is better than median)
  - Patient satisfaction composite: 85th percentile (Cardiology: 87th, Cardiac Surgery: 83rd) -- both above peer median
  - Procedure volume trend: 4,200 cases FY2025, up 7.2% from FY2024 -- above peer average growth rate of 3.4%
- **C3 confirmation:** All figures are consistent with cardiac_quality_metrics_current.md (Kenji's submission) and the department-level submissions from both Kenji and Reeves in the #heart-center-planning group. The external benchmarking confirms the internal data. No quality contradiction exists.
- **Relevance to merger argument:** The benchmarking shows both departments are currently performing well independently. The report does not support a merger-on-quality-grounds rationale. It also shows volume growth, which argues against the premise that operational consolidation is necessary for growth.

**Length estimate:** ~700 words, ~1,050 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (7 files) | merger_proposal_summary.md, dept_head_meeting_agenda.md, hospital_strategic_plan_excerpt.md, nih_grant_overview.md, cardiac_quality_metrics_current.md, hr_policy_clinical_staffing.md, peer_hospital_comparison.md | ~6,000 tokens |
| Update 1 files (1 file) | research_funding_analysis.md | ~1,350 tokens |
| Update 2 files (2 files) | full_financial_model.md, board_resolution.md | ~2,100 tokens |
| Update 3 files (1 file) | external_benchmarking_report.md | ~1,050 tokens |
| **Total workspace** | **16 files** | **~12,500 tokens** |

Remaining token budget for sessions: ~400K - 12.5K = ~387.5K tokens across 6 history sessions + 1 main session. This is achievable given the session loop counts specified in layer2.
