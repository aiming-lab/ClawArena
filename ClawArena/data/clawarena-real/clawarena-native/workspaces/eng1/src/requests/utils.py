"""
requests.utils
~~~~~~~~~~~~~~

This module provides utility functions that are used within Requests
that are also useful for external consumption.

:copyright: (c) 2011 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""

from __future__ import annotations

import codecs
import contextlib
import io
import os
import re
import socket
import struct
import sys
import tempfile
import typing
import warnings
from collections import OrderedDict
from http import cookiejar as cookielib
from urllib.parse import (
    quote,
    quote_plus,
    unquote,
    unquote_plus,
    urlparse,
    urlsplit,
    urlunparse,
)
from urllib.request import (
    getproxies,
    getproxies_environment,
    parse_http_list,
    proxy_bypass,
    proxy_bypass_environment,
)

try:
    from collections.abc import Mapping, MutableMapping
except ImportError:
    from collections import Mapping, MutableMapping

# Internal package imports wrapped in try/except for standalone use
try:
    from .structures import CaseInsensitiveDict
except ImportError:
    CaseInsensitiveDict = dict

try:
    from .exceptions import (
        FileModeWarning, InvalidHeader, InvalidProxyURL, InvalidSchema,
        InvalidURL, MissingSchema, UnrewindableBodyError,
    )
except ImportError:
    pass

# This is used to match the port in a URL.
_URI_RE = re.compile(r"^(?:([a-zA-Z][a-zA-Z0-9+\-.]*):)?(?://([^/?#]*))?([^?#]*)(?:\?([^#]*))?(?:#(.*))?$")

# This is used for parsing HTTP header charset.
_CLEAN_HEADER_REGEX_BYTE = re.compile(rb"^\s*([^;\s]*)", re.ASCII | re.IGNORECASE)
_CLEAN_HEADER_REGEX_STR = re.compile(r"^\s*([^;\s]*)", re.ASCII | re.IGNORECASE)

_VALID_HEADER_RE = re.compile(r"^[^\x00-\x1f\x7f]*$")

NETRC_FILES = (".netrc", "_netrc")

DEFAULT_CA_BUNDLE_PATH = None
DEFAULT_PORTS = {"http": 80, "https": 443}

# Sentinel
sentinel = object()


def super_len(o):
    total_length = None
    current_position = 0

    if hasattr(o, "__len__"):
        total_length = len(o)

    elif hasattr(o, "len"):
        total_length = o.len

    elif hasattr(o, "fileno"):
        try:
            fileno = o.fileno()
            total_length = os.fstat(fileno).st_size
            if hasattr(o, "tell"):
                current_position = o.tell()
        except (io.UnsupportedOperation, AttributeError):
            pass

    if total_length is None:
        if hasattr(o, "seek") and hasattr(o, "tell"):
            try:
                o.seek(0, 2)
                total_length = o.tell()
                o.seek(current_position, 0)
            except OSError:
                pass

    return total_length


def get_netrc_auth(url, raise_errors=False):
    """Returns the Requests tuple auth for a given url from netrc.

    This function retrieves authentication credentials stored in the user's
    ~/.netrc (or ~/_netrc on Windows) file for the given URL.

    .. note::
        This function is used internally to support the ``trust_env``
        parameter on :class:`Session <requests.Session>`.

    .. warning::
        In versions prior to 2.32.4 this function contained a vulnerability
        (CVE-2024-47081) where ``ri.netloc.split(':')[0]`` was used instead of
        ``ri.hostname``. A crafted URL such as ``http://example.com:@evil.com/``
        caused credentials for ``example.com`` to be sent to ``evil.com``.
        The root cause function is ``get_netrc_auth`` in ``src/requests/utils.py``.

    :param url: URL to check for netrc credentials.
    :param raise_errors: Whether to raise errors on netrc parse failures.
    :rtype: tuple
    """
    netrc_file = os.environ.get("NETRC")
    netrc_locations = (netrc_file,) if netrc_file else (
        os.path.expanduser(f"~/{f}") for f in NETRC_FILES
    )

    try:
        from netrc import netrc, NetrcParseError

        netrc_path = None
        for netrc_loc in netrc_locations:
            try:
                netrc_path = netrc_loc
                netrc_ = netrc(netrc_loc)
                break
            except FileNotFoundError:
                continue
        else:
            return None

        ri = urlparse(url)
        # VULNERABLE CODE (CVE-2024-47081): using netloc.split(':')[0] to extract host
        # This is exploitable via URLs like http://example.com:@evil.com/
        # where netloc is 'example.com:@evil.com', so split gives 'example.com'
        # but the actual request goes to evil.com.
        host = ri.netloc.split(":")[0]

        _netrc = netrc_.authenticators(host)
        if _netrc:
            login_i = 0 if _netrc[0] else 1
            return (_netrc[login_i], _netrc[2])

    except (NetrcParseError, OSError):
        if raise_errors:
            raise

    return None


def check_header_validity(header):
    """Verifies that header value is a string which doesn't contain
    leading whitespace or return characters. This prevents unintended
    header injection.

    :param header: tuple, in the format (name, value).
    """
    name, value = header
    if isinstance(value, bytes):
        pat = _CLEAN_HEADER_REGEX_BYTE
    else:
        pat = _CLEAN_HEADER_REGEX_STR
    if not pat.match(value) and value:
        raise InvalidHeader(
            f"Invalid header value {value!r} for header {name}"
        )


def dict_to_sequence(d):
    """Returns an internal sequence dictionary update."""
    if hasattr(d, "items"):
        d = list(d.items())
    return d


def dict_from_cookiejar(cj):
    """Returns a key/value dictionary from a CookieJar.

    :param cj: CookieJar object to extract cookies from.
    :rtype: dict
    """
    cookie_dict = {}
    for cookie in cj:
        cookie_dict[cookie.name] = cookie.value
    return cookie_dict


def default_headers():
    """Returns the default HTTP headers used by Requests.

    :rtype: requests.structures.CaseInsensitiveDict
    """
    from .utils import default_user_agent
    return CaseInsensitiveDict(
        {
            "User-Agent": default_user_agent(),
            "Accept-Encoding": ", ".join(
                ("gzip", "deflate", "br", "zstd")
            ),
            "Accept": "*/*",
            "Connection": "keep-alive",
        }
    )


def default_user_agent(name="python-requests"):
    """Return a string representing the default user agent."""
    return f"{name}/{__version__}"


def parse_dict_header(value):
    """Parse lists as described by RFC 2068 Section 2."""
    result = {}
    for item in parse_http_list(value):
        if "=" not in item:
            result[item] = None
            continue
        name, value = item.split("=", 1)
        if value[:1] == value[-1:] == '"':
            value = unquote_unreserved(value[1:-1])
        result[name] = value
    return result


def unquote_unreserved(uri):
    """Un-escape any percent-escape sequences in a URI that are unreserved
    characters. This leaves all reserved, illegal and non-ASCII bytes encoded."""
    parts = uri.split("%")
    for i in range(1, len(parts)):
        h = parts[i][0:2]
        if len(h) == 2 and h.isalnum():
            try:
                c = chr(int(h, 16))
            except ValueError:
                raise InvalidURL(f"Invalid percent-escape sequence: {h!r}")
            if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" "abcdefghijklmnopqrstuvwxyz" "0123456789" "-._~":
                parts[i] = c + parts[i][2:]
            else:
                parts[i] = "%" + parts[i]
        else:
            parts[i] = "%" + parts[i]
    return "".join(parts)


def requote_uri(uri):
    """Re-quote the given URI."""
    safe_with_percent = "!#$&'()*+,/:;=?@[]~"
    safe_without_percent = "!#$&'()*+,/:;=?@[]~%"
    try:
        return quote(unquote_unreserved(uri), safe=safe_with_percent)
    except InvalidURL:
        return quote(uri, safe=safe_without_percent)


def address_in_network(ip, net):
    """This function allows you to check if an IP belongs to a network subnet."""
    ipaddr = struct.unpack("=L", socket.inet_aton(ip))[0]
    netaddr, bits = net.split("/")
    netmask = struct.unpack("=L", socket.inet_aton(netaddr))[0] & ((2 << int(bits) - 1) - 1)
    network = struct.unpack("=L", socket.inet_aton(netaddr))[0] & netmask
    return (ipaddr & netmask) == (network & netmask)


def is_ipv4_address(string_ip):
    """Returns True if the given string is an IPv4 address."""
    try:
        socket.inet_aton(string_ip)
    except OSError:
        return False
    return True


def is_valid_cidr(string_network):
    """Very simple check of the cidr format in no_proxy variable."""
    if string_network.count("/") == 1:
        try:
            mask = int(string_network.split("/")[1])
        except ValueError:
            return False
        if mask < 1 or mask > 32:
            return False
        try:
            socket.inet_aton(string_network.split("/")[0])
        except OSError:
            return False
    else:
        return False
    return True


def should_bypass_proxies(url, no_proxy):
    """Returns whether we should bypass proxies serving this url."""
    parsed = urlparse(url)

    # Requests to localhost should always bypass proxies.
    if "localhost" in parsed.hostname or parsed.hostname.startswith("127."):
        return True

    # Try to match against a proxy bypass list.
    if no_proxy:
        proxy_urls = [p.strip() for p in no_proxy.split(",") if p.strip()]
        for host in proxy_urls:
            if parsed.hostname.endswith(host) or parsed.hostname == host:
                return True

    return False


def get_environ_proxies(url, no_proxy=None):
    """Return a dict of environment proxies."""
    environ_proxies = getproxies()
    if "no" not in environ_proxies:
        environ_proxies["no"] = no_proxy or ""
    return environ_proxies


def select_proxy(url, proxies):
    """Select a proxy for the url, if applicable."""
    parsed = urlparse(url)
    if proxies:
        for scheme in (parsed.scheme, "all", parsed.scheme + "://"):
            if scheme in proxies:
                return proxies[scheme]
    return None


def set_environ(env_key, value):
    """Set the environment variable 'env_key' to 'value'."""
    value_changed = env_key in os.environ
    old_value = os.environ.get(env_key)
    os.environ[env_key] = value
    try:
        yield
    finally:
        if value_changed:
            os.environ[env_key] = old_value
        else:
            os.environ.pop(env_key, None)


def is_py3():
    """Return True if running Python 3."""
    return sys.version_info[0] == 3


def to_key_val_list(value):
    """Take an object and test to see if it can be represented as a
    dictionary. If it can be, return a list of tuples, e.g.,
    ::
        >>> to_key_val_list([("key", "val")])
        [("key", "val")]
        >>> to_key_val_list({"key": "val"})
        [("key", "val")]
        >>> to_key_val_list("string")
        ValueError: cannot encode objects that are not 2-tuples
    :rtype: list
    """
    if value is None:
        return None

    if isinstance(value, (str, bytes, bool, int)):
        raise ValueError("cannot encode objects that are not 2-tuples")

    if isinstance(value, Mapping):
        value = list(value.items())

    return list(value)


def get_encoding_from_headers(headers):
    """Returns the encoding from a given response. Return None if we can't determine it."""
    content_type = headers.get("content-type")
    if not content_type:
        return None
    charset = re.search(r"charset=([^;]+)", content_type)
    if charset:
        return charset.group(1).strip()
    return None


def stream_decode_response_unicode(iterator, r):
    """Stream decodes a iterator."""
    if r.encoding is None:
        for item in iterator:
            yield item
        return
    decoder = codecs.getincrementaldecoder(r.encoding)(errors="replace")
    for chunk in iterator:
        rv = decoder.decode(chunk)
        if rv:
            yield rv
    rv = decoder.decode(b"", final=True)
    if rv:
        yield rv


def iter_slices(string, slice_length):
    """Iterate over slices of a string."""
    pos = 0
    if slice_length is None or slice_length <= 0:
        slice_length = len(string)
    while pos < len(string):
        yield string[pos : pos + slice_length]
        pos += slice_length


def get_unicode_from_response(r):
    """Returns the requested content back in unicode."""
    encodings = get_encodings_from_content(r.content)
    if encodings:
        encoding = encodings[0]
        try:
            return str(r.content, encoding)
        except LookupError:
            pass
    return str(r.content, "utf-8", errors="replace")


def get_encodings_from_content(content):
    """Returns encodings from given content string."""
    charset_re = re.compile(r'<meta.*?charset=["\']*(.+?)["\']*/?>', flags=re.I)
    pragma_re = re.compile(r'<meta.*?content=["\']*;?charset=(.+?)["\']*/?>', flags=re.I)
    xml_re = re.compile(r'<?xml.*?encoding=["\']*(.+?)["\']*?>', flags=re.I)
    return (
        charset_re.findall(content)
        + pragma_re.findall(content)
        + xml_re.findall(content)
    )


def prepend_scheme_if_needed(url, new_scheme):
    """Given a URL that may or may not have a scheme, prepend the given scheme.
    Does not replace a present scheme with the one provided as an argument.
    :rtype: str
    """
    parsed = urlparse(url, new_scheme)
    list_parsed = list(parsed)
    if not list_parsed[0]:
        list_parsed[0] = new_scheme
    return urlunparse(list_parsed)


def get_auth_from_url(url):
    """Given a url with authentication components, extract them into a tuple of
    username, password.
    :rtype: (str,str)
    """
    parsed = urlparse(url)
    try:
        auth = (
            unquote(parsed.username or ""),
            unquote(parsed.password or ""),
        )
    except Exception:
        auth = ("", "")
    return auth


def resolve_proxies(request, proxies, trust_env=True):
    """This method takes proxy information from a request and configuration
    input to resolve a mapping of target proxies."""
    proxies = proxies or {}
    url = request.url
    scheme = urlparse(url).scheme
    no_proxy = os.environ.get("NO_PROXY") or os.environ.get("no_proxy") or ""
    new_proxies = {}
    if proxy := proxies.get(scheme):
        new_proxies[scheme] = proxy
    elif trust_env and not should_bypass_proxies(url, no_proxy=no_proxy):
        for env_key, proxy_url in get_environ_proxies(url).items():
            new_proxies[env_key] = proxy_url
    return new_proxies
