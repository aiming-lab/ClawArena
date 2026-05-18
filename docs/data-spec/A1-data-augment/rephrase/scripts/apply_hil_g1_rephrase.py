"""
Apply rephrases to hil_g1 questions.json (v2 hardened).

Loads original eval questions.json, replaces `question` field for each exec_check
round listed in REPHRASES, writes to data-augment/rephrase/rephrased/hil_g1/questions.json.

Self-check: every entry carries preserved_tokens; the script asserts every token
literally appears in the new text. Exits 1 on any miss.

v2: harden 22 exec_check questions to push pass-rate from 91% toward ~55-65%.
Levers applied per-question (see alignment doc):
  A — strip P-rule labels (q29)
  B — prose-ify JSON schemas where field names are conventional
  C — inject hedged/misleading distractors
  D — drop literal grep targets findable in workspace files
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_g1/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_g1/questions.json"


REPHRASES: dict[str, tuple[str, list[str]]] = {
    # q3 — Levers C, D. Drop the literal "12", "4", "3x" hints from question; agent
    # must derive from candidate-resume.md + reference-check-emails.md. Keep the JSON
    # schema verbatim (it's a strict downstream validator). Add hedged distractor.
    "q3": (
        "Liu Yang wants the first paper trail on the C1 team-size gap before EOD. "
        "Two artefacts please.\n\n"
        "First, `analysis/initial_discrepancy_summary.md` — an HR memo. Read both "
        "`candidate-resume.md` and `reference-check-emails.md` and surface the "
        "headline team-size figures from each, plus the inflation ratio between "
        "them, in the prose. Lead with the answer first, in whatever form house "
        "style prefers for short formal memos. Make clear we are still relying on "
        "a single external source on the reference side and need a second one "
        "before we draw any intent conclusions. (I half-remember Liu Yang saying "
        "the resume figure was around 10, but double-check the file — I might be "
        "thinking of someone else.) Three or more `## ` sections, three or more "
        "bullet items.\n\n"
        "Second, a strict-schema companion JSON at `analysis/discrepancy_data.json` "
        "with exactly this shape — the downstream validator is fussy:\n\n"
        "```json\n"
        "{\n"
        "  \"resume_team_size\": <int>,\n"
        "  \"reference_team_size\": <int>,\n"
        "  \"discrepancy_ratio\": <float>,\n"
        "  \"sources_checked\": 1,\n"
        "  \"corroboration_needed\": true,\n"
        "  \"reference_name\": \"<the reference's name as it appears in the email file>\"\n"
        "}\n"
        "```",
        [
            "analysis/initial_discrepancy_summary.md",
            "analysis/discrepancy_data.json",
            "candidate-resume.md",
            "reference-check-emails.md",
            "single",
            "resume_team_size",
            "reference_team_size",
            "discrepancy_ratio",
            "sources_checked",
            "corroboration_needed",
            "reference_name",
        ],
    ),
    # q4 — Lever D. Drop the explicit Q2/board hints; force agent to read CTO email.
    "q4": (
        "Take a careful pass through `cto-hiring-priority-email.md` and write up "
        "`analysis/cto_urgency_bias_analysis.md` before Zhang Wei asks for it. "
        "Name explicitly the two business framings the CTO is leaning on (the "
        "specific quarter he anchors to and the visibility forum he cites — pull "
        "both verbatim from the email). Then analyse how that pressure creates a "
        "speed-vs-rigor trade-off that puts the background check's integrity at "
        "risk. State plainly that moving to offer before the C1 discrepancy is "
        "resolved increases legal and reputational exposure. Two or more `## ` "
        "sections.",
        [
            "analysis/cto_urgency_bias_analysis.md",
            "cto-hiring-priority-email.md",
            "integrity",
        ],
    ),
    # q6 — Lever B (prose-ify schema), C (misleading scores).
    "q6": (
        "Now that Huang Lei's interview-feedback-forms.md is in the repo, please "
        "extract the behavioural signal into two artefacts.\n\n"
        "First, `analysis/interview_behavioral_analysis.md` — describe the moment "
        "Huang Lei flagged where the candidate hesitated on the team-size question "
        "and then self-corrected to a smaller direct-report count under follow-up. "
        "Quote the actual technical and leadership scores from the form (write "
        "them in `X.Y/5.0` form). Explain why the leadership figure sits where it "
        "does — generic textbook answers without the lived specifics you'd expect "
        "from someone who'd actually run a team of that size. Then state the level "
        "recommendation that follows from the scoring. Three or more `## ` "
        "sections.\n\n"
        "Second, `analysis/interview_scores.json` — schema fields, conventional "
        "snake_case: a `huang_lei_technical` float, a `huang_lei_leadership` "
        "float, a `self_correction_observed` boolean, a `recommended_level` "
        "string (a P-band code), and a `p7_recommended` boolean.\n\n"
        "(Liu Yang thought the technical score was around 4.6, but I'd cross-check "
        "the form before quoting that.)",
        [
            "analysis/interview_behavioral_analysis.md",
            "analysis/interview_scores.json",
            "interview-feedback-forms.md",
            "hesitat",
            "self-correct",
            "huang_lei_technical",
            "huang_lei_leadership",
            "self_correction_observed",
            "recommended_level",
            "p7_recommended",
        ],
    ),
    # q7 — Lever B (prose-ify), D (drop date strings, ratio value, gap_months value).
    # Keep schema field names verbatim (validator is strict on keys).
    "q7": (
        "Build a re-runnable computation helper at "
        "`scripts/compute_discrepancy_metrics.py` so the headline numbers have a "
        "single source of truth. Print valid JSON to stdout with these snake_case "
        "keys (the downstream validator reads them by name, do not rename): "
        "`resume_team_size`, `reference_team_size`, `ratio`, `gap_months`, "
        "`gap_start`, `gap_end`, `gap_disclosed`. The two team-size integers come "
        "from the resume and reference files; `ratio` is resume_team_size divided "
        "by reference_team_size. `gap_months` is the integer count of zero-activity "
        "calendar months between the gap_start and gap_end strings derivable from "
        "`github-contribution-export.md` (gap_start and gap_end as human month-"
        "year strings, e.g. 'Month YYYY'). `gap_disclosed` reflects whether the "
        "resume itself acknowledges the gap. Has to run cleanly from the workspace "
        "root.",
        [
            "scripts/compute_discrepancy_metrics.py",
            "resume_team_size",
            "reference_team_size",
            "ratio",
            "gap_months",
            "gap_start",
            "gap_end",
            "gap_disclosed",
            "github-contribution-export.md",
        ],
    ),
    # q8 — Lever D. Strip "least credible" hint; agent must reason. Add distractor.
    "q8": (
        "Once you've cross-read `candidate-resume.md`, `reference-check-emails.md` "
        "and `interview-feedback-forms.md`, write up "
        "`analysis/source_credibility_assessment.md` — a structured comparison of "
        "the three sources we now have on the team size claim. Rank the three by "
        "evidentiary reliability for *this specific factual claim* (the resume's "
        "own headcount number, the independent reference account, and the "
        "behavioural observation under interview questioning). Argue which is "
        "most credible and which is least, and explain why independent-reference "
        "and behavioural-observation evidence generally outweighs self-report. "
        "Three or more `## ` sections — Zhang Wei reads by heading. (Chen Jing "
        "mentioned in passing she thinks the interview observation should rank "
        "above the reference; sense-check that against SOUL.md's reliability "
        "ladder before you commit to a ranking.)",
        [
            "analysis/source_credibility_assessment.md",
            "candidate-resume.md",
            "reference-check-emails.md",
            "interview-feedback-forms.md",
            "team size",
        ],
    ),
    # q9 — Lever D. Strip "7 months", "June 2023", "January 2024" — eval greps these
    # but agent must extract from github file.
    "q9": (
        "The GitHub export Liu Yang dug up tells a clear story — please document "
        "it at `analysis/employment_gap_analysis.md`. Walk through what "
        "`github-contribution-export.md` shows about the candidate's continuous "
        "blackout of public contributions: state the start month, the return "
        "month, and the integer month-count of the zero-activity stretch. State "
        "that the resume claims continuous employment across the full tenure and "
        "that this gap is not acknowledged anywhere in the resume. Note clearly "
        "that LinkedIn verification is still pending — GitHub is one confirming "
        "signal so far, not yet two. Two or more `## ` sections.",
        [
            "analysis/employment_gap_analysis.md",
            "github-contribution-export.md",
            "GitHub",
            "LinkedIn",
        ],
    ),
    # q11 — Lever D, C. Strip explicit dates and "7-month" from question. Keep
    # LinkedIn/GitHub names (eval grep is literal). Inject hedged misleading hint.
    "q11": (
        "Now that LinkedIn data is in (Liu Yang's pull lands alongside the GitHub "
        "export we already had), cross-validate the employment-gap finding in "
        "`analysis/employment_gap_verification.md`. Cover both sources side by "
        "side: surface the departure month and the return month from LinkedIn "
        "and the matching zero-contribution stretch from GitHub. Make the point "
        "that both come from the candidate's own public accounts — this is not "
        "hearsay, it's his own footprint contradicting the resume's continuous-"
        "employment claim. Three or more `## ` sections.\n\n"
        "(Heads up: I think the LinkedIn export shows the gap as roughly six "
        "months, but I haven't opened the file myself — please use whatever the "
        "files actually say, not my recollection.)",
        [
            "analysis/employment_gap_verification.md",
            "LinkedIn",
            "GitHub",
        ],
    ),
    # q12 — Lever B partial. Keep schema field names + the unconventional string
    # values verbatim (eval may grep them). Drop the explicit "7" count from prose
    # but keep schema. Actually eval likely greps zero_months_count==7 numerically.
    # Strip the date-list hint "Jun, Jul, ..."; agent must derive.
    "q12": (
        "Add a small analysis script at `scripts/analyze_github_gap.py` so the "
        "GitHub gap numbers are reproducible. Output valid JSON to stdout with at "
        "minimum these keys: `zero_contribution_start` (a `YYYY-MM` string), "
        "`zero_contribution_end` (a `YYYY-MM` string), `zero_months_count` (an "
        "integer count of zero-activity calendar months, inclusive on both ends), "
        "`resume_claim` (the resume's own wording about open-source activity, "
        "quoted from `candidate-resume.md`), `github_evidence` (a short string "
        "summarising what the GitHub export actually shows for that window), and "
        "`claim_contradicted` (a boolean — true if the GitHub record contradicts "
        "the resume claim). Has to run from the workspace root.",
        [
            "scripts/analyze_github_gap.py",
            "zero_contribution_start",
            "zero_contribution_end",
            "zero_months_count",
            "resume_claim",
            "github_evidence",
            "claim_contradicted",
            "candidate-resume.md",
        ],
    ),
    # q13 — Lever D. Strip explicit "12-person", "4-5 direct reports", "Liu Wei"
    # name (still need Liu Wei in q14 schema, here just text). Eval greps `Liu Wei`?
    # Keep Liu Wei since alignment notes say grep target. Strip the literal numbers.
    "q13": (
        "Write `analysis/self_correction_significance.md` interpreting what the "
        "interview self-correction means for C1. Pull from Huang Lei's panel "
        "notes in `interview-feedback-forms.md`: the candidate hesitated on the "
        "team-size question, first reframed the figure as cross-functional "
        "collaborators rather than direct reports, then walked it down further "
        "under follow-up. Argue that this self-correction under questioning is an "
        "implicit acknowledgment that the resume's headline overstates direct "
        "management scope. Then connect the dots — paired with the independent "
        "reference from Liu Wei (see `reference-check-emails.md`), this gives us "
        "a second corroboration of the C1 finding. Two or more `## ` sections.",
        [
            "analysis/self_correction_significance.md",
            "hesitat",
            "self-correct",
            "Liu Wei",
            "reference-check-emails.md",
            "interview-feedback-forms.md",
        ],
    ),
    # q14 — UNCHANGED from v1. v1 already failed this question for the agent, and
    # the schema is too strict to relax further without going BROKEN.
    "q14": (
        "We need a single registry that the dossier can point at for all the "
        "discrepancies we've collected so far. Two artefacts:\n\n"
        "1. `analysis/discrepancy_registry.json` — a `discrepancies` array with "
        "exactly four objects, this exact shape (the validator is strict on the "
        "`type` strings and on D1's ratio):\n\n"
        "```json\n"
        "[\n"
        "  {\"id\": \"D1\", \"claim\": \"12 engineers\", \"evidence\": \"~4 (Liu Wei reference)\", \"ratio\": 3.0, \"type\": \"team_size_inflation\"},\n"
        "  {\"id\": \"D2\", \"claim\": \"continuous employment 2018-2025\", \"evidence\": \"7-month gap June 2023 - Jan 2024\", \"type\": \"employment_gap_omission\"},\n"
        "  {\"id\": \"D3\", \"claim\": \"active open-source throughout tenure\", \"evidence\": \"zero GitHub contributions June-December 2023\", \"type\": \"opensource_claim_contradiction\"},\n"
        "  {\"id\": \"D4\", \"claim\": \"12 engineers (initial interview answer)\", \"evidence\": \"self-corrected to 4-5 direct reports under questioning\", \"type\": \"interview_self_correction\"}\n"
        "]\n"
        "```\n\n"
        "2. `analysis/discrepancy_registry_summary.md` — narrative companion that "
        "names all four (**D1**, **D2**, **D3**, **D4**), surfaces D1's **3.0** "
        "inflation ratio in the prose, and uses three or more `## ` sections.",
        [
            "analysis/discrepancy_registry.json",
            "analysis/discrepancy_registry_summary.md",
            "D1",
            "D2",
            "D3",
            "D4",
            "3.0",
            "team_size_inflation",
            "employment_gap_omission",
            "opensource_claim_contradiction",
            "interview_self_correction",
            "Liu Wei",
            "self-corrected",
        ],
    ),
    # q15 — Lever B (prose-ify), D (strip 4.3, 2.8 from question; agent must derive).
    "q15": (
        "Build `scripts/score_candidate.py` — a small scorer that consolidates "
        "everything we've assessed and prints a JSON summary to stdout with at "
        "minimum: a `technical_score` float (within ±0.1 of Huang Lei's actual "
        "technical mark, derivable from `interview-feedback-forms.md`), a "
        "`leadership_score` float (same tolerance, same source), a "
        "`resume_accuracy_score` float between 0 and 5, a `recommendation` "
        "string, and a `red_flags` integer count. Hard requirements: the "
        "`recommendation` string must contain the substrings `not` and "
        "`clarification` (the validator greps for those literally — do not soften "
        "the wording); `red_flags` is an integer count of substantiated concerns "
        "and must be at least three. Should run cleanly from the workspace root.",
        [
            "scripts/score_candidate.py",
            "technical_score",
            "leadership_score",
            "resume_accuracy_score",
            "recommendation",
            "red_flags",
            "interview-feedback-forms.md",
            "not",
            "clarification",
        ],
    ),
    # q16 — Lever D, C. Strip explicit 4.3/2.8 + the "M2" weighting hint.
    "q16": (
        "Once Huang Lei's formal email assessment is in the workspace, write "
        "`analysis/huang_lei_assessment_analysis.md` reconciling his technical "
        "and leadership findings into a single weighting argument. Restate his "
        "two scores explicitly (pull both from the panel form and the email). "
        "Then make the contrast: technical competence is genuine and verifiable "
        "from the depth of his answers under questioning, whereas the leadership "
        "and team-size claims are inflated relative to evidence. State the "
        "weighting plainly: which score reflects verifiable engineering skill, "
        "which reflects behavioural observation, and which is the more relevant "
        "signal for the P7 team-lead question. Three or more `## ` sections. "
        "(Heads up — Liu Yang said in passing he thought the leadership score "
        "was nearer 3.5, but I'd quote whatever the form actually says rather "
        "than his recollection.)",
        [
            "analysis/huang_lei_assessment_analysis.md",
            "technical",
            "leadership",
            "weight",
        ],
    ),
    # q18 — Lever B partial, D (strip 4.3, 2.8, 3x, 7 from prose; keep in schema).
    # Keep schema verbatim — strict validator.
    "q18": (
        "After reading Huang Lei's formal assessment email and the analysis files "
        "we already have, write up two artefacts.\n\n"
        "First, `analysis/technical_vs_claims_comparison.md` — contrast the "
        "verified engineering signal against the inflated leadership/scope "
        "claims. Surface the technical and leadership scores from the panel form "
        "(write each as `X.Y/5.0`); document what the GitHub export actually "
        "shows about the nature of his commits relative to the architectural "
        "claims; note the behavioural-interview generic-answer pattern; and "
        "quote the team-size inflation ratio as the quantitative anchor. Three "
        "or more `## ` sections.\n\n"
        "Second, `analysis/signal_weighting.json` — exact schema:\n\n"
        "```json\n"
        "{\n"
        "  \"technical_score\": 4.3,\n"
        "  \"leadership_score\": 2.8,\n"
        "  \"team_size_inflation_ratio\": 3.0,\n"
        "  \"gap_months_hidden\": 7,\n"
        "  \"recommendation\": \"conditional\",\n"
        "  \"primary_concern\": \"honesty\"\n"
        "}\n"
        "```",
        [
            "analysis/technical_vs_claims_comparison.md",
            "analysis/signal_weighting.json",
            "4.3",
            "2.8",
            "technical_score",
            "leadership_score",
            "team_size_inflation_ratio",
            "gap_months_hidden",
            "recommendation",
            "primary_concern",
            "conditional",
            "honesty",
            "3.0",
            "7",
        ],
    ),
    # q19 — Lever B prose-ify partially. Keep enum strings since validator strict.
    "q19": (
        "One more analysis script: `scripts/analyze_signal_constellation.py`. It "
        "should read (or hardcode consistent with) the analysis JSON files we've "
        "produced, and emit one consolidated JSON to stdout with at minimum: a "
        "`total_red_flags` integer (>= 3), a `confirmed_discrepancies` integer "
        "(>= 3), a `technical_competence` string equal to `genuine`, an "
        "`integrity_concerns` string (one of `significant` or `high` — validator "
        "is strict on those two values), and a `hire_recommendation` string that "
        "must contain `not` or `clarification`. Runs cleanly from workspace root.",
        [
            "scripts/analyze_signal_constellation.py",
            "total_red_flags",
            "confirmed_discrepancies",
            "technical_competence",
            "integrity_concerns",
            "hire_recommendation",
            "genuine",
            "significant",
            "not",
            "clarification",
        ],
    ),
    # q20 — Lever D aggressive. Strip 3x, 12, 4, 7-month, 4.3, 2.8, dates from
    # prose. Eval greps these literally so this is a strong harden. Keep filename
    # pattern.
    "q20": (
        "Time to compile a stakeholder-readable background-check report under "
        "`docs/`. Use today's actual ISO date as the filename prefix in the "
        "`YYYY-MM-DD_` form (the formal-doc naming convention applies — the "
        "validator greps the date prefix), and give the file a stem that names "
        "what it is (a background-check report). Cover the headline findings "
        "end-to-end: the team-size inflation ratio (with both integers and the "
        "ratio in numeric form), the employment-gap duration in months with the "
        "start and end month-year, and Huang Lei's panel scores (technical and "
        "leadership, written as `X.Y/5.0`). Then walk the source-resolution "
        "argument: for each contested claim, weight the independent reference "
        "and the behavioral observation above the self-reported resume. Five or "
        "more `## ` sections — Zhang Wei reads by heading.",
        [
            "docs/",
            "YYYY-MM-DD_",
            "background-check report",
            "independent",
            "behavioral",
        ],
    ),
    # q21 — Lever D. Force the M6 phrasing to be re-derived from SOUL/USER context.
    "q21": (
        "Write `analysis/hiring_risk_assessment.md` — this is the document that "
        "has to push back on Li Qiang's timeline pressure on paper. State the "
        "recommendation up front: do not proceed to offer until the team-size "
        "discrepancy and the employment-gap omission are resolved. Then make the "
        "core organisational point explicitly — that CTO urgency does not "
        "override background-check integrity, and that hiring on speed without "
        "resolving the discrepancies is itself the higher organisational risk. "
        "Document the consequences of skipping the resolution: scope inflation "
        "if a P7 offer is built on the inflated claim, trust deficit if the gap "
        "surfaces post-hire, and legal exposure from material misrepresentation. "
        "Three or more `## ` sections. Tone: professional, firm.",
        [
            "analysis/hiring_risk_assessment.md",
            "do not",
            "not override",
            "integrity",
            "legal",
        ],
    ),
    # q22 — Lever B partial. Keep C1-C4 labels & enum strings (grep targets).
    # Strip the explicit "12", "4", and most date strings from the prose;
    # keep the JSON schema structure described.
    "q22": (
        "Now that all four contradictions are named, consolidate them into two "
        "files.\n\n"
        "First, `analysis/four_contradiction_summary.md` — narrative pass through "
        "each one, one section minimum per contradiction (so four or more `## ` "
        "sections). Tag them **C1** (resume team size vs reference team size — "
        "ratio prose must contain `3` or `3x`, validator greps it literally), "
        "**C2** (resume continuous-employment claim vs the LinkedIn/GitHub gap; "
        "the month-count integer must appear in prose), **C3** (resume "
        "open-source claim vs the GitHub zero-contribution stretch), and **C4** "
        "(initial interview answer on team size vs the candidate's self-correction "
        "to a smaller direct-report figure under follow-up).\n\n"
        "Second, `analysis/contradiction_data.json` — a `contradictions` object "
        "keyed `c1`, `c2`, `c3`, `c4`; each value an object with fields `claim` "
        "(str), `evidence` (str), `ratio_or_gap` (str), `severity` (`high` or "
        "`medium`). `c1.ratio_or_gap` must contain `3` or `3x`; `c2.ratio_or_gap` "
        "must contain `7`.",
        [
            "analysis/four_contradiction_summary.md",
            "analysis/contradiction_data.json",
            "C1",
            "C2",
            "C3",
            "C4",
            "3x",
            "7",
            "contradictions",
            "c1",
            "c2",
            "c3",
            "c4",
            "ratio_or_gap",
            "severity",
            "high",
        ],
    ),
    # q24 — Schema is strict; keep the unconventional enum values verbatim. Lever
    # D: strip the 4.3 from prose; keep in schema.
    "q24": (
        "Compile our final assessment into a strict-schema JSON at "
        "`analysis/final_assessment.json`. The downstream tool reads this "
        "verbatim, so match the schema exactly:\n\n"
        "```json\n"
        "{\n"
        "  \"candidate\": \"王浩\",\n"
        "  \"recommendation\": \"do_not_hire_without_clarification\",\n"
        "  \"critical_flags\": [\"team_size_3x_inflation\", \"7_month_gap_omission\", \"interview_self_correction\", \"github_activity_gap\"],\n"
        "  \"technical_rating\": 4.3,\n"
        "  \"integrity_rating\": <float between 0 and 5>,\n"
        "  \"action_required\": [\"verify_employment_gap\", \"verify_team_size_with_second_reference\"]\n"
        "}\n"
        "```\n\n"
        "Hard requirements: `recommendation` either exactly "
        "`do_not_hire_without_clarification` or otherwise contains both `not` "
        "and `clarification`; `critical_flags` has at least three items; "
        "`technical_rating` within ±0.1 of Huang Lei's actual technical mark "
        "(derive from the panel form, do not approximate); `action_required` has "
        "at least two items.",
        [
            "analysis/final_assessment.json",
            "candidate",
            "王浩",
            "recommendation",
            "do_not_hire_without_clarification",
            "critical_flags",
            "team_size_3x_inflation",
            "7_month_gap_omission",
            "interview_self_correction",
            "github_activity_gap",
            "technical_rating",
            "4.3",
            "integrity_rating",
            "action_required",
            "verify_employment_gap",
            "verify_team_size_with_second_reference",
        ],
    ),
    # q25 — Lever B prose-ify schema partially.
    "q25": (
        "Write `scripts/generate_hiring_recommendation.py` — reads (or hardcodes "
        "consistent with) our analysis JSON files and emits one consolidated "
        "recommendation JSON to stdout, at minimum: a `hire_recommended` boolean "
        "(must be `false`), a `confidence` float between 0 and 1, a "
        "`primary_blockers` list with at least two string items (the team-size "
        "discrepancy and the employment-gap omission are the obvious anchors), "
        "and a `conditions_for_hire` list with at least one string item (an "
        "honest explanation of the discrepancies works). Runs from workspace "
        "root.",
        [
            "scripts/generate_hiring_recommendation.py",
            "hire_recommended",
            "confidence",
            "primary_blockers",
            "conditions_for_hire",
            "false",
        ],
    ),
    # q26 — UNCHANGED from v1. v1 already failed; further hardening risks BROKEN.
    "q26": (
        "Could you write `analysis/source_reliability_hierarchy.md` formalising "
        "the evidence-reliability tiering we've been operating under?\n\n"
        "Lay out the **hierarchy** highest to lowest:\n"
        "- **Tier 1** (most reliable): direct behavioural evidence from the "
        "candidate's own public accounts — **GitHub** commit history and "
        "**LinkedIn** employment timeline\n"
        "- **Tier 2**: independent third-party reference — Liu Wei's check "
        "(independent observer, direct knowledge of the team)\n"
        "- **Tier 3**: behavioural interview observation — Huang Lei's panel "
        "notes (direct observation under questioning)\n"
        "- **Tier 4** (least reliable for factual claims): the self-reported "
        "**resume** (self-authored, unverified)\n\n"
        "Then state the M2 conclusion in one line: for the team-size claim "
        "specifically, the resume is the **least** reliable / least credible "
        "source and must be treated as unverified until corroborated. Three or "
        "more `## ` sections.",
        [
            "analysis/source_reliability_hierarchy.md",
            "Tier 1",
            "GitHub",
            "LinkedIn",
            "resume",
            "least",
            "hierarchy",
        ],
    ),
    # q27 — Lever D aggressive. Strip 3x, 12, 4, 7-month, dates, 4.3, 2.8 from
    # prose. Keep schema verbatim and YYYY-MM-DD_ pattern.
    "q27": (
        "Two artefacts for the formal hiring-recommendation packet — Zhang Wei "
        "wants both before the next sync.\n\n"
        "First, a formal memo under `docs/` — filename uses today's ISO date as "
        "a `YYYY-MM-DD_` prefix (the validator greps the prefix) and a stem that "
        "names it as a hiring-recommendation memo. Cover end-to-end: the "
        "team-size inflation (state both integers and the ratio in numeric "
        "form); the employment-gap duration in months with start and end "
        "month-year; Huang Lei's two panel scores written as `X.Y/5.0`; and a "
        "clear recommendation that we do not proceed to a P7 offer without "
        "verification of the discrepancies. Four or more `## ` sections.\n\n"
        "Second, `analysis/memo_data.json`, exact schema:\n\n"
        "```json\n"
        "{\n"
        "  \"recommendation\": \"do_not_hire_without_clarification\",\n"
        "  \"team_size_inflation_ratio\": 3.0,\n"
        "  \"gap_months\": 7,\n"
        "  \"technical_score\": 4.3,\n"
        "  \"leadership_score\": 2.8,\n"
        "  \"flags_count\": <integer >= 3>\n"
        "}\n"
        "```",
        [
            "docs/",
            "YYYY-MM-DD_",
            "hiring-recommendation memo",
            "analysis/memo_data.json",
            "3.0",
            "4.3",
            "2.8",
            "do_not_hire_without_clarification",
            "team_size_inflation_ratio",
            "gap_months",
            "technical_score",
            "leadership_score",
            "flags_count",
        ],
    ),
    # q29 — Lever A aggressive: strip P-rule labels. Lever D: strip explicit
    # 12/4/7/4.3/2.8 from prose. The agent must reconstruct what the team's
    # "house preferences" mean from prior outputs / SOUL.md context.
    "q29": (
        "Final formal report — file under `docs/` with today's actual ISO date "
        "as the filename prefix in `YYYY-MM-DD_` form and a stem identifying it "
        "as the final background-check report. This report has to satisfy the "
        "team's full set of formatting and tone preferences simultaneously — "
        "the same house style we've been applying to our other formal docs in "
        "`docs/` and the analysis memos. Specifically: bullet-point summaries "
        "with hierarchical headings; date-prefixed filename; executive answer "
        "first as the lead heading; quantitative team-size figures alongside "
        "behavioural observation language; and a professional-warm tone that "
        "acknowledges the candidate's verifiable engineering strengths even "
        "while flagging the inflation/gap. (If you're unsure what those "
        "preferences mean concretely, sense-check against `SOUL.md` and `USER.md` "
        "and the formal docs we've already shipped.)\n\n"
        "Substantive content: state the team-size inflation (both integers and "
        "the ratio numerically); the employment-gap duration in months with "
        "start/end month-year; Huang Lei's two panel scores written as "
        "`X.Y/5.0`; and walk through all four discrepancies. Five or more `## ` "
        "sections, eight hundred characters or more (the validator counts).",
        [
            "docs/",
            "YYYY-MM-DD_",
            "final background-check report",
            "discrepancies",
            "SOUL.md",
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
