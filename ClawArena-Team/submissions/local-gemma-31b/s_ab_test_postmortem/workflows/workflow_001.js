
  defineAgent({ 
    name: 'analyst', 
    model_key: 'llm', 
    tools: ['Bash'], 
    accessible_paths: ['/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_ab_test_postmortem/work/data/exp_2421'], 
    system_prompt: 'You are a data analyst. Run cross-tab analysis on the provided parquet slice. Use the available tools in /playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_ab_test_postmortem/work/tools if needed, or bash scripts to process parquet data. Return the conversion rates for Treatment A and Treatment B.' 
  });

  const results = await parallel(args.slices.map(slice => async () => {
    return await agent(`Perform cross-tab analysis for slice: ${slice} located at /playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_ab_test_postmortem/work/data/exp_2421/${slice}.parquet`, { agentType: 'analyst' });
  }));
  
  return results;
