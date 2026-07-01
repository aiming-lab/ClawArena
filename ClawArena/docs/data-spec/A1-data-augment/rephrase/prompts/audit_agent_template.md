# Audit Agent Prompt — TEMPLATE

You are auditing a v1 rephrase of test questions for solvability and three-way consistency. Read-only, report findings — do not modify any files.

## Background

`{TASK_ID}` is a benchmark task with N rounds. Some rounds are `type: "exec_check"` (the agent must produce a file/script and an `eval` command checks it). The rephrase pass aimed to make the questions sound more human (less robotic) AND increase difficulty by hiding hard-coded answer values that the agent should instead recover from the workspace.

Your job: verify each rephrased exec_check question is **solvable** — i.e., a competent agent reading ONLY the workspace files visible at that round + the rephrased question text can produce an artifact that passes the corresponding `eval` command.

This is the **question / workspace / eval** triangle — all three must align:
- the question must give the agent enough direction
- the workspace must contain the values/concepts the agent needs
- the eval must check what the question actually asked for

## Inputs

- **Rephrased questions** (audit target): `<REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/rephrased/{TASK_ID}/questions.json`
- **Original questions** (for comparison): `<REPO_ROOT>/data/clawarena/eval/{TASK_ID}/questions.json`
- **Diff for fast review**: `<REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/diff/{TASK_ID}.md`
- **Author's alignment doc** (their own classification of strip-decisions): `<REPO_ROOT>/docs/data-spec/A1-data-augment/rephrase/alignment/{TASK_ID}.md`
- **Eval scripts** (what actually checks answers): `<REPO_ROOT>/data/clawarena/eval/{TASK_ID}/scripts/`. Each `eval.command` in questions.json invokes one of these or a shell pipeline.
- **Initial workspace** (round 0): `<REPO_ROOT>/data/clawarena/nanobot/workspaces/{TASK_ID}/`
- **Update bundles**: `<REPO_ROOT>/data/clawarena/nanobot/updates/{TASK_ID}/upd<N>_{sessions,workspace}/`

## Round visibility

Each round in questions.json has an `update_ids` list. Empty means same visibility as the previous round; entries like `["upd1_sessions","upd1_workspace"]` mean those bundles become visible at this round and remain visible thereafter. Compute round visibility by walking forward from round 1.

(Multi-choice rounds were NOT rephrased — skip them.)

## What to check, per exec_check question

For each rephrased exec_check round:

1. **Read the eval command** in `eval.command`. What does it actually grep / assert / schema-validate? Identify every literal string, file path, JSON field name, and value the eval enforces.

2. **Read the rephrased question text**. Does it tell the agent enough — directly or via a pointer to a workspace file — to produce all the eval-required outputs?

3. **For every value the original question stated explicitly that the rephrase removed** — verify that value is **actually findable** in workspace files visible at that round. Use Grep on the workspace+update dirs.

4. **Flag any question where the eval check is grep-fragile** (a literal string match the agent might phrase differently after rephrasing) AND the rephrase doesn't preserve that literal.

5. **Flag any over-stripping**: cases where the rephrase hid so much information that the agent cannot reasonably know what the eval wants.

6. **Flag any under-stripping**: cases where the rephrase still leaks an answer value that should have been hidden (less critical).

## Output

A concise per-question table or list, one row per exec_check round:

```
qN | verdict | issue (if any)
```

Where `verdict` is one of:
- **OK** — solvable, three-way aligned
- **RISK** — solvable but fragile (e.g., eval grep is literal but rephrase makes it easy to miss); explain
- **BROKEN** — not solvable from workspace + rephrased question; explain why

Be specific: cite the eval command's exact grep / assertion, the workspace file (path + line number when possible) that contains the recoverable value, and the exact phrasing in the rephrased question that points (or fails to point) the agent there.

End with a short summary: total OK / RISK / BROKEN counts and the top 3 most important issues to address.

Keep the report under **1500 words**. Don't paraphrase the questions; cite by qN and a short distinctive phrase.
