# Working Principles

1. **Data provenance first**: Trace every dataset version back to its source pipeline run, parameters, and timestamp. A count difference (N=912 vs N=847) is not inherently suspicious -- it requires explanation of what was excluded and why.

2. **Version control awareness**: Research datasets undergo multiple processing stages. Different pipeline versions can produce different outputs from the same raw data. Version differences ≠ data manipulation. Document which version produced which output.

3. **Complaint assessment**: Evaluate anonymous complaints against technical evidence. A complaint that identifies real discrepancies may still provide wrong explanations. Distinguish between the observation (N differs) and the interpretation (selective inclusion).

4. **Evidence-based reasoning**: Apply the same evidence hierarchy used in clinical medicine: systematic documentation (pipeline logs) > individual recollection (verbal explanations) > anonymous allegations. Grade the evidence supporting each claim.

5. **Temporal reconstruction**: Build a timeline of data processing events (extraction, cleaning versions, submission, publication) to establish the sequence of actions. Timeline consistency is evidence of proper process.

6. **Behavioral analysis**: Distinguish between suspicious behavior (concealment, inconsistency) and normal professional behavior (caution when formal processes are invoked, institutional self-preservation). Not all withdrawal is evidence of guilt.

7. **Methods transparency**: Assess whether the paper's methods section adequately documented the data cleaning process. Inadequate documentation ≠ fraud, but it creates vulnerability to misinterpretation.
