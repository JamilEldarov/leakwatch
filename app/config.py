import os
import re
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


def csv_values(value: str) -> tuple[str, ...]:
    return tuple(v.strip() for v in value.split(",") if v.strip())


@dataclass(frozen=True)
class Settings:
    target_domain: str
    database_url: str
    paste_urls: tuple[str, ...]
    telegram_api_id: str
    telegram_api_hash: str
    telegram_channels: tuple[str, ...]
    webhook_url: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    domain = os.getenv("TARGET_DOMAIN", "acme-demo.example").strip().lower().lstrip("@")
    if not re.fullmatch(r"(?=.{3,253}$)[a-z0-9-]+(?:\.[a-z0-9-]+)+", domain):
        raise ValueError("TARGET_DOMAIN must be a valid DNS-style domain")
    return Settings(
        target_domain=domain,
        database_url=os.getenv(
            "DATABASE_URL", "postgresql+psycopg://leakwatch:dev-only-change-me@localhost:5432/leakwatch"
        ),
        paste_urls=csv_values(os.getenv("PASTE_URLS", "")),
        telegram_api_id=os.getenv("TELEGRAM_API_ID", "").strip(),
        telegram_api_hash=os.getenv("TELEGRAM_API_HASH", "").strip(),
        telegram_channels=csv_values(os.getenv("TELEGRAM_CHANNELS", "")),
        webhook_url=os.getenv("WEBHOOK_URL", "").strip(),
    )
