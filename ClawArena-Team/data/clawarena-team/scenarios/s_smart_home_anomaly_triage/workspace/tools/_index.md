# Tools Directory

| File | Description |
|------|-------------|
| `verify_home_signoff.py` | Validates ha_response_config.yaml and emits SIGNOFF_TOKEN |

Usage (q5):
    python tools/verify_home_signoff.py output/ha_response_config.yaml

Output: SIGNOFF_TOKEN: <token>
Paste the token into your svp_email.md.
