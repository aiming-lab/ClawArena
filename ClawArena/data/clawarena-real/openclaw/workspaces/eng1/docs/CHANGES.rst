Changelog
=========

2.32.4 (2025-06-10)
-------------------

**Security**

- Fixed CVE-2024-47081 (GHSA-9hjg-9r4m-mvj7): Netrc credential leakage via
  crafted URL in ``get_netrc_auth``. The vulnerability used ``ri.netloc.split(':')[0]``
  to extract the hostname, allowing a URL like ``http://example.com:@evil.com/`` to
  cause credentials for ``example.com`` to be forwarded to ``evil.com``. Fixed by
  using ``ri.hostname`` instead. Users unable to upgrade should set
  ``trust_env=False`` on their Session as a workaround. (:issue:`6964`, :pr:`6965`)

2.32.3 (2024-05-29)
-------------------

**Bugfixes**

- Fixed SSLContext caching issues with urllib3. (:pr:`6966`)

2.31.0 (2023-05-22)
-------------------

**Security**

- Fixed CVE-2023-32681 (GHSA-j8r2-6x86-q33q): ``Proxy-Authorization`` header
  was inadvertently forwarded to destination servers when following HTTPS proxy
  redirects. Fixed by stripping the header on scheme change. (:pr:`6491`)

**Features**

- Added ``trust_env=False`` to disable all environment-based configuration.

2.30.0 (2023-03-08)
-------------------

**Features**

- Improved streaming response handling.
- Added ``PreparedRequest.copy()`` method.

2.29.0 (2023-01-12)
-------------------

**Bugfixes**

- Fixed digest auth nonce counting edge case.

2.28.2 (2023-01-12)
-------------------

**Bugfixes**

- urllib3 compatibility fix.

2.28.0 (2022-06-09)
-------------------

**Features**

- Python 3.11 compatibility improvements.

2.27.0 (2021-12-15)
-------------------

**Features**

- Python 3.10 compatibility.

2.26.0 (2021-07-13)
-------------------

**Improvements**

- Large request body performance improvements.

2.25.1 (2021-01-02)
-------------------

**Bugfixes**

- urllib3 pinning issue fixed.

2.25.0 (2020-11-11)
-------------------

**Features**

- Brotli content encoding support.

2.24.0 (2020-06-17)
-------------------

**Improvements**

- Improved JSON decoding error messages.

2.23.0 (2020-02-19)
-------------------

**Features**

- Improved proxy handling.

2.22.0 (2019-05-15)
-------------------

**Features**

- ``idna`` package support for international domain names.

2.21.0 (2019-01-22)
-------------------

**Bugfixes**

- Redirect handling edge case fix.

2.20.0 (2018-10-18)
-------------------

**Security**

- Dropped Python 2.6 and 3.3 support.

2.19.1 (2018-06-14)
-------------------

**Bugfixes**

- Fixed regression from 2.19.0.
