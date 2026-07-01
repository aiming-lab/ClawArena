# iOS 14 WKWebView Color Rendering Bug — Bugzilla #88432

## Summary

WKWebView on iOS 14 (14.0–14.8.1) has a confirmed rendering anomaly affecting
CSS `background-color` hex values in the warm orange range (approx #ff5500–#ff9900).
The affected values are composited through an incorrect alpha-blending path that
maps saturated warm colors to neutral grey (#d3d3d3 ± 10%).

## Impact on EXP-2421

The experiment treatment button uses `checkout_button_color: #ff6633`.
On iOS 14, this renders as grey (#d3d3d3), making the button appear disabled.
This explains the -3.8% conversion drop in mobile_us (iOS 14 user share: 67%)
compared to near-zero drops in desktop segments.

## Affected platforms

- iOS 14.0–14.8.1 (WKWebView only; UIWebView not affected — already deprecated)
- Mobile Safari on iOS 14 (same engine)
- Apps using WKWebView rendering pipeline

## Fix

Upgrade target hex to #e05c00 (darker orange, outside the affected range) OR
disable treatment for iOS 14 user-agents until fixed.

## References

- Internal bug tracker: Bugzilla #88432 (filed 2026-04-09, resolved 2026-04-12)
- Apple developer forums: thread 4487921
- EXP-2421 PRD risk register: Risk 1 (CSS rendering divergence on iOS 14)
