defineAgent({ name: 'mi-scanner', model_key: 'llm', tools: ['Glob', 'Read'], accessible_paths: ['/playpen2/xkaiwen/smbench_results/exp/local-qwen3.6-27b/run_1780730698_cf3182/s_product_launch_warroom/work/market_intel'], system_prompt: 'You scan market intelligence files. Use Glob to find all .md files, then Read each one. Extract competitor name, Last updated date, and differentiator from each file. Return structured data.' });

const step1 = await agent('Use Glob pattern "*.md" to find all markdown files in the market_intel directory. List every filename you find.', { agentType: 'mi-scanner' });

return step1;