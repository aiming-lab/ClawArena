export const meta = { name: "read_agreements_targeted" };

defineAgent({
  name: "term_extractor",
  model_key: "llm",
  tools: ["Read", "Grep"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/grant_agreements"
  ],
  system_prompt: "You extract specific sections from a grant agreement. Read the file in chunks using offset/limit as needed. For each target section, return the exact text. Do NOT summarize — return the verbatim section content."
});

// Read Halcyon agreement with targeted extraction
const halcyon = await agent(
  "Read grant_agreements/halcyon_agreement_2025.md. This file is large (~20k tokens). Read it fully, possibly in multiple passes using offset/limit.\n\nExtract ONLY these sections, returning the exact text of each:\n1. The section listing eligible expenditure categories (with any caps)\n2. The section on travel documentation/approval requirements\n3. The section on indirect/overhead costs (including Appendix III §3.4)\n4. The section on equipment purchase thresholds\n\nFor each, quote the section number and return the full clause text. Be precise — do not summarize or paraphrase.",
  { agentType: "term_extractor" }
);

return { halcyon: halcyon };