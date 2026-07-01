export const meta = { name: "extract_nordic_abs" };

defineAgent({
  name: "nordic_extractor",
  model_key: "llm",
  tools: ["Read", "Grep"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/grant_agreements"
  ],
  system_prompt: "You extract specific sections from a grant agreement file. Always use absolute paths. Return exact text with section numbers."
});

const nordic = await agent(
  "Read the file at this absolute path:\n/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/grant_agreements/nordic_agreement_2025.md\n\nThis is a large file. CRITICAL: §9 is labeled 'Non-Binding Programmatic Clarification'. Only terms in §§1-8 are binding.\n\nExtract these sections:\n1. Eligible expenditure categories (with caps) — from binding sections only\n2. Travel documentation requirements\n3. Indirect/overhead costs eligibility\n4. Equipment purchase thresholds\n5. What §9 says (label as NON-BINDING)\n\nFor each finding, state the section number and whether it is binding or non-binding. Return exact clause text where possible.",
  { agentType: "nordic_extractor" });

return { nordic: nordic };