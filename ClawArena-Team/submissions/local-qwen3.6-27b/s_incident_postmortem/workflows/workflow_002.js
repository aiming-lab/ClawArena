defineAgent({
  name: "grep-only",
  model_key: "llm",
  tools: ["Grep"],
  accessible_paths: ["/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/logs"],
  system_prompt: "Use ONLY Grep (not Read). Search a single log file for the first ERROR line in the 14:20-14:50 UTC window. Use head_limit=1. Return the exact line."
});

const LOG_ROOT = "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/logs";
const SERVICES = ["payments-api", "redis-fleet-2", "auth-edge", "orders-api", "user-profile", "search-index", "cdn-router", "notifications"];

const results = await parallel(SERVICES.map(svc => () => {
  const f = `${LOG_ROOT}/${svc}_2026-05-12.log`;
  return agent(
    `Use Grep on ${f} to find the FIRST line containing ERROR (case-insensitive) where the timestamp is between 14:20 and 14:50. Use pattern: '14:(2[0-9]|3[0-9]|4[0-9]):[0-5][0-9].*ERROR'. Set head_limit=1 and output_mode=content. Return the exact matching line or say none found.`,
    { agentType: "grep-only" }
  );
}));

return results;