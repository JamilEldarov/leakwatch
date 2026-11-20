from app.detector import Entity, extract_entities, mask_entity


def test_scoped_email_and_username():
    text = "CONFIDENTIAL user=alice login for acme-demo.example; security@acme-demo.example"
    result = extract_entities(text, "acme-demo.example")
    assert Entity("email", "security@acme-demo.example") in result
    assert Entity("username", "alice") in result
    assert Entity("document_marker", "CONFIDENTIAL") in result
    assert Entity("domain", "acme-demo.example") in result


def test_other_domain_not_scoped():
    assert extract_entities("admin@different.example", "acme-demo.example") == []


def test_subdomain_not_misclassified_as_target():
    assert extract_entities("abc.acme-demo.example", "acme-demo.example") == []


def test_email_masking():
    assert mask_entity(Entity("email", "security@acme-demo.example")) == "se***@acme-demo.example"
