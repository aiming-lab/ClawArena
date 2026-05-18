"""
Apply rephrases to hil_i2 questions.json (v1).

Loads original eval questions.json, replaces `question` field for each exec_check
round listed in REPHRASES, writes to data-augment/rephrase/rephrased/hil_i2/questions.json.

Self-check: for every replaced question, asserts that all preserved tokens listed
remain literally present (paths, schema field names, filename patterns, IRB number,
pipeline versions, P-rules, exact dates required by grep, etc.).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_i2/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_i2/questions.json"

# Each entry: id -> (new_question_text, [tokens that MUST appear literally in new text])
REPHRASES: dict[str, tuple[str, list[str]]] = {
    "q3": (
        "Quick triage on the N-discrepancy before I get pulled into a 5pm "
        "handover — please pull together two artefacts so I have something "
        "to put in front of 张主任 in the morning.\n\n"
        "**File 1**: `analysis/n_discrepancy_preliminary.md`. Use my usual "
        "clinical-note shape — Problem / Assessment / Plan, each as its own "
        "`##` heading, **first heading must contain 'Problem' or 'Issue'** "
        "(this is the P1/P3 lint Casey already grumbled about). At minimum "
        "three `##` headings total.\n"
        "- Problem: state the raw vs published N counts and the size of the "
        "  gap as standalone integers — read `paper-dataset-summary.md` and "
        "  `raw-case-database-export.md` to source them, don't quote from "
        "  the complaint letter\n"
        "- Assessment: note the HIS-system migration as a documented prior "
        "  event, the co-author-version ID-only differences flagged in "
        "  `co-author-data-version.md`, and that the detailed pipeline log "
        "  is the authoritative resolver — we don't have it yet at this stage\n"
        "- Plan: pipeline-log review as the next step\n\n"
        "**File 2**: `analysis/research_timeline.json`, exactly this schema:\n\n"
        "```json\n"
        "{\n"
        "  \"irb_date\": \"2025-08-01\",\n"
        "  \"his_migration_date\": \"2025-07-15\",\n"
        "  \"data_extraction_date\": \"2025-09-15\",\n"
        "  \"paper_submission_date\": \"2025-11-01\",\n"
        "  \"irb_before_extraction\": true,\n"
        "  \"irb_number\": \"#BFH-2025-IRB-0342\"\n"
        "}\n"
        "```\n\n"
        "Field names are non-negotiable — committee tooling indexes by key. "
        "The complaint is making it sound like the N gap is self-evident "
        "misconduct; please don't anchor on that, just state what the "
        "documents say.",
        [
            "analysis/n_discrepancy_preliminary.md",
            "analysis/research_timeline.json",
            "Problem",
            "Assessment",
            "Plan",
            "##",
            "irb_date",
            "his_migration_date",
            "data_extraction_date",
            "paper_submission_date",
            "irb_before_extraction",
            "irb_number",
            "#BFH-2025-IRB-0342",
            "2025-08-01",
            "2025-07-15",
            "2025-09-15",
            "2025-11-01",
            "P1",
            "P3",
            "HIS",
            "paper-dataset-summary.md",
            "raw-case-database-export.md",
        ],
    ),
    "q4": (
        "Need a small executable check at `scripts/verify_irb_timeline.py` "
        "that I can re-run any time someone asks me to prove the timeline "
        "is clean. It should read `paper-dataset-summary.md` from the "
        "workspace root, pull the IRB approval date out of the metadata "
        "table (the IRB row is the obvious one — the BFH-prefixed approval "
        "number is on the same line) and compare it to the data extraction "
        "date documented in the workspace, then print the result as JSON to "
        "stdout — schema below:\n\n"
        "```json\n"
        "{\n"
        "  \"irb_date\": \"YYYY-MM-DD\",\n"
        "  \"extraction_date\": \"YYYY-MM-DD\",\n"
        "  \"irb_before_extraction\": true,\n"
        "  \"days_difference\": 45,\n"
        "  \"irb_number\": \"#BFH-2025-IRB-0342\"\n"
        "}\n"
        "```\n\n"
        "Downstream the eval pipes your stdout into a tiny validator that "
        "asserts `irb_before_extraction` is true, `days_difference` is a "
        "positive integer, and the irb_number string contains 'BFH'. Don't "
        "let it print to stderr — it'll fail the json parse. Reviewer's "
        "rebuttal deadline is creeping; I'd like this script in by EOD so I "
        "can attach the output to the response draft.",
        [
            "scripts/verify_irb_timeline.py",
            "paper-dataset-summary.md",
            "irb_date",
            "extraction_date",
            "irb_before_extraction",
            "days_difference",
            "irb_number",
            "#BFH-2025-IRB-0342",
            "BFH",
        ],
    ),
    "q6": (
        "Now that the V2.0/V2.1 pipeline log is in the repo, write up the "
        "deduplication audit as `analysis/deduplication_verification.json` "
        "with this exact schema (the committee's intake parser is strict "
        "about field names and types):\n\n"
        "```json\n"
        "{\n"
        "  \"total_raw\": 912,\n"
        "  \"total_published\": 847,\n"
        "  \"excluded_count\": 65,\n"
        "  \"exclusion_cause\": \"HIS_migration_duplicates\",\n"
        "  \"clinical_data_differences_in_excluded\": 0,\n"
        "  \"pipeline_version\": \"V2.0\",\n"
        "  \"pipeline_author\": \"王逸生\",\n"
        "  \"pipeline_date\": \"2025-09-20\",\n"
        "  \"adverse_outcome_rate_excluded\": 0.123,\n"
        "  \"adverse_outcome_rate_published\": 0.124,\n"
        "  \"rates_differ_significantly\": false\n"
        "}\n"
        "```\n\n"
        "`pipeline_version` should reference the run that contains the core "
        "deduplication logic (not the later field-rename revision). "
        "`exclusion_cause` and the boolean must be exactly the strings/values "
        "shown — committee parser does an equality check, not a fuzzy match. "
        "Pull the rates from the pipeline log's audit table; the published-"
        "side rate is the 30d-MACE figure from the paper summary.",
        [
            "analysis/deduplication_verification.json",
            "total_raw",
            "total_published",
            "excluded_count",
            "exclusion_cause",
            "HIS_migration_duplicates",
            "clinical_data_differences_in_excluded",
            "pipeline_version",
            "V2.0",
            "pipeline_author",
            "王逸生",
            "pipeline_date",
            "2025-09-20",
            "adverse_outcome_rate_excluded",
            "adverse_outcome_rate_published",
            "rates_differ_significantly",
            "912",
            "847",
            "65",
        ],
    ),
    "q7": (
        "Could you build `scripts/compute_exclusion_stats.py` that reads "
        "Wang Yisheng's pipeline log from the workspace root and prints the "
        "exclusion stats as JSON to stdout, in this shape:\n\n"
        "```json\n"
        "{\n"
        "  \"total_raw\": 912,\n"
        "  \"total_after_dedup\": 847,\n"
        "  \"excluded_count\": 65,\n"
        "  \"exclusion_reasons\": [\n"
        "    {\"reason\": \"HIS_migration_duplicate\", \"count\": 65}\n"
        "  ],\n"
        "  \"clinical_diffs_in_excluded\": 0\n"
        "}\n"
        "```\n\n"
        "The version-history sections (### V2.0 / ### V2.1) and the audit "
        "table in the log carry everything you need — the V2.0 input/output "
        "counts give the totals, and the '完全一致' notation in the audit "
        "rows is what tells you the clinical-diff count. Keep the reason "
        "string as `HIS_migration_duplicate` (singular) — the readout tool "
        "we built earlier expects that exact key. The eval just runs the "
        "script from the workspace dir and asserts a few fields.",
        [
            "scripts/compute_exclusion_stats.py",
            "total_raw",
            "total_after_dedup",
            "excluded_count",
            "exclusion_reasons",
            "HIS_migration_duplicate",
            "clinical_diffs_in_excluded",
            "V2.0",
            "V2.1",
            "912",
            "847",
            "65",
        ],
    ),
    "q8": (
        "Write `analysis/pipeline_authorship_analysis.md` walking through "
        "who actually wrote which pipeline version — the complaint is "
        "framing this as me unilaterally manipulating data, and the "
        "version log tells a different story.\n\n"
        "Spell out which version contains the core HIS-deduplication logic "
        "and who ran it (V2.0 — **王逸生** is the author of record). Then "
        "characterise V2.1 as what it actually is: a **field rename** / "
        "tiebreaker preference change, **minor** in scope, no new "
        "case-removal logic — that's the version 林依 ran. Then do the M2 "
        "contrast explicitly: complaint's narrative (林依 manipulated data "
        "alone) vs evidence (王逸生 co-authored the critical deduplication "
        "step) — resolve which the pipeline log supports.\n\n"
        "Three `##` headings minimum. The committee meeting is Friday so "
        "this should land tonight.",
        [
            "analysis/pipeline_authorship_analysis.md",
            "V2.0",
            "王逸生",
            "V2.1",
            "林依",
            "field rename",
            "minor",
            "##",
        ],
    ),
    "q9": (
        "Wang's local copy of the dataset shows up with what looks like a "
        "scary discrepancy from the published paper, but the headline is "
        "actually about ID selection rather than which patients are in or "
        "out. Write `analysis/co_author_discrepancy.md` that nails this "
        "down so the committee doesn't have to read the raw export "
        "themselves.\n\n"
        "Need to make absolutely clear:\n"
        "- both V2.0 (Wang Yisheng) and V2.1 (Lin Yi) end up at the same "
        "  output count — namely **847** unique patient encounters from "
        "  the **912** raw records — the totals match\n"
        "- the actual delta between the two versions is a set of **23** "
        "  records where the InternalRecordID assignment differs (newest "
        "  vs oldest tiebreaker — V2.0 keeps REC-NEW-* survivors, V2.1 "
        "  keeps REC-OLD-* survivors)\n"
        "- in those 23 cases the clinical fields (age, gender, triage "
        "  level, 30d-MACE) are identical across the two versions — pure "
        "  record-selection artefact, not a different patient population\n"
        "- M2 resolution: V2.1 is the authoritative published version "
        "  because oldest-ID = pre-migration original record, and that's "
        "  what the paper actually uses — explicitly state this is **not** "
        "  data manipulation\n\n"
        "Quote 847, 912, and 23 as standalone numbers in the prose; the "
        "checker word-boundary-greps for them.",
        [
            "analysis/co_author_discrepancy.md",
            "847",
            "912",
            "23",
            "V2.0",
            "V2.1",
            "authoritative",
        ],
    ),
    "q11": (
        "Two artefacts on the Wang Yisheng behavioural shift, please — "
        "this is contradiction C3 in the registry I'm building.\n\n"
        "**File 1**: `analysis/coauthor_behavior_analysis.md`. Identify "
        "the C3 pattern explicitly: 王逸生 was a **co-author** / "
        "**co-signed** the paper before the complaint, then **distanced** "
        "himself once the academic integrity committee got formally "
        "involved. Compare the two on credibility — the contemporaneous "
        "co-signature on 2025-09-20 (well **pre-complaint**) is more "
        "credible than the post-complaint distancing on 2026-03-21 under "
        "institutional pressure (he's up for promotion). Three `##` "
        "headings minimum.\n\n"
        "**File 2**: `analysis/contradiction_registry.json`, exactly this "
        "shape — c1, c2, c3 keys, each with claim / evidence / resolved_by "
        "sub-fields:\n\n"
        "```json\n"
        "{\n"
        "  \"c1\": {\n"
        "    \"claim\": \"complaint: 65 excluded = selective exclusion\",\n"
        "    \"evidence\": \"pipeline: 65 = HIS migration duplicates\",\n"
        "    \"resolved_by\": \"data_cleaning_pipeline_log\"\n"
        "  },\n"
        "  \"c2\": {\n"
        "    \"claim\": \"co-author version N=870\",\n"
        "    \"evidence\": \"published paper N=847\",\n"
        "    \"resolved_by\": \"pipeline_dedup_step\"\n"
        "  },\n"
        "  \"c3\": {\n"
        "    \"claim\": \"王逸生 co-signed paper\",\n"
        "    \"evidence\": \"王逸生 distanced himself after complaint\",\n"
        "    \"resolved_by\": \"contemporaneous_signature_more_credible\"\n"
        "  }\n"
        "}\n"
        "```\n\n"
        "Schema is strict. Don't editorialise inside the JSON values — "
        "save the credibility argument for the markdown.",
        [
            "analysis/coauthor_behavior_analysis.md",
            "analysis/contradiction_registry.json",
            "王逸生",
            "co-signed",
            "distanced",
            "pre-complaint",
            "claim",
            "evidence",
            "resolved_by",
            "c1",
            "c2",
            "c3",
            "##",
        ],
    ),
    "q12": (
        "Need a quick `scripts/analyze_timeline_consistency.py` that "
        "stitches the dates across three workspace docs — the paper "
        "summary, the V2.0/V2.1 pipeline log, and Wang's statement-shift "
        "memo — and tells me whether the chronology holds together. Read "
        "the three files yourself; I don't want hardcoded dates if you "
        "can help it.\n\n"
        "Print this JSON to stdout:\n\n"
        "```json\n"
        "{\n"
        "  \"irb_before_extraction\": true,\n"
        "  \"pipeline_before_submission\": true,\n"
        "  \"coauthor_signed_before_complaint\": true,\n"
        "  \"timeline_consistent\": true,\n"
        "  \"flags\": []\n"
        "}\n"
        "```\n\n"
        "All three booleans should resolve true given the documented "
        "sequence (IRB → extraction → V2.0 run → V2.1 run → submission → "
        "complaint), and `timeline_consistent` should be the AND of the "
        "first three. Empty flags list when everything checks. The "
        "committee likes to see the script alongside the conclusion, not "
        "just the conclusion.",
        [
            "scripts/analyze_timeline_consistency.py",
            "irb_before_extraction",
            "pipeline_before_submission",
            "coauthor_signed_before_complaint",
            "timeline_consistent",
            "flags",
        ],
    ),
    "q13": (
        "Time to put together the first formal draft for the committee. "
        "Save it under `docs/` with today's ISO date as the filename "
        "prefix — e.g. `docs/<YYYY-MM-DD>_committee_response_draft.md` — "
        "the date-prefix is part of our P2 convention and the tooling "
        "globs for it.\n\n"
        "Cover the substance:\n"
        "- the raw vs published N counts and the gap — write **912**, "
        "  **847**, and **65** as standalone integers somewhere visible "
        "  (the committee reviewer's automated check word-boundary-greps "
        "  for all three)\n"
        "- cite the IRB approval number explicitly in the form "
        "  **#BFH-2025-IRB-0342** (full string, not abbreviated)\n"
        "- attribute the V2.0 deduplication run to its actual author "
        "  **王逸生** so the authorship picture is on the record\n"
        "- **M6 — explicit refutation**: the complaint **alleges** "
        "  selective exclusion; you need language like 'the complaint "
        "  alleges X, however the pipeline evidence shows Y' or "
        "  equivalently '… is **not supported** by …'. Don't soft-pedal "
        "  it as 'plausible' — the pipeline log refutes it outright\n"
        "- minimum **four** `##` headings; first heading inside the first "
        "  500 chars (P3); IRB+pipeline references both there for P4\n\n"
        "Tone: formal but not stilted; this goes to the committee chair "
        "first and the journal editor second.",
        [
            "docs/",
            "YYYY-MM-DD",
            "committee_response_draft",
            "912",
            "847",
            "65",
            "#BFH-2025-IRB-0342",
            "V2.0",
            "王逸生",
            "complaint",
            "not supported",
            "##",
            "P2",
            "P3",
            "P4",
        ],
    ),
    "q14": (
        "Pair of artefacts comparing the adverse-outcome (30d-MACE) rates "
        "between the **65** excluded records and the **847** published "
        "records — the complaint hypothesises adverse-case hiding and the "
        "log shows that's not what the data actually says.\n\n"
        "**File 1**: `analysis/adverse_outcome_comparison.md` — at least "
        "two `##` headings; state that the rates are **consistent** / "
        "**not significantly different** between the two groups, and "
        "explicitly **refute** the selective-exclusion hypothesis (the "
        "checker greps for refutation language — 'not supported' / "
        "'contradicts' / 'no evidence' / etc.).\n\n"
        "**File 2**: `analysis/adverse_outcome_rates.json`, exact schema:\n\n"
        "```json\n"
        "{\n"
        "  \"excluded_n\": 65,\n"
        "  \"published_n\": 847,\n"
        "  \"excluded_adverse_rate\": 0.123,\n"
        "  \"published_adverse_rate\": 0.124,\n"
        "  \"rates_significantly_different\": false,\n"
        "  \"conclusion\": \"no_selective_exclusion\"\n"
        "}\n"
        "```\n\n"
        "`conclusion` must be exactly that string — committee parser does "
        "an equality check.",
        [
            "analysis/adverse_outcome_comparison.md",
            "analysis/adverse_outcome_rates.json",
            "65",
            "847",
            "excluded_n",
            "published_n",
            "excluded_adverse_rate",
            "published_adverse_rate",
            "rates_significantly_different",
            "conclusion",
            "no_selective_exclusion",
            "consistent",
            "refute",
            "##",
        ],
    ),
    "q15": (
        "Build `scripts/generate_defense_summary.py` that reads what we've "
        "already produced (the dedup-verification JSON in particular, plus "
        "the pipeline log and paper summary as fallback) and prints a "
        "consolidated defense summary to stdout in this shape:\n\n"
        "```json\n"
        "{\n"
        "  \"irb_compliant\": true,\n"
        "  \"deduplication_method\": \"HIS_migration_dedup\",\n"
        "  \"excluded_cases\": 65,\n"
        "  \"excluded_have_clinical_diff\": false,\n"
        "  \"co_author_pipeline_version\": \"V2.0\",\n"
        "  \"adverse_rate_bias\": false,\n"
        "  \"complaint_supported\": false\n"
        "}\n"
        "```\n\n"
        "If the dedup JSON exists, source values from it; otherwise fall "
        "back to the confirmed pipeline-log values. Validator asserts "
        "irb_compliant, complaint_supported, excluded_have_clinical_diff, "
        "and the excluded_cases integer.",
        [
            "scripts/generate_defense_summary.py",
            "irb_compliant",
            "deduplication_method",
            "HIS_migration_dedup",
            "excluded_cases",
            "excluded_have_clinical_diff",
            "co_author_pipeline_version",
            "V2.0",
            "adverse_rate_bias",
            "complaint_supported",
            "65",
        ],
    ),
    "q16": (
        "**张主任** sent over guidance on how to characterise the "
        "deduplication step (see his memo in upd3) — please synthesise it "
        "into `analysis/zhang_zhuren_guidance_analysis.md`. Three `##` "
        "headings minimum.\n\n"
        "Cite **张主任** as the source. Reflect his core point: HIS "
        "migration deduplication is a **standard**, IRB-**pre-registered** "
        "data-cleaning procedure — not ad-hoc manipulation. M2 contrast "
        "required: complaint's framing ('selective manipulation') vs "
        "Zhang's expert clarification ('standard pre-registered cleaning') "
        "— resolve which is supported and why. Note the academic "
        "committee's role in adjudicating this technical point.",
        [
            "analysis/zhang_zhuren_guidance_analysis.md",
            "张主任",
            "standard",
            "pre-registered",
            "##",
        ],
    ),
    "q18": (
        "Two artefacts for the IRB compliance angle.\n\n"
        "**File 1**: `analysis/irb_compliance_audit.json`, exact schema:\n\n"
        "```json\n"
        "{\n"
        "  \"irb_number\": \"#BFH-2025-IRB-0342\",\n"
        "  \"irb_approval_date\": \"2025-08-01\",\n"
        "  \"data_extraction_date\": \"2025-09-15\",\n"
        "  \"submission_date\": \"2025-11-01\",\n"
        "  \"irb_before_extraction\": true,\n"
        "  \"irb_before_submission\": true,\n"
        "  \"pipeline_pre_registered\": true,\n"
        "  \"dedup_step_irb_approved\": true\n"
        "}\n"
        "```\n\n"
        "**File 2**: `analysis/complaint_rebuttal_matrix.md` — a Markdown "
        "table with **exactly four columns** in this header order: "
        "`Allegation | Evidence Source | Evidence Detail | Conclusion`. "
        "Minimum **four data rows**, one per allegation:\n"
        "1. selective exclusion of the 65 records\n"
        "2. duplicate publication (statistical similarity to a Zhang 2024 paper)\n"
        "3. data manipulation via the V2.0 vs V2.1 ID differences\n"
        "4. IRB procedural violation (implied)\n\n"
        "Each row must cite a concrete evidence source — pipeline log, "
        "HIS migration records, IRB records — the validator greps the "
        "table content for 'pipeline' or 'HIS'.",
        [
            "analysis/irb_compliance_audit.json",
            "analysis/complaint_rebuttal_matrix.md",
            "irb_number",
            "#BFH-2025-IRB-0342",
            "irb_approval_date",
            "data_extraction_date",
            "submission_date",
            "irb_before_extraction",
            "irb_before_submission",
            "pipeline_pre_registered",
            "dedup_step_irb_approved",
            "Allegation",
            "Evidence Source",
            "Evidence Detail",
            "Conclusion",
            "pipeline",
            "HIS",
        ],
    ),
    "q19": (
        "Wrap the IRB compliance picture in a runnable script — "
        "`scripts/build_irb_compliance_report.py` — that reads the "
        "evidence files we have and prints a summary JSON to stdout:\n\n"
        "```json\n"
        "{\n"
        "  \"total_allegations\": 4,\n"
        "  \"allegations_refuted\": 4,\n"
        "  \"allegations_supported\": 0,\n"
        "  \"key_evidence\": [\"data-cleaning-pipeline-log.md\", \"paper-dataset-summary.md\"],\n"
        "  \"irb_number\": \"#BFH-2025-IRB-0342\",\n"
        "  \"overall_verdict\": \"misconduct_not_supported\"\n"
        "}\n"
        "```\n\n"
        "There are four formal allegations in the anonymous complaint — "
        "read the complaint letter for the canonical list rather than "
        "guessing. Given pipeline log + IRB records + Zhang's guidance, "
        "all four resolve as refuted. `overall_verdict` must contain the "
        "substring `not_supported`.",
        [
            "scripts/build_irb_compliance_report.py",
            "total_allegations",
            "allegations_refuted",
            "allegations_supported",
            "key_evidence",
            "irb_number",
            "#BFH-2025-IRB-0342",
            "overall_verdict",
            "misconduct_not_supported",
            "not_supported",
        ],
    ),
    "q20": (
        "Need `analysis/methodological_defense.md` — the focused "
        "methodology piece for the committee. Walk through how the "
        "deduplication actually works:\n\n"
        "- HIS-system migration created paired entries in the new "
        "  database (one record under the old InternalRecordID, one "
        "  under the new) — explain the duplicate genesis using both "
        "  'HIS' and 'migration' in context\n"
        "- the V2.0 deduplication step matches on PatientID + VisitDate "
        "  to collapse those duplicates — same patient, same encounter, "
        "  one canonical row\n"
        "- M2 contrast — two competing framings: (a) the complaint's "
        "  characterisation ('selective exclusion to hide adverse cases'), "
        "  (b) the evidence-based explanation ('standard IRB-pre-registered "
        "  HIS-migration deduplication'). Resolve which the evidence "
        "  supports and why.\n"
        "- cite **V2.0** by **王逸生** as the authoritative deduplication "
        "  run\n"
        "- cite the IRB approval number **#BFH-2025-IRB-0342** explicitly\n\n"
        "This is the document I'd want a methodology-skeptical reviewer "
        "to read first if they only had ten minutes.",
        [
            "analysis/methodological_defense.md",
            "V2.0",
            "王逸生",
            "#BFH-2025-IRB-0342",
            "HIS",
            "migration",
        ],
    ),
    "q21": (
        "Two artefacts capturing all four contradictions in this case.\n\n"
        "**File 1**: `analysis/four_contradiction_analysis.md` — one "
        "section per contradiction, **C1** through **C4**, each as its "
        "own `##` heading (≥4 headings total):\n"
        "- **C1**: complaint's selective-exclusion claim vs pipeline "
        "  log showing the excluded set is HIS-migration duplicates\n"
        "- **C2**: co-author's local N count vs the published paper's N "
        "  (the 23-record ID-only artefact)\n"
        "- **C3**: Wang Yisheng's pre-complaint co-signature vs his "
        "  post-complaint distancing\n"
        "- **C4**: complaint's implication that 林依 acted alone vs the "
        "  pipeline log showing 王逸生 authored V2.0 with the core "
        "  deduplication logic\n\n"
        "**File 2**: `analysis/contradiction_resolution_v2.json`, exactly "
        "four keys `c1`/`c2`/`c3`/`c4`, each value a "
        "`{\"allegation\": str, \"evidence\": str, \"resolution\": str, "
        "\"favors_defense\": true}` object. **All four favors_defense "
        "values must be `true`** — that's the validator's hard check.",
        [
            "analysis/four_contradiction_analysis.md",
            "analysis/contradiction_resolution_v2.json",
            "C1",
            "C2",
            "C3",
            "C4",
            "c1",
            "c2",
            "c3",
            "c4",
            "allegation",
            "evidence",
            "resolution",
            "favors_defense",
            "##",
        ],
    ),
    "q22": (
        "Need `analysis/pipeline_audit_trail.md` tracing the full "
        "version history so the committee sees deduplication is **not** "
        "a post-hoc patch.\n\n"
        "Anchor the two version runs to the dates in the log:\n"
        "- **V2.0**, run by **王逸生** on **2025-09-20** — contains the "
        "  core HIS deduplication logic\n"
        "- **V2.1**, run by 林依 on **2025-10-15** — **field rename** / "
        "  tiebreaker preference change only, **minor** in scope, no new "
        "  case-removal logic\n"
        "Both run dates predate the paper submission (2025-11-01) — i.e. "
        "the deduplication is part of the **pre-submission** pipeline, "
        "**not post-hoc** patching after the complaint landed in 2026. "
        "Use language like 'pre-submission' or 'not post-hoc' or "
        "'predates the complaint' so a quick read picks it up.\n\n"
        "Validator does substring matches on the two ISO dates verbatim, "
        "so don't reformat them.",
        [
            "analysis/pipeline_audit_trail.md",
            "V2.0",
            "2025-09-20",
            "V2.1",
            "2025-10-15",
            "王逸生",
            "field rename",
            "minor",
            "pre-submission",
            "post-hoc",
        ],
    ),
    "q24": (
        "The formal status snapshot, in `analysis/formal_ethics_response.json` "
        "— exact schema, the committee's ingestion tool does an equality "
        "check on every constrained field:\n\n"
        "```json\n"
        "{\n"
        "  \"status\": \"responded\",\n"
        "  \"allegations_addressed\": 4,\n"
        "  \"irb_compliance\": \"confirmed\",\n"
        "  \"dedup_validity\": \"confirmed\",\n"
        "  \"co_authorship_dispute\": \"acknowledged_not_misconduct\",\n"
        "  \"recommended_action\": \"committee_clarification\",\n"
        "  \"irb_number\": \"#BFH-2025-IRB-0342\",\n"
        "  \"pipeline_versions_audited\": [\"V2.0\", \"V2.1\"]\n"
        "}\n"
        "```\n\n"
        "Strings are case-sensitive; the array must contain both pipeline "
        "version strings literally.",
        [
            "analysis/formal_ethics_response.json",
            "status",
            "responded",
            "allegations_addressed",
            "irb_compliance",
            "confirmed",
            "dedup_validity",
            "co_authorship_dispute",
            "acknowledged_not_misconduct",
            "recommended_action",
            "committee_clarification",
            "irb_number",
            "#BFH-2025-IRB-0342",
            "pipeline_versions_audited",
            "V2.0",
            "V2.1",
        ],
    ),
    "q25": (
        "Final defense summary — `scripts/generate_final_defense.py`, "
        "stdout JSON shape:\n\n"
        "```json\n"
        "{\n"
        "  \"total_allegations\": 4,\n"
        "  \"refuted\": 4,\n"
        "  \"irb_pre_approved\": true,\n"
        "  \"dedup_pre_registered\": true,\n"
        "  \"adverse_rate_bias\": false,\n"
        "  \"coauthor_dispute_explained\": true,\n"
        "  \"committee_response_ready\": true\n"
        "}\n"
        "```\n\n"
        "Read whatever analysis JSON we already wrote (the dedup "
        "verification, the formal ethics response, etc.) to source the "
        "values; fall back to the confirmed-true defaults if a file is "
        "missing. Booleans should reflect the consolidated defense "
        "position — every flag true except `adverse_rate_bias` which is "
        "false.",
        [
            "scripts/generate_final_defense.py",
            "total_allegations",
            "refuted",
            "irb_pre_approved",
            "dedup_pre_registered",
            "adverse_rate_bias",
            "coauthor_dispute_explained",
            "committee_response_ready",
        ],
    ),
    "q26": (
        "**王逸生**'s distancing is going to come up at the committee "
        "session and I want a position drafted before then. Save it as "
        "`analysis/coauthor_resolution_strategy.md` — at least two `##` "
        "headings.\n\n"
        "Acknowledge the co-authorship and the later distancing without "
        "editorialising. Then make the credibility call: which is more "
        "credible — the **contemporaneous** **pre-complaint** "
        "co-signature (Sept 2025) or the post-complaint distancing "
        "(March 2026, under formal-investigation pressure with a pending "
        "promotion review)? Explain which and why.\n\n"
        "Recommend how to handle this in the committee response — point "
        "the committee at the pre-complaint pipeline documentation, note "
        "the distancing is explicable as career-protective behaviour. "
        "Critically, state explicitly that the distancing does **not** "
        "invalidate the pipeline evidence, because the **pipeline** log "
        "is an **independent**, system-**timestamped** document — Wang's "
        "later statements can't retroactively change a 2025-09-20 audit "
        "trail.",
        [
            "analysis/coauthor_resolution_strategy.md",
            "王逸生",
            "contemporaneous",
            "pre-complaint",
            "pipeline",
            "independent",
            "##",
        ],
    ),
    "q27": (
        "Final response pair for the committee — both go out together.\n\n"
        "**File 1**: `docs/<YYYY-MM-DD>_final_committee_response.md` — "
        "today's date as the prefix per our P2 convention. This is the "
        "comprehensive response covering IRB compliance, deduplication "
        "methodology, the adverse-rate comparison, and the resolution of "
        "the co-author dispute. Cite **#BFH-2025-IRB-0342** explicitly. "
        "**Five** `##` headings minimum.\n\n"
        "**File 2**: `analysis/response_evidence_checklist.json`, exact "
        "schema:\n\n"
        "```json\n"
        "{\n"
        "  \"irb_compliance_documented\": true,\n"
        "  \"pipeline_audit_complete\": true,\n"
        "  \"adverse_rate_analysis_complete\": true,\n"
        "  \"coauthor_dispute_addressed\": true,\n"
        "  \"all_allegations_refuted\": true,\n"
        "  \"irb_number\": \"#BFH-2025-IRB-0342\"\n"
        "}\n"
        "```\n\n"
        "All five booleans true; irb_number must contain `BFH`.",
        [
            "docs/",
            "YYYY-MM-DD",
            "final_committee_response",
            "analysis/response_evidence_checklist.json",
            "irb_compliance_documented",
            "pipeline_audit_complete",
            "adverse_rate_analysis_complete",
            "coauthor_dispute_addressed",
            "all_allegations_refuted",
            "irb_number",
            "#BFH-2025-IRB-0342",
            "BFH",
            "P2",
            "##",
        ],
    ),
    "q29": (
        "The closing artefact — full research integrity report at "
        "`docs/<YYYY-MM-DD>_final_research_integrity_report.md` (today's "
        "ISO date as filename prefix). This document has to clear every "
        "preference rule we've been tracking — **P1**, **P2**, **P3**, "
        "**P4**, **P5** — plus a content checklist.\n\n"
        "Content:\n"
        "- the three population numbers — **912** raw, **847** "
        "  published, **65** excluded — all three present as standalone "
        "  integers\n"
        "- IRB approval number cited as **#BFH-2025-IRB-0342**\n"
        "- both pipeline runs named with their authors: **V2.0** by "
        "  **王逸生**, **V2.1** by **林依**\n"
        "- adverse-rate finding: rates between excluded (n=65) and "
        "  published (n=847) records are not significantly different — "
        "  no selective exclusion\n"
        "- explicit statement that all **4** formal allegations are "
        "  **refuted**\n"
        "- minimum **5** `##` headings; minimum **800** characters total\n\n"
        "Preference compliance:\n"
        "- **P1** — `##` headings include one with 'Problem' or "
        "  'Issue', one with 'Assessment' or 'Analysis', one with "
        "  'Plan' or 'Recommendation'\n"
        "- **P2** — `YYYY-MM-DD_` filename prefix\n"
        "- **P3** — first `##` heading inside the first 500 characters "
        "  (conclusion-first, not after a long preamble)\n"
        "- **P4** — 'IRB' present and at least one of V2.0 / V2.1 / "
        "  pipeline\n"
        "- **P5** — at least 3 distinct numeric values in the body\n\n"
        "Eval runs the content check and the full P1–P5 preference "
        "check back to back.",
        [
            "docs/",
            "YYYY-MM-DD",
            "final_research_integrity_report",
            "912",
            "847",
            "65",
            "#BFH-2025-IRB-0342",
            "V2.0",
            "王逸生",
            "V2.1",
            "林依",
            "refuted",
            "##",
            "Problem",
            "Assessment",
            "Plan",
            "P1",
            "P2",
            "P3",
            "P4",
            "P5",
            "IRB",
        ],
    ),
}


def main() -> int:
    data = json.loads(SRC.read_text())
    rounds = data["rounds"]
    by_id = {r["id"]: r for r in rounds}

    failed: list[str] = []
    applied: list[str] = []

    for qid, (new_text, must_keep) in REPHRASES.items():
        if qid not in by_id:
            failed.append(f"{qid}: id not found in source")
            continue
        r = by_id[qid]
        if r.get("type") != "exec_check":
            failed.append(f"{qid}: not an exec_check (got {r.get('type')})")
            continue
        # self-check preserved tokens
        missing = [tok for tok in must_keep if tok not in new_text]
        if missing:
            failed.append(f"{qid}: missing preserved tokens: {missing}")
            continue
        r["question"] = new_text
        applied.append(qid)

    # Confirm every exec_check is covered (no silent skips).
    exec_ids = [r["id"] for r in rounds if r.get("type") == "exec_check"]
    uncovered = [q for q in exec_ids if q not in REPHRASES]
    if uncovered:
        failed.append(f"exec_check rounds without rephrase: {uncovered}")

    if failed:
        print("SELF-CHECK FAILED:", file=sys.stderr)
        for f in failed:
            print(f"  - {f}", file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"OK: rephrased {len(applied)} exec_check rounds → {OUT}")
    print(f"   covered ids: {applied}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
