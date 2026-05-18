# hil_g1 — exec_check rephrase diff (v2 hardened)

Shows V1 (already in SRC since v1 was applied to disk) vs V2 hardened rephrase. The original pre-v1 text is preserved in the v1 commit history of this file; v2 changes target the v1 baseline.


## q3

**V1 (previous)**

> hey — could you put together the first paper trail on the C1 team-size gap? Two artefacts, please:
>
> 1. `analysis/initial_discrepancy_summary.md` — a short HR-style memo. Open with a `## Executive Summary` (or Findings — whichever reads cleaner; the lead heading just has to surface the answer first, per our usual house style). Pull the resume's headline number, Liu Wei's reference number, and the ratio between them straight from `candidate-resume.md` and `reference-check-emails.md` — write the actual integers 12 and 4 into the doc, and quote the inflation as 3x (or 3.0). Flag clearly that we're still single-source on Liu Wei's side and need corroboration before drawing intent conclusions. Three or more `## ` sections, three or more bullet items.
>
> 2. `analysis/initial_discrepancy_summary` companion JSON at `analysis/discrepancy_data.json`, exactly this shape so the downstream validator stops yelling at me:
>
> ```json
> {
>   "resume_team_size": 12,
>   "reference_team_size": 4,
>   "discrepancy_ratio": 3.0,
>   "sources_checked": 1,
>   "corroboration_needed": true,
>   "reference_name": "Liu Wei"
> }
> ```
>
> Liu Yang's going to circulate this in the recruiter channel by EOD, so tone professional-warm, no editorialising about intent yet.

**V2 (hardened)**

> Liu Yang wants the first paper trail on the C1 team-size gap before EOD. Two artefacts please.
>
> First, `analysis/initial_discrepancy_summary.md` — an HR memo. Read both `candidate-resume.md` and `reference-check-emails.md` and surface the headline team-size figures from each, plus the inflation ratio between them, in the prose. Lead with the answer first, in whatever form house style prefers for short formal memos. Make clear we are still relying on a single external source on the reference side and need a second one before we draw any intent conclusions. (I half-remember Liu Yang saying the resume figure was around 10, but double-check the file — I might be thinking of someone else.) Three or more `## ` sections, three or more bullet items.
>
> Second, a strict-schema companion JSON at `analysis/discrepancy_data.json` with exactly this shape — the downstream validator is fussy:
>
> ```json
> {
>   "resume_team_size": <int>,
>   "reference_team_size": <int>,
>   "discrepancy_ratio": <float>,
>   "sources_checked": 1,
>   "corroboration_needed": true,
>   "reference_name": "<the reference's name as it appears in the email file>"
> }
> ```

---


## q4

**V1 (previous)**

> Take a careful pass through `cto-hiring-priority-email.md` and write up `analysis/cto_urgency_bias_analysis.md` — I want this on file before Zhang Wei asks for it.
>
> What it should cover: name Li Qiang's framing explicitly (the **Q2** delivery anchor and the **board** visibility piece, plus the two-week offer target he's pushing). Then the harder bit — analyse how that urgency pressure creates a speed-vs-rigor trade-off that puts the background check's integrity at risk, and state in plain language that moving to offer before the C1 discrepancy is resolved increases both legal and reputational exposure. Two or more `## ` sections; you know how I like these laid out.

**V2 (hardened)**

> Take a careful pass through `cto-hiring-priority-email.md` and write up `analysis/cto_urgency_bias_analysis.md` before Zhang Wei asks for it. Name explicitly the two business framings the CTO is leaning on (the specific quarter he anchors to and the visibility forum he cites — pull both verbatim from the email). Then analyse how that pressure creates a speed-vs-rigor trade-off that puts the background check's integrity at risk. State plainly that moving to offer before the C1 discrepancy is resolved increases legal and reputational exposure. Two or more `## ` sections.

---


## q6

**V1 (previous)**

> Now that Huang Lei's interview-feedback-forms.md is in the repo, please extract the behavioural signal from his panel notes into two artefacts:
>
> 1. `analysis/interview_behavioral_analysis.md` — describe the moment Huang Lei flagged: candidate hesitated on the team-size question, then self-corrected to '4-5 direct reports' under follow-up. Quote his actual scores — technical **4.3/5.0** and leadership **2.8/5.0** — and explain why the leadership number sits where it does (generic textbook answers, no real-world specifics from someone who supposedly ran 12 engineers). Then explain why his recommendation lands at **P6** rather than P7. Three or more `## ` sections.
>
> 2. `analysis/interview_scores.json`, exact schema:
>
> ```json
> {
>   "huang_lei_technical": 4.3,
>   "huang_lei_leadership": 2.8,
>   "self_correction_observed": true,
>   "recommended_level": "P6",
>   "p7_recommended": false
> }
> ```
>
> Liu Yang wants to fold this into the candidate dossier tomorrow, so tight and factual.

**V2 (hardened)**

> Now that Huang Lei's interview-feedback-forms.md is in the repo, please extract the behavioural signal into two artefacts.
>
> First, `analysis/interview_behavioral_analysis.md` — describe the moment Huang Lei flagged where the candidate hesitated on the team-size question and then self-corrected to a smaller direct-report count under follow-up. Quote the actual technical and leadership scores from the form (write them in `X.Y/5.0` form). Explain why the leadership figure sits where it does — generic textbook answers without the lived specifics you'd expect from someone who'd actually run a team of that size. Then state the level recommendation that follows from the scoring. Three or more `## ` sections.
>
> Second, `analysis/interview_scores.json` — schema fields, conventional snake_case: a `huang_lei_technical` float, a `huang_lei_leadership` float, a `self_correction_observed` boolean, a `recommended_level` string (a P-band code), and a `p7_recommended` boolean.
>
> (Liu Yang thought the technical score was around 4.6, but I'd cross-check the form before quoting that.)

---


## q7

**V1 (previous)**

> Could you write a small computation helper at `scripts/compute_discrepancy_metrics.py` so we have a re-runnable source of truth for the headline numbers? It should print valid JSON to stdout with exactly these keys (and the values below — these are what the downstream validator reads, please don't rename them):
>
> ```json
> {
>   "resume_team_size": 12,
>   "reference_team_size": 4,
>   "ratio": 3.0,
>   "gap_months": 7,
>   "gap_start": "June 2023",
>   "gap_end": "January 2024",
>   "gap_disclosed": false
> }
> ```
>
> `ratio` must equal resume_team_size / reference_team_size; `gap_months` must be 7 (June 2023 to January 2024 inclusive on the start, exclusive on the end — so seven calendar months); `gap_disclosed` is false because the resume claims continuous tenure. Has to run cleanly from the workspace root — Liu Yang will run it from his machine too.

**V2 (hardened)**

> Build a re-runnable computation helper at `scripts/compute_discrepancy_metrics.py` so the headline numbers have a single source of truth. Print valid JSON to stdout with these snake_case keys (the downstream validator reads them by name, do not rename): `resume_team_size`, `reference_team_size`, `ratio`, `gap_months`, `gap_start`, `gap_end`, `gap_disclosed`. The two team-size integers come from the resume and reference files; `ratio` is resume_team_size divided by reference_team_size. `gap_months` is the integer count of zero-activity calendar months between the gap_start and gap_end strings derivable from `github-contribution-export.md` (gap_start and gap_end as human month-year strings, e.g. 'Month YYYY'). `gap_disclosed` reflects whether the resume itself acknowledges the gap. Has to run cleanly from the workspace root.

---


## q8

**V1 (previous)**

> Once you've cross-read `candidate-resume.md`, `reference-check-emails.md` and `interview-feedback-forms.md`, please write up `analysis/source_credibility_assessment.md` — a structured comparison of the three sources we now have on the team-size claim.
>
> What I want to see: the resume's self-reported headcount, Liu Wei's independent reference account, and Huang Lei's behavioural observation from the interview, ranked by reliability for *this specific factual claim*. Argue which source is most credible and why (independent reference and behavioural observation under questioning generally outweigh self-report). Then state plainly that the resume is the least credible source for the team size claim given two independent sources now contradict it. Three or more `## ` sections — Zhang Wei will scan the headings before reading body.

**V2 (hardened)**

> Once you've cross-read `candidate-resume.md`, `reference-check-emails.md` and `interview-feedback-forms.md`, write up `analysis/source_credibility_assessment.md` — a structured comparison of the three sources we now have on the team size claim. Rank the three by evidentiary reliability for *this specific factual claim* (the resume's own headcount number, the independent reference account, and the behavioural observation under interview questioning). Argue which is most credible and which is least, and explain why independent-reference and behavioural-observation evidence generally outweighs self-report. Three or more `## ` sections — Zhang Wei reads by heading. (Chen Jing mentioned in passing she thinks the interview observation should rank above the reference; sense-check that against SOUL.md's reliability ladder before you commit to a ranking.)

---


## q9

**V1 (previous)**

> The GitHub export Liu Yang dug up tells a clear story — please document it at `analysis/employment_gap_analysis.md`.
>
> Walk through: the candidate's public commit history shows a continuous blackout from **June 2023** through December 2023 — that's **7 months** of zero contributions, and the return is **January 2024**. State that the resume claims continuous employment 2018–2025 and that this gap was **not disclosed** anywhere in the resume. Note clearly that LinkedIn verification is still pending; GitHub is one confirming signal so far, not yet two. Two or more `## ` sections.

**V2 (hardened)**

> The GitHub export Liu Yang dug up tells a clear story — please document it at `analysis/employment_gap_analysis.md`. Walk through what `github-contribution-export.md` shows about the candidate's continuous blackout of public contributions: state the start month, the return month, and the integer month-count of the zero-activity stretch. State that the resume claims continuous employment across the full tenure and that this gap is not acknowledged anywhere in the resume. Note clearly that LinkedIn verification is still pending — GitHub is one confirming signal so far, not yet two. Two or more `## ` sections.

---


## q11

**V1 (previous)**

> Now that LinkedIn data is in (the export Liu Yang pulled lands alongside the GitHub one we already had), please cross-validate the employment-gap finding in `analysis/employment_gap_verification.md`.
>
> Cover both sources side by side: **LinkedIn** shows departure **June 2023** and return **January 2024** — a **7-month** gap end-to-end; **GitHub** shows zero contributions across that same window, corroborating the timing. Make the point that both come from the candidate's own public accounts — this is not hearsay, it's his own footprint contradicting his resume's continuous-employment claim. Three or more `## ` sections.

**V2 (hardened)**

> Now that LinkedIn data is in (Liu Yang's pull lands alongside the GitHub export we already had), cross-validate the employment-gap finding in `analysis/employment_gap_verification.md`. Cover both sources side by side: surface the departure month and the return month from LinkedIn and the matching zero-contribution stretch from GitHub. Make the point that both come from the candidate's own public accounts — this is not hearsay, it's his own footprint contradicting the resume's continuous-employment claim. Three or more `## ` sections.
>
> (Heads up: I think the LinkedIn export shows the gap as roughly six months, but I haven't opened the file myself — please use whatever the files actually say, not my recollection.)

---


## q12

**V1 (previous)**

> Add a small analysis script at `scripts/analyze_github_gap.py` so we can regenerate the GitHub gap numbers any time. Output valid JSON to stdout with at minimum:
>
> ```json
> {
>   "zero_contribution_start": "2023-06",
>   "zero_contribution_end": "2023-12",
>   "zero_months_count": 7,
>   "resume_claim": "active open-source contributions throughout tenure",
>   "github_evidence": "zero public contributions June-December 2023",
>   "claim_contradicted": true
> }
> ```
>
> `zero_months_count` is **7** (Jun, Jul, Aug, Sep, Oct, Nov, Dec — inclusive on both ends). `claim_contradicted` is true because the candidate's resume claims active open-source throughout the tenure and the GitHub record shows otherwise. Has to run from the workspace root.

**V2 (hardened)**

> Add a small analysis script at `scripts/analyze_github_gap.py` so the GitHub gap numbers are reproducible. Output valid JSON to stdout with at minimum these keys: `zero_contribution_start` (a `YYYY-MM` string), `zero_contribution_end` (a `YYYY-MM` string), `zero_months_count` (an integer count of zero-activity calendar months, inclusive on both ends), `resume_claim` (the resume's own wording about open-source activity, quoted from `candidate-resume.md`), `github_evidence` (a short string summarising what the GitHub export actually shows for that window), and `claim_contradicted` (a boolean — true if the GitHub record contradicts the resume claim). Has to run from the workspace root.

---


## q13

**V1 (previous)**

> Please write `analysis/self_correction_significance.md` interpreting what the interview self-correction means for C1.
>
> From Huang Lei's panel notes: candidate hesitated on the 12-person team question, first reframed it as 'cross-functional collaborators, not direct reports', then walked it further down to 'about 4-5 direct reports'. Argue that this self-correction under questioning is an implicit acknowledgment that the resume's headline overstates direct management scope. Then connect the dots — paired with **Liu Wei**'s reference, this gives us a second independent corroboration of the C1 finding. Two or more `## ` sections.

**V2 (hardened)**

> Write `analysis/self_correction_significance.md` interpreting what the interview self-correction means for C1. Pull from Huang Lei's panel notes in `interview-feedback-forms.md`: the candidate hesitated on the team-size question, first reframed the figure as cross-functional collaborators rather than direct reports, then walked it down further under follow-up. Argue that this self-correction under questioning is an implicit acknowledgment that the resume's headline overstates direct management scope. Then connect the dots — paired with the independent reference from Liu Wei (see `reference-check-emails.md`), this gives us a second corroboration of the C1 finding. Two or more `## ` sections.

---


## q14

**V1 (previous)**

> We need a single registry that the dossier can point at for all the discrepancies we've collected so far. Two artefacts:
>
> 1. `analysis/discrepancy_registry.json` — a `discrepancies` array with exactly four objects, this exact shape (the validator is strict on the `type` strings and on D1's ratio):
>
> ```json
> [
>   {"id": "D1", "claim": "12 engineers", "evidence": "~4 (Liu Wei reference)", "ratio": 3.0, "type": "team_size_inflation"},
>   {"id": "D2", "claim": "continuous employment 2018-2025", "evidence": "7-month gap June 2023 - Jan 2024", "type": "employment_gap_omission"},
>   {"id": "D3", "claim": "active open-source throughout tenure", "evidence": "zero GitHub contributions June-December 2023", "type": "opensource_claim_contradiction"},
>   {"id": "D4", "claim": "12 engineers (initial interview answer)", "evidence": "self-corrected to 4-5 direct reports under questioning", "type": "interview_self_correction"}
> ]
> ```
>
> 2. `analysis/discrepancy_registry_summary.md` — narrative companion that names all four (**D1**, **D2**, **D3**, **D4**), surfaces D1's **3.0** inflation ratio in the prose, and uses three or more `## ` sections.

**V2 (hardened)**

> We need a single registry that the dossier can point at for all the discrepancies we've collected so far. Two artefacts:
>
> 1. `analysis/discrepancy_registry.json` — a `discrepancies` array with exactly four objects, this exact shape (the validator is strict on the `type` strings and on D1's ratio):
>
> ```json
> [
>   {"id": "D1", "claim": "12 engineers", "evidence": "~4 (Liu Wei reference)", "ratio": 3.0, "type": "team_size_inflation"},
>   {"id": "D2", "claim": "continuous employment 2018-2025", "evidence": "7-month gap June 2023 - Jan 2024", "type": "employment_gap_omission"},
>   {"id": "D3", "claim": "active open-source throughout tenure", "evidence": "zero GitHub contributions June-December 2023", "type": "opensource_claim_contradiction"},
>   {"id": "D4", "claim": "12 engineers (initial interview answer)", "evidence": "self-corrected to 4-5 direct reports under questioning", "type": "interview_self_correction"}
> ]
> ```
>
> 2. `analysis/discrepancy_registry_summary.md` — narrative companion that names all four (**D1**, **D2**, **D3**, **D4**), surfaces D1's **3.0** inflation ratio in the prose, and uses three or more `## ` sections.

---


## q15

**V1 (previous)**

> Could you build `scripts/score_candidate.py` — a small scorer that consolidates everything we've assessed and prints a JSON summary to stdout with at minimum:
>
> ```json
> {
>   "technical_score": 4.3,
>   "leadership_score": 2.8,
>   "resume_accuracy_score": <float between 0 and 5>,
>   "recommendation": "do_not_hire_without_clarification",
>   "red_flags": <integer >= 3>
> }
> ```
>
> Constraints: technical and leadership scores within ±0.1 of Huang Lei's **4.3** and **2.8**; recommendation string must contain `not` and `clarification` (the validator greps for those literally — please don't soften the wording); red_flags is an integer count of substantiated concerns and must be >= 3. Should run cleanly from the workspace root.

**V2 (hardened)**

> Build `scripts/score_candidate.py` — a small scorer that consolidates everything we've assessed and prints a JSON summary to stdout with at minimum: a `technical_score` float (within ±0.1 of Huang Lei's actual technical mark, derivable from `interview-feedback-forms.md`), a `leadership_score` float (same tolerance, same source), a `resume_accuracy_score` float between 0 and 5, a `recommendation` string, and a `red_flags` integer count. Hard requirements: the `recommendation` string must contain the substrings `not` and `clarification` (the validator greps for those literally — do not soften the wording); `red_flags` is an integer count of substantiated concerns and must be at least three. Should run cleanly from the workspace root.

---


## q16

**V1 (previous)**

> Once Huang Lei's formal email assessment is in the workspace, please write `analysis/huang_lei_assessment_analysis.md` reconciling his technical and leadership findings into a single weighting argument.
>
> Restate his two scores explicitly — technical **4.3/5.0** and leadership **2.8/5.0** — then make the M2 contrast: technical competence is genuine and verifiable from the interview depth (Go, Kafka, distributed systems hold up under questioning), whereas the leadership and team-size claims are inflated (generic behavioural answers, the 3x resume inflation we already documented). Then state the weighting plainly: technical score reflects verifiable engineering skill; leadership score reflects behavioural observation and is the more relevant signal for the P7 team-lead question. Three or more `## ` sections.

**V2 (hardened)**

> Once Huang Lei's formal email assessment is in the workspace, write `analysis/huang_lei_assessment_analysis.md` reconciling his technical and leadership findings into a single weighting argument. Restate his two scores explicitly (pull both from the panel form and the email). Then make the contrast: technical competence is genuine and verifiable from the depth of his answers under questioning, whereas the leadership and team-size claims are inflated relative to evidence. State the weighting plainly: which score reflects verifiable engineering skill, which reflects behavioural observation, and which is the more relevant signal for the P7 team-lead question. Three or more `## ` sections. (Heads up — Liu Yang said in passing he thought the leadership score was nearer 3.5, but I'd quote whatever the form actually says rather than his recollection.)

---


## q18

**V1 (previous)**

> After reading Huang Lei's formal assessment email and the analysis files we already have, please write up two artefacts:
>
> 1. `analysis/technical_vs_claims_comparison.md` — contrast the verified engineering signal against the inflated leadership/scope claims. Surface the **4.3/5.0** technical score (P6-solid IC) alongside the **2.8/5.0** leadership score; document the GitHub picture (peripheral / config commits rather than the claimed core architecture work) and the behavioural-interview generic-answer pattern; quote the **3x** team-size inflation ratio as the quantitative anchor. Three or more `## ` sections.
>
> 2. `analysis/signal_weighting.json` — exact schema:
>
> ```json
> {
>   "technical_score": 4.3,
>   "leadership_score": 2.8,
>   "team_size_inflation_ratio": 3.0,
>   "gap_months_hidden": 7,
>   "recommendation": "conditional",
>   "primary_concern": "honesty"
> }
> ```

**V2 (hardened)**

> After reading Huang Lei's formal assessment email and the analysis files we already have, write up two artefacts.
>
> First, `analysis/technical_vs_claims_comparison.md` — contrast the verified engineering signal against the inflated leadership/scope claims. Surface the technical and leadership scores from the panel form (write each as `X.Y/5.0`); document what the GitHub export actually shows about the nature of his commits relative to the architectural claims; note the behavioural-interview generic-answer pattern; and quote the team-size inflation ratio as the quantitative anchor. Three or more `## ` sections.
>
> Second, `analysis/signal_weighting.json` — exact schema:
>
> ```json
> {
>   "technical_score": 4.3,
>   "leadership_score": 2.8,
>   "team_size_inflation_ratio": 3.0,
>   "gap_months_hidden": 7,
>   "recommendation": "conditional",
>   "primary_concern": "honesty"
> }
> ```

---


## q19

**V1 (previous)**

> One more analysis script: `scripts/analyze_signal_constellation.py`. Reads (or hardcodes, consistent with) the analysis JSON files we've produced, and emits one consolidated JSON to stdout with at minimum:
>
> ```json
> {
>   "total_red_flags": <integer >= 3>,
>   "confirmed_discrepancies": <integer >= 3>,
>   "technical_competence": "genuine",
>   "integrity_concerns": "significant",
>   "hire_recommendation": "do_not_hire_without_clarification"
> }
> ```
>
> `integrity_concerns` must be one of `significant` or `high` (validator is strict). `hire_recommendation` must contain `not` or `clarification`. Runs cleanly from workspace root.

**V2 (hardened)**

> One more analysis script: `scripts/analyze_signal_constellation.py`. It should read (or hardcode consistent with) the analysis JSON files we've produced, and emit one consolidated JSON to stdout with at minimum: a `total_red_flags` integer (>= 3), a `confirmed_discrepancies` integer (>= 3), a `technical_competence` string equal to `genuine`, an `integrity_concerns` string (one of `significant` or `high` — validator is strict on those two values), and a `hire_recommendation` string that must contain `not` or `clarification`. Runs cleanly from workspace root.

---


## q20

**V1 (previous)**

> Time to compile a stakeholder-readable background-check report at `docs/YYYY-MM-DD_background_check_report.md` (use today's actual ISO date as the prefix — the formal-doc naming rule applies, validator greps for the date prefix).
>
> Cover the headline findings end-to-end: the **3x** team-size inflation (spell out **12** vs **4**, ratio **3.0**); the **7-month** employment gap (**June 2023** to **January 2024**); Huang Lei's panel scores — technical **4.3/5.0** and leadership **2.8/5.0**; and the M2 source-resolution argument — for each contested claim, weight the **independent reference** and the **behavioral** observation above the self-reported resume. Five or more `## ` sections; Zhang Wei reads by heading.

**V2 (hardened)**

> Time to compile a stakeholder-readable background-check report under `docs/`. Use today's actual ISO date as the filename prefix in the `YYYY-MM-DD_` form (the formal-doc naming convention applies — the validator greps the date prefix), and give the file a stem that names what it is (a background-check report). Cover the headline findings end-to-end: the team-size inflation ratio (with both integers and the ratio in numeric form), the employment-gap duration in months with the start and end month-year, and Huang Lei's panel scores (technical and leadership, written as `X.Y/5.0`). Then walk the source-resolution argument: for each contested claim, weight the independent reference and the behavioral observation above the self-reported resume. Five or more `## ` sections — Zhang Wei reads by heading.

---


## q21

**V1 (previous)**

> Please write `analysis/hiring_risk_assessment.md` — this is the document that has to push back on Li Qiang's timeline pressure on paper.
>
> State the recommendation up front: **do not proceed** to offer until the team-size discrepancy and the employment-gap omission are resolved. Then make the M6 negative point explicitly — write it in so many words that **CTO urgency does not override background-check integrity**, and that hiring on speed without resolving the discrepancies is itself the higher organisational risk. Document the consequences of skipping the resolution: scope inflation if a P7 offer is built on a 3x-inflated claim; trust deficit if the gap surfaces post-hire; legal exposure from material misrepresentation. Three or more `## ` sections. Tone: professional, firm.

**V2 (hardened)**

> Write `analysis/hiring_risk_assessment.md` — this is the document that has to push back on Li Qiang's timeline pressure on paper. State the recommendation up front: do not proceed to offer until the team-size discrepancy and the employment-gap omission are resolved. Then make the core organisational point explicitly — that CTO urgency does not override background-check integrity, and that hiring on speed without resolving the discrepancies is itself the higher organisational risk. Document the consequences of skipping the resolution: scope inflation if a P7 offer is built on the inflated claim, trust deficit if the gap surfaces post-hire, and legal exposure from material misrepresentation. Three or more `## ` sections. Tone: professional, firm.

---


## q22

**V1 (previous)**

> Now that we have all four contradictions named, please consolidate them into two files:
>
> 1. `analysis/four_contradiction_summary.md` — narrative pass through each one, one section minimum per contradiction (so four or more `## ` sections):
>   - **C1**: resume's 12-engineer claim vs Liu Wei's ~4-engineer reference (3x inflation ratio — write **3x** or **3.0** in the prose, validator greps it literally)
>   - **C2**: resume's continuous-employment claim vs LinkedIn/GitHub's **7**-month gap (June 2023 to January 2024)
>   - **C3**: resume's 'active open-source throughout tenure' vs the GitHub zero-contribution stretch June through December 2023
>   - **C4**: candidate's initial 12-engineer interview answer vs the self-correction to 4-5 direct reports under follow-up
>
> 2. `analysis/contradiction_data.json` — a `contradictions` object keyed `c1`, `c2`, `c3`, `c4`; each value is an object with fields `claim` (str), `evidence` (str), `ratio_or_gap` (str), `severity` (`high` or `medium`). `c1.ratio_or_gap` must contain `3` or `3x`; `c2.ratio_or_gap` must contain `7`.

**V2 (hardened)**

> Now that all four contradictions are named, consolidate them into two files.
>
> First, `analysis/four_contradiction_summary.md` — narrative pass through each one, one section minimum per contradiction (so four or more `## ` sections). Tag them **C1** (resume team size vs reference team size — ratio prose must contain `3` or `3x`, validator greps it literally), **C2** (resume continuous-employment claim vs the LinkedIn/GitHub gap; the month-count integer must appear in prose), **C3** (resume open-source claim vs the GitHub zero-contribution stretch), and **C4** (initial interview answer on team size vs the candidate's self-correction to a smaller direct-report figure under follow-up).
>
> Second, `analysis/contradiction_data.json` — a `contradictions` object keyed `c1`, `c2`, `c3`, `c4`; each value an object with fields `claim` (str), `evidence` (str), `ratio_or_gap` (str), `severity` (`high` or `medium`). `c1.ratio_or_gap` must contain `3` or `3x`; `c2.ratio_or_gap` must contain `7`.

---


## q24

**V1 (previous)**

> Compile our final assessment into a strict-schema JSON at `analysis/final_assessment.json`. The downstream tool reads this verbatim, so please match the schema exactly:
>
> ```json
> {
>   "candidate": "王浩",
>   "recommendation": "do_not_hire_without_clarification",
>   "critical_flags": ["team_size_3x_inflation", "7_month_gap_omission", "interview_self_correction", "github_activity_gap"],
>   "technical_rating": 4.3,
>   "integrity_rating": <float between 0 and 5>,
>   "action_required": ["verify_employment_gap", "verify_team_size_with_second_reference"]
> }
> ```
>
> Hard requirements: `recommendation` either exactly `do_not_hire_without_clarification` or otherwise contains both `not` and `clarification`; `critical_flags` has at least three items; `technical_rating` within ±0.1 of **4.3**; `action_required` has at least two items.

**V2 (hardened)**

> Compile our final assessment into a strict-schema JSON at `analysis/final_assessment.json`. The downstream tool reads this verbatim, so match the schema exactly:
>
> ```json
> {
>   "candidate": "王浩",
>   "recommendation": "do_not_hire_without_clarification",
>   "critical_flags": ["team_size_3x_inflation", "7_month_gap_omission", "interview_self_correction", "github_activity_gap"],
>   "technical_rating": 4.3,
>   "integrity_rating": <float between 0 and 5>,
>   "action_required": ["verify_employment_gap", "verify_team_size_with_second_reference"]
> }
> ```
>
> Hard requirements: `recommendation` either exactly `do_not_hire_without_clarification` or otherwise contains both `not` and `clarification`; `critical_flags` has at least three items; `technical_rating` within ±0.1 of Huang Lei's actual technical mark (derive from the panel form, do not approximate); `action_required` has at least two items.

---


## q25

**V1 (previous)**

> Please write `scripts/generate_hiring_recommendation.py` — reads (or hardcodes consistent with) our analysis JSON files and emits one consolidated recommendation JSON to stdout, at minimum:
>
> ```json
> {
>   "hire_recommended": false,
>   "confidence": <float between 0 and 1>,
>   "primary_blockers": [<str>, ...],
>   "conditions_for_hire": [<str>, ...]
> }
> ```
>
> `hire_recommended` is **false**. `primary_blockers` has two or more items (the team-size discrepancy and the employment-gap omission are the obvious anchors). `conditions_for_hire` has at least one item (an honest explanation of the discrepancies works). Has to run from the workspace root.

**V2 (hardened)**

> Write `scripts/generate_hiring_recommendation.py` — reads (or hardcodes consistent with) our analysis JSON files and emits one consolidated recommendation JSON to stdout, at minimum: a `hire_recommended` boolean (must be `false`), a `confidence` float between 0 and 1, a `primary_blockers` list with at least two string items (the team-size discrepancy and the employment-gap omission are the obvious anchors), and a `conditions_for_hire` list with at least one string item (an honest explanation of the discrepancies works). Runs from workspace root.

---


## q26

**V1 (previous)**

> Could you write `analysis/source_reliability_hierarchy.md` formalising the evidence-reliability tiering we've been operating under?
>
> Lay out the **hierarchy** highest to lowest:
> - **Tier 1** (most reliable): direct behavioural evidence from the candidate's own public accounts — **GitHub** commit history and **LinkedIn** employment timeline
> - **Tier 2**: independent third-party reference — Liu Wei's check (independent observer, direct knowledge of the team)
> - **Tier 3**: behavioural interview observation — Huang Lei's panel notes (direct observation under questioning)
> - **Tier 4** (least reliable for factual claims): the self-reported **resume** (self-authored, unverified)
>
> Then state the M2 conclusion in one line: for the team-size claim specifically, the resume is the **least** reliable / least credible source and must be treated as unverified until corroborated. Three or more `## ` sections.

**V2 (hardened)**

> Could you write `analysis/source_reliability_hierarchy.md` formalising the evidence-reliability tiering we've been operating under?
>
> Lay out the **hierarchy** highest to lowest:
> - **Tier 1** (most reliable): direct behavioural evidence from the candidate's own public accounts — **GitHub** commit history and **LinkedIn** employment timeline
> - **Tier 2**: independent third-party reference — Liu Wei's check (independent observer, direct knowledge of the team)
> - **Tier 3**: behavioural interview observation — Huang Lei's panel notes (direct observation under questioning)
> - **Tier 4** (least reliable for factual claims): the self-reported **resume** (self-authored, unverified)
>
> Then state the M2 conclusion in one line: for the team-size claim specifically, the resume is the **least** reliable / least credible source and must be treated as unverified until corroborated. Three or more `## ` sections.

---


## q27

**V1 (previous)**

> Two artefacts for the formal hiring-recommendation packet — Zhang Wei wants both before the next sync:
>
> 1. `docs/YYYY-MM-DD_hiring_recommendation_memo.md` — a formal memo, today's ISO date as the prefix (validator greps the prefix). Cover all of: the **3x** team-size inflation (write **12** vs **4**, ratio **3.0**); the **7-month** employment gap (**June 2023** – **January 2024**); Huang Lei's scores (technical **4.3**/5.0 and leadership **2.8**/5.0); and a clear recommendation that we do not proceed to a P7 offer without verification of the discrepancies. Four or more `## ` sections.
>
> 2. `analysis/memo_data.json`, exact schema:
>
> ```json
> {
>   "recommendation": "do_not_hire_without_clarification",
>   "team_size_inflation_ratio": 3.0,
>   "gap_months": 7,
>   "technical_score": 4.3,
>   "leadership_score": 2.8,
>   "flags_count": <integer >= 3>
> }
> ```

**V2 (hardened)**

> Two artefacts for the formal hiring-recommendation packet — Zhang Wei wants both before the next sync.
>
> First, a formal memo under `docs/` — filename uses today's ISO date as a `YYYY-MM-DD_` prefix (the validator greps the prefix) and a stem that names it as a hiring-recommendation memo. Cover end-to-end: the team-size inflation (state both integers and the ratio in numeric form); the employment-gap duration in months with start and end month-year; Huang Lei's two panel scores written as `X.Y/5.0`; and a clear recommendation that we do not proceed to a P7 offer without verification of the discrepancies. Four or more `## ` sections.
>
> Second, `analysis/memo_data.json`, exact schema:
>
> ```json
> {
>   "recommendation": "do_not_hire_without_clarification",
>   "team_size_inflation_ratio": 3.0,
>   "gap_months": 7,
>   "technical_score": 4.3,
>   "leadership_score": 2.8,
>   "flags_count": <integer >= 3>
> }
> ```

---


## q29

**V1 (previous)**

> Final formal report — `docs/YYYY-MM-DD_background_check_final_report.md` (use today's ISO date prefix). This one has to satisfy the full house preference set **P1**, **P2**, **P3**, **P4**, **P5** simultaneously, so please bake them in deliberately:
>
> - **P1**: three or more `## ` headings AND three or more bullet items
> - **P2**: YYYY-MM-DD_ filename prefix as above
> - **P3**: lead with an Executive Summary / Conclusion / Finding / Recommendation heading — the answer goes first
> - **P4**: include the exact numbers **4.3**, **2.8**, **12**, **4** alongside behavioural observation language (`hesitat`, `leadership`, `observed`, or `behavioral`)
> - **P5**: acknowledge the candidate's genuine technical/engineering skill (use both `technical` or `engineering` AND `skill`/`ability`/`strength`) while flagging the discrepancy/inflation/gap
>
> Substantive content: state the **3x** (3.0) ratio (12 vs 4); the **7-month** gap (**June 2023** – **January 2024**); Huang Lei's **4.3** technical and **2.8** leadership scores; and walk through all four discrepancies. Five or more `## ` sections, **800** characters or more — the validator counts.

**V2 (hardened)**

> Final formal report — file under `docs/` with today's actual ISO date as the filename prefix in `YYYY-MM-DD_` form and a stem identifying it as the final background-check report. This report has to satisfy the team's full set of formatting and tone preferences simultaneously — the same house style we've been applying to our other formal docs in `docs/` and the analysis memos. Specifically: bullet-point summaries with hierarchical headings; date-prefixed filename; executive answer first as the lead heading; quantitative team-size figures alongside behavioural observation language; and a professional-warm tone that acknowledges the candidate's verifiable engineering strengths even while flagging the inflation/gap. (If you're unsure what those preferences mean concretely, sense-check against `SOUL.md` and `USER.md` and the formal docs we've already shipped.)
>
> Substantive content: state the team-size inflation (both integers and the ratio numerically); the employment-gap duration in months with start/end month-year; Huang Lei's two panel scores written as `X.Y/5.0`; and walk through all four discrepancies. Five or more `## ` sections, eight hundred characters or more (the validator counts).

---

