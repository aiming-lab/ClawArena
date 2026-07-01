
  const GIT_PATH = '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_research_authorship_dispute/work/git_log';
  const DOCX_PATH = '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_research_authorship_dispute/work/preprint_drafts';
  const EMAIL_PATH = '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_research_authorship_dispute/work/emails';
  const AUDIT_PATH = '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_research_authorship_dispute/work/audit';

  defineAgent({ 
    name: 'git-audit', 
    model_key: 'llm', 
    tools: ['Read', 'Glob', 'Write'], 
    accessible_paths: [GIT_PATH, AUDIT_PATH], 
    system_prompt: 'Analyze git logs and write a partial attribution report to ' + AUDIT_PATH + '/git_partial.md' 
  });
  defineAgent({ 
    name: 'docx-audit', 
    model_key: 'llm', 
    tools: ['Read', 'Glob', 'Write'], 
    accessible_paths: [DOCX_PATH, AUDIT_PATH], 
    system_prompt: 'Analyze preprint drafts and write an authorship trace to ' + AUDIT_PATH + '/docx_partial.md' 
  });
  defineAgent({ 
    name: 'email-audit', 
    model_key: 'llm', 
    tools: ['Read', 'Glob', 'Write'], 
    accessible_paths: [EMAIL_PATH, AUDIT_PATH], 
    system_prompt: 'Analyze emails and write a per-PI position summary to ' + AUDIT_PATH + '/email_partial.md' 
  });

  await parallel([
    () => agent('Read git logs and write the attribution analysis to ' + AUDIT_PATH + '/git_partial.md', { agentType: 'git-audit' }),
    () => agent('Read preprint drafts and write the authorship trace to ' + AUDIT_PATH + '/docx_partial.md', { agentType: 'docx-audit' }),
    () => agent('Read emails and write the per-PI position summary to ' + AUDIT_PATH + '/email_partial.md', { agentType: 'email-audit' }),
  ]);

  return 'Audit partials generated in /audit/';
