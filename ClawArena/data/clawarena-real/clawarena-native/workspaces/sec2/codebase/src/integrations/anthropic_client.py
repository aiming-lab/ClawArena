#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Anthropic Claude API client for NovaBridge backend.

Note: This file also contains a hardcoded secret (anthropic_api_key).
Discovered in Update 1 via GitGuardian webhook v2 (alert #51).
"""
import anthropic

# SECURITY VIOLATION: hardcoded Anthropic API key
ANTHROPIC_API_KEY = "sk-ant-api03-xXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX-XXXXXXXX"

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def get_claude_response(prompt: str) -> str:
    """Send a prompt to Claude and return the response."""
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


# TODO: Use environment variable: ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
# secret_type: anthropic_api_key (GitHub Secret Scanning verbatim type name)
