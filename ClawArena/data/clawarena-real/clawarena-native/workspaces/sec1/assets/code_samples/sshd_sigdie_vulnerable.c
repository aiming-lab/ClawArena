/*
 * sshd_sigdie_vulnerable.c — OpenSSH 8.5p1 to 9.7p1 (vulnerable to CVE-2024-6387)
 *
 * This excerpt shows the VULNERABLE version of sshsigdie() AFTER commit
 * 752250caabda3dd24635503c4cd689b32a650794 (2020-10-16) removed the
 * DO_LOG_SAFE_IN_SIGHAND protection.
 *
 * Source: openssh-portable, log.c (vulnerable versions)
 */

#include <stdarg.h>
#include <syslog.h>
#include <stdlib.h>
#include "log.h"

/* BUG: The #ifdef DO_LOG_SAFE_IN_SIGHAND guard was REMOVED by commit 752250c.
 * syslog() is NOT async-signal-safe. Calling it from a signal handler creates
 * a race condition exploitable when the main thread is inside malloc()/free().
 */
void
sshsigdie(const char *file, const char *func, int line,
    struct ssh *ssh, const char *tag, int r, const char *fmt, ...)
{
    va_list args;
    char fmtbuf[MSGBUFSIZ];

    /* This block was NOT protected by #ifdef DO_LOG_SAFE_IN_SIGHAND */
    if (fmt != NULL) {
        va_start(args, fmt);
        vsnprintf(fmtbuf, sizeof(fmtbuf), fmt, args);
        va_end(args);
        syslog(LOG_CRIT, "%.500s", fmtbuf);  /* NOT async-signal-safe! */
    }
    _exit(1);
}

/*
 * SIGALRM handler — called when LoginGraceTime expires
 * This calls sigdie() which calls sshsigdie() which calls syslog()
 */
static void
grace_alarm_handler(int sig)
{
    ssh_signal(SIGALRM, SIG_DFL);
    sigdie("Timeout before authentication for %s port %d",
        ssh_remote_ipaddr(the_active_state),
        ssh_remote_port(the_active_state));
    /* sigdie() -> sshsigdie() -> syslog() [race condition here!] -> _exit(1) */
}
