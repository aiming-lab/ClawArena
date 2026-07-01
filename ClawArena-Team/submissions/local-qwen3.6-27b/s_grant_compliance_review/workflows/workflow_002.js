export const meta = { name: "verify_agreements" };

defineAgent({
  name: "agreement_reader",
  model_key: "llm",
  tools: ["Read", "Grep", "Glob"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/grant_agreements"
  ],
  system_prompt: "You read grant agreement files carefully. Return the exact content you find, quoting section numbers and dollar amounts precisely. Do NOT hallucinate or infer — return only what is written in the file."
});

// First read the index
const index = await agent(
  "Read grant_agreements/_index.md and return its full content.",
  { agentType: "agreement_reader" }
);

return {
  index: index,
  note: "Checking if the three agreements were read correctly. Next step: re-read each file."
};