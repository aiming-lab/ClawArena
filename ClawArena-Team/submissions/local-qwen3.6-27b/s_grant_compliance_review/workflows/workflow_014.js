export const meta = { name: "extract_halcyon_abs" };

defineAgent({
  name: "halcyon_extractor",
  model_key: "llm",
  tools: ["Read", "Grep"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/grant_agreements"
  ],
  system_prompt: "You extract specific sections from a grant agreement file. Always use absolute paths. Return exact text with section numbers."
});

const halcyon = await agent(
  "Read the file at this absolute path:\n/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/grant_agreements/halcyon_agreement_2025.md\n\nThis file was recently updated (amended Appendix III). Extract these sections:\n1. Eligible expenditure categories (with caps)\n2. Travel documentation requirements (especially §4.1.b on international travel prior approval)\n3. Indirect/overhead costs eligibility (especially Appendix III §3.4)\n4. Equipment purchase thresholds\n\nFor each finding, quote the section number and full clause text.",
  { agentType: "halcyon_extractor" });

return { halcyon: halcyon };