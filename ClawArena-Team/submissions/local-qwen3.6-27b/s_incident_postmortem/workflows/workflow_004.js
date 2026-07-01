defineAgent({
  name: "metrics-puller",
  model_key: "vlm",
  tools: ["Read", "Grep", "Write"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/figures",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/logs",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/output"
  ],
  system_prompt: "You extract p99 latency statistics from a Grafana PNG panel and per-service logs. Read the PNG image, find the peak p99 value, time of peak, and recovery timestamp. Cross-check with the logs. Write findings to output/metrics_pull_result.md."
});

defineAgent({
  name: "synthesis-writer",
  model_key: "llm",
  tools: ["Read", "Write"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/output"
  ],
  system_prompt: "You synthesize prior-round notes into an executive summary. Read all prior notes and the RCA JSON, then write a cohesive executive summary to output/postmortem_final.md."
});

phase("Stream A: background metrics pull");

// (a) Launch metrics pull in background
const metricsResult = agent(
  `Read the PNG image at /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/figures/p99_time_series.png.

Extract:
- Peak p99 latency value (from the y-axis of the spike)
- Time of peak (from the x-axis)
- Recovery timestamp (when the line returns to baseline)

Also cross-check: use Grep on any of the service log files under /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/logs/ to find latency values around the incident window (search for 'latency_ms' or 'p99' in payments-api logs between 14:20-14:50).

Write your findings to /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/output/metrics_pull_result.md with clear headings for peak p99, time of peak, and recovery timestamp.`,
  { agentType: "metrics-puller" }
);

phase("Stream B: main-thread final synthesis");

// (b) Main-thread synthesis
const synthesisResult = agent(
  `Read these five files:
1. /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/output/notes/q1_scope.md
2. /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/output/notes/q2_first_error.md
3. /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/output/notes/q3_dashboard.md
4. /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/output/notes/q4_comms_vs_data.md
5. /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/output/rca_summary.json

Then write a single executive summary to /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_incident_postmortem/work/output/postmortem_final.md that:
- References all five of those prior-round files explicitly by filename (e.g. "output/notes/q1_scope.md")
- States the confirmed root cause: migration v23 (v23_unbatched_shipments_update.py) causing a deadlock on orders.shipments
- Includes the impact numbers: 23-minute duration, 4,500 users impacted, $87,000 revenue impact
- Includes a one-paragraph 'Lessons Learned' section covering: (1) on-call blamed the wrong service initially, (2) the unbatched migration should never have shipped without a batching review, (3) deadlock detection thresholds need tightening
- Is concise: 3–5 paragraphs total`,
  { agentType: "synthesis-writer" }
);

return { metrics: metricsResult, synthesis: synthesisResult };