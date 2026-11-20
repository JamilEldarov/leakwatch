"""Optional alerting. Never transmit raw paste content or full discovered email values."""
import logging
from urllib.parse import urlsplit

import requests

from app.config import get_settings
from app.models import Finding

log = logging.getLogger(__name__)


def notify_high_risk(finding: Finding) -> None:
    url = get_settings().webhook_url
    if not url or finding.risk_level != "HIGH":
        return
    if urlsplit(url).scheme != "https":
        log.warning("WEBHOOK_URL must use HTTPS; skipping")
        return
    payload = {
        "text": (
            f"LeakWatch HIGH risk ({finding.risk_score}/100): {finding.entity_type} "
            f"{finding.entity_masked} on {finding.source_name}. "
            f"Source: {finding.source_url} — investigate, do not assume compromise."
        )
    }
    try:
        requests.post(url, json=payload, timeout=6).raise_for_status()
    except requests.RequestException as exc:
        log.warning("Webhook delivery failed: %s", exc)
