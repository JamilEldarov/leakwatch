# 3-minute jury demo script

**0:00–0:25 — Problem:** Organizations discover external exposure late. LeakWatch surfaces *candidate* indicators for investigation, without claiming to prove a breach.

**0:25–0:45 — Architecture:** Show Collector -> Regex -> Risk -> PostgreSQL -> Dashboard/Alert diagram.

**0:45–1:30 — Demonstration:** Open dashboard, click **Load synthetic demo**. Show the target domain, indicators, source types, masked values, HIGH/MEDIUM/LOW scoring and filtering. Reload and show the duplicate count stays unchanged.

**1:30–2:05 — Live collection:** Show configured public Telegram channel keyword search or explicit paste URL scan if source availability and authorization allow. If network is unavailable, show the pretested simulated data rather than claiming a live result.

**2:05–2:35 — Design decisions:** Explain why no full leaked passwords/documents are stored; source provenance, hash-based dedup and risk are visible.

**2:35–3:00 — Roadmap:** Wider source discovery, ownership verification, scheduled monitoring, false positive feedback, analyst workflows.

## Expected questions

- **Is this proof of a leak?** No; the indicator must be verified by an analyst.
- **Does it search every paste site?** No; MVP currently monitors explicit raw paste URLs.
- **Does it search Telegram globally?** No; only configured public channels.
- **Does it store leaked credentials?** No; masked indicators and metadata only.
