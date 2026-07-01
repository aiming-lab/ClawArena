
  defineAgent({ 
    name: 'site-counter', 
    model_key: 'llm', 
    tools: ['Read'], 
    accessible_paths: ['/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_clinical_trial_audit/work/edc_export'], 
    system_prompt: 'Read the provided CSV file. Count how many rows have Grade 3. Return ONLY the number.' 
  });

  const sites = ['01', '02', '03', '04', '05'];
  const edcCounts = await parallel(sites.map(site => async () => {
    const filePath = `/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_clinical_trial_audit/work/edc_export/site_${site}.csv`;
    const res = await agent(`Count Grade 3 SAEs in ${filePath}`, { agentType: 'site-counter' });
    return { site, count: parseInt(res) || 0 };
  }));

  return edcCounts;
