defineAgent({
  name: "reader",
  model_key: "llm",
  tools: ["Read"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_ab_test_postmortem/work/docs",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_ab_test_postmortem/work/tools"
  ],
  system_prompt: "Read files and return their full content verbatim."
});

const r1 = await agent("Read docs/mobile_ios14_bugzilla.md and return its full content.", { agentType: "reader" });
const r2 = await agent("Read docs/pytest_mobile_us_log.txt and return its full content.", { agentType: "reader" });
const r3 = await agent("Read tools/verify_decision.py and return its full content.", { agentType: "reader" });

return { bugzilla: r1, pytest: r2, verify: r3 };