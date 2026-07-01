export const meta = { name: "extract_nordic_terms" };

defineAgent({
  name: "nordic_reader",
  model_key: "llm",
  tools: ["Read", "Grep"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/grant_agreements"
  ],
  system_prompt: "Read the Nordic Development Cooperative grant agreement carefully. Return exact terms with section numbers. IMPORTANT: §9 is explicitly labeled non-binding. Only extract terms from §§1-8 as binding. Clearly label any §9 content as non-binding guidance only."
});

const result = await agent(
  "Read grant_agreements/nordic_agreement_2025.md fully. CRITICAL: §9 is labeled 'Non-Binding Programmatic Clarification' — do NOT treat any of §9 as a binding constraint. Binding terms are only in §§1-8.\n\nExtract these four areas from the BINDING sections only (unless §9 is relevant as context):\n\n1. Eligible expenditure categories — list each category and any per-item or percentage caps.\n2. Travel documentation requirements — prior approval, receipts, forms needed.\n3. Indirect/overhead costs — eligible? What rate or ceiling?\n4. Equipment purchase thresholds — minimum amounts, pre-approval rules.\n\nFor each finding, note whether it comes from a binding section (§§1-8) or the non-binding §9.\n\nReturn as structured bullet points under each heading. Quote section numbers.",
  { agentType: "nordic_reader" }
);

return { nordic: result };