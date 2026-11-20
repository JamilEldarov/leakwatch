from app.detector import Entity
from app.risk import score_finding


def test_high_with_document_and_secret_keyword():
    email = Entity("email", "hr@acme-demo.example")
    other = Entity("document_marker", "CONFIDENTIAL")
    domain = Entity("domain", "acme-demo.example")
    score, level, reason = score_finding(email, "CONFIDENTIAL secret=FAKE", [email, other, domain])
    assert score == 100
    assert level == "HIGH"
    assert "document-related" in reason


def test_domain_only_low_risk():
    domain = Entity("domain", "acme-demo.example")
    assert score_finding(domain, "acme-demo.example", [domain])[:2] == (25, "LOW")
