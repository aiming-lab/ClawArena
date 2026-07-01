# Rephrase Agent Prompt — TEMPLATE

You are rephrasing exec_check test questions for one ClawArena benchmark task. Read this entire briefing before acting.

## Goal

Rewrite `question` text of every `type: "exec_check"` round in the target task's `questions.json` to:

1. **Sound human, not like a machine command.** Adopt voices of the human team members described in `USER.md` (PM/eng/analyst/etc.). Slack/Discord/Telegram register varies — casual one place, more formal another. Match the implied stakes.
2. **Increase difficulty** by stripping leaked answer values from the question. Force the agent to read workspace files to recover them.
3. **Preserve three-way alignment**: question ↔ workspace ↔ eval. Whatever the eval script checks must remain producible by an agent that reads only the workspace + your rephrased question.

You do **NOT** rephrase `multi_choice` rounds. They stay byte-identical.

## Inputs

- **Task ID**: `{TASK_ID}`
- **Original questions**: `<REPO_ROOT>/data/clawarena/eval/{TASK_ID}/questions.json`
- **Eval scripts** (what the checks actually do): `<REPO_ROOT>/data/clawarena/eval/{TASK_ID}/scripts/`
- **Initial workspace** (round 0): `<REPO_ROOT>/data/clawarena/nanobot/workspaces/{TASK_ID}/`
- **Update bundles** (added at later rounds): `<REPO_ROOT>/data/clawarena/nanobot/updates/{TASK_ID}/upd<N>_{sessions,workspace}/`. Each round in questions.json has an `update_ids` list — empty means same visibility as the previous round; entries like `["upd1_sessions","upd1_workspace"]` mean those bundles become visible at this round and remain visible thereafter.
- **USER.md** (personas, comms preferences): in the workspace root.

## Pilot reference (gold sample)

A pilot was completed for `hil_s1`. Read these to understand the quality bar:

- `<REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/alignment/hil_s1.md` — alignment table format
- `<REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/scripts/apply_hil_s1_rephrase.py` — rephrase + self-check script
- `<REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/diff/hil_s1.md` — original-vs-rephrased side-by-side

Mimic this workflow. Your apply script's `REPHRASES` dict maps `qid → (new_text, [preserved_tokens])`. Your self-check asserts every preserved token literally appears in the new text.

## Hard constraints (eval-driven preservation)

These MUST appear verbatim in your rephrased question text whenever the original required them:

1. **Output paths** (e.g., `project/docs/foo.json`, `data/processed/bar.csv`) — eval scripts `test -f` them.
2. **JSON schema field names** (`cvss_score`, `affected_endpoints`, `update`, `action_items`, `due`, etc.) — eval scripts index by key.
3. **Enum values** in schema (`not_started|in_progress|blocked|...`) — eval validates membership.
4. **Filename patterns** (e.g., `YYYY-MM-DD_*_v<N>.md`, `*_progress_update_v1.md`) — eval globs by pattern.
5. **Literal grep targets** in eval (read each `eval.command` carefully — anything inside `grep -q "..."` or `grep -qE "..."` MUST appear in the agent's output, which means your question must direct the agent to produce it). When the literal is short and easy to miss (e.g., `Project Status`, a specific date like `2025-03-12`, a number with thousands separator like `39,426`), **keep it explicit in the question** even if you'd rather strip it. The pilot's `q14`, `q16`, `q22` show this pattern.
6. **Style-rule labels** (`P1`, `P2`, `P3`, `P4`, `P5`) when eval checks them.

## What you CAN and SHOULD strip

Anything that is **findable in the visible workspace files** at the round when the question fires:

- Hardcoded values (CVSS scores, record counts, dates, percentages) when they appear in source documents.
- Source-file names (replace with semantic indirect references like "the changelog Maya dropped", "the forensic write-up", "the latest deduplicated raw file") **after the first time the file appears** — for the round where the file first becomes visible, you may keep its name to ease discovery.
- Bullet-list enumerations of "must include" items when the structure is implied by style guide rules already cited.
- Pre-computed derivations (e.g., "exposure_window_hours = 518") when the agent can compute them from inputs that are in the workspace.

## What you must NOT do

- **Do not lie** in distractors. You may inject tangential / soft / misleading-sounding sentences (`"Diego's still digging through logs btw"`, `"Casey wants this before her 4pm"`) but **never** state a fact that contradicts what the eval expects. Distractors must be neutral or true-but-irrelevant.
- **Do not rephrase multi_choice questions.** Skip them; their `question` field stays byte-identical.
- **Do not modify** any field other than the `question` text of `type: "exec_check"` rounds.

## Source-file naming arc (progressive reveal)

A task spans round 0 → upd1 → upd2 → upd3 → upd4. The agent gets more workspace-familiar over time. So:

- **Early rounds**: you may name source files (`USER.md`, `data_dictionary.md`, `meeting_notes.md`) directly to seed orientation.
- **After a file's introduction round**: prefer indirect references ("Diego's log analysis", "the v2 changelog Maya pushed", "the contamination notes").

## Tone / register / persona

Read `USER.md` first. Identify the team members, their channels (Slack, Discord, Feishu, Telegram), expertise, and communication patterns. Then for each rephrased question, mentally cast which team member would most naturally make this ask, and adopt their voice.

Vary register across questions:
- **Slack speed-ask** for early scoping ("hey — can you pin down ...")
- **Spec-style** for formal artifacts going to stakeholders / legal
- **Engineering Discord** for code/test asks ("pls add ...", "heads up: ...")
- **PM Telegram** for status/comm artifacts ("need a stakeholder-facing update — ...")
- **Voice can be informal, slightly ungrammatical, with em-dashes / parenthetical asides / soft hedges** ("idk if this is overkill but ...", "totally my fault, btw").

## Distractor density

Every rephrased question gets **≥ 1 sentence of tangential context** (a stakeholder mention, scheduling pressure, side concern). Simple/short questions can take 2-3.

## Workflow

1. **Read** `questions.json` for `{TASK_ID}` end-to-end. Read `USER.md`. Skim the eval scripts referenced by exec_check rounds.
2. **Inventory** the workspace + each upd bundle (use Bash `find` or Glob). Note which files appear at which round.
3. **Build alignment table**: for every exec_check round, identify
   (a) what the eval command checks (literals, schema, grep targets);
   (b) which values the original question leaks;
   (c) where each leaked value is recoverable in the workspace files visible at that round (run grep to confirm);
   (d) your strip-decision (STRIP / KEEP-LITERAL / DERIVE-WITH-POINTER).
   Save as `data-augment/rephrase/alignment/{TASK_ID}.md`. Keep it concise, table-style.
4. **Write the apply script** `data-augment/rephrase/scripts/apply_{TASK_ID}_rephrase.py`. Use the pilot script as a template — copy its structure (REPHRASES dict, self-check loop). Each entry: `qid → (new_question_text, [preserved_tokens])`. Preserved-tokens list MUST cover every literal that the eval command's grep / schema / path checks. Run the script. It must report `OK: rephrased N exec_check rounds`.
5. **Emit diff** `data-augment/rephrase/diff/{TASK_ID}.md`. Side-by-side ORIGINAL vs REPHRASED for every exec_check round. (Reuse pilot's `emit_hil_s1_diff.py` style, parameterized.)
6. **Output written to** `data-augment/rephrase/rephrased/{TASK_ID}/questions.json` (the apply script writes there).

## Output report (back to me)

After writing all artifacts, return a concise report (≤ 400 words):

- Number of exec_check rounds rephrased
- Tone choices made (which persona for which questions, briefly)
- Any STRIP decisions you were uncertain about (and why) — list ≤ 5
- Any literal grep targets you had to KEEP-LITERAL despite preferring to strip — list with question id
- Any rounds you flagged as RISK (solvable but fragile)

Do not paste the rephrased text back. The artifacts on disk are the deliverable.

## Self-check requirement

Your apply script must include the same self-check the pilot has: every entry in the REPHRASES dict carries a `preserved_tokens` list, and the script asserts every token literally appears in the new text. If any token is missing, the script exits 1 and you fix it before reporting back. Do not mark the task complete until the script exits 0.

If you find a question whose constraints are impossible to satisfy without a value the workspace doesn't contain, flag it in your report and leave the original `question` unchanged for that round (do not include it in REPHRASES).
