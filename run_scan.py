"""CLI: python run_scan.py --demo | --pastes | --telegram | --all"""
import argparse
import asyncio
import sys

from app.collectors.demo import seed_demo
from app.collectors.pastes import scan_configured_pastes
from app.collectors.telegram import scan_telegram
from app.config import get_settings
from app.db import init_db


def main() -> int:
    parser = argparse.ArgumentParser(description="LeakWatch scoped collectors")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--demo", action="store_true", help="Insert fictional test indicators")
    group.add_argument("--pastes", action="store_true", help="Fetch explicitly configured paste URLs")
    group.add_argument("--telegram", action="store_true", help="Search configured public Telegram channels")
    group.add_argument("--all", action="store_true", help="Run demo + configured live collectors")
    args = parser.parse_args()
    settings = get_settings()
    print(f"Target: {settings.target_domain}")
    init_db()
    total = 0
    if args.demo or args.all:
        new = seed_demo()
        print(f"Synthetic demo: {new} new findings")
        total += new
    if args.pastes or args.all:
        new, errors = scan_configured_pastes()
        print(f"Pastes: {new} new findings")
        for error in errors:
            print(f"WARN: {error}", file=sys.stderr)
        total += new
    if args.telegram or args.all:
        if settings.telegram_channels:
            new = asyncio.run(scan_telegram())
            print(f"Telegram: {new} new findings")
            total += new
        else:
            print("Telegram skipped: no TELEGRAM_CHANNELS configured")
    print(f"TOTAL: {total} new findings; existing findings deduplicated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
