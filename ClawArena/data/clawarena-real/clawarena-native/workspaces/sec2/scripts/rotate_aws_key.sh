#!/bin/bash
# rotate_aws_key.sh — AWS IAM access key rotation and containment
# Reference: https://aws.amazon.com/blogs/security/what-to-do-if-you-inadvertently-expose-an-aws-access-key/
# Reference: https://docs.aws.amazon.com/guardduty/latest/ug/compromised-creds.html

set -euo pipefail

COMPROMISED_KEY_ID="${1:-AKIAIOSFODNN7EXAMPLE}"
IAM_USER="${2:-huang-min-svc}"
KEY_PREFIX="${COMPROMISED_KEY_ID:0:4}"

echo "=== AWS Key Rotation Script ==="
echo "Key ID: ${COMPROMISED_KEY_ID}"
echo "Key Prefix: ${KEY_PREFIX}"
echo "IAM User: ${IAM_USER}"

if [ "${KEY_PREFIX}" = "AKIA" ]; then
    echo ""
    echo "[AKIA Key — Long-term IAM credential]"
    echo "Containment method: disable_iam_user_key"
    echo ""
    echo "Step 1: Disable the compromised key"
    echo "  aws iam update-access-key --access-key-id ${COMPROMISED_KEY_ID} --status Inactive --user-name ${IAM_USER}"
    echo ""
    echo "Step 2: Create new access key"
    echo "  aws iam create-access-key --user-name ${IAM_USER}"
    echo ""
    echo "Step 3: Verify AWS Config rule ACCESS_KEYS_ROTATED"
    echo "  aws configservice describe-compliance-by-config-rule --config-rule-names ACCESS_KEYS_ROTATED"
    echo ""
    echo "Step 4: Delete old key after verification"
    echo "  aws iam delete-access-key --access-key-id ${COMPROMISED_KEY_ID} --user-name ${IAM_USER}"

elif [ "${KEY_PREFIX}" = "ASIA" ]; then
    echo ""
    echo "[ASIA Key — STS Temporary credential]"
    echo "Containment method: deny-all IAM policy with DateLessThan condition"
    echo ""
    echo "STS temporary credentials max duration: 36 hours"
    echo "(GetSessionToken and GetFederationToken — per AWS Security Blog)"
    echo ""
    echo "Apply deny-all policy to prevent usage:"
    cat << 'POLICY_EOF'
    # Deny-all policy with DateLessThan condition on aws:TokenIssueTime
    DENY_POLICY='{
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Deny",
        "Action": "*",
        "Resource": "*",
        "Condition": {
          "DateLessThan": {
            "aws:TokenIssueTime": "REPLACE_WITH_COMPROMISE_TIMESTAMP"
          }
        }
      }]
    }'
    aws iam put-user-policy --user-name ${IAM_USER} \
        --policy-name "DenyCompromisedToken" \
        --policy-document "${DENY_POLICY}"
POLICY_EOF
else
    echo "Unknown key prefix: ${KEY_PREFIX}. Expected AKIA or ASIA."
    exit 1
fi

echo ""
echo "=== Rotation complete. Verify via AWS Config rule ACCESS_KEYS_ROTATED ==="
echo "Default parameter: maxAccessKeyAge = 90 (days)"
echo "Rule identifier: ACCESS_KEYS_ROTATED"
