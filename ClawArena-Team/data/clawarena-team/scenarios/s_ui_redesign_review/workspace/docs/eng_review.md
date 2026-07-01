# Engineering Review — merchant-portal-v7 UI Redesign

**Version:** v7.0.0-rc1
**Date:** 2026-05-18
**Author:** Engineering Review Committee (Frontend Platform Team)

## 1. Component Change Summary

The v7 redesign introduces targeted changes to improve the merchant onboarding experience
and reduce time-to-task for core workflows.

### 1.1 Sidebar.Navigation

This is the **primary structural change** in v7. The redesign consolidates the five-item
vertical navigation (Dashboard, Orders, Analytics, Promotions, Disputes) into three
top-level entries:

- **Dashboard** — absorbs Orders as a sub-menu item
- **Operations** — merges Promotions and Disputes under one umbrella
- **Insights** — renamed from Analytics (content unchanged, only label updated)

The motivation is a 40% reduction in navigation depth for the most common merchant
workflows (order management and dispute resolution).

**Impact:** Medium-high. Requires frontend routing updates, breadcrumb re-mapping,
and mobile touch-target recalculations.

### 1.2 Header.Bar

No structural changes. The Header.Bar layout (Logo → Search → UserMenu → Notifications)
is identical in v6 and v7. Only a minor CSS variable update was applied for the teal
color scheme alignment.

### 1.3 Main.Content Area

No layout changes. The OrderList.Table and Pagination.Controls remain identical.

## 2. Token / Token-library Alignment

The v7 design tokens are available in `docs/design-tokens-v7.json` (not yet published;
pending v7 GA). Placeholder tokens used in rc1 for color and spacing are backported from
v6 with teal overrides.

## 3. Mobile Responsiveness

Tested at 375px (iPhone SE) and 768px (iPad). Issues found:

1. **Focus ring on Sidebar.CollapseToggle**: Missing in all breakpoints.
   CSS class `.sidebar-toggle:focus-visible` not implemented.
2. **Color contrast on secondary nav labels**: Measured at 3.8:1 (target: 4.5:1 WCAG AA).
   Affected text: `.nav-label-secondary` color `#999999` on background `#F5F5F5`.

These are **required fixes** before GA. Non-blocking for RC review, but must be resolved
before approval sign-off.

## 4. Localization Coverage

The design supports four locales: en, zh-CN, ja, de. String table is in
`docs/localization_targets.csv`. All four locales have been accounted for in the
string-length stress test (Japanese text expansion factor: 0.9x; German: 1.3x).

German-locale sidebar labels may overflow at 375px width. Engineering has applied
truncation with ellipsis as a workaround.

## 5. A11y Checklist Reference

See `docs/a11y_checklist.md` for the full accessibility audit. Two issues are outstanding
(see §3 above). All other checks pass.

## 6. Recommendation

Engineering endorses v7 for approval **with mandatory a11y fixes** (focus ring + contrast).
Once those two items are resolved, v7 is ready for GA.
