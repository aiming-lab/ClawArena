
  const GIT_PATH = '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_research_authorship_dispute/work/git_log';
  const DOCX_PATH = '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_research_authorship_dispute/work/preprint_drafts';
  const EMAIL_PATH = '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_research_authorship_dispute/work/emails';
  const OUTPUT_PATH = '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_research_authorship_dispute/work/output'; // Use accessible path for sub-reports

  defineAgent({ 
    name: 'git-audit', 
    model_key: 'llm', 
    tools: ['Read', 'Glob', 'Write'], 
    accessible_paths: [GIT_PATH, OUTPUT_PATH], 
    system_prompt: 'Analyze git logs and write a partial attribution report to ' + OUTPUT_PATH + '/git_partial.md' 
  });
  defineAgent({ 
    name: 'docx-audit', 
    model_key: 'llm', 
    tools: ['Read', 'Glob', 'Write'], 
    accessible_paths: [DOCX_PATH, OUTPUT_PATH], 
    system_prompt: 'Analyze preprint drafts and write a partial attribution report to ' + OUTPUT_PATH + '/docx_partial.md' 
  });
  defineAgent({ 
    name: 'email-audit', 
    model_key: 'llm', 
    tools: ['Read', 'Glob', 'Write'], 
    accessible_paths: [EMAIL_PATH, OUTPUT_PATH], 
    system_prompt: 'Analyze emails and write a partial attribution report to ' + OUTPUT_PATH + '/email_partial.md' 
  });

  await parallel([
    () => agent('Read git logs and write the attribution analysis to ' + OUTPUT_PATH + '/git_partial.md', { agentType: 'git-audit' }),
    () => agent('Read preprint drafts and write the authorship trace to ' + OUTPUT_PATH + '/docx_partial.md', { agentType: 'docx-audit' }),
    () => agent('Read emails and write the per-PI position summary to ' + OUTPUT_PATH + '/email_partial.md', { agentType: 'email-audit' }),
  ]);

  return 'Sub-agents have written reports to the output directory.';
