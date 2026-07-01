#!/bin/bash
# rotate_aws_key.sh — AWS IAM access key rotation and containment (v2, Update 2)
# Reference: https://aws.amazon.com/blogs/security/what-to-do-if-you-inadvertently-expose-an-aws-access-key/
# Update 2 addition: explicit 36h deny-all snippet for STS (ASIA) credentials

set -euo pipefail

COMPROMISED_KEY_ID="${1:-AKIAIOSFODNN7EXAMPLE}"
IAM_USER="${2:-huang-min-svc}"
KEY_PREFIX="${COMPROMISED_KEY_ID:0:4}"

echo "=== AWS Key Rotation Script v2 ==="
echo "Key ID: ${COMPROMISED_KEY_ID}"
echo "Key Prefix: ${KEY_PREFIX}"

if [ "${KEY_PREFIX}" = "AKIA" ]; then
    echo "[AKIA] Long-term IAM key: disable_iam_user_key"
    echo "  aws iam update-access-key --access-key-id ${COMPROMISED_KEY_ID} --status Inactive --user-name ${IAM_USER}"
    echo "  aws iam create-access-key --user-name ${IAM_USER}"
    echo "  Verify: aws configservice describe-compliance-by-config-rule --config-rule-names ACCESS_KEYS_ROTATED"

elif [ "${KEY_PREFIX}" = "ASIA" ]; then
    echo "[ASIA] STS temporary credential"
    echo "Max lifetime: 36 hours (GetSessionToken/GetFederationToken)"
    echo ""
    echo "Apply deny-all policy with DateLessThan condition:"
    echo ""
    cat << 'DENY_EOF'
# Deny-all policy for STS temporary credentials
# Uses DateLessThan condition on aws:TokenIssueTime
# This invalidates all tokens issued before the compromise time
DENY_POLICY='{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "DenyCompromisedSTSToken",
    "Effect": "Deny",
    "Action": "*",
    "Resource": "*",
    "Condition": {
      "DateLessThan": {
        "aws:TokenIssueTime": "REPLACE_WITH_COMPROMISE_TIMESTAMP_ISO8601"
      }
    }
  }]
}'
aws iam put-user-policy \
    --user-name "${IAM_USER}" \
    --policy-name "DenyCompromisedSTS" \
    --policy-document "${DENY_POLICY}"

# The 36-hour window: any ASIA token issued up to 36 hours ago may still be valid
# You must keep the deny policy active for at least 36 hours after the compromise timestamp
echo "NOTE: Keep deny policy active for >= 36 hours to cover maximum STS token lifetime"
DENY_EOF
fi

echo ""
echo "Post-rotation: verify AWS Config rule ACCESS_KEYS_ROTATED"
echo "Rule identifier: ACCESS_KEYS_ROTATED (verbatim)"
echo "Default: maxAccessKeyAge = 90 days"
