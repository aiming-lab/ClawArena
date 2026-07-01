defineAgent({
  name: "crosstab-runner",
  model_key: "llm",
  tools: ["Bash", "Read", "Write"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_ab_test_postmortem/work/data/exp_2421",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_ab_test_postmortem/work/tools",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_ab_test_postmortem/work/findings"
  ],
  system_prompt: "Run crosstab against a parquet file and write the output to a markdown file. Working directory is /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_ab_test_postmortem/work"
});

const output = await agent(
  `Run this command and capture the full stdout:\npython tools/run_crosstab.py data/exp_2421/mobile_us.parquet\n\nThen write a markdown file to findings/replication.md that contains the full output of that command as a code block. Add a brief title "EXP-2421 Replication — mobile_us Crosstab" at the top. Return the file contents.`,
  { agentType: "crosstab-runner" }
);

return output;