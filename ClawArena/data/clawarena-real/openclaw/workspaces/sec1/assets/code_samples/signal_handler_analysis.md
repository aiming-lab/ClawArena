# Signal Handler Safety Analysis: CVE-2024-6387

## Summary

CVE-2024-6387 is a signal handler race condition in OpenSSH's server (sshd) affecting
versions 8.5p1 through 9.7p1 on glibc-based Linux systems.

## Root Cause

### The Original Protection (pre-2020)

OpenSSH 4.4p1 through 8.4p1 used a compile-time macro `DO_LOG_SAFE_IN_SIGHAND` to
guard calls to non-async-signal-safe functions within signal handlers:

```c
#ifdef DO_LOG_SAFE_IN_SIGHAND
    syslog(LOG_CRIT, "%.500s", fmtbuf);  /* Only in non-signal contexts */
#endif
    _exit(1);  /* Always safe */
```

This ensured that when called from a signal handler, only `_exit(1)` (which is
async-signal-safe per POSIX.1-2008) was executed.

### The Regression (Commit 752250caabda3dd24635503c4cd689b32a650794)

On 2020-10-16, Damien Miller committed a log infrastructure refactor. The commit
removed the `#ifdef DO_LOG_SAFE_IN_SIGHAND` guard from `sshsigdie()`, making `syslog()`
unconditionally callable from signal handler context.

**Commit details:**
- Hash: 752250caabda3dd24635503c4cd689b32a650794
- Author: Damien Miller (djmdjm@mindrot.org)
- Date: 2020-10-16
- Subject: "upstream: revised log infrastructure for OpenSSH"
- Files changed: 7 files, 154 additions, 133 deletions

This reintroduced CVE-2006-5051 — the original signal handler race condition fixed in 2006.

## POSIX Signal Safety Reference

Functions guaranteed async-signal-safe (POSIX.1-2008, relevant subset):
- `_exit(status)` ✓ — immediate process termination
- `write(fd, buf, count)` ✓ — raw I/O
- `kill(pid, sig)` ✓ — signal delivery
- `getpid()` ✓ — process ID query

Functions NOT async-signal-safe (may cause corruption if called from signal handler):
- `syslog()` ✗ — calls malloc() internally
- `malloc()` / `free()` ✗ — heap operations with internal locks
- `printf()` / `fprintf()` ✗ — buffered I/O with locking
- `fopen()` / `fclose()` ✗ — FILE* operations

## Fix Applied in 9.8p1

The fix reinstates `#ifdef DO_LOG_SAFE_IN_SIGHAND` in `sshsigdie()`, ensuring:
1. In signal handler context: only `_exit(1)` is called (async-signal-safe)
2. In normal logging context: full `syslog()` diagnostics are preserved
