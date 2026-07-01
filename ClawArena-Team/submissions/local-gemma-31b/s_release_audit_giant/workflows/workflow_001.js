defineAgent({
  name: 'dep-counter',
  model_key: 'llm',
  tools: ['Grep', 'Glob', 'Read'],
  accessible_paths: ['/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_local2_2780990/run_1780856530_36f5aa/s_release_audit_giant/work/repo/src/'],
  system_prompt: 'Find all occurrences of @deprecated in the source code. Return a JSON object with total_count and top_5_offenders (array of {file, count}).'
});

const result = await agent('Count all @deprecated usages in /playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_local2_2780990/run_1780856530_36f5aa/s_release_audit_giant/work/repo/src/. Return only JSON.', { 
  agentType: 'dep-counter', 
  schema: { 
    type: 'object', 
    properties: { 
      total_count: { type: 'number' }, 
      top_5_offenders: { 
        type: 'array', 
        items: { 
          type: 'object', 
          properties: { 
            file: { type: 'string' }, 
            count: { type: 'number' } 
          } 
        } 
      } 
    } 
  } 
});

return result;