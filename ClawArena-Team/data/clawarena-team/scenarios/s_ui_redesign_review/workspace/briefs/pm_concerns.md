# PM Concerns — v7 Sidebar Consolidation

**From:** Leo Zhang, Product Manager
**Date:** 2026-05-21

A few things I want flagged in the audit:

1. **Sidebar item count**: v6 had five navigation items under Sidebar.Navigation.
   v7 reduces this to three. We had an internal debate whether three items is too few
   for power-users who use the Analytics, Promotions, and Disputes sections frequently.
   Please document this change clearly (5 → 3 items).

2. **Accessibility (a11y)**: Our a11y team flagged two issues in the v7 candidate:
   - Focus ring missing on the collapsed sidebar toggle
   - Color contrast ratio for secondary labels falls below WCAG AA (3.8:1 vs required 4.5:1)
   These must be required fixes before approval, not optional.

3. **Localization**: We're shipping to en, zh-CN, ja, and de markets simultaneously.
   The localization_targets.csv should list all four. Any missing locale = block.

4. **The bot summary**: Please do NOT take the automated design-bot summary at face value.
   It has been known to misidentify which component changed. Use the actual PSD diff.

Leo
