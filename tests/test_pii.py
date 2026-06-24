from groww_pulse.pii import scrub_pii

def test_scrub_email():
    text = "Contact me at user@example.com for details."
    scrubbed, count = scrub_pii(text)
    assert scrubbed == "Contact me at [REDACTED] for details."
    assert count == 1

def test_scrub_phone():
    text = "Call me at +91 9876543210 or 9876543210."
    scrubbed, count = scrub_pii(text)
    assert scrubbed == "Call me at [REDACTED] or [REDACTED]."
    assert count == 2

def test_scrub_aadhaar():
    text = "My Aadhaar is 1234 5678 9012."
    scrubbed, count = scrub_pii(text)
    assert scrubbed == "My Aadhaar is [REDACTED]."
    assert count == 1

def test_scrub_pan():
    text = "PAN card ABCDE1234F is attached."
    scrubbed, count = scrub_pii(text)
    assert scrubbed == "PAN card [REDACTED] is attached."
    assert count == 1

def test_no_pii():
    text = "This is a clean review."
    scrubbed, count = scrub_pii(text)
    assert scrubbed == text
    assert count == 0

def test_mixed_pii():
    text = "My email is test@test.com and phone is 123-456-7890."
    scrubbed, count = scrub_pii(text)
    assert scrubbed == "My email is [REDACTED] and phone is [REDACTED]."
    assert count == 2
