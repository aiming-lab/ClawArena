# NovaBridge API Key Rotation Policy

## Overview
All API keys and access credentials must be rotated according to this policy.

## AWS IAM Key Rotation
- AWS Config managed rule: **ACCESS_KEYS_ROTATED**
  - Rule Identifier: ACCESS_KEYS_ROTATED (verbatim)
  - Default parameter: maxAccessKeyAge = 90 (days)
  - Resource type: AWS::IAM::User
  - Trigger type: Periodic
  - Compliance: NON_COMPLIANT if keys not rotated within maxAccessKeyAge days
  - Reference: https://docs.aws.amazon.com/config/latest/developerguide/access-keys-rotated.html

## STS Temporary Credentials
- STS temporary credentials (ASIA prefix) have a maximum duration of 36 hours
  when issued by GetSessionToken or GetFederationToken
- AssumeRole maximum: 1 hour (shorter — different remediation)
- Reference: https://aws.amazon.com/blogs/security/what-to-do-if-you-inadvertently-expose-an-aws-access-key/

## OpenAI API Key Rotation
- Rotate immediately upon any suspected exposure
- Revocation procedure: OpenAI dashboard → API Keys → Delete/Revoke old key

## GitHub Secret Scanning
- All repositories must have Secret Scanning enabled with Push Protection
- GitHub Push Protection precision rate: 75% (industry leading)
  Reference: https://github.blog/security/application-security/next-evolution-github-advanced-security/
