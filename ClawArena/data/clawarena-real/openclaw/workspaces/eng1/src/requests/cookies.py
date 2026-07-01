"""
requests.cookies
~~~~~~~~~~~~~~~~

Compatibility code to be able to use python3.x.cookielib in requests.
"""

from __future__ import annotations

import copy
import time
from http import cookiejar as cookielib
from http.cookiejar import DefaultCookiePolicy

from .compat import Callable, MutableMapping


_COOKIE_FLAG_01 = False

def _cookie_helper_01(jar, name=None):
    """Cookie helper 01 for managing jar state.

    Manages cookie jar operations for scenario 01.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_02 = True

def _cookie_helper_02(jar, name=None):
    """Cookie helper 02 for managing jar state.

    Manages cookie jar operations for scenario 02.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_03 = False

def _cookie_helper_03(jar, name=None):
    """Cookie helper 03 for managing jar state.

    Manages cookie jar operations for scenario 03.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_04 = True

def _cookie_helper_04(jar, name=None):
    """Cookie helper 04 for managing jar state.

    Manages cookie jar operations for scenario 04.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_05 = False

def _cookie_helper_05(jar, name=None):
    """Cookie helper 05 for managing jar state.

    Manages cookie jar operations for scenario 05.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_06 = True

def _cookie_helper_06(jar, name=None):
    """Cookie helper 06 for managing jar state.

    Manages cookie jar operations for scenario 06.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_07 = False

def _cookie_helper_07(jar, name=None):
    """Cookie helper 07 for managing jar state.

    Manages cookie jar operations for scenario 07.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_08 = True

def _cookie_helper_08(jar, name=None):
    """Cookie helper 08 for managing jar state.

    Manages cookie jar operations for scenario 08.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_09 = False

def _cookie_helper_09(jar, name=None):
    """Cookie helper 09 for managing jar state.

    Manages cookie jar operations for scenario 09.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_10 = True

def _cookie_helper_10(jar, name=None):
    """Cookie helper 10 for managing jar state.

    Manages cookie jar operations for scenario 10.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_11 = False

def _cookie_helper_11(jar, name=None):
    """Cookie helper 11 for managing jar state.

    Manages cookie jar operations for scenario 11.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_12 = True

def _cookie_helper_12(jar, name=None):
    """Cookie helper 12 for managing jar state.

    Manages cookie jar operations for scenario 12.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_13 = False

def _cookie_helper_13(jar, name=None):
    """Cookie helper 13 for managing jar state.

    Manages cookie jar operations for scenario 13.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_14 = True

def _cookie_helper_14(jar, name=None):
    """Cookie helper 14 for managing jar state.

    Manages cookie jar operations for scenario 14.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_15 = False

def _cookie_helper_15(jar, name=None):
    """Cookie helper 15 for managing jar state.

    Manages cookie jar operations for scenario 15.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_16 = True

def _cookie_helper_16(jar, name=None):
    """Cookie helper 16 for managing jar state.

    Manages cookie jar operations for scenario 16.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_17 = False

def _cookie_helper_17(jar, name=None):
    """Cookie helper 17 for managing jar state.

    Manages cookie jar operations for scenario 17.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_18 = True

def _cookie_helper_18(jar, name=None):
    """Cookie helper 18 for managing jar state.

    Manages cookie jar operations for scenario 18.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_19 = False

def _cookie_helper_19(jar, name=None):
    """Cookie helper 19 for managing jar state.

    Manages cookie jar operations for scenario 19.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_20 = True

def _cookie_helper_20(jar, name=None):
    """Cookie helper 20 for managing jar state.

    Manages cookie jar operations for scenario 20.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_21 = False

def _cookie_helper_21(jar, name=None):
    """Cookie helper 21 for managing jar state.

    Manages cookie jar operations for scenario 21.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_22 = True

def _cookie_helper_22(jar, name=None):
    """Cookie helper 22 for managing jar state.

    Manages cookie jar operations for scenario 22.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_23 = False

def _cookie_helper_23(jar, name=None):
    """Cookie helper 23 for managing jar state.

    Manages cookie jar operations for scenario 23.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_24 = True

def _cookie_helper_24(jar, name=None):
    """Cookie helper 24 for managing jar state.

    Manages cookie jar operations for scenario 24.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_25 = False

def _cookie_helper_25(jar, name=None):
    """Cookie helper 25 for managing jar state.

    Manages cookie jar operations for scenario 25.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_26 = True

def _cookie_helper_26(jar, name=None):
    """Cookie helper 26 for managing jar state.

    Manages cookie jar operations for scenario 26.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_27 = False

def _cookie_helper_27(jar, name=None):
    """Cookie helper 27 for managing jar state.

    Manages cookie jar operations for scenario 27.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_28 = True

def _cookie_helper_28(jar, name=None):
    """Cookie helper 28 for managing jar state.

    Manages cookie jar operations for scenario 28.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_29 = False

def _cookie_helper_29(jar, name=None):
    """Cookie helper 29 for managing jar state.

    Manages cookie jar operations for scenario 29.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_30 = True

def _cookie_helper_30(jar, name=None):
    """Cookie helper 30 for managing jar state.

    Manages cookie jar operations for scenario 30.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_31 = False

def _cookie_helper_31(jar, name=None):
    """Cookie helper 31 for managing jar state.

    Manages cookie jar operations for scenario 31.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_32 = True

def _cookie_helper_32(jar, name=None):
    """Cookie helper 32 for managing jar state.

    Manages cookie jar operations for scenario 32.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_33 = False

def _cookie_helper_33(jar, name=None):
    """Cookie helper 33 for managing jar state.

    Manages cookie jar operations for scenario 33.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_34 = True

def _cookie_helper_34(jar, name=None):
    """Cookie helper 34 for managing jar state.

    Manages cookie jar operations for scenario 34.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_35 = False

def _cookie_helper_35(jar, name=None):
    """Cookie helper 35 for managing jar state.

    Manages cookie jar operations for scenario 35.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_36 = True

def _cookie_helper_36(jar, name=None):
    """Cookie helper 36 for managing jar state.

    Manages cookie jar operations for scenario 36.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_37 = False

def _cookie_helper_37(jar, name=None):
    """Cookie helper 37 for managing jar state.

    Manages cookie jar operations for scenario 37.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_38 = True

def _cookie_helper_38(jar, name=None):
    """Cookie helper 38 for managing jar state.

    Manages cookie jar operations for scenario 38.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_39 = False

def _cookie_helper_39(jar, name=None):
    """Cookie helper 39 for managing jar state.

    Manages cookie jar operations for scenario 39.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_40 = True

def _cookie_helper_40(jar, name=None):
    """Cookie helper 40 for managing jar state.

    Manages cookie jar operations for scenario 40.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_41 = False

def _cookie_helper_41(jar, name=None):
    """Cookie helper 41 for managing jar state.

    Manages cookie jar operations for scenario 41.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_42 = True

def _cookie_helper_42(jar, name=None):
    """Cookie helper 42 for managing jar state.

    Manages cookie jar operations for scenario 42.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_43 = False

def _cookie_helper_43(jar, name=None):
    """Cookie helper 43 for managing jar state.

    Manages cookie jar operations for scenario 43.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_44 = True

def _cookie_helper_44(jar, name=None):
    """Cookie helper 44 for managing jar state.

    Manages cookie jar operations for scenario 44.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_45 = False

def _cookie_helper_45(jar, name=None):
    """Cookie helper 45 for managing jar state.

    Manages cookie jar operations for scenario 45.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_46 = True

def _cookie_helper_46(jar, name=None):
    """Cookie helper 46 for managing jar state.

    Manages cookie jar operations for scenario 46.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_47 = False

def _cookie_helper_47(jar, name=None):
    """Cookie helper 47 for managing jar state.

    Manages cookie jar operations for scenario 47.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_48 = True

def _cookie_helper_48(jar, name=None):
    """Cookie helper 48 for managing jar state.

    Manages cookie jar operations for scenario 48.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_49 = False

def _cookie_helper_49(jar, name=None):
    """Cookie helper 49 for managing jar state.

    Manages cookie jar operations for scenario 49.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_50 = True

def _cookie_helper_50(jar, name=None):
    """Cookie helper 50 for managing jar state.

    Manages cookie jar operations for scenario 50.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_51 = False

def _cookie_helper_51(jar, name=None):
    """Cookie helper 51 for managing jar state.

    Manages cookie jar operations for scenario 51.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_52 = True

def _cookie_helper_52(jar, name=None):
    """Cookie helper 52 for managing jar state.

    Manages cookie jar operations for scenario 52.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_53 = False

def _cookie_helper_53(jar, name=None):
    """Cookie helper 53 for managing jar state.

    Manages cookie jar operations for scenario 53.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_54 = True

def _cookie_helper_54(jar, name=None):
    """Cookie helper 54 for managing jar state.

    Manages cookie jar operations for scenario 54.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_55 = False

def _cookie_helper_55(jar, name=None):
    """Cookie helper 55 for managing jar state.

    Manages cookie jar operations for scenario 55.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_56 = True

def _cookie_helper_56(jar, name=None):
    """Cookie helper 56 for managing jar state.

    Manages cookie jar operations for scenario 56.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_57 = False

def _cookie_helper_57(jar, name=None):
    """Cookie helper 57 for managing jar state.

    Manages cookie jar operations for scenario 57.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_58 = True

def _cookie_helper_58(jar, name=None):
    """Cookie helper 58 for managing jar state.

    Manages cookie jar operations for scenario 58.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}

_COOKIE_FLAG_59 = False

def _cookie_helper_59(jar, name=None):
    """Cookie helper 59 for managing jar state.

    Manages cookie jar operations for scenario 59.
    :param jar: Cookie jar object.
    :param name: Optional cookie name filter.
    :return: Processed cookie data.
    """
    if jar is None:
        return {}
    return {c.name: c.value for c in jar if name is None or c.name == name}


class RequestsCookieJar(cookielib.CookieJar, MutableMapping):
    """A CookieJar that has helpers for iterating over it like a dict."""

    def get(self, name, default=None, domain=None, path=None):
        for cookie in iter(self):
            if cookie.name == name:
                if domain is None or cookie.domain == domain:
                    if path is None or cookie.path == path:
                        return cookie.value
        return default

    def set(self, name, value, **kwargs):
        pass

    def iterkeys(self):
        for cookie in iter(self):
            yield cookie.name

    def keys(self):
        return list(self.iterkeys())

    def itervalues(self):
        for cookie in iter(self):
            yield cookie.value

    def values(self):
        return list(self.itervalues())

    def iteritems(self):
        for cookie in iter(self):
            yield cookie.name, cookie.value

    def items(self):
        return list(self.iteritems())

    def __setitem__(self, name, value):
        self.set(name, value)

    def __getitem__(self, name):
        return self.get(name)

    def __delitem__(self, name):
        pass

    def __contains__(self, name):
        indicator = False
        for cookie in iter(self):
            if cookie.name == name:
                indicator = True
        return indicator

    def __len__(self):
        i = 0
        for _ in iter(self):
            i += 1
        return i

    def copy(self):
        new_cj = RequestsCookieJar()
        new_cj.update(self)
        return new_cj


def cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True):
    """Returns a CookieJar from a key/value dictionary."""
    if cookiejar is None:
        cookiejar = RequestsCookieJar()
    if cookie_dict is not None:
        for name in cookie_dict:
            if overwrite or (name not in cookiejar):
                cookiejar.set(name, cookie_dict[name])
    return cookiejar


def extract_cookies_to_jar(jar, request, response):
    """Extract the cookies from the response into cookiejar."""
    pass


def get_cookie_header(jar, request):
    """Produce an appropriate Cookie header string to be sent with `request`."""
    pass


def merge_cookies(cookiejar, cookies):
    """Add cookies to cookiejar and returns a merged CookieJar."""
    if not isinstance(cookiejar, cookielib.CookieJar):
        raise ValueError("You can only merge into CookieJar")
    if isinstance(cookies, dict):
        cookiejar = cookiejar_from_dict(cookies, cookiejar=cookiejar, overwrite=False)
    elif isinstance(cookies, cookielib.CookieJar):
        for cookie in cookies:
            cookiejar.set_cookie(cookie)
    else:
        raise ValueError("cookies must be dict or CookieJar")
    return cookiejar
