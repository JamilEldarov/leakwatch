"""Fetch only explicit public raw-paste URLs from supported hosts; no sitewide search."""
import re
from urllib.parse import urlsplit

import requests

from app.config import get_settings
from app.pipeline import ingest_text

# Restrict destinations and paths to avoid an open URL fetcher / SSRF.
RAW_PATHS = {
    "pastebin.com": re.compile(r"^/raw/[A-Za-z0-9]{4,32}$"),
    "rentry.co": re.compile(r"^/raw/[A-Za-z0-9_-]{3,64}$"),
    "paste.rs": re.compile(r"^/[A-Za-z0-9_-]{3,64}$"),
}


def validate_paste_url(url: str) -> str:
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https" or parsed.username or parsed.password or parsed.port
        or parsed.query or parsed.fragment or parsed.hostname not in RAW_PATHS
    ):
        raise ValueError("Only HTTPS raw-paste links on supported hosts are permitted")
    if not RAW_PATHS[parsed.hostname].fullmatch(parsed.path):
        raise ValueError("Paste URL must be an allowed raw-paste path")
    return parsed.hostname


def scan_paste_url(url: str) -> int:
    hostname = validate_paste_url(url)
    response = requests.get(
        url, timeout=(4, 10), allow_redirects=False, stream=True,
        headers={"User-Agent": "LeakWatch-Hackathon/0.1 (public-source monitoring)"},
    )
    try:
        if response.status_code != 200:
            raise ValueError(f"Paste fetch returned HTTP {response.status_code}")
        content_type = response.headers.get("Content-Type", "").lower()
        if content_type and not ("text/" in content_type or "application/octet-stream" in content_type):
            raise ValueError("Response is not text")
        data = bytearray()
        for chunk in response.iter_content(chunk_size=8192):
            data.extend(chunk)
            if len(data) > 200_000:
                raise ValueError("Paste larger than 200 KB; skipped")
        text = bytes(data).decode("utf-8", errors="replace")
        return ingest_text(hostname.split(".")[0], hostname, url, text)
    finally:
        response.close()


def scan_configured_pastes() -> tuple[int, list[str]]:
    total = 0
    errors = []
    for url in get_settings().paste_urls:
        try:
            total += scan_paste_url(url)
        except (requests.RequestException, ValueError) as exc:
            errors.append(f"{url}: {exc}")
    return total, errors
