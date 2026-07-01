# Bug Tracker Excerpts — EXP-2421 Related Issues

## Bugzilla #88432 — iOS 14 WKWebView warm-hue color compositing bug

**Filed**: 2026-04-09 by priya.data  
**Priority**: P1  
**Status**: RESOLVED (2026-04-12)  

### Description

WKWebView on iOS 14 (tested builds: 14.0, 14.3, 14.6, 14.8, 14.8.1) exhibits an incorrect color compositing behavior for CSS background-color values in the warm orange range approximately #ff5500 to #ff9900. The root cause is an off-by-one error in the CoreAnimation color space transform applied when rendering non-opaque layers on top of white backgrounds.

Affected hex values (partial list):
- #ff6600 → renders as #d3d3d3
- #ff6633 → renders as #d3d3d3 (EXP-2421 treatment color)
- #ff7722 → renders as #d3d3d3
- #ff8800 → renders as #e0e0e0 (partially affected)

### Reproduction steps

1. Open test page at https://internal-qa.example.com/ios14-color-test
2. Load on iOS 14.x device or simulator
3. Observe that element with background-color #ff6633 appears grey

### Impact

EXP-2421 treatment arm uses checkout_button_color #ff6633. On iOS 14, the checkout button appears grey and disabled. This causes a -3.8% conversion drop in mobile_us (67% iOS 14 user share) and a -1.5% drop in mobile_eu (lower iOS 14 share due to Android dominance).

### Fix

Short-term: Roll back treatment B for mobile_us (or all) to control A.
Long-term: Use hex #e05c00 (outside affected range) for redesigned button.

---

## Ticket #92104 — AI bot incorrect root cause attribution

**Filed**: 2026-04-11 by jordan.exp  
**Priority**: P3 (tracking issue)  
**Status**: OPEN

The exp-review-bot (ai_summaries/exp_review_bot.md) incorrectly identifies desktop_eu as the primary cause of EXP-2421 regression. The actual root cause is iOS 14 rendering of #ff6633 in mobile_us. Bot output should not be used as authoritative source for postmortem decisions.

## Bugzilla #88433 — Related rendering issue follow-up

**Filed**: 2026-04-12  
**Status**: WONTFIX / DEFERRED  

Related to #88432. Testing additional hex values in the ff5000-ff9000 range. Confirmed that the range #ff5400-#ff8c00 is affected on iOS 14.x but not on iOS 15+ (WKWebView updated compositing pipeline).

## Bugzilla #88434 — Related rendering issue follow-up

**Filed**: 2026-04-13  
**Status**: WONTFIX / DEFERRED  

Related to #88432. Testing additional hex values in the ff5000-ff9000 range. Confirmed that the range #ff5400-#ff8c00 is affected on iOS 14.x but not on iOS 15+ (WKWebView updated compositing pipeline).

## Bugzilla #88435 — Related rendering issue follow-up

**Filed**: 2026-04-14  
**Status**: WONTFIX / DEFERRED  

Related to #88432. Testing additional hex values in the ff5000-ff9000 range. Confirmed that the range #ff5400-#ff8c00 is affected on iOS 14.x but not on iOS 15+ (WKWebView updated compositing pipeline).

## Bugzilla #88436 — Related rendering issue follow-up

**Filed**: 2026-04-15  
**Status**: WONTFIX / DEFERRED  

Related to #88432. Testing additional hex values in the ff5000-ff9000 range. Confirmed that the range #ff5400-#ff8c00 is affected on iOS 14.x but not on iOS 15+ (WKWebView updated compositing pipeline).

## Bugzilla #88437 — Related rendering issue follow-up

**Filed**: 2026-04-16  
**Status**: WONTFIX / DEFERRED  

Related to #88432. Testing additional hex values in the ff5000-ff9000 range. Confirmed that the range #ff5400-#ff8c00 is affected on iOS 14.x but not on iOS 15+ (WKWebView updated compositing pipeline).

## Bugzilla #88438 — Related rendering issue follow-up

**Filed**: 2026-04-17  
**Status**: WONTFIX / DEFERRED  

Related to #88432. Testing additional hex values in the ff5000-ff9000 range. Confirmed that the range #ff5400-#ff8c00 is affected on iOS 14.x but not on iOS 15+ (WKWebView updated compositing pipeline).

## Bugzilla #88439 — Related rendering issue follow-up

**Filed**: 2026-04-18  
**Status**: WONTFIX / DEFERRED  

Related to #88432. Testing additional hex values in the ff5000-ff9000 range. Confirmed that the range #ff5400-#ff8c00 is affected on iOS 14.x but not on iOS 15+ (WKWebView updated compositing pipeline).

## Bugzilla #88440 — Related rendering issue follow-up

**Filed**: 2026-04-19  
**Status**: WONTFIX / DEFERRED  

Related to #88432. Testing additional hex values in the ff5000-ff9000 range. Confirmed that the range #ff5400-#ff8c00 is affected on iOS 14.x but not on iOS 15+ (WKWebView updated compositing pipeline).

