# Accessibility Checklist — merchant-portal-v7

**Audit date:** 2026-05-17
**Auditor:** Accessibility Platform team
**Standard:** WCAG 2.1 AA

## Checklist

| # | Check | Component | Result | Notes |
|---|---|---|---|---|
| 1 | Keyboard navigation (Tab order) | All | PASS | Tab order follows visual order |
| 2 | Focus ring visibility | Sidebar.CollapseToggle | **FAIL** | Focus ring not rendered |
| 3 | Color contrast — primary text | All text | PASS | 7.2:1 (exceeds AA) |
| 4 | Color contrast — secondary text | Nav labels (secondary) | **FAIL** | 3.8:1 < 4.5:1 required |
| 5 | ARIA labels | Navigation items | PASS | aria-label present on all items |
| 6 | Screen reader announcement | Modal dialogs | PASS | aria-live region set |
| 7 | Touch target size | Sidebar.CollapseToggle | PASS | 44×44px minimum met |
| 8 | Zoom support (200%) | All | PASS | No horizontal scroll at 200% |
| 9 | Animation preference | Loading.Spinner | PASS | prefers-reduced-motion respected |
| 10 | Form labels | Filter.Panel inputs | PASS | All inputs labeled |

## Outstanding Issues (blockers)

1. **Focus ring** — Sidebar.CollapseToggle — must add CSS `:focus-visible` ring
2. **Color contrast** — `.nav-label-secondary` — change to #767676 or darker (#555)

## Passed Items Summary

8 of 10 checks pass. 2 blockers require engineering fix before approval.
