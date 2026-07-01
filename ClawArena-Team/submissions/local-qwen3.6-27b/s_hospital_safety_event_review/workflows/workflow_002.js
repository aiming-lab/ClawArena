export const meta = { name: "RCA findings synthesis", description: "Read Field Safety Notice, CCTV frames, telemetry, archive, RCA template, and synthesize rca_findings.yaml" };

defineAgent({
  name: "rca-synthesis-agent",
  model_key: "vlm",
  tools: ["Read", "Glob", "Bash"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/device_telemetry",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/corridor_cctv",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/rca_templates",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/archive",
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/output"
  ],
  system_prompt: "You are synthesizing RCA findings for a patient safety event. Read all relevant files and produce a YAML output. You have access to device_telemetry/, corridor_cctv/, rca_templates/, archive/, and output/."
});

const result = await agent(`
Synthesise the RCA findings for incident IR-2026-0547. Follow these steps:

**Step 1 — Read Field Safety Notice v2:**
Read device_telemetry/field_safety_notice_v2.html. Extract: firmware version, firmware action required, any recalls or patches.

**Step 2 — Read CCTV frames:**
List files in corridor_cctv/frames/ and read all PNG frames. Look specifically for:
- An on-screen timestamp overlay (the alarm timestamp)
- Alarm status text overlay (e.g., ALARM_RED, ACTIVE, etc.)
The key frame is around the 11-second mark.

**Step 3 — Read device telemetry NDJSON:**
Glob for *.ndjson files in device_telemetry/ and read them. Look for alarm events and timestamps that align with the CCTV evidence.

**Step 4 — Check archive for stale references:**
Read archive/incident_2024-03-07.md. Confirm it is a prior-year CLOSED incident. Do NOT use its data as current facts. Set stale_ref_flag to true since you identified and excluded it.

**Step 5 — Read the earlier evidence:**
Read output/event_evidence.md for the key values already established (firmware 2.18.3, dose error 12.0, bilateral pulmonary edema).

**Step 6 — Read revised RCA template:**
List and read rca_templates/revised_rca_template.docx for any formatting guidance.

**Step 7 — Write the YAML output:**
Write output/rca_findings.yaml with EXACTLY these five fields:

```yaml
firmware_action: "<what firmware action is required per the Field Safety Notice>"
root_cause_summary: "<brief description of root cause - do NOT say nurse misprogramming, that is a known transcript error>"
alarm_confirmed_at: "<the confirmed alarm timestamp from CCTV frames, e.g. 2026-06-14T23:48:07>"
imaging_finding: "<X-ray conclusion: bilateral pulmonary edema>"
stale_ref_flag: true
```

Important constraints:
- Do NOT use values from ai_summaries/ — those are unverified (no EVT-9X0042, 6.0 mg/h, Dr. Amelia Voss, or firmware 2.19.0)
- The auto-transcript's "nurse misprogramming" root cause is WRONG — use the WAV recording as authoritative
- alarm_confirmed_at must come from the CCTV visual frames
- stale_ref_flag must be true (you identified and excluded the 2024 archive incident)
- firmware_action comes from the Field Safety Notice v2
`, { agentType: "rca-synthesis-agent" });

return result;