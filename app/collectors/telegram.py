"""Keyword search within explicitly configured public Telegram channels."""
import re
from pathlib import Path

from app.config import get_settings
from app.pipeline import ingest_text


def normalize_public_channel(channel: str) -> str:
    channel = channel.strip().removeprefix("@").removeprefix("https://t.me/")
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{4,31}", channel):
        raise ValueError(f"Expected public channel username, got: {channel!r}")
    return channel


async def scan_telegram() -> int:
    try:
        from telethon import TelegramClient
    except ImportError as exc:
        raise RuntimeError("Install the Python requirements first") from exc

    settings = get_settings()
    if not (settings.telegram_api_id and settings.telegram_api_hash and settings.telegram_channels):
        raise ValueError("Set TELEGRAM_API_ID, TELEGRAM_API_HASH and TELEGRAM_CHANNELS in .env")
    Path(".sessions").mkdir(exist_ok=True)
    client = TelegramClient(".sessions/leakwatch", int(settings.telegram_api_id), settings.telegram_api_hash)
    total = 0
    async with client:
        for item in settings.telegram_channels:
            channel = normalize_public_channel(item)
            # Telegram searches within this public channel, not the entire platform.
            async for message in client.iter_messages(channel, search=settings.target_domain, limit=50):
                if message.message:
                    total += ingest_text(
                        "telegram", f"@{channel}", f"https://t.me/{channel}/{message.id}", message.message
                    )
    return total
