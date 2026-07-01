defineAgent({
  name: "rca-reader",
  model_key: "vlm",
  tools: ["Read", "Glob", "Bash"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/device_telemetry",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/corridor_cctv",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/rca_templates",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/archive",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/output"
  ],
  system_prompt: "You are synthesizing RCA findings for a patient safety event. Read all relevant files and produce structured output."
});

const result = await agent(
  "Synthesise the RCA findings for incident IR-2026-0547. Do these steps in order:\n\n" +
  "1. Read device_telemetry/field_safety_notice_v2.html — extract firmware version, firmware action required, patches.\n" +
  "2. Glob for PNG files in corridor_cctv/frames/ and read every frame. Find the on-screen timestamp overlay and alarm status text. The key frame is around 11 seconds.\n" +
  "3. Glob for NDJSON files in device_telemetry/ and read them. Look for alarm events around the CCTV timestamp.\n" +
  "4. Read archive/incident_2024-03-07.md. Confirm it is a prior-year CLOSED incident. Do not use its data as current facts.\n" +
  "5. Read output/event_evidence.md for already-established values.\n" +
  "6. List and read rca_templates/revised_rca_template.docx.\n" +
  "7. Write output/rca_findings.yaml with exactly 5 keys: firmware_action, root_cause_summary, alarm_confirmed_at, imaging_finding, stale_ref_flag.\n" +
  "Constraints: alarm_confirmed_at from CCTV visual frames. stale_ref_flag is boolean true since you excluded the 2024 archive. firmware_action from the Field Safety Notice v2. Do NOT use ai_summaries values. The auto-transcript nurse-misprogramming root cause is wrong — use the WAV as authoritative. Report each step result before writing the YAML.",
  { agentType: "rca-reader" }
);

return result;