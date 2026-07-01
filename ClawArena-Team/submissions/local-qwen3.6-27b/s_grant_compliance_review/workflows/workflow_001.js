export const meta = { name: "extract_grant_terms" };

defineAgent({
  name: "terms_extractor",
  model_key: "llm",
  tools: ["Read", "Grep", "Glob"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/grant_agreements"
  ],
  system_prompt: "You extract binding terms from a grant agreement. Return a structured summary covering: (1) eligible expenditure categories with any per-item or percentage caps, (2) documentation requirements for travel, (3) whether indirect/overhead costs are eligible and at what rate, (4) equipment purchase thresholds or restrictions. If any section is explicitly labeled non-binding, flag it clearly. Return ONLY the structured facts, no preamble or commentary."
});

const agreements = [
  { file: "grant_agreements/halcyon_agreement_2025.md", grantor: "Grantor A — Halcyon Foundation" },
  { file: "grant_agreements/nordic_agreement_2025.md", grantor: "Grantor B — Nordic Development Cooperative" },
  { file: "grant_agreements/opal_city_contract_2025.md", grantor: "Grantor C — Opal City Community Fund" }
];

const results = await parallel(agreements.map(a => () =>
  agent(`Read the full grant agreement and extract all binding terms. Focus on:

1. Eligible expenditure categories — list each category and any per-item or percentage caps.
2. Travel documentation requirements — what must accompany a travel claim (authorisation forms, receipts, prior written approval, etc.).
3. Indirect/overhead costs — are they eligible? If so, at what rate or ceiling?
4. Equipment purchase thresholds — minimum amounts, approval requirements, eligibility rules.

For Grantor B (Nordic), pay special attention: §9 is labeled "Non-Binding Programmatic Clarification" — clearly separate any terms from §9 as non-binding; binding terms are in §§1–8 only.

Return your answer as a structured list under these four headings. Quote section numbers where possible.`, { agentType: "terms_extractor" })
));

return results;