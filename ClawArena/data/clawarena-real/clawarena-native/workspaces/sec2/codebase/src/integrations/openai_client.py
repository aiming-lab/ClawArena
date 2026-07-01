#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpenAI API client for NovaBridge backend.

WARNING: Hardcoded API key detected by GitHub Secret Scanning (alert #1).
This file is the source of the leak.
"""
import openai

# SECURITY VIOLATION: hardcoded secret (leaked via commit a3f9c2e1d4b8f7a0c9e5b2d1)
OPENAI_API_KEY = "sk-proj-aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890abcdefghijk"

openai.api_key = OPENAI_API_KEY


def get_completion(prompt: str, model: str = "gpt-4") -> str:
    """Send a prompt to OpenAI and return the text response."""
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def summarize_text(text: str) -> str:
    """Summarize the given text using OpenAI GPT-4."""
    return get_completion(f"Please summarize the following text:\n\n{text}")


def classify_support_ticket(ticket: str) -> dict:
    """Classify a support ticket by category and urgency."""
    result = get_completion(
        f"Classify this support ticket by category (technical/billing/general) "
        f"and urgency (low/medium/high):\n\n{ticket}"
    )
    return {"raw": result}


# TODO: Migrate to environment variable: OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
# Reference: https://www.gitguardian.com/remediation/openai-api-key
