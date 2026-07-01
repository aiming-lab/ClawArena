export const meta = { name: "read_sop" };

defineAgent({
  name: "sop_reader",
  model_key: "llm",
  tools: ["Read", "Grep"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/internal_reports"
  ],
  system_prompt: "Read MAN's compliance SOP and return the NC numbering system rules."
});

const result = await agent(
  "Read the file at:\n/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/internal_reports/compliance_sop_v4.md\n\nExtract the NC numbering system rules, remediation action categories, and any classification guidance.\n\nReturn the full relevant text.",
  { agentType: "sop_reader" });

return result;