export const meta = { name: "read_opal_agreement_fixed" };

defineAgent({
  name: "term_extractor",
  model_key: "llm",
  tools: ["Read", "Grep"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/grant_agreements"
  ],
  system_prompt: "You extract specific sections from a grant agreement. Return exact text with section numbers."
});

const opal = await agent(
  "Read grant_agreements/opal_city_contract_2025.md fully. This is a large file (~20k tokens).\n\nExtract these sections, returning the exact text:\n1. Eligible expenditure categories (with caps)\n2. Travel documentation requirements\n3. Indirect/overhead costs eligibility\n4. Equipment purchase thresholds\n5. Any excluded categories (especially entertainment)\n\nFor each finding, quote the section number and full clause text.",
  { agentType: "term_extractor" });

return { opal: opal };