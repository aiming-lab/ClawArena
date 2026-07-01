
  const DEVOPS_NOTE = `/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_codebase_migration_review/work/briefs/devops_note.md`;
  const SQL_0042 = `/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_codebase_migration_review/work/legacy/migrations/0042_pii_columns.sql`;
  const SQL_0043 = `/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_codebase_migration_review/work/legacy/migrations/0043_split_safety.sql`;

  defineAgent({ 
    name: 'security-analyst', 
    model_key: 'llm', 
    tools: ['Read'], 
    accessible_paths: ['/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_codebase_migration_review/work/legacy', '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_codebase_migration_review/work/briefs'], 
    system_prompt: 'You are a security specialist analyzing SQL migrations for PII leaks and safety. Compare migration files and evaluate if security patches adequately address the identified risks.' 
  });

  const analysis = await agent(`
    Please analyze the relationship between two SQL migrations:
    1. ${SQL_0042} (The PII-risk migration)
    2. ${SQL_0043} (The safety patch)
    
    Also consider the context in ${DEVOPS_NOTE}.
    
    Provide a detailed evaluation of:
    - How 0043 relates to 0042.
    - Whether 0043 adequately addresses the PII risks (specifically regarding audit logging and row-level security mentioned in the DevOps note).
    - Any remaining gaps or risks.
  `, { agentType: 'security-analyst' });

  return analysis;
