# siem_alerts/ — SIEM Alert Stream

| File | Content |
|---|---|
| alerts.ndjson | Current incident alert stream (300+ events, NDJSON format) |
| alert_correlations.ndjson | Alert correlation clusters from SIEM engine |

Parse with: `cat alerts.ndjson | python -c "import sys,json; [print(json.dumps(json.loads(l),indent=2)) for l in sys.stdin]"`
