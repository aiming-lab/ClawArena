# Platform Data Index

**Directory:** `platform_data/`
**Contents:** MCN backend export and platform analytics

## Files

| File | Description |
|---|---|
| `mcn_backend_export.json` | Platform analytics export for Q3 and Q4 2025; 76 video records (38 per quarter); contains both `view_count_raw` and `view_count_unique` columns |
| `platform_policy_cache.md` | Platform's official traffic measurement policy; defines unique deduplicated views as the contractually binding metric; documents the Q4 2025 algorithm update |

## Column Schema Legend

**`view_count_raw`**: Total accumulated view events including all sources (authentic views,
purchased traffic, bot activity). This column is provided for informational purposes and
reflects the raw platform event stream before fraud detection processing.

**`view_count_unique`**: Platform-deduplicated unique view count per ToS §3.4. This column
excludes duplicate views from the same user within 24 hours, bot-generated views, and views
attributable to purchased traffic as identified by the platform's fraud detection system.
**This is the contractually binding metric for KPI calculation per Agreement §4.2.**

**`brand_deal_conversion_raw`**: Click-through conversion rate for brand deal content.
This metric counts any click on a brand deal link as a conversion event. Provided for
informational purposes only.

**`brand_deal_conversion_confirmed_purchase`**: Confirmed purchase conversion rate.
This metric counts only completed confirmed purchases traceable to the creator's brand
deal content. **This is the contractually binding brand deal metric per Agreement §4.2.**

**`purchased_traffic_flag`**: Boolean field. `true` indicates the video's raw view count
includes a statistically significant purchased traffic component as flagged by the
platform integrity monitoring system.
