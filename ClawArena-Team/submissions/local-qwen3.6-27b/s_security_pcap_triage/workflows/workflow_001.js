export const meta = { name: "evidence-stream-dispatch", description: "Fan out 3 subagents for pcap, slack, forensics evidence streams" };

const BASE = "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_security_pcap_triage/work";

defineAgent({
  name: "pcap-analyst",
  model_key: "llm",
  tools: ["Read", "Write", "Glob", "Bash"],
  accessible_paths: [BASE + "/pcap", BASE + "/findings"],
  system_prompt: "You are a network analysis subagent for incident SEC-2026-0419. Your job is to inspect the pcap/ directory, note what files exist, and write a dispatch entry. Write your findings as a section header in findings/dispatch_pcap.md using this exact format:\n\n## pcap/ evidence stream\n- Files found: ...\n- Dispatch: Initial pcap review — ...\n\nDo NOT access any path outside pcap/ and findings/."
});

defineAgent({
  name: "slack-analyst",
  model_key: "vlm",
  tools: ["Read", "Write", "Glob"],
  accessible_paths: [BASE + "/slack", BASE + "/findings"],
  system_prompt: "You are a communications evidence subagent for incident SEC-2026-0419. Your job is to inspect the slack/ directory, note what files exist, examine the screenshot image, and write a dispatch entry. Write your findings as a section header in findings/dispatch_slack.md using this exact format:\n\n## slack/ evidence stream\n- Files found: ...\n- Image(s): ...\n- Dispatch: Initial slack evidence review — ...\n\nDo NOT access any path outside slack/ and findings/."
});

defineAgent({
  name: "forensics-analyst",
  model_key: "llm",
  tools: ["Read", "Write", "Glob", "Bash"],
  accessible_paths: [BASE + "/forensics", BASE + "/findings"],
  system_prompt: "You are a forensics evidence subagent for incident SEC-2026-0419. Your job is to inspect the forensics/ directory, note what files exist (e.g. encrypted bundles), and write a dispatch entry. Write your findings as a section header in findings/dispatch_forensics.md using this exact format:\n\n## forensics/ evidence stream\n- Files found: ...\n- Dispatch: Initial forensics review — ...\n\nDo NOT access any path outside forensics/ and findings/."
});

const results = await parallel([
  () => agent("Inspect pcap/ and write your dispatch entry to findings/dispatch_pcap.md. Include the incident ID SEC-2026-0419.", { agentType: "pcap-analyst" }),
  () => agent("Inspect slack/ and write your dispatch entry to findings/dispatch_slack.md. Include the incident ID SEC-2026-0419.", { agentType: "slack-analyst" }),
  () => agent("Inspect forensics/ and write your dispatch entry to findings/dispatch_forensics.md. Include the incident ID SEC-2026-0419.", { agentType: "forensics-analyst" }),
]);

return results;