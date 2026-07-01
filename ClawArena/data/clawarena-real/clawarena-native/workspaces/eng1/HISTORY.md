# Requests HISTORY

## 2.32.5 (2025-08-18)

**Bugfixes**

- Reverted the SSLContext caching behaviour introduced in 2.32.3 due to compatibility
  issues with certain environments.

**Dependencies**

- Bumped minimum urllib3 requirement.

---

## 2.32.4 (2025-06-10)

**Security**

- Fixed CVE-2024-47081: ``get_netrc_auth`` used ``ri.netloc.split(':')[0]`` to
  extract the hostname for netrc lookup. A crafted URL such as
  ``http://example.com:@evil.com/`` would cause credentials for ``example.com``
  to be sent to ``evil.com``. The fix replaces the vulnerable extraction with
  ``ri.hostname``, which is correctly parsed by Python's ``urllib.parse.urlparse``
  and does not include userinfo. Users who cannot upgrade immediately should set
  ``trust_env=False`` on their Session objects as a workaround.

  Credit: Maxime Villard (GHSA-9hjg-9r4m-mvj7, CVE-2024-47081).

---

## 2.32.3 (2024-05-29)

**Bugfixes**

- Fixed SSLContext handling to prevent caching issues with certain versions of
  urllib3. This was not a security fix.

**Dependencies**

- Updated certifi to 2024.2.2.

---

## 2.31.0 (2023-05-22)

**Security**

- Fixed CVE-2023-32681: ``Proxy-Authorization`` headers were inadvertently forwarded
  to destination servers when following redirects through an HTTPS proxy. The fix
  strips the ``Proxy-Authorization`` header when the scheme changes or when a
  non-proxy redirect is encountered.

  This was assigned GHSA-j8r2-6x86-q33q.

**Features**

- Added support for ``trust_env=False`` to disable all environment variable based
  configuration including ``.netrc`` file reading and proxy environment variables.

---

## 2.30.0 (2023-03-08)

**Features**

- Improved streaming response handling performance.
- Added ``PreparedRequest.copy()`` method.

**Bugfixes**

- Fixed content-length header setting for chunked uploads.

---

## 2.29.0 (2023-01-12)

**Bugfixes**

- Fixed an issue with digest auth nonce counting.
- Improved proxy URL parsing to handle edge cases.

---

## 2.28.2 (2023-01-12)

**Bugfixes**

- Fixed urllib3 compatibility issue.

---

## 2.28.0 (2022-06-09)

**Features**

- Added experimental support for the ``airport_fee`` field in TLC integrations
  (internal note: not applicable to requests library itself).

---

## 2.27.0 (2021-12-15)

**Features**

- Python 3.10 compatibility improvements.

---

## 2.26.0 (2021-07-13)

**Improvements**

- Performance improvements for large request bodies.

---

## 2.25.1 (2021-01-02)

**Bugfixes**

- Fixed urllib3 pinning issue.

---

## 2.25.0 (2020-11-11)

**Features**

- Added Brotli content encoding support.

---

## 2.24.0 (2020-06-17)

**Improvements**

- Improved JSON decoding error messages.

---

## 2.23.0 (2020-02-19)

**Features**

- Improved proxy handling for complex network topologies.

---

## 2.22.0 (2019-05-15)

**Features**

- Added support for the ``idna`` package for international domain names.

---

## 2.21.0 (2019-01-22)

**Bugfixes**

- Fixed an edge case in redirect handling.

---

## 2.20.0 (2018-10-18)

**Security**

- Dropped support for Python 2.6, 3.3 which are no longer maintained.
  Avoided importing pyOpenSSL where urllib3 does not offer it.

---

## 2.19.1 (2018-06-14)

**Bugfixes**

- Fixed regression in 2.19.0.
