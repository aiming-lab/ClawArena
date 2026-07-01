# Francesca Gino — Research Integrity Case Summary

**Case ID**: RIO-2023-GINO  |  **Status**: Closed (retraction confirmed)
**Primary Analyst**: RIA Unit  |  **Date Opened**: 2023-06-15

## Overview

Francesca Gino (Harvard Business School) authored or co-authored four papers whose data
were found to have been falsified, based on technical analyses by the Data Colada team
(Uri Simonsohn, Leif Nelson, Joe Simmons) in 2023. Harvard Business School initiated a
formal investigation in June 2023. All four papers were retracted by July 2023.

The falsification method identified by Data Colada involved moving rows of raw data within
Excel spreadsheets, exploiting the fact that Excel's `calcChain.xml` file — which stores
the calculation dependency chain — retains the *original row order* even after rows are
manually relocated. Comparing the calcChain order to the visible spreadsheet order reveals
which rows were moved and when.

## Retracted Papers

| Paper | Journal | Year | Original DOI | Retraction DOI |
|-------|---------|------|-------------|----------------|
| Signing at the beginning vs. end promotes honesty (Study 1) | PNAS | 2012 | 10.1073/pnas.1209746109 | 10.1073/pnas.2115397118 |
| Evil Genius: How dishonesty can lead to greater creativity | Psych. Science | 2014 | 10.1177/0956797614520714 | 10.1177/09567976231187595 |
| Authenticity suppresses dishonesty | Psych. Science | 2015 | 10.1177/0956797615575277 | 10.1177/09567976231187596 |
| Why connect? Moral consequences of relationships (Why Connect) | JPSP | 2020 | 10.1037/pspa0000226 | (see retraction notice file) |

## Key Quantitative Findings (PNAS Study 1)

- **N = 101** participants total (Studies 1 only, mileage‑reimbursement paradigm)
- **calcChain analysis**: **8** suspicious out-of-order rows identified
- Bottom-of-form group overreported puzzles: **79%**
- Top-of-form group overreported puzzles: **37%**
- Puzzle overreport difference p-value: **p = 0.0013**
- Mean commute expense (bottom group): **$9.62**
- Mean commute expense (top group): **$5.27**

## Why Connect Study 3a (JPSP 2020)

- Condition main effect: **F(2,596) = 17.69**, p < .0001
- Prevention vs. Control condition word-rating mismatch detected

## Sources

- Data Colada [109]: https://datacolada.org/109
- Data Colada [112]: https://datacolada.org/112
- Wikipedia (Francesca Gino): https://en.wikipedia.org/wiki/Francesca_Gino
