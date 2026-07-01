export const meta = { name: "read_ledger_full" };

defineAgent({
  name: "ledger_full_reader",
  model_key: "llm",
  tools: ["Read", "Grep"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/ledger"
  ],
  system_prompt: "Read the full reimbursement ledger CSV and return all rows grouped by grantor prefix. Do not summarize — return every row."
});

const result = await agent(
  "Read the full CSV at:\n/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/ledger/reimbursements_fy2025.csv\n\nThis has 310 rows. I need you to categorize every transaction by grantor prefix (GRA for Halcyon, GRB for Nordic, GRC for Opal City) and list them all.\n\nFor each transaction, show: txn_id, grantor_id, date, vendor, category, amount_usd, receipt_ref, approval_flag, notes.\n\nGroup by grantor prefix and list all transactions within each group.",
  { agentType: "ledger_full_reader" });

return result;