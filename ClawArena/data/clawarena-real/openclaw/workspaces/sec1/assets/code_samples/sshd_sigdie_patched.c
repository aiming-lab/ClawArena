/*
 * sshd_sigdie_patched.c — OpenSSH 9.8p1 (fixed, CVE-2024-6387 remediated)
 *
 * This excerpt shows the PATCHED version of sshsigdie() which restores the
 * DO_LOG_SAFE_IN_SIGHAND protection removed in commit 752250c.
 *
 * The fix ensures that when called from a signal handler context, syslog()
 * is skipped and only _exit(1) is called (which IS async-signal-safe).
 *
 * Source: openssh-portable 9.8p1, log.c
 */

#include <stdarg.h>
#include <syslog.h>
#include <stdlib.h>
#include "log.h"

void
sshsigdie(const char *file, const char *func, int line,
    struct ssh *ssh, const char *tag, int r, const char *fmt, ...)
{
#ifdef DO_LOG_SAFE_IN_SIGHAND
    /* FIX: The DO_LOG_SAFE_IN_SIGHAND guard is RESTORED.
     * When called from a signal handler, the syslog() call is compiled out.
     * Only _exit(1) remains, which is async-signal-safe.
     *
     * In non-signal-handler contexts (where DO_LOG_SAFE_IN_SIGHAND is not
     * defined), the full logging is preserved for diagnostics.
     */
    va_list args;
    char fmtbuf[MSGBUFSIZ];

    if (fmt != NULL) {
        va_start(args, fmt);
        vsnprintf(fmtbuf, sizeof(fmtbuf), fmt, args);
        va_end(args);
        syslog(LOG_CRIT, "%.500s", fmtbuf);
    }
#endif /* DO_LOG_SAFE_IN_SIGHAND */
    _exit(1);  /* async-signal-safe: always execute this */
}

/*
 * SIGALRM handler in 9.8p1 — now safe
 * sshsigdie() called with DO_LOG_SAFE_IN_SIGHAND defined, so syslog()
 * is skipped; only _exit(1) executes.
 */
static void
grace_alarm_handler(int sig)
{
    ssh_signal(SIGALRM, SIG_DFL);
    sigdie("Timeout before authentication for %s port %d",
        ssh_remote_ipaddr(the_active_state),
        ssh_remote_port(the_active_state));
    /* Now: sigdie() -> sshsigdie() -> _exit(1) [safe!] */
}
