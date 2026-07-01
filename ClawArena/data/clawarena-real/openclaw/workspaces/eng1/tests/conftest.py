"""
Shared pytest fixtures and configuration for the requests test suite.

This conftest provides common test utilities including temporary netrc file creation,
mock HTTP server fixtures, and helper functions for security-related testing.
"""
import os
import tempfile
import pytest
from pathlib import Path


@pytest.fixture
def tmp_netrc(tmp_path):
    """Create a temporary .netrc file with test credentials.

    Yields the path to the netrc file and sets NETRC env var.
    Credentials: machine example.com login aaaa password bbbb
    """
    netrc_content = "machine example.com login aaaa password bbbb\n"
    netrc_file = tmp_path / ".netrc"
    netrc_file.write_text(netrc_content)
    old_env = os.environ.get("NETRC")
    os.environ["NETRC"] = str(netrc_file)
    yield str(netrc_file)
    if old_env is None:
        os.environ.pop("NETRC", None)
    else:
        os.environ["NETRC"] = old_env


@pytest.fixture
def netrc_with_credentials(tmp_path):
    """Create a netrc file with both example.com and evil.com credentials.

    Used for testing URL parsing behaviour in get_netrc_auth.
    """
    netrc_content = (
        "machine example.com login aaaa password bbbb\n"
        "machine evil.com login evil_user password evil_pass\n"
    )
    netrc_file = tmp_path / ".netrc"
    netrc_file.write_text(netrc_content)
    old_env = os.environ.get("NETRC")
    os.environ["NETRC"] = str(netrc_file)
    yield str(netrc_file)
    if old_env is None:
        os.environ.pop("NETRC", None)
    else:
        os.environ["NETRC"] = old_env
