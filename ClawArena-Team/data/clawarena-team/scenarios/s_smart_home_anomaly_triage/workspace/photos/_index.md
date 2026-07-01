# Photos Directory

Visual evidence files for the anomaly triage.

| File | Contents | Key Data |
|------|----------|----------|
| `floorplan.png` | Household floor plan with camera positions | cam_basement_03 location marked |
| `camera_basement_screenshot.png` | cam_basement_03 live feed at 02:14:07 | Camera ID, timestamp, face detection box |
| `thermal_basement.png` | Thermal image of basement utility room | **Humidity: 94%** (on-image caption) |
| `dhcp_alert_screenshot.png` | Gateway DHCP alert screen | Unknown MAC a4:cf:12:8e:7b:3d |

**All images require a vlm-capable subagent to extract the on-image text values.**
The humidity value (94%) is visible only in the thermal image caption.
