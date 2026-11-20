# 24-hour hackathon plan

| Time | Goal | Evidence |
|---|---|---|
| 00:00–01:00 | Repo, roles, scope, backlog | Repository + README + Issues |
| 01:00–04:00 | Docker PostgreSQL + schema + sample data | DB running + demo records |
| 04:00–08:00 | Regex and dedup tests | CI green + detection outputs |
| 08:00–12:00 | Telegram public-channel collector + paste URL collector | Controlled collection logs |
| 12:00–16:00 | Dashboard + filters + risk visualization | Browser demo |
| 16:00–19:00 | Risk scoring + optional alert | Redacted alert screenshot |
| 19:00–21:00 | Debug, failure handling, integration | Verified end-to-end run |
| 21:00–23:00 | README, slides, demo script | Architecture + screenshots |
| 23:00–24:00 | Dry run + contingency | Stable 3-minute presentation |

## Roles (adapt to team size)

- **Coordinator / GitHub:** task board, PR review, integration, demo.
- **Collector engineer:** public Telegram channels and paste URL fetcher.
- **Detection engineer:** regex matching, scoring, deduplication, tests.
- **UI/DB engineer:** PostgreSQL schema, Streamlit dashboard, filters.
- **Demo/documentation:** scenario, screenshots, README, 3-minute pitch.

## Order of importance

1. A reliable synthetic end-to-end demonstration.
2. One working scoped live collector.
3. A second collector, filtering, visible prioritization.
4. Alert webhooks.
5. Scheduled background scanning (stretch goal).

Do not sacrifice the end-to-end working demo for broad source coverage.
