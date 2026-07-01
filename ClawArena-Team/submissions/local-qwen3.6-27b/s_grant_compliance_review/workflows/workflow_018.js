export const meta = { name: "read_amendment_and_correspondence" };

defineAgent({
  name: "correspondence_reader",
  model_key: "llm",
  tools: ["Read", "Grep"],
  accessible_paths: [
    "/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/correspondence"
  ],
  system_prompt: "Read grantor correspondence threads and return exact text of amendments and clarifications."
});

const amendment = await agent(
  "Read the file at:\n/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/correspondence/thread_grantor_a_amendment.md\n\nReturn the FULL text of this amendment email, especially the revised Appendix III §3.4. Quote the exact new terms.",
  { agentType: "correspondence_reader" });

const halcyon_thread = await agent(
  "Read the file at:\n/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/correspondence/thread_grantor_a_q1_q2.md\n\nReturn the full text of this correspondence thread with Halcyon Foundation.",
  { agentType: "correspondence_reader" });

const nordic_thread = await agent(
  "Read the file at:\n/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/correspondence/thread_grantor_b_q1_q2.md\n\nReturn the full text of this correspondence thread with Nordic DC.",
  { agentType: "correspondence_reader" });

const opal_thread = await agent(
  "Read the file at:\n/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_grant_compliance_review/work/correspondence/thread_grantor_c_q1_q2.md\n\nReturn the full text of this correspondence thread with Opal City Community Fund.",
  { agentType: "correspondence_reader" });

return {
  amendment: amendment,
  halcyon_thread: halcyon_thread,
  nordic_thread: nordic_thread,
  opal_thread: opal_thread
};