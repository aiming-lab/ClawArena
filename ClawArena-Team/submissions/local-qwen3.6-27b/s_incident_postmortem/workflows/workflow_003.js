defineAgent({
  name: "grep-correct",
  model_key: "llm",
  tools: ["Grep"],
  accessible_paths: ["/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/logs"],
  system_prompt: "Use ONLY Grep. Search log files using ISO 8601 timestamps. Find the FIRST ERROR line between 14:20 and 14:50 UTC."
});

const LOG_ROOT = "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/logs";
const SERVICES = ["payments-api", "redis-fleet-2", "auth-edge", "orders-api", "user-profile", "search-index", "cdn-router", "notifications"];

// Pattern: 2026-05-12T14:(20-49):.. [ERROR]
const results = await parallel(SERVICES.map(svc => () => {
  const f = `${LOG_ROOT}/${svc}_2026-05-12.log`;
  return agent(
    `Use Grep on ${f} to find the FIRST line containing [ERROR] where the ISO timestamp hour:minute is between 14:20 and 14:50.

Use pattern: '2026-05-12T14:(2[0-9]|3[0-9]|4[0-9]):[0-5][0-9].*\\\\[ERROR\\\\]'
Set output_mode=content, head_limit=1.

Return the exact matching line. If none found, try a broader pattern for just '[ERROR]' in the 14:xx range. Say 'none found' only if truly nothing matches.`,
    { agentType: "grep-correct" }
  );
}));

return results;