#!/bin/bash
# artifact_check.sh - Validate GitLab CI artifact configurations
# Checks expire_in format, artifact paths, and policy settings

set -euo pipefail

VALID_FORMATS_REGEX="^([0-9]+ (seconds?|mins?|hours?|days?|weeks?|months?|mos)( [0-9]+ (seconds?|mins?|hours?|days?))?|never|[0-9]+h[0-9]+min)$"

check_expire_in() {
    local value="$1"
    if echo "$value" | grep -qE "$VALID_FORMATS_REGEX"; then
        echo "OK: expire_in='$value' is valid"
        return 0
    else
        echo "ERROR: expire_in='$value' is NOT a valid GitLab CI format"
        echo "Valid examples: '42 seconds', '3 mins 4 sec', '2h20min', '6 mos 1 day', 'never'"
        return 1
    fi
}

# Check known bad format
check_expire_in "30d" || true  # Will fail - intended to demonstrate the issue
check_expire_in "30 days" && echo "Correct format confirmed"
check_expire_in "never" && echo "Special value 'never' is valid"
