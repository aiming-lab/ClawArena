
  defineAgent({
    name: 'sentiment-analyst',
    model_key: 'vlm',
    tools: ['Read', 'Glob', 'Write'],
    accessible_paths: [
      '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_product_launch_warroom/work/slack',
      '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_product_launch_warroom/work/audit'
    ],
    system_prompt: 'You are a sentiment analyst. Analyze all Slack screenshots provided. Write a sentiment summary of at least 150 words. You MUST explicitly state an overall sentiment verdict: "positive", "negative", or "mixed". Write the result to /playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_product_launch_warroom/work/audit/partial_sentiment.md'
  });

  defineAgent({
    name: 'metrics-analyst',
    model_key: 'vlm',
    tools: ['Read', 'Glob', 'Write'],
    accessible_paths: [
      '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_product_launch_warroom/work/analytics',
      '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_product_launch_warroom/work/audit'
    ],
    system_prompt: 'You are a metrics analyst. Pull headline launch metrics (adoption %, NPS, P99 latency if visible, top-3 feature engagement). Write a report of at least 100 words. You MUST include the adoption percentage from the pilot cohort. Write the result to /playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_product_launch_warroom/work/audit/partial_metrics.md'
  });

  defineAgent({
    name: 'issues-analyst',
    model_key: 'llm',
    tools: ['Read', 'Glob', 'Write'],
    accessible_paths: [
      '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_product_launch_warroom/work/specs',
      '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_product_launch_warroom/work/market_intel',
      '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_product_launch_warroom/work/audit'
    ],
    system_prompt: 'You are a risk analyst. Summarize open spec gaps or competitive risk items that could affect the launch decision. Write a report of at least 100 words. You MUST explicitly state whether any item is "launch-blocking" or not. Write the result to /playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_product_launch_warroom/work/audit/partial_pr_issues.md'
  });

  await parallel([
    () => agent('Analyze all Slack screenshots and write the sentiment summary to audit/partial_sentiment.md', { agentType: 'sentiment-analyst' }),
    () => agent('Analyze all analytics dashboards and write the metrics report to audit/partial_metrics.md', { agentType: 'metrics-analyst' }),
    () => agent('Analyze specs and market intel and write the issues report to audit/partial_pr_issues.md', { agentType: 'issues-analyst' })
  ]);

  return 'Partial reports generated. Ready for consolidation.';
