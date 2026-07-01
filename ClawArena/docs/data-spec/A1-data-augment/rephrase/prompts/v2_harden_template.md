# v2 Hardening Agent Prompt — TEMPLATE

You are **hardening** the v1 rephrase of exec_check questions for one ClawArena benchmark task. The v1 rephrase was too lenient — gpt-5.4 still scored 85-100% on this task. We need to drop ec score on this task to ~50-65%.

## Inputs

- **Task ID**: `{TASK_ID}`
- **v1 rephrased questions** (your starting point): `<REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/rephrased/{TASK_ID}/questions.json`
- **Original (pre-rephrase) questions** (for comparison): `<REPO_ROOT>/data/clawarena/eval/{TASK_ID}/questions.json` — NOTE: this file has now been **overwritten with v1**, so look at `data-augment/rephrase/diff/{TASK_ID}.md` for the original-vs-v1 diff.
- **v1 alignment doc**: `<REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/alignment/{TASK_ID}.md`
- **v1 apply script**: `<REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/scripts/apply_{TASK_ID}_rephrase.py`
- **Eval scripts**: `<REPO_ROOT>/data/clawarena/eval/{TASK_ID}/scripts/`
- **Workspace** (round 0): `<REPO_ROOT>/data/clawarena/nanobot/workspaces/{TASK_ID}/`
- **Update bundles**: `<REPO_ROOT>/data/clawarena/nanobot/updates/{TASK_ID}/upd<N>_{sessions,workspace}/`
- **v1 per-question pass/fail data**: see `data-augment/rephrase/scripts/extract_per_q_pass.py` output for which questions agent passed too easily — those are your hardening targets

## Goal

Modify `apply_{TASK_ID}_rephrase.py`'s `REPHRASES` dict to make exec_check questions **harder** without breaking solvability. Re-run the script to regenerate `rephrased/{TASK_ID}/questions.json`. Re-run `emit_*_diff.py` if needed.

## Four Hardening Levers

Apply these aggressively. The v1 was too gentle.

### A. Strip P-rule labels

If v1 says "**P1**/**P2**/**P3** apply" or "P5 communication rules apply", replace with indirect references like "the team's house style guide has rules for this", "follow the formatting conventions documented for the team", "stick to whatever the style doc says about [tone/structure/numbers]". Agent must read `style_guide.md` (in workspace) to recover P-rule details. Do not name the P-codes.

**Why this works**: eval validates compliance with P-rules, but agents who don't see "P1 P2 P3" tags in the question often forget to apply specific formatting (ISO 8601, thousands-sep, file-name prefix, etc.).

### B. Prose-ify JSON schema code blocks

If v1 includes ```json {...} ``` schema blocks listing every field, convert to prose: "Save a JSON with the action's id, a description, an owner, status, and due-date — schema fields are conventional snake_case." Agent must derive exact field names from prose semantics. Risk: agent picks `due_date` instead of `due`, fails strict schema check.

**Caveat**: keep the schema block ONLY where the validator script is `check_schema.py --schema X` style and the schema file is **not** in the agent's workspace. In those cases stripping is fair (agent should match conventional names). Where the schema is unconventional (e.g., `staff_nurses_understated_count`, `mock_date`), keep at least the unconventional field names verbatim — otherwise BROKEN.

### C. Inject misleading distractors

Replace the v1 "tangential and true" distractors with **mildly misleading** sentences that an agent might trust without verification. Examples:
- "I think Maya mentioned the threshold was 45 days but I'm not sure" (when actual is 30)
- "the changelog only added the channel column, but I recall seeing a price field too" (false addition)
- "the contamination is around 15%" (when actual is 23%)
- "the deadline is March 7 — or maybe March 14, check the meeting notes" (forces agent to verify)

**Hard rule**: the misleading hint must be flagged as uncertain ("I think", "maybe", "not sure", "or check"). Never assert a falsehood. Agent who reads workspace finds truth.

**Why this works**: agents pattern-match on assertive hints. Hedged-but-wrong hints sometimes leak into outputs.

### D. Drop more literal grep targets

Re-read each `eval.command`. Find every literal string the eval checks (`grep -q "X"`, schema keys, regex patterns). For each:
- If it's directly in a workspace file → strip from question, force agent to read it
- If it's a derivable computation (counts, percentages, dates) → strip and force agent to compute
- If it's an unconventional name the agent won't guess (e.g., `pip-email-chain.md` filename) → keep verbatim

**Be aggressive**. v1 kept many grep-targets "for safety". Now relax that — accept some questions WILL fail on literal-mismatch. That's the point.

## Hard preservation (unchanged from v1)

You still MUST preserve verbatim:

1. **Output paths** (`project/docs/foo.json`, `data/processed/bar.csv`)
2. **Filename pattern templates** (`YYYY-MM-DD_*_v<N>.md`, `*_progress_update_v1.md`)
3. **Unconventional schema field names** that agent won't guess (e.g., `staff_nurses_understated_count`, `mock_date`, `compliant_72h`)
4. **Standard schema field names** if the schema is referenced by `check_schema.py --schema X` and the schema file is NOT in agent workspace AND fields are conventional (id, description, etc.) — you may prose-ify these per Lever B

## Distractor density

v1: ≥1 sentence per question. v2: **≥2 sentences for at least half the questions**. Mix tangential + misleading.

## Workflow

1. Read v1 rephrased questions.json, v1 alignment doc, v1 apply script.
2. Read pass/fail map for this task (run `python3 <REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/scripts/extract_per_q_pass.py | grep -A2 "{TASK_ID}"` if helpful).
3. For each exec_check question, decide which of levers A/B/C/D to apply (often multiple).
4. Edit `apply_{TASK_ID}_rephrase.py` REPHRASES dict — modify each entry's text. **You may also need to edit the preserved_tokens list** to drop tokens you've now stripped from the new text. Self-check still requires every preserved token literally present.
5. Run the script. Confirm exit 0.
6. Run `emit_{TASK_ID}_diff.py` (or write a parameterized diff if missing) to regenerate the diff doc.
7. Append a section to `alignment/{TASK_ID}.md` titled "## v2 hardening notes" briefly describing which levers you used per question.

## Self-check (still required)

Apply script must exit 0 — every token in updated `preserved_tokens` literal-matches in updated text. If you strip a value but the eval grep-checks it literally, the agent's output (not the question) must still produce it; that's solvable by workspace reading. The preserved_tokens list is for what MUST be in the **question**, not the output.

## Output report (back to me)

After hardening, return a report ≤ 400 words:

- Which questions you hardened most aggressively and which levers (A/B/C/D)
- Which questions you LEFT v1 unchanged (and why — typically already-hard or already-failed-by-agent)
- Self-check result (must be exit 0)
- Any concern that you may have crossed into BROKEN territory

Do not paste rephrased text. Artifacts on disk are the deliverable.
