"""Conservative regex detection; a domain match is NOT proof of breach or ownership."""
import re
from dataclasses import dataclass

EMAIL_RE = re.compile(r"(?<![\w.+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w.-])")
USERNAME_RE = re.compile(r"\b(?:user(?:name)?|login)\s*[:=]\s*([A-Za-z0-9._-]{3,40})", re.I)
DOC_RE = re.compile(r"\b(CONFIDENTIAL|INTERNAL[ -]ONLY|PAYROLL|EMPLOYEE[ -]RECORDS)\b", re.I)


@dataclass(frozen=True)
class Entity:
    kind: str
    value: str


def extract_entities(text: str, target_domain: str) -> list[Entity]:
    """Only return relevant entities from text mentioning the scoped domain."""
    domain = target_domain.lower().strip()
    domain_re = re.compile(r"(?<![a-z0-9.-])" + re.escape(domain) + r"(?![a-z0-9.-])", re.I)
    if not domain_re.search(text):
        return []

    found: set[tuple[str, str]] = set()
    found.add(("domain", domain))

    for email in EMAIL_RE.findall(text):
        if email.rsplit("@", 1)[-1].lower() == domain:
            found.add(("email", email.lower()))
    for username in USERNAME_RE.findall(text):
        found.add(("username", username))
    for keyword in DOC_RE.findall(text):
        found.add(("document_marker", keyword.upper()))

    return [Entity(kind, value) for kind, value in sorted(found)]


def mask_entity(entity: Entity) -> str:
    if entity.kind == "email":
        local, domain = entity.value.split("@", 1)
        return local[:2] + "***@" + domain
    if entity.kind == "username":
        return entity.value[:2] + "***"
    # A domain or document classification marker is non-sensitive metadata.
    return entity.value
