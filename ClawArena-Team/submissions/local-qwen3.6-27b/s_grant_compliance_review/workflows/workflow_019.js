export const meta = { name: "read_waiver" };

defineAgent({
  name: "waiver_reader",
  model_key: "llm",
  tools: ["Read"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/correspondence"
  ],
  system_prompt: "Read grantor correspondence and return exact text."
});

const waiver = await agent(
  "Read the file at:\n/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/correspondence/thread_grantor_a_waiver.md\n\nReturn the FULL text of this waiver email.",
  { agentType: "waiver_reader" });

return { waiver: waiver };