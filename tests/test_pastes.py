import pytest

from app.collectors.pastes import validate_paste_url


@pytest.mark.parametrize("url", [
    "http://pastebin.com/raw/Abcd1234", "https://127.0.0.1/a",
    "https://pastebin.com/Abcd1234", "https://pastebin.com.evil.example/raw/Abcd1234",
    "https://pastebin.com/raw/Abcd1234?redirect=1",
])
def test_rejects_unapproved_urls(url):
    with pytest.raises(ValueError):
        validate_paste_url(url)


def test_accepts_supported_raw_urls():
    assert validate_paste_url("https://pastebin.com/raw/Abcd1234") == "pastebin.com"
    assert validate_paste_url("https://rentry.co/raw/example-1") == "rentry.co"
