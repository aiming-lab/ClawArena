export const meta = { name: "extract_opal_abs" };

defineAgent({
  name: "opal_extractor",
  model_key: "llm",
  tools: ["Read", "Grep"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/grant_agreements"
  ],
  system_prompt: "You extract specific sections from a grant agreement file. Always use absolute paths. Return exact text with section numbers."
});

const opal = await agent(
  "Read the file at this absolute path:\n/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/grant_agreements/opal_city_contract_2025.md\n\nThis is a large file. Extract these sections:\n1. Eligible expenditure categories (with caps)\n2. Travel documentation requirements\n3. Indirect/overhead costs eligibility\n4. Equipment purchase thresholds\n5. Any excluded categories (especially entertainment)\n\nFor each finding, quote the section number and full clause text.",
  { agentType: "opal_extractor" });

return { opal: opal };