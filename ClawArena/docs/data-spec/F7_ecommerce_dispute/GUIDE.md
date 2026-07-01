# trace_f7 -- E-commerce Dispute (618 GPU Substitution): Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_f7`

**Scenario:** 赵磊 (independent quant trader, Shanghai) ordered an NVIDIA A100 80GB GPU (¥72,999) during the 618 shopping festival on JD.com. He received an A40 48GB GPU (~¥32,000) three times in a row. Order records show A100, logistics labels say "NVIDIA 专业显卡" (deliberately vague), and the courier's internal system confirms A40 for all shipments. Customer service claimed "authorized replacement" but the order system has only one RMA record. The product page still shows A100 "in stock" despite the courier confirming zero A100 inventory. The seller later cited a non-existent "supplementary terms clause" allowing substitution.

**Core evaluation goals:**
1. Can the agent cross-reference order records (A100) with logistics tracking (A40) and payment records (partial refund at A40 price) to identify systemic product substitution? (MS)
2. Can the agent integrate new evidence (third wrong item, payment manipulation, courier screenshots, fake terms) and revise prior assessments? (DU)
3. Does the agent maintain 赵磊's preferred format (code/table output, timestamp naming, evidence-first, quantitative, terse) after calibration? (P)
4. Can the agent synthesize product, logistics, payment, and legal evidence to produce a comprehensive consumer fraud assessment? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_f7/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_f7/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_f7/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_f7/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (W1--W2), 4 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T6), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 5 initial scenario files + 4 update-added files, timing table, noise design, token estimates | 2 |
| `layer2-sessions.md` | All 4 sessions: main session + 3 history sessions (~34 total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops | 3 |
| `layer3-eval.md` | 30 eval rounds (r1--r30): option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| 客服小刘 | Customer Service Rep | Online CS IM | `zhaolei_kefu_im_{uuid}.jsonl` | `PLACEHOLDER_KEFU_IM_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| 快递小哥张师傅 | Courier | SMS | `zhaolei_courier_sms_{uuid}.jsonl` | `PLACEHOLDER_COURIER_SMS_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| #购物群 | Group: 赵磊, 老韩, others | WeChat Group | `shopping_group_{uuid}.jsonl` | `PLACEHOLDER_SHOPPING_GROUP_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |

---

## 4. Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Order A100 (order system) vs shipped A40 (logistics + courier internal system) | R1 (partial -- order/tracking visible) | R2->R5 (three-time pattern); R2->R9 (courier definitive) |
| C2 | CS says "authorized replacement" (IM) vs only one RMA in system + partial refund at A40 price (payment) | R2 (partial -- IM + order records) | R3->R7 (payment manipulation confirms no real authorization) |
| C3 | Payment/order/logistics timeline: all consistent (NON-CONFLICT) | R1 (persistent synthesis) | None |
| C4 | Product page "in stock" vs courier "no A100 inventory" vs seller cites non-existent terms | R4 (partial -- screenshot visible) | R4->R8 (courier confirms); R4->R11 (seller's fake terms exposed) |
| B1 | #购物群 Loop 6: Agent normalizes as "618 logistics error" | R5 (corrected by third wrong item + stock page) | Explicit correction in group Phase 2 append |
| B2 | 客服 IM Loop 7: Agent accepts CS "authorized replacement" claim | R7 (corrected by payment manipulation evidence) | Explicit correction after Update 2 |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design
Read all 5 layer files. Generate 4 UUIDs (one per session): MAIN, KEFU_IM, COURIER_SMS, SHOPPING_GROUP.

### Step 1: Create Workspace Files (layer1)
Target directory: `benchmark/data/calmb-new/workspaces/trace_f7/`

### Step 2: Write History Sessions (layer2)
Write 3 history session files + main. B1 exact phrase in shopping_group Loop 6. B2 exact phrase in kefu_im Loop 7.

### Step 3: Write Questions File (layer3)
Write 30 rounds with exec_check at 30%.

### Step 4: Write Update Source Files (layer4)
Write 4 update action sets.

### Step 5: Runtime Checks
- [ ] B1 and B2 phrases verbatim in specified loops
- [ ] C1-C4 sources independent
- [ ] C3 no contradictions
- [ ] All financial figures consistent
- [ ] All dates consistent
- [ ] exec_check = 30% of rounds
