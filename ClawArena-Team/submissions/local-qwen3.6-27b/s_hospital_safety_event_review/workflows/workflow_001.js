// Split VLM image analysis into parallel focused tasks

defineAgent({
  name: 'image-reader',
  model_key: 'vlm',
  tools: ['Read', 'Glob'],
  accessible_paths: [
    '/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/output',
    '/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/corridor_cctv'
  ],
  system_prompt: 'You are a vision-language agent. Read PNG images and report ALL text visible in them. Be precise with numbers, dates, and clinical terminology.'
});

// Task 1: Read X-ray report annotated
// Task 2: Read DICOM screenshot 01
// Task 3: Read DICOM screenshot 02
// Task 4: Read DICOM screenshot 03
// Task 5: Read CCTV frames
// Task 6: Read FSN HTML

const results = await parallel([
  () => agent('Read the image at /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/output/xray_report_annotated.png. Report ALL text visible in this annotated X-ray report. What is the clinical finding/conclusion?', { agentType: 'image-reader' }),
  () => agent('Read the image at /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/output/dicom_screenshot_01.png. Report ALL text visible on this pump LCD screenshot. Look for firmware version, dose values, alarm status.', { agentType: 'image-reader' }),
  () => agent('Read the image at /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/output/dicom_screenshot_02.png. Report ALL text visible on this pump LCD screenshot. Look for firmware version, dose values, alarm status.', { agentType: 'image-reader' }),
  () => agent('Read the image at /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/output/dicom_screenshot_03.png. Report ALL text visible on this pump LCD screenshot. Look for firmware version, dose values, alarm status.', { agentType: 'image-reader' }),
  () => agent('List files in /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/corridor_cctv/frames/ using Glob. Then read the PNG that has the earliest timestamp showing alarm status. Report all text overlays visible including timestamps and alarm status. Also read /playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_local2_2780990/run_1780830995_516fc2/s_hospital_safety_event_review/work/corridor_cctv/_index.md.', { agentType: 'image-reader' }),
]);

return {
  xray_annotated: results[0],
  screenshot_01: results[1],
  screenshot_02: results[2],
  screenshot_03: results[3],
  cctv: results[4]
};