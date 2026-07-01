#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AWS S3 uploader for NovaBridge backend.

WARNING: Hardcoded AWS access key detected by GitHub Secret Scanning (alert #2).
The AKIA prefix indicates this is a long-term IAM user access key.
"""
import boto3

# SECURITY VIOLATION: hardcoded IAM long-term credentials (AKIA prefix)
# Source: https://docs.aws.amazon.com/guardduty/latest/ug/compromised-creds.html
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_DEFAULT_REGION = "us-east-1"
S3_BUCKET = "novabridge-data"


def get_s3_client():
    """Return an authenticated S3 client using hardcoded credentials."""
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION,
    )


def upload_file(local_path: str, s3_key: str) -> bool:
    """Upload a local file to S3."""
    client = get_s3_client()
    try:
        client.upload_file(local_path, S3_BUCKET, s3_key)
        return True
    except Exception as e:
        print(f"Upload failed: {e}")
        return False


def list_bucket_contents() -> list:
    """List all objects in the S3 bucket."""
    client = get_s3_client()
    response = client.list_objects_v2(Bucket=S3_BUCKET)
    return [obj["Key"] for obj in response.get("Contents", [])]


# TODO: Use IAM roles or environment variables; containment: disable AKIA key via IAM console
# AKIA prefix = long-term IAM user key; ASIA prefix = STS temporary credential (different remediation)
