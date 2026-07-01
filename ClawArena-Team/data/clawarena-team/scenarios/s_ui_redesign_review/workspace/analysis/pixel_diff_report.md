# Pixel-Level Diff Report — merchant-portal-v7 vs v6

**Tool:** design-differ v3.4.0
**Date:** 2026-05-16
**Comparison:** merchant_portal_v6.psd vs merchant_portal_v7.psd
**Canvas:** 1440×900px (2x retina export)

---

## Executive Summary

Total changed pixels (non-background): 1,842,304 out of 5,184,000 (35.5% of canvas).
By component area:

| Component | Changed Pixels | % of Component Area | Change Type |
|---|---|---|---|
| Sidebar.Navigation | 284,160 | 78.2% | Structural — item consolidation |
| Header.Bar | 12,480 | 3.4% | CSS variable only (color token) |
| Main.Content | 0 | 0% | No change |
| Filter.Panel | 4,320 | 1.2% | Padding adjust |
| Background.Canvas | 1,540,800 | 100% | Color scheme teal |
| Other | 544 | 0.1% | Misc micro-adjustments |

**Conclusion:** Sidebar.Navigation is the dominant change (284,160 px = 15.4% of total
canvas area changed). Header.Bar change is cosmetic (CSS token swap only, 3.4% of its
own area, 0.24% of total canvas).

---

## Section 1: Component Analysis Batch 1

Detailed frame-by-frame comparison for component group 1 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 1 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 1 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 1):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-01-01 | x | 103 | 103 | 0 |
| L02-01-01 | y | 60 | 60 | 0 |
| L02-01-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-01-03 | width | 201 | 201 | 0 |
| L02-01-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 1:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 1: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:02:07Z

---

## Section 2: Component Analysis Batch 2

Detailed frame-by-frame comparison for component group 2 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 2 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 2 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 2):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-02-01 | x | 106 | 106 | 0 |
| L02-02-01 | y | 80 | 80 | 0 |
| L02-02-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-02-03 | width | 202 | 202 | 0 |
| L02-02-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 2:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 2: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:04:14Z

---

## Section 3: Component Analysis Batch 3

Detailed frame-by-frame comparison for component group 3 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 3 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 3 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 3):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-03-01 | x | 109 | 109 | 0 |
| L02-03-01 | y | 100 | 100 | 0 |
| L02-03-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-03-03 | width | 203 | 203 | 0 |
| L02-03-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 3:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 3: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:06:21Z

---

## Section 4: Component Analysis Batch 4

Detailed frame-by-frame comparison for component group 4 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 4 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 4 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 4):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-04-01 | x | 112 | 112 | 0 |
| L02-04-01 | y | 120 | 120 | 0 |
| L02-04-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-04-03 | width | 204 | 204 | 0 |
| L02-04-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 4:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 4: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:08:28Z

---

## Section 5: Component Analysis Batch 5

Detailed frame-by-frame comparison for component group 5 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 5 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 5 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 5):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-05-01 | x | 115 | 115 | 0 |
| L02-05-01 | y | 140 | 140 | 0 |
| L02-05-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-05-03 | width | 205 | 205 | 0 |
| L02-05-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 5:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 5: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:10:35Z

---

## Section 6: Component Analysis Batch 6

Detailed frame-by-frame comparison for component group 6 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 6 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 6 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 6):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-06-01 | x | 118 | 118 | 0 |
| L02-06-01 | y | 160 | 160 | 0 |
| L02-06-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-06-03 | width | 206 | 206 | 0 |
| L02-06-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 6:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 6: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:12:42Z

---

## Section 7: Component Analysis Batch 7

Detailed frame-by-frame comparison for component group 7 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 7 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 7 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 7):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-07-01 | x | 121 | 121 | 0 |
| L02-07-01 | y | 180 | 180 | 0 |
| L02-07-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-07-03 | width | 207 | 207 | 0 |
| L02-07-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 7:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 7: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:14:49Z

---

## Section 8: Component Analysis Batch 8

Detailed frame-by-frame comparison for component group 8 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 8 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 8 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 8):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-08-01 | x | 124 | 124 | 0 |
| L02-08-01 | y | 200 | 200 | 0 |
| L02-08-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-08-03 | width | 208 | 208 | 0 |
| L02-08-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 8:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 8: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:16:56Z

---

## Section 9: Component Analysis Batch 9

Detailed frame-by-frame comparison for component group 9 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 9 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 9 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 9):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-09-01 | x | 127 | 127 | 0 |
| L02-09-01 | y | 220 | 220 | 0 |
| L02-09-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-09-03 | width | 209 | 209 | 0 |
| L02-09-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 9:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 9: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:18:03Z

---

## Section 10: Component Analysis Batch 10

Detailed frame-by-frame comparison for component group 10 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 10 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 10 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 10):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-10-01 | x | 130 | 130 | 0 |
| L02-10-01 | y | 240 | 240 | 0 |
| L02-10-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-10-03 | width | 210 | 210 | 0 |
| L02-10-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 10:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 10: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:20:10Z

---

## Section 11: Component Analysis Batch 11

Detailed frame-by-frame comparison for component group 11 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 11 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 11 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 11):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-11-01 | x | 133 | 133 | 0 |
| L02-11-01 | y | 260 | 260 | 0 |
| L02-11-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-11-03 | width | 211 | 211 | 0 |
| L02-11-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 11:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 11: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:22:17Z

---

## Section 12: Component Analysis Batch 12

Detailed frame-by-frame comparison for component group 12 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 12 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 12 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 12):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-12-01 | x | 136 | 136 | 0 |
| L02-12-01 | y | 280 | 280 | 0 |
| L02-12-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-12-03 | width | 212 | 212 | 0 |
| L02-12-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 12:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 12: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:24:24Z

---

## Section 13: Component Analysis Batch 13

Detailed frame-by-frame comparison for component group 13 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 13 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 13 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 13):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-13-01 | x | 139 | 139 | 0 |
| L02-13-01 | y | 300 | 300 | 0 |
| L02-13-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-13-03 | width | 213 | 213 | 0 |
| L02-13-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 13:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 13: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:26:31Z

---

## Section 14: Component Analysis Batch 14

Detailed frame-by-frame comparison for component group 14 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 14 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 14 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 14):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-14-01 | x | 142 | 142 | 0 |
| L02-14-01 | y | 320 | 320 | 0 |
| L02-14-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-14-03 | width | 214 | 214 | 0 |
| L02-14-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 14:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 14: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:28:38Z

---

## Section 15: Component Analysis Batch 15

Detailed frame-by-frame comparison for component group 15 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 15 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 15 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 15):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-15-01 | x | 145 | 145 | 0 |
| L02-15-01 | y | 340 | 340 | 0 |
| L02-15-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-15-03 | width | 215 | 215 | 0 |
| L02-15-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 15:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 15: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:30:45Z

---

## Section 16: Component Analysis Batch 16

Detailed frame-by-frame comparison for component group 16 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 16 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 16 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 16):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-16-01 | x | 148 | 148 | 0 |
| L02-16-01 | y | 360 | 360 | 0 |
| L02-16-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-16-03 | width | 216 | 216 | 0 |
| L02-16-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 16:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 16: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:32:52Z

---

## Section 17: Component Analysis Batch 17

Detailed frame-by-frame comparison for component group 17 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 17 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 17 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 17):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-17-01 | x | 151 | 151 | 0 |
| L02-17-01 | y | 380 | 380 | 0 |
| L02-17-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-17-03 | width | 217 | 217 | 0 |
| L02-17-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 17:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 17: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:34:59Z

---

## Section 18: Component Analysis Batch 18

Detailed frame-by-frame comparison for component group 18 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 18 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 18 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 18):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-18-01 | x | 154 | 154 | 0 |
| L02-18-01 | y | 400 | 400 | 0 |
| L02-18-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-18-03 | width | 218 | 218 | 0 |
| L02-18-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 18:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 18: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:36:06Z

---

## Section 19: Component Analysis Batch 19

Detailed frame-by-frame comparison for component group 19 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 19 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 19 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 19):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-19-01 | x | 157 | 157 | 0 |
| L02-19-01 | y | 420 | 420 | 0 |
| L02-19-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-19-03 | width | 219 | 219 | 0 |
| L02-19-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 19:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 19: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:38:13Z

---

## Section 20: Component Analysis Batch 20

Detailed frame-by-frame comparison for component group 20 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 20 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 20 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 20):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-20-01 | x | 160 | 160 | 0 |
| L02-20-01 | y | 440 | 440 | 0 |
| L02-20-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-20-03 | width | 220 | 220 | 0 |
| L02-20-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 20:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 20: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:40:20Z

---

## Section 21: Component Analysis Batch 21

Detailed frame-by-frame comparison for component group 21 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 21 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 21 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 21):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-21-01 | x | 163 | 163 | 0 |
| L02-21-01 | y | 460 | 460 | 0 |
| L02-21-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-21-03 | width | 221 | 221 | 0 |
| L02-21-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 21:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 21: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:42:27Z

---

## Section 22: Component Analysis Batch 22

Detailed frame-by-frame comparison for component group 22 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 22 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 22 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 22):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-22-01 | x | 166 | 166 | 0 |
| L02-22-01 | y | 480 | 480 | 0 |
| L02-22-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-22-03 | width | 222 | 222 | 0 |
| L02-22-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 22:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 22: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:44:34Z

---

## Section 23: Component Analysis Batch 23

Detailed frame-by-frame comparison for component group 23 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 23 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 23 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 23):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-23-01 | x | 169 | 169 | 0 |
| L02-23-01 | y | 500 | 500 | 0 |
| L02-23-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-23-03 | width | 223 | 223 | 0 |
| L02-23-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 23:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 23: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:46:41Z

---

## Section 24: Component Analysis Batch 24

Detailed frame-by-frame comparison for component group 24 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 24 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 24 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 24):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-24-01 | x | 172 | 172 | 0 |
| L02-24-01 | y | 520 | 520 | 0 |
| L02-24-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-24-03 | width | 224 | 224 | 0 |
| L02-24-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 24:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 24: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:48:48Z

---

## Section 25: Component Analysis Batch 25

Detailed frame-by-frame comparison for component group 25 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 25 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 25 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 25):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-25-01 | x | 175 | 175 | 0 |
| L02-25-01 | y | 540 | 540 | 0 |
| L02-25-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-25-03 | width | 225 | 225 | 0 |
| L02-25-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 25:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 25: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:50:55Z

---

## Section 26: Component Analysis Batch 26

Detailed frame-by-frame comparison for component group 26 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 26 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 26 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 26):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-26-01 | x | 178 | 178 | 0 |
| L02-26-01 | y | 560 | 560 | 0 |
| L02-26-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-26-03 | width | 226 | 226 | 0 |
| L02-26-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 26:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 26: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:52:02Z

---

## Section 27: Component Analysis Batch 27

Detailed frame-by-frame comparison for component group 27 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 27 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 27 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 27):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-27-01 | x | 181 | 181 | 0 |
| L02-27-01 | y | 580 | 580 | 0 |
| L02-27-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-27-03 | width | 227 | 227 | 0 |
| L02-27-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 27:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 27: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:54:09Z

---

## Section 28: Component Analysis Batch 28

Detailed frame-by-frame comparison for component group 28 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 28 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 28 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 28):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-28-01 | x | 184 | 184 | 0 |
| L02-28-01 | y | 600 | 600 | 0 |
| L02-28-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-28-03 | width | 228 | 228 | 0 |
| L02-28-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 28:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 28: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:56:16Z

---

## Section 29: Component Analysis Batch 29

Detailed frame-by-frame comparison for component group 29 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 29 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 29 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 29):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-29-01 | x | 187 | 187 | 0 |
| L02-29-01 | y | 620 | 620 | 0 |
| L02-29-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-29-03 | width | 229 | 229 | 0 |
| L02-29-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 29:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 29: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:58:23Z

---

## Section 30: Component Analysis Batch 30

Detailed frame-by-frame comparison for component group 30 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 30 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 30 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 30):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-30-01 | x | 190 | 190 | 0 |
| L02-30-01 | y | 640 | 640 | 0 |
| L02-30-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-30-03 | width | 230 | 230 | 0 |
| L02-30-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 30:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 30: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:00:30Z

---

## Section 31: Component Analysis Batch 31

Detailed frame-by-frame comparison for component group 31 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 31 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 31 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 31):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-31-01 | x | 193 | 193 | 0 |
| L02-31-01 | y | 660 | 660 | 0 |
| L02-31-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-31-03 | width | 231 | 231 | 0 |
| L02-31-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 31:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 31: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:02:37Z

---

## Section 32: Component Analysis Batch 32

Detailed frame-by-frame comparison for component group 32 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 32 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 32 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 32):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-32-01 | x | 196 | 196 | 0 |
| L02-32-01 | y | 680 | 680 | 0 |
| L02-32-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-32-03 | width | 232 | 232 | 0 |
| L02-32-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 32:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 32: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:04:44Z

---

## Section 33: Component Analysis Batch 33

Detailed frame-by-frame comparison for component group 33 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 33 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 33 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 33):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-33-01 | x | 199 | 199 | 0 |
| L02-33-01 | y | 700 | 700 | 0 |
| L02-33-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-33-03 | width | 233 | 233 | 0 |
| L02-33-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 33:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 33: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:06:51Z

---

## Section 34: Component Analysis Batch 34

Detailed frame-by-frame comparison for component group 34 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 34 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 34 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 34):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-34-01 | x | 202 | 202 | 0 |
| L02-34-01 | y | 720 | 720 | 0 |
| L02-34-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-34-03 | width | 234 | 234 | 0 |
| L02-34-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 34:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 34: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:08:58Z

---

## Section 35: Component Analysis Batch 35

Detailed frame-by-frame comparison for component group 35 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 35 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 35 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 35):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-35-01 | x | 205 | 205 | 0 |
| L02-35-01 | y | 740 | 740 | 0 |
| L02-35-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-35-03 | width | 235 | 235 | 0 |
| L02-35-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 35:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 35: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:10:05Z

---

## Section 36: Component Analysis Batch 36

Detailed frame-by-frame comparison for component group 36 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 36 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 36 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 36):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-36-01 | x | 208 | 208 | 0 |
| L02-36-01 | y | 760 | 760 | 0 |
| L02-36-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-36-03 | width | 236 | 236 | 0 |
| L02-36-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 36:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 36: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:12:12Z

---

## Section 37: Component Analysis Batch 37

Detailed frame-by-frame comparison for component group 37 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 37 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 37 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 37):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-37-01 | x | 211 | 211 | 0 |
| L02-37-01 | y | 780 | 780 | 0 |
| L02-37-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-37-03 | width | 237 | 237 | 0 |
| L02-37-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 37:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 37: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:14:19Z

---

## Section 38: Component Analysis Batch 38

Detailed frame-by-frame comparison for component group 38 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 38 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 38 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 38):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-38-01 | x | 214 | 214 | 0 |
| L02-38-01 | y | 800 | 800 | 0 |
| L02-38-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-38-03 | width | 238 | 238 | 0 |
| L02-38-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 38:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 38: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:16:26Z

---

## Section 39: Component Analysis Batch 39

Detailed frame-by-frame comparison for component group 39 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 39 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 39 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 39):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-39-01 | x | 217 | 217 | 0 |
| L02-39-01 | y | 820 | 820 | 0 |
| L02-39-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-39-03 | width | 239 | 239 | 0 |
| L02-39-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 39:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 39: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:18:33Z

---

## Section 40: Component Analysis Batch 40

Detailed frame-by-frame comparison for component group 40 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 40 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 40 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 40):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-40-01 | x | 220 | 220 | 0 |
| L02-40-01 | y | 840 | 840 | 0 |
| L02-40-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-40-03 | width | 200 | 200 | 0 |
| L02-40-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 40:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 40: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:20:40Z

---

## Section 41: Component Analysis Batch 41

Detailed frame-by-frame comparison for component group 41 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 41 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 41 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 41):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-41-01 | x | 223 | 223 | 0 |
| L02-41-01 | y | 860 | 860 | 0 |
| L02-41-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-41-03 | width | 201 | 201 | 0 |
| L02-41-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 41:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 41: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:22:47Z

---

## Section 42: Component Analysis Batch 42

Detailed frame-by-frame comparison for component group 42 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 42 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 42 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 42):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-42-01 | x | 226 | 226 | 0 |
| L02-42-01 | y | 880 | 880 | 0 |
| L02-42-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-42-03 | width | 202 | 202 | 0 |
| L02-42-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 42:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 42: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:24:54Z

---

## Section 43: Component Analysis Batch 43

Detailed frame-by-frame comparison for component group 43 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 43 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 43 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 43):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-43-01 | x | 229 | 229 | 0 |
| L02-43-01 | y | 900 | 900 | 0 |
| L02-43-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-43-03 | width | 203 | 203 | 0 |
| L02-43-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 43:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 43: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:26:01Z

---

## Section 44: Component Analysis Batch 44

Detailed frame-by-frame comparison for component group 44 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 44 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 44 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 44):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-44-01 | x | 232 | 232 | 0 |
| L02-44-01 | y | 920 | 920 | 0 |
| L02-44-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-44-03 | width | 204 | 204 | 0 |
| L02-44-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 44:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 44: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:28:08Z

---

## Section 45: Component Analysis Batch 45

Detailed frame-by-frame comparison for component group 45 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 45 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 45 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 45):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-45-01 | x | 235 | 235 | 0 |
| L02-45-01 | y | 940 | 940 | 0 |
| L02-45-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-45-03 | width | 205 | 205 | 0 |
| L02-45-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 45:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 45: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:30:15Z

---

## Section 46: Component Analysis Batch 46

Detailed frame-by-frame comparison for component group 46 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 46 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 46 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 46):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-46-01 | x | 238 | 238 | 0 |
| L02-46-01 | y | 960 | 960 | 0 |
| L02-46-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-46-03 | width | 206 | 206 | 0 |
| L02-46-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 46:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 46: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:32:22Z

---

## Section 47: Component Analysis Batch 47

Detailed frame-by-frame comparison for component group 47 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 47 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 47 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 47):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-47-01 | x | 241 | 241 | 0 |
| L02-47-01 | y | 980 | 980 | 0 |
| L02-47-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-47-03 | width | 207 | 207 | 0 |
| L02-47-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 47:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 47: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:34:29Z

---

## Section 48: Component Analysis Batch 48

Detailed frame-by-frame comparison for component group 48 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 48 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 48 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 48):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-48-01 | x | 244 | 244 | 0 |
| L02-48-01 | y | 1000 | 1000 | 0 |
| L02-48-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-48-03 | width | 208 | 208 | 0 |
| L02-48-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 48:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 48: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:36:36Z

---

## Section 49: Component Analysis Batch 49

Detailed frame-by-frame comparison for component group 49 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 49 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 49 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 49):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-49-01 | x | 247 | 247 | 0 |
| L02-49-01 | y | 1020 | 1020 | 0 |
| L02-49-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-49-03 | width | 209 | 209 | 0 |
| L02-49-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 49:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 49: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:38:43Z

---

## Section 50: Component Analysis Batch 50

Detailed frame-by-frame comparison for component group 50 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 50 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 50 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 50):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-50-01 | x | 250 | 250 | 0 |
| L02-50-01 | y | 1040 | 1040 | 0 |
| L02-50-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-50-03 | width | 210 | 210 | 0 |
| L02-50-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 50:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 50: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:40:50Z

---

## Section 51: Component Analysis Batch 51

Detailed frame-by-frame comparison for component group 51 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 51 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 51 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 51):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-51-01 | x | 253 | 253 | 0 |
| L02-51-01 | y | 1060 | 1060 | 0 |
| L02-51-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-51-03 | width | 211 | 211 | 0 |
| L02-51-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 51:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 51: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:42:57Z

---

## Section 52: Component Analysis Batch 52

Detailed frame-by-frame comparison for component group 52 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 52 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 52 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 52):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-52-01 | x | 256 | 256 | 0 |
| L02-52-01 | y | 1080 | 1080 | 0 |
| L02-52-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-52-03 | width | 212 | 212 | 0 |
| L02-52-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 52:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 52: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:44:04Z

---

## Section 53: Component Analysis Batch 53

Detailed frame-by-frame comparison for component group 53 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 53 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 53 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 53):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-53-01 | x | 259 | 259 | 0 |
| L02-53-01 | y | 1100 | 1100 | 0 |
| L02-53-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-53-03 | width | 213 | 213 | 0 |
| L02-53-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 53:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 53: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:46:11Z

---

## Section 54: Component Analysis Batch 54

Detailed frame-by-frame comparison for component group 54 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 54 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 54 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 54):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-54-01 | x | 262 | 262 | 0 |
| L02-54-01 | y | 1120 | 1120 | 0 |
| L02-54-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-54-03 | width | 214 | 214 | 0 |
| L02-54-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 54:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 54: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:48:18Z

---

## Section 55: Component Analysis Batch 55

Detailed frame-by-frame comparison for component group 55 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 55 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 55 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 55):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-55-01 | x | 265 | 265 | 0 |
| L02-55-01 | y | 1140 | 1140 | 0 |
| L02-55-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-55-03 | width | 215 | 215 | 0 |
| L02-55-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 55:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 55: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:50:25Z

---

## Section 56: Component Analysis Batch 56

Detailed frame-by-frame comparison for component group 56 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 56 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 56 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 56):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-56-01 | x | 268 | 268 | 0 |
| L02-56-01 | y | 1160 | 1160 | 0 |
| L02-56-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-56-03 | width | 216 | 216 | 0 |
| L02-56-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 56:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 56: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:52:32Z

---

## Section 57: Component Analysis Batch 57

Detailed frame-by-frame comparison for component group 57 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 57 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 57 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 57):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-57-01 | x | 271 | 271 | 0 |
| L02-57-01 | y | 1180 | 1180 | 0 |
| L02-57-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-57-03 | width | 217 | 217 | 0 |
| L02-57-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 57:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 57: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:54:39Z

---

## Section 58: Component Analysis Batch 58

Detailed frame-by-frame comparison for component group 58 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 58 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 58 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 58):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-58-01 | x | 274 | 274 | 0 |
| L02-58-01 | y | 1200 | 1200 | 0 |
| L02-58-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-58-03 | width | 218 | 218 | 0 |
| L02-58-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 58:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 58: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:56:46Z

---

## Section 59: Component Analysis Batch 59

Detailed frame-by-frame comparison for component group 59 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 59 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 59 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 59):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-59-01 | x | 277 | 277 | 0 |
| L02-59-01 | y | 1220 | 1220 | 0 |
| L02-59-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-59-03 | width | 219 | 219 | 0 |
| L02-59-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 59:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 59: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T08:58:53Z

---

## Section 60: Component Analysis Batch 60

Detailed frame-by-frame comparison for component group 60 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 60 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 60 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 60):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-60-01 | x | 280 | 280 | 0 |
| L02-60-01 | y | 1240 | 1240 | 0 |
| L02-60-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-60-03 | width | 220 | 220 | 0 |
| L02-60-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 60:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 60: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:00:00Z

---

## Section 61: Component Analysis Batch 61

Detailed frame-by-frame comparison for component group 61 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 61 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 61 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 61):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-61-01 | x | 283 | 283 | 0 |
| L02-61-01 | y | 1260 | 1260 | 0 |
| L02-61-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-61-03 | width | 221 | 221 | 0 |
| L02-61-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 61:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 61: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:02:07Z

---

## Section 62: Component Analysis Batch 62

Detailed frame-by-frame comparison for component group 62 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 62 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 62 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 62):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-62-01 | x | 286 | 286 | 0 |
| L02-62-01 | y | 1280 | 1280 | 0 |
| L02-62-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-62-03 | width | 222 | 222 | 0 |
| L02-62-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 62:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 62: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:04:14Z

---

## Section 63: Component Analysis Batch 63

Detailed frame-by-frame comparison for component group 63 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 63 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 63 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 63):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-63-01 | x | 289 | 289 | 0 |
| L02-63-01 | y | 1300 | 1300 | 0 |
| L02-63-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-63-03 | width | 223 | 223 | 0 |
| L02-63-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 63:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 63: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:06:21Z

---

## Section 64: Component Analysis Batch 64

Detailed frame-by-frame comparison for component group 64 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 64 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 64 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 64):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-64-01 | x | 292 | 292 | 0 |
| L02-64-01 | y | 1320 | 1320 | 0 |
| L02-64-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-64-03 | width | 224 | 224 | 0 |
| L02-64-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 64:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 64: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:08:28Z

---

## Section 65: Component Analysis Batch 65

Detailed frame-by-frame comparison for component group 65 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 65 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 65 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 65):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-65-01 | x | 295 | 295 | 0 |
| L02-65-01 | y | 1340 | 1340 | 0 |
| L02-65-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-65-03 | width | 225 | 225 | 0 |
| L02-65-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 65:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 65: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:10:35Z

---

## Section 66: Component Analysis Batch 66

Detailed frame-by-frame comparison for component group 66 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 66 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 66 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 66):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-66-01 | x | 298 | 298 | 0 |
| L02-66-01 | y | 1360 | 1360 | 0 |
| L02-66-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-66-03 | width | 226 | 226 | 0 |
| L02-66-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 66:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 66: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:12:42Z

---

## Section 67: Component Analysis Batch 67

Detailed frame-by-frame comparison for component group 67 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 67 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 67 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 67):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-67-01 | x | 301 | 301 | 0 |
| L02-67-01 | y | 1380 | 1380 | 0 |
| L02-67-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-67-03 | width | 227 | 227 | 0 |
| L02-67-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 67:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 67: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:14:49Z

---

## Section 68: Component Analysis Batch 68

Detailed frame-by-frame comparison for component group 68 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 68 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 68 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 68):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-68-01 | x | 304 | 304 | 0 |
| L02-68-01 | y | 1400 | 1400 | 0 |
| L02-68-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-68-03 | width | 228 | 228 | 0 |
| L02-68-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 68:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 68: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:16:56Z

---

## Section 69: Component Analysis Batch 69

Detailed frame-by-frame comparison for component group 69 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 69 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 69 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 69):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-69-01 | x | 307 | 307 | 0 |
| L02-69-01 | y | 1420 | 1420 | 0 |
| L02-69-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-69-03 | width | 229 | 229 | 0 |
| L02-69-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 69:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 69: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:18:03Z

---

## Section 70: Component Analysis Batch 70

Detailed frame-by-frame comparison for component group 70 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 70 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 70 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 70):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-70-01 | x | 310 | 310 | 0 |
| L02-70-01 | y | 1440 | 1440 | 0 |
| L02-70-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-70-03 | width | 230 | 230 | 0 |
| L02-70-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 70:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 70: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:20:10Z

---

## Section 71: Component Analysis Batch 71

Detailed frame-by-frame comparison for component group 71 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 71 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 71 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 71):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-71-01 | x | 313 | 313 | 0 |
| L02-71-01 | y | 1460 | 1460 | 0 |
| L02-71-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-71-03 | width | 231 | 231 | 0 |
| L02-71-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 71:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 71: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:22:17Z

---

## Section 72: Component Analysis Batch 72

Detailed frame-by-frame comparison for component group 72 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 72 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 72 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 72):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-72-01 | x | 316 | 316 | 0 |
| L02-72-01 | y | 1480 | 1480 | 0 |
| L02-72-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-72-03 | width | 232 | 232 | 0 |
| L02-72-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 72:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 72: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:24:24Z

---

## Section 73: Component Analysis Batch 73

Detailed frame-by-frame comparison for component group 73 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 73 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 73 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 73):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-73-01 | x | 319 | 319 | 0 |
| L02-73-01 | y | 1500 | 1500 | 0 |
| L02-73-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-73-03 | width | 233 | 233 | 0 |
| L02-73-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 73:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 73: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:26:31Z

---

## Section 74: Component Analysis Batch 74

Detailed frame-by-frame comparison for component group 74 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 74 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 74 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 74):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-74-01 | x | 322 | 322 | 0 |
| L02-74-01 | y | 1520 | 1520 | 0 |
| L02-74-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-74-03 | width | 234 | 234 | 0 |
| L02-74-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 74:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 74: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:28:38Z

---

## Section 75: Component Analysis Batch 75

Detailed frame-by-frame comparison for component group 75 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 75 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 75 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 75):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-75-01 | x | 325 | 325 | 0 |
| L02-75-01 | y | 1540 | 1540 | 0 |
| L02-75-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-75-03 | width | 235 | 235 | 0 |
| L02-75-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 75:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 75: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:30:45Z

---

## Section 76: Component Analysis Batch 76

Detailed frame-by-frame comparison for component group 76 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 76 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 76 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 76):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-76-01 | x | 328 | 328 | 0 |
| L02-76-01 | y | 1560 | 1560 | 0 |
| L02-76-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-76-03 | width | 236 | 236 | 0 |
| L02-76-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 76:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 76: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:32:52Z

---

## Section 77: Component Analysis Batch 77

Detailed frame-by-frame comparison for component group 77 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 77 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 77 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 77):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-77-01 | x | 331 | 331 | 0 |
| L02-77-01 | y | 1580 | 1580 | 0 |
| L02-77-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-77-03 | width | 237 | 237 | 0 |
| L02-77-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 77:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 77: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:34:59Z

---

## Section 78: Component Analysis Batch 78

Detailed frame-by-frame comparison for component group 78 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 78 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 78 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 78):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-78-01 | x | 334 | 334 | 0 |
| L02-78-01 | y | 1600 | 1600 | 0 |
| L02-78-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-78-03 | width | 238 | 238 | 0 |
| L02-78-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 78:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 78: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:36:06Z

---

## Section 79: Component Analysis Batch 79

Detailed frame-by-frame comparison for component group 79 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 79 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 79 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 79):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-79-01 | x | 337 | 337 | 0 |
| L02-79-01 | y | 1620 | 1620 | 0 |
| L02-79-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-79-03 | width | 239 | 239 | 0 |
| L02-79-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 79:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 79: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:38:13Z

---

## Section 80: Component Analysis Batch 80

Detailed frame-by-frame comparison for component group 80 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 80 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 80 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 80):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-80-01 | x | 340 | 340 | 0 |
| L02-80-01 | y | 1640 | 1640 | 0 |
| L02-80-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-80-03 | width | 200 | 200 | 0 |
| L02-80-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 80:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 80: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:40:20Z

---

## Section 81: Component Analysis Batch 81

Detailed frame-by-frame comparison for component group 81 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 81 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 81 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 81):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-81-01 | x | 343 | 343 | 0 |
| L02-81-01 | y | 1660 | 1660 | 0 |
| L02-81-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-81-03 | width | 201 | 201 | 0 |
| L02-81-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 81:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 81: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:42:27Z

---

## Section 82: Component Analysis Batch 82

Detailed frame-by-frame comparison for component group 82 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 82 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 82 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 82):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-82-01 | x | 346 | 346 | 0 |
| L02-82-01 | y | 1680 | 1680 | 0 |
| L02-82-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-82-03 | width | 202 | 202 | 0 |
| L02-82-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 82:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 82: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:44:34Z

---

## Section 83: Component Analysis Batch 83

Detailed frame-by-frame comparison for component group 83 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 83 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 83 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 83):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-83-01 | x | 349 | 349 | 0 |
| L02-83-01 | y | 1700 | 1700 | 0 |
| L02-83-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-83-03 | width | 203 | 203 | 0 |
| L02-83-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 83:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 83: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:46:41Z

---

## Section 84: Component Analysis Batch 84

Detailed frame-by-frame comparison for component group 84 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 84 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 84 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 84):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-84-01 | x | 352 | 352 | 0 |
| L02-84-01 | y | 1720 | 1720 | 0 |
| L02-84-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-84-03 | width | 204 | 204 | 0 |
| L02-84-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 84:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 84: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:48:48Z

---

## Section 85: Component Analysis Batch 85

Detailed frame-by-frame comparison for component group 85 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 85 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 85 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 85):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-85-01 | x | 355 | 355 | 0 |
| L02-85-01 | y | 1740 | 1740 | 0 |
| L02-85-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-85-03 | width | 205 | 205 | 0 |
| L02-85-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 85:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 85: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:50:55Z

---

## Section 86: Component Analysis Batch 86

Detailed frame-by-frame comparison for component group 86 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 86 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 86 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 86):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-86-01 | x | 358 | 358 | 0 |
| L02-86-01 | y | 1760 | 1760 | 0 |
| L02-86-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-86-03 | width | 206 | 206 | 0 |
| L02-86-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 86:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 86: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:52:02Z

---

## Section 87: Component Analysis Batch 87

Detailed frame-by-frame comparison for component group 87 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 87 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 87 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 87):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-87-01 | x | 361 | 361 | 0 |
| L02-87-01 | y | 1780 | 1780 | 0 |
| L02-87-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-87-03 | width | 207 | 207 | 0 |
| L02-87-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 87:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 87: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:54:09Z

---

## Section 88: Component Analysis Batch 88

Detailed frame-by-frame comparison for component group 88 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 88 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 88 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 88):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-88-01 | x | 364 | 364 | 0 |
| L02-88-01 | y | 1800 | 1800 | 0 |
| L02-88-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-88-03 | width | 208 | 208 | 0 |
| L02-88-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 88:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 88: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:56:16Z

---

## Section 89: Component Analysis Batch 89

Detailed frame-by-frame comparison for component group 89 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 89 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 89 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 89):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-89-01 | x | 367 | 367 | 0 |
| L02-89-01 | y | 1820 | 1820 | 0 |
| L02-89-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-89-03 | width | 209 | 209 | 0 |
| L02-89-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 89:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 89: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:58:23Z

---

## Section 90: Component Analysis Batch 90

Detailed frame-by-frame comparison for component group 90 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 90 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 90 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 90):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-90-01 | x | 370 | 370 | 0 |
| L02-90-01 | y | 1840 | 1840 | 0 |
| L02-90-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-90-03 | width | 210 | 210 | 0 |
| L02-90-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 90:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 90: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:00:30Z

---

## Section 91: Component Analysis Batch 91

Detailed frame-by-frame comparison for component group 91 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 91 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 91 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 91):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-91-01 | x | 373 | 373 | 0 |
| L02-91-01 | y | 1860 | 1860 | 0 |
| L02-91-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-91-03 | width | 211 | 211 | 0 |
| L02-91-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 91:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 91: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:02:37Z

---

## Section 92: Component Analysis Batch 92

Detailed frame-by-frame comparison for component group 92 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 92 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 92 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 92):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-92-01 | x | 376 | 376 | 0 |
| L02-92-01 | y | 1880 | 1880 | 0 |
| L02-92-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-92-03 | width | 212 | 212 | 0 |
| L02-92-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 92:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 92: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:04:44Z

---

## Section 93: Component Analysis Batch 93

Detailed frame-by-frame comparison for component group 93 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 93 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 93 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 93):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-93-01 | x | 379 | 379 | 0 |
| L02-93-01 | y | 1900 | 1900 | 0 |
| L02-93-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-93-03 | width | 213 | 213 | 0 |
| L02-93-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 93:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 93: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:06:51Z

---

## Section 94: Component Analysis Batch 94

Detailed frame-by-frame comparison for component group 94 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 94 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 94 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 94):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-94-01 | x | 382 | 382 | 0 |
| L02-94-01 | y | 1920 | 1920 | 0 |
| L02-94-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-94-03 | width | 214 | 214 | 0 |
| L02-94-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 94:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 94: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:08:58Z

---

## Section 95: Component Analysis Batch 95

Detailed frame-by-frame comparison for component group 95 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 95 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 95 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 95):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-95-01 | x | 385 | 385 | 0 |
| L02-95-01 | y | 1940 | 1940 | 0 |
| L02-95-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-95-03 | width | 215 | 215 | 0 |
| L02-95-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 95:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 95: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:10:05Z

---

## Section 96: Component Analysis Batch 96

Detailed frame-by-frame comparison for component group 96 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 96 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 96 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 96):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-96-01 | x | 388 | 388 | 0 |
| L02-96-01 | y | 1960 | 1960 | 0 |
| L02-96-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-96-03 | width | 216 | 216 | 0 |
| L02-96-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 96:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 96: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:12:12Z

---

## Section 97: Component Analysis Batch 97

Detailed frame-by-frame comparison for component group 97 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 97 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 97 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 97):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-97-01 | x | 391 | 391 | 0 |
| L02-97-01 | y | 1980 | 1980 | 0 |
| L02-97-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-97-03 | width | 217 | 217 | 0 |
| L02-97-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 97:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 97: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:14:19Z

---

## Section 98: Component Analysis Batch 98

Detailed frame-by-frame comparison for component group 98 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 98 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 98 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 98):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-98-01 | x | 394 | 394 | 0 |
| L02-98-01 | y | 2000 | 2000 | 0 |
| L02-98-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-98-03 | width | 218 | 218 | 0 |
| L02-98-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 98:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 98: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:16:26Z

---

## Section 99: Component Analysis Batch 99

Detailed frame-by-frame comparison for component group 99 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 99 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 99 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 99):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-99-01 | x | 397 | 397 | 0 |
| L02-99-01 | y | 2020 | 2020 | 0 |
| L02-99-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-99-03 | width | 219 | 219 | 0 |
| L02-99-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 99:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 99: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:18:33Z

---

## Section 100: Component Analysis Batch 100

Detailed frame-by-frame comparison for component group 100 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 100 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 100 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 100):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-100-01 | x | 400 | 400 | 0 |
| L02-100-01 | y | 2040 | 2040 | 0 |
| L02-100-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-100-03 | width | 220 | 220 | 0 |
| L02-100-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 100:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 100: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:20:40Z

---

## Section 101: Component Analysis Batch 101

Detailed frame-by-frame comparison for component group 101 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 101 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 101 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 101):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-101-01 | x | 403 | 403 | 0 |
| L02-101-01 | y | 2060 | 2060 | 0 |
| L02-101-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-101-03 | width | 221 | 221 | 0 |
| L02-101-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 101:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 101: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:22:47Z

---

## Section 102: Component Analysis Batch 102

Detailed frame-by-frame comparison for component group 102 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 102 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 102 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 102):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-102-01 | x | 406 | 406 | 0 |
| L02-102-01 | y | 2080 | 2080 | 0 |
| L02-102-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-102-03 | width | 222 | 222 | 0 |
| L02-102-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 102:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 102: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:24:54Z

---

## Section 103: Component Analysis Batch 103

Detailed frame-by-frame comparison for component group 103 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 103 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 103 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 103):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-103-01 | x | 409 | 409 | 0 |
| L02-103-01 | y | 2100 | 2100 | 0 |
| L02-103-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-103-03 | width | 223 | 223 | 0 |
| L02-103-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 103:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 103: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:26:01Z

---

## Section 104: Component Analysis Batch 104

Detailed frame-by-frame comparison for component group 104 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 104 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 104 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 104):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-104-01 | x | 412 | 412 | 0 |
| L02-104-01 | y | 2120 | 2120 | 0 |
| L02-104-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-104-03 | width | 224 | 224 | 0 |
| L02-104-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 104:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 104: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:28:08Z

---

## Section 105: Component Analysis Batch 105

Detailed frame-by-frame comparison for component group 105 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 105 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 105 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 105):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-105-01 | x | 415 | 415 | 0 |
| L02-105-01 | y | 2140 | 2140 | 0 |
| L02-105-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-105-03 | width | 225 | 225 | 0 |
| L02-105-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 105:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 105: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:30:15Z

---

## Section 106: Component Analysis Batch 106

Detailed frame-by-frame comparison for component group 106 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 106 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 106 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 106):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-106-01 | x | 418 | 418 | 0 |
| L02-106-01 | y | 2160 | 2160 | 0 |
| L02-106-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-106-03 | width | 226 | 226 | 0 |
| L02-106-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 106:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 106: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:32:22Z

---

## Section 107: Component Analysis Batch 107

Detailed frame-by-frame comparison for component group 107 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 107 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 107 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 107):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-107-01 | x | 421 | 421 | 0 |
| L02-107-01 | y | 2180 | 2180 | 0 |
| L02-107-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-107-03 | width | 227 | 227 | 0 |
| L02-107-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 107:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 107: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:34:29Z

---

## Section 108: Component Analysis Batch 108

Detailed frame-by-frame comparison for component group 108 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 108 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 108 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 108):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-108-01 | x | 424 | 424 | 0 |
| L02-108-01 | y | 2200 | 2200 | 0 |
| L02-108-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-108-03 | width | 228 | 228 | 0 |
| L02-108-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 108:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 108: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:36:36Z

---

## Section 109: Component Analysis Batch 109

Detailed frame-by-frame comparison for component group 109 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 109 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 109 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 109):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-109-01 | x | 427 | 427 | 0 |
| L02-109-01 | y | 2220 | 2220 | 0 |
| L02-109-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-109-03 | width | 229 | 229 | 0 |
| L02-109-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 109:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 109: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:38:43Z

---

## Section 110: Component Analysis Batch 110

Detailed frame-by-frame comparison for component group 110 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 110 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 110 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 110):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-110-01 | x | 430 | 430 | 0 |
| L02-110-01 | y | 2240 | 2240 | 0 |
| L02-110-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-110-03 | width | 230 | 230 | 0 |
| L02-110-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 110:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 110: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:40:50Z

---

## Section 111: Component Analysis Batch 111

Detailed frame-by-frame comparison for component group 111 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 111 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 111 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 111):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-111-01 | x | 433 | 433 | 0 |
| L02-111-01 | y | 2260 | 2260 | 0 |
| L02-111-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-111-03 | width | 231 | 231 | 0 |
| L02-111-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 111:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 111: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:42:57Z

---

## Section 112: Component Analysis Batch 112

Detailed frame-by-frame comparison for component group 112 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 112 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 112 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 112):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-112-01 | x | 436 | 436 | 0 |
| L02-112-01 | y | 2280 | 2280 | 0 |
| L02-112-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-112-03 | width | 232 | 232 | 0 |
| L02-112-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 112:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 112: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:44:04Z

---

## Section 113: Component Analysis Batch 113

Detailed frame-by-frame comparison for component group 113 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 113 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 113 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 113):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-113-01 | x | 439 | 439 | 0 |
| L02-113-01 | y | 2300 | 2300 | 0 |
| L02-113-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-113-03 | width | 233 | 233 | 0 |
| L02-113-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 113:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 113: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:46:11Z

---

## Section 114: Component Analysis Batch 114

Detailed frame-by-frame comparison for component group 114 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 114 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 114 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 114):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-114-01 | x | 442 | 442 | 0 |
| L02-114-01 | y | 2320 | 2320 | 0 |
| L02-114-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-114-03 | width | 234 | 234 | 0 |
| L02-114-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 114:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 114: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:48:18Z

---

## Section 115: Component Analysis Batch 115

Detailed frame-by-frame comparison for component group 115 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 115 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 115 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 115):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-115-01 | x | 445 | 445 | 0 |
| L02-115-01 | y | 2340 | 2340 | 0 |
| L02-115-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-115-03 | width | 235 | 235 | 0 |
| L02-115-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 115:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 115: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:50:25Z

---

## Section 116: Component Analysis Batch 116

Detailed frame-by-frame comparison for component group 116 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 116 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 116 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 116):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-116-01 | x | 448 | 448 | 0 |
| L02-116-01 | y | 2360 | 2360 | 0 |
| L02-116-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-116-03 | width | 236 | 236 | 0 |
| L02-116-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 116:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 116: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:52:32Z

---

## Section 117: Component Analysis Batch 117

Detailed frame-by-frame comparison for component group 117 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 117 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 117 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 117):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-117-01 | x | 451 | 451 | 0 |
| L02-117-01 | y | 2380 | 2380 | 0 |
| L02-117-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-117-03 | width | 237 | 237 | 0 |
| L02-117-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 117:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 117: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:54:39Z

---

## Section 118: Component Analysis Batch 118

Detailed frame-by-frame comparison for component group 118 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 118 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 118 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 118):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-118-01 | x | 454 | 454 | 0 |
| L02-118-01 | y | 2400 | 2400 | 0 |
| L02-118-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-118-03 | width | 238 | 238 | 0 |
| L02-118-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 118:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 118: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:56:46Z

---

## Section 119: Component Analysis Batch 119

Detailed frame-by-frame comparison for component group 119 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 119 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 119 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 119):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-119-01 | x | 457 | 457 | 0 |
| L02-119-01 | y | 2420 | 2420 | 0 |
| L02-119-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-119-03 | width | 239 | 239 | 0 |
| L02-119-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 119:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 119: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T09:58:53Z

---

## Section 120: Component Analysis Batch 120

Detailed frame-by-frame comparison for component group 120 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 120 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 120 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 120):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-120-01 | x | 460 | 460 | 0 |
| L02-120-01 | y | 2440 | 2440 | 0 |
| L02-120-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-120-03 | width | 200 | 200 | 0 |
| L02-120-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 120:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 120: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:00:00Z

---

## Section 121: Component Analysis Batch 121

Detailed frame-by-frame comparison for component group 121 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 121 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 121 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 121):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-121-01 | x | 463 | 463 | 0 |
| L02-121-01 | y | 2460 | 2460 | 0 |
| L02-121-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-121-03 | width | 201 | 201 | 0 |
| L02-121-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 121:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 121: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:02:07Z

---

## Section 122: Component Analysis Batch 122

Detailed frame-by-frame comparison for component group 122 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 122 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 122 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 122):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-122-01 | x | 466 | 466 | 0 |
| L02-122-01 | y | 2480 | 2480 | 0 |
| L02-122-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-122-03 | width | 202 | 202 | 0 |
| L02-122-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 122:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 122: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:04:14Z

---

## Section 123: Component Analysis Batch 123

Detailed frame-by-frame comparison for component group 123 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 123 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 123 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 123):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-123-01 | x | 469 | 469 | 0 |
| L02-123-01 | y | 2500 | 2500 | 0 |
| L02-123-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-123-03 | width | 203 | 203 | 0 |
| L02-123-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 123:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 123: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:06:21Z

---

## Section 124: Component Analysis Batch 124

Detailed frame-by-frame comparison for component group 124 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 124 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 124 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 124):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-124-01 | x | 472 | 472 | 0 |
| L02-124-01 | y | 2520 | 2520 | 0 |
| L02-124-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-124-03 | width | 204 | 204 | 0 |
| L02-124-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 124:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 124: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:08:28Z

---

## Section 125: Component Analysis Batch 125

Detailed frame-by-frame comparison for component group 125 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 125 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 125 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 125):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-125-01 | x | 475 | 475 | 0 |
| L02-125-01 | y | 2540 | 2540 | 0 |
| L02-125-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-125-03 | width | 205 | 205 | 0 |
| L02-125-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 125:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 125: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:10:35Z

---

## Section 126: Component Analysis Batch 126

Detailed frame-by-frame comparison for component group 126 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 126 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 126 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 126):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-126-01 | x | 478 | 478 | 0 |
| L02-126-01 | y | 2560 | 2560 | 0 |
| L02-126-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-126-03 | width | 206 | 206 | 0 |
| L02-126-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 126:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 126: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:12:42Z

---

## Section 127: Component Analysis Batch 127

Detailed frame-by-frame comparison for component group 127 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 127 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 127 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 127):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-127-01 | x | 481 | 481 | 0 |
| L02-127-01 | y | 2580 | 2580 | 0 |
| L02-127-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-127-03 | width | 207 | 207 | 0 |
| L02-127-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 127:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 127: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:14:49Z

---

## Section 128: Component Analysis Batch 128

Detailed frame-by-frame comparison for component group 128 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 128 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 128 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 128):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-128-01 | x | 484 | 484 | 0 |
| L02-128-01 | y | 2600 | 2600 | 0 |
| L02-128-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-128-03 | width | 208 | 208 | 0 |
| L02-128-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 128:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 128: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:16:56Z

---

## Section 129: Component Analysis Batch 129

Detailed frame-by-frame comparison for component group 129 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 129 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 129 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 129):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-129-01 | x | 487 | 487 | 0 |
| L02-129-01 | y | 2620 | 2620 | 0 |
| L02-129-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-129-03 | width | 209 | 209 | 0 |
| L02-129-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 129:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 129: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:18:03Z

---

## Section 130: Component Analysis Batch 130

Detailed frame-by-frame comparison for component group 130 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 130 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 130 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 130):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-130-01 | x | 490 | 490 | 0 |
| L02-130-01 | y | 2640 | 2640 | 0 |
| L02-130-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-130-03 | width | 210 | 210 | 0 |
| L02-130-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 130:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 130: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:20:10Z

---

## Section 131: Component Analysis Batch 131

Detailed frame-by-frame comparison for component group 131 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 131 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 131 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 131):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-131-01 | x | 493 | 493 | 0 |
| L02-131-01 | y | 2660 | 2660 | 0 |
| L02-131-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-131-03 | width | 211 | 211 | 0 |
| L02-131-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 131:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 131: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:22:17Z

---

## Section 132: Component Analysis Batch 132

Detailed frame-by-frame comparison for component group 132 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 132 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 132 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 132):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-132-01 | x | 496 | 496 | 0 |
| L02-132-01 | y | 2680 | 2680 | 0 |
| L02-132-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-132-03 | width | 212 | 212 | 0 |
| L02-132-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 132:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 132: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:24:24Z

---

## Section 133: Component Analysis Batch 133

Detailed frame-by-frame comparison for component group 133 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 133 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 133 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 133):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-133-01 | x | 499 | 499 | 0 |
| L02-133-01 | y | 2700 | 2700 | 0 |
| L02-133-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-133-03 | width | 213 | 213 | 0 |
| L02-133-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 133:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 133: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:26:31Z

---

## Section 134: Component Analysis Batch 134

Detailed frame-by-frame comparison for component group 134 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 134 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 134 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 134):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-134-01 | x | 502 | 502 | 0 |
| L02-134-01 | y | 2720 | 2720 | 0 |
| L02-134-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-134-03 | width | 214 | 214 | 0 |
| L02-134-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 134:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 134: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:28:38Z

---

## Section 135: Component Analysis Batch 135

Detailed frame-by-frame comparison for component group 135 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 135 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 135 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 135):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-135-01 | x | 505 | 505 | 0 |
| L02-135-01 | y | 2740 | 2740 | 0 |
| L02-135-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-135-03 | width | 215 | 215 | 0 |
| L02-135-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 135:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 135: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:30:45Z

---

## Section 136: Component Analysis Batch 136

Detailed frame-by-frame comparison for component group 136 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 136 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 136 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 136):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-136-01 | x | 508 | 508 | 0 |
| L02-136-01 | y | 2760 | 2760 | 0 |
| L02-136-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-136-03 | width | 216 | 216 | 0 |
| L02-136-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 136:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 136: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:32:52Z

---

## Section 137: Component Analysis Batch 137

Detailed frame-by-frame comparison for component group 137 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 137 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 137 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 137):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-137-01 | x | 511 | 511 | 0 |
| L02-137-01 | y | 2780 | 2780 | 0 |
| L02-137-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-137-03 | width | 217 | 217 | 0 |
| L02-137-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 137:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 137: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:34:59Z

---

## Section 138: Component Analysis Batch 138

Detailed frame-by-frame comparison for component group 138 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 138 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 138 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 138):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-138-01 | x | 514 | 514 | 0 |
| L02-138-01 | y | 2800 | 2800 | 0 |
| L02-138-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-138-03 | width | 218 | 218 | 0 |
| L02-138-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 138:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 138: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:36:06Z

---

## Section 139: Component Analysis Batch 139

Detailed frame-by-frame comparison for component group 139 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 139 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 139 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 139):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-139-01 | x | 517 | 517 | 0 |
| L02-139-01 | y | 2820 | 2820 | 0 |
| L02-139-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-139-03 | width | 219 | 219 | 0 |
| L02-139-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 139:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 139: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:38:13Z

---

## Section 140: Component Analysis Batch 140

Detailed frame-by-frame comparison for component group 140 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 140 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 140 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 140):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-140-01 | x | 520 | 520 | 0 |
| L02-140-01 | y | 2840 | 2840 | 0 |
| L02-140-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-140-03 | width | 220 | 220 | 0 |
| L02-140-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 140:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 140: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:40:20Z

---

## Section 141: Component Analysis Batch 141

Detailed frame-by-frame comparison for component group 141 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 141 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 141 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 141):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-141-01 | x | 523 | 523 | 0 |
| L02-141-01 | y | 2860 | 2860 | 0 |
| L02-141-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-141-03 | width | 221 | 221 | 0 |
| L02-141-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 141:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 141: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:42:27Z

---

## Section 142: Component Analysis Batch 142

Detailed frame-by-frame comparison for component group 142 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 142 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 142 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 142):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-142-01 | x | 526 | 526 | 0 |
| L02-142-01 | y | 2880 | 2880 | 0 |
| L02-142-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-142-03 | width | 222 | 222 | 0 |
| L02-142-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 142:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 142: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:44:34Z

---

## Section 143: Component Analysis Batch 143

Detailed frame-by-frame comparison for component group 143 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 143 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 143 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 143):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-143-01 | x | 529 | 529 | 0 |
| L02-143-01 | y | 2900 | 2900 | 0 |
| L02-143-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-143-03 | width | 223 | 223 | 0 |
| L02-143-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 143:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 143: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:46:41Z

---

## Section 144: Component Analysis Batch 144

Detailed frame-by-frame comparison for component group 144 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 144 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 144 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 144):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-144-01 | x | 532 | 532 | 0 |
| L02-144-01 | y | 2920 | 2920 | 0 |
| L02-144-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-144-03 | width | 224 | 224 | 0 |
| L02-144-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 144:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 144: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:48:48Z

---

## Section 145: Component Analysis Batch 145

Detailed frame-by-frame comparison for component group 145 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 145 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 145 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 145):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-145-01 | x | 535 | 535 | 0 |
| L02-145-01 | y | 2940 | 2940 | 0 |
| L02-145-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-145-03 | width | 225 | 225 | 0 |
| L02-145-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 145:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 145: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:50:55Z

---

## Section 146: Component Analysis Batch 146

Detailed frame-by-frame comparison for component group 146 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 146 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 146 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 146):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-146-01 | x | 538 | 538 | 0 |
| L02-146-01 | y | 2960 | 2960 | 0 |
| L02-146-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-146-03 | width | 226 | 226 | 0 |
| L02-146-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 146:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 146: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:52:02Z

---

## Section 147: Component Analysis Batch 147

Detailed frame-by-frame comparison for component group 147 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 147 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 147 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 147):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-147-01 | x | 541 | 541 | 0 |
| L02-147-01 | y | 2980 | 2980 | 0 |
| L02-147-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-147-03 | width | 227 | 227 | 0 |
| L02-147-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 147:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 147: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:54:09Z

---

## Section 148: Component Analysis Batch 148

Detailed frame-by-frame comparison for component group 148 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 148 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 148 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 148):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-148-01 | x | 544 | 544 | 0 |
| L02-148-01 | y | 3000 | 3000 | 0 |
| L02-148-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-148-03 | width | 228 | 228 | 0 |
| L02-148-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 148:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 148: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:56:16Z

---

## Section 149: Component Analysis Batch 149

Detailed frame-by-frame comparison for component group 149 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 149 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 149 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 149):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-149-01 | x | 547 | 547 | 0 |
| L02-149-01 | y | 3020 | 3020 | 0 |
| L02-149-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-149-03 | width | 229 | 229 | 0 |
| L02-149-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 149:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 149: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:58:23Z

---

## Section 150: Component Analysis Batch 150

Detailed frame-by-frame comparison for component group 150 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 150 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 150 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 150):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-150-01 | x | 550 | 550 | 0 |
| L02-150-01 | y | 3040 | 3040 | 0 |
| L02-150-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-150-03 | width | 230 | 230 | 0 |
| L02-150-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 150:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 150: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:00:30Z

---

## Section 151: Component Analysis Batch 151

Detailed frame-by-frame comparison for component group 151 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 151 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 151 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 151):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-151-01 | x | 553 | 553 | 0 |
| L02-151-01 | y | 3060 | 3060 | 0 |
| L02-151-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-151-03 | width | 231 | 231 | 0 |
| L02-151-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 151:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 151: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:02:37Z

---

## Section 152: Component Analysis Batch 152

Detailed frame-by-frame comparison for component group 152 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 152 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 152 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 152):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-152-01 | x | 556 | 556 | 0 |
| L02-152-01 | y | 3080 | 3080 | 0 |
| L02-152-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-152-03 | width | 232 | 232 | 0 |
| L02-152-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 152:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 152: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:04:44Z

---

## Section 153: Component Analysis Batch 153

Detailed frame-by-frame comparison for component group 153 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 153 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 153 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 153):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-153-01 | x | 559 | 559 | 0 |
| L02-153-01 | y | 3100 | 3100 | 0 |
| L02-153-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-153-03 | width | 233 | 233 | 0 |
| L02-153-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 153:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 153: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:06:51Z

---

## Section 154: Component Analysis Batch 154

Detailed frame-by-frame comparison for component group 154 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 154 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 154 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 154):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-154-01 | x | 562 | 562 | 0 |
| L02-154-01 | y | 3120 | 3120 | 0 |
| L02-154-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-154-03 | width | 234 | 234 | 0 |
| L02-154-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 154:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 154: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:08:58Z

---

## Section 155: Component Analysis Batch 155

Detailed frame-by-frame comparison for component group 155 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 155 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 155 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 155):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-155-01 | x | 565 | 565 | 0 |
| L02-155-01 | y | 3140 | 3140 | 0 |
| L02-155-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-155-03 | width | 235 | 235 | 0 |
| L02-155-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 155:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 155: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:10:05Z

---

## Section 156: Component Analysis Batch 156

Detailed frame-by-frame comparison for component group 156 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 156 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 156 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 156):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-156-01 | x | 568 | 568 | 0 |
| L02-156-01 | y | 3160 | 3160 | 0 |
| L02-156-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-156-03 | width | 236 | 236 | 0 |
| L02-156-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 156:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 156: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:12:12Z

---

## Section 157: Component Analysis Batch 157

Detailed frame-by-frame comparison for component group 157 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 157 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 157 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 157):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-157-01 | x | 571 | 571 | 0 |
| L02-157-01 | y | 3180 | 3180 | 0 |
| L02-157-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-157-03 | width | 237 | 237 | 0 |
| L02-157-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 157:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 157: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:14:19Z

---

## Section 158: Component Analysis Batch 158

Detailed frame-by-frame comparison for component group 158 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 158 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 158 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 158):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-158-01 | x | 574 | 574 | 0 |
| L02-158-01 | y | 3200 | 3200 | 0 |
| L02-158-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-158-03 | width | 238 | 238 | 0 |
| L02-158-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 158:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 158: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:16:26Z

---

## Section 159: Component Analysis Batch 159

Detailed frame-by-frame comparison for component group 159 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 159 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 159 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 159):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-159-01 | x | 577 | 577 | 0 |
| L02-159-01 | y | 3220 | 3220 | 0 |
| L02-159-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-159-03 | width | 239 | 239 | 0 |
| L02-159-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 159:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 159: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:18:33Z

---

## Section 160: Component Analysis Batch 160

Detailed frame-by-frame comparison for component group 160 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 160 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 160 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 160):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-160-01 | x | 580 | 580 | 0 |
| L02-160-01 | y | 3240 | 3240 | 0 |
| L02-160-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-160-03 | width | 200 | 200 | 0 |
| L02-160-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 160:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 160: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:20:40Z

---

## Section 161: Component Analysis Batch 161

Detailed frame-by-frame comparison for component group 161 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 161 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 161 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 161):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-161-01 | x | 583 | 583 | 0 |
| L02-161-01 | y | 3260 | 3260 | 0 |
| L02-161-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-161-03 | width | 201 | 201 | 0 |
| L02-161-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 161:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 161: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:22:47Z

---

## Section 162: Component Analysis Batch 162

Detailed frame-by-frame comparison for component group 162 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 162 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 162 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 162):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-162-01 | x | 586 | 586 | 0 |
| L02-162-01 | y | 3280 | 3280 | 0 |
| L02-162-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-162-03 | width | 202 | 202 | 0 |
| L02-162-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 162:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 162: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:24:54Z

---

## Section 163: Component Analysis Batch 163

Detailed frame-by-frame comparison for component group 163 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 163 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 163 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 163):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-163-01 | x | 589 | 589 | 0 |
| L02-163-01 | y | 3300 | 3300 | 0 |
| L02-163-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-163-03 | width | 203 | 203 | 0 |
| L02-163-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 163:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 163: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:26:01Z

---

## Section 164: Component Analysis Batch 164

Detailed frame-by-frame comparison for component group 164 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 164 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 164 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 164):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-164-01 | x | 592 | 592 | 0 |
| L02-164-01 | y | 3320 | 3320 | 0 |
| L02-164-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-164-03 | width | 204 | 204 | 0 |
| L02-164-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 164:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 164: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:28:08Z

---

## Section 165: Component Analysis Batch 165

Detailed frame-by-frame comparison for component group 165 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 165 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 165 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 165):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-165-01 | x | 595 | 595 | 0 |
| L02-165-01 | y | 3340 | 3340 | 0 |
| L02-165-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-165-03 | width | 205 | 205 | 0 |
| L02-165-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 165:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 165: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:30:15Z

---

## Section 166: Component Analysis Batch 166

Detailed frame-by-frame comparison for component group 166 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 166 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 166 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 166):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-166-01 | x | 598 | 598 | 0 |
| L02-166-01 | y | 3360 | 3360 | 0 |
| L02-166-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-166-03 | width | 206 | 206 | 0 |
| L02-166-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 166:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 166: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:32:22Z

---

## Section 167: Component Analysis Batch 167

Detailed frame-by-frame comparison for component group 167 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 167 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 167 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 167):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-167-01 | x | 601 | 601 | 0 |
| L02-167-01 | y | 3380 | 3380 | 0 |
| L02-167-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-167-03 | width | 207 | 207 | 0 |
| L02-167-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 167:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 167: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:34:29Z

---

## Section 168: Component Analysis Batch 168

Detailed frame-by-frame comparison for component group 168 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 168 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 168 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 168):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-168-01 | x | 604 | 604 | 0 |
| L02-168-01 | y | 3400 | 3400 | 0 |
| L02-168-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-168-03 | width | 208 | 208 | 0 |
| L02-168-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 168:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 168: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:36:36Z

---

## Section 169: Component Analysis Batch 169

Detailed frame-by-frame comparison for component group 169 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 169 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 169 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 169):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-169-01 | x | 607 | 607 | 0 |
| L02-169-01 | y | 3420 | 3420 | 0 |
| L02-169-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-169-03 | width | 209 | 209 | 0 |
| L02-169-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 169:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 169: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:38:43Z

---

## Section 170: Component Analysis Batch 170

Detailed frame-by-frame comparison for component group 170 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 170 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 170 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 170):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-170-01 | x | 610 | 610 | 0 |
| L02-170-01 | y | 3440 | 3440 | 0 |
| L02-170-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-170-03 | width | 210 | 210 | 0 |
| L02-170-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 170:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 170: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:40:50Z

---

## Section 171: Component Analysis Batch 171

Detailed frame-by-frame comparison for component group 171 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 171 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 171 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 171):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-171-01 | x | 613 | 613 | 0 |
| L02-171-01 | y | 3460 | 3460 | 0 |
| L02-171-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-171-03 | width | 211 | 211 | 0 |
| L02-171-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 171:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 171: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:42:57Z

---

## Section 172: Component Analysis Batch 172

Detailed frame-by-frame comparison for component group 172 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 172 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 172 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 172):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-172-01 | x | 616 | 616 | 0 |
| L02-172-01 | y | 3480 | 3480 | 0 |
| L02-172-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-172-03 | width | 212 | 212 | 0 |
| L02-172-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 172:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 172: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:44:04Z

---

## Section 173: Component Analysis Batch 173

Detailed frame-by-frame comparison for component group 173 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 173 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 173 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 173):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-173-01 | x | 619 | 619 | 0 |
| L02-173-01 | y | 3500 | 3500 | 0 |
| L02-173-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-173-03 | width | 213 | 213 | 0 |
| L02-173-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 173:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 173: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:46:11Z

---

## Section 174: Component Analysis Batch 174

Detailed frame-by-frame comparison for component group 174 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 174 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 174 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 174):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-174-01 | x | 622 | 622 | 0 |
| L02-174-01 | y | 3520 | 3520 | 0 |
| L02-174-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-174-03 | width | 214 | 214 | 0 |
| L02-174-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 174:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 174: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:48:18Z

---

## Section 175: Component Analysis Batch 175

Detailed frame-by-frame comparison for component group 175 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 175 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 175 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 175):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-175-01 | x | 625 | 625 | 0 |
| L02-175-01 | y | 3540 | 3540 | 0 |
| L02-175-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-175-03 | width | 215 | 215 | 0 |
| L02-175-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 175:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 175: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:50:25Z

---

## Section 176: Component Analysis Batch 176

Detailed frame-by-frame comparison for component group 176 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 176 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 176 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 176):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-176-01 | x | 628 | 628 | 0 |
| L02-176-01 | y | 3560 | 3560 | 0 |
| L02-176-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-176-03 | width | 216 | 216 | 0 |
| L02-176-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 176:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 176: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:52:32Z

---

## Section 177: Component Analysis Batch 177

Detailed frame-by-frame comparison for component group 177 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 177 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 177 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 177):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-177-01 | x | 631 | 631 | 0 |
| L02-177-01 | y | 3580 | 3580 | 0 |
| L02-177-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-177-03 | width | 217 | 217 | 0 |
| L02-177-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 177:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 177: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:54:39Z

---

## Section 178: Component Analysis Batch 178

Detailed frame-by-frame comparison for component group 178 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 178 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 178 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 178):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-178-01 | x | 634 | 634 | 0 |
| L02-178-01 | y | 3600 | 3600 | 0 |
| L02-178-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-178-03 | width | 218 | 218 | 0 |
| L02-178-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 178:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 178: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:56:46Z

---

## Section 179: Component Analysis Batch 179

Detailed frame-by-frame comparison for component group 179 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 179 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 179 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 179):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-179-01 | x | 637 | 637 | 0 |
| L02-179-01 | y | 3620 | 3620 | 0 |
| L02-179-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-179-03 | width | 219 | 219 | 0 |
| L02-179-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 179:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 179: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T10:58:53Z

---

## Section 180: Component Analysis Batch 180

Detailed frame-by-frame comparison for component group 180 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 180 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 180 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 180):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-180-01 | x | 640 | 640 | 0 |
| L02-180-01 | y | 3640 | 3640 | 0 |
| L02-180-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-180-03 | width | 220 | 220 | 0 |
| L02-180-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 180:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 180: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:00:00Z

---

## Section 181: Component Analysis Batch 181

Detailed frame-by-frame comparison for component group 181 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 181 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 181 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 181):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-181-01 | x | 643 | 643 | 0 |
| L02-181-01 | y | 3660 | 3660 | 0 |
| L02-181-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-181-03 | width | 221 | 221 | 0 |
| L02-181-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 181:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 181: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:02:07Z

---

## Section 182: Component Analysis Batch 182

Detailed frame-by-frame comparison for component group 182 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 182 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 182 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 182):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-182-01 | x | 646 | 646 | 0 |
| L02-182-01 | y | 3680 | 3680 | 0 |
| L02-182-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-182-03 | width | 222 | 222 | 0 |
| L02-182-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 182:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 182: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:04:14Z

---

## Section 183: Component Analysis Batch 183

Detailed frame-by-frame comparison for component group 183 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 183 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 183 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 183):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-183-01 | x | 649 | 649 | 0 |
| L02-183-01 | y | 3700 | 3700 | 0 |
| L02-183-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-183-03 | width | 223 | 223 | 0 |
| L02-183-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 183:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 183: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:06:21Z

---

## Section 184: Component Analysis Batch 184

Detailed frame-by-frame comparison for component group 184 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 184 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 184 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 184):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-184-01 | x | 652 | 652 | 0 |
| L02-184-01 | y | 3720 | 3720 | 0 |
| L02-184-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-184-03 | width | 224 | 224 | 0 |
| L02-184-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 184:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 184: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:08:28Z

---

## Section 185: Component Analysis Batch 185

Detailed frame-by-frame comparison for component group 185 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 185 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 185 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 185):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-185-01 | x | 655 | 655 | 0 |
| L02-185-01 | y | 3740 | 3740 | 0 |
| L02-185-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-185-03 | width | 225 | 225 | 0 |
| L02-185-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 185:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 185: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:10:35Z

---

## Section 186: Component Analysis Batch 186

Detailed frame-by-frame comparison for component group 186 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 186 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 186 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 186):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-186-01 | x | 658 | 658 | 0 |
| L02-186-01 | y | 3760 | 3760 | 0 |
| L02-186-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-186-03 | width | 226 | 226 | 0 |
| L02-186-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 186:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 186: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:12:42Z

---

## Section 187: Component Analysis Batch 187

Detailed frame-by-frame comparison for component group 187 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 187 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 187 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 187):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-187-01 | x | 661 | 661 | 0 |
| L02-187-01 | y | 3780 | 3780 | 0 |
| L02-187-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-187-03 | width | 227 | 227 | 0 |
| L02-187-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 187:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 187: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:14:49Z

---

## Section 188: Component Analysis Batch 188

Detailed frame-by-frame comparison for component group 188 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 188 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 188 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 188):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-188-01 | x | 664 | 664 | 0 |
| L02-188-01 | y | 3800 | 3800 | 0 |
| L02-188-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-188-03 | width | 228 | 228 | 0 |
| L02-188-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 188:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 188: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:16:56Z

---

## Section 189: Component Analysis Batch 189

Detailed frame-by-frame comparison for component group 189 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 189 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 189 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 189):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-189-01 | x | 667 | 667 | 0 |
| L02-189-01 | y | 3820 | 3820 | 0 |
| L02-189-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-189-03 | width | 229 | 229 | 0 |
| L02-189-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 189:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 189: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:18:03Z

---

## Section 190: Component Analysis Batch 190

Detailed frame-by-frame comparison for component group 190 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 190 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 190 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 190):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-190-01 | x | 670 | 670 | 0 |
| L02-190-01 | y | 3840 | 3840 | 0 |
| L02-190-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-190-03 | width | 230 | 230 | 0 |
| L02-190-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 190:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 190: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:20:10Z

---

## Section 191: Component Analysis Batch 191

Detailed frame-by-frame comparison for component group 191 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 191 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 191 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 191):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-191-01 | x | 673 | 673 | 0 |
| L02-191-01 | y | 3860 | 3860 | 0 |
| L02-191-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-191-03 | width | 231 | 231 | 0 |
| L02-191-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 191:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 191: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:22:17Z

---

## Section 192: Component Analysis Batch 192

Detailed frame-by-frame comparison for component group 192 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 192 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 192 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 192):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-192-01 | x | 676 | 676 | 0 |
| L02-192-01 | y | 3880 | 3880 | 0 |
| L02-192-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-192-03 | width | 232 | 232 | 0 |
| L02-192-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 192:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 192: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:24:24Z

---

## Section 193: Component Analysis Batch 193

Detailed frame-by-frame comparison for component group 193 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 193 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 193 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 193):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-193-01 | x | 679 | 679 | 0 |
| L02-193-01 | y | 3900 | 3900 | 0 |
| L02-193-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-193-03 | width | 233 | 233 | 0 |
| L02-193-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 193:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 193: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:26:31Z

---

## Section 194: Component Analysis Batch 194

Detailed frame-by-frame comparison for component group 194 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 194 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 194 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 194):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-194-01 | x | 682 | 682 | 0 |
| L02-194-01 | y | 3920 | 3920 | 0 |
| L02-194-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-194-03 | width | 234 | 234 | 0 |
| L02-194-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 194:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 194: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:28:38Z

---

## Section 195: Component Analysis Batch 195

Detailed frame-by-frame comparison for component group 195 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 195 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 195 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 195):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-195-01 | x | 685 | 685 | 0 |
| L02-195-01 | y | 3940 | 3940 | 0 |
| L02-195-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-195-03 | width | 235 | 235 | 0 |
| L02-195-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 195:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 195: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:30:45Z

---

## Section 196: Component Analysis Batch 196

Detailed frame-by-frame comparison for component group 196 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 196 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 196 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 196):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-196-01 | x | 688 | 688 | 0 |
| L02-196-01 | y | 3960 | 3960 | 0 |
| L02-196-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-196-03 | width | 236 | 236 | 0 |
| L02-196-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 196:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 196: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:32:52Z

---

## Section 197: Component Analysis Batch 197

Detailed frame-by-frame comparison for component group 197 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 197 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 197 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 197):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-197-01 | x | 691 | 691 | 0 |
| L02-197-01 | y | 3980 | 3980 | 0 |
| L02-197-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-197-03 | width | 237 | 237 | 0 |
| L02-197-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 197:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 197: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:34:59Z

---

## Section 198: Component Analysis Batch 198

Detailed frame-by-frame comparison for component group 198 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 198 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 198 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 198):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-198-01 | x | 694 | 694 | 0 |
| L02-198-01 | y | 4000 | 4000 | 0 |
| L02-198-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-198-03 | width | 238 | 238 | 0 |
| L02-198-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 198:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 198: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:36:06Z

---

## Section 199: Component Analysis Batch 199

Detailed frame-by-frame comparison for component group 199 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 199 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 199 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 199):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-199-01 | x | 697 | 697 | 0 |
| L02-199-01 | y | 4020 | 4020 | 0 |
| L02-199-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-199-03 | width | 239 | 239 | 0 |
| L02-199-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 199:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 199: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:38:13Z

---

## Section 200: Component Analysis Batch 200

Detailed frame-by-frame comparison for component group 200 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 200 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 200 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 200):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-200-01 | x | 700 | 700 | 0 |
| L02-200-01 | y | 4040 | 4040 | 0 |
| L02-200-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-200-03 | width | 200 | 200 | 0 |
| L02-200-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 200:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 200: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:40:20Z

---

## Section 201: Component Analysis Batch 201

Detailed frame-by-frame comparison for component group 201 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 201 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 201 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 201):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-201-01 | x | 703 | 703 | 0 |
| L02-201-01 | y | 4060 | 4060 | 0 |
| L02-201-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-201-03 | width | 201 | 201 | 0 |
| L02-201-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 201:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 201: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:42:27Z

---

## Section 202: Component Analysis Batch 202

Detailed frame-by-frame comparison for component group 202 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 202 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 202 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 202):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-202-01 | x | 706 | 706 | 0 |
| L02-202-01 | y | 4080 | 4080 | 0 |
| L02-202-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-202-03 | width | 202 | 202 | 0 |
| L02-202-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 202:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 202: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:44:34Z

---

## Section 203: Component Analysis Batch 203

Detailed frame-by-frame comparison for component group 203 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 203 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 203 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 203):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-203-01 | x | 709 | 709 | 0 |
| L02-203-01 | y | 4100 | 4100 | 0 |
| L02-203-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-203-03 | width | 203 | 203 | 0 |
| L02-203-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 203:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 203: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:46:41Z

---

## Section 204: Component Analysis Batch 204

Detailed frame-by-frame comparison for component group 204 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 204 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 204 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 204):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-204-01 | x | 712 | 712 | 0 |
| L02-204-01 | y | 4120 | 4120 | 0 |
| L02-204-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-204-03 | width | 204 | 204 | 0 |
| L02-204-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 204:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 204: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:48:48Z

---

## Section 205: Component Analysis Batch 205

Detailed frame-by-frame comparison for component group 205 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 205 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 205 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 205):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-205-01 | x | 715 | 715 | 0 |
| L02-205-01 | y | 4140 | 4140 | 0 |
| L02-205-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-205-03 | width | 205 | 205 | 0 |
| L02-205-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 205:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 205: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:50:55Z

---

## Section 206: Component Analysis Batch 206

Detailed frame-by-frame comparison for component group 206 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 206 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 206 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 206):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-206-01 | x | 718 | 718 | 0 |
| L02-206-01 | y | 4160 | 4160 | 0 |
| L02-206-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-206-03 | width | 206 | 206 | 0 |
| L02-206-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 206:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 206: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:52:02Z

---

## Section 207: Component Analysis Batch 207

Detailed frame-by-frame comparison for component group 207 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 207 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 207 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 207):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-207-01 | x | 721 | 721 | 0 |
| L02-207-01 | y | 4180 | 4180 | 0 |
| L02-207-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-207-03 | width | 207 | 207 | 0 |
| L02-207-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 207:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 207: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:54:09Z

---

## Section 208: Component Analysis Batch 208

Detailed frame-by-frame comparison for component group 208 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 208 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 208 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 208):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-208-01 | x | 724 | 724 | 0 |
| L02-208-01 | y | 4200 | 4200 | 0 |
| L02-208-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-208-03 | width | 208 | 208 | 0 |
| L02-208-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 208:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 208: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:56:16Z

---

## Section 209: Component Analysis Batch 209

Detailed frame-by-frame comparison for component group 209 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 209 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 209 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 209):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-209-01 | x | 727 | 727 | 0 |
| L02-209-01 | y | 4220 | 4220 | 0 |
| L02-209-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-209-03 | width | 209 | 209 | 0 |
| L02-209-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 209:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 209: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:58:23Z

---

## Section 210: Component Analysis Batch 210

Detailed frame-by-frame comparison for component group 210 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 210 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 210 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 210):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-210-01 | x | 730 | 730 | 0 |
| L02-210-01 | y | 4240 | 4240 | 0 |
| L02-210-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-210-03 | width | 210 | 210 | 0 |
| L02-210-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 210:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 210: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:00:30Z

---

## Section 211: Component Analysis Batch 211

Detailed frame-by-frame comparison for component group 211 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 211 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 211 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 211):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-211-01 | x | 733 | 733 | 0 |
| L02-211-01 | y | 4260 | 4260 | 0 |
| L02-211-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-211-03 | width | 211 | 211 | 0 |
| L02-211-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 211:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 211: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:02:37Z

---

## Section 212: Component Analysis Batch 212

Detailed frame-by-frame comparison for component group 212 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 212 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 212 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 212):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-212-01 | x | 736 | 736 | 0 |
| L02-212-01 | y | 4280 | 4280 | 0 |
| L02-212-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-212-03 | width | 212 | 212 | 0 |
| L02-212-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 212:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 212: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:04:44Z

---

## Section 213: Component Analysis Batch 213

Detailed frame-by-frame comparison for component group 213 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 213 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 213 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 213):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-213-01 | x | 739 | 739 | 0 |
| L02-213-01 | y | 4300 | 4300 | 0 |
| L02-213-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-213-03 | width | 213 | 213 | 0 |
| L02-213-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 213:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 213: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:06:51Z

---

## Section 214: Component Analysis Batch 214

Detailed frame-by-frame comparison for component group 214 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 214 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 214 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 214):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-214-01 | x | 742 | 742 | 0 |
| L02-214-01 | y | 4320 | 4320 | 0 |
| L02-214-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-214-03 | width | 214 | 214 | 0 |
| L02-214-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 214:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 214: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:08:58Z

---

## Section 215: Component Analysis Batch 215

Detailed frame-by-frame comparison for component group 215 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 215 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 215 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 215):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-215-01 | x | 745 | 745 | 0 |
| L02-215-01 | y | 4340 | 4340 | 0 |
| L02-215-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-215-03 | width | 215 | 215 | 0 |
| L02-215-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 215:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 215: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:10:05Z

---

## Section 216: Component Analysis Batch 216

Detailed frame-by-frame comparison for component group 216 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 216 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 216 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 216):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-216-01 | x | 748 | 748 | 0 |
| L02-216-01 | y | 4360 | 4360 | 0 |
| L02-216-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-216-03 | width | 216 | 216 | 0 |
| L02-216-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 216:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 216: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:12:12Z

---

## Section 217: Component Analysis Batch 217

Detailed frame-by-frame comparison for component group 217 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 217 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 217 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 217):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-217-01 | x | 751 | 751 | 0 |
| L02-217-01 | y | 4380 | 4380 | 0 |
| L02-217-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-217-03 | width | 217 | 217 | 0 |
| L02-217-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 217:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 217: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:14:19Z

---

## Section 218: Component Analysis Batch 218

Detailed frame-by-frame comparison for component group 218 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 218 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 218 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 218):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-218-01 | x | 754 | 754 | 0 |
| L02-218-01 | y | 4400 | 4400 | 0 |
| L02-218-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-218-03 | width | 218 | 218 | 0 |
| L02-218-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 218:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 218: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:16:26Z

---

## Section 219: Component Analysis Batch 219

Detailed frame-by-frame comparison for component group 219 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 219 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 219 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 219):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-219-01 | x | 757 | 757 | 0 |
| L02-219-01 | y | 4420 | 4420 | 0 |
| L02-219-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-219-03 | width | 219 | 219 | 0 |
| L02-219-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 219:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 219: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:18:33Z

---

## Section 220: Component Analysis Batch 220

Detailed frame-by-frame comparison for component group 220 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 220 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 220 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 220):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-220-01 | x | 760 | 760 | 0 |
| L02-220-01 | y | 4440 | 4440 | 0 |
| L02-220-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-220-03 | width | 220 | 220 | 0 |
| L02-220-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 220:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 220: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:20:40Z

---

## Section 221: Component Analysis Batch 221

Detailed frame-by-frame comparison for component group 221 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 221 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 221 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 221):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-221-01 | x | 763 | 763 | 0 |
| L02-221-01 | y | 4460 | 4460 | 0 |
| L02-221-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-221-03 | width | 221 | 221 | 0 |
| L02-221-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 221:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 221: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:22:47Z

---

## Section 222: Component Analysis Batch 222

Detailed frame-by-frame comparison for component group 222 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 222 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 222 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 222):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-222-01 | x | 766 | 766 | 0 |
| L02-222-01 | y | 4480 | 4480 | 0 |
| L02-222-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-222-03 | width | 222 | 222 | 0 |
| L02-222-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 222:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 222: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:24:54Z

---

## Section 223: Component Analysis Batch 223

Detailed frame-by-frame comparison for component group 223 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 223 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 223 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 223):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-223-01 | x | 769 | 769 | 0 |
| L02-223-01 | y | 4500 | 4500 | 0 |
| L02-223-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-223-03 | width | 223 | 223 | 0 |
| L02-223-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 223:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 223: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:26:01Z

---

## Section 224: Component Analysis Batch 224

Detailed frame-by-frame comparison for component group 224 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 224 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 224 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 224):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-224-01 | x | 772 | 772 | 0 |
| L02-224-01 | y | 4520 | 4520 | 0 |
| L02-224-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-224-03 | width | 224 | 224 | 0 |
| L02-224-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 224:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 224: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:28:08Z

---

## Section 225: Component Analysis Batch 225

Detailed frame-by-frame comparison for component group 225 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 225 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 225 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 225):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-225-01 | x | 775 | 775 | 0 |
| L02-225-01 | y | 4540 | 4540 | 0 |
| L02-225-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-225-03 | width | 225 | 225 | 0 |
| L02-225-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 225:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 225: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:30:15Z

---

## Section 226: Component Analysis Batch 226

Detailed frame-by-frame comparison for component group 226 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 226 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 226 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 226):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-226-01 | x | 778 | 778 | 0 |
| L02-226-01 | y | 4560 | 4560 | 0 |
| L02-226-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-226-03 | width | 226 | 226 | 0 |
| L02-226-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 226:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 226: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:32:22Z

---

## Section 227: Component Analysis Batch 227

Detailed frame-by-frame comparison for component group 227 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 227 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 227 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 227):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-227-01 | x | 781 | 781 | 0 |
| L02-227-01 | y | 4580 | 4580 | 0 |
| L02-227-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-227-03 | width | 227 | 227 | 0 |
| L02-227-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 227:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 227: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:34:29Z

---

## Section 228: Component Analysis Batch 228

Detailed frame-by-frame comparison for component group 228 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 228 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 228 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 228):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-228-01 | x | 784 | 784 | 0 |
| L02-228-01 | y | 4600 | 4600 | 0 |
| L02-228-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-228-03 | width | 228 | 228 | 0 |
| L02-228-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 228:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 228: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:36:36Z

---

## Section 229: Component Analysis Batch 229

Detailed frame-by-frame comparison for component group 229 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 229 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 229 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 229):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-229-01 | x | 787 | 787 | 0 |
| L02-229-01 | y | 4620 | 4620 | 0 |
| L02-229-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-229-03 | width | 229 | 229 | 0 |
| L02-229-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 229:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 229: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:38:43Z

---

## Section 230: Component Analysis Batch 230

Detailed frame-by-frame comparison for component group 230 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 230 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 230 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 230):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-230-01 | x | 790 | 790 | 0 |
| L02-230-01 | y | 4640 | 4640 | 0 |
| L02-230-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-230-03 | width | 230 | 230 | 0 |
| L02-230-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 230:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 230: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:40:50Z

---

## Section 231: Component Analysis Batch 231

Detailed frame-by-frame comparison for component group 231 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 231 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 231 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 231):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-231-01 | x | 793 | 793 | 0 |
| L02-231-01 | y | 4660 | 4660 | 0 |
| L02-231-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-231-03 | width | 231 | 231 | 0 |
| L02-231-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 231:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 231: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:42:57Z

---

## Section 232: Component Analysis Batch 232

Detailed frame-by-frame comparison for component group 232 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 232 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 232 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 232):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-232-01 | x | 796 | 796 | 0 |
| L02-232-01 | y | 4680 | 4680 | 0 |
| L02-232-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-232-03 | width | 232 | 232 | 0 |
| L02-232-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 232:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 232: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:44:04Z

---

## Section 233: Component Analysis Batch 233

Detailed frame-by-frame comparison for component group 233 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 233 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 233 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 233):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-233-01 | x | 799 | 799 | 0 |
| L02-233-01 | y | 4700 | 4700 | 0 |
| L02-233-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-233-03 | width | 233 | 233 | 0 |
| L02-233-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 233:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 233: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:46:11Z

---

## Section 234: Component Analysis Batch 234

Detailed frame-by-frame comparison for component group 234 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 234 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 234 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 234):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-234-01 | x | 802 | 802 | 0 |
| L02-234-01 | y | 4720 | 4720 | 0 |
| L02-234-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-234-03 | width | 234 | 234 | 0 |
| L02-234-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 234:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 234: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:48:18Z

---

## Section 235: Component Analysis Batch 235

Detailed frame-by-frame comparison for component group 235 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 235 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 235 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 235):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-235-01 | x | 805 | 805 | 0 |
| L02-235-01 | y | 4740 | 4740 | 0 |
| L02-235-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-235-03 | width | 235 | 235 | 0 |
| L02-235-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 235:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 235: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:50:25Z

---

## Section 236: Component Analysis Batch 236

Detailed frame-by-frame comparison for component group 236 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 236 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 236 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 236):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-236-01 | x | 808 | 808 | 0 |
| L02-236-01 | y | 4760 | 4760 | 0 |
| L02-236-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-236-03 | width | 236 | 236 | 0 |
| L02-236-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 236:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 236: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:52:32Z

---

## Section 237: Component Analysis Batch 237

Detailed frame-by-frame comparison for component group 237 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 237 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 237 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 237):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-237-01 | x | 811 | 811 | 0 |
| L02-237-01 | y | 4780 | 4780 | 0 |
| L02-237-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-237-03 | width | 237 | 237 | 0 |
| L02-237-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 237:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 237: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:54:39Z

---

## Section 238: Component Analysis Batch 238

Detailed frame-by-frame comparison for component group 238 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 238 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 238 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 238):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-238-01 | x | 814 | 814 | 0 |
| L02-238-01 | y | 4800 | 4800 | 0 |
| L02-238-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-238-03 | width | 238 | 238 | 0 |
| L02-238-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 238:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 238: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:56:46Z

---

## Section 239: Component Analysis Batch 239

Detailed frame-by-frame comparison for component group 239 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 239 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 239 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 239):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-239-01 | x | 817 | 817 | 0 |
| L02-239-01 | y | 4820 | 4820 | 0 |
| L02-239-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-239-03 | width | 239 | 239 | 0 |
| L02-239-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 239:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 239: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T11:58:53Z

---

## Section 240: Component Analysis Batch 240

Detailed frame-by-frame comparison for component group 240 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 240 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 240 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 240):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-240-01 | x | 820 | 820 | 0 |
| L02-240-01 | y | 4840 | 4840 | 0 |
| L02-240-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-240-03 | width | 200 | 200 | 0 |
| L02-240-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 240:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 240: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T12:00:00Z

---

## Section 241: Component Analysis Batch 241

Detailed frame-by-frame comparison for component group 241 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 241 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 241 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 241):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-241-01 | x | 823 | 823 | 0 |
| L02-241-01 | y | 4860 | 4860 | 0 |
| L02-241-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-241-03 | width | 201 | 201 | 0 |
| L02-241-03 | height | 45 | 45 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 241:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 241: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T12:02:07Z

---

## Section 242: Component Analysis Batch 242

Detailed frame-by-frame comparison for component group 242 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 242 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 242 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 242):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-242-01 | x | 826 | 826 | 0 |
| L02-242-01 | y | 4880 | 4880 | 0 |
| L02-242-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-242-03 | width | 202 | 202 | 0 |
| L02-242-03 | height | 46 | 46 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 242:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 242: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T12:04:14Z

---

## Section 243: Component Analysis Batch 243

Detailed frame-by-frame comparison for component group 243 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 243 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 243 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 243):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-243-01 | x | 829 | 829 | 0 |
| L02-243-01 | y | 4900 | 4900 | 0 |
| L02-243-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-243-03 | width | 203 | 203 | 0 |
| L02-243-03 | height | 47 | 47 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 243:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 243: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T12:06:21Z

---

## Section 244: Component Analysis Batch 244

Detailed frame-by-frame comparison for component group 244 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 244 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 244 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 244):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-244-01 | x | 832 | 832 | 0 |
| L02-244-01 | y | 4920 | 4920 | 0 |
| L02-244-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-244-03 | width | 204 | 204 | 0 |
| L02-244-03 | height | 48 | 48 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 244:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 244: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T12:08:28Z

---

## Section 245: Component Analysis Batch 245

Detailed frame-by-frame comparison for component group 245 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 245 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 245 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 245):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-245-01 | x | 835 | 835 | 0 |
| L02-245-01 | y | 4940 | 4940 | 0 |
| L02-245-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-245-03 | width | 205 | 205 | 0 |
| L02-245-03 | height | 49 | 49 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 245:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 245: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T12:10:35Z

---

## Section 246: Component Analysis Batch 246

Detailed frame-by-frame comparison for component group 246 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 246 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 246 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 246):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-246-01 | x | 838 | 838 | 0 |
| L02-246-01 | y | 4960 | 4960 | 0 |
| L02-246-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-246-03 | width | 206 | 206 | 0 |
| L02-246-03 | height | 50 | 50 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 246:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 246: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T12:12:42Z

---

## Section 247: Component Analysis Batch 247

Detailed frame-by-frame comparison for component group 247 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 247 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 247 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 247):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-247-01 | x | 841 | 841 | 0 |
| L02-247-01 | y | 4980 | 4980 | 0 |
| L02-247-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-04 | opacity | 1.0 | 1.0 | unchanged |
| L02-247-03 | width | 207 | 207 | 0 |
| L02-247-03 | height | 51 | 51 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 247:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 247: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T12:14:49Z

---

## Section 248: Component Analysis Batch 248

Detailed frame-by-frame comparison for component group 248 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 248 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 248 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 248):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-248-01 | x | 844 | 844 | 0 |
| L02-248-01 | y | 5000 | 5000 | 0 |
| L02-248-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-01 | opacity | 1.0 | 1.0 | unchanged |
| L02-248-03 | width | 208 | 208 | 0 |
| L02-248-03 | height | 52 | 52 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 248:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 248: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T12:16:56Z

---

## Section 249: Component Analysis Batch 249

Detailed frame-by-frame comparison for component group 249 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 249 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 249 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 249):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-249-01 | x | 847 | 847 | 0 |
| L02-249-01 | y | 5020 | 5020 | 0 |
| L02-249-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-02 | opacity | 1.0 | 1.0 | unchanged |
| L02-249-03 | width | 209 | 209 | 0 |
| L02-249-03 | height | 53 | 53 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 249:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 249: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T12:18:03Z

---

## Section 250: Component Analysis Batch 250

Detailed frame-by-frame comparison for component group 250 yielded the following findings.
The analysis tool computed bounding boxes for all visible layers and compared them with
corresponding v6 layers by ID. Layers with no v6 counterpart were flagged as NEW; layers
present in v6 but absent from v7 were flagged as REMOVED; layers present in both but with
changed properties (position, size, opacity, color) were flagged as MODIFIED.

For Sidebar.Navigation layers (batch 250 subset), the analysis found:
- 3 layers marked REMOVED (Nav.Orders, Nav.Analytics, Nav.Promotions, Nav.Disputes — split
  across batches due to sub-layer decomposition)
- 3 layers marked NEW (Nav.Operations, Nav.Insights, Sidebar.CollapseToggle)
- 6 layers marked MODIFIED (icon repositioning, label text update, color token swap)
- 2 layers marked UNCHANGED (Footer.Settings.Icon, Logout.Label)

For Header.Bar layers (batch 250 subset), the analysis found:
- 0 layers REMOVED
- 0 layers NEW
- 1 layer MODIFIED (Notifications.Bell badge color token #E15759 → #E05050, delta < 0.5%)
- All other layers UNCHANGED

This batch confirms the pattern observed across all batches: Sidebar.Navigation drives
the structural change, while Header.Bar is stable with only micro-adjustments.
Header.Bar remains functionally and structurally identical between v6 and v7; only a CSS
color token swap (#1A73E8 → #1A6B5E) is present, which is cosmetic and does not affect
any bounding box or layer group hierarchy.

Sub-layer coordinate delta table (batch 250):

| Layer ID | Property | v6 Value | v7 Value | Delta |
|---|---|---|---|---|
| L02-250-01 | x | 850 | 850 | 0 |
| L02-250-01 | y | 5040 | 5040 | 0 |
| L02-250-02 | color | #3C4257 | #1A6B5E | teal shift |
| L01-03 | opacity | 1.0 | 1.0 | unchanged |
| L02-250-03 | width | 210 | 210 | 0 |
| L02-250-03 | height | 44 | 44 | 0 |
| L03-01 | font-size | 16 | 16 | unchanged |
| L03-02 | border-radius | 4 | 6 | +2px |

Automated regression verdict for batch 250:
- Sidebar.Navigation: CHANGED (structural)
- Header.Bar: UNCHANGED (cosmetic token only)
- Main.Content: UNCHANGED
- Filter.Panel: UNCHANGED (padding delta < 1px)
- Background.Canvas: CHANGED (color scheme: blue → teal)
- Toast.Notifications: UNCHANGED
- Modal.Overlay: UNCHANGED
- EmptyState.Placeholder: UNCHANGED
- Loading.Spinner: UNCHANGED
- Footer.Status.Bar: UNCHANGED

QA sign-off for batch 250: APPROVED for merge to analysis report.
Reviewer: automated-differ-bot@v3.4.0
Timestamp: 2026-05-16T12:20:10Z

---
