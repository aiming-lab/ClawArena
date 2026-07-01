# Design Review Request — merchant-portal-v7

**From:** Priya Nair, Design Director
**To:** UX Ops Review Team
**Date:** 2026-05-20
**Subject:** Approve or block v7 candidate for 2026 Q2 GA

Hi team,

As we approach the Q2 GA milestone for the merchant back-office portal, I need a formal
design-ops audit of the v7 candidate before we hand it off to engineering for final
implementation.

The v6 design went live in 2024 Q3 and has been our baseline. The v7 redesign introduces
a major consolidation of the navigation sidebar (Sidebar.Navigation) as part of our
"Simplified Flows" initiative. A condensed nav reduces cognitive load for merchants who
primarily use 3–5 key workflows.

**What I need from you:**
1. A structured review plan covering: navigation-delta, accessibility, localization,
   component library alignment, and mobile responsiveness.
2. Identify exactly which component changed most significantly in the layout diff.
3. Validate PSD tree consistency (number of root layers and nesting depth).
4. Check the localization targets CSV for the 4 supported locales.
5. Cross-check the design bot summary with your own findings and flag any discrepancies.
6. A final audit decision JSON with your recommendation.

Please reference project code **merchant-portal-v7** throughout.

Thanks,
Priya
