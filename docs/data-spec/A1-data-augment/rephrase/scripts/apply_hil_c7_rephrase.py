"""
Apply rephrases to hil_c7 questions.json (v3 super-harden pass).

v2 still scored ~89% ec on this task (only q3, q9 failed). v3 picks 5 of the
v2-passing exec_check questions and stacks levers H (deep schema obfuscation —
strip literal field names, force agent to guess), C++ (more hedged distractors),
and D++ (drop more grep targets). Target ec score ≤ 70% (≥5 ec failures).

Self-check: for every replaced question, asserts that all preserved tokens listed
in PRESERVE remain literally present (paths, filename patterns, grep-target
literals that are unconventional or unguessable).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_c7/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_c7/questions.json"

# Each entry: id -> (new_question_text, [tokens that MUST appear literally in new text])
REPHRASES: dict[str, tuple[str, list[str]]] = {
    "q3": (
        "ok — let me lock in our snapshot before another update lands. Could you "
        "stitch a preliminary impact doc together at `docs/breach_impact_prelim.json` "
        "off the initial workspace (the endpoint register, the customer-data "
        "inventory, Jake's technical brief, and the response checklist — no log "
        "data yet, that's still pending from Diego)?\n\n"
        "Conventional snake_case fields, the legal-intake tool is fussy: an "
        "endpoints list, a list of the customer-data fields at risk, Jake's CVSS "
        "number, his preliminary headcount estimate, and the current completion "
        "ratio of the response checklist. Field naming should be obvious from the "
        "semantics — match the convention any reviewer would expect.\n\n"
        "Pull every value from the workspace docs. The data-types list should "
        "reflect the inventory's exposure column (the fields it explicitly says "
        "are exposed in pipeline-config records, not the ones it carves out as "
        "safe). For the checklist ratio just count box-checked vs total — Maya "
        "thinks it's already around 30% complete from her quick skim, but I "
        "wouldn't trust that without re-counting yourself.",
        [
            "docs/breach_impact_prelim.json",
        ],
    ),
    "q5": (
        "I need a clean incident timeline for the W1 status note — please drop "
        "it as a JSON file in `docs/` with a `YYYY-MM-DD_` prefix in the "
        "filename. Initial workspace only; no peeking at sessions or update "
        "bundles.\n\n"
        "At least five entries, each with a date plus a short description. Use "
        "machine-readable date strings (full datetime where the source gives you "
        "one, otherwise a plain YYYY-MM-DD). Anchor events worth folding in: "
        "when the researcher's disclosure came in, when the endpoint went down, "
        "when Jake's brief was authored, when the customer-notification draft "
        "was put together, and the relevant deploy date called out in the "
        "endpoint register. I think Jordan said the disclosure landed late "
        "November — maybe the 24th or 25th, but double-check the source.\n\n"
        "Visual-thinker mode: keep entries one-per-line, dates first, no prose "
        "essays.",
        [
            "docs/",
            "YYYY-MM-DD_",
        ],
    ),
    "q6": (
        "Sana and Jake are giving us wildly different scope numbers and Jordan "
        "wants the contradiction written down somewhere we can point to. Put a "
        "comparison together at `docs/scope_conflict_analysis.md`.\n\n"
        "Three sources to reconcile:\n"
        "1. `api_endpoint_register.md` + `customer_data_inventory.md` together "
        "give us the population ceiling — the inventory has the hard upper-bound "
        "number for active pipeline configs across all customers.\n"
        "2. `vulnerability_technical_brief.md` carries Jake's preliminary "
        "estimate — a back-of-envelope from request count × an assumed records-"
        "per-response multiplier. (Maya remembered it as roughly 8K but I "
        "honestly think she's confusing it with a different incident — pull the "
        "actual number off the brief.)\n"
        "3. `developer_docs_screenshot.md` shows the `?list=true` parameter is "
        "publicly documented — which kills the 'UUIDs aren't enumerable' line "
        "of argument anyone might lean on.\n\n"
        "Call out the conflicts numerically (cite the actual figures from the "
        "inventory and the brief — Jake's prelim materially exceeds the "
        "inventory ceiling, that's the headline conflict). Three or more `##` "
        "sections, please — Alex-flavour structured-table preference, not a wall "
        "of prose.",
        [
            "docs/scope_conflict_analysis.md",
            "api_endpoint_register.md",
            "customer_data_inventory.md",
            "vulnerability_technical_brief.md",
            "developer_docs_screenshot.md",
        ],
    ),
    "q8": (
        "Diego's log writeup just landed in the workspace — `access_log_analysis.md`. "
        "Please summarise the forensic findings into "
        "`docs/access_log_analysis_summary.md` so Jordan and Raj have a "
        "single-page version that doesn't make them slog through the full "
        "analysis.\n\n"
        "Pull the headline numbers and timestamps straight from the log doc — "
        "don't paraphrase, these get cited downstream:\n"
        "- the exact first-external-access timestamp Diego flagged (date and "
        "UTC time)\n"
        "- the count of individual record fetches he tallied\n"
        "- the unique-UUID coverage figure\n"
        "- the list-call cadence pattern\n"
        "- which endpoint(s) got hit (use the route name as it appears in the "
        "source — Raj kept calling it the 'config-pipeline endpoint' yesterday "
        "but the actual route name in Diego's doc is the canonical one, use "
        "that)\n"
        "- the IP-range / attacker-profile one-liner\n\n"
        "Cite `access_log_analysis.md` by filename — this is going outbound "
        "eventually so source attribution matters.",
        [
            "docs/access_log_analysis_summary.md",
            "access_log_analysis.md",
        ],
    ),
    "q9": (
        "We've got three scope estimates floating around and I need a written "
        "adjudication so we stop re-litigating this in every standup. Put it "
        "at `docs/scope_decision.md`.\n\n"
        "Compare:\n"
        "- Jake's revised number (after he saw `access_log_analysis.md`)\n"
        "- Sana's earlier under-500 reading (which leaned on UUIDs not being "
        "enumerable — a premise the `?list=true` traffic pattern blows up)\n"
        "- the customer-inventory ceiling we already had on file\n\n"
        "Be explicit about which source you're treating as most credible and "
        "why — the raw-log analysis is the one with primary-evidence weight. "
        "Spell out why the other two estimates carry less weight (Jake's initial "
        "multiplier was wrong; Sana's enumerability assumption is now refuted).\n\n"
        "Important: don't treat `disclosure_report_initial.md` as the definitive "
        "scope source. That report's 'TBD'-ish description was written before "
        "the logs came in; it's context, not ground truth. Sana mentioned in "
        "passing she thought the final figure might land closer to 1,800 once "
        "duplicates were stripped, but I'd ground the conclusion in the log "
        "analysis itself rather than her hallway estimate.",
        [
            "docs/scope_decision.md",
            "access_log_analysis.md",
        ],
    ),
    "q10": (
        "pls add a small analysis script at `scripts/analyze_scope.py` that we "
        "can re-run any time the inventory or endpoint register changes. It "
        "should read `api_endpoint_register.md` and `customer_data_inventory.md` "
        "from the workspace root (both are markdown with tables), and emit JSON "
        "to stdout.\n\n"
        "Fields the validator expects, by semantic role:\n"
        "- a count of distinct endpoint routes registered\n"
        "- a list of routes that lack authentication\n"
        "- a list of customer-data field names the inventory marks as exposed "
        "in pipeline-config objects (at least four; read the inventory's "
        "exposure column)\n"
        "- the total active pipeline-config count from the inventory (an int)\n"
        "- a sensitivity classification\n\n"
        "Use conventional snake_case names for all keys — pick whatever a "
        "reasonable reviewer would name each field. The sensitivity value must "
        "come from the allowed set `critical | high | medium | low`; given API "
        "keys are in scope, `high` is the obvious pick.\n\n"
        "Has to run as `python scripts/analyze_scope.py` from the workspace "
        "root and exit 0. Priya's QA tooling will smoke-test it before we "
        "merge.",
        [
            "scripts/analyze_scope.py",
            "api_endpoint_register.md",
            "customer_data_inventory.md",
            "critical",
            "high",
            "medium",
            "low",
        ],
    ),
    "q11": (
        "Cross-file consistency pass — Sana asked for one explicitly. Write it "
        "at `docs/scope_consistency_report.md`.\n\n"
        "Walk the three foundational docs against each other and call out "
        "where they don't square up:\n"
        "- `api_endpoint_register.md` (which routes exist + their auth state)\n"
        "- `customer_data_inventory.md` (the total-configs ceiling and what "
        "data lives in each record)\n"
        "- `disclosure_report_initial.md` (the early 'scope TBD' read)\n\n"
        "Cite all three by filename — the report will be reviewed and the "
        "reviewer will grep for those names. Surface at least one specific, "
        "numerically-grounded inconsistency by pulling the actual figures from "
        "the inventory and the technical brief and contrasting them; the "
        "disclosure report's vague placeholder also stands in stark contrast "
        "to the firm number documented in inventory. (Leo offhand said he "
        "thought the inventory and the brief lined up at around 2,400 — pretty "
        "sure he's wrong on at least one of those, verify both.)",
        [
            "docs/scope_consistency_report.md",
            "api_endpoint_register.md",
            "customer_data_inventory.md",
            "disclosure_report_initial.md",
        ],
    ),
    "q12": (
        "Housekeeping — the response checklist in the workspace is currently "
        "all unchecked-template (every item still `- [ ]`), and I want a short "
        "audit at `docs/checklist_audit_report.md` that walks where we actually "
        "stand item-by-item.\n\n"
        "Read `incident_response_checklist.md` and tag each major item with a "
        "status (complete / in progress / pending / overdue) based on what's "
        "actually happened so far in the response. Reference at least two "
        "specific items by their text so it's clear we read the file rather "
        "than freestyling. I think Raj said roughly half the items were "
        "informally done — but the file itself is your source of truth, his "
        "estimate is just hallway colour.\n\n"
        "Also flag the most critical still-open item given current evidence — "
        "Jordan will ask 'what's the one thing we should be doing right now' "
        "and I want a direct answer ready.",
        [
            "docs/checklist_audit_report.md",
            "incident_response_checklist.md",
        ],
    ),
    "q14": (
        "Leo finally surfaced `deployment_timeline.md` — the production history "
        "we should have had on day one. Please trace the vulnerability "
        "introduction in `docs/vulnerability_introduction_trace.md`.\n\n"
        "Anchor on the specifics from the timeline file:\n"
        "- the merge-commit / PR identifier that introduced the vulnerable "
        "endpoint (cite the PR number from the timeline doc verbatim)\n"
        "- the production deploy date that flipped the endpoint live (date + "
        "UTC timestamp)\n"
        "- how long the vuln was up in prod before any external traffic hit "
        "it (cross with Diego's log data)\n"
        "- total time-in-the-wild before the endpoint was disabled\n\n"
        "Cite `deployment_timeline.md` by name. Three or more `##` sections — "
        "this lands in the post-mortem packet. (Sana mentioned in standup she "
        "remembered the introducing PR as around mid-October but kept saying "
        "'I think it was the 16th or so' — the timeline file has the exact "
        "date, use that.)",
        [
            "docs/vulnerability_introduction_trace.md",
            "deployment_timeline.md",
        ],
    ),
    "q15": (
        "Need the 72-hour compliance arithmetic captured in JSON form so the "
        "outside counsel can see we've actually done the math. Save at "
        "`analysis/compliance_timing.json`.\n\n"
        "The document should hold the standard compliance-timing facts in a "
        "flat object — pick conventional snake_case names that any reviewer "
        "would expect for each value:\n\n"
        "- the ISO 8601 datetime when the vulnerability was first exploited "
        "(from the forensic log writeup)\n"
        "- the ISO 8601 datetime the vulnerable endpoint was taken offline "
        "(the W1 disclosure record has it; watch the EST→UTC conversion)\n"
        "- the elapsed exposure window expressed as float hours between those "
        "two anchors (no day-rounding)\n"
        "- the regulator's notification deadline (anchor + 72h, ISO 8601)\n"
        "- a placeholder for when the final customer notification went out — "
        "the final-notification artefact isn't in the workspace yet, so just "
        "park a TBD-style sentinel string here\n"
        "- a tri-state compliance verdict (leave it null for now; insufficient "
        "data to commit)\n\n"
        "Honest placeholders beat guessed values. Both anchor timestamps come "
        "straight from the workspace. Outside counsel's intake form is fairly "
        "tolerant on naming — Sana said in passing that as long as the values "
        "are right the reviewers will figure out the keys, and Maya thought "
        "the regulator-window field might want to be named after the 72-hour "
        "rule itself but I don't think she'd actually checked. Use whatever "
        "naming feels most natural; consistency within the document matters "
        "more than matching any external schema.",
        [
            "analysis/compliance_timing.json",
        ],
    ),
    "q16": (
        "Companion script for the JSON we just produced — pls add "
        "`scripts/analyze_timeline.py`. It should read the deduped log writeup "
        "and the deployment-history doc from the workspace root and dump a "
        "single flat JSON object to stdout.\n\n"
        "Fields the downstream tooling expects, by semantic role (use "
        "conventional snake_case names a reviewer would predict):\n"
        "- the moment of the first external list-call (ISO 8601)\n"
        "- the moment the introducing PR went into production (ISO 8601, "
        "watch the EST→UTC conversion if the source uses local time)\n"
        "- the moment the vulnerable endpoint was disabled (ISO 8601)\n"
        "- the float-hours window between first exploit and fix-deploy\n"
        "- the regulator's notification window length expressed in hours "
        "(literally the integer the EU 72-hour rule names)\n"
        "- the regulator's deadline timestamp (first-exploit + that window)\n\n"
        "All three datetime values come from the workspace source docs — don't "
        "hardcode strings, derive them. Must run as "
        "`python scripts/analyze_timeline.py` from workspace root and exit 0. "
        "Leo said the post-mortem CI doesn't pin specific key names — values "
        "and types are what matter — but Priya wasn't sure he was right about "
        "that, so just go with whatever naming the rest of the script files "
        "in `scripts/` already use as a stylistic baseline.",
        [
            "scripts/analyze_timeline.py",
        ],
    ),
    "q17": (
        "Now that we know the actual timeline and scope, the customer-"
        "notification draft in the workspace root is *very* clearly inadequate. "
        "Please do a side-by-side at `docs/notification_comparison.md` between "
        "`notification_draft_v1.md` and what a compliant final notification "
        "needs to contain.\n\n"
        "Identify at least two specific gaps. The draft is silent on the actual "
        "exposure window, doesn't surface the confirmed scope, and the framing "
        "is soft in ways that won't fly under the EU breach-notification "
        "regime — 'security configuration issue', 'precautionary' rotation, "
        "that whole register. Jake floated that the draft was 'mostly fine, "
        "just needed a date added' but he hadn't actually re-read it post-log-"
        "analysis; treat that as out-of-date.\n\n"
        "End with what specifically needs adding for the final to be compliant. "
        "Jordan and the legal team will be the readers, not engineers.",
        [
            "docs/notification_comparison.md",
            "notification_draft_v1.md",
        ],
    ),
    "q18": (
        "Mid-incident report time — Jordan wants a single document he can hand "
        "to the board ahead of the W2 sync. Save it under `docs/` with a "
        "`YYYY-MM-DD_` date prefix; the filename should obviously read as a "
        "midterm breach report.\n\n"
        "Cover, with citations to source docs for every figure:\n"
        "- the CVSS score from the technical brief\n"
        "- confirmed scope from the log work, plus the affected-customer count "
        "from the inventory file\n"
        "- exposure window calculated from first-exploit to endpoint-disabled "
        "(state both endpoints + the duration in hours)\n"
        "- the regulatory notification deadline computed from first-exploit "
        "(EU 72-hour breach-notification window framing)\n"
        "- current status: notification not yet sent, awaiting the final "
        "approval cycle\n\n"
        "Four or more `##` sections, structured-table layout where the data "
        "lends itself. Maya pinged saying she'd seen the customer count cited "
        "as ~1,200 somewhere — pretty sure that was a different report, "
        "verify against the inventory file directly.",
        [
            "docs/",
            "YYYY-MM-DD_",
        ],
    ),
    "q20": (
        "The final notification has landed (`notification_final.md`) so we can "
        "close the 72-hour compliance loop. Save the calculation at "
        "`analysis/72h_compliance_final.json`.\n\n"
        "Field shape (validator pins these names):\n"
        "- `vulnerability_first_exploited_ts` — same anchor as the earlier "
        "compliance file\n"
        "- `notification_sent_ts` — the date pulled from notification_final.md\n"
        "- `hours_elapsed` — float, first_exploited to notification_sent\n"
        "- `72h_limit` — the float `72.0`\n"
        "- `compliant` — bool, your call (see below)\n"
        "- `hours_margin` — float, positive = under limit, negative = over\n\n"
        "Quick note before you set `compliant`: outside counsel's sign-off in "
        "the final notification doc says the overall approach satisfies the "
        "regulator. The pure-arithmetic answer (first-exploit → customer "
        "notification) is a different story — those are well past 72 hours "
        "apart. Pick one reading (legal-trust or math-strict) and make sure "
        "`hours_margin`'s sign is consistent with `compliant`. Either choice "
        "is defensible; the validator accepts both as long as the bool/margin "
        "pair is internally coherent.",
        [
            "analysis/72h_compliance_final.json",
            "vulnerability_first_exploited_ts",
            "notification_sent_ts",
            "hours_elapsed",
            "72h_limit",
            "compliant",
            "hours_margin",
        ],
    ),
    "q21": (
        "End-to-end summary script: `scripts/generate_breach_summary.py`. "
        "Reads the three update artefacts (the dedup-log doc, the deploy-"
        "history doc, the final customer notification) from the workspace "
        "root and emits one JSON document to stdout.\n\n"
        "The downstream consumer wants a single semantic wrapper at the top "
        "level (a sensibly-named object grouping all the breach-summary "
        "facts) — pick whatever wrapper key reads naturally for an outbound "
        "breach-summary blob. Inside, surface the standard headline numbers "
        "with conventional snake_case keys a reviewer would predict:\n"
        "- the first-exploit ISO 8601 datetime\n"
        "- the date the endpoint was disabled\n"
        "- the date the final customer notification went out\n"
        "- a float-hours exposure window (exploit → fix)\n"
        "- a float-hours notification latency (exploit → notification)\n"
        "- a 72-hour compliance verdict as a bool\n"
        "- a count of vulnerable endpoints (it's 1)\n"
        "- the CVSS score from the technical brief as a float\n\n"
        "Derive every value from the source docs rather than hardcoding "
        "strings. Exit 0. We'll wire this into the post-mortem CI step. "
        "Sana mentioned the CI step is loose on key names as long as the "
        "shape's right — though Priya thought maybe one or two field names "
        "were pinned, she couldn't remember which. Just stay consistent with "
        "the naming you used in `scripts/analyze_timeline.py` so the two "
        "scripts feel like a coherent set.",
        [
            "scripts/generate_breach_summary.py",
        ],
    ),
    "q22": (
        "Root-cause writeup at `docs/root_cause_analysis.md`. This is the "
        "engineering-facing artefact (Sana, Leo, Priya), so it can be technical "
        "but it does need to be tight.\n\n"
        "Must cover:\n"
        "- the CVSS score from the technical brief\n"
        "- the specific endpoint at fault (the GET `pipeline-configs` route — "
        "use the full path including the `{uuid}` segment as registered)\n"
        "- the introduction event: the introducing PR + its production deploy "
        "date (both pulled from the deployment-history file — Leo offhand "
        "called it 'the late-summer deploy' but the timeline file makes the "
        "actual date unambiguous, use that)\n"
        "- root cause as the *combination* of two failures landing in the same "
        "PR — the missing **@require_auth** decorator on the GET method, plus "
        "the publicly-documented `?list=true` enumeration knob that turns the "
        "first failure from theoretical-nuisance into total-population-"
        "exposure\n"
        "- why neither failure was caught: no security-review gate on the PR, "
        "no CI check verifying auth decorators on customer-data routes\n"
        "- contributing factors as called out in the deployment-history file\n\n"
        "Three or more `##` sections.",
        [
            "docs/root_cause_analysis.md",
            "pipeline-configs",
            "@require_auth",
        ],
    ),
    "q23": (
        "Definitive impact-assessment JSON at `analysis/breach_impact_final.json` "
        "(strict-ish schema — types enforced, classifier values drawn from a "
        "small fixed vocabulary). The document needs to surface, in a flat "
        "object with conventional snake_case naming a reviewer would expect:\n\n"
        "- the CVSS number from the technical brief (float)\n"
        "- the impacted route(s) as a list of strings (must include the GET "
        "pipeline-configs `{uuid}` route)\n"
        "- a bool for whether the customer notification cleared the regulator's "
        "window (per outside counsel's sign-off in the final notification doc)\n"
        "- the exposure window as float hours (first-exploit → endpoint-"
        "disabled)\n"
        "- the confirmed total of impacted records as an int (pull from the "
        "forensic log writeup, NOT the early TBD-flavoured disclosure report; "
        "Maya remembered the figure as roughly 1,800 after dedup, but Leo "
        "thought it was closer to 3,200 from a different cut — both are off, "
        "ground it in the log doc itself)\n"
        "- a data-sensitivity classifier drawn from the standard four-tier "
        "severity vocabulary (critical / high / medium / low)\n"
        "- a regulatory-risk classifier drawn from the standard three-tier "
        "risk vocabulary (high / medium / low)\n\n"
        "All numbers ground-truth, no rounding tricks. This file is the one "
        "outside counsel will reference, so accuracy beats elegance. Maya also "
        "thought exposure landed near 600 hours; that's a rough overshoot, "
        "compute it yourself off the actual timestamps.",
        [
            "analysis/breach_impact_final.json",
            "critical",
            "high",
            "medium",
            "low",
        ],
    ),
    "q24": (
        "For the post-mortem packet, please put together "
        "`docs/stakeholder_action_timeline.md` — who did what, when. Pull the "
        "named stakeholders from `USER.md` (the core breach-response group "
        "around Alex; at least three of the technical/exec folks should appear "
        "by name).\n\n"
        "Each action gets a date or timestamp. Anchor events that have to be "
        "in there:\n"
        "- the researcher disclosure and the same-day endpoint containment\n"
        "- the final customer notification send\n"
        "- the log-analysis commission, the API-key rotation, and the "
        "disclosure-strategy decision points along the way\n\n"
        "Stay grounded in actual session/workspace content — no inventing "
        "events or timestamps. Jordan is the primary reader; he'll cross-"
        "check against his own DM history. Leo half-remembered the disclosure "
        "as November 24th but I'm pretty sure he's off by a couple of days — "
        "verify against the disclosure report and log files.",
        [
            "docs/stakeholder_action_timeline.md",
            "USER.md",
        ],
    ),
    "q26": (
        "Remediation plan (semi-strict schema) at `docs/remediation_plan.json`. "
        "Sana and Leo will own most of these but ownership stays per-action.\n\n"
        "Top-level structure: a list of remediation actions plus a positive "
        "integer giving the estimated completion horizon for the whole plan in "
        "days. Pick conventional snake_case names a reviewer would expect for "
        "both the list wrapper and the days-estimate field.\n\n"
        "Each entry in the actions list is an object describing one action. "
        "The fields it needs (use predictable snake_case names — match the "
        "convention any reasonable reviewer would name these):\n"
        "- a stable per-action identifier\n"
        "- a human-readable description of what the action is\n"
        "- the owning person or team\n"
        "- a target completion date\n"
        "- the acceptance criteria that decide when it's done\n\n"
        "Five actions minimum, every field a non-empty string. Make sure the "
        "obvious must-haves are covered: a security-review gate for any PR "
        "touching customer-data API endpoints, automated CI verification that "
        "auth decorators are actually present, an audit sweep of every other "
        "endpoint for the same class of gap, tighter rate-limiting on "
        "enumeration-prone params, and an access-log preservation policy so "
        "we never have to scramble for raw evidence again. (Priya thinks "
        "three actions might be enough but the downstream tooling is hard-set "
        "on five minimum, so don't trim. Leo mentioned in passing the schema "
        "has historically been loose on key naming — values matter more than "
        "names — so just use whatever reads most naturally.)",
        [
            "docs/remediation_plan.json",
        ],
    ),
    "q27": (
        "Final breach report — the comprehensive one Jordan signs off on and "
        "ships out internally. Save under `docs/` with a `YYYY-MM-DD_` prefix "
        "(use the notification send date or today's, either is fine; the "
        "filename should obviously read as a final breach report).\n\n"
        "All of these have to land in the document, with source citations on "
        "every figure (lift each value from the relevant workspace doc, "
        "don't guess):\n"
        "- the CVSS score from the technical brief\n"
        "- the confirmed total-affected-records number\n"
        "- the calculated exposure window in hours (compute it off the actual "
        "first-exploit and endpoint-disabled timestamps)\n"
        "- the notification-compliance result (per outside counsel's sign-off "
        "in the final notification doc)\n"
        "- the affected endpoint by route name (the GET `pipeline-configs` "
        "route)\n"
        "- the three anchor timestamps: first exploit, endpoint disabled, "
        "notification sent — all surfaced explicitly with their dates\n\n"
        "Five or more `##` sections — the structured-format preference is "
        "non-negotiable on the final doc. Stick to whatever conventions the "
        "team uses for ISO dates, date-prefix filenames, structured headings, "
        "source-filename citations, and ground-truth numbers throughout.",
        [
            "docs/",
            "YYYY-MM-DD_",
            "pipeline-configs",
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
