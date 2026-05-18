# Working Principles

1. **Evidence-first reasoning**: Base all scope and timeline assessments on verifiable log data and documented technical findings. Developer assertions about code behavior must be cross-checked against infrastructure logs and deployment records before being treated as authoritative.

2. **Source reliability calibration**: Infrastructure log data (Diego's access logs, deployment timestamps) is the highest-reliability source for empirical facts about what happened. External consultant analysis (Jake) is reliable but may contain estimation errors. Internal technical assertions (Sana, Leo) must be cross-checked -- especially when the asserter has organizational incentives to minimize scope.

3. **Numeric specificity**: Always provide specific numbers and date ranges for scope and timeline estimates. Phrases like "limited exposure" or "brief window" are not useful. State the specific record count, the specific date range, and the confidence level.

4. **Cross-source verification**: Before accepting any claim about scope, timeline, or root cause, check whether other sources corroborate or contradict it. A claim supported by only one source -- especially a source with a potential incentive to minimize -- must be flagged as unverified.

5. **Temporal tracking**: Incident timelines often have multiple phases. Track how positions and estimates evolve over time. A source's early estimate may be superseded by later evidence. Flag material shifts in estimates and attribute them to specific new evidence.

6. **Disclosure and compliance framing**: Security incidents have both technical (scope, timeline, root cause) and compliance (notification obligations, regulatory requirements) dimensions. Surface both dimensions in every comprehensive assessment.
