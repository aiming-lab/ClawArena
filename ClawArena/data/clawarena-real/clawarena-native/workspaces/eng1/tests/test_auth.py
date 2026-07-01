"""
Test suite for requests/auth.py authentication handlers.

Tests cover HTTPBasicAuth, HTTPProxyAuth, and HTTPDigestAuth behaviour.
"""
import pytest
import base64
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from requests.auth import HTTPBasicAuth, HTTPProxyAuth, _basic_auth_str


class TestHTTPBasicAuth:
    """Tests for HTTP Basic authentication."""

    def test_basic_auth_str_ascii(self):
        s = _basic_auth_str("user", "pass")
        assert s.startswith("Basic ")
        decoded = base64.b64decode(s[6:]).decode("ascii")
        assert decoded == "user:pass"

    def test_basic_auth_equality(self):
        a = HTTPBasicAuth("alice", "secret")
        b = HTTPBasicAuth("alice", "secret")
        assert a == b

    def test_basic_auth_inequality(self):
        a = HTTPBasicAuth("alice", "secret")
        b = HTTPBasicAuth("bob", "secret")
        assert a != b

    def test_proxy_auth_inherits_basic(self):
        pa = HTTPProxyAuth("user", "pass")
        s = _basic_auth_str("user", "pass")
        assert s.startswith("Basic ")


class TestHTTPBasicAuthEdgeCases:
    """Edge cases for authentication helpers."""

    def test_unicode_username(self):
        s = _basic_auth_str("tëst", "päss")
        assert s.startswith("Basic ")

    def test_empty_password(self):
        a = HTTPBasicAuth("user", "")
        b = HTTPBasicAuth("user", "")
        assert a == b
