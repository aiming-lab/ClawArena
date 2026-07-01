export const meta = { name: "extract_halcyon_terms" };

defineAgent({
  name: "halcyon_reader",
  model_key: "llm",
  tools: ["Read", "Grep"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/grant_agreements"
  ],
  system_prompt: "Read the Halcyon Foundation grant agreement carefully. Return exact terms with section numbers. Focus on: (1) eligible categories with caps, (2) travel documentation rules, (3) indirect/overhead cost eligibility and rate, (4) equipment purchase thresholds. Quote section numbers. Do NOT fabricate terms."
});

const result = await agent(
  "Read grant_agreements/halcyon_agreement_2025.md fully. Extract these four areas with exact section numbers and dollar amounts:\n\n1. Eligible expenditure categories — list each category and any per-item or percentage caps.\n2. Travel documentation requirements — prior approval, receipts, forms needed.\n3. Indirect/overhead costs — eligible? What rate or ceiling?\n4. Equipment purchase thresholds — minimum amounts, pre-approval rules.\n\nReturn as structured bullet points under each heading. Quote section numbers.",
  { agentType: "halcyon_reader" }
);

return { halcyon: result };