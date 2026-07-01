export const meta = { name: "rcp007_and_ledger" };

defineAgent({
  name: "rcp007_reader",
  model_key: "vlm",
  tools: ["Read"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/receipts"
  ],
  system_prompt: "Read this degraded receipt image. Extract vendor name, date, expense category, and the stated amount. If the amount is unclear due to low contrast, report what you CAN read and flag the ambiguity."
});

defineAgent({
  name: "ledger_reader",
  model_key: "llm",
  tools: ["Read", "Grep"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/ledger"
  ],
  system_prompt: "Read the reimbursement ledger CSV. Search for transactions matching a given vendor, date range, and grantor prefix. Return exact matching rows."
});

// Read the degraded receipt
const image_result = await agent(
  "Read the image at receipts/RCP-007.png. This image has a known legibility issue with the amount field. Extract:\n1. Vendor name\n2. Date\n3. Expense category\n4. Amount (report what you can read; if unclear, flag it)\n\nReturn structured data.",
  { agentType: "rcp007_reader" }
);

// Search ledger for Nordic Supply Co., Stockholm with GRB prefix, October 2025
const ledger_result = await agent(
  "Read the ledger file ledger/reimbursements_fy2025.csv. Search for transactions matching:\n- Vendor: 'Nordic Supply Co.' or 'Nordic Supply'\n- Grantor prefix: 'GRB' (Grantor B / Nordic)\n- Date: October 2025 (2025-10)\n\nReturn the matching row(s) with all columns: txn_id, grantor_id, date, vendor, category, amount_usd, receipt_ref, approval_flag, notes.",
  { agentType: "ledger_reader" }
);

return {
  rcp007_image: image_result,
  ledger_match: ledger_result
};