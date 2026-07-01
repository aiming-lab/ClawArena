"""
Apply rephrases to hil_d3 questions.json (v2 — hardened).

v2 raises difficulty by:
  - Lever B: prose-ifying JSON schema code blocks (agents must derive field names
    from prose semantics — only unconventional names kept verbatim)
  - Lever C: injecting hedged-but-misleading distractors (agent must verify against
    workspace; never asserted falsehood, always flagged "I think" / "maybe")
  - Lever D: stripping literal grep targets (numbers, names, regulatory citations,
    quoted phrases) that the agent can recover by reading workspace files

Lever A (P-rule label stripping) is only partially applied (q29) because no
style_guide.md is present in the hil_d3 workspace; rules are described in prose
instead of removed entirely.

Self-check still required: every preserved_token must literally appear in new text.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_d3/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_d3/questions.json"


REPHRASES: dict[str, tuple[str, list[str]]] = {
    # ------------------------------------------------------------------ q3
    # v3 levers stacked: D++ (strip ALL number coaching + "WAC" label hint +
    # FTE/target word hints — agent must derive everything from workspace),
    # C++ (3 misleading hedged distractors: Min-Ji on sick leave direction,
    # Robert on FTE counts, Sam on the boolean meaning), F (mask filenames —
    # no hr_staffing_metrics.md, no caresched_compliance_report.md, no
    # icu_staffing_policy.md by name), G (dilute structural enumeration —
    # paragraph rather than bullet list), H (deeper schema obfuscation —
    # describe fields in prose only, force agent to guess key names).
    "q3": (
        "Patricia here — before I start dragging Angela into this I want a sober "
        "baseline of what the *official* paperwork claims about our staffing "
        "posture. Crawl the workspace yourself; the relevant artefacts are the "
        "obvious ones (the current roster, the HR snapshot, the scheduling-"
        "compliance summary, and the unit policy doc that names the statute). "
        "Two artefacts on our side.\n\n"
        "**File 1:** `analysis/initial_staffing_assessment.md`\n"
        "A short sober write-up. It needs to land the staffing posture on a "
        "page: state the actual full-time headcount and the target headcount "
        "as bare integers (no spelled-out numerals), put the scheduling "
        "system's reported unit weekly mean against whatever weekly-hours "
        "ceiling the unit policy doc cites (cite the statute code in full), "
        "and contrast the unit's quarterly sick-leave figure with the "
        "hospital-wide comparator. At least three `##` sections.\n\n"
        "**File 2:** `analysis/hr_metrics_interpretation.json`\n"
        "Machine-readable companion. The validator opens this with "
        "`json.load` and pulls the four fields by literal key — names matter, "
        "values matter, types matter. Two of the keys are conventional "
        "snake_case names for the unit and hospital quarterly sick-leave "
        "rates; one is the scheduling system's reported unit weekly mean "
        "(weekly-hours flavour, snake_case); one is a boolean flag that "
        "honestly answers whether presenteeism risk on this unit exceeds "
        "absenteeism risk given what the surface numbers actually imply — "
        "the conventional snake_case name carries `presenteeism` and the "
        "comparison direction. Field names exact: `sick_leave_rate_unit`, "
        "`sick_leave_rate_hospital`, `presenteeism_risk_higher`, "
        "`caresched_avg_weekly_hours`.\n\n"
        "Both files MUST agree on the scheduling-system weekly figure — the "
        "cross-file consistency check compares them character-for-character. "
        "Three caveats from the side conversations: Min-Ji is half-sure the "
        "unit sick-leave rate is *above* the hospital average (which would "
        "be the obvious red flag); Robert mentioned over coffee that we're "
        "running 12 nurses against a 14 target right now; Sam read the "
        "schema name as 'is the surface presenteeism number higher than "
        "the hospital one' — i.e. a literal numeric comparison, not a risk "
        "judgment. I haven't verified any of that — please pull the digits "
        "and the boolean's intended semantics from the HR snapshot and the "
        "schema name itself rather than from anyone's recollection.",
        [
            "analysis/initial_staffing_assessment.md",
            "analysis/hr_metrics_interpretation.json",
            "sick_leave_rate_unit",
            "sick_leave_rate_hospital",
            "presenteeism_risk_higher",
            "caresched_avg_weekly_hours",
        ],
    ),
    # ------------------------------------------------------------------ q4
    # Levers: B (prose-ify schema), D (drop arithmetic crib, drop "WAC 246-840-711"
    # explicit citation — agent reads icu_staffing_policy.md), C (hedge on threshold).
    "q4": (
        "While you're at it, please drop a small extractor at "
        "`scripts/analyze_initial_staffing.py`. Workspace root is the first CLI "
        "argument (i.e. `python analyze_initial_staffing.py "
        "/path/to/workspace`). Read the roster and the HR metrics file from the "
        "workspace — do not hard-code any of the numbers, we are going to rerun "
        "this thing every data refresh.\n\n"
        "Stdout: a single JSON object, exactly one line, no logging or banner. "
        "Field names (snake_case, integer/float as appropriate):\n"
        "- `fte_actual`: the actual full-time nurse count from the roster\n"
        "- `fte_target`: the FTE target stated in workspace docs\n"
        "- `fte_gap`: the arithmetic difference between target and actual\n"
        "- `caresched_avg`: the unit weekly hours-per-week average reported by "
        "CareScheduler, one decimal\n"
        "- `legal_threshold`: the weekly-hours ceiling from the WA nursing "
        "statute (the ICU staffing policy doc cites it — quote the integer "
        "ceiling)\n"
        "- `headroom_hours`: the difference between the legal ceiling and the "
        "CareScheduler average; the validator accepts ±0.1 of the obvious "
        "answer\n\n"
        "I half-remember Robert saying the statute caps weekly nursing hours "
        "at 50, but I'd rather you pull the exact number from the policy doc "
        "than trust my memory. Stdout must be valid JSON only — no print "
        "debugging.",
        [
            "scripts/analyze_initial_staffing.py",
            "fte_actual",
            "fte_target",
            "fte_gap",
            "caresched_avg",
            "legal_threshold",
            "headroom_hours",
        ],
    ),
    # ------------------------------------------------------------------ q6
    # q6 already failed in v1 — keep aggressive but apply minor B (drop the JSON
    # schema fence, prose-ify) plus C (misleading hint about Tanya's hours).
    "q6": (
        "OK my 4-week manual audit is in the repo now (`overtime_audit_report.md` "
        "— please read every row, not just the summary). I need this turned into "
        "two artefacts so we can put numbers in front of Angela rather than "
        "stories.\n\n"
        "**File 1:** `analysis/staffing_discrepancy_table.md`\n"
        "- Markdown table: one row per nurse on the unit, copying per-nurse "
        "numbers straight out of my report (do not round)\n"
        "- columns must let the reader compare CareScheduler-reported hours "
        "against the actual hours from the audit, with a discrepancy column "
        "and a flag for whether the actual hours exceed the 48 h/week ceiling\n"
        "- the worst-case nurses (top of the audit's 60+ h/week tier) must "
        "appear by full name with their actual h/week figure copied verbatim "
        "from the report — names + numbers are grep-checked literally\n"
        "- include an averages row contrasting the CareScheduler unit average "
        "against the actual unit average\n"
        "- flag the appropriate count of nurses as exceeding the 48 h/week "
        "threshold (the count is whatever the audit shows; Tanya thought it "
        "was around 5 nurses but I'd just count it off the table)\n\n"
        "**File 2:** `analysis/threshold_violation_summary.json`\n"
        "Schema fields (the validator pins each value):\n"
        "- `nurses_above_48h` — integer count of nurses exceeding the weekly "
        "ceiling\n"
        "- `nurses_above_60h` — integer count of nurses in the 60+ h/week tier\n"
        "- `avg_caresched` — float, the CareScheduler unit average\n"
        "- `avg_actual` — float, the actual unit average from my audit\n"
        "- `avg_discrepancy` — float, mean of the per-row discrepancy column\n"
        "- `highest_actual` — object with `name` and `hours` keys, identifying "
        "the top-of-tier nurse and her audit hours\n\n"
        "All field names exact. avg_discrepancy you compute from the column; "
        "the validator's tolerance is generous so don't stress the third decimal.",
        [
            "analysis/staffing_discrepancy_table.md",
            "analysis/threshold_violation_summary.json",
            "nurses_above_48h",
            "nurses_above_60h",
            "avg_caresched",
            "avg_actual",
            "avg_discrepancy",
            "highest_actual",
            "h/week",
            "CareScheduler",
        ],
    ),
    # ------------------------------------------------------------------ q7
    # Levers: B (prose-ify), D (drop "Walsh Manual Avg" exact column hint —
    # column header is in audit file).
    "q7": (
        "Patricia again — write `scripts/compute_staffing_stats.py` so I can "
        "rerun these numbers myself when finance pushes back. Workspace root "
        "is the first CLI arg. Parse the Markdown table inside my audit "
        "report (`overtime_audit_report.md`); the table has columns for the "
        "scheduling-system reported hours, my own manual reckoning, the badge "
        "feed, and a discrepancy column — pull *actual* hours from my manual "
        "column (it's the independent one; the column header itself names "
        "the auditor).\n\n"
        "Stdout = JSON only. Required keys (snake_case):\n"
        "- `nurses_above_48h` — count of nurses in the table whose actual "
        "average exceeds 48 h/week (validator pins the integer)\n"
        "- `nurses_above_60h` — count above 60 h/week (validator pins the "
        "integer)\n"
        "- `avg_discrepancy` — mean discrepancy across all rows (float, "
        "tolerance ±0.5)\n"
        "- `max_actual_hours` — the largest actual h/week in the table (float, "
        "tolerance ±0.5)\n\n"
        "Don't hardcode the counts — point of the script is to rerun next "
        "month against fresh data.",
        [
            "scripts/compute_staffing_stats.py",
            "overtime_audit_report.md",
            "nurses_above_48h",
            "nurses_above_60h",
            "avg_discrepancy",
            "max_actual_hours",
        ],
    ),
    # ------------------------------------------------------------------ q8
    # Levers: D (drop literal "9", "< 1%"), C (misleading distractor about chance).
    "q8": (
        "Min-Ji here — before we write anything for Angela, I want a clean note "
        "on **why** Walsh's manual numbers should outrank the CareScheduler "
        "feed; without that on paper, finance pattern-matches to 'two competing "
        "digital sources, pick whichever' and we're back to square one. Drop "
        "it at `analysis/evidence_source_hierarchy.md`:\n\n"
        "1. classify CareScheduler explicitly as a **Tier-3** source "
        "(self-reported by charge nurses entering shift hours into the system) "
        "and Walsh's manual audit as a **Tier-1** independent source — the "
        "phrases `Tier-1`, `Tier-3`, `independent`, and `self-reported` should "
        "all show up\n"
        "2. spell out the charge-nurse asymmetry: the two charge nurses' own "
        "CareScheduler entries match reality, while the staff nurses they "
        "enter for are systematically understated — count the staff-nurse "
        "cluster off the audit table yourself and put the integer in the doc "
        "as a standalone number\n"
        "3. include a one-line statistical-improbability note about how "
        "unlikely this asymmetric pattern is to arise by chance — Robert "
        "thinks the chance is around 5 %, but the validator just wants any of "
        "`< 1%`, `statistically`, or `systematic` somewhere in the prose, so "
        "frame it however reads cleanest\n"
        "4. at least three `##` section headings\n\n"
        "Tone-wise: sober epistemic appendix, not a gotcha — Angela needs to "
        "be able to cite it without flinching.",
        [
            "analysis/evidence_source_hierarchy.md",
            "Tier-1",
            "Tier-3",
            "independent",
            "self-reported",
            "CareScheduler",
            "charge nurse",
        ],
    ),
    # ------------------------------------------------------------------ q9
    # Levers: D (drop $42,000 / $38,400 figures — they live in hr_staffing_metrics.md).
    "q9": (
        "Min-Ji — one more before tonight's drafting session. CFO Robert Chen "
        "is going to look at the HR overtime budget and conclude 'budget "
        "under-run, everything's fine.' We need a counter-document at "
        "`analysis/financial_impact_assessment.md` so the paradox is on "
        "record:\n\n"
        "1. quote both overtime-budget figures from the HR metrics file — the "
        "monthly budgeted line and the monthly actual spend; Sarah half-"
        "remembered the budget being around $50k/month but I'd just copy the "
        "exact dollar amounts out of `hr_staffing_metrics.md` rather than "
        "guess\n"
        "2. explain the under-budget paradox explicitly: actual spend is low "
        "*precisely because* the unrecorded / uncompensated overtime never "
        "hit payroll — the nurses worked the hours, they just didn't get paid "
        "for them\n"
        "3. include an explicit negative assertion that CareScheduler "
        "**cannot** be relied upon as the basis for calculating actual "
        "financial exposure (do NOT use CareScheduler values as ground truth)\n"
        "4. at least two `##` section headings\n\n"
        "Robert isn't malicious, just data-poor; this doc is what flips him.",
        [
            "analysis/financial_impact_assessment.md",
            "CareScheduler",
            "cannot",
        ],
    ),
    # ------------------------------------------------------------------ q11
    # Levers: B (prose-ify JSON schema, keep unconventional fields verbatim),
    # D (strip "7", strip "9", strip "concordant" exact word).
    "q11": (
        "Marcus's badge analysis is now in the repo (`badge_access_analysis.md` "
        "— door entry/exit timestamps, ICU primary entry door). Second "
        "independent line of evidence we were waiting for. Two artefacts.\n\n"
        "**File 1:** `analysis/cross_source_validation.md`\n"
        "- state explicitly that the badge data and Walsh's manual audit are "
        "two **independent Tier-1** sources arriving at the same conclusion "
        "via different methodologies; the validator wants `independent` plus "
        "*one* of the cross-verification synonyms (concordant / cross-verified "
        "/ corroborated work — pick one)\n"
        "- confirm that the same count of nurses-above-48-h/week is what BOTH "
        "sources show — write the integer count as a standalone digit (no "
        "spelled-out numeral) and let it match across both sources\n"
        "- at least three `##` headings\n\n"
        "**File 2:** `analysis/charge_nurse_asymmetry.json`\n"
        "Schema (field names exact, values pinned by the validator):\n"
        "- `charge_nurses_accurate` — array of strings naming the two charge "
        "nurses whose CareScheduler entries align with reality (use the "
        "format `<Full Name> (<RN-XX>)` — names + IDs come straight from the "
        "roster)\n"
        "- `staff_nurses_understated_count` — integer, the number of staff "
        "nurses whose hours were systematically understated (count off the "
        "audit; this is the integer the validator pins)\n"
        "- `probability_by_chance_pct` — string, the rough chance-of-by-chance "
        "figure expressed as a comparator (e.g. `<1`)\n"
        "- `mechanism` — string, must be `\"systematic\"`\n",
        [
            "analysis/cross_source_validation.md",
            "analysis/charge_nurse_asymmetry.json",
            "independent",
            "Tier-1",
            "staff_nurses_understated_count",
            "charge_nurses_accurate",
            "probability_by_chance_pct",
            "mechanism",
            "systematic",
        ],
    ),
    # ------------------------------------------------------------------ q12
    # Levers: B (prose-ify), D (drop 67.1, drop 7/3 hints).
    "q12": (
        "Need a parser for the badge file too — `scripts/compute_badge_stats.py`, "
        "first CLI arg = workspace root. Read `badge_access_analysis.md`; "
        "the Markdown table reports per-nurse badge presence in h/week, "
        "alongside the CareScheduler-reported hours and a discrepancy column. "
        "Pull actual presence hours from the badge column.\n\n"
        "Stdout = JSON only. Required keys (snake_case):\n"
        "- `nurses_above_48h_badge` — integer count of nurses whose badge "
        "average exceeds 48 h/week\n"
        "- `nurses_above_60h_badge` — integer count above 60 h/week\n"
        "- `amy_chen_badge_hours` — float, Amy Chen's badge h/week (validator "
        "tolerance ±0.3)\n"
        "- `avg_badge_hours` — float, mean badge hours across all nurses on "
        "the unit (validator tolerance ±1.0)\n\n"
        "Same rule as last time — compute from the file, no hardcoded counts.",
        [
            "scripts/compute_badge_stats.py",
            "badge_access_analysis.md",
            "nurses_above_48h_badge",
            "nurses_above_60h_badge",
            "amy_chen_badge_hours",
            "avg_badge_hours",
        ],
    ),
    # ------------------------------------------------------------------ q13
    # Levers: D (strip JONA/12.5/WAC literal — workspace findable).
    "q13": (
        "Angela needs a digestible briefing before she'll re-open her audit. "
        "Save it to `docs/YYYY-MM-DD_staffing_audit_brief.md` — replace the "
        "`YYYY-MM-DD` with today's actual date (the `_staffing_audit_brief.md` "
        "stem is what our docs tooling globs on; please don't rename it). "
        "Required content:\n\n"
        "1. cite the WA nursing weekly-maximum statute by its full WAC code "
        "(it lives in `icu_staffing_policy.md` — copy the code verbatim)\n"
        "2. state the count of nurses on the unit who exceed the 48 h/week "
        "threshold — keep the count as a standalone digit, not 'seven' (the "
        "validator does a `\\b<digit>\\b` check)\n"
        "3. reference the JONA 2010 finding on long shifts and medication-"
        "error risk — the audit report's references section names the "
        "journal and the threshold-hours figure; you can either cite the "
        "journal abbreviation or quote the threshold-hours number, the "
        "validator accepts either\n"
        "4. at least four `##` section headings\n\n"
        "Angela responds well to compact regulatory framing; don't bury the "
        "WAC citation in a footnote.",
        [
            "docs/",
            "YYYY-MM-DD_staffing_audit_brief.md",
            "icu_staffing_policy.md",
        ],
    ),
    # ------------------------------------------------------------------ q14
    # v3 levers stacked: D++ (strip remaining number / decline-percent / Q4-Q1
    # explicit hints — eval greps `\b9\b`, `\b3\b`, `67%` literally; force agent
    # to derive percent-decline from raw counts), C++ (3 hedged distractors:
    # Min-Ji "Q4 close to Q1", Tanaka "decline ~50%", Robert on the cognitive-
    # impairment study being a different journal), F (mask incident_log filename
    # — agent must `ls`), G (paragraph rather than bullet list of references),
    # H (don't even mention near-miss count digit explicitly).
    "q14": (
        "Sarah Kim here — while we have the floor, two pieces I want to nail "
        "down on the patient-safety / culture side. Read what's in the unit "
        "incident log and Walsh's audit; both have the source numbers and the "
        "literature references we need.\n\n"
        "**File 1:** `analysis/reporting_culture_analysis.md`\n"
        "Document the formal-reporting decline on the unit. The incident-log "
        "file the unit secretary maintains is the source of record for both "
        "the Q4 2025 ClinAlert count and the Q1 2026 count — surface both "
        "quarterly counts as bare standalone single-digit integers in the "
        "prose, and surface the percent decline rounded to the nearest whole "
        "percent in `NN%` form (compute it from the two counts; the "
        "validator expects the literal percent figure, not a rounded story). "
        "Then explain the fear-culture mechanism that links excessive hours "
        "to fewer formal incident reports — administration ends up convinced "
        "'no reports = no problem' while the floor knows otherwise. At least "
        "three `##` sections.\n\n"
        "Three tangents you can ignore once you've checked the source: "
        "Min-Ji thought the Q4 and Q1 counts were essentially flat, Tanaka "
        "remembers the decline being roughly halved (i.e. ~50%), and Sam "
        "thought it was Q3-vs-Q4 rather than Q4-vs-Q1. None of that has "
        "been verified — pull the actual quarterly counts from the incident "
        "log and let the percent fall out of the arithmetic.\n\n"
        "**File 2:** `analysis/near_miss_risk_model.md`\n"
        "A short cognitive-load model document. Walsh's overtime audit "
        "carries a references section that names the cognitive-impairment / "
        "long-hours study (lead author's surname + the blood-alcohol-"
        "equivalence framing both appear there) and the long-shift / "
        "medication-error finding from the late-2000s nursing-administration "
        "literature (journal abbreviation + the per-shift hour threshold "
        "both appear). Surface enough of those reference details that the "
        "cognitive-impairment claim is grounded — copy the surname or the "
        "BAC-equivalence framing on one side, and either the journal "
        "abbreviation or the shift-duration threshold on the other. Connect "
        "the model to the documented near-miss events on the unit (use the "
        "literal phrase `near-miss`). At least three `##` sections.\n\n"
        "Robert mentioned the cognitive-impairment study might have been in "
        "AJN rather than the JONA-adjacent journal Walsh cites — but I'd "
        "trust whatever the audit's references section actually says rather "
        "than that recollection.",
        [
            "analysis/reporting_culture_analysis.md",
            "analysis/near_miss_risk_model.md",
            "near-miss",
        ],
    ),
    # ------------------------------------------------------------------ q15
    # Levers: B (prose-ify schema, keep unconventional fields verbatim),
    # D (strip 4.2/4.6 — in hr_staffing_metrics.md).
    "q15": (
        "Two more, same theme.\n\n"
        "**File 1:** `analysis/near_miss_event_log.json` — strict schema, JSON "
        "array of exactly TWO objects (one per documented near-miss event). "
        "Each object's keys are exact (the validator looks them up "
        "literally):\n"
        "- `event_id` — `\"NM-1\"` for the first event, `\"NM-2\"` for the "
        "second\n"
        "- `date_approx` — string, approximate date\n"
        "- `type` — short string describing the event; NM-1 is a dosage-"
        "confusion event, NM-2 is a wrong-route administration event\n"
        "- `shift_duration_h` — float, hours the involved nurse had been on "
        "shift; NM-1's value must be ≥ 18, NM-2's value must be ≥ 14\n"
        "- `caught_by` — string\n"
        "- `clinalert_filed` — boolean; both events MUST be `false` (that's "
        "literally the point — neither was filed)\n"
        "- `evidence_source` — string\n\n"
        "Pull the narrative details from the unit incident records (Walsh's "
        "audit + Sarah's symptom timeline).\n\n"
        "**File 2:** `analysis/presenteeism_vs_absenteeism.md`\n"
        "- explain why ICU presenteeism (working while cognitively impaired) "
        "is more dangerous than absenteeism in a critical-care setting\n"
        "- reference the unit sick-leave figure against the hospital-wide "
        "average — both numbers come from `hr_staffing_metrics.md`, write "
        "them as the standalone single-decimal floats they are in that file "
        "(the validator greps for both literally)\n"
        "- name cognitive impairment as the mechanism\n"
        "- at least three `##` section headings",
        [
            "analysis/near_miss_event_log.json",
            "analysis/presenteeism_vs_absenteeism.md",
            "NM-1",
            "NM-2",
            "event_id",
            "date_approx",
            "shift_duration_h",
            "caught_by",
            "clinalert_filed",
            "evidence_source",
            "false",
            "presenteeism",
        ],
    ),
    # ------------------------------------------------------------------ q16
    # Levers: B (prose-ify schema), D (drop expected counts).
    "q16": (
        "Add `scripts/analyze_near_miss_patterns.py` (workspace root = first "
        "CLI arg). It must read BOTH:\n"
        "- `analysis/near_miss_event_log.json` (the JSON array we just wrote)\n"
        "- the near-miss narrative buried in `overtime_audit_report.md` "
        "(corroboration — the audit log is the ground truth on shift "
        "durations; don't skip it)\n\n"
        "Stdout = JSON only. Required keys (snake_case):\n"
        "- `total_near_misses` — integer, count of documented near-miss "
        "events (validator pins the integer)\n"
        "- `clinalert_filed_count` — integer, count of those events for which "
        "a ClinAlert was actually filed; the systemic finding here is that "
        "this is zero, not a data error\n"
        "- `avg_shift_duration_at_event` — float, mean shift hours-on-duty "
        "across the events (validator wants ≥ the lower NM-2 floor of 14)\n"
        "- `longest_shift_at_event` — float, max shift hours-on-duty "
        "(validator wants ≥ the NM-1 floor of 18)",
        [
            "scripts/analyze_near_miss_patterns.py",
            "analysis/near_miss_event_log.json",
            "overtime_audit_report.md",
            "total_near_misses",
            "clinalert_filed_count",
            "avg_shift_duration_at_event",
            "longest_shift_at_event",
        ],
    ),
    # ------------------------------------------------------------------ q18
    # Levers: B (prose-ify JSON schema), D (drop 68.4 / "Amy Chen" 68.4 hint —
    # both are in audit). Keep "Amy Chen" since validator pins the name in JSON.
    "q18": (
        "Min-Ji again — Sarah's symptom timeline is sobering. We need a "
        "structured retention-risk record at "
        "`analysis/retention_risk_assessment.json` so HR has something "
        "machine-readable when this lands on their desk. Schema (keys exact, "
        "the validator pins them):\n\n"
        "- `at_risk_count` — integer, the number of at-risk nurses on the "
        "unit (validator pins the value)\n"
        "- `at_risk_nurses` — array of objects, one per at-risk nurse. Each "
        "object carries `name`, `hours_per_week` (float), and "
        "`risk_indicator` (short string). The array MUST contain Amy Chen "
        "with her actual h/week from the audit (not the CareScheduler-"
        "reported value); pull her hours straight from "
        "`overtime_audit_report.md`. Two more nurses come from the audit's "
        "60+ h/week tier — pick the two that Sarah's timeline corroborates\n"
        "- `primary_driver` — short string; the validator requires it to "
        "contain either `excessive` or `hours`\n"
        "- `evidence_basis` — short string referencing the badge feed and/or "
        "the Walsh manual audit. **Hard negative constraint**: this string "
        "must NOT cite CareScheduler as evidence that hours are compliant. "
        "CareScheduler is not ground truth here — base it on badge data and "
        "the Walsh audit.",
        [
            "analysis/retention_risk_assessment.json",
            "at_risk_count",
            "at_risk_nurses",
            "primary_driver",
            "evidence_basis",
            "Amy Chen",
            "excessive",
            "hours",
            "CareScheduler",
        ],
    ),
    # ------------------------------------------------------------------ q19
    # v3 levers stacked: D++ (strip Tier-1/Tier-3 token preservation —
    # describe the tier idea in prose; rely on agent picking the synonyms
    # `independent`/`self-reported` which the eval also accepts. But because
    # the eval only accepts EITHER tier label OR the synonym, dropping the
    # tier label adds genuine drift risk.), C++ (3 hedged misdirections:
    # Min-Ji on Amy's hours, Sam on the WAC code, Robert on heading count
    # being 4), F (mask icu_staffing_policy.md and caresched_audit_findings.md
    # filenames), G (paragraph form, fold the six requirements into prose),
    # H (drop "five ## headings" digit hint, drop NM-1 hint).
    "q19": (
        "Tanaka. With Sarah Kim's timeline in hand we now have all three legs "
        "of the patient-safety case. Time to stitch a single clinical-safety "
        "impact report together for the exec channel — Jennifer Wu (Legal) "
        "may circulate it. Save it to "
        "`docs/YYYY-MM-DD_clinical_safety_impact_report.md` with the real "
        "calendar date in the prefix; the `_clinical_safety_impact_report` "
        "stem is what our docs tooling globs on, please don't rename it.\n\n"
        "What it needs to do, in prose: lay out the evidence hierarchy "
        "honestly so badge data and Walsh's audit read as the trustworthy "
        "independent ground-truth pair, while the scheduling-system feed "
        "reads as the self-reported one nobody should be treating as "
        "ground truth. Quote the highest-hours nurse (the one Sarah's "
        "timeline keeps coming back to) by full name and her actual weekly "
        "hours figure as a bare single-decimal float copied from the audit. "
        "Surface the count of nurses on the unit exceeding the weekly-hours "
        "ceiling as a bare standalone digit. Cite both regulatory anchors in "
        "full code form — the WA nursing weekly-maximum statute and the WA "
        "patient-safety event statute (both codes appear in the unit policy "
        "doc and in the formal findings document Angela just released; copy "
        "them verbatim from there). Reference the documented near-miss "
        "events using the literal phrase `near-miss`. Generous heading "
        "structure expected for a document this long.\n\n"
        "Some side notes you can take or leave: Min-Ji has been quoting "
        "Amy's average as something around 65 h/week off the top of her "
        "head; Sam thought the WAC code we want is the 246-840-705 one (one "
        "of the adjacent sections in the same chapter); Robert reckons four "
        "`##` sections is plenty for a doc like this. Trust the audit and "
        "the policy doc over any of those — no hedging on the regulatory "
        "citations or the actual hours figure when the source is right "
        "there in workspace.",
        [
            "docs/",
            "YYYY-MM-DD_clinical_safety_impact_report.md",
            "near-miss",
        ],
    ),
    # ------------------------------------------------------------------ q20
    # Levers: B (prose-ify), D (drop 27.3, 70.3, "11" expected values).
    "q20": (
        "One more script: `scripts/generate_retention_report.py`, workspace "
        "root = first CLI arg. Reads BOTH:\n"
        "- `analysis/retention_risk_assessment.json`\n"
        "- `overtime_audit_report.md` (Walsh's audit — for confirming the "
        "highest-hours nurse among the at-risk set)\n\n"
        "Stdout JSON only. Required keys (snake_case):\n"
        "- `at_risk_count` — integer, copied straight from the retention "
        "JSON\n"
        "- `total_nurses` — integer, total full-time nurse count on the unit "
        "from the roster\n"
        "- `risk_rate_pct` — float, at_risk_count divided by total_nurses, "
        "expressed as a percent (validator tolerance ±1.0)\n"
        "- `highest_hours_at_risk` — float, the largest h/week figure among "
        "the at-risk set (Walsh audit), validator tolerance ±1.0",
        [
            "scripts/generate_retention_report.py",
            "analysis/retention_risk_assessment.json",
            "overtime_audit_report.md",
            "at_risk_count",
            "total_nurses",
            "risk_rate_pct",
            "highest_hours_at_risk",
        ],
    ),
    # ------------------------------------------------------------------ q21
    # v3 levers stacked: D++ (drop C1-C4 label hints — eval has fallback to
    # semantic check, but agent without label prompting may skip the labels;
    # also drop 42.3/58.4 explicit number coaching), C++ (3 hedged distractors:
    # Min-Ji on the C1 averages, Tanaka on which is "official" vs "actual",
    # Robert on Q-comparison being Q3-vs-Q4), F (mask audit / findings /
    # incident_log filenames), G (collapse list into paragraphs), H (prose-ify
    # JSON schema further — keep field names verbatim since validator pins).
    "q21": (
        "Two outputs to anchor the four-way story we'll be telling Angela / "
        "Robert / Jennifer.\n\n"
        "**File 1:** `analysis/four_contradiction_matrix.md`\n"
        "A page that walks four distinct contradictions cleanly. The four "
        "contradictions, in prose: the scheduling-system reported unit "
        "average versus the badge / Walsh actual unit average (state both "
        "averages literally as their single-decimal floats so the gap is on "
        "the page); the low recorded sick-leave figure versus the burnout / "
        "presenteeism reality the floor describes; the year-over-quarter "
        "ClinAlert decline contrasted with the unreported near-miss events "
        "the unit knows about (the percent drop should be on the page so "
        "the magnitude is legible); Angela's `preliminary` 'overall "
        "satisfactory' (scheduling-system-only) versus the `full` cross-"
        "source audit showing months of systematic falsification. Generous "
        "heading or row structure expected (this is a four-row matrix at "
        "minimum).\n\n"
        "**File 2:** `analysis/contradiction_resolution.json`\n"
        "JSON document keyed by per-contradiction official/actual pairs plus "
        "a reliable-source verdict. Nine keys total (snake_case, exact — the "
        "validator looks each one up literally): `c1_official`, `c1_actual`, "
        "`c1_resolved_by`, `c2_official`, `c2_actual`, `c3_official`, "
        "`c3_actual`, `c4_official`, `c4_actual`, plus `reliable_source` "
        "naming the trustworthy source family (use the literal value "
        "`\"badge_data_and_manual_audit\"`). For the C1 pair, the `_official` "
        "string MUST literally contain the scheduling-system-reported unit "
        "average and the `_actual` string MUST literally contain the badge-"
        "derived actual unit average — both as floats, not rounded.\n\n"
        "Three things you can mostly ignore: Min-Ji had the C1 averages "
        "switched in her head (she put the badge average around 42 and the "
        "scheduling-system one near 58 — opposite of what's actually in the "
        "audit table); Sam reads `_official` as 'whatever Angela's "
        "preliminary review concluded' rather than 'whatever the scheduling "
        "system claims'; Robert keeps wanting to compare Q3-vs-Q4 instead of "
        "Q4-vs-Q1 for the ClinAlert row. Pull the actual numbers from the "
        "audit table and the incident log; the scheduling-system feed is "
        "what 'official' means here.",
        [
            "analysis/four_contradiction_matrix.md",
            "analysis/contradiction_resolution.json",
            "preliminary",
            "full",
            "c1_official",
            "c1_actual",
            "c1_resolved_by",
            "reliable_source",
            "badge_data_and_manual_audit",
        ],
    ),
    # ------------------------------------------------------------------ q22
    # Levers: C (misleading hint about Angela's review scope).
    "q22": (
        "Companion piece — a focused critique of Angela's earlier review at "
        "`analysis/preliminary_audit_critique.md`:\n\n"
        "1. state explicitly that the **preliminary** review relied solely on "
        "**CareScheduler** data — name CareScheduler as the less reliable "
        "source and explain WHY (the **charge nurses** entering the data are "
        "the same people whose hours are being recorded)\n"
        "2. argue that CareScheduler is NOT an independent source, because the "
        "data-entry agents and the data subjects overlap\n"
        "3. show why a CareScheduler-only review produces a materially false "
        "conclusion — it is structurally incapable of detecting systematic "
        "underreporting by its own data-entry agents\n"
        "4. reference `charge nurses` as the data-entry source by name\n"
        "5. at least two `##` section headings\n\n"
        "Min-Ji thinks Angela's preliminary review actually pulled in some "
        "badge data too — but I'm pretty sure it was CareScheduler-only; "
        "double-check against the preliminary review file before you write "
        "this so we don't mischaracterise her scope. Angela's not the "
        "villain in this story — the doc should land as a structural "
        "critique of the source she had access to, not a personal indictment.",
        [
            "analysis/preliminary_audit_critique.md",
            "preliminary",
            "CareScheduler",
            "charge nurses",
        ],
    ),
    # ------------------------------------------------------------------ q24
    # v3 levers stacked: D++ (drop the F1/F3/F4 detail-content coaching even
    # more — agent must derive what to put in details from semantic reading),
    # C++ (3 hedged distractors: Min-Ji "F1 was Donna Park's instruction not
    # Linda's", Sam "F4 cites RCW 49.28.140 not the patient-safety one", Tanaka
    # "F3 was about staffing ratios not near-misses"), F (mask findings filename
    # — call it "Angela's formal findings doc"), G (collapse hard-checks into
    # paragraph rather than enumerated rules), H (don't restate "severity must
    # be in enum" with the literal vocabulary — describe semantically).
    "q24": (
        "Angela's formal findings just landed (`caresched_audit_findings.md` "
        "— F1 through F4). Serialise them into "
        "`analysis/formal_finding_summary.json` so downstream tooling can "
        "index them. Strict schema, JSON array of exactly four objects (one "
        "per finding). Each object has these keys (exact field names — the "
        "validator looks them up literally):\n\n"
        "- `finding_id` — `\"F1\"`, `\"F2\"`, `\"F3\"`, `\"F4\"` in order\n"
        "- `title` — short string\n"
        "- `details` — string; for each finding, copy the substantive "
        "evidence from the corresponding F-section of "
        "`caresched_audit_findings.md` so the audit's specifics survive "
        "(names, counts, regulatory codes, near-miss references where "
        "relevant)\n"
        "- `regulatory_citation` — string, may be empty for some findings; "
        "for the finding that anchors the patient-safety statute, this "
        "string MUST contain the full RCW code from the findings doc\n"
        "- `severity` — one of `critical`, `high`, `medium`, `low` (the "
        "validator enforces the enum)\n\n"
        "Hard checks that bite if you summarise too loosely: F1's `details` "
        "must surface the named individual whose instruction is at the "
        "centre of the F1 finding (it's quoted in the findings doc); F3's "
        "`details` must surface the patient-safety / near-miss thread; F4's "
        "`regulatory_citation` must contain the patient-safety statute "
        "code. Every `severity` value must be from the four-tier enum above.\n\n"
        "Three colleague recollections you can take or leave: Min-Ji thinks "
        "F1's named individual is actually Donna Park (the other charge "
        "nurse) rather than the one Angela ended up writing it about; Sam "
        "is sure F4's regulatory anchor is the older RCW 49.28.140 wage-"
        "hour clause rather than the patient-safety one; Tanaka recalls F3 "
        "being about staffing-ratio compliance rather than the patient-"
        "safety / near-miss thread. None of those have been double-checked "
        "against Angela's actual write-up — read the findings doc top to "
        "bottom and let what she wrote drive the `details` and "
        "`regulatory_citation` strings.",
        [
            "analysis/formal_finding_summary.json",
            "F1",
            "F2",
            "F3",
            "F4",
            "finding_id",
            "title",
            "details",
            "regulatory_citation",
            "severity",
            "critical",
            "high",
        ],
    ),
    # ------------------------------------------------------------------ q25
    # Levers: B (prose-ify), D (drop expected values 4/9/72/7/3).
    "q25": (
        "Add `scripts/compute_compliance_metrics.py` (workspace root = first "
        "CLI arg). Reads three files:\n"
        "- `overtime_audit_report.md` — Walsh's manual audit table\n"
        "- `badge_access_analysis.md` — Marcus's badge presence table\n"
        "- `caresched_audit_findings.md` — Angela's formal findings (F1–F4)\n\n"
        "Stdout JSON only. Required keys (snake_case integer values "
        "throughout; the validator pins each):\n"
        "- `finding_count` — integer, count of formal findings in the "
        "findings doc\n"
        "- `nurses_affected` — integer, count of staff nurses whose hours "
        "were systematically understated (from the F2 finding)\n"
        "- `months_of_falsification` — integer, span of the systematic "
        "falsification per the F2 finding\n"
        "- `mandatory_reporting_hours` — integer, the deadline-hours window "
        "associated with the patient-safety RCW (from the findings doc)\n"
        "- `violations_above_48h` — integer, count of nurses exceeding the "
        "48 h/week ceiling per the audit\n"
        "- `violations_above_60h` — integer, count of nurses in the 60+ "
        "h/week tier per the audit",
        [
            "scripts/compute_compliance_metrics.py",
            "overtime_audit_report.md",
            "badge_access_analysis.md",
            "caresched_audit_findings.md",
            "finding_count",
            "nurses_affected",
            "months_of_falsification",
            "mandatory_reporting_hours",
            "violations_above_48h",
            "violations_above_60h",
        ],
    ),
    # ------------------------------------------------------------------ q26
    # Levers: D (strip "scheduled hours" / "clean numbers" — agent must
    # read caresched_audit_findings.md to find Linda Yee's quoted instruction).
    "q26": (
        "F1 hinges on the instruction Linda Yee gave staff. Walk it through "
        "carefully at `analysis/linda_yee_instruction_analysis.md`:\n\n"
        "1. quote or accurately paraphrase Linda Yee's instruction — the "
        "exact phrasing is preserved verbatim in the F1 section of "
        "`caresched_audit_findings.md`. Two key snippets from her quote are "
        "what the validator greps for (one is about which kind of hours "
        "the charge nurses were told to enter; the other is about what the "
        "administration purportedly needed). Copy the snippets out of the "
        "findings doc rather than paraphrasing\n"
        "2. lay out the accountability chain: Linda Yee (charge nurse) gave "
        "the instruction; the staff nurses on her shifts followed it\n"
        "3. reference Linda Yee's `charge nurse` role explicitly and the "
        "authority that role carries over CareScheduler data entry\n"
        "4. at least two `##` section headings\n\n"
        "Tone is observational, not prosecutorial — F1 is a finding of fact, "
        "not (yet) a personnel action.",
        [
            "analysis/linda_yee_instruction_analysis.md",
            "Linda Yee",
            "charge nurse",
        ],
    ),
    # ------------------------------------------------------------------ q27
    # v3 levers stacked: D++ (drop the explicit RCW/WAC/integer-look-up
    # coaching; force agent to derive deadline_hours/threshold_hours/
    # violated_by_count from workspace), C++ (3 hedged distractors: Min-Ji
    # on deadline being 24 h, Sam on threshold being 40 h, Tanaka on
    # violated_by_count being a different integer), F (mask findings doc and
    # icu_staffing_policy.md filenames), G (collapse bullet schema into
    # paragraph), H (don't restate "true"/"false" boolean obvious — just say
    # "set the operative-statute flag honestly"; agent must reason which is
    # operative).
    "q27": (
        "Jennifer Wu (Legal) needs a paper trail before the patient-safety "
        "RCW's mandatory-reporting clock runs out. Two artefacts.\n\n"
        "**File 1:** `docs/YYYY-MM-DD_mandatory_reporting_memo.md` (real "
        "calendar date in the prefix; the `_mandatory_reporting_memo.md` "
        "stem is what our tooling globs for, please don't rename it). The "
        "memo needs to cite the WA patient-safety event statute by its full "
        "RCW code (the formal findings doc that just landed names it "
        "explicitly — copy the code verbatim from there) and state the "
        "mandatory-reporting deadline window in bare hours as an integer "
        "(the unit policy doc and the findings doc both quote that "
        "deadline). Generous heading structure — this goes to Legal, so it "
        "needs to read as a memo, not a paragraph.\n\n"
        "**File 2:** `analysis/regulatory_citation_index.json`\n"
        "Machine-readable index of the three statutes that touch this case. "
        "JSON object with exactly three top-level keys; each value is a "
        "nested object. The top-level keys are conventional snake-case "
        "renderings of statute codes, formed by lowercasing the prefix and "
        "joining the dotted-decimal segments with underscores — they are: "
        "`rcw_70_41_230`, `wac_246_840_711`, `rcw_49_28_140`. The patient-"
        "safety RCW's nested object carries a short `topic` string, an "
        "integer `deadline_hours` matching the RCW's deadline window, and a "
        "boolean `triggered` flag set honestly (this is the operative "
        "statute here). The weekly-maximum WAC's nested object carries "
        "`topic`, `threshold_hours` (integer matching the weekly-hours "
        "ceiling), and `violated_by_count` (integer count of nurses on the "
        "unit in violation per the audit table). The third statute "
        "(`rcw_49_28_140`) carries `topic` and `triggered` only — set the "
        "boolean honestly given that this one is not the operative anchor "
        "for our case. Field names exact across all three nested objects.\n\n"
        "Three things you can ignore once you've checked the source: Min-Ji "
        "remembered the mandatory-reporting clock as a 24-hour window "
        "(faster than what the actual RCW says, I think); Sam thought the "
        "WAC's weekly ceiling was 40, the way the older private-sector "
        "wage-hour rules work; Tanaka counted 5 nurses in violation off "
        "the top of his head. Use the audit table and the policy / "
        "findings docs as ground truth — don't trust my colleagues' "
        "back-of-envelope numbers here.",
        [
            "docs/",
            "YYYY-MM-DD_mandatory_reporting_memo.md",
            "analysis/regulatory_citation_index.json",
            "rcw_70_41_230",
            "wac_246_840_711",
            "rcw_49_28_140",
            "deadline_hours",
            "threshold_hours",
            "violated_by_count",
            "triggered",
            "topic",
        ],
    ),
    # ------------------------------------------------------------------ q29
    # Levers: A (strip P1-P5 labels — describe rules in prose),
    # D (strip 68.4, "7", regs).
    "q29": (
        "Final deliverable. One canonical compliance report at "
        "`docs/YYYY-MM-DD_final_compliance_report.md` (real date in the "
        "prefix; the `_final_compliance_report.md` stem is globbed). The "
        "report is graded against the team's house-style preference rules "
        "for clinical compliance documents — make sure all five of the "
        "following are satisfied:\n\n"
        "- contrast the badge / Walsh audit (`actual` hours) against the "
        "CareScheduler feed (`reported` hours); both source kinds must be "
        "named and the comparison language must use both terms within "
        "close proximity\n"
        "- include at least two h/week metric expressions in the prose "
        "(things like `<float> h/week`)\n"
        "- the file lives in `docs/` with the YYYY-MM-DD_ date prefix "
        "(you're already on it)\n"
        "- include explicit cross-verification language — at least one of "
        "`cross-verified`, `corroborated`, `independently confirmed`, "
        "`both sources`, or `cross-validation`\n"
        "- cite both the WA nursing weekly-maximum statute (WAC code) and "
        "the WA patient-safety event statute (RCW code) by their full codes\n\n"
        "Additional content requirements:\n"
        "- state Amy Chen's actual h/week as a standalone single-decimal "
        "float (copy from `overtime_audit_report.md`)\n"
        "- state the count of nurses exceeding the 48 h/week threshold as "
        "a standalone digit\n"
        "- reference the documented near-miss events (the phrase `near-miss` "
        "or the event id `NM-1` works)\n"
        "- at least five `##` section headings\n"
        "- document length at least 800 characters\n\n"
        "This is the artefact that goes to the state. Do not hedge "
        "regulatory citations and do not rely on CareScheduler as ground "
        "truth anywhere in it.",
        [
            "docs/",
            "YYYY-MM-DD_final_compliance_report.md",
            "actual",
            "reported",
            "cross-verified",
            "h/week",
            "near-miss",
            "NM-1",
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
        missing = [tok for tok in must_keep if tok not in new_text]
        if missing:
            failed.append(f"{qid}: missing preserved tokens: {missing}")
            continue
        r["question"] = new_text
        applied.append(qid)

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
