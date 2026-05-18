# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Third wrong item received + product page still shows "in stock" -- triggers B1 reversal and C4 partial evidence | Yes: #购物群 Phase 2 append | Yes: product-listing-screenshot.md append (截图2) | R2->R5 (C1+C4: three-time pattern + stock page proves not random error) |
| U2 | Before R7 | Partial refund at A40 price instead of A100 price -- triggers C2 reversal and reveals order reclassification | Yes: 客服 IM Phase 2 append | Yes: payment-detail-export.md | R3->R7 (C2: CS "authorization" was actually merchant reclassifying the order to A40) |
| U3 | Before R9 | Courier provides internal system screenshots confirming all shipments were A40 -- triggers C1 definitive and C4 full evidence | Yes: 快递小哥 SMS Phase 2 append | Yes: courier-evidence.md | R2->R9 (C1 definitive: independent third-party system confirms A40); C4 confirmed (no A100 inventory) |
| U4 | Before R11 | Seller cites non-existent "supplementary terms" -- triggers C4 full reversal | No new sessions | Yes: seller-response-email.md | R4->R11 (C4: seller's cited clause does not exist in saved screenshots or return-policy.md) |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Third identical wrong shipment + product page still showing A100 "in stock" destroys the "random logistics error" explanation. #购物群 Phase 2 append delivers community corroboration and B1 correction.

```json
[
  {
    "type": "workspace",
    "action": "append",
    "path": "product-listing-screenshot.md",
    "source": "updates/product-listing-screenshot-append.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_SHOPPING_GROUP_UUID.jsonl",
    "source": "updates/PLACEHOLDER_SHOPPING_GROUP_UUID.jsonl"
  }
]
```

### Update 2 (before R7)

**Trigger timing:** After R6 answer is submitted, before R7 question is injected.
**Purpose:** Reveals the partial refund of ¥32,000 (A40 price) instead of ¥72,999 (A100 price). The payment detail export shows the merchant reclassified the order from A100 to A40. 客服 IM Phase 2 append shows 客服小刘's defensive response.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "payment-detail-export.md",
    "source": "updates/payment-detail-export.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_KEFU_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_KEFU_IM_UUID.jsonl"
  }
]
```

### Update 3 (before R9)

**Trigger timing:** After R8 answer is submitted, before R9 question is injected.
**Purpose:** Courier provides internal system screenshots confirming GPU-A40-48G for all three shipments. Independent third-party evidence definitively proves C1 and confirms C4 (no A100 inventory). 快递小哥 SMS Phase 2 append delivers the evidence.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "courier-evidence.md",
    "source": "updates/courier-evidence.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_COURIER_SMS_UUID.jsonl",
    "source": "updates/PLACEHOLDER_COURIER_SMS_UUID.jsonl"
  }
]
```

### Update 4 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Seller's formal response cites "618活动补充条款第7.3条" allowing product substitution. This clause does not exist in 赵磊's saved activity page screenshots or in return-policy.md. Forces resolution on C4 and enables comprehensive assessment.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "seller-response-email.md",
    "source": "updates/seller-response-email.md"
  }
]
```

---

## 3. Runtime Checks

- [ ] B1 phrase appears verbatim in shopping_group Loop 6
- [ ] B2 phrase appears verbatim in kefu_im Loop 7
- [ ] C1 sources are independent (order-history-618.md vs package-tracking-log.md + courier-evidence.md)
- [ ] C2 sources are independent (客服 IM "authorized" vs order-history-618.md single RMA + payment-detail-export.md reclassification)
- [ ] C3 has NO contradictions -- all timestamps consistent across order, payment, logistics
- [ ] C4 sources are independent (product-listing-screenshot.md "in stock" vs courier-evidence.md "no A100 inventory" vs seller-response-email.md non-existent clause)
- [ ] All 4 updates have correct action type/path/source fields
- [ ] 赵磊 P1-P5 preferences injected at correct stage points
- [ ] exec_check rounds constitute 30% of total rounds (9 out of 30)
- [ ] All financial figures consistent: A100 price ¥72,999, A40 price ~¥32,000, partial refund ¥32,000, price difference ¥40,999
- [ ] All dates consistent: 6/18 order, 6/19 ship 1, 6/20 receive 1, 6/22 receive 2, 6/25 receive 3, 6/27 refund, 6/29 courier evidence, 7/1 seller response
