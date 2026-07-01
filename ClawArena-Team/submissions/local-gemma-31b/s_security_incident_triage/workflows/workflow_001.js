
  const IDS_PATH = '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_security_incident_triage/work/ids_logs';
  const FW_PATH = '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_security_incident_triage/work/firewall';
  const AUTH_PATH = '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_security_incident_triage/work/auth_audit';
  const AUDIT_PATH = '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_security_incident_triage/work/audit';

  defineAgent({ 
    name: 'ids_sub', 
    model_key: 'llm', 
    tools: ['Read', 'Glob', 'Write'], 
    accessible_paths: [IDS_PATH, AUDIT_PATH], 
    system_prompt: 'Read ids_logs/ and write a summary of INC-2026-0514-A findings to audit/partial_ids.md' 
  });
  defineAgent({ 
    name: 'fw_sub', 
    model_key: 'llm', 
    tools: ['Read', 'Glob', 'Write'], 
    accessible_paths: [FW_PATH, AUDIT_PATH], 
    system_prompt: 'Read firewall/ and write pending containment rule details to audit/partial_fw.md' 
  });
  defineAgent({ 
    name: 'auth_sub', 
    model_key: 'llm', 
    tools: ['Read', 'Glob', 'Write'], 
    accessible_paths: [AUTH_PATH, AUDIT_PATH], 
    system_prompt: 'Read auth_audit/ and write token revocation and credential rotation requirements to audit/partial_auth.md' 
  });

  await parallel([
    () => agent('Process IDS logs and write to audit/partial_ids.md', { agentType: 'ids_sub' }),
    () => agent('Process Firewall config and write to audit/partial_fw.md', { agentType: 'fw_sub' }),
    () => agent('Process Auth audit and write to audit/partial_auth.md', { agentType: 'auth_sub' }),
  ]);

  return 'Audit agents completed';
