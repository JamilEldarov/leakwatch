"""Ingest metadata and redacted indicators; deduplicate by source/event/entity."""
import hashlib

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.alerts import notify_high_risk
from app.config import get_settings
from app.db import get_session
from app.detector import extract_entities, mask_entity
from app.models import Finding
from app.risk import score_finding


def ingest_text(source_type: str, source_name: str, source_url: str, text: str) -> int:
    if not text or len(text) > 200_000:
        return 0
    domain = get_settings().target_domain
    entities = extract_entities(text, domain)
    inserted: list[Finding] = []
    with get_session() as session:
        for entity in entities:
            fp_raw = f"{source_type}|{source_url}|{entity.kind}|{entity.value.casefold()}"
            fingerprint = hashlib.sha256(fp_raw.encode()).hexdigest()
            if session.scalar(select(Finding.id).where(Finding.fingerprint == fingerprint)) is not None:
                continue
            score, level, reason = score_finding(entity, text, entities)
            finding = Finding(
                fingerprint=fingerprint,
                source_type=source_type,
                source_name=source_name,
                source_url=source_url,
                entity_type=entity.kind,
                entity_masked=mask_entity(entity),
                entity_sha256=hashlib.sha256(entity.value.casefold().encode()).hexdigest(),
                matched_domain=domain,
                risk_score=score,
                risk_level=level,
                reason=reason,
            )
            session.add(finding)
            # Flush in one batch, then commit. Precheck handles typical repeated scans.
            inserted.append(finding)
        if inserted:
            try:
                session.commit()
            except IntegrityError:
                # A concurrent worker may insert the same fingerprint; avoid duplicate alerts.
                session.rollback()
                return 0
        for finding in inserted:
            notify_high_risk(finding)
    return len(inserted)
