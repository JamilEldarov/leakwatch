"""Every sample is synthetic. Never load authentic leaked credentials into a demo."""
from app.config import get_settings
from app.pipeline import ingest_text


def seed_demo() -> int:
    domain = get_settings().target_domain
    samples = [
        ("telegram", "Demo Telegram", "demo://telegram/101", f"Interesting domain: {domain}"),
        ("telegram", "Demo Telegram", "demo://telegram/102", f"username=training_user login page for {domain}"),
        ("pastebin", "Demo Pastebin", "demo://pastebin/201", f"Contact security@{domain}; internal systems list"),
        ("rentry", "Demo Rentry", "demo://rentry/301", f"CONFIDENTIAL PAYROLL — synthetic example only — hr@{domain}"),
        ("pastebin", "Demo Pastebin", "demo://pastebin/202", f"password=FAKE_ONLY example for it@{domain}"),
    ]
    return sum(ingest_text(source_type, source_name, url, text) for source_type, source_name, url, text in samples)
