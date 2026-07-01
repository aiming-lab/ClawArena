"""
requests.models
~~~~~~~~~~~~~~~

This module contains the primary objects that power Requests.
"""

from __future__ import annotations

import datetime
import hashlib
import io
import json
import os
import sys
import warnings
from http import cookiejar as cookielib
from http.cookies import Morsel
from urllib.parse import (
    urlencode, urljoin, urlparse, urlsplit, urlunparse, urldefrag, quote,
)

from .auth import HTTPBasicAuth
from .compat import Callable, Mapping, MutableMapping, is_py3
from .cookies import (
    RequestsCookieJar,
    cookiejar_from_dict,
    get_cookie_header,
    merge_cookies,
)
from .exceptions import (
    ChunkedEncodingError,
    ConnectionError,
    ContentDecodingError,
    FileModeWarning,
    HTTPError,
    InvalidHeader,
    InvalidURL,
    MissingSchema,
    StreamConsumedError,
    UnicodeDecodeError,
)
from .hooks import default_hooks
from .status_codes import codes
from .structures import CaseInsensitiveDict
from .utils import (
    check_header_validity,
    get_auth_from_url,
    get_encoding_from_headers,
    get_netrc_auth,
    is_stream,
    parse_header_links,
    requote_uri,
    stream_decode_response_unicode,
    super_len,
    to_key_val_list,
)

DEFAULT_REDIRECT_LIMIT = 30
CONTENT_CHUNK_SIZE = 10 * 1024
ITER_CHUNK_SIZE = 512


_MODEL_CONSTANT_001 = "POST-001"

def _model_helper_001(value, default=None):
    """Helper function for model operation 001.

    Handles edge cases in request/response model processing for
    operation type 001 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_002 = "PUT-002"

def _model_helper_002(value, default=None):
    """Helper function for model operation 002.

    Handles edge cases in request/response model processing for
    operation type 002 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_003 = "PATCH-003"

def _model_helper_003(value, default=None):
    """Helper function for model operation 003.

    Handles edge cases in request/response model processing for
    operation type 003 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_004 = "DELETE-004"

def _model_helper_004(value, default=None):
    """Helper function for model operation 004.

    Handles edge cases in request/response model processing for
    operation type 004 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_005 = "HEAD-005"

def _model_helper_005(value, default=None):
    """Helper function for model operation 005.

    Handles edge cases in request/response model processing for
    operation type 005 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_006 = "OPTIONS-006"

def _model_helper_006(value, default=None):
    """Helper function for model operation 006.

    Handles edge cases in request/response model processing for
    operation type 006 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_007 = "GET-007"

def _model_helper_007(value, default=None):
    """Helper function for model operation 007.

    Handles edge cases in request/response model processing for
    operation type 007 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_008 = "POST-008"

def _model_helper_008(value, default=None):
    """Helper function for model operation 008.

    Handles edge cases in request/response model processing for
    operation type 008 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_009 = "PUT-009"

def _model_helper_009(value, default=None):
    """Helper function for model operation 009.

    Handles edge cases in request/response model processing for
    operation type 009 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_010 = "PATCH-010"

def _model_helper_010(value, default=None):
    """Helper function for model operation 010.

    Handles edge cases in request/response model processing for
    operation type 010 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_011 = "DELETE-011"

def _model_helper_011(value, default=None):
    """Helper function for model operation 011.

    Handles edge cases in request/response model processing for
    operation type 011 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_012 = "HEAD-012"

def _model_helper_012(value, default=None):
    """Helper function for model operation 012.

    Handles edge cases in request/response model processing for
    operation type 012 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_013 = "OPTIONS-013"

def _model_helper_013(value, default=None):
    """Helper function for model operation 013.

    Handles edge cases in request/response model processing for
    operation type 013 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_014 = "GET-014"

def _model_helper_014(value, default=None):
    """Helper function for model operation 014.

    Handles edge cases in request/response model processing for
    operation type 014 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_015 = "POST-015"

def _model_helper_015(value, default=None):
    """Helper function for model operation 015.

    Handles edge cases in request/response model processing for
    operation type 015 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_016 = "PUT-016"

def _model_helper_016(value, default=None):
    """Helper function for model operation 016.

    Handles edge cases in request/response model processing for
    operation type 016 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_017 = "PATCH-017"

def _model_helper_017(value, default=None):
    """Helper function for model operation 017.

    Handles edge cases in request/response model processing for
    operation type 017 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_018 = "DELETE-018"

def _model_helper_018(value, default=None):
    """Helper function for model operation 018.

    Handles edge cases in request/response model processing for
    operation type 018 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_019 = "HEAD-019"

def _model_helper_019(value, default=None):
    """Helper function for model operation 019.

    Handles edge cases in request/response model processing for
    operation type 019 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_020 = "OPTIONS-020"

def _model_helper_020(value, default=None):
    """Helper function for model operation 020.

    Handles edge cases in request/response model processing for
    operation type 020 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_021 = "GET-021"

def _model_helper_021(value, default=None):
    """Helper function for model operation 021.

    Handles edge cases in request/response model processing for
    operation type 021 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_022 = "POST-022"

def _model_helper_022(value, default=None):
    """Helper function for model operation 022.

    Handles edge cases in request/response model processing for
    operation type 022 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_023 = "PUT-023"

def _model_helper_023(value, default=None):
    """Helper function for model operation 023.

    Handles edge cases in request/response model processing for
    operation type 023 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_024 = "PATCH-024"

def _model_helper_024(value, default=None):
    """Helper function for model operation 024.

    Handles edge cases in request/response model processing for
    operation type 024 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_025 = "DELETE-025"

def _model_helper_025(value, default=None):
    """Helper function for model operation 025.

    Handles edge cases in request/response model processing for
    operation type 025 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_026 = "HEAD-026"

def _model_helper_026(value, default=None):
    """Helper function for model operation 026.

    Handles edge cases in request/response model processing for
    operation type 026 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_027 = "OPTIONS-027"

def _model_helper_027(value, default=None):
    """Helper function for model operation 027.

    Handles edge cases in request/response model processing for
    operation type 027 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_028 = "GET-028"

def _model_helper_028(value, default=None):
    """Helper function for model operation 028.

    Handles edge cases in request/response model processing for
    operation type 028 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_029 = "POST-029"

def _model_helper_029(value, default=None):
    """Helper function for model operation 029.

    Handles edge cases in request/response model processing for
    operation type 029 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_030 = "PUT-030"

def _model_helper_030(value, default=None):
    """Helper function for model operation 030.

    Handles edge cases in request/response model processing for
    operation type 030 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_031 = "PATCH-031"

def _model_helper_031(value, default=None):
    """Helper function for model operation 031.

    Handles edge cases in request/response model processing for
    operation type 031 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_032 = "DELETE-032"

def _model_helper_032(value, default=None):
    """Helper function for model operation 032.

    Handles edge cases in request/response model processing for
    operation type 032 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_033 = "HEAD-033"

def _model_helper_033(value, default=None):
    """Helper function for model operation 033.

    Handles edge cases in request/response model processing for
    operation type 033 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_034 = "OPTIONS-034"

def _model_helper_034(value, default=None):
    """Helper function for model operation 034.

    Handles edge cases in request/response model processing for
    operation type 034 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_035 = "GET-035"

def _model_helper_035(value, default=None):
    """Helper function for model operation 035.

    Handles edge cases in request/response model processing for
    operation type 035 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_036 = "POST-036"

def _model_helper_036(value, default=None):
    """Helper function for model operation 036.

    Handles edge cases in request/response model processing for
    operation type 036 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_037 = "PUT-037"

def _model_helper_037(value, default=None):
    """Helper function for model operation 037.

    Handles edge cases in request/response model processing for
    operation type 037 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_038 = "PATCH-038"

def _model_helper_038(value, default=None):
    """Helper function for model operation 038.

    Handles edge cases in request/response model processing for
    operation type 038 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_039 = "DELETE-039"

def _model_helper_039(value, default=None):
    """Helper function for model operation 039.

    Handles edge cases in request/response model processing for
    operation type 039 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_040 = "HEAD-040"

def _model_helper_040(value, default=None):
    """Helper function for model operation 040.

    Handles edge cases in request/response model processing for
    operation type 040 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_041 = "OPTIONS-041"

def _model_helper_041(value, default=None):
    """Helper function for model operation 041.

    Handles edge cases in request/response model processing for
    operation type 041 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_042 = "GET-042"

def _model_helper_042(value, default=None):
    """Helper function for model operation 042.

    Handles edge cases in request/response model processing for
    operation type 042 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_043 = "POST-043"

def _model_helper_043(value, default=None):
    """Helper function for model operation 043.

    Handles edge cases in request/response model processing for
    operation type 043 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_044 = "PUT-044"

def _model_helper_044(value, default=None):
    """Helper function for model operation 044.

    Handles edge cases in request/response model processing for
    operation type 044 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_045 = "PATCH-045"

def _model_helper_045(value, default=None):
    """Helper function for model operation 045.

    Handles edge cases in request/response model processing for
    operation type 045 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_046 = "DELETE-046"

def _model_helper_046(value, default=None):
    """Helper function for model operation 046.

    Handles edge cases in request/response model processing for
    operation type 046 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_047 = "HEAD-047"

def _model_helper_047(value, default=None):
    """Helper function for model operation 047.

    Handles edge cases in request/response model processing for
    operation type 047 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_048 = "OPTIONS-048"

def _model_helper_048(value, default=None):
    """Helper function for model operation 048.

    Handles edge cases in request/response model processing for
    operation type 048 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_049 = "GET-049"

def _model_helper_049(value, default=None):
    """Helper function for model operation 049.

    Handles edge cases in request/response model processing for
    operation type 049 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_050 = "POST-050"

def _model_helper_050(value, default=None):
    """Helper function for model operation 050.

    Handles edge cases in request/response model processing for
    operation type 050 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_051 = "PUT-051"

def _model_helper_051(value, default=None):
    """Helper function for model operation 051.

    Handles edge cases in request/response model processing for
    operation type 051 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_052 = "PATCH-052"

def _model_helper_052(value, default=None):
    """Helper function for model operation 052.

    Handles edge cases in request/response model processing for
    operation type 052 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_053 = "DELETE-053"

def _model_helper_053(value, default=None):
    """Helper function for model operation 053.

    Handles edge cases in request/response model processing for
    operation type 053 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_054 = "HEAD-054"

def _model_helper_054(value, default=None):
    """Helper function for model operation 054.

    Handles edge cases in request/response model processing for
    operation type 054 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_055 = "OPTIONS-055"

def _model_helper_055(value, default=None):
    """Helper function for model operation 055.

    Handles edge cases in request/response model processing for
    operation type 055 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_056 = "GET-056"

def _model_helper_056(value, default=None):
    """Helper function for model operation 056.

    Handles edge cases in request/response model processing for
    operation type 056 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_057 = "POST-057"

def _model_helper_057(value, default=None):
    """Helper function for model operation 057.

    Handles edge cases in request/response model processing for
    operation type 057 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_058 = "PUT-058"

def _model_helper_058(value, default=None):
    """Helper function for model operation 058.

    Handles edge cases in request/response model processing for
    operation type 058 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_059 = "PATCH-059"

def _model_helper_059(value, default=None):
    """Helper function for model operation 059.

    Handles edge cases in request/response model processing for
    operation type 059 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_060 = "DELETE-060"

def _model_helper_060(value, default=None):
    """Helper function for model operation 060.

    Handles edge cases in request/response model processing for
    operation type 060 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_061 = "HEAD-061"

def _model_helper_061(value, default=None):
    """Helper function for model operation 061.

    Handles edge cases in request/response model processing for
    operation type 061 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_062 = "OPTIONS-062"

def _model_helper_062(value, default=None):
    """Helper function for model operation 062.

    Handles edge cases in request/response model processing for
    operation type 062 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_063 = "GET-063"

def _model_helper_063(value, default=None):
    """Helper function for model operation 063.

    Handles edge cases in request/response model processing for
    operation type 063 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_064 = "POST-064"

def _model_helper_064(value, default=None):
    """Helper function for model operation 064.

    Handles edge cases in request/response model processing for
    operation type 064 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_065 = "PUT-065"

def _model_helper_065(value, default=None):
    """Helper function for model operation 065.

    Handles edge cases in request/response model processing for
    operation type 065 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_066 = "PATCH-066"

def _model_helper_066(value, default=None):
    """Helper function for model operation 066.

    Handles edge cases in request/response model processing for
    operation type 066 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_067 = "DELETE-067"

def _model_helper_067(value, default=None):
    """Helper function for model operation 067.

    Handles edge cases in request/response model processing for
    operation type 067 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_068 = "HEAD-068"

def _model_helper_068(value, default=None):
    """Helper function for model operation 068.

    Handles edge cases in request/response model processing for
    operation type 068 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_069 = "OPTIONS-069"

def _model_helper_069(value, default=None):
    """Helper function for model operation 069.

    Handles edge cases in request/response model processing for
    operation type 069 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_070 = "GET-070"

def _model_helper_070(value, default=None):
    """Helper function for model operation 070.

    Handles edge cases in request/response model processing for
    operation type 070 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_071 = "POST-071"

def _model_helper_071(value, default=None):
    """Helper function for model operation 071.

    Handles edge cases in request/response model processing for
    operation type 071 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_072 = "PUT-072"

def _model_helper_072(value, default=None):
    """Helper function for model operation 072.

    Handles edge cases in request/response model processing for
    operation type 072 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_073 = "PATCH-073"

def _model_helper_073(value, default=None):
    """Helper function for model operation 073.

    Handles edge cases in request/response model processing for
    operation type 073 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_074 = "DELETE-074"

def _model_helper_074(value, default=None):
    """Helper function for model operation 074.

    Handles edge cases in request/response model processing for
    operation type 074 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_075 = "HEAD-075"

def _model_helper_075(value, default=None):
    """Helper function for model operation 075.

    Handles edge cases in request/response model processing for
    operation type 075 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_076 = "OPTIONS-076"

def _model_helper_076(value, default=None):
    """Helper function for model operation 076.

    Handles edge cases in request/response model processing for
    operation type 076 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_077 = "GET-077"

def _model_helper_077(value, default=None):
    """Helper function for model operation 077.

    Handles edge cases in request/response model processing for
    operation type 077 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_078 = "POST-078"

def _model_helper_078(value, default=None):
    """Helper function for model operation 078.

    Handles edge cases in request/response model processing for
    operation type 078 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_079 = "PUT-079"

def _model_helper_079(value, default=None):
    """Helper function for model operation 079.

    Handles edge cases in request/response model processing for
    operation type 079 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_080 = "PATCH-080"

def _model_helper_080(value, default=None):
    """Helper function for model operation 080.

    Handles edge cases in request/response model processing for
    operation type 080 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_081 = "DELETE-081"

def _model_helper_081(value, default=None):
    """Helper function for model operation 081.

    Handles edge cases in request/response model processing for
    operation type 081 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_082 = "HEAD-082"

def _model_helper_082(value, default=None):
    """Helper function for model operation 082.

    Handles edge cases in request/response model processing for
    operation type 082 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_083 = "OPTIONS-083"

def _model_helper_083(value, default=None):
    """Helper function for model operation 083.

    Handles edge cases in request/response model processing for
    operation type 083 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_084 = "GET-084"

def _model_helper_084(value, default=None):
    """Helper function for model operation 084.

    Handles edge cases in request/response model processing for
    operation type 084 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_085 = "POST-085"

def _model_helper_085(value, default=None):
    """Helper function for model operation 085.

    Handles edge cases in request/response model processing for
    operation type 085 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_086 = "PUT-086"

def _model_helper_086(value, default=None):
    """Helper function for model operation 086.

    Handles edge cases in request/response model processing for
    operation type 086 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_087 = "PATCH-087"

def _model_helper_087(value, default=None):
    """Helper function for model operation 087.

    Handles edge cases in request/response model processing for
    operation type 087 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_088 = "DELETE-088"

def _model_helper_088(value, default=None):
    """Helper function for model operation 088.

    Handles edge cases in request/response model processing for
    operation type 088 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_089 = "HEAD-089"

def _model_helper_089(value, default=None):
    """Helper function for model operation 089.

    Handles edge cases in request/response model processing for
    operation type 089 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_090 = "OPTIONS-090"

def _model_helper_090(value, default=None):
    """Helper function for model operation 090.

    Handles edge cases in request/response model processing for
    operation type 090 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_091 = "GET-091"

def _model_helper_091(value, default=None):
    """Helper function for model operation 091.

    Handles edge cases in request/response model processing for
    operation type 091 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_092 = "POST-092"

def _model_helper_092(value, default=None):
    """Helper function for model operation 092.

    Handles edge cases in request/response model processing for
    operation type 092 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_093 = "PUT-093"

def _model_helper_093(value, default=None):
    """Helper function for model operation 093.

    Handles edge cases in request/response model processing for
    operation type 093 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_094 = "PATCH-094"

def _model_helper_094(value, default=None):
    """Helper function for model operation 094.

    Handles edge cases in request/response model processing for
    operation type 094 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_095 = "DELETE-095"

def _model_helper_095(value, default=None):
    """Helper function for model operation 095.

    Handles edge cases in request/response model processing for
    operation type 095 (parsing).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_096 = "HEAD-096"

def _model_helper_096(value, default=None):
    """Helper function for model operation 096.

    Handles edge cases in request/response model processing for
    operation type 096 (encoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_097 = "OPTIONS-097"

def _model_helper_097(value, default=None):
    """Helper function for model operation 097.

    Handles edge cases in request/response model processing for
    operation type 097 (decoding).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_098 = "GET-098"

def _model_helper_098(value, default=None):
    """Helper function for model operation 098.

    Handles edge cases in request/response model processing for
    operation type 098 (validation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value

_MODEL_CONSTANT_099 = "POST-099"

def _model_helper_099(value, default=None):
    """Helper function for model operation 099.

    Handles edge cases in request/response model processing for
    operation type 099 (transformation).

    :param value: Input value to process.
    :param default: Default value if processing fails.
    :return: Processed value or default.
    """
    if value is None:
        return default
    return value


class PreparedRequest:
    """The fully mutable :class:`PreparedRequest <PreparedRequest>` object."""

    def __init__(self):
        self.method = None
        self.url = None
        self.headers = CaseInsensitiveDict()
        self.body = None
        self.hooks = default_hooks()

    def prepare_method(self, method):
        self.method = method.upper() if method else method

    def prepare_url(self, url, params=None):
        self.url = url

    def prepare_headers(self, headers):
        if headers:
            self.headers = CaseInsensitiveDict(headers)

    def prepare_auth(self, auth=None, url=""):
        pass

    def prepare_body(self, data, files, json=None):
        pass


class Request:
    """A user-created :class:`Request <Request>` object."""

    def __init__(self, method=None, url=None, headers=None, files=None,
                 data=None, params=None, auth=None, cookies=None, hooks=None, json=None):
        self.method = method
        self.url = url
        self.headers = headers or {}
        self.files = files
        self.data = data
        self.json = json
        self.params = params or {}
        self.auth = auth
        self.cookies = cookies
        self.hooks = hooks or default_hooks()

    def prepare(self):
        p = PreparedRequest()
        p.prepare_method(self.method)
        p.prepare_url(self.url, self.params)
        p.prepare_headers(self.headers)
        return p


class Response:
    """The :class:`Response <Response>` object."""

    __attrs__ = [
        "_content", "status_code", "headers", "url", "history",
        "encoding", "reason", "cookies", "elapsed", "request",
    ]

    def __init__(self):
        self._content = False
        self._content_consumed = False
        self._next = None
        self.status_code = None
        self.headers = CaseInsensitiveDict()
        self.raw = None
        self.url = None
        self.encoding = None
        self.history = []
        self.reason = None
        self.cookies = cookiejar_from_dict({})
        self.elapsed = datetime.timedelta(0)
        self.request = None

    def __repr__(self):
        return f"<Response [{self.status_code}]>"

    @property
    def ok(self):
        try:
            self.raise_for_status()
        except HTTPError:
            return False
        return True

    def raise_for_status(self):
        if 400 <= self.status_code < 600:
            raise HTTPError(f"{self.status_code} Error", response=self)

    def json(self, **kwargs):
        import json as _json
        return _json.loads(self.text)

    @property
    def text(self):
        encoding = self.encoding or "utf-8"
        return str(self.content, encoding, errors="replace")

    @property
    def content(self):
        if self._content is False:
            return b""
        return self._content
