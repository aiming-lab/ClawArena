defineAgent({
  name: 'lint-agent',
  model_key: 'llm',
  tools: ['Bash'],
  accessible_paths: ['/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_local2_2780990/run_1780856530_36f5aa/s_release_audit_giant/work/tools', '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_local2_2780990/run_1780856530_36f5aa/s_release_audit_giant/work/repo'],
  system_prompt: 'Execute the release lint script and return the output.'
});

defineAgent({
  name: 'risk-synthesizer',
  model_key: 'llm',
  tools: ['Read', 'Write'],
  accessible_paths: [
    '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_local2_2780990/run_1780856530_36f5aa/s_release_audit_giant/work/output',
    '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_local2_2780990/run_1780856530_36f5aa/s_release_audit_giant/work/analysis'
  ],
  system_prompt: 'You are a risk assessment specialist. Your task is to synthesize a consolidated risk summary based on previous audit notes. You must cite specific files from the output/notes directory. Save the final report to analysis/risk_summary.md.'
});

phase('Initiating Parallel Deployment De-risking');

// Start linting in background (the agent call itself is the execution)
const lintPromise = agent('Run the lint script: /playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_local2_2780990/run_1780856530_36f5aa/s_release_audit_giant/work/tools/lint_release.sh. Return the output.', { agentType: 'lint-agent' });

// Simultaneously synthesize risk summary
const riskPromise = agent('Read all files in /playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_local2_2780990/run_1780856530_36f5aa/s_release_audit_giant/work/output/notes/ and /playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_local2_2780990/run_1780856530_36f5aa/s_release_audit_giant/work/output/release_summary.json. Draft a consolidated risk summary at /playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_local2_2780990/run_1780856530_36f5aa/s_release_audit_giant/work/analysis/risk_summary.md. Ensure you cite previous notes (e.g., output/notes/q2_security.md).', { agentType: 'risk-synthesizer' });

const [lintResult, riskResult] = await parallel([() => lintPromise, () => riskPromise]);

return {
  lint_output: lintResult,
  risk_summary_status: riskResult
};
