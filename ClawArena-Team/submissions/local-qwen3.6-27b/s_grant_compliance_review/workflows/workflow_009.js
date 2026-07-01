export const meta = { name: "read_nordic_agreement" };

defineAgent({
  name: "term_extractor",
  model_key: "llm",
  tools: ["Read", "Grep"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/grant_agreements"
  ],
  system_prompt: "You extract specific sections from a grant agreement. Read carefully, using offset/limit if needed. Return exact text with section numbers. For §9, explicitly label it as non-binding."
});

const nordic = await agent(
  "Read grant_agreements/nordic_agreement_2025.md fully. This is a large file (~20k tokens).\n\nCRITICAL: §9 is labeled 'Non-Binding Programmatic Clarification'. Only terms in §§1-8 are binding.\n\nExtract these sections, returning the exact text:\n1. Eligible expenditure categories (with caps) — from binding sections only\n2. Travel documentation requirements\n3. Indirect/overhead costs eligibility\n4. Equipment purchase thresholds\n5. What §9 says (label as NON-BINDING)\n\nFor each finding, state the section number and whether it is binding or non-binding.",
  { agentType: "term_extractor" }
);

return { nordic: nordic };