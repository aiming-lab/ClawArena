export const meta = { name: "exp2421-crosstab-all-segments" };

defineAgent({
  name: "crosstab-runner",
  model_key: "llm",
  tools: ["Bash", "Read"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_ab_test_postmortem/work/data/exp_2421",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_ab_test_postmortem/work/tools"
  ],
  system_prompt: "Run run_crosstab.py on a given parquet segment file. Return the full stdout output verbatim. Working directory is /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_ab_test_postmortem/work"
});

const segments = ["desktop_us", "desktop_eu", "mobile_us", "mobile_eu"];
const base = "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_ab_test_postmortem/work";

const results = await parallel(segments.map(seg => () =>
  agent(
    `Run: python tools/run_crosstab.py data/exp_2421/${seg}.parquet\nReturn the full stdout output verbatim, nothing else.`,
    { agentType: "crosstab-runner" }
  )
));

return results;