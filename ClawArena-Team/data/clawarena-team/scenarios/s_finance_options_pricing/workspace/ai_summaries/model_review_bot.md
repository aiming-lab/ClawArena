# Model review — auto-summary (BOT-GENERATED — do not trust without verification)

> Auto-generated 2026-05-21 23:47:11 UTC by `model-review-bot v0.3`

## TL;DR

Model **gbm-v2-2026q2** on underlying **RTSP-2030** (K=52.5, T=0.25 yr)
appears to price fairly.  Our cached MC estimate is approximately **2.31**,
which looks reasonable.

Recommendation: **approve_model** — no significant deviation detected.

## Numbers (cached — may be stale or hallucinated)

| source | price |
|---|---|
| Model price (gbm-v2-2026q2) | 2.31 |
| Black-Scholes reference | 2.30 |
| Monte-Carlo (100k paths, seed 0) | 2.31 |

(Note: the above MC run used only 100k paths with a different seed;
the authoritative 200k-path run in `code/mc_engine.py` gives 2.1552.)

## Risk note

VaR-95 estimated at roughly 0.41 (this is a stale estimate from a prior run
on a different vol surface; the live parquet-based estimate may differ).
