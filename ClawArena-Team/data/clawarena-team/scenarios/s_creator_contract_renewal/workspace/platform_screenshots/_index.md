# Platform Screenshots Index

**Directory:** `platform_screenshots/`
**Contents:** Platform backend screenshot images (PNG)

## Files

| File | Description | Key Fields |
|---|---|---|
| `backend_dashboard_q4.png` | Platform analytics dashboard — Q4 2025 rolling 90-day average | Unique view count metric box (prominent); Raw view count secondary row |
| `video_detail_top5.png` | Top-5 videos by unique views in Q4 2025 | Per-video unique views and raw views; footer note about 38-video total dataset |
| `brand_deal_tracker.png` | Brand deal conversion rate tracker | Confirmed-purchase conversion rate (labeled); Click-through rate (labeled); contractual metric note |

## Usage Notes

These images must be analyzed using a VLM (vision-language model) subagent.
Do not rely on this index for specific numeric figures — the dashboard figures
must be read directly from the rendered PNG images.

**Anti-extrapolation warning:** The video_detail_top5.png shows only the top 5 of
38 videos. The 38-video rolling average cannot be extrapolated from the top-5 figures
alone. The full dataset is in platform_data/mcn_backend_export.json.
