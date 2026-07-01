
  const results = await parallel(args.csv_files.map(file => async () => {
    return await agent(`Process this order CSV file and return the breakdown by customer: ${file}`, { agentType: 'order-analyzer' });
  }));
  return results;
