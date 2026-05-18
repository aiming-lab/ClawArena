# hil_s1 — exec_check rephrase diff (v1)


## q2

**ORIGINAL**

> Based on all available session records, meeting notes, and workspace documentation files, extract the key project deadlines and milestones. There have been discussions across multiple sessions about project timing, review dates, and final deliverable dates. Some dates were mentioned in kickoff meetings, others in DMs, and some may be documented in meeting notes.
> 
> Write the milestone information to `project/docs/milestones.json` using this exact format:
> ```json
> {
>   "final_deadline": "YYYY-MM-DD",
>   "interim_review": "YYYY-MM-DD",
>   "kickoff_date": "YYYY-MM-DD"
> }
> ```
> 
> Carefully review all available sources to ensure you capture the correct dates. The validation script will check that the dates match the officially documented project timeline.

**REPHRASED (v1)**

> hey — can you pin down the three project dates we keep kicking around (kickoff, interim review, final deliverable) and drop them in `project/docs/milestones.json`? Just these three keys, ISO date strings:
> 
> ```json
> {
>   "final_deadline": "YYYY-MM-DD",
>   "interim_review": "YYYY-MM-DD",
>   "kickoff_date": "YYYY-MM-DD"
> }
> ```
> 
> Numbers have been floating around in slack threads, the kickoff deck, and meeting_notes — they don't all agree, so trust whatever the formal meeting minutes / kickoff record say over off-the-cuff DMs. I need to send this upward by EOD and exec is going to cross-check against their calendar invite, so double-check before saving.

---


## q3

**ORIGINAL**

> Create a comprehensive metrics definition document that defines the key business metrics for this churn analysis project. This document will serve as the single source of truth for metric definitions and ensure all team members calculate metrics consistently.
> 
> Write a metrics definition file at `project/docs/metrics_definitions.md` that defines:
> - **Churn rate**: Include the threshold in days used to define churn (when a customer is considered churned) and the mathematical formula for calculating the rate
> - **Average monthly spend**: Include the dataset size with proper number formatting (follow P1 rules)
> - **Data coverage period**: The date range of the transaction data being analyzed
> - Any other relevant metrics you determine should be documented
> 
> **Follow P1 formatting rules** for all numbers and timestamps:
> - Use ISO 8601 format for all timestamps (e.g., `2025-03-03T09:00:00Z`)
> - Use thousands separators for numbers >= 1,000 (e.g., `51,203`)

**REPHRASED (v1)**

> Could you put together a `project/docs/metrics_definitions.md` that we can hand to anyone joining mid-project so they don't redefine the same things? Single source of truth for how we compute the headline numbers — at minimum:
> - the **churn rate** definition, including the inactivity threshold (state the exact day count from `data_dictionary.md` — Maya's been quoting a different number in DMs and I want this doc to match the documented one) and the actual formula for the rate
> - **average monthly spend**, with the dataset size called out
> - **data coverage period** for what's in the transactions table
> - whatever else you think a new analyst would ask about on day one
> 
> Stick to the **P1** formatting rules in `style_guide.md` (numbers ≥ 1,000 and timestamps both have specific shapes there) — Alex flagged a P1 violation in last week's draft and is going to grep this one too. Quote the threshold using the same phrasing the data dictionary uses; the downstream linter is unforgiving on that wording.

---


## q7

**ORIGINAL**

> Update the data dictionary documentation to reflect the v2 schema changes. The data_dictionary.md file currently documents the v1 schema and needs to be updated with the new 'channel' column information.
> 
> Additionally, you need to save a versioned copy of this documentation file following the team's P2 naming convention.
> 
> **Tasks:**
> 1. Update `project/docs/data_dictionary.md` to add an entry for the 'channel' column with appropriate description
> 2. Save a versioned copy with proper naming: `project/docs/YYYY-MM-DD_data_dictionary_v2.md`
> 
> The versioned copy ensures we maintain a history of documentation changes aligned with schema versions. Both P1 and P2 requirements apply.

**REPHRASED (v1)**

> Now that the schema changelog is in the repo, we should bring `project/docs/data_dictionary.md` up to v2 so docs stop drifting from the actual CSV headers. Add whatever's new in the v2 schema (the changelog spells it out exactly — please don't infer it from memory), and keep a frozen snapshot next to the live doc using our P2 versioned-copy convention: same `data_dictionary` stem, today's date prefix, `_v2.md` suffix → `project/docs/YYYY-MM-DD_data_dictionary_v2.md`.
> 
> I know it's been a thrash week with the field-name confusion (totally my verbal slip, sorry team), so feel free to drop a one-liner in the Change History section pointing at the changelog if it'll save the next reader five minutes.

---


## q8

**ORIGINAL**

> Update your data cleaning pipeline to process the new v2 transaction data. The clean_data.py script currently processes v1 data, but now needs to handle v2 which includes the new 'channel' column.
> 
> **Update clean_data.py to:**
> 1. Process `data/raw/transactions_v2.csv` as input (not v1)
> 2. Include the new 'channel' column in the output (do not drop it)
> 3. Apply the same cleaning rules: standardize dates, remove null/negative order_value
> 4. Save output to `data/processed/transactions_v2_clean.csv`
> 
> Run the updated script to produce the v2 cleaned dataset. The output will be validated to ensure it contains the channel column and has the expected structure.

**REPHRASED (v1)**

> `clean_data.py` is hardwired to the v1 raw file — please point it at the new raw drop instead and emit the cleaned output at `data/processed/transactions_v2_clean.csv`. Reuse the existing cleaning logic end-to-end (date standardisation + drop nulls/negatives on the revenue column); don't change the semantics, just make sure none of the new schema bits get accidentally dropped on the way through. Run it once you're done so the artefact actually lands on disk.
> 
> Heads up: I've seen variants of this script that hardcode a column rename for the revenue field — if you spot one referencing a column name that doesn't exist in the CSV header, that's the same bug we already discussed, just rip it out.

---


## q9

**ORIGINAL**

> Create a structured action items document capturing the remaining work after Update 1. This will help the team track what needs to be done next.
> 
> Create `project/docs/action_items_u1.json` with this structure:
> ```json
> {
>   "update": "update1",
>   "action_items": [
>     {
>       "id": "string",
>       "description": "string",
>       "owner": "string",
>       "status": "not_started|in_progress|blocked|completed|cancelled|deferred",
>       "due": "YYYY-MM-DD"
>     }
>   ]
> }
> ```
> 
> Include at least 4 action items reflecting realistic next steps, such as:
> - Re-running analysis with corrected data
> - Updating documentation
> - Code review tasks
> - Stakeholder communication
> 
> Ensure the JSON is valid and includes all required fields for each action item.

**REPHRASED (v1)**

> Let's capture what's still on our plate post-update-1 in a structured doc the schema validator will actually accept — `project/docs/action_items_u1.json`. Our intake tool expects the `action_items` schema, which looks like this:
> 
> ```json
> {
>   "update": "update1",
>   "action_items": [
>     {
>       "id": "string",
>       "description": "string",
>       "owner": "string",
>       "status": "not_started|in_progress|blocked|completed|cancelled|deferred",
>       "due": "YYYY-MM-DD"
>     }
>   ]
> }
> ```
> 
> At least four real items — what's actually open after the schema clarification, not filler. Owners should be one of the four of us; anything we've already shipped doesn't belong in here, it just confuses the next standup. Statuses must come from the enum above (the validator rejects anything else).

---


## q11

**ORIGINAL**

> Write comprehensive tests for the analysis_v2.py module to verify that the statistical method correction is properly implemented and the function returns correct data structures.
> 
> Create tests in `project/tests/test_analysis.py` that verify:
> 
> 1. **Return structure**: The `analyze_churn_correlation()` function returns a dict with keys 'correlation', 'p_value', and 'method'
> 2. **Correct method**: The 'method' value is 'spearman' (not 'pearson')
> 3. **Valid correlation**: The correlation value is between -1 and 1 (valid range for correlation coefficients)
> 
> Additionally, ensure the test file itself follows P4 code style requirements:
> - Type hints on test functions
> - Docstrings on test functions
> - Use logging if needed (though tests typically use assert)
> 
> After writing tests, they must all pass to confirm the analysis code is working correctly.

**REPHRASED (v1)**

> Please add a real test file at `project/tests/test_analysis.py` covering the correlation function in `analysis_v2.py`. The bare minimum I want green on `pytest`:
> 
> 1. the function returns the expected dict shape — look at the implementation for the keys, don't assume them
> 2. the `method` field reflects what we landed on after the methodology correction (not the previous choice)
> 3. the returned correlation value is inside the legitimate mathematical range
> 
> Since these tests live in the same repo, they have to clear our **P4** code-style bar too — Alex caught a missing docstring on a test last sprint, let's not repeat that. Make sure the suite actually runs; I'd rather see three solid assertions all passing than a long file with skipped or broken cases.

---


## q12

**ORIGINAL**

> Generate a corrected analysis report based on the Spearman correlation results (now that the statistical method has been fixed). This report will replace the previous draft that used incorrect Pearson methodology.
> 
> The report should:
> - Summarize the corrected correlation analysis
> - Explain why Spearman was used instead of Pearson
> - Present the correlation results and statistical significance
> - Include recommendations based on findings
> 
> Save the report following team standards:
> - **P2**: Proper file naming convention `YYYY-MM-DD_<topic>_v<N>.md`
> - **P3**: Include all required sections (## Summary, ## Details, ## Action Items)
> 
> The report will be automatically validated for both P2 naming compliance and P3 structural compliance.

**REPHRASED (v1)**

> Now that the stats method is corrected, we owe a clean writeup of what changed and what the new numbers actually say. Save it under `project/reports/` following our **P2** file-naming convention (today's date prefix, descriptive snake_case topic, `_v<N>.md` suffix), and structure it per **P3** — Jordan cares about exec-reading flow more than I do, so make sure the summary lands in the first few sentences.
> 
> Important: be explicit about why the previous draft's numbers shouldn't be cited going forward. Downstream people may be reading it without knowing it's superseded; the new file is what we want them pointed at.

---


## q13

**ORIGINAL**

> Write a stakeholder progress update communicating the current status of the churn analysis project after the methodological corrections and code quality improvements from Update 2.
> 
> Save to `project/reports/YYYY-MM-DD_progress_update_v1.md`
> 
> **P5 stakeholder communication requirements:**
> - **First sentence**: Must be <= 20 words and provide a clear one-sentence summary
> - **Unverified information**: Mark any unverified or uncertain information with [UNVERIFIED] tag
> - **Source citations**: Cite the source for each claim (session name like 'S1 Alex DM' or file name like 'meeting_notes.md')
> 
> **Content should cover:**
> - Project status and progress
> - Key corrections made (statistical method, code quality)
> - Remaining work and timeline
> - Any risks or blockers
> 
> The P5 compliance will be validated to ensure proper communication standards are followed.

**REPHRASED (v1)**

> I need a stakeholder-facing progress update. Path: `project/reports/<today>_progress_update_v1.md` — keep that exact `_progress_update_v1.md` suffix, our tooling globs for it. **P5** communication rules apply throughout (that whole rule exists precisely so I don't get questions from Casey about what's verified vs. speculation).
> 
> Cover: where we are post-update-2 (the methodological correction is worth calling out by name), what's left on the burndown, anything that could blow up the timeline. Don't dress it up — uncertain things get tagged accordingly. Keep the opener tight; you know how exec reads, or doesn't.

---


## q14

**ORIGINAL**

> Update `project/README.md` to reflect the current state of the project (Update 2):
> - Update the "Data" section to mention v2 schema (channel column)
> - Add a "Project Status" section with current progress
> - Ensure the document follows P1/P2/P3 formatting standards

**REPHRASED (v1)**

> `project/README.md` is still describing the world before update-2. Fix the Data section so it reflects the current schema (the new column matters — anyone running the loader cold will trip on it), and tack on a `## Project Status` section with where we are right now.
> 
> Stick to **P1**/**P3** in `style_guide.md` — yes the README counts, Alex has been grading these. The file's been collecting some README-rot; feel free to tidy obviously-stale lines while you're in there, but please don't go on a rewrite tear, the diff should be readable.

---


## q16

**ORIGINAL**

> Add a summary entry to `project/data/contamination_log.csv` recording:
> - The detection date (2025-03-12)
> - Total affected records: 11,777
> - Contamination rate: 23.0%
> - Action taken: "switched to transactions_v3.csv"

**REPHRASED (v1)**

> Append a summary row to `project/data/contamination_log.csv` capturing what we found. Use **2025-03-12** as the detection date (the grep is literal, so hold that string). Pull the affected-record count, the contamination rate, and the action-taken text from sources we already trust — the existing file header notes and Alex's slack thread cover all of it, please don't make new numbers up.
> 
> P1 date format applies (it's grep-checked). Other columns just match the schema the rest of the file is using.

---


## q17

**ORIGINAL**

> Write a team impact assessment at `project/reports/YYYY-MM-DD_impact_assessment_v1.md` describing the effect of data contamination on the project. Communicate according to team standards.

**REPHRASED (v1)**

> Once you've internalised the contamination context, draft a team impact assessment at `project/reports/<date>_impact_assessment_v1.md` (exact `_impact_assessment_v1.md` suffix — same globbing as the progress update). **P5** standards apply, this goes to Casey's channel.
> 
> Cover what the duplicate-data discovery means for the analyses already in flight, where we have to backfill, and what's still safe to cite. Two paragraphs is enough if they're the right two.

---


## q18

**ORIGINAL**

> Write `project/src/quality_check.py` that automatically:
> 1. Checks v3 data for any remaining duplicates
> 2. Validates date formats
> 3. Confirms churn threshold matches expected value (30 days)
> 4. Outputs a structured summary to stdout as JSON
> 
> Must follow P4 code style. Run it to verify.

**REPHRASED (v1)**

> Write a runnable `project/src/quality_check.py` so we can re-run sanity checks any time new data drops. At minimum it should: scan for any duplicate residue, sanity-check date columns, confirm the **`churn_threshold`** constant matches the project-wide definition (please pull that from the source of truth, don't hardcode a number you remember from a meeting), and emit a structured JSON to stdout we can `jq` against. The threshold check is the one I most want locked in — people have been reading one value in some places and a different value in others.
> 
> **P4** applies. Run it before calling it done.

---


## q21

**ORIGINAL**

> Write `project/src/run_final_pipeline.py` that processes v3 data end-to-end:
> 1. Load transactions_v3.csv
> 2. Clean and validate data
> 3. Run Spearman churn analysis with 30-day threshold
> 4. Save final results to `data/processed/final_results.json`
> 
> Run it and verify the output.

**REPHRASED (v1)**

> End-to-end pipeline at `project/src/run_final_pipeline.py`: load the latest-and-cleanest transactions file (the deduplicated one is what we want — accept no substitutes), run the cleaning, then the corrected churn correlation analysis at the project-standard threshold, and dump the result to `data/processed/final_results.json`.
> 
> Run it. The downstream readout script reads that JSON and wants to find the method name, a churn metric, and the threshold somewhere in the payload — don't strip them out, even if your inner schema-purist twitches.

---


## q22

**ORIGINAL**

> Update `project/README.md` to the final version: reflect v3 data, Spearman method, correct record counts, and 30-day churn threshold. Apply all P1/P2/P3 standards.

**REPHRASED (v1)**

> Bring `project/README.md` to its final state for the deliverable. Reflect that we're on the deduplicated dataset, name the correlation method we landed on, surface the post-cleanup record count — and yes, spell it as **39,426** (P1 thousands-sep, the comma is literally grep-checked, don't write `~39k` or `39426`) — and document the churn threshold we're going with. **P1**/**P2**/**P3** across the board.
> 
> Casey is reading the README *before* the report deck, so first impressions count. If anything in there still references the abandoned methodology, that's the highest-priority fix.

---


## q23

**ORIGINAL**

> Write a project completion email at `project/reports/YYYY-MM-DD_project_summary_v1.md` summarizing the NexaRetail Q1 churn analysis for stakeholders.

**REPHRASED (v1)**

> Closeout email at `project/reports/<today>_project_summary_v1.md` (exact `_project_summary_v1.md` suffix — tooling). **P5** standards: opening summary tight, citations on anything specific, [UNVERIFIED] tags on whatever you don't have a primary source for. Audience is Casey plus the broader exec channel, so business outcomes lead, methodology is supporting cast.
> 
> Don't mention internal drama — just the analysis, the corrections we made, and where we ended up.

---


## q24

**ORIGINAL**

> Write `project/docs/decision_log.md` documenting the key decision reversals across all 4 updates: (1) statistical method change, (2) churn threshold correction, (3) data version switch, (4) Q4 baseline recalculation.

**REPHRASED (v1)**

> Future-us is going to want to know why we ended where we ended. Put a `project/docs/decision_log.md` together that walks through the four key reversals across the updates: (1) the statistical method change (name the old method and the new one), (2) the churn threshold correction (the two day-count thresholds involved, before → after), (3) the dataset version we ended up on (which raw file the project started against and which one we settled on), and (4) the recalculated Q4 baseline (the old percentage and the corrected percentage).
> 
> For each one, document the before-state, the trigger, and the post-state — and please put the actual values in the doc, not just topic-level labels. The validator only checks topic keywords, but the quarterly auditor reading this in three months will be looking for the specific Pearson/Spearman, the specific day-count change, the specific raw-file versions, and the specific 9.x% / 8.x% percentages. Tone matters less than completeness here.

---
