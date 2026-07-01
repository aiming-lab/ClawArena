
  defineAgent({ 
    name: 'metrics-puller', 
    model_key: 'vlm', 
    tools: ['Read', 'Glob', 'Write'], 
    accessible_paths: [
      '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_incident_postmortem/work/figures',
      '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_incident_postmortem/work/logs',
      '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_incident_postmortem/work/output'
    ], 
    system_prompt: 'You are a metrics analyst. Read p99_time_series.png and logs to extract peak p99 value, time of peak, and recovery timestamp. Write the result to output/metrics_pull_result.md.' 
  });

  defineAgent({ 
    name: 'synthesizer', 
    model_key: 'llm', 
    tools: ['Read', 'Write'], 
    accessible_paths: [
      '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_incident_postmortem/work/output'
    ], 
    system_prompt: 'You are a technical writer. Synthesize multiple incident notes into a final executive summary.' 
  });

  // (a) Background metrics pull (simulated by agent call)
  // We use a separate promise for this to emulate backgrounding, 
  // but the workflow harness will execute it. 
  // Note: agent() calls in workflow are typically foreground unless handled.
  // However, the prompt asks to orchestrate both.
  
  const metricsPromise = agent(`
    Read the file /playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_incident_postmortem/work/figures/p99_time_series.png and the logs in /playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_incident_postmortem/work/logs/.
    Extract:
    - Peak p99 value
    - Time of peak
    - Recovery timestamp
    Write these findings to /playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_incident_postmortem/work/output/metrics_pull_result.md.
  `, { agentType: 'metrics-puller' });

  // (b) Main-thread synthesis
  const synthesisResult = await agent(`
    Gather findings from the following files:
    - output/notes/q1_scope.md
    - output/notes/q2_first_error.md
    - output/notes/q3_dashboard.md
    - output/notes/q4_comms_vs_data.md
    - output/rca_summary.json
    
    Synthesize them into a single executive summary and write it to /playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_incident_postmortem/work/output/postmortem_final.md.
    
    The summary MUST:
    1. Explicitly reference all five files.
    2. State the confirmed root cause (migration v23_unbatched_shipments_update.py causing a deadlock on orders.shipments).
    3. Include the impact numbers: duration (23 min), users (4500), revenue ($87,000).
    4. Include a one-paragraph 'lessons learned' section regarding unbatched migrations and misleading initial signals.
  `, { agentType: 'synthesizer' });

  await metricsPromise;
  return { synthesis: synthesisResult };
