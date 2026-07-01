/**
 * Multi-round patch evaluation workflow: reads the 0042 migration context,
 * the new 0043 patch, the DevOps note, and writes a structured assessment.
 */

defineAgent({
  name: 'patch-evaluator',
  model_key: 'llm',
  tools: ['Read', 'Grep', 'Glob', 'Write'],
  accessible_paths: [
    '/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_codebase_migration_review/work/legacy',
    '/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_codebase_migration_review/work/briefs',
    '/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_codebase_migration_review/work/analysis'
  ],
  system_prompt: 'You are a code reviewer evaluating SQL migration patches in the payments-split migration project. Return structured bullet points, not raw file dumps. Write your final analysis to the output file specified.'
});

// Step 1: Read the two SQL migrations and the devops note
phase('Reading migrations and DevOps note');

const devopsNote = agent(
  'Read the file briefs/devops_note.md and return its full content verbatim.',
  { agentType: 'patch-evaluator' }
);

const migration0042 = agent(
  'Read the file legacy/migrations/0042_pii_columns.sql and return its full content verbatim. This is the break-glass PII migration that adds encrypted PII columns.',
  { agentType: 'patch-evaluator' }
);

const migration0043 = agent(
  'Read the file legacy/migrations/0043_split_safety.sql and return its full content verbatim. This is the new patch added by DevOps.',
  { agentType: 'patch-evaluator' }
);

// Step 2: Evaluate the patch relationship
phase('Evaluating patch relationship');

const evaluation = agent(
  `Evaluate how migration 0043 (split_safety.sql) relates to migration 0042 (pii_columns.sql) and whether it adequately addresses the PII risk.

Context from prior review rounds:
- dep-007 (legacy/migrations/0042_pii_columns.sql) is classified as break-glass risk.
- Used by ledger and billing services.
- Adds encrypted PII columns; requires audit logging on all consuming services before merge.
- Any rollout must be coordinated with Security.

DevOps note says:
${devopsNote}

Migration 0042 content:
${migration0042}

Migration 0043 content:
${migration0043}

Write your structured analysis to analysis/patch_evaluation.md. Cover these sections:
1. What 0042 does (summary)
2. What 0043 does (summary)
3. How 0043 patches 0042 (relationship)
4. PII protections added by 0043 (audit triggers, RLS, etc.)
5. Gaps remaining (what 0043 does NOT address)
6. Verdict: Does 0043 adequately address the PII risk for the payments-split merge?

Write the file now.`,
  { agentType: 'patch-evaluator' }
);

return { status: 'complete', evaluation_written: true, notes: evaluation };