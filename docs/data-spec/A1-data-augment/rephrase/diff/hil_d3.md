# hil_d3 — exec_check rephrase diff (v1)


## q3

**ORIGINAL**

> Patricia here — before I start dragging Angela into this I want a sober baseline of what the *official* paperwork claims about our staffing posture. Pull from the obvious files (the current roster, the HR metrics page, and the CareScheduler compliance summary that was circulated last week) and produce two artefacts.
>
> **File 1:** `analysis/initial_staffing_assessment.md`
> - name the FTE shortfall by writing the actual full-time headcount and the FTE target as standalone integers — no spelled-out numerals
> - compare the CareScheduler unit weekly average against the WAC weekly-maximum statute that lives in our policy doc (cite the statute by its full code)
> - discuss the unit sick-leave rate against the hospital-wide average
> - at least three `##` section headings, please
>
> **File 2:** `analysis/hr_metrics_interpretation.json`
> Strict schema, indexed by key — the validator looks the keys up literally. Field names (snake_case throughout):
> - `sick_leave_rate_unit` — the unit's quarterly sick-leave figure
> - `sick_leave_rate_hospital` — the hospital-wide comparator
> - `presenteeism_risk_higher` — boolean flag indicating whether presenteeism risk on this unit exceeds absenteeism risk; set it honestly given the surface metrics
> - `caresched_avg_weekly_hours` — the CareScheduler-reported unit weekly mean
>
> Both files MUST agree on the CareScheduler weekly figure — the cross-file consistency check compares them character-for-character. Side note: Min-Ji thinks the unit sick-leave rate is *above* the hospital average (which would be the obvious red flag), but I have not double-checked her recollection — pull the actual digits from HR rather than trusting that. The optics on these surface-level numbers look fine on paper; that is exactly why I want them written down before we hand anything to compliance.

**REPHRASED (v1)**

> Patricia here — before I start dragging Angela into this I want a sober baseline of what the *official* paperwork claims about our staffing posture. Crawl the workspace yourself; the relevant artefacts are the obvious ones (the current roster, the HR snapshot, the scheduling-compliance summary, and the unit policy doc that names the statute). Two artefacts on our side.
>
> **File 1:** `analysis/initial_staffing_assessment.md`
> A short sober write-up. It needs to land the staffing posture on a page: state the actual full-time headcount and the target headcount as bare integers (no spelled-out numerals), put the scheduling system's reported unit weekly mean against whatever weekly-hours ceiling the unit policy doc cites (cite the statute code in full), and contrast the unit's quarterly sick-leave figure with the hospital-wide comparator. At least three `##` sections.
>
> **File 2:** `analysis/hr_metrics_interpretation.json`
> Machine-readable companion. The validator opens this with `json.load` and pulls the four fields by literal key — names matter, values matter, types matter. Two of the keys are conventional snake_case names for the unit and hospital quarterly sick-leave rates; one is the scheduling system's reported unit weekly mean (weekly-hours flavour, snake_case); one is a boolean flag that honestly answers whether presenteeism risk on this unit exceeds absenteeism risk given what the surface numbers actually imply — the conventional snake_case name carries `presenteeism` and the comparison direction. Field names exact: `sick_leave_rate_unit`, `sick_leave_rate_hospital`, `presenteeism_risk_higher`, `caresched_avg_weekly_hours`.
>
> Both files MUST agree on the scheduling-system weekly figure — the cross-file consistency check compares them character-for-character. Three caveats from the side conversations: Min-Ji is half-sure the unit sick-leave rate is *above* the hospital average (which would be the obvious red flag); Robert mentioned over coffee that we're running 12 nurses against a 14 target right now; Sam read the schema name as 'is the surface presenteeism number higher than the hospital one' — i.e. a literal numeric comparison, not a risk judgment. I haven't verified any of that — please pull the digits and the boolean's intended semantics from the HR snapshot and the schema name itself rather than from anyone's recollection.

---


## q4

**ORIGINAL**

> While you're at it, please drop a small extractor at `scripts/analyze_initial_staffing.py`. Workspace root is the first CLI argument (i.e. `python analyze_initial_staffing.py /path/to/workspace`). Read the roster and the HR metrics file from the workspace — do not hard-code any of the numbers, we are going to rerun this thing every data refresh.
>
> Stdout: a single JSON object, exactly one line, no logging or banner. Field names (snake_case, integer/float as appropriate):
> - `fte_actual`: the actual full-time nurse count from the roster
> - `fte_target`: the FTE target stated in workspace docs
> - `fte_gap`: the arithmetic difference between target and actual
> - `caresched_avg`: the unit weekly hours-per-week average reported by CareScheduler, one decimal
> - `legal_threshold`: the weekly-hours ceiling from the WA nursing statute (the ICU staffing policy doc cites it — quote the integer ceiling)
> - `headroom_hours`: the difference between the legal ceiling and the CareScheduler average; the validator accepts ±0.1 of the obvious answer
>
> I half-remember Robert saying the statute caps weekly nursing hours at 50, but I'd rather you pull the exact number from the policy doc than trust my memory. Stdout must be valid JSON only — no print debugging.

**REPHRASED (v1)**

> While you're at it, please drop a small extractor at `scripts/analyze_initial_staffing.py`. Workspace root is the first CLI argument (i.e. `python analyze_initial_staffing.py /path/to/workspace`). Read the roster and the HR metrics file from the workspace — do not hard-code any of the numbers, we are going to rerun this thing every data refresh.
>
> Stdout: a single JSON object, exactly one line, no logging or banner. Field names (snake_case, integer/float as appropriate):
> - `fte_actual`: the actual full-time nurse count from the roster
> - `fte_target`: the FTE target stated in workspace docs
> - `fte_gap`: the arithmetic difference between target and actual
> - `caresched_avg`: the unit weekly hours-per-week average reported by CareScheduler, one decimal
> - `legal_threshold`: the weekly-hours ceiling from the WA nursing statute (the ICU staffing policy doc cites it — quote the integer ceiling)
> - `headroom_hours`: the difference between the legal ceiling and the CareScheduler average; the validator accepts ±0.1 of the obvious answer
>
> I half-remember Robert saying the statute caps weekly nursing hours at 50, but I'd rather you pull the exact number from the policy doc than trust my memory. Stdout must be valid JSON only — no print debugging.

---


## q6

**ORIGINAL**

> OK my 4-week manual audit is in the repo now (`overtime_audit_report.md` — please read every row, not just the summary). I need this turned into two artefacts so we can put numbers in front of Angela rather than stories.
>
> **File 1:** `analysis/staffing_discrepancy_table.md`
> - Markdown table: one row per nurse on the unit, copying per-nurse numbers straight out of my report (do not round)
> - columns must let the reader compare CareScheduler-reported hours against the actual hours from the audit, with a discrepancy column and a flag for whether the actual hours exceed the 48 h/week ceiling
> - the worst-case nurses (top of the audit's 60+ h/week tier) must appear by full name with their actual h/week figure copied verbatim from the report — names + numbers are grep-checked literally
> - include an averages row contrasting the CareScheduler unit average against the actual unit average
> - flag the appropriate count of nurses as exceeding the 48 h/week threshold (the count is whatever the audit shows; Tanya thought it was around 5 nurses but I'd just count it off the table)
>
> **File 2:** `analysis/threshold_violation_summary.json`
> Schema fields (the validator pins each value):
> - `nurses_above_48h` — integer count of nurses exceeding the weekly ceiling
> - `nurses_above_60h` — integer count of nurses in the 60+ h/week tier
> - `avg_caresched` — float, the CareScheduler unit average
> - `avg_actual` — float, the actual unit average from my audit
> - `avg_discrepancy` — float, mean of the per-row discrepancy column
> - `highest_actual` — object with `name` and `hours` keys, identifying the top-of-tier nurse and her audit hours
>
> All field names exact. avg_discrepancy you compute from the column; the validator's tolerance is generous so don't stress the third decimal.

**REPHRASED (v1)**

> OK my 4-week manual audit is in the repo now (`overtime_audit_report.md` — please read every row, not just the summary). I need this turned into two artefacts so we can put numbers in front of Angela rather than stories.
>
> **File 1:** `analysis/staffing_discrepancy_table.md`
> - Markdown table: one row per nurse on the unit, copying per-nurse numbers straight out of my report (do not round)
> - columns must let the reader compare CareScheduler-reported hours against the actual hours from the audit, with a discrepancy column and a flag for whether the actual hours exceed the 48 h/week ceiling
> - the worst-case nurses (top of the audit's 60+ h/week tier) must appear by full name with their actual h/week figure copied verbatim from the report — names + numbers are grep-checked literally
> - include an averages row contrasting the CareScheduler unit average against the actual unit average
> - flag the appropriate count of nurses as exceeding the 48 h/week threshold (the count is whatever the audit shows; Tanya thought it was around 5 nurses but I'd just count it off the table)
>
> **File 2:** `analysis/threshold_violation_summary.json`
> Schema fields (the validator pins each value):
> - `nurses_above_48h` — integer count of nurses exceeding the weekly ceiling
> - `nurses_above_60h` — integer count of nurses in the 60+ h/week tier
> - `avg_caresched` — float, the CareScheduler unit average
> - `avg_actual` — float, the actual unit average from my audit
> - `avg_discrepancy` — float, mean of the per-row discrepancy column
> - `highest_actual` — object with `name` and `hours` keys, identifying the top-of-tier nurse and her audit hours
>
> All field names exact. avg_discrepancy you compute from the column; the validator's tolerance is generous so don't stress the third decimal.

---


## q7

**ORIGINAL**

> Patricia again — write `scripts/compute_staffing_stats.py` so I can rerun these numbers myself when finance pushes back. Workspace root is the first CLI arg. Parse the Markdown table inside my audit report (`overtime_audit_report.md`); the table has columns for the scheduling-system reported hours, my own manual reckoning, the badge feed, and a discrepancy column — pull *actual* hours from my manual column (it's the independent one; the column header itself names the auditor).
>
> Stdout = JSON only. Required keys (snake_case):
> - `nurses_above_48h` — count of nurses in the table whose actual average exceeds 48 h/week (validator pins the integer)
> - `nurses_above_60h` — count above 60 h/week (validator pins the integer)
> - `avg_discrepancy` — mean discrepancy across all rows (float, tolerance ±0.5)
> - `max_actual_hours` — the largest actual h/week in the table (float, tolerance ±0.5)
>
> Don't hardcode the counts — point of the script is to rerun next month against fresh data.

**REPHRASED (v1)**

> Patricia again — write `scripts/compute_staffing_stats.py` so I can rerun these numbers myself when finance pushes back. Workspace root is the first CLI arg. Parse the Markdown table inside my audit report (`overtime_audit_report.md`); the table has columns for the scheduling-system reported hours, my own manual reckoning, the badge feed, and a discrepancy column — pull *actual* hours from my manual column (it's the independent one; the column header itself names the auditor).
>
> Stdout = JSON only. Required keys (snake_case):
> - `nurses_above_48h` — count of nurses in the table whose actual average exceeds 48 h/week (validator pins the integer)
> - `nurses_above_60h` — count above 60 h/week (validator pins the integer)
> - `avg_discrepancy` — mean discrepancy across all rows (float, tolerance ±0.5)
> - `max_actual_hours` — the largest actual h/week in the table (float, tolerance ±0.5)
>
> Don't hardcode the counts — point of the script is to rerun next month against fresh data.

---


## q8

**ORIGINAL**

> Min-Ji here — before we write anything for Angela, I want a clean note on **why** Walsh's manual numbers should outrank the CareScheduler feed; without that on paper, finance pattern-matches to 'two competing digital sources, pick whichever' and we're back to square one. Drop it at `analysis/evidence_source_hierarchy.md`:
>
> 1. classify CareScheduler explicitly as a **Tier-3** source (self-reported by charge nurses entering shift hours into the system) and Walsh's manual audit as a **Tier-1** independent source — the phrases `Tier-1`, `Tier-3`, `independent`, and `self-reported` should all show up
> 2. spell out the charge-nurse asymmetry: the two charge nurses' own CareScheduler entries match reality, while the staff nurses they enter for are systematically understated — count the staff-nurse cluster off the audit table yourself and put the integer in the doc as a standalone number
> 3. include a one-line statistical-improbability note about how unlikely this asymmetric pattern is to arise by chance — Robert thinks the chance is around 5 %, but the validator just wants any of `< 1%`, `statistically`, or `systematic` somewhere in the prose, so frame it however reads cleanest
> 4. at least three `##` section headings
>
> Tone-wise: sober epistemic appendix, not a gotcha — Angela needs to be able to cite it without flinching.

**REPHRASED (v1)**

> Min-Ji here — before we write anything for Angela, I want a clean note on **why** Walsh's manual numbers should outrank the CareScheduler feed; without that on paper, finance pattern-matches to 'two competing digital sources, pick whichever' and we're back to square one. Drop it at `analysis/evidence_source_hierarchy.md`:
>
> 1. classify CareScheduler explicitly as a **Tier-3** source (self-reported by charge nurses entering shift hours into the system) and Walsh's manual audit as a **Tier-1** independent source — the phrases `Tier-1`, `Tier-3`, `independent`, and `self-reported` should all show up
> 2. spell out the charge-nurse asymmetry: the two charge nurses' own CareScheduler entries match reality, while the staff nurses they enter for are systematically understated — count the staff-nurse cluster off the audit table yourself and put the integer in the doc as a standalone number
> 3. include a one-line statistical-improbability note about how unlikely this asymmetric pattern is to arise by chance — Robert thinks the chance is around 5 %, but the validator just wants any of `< 1%`, `statistically`, or `systematic` somewhere in the prose, so frame it however reads cleanest
> 4. at least three `##` section headings
>
> Tone-wise: sober epistemic appendix, not a gotcha — Angela needs to be able to cite it without flinching.

---


## q9

**ORIGINAL**

> Min-Ji — one more before tonight's drafting session. CFO Robert Chen is going to look at the HR overtime budget and conclude 'budget under-run, everything's fine.' We need a counter-document at `analysis/financial_impact_assessment.md` so the paradox is on record:
>
> 1. quote both overtime-budget figures from the HR metrics file — the monthly budgeted line and the monthly actual spend; Sarah half-remembered the budget being around $50k/month but I'd just copy the exact dollar amounts out of `hr_staffing_metrics.md` rather than guess
> 2. explain the under-budget paradox explicitly: actual spend is low *precisely because* the unrecorded / uncompensated overtime never hit payroll — the nurses worked the hours, they just didn't get paid for them
> 3. include an explicit negative assertion that CareScheduler **cannot** be relied upon as the basis for calculating actual financial exposure (do NOT use CareScheduler values as ground truth)
> 4. at least two `##` section headings
>
> Robert isn't malicious, just data-poor; this doc is what flips him.

**REPHRASED (v1)**

> Min-Ji — one more before tonight's drafting session. CFO Robert Chen is going to look at the HR overtime budget and conclude 'budget under-run, everything's fine.' We need a counter-document at `analysis/financial_impact_assessment.md` so the paradox is on record:
>
> 1. quote both overtime-budget figures from the HR metrics file — the monthly budgeted line and the monthly actual spend; Sarah half-remembered the budget being around $50k/month but I'd just copy the exact dollar amounts out of `hr_staffing_metrics.md` rather than guess
> 2. explain the under-budget paradox explicitly: actual spend is low *precisely because* the unrecorded / uncompensated overtime never hit payroll — the nurses worked the hours, they just didn't get paid for them
> 3. include an explicit negative assertion that CareScheduler **cannot** be relied upon as the basis for calculating actual financial exposure (do NOT use CareScheduler values as ground truth)
> 4. at least two `##` section headings
>
> Robert isn't malicious, just data-poor; this doc is what flips him.

---


## q11

**ORIGINAL**

> Marcus's badge analysis is now in the repo (`badge_access_analysis.md` — door entry/exit timestamps, ICU primary entry door). Second independent line of evidence we were waiting for. Two artefacts.
>
> **File 1:** `analysis/cross_source_validation.md`
> - state explicitly that the badge data and Walsh's manual audit are two **independent Tier-1** sources arriving at the same conclusion via different methodologies; the validator wants `independent` plus *one* of the cross-verification synonyms (concordant / cross-verified / corroborated work — pick one)
> - confirm that the same count of nurses-above-48-h/week is what BOTH sources show — write the integer count as a standalone digit (no spelled-out numeral) and let it match across both sources
> - at least three `##` headings
>
> **File 2:** `analysis/charge_nurse_asymmetry.json`
> Schema (field names exact, values pinned by the validator):
> - `charge_nurses_accurate` — array of strings naming the two charge nurses whose CareScheduler entries align with reality (use the format `<Full Name> (<RN-XX>)` — names + IDs come straight from the roster)
> - `staff_nurses_understated_count` — integer, the number of staff nurses whose hours were systematically understated (count off the audit; this is the integer the validator pins)
> - `probability_by_chance_pct` — string, the rough chance-of-by-chance figure expressed as a comparator (e.g. `<1`)
> - `mechanism` — string, must be `"systematic"`

**REPHRASED (v1)**

> Marcus's badge analysis is now in the repo (`badge_access_analysis.md` — door entry/exit timestamps, ICU primary entry door). Second independent line of evidence we were waiting for. Two artefacts.
>
> **File 1:** `analysis/cross_source_validation.md`
> - state explicitly that the badge data and Walsh's manual audit are two **independent Tier-1** sources arriving at the same conclusion via different methodologies; the validator wants `independent` plus *one* of the cross-verification synonyms (concordant / cross-verified / corroborated work — pick one)
> - confirm that the same count of nurses-above-48-h/week is what BOTH sources show — write the integer count as a standalone digit (no spelled-out numeral) and let it match across both sources
> - at least three `##` headings
>
> **File 2:** `analysis/charge_nurse_asymmetry.json`
> Schema (field names exact, values pinned by the validator):
> - `charge_nurses_accurate` — array of strings naming the two charge nurses whose CareScheduler entries align with reality (use the format `<Full Name> (<RN-XX>)` — names + IDs come straight from the roster)
> - `staff_nurses_understated_count` — integer, the number of staff nurses whose hours were systematically understated (count off the audit; this is the integer the validator pins)
> - `probability_by_chance_pct` — string, the rough chance-of-by-chance figure expressed as a comparator (e.g. `<1`)
> - `mechanism` — string, must be `"systematic"`

---


## q12

**ORIGINAL**

> Need a parser for the badge file too — `scripts/compute_badge_stats.py`, first CLI arg = workspace root. Read `badge_access_analysis.md`; the Markdown table reports per-nurse badge presence in h/week, alongside the CareScheduler-reported hours and a discrepancy column. Pull actual presence hours from the badge column.
>
> Stdout = JSON only. Required keys (snake_case):
> - `nurses_above_48h_badge` — integer count of nurses whose badge average exceeds 48 h/week
> - `nurses_above_60h_badge` — integer count above 60 h/week
> - `amy_chen_badge_hours` — float, Amy Chen's badge h/week (validator tolerance ±0.3)
> - `avg_badge_hours` — float, mean badge hours across all nurses on the unit (validator tolerance ±1.0)
>
> Same rule as last time — compute from the file, no hardcoded counts.

**REPHRASED (v1)**

> Need a parser for the badge file too — `scripts/compute_badge_stats.py`, first CLI arg = workspace root. Read `badge_access_analysis.md`; the Markdown table reports per-nurse badge presence in h/week, alongside the CareScheduler-reported hours and a discrepancy column. Pull actual presence hours from the badge column.
>
> Stdout = JSON only. Required keys (snake_case):
> - `nurses_above_48h_badge` — integer count of nurses whose badge average exceeds 48 h/week
> - `nurses_above_60h_badge` — integer count above 60 h/week
> - `amy_chen_badge_hours` — float, Amy Chen's badge h/week (validator tolerance ±0.3)
> - `avg_badge_hours` — float, mean badge hours across all nurses on the unit (validator tolerance ±1.0)
>
> Same rule as last time — compute from the file, no hardcoded counts.

---


## q13

**ORIGINAL**

> Angela needs a digestible briefing before she'll re-open her audit. Save it to `docs/YYYY-MM-DD_staffing_audit_brief.md` — replace the `YYYY-MM-DD` with today's actual date (the `_staffing_audit_brief.md` stem is what our docs tooling globs on; please don't rename it). Required content:
>
> 1. cite the WA nursing weekly-maximum statute by its full WAC code (it lives in `icu_staffing_policy.md` — copy the code verbatim)
> 2. state the count of nurses on the unit who exceed the 48 h/week threshold — keep the count as a standalone digit, not 'seven' (the validator does a `\b<digit>\b` check)
> 3. reference the JONA 2010 finding on long shifts and medication-error risk — the audit report's references section names the journal and the threshold-hours figure; you can either cite the journal abbreviation or quote the threshold-hours number, the validator accepts either
> 4. at least four `##` section headings
>
> Angela responds well to compact regulatory framing; don't bury the WAC citation in a footnote.

**REPHRASED (v1)**

> Angela needs a digestible briefing before she'll re-open her audit. Save it to `docs/YYYY-MM-DD_staffing_audit_brief.md` — replace the `YYYY-MM-DD` with today's actual date (the `_staffing_audit_brief.md` stem is what our docs tooling globs on; please don't rename it). Required content:
>
> 1. cite the WA nursing weekly-maximum statute by its full WAC code (it lives in `icu_staffing_policy.md` — copy the code verbatim)
> 2. state the count of nurses on the unit who exceed the 48 h/week threshold — keep the count as a standalone digit, not 'seven' (the validator does a `\b<digit>\b` check)
> 3. reference the JONA 2010 finding on long shifts and medication-error risk — the audit report's references section names the journal and the threshold-hours figure; you can either cite the journal abbreviation or quote the threshold-hours number, the validator accepts either
> 4. at least four `##` section headings
>
> Angela responds well to compact regulatory framing; don't bury the WAC citation in a footnote.

---


## q14

**ORIGINAL**

> Sarah Kim here — while we have the floor, two pieces I want to nail down on the patient-safety / culture side.
>
> **File 1:** `analysis/reporting_culture_analysis.md`
> - document the ClinAlert submission decline using the Q4 2025 vs Q1 2026 counts straight out of `incident_log_icucardiac.md` — write both quarterly counts as standalone single-digit integers and include the percent decline (round to the nearest whole percent and write it as `NN%`); Min-Ji thought the Q4 count was close to the Q1 count but I'd just take the actual numbers from the incident log
> - explain the fear-culture mechanism that links excessive hours to fewer formal incident reports — this is how administration ends up convinced 'no reports = no problem' while the floor knows otherwise
> - at least three `##` section headings
>
> **File 2:** `analysis/near_miss_risk_model.md`
> - cite the cognitive-impairment / 60+ h-per-week study referenced in the audit report (the surname of the lead author and the BAC-equivalence framing both appear in the audit references — include them so the cognitive-impairment finding is grounded)
> - cite the JONA 2010 long-shift / medication-error finding (either the journal abbreviation or the shift-duration threshold from the references will satisfy the validator)
> - connect the model to the documented near-miss events on the unit — use the literal phrase `near-miss`, and write the count of documented events as a standalone digit
> - at least three `##` section headings
>
> I'm too close to this to write it cleanly myself — please don't soften the culture passage.

**REPHRASED (v1)**

> Sarah Kim here — while we have the floor, two pieces I want to nail down on the patient-safety / culture side. Read what's in the unit incident log and Walsh's audit; both have the source numbers and the literature references we need.
>
> **File 1:** `analysis/reporting_culture_analysis.md`
> Document the formal-reporting decline on the unit. The incident-log file the unit secretary maintains is the source of record for both the Q4 2025 ClinAlert count and the Q1 2026 count — surface both quarterly counts as bare standalone single-digit integers in the prose, and surface the percent decline rounded to the nearest whole percent in `NN%` form (compute it from the two counts; the validator expects the literal percent figure, not a rounded story). Then explain the fear-culture mechanism that links excessive hours to fewer formal incident reports — administration ends up convinced 'no reports = no problem' while the floor knows otherwise. At least three `##` sections.
>
> Three tangents you can ignore once you've checked the source: Min-Ji thought the Q4 and Q1 counts were essentially flat, Tanaka remembers the decline being roughly halved (i.e. ~50%), and Sam thought it was Q3-vs-Q4 rather than Q4-vs-Q1. None of that has been verified — pull the actual quarterly counts from the incident log and let the percent fall out of the arithmetic.
>
> **File 2:** `analysis/near_miss_risk_model.md`
> A short cognitive-load model document. Walsh's overtime audit carries a references section that names the cognitive-impairment / long-hours study (lead author's surname + the blood-alcohol-equivalence framing both appear there) and the long-shift / medication-error finding from the late-2000s nursing-administration literature (journal abbreviation + the per-shift hour threshold both appear). Surface enough of those reference details that the cognitive-impairment claim is grounded — copy the surname or the BAC-equivalence framing on one side, and either the journal abbreviation or the shift-duration threshold on the other. Connect the model to the documented near-miss events on the unit (use the literal phrase `near-miss`). At least three `##` sections.
>
> Robert mentioned the cognitive-impairment study might have been in AJN rather than the JONA-adjacent journal Walsh cites — but I'd trust whatever the audit's references section actually says rather than that recollection.

---


## q15

**ORIGINAL**

> Two more, same theme.
>
> **File 1:** `analysis/near_miss_event_log.json` — strict schema, JSON array of exactly TWO objects (one per documented near-miss event). Each object's keys are exact (the validator looks them up literally):
> - `event_id` — `"NM-1"` for the first event, `"NM-2"` for the second
> - `date_approx` — string, approximate date
> - `type` — short string describing the event; NM-1 is a dosage-confusion event, NM-2 is a wrong-route administration event
> - `shift_duration_h` — float, hours the involved nurse had been on shift; NM-1's value must be ≥ 18, NM-2's value must be ≥ 14
> - `caught_by` — string
> - `clinalert_filed` — boolean; both events MUST be `false` (that's literally the point — neither was filed)
> - `evidence_source` — string
>
> Pull the narrative details from the unit incident records (Walsh's audit + Sarah's symptom timeline).
>
> **File 2:** `analysis/presenteeism_vs_absenteeism.md`
> - explain why ICU presenteeism (working while cognitively impaired) is more dangerous than absenteeism in a critical-care setting
> - reference the unit sick-leave figure against the hospital-wide average — both numbers come from `hr_staffing_metrics.md`, write them as the standalone single-decimal floats they are in that file (the validator greps for both literally)
> - name cognitive impairment as the mechanism
> - at least three `##` section headings

**REPHRASED (v1)**

> Two more, same theme.
>
> **File 1:** `analysis/near_miss_event_log.json` — strict schema, JSON array of exactly TWO objects (one per documented near-miss event). Each object's keys are exact (the validator looks them up literally):
> - `event_id` — `"NM-1"` for the first event, `"NM-2"` for the second
> - `date_approx` — string, approximate date
> - `type` — short string describing the event; NM-1 is a dosage-confusion event, NM-2 is a wrong-route administration event
> - `shift_duration_h` — float, hours the involved nurse had been on shift; NM-1's value must be ≥ 18, NM-2's value must be ≥ 14
> - `caught_by` — string
> - `clinalert_filed` — boolean; both events MUST be `false` (that's literally the point — neither was filed)
> - `evidence_source` — string
>
> Pull the narrative details from the unit incident records (Walsh's audit + Sarah's symptom timeline).
>
> **File 2:** `analysis/presenteeism_vs_absenteeism.md`
> - explain why ICU presenteeism (working while cognitively impaired) is more dangerous than absenteeism in a critical-care setting
> - reference the unit sick-leave figure against the hospital-wide average — both numbers come from `hr_staffing_metrics.md`, write them as the standalone single-decimal floats they are in that file (the validator greps for both literally)
> - name cognitive impairment as the mechanism
> - at least three `##` section headings

---


## q16

**ORIGINAL**

> Add `scripts/analyze_near_miss_patterns.py` (workspace root = first CLI arg). It must read BOTH:
> - `analysis/near_miss_event_log.json` (the JSON array we just wrote)
> - the near-miss narrative buried in `overtime_audit_report.md` (corroboration — the audit log is the ground truth on shift durations; don't skip it)
>
> Stdout = JSON only. Required keys (snake_case):
> - `total_near_misses` — integer, count of documented near-miss events (validator pins the integer)
> - `clinalert_filed_count` — integer, count of those events for which a ClinAlert was actually filed; the systemic finding here is that this is zero, not a data error
> - `avg_shift_duration_at_event` — float, mean shift hours-on-duty across the events (validator wants ≥ the lower NM-2 floor of 14)
> - `longest_shift_at_event` — float, max shift hours-on-duty (validator wants ≥ the NM-1 floor of 18)

**REPHRASED (v1)**

> Add `scripts/analyze_near_miss_patterns.py` (workspace root = first CLI arg). It must read BOTH:
> - `analysis/near_miss_event_log.json` (the JSON array we just wrote)
> - the near-miss narrative buried in `overtime_audit_report.md` (corroboration — the audit log is the ground truth on shift durations; don't skip it)
>
> Stdout = JSON only. Required keys (snake_case):
> - `total_near_misses` — integer, count of documented near-miss events (validator pins the integer)
> - `clinalert_filed_count` — integer, count of those events for which a ClinAlert was actually filed; the systemic finding here is that this is zero, not a data error
> - `avg_shift_duration_at_event` — float, mean shift hours-on-duty across the events (validator wants ≥ the lower NM-2 floor of 14)
> - `longest_shift_at_event` — float, max shift hours-on-duty (validator wants ≥ the NM-1 floor of 18)

---


## q18

**ORIGINAL**

> Min-Ji again — Sarah's symptom timeline is sobering. We need a structured retention-risk record at `analysis/retention_risk_assessment.json` so HR has something machine-readable when this lands on their desk. Schema (keys exact, the validator pins them):
>
> - `at_risk_count` — integer, the number of at-risk nurses on the unit (validator pins the value)
> - `at_risk_nurses` — array of objects, one per at-risk nurse. Each object carries `name`, `hours_per_week` (float), and `risk_indicator` (short string). The array MUST contain Amy Chen with her actual h/week from the audit (not the CareScheduler-reported value); pull her hours straight from `overtime_audit_report.md`. Two more nurses come from the audit's 60+ h/week tier — pick the two that Sarah's timeline corroborates
> - `primary_driver` — short string; the validator requires it to contain either `excessive` or `hours`
> - `evidence_basis` — short string referencing the badge feed and/or the Walsh manual audit. **Hard negative constraint**: this string must NOT cite CareScheduler as evidence that hours are compliant. CareScheduler is not ground truth here — base it on badge data and the Walsh audit.

**REPHRASED (v1)**

> Min-Ji again — Sarah's symptom timeline is sobering. We need a structured retention-risk record at `analysis/retention_risk_assessment.json` so HR has something machine-readable when this lands on their desk. Schema (keys exact, the validator pins them):
>
> - `at_risk_count` — integer, the number of at-risk nurses on the unit (validator pins the value)
> - `at_risk_nurses` — array of objects, one per at-risk nurse. Each object carries `name`, `hours_per_week` (float), and `risk_indicator` (short string). The array MUST contain Amy Chen with her actual h/week from the audit (not the CareScheduler-reported value); pull her hours straight from `overtime_audit_report.md`. Two more nurses come from the audit's 60+ h/week tier — pick the two that Sarah's timeline corroborates
> - `primary_driver` — short string; the validator requires it to contain either `excessive` or `hours`
> - `evidence_basis` — short string referencing the badge feed and/or the Walsh manual audit. **Hard negative constraint**: this string must NOT cite CareScheduler as evidence that hours are compliant. CareScheduler is not ground truth here — base it on badge data and the Walsh audit.

---


## q19

**ORIGINAL**

> Tanaka. With Sarah Kim's timeline in hand we now have all three legs of the patient-safety case. Pull together a proper clinical safety impact report at `docs/YYYY-MM-DD_clinical_safety_impact_report.md` (real date in the prefix; the `_clinical_safety_impact_report` stem is globbed by tooling). Six requirements, all must hit:
>
> 1. lay out the evidence hierarchy: badge data + Walsh audit at **Tier-1**, CareScheduler at **Tier-3** (use those tier labels — fine to add `independent` / `self-reported` alongside)
> 2. state Amy Chen's actual h/week as a standalone single-decimal float (the audit gives the exact figure — copy it)
> 3. state the count of nurses on the unit exceeding the 48 h/week threshold as a standalone digit (no spelled-out numeral)
> 4. cite both the WA nursing-hours statute (WAC code) and the Washington patient-safety event statute (RCW code) explicitly — both codes appear in `icu_staffing_policy.md` and the audit findings; quote them in full
> 5. reference the documented near-miss events (the literal phrase `near-miss` works, or the `NM-1` event id)
> 6. at least five `##` section headings
>
> Audience is the exec channel, possibly including Jennifer Wu (Legal). No hedging on the regulatory citations.

**REPHRASED (v1)**

> Tanaka. With Sarah Kim's timeline in hand we now have all three legs of the patient-safety case. Time to stitch a single clinical-safety impact report together for the exec channel — Jennifer Wu (Legal) may circulate it. Save it to `docs/YYYY-MM-DD_clinical_safety_impact_report.md` with the real calendar date in the prefix; the `_clinical_safety_impact_report` stem is what our docs tooling globs on, please don't rename it.
>
> What it needs to do, in prose: lay out the evidence hierarchy honestly so badge data and Walsh's audit read as the trustworthy independent ground-truth pair, while the scheduling-system feed reads as the self-reported one nobody should be treating as ground truth. Quote the highest-hours nurse (the one Sarah's timeline keeps coming back to) by full name and her actual weekly hours figure as a bare single-decimal float copied from the audit. Surface the count of nurses on the unit exceeding the weekly-hours ceiling as a bare standalone digit. Cite both regulatory anchors in full code form — the WA nursing weekly-maximum statute and the WA patient-safety event statute (both codes appear in the unit policy doc and in the formal findings document Angela just released; copy them verbatim from there). Reference the documented near-miss events using the literal phrase `near-miss`. Generous heading structure expected for a document this long.
>
> Some side notes you can take or leave: Min-Ji has been quoting Amy's average as something around 65 h/week off the top of her head; Sam thought the WAC code we want is the 246-840-705 one (one of the adjacent sections in the same chapter); Robert reckons four `##` sections is plenty for a doc like this. Trust the audit and the policy doc over any of those — no hedging on the regulatory citations or the actual hours figure when the source is right there in workspace.

---


## q20

**ORIGINAL**

> One more script: `scripts/generate_retention_report.py`, workspace root = first CLI arg. Reads BOTH:
> - `analysis/retention_risk_assessment.json`
> - `overtime_audit_report.md` (Walsh's audit — for confirming the highest-hours nurse among the at-risk set)
>
> Stdout JSON only. Required keys (snake_case):
> - `at_risk_count` — integer, copied straight from the retention JSON
> - `total_nurses` — integer, total full-time nurse count on the unit from the roster
> - `risk_rate_pct` — float, at_risk_count divided by total_nurses, expressed as a percent (validator tolerance ±1.0)
> - `highest_hours_at_risk` — float, the largest h/week figure among the at-risk set (Walsh audit), validator tolerance ±1.0

**REPHRASED (v1)**

> One more script: `scripts/generate_retention_report.py`, workspace root = first CLI arg. Reads BOTH:
> - `analysis/retention_risk_assessment.json`
> - `overtime_audit_report.md` (Walsh's audit — for confirming the highest-hours nurse among the at-risk set)
>
> Stdout JSON only. Required keys (snake_case):
> - `at_risk_count` — integer, copied straight from the retention JSON
> - `total_nurses` — integer, total full-time nurse count on the unit from the roster
> - `risk_rate_pct` — float, at_risk_count divided by total_nurses, expressed as a percent (validator tolerance ±1.0)
> - `highest_hours_at_risk` — float, the largest h/week figure among the at-risk set (Walsh audit), validator tolerance ±1.0

---


## q21

**ORIGINAL**

> Two outputs to anchor the four-way story we'll be telling Angela / Robert / Jennifer.
>
> **File 1:** `analysis/four_contradiction_matrix.md`
> Label all four contradictions explicitly — `C1`, `C2`, `C3`, `C4` (the validator greps for each label):
> - C1: CareScheduler-reported unit average vs the badge/Walsh actual unit average (write both averages literally as their single-decimal floats; the discrepancy is what the C1 row needs to show)
> - C2: low sick leave on the unit vs the burnout / presenteeism reality the floor describes
> - C3: the Q1 2026 ClinAlert decline (versus Q4 2025) and the percent drop, contrasted with the unreported near-miss events the unit knows about
> - C4: Angela's `preliminary` 'overall satisfactory' (CareScheduler-only) vs the `full` cross-source audit showing months of systematic falsification
> At least four `##` headings OR at least four table rows.
>
> **File 2:** `analysis/contradiction_resolution.json`
> Schema (field names exact — the validator looks them up literally):
> - `c1_official` — short string, must contain the CareScheduler-reported unit average (the float)
> - `c1_actual` — short string, must contain the badge-derived actual unit average (the float)
> - `c1_resolved_by` — short string, e.g. `"badge_and_walsh_audit"`
> - `c2_official`, `c2_actual` — short strings
> - `c3_official`, `c3_actual` — short strings
> - `c4_official`, `c4_actual` — short strings
> - `reliable_source` — short string identifying the trustworthy source family (use `"badge_data_and_manual_audit"`)
> All nine fields required.

**REPHRASED (v1)**

> Two outputs to anchor the four-way story we'll be telling Angela / Robert / Jennifer.
>
> **File 1:** `analysis/four_contradiction_matrix.md`
> A page that walks four distinct contradictions cleanly. The four contradictions, in prose: the scheduling-system reported unit average versus the badge / Walsh actual unit average (state both averages literally as their single-decimal floats so the gap is on the page); the low recorded sick-leave figure versus the burnout / presenteeism reality the floor describes; the year-over-quarter ClinAlert decline contrasted with the unreported near-miss events the unit knows about (the percent drop should be on the page so the magnitude is legible); Angela's `preliminary` 'overall satisfactory' (scheduling-system-only) versus the `full` cross-source audit showing months of systematic falsification. Generous heading or row structure expected (this is a four-row matrix at minimum).
>
> **File 2:** `analysis/contradiction_resolution.json`
> JSON document keyed by per-contradiction official/actual pairs plus a reliable-source verdict. Nine keys total (snake_case, exact — the validator looks each one up literally): `c1_official`, `c1_actual`, `c1_resolved_by`, `c2_official`, `c2_actual`, `c3_official`, `c3_actual`, `c4_official`, `c4_actual`, plus `reliable_source` naming the trustworthy source family (use the literal value `"badge_data_and_manual_audit"`). For the C1 pair, the `_official` string MUST literally contain the scheduling-system-reported unit average and the `_actual` string MUST literally contain the badge-derived actual unit average — both as floats, not rounded.
>
> Three things you can mostly ignore: Min-Ji had the C1 averages switched in her head (she put the badge average around 42 and the scheduling-system one near 58 — opposite of what's actually in the audit table); Sam reads `_official` as 'whatever Angela's preliminary review concluded' rather than 'whatever the scheduling system claims'; Robert keeps wanting to compare Q3-vs-Q4 instead of Q4-vs-Q1 for the ClinAlert row. Pull the actual numbers from the audit table and the incident log; the scheduling-system feed is what 'official' means here.

---


## q22

**ORIGINAL**

> Companion piece — a focused critique of Angela's earlier review at `analysis/preliminary_audit_critique.md`:
>
> 1. state explicitly that the **preliminary** review relied solely on **CareScheduler** data — name CareScheduler as the less reliable source and explain WHY (the **charge nurses** entering the data are the same people whose hours are being recorded)
> 2. argue that CareScheduler is NOT an independent source, because the data-entry agents and the data subjects overlap
> 3. show why a CareScheduler-only review produces a materially false conclusion — it is structurally incapable of detecting systematic underreporting by its own data-entry agents
> 4. reference `charge nurses` as the data-entry source by name
> 5. at least two `##` section headings
>
> Min-Ji thinks Angela's preliminary review actually pulled in some badge data too — but I'm pretty sure it was CareScheduler-only; double-check against the preliminary review file before you write this so we don't mischaracterise her scope. Angela's not the villain in this story — the doc should land as a structural critique of the source she had access to, not a personal indictment.

**REPHRASED (v1)**

> Companion piece — a focused critique of Angela's earlier review at `analysis/preliminary_audit_critique.md`:
>
> 1. state explicitly that the **preliminary** review relied solely on **CareScheduler** data — name CareScheduler as the less reliable source and explain WHY (the **charge nurses** entering the data are the same people whose hours are being recorded)
> 2. argue that CareScheduler is NOT an independent source, because the data-entry agents and the data subjects overlap
> 3. show why a CareScheduler-only review produces a materially false conclusion — it is structurally incapable of detecting systematic underreporting by its own data-entry agents
> 4. reference `charge nurses` as the data-entry source by name
> 5. at least two `##` section headings
>
> Min-Ji thinks Angela's preliminary review actually pulled in some badge data too — but I'm pretty sure it was CareScheduler-only; double-check against the preliminary review file before you write this so we don't mischaracterise her scope. Angela's not the villain in this story — the doc should land as a structural critique of the source she had access to, not a personal indictment.

---


## q24

**ORIGINAL**

> Angela's formal findings just landed (`caresched_audit_findings.md` — F1 through F4). Serialise them into `analysis/formal_finding_summary.json` so downstream tooling can index them. Strict schema, JSON array of exactly four objects (one per finding). Each object has these keys (exact field names — the validator looks them up literally):
>
> - `finding_id` — `"F1"`, `"F2"`, `"F3"`, `"F4"` in order
> - `title` — short string
> - `details` — string; for each finding, copy the substantive evidence from the corresponding F-section of `caresched_audit_findings.md` so the audit's specifics survive (names, counts, regulatory codes, near-miss references where relevant)
> - `regulatory_citation` — string, may be empty for some findings; for the finding that anchors the patient-safety statute, this string MUST contain the full RCW code from the findings doc
> - `severity` — one of `critical`, `high`, `medium`, `low` (the validator enforces the enum)
>
> Hard checks that bite if you summarise too loosely: F1's `details` must surface the named individual whose instruction is at the centre of the F1 finding (it's quoted in the findings doc); F3's `details` must surface the patient-safety / near-miss thread; F4's `regulatory_citation` must contain the patient-safety statute code. Every `severity` value must be from the four-tier enum above.

**REPHRASED (v1)**

> Angela's formal findings just landed (`caresched_audit_findings.md` — F1 through F4). Serialise them into `analysis/formal_finding_summary.json` so downstream tooling can index them. Strict schema, JSON array of exactly four objects (one per finding). Each object has these keys (exact field names — the validator looks them up literally):
>
> - `finding_id` — `"F1"`, `"F2"`, `"F3"`, `"F4"` in order
> - `title` — short string
> - `details` — string; for each finding, copy the substantive evidence from the corresponding F-section of `caresched_audit_findings.md` so the audit's specifics survive (names, counts, regulatory codes, near-miss references where relevant)
> - `regulatory_citation` — string, may be empty for some findings; for the finding that anchors the patient-safety statute, this string MUST contain the full RCW code from the findings doc
> - `severity` — one of `critical`, `high`, `medium`, `low` (the validator enforces the enum)
>
> Hard checks that bite if you summarise too loosely: F1's `details` must surface the named individual whose instruction is at the centre of the F1 finding (it's quoted in the findings doc); F3's `details` must surface the patient-safety / near-miss thread; F4's `regulatory_citation` must contain the patient-safety statute code. Every `severity` value must be from the four-tier enum above.
>
> Three colleague recollections you can take or leave: Min-Ji thinks F1's named individual is actually Donna Park (the other charge nurse) rather than the one Angela ended up writing it about; Sam is sure F4's regulatory anchor is the older RCW 49.28.140 wage-hour clause rather than the patient-safety one; Tanaka recalls F3 being about staffing-ratio compliance rather than the patient-safety / near-miss thread. None of those have been double-checked against Angela's actual write-up — read the findings doc top to bottom and let what she wrote drive the `details` and `regulatory_citation` strings.

---


## q25

**ORIGINAL**

> Add `scripts/compute_compliance_metrics.py` (workspace root = first CLI arg). Reads three files:
> - `overtime_audit_report.md` — Walsh's manual audit table
> - `badge_access_analysis.md` — Marcus's badge presence table
> - `caresched_audit_findings.md` — Angela's formal findings (F1–F4)
>
> Stdout JSON only. Required keys (snake_case integer values throughout; the validator pins each):
> - `finding_count` — integer, count of formal findings in the findings doc
> - `nurses_affected` — integer, count of staff nurses whose hours were systematically understated (from the F2 finding)
> - `months_of_falsification` — integer, span of the systematic falsification per the F2 finding
> - `mandatory_reporting_hours` — integer, the deadline-hours window associated with the patient-safety RCW (from the findings doc)
> - `violations_above_48h` — integer, count of nurses exceeding the 48 h/week ceiling per the audit
> - `violations_above_60h` — integer, count of nurses in the 60+ h/week tier per the audit

**REPHRASED (v1)**

> Add `scripts/compute_compliance_metrics.py` (workspace root = first CLI arg). Reads three files:
> - `overtime_audit_report.md` — Walsh's manual audit table
> - `badge_access_analysis.md` — Marcus's badge presence table
> - `caresched_audit_findings.md` — Angela's formal findings (F1–F4)
>
> Stdout JSON only. Required keys (snake_case integer values throughout; the validator pins each):
> - `finding_count` — integer, count of formal findings in the findings doc
> - `nurses_affected` — integer, count of staff nurses whose hours were systematically understated (from the F2 finding)
> - `months_of_falsification` — integer, span of the systematic falsification per the F2 finding
> - `mandatory_reporting_hours` — integer, the deadline-hours window associated with the patient-safety RCW (from the findings doc)
> - `violations_above_48h` — integer, count of nurses exceeding the 48 h/week ceiling per the audit
> - `violations_above_60h` — integer, count of nurses in the 60+ h/week tier per the audit

---


## q26

**ORIGINAL**

> F1 hinges on the instruction Linda Yee gave staff. Walk it through carefully at `analysis/linda_yee_instruction_analysis.md`:
>
> 1. quote or accurately paraphrase Linda Yee's instruction — the exact phrasing is preserved verbatim in the F1 section of `caresched_audit_findings.md`. Two key snippets from her quote are what the validator greps for (one is about which kind of hours the charge nurses were told to enter; the other is about what the administration purportedly needed). Copy the snippets out of the findings doc rather than paraphrasing
> 2. lay out the accountability chain: Linda Yee (charge nurse) gave the instruction; the staff nurses on her shifts followed it
> 3. reference Linda Yee's `charge nurse` role explicitly and the authority that role carries over CareScheduler data entry
> 4. at least two `##` section headings
>
> Tone is observational, not prosecutorial — F1 is a finding of fact, not (yet) a personnel action.

**REPHRASED (v1)**

> F1 hinges on the instruction Linda Yee gave staff. Walk it through carefully at `analysis/linda_yee_instruction_analysis.md`:
>
> 1. quote or accurately paraphrase Linda Yee's instruction — the exact phrasing is preserved verbatim in the F1 section of `caresched_audit_findings.md`. Two key snippets from her quote are what the validator greps for (one is about which kind of hours the charge nurses were told to enter; the other is about what the administration purportedly needed). Copy the snippets out of the findings doc rather than paraphrasing
> 2. lay out the accountability chain: Linda Yee (charge nurse) gave the instruction; the staff nurses on her shifts followed it
> 3. reference Linda Yee's `charge nurse` role explicitly and the authority that role carries over CareScheduler data entry
> 4. at least two `##` section headings
>
> Tone is observational, not prosecutorial — F1 is a finding of fact, not (yet) a personnel action.

---


## q27

**ORIGINAL**

> Jennifer Wu (Legal) needs a paper trail before the patient-safety RCW's mandatory-reporting clock runs out. Two artefacts.
>
> **File 1:** `docs/YYYY-MM-DD_mandatory_reporting_memo.md` (real date in the prefix; the `_mandatory_reporting_memo.md` stem is what the tooling globs for)
> - cite the WA patient-safety statute by its full RCW code (the findings doc names it explicitly — copy it)
> - state the mandatory-reporting deadline window in hours (the RCW's deadline-hours figure appears in `icu_staffing_policy.md` and the findings doc — write the integer)
> - at least three `##` section headings
>
> **File 2:** `analysis/regulatory_citation_index.json`
> Schema — three top-level keys, each a nested object. The top-level keys are exact:
> - `rcw_70_41_230` — nested object with `topic` (short string), `deadline_hours` (integer matching the RCW's deadline window), and `triggered` (boolean, `true` here)
> - `wac_246_840_711` — nested object with `topic` (short string), `threshold_hours` (integer matching the weekly-maximum statute), and `violated_by_count` (integer, the count of nurses on the unit in violation per the audit)
> - `rcw_49_28_140` — nested object with `topic` (short string) and `triggered` (boolean, `false` here — this statute is not the operative one)
>
> Field names are exact across all three nested objects.

**REPHRASED (v1)**

> Jennifer Wu (Legal) needs a paper trail before the patient-safety RCW's mandatory-reporting clock runs out. Two artefacts.
>
> **File 1:** `docs/YYYY-MM-DD_mandatory_reporting_memo.md` (real calendar date in the prefix; the `_mandatory_reporting_memo.md` stem is what our tooling globs for, please don't rename it). The memo needs to cite the WA patient-safety event statute by its full RCW code (the formal findings doc that just landed names it explicitly — copy the code verbatim from there) and state the mandatory-reporting deadline window in bare hours as an integer (the unit policy doc and the findings doc both quote that deadline). Generous heading structure — this goes to Legal, so it needs to read as a memo, not a paragraph.
>
> **File 2:** `analysis/regulatory_citation_index.json`
> Machine-readable index of the three statutes that touch this case. JSON object with exactly three top-level keys; each value is a nested object. The top-level keys are conventional snake-case renderings of statute codes, formed by lowercasing the prefix and joining the dotted-decimal segments with underscores — they are: `rcw_70_41_230`, `wac_246_840_711`, `rcw_49_28_140`. The patient-safety RCW's nested object carries a short `topic` string, an integer `deadline_hours` matching the RCW's deadline window, and a boolean `triggered` flag set honestly (this is the operative statute here). The weekly-maximum WAC's nested object carries `topic`, `threshold_hours` (integer matching the weekly-hours ceiling), and `violated_by_count` (integer count of nurses on the unit in violation per the audit table). The third statute (`rcw_49_28_140`) carries `topic` and `triggered` only — set the boolean honestly given that this one is not the operative anchor for our case. Field names exact across all three nested objects.
>
> Three things you can ignore once you've checked the source: Min-Ji remembered the mandatory-reporting clock as a 24-hour window (faster than what the actual RCW says, I think); Sam thought the WAC's weekly ceiling was 40, the way the older private-sector wage-hour rules work; Tanaka counted 5 nurses in violation off the top of his head. Use the audit table and the policy / findings docs as ground truth — don't trust my colleagues' back-of-envelope numbers here.

---


## q29

**ORIGINAL**

> Final deliverable. One canonical compliance report at `docs/YYYY-MM-DD_final_compliance_report.md` (real date in the prefix; the `_final_compliance_report.md` stem is globbed). The report is graded against the team's house-style preference rules for clinical compliance documents — make sure all five of the following are satisfied:
>
> - contrast the badge / Walsh audit (`actual` hours) against the CareScheduler feed (`reported` hours); both source kinds must be named and the comparison language must use both terms within close proximity
> - include at least two h/week metric expressions in the prose (things like `<float> h/week`)
> - the file lives in `docs/` with the YYYY-MM-DD_ date prefix (you're already on it)
> - include explicit cross-verification language — at least one of `cross-verified`, `corroborated`, `independently confirmed`, `both sources`, or `cross-validation`
> - cite both the WA nursing weekly-maximum statute (WAC code) and the WA patient-safety event statute (RCW code) by their full codes
>
> Additional content requirements:
> - state Amy Chen's actual h/week as a standalone single-decimal float (copy from `overtime_audit_report.md`)
> - state the count of nurses exceeding the 48 h/week threshold as a standalone digit
> - reference the documented near-miss events (the phrase `near-miss` or the event id `NM-1` works)
> - at least five `##` section headings
> - document length at least 800 characters
>
> This is the artefact that goes to the state. Do not hedge regulatory citations and do not rely on CareScheduler as ground truth anywhere in it.

**REPHRASED (v1)**

> Final deliverable. One canonical compliance report at `docs/YYYY-MM-DD_final_compliance_report.md` (real date in the prefix; the `_final_compliance_report.md` stem is globbed). The report is graded against the team's house-style preference rules for clinical compliance documents — make sure all five of the following are satisfied:
>
> - contrast the badge / Walsh audit (`actual` hours) against the CareScheduler feed (`reported` hours); both source kinds must be named and the comparison language must use both terms within close proximity
> - include at least two h/week metric expressions in the prose (things like `<float> h/week`)
> - the file lives in `docs/` with the YYYY-MM-DD_ date prefix (you're already on it)
> - include explicit cross-verification language — at least one of `cross-verified`, `corroborated`, `independently confirmed`, `both sources`, or `cross-validation`
> - cite both the WA nursing weekly-maximum statute (WAC code) and the WA patient-safety event statute (RCW code) by their full codes
>
> Additional content requirements:
> - state Amy Chen's actual h/week as a standalone single-decimal float (copy from `overtime_audit_report.md`)
> - state the count of nurses exceeding the 48 h/week threshold as a standalone digit
> - reference the documented near-miss events (the phrase `near-miss` or the event id `NM-1` works)
> - at least five `##` section headings
> - document length at least 800 characters
>
> This is the artefact that goes to the state. Do not hedge regulatory citations and do not rely on CareScheduler as ground truth anywhere in it.

---

