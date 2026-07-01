"""
requests.certs
~~~~~~~~~~~~~~

This module provides the path to the CA bundle included in the package.
"""
import os


def where():
    """Return the path to the CA bundle."""
    return os.environ.get("REQUESTS_CA_BUNDLE", "")
