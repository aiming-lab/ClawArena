export const meta = { name: "rcp007_fix_abs" };

defineAgent({
  name: "rcp007_reader",
  model_key: "vlm",
  tools: ["Read"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/receipts"
  ],
  system_prompt: "You read receipt images. Always use absolute file paths."
});

defineAgent({
  name: "ledger_searcher",
  model_key: "llm",
  tools: ["Read", "Grep"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/ledger"
  ],
  system_prompt: "You search a CSV ledger file. Always use absolute file paths. Return matching rows exactly."
});

const image_result = await agent(
  "Read the image at this absolute path:\n/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/receipts/RCP-007.png\n\nThis image has a known legibility issue with the amount field. Extract:\n1. Vendor name\n2. Date\n3. Expense category\n4. Amount (report what you can read; if unclear, flag it)\n\nReturn structured data.",
  { agentType: "rcp007_reader" });

const ledger_result = await agent(
  "Read the CSV file at this absolute path:\n/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/ledger/reimbursements_fy2025.csv\n\nSearch for rows where:\n- The vendor column contains 'Nordic Supply'\n- The grantor_id column starts with 'GRB'\n\nReturn ALL matching rows with every column value. Do not summarize.",
  { agentType: "ledger_searcher" });

return {
  rcp007_image: image_result,
  ledger_match: ledger_result
};