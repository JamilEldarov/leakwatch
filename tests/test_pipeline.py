from sqlalchemy import func, select

from app.collectors.demo import seed_demo
from app.config import get_settings
from app.db import engine, get_session, init_db
from app.models import Finding


def test_seed_demo_inserts_masked_findings_only_once(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    monkeypatch.setenv("TARGET_DOMAIN", "acme-demo.example")
    monkeypatch.setenv("WEBHOOK_URL", "")
    get_settings.cache_clear()
    engine.cache_clear()
    try:
        init_db()
        first_count = seed_demo()
        second_count = seed_demo()
        assert first_count >= 5
        assert second_count == 0
        with get_session() as session:
            assert session.scalar(select(func.count()).select_from(Finding)) == first_count
            emails = session.scalars(select(Finding).where(Finding.entity_type == "email")).all()
            assert len(emails) > 0
            assert all("***@" in f.entity_masked for f in emails)
            assert any(f.risk_level == "HIGH" for f in session.scalars(select(Finding)).all())
    finally:
        engine().dispose()
        engine.cache_clear()
        get_settings.cache_clear()
