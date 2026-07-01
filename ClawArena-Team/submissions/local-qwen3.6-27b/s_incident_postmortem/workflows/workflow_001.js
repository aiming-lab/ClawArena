defineAgent({
  name: "log-grepper",
  model_key: "llm",
  tools: ["Grep", "Read"],
  accessible_paths: ["/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/logs"],
  system_prompt: "You search log files using Grep. Given a file path, use Grep to find the FIRST line matching ERROR, FATAL, PANIC, OOM, or eviction-related errors within the 14:20-14:50 UTC time window. Return the earliest match: timestamp, level, and full message. If nothing matches, say so."
});

const SERVICES = [
  "payments-api",
  "redis-fleet-2",
  "auth-edge",
  "orders-api",
  "user-profile",
  "search-index",
  "cdn-router",
  "notifications"
];

const LOG_ROOT = "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/logs";

// For each service, grep for the first error/warn in the 14:20-14:50 window
const results = [];

for (const svc of SERVICES) {
  const filePath = `${LOG_ROOT}/${svc}_2026-05-12.log`;
  phase(`Scanning ${svc} logs`);

  const resp = await agent(
    `Search ${filePath} for the VERY FIRST error-level or warning-level line between 14:20 and 14:50 UTC.

Use Grep with a regex that matches timestamps like "14:20:.." through "14:50:.." combined with keywords ERROR, FATAL, PANIC, OOM, evict, crash, timeout, 5xx.

Steps:
1. First, run a broad Grep for lines matching the time window AND any error keyword.
2. If nothing, try WARN, then just the time window to see what's there.
3. Return the EARLIEST matching line with exact timestamp, log level, and message.
4. If no errors found in that window at all, say so explicitly.`,
    { agentType: "log-grepper" }
  );

  results.push({ service: svc, finding: resp });
}

return results;