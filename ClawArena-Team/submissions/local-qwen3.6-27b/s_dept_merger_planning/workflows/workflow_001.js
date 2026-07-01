// Read both HR exports and staffing analysis guides, then consolidate the roster.

defineAgent({
  name: 'hr_reader',
  model_key: 'llm',
  tools: ['Read', 'Glob'],
  accessible_paths: [
    '/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_dept_merger_planning/work/hr_data',
    '/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_dept_merger_planning/work/staffing_analysis'
  ],
  system_prompt: 'You read CSV and markdown files from the hr_data and staffing_analysis directories. Return exact file contents as requested. For CSVs, return the full content verbatim. For markdown, return the full content verbatim.'
});

const path_root = '/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_resume_2246329/run_1780816418_633326/s_dept_merger_planning/work';

// Step 1: Discover files
phase('Discovering HR data and staffing analysis files');

const discoverResult = await agent(`
List every file in both directories:
1. ${path_root}/hr_data/
2. ${path_root}/staffing_analysis/

For each file, report the full path and a one-line description. Return as a structured list.
`, { agentType: 'hr_reader' });

log(discoverResult);

// Step 2: Read all files in parallel
phase('Reading all HR and staffing files');

// Based on what we discover, read all files
const readResult = await agent(`
Here is the file inventory:\n${discoverResult}\n\nNow read EVERY file in both directories and return the COMPLETE content of each file. For each file, use the format:\n\n--- FILE: <full-path> ---\n<full content verbatim>\n\nDo NOT summarize. Return every row of every CSV and every line of every markdown file.
`, { agentType: 'hr_reader' });

log('All files read. Contents returned.');

// Return everything for the next stage
return { discoverResult, readResult };