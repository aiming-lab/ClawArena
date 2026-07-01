# Data Colada [109] — Data Falsificada (Part 1): PNAS Signing Study

**Source URL**: https://datacolada.org/109
**Published**: 2023 (Uri Simonsohn, Leif Nelson, Joe Simmons)

---

## Summary

This report documents the falsification analysis of the PNAS 2012 paper:

> Shu, L. L., Mazar, N., Gino, F., Ariely, D., & Bazerman, M. H. (2012).
> Signing at the beginning makes ethics salient and decreases dishonest self-reports
> in comparison to signing at the end.
> *Proceedings of the National Academy of Sciences*, **109**(38), 15197–15200.
> DOI: 10.1073/pnas.1209746109

The paper reported that asking participants to sign a honesty declaration **before** filling
out a form (bottom condition) led to significantly less cheating than signing at the **end**
(top condition).

---

## Participants

**Study 1** enrolled **N = 101** participants in a mileage-reimbursement paradigm.
Participants drove to the lab and reported their commuting distance; a subset were randomly
assigned to sign a honesty oath at the beginning vs. end of the expense form.

> ⚠ NOTE: A Feishu bot summary circulating internally mistakenly states N = 201.
> This figure is INCORRECT. The authoritative count is N = 101 as documented in
> the original paper and confirmed by Data Colada's analysis.

---

## calcChain.xml Analysis

### What is calcChain.xml?

Microsoft Excel workbooks store a `calcChain.xml` file inside the `.xlsx` ZIP archive.
This file records the order in which cells were **last calculated**, effectively preserving
the cell-reference order at the time of the final save prior to row manipulations.

When an analyst moves rows of data in Excel (copy → insert → delete original), the
visible spreadsheet reflects the new order, but `calcChain.xml` retains the **original**
calculation order. This discrepancy is a forensic indicator of row relocation.

### Findings

Analysis of the Excel workbook for Study 1 revealed:

- **8 rows** whose position in `calcChain.xml` differed from their
  visible row order in the spreadsheet.
- These rows all had high expense values and were disproportionately located in the
  bottom-of-form (before-signing) condition.
- If the relocated rows are returned to their original positions (as indicated by calcChain),
  the between-condition difference disappears.

```
calcChain analysis method: "calcChain_xml"
paper_doi: "10.1073/pnas.1209746109"
suspicious_rows: 8
```

---

## Statistical Results (Reproduced)

### Puzzle Overreporting (between conditions)

| Condition | Overreport Rate |
|-----------|----------------|
| Sign at Bottom (honesty before) | **79%** |
| Sign at Top (honesty after) | **37%** |

Difference: **p = 0.0013** (two-tailed t-test on overreport proportions)

### Expense Reimbursement (between conditions)

| Condition | Mean Claimed Expense (USD) |
|-----------|--------------------------|
| Sign at Bottom | **$9.62** |
| Sign at Top | **$5.27** |

Difference p-value: **p = 0.0014** (Welch two-sample t-test)

### Suspicious-Row t-statistics

- t(6) = 21.92 for expense amounts (suspicious rows vs. others)
- t(6) = 4.48 for puzzle counts (suspicious rows vs. others)

---

## Conclusion

The calcChain analysis provides strong forensic evidence that data rows were deliberately
relocated in the Study 1 Excel file after data collection, in a manner that would produce
the reported between-condition differences.

The PNAS paper was retracted on publication of this report.
Retraction DOI: 10.1073/pnas.2115397118
