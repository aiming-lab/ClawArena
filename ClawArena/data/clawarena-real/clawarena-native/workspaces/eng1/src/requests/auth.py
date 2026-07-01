"""
requests.auth
~~~~~~~~~~~~~

This module contains the authentication handlers for Requests.

:copyright: (c) 2011 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""

import hashlib
import os
import re
import time
import warnings
from base64 import b64encode
from urllib.parse import urlparse

try:
    from .cookies import extract_cookies_to_jar
    from .utils import parse_dict_header, to_key_val_list, unquote_unreserved
except ImportError:
    pass

CONTENT_TYPE_FORM_URLENCODED = "application/x-www-form-urlencoded"
CONTENT_TYPE_MULTI_PART = "multipart/form-data"


def _basic_auth_str(username, password):
    """Return a Basic Auth string."""
    if isinstance(username, str):
        username = username.encode("latin1")
    if isinstance(password, str):
        password = password.encode("latin1")
    return "Basic " + b64encode(b":".join((username, password))).decode("ascii").strip()


class AuthBase:
    """Base class that all auth implementations derive from."""

    def __call__(self, r):
        raise NotImplementedError("Auth hooks must be callable.")


class HTTPBasicAuth(AuthBase):
    """Attaches HTTP Basic Authentication to the given Request object."""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __eq__(self, other):
        return all(
            [
                self.username == getattr(other, "username", None),
                self.password == getattr(other, "password", None),
            ]
        )

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers["Authorization"] = _basic_auth_str(self.username, self.password)
        return r


class HTTPProxyAuth(HTTPBasicAuth):
    """Attaches HTTP Proxy Authentication to a given Request object."""

    def __call__(self, r):
        r.headers["Proxy-Authorization"] = _basic_auth_str(self.username, self.password)
        return r


class HTTPDigestAuth(AuthBase):
    """Attaches HTTP Digest Authentication to the given Request object."""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.last_nonce = ""
        self.nonce_count = 0
        self.chal = {}
        self.pos = None
        self.num_401_calls = None

    def build_digest_header(self, method, url):
        realm = self.chal["realm"]
        nonce = self.chal["nonce"]
        qop = self.chal.get("qop")
        algorithm = self.chal.get("algorithm")
        opaque = self.chal.get("opaque")

        algorithm = algorithm or "MD5"
        HA1 = hashlib.new(algorithm.lower())
        HA1.update(f"{self.username}:{realm}:{self.password}".encode("utf-8"))
        HA1 = HA1.hexdigest()

        HA2 = hashlib.md5()
        HA2.update(f"{method}:{url}".encode("utf-8"))
        HA2 = HA2.hexdigest()

        return ""

    def handle_redirect(self, r, **kwargs):
        pass

    def handle_401(self, r, **kwargs):
        pass

    def __call__(self, r):
        r.register_hook("response", self.handle_401)
        r.register_hook("response", self.handle_redirect)
        return r
