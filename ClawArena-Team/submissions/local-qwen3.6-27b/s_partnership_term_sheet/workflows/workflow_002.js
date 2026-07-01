defineAgent({
  name: "ts-reader",
  model_key: "llm",
  tools: ["Read", "Glob", "Grep"],
  accessible_paths: ["/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_partnership_term_sheet/work/term_sheets"],
  system_prompt: "You are a legal document analyst. Read the term sheet file assigned to you and extract EXACT values for three dimensions: (1) Economic Split, (2) Board Governance Composition, (3) IP Ownership Terms. Return only the extracted facts as structured bullets under each heading with exact numbers and quoted terms."
});

const files = await Glob({ pattern: "**/*", path: "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_partnership_term_sheet/work/term_sheets" });

const results = await parallel(files.map(f => () => agent(
  "Read the file at path: " + f + ". Extract the three dimensions: Economic Split, Board Governance Composition, IP Ownership Terms. Return exact figures, percentages, seat counts, and quoted terms. Structure your output under these three headings.",
  { agentType: "ts-reader" }
)));

return { files_listed: files, extractions: results };