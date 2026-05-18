# Layer 5 -- Cross-Layer Consistency Checks

> Validates internal consistency across all layers for trace_j3.

---

## 1. Financial Figure Consistency

| Figure | L0 | L1 | L2 | L3 | L4 | Status |
|---|---|---|---|---|---|---|
| Hotel invoice total | ¥4,800 | hotel-invoice-scan.md | 李姐 Loop 1 | R1 opt A | ✅ | ✅ |
| Room fee (pre-tax) | ¥4,248 | hotel-invoice-scan.md | -- | R1 opt A | ✅ | ✅ |
| VAT (13%) | ¥552 | hotel-invoice-scan.md | -- | R1 opt E | ✅ | ✅ |
| MCN record amount | ¥3,600 | mcn-reimbursement-record.md | 李姐 Loop 2 | R1 opt B | ✅ | ✅ |
| Management fee | ¥360 | mcn-reimbursement-record.md | 李姐 Loop 3 | R1 opt B | ✅ | ✅ |
| Net to 周芳 | ¥3,240 | bank-payment-records.md | 李姐 Loop 16 | R1 opt H | ✅ | ✅ |
| Brand budget (housing) | ¥5,000 | brand-budget-confirmation.md | 张品牌 Loop 2 | R1 opt C | ✅ | ✅ |
| Brand total to MCN | ¥25,000 | brand-budget-confirmation.md | 张品牌 Loop 7 | R6 | ✅ | ✅ |
| MCN retention | ¥1,760 | Derived | -- | R1 opt H | ✅ | ✅ |

---

## 2-7. Standard sections (timestamps, contradiction matrix, bias matrix, preferences, update-round alignment, exec_check)

All consistent. Travel dates 03-10 to 03-14 uniform. C1/C2/C3/C4 traced. B1/B2 placed correctly. P1-P5 applied.
