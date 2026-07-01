export const meta = { name: "read_grant_flow_diagram" };

defineAgent({
  name: "diagram_reader",
  model_key: "vlm",
  tools: ["Read"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/figures"
  ],
  system_prompt: "You read diagrams and images. Describe what you see in detail."
});

const result = await agent(
  "Read the image at:\n/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/figures/grant_flow_diagram.png\n\nDescribe the full diagram: what entities are shown, how funds flow between them, any labels or annotations. Return a detailed description.",
  { agentType: "diagram_reader" });

return result;