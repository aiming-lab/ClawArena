export const meta = { name: "lint_and_risk_summary" };

defineAgent({
  name: "risk-synthesizer",
  model_key: "llm",
  tools: ["Read", "Write"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_release_audit_giant/work/output",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_release_audit_giant/work/analysis",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_release_audit_giant/work/release_notes_draft.md"
  ],
  system_prompt: "You synthesize findings from multiple audit notes into a consolidated risk summary. You must cite at least one previous note by its file path (e.g. output/notes/q2_security.md)."
});

phase("1. Kick off lint_release.sh in background");

// Run lint in background via the main agent's Bash — this is a background bash command
// The workflow itself can't run bash, so we return a flag; the lint is handled outside the workflow.
// Instead, the workflow agent writes the risk summary while lint runs independently.

phase("2. Synthesize risk summary from existing findings");

const summary = await agent(
`Read the following files and produce a consolidated risk summary for the v2.4 release:

1. Read /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_release_audit_giant/work/output/notes/q1_modules.md
2. Read /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_release_audit_giant/work/output/notes/q2_security.md
3. Read /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_release_audit_giant/work/output/notes/q3_deprecated.md
4. Read /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_release_audit_giant/work/output/release_summary.json
5. Read /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_release_audit_giant/work/release_notes_draft.md

Then write a consolidated risk summary to /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_release_audit_giant/work/analysis/risk_summary.md.

The summary must:
- Cover all three pending issues and their affected modules
- Include the security blast radius analysis
- Include the deprecation footprint and the recording-vs-docs conflict
- Rate overall release risk (High/Medium/Low) with justification
- Cite at least one previous finding by its exact file path (e.g. "see output/notes/q2_security.md")
- List recommended actions before merging to main

Write the markdown file directly. Return "done" on success.`,
{ agentType: "risk-synthesizer" });

return { risk_summary_written: summary };