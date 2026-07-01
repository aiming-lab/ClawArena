# Source Datasets Documentation

## ULB Credit Card Fraud Detection Dataset

- **Source URL**: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- **Academic reference**: Dal Pozzolo et al. (2014) — DOI: 10.1016/j.eswa.2014.02.026
- **Coverage**: September 2013, European cardholders, 2 days
- **Total transactions**: 284,807
- **Fraud transactions** (Class=1): 492
- **Fraud rate**: 0.00172 (0.172%)
- **Features**:
  - V1–V28: PCA-transformed principal components (confidential; original features not disclosed)
  - Time: Seconds elapsed from first transaction in dataset
  - Amount: Transaction amount in EUR
  - Class: Response variable — 0 = normal, 1 = fraud; values: {0, 1}
- **Class imbalance**: Highly imbalanced; fraud represents only 0.172% of all transactions

## PaySim Synthetic Financial Transactions Dataset

- **Source URL**: https://www.kaggle.com/datasets/ealaxi/paysim1
- **GitHub (Lopez-Rojas)**: https://github.com/EdgarLopezPhD/PaySim
- **Simulation**: 744 steps (30 days, 1 step = 1 hour)
- **Total transactions**: 6,362,620
- **Fraud transactions** (isFraud=1): 8,213
- **Fraud rate**: 0.00129 (0.129%)
- **Transaction types**: CASH-IN, CASH-OUT, DEBIT, PAYMENT, TRANSFER
  - Fraud occurs ONLY in CASH-OUT and TRANSFER transactions
- **isFlaggedFraud threshold**: 200,000 (local currency)
  - System auto-flags TRANSFER > 200,000 as isFlaggedFraud=1
- **Fields**: step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig,
  nameDest, oldbalanceDest, newbalanceDest, isFraud, isFlaggedFraud

## Field Notes

All field names above are verbatim from the official dataset documentation.
Use exact names when referencing in outputs and case records.
