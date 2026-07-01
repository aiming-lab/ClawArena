defineAgent({
  name: 'sentiment-sub',
  model_key: 'vlm',
  tools: ['Read', 'Glob'],
  accessible_paths: ['/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_product_launch_warroom/work/slack', '/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_product_launch_warroom/work/audit'],
  system_prompt: 'You analyse Slack thread screenshots (PNGs) from a launch warroom channel. Read each PNG carefully and extract: what people are saying, sentiment tone, any specific concerns or praise. Write a sentiment summary of at least 150 words to audit/partial_sentiment.md. The summary MUST state the overall sentiment verdict clearly: positive, negative, or mixed.'
});

defineAgent({
  name: 'metrics-sub',
  model_key: 'vlm',
  tools: ['Read', 'Glob'],
  accessible_paths: ['/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_product_launch_warroom/work/analytics', '/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_product_launch_warroom/work/audit'],
  system_prompt: 'You analyse analytics dashboard PNGs. Read every PNG in the analytics directory. Extract: headline adoption percentage, NPS score, P99 latency (if visible), top-3 feature engagement metrics. Write these to audit/partial_metrics.md in at least 100 words. You MUST include the adoption percentage from the pilot cohort.'
});

defineAgent({
  name: 'issues-sub',
  model_key: 'llm',
  tools: ['Read', 'Glob'],
  accessible_paths: ['/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_product_launch_warroom/work/specs', '/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_product_launch_warroom/work/market_intel', '/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_product_launch_warroom/work/audit'],
  system_prompt: 'You review spec files and market intelligence for open issues and competitive risks. Read specs/_index.md, market_intel/_index.md (and any addendum), and scan spec files for open gaps or TBD items. Summarise any open spec gaps or competitive risks that could affect the launch. Write to audit/partial_pr_issues.md in at least 100 words. You MUST state whether any item is launch-blocking.'
});

defineAgent({
  name: 'consolidator',
  model_key: 'llm',
  tools: ['Read', 'Write'],
  accessible_paths: ['/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_product_launch_warroom/work/audit'],
  system_prompt: 'You consolidate partial reports into a launch decision JSON. Read all three partial reports from audit/, then decide go/no_go/delay based on the evidence. Write audit/launch_decision.json with: decision (go/no_go/delay), rationale (>=80 words), and sources (list of three partial filenames).'
});

phase('Phase 1: Run 3 parallel subagents');

const results = await parallel([
  () => agent(
    'Step 1: Glob for all PNG files in the slack directory. Step 2: Read each PNG screenshot carefully — extract the conversation content, who said what, sentiment indicators. Step 3: Write audit/partial_sentiment.md with a sentiment summary of at least 150 words. You MUST state the overall verdict: positive, negative, or mixed. Include specific details from each screenshot.',
    { agentType: 'sentiment-sub' }
  ),
  () => agent(
    'Step 1: Glob for all PNG files in the analytics directory. Step 2: Read every PNG dashboard — extract adoption percentage, NPS, P99 latency, feature engagement top-3. Step 3: Write audit/partial_metrics.md with at least 100 words. You MUST include the adoption percentage from the pilot cohort (98% day-30 adoption).',
    { agentType: 'metrics-sub' }
  ),
  () => agent(
    'Step 1: Glob for all .md files in specs/ and market_intel/. Step 2: Read specs/_index.md and market_intel/_index.md (and _index_addendum.md if it exists). Step 3: Scan spec files for open gaps, TBDs, or unresolved items. Step 4: Summarise any open spec gaps or competitive risks. Write audit/partial_pr_issues.md with at least 100 words. You MUST state whether any item is launch-blocking.',
    { agentType: 'issues-sub' }
  )
]);

phase('Phase 2: Consolidate into launch decision');

const consolidate = await agent(
  'Read audit/partial_sentiment.md, audit/partial_metrics.md, and audit/partial_pr_issues.md. Then decide go/no_go/delay based on the combined evidence. Write audit/launch_decision.json with exactly these fields: "decision" (one of "go", "no_go", "delay"), "rationale" (string, >=80 words), "sources" (array of the three partial filenames). Write the file directly.',
  { agentType: 'consolidator' }
);

return { results: results.map(r => r ? 'completed' : 'failed'), consolidate };