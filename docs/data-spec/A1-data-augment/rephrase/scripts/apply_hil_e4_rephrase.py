"""
Apply rephrases to hil_e4 questions.json.

v2 hardening pass: strips P-rule labels, prose-ifies several schema blocks where
the field names are conventional, drops more literal grep targets, and injects
mildly misleading hedged distractors. Self-check still asserts every preserved
token appears verbatim. Writes to data-augment/rephrase/rephrased/hil_e4/questions.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_e4/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_e4/questions.json"

REPHRASES: dict[str, tuple[str, list[str]]] = {
    "q3": (
        "Kicking off the Pemberton mid-term review prep — before I touch the formal "
        "compliance memos I want a structured map of every place our three core "
        "intake docs disagree with each other. Read the financial tracking file, "
        "the grant deliverables annex, and the Nairobi field narrative for the "
        "current quarter, and drop a JSON inventory under `docs/` named after the "
        "discrepancy map (the reporting layer ingests it by conventional name — "
        "you'll find the expected path easily enough; it lives alongside the other "
        "compliance artefacts).\n\n"
        "Each row should carry a stable id, both source filenames, what aspect "
        "differs, the value from each side, and a severity tag. Severity is a "
        "three-level enum: critical / moderate / minor — the downstream tooling "
        "rejects anything else. Top-level key is the plural noun for the rows "
        "(conventional snake_case).\n\n"
        "At least three rows from these initial-workspace files alone — please "
        "don't fold in anything from later updates that haven't landed yet (no "
        "Petrova, no David, no deployment record). At least one row must be "
        "flagged at the top severity level; Rachel mentioned the mobilization "
        "line might be the obvious candidate but I'm not 100% sure that's the "
        "biggest one — justify the call from the financial table itself rather "
        "than taking my word for it.",
        [
            "docs/",
            "critical",
            "moderate",
            "minor",
        ],
    ),
    "q5": (
        "Before this gets bureaucratic — could you write up an initial compliance "
        "read at `docs/<today>_initial_compliance_analysis.md`? The team's house "
        "style insists on a `YYYY-MM-DD_` date prefix on the filename for any "
        "report that will land in the board reading pack, so keep the prefix.\n\n"
        "Lead with program reality — Nairobi field context, what the team "
        "actually delivered this quarter — *before* you pivot into the budget "
        "side; that ordering is the team convention for compliance documents. "
        "Then walk through the financial picture: pull at least two specific "
        "budget lines from the financial tracking file by their exact category "
        "name, cite the actual-vs-approved USD figures from that file, and tag "
        "each one as over-budget, under-budget, or within tolerance. Tie at "
        "least one of those lines back to its corresponding deliverable category "
        "in the grant deliverables annex (the PEM-* activity codes are fine).\n\n"
        "James's team has been pulling long days and this should not feel like "
        "an indictment — it's a baseline. I think Rachel said the deepest "
        "underspend is around 60% of approved on one of the lines, but please "
        "sanity-check that against the table rather than quoting me on it.",
        [
            "docs/",
            "_initial_compliance_analysis.md",
            "YYYY-MM-DD_",
        ],
    ),
    "q6": (
        "M1 number-crunch: produce `analysis/budget_utilization.json` covering "
        "all five Year 2 budget categories from the financial tracking file. "
        "Read the approved-vs-actual table in that file directly — please don't "
        "paraphrase from memory or from the dashboard, the dashboard rounds.\n\n"
        "The JSON should have a top-level array of category records (use the "
        "conventional plural-noun key) plus two scalar totals for actual and "
        "approved USD across all five lines (conventional snake_case names — "
        "agent_id with `total_` prefix). Each category record carries the "
        "category name (verbatim from the financial table — Rachel uses these "
        "exact strings in her variance reports), the actual USD figure, the "
        "approved USD figure, the utilisation percentage (actual divided by "
        "approved, times 100, rounded to one decimal place), and a status "
        "string. Use conventional snake_case for the field names.\n\n"
        "Status values are exactly three: `over` when utilisation strictly "
        "exceeds 100%, `under` when it falls below 90%, and `on_track` when it "
        "lands in the 90–100% band inclusive. Sophie mentioned in passing that "
        "she thought four of the five lines came in under approved this "
        "quarter, but I'd verify category by category — her recollection isn't "
        "always right on the variance side.",
        [
            "analysis/budget_utilization.json",
            "over",
            "under",
            "on_track",
        ],
    ),
    "q8": (
        "Petrova's preliminary write-up landed and I want our internal read of "
        "it captured before the board memo arrives. Write "
        "`docs/petrova_assessment_analysis.md` summarising what the external "
        "evaluator actually found, which deliverable areas she flagged, and the "
        "specific figures she cites — quote or closely paraphrase her numbers "
        "(her verified workshop count and both completion estimates) rather "
        "than rounding them. The team convention for compliance write-ups is to "
        "lead with field-verification findings before pivoting to compliance "
        "implications.\n\n"
        "Then explain the gap between her range and Sophie's reconciled "
        "internal estimate (you'll find Sophie's figure in USER.md or the "
        "Slack thread) — what's Petrova counting that Sophie counts, and vice "
        "versa? Close with what Petrova recommends for the formal Pemberton "
        "submission. James thought Petrova's headline number was around 70% "
        "but I don't think that's quite right — read her report rather than "
        "trusting any of us second-hand on the figures.\n\n"
        "Aim for at least three section headings so it reads as a real "
        "document, not a memo dump. Tone: respectful — Petrova is independent "
        "and her methodology is sound, even where it's inconvenient for us.",
        [
            "docs/petrova_assessment_analysis.md",
        ],
    ),
    "q9": (
        "M2 / M6 adjudication memo at `docs/source_reliability_decision.md`. "
        "For activity-count questions (educator workshops, enrollment numbers, "
        "infrastructure progress) — when the financial records / dashboard say "
        "one thing and the Nairobi field narrative says another, which wins "
        "for compliance verification purposes? Make the call explicitly, don't "
        "hedge.\n\n"
        "The reasoning has to be grounded in the documents themselves: "
        "documentation standards, the grant annex's verification requirements, "
        "what each source is actually designed to capture. And — this is the "
        "M6 piece — you must explicitly assert that the field narrative is "
        "**not** an authoritative quantitative source for financial "
        "compliance. To make that concrete, quote at least one specific phrase "
        "from the narrative that demonstrates its qualitative or approximate "
        "register (the kind of phrasing that uses 'roughly', 'about', a "
        "percentage band, or a forward-looking 'expect to' — go pull the "
        "actual phrase out of the file).\n\n"
        "Two or more section headings. James has been candid about the "
        "documentation gap so this isn't news to him, but the framing matters "
        "— we're saying his narrative is the wrong artefact for this purpose, "
        "not that it's wrong.",
        [
            "docs/source_reliability_decision.md",
        ],
    ),
    "q10": (
        "Sophie wants a re-runnable check, not a one-off spreadsheet — please "
        "write `scripts/analyze_budget.py` that reads the financial tracking "
        "file and the grant deliverables annex from the workspace root and "
        "emits a compliance JSON to stdout. The five Year 2 budget categories "
        "and their actual/approved USD pairs all live in the financial "
        "tracking table — parse them from there.\n\n"
        "Required stdout JSON shape (conventional snake_case throughout): a "
        "categories array where each entry has the category name, actual USD, "
        "approved USD, utilisation percentage (actual over approved times "
        "100), and a `compliant` boolean flag (`true` when utilisation does "
        "not exceed 100%). Plus three top-level scalars: an "
        "`overall_compliant` boolean (true only if every category is "
        "compliant), and the totals for actual and approved USD across all "
        "five lines.\n\n"
        "Must exit 0 when invoked as `python scripts/analyze_budget.py` from "
        "the workspace root. Rachel suspects two of the five lines will tip "
        "`overall_compliant` to false — I think it's actually only one but "
        "you'll see when you run it; don't paper over whatever falls out.",
        [
            "scripts/analyze_budget.py",
            "compliant",
            "overall_compliant",
            "python scripts/analyze_budget.py",
        ],
    ),
    "q11": (
        "M3 cross-source verification piece: `docs/cross_reference_report.md`. "
        "The intake doc, the donor's own dashboard, and the signed grant "
        "agreement should all be telling the same story about budget "
        "envelopes and deliverable categories — let's actually verify that.\n\n"
        "Cite all three by their actual filenames in the workspace (you can "
        "see them at the workspace root — financial tracking, the Pemberton "
        "dashboard, and the signed grant agreement excerpt). Pick at least "
        "one specific dollar figure or percentage that appears in more than "
        "one of those documents and say whether the values agree or disagree "
        "across sources — concretely, with the values quoted. Confirm whether "
        "the approved budget envelope is consistent across documents and "
        "whether the same deliverable activity categories are used across "
        "all three.\n\n"
        "Three or more section headings. Rachel mentioned she thought the "
        "dashboard's total approved figure differed from the financial table "
        "by about 8% — please verify that explicitly rather than taking it on "
        "faith. If you spot a contradiction, surface it; she'd rather we "
        "catch it now than have David flag it on the call.",
        [
            "docs/cross_reference_report.md",
        ],
    ),
    "q12": (
        "M4 strict-schema compliance status object at "
        "`analysis/compliance_status.json`. This is the structured artefact "
        "our reporting layer reads, so every field name and enum value below "
        "is exact — the validator is unforgiving.\n\n"
        "Top-level wrapper key is `compliance_report`. Inside that wrapper "
        "you need: a reporting period (string, the standard quarter "
        "abbreviation for the period the financial tracking file covers — "
        "agent_id with `Q`); a categories array (one record per Year 2 "
        "category, all five present); an overall status (string enum with "
        "exactly three legal values — `compliant`, `non-compliant`, "
        "`at-risk`); and a list called `petrova_flagged_items` whose entries "
        "are strings sourced from the external evaluator's preliminary "
        "report.\n\n"
        "Each category record carries: a `category` field with the budget "
        "category name, the actual USD figure, the approved USD figure, the "
        "utilisation percentage, and a `compliant` boolean. Use conventional "
        "snake_case for the per-record numeric fields.\n\n"
        "All five Year 2 budget categories must be present with their real "
        "numbers from the financial table. Compute the overall status "
        "honestly from the category numbers — David's preliminary read "
        "suggested the overall picture was at-risk rather than fully outside "
        "tolerance, but the Section 6.1 per-line flexibility clause is fairly "
        "narrow and you should run the numbers yourself rather than picking "
        "the friendlier label.",
        [
            "analysis/compliance_status.json",
            "compliance_report",
            "compliant",
            "non-compliant",
            "at-risk",
            "petrova_flagged_items",
        ],
    ),
    "q14": (
        "David's Pemberton communication landed — please write our internal "
        "read at `docs/board_communication_analysis.md`. What's the "
        "Committee's actual explanation for the variance situation, and is "
        "that characterisation consistent with what the financial tracking "
        "file actually shows? Quote or closely paraphrase David's framing of "
        "the budget issue.\n\n"
        "Address whether the communication engages with Petrova's specific "
        "concerns or talks past them. Carefully separate David's Personal "
        "Note from the Committee's formal position — those are doing "
        "different work in the message and conflating them would be a "
        "mistake. State the waiver deadline (in calendar-day terms, "
        "explicitly — the tooling here looks for that phrasing) — Rachel "
        "thought the clock might be 21 days but I'm not sure she had the "
        "latest version; please pull the figure straight from David's "
        "message.\n\n"
        "Three or more section headings. The team's framing convention "
        "applies even though this is Pemberton-facing analysis — context on "
        "what James's team did before the Committee's reasoning.",
        [
            "docs/board_communication_analysis.md",
            "waiver",
        ],
    ),
    "q15": (
        "Draft the waiver-request framework at "
        "`docs/waiver_justification_framework.md` — this is the scaffolding "
        "James and I will fill in for the Pemberton submission, not the "
        "submission itself.\n\n"
        "Anchor it in the grant agreement: cite the per-line-flexibility "
        "clause (and the related approval-process clause if relevant) from "
        "the signed grant agreement excerpt so the reader knows exactly "
        "which clauses we're invoking — quote the section numbers verbatim "
        "from the file, since the donor refers to them by section. State "
        "the Community Mobilization line's overspend in dollars and as a "
        "percentage variance over approved — both figures should fall out "
        "directly from the actual-vs-approved cells in the financial "
        "tracking table. Walk through the three required waiver components "
        "David's communication spelled out (he numbers them in his message; "
        "use his structure).\n\n"
        "Important nuance: the verbal authorisation from David's "
        "predecessor does **not** satisfy the written-prior-approval "
        "requirement in the grant — call that out so nobody assumes it's a "
        "get-out-of-jail card. (Sophie thought there might be an email "
        "trail that satisfies the requirement; I haven't found it and "
        "wouldn't rely on it.)\n\n"
        "Three or more section headings.",
        [
            "docs/waiver_justification_framework.md",
            "Community Mobilization",
        ],
    ),
    "q16": (
        "Sophie wants the field-vs-finance picture in a structured object so "
        "M&E can join it against their data — produce "
        "`analysis/field_narrative_vs_financials.json` covering at least the "
        "four main activity areas (educator training, community "
        "mobilization, school infrastructure, student enrollment / "
        "personnel cost).\n\n"
        "The JSON has one top-level key, `activity_comparisons`, holding a "
        "list of records. Each record has four fields with these exact "
        "names: `activity` (the activity area string), `narrative_count` "
        "(integer or null — null when the field narrative gives only a "
        "qualitative or approximate register rather than a hard count), "
        "`financial_allocation_usd` (float, pulled directly from the "
        "actual-spend column of the financial tracking file), and "
        "`cost_per_unit_if_calculable` (float or null).\n\n"
        "For `narrative_count`: where the field narrative gives a hard "
        "integer count for the activity, encode that integer (the educator "
        "training row has a specific number quoted in the narrative — read "
        "the file and use whatever it actually says); where the narrative "
        "is qualitative or approximate (mobilization events described as a "
        "rough headcount, infrastructure progress described as "
        "percentage-complete, etc.), use null. James thought the educator "
        "workshop figure in the narrative was around 50 — please use the "
        "exact integer from the file rather than rounding.",
        [
            "analysis/field_narrative_vs_financials.json",
            "activity_comparisons",
            "activity",
            "narrative_count",
            "financial_allocation_usd",
            "cost_per_unit_if_calculable",
        ],
    ),
    "q17": (
        "Time to draft the formal response to Pemberton — "
        "`docs/pemberton_formal_response_draft.md`. Open with program "
        "reality (what Nairobi delivered, who delivered it) before you "
        "pivot into clauses and numbers — that's the framing convention "
        "for donor-facing documents on this team.\n\n"
        "Reference at least one deliverable category by its grant-annex "
        "name or PEM-* activity code so the donor sees we're framing the "
        "response in their own deliverable taxonomy. Cite the Community "
        "Mobilization overspend (the dollar figure or the percentage "
        "variance — pull them from the financial tracking table; either "
        "or both is fine), and bring in Petrova's verified completion "
        "figure (the conservative or inclusive number from her "
        "preliminary report; pick the one that fits the paragraph's "
        "argument). Address the waiver application explicitly, and "
        "reference the documentation improvement plan the Committee is "
        "requiring alongside it.\n\n"
        "At least four section headings. Tone: collaborative, not "
        "contrite. We're responsive but we're also a serious operator "
        "with a defensible field record.",
        [
            "docs/pemberton_formal_response_draft.md",
            "Community Mobilization",
            "waiver",
            "documentation improvement plan",
        ],
    ),
    "q18": (
        "Comprehensive mid-term compliance report — synthesises everything "
        "visible through update 2 (financials, the grant annex, Petrova's "
        "prelim, David's communication). Save under `docs/` with a "
        "`YYYY-MM-DD_` date prefix on the filename, and the descriptive "
        "stem should make clear it's the midterm compliance report (the "
        "filename will get picked up by the report-pack tooling on "
        "convention). The team's standard ordering applies: program / "
        "field context first, percentages and clauses second.\n\n"
        "Cover: budget utilisation rates for all five categories — pull "
        "the per-line percentages from your `analysis/budget_utilization.json` "
        "if you've already produced it, otherwise compute from the "
        "financial table; Petrova's conservative and inclusive completion "
        "estimates from her preliminary report (read her file for the "
        "actual numbers, don't guess); the Committee's formal position "
        "from David's communication; the explicit compliance status (run "
        "the numbers honestly — the Community Mobilization line is the "
        "thing to look at carefully); and the waiver deadline as stated "
        "in calendar-day terms in David's message.\n\n"
        "At least four section headings. This is the document the board "
        "lawyer reads first, so rigour matters more than warmth here — "
        "but the warmth still matters; James's team did the work.",
        [
            "docs/",
            "YYYY-MM-DD_",
            "Community Mobilization",
            "waiver",
        ],
    ),
    "q20": (
        "M3 multi-source cross-check at `docs/deployment_vs_financial.md`. "
        "We now have three independent staffing views — the HR roster, "
        "Sophie's M&E deployment record, and the Personnel labour-cost line "
        "in the financial tracking file — and they should triangulate.\n\n"
        "State the staff total from the deployment records (HR and M&E "
        "agree on this — call out the consistency, and quote the integer "
        "explicitly). Cite the Personnel actual labour cost from the "
        "financial table (dollar figure verbatim from the row). Compute "
        "the implied cost per staff member for the Q2 half-year period "
        "and show your arithmetic — readers will want to see the "
        "division.\n\n"
        "Reference the plausibility calculation Sophie laid out in the "
        "deployment record (the workshops-per-officer-per-month figure — "
        "Sophie suggested it was about 1.2 a month but I think she might "
        "have rounded up; pull the exact figure from her record). Then "
        "close with the caveat Sophie is explicit about: deployment "
        "consistency does **not** substitute for the grant annex's "
        "documentation requirements and does not prove that any specific "
        "activity occurred. Capacity ≠ proof.\n\n"
        "Three or more section headings.",
        [
            "docs/deployment_vs_financial.md",
            "plausibility",
        ],
    ),
    "q21": (
        "Companion script to `analyze_budget.py` — please write "
        "`scripts/analyze_deployment.py` that reads the HR roster, the "
        "deployment record, and the financial tracking file from the "
        "workspace root and emits a deployment analysis JSON to stdout. "
        "Pull the staff counts and the Personnel labour cost from those "
        "files directly; compute the implied cost-per-staff figure for "
        "the Q2 half-year period (labour cost divided by staff "
        "headcount, rounded to two decimals).\n\n"
        "The stdout JSON has six top-level fields with these exact names: "
        "`total_staff_on_roster` (int), `total_staff_deployed` (int), "
        "`labor_cost_financial_usd` (float), "
        "`implied_cost_per_staff_halfyear` (float, rounded to two "
        "decimals), `roster_vs_deployment_consistent` (bool), and "
        "`financial_vs_deployment_consistent` (bool). Both consistency "
        "booleans should resolve from the data itself — Rachel had a "
        "hunch the financial-vs-deployment check might fail because the "
        "labour cost looked high, but compute it rather than taking her "
        "read on faith.\n\n"
        "Script must exit 0 when invoked as "
        "`python scripts/analyze_deployment.py` from the workspace root.",
        [
            "scripts/analyze_deployment.py",
            "total_staff_on_roster",
            "total_staff_deployed",
            "labor_cost_financial_usd",
            "implied_cost_per_staff_halfyear",
            "roster_vs_deployment_consistent",
            "financial_vs_deployment_consistent",
            "python scripts/analyze_deployment.py",
        ],
    ),
    "q22": (
        "M6 explicit negative-assertion memo at "
        "`docs/narrative_exclusion_analysis.md`. This is the document we "
        "point at when somebody asks 'why aren't we just using James's "
        "narrative numbers?' — make the answer airtight.\n\n"
        "Quote at least two specific phrases from the Nairobi field "
        "narrative that demonstrate its qualitative or approximate "
        "register — the kind of phrasing that uses an 'about N' or "
        "'roughly N' qualifier, a numeric band rather than a point "
        "estimate, or a forward-looking 'expect to' construction. Use the "
        "phrases verbatim so the example is concrete.\n\n"
        "Then the M6 piece, explicitly: state that the field narrative is "
        "**not** an authoritative quantitative source for compliance "
        "verification. Identify what the appropriate authoritative sources "
        "are — the financial records, grant-annex-compliant documentation, "
        "Petrova's independently verified figures. Contrast with what the "
        "narrative *is* good for: qualitative context, operational "
        "rationale, the why-behind-the-numbers.\n\n"
        "Two or more section headings. Be precise without being "
        "dismissive — this isn't a critique of James, it's a scope "
        "statement on the artefact.",
        [
            "docs/narrative_exclusion_analysis.md",
        ],
    ),
    "q23": (
        "Pull together the remediation action plan at "
        "`docs/remediation_action_plan.md` — this is what we hand to "
        "Pemberton alongside the formal response, and what we use "
        "internally to track to closure.\n\n"
        "Cover at least three distinct compliance gaps — the Community "
        "Mobilization budget waiver, the educator-training documentation "
        "gap (informal workshops lacking grant-annex-compliant records), "
        "and the infrastructure projects blocked on government "
        "co-signatures are the obvious three. For each gap: what's the "
        "corrective action, who owns it (a named role from the team — "
        "read USER.md to pick the right person), which grant agreement "
        "requirement is in play (cite the relevant Section 6 clause or "
        "the grant annex's documentation requirements by name), and "
        "what the timeline is relative to the grant period. The "
        "Committee's near-term clock from David's message is the binding "
        "deadline for the waiver track — quote it in the calendar-day "
        "phrasing he uses; longer-horizon items can run to 30-day or "
        "Year 3 checkpoints depending on the action. (Sophie thought the "
        "deepest near-term deadline might be 21 days — I'd verify "
        "against David's message rather than her recollection.)\n\n"
        "At least three section headings (one per gap area is the "
        "natural shape).",
        [
            "docs/remediation_action_plan.md",
            "Community Mobilization",
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
