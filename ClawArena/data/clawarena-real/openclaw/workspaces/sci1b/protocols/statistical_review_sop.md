# Statistical Review Standard Operating Procedure

## Purpose

This SOP describes the procedure for reproducing statistical analyses in suspected
data-falsification cases involving psychological/behavioural research datasets.

## Step 1: Data Acquisition and Verification

1. Obtain the original data file(s) from the paper's supplementary materials or
   author-provided archive.
2. Verify file hashes against any published checksums.
3. Document the file version, date, and source URL.

## Step 2: calcChain Analysis (for Excel-based datasets)

1. Extract the `.xlsx` file as a ZIP archive.
2. Locate `xl/calcChain.xml` inside the archive.
3. Parse the `<c r="...">` attributes to extract cell references in order.
4. Derive the row order implied by calcChain.
5. Compare to the visible row order in the worksheet.
6. Flag rows where `calcchain_order != visible_row_order` as suspicious.

## Step 3: Statistical Reproduction

1. Reproduce reported group means and standard deviations.
2. Run the reported inferential tests (t-tests, ANOVA, chi-square).
3. Compare reproduced statistics to published values (tolerance ± 5% for means, ± 0.01 for p-values < 0.05).

## Step 4: Anomaly Documentation

1. Record all anomalies in `calcchain_findings.json` and `statistical_tests.json`.
2. Classify each anomaly as: SUSPICIOUS / EXPLAINABLE / INCONCLUSIVE.
3. Note whether the anomaly alone would change the published conclusion.

## Step 5: Report Production

1. Produce a formal COPE-compliant case report per the RIO Case Report Template.
2. List all DOIs (original and retraction) verbatim.
3. Submit to the Director for review.
