# In the Matter of Knight Capital Americas LLC
## SEC Administrative Order — Release No. 34-70694
## Admin Proc. File No. 3-15570

**Source**: U.S. Securities and Exchange Commission
**Reference URL**: https://www.sec.gov/files/litigation/admin/2013/34-70694.pdf
**Date**: October 16, 2013

---

## Summary of Violations

Knight Capital Americas LLC ("Knight") violated Rule **15c3-5(b)** of the
Securities Exchange Act of 1934 (the "Market Access Rule") by failing to
maintain adequate financial risk management controls and supervisory procedures.

Knight agreed to pay a civil penalty of **$12,000,000** and to undertake
certain remedial measures.

---

## Factual Findings

### The Deployment (July 27 – August 1, 2012)

Knight employed a manual, undocumented deployment procedure. Beginning on
**July 27, 2012**, over a period of multiple days, Knight deployed new
Retail Liquidity Provider (RLP) code to its **8 SMARS servers** (Smart Market
Access Routing System), deploying to one server per day.

On **August 1, 2012**, the 8th and final SMARS server had not received the
new RLP code. Instead, it retained dormant "Power Peg" code from approximately
2005, which had been deactivated but not removed.

### The August 1, 2012 Incident

On **August 1, 2012**, beginning at market open (9:30 AM ET):

- Knight's SMARS system received **212 customer orders** for various equities
- The 8th server, running the legacy Power Peg code, began generating child orders
  at approximately **18,868 child orders per parent order**
- Over approximately **45 minutes** (9:30 AM to ~9:58 AM ET), SMARS generated
  **4,000,000+ child orders** in **154 stocks**
- Total shares traded: **397,000,000+ shares** (approximately 3.97 billion shares)

### The Automated Emails

Beginning at **8:01 AM ET**, over 90 minutes before market open, Knight's
automated monitoring system sent **97 automated emails** with subject line
"Power Peg disabled" to Knight's personnel. These warning emails were
not escalated or acted upon prior to market open.

### Financial Impact

The incident resulted in a trading loss exceeding **$460,000,000** (four hundred
sixty million dollars). This figure represents the net loss after Knight attempted
to unwind its positions in the affected securities over the days following August 1, 2012.

**Note**: Some preliminary and media reports cited an initial estimate of approximately
$440 million. The **authoritative SEC-confirmed figure is $460,000,000+** as stated
in SEC Press Release 2013-222.

### Shutdown

Knight's engineers identified the root cause and manually disabled SMARS at
approximately **9:58 AM ET**, approximately 45 minutes after the erroneous
ordering had begun.

---

## Rule Violations

Knight Capital Americas LLC violated:

**Rule 15c3-5(b)** — Knight failed to establish, document, and maintain a system
of risk management controls and supervisory procedures reasonably designed to
manage the financial risks of its market access. Specifically:

- Knight lacked a mechanism to identify that the 8th SMARS server had not received
  the new RLP deployment
- Knight did not halt trading upon receiving the 97 automated "Power Peg disabled"
  emails (a clear signal of system misconfiguration)
- Knight's supervisory procedures were not reasonably designed to prevent the type
  of erroneous ordering that occurred

---

## Penalty and Remediation

Knight Capital Americas LLC agreed to:
1. **Cease and desist** from committing or causing any violations of Rule 15c3-5(b)
2. **Pay a civil money penalty** of **$12,000,000**
3. Undertake certain compliance undertakings, including annual CEO certification
   and enhanced deployment procedures

---

*Admin Proc. File No. 3-15570 | Release No. 34-70694 | October 16, 2013*
