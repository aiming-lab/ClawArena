"""
Apply pilot rephrases to hil_s1 questions.json (v1).

Loads original eval questions.json, replaces `question` field for each exec_check
round listed in REPHRASES, writes to data-augment/rephrase/rephrased/hil_s1/questions.json.

Self-check: for every replaced question, asserts that all preserved tokens listed
in PRESERVE remain literally present (paths, schema field names, filename patterns,
P-rules, etc.).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_s1/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_s1/questions.json"

# Each entry: id -> (new_question_text, [tokens that MUST appear literally in new text])
REPHRASES: dict[str, tuple[str, list[str]]] = {
    "q2": (
        "hey — can you pin down the three project dates we keep kicking around "
        "(kickoff, interim review, final deliverable) and drop them in "
        "`project/docs/milestones.json`? Just these three keys, ISO date strings:\n\n"
        "```json\n"
        "{\n"
        "  \"final_deadline\": \"YYYY-MM-DD\",\n"
        "  \"interim_review\": \"YYYY-MM-DD\",\n"
        "  \"kickoff_date\": \"YYYY-MM-DD\"\n"
        "}\n"
        "```\n\n"
        "Numbers have been floating around in slack threads, the kickoff deck, and "
        "meeting_notes — they don't all agree, so trust whatever the formal meeting "
        "minutes / kickoff record say over off-the-cuff DMs. I need to send this "
        "upward by EOD and exec is going to cross-check against their calendar "
        "invite, so double-check before saving.",
        [
            "project/docs/milestones.json",
            "final_deadline",
            "interim_review",
            "kickoff_date",
            "YYYY-MM-DD",
        ],
    ),
    "q3": (
        "Could you put together a `project/docs/metrics_definitions.md` that we can "
        "hand to anyone joining mid-project so they don't redefine the same things? "
        "Single source of truth for how we compute the headline numbers — at minimum:\n"
        "- the **churn rate** definition, including the inactivity threshold (state "
        "the exact day count from `data_dictionary.md` — Maya's been quoting a "
        "different number in DMs and I want this doc to match the documented one) "
        "and the actual formula for the rate\n"
        "- **average monthly spend**, with the dataset size called out\n"
        "- **data coverage period** for what's in the transactions table\n"
        "- whatever else you think a new analyst would ask about on day one\n\n"
        "Stick to the **P1** formatting rules in `style_guide.md` (numbers ≥ 1,000 "
        "and timestamps both have specific shapes there) — Alex flagged a P1 "
        "violation in last week's draft and is going to grep this one too. Quote "
        "the threshold using the same phrasing the data dictionary uses; the "
        "downstream linter is unforgiving on that wording.",
        [
            "project/docs/metrics_definitions.md",
            "churn",
            "P1",
            "data_dictionary.md",
        ],
    ),
    "q7": (
        "Now that the schema changelog is in the repo, we should bring "
        "`project/docs/data_dictionary.md` up to v2 so docs stop drifting from "
        "the actual CSV headers. Add whatever's new in the v2 schema (the changelog "
        "spells it out exactly — please don't infer it from memory), and keep a "
        "frozen snapshot next to the live doc using our P2 versioned-copy "
        "convention: same `data_dictionary` stem, today's date prefix, `_v2.md` "
        "suffix → `project/docs/YYYY-MM-DD_data_dictionary_v2.md`.\n\n"
        "I know it's been a thrash week with the field-name confusion (totally my "
        "verbal slip, sorry team), so feel free to drop a one-liner in the Change "
        "History section pointing at the changelog if it'll save the next reader "
        "five minutes.",
        [
            "project/docs/data_dictionary.md",
            "YYYY-MM-DD_data_dictionary_v2.md",
            "data_dictionary",
            "P2",
        ],
    ),
    "q8": (
        "`clean_data.py` is hardwired to the v1 raw file — please point it at the "
        "new raw drop instead and emit the cleaned output at "
        "`data/processed/transactions_v2_clean.csv`. Reuse the existing cleaning "
        "logic end-to-end (date standardisation + drop nulls/negatives on the "
        "revenue column); don't change the semantics, just make sure none of the "
        "new schema bits get accidentally dropped on the way through. Run it once "
        "you're done so the artefact actually lands on disk.\n\n"
        "Heads up: I've seen variants of this script that hardcode a column rename "
        "for the revenue field — if you spot one referencing a column name that "
        "doesn't exist in the CSV header, that's the same bug we already discussed, "
        "just rip it out.",
        [
            "data/processed/transactions_v2_clean.csv",
            "clean_data.py",
        ],
    ),
    "q9": (
        "Let's capture what's still on our plate post-update-1 in a structured doc "
        "the schema validator will actually accept — `project/docs/action_items_u1.json`. "
        "Our intake tool expects the `action_items` schema, which looks like this:\n\n"
        "```json\n"
        "{\n"
        "  \"update\": \"update1\",\n"
        "  \"action_items\": [\n"
        "    {\n"
        "      \"id\": \"string\",\n"
        "      \"description\": \"string\",\n"
        "      \"owner\": \"string\",\n"
        "      \"status\": \"not_started|in_progress|blocked|completed|cancelled|deferred\",\n"
        "      \"due\": \"YYYY-MM-DD\"\n"
        "    }\n"
        "  ]\n"
        "}\n"
        "```\n\n"
        "At least four real items — what's actually open after the schema "
        "clarification, not filler. Owners should be one of the four of us; "
        "anything we've already shipped doesn't belong in here, it just confuses "
        "the next standup. Statuses must come from the enum above (the validator "
        "rejects anything else).",
        [
            "project/docs/action_items_u1.json",
            "update1",
            "action_items",
            "not_started",
            "in_progress",
            "blocked",
            "completed",
            "cancelled",
            "deferred",
            "YYYY-MM-DD",
        ],
    ),
    "q11": (
        "Please add a real test file at `project/tests/test_analysis.py` covering "
        "the correlation function in `analysis_v2.py`. The bare minimum I want "
        "green on `pytest`:\n\n"
        "1. the function returns the expected dict shape — look at the "
        "implementation for the keys, don't assume them\n"
        "2. the `method` field reflects what we landed on after the methodology "
        "correction (not the previous choice)\n"
        "3. the returned correlation value is inside the legitimate mathematical "
        "range\n\n"
        "Since these tests live in the same repo, they have to clear our **P4** "
        "code-style bar too — Alex caught a missing docstring on a test last "
        "sprint, let's not repeat that. Make sure the suite actually runs; I'd "
        "rather see three solid assertions all passing than a long file with "
        "skipped or broken cases.",
        [
            "project/tests/test_analysis.py",
            "P4",
        ],
    ),
    "q12": (
        "Now that the stats method is corrected, we owe a clean writeup of what "
        "changed and what the new numbers actually say. Save it under "
        "`project/reports/` following our **P2** file-naming convention (today's "
        "date prefix, descriptive snake_case topic, `_v<N>.md` suffix), and "
        "structure it per **P3** — Jordan cares about exec-reading flow more than "
        "I do, so make sure the summary lands in the first few sentences.\n\n"
        "Important: be explicit about why the previous draft's numbers shouldn't "
        "be cited going forward. Downstream people may be reading it without "
        "knowing it's superseded; the new file is what we want them pointed at.",
        [
            "project/reports/",
            "P2",
            "P3",
        ],
    ),
    "q13": (
        "I need a stakeholder-facing progress update. Path: "
        "`project/reports/<today>_progress_update_v1.md` — keep that exact "
        "`_progress_update_v1.md` suffix, our tooling globs for it. **P5** "
        "communication rules apply throughout (that whole rule exists precisely "
        "so I don't get questions from Casey about what's verified vs. speculation).\n\n"
        "Cover: where we are post-update-2 (the methodological correction is "
        "worth calling out by name), what's left on the burndown, anything that "
        "could blow up the timeline. Don't dress it up — uncertain things get "
        "tagged accordingly. Keep the opener tight; you know how exec reads, or "
        "doesn't.",
        [
            "project/reports/",
            "_progress_update_v1.md",
            "P5",
        ],
    ),
    "q14": (
        "`project/README.md` is still describing the world before update-2. Fix "
        "the Data section so it reflects the current schema (the new column "
        "matters — anyone running the loader cold will trip on it), and tack on "
        "a `## Project Status` section with where we are right now.\n\n"
        "Stick to **P1**/**P3** in `style_guide.md` — yes the README counts, Alex "
        "has been grading these. The file's been collecting some README-rot; feel "
        "free to tidy obviously-stale lines while you're in there, but please "
        "don't go on a rewrite tear, the diff should be readable.",
        [
            "project/README.md",
            "Project Status",
            "P1",
            "P3",
        ],
    ),
    "q16": (
        "Append a summary row to `project/data/contamination_log.csv` capturing "
        "what we found. Use **2025-03-12** as the detection date (the grep is "
        "literal, so hold that string). Pull the affected-record count, the "
        "contamination rate, and the action-taken text from sources we already "
        "trust — the existing file header notes and Alex's slack thread cover "
        "all of it, please don't make new numbers up.\n\n"
        "P1 date format applies (it's grep-checked). Other columns just match "
        "the schema the rest of the file is using.",
        [
            "project/data/contamination_log.csv",
            "2025-03-12",
            "P1",
        ],
    ),
    "q17": (
        "Once you've internalised the contamination context, draft a team impact "
        "assessment at `project/reports/<date>_impact_assessment_v1.md` (exact "
        "`_impact_assessment_v1.md` suffix — same globbing as the progress update). "
        "**P5** standards apply, this goes to Casey's channel.\n\n"
        "Cover what the duplicate-data discovery means for the analyses already "
        "in flight, where we have to backfill, and what's still safe to cite. "
        "Two paragraphs is enough if they're the right two.",
        [
            "project/reports/",
            "_impact_assessment_v1.md",
            "P5",
        ],
    ),
    "q18": (
        "Write a runnable `project/src/quality_check.py` so we can re-run sanity "
        "checks any time new data drops. At minimum it should: scan for any "
        "duplicate residue, sanity-check date columns, confirm the "
        "**`churn_threshold`** constant matches the project-wide definition (please "
        "pull that from the source of truth, don't hardcode a number you remember "
        "from a meeting), and emit a structured JSON to stdout we can `jq` against. "
        "The threshold check is the one I most want locked in — people have been "
        "reading one value in some places and a different value in others.\n\n"
        "**P4** applies. Run it before calling it done.",
        [
            "project/src/quality_check.py",
            "churn_threshold",
            "P4",
        ],
    ),
    "q21": (
        "End-to-end pipeline at `project/src/run_final_pipeline.py`: load the "
        "latest-and-cleanest transactions file (the deduplicated one is what we "
        "want — accept no substitutes), run the cleaning, then the corrected "
        "churn correlation analysis at the project-standard threshold, and dump "
        "the result to `data/processed/final_results.json`.\n\n"
        "Run it. The downstream readout script reads that JSON and wants to find "
        "the method name, a churn metric, and the threshold somewhere in the "
        "payload — don't strip them out, even if your inner schema-purist twitches.",
        [
            "project/src/run_final_pipeline.py",
            "data/processed/final_results.json",
        ],
    ),
    "q22": (
        "Bring `project/README.md` to its final state for the deliverable. "
        "Reflect that we're on the deduplicated dataset, name the correlation "
        "method we landed on, surface the post-cleanup record count — and yes, "
        "spell it as **39,426** (P1 thousands-sep, the comma is literally "
        "grep-checked, don't write `~39k` or `39426`) — and document the churn "
        "threshold we're going with. **P1**/**P2**/**P3** across the board.\n\n"
        "Casey is reading the README *before* the report deck, so first "
        "impressions count. If anything in there still references the abandoned "
        "methodology, that's the highest-priority fix.",
        [
            "project/README.md",
            "39,426",
            "P1",
            "P3",
        ],
    ),
    "q23": (
        "Closeout email at `project/reports/<today>_project_summary_v1.md` "
        "(exact `_project_summary_v1.md` suffix — tooling). **P5** standards: "
        "opening summary tight, citations on anything specific, [UNVERIFIED] tags "
        "on whatever you don't have a primary source for. Audience is Casey plus "
        "the broader exec channel, so business outcomes lead, methodology is "
        "supporting cast.\n\n"
        "Don't mention internal drama — just the analysis, the corrections we "
        "made, and where we ended up.",
        [
            "project/reports/",
            "_project_summary_v1.md",
            "P5",
        ],
    ),
    "q24": (
        "Future-us is going to want to know why we ended where we ended. Put a "
        "`project/docs/decision_log.md` together that walks through the four key "
        "reversals across the updates: (1) the statistical method change "
        "(name the old method and the new one), (2) the churn threshold "
        "correction (the two day-count thresholds involved, before → after), "
        "(3) the dataset version we ended up on (which raw file the project "
        "started against and which one we settled on), and (4) the recalculated "
        "Q4 baseline (the old percentage and the corrected percentage).\n\n"
        "For each one, document the before-state, the trigger, and the "
        "post-state — and please put the actual values in the doc, not just "
        "topic-level labels. The validator only checks topic keywords, but the "
        "quarterly auditor reading this in three months will be looking for the "
        "specific Pearson/Spearman, the specific day-count change, the specific "
        "raw-file versions, and the specific 9.x% / 8.x% percentages. Tone "
        "matters less than completeness here.",
        [
            "project/docs/decision_log.md",
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
