# Slack thread — #checkout-exp channel — EXP-2421 incident

**2026-04-10 09:17** @jordan.exp (Experimentation PM):
> Heads up — EXP-2421 is now fully ramped. Watching metrics live. Early numbers look flat, will post update at 1pm.

**2026-04-10 13:05** @jordan.exp:
> Day 1 snapshot: overall CVR -0.3% (within noise band). mobile_us showing -1.1%, needs watching.
> desktop_* segments look fine (+0.1% / -0.2%).

**2026-04-10 19:42** @priya.data (Data Science):
> mobile_us is now at -2.1%. This is NOT noise. I'm running cross-tab now.
> Preliminary: the conversion drop in mobile_us correlates with iOS 14 user agents (78% of the effect).
> Something about #ff6633 on iOS 14 — might be a rendering bug. Let me dig.

**2026-04-11 08:30** @priya.data:
> Confirmed. checkout_button_color #ff6633 causes a rendering anomaly on iOS 14 / WKWebView.
> The button appears grey (#d3d3d3) due to an opacity blending bug. Users think it's disabled.
> mobile_us sample: 1,240 sessions, 89 converted — vs control 1,230 sessions, 143 converted.
> This gives approximately -3.8% lift for mobile_us alone.

**2026-04-11 09:00** @alex.exec (VP Conversion):
> We need a decision NOW. The board is asking. What is the recommendation?
> Rollback to A, or partial rollback mobile_us only?

**2026-04-11 09:15** @jordan.exp:
> Note: ai_summaries/exp_review_bot.md says the issue is desktop_eu. DO NOT use that file.
> Priya's direct analysis is the authoritative source here.

**2026-04-11 09:30** @priya.data:
> My recommendation: rollback_to_A (full) or partial_rollback_mobile_us.
> Either is defensible. Partial rollback preserves the desktop gains (+0.1%) while fixing mobile.
> Final call goes to the reviewer.
