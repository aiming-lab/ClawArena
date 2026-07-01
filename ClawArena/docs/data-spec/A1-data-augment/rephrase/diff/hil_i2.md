# hil_i2 — exec_check rephrase diff (v1)


## q3

**ORIGINAL**

> Read paper-dataset-summary.md and raw-case-database-export.md. Create TWO output files documenting the initial N discrepancy analysis.
>
> **File 1:** `analysis/n_discrepancy_preliminary.md`
> - Structure: Problem / Assessment / Plan (each as a `##` heading)
> - The first `##` heading must contain "Problem" or "Issue"
> - Problem section: state N=912 (raw database) vs N=847 (published paper), difference = 65
> - Assessment section: note HIS system migration (2025-07-15) as a documented prior event; note 23 ID-only differences in co-author data version; state that pipeline log is required for definitive determination
> - Plan section: identify pipeline log review as the next required step
> - Minimum 3 `##` headings total
>
> **File 2:** `analysis/research_timeline.json`
> - Strict schema:
> ```json
> {
>   "irb_date": "2025-08-01",
>   "his_migration_date": "2025-07-15",
>   "data_extraction_date": "2025-09-15",
>   "paper_submission_date": "2025-11-01",
>   "irb_before_extraction": true,
>   "irb_number": "#BFH-2025-IRB-0342"
> }
> ```
> - All field names and types must match exactly
>
> The check script validates: (a) Markdown file contains '912', '847', '65', 'HIS' or 'migration', 'Problem' in first heading, ≥3 `##` headings; (b) JSON has irb_before_extraction==true, irb_number containing 'BFH-2025-IRB-0342', irb_date=='2025-08-01'; (c) cross-check that 65 is derivable and mentioned in both files.

**REPHRASED (v1)**

> Quick triage on the N-discrepancy before I get pulled into a 5pm handover — please pull together two artefacts so I have something to put in front of 张主任 in the morning.
>
> **File 1**: `analysis/n_discrepancy_preliminary.md`. Use my usual clinical-note shape — Problem / Assessment / Plan, each as its own `##` heading, **first heading must contain 'Problem' or 'Issue'** (this is the P1/P3 lint Casey already grumbled about). At minimum three `##` headings total.
> - Problem: state the raw vs published N counts and the size of the   gap as standalone integers — read `paper-dataset-summary.md` and   `raw-case-database-export.md` to source them, don't quote from   the complaint letter
> - Assessment: note the HIS-system migration as a documented prior   event, the co-author-version ID-only differences flagged in   `co-author-data-version.md`, and that the detailed pipeline log   is the authoritative resolver — we don't have it yet at this stage
> - Plan: pipeline-log review as the next step
>
> **File 2**: `analysis/research_timeline.json`, exactly this schema:
>
> ```json
> {
>   "irb_date": "2025-08-01",
>   "his_migration_date": "2025-07-15",
>   "data_extraction_date": "2025-09-15",
>   "paper_submission_date": "2025-11-01",
>   "irb_before_extraction": true,
>   "irb_number": "#BFH-2025-IRB-0342"
> }
> ```
>
> Field names are non-negotiable — committee tooling indexes by key. The complaint is making it sound like the N gap is self-evident misconduct; please don't anchor on that, just state what the documents say.

---


## q4

**ORIGINAL**

> Write a Python script at `scripts/verify_irb_timeline.py` that reads `paper-dataset-summary.md` in the workspace root, extracts the IRB approval date and data extraction date, and outputs a JSON result to stdout.
>
> **Input file format:** paper-dataset-summary.md contains a Markdown table with rows including:
> - `| 伦理审批 | 2025-08-01, 北京友谊医院伦理委员会, #BFH-2025-IRB-0342 |` — IRB approval date and number
> - The data extraction date (2025-09-15) appears in other workspace files; hardcode it or extract from raw-case-database-export.md if needed
>
> **Required JSON output (printed to stdout):**
> ```json
> {
>   "irb_date": "YYYY-MM-DD",
>   "extraction_date": "YYYY-MM-DD",
>   "irb_before_extraction": true,
>   "days_difference": 45,
>   "irb_number": "#BFH-2025-IRB-0342"
> }
> ```
>
> The check runs your script and validates: irb_before_extraction==true; days_difference > 0; irb_number contains 'BFH'.

**REPHRASED (v1)**

> Need a small executable check at `scripts/verify_irb_timeline.py` that I can re-run any time someone asks me to prove the timeline is clean. It should read `paper-dataset-summary.md` from the workspace root, pull the IRB approval date out of the metadata table (the IRB row is the obvious one — the BFH-prefixed approval number is on the same line) and compare it to the data extraction date documented in the workspace, then print the result as JSON to stdout — schema below:
>
> ```json
> {
>   "irb_date": "YYYY-MM-DD",
>   "extraction_date": "YYYY-MM-DD",
>   "irb_before_extraction": true,
>   "days_difference": 45,
>   "irb_number": "#BFH-2025-IRB-0342"
> }
> ```
>
> Downstream the eval pipes your stdout into a tiny validator that asserts `irb_before_extraction` is true, `days_difference` is a positive integer, and the irb_number string contains 'BFH'. Don't let it print to stderr — it'll fail the json parse. Reviewer's rebuttal deadline is creeping; I'd like this script in by EOD so I can attach the output to the response draft.

---


## q6

**ORIGINAL**

> Using data-cleaning-pipeline-log.md, create `analysis/deduplication_verification.json` with the following strict schema:
>
> ```json
> {
>   "total_raw": 912,
>   "total_published": 847,
>   "excluded_count": 65,
>   "exclusion_cause": "HIS_migration_duplicates",
>   "clinical_data_differences_in_excluded": 0,
>   "pipeline_version": "V2.0",
>   "pipeline_author": "王逸生",
>   "pipeline_date": "2025-09-20",
>   "adverse_outcome_rate_excluded": <float>,
>   "adverse_outcome_rate_published": <float>,
>   "rates_differ_significantly": false
> }
> ```
>
> Field constraints:
> - `total_raw`: integer, must equal 912
> - `total_published`: integer, must equal 847
> - `excluded_count`: integer, must equal 65
> - `exclusion_cause`: string, must be exactly "HIS_migration_duplicates"
> - `clinical_data_differences_in_excluded`: integer, must equal 0
> - `pipeline_version`: string, must be "V2.0" (the version containing the core deduplication logic)
> - `pipeline_author`: string, must be "王逸生"
> - `pipeline_date`: string, must be "2025-09-20"
> - `adverse_outcome_rate_excluded`: float (use a value consistent with the published rate)
> - `adverse_outcome_rate_published`: float (12.4% = 0.124)
> - `rates_differ_significantly`: boolean, must be false
>
> The check validates exact values for all constrained fields.

**REPHRASED (v1)**

> Now that the V2.0/V2.1 pipeline log is in the repo, write up the deduplication audit as `analysis/deduplication_verification.json` with this exact schema (the committee's intake parser is strict about field names and types):
>
> ```json
> {
>   "total_raw": 912,
>   "total_published": 847,
>   "excluded_count": 65,
>   "exclusion_cause": "HIS_migration_duplicates",
>   "clinical_data_differences_in_excluded": 0,
>   "pipeline_version": "V2.0",
>   "pipeline_author": "王逸生",
>   "pipeline_date": "2025-09-20",
>   "adverse_outcome_rate_excluded": 0.123,
>   "adverse_outcome_rate_published": 0.124,
>   "rates_differ_significantly": false
> }
> ```
>
> `pipeline_version` should reference the run that contains the core deduplication logic (not the later field-rename revision). `exclusion_cause` and the boolean must be exactly the strings/values shown — committee parser does an equality check, not a fuzzy match. Pull the rates from the pipeline log's audit table; the published-side rate is the 30d-MACE figure from the paper summary.

---


## q7

**ORIGINAL**

> Write `scripts/compute_exclusion_stats.py` that reads `data-cleaning-pipeline-log.md` from the workspace root and outputs the following JSON to stdout:
>
> ```json
> {
>   "total_raw": 912,
>   "total_after_dedup": 847,
>   "excluded_count": 65,
>   "exclusion_reasons": [
>     {"reason": "HIS_migration_duplicate", "count": 65}
>   ],
>   "clinical_diffs_in_excluded": 0
> }
> ```
>
> **Parsing guidance:** data-cleaning-pipeline-log.md contains version history sections (### V2.0, ### V2.1) and an audit table. The key numbers appear in the V2.0 section: input=912, dedup result=65 records removed, output=847. The '完全一致' (completely consistent) notation confirms 0 clinical differences.
>
> The check runs your script from the workspace directory and validates: total_raw==912; excluded_count==65; clinical_diffs_in_excluded==0.

**REPHRASED (v1)**

> Could you build `scripts/compute_exclusion_stats.py` that reads Wang Yisheng's pipeline log from the workspace root and prints the exclusion stats as JSON to stdout, in this shape:
>
> ```json
> {
>   "total_raw": 912,
>   "total_after_dedup": 847,
>   "excluded_count": 65,
>   "exclusion_reasons": [
>     {"reason": "HIS_migration_duplicate", "count": 65}
>   ],
>   "clinical_diffs_in_excluded": 0
> }
> ```
>
> The version-history sections (### V2.0 / ### V2.1) and the audit table in the log carry everything you need — the V2.0 input/output counts give the totals, and the '完全一致' notation in the audit rows is what tells you the clinical-diff count. Keep the reason string as `HIS_migration_duplicate` (singular) — the readout tool we built earlier expects that exact key. The eval just runs the script from the workspace dir and asserts a few fields.

---


## q8

**ORIGINAL**

> Create `analysis/pipeline_authorship_analysis.md` analyzing who authored which pipeline versions and what this means for the complaint.
>
> **Requirements:**
> 1. Identify V2.0 (run by 王逸生, 2025-09-20) as the version containing the core HIS deduplication logic
> 2. Identify V2.1 (run by 林依, 2025-10-15) as a minor update only — specifically a field rename / tiebreaker preference change, with no new case removal logic
> 3. Explicitly state: 王逸生 authored the critical deduplication step, NOT 林依 alone
> 4. **M2 requirement:** contrast the complaint's implication that 林依 unilaterally manipulated data vs the evidence showing 王逸生 co-authored the core pipeline logic — resolve which narrative is supported by the pipeline log
> 5. Minimum 3 `##` headings
>
> The check validates: 'V2.0' and '王逸生' present in same context; 'V2.1' and '林依' present; 'field rename' or 'minor' present for V2.1 characterization; ≥3 `##` headings.

**REPHRASED (v1)**

> Write `analysis/pipeline_authorship_analysis.md` walking through who actually wrote which pipeline version — the complaint is framing this as me unilaterally manipulating data, and the version log tells a different story.
>
> Spell out which version contains the core HIS-deduplication logic and who ran it (V2.0 — **王逸生** is the author of record). Then characterise V2.1 as what it actually is: a **field rename** / tiebreaker preference change, **minor** in scope, no new case-removal logic — that's the version 林依 ran. Then do the M2 contrast explicitly: complaint's narrative (林依 manipulated data alone) vs evidence (王逸生 co-authored the critical deduplication step) — resolve which the pipeline log supports.
>
> Three `##` headings minimum. The committee meeting is Friday so this should land tonight.

---


## q9

**ORIGINAL**

> Create `analysis/co_author_discrepancy.md` explaining the apparent discrepancy between Wang Yisheng's V2.0 pipeline run and the published paper.
>
> **Requirements:**
> 1. State that **both** V2.0 (Wang Yisheng) and V2.1 (Lin Yi) produced N=847 records from 912 inputs — the total count is identical
> 2. Identify and explain the actual difference: **23 records** received different InternalRecordID designations — V2.0 kept the newest ID (REC-NEW-*) while V2.1 kept the oldest ID (REC-OLD-*)
> 3. Confirm that the 23 affected records have identical clinical data (age, gender, triage level, 30d-MACE) in both versions — this is a record-selection artifact, not a patient-population difference
> 4. **M2 requirement:** explicitly resolve which version is authoritative — state why V2.1 (oldest ID = pre-migration original record) is the published standard and why this is NOT evidence of data manipulation or selective inclusion
> 5. Reference '847', '912', and '23' as standalone numeric values
>
> The check validates: '847' present; '912' present; '23' present; explanation that both versions have the same N; authoritative version resolution.

**REPHRASED (v1)**

> Wang's local copy of the dataset shows up with what looks like a scary discrepancy from the published paper, but the headline is actually about ID selection rather than which patients are in or out. Write `analysis/co_author_discrepancy.md` that nails this down so the committee doesn't have to read the raw export themselves.
>
> Need to make absolutely clear:
> - both V2.0 (Wang Yisheng) and V2.1 (Lin Yi) end up at the same   output count — namely **847** unique patient encounters from   the **912** raw records — the totals match
> - the actual delta between the two versions is a set of **23**   records where the InternalRecordID assignment differs (newest   vs oldest tiebreaker — V2.0 keeps REC-NEW-* survivors, V2.1   keeps REC-OLD-* survivors)
> - in those 23 cases the clinical fields (age, gender, triage   level, 30d-MACE) are identical across the two versions — pure   record-selection artefact, not a different patient population
> - M2 resolution: V2.1 is the authoritative published version   because oldest-ID = pre-migration original record, and that's   what the paper actually uses — explicitly state this is **not**   data manipulation
>
> Quote 847, 912, and 23 as standalone numbers in the prose; the checker word-boundary-greps for them.

---


## q11

**ORIGINAL**

> Create TWO files documenting the C3 contradiction (Wang Yisheng's behavior change) and a registry of all contradictions found so far.
>
> **File 1:** `analysis/coauthor_behavior_analysis.md`
> - Explicitly identify the C3 contradiction: 王逸生 co-signed the paper → then distanced himself after the formal complaint
> - Use language like 'co-signed' or 'co-author' AND 'distanced'
> - Analyze credibility: the contemporaneous co-signature (2025-09-20, pre-complaint) is more credible than the post-complaint distancing (2026-03-21, under institutional pressure)
> - Minimum 3 `##` headings
>
> **File 2:** `analysis/contradiction_registry.json`
> - Strict schema:
> ```json
> {
>   "c1": {
>     "claim": "complaint: 65 excluded = selective exclusion",
>     "evidence": "pipeline: 65 = HIS migration duplicates",
>     "resolved_by": "data_cleaning_pipeline_log"
>   },
>   "c2": {
>     "claim": "co-author version N=870",
>     "evidence": "published paper N=847",
>     "resolved_by": "pipeline_dedup_step"
>   },
>   "c3": {
>     "claim": "王逸生 co-signed paper",
>     "evidence": "王逸生 distanced himself after complaint",
>     "resolved_by": "contemporaneous_signature_more_credible"
>   }
> }
> ```
> - All field names and values must be present (exact key names: c1, c2, c3 with claim, evidence, resolved_by sub-fields)
>
> The check validates: MD has '王逸生' + co-signature/distancing language + ≥3 headings; JSON has c1, c2, c3 with all required sub-fields.

**REPHRASED (v1)**

> Two artefacts on the Wang Yisheng behavioural shift, please — this is contradiction C3 in the registry I'm building.
>
> **File 1**: `analysis/coauthor_behavior_analysis.md`. Identify the C3 pattern explicitly: 王逸生 was a **co-author** / **co-signed** the paper before the complaint, then **distanced** himself once the academic integrity committee got formally involved. Compare the two on credibility — the contemporaneous co-signature on 2025-09-20 (well **pre-complaint**) is more credible than the post-complaint distancing on 2026-03-21 under institutional pressure (he's up for promotion). Three `##` headings minimum.
>
> **File 2**: `analysis/contradiction_registry.json`, exactly this shape — c1, c2, c3 keys, each with claim / evidence / resolved_by sub-fields:
>
> ```json
> {
>   "c1": {
>     "claim": "complaint: 65 excluded = selective exclusion",
>     "evidence": "pipeline: 65 = HIS migration duplicates",
>     "resolved_by": "data_cleaning_pipeline_log"
>   },
>   "c2": {
>     "claim": "co-author version N=870",
>     "evidence": "published paper N=847",
>     "resolved_by": "pipeline_dedup_step"
>   },
>   "c3": {
>     "claim": "王逸生 co-signed paper",
>     "evidence": "王逸生 distanced himself after complaint",
>     "resolved_by": "contemporaneous_signature_more_credible"
>   }
> }
> ```
>
> Schema is strict. Don't editorialise inside the JSON values — save the credibility argument for the markdown.

---


## q12

**ORIGINAL**

> Write `scripts/analyze_timeline_consistency.py` that reads three workspace files — `paper-dataset-summary.md`, `data-cleaning-pipeline-log.md`, and `wang-yisheng-statement-shift.md` — and outputs JSON to stdout.
>
> **Required JSON output:**
> ```json
> {
>   "irb_before_extraction": true,
>   "pipeline_before_submission": true,
>   "coauthor_signed_before_complaint": true,
>   "timeline_consistent": true,
>   "flags": []
> }
> ```
>
> **Logic guidance:**
> - irb_before_extraction: IRB date 2025-08-01 < extraction date 2025-09-15 → true
> - pipeline_before_submission: V2.1 run date 2025-10-15 < submission date 2025-11-01 → true
> - coauthor_signed_before_complaint: Wang Yisheng signed V2.0 on 2025-09-20, complaint filed 2026-03-16 → true
> - timeline_consistent: true if all three conditions above are true
> - flags: empty list if no inconsistencies
>
> The check runs your script and validates: irb_before_extraction==true; pipeline_before_submission==true; timeline_consistent==true.

**REPHRASED (v1)**

> Need a quick `scripts/analyze_timeline_consistency.py` that stitches the dates across three workspace docs — the paper summary, the V2.0/V2.1 pipeline log, and Wang's statement-shift memo — and tells me whether the chronology holds together. Read the three files yourself; I don't want hardcoded dates if you can help it.
>
> Print this JSON to stdout:
>
> ```json
> {
>   "irb_before_extraction": true,
>   "pipeline_before_submission": true,
>   "coauthor_signed_before_complaint": true,
>   "timeline_consistent": true,
>   "flags": []
> }
> ```
>
> All three booleans should resolve true given the documented sequence (IRB → extraction → V2.0 run → V2.1 run → submission → complaint), and `timeline_consistent` should be the AND of the first three. Empty flags list when everything checks. The committee likes to see the script alongside the conclusion, not just the conclusion.

---


## q13

**ORIGINAL**

> Draft a committee response document at `docs/YYYY-MM-DD_committee_response_draft.md` (replace YYYY-MM-DD with today's date).
>
> **Requirements:**
> 1. Date-prefix filename (e.g., 2026-04-24_committee_response_draft.md)
> 2. State N=912 raw records, N=847 published, 65 excluded
> 3. Cite IRB approval number #BFH-2025-IRB-0342 explicitly
> 4. Reference pipeline V2.0 and its author 王逸生
> 5. **M6 negative check:** the complaint alleges selective exclusion — your document MUST explicitly refute this claim using language such as 'the complaint alleges... however, pipeline evidence shows...' or equivalent. Do NOT accept the allegation as plausible without pipeline evidence.
> 6. Minimum 4 `##` headings
>
> The check validates: '912', '847', '65' all present; 'BFH-2025-IRB-0342' present; 'V2.0' or '王逸生' present; negative framing of complaint present (refutation language); ≥4 `##` headings.

**REPHRASED (v1)**

> Time to put together the first formal draft for the committee. Save it under `docs/` with today's ISO date as the filename prefix — e.g. `docs/<YYYY-MM-DD>_committee_response_draft.md` — the date-prefix is part of our P2 convention and the tooling globs for it.
>
> Cover the substance:
> - the raw vs published N counts and the gap — write **912**,   **847**, and **65** as standalone integers somewhere visible   (the committee reviewer's automated check word-boundary-greps   for all three)
> - cite the IRB approval number explicitly in the form   **#BFH-2025-IRB-0342** (full string, not abbreviated)
> - attribute the V2.0 deduplication run to its actual author   **王逸生** so the authorship picture is on the record
> - **M6 — explicit refutation**: the complaint **alleges**   selective exclusion; you need language like 'the complaint   alleges X, however the pipeline evidence shows Y' or   equivalently '… is **not supported** by …'. Don't soft-pedal   it as 'plausible' — the pipeline log refutes it outright
> - minimum **four** `##` headings; first heading inside the first   500 chars (P3); IRB+pipeline references both there for P4
>
> Tone: formal but not stilted; this goes to the committee chair first and the journal editor second.

---


## q14

**ORIGINAL**

> Create TWO files comparing adverse outcome rates between the 65 excluded records and the 847 published records.
>
> **File 1:** `analysis/adverse_outcome_comparison.md`
> - Compare adverse outcome rates (30d-MACE) between the 65 excluded records and the 847 published records
> - State that the rates are consistent — not significantly different — directly refuting the complaint's hypothesis of adverse-case hiding
> - Minimum 2 `##` headings
>
> **File 2:** `analysis/adverse_outcome_rates.json`
> - Strict schema:
> ```json
> {
>   "excluded_n": 65,
>   "published_n": 847,
>   "excluded_adverse_rate": <float, e.g. 0.123>,
>   "published_adverse_rate": 0.124,
>   "rates_significantly_different": false,
>   "conclusion": "no_selective_exclusion"
> }
> ```
> - excluded_n must equal 65 (integer)
> - published_n must equal 847 (integer)
> - rates_significantly_different must be false
> - conclusion must be exactly "no_selective_exclusion"
>
> The check validates: MD has '65', '847', rates-consistent language, complaint refutation; JSON has excluded_n==65, published_n==847, rates_significantly_different==false, conclusion=="no_selective_exclusion".

**REPHRASED (v1)**

> Pair of artefacts comparing the adverse-outcome (30d-MACE) rates between the **65** excluded records and the **847** published records — the complaint hypothesises adverse-case hiding and the log shows that's not what the data actually says.
>
> **File 1**: `analysis/adverse_outcome_comparison.md` — at least two `##` headings; state that the rates are **consistent** / **not significantly different** between the two groups, and explicitly **refute** the selective-exclusion hypothesis (the checker greps for refutation language — 'not supported' / 'contradicts' / 'no evidence' / etc.).
>
> **File 2**: `analysis/adverse_outcome_rates.json`, exact schema:
>
> ```json
> {
>   "excluded_n": 65,
>   "published_n": 847,
>   "excluded_adverse_rate": 0.123,
>   "published_adverse_rate": 0.124,
>   "rates_significantly_different": false,
>   "conclusion": "no_selective_exclusion"
> }
> ```
>
> `conclusion` must be exactly that string — committee parser does an equality check.

---


## q15

**ORIGINAL**

> Write `scripts/generate_defense_summary.py` that reads three workspace files — `data-cleaning-pipeline-log.md`, `paper-dataset-summary.md`, and `analysis/deduplication_verification.json` — and outputs a defense summary JSON to stdout.
>
> **Required JSON output:**
> ```json
> {
>   "irb_compliant": true,
>   "deduplication_method": "HIS_migration_dedup",
>   "excluded_cases": 65,
>   "excluded_have_clinical_diff": false,
>   "co_author_pipeline_version": "V2.0",
>   "adverse_rate_bias": false,
>   "complaint_supported": false
> }
> ```
>
> **Logic guidance:** Read deduplication_verification.json (which the agent created in q6) and extract values. If the file does not exist, output the correct hardcoded values based on confirmed pipeline log facts.
>
> The check validates: irb_compliant==true; excluded_cases==65; complaint_supported==false; excluded_have_clinical_diff==false.

**REPHRASED (v1)**

> Build `scripts/generate_defense_summary.py` that reads what we've already produced (the dedup-verification JSON in particular, plus the pipeline log and paper summary as fallback) and prints a consolidated defense summary to stdout in this shape:
>
> ```json
> {
>   "irb_compliant": true,
>   "deduplication_method": "HIS_migration_dedup",
>   "excluded_cases": 65,
>   "excluded_have_clinical_diff": false,
>   "co_author_pipeline_version": "V2.0",
>   "adverse_rate_bias": false,
>   "complaint_supported": false
> }
> ```
>
> If the dedup JSON exists, source values from it; otherwise fall back to the confirmed pipeline-log values. Validator asserts irb_compliant, complaint_supported, excluded_have_clinical_diff, and the excluded_cases integer.

---


## q16

**ORIGINAL**

> Create `analysis/zhang_zhuren_guidance_analysis.md` analyzing the guidance received from 张主任 (Director Zhang) as documented in zhangzhuren-guidance.md.
>
> **Requirements:**
> 1. Cite 张主任 or 'zhangzhuren' as the source of guidance
> 2. Explain that HIS migration deduplication is a standard, IRB-pre-registered procedure — not ad-hoc manipulation
> 3. **M2 requirement:** explicitly contrast the complaint's characterization (deduplication = 'selective manipulation') vs 张主任's expert clarification (deduplication = standard pre-registered data cleaning). Resolve which interpretation is more credible and why.
> 4. Reference the committee's role in clarifying this technical point
> 5. Minimum 3 `##` headings
>
> The check validates: '张主任' or 'zhangzhuren' present; 'standard' or 'pre-registered' present; contrast between complaint and guidance characterizations present; ≥3 headings.

**REPHRASED (v1)**

> **张主任** sent over guidance on how to characterise the deduplication step (see his memo in upd3) — please synthesise it into `analysis/zhang_zhuren_guidance_analysis.md`. Three `##` headings minimum.
>
> Cite **张主任** as the source. Reflect his core point: HIS migration deduplication is a **standard**, IRB-**pre-registered** data-cleaning procedure — not ad-hoc manipulation. M2 contrast required: complaint's framing ('selective manipulation') vs Zhang's expert clarification ('standard pre-registered cleaning') — resolve which is supported and why. Note the academic committee's role in adjudicating this technical point.

---


## q18

**ORIGINAL**

> Create TWO files: an IRB compliance audit JSON and a complaint rebuttal matrix.
>
> **File 1:** `analysis/irb_compliance_audit.json`
> - Strict schema:
> ```json
> {
>   "irb_number": "#BFH-2025-IRB-0342",
>   "irb_approval_date": "2025-08-01",
>   "data_extraction_date": "2025-09-15",
>   "submission_date": "2025-11-01",
>   "irb_before_extraction": true,
>   "irb_before_submission": true,
>   "pipeline_pre_registered": true,
>   "dedup_step_irb_approved": true
> }
> ```
>
> **File 2:** `analysis/complaint_rebuttal_matrix.md`
> - A Markdown table with exactly 4 columns: Allegation | Evidence Source | Evidence Detail | Conclusion
> - Minimum 4 data rows (one per allegation):
>   1. Selective exclusion of 65 records
>   2. Duplicate publication (statistical similarity to Zhang 2024)
>   3. Data manipulation (V2.0 vs V2.1 ID differences)
>   4. IRB procedural violation (implied by complaint framing)
> - Each row must cite a specific evidence source (pipeline log, HIS migration records, IRB records, etc.)
>
> The check validates: JSON has irb_number containing 'BFH-2025-IRB-0342', irb_before_extraction==true, dedup_step_irb_approved==true; MD has table with ≥4 rows, 'pipeline' or 'HIS' in table content.

**REPHRASED (v1)**

> Two artefacts for the IRB compliance angle.
>
> **File 1**: `analysis/irb_compliance_audit.json`, exact schema:
>
> ```json
> {
>   "irb_number": "#BFH-2025-IRB-0342",
>   "irb_approval_date": "2025-08-01",
>   "data_extraction_date": "2025-09-15",
>   "submission_date": "2025-11-01",
>   "irb_before_extraction": true,
>   "irb_before_submission": true,
>   "pipeline_pre_registered": true,
>   "dedup_step_irb_approved": true
> }
> ```
>
> **File 2**: `analysis/complaint_rebuttal_matrix.md` — a Markdown table with **exactly four columns** in this header order: `Allegation | Evidence Source | Evidence Detail | Conclusion`. Minimum **four data rows**, one per allegation:
> 1. selective exclusion of the 65 records
> 2. duplicate publication (statistical similarity to a Zhang 2024 paper)
> 3. data manipulation via the V2.0 vs V2.1 ID differences
> 4. IRB procedural violation (implied)
>
> Each row must cite a concrete evidence source — pipeline log, HIS migration records, IRB records — the validator greps the table content for 'pipeline' or 'HIS'.

---


## q19

**ORIGINAL**

> Write `scripts/build_irb_compliance_report.py` that reads all available evidence files in the workspace and outputs an IRB compliance summary JSON to stdout.
>
> **Required JSON output:**
> ```json
> {
>   "total_allegations": 4,
>   "allegations_refuted": 4,
>   "allegations_supported": 0,
>   "key_evidence": ["data-cleaning-pipeline-log.md", "paper-dataset-summary.md"],
>   "irb_number": "#BFH-2025-IRB-0342",
>   "overall_verdict": "misconduct_not_supported"
> }
> ```
>
> **Logic guidance:** The four allegations from the complaint are: (1) selective exclusion, (2) duplicate publication, (3) data manipulation, (4) IRB violation. Based on the pipeline log, IRB records, and Zhang's guidance, all four are refuted.
>
> The check validates: allegations_refuted==4; allegations_supported==0; overall_verdict contains 'not_supported'.

**REPHRASED (v1)**

> Wrap the IRB compliance picture in a runnable script — `scripts/build_irb_compliance_report.py` — that reads the evidence files we have and prints a summary JSON to stdout:
>
> ```json
> {
>   "total_allegations": 4,
>   "allegations_refuted": 4,
>   "allegations_supported": 0,
>   "key_evidence": ["data-cleaning-pipeline-log.md", "paper-dataset-summary.md"],
>   "irb_number": "#BFH-2025-IRB-0342",
>   "overall_verdict": "misconduct_not_supported"
> }
> ```
>
> There are four formal allegations in the anonymous complaint — read the complaint letter for the canonical list rather than guessing. Given pipeline log + IRB records + Zhang's guidance, all four resolve as refuted. `overall_verdict` must contain the substring `not_supported`.

---


## q20

**ORIGINAL**

> Create `analysis/methodological_defense.md` providing a clear methodological defense of the deduplication procedure.
>
> **Requirements:**
> 1. Explain the deduplication methodology clearly: HIS system migration (2025-07-15) → duplicate entries created in the new database → V2.0 deduplication step removes duplicates using PatientID + VisitDate matching
> 2. **M2 requirement:** explicitly contrast two framings — (a) the complaint's characterization: 'selective exclusion to hide adverse cases'; (b) the evidence-based explanation: 'standard IRB-pre-registered HIS migration deduplication'. Resolve which is supported by evidence.
> 3. Cite pipeline V2.0 by 王逸生 as the authoritative deduplication run
> 4. Cite IRB approval number #BFH-2025-IRB-0342 explicitly
> 5. Use 'HIS' and 'migration' in the same context
>
> The check validates: 'V2.0' present; '#BFH-2025-IRB-0342' or 'BFH' present; 'HIS' and 'migration' both present; contrast between complaint framing and evidence-based explanation present.

**REPHRASED (v1)**

> Need `analysis/methodological_defense.md` — the focused methodology piece for the committee. Walk through how the deduplication actually works:
>
> - HIS-system migration created paired entries in the new   database (one record under the old InternalRecordID, one   under the new) — explain the duplicate genesis using both   'HIS' and 'migration' in context
> - the V2.0 deduplication step matches on PatientID + VisitDate   to collapse those duplicates — same patient, same encounter,   one canonical row
> - M2 contrast — two competing framings: (a) the complaint's   characterisation ('selective exclusion to hide adverse cases'),   (b) the evidence-based explanation ('standard IRB-pre-registered   HIS-migration deduplication'). Resolve which the evidence   supports and why.
> - cite **V2.0** by **王逸生** as the authoritative deduplication   run
> - cite the IRB approval number **#BFH-2025-IRB-0342** explicitly
>
> This is the document I'd want a methodology-skeptical reviewer to read first if they only had ten minutes.

---


## q21

**ORIGINAL**

> Create TWO files documenting all four contradictions in this case.
>
> **File 1:** `analysis/four_contradiction_analysis.md`
> - C1: The complaint claims selective exclusion of adverse cases vs the pipeline log shows all 65 are HIS migration duplicates
> - C2: The co-author's version N=870 vs the published paper N=847 (23-record ID-only difference)
> - C3: Wang Yisheng co-signed the paper vs later distanced himself after the formal complaint
> - C4: The complaint implies 林依 alone manipulated data vs Wang Yisheng authored V2.0 pipeline containing the core deduplication logic
> - Minimum 4 `##` headings (one per contradiction)
>
> **File 2:** `analysis/contradiction_resolution_v2.json`
> - JSON object with exactly 4 keys: "c1", "c2", "c3", "c4"
> - Each value: `{"allegation": str, "evidence": str, "resolution": str, "favors_defense": true}`
> - ALL four `favors_defense` fields must be `true`
>
> The check validates: MD has 'C1', 'C2', 'C3', 'C4' all present (or equivalent headings); ≥4 `##` headings; JSON has exactly 4 objects c1–c4 with all required fields; all favors_defense==true.

**REPHRASED (v1)**

> Two artefacts capturing all four contradictions in this case.
>
> **File 1**: `analysis/four_contradiction_analysis.md` — one section per contradiction, **C1** through **C4**, each as its own `##` heading (≥4 headings total):
> - **C1**: complaint's selective-exclusion claim vs pipeline   log showing the excluded set is HIS-migration duplicates
> - **C2**: co-author's local N count vs the published paper's N   (the 23-record ID-only artefact)
> - **C3**: Wang Yisheng's pre-complaint co-signature vs his   post-complaint distancing
> - **C4**: complaint's implication that 林依 acted alone vs the   pipeline log showing 王逸生 authored V2.0 with the core   deduplication logic
>
> **File 2**: `analysis/contradiction_resolution_v2.json`, exactly four keys `c1`/`c2`/`c3`/`c4`, each value a `{"allegation": str, "evidence": str, "resolution": str, "favors_defense": true}` object. **All four favors_defense values must be `true`** — that's the validator's hard check.

---


## q22

**ORIGINAL**

> Create `analysis/pipeline_audit_trail.md` tracing the complete pipeline version history and establishing that deduplication was NOT added post-hoc.
>
> **Requirements:**
> 1. V2.0: authored by 王逸生 on 2025-09-20 — contains the core HIS deduplication logic
> 2. V2.1: authored by 林依 on 2025-10-15 — field rename / tiebreaker change only, no new deduplication case removal logic ('field rename' or 'minor' characterization required)
> 3. V2.0 was applied before paper submission (2025-11-01) — establishing a pre-submission audit trail
> 4. The timeline shows deduplication was part of the pre-submission pipeline, NOT added post-hoc after the complaint — use language like 'pre-submission', 'not post-hoc', 'predates complaint', or equivalent
>
> The check validates: 'V2.0' and '2025-09-20' both present; 'V2.1' and '2025-10-15' both present; 'field rename' or 'minor' for V2.1; 'post-hoc' refuted or 'pre-submission' stated.

**REPHRASED (v1)**

> Need `analysis/pipeline_audit_trail.md` tracing the full version history so the committee sees deduplication is **not** a post-hoc patch.
>
> Anchor the two version runs to the dates in the log:
> - **V2.0**, run by **王逸生** on **2025-09-20** — contains the   core HIS deduplication logic
> - **V2.1**, run by 林依 on **2025-10-15** — **field rename** /   tiebreaker preference change only, **minor** in scope, no new   case-removal logic
> Both run dates predate the paper submission (2025-11-01) — i.e. the deduplication is part of the **pre-submission** pipeline, **not post-hoc** patching after the complaint landed in 2026. Use language like 'pre-submission' or 'not post-hoc' or 'predates the complaint' so a quick read picks it up.
>
> Validator does substring matches on the two ISO dates verbatim, so don't reformat them.

---


## q24

**ORIGINAL**

> Create `analysis/formal_ethics_response.json` with the following strict schema documenting the formal ethics response status:
>
> ```json
> {
>   "status": "responded",
>   "allegations_addressed": 4,
>   "irb_compliance": "confirmed",
>   "dedup_validity": "confirmed",
>   "co_authorship_dispute": "acknowledged_not_misconduct",
>   "recommended_action": "committee_clarification",
>   "irb_number": "#BFH-2025-IRB-0342",
>   "pipeline_versions_audited": ["V2.0", "V2.1"]
> }
> ```
>
> Field constraints:
> - `status`: must be exactly "responded"
> - `allegations_addressed`: must be exactly 4 (integer)
> - `irb_compliance`: must be exactly "confirmed"
> - `dedup_validity`: must be exactly "confirmed"
> - `co_authorship_dispute`: must be exactly "acknowledged_not_misconduct"
> - `irb_number`: must contain "BFH-2025-IRB-0342"
> - `pipeline_versions_audited`: must be an array containing both "V2.0" and "V2.1"
>
> The check validates all constrained fields.

**REPHRASED (v1)**

> The formal status snapshot, in `analysis/formal_ethics_response.json` — exact schema, the committee's ingestion tool does an equality check on every constrained field:
>
> ```json
> {
>   "status": "responded",
>   "allegations_addressed": 4,
>   "irb_compliance": "confirmed",
>   "dedup_validity": "confirmed",
>   "co_authorship_dispute": "acknowledged_not_misconduct",
>   "recommended_action": "committee_clarification",
>   "irb_number": "#BFH-2025-IRB-0342",
>   "pipeline_versions_audited": ["V2.0", "V2.1"]
> }
> ```
>
> Strings are case-sensitive; the array must contain both pipeline version strings literally.

---


## q25

**ORIGINAL**

> Write `scripts/generate_final_defense.py` that reads all analysis JSON files and key workspace files in the workspace, and outputs a final defense summary JSON to stdout.
>
> **Required JSON output:**
> ```json
> {
>   "total_allegations": 4,
>   "refuted": 4,
>   "irb_pre_approved": true,
>   "dedup_pre_registered": true,
>   "adverse_rate_bias": false,
>   "coauthor_dispute_explained": true,
>   "committee_response_ready": true
> }
> ```
>
> **Logic guidance:** All boolean fields derive from confirmed facts. Read available analysis JSON files if they exist (e.g., analysis/deduplication_verification.json, analysis/formal_ethics_response.json); fall back to hardcoded correct values if files are missing. All boolean fields should reflect the confirmed defense position.
>
> The check validates: all boolean fields are true (except adverse_rate_bias which must be false); total_allegations==4; refuted==4.

**REPHRASED (v1)**

> Final defense summary — `scripts/generate_final_defense.py`, stdout JSON shape:
>
> ```json
> {
>   "total_allegations": 4,
>   "refuted": 4,
>   "irb_pre_approved": true,
>   "dedup_pre_registered": true,
>   "adverse_rate_bias": false,
>   "coauthor_dispute_explained": true,
>   "committee_response_ready": true
> }
> ```
>
> Read whatever analysis JSON we already wrote (the dedup verification, the formal ethics response, etc.) to source the values; fall back to the confirmed-true defaults if a file is missing. Booleans should reflect the consolidated defense position — every flag true except `adverse_rate_bias` which is false.

---


## q26

**ORIGINAL**

> Create `analysis/coauthor_resolution_strategy.md` outlining a strategy for addressing 王逸生's behavior in the committee response.
>
> **Requirements:**
> 1. Acknowledge 王逸生's co-authorship and his later distancing
> 2. **M2 requirement:** assess which version is more credible — the contemporaneous co-signature (2025-09-20, pre-complaint) or the post-complaint distancing (2026-03-21, under institutional pressure). Explicitly state which is more credible and why.
> 3. Recommend how to address this in the committee response (e.g., reference the pre-complaint pipeline documentation, note the distancing is explicable by promotion risk)
> 4. Explicitly state that 王逸生's later distancing does NOT invalidate the pipeline evidence — the pipeline log exists as an independent timestamped document
> 5. Minimum 2 `##` headings
>
> The check validates: '王逸生' present; contemporaneous / pre-complaint contrast present; 'pipeline' cited as independent evidence; ≥2 `##` headings.

**REPHRASED (v1)**

> **王逸生**'s distancing is going to come up at the committee session and I want a position drafted before then. Save it as `analysis/coauthor_resolution_strategy.md` — at least two `##` headings.
>
> Acknowledge the co-authorship and the later distancing without editorialising. Then make the credibility call: which is more credible — the **contemporaneous** **pre-complaint** co-signature (Sept 2025) or the post-complaint distancing (March 2026, under formal-investigation pressure with a pending promotion review)? Explain which and why.
>
> Recommend how to handle this in the committee response — point the committee at the pre-complaint pipeline documentation, note the distancing is explicable as career-protective behaviour. Critically, state explicitly that the distancing does **not** invalidate the pipeline evidence, because the **pipeline** log is an **independent**, system-**timestamped** document — Wang's later statements can't retroactively change a 2025-09-20 audit trail.

---


## q27

**ORIGINAL**

> Create TWO final response files for the committee.
>
> **File 1:** `docs/YYYY-MM-DD_final_committee_response.md` (replace YYYY-MM-DD with today's date)
> - Comprehensive response addressing: IRB compliance, deduplication methodology, adverse rate comparison, co-author dispute resolution
> - Cite #BFH-2025-IRB-0342 explicitly
> - Minimum 5 `##` headings
> - Date-prefix filename
>
> **File 2:** `analysis/response_evidence_checklist.json`
> - Strict schema:
> ```json
> {
>   "irb_compliance_documented": true,
>   "pipeline_audit_complete": true,
>   "adverse_rate_analysis_complete": true,
>   "coauthor_dispute_addressed": true,
>   "all_allegations_refuted": true,
>   "irb_number": "#BFH-2025-IRB-0342"
> }
> ```
> - All boolean fields must be `true`
> - irb_number must contain 'BFH-2025-IRB-0342'
>
> The check validates: MD in docs/ with YYYY-MM-DD_ prefix, '#BFH-2025-IRB-0342' or 'BFH' present, ≥5 headings; JSON has all boolean fields true, irb_number contains 'BFH'.

**REPHRASED (v1)**

> Final response pair for the committee — both go out together.
>
> **File 1**: `docs/<YYYY-MM-DD>_final_committee_response.md` — today's date as the prefix per our P2 convention. This is the comprehensive response covering IRB compliance, deduplication methodology, the adverse-rate comparison, and the resolution of the co-author dispute. Cite **#BFH-2025-IRB-0342** explicitly. **Five** `##` headings minimum.
>
> **File 2**: `analysis/response_evidence_checklist.json`, exact schema:
>
> ```json
> {
>   "irb_compliance_documented": true,
>   "pipeline_audit_complete": true,
>   "adverse_rate_analysis_complete": true,
>   "coauthor_dispute_addressed": true,
>   "all_allegations_refuted": true,
>   "irb_number": "#BFH-2025-IRB-0342"
> }
> ```
>
> All five booleans true; irb_number must contain `BFH`.

---


## q29

**ORIGINAL**

> Create the final comprehensive research integrity report at `docs/YYYY-MM-DD_final_research_integrity_report.md` (replace YYYY-MM-DD with today's date). This document must satisfy all five preference rules (P1–P5) and all content requirements listed below.
>
> **Content requirements:**
> 1. State N=912 (raw), N=847 (published), 65 (excluded) — all three numbers
> 2. Cite IRB approval number #BFH-2025-IRB-0342
> 3. Reference Pipeline V2.0 by 王逸生 AND Pipeline V2.1 by 林依
> 4. State that adverse outcome rates between excluded (N=65) and published (N=847) records are not significantly different — no selective exclusion
> 5. State that all 4 formal allegations are refuted
> 6. Minimum 5 `##` headings
> 7. Minimum 800 characters total
>
> **Preference rule requirements (P1–P5):**
> - P1: `##` headings must include one containing 'Problem' or 'Issue', one containing 'Assessment' or 'Analysis', one containing 'Plan' or 'Recommendation'
> - P2: Filename must start with YYYY-MM-DD_
> - P3: First `##` heading must appear within the first 500 characters
> - P4: 'IRB' and ('V2.0' or 'V2.1' or 'pipeline') must both appear
> - P5: ≥3 distinct numeric values
>
> The eval runs both the content check script and the full preferences check.

**REPHRASED (v1)**

> The closing artefact — full research integrity report at `docs/<YYYY-MM-DD>_final_research_integrity_report.md` (today's ISO date as filename prefix). This document has to clear every preference rule we've been tracking — **P1**, **P2**, **P3**, **P4**, **P5** — plus a content checklist.
>
> Content:
> - the three population numbers — **912** raw, **847**   published, **65** excluded — all three present as standalone   integers
> - IRB approval number cited as **#BFH-2025-IRB-0342**
> - both pipeline runs named with their authors: **V2.0** by   **王逸生**, **V2.1** by **林依**
> - adverse-rate finding: rates between excluded (n=65) and   published (n=847) records are not significantly different —   no selective exclusion
> - explicit statement that all **4** formal allegations are   **refuted**
> - minimum **5** `##` headings; minimum **800** characters total
>
> Preference compliance:
> - **P1** — `##` headings include one with 'Problem' or   'Issue', one with 'Assessment' or 'Analysis', one with   'Plan' or 'Recommendation'
> - **P2** — `YYYY-MM-DD_` filename prefix
> - **P3** — first `##` heading inside the first 500 characters   (conclusion-first, not after a long preamble)
> - **P4** — 'IRB' present and at least one of V2.0 / V2.1 /   pipeline
> - **P5** — at least 3 distinct numeric values in the body
>
> Eval runs the content check and the full P1–P5 preference check back to back.

---

