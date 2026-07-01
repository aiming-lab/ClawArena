# v3 Super-Harden Agent Prompt — TEMPLATE

You are doing a **third pass** of hardening on exec_check questions for one ClawArena task. v2 dropped scores but not enough — we need ~3-5 MORE ec fails on this task to push overall benchmark average below 70%.

## Inputs

- **Task ID**: `{TASK_ID}`
- **v2 rephrased questions** (your starting point): `<REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/rephrased/{TASK_ID}/questions.json`
- **v2 apply script**: `<REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/scripts/apply_{TASK_ID}_rephrase.py`
- **v2 alignment + diff**: `<REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/{alignment,diff}/{TASK_ID}.md`
- **Eval scripts**: `<REPO_ROOT>/data/clawarena/eval/{TASK_ID}/scripts/`
- **Workspace + updates**: `<REPO_ROOT>/data/clawarena/nanobot/{workspaces,updates}/{TASK_ID}/`
- **v2 fail map**: which questions agent already failed in v2 — those are NOT your target. Look for **questions agent PASSED in v2** and harden those further.
- **v2 fail map command**:
  ```
  python3 <REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/scripts/extract_per_q_pass.py <REPO_ROOT>/results/codex_gpt-5.4_openclaw_rephrase_v2/openclaw/infer
  ```
  Pipe into `grep -A2 {TASK_ID}` to filter.

## Goal

Identify the exec_check questions where the v2 agent PASSED. For each, push it harder. Target: 3-5 more failures than v2 produced for this task.

## Strategy: aggressive lever-stacking

For each "passed in v2" exec_check question, apply MULTIPLE additional levers simultaneously:

### Lever D++ (drop literal grep targets even more)

v2 may have kept some grep targets verbatim "for safety". v3: strip them all unless the eval depends on **structural** content (output path, schema field name) rather than data values.

For every `eval.command`, identify:
- **Output values agent must write**: numbers, dates, names, phrases. These should appear in the **agent's output**, not the question.
- If the value is in workspace → strip from question, agent must read.
- If the value is computable → strip, agent must compute.
- If the value is conventional → maybe agent guesses right; strip and accept variance.

### Lever C++ (multiple misleading distractors per question)

v2 had ≥2 misleading sentences per ~half questions. v3: **2-3 misleading sentences per question** for the still-passing ones. Stack them.

Examples of compounding misdirection:
- "Maya thinks the threshold is 45 days" + "Sam later corrected to maybe 60" + "actually I think Alex confirmed 28 in the doc"
- Every false-but-hedged hint forces agent to verify against workspace; some will slip.

### Lever F (new): mask filename hints

For files with conventional / discoverable names, replace direct mentions:
- `data_dictionary.md` → "the schema doc"
- `pip-email-chain.md` → "the email thread"
- `style_guide.md` → "the team's writing rules"

Agent must `ls` workspace and locate. Multi-file confusion possible.

### Lever G (new): dilute structural enumeration

If a question lists "must include: A, B, C, D, E", reduce to a paragraph that mentions some items but not all:
- "A meaningful summary covers what happened, who knew when, and what we did about it" instead of an explicit bullet list of timestamps, owners, decisions.

The eval will still check for specific items, but the agent's output may genuinely miss one.

### Lever H (new): deeper schema obfuscation

Where v2 kept full JSON schema as code block, v3: convert to single sentence, e.g.:
- v2: ```json {"action_id": "...", "description": "...", "owner": "...", "status": "...", "due": "..."} ```
- v3: "JSON document with the action's identifier, what to do, who owns it, current state from the standard pipeline-state vocabulary, and a target date."

Agent guesses. Eval validates strict schema. Some will fail on wrong keys (e.g., `action_id` vs `id`, `status` vs `state`, `due` vs `due_date`).

**Caveat**: only apply lever H if eval calls `check_schema.py` (which validates against a stored schema). If eval validates with `json.load + assert keys`, the assertion typically uses the exact key — same effect.

**Hard preservation** (still required):
- Output paths verbatim (eval `test -f`)
- Filename pattern templates (eval globs)
- Truly unconventional field names (e.g., `staff_nurses_understated_count`) — keep these verbatim

## Workflow

1. Run `python3 <REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/scripts/extract_per_q_pass.py <REPO_ROOT>/results/codex_gpt-5.4_openclaw_rephrase_v2/openclaw/infer | grep -A2 {TASK_ID}` to see which questions passed in v2.
2. For each passing exec_check question, decide which v3 levers (D++/C++/F/G/H) to apply.
3. Edit `<REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/scripts/apply_{TASK_ID}_rephrase.py`'s REPHRASES dict — modify the question text, **shrink preserved_tokens lists** as you strip more.
4. Run apply script — must exit 0.
5. Run diff emitter to refresh diff doc.
6. Append "## v3 super-harden notes" to `alignment/{TASK_ID}.md`.

## Self-check

Apply script exits 0 — every preserved token literal-matches in new text.

## Output report (≤ 300 words)

- Which v2-passing questions you targeted
- Which levers stacked per question
- Estimated additional fails (target: 3-5 more than v2)
- Any BROKEN concerns
