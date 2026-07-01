
  const receiptFiles = [
    'RCP-001.png', 'RCP-002.png', 'RCP-003.png', 'RCP-004.png', 
    'RCP-005.png', 'RCP-006.png', 'RCP-007.png', 'RCP-008.png'
  ];
  
  const receiptPathPrefix = '/playpen2/xkaiwen/smbench_results/exp/local-gemma-31b/run_gemmalane2_3256605/run_1780856529_73f293/s_grant_compliance_review/work/receipts/';
  
  const extractions = await parallel(receiptFiles.map(file => async () => {
    const result = await agent(`Extract details from the receipt image at ${receiptPathPrefix}${file}.`, { agentType: 'receipt-reader' });
    return { file, result };
  }));

  return extractions;
