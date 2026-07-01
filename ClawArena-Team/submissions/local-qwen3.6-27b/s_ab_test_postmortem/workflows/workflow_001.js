export const meta = { name: "exp-2421-cross-tabs" };

defineAgent({
  name: "crosstab-runner",
  model_key: "llm",
  tools: ["Bash", "Read"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_ab_test_postmortem/work/data/exp_2421",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_ab_test_postmortem/work/tools"
  ],
  system_prompt: "Run a single cross-tab via python. The agent will be given a segment name. Run: python tools/run_crosstab.py data/exp_2421/<segment>.parquet. Return the full stdout output verbatim."
});

const segments = ["desktop_us", "desktop_eu", "mobile_us", "mobile_eu"];

const results = await parallel(segments.map(seg => () =>
  agent(`Run the cross-tab for segment: ${seg}`, { agentType: "crosstab-runner" })
));

return { segments: segments.map((seg, i) => ({ segment: seg, output: results[i] })) };