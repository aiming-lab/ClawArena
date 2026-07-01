export const meta = { name: "read_receipts_images" };

defineAgent({
  name: "receipt_reader",
  model_key: "vlm",
  tools: ["Read", "Glob"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/receipts"
  ],
  system_prompt: "You read scanned receipt images and extract: vendor name, date, stated amount (with currency), and expense category. Return structured data for each receipt."
});

// Read the index first
const index = await agent(
  "Read receipts/_index.md and return its full content.",
  { agentType: "receipt_reader" }
);

// Now read RCP-001 through RCP-006 and RCP-008 (legible receipts)
const receipts = await parallel([
  () => agent("Read the image at receipts/RCP-001.png. Extract: vendor name, date, amount (with currency), and expense category. Return as a single structured entry.", { agentType: "receipt_reader" }),
  () => agent("Read the image at receipts/RCP-002.png. Extract: vendor name, date, amount (with currency), and expense category. Return as a single structured entry.", { agentType: "receipt_reader" }),
  () => agent("Read the image at receipts/RCP-003.png. Extract: vendor name, date, amount (with currency), and expense category. Return as a single structured entry.", { agentType: "receipt_reader" }),
  () => agent("Read the image at receipts/RCP-004.png. Extract: vendor name, date, amount (with currency), and expense category. Return as a single structured entry.", { agentType: "receipt_reader" }),
  () => agent("Read the image at receipts/RCP-005.png. Extract: vendor name, date, amount (with currency), and expense category. Return as a single structured entry.", { agentType: "receipt_reader" }),
  () => agent("Read the image at receipts/RCP-006.png. Extract: vendor name, date, amount (with currency), and expense category. Return as a single structured entry.", { agentType: "receipt_reader" }),
  () => agent("Read the image at receipts/RCP-008.png. Extract: vendor name, date, amount (with currency), and expense category. Return as a single structured entry.", { agentType: "receipt_reader" })
]);

return {
  index: index,
  receipts: {
    "RCP-001": receipts[0],
    "RCP-002": receipts[1],
    "RCP-003": receipts[2],
    "RCP-004": receipts[3],
    "RCP-005": receipts[4],
    "RCP-006": receipts[5],
    "RCP-008": receipts[6]
  }
};