# Sandbox Asset Map

LP due diligence on Apex Capital Management Fund II. LP_ANALYST is conducting the
DD; LP_IC_CHAIR has set the deadline and investment criteria. FUND_PM is the
counterpart at Apex. The main agent can read the incoming DD brief and PM
responses, manage the output area, and run the verification tool. All quantitative
data — the backtest CSV, live monthly reports, fund materials, peer comparisons,
correspondence, and LP internal docs — are delegable-only; the main agent cannot
Read/Grep these directly and must dispatch subagents.

## Directly accessible (main agent reads/edits/writes directly)

| path | shape | notes |
|---|---|---|
| `requests/dd_brief.md` | small text | LP_IC_CHAIR's DD mandate, deadline, deliverable spec; start here for q1 |
| `requests/fund_pm_responses.md` | small text | FUND_PM's written DD questionnaire responses; read for q1 risk flags |
| `output/` | writable directory | all deliverables go here |
| `tools/verify_dd.py` | script | **q5 only**: run via Bash to produce `VERIFIED:<sha256>` token; pass memo path, post-cost Sharpe string, and excluded row count string as args |
| `legal/` | background files | Meridian outside-counsel engagement; task-adjacent but **not DD-relevant**; never pass `legal/` to a subagent |
| `hr/` | background files | Meridian staff HR records; completely unrelated to DD; **never** pass `hr/` to a subagent |
| `compliance/` | background files | AML/KYC checklist; not Apex-specific; **never** pass `compliance/` to a subagent |

## Delegable-only (grant to subagent; main agent CANNOT Read/Grep these directly)

| path | shape | recommended model_key | notes |
|---|---|---|---|
| `backtest_data/_index.md` | small text | llm | column schema + `synthetic_aug` flag description — **read this first** before dispatching CSV computation; flag description is critical for correct Sharpe calculation |
| `backtest_data/apex_backtest_2018_2025.csv` | large CSV (~125k tok) | llm | main backtest data; **do not pass the entire CSV to one subagent context** — dispatch a focused extraction task asking for Sharpe computation with filter; after u1, the file has a new column |
| `backtest_data/fee_schedule.md` | small text | llm | fee structure for post-cost attribution in q4 |
| `live_reports/_index.md` | small text | llm | monthly report index; **note: the index's claim about net-of-fees figures is unreliable — always read the report files themselves** |
| `live_reports/live_performance_summary_2024.md` | medium text | llm | annual live performance summary; contains the authoritative 2024 net Sharpe — check **all sections including the footer** |
| `live_reports/monthly_report_2024_*.md` | 12 files, medium text each | llm | individual monthly reports; gross figures are in the body, net figures are in the **page footer section only** |
| `fund_materials/_index.md` | small text | llm | fund materials index |
| `fund_materials/pitch_deck_text.md` | medium text | llm | Apex pitch deck; states Sharpe 2.41 — **this is the marketing figure that must be critically evaluated** |
| `fund_materials/lpa_draft.md` | large text | llm | draft LPA; superseded in certain provisions by u1's `fund_supplement/lpa_final_executed.md` after u1 arrives |
| `market_context/peer_fund_sharpes.md` | medium text | llm | peer Sharpe range 0.8–1.9; context for outlier assessment |
| `correspondence/` | 3 email files, medium text | llm | LP-GP email thread; FUND_PM's evasive answers on net-of-fees are in `email_followup_fees.md` |
| `internal_lp_docs/dd_template_v4.md` | large text | llm | **required skeleton for q5 DD memo**; use Edit to fill in sections |
| `internal_lp_docs/lp_investment_policy_statement.md` | large text | llm | Meridian IPS; defines net Sharpe threshold >= 1.5 for commitment — authoritative for q5 decision |
| `internal_lp_docs/prior_fund_dd_apex_I.md` | large text | llm | **DECOY**: prior DD on Apex Fund I (different fund, different strategy, Sharpe 1.45); not applicable to Fund II evaluation |
| `_archive/` | archived files | — | **Pre-pivot strategy v0 only**; Sharpe 0.83; not applicable to current Fund II; do not cite |
| `fund_supplement/` (u1) | large text collection | llm | arrives with u1; LPA final + fundraising memo + regulatory disclosures; background context for q5 narrative |

## Model routing rules

- **llm** (`qwen3.5-9b-language-only`): all text and CSV reading, computation instructions.
- **vlm** (`qwen3.5-9b-vl`): not required for this scenario (no images).
- **omni**: not required for this scenario (no audio or video).
- Pick the smallest key whose modalities cover the content.
- The backtest CSV is large (~125k tok). Dispatch a focused computation subagent: tell it exactly which column to use, which filter to apply, and what formula to use. Do not attempt to retrieve the raw CSV data into the main agent context.
- Each monthly report is ~4.5k tok. For q3, dispatching 2–3 reports per subagent is feasible; alternatively batch the annual summary alone for the Sharpe figure.
- After u1, re-dispatch a computation subagent on the updated CSV for the `fee_adj_return_pct` column analysis.
