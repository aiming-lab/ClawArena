"""
Test suite for requests/utils.py utility functions.

This module tests URL parsing, header validation, encoding detection,
and authentication helper functions including netrc credential lookup.

Real test cases for CVE-2024-47081 (get_netrc_auth credential leak) are in
tests/test_utils_regression.py.
"""
import os
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from requests.utils import (
    get_netrc_auth,
    requote_uri,
    get_encoding_from_headers,
    is_ipv4_address,
    is_valid_cidr,
)


class TestGetNetrcAuth:
    """Tests for the get_netrc_auth utility function."""

    def test_works(self, tmp_netrc):
        """Normal case: legitimate URL returns correct credentials from netrc.

        Anchor: assert auth == ("aaaa", "bbbb")
        Source: https://raw.githubusercontent.com/psf/requests/main/tests/test_utils.py
        """
        auth = get_netrc_auth("http://example.com/")
        assert auth == ("aaaa", "bbbb")

    def test_missing_netrc_returns_none(self, tmp_path, monkeypatch):
        """If no netrc file exists, function returns None."""
        monkeypatch.setenv("NETRC", str(tmp_path / "nonexistent_netrc"))
        auth = get_netrc_auth("http://example.com/")
        assert auth is None

    def test_unknown_host_returns_none(self, tmp_netrc):
        """Host not in netrc returns None."""
        auth = get_netrc_auth("http://unknown.example.org/")
        assert auth is None

    def test_https_url(self, tmp_netrc):
        """HTTPS URLs are also supported."""
        auth = get_netrc_auth("https://example.com/path?query=1")
        assert auth == ("aaaa", "bbbb")


class TestRequoteUri:
    """Tests for requote_uri."""

    def test_requote_uri_noop(self):
        assert requote_uri("http://example.com/path") == "http://example.com/path"

    def test_requote_uri_with_percent(self):
        result = requote_uri("http://example.com/path%20with%20spaces")
        assert "example.com" in result


class TestHeaderEncoding:
    """Tests for get_encoding_from_headers."""

    def test_encoding_from_content_type(self):
        headers = {"content-type": "text/html; charset=utf-8"}
        assert get_encoding_from_headers(headers) == "utf-8"

    def test_no_encoding(self):
        headers = {"content-type": "application/json"}
        assert get_encoding_from_headers(headers) is None

    def test_no_content_type(self):
        assert get_encoding_from_headers({}) is None


class TestNetworkUtils:
    """Tests for IP/CIDR utilities."""

    def test_is_ipv4_address_valid(self):
        assert is_ipv4_address("192.168.1.1") is True
        assert is_ipv4_address("0.0.0.0") is True
        assert is_ipv4_address("255.255.255.255") is True

    def test_is_ipv4_address_invalid(self):
        assert is_ipv4_address("192.168.1.256") is False
        assert is_ipv4_address("hostname") is False
        assert is_ipv4_address("") is False

    def test_is_valid_cidr(self):
        assert is_valid_cidr("192.168.0.0/24") is True
        assert is_valid_cidr("10.0.0.0/8") is True

    def test_is_valid_cidr_invalid(self):
        assert is_valid_cidr("192.168.0.0") is False
        assert is_valid_cidr("192.168.0.0/33") is False
