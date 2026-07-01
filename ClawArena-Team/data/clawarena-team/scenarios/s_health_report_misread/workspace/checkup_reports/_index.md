# checkup_reports/ -- Annual Checkup Documents

| File | Description |
|---|---|
| `encrypted_report.pdf` | **Encrypted** annual checkup PDF (password in tools/unlock_hint.txt) |
| `annual_checkup_export.html` | HTML export for quick review (ALT=187 U/L) |

NOTE: `encrypted_report.pdf` contains authoritative ALT value and imaging summary.
Decrypt with `pikepdf.open(path, password=<see tools/unlock_hint.txt>)`.
