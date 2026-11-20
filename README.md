# 🛡️ LeakWatch

**Organizational Data Leak Monitoring & Early-Warning System** — 24-hour cybersecurity hackathon MVP.

> ⚠️ Educational prototype. A keyword/domain match is not evidence that an organization has been breached. Demo data is fully synthetic.

## Scope of the starter

✅ Synthetic Telegram/Pastebin/Rentry events
✅ Domain-scoped regex entity extraction (emails, usernames, domain, document markers)
✅ PostgreSQL findings with SHA-256-based deduplication
✅ Explainable LOW/MEDIUM/HIGH risk scoring
✅ Streamlit dashboard with filters, metrics, charts, redacted CSV
✅ Optional Telegram search **inside configured public channels** via Telethon
✅ Optional fetching of **explicit public raw paste URLs** from Pastebin, Rentry and paste.rs
✅ Optional HTTPS webhook for new HIGH findings
✅ Pytest and GitHub Actions CI

❌ No cross-platform keyword discovery across every paste site; requires external search/discovery integrations.
❌ No ownership confirmation, scheduled scanner, real-time streaming or production access control yet.

## 1. Windows setup (PowerShell)

Install Python 3.11+, Git and Docker Desktop, and make sure Docker is running.

```powershell
cd leakwatch-starter
Copy-Item .env.example .env
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
docker compose up -d db
python run_scan.py --demo
streamlit run dashboard.py
```

If your installed Python is newer and `py -3.11` is unavailable, use `py -m venv .venv`. Check dashboard at <http://localhost:8501>.

If PowerShell blocks venv activation, use `cmd.exe` with `.venv\Scripts\activate.bat`, or run `.\.venv\Scripts\python.exe` directly. Avoid weakening the machine-wide execution policy.

### Linux/macOS

```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
docker compose up -d db
python run_scan.py --demo
streamlit run dashboard.py
```

**Database:** Postgres runs locally on `127.0.0.1:5432`. The `.env` password is for local demo only, not production. If database connection fails, run `docker compose ps` and inspect `docker compose logs db`.

## 2. Run tests

```bash
python -m pytest -q
```

## 3. Explicit public paste monitoring (optional)

Edit `.env` and set URLs **you are authorized to retrieve**, for example:

```ini
PASTE_URLS=https://pastebin.com/raw/REPLACE_WITH_VALID_ID,https://rentry.co/raw/replace-with-valid-id
```

Then:

```bash
python run_scan.py --pastes
```

The starter **does not discover paste URLs automatically** and doesn't scrape private or authenticated content. Pastebin or Rentry may throttle or block automated requests; use controlled samples and follow service policies.

## 4. Telegram collector (optional)

Get your own `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` from <https://my.telegram.org>. Set:

```ini
TELEGRAM_API_ID=123456
TELEGRAM_API_HASH=YOUR_OWN_API_HASH
TELEGRAM_CHANNELS=public_channel_username,another_public_username
```

Run **in a terminal**:

```bash
python run_scan.py --telegram
```

The first Telethon run may request phone and a login code. Store the `.sessions/` folder privately. This searches **the monitored domain within the named public channels**, not globally, and only when permitted by platform rules.

## 5. Alerts (optional)

Set `WEBHOOK_URL` to a trusted HTTPS endpoint accepting a JSON body with `text`, then scan again with new findings. Only new HIGH alerts are delivered; raw content is not sent. Slack-compatible hooks are straightforward; other services may need payload adaptation.

## 6. Upload to GitHub

Create a new **private** repo using the GitHub website or GitHub CLI. If using `gh`, authenticate first (`gh auth login`) and then run:

```bash
git init
git branch -M main
git add .
git commit -m "feat: scaffold LeakWatch MVP"
gh repo create leakwatch --private --source=. --remote=origin --push
```

If the GitHub repository already exists, do **not** run `gh repo create` again; instead use `git remote add origin https://github.com/OWNER/REPO.git` then `git push -u origin main`.

Before publishing, check `git status` and `git ls-files` to make sure `.env`, `.sessions`, and authentic evidence are not tracked. Invite collaborators under **Settings → Collaborators**, and create branch-specific PRs rather than pushing everything to `main`.

## 7. Team workflow

```bash
git checkout -b feature/telegram-collector
# make change
git add .
git commit -m "feat: improve public Telegram collector"
git push -u origin feature/telegram-collector
```

Open a Pull Request and have a second teammate review/merge. Use GitHub Issues to track tasks.

## Files

```
app/
  config.py           env settings
  models.py           SQLAlchemy schema
  db.py               database initialization
  detector.py         regex entity extraction and masking
  risk.py             risk score + explanation
  pipeline.py         deduplication and persistence
  alerts.py           optional HTTPS alerts
  collectors/
    demo.py           synthetic events
    pastes.py         explicit raw-paste URLs
    telegram.py       public channel search
run_scan.py            command-line collection entry point
dashboard.py           Streamlit application
docker-compose.yml     PostgreSQL
requirements.txt       Python dependencies
tests/                 unit tests
docs/                  architecture, timeline and pitch
.github/workflows/     pytest CI
SECURITY.md            safe-use policy
```

## Ethics & limitations

Use only synthetic data or sources you have authorization to inspect. Respect rate limits and platform terms. Never upload real leaked credentials to GitHub, demo slides or screenshots. There is no authentication on the dashboard: keep it on localhost. This MVP is **post-exposure detection and triage**, not DLP prevention.

See [Architecture](docs/ARCHITECTURE.md), [Hackathon timeline](docs/24H_PLAN.md) and [Demo script](docs/DEMO_SCRIPT.md).
