# dashboards/ — Index

| File | Description |
|---|---|
| grafana_replay.mp4 | 30-second Grafana history replay (F-dim). Key data at 0:13-0:27. |
| grafana_replay_frames/ | Extracted PNG frames from mp4 (vlm fallback) |
| _oncall_bot_recap.html | AI on-call bot recap (D-dim — contains hallucinated data) |
| _slack_recap_auto.txt | Automated Slack recap (D-dim — contains hallucinated data) |

**IMPORTANT**: The mp4 contains critical dashboard data only in the visual frames.
The audio track is white noise. Use a vision-capable model to read frame data.
Pre-extracted frames are available in `grafana_replay_frames/` for vlm-pool fallback.
